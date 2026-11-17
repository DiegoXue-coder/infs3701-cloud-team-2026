# Reading Tracker · 60-second recording script

## Current solo version for Tenzi

Record the live site in your own session once the new URL works and both targets are healthy. You can narrate while recording or add the voice-over afterwards. Edit and export the final cut yourself. Diego will provide the diagram PDF. The original storyboard below was prepared by Marina.

| Time | Show | Suggested English narration |
| --- | --- | --- |
| 0–15 s | Open the live homepage, add a uniquely named fictional book and show it in the list. | “Reading Tracker saves books and tracks reading progress. I’ll add a fictional book and save it. It now appears in the reading list.” |
| 15–40 s | Show dated live requests with both instance labels and the same fictional record. | “The load balancer routes requests to two private EC2 instances in different Availability Zones. Both use the same DynamoDB table, so the record is available through either instance. Here are successful requests from both targets.” |
| 40–60 s | Show the architecture and verified CloudWatch evidence if captured. | “The load balancer is the public entry point. The application servers stay in private subnets, and DynamoDB keeps the data separate from those servers. CloudWatch tracks healthy targets so we can see when redundancy drops.” |

Use the actual observed results. Save the raw recording, final cut and evidence links. If the final diagram PDF arrives later, record the live browser footage first and add the diagram during editing.

## Original joint-recording draft (historical record)

Candidate recording version `06c2292`. Each person is responsible for their own narration. The screen recording uses the actual business service and that session's logs; a recording window in UTC is suggested, with waits compressed to the edit timecodes below. Length is prepared at the group's provisional 60 seconds.

| Timecode | On screen | Draft English narration |
| --- | --- | --- |
| 0–11s | Diego, showing the business entry point and the two-AZ architecture diagram | “Reading Tracker uses one load balancer across two Availability Zones. Each private EC2 instance runs the same release.” |
| 11–24s | Alex, filling in one unique fictional record and showing the saved list and statistics | “I add a fictional reading record. The application writes to DynamoDB, so either server can read the same progress and rating.” |
| 24–37s | Marina, highlighting `az-a`, `az-b` and the status column in the log, then cutting to the record readback | “I independently checked the same record on both instances. In a 30-request sample, each instance served 15 requests, and all returned HTTP 200.” |
| 37–52s | Diego actually stops one host; Marina shows the synchronised log and CloudWatch alarm history. Waiting can be edited out, keeping the actual UTC | “During the single-instance test, we tracked requests to the surviving target and compared the results with the CloudWatch alarm history.” |
| 52–60s | Marina shows both labels and the same record after recovery; Diego presents the recovery evidence | “After recovery, we check both targets again and confirm the record is still available.” |

When archiving the footage keep the version, date, actual operator and matching logs. The stop, alarm and recovery segments must wait until the joint test yields real footage before being cut in, with the narration adjusted to the actual failure count. The business entry point is the current HTTP demo, and all records use fictional data. [Deployment handoff](business-handoff-2026-11-07.md) · [independent cloud evidence](c-t12-cloud-validation-2026-11-07.md)
