import urllib.request,json,time,collections,datetime
url='http://infs3701-team-alb-788523332.us-east-1.elb.amazonaws.com/health'
counts=collections.Counter(); failures=0; request_count=12
for number in range(request_count):
 started=time.monotonic()
 try:
  request=urllib.request.Request(url,headers={'Connection':'close'})
  with urllib.request.urlopen(request,timeout=8) as response:
   body=json.load(response); label=response.headers.get('X-App-Instance','missing'); counts[label]+=1
   print('REQUEST='+json.dumps({'n':number+1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':response.status,'instance':label,'stage':body.get('stage'),'ms':round((time.monotonic()-started)*1000)}),flush=True)
 except Exception as exc:
  failures+=1; print('REQUEST_ERROR='+json.dumps({'n':number+1,'error':str(exc)[:180]}),flush=True)
 time.sleep(0.5)
print('ROUTING_SUMMARY='+json.dumps({'requests':request_count,'failures':failures,'instances':dict(counts),'business_app_tested':False}))
