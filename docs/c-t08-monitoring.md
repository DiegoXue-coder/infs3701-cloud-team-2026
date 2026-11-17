# C's monitoring review and joint experiment steps

2026-11-04; this time only an offline check of existing configuration/records, with no AWS login or cloud experiment.

## Independent file check of the existing baseline

Checking `deployment/configure-monitoring-baseline.py`, `project/aws-resources.json`, `project/handoffs.json` and `docs/2026-11-01-foundation-verification.md`, the existing healthy-targets alarm definition is consistent: AWS/ApplicationELB, HealthyHostCount, Minimum, ALB+TG dimensions, 60 seconds, 2 consecutive points below 2, missing data notBreaching. This check only shows the repository files agree; it does not prove the current console configuration or health.

The threshold detects a drop in two-host redundancy: with 1 healthy host the service may still keep running. It is not an alarm for business transactions, database writes or a whole-site outage. notBreaching can make a total absence of data look untriggered, so it should be combined with independent HTTP availability samples and a manual check of data freshness. There is no notification recipient, so it cannot be claimed that an email was sent.

`deployment/c-t08-alarm-review.json` holds the exact expected baseline readback values and is not a deployment script. A should first read back the actual configuration and compare it with this file; to change the threshold or missing-data policy, first explain it on the task card and save the configuration from before the change. There is no need to recreate an alarm with the same name for the sake of C's contribution.

## Dashboard checklist

| Signal | Dimensions/statistic/period | Purpose and limitations |
| --- | --- | --- |
| HealthyHostCount / UnHealthyHostCount | LoadBalancer+TargetGroup；Minimum/Maximum；60s | 冗余/异常目标；同时读target health确认真实实例 |
| RequestCount / HTTPCode_Target_5XX_Count | LoadBalancer；Sum；60s | 流量与后端5xx；另看HTTPCode_ELB_5XX_Count区分LB错误；低流量时不要只看百分比 |
| TargetResponseTime | LoadBalancer；p95；60s | 目标响应延迟，低样本分位数不稳定；不可直接等同客户端整页耗时 |
| CPUUtilization | 每个InstanceId；Average；300s基本监控 | 定位资源压力；单独CPU不能证明业务可用 |
| ConsumedRead/WriteCapacityUnits | TableName；Sum；60s | DynamoDB用量；成功交易还需应用读写证据 |

正式业务上线后先取健康流量基线，再讨论延迟和5xx阈值；本次不捏造业务SLO。基线已有6个组件，新增图表由A确认，不为取证无限高频造流量。

## 给A的单实例实验请求（尚未发送/执行）

1. 确认B发布commit、两台实例同版本、两target均healthy，确认没有其他维护者同时操作；记录当前告警、健康检查interval/threshold/deregistration配置。C启动请求工具，`--count 300 --interval 1 --timeout 2`，输出新文件；在窗口不足时用新文件开启下一段，不能覆盖。
2. 先记录不少于30条基线样本。A记录UTC并只停止其中一台；另一台保留。预期健康数降至1，告警随后转ALARM；不能把两分钟评价窗口说成固定两分钟端到端检测时间。
3. C保留停机前后全部样本，记录观测失败数、首次/末次失败、各实例计数、最长连续失败；样本边界无法精确推断LB内部停止分流时刻。客户端1秒采样不能排除样本间短暂故障。
4. 获取实际指标点和告警历史，保存真实ALARM截图。禁止用SetAlarmState冒充实测。
5. A启动原实例并确认应用/target恢复，C记录恢复时间和OK历史、再取至少30条样本，并确认共享记录仍在。未恢复则停止进一步故障动作，交A排障；不停止另一台，不删除数据。
6. 保存前后配置、UTC操作记录、原始JSONL和截图，注明实际操作者A、C的取证工作。独立另一账号复核后再提交T12/T13/T14最终结论。

预期证据目录：`evidence/T12/`分流日志与dashboard，`evidence/T13/`配置/指标/状态历史，`evidence/T14/`故障操作时间和请求日志。此处为保存约定，当前这些新证据尚未生成。

依据：[AWS ALB指标](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-cloudwatch-metrics.html)、[CloudWatch缺失数据处理](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/alarms-and-missing-data.html)。文档核对日期2026-11-04；阈值选择和实验安排为本项目方案。
