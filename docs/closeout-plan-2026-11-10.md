# Pre-submission closeout: not waiting for the new member's reply

**11 Nov update:** the project owner has explicitly deferred auto scaling for now; the brief/rubric conflict is kept for the teacher to confirm, and the deferral is not described as agreed by the teacher. The 1-page architecture PDF, network-security chapter and review entry point are prepared, see [architecture handoff](architecture-review-2026-11-11.md). The table below is the 10 Nov stocktake; the task is no longer "produce the architecture diagram from scratch" but to cross-check it and revise/freeze it once the HTTPS approach is settled.

2026-11-10, Sydney time. The user explicitly asked to keep going and not to stop work because Tenzin has not yet replied. A, under his own DiegoXue-coder identity, temporarily claims T25/T19 to prepare the objectives, evidence matrix and overall report; this is not Tenzin's contribution, does not cancel his membership and does not change the attribution of B/C's existing work. When D arrives he can take over the coordinated writing, review or unclaimed video preparation, and cannot overwrite existing claims.

## Current measured state and remaining items

| Item | Real results so far | Still to deliver/resolve | Owner and work that can run in parallel |
| --- | --- | --- | --- |
| System running | After starting the Lab on 10 Nov both targets healthy, business GET 200, two old records read back; source 06c2292 | B to add his own independent retest after the failed pre-check; reconfirm it is online before the final recording/acceptance | A keeps the operation window, B retests; do not wait for documents |
| Monitoring/failure evidence | A's stop/restart readback logs; C's 30 independent requests all 200, 15 per host; on 10 Nov the real 7 Nov business-alarm history and same-period metrics were retrieved | C independently checks the new CloudWatch evidence and decides whether to add full continuous sampling; A's current short sample cannot claim seamless failover or a whole-AZ failure | A provides the original AWS records, C reviews; if insufficient, arrange another 20–30 minute window |
| HTTPS/security | Private two-host setup, restricted security groups/endpoints, encrypted disks and role access checked | The listener is still HTTP 80 and ACM has no certificate; settle a course-accepted domain/certificate approach and verify it for real; keep limitations such as the broad LabRole | A; this is a technical gap and cannot be replaced by explanation in the report alone |
| Scaling with demand | Two-host routing, shared data and a stateless application exist | On 10 Nov there was actually no Auto Scaling Group. The rubric lists scaling on demand as core while the brief's wording conflicts; confirm soon or implement and test an approved approach; two fixed instances are not evidence of auto scaling | A prepares the plan and checks Lab limits; this cannot be left to the last day |
| Design report PDF | Alex's application/data first draft, C's experiment/cost drafts, A's objectives and integration draft from this round | Technical owners check their chapters, add final results and limitations, unify references, measure word/page count and export the PDF | A coordinates temporarily, B/C each write and check their own parts, D can review/take over after replying |
| Architecture diagram PDF | Real resources, subnets, SGs, EBS, database and protocols checked | Produce the final diagram with AWS symbols, including two AZs, ALB, EC2/EBS, DynamoDB, endpoints, monitoring and real protocols; conservatively 1 page | A, with B/C cross-checking; can be done now |
| Cost PDF | C's 12-month calculator input/amount draft | Save verifiable calculator inputs/results, review public IPv4, snapshots/retained volumes, logs/transfer against the actual architecture, and state the free-tier/full-year assumptions; conservatively a 1-page PDF | C; kept separate from the Lab account's actual usage |
| Video | C has a 60-second script | Real browser insert/read, two-host routing or availability footage, narration of key choices, edited into a playable final cut with measured length | A coordinates footage for now, B demonstrates the application, C provides request/monitoring footage; continue even if D does not reply |
| Sign-off/final submission | Originals/templates, source code and process evidence are archived | Each of the four declares their actual contribution, signs the cover sheet personally and records AI use; check all files against Moodle requirements, one person uploads and another checks the receipt | C collates, everyone confirms personally; A designates the uploader/checker |

## Shortest completion order

1. **Suggested for 10–11 Nov**: first restore/check the current service; B retests, C checks the new monitoring evidence; A handles the HTTPS and scaling requirements; report/diagram/cost drafts progress at the same time.
2. **Suggested for 12–13 Nov**: complete the technical experiments that still need doing, and produce first versions of the report, architecture diagram, cost PDF and video; unverified results are not written up as successes.
3. **Suggested for 14–16 Nov**: cross-review, fix, measure format/word count/page count/duration, check code and references, complete individual sign-off, freeze the version and back up.
4. **Before 17 Nov 16:00 Sydney**: upload following the current Moodle submission page, independently open the files to check them and save the receipt; handle resource retention/teardown according to the course-confirmed requirements.

The dates are this round's suggestions and do not mean other members have committed to being online at those times. The formal deadline is 2026-11-17 16:00 Australia/Sydney. The conflict between the brief's 1-minute video and the rubric's 2 minutes is handled conservatively at 60 seconds for now; the report body is strictly under 4000 words and under 8 pages, excluding references/appendices.

## This round's budget and operating boundaries

The Lab shows $32.10/$50 used, a delayed account reading, not this project's single-session spend or the formal annual cost. After starting, extra old-assignment/course cafe instances were also seen running; they are not part of this group's final architecture cost, and these exercises were not changed this round. The role-less runtime-builder, having served its purpose, was returned to stopped with its disk kept. After the necessary evidence is collected, resource use is scheduled in batches and no unrelated features are added.

## Items to confirm with the tutor in one message (to be sent by a real person)

“Our Learner Lab solution currently uses two private EC2 instances behind an ALB and DynamoDB. Could you confirm whether automatic capacity scaling is required for the core criteria, given the brief/rubric wording? What HTTPS/domain/certificate approach is accepted when the Lab provides no domain? Should the video be one or up to two minutes, and what resources must remain available for marking after evidence is captured?”

This file is not a message already sent to the teacher and does not replace a course answer. The questions above do not block organising evidence, writing and preparing the video now.

Tenzin not replying does not block technical and documentation progress. If, close to submission, his own contribution confirmation or sign-off is still missing, explain the real participation and contact situation to the tutor under course rules; do not sign on his behalf or invent contributions, and do not assert that the course has waived the requirement.
