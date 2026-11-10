# 报告取材入口：要求、图片、日志与回执

**11/10增补：** [收尾清单](closeout-plan-2026-11-10.md)、[英文总报告工作稿](design-report-working.md)、[要求/证据矩阵](requirements-evidence-matrix-2026-11-10.md)、[真实业务告警与C同期监控核对](monitoring-reconciliation-2026-11-10.md)。最新网络/业务读回及看板截图由矩阵链接，旧证据按原日期保留。不是所有最终交付已完成。

更新：2026-11-01。本轮证据基线 commit：`b6c091c`。本页是取材索引，不是已完成的报告或最终验收。

**2026-11-07业务证据增补**：优先读取 [业务发布与B/C交接](business-handoff-2026-11-07.md)、[真实页面截图](../evidence/T09/2026-11-07-A-reading-tracker-live.png)、[真实写入和跨实例读回](../evidence/T09/2026-11-07-A-cloud-write-read.log)、[停止写入实例期间服务继续](../evidence/T09/2026-11-07-A-during-writer-stop.log)、[重启后同一record_id保留](../evidence/T09/2026-11-07-A-post-restart-read.log)、[发布/回退步骤](business-rollout-2026-11-07.md)。这些是A的真实云端操作证据；C尚未独立验收、HTTPS尚未完成。下表11月1日的“业务尚未验证”保留为历史，不代表11月7日的当前进度。

## 确实需要写报告

原始 [作业 brief](../sources/original/assignment/INFS3701_Group_Assignment.pdf)、[评分表](../sources/original/assignment/INFS3701_Group_Assignment_Marking_Scheme.pdf) 和 [要求摘要](assignment-requirements.md) 是依据。当前要求包含五项交付：部署系统、设计报告、架构图、12个月成本估算、视频。

设计报告正文须严格少于4,000词且少于8页，参考文献与附录除外；图片放正文也会占正文页数。图与成本文件分别按 brief 的 under 2 pages 控制，当前保守各做1页。视频时长 brief/rubric 冲突待 tutor 确认，先按60秒准备。还需个人贡献声明、真实签认、代码及AI/过程记录；签名等个人资料不因此自动获准上传仓库。

报告要解释服务解决谁的问题、为什么选这些服务、请求怎么流动、为何这样配置、真实测试结果和代价/限制；不能只把操作截图排成报告。最终提交前核对 Moodle 最新要求与 tutor 答复。

## 按报告内容找证据

下列链接均为仓库内真实文件，可由已获私有仓库权限的成员查看/下载。详细配置和限制见 [本轮验证与交接](2026-11-01-foundation-verification.md)。

| 写哪部分 | 可直接取的材料 | 能支持的结论与边界 |
| --- | --- | --- |
| 云服务目标、旧项目如何升级 | [旧代码](../app/reading_tracker.py)、[原始快照](../reference/reading_tracker_candidate.py)、[项目选择](../project/config.json) | 采用 Diego 的 Reading Tracker 为起点；仍需补具体用户需求和升级理由 |
| 网络、两个AZ、访问流程 | [实际资源清单](../project/aws-resources.json)、[最终配置读回日志](../evidence/T09/2026-11-01-final-readback.log)、[VPC详情截图](../evidence/T06/2026-11-01-vpc-details.png) | 真实子网、路由、端点和安全组；网络图须包含EBS、数据库与真实HTTP协议，最终图仍待制作 |
| 服务器、加密磁盘与启动方式 | [私有主机角色检查截图](../evidence/T09/2026-11-01-private-role-check.png)、[维护验证日志](../evidence/T09/2026-11-01-maintenance-validation.log)、[运行环境构建脚本](../deployment/runtime-builder.sh)、[依赖版本](../deployment/runtime-requirements.lock) | 两台角色访问、磁盘加密、重启后基础服务正常；不是业务应用发布证据 |
| 数据库选择与访问方式 | [选择理由与代价](aws-owner-handoff.md)、[建表脚本](../deployment/create-database.py)、[维护验证日志](../evidence/T09/2026-11-01-maintenance-validation.log) | DynamoDB ACTIVE、两私有机Describe/Scan通过；尚无业务写入、迁移或共享业务数据验证 |
| 负载均衡 | [逐条请求日志](../evidence/T09/2026-11-01-live-routing.log)、[基础页面截图](../evidence/T09/2026-11-01-foundation-live-page.png) | 初次12条HTTP200，两实例各6条；页面明确是占位基础页，不能用它证明Reading Tracker功能完成 |
| 监控看板 | [恢复后的图表截图](../evidence/T09/2026-11-01-cloudwatch-dashboard-final.png)、[监控配置脚本](../deployment/configure-monitoring-baseline.py) | 实际监控组件与健康数变化；截图是当时记录，不是GitHub内实时AWS看板；监控是本次core要求 |
| 单机停止、告警、恢复 | [真实告警截图](../evidence/T09/2026-11-01-real-alarm-trigger.png)、[维护日志](../evidence/T09/2026-11-01-maintenance-validation.log)、[告警状态历史](../evidence/T09/2026-11-01-final-readback.log) | 真实OK→ALARM→OK；期间取样另一台响应正常。不是整个AZ故障实测、零停机保证或SNS通知证明 |
| 安全与Lab限制 | [实际访问审计](aws-access-audit.md)、[最终规则日志](../evidence/T09/2026-11-01-final-readback.log)、[运维限制说明](2026-11-01-foundation-verification.md) | LabRole较宽、OpenTunnel拒绝、已关闭未用SSH路径；HTTPS与完整最小权限仍有缺口，须如实写 |
| 可复现操作、失败与修正 | [部署脚本目录](../deployment/)、[本轮操作汇总](2026-11-01-foundation-verification.md)、[离线测试日志](../evidence/T09/2026-11-01-foundation-maintenance-offline-tests.log) | 提供区域、依赖、资源、配置和步骤；48项离线通过不能替代云端业务测试；短样本汇总计数错误已在汇总里明确解释 |
| 真实贡献、AI使用与版本 | [T05交付](../deliveries/T05/2026-11-01-DiegoXue-coder-foundation-verified.json)、[T06交付](../deliveries/T06/2026-11-01-DiegoXue-coder-foundation-verified.json)、[T09交付](../deliveries/T09/2026-11-01-DiegoXue-coder-foundation-verified.json)、[回执数据](../data/receipts.json) | 本轮属于A的实际操作与AI协助；均为partial，不可写成B/C贡献或独立复核已通过 |
| 成本 | [环境与预算观察](../project/aws-resources.json) | $1.30/$50是延迟预算读数，不是本轮消耗或12个月估算；Pricing Calculator文件、运行时长和假设仍需补 |

## 图片怎样取出来用于报告

1. 人工：在 GitHub 点上表的图片链接，查看原图并下载PNG；从相邻日志取测试时间、参数和结果。报告插图优先使用原始PNG，避免截取GitHub网页造成文字模糊。
2. 有工具的AI：用成员本人的GitHub授权读取仓库，或拉取本地克隆，按本页路径读取PNG、日志、JSON及源码，再把图片真正嵌入Word/PDF。不要只给Word写一个需要登录的私有图片URL。
3. 普通聊天不能读取私有仓库时，由本人把所需文件下载给它；仓库邀请本身不会自动连接每个AI。不要把仓库改为公开，也不用分享AWS凭证。
4. 每张使用的图记录：图号、说明、测试日期/环境、文件路径、证据commit和对应日志。定稿时用指定commit的GitHub链接，避免以后main更新造成引用漂移。
5. 正文只选能说明设计和结果的关键图；大量操作过程可整理在附录或证据目录，按最终提交要求打包。GitHub是协作取材库，最终仍按Moodle要求提交文档、代码和视频。

示例图注：“图X：2026-11-01基础设施单机停止测试的健康目标数变化，随后恢复为2；来源：evidence/T09/2026-11-01-cloudwatch-dashboard-final.png，commit b6c091c。此测试使用基础健康服务，未验证业务写入。”

## 后续必须补的材料

业务版本commit与发布记录、真实新增/读取等功能结果、跨实例共享业务数据、业务故障与恢复日志、HTTPS证据、独立成员复核、完整成本估算、最终AWS架构图、可实际操作的视频。每轮新交付后在本页补映射，不覆盖旧记录或把计划当成已实现。

## 可直接交给组员AI的写作指令

> 请先拉取仓库最新main，读取AGENTS.md、docs/assignment-requirements.md、原始作业brief/rubric及docs/report-evidence-index.md。按我负责的章节整理报告草稿，读取真实PNG并准备嵌图，给每个结论标注证据路径、commit、测试时间与限制。区分基础设施测试和最终业务验证；未测的写待验证，不虚构结果、参考文献、个人贡献或同伴批准。缺少工具权限时明确列出需要本人提供的文件。正文控制在严格少于4,000词、少于8页的总报告限制内；现在先交草稿，不自动提交Moodle。
