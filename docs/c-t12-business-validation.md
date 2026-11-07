# T12 联调准备与 T07 候选版复核

Marina057（C），2026-11-07 悉尼时间。候选版 `06c2292cdf0aca80f050709b8172fac3595b54cc`。本次使用 Windows、Python 3.12.14 及 `deployment/runtime-requirements.lock` 中的依赖。对比候选版与本次检出的应用、原有测试、采样器和依赖锁，相关文件无差异。

## 接口与本地复现

| 接口约定 | 独立复现结果 | 证据 |
| --- | --- | --- |
| `GET /health` 200，`stage=reading-tracker`，响应头与 JSON 实例名一致 | 真实回环 HTTP 检查通过，模拟存储异常测试也确认健康端点无需读表 | [HTTP 日志](../evidence/T12/2026-11-07-Marina057-local-http.log) |
| `POST /` 成功返回 302，输入不合法返回 400 | T08 表单夹具 8 项通过。7 个无效请求返回 400，唯一有效请求返回 302，随后页面显示一条记录和 10 页 | [HTTP 日志](../evidence/T12/2026-11-07-Marina057-local-http.log) |
| DynamoDB 条件新增、强一致分页读取、存储异常返回 503 | Alex 的 4 项测试独立复跑通过，存储交互由 botocore Stubber 或模拟异常验证 | [T07 回归](../evidence/T12/2026-11-07-Marina057-t07-regression.log) |
| 既有统计和采样器兼容 | 原 T08 17 项全部复跑通过。对真实本地候选版采样 4 次全部 2xx，标签均为 `t12-local-candidate` | [T08 回归](../evidence/T12/2026-11-07-Marina057-t08-regression.log) · [采样 JSONL](../evidence/T12/2026-11-07-Marina057-local-samples.jsonl) |

复现可使用 `python -m unittest discover -s tests -p test_reading_tracker.py -v`、`python -m unittest discover -s tests/c_t08 -v` 及 `python tests/smoke_t12_http.py --samples <新的本地日志路径>`。测试服务器绑定 `127.0.0.1`，用内存数据，运行后关闭。Linux Python 3.11/Gunicorn、真实实例角色和持久化仍在联合验证范围内。

## 部署交接与取证顺序

1. Diego 在 T09/T10 登记部署 SHA、对外业务 URL、两台实例的不同 `APP_INSTANCE` 标签及其目标组/AZ 对照。按 [部署说明](../app/README.md) 逐台发布、核对本机业务页和目标健康。`/health` 的 JSON 没有 SHA，部署版本用 A 的发布记录和两台主机上的版本证据核对。
2. 双机业务发布后，用小批量 `GET /health` 确认两台均返回 200、`stage=reading-tracker`，且 JSON 实例名、`X-App-Instance` 与交接表一致。若看到占位页、未知标签或 5xx，保留日志交 A/B 排查。入口使用 A 确认的协议及最终地址。
3. A 在确定标签的实例上提交一条独特标题的虚构记录，留 POST 302、目标标签和时间。C 在另一台标签对应的页面确认同一条记录，A 重启一台应用后再次读回。记录成功响应和可见性分开，写入超时先查该唯一标题再决定是否重试。使用本轮测试记录，不纳入个人数据。
4. C 在确认小流量窗口后对业务 `GET /` 采样，建议 30 次、每 2 秒一次、单次超时 5 秒。使用 `python scripts/c_request_log.py --url <业务根地址> --count 30 --interval 2 --timeout 5 --stage business-release --output <新的JSONL路径>`。记录两个预期标签各自次数、缺失/未知标签、HTTP 状态和失败数。分流通过条件为两台均有成功样本，且标签匹配交接表。工具的 2xx 汇总需与业务版本核对和读回证据一起使用。
5. A 导出同一 UTC 窗口内的 dashboard 图和配置。C 对齐采样日志、目标健康和 `RequestCount`，并区分 `HTTPCode_ELB_5XX_Count` 与 `HTTPCode_Target_5XX_Count`。现有监控模板的 ALB+TargetGroup 健康目标、`TargetResponseTime` 和表读写容量指标继续使用。图表缺数应记录，延迟图结合样本量解释。 [监控模板与参数](c-t08-monitoring.md) · [AWS ALB 指标文档](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-cloudwatch-metrics.html)
6. T11/T12 联合条件满足后，A 按既有 T13/T14 方案一次只停一台并恢复，C 记录实际 UTC、请求失败窗口、告警 `OK → ALARM → OK` 历史及恢复后业务读回。双方核对成功标准，再各自提交真实证据。 [故障与告警取证方案](c-t08-monitoring.md)

## 成本及报告增补

T08 的成本草稿曾用最终一致读举例。当前候选版每次业务首页读取执行 `ConsistentRead=True` 的全表分页 Scan，T18 应按每月业务首页次数乘以每次全表读取的实际消耗单位估算。健康端点不读表，浏览器跟随新增后的 302 会再读取首页。小规模验证时记录表大小、页数、用量和 UTC 窗口，可由 A/B 用 `ReturnConsumedCapacity=TOTAL` 或 CloudWatch 用量做校准。容量单位与每月请求次数分列，存储和写入保留独立假设。 [T08 成本草稿](c-t08-cost-assumptions.md) · [AWS DynamoDB Scan 文档](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html)

报告可写入本轮已复现的 HTTP 状态、4 项应用测试和 17 项回归。部署 SHA、两个目标的采样分布、读写持久化、故障窗口和告警历史在联合测试后补齐。T12 当前为准备上报，完整验收等待 T10 和业务现场证据。
