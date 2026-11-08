# Reading Tracker

The app keeps the original form, reading list and statistics. The upgrade entry is
`app/reading_tracker.py`. The original archive is `reference/reading_tracker_candidate.py`.

## Run locally

From the repo root, with Python 3.9+:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r app/requirements.txt
READING_DATA_MODE=local APP_PORT=8000 APP_INSTANCE=local-dev .venv/bin/python app/reading_tracker.py
```

Open http://127.0.0.1:8000. Add a fictional book, then confirm it appears in the
list and the statistics update. Local data lives in one process and resets on restart.
Local mode uses the loopback address and never initializes the AWS SDK.

```sh
curl -i http://127.0.0.1:8000/health
.venv/bin/python -m unittest discover -s tests -p test_reading_tracker.py -v
```

Expect HTTP 200, `X-App-Instance: local-dev` and JSON with `stage: reading-tracker`.
Health verifies the process only. A failed storage operation on the book page
returns 503. Invalid form input returns 400.

## AWS handoff for Diego

Use Python 3.11 and the Flask, boto3 and Gunicorn versions on the existing image
(`deployment/runtime-requirements.lock`). The app adds no dependencies to that
image. From the exact commit named in the T07 receipt, copy
`app/reading_tracker.py` to `app.py` at the root of the release archive. Include the
runtime lock as `requirements.txt` for reference. Build it from a checkout of the
receipt's commit:

```sh
stage=$(mktemp -d)
cp app/reading_tracker.py "$stage/app.py"
cp deployment/runtime-requirements.lock "$stage/requirements.txt"
tar -czf "reading-tracker-$(git rev-parse --short HEAD).tar.gz" -C "$stage" app.py requirements.txt
```

Use the project's private release
bucket and approved maintenance path. The existing foundation maintenance script
is for the placeholder and does not deploy this archive.

On each private host, stage the archive in a fresh directory. Back up the current
app and `/etc/infs3701/app.env` before switching. Add
`READING_DATA_MODE=dynamodb` to the existing environment, and verify
`READING_TABLE=infs3701-team-books`, `AWS_DEFAULT_REGION=us-east-1`, `APP_PORT=8000`
and a distinct non-sensitive `APP_INSTANCE` on each host. The DynamoDB table is
already provisioned with String partition key `record_id` and no sort key. The app
uses only Scan and PutItem through the instance role. Legacy S3 records require a
separate migration and remain in the existing bucket.

Use the existing systemd service and its Gunicorn entry point
`gunicorn --bind 0.0.0.0:8000 --workers 2 app:app`. Switch one host at a time.
After restarting `infs3701-app`, check its journal, local `/health` and GET `/`.
Only proceed to the second host after the first returns the business page and the
expected instance label. If checks fail, restore that host's previous app and
environment, restart the service, and verify the prior health response and target
health before continuing. Keep the same DynamoDB table during rollback.

For acceptance, submit one uniquely named fictional book on host A and read it
on host B, then restart the application and confirm the same record is still
visible. Record the deployed commit, HTTP codes, instance labels and readback
before and after restart. Marina can then verify routing through the ALB.
The app scans all pages for the course-sized library to compute its statistics.
Scan cost grows with the table. Use a small number of fictional writes for validation.

## Published demo and independent verification

The [7 November release handoff](../docs/business-handoff-2026-11-07.md)
records the deployed commit, both host startup logs and A's write/read/restart
checks. Check the current endpoint and release in `project/handoffs.json`.
The AWS demo uses HTTP and fictional records. If health is unavailable, record
the status and time and ask A to check the Lab and target group. Run no writes
until both business labels are available. See [B's T11 checks](../docs/b-t11-verification.md).
