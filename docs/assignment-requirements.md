# Assignment requirements: AI and teammates read this first

INFS3701 cloud architecture and AWS practice, Term 3, 2026. The three original files were filed on 2026-10-31 in the study library under `source_materials/INFS3701/03_assessments/group_assessment/`. They had earlier been misplaced in the INFS3822 directory, which is now corrected; this repository's copies of the originals have always been classified under INFS3701 and are not mixed with INFS3822 slides.

## Must be implemented

- At least two instances with requests distributed by a load balancer, or a suitable serverless equivalent.
- At least two AZs, with a design that copes with the loss of an instance or a single AZ.
- A stateless application to which instances can be added, with no important state left on any one server.
- A sensible VPC with public/private subnets, exposing only the necessary entry point.
- A resilient managed database: a multi-AZ relational database or managed NoSQL; S3 alone does not meet the requirement.
- A dashboard, and at least one alarm that is meaningful for the business and has actually been triggered.
- Least privilege, strict security groups, encryption in transit and at rest; limitations must be verified, raised with staff and stated honestly.
- A back-end service that can actually be used in a browser, not just a static page.

## Five items, 5 marks each

Deployed system, design report, architecture diagram, 12-month cost estimate, video. The body of the design report must be strictly under 4,000 words and under 8 pages, excluding references and appendices. Following the brief's "under 2 pages", the diagram and cost files are conservatively made as 1-page PDFs each. Cost uses the AWS Pricing Calculator, us-east-1, 12 months, with assumptions stated. The video is for now prepared as real operation and architecture explanation within 60 seconds.

In addition: a contribution statement signed off individually by each person, a genuinely signed cover sheet, code and process/AI records. The official brief deadline is 2026-11-17 16:00 Australia/Sydney; one person uploads on behalf of the group, and the submission contents and latest announcements are to be checked against Moodle.

## Awaiting confirmation; the AI must not resolve these on its own

1. The brief says the video is 1 minute, the rubric says up to 2 minutes; produce it at 60 seconds for now.
2. The brief lists auto scaling as an enhancement, while the rubric checklist reads like core; needs tutor confirmation.
3. The brief requires teardown after collecting evidence to save budget, and also requires a deployed service; confirm the final resource-retention/acceptance approach.
4. Multi-person access and role permissions in the Lab follow whatever the course actually allows.

Basic monitoring is core this time and cannot be used as an extra enhancement. The enhancement is either auto scaling, or choosing and verifying three W5–9 topics beyond core as the brief allows; T16 is not enabled for now, pending a whole-group decision.

## Rules for this assignment that respond to the previous feedback

A screenshot of a switch is not a successful test; service choices need specific reasons and trade-offs; the diagram, protocols and actual deployment must agree; steps include region, resource creation, identity, dependencies and code; cost separates lab usage from the 12-month estimate; the video must show real operation and cannot just stitch screenshots together; missing AI/contribution/signature records or leftover template text must be fixed before submission.

This file is a working summary of the original files. In case of conflict, check the originals in `sources/original/assignment/` and the latest Moodle/tutor answers; do not invent course requirements from general knowledge.
