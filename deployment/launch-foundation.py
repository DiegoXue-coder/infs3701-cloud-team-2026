"""Prepared next stage. Default is an offline plan; --apply needs explicit access approval.

Run only with the project operator's already-authorized AWS identity inside AWS.
This creates a labelled infrastructure placeholder, not the Reading Tracker business app.
"""
import argparse
import json
import boto3

REGION = "us-east-1"
ACCOUNT = "214018170594"
VPC = "vpc-0836d003a70f93405"
IMAGE = "ami-03616f6b53c85f036"
PUBLIC = ["subnet-0567427f846712996", "subnet-0358770cf9d551064"]
PRIVATE = ["subnet-026f2c6afbe3692e8", "subnet-00fc1e9a647c3530e"]
PRIVATE_ROUTES = ["rtb-03e1a36c6b2440ed7", "rtb-02f19dad4efe80bd3"]
PROJECT = "infs3701-team"
ROLE = f"arn:aws:iam::{ACCOUNT}:role/LabRole"
TABLE = f"arn:aws:dynamodb:{REGION}:{ACCOUNT}:table/infs3701-team-books"
ARTIFACTS = f"arn:aws:s3:::infs3701-team-artifacts-{ACCOUNT}/releases/*"


def tags(name):
    return [{"Key": "Project", "Value": PROJECT}, {"Key": "Name", "Value": name}]


def emit(stage, value):
    print(stage + "=" + json.dumps(value, default=str), flush=True)


def endpoint_policy(actions, resource):
    return {"Version": "2012-10-17", "Statement": [{
        "Effect": "Allow", "Principal": "*", "Action": actions, "Resource": [resource],
        "Condition": {"ArnEquals": {"aws:PrincipalArn": ROLE},
                      "Bool": {"aws:SecureTransport": "true"}}}]}


def group_permission(port, group):
    return {"IpProtocol": "tcp", "FromPort": port, "ToPort": port,
            "UserIdGroupPairs": [{"GroupId": group}]}


def apply():
    session = boto3.Session(region_name=REGION)
    if session.client("sts").get_caller_identity()["Account"] != ACCOUNT:
        raise RuntimeError("Wrong AWS account; no infrastructure changes allowed")
    ec2, elb = session.client("ec2"), session.client("elbv2")
    if ec2.describe_vpcs(VpcIds=[VPC])["Vpcs"][0]["CidrBlock"] != "10.37.0.0/16":
        raise RuntimeError("Unexpected VPC CIDR")
    image = ec2.describe_images(ImageIds=[IMAGE])["Images"][0]
    if image["State"] != "available" or image["OwnerId"] != ACCOUNT:
        raise RuntimeError("Runtime image unavailable or owned by another account")
    if not all(x["Ebs"].get("Encrypted", False) for x in image["BlockDeviceMappings"] if "Ebs" in x):
        raise RuntimeError("Unencrypted runtime image volume")
    groups, new = {}, {}
    for label in ["alb", "app", "eic"]:
        name = f"{PROJECT}-{label}-sg"
        rows = ec2.describe_security_groups(Filters=[
            {"Name": "vpc-id", "Values": [VPC]}, {"Name": "group-name", "Values": [name]}])["SecurityGroups"]
        if rows:
            if len(rows) != 1 or dict((x["Key"], x["Value"]) for x in rows[0].get("Tags", [])).get("Project") != PROJECT:
                raise RuntimeError("Security group ownership mismatch")
            groups[label], new[label] = rows[0]["GroupId"], False
        else:
            groups[label] = ec2.create_security_group(
                GroupName=name, Description=f"{PROJECT} restricted {label} access", VpcId=VPC,
                TagSpecifications=[{"ResourceType": "security-group", "Tags": tags(name)}])["GroupId"]
            new[label] = True
    emit("SECURITY_GROUPS", groups)
    ingress = {
        "alb": [{"IpProtocol": "tcp", "FromPort": 80, "ToPort": 80, "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}],
        "app": [group_permission(8000, groups["alb"]), group_permission(22, groups["eic"])],
        "eic": []}
    egress = {
        "alb": [group_permission(8000, groups["app"])],
        "app": [{"IpProtocol": "tcp", "FromPort": 443, "ToPort": 443,
                 "PrefixListIds": [{"PrefixListId": "pl-63a5400a"}, {"PrefixListId": "pl-02cd2c6b"}]}],
        "eic": [group_permission(22, groups["app"])]}
    for label, ident in groups.items():
        if not new[label]:
            raise RuntimeError("Existing foundation security group: inspect rules and resume manually; no blind overwrite")
        defaults = ec2.describe_security_groups(GroupIds=[ident])["SecurityGroups"][0]["IpPermissionsEgress"]
        if defaults:
            ec2.revoke_security_group_egress(GroupId=ident, IpPermissions=defaults)
        if ingress[label]:
            ec2.authorize_security_group_ingress(GroupId=ident, IpPermissions=ingress[label])
        ec2.authorize_security_group_egress(GroupId=ident, IpPermissions=egress[label])
    for service, actions, resource in [
            ("s3", ["s3:GetObject"], ARTIFACTS),
            ("dynamodb", ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:Scan", "dynamodb:DescribeTable"], TABLE)]:
        service_name = f"com.amazonaws.{REGION}.{service}"
        existing = ec2.describe_vpc_endpoints(Filters=[
            {"Name": "vpc-id", "Values": [VPC]}, {"Name": "service-name", "Values": [service_name]}])["VpcEndpoints"]
        if existing:
            raise RuntimeError("Unexpected existing gateway endpoint; inspect before changing permissions")
        out = ec2.create_vpc_endpoint(VpcEndpointType="Gateway", VpcId=VPC, ServiceName=service_name,
            RouteTableIds=PRIVATE_ROUTES, PolicyDocument=json.dumps(endpoint_policy(actions, resource)),
            TagSpecifications=[{"ResourceType": "vpc-endpoint", "Tags": tags(f"{PROJECT}-{service}-gateway")}])
        emit("GATEWAY_" + service.upper(), out["VpcEndpoint"]["VpcEndpointId"])
    eic = ec2.create_instance_connect_endpoint(SubnetId=PRIVATE[0], SecurityGroupIds=[groups["eic"]],
        PreserveClientIp=False, TagSpecifications=[
            {"ResourceType": "instance-connect-endpoint", "Tags": tags(f"{PROJECT}-eic")}])
    emit("MAINTENANCE_ENDPOINT", eic["InstanceConnectEndpoint"]["InstanceConnectEndpointId"])
    instance_ids = []
    for suffix, subnet in zip(["a", "b"], PRIVATE):
        name = f"{PROJECT}-app-{suffix}"
        found = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values": [name]},
            {"Name": "instance-state-name", "Values": ["pending", "running", "stopped", "stopping"]}])["Reservations"]
        if found:
            raise RuntimeError("Existing application instance; inspect instead of creating duplicates")
        user_data = f"""#!/bin/bash
set -euxo pipefail
mkdir -p /etc/infs3701
cat > /etc/infs3701/app.env <<'ENV'
APP_INSTANCE=az-{suffix}
APP_PORT=8000
READING_TABLE=infs3701-team-books
AWS_DEFAULT_REGION=us-east-1
AWS_REGION=us-east-1
ENV
systemctl enable --now infs3701-app.service
"""
        out = ec2.run_instances(ImageId=IMAGE, InstanceType="t3.micro", MinCount=1, MaxCount=1,
            NetworkInterfaces=[{"DeviceIndex": 0, "SubnetId": subnet, "Groups": [groups["app"]],
                                "AssociatePublicIpAddress": False}],
            IamInstanceProfile={"Name": "LabInstanceProfile"},
            BlockDeviceMappings=[{"DeviceName": image["RootDeviceName"],
                "Ebs": {"VolumeSize": 8, "VolumeType": "gp3", "Encrypted": True, "DeleteOnTermination": True}}],
            MetadataOptions={"HttpTokens": "required", "HttpEndpoint": "enabled"},
            CreditSpecification={"CpuCredits": "standard"}, UserData=user_data,
            ClientToken=f"infs3701-foundation-{suffix}-03616f6b53c85f036",
            TagSpecifications=[{"ResourceType": "instance", "Tags": tags(name)},
                               {"ResourceType": "volume", "Tags": tags(name + "-root")}])
        instance_ids.append(out["Instances"][0]["InstanceId"])
        emit("PRIVATE_INSTANCE", {"name": name, "id": instance_ids[-1]})
    emit("WAITING_FOR_INSTANCES", instance_ids)
    ec2.get_waiter("instance_running").wait(InstanceIds=instance_ids, WaiterConfig={"Delay": 10, "MaxAttempts": 30})
    tg = elb.create_target_group(Name=f"{PROJECT}-tg", Protocol="HTTP", Port=8000, VpcId=VPC,
        TargetType="instance", HealthCheckProtocol="HTTP", HealthCheckPath="/health",
        HealthCheckIntervalSeconds=15, HealthCheckTimeoutSeconds=5,
        HealthyThresholdCount=2, UnhealthyThresholdCount=2, Matcher={"HttpCode": "200"},
        Tags=tags(f"{PROJECT}-tg"))["TargetGroups"][0]
    lb = elb.create_load_balancer(Name=f"{PROJECT}-alb", Subnets=PUBLIC, SecurityGroups=[groups["alb"]],
        Scheme="internet-facing", Type="application", IpAddressType="ipv4", Tags=tags(f"{PROJECT}-alb"))["LoadBalancers"][0]
    elb.create_listener(LoadBalancerArn=lb["LoadBalancerArn"], Protocol="HTTP", Port=80,
        DefaultActions=[{"Type": "forward", "TargetGroupArn": tg["TargetGroupArn"]}])
    elb.register_targets(TargetGroupArn=tg["TargetGroupArn"], Targets=[{"Id": x, "Port": 8000} for x in instance_ids])
    emit("FOUNDATION_CREATED", {"instances": instance_ids, "target_group": tg["TargetGroupArn"],
        "load_balancer": lb["LoadBalancerArn"], "test_url": "http://" + lb["DNSName"],
        "stage": "infrastructure-only; business app/TLS/monitoring not complete"})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Only after explicit action-time access approval")
    args = parser.parse_args()
    if not args.apply:
        emit("OFFLINE_PLAN", {"region": REGION, "vpc": VPC, "image": IMAGE, "private_subnets": PRIVATE,
            "instance_profile": "LabInstanceProfile", "public_listener": 80,
            "approval_required": True, "details": "project/next-deployment.json"})
        return
    apply()


if __name__ == "__main__":
    main()
