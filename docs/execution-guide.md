# Three people completing a cloud service together: execution manual

INFS3701 cloud architecture and AWS practice | Drawn up 2026-10-31 | All dates are Sydney time

For the latest schedule, handoffs and single-person AWS operation arrangements see [parallel-plan.md](parallel-plan.md); where they differ, that plan and the latest task cards prevail. This is an execution draft that can be taken to tonight's meeting to divide the work. Upgrading the user's own Reading Tracker is now confirmed; member names, the database and permissions still need confirming at the first meeting. The AWS project is not yet actually deployed; the private GitHub collaboration hub and task cards are set up, and the current way of operating is in the README and docs/system-status.md. The code entry point is app/reading_tracker.py, using Option A.

The formal brief deadline is **2026-11-17 16:00**; dates below such as 3 Nov and 6 Nov are suggested internal milestones. The goal is a submittable version by 16 Nov. The official evidence is the INFS3701 assignment brief and marking sheet in `source_materials/INFS3701/03_assessments/group_assessment/`; the earlier meeting outline has been worked through item by item.

## 1. What we finally build

Keep a small, usable reading-record web page: add records, view records, show statistics. Upgrade the system behind it to:

`User's browser → single entry point (load balancer) → two application servers in different Availability Zones → one shared managed database`

Plus a monitoring page to observe how it is running and an alarm that can really be triggered. An Availability Zone can be understood as a separate data-centre area within the same region; stateless means important data cannot live only in one application server's memory or local files.

First get "still available when one fails, two servers read and write the same data, with alarm evidence" right. A new account system, recommendation algorithms, complex interfaces and the like are left out of scope for now. Whether there are real users and real traffic must be stated honestly; test concurrency can be used as a design assumption, but user scale must not be invented.

**Draft selection:** continue with Flask + two EC2 + Application Load Balancer; for the database first compare DynamoDB and Multi-AZ RDS. If it is only small independent book records, the DynamoDB route can be verified first; if course labs, query needs or permissions suit a relational database better, choose Multi-AZ RDS. The choice is not a price conclusion; it finally rests on requirements, operability, permissions and the calculator estimate.

## 2. The three people's responsibilities

| Code | Suggested person | Main responsibility | What must be handed to the others |
| --- | --- | --- | --- |
| A | You (DiegoXue-coder) | Network, servers, single entry point, deployment environment | A reachable address, resource configuration, deployment steps, architecture diagram |
| B | Member two | Web back end, database read/write, both servers running the same version | Runnable code, data fields, start method, feature demo |
| C | Member three | Monitoring, testing, evidence, cost estimate, video integration | Test results, alarm evidence, estimate, video draft |

Being responsible does not mean doing it all alone: A's deployment needs B's code; C's testing needs A/B's cooperation. Everyone writes their own design reasons, steps and limitations, and the whole report is not dumped on C. A finally integrates the architecture, B the report, and C the video and evidence; the three cross-check.

Divide the work by the codes above first and write the names on the task board tonight. Adjust for free time, and do not presume the three people's actual contributions are equal.

## 3. How the time runs and what can be done at the same time

| Time | A at the same time | B at the same time | C at the same time | What to have at the end of the stage |
| --- | --- | --- | --- | --- |
| 31 Oct | Jointly settle the topic, confirm permissions/balance | Jointly confirm whether the old code can be reproduced | Jointly set up the task board, record questions to ask | Project, owners, collaboration location and first integration time settled |
| 1–3 Nov | Verify network/servers, HTTPS and lab permissions | Settle the database, get the single-instance application working | Test checklist, report skeleton, cost assumptions | First version of the application can write new records to the managed database |
| 4–6 Nov | Connect the single entry point and the second server | Get both running the same code version, sharing data | Check read/write on both, build the monitoring page | Single entry point usable, both healthy, data shared |
| 7–10 Nov | Help with failure testing, security checks and the chosen enhancement | Fix test problems, organise reproduction steps | Measure the alarm, record failure and routing, calculate the formal cost | Every core requirement has evidence; decide whether to complete the enhancement |
| 11–13 Nov | Finalise the architecture diagram and network chapter | Integrate the report, others reproduce by the steps | Joint recording, edit the video, finalise the cost | First drafts of all five deliverables complete |
| 14–16 Nov | Check the deployment against the diagram | Check text, code, references | Check the video, evidence, file completeness | A submittable version signed off by everyone |
| Before 17 Nov 16:00 | Designated submitter uploads | Check content and that files open | Save the submission receipt | Formal submission complete |

Dates are only available windows and do not mean everyone is online all day every day. Each person schedules independent work; four joint checks of about 30–45 minutes are suggested on 3, 6, 10 and 13 Nov; set the actual times tonight from the three timetables.

### Order of joint completion (independent preparation can start early)

On 2026-10-31 the actual task cards were changed to two gates, "start preparation" and "complete acceptance"; the details are in [parallel-plan.md](parallel-plan.md) and the latest Issues. The order below describes real integration results and does not mean the next member must wait for the previous one to finish everything before starting.

1. Settle the service and database direction → write down the data fields and start convention.
2. The application works with the database → both application hosts run the same version.
3. The network and both application hosts are ready → connect the single entry point and test jointly.
4. The joint system works → measure routing, stopping one host, and the alarm.
5. Tests pass and evidence is saved → record the real-operation video and finalise documents.
6. All three check and sign → submit → clean up resources according to the confirmed acceptance arrangement.

**Can be done early:** report outline, first architecture draft, test scripts, cost assumptions, video script and deployment document, from day one. **Can only be finished with real results:** the actual failure conclusion, final cost, final architecture diagram and real demo video. An experiment that stops one server cannot be written up as a fully measured AZ failure.

## 4. How to do each step

Task numbers, live owners and acceptance are detailed in the [GitHub task cards](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues) and `DASHBOARD.md` in the root. The operating order below is the team's workflow and does not assume the lab has every AWS permission.

### Step 1: write down the joint agreements tonight (T01–T03)

The starting service is confirmed as Reading Tracker, with no reselection of topic. Write in one sentence "who uses it, what it does, and why it should not go down". Confirm which Learner Lab is used for the final demo and note the remaining credit. C organises and asks the tutor: video length, whether auto scaling is mandatory, whether teardown is allowed after evidence collection, and how several members should obtain permitted lab access.

A creates the private code repository and invites the other two under course rules; C sets up the task board with owners, start dates, target dates and prerequisite tasks; B uploads the cleaned-up application code and dependency list. Do not upload the whole study-materials directory to the repository.

**Handoff:** C records the meeting conclusions in `collaboration_starter/docs/decisions.md`; the three confirm, and later changes are recorded here too.

### Step 2: first agree how the code connects (T04)

B writes a short agreement; after A/C review it, work proceeds in parallel:

- Which features the page keeps, and what result a test insert should produce.
- Data fields, for example `record_id`, `title`, `status`, `pages_read`, `total_pages`, `rating`, `created_at`; the primary key uses an ID that will not easily collide on simultaneous submissions.
- Configuration goes in environment variables, such as region, table name and server label; access keys must not be written in the code.
- Provide `/health` for the load balancer to judge whether the application has started, returning 200 when the process can respond; data-tier read/write gets a separate functional test. Do not treat "the process is alive" as "the database is definitely available".
- For example, standardise the application port as `8000` and a single start entry point; add the exact command to `docs/deploy.md` once dependencies and file names are settled. The two machines must be identical, and the Flask development server is not used as the final deployment method.
- The page or log shows a short `APP_INSTANCE_LABEL` and code version identifier, to help demonstrate that requests come from different instances; do not expose keys, full configuration or sensitive internal information in the interface.

**Why agree now:** A does not have to wait for all features before building servers, and C does not have to wait for the system to go live before writing tests.

### Step 3: A builds the foundation environment, B changes the application, C prepares checks (T05–T08, in parallel)

**A:** after entering the Learner Lab, first confirm us-east-1, the balance and the permitted role. Check whether two AZs, load balancing, a managed database, monitoring and the resources HTTPS needs can be used. Draw the public/private subnets of each AZ in the VPC, the entry point, and the application and data paths. Confirm how the private application reaches the database, downloads dependencies and is maintained, then create the smallest testable environment; if egress or endpoints are charged, include them in the cost. If a program in a private subnet cannot download dependencies, repeated restarts are not the fix; check the path.

Verify from the first stage whether the domain/certificate/lab permissions make HTTPS feasible, and do not wait until recording the video to find it cannot be configured. If restricted, keep the error and ask the tutor, and do not draw HTTPS that is not implemented. The RDS route also needs a separate database security group, multi-AZ capability and credential management; the DynamoDB route needs the application role and access path confirmed.

**B:** first reproduce the old application in your own development environment, then separate out the data-access code and move it to the chosen database. Verify with "create a test record → read it back → still there after refresh → still there after restarting the application". Use unique identifiers such as UUIDs to avoid the old code's second-resolution timestamp plus title overwriting same-second, same-name records. Do not write data only to a local JSON file; test with fictional book records and import no private information.

If B has no permission to operate the final environment, B submits the code and database creation steps and A runs them on a shared screen; B guides, explains and verifies the results. Development can use a permitted local substitute or B's own Lab, but the final evidence comes from the same integrated system.

**C:** first write the test steps and evidence table, stating how load distribution, data sharing, failure, alarm and security checks will each be accepted. Prepare the report headings, the cost table's items and traffic assumptions, and a 60-second video script. Do not wait until the screenshots are all in before thinking about what needs proving.

**3 Nov checkpoint:** A can show the environment sketch and permission results; B can demonstrate one real database write and read; C has a test table. If any one fails, fix it first and hold off on enhancements.

### Step 4: connect the two application hosts to one entry point (T09–T12)

A creates two instances following the two-AZ design and deploys the same commit B has reviewed; the code on the two servers is not hand-edited separately. Configure the target group (think of it as the load balancer's list of servers), application port and health-check path, and access through the single entry point only after both are healthy. Application inbound allows only the necessary sources; all ports must not stay open long-term for debugging.

B adds a record through this entry point and verifies the other instance can read it too; check whether sessions or temporary files make users lose data when they switch servers. Record the code commit ID and configuration with the deployment result, not just a URL.

C sends a small batch of reasonably spaced requests, keeping the time, response status and instance label. Connection reuse may make several consecutive requests come from the same host, so strict alternation is not required; there must be enough results to show both hosts handled requests. If data readback uses eventually consistent reads, the test should state the expectation and how long to wait, and not every brief delay should be classed as a failure.

**6 Nov checkpoint:** all three can use the features through the same address; both hosts healthy; both see the same persistent data; every major component on the diagram maps to the resource list.

### Step 5: monitoring, failure and security checks (T13–T16)

C builds the dashboard from real resources, showing at least entry-point request volume/errors, target health and suitable application or database metrics. Choose a meaningful alarm, such as too few healthy targets or an abnormal error rate. Explain why it was chosen, what the threshold and statistical window are, and how it is tested; the notification method depends on what the lab allows. Save the times and evidence from normal to ALARM and back to recovery; saving only "created successfully" is not enough.

The failure test is done by all three together: C first starts continuous requests and records results → A stops one test instance after confirming the other is healthy → B exercises the read/write features → C records the failure count, switchover time and recovery result → A restores the environment. Record the target group's health-check configuration first; there may really be brief failures, which should be explained, without demanding that the log show zero failures.

Security checks are asked by C and shown by A/B: what is the public entry point? Who can reach the application port? Who can read and write the database? Does EC2 use the permitted role and not copied old session keys? Where are encryption in transit and at rest actually configured? Are there unhandled limitations? Write the actual situation into the documents, to avoid a repeat of "the diagram says HTTPS, the system runs HTTP".

If auto scaling is chosen as the enhancement, A configures the policy, B ensures new instances start reproducibly, and C records scale-out and scale-in under controlled traffic. Setting the ASG minimum to 2 does not by itself prove automatic scaling with demand. If three enhancement topics are chosen instead, confirm before implementing that core is not double-counted, and leave tests and a business reason for each topic.

**10 Nov checkpoint:** core evidence complete and unresolved problems have owners; enhancements without evidence cannot be written up as done. If time is tight, stop non-essential new features first, but mandatory course items cannot be dropped as a "downgrade".

### Step 6: produce the documents, cost and video from the actual system (T17–T21)

- A checks the architecture diagram item by item against the resource list: AZs, subnets, entry protocol, flow direction, both instances, boot volumes, data tier, monitoring. The diagram is not an imagined target state.
- B brings together everyone's chapters. Important choices are written as "what was needed → what was considered → why this was chosen → cost/limitation → measured evidence". C/A reproduce the key steps from the deployment document, and missing steps are added by the original author.
- C uses the AWS Pricing Calculator, selecting us-east-1 and 12 months, to cost the important resources of the final architecture. State assumptions such as instance size/running hours, data volume, requests and traffic, including the load balancing, disks, database, logs and egress actually chosen. Also attach the Lab balance record from before and after experiments; the two are different accounts.
- The video is recorded jointly with real browser operation. Suggested: 0–10 seconds the goal and request path; 10–25 seconds add and read a record live; 25–45 seconds key clips of real routing or failure testing already done; 45–60 seconds one choice and its trade-off. A long failure test can be edited, but mark the elapsed time and do not pretend it finished in 1 second. Whether everyone must appear on camera follows the latest course instructions.
- Each person organises their actual AI-use statement, progress screenshots and individual contribution, without fabricating historical records.

### Step 7: cross-check and submit (T22–T24)

A checks "the diagram matches the deployment"; B checks "the report, code and steps are reproducible"; C checks "the video shows real operation, the cost, the evidence". Then rotate: A checks C's cost, B checks A's diagram, C checks B's notes. Check for leftover template text and keys, and confirm every file opens.

The design document body is strictly under 4,000 words and under 8 pages; the architecture diagram and cost estimate are conservatively 1-page PDFs each; the video is made within 60 seconds, pending tutor confirmation of the conflict. Have the individually signed contribution statements and genuinely signed cover sheet ready. Designate one uploader and one checker, and check the code, files and submission receipt Moodle requires. Clean up according to the confirmed acceptance arrangement; do not tear down resources before the final recording, and do not assume End Lab deletes all resources.

## 5. How the three manage things together

The collaboration system is already built, so no second progress sheet is created from scratch. The current formal process is in [team-protocol.md](team-protocol.md), and new members read [onboarding.md](onboarding.md) first.

- GitHub Issues are the source of live task state; DASHBOARD.md and data/snapshot.json are generated from them.
- Each person's AI runs `python scripts/team.py --user <own username> start` at the beginning to read their own tasks; at the end it uses the command function to synchronise actual progress or deliveries.
- The real usernames for A/B/C are registered in project/config.json. Claiming requires a matching personal identity, and changing the same AWS environment requires coordination; personal passwords or temporary credentials are not shared.
- Code is developed on separate branches and merged into one version after checking; configuration and documents are deliverables too, and not everyone is required to write application code.
- When several people cannot each operate the cloud, the environment holder executes on a shared screen while the others provide code/steps and verify together; state the actual operator and checker clearly.
- GitHub-hosted auto-refresh is temporarily limited by the account's payment/quota; for now the chat-time sync helper refreshes, without relying on GitHub Projects or a public website.
- Every completed item needs: an actual artefact, tests and evidence, reasons/limitations, and review by another member. A task cannot be marked complete on a bare "done".

## 6. Tonight's 45-minute kickoff checklist

- 0–10 minutes: confirm the Reading Tracker upgrade scope, claim A/B/C, and write actual names and each person's free times.
- 10–20 minutes: settle the final Lab environment holder; check budget, permissions, database candidates and the HTTPS difficulty.
- 20–30 minutes: open the private repository and task dashboard already set up; check member joining and role configuration.
- 30–40 minutes: A/B/C each describe their first deliverable and confirm the connection conventions for data/port/health check and so on.
- 40–45 minutes: set the first integration time, and record the tutor questions and who asks them.

First action after the meeting: A checks permissions and the network plan, B reproduces the old application, C writes the test checklist. All three can start at the same time.

## 7. Common terms in plain language

| Term | What it means in your project |
| --- | --- |
| GitHub repository | Where the three of you keep one set of code and its change history |
| Branch / Pull Request | Each changes a copy first, then asks another person to check before merging |
| commit | One numbered save of the code; both servers must use the same save |
| VPC / subnet | Your network range in AWS, and the areas it is divided into |
| Security group | Rules for which sources can reach which ports |
| Availability Zone (AZ) | Separate data-centre areas in the same region, used to reduce the risk of everything going down together |
| Load balancer / target group | The single entry point users reach / the list of servers behind it that can receive requests |
| Stateless | Important records live in the shared data tier and cannot exist only on one application server |
| IAM role | The identity that defines which AWS operations a program may perform; not a shared personal password |
| Dashboard / Alarm | The page for viewing running state / the rule that enters the alarm state when a metric is abnormal |

## 8. References and scope

- Path of this course's source files: `source_materials/INFS3701/03_assessments/group_assessment/`; the content is INFS3701. Requirement conflicts and Moodle updates still await confirmation.
- [GitHub Projects official documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects): task, board, table and timeline capabilities.
- [AWS official documentation on IAM roles for EC2 applications](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html): avoid distributing long-term credentials to instances; the Lab is still bound by course permissions.
- [DynamoDB getting-started official documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStartedDynamoDB.html): reference for later table creation and read/write operations.

This is an executable organisation and implementation order, not a verified set of deployment commands. Once the database, runtime, TLS and network path are chosen, each technical owner adds the real parameters and measured commands to the deployment record; do not invent ARNs, resource IDs, prices or test conclusions.
