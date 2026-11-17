# New network configuration draft: form filled in, not created

2026-11-01, us-east-1. Machine-readable configuration: project/network-plan.json.

Name prefix infs3701-team; VPC 10.37.0.0/16, separate from the original default VPC 172.31.0.0/16. The original network and old website are kept.

| AZ | Public subnet | Private subnet |
| --- | --- | --- |
| us-east-1a | 10.37.0.0/24 | 10.37.10.0/24 |
| us-east-1b | 10.37.1.0/24 | 10.37.11.0/24 |

NAT=None; VPC endpoints=None; DNS hostnames/resolution on; no IPv6; Default tenancy; the separately charged VPC encryption control=None. That optional control is different from HTTPS/disk encryption, which still have to be implemented and verified separately.

The public subnets are intended for the load-balancer entry point and the private subnets for the back end. This is currently only a network foundation draft: with NAT off, private subnets cannot download dependencies directly from the internet; a prepared image/dependency delivery, maintenance and AWS service access paths must be in place before the business can be deployed. Endpoints are chosen separately according to the final database and maintenance approach, with permissions and cost reviewed, and the default full-access endpoint policy is not simply reused.

The browser preview shows four subnets, three displayed route tables and one internet gateway connection; after creation check the actual routes and associations item by item, as well as the implicit main route table. There is no creation-success page, resource ID or connectivity test, so it cannot be marked as a built network.

This session's real record: evidence/T06/2026-11-01-vpc-form.log; screenshots are in the same directory. Create VPC has not been clicked yet.

## Later actual creation result

On 2026-11-01 Create VPC was run successfully. VPC vpc-0836d003a70f93405, with all four subnets and the IGW in place; an actual describe_route_tables check showed four tables in total (including the implicit main route table), with the public default route to the IGW and only local routes for private. The "not created" wording above is kept as a description of the draft stage at the time; the current state is as in project/network-plan.json and project/aws-resources.json. The final business/maintenance/database private paths still await implementation and verification.
