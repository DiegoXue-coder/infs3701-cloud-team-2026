# Reading Tracker: scalable and highly available cloud service

**Working source, updated11 November 2026 Sydney. Not submission-ready.** Integrated by DiegoXue-coder with Codex under the owner's instruction not to wait for Tenzin. Application/data content adapts Alex's original `docs/b-design-report-draft.md`; test, cost and video material credits Marina's existing files. Tenzin has not been credited with this preparation. Technical owners must check their sections before PDF export.

## 1. Objective and scope

The project takes Option A: upgrade Diego's individual Reading Tracker into a shared, fault-tolerant course demonstration. A small study group can add fictional book records and revisit reading status, pages, ratings and summary statistics. The workload consists of occasional browser reads and small independent writes, with no relational joins or long-running background jobs. One shared demonstration library is implemented; private multi-user accounts are not.

The cloud objective is to retain the same authoritative data when different servers answer requests or one application host stops. A single local process cannot provide that separation of compute availability and retained data. The system therefore uses a common load-balanced entry, two application hosts in different Availability Zones and a managed shared database. The project deliberately retains the original business workflow so that infrastructure choices can be tested against a concrete application rather than an unrelated static page.

## 2. Architecture and request flow

The audited deployment is in us-east-1, within project VPC 10.37.0.0/16. The Application Load Balancer spans public subnets in us-east-1a and us-east-1b. Each AZ also has a private subnet containing one t3.micro application host and an 8 GiB encrypted gp3 root volume. Neither application host has a public IPv4 address. The public subnets route through the internet gateway; private route tables contain local and S3/DynamoDB gateway-endpoint routes without an internet default route. Gateway endpoints support these AWS service paths without a NAT device [1].

A browser sends an HTTP request to the ALB, whose current listener is port 80. The target group forwards to port 8000 on the private hosts. Both run pinned release `06c2292cdf0aca80f050709b8172fac3595b54cc` using Python 3.11.18, Flask and two Gunicorn workers. A valid POST causes the receiving application to validate the form and conditionally create a DynamoDB item, then return302 to the library page. A subsequent GET reads the shared table, derives display statistics and renders the response. `X-App-Instance` identifies az-a or az-b for routing evidence. `/health` reports process stage and label, and deliberately does not test database operations.

A one-page architecture review candidate is now available at `output/pdf/reading-tracker-architecture.pdf`, with an editable generator and PNG preview. It includes EC2 root volumes, both AZ/subnet boundaries, gateway paths, DynamoDB, S3 release storage and monitoring. It labels the implemented HTTP paths truthfully and dates the configuration evidence to10November. Independent technical review and any later HTTPS-related revision are still required before freezing it for submission.

## 3. Application, compute and data choices

Alex's application/data implementation retains the original form, list and statistics. UUID string `record_id` is the table partition key. Records contain title, reading state, page counts, optional rating/note and creation time. Server-side checks reject invalid ranges and inconsistent page counts. Conditional PutItem protects a generated key from replacing an existing record. The explicit local-development mode uses an in-process list; deployed DynamoDB mode calls the shared table for authoritative reads and writes. Legacy S3 records were not migrated.

DynamoDB matches independent documents without joins and avoids running a database server for a small irregular workload. Strongly consistent table reads reflect successful earlier writes [2]. The implementation uses paginated, strongly consistent Scan and sorts/aggregates on the application host. This favours a simple, verifiable demonstration but costs more read work as the table grows; Scan is not a point-in-time snapshot across concurrent updates. For a larger library, bounded queries and a different aggregation approach would be necessary. A claim that another database is inherently too costly would require a comparable workload/cost analysis and is not made here.

EC2/Gunicorn preserves the existing Python application and gives direct control of the runtime, process configuration and release version. Its costs include patch/image maintenance, controlled rollout, health checks and recovery. Moving to Lambda would require changing packaging and invocation behaviour; it would not remove the need for durable shared storage. The choice is based on this application's continuity and the course demonstration, rather than an unrelated monitoring feature.

## 4. Scalability and availability

External state permits another correctly configured host to serve the same library. The ALB distributes traffic and checks target health before normal routing [3]. On7November, C observed thirty successful homepage samples, with fifteen responses per label. This is a routing result in that sample, not a guarantee of exact equal distribution or unlimited throughput. The current strongly consistent full-table read remains a data-access bottleneck that more application hosts do not remove.

**Unresolved core/rubric risk:** on 10 November the account had no Auto Scaling Group. The application is structured for horizontal expansion, but demand-driven capacity scaling has not been implemented or tested. The rubric's core checklist and brief's enhancement wording require clarification or an approved implementation. Fixed dual instances must not be presented as proof of automatic scaling.

The owner has deferred automatic scaling while completing core work and deliverables. The prepared surge configuration is an unexecuted proposal, not an implemented enhancement. This choice does not resolve the conflicting assessment wording or guarantee a particular mark.

For availability, A wrote one uniquely labelled fictional record through az-b and read it through both hosts. A then fully stopped the writer; az-a returned200 with the original record. After restarting az-b, both labels returned the same record, and a strongly consistent query verified that its original record_id remained. This supports shared-data retention and sampled service continuity under one host stop. It does not test loss of the entire AZ or measure every failure during transition. CloudWatch history subsequently retrieved on 10 November provides additional genuine evidence of redundancy loss and recovery during that business-stage operation.

## 5. Networking, security and deployment

Current security-group readback limits ALB ingress to HTTP 80 and ALB egress to application 8000. Application8000 ingress accepts only the ALB security group; application egress is443 to the managed S3 and DynamoDB prefix lists. SSH is closed. The unused maintenance endpoint security group has no ingress or egress. Instance metadata requires IMDSv2. Application AWS access uses the existing instance profile and dynamically obtained role credentials, rather than session keys stored in the application or a shared credentials file.

The S3 endpoint policy permits GetObject only under the project's releases prefix and the DynamoDB endpoint policy permits the required table operations only on the project table, both conditioned on HTTPS and the existing LabRole. These endpoint restrictions do not turn the broader supplied LabRole into a custom least-privilege identity policy. The Lab limitation and the difference between network-path restrictions and role permissions must be stated.

A proposed application permissions document scopes the required database actions to this table and S3 GetObject to the exact pinned release archive. It has not been attached or tested as effective IAM access. Adding a narrow Allow policy would not remove existing broader permissions; applicable policies must be evaluated together [5]. The separate security chapter explains deployment/verification permissions, release-update trade-offs and the review needed before changing any real identity.

The project roots are encrypted gp3 volumes; the artifact bucket uses AES256 encryption and all four public-access blocks. The current public listener remains HTTP 80, and no ACM certificate was returned by the 10 November audit. HTTPS therefore remains an implementation gap; no trusted-domain/certificate arrangement has been confirmed. The demo has no authentication or CSRF protection, and contains fictional records only. A final report cannot substitute reassuring prose for missing transport protection.

Deployments use a fixed two-file archive containing app.py and the observed runtime lock. The private S3 archive hash and source hash are verified before the existing service is restarted. Per-boot configuration preserves DynamoDB mode and distinct host labels across Lab restarts. The host script retains the previous application/environment and blocks blind retries after a failed switch. Rollback tooling has offline tests, but a live business rollback rehearsal has not been claimed. The role-based stop/update-user-data/start maintenance path reflects Lab access restrictions; no SSH permission bypass was used.

## 6. Monitoring and measured results

The CloudWatch dashboard contains healthy targets, request/error counts, target-response p95, basic instance CPU and DynamoDB read/write consumption. The redundancy alarm evaluates minimum HealthyHostCount below 2 over two 60-second periods. Its purpose is to detect loss of the spare application target, which can occur while the service still works. `notBreaching` for missing data and an empty AlarmActions list are limitations: an OK state alone does not establish current data freshness or an emailed notification. CloudWatch state and action semantics are documented separately [4].

AWS history shows the business-window alarm changing OK→ALARM at7 November 12:29:53.285UTC and ALARM→OK at12:30:53.284UTC. The evaluated healthy-target values were 1 at12:25/12:26 and 2 at12:27. These are real history records, not manually forced alarm states. The state timestamps lag the metric periods and even the application recovery observation, so the configured two periods must not be reported as an exactly two-minute end-to-end alert guarantee. C's independent review of this newly exported evidence is still pending.

During C's 12:42–12:45UTC window, HealthyHostCount minimum was2 in each minute and ALB RequestCount was12+23+2=37. C's full script made seven functional calls plus thirty routing samples, so the counts agree. Empty target/ALB5xx datapoint arrays are preserved as empty rather than replaced with invented zeros; the client sample separately recorded zero failures. C's response-header latency measurements and ALB target latency have different measurement scopes and should not be equated.

B recorded an HTTP503 preflight on 8 November and stopped before any POST. Its cause was not established at that time. On10November the Lab was found terminated; after starting it, A verified both healthy business hosts and both earlier fictional records. This recovery observation is consistent with session availability being important, but does not conclusively diagnose the earlier failure without contemporaneous control-plane evidence. A fresh independent B run is still required.

## 7. Cost, limitations and completion conditions

Marina's separate 12-month cost draft uses the AWS Pricing Calculator, us-east-1, continuous operation and explicit traffic/storage assumptions. It includes EC2/gp3, ALB, public IPv4, DynamoDB, CloudWatch and S3. The final calculation must retain verifiable inputs and include material snapshot/retained-volume, transfer/logging and free-tier assumptions; the draft is not a final reviewed cost PDF. Strongly consistent Scan usage must be based on table size and business homepage reads, rather than equating HTTP requests with DynamoDB read units.

The10November Learner Lab displayed $32.10 used of $50. This is a delayed account-wide observation, not the cost of this deployment alone or its annual estimate. Additional old/cafe practice instances were present outside the final project architecture. A stopped the no-longer-needed runtime builder and retained its disk; the other practice resources were not changed. Testing and footage should be collected in coordinated windows, with retention/teardown handled according to confirmed course instructions rather than an unreviewed reset.

Before submission, resolve HTTPS and the capacity-scaling requirement, obtain independent evidence/section reviews, verify all references and prepare the final architecture/cost PDFs and playable video. Measure report body words and rendered pages; the requirement is strictly under 4,000 words AND 8 body pages, references/appendices excluded. Each member personally confirms actual contributions and AI use and signs the required statements. No work performed by A while Tenzin was unavailable is attributed to Tenzin. The final submission and resource-retention method must be checked against current Moodle/tutor guidance.

## References and internal evidence

[1] Amazon Web Services, “Gateway endpoints,” Amazon VPC documentation, accessed 10 November 2026. https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html

[2] Amazon Web Services, “DynamoDB read consistency,” accessed 10 November 2026. https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html

[3] Amazon Web Services, “Health checks for Application Load Balancer target groups,” accessed 10 November 2026. https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html

[4] Amazon Web Services, “Using Amazon CloudWatch alarms,” accessed 10 November 2026. https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Alarms.html

[5] Amazon Web Services, “Policy evaluation logic,” accessed 11 November 2026 Sydney. https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html

Internal evidence: `docs/business-handoff-2026-11-07.md`; A's T09 deployment/write/restart logs; `docs/b-design-report-draft.md`; `docs/b-t11-verification.md`; C's T12 cloud-run/sample logs; C's cost/video drafts; the 10 November restoration/security/monitoring exports linked from `docs/requirements-evidence-matrix-2026-11-10.md`. These links support review; final report figure numbers and frozen commit references are not yet finalized.
