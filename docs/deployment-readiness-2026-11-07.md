# T09 业务发布前核对（2026-11-07）

由DiegoXue-coder的AI读取最新T07/T12交付并复跑本地候选版。候选commit：`06c2292cdf0aca80f050709b8172fac3595b54cc`。本次检出版本与该commit的app/reading_tracker.py、运行依赖锁无差异。

## 已实际通过

- 4项应用测试：[日志](../evidence/T09/2026-11-07-A-candidate-app-tests.log)。包含本地新增读回、健康与实例头、DynamoDB分页/条件写的Stubber测试、存储异常和配置验证。
- 17项C回归：[日志](../evidence/T09/2026-11-07-A-candidate-regression.log)。
- 本地HTTP健康、8项表单输入、页面读回及4次采样：[日志](../evidence/T09/2026-11-07-A-candidate-http.log)、[JSONL](../evidence/T09/2026-11-07-A-candidate-local-samples.jsonl)。

环境为本机Windows/Python3.12.14；上述不是Linux/Python3.11/Gunicorn或真实AWS验收。未在本轮部署、上传AWS发布包、写云数据库、停启实例或公开业务页面。T07仍应保留partial，直到真实写入、跨实例读回及重启保留得到验证。

## 正式发布必须处理

现有 `deployment/maintain-foundation.py` 的每次启动脚本会重写 `/etc/infs3701/app.env`，只适用于基础占位服务；缺少新应用要求的 `READING_DATA_MODE=dynamodb`，也不安装业务包。单独复制app.py后重启不是完整发布方法。

发布需准备可审核的新业务启动/发布步骤：固定上述commit与包哈希；从既有私有S3 release前缀读取；保留现有app、环境和版本信息；正确设置READING_DATA_MODE、READING_TABLE、AWS_DEFAULT_REGION、APP_INSTANCE；校验Gunicorn与运行依赖；一次发布一台，先核对本机健康与真实业务读取，再处理另一台。失败时恢复该台上一版app和环境，保留数据库，复核目标健康。

原计划主机标签为az-a/az-b，当前实例、ALB和数据库状态须在本次已登录Lab重新读取，不将11月1日的状态当作当前状态。IAM与网络原则上沿用现有资源，若实际发现需新增权限，先记录具体差异。旧EC2、旧S3记录不自动迁移或改写。

公开入口目前只批准过HTTP基础测试页。实际替换为可新增/读取数据的Reading Tracker前，须向用户说明公开演示页面和数据写入范围并取得对应确认；只使用虚构测试数据。HTTPS仍单独待解决，不称作全部安全要求通过。

## 发布后向Marina交接

在T09/T10及handoffs中记录真实业务URL、部署commit、源码/包哈希、两台标签与实例/AZ对照；提供首次云端新增/读回结果。先验证另一标签对应实例可读同一条记录，再重启一台确认数据保留，最后由C独立复测并记录分流/故障/告警。收到截图中的请求不代表这些操作已经完成。
