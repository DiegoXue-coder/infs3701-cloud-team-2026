# INFS3701_Week05_Securing_User_Access_and_Data.pptx

Course: INFS3701. Searchable text; original diagrams and layout remain authoritative.

## Slide 1

INFS3701    ·    TERM 3, 2026
Enterprise Architecture for Scalable Cloud Solutions
Week 05 · Lecture
Securing User Access & Data
Tomas Lagos

Lecturer · School of Information Systems & Technology Management
tomas.lagos@unsw.edu.au

## Slide 2

Today's Lecture
Where we're headed in this session.
1
Identity is the new perimeter
2
IAM building blocks: users, groups, roles, policies
3
How a policy works: users vs roles
4
Access best practices and identity at scale
5
Protecting data: encryption at rest and in transit
6
Keys, secrets and finding sensitive data

## Slide 3

Defence in Depth
No single control is enough, protect at every layer, from the edge to your identity and data.
Edge
DDoS protection & filtering: Shield, WAF, CloudFront
Network
Isolation & firewalls: VPC, subnets, security groups, NACLs
Compute
Hardening & patching: minimal images, least privilege
Application
Secure code & secrets: input validation, Secrets Manager
Data
Encryption everywhere: at rest and in transit (KMS)
Identity
Who can do what: IAM, MFA, least privilege
From week 4 Cloud Economics & Security Foundations.

## Slide 4

Identity Is the New Perimeter
In the cloud, there's no network wall around everything. 
What matters is who can do what. So, identity and access management (IAM) is your front door.
Every request is authenticated
AWS checks identity on every API call
Every request is authorised
Policies decide if the action is allowed
Every request is logged
CloudTrail records who did what, when
Real world:  
identity is where attacks start. Phishing alone was the way in for 16% of breaches in 2025, with stolen credentials close behind (IBM Cost of a Data Breach, 2025).

## Slide 5

IAM Building Blocks
Four pieces control who can do what in your account.
Users
A person or application with its own credentials.
Groups
A collection of users that share permissions.
Roles
An identity you assume for temporary credentials.
Policies
A document that grants or denies permissions.

## Slide 6

How an IAM Policy Works
Who can do what, on which resource, under what conditions?
EXAMPLE POLICY
Effect:  
Allow
Action:  
s3:GetObject
Resource:  
reports-bucket/*
Condition:  
MFA present
WHAT EACH PART MEANS
Effect

Allow or deny the request
Action

The API calls that are permitted
Resource

Which resources (ARNs) the rule covers
Condition

Optional limits (time, IP, MFA)
By default everything is denied. Access is granted only by an explicit Allow.

## Slide 7

How AWS Decides: Policy Evaluation
Every request runs the same gauntlet. Deny always wins.
1 · Is there an explicit Deny in any applicable policy?
yes
DENIED
One Deny anywhere overrides every Allow.
no
2 · Is there an explicit Allow for this action?
yes
ALLOWED
Only an explicit Allow grants access.
no
3 · Neither applies? The default takes over.
DENIED (implicit)
Silence means no, nothing is open by default.
This is why guardrails work:  
an 
organisation
-level Deny (an SCP; coming up) can never be overridden by any account underneath it.

## Slide 8

Exercise: Critique This Policy
An intern wrote this so the reporting app could read one bucket. Two minutes. What's wrong?
THE INTERN'S POLICY
Effect:  
Allow
Action:  
s3:*
Resource:  
*
Condition:  
(none)
FIND THE PROBLEMS
1
What can this identity actually do? is it just reading?
2
Which buckets does it reach? Count them.
3
What would least privilege look like? Rewrite it.
ONE GOOD ANSWER
Effect: 
Allow    
Action: 
s3:GetObject    
Resource: 
arn:aws:s3:::reports-bucket/*
Read-only, one bucket, nothing else. Attach it to a role, not a user. Full critique in the speaker notes.

## Slide 9

Users vs Roles
Long-term credentials for people; temporary, assumable credentials for everything else.
IAM Users
Permanent credentials for an individual person or a specific app.
CREDENTIALS
Long-term (password / access keys)
BEST FOR
Human sign-in, some legacy apps
IAM Roles
Temporary credentials an identity assumes only when needed.
CREDENTIALS
Short-lived, auto-rotated
BEST FOR
EC2 & services, federation, cross-account
Prefer roles. There are no long-lived keys to leak.

## Slide 10

Roles in Action: Temporary Credentials
What actually happens when an EC2 app talks to S3.
App needs S3
No keys stored anywhere on the instance
Assumes its role
Asks AWS STS for the instance's role
Short-lived keys
Credentials auto-expire within hours
Access + audit
Calls S3, and CloudTrail logs every call
Nothing long-lived to leak.
 The keys rotate themselves. 
But remember Capital One: 
a role is only as safe as the permissions you give it.

## Slide 11

Securing Access: Best Practices
The rules that prevent most identity incidents.
Least privilege
Grant only the permissions actually needed.
Require MFA
Add a second factor to every sign-in.
Prefer roles over keys
Use temporary credentials, not long-lived keys.
Protect the root account
Lock it away and enable MFA; never use it daily.
Rotate & audit
Retire stale credentials; review access regularly.
Manage with groups
Assign permissions to groups, not one-by-one.

## Slide 12

Identity at Scale
Managing identity across many accounts and many users.
AWS Organizations
Group and govern many AWS accounts from one place.
Service Control Policies
Set account-wide guardrails on what is even allowed.
IAM Identity Center
Single sign-on and federation with your existing directory.
Amazon Cognito
Manage sign-up and sign-in for your applications' users.

## Slide 13

Protecting Data: Encryption
Two states of data.
At Rest
Data stored on disk: in S3, EBS and RDS. Encrypt it so stolen storage is useless.
How: server-side encryption with KMS keys
In Transit
Data moving across the network between clients and services.
How: TLS / HTTPS with AWS Certificate Manager
AWS encrypts much of this for you,
 but you control the keys and decide where encryption is enforced.

## Slide 14

Keys, Secrets & Sensitive Data
AWS manages the keys and the secrets so you don't have to.
AWS KMS
Create and control encryption keys; integrates with S3, EBS and RDS, and every use is logged.
Secrets Manager
Store and automatically rotate database passwords and API keys.
Certificate Manager
Provision and auto-renew the TLS certificates that power HTTPS.
AWS CloudHSM
Dedicated hardware for managing your own keys: for the strictest compliance needs.

## Slide 15

Identity & Encryption Across the Big Three
Every cloud has an identity service and a key-management service.
Service
AWS
Azure
GCP
Identity & access
AWS IAM
Microsoft Entra ID
Cloud IAM
Key management
AWS KMS
Azure Key Vault
Cloud KMS
Secrets
Secrets Manager
Key Vault
Secret Manager
WHERE EACH HAS AN EDGE
AWS
:
 
IAM offers fine-grained, resource-level access policies.
Azure
:
 
Entra ID (formerly Azure AD) leads on enterprise identity and SSO.
GCP
:
 
IAM inherits permissions down a resource hierarchy.

## Slide 16

Quick Check
Four questions before we wrap.
Q1
Your EC2 app needs to read from S3. A teammate suggests pasting access keys into a config file. What's the right alternative? and why is it safer?
Q2
A partner organisation's AWS account needs limited access to one of your buckets. Do you create them an IAM user, or something else?
Q3
TLS/HTTPS protects data in which state? And a stolen physical disk is useless thanks to encryption in which state?
Q4
Where should the app's database password live? and what should happen to it regularly?
Answers are in the speaker notes of this slide.

## Slide 17

Key Takeaways
In the cloud, identity is 
the perimeter. 
IAM controls who can do what.
IAM is built from users, groups, roles and policies; a policy says who can do what, where and when.
Prefer roles and least privilege, require MFA, and lock down the root account.
Encrypt data at rest and in transit, and control the keys with AWS KMS.
Scale identity with Organizations, SCP guardrails and IAM Identity Center.
NEXT WEEK
Networking & Content Distribution: Building a VPC
Week 6 is Flexibility Week (no class) · This week’s Tutorial: Securing User Access and Data
