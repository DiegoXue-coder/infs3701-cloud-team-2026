# How to test whether the GitHub connection works

## First test whether you can open it yourself

If all three links return 404, first sign in as DiegoXue-coder in the same browser as described in [access-404.md](access-404.md); a Git tool's sign-in state is not the browser's sign-in state.

Sign in with your own GitHub account and open the [repository home page](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026), [material index](../sources/INDEX.md), [online task entry](../LIVE_BOARD.md) and [T01](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues/1). If they open, web reading works; other teammates must accept the repository invitation first.

## Then test your own AI

Give the AI the following paragraph:

> Please run a read-only connection test: do not claim, do not complete tasks, do not change AWS. Read this repository's README, sources/INDEX.md and project/config.json, and the latest body of T01 on GitHub. Tell me the repository name, number of materials, my role and T01's current status that you actually read; if you have no access, report the error clearly and do not answer from chat history.

Being able to read files does not mean being able to write progress; a readable web page does not mean the AI connector has been granted access. If the web page opens but the AI returns 404, first check the account the AI uses and the repository authorisation scope; there is no need to make the repository public.

## An AI with terminal capability can run a read-only self-check

In the local clone directory of this repository, run with your own username:

```text
python scripts/team.py --user DiegoXue-coder doctor
```

Other members substitute their own GitHub username. The self-check only reads identity, role, materials, task cards and workflow state; it creates no sync lock, posts no task comment, does not refresh the dashboard and claims no task. After the four-person configuration update and the creation of T25 you should see: `source_files: 21`, `task_cards: 25`, your user and role, and each read check as true. A role reservation does not mean the member's connection has passed. D follows the [English setup](member-D.md) and must use wyend12's own identity.

The local Git/REST route and the Codex GitHub connector are two different connections. On 2026-11-04 the holder approved and saved connector access for this repository, and the DiegoXue-coder connector actually read the configuration and T08 successfully; the holder's old 404 problem is fixed. Marina and other members still need to retry their own connections; a successful local doctor or the holder's success cannot be treated as your own plugin having passed. See [this authorisation record and C's resume steps](2026-11-04-connector-access.md).

## Testing "can it synchronise"

After the first read-only test passes, you can have the AI send `/team status` on T01, processed through the sync helper, and check the new "task sync receipt" in the Issue and the dashboard time. This command queries status and does not mark course tasks complete.

```text
python scripts/team.py --user DiegoXue-coder command T01 --body-file temporary-command.txt
```

temporary-command.txt contains the single line `/team status`. Do not write passwords or tokens in it. For upload tests use only ordinary test records, not real course work passed off as complete.

## What counts as success

1. The information the AI reports really comes from this remote read.
2. The sync command receives a receipt, instead of only saying "updated" in the local chat.
3. Another teammate with permission opens the same task and sees the same status and comments.
4. Screenshot/configuration/report originals can be opened from the material or delivery links.
