# Reading Tracker · 12 个月 AWS 成本草案

**USD 40.44／月，USD 485.28／12 个月，预付 USD 0.00。** 2026-11-07 在 AWS Pricing Calculator 中按 `us-east-1` 配置六项。计算场景为全年运行的双实例演示，按月 730 小时、全年 8,760 小时。以下是计算器摘要转录，金额未含税。 [AWS Pricing Calculator](https://calculator.aws/#/estimate)

| 计费项 | 输入假设 | USD／月 |
| --- | --- | ---: |
| EC2 与 gp3 | Linux 按需 2 × t3.micro，100% 运行率，各 8 GB gp3 | 16.46 |
| Application Load Balancer | 1 台全年。约 100,000 请求/月，处理量约 0.003 GB/小时，新连接约 0.04/秒、持续 1 秒。使用简单路由，规则额外负荷留空 | 16.45 |
| 公网 IPv4 | 2 个 ALB 使用中的地址，全年。实例位于私有子网 | 7.30 |
| DynamoDB Standard | 按需，项目平均 1 KB，存储 0.001 GB，月 0.8 百万次强一致读取单位等效输入，月 2 次标准写入 | 0.10 |
| CloudWatch | 1 dashboard、1 标准告警指标，计算器当前假设下的显示费用 | 0.10 |
| S3 Standard | 发布包 1 GB，月 1,000 次 PUT 类请求、10,000 次 GET 类请求 | 0.03 |
| **合计** | **六项基础场景** | **40.44** |

**读取假设。** 示例从 20 条虚构记录起步，每月净增 2 条，全年平均约 32 条。每项约 1 KiB 时，一个全表 Scan 近似读取 32 KiB，以 4 KiB 单位估约 8 个强一致读单位。每月 100,000 次业务首页读取对应约 800,000 个单位。`/health` 无数据库读，新增后的页面重定向读计入首页请求。表增长、分区、分页、项目大小和吞吐上限会改变开销与可用性，待用实际容量数据校准。 [AWS DynamoDB Scan](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html)

**定稿前复核。** A 核对账单中的公网 IPv4 实际数量、AMI/快照使用量、保留卷、账户 CloudWatch 免费额度和出站用量。当前六项合计未单列快照、额外日志、突发 CPU 额度、额外传输或未部署的 HTTPS 相关服务。约 2 GB/月互联网出站可按账户剩余额度复核。示例若另保留 8 GB 标准快照且适用 USD 0.05/GB-month，增加约 USD 4.80/年。实验 Lab 的实际运行时长和额度另行记录。 [AWS EBS 计价](https://aws.amazon.com/ebs/pricing/) · [AWS 数据传输计价](https://aws.amazon.com/ec2/pricing/on-demand/)

估算输入和结果保留在小组私有仓库供复核。计算器导出会生成可公开访问的共享地址，本次留档采用摘要转录。
