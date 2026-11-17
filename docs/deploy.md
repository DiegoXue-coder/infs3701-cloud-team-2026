# Real steps from code to a usable system

Filled in by A/B after actually operating; another person follows it to review. Currently only a template, with no claim that it is reproducible yet.

1. Prerequisites: region, permitted role, balance, software/dependency versions.
2. Create the network: VPC, AZs, subnets, routes, egress or endpoints, security groups.
3. Create the data tier: table/database, schema, encryption, identity/credential management, application access path.
4. Create instances: image, size, EBS, role, access and maintenance method.
5. Deploy code: repository and commit, dependency installation, environment variable names (no secrets), real start command, restart policy.
6. Connect the entry point: target group, port, health check, listener, TLS.
7. Monitoring: dashboard, alarm, test and recovery.
8. Verification: real browser operation, shared data, routing, failure.
9. Updates: how to deploy the same version to both machines, how to restore the previous version, how data changes are handled.
10. Evidence and cleanup: backup, recording, conditions for keeping resources for acceptance, item-by-item deletion confirmation.

For each step fill in: operator, real command or console action, actual parameters, success criterion, evidence link, problems encountered. Do not enter keys.
