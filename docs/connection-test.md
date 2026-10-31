# 怎么测试 GitHub 是否连接成功

## 先测本人能不能打开

如果三个链接都返回 404，先按 [access-404.md](access-404.md) 在同一浏览器登录 DiegoXue-coder；Git 工具的登录状态不等于浏览器登录状态。

用本人 GitHub 账号登录，打开 [仓库首页](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026)、[资料索引](../sources/INDEX.md)、[在线任务入口](../LIVE_BOARD.md) 和 [T01](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues/1)。能打开说明网页读取正常；其他组员需先接受仓库邀请。

## 再测自己的 AI

把下面一段交给 AI：

> 请做只读连接测试，不认领、不完成任务、不改 AWS。读取本仓库 README、sources/INDEX.md、project/config.json，以及 GitHub 上 T01 的最新正文。告诉我你实际读到的仓库名、资料数量、我的角色和 T01 当前状态；如果没有访问权限，明确报告错误，不凭聊天历史回答。

能读文件不等于能写进度；网页能读也不等于 AI 连接器已获准访问。若网页能开而 AI 返回 404，先检查 AI 使用的账号和仓库授权范围，不需要把仓库改为公开。

## 有终端能力的 AI 可运行只读自检

在本仓库本地克隆目录里，以本人用户名运行：

```text
python scripts/team.py --user DiegoXue-coder doctor
```

其他成员换成本人 GitHub 用户名。自检只读取身份、角色、资料、任务卡和工作流状态；不创建同步锁、不发任务评论、不刷新看板、不认领任务。当前应看到：`source_files: 21`、`task_cards: 24`、本人用户及角色、各读取检查为 true。B/C 尚未加入时，不能假装绑定成功。

本机 Git/REST 方式与 Codex GitHub 连接器是两条不同连接。当前连接器读取新仓库仍返回 404；本机已有 Git 授权可以访问。自检输出不会声称同时测过连接器。

## 测“能不能同步”

首次只读测试通过后，可以让 AI 在 T01 发 `/team status`，通过同步助手处理，并检查 Issue 中新增的“任务同步回执”和看板时间。这个命令查询状态，不把课程任务标完成。

```text
python scripts/team.py --user DiegoXue-coder command T01 --body-file 临时命令.txt
```

临时命令.txt 内容为一行 `/team status`。不要把密码或 token 写进去。上传文件测试只用普通测试记录，不用课程真实成果冒充完成。

## 什么才是成功

1. AI 报告的信息确实来自本次远程读取。
2. 同步命令收到回执，而不是仅在本地聊天里说“更新了”。
3. 另一位有权限组员打开同一个任务，能看到同样的状态和评论。
4. 截图/配置/报告原件能从资料或交付链接打开。
