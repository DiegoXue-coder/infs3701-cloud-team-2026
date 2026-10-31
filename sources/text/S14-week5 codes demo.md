# week5 codes demo.txt

Course: INFS3701. Searchable text; original diagrams and layout remain authoritative.

Classroom demonstration only. Do not submit the Notes/cafe worked example as the group service. Do not execute automatically.

```text

  "AWSTemplateFormatVersion": "2010-09-09",
  "Description": "INFS3701 Week 5 tutorial - the Notes demo service (EC2 + S3) ready to secure. The instance starts WITHOUT a role (Step 1 attaches LabInstanceProfile). Port 8080 is open to the internet (Step 5 narrows it).",
  "Parameters": {
    "LatestAmiId": {
      "Type": "AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>",
      "Default": "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64",
      "Description": "Latest Amazon Linux 2023 image (leave as is)."
    },
    "AttachLabRole": {
      "Type": "String",
      "AllowedValues": [
        "no",
        "yes"
      ],
      "Default": "no",
      "Description": "Leave as 'no' for the tutorial: Step 1 attaches the role by hand. Choose 'yes' only if attaching it by hand is blocked."
    }
  },
  "Conditions": {
    "AttachRole": {
      "Fn::Equals": [
        {
          "Ref": "AttachLabRole"
        },
        "yes"
      ]
    }
  },
  "Resources": {
    "NotesBucket": {
      "Type": "AWS::S3::Bucket",
      "Properties": {
        "Tags": [
          {
            "Key": "course",
            "Value": "INFS3701"
          }
        ]
      }
    },
    "NotesSecurityGroup": {
      "Type": "AWS::EC2::SecurityGroup",
      "Properties": {
        "GroupDescription": "notes-sg: the app on 8080, SSH only from EC2 Instance Connect",
        "SecurityGroupIngress": [
          {
            "IpProtocol": "tcp",
            "FromPort": 8080,
            "ToPort": 8080,
            "CidrIp": "0.0.0.0/0",
            "Description": "Notes app - open to everyone (Step 5 narrows this)"
          },
          {
            "IpProtocol": "tcp",
            "FromPort": 22,
            "ToPort": 22,
            "CidrIp": "18.206.107.24/29",
            "Description": "EC2 Instance Connect service, us-east-1 only"
          }
        ],
        "Tags": [
          {
            "Key": "Name",
            "Value": "notes-sg"
          }
        ]
      }
    },
    "NotesInstance": {
      "Type": "AWS::EC2::Instance",
      "Properties": {
        "ImageId": {
          "Ref": "LatestAmiId"
        },
        "InstanceType": "t3.micro",
        "SecurityGroupIds": [
          {
            "Fn::GetAtt": [
              "NotesSecurityGroup",
              "GroupId"
            ]
          }
        ],
        "IamInstanceProfile": {
          "Fn::If": [
            "AttachRole",
            "LabInstanceProfile",
            {
              "Ref": "AWS::NoValue"
            }
          ]
        },
        "Tags": [
          {
            "Key": "Name",
            "Value": "notes-app"
          }
        ],
        "UserData": {
          "Fn::Base64": {
            "Fn::Sub": "#!/bin/bash\n# INFS3701 Week 5 demo service - installs the Notes app as a systemd service.\nset -x\ndnf -y install python3-pip\npip3 install --quiet flask boto3 || pip3 install --quiet --break-system-packages flask boto3\nmkdir -p /opt/notes\ncat > /opt/notes/app.py <<'APP'\n\"\"\"\nNotes - INFS3701 demo service, WEEK 5 version (securing it).\n\nSame app as Week 3 (every note is an object in S3), plus three things that make\ntoday's security tests visible on the page:\n  * who the app is running as (its AWS identity, or \"no credentials\"),\n  * how each note is encrypted at rest (AES256 = SSE-S3, aws:kms = SSE-KMS),\n  * a Delete button, so a bucket policy that refuses deletes can be seen working.\n\nThere are NO access keys in this file. A new AWS client is made for every\nrequest, so attaching a role to the running instance takes effect without a\nrestart.\n\nRuns on port 8080.  Requires: flask, boto3.\n\"\"\"\nimport datetime\nimport os\nimport uuid\n\nimport boto3\nfrom botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError\nfrom flask import Flask, redirect, render_template_string, request, url_for\n\nBUCKET = os.environ.get(\"NOTES_BUCKET\", \"infs3701-notes-demo\")\nREGION = os.environ.get(\"AWS_REGION\", \"us-east-1\")\nPREFIX = \"notes/\"\n\napp = Flask(__name__)\n\n\ndef client(service):\n    \"\"\"A fresh client each time, so newly attached role credentials are picked up.\"\"\"\n    return boto3.session.Session().client(service, region_name=REGION)\n\n\ndef explain(exc):\n    \"\"\"Turn an AWS error into one plain sentence for the banner.\"\"\"\n    if isinstance(exc, NoCredentialsError):\n        return (\"No AWS credentials: the instance has no role attached, and there are \"\n                \"no keys in the code - so the app cannot reach S3.\")\n    if isinstance(exc, ClientError):\n        err = exc.response.get(\"Error\", {})\n        return \"%s: %s\" % (err.get(\"Code\", \"Error\"), err.get(\"Message\", str(exc)))\n    return str(exc)\n\n\ndef identity():\n    try:\n        arn = client(\"sts\").get_caller_identity()[\"Arn\"]\n        return arn, True\n    except (BotoCoreError, ClientError) as exc:\n        return explain(exc), False\n\n\ndef load_notes(limit=25):\n    s3 = client(\"s3\")\n    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX, MaxKeys=200)\n    objects = sorted(resp.get(\"Contents\", []),\n                     key=lambda o: o[\"LastModified\"], reverse=True)[:limit]\n    notes = []\n    for obj in objects:\n        got = s3.get_object(Bucket=BUCKET, Key=obj[\"Key\"])\n        notes.append({\n            \"text\": got[\"Body\"].read().decode(\"utf-8\", \"replace\"),\n            \"when\": obj[\"LastModified\"].strftime(\"%d %b %Y, %H:%M UTC\"),\n            \"key\": obj[\"Key\"],\n            \"enc\": got.get(\"ServerSideEncryption\", \"none\"),\n        })\n    return notes\n\n\nPAGE = \"\"\"\n<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>Notes - Week 5</title>\n<style>\n body{font-family:system-ui,Arial,sans-serif;max-width:760px;margin:32px auto;padding:0 16px;color:#1A1A1A}\n .who{padding:10px 14px;border-radius:8px;font-weight:600;margin:8px 0}\n .who.ok{background:#FFDB00} .who.bad{background:#FDE2E1;color:#8A1C14}\n .msg{padding:10px 14px;border-radius:8px;margin:8px 0}\n .msg.err{background:#FDE2E1;color:#8A1C14} .msg.info{background:#F5F5F3}\n textarea{width:100%;padding:8px;font:inherit;box-sizing:border-box}\n button{padding:7px 16px;margin-top:6px;cursor:pointer}\n ul{padding:0;list-style:none} li{margin:10px 0;padding:10px 0;border-bottom:1px solid #E4E4E1}\n .meta{color:#6E6E6E;font-size:.85em} .enc{font-family:monospace;background:#F5F5F3;padding:1px 6px;border-radius:4px}\n .row{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}\n code{background:#F5F5F3;padding:2px 6px;border-radius:4px}\n</style></head><body>\n<h1>Notes</h1>\n<div class=\"who {{ 'ok' if who_ok else 'bad' }}\">Running as: {{ who }}</div>\n{% if msg %}<div class=\"msg {{ kind }}\">{{ msg }}</div>{% endif %}\n<p class=\"meta\">Bucket <code>{{ bucket }}</code></p>\n<form method=\"post\" action=\"/add\">\n  <textarea name=\"text\" rows=\"3\" placeholder=\"Write a note...\" required></textarea>\n  <button type=\"submit\">Post note</button>\n</form>\n<h2>{{ notes|length }} note(s)</h2>\n<ul>\n{% for n in notes %}\n  <li><div class=\"row\"><div>{{ n.text }}<br>\n    <span class=\"meta\">{{ n.when }} &middot; encrypted at rest: <span class=\"enc\">{{ n.enc }}</span></span></div>\n    <form method=\"post\" action=\"/delete\"><input type=\"hidden\" name=\"key\" value=\"{{ n.key }}\">\n    <button type=\"submit\">Delete</button></form></div></li>\n{% else %}\n  <li class=\"meta\">Nothing to show yet.</li>\n{% endfor %}\n</ul>\n</body></html>\n\"\"\"\n\n\n@app.route(\"/\")\ndef home():\n    who, who_ok = identity()\n    msg, kind = request.args.get(\"msg\"), request.args.get(\"kind\", \"info\")\n    notes = []\n    if who_ok:\n        try:\n            notes = load_notes()\n        except (BotoCoreError, ClientError) as exc:\n            msg, kind = \"Could not read the bucket. \" + explain(exc), \"err\"\n    return render_template_string(PAGE, who=who, who_ok=who_ok, msg=msg, kind=kind,\n                                  notes=notes, bucket=BUCKET)\n\n\n@app.route(\"/add\", methods=[\"POST\"])\ndef add():\n    text = request.form.get(\"text\", \"\").strip()\n    if not text:\n        return redirect(url_for(\"home\"))\n    key = \"%s%s-%s.txt\" % (PREFIX, datetime.datetime.utcnow().strftime(\"%Y%m%d-%H%M%S\"),\n                           uuid.uuid4().hex[:6])\n    try:\n        client(\"s3\").put_object(Bucket=BUCKET, Key=key, Body=text.encode(\"utf-8\"),\n                                ContentType=\"text/plain\")\n        return redirect(url_for(\"home\", msg=\"Note saved.\", kind=\"info\"))\n    except (BotoCoreError, ClientError) as exc:\n        return redirect(url_for(\"home\", msg=\"Could not save the note. \" + explain(exc), kind=\"err\"))\n\n\n@app.route(\"/delete\", methods=[\"POST\"])\ndef delete():\n    key = request.form.get(\"key\", \"\")\n    if not key.startswith(PREFIX):\n        return redirect(url_for(\"home\"))\n    try:\n        client(\"s3\").delete_object(Bucket=BUCKET, Key=key)\n        return redirect(url_for(\"home\", msg=\"Note deleted.\", kind=\"info\"))\n    except (BotoCoreError, ClientError) as exc:\n        return redirect(url_for(\"home\", msg=\"Could not delete the note. \" + explain(exc), kind=\"err\"))\n\n\n@app.route(\"/health\")\ndef health():\n    try:\n        client(\"s3\").head_bucket(Bucket=BUCKET)\n        return \"ok\", 200\n    except (BotoCoreError, ClientError):\n        return \"bucket unreachable\", 503\n\n\nif __name__ == \"__main__\":\n    app.run(host=\"0.0.0.0\", port=8080, threaded=True)\nAPP\ncat > /etc/systemd/system/notes.service <<'UNIT'\n[Unit]\nDescription=INFS3701 Notes demo app\nAfter=network-online.target\nWants=network-online.target\n\n[Service]\nUser=ec2-user\nWorkingDirectory=/opt/notes\nEnvironment=NOTES_BUCKET=${NotesBucket}\nEnvironment=AWS_REGION=${AWS::Region}\nExecStart=/usr/bin/python3 /opt/notes/app.py\nRestart=always\nRestartSec=3\n\n[Install]\nWantedBy=multi-user.target\nUNIT\ncat > /etc/profile.d/notes.sh <<'PROFILE'\nexport BUCKET=${NotesBucket}\nexport AWS_DEFAULT_REGION=${AWS::Region}\nPROFILE\nsystemctl daemon-reload\nsystemctl enable --now notes.service\n"
          }
        }
      }
    }
  },
  "Outputs": {
    "AppURL": {
      "Description": "Open this in your browser (allow 2-3 minutes after the stack completes)",
      "Value": {
        "Fn::Sub": "http://${NotesInstance.PublicIp}:8080"
      }
    },
    "BucketName": {
      "Description": "Your notes bucket",
      "Value": {
        "Ref": "NotesBucket"
      }
    },
    "BucketArn": {
      "Description": "Paste into the bucket policy (Step 3)",
      "Value": {
        "Fn::GetAtt": [
          "NotesBucket",
          "Arn"
        ]
      }
    },
    "InstanceId": {
      "Description": "The notes-app instance",
      "Value": {
        "Ref": "NotesInstance"
      }
    }
  }
}
```
