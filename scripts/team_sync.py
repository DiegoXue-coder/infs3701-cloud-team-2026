"""Deterministic GitHub task coordinator. No LLM or AWS credentials required."""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

ROOT = Path(__file__).resolve().parents[1]
STATE_RE = re.compile(r'<!-- team-state\s*\n(.*?)\n-->', re.S)
STATUS = {'todo':'未开始','in_progress':'进行中','blocked':'被卡住','review':'等检查','done':'已完成','skipped':'未启用（可选）'}
COLORS = {'todo':'d9e1e8','in_progress':'0969da','blocked':'cf222e','review':'bf8700','done':'1a7f37','skipped':'8250df'}

def load_config(root=ROOT):
    return json.loads((root/'project/config.json').read_text(encoding='utf-8'))

def load_tasks(root=ROOT):
    return json.loads((root/'project/tasks.json').read_text(encoding='utf-8'))

def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')

def initial_state(task, config):
    return {'task_id':task['id'],'status':'skipped' if task['optional'] and not config['enhancements_enabled'] else 'todo',
        'owner':None,'owner_role':None,'submission':None,'reviewer':None,'last_update':None,
        'last_note':'可选增强尚未启用' if task['optional'] and not config['enhancements_enabled'] else '尚未认领',
        'processed_comments':[]}

def parse_state(body):
    match = STATE_RE.search(body or '')
    return json.loads(match.group(1)) if match else None

def required_dependencies(task, config):
    result = list(task['depends_on'])
    if config['enhancements_enabled'] and task['id'] in {'T17','T18','T19','T20'}:
        result.append('T16')
    return result

def unmet_dependencies(task, states, config):
    return [key for key in required_dependencies(task,config) if states.get(key,{}).get('status') != 'done']

def text_cell(value):
    return str(value or '—').replace('|','／').replace('\n',' ')[:250]

def issue_body(task, state, config):
    lines=[f"<!-- team-task:{task['id']} -->",f"# {task['id']} · {task['title']}",'',
        f"主责角色：**{task['role']}**；建议检查角色：{task['reviewer_role']}（必须不同 GitHub 用户）",
        f"内部计划：{task['start']} → {task['due']}（悉尼日期；不是课程新增截止）",
        '前置任务：'+('、'.join(required_dependencies(task,config)) or '无'),'',
        '## 具体做法','']
    lines += [f'{i}. {step}' for i,step in enumerate(task['steps'],1)]
    if task.get('materials'):
        lines += ['', '## 相关课件与示例','']
        for item in task['materials']:
            url=f"https://github.com/{config['repository']}/blob/main/"+urllib.parse.quote(item['path'],safe='/')
            lines.append(f"- [{item['source_id']} · {item['title']}]({url})")
        lines.append('课堂示例仅用于理解与改造，不能直接作为本组最终服务。')
    lines += ['', '## 验收标准','']+[f'- {item}' for item in task['acceptance']]
    lines += ['', '## 怎样更新','',
        f"评论 `/team claim {task['role']}` 认领；等系统确认再操作。",
        f"完成后提交真实 JSON 交付文件，再评论 `/team submit deliveries/{task['id']}/日期-用户名.json`。",
        '另一位成员实际检查后评论 `/team approve 检查说明`；有问题用 `/team changes 需要修改什么`。',
        '更新 `/team progress 实际进度`；遇阻 `/team block 问题与需要谁协助`。',
        '', f"[完整规则](https://github.com/{config['repository']}/blob/main/docs/team-protocol.md) · [操作手册](https://github.com/{config['repository']}/blob/main/docs/execution-guide.md)",
        '', '## 同步状态（系统维护）','',
        f"- 状态：**{STATUS[state['status']]}**",
        '- 负责人：'+text_cell(state.get('owner')),
        '- 最近记录：'+text_cell(state.get('last_note')),
        '- 时间：'+text_cell(state.get('last_update')),
        '', '<!-- team-state',json.dumps(state,ensure_ascii=False,separators=(',',':')),'-->']
    return '\n'.join(lines)+'\n'

class GitHub:
    def __init__(self, config):
        self.repo = config['repository']
        self.token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
        if not self.token:
            raise RuntimeError('需要当前用户获准的 GH_TOKEN/GITHUB_TOKEN；不要把 token 写进仓库。')

    def request(self, method, path, data=None):
        request=urllib.request.Request('https://api.github.com'+path,
            data=json.dumps(data).encode() if data is not None else None,
            headers={'Authorization':'Bearer '+self.token,'Accept':'application/vnd.github+json',
                'X-GitHub-Api-Version':'2022-11-28','User-Agent':'infs3701-team-hub','Content-Type':'application/json',
                'Cache-Control':'no-cache'},method=method)
        try:
            with urllib.request.urlopen(request,timeout=45) as response:
                body=response.read()
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as error:
            try: message=json.loads(error.read()).get('message','request failed')
            except ValueError: message='request failed'
            raise RuntimeError(f'GitHub HTTP {error.code}: {message}') from None

    def path(self, suffix):
        return f'/repos/{self.repo}'+suffix

    def pages(self, path):
        page=1
        while True:
            sep='&' if '?' in path else '?'
            rows=self.request('GET',f'{path}{sep}per_page=100&page={page}')
            yield from rows
            if len(rows)<100: break
            page+=1

    def issue_list(self):
        return list(self.pages(self.path('/issues?state=all&sort=created&direction=asc')))

    def comments(self, number):
        return list(self.pages(self.path(f'/issues/{number}/comments')))

    def permission(self, user):
        return self.request('GET',self.path(f'/collaborators/{urllib.parse.quote(user,safe="")}/permission'))['permission']

    def get_file(self, path, ref='main'):
        safe=validate_path(path)
        return self.request('GET',self.path('/contents/'+urllib.parse.quote(safe,safe='/'))+'?ref='+urllib.parse.quote(ref,safe=''))

    def head(self):
        return self.request('GET',self.path('/git/ref/heads/main'))['object']['sha']

def validate_path(value):
    if not isinstance(value,str) or not value or '\\' in value or ':' in value or value.startswith('/'):
        raise ValueError('交付必须是仓库内相对路径。')
    path=PurePosixPath(value)
    if '..' in path.parts or str(path)!=value or not path.parts:
        raise ValueError('路径不能含跳转或非规范目录。')
    return value

def validate_delivery(api, task, actor, path, timestamp=None):
    validate_path(path)
    if not path.startswith(f"deliveries/{task['id']}/") or not path.endswith('.json'):
        raise ValueError(f"请提交 deliveries/{task['id']}/ 下的真实 JSON 交付文件。")
    ref=api.head()
    file=api.get_file(path,ref)
    if file.get('type')!='file' or not 50<file.get('size',0)<100_000:
        raise ValueError('交付文件缺失、为空或过大。')
    delivery=json.loads(base64.b64decode(file['content']).decode('utf-8'))
    if delivery.get('task_id')!=task['id'] or str(delivery.get('actor','')).casefold()!=actor.casefold():
        raise ValueError('交付中的任务号和操作者必须与本次任务及评论人一致。')
    for field in ['environment','summary','limitations','next_step','ai_use']:
        value=delivery.get(field)
        if not isinstance(value,str) or not value.strip() or 'REPLACE_' in value:
            raise ValueError(f'交付缺少真实 {field} 字段。')
    tested=datetime.fromisoformat(delivery.get('tested_at','').replace('Z','+00:00'))
    if tested.tzinfo is None or tested.astimezone(timezone.utc).timestamp()>datetime.now(timezone.utc).timestamp()+300:
        raise ValueError('测试时间必须含时区，且不能是未来时间。')
    tests=delivery.get('tests')
    if not isinstance(tests,list) or not tests or not all(isinstance(t,dict) and all(isinstance(t.get(k),str) and t[k].strip() for k in ['action','expected','actual']) for t in tests):
        raise ValueError('请记录实际测试/核对的步骤、期望及实际结果。')
    evidence=delivery.get('evidence')
    if not isinstance(evidence,list) or not evidence or not all(isinstance(p,str) for p in evidence):
        raise ValueError('至少引用一个真实证据文件。')
    evidence_shas={}
    for item in evidence:
        validate_path(item)
        if item==path or item.startswith(('templates/','sources/','data/')) or item in {'DASHBOARD.md','README.md'}:
            raise ValueError('模板、课程原件或进度表不能代替实际交付证据。')
        evidence_file=api.get_file(item,ref)
        if evidence_file.get('type')!='file' or not evidence_file.get('size'):
            raise ValueError(f'证据文件不存在或为空：{item}')
        evidence_shas[item]=evidence_file['sha']
    return {'path':path,'commit':ref,'manifest_sha':file['sha'],'evidence_shas':evidence_shas,
        'summary':delivery['summary'][:1000],'tested_at':delivery['tested_at'],'submitted_by':actor}

def validate_review(api, submission):
    if api.get_file(submission['path'])['sha']!=submission['manifest_sha']:
        raise ValueError('交付文件在提交后已修改，请重新 submit 后再复核。')
    for path,sha in submission['evidence_shas'].items():
        if api.get_file(path)['sha']!=sha:
            raise ValueError('证据已修改，请重新 submit 后再复核。')

def apply_command(api, task, state, states, config, actor, command, args, timestamp):
    """Pure state transition apart from explicit evidence checks. Caller serializes events."""
    result=json.loads(json.dumps(state))
    maintainer=actor.casefold() in {x.casefold() for x in config['maintainers']}
    assigned=config['members'].get(task['role'])
    is_owner=str(state.get('owner') or '').casefold()==actor.casefold()
    if command=='status':
        waiting=unmet_dependencies(task,states,config)
        return result,f"{task['id']}：{STATUS[state['status']]}；负责人 {state.get('owner') or '未认领'}；前置未完成 {', '.join(waiting) or '无'}。"
    if command=='claim':
        role=args.strip().upper()
        if role!=task['role'] or (not maintainer and str(assigned or '').casefold()!=actor.casefold()):
            raise ValueError('角色与任务不匹配或尚未登记。请先更新成员配置；管理员可记录接替。')
        if state['status']=='skipped': raise ValueError('可选增强尚未启用；需小组决定并更新配置。')
        if state['status']=='done': raise ValueError('任务已完成；如需返工先由他人提出 changes。')
        if state.get('owner') and not is_owner: raise ValueError('任务已由其他成员认领，请协调交接，不能覆盖。')
        waiting=unmet_dependencies(task,states,config)
        if waiting: raise ValueError('前置任务还未完成：'+', '.join(waiting))
        if is_owner: return result,'已由你认领，保留当前状态。'
        result.update(status='in_progress',owner=actor,owner_role=role,last_note='已认领'+('（管理员接替未绑定角色）' if maintainer and str(assigned or '').casefold()!=actor.casefold() else ''))
    elif command in {'progress','block','resume','submit'}:
        if not is_owner: raise ValueError('只有实际认领人可以更新或提交此任务。')
        if state['status'] in {'done','skipped'}: raise ValueError('该状态不能直接更新，请先安排返工或启用任务。')
        if command in {'progress','block'}:
            if not args.strip(): raise ValueError('请补充实际进度或阻碍原因。')
            result['last_note']=args.strip()[:2000]
            if command=='block': result['status']='blocked'
        elif command=='resume':
            waiting=unmet_dependencies(task,states,config)
            if waiting: raise ValueError('前置条件仍未满足：'+', '.join(waiting))
            result.update(status='in_progress',last_note=args.strip() or '恢复工作')
        else:
            paths=shlex.split(args)
            if len(paths)!=1: raise ValueError('submit 后只填写一个交付 JSON 路径。')
            waiting=unmet_dependencies(task,states,config)
            if waiting: raise ValueError('前置条件尚未完成：'+', '.join(waiting))
            submission=validate_delivery(api,task,actor,paths[0],timestamp)
            result.update(status='review',submission=submission,reviewer=None,last_note='已提交真实文件，等待另一成员检查：'+submission['summary'])
    elif command in {'approve','changes'}:
        if not state.get('owner') or is_owner: raise ValueError('必须由另一 GitHub 用户复核，不能自己批准或假装他人检查。')
        if not args.strip(): raise ValueError('请写清实际检查了什么或需要修改什么。')
        if command=='approve':
            if state['status']!='review' or not state.get('submission'): raise ValueError('当前没有待检查的交付。')
            waiting=unmet_dependencies(task,states,config)
            if waiting: raise ValueError('前置任务被重新打开，需要先解决：'+', '.join(waiting))
            validate_review(api,state['submission'])
            result.update(status='done',reviewer=actor,last_note='复核通过：'+args.strip()[:1900])
        else:
            if state['status'] not in {'review','done'}: raise ValueError('只有待检查或已完成任务可以提出返工。')
            result.update(status='in_progress',reviewer=actor,last_note='需要修改：'+args.strip()[:1900])
    else:
        raise ValueError('未知命令；支持 claim / progress / block / resume / submit / approve / changes / status。')
    result['last_update']=timestamp
    return result,f"{task['id']} 已更新为「{STATUS[result['status']]}」。{result['last_note']}"

def bootstrap(api, tasks, config):
    repository=api.request('GET',api.path(''))
    if not repository.get('private'): raise RuntimeError('只允许在 private 仓库初始化课程资料系统。')
    labels={label['name'] for label in api.pages(api.path('/labels'))}
    definitions={'task':('0366d6','小组任务'),**{f'role:{role}':('7057ff',f'角色 {role}') for role in 'ABC'},
        **{f'status:{key}':(COLORS[key],value) for key,value in STATUS.items()}}
    for name,(color,description) in definitions.items():
        if name not in labels: api.request('POST',api.path('/labels'),{'name':name,'color':color,'description':description})
    existing={}
    for issue in api.issue_list():
        if 'pull_request' in issue: continue
        state=parse_state(issue.get('body'))
        if state:
            key=state['task_id']
            if key in existing: raise RuntimeError('任务 Issue 重复：'+key)
            existing[key]=issue
    for task in tasks:
        if task['id'] in existing: continue
        state=initial_state(task,config)
        issue=api.request('POST',api.path('/issues'),{'title':f"[{task['id']}] {task['title']}",
            'body':issue_body(task,state,config),'labels':['task',f"role:{task['role']}",f"status:{state['status']}"]})
        existing[task['id']]=issue
    return existing

def synchronize(api, tasks, config, root=ROOT, issue_seed=None, comment_seed=None):
    by_id={task['id']:task for task in tasks}
    issues={}
    for issue in api.issue_list():
        if 'pull_request' in issue: continue
        state=parse_state(issue.get('body'))
        if state and state.get('task_id') in by_id:
            if state['task_id'] in issues: raise RuntimeError('发现重复任务 Issue，停止以避免覆盖。')
            issues[state['task_id']]=issue
    # Newly created Issues can briefly lag in the list endpoint. Reuse only
    # confirmed bootstrap responses for cards not yet visible in that list.
    for key,issue in (issue_seed or {}).items():
        if key not in issues and key in by_id:
            issues[key]=issue
    missing=set(by_id)-set(issues)
    if missing: raise RuntimeError('缺少任务卡，先运行 bootstrap：'+', '.join(sorted(missing)))
    # Read each authoritative card directly; recently mutated list responses can lag.
    for key,issue in list(issues.items()):
        issues[key]=api.request('GET',api.path(f"/issues/{issue['number']}"))
    states={key:parse_state(issue['body']) for key,issue in issues.items()}
    events=[]
    for key,issue in issues.items():
        task=by_id[key];state=states[key]
        if task['optional']:
            if not config['enhancements_enabled'] and state['status'] not in {'done','skipped'}:
                state.update(status='skipped',last_note='小组尚未启用可选增强')
            elif config['enhancements_enabled'] and state['status']=='skipped':
                state.update(status='todo',last_note='已启用增强，待认领')
        comments=api.comments(issue['number'])
        seen={comment['id'] for comment in comments}
        comments += [comment for comment in (comment_seed or {}).get(key,[]) if comment['id'] not in seen]
        for comment in comments:
            first=(comment.get('body') or '').strip().split('\n',1)[0]
            if first.startswith('/team ') and comment['id'] not in state.get('processed_comments',[]):
                events.append((comment['id'],key,comment,first))
    permissions={}
    for comment_id,key,comment,line in sorted(events):
        state=states[key]; actor=comment['user']['login']
        try:
            if actor not in permissions: permissions[actor]=api.permission(actor)
            if permissions[actor] not in {'write','maintain','admin'}:
                raise ValueError('只有有写权限的小组成员可以操作任务。')
            parts=line.split(maxsplit=2)
            if len(parts)<2: raise ValueError('缺少命令。')
            command=parts[1].lower();args=parts[2] if len(parts)>2 else ''
            next_state,message=apply_command(api,by_id[key],state,states,config,actor,command,args,comment['created_at'])
        except (ValueError,KeyError,TypeError,json.JSONDecodeError,RuntimeError) as error:
            next_state=json.loads(json.dumps(state));message='未更新：'+str(error)
        next_state.setdefault('processed_comments',[]).append(comment_id)
        states[key]=next_state
        # Persist before acknowledgment; a retry will not apply the command twice.
        body=issue_body(by_id[key],next_state,config)
        api.request('PATCH',api.path(f"/issues/{issues[key]['number']}"),{'body':body,'state':'closed' if next_state['status']=='done' else 'open',
            'assignees':[next_state['owner']] if next_state.get('owner') else [],
            'labels':['task',f"role:{by_id[key]['role']}",f"status:{next_state['status']}"]})
        issues[key]['body']=body
        api.request('POST',api.path(f"/issues/{issues[key]['number']}/comments"),{'body':f'**任务同步回执** · @{actor}\n\n{message}\n\n<!-- team-receipt:{comment_id} -->'})
    # Reconcile configuration and label/close changes even when no new command arrived.
    for key,issue in issues.items():
        state=states[key];body=issue_body(by_id[key],state,config)
        labels={item['name'] for item in issue.get('labels',[])}
        expected={'task',f"role:{by_id[key]['role']}",f"status:{state['status']}"}
        if body!=issue.get('body') or labels!=expected or issue['state']!=('closed' if state['status']=='done' else 'open'):
            api.request('PATCH',api.path(f"/issues/{issue['number']}"),{'body':body,'state':'closed' if state['status']=='done' else 'open',
                'labels':sorted(expected),'assignees':[state['owner']] if state.get('owner') else []})
    snapshot={'schema_version':1,'generated_at':now(),'repository':config['repository'],'timezone':config['timezone'],
        'members':config['members'],'service':config['service'],'aws_state':'Not polled; evidence is time/environment-specific.',
        'tasks':[{**task,**states[task['id']], 'issue_number':issues[task['id']]['number'],
            'issue_url':issues[task['id']]['html_url'],
            'waiting_for':unmet_dependencies(task,states,config)} for task in tasks]}
    (root/'data').mkdir(exist_ok=True)
    (root/'data/snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    render_dashboard(snapshot,root)
    print(json.dumps({'tasks':len(tasks),'new_commands':len(events),'snapshot':snapshot['generated_at']},ensure_ascii=False))

def render_dashboard(snapshot, root=ROOT):
    tasks=snapshot['tasks']; active=[t for t in tasks if t['status']!='skipped'];done=[t for t in active if t['status']=='done']
    try:
        local=datetime.fromisoformat(snapshot['generated_at']).astimezone(ZoneInfo('Australia/Sydney')).strftime('%Y-%m-%d %H:%M %Z')
    except ZoneInfoNotFoundError:
        raise RuntimeError('当前 Python 缺少时区数据；Windows 环境先由 AI 安装 tzdata，再重新同步。') from None
    lines=['# 三人项目进度看板','',f"最后同步：**{local}** · [在线任务入口](LIVE_BOARD.md) · [系统运行方式](docs/system-status.md)",'',
        f'已完成并复核 **{len(done)} / {len(active)}** 项；等检查 **{sum(t["status"]=="review" for t in tasks)}** 项；被卡住 **{sum(t["status"]=="blocked" for t in tasks)}** 项。',
        '', '**当前同步：每次聊天由 AI 运行同步助手；后台 Actions 暂停。** [系统状态](docs/system-status.md)。', '', '**这是任务同步快照，不是 AWS 实时监控。** 点击任务读取最新正文和评论；没有同步回执的认领/提交仍在处理中。所有项目任务未完成前，不把协作系统搭建计作云服务完成。',
        '', '## 每个人现在可以做什么','', '| 角色 / 成员 | 当前工作 | 前置条件满足的下一项 |','| --- | --- | --- |']
    for role in 'ABC':
        current=[t for t in tasks if t['role']==role and t['status'] in {'in_progress','blocked','review'}]
        ready=[t for t in tasks if t['role']==role and t['status']=='todo' and not t['waiting_for']]
        links=lambda items:'；'.join(f"[{t['id']} {t['title']}]({t['issue_url']})" for t in items) or '无'
        lines.append(f"| {role} / {snapshot['members'].get(role) or '待加入'} | {links(current)} | {links(ready)} |")
    for status in ['in_progress','blocked','review','todo','done','skipped']:
        group=[t for t in tasks if t['status']==status]
        lines += ['',f'## {STATUS[status]} · {len(group)}','', '| 任务 | 负责人 / 角色 | 内部目标日期 | 等待什么 / 最近记录 |','| --- | --- | --- | --- |']
        for task in group:
            note=('先等 '+','.join(task['waiting_for'])+'；' if task['waiting_for'] else '')+task['last_note']
            lines.append(f"| [{task['id']} {text_cell(task['title'])}]({task['issue_url']}) | {task.get('owner') or '未认领'} / {task['role']} | {task['due']} | {text_cell(note)} |")
        if not group: lines.append('| — | — | — | — |')
    lines += ['', '## 建议时间安排','', '```mermaid','gantt','    title 三人共同推进（内部建议）','    dateFormat YYYY-MM-DD',
        '    section A 网络部署','    权限与网络 :2026-11-01, 3d','    双实例与入口 :2026-11-04, 3d','    安全与故障配合 :2026-11-07, 4d','    架构图与复核 :2026-11-11, 6d',
        '    section B 应用数据','    约定与数据库 :2026-11-01, 3d','    共享数据验证 :2026-11-04, 3d','    修复与部署步骤 :2026-11-07, 4d','    报告与复核 :2026-11-11, 6d',
        '    section C 测试证据','    测试与成本假设 :2026-11-01, 3d','    分流与监控 :2026-11-04, 3d','    告警与故障测试 :2026-11-07, 4d','    成本视频与复核 :2026-11-11, 6d','```','',
        '日期是计划，任务卡显示实际进度；成员加入后按空闲时间调整。课程正式截止为 2026-11-17 16:00 悉尼时间。',
        '', '## 日常命令','', '`/team claim B` → 认领；`/team progress 实际进度` → 记录；`/team block 问题` → 遇阻；`/team submit deliveries/Txx/文件.json` → 等检查；另一人 `/team approve 检查说明` → 完成。',
        '', '[AI 开场语](prompts/START.md) · [资料索引](sources/INDEX.md) · [协议](docs/team-protocol.md) · [操作手册](docs/execution-guide.md)']
    (root/'DASHBOARD.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['bootstrap','sync','validate'])
    args=parser.parse_args();config=load_config();tasks=load_tasks()
    if args.command=='validate':
        validate_plan(tasks,config);print('Plan and role configuration valid.');return
    api=GitHub(config)
    # Hosted and chat-driven execution use the same atomic repository lock.
    from team import repository_lock
    with repository_lock(api,'github-actions'):
        seed=bootstrap(api,tasks,config) if args.command=='bootstrap' else None
        synchronize(api,tasks,config,issue_seed=seed)

def validate_plan(tasks,config):
    ids={t['id'] for t in tasks}
    if len(ids)!=len(tasks):raise ValueError('Duplicate task IDs')
    people=[v.casefold() for v in config['members'].values() if v]
    if len(set(people))!=len(people):raise ValueError('Each person must bind only one role')
    visiting=set();visited=set();by_id={t['id']:t for t in tasks}
    def visit(key):
        if key in visiting:raise ValueError('Cyclic task dependencies')
        if key in visited:return
        visiting.add(key)
        for dep in required_dependencies(by_id[key],config):
            if dep not in ids:raise ValueError('Unknown dependency '+dep)
            visit(dep)
        visiting.remove(key);visited.add(key)
    for task in tasks:
        if task['role'] not in config['members']:raise ValueError('Unknown role')
        if task['start']>task['due']:raise ValueError('Invalid dates')
        visit(task['id'])

if __name__=='__main__':main()
