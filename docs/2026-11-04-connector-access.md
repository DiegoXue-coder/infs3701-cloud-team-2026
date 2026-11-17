# 2026-11-04 Connector authorisation and resuming Marina's submission

Diego explicitly approved in chat: add only DiegoXue-coder/infs3701-cloud-team-2026 to the existing ChatGPT Codex Connector, keep the repository private, and keep the original authorisation for second-brain.

After actually saving, GitHub displayed "Okay, ChatGPT Codex Connector was updated". The option is still Only select repositories, covering the two repositories above. This installation already had read/write permission for code, Issues, PRs, Actions and workflows; this change applied those existing permissions to the team repository, and All repositories was not selected.

## Actually verified

- Reading the team repository's metadata through the GitHub connector, using the DiegoXue-coder connection, succeeded, visibility=private.
- Reading project/config.json by the same route succeeded; the file SHA was 2369430a6095f2c17d793baab476dc69e3829676; at the time A=DiegoXue-coder, B=Alex4325Li, C=null.
- Reading the real T08 (Issue 8) by the same route succeeded, status todo, owner=null.
- Saved screenshot: [GitHub success message and selected scope](../evidence/T02/2026-11-04-connector-access-saved.png).

This shows the holder's installation scope is now complete and the current holder's connector 404 is resolved; Marina's AI connection was not signed in to or verified, and her upload or claim was not simulated.

## What Marina's AI does next

1. Keep the existing test data, scripts, original logs of the 17 tests and drafts; do not overwrite the original work with a fresh clone. Check the Git status of the current folder first.
2. Retry reading README, AGENTS, project/config.json and Issue 8 using Marina057's own GitHub connection. If it still fails, check which account is connected; her existing Git login can be used to read/clone the repository without waiting for the plugin.
3. Complete the read-only doctor as described in docs/self-service.md; while C is vacant, she herself runs `python scripts/team.py --user Marina057 join --role C` and re-reads to confirm enrolment. Diego must not run this under Marina's identity.
4. Send `/team claim C` to T08 through the same helper's command subcommand, obtain the receipt, then upload the organised delivery. Record the work already done honestly as local preparation before enrolment, and do not alter test dates.
5. Put the real scripts, data, run records and drafts in the appropriate directories, and use templates/delivery.json to record environment, expected, actual, limitations and evidence paths. The 17 tests are Marina's report and need original logs/actual review to support them; do not replace the repository's existing tests or write a local pass up as an AWS pass.
6. After merging into main through the normal Git process, send `/team report deliveries/T08/<actual filename>.json` under her own identity; submit only when T08's requirements are fully met, and wait for another member's independent check. Keep the cloud verification still to be done and the draft status as they are.

For identity checks, the virtual-environment path and full commands use the repository's existing self-service entry; do not share account passwords, tokens or AWS credentials. This permission fix does not mean T08 is complete and does not restore the paused GitHub Actions.
