# INFS3701_Tutorial_07_Networking_and_Content_Delivery.pdf

Course: INFS3701. Searchable text; original diagrams and layout remain authoritative.

## Page 1

I N F S 3 7 0 1     ·     T E R M  3 ,  2 0 2 6
Enterprise Architecture for Scalable 
Cloud Solutions
Week 07 · Tutorial
Networking & Content Delivery
TWO -PA RT PRA CTIC AL  S ES S IO N

## Page 2

W EE K  0 7 · TUTO R IA L
Today's Tutorial
How this two-part session works and what you'll walk out with.
1 Prep check: last week's IAM module
2 Meet the café: our working example for the tutorials from 
now on
3 This week's objectives: VPC & content delivery
4 Part 1: we build the café's network (~75 min)
5 Part 2: your group assignment begins (~45 min)

## Page 3

W EE K  0 7 · TUTO R IA L
How This Tutorial Works
Each week: learn it on a working example, then apply it to your own assignment.
Part 1 · Tutor-led
≈ 75 min
We build a proper network for the café, our working example for the rest of term. You'll apply it to your group's project.
Part 2 · Your assignment
≈ 45 min
Your group works on its own project with help on hand, keeping progress and recording who did what.
H OW Y OU R  TU T ORI AL M ARK  IS  S P LI T
Preparation (50%): complete the AWS Academy modules and labs set in each tutorial before the next session.
Participation (50%): work on your next assessment in the session, and keep evidence: AI-prompt screenshots, dated versions of your docs and code, and a short reflection.

## Page 4

W EE K  0 7  · T U T O R I A L
This Week's Objectives
Week 7: Networking & Content Delivery.
B Y  T H E  E N D,  Y O U  C A N
Explain a VPC: subnets, route tables and gateways
Place resources in public and private subnets
Use security groups to control traffic
Explain content delivery with a CDN, and DNS routing with Route 53
H O W  T HI S  W E E K ' S  M A R K  I S  S P L I T
Preparation  (50%)
The Week 5 module (IAM · Module 4, Lab 1) 
completed in AWS Academy before today.
Participation  (50%)
Your work in Parts 1 and 2 today, and your group's 
progress and contribution record.
F R O M  T H E  L E C T U R E
Today builds this week's lecture hands on: VPCs, public and private subnets, routing and security groups; networking the café.

## Page 5

PART 1
T U T O R- L E D
Building the café's network
A VPC with public and private subnets
≈ 75 MINUTES


## Page 6

W EE K  0 7 · TUTO R IA L
Meet the Café
The working example we'll scale for the rest of term.
From here on, our working example is the café: an online coffee-ordering app. 
Over Weeks 7 to 10 we make it scalable and highly available, one tier at a time.
The café app
An online coffee-ordering app to make scalable and available.
Networking · today
We give it a proper VPC with public and private subnets.
The goal
By Week 10: scalable and highly available.
Your group scales one member's own service, not the café. The café shows you how.

## Page 7

WEEK 07 · TUTORIAL
The Café: The Business and the Problem
Our working example for Weeks 7 to 10
THE BUS INES S THE PROBLEM TODAY
Order and pay ahead
A small Sydney café chain. Customers order and 
pay in the app, then collect. Card payments go 
through an external payment provider.
A sharp morning rush
Orders jump roughly tenfold between 7 and 9 
am, then go quiet; almost nothing overnight.
Orders must never go missing
A lost order is a lost sale; one recorded twice 
charges the customer twice. Either way: a 
refund and an unhappy customer.
One server does everything
Web, application and data all run on a single 
EC2 instance in a public subnet.
It fails at the worst time
If that server stops, nobody can order. If the 
rush overloads it, the app slows or crashes.
Exposed and unwatched
The data sits on an internet-facing server, and 
nobody is alerted when something breaks.
THE PLAN : ONE STEP  EAC H WEEK
7 Week 7 · Network
Private app servers reach the 
payment provider and updates 
via NA T; nothing reaches them.
8 Week 8 · Resilient 
data
A managed database with a 
standby in a second zone.
9 Week 9 · Front door
One load balancer across both 
zones, and alarms that warn 
before customers notice.
10 Week 10 · Scale for 
the rush
More servers in the morning, 
fewer at night.

## Page 8

WEEK 07 · TUTORIAL
The Café's Network: What We Build Today
One VPC across two Availability Zones.
Customers' phones (internet)
Region us-east-1
VPC  10.0.0.0/16
Internet Gateway
Availability Zone us-east-1a
PUBLIC  10.0.1.0/24
PRIVATE · APP  10.0.11.0 /24
PRIVATE · DATA  10.0.21.0/24
Availability Zone us-east-1b
PUBLIC  10.0.2.0/24
PRIVATE · APP  10.0.12.0/24
PRIVATE · DATA  10.0.22.0 /24
Web server (EC2)
App server (EC2)
Database · Week 8
Web server (EC2)
App server (EC2)
Database · Week 8
NAT gateway NAT gateway
ROUTI NG
Public route table
internet traffic → Internet Gateway
Private route tables, one per zone
outbound only → that zone's own NAT 
       gateway
SEC URITY  G ROU PS
web-sg
web traffic from anywhere
app-sg
8080 only from web-sg
db-sg
database port only from app-sg (Week 8)
Each group admits traffic only 
from the tier in front of it.

## Page 9

W EE K  0 7 · TUTO R IA L
Part 1: Build the Network
Follow along as we design the café's VPC.
1 Create a VPC with public and private subnets across two Availability Zones.
2 Add an internet gateway and route tables.
3 Put the web tier in public subnets, the app and data tier in private.
4 Set security groups and allow only the traffic each tier needs.
5 Test it: the web servers answer from the internet; the app servers can't be reached.
An AI assistant can explain VPC concepts and generate CLI commands, but you design the network.

## Page 10

WEEK 07 · TUTORIAL
Your Prompt Checklist
Check your prompt covers each of these.
EVERY PROMP T THIS  WEEK, ALSO COV ER
Your goal
What you want to end up with, in one sentence.
Your context
The café's order-and-pay app: web, app and data 
tiers, and who needs to reach each one.
Your limits
The AWS Academy Learner Lab (us-east-1): LabRole 
only, no new roles; small instances; limited credits.
Ask for the why
Ask it to explain each choice, so you can justify it in 
your own words.
Ask how to test it
How to check it works, and how to tear it down 
afterwards.
The layout
One VPC, with public and private subnets in two 
Availability Zones, and their address ranges.
What goes where
Web servers in public subnets; app and data tiers in 
private ones.
Routing
What each route table sends where , and what 
makes a subnet public.
Outbound access
A NAT gateway in each zone, so private servers 
reach the payment provider and updates.
Security groups
Each tier admits traffic only from the tier in front of 
it.
“I'm designing the network for a café's order-and-pay app, which has web, app and data tiers. The goal is a VPC where only the web tier faces the internet. Use 
10.0.0.0/16 with one public subnet and two private subnets (app and data) in each of two Availability Zones,and suggest sensible address ranges. Explain what each 
route table should send where, and what makes a subnet public. The private app servers must reach an external payment provider and download updates, so include a 
NAT gateway in each zone and explain why one per zone matters. Write security groups so each tier accepts traffic only from the tier in front of it. I'm in the AWS 
Academy Learner Lab (us-east-1) with limited credits and no new IAM roles, so keep instances small and tell me what costs money while it runs. Explain each choice 
so I can justify it. Then show me how to test that the web servers are reachable from the internet and the app servers are not, and how to delete everything 
afterwards.”

## Page 11

W EE K  0 7 · TUTO R IA L
Networking in Action
The lecture's networking ideas  and protecting your credits.
F RO M T HE L EC TU R E
P R O TE CT  Y O U R  CR E DI TS
You're now building a bigger, multi-resource stack.
Build, capture evidence, then tear it down.
Keep instances small while you learn.
Watch your credits, there’re more things running now.
From here on you're building a bigger stack, keep an eye on your credits.
Subnets across two Availability Zones:
public for web, private for app and data.
Route tables and gateways: an IGW for 
public, NAT for private outbound.
Security groups and NACLs: two firewall 
layers around each tier .
CloudFront: cache content close to users 
and take load off your origin.

## Page 12

PART 2
Y O U R  G R O U P  A S S I G N M E N T  ·  S U P E R V I S E D
Your group assignment begins
Build a scalable, highly available version of one member's service.
≈ 45 MINUTES


## Page 13

W EE K  0 7 · TUTO R IA L
Your Group Assignment Begins
Your network design and the first draft of your architecture diagram.
Group Assignment A Scalable, Highly Available Cloud Service
Group    ·    25% of the course    ·    Due Week 10
Confirm your route: scale a member's individual service or start from a new idea.
Today's step: design its network. A VPC with public and private subnets across two Availability Zones.
Sketch your first architecture diagram, it is graded, and it starts today.
The café is your working example; your submission is your group's own project. Read 
the group brief on Moodle.

## Page 14

W EE K  0 7 · TUTO R IA L
Keep Your Progress
Record as a group.
AS  Y OU  WO RK
Keep a versioned design document and update who did what.
Screenshot each milestone for your group's evidence.
BY  T HE E ND O F T OD AY
Your group's starting service chosen
A VPC designed across two Availability Zones
Work split agreed and contribution statement started
A first architecture diagram sketched, with screenshots
This is your participation mark and every screenshot saves you time when you write 
the final deliverables.

## Page 15

W EE K  0 7 · TUTO R IA L
Before Next Week
Self-study now and keep your project moving.
Complete the Week 7 preparation activities: AWS Academy Module 5 · Lab 2 (VPC). Your prep mark for next week.
Tidy up your network so you don't waste credits.
Keep your group project moving toward Week 10.
NE X T TU TOR IA L
Week 8 Databases
We give the café a resilient database and you add one to your project.

