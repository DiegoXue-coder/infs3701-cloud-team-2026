#!/bin/bash
set -euo pipefail
exec > >(tee -a /var/log/infs3701-surge.log /dev/console) 2>&1
/opt/infs3701/venv/bin/python - <<'SURGEPY'
"""Run with the existing runtime Python as root, via cloud-init per-boot.

Only fictional course data is permitted. This script never changes IAM/network
or deletes database records. The saved foundation remains available for rollback.
"""
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.request

import boto3
from botocore.config import Config

BASE = Path('/opt/infs3701')
CURRENT = BASE / 'current'
ENV = Path('/etc/infs3701/app.env')
BACKUP = BASE / 'foundation-backup'


def restart():
    subprocess.run(['systemctl', 'restart', 'infs3701-app'], check=True)


def check(label, stage):
    for attempt in range(25):
        try:
            with urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4) as r:
                health = json.load(r)
                assert r.headers['X-App-Instance'] == label
            assert health['stage'] == stage and health['instance'] == label
            # Unlike /health, GET / verifies a real database read in business mode.
            with urllib.request.urlopen('http://127.0.0.1:8000/', timeout=15) as r:
                page = r.read().decode()
                assert r.status == 200
                assert ('Reading Tracker' in page) if stage == 'reading-tracker' else ('infrastructure ready' in page)
            return health
        except Exception:
            if attempt == 24:
                raise
            time.sleep(1)


def switch(target):
    temporary = BASE / 'next-current'
    if temporary.is_symlink():
        temporary.unlink()
    os.symlink(str(target), str(temporary))
    # Initial current is a directory; preserve it before the atomic symlink switch.
    if CURRENT.is_dir() and not CURRENT.is_symlink():
        CURRENT.rename(BASE / 'initial-current-preserved')
    os.replace(temporary, CURRENT)


def main(plan):
    assert os.geteuid() == 0
    label, mode = plan['label'], plan['mode']
    assert __import__('re').fullmatch(r'asg-i-[0-9a-f]{17}', label) and mode == 'release'
    if not BACKUP.exists():
        assert mode == 'release'
        stage = BASE / 'foundation-backup-staging'
        stage.mkdir(exist_ok=True)
        shutil.copytree(CURRENT, stage / 'app', dirs_exist_ok=True)
        shutil.copy2(ENV, stage / 'app.env')
        # Existing baseline must actually be the known placeholder.
        assert 'infrastructure-only' in (stage / 'app/app.py').read_text()
        stage.rename(BACKUP)
    if mode == 'rollback':
        switch(BACKUP / 'app')
        shutil.copy2(BACKUP / 'app.env', ENV)
        restart()
        print('INFS3701_ROLLBACK_OK=' + json.dumps(check(label, 'infrastructure-only')), flush=True)
        return

    commit = plan['commit']
    assert len(commit) == 40 and all(c in '0123456789abcdef' for c in commit)
    blocked = BASE / ('release-blocked-' + commit)
    if blocked.exists():
        raise RuntimeError('Prior failed release is blocked; inspect and explicitly rollback before retry')
    session = boto3.Session(region_name='us-east-1')
    assert session.get_credentials().method == 'iam-role'
    client = session.client('s3', config=Config(connect_timeout=4, read_timeout=12, retries={'total_max_attempts': 2}))
    raw = client.get_object(Bucket=plan['bucket'], Key=plan['key'])['Body'].read(1000001)
    assert len(raw) <= 1000000 and hashlib.sha256(raw).hexdigest() == plan['archive_sha256']
    release = BASE / 'releases' / commit
    release.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as archive:
        members = archive.getmembers()
        assert sorted(m.name for m in members) == ['app.py', 'requirements.txt']
        for member in members:
            assert member.isfile() and member.size < 1000000
            content = archive.extractfile(member).read()
            assert hashlib.sha256(content).hexdigest() == plan['files'][member.name]
            path = release / member.name
            path.write_bytes(content)
            path.chmod(0o644)
    # Compilation/import runs with the production interpreter and actual dependencies.
    subprocess.run([sys.executable, '-m', 'py_compile', str(release / 'app.py')], check=True)
    installed = {x.split('==')[0].lower(): x.split('==')[1] for x in subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], text=True).splitlines() if '==' in x}
    expected = [x.strip().split('==') for x in (release / 'requirements.txt').read_text().splitlines() if x.strip() and not x.startswith('#')]
    assert all(installed.get(name.lower()) == version for name, version in expected), 'Runtime lock mismatch'
    env = '\n'.join(['APP_INSTANCE=' + label, 'APP_PORT=8000', 'READING_DATA_MODE=dynamodb', 'READING_TABLE=infs3701-team-books', 'AWS_DEFAULT_REGION=us-east-1', 'AWS_REGION=us-east-1', ''])
    # Initial directory is renamed by switch(); the immutable backup is its
    # stable rollback path. A pointer to /current itself would become a loop.
    previous = CURRENT.resolve() if CURRENT.is_symlink() else BACKUP / 'app'
    previous_env = ENV.read_bytes()
    try:
        ENV.write_text(env)
        ENV.chmod(0o644)
        switch(release)
        restart()
        health = check(label, 'reading-tracker')
        marker = {'commit': commit, 'archive_sha256': plan['archive_sha256'], 'source_sha256': plan['files']['app.py'], 'instance': label, 'credential_source': 'iam-role', 'health': health, 'business_get': 200, 'python': sys.version.split()[0]}
        (BASE / 'active-release.json').write_text(json.dumps(marker))
        print('INFS3701_RELEASE_OK=' + json.dumps(marker), flush=True)
    except Exception:
        blocked.write_text('Release failed; previous app restored. Inspect journal/console.\n')
        switch(previous)
        ENV.write_bytes(previous_env)
        restart()
        print('INFS3701_RELEASE_FAILED_RESTORED_PREVIOUS', flush=True)
        raise


if False:
    main(json.loads(sys.argv[1]))


request = urllib.request.Request('http://169.254.169.254/latest/api/token',
    headers={'X-aws-ec2-metadata-token-ttl-seconds':'60'}, method='PUT')
with urllib.request.urlopen(request, timeout=3) as response:
    token = response.read().decode()
request = urllib.request.Request('http://169.254.169.254/latest/meta-data/instance-id',
    headers={'X-aws-ec2-metadata-token':token})
with urllib.request.urlopen(request, timeout=3) as response:
    instance_id = response.read().decode()

plan = {'commit': '06c2292cdf0aca80f050709b8172fac3595b54cc', 'bucket': 'infs3701-team-artifacts-214018170594', 'key': 'releases/reading-tracker/06c2292cdf0aca80f050709b8172fac3595b54cc/app.tar.gz', 'archive_sha256': 'fc40e1969c6b90f154b120979aaddf45f554d6e5fdd0fa6b0b2d17fd2ac980cd', 'files': {'app.py': 'a0eb70b7e8a9505e912c14fead268e9c0798064e35708243404c250def1abfb5', 'requirements.txt': '0c3bfc3d3602f536f24ba1ff9ea7e6790f82e0c3299e2abd98f3ef5a99e7547e'}, 'public_scope': 'Existing HTTP ALB becomes unauthenticated fictional-demo list/add. No real personal data. TLS unresolved.', 'hosts': {'a': 'i-00572a14ca8b71156', 'b': 'i-0081259c52a32e051'}, 'rollback': 'Per-host foundation backup; rollback mode retains database and release files.', 'mode': 'release'}
plan['label'] = 'asg-' + instance_id
if not ENV.exists():
    ENV.write_text('APP_INSTANCE=' + plan['label'] + '\nAPP_PORT=8000\n')
subprocess.run(['systemctl', 'enable', 'infs3701-app'], check=True)
main(plan)

SURGEPY
