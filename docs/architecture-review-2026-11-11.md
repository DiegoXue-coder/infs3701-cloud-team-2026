# Architecture review / 架构图交接

Prepared 11 November 2026, Sydney, by A / DiegoXue-coder with Codex. Based on **10 November AWS evidence**, not a new live AWS inspection. T17 partial preparation; T15 and independent technical review are not complete.

## Files / 文件

- [One-page architecture PDF](../output/pdf/reading-tracker-architecture.pdf): A3 landscape, English labels, official AWS symbols; submission candidate pending HTTPS resolution and independent review.
- [PNG preview](../output/pdf/reading-tracker-architecture.png): viewable in GitHub and usable as a report/video figure; use the PDF for the diagram deliverable.
- [Editable generator](../scripts/build_architecture_pdf.py) and [icon provenance](../assets/aws/manifest.json): future AI can edit labels/layout and regenerate. No paid design account required. Run from repository root with Python/reportlab, then render using Poppler. Do not change labels without checking deployment evidence.
- [Security/network explanation and unimplemented permission proposal](network-security-chapter-2026-11-11.md).

## How to read it / 怎么看

1. Browser -> internet gateway -> one logical ALB enabled in the two public subnets, on **HTTP80**.
2. ALB -> either private EC2/Gunicorn host on **HTTP8000**. Each EC2 has its own encrypted8GiB gp3 EBS root volume.
3. Each application uses shared DynamoDB through the gateway route; S3 holds deployment archives, not book records. These AWS API paths use **HTTPS443**. Responses return along the request connection; arrows are logical request/dependency direction, not one-way network rules.
4. CloudWatch shows native ALB/EC2/DynamoDB metrics and the redundancy-loss alarm. The dashed telemetry line is logical and does not assert a new private-host network connection or agent.

DynamoDB and S3 are regional managed services outside the VPC drawing, not additional EC2 servers or databases installed in a subnet. The two gateway endpoint paths are route-table integrations, not endpoint instances. AWS's internal replicas are not drawn as group-owned servers.

## Trace the drawing to real evidence / 对照依据

| Figure element | Evidence / exact mapping |
| --- | --- |
| VPC /4subnets | `project/aws-resources.json` and dated network export: VPC10.37.0.0/16; public10.37.0.0/24,10.37.1.0/24; private10.37.10.0/24,10.37.11.0/24 |
| AZs /hosts | us-east-1a: i-00572a14ca8b71156 /10.37.10.88; us-east-1b: i-0081259c52a32e051 /10.37.11.110 |
| EBS | `evidence/T05/2026-11-10-A-network-security.log`: vol-0befb64658670f366, vol-0627d63a4f014f2b4;8GiB encrypted gp3 |
| ALB /target | `infs3701-team-alb`, `infs3701-team-tg`; actual listenerHTTP80 -> targetHTTP8000; /health |
| Security groups | ALB sg-00ebc11a2282074f6, app sg-0a3ae03837c952009; actual source-group/port restrictions in dated export |
| Gateways | IGW igw-0a4f8f537ed7f4663; S3 vpce-0edea5c7a05bc729d, DDB vpce-028353eb0e050df0a; private routes have no internet default |
| Business/data | `docs/business-handoff-2026-11-07.md`,10Nov restoration; release06c2292, table infs3701-team-books, original2fictional records retained |
| Metrics /alarm | `docs/monitoring-reconciliation-2026-11-10.md`; genuine business alarm history, not manual state injection; no notification destination |

The unused maintenance endpoint, stopped runtime builder/AMI pipeline and unrelated cafe/old individual resources are off the operational request path. They remain inventoried separately. Diagram omission is not proof of deletion; retained project disks/snapshots remain relevant to costs.

## B/C independent review checklist / 给组员复核

- Compare AZ, subnet CIDR, instance IDs, EBS and exact ports with evidence, rather than only checking appearance.
- Confirm S3 is described as artifacts and DynamoDB as shared business data; do not claim old S3 record migration.
- Confirm native metrics do not imply a CloudWatch agent/egress rule; empty alarm actions mean no emailed notification.
- Confirm the caption dates evidence to10Nov, states whole-AZ failure was not tested and shows HTTP honestly.
- Automatic scaling is **deferred by owner**, not approved or deployed. JSON/bootstrap preparation from10Nov is historical preparation only. Do not execute it on the basis of this diagram.
- After a real HTTPS change, update the actual listener, SG, certificate and request-flow labels together, rerender, and review again.

Review via another member's own account. A cannot independently approve A's file. T17 remains partial until its dependencies and real review are satisfied.

## Suggested report caption

Figure 1. Reading Tracker deployment in us-east-1, based on configuration evidence collected10November2026. A logical ALB spans two public subnets and distributes requests to two private EC2 hosts; business state resides in DynamoDB and deployment artifacts in S3. HTTP client/application links remain unencrypted, while AWS API paths use HTTPS. Native service telemetry is shown as a logical dependency. Automatic scaling has been deferred. This figure is a review candidate, not proof of current online health.
