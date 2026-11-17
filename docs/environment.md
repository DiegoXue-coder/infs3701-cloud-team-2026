# Environment and resource record (no secrets)

> Latest actual progress (2026-11-01): the new two-host ALB foundation has been created; the business application and HTTPS are not yet complete; the older records below are kept by date. Read [this round's verification and three-person handoff](2026-11-01-foundation-verification.md) and project/aws-resources.json first.


Region: console showed us-east-1 on 2026-10-31; final deployment region to be confirmed, the formal cost requires us-east-1
Lab holder: DiegoXue-coder (the user has designated himself responsible for AWS). The current Lab prohibits creating users/groups, so the approved holder executes; a separate multi-user entry from teaching staff awaits confirmation.
Single entry point: to be deployed
Currently deployed code commit: to be deployed
Application port/start method/health path: to be confirmed
HTTPS/certificate approach and verification: to be confirmed
Application data tier and access path: to be confirmed
Instance role permitted for use: the Readme pre-provisions LabRole / LabInstanceProfile; whether specific instances have it attached has not been checked.

| Resource | Purpose | AZ/subnet | Non-sensitive identifier | Owner | Created/changed | Delete/keep arrangement |
| --- | --- | --- | --- | --- | --- | --- |

| Date | Balance before experiment | Balance after experiment | Running time | Running resources and notes | Recorded by |
| --- | --- | --- | --- | --- | --- |

Do not record access keys, session tokens, passwords or the contents of credential files.

Budget screen during the read-only check on 2026-10-31: $1.20 / $50 used, showing about $48.80 remaining (with an update delay; not a measurement of deployment cost).

## 2026-11-01 inventory update

See [this inventory](2026-11-01-aws-inventory.md). The old instance is running but the web connection is refused; no role attached, SSH open to the whole internet and the 8 GiB system disk unencrypted, none of which was changed. The old S3 books/ is still there, contents not read. The Lab shows $1.30/$50 used. The official service entry point/database/deployed version are still unconfirmed.

### Role-binding progress

On 2026-11-01 the user himself completed the LabInstanceProfile binding; the AI actually checked IAM role=LabRole in the instance details and saved the role-bound screenshot. This only proves the binding is done, not that the database is accessible. Session Manager shows Not connected for now; the credential error shown is timed before this binding and cannot be used to conclude that the binding failed. The EC2 Instance Connect browser connection page is prepared; login, running commands and fixing the old web page have not yet been verified.

### Old website restored successfully (later status)

On 2026-11-01 the user verified in EC2 Instance Connect that the role credential source is iam-role, and manually started the old app.py in a way that excludes static credential files/variables. The AI independently visited the old public HTTP address and the page showed 3 existing records; a terminal GET / returned 200. The earlier "connection refused" is superseded by this successful access, and the historical inventory is kept. This is currently only a foreground Flask+S3 single-instance baseline, with writes, keep-alive across restart and the final architecture unverified, and cannot be treated as the group's final service. Evidence: evidence/T05/2026-11-01-legacy-recovery.log.

## New foundation resources created

On 2026-11-01 the new VPC with four subnets, the ACTIVE DynamoDB table and the private encrypted deployment bucket were actually created; exact resources and verification limits are in project/aws-resources.json and docs/aws-owner-handoff.md. The new private instances/load balancer are not yet created; the official BASE_URL is still not provided. The old instance's SSM is now Online and its LabRole test read of the new table passed, which cannot be written up as connectivity from the new private subnets having passed.
