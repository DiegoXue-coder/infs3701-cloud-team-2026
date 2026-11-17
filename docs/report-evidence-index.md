# Report source-material entry: requirements, images, logs and receipts

**12 November review:** The [design report PDF](../output/pdf/reading-tracker-design-review.pdf) has four body pages and a separate references page. Edit the [English source](design-report-working.md) and regenerate with `python scripts/build_design_report_pdf.py` using ReportLab. Review this PDF before freezing the submission.

| Reviewer | Next review action |
| --- | --- |
| Diego | Check the security and deployment claims against the latest AWS evidence. Update the report and diagram after any verified HTTPS change. |
| Alex | Check application and DynamoDB details against the pinned release. Record the independent retest result when the live endpoint is available. |
| Marina | Check the alarm and routing evidence and finish the separate 12-month cost PDF. Confirm whether the historical estimate in the report needs updating. |
| Tenzi | Redraw the existing architecture in Draw.io and hand over the editable source and one-page PDF for Diego to verify. [Reference and checks](architecture-review-2026-11-11.md) |

T20 video still needs a lead. Prepare the shot list from Marina's script, then arrange one live recording window for the browser demonstration and evidence. Each member should confirm their own contribution and AI-use record before signing.

**10 Nov addition:** [closeout checklist](closeout-plan-2026-11-10.md), [English overall report working draft](design-report-working.md), [requirements/evidence matrix](requirements-evidence-matrix-2026-11-10.md), [real business alarm and C's same-period monitoring check](monitoring-reconciliation-2026-11-10.md). The latest network/business readback and dashboard screenshots are linked from the matrix, and older evidence is kept at its original dates. Not all final deliverables are complete.

Updated: 2026-11-01. Evidence baseline commit for this round: `b6c091c`. This page is a source-material index, not a finished report or final acceptance.

**2026-11-07 business-evidence addition**: read first the [business release and B/C handoff](business-handoff-2026-11-07.md), [real page screenshot](../evidence/T09/2026-11-07-A-reading-tracker-live.png), [real write and cross-instance readback](../evidence/T09/2026-11-07-A-cloud-write-read.log), [service continuing while the writing instance was stopped](../evidence/T09/2026-11-07-A-during-writer-stop.log), [same record_id kept after restart](../evidence/T09/2026-11-07-A-post-restart-read.log) and [release/rollback steps](business-rollout-2026-11-07.md). These are A's real cloud-operation evidence; C has not yet independently accepted and HTTPS is not complete. The 1 November "business not yet verified" entries in the table below are kept as history and do not represent progress as of 7 November.

## What the report really needs

The original [assignment brief](../sources/original/assignment/INFS3701_Group_Assignment.pdf), [marking sheet](../sources/original/assignment/INFS3701_Group_Assignment_Marking_Scheme.pdf) and [requirements summary](assignment-requirements.md) are the basis. The current requirements comprise five deliverables: deployed system, design report, architecture diagram, 12-month cost estimate and video.

The body of the design report must be strictly under 4,000 words and under 8 pages, excluding references and appendices; images placed in the body also count towards body pages. The diagram and cost files are each kept to the brief's "under 2 pages", currently made conservatively as 1 page each. The brief/rubric conflict on video length awaits tutor confirmation; prepare at 60 seconds first. Individual contribution statements, genuine sign-off, code and AI/process records are also required; personal material such as signatures is not thereby automatically approved for upload to the repository.

The report must explain whose problem the service solves, why these services were chosen, how requests flow, why it is configured this way, real test results and trade-offs/limitations; it cannot simply arrange operation screenshots into a report. Before final submission check the latest Moodle requirements and tutor answers.

## Find evidence by report content

The links below are all real files in the repository, which members with private-repository permission can view/download. Detailed configuration and limitations are in [this round's verification and handoff](2026-11-01-foundation-verification.md).

| Which part to write | Material that can be used directly | Conclusions it supports and their limits |
| --- | --- | --- |
| Cloud service goal, how the old project is upgraded | [Old code](../app/reading_tracker.py), [original snapshot](../reference/reading_tracker_candidate.py), [project choice](../project/config.json) | Diego's Reading Tracker is the starting point; specific user needs and upgrade reasons still need adding |
| Network, two AZs, access flow | [Actual resource inventory](../project/aws-resources.json), [final configuration readback log](../evidence/T09/2026-11-01-final-readback.log), [VPC details screenshot](../evidence/T06/2026-11-01-vpc-details.png) | Real subnets, routes, endpoints and security groups; the network diagram must include EBS, the database and the real HTTP protocol, and the final diagram is still to be made |
| Servers, encrypted disks and start-up method | [Private-host role check screenshot](../evidence/T09/2026-11-01-private-role-check.png), [maintenance verification log](../evidence/T09/2026-11-01-maintenance-validation.log), [runtime build script](../deployment/runtime-builder.sh), [dependency versions](../deployment/runtime-requirements.lock) | Role access on both hosts, disk encryption, foundation service normal after restart; not evidence of the business application release |
| Database choice and access method | [Reasons and trade-offs](aws-owner-handoff.md), [table-creation script](../deployment/create-database.py), [maintenance verification log](../evidence/T09/2026-11-01-maintenance-validation.log) | DynamoDB ACTIVE, Describe/Scan passed from both private hosts; no business write, migration or shared business-data verification yet |
| Load balancing | [Per-request log](../evidence/T09/2026-11-01-live-routing.log), [foundation page screenshot](../evidence/T09/2026-11-01-foundation-live-page.png) | First 12 requests HTTP 200, 6 per instance; the page is clearly a placeholder foundation page and cannot be used to prove Reading Tracker features are complete |
| Monitoring dashboard | [Graph screenshot after recovery](../evidence/T09/2026-11-01-cloudwatch-dashboard-final.png), [monitoring configuration script](../deployment/configure-monitoring-baseline.py) | Actual monitoring widgets and healthy-count changes; the screenshot is a record from that time, not a live AWS dashboard inside GitHub; monitoring is a core requirement this time |
| Single-host stop, alarm, recovery | [Real alarm screenshot](../evidence/T09/2026-11-01-real-alarm-trigger.png), [maintenance log](../evidence/T09/2026-11-01-maintenance-validation.log), [alarm state history](../evidence/T09/2026-11-01-final-readback.log) | Real OK→ALARM→OK; the other host responded normally in samples during the period. Not a measured whole-AZ failure, a zero-downtime guarantee or proof of SNS notification |
| Security and Lab limitations | [Actual access audit](aws-access-audit.md), [final rules log](../evidence/T09/2026-11-01-final-readback.log), [operations limitations note](2026-11-01-foundation-verification.md) | LabRole is broad, OpenTunnel is denied, the unused SSH path is closed; HTTPS and full least privilege still have gaps that must be stated honestly |
| Reproducible operations, failures and fixes | [Deployment scripts directory](../deployment/), [this round's operation summary](2026-11-01-foundation-verification.md), [offline test log](../evidence/T09/2026-11-01-foundation-maintenance-offline-tests.log) | Provides region, dependencies, resources, configuration and steps; 48 offline passes cannot replace cloud business tests; the short-sample summary count error is explained clearly in the summary |
| Real contribution, AI use and versions | [T05 delivery](../deliveries/T05/2026-11-01-DiegoXue-coder-foundation-verified.json), [T06 delivery](../deliveries/T06/2026-11-01-DiegoXue-coder-foundation-verified.json), [T09 delivery](../deliveries/T09/2026-11-01-DiegoXue-coder-foundation-verified.json), [receipt data](../data/receipts.json) | This round is A's actual operation with AI assistance; all are partial and cannot be written up as B/C's contribution or as independent review passed |
| Cost | [Environment and budget observation](../project/aws-resources.json) | $1.30/$50 is a delayed budget reading, not this round's spend or the 12-month estimate; the Pricing Calculator file, running hours and assumptions still need adding |

## How to extract images for the report

1. Manually: click the image links in the table above on GitHub, view the original and download the PNG; take the test time, parameters and results from the adjacent log. Prefer the original PNG for report figures, to avoid blurry text from screenshots of the GitHub web page.
2. An AI with tools: read the repository with the member's own GitHub authorisation, or pull a local clone, read the PNGs, logs, JSON and source by the paths on this page, then actually embed the images in the Word/PDF. Do not just write into Word a private image URL that requires login.
3. When ordinary chat cannot read the private repository, the member downloads the needed files and gives them to it; a repository invitation does not automatically connect every AI. Do not make the repository public, and do not share AWS credentials.
4. For each image used record: figure number, caption, test date/environment, file path, evidence commit and matching log. In the final version use GitHub links at a specified commit, to avoid references drifting as main is updated later.
5. In the body choose only key figures that explain the design and results; extensive operation processes can go in an appendix or the evidence directory, packaged as the final submission requires. GitHub is the collaborative source library; the documents, code and video are still submitted as Moodle requires.

Sample caption: "Figure X: change in healthy target count during the 2026-11-01 infrastructure single-host stop test, later recovering to 2; source: evidence/T09/2026-11-01-cloudwatch-dashboard-final.png, commit b6c091c. This test used the foundation health service and did not verify business writes."

## Material that must be added later

The business version commit and release record, real feature results such as insert/read, shared business data across instances, business failure and recovery logs, HTTPS evidence, independent member review, the complete cost estimate, the final AWS architecture diagram and a video of real operation. After each new delivery add the mapping on this page, without overwriting old records or treating plans as implemented.

## Writing instruction that can be given directly to a teammate's AI

> Please first pull the repository's latest main and read AGENTS.md, docs/assignment-requirements.md, the original assignment brief/rubric and docs/report-evidence-index.md. Organise a report draft for the chapters I am responsible for, read the real PNGs and prepare to embed them, and label each conclusion with its evidence path, commit, test time and limitations. Distinguish infrastructure tests from final business verification; write untested items as to be verified, and do not invent results, references, individual contributions or peer approval. When tool permissions are missing, list clearly the files I need to provide. Keep the body within the overall report limit of strictly under 4,000 words and under 8 pages; deliver a draft now and do not submit to Moodle automatically.
