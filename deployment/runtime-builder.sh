#!/bin/bash
set -euxo pipefail
exec > >(tee -a /var/log/infs3701-runtime-build.log /dev/console) 2>&1
dnf install -y python3.11 python3.11-pip
mkdir -p /opt/infs3701/current /etc/infs3701
python3.11 -m venv /opt/infs3701/venv
/opt/infs3701/venv/bin/python -m pip install --upgrade pip
/opt/infs3701/venv/bin/python -m pip install Flask boto3 gunicorn
/opt/infs3701/venv/bin/python -m pip freeze > /opt/infs3701/runtime-requirements.lock
cat > /opt/infs3701/current/app.py <<'PYAPP'
import os
from flask import Flask, jsonify
app=Flask(__name__)
@app.after_request
def identify(response):
 response.headers['X-App-Instance']=os.getenv('APP_INSTANCE','unconfigured')
 return response
@app.get('/health')
def health():
 return jsonify(status='ok',instance=os.getenv('APP_INSTANCE','unconfigured'),stage='infrastructure-only')
@app.get('/')
def home():
 return '<h1>INFS3701 infrastructure ready</h1><p>Reading Tracker application has not been deployed here yet.</p>'
PYAPP
cat > /etc/systemd/system/infs3701-app.service <<'UNIT'
[Unit]
Description=INFS3701 staged application runtime
After=network-online.target
Wants=network-online.target
[Service]
User=ec2-user
WorkingDirectory=/opt/infs3701/current
EnvironmentFile=-/etc/infs3701/app.env
ExecStart=/opt/infs3701/venv/bin/gunicorn --bind 0.0.0.0:8000 --workers 2 --access-logfile - --error-logfile - app:app
Restart=on-failure
RestartSec=3
[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
/opt/infs3701/venv/bin/python -c 'import sys,flask,boto3,gunicorn; print("RUNTIME_IMPORTS_OK",sys.version.split()[0])'
cat /opt/infs3701/runtime-requirements.lock
printf 'INFS3701_RUNTIME_READY\n'
