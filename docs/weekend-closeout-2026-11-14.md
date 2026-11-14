# Reading Tracker weekend handoff

**Recovery update, 14 November.** Tenzi deploys in his Lab under [T26](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues/26) and leads the English recording under [T20](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues/20). If he has started the Draw.io diagram, he can finish that draft and share it in [T17](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues/17). Otherwise Diego finishes the drawing. Diego checks and integrates Figure 1 in either case.

| Person | Start before deployment | Once the new endpoint works and both targets are healthy |
| --- | --- | --- |
| Tenzi | Confirm the diagram status in T17, run the T26 preflight, rehearse Marina’s script and test screen/audio recording. | Record and narrate the live demo in English. Capture a fictional write and readback, then show real routing or availability evidence. |
| Diego | Review the change set and draft report updates against the template. Prepare the final package checklist, cover sheet and contribution evidence. Prepare Figure 1 for integration using the existing draft. | Confirm the diagram, URL and protocol against the deployed environment, then integrate the verified results and export the final report. |
| Alex | Review report §3 and rehearse the test with the local application. Prepare the exact command and fictional record values. | Independently verify the write, readback and both instance labels while Tenzi records. Save the log under T11. |
| Marina | Finish the cost PDF against the template assumptions, check existing Lab spend with Tenzi, and prepare dated CloudWatch evidence and the video shot list. | Capture current CloudWatch/target evidence and check the final video. Update costs only if the deployed configuration differs. |

Use the [replacement Lab guide](tenzi-lab-redeployment.md) for the live session. Begin recording when the service is healthy and the first read/write works. Alex’s independent check and Marina’s evidence capture can run during the recording window. T26 records the deployment and raw footage. T20 records the final cut. The original plan follows below.

Diego confirmed the work split below for 14–15 November 2026, Sydney time. The targets are suggested and the shared lab session time is pending. The official deadline in the brief is 17 November at 16:00 Sydney.

| Person | Deliverable | Suggested target |
| --- | --- | --- |
| Diego | Restore the AWS demo, lead the shared test and record the 60-second video. Check Learner Lab, both EC2 instances and ALB target health. Review the final diagram and integrate the reviewed report sections. | Confirm a Saturday session and assemble a draft video by Sunday evening. |
| Alex | Review the application and DynamoDB section of the report. During the lab session, repeat the independent test, add one fictional record and read it from both instance labels. Save the execution log and help Diego capture the browser demonstration. | Return report comments and the test log or exact blocker by Saturday evening. |
| Marina | Complete the one-page 12-month cost PDF based on the Pricing Calculator draft. Record the assumptions and verify the total against the architecture. Review the existing CloudWatch business alarm and routing evidence, and prepare the matching video clip or screenshot. | Return the cost PDF and evidence review by Sunday evening. |
| Tenzi | Redraw the architecture with AWS icons and English labels, using the evidence and existing reference. Return the editable Draw.io source and a readable one-page PDF for Diego to check. | Share a first pass by Saturday evening and the reviewed version by Sunday evening. |
| Everyone | Use GitHub activity and evidence to draft the contribution table. Each member confirms their actual work and AI use, agrees the share with the group, and signs their own statement. | Have the statements and group cover sheet ready for Monday's final check. |

Tenzi prepares the drawing under T17 and Diego reviews it as the task owner. Alex continues T11. Marina can record her own claim on T18 when starting the cost PDF. The assigned work here records Diego's decision. Individual acknowledgements and GitHub task claims are tracked separately.

## Live session and recording

A read-only request to the public `/health` endpoint on 12 November at 17:54:59 Sydney returned HTTP 503 from the ALB without an instance label. The cause is unverified. Diego checks the Lab session, EC2 states and target health. Once the business endpoint responds and both labels are visible, Alex can proceed with the [existing independent verification procedure](b-t11-verification.md). Use a single fictional write in the test and capture its actual readback from both labels.

Use Marina's [video script](c-t20-video-script-2026-11-07.md) and aim for around 60 seconds. Capture the live browser session first, including the fictional record being saved and retrieved. Then show both instance labels from actual requests, explain how the two EC2 instances share DynamoDB, and show the verified CloudWatch evidence if it fits. A repeat instance-stop experiment can be scheduled separately if the team wants additional evidence. The brief gives observed request distribution across instances as one example of a suitable demonstration.

## Monday packaging check

Open the design report PDF, separate architecture PDF, separate 12-month cost PDF and playable video. Check that the architecture diagram and report describe the same verified deployment. Include the required contribution statements, cover sheet and code using the current Moodle instructions. Confirm which member uploads and who independently checks the submission receipt.

References: [assignment requirements](assignment-requirements.md), [report review PDF](../output/pdf/reading-tracker-design-review.pdf), [architecture reference](architecture-review-2026-11-11.md), [Marina's cost draft](c-t18-calculator-draft-2026-11-07.md), and [monitoring evidence](monitoring-reconciliation-2026-11-10.md).
