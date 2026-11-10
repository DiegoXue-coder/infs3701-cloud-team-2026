"""Render the evidence-dated architecture; offline, no AWS changes.

Requires reportlab and the selected official AWS icon assets in assets/aws/.
Run from the repository root. Coordinates use an A3 landscape PDF canvas.
"""
from pathlib import Path
import json
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pdf/reading-tracker-architecture.pdf'
INK = '#182C43'
BLUE = '#254E77'
GREEN = '#177869'
PURPLE = '#7A49A5'
GRAY = '#526476'
manifest = json.loads((ROOT/'assets/aws/manifest.json').read_text(encoding='utf-8'))


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=landscape(A3), pageCompression=1)
    c.setTitle('INFS3701 Reading Tracker - evidence-dated deployed architecture')
    c.setAuthor('DiegoXue-coder; AI-assisted; technical review pending')
    W, H = landscape(A3)

    def text(x, y, content, size=10, color=INK, bold=False):
        assert all(ord(ch)<128 for ch in content), content
        c.setFillColor(HexColor(color))
        c.setFont('Helvetica-Bold' if bold else 'Helvetica', size)
        c.drawString(x, y, content)

    def box(x, y, w, h, stroke='#C9D5DF', fill='#FFFFFF', dash=None, radius=5):
        c.setStrokeColor(HexColor(stroke)); c.setFillColor(HexColor(fill))
        c.setLineWidth(1)
        c.setDash(dash or [])
        c.roundRect(x,y,w,h,radius,stroke=1,fill=1)
        c.setDash([])

    def icon(key,x,y,size=32):
        c.drawImage(ImageReader(str(ROOT/'assets/aws'/manifest['files'][key]['png'])),x,y,size,size,mask='auto')

    def arrow(points,color=BLUE,dash=None,width=1.6,head=True):
        c.setStrokeColor(HexColor(color));c.setFillColor(HexColor(color));c.setLineWidth(width);c.setDash(dash or [])
        p=c.beginPath();p.moveTo(*points[0])
        for xy in points[1:]:p.lineTo(*xy)
        c.drawPath(p);c.setDash([])
        if head:
            x,y=points[-1];x0,y0=points[-2];a=math.atan2(y-y0,x-x0)
            p=c.beginPath();p.moveTo(x,y)
            for angle in [a+2.65,a-2.65]:p.lineTo(x+7*math.cos(angle),y+7*math.sin(angle))
            p.close();c.drawPath(p,stroke=0,fill=1)

    text(28,802,'Reading Tracker | deployed architecture',27,bold=True)
    text(29,778,'INFS3701  /  us-east-1  /  release 06c2292  /  configuration evidence: 10 Nov 2026  /  review draft: 11 Nov Sydney',10.8,GRAY)
    box(138,190,1020,560,'#879CAF','#FAFCFE')
    text(152,735,'AWS Region: US East (N. Virginia) - us-east-1',11,bold=True)
    box(158,206,680,515,'#6D87A1','#FFFFFF')
    text(173,706,'VPC 10.37.0.0/16',12,bold=True)

    for x,az,pub,priv,label,ip,iid in [
        (177,'us-east-1a','10.37.0.0/24','10.37.10.0/24','az-a','10.37.10.88','i-00572a14ca8b71156'),
        (511,'us-east-1b','10.37.1.0/24','10.37.11.0/24','az-b','10.37.11.110','i-0081259c52a32e051')]:
        box(x,326,306,334,'#B5A1C9','#FEFCFF',dash=[4,3])
        text(x+13,643,'Availability Zone '+az,11,PURPLE,True)
        box(x+13,554,280,74,'#91B7A6','#F2FAF5')
        text(x+24,613,'Public subnet '+pub,10,bold=True)
        box(x+13,346,280,155,'#8CA9C4','#F2F7FB')
        text(x+24,486,'Private subnet '+priv,10,bold=True)
        box(x+29,400,248,70,'#D5DEE7')
        icon('ec2',x+40,429,30)
        text(x+80,451,'EC2 '+label+' | t3.micro',11,bold=True)
        text(x+80,435,'Flask + Gunicorn :8000',10)
        text(x+40,416,iid+'  |  '+ip,8.5,GRAY)
        box(x+29,359,248,32,'#D5DEE7')
        icon('ebs',x+40,364,22)
        text(x+72,372,'EBS root: 8 GiB gp3, encrypted',9.7)
        arrow([(x+153,400),(x+153,391)],width=1,head=False)

    # One logical ALB spans both public subnet/AZ boxes.
    box(300,563,397,38,'#765597','#FFFFFF')
    icon('alb',307,568,27)
    text(343,586,'Application Load Balancer',11,bold=True)
    text(343,572,'HTTP :80  |  both public subnets',9,GRAY)
    icon('users',38,683,34)
    text(27,667,'Browser users',11,bold=True)
    text(27,652,'Fictional records',9,GRAY)
    icon('igw',210,667,29)
    text(245,687,'Internet gateway',10,bold=True)
    arrow([(78,699),(128,699),(128,682),(210,682)])
    text(87,709,'1  HTTP :80',10,BLUE,True)
    arrow([(239,676),(497,676),(497,601)])
    arrow([(497,563),(497,531),(440,531),(440,470)])
    arrow([(497,531),(776,531),(776,470)])
    text(295,517,'2  HTTP :8000',10,BLUE,True)
    text(544,517,'Target health: GET /health',9,GRAY)

    # Both application hosts use the same endpoint routes and durable store.
    box(254,222,474,77,'#70AA9D','#F1FAF7')
    text(267,283,'3  Private route tables - gateway endpoints',10,GREEN,True)
    text(269,264,'DynamoDB endpoint',10,bold=True)
    text(269,238,'S3 endpoint',10,bold=True)
    text(427,264,'Application reads / writes',9,GRAY)
    text(427,238,'Pinned release download at deployment',9,GRAY)
    arrow([(454,437),(477,437),(477,314),(430,314),(430,299)],GREEN)
    arrow([(790,437),(804,437),(804,314),(570,314),(570,299)],GREEN)
    text(452,305,'HTTPS :443 (SDK)',8.8,GREEN)
    arrow([(728,270),(846,270),(846,488),(866,488)],GREEN)
    arrow([(728,239),(826,239),(826,335),(866,335)],GREEN)

    box(866,440,270,120,'#8599D0')
    icon('ddb',879,509,33)
    text(920,530,'Amazon DynamoDB',12,bold=True)
    text(881,494,'infs3701-team-books',10.5,bold=True)
    text(881,478,'Shared durable records; managed regional service',9)
    text(881,462,'On-demand | record_id partition key | encrypted',9)
    box(866,285,270,113,'#8FB79B')
    icon('s3',879,349,33)
    text(920,370,'Amazon S3',12,bold=True)
    text(881,335,'Private release artifacts; not the business database',9)
    text(881,319,'Pinned archive/hash | SSE-S3 | public access blocked',9)
    text(881,303,'Only project releases/ accessible on endpoint path',9)

    box(866,610,270,116,'#C28EAD')
    icon('cw',879,679,32)
    text(920,699,'Amazon CloudWatch',12,bold=True)
    text(881,666,'Dashboard: ALB / EC2 / DynamoDB native metrics',9)
    text(881,650,'Alarm: minimum healthy targets < 2, 2 x 60 s',9)
    text(881,634,'Real ALARM / OK history retained; no notifications',9)
    arrow([(697,590),(850,590),(850,686),(866,686)],PURPLE,[4,3])
    text(710,601,'Native metrics*',9,PURPLE)

    arrow([(30,171),(65,171)],BLUE);text(75,168,'HTTP request; response returns on same path',9)
    arrow([(384,171),(419,171)],GREEN);text(429,168,'HTTPS AWS-service path',9)
    arrow([(649,171),(684,171)],PURPLE,[4,3]);text(694,168,'*Logical telemetry; no host egress to CloudWatch required',9)

    for x,title,lines in [
        (28,'SECURITY BOUNDARY',[
            'ALB ingress :80 from internet; app :8000 from ALB SG only.',
            'No public IP / SSH / NAT; app egress :443 to S3/DDB only.',
            'IMDSv2 + LabRole; broader LabRole limitation remains.',
            'HTTP links are unencrypted. HTTPS certificate unresolved.']),
        (405,'AVAILABILITY AND SCALING',[
            'Two fixed, stateless app hosts share DynamoDB data.',
            'One-instance stop / restart tested; whole AZ not tested.',
            '/health checks the app process, not database access.',
            'Automatic scaling deferred by owner; no ASG deployed.']),
        (782,'EVIDENCE AND SCOPE',[
            'Based on AWS exports dated 10 Nov; not a live status view.',
            'Prepared by A; independent B/C review still required.',
            'Unused maintenance endpoint/builder off request path.',
            'No login or CSRF protection; fictional demo data only.'])]:
        box(x,47,355,102,'#D7DFE7','#F7F9FC')
        text(x+12,131,title,10,bold=True)
        for i,line in enumerate(lines):text(x+12,114-i*16,line,9)
    text(29,25,'Source: evidence/T05/2026-11-10-A-network-security.log; evidence/T09/2026-11-10-A-current-restoration.log; dated service preflight.',8,GRAY)
    text(29,12,'Official AWS Architecture Icons (31 Jul 2026 package): aws.amazon.com/architecture/icons/  |  Editable source: scripts/build_architecture_pdf.py  |  1 / 1',7.5,GRAY)
    c.showPage();c.save()
    print(json.dumps({'pdf':str(OUT),'pages':1,'configuration_evidence_date':'2026-11-10','aws_changes':0}))


if __name__ == '__main__':build()
