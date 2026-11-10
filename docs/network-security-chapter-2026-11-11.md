# Network and security section / 网络与安全说明

11 November2026 Sydney. A / DiegoXue-coder, AI-assisted drafting from dated10Nov evidence. No new AWS configuration or policy attachment performed. See [architecture PDF](../output/pdf/reading-tracker-architecture.pdf) and [review checklist](architecture-review-2026-11-11.md).

## Report-ready English technical explanation

The VPC separates the publicly reachable load balancer from application hosts. Public subnet route tables have an internet-gateway default route. Private application route tables contain local routes and S3/DynamoDB gateway-endpoint routes, without a NAT gateway or internet default route. This avoids a general internet egress path and the cost of NAT, but prevents downloading packages directly onto the private hosts. A prepared runtime image and a pinned private S3 release archive therefore provide a reproducible deployment path. Additional dependencies require a new reviewed image or deployment process rather than opening unrestricted egress.

The ALB security group accepts TCP80 from internet clients and sends TCP8000 only to the application security group. Application ingress8000 accepts only that ALB security group, and egress443 targets the managed S3 and DynamoDB prefix lists. The application hosts have no public IPv4 or SSH ingress. The SDK performs authenticated HTTPS calls through the gateway routes. S3 access on that route is restricted to project release downloads; DynamoDB access is restricted to required operations on the project table. These are network-path and endpoint-policy controls, not proof that the supplied LabRole has only those permissions.

EC2 uses LabInstanceProfile and temporary role credentials discovered by boto3; metadata requires IMDSv2. No shared member AWS passwords or static application access keys are needed. AWS recommends temporary workload credentials and permissions limited to the necessary actions/resources [1]. In this Lab the supplied role remains broader than the application requires. A separate application permission proposal is provided for analysis, not attached to the role. Simply adding a narrower Allow policy to a role that retains broader Allow policies would not remove those existing permissions; effective access must be evaluated across applicable policies [3].

The two EBS root volumes are encrypted gp3. The artifact bucket has SSE-S3 encryption, public-access blocks and transport restrictions; DynamoDB is the managed durable business store. These protections do not encrypt every request path: browser-to-ALB HTTP80 and ALB-to-application HTTP8000 remain cleartext. On10November ACM returned no certificates, Route53 no hosted zones, and CloudFront listing was denied. There is no verified HTTPS solution yet, and the diagram/report preserve that gap. The application also lacks authentication and CSRF protection, so only fictional demonstration records are permitted. This is not described as a production-secure service.

## Proposed application permissions - NOT ATTACHED

File: [proposed-app-permissions-not-attached.json](../deployment/policies/proposed-app-permissions-not-attached.json). It is a JSON permissions-policy proposal, not a role/trust policy or a tool that changes IAM. No user, role, identity permission or endpoint rule was changed.

| Proposed permission | Concrete reason / trade-off |
| --- | --- |
| DynamoDB PutItem | Create validated fictional records; app conditional write prevents replacing an existing generated record key |
| Scan | Current paginated library page/statistics; full-table read grows with data size, so not an efficient large-library design |
| GetItem /DescribeTable | Existing verification/provisioning checks on this single table; can be removed from a separately isolated production serving identity if checks are separated |
| S3 GetObject on one exact archive | Current bootstrap downloads only release06c2292; changing release requires reviewing/updating this scope |
| SecureTransport=true | Allow statements are conditioned on TLS for AWS API calls; this is not browser HTTPS |

The proposal does not allow DeleteItem, table administration, S3 uploads/listing, IAM changes, instance management or CloudWatch log publishing. Native service metrics are provided without adding a host agent. Identity permissions support resource-scoped DynamoDB statements [2]. Actual effective access would still depend on other identity policies, boundaries, resource/endpoint policies and the role's permitted trust relationship. In particular, the current endpoint policies name LabRole: substituting a different role later would require separately reviewing that condition.

Before any real attachment elsewhere, an authorized administrator must review the effective policy set and validate actual allowed and denied operations. No IAM Policy Simulator/Access Analyzer or AWS deny-operation test was run for this draft. Local JSON/static checks are not an effective-permission test. Do not count this proposal as a tested enhancement or as resolution of the broader LabRole limitation.

## 中文速读

- 外面只能访问负载均衡器；两台应用机不直接暴露公网。
- 两台应用机使用同一个数据库，S3只负责保存部署包。
- 应用访问AWS数据服务时用HTTPS，但用户访问网站、负载均衡到应用目前还是HTTP，需要继续解决。
- 已写好“正常情况下应用真正需要哪些权限”的草案，但没有修改课程LabRole，也没有冒充已经实现最小权限。
- 不增加资源、不部署自动扩容；组员可以直接用现有资料审阅这一章。

References: [1] [AWS IAM security best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html); [2] [DynamoDB IAM integration](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/security_iam_service-with-iam.html); [3] [IAM policy evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html), accessed11November2026Sydney. Actual project controls are supported by `evidence/T05/2026-11-10-A-network-security.log` and `evidence/T15/2026-11-10-A-next-preflight.log`.
