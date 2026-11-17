# First-time joining: do it once, then just talk to your AI

**Current four-person entry points:** [self-service](self-service.md), [D English setup](member-D.md), [English prompt](../prompts/START-en.md). A/B/C/D are already reserved in config, and Tenzin does not use the historical B/C vacancy role-selection process below. A role does not mean access or that the member's own connection is verified.

The full self-service setup, role selection and copyable AI opening prompt are at the [self-service entry](self-service.md). Before the split is settled, the two members can join first and then each choose B/C.

## Project owner

1. Keep the repository Private and do not enable public Pages. Confirm that those joining are real teammates entitled to access the course materials.
2. After obtaining a teammate's GitHub username, send an invitation through the repository's Settings → Collaborators, which the teammate accepts themselves. Do not share accounts.
3. No manual B/C binding is needed. After accepting the invitation a teammate runs doctor to see the vacancies, chooses, and has their AI run join --role B or C; the same role cannot be overwritten, and each person can hold only one.
4. If the starting service or database changes, record the reason in `docs/decisions.md` and update the configuration; do not let each person's AI choose a different approach.

## Each teammate

1. Accept the repository invitation with your own GitHub account and confirm you can open the README and Issues.
2. It is recommended to have an AI with terminal capability open a local clone of this repository, confirm Python 3.9+ runs, and use your existing Git/gh authorisation. The sync helper tries, in order, the current process's GH_TOKEN, your gh login or Git credentials, and stores no secrets. No AI API key needs to be committed to this repository. If you use a connector, you must make sure it can access this new private repository; the existing connection in Codex does not currently include the new repository.
3. Give the AI the first-time opening prompt from `prompts/START.md`, filling in your own GitHub username. The AI should report the role it read from the configuration. If Windows Python reports missing time-zone data, have the AI install `tzdata` in that environment and retry; Sydney time must not be guessed as the computer's local time.
4. First complete the local setup, doctor and join as in self-service; then have the AI run `python scripts/team.py --user <own username> start` and claim with the command function; start only after seeing the system receipt. If access fails, resolve the connection permission first and do not let someone else sign for you.
5. Operate AWS only if you have access; otherwise arrange a shared screen with the final environment holder, submit the steps and verify together.

## With chat only and no GitHub tools

The AI can explain tasks but cannot synchronise automatically. You copy the command into a task comment and upload the delivery yourself, then ask a member with terminal capability and repository write access to run the sync; the command is still validated against the original commenter's identity and cannot be signed for someone else. Until GitHub Actions is restored, immediate automatic execution after a web comment is not promised. Do not claim that ordinary chat can manage the repository automatically from a private link alone.

## Joining items not yet complete

B/C usernames are still to be provided; no new members have been invited yet. The starting service is settled as Reading Tracker, and the Lab holder is designated as DiegoXue-coder. Missing course materials are listed in the material index.

## Connection self-check that does not change progress

Have the AI run `python scripts/team.py --user <own username> doctor` in the local clone. It only reads identity, materials and tasks, and does not claim or complete tasks. The full method is in [connection-test.md](connection-test.md), and the online role entry is [LIVE_BOARD.md](../LIVE_BOARD.md).
