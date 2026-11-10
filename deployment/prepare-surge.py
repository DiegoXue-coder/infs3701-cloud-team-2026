"""Build an OFFLINE proposal only. No boto3 calls and no AWS changes.

Keep the two original hosts outside this group. A future approved operator
must recheck permissions, AMI, account quota and costs before applying it.
"""
import argparse
import base64
import importlib.util
import json
from pathlib import Path


def build(out):
    spec = importlib.util.spec_from_file_location('release', Path(__file__).with_name('release-business.py'))
    release = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(release)
    release.build(out)
    plan = json.loads((out / 'plan.json').read_text(encoding='utf-8'))
    host = Path(__file__).with_name('business-host.py').read_text(encoding='utf-8')
    original = "assert label in ('az-a', 'az-b') and mode in ('release', 'rollback')"
    assert host.count(original) == 1, 'Re-review label validation after source changes'
    host = host.replace(original, "assert __import__('re').fullmatch(r'asg-i-[0-9a-f]{17}', label) and mode == 'release'")
    host = host.replace("if __name__ == '__main__':", 'if False:')
    compile(host, 'surge-host.py', 'exec')
    # IMDSv2-local identity; no public metadata service or static credentials.
    identity = '''
request = urllib.request.Request('http://169.254.169.254/latest/api/token',
    headers={'X-aws-ec2-metadata-token-ttl-seconds':'60'}, method='PUT')
with urllib.request.urlopen(request, timeout=3) as response:
    token = response.read().decode()
request = urllib.request.Request('http://169.254.169.254/latest/meta-data/instance-id',
    headers={'X-aws-ec2-metadata-token':token})
with urllib.request.urlopen(request, timeout=3) as response:
    instance_id = response.read().decode()
'''
    configured = dict(plan, mode='release')
    python = host + '\n' + identity + '\nplan = ' + repr(configured) + "\nplan['label'] = 'asg-' + instance_id\n"
    # The builder AMI has the placeholder/unit but no app.env and no enabled
    # service. Existing-host releases get these from foundation provisioning.
    python += "if not ENV.exists():\n    ENV.write_text('APP_INSTANCE=' + plan['label'] + '\\nAPP_PORT=8000\\n')\n"
    python += "subprocess.run(['systemctl', 'enable', 'infs3701-app'], check=True)\nmain(plan)\n"
    compile(python, 'surge-bootstrap.py', 'exec')
    script = '#!/bin/bash\nset -euo pipefail\nexec > >(tee -a /var/log/infs3701-surge.log /dev/console) 2>&1\n'
    script += "/opt/infs3701/venv/bin/python - <<'SURGEPY'\n" + python + '\nSURGEPY\n'
    assert len(script.encode()) < 16384, 'User data exceeds EC2 limit'
    template = {
        'ImageId': 'ami-03616f6b53c85f036', 'InstanceType': 't3.micro',
        'IamInstanceProfile': {'Name': 'LabInstanceProfile'},
        'NetworkInterfaces': [{'DeviceIndex': 0, 'AssociatePublicIpAddress': False,
                               'Groups': ['sg-0a3ae03837c952009']}],
        'MetadataOptions': {'HttpTokens': 'required', 'HttpEndpoint': 'enabled'},
        'CreditSpecification': {'CpuCredits': 'standard'},
        'BlockDeviceMappings': [{'DeviceName': '/dev/xvda', 'Ebs': {
            'VolumeSize': 8, 'VolumeType': 'gp3', 'Encrypted': True, 'DeleteOnTermination': True}}],
        'UserData': base64.b64encode(script.encode()).decode(),
        'TagSpecifications': [{'ResourceType': kind, 'Tags': [
            {'Key': 'Name', 'Value': 'infs3701-team-surge'},
            {'Key': 'Project', 'Value': 'INFS3701'}]} for kind in ['instance', 'volume']],
    }
    group = {
        'AutoScalingGroupName': 'infs3701-team-surge',
        'MinSize': 0, 'MaxSize': 1, 'DesiredCapacity': 0,
        'VPCZoneIdentifier': 'subnet-026f2c6afbe3692e8,subnet-00fc1e9a647c3530e',
        'TargetGroupARNs': [release.TG], 'HealthCheckType': 'ELB',
        'HealthCheckGracePeriod': 300, 'DefaultInstanceWarmup': 180,
        'NewInstancesProtectedFromScaleIn': False,
        'InstanceMaintenancePolicy': {'MinHealthyPercentage': 0, 'MaxHealthyPercentage': 100},
    }
    proposal = {'status': 'OFFLINE_DRAFT_NOT_AUTHORIZED_OR_DEPLOYED',
        'original_hosts_not_attached': release.IDS,
        'launch_template_data': template, 'group_parameters': group,
        'launch_template_reference': 'Resolve newly created template ID and pin its numeric version before CreateAutoScalingGroup.',
        'before_enabling_alarm_actions': 'Suspend AZRebalance and InstanceRefresh while desired=0; verify processes and capacity bounds before policies can launch instances.',
        'policy': {'type': 'SimpleScaling', 'adjustment_type': 'ChangeInCapacity',
            'scale_out': {'adjustment': 1, 'cooldown_seconds': 300,
                'metric': 'AWS/ApplicationELB RequestCount Sum', 'period_seconds': 60,
                'comparison': 'GreaterThanThreshold', 'threshold': 60, 'evaluation_periods': 2},
            'scale_in': {'adjustment': -1, 'cooldown_seconds': 300,
                'metric': 'AWS/ApplicationELB RequestCount Sum', 'period_seconds': 60,
                'comparison': 'LessThanOrEqualToThreshold', 'threshold': 10, 'evaluation_periods': 5},
            'dimensions': {'LoadBalancer': 'app/infs3701-team-alb/cdc408a1dfd1268c'},
            'treat_missing_data': 'notBreaching'},
        'gates': ['Verify permission for automatic AWSServiceRoleForAutoScaling creation; absent at preflight.',
            'Confirm launch-template, ASG, alarms and pass-LabInstanceProfile permissions.',
            'User approval for one additional LabRole-bearing host and its automatic permanent termination.',
            'Refresh running/pending EC2 count; keep account <=9 and group <=1.',
            'Copy diagnostics before scale-in; database is external and must not be deleted.']}
    (out / 'surge-proposal.json').write_text(json.dumps(proposal, indent=2) + '\n', encoding='utf-8')
    (out / 'surge-user-data.sh').write_bytes(script.encode('utf-8'))
    print(json.dumps({'proposal': str(out / 'surge-proposal.json'), 'user_data_bytes': len(script.encode()),
                      'aws_calls': 0, 'status': proposal['status']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('tmp/surge-proposal'))
    build(parser.parse_args().out)
