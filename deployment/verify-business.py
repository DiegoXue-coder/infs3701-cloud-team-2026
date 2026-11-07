"""Small live acceptance probe: one fictional POST, bounded low-rate readback.

Run write once after both business hosts are healthy. Run read before and after
restarting the recorded writer host. No data deletion or repeated POST retries.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request
from uuid import uuid4

URL = 'http://infs3701-team-alb-788523332.us-east-1.elb.amazonaws.com'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['write', 'read'])
    parser.add_argument('--state', type=Path, required=True)
    args = parser.parse_args()
    if args.phase == 'write':
        assert not args.state.exists(), 'Existing acceptance state; never repeat POST automatically'
        state = {'title': 'Fictional cloud acceptance ' + uuid4().hex, 'created_at': datetime.now(timezone.utc).isoformat()}
        # Persist the intent before POST, preventing accidental duplicate retries.
        args.state.write_text(json.dumps(state))
        body = urllib.parse.urlencode({'title': state['title'], 'status': 'reading', 'pages_read': '12', 'total_pages': '120', 'rating': '4', 'note': 'Fictional course test only; cross-instance and restart validation.'}).encode()
        request = urllib.request.Request(URL + '/', data=body, headers={'Content-Type': 'application/x-www-form-urlencoded'}, method='POST')
        try:
            response = urllib.request.build_opener(NoRedirect).open(request, timeout=15)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            state.update(post_status=response.code, write_instance=response.headers.get('X-App-Instance'), redirect=response.headers.get('Location'))
        args.state.write_text(json.dumps(state, indent=2))
        print('LIVE_WRITE=' + json.dumps(state), flush=True)
        assert state['post_status'] == 302 and state['write_instance'] in ('az-a', 'az-b') and state['redirect'] == '/'
    else:
        state = json.loads(args.state.read_text())
    found, health_labels = set(), set()
    for attempt in range(24):
        with urllib.request.urlopen(URL + '/', timeout=15) as response:
            page, label = response.read().decode(), response.headers.get('X-App-Instance')
            visible = state['title'] in page
            business = '<form method="post">' in page and 'shared reading library' in page
            print('LIVE_READ=' + json.dumps({'at': datetime.now(timezone.utc).isoformat(), 'status': response.status, 'instance': label, 'record_visible': visible, 'business_form': business}), flush=True)
            assert response.status == 200 and visible and business
            found.add(label)
        with urllib.request.urlopen(URL + '/health', timeout=5) as response:
            health = json.load(response)
            assert response.status == 200 and health['stage'] == 'reading-tracker' and health['instance'] == response.headers.get('X-App-Instance')
            health_labels.add(health['instance'])
        if found == {'az-a', 'az-b'} and health_labels == found:
            break
        time.sleep(1)
    assert found == health_labels == {'az-a', 'az-b'}, 'Both labels must be observed'
    import boto3
    table = boto3.Session(region_name='us-east-1').resource('dynamodb').Table('infs3701-team-books')
    result = table.scan(ConsistentRead=True)
    records = list(result['Items'])
    while result.get('LastEvaluatedKey'):
        result = table.scan(ConsistentRead=True, ExclusiveStartKey=result['LastEvaluatedKey'])
        records.extend(result['Items'])
    matches = [x for x in records if x.get('title') == state['title']]
    assert len(matches) == 1
    record = matches[0]
    assert int(record['pages_read']) == 12 and int(record['total_pages']) == 120
    assert record['rating'] == 4 and record['status'] == 'reading'
    if state.get('record_id'):
        assert record['record_id'] == state['record_id'], 'Same record must survive restart'
    state['record_id'] = record['record_id']
    args.state.write_text(json.dumps(state, indent=2))
    print('LIVE_ACCEPTANCE_OK=' + json.dumps({'title': state['title'], 'record_id': state['record_id'], 'writer': state['write_instance'], 'read_instances': sorted(found), 'health_instances': sorted(health_labels), 'same_record_verified': True}), flush=True)


if __name__ == '__main__':
    main()
