# At the end of each work session, have your AI report and get a receipt

## All a teammate needs to say

> Organise the operations, tests and evidence I actually did this time, and help me upload them and get a receipt. Record honestly what is not finished, and tell me the next step and who needs to check.

The AI acts according to this repository's AGENTS.md, the member's identity and the task card. Network access, GitHub write permission and usable local tools are prerequisites; when offline or without permission it says clearly "not reported" and must not pretend in chat that the remote succeeded.

## What each report leaves behind

| Item | Specific content |
| --- | --- |
| Who, which item, when | GitHub user, T number, actual time with time zone |
| Where it was done | Local/test/real AWS, region and a non-sensitive environment description |
| What was done | Steps, actual commands, start/end and exit code, or a record of real console operations |
| What the result was | Expected, actual, pass / fail / partial |
| Where the evidence is | Real repository paths of screenshots, logs, configuration, code or documents |
| Which version | The system records the commit at delivery time, the delivery file and the evidence version |
| What is still not done | Limitations, errors, next step and whose help is needed |
| Who checks | Another GitHub user's review comments and receipt |

Not every item needs a screenshot, but **every structured report must have an actual execution/check record**. Report-writing tasks also record which materials and content were actually checked, and must not pretend an AWS experiment was run.

## The AI's actual order of operations

1. Confirm the member has claimed the task and read the latest state; in the preparation stage, the completion gate does not block.
2. Keep logs while carrying out authorised operations. Terminal commands can be wrapped with `scripts/capture_run.py`; it records time, command, exit code and standard output/error, and does not record the whole environment.
3. With browser capability and permission, save real screenshots; when only the member can operate, ask them to provide screenshots and note the actual operator. Generated images or old images must not be passed off as this session's operation.
4. Fill in actual data following version 2 of `templates/delivery.json`, and upload the JSON, execution record and evidence to the default branch. The AI handles the format, and members are not asked to fill in JSON by hand.
5. Use **report** for partial completion/failure; use **submit** when the task requirements are met. Both generate receipts; report does not mark complete, and submit enters awaiting check.
6. Another member approves or requests changes after actually checking. A fail/partial test result, changed evidence files or self-approval cannot pass completion.
7. After synchronising, check the receipt number in the Issue and the latest report record on the dashboard; tell the member "reported" only after confirming success.

## Reporting and completion are separate

```text
/team report deliveries/T07/<date>-<own name>.json    Partial results, preparation work or failed tests; stays in progress/blocked
/team submit deliveries/T07/<date>-<own name>.json    Full delivery; enters awaiting check
/team approve <what was actually checked and the result>            Completed after another person verifies
/team changes <specific defect or evidence to add>          Sent back for changes
```

The completion gate does not block report, so A, B and C can all keep reporting their independent results without waiting for someone else's whole card to finish. If there are screenshots but the test was not done, the result should be partial; a discovered failure is written honestly as fail, and the report itself can still succeed.

## Example execution-record command

```text
python scripts/capture_run.py --task T07 --actor <own username> --output evidence/T07/<date>-run.log -- python -m unittest discover -s tests
```

Wrap only operations that are already authorised; using the recorder grants no new permission. Check for sensitive information before uploading; the recorder masks some common credential forms but cannot be guaranteed to recognise every secret. AWS keys, session tokens or passwords must not be entered into shared material.

## How receipts are traced

- Numbers look like `R-T07-<comment ID>`, with one receipt per report request.
- The Issue comment shows the operator, operation, processing result, status change and corresponding version; report-type receipts attach the delivery, execution record and evidence links.
- `data/receipts.json` is the collection of all machine-readable receipts, and `DASHBOARD.md` shows recent records. The original source is still the Issue and the pinned-version delivery file.
- Old plain receipts are marked legacy, and structured state that was not recorded in the past is not fabricated.
- If the task state was saved but sending the receipt was interrupted, the next sync resends it; the same request is not executed twice. Do not redo a claim by deleting comments.

## Current sync boundaries

GitHub background Actions is still paused, so each member's AI must run the sync helper at the end of the chat. Saying "done" only in chat, or uploading only a local file, does not report automatically. When the tool cannot run, the teammate must be told who will do the sync.

A receipt proves "who reported which version and what was checked"; alone it cannot guarantee that AWS stays healthy. Joint deployment, shared data, failure and alarm still need real verification; execution records are the basis for finding problems and rolling back.
