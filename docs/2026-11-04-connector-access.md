# 2026-11-04 连接器授权与 Marina 恢复提交

Diego本人在聊天中明确批准：仅新增 DiegoXue-coder/infs3701-cloud-team-2026 至现有 ChatGPT Codex Connector，仓库保持私有，保留 second-brain 的原授权。

实际保存后，GitHub显示“Okay, ChatGPT Codex Connector was updated”。选项仍为 Only select repositories，共上述两个仓库。此安装本身已有对代码、Issues、PR、Actions与工作流的读写权限；本次将这些现有权限应用到小组仓库，没有选择 All repositories。

## 已实际验证

- 通过GitHub连接器、使用DiegoXue-coder连接读取小组仓库元数据成功，visibility=private。
- 同一路径读取 project/config.json 成功，文件SHA为2369430a6095f2c17d793baab476dc69e3829676；当时A=DiegoXue-coder，B=Alex4325Li，C=null。
- 同一路径读取真实T08（Issue8）成功，状态todo、owner=null。
- 保存截图：[GitHub成功提示和选定范围](../evidence/T02/2026-11-04-connector-access-saved.png)。

这证明持有人安装范围已补齐、当前持有人连接器的404已解决；没有登录或验证Marina的AI连接，也没有模拟她上传或认领。

## Marina 的AI接下来执行

1. 保留已有测试数据、脚本、17项测试原日志和草稿；不要用新克隆覆盖原工作。先检查当前文件夹的Git状态。
2. 用Marina057本人GitHub连接重试读取README、AGENTS、project/config.json和Issue8。仍失败时核对本人所连账号；可以用自己已有Git登录读取/克隆仓库，不必等待插件。
3. 按 docs/self-service.md 完成只读doctor；C空缺时由本人运行 `python scripts/team.py --user Marina057 join --role C`，重新读取确认登记。这里不能由Diego冒用Marina身份运行。
4. 通过同一助手的command子命令向T08发 `/team claim C`，取得回执再上传整理后的交付。当前已做工作如实记录为登记前本地准备，不改造测试日期。
5. 将真实脚本、数据、运行记录和草稿放入相应目录，用 templates/delivery.json 记录环境、期望、实际、限制与证据路径。17项是Marina反馈，需原始日志/实际复核支持；不要替换仓库原有测试或把本地通过写成AWS通过。
6. 通过正常Git流程合入main后，以本人身份 `/team report deliveries/T08/实际文件名.json`；仅完整满足T08要求时submit，等待另一成员独立检查。保留尚未完成的云端验证与草稿状态。

身份检查、虚拟环境路径与完整命令用仓库现有自助入口；不分享账号密码、token或AWS凭证。此次权限修复不等于T08已完成，也不恢复暂停的GitHub Actions。
