# Member three: test and monitoring preparation, ready to start without waiting for deployment

> Latest entry point and actual limitations: [this round's verification and three-person handoff](2026-11-01-foundation-verification.md). The new ALB can already be used for foundation checks, and the business application is not yet released; do not treat the earlier "entry point not created" records below as the latest state.


First set up your own environment through the [self-service entry](self-service.md) and join C. Read the old code `app/reading_tracker.py`, the marking requirements and `project/handoffs.json`. The first item is T08, followed by preparation for cards such as T12/T13; the real final test conditions still follow the task cards.

2026-11-01 handoff update: read this round's verification and three-person handoff and project/aws-resources.json. The new ALB has a clearly labelled foundation test page that can be used to verify the request tool; the Reading Tracker business is not yet released. Continue local data/feature testing and independently review the existing monitoring baseline, with final acceptance after the business release.

## The first round must deliver things that run

1. Build fictional reading-record data: an empty set, a normal mixed-status set and a boundary-input set; write explicit expected counts/pages/ratings for each. Do not use private data.
2. Write independent tests using compute_stats from the old code. This can be done without the full web page or AWS; `scripts/check_reading_baseline.py` shows how to isolate the original function, and the tests should cover new risks, not copy existing assertions.
3. Write a continuous request-logging tool with a configurable `BASE_URL` that records time, HTTP status, duration and instance identifier; set a timeout and a maximum request count, with no unlimited high-frequency requests.
4. Actually run it against a local test target and save the real results. Before B's web page is delivered, a local HTTP service clearly labelled as a test substitute can be used to verify the tool, and it cannot be written up as business functionality passing.
5. Prepare the CloudWatch settings file/steps: which signal to observe, resource dimensions, statistical period, threshold reasoning, trigger condition, recovery action and expected screenshot locations. Hand them to A to implement, and take responsibility for checking and explaining.
6. For cost, first organise the service list and usage assumptions; without final resources mark it as an estimate draft and do not invent balances or prices.

The first round is not just a test checklist; it includes at least data files, executable scripts and actual local execution records. Report partial results through T08's report, without waiting for all cloud tests to finish.

## During joint testing

Get the real address and version from handoffs.json / docs/environment.md. Verify item by item for features, shared data, routing, failure, alarm and security. Resource creation/stop/recovery is done by A; you record inputs, expected, actual, duration, failure count and evidence.

Problem cards state clearly: address/version accessed, reproduction steps, expected and actual, logs, and whether it likely belongs to A (environment) or B (application). If the cause is unknown mark it as to be located and do not assign it arbitrarily. After a fix, retest yourself and give a receipt.

## While waiting for cloud parameters

Continue with test scripts, sample data, monitoring configuration, cost assumptions, the video script and evidence checks; once B's delivery is in, independently try to reproduce and review it. Do not pause the whole job with a single "waiting for deployment". Only the real final cloud conclusions need to wait for A, and there is no need to message the project owner privately to ask again for source code or the development port.
