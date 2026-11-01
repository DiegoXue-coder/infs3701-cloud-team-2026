import boto3,json
c=boto3.client('ec2',region_name='us-east-1'); name='infs3701-team-runtime-20261101'
images=c.describe_images(Owners=['self'],Filters=[{'Name':'name','Values':[name]}])['Images']
if images:
 print('RUNTIME_IMAGE='+json.dumps([{'id':x['ImageId'],'state':x['State']} for x in images]))
else:
 output=c.get_console_output(InstanceId='i-030acdefe159caa87',Latest=True).get('Output','')
 if 'INFS3701_RUNTIME_READY' not in output:raise RuntimeError('Runtime build is not ready; do not create image')
 r=c.create_image(InstanceId='i-030acdefe159caa87',Name=name,Description='INFS3701 Python3.11 Flask boto3 Gunicorn runtime and clearly labelled infrastructure-only placeholder; no business data or instance role',NoReboot=False,TagSpecifications=[{'ResourceType':'image','Tags':[{'Key':'Project','Value':'infs3701-team'},{'Key':'Name','Value':name}]},{'ResourceType':'snapshot','Tags':[{'Key':'Project','Value':'infs3701-team'}]}])
 print('RUNTIME_IMAGE_CREATING='+r['ImageId'])
