# Four-person self-service entry

**Tenzin / wyend12: use [the complete English setup](member-D.md) and [English start prompt](../prompts/START-en.md).** Accept your own invitation and authorize your own GitHub/AI; no AWS password or AI API key is needed.

Current roles A=DiegoXue-coder, B=Alex4325Li, C=Marina057, D=wyend12. The latest split is in [four-person-plan.md](four-person-plan.md). D is reserved and needs the member to accept the invitation and verify his own connection; role assignment does not mean access, claiming or contribution is complete.

D runs setup_member.py --role D --install, which installs only the coordinator's time-zone dependency, then uses his own GitHub identity for doctor, join --role D and start; the first item is T25, then T19/T20. A claim must have a remote receipt and cannot be made on his behalf. Follow the full commands and real delivery rules in the English guide.

New D tasks are in English, new receipts include bilingual labels, the original free text is kept, and each person's AI can translate. The original B/C role-selection record below is kept as history and cannot be used to overwrite the current four-person reservations or to have Tenzin take over B/C.

---

## Original B/C self-service joining process (historical record)

The repository owner has chosen A=DiegoXue-coder to operate AWS, B to do the application, and C to prepare testing and monitoring. This note and `project/handoffs.json` are the single entry point. Pull the latest version when acting, and do not wait for the owner's verbal reply item by item.

## One-time prerequisites

The owner needs to obtain the two real teammates' usernames and invite them to this private repository, or have the authorised person accept an existing invitation. This step is not yet done; without access, no opening prompt can make an AI read private code. A role is a division of work, not an AWS permission.

Each teammate accepts the invitation personally, installs/signs in to GitHub tools on their own computer, and uses an AI with local terminal, file and GitHub capability. Their own account, verification and authorisation are done by them; there is no need to ask the owner for AWS keys, an AI API key or personal passwords. Ordinary chat without tools cannot execute automatically.

## When the two have not yet split roles

After accepting the invitation both use this same page; each person's AI first runs doctor to see the B/C vacancies, and the member chooses. Whoever claims successfully first takes the role and the other chooses the remaining one, with no need for the owner to edit the configuration by hand. An enrolled member cannot be overwritten.

## When application role B is chosen

> You are responsible for the Reading Tracker application and data code. After accepting this repository's invitation, sign in with your own GitHub, have an AI with terminal capability clone the repository, and give it the whole paragraph below. Repository: https://github.com/DiegoXue-coder/infs3701-cloud-team-2026 . Please set up and start work by yourself following docs/member-B.md, without waiting for me to explain separately.

## When testing role C is chosen

> You are responsible for the test tools, monitoring plan, cost and evidence. After accepting this repository's invitation, sign in with your own GitHub, have an AI with terminal capability clone the repository, and give it the whole paragraph below. Repository: https://github.com/DiegoXue-coder/infs3701-cloud-team-2026 . Please set up and start work by yourself following docs/member-C.md, without waiting for me to explain separately.

## Opening prompt for the two members to copy to their AI

> I am a member of this group, my GitHub username is [fill in own username], and the split is not yet settled. Please first run doctor to see the vacant roles, explain to me the difference between B (application) and C (testing), and let me choose; if already enrolled, continue with my role. Please carry out this repository's AGENTS.md and docs/self-service.md directly: check my identity and private-repository permission, read the matching member document, set up the local environment, run the baseline check and complete doctor; if the role is not enrolled, run join --role to bind me to my vacant role, then synchronise and claim the first task. Use the settled development parameters in project/handoffs.json and do not ask the owner to send code or verbal parameters again. Help me complete a first verifiable result, save real records, report and get a receipt. When cloud values are missing, continue independent local work and record precise requests on the task card; do not guess AWS results, approve on my behalf or ask for shared credentials. When authorisation is insufficient, installation fails or roles conflict, explain the real obstacle and first troubleshoot what can be solved on my computer.

## Order of AI execution

1. Clone the repository or pull the default branch with the member's existing GitHub authorisation; first read AGENTS, the current role guide, handoffs and the latest Issue.
2. Check Git and Python 3.9+; a missing runtime is handled by the member/tool, without asking the owner to install it remotely.
3. Run `python scripts/setup_member.py --role B --install` (use C for C). It creates a separate .venv, installs the app dependencies and tzdata, and runs the offline old-code check. Later commands use that virtual environment's Python: `.venv/Scripts/python.exe` on Windows, `.venv/bin/python` on macOS/Linux.
4. Run `python scripts/team.py --user <own username> doctor`. If the repository cannot be read, first check the member's account, invitation acceptance and authorisation scope; do not make the private repository public.
5. Run `python scripts/team.py --user <own username> join --role B` (use C for C). Only the member with existing repository write access may join a vacant B/C; it cannot overwrite others, hold two roles or take over A. Joining the same role again does not change the configuration again. The record uses a server-side lock and file SHA to stop the same vacancy being overwritten by normal concurrent flows.
6. join updates the role and dashboard; then pull the latest code and read the latest tasks. B's first item is T04 and C's is T08; if completed, continue by the role guide, if claimed, carry on, and do not take a task already claimed by someone else.
7. Send `/team claim B` or C through the existing command function and act only after seeing the remote receipt. The AI generates the temporary command file, and members need not fill in JSON by hand; see docs/team-protocol.md.
8. After completing the current smallest result, generate the real delivery, execution record and AI note, merge into the default branch, then report/submit and confirm the receipt. The next person gets the result and specific next step through GitHub.

## How to hand over without verbal replies

Parameters are as in handoffs.json and the environment record, and the latest task comment explains temporary limitations. To change a development convention, submit a file change and state its impact; do not each guess.

In the first round B delivers the local version, data format and start-up notes; at the same time C writes tests and the request-logging tool against the old code. Empty cloud fields do not block starting on day one; final verification of the managed database, real two instances, alarm and failure must wait for A to provide real resources.

When A's action is needed, write in the relevant task Issue: task, configuration/script path, version, resource, parameters, expectation, check and restore method. A reads and handles it the next time he starts work with his AI. There is no resident background process or AWS executor, nothing deploys automatically while A is offline, and A is not required to answer each item in private chat.

## Current scope of verification

Self-service enrolment has automated tests and the setup script has local offline checks; no two other real accounts have yet completed a first join, so it cannot be claimed that everyone has accepted. Installing dependencies, the member's own GitHub connection and the local environment may still need to be handled by that member. Screenshots/logs must be from real operations and are finally checked by another person.
