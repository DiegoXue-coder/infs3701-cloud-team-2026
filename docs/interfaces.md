# Shared development conventions

On 2026-10-31, after the project owner authorised setting up the self-service workflow, the following development defaults were specified; the machine-readable entry is `project/handoffs.json`. These are implementation requirements and do not mean they are implemented, deployed or signed off by everyone.

| Item | Development default | Implemented/provided by |
| --- | --- | --- |
| Port | APP_PORT, default 8000 | B implements, A configures deployment |
| Local address | http://127.0.0.1:8000, development only | B; used by C for testing |
| Process health | GET /health; not the same as successful database read/write | B |
| Instance identification | Response header X-App-Instance, configured by APP_INSTANCE | B implements, A gives the two instances different non-sensitive labels |
| Test address | BASE_URL, with no single host's address hard-coded | C |
| Data fields | record_id, title, status, pages_read, total_pages, rating, note, created_at | B adds types/constraints, C writes expectations |
| Local data | Explicit development mode, with no AWS credentials and no AWS requests | B |
| Cloud database | DynamoDB, us-east-1, table infs3701-team-books, record_id:String; READING_TABLE/AWS_DEFAULT_REGION; code still to be connected | Written to handoffs after A/B check |
| Start method | B delivers dependencies and a reproducible command; port 80 in the old file is not the new default | B |
| Deployed version | Both instances on the same commit, configuration recorded separately | A |

The old code does not yet implement the new interfaces above; the current baseline verification only checks syntax and the statistics function. The actual cloud URL, database and deployed version are still empty, and no values are invented. Parameter changes are handed over through GitHub files and task records, not announced only in private chat.

Target cloud runtime: Python3.11, Gunicorn WSGI entry app:app; the release-package and extra-dependency rules are in docs/aws-owner-handoff.md.

## B's first-round data contract (2026-11-03, awaiting A/C review)

The following are T04 design conventions and must not be regarded as existing behaviour before T07 is implemented.

| Field | Type and constraints |
| --- | --- |
| record_id | Server-generated UUID string, DynamoDB partition key; inserts with the same title in the same second must not overwrite either |
| title | 1–120 characters after trimming leading/trailing whitespace, required |
| status | want / reading / finished, default reading; any other explicitly supplied value returns 400 |
| pages_read | Non-negative integer, default 0 |
| total_pages | Non-negative integer, default 0 meaning unknown; when known, pages_read must not exceed total_pages |
| rating | null or an integer 1–5; an empty form value becomes null |
| note | String, default empty, at most 2000 characters |
| created_at | Server-side UTC ISO 8601 string with time zone; callers must not overwrite it |

Statistics keep the old meaning: total is the record count, each status is counted separately, the total_pages statistics key actually represents cumulative pages_read (not the books' total pages), avg_rating averages only non-empty ratings to one decimal place, and is null when there are no ratings. Progress pct is a derived display value, round(pages_read / total_pages * 100) when total pages are known and null when unknown; it is not a required database field. The list is in descending created_at order, stabilised by record_id for equal times.

### Data-layer and HTTP contract

- load_books() -> list[dict]: returns normalised records; a read failure must raise explicitly and must not be shown as an empty library. DynamoDB Scan must handle LastEvaluatedKey; for small course data only, full-table statistics do not suit large scale.
- save_book(entry) -> str: inserts after validation and returns record_id; DynamoDB uses a conditional write to avoid overwriting, and a failure must not return a success redirect. No edit/delete interface is provided.
- GET /: HTML list and statistics; POST /: form insert, 302 back to / on success; 400 on invalid input, 503 on storage failure, and the page does not expose internal exceptions or credentials.
- GET /health: 200 JSON, meaning the process can respond, without reading the database; it cannot serve as verification of cloud writes. All responses include X-App-Instance, with the value from APP_INSTANCE, default local-dev, and the machine's private address is not used.

### Draft configuration and start-up

READING_DATA_MODE must explicitly select local or dynamodb. local is for development only, uses in-memory records cleared on restart, does not import/call boto3, look for credentials or send AWS requests, and the development server binds only to 127.0.0.1. dynamodb uses READING_TABLE and AWS_DEFAULT_REGION and refuses to start if configuration is missing; the cloud uses the instance role, and copying credential files is prohibited. Old S3 data is not automatically migrated or deleted.

Draft local command after T07 is implemented: `READING_DATA_MODE=local APP_PORT=8000 APP_INSTANCE=local-dev .venv/bin/python app/reading_tracker.py`. The current old code does not support it yet, so do not treat it as a verified start command.

Deployment uses Python 3.11, Flask+boto3 and Gunicorn, with the release package's app.py exposing app:app; draft command `gunicorn --bind 0.0.0.0:8000 app:app`. Dependency versions should be handed to A after actual verification and alignment with deployment/runtime-requirements.lock; this time only dependency installation and the offline check of the old statistics were completed on macOS Python 3.9.6, and the Python3.11 release package is not yet verified.

The database stays with the DynamoDB A already chose: independent documents with no joins needed, managed multi-AZ, and on-demand billing that suits intermittent experiments; the trade-offs are the cost/latency of full-table statistics Scans and the current throughput cap. Read the table and region from handoffs.json. A/C, please check deployment and test feasibility in T04; T07 implementation, local testing and actual cloud acceptance are still needed.

## T07 implementation update (2026-11-07)

The local command, field validation, health endpoint and storage interfaces above
are implemented in `app/reading_tracker.py`. See [app startup and AWS handoff](../app/README.md).
Page counts support up to 38 digits in both modes to fit DynamoDB's number type.
The cloud health JSON identifies the release stage as `reading-tracker`.
Actual AWS write/read and restart persistence remain deployment acceptance checks.

## Published database contract (2026-11-08)

The 7 November release handoff records DynamoDB mode on both hosts for
`06c2292`. Local mode is development-only. A successful conditional PutItem
creates one UUID-keyed record, and each subsequent list request scans the same
table with ConsistentRead on each page. Scan does not offer snapshot isolation
across pages. A complete write/read check uses the business page and verifies
the same unique record and values from both labels. Health alone checks only
the serving process. See [release evidence](business-handoff-2026-11-07.md)
and [B verification](b-t11-verification.md).
