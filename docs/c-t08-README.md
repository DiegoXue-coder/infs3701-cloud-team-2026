# C / T08 test-preparation delivery

Marina057 (C), assisted by Codex, 2026-11-04. doctor, join C and the T08 claim were run through her own Git login; claim receipt [R-T08-6624693113](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues/8#issuecomment-6624699434). The first round of local work took place before role enrolment, and the original test times are kept.

## Contents and results

- [Test plan and reproduction](c-t08-test-plan.md): four fictional data sets, 10 statistics tests and 7 HTTP-tool tests all passed; item-by-item core acceptance plan.
- [Monitoring plan](c-t08-monitoring.md): offline check of 11 fields of the existing alarm, and a failure/recovery operation plan for A.
- [Cost assumptions](c-t08-cost-assumptions.md): full-year service inputs for us-east-1; T18 then uses the Calculator to produce prices and the PDF.
- [Report and video draft](c-t08-report-and-video.md): English paragraphs ready for integration, a 60-second shot plan and AI records.
- [Structured delivery](../deliveries/T08/2026-11-04-Marina057.json): original tests, evidence and limitations.

This delivery only declares that the T08 preparation requirements are met and needs an independent check by another account; it is not all of C's work complete. No AWS deployment, database write, stop, real routing or business HTTP acceptance was performed. The four persistent HTTP samples come from a local service clearly labelled local-fixture-only.

## Review steps

In the repository root run `python tests/c_t08/test_statistics.py`, `python tests/c_t08/test_request_log.py` and `python scripts/c_t08_review.py`. This run used Windows/Python3.12.14 and needs no Flask/boto3 or AWS identity; cloud Python3.11 is retested separately. Check one by one that the documents cover all core items, expected results and evidence, and inspect the original run.log and JSONL. Existing samples are not overwritten.

After T08 is submitted it should enter awaiting check, to be approved or sent back for changes after A or B actually checks it; the author cannot self-approve. The receipt on the [task card](https://github.com/DiegoXue-coder/infs3701-cloud-team-2026/issues/8) is authoritative.

## Material gaps and follow-up

The material index still lacks the formal W8 database and W9 monitoring lecture/tutorial materials and the latest Moodle/tutor replies. The conflicts over 60 seconds vs 2 minutes for the video, whether auto scaling is core, resource retention and multi-person Lab permissions are still to be confirmed under T03 and cannot be resolved by a draft.

After B/A release the exact business version, C continues with T12 routing, T13 alarm and T14 failure evidence, finalises the T18 cost, and does the T20 real video and T21 individual sign-off. A is responsible for the actual AWS stop/start and recovery, C for sampling and independent interpretation. No draft may stand in for cloud acceptance.
