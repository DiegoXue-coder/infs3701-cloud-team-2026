# INFS3701_Week03_Storage.pdf

Extracted text for search; diagrams/layout must be checked in the original.

## Page 1

I N F S 3 7 0 1     ·     T E R M  3 ,  2 0 2 6
Enterprise Architecture for Scalable 
Cloud Solutions
Week 03 · Lecture
Cloud Architecting: Storage
T omas Lagos
Lecturer · School of Information Systems & Technology Management
tomas.lagos@unsw.edu.au

## Page 2

Today's Lecture
Where we're headed in this session.
1 The three types of storage: block, object and file
2 Amazon S3: object storage at scale
3 S3 storage classes and the cost of access
4 Lifecycle policies: automating cost control
5 Block storage with Amazon EBS
6 Shared files, durability, and choosing the right tool

## Page 3

Three Types of Storage
Match the storage to how your data is accessed.
Block
A raw disk you format 
and attach to a single 
server .
A W S  S E R V I C E
Amazon EBS
U S E  F O R
OS volumes, databases
Object
Files plus metadata in a 
flat namespace, accessed 
over HTTP .
A W S  S E R V I C E
Amazon S3
U S E  F O R
Backups, media, data lakes, websites
File
A shared file system 
many servers can mount 
at once.
A W S  S E R V I C E
Amazon EFS / FSx
U S E  F O R
Shared content, lift-and-shift

## Page 4

Block Storage: Amazon EBS
A virtual disk attached to one EC2 instance, in one Availability Zone.
gp3
General Purpose SSD
Balanced price-
performance; boot 
volumes, most apps
io2
Provisioned IOPS SSD
Highest IOPS, low 
latency; critical 
databases
st1
Throughput Optimised HDD
High throughput, 
sequential; big data, 
logs
sc1
Cold HDD
Lowest cost; 
infrequently accessed 
data
Snapshots: incremental, point-in-time backups stored in Amazon S3. Restore anytime or copy 
across Regions.

## Page 5

Amazon S3: Object Storage at Scale
The default home for data in AWS: Virtually unlimited, durable and accessed over the web.
W HA T  IT  I S
Buckets & objects
Any file, any type, up to 5 TB each
Eleven nines of durability
Designed never to lose an object
Accessed over HTTPS
Via API or SDK, from anywhere
Pay for what you use
Storage, requests and data transfer
W HA T  IT ' S F O R
Backup & archive
 Data lakes & analytics
Static website hosting
E.g., Assignment 1
Content & media

## Page 6

Real Case: The Capital One Breach (2019)
100 million records exposed from S3 through a misconfiguration, not a sophisticated hack.
HOW IT HAPP ENED WHAT WOU LD HAVE STOP PED  IT
Misconfigured firewall
An SSRF attack reached the server’s metadata service.
Leaked credentials
It handed over an IAM role with far too much access.
S3 raided
The role listed ~700 buckets and copied 100M+ 
records.
Unnoticed ~4 months
Logs existed but no one was watching them.
Least privilege
The firewall's role never needed any S3 access.
Monitor & alert
Flag unusual API calls; don’t wait for an outsider to tell 
you.
IAM Access Analyzer
Would have flagged the over -broad permissions.
Defence in depth
Data was encrypted , but the same role could decrypt 
it.
The bill: an US$80M regulatory fine plus a US$190M settlement. 
AWS secures the cloud; securing what 's in your buckets and who can reach them is on you.
Capital One cyber incident, 2019 , sources: US DOJ; KrebsOnSecurity.

## Page 7

S3 Storage Classes
Trade instant access for lower cost. Pick a class by how often you read the data.
Hot · frequent
 Cold · archive
S3 Standard
A CC E SS
Frequent access
RE TRIE V AL
Instant
STORAGE PRICE
$0.023 /GB·mo
S3 Standard-IA
A CC E SS
Infrequent access
RE TRIE V AL
Instant *
STORAGE PRICE
$0.0125 /GB·mo
Glacier Flexible
A CC E SS
Archive
RE TRIE V AL
Minutes-hours
STORAGE PRICE
$0.0036 /GB·mo
Glacier Deep Archive
A CC E SS
Long-term archive
RE TRIE V AL
Hours
STORAGE PRICE
$0.00099 /GB·mo
Plus Intelligent-Tiering (moves objects automatically) and One Zone -IA (cheaper, single Availability Zone).
Storage prices, US East (N. Virginia), first tier · Source: AWS S3 pricing, 2026

## Page 8

What the Class Ladder Is Worth
The price gap between hot and cold storage is enormous, choosing well is real money.
Source: AWS S3 pricing, US East (N. Virginia), 2026
23×
cheaper to hold data in 
Deep Archive than in 
Standard
~US$1
per terabyte per month at 
the bottom of the ladder
180 days
minimum storage 
duration in Deep Archive, 
plus retrieval fees
Cheap to store is not cheap to retrieve: 
Archive classes charge for access, so the class must match the access pattern.

## Page 9

Lifecycle Management
Let rules move data to cheaper classes (and delete it) automatically as it ages.
Day 0
Object created
in S3 Standard
After 30 days
Move to
Standard-IA
After 90 days
Archive to
Glacier
After 365 days
Expire and
delete
Illustrative, US East prices
One rule set, ~71% saved:  a terabyte kept for a year costs ~$283 in Standard but ~$82 with this 
lifecycle, no manual cleanup, ever.

## Page 10

Amazon S3 Best Practices
Keep S3 secure, fast and cost-effective, most slip-ups are configuration, not code.
SEC URITY P ERF ORMANC E & COS T
Lock down access
Block public access (on by default); least-
privilege policies.
Encrypt everything
At rest with SSE-S3 or KMS; in transit over 
HTTPS.
Watch & protect
Access Analyzer , Config, Macie and access logs; 
replicate across Regions.
Right class + lifecycle
Match the class to access; lifecycle rules 
archive and expire to cut cost.
Serve it fast
CloudFront caches at the edge; Transfer 
Acceleration speeds global uploads.
Name keys with care
Consistent, descriptive prefixes; avoid 
sequential keys at high request rates.
Most S3 incidents trace back to one thing, e.g., a bucket or an IAM role left more open than it 
needed to be.

## Page 11

Case: Storage for a Photo-Sharing App
Millions of uploads a day and almost all views happen in the first month.
T H E  L I F E  O F  A N  U P L O A D E D  P HO T O
Upload:  Original lands in S3 Standard; viewed 
heavily this week
Day 30:  Lifecycle moves it to Standard-IA
Day 180:  Glacier Flexible, kept forever, fetched 
almost never
Except thumbnails:  every feed scroll hits them, so 
they stay in S3 Standard for good.
T H E  RE S T  O F  TH E  D E S I G N
App database volume
Block storage: EBS gp3 attached to the EC2 
tier
Shared ML scratch space
File storage: EFS mounted by the 
processing fleet
The website itself
S3 static hosting + CloudFront (Weeks 1 & 4, 
and Assignment 1)
One app, three storage types chosen by 
access pattern.

## Page 12

Durability vs Availability
Two different promises.
Durability
“Will my data survive?”
Amazon S3 is designed for eleven nines 
(99.999999999%). You essentially never 
lose a stored object.
Availability
“Can I reach it right now?”
Measured as uptime (S3 Standard targets 
about 99.99%). Some classes trade 
availability for lower cost.
High durability ≠ high availability: S3 One Zone-IA is durable, but lives in a single Availability 
Zone.

## Page 13

When an Availability Zone Is Destroyed
AWS Middle East. The first time a cloud Region lost customer data to an airstrike.
W HA T H A PP E N E D W HA T I T M E AN S  F O R Y O U R DE S IG N
Drone strikes, March 2026
Two UAE facilities hit directly; a nearby strike damaged 
Bahrain. Structural damage, lost power, and water 
damage from fire suppression.
Bahrain lost multiple AZs
AWS: the damage “exceeded what our regional and 
multi-AZ services are designed to withstand”.
Some data is gone for good
On 15 September AWS said it cannot restore data held 
exclusively in one UAE zone (mec1 -az2), or exclusively 
in the Bahrain Region.
One Zone-IA keeps one copy, in one AZ
That ~20% discount is a risk premium. This is precisely 
the event it excludes.
Standard spans three or more AZs
In the UAE the other two zones survived, so data 
written across AZs had somewhere to come back from.
Only multi-Region survives a Region
Bahrain shows multi -AZ has a ceiling. Cross -Region 
replication is what clears it.
Eleven nines models independent disk failures, not a building being destroyed. 
The only data lost was data held “exclusively” in one place. That single word is the whole lesson.
Sources: AWS Health Dashboard updates, 15 September 2026; reporting by The Wall Street Journal, CNBC and DataCenterDynamics.

## Page 14

Shared File Storage: EFS & FSx
When many servers need to read and write the same files.
Amazon EFS
Elastic File System
A managed NFS file system for Linux that 
grows and shrinks automatically and can 
be mounted across Availability Zones.
U S E  F O R
Shared app content, web farms, lift-and-shift
Amazon FSx
Managed File Systems
Fully managed third-party file systems: FSx 
for Windows File Server (SMB) and FSx for 
Lustre for high-performance computing.
U S E  F O R
Windows workloads, HPC and analytics

## Page 15

Choosing the Right Storage
A few questions point you straight to the right service.
Attached to a single server?
 Block: Amazon EBS
Shared by many servers at once, highly 
updated?
 File: Amazon EFS / FSx
Web-scale, any file, from anywhere?
 Object: Amazon S3
Rarely accessed or archival?
 S3 Glacier classes
Want cost control on aging data?
 S3 Lifecycle policies/Intelligent 
tiering

## Page 16

Storage Across the Big Three
Object, block and archival storage exist on every major cloud.
Service AWS Azure GCP
Object Amazon S3 Blob Storage Cloud Storage
Block / file EBS / EFS Managed Disks / Files Persistent Disk / Filestore
Archival S3 Glacier Archive Storage Cloud Storage 
Nearline/Coldline
W H E R E  E A C H  HA S  A N  E D G E
AWS: S3 is the most mature, with the broadest tooling and integrations.
Azure: storage tiers integrate closely with its analytics stack.
GCP: Cloud Storage uses one global namespace and one API across tiers.

## Page 17

Key Takeaways
Storage comes in three shapes: block (EBS), object (S3) and file (EFS/FSx). Chosen between 
them by access pattern.
Amazon S3 is durable, web-scale object storage.
S3 storage classes trade instant access for lower cost; lifecycle rules automate the move.
EBS gives an EC2 instance a fast attached disk; snapshots back it up to S3.
Durability (will it survive?) and availability (can I reach it now?) are different promises.
N E X T  WE E K
Cloud Economics & Security Foundations
This week’s Tutorial: Adding a Storage Layer (Module 7, Lab 4)

