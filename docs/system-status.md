# 当前系统状态

> 2026-11-11 HTTPS 方案已定为两段 TLS。现有 ALB 使用公开可信证书，两台 EC2 使用仅对 ALB 开放的内网 TLS。配置顺序、验证和回退见[HTTPS 实施方案](https-rollout.md)。入口仍待确认可管理 DNS 的子域名或已有可用证书，方案尚未部署。

> 2026-11-11悉尼文档进展：负责人明确暂缓自动扩容，10Nov准备的surge文件没有执行授权，config保持enhancements_enabled=false。已生成[1页架构图PDF及复核入口](architecture-review-2026-11-11.md)、[网络/安全章节](network-security-chapter-2026-11-11.md)和[给老师的问题草稿](tutor-questions-ready-en.md)。图据10Nov证据绘制，非11Nov在线检查；HTTPS仍未解决，T15/T17仍待独立核对，老师消息未发送。

> 11/10后续只读预检：CloudFront ListDistributions被拒；ACM证书/Route53托管区/ASG均空，AutoScaling服务关联角色不存在（创建权限尚未验证）。已完成T15部分安全核对及本地扩容草案构建，未新增AWS资源。见[实际检查、HTTPS卡点与扩容边界](security-next-steps-2026-11-10.md)。现有两台不加入拟议扩容组；方案未部署，不计作增强完成。

> 2026-11-10实际更新：Lab原为Terminated，启动后两台业务目标healthy、HTTP200并读回原两条记录；当前仍仅HTTP80、ACM无证书、无ASG。已导出11/7业务停机时真实OK→ALARM→OK历史和C采样同期CloudWatch数据，待C独立核对。临时构建机已恢复stopped；Lab延迟预算显示$32.10/$50。报告由A先推进，见[收尾清单](closeout-plan-2026-11-10.md)。B的11/8错误原因未被追溯证明，不把本次恢复冒充当时根因结论。

> 2026-11-08协作更新：D分工已预留给Tenzin/wyend12，英文入口见[member-D.md](member-D.md)。GitHub访问、本人AI连接和任务认领仍须分别确认。B在11/8 15:35悉尼报告HTTP503且未写入，原因未知；不要把下方11/7成功记录称为当前在线健康。

> 最新实际进展（2026-11-07 12:28 UTC）：双私有机已发布 Reading Tracker 06c2292；真实数据库写入、两实例读回、停止写入实例期间另一台继续读取、重启后同一记录保留均通过。B/C独立云端复测与HTTPS尚待完成。优先读 [最新业务交接](business-handoff-2026-11-07.md)。以下按原日期保留历史，不以旧描述覆盖最新实测。


建立于 2026-10-31，Australia/Sydney。

## 已可使用

- 私有仓库、21 份原始资料及文本索引、24 张任务卡、角色和依赖计划。
- 固定命令的认领、进度、阻塞、JSON 交付与另一账号复核规则。
- `scripts/team.py`：由每个人自己的 AI 使用已有 GitHub 授权，在聊天时读取并刷新任务与看板。无需模型 API key 或新付费服务。
- `AGENTS.md`、`CLAUDE.md`、通用开场语和加入说明。

## 已发现的限制

1. **GitHub Actions 不能启动。** 首次运行回报：`The job was not started because recent account payments have failed or your spending limit needs to be increased.` [原始运行](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/actions/runs/41182740718)。未修改付款信息或限额；工作流保留但暂停，避免反复红灯。当前使用聊天驱动同步。
2. **没有 GitHub Projects scope。** 当前已有 Git 授权可管理仓库和 Issues，不能创建 Projects v2。因此看板是仓库内自动生成、带任务链接及时间表的 `DASHBOARD.md`，不是原生拖动式 Projects。
3. **持有人连接器404已于2026-11-04修复。** 经本人明确批准，仅将小组仓库加入现有 ChatGPT Codex Connector 选定范围，保留second-brain，仓库仍私有。连接器实际读取仓库、project/config.json和T08成功。其他成员自己的连接尚需重试验证，详见 [授权记录](2026-11-04-connector-access.md)。
4. Marina057 与 Alex4325Li 已接受仓库邀请并有写权限。Alex4325Li 已登记B并上传T04交付；Marina经Diego转述已选择C，但尚未在系统登记/认领。她反馈有17项本地测试及草稿，文件尚未上传，不能作为已验收结果。A为DiegoXue-coder；最新状态仍读取Issue/配置。
5. Week 5 和 Week 7 的 8 个新文件已归档并共享；Week 8/9 正式课件仍待收到，不能宣称全学期资料已齐。

6. 当前 Learner Lab Readme 明确禁止创建用户或组；不能为另两位成员创建独立 IAM 登录账号。已进入 us-east-1 控制台，只读检查，没有更改权限。另行提供的小组访问方式待 tutor 确认，见 `docs/aws-access-audit.md`。

## 恢复后台模式时

由账号持有人自行处理 GitHub 账单/额度问题后，负责人可重新启用 `.github/workflows/team-sync.yml` 并手动运行验证；成功前仍使用聊天同步。GitHub Projects 和 AI 连接器授权若需要扩大，另由本人处理，不在初始化中擅自扩大权限。

## 完成的含义

协作系统可用不等于作业已完成。真实 AWS 配置、运行测试、报告、成本和视频仍要按任务卡逐项实施并复核。没有第二位成员时，不能演示或伪造独立复核成功。

## 自助开工入口（2026-10-31）

已提供 docs/self-service.md、B/C 角色指南、project/handoffs.json、setup_member.py 及 team.py join。44 项测试通过，本机隔离依赖安装和离线基线检查通过；尚未有另两位真实账号验收。需先邀请并由本人接受 private 仓库访问，两人可各自选择空缺角色，不必预先分工；角色绑定不是新增 AWS 授权。

## 2026-11-01 实际开工

T05 已由 DiegoXue-coder 认领。今日 Lab 已启动并只读盘点旧 EC2/S3，尚无新的可用云服务。详见 docs/2026-11-01-aws-inventory.md；实际缺陷与未测项均保留，不能报为已修复。
