# Security audit and bounded scaling proposal / 安全核对与扩容准备

Prepared by A / DiegoXue-coder on 10 November. **Partial; not final security acceptance. No new AWS resources or access were created in this preparation.**

## What was actually checked

The earlier same-day [network export](../evidence/T05/2026-11-10-A-network-security.log) confirms:

| Check | Observed | Meaning / limitation |
| --- | --- | --- |
| Public entrance | ALB TCP80 from internet; outbound8000 only to app SG | HTTP remains unencrypted |
| App entrance | TCP8000 only from ALB SG; no SSH rule | Two private hosts; not directly internet accessible |
| App egress/routes | TCP443 to S3/DynamoDB prefix lists; no private default internet route | No general package-download access; use prepared AMI |
| Instance identity | LabInstanceProfile, IMDSv2 required; runtime uses iam-role | LabRole is broad; endpoint restrictions do not make the entire role least-privilege |
| Disk | Both roots encrypted gp3,8GiB | Encryption at rest observed; not a restore test |
| Artifacts | All S3 public blocks; AES256; release path/role/TLS restricted endpoint | Private deployment artifacts, not public course materials |
| Database endpoint | DescribeTable/GetItem/PutItem/Scan, only project table and LabRole, TLS required | App-to-AWS HTTPS; does not encrypt browser→ALB or ALB→app |
| App access | Fictional-data list/add demo without login | Never upload personal reading data; no production authentication/CSRF claim |

The [new read-only preflight](../evidence/T15/2026-11-10-A-next-preflight.log), timestamp **2026-11-10T10:29:56.906403Z**, found:

- ASG list empty; ACM certificate list empty; Route53 hosted-zone list empty. Absence of hosted zones does not prove the user owns no domain elsewhere.
- `GetRole(AWSServiceRoleForAutoScaling)` returned `NoSuchEntity`. It does **not** prove creation is forbidden: service-linked-role creation permission is still unverified. Do not create a custom IAM workaround.
- `cloudfront:ListDistributions` returned `AccessDenied` because no identity-based allow. No CloudFront mutation was attempted; do not report CreateDistribution as tested/denied.
- Seven running/pending EC2 instances were listed. Lab Readme supports at most9 concurrent instances; other coursework consumes quota too. Builder remained stopped in this inventory.
- Existing runtime AMI available, x86_64, root `/dev/xvda`,8GiB encrypted gp3. No new image or machine created.

## HTTPS decision that remains

An ALB HTTPS listener needs a certificate. The assignment does not supply a usable domain. We have not established user-controlled DNS or a course certificate. Do not buy a domain or request a certificate for an AWS-owned ALB hostname.

CloudFront's default hostname can supply viewer HTTPS, but current listing permission is denied and HTTPS only to CloudFront would still leave an HTTP origin segment. It cannot honestly close the entire in-transit-encryption gap. No self-signed-warning bypass, unapproved tunnel or public proxy will be used.

**Owner/tutor question, drafted only, not sent:**

> Our Learner Lab deployment has two private EC2 instances behind an HTTP ALB and a managed DynamoDB table. ACM has no certificates, Route53 has no hosted zones, and CloudFront listing is denied. Does the course provide a DNS name/certificate or an approved no-owned-domain HTTPS approach? Please also clarify whether automatic scaling is required by the rubric, since the brief calls it Going Further. We will describe HTTP accurately until this is resolved.

## Prepared scaling option: existing2 + elastic0–1

`deployment/prepare-surge.py` builds a local proposal and user data, **without AWS calls**. Existing hosts are not attached to the ASG and will not become scale-in candidates. A separate private group would have min0/desired0/max1 and join the existing target group when launched. Total project capacity would be2–3. This is demand expansion, **not automatic replacement of the two original hosts**.

Reviewable generated files: [proposal JSON](../project/surge-proposal.json) and [startup script](../deployment/surge-user-data.sh). Final [offline build](../evidence/T15/2026-11-10-A-offline-surge-final.log) and [integrity check](../evidence/T15/2026-11-10-A-proposal-integrity-final.log) passed. An earlier byte-comparison check failed because Windows text writing changed LF to CRLF; the builder now writes script bytes and the final check verifies exact equality with launch-template user data. The failed dated log is retained. These checks do not replace a real launch or demand-scaling test.

The new host would reuse the verified runtime AMI, pinned06c2292 archive/hash, existing app SG, private subnets,8GiB encrypted gp3, IMDSv2 and LabInstanceProfile. A unique `asg-i-...` response label would be derived locally through IMDSv2. Existing deployment scripts/labels remain unchanged. New user data is compiled locally but has not booted on AWS.

Proposed alarms: ALB RequestCount Sum >60/min for2 consecutive periods adds1; <=10/min for5 periods removes1, cooldown300s, missing data notBreaching. No traffic means scale-in may need observed low-volume requests rather than absent datapoints. These are demonstration thresholds, not a measured production sizing recommendation. Snapshot the exact launch-template numeric version and create policy/alarms only after permission checks and approval.

Before execution: refresh quota/credit, verify service-linked-role creation and PassRole/ASG/launch-template permissions, obtain action-time approval for the additional LabRole host and automatic termination, then set up the initially empty group. Preserve current raw logs before any termination. LabRole permissions cannot be narrowed by inventing unsupported IAM changes.

Keep maintenance replacement terminate-first (`MinHealthyPercentage=0`, `MaxHealthyPercentage=100`); suspend `AZRebalance` and `InstanceRefresh` while the group is empty, before enabling alarm actions. This avoids intentionally using a second temporary host above the approved one-host surge bound. Any later change to these controls requires re-review. No permissions were tested through a mutation.

Test plan: C samples health/homepage before/during/after; A runs bounded GET-only load at no more than2 requests/second for at most4 minutes, stopping on repeated errors. Record the real alarm/policy event, third target healthy, third unique response label and shared existing records. Stop load; make occasional low-volume samples until observed scale-in. Capture new-host logs first; scale-in permanently deletes its root disk. Verify original2 IDs and database records remain. Do not call a manual desired-capacity change automatic demand scaling. No test is yet passed.

Rollback plan: disable new alarm actions/policies; remove the surge target from service, preserve diagnostics, and only terminate the specifically approved surge instance. Original2/TG/table/SG stay. No automatic deletion of original hosts, AMI, S3 releases or database. An error or permission denial stops this rollout and is reported; no broadened permission workaround.

## Work that can proceed now

- B: retry independent current business checks; review network/protocol claims and app/data chapter. No AWS credentials needed to review exported evidence.
- C: reconcile genuine Nov7 alarm history with exported metrics, finalize cost assumptions using current two-host design; keep proposed third-host cost separate until deployed. Coordinate new live sampling only after A reports a real deployment.
- A: resolve approved HTTPS approach and ASG permission gate; prepare final diagram from actual deployed configuration.
- D, if available: review English report/prepare video from current evidence; do not wait for a proposed enhancement to draft.

Official references: [ALB HTTPS certificate prerequisite](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html), [CloudFront viewer HTTPS and separate origin encryption](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-https-viewers-to-cloudfront.html), [ASG scale-in protection limits](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-instance-protection.html). These describe mechanisms; actual Lab authorization is evidenced separately above.
