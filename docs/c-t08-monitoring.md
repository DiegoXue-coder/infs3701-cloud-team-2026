# C 监控复核与联合实验步骤

2026-11-04；本次仅离线检查已有配置/记录，未登录AWS或执行云端实验。

## 已有基线的独立文件检查

核对 `deployment/configure-monitoring-baseline.py`、`project/aws-resources.json`、`project/handoffs.json` 和 `docs/2026-11-01-foundation-verification.md`，现有健康目标告警定义一致：AWS/ApplicationELB、HealthyHostCount、Minimum、ALB+TG维度、60秒、连续2点低于2、缺失notBreaching。此检查只证明仓库文件相符，不证明当前控制台配置或健康。

该阈值检测双机冗余下降：1台健康仍可能持续提供服务。它不是业务交易、数据库写入或整站中断告警。notBreaching可能使全无数据看起来未触发，应结合独立HTTP可用性样本和人工核查数据新鲜度。没有通知收件人，不能声称已发送邮件。

`deployment/c-t08-alarm-review.json` 为精确的基线期望读回值，不是部署脚本。A应先读回实际配置，与此文件比较；若要改阈值或缺失策略，先在任务卡说明并保存变更前配置。无需为了C的贡献重复创建同名告警。

## dashboard核对表

| 信号 | 维度/统计/周期 | 用途与限制 |
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
