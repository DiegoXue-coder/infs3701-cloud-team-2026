"""Exercise the candidate over loopback using the approved T08 fixtures."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from threading import Thread
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import ProxyHandler, Request, build_opener

from werkzeug.serving import make_server


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "app/reading_tracker.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, required=True)
    args = parser.parse_args()

    fixtures = json.loads((ROOT / "tests/c_t08/fixtures.json").read_text(encoding="utf-8"))
    logger = load_module("t12_request_logger", ROOT / "scripts/c_request_log.py")
    label = "t12-local-candidate"
    with patch.dict(os.environ, {"READING_DATA_MODE": "local", "APP_INSTANCE": label}):
        tracker = load_module("t12_reading_tracker", SOURCE)

    server = make_server("127.0.0.1", 0, tracker.app)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    opener = build_opener(ProxyHandler({}), logger.NoRedirect())

    def call(path, form=None):
        data = urlencode(form).encode("ascii") if form is not None else None
        request = Request(base + path, data=data)
        try:
            response = opener.open(request, timeout=3)
        except HTTPError as error:
            response = error
        with response:
            return response.code, response.headers, response.read()

    print("Source SHA-256:", hashlib.sha256(SOURCE.read_bytes()).hexdigest(), flush=True)
    try:
        status, headers, body = call("/health")
        require(status == 200 and headers["X-App-Instance"] == label, "health status or instance mismatch")
        require(json.loads(body) == {"status": "ok", "stage": "reading-tracker", "instance": label},
                "health payload mismatch")
        print("PASS /health JSON and matching X-App-Instance", flush=True)

        for case in fixtures["future_http_cases"]:
            status, headers, _ = call("/", case["form"])
            require(status == case["expected_status"], f"{case['name']}: HTTP {status}")
            require(headers["X-App-Instance"] == label, f"{case['name']}: instance header mismatch")
            if status == 302:
                require(headers["Location"] == "/", "successful form redirected to unexpected path")
            print(f"PASS {case['name']}: HTTP {status}", flush=True)

        status, _, body = call("/")
        require(status == 200 and body.count(b"<h2>Synthetic</h2>") == 1,
                "expected exactly one accepted synthetic record")
        require(b'<div class="num">10</div><div class="lbl">Pages read</div>' in body,
                "expected 10 pages read")
        print("PASS GET / shows exactly one accepted record and 10 pages read", flush=True)

        summary = logger.sample(base + "/", 4, 0.2, 3, args.samples, "local-fixture")
        require(summary["successful_2xx"] == 4 and summary["instances"] == {label: 4},
                "expected four HTTP successes with the configured label")
        print("PASS sampler logged four successful requests with the configured instance label", flush=True)
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


if __name__ == "__main__":
    main()
