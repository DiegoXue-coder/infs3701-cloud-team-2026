# Reading Tracker release batches and operation record

Operator: DiegoXue-coder (A, assisted by this AI session). Application author: Alex4325Li (B). C's independent cloud review has not yet taken place.

In this session the user replied to the specific public scope below with "Agreed, release the fictional-data demo within this scope". The host-by-host release was then carried out; the preparation records in this file are kept at their original times, and the latest measured results are in this round's final handoff and execution evidence.

## Preparation completed

- Actual AWS query at 2026-11-07 12:01 UTC: both targets running/healthy, ALB active; /health returned 200 twice from az-a and twice from az-b, stage=infrastructure-only; GET / was still the foundation placeholder page. DynamoDB ACTIVE, strongly consistent COUNT actually 0 items, no further pages. Both gateway endpoints available. Alarm state OK, but the state reason is old data from 1 November, so this is not called a verification of current monitoring-data freshness. No notification subscriptions.
- The release source is pinned to `06c2292cdf0aca80f050709b8172fac3595b54cc`, with files taken directly from Git objects, independent of working-tree line endings.
- The package contains only `app.py` and `requirements.txt`; the plan and each file's hash: [business-release-plan.json](../project/business-release-plan.json). Package SHA256: `fc40e1969c6b90f154b120979aaddf45f554d6e5fdd0fa6b0b2d17fd2ac980cd`.
- The application package was uploaded to the existing private bucket and downloaded again to compare hashes; no public ACL. Path: `s3://infs3701-team-artifacts-214018170594/releases/reading-tracker/06c2292cdf0aca80f050709b8172fac3595b54cc/app.tar.gz`. CloudShell staging directory: `~/infs3701-release-06c2292`.
- Three offline tests passed, covering pinned-package/boot-payload parsing, restoring the old environment and blocking automatic retry on health failure, and a corrupted package being unable to switch the service. The offline tests use a simulated service and do not show that actual Linux/AWS recovery succeeds. Actual run log: [release-safety-tests.log](../evidence/T09/2026-11-07-A-release-safety-tests.log).

## Specific impact awaiting confirmation

Once the existing HTTP load-balancer entry point is switched from the foundation test page to Reading Tracker, any visitor who knows the address can view and add demo records; there is currently no login or CSRF protection. Enter only fictional book titles and test text, no private information. This batch adds no AWS resources, open ports, IAM permissions, accounts or member credentials; it still uses the original two private instances, LabInstanceProfile and the existing DynamoDB/S3 endpoints. HTTP has no TLS yet, so the security requirements cannot be called fully met.

## Operation order after confirmation

1. `python3 ~/infs3701-release-06c2292/release-business.py prepare --instance a --directory ~/infs3701-release-06c2292`. The script first confirms the other host is healthy, then stops A; it saves the original user-data attribute.
2. Query with inspect, wait until A is actually stopped, then run the `start` phase of the same command. It writes a per-boot script smaller than 16 KiB; no SSH, no IAM changes.
3. The boot script first keeps the foundation app and env, fetches the pinned package from private S3, checks the archive and both file hashes, checks the production Python's dependency lock, and sets dynamodb mode and the az-a label; the original systemd service keeps using Gunicorn on 8000. It reads /health and a real GET /, and on success prints `INFS3701_RELEASE_OK` with the commit/hashes/label. Externally, target health and the actual business page still need to be checked.
4. Only after the first host succeeds is the same done for B. A/B are `i-00572a14ca8b71156` (us-east-1a) and `i-0081259c52a32e051` (us-east-1b) respectively.
5. Create only a few fictional records with unique markers, record the label of the instance that received the POST, then read back from the other label; restart one host and confirm the same data can still be read. Keep the original records and screenshots, and do not empty the database.
6. Update the actual commit/labels and verification time in handoffs, and give Marina the real URL and exact version. She independently carries out the T12/T11-related retests; A's logs do not stand in for C's acceptance.

Each phase returns independently and does not loop stop/start. `inspect` shows target state and bounded project boot diagnostics, and does not print temporary keys.

## Failure and recovery

When health or the real business GET fails, the host script restores the paths and env from before that switch, restarts the old service and saves a failure-block marker for that commit; A must read the actual diagnostics and must not continue to the second host. The foundation directory and env from before the first deployment also have a non-overwritable backup.

Explicit return to the foundation version: first confirm the other host is healthy, stop the failed host with prepare, and once stopped run `rollback-start --instance a|b --directory ~/infs3701-release-06c2292`. The new per-boot script restores the foundation directory and env and verifies infrastructure-only. Do not use the old maintain-foundation.py restore-userdata as a business recovery; restoring only the EC2 attribute cannot clear the cached script. Before retrying a failed package, the cause must be investigated and the fix and failure-block marker reviewed; no automatic unlimited retries.

This method keeps the database, old EC2/S3, foundation backup and release files. An actual rollback has not yet been performed in the cloud, and no drill is claimed to have passed.
