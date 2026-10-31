# INFS3701_Week07_Networking_and_Content_Delivery.pdf

Course: INFS3701. Searchable text; original diagrams and layout remain authoritative.

## Page 1

I N F S 3 7 0 1     ·     T E R M  3 ,  2 0 2 6
Enterprise Architecture for Scalable 
Cloud Solutions
Week 07 · Lecture
Cloud Architecting: Networking & Content Distribution
T omas Lagos
Lecturer · School of Information Systems & Technology Management
tomas.lagos@unsw.edu.au

## Page 2

Today's Lecture
Where we're headed in this session.
1 The AWS global network
2 Amazon VPC and its building blocks
3 Subnets, gateways and routing
4 A reference VPC architecture
5 Securing the network
6 Connecting to on-premises
7 Content delivery, DNS and the edge

## Page 3

The AWS Global Network
A quick refresher.
39Geographic Regions 123Ava ilability Zones 750+Points of Presence 150+Direct Connect locations
Region
A separate geographic area, such as 
Sydney. You choose where your data 
and workloads live.
FROM WEEK 1
Availability Zone
One or more isolated data centres
inside a Region, each with its own 
power , cooling and network.
FROM WEEK 1
Local Zone
Puts compute and storage in a big 
city far from its Region: single-digit 
millisecond latency. 30+ worldwide.
NEW THIS WEEK
Wavelength Zone
Sits inside a telco's 5G network, 
so mobile traffic never leaves it. 
30+ worldwide.
NEW THIS WEEK
Regions and Zones buy you resilience; Local and Wavelength Zones buy you  further in latency. Points of 
Presence cache content.
Sources: AWS Global Infrastructure (Regions and AZs as at June 2026); AWS Direct Connect announcements, 2026. These counts ch ange. Check the AWS global infrastructure 
page.

## Page 4

Amazon VPC: Your Private Network
Your own isolated virtual network inside AWS. You decide what's exposed and what stays 
private.
AWS Region
Amazon VPC
Subnet · AZ-A
 Subnet · AZ-B
Logically isolated
Your own network, separate from everyone 
else's
Spans a Region
Subnets live in its Availability Zones
You choose the IP range
A private CIDR block: the design matters more 
than the math
You control the traffic
Routing, gateways and firewalls are all yours

## Page 5

The Building Blocks of a VPC
Six parts you assemble every time. The next few slides take them one at a time.
CIDR block
The private IP range for the VPC : 10.0.0.0/16 gives you 
about 65,000 addresses.
Subnets
Slices of that range, each sitting in one Availability 
Zone (typically web, app and database tiers ).
Route tables
The rules that decide where a subnet's traffic goes. 
Every subnet has one.
Gateways
Internet Gateway for traffic in and out; NAT Gateway 
for outbound -only from private subnets.
Security groups & NACLs
Two firewall layers: one at the instance, one at the 
subnet boundary.
VPC Flow Logs
Records which traffic was accepted and rejected .
Mainly for troubleshooting and security investigations.
Design the address range first. Everything else can be changed later, but resizing a VPC in place cannot.

## Page 6

Subnets: Public vs Private
Place each resource by how exposed it should be.
Public Subnet
Has a route to the internet through an 
Internet Gateway.
IN TE RNE T Inbound & outbound (via IGW)
FO R Load balancers, web / bastion tier
Private Subnet
No direct route in from the internet (stays 
hidden).
IN TE RNE T Outbound only (via NAT)
FO R Application servers, databases

## Page 7

Gateways & Routing
Three pieces decide where traffic is allowed to go.
Internet Gateway
Lets resources in public 
subnets send and receive 
internet traffic.
NAT Gateway
Lets private subnets reach out (e.g. for updates) 
without being reachable 
from outside.
Route Tables
Direct traffic between 
subnets, gateways and 
connected networks.
A subnet is “public” simply because its route table sends internet-bound traffic to the Internet 
Gateway.

## Page 8

A Reference VPC Architecture
A typical three-tier application, spread across two Availability Zones.
Internet
Amazon VPC AZ-A AZ-B
PUBLI C S UBNE T
NAT Gateway
PRIVATE SUBNET · APPL ICATIO N
EC2
 EC2
PRIVATE SUBNET · DA TABAS E
RDS primary
 RDS standby
Public subnet reaches 
the internet via the 
IGW
Private subnets take 
no inbound traffic 
from the internet
NA T lets private tiers 
fetch updates 
outbound only
Load Balancer
NAT Gateway

## Page 9

Securing the Network
Two layers of firewall: one at the instance, one at the subnet.
Security Groups
Attached to instances. 
Stateful: return traffic is automatic. 
Allow rules only.
Scope: a single instance / interface
Network ACLs
Attached to subnets. 
Stateless: evaluated in order . 
Allow and deny rules.
Scope: the whole subnet
Layer them for defence in depth.  Identity and access controls were covered in Weeks 4-5.

## Page 10

Case: Locking Down the Traffic Paths
The reference architecture again.
P AT H V ER DI C T ENF OR C ED  BY
Internet → Load balancer :443 ALLOW ALB security group permits HTTPS from 
anywhere
Internet → App instances DENY Private subnet: no inbound route, no public IP
Load balancer → App :8080 ALLOW App SG accepts traffic only from the ALB's SG
App → Database :5432 ALLOW DB SG accepts traffic only from the app's SG
Database → Internet DENY No IGW route; outbound patches via NAT only if 
allowed
Notice the pattern:  security groups reference each other; “from the ALB's group”, not from a list of IPs. Identity-style firewalling.

## Page 11

Connecting Networks
Linking VPCs to each other, to your data centre, and to AWS services.
VPC Peering
Connect two VPCs 
directly
Transit Gateway
A hub for many VPCs 
and accounts
Site-to-Site VPN
Encrypted tunnel to 
on-premises
Direct Connect
A dedicated private 
line to AWS
PrivateLink
Reach AWS services 
privately
Peering and Transit Gateway join VPCs; VPN and Direct Connect reach on-premises; PrivateLink keeps AWS-service traffic off the internet.

## Page 12

Hybrid Connectivity: Reaching On-Premises
Most enterprises keep something in their own data centre.
AWS Client VPN
One person, from anywhere. A VPN client on a laptop reaches your VPC; split tunnelling sends only AWS -bound traffic down it.
Site-to-Site VPN
A whole office or data centre, over the internet. Two encrypted IPsec tunnels, and quick to stand up.
Site-to-Site VPN + Transit Gateway
Many VPCs and many sites. The Transit Gateway is the hub, so you stop building a mesh of point -to-point links.
AWS Direct Connect
A dedicated private line. Consistent latency, higher throughput and cheaper data transfer , but weeks to provision, and not 
encrypted by default.
AWS Cloud WAN
A global network with segments, built and monitored from one dashboard : for enterprises with many branches across many 
Regions.
These are not five competing options. 
They answer different questions: who connects, how many sites, private line or internet 
And they are routinely combined: Direct Connect for speed, with a VPN over it for encryption.

## Page 13

Real Case: A Bank Goes Hybrid
TBC Bank kept its data centre, and made it feel like part of AWS.
WHAT THEY BU ILT WHAT CH ANGED
Security first
Network security services went onto AWS before the 
workloads did.
Direct Connect
A dedicated line replaced internet paths between the 
data centre and AWS.
PrivateLink
Third-party services reached privately, without 
exposing traffic to the internet.
20 ms less per API call
Jitter gone. One user action makes many calls, so the 
saving compounds.
99.92% availability
Achieved across the hybrid environment.
19,991 deployments in 2025
Up from 4,662 in 2022 , and 88.4% of them automated.
The catch worth remembering: Direct Connect is not encrypted by default. Pair it with a VPN, or turn on 
MACsec, whenever the data is sensitive.
Source: AWS customer case study . TBC Bank (Georgia).

## Page 14

Content Delivery & DNS
Get content to users fast, and send them to the right place.
Amazon CloudFront
Content Delivery Network
Caches content at edge locations close to 
users. 
Faster delivery, less load on your origin, 
and built-in DDoS protection.
Amazon Route 53
Managed DNS
Resolves your domain and routes users 
with latency, geolocation and failover 
policies, backed by health checks.
Together: Route 53 sends a user to the nearest CloudFront edge, which serves cached content or 
fetches it from your origin.
Real world:  CloudFront runs 750+ Points of Presence in 100+ cities.
Across one Prime Day served over 1 trillion HTTP requests, peaking above 500 million per minute. 
(AWS)

## Page 15

Why Edge Locations Matter
Distance is latency: caching close to the user transforms the experience.
Typical public round -trip times, illustrative
750+
CloudFront Points of 
Presence, in 100+ cities 
across 50+ countries
1 trillion HTTP requests served 
across a single Prime Day
500M+ requests per minute at 
that day's peak
Sources: AWS CloudFront features page; AWS Prime Day report
Static content comes from the edge; dynamic requests still ride AWS's private backbone to your 
Region.

## Page 16

Route 53: Choosing Where Traffic Goes
One domain name, seven ways to decide which server answers.
Simple
One record, one destination . The default.
Failover
Active-passive: switch to the standby when a health 
check fails.
Latency
Sends each user to whichever Region answers fastest 
for them.
Geolocation
Routes on where the user is : for licensing or local 
language.
Geoproximity
Routes on distance to your resources, with a bias you 
can tune.
Weighted
Splits traffic by proportion : 80/20 for a canary release 
or A/B test.
Multivalue answer
Returns up to eight healthy records at random : simple 
load spreading.
Policies can be nested: geolocation to pick a Region, then weighted inside it. 
Route 53 is the only AWS service with a 100% availability SLA.

## Page 17

Anatomy of a Page Load
Trace one request through everything we've just built.
1
DNS lookup
Route 53 resolves shop.example.com and points 
the browser at the nearest entry point.
 2
Edge first
CloudFront serves the cached images, CSS and 
JavaScript from a nearby edge location.
3
Into the VPC
The dynamic request enters through the Internet 
Gateway to the load balancer in the public 
subnet.
4
App tier
The load balancer forwards the request to a 
healthy EC2 instance in a private subnet.
5
Data tier
The app queries RDS in the private database 
subnet and assembles the page.
 6
The way back
The response retraces the path. The user never 
touched a private subnet directly.
What never happens:  inbound internet traffic reaching the app or database tiers, their subnets simply have no route for it.

## Page 18

Which Edge Service Does What?
Four services and four different jobs: they are often used together.
Route 53
DNS
Decides which endpoint a name 
resolves to. The traffic then 
goes there directly.
CloudFront
Co ntent  d eliv er y
Caches your content at 750+ 
edge locations and serves it 
from the nearest one.
Global Accelerator
Netw or k path
Static IPs that pull traffic onto 
the AWS backbone early. No 
caching. Fails over in about 30 
seconds.
Wavelength
5G edg e c om put e
Runs your compute inside a 
telco's 5G network, so mobile 
traffic never crosses the 
internet.
CloudFront caches the content; Global Accelerator only speeds up the path to it. Route 53 picks the 
destination; Wavelength moves the compute to the user.
USE  FOR
Choosing a destination
USE  FOR
Cacheable web content, video
USE  FOR
TCP/UDP apps, gaming, VoIP
USE  FOR
Ultra-low-latency mobile apps

## Page 19

Networking Best Practices
Architecting a sound and secure network.
Keep data private
Put databases and app servers in private subnets.
Span multiple AZs
Place subnets in two or more zones for resilience.
Least-privilege rules
Open only the ports and sources you truly need.
Serve globally
Front public content with 
CloudFront.
Stay off the internet
Reach AWS services 
through PrivateLink 
endpoints.
Plan your ranges
Choose address blocks 
that won't overlap when 
you connect.

## Page 20

Networking Across the Big Three
Private networks, firewalls, DNS, CDNs and hybrid links.
Service AWS Azure GCP
Private network Amazon VPC Virtual Network (VNet) VPC
Network firewalls Security groups & NACLs Network security groups VPC firewall rules
DNS / CDN Route 53 / CloudFront Azure DNS / Front Door Cloud DNS / Cloud CDN
Private link to on-
premises AWS Direct Connect Azure ExpressRoute Cloud Interconnect
W H E R E  E A C H  HA S  A N  E D G E
AWS: the largest number of regions and edge locations.
Azure: ExpressRoute for strong hybrid and on-premises connectivity.
GCP: a VPC is global. One network can span regions without peering.

## Page 21

Key Takeaways
N E X T  WE E K
Databases: Selecting the Right Database Service
This week’s Tutorial: Networking (Module 5, Lab 2)
Regions and Availability Zones buy you resilience; Local and Wavelength Zones buy you latency.
A VPC is your own isolated network in a Region, divided into subnets across Availability Zones.
Public subnets reach the internet via an IGW; private subnets stay hidden and use NAT for 
outbound.
Security groups (instance, stateful) and network ACLs (subnet, stateless) layer your defences.
VPN, Transit Gateway, Direct Connect and Cloud WAN join AWS to on-premises; usually 
combined, not chosen between.
Route 53 picks the destination, CloudFront caches the content, Global Accelerator speeds up 
the path.
