# Tenzin / wyend12 — self-service English setup and work

**Current priorities are T26 and T20.** Tenzi operates the replacement demo in his own Learner Lab and records, narrates, edits and finalises the video alone. Start with the [English deployment guide](tenzi-lab-redeployment.md) and [solo narration](c-t20-video-script-2026-11-07.md). Diego exports and integrates the Draw.io source already delivered in T17.

Your assigned role is **D: English report, objectives/evidence audit and final presentation**. A/B/C remain DiegoXue-coder, Alex4325Li and Marina057. Role assignment is not repository permission, proof of joining, a task claim or a contribution record.

**10November continuity update:** the owner instructed the team not to wait for a reply. Diego has temporarily claimed T25/T19 under his own identity and is preparing the objective/evidence audit and integrated report. Check live ownership before claiming. Do not overwrite his claim; coordinate a handoff, independently review his preparation, or begin an unclaimed D task such as T20. His work is not attributed to you. Current source: `docs/design-report-working.md` and `docs/closeout-plan-2026-11-10.md`.

## One-time setup

1. Accept Diego's invitation to the **private** repository at https://github.com/DiegoXue-coder/infs3701-cloud-team-2026 using **wyend12**. If you see404, check the signed-in account and invitation first. Do not make the repository public.
2. Give your own AI permission to this repository under your own identity. A coding AI with local files, terminal and Git/GitHub support can execute this workflow. If you only have read/search access, it cannot truthfully claim or submit work; connect a tool with Git write access. Your browser permission does not automatically authorize an AI connector.
3. Clone the repository if no local checkout exists, otherwise pull main safely. Authenticate Git using an existing secure credential manager or your own interactive login. Never paste a token, password, AWS key or AI API key into chat or commit it.

```sh
git clone https://github.com/DiegoXue-coder/infs3701-cloud-team-2026.git
cd infs3701-cloud-team-2026
python --version
python scripts/setup_member.py --role D --install
```

Use Python3.9+ (some systems call it `python3`). D's setup creates a venv, installs only `tzdata` for coordinator time zones, and validates the task plan. It does not install the app, request AWS credentials or change progress. For subsequent commands choose `PY` as `.venv/bin/python` on macOS/Linux or `.venv/Scripts/python.exe` on Windows. These are path examples; do not literally run a placeholder named PY.

Run with that Python executable:

```text
PY scripts/team.py --user wyend12 doctor
PY scripts/team.py --user wyend12 join --role D
git pull --ff-only
PY scripts/team.py --user wyend12 start
```

`doctor` must report authenticated user `wyend12`, role D and readable files/tasks. An existing D binding makes join idempotent; it does not grant GitHub access. Missing rights or an identity mismatch must be resolved using your own account, not by impersonating Diego. If a connector fails but authenticated Git works, use Git and the helper; keep the repository private. No one else has verified your device's connection yet.

## Earlier report and evidence work (T25)

Read `AGENTS.md`, `AGENTS.en.md`, `project/config.json`, `project/handoffs.json`, `docs/four-person-plan.md`, the authoritative English assignment brief/rubric and the latest T25 Issue. Let your AI translate older Chinese material without changing its meaning.

Ask your AI to write a UTF-8 temporary file containing only `/team claim D` and run:

```text
PY scripts/team.py --user wyend12 command T25 --body-file PATH_TO_TEMP_FILE
```

Wait for the remote accepted receipt with owner `wyend12`. Then produce:

- A 500–700-word initial objective/design/limitations draft grounded in the actual workload.
- A requirement-to-evidence table: requirement source; evidence path/commit/time; what is proven; gaps; responsible member; review status.
- One consolidated technical-question list and a report outline integrating existing chapters with credit.

These outputs do not require the AWS service to be online. Then continue T19 report integration and T20 video/script work; each needs its own accepted task claim.

## Existing material and real limitations

- Original English brief/rubric: `sources/original/assignment/`; searchable extracted text: `sources/text/S12-*`, `S13-*`.
- Alex's chapter: `docs/b-design-report-draft.md`; app/run notes: `app/README.md`; original author and current limitations must be preserved.
- A's deployment/evidence: `docs/business-handoff-2026-11-07.md`, `docs/business-rollout-2026-11-07.md` and linked logs. Release06c2292 ran on two private EC2/Gunicorn hosts sharing DynamoDB. S3 holds the release archive, not the business records.
- C's independent observations: `docs/c-t12-cloud-validation-2026-11-07.md`; cost draft: `docs/c-t18-calculator-draft-2026-11-07.md`; existing video script: `docs/c-t20-video-script-2026-11-07.md`.
- B reported HTTP503 on 8 November at 15:35 Sydney and stopped before POST: `docs/b-t11-verification.md`. Cause unconfirmed. Last success on 7 November is not current health. Do not wait for repairs to draft/audit evidence.
- HTTPS, final business alarm/failure evidence, some assignment ambiguities and final artifacts remain pending. Only fictional data may enter the HTTP demo. No full-AZ failure was demonstrated.

## Finish a session and get a receipt

Save actual artifacts in your own files, such as `docs/d-objectives-draft.md`, `docs/d-evidence-matrix.md`, `docs/d-report-outline.md`, and a real review log under `evidence/T25/`. Log the sources actually read, checks performed, date, findings and limitations. Do not invent a deployment just to fill a log.

Your AI should create `deliveries/T25/YYYY-MM-DD-wyend12.json` using `templates/delivery.json` schema2, with genuine environment, checks/results, evidence, run_log, AI use and next step. Push artifacts safely to main, then report using a UTF-8 command file:

```text
/team report deliveries/T25/YYYY-MM-DD-wyend12.json
```

Pass that file to `PY scripts/team.py --user wyend12 command T25 --body-file PATH`. Use report for partial work, submit only when fully met. Read the actual receipt URL/status and ask a different member to inspect the completed result. English notes remain English in GitHub; each reader's AI can translate them. New receipts include English and Chinese status labels and preserve the original content; there is no automatic free-text translation service.

Before each session: pull main, run start, read your latest task/comments and continue existing work. Never force-push over someone else's work or automatically commit unrelated local files. The board is a synchronization snapshot, not a live AWS dashboard.
