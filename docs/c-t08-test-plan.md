# C / T08 测试与证据计划

作者账号：Marina057；AI 协助：Codex。2026-11-04。初轮测试在角色登记前本地执行。2026-11-04已以Marina057登记C并认领T08；认领回执R-T08-6624693113。本文提交范围为T08测试准备；后续云端验证另属T12/T13/T14。

## 已执行的范围

基于 Chrome 下载的 main 源码副本，页面对应提交 6a8da48b5fc5d932bc25a56054a1cd0cc605c5b8。Windows / Python 3.12.14；云端目标 Python 3.11 尚未复测。没有导入 Flask/boto3，没有连接 AWS，没有创建或改变云资源。

- `tests/c_t08/fixtures.json`：四组虚构统计记录及手工预期；另有八项将来 HTTP 验收输入。
- `tests/c_t08/test_statistics.py`：AST 提取原函数，10 项测试全部通过；包含页数语义、未评分排除、顺序不变性、重复记录、输入不变性、旧格式及异常数值行为。
- `scripts/c_request_log.py`：只读、有限次数的 HTTP 访问工具。
- `tests/c_t08/test_request_log.py`：7 项实际 loopback HTTP 测试通过，覆盖 BASE_URL、200、503、超时、缺少实例头、参数上限、证据防覆盖。
- 持久样本 `evidence/T08/2026-11-04-local-fixture-requests.jsonl` 的四条成功响应全部来自 `local-fixture-only`，不是负载均衡或 Reading Tracker 业务证据。

原函数 SHA-256：`f1f20663612aa3343f5bce9f9acc749da2c8def46eea8e369fdcdc7bfd7e5d10`。统计测试不证明 HTTP 输入验证、DynamoDB 读写或 Python3.11 部署通过。

## 复现方法

在仓库根目录，用 Python 3.9+（本次为 3.12.14）：

```text
python tests/c_t08/test_statistics.py
python tests/c_t08/test_request_log.py
```

第二条会启动临时 loopback 测试服务并自动关闭，不需要依赖安装或 AWS 身份。首次执行保存四条本地样本；已有该证据文件时使用临时输出，不覆盖历史。

访问指定环境的 PowerShell 示例（仅在确认端点/版本后执行）：

```powershell
$env:BASE_URL='http://127.0.0.1:8000/health'
python scripts/c_request_log.py --count 12 --interval 1 --timeout 5 --stage local-fixture --output evidence/T08/new-local-requests.jsonl
```

云端入口从最新 `project/handoffs.json` 获取；基础环境用 `--stage infrastructure-only`，业务发布后才用 `--stage business-release`。stage 是人工标签，不能自动证明部署身份。脚本不会保存正文或跟随重定向；耗时截至响应头，不是整页加载时间。返回码 0 表示所有样本 2xx，1 表示至少一个失败。文件已存在则拒绝覆盖。要识别分流必须同时检查 `instances` 和 `missing_instance`；200 不代表数据库正常。

## core 验收矩阵（以下尚未执行）

| 要求 | 操作与预期 | 证据 | 操作/检查 |
| --- | --- | --- | --- |
| 可用界面与后端 | 对 B 发布版本新增一条虚构记录，302 后列表及统计准确；无效输入400且未写库；存储故障503而非空列表 | 版本、输入、HTTP输出、浏览器截图、记录ID | C执行，B复核 |
| 共享托管数据/无状态 | 新增后多次读取，确认不同实例显示同一记录；单机重启后记录仍在；DynamoDB读写独立核对 | 实例头、同一record_id、表记录、重启时间 | A操作AWS，C取证，B核对 |
| 分流 | 确认两实例同版本/标签，持续请求；预期样本至少看到两标签，不要求严格50:50 | 完整逐条JSONL、实例计数、target健康状态 | C执行，A复核 |
| 实例故障 | 先确认两台健康，C持续采样，A一次停止一台；记录过渡失败与恢复，修复后再确认两台健康 | 停/启UTC、首个失败/最后失败、失败数、监控和请求原始日志 | A停/启，C记录，B复核 |
| AZ韧性 | 检查跨AZ拓扑和托管数据库；如课程允许，再设计并批准AZ级实验；一次单机停止仅证明该实验范围 | 子网/AZ映射、实际实验覆盖声明 | A提供，C核对 |
| 监控 | 读回实际dashboard/alarm；真实健康数下降后ALARM、恢复后OK | 配置JSON、指标点、状态历史、UTC截图 | A操作，C独立核对 |
| 网络/最小权限 | 核对ALB入口、后端仅ALB来源、私有机无公网IP、实例角色与数据库/桶策略 | 只读配置与被拒绝的越权访问证据；不扩大权限 | A读取，C核对 |
| 加密 | 核查EBS/桶/数据库加密；浏览器有效HTTPS及证书；后端链路另行说明 | 证书、listener、加密属性 | A操作，C核对；当前HTTPS未验收 |
| 横向扩容 | 核查应用无本机持久状态；新增实例/自动扩容若启用须另做真实实验 | 版本配置、实例变化、请求与数据一致性 | A/B实施，C取证 |

## 输入边界与缺陷交接

B 的 2026-11-03 契约见 `docs/interfaces.md`。除 fixtures 中八项外，还需测 title 的120/121字符、note 的2000/2001字符、整数边界、同标题同秒不覆盖、用户不能覆盖 created_at、DynamoDB多页Scan、读取失败明确报错。当前未对业务HTTP执行这些测试。

原统计函数会接受某些不合法值（例如负页数、未知状态），非数字字符串会抛 ValueError；这是旧函数行为的记录，不是合格的输入验证。B应在入库前验证，C在T07实际版本上重新验收。不修改旧代码或把预期规则说成现有功能。

每个问题记录：版本/地址、重现输入、期望、实际、UTC、日志路径、归属A/B或待定位、修复后复测结果。当前没有业务版本，以上风险尚非对B新实现的失败结论。
