# How three people jointly develop one AWS service

Current permission check: on 2026-10-31 it was confirmed that this Lab's Readme prohibits creating users or groups, so IAM accounts cannot be created for the two teammates. An entry point provided separately by the course awaits the tutor's reply. See the [check record](aws-access-audit.md). For now collaborate by the process below, executed by the approved environment holder.

## Settled and not yet settled

- Settled application: upgrade the member's own individual assignment Reading Tracker (Option A). The code entry point is `app/reading_tracker.py`.
- Your own Lab has been chosen and you are responsible for the actual configuration; the database approach and full deployment parameters are to be confirmed, and the balance needs re-reading each time. The current Lab prohibits creating users/groups, and a separately shared entry from teaching staff awaits confirmation.
- Choosing the old application does not require continuing to use the old EC2; the application's features can be kept while building or upgrading compliant networking, compute and data tiers in the chosen Lab. Whether to keep old resources should be decided after an inventory, without a Reset or deletion to "start over".

## Joint development and joint operation are two layers

GitHub shares the application, network configuration/scripts, tests, resource records and receipts; the final AWS environment runs one version of the service. The three individual Labs can be used for each person's permitted experiments, but the final demo is integrated in the chosen environment, and resources with the same name under different accounts cannot be assumed to be the same resource.

## First confirm with the course which access method is allowed

### If the course provides access to the same environment with several individual identities

Each person uses their own approved identity and operates according to their responsibilities. Maintain one shared resource list and agree deployment windows, to avoid changing the same network, database or instance at the same time. The application accesses AWS using the permitted role and temporary identity mechanism.

### If the individual Learner Lab does not allow such authorisation

Do not assume you can create three IAM users or cross-account roles. Configuration is executed by the final environment holder in the way the course allows; the other two provide code/configuration/tests and jointly operate, explain and verify on a shared screen.

This is still joint development by three people: A writes reviewable network/deployment configuration, B writes application/data code, C writes monitoring/test configuration; the environment holder executes the reviewed version, and does not design and hand-complete everyone's tasks on the spot. Personal passwords, access keys or session tokens must not be copied to other members.

## What the three can deliver at the same time

| Person | Independent work | How it enters the final environment |
| --- | --- | --- |
| A | VPC/subnet/security group/load balancer configuration, deployment scripts and architecture diagram | Reviewed scripts/configuration, applied by the approved operator in an agreed window |
| B | Reading Tracker, data layer, configuration variables, health endpoint, dependencies and start-up notes | A/the environment holder deploys the application at one commit |
| C | Request and failure test scripts, monitoring/alarm configuration, cost assumptions, evidence rules | After resources are available, fill in actual IDs/URLs and run real verification |

While the final Lab is not yet chosen, A can prepare templates with replaceable parameters, B develops locally, and C writes tests against a local fake service. Nothing is marked complete while the real AWS configuration or experiment has not happened.

## Fixed process for every AWS change

1. State on GitHub which part is being changed, the parameters, the execution method and the expected impact; another member checks.
2. Record in `docs/environment.md` the environment holder, region, current commit and resource list. Write only non-sensitive information.
3. The approved operator executes in the agreed window; the others do not change the same resource at the same time. Keep configuration in scripts/templates to reduce large amounts of repeated manual clicking.
4. Record the actual steps, results and screenshots/logs; feature or data changes are verified jointly by B/C.
5. Report through `/team report` or `/team submit` and obtain a receipt. Record the actual operator; contribution cannot be rewritten because the GitHub committer differs.
6. When something goes wrong, locate it from this change record and restore the last working version. Where database data is involved, prepare a separate backup/compatibility plan; saying "roll back the code" is not enough.

## Three things to do now

1. B does a first full local run check with the code already found, recording the configuration needed and the points to change.
2. A checks the candidate Lab's permissions, balance and existing resources, and proposes a workable deployment plan, without deleting the old environment first.
3. C continues preparing tests and evidence that fit the common interface, without waiting for A/B to finish everything.

The specific sharing permissions of the course Lab need confirmation from the tutor/lab instructions. For ordinary AWS, the principles of separate identities/roles can be found in the [AWS IAM official best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html), from which it cannot be inferred that the Learner Lab allows creating identities freely.
