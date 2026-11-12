# Reading Tracker weekend handoff

Proposed team milestones for 14–15 November 2026, Sydney time. The official deadline in the brief is 17 November at 16:00 Sydney. Each member should reply with availability for a shared lab session and confirm their deliverable.

| Person | Deliverable | Suggested target |
| --- | --- | --- |
| Diego | Coordinate the AWS session and video. Check Learner Lab, both EC2 instances and ALB target health. Confirm both targets and the business page before recording. Review the final diagram and integrate the reviewed report sections. | Confirm a Saturday session and assemble a draft video by Sunday evening. |
| Alex | Review the application and DynamoDB section of the report. During the lab session, repeat the independent test, add one fictional record and read it from both instance labels. Save the execution log and record the browser demonstration. | Return report comments and the test log or exact blocker by Saturday evening. |
| Marina | Complete the one-page 12-month cost PDF based on the Pricing Calculator draft. Record the assumptions and verify the total against the architecture. Review the existing CloudWatch business alarm and routing evidence, and prepare the matching video clip or screenshot. | Return the cost PDF and evidence review by Sunday evening. |
| Tenzi | Redraw the architecture with AWS icons and English labels, using the evidence and existing reference. Return the editable Draw.io source and a readable one-page PDF for Diego to check. | Share a first pass by Saturday evening and the reviewed version by Sunday evening. |
| Everyone | Confirm actual contributions and AI use, and prepare the signed individual statement and group cover sheet as the course requires. | Have the statements ready for Monday's final check. |

## Live session and recording

A read-only request to the public `/health` endpoint on 12 November at 17:54:59 Sydney returned HTTP 503 from the ALB without an instance label. The cause is unverified. Diego checks the Lab session, EC2 states and target health. Once the business endpoint responds and both labels are visible, Alex can proceed with the [existing independent verification procedure](b-t11-verification.md). Use a single fictional write in the test and capture its actual readback from both labels.

Use Marina's [video script](c-t20-video-script-2026-11-07.md) and aim for around 60 seconds. Capture the live browser session first, including the fictional record being saved and retrieved. Then show both instance labels from actual requests, explain how the two EC2 instances share DynamoDB, and show the verified CloudWatch evidence if it fits. A repeat instance-stop experiment can be scheduled separately if the team wants additional evidence. The brief gives observed request distribution across instances as one example of a suitable demonstration.

## Monday packaging check

Open the design report PDF, separate architecture PDF, separate 12-month cost PDF and playable video. Check that the architecture diagram and report describe the same verified deployment. Include the required contribution statements, cover sheet and code using the current Moodle instructions. Confirm which member uploads and who independently checks the submission receipt.

References: [assignment requirements](assignment-requirements.md), [report review PDF](../output/pdf/reading-tracker-design-review.pdf), [architecture reference](architecture-review-2026-11-11.md), [Marina's cost draft](c-t18-calculator-draft-2026-11-07.md), and [monitoring evidence](monitoring-reconciliation-2026-11-10.md).
