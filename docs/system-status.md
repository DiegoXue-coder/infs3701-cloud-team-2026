# 当前系统状态

建立于 2026-10-31，Australia/Sydney。

## 已可使用

- 私有仓库、21 份原始资料及文本索引、24 张任务卡、角色和依赖计划。
- 固定命令的认领、进度、阻塞、JSON 交付与另一账号复核规则。
- `scripts/team.py`：由每个人自己的 AI 使用已有 GitHub 授权，在聊天时读取并刷新任务与看板。无需模型 API key 或新付费服务。
- `AGENTS.md`、`CLAUDE.md`、通用开场语和加入说明。

## 已发现的限制

1. **GitHub Actions 不能启动。** 首次运行回报：`The job was not started because recent account payments have failed or your spending limit needs to be increased.` [原始运行](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/actions/runs/41182740718)。未修改付款信息或限额；工作流保留但暂停，避免反复红灯。当前使用聊天驱动同步。
2. **没有 GitHub Projects scope。** 当前已有 Git 授权可管理仓库和 Issues，不能创建 Projects v2。因此看板是仓库内自动生成、带任务链接及时间表的 `DASHBOARD.md`，不是原生拖动式 Projects。
3. **Codex 的现有 GitHub 连接器尚未包含新仓库。** 接口读取返回 404，现有本机 Git 授权可以正常读写。使用本地克隆和同步助手不受该连接器范围影响；未来每位成员需给自己的工具配置访问，不会因为被邀请就自动连接所有 AI。
4. A/C 成员未提供，未发邀请；B 暂绑定 DiegoXue-coder。起始服务、最终 Lab 持有人和若干课程冲突待 T01/T03 确认。
5. Week 5 和 Week 7 的 8 个新文件已归档并共享；Week 8/9 正式课件仍待收到，不能宣称全学期资料已齐。

## 恢复后台模式时

由账号持有人自行处理 GitHub 账单/额度问题后，负责人可重新启用 `.github/workflows/team-sync.yml` 并手动运行验证；成功前仍使用聊天同步。GitHub Projects 和 AI 连接器授权若需要扩大，另由本人处理，不在初始化中擅自扩大权限。

## 完成的含义

协作系统可用不等于作业已完成。真实 AWS 配置、运行测试、报告、成本和视频仍要按任务卡逐项实施并复核。没有第二位成员时，不能演示或伪造独立复核成功。
