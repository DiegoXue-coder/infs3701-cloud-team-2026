"""Close unused project SSH paths after boot-based maintenance was verified.

No IAM change or endpoint deletion; no old environment changes.
"""
import boto3
import json

s=boto3.Session(region_name="us-east-1")
assert s.client("sts").get_caller_identity()["Account"]=="214018170594"
e=s.client("ec2")
for group,field,operation in [
        ("sg-0a3ae03837c952009","IpPermissions",e.revoke_security_group_ingress),
        ("sg-02f5195143dca6ea5","IpPermissionsEgress",e.revoke_security_group_egress)]:
    g=e.describe_security_groups(GroupIds=[group])["SecurityGroups"][0]
    assert g["VpcId"]=="vpc-0836d003a70f93405"
    assert dict((t["Key"],t["Value"]) for t in g["Tags"])["Project"]=="infs3701-team"
    rules=[r for r in g[field] if r.get("IpProtocol")=="tcp" and r.get("FromPort")==22 and r.get("ToPort")==22]
    if rules:operation(GroupId=group,IpPermissions=rules)
    final=e.describe_security_groups(GroupIds=[group])["SecurityGroups"][0]
    print("TIGHTENED_GROUP="+json.dumps({"id":group,"ingress":final["IpPermissions"],"egress":final["IpPermissionsEgress"]}),flush=True)
