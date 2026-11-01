import boto3,json
from botocore.exceptions import ClientError
c=boto3.client('ec2',region_name='us-east-1')
checks=[('private_instance_with_profile','run_instances',{'ImageId':'ami-03616f6b53c85f036','InstanceType':'t3.micro','MinCount':1,'MaxCount':1,'NetworkInterfaces':[{'DeviceIndex':0,'SubnetId':'subnet-026f2c6afbe3692e8','Groups':['sg-013228415d94c19e2'],'AssociatePublicIpAddress':False}],'IamInstanceProfile':{'Name':'LabInstanceProfile'},'MetadataOptions':{'HttpTokens':'required'}}),('dynamodb_gateway','create_vpc_endpoint',{'VpcId':'vpc-0836d003a70f93405','VpcEndpointType':'Gateway','ServiceName':'com.amazonaws.us-east-1.dynamodb','RouteTableIds':['rtb-03e1a36c6b2440ed7','rtb-02f19dad4efe80bd3']}),('maintenance_endpoint','create_instance_connect_endpoint',{'SubnetId':'subnet-026f2c6afbe3692e8','SecurityGroupIds':['sg-013228415d94c19e2'],'PreserveClientIp':False})]
for label,operation,args in checks:
 try:
  getattr(c,operation)(DryRun=True,**args)
  print(label+'=unexpected_dryrun_return')
 except ClientError as e:
  print('DRYRUN_'+label+'='+e.response['Error']['Code'])
