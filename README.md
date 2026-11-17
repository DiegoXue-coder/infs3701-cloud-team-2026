# INFS3701 four-person cloud service collaboration hub / Four-person team hub

**11 Nov, ready for direct review:** [architecture diagram PDF/preview/editable source](docs/architecture-review-2026-11-11.md) · [network and security chapter](docs/network-security-chapter-2026-11-11.md) · [draft questions for the tutor, not sent](docs/tutor-questions-ready-en.md). Auto scaling has been deferred by the project owner; old preparation files do not represent deployment authorisation. The diagram is based on actual 10 Nov evidence; HTTPS is not complete.

**10 Nov security preparation:** [verified controls, actual HTTPS limitations and a draft 2→3 instance scale-out plan](docs/security-next-steps-2026-11-10.md). Preparation only, no new cloud resources, T15 not yet complete; B/C can review in parallel without waiting for D.

**10 Nov closeout entry point:** [what is still missing and the completion order](docs/closeout-plan-2026-11-10.md) · [English report working draft](docs/design-report-working.md) · [requirements/evidence matrix](docs/requirements-evidence-matrix-2026-11-10.md) · [recovered business alarm and metrics from the same period](docs/monitoring-reconciliation-2026-11-10.md). A has temporarily advanced T25/T19 without waiting for D's reply; this is not D's contribution or final acceptance.

**Come here to see progress, claim tasks and hand in evidence, then work with your own AI.** The cloud service runs on AWS; this repository connects the four members' work.

**Tenzin / wyend12: [English setup and your work](docs/member-D.md) · [Copy this English prompt](prompts/START-en.md) · [Four-person responsibilities](docs/four-person-plan.md).** Accept your invitation and authenticate your own GitHub/AI first. Your role assignment is not a task claim or a verified connection.

**Latest business handoff (2026-11-07):** [the two-instance application is deployed; B/C start independent cloud review from here](docs/business-handoff-2026-11-07.md). It includes the real URL, version 06c2292, the two instance labels, read/write/restart evidence and each person's next step; HTTPS and the group's final acceptance are not yet complete.

→ **[Self-service start for new members / Self-service entry](docs/self-service.md)**

→ [Online task entry](LIVE_BOARD.md) · [progress dashboard](DASHBOARD.md) · [all tasks](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues) · [daily opening prompt](prompts/START.md) · [first-time joining](docs/onboarding.md)

## All you need to say to your AI each day

> I am GitHub user ___. Please first read this repository's AGENTS.md, confirm my role and my latest GitHub task, tell me the project progress and what I should do first today, then take me through it step by step. At the end, organise the real delivery and update the task, and wait for synchronisation to be confirmed.

The first time, you need to give the AI tool your own GitHub access, or open a local copy of this repository. Giving an ordinary chat a private link does not automatically grant read access. After that you can simply say "start today's task".

## How collaboration works

1. The AI reads the latest Issue and recommends work based on prerequisite tasks and the member's role.
2. Comment `/team claim B` on the task card and wait for the system to confirm the claim.
3. Configure AWS, write code or produce materials, and keep real evidence.
4. Submit the delivery with its execution record to the default branch; use `/team report <file path>` for partial results and `/team submit <file path>` for a full delivery, which enters "awaiting check". Both produce numbered receipts.
5. After another member checks it and comments `/team approve <check notes>`, it becomes "completed".
6. The AI runs the repository sync helper to refresh the [dashboard](DASHBOARD.md) and the AI-readable [state snapshot](data/snapshot.json).

The current mode is **synchronise while chatting**: at each start the AI runs `python scripts/team.py --user <own username> start`; when updating a task it runs the same helper's command function. It reads the member's existing GitHub authorisation, calls no paid AI API and does not control AWS. Reading tasks, planning and checking are assisted by each person's own AI.

The GitHub Actions background-refresh configuration is kept, but the account currently cannot start runs because of payment/quota limits, so it is paused to avoid repeated failures; billing was not changed and limits were not raised. In this state a comment posted on the web page alone does not refresh automatically; the AI of any member with write access needs to run the sync helper. See [current system status](docs/system-status.md) for details.

## Working in parallel

[Current four-person split](docs/four-person-plan.md): A operates AWS/architecture, B application/data, C testing/monitoring/cost, D English report/evidence audit/video coordination. Preparation can run in parallel, while final acceptance keeps its necessary conditions; the [original three-person plan](docs/parallel-plan.md) is kept as history.

## The four roles

| Role | Main responsibility | Current member |
| --- | --- | --- |
| A | Network, servers, single entry point, deployment environment, architecture diagram | DiegoXue-coder (you) |
| B | Application, data code, independent verification, application/database chapter | Alex4325Li |
| C | Monitoring, testing, failure evidence, cost, collation of contribution records | Marina057 |
| D | English objectives/evidence audit, overall report integration, video coordination | Tenzin / wyend12 (access and own start pending verification) |

Each task has an owner, collaborators, check criteria and prerequisite tasks. A is responsible for the actual AWS configuration, B/C provide technical content and experimental evidence, and D integrates the English report and presentation; each person keeps original authorship, their own technical chapter and real contribution, using their own GitHub identity.

## How things are organised

| Content | Where |
| --- | --- |
| Original slides and examples, sorted by week | sources/original/course/02_weekly_materials/week_XX/ |
| The three original group-assignment files | sources/original/assignment/ |
| AI-searchable text and file checksums | sources/text/, sources/manifest.json |
| Live task cards and roles | GitHub Issues; project/config.json binds A/B/C/D |
| Real deliveries, tests, screenshots and logs | deliveries/ and the evidence files each task references |
| AI working rules and operating manuals | AGENTS.md, CLAUDE.md, prompts/, docs/ |
| Online access and progress summary | LIVE_BOARD.md (filtered entry), DASHBOARD.md (synchronised snapshot) |

[How to run a connection test](docs/connection-test.md) · [the difference between online and auto-refresh](docs/online-board.md)

## Materials and records

- [Report source-material entry](docs/report-evidence-index.md): find actual screenshots, logs, configuration and receipts by chapter, and how to download images or embed them in the report.
- [Material index](sources/INDEX.md): original assignment files, existing related slides, AI-searchable text, the list of missing items and checksums.
- [Assignment requirements and conflicts](docs/assignment-requirements.md): core requirements that must not be missed, deliverables and questions awaiting confirmation.
- [Three-person operating manual](docs/execution-guide.md): what to do, how, in what order, and the joint checkpoints.
- [Task definitions](project/tasks.json): plan and acceptance; live state is in the corresponding Issue, do not hand-edit the snapshot.
- [Delivery template](templates/delivery.json), [meeting decisions](docs/decisions.md), [environment record](docs/environment.md).
- [How to report at the end of work](docs/reporting.md): actual screenshots/logs, test results, receipts, review; the dashboard shows recent records and full receipts are in data/receipts.json.
- [Protocol](docs/team-protocol.md): claiming, progress, blocking, submission, review and recovery.

## Current boundaries

The user has confirmed upgrading their own Reading Tracker (Option A). The [code entry point](app/reading_tracker.py) and [run notes](app/README.md) are available; two private hosts with shared DynamoDB are now released, and A has verified real read/write, cross-instance readback and persistence after restart; B/C independent cloud review, HTTPS and final deliverables such as the report still need to be completed. The deadline is **2026-11-17 16:00 (Sydney)**; internal milestones are suggestions; Moodle updates and tutor answers on conflicts should be recorded before adjusting.

The repository must stay private; do not deploy public Pages, and do not upload account passwords, AWS keys, private data or personal files with signatures/student IDs. Invite only actual teammates who are entitled to use the course materials.

## Current application and AWS collaboration

[Reading Tracker code](app/reading_tracker.py) has been selected and is integrated as described in [three people jointly managing AWS](docs/shared-aws.md). Keep the application's features and upgrade networking/compute/database and monitoring; do not lose the existing application just because the environment is rebuilt.
