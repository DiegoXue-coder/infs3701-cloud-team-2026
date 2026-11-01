import boto3,json,jmespath
checks=[('routes','ec2','describe_route_tables',{'Filters':[{'Name':'vpc-id','Values':['vpc-0836d003a70f93405']}]},'RouteTables[].{id:RouteTableId,routes:Routes[].{cidr:DestinationCidrBlock,gateway:GatewayId,state:State},subnets:Associations[].SubnetId}'),('certificates','acm','list_certificates',{},'CertificateSummaryList[].{domain:DomainName,status:Status,arn:CertificateArn}'),('dns_zones','route53','list_hosted_zones',{},'HostedZones[].{name:Name,id:Id}'),('tables','dynamodb','list_tables',{},'TableNames'),('rds','rds','describe_db_instances',{},'DBInstances[].{name:DBInstanceIdentifier,engine:Engine,multiAZ:MultiAZ}'),('profile','iam','get_instance_profile',{'InstanceProfileName':'LabInstanceProfile'},'InstanceProfile.Roles[].RoleName'),('ami','ssm','get_parameter',{'Name':'/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64'},'Parameter.Value'),('eic_endpoints','ec2','describe_instance_connect_endpoints',{},'InstanceConnectEndpoints[].{id:InstanceConnectEndpointId,state:State,vpc:VpcId}')]
for label,service,operation,args,query in checks:
 try:
  response=getattr(boto3.client(service,region_name='us-east-1'),operation)(**args)
  print(label+'='+json.dumps(jmespath.search(query,response),separators=(',',':')))
 except Exception as e:
  print(label+'=ERROR:'+str(getattr(e,'response',{}).get('Error',{}).get('Code',type(e).__name__)))
