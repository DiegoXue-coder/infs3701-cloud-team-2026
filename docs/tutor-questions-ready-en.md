# Tutor clarification - ready to copy, NOT SENT

Prepared11November2026Sydney. Send through your normal course channel; no tutor recipient/address has been assumed. This is a question draft, not a course ruling or a request for approval to change account permissions.

Hi,

We are finalising our INFS3701 Reading Tracker project, using two private EC2 application instances in different Availability Zones, an internet-facing ALB, DynamoDB and CloudWatch. Could you please clarify these points?

1. **HTTPS:** Our ALB currently uses HTTP80. We have not established access to a domain, ACM returned no certificates and Route53 no hosted zones in the Lab, and CloudFront listing is denied. Does the course provide a DNS name/certificate, or is there an approved Learner Lab approach for implementing HTTPS without an owned domain? We are currently reporting HTTP accurately rather than claiming TLS is implemented.
2. **Scaling:** Page2 of the assignment brief calls automatic scaling Going Further and says it is not required. The marking checklist on page2 of the rubric lists capacity scaling with demand (auto scaling/serverless) under core. Will a stateless two-instance architecture that can be expanded manually satisfy core? We have deferred the automatic-scaling enhancement while finishing core work and deliverables.
3. **Video:** The brief requests a one-minute video while the rubric permits up to two minutes. We are preparing60seconds; is this the intended limit?
4. **Resource retention:** The brief asks us to capture evidence before teardown to protect Lab credits, but the deployed solution is also assessed. Which resources must remain available for marking, and when may we stop or remove the stack after recording?

Thank you.

---

Note: this passage can be sent to the teacher in one message, asking items 1 and 2 first. Requirements can be updated only after a real answer is received; until item 3 is answered keep to 60 seconds, and until item 4 is answered do not delete the system without approval. This file was not sent automatically.
