# Reading Tracker · 60 秒录制脚本

候选录制版本 `06c2292`。每人负责自己的解说。录屏使用实际业务与当次日志，建议录制窗口统一 UTC，按以下剪辑时码压缩等待。时长按组内暂定 60 秒准备。

| 时码 | 出镜与画面 | 英文解说草稿 |
| --- | --- | --- |
| 0–11s | Diego，展示业务入口和双 AZ 架构图 | “Reading Tracker uses one load balancer across two Availability Zones. Each private EC2 instance runs the same release.” |
| 11–24s | Alex，填写一条独特的虚构记录，显示保存后的列表和统计 | “I add a fictional reading record. The application writes to DynamoDB, so either server can read the same progress and rating.” |
| 24–37s | Marina，在日志中标出 `az-a`、`az-b` 和状态列，切到记录读回 | “I independently checked the same record on both instances. In a 30-request sample, each instance served 15 requests, and all returned HTTP 200.” |
| 37–52s | Diego 实际停一台，Marina 展示同步日志及 CloudWatch 告警历史。镜头等待可剪辑，保留实际 UTC | “During the single-instance test, we tracked requests to the surviving target and compared the results with the CloudWatch alarm history.” |
| 52–60s | Marina 展示恢复后两标签与同一条记录，Diego 出示恢复证据 | “After recovery, we check both targets again and confirm the record is still available.” |

录制素材归档时保留版本、日期、实际操作者和对应日志。停机、告警与恢复段须等联合测试取得真实画面后剪入，并按实际失败数改解说。业务入口为当前 HTTP 演示，记录全部用虚构数据。 [部署交接](business-handoff-2026-11-07.md) · [独立云端证据](c-t12-cloud-validation-2026-11-07.md)
