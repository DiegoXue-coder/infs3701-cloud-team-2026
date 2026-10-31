# INFS3701_week_02_compute_tutorial.pdf

Extracted text for search; diagrams/layout must be checked in the original.

## Page 1

I N F S 3 7 0 1     ·     T E R M  3 ,  2 0 2 6
Enterprise Architecture for Scalable 
Cloud Solutions
Week 02 · Tutorial
Compute: Running Your Code on Amazon EC2
TWO -PA RT PRA CTIC AL  S ES S IO N

## Page 2

W E E K  0 2  ·  T U T O R I A L
Today's Tutorial
How this two-part session works and what you'll walk out with.
1 Preparation check: last week's module
2 How this tutorial works, and how you're marked
3 This week's objectives: Compute on EC2
4 Part 1: we build the demo service together
5 Part 2: you start your own assignment

## Page 3

W E E K  0 2  ·  T U T O R I A L
How This Tutorial Works
Each week: learn it on a working example, then apply it to your own assignment.
Part 1 · Instructor-led
≈ 75 min
We build the demo service together on AWS. 
You'll repeat each step on your own project in Part 2.
Part 2 · Your assignment
≈ 45 min
You work on your own service with help on hand, keeping 
progress as you go (a versioned doc and screenshots).
H O W  Y O U R  T U T O R I A L  M A R K  I S  S P L I T
Preparation (50%): complete the AWS Academy modules and labs set in each tutorial before the next session.
Participation (50%): work on your next assessment in the session, and keep evidence: AI -prompt screenshots, dated versions of your docs and 
code, and a short reflection.

## Page 4

W E E K  0 2  ·  T U T O R I A L
This Week's Objectives
Week 2 Compute on Amazon EC2.
B Y T H E  E N D ,  Y O U  C A N
Explain what Amazon EC2 is and when to use it
Launch an instance and connect to it
Choose an instance type and AMI for a workload
Deploy and run a small web app on EC2
H O W  T H I S  W E E K ' S  M A R K  I S  S P L I T
Preparation  (50%)
The Week 1 module (Cloud Foundations) completed in AWS Academy before 
today.
Participation  (50%)
Work on your assessment in the session, and keep evidence: AI -prompt 
screenshots, dated document and code versions, and a short reflection.
F R O M  T H E  L E C T U R E
Today you'll see this week's lecture in action (instance types and sizing, AMIs, security groups and the EC2 lifecycle( on a real, running service.

## Page 5

PART 1
T U T O R - L E D
Building the demo service's compute tier
We stand up a small web app on Amazon EC2 together, step by step.
≈ 7 5 M INUTES


## Page 6

W E E K  0 2  ·  T U T O R I A L
Meet the Demo Service
Our working example for the next few weeks: a small Notes app.
Users post short notes that are saved and listed back. It needs compute, storage and an interface, the same shape as your ind ividual assignment 
on a different case.
Compute  ·  today
A small web server, running on EC2, that 
handles requests.
Storage  ·  Week 3
Where the notes are saved, we add this 
next week.
Interface
A simple web page where users read and 
post notes.
Y ou'll build your own service on your own case, not this one. The demo is here to show you how the pieces fit.

## Page 7

W E E K  0 2  ·  T U T O R I A L
Part 1: Build the Compute Tier
Follow along as we launch and run the app on EC2.
1 Launch an EC2 instance: the Amazon Linux AMI with a t3.micro size.
2 Set the security group: allow only the web port (and your admin access).
3 Connect with EC2 Instance Connect.
4 Install the runtime, then deploy the app code.
5 Open the public address in a browser and the Notes app.
We'll write the app's code with an AI assistant in the next step; you don't type it from scratch.

## Page 8

W E E K  0 2  ·  T U T O R I A L
Writing Prompts for AI
Learn to write your own, the example shows the shape, not a script to copy.
H O W  T O  W R I T E  O N E
1 Say what you're building: language, framework, what it does.
2 Add the context: where it runs and what it connects to.
3 Ask it to explain its answer, so you can justify it.
4 Run it, then refine your prompt, don't start over .
Free, no-subscription AI tools are plenty and enough for this use.
A N  E X A M P L E  O F  T H A T
“Write a small Python Flask app where users post a 
short note and see all notes. Give me the code and 
the commands to run it on an Amazon Linux EC2 
instance and explain each part.”
Write your own for your project. Copying this won't fit your case. Y ou still have to understand and explain whatever you build.

## Page 9

W E E K  0 2  ·  T U T O R I A L
Compute in Action
What just happened, and how to protect your credits.
F R O M  T H E  L E C T U R E
Instance type & sizing: a t3.micro for a small workload.
The AMI: the image your instance starts from.
The security group: your instance's virtual firewall.
The EC2 lifecycle: running, stopped, terminated.
P RO T E C T  Y OU R  C R E DI T S
Your Learner Lab runs on a limited budget of credits.
Stop your instance when you're not using it. A running instance 
burns credits around the clock.
Terminate anything you no longer need.
Keep instances small; you're learning, not running production.
Lambda is the lower-cost option, it only runs when called.

## Page 10

PART 2
Y O U R  A S S I G N M E N T  ·  S U P E R V I S E D
Get your own compute tier running
Apply what we just did to your own service. Help is on hand.
≈ 4 5 M INUTES


## Page 11

W E E K  0 2  ·  T U T O R I A L
Your Assignment: This Week's Step
The individual assignment is due Week 5 before the lecture.
Individual Assignment Building a Cloud Service on AWS
Individual    ·    15% of the course    ·    Due Week 5
Choose your project (compute + storage + interface).
Today's goal: get your compute running: an EC2 instance serving your app or decide on Lambda and note why.
Use an AI assistant to write your first version, the same way we just did.
Don't aim to finish today! Aim to get something running and learn how the pieces fit.

## Page 12

W E E K  0 2  ·  T U T O R I A L
Keep Your Progress
Record as you go: it's your participation evidence and your design -doc head start.
A S  Y O U  W O R K
Keep a versioned design document: date each 
version as it grows.
Screenshot each milestone: your instance, your app 
responding, your settings, your prompts.
B Y T H E  E N D  O F  T O D A Y
Your service idea chosen and noted
An EC2 instance running (or a Lambda decision made)
Your app responding at its address (even a hello -world)
Screenshots and a first sketch saved in your design doc
This is your participation mark, and every screenshot saves you time when you write the design document.

## Page 13

W E E K  0 2  ·  T U T O R I A L
Before Next Week
Self-study now and keep your project moving.
Complete the Week 2 module: AWS Academy Module 6 · Lab 3 (Amazon EC2). This is your preparation mark for next week.
Tidy up: stop or terminate any instances so you don't waste credits.
Keep building your service toward the Week 5 deadline.
N E X T  T U T O R I A L
Week 3: Storage
We add storage to the demo service, and you add it to yours.

