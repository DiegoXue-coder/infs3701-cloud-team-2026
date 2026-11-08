# 第一次加入：做一次，以后直接和 AI 聊

**当前四人入口：** [self-service](self-service.md)、[D English setup](member-D.md)、[English prompt](../prompts/START-en.md)。A/B/C/D已在config预留，Tenzin不使用下方历史B/C空缺选岗流程。角色不等于访问或本人连接已验证。

完整的自助设置、角色选择和可复制 AI 开场语见 [自助入口](self-service.md)。尚未分工时，两位可先加入后各自选 B/C。

## 项目负责人

1. 保持仓库 Private，不启用公开 Pages。确认要加入的是有权访问课程资料的真实组员。
2. 获得组员 GitHub 用户名后，通过仓库 Settings → Collaborators 发邀请，组员自己接受。不要共享账号。
3. 无需手动绑定 B/C。组员接受邀请后运行 doctor 查看空缺，自己选择并由 AI 运行 join --role B 或 C；同一角色不能被覆盖，每人只能占一岗。
4. 若改变起始服务或数据库，将理由记入 `docs/decisions.md` 并更新配置；不要让各人的 AI 自行选不同方案。

## 每位组员

1. 用自己的 GitHub 账号接受仓库邀请，确认能打开 README 和 Issues。
2. 推荐让有终端能力的 AI 打开本仓库的本地克隆，确认 Python 3.9+ 可运行，并使用本人已有的 Git/gh 授权。同步助手会依次使用当前进程 GH_TOKEN、本人 gh 登录或 Git 凭证，不保存秘密。无需向本仓库提交任何 AI API key。若使用连接器，需本人确保其能访问这个新 private 仓库；目前 Codex 中既有连接未包含新仓库。
3. 把 `prompts/START.md` 的首次开场语给 AI，填写自己的 GitHub 用户名。AI 应报告从配置读到的角色。若 Windows Python 提示缺少时区数据，让 AI 在该环境安装 `tzdata` 后重试，不能把悉尼时间猜成电脑本地时间。
4. 先按 self-service 完成本地 setup、doctor 和 join；再让 AI 运行 `python scripts/team.py --user 本人用户名 start`，用 command 功能认领；看到系统回执再开始。若无法访问，先解决连接权限，不让别人代签。
5. 有 AWS 访问权限才实际操作；否则与最终环境持有人约共享屏幕，提交步骤并共同验证。

## 只有聊天、没有 GitHub 工具时

AI 可以解释任务，但不能自动同步。由本人把命令复制到任务评论、上传交付，再请有终端能力且已获仓库写权限的成员运行同步；命令仍以原评论人的身份校验，不能代签。GitHub Actions 恢复前，不承诺网页评论后马上自动执行。不要声称普通聊天能仅凭一个 private 链接自动管理仓库。

## 当前尚未完成的加入事项

B/C 用户名待提供；尚未邀请任何新成员。起始服务已确定为 Reading Tracker，Lab 持有人已指定为 DiegoXue-coder。课件缺失项见资料索引。

## 不改进度的连接自检

让 AI 在本地克隆运行 `python scripts/team.py --user 本人用户名 doctor`。它只读身份、资料和任务，不认领或完成任务。完整方法见 [connection-test.md](connection-test.md)，在线角色入口见 [LIVE_BOARD.md](../LIVE_BOARD.md)。
