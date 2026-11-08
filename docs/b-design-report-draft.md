# Reading Tracker design report — working draft

## Application and data tier (Alex)

Reading Tracker serves readers who want a lightweight record of books, reading
progress and ratings. Its core workflow is to enter a book, then revisit the
same library and see progress and summary statistics. The coursework deployment
uses one shared demonstration library. It is not a multi-user product with
private accounts.

A cloud deployment lets the same library stay available when traffic goes to a
different server or one application instance stops. The Application Load Balancer
routes HTTP requests to two private EC2 instances across two Availability Zones.
Both run the same Flask application under Gunicorn. Flask reuses the original form,
list and statistics, which keeps the business scope small enough to test the
infrastructure changes. EC2 and Gunicorn give us control of the runtime and release
version, but require image maintenance, rollout checks and instance monitoring.

The application writes each reading record as a DynamoDB item with a UUID string
partition key. The schema stores status, pages, rating, note and UTC creation
time. A conditional put prevents a new record from replacing an existing key.
The application sorts records and derives progress and summary statistics on read.
The EC2 instance role supplies access. Application instances do not retain
authoritative book data in local memory or files. A separate in-memory mode is
available for local development and resets when the local process stops.

DynamoDB suits this workload because records are independent and do not require
joins. It supplies a shared managed data tier while letting either application
instance serve requests. The current library page uses a paginated,
strongly consistent full-table Scan so a successful write can be read from
either instance. A Scan is not a point-in-time snapshot across concurrent
updates. As the library grows, scanning every item on every page load increases
latency and read usage. A larger version would need bounded queries for the list
and a separate approach to aggregate statistics. Legacy S3 records were not migrated.

The current demo uses HTTP and has no authentication or CSRF protection. It
should use fictional data only. HTTPS and tighter access controls remain
production requirements. Process health and instance labels help identify
routing but do not establish database health. A real POST and subsequent
business page GET are the checks for data access.

## Integration and evidence

- A owns networking, compute, security and the architecture diagram. Use the
  [business rollout](business-rollout-2026-11-07.md) and [operator evidence](business-handoff-2026-11-07.md).
  A recorded cross-instance readback, service during a single instance stop and
  persistence after restart on release `06c2292`. Whole-AZ loss was not tested.
- B owns application/data design and independent functional verification. Use the
  [app and deployment guide](../app/README.md) and [data contract](interfaces.md).
- C owns independent routing tests, monitoring, costs and video. Use the
  [business validation](c-t12-cloud-validation-2026-11-07.md),
  [cost draft](c-t18-calculator-draft-2026-11-07.md) and
  [video script](c-t20-video-script-2026-11-07.md). Keep the business alarm
  experiment separate from the earlier infrastructure alarm evidence.

Before assembling the final PDF, reconcile the release ID and resource labels
across the prose and architecture diagram. Separate observed results from
planned checks. Confirm the course's unresolved requirements with A. Keep the
report body below 4,000 words and below eight pages.

On 8 November at 15:35 Sydney time, B received HTTP 503 without an instance
label from the ALB health route. The preflight stopped before any write.
Independent cross-instance verification awaits restoration of the demo.
See the [B execution log](../evidence/T11/2026-11-08-B-cloud-http.log).
