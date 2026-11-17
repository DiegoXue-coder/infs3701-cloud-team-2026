# 2026-11-01: today's inventory of your AWS environment

Status: T05 in progress; one round of real, read-only browser inventory is complete; this is not a successful deployment or final acceptance. Today's Lab was started, which restores existing instances; no new resources were created.

| Item | Actual result |
| --- | --- |
| Region and balance | us-east-1; shows $1.30/$50 used, about $48.70 left, with an update delay |
| Old EC2 | INFS3701-Week2-EC2 / i-0bdbde44eb450f334 / t3.micro / us-east-1a; running |
| Original network | VPC vpc-0524ecd6aeeb47b61; subnet-08fdfb8bd68d62433; routes not yet inventoried |
| Instance role | IAM role shows empty (—), not yet attached; IMDSv2 Required |
| Security group | INFS3701-Week2-web-sg / sg-0a2612289ccca5dce; 22 and 80 open to 0.0.0.0/0, outbound All |
| System disk | vol-0b3fe0452d4345c18; 8 GiB EBS, not encrypted |
| Scaling components | EC2 dashboard shows 0 load balancers and 0 Auto Scaling Groups; not the final architecture |
| Old web page | HTTP access at the time was refused; the application/listener/startup-configuration cause is not yet located |
| S3 | infs3701-reading-notes-inbox, us-east-1; books/, notes/ and version-test.txt are still there, contents not read |
| Availability Zones | The console lists us-east-1a to us-east-1f; actual deployment permission/capacity in a second AZ is not yet verified |

## Direct handoff to teammates

- B: continue developing from app/reading_tracker.py in the repository; local mode does not need this Lab's credentials. The old instance has no role configured and the web page is not restored, so do not treat it as a ready back end. Database read/write code and resource requirements are handed over in T04/T07; do not copy old session keys.
- C: there is currently no cloud BASE_URL that can be claimed as business-ready. Run the local tests and request tool first; add the role, SSH exposure and disk encryption items above to the security checks, and do not write a discovered problem up as already fixed.
- A (you): next, inventory the role/network path and the feasibility of the database and TLS, then prepare a minimal deployment configuration. Keep the old bucket and old instance for now; no Reset, no data deletion. Record each setting as it is corrected, and do not let the architecture diagram say HTTPS first.

## Still to do

Actual database resources and permissions, LabRole/instance profile, network routes, certificate/domain verification, deployment budget. No database/network/instance was created and no security group was changed today; T05 is not marked complete.

Real operation record: [browser-audit.log](../evidence/T05/2026-11-01-browser-audit.log). Screenshots are at evidence/T05/2026-11-01-*.png. The old public address changes each time the instance starts; do not record it as the official service entry point.
