# T12 business read/write and two-instance routing

Marina057 accessed the official demo entry point from her own machine on 2026-11-07 23:42–23:44 AEDT. The released version `06c2292cdf0aca80f050709b8172fac3595b54cc` comes from A's host release record. This collection used public business HTTP. [Deployment handoff](business-handoff-2026-11-07.md)

| Check | Actual result |
| --- | --- |
| `/health` | `az-a` and `az-b` both HTTP 200, `stage=reading-tracker`, JSON instance name matches `X-App-Instance` |
| Original record | The fictional record kept by A appeared once on each instance, status reading, 12/120 pages, rating 4 |
| Independent business insert and readback | One POST returned HTTP 302 and `az-b` wrote `Fictional Marina T12 4efe5cd92f30`. Both hosts read back a single record, status reading, 7/35 pages, rating 3 |
| Business home-page routing | 2026-11-07 12:42:48.354–12:44:04.734 UTC, 30 consecutive GETs, HTTP 200 for all 30, `az-a` 15, `az-b` 15, with 0 errors and 0 missing instance labels |

The sampler waits 2 seconds after each request finishes. Median client time to response headers was 572 ms and P95 was 688 ms (nearest rank, 30 samples). This window reflects only one normal two-host test. [Execution log](../evidence/T12/2026-11-07-Marina057-cloud-run.log) · [original request JSONL](../evidence/T12/2026-11-07-Marina057-cloud-samples.jsonl)

## A/C joint-window handoff

Diego, please provide a 20–30 minute window both can attend, suggested for 8–9 November Sydney time, and open the Lab. C will review using the existing fictional records, to avoid inserting during a stop or timeout.

1. A confirms both hosts still run `06c2292` and both targets are healthy. Open `infs3701-team-dashboard` and confirm the ALB and target-group dimensions and the UTC time range. C provides this round's 12:42–12:44 UTC window, and A exports the matching healthy-targets, requests, target and ALB 5xx, and response-time graphs. If the old window is unavailable, leave a new baseline period before the joint experiment.
2. A checks the current parameters and history of `infs3701-team-healthy-targets-below-two`, verifying 60 seconds, two evaluations, minimum healthy targets below 2 and the missing-data policy. Both first record the UTC start time, healthy count and alarm state. C starts continuous business GETs every 2 seconds and saves the logs from before, during and after the stop in the same new file.
3. After the T11/T12 joint prerequisites are met, A stops only the specified instance and records the API confirmation time. C checks the surviving instance's HTTP responses, the retained records and target health. A saves the actual ALARM state and trigger time. C reports the failure count and sampling coverage, and records the time window of the switch to the surviving label.
4. A starts the original instance and confirms both targets are healthy again, saving the OK state and UTC time. C checks that both labels appear again and the same record is read back. If the other target becomes abnormal, A immediately restores the stopped instance, and C saves the actual anomaly without adding further failure actions.

The current report is a partial result. Formal T12 acceptance awaits T10 and CloudWatch evidence from the same period. Business-alarm trigger and recovery, and single-instance failure, belong to T13/T14 respectively. [Existing monitoring plan](c-t08-monitoring.md)
