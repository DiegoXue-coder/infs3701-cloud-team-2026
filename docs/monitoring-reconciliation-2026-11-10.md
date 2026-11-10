# Business monitoring evidence retrieved on 10 November

A / DiegoXue-coder retrieved these actual AWS records through the authenticated Lab. This export is not C's independent review and is not a new fault experiment. Raw CloudShell output, including original timestamps and terminal wrapping: [history/metrics](../evidence/T13/2026-11-10-A-retrieved-business-history.log). Compare with A's7November T09 writer-stop/restart logs and C's T12 raw request log, not with the1November infrastructure-only experiment.

## Genuine business-stage alarm cycle

| AWS state event, UTC | Evaluated evidence | Interpretation |
| --- | --- | --- |
| 7Nov12:29:53.285, OK→ALARM | Minimum healthy-target values1.0 at12:25 and12:26 | Two below-threshold periods during the business writer-host stop |
| 7Nov12:30:53.284, ALARM→OK | Healthy-target value2.0 at12:27 | A real recovery datapoint caused the state recovery |

The history also contains an earlier12:24/12:25 cycle during rollout. Use the later business writer-stop cycle for the main business demonstration. State-evaluation timestamps lag datapoint times and the12:28 application readback; neither the configured two periods nor the one-minute interval between these state events is a measured service downtime or guaranteed end-to-end detection delay. No SetAlarmState call was made by this export. AlarmActions remains empty; no email notification was tested or claimed.

## Aligning C's normal-operation window

For7Nov12:42:00–12:45:00UTC,60-second periods:

| Metric |12:42|12:43|12:44|
| --- | ---: | ---: | ---: |
| HealthyHostCount, Minimum |2|2|2|
| RequestCount, Sum |12|23|2|
| TargetResponseTime, p95 seconds |0.240579|0.235912|0.144097|

RequestCount totals37. C's complete script logged2health calls,2original-record reads,1POST,2new-record reads and30routing samples:37HTTP calls. This numerical agreement supports the time-window reconciliation; aggregate metrics are not unique per-client trace attribution. C's routing sample remains30/30HTTP200,15per label, rather than37routing samples.

The target and ALB5xx queries returned empty datapoint arrays. Keep them empty; do not manufacture zero-valued samples. C's client results independently show zero failed requests in its sample. Client response-header timing and target-response timing have different boundaries, so their p95values should not be equated.

## Dashboard correction and next review

The dashboard still described a foundation-only service. A backed it up in CloudShell as `/home/cloudshell-user/infs3701-dashboard-2026-11-10-before.json`, then updated its descriptive text and added the existing native `HTTPCode_ELB_5XX_Count` series to the request/error widget. No alarm threshold, missing-data policy, notification recipient or AWS permission was changed. API readback matched the submitted six-widget configuration at2026-11-10T07:15:08.222997Z. [Actual console screenshot](../evidence/T12/2026-11-10-A-dashboard-current.png).

C can now independently compare the raw history, A's stopped-writer evidence and her own request JSONL. If complete transition-failure counts or new video footage are needed, arrange one short continuous-sampling window with A and only stop one host after the other is confirmed healthy. Existing sparse A samples do not establish zero downtime or a whole-AZ failure. Do not repeat every completed test automatically, and do not approve T13/T14 merely because this document exists.
