# Draft inputs for the 12-month cost estimate

T08 / Marina057 / 2026-11-04. Region us-east-1, currency USD. This only organises services and assumptions; no AWS Pricing Calculator estimate, quote or cost PDF was produced. The Lab balance is a historical observation and is not a basis for this cost or annual pricing.

## Steady low-traffic scenario (for T18 to enter into the calculator)

| Service | Assumed input | Billing items to confirm |
| --- | --- | --- |
| EC2 | 2 t3.micro, Linux, on-demand, 8760 hours per instance per year; monthly average 730 hours per instance | Instance type/OS/region, CPU surplus-credit policy; no savings plan promised |
| EBS | Two 8 GiB gp3 volumes, 16 GiB total, all year; no extra provisioned IOPS/throughput | Baseline IOPS/throughput included by the calculator; disk retention cost after restart/stop |
| ALB | 1 for the full 8760 hours; example 100000 requests/month, average response 20 KiB, request 2 KiB | The four LCU dimensions: active/new connections, rules, processed bytes; the example is not a measurement; public IPv4 listed separately by actual address-hours to avoid omission |
| DynamoDB | on-demand, example 10000 writes/month, 100000 eventually consistent reads/month, about 1 KiB per item, 1 GiB storage | Recalculate by read/write request units and Scan pagination amplification; backup/PITR not assumed included if not enabled |
| S3 release bucket | Standard, about 1 GiB; 1000 PUT, 10000 GET/month | Requests, storage, whether logging is enabled; the old personal S3 bucket is not automatically included in the final business |
| AMI/EBS snapshot | Example 8 GiB of effective snapshot storage, to be revised with the actual snapshot billed size | An AMI is not a free disk copy; incremental snapshots are not blindly costed at logical capacity |
| CloudWatch | Existing 1 dashboard, 1 standard alarm; native metrics, detailed EC2 monitoring not enabled | Free tier not guaranteed to apply; custom metrics/log ingestion and retention costed separately if added |
| Data transfer | Example 2 GiB internet egress/month, cross-AZ traffic estimated separately | ALB processed volume and internet egress are different billing items; avoid double counting or omission |
| Public IPv4 | ALB in two AZs, first assume 2 addresses all year; read back the actual allocation at the end | The two private EC2 hosts have no public address; the old EC2 and build resources are listed separately if kept |
| Network endpoints | Existing S3/DynamoDB gateways; no NAT or charged interface endpoints | Do not invent quantities for undeployed NAT or interface endpoints; recalculate if the architecture changes |

Monthly request volume is a workload assumption, not measured traffic. 8760 hours is a 365-day annual scenario; if the calculator uses 730 hours/month, 12 months is also 8760. Region, public IPs, taxes, free tier, transfer direction and billing units must be checked item by item in the final Calculator.

## Steps to complete T18

1. A provides the final resource list, instance running policy, retained disks/snapshots, actual monitoring and encryption configuration; B provides the read/write pattern and the Scan cost of each page load.
2. Use the [AWS Pricing Calculator](https://calculator.aws/#/estimate) to create the us-east-1 scenario above; keep the price date, input screenshots, a shareable estimate link/export record and a note on applicable discounts. The calculator does not require creating actual AWS resources.
3. Base annual cost is steady monthly cost × 12 plus one-off costs; separate lab-period running hours from the full-year service scenario. Compare sensitivity with request volumes at 0.1× and 10× the base, without multiplying all fixed costs by 10.
4. Output a PDF strictly under 2 pages (conservatively 1 page) with service subtotals, the 12-month total, key assumptions, items not costed and the trade-off between cost and resilience. There are currently no prices or total, so this is not the final estimate.

Lab budget strategy: agree a short joint evidence window with A and, after checks end, handle resources according to the course's retention requirements. Stopping EC2 does not stop ALB, EBS or snapshot charges; do not automatically delete resources while the requirement is unconfirmed.

Reference: [Getting started with AWS Pricing Calculator](https://docs.aws.amazon.com/pricing-calculator/latest/userguide/getting-started.html). All capacities/traffic above are draft project assumptions.
