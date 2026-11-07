"""Pinned course release builder and guarded, one-host-at-a-time operator.

build is local-only. AWS phases run in authenticated CloudShell, after the
operator has confirmed the public demonstration scope described in the plan.
"""
import argparse
import base64
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMIT = '06c2292cdf0aca80f050709b8172fac3595b54cc'
BUCKET = 'infs3701-team-artifacts-214018170594'
IDS = {'a': 'i-00572a14ca8b71156', 'b': 'i-0081259c52a32e051'}
TG = 'arn:aws:elasticloadbalancing:us-east-1:214018170594:targetgroup/infs3701-team-tg/9597ed4011467b27'


def build(out):
    out.mkdir(parents=True, exist_ok=True)
    content = {name: subprocess.check_output(['git', 'show', COMMIT + ':' + source]) for name, source in [('app.py', 'app/reading_tracker.py'), ('requirements.txt', 'deployment/runtime-requirements.lock')]}
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode='w', format=tarfile.USTAR_FORMAT) as archive:
        for name, raw in content.items():
            member = tarfile.TarInfo(name)
            member.size, member.mode, member.mtime = len(raw), 0o644, 0
            archive.addfile(member, io.BytesIO(raw))
    raw = gzip.compress(buf.getvalue(), mtime=0)
    plan = {'commit': COMMIT, 'bucket': BUCKET, 'key': 'releases/reading-tracker/' + COMMIT + '/app.tar.gz', 'archive_sha256': hashlib.sha256(raw).hexdigest(), 'files': {n: hashlib.sha256(x).hexdigest() for n, x in content.items()}, 'public_scope': 'Existing HTTP ALB becomes unauthenticated fictional-demo list/add. No real personal data. TLS unresolved.', 'hosts': IDS, 'rollback': 'Per-host foundation backup; rollback mode retains database and release files.'}
    (out / 'app.tar.gz').write_bytes(raw)
    (out / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
    (out / 'business-host.py').write_bytes(Path(__file__).with_name('business-host.py').read_bytes())
    print(json.dumps(plan, indent=2))


def user_data(plan, label, mode, host_code):
    configured = dict(plan, label='az-' + label, mode=mode)
    script = '#!/bin/bash\nset -euo pipefail\nexec > >(tee -a /var/log/infs3701-release.log /dev/console) 2>&1\n'
    script += "echo INFS3701_RELEASE_BEGIN\n/opt/infs3701/venv/bin/python - <<'HOSTPY'\n"
    script += host_code + '\nmain(' + repr(configured) + ')\nHOSTPY\n'
    # Embedded code must not run its normal CLI branch before configured main.
    script = script.replace("if __name__ == '__main__':", "if False:")
    message = MIMEMultipart()
    message.attach(MIMEText(script, _subtype='x-shellscript-per-boot', _charset='us-ascii'))
    data = message.as_bytes()
    assert len(data) < 16384, 'EC2 user-data limit'
    return data


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('phase', choices=['build', 'upload', 'prepare', 'start', 'inspect', 'rollback-start'])
    p.add_argument('--directory', type=Path, default=Path('release-staging'))
    p.add_argument('--instance', choices=IDS)
    args = p.parse_args()
    if args.phase == 'build':
        build(args.directory)
        return
    import boto3
    s = boto3.Session(region_name='us-east-1')
    assert s.client('sts').get_caller_identity()['Account'] == '214018170594'
    plan = json.loads((args.directory / 'plan.json').read_text())
    assert plan['commit'] == COMMIT and plan['bucket'] == BUCKET
    raw = (args.directory / 'app.tar.gz').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == plan['archive_sha256']
    ec2, elb = s.client('ec2'), s.client('elbv2')
    if args.phase == 'upload':
        # Immutable content-addressed key; no public ACL, credentials or course files.
        obj = s.client('s3')
        obj.put_object(Bucket=BUCKET, Key=plan['key'], Body=raw, ServerSideEncryption='AES256', ContentType='application/gzip', Metadata={'commit': COMMIT, 'sha256': plan['archive_sha256']})
        check = obj.get_object(Bucket=BUCKET, Key=plan['key'])
        assert hashlib.sha256(check['Body'].read()).hexdigest() == plan['archive_sha256']
        print('PRIVATE_ARCHIVE_VERIFIED=' + plan['archive_sha256'])
        return
    assert args.instance, '--instance required'
    ident = IDS[args.instance]
    host = ec2.describe_instances(InstanceIds=[ident])['Reservations'][0]['Instances'][0]
    assert host['VpcId'] == 'vpc-0836d003a70f93405' and not host.get('PublicIpAddress')
    assert host['IamInstanceProfile']['Arn'].endswith('/LabInstanceProfile')
    assert dict((t['Key'], t['Value']) for t in host['Tags'])['Project'] == 'infs3701-team'
    state = host['State']['Name']
    print('HOST_STATE=' + json.dumps({'id': ident, 'state': state}), flush=True)
    if args.phase == 'prepare':
        other = IDS['b' if args.instance == 'a' else 'a']
        targets = elb.describe_target_health(TargetGroupArn=TG)['TargetHealthDescriptions']
        assert any(x['Target']['Id'] == other and x['TargetHealth']['State'] == 'healthy' for x in targets)
        assert state == 'running'
        backup = Path.home() / (ident + '-pre-business-userdata.txt')
        if not backup.exists():
            backup.write_bytes(base64.b64decode(ec2.describe_instance_attribute(InstanceId=ident, Attribute='userData')['UserData']['Value']))
        ec2.stop_instances(InstanceIds=[ident])
        print('STOP_REQUESTED=' + ident, flush=True)
    elif args.phase in ('start', 'rollback-start'):
        assert state == 'stopped', 'Poll until stopped; do not repeat stop/start'
        code = (args.directory / 'business-host.py').read_text()
        data = user_data(plan, args.instance, 'rollback' if args.phase == 'rollback-start' else 'release', code)
        ec2.modify_instance_attribute(InstanceId=ident, UserData={'Value': data})
        ec2.start_instances(InstanceIds=[ident])
        print('START_REQUESTED=' + json.dumps({'id': ident, 'commit': COMMIT, 'mode': args.phase, 'userdata_bytes': len(data)}), flush=True)
    else:
        print('TARGETS=' + json.dumps(elb.describe_target_health(TargetGroupArn=TG)['TargetHealthDescriptions']))
        output = ec2.get_console_output(InstanceId=ident, Latest=True).get('Output', '')
        # Only bounded project diagnostics; never dump credentials or entire console.
        print('RELEASE_DIAGNOSTICS=' + json.dumps([x for x in output.splitlines() if 'INFS3701_RELEASE' in x or 'INFS3701_ROLLBACK' in x]))


if __name__ == '__main__':
    main()
