"""Capture one already-authorized command as a task execution record; no shell."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import shlex
import subprocess
import sys

def redact(text):
    text=re.sub(r'(?:AKIA|ASIA)[A-Z0-9]{16}','[REDACTED AWS access key]',text)
    text=re.sub(r'(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})','[REDACTED GitHub token]',text)
    return re.sub(r'(?im)^.*(?:aws_secret_access_key|aws_session_token|github_token|gh_token|authorization\s*:|password\s*[:=]).*$','[REDACTED credential-bearing line]',text)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task',required=True);parser.add_argument('--actor',required=True)
    parser.add_argument('--output',required=True);parser.add_argument('command',nargs=argparse.REMAINDER)
    args=parser.parse_args();command=args.command[1:] if args.command[:1]==['--'] else args.command
    if not command:parser.error('Provide an authorized command after --')
    if not re.fullmatch(r'T\d{2}',args.task):parser.error('Invalid task ID')
    output=Path(args.output)
    if output.exists():parser.error('Output already exists; use a new run filename to preserve history')
    started=datetime.now(timezone.utc).isoformat(timespec='seconds')
    run=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
    finished=datetime.now(timezone.utc).isoformat(timespec='seconds')
    shown=[];hide_next=False
    for value in command:
        if hide_next:shown.append('[REDACTED]');hide_next=False;continue
        if value.lower() in {'--password','--token','--secret-access-key','--session-token'}:
            shown.append(value);hide_next=True
        else:shown.append(value)
    content=f'Task: {args.task}\nGitHub actor: {args.actor}\nExecuted by: local command runner (AI-assisted)\nStarted UTC: {started}\nFinished UTC: {finished}\nExit code: {run.returncode}\nCommand: {shlex.join(shown)}\n\nSTDOUT\n'+run.stdout.decode('utf-8',errors='replace')+'\nSTDERR\n'+run.stderr.decode('utf-8',errors='replace')
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(redact(content)+'\n',encoding='utf-8',newline='\n')
    print(f'Execution record saved: {output}; exit code: {run.returncode}. Review for sensitive data before upload.')
    return run.returncode

if __name__=='__main__':sys.exit(main())
