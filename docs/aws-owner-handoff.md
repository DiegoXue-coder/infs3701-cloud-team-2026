# You finish the AWS foundation first; how teammates take over

> Latest actual progress (2026-11-01): the new two-host ALB foundation has been created; the business application and HTTPS are not yet complete; the older records below are kept by date. Read [this round's verification and three-person handoff](2026-11-01-foundation-verification.md) and project/aws-resources.json first.


2026-11-01, A=DiegoXue-coder. The live resource inventory is in project/aws-resources.json; the next batch of deployment plans not yet executed is in project/next-deployment.json. What follows strictly separates what was created from what is planned; the placeholder health page must not be treated as Reading Tracker.

## Actually completed

- VPC vpc-0836d003a70f93405, 10.37.0.0/16, four subnets across us-east-1a/b. Actual API checks confirmed that the two public subnets share the IGW default route and that neither private subnet has a public default route, plus the automatic main route table; four route tables in total.
- DynamoDB table infs3701-team-books is ACTIVE, primary key record_id (String), on-demand billing, with read and write throughput caps of 10 each. The existing instance's LabRole was shown by a real SSM command to be able to DescribeTable and Scan, and the table was empty at the time; no old books were written or migrated.
- The new deployment-package bucket infs3701-team-artifacts-214018170594 was created, with all four public-access blocks on, AES256 encryption and a policy denying non-HTTPS requests; the old reading-records bucket was left completely untouched.
- Temporary build instance i-030acdefe159caa87: t3.micro, 8 GiB encrypted gp3, no IAM role, no inbound rules; Python3.11, Flask, boto3 and Gunicorn installed, with the success marker appearing in the console log. Runtime image ami-03616f6b53c85f036 was created and verified as available and encrypted; the build instance is stopped, and the disk/image are still kept.
- The old instance/old website are kept; its credential files and user data were not copied into the image. The new image contains only the runtime environment and a health placeholder application clearly labelled infrastructure-only; running the service under systemd/Gunicorn is prepared but not yet verified on the new private instances.

## Why the database was chosen this way

Reading records are independent documents that need no multi-table joins or cross-table transactions; the current small-scale demo can locate items by record_id and compute statistics in the application. DynamoDB's managed multi-AZ resilience matches the managed-NoSQL route the brief explicitly allows; no database instance has to be maintained. On-demand billing suits intermittent course testing; "RDS is too expensive" is not used as an unsupported conclusion.

Trade-offs: complex joins/SQL queries are inconvenient; Scan cost and latency rise as data grows, so B must paginate and control data volume; the 10/10 cap protects the budget but also limits load testing, so C should first collect evidence with functional/failure tests below 1 request per second and review the budget before raising the cap. The database's built-in scaling is not implemented application auto scaling and does not automatically earn extra enhancement marks.

References: [DynamoDB official documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html), [billing modes](https://aws.amazon.com/dynamodb/pricing/).

## Next batch: prepared, not yet executed

- Two private t3.micro hosts, each with 8 GiB encrypted gp3, placed in the two private subnets with no public IP; they need the course-provisioned LabInstanceProfile/LabRole attached.
- One public ALB, initially HTTP 80 only, with back-end port 8000 accepting only the ALB security group; HTTPS awaits a certificate approach.
- One EC2 Instance Connect Endpoint: SSH 22 accepts only that maintenance endpoint's security group, and SSH is not opened to the internet.
- S3/DynamoDB gateway endpoints, used only by the two private route tables; policies restrict LabRole to accessing this project's release-package prefix/database table over HTTPS. Private-instance outbound 443 is allowed only to the prefix lists of the two AWS services.
- No NAT; do not automatically add a continuously charged NAT or multiple interface endpoints. Dependencies are installed into a clean image in advance and the release package is fetched over the private S3 gateway path; operations go through the EC2 Instance Connect Endpoint, without assuming private instances can pip install directly from the internet.

Basis for the gateway endpoint path: [AWS DynamoDB Gateway endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-ddb.html). Basis for the maintenance security-group design: [EC2 Instance Connect Endpoint security groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/eice-security-groups.html). These are design references, not measured results on the new private instances.

Granting LabRole to new instances and opening a public entry point are new access configuration and need confirmation at execution time. LabRole is broader than the application actually needs, and the Lab does not let us create a narrower role/policy; deployment/policies/recommended-app-role-NOT-ATTACHED.json is only a recommended policy and is not claimed to be attached. The gateway policies have not been applied yet either.

## What B can do right now

Continue from T04/T07. The database resource has already been created by A; B does not need AWS credentials, another database or to wait for a new selection. The configuration contract is READING_TABLE=infs3701-team-books, AWS_DEFAULT_REGION=us-east-1, and record_id is a UUID string.

The later deployment package contains app.py (WSGI app:app), requirements.txt and the required modules/templates; the source can stay in app/reading_tracker.py with app.py as the import entry point. APP_PORT=8000, the /health and X-App-Instance conventions are kept, and the instance identifier is taken from APP_INSTANCE. Target runtime is Python3.11. Continue with Flask+boto3 by default; state new dependencies in requirements and the delivery first so that A can prepare the image or offline dependencies, and do not install over the network ad hoc on private hosts.

B delivers the local mode, DynamoDB adapter, input constraints, pagination/statistics logic, sample requests, actual tests and a clear release package. A then applies the exact commit and verifies the real cloud identity; when B's personal AI has no AWS permission, B cannot claim cloud read/write passed.

## What C can do right now

First do T08's executable tests and fictional data set, and review B's local version. Design the check steps for shared data, routing, failure, alarm and security. When the new ALB/instances are not created or only show the placeholder page, do not report the business as passing.

For monitoring, prefer native ELB/EC2 metrics; first deliver a draft dashboard/alarm configuration, metric dimensions, threshold reasoning and trigger/recovery steps, without requiring A to design them on the spot. An availability alarm for "fewer than two healthy targets" can be considered, but the actual threshold and period must be explained and verified; do not rely on undeployed log agents or custom metrics to prove success. Cost must include the actual new resources, image/disks/ALB and running hours, not only EC2.

## What you will still need to cooperate on later

| When | What you actually do | What teammates prepare in advance |
| --- | --- | --- |
| B's first runnable version | Deploy both hosts from the specified version and fill in real parameters | B's release package, dependencies, startup, configuration and known issues |
| C's monitoring plan complete | Apply the dashboard/alarm configuration | C's specific parameters/scripts and test method |
| Joint failure test | Stop/start the specified new instance as agreed and recover | C keeps a continuous request record, B checks the application and data |
| Recording/delivery | Show the actual architecture, check your chapter and contribution | Each of the three writes their own reasons/steps, with cross-review |

So you can finish the infrastructure first, but you will not step away completely while B/C have yet to deliver. Combine small operations into short deployment windows and have teammates write precise requests first, to reduce repeated verbal replies from you.

## HTTPS awaiting confirmation

Page 2 of the brief requires encryption in transit and at rest, but issues no domain and does not require buying one. An actual check showed the current us-east-1 ACM certificate list and Route53 hosted zones are both empty; the user is unsure whether they own a domain. No domain was bought/registered, and no self-signed certificate was used to get around browser security warnings. Question to send to the tutor: when an individual Learner Lab has no known manageable domain, does the course provide a domain/certificate, or which HTTPS approach does it accept? This question has not actually been sent to the tutor and there is no answer.

## Additional pre-execution checks

Three EC2 DryRun calls returned DryRunOperation: launching a private instance with LabInstanceProfile, the DynamoDB gateway endpoint, and the EC2 Instance Connect Endpoint. These are permission/request pre-checks, not an actual deployment or a final test of network/endpoint policies. The next-batch script deployment/launch-foundation.py by default only prints an offline plan and does not connect to AWS; only --apply executes; --apply has not been run. Python3.11.18 was measured inside the runtime image, with versions recorded in deployment/runtime-requirements.lock.
