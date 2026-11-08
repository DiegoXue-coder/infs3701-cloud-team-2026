# 共同开发约定

2026-10-31 由项目负责人授权建立自助工作流程后，指定以下开发默认要求，机器可读入口为 `project/handoffs.json`。这是实施要求，不代表已实现、部署或全员签认。

| 项目 | 开发默认要求 | 由谁实现/提供 |
| --- | --- | --- |
| 端口 | APP_PORT，默认 8000 | B 实现，A 部署配置 |
| 本地地址 | http://127.0.0.1:8000，仅开发 | B；C 测试使用 |
| 进程健康 | GET /health；不等同数据库读写成功 | B |
| 实例识别 | 响应头 X-App-Instance，由 APP_INSTANCE 配置 | B 实现，A 给两实例不同非敏感标签 |
| 测试地址 | BASE_URL，不把某台地址写死 | C |
| 数据字段 | record_id、title、status、pages_read、total_pages、rating、note、created_at | B 补类型/约束，C 写预期 |
| 本地数据 | 明确开发模式，无 AWS 凭证且不发起 AWS 请求 | B |
| 云端数据库 | DynamoDB，us-east-1，表 infs3701-team-books，record_id:String；READING_TABLE/AWS_DEFAULT_REGION；代码尚待接入 | A/B 核查后写入 handoffs |
| 启动方式 | B 交依赖和可复现命令；旧文件 port 80 不是新默认 | B |
| 部署版本 | 两实例同一 commit，配置另记 | A |

旧代码尚未实现上述新增接口；当前基线验证只检查语法与统计函数。实际云端 URL、数据库和部署版本仍为空，不编造值。参数变动通过 GitHub 文件与任务记录交接，不能只在私聊里通知。

目标云端运行环境：Python3.11，Gunicorn WSGI 入口 app:app；发布包与额外依赖规则见 docs/aws-owner-handoff.md。

## B 首轮数据契约（2026-11-03，待 A/C 复核）

以下为 T04 设计约定，T07 实现前不得视为现有行为。

| 字段 | 类型与约束 |
| --- | --- |
| record_id | 服务端生成 UUID 字符串，DynamoDB 分区键；同标题同秒新增也不得覆盖 |
| title | 去首尾空白后 1–120 字符，必填 |
| status | want / reading / finished，默认 reading；明确传入其他值返回 400 |
| pages_read | 非负整数，默认 0 |
| total_pages | 非负整数，默认 0 表示未知；已知时 pages_read 不得超过 total_pages |
| rating | null 或整数 1–5；空表单转 null |
| note | 字符串，默认空，最多 2000 字符 |
| created_at | 服务端 UTC ISO 8601 字符串，含时区；调用者不得覆盖 |

统计保留旧含义：total 为记录数，各状态分别计数，total_pages 统计键实际表示累计 pages_read（不是书籍总页数），avg_rating 只对非空评分取平均并保留一位小数，无评分为 null。进度 pct 为展示派生值，已知总页数时 round(pages_read / total_pages * 100)，未知为 null；不作为数据库必填字段。列表按 created_at 降序，同时间以 record_id 排序稳定化。

### 数据层与 HTTP 契约

- load_books() -> list[dict]：返回规范记录；读取失败须显式报错，不把失败显示为空书库。DynamoDB Scan 必须处理 LastEvaluatedKey；仅限小规模课程数据，全量统计不适合大规模场景。
- save_book(entry) -> str：验证后新增，返回 record_id；DynamoDB 用条件写避免覆盖，失败不得返回成功重定向。不提供编辑/删除接口。
- GET /：HTML 列表及统计；POST /：表单新增，成功 302 返回 /；输入无效 400，存储失败 503，页面不暴露内部异常或凭证。
- GET /health：200 JSON，表示进程可响应，不读数据库；不能当作云端写入验证。所有响应含 X-App-Instance，值来自 APP_INSTANCE，默认 local-dev，不使用机器私有地址。

### 配置和启动草案

READING_DATA_MODE 必须显式选择 local 或 dynamodb。local 仅作开发，用内存记录，重启清空，不导入/调用 boto3、不查找凭证、不发 AWS 请求，开发服务器仅绑定 127.0.0.1。dynamodb 使用 READING_TABLE 与 AWS_DEFAULT_REGION，缺配置则拒绝启动；云端使用实例角色，禁止复制凭证文件。旧 S3 数据不自动迁移、不删除。

T07 实现后的本地命令草案：`READING_DATA_MODE=local APP_PORT=8000 APP_INSTANCE=local-dev .venv/bin/python app/reading_tracker.py`。当前旧代码尚未支持，暂勿当作已验证启动命令。

部署使用 Python 3.11，Flask+boto3 及 Gunicorn，发布包 app.py 暴露 app:app；草案命令 `gunicorn --bind 0.0.0.0:8000 app:app`。依赖版本应以实际验证和 deployment/runtime-requirements.lock 对齐后交 A；本次仅在 macOS Python 3.9.6 完成依赖安装和旧统计离线检查，尚未验证 Python3.11 发布包。

数据库沿用 A 已选 DynamoDB：独立文档、无需关联，托管多 AZ，按请求计费适合间歇实验；代价是全表统计 Scan 的成本/延迟及当前吞吐上限。表与区域读 handoffs.json。A/C 请在 T04 核对部署与测试可行性；仍需 T07 实现、本地测试和实际云端验收。

## T07 implementation update (2026-11-07)

The local command, field validation, health endpoint and storage interfaces above
are implemented in `app/reading_tracker.py`. See [app startup and AWS handoff](../app/README.md).
Page counts support up to 38 digits in both modes to fit DynamoDB's number type.
The cloud health JSON identifies the release stage as `reading-tracker`.
Actual AWS write/read and restart persistence remain deployment acceptance checks.

## Published database contract (2026-11-08)

The 7 November release handoff records DynamoDB mode on both hosts for
`06c2292`. Local mode is development-only. A successful conditional PutItem
creates one UUID-keyed record, and each subsequent list request scans the same
table with ConsistentRead on each page. Scan does not offer snapshot isolation
across pages. A complete write/read check uses the business page and verifies
the same unique record and values from both labels. Health alone checks only
the serving process. See [release evidence](business-handoff-2026-11-07.md)
and [B verification](b-t11-verification.md).
