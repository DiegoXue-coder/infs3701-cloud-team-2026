# 成员二：应用开发，拿到仓库即可开始

> 最新入口与实际限制：[本轮验证与三人交接](2026-11-01-foundation-verification.md)。新 ALB 已可做基础检查，业务应用尚未发布；不要把下面较早的“入口未创建”记录当最新状态。


先按 [自助入口](self-service.md) 配好自己的 AI/GitHub/Python，join B。只需要仓库访问权，不需要负责人 AWS 凭证。当前旧代码位于 `app/reading_tracker.py`，原始归档在 `reference/reading_tracker_candidate.py`。

2026-11-01 交接更新：A 已创建 DynamoDB 表 infs3701-team-books（us-east-1），主键 record_id:String，READING_TABLE 与 AWS_DEFAULT_REGION 作为配置。目标运行环境 Python3.11；读取 docs/aws-owner-handoff.md，不必再等待数据库重新选型，也不要索取 A 的 AWS 凭证。业务代码尚未接通，仍需本人真实实现和测试。

## 首项 T04：给所有人同一份运行约定

读取 `project/handoffs.json`。开发目标已指定：端口 8000（APP_PORT）、`/health`、实例响应头 X-App-Instance、配置 APP_INSTANCE、测试端 BASE_URL。它们是待实现要求，旧代码还未具备，不能直接声称已运行。

1. 读旧代码、运行基线检查，记录原来 S3 读写依赖。
2. 在 `docs/interfaces.md` 补清记录字段、状态取值、统计行为、配置名及数据层函数契约。遵循既定端口/路径，不另问负责人猜值。
3. 提供部署依赖和启动草案，列本地开发与真实 AWS 两种模式的差别。
4. 保存核对记录并 report；字段/API 确实符合 T04 验收后再 submit，等待 C 独立检查。首项完成前仍可准备 T07。

## 同时准备 T07：第一份可运行版本

- 先增加明确标为 local/development 的测试数据模式，保证这一路径不调用 boto3、不需要任何 AWS 身份；仅绑定本地地址作为开发用途。
- 增加健康路径与非敏感实例标识、输入处理；保留原功能，提供一条可复制的启动命令。需要新依赖时写入 requirements。
- 按已建 DynamoDB 表和 handoffs.json 实现适配代码，先分离数据读写接口；若实际功能缺少权限，在任务卡向 A 交具体操作/资源请求。不要自行换库或等待重新选型，不暂停本地版本。
- 用虚构数据证明新增/查询和统计的实际结果；本地数据不是最终托管数据库证据。

## 交给 A/C 的包

在 `deliveries/T07/` 上报真实版本，附：commit、依赖、启动命令、配置变量、示例输入输出、数据模式、健康路径、测试记录、已知问题。A 据此部署；C 据此测试。不要交“代码好了”但无运行说明的版本。

## 等 A 部署期间

继续输入与统计测试、数据库代码、运行说明和应用章节；从 Issue 读取 C 的失败案例并复现。A 更新真实 URL 后，再配合云端验证；没有云端权限时准确记录 A 实际执行，B 设计/指导。
