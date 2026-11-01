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
