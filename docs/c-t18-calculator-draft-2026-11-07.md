# Reading Tracker · 12-month AWS cost draft

**USD 40.44 per month, USD 485.28 for 12 months, upfront USD 0.00.** Six items were configured in the AWS Pricing Calculator for `us-east-1` on 2026-11-07. The scenario is a two-instance demo running all year, at 730 hours per month and 8,760 hours per year. The following is a transcription of the calculator summary; amounts exclude tax. [AWS Pricing Calculator](https://calculator.aws/#/estimate)

| Billing item | Input assumptions | USD per month |
| --- | --- | ---: |
| EC2 and gp3 | Linux on-demand 2 × t3.micro, 100% utilisation, 8 GB gp3 each | 16.46 |
| Application Load Balancer | 1 for the full year. About 100,000 requests/month, about 0.003 GB/hour processed, about 0.04 new connections/second lasting 1 second. Simple routing, extra rule load left blank | 16.45 |
| Public IPv4 | 2 addresses in use by the ALB, all year. Instances are in private subnets | 7.30 |
| DynamoDB Standard | On-demand, average item 1 KB, storage 0.001 GB, input equivalent to 0.8 million strongly consistent read units per month, 2 standard writes per month | 0.10 |
| CloudWatch | 1 dashboard, 1 standard alarm metric; the charge shown under the calculator's current assumptions | 0.10 |
| S3 Standard | 1 GB release package, 1,000 PUT-class and 10,000 GET-class requests per month | 0.03 |
| **Total** | **Six-item base scenario** | **40.44** |

**Read assumption.** The example starts from 20 fictional records and adds a net 2 per month, averaging about 32 over the year. At about 1 KiB per item, one full-table Scan reads roughly 32 KiB, estimated at about 8 strongly consistent read units in 4 KiB units. 100,000 business home-page reads per month correspond to about 800,000 units. `/health` makes no database read, and the page redirect read after an insert is counted in home-page requests. Table growth, partitions, pagination, item size and throughput caps change the cost and availability, to be calibrated with actual capacity data. [AWS DynamoDB Scan](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html)

**Review before finalising.** A checks the actual number of public IPv4 addresses on the bill, AMI/snapshot usage, retained volumes, the account's CloudWatch free tier and egress usage. The current six-item total does not separately list snapshots, extra logs, burst CPU credits, extra transfer or undeployed HTTPS-related services. About 2 GB/month of internet egress can be reviewed against the account's remaining allowance. As an example, keeping an additional 8 GB standard snapshot at USD 0.05/GB-month would add about USD 4.80 per year. The Lab's actual running hours and credit are recorded separately. [AWS EBS pricing](https://aws.amazon.com/ebs/pricing/) · [AWS data transfer pricing](https://aws.amazon.com/ec2/pricing/on-demand/)

The estimate's inputs and results are kept in the group's private repository for review. A calculator export generates a publicly accessible share address, so a summary transcription is used for the record this time.
