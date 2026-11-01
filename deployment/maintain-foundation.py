"""Restricted Lab alternative to SSH: stop/update user-data/start ONE staged host.

No IAM changes; no SSH tunnel. Run in authenticated CloudShell. Only the two
project placeholder hosts are allowed. Do not use on a business release until
its deployment/rollback bundle has been reviewed. Each phase returns promptly.
"""
import argparse
import base64
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import boto3

IDS = {"a": "i-00572a14ca8b71156", "b": "i-0081259c52a32e051"}
TG = "arn:aws:elasticloadbalancing:us-east-1:214018170594:targetgroup/infs3701-team-tg/9597ed4011467b27"
PROBE_SHA = "d62182089dfb9eaede166463362157edb9f3f5f15f6ac0dc46d1097fca642db7"


def user_data(label):
    script = r'''#!/bin/bash
set -euo pipefail
exec > >(tee -a /var/log/infs3701-boot-check.log /dev/console) 2>&1
echo INFS3701_BOOT_CHECK_BEGIN
mkdir -p /etc/infs3701
cat > /etc/infs3701/app.env <<'ENV'
APP_INSTANCE=az-LABEL
APP_PORT=8000
READING_TABLE=infs3701-team-books
AWS_DEFAULT_REGION=us-east-1
AWS_REGION=us-east-1
ENV
systemctl enable --now infs3701-app.service
/opt/infs3701/venv/bin/python - <<'PY'
import boto3, hashlib, json, time, urllib.request
from botocore.config import Config
s=boto3.Session(region_name='us-east-1')
result={'instance':'az-LABEL','credential_source':s.get_credentials().method}
assert result['credential_source']=='iam-role'
cfg=Config(connect_timeout=5,read_timeout=10,retries={'max_attempts':2})
d=s.client('dynamodb',config=cfg)
result['table_status']=d.describe_table(TableName='infs3701-team-books')['Table']['TableStatus']
result['visible_records']=d.scan(TableName='infs3701-team-books',Select='COUNT')['Count']
obj=s.client('s3',config=cfg).get_object(Bucket='infs3701-team-artifacts-214018170594',Key='releases/infrastructure/2026-11-01/probe.txt')
result['artifact_sha256']=hashlib.sha256(obj['Body'].read()).hexdigest()
assert result['artifact_sha256']=='PROBESHA'
for attempt in range(20):
 try:
  with urllib.request.urlopen('http://127.0.0.1:8000/health',timeout=3) as r:
   result['local_health']=json.load(r)
  break
 except Exception:
  if attempt==19: raise
  time.sleep(1)
assert result['local_health']['instance']=='az-LABEL'
print('INFS3701_BOOT_CHECK_OK='+json.dumps(result),flush=True)
PY
echo INFS3701_BOOT_CHECK_END
'''.replace("LABEL", label).replace("PROBESHA", PROBE_SHA)
    message = MIMEMultipart()
    message.attach(MIMEText(script, _subtype="x-shellscript-per-boot", _charset="us-ascii"))
    result = message.as_string()
    assert len(result.encode()) < 16384
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--instance", choices=IDS, required=True)
    p.add_argument("--phase", choices=["prepare", "start", "inspect", "restore-userdata"], required=True)
    args = p.parse_args()
    s = boto3.Session(region_name="us-east-1")
    assert s.client("sts").get_caller_identity()["Account"] == "214018170594"
    ec2, elb = s.client("ec2"), s.client("elbv2")
    ident = IDS[args.instance]
    host = ec2.describe_instances(InstanceIds=[ident])["Reservations"][0]["Instances"][0]
    assert host["VpcId"] == "vpc-0836d003a70f93405" and not host.get("PublicIpAddress")
    assert dict((t["Key"], t["Value"]) for t in host["Tags"])["Project"] == "infs3701-team"
    state = host["State"]["Name"]
    backup = Path.home() / (ident + "-foundation-userdata-backup.txt")
    print("HOST_STATE=" + json.dumps({"id": ident, "state": state}), flush=True)
    if args.phase == "prepare":
        other = IDS["b" if args.instance == "a" else "a"]
        health = elb.describe_target_health(TargetGroupArn=TG)["TargetHealthDescriptions"]
        assert any(x["Target"]["Id"] == other and x["TargetHealth"]["State"] == "healthy" for x in health), "Other target must be healthy"
        assert state == "running"
        if not backup.exists():
            old = ec2.describe_instance_attribute(InstanceId=ident, Attribute="userData")["UserData"]["Value"]
            backup.write_bytes(base64.b64decode(old))
        ec2.stop_instances(InstanceIds=[ident])
        print("STOP_REQUESTED=" + ident, flush=True)
    elif args.phase in ("start", "restore-userdata"):
        assert state == "stopped", "Wait until stopped; no repeated stop/start loops"
        # Restores only the EC2 user-data attribute. It does not remove cached
        # per-boot scripts or roll back application files. Not a release rollback.
        content = backup.read_bytes() if args.phase == "restore-userdata" else user_data(args.instance).encode()
        ec2.modify_instance_attribute(InstanceId=ident, UserData={"Value": content})
        ec2.start_instances(InstanceIds=[ident])
        print("START_REQUESTED=" + json.dumps({"id": ident, "phase": args.phase}), flush=True)
    else:
        print("TARGET_HEALTH=" + json.dumps(elb.describe_target_health(TargetGroupArn=TG)["TargetHealthDescriptions"]), flush=True)
        output = ec2.get_console_output(InstanceId=ident, Latest=True).get("Output", "")
        lines = [x for x in output.splitlines() if "INFS3701_BOOT_CHECK" in x]
        print("BOOT_DIAGNOSTICS=" + json.dumps(lines), flush=True)
        vols = ec2.describe_volumes(VolumeIds=[x["Ebs"]["VolumeId"] for x in host["BlockDeviceMappings"]])["Volumes"]
        print("ROOT_VOLUMES=" + json.dumps([{k:v[k] for k in ["VolumeId","Encrypted","Size","VolumeType"]} for v in vols]), flush=True)
        alarm = s.client("cloudwatch").describe_alarms(AlarmNames=["infs3701-team-healthy-targets-below-two"])["MetricAlarms"]
        print("ALARM=" + json.dumps([{k:a[k] for k in ["AlarmName","StateValue","StateUpdatedTimestamp","AlarmActions"]} for a in alarm], default=str), flush=True)


if __name__ == "__main__":
    main()
