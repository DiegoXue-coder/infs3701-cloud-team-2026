# INFS3701_Tutorial_03_Storage.pdf

Extracted text for search; diagrams/layout must be checked in the original.

## Page 1

I N F S3 7 0 1     ·     T E R M  3 , 2 0 2 6
Enterprise Architecture for Scalable 
Cloud Solutions
Week 03 · Tutorial
Storage: Saving Data with Amazon S3
TWO -PA RT PRA CTIC AL  S ES S IO N

## Page 2

W E E K  03 ·  T U T O R I A L
Today's Tutorial
How this two-part session works and what you'll walk out with.
1 Prep check: last week's Compute module
2 Recap the demo service so far
3 This week's objectives: Storage on S3
4 Part 1: we add storage to the demo service
5 Part 2: you add storage to your own service

## Page 3

W E E K  03 ·  T U T O R I A L
How This Tutorial Works
Each week: learn it on a working example, then apply it to your own assignment.
Part 1 · Tutor-led
≈ 75 min
We add Amazon S 3 to the demo service so it saves data. 
Follow along and do the same to your project in Part 2.
Part 2 · Your assignment
≈ 45 min
You work on your own service with help on hand, keeping 
progress as you go (a versioned doc and screenshots).
H O W  Y O U R  T U T O R I A L  M A R K  I S  S P L I T
Preparation (50%): complete the AWS Academy modules and labs set in each tutorial before the next session.
Participation (50%): work on your next assessment in the session, and keep evidence: AI -prompt screenshots, dated versions of your docs and 
code, and a short reflection.

## Page 4

W E E K  03 ·  T U T O R I A L
This Week's Objectives
Week 3: Storage on Amazon S3.
B Y T H E  E N D ,  Y O U  C A N
Explain what Amazon S 3 is and when to use it
Create a bucket and store and retrieve objects
Choose a storage class for an access pattern
Wire a web app to read and write S 3
H O W  T H I S  W E E K ' S  M A R K  I S  S P L I T
Preparation  (50%)
The Week 2 module (Compute · Module 6, Lab 3) completed in AWS Academy 
before today.
Participation  (50%)
Your work in Parts 1 and 2 today, and the progress you record (design 
document + screenshots).
F R O M  T H E  L E C T U R E
Today you'll see this week's lecture in action: buckets and objects, durability, and storage classes.

## Page 5

PART 1
T U T O R - L E D
Adding storage to the demo service
We wire the Notes app up to Amazon S3 together , step by step.
≈ 75 MI NU TES


## Page 6

W E E K  03 ·  T U T O R I A L
The Demo Service So Far
What we built last week, and what we add today.
Compute · done
The Notes app runs on an EC2 instance.
Storage · today
We add S3 so notes and uploads are saved.
Interface
The web page where users read and post 
notes.
Y ou'll add storage to your own service in Part 2, same idea on your own case.

## Page 7

W E E K  03 ·  T U T O R I A L
Part 1: Add Storage
Follow along as we connect the app to Amazon S3.
1 Create an S3 bucket: kept private.
2 Set up access: IAM role lets the app use the bucket.
3 Update the app: save each note or upload to S 3.
4 Read it back: list and display what's stored.
5 Test it: post a note, confirm it survives a refresh.
Ask an AI assistant for the S3 read/write code, then make sure you understand it.

## Page 8

W E E K  03 ·  T U T O R I A L
Writing Prompts for AI
Learn to write your own, the example shows the shape, not a script to copy.
H O W  T O  W R I T E  O N E
1 Say what you're building: language, framework, what it does.
2 Add the context: where it runs and what it connects to.
3 Ask it to explain its answer, so you can justify it.
4 Run it, then refine your prompt.
Free, no-subscription AI tools are plenty; no paid plan needed.
A N  E X A M P L E  O F  T H A T
“Update my Flask Notes app so each note is saved as 
an object in an S3 bucket, and the page lists all 
notes from the bucket. Use boto3 and explain the 
bucket calls.”
Write your own for your project: copying this won't fit your case. 
Y ou still have to understand and explain whatever you build.

## Page 9

W E E K  03 ·  T U T O R I A L
Storage in Action and the Cost
What just happened and how to protect your credits.
F R O M  T H E  L E C T U R E
Buckets & objects: where your data lives.
Storage classes: Standard, Infrequent Access, Glacier .
Private by default: block public access.
Durability: S3 keeps many copies for you.
P RO T E C T  Y OU R  C R E DI T S
S3 storage for a few small files costs very little.
Delete test buckets and objects when you're done.
Keep your EC2 instance stopped when it's not in use.
Watch your remaining credits as you go.
Right storage class = lower cost which fits the use case

## Page 10

PART 2
Y O U R  A S S I G N M E N T  ·  S U P E R V I S E D
Add storage to your service
Your individual assignment.
≈ 45 MI NU TES


## Page 11

W E E K  03 ·  T U T O R I A L
Your Assignment: This Week's Step
The individual assignment is due Week 5 before the lecture.
Individual Assignment: Building a Cloud Service on AWS
Individual    ·    15% of the course    ·    Due Week 5
Add a storage service to your app, save and retrieve its data (e.g. S 3).
Use an AI assistant for the storage code, the same way we just did.
Update your design document, note your storage choice and why.
Compute + Storage working together is the core of your assignment.

## Page 12

WE EK 03 · T UT OR IAL
First, a Choice: How Far to Wire It Up?
The lab resets between sessions, so last week's compute service is gone. Decide how much to connect today.
Storage on its own
Build and test S3 by itself: make a bucket, upload 
and read a file. Wire it into your app later or point 
it at a throwaway "dummy" instance.
GOOD IF time is short or last week's code isn't handy
The whole pipeline
Paste back your saved Week 2 code, follow the 
steps to rebuild your compute, then add S3 and 
connect the two.
GOOD IF you kept your Week 2 work and are OK with 
code
Take it gently
Let the AI guide you click-by-click in AWS: make a 
bucket, upload and download a file. No coding or 
wiring yet, connect it later with help.
GOOD IF coding isn't your strength
All three are fine today, the goal is storage working, with screenshots saved. Connecting everything can wait for the final report.

## Page 13

WE EK 03 · T UT OR IAL
Prompts to Decide and to Build
Get the AI to help you pick a path, then walk you through it step by step.
F I R S T  ·  D E CI D E
1 Saved last week's prompts and code? 2 OK reading and running code? 3 Time to spare this session?
Three yeses → the whole pipeline (Path 2). Otherwise → Storage on its own (1) or Take it gently (2).
T H E N  ·  P R OM P T  YO U R  C H OS E N  P AT H
PAT H A ·  STORAGE ON  I TS OWN
“Help me build just the storage part: create an S3 bucket and a short script to upload and download one file. We'll connect it 
to the app later.”
PAT H B · THE WHOLE  PI PE LIN E
“Here are last week's prompts and code: [paste]. Help me rebuildmy compute service, then add an S3 bucket it reads from and 
writes to. Step by step, please.”
PAT H C ·  TAKE IT GE NTLY
“I'm new to coding. Show me step by step how to make an S3 bucket in the console and upload a file. Don't assume I know my way 
around.”

## Page 14

W E E K  03 ·  T U T O R I A L
Keep Your Progress
Record as you go. It's your participation evidence and your design -doc head start.
A S  Y O U  W O R K
Keep a versioned design document: date each 
version as it grows.
Screenshot each milestone: your settings and your 
app responding.
B Y T H E  E N D  O F  T O D A Y
Your app saves data to a storage service
Stored data is read back and displayed
Storage choice noted in your design doc
Screenshots of your bucket and working app saved
This is your participation mark and every screenshot saves you time when you write the report document.

## Page 15

W E E K  03 ·  T U T O R I A L
Before Next Week
Self-study now and keep your project moving.
Complete the AWS Academy Module 7 and Lab 4 (Storage). Your prep mark for next week.
Stop or terminate anything you're not using.
Keep building your service toward the Week 5 deadline.
N E X T  T U T O R I A L
Week 4: Cloud Economics & Security Foundations
We cost and diagram the demo service, so you do the same for your project.

