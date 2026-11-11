# Reading Tracker HTTPS rollout

Decision recorded on 11 November 2026 Sydney for T15. Encrypt both application links to cover the assignment's broad transport-encryption requirement. The public browser connection terminates TLS at the existing ALB, which starts a separate TLS connection to each EC2 target. The AWS API connections to DynamoDB and S3 already use HTTPS. The existing diagram remains a record of the HTTP deployment evidenced on 10 November.

## Configuration

| Link | Target configuration | Prerequisite |
| --- | --- | --- |
| Browser to ALB | HTTPS 443 on `infs3701-team-alb` using a browser-trusted ACM certificate covering the exact demo hostname | Obtain an authorized public DNS hostname and permission to add its validation and routing records. Request or import the certificate in `us-east-1`. |
| ALB to both EC2 hosts | New instance target group `infs3701-team-tg-tls` in the existing project VPC. HTTPS port 8443. HTTPS health check on `/health` with matcher 200. | Each host serves the existing release on 8443 with its own server certificate and private key. Allow TCP 8443 only between the existing ALB and app security groups. |
| EC2 to AWS services | Existing HTTPS 443 SDK connections via the S3 and DynamoDB gateway endpoints. | Existing endpoint and IAM configuration. |

AWS documents that an HTTPS listener needs a server certificate and that an HTTPS target group encrypts target connections without validating their certificates. The private targets can therefore use separate self-signed certificates. Keep each key on its own instance and give only the application service identity the read access it needs. The browser uses the ACM certificate on the ALB and never sees either EC2 certificate. [ALB listener](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html) · [Target connection behavior](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html#routing-configuration)

## Rollout and validation

1. Check for a usable issued certificate in ACM. If none covers the chosen hostname, request a public certificate for an authorized subdomain in `us-east-1` and add the ACM validation CNAME with the DNS provider. Add a separate routing CNAME pointing the demo subdomain to the current ALB hostname. Verify both DNS records and ACM status `ISSUED`. [ACM DNS validation](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html)
2. Record the existing ALB listener action, app and ALB security-group rules, CloudWatch alarm dimensions, and each host's current user data. Check that both HTTP targets are healthy and that the pinned Reading Tracker release is present. Stage a separate Gunicorn service on port 8443 using the same application directory and environment file as `infs3701-app.service`. Use Gunicorn's certificate and key settings with certificates generated on each host. Verify the installed runtime supports the flags and that the host has a certificate-generation tool before applying the service. Keep the current 8000 service available for rollback.
3. Configure one host at a time. If the verified EC2 stop/update-user-data/start path is needed, confirm the other host is healthy first and preserve the working per-boot business bootstrap. Confirm the restarted host serves the business release on 8000 again and answers HTTPS locally on 8443. Verify `/health`, the instance label and a real homepage read. For the local HTTPS check, trust that host's generated certificate explicitly. Complete the first host's checks before starting the second.
4. Add app ingress 8443 from the ALB security group and matching ALB egress to the app security group. Register both private EC2 instances in the HTTPS target group, then attach the new group to ALB HTTPS 443 with the issued certificate. Check ALB ingress 443 and that both HTTPS targets are healthy. Keep the existing HTTP listener forwarding during these checks.
5. Open the HTTPS hostname in a browser using normal certificate validation. Verify hostname and certificate validity, both instance labels, and an actual read and write of a fictional demo record. Point the dashboard and redundancy alarm at the serving HTTPS target group and check that it emits data. Save protocol, target-health and application evidence.
6. Once HTTPS passes, change HTTP port 80 to redirect to the verified HTTPS hostname. Verify the old port redirects and no longer serves the application. Update the diagram, report, demo link and annual cost assumptions from the verified configuration.

If a host fails during setup, stop the rollout, restore its previous user data if changed, disable the new TLS service on that host and check both original HTTP targets. If listener or monitoring checks fail, preserve or restore the recorded HTTP listener action and alarm dimensions while diagnosing the failure. Resume cutover only after both HTTPS targets and the browser path pass.

## Deployment prerequisite still open

The 10 November inventory found no issued certificate or hosted zone in the Lab. A usable hostname under authorized DNS control is still unconfirmed. The course or a group member can provide a subdomain. An already-issued certificate for an authorized hostname with DNS pointing to this ALB would also satisfy the entry prerequisite. This plan records the implementation choice and has not been applied to AWS.
