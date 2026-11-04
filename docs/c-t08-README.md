# C / T08 测试准备交付

Marina057（C），Codex协助，2026-11-04。已通过本人Git登录执行doctor、join C、认领T08；认领回执[R-T08-6624693113](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues/8#issuecomment-6624699434)。初轮本地工作发生在角色登记前，保留原测试时间。

## 内容与结果

- [测试计划与复现](c-t08-test-plan.md)：四组虚构数据、10项统计测试和7项HTTP工具测试全部通过；逐项core验收计划。
- [监控方案](c-t08-monitoring.md)：已有告警的11字段离线核对、给A的故障/恢复操作计划。
- [成本假设](c-t08-cost-assumptions.md)：us-east-1全年服务输入；T18再用Calculator生成价格和PDF。
- [报告与视频草稿](c-t08-report-and-video.md)：可整合英文段落、60秒镜头安排和AI记录。
- [结构化交付](../deliveries/T08/2026-11-04-Marina057.json)：原始测试、证据及限制。

本交付只声明T08准备要求通过，需另一账号独立检查；不是C所有工作完成。没有执行AWS部署、数据库写入、停机、真实分流或业务HTTP验收。四条持久HTTP样本来自明确标为local-fixture-only的本地服务。

## 复核步骤

在仓库根目录运行 `python tests/c_t08/test_statistics.py`、`python tests/c_t08/test_request_log.py`、`python scripts/c_t08_review.py`。本次Windows/Python3.12.14，无需Flask/boto3或AWS身份；云端Python3.11另行复测。逐一核对文档覆盖所有core、预期结果和证据，检查原始run.log及JSONL。已有样本不覆盖。

T08提交后应进入等检查，由A或B实际核对后批准或要求修改，本人不能自批。回执以[任务卡](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues/8)为准。

## 资料缺口与后续

资料索引仍缺W8数据库、W9监控正式讲义/教程及最新Moodle/tutor回复。视频60秒/2分钟、自动扩容是否core、资源保留方式与Lab多人权限的冲突仍按T03确认，不能由草稿擅自消除。

B/A发布确切业务版本后，C继续T12分流、T13告警、T14故障取证，T18成本定稿，T20真实视频与T21个人签认。A负责AWS实际停/启与恢复，C负责取样和独立解释。任何草稿都不能冒充云端验收。
