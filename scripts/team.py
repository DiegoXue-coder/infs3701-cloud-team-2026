"""Chat-driven synchronization using each member's existing GitHub authentication."""
from __future__ import annotations

import argparse
import base64
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

import team_sync as core

LOCK_REF = 'heads/team-sync-lock'

def existing_token(user):
    value=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if value:return value
    if shutil.which('gh'):
        response=subprocess.run(['gh','auth','token','--hostname','github.com','--user',user],capture_output=True,text=True,timeout=20)
        if response.returncode==0 and response.stdout.strip():return response.stdout.strip()
    env=dict(os.environ,GIT_TERMINAL_PROMPT='0',GCM_INTERACTIVE='never')
    response=subprocess.run(['git','-c','credential.interactive=never','credential','fill'],
        input=f'protocol=https\nhost=github.com\nusername={user}\n\n',capture_output=True,text=True,env=env,timeout=20)
    if response.returncode==0:
        fields=dict(line.split('=',1) for line in response.stdout.splitlines() if '=' in line)
        if fields.get('password'):return fields['password']
    raise RuntimeError('找不到本人已有的 GitHub 授权。请由本人连接 GitHub/gh/Git 凭证；不要把 token 发给同学或写入仓库。')

def decode_json(file):
    return json.loads(base64.b64decode(file['content']).decode('utf-8'))

@contextmanager
def repository_lock(api, actor):
    """Atomic reference creation serializes manual and hosted synchronizers."""
    head=api.head()
    commit=api.request('GET',api.path('/git/commits/'+head))
    lock_commit=api.request('POST',api.path('/git/commits'),{
        'message':f'Temporary task sync lock: {actor} at {core.now()}',
        'tree':commit['tree']['sha'],'parents':[head]})
    try:
        api.request('POST',api.path('/git/refs'),{'ref':'refs/'+LOCK_REF,'sha':lock_commit['sha']})
    except RuntimeError as error:
        if '422' in str(error):
            raise RuntimeError('另一位成员正在同步。稍后重试；认领未确认前不要开始。若长期卡住，由维护者核查锁分支及运行记录，不能直接抢占。') from None
        raise
    try:
        yield
    finally:
        current=api.request('GET',api.path('/git/ref/'+LOCK_REF))
        if current['object']['sha']==lock_commit['sha']:
            api.request('DELETE',api.path('/git/refs/'+LOCK_REF))

def publish(api, directory):
    entries=[{'path':path,'mode':'100644','type':'blob','content':(directory/path).read_text(encoding='utf-8')}
        for path in ['DASHBOARD.md','data/snapshot.json','data/receipts.json']]
    for attempt in range(3):
        head=api.head()
        parent=api.request('GET',api.path('/git/commits/'+head))
        tree=api.request('POST',api.path('/git/trees'),{'base_tree':parent['tree']['sha'],'tree':entries})
        commit=api.request('POST',api.path('/git/commits'),{
            'message':'Sync team task dashboard and AI snapshot','tree':tree['sha'],'parents':[head]})
        try:
            api.request('PATCH',api.path('/git/refs/heads/main'),{'sha':commit['sha'],'force':False})
            return commit['sha']
        except RuntimeError as error:
            if not ('422' in str(error) and attempt<2):raise
    raise RuntimeError('默认分支持续变化，请同步最新状态后重试。')

def report(snapshot,user):
    role=next((role for role,login in snapshot['members'].items() if login and login.casefold()==user.casefold()),None)
    print(json.dumps({'user':user,'role':role,'synced_at':snapshot['generated_at'],
        'self_service':'docs/self-service.md',
        'role_guide':f'docs/member-{role}.md' if role and role!='A' else 'docs/parallel-plan.md',
        'available_roles':[key for key,value in snapshot['members'].items() if key!='A' and not value],
        'dashboard':f"https://github.com/{snapshot['repository']}/blob/main/DASHBOARD.md",
        'current':[{'id':t['id'],'title':t['title'],'status':t['status'],'completion_waiting_for':t['waiting_for'],
            'start_waiting_for':t.get('start_waiting_for',t['waiting_for']),'early_steps':t.get('early_steps',[]),'url':t['issue_url']}
            for t in snapshot['tasks'] if str(t.get('owner') or '').casefold()==user.casefold() and t['status'] not in {'done','skipped'}],
        'ready':[{'id':t['id'],'title':t['title'],'completion_waiting_for':t['waiting_for'],
            'early_steps':t.get('early_steps',[]),'url':t['issue_url']}
            for t in snapshot['tasks'] if t['role']==role and t['status']=='todo' and not t.get('start_waiting_for',t['waiting_for'])],
        'needs_review':[{'id':t['id'],'title':t['title'],'owner':t.get('owner'),'url':t['issue_url']}
            for t in snapshot['tasks'] if t['status']=='review' and str(t.get('owner') or '').casefold()!=user.casefold()]},ensure_ascii=False,indent=2))

def enroll(api, user, role):
    """Called under repository_lock, after authenticated private-repo write checks."""
    if role not in {'B','C','D'}:
        raise ValueError('Self-service roles: B (application), C (testing), D (report/presentation). AWS operator A cannot be taken over.')
    source=api.get_file('project/config.json')
    config=decode_json(source)
    members=config['members']
    if role not in members:
        raise ValueError('This role is not configured in the repository. Ask the maintainer to prepare the role first.')
    bound=next((key for key,login in members.items() if login and login.casefold()==user.casefold()),None)
    if bound and bound!=role:
        raise ValueError('本人已经绑定其他角色，不能自动换岗；保留原身份与贡献记录。')
    occupant=members.get(role)
    if occupant and occupant.casefold()!=user.casefold():
        raise ValueError('这个角色已有成员，不能覆盖；请使用自己的分工。')
    if bound==role:
        return config
    members[role]=user
    config.setdefault('enrollment_history',[]).append({'actor':user,'role':role,'at':core.now()})
    content=json.dumps(config,ensure_ascii=False,indent=2)+'\n'
    api.request('PUT',api.path('/contents/project/config.json'),{
        'message':f'Join team role {role}: {user}',
        'sha':source['sha'],'branch':'main',
        'content':base64.b64encode(content.encode('utf-8')).decode('ascii')})
    return config

def diagnose(api, user):
    """Read-only connection check; never claim work, process comments or commit."""
    config=decode_json(api.get_file('project/config.json'))
    manifest=decode_json(api.get_file('sources/manifest.json'))
    snapshot=decode_json(api.get_file('data/snapshot.json'))
    readme=api.get_file('README.md')
    index=api.get_file('sources/INDEX.md')
    board=api.get_file('LIVE_BOARD.md')
    issues=api.issue_list()
    cards=[row for row in issues if core.parse_state(row.get('body'))]
    workflow=api.request('GET',api.path('/actions/workflows/team-sync.yml'))
    role=next((key for key,login in config['members'].items() if login and login.casefold()==user.casefold()),None)
    return {'checked_at':core.now(),'mode':'read_only_no_progress_changed','repository':config['repository'],
        'authenticated_user':user,'role':role,'readme_readable':readme.get('type')=='file',
        'available_roles':[key for key,value in config['members'].items() if key!='A' and not value],
        'preferred_language':config.get('member_languages',{}).get(role,'en' if role=='D' else 'zh'),
        'role_guide':f'docs/member-{role}.md' if role and role!='A' else 'docs/parallel-plan.md',
        'self_service':'docs/self-service.md',
        'source_index_readable':index.get('type')=='file','online_entry_readable':board.get('type')=='file',
        'source_files':len(manifest),'courses':sorted({'INFS3701' if item['source_origin'].startswith('source_materials/INFS3701/') else 'UNEXPECTED' for item in manifest}),
        'task_cards':len(cards),'snapshot_generated_at':snapshot['generated_at'],
        'hosted_workflow_state':workflow.get('state'),'connector_access':'not tested by this helper; Git/REST authentication only',
        'online_entry':f"https://github.com/{config['repository']}/blob/main/LIVE_BOARD.md"}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--user',required=True,help='Your own GitHub username')
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('start');sub.add_parser('sync');sub.add_parser('doctor')
    join=sub.add_parser('join');join.add_argument('--role',required=True,choices=['B','C','D'])
    cmd=sub.add_parser('command');cmd.add_argument('task');cmd.add_argument('--body-file',required=True)
    args=parser.parse_args()
    local=core.load_config()
    os.environ['GH_TOKEN']=existing_token(args.user)
    api=core.GitHub(local)
    identity=api.request('GET','/user')['login']
    if identity.casefold()!=args.user.casefold():raise RuntimeError('当前授权账号与指定本人不一致，停止操作。')
    if api.permission(identity) not in {'write','maintain','admin'}:raise RuntimeError('当前账号没有本仓库的写权限。')
    if not api.request('GET',api.path(''))['private']:raise RuntimeError('课程协作仓库必须保持私有。')
    if args.command=='doctor':
        print(json.dumps(diagnose(api,identity),ensure_ascii=False,indent=2))
        return
    with repository_lock(api,identity):
        config=decode_json(api.get_file('project/config.json'))
        if config['repository']!=local['repository']:raise RuntimeError('远程仓库配置与本地目标不一致。')
        if args.command=='join':
            config=enroll(api,identity,args.role)
        tasks=decode_json(api.get_file('project/tasks.json'))
        core.validate_plan(tasks,config)
        comment_seed={}
        if args.command=='command':
            if args.task not in {task['id'] for task in tasks}:raise RuntimeError('未知任务号。')
            body=Path(args.body_file).read_text(encoding='utf-8').strip()
            if not body.startswith('/team ') or len(body)>5000:raise RuntimeError('命令文件应以 /team 开头，且不超过 5000 字符。')
            rows=api.issue_list()
            matches=[row for row in rows if (core.parse_state(row.get('body')) or {}).get('task_id')==args.task]
            if len(matches)!=1:raise RuntimeError('无法唯一找到任务卡，停止以避免更新错任务。')
            posted=api.request('POST',api.path(f"/issues/{matches[0]['number']}/comments"),{'body':body})
            comment_seed[args.task]=[posted]
        with tempfile.TemporaryDirectory(prefix='team-sync-') as folder:
            directory=Path(folder)
            core.synchronize(api,tasks,config,root=directory,comment_seed=comment_seed)
            sha=publish(api,directory)
            snapshot=json.loads((directory/'data/snapshot.json').read_text(encoding='utf-8'))
            print('GitHub dashboard saved at commit '+sha[:12])
            report(snapshot,identity)

if __name__=='__main__':
    try:main()
    except (RuntimeError,ValueError) as error:raise SystemExit(str(error))
