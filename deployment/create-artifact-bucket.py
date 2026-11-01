import boto3,json
s3=boto3.client('s3',region_name='us-east-1'); account=boto3.client('sts',region_name='us-east-1').get_caller_identity()['Account']; name='infs3701-team-artifacts-'+account
names=[x['Name'] for x in s3.list_buckets()['Buckets']]
if name not in names: s3.create_bucket(Bucket=name)
s3.head_bucket(Bucket=name,ExpectedBucketOwner=account)
s3.put_public_access_block(Bucket=name,PublicAccessBlockConfiguration={'BlockPublicAcls':True,'IgnorePublicAcls':True,'BlockPublicPolicy':True,'RestrictPublicBuckets':True})
s3.put_bucket_encryption(Bucket=name,ServerSideEncryptionConfiguration={'Rules':[{'ApplyServerSideEncryptionByDefault':{'SSEAlgorithm':'AES256'}}]})
s3.put_bucket_tagging(Bucket=name,Tagging={'TagSet':[{'Key':'Project','Value':'infs3701-team'},{'Key':'Purpose','Value':'private-deployment-artifacts'}]})
s3.put_bucket_policy(Bucket=name,Policy=json.dumps({'Version':'2012-10-17','Statement':[{'Sid':'DenyInsecureTransport','Effect':'Deny','Principal':'*','Action':'s3:*','Resource':['arn:aws:s3:::'+name,'arn:aws:s3:::'+name+'/*'],'Condition':{'Bool':{'aws:SecureTransport':'false'}}}]}))
print('ARTIFACT_BUCKET='+json.dumps({'name':name,'public_access':'all_blocked','encryption':'AES256','http':'denied','old_bucket':'unchanged'}))
