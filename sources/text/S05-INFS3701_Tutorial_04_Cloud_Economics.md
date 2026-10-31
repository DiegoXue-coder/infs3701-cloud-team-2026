# INFS3701_Tutorial_04_Cloud_Economics.pdf

Extracted text for search; diagrams/layout must be checked in the original.

## Page 1

I N F S 3 7 0 1     ·     T E R M  3 ,  2 0 2 6
Enterprise Architecture for Scalable 
Cloud Solutions
Week 04 · Tutorial
Cloud Economics & Security Foundations
TWO -PA RT PRA CTIC AL  S ES S IO N

## Page 2

W EE K  0 4 · TUTO R IA L
Today's Tutorial
How this two-part session works.
1 Prep check: last week's Storage module
2 Recap: the demo service so far
3 This week's objectives: cost, diagrams & security
4 Part 1: we diagram and cost the demo service
5 Part 2: you diagram and cost your own service

## Page 3

W EE K  0 4 · TUTO R IA L
How This Tutorial Works
Each week: learn it on a working example, then apply it to your own assignment.
Part 1 · Instructor-led
≈ 75 min
We draw the demo service's architecture and estimate its cost with the AWS Pricing Calculator. You'll do the same for your project.
Part 2 · Your assignment
≈ 45 min
You work on your own service with help on hand, keeping progress as you go (a versioned doc and screenshots).
H OW Y OU R  TU T ORI AL M ARK  IS  S P LI T
Preparation (50%): complete the AWS Academy modules and labs set in each tutorial before the next session.
Participation (50%): work on your next assessment in the session, and keep evidence: AI-prompt screenshots, dated versions of your docs and code, and a short reflection.

## Page 4

W EE K  0 4 · TUTO R IA L
This Week's Objectives
Week 4: Cloud Economics & Security Foundations.
BY  T HE E ND,  YO U  C AN
Explain capex vs opex and total cost of ownership
Estimate a solution's cost with the Pricing Calculator
Draw a clear cloud architecture diagram
Explain the shared responsibility model
H OW T HI S  WEEK 'S  M AR K IS  S P LI T
Preparation  (50%)
The Week 3 module (Storage · Module 7, Lab 4) completed in AWS Academy before today.
Participation  (50%)
Your work in Parts 1 and 2 today, and the diagram and cost estimate you produce.
F RO M T HE L EC TU R E
Today turns this week's lecture into practice: total cost of ownership, the Pricing Calculator, and the shared responsibility model. We will apply it to the demo service.

## Page 5

PART 1
T U T O R- L E D
Costing and diagramming the demo 
service
We draw its architecture and price it up.
≈ 75 MINUTES


## Page 6

W EE K  0 4 · TUTO R IA L
What We're Pricing & Drawing
The demo service as it stands: compute, storage, interface.
Compute
The EC2 instance running the app.
Storage
The S3 bucket holding the data.
Architecture · today
We map how the pieces connect and what each costs.
These two skills (a diagram and a cost estimate) go straight into your design document (and will be asked in the final exam).

## Page 7

W EE K  0 4 · TUTO R IA L
Part 1: Cost & Diagram
Follow along with the Pricing Calculator and a quick diagram.
1 Go to the public AWS Pricing Calculator (https://calculator.aws/#/estimate).
2 Add your compute type.
3 Add your storage type and requests.
4 If possible for your case, scale the cost to the scope of your estimation and specify your assumptions.
5 Sketch the architecture, services, and how they connect.
An AI assistant can describe an architecture in words, but the diagram and the cost reasoning are yours.

## Page 8

W EE K  0 4  · T U T O R I A L
Writing Prompts for AI
Learn to write your own, the example shows the shape.
H O W  T O  W RI T E  O N E
1 Say what you're building, language, framework, what it does.
2 Add the context, where it runs and what it connects to.
3 Ask it to explain its answer , so you can justify it.
4 Run it, then refine your prompt, don't start over .
Free, no-subscription AI tools are plenty, no paid plan needed.
A N  E X A M P L E  O F  TH A T
“Describe a simple, well-structured 
architecture for a web app that uses 
EC2 for compute and S3 for storage, 
and explain what each component is 
responsible for, so I can draw a 
diagram.”
Write your own for your project, copying this won't fit your case. You still have to understand and 
explain whatever you build.

## Page 9

W EE K  0 4 · TUTO R IA L
Security Foundations
The lecture's security ideas and keeping spend in check.
F RO M T HE L EC TU R E
Shared responsibility: AWS secures the cloud; you secure what's in it.
Encryption: protect data at rest and in transit.
Right-sizing: pay for what you need, not more.
Cost awareness: tagging and budgets keep spend visible.
P R O TE CT  Y O U R  CR E DI TS
The Pricing Calculator is free, and it doesn't touch your credits.
Right-size now: a cost-aware design earns marks later .
Stop or delete anything you're only testing.
Tag resources so spend stays visible.
Cost optimisation is a Going Beyond topic.

## Page 10

W EE K  0 4 · TUTO R IA L
Drawing the Architecture
A clear diagram is worth a thousand words.
User
 EC2 · App
 S3 · Data
The demo service, as a diagram, user to app to data.
A G OOD  D IAG R AM
Group by tier or VPC
Show how data flows
Use standard AWS icons
Keep it to one page
Your architecture diagram is a required part of your design document, draw it as you build, not at the end.

## Page 11

WEEK 04 · TUTORIAL
The Demo Service Drawn
One instance in the default VPC with its notes in S3
Your browser (internet)
Region us-east-1
Default VPC
172.31.0.0/16
Internet Gateway
Availability Zone us -east-1a
DEFAULT PUBLIC SUBNET
notes-sg · port 8080 open to anyone (narrowed in 
Week 5)
Notes app
EC2 t3.micro
$
Public IPv4
$
EBS · 8 GB
$ IAM role · 
LabRole
REGIONAL SERVICE, OUTSIDE THE VPC
S3 bucket
the notes · private
encrypted at rest
$
The app reads and writes notes
using the instance's role ,
no keys in the code.
WHAT YOU PAY  FOR
$ EC2 instance
per hour , while it runs
$ EBS volume
per GB-month, even when stopped
$ Public IPv4 address
per hour , while it's assigned
$ S3
storage, requests and data out
WHO S ECU RES  WHAT
Y ou: the security group, the IAM role, 
bucket access and encryption, the app 
and its OS updates.
AWS: data centres, hardware, the 
hypervisor, and S3's durability.
One instance in one zone: fine for a demo , and the single point of failure that Weeks 7 to 10 teach you to 
remove.

## Page 12

W EE K  0 4 · TUTO R IA L
Estimating the Cost
Use the AWS Pricing Calculator and state your assumptions.
Service Monthly 12 months
EC2 t3.micro ≈ $7.50 ≈ $90
S3 (5 GB) ≈ $0.15 ≈ $1.80
Total ≈ $92
Example only:  get current prices from the Calculator.
H OW T O C OS T I T
Include every service
State your assumptions
Set the period to 12 months
Tie each figure to your 
diagram
The Pricing Calculator is free and doesn't touch your credits, use it freely to compare 
options.

## Page 13

PART 2
Y O U R  A S S I G N M E N T  ·  S U P E R V I S E D
Diagram and cost your service
Your individual assignment.
≈ 45 MINUTES


## Page 14

W EE K  0 4 · TUTO R IA L
Your Assignment: This Week's Step
Two design-document sections, done today.
Individual Assignment: Building a Cloud Service on AWS
Individual    ·    15% of the course    ·    Due Week 5 before the lecture
Draw your service's architecture diagram: it goes in your design document.
Estimate your service's cost with the Pricing Calculator and note your assumptions.
Note your security responsibilities: what you must protect? (a Week 5 focus).
Two design-document sections done today: your architecture diagram and your cost 
discussion.

## Page 15

W EE K  0 4 · TUTO R IA L
Keep Your Progress
Record as you go, it's your participation evidence and your design -doc head start.
AS  Y OU  WO RK
Draw your architecture as it stands and update it as you build.
Save your Pricing Calculator estimate and your assumptions.
BY  T HE E ND O F T OD AY
An architecture diagram of your service drawn
An xx-month cost estimate with stated assumptions
Both saved into your design document
Screenshots of your Pricing Calculator estimate
This is your participation mark and every screenshot saves you time when you write 
the design document.

## Page 16

W EE K  0 4 · TUTO R IA L
Before Next Week
Self-study now and keep your project moving.
Complete the Week 4 AWS Academy Module 2 (Cloud Economics). Your prep mark for next week.
Refine your diagram and cost estimate in your design doc.
Keep building your service toward the Week 5 deadline.
NE X T TU TOR IA L
Week 5: Securing User Access & Data
We lock down the demo service with IAM and encryption and you secure yours.

