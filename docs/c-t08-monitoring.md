# C's monitoring review and joint experiment steps

2026-11-04; this time only an offline check of existing configuration/records, with no AWS login or cloud experiment.

## Independent file check of the existing baseline

Checking `deployment/configure-monitoring-baseline.py`, `project/aws-resources.json`, `project/handoffs.json` and `docs/2026-11-01-foundation-verification.md`, the existing healthy-targets alarm definition is consistent: AWS/ApplicationELB, HealthyHostCount, Minimum, ALB+TG dimensions, 60 seconds, 2 consecutive points below 2, missing data notBreaching. This check only shows the repository files agree; it does not prove the current console configuration or health.

The threshold detects a drop in two-host redundancy: with 1 healthy host the service may still keep running. It is not an alarm for business transactions, database writes or a whole-site outage. notBreaching can make a total absence of data look untriggered, so it should be combined with independent HTTP availability samples and a manual check of data freshness. There is no notification recipient, so it cannot be claimed that an email was sent.

`deployment/c-t08-alarm-review.json` holds the exact expected baseline readback values and is not a deployment script. A should first read back the actual configuration and compare it with this file; to change the threshold or missing-data policy, first explain it on the task card and save the configuration from before the change. There is no need to recreate an alarm with the same name for the sake of C's contribution.

## Dashboard checklist

| Signal | Dimensions/statistic/period | Purpose and limitations |
| --- | --- | --- |
| HealthyHostCount / UnHealthyHostCount | LoadBalancer+TargetGroup; Minimum/Maximum; 60s | Redundancy/abnormal targets; also read target health to confirm the real instances |
| RequestCount / HTTPCode_Target_5XX_Count | LoadBalancer; Sum; 60s | Traffic and back-end 5xx; also check HTTPCode_ELB_5XX_Count to separate LB errors; at low traffic do not look only at percentages |
| TargetResponseTime | LoadBalancer; p95; 60s | Target response latency; percentiles are unstable with few samples; not directly equal to client full-page time |
| CPUUtilization | Per InstanceId; Average; 300s basic monitoring | Locates resource pressure; CPU alone cannot prove the business is available |
| ConsumedRead/WriteCapacityUnits | TableName; Sum; 60s | DynamoDB usage; successful transactions still need application read/write evidence |

After the formal business release, take a healthy-traffic baseline first and then discuss latency and 5xx thresholds; no business SLO is invented this time. The baseline already has 6 widgets; new graphs are confirmed by A, and traffic is not generated at unlimited frequency just to collect evidence.

## Single-instance experiment request to A (not yet sent/executed)

1. Confirm B's release commit, that both instances run the same version and both targets are healthy, and that no other maintainer is operating at the same time; record the current alarm and the health-check interval/threshold/deregistration configuration. C starts the request tool with `--count 300 --interval 1 --timeout 2`, writing to a new file; if the window is too short, start the next segment with a new file and never overwrite.
2. First record at least 30 baseline samples. A records the UTC time and stops only one host; the other stays up. Expected: healthy count drops to 1 and the alarm then changes to ALARM; the two-minute evaluation window must not be described as a fixed two-minute end-to-end detection time.
3. C keeps all samples from before and after the stop and records the observed failure count, first/last failure, per-instance counts and longest run of consecutive failures; sample boundaries cannot pinpoint the moment the LB stopped routing internally. One-second client sampling cannot rule out brief faults between samples.
4. Obtain the actual metric points and alarm history and save a real ALARM screenshot. Using SetAlarmState to pass off as a real test is prohibited.
5. A starts the original instance and confirms the application/target has recovered; C records the recovery time and OK history, takes at least 30 more samples and confirms the shared record is still there. If it has not recovered, stop further failure actions and hand over to A for troubleshooting; do not stop the other host and do not delete data.
6. Save the before/after configuration, UTC operation record, original JSONL and screenshots, noting the actual operator A and C's evidence work. Submit the final T12/T13/T14 conclusions only after an independent review by another account.

Expected evidence directories: `evidence/T12/` for routing logs and dashboard, `evidence/T13/` for configuration/metrics/state history, `evidence/T14/` for failure-operation times and request logs. This is a storage convention; none of this new evidence has been produced yet.

References: [AWS ALB metrics](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-cloudwatch-metrics.html), [CloudWatch missing-data handling](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/alarms-and-missing-data.html). Documentation checked on 2026-11-04; the threshold choice and experiment arrangement are this project's own plan.
