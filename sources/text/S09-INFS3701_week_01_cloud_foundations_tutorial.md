# INFS3701_week_01_cloud_foundations_tutorial.pdf

Extracted text for search; diagrams/layout must be checked in the original.

## Page 1

I N F S 3 7 0 1     ·     T E R M  3 ,  2 0 2 6
Enterprise Architecture for Scalable 
Cloud Solutions
Week 01 · Tutorial
Cloud Foundations: Getting Started on AWS
H A N D S- O N  L A B  S E S S I O N

## Page 2

W E E K  0 1  ·  T U T O R I A L
Today's Tutorial
What we'll cover, and how this session works.
1 How the course tutorials work?
2 The course schedule
3 This week's objectives
4 Preparation and the AWS Academy lab
5 Your individual assignment is released today

## Page 3

W E E K  0 1  ·  T U T O R I A L
How Tutorials Work
From Week 2, each two-hour session runs in two parts. Learn it on a working example, then apply it.
Part 1 · Together
We build a working example, 
step by step.
Part 2 · Your work
You apply it to your own 
assignment.
Reinforces the lecture
Each tutorial builds on that 
week's lecture topic.
Prepare, then participate
AWS module to complete 
before the next tutorial
(Participation mark).

## Page 4

W E E K  0 1  ·  T U T O R I A L
How You're Marked Each Week
Your tutorial mark is split evenly: preparation before, participation during.
Preparation
50% of the tutorial mark
Complete the AWS Academy modules and labs set for the week 
before your next session.
Participation
50% of the tutorial mark
Work on your assessment in the session, and keep evidence: AI -prompt 
screenshots, dated versions of your docs and code, and a short reflection.
G O O D  T O  K N OW
Preparation and participation each count for half of that week's tutorial mark.
Do the preparation before the session: the AWS Academy module and lab set for the week.
Keep your evidence in one place: it's also a head start on your assessment write-up.

## Page 5

W E E K  0 1  ·  T U T O R I A L
The Course Schedule
Each tutorial reinforces that week's lecture, using AWS Academy.
Wk Tutor ia l topi c AWS Academ y (C om pl e te by)
1 Cloud Foundations
2 Compute: Amazon EC2 Learner Lab + Modules 1 & 3
3 Storage Module 6 · Lab 3
4 Cloud Economics Module 7 · Lab 4
5 Securing User Access & Data Module 2
7 Networking & Content Delivery Module 4 · Lab 1
8 Databases Module 5 · Lab 2
9 Logging, Monitoring & Incidents Module 8 · Lab 5
10 Auto Scaling Modules 9 & 10 – Lab 6
No tutorial in Week 6 (Flexibility Week).

## Page 6

W E E K  0 1  ·  T U T O R I A L
This Week's Objectives
Week 1: Cloud Foundations.
B Y T H E  E N D ,  Y O U  C A N
Explain what cloud computing is and its value
Distinguish IaaS, PaaS and SaaS service models
Distinguish public, private and hybrid deployment
Describe AWS's global infrastructure
H O W  T H I S  W E E K ' S  M A R K  I S  S P L I T
Preparation  (50%)
No preparation mark this week.
Participation  (50%)
Set up your AWS Academy account and open the Learner Lab.
F R O M  T H E  L E C T U R E
As you explore the console, spot the ideas from this week's lecture: the three service models, the deployment models, and AWS's global 
infrastructure of Regions and Availability Zones.

## Page 7

W E E K  0 1  ·  T U T O R I A L
Participation: AWS Academy Learner Lab
Complete this in the tutorial
A C C E S S  T H E  L E A R N E R  L A B
1 Check your UNSW email for the AWS Academy invitation.
2 Follow the instructions in the email to register .
3 Open the AWS Academy Learner Lab course on your 
dashboard.
T H E N  C O M P L E T E
The 'Compliance and Security' section in the Learner Lab.
The module Knowledge Check (your first attempt is the one that 
counts).
Walk through 'Launch AWS Academy Learner Lab' so you're 
ready to build.
This Learner Lab is the same environment you'll use for your individual assignment.

## Page 8

WEEK 01 · TUTORIAL
The Individual Assignment: What to Build?
A small cloud service that is genuinely your own.
Pick a project that needs both
Photo or file upload, a notes or guestbook 
app, an image gallery, a link shortener, or 
your own idea. Keep it small and focused.
Compute + storage, together
Your code does real server-side work on 
EC2 or Lambda, reads and writes storage 
such as S3, behind a usable interface. A 
static page alone will not pass.
Go beyond for the top band
Add three justified ideas from Weeks 1-4
(least-privilege IAM, a cost-smart storage 
class) and explain why each one helps.
HAND IN
Your deployed AWS service :
· a design document (PDF, under 2,000 words) 
· a one-minute video.  
Worth 15%, due Week 5 before the lecture .

## Page 9

W E E K  0 1  ·  T U T O R I A L
Your Individual Assignment
Released today.
Building a Cloud Service on AWS
Deploy a real cloud service on AWS: compute, storage and an interface (justify it).
Individual    ·    15% of the course    ·    Due Week 5
The core is to set compute and storage working together . This is built up week by week through the Week 2 -4 tutorials.
Top marks reward Going Beyond: extend your service with concepts from Weeks 1 -4 and justify them.
Find the full brief and marking scheme on Moodle. Submit your deployed service, a design document and a one -minute video.
Y ou'll build this up in the Week 2-4 tutorials. Keep a versioned design doc and screenshots as you go.

## Page 10

WEEK 01 · TUTORIAL
Using AI to Build Your Service
Using AI to write your code is encouraged, free tools are fine. What is marked is that you understand it.
H OW T O P RO M PT  W EL L
1 Ask for the step-by-step to set up the service on AWS.
2 Name the language: say "use Python" or "use JavaScript".
3 New to coding? Ask the AI to write the code and help you deploy it.
4 Give context: the AWS service and what it connects to.
5 Ask it to explain the code, then refine it if it is wrongor it does not work.
E XA M PL E  PR O MP T S
”Give me step-by-step instructions to configure an 
EC2 instance and deploy my app."
"Write the app in Python using Flask."
"I am new to programming — please help me produce 
the code and deploy it."
"This runs on a Lambda that reads and writes an S3 
bucket — keep that in mind."
Always test AI-generated code yourself and never paste credentials or secrets into a prompt.

## Page 11

W E E K  0 1  ·  T U T O R I A L
After the Lab: Modules 1 & 3
Week 2 Preparation mark.
Module 1: Cloud 
Concepts
Read the guide and complete the Module 
1 Knowledge Check.
Module 3: Global 
Infrastructure
Read the guide and complete the Module 
3 Knowledge Check.
Explore the console
Launch the lab; switch the Region 
selector to see the global footprint.
T I E  I T  B A C K  T O T HE  L E C T U R E
In the console, find a service for each model: 
compute you manage (IaaS), a managed platform (PaaS), a ready-to-use app (SaaS). 
Switch the Region selector to see AWS's global footprint first-hand.

## Page 12

W E E K  0 1  ·  T U T O R I A L
Before Next Week
A quick checklist to keep you on track.
Register for AWS Academy and open the Learner Lab.
Complete the Module 1 and Module 3 Knowledge Checks.
Read the individual assignment brief on Moodle.
N E X T  T U T O R I A L
Week 2 Compute with Amazon EC2
AWS Academy · Module 6 · Lab 3

