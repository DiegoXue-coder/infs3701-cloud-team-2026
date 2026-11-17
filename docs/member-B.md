# Member two: application development, ready to start once you have the repository

> Latest entry point and actual limitations: [this round's verification and three-person handoff](2026-11-01-foundation-verification.md). The new ALB can already be used for foundation checks, and the business application is not yet released; do not treat the earlier "entry point not created" records below as the latest state.


First set up your own AI/GitHub/Python through the [self-service entry](self-service.md) and join B. Only repository access is needed, not the project owner's AWS credentials. The current old code is at `app/reading_tracker.py`, with the original archive at `reference/reading_tracker_candidate.py`.

2026-11-01 handoff update: A has created the DynamoDB table infs3701-team-books (us-east-1), primary key record_id:String, with READING_TABLE and AWS_DEFAULT_REGION as configuration. Target runtime is Python3.11; read docs/aws-owner-handoff.md, with no need to wait for a new database selection, and do not ask for A's AWS credentials. The business code is not yet connected and still needs your own real implementation and testing.

## First item T04: give everyone the same running conventions

Read `project/handoffs.json`. The development targets are specified: port 8000 (APP_PORT), `/health`, instance response header X-App-Instance, configuration APP_INSTANCE, and BASE_URL on the test side. They are requirements to be implemented, which the old code does not yet have, so do not claim they already run.

1. Read the old code, run the baseline check, and record the original S3 read/write dependency.
2. In `docs/interfaces.md` fill in the record fields, status values, statistics behaviour, configuration names and data-layer function contract. Follow the settled port/paths and do not ask the project owner to guess values again.
3. Provide the deployment dependencies and a draft start-up, listing the differences between local development and real AWS modes.
4. Save the check record and report; submit only once the fields/API really meet T04's acceptance, and wait for C's independent check. T07 can still be prepared before the first item is complete.

## Prepare T07 at the same time: the first runnable version

- First add a test-data mode clearly labelled local/development, making sure this path does not call boto3 or need any AWS identity; bind only to a local address for development use.
- Add the health path, a non-sensitive instance identifier and input handling; keep the original features and provide one copyable start command. Write any new dependencies into requirements.
- Implement the adapter code against the existing DynamoDB table and handoffs.json, separating the data read/write interface first; if a real feature lacks permission, give A a specific operation/resource request on the task card. Do not switch databases yourself or wait for a new selection, and do not pause the local version.
- Use fictional data to show the actual results of insert/query and statistics; local data is not evidence for the final managed database.

## The package for A/C

Report the real version in `deliveries/T07/`, attaching: commit, dependencies, start command, configuration variables, sample inputs and outputs, data mode, health path, test records and known issues. A deploys from this; C tests from this. Do not hand over a version that says "the code is done" with no run instructions.

## While waiting for A to deploy

Continue input and statistics tests, database code, run instructions and the application chapter; read C's failure cases from the Issue and reproduce them. After A updates the real URL, help with cloud verification; without cloud permission, record accurately that A actually executed and B designed/guided.
