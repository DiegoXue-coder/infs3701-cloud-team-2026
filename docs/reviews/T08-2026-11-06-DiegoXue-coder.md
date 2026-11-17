# T08 review: preparation stage passed

Date: 2026-11-06 (Australia/Sydney). Reviewing account: DiegoXue-coder (A); submitting account: Marina057 (C). The user explicitly authorised the assistant in this chat to carry out the review and record the conclusion. Commands, code checks and document checks were run by Codex in A's workspace; it is not claimed that Diego ran them by hand, that Marina self-approved or that another real person separately signed off.

## Conclusion and versions

**T08 "test checklist, report outline, cost assumptions" passes preparation-stage acceptance, with no defects blocking approval.** This is not acceptance of the final business, AWS deployment, HTTPS, cost quote or video.

审核的提交回执：R-T08-6624791560；提交版本：`cb07163da0e2beb69797902b433efd8999fd4849`；交付文件：`deliveries/T08/2026-11-04-Marina057.json`。已将当前交付及15个证据文件的Git blob与提交回执逐一比较，16项全部匹配，也检查了工作区过滤后的blob；未修改Marina的提交、原日志或样本。

复跑环境：Windows 11，Python3.12.14，仓库隔离虚拟环境。原始执行时间与完整环境见下列日志；没有AWS操作，仅HTTP工具测试使用127.0.0.1临时服务。

## 实际检查

| 项目 | 复核动作与结果 | 证据 |
| --- | --- | --- |
| 统计与样本 | 独立核算四组虚构样本的记录数、状态数、页数与评分预期；复跑10项统计测试全部通过，包括旧格式、异常、顺序、输入不变性 | [统计复跑日志](../../evidence/T08/2026-11-06-A-review-statistics.log) |
| HTTP记录工具 | 阅读脚本和测试，复跑7项loopback测试全部通过；覆盖BASE_URL、成功、503、超时、缺少实例头、参数边界、防覆盖 | [HTTP工具复跑日志](../../evidence/T08/2026-11-06-A-review-http-tool.log) |
| 监控基线 | 只解析AST和配置，不执行部署代码；11个期望字段及ALB/TG维度匹配 | [告警源码核对日志](../../evidence/T08/2026-11-06-A-review-alarm-source.log) |
| 版本与历史证据 | 16个已提交blob全部匹配；原4条JSONL确为local-fixture-only、HTTP200、序号1–4；保留原文件 | [完整性结果](../../evidence/T08/2026-11-06-A-review-integrity.json)、[执行日志](../../evidence/T08/2026-11-06-A-review-integrity.log) |
| core测试计划 | 已覆盖真实界面/输入验证、数据库共享状态、分流、单机故障、AZ设计边界、监控、网络权限、加密和扩容；列出操作、预期、证据及角色 | [测试计划](../c-t08-test-plan.md) |
| 监控与故障准备 | 指标维度、统计周期、阈值理由、缺失点限制、无通知收件人、停机前/中/后样本和恢复步骤均明确；禁止人工伪造告警状态 | [监控计划](../c-t08-monitoring.md) |
| 成本准备 | us-east-1、12个月、8760小时场景，包含EC2/EBS/ALB/数据库/S3/快照/监控/传输/公网IPv4/网络端点；把工作量假设、价格待填和历史Lab余额区分清楚 | [成本假设](../c-t08-cost-assumptions.md) |
| 报告与视频准备 | 八部分报告框架覆盖brief要求；视频60秒镜头安排要求真实业务操作、分流/可用性和决策解释；草稿、真实贡献及AI使用边界已标注 | [报告与视频草稿](../c-t08-report-and-video.md) |

本轮核对了原始brief/rubric提取文本及T08任务卡。T08要求的是可执行准备、逐项验收安排、报告框架和估算假设，不要求在尚无业务发布时完成T12/T13/T14/T18/T20全部结果。

## 哈希差异的处理

复跑时原源码raw SHA-256为`f50fea5190314216ffcffb4c175d0a0dcf9dd5c57c2c69449e4ef73cb0856947`，Marina日志为`f1f20663612aa3343f5bce9f9acc749da2c8def46eea8e369fdcdc7bfd7e5d10`。核实本机工作区是CRLF，Git索引与Marina副本为LF；规范为LF后SHA完全相同，整文件AST也与原快照一致。因此这是换行差异，不是不同业务代码，不要求重写历史日志。

## 后续提醒（不阻止T08准备验收）

- Python3.11目标环境、新业务HTTP、DynamoDB真实写入、共享数据和云端故障测试仍待T07/T09之后执行；现在17项通过不能用于声称这些已完成。
- 当前统计测试隔离旧函数，后续要跟随B的实际版本更新调用/测试，不把旧函数接受负值等行为当成合格输入校验。
- 请求工具只记录响应头阶段的耗时，人工stage标签不自动证明部署；最终故障实验必须覆盖停机前后、保存实际时间和失败样本。
- 实时监控读回、通知和缺失数据策略、HTTPS、Calculator价格/PDF、正式报告/视频，以及课程冲突回复仍在后续任务处理。

本复核只将T08准备任务按上述范围批准；其他任务状态、其他成员贡献和个人签名由各自实际工作决定。GitHub评论与同步回执是状态生效依据。
