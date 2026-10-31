# 已选服务的原始基线归档

用户已于 2026-10-31 确认用自己的 Reading Tracker（Option A）。本目录保留原始基线，不在这里继续修改；后续升级使用 `app/reading_tracker.py`。历史文件名 reading_tracker_candidate.py 保留以维持引用。

基线仍使用 S3、单实例启动逻辑，固定 bucket 已替换为环境变量；尚未完成本次多 AZ、负载均衡、托管数据库和监控要求。不要把存有代码等同云服务已部署。
