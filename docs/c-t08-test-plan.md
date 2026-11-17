# C / T08 test and evidence plan

Author account: Marina057; AI assistance: Codex. 2026-11-04. The first round of tests was run locally before role enrolment. On 2026-11-04 Marina057 was enrolled as C and claimed T08; claim receipt R-T08-6624693113. The scope submitted here is T08 test preparation; later cloud verification belongs to T12/T13/T14.

## Scope already executed

Based on a copy of the main source downloaded through Chrome; the page corresponds to commit 6a8da48b5fc5d932bc25a56054a1cd0cc605c5b8. Windows / Python 3.12.14; the cloud target Python 3.11 has not yet been retested. Flask/boto3 were not imported, AWS was not connected to, and no cloud resources were created or changed.

- `tests/c_t08/fixtures.json`: four fictional sets of statistics records with hand-computed expectations; plus eight future HTTP acceptance inputs.
- `tests/c_t08/test_statistics.py`: extracts the original function by AST; all 10 tests pass; covers page semantics, exclusion of unrated items, order invariance, duplicate records, input immutability, the old format and behaviour with abnormal values.
- `scripts/c_request_log.py`: a read-only HTTP request tool with a bounded number of requests.
- `tests/c_t08/test_request_log.py`: 7 real loopback HTTP tests pass, covering BASE_URL, 200, 503, timeout, missing instance header, parameter limits and protection against overwriting evidence.
- The four successful responses in the persistent sample `evidence/T08/2026-11-04-local-fixture-requests.jsonl` all come from `local-fixture-only` and are not load-balancer or Reading Tracker business evidence.

SHA-256 of the original function: `f1f20663612aa3343f5bce9f9acc749da2c8def46eea8e369fdcdc7bfd7e5d10`. The statistics tests do not prove that HTTP input validation, DynamoDB read/write or the Python3.11 deployment pass.

## How to reproduce

In the repository root, with Python 3.9+ (3.12.14 this time):

```text
python tests/c_t08/test_statistics.py
python tests/c_t08/test_request_log.py
```

The second command starts a temporary loopback test service and shuts it down automatically; it needs no dependency installation or AWS identity. The first run saves four local samples; when that evidence file already exists it uses a temporary output and does not overwrite history.

PowerShell example for accessing a specified environment (run only after confirming the endpoint/version):

```powershell
$env:BASE_URL='http://127.0.0.1:8000/health'
python scripts/c_request_log.py --count 12 --interval 1 --timeout 5 --stage local-fixture --output evidence/T08/new-local-requests.jsonl
```

Get the cloud entry point from the latest `project/handoffs.json`; use `--stage infrastructure-only` for the foundation environment and `--stage business-release` only after the business release. stage is a manual label and cannot automatically prove deployment identity. The script does not save bodies or follow redirects; timing ends at the response headers and is not full-page load time. Return code 0 means all samples were 2xx; 1 means at least one failed. If the file already exists it refuses to overwrite. To identify routing, check both `instances` and `missing_instance`; a 200 does not mean the database is working.

## Core acceptance matrix (not yet executed)

| Requirement | Action and expected result | Evidence | Operation/check |
| --- | --- | --- | --- |
| Usable interface and back end | Add one fictional record to B's released version; after the 302 the list and statistics are accurate; invalid input returns 400 and is not written; a storage failure returns 503, not an empty list | Version, input, HTTP output, browser screenshot, record ID | C executes, B reviews |
| Shared managed data/stateless | Read several times after adding and confirm different instances show the same record; the record remains after a single-host restart; DynamoDB read/write checked independently | Instance header, same record_id, table record, restart time | A operates AWS, C collects evidence, B checks |
| Routing | Confirm both instances have the same version/labels and send continuous requests; expect the sample to show at least both labels, with no strict 50:50 requirement | Full per-request JSONL, instance counts, target health state | C executes, A reviews |
| Instance failure | First confirm both hosts are healthy; C samples continuously while A stops one host at a time; record transitional failures and recovery, then confirm both healthy after the fix | Stop/start UTC, first/last failure, failure count, original monitoring and request logs | A stops/starts, C records, B reviews |
| AZ resilience | Check the cross-AZ topology and managed database; if the course allows, then design and approve an AZ-level experiment; one single-host stop proves only that experiment's scope | Subnet/AZ mapping, statement of actual experiment coverage | A provides, C checks |
| Monitoring | Read back the actual dashboard/alarm; ALARM after a real drop in healthy count, OK after recovery | Configuration JSON, metric points, state history, UTC screenshots | A operates, C checks independently |
| Network/least privilege | Check the ALB entry point, back end accepting only the ALB as source, private hosts without public IP, instance role and database/bucket policies | Read-only configuration and evidence of denied out-of-scope access; do not widen permissions | A reads, C checks |
| Encryption | Check EBS/bucket/database encryption; valid browser HTTPS and certificate; back-end link explained separately | Certificate, listener, encryption attributes | A operates, C checks; HTTPS currently not accepted |
| Horizontal scaling | Check the application keeps no persistent local state; adding instances/auto scaling, if enabled, needs a separate real experiment | Version configuration, instance changes, request and data consistency | A/B implement, C collects evidence |

## Input boundaries and defect handoff

B's 2026-11-03 contract is in `docs/interfaces.md`. Besides the eight items in the fixtures, still to test: title at 120/121 characters, note at 2000/2001 characters, integer boundaries, same title in the same second not overwriting, users unable to overwrite created_at, multi-page DynamoDB Scan, and a clear error on read failure. These tests have not been run against the business HTTP yet.

The original statistics function accepts some invalid values (for example negative pages, unknown status), and non-numeric strings raise ValueError; this records the old function's behaviour and is not adequate input validation. B should validate before storing, and C re-accepts on the actual T07 version. Do not modify the old code or describe expected rules as existing features.

For each problem record: version/address, reproducing input, expected, actual, UTC, log path, owner A/B or to be located, and retest result after the fix. There is currently no business version, so the risks above are not yet a failure finding against B's new implementation.
