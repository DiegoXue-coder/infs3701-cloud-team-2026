# Reading Tracker recovery in Tenzi’s Learner Lab

Tenzi (`wyend12`) deploys through his own AWS Academy session and leads the live recording and English narration. Diego reviews the deployment and integrates Figure 1. Alex verifies the live application independently. Marina monitors cost and collects CloudWatch evidence. See the [current work split](weekend-closeout-2026-11-14.md) for what to prepare in parallel. Diego’s former endpoint and its November test logs are historical. Report the replacement environment only after actual checks.

## 1. Check your Lab and prepare the files

1. In AWS Academy, record the displayed amount used and total. Start your Lab, open AWS and select **N. Virginia (us-east-1)**. Confirm the session stays active. In GitHub issue **T26** post the remaining credits and your available test window.
2. Open **CloudShell** in that session. In GitHub, download the private repository ZIP from **Code → Download ZIP** on `main`. Upload it with **CloudShell → Actions → Upload file**, then unzip it and enter the extracted project directory. Use GitHub on your computer for Issues and submitting evidence. You do not need a GitHub token in CloudShell or to share AWS credentials.
3. Run the commands below from the project directory. Keep command output in a log and omit credentials from screenshots.

```bash
set -o pipefail
bash deployment/learner-lab/redeploy.sh preflight 2>&1 | tee ~/reading-tracker-preflight.log
```

The script uses CloudShell’s session identity. It checks CloudFormation read access, the course instance profile, an Amazon Linux AMI, gateway prefix lists and the templates. It lists existing EC2, load balancers, NAT gateways, RDS instances and DynamoDB tables for Marina’s review. Compare those with the Lab cost view and check for retained volumes, snapshots and extra monitoring use. If an inventory API alone is denied, post the error and use the console to check it. If a required service or profile is denied, post the exact error in T26.

## 2. Prepare and review

Run this on the same region and account. Replace `123456789012` with the account ID printed by preflight.

```bash
LAB_ACCOUNT=123456789012
bash deployment/learner-lab/redeploy.sh prepare "$LAB_ACCOUNT" 2>&1 | tee ~/reading-tracker-prepare.log
```

This downloads pinned Linux Python wheels, verifies the application file against release `06c2292`, uploads the bundle to a small private encrypted S3 bucket and creates a CloudFormation change set. The change set must show **Add** for the new resources. Review it in CloudFormation as `reading-tracker-recovery` / `initial`. It describes two private `t3.micro` instances with encrypted 8 GiB gp3 disks, one public ALB, a fresh capped DynamoDB table, two gateway endpoints, one dashboard and one alarm. The template uses the existing course profile and the region’s public Amazon Linux AMI. The private hosts install Linux packages through the S3 gateway and install Python dependencies from the bundle. [AWS documentation for the AL2023 package repository path](https://docs.aws.amazon.com/mgn/latest/ug/preparing-environments.html#network-requirements).

The demonstration exposes **HTTP port 80** at the load balancer. Anyone who reaches this URL can view or add records. Use only fictional data and share the URL in the private team Issue. Record HTTP as the verified deployment protocol and keep HTTPS as an open report item. Confirm the group’s budget and recording window before executing the change set.

## 3. Deploy and verify

```bash
bash deployment/learner-lab/redeploy.sh deploy "$LAB_ACCOUNT" 2>&1 | tee ~/reading-tracker-deploy.log
bash deployment/learner-lab/redeploy.sh status
```

If the terminal disconnects, use `status` or CloudFormation Events before taking any further action. On failure, save the first actionable resource error. Inspect the rollback and any leftover stacks in CloudFormation before retrying. Instances, the load balancer and the database are created when the change set executes. A stack marked complete still needs the live checks below.

1. In **EC2 → Target Groups → Targets**, verify both targets are healthy. If one stays unhealthy, view **EC2 → Monitor and troubleshoot → Get system log** for the first bootstrap error and the expected `READING_TRACKER_READY` line. Use the `DemoUrl` output in the browser. Check that `/health` identifies the Reading Tracker stage. Open the home page to verify the real data path.
2. Record one browser write with the status **Reading**, **12 of 120 pages**, a rating of **4**, and a unique fictional title. Put the demo URL and exact title in T26. Alex can now run the existing independent check and add one additional fictional record.

```bash
python3 scripts/b_t11_live.py --url 'http://REPLACE-WITH-NEW-ALB' \
  --reference-title 'REPLACE WITH THE EXACT FICTIONAL TITLE' --write-one-fictional \
  | tee reading-tracker-independent.log
```

3. Marina captures target health, both instance labels and the CloudWatch dashboard. Set dashboard auto-refresh to **five minutes or slower**, or turn it off. For a fresh alarm test, after the initial recording and once both targets are healthy, Tenzi stops one project instance using the stack outputs while Alex samples the page and Marina records the healthy-target alarm. Restart that instance, check both targets and verify the same fictional record. Save the real outcomes with timestamps. If only dated evidence from Diego’s original Lab is used, identify that environment and date.
4. Save the files locally before any Lab cleanup. Post release SHA, DemoUrl, both labels, result, dated logs and the playable recording location in T26. Use the normal delivery JSON and independent review. Confirm the course’s evidence and retention requirements, then follow its cleanup instructions. If cleaning up only this deployment, delete the demo stack, remove the uploaded release object from its private bucket, then delete the artifact stack. Check the terminal stack states and remaining costs.
