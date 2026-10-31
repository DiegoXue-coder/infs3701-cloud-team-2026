# INFS3701_Tutorial_05_Securing_User_Access_and_Data.pdf

Course: INFS3701. Searchable text; original diagrams and layout remain authoritative.

## Page 1

I N F S 3 7 0 1     ·     T E R M  3 ,  2 0 2 6
Enterprise Architecture for Scalable 
Cloud Solutions
Week 05 · Tutorial
Securing User Access & Data
TWO -PA RT PRA CTIC AL  S ES S IO N

## Page 2

W EE K  0 5 · TUTO R IA L
Today's Tutorial
How this two-part session works.
1 Prep check: last week's Cloud Economics module
2 Recap the demo service so far
3 This week's objectives: IAM & encryption
4 Part 1: we secure the demo service
5 Part 2: form your groups and choose your project

## Page 3

W EE K  0 5 · TUTO R IA L
How This Tutorial Works
Each week: learn it on a working example, then apply it to your own assignment.
Part 1 · tutor-led
≈ 75 min
We lock down the demo service with least-privilege IAM and encryption. Follow along; you'll secure your own project too.
Part 2 · Your assignment
≈ 45 min
You work on your own service with help on hand, keeping progress as you go (a versioned doc and screenshots).
H OW Y OU R  TU T ORI AL M ARK  IS  S P LI T
Preparation (50%): complete the AWS Academy modules and labs set in each tutorial before the next session.
Participation (50%): work on your next assessment in the session, and keep evidence: AI-prompt screenshots, dated versions of your docs and code, and a short reflection.

## Page 4

W EE K  0 5 · TUTO R IA L
This Week's Objectives
Week 5: Securing User Access & Data.
BY  T HE E ND,  YO U  C AN
Explain IAM: users, roles and policies
Apply least-privilege access to a service
Encrypt data at rest
Explain how access keys and roles differ
H OW T HI S  WEEK 'S  M AR K IS  S P LI T
Preparation  (50%)
The Week 4 module (Cloud Economics · Module 2) completed in AWS Academy before today.
Participation  (50%)
Your work in Parts 1 and 2 today, and the progress you record (design document + screenshots).
F RO M T HE L EC TU R E
Today puts this week's lecture to work (IAM users, roles and policies, least privilege, and encryption) securing the demo service.

## Page 5

PART 1
T U T O R- L E D
Securing the demo service
Least-privilege access and encryption, together, step by step.
≈ 75 MINUTES


## Page 6

W EE K  0 5 · TUTO R IA L
The Demo Service So Far
Built and costed, now we secure it.
Compute · done
The app on EC2.
Storage · done
Notes saved in S3.
Security · today
We add least-privilege access and encryption.

## Page 7

WEEK 05 · TUTORIAL
The Demo Service, Locked Down
The same boxes as last week, but now each one has a rule about who may use it.
Your browser (internet)
Region us-east-1
Default VPC
172.31.0.0/16
Internet Gateway
Availability Zone us -east-1a
DEFAULT PUBLIC SUBNET plain HTTP · no certificate in the lab
notes-sg · port 8080 from your IP only
Notes app
EC2 t3.micro · no keys in the code
Public IPv4 EBS · 8 GB IAM role · 
LabRole
REGIONAL SERVICES, OUTSIDE THE 
VPC
S3 bucket
public access blocked
encrypted at rest
Reads and writes notes over HTTPS,
using temporary credentials
from the instance's role.
CloudTrail
records who called what, and when
LOC KED D OWN TODAY
Security group
port 8080 from your IP only
Least privilege
read and write notes in one bucket only
No keys in the code
temporary credentials from the role
Encryption
at rest in S3; in transit to S3 over HTTPS
WHAT THE LAB LI MITS
No new roles: LabRole stays attached, so 
draft the policy you'd attach and compare it.
No certificate: the browser reaches 
the app over plain HTTP.
Security barely changes the diagram, it changes who may use each box, and how.

## Page 8

W EE K  0 5 · TUTO R IA L
Part 1: Secure It
Follow along on your own copy of the demo service.
1 Give the app an identity, attach LabRole, with no keys in the code.
2 See how a least-privilege role is built and watch the lab refuse it.
3 Let the bucket say no: a bucket policy that blocks deletes and plain HTTP .
4 Choose the encryption key: switch from SSE-S3 to SSE-KMS, and compare.
5 Tighten the security group to your IP , and then prove it's locked down.
We can't shrink LabRole, but the bucket and the network can still say no. 

## Page 9

WEEK 05 · TUTORIA L · PART 1 · GET SET UP
Get Set Up: Your Own Demo Service
One template builds the same starting point for everyone, in about five minutes.
DO  T HI S
1 Download INFS3701_W5_Notes_Demo.json  from 
Moodle (Week 5).
2 Start your Learner Lab, wait for the green dot, then open 
the console. Check the Region is N. Virginia (us-east-1).
3 Go to CloudFormation → Create stack → With new 
resources (standard).
4 Choose Upload a template file → Choose file, pick 
the JSON file, then Next.
5 Stack name notes-w5. Leave AttachLabRole = no. 
Click Next → Next → Submit.
6 At CREATE_COMPLETE, wait 2-3 minutes, then open 
the AppURL on the Outputs tab.
W HA T T HE  T E M P L AT E  BU IL DS
# compute
notes-app    EC2 t3.micro · the Notes app on port 8080
             no IAM role attached (yet)
# storage
bucket       S3 · private · default settings
# network
notes-sg     8080 ← 0.0.0.0/0 (anyone)
             22   ← EC2 Instance Connect only
Y O U S H O UL D S E E
The app opens with a red banner: “Running as: No AWS 
credentials…” . That's our starting point. If the page won't 
load, wait another minute: the app is still installing.
Infrastructure as code: the stack is a record of exactly what was built and deleting it removes everything at once.

## Page 10

WEEK 05 · TUTORIA L · PART 1 · STEP 1 OF 5
Step 1: Give the App an Identity
The app has no role and no keys, so it can't reach S3. 
DO  T HI S
1
EC2 → Instances, select notes-app → Connect. Use the EC2 
Instance Connect tab, not Session Manager, then Connect.
2 Run the first two commands. The second says Unable 
to locate credentials.
3 Back in the console: Actions → Security → Modify 
IAM role.
4 Choose LabInstanceProfile → Update IAM role.
5 Wait 30 seconds. Run aws sts get-caller-identity 
again, then refresh the app.
6 Post two notes. Then run the last block to see when 
the credentials expire.
TY P E  TH IS  IN  TH E  TE R M IN A L
echo $BUCKET
aws sts get-caller-identity
# after attaching the role, run it again:
aws sts get-caller-identity
# how long do these credentials last?
MD=http://169.254.169.254/latest
TOKEN=$(curl -s -X PUT $MD/api/token \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 60")
H="X-aws-ec2-metadata-token: $TOKEN"
ROLE=$(curl -s -H "$H" $MD/meta-data/iam/security-credentials/)
curl -s -H "$H" $MD/meta-data/iam/security-credentials/$ROLE \
  | grep -E '"Type"|"Expiration"'
Y O U S H O UL D S E E
Before: Unable to locate credentials . After: an ARN ending 
assumed-role/LabRole/i-…, the app's banner turns yellow 
and notes save. The Expiration is only hours away.
A key in code works until someone deletes it. A role's credentials expire within hours, renew automatically and 
never touch your code.

## Page 11

WEEK 05 · TUTORIA L · PART 1 · STEP 2 OF 5
Step 2: How a Least-Privilege Role Is Built
The lab won't let us create roles or policies.
DO  T HI S
1 IAM → Roles → LabRole. Open Trust relationships: 
who may use this role.
2 Open Permissions: what it may do. Far more than our 
app needs.
3 IAM → Policies → Create policy → JSON. Paste the 
policy with your bucket name, then Next.
4 Name it notes-app-s3-only → Create policy. The lab 
refuses.
5 IAM → Roles → Create role → AWS service → EC2 → Next. 
Tick AmazonS3ReadOnlyAccess as a stand-in, then Next.
6 Name it notes-app-role. Read the review page, then 
Create role. Refused again.
TH E  P O L I CY  W E  W O UL D  A TTA C H
{ "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::YOUR-BUCKET" },
    { "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::YOUR-BUCKET/notes/*" } ] }
# no s3:DeleteObject: notes are a permanent record
Y O U S H O UL D S E E
Both Create buttons refused with an access -denied error. 
In a real account, you'd attach the new role to the instance 
in Step 1 instead of LabRole and the job is done.
A role has two halves: a trust policy (who can use it) and a permissions policy (what it can do).

## Page 12

WEEK 05 · TUTORIA L · PART 1 · STEP 3 OF 5
Step 3: Let the Bucket Say No
We can't shrink LabRole, but the bucket can refuse requests itself. Our rule: notes are 
permanent, and travel only over HTTPS.
DO  T HI S
1 S3 → your bucket → Permissions → Bucket policy → 
Edit.
2 Paste the policy. Replace both YOUR-BUCKETs with your 
bucket name (it's in the Bucket ARN above the editor).
3 Click Save changes.
4 In the app, click Delete on a note.
5 In S3, open notes/, tick a note, choose Delete and 
confirm.
6 In the terminal, run the two commands: HTTPS first, 
then plain HTTP .
P A S TE  T HI S , T HE N  TY P E  TH E  C O M M A N DS
{ "Version": "2012-10-17",
  "Statement": [
   { "Sid": "NotesArePermanent", "Effect": "Deny",
     "Principal": "*", "Action": "s3:DeleteObject",
     "Resource": "arn:aws:s3:::YOUR-BUCKET/notes/*" },
   { "Sid": "HttpsOnly", "Effect": "Deny",
     "Principal": "*", "Action": "s3:*",
     "Resource": ["arn:aws:s3:::YOUR-BUCKET",
                  "arn:aws:s3:::YOUR-BUCKET/*"],
     "Condition": {"Bool": {"aws:SecureTransport": "false"}} } ] }
 
aws s3 ls s3://$BUCKET/notes/
aws s3 ls s3://$BUCKET/notes/ \
  --endpoint-url http://s3.us-east-1.amazonaws.com
Y O U S H O UL D S E E
Delete is refused with AccessDenied , in the app and in the 
console, even for you. The HTTPS command lists the notes; 
the HTTP one gives AccessDenied .
An explicit Deny beats every Allow, even LabRole's. This is least privilege you can test in the lab.

## Page 13

WEEK 05 · TUTORIA L · PART 1 · STEP 4 OF 5
Step 4: Choose the Encryption Key
Since January 2023, S3 encrypts every new object for you (SSE-S3). 
DO  T HI S
1 S3 → your bucket → Properties → Default encryption . 
It already says SSE-S3, and the app shows AES256.
2 Click Edit → SSE-KMS → Choose from your AWS KMS 
keys → aws/s3.
3 Set Bucket Key: Enable, then Save changes.
4 Post a new note in the app.
5 Compare the notes on the page: the new one shows 
aws:kms, the old ones AES256.
6 Confirm it in the terminal: the command prints every 
note with its encryption.
TY P E  TH IS  IN  TH E  TE R M IN A L
# every note, with how it is encrypted at rest
for k in $(aws s3api list-objects-v2 --bucket $BUCKET \
    --prefix notes/ --query 'Contents[].Key' --output text)
do
  echo "$k  $(aws s3api head-object --bucket $BUCKET \
    --key $k --query ServerSideEncryption --output text)"
done
Y O U S H O UL D S E E
One line per note: the new note ends in aws:kms, the 
older ones still in AES256. Changing the default changes 
new objects only, existing ones keep the key they were 
written with.
With your own KMS key, reading the data also needs permission to use the key. Every use of the key is logged.

## Page 14

WEEK 05 · TUTORIA L · PART 1 · STEP 5 OF 5
Step 5: Tighten the Security Group
Port 8080 is still open to the whole internet. Only you need it.
DO  T HI S
1 EC2 → Instances → notes-app → Security tab. Click 
the security group's name.
2 Click Edit inbound rules.
3 On the 8080 rule, set Source → My IP.
4 Leave the 22 rule alone: it admits only AWS's Instance 
Connect service.
5 Click Save rules.
6 Refresh the app on your laptop. Then open it on your 
phone with Wi-Fi off.
TH E  I NB O UN D R UL E S
# before
8080  0.0.0.0/0           anyone on the internet
22    18.206.107.24/29    EC2 Instance Connect
# after
8080  <your IP>/32        only your network
22    unchanged
Y O U S H O UL D S E E
Your laptop still loads the app; your phone on mobile data 
times out. On campus Wi -Fi everyone shares one public IP , 
so classmates' laptops still get in.
Least privilege applies to networks too: open only the ports you need, to only the people who need them.
W HE N  Y O U' RE  DO N E: I N THI S  O RD E R
1.  Delete the bucket policy first, its Deny blocks step 2.
2.  Empty the bucket.
3.  CloudFormation → notes-w5 → Delete.

## Page 15

W EE K  0 5 · TUTO R IA L
Security in Action
The lecture's access ideas  and keeping spend in check.
F RO M T HE L EC TU R E: W HAT  YO U  S AW
Identities: users and roles.
Policies: what an identity may do.
Least privilege: grant only what's needed.
Encryption: protect data at rest and in transit.
P R O TE CT  Y O U R  CR E DI TS
Security adds little cost, but a running stack still does.
Stop or terminate your instance when you're not using it.
Delete test buckets and roles you no longer need.
Watch your remaining credits as the deadline nears.
IAM, encryption and cost are three Going Beyond topics for the group assignment (pick three topics to reach the top band).

## Page 16

PART 2
Y O U R  G R O U P  ·  S U P E R V I S E D
Form your groups, choose your 
project
Released after today's lecture.
≈ 45 MINUTES


## Page 17

W EE K  0 5 · TUTO R IA L
Forming Your Groups
Your individual assignment is in. The group assignment is released today.
Group Assignment: A Scalable, Highly Available Cloud Service
Group    ·    25% of the course    ·    Due Week 10
Form your group today: anyone without one by the start of week 7’s lecture will be assigned to a group.
Start ahead and choose your project: scale a member's individual service or start from a new idea.
Agree how you'll work together and start your contribution statement.
Today's IAM and encryption work can count later as one of your Going Beyond topics.


## Page 18

W EE K  0 5 · TUTO R IA L
Before Next Week
Self-study now and keep your project moving.
Confirm your group: anyone still without one will be assigned to a group.
Complete the Week 5 module (AWS Academy Module 4 · Lab 1 (IAM)). Your prep mark for Week 7.
Read the group assessment document in full before Week 7.
NE X T TU TOR IA L
Week 7 Networking & Content Delivery
After Flexibility Week: building begins, and we meet the café.

