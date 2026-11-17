# T08 review: preparation stage passed

Date: 2026-11-06 (Australia/Sydney). Reviewing account: DiegoXue-coder (A); submitting account: Marina057 (C). The user explicitly authorised the assistant in this chat to carry out the review and record the conclusion. Commands, code checks and document checks were run by Codex in A's workspace; it is not claimed that Diego ran them by hand, that Marina self-approved or that another real person separately signed off.

## Conclusion and versions

**T08 "test checklist, report outline, cost assumptions" passes preparation-stage acceptance, with no defects blocking approval.** This is not acceptance of the final business, AWS deployment, HTTPS, cost quote or video.

Submission receipt reviewed: R-T08-6624791560; submitted version: `cb07163da0e2beb69797902b433efd8999fd4849`; delivery file: `deliveries/T08/2026-11-04-Marina057.json`. The Git blobs of the current delivery and 15 evidence files were compared one by one with the submission receipt, and all 16 match; the blobs after working-tree filtering were also checked; Marina's commit, original logs and samples were not modified.

Rerun environment: Windows 11, Python3.12.14, an isolated virtual environment for the repository. The original execution times and full environment are in the logs below; there were no AWS operations, and only the HTTP tool tests used a temporary 127.0.0.1 service.

## Actual checks

| Item | Review action and result | Evidence |
| --- | --- | --- |
| Statistics and samples | Independently calculated the expected record count, status counts, pages and ratings for the four fictional samples; reran the 10 statistics tests, all passed, including old format, exceptions, order and input immutability | [Statistics rerun log](../../evidence/T08/2026-11-06-A-review-statistics.log) |
| HTTP logging tool | Read the script and tests and reran the 7 loopback tests, all passed; covering BASE_URL, success, 503, timeout, missing instance header, parameter boundaries and overwrite protection | [HTTP tool rerun log](../../evidence/T08/2026-11-06-A-review-http-tool.log) |
| Monitoring baseline | Parsed only the AST and configuration without executing deployment code; the 11 expected fields and ALB/TG dimensions match | [Alarm source check log](../../evidence/T08/2026-11-06-A-review-alarm-source.log) |
| Versions and historical evidence | All 16 committed blobs match; the original 4 JSONL lines are indeed local-fixture-only, HTTP 200, sequence 1–4; original files kept | [Integrity result](../../evidence/T08/2026-11-06-A-review-integrity.json), [execution log](../../evidence/T08/2026-11-06-A-review-integrity.log) |
| Core test plan | Covers real interface/input validation, shared database state, routing, single-host failure, the limits of the AZ design, monitoring, network permissions, encryption and scaling; lists actions, expectations, evidence and roles | [Test plan](../c-t08-test-plan.md) |
| Monitoring and failure preparation | Metric dimensions, statistical period, threshold reasoning, missing-data limitation, no notification recipient, before/during/after-stop samples and recovery steps are all explicit; faking alarm state by hand is prohibited | [Monitoring plan](../c-t08-monitoring.md) |
| Cost preparation | us-east-1, 12 months, 8760-hour scenario, including EC2/EBS/ALB/database/S3/snapshots/monitoring/transfer/public IPv4/network endpoints; clearly separates workload assumptions, prices still to be filled in and the historical Lab balance | [Cost assumptions](../c-t08-cost-assumptions.md) |
| Report and video preparation | The eight-part report outline covers the brief's requirements; the 60-second video shot plan requires real business operation, routing/availability and explanation of decisions; drafts, real contribution and the limits of AI use are labelled | [Report and video draft](../c-t08-report-and-video.md) |

This round checked the extracted text of the original brief/rubric and the T08 task card. T08 requires executable preparation, an item-by-item acceptance plan, a report outline and estimate assumptions, and does not require all T12/T13/T14/T18/T20 results while there is no business release yet.

## Handling of the hash difference

On rerun the raw SHA-256 of the original source was `f50fea5190314216ffcffb4c175d0a0dcf9dd5c57c2c69449e4ef73cb0856947`, while Marina's log has `f1f20663612aa3343f5bce9f9acc749da2c8def46eea8e369fdcdc7bfd7e5d10`. It was verified that the local working tree is CRLF while the Git index and Marina's copy are LF; after normalising to LF the SHA is identical, and the whole-file AST also matches the original snapshot. This is therefore a line-ending difference, not different business code, and the historical log does not need rewriting.

## Follow-up reminders (do not block T08 preparation acceptance)

- The Python3.11 target environment, new business HTTP, real DynamoDB writes, shared data and cloud failure tests are still to be run after T07/T09; the current 17 passes cannot be used to claim these are done.
- The current statistics tests isolate the old function; later the calls/tests must be updated to follow B's actual version, and behaviour such as the old function accepting negative values is not treated as adequate input validation.
- The request tool records time only to the response-header stage, and the manual stage label does not automatically prove deployment; the final failure experiment must cover before and after the stop and save actual times and failed samples.
- Live monitoring readback, notification and missing-data policy, HTTPS, Calculator prices/PDF, the formal report/video and the replies on course conflicts are still handled in later tasks.

This review approves only the T08 preparation task within the scope above; other task statuses, other members' contributions and personal signatures are determined by each person's actual work. The GitHub comment and sync receipt are the basis for the status taking effect.
