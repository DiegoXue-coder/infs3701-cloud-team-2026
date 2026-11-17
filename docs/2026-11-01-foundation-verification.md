# This round's infrastructure and three-person handoff

This is environment work actually performed by A (DiegoXue-coder) and cannot be counted as B/C's contribution or review. Live state must be checked in AWS; this document and the GitHub dashboard are time-stamped records.

## What can be used now

- Region us-east-1; the new VPC spans us-east-1a/b. Two private t3.micro hosts each use an 8 GiB encrypted gp3 volume, have LabInstanceProfile attached, no public IP, and IMDSv2 required.
- Foundation test entry point: <http://infs3701-team-alb-788523332.us-east-1.elb.amazonaws.com/>. The page clearly states that the business application is not yet deployed. `/health` returns the instance identifier; the response header is X-App-Instance.
- DynamoDB: infs3701-team-books, primary key record_id:String; region and table name are configured through AWS_DEFAULT_REGION and READING_TABLE. Old S3 records were not migrated.
- Private release bucket: infs3701-team-artifacts-214018170594. All four public-access blocks, AES256 encryption at rest, and non-HTTPS denied.
- The two private route tables each have S3/DynamoDB gateway routes, with no public default route or NAT. The endpoint policies allow only LabRole to access the named project resources over HTTPS; host outbound 443 goes only to the two service prefix lists. DynamoDB currently allows DescribeTable, Scan, GetItem and PutItem; DeleteItem/UpdateItem are not allowed. B must not assume arbitrary database operations are approved; submit a specific request when extra operations are needed.
- The ALB exposes only HTTP 80; back-end port 8000 accepts only the ALB security group. LabRole is still broader than actually needed, so this cannot be described as full least privilege.
- Python3.11.18 / Flask / boto3 / Gunicorn are pre-installed in the encrypted image, and systemd manages the application. Exact dependencies are in deployment/runtime-requirements.lock.

First real routing sample: 12 requests all returned 200, 6 each from az-a/b, see evidence/T09/2026-11-01-live-routing.log. This short sample does not prove long-term availability, business functionality or a passed whole-AZ failure.

## Actual limitations of the operations approach

The EC2 Instance Connect Endpoint was created, but an actual connection with the student identity received an ec2-instance-connect:OpenTunnel permission denial. DryRun can only check the creation request and does not show that connection works. IAM was not changed to get around the denial, and no chargeable SSM interface endpoints were added.

The alternative has actually passed on both new hosts: using only the holder's existing EC2 management capability, stop one host at a time, update user-data, start it, read the console output, and confirm health before handling the other. Both hosts showed BOOT_CHECK_OK, credential source iam-role, DynamoDB ACTIVE/record count 0, matching S3 object hash and normal local health; both were then healthy. deployment/maintain-foundation.py checks the account, VPC, host ID and the other host's health, and backs up the original user-data; it is not a general-purpose executor for arbitrary hosts.

After verification, inbound 22 on the new application security group and outbound 22 on the unused EIC security group were closed. The EIC resource is kept and cannot be used as a working login channel; nothing was permanently deleted.

The script registers an every-boot check using MIME `text/x-shellscript-per-boot`. Ordinary shell user-data, which by default runs only once, must not be treated as a repeat-deployment mechanism. It currently checks the role credential source, DynamoDB Describe/Scan, the hash of a fixed S3 test object and local health; it writes no business data and does not install B's business release package.

References: [EC2 user-data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html), [cloud-init MIME and per-boot scripts](https://docs.cloud-init.io/en/latest/explanation/format/mime.html). Actual results are those in the maintenance verification log; the documented pattern by itself is not a successful test.

When A repeats the foundation check: in a CloudShell signed in to this account, save the reviewed maintain-foundation.py and first run `python3 maintain-foundation.py --instance a --phase prepare`; once EC2 shows stopped, run `--phase start` with the same parameters. Then run `--phase inspect` and confirm BOOT_CHECK_OK and a healthy target before repeating the three steps for b. Never prepare both hosts at once; do not use it on the old instance; this set of commands does not release new business code.

## Monitoring baseline

Dashboard: infs3701-team-dashboard, 6 widgets, covering healthy targets, requests/5xx, p95 response time, CPU of both instances, database read/write capacity and a limitations note.

Alarm: infs3701-team-healthy-targets-below-two. Two dimensions (ALB + TargetGroup), Minimum of HealthyHostCount, 60-second period, 2 consecutive points below 2, missing data treated as not breaching. It means two-host redundancy has dropped and must not be read as a full service outage; there is no SNS/email recipient, so it cannot be claimed that a person was notified. The missing-data treatment hides some no-data situations; C should review it and add availability monitoring.

For the single-host stop, requests and real state changes see evidence/T09/2026-11-01-maintenance-validation.log: at 05:56:06 UTC the alarm really changed to ALARM (read at 05:56:15), based on healthy count 1 at 05:52/05:53 UTC; after both hosts recovered, an actual ALARM→OK occurred at 06:00:06 UTC, based on real data points with healthy count 2; the full history is in final-readback.log. SetAlarmState was not used to fake a trigger. C still needs to independently check the metric, threshold, business functionality and the final application's failure behaviour.

The original log keeps one summary error from the sampling script: the short single-host sample actually has 6 REQUEST lines and an instance count of 6, while the summary field requests still prints a hard-coded 12; the real number, by individual records, is 6. A later continuous sample has another 25 single-host 200 responses. The sampling script now uses one variable for the request count. The first two-host record of 12 requests, 6 each, is not affected by this error; these samples do not cover the whole stop/start moment, so zero-downtime switchover cannot be claimed from them.

## B can start today without waiting for A

1. Accept the private-repository invitation, authenticate with your own GitHub as described in docs/self-service.md and join B; read AGENTS.md and claim T04/T07.
2. The original code is in app/reading_tracker.py and the original snapshot in reference/reading_tracker_candidate.py. First provide a local mode that needs no AWS identity, then implement the DynamoDB adapter; do not ask A for credentials.
3. Contract: port 8000, WSGI `app:app`, `/health`, APP_INSTANCE maps to X-App-Instance. The environment is Python3.11, with READING_TABLE and AWS_DEFAULT_REGION as above.
4. Deliver the exact commit, app.py entry point, requirements, templates/modules, sample inputs and outputs, local test records, database fields and known issues. New dependencies must be explained first; private instances cannot pip install directly from the public internet.
5. Report the delivery receipt on T07. A prepares the real release steps/package from this version, deploys and records the cloud results; the current maintenance check script cannot be used directly as a business releaser. After B's code is delivered, cloud deployment still needs one operation window from A.

## C can start today without waiting for B

1. Accept the invitation, join C through the self-service entry, claim T08, and read the materials and old code.
2. First deliver a fictional data set, expected statistics/input boundaries, an executable request tool and real local logs, with a configurable BASE_URL.
3. The test entry point above can be used to check response time, instance identifier and tool format; it must be marked infrastructure-only, and a 200 from the test page does not count as Reading Tracker functionality passing.
4. Review the existing dashboard/alarm configuration and propose improvements with threshold reasoning. A's actual configuration and records cannot be counted as your own independent acceptance.
5. Prepare 12-month cost assumptions (including ALB, disks and image), plus report and video evidence scripts; the real joint business test takes place after B/A release.

## The three windows where you will need to cooperate later

| Window | What teammates hand over first | What A does | Who continues afterwards |
| --- | --- | --- | --- |
| First business release | B's exact version, release package and local tests | Review dependencies, release host by host, record version/parameters/health results | C independently verifies the real business, B fixes failures |
| Joint test | C's request script, monitoring parameters and recovery steps | Stop/start one host, recover, help collect evidence | C records requests/alarm/recovery, B checks the shared data |
| Final review | Each of the three members' chapters, cost and evidence | Check real resources against the diagram, provide an operation demo | Another account reviews the delivery, all three confirm the submission |

Always pull/start first and read the latest Issue. B/C give parameters and steps in the task receipt and A handles them in a batch; there is no background bot that runs AWS automatically, and there is no guarantee that cloud requests are carried out immediately while A is offline.

## Not yet done, must not be skipped

New Reading Tracker business release, real managed-database write/read, business failure and shared-data tests, HTTPS, the auto-scaling/enhancement decision, the complete cost/report/architecture diagram/video, and independent cross-review.

The brief requires encryption in transit, provides no domain and does not require buying one. There is currently no known manageable domain, ACM certificate or Route53 hosted zone; the certificate/domain approach accepted by the course needs to be confirmed with the tutor. No message was sent to teaching staff, no domain was bought and no browser certificate warning was bypassed.

The build instance is stopped. The two running application instances, the ALB, EBS, AMI snapshot and monitoring may keep consuming credit; no resources were permanently deleted this round. The delayed reading on the Lab budget screen must not be treated as this session's spend or as the 12-month cost. When testing ends later, schedule shutdown and cleanup according to the course's resource-retention requirements.

Final configuration verification time: 2026-11-01T06:01:13.014386+00:00. For the 48 offline tests see foundation-maintenance-offline-tests.log; offline passes do not replace cloud evidence. The maintenance tool's restore-userdata only restores the EC2 metadata field; it cannot remove a cached per-boot script and is not a business-version rollback tool.
