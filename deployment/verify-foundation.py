"""Read-only readback of the deployed foundation; not a business acceptance test."""
import boto3
import datetime
import json

s = boto3.Session(region_name="us-east-1")
ec2, elb, cw = s.client("ec2"), s.client("elbv2"), s.client("cloudwatch")
assert s.client("sts").get_caller_identity()["Account"] == "214018170594"


def out(key, value):
    print(key + "=" + json.dumps(value, default=str, separators=(",", ":")), flush=True)


out("CHECKED_AT", datetime.datetime.now(datetime.timezone.utc).isoformat())
for group in ec2.describe_security_groups(GroupIds=["sg-00ebc11a2282074f6", "sg-0a3ae03837c952009", "sg-02f5195143dca6ea5"])["SecurityGroups"]:
    out("SECURITY_GROUP", {k:group[k] for k in ["GroupId", "IpPermissions", "IpPermissionsEgress"]})
for endpoint in ec2.describe_vpc_endpoints(VpcEndpointIds=["vpce-0edea5c7a05bc729d", "vpce-028353eb0e050df0a"])["VpcEndpoints"]:
    out("GATEWAY", {k:endpoint[k] for k in ["VpcEndpointId", "State", "RouteTableIds", "PolicyDocument"]})
for table in ec2.describe_route_tables(RouteTableIds=["rtb-03e1a36c6b2440ed7", "rtb-02f19dad4efe80bd3"])["RouteTables"]:
    out("PRIVATE_ROUTES", {k:table[k] for k in ["RouteTableId", "Routes"]})
for reservation in ec2.describe_instances(InstanceIds=["i-00572a14ca8b71156", "i-0081259c52a32e051", "i-030acdefe159caa87"])["Reservations"]:
    for host in reservation["Instances"]:
        out("INSTANCE", {k:host.get(k) for k in ["InstanceId", "State", "PrivateIpAddress", "PublicIpAddress", "IamInstanceProfile", "MetadataOptions"]})
lb=elb.describe_load_balancers(Names=["infs3701-team-alb"])["LoadBalancers"][0]
out("ALB", {k:lb[k] for k in ["LoadBalancerArn", "DNSName", "State", "Scheme", "AvailabilityZones"]})
out("LISTENERS", [{k:l[k] for k in ["Port","Protocol"]} for l in elb.describe_listeners(LoadBalancerArn=lb["LoadBalancerArn"])["Listeners"]])
alarm="infs3701-team-healthy-targets-below-two"
out("ALARM_HISTORY", [{k:h.get(k) for k in ["Timestamp", "HistorySummary", "HistoryData"]} for h in cw.describe_alarm_history(AlarmName=alarm,HistoryItemType="StateUpdate",MaxRecords=8)["AlarmHistoryItems"]])
out("DASHBOARD", {"name":"infs3701-team-dashboard", "widget_count":len(json.loads(cw.get_dashboard(DashboardName="infs3701-team-dashboard")["DashboardBody"])["widgets"])})
