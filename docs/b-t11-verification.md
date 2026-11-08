# B independent shared-data verification

B verified the source SHA-256 for `06c2292` against the startup evidence from
both hosts. This is a comparison with A's recorded logs. The DynamoDB path in
the release calls the shared table for each read and write. The in-memory store
is selected only by explicit local mode. No file stores reading records in the
deployed path.

On 8 November 2026 at 15:35:14 Sydney time the public ALB returned 503 for
GET /health without X-App-Instance. Preflight stopped before any POST. The
cause is unconfirmed. Diego should check Learner Lab state, both EC2 instances
and ALB target health, then confirm the business stage and both labels are back.
No application fix is indicated by this observation alone.

After restoration, run from the repository root with the current URL and
existing synthetic reference title from the release handoff:

```sh
.venv/bin/python scripts/b_t11_live.py --url "$BASE_URL" --reference-title "$REFERENCE_TITLE" --write-one-fictional
```

Save a new execution log. The script verifies the business health stage, the
existing reference record on each instance, then sends at most one fictional
POST. It expects 302 and reads the new record once per label with status
reading, 9/45 pages and rating 5. If a POST is ambiguous, read back its logged
unique title before attempting any further write. For restart verification,
coordinate with A and preserve the same title and values. A performs the restart
and B checks readback afterward without resubmitting. Record the instance
labels, status and timestamps. Marina independently reviews the evidence.
