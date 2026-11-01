# 本轮基础设施与三人交接

这是 A（DiegoXue-coder）实际执行的环境工作，不能算成 B/C 的贡献或复核。实时状态要回到 AWS 检查；本文及 GitHub 看板是带时间的记录。

## 现在可以用什么

- 区域 us-east-1，新 VPC 跨 us-east-1a/b。两台私有 t3.micro 各使用 8 GiB 加密 gp3，绑定 LabInstanceProfile，无公网 IP，IMDSv2 required。
- 基础测试入口：<http://infs3701-team-alb-788523332.us-east-1.elb.amazonaws.com/>。页面明确标着业务应用尚未部署。`/health` 返回实例标识，响应头为 X-App-Instance。
- DynamoDB：infs3701-team-books，主键 record_id:String；区域与表名通过 AWS_DEFAULT_REGION、READING_TABLE 配置。旧 S3 记录未迁移。
- 私有发布桶：infs3701-team-artifacts-214018170594。四项公共访问阻止、静态 AES256 加密、拒绝非 HTTPS。
- 两个私有路由表各有 S3/DynamoDB gateway 路由，没有公网默认路由或 NAT。端点策略只允许 LabRole 通过 HTTPS 访问指定项目资源；主机出站443只到两项服务前缀列表。DynamoDB当前允许 DescribeTable、Scan、GetItem、PutItem；未允许 DeleteItem/UpdateItem。B不能假设任意数据库操作已获准；需要额外操作时提交具体请求。
- ALB 只公开 HTTP80；后端8000只接受 ALB 安全组。LabRole 仍宽于实际需要，不能写成完整最小权限已经实现。
- Python3.11.18 / Flask / boto3 / Gunicorn 已在加密镜像中预装，systemd 管理程序。具体依赖见 deployment/runtime-requirements.lock。

初次真实分流取样：12 个请求全部200，az-a/b各6个，见 evidence/T09/2026-11-01-live-routing.log。这个短样本不证明长期可用率，也不证明业务功能或整个 AZ 故障通过。

## 运维方式的实际限制

EC2 Instance Connect Endpoint 已创建，但学生身份实际连接收到 ec2-instance-connect:OpenTunnel 权限拒绝。DryRun 只能检查创建请求，不能代表连接可用。没有改 IAM 绕过拒绝，也没有新增收费的 SSM 接口端点。

替代方案已在两台新主机实际通过：只使用持有人的现有 EC2 管理能力，一次停止一台，更新 user-data，启动，读取 console output，确认健康后再处理另一台。两台均出现 BOOT_CHECK_OK，凭证来源 iam-role，DynamoDB ACTIVE/记录数0，S3对象哈希一致、本机健康正常；两台随后均为 healthy。deployment/maintain-foundation.py 对账号、VPC、主机 ID 和另一台健康状态设有检查，并备份原 user-data；不是通用任意主机执行器。

验证后已关闭新应用安全组的22入站与未使用EIC安全组的22出站。EIC资源保留，不能作为可用登录通道；未做永久删除。

脚本用 MIME `text/x-shellscript-per-boot` 注册每次启动检查。不能把默认只执行一次的普通 shell user-data 当成重复部署机制。它目前检查角色凭证来源、DynamoDB Describe/Scan、S3 固定测试对象哈希和本机健康；不写业务数据，也不会安装 B 的业务发布包。

资料依据：[EC2 user-data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)、[cloud-init MIME 与每次启动脚本](https://docs.cloud-init.io/en/latest/explanation/format/mime.html)。实际结果以维护验证日志为准，文档模式本身不算测试成功。

A 重做基础检查时：在已登录本账号的 CloudShell 保存已审核的 maintain-foundation.py，先运行 `python3 maintain-foundation.py --instance a --phase prepare`；待 EC2 显示 stopped，再运行同参数的 `--phase start`。随后 `--phase inspect`，确认 BOOT_CHECK_OK 且目标 healthy，才可对 b 重复这三步。不得同时 prepare 两台；不要对旧实例使用；这组命令不负责发布新业务代码。

## 监控基线

Dashboard：infs3701-team-dashboard，6个组件，包含健康目标、请求/5xx、响应时间p95、两实例CPU、数据库读写容量，以及限制说明。

Alarm：infs3701-team-healthy-targets-below-two。ALB+TargetGroup 两个维度，HealthyHostCount 的 Minimum，60秒周期，连续2个点低于2，缺失点按不告警处理。含义是双机冗余下降，不能解释成全部服务中断；没有 SNS/邮件收件人，不能声称已通知真人。缺失点处理会掩盖某些无数据情形，C 应复核并补充可用性监测。

单机停止、请求和真实状态变化见 evidence/T09/2026-11-01-maintenance-validation.log：05:56:06UTC 告警真实转为 ALARM（05:56:15 读取到），依据05:52/05:53UTC的健康数1；两台恢复后，06:00:06UTC 实际 ALARM→OK；依据真实健康数2的数据点，完整历史在 final-readback.log。不用 SetAlarmState 人工伪造触发。C 仍需独立检查指标、阈值、业务功能和最终应用的故障行为。

原始日志保留了一处取样脚本的汇总错误：单机短样本实际有6条REQUEST、实例计数6，汇总字段requests仍打印硬编码12；真实数量按逐条记录为6。之后持续样本另有25条单机响应200。采样脚本已把请求数量改成统一变量。初次双机12条、各6条的记录不受此错误影响；这些样本没有覆盖整个停/启瞬间，不能据此声称零停机切换。

## B 今天可以开始，不等 A

1. 接受私有仓库邀请，按 docs/self-service.md 用本人 GitHub 认证并 join B；读 AGENTS.md，认领 T04/T07。
2. 原代码在 app/reading_tracker.py，原始快照在 reference/reading_tracker_candidate.py。先提供无需 AWS 身份的本地模式，再实现 DynamoDB 适配，不向 A 索要凭证。
3. 契约：端口8000，WSGI `app:app`，`/health`，APP_INSTANCE 对应 X-App-Instance。环境为 Python3.11，READING_TABLE 与 AWS_DEFAULT_REGION 如上。
4. 交付确切 commit、app.py入口、requirements、模板/模块、示例输入输出、本地测试记录、数据库字段与已知问题。新增依赖必须先说明；私有实例不能直接去公网 pip install。
5. 在 T07 上报交付回执。A 根据这个版本准备真实发布步骤/包、部署并记录云端结果；当前维护检查脚本不能直接当业务发布器。B 的代码交付后，云端部署仍需要 A 的一次操作窗口。

## C 今天可以开始，不等 B

1. 接受邀请，按自助入口 join C，认领 T08，读资料和旧代码。
2. 先交虚构数据集、统计/输入边界预期、可执行访问工具及真实本地日志，BASE_URL 可配置。
3. 可用上述测试入口检查响应时间、实例标识、工具格式；必须标记 infrastructure-only，不能测试页200就算 Reading Tracker 功能通过。
4. 复核已有 dashboard/alarm 配置，提出改进与阈值理由。A 的实际配置和记录不能算成自己已做的独立验收。
5. 准备12个月成本假设（包括ALB、磁盘和镜像）、报告与视频取证脚本；真实业务联合测试在 B/A 发布后进行。

## 你以后需要配合的三个窗口

| 窗口 | 组员先交什么 | A 操作什么 | 完成后谁接着做 |
| --- | --- | --- | --- |
| 首次业务发布 | B 的确切版本、发布包和本地测试 | 审核依赖，逐台发布，记录版本/参数/健康结果 | C 独立验证真实业务，B 修复失败 |
| 联合测试 | C 的请求脚本、监控参数和恢复步骤 | 停/启一台、恢复，配合取证 | C 记录请求/告警/恢复，B 检查共享数据 |
| 最终复核 | 三人的各自章节、成本和证据 | 核对真实资源与图，提供操作演示 | 另一账号复核交付，三人确认提交件 |

每次先 pull/start，读取最新 Issue。B/C 在任务回执里给出参数和步骤，A 集中处理；不存在后台自动执行 AWS 的机器人，也不能保证 A 离线时云端请求立即执行。

## 尚未完成，不能省略

Reading Tracker 新业务发布、真实托管数据库写入/读取、业务故障与共享数据测试、HTTPS、自动扩容/增强项决定、完整成本/报告/架构图/视频、独立交叉复核。

brief 要求传输加密，没有提供域名，也没有要求购买域名。当前无已知可管理域名、ACM证书或Route53 hosted zone；需向 tutor 确认课程认可的证书/域名方案。没有发送老师消息、购买域名或绕过浏览器证书警告。

构建实例已停止。运行的两台应用实例、ALB、EBS、AMI快照和监控可能继续消耗额度；本轮没有永久删除资源。Lab预算界面的延迟读数不能当作本次消耗或12个月成本。后续结束测试时按课程资源保留要求安排停机与清理。

最终配置核验时间：2026-11-01T06:01:13.014386+00:00。48项离线测试另见 foundation-maintenance-offline-tests.log；离线通过不代替云端证据。维护工具的 restore-userdata 只恢复 EC2 元数据字段，不能移除已缓存的每次启动脚本，也不是业务版本回滚器。
