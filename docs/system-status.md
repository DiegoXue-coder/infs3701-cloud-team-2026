# Current system status

> 2026-11-12: the English design report has been generated as a [review PDF](../output/pdf/reading-tracker-design-review.pdf). The body is 4 pages and about 1,965 words, plus 1 page of references. Teammate review and follow-up work are in the [report source-material entry](report-evidence-index.md). This round was organised from evidence already in the repository.

> 2026-11-11: the HTTPS approach is settled as two-leg TLS. The existing ALB uses a publicly trusted certificate, and the two EC2 hosts use internal TLS open only to the ALB. The configuration order, verification and rollback are in the [HTTPS implementation plan](https-rollout.md). The entry point still awaits confirmation of a subdomain with manageable DNS or an existing usable certificate, and the plan is not yet deployed.

> 2026-11-11 Sydney documentation progress: the project owner explicitly deferred auto scaling; the surge files prepared on 10 Nov have no execution authorisation, and config keeps enhancements_enabled=false. A [1-page architecture PDF and review entry](architecture-review-2026-11-11.md), a [network/security chapter](network-security-chapter-2026-11-11.md) and a [draft of questions for the teacher](tutor-questions-ready-en.md) have been produced. The diagram is drawn from 10 Nov evidence, not an online check on 11 Nov; HTTPS is still unresolved, T15/T17 still await independent checking, and the message to the teacher has not been sent.

> Follow-up read-only pre-check on 10 Nov: CloudFront ListDistributions was denied; ACM certificates/Route53 hosted zones/ASGs are all empty, and the AutoScaling service-linked role does not exist (creation permission not yet verified). The T15 partial security audit and a local build of the scaling draft are complete, with no new AWS resources. See [actual checks, HTTPS blockers and scaling limits](security-next-steps-2026-11-10.md). The existing two hosts do not join the proposed scaling group; the plan is not deployed and does not count as a completed enhancement.

> 2026-11-10 actual update: the Lab was Terminated; after starting, both business targets were healthy, HTTP 200, and read back the original two records; currently still HTTP 80 only, no ACM certificate, no ASG. The real OK→ALARM→OK history from the 7 Nov business stop and CloudWatch data from the same period as C's sampling have been exported, awaiting C's independent check. The temporary build host is back to stopped; the Lab's delayed budget shows $32.10/$50. The report is being advanced by A first, see the [closeout checklist](closeout-plan-2026-11-10.md). The cause of B's 8 Nov error has not been proven retrospectively, and this recovery is not passed off as a root-cause conclusion for that time.

> 2026-11-08 collaboration update: role D is reserved for Tenzin/wyend12, with the English entry at [member-D.md](member-D.md). GitHub access, the member's own AI connection and task claims still need to be confirmed separately. B reported HTTP 503 at 15:35 Sydney on 8 Nov and did not write, cause unknown; do not call the 7 Nov success records below current online health.

> Latest actual progress (2026-11-07 12:28 UTC): Reading Tracker 06c2292 is released on the two private hosts; real database write, readback from both instances, the other host continuing to read while the writing instance was stopped, and the same record persisting after restart all passed. B/C independent cloud retests and HTTPS are still to be completed. Read the [latest business handoff](business-handoff-2026-11-07.md) first. History below is kept at its original dates, and old descriptions do not override the latest measurements.


Established 2026-10-31, Australia/Sydney.

## Ready to use

- Private repository, 21 original materials with a text index, 24 task cards, roles and a dependency plan.
- Fixed-command rules for claiming, progress, blocking, JSON delivery and review by another account.
- `scripts/team.py`: each person's own AI uses existing GitHub authorisation to read and refresh tasks and the dashboard during chat. No model API key or new paid service is needed.
- `AGENTS.md`, `CLAUDE.md`, a general opening prompt and joining notes.

## Limitations found

1. **GitHub Actions cannot start.** The first run reported: `The job was not started because recent account payments have failed or your spending limit needs to be increased.` [Original run](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/actions/runs/41182740718). Payment information and limits were not changed; the workflow is kept but paused, to avoid repeated red failures. Chat-driven sync is used for now.
2. **No GitHub Projects scope.** The existing Git authorisation can manage the repository and Issues but cannot create Projects v2. The dashboard is therefore `DASHBOARD.md`, generated automatically in the repository with task links and a timetable, not a native drag-and-drop Projects board.
3. **The holder's connector 404 was fixed on 2026-11-04.** With the user's explicit approval, only the team repository was added to the selected scope of the existing ChatGPT Codex Connector, second-brain was kept, and the repository is still private. The connector actually read the repository, project/config.json and T08 successfully. Other members' own connections still need retrying and verifying, see the [authorisation record](2026-11-04-connector-access.md).
4. Marina057 and Alex4325Li have accepted the repository invitation and have write access. Alex4325Li is enrolled as B and has uploaded the T04 delivery; Marina, as relayed by Diego, has chosen C but has not yet enrolled/claimed in the system. She reports 17 local tests and drafts, whose files are not yet uploaded and cannot be treated as accepted results. A is DiegoXue-coder; for the latest state still read the Issues/configuration.
5. The 8 new files for Week 5 and Week 7 are archived and shared; the formal Week 8/9 slides are still to be received, and it cannot be claimed that the whole term's materials are complete.

6. The current Learner Lab Readme explicitly prohibits creating users or groups; separate IAM login accounts cannot be created for the other two members. The us-east-1 console was entered for a read-only check, and no permissions were changed. A separately provided group access method awaits tutor confirmation, see `docs/aws-access-audit.md`.

## When restoring background mode

After the account holder resolves the GitHub billing/quota problem themselves, the owner can re-enable `.github/workflows/team-sync.yml` and run it manually to verify; until it succeeds, chat sync is still used. If GitHub Projects and AI connector authorisation need widening, the user handles that separately, and permissions are not widened without approval during initialisation.

## What "complete" means

A working collaboration system does not mean the assignment is done. Real AWS configuration, running tests, the report, cost and video still have to be carried out and reviewed item by item from the task cards. Without a second member, independent review cannot be demonstrated or faked as successful.

## Self-service start entry (2026-10-31)

docs/self-service.md, the B/C role guides, project/handoffs.json, setup_member.py and team.py join are provided. 44 tests pass, and local isolated dependency installation and the offline baseline check pass; no two other real accounts have accepted yet. Private repository access must first be invited and accepted by each person; the two can each choose a vacant role without splitting in advance; role binding is not new AWS authorisation.

## 2026-11-01 actual start

T05 has been claimed by DiegoXue-coder. Today's Lab was started and the old EC2/S3 inventoried read-only; there is no new usable cloud service yet. See docs/2026-11-01-aws-inventory.md; actual defects and untested items are all kept and cannot be reported as fixed.
