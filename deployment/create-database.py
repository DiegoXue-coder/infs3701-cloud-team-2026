import boto3,json
c=boto3.client('dynamodb',region_name='us-east-1')
name='infs3701-team-books'
try:
 r=c.describe_table(TableName=name)['Table']
 print('EXISTING_TABLE='+json.dumps({'name':r['TableName'],'status':r['TableStatus'],'keys':r['KeySchema']}))
except c.exceptions.ResourceNotFoundException:
 r=c.create_table(TableName=name,AttributeDefinitions=[{'AttributeName':'record_id','AttributeType':'S'}],KeySchema=[{'AttributeName':'record_id','KeyType':'HASH'}],BillingMode='PAY_PER_REQUEST',OnDemandThroughput={'MaxReadRequestUnits':10,'MaxWriteRequestUnits':10},Tags=[{'Key':'Project','Value':'infs3701-team'},{'Key':'Course','Value':'INFS3701'}])
 print('CREATING_TABLE='+r['TableDescription']['TableName'])
