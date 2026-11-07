# 已可联调：双实例 Reading Tracker

操作者A：DiegoXue-coder，由本会话Codex协助。实测至 **2026-11-07 12:28:05 UTC / 23:28:05 Sydney**。B/C请读取本页后独立复核，不必再向A索取网址、版本或标签。此次不是C的测试结果。

## 真实入口与版本

- [业务网址](http://infs3701-team-alb-788523332.us-east-1.elb.amazonaws.com/)；同域 `/health` 应为200、`stage=reading-tracker`，实例JSON与 `X-App-Instance` 一致。
- 源码commit：`06c2292cdf0aca80f050709b8172fac3595b54cc`。两台生产Python3.11.18/Gunicorn已核对相同源码/归档哈希；依赖锁匹配。不从/health推断SHA。
- 发布包SHA256：`fc40e1969c6b90f154b120979aaddf45f554d6e5fdd0fa6b0b2d17fd2ac980cd`；app.py SHA256：`a0eb70b7e8a9505e912c14fead268e9c0798064e35708243404c250def1abfb5`。
- DynamoDB：`infs3701-team-books`，us-east-1，字符串主键record_id。模式明确为dynamodb，实例角色访问；没有复制凭证给组员。旧S3数据未迁移。

| 请求标签 | 实例 | AZ | 私有地址 |
| --- | --- | --- | --- |
| az-a | i-00572a14ca8b71156 | us-east-1a | 10.37.10.88 |
| az-b | i-0081259c52a32e051 | us-east-1b | 10.37.11.110 |

两台在最后读取目标组时均healthy、无公网IP。HTTP80经ALB到应用8000；本次没有扩大IAM/安全组或新增资源。角色权限较宽的Lab限制仍需报告说明。

## A已经实际验证

1. 两台逐台发布，本机真实业务GET与健康检查通过；主机启动日志记录固定commit、源码/包哈希、iam-role来源、Python版本。见 [A主机](../evidence/T09/2026-11-07-A-first-host-release.log)、[B主机](../evidence/T09/2026-11-07-A-second-host-release.log)。最初A主机外部探针的字符串“Reading Tracker”也匹配占位页，不能单独作为B已发布证据；B的后续启动日志、stage及业务表单检查才是依据。
2. **12:25:06 UTC**，通过真实ALB POST一条虚构记录，返回302，写入实例az-b。az-a/az-b随后均返回200，均显示业务表单和该记录；数据库强一致查询得到唯一记录、字段值符合预期。见 [写入/读回日志](../evidence/T09/2026-11-07-A-cloud-write-read.log)。
3. 唯一标题 `Fictional cloud acceptance 95c34a0851c940db8b642eb3317d0a45`；record_id `effa5b9c-f7b6-4534-8cd3-c13ef4bb65dd`；reading、12/120页、rating4。此记录保留给B/C复核，不能用真人数据代替。
4. 完全停止写入主机az-b，控制面确认为stopped；ALB仍由az-a返回200并显示该记录。见 [停机期间](../evidence/T09/2026-11-07-A-during-writer-stop.log)。这是单实例停机检查，未实测整个AZ丢失。
5. 重新启动az-b，自动读取同一发布包、保留dynamodb配置，两目标再次healthy。**12:28:04–05 UTC**，az-b及az-a再次读到原记录，强一致查询确认record_id未变。见 [重启启动日志](../evidence/T09/2026-11-07-A-restart-boot.log)、[重启后读回](../evidence/T09/2026-11-07-A-post-restart-read.log)。不是新建同名记录冒充持久化。
6. [真实浏览器页面截图](../evidence/T09/2026-11-07-A-reading-tracker-live.png)显示共享存储说明、表单、1条记录、12页及4.0评分。截图拍于首次写入后；重启后结论以独立带时间的HTTP/数据库日志为据。

## B现在直接做什么

Alex4325Li：拉最新main，按T07交付核对部署证据与代码；浏览器实际查看并新增一条独特虚构记录，记录状态/响应/字段结果。若发现程序问题，交可复现输入与预期/实测，修复后给A新commit。可认领T11，独立核对共享数据与无状态证据，并与C完成复测；不要直接拿A日志声称自己已经做过实验。完善T04/T07完整交付和报告中的应用/数据库选择及代价。

## C现在直接做什么

Marina057：拉最新main，按 [你自己的T12方案](c-t12-business-validation.md) 先核对真实stage、两标签和上述记录；可不登录AWS，直接访问业务网址与低频HTTP采样。建议使用你已有的工具：

```sh
python scripts/c_request_log.py --url http://infs3701-team-alb-788523332.us-east-1.elb.amazonaws.com/ --count 30 --interval 2 --timeout 5 --stage business-release --output evidence/T12/YOUR-NEW-BUSINESS-SAMPLES.jsonl
```

将输出路径换为你实际日期/用户名的新文件，核对标签分布、状态码和业务页，不覆盖旧证据。真实新增/读回可以独立执行少量虚构数据；重启与AWS监控配置需A配合，不索要密码。已有监控dashboard和alarm仍在，但本轮尚未对齐最新指标图/业务负载或独立复测告警，不能复用11月1日基础告警当本次业务故障验收。

## 仍然没有完成的内容

HTTPS和域名方案待课程确认；公开演示无登录/CSRF防护，仅虚构数据。未执行真正整个AZ故障、业务告警全流程或云端回退演练。报告、架构图、12个月成本和视频仍需正式制作。现有应用全表强一致Scan只适用于小规模课程数据，成本/扩展限制要说明。

Lab会话结束可能停止实例，本页不承诺全天在线。访问失败先保留时间/HTTP错误，不重新写入或改权限；核对Lab是否开启，由A恢复会话。停止自动影响的是实验运行状态，数据保留已实测。不要将T09/T10 partial上报当作小组独立验收全部通过。
