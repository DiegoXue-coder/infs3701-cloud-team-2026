# Reading Tracker weekend handoff

**Current handoff, 14 November.** Tenzi deploys in his Lab under [T26](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues/26) and completes the video alone under [T20](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues/20). Diego exports the [Draw.io source Tenzi delivered](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues/17#issuecomment-6872968721) to a readable one-page PDF and integrates Figure 1.

The [one-page replacement architecture PDF](../output/pdf/reading-tracker-replacement-architecture.pdf), [editable Draw.io file](../output/pdf/reading-tracker-replacement-architecture.drawio) and [report image](../output/pdf/reading-tracker-replacement-architecture.png) are ready for review. They adapt Tenzi's redraw to the replacement CloudFormation template, including the shared private route table and scoped S3 access. Use the caption “Figure 1. Reading Tracker architecture for the replacement Learner Lab, based on the CloudFormation template.” After T26, compare the deployed region, Availability Zones, ports and resource types against the diagram before updating the caption. Use the archived AWS logs as dated evidence from the original Lab.

Use the [shared report](https://docs.google.com/document/d/1skzD5LWhF6BnX8TDrMVxz39r37WKdVzXbseMskMbcxw/edit) for team edits. Marina owns the [cost PDF](../output/pdf/reading-tracker-12-month-aws-cost.pdf) and the report's cost and monitoring sections. Alex owns the application and verification sections. Confirm each person's actual contributions and AI use before signing the individual statements. Check the official cover sheet, all four signatures, report and diagram PDFs, cost PDF, playable video and Moodle requirements before submission.

| Person | Start before deployment | Once the new endpoint works and both targets are healthy |
| --- | --- | --- |
| Tenzi | Run the T26 preflight and rehearse the solo section of [Marina’s script](c-t20-video-script-2026-11-07.md). | Record the live fictional write, readback and request distribution. Narrate live or record the voice-over later. Edit and deliver the final video yourself. Save the CloudWatch and target evidence for Marina. |
| Diego | Review the deployment plan, export Figure 1, prepare references and collect everyone’s AI-use notes. | Check the figure and report against the actual deployment, assemble sections and finalise the submission package. |
| Alex | Complete the application and DynamoDB section and prepare the independent test. | Verify the write, readback and both labels when the endpoint is available, save the log under T11, and finish the report results and evidence links. Help Diego check the package. |
| Marina | Finalise the cost PDF and draft the cost and monitoring report sections. | Use Tenzi’s timestamped AWS captures and Alex’s logs to complete the report. Check the video claims and help Diego check the package asynchronously. |

Use the [replacement Lab guide](tenzi-lab-redeployment.md). Tenzi chooses his own recording time once the application works and both targets are healthy. Post the new URL, fictional record title and expected endpoint availability in T26 so Alex can test independently. Save the recording and evidence before course-directed cleanup. The original plan follows below.

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
