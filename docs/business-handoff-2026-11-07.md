# Ready for joint testing: two-instance Reading Tracker

Operator A: DiegoXue-coder, assisted by Codex in this session. Measured up to **2026-11-07 12:28:05 UTC / 23:28:05 Sydney**. B/C should read this page and then review independently, without asking A again for the URL, version or labels. This is not C's test result.

## Real entry point and version

- [Business URL](http://infs3701-team-alb-788523332.us-east-1.elb.amazonaws.com/); `/health` on the same domain should return 200 and `stage=reading-tracker`, with the instance in the JSON matching `X-App-Instance`.
- Source commit: `06c2292cdf0aca80f050709b8172fac3595b54cc`. Both production Python3.11.18/Gunicorn hosts were checked to have the same source/archive hashes; the dependency lock matches. Do not infer the SHA from /health.
- Release package SHA256: `fc40e1969c6b90f154b120979aaddf45f554d6e5fdd0fa6b0b2d17fd2ac980cd`; app.py SHA256: `a0eb70b7e8a9505e912c14fead268e9c0798064e35708243404c250def1abfb5`.
- DynamoDB: `infs3701-team-books`, us-east-1, string primary key record_id. The mode is explicitly dynamodb, accessed through the instance role; no credentials were copied to teammates. Old S3 data was not migrated.

| Request label | Instance | AZ | Private address |
| --- | --- | --- | --- |
| az-a | i-00572a14ca8b71156 | us-east-1a | 10.37.10.88 |
| az-b | i-0081259c52a32e051 | us-east-1b | 10.37.11.110 |

Both hosts were healthy with no public IP when the target group was last read. HTTP 80 goes through the ALB to the application on 8000; IAM/security groups were not widened and no resources were added this time. The Lab limitation of a broad role still needs to be explained in the report.

## What A has actually verified

1. Both hosts were released one at a time, and real local business GET and health checks passed; the host boot logs record the pinned commit, source/package hashes, iam-role source and Python version. See [host A](../evidence/T09/2026-11-07-A-first-host-release.log), [host B](../evidence/T09/2026-11-07-A-second-host-release.log). The string "Reading Tracker" in the first external probe of host A also matches the placeholder page and cannot alone serve as evidence that B's code was released; B's later boot log, the stage and the business-form check are the basis.
2. At **12:25:06 UTC**, one fictional record was POSTed through the real ALB, returning 302, written by instance az-b. az-a/az-b then both returned 200 and both showed the business form and that record; a strongly consistent database query returned a single record with the expected field values. See [write/readback log](../evidence/T09/2026-11-07-A-cloud-write-read.log).
3. Unique title `Fictional cloud acceptance 95c34a0851c940db8b642eb3317d0a45`; record_id `effa5b9c-f7b6-4534-8cd3-c13ef4bb65dd`; reading, 12/120 pages, rating 4. This record is kept for B/C to review and must not be replaced with real personal data.
4. The writing host az-b was fully stopped and confirmed as stopped in the control plane; the ALB still returned 200 from az-a and showed the record. See [during the stop](../evidence/T09/2026-11-07-A-during-writer-stop.log). This is a single-instance stop check; loss of a whole AZ was not tested.
5. az-b was restarted, automatically read the same release package and kept the dynamodb configuration, and both targets were healthy again. At **12:28:04–05 UTC**, az-b and az-a again read the original record, and a strongly consistent query confirmed the record_id was unchanged. See [restart boot log](../evidence/T09/2026-11-07-A-restart-boot.log), [readback after restart](../evidence/T09/2026-11-07-A-post-restart-read.log). This is not a new record with the same name passed off as persistence.
6. The [real browser page screenshot](../evidence/T09/2026-11-07-A-reading-tracker-live.png) shows the shared-storage note, the form, 1 record, 12 pages and a 4.0 rating. The screenshot was taken after the first write; conclusions after the restart rest on the independent time-stamped HTTP/database logs.

## What B does right now

Alex4325Li: pull the latest main and check the deployment evidence and code against the T07 delivery; actually view it in a browser and add one unique fictional record, recording the status/response/field results. If you find an application problem, hand over reproducible input with expected/actual results, and give A a new commit after fixing. You can claim T11, independently check the shared-data and stateless evidence, and complete a retest with C; do not use A's logs to claim you ran the experiment yourself. Complete the full T04/T07 delivery and the application/database choices and trade-offs in the report.

## What C does right now

Marina057: pull the latest main and, following [your own T12 plan](c-t12-business-validation.md), first check the real stage, the two labels and the record above; no AWS login is needed, just visit the business URL and sample HTTP at low frequency. Using your existing tool is suggested:

```sh
python scripts/c_request_log.py --url http://infs3701-team-alb-788523332.us-east-1.elb.amazonaws.com/ --count 30 --interval 2 --timeout 5 --stage business-release --output evidence/T12/YOUR-NEW-BUSINESS-SAMPLES.jsonl
```

Change the output path to a new file with your actual date/username, check the label distribution, status codes and business page, and do not overwrite old evidence. Real add/readback can be done independently with a small amount of fictional data; restarts and AWS monitoring configuration need A's cooperation, without asking for passwords. The existing monitoring dashboard and alarm are still there, but this round has not yet aligned them with the latest metric graphs/business load or independently retested the alarm; the 1 November foundation alarm cannot be reused as this business-failure acceptance.

## What is still not complete

The HTTPS and domain approach awaits course confirmation; the public demo has no login/CSRF protection and uses fictional data only. A real whole-AZ failure, the full business-alarm flow and a cloud rollback drill were not performed. The report, architecture diagram, 12-month cost and video still need to be produced formally. The current application's strongly consistent full-table Scan suits only small course data; its cost/scaling limits must be explained.

The end of a Lab session may stop the instances; this page does not promise all-day availability. If access fails, first keep the time/HTTP error and do not rewrite or change permissions; check whether the Lab is on and have A restore the session. Stopping automatically affects the lab's running state; data retention has been tested. Do not treat the T09/T10 partial reports as the group's independent acceptance having fully passed.
