# C's report chapter and video draft

2026-11-04. For the group to integrate; not signed on behalf of any member and not representing a human review. The body of the final report is strictly under 4000 words and under 8 pages; conflicts between the original brief and rubric are to be confirmed with the tutor under T03.

## Whole-group report outline and split

1. Objective and route (B integrates): Reading Tracker / Option A, original author DiegoXue-coder, with clear upgrade objectives.
2. Architecture and services (A): two-AZ network, ALB, private EC2, DynamoDB, citing an architecture diagram that matches reality.
3. Scalability and availability (A/B/C): stateless and shared-data design; C provides real routing/failure samples and limitations.
4. Networking, security and data (A/B): entry point and role, data model, encryption and the unresolved HTTPS limitation.
5. Monitoring and validation (C): metrics, threshold reasoning, experiment method, inputs/expected/actual, failures and fixes.
6. Cost and trade-offs (C): 12-month Calculator inputs and final estimate, lab budget and resource trade-offs.
7. Enhancements if attempted (the relevant operator): describe only enhancements that are implemented and evidenced; basic monitoring is core.
8. Contributions, AI use and references (each person): confirmed individually, with one consistent referencing style.

## English paragraphs from this round, ready to integrate

**Validation method and current scope.** Member C prepared four synthetic datasets and independent tests of the original Reading Tracker statistics function. Ten tests passed on Windows with Python 3.12.14. The tests execute the original function in isolation, covering aggregate semantics, missing ratings, boundary values, legacy numeric strings, order invariance and input preservation. They do not import the web application or access AWS. Seven additional tests passed against a real loopback HTTP fixture, validating bounded request sampling, status and instance-header capture, timeout handling and protection against overwriting evidence. Four persisted HTTP samples returned 200 from the explicitly labelled local fixture. These results validate the statistics baseline and the sampling tool; they do not establish that the final application or managed database is deployed.

**Monitoring rationale.** The repository baseline alarms when the minimum healthy-target count falls below two over two consecutive 60-second periods. This is a redundancy signal: one surviving target may still serve requests. C's offline review found that the documented threshold and dimensions match the deployment source. Live configuration readback remains pending. The missing-data setting and lack of configured notification recipients are explicit limitations. Final acceptance will correlate request samples with target health, real alarm history and the operator's failure and recovery timestamps.

**Availability evidence to collect.** The planned joint experiment will first establish two healthy instances, sample steady traffic, stop one instance under A's control, record observed failures, and restore the original instance. Both instance identity and shared-data persistence will be checked. The report will distinguish client sampling resolution, load-balancer health-check behavior and alarm evaluation delay. A single-instance experiment will not be presented as proof of a complete Availability Zone outage.

The paragraphs above describe only this round's facts/plans and should finally be updated to the actual release version and joint-experiment results. A's existing cloud evidence must state its date and operator and cannot be counted as C's measurement this round.

## 60-second video shot script (not yet recorded)

| Time | Screen and real action | Narration points |
| --- | --- | --- |
| 0–8s | Open Reading Tracker at the actual business URL; show the deployed version | Reading Tracker, a single-server service upgraded to a two-AZ shared-data architecture |
| 8–22s | Add a fictional record, return to the list and show the statistics | The back end actually processes the record and DynamoDB keeps the shared state |
| 22–35s | Show the real request log from the same window, with at least two instance labels | ALB routing; both instances run the same application version |
| 35–49s | Align A's actual single-host stop time, the continuous requests and the real alarm state | The service kept responding within the tested scope; show any failures honestly |
| 49–60s | Recovered health/data still present, brief view of the architecture diagram | Private application tier, shared data tier, monitoring and trade-offs |

Record only the running business service; the foundation test page, simulated instance labels or console screenshots alone cannot be substituted. The formal video needs a real screen recording and the member's own narration; no video, voice-over or cloud screenshots were produced this time.

## Draft contribution and AI record

Marina057 (C): with her authorisation, Codex assisted in reading the repository, generating four fictional data sets, writing statistics tests and the HTTP sampling tool, running local tests, and organising the monitoring/cost/report and video drafts. The actual commands were run by the AI tool on her machine; the user has not yet manually verified each item, and another account has not yet reviewed. AWS resources were created by A's existing work, and C did not operate AWS this time. On 2026-11-04 join C and the T08 claim were completed under her own GitHub identity, claim receipt R-T08-6624693113. The original test logs keep their pre-enrolment times; this delivery submits only the T08 preparation work, and the work share and independent review must be confirmed by a real person.
