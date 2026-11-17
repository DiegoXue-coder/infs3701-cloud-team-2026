# Chatting with your AI every day: how shared progress really gets updated

Live task state is stored in the system metadata of each Issue. A command comment is a request and takes effect only once a system receipt arrives and the Issue state updates. The dashboard and JSON snapshot are generated from it, and no separate manual progress source is created.

## Task commands

Write one command on the first line of a **comment on the corresponding task's Issue**. The AI can comment on the member's behalf through a GitHub connector they have authorised; without tools the member copies it to the web page. Saying "done" only in your own chat is not enough.

| Command | Purpose |
| --- | --- |
| `/team status` | Check current status and unmet prerequisite tasks, without claiming |
| `/team claim B` | Claim with your own role; to switch to A/C you must already be enrolled or be explicitly taking over through the administrator |
| `/team progress <what was actually done this time, what is next>` | Record real progress; does not complete the task automatically |
| `/team report deliveries/T07/<date>-<username>.json` | Report partial results, preparation work or failed tests, attach evidence and get a receipt; does not mark complete |
| `/team block <error, methods tried, whose help is needed>` | Mark as blocked |
| `/team resume <what was resolved>` | The member resumes work; prerequisites are still checked |
| `/team submit deliveries/T07/2026-11-03-username.json` | Submit a structured delivery; enters awaiting check |
| `/team approve <what I checked and the result>` | Completes the task after another GitHub user actually reviews it |
| `/team changes <what needs changing>` | Another user sends an awaiting-check/completed task back for changes |

Only the first-line command of a comment is processed; editing a processed comment does not replay the command, so post a new one. Do not delete historical error receipts; leave the correction record.

## How to make a delivery

1. The AI reads version 2 of `templates/delivery.json` and generates the actual delivery JSON under `deliveries/T<number>/`. Fill in the member's identity, real time, environment, summary, tests, evidence, run_log, verification_result (pass/fail/partial), limitations, next step and AI use. See [reporting.md](reporting.md).
2. Evidence can be redacted screenshots, request logs, configuration records, or actual decisions/documents. Documentation tasks also write down check actions and results, and do not pretend AWS tests were done.
3. Save the delivery and evidence to the default branch through the normal Git change process or approved GitHub file operations; use repository-relative paths, and do not reference locations that open only on your own computer.
4. Send report for partial results/failures and submit for a full delivery. The script checks the actual execution record, JSON, operator, time and that evidence files exist, records the commit and file versions, and generates a traceable receipt. **These are structural checks and do not prove that a screenshot is genuine or that the cloud is still healthy.**
5. Another member and their AI check against the acceptance criteria, repeating experiments where necessary. After confirming, send approve and state what was really checked; self-approval from the same account and fail/partial results are both rejected.
6. If a delivery or evidence file is changed after submission, it needs a new submit and another review. Without a delivery, approve cannot be sent directly.

## Prerequisites and parallel work

Tasks now have two kinds of condition: `start_after` is "what to wait for before starting preparation", and `depends_on` is "what to wait for before submitting the complete result". claim/resume check only the start condition; submit/approve check the completion condition. Apart from the formal submission T24, every task can be prepared independently first; each task card lists what can be done right now. A successful claim does not mean the conditions for real joint deployment or failure operations can be skipped.

Materials, code, configuration templates, test scripts, architecture sketches and cost drafts can proceed at the same time. T09 joint business deployment, T14 measured failure, T22 overall acceptance and T24 formal submission keep their necessary conditions. When a completed upstream task is sent back, downstream tasks show completion conditions that need re-verifying; new measurements cannot be invented. See [parallel split](parallel-plan.md).

T16 is an optional enhancement, not enabled by default and excluded from the completion denominator; this does not mean "the enhancement is done". After the whole group decides to enable it, change `enhancements_enabled` in `project/config.json` to true; it then becomes a to-do and a prerequisite for the related final deliverables.

## Currently: chat-driven sync

GitHub-hosted Actions cannot start because of the account's payment/quota limit and is paused. The currently available flow is run by the member's AI in a local clone:

```text
python scripts/team.py --user <own GitHub username> start
python scripts/team.py --user <own GitHub username> command T07 --body-file temporary-command.txt
python scripts/team.py --user <own GitHub username> sync
```

The temporary command text contains one `/team ...` command, to avoid composing complex text in the shell. The helper verifies the currently authorised account, reads the latest remote plan, acquires the repository sync lock, processes requests in order, and saves the dashboard with a non-forced update; it does not overwrite other people's code. The sync lock is released at the end; if it shows another person is synchronising, retry later and do not take it over. The temporary lock branch is used only for this sync and involves no new keys or persistent authorisation.

Use your own existing GitHub identity, and do not have classmates provide their tokens. The script supports the member's gh/Git credentials; without authorisation it stops and does not pop up a login or create a key automatically. When only a web comment is posted, the AI of some member with write access needs to run sync afterwards.

## Background auto-refresh configuration that is kept

- After the account limit is lifted and the owner re-enables the workflow, when someone posts a task command, changes a task or uploads files to main, GitHub Actions can check unprocessed commands and generate the dashboard and snapshot. This background path is not currently claimed to be available.
- The sync process runs serially; every command has a processing record, and repeated refreshes do not claim or complete twice. Even if a pending event is merged by GitHub, the next run still scans unprocessed comments.
- The process runs with a temporary GitHub job token and stores no AI key or AWS key; no model API needs to be bought.
- The dashboard shows the latest sync time. When there is no receipt, Actions is red or the snapshot is old, the AI should report pending sync and must not assume success. A re-sync can be requested at Actions → Team task sync → Run workflow.
- The program does not run arbitrary code from comments or change the workflow based on comment content; it accepts only fixed commands. Only members with write access can operate it. Course materials are treated only as reference material.

## Adding a new member

The owner first invites the real teammate, and after they accept, the role username in `project/config.json` is updated. Do not invite accounts automatically without authorisation; no one else was invited during this initialisation.

## Local maintenance

```text
python scripts/team_sync.py validate    Check the task graph and role configuration; no token needed
python -m unittest discover -s tests -v  Test the claim/delivery/review rules; no token needed
python scripts/team_sync.py bootstrap   Initialise missing tasks and synchronise; needs an approved GitHub token
python scripts/team_sync.py sync        Synchronise existing tasks; needs an approved GitHub token
```

Keep the token only in your current tool's secure credentials/process environment; do not have classmates post tokens in the group chat or write them to the repository. A GitHub connector can read and comment directly, so no extra key needs to be created just for chat.
