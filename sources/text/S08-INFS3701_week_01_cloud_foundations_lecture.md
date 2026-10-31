# INFS3701_week_01_cloud_foundations_lecture.pptx

Extracted text for search; diagrams/layout must be checked in the original.

## Slide 1

INFS3701    ·    TERM 3, 2026
Enterprise Architecture for Scalable Cloud Solutions
Week 01 · Lecture
Cloud Foundations
Tomas Lagos

Lecturer · School of Information Systems & Technology Management
tomas.lagos@unsw.edu.au

## Slide 2

Summary of 
Assessments
Class Preparation & Participation
20%
Group 
Assignment
25
%
Final Exam
40
%
Preparation (50%): 
finish the week's AWS Academy knowledge check before the tutorial.
Participation (50%): 
work on your assessment in the session, keeping evidence.
As a group, take one member’s individual service (optional) and rearchitect it into a scalable, highly available solution, then justify your design.
Build and deploy a working cloud service on AWS using compute and storage, then explain your design choices in a short document and video.
2 hours plus 15 minutes reading, 5 questions 
a
pplying concepts to realistic scenarios and justifying your design choices. One A4 note page allowed.
Individual Assignment
15
%
INFS3701
Enterprise Architecture for Scalable Cloud Solutions

## Slide 3

INFS3701 - 
Enterprise Architecture for Scalable Cloud Solutions
1
2
3
4
5
6
7
8
9
10
Weeks
Topics
Cloud Foundations
Cloud Architecting Compute
Cloud Architecting Storage
Cloud Economics & Security Foundations
Securing User Access & Data: IAM & encryption
Flex week
P&P
P&P
Logging, monitoring, and managing incidents
Networking
Group Assignment Submission
Final 
Exam
Assessments
Databases
Auto scaling
In tutorial
In tutorial
Moodle submission
Inspera
Individual Assignment Submission
Moodle submission

## Slide 4

We use 
Moodle
 
for communications
Moodle
 will be used for all weekly materials, assignment submissions, and lecture recordings.
If you have any questions regarding the materials or the assessment, post on the Q&A forum. 
Responses can come from peers or the teaching team
WE WILL NOT RESPOND TO QUESTIONS RELATED TO THE COURSE VIA EMAIL. 
The only queries we will respond to via email will be those of a personal nature, if relevant for the course
4

## Slide 5

How This Course Fits Together
INFS3701 is built around three connected themes.
01
Architecting Scalable Infrastructure
Design and scale systems across the IaaS, PaaS and SaaS models  (compute, storage, databases and networking).
02
Security & Governance Guardrails
Keep environments secure and compliant with IAM, policy enforcement, monitoring and incident response.
03
Enterprise Service Delivery
Operate cloud services well: quality assurance, incident management, SLAs and IT service governance.

## Slide 6

Today's Lecture
Where we're headed in this session.
1
What cloud computing actually is
2
Traditional IT versus the cloud
3
The three service models: IaaS, PaaS and SaaS
4
Public, private and hybrid deployment
5
How AWS's global infrastructure is built
6
Why cloud is a business strategy, not just IT

## Slide 7

What Is Cloud Computing?
On-demand delivery of IT resources over the internet, 
with pay-as-you-go pricing  (no owning or running the hardware yourself).
FIVE ESSENTIAL CHARACTERISTICS
On-demand self-service
Provision resources yourself, instantly
Broad network access
Reach services from anywhere, any device
Resource pooling
Shared infrastructure across many tenants
Rapid elasticity
Scale out and back in as demand moves
Measured service
Pay only for what you actually use

## Slide 8

Six Advantages of the Cloud
Why 
organisations
 move?
Trade CapEx for OpEx
Swap big upfront purchases for flexible, variable spend.
Economies of scale
Aggregated demand drives lower pay-as-you-go prices.
Stop guessing capacity
Match real demand instead of over- or under-provisioning.
Speed and agility
New resources are minutes away, not weeks or months.
No more data centres
Drop the heavy lifting of racking, powering and cooling.
Go global in minutes
Deploy close to users almost anywhere in the world.

## Slide 9

Traditional IT versus the Cloud
The shift is financial and operational.
On-Premises
Cloud
Upfront cost
Capital purchase (CapEx)
Pay-as-you-go (OpEx)
Provisioning
Weeks to months
Minutes
Scaling
Sized for peak demand
Elastic (up and down; in and out)
Maintenance
You patch and run it
Provider does the heavy lifting
Global reach
A data centre per region
New regions in minutes
Fixed capacity vs elastic capacity over a day (illustrative)

## Slide 10

Case: When Demand Breaks Fixed Capacity
Taylor Swift's Eras Tour presale crashes Ticketmaster (November 2022).
Illustrative reconstruction · Sources: Ticketmaster statement (Nov 2022); NPR; Variety
3.5 billion
system requests hit the platform in a single day
4×
the platform's previous record peak
~14 million
fans (and bots) arriving at once
2.4 million
tickets still sold: a single-day record
The architecture lesson:  
capacity sized for a normal day fails on launch day. 
Elasticity:
 scale for the spike (release it after). This is the cloud's core promise (and Week 10's topic).

## Slide 11

Cloud Service Models: Who Manages What
Move from IaaS to SaaS and more of the stack shifts to the provider.
Applications
Data
Runtime
Middleware
Operating System
Virtualisation
Servers
Storage & Networking
On-Premises
Your data centre
IaaS
EC2 · EBS · VPC
PaaS
RDS · Beanstalk
SaaS
QuickSight · WorkSpaces
You manage
Cloud provider manages

## Slide 12

The Three Models at a Glance
IaaS
Infrastructure as a Service
WHAT IT IS
Raw compute, storage and networking that you configure and control.
EXAMPLE
Amazon EC2, EBS, VPC
BEST WHEN
Migrating legacy systems or needing full control of the OS.
PaaS
Platform as a Service
WHAT IT IS
A managed platform to build and run apps without managing servers.
EXAMPLE
Elastic Beanstalk, Amazon RDS
BEST WHEN
Teams that want to focus on code, not infrastructure.
SaaS
Software as a Service
WHAT IT IS
Ready-to-use applications delivered to you over the internet.
EXAMPLE
Amazon QuickSight, WorkSpaces
BEST WHEN
Standard business needs with zero maintenance.

## Slide 13

Cloud Deployment Models
Where the infrastructure lives shapes control, cost and compliance.
Public
Shared provider infrastructure, on demand over the internet.
AWS · Azure · GCP
Private
A dedicated environment for a single organisation.
On-prem or hosted private cloud
Hybrid
Public and private working together as one system.
Burst to cloud at peak demand
Multi-cloud
More than one public cloud provider, by design.
Avoid lock-in · best-of-breed

## Slide 14

How AWS Global Infrastructure Is Built
A hierarchy designed for performance, resilience and data residency.
39  
Geographic Regions
123  
Availability Zones
+2  
Regions announced
Regions
Separate geographic areas (e.g. Sydney, Tokyo). You choose where your data and workloads live.
Availability Zones
One or more isolated data centres inside a Region, each with independent power and cooling.
Edge Locations
Hundreds of sites worldwide that cache content close to users for low latency.
Footprint: AWS Global Infrastructure, 
aws.amazon.com
 (June 2026) (announced: Saudi Arabia, Chile)
WHY THREE LAYERS
Lower latency

Serve users from nearby
Fault isolation

Zones fail independently
Data residency

Meet local compliance rules

## Slide 15

Cloud Is a Business Strategy
How can organisations create value using the cloud?
Cloud turns IT from a fixed cost centre into a flexible engine for growth (letting teams experiment, scale and reach customers faster).
Experiment & innovate
Spin up ideas cheaply and fail fast: the cost of trying something new drops sharply.
Reach customers globally
Serve users anywhere with low latency, while meeting local data rules.
Turn data into products
Pool and analyse data at scale to build smarter, more personalised services.

## Slide 16

The Market Is Voting With Its Wallet
Worldwide end-user spending on public cloud services.
Source: Gartner public cloud forecasts (Nov 2024; 3Q25 update)
+21.5%
growth in 2025 alone
90%
of organisations expected to adopt hybrid cloud through 2027
US$1.48T
projected market size by 2029
For an IS professional, cloud skills aren't a niche: they're where the industry's money and jobs are moving.
Forecasts in 2025 show that 55% of workloads for Australian 
organisations
 will be hosted on public clouds (Source: 
adapt.com.au
).

## Slide 17

Digital Transformation
Using the cloud and new technology to reinvent how a business creates value.
An example
McDonald’s
It reinvented ordering with self-service kiosks and AI-driven voice ordering
:
 shifting from staff-taken orders to a fast, digital, customer-led experience.
Getting it right
—  Ask the right questions
:
 serve customers better, not just faster
—  Get leadership buy-in from the C-suite
—  Define clear objectives and avoid scope creep
—  Work in agile iterations
:
 ship, learn, adjust
—  Encourage smart risk-taking; learn from failure
—  Know one-way vs two-way-door decisions
—  Set clear roles and responsibilities

## Slide 18

The 7 Rs of Cloud Migration
Seven ways to move a workload to the cloud
,
 pick the right one per application.
Rehost
Lift and shift, as-is
Re-platform
Lift, tinker and shift
Refactor
Re-architect, cloud-native
Relocate
Move infrastructure as-is
Repurchase
Drop and shop
:
 move to SaaS
Retain
Keep on-prem, revisit later
Retire
Decommission and switch off
Most migrations mix several Rs
:
 retire what you can, rehost the simple apps, and refactor what gains the most from the cloud.

## Slide 19

The Well-Architected Framework
Six lenses for reviewing any cloud architecture 
(
we
'
ll come back to them all term
)
.
Operational Excellence
Run and improve systems to deliver value.
Security
Protect data, systems and identities.
Reliability
Recover from failure and meet demand.
Performance Efficiency
Use the right resources, sized well.
Cost Optimisation
Pay only for what delivers value.
Sustainability
Minimise the environmental impact.

## Slide 20

AWS Certifications
Four levels, 
and 
many path
s
.
Foundational
~6 months experience
AWS Certified
Cloud Practitioner
Associate
~1 year experience
Solutions Architect
Developer
SysOps Administrator
Professional
~2 years experience
Solutions Architect
DevOps Engineer
Specialty
Deep domain expertise
Advanced Networking
Data Analytics
Database
Machine Learning
Security
SAP on AWS

## Slide 21

Building Your AWS Career
Common certification paths and how to get there.
Solutions Architect
Cloud Practitioner
SA 
-
 
Associate
SA 
-
 Professional
DevOps Engineer
SysOps
 
-
 Associate
Developer 
-
 Associate
DevOps 
-
 Professional
Specialty Architect
Any Associate
A Specialty cert
Tips: 
F
ocus on one cloud provider
,
 start at the Associate level
.
 
G
et hands-on
:
 AWS suggests ~1 year before Associate and ~2 before Professional.

## Slide 22

Same Concepts, Different Names
You'll learn AWS
,
 but every major service
 we will see
 has an Azure and a GCP equivalent.
Service
AWS
Azure
GCP
Compute
Amazon EC2
Azure VMs
Compute Engine
Containers
ECS / EKS
AKS
GKE
Object storage
Amazon S3
Blob Storage
Cloud Storage
Databases
RDS / DynamoDB
Azure SQL / Cosmos DB
Cloud SQL / Spanner
Serverless
Lambda
Azure Functions
Cloud Functions
Networking
Amazon VPC
Virtual Network
VPC
Load balancing
ELB
Load Balancer
Cloud Load Balancing
Adapted from Shrivastava (2023), AWS for Solutions Architects — Figures 1.2–1.4.
The skills transfer: learn the concept on AWS, and you can map it to any provider.

## Slide 23

Quick Check
Four questions before we wrap!
Q1
A developer provisions a test server from the console in minutes, with no human approval needed. Which essential characteristic of cloud is at work?
Q2
Your team wants to deploy an app without managing servers, operating systems or runtimes. Which service model fits?
Q3
You run a database on an EC2 instance (IaaS). Who is responsible for patching the operating system? you or AWS?
Q4
A hospital keeps patient records on-premises but bursts month-end analytics to AWS. Which deployment model is this?
Answers are in the speaker notes of this slide.

## Slide 24

Key Takeaways
Cloud is on-demand, pay-as-you-go IT: defined by five essential characteristics.
IaaS, PaaS and SaaS trade control for convenience as you move up the stack.
Public, private and hybrid models balance control, cost and compliance.
Regions, Availability Zones and Edge Locations deliver performance and resilience.
Above all, cloud is a business strategy, and the concepts transfer across providers.
NEXT WEEK
Compute: Provisioning & Scaling with Amazon EC2
This Week’s Tutorial: Getting Started on AWS
