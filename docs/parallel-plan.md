# Three-person work plan: you operate AWS, three workstreams advance together

**2026-11-08 update: this page's original three-person timeline is kept as history; the [four-person split](four-person-plan.md) is now used. D=wyend12 is responsible for T25, T19 and T20, and B/C's original work and authorship records are unchanged.**

Updated 2026-10-31; all dates are Sydney time and are suggested internal milestones, with no specific meeting times agreed yet. The formal deadline is 17 Nov 16:00. A plan is not a record of completion.

## People and responsibilities

| Person | GitHub role | Responsible for | Can start without waiting for anyone |
| --- | --- | --- | --- |
| You, DiegoXue-coder | A | The only approved actual AWS operator; network, instances, entry point, database resources, monitoring configuration, security, deployment and architecture diagram | Inventory and check the environment first; prepare the deployment path with a simple test page |
| Member two, yet to join | B | Application, data-access code, local start-up, database fields, application chapter and report integration | The old source exists; first provide a local development mode that needs no AWS credentials |
| Member three, yet to join | C | Executable tests, monitoring parameters and verification method, cost, evidence, video integration | Write tests, a request-logging tool and expected results from the existing code and fictional data |

A/B/C are task labels and do not indicate work order. The original binding of the user as B was migrated to A, and historical receipts and past actual contributions are not rewritten. The two members' usernames are still missing, and they have not been invited or impersonated in a claim. Accept the invitation on GitHub and open the source first, then begin formal collaboration.

## What the outline says about collaboration

Page 3 of the assignment brief, Working as a Team: everyone must contribute, with a suggested split by networking, compute/data tier, security, monitoring and written deliverables; the independent contribution statement must be signed off, and individual marks may be adjusted for clearly uneven contribution. Page 4 only explains the steps for entering the Learner Lab with a student account. The outline and marking sheet do not clearly say how three people can sign in to the same Lab at once, share an account or create teammate identities, nor do they require everyone to click in the console directly.

The current Lab Readme prohibits creating users/groups, see [permission check](aws-access-audit.md). If the course has a separate group access entry, the tutor needs to confirm it. The split follows the suggested direction, which does not mean the course has additionally approved a specific way of identity access.

## Four things to finish tonight (suggested 30 minutes)

1. Provide the other two people's GitHub usernames; you invite them and they accept; each confirms they can open `app/reading_tracker.py` and the task cards; do not say everyone is connected just because you can open them.
2. Fix a small scope: keep reading records and statistics, first complete two AZs, two instances/load balancing, a shared managed database, monitoring and encryption, and add no complex business features.
3. A/B/C take 10 minutes to confirm the port, start-up, data format, health path and instance identification in `docs/interfaces.md`; draft values still need explicit confirmation.
4. Each person claims a first task and agrees the first integration window on 2 Nov, with the exact time set from timetables. B delivers a minimal runnable version first, without waiting for all the changes.

## Phased schedule: all three deliver real results in every phase

| Suggested time | You, A: AWS | B: application | C: testing, monitoring, cost | Checkpoint for the phase |
| --- | --- | --- | --- | --- |
| 31 Oct–1 Nov | Inventory old resources and balance; check database, network and HTTPS feasibility; draw a first draft; prepare a minimal deployment environment | Pull the code, tidy dependencies; add a local data mode clearly labelled for development; deliver the start command, sample data and a first interface note | From the old code deliver three data sets with expected statistics; write executable statistics tests and a configurable request-logging script; actually run local checks | Three viewable results, with no blank documents counted as deliveries; recorded failures also count as real progress |
| 2–3 Nov | Create the chosen database and the first application host; deploy B's specific commit; check the role and access path | Write the managed-database read/write code; adjust configuration to A's non-sensitive parameters; deliver migration/table-creation requirements and verification steps | Write insert/query/restart cases in advance; verify scripts locally; run the first round and report problems as soon as the URL arrives | One version can really write to and read back from the cloud database; if it fails, fix core first |
| 4–6 Nov | Second AZ, second instance and load balancing; configure CloudWatch from the parameters C already gave | Ensure both hosts run the same version and share the database; add health and instance labels; fix problems C finds | Run two-instance read/write and routing checks; check monitoring metrics; prepare alarm trigger/recovery steps; update cost assumptions | Both healthy, one set of data, and requests can be traced to a host |
| 7–10 Nov | Run failure, alarm and recovery in the agreed window; fix network/security; save resource parameters | Fix application/data problems; write the reasons for application choices and reproduction notes | Send continuous requests and count failures/recovery time; save alarm and recovery evidence; check encryption and permissions; formal cost estimate | Core requirements have real evidence; a stop-instance test is not passed off as a full AZ failure |
| 11–13 Nov | Finalise the architecture diagram and AWS configuration chapter; help with the demo | Integrate each of the three people's chapters; have others check the run instructions | Integrate tests, cost and video; produce at 60 seconds first, with the length conflict still to ask the tutor | First versions of all five deliverables complete, each matching a real version |
| 14–16 Nov | Check the cloud against the diagram and make final necessary fixes | Fix text, references, code and steps | Cross-check evidence, video and files; each person's independent contribution sign-off | Internal final version on 16 Nov, leaving one day of buffer |
| Before 17 Nov 16:00 | The designated submitter uploads and saves the receipt; handle resources as the course confirms | Check the uploaded files and versions | Check the submission opens and is complete | Formal submission succeeds; clicking upload is not treated as success |

These windows do not require being online all day. Joint checks of 30–45 minutes are suggested on 2, 6, 10 and 13 Nov, adjusted to the three people's actual timetables. Start resources on demand only before multi-person experiments; evidence, recording and resource-retention arrangements follow the course's answer, and a full set of resources cannot be left running long-term just to wait.

## Each person's first delivery: can be finished before deployment

- **A (T05/T06)**: environment inventory, budget reading and time, two-AZ network sketch, limitations and deployment steps. A simple test page can be used to check the environment first, without waiting for all the business code changes.
- **B (T04/T07)**: start from `app/reading_tracker.py`; deliver dependencies, a reproducible start method, a local data mode and field conventions. The source exists now, but the old S3 dependency means running without credentials cannot yet be promised; that development mode is still to be implemented by B. Local data is for development only and does not satisfy cloud database acceptance.
- **C (T08)**: three fictional reading data sets with expected totals/pages/ratings; executable statistics tests; a request-recording script that reads BASE_URL with local run records; a draft of specific monitoring parameters. A checklist alone or waiting for screenshots is not enough.

C can read the old code directly and write statistics tests first, without waiting for B's full web page. Final acceptance of web feature tests and real failure tests still needs a working application and AWS environment, so it cannot be called completely free of dependencies.

## Hand over a small piece each time, without waiting for the whole item

B to A: code commit, dependencies, start command, environment variable names, port, health path, database table-creation requirements. No session keys.

A to B/C: deployed commit, non-sensitive URL, database resource name/region, port, current limitations. Without a real address use a variable first and do not fill in an invented URL.

C to A: specific monitoring metrics, dimensions, statistical period, threshold reasoning, trigger/recovery steps, and the verification script to be run; A should be applying a reviewed configuration and need not design C's work from scratch.

C to B: input, expected result, actual result, reproduction steps and logs. Environment problems go to A, application problems to B, and C retests.

Configuration changes are recorded in `interfaces.md` and the task card; each of the three writes the design reasons, trade-offs, steps and limitations for their own part, and B only integrates the report without writing everyone else's content.

## How to avoid queueing when you are the only AWS operator

1. Whoever needs a cloud operation first lists on the card the specific resource, parameters, command/click steps, expected impact, verification and restore method, checked by another person.
2. Each day, as your time allows, handle one batched 20–30 minute operation window, completing compatible changes together where possible. There is no need to be online at all times for small requests; long experiments get a separate window.
3. While waiting for a window, B continues local code and unit verification; C continues scripts, cost and evidence checks. When blocked, pause only the blocked sub-item, not the whole workstream.
4. You operate the shared resource; guidance, design and verification are each recorded as actual contributions. Monitoring configuration and database resource creation both count as your actual operation, while the plan/code contribution still belongs to B/C.
5. When requests exceed the window, first resolve the smallest parameters/resources that affect later integration; add no enhancements or new features before core passes.

## Daily GitHub rules

Read the latest task → claim your own role → keep the current usable artefacts and real execution records → merge into the default branch → `/team report` for partial results, `/team submit` for complete results → review by another account.

Each time record "what was done, where the files are, how it was verified, what is still missing, who does the next step". The start condition `start_after` and the completion condition `depends_on` remain separate, and final acceptance dependencies cannot be skipped. GitHub chat sync is not automatic AWS monitoring; CloudWatch is what handles runtime metrics; without configuration, real-time monitoring cannot be said to be live.
