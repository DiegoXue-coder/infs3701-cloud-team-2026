# T09 pre-release check for the business release (2026-11-07)

DiegoXue-coder's AI read the latest T07/T12 deliveries and reran the local candidate. Candidate commit: `06c2292cdf0aca80f050709b8172fac3595b54cc`. The version checked out here shows no differences from that commit's app/reading_tracker.py and runtime dependency lock.

## Actually passed

- 4 application tests: [log](../evidence/T09/2026-11-07-A-candidate-app-tests.log). Covers local insert and readback, health and instance header, Stubber tests of DynamoDB pagination/conditional write, storage failure and configuration validation.
- 17 C regression tests: [log](../evidence/T09/2026-11-07-A-candidate-regression.log).
- Local HTTP health, 8 form inputs, page readback and 4 samples: [log](../evidence/T09/2026-11-07-A-candidate-http.log), [JSONL](../evidence/T09/2026-11-07-A-candidate-local-samples.jsonl).

The environment is local Windows/Python3.12.14; the above is not Linux/Python3.11/Gunicorn or real AWS acceptance. This round did not deploy, upload an AWS release package, write to the cloud database, stop/start instances or publish the business page. T07 should stay partial until real writes, cross-instance readback and persistence after restart are verified.

## Must be handled for the formal release

The per-boot script of the existing `deployment/maintain-foundation.py` rewrites `/etc/infs3701/app.env` and suits only the foundation placeholder service; it lacks the `READING_DATA_MODE=dynamodb` the new application requires and does not install the business package. Copying app.py alone and restarting is not a complete release method.

The release needs a reviewable new business boot/release procedure: pin the commit and package hash above; read from the existing private S3 release prefix; keep the existing app, environment and version information; set READING_DATA_MODE, READING_TABLE, AWS_DEFAULT_REGION and APP_INSTANCE correctly; verify Gunicorn and the runtime dependencies; release one host at a time, checking local health and a real business read before handling the other. On failure restore that host's previous app and environment, keep the database, and recheck target health.

The originally planned host labels are az-a/az-b; the current instance, ALB and database state must be re-read in this signed-in Lab, and the 1 November state is not treated as current. IAM and networking in principle reuse existing resources; if new permissions turn out to be needed, record the specific difference first. The old EC2 and old S3 records are not automatically migrated or rewritten.

The public entry point has so far been approved only for the HTTP foundation test page. Before actually replacing it with a Reading Tracker that can add/read data, the public demo page and the scope of data writes must be explained to the user and the corresponding confirmation obtained; use only fictional test data. HTTPS is still a separate open item and is not described as all security requirements passing.

## Handoff to Marina after release

Record in T09/T10 and handoffs the real business URL, deployed commit, source/package hashes, the two labels and their instance/AZ mapping; provide the first cloud insert/readback results. First verify that the instance behind the other label can read the same record, then restart one host to confirm the data persists, and finally C retests independently and records routing/failure/alarm. Receiving the request in the screenshot does not mean these operations have been completed.
