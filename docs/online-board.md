# 在线、最新与自动刷新，分别是什么意思

## 现在可以随时在线访问

仓库和 Issues 本身由 GitHub 在线提供，组员登录并有仓库权限即可随时查看，不需要你的电脑开机。[在线任务入口](../LIVE_BOARD.md) 按 A/B/C 和状态链接到 GitHub 当前的任务列表；每次打开或刷新列表会查询已同步的状态，搜索索引可能有短暂延迟。

`DASHBOARD.md` 是整理好的进度快照，显示最后同步时间。它也是在线文件，但不会自己每秒重算。浏览器已打开的页面也不保证自动推送变化。

## 现在如何更新

成员和自己的 AI 完成操作 → 上传真实交付或记录 → 运行同步助手 → Issue 元数据、标签和看板一起更新。其他成员刷新任务页即可看到更新。

在 AWS 控制台做了操作、但没有上报项目时，GitHub 不会自动知道；即使换成实时网页也不能凭空知道。只发 `/team ...` 评论而没有处理回执时，命令仍是待处理请求。

## 三个人分别看什么

- A：网络、服务器、统一入口、部署、架构图。
- B：应用、数据库、部署约定、报告；由成员二负责，用户名待登记。
- C：监控、测试、证据、成本、视频。

在线入口的 A/B/C 表示计划角色，实际认领人记录在 Issue assignee；成员加入后在 config 中绑定，不能把未认领任务当作某人已在做。

## 若希望更自动

1. **原生 GitHub Projects：** 可以用表格、按状态分列的看板、时间轴，关联 Issue；它适合拖动和按角色查看。现有授权没有 Projects scope，本次没有擅自扩大授权或创建。启用它仍需保持任务命令/交付规则一致，拖动一个格子不能替代真实复核。
2. **恢复托管同步：** GitHub Actions 账号的付款/额度限制解除后，重新启用并验证现有工作流，可以在提交命令后后台处理。当前没有修改账单，不能宣称已恢复。
3. **独立实时网页：** 需要另设登录、私有数据访问和持续运行的服务；不能把课程资料或访问 token 直接放入公开页面。这会增加维护，当前三人作业先使用已有 GitHub 在线任务入口即可。

不要在没有实际测试的情况下承诺“秒级更新”或“AI 自动看到 AWS 实时配置”。

官方说明：[GitHub 任务筛选](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/filtering-and-searching-issues-and-pull-requests)、[GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)。
