import boto3,json
region='us-east-1'; lb='app/infs3701-team-alb/cdc408a1dfd1268c'; tg='targetgroup/infs3701-team-tg/9597ed4011467b27'; instances=['i-00572a14ca8b71156','i-0081259c52a32e051']; widgets=[]
widgets.append({'type':'text','x':0,'y':0,'width':24,'height':2,'properties':{'markdown':'# INFS3701 staging infrastructure\nTwo-AZ runtime foundation only. Reading Tracker integration and HTTPS are pending. No notification recipients configured. Re-test with the real application before final acceptance.'}})
def graph(title,x,y,metrics,period=60):
 widgets.append({'type':'metric','x':x,'y':y,'width':12,'height':6,'properties':{'title':title,'region':region,'view':'timeSeries','period':period,'metrics':metrics}})
graph('Healthy targets: expected 2; loss means reduced redundancy',0,2,[['AWS/ApplicationELB','HealthyHostCount','LoadBalancer',lb,'TargetGroup',tg,{'stat':'Minimum'}],['AWS/ApplicationELB','UnHealthyHostCount','LoadBalancer',lb,'TargetGroup',tg,{'stat':'Maximum'}]])
graph('Requests and target errors',12,2,[['AWS/ApplicationELB','RequestCount','LoadBalancer',lb,{'stat':'Sum'}],['AWS/ApplicationELB','HTTPCode_Target_5XX_Count','LoadBalancer',lb,{'stat':'Sum'}]])
graph('Target latency (p95 seconds)',0,8,[['AWS/ApplicationELB','TargetResponseTime','LoadBalancer',lb,{'stat':'p95'}]])
graph('Instance CPU: basic five-minute metrics',12,8,[['AWS/EC2','CPUUtilization','InstanceId',ident,{'stat':'Average'}] for ident in instances],300)
graph('Database read/write capacity consumed',0,14,[['AWS/DynamoDB','ConsumedReadCapacityUnits','TableName','infs3701-team-books',{'stat':'Sum'}],['AWS/DynamoDB','ConsumedWriteCapacityUnits','TableName','infs3701-team-books',{'stat':'Sum'}]])
c=boto3.client('cloudwatch',region_name=region)
r=c.put_dashboard(DashboardName='infs3701-team-dashboard',DashboardBody=json.dumps({'widgets':widgets,'start':'-PT1H'}))
print('DASHBOARD_VALIDATION='+json.dumps(r.get('DashboardValidationMessages',[])))
c.put_metric_alarm(AlarmName='infs3701-team-healthy-targets-below-two',AlarmDescription='Staging availability: fewer than 2 healthy targets for 2 consecutive one-minute periods means loss of intended two-instance redundancy; not proof of business-data health.',Namespace='AWS/ApplicationELB',MetricName='HealthyHostCount',Dimensions=[{'Name':'LoadBalancer','Value':lb},{'Name':'TargetGroup','Value':tg}],Statistic='Minimum',Period=60,EvaluationPeriods=2,DatapointsToAlarm=2,Threshold=2,ComparisonOperator='LessThanThreshold',TreatMissingData='notBreaching',ActionsEnabled=True,Tags=[{'Key':'Project','Value':'infs3701-team'}])
a=c.describe_alarms(AlarmNames=['infs3701-team-healthy-targets-below-two'])['MetricAlarms'][0]
print('MONITORING_CREATED='+json.dumps({'dashboard':'infs3701-team-dashboard','alarm':a['AlarmName'],'state':a['StateValue'],'statistic':a['Statistic'],'threshold':a['Threshold'],'period':a['Period'],'evaluation_periods':a['EvaluationPeriods'],'notification_actions':a.get('AlarmActions',[])}))
