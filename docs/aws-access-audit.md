# Can three people each sign in to the same course Lab: findings

Check date: 2026-10-31, Australia/Sydney. After the user signed in, the AI viewed the Lab's actual instructions read-only and entered the console through its AWS button.

**Conclusion: this Learner Lab explicitly prohibits creating users or groups, so the approach of "creating IAM users and passwords for the two teammates" cannot be used. No accounts or passwords were created and no permissions were changed.**

## Actual basis

- Source: [Launch Lab of the signed-in course](https://awsacademy.instructure.com/courses/188838/modules/items/18668931), Vocareum Readme, ZH-CN, instructions last updated 2025-06-24.
- The "AWS Identity and Access Management (AWS IAM)" paragraph says (translated from the Chinese Readme): "Extremely limited access. You cannot create users or groups. You can create service-linked roles, but you cannot create any other roles."
- The same paragraph says LabRole is pre-provisioned; EC2 can use it through LabInstanceProfile. This is the mechanism for services to access AWS and cannot be treated as a teammate login account.
- The Lab showed Ready; entering Console Home through the AWS button succeeded, region us-east-1.
- At the time of the check it showed Used $1.2 of $50, about $48.80 remaining on screen. The figure is delayed and does not represent the measured cost of this architecture.

## Limits of the conclusion

The basis is the current Lab's own statement of restrictions; CreateUser was not called as a failure experiment, and no actual API denial log is claimed. Do not probe or work around the explicit restriction by creating users or by other identity routes.

Whether the course also has a staff-configured group environment or a separate access entry point still needs tutor confirmation. The conclusion applies only to the current individual Learner Lab.

The old EC2/S3/data were not inventoried, and the application, two AZs, HTTPS, resource-level permissions and architecture budget were not verified; T05 is still not complete. AWS Details was not read, temporary credentials were not extracted, and there was no Reset, End Lab, resource deletion or deployment.

## Current way of collaborating

1. This Lab can serve as the candidate integration environment; the user has chosen to be the holder and deployment owner (DiegoXue-coder).
2. A prepares the network and deployment configuration, B prepares the application and data code, C prepares tests, monitoring and evidence, and all three submit to GitHub in parallel.
3. After another person checks a change, the approved environment holder executes it; when sharing a screen, distinguish the actual operator, the guide and the checker.
4. Record the commit, steps, logs/screenshots and test results, then report the task receipt.
5. A real person asks the tutor: does the course provide a way for three people to access the same environment with their own identities? Update the plan after a real answer arrives. For now, do not exchange personal passwords, keys or session tokens.

For the operating process see [shared-aws.md](shared-aws.md).
