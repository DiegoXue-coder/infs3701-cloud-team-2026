# INFS3701_Week04_Cloud_Economics_and_Security_Foundations.pdf

Extracted text for search; diagrams/layout must be checked in the original.

## Page 1

I N F S 3 7 0 1     ·     T E R M  3 ,  2 0 2 6
Enterprise Architecture for Scalable 
Cloud Solutions
Week 04 · Lecture
Cloud Economics & Security Foundations
T omas Lagos
Lecturer · School of Information Systems & Technology Management
tomas.lagos@unsw.edu.au

## Page 2

Today's Lecture
Where we're headed in this session.
1 The economics of cloud
2 Tracking and controlling cost with AWS tools
3 The threat landscape
4 The shared responsibility model
5 Confidentiality, integrity, availability
6 Defence in depth, and the Well-Architected security pillar
7 The AWS security toolbox
8 Governance, compliance, and continuous security

## Page 3

The Economics of Cloud
Why moving to the cloud changes the shape of the bill.
From capex to opex
No large upfront hardware purchase, 
you rent capacity and pay as you go.
Pay only for what you use
Switch resources off and the charges 
stop; spend rises and falls with 
demand.
Economies of scale
AWS buys at vast scale and passes the 
lower unit prices on to its customers.
Total cost of ownership
Weigh the whole picture (power, 
space, staff) not just the price.
Detailed compute pricing (On-Demand, Reserved, Spot and Savings Plans) was covered in the Week 2 
Compute lecture.

## Page 4

Tracking & Controlling Cost
AWS gives you tools to estimate, see and cap what you spend.
AWS Pricing Calculator
Estimate the monthly cost of a design before you build it.
AWS Cost Explorer
Visualise spending over time and see which services drive it.
AWS Budgets
Set a threshold and get alerted before you overspend.
Consolidated billing
One bill across many accounts via AWS Organizations,  with volume discounts.
That covers the business of cloud, the rest of today is about keeping it secure.

## Page 5

Real Case: The Bill Nobody Budgeted For
Self-service makes it easy to launch resources, and easy to lose track of what they cost.
THE SU RPRIS E WHY IT HAPP ENS
Pinterest
~US$190M on AWS in a year. About $20M over 
budget.
Intuit
AWS bill up 93% to ~US$145M.
Lyft
~US$300M AWS contract, roughly $8M every 
month.
Easy to spin up
Anyone can launch resources with no red tape.
Hard to see in time
Spend is tough to track live; bills land weeks 
later .
Lift-and-shift waste
Old apps moved without rewriting run 
inefficiently.
This is exactly why you tag resources, watch Cost Explorer, and set Budgets with alerts; the tools on the last 
slide exist for this.
Reported by The Information, 2019; Lyft figures from its S -1 filing.

## Page 6

Cost Models Across the Big Three
Same pay-as-you-go idea, but each provider discounts differently.
Discount lever AWS Azure GCP
Commit 1–3 years Savings Plans / Reserved Reservations Committed-use discounts
Spare capacity Spot Instances Spot VMs Spot / Preemptible VMs
No commitment — — Sustained-use discounts (automatic)
W H E R E  E A C H  HA S  A N  E D G E
AWS: Savings Plans and Spot give deep, flexible discounts.
Azure: Hybrid Benefit reuses existing Windows Server / SQL licences.
GCP: sustained-use discounts apply automatically, with no commitment.

## Page 7

What a Breach Costs
The financial stakes behind everything in this lecture.
Source: IBM Cost of a Data Breach reports, 2021 –2025
US$10.22M
record average breach 
cost in the United States, 
2025
241 days
mean time to identify 
and contain a breach (a 
9-year low)
US$1.9M
average saving for heavy 
users of security AI & 
automation
Defence is cheaper than failure, and detection speed is where the money moves (that's Week 9's 
topic).

## Page 8

The Shared Responsibility Model
AWS secures the cloud; you secure what you put in it.
AWS
Security OF the cloud
YOU
Security IN the cloud
Physical data centres
Hardware & networking
The virtualisation layer
Managed-service software
Your data & content
Identity & access (IAM)
OS, network & firewall config
Encryption (in transit & at rest)
Application security

## Page 9

Responsibility Shifts by Service Type
The more managed the service, the more AWS secures for you, and the less you tune.
Infrastructure
e.g., Amazon EC2
You manage the OS, patching, firewall, 
network and your data. AWS secures the 
hardware beneath.
Platform
e.g., Amazon RDS
AWS runs the OS and database engine. You 
handle your data, access and network 
settings.
Abstracted
e.g., S3, DynamoDB, KMS
You manage your data and who can reach it. 
AWS does almost everything else.
AWS takes on more of the work →
◄  More to customize; more is on you Less to customize; more built in  ►
AWS hands you the locks, you still have to use them. 
A managed service like RDS won't stop you leaking its credentials.

## Page 10

The Threat Landscape
What are we actually defending against?
Data breaches & loss
Sensitive data exposed, 
leaked or destroyed
Unauthorised access
Stolen credentials and 
account hijacking
Denial of service
Attacks that overwhelm 
and take systems down
Misconfiguration
Open buckets and loose 
rules. The #1 cause
Most cloud incidents are self-inflicted.
Gartner famously predicted that through 2025, 99% of cloud security failures would be the 
customer's fault.
Yet cloud is usually safer than running it yourself. AWS gives one view of every asset, certified compliance 
(PCI-DSS, HIPAA, FISMA) and automated guardrails, strengths most in-house teams can't match. 
The catch: those protections only help if you switch them on.

## Page 11

The CIA Triad
Every security control serves one of three goals.
Confidentiality
Only the right people can 
see the data.
Encryption · access control
Integrity
Data isn't altered or 
tampered with.
Hashing · versioning · signing
Availability
Systems and data are there 
when needed.
Redundancy · backups · DDoS 
defence

## Page 12

Defence in Depth
No single control is enough, protect at every layer, from the edge to your identity and data.
Edge DDoS protection & filtering: Shield, WAF, CloudFront
Network Isolation & firewalls: VPC, subnets, security groups, NACLs
Compute Hardening & patching: minimal images, least privilege
Application Secure code & secrets: input validation, Secrets Manager
Data Encryption everywhere: at rest and in transit (KMS)
Identity Who can do what: IAM, MFA, least privilege

## Page 13

Case: Capital One, 2019
One misconfiguration that led to a chain of failures.
H O W  I T  U N F O L D E D
1
A misconfigured WAF on an EC2 instance let an 
attacker make the server send requests on her 
behalf (SSRF).
2 The server was tricked into handing over the 
temporary credentials of its own IAM role.
3 That role was wildly over-privileged, it could list and 
read more than 700 S3 buckets.
4 Data on ~106 million people was copied out and 
discovered four months later, via an outside tip.
L A Y E R  BY  L A Y E R
Application
WAF misconfigured, SSRF possible FAILED
Identity
Role had far more access than needed FAILED
Data
Encrypted: but the role could read it FAILED
Detection
Exfiltration unnoticed for months FAILED
The bill:  a US$80M regulatory fine plus a US$190M settlement and every failure sat on the customer's side of 
the shared responsibility line. 
Sources: OCC (2020); US DOJ; public reporting.

## Page 14

The Well-Architected Security Pillar
AWS's design principles for building secure systems.
Strong identity foundation
Centralise identity; grant 
least privilege.
Enable traceability
Log, monitor and audit every 
action.
Security at all layers
Apply defence in depth, not 
one perimeter.
Automate security
Build guardrails and controls 
as code.
Protect data everywhere
Encrypt in transit and at rest 
by default.
Prepare for events
Plan, practise and automate 
incident response.

## Page 15

Security Is Continuous
Not a one-off project, an ongoing cycle of identify, protect, detect, respond and recover.
Identify
Know your assets & risks
Protect
Put controls in place
Detect
Spot threats early
Respond
Contain and fix
Recover
Restore and learn
…then back to Identify.

## Page 16

The AWS Security Toolbox
A service for every part of the job.
Identity
IAM
Organizations
IAM Identity Center
Detect
CloudTrail
GuardDuty
Config
Protect network
Security Groups
WAF
Shield
Protect data
KMS
Macie
Secrets Manager
Respond
Security Hub
Detective
Inspector
Identity (IAM) and data protection get a full week next week.

## Page 17

AWS Security Services, Up Close
What the toolbox services actually do.
Amazon GuardDuty
Watches logs for threats, odd API calls, crypto-
mining, leaked keys.
Amazon Inspector
Scans your workloads for known vulnerabilities 
and weak config.
Amazon Macie
Uses ML to find sensitive data (PII) sitting in 
your S3 buckets.
AWS WAF + Shield
Filter malicious web traffic and absorb large 
DDoS attacks.
AWS Security Hub
One dashboard that pulls together findings 
from all the above.
Amazon Detective
Connects the dots across logs to investigate an 
incident.
You don't wire these up by hand for the assignment, but knowing what each one watches is part of thinking 
securely.

## Page 18

Governance & Compliance
Keeping data where it must be.
Shared compliance
AWS certifies the platform (ISO, SOC, 
PCI); you certify how you use it.
Guardrails at scale
AWS Organizations and Control T ower 
enforce policy across accounts.
Continuous compliance
AWS Config tracks resource settings 
against your rules.
Data sovereignty
Choose Regions to meet local data-
residency laws.

## Page 19

Running Many Accounts: AWS Organizations
Big companies don't run one AWS account, they run dozens. Organizations ties them together.
One bill, volume discounts
Consolidate every account's spend into one invoice and 
earn volume pricing.
Group by team or stage
Organise accounts into units (Finance, HR, Prod, Dev ) 
that mirror the business.
Govern from one place
Apply the same guardrails to every account at once.
Keep Prod away from Dev
Separate accounts contain the blast radius : a Dev slip 
can't touch Production.
Audit centrally
See activity across the whole organisation in one place.
Onboard teams fast
Spin up a new account with your standards already 
baked in (Control Tower).
Example: a retailer gives Finance, Marketing and Engineering their own accounts : one bill, the same 
guardrails on all three, full visibility for auditors. 
The policy mechanics (SCPs, IAM) come next week.

## Page 20

Security Across the Big Three
Every provider protects the same things.
Security need AWS Azure GCP
Identity & access IAM + Identity Center Microsoft Entra ID Cloud IAM
Threat detection Amazon GuardDuty Defender for Cloud Security Command Center
Web firewall & DDoS AWS WAF + Shield Azure WAF + DDoS Protection Cloud Armor
Keys & secrets KMS + Secrets Manager Azure Key Vault Cloud KMS + Secret Manager
Account governance AWS Organizations Management groups Folders + Org Policy
W H E R E  E A C H  HA S  A N  E D G E
AWS: the widest set of specialised services; you pick and combine them yourself.
Azure: Defender for Cloud bundles detection and posture into one product, tied to Microsoft 
identity.
GCP: Security Command Center gives a single console; Cloud Armor is built into its global load 
balancer .

## Page 21

Key Takeaways
Under the shared responsibility model, AWS secures the cloud and you secure what's in it.
Security serves confidentiality, integrity and availability (the CIA triad).
Defend in depth: layer controls from the edge down to identity and data.
AWS gives you a toolbox across identity, detection, network, data and compliance.
Security is continuous, with guardrails (Organizations, Config) to keep you compliant.
N E X T  WE E K
Securing User Access & Data
Identity & access management, encryption and key management ·This week’s Tutorial: Cloud 
Economics (Module 2)

