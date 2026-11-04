"""Bounded, read-only HTTP sampler. No credentials, response bodies or AWS SDK required."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler, ProxyHandler


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def sample(url, count, interval, timeout, output, stage):
    parts = urlsplit(url)
    if parts.scheme not in {'http', 'https'} or not parts.hostname or parts.username or parts.password or parts.query or parts.fragment:
        raise ValueError('Use an HTTP(S) URL without credentials, query parameters or fragments.')
    if not 1 <= count <= 600:
        raise ValueError('count must be 1..600')
    if not math.isfinite(interval) or not 0.1 <= interval <= 60:
        raise ValueError('interval must be 0.1..60 seconds')
    if not math.isfinite(timeout) or not 0.05 <= timeout <= 30:
        raise ValueError('timeout must be 0.05..30 seconds')
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    # No environment proxy for the explicitly local fixture; normal proxy policy elsewhere.
    handlers = [NoRedirect()]
    if parts.hostname in {'localhost', '127.0.0.1', '::1'}:
        handlers.append(ProxyHandler({}))
    opener = build_opener(*handlers)
    rows = []
    with output.open('x', encoding='utf-8') as handle:
        for index in range(count):
            started = time.perf_counter()
            row = {'sequence': index + 1, 'time_utc': datetime.now(timezone.utc).isoformat(timespec='milliseconds'), 'stage': stage, 'url': url, 'status': None, 'instance': None, 'error': None}
            try:
                request = Request(url, headers={'User-Agent': 'INFS3701-C-T08-readonly/1.0', 'Connection': 'close'})
                with opener.open(request, timeout=timeout) as response:
                    row['status'] = response.status
                    row['instance'] = response.headers.get('X-App-Instance')
            except HTTPError as error:
                row['status'] = error.code
                row['instance'] = error.headers.get('X-App-Instance')
                row['error'] = 'http_error'
                error.close()
            except (URLError, TimeoutError, OSError) as error:
                # Store the class, not exception text which could contain local network details.
                row['error'] = type(error).__name__
            row['elapsed_ms'] = round((time.perf_counter() - started) * 1000, 3)
            row['success'] = row['status'] is not None and 200 <= row['status'] < 300
            rows.append(row)
            handle.write(json.dumps(row, ensure_ascii=False) + '\n')
            handle.flush()
            if index + 1 < count:
                time.sleep(interval)
    summary = {'stage': stage, 'requests': len(rows), 'successful_2xx': sum(row['success'] for row in rows), 'failures': sum(not row['success'] for row in rows), 'missing_instance': sum(not row['instance'] for row in rows), 'instances': dict(Counter(row['instance'] for row in rows if row['instance'])), 'output': str(output), 'latency_scope': 'response headers only; not full page load', 'business_acceptance': False}
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default=os.environ.get('BASE_URL'))
    parser.add_argument('--count', type=int, default=12)
    parser.add_argument('--interval', type=float, default=1.0)
    parser.add_argument('--timeout', type=float, default=5.0)
    parser.add_argument('--output', required=True)
    parser.add_argument('--stage', required=True, choices=['local-fixture', 'infrastructure-only', 'business-release'])
    args = parser.parse_args()
    if not args.url:
        parser.error('Set BASE_URL or --url to the exact endpoint to sample.')
    try:
        summary = sample(args.url, args.count, args.interval, args.timeout, args.output, args.stage)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    return 0 if summary['failures'] == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
