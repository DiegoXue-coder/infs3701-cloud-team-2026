"""Local onboarding checks; never accesses AWS or stores credentials."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import venv

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--role',required=True,choices=['B','C'])
    parser.add_argument('--install',action='store_true',help='Create .venv and install app requirements plus tzdata')
    args=parser.parse_args()
    if sys.version_info<(3,9):
        raise SystemExit('Python 3.9+ is required.')
    python=Path(sys.executable)
    if args.install:
        destination=ROOT/'.venv'
        venv.EnvBuilder(with_pip=True).create(destination)
        python=destination/('Scripts/python.exe' if sys.platform=='win32' else 'bin/python')
        subprocess.run([str(python),'-m','pip','install','-r',str(ROOT/'app/requirements.txt'),'tzdata'],check=True,cwd=ROOT)
    subprocess.run([str(python),str(ROOT/'scripts/check_reading_baseline.py')],check=True,cwd=ROOT)
    print(json.dumps({'role':args.role,'python':str(python),
        'role_guide':f'docs/member-{args.role}.md','handoffs':'project/handoffs.json',
        'local_baseline':'passed','dependencies_installed_by_this_command':args.install,
        'full_web_runtime_tested':False,'AWS_accessed':False,
        'next':'Authenticate your own GitHub, run doctor, then join your assigned role.'},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
