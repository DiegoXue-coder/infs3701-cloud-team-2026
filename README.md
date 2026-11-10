# INFS3701 四人云服务协作中心 / Four-person team hub

**11/10安全准备：** [已验证控制、HTTPS实际限制和2→3台扩容草案](docs/security-next-steps-2026-11-10.md)。仅准备，未新增云资源，T15尚未完成；B/C可并行复核，不必等D。

**11/10收尾入口：** [还差什么与完成顺序](docs/closeout-plan-2026-11-10.md) · [英文报告工作稿](docs/design-report-working.md) · [要求/证据矩阵](docs/requirements-evidence-matrix-2026-11-10.md) · [已找回的业务告警与同期指标](docs/monitoring-reconciliation-2026-11-10.md)。A已临时推进T25/T19，不等待D回复；这不是D的贡献或最终验收通过。

**来这里看进度、领任务、交证据，再和你自己的 AI 一起做。** 云服务在 AWS 运行，本仓库负责把四个人的工作接起来。

**Tenzin / wyend12: [English setup and your work](docs/member-D.md) · [Copy this English prompt](prompts/START-en.md) · [Four-person responsibilities](docs/four-person-plan.md).** Accept your invitation and authenticate your own GitHub/AI first. Your role assignment is not a task claim or a verified connection.

**最新业务交接（2026-11-07）：** [双实例程序已部署，B/C从这里开始云端独立复核](docs/business-handoff-2026-11-07.md)。包含真实网址、06c2292版本、两台标签、读写/重启证据与各自下一步；HTTPS和小组最终验收尚未完成。

→ **[新成员自助开工 / Self-service entry](docs/self-service.md)**

→ [在线任务入口](LIVE_BOARD.md) · [进度看板](DASHBOARD.md) · [全部任务](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues) · [每天开始的开场语](prompts/START.md) · [首次加入](docs/onboarding.md)

## 每天只需对 AI 说

> 我是 GitHub 用户名 ___。请先读取这个仓库的 AGENTS.md，确认我的角色和 GitHub 最新任务，告诉我项目进度、我今天先做什么，再带我一步步完成。结束时整理真实交付并更新任务，等同步确认。

第一次需让 AI 工具获得你自己的 GitHub 访问权限，或打开本仓库的本地副本。仅给普通聊天一个 private 链接不会自动授予读取权限。之后可继续用简短的“开始今天的任务”。

## 协作怎样运转

1. AI 读取最新 Issue，按前置任务和本人角色推荐工作。
2. 在任务卡评论 `/team claim B`，等待系统确认认领。
3. 配置 AWS、编写代码或制作材料，保留真实证据。
4. 提交带执行记录的交付到默认分支；部分成果用 `/team report 文件路径`，完整交付用 `/team submit 文件路径` 进入“等检查”。两者都有编号回执。
5. 另一位成员检查后评论 `/team approve 检查说明`，才进入“已完成”。
6. AI 运行仓库同步助手，刷新 [看板](DASHBOARD.md) 和 AI 可读的 [状态快照](data/snapshot.json)。

当前采用**聊天时同步**：每次开始时 AI 运行 `python scripts/team.py --user 本人用户名 start`；更新任务时运行同一助手的 command 功能。它读取本人已有的 GitHub 授权，不调用收费 AI API、不控制 AWS。读任务、计划和检查由每个人自己的 AI 协助。

GitHub Actions 的后台刷新配置已保留，但账号当前因付款/额度限制无法启动运行，已暂停以免反复失败；没有修改账单或提高限额。此时仅在网页发评论不会自动刷新，需要任一有写权限成员的 AI 运行同步助手。详情见 [当前系统状态](docs/system-status.md)。

## 并行方式

[四人当前分工](docs/four-person-plan.md)：A操作AWS/架构，B应用/数据，C测试/监控/成本，D英文报告/证据核对/视频统筹。准备可并行，最终验收保留必要条件；[原三人计划](docs/parallel-plan.md)保留为历史。

## 四个角色

| 角色 | 主要负责 | 当前成员 |
| --- | --- | --- |
| A | 网络、服务器、统一入口、部署环境、架构图 | DiegoXue-coder（你） |
| B | 应用、数据代码、独立验证、应用/数据库章节 | Alex4325Li |
| C | 监控、测试、故障取证、成本、贡献记录汇总 | Marina057 |
| D | 英文目标/证据核对、总报告整合、视频统筹 | Tenzin / wyend12（访问与本人开工待验证） |

每个任务有主责、协作者、检查标准和前置任务。A负责AWS实际配置，B/C提供技术内容和实验证据，D整合英文报告与呈现；每人保留原作者归属、各自技术章节和真实贡献，使用本人GitHub身份。

## 分类方式

| 内容 | 在哪里 |
| --- | --- |
| 按周分好的原始课件与示例 | sources/original/course/02_weekly_materials/week_XX/ |
| 三份小组作业原件 | sources/original/assignment/ |
| AI 检索文本与文件校验 | sources/text/、sources/manifest.json |
| 实时任务卡和角色 | GitHub Issues；project/config.json 绑定 A/B/C/D |
| 真实交付、测试、截图和日志 | deliveries/ 与各任务所引用的证据文件 |
| AI 工作规则与操作手册 | AGENTS.md、CLAUDE.md、prompts/、docs/ |
| 在线访问和进度摘要 | LIVE_BOARD.md（筛选入口）、DASHBOARD.md（同步快照） |

[如何做连接测试](docs/connection-test.md) · [在线与自动刷新的区别](docs/online-board.md)

## 资料与记录

- [报告取材入口](docs/report-evidence-index.md)：按章节查找实际截图、日志、配置与回执，以及图片下载/嵌入报告的方法。
- [资料索引](sources/INDEX.md)：原始作业文件、现有相关课件、AI 可检索文本、缺失清单及校验值。
- [作业要求与冲突](docs/assignment-requirements.md)：不能遗漏的核心要求、交付和待确认问题。
- [三人操作手册](docs/execution-guide.md)：做什么、怎么做、先后顺序和联合检查节点。
- [任务定义](project/tasks.json)：计划和验收；实时状态在对应 Issue，不手改快照。
- [交付模板](templates/delivery.json)、[会议决定](docs/decisions.md)、[环境记录](docs/environment.md)。
- [工作结束怎样上报](docs/reporting.md)：实际截图/日志、测试结果、回执、复核；看板显示最近记录，完整回执在 data/receipts.json。
- [协议](docs/team-protocol.md)：认领、进度、阻塞、提交、复核及恢复。

## 当前边界

用户已确认升级自己的 Reading Tracker（Option A）。[代码入口](app/reading_tracker.py)与[运行说明](app/README.md)可用；现已发布双私有机与共享DynamoDB，并由A验证真实读写、跨实例读回和重启保留；B/C独立云端复核、HTTPS及报告等最终交付仍需完成。截止为 **2026-11-17 16:00（悉尼）**，内部节点是建议；Moodle 更新和 tutor 对冲突的答复应记录后再调整。

仓库必须保持私有；不部署公开 Pages，不上传账号密码、AWS 密钥、私人数据或带签名/学号的个人文件。只邀请有权使用课程材料的实际组员。

## 当前应用与 AWS 协作

已选择 [Reading Tracker 代码](app/reading_tracker.py)，按 [三人共同管理 AWS](docs/shared-aws.md) 统一集成。保留应用功能，升级网络/计算/数据库与监控；不因重建环境就丢掉现有应用。
