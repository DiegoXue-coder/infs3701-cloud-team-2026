# What online, latest and auto-refresh each mean

## Available online at any time now

The repository and Issues are served online by GitHub, so teammates who are signed in with repository permission can view them at any time without your computer being on. The [online task entry](../LIVE_BOARD.md) links by A/B/C and status to GitHub's current task lists; each time a list is opened or refreshed it queries the synchronised state, and the search index may lag briefly.

`DASHBOARD.md` is a prepared progress snapshot showing the last sync time. It is also an online file, but it does not recalculate itself every second. A page already open in the browser is not guaranteed to receive pushed changes either.

## How it is updated now

A member and their AI complete an operation → upload the real delivery or record → run the sync helper → the Issue metadata, labels and dashboard update together. Other members see the update by refreshing the task page.

When an operation is done in the AWS console but not reported to the project, GitHub does not know about it automatically; even a real-time web page could not know it out of nowhere. When only a `/team ...` comment is posted with no processed receipt, the command is still a pending request.

## What each of the three looks at

- A: network, servers, single entry point, deployment, architecture diagram.
- B: application, database, deployment conventions, report; handled by member two, username to be registered.
- C: monitoring, testing, evidence, cost, video.

A/B/C on the online entry are planned roles; the actual claimant is recorded in the Issue assignee; members are bound in config after joining, and an unclaimed task cannot be treated as someone already working on it.

## If more automation is wanted

1. **Native GitHub Projects:** offers tables, boards with columns by status and timelines, linked to Issues; it suits dragging and viewing by role. The existing authorisation has no Projects scope, and this time the authorisation was not widened or a project created without permission. Enabling it still requires keeping the task command/delivery rules consistent, and dragging a card cannot replace real review.
2. **Restore hosted sync:** once the payment/quota limit on the GitHub Actions account is lifted, re-enable and verify the existing workflow so commands are processed in the background after submission. Billing has not been changed, so it cannot be claimed as restored.
3. **Separate real-time web page:** needs its own login, private data access and a continuously running service; course materials or access tokens cannot be placed directly on a public page. This adds maintenance, and for the current three-person assignment the existing GitHub online task entry is enough.

Do not promise "second-level updates" or "the AI automatically sees live AWS configuration" without actual testing.

Official documentation: [GitHub task filtering](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/filtering-and-searching-issues-and-pull-requests), [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects).
