# Reading Tracker 发布批次与操作记录

操作者：DiegoXue-coder（A，由本次 AI 会话协助）。程序作者：Alex4325Li（B）。C 的独立云端复核尚未进行。

本会话用户已对下述具体公开范围回复“同意，按此范围发布虚构数据演示”。随后执行逐台发布；本文件中的准备记录按原时间保留，最新实测结果另见本轮最终交接与执行证据。

## 已完成的准备

- 2026-11-07 12:01 UTC 实际 AWS 查询：两台目标 running/healthy，ALB active；两次 az-a、两次 az-b 的 /health 均为200，stage=infrastructure-only；GET / 仍为基础占位页。DynamoDB ACTIVE，强一致 COUNT 实际0条、无后续页。两个网关端点 available。告警状态 OK，但状态理由是11月1日旧数据，不把它称为当前监控数据新鲜度验证。无通知订阅。
- 发布源码固定 `06c2292cdf0aca80f050709b8172fac3595b54cc`，直接从Git对象取文件，不依赖工作区换行。
- 包仅含 `app.py` 与 `requirements.txt`，计划及各文件哈希：[business-release-plan.json](../project/business-release-plan.json)。包SHA256：`fc40e1969c6b90f154b120979aaddf45f554d6e5fdd0fa6b0b2d17fd2ac980cd`。
- 程序包已上传既有私有桶并下载比对哈希，无公开ACL。路径：`s3://infs3701-team-artifacts-214018170594/releases/reading-tracker/06c2292cdf0aca80f050709b8172fac3595b54cc/app.tar.gz`。CloudShell暂存目录：`~/infs3701-release-06c2292`。
- 三项离线测试已通过，覆盖固定包/启动负载解析、健康失败恢复旧环境并阻止自动重试、损坏包无法切换服务。离线测试使用模拟服务，不代表实际Linux/AWS恢复成功。实际运行日志：[release-safety-tests.log](../evidence/T09/2026-11-07-A-release-safety-tests.log)。

## 待确认的具体影响

把现有HTTP负载均衡入口从基础测试页换为 Reading Tracker 后，任何知道地址的访客均可查看和新增演示记录；当前没有登录或CSRF保护。仅输入虚构书名与测试文字，不输入私人信息。此批不新增AWS资源、开放端口、IAM权限、账号或成员凭证；仍使用原先两台私有实例、LabInstanceProfile和既有DynamoDB/S3端点。HTTP尚无TLS，不能称安全要求全部完成。

## 确认后的操作顺序

1. `python3 ~/infs3701-release-06c2292/release-business.py prepare --instance a --directory ~/infs3701-release-06c2292`。脚本先确认另一台healthy，再停止A；保存原始user-data属性。
2. inspect查询，等A实际stopped，再执行同命令的 `start` 阶段。写入小于16KiB的每次启动脚本；不连SSH、不改IAM。
3. 启动脚本先保留基础app和env，从私有S3取固定包、核对归档和两文件哈希，检查生产Python的依赖锁，设置dynamodb模式和az-a标签；原systemd服务继续使用Gunicorn8000。读取/health和真实GET /，成功打印带commit/哈希/标签的 `INFS3701_RELEASE_OK`。外部还需核对目标healthy和实际业务页面。
4. 第一台成功后才对B做同样操作。A/B分别是 `i-00572a14ca8b71156`（us-east-1a）和 `i-0081259c52a32e051`（us-east-1b）。
5. 只创建少量有唯一标记的虚构记录，记录接收POST的实例标签，再从另一标签读回；重启一台，确认同一数据仍能读到。保留原始记录与截图，不清空数据库。
6. 更新handoffs中的实际commit/标签和验证时间，向Marina提供真实URL与精确版本。她独立进行T12/T11相关复测；A的日志不冒充C的验收。

每个阶段独立返回，不循环停启。`inspect` 显示目标状态与有界项目启动诊断，不输出临时密钥。

## 失败与恢复

健康或真实业务GET失败时，主机脚本恢复该次切换前的路径和env、重启旧服务，并保存该commit的失败阻止标记；A须读实际诊断，不能继续第二台。第一次部署前的基础目录和env另有不可覆盖备份。

显式回基础版本：先确认另一台健康，用prepare停止失败主机，等stopped后执行 `rollback-start --instance a|b --directory ~/infs3701-release-06c2292`。新每次启动脚本恢复基础目录与env，并验证 infrastructure-only。不要用旧maintain-foundation.py的restore-userdata冒充业务恢复；仅恢复EC2属性不能清除缓存脚本。失败包重试前须调查原因、审核修正和失败阻止标记，不能自动无限重试。

此方法保留数据库、旧EC2/S3、基础备份及发布文件。实际回退目前尚未在云端执行，不声称演练通过。
