# C报告章节与视频草稿

2026-11-04。供小组整合，未替任何成员签字，未代表真人复核。最终报告正文严格少于4000词且少于8页；原始brief和rubric的冲突由T03向tutor确认。

## 整组报告框架及分工

1. Objective and route（B整合）：Reading Tracker / Option A，原作者DiegoXue-coder，明确升级目标。
2. Architecture and services（A）：双AZ网络、ALB、私有EC2、DynamoDB，引用与实际一致的架构图。
3. Scalability and availability（A/B/C）：无状态与共享数据设计，C提供分流/故障的真实样本及限制。
4. Networking, security and data（A/B）：入口和角色、数据模型、加密与尚未解决的HTTPS限制。
5. Monitoring and validation（C）：指标、阈值理由、实验方法、输入/期望/实测、失败及修复。
6. Cost and trade-offs（C）：12个月Calculator输入及最终估算，实验预算和资源取舍。
7. Enhancements if attempted（对应操作者）：仅描述已实现且有证据的增强；基础monitoring为core。
8. Contributions, AI use and references（每人）：个人独立确认，统一引用格式。

## 可直接整合的本轮英文段落

**Validation method and current scope.** Member C prepared four synthetic datasets and independent tests of the original Reading Tracker statistics function. Ten tests passed on Windows with Python 3.12.14. The tests execute the original function in isolation, covering aggregate semantics, missing ratings, boundary values, legacy numeric strings, order invariance and input preservation. They do not import the web application or access AWS. Seven additional tests passed against a real loopback HTTP fixture, validating bounded request sampling, status and instance-header capture, timeout handling and protection against overwriting evidence. Four persisted HTTP samples returned 200 from the explicitly labelled local fixture. These results validate the statistics baseline and the sampling tool; they do not establish that the final application or managed database is deployed.

**Monitoring rationale.** The repository baseline alarms when the minimum healthy-target count falls below two over two consecutive 60-second periods. This is a redundancy signal: one surviving target may still serve requests. C's offline review found that the documented threshold and dimensions match the deployment source. Live configuration readback remains pending. The missing-data setting and lack of configured notification recipients are explicit limitations. Final acceptance will correlate request samples with target health, real alarm history and the operator's failure and recovery timestamps.

**Availability evidence to collect.** The planned joint experiment will first establish two healthy instances, sample steady traffic, stop one instance under A's control, record observed failures, and restore the original instance. Both instance identity and shared-data persistence will be checked. The report will distinguish client sampling resolution, load-balancer health-check behavior and alarm evaluation delay. A single-instance experiment will not be presented as proof of a complete Availability Zone outage.

上述段落只描述本轮事实/计划，最终应更新为实际发布版本及联合实验结果。A既有云端证据须注明其日期与操作者，不能算作C本轮实测。

## 60秒视频镜头脚本（尚未录制）

| 时间 | 画面与真实动作 | 解说要点 |
| --- | --- | --- |
| 0–8s | 实际业务URL打开Reading Tracker；展示已部署版本 | Reading Tracker，升级单机服务为双AZ共享数据架构 |
| 8–22s | 新增虚构记录，返回列表并展示统计 | 后端实际处理记录，DynamoDB保存共享状态 |
| 22–35s | 显示同一窗口真实请求日志，至少两个实例标签 | ALB分流，两台实例使用同一应用版本 |
| 35–49s | 对齐A的实际单机停机时间、连续请求及真实告警状态 | 服务在测试范围内继续响应；如有失败如实显示 |
| 49–60s | 恢复健康/数据仍在，短暂展示架构图 | 私有应用层、共享数据层、监控与取舍 |

只录运行中的业务服务；不能用基础测试页、模拟实例标签或仅控制台截图代替。正式视频需真实录屏和本人解说，本次未生成视频、配音或云端截图。

## 贡献与AI记录草稿

Marina057（C）：在本人授权下由Codex协助阅读仓库、生成四组虚构数据、编写统计测试和HTTP取样工具、运行本地测试、整理监控/成本/报告与视频草稿。实际命令由本机AI工具执行；用户尚未逐项人工验证，另一账号尚未复核。AWS资源由A既有工作创建，本次C未操作AWS。2026-11-04以本人GitHub身份完成join C和T08 claim，认领回执R-T08-6624693113。测试原日志仍保留登记前时间；本交付仅提交T08准备工作，工作比例和独立复核须真人确认。
