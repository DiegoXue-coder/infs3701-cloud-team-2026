# Tests and evidence

| Task/requirement | Owner | Test date and environment/commit | Steps | Expected | Actual result | Screenshot/log path | Checker |
| --- | --- | --- | --- | --- | --- | --- | --- |

Cover at least: real interface operation, database write/read, shared data across instances, routing, single-instance failure, dashboard, alarm trigger and recovery, security and encryption checks, and the chosen enhancement.

For failure tests also record: the continuous-request period, target health-check settings, the moment the instance was stopped, failures/total, the recovery moment, and the actions to restore the environment. Do not describe a single-instance test as a full measured AZ failure.

Suggested naming: `T14_2026-11-08_failover_requests.log`. Remove keys, tokens and private data from screenshots and logs; leave enough time and configuration context.
