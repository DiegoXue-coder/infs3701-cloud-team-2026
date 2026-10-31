# INFS3701 三人云服务协作中心

**来这里看进度、领任务、交证据，再和你自己的 AI 一起做。** 云服务在 AWS 运行，本仓库负责把三个人的工作接起来。

→ [在线任务入口](LIVE_BOARD.md) · [进度看板](DASHBOARD.md) · [全部任务](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues) · [每天开始的开场语](prompts/START.md) · [首次加入](docs/onboarding.md)

## 每天只需对 AI 说

> 我是 GitHub 用户名 ___。请先读取这个仓库的 AGENTS.md，确认我的角色和 GitHub 最新任务，告诉我项目进度、我今天先做什么，再带我一步步完成。结束时整理真实交付并更新任务，等同步确认。

第一次需让 AI 工具获得你自己的 GitHub 访问权限，或打开本仓库的本地副本。仅给普通聊天一个 private 链接不会自动授予读取权限。之后可继续用简短的“开始今天的任务”。

## 协作怎样运转

1. AI 读取最新 Issue，按前置任务和本人角色推荐工作。
2. 在任务卡评论 `/team claim B`，等待系统确认认领。
3. 配置 AWS、编写代码或制作材料，保留真实证据。
4. 提交交付文件到默认分支，评论 `/team submit 文件路径`，进入“等检查”。
5. 另一位成员检查后评论 `/team approve 检查说明`，才进入“已完成”。
6. AI 运行仓库同步助手，刷新 [看板](DASHBOARD.md) 和 AI 可读的 [状态快照](data/snapshot.json)。

当前采用**聊天时同步**：每次开始时 AI 运行 `python scripts/team.py --user 本人用户名 start`；更新任务时运行同一助手的 command 功能。它读取本人已有的 GitHub 授权，不调用收费 AI API、不控制 AWS。读任务、计划和检查由每个人自己的 AI 协助。

GitHub Actions 的后台刷新配置已保留，但账号当前因付款/额度限制无法启动运行，已暂停以免反复失败；没有修改账单或提高限额。此时仅在网页发评论不会自动刷新，需要任一有写权限成员的 AI 运行同步助手。详情见 [当前系统状态](docs/system-status.md)。

## 三个角色

| 角色 | 主要负责 | 当前成员 |
| --- | --- | --- |
| A | 网络、服务器、统一入口、部署环境、架构图 | 待加入 |
| B | 应用、数据库、部署约定、报告整合 | DiegoXue-coder（暂定，可调整） |
| C | 监控、测试、证据、成本、视频整合 | 待加入 |

每个任务有主责、协作者、检查标准和前置任务。不是一个人做云端、另外两人只写报告。角色可调整，成员加入后更新配置；每人使用自己的 GitHub 身份。

## 分类方式

| 内容 | 在哪里 |
| --- | --- |
| 按周分好的原始课件与示例 | sources/original/course/02_weekly_materials/week_XX/ |
| 三份小组作业原件 | sources/original/assignment/ |
| AI 检索文本与文件校验 | sources/text/、sources/manifest.json |
| 实时任务卡和角色 | GitHub Issues；project/config.json 绑定 A/B/C |
| 真实交付、测试、截图和日志 | deliveries/ 与各任务所引用的证据文件 |
| AI 工作规则与操作手册 | AGENTS.md、CLAUDE.md、prompts/、docs/ |
| 在线访问和进度摘要 | LIVE_BOARD.md（筛选入口）、DASHBOARD.md（同步快照） |

[如何做连接测试](docs/connection-test.md) · [在线与自动刷新的区别](docs/online-board.md)

## 资料与记录

- [资料索引](sources/INDEX.md)：原始作业文件、现有相关课件、AI 可检索文本、缺失清单及校验值。
- [作业要求与冲突](docs/assignment-requirements.md)：不能遗漏的核心要求、交付和待确认问题。
- [三人操作手册](docs/execution-guide.md)：做什么、怎么做、先后顺序和联合检查节点。
- [任务定义](project/tasks.json)：计划和验收；实时状态在对应 Issue，不手改快照。
- [交付模板](templates/delivery.json)、[会议决定](docs/decisions.md)、[环境记录](docs/environment.md)。
- [协议](docs/team-protocol.md)：认领、进度、阻塞、提交、复核及恢复。

## 当前边界

起始服务尚待 T01 小组决定，Reading Tracker 仅是可复用候选。建立协作系统不等于已完成课程作业。截止为 **2026-11-17 16:00（悉尼）**，内部节点是建议；Moodle 更新和 tutor 对冲突的答复应记录后再调整。

仓库必须保持私有；不部署公开 Pages，不上传账号密码、AWS 密钥、私人数据或带签名/学号的个人文件。只邀请有权使用课程材料的实际组员。
