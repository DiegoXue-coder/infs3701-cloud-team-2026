# 你先完成 AWS 基础，组员怎样接手

2026-11-01，A=DiegoXue-coder。实时资源清单见 project/aws-resources.json；下一批尚未执行的部署方案见 project/next-deployment.json。下面严格区分已创建和计划，不能把占位健康页面当 Reading Tracker。

## 已经实际完成

- VPC vpc-0836d003a70f93405，10.37.0.0/16，四子网跨 us-east-1a/b。实际 API 核对了两个公有子网共享 IGW 默认路由、两个私有子网各自没有公网默认路由，另有自动主路由表；总共四张路由表。
- DynamoDB 表 infs3701-team-books 为 ACTIVE，主键 record_id（String），按请求计费，读写吞吐上限分别为 10。现有实例的 LabRole 已通过真实 SSM 命令证明可 DescribeTable 和 Scan，表当时为空；没有写入或迁移旧书籍。
- 新的部署包桶 infs3701-team-artifacts-214018170594 已创建，四项公共访问阻止开启，AES256 加密，策略拒绝非 HTTPS 请求；旧读书记录桶完全不动。
- 临时构建实例 i-030acdefe159caa87：t3.micro，8 GiB 加密 gp3，无 IAM 角色、无入站规则；安装 Python3.11、Flask、boto3、Gunicorn，控制台日志出现成功标记。创建运行镜像 ami-03616f6b53c85f036，已核实 available、加密；构建实例已停止，磁盘/镜像仍保留。
- 旧实例/旧网站保留；没有复制它的凭证文件或用户数据到镜像。新镜像只含运行环境和明确写着 infrastructure-only 的健康占位程序，服务由 systemd/Gunicorn 管理的方式已准备，尚未在新私有实例验证。

## 数据库为什么这样选

读书记录是相互独立的文档，不需要多表关联或跨表事务；当前小规模演示可以用 record_id 定位、应用侧统计。DynamoDB 的托管多 AZ 韧性符合 brief 明确允许的托管 NoSQL 路线；不需要自行维护数据库实例。按请求计费适合不连续的课程测试，不把“RDS 太贵”当作无依据的结论。

代价：复杂关联/SQL 查询不方便；Scan 随数据增长成本和延迟会上升，B 要分页并控制数据量；10/10 上限是预算保护，也会限制压力测试，C 应先以小于 1 请求/秒的功能/故障测试取证，提升上限前先复核预算。数据库内置扩展不是应用自动扩容已实现，也不自动获得额外增强分。

依据：[DynamoDB 官方说明](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)、[计费模式](https://aws.amazon.com/dynamodb/pricing/)。

## 下一批：已准备，尚未执行

- 两台私有 t3.micro，各 8 GiB 加密 gp3，分别放入两个私有子网，不分配公网 IP；需要绑定课程预置 LabInstanceProfile/LabRole。
- 一个公网 ALB，初期仅 HTTP80，后端8000只接受 ALB 安全组；HTTPS 尚待证书方案。
- 一个 EC2 Instance Connect Endpoint：SSH22 只接受该维护端点的安全组，不把 SSH 向公网开放。
- S3/DynamoDB Gateway endpoints，只有两个私有路由表使用；策略限制 LabRole 通过 HTTPS 访问本项目发布包前缀/数据库表。私有实例出站443只允许两项 AWS 服务的前缀列表。
- 无 NAT，不自动增加持续收费的 NAT 或多个接口终端节点。依赖提前装入干净镜像，发布包经私有 S3 网关路径取得；运维走 EC2 Instance Connect Endpoint，而不是假设私有实例能直接联网 pip install。

网关端点路径依据：[AWS DynamoDB Gateway endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-ddb.html)。维护安全组设计依据：[EC2 Instance Connect Endpoint 安全组](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/eice-security-groups.html)。这些是设计依据，不是新私有实例的实测结果。

为新实例授予 LabRole 和开放公网入口属于新的访问配置，需要执行时确认。LabRole 比应用实际所需权限宽，Lab 不允许我们新建更窄角色/策略；deployment/policies/recommended-app-role-NOT-ATTACHED.json 只是推荐策略，不声称已附加。Gateway policies 也尚未应用。

## B 现在可直接做

从 T04/T07 继续。数据库资源已经由 A 建好，不需要 B 获得 AWS 凭证、另建数据库或等待重新选型。配置契约为 READING_TABLE=infs3701-team-books，AWS_DEFAULT_REGION=us-east-1，record_id 为 UUID 字符串。

后续部署包包含 app.py（WSGI app:app）、requirements.txt、所需模块/模板；源码可继续 app/reading_tracker.py，app.py 可作为导入入口。APP_PORT=8000，/health 与 X-App-Instance 约定保留，实例标识从 APP_INSTANCE 取。目标运行环境 Python3.11。默认继续 Flask+boto3；新增依赖先在 requirements 和交付中说明，让 A 准备镜像或离线依赖，不在私有主机临时联网安装。

B 交本地模式、DynamoDB 适配、输入约束、分页/统计逻辑、示例请求、实际测试和明晰的发布包。A 之后应用确切 commit 并验证真实云端身份；B 在个人 AI 没有 AWS 权限时不能声称云端读写通过。

## C 现在可直接做

先做 T08 的可执行测试和虚构数据集，复核 B 的本地版本。设计共享数据、分流、故障、告警、安全的检查步骤。新的 ALB/实例未创建或仅有占位页面时，不报告业务通过。

监控优先使用 ELB/EC2 原生指标，先交 dashboard/告警配置草稿、指标维度、阈值理由和触发/恢复步骤，不要求 A 临时设计。可考虑“健康目标少于两台”的可用性告警，但实际阈值和周期要解释并验证；不靠未部署的日志代理或自定义指标证明成功。成本需包含实际新资源、镜像/磁盘/ALB及运行时长，不只列 EC2。

## 你以后仍需配合什么

| 时点 | 你实际操作 | 组员要提前准备 |
| --- | --- | --- |
| B 第一版可运行 | 从指定版本部署两台，填真实参数 | B 的发布包、依赖、启动、配置与已知问题 |
| C 监控方案完成 | 应用 dashboard/告警配置 | C 的具体参数/脚本与测试方法 |
| 联合故障测试 | 按约定停/启指定新实例并恢复 | C 持续请求记录，B 检查应用和数据 |
| 录制/交付 | 展示实际架构，核对你的章节和贡献 | 三人各写各的理由/步骤，交叉复核 |

所以你可以先把基础设施做完，但不会在 B/C 尚未交付时就完全退出。把零碎操作合成短部署窗口，组员先写精确请求，减少你反复口头回复。

## HTTPS 待确认

brief 第2页要求 encryption in transit and at rest，但没有发放域名或要求购买域名。实际检查当前 us-east-1 ACM 证书列表与 Route53 hosted zones 都为空；用户不确定有无自有域名。没有购买/注册域名，也没有通过自签证书绕过浏览器安全提示。向 tutor 的待发问题：个人 Learner Lab 无已知可管理域名时，课程是否提供域名/证书，或认可哪一种 HTTPS 方式？此问题尚未实际发给 tutor，也无答复。

## 执行前核验补充

三项 EC2 DryRun 返回 DryRunOperation：携带 LabInstanceProfile 启动私有实例、DynamoDB gateway endpoint、EC2 Instance Connect Endpoint。这是权限/请求预检，不是实际部署或最终网络/端点策略测试。下一批脚本 deployment/launch-foundation.py 默认只输出离线计划，不连接 AWS，只有 --apply 才执行；尚未执行 --apply。运行镜像内实测 Python3.11.18，版本记录在 deployment/runtime-requirements.lock。
