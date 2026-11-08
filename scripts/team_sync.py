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
RECEIPT_RE = re.compile(r'<!-- team-receipt-data\s*\n(.*?)\n-->', re.S)
STATUS = {'todo':'未开始','in_progress':'进行中','blocked':'被卡住','review':'等检查','done':'已完成','skipped':'未启用（可选）'}
STATUS_EN = {'todo':'Not started','in_progress':'In progress','blocked':'Blocked','review':'Awaiting review','done':'Done','skipped':'Optional / disabled'}
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

def parse_receipt(body):
    match=RECEIPT_RE.search(body or '')
    return json.loads(match.group(1)) if match else None

def required_dependencies(task, config):
    result = list(task['depends_on'])
    if config['enhancements_enabled'] and task['id'] in {'T17','T18','T19','T20'}:
        result.append('T16')
    return result

def unmet_dependencies(task, states, config):
    return [key for key in required_dependencies(task,config) if states.get(key,{}).get('status') != 'done']

def start_dependencies(task):
    # Old task definitions retain their original behavior until explicitly migrated.
    return list(task.get('start_after',task['depends_on']))

def unmet_start_dependencies(task, states):
    return [key for key in start_dependencies(task) if states.get(key,{}).get('status') != 'done']

def text_cell(value):
    return str(value or '—').replace('|','／').replace('\n',' ')[:250]

def issue_body(task, state, config):
    if task.get('language')=='en':
        return english_issue_body(task,state,config)
    lines=[f"<!-- team-task:{task['id']} -->",f"# {task['id']} · {task['title']}",'',
        f"主责角色：**{task['role']}**；建议检查角色：{task['reviewer_role']}（必须不同 GitHub 用户）",
        f"内部计划：{task['start']} → {task['due']}（悉尼日期；不是课程新增截止）",
        '开始准备前需完成：'+('、'.join(start_dependencies(task)) or '**无，可以独立开始**'),
        '提交完整成果前需完成：'+('、'.join(required_dependencies(task,config)) or '无'),'',
        '## 现在就能做（不等别人）','']
    lines += [f'- {step}' for step in task.get('early_steps',task['steps'])]
    lines += ['', '## 联合实施与最终验证','']
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
        f"部分成果或失败测试也应上报：`/team report deliveries/{task['id']}/日期-用户名.json`，不会因此标完成。",
        '', f"[完整规则](https://github.com/{config['repository']}/blob/main/docs/team-protocol.md) · [操作手册](https://github.com/{config['repository']}/blob/main/docs/execution-guide.md)",
        '', '## 同步状态（系统维护）','',
        f"- 状态：**{STATUS[state['status']]}**",
        '- 负责人：'+text_cell(state.get('owner')),
        '- 最近记录：'+text_cell(state.get('last_note')),
        '- 时间：'+text_cell(state.get('last_update')),
        '- 最近回执：'+text_cell((state.get('last_receipt') or {}).get('receipt_id'))]
    latest=state.get('submission') or state.get('last_report')
    if latest:
        url=f"https://github.com/{config['repository']}/blob/{latest['commit']}/"
        lines += ['- 实际上报结果：'+text_cell(latest.get('verification_result')),
            f"- [交付记录]({url+urllib.parse.quote(latest['path'],safe='/')}) · [执行记录]({url+urllib.parse.quote(latest['run_log'],safe='/')})"]
    lines += ['', '<!-- team-state',json.dumps(state,ensure_ascii=False,separators=(',',':')),'-->']
    return '\n'.join(lines)+'\n'


def english_issue_body(task,state,config):
    """English cards share exactly the same state/receipts and completion gates."""
    lines=[f"<!-- team-task:{task['id']} -->",f"# {task['id']} · {task['title']}",'',
        f"Responsible role: **{task['role']}**. Suggested reviewer: {task['reviewer_role']} (a different GitHub account).",
        f"Suggested internal dates: {task['start']} → {task['due']} (Sydney; not a new course deadline).",
        'To begin preparation: '+(', '.join(start_dependencies(task)) or '**No dependencies; start independently.**'),
        'Before final submission: '+(', '.join(required_dependencies(task,config)) or 'None'),'',
        '## Start now','']
    lines += ['- '+step for step in task.get('early_steps',task['steps'])]
    lines += ['', '## Work and final validation','']+[f'{i}. {step}' for i,step in enumerate(task['steps'],1)]
    lines += ['', '## Acceptance criteria','']+['- '+item for item in task['acceptance']]
    lines += ['', '## Updates and evidence','',
        f"Claim using `/team claim {task['role']}` through `scripts/team.py command {task['id']} --body-file <file>`. Authenticate as yourself and wait for an accepted receipt.",
        f"Partial work: `/team report deliveries/{task['id']}/YYYY-MM-DD-username.json`. Full delivery: `/team submit deliveries/{task['id']}/YYYY-MM-DD-username.json`.",
        'Use delivery schema version 2 with a genuine review/execution log. A document-only review is valid when its actual sources, checks and limitations are recorded. Never invent AWS tests.',
        'A different member must inspect the result before `/team approve <what was checked>`; never approve your own delivery.',
        'Use `/team progress <actual progress>` or `/team block <specific obstacle>`. Reports and partial work do not mark a task complete.',
        f"[English guide](https://github.com/{config['repository']}/blob/main/docs/member-D.md) · [Four-person handoffs](https://github.com/{config['repository']}/blob/main/docs/four-person-plan.md)",
        '', '## Synchronized state','',
        f"- Status: **{STATUS_EN[state['status']]}** (`{state['status']}`)",
        '- Owner: '+text_cell(state.get('owner')),
        '- Latest note (original language; your AI may translate): '+text_cell(state.get('last_note')),
        '- Updated: '+text_cell(state.get('last_update')),
        '- Receipt: '+text_cell((state.get('last_receipt') or {}).get('receipt_id'))]
    latest=state.get('submission') or state.get('last_report')
    if latest:
        url=f"https://github.com/{config['repository']}/blob/{latest['commit']}/"
        lines += ['- Actual verification result: '+text_cell(latest.get('verification_result')),
            f"- [Delivery]({url+urllib.parse.quote(latest['path'],safe='/')}) · [Run/review log]({url+urllib.parse.quote(latest['run_log'],safe='/')})"]
    lines += ['', '<!-- team-state',json.dumps(state,ensure_ascii=False,separators=(',',':')),'-->']
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
    if delivery.get('schema_version')!=2:
        raise ValueError('请使用 templates/delivery.json 的第 2 版格式，包含实际执行记录和测试结果。')
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
    if not isinstance(tests,list) or not 1<=len(tests)<=20 or not all(isinstance(t,dict) and all(isinstance(t.get(k),str) and t[k].strip() for k in ['action','expected','actual']) for t in tests):
        raise ValueError('请记录实际测试/核对的步骤、期望及实际结果。')
    evidence=delivery.get('evidence')
    if not isinstance(evidence,list) or not 1<=len(evidence)<=20 or not all(isinstance(p,str) and len(p)<=300 for p in evidence):
        raise ValueError('至少引用一个真实证据文件。')
    verification=delivery.get('verification_result')
    if verification not in {'pass','fail','partial'}:
        raise ValueError('verification_result 必须是 pass、fail 或 partial；不能把部分完成写成通过。')
    run_log=delivery.get('run_log')
    if not isinstance(run_log,str) or run_log not in evidence:
        raise ValueError('必须提供实际执行/核对记录 run_log，且它应包含在 evidence 列表中。')
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
        'summary':delivery['summary'][:1000],'tested_at':delivery['tested_at'],'submitted_by':actor,
        'environment':delivery['environment'][:1000],'verification_result':verification,'run_log':run_log,
        'test_count':len(tests),'test_summary':[{key:test[key][:200] for key in ['action','expected','actual']} for test in tests[:5]]}

def validate_review(api, submission):
    if submission.get('verification_result')!='pass':
        raise ValueError('测试结果仍为失败或部分完成，不能批准完成；请修复后重新提交真实通过的结果。')
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
        start_waiting=unmet_start_dependencies(task,states)
        return result,f"{task['id']}：{STATUS[state['status']]}；负责人 {state.get('owner') or '未认领'}；开始准备需等 {', '.join(start_waiting) or '无'}；最终完成需等 {', '.join(waiting) or '无'}。"
    if command=='claim':
        role=args.strip().upper()
        if role!=task['role'] or (not maintainer and str(assigned or '').casefold()!=actor.casefold()):
            raise ValueError('角色与任务不匹配或尚未登记。请先更新成员配置；管理员可记录接替。')
        if state['status']=='skipped': raise ValueError('可选增强尚未启用；需小组决定并更新配置。')
        if state['status']=='done': raise ValueError('任务已完成；如需返工先由他人提出 changes。')
        if state.get('owner') and not is_owner: raise ValueError('任务已由其他成员认领，请协调交接，不能覆盖。')
        waiting=unmet_start_dependencies(task,states)
        if waiting: raise ValueError('开始条件还未完成：'+', '.join(waiting))
        if is_owner: return result,'已由你认领，保留当前状态。'
        result.update(status='in_progress',owner=actor,owner_role=role,last_note='已认领'+('（管理员接替未绑定角色）' if maintainer and str(assigned or '').casefold()!=actor.casefold() else ''))
    elif command in {'progress','block','resume','submit','report'}:
        if not is_owner: raise ValueError('只有实际认领人可以更新或提交此任务。')
        if state['status'] in {'done','skipped'}: raise ValueError('该状态不能直接更新，请先安排返工或启用任务。')
        if command in {'progress','block'}:
            if not args.strip(): raise ValueError('请补充实际进度或阻碍原因。')
            result['last_note']=args.strip()[:2000]
            if command=='block': result['status']='blocked'
        elif command=='resume':
            waiting=unmet_start_dependencies(task,states)
            if waiting: raise ValueError('开始条件仍未满足：'+', '.join(waiting))
            result.update(status='in_progress',last_note=args.strip() or '恢复工作')
        else:
            paths=shlex.split(args)
            if len(paths)!=1: raise ValueError('report/submit 后只填写一个交付 JSON 路径。')
            waiting=unmet_dependencies(task,states,config) if command=='submit' else []
            if waiting: raise ValueError('前置条件尚未完成：'+', '.join(waiting))
            submission=validate_delivery(api,task,actor,paths[0],timestamp)
            if command=='report':
                result.update(status='blocked' if state['status']=='blocked' else 'in_progress',
                    last_report=submission,submission=None,reviewer=None,
                    last_note=f"实际上报（{submission['verification_result']}，尚未完成）："+submission['summary'])
            else:
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
        raise ValueError('未知命令；支持 claim / progress / block / resume / report / submit / approve / changes / status。')
    result['last_update']=timestamp
    return result,f"{task['id']} 已更新为「{STATUS[result['status']]}」。{result['last_note']}"

def make_receipt(task_id, comment, command, accepted, before, after, message):
    submission=after.get('submission') if command in {'submit','approve','changes'} else after.get('last_report') if command=='report' else None
    reference=None
    if submission:
        reference={key:submission.get(key) for key in ['path','commit','manifest_sha','run_log','verification_result','tested_at','test_count']}
        reference['evidence_count']=len(submission['evidence_shas'])
        reference['evidence_preview']=list(submission['evidence_shas'])[:3]
    return {'schema_version':1,'receipt_id':f"R-{task_id}-{comment['id']}",'task_id':task_id,
        'request_comment_id':comment['id'],'actor':comment['user']['login'],'command':command,
        'requested_at':comment['created_at'],'processed_at':now(),
        'outcome':'accepted' if accepted else 'rejected','status_before':before['status'],'status_after':after['status'],
        'summary':message[:2000],'request_url':comment.get('html_url'),'submission':reference}

def receipt_body(receipt,config):
    lines=[f"**任务同步回执 `{receipt['receipt_id']}`**",'',
        f"任务：{receipt['task_id']} · 操作者：@{receipt['actor']} · 操作：{receipt['command']}",
        f"处理：{receipt['outcome']} · 状态：{STATUS[receipt['status_before']]} → {STATUS[receipt['status_after']]}",
        '时间：'+receipt['processed_at'],'',receipt['summary']]
    reference=receipt.get('submission')
    if reference:
        url=f"https://github.com/{config['repository']}/blob/{reference['commit']}/"
        lines += ['',f"结果：**{reference['verification_result']}** · 测试/核对 {reference['test_count']} 项 · 证据 {reference['evidence_count']} 份",
            f"[完整交付记录]({url+urllib.parse.quote(reference['path'],safe='/')}) · [实际执行记录]({url+urllib.parse.quote(reference['run_log'],safe='/')})",
            '对应版本：`'+reference['commit']+'`']
        lines += [f"- [证据：{path}]({url+urllib.parse.quote(path,safe='/')})" for path in reference['evidence_preview']]
    lines += ['', '### English receipt summary',
        f"Task: {receipt['task_id']} · Actor: @{receipt['actor']} · Command: {receipt['command']}",
        f"Outcome: **{receipt['outcome']}** · {STATUS_EN[receipt['status_before']]} → {STATUS_EN[receipt['status_after']]}",
        'Processed UTC: '+receipt['processed_at'],
        'The original-language note above is preserved. Your own AI may translate it; task IDs, status, evidence and verification results must not change.']
    if reference:
        lines += [f"Actual result: **{reference['verification_result']}**; checks: {reference['test_count']}; evidence files: {reference['evidence_count']}.",
            f"[Delivery]({url+urllib.parse.quote(reference['path'],safe='/')}) · [Run/review log]({url+urllib.parse.quote(reference['run_log'],safe='/')}) · Commit: `{reference['commit']}`"]
    lines += ['', '回执确认本次上报和文件版本；它不是 AWS 实时健康证明。 / This receipt confirms the report and file version, not live AWS health.', '',
        f"<!-- team-receipt:{receipt['request_comment_id']} -->", '<!-- team-receipt-data',
        json.dumps(receipt,ensure_ascii=False,separators=(',',':')), '-->']
    return '\n'.join(lines)

def flush_receipt(api,issue,state,comments,config):
    """Durable outbox: repair an interrupted acknowledgment without applying twice."""
    pending=state.get('pending_receipt')
    if not pending:return
    marker=f"<!-- team-receipt:{pending['request_comment_id']} -->"
    existing=next((comment for comment in comments if marker in (comment.get('body') or '')),None)
    if existing is None:
        existing=api.request('POST',api.path(f"/issues/{issue['number']}/comments"),{'body':receipt_body(pending,config)})
        comments.append(existing)
    url=existing.get('html_url') or f"{issue['html_url']}#issuecomment-{existing['id']}"
    state['last_receipt']={key:pending[key] for key in ['receipt_id','command','outcome','status_after','processed_at']}
    state['last_receipt']['url']=url
    state.pop('pending_receipt',None)

def collect_receipts(task_id,comments):
    requests={comment['id']:comment for comment in comments}
    result=[]
    for comment in comments:
        body=comment.get('body') or ''
        record=parse_receipt(body)
        if record:
            record['receipt_url']=comment.get('html_url')
            result.append(record)
        else:
            match=re.search(r'<!-- team-receipt:(\d+) -->',body)
            if not match:continue
            original=requests.get(int(match.group(1)),{})
            result.append({'receipt_id':f'R-{task_id}-{match.group(1)}','task_id':task_id,'legacy':True,
                'actor':original.get('user',{}).get('login'),'command':(original.get('body') or '').split(maxsplit=2)[1] if len((original.get('body') or '').split(maxsplit=2))>1 else None,
                'processed_at':comment.get('created_at'),'outcome':'legacy','status_before':None,'status_after':None,
                'summary':'历史回执保留；不补造当时未保存的结构化状态。','receipt_url':comment.get('html_url'),'submission':None})
    return result

def bootstrap(api, tasks, config):
    repository=api.request('GET',api.path(''))
    if not repository.get('private'): raise RuntimeError('只允许在 private 仓库初始化课程资料系统。')
    labels={label['name'] for label in api.pages(api.path('/labels'))}
    definitions={'task':('0366d6','小组任务'),**{f'role:{role}':('7057ff',f'角色 / Role {role}') for role in config['members']},
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
    for key,state in states.items():
        if state.get('owner') and state.get('owner_role') not in (None,by_id[key]['role']):
            raise RuntimeError('Role change would conflict with an existing claim on '+key+'; coordinate the handoff instead of overwriting ownership.')
    events=[];comment_cache={}
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
        comment_cache[key]=comments
        flush_receipt(api,issue,state,comments,config)
        for comment in comments:
            first=(comment.get('body') or '').strip().split('\n',1)[0]
            if first.startswith('/team ') and comment['id'] not in state.get('processed_comments',[]):
                events.append((comment['id'],key,comment,first))
    permissions={}
    for comment_id,key,comment,line in sorted(events):
        state=states[key]; actor=comment['user']['login']
        command='invalid';accepted=True
        try:
            if actor not in permissions: permissions[actor]=api.permission(actor)
            if permissions[actor] not in {'write','maintain','admin'}:
                raise ValueError('只有有写权限的小组成员可以操作任务。')
            parts=line.split(maxsplit=2)
            if len(parts)<2: raise ValueError('缺少命令。')
            command=parts[1].lower();args=parts[2] if len(parts)>2 else ''
            next_state,message=apply_command(api,by_id[key],state,states,config,actor,command,args,comment['created_at'])
        except (ValueError,KeyError,TypeError,json.JSONDecodeError,RuntimeError) as error:
            accepted=False;next_state=json.loads(json.dumps(state));message='未更新：'+str(error)
        next_state.setdefault('processed_comments',[]).append(comment_id)
        next_state['pending_receipt']=make_receipt(key,comment,command,accepted,state,next_state,message)
        states[key]=next_state
        # Persist before acknowledgment; a retry will not apply the command twice.
        body=issue_body(by_id[key],next_state,config)
        api.request('PATCH',api.path(f"/issues/{issues[key]['number']}"),{'body':body,'state':'closed' if next_state['status']=='done' else 'open',
            'assignees':[next_state['owner']] if next_state.get('owner') else [],
            'labels':['task',f"role:{by_id[key]['role']}",f"status:{next_state['status']}"]})
        issues[key]['body']=body
        flush_receipt(api,issues[key],next_state,comment_cache[key],config)
    # Reconcile configuration and label/close changes even when no new command arrived.
    for key,issue in issues.items():
        state=states[key];body=issue_body(by_id[key],state,config)
        labels={item['name'] for item in issue.get('labels',[])}
        expected={'task',f"role:{by_id[key]['role']}",f"status:{state['status']}"}
        title=f"[{key}] {by_id[key]['title']}"
        if body!=issue.get('body') or labels!=expected or issue['state']!=('closed' if state['status']=='done' else 'open') or issue.get('title')!=title:
            api.request('PATCH',api.path(f"/issues/{issue['number']}"),{'title':title,'body':body,'state':'closed' if state['status']=='done' else 'open',
                'labels':sorted(expected),'assignees':[state['owner']] if state.get('owner') else []})
    receipts=sorted([receipt for key,comments in comment_cache.items() for receipt in collect_receipts(key,comments)],key=lambda receipt:receipt.get('processed_at') or '')
    snapshot={'schema_version':1,'generated_at':now(),'repository':config['repository'],'timezone':config['timezone'],
        'members':config['members'],'service':config['service'],'aws_state':'Not polled; evidence is time/environment-specific.',
        'recent_receipts':receipts[-10:],
        'tasks':[{**task,**states[task['id']], 'issue_number':issues[task['id']]['number'],
            'issue_url':issues[task['id']]['html_url'],
            'waiting_for':unmet_dependencies(task,states,config),
            'start_waiting_for':unmet_start_dependencies(task,states)} for task in tasks]}
    (root/'data').mkdir(exist_ok=True)
    (root/'data/snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (root/'data/receipts.json').write_text(json.dumps({'schema_version':1,'generated_at':snapshot['generated_at'],'receipts':receipts},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    render_dashboard(snapshot,root)
    print(json.dumps({'tasks':len(tasks),'new_commands':len(events),'snapshot':snapshot['generated_at']},ensure_ascii=False))

def render_dashboard(snapshot, root=ROOT):
    tasks=snapshot['tasks']; active=[t for t in tasks if t['status']!='skipped'];done=[t for t in active if t['status']=='done']
    try:
        local=datetime.fromisoformat(snapshot['generated_at']).astimezone(ZoneInfo('Australia/Sydney')).strftime('%Y-%m-%d %H:%M %Z')
    except ZoneInfoNotFoundError:
        raise RuntimeError('当前 Python 缺少时区数据；Windows 环境先由 AI 安装 tzdata，再重新同步。') from None
    lines=['# 项目进度看板 / Team dashboard','',f"最后同步：**{local}** · [在线任务入口](LIVE_BOARD.md) · [四人分工 / Four-person plan](docs/four-person-plan.md) · [English start](prompts/START-en.md) · [系统运行方式](docs/system-status.md)",'',
        f'已完成并复核 **{len(done)} / {len(active)}** 项；等检查 **{sum(t["status"]=="review" for t in tasks)}** 项；被卡住 **{sum(t["status"]=="blocked" for t in tasks)}** 项。',
        '', '**当前同步：每次聊天由 AI 运行同步助手；后台 Actions 暂停。** [系统状态](docs/system-status.md)。', '', '**这是任务同步快照，不是 AWS 实时监控。** 点击任务读取最新正文和评论；没有同步回执的认领/提交仍在处理中。所有项目任务未完成前，不把协作系统搭建计作云服务完成。',
        '', '**可以先独立准备，最后再联合验收。** 卡片区分开始条件和完成条件；不要等别人整张卡复核完才写代码、配置草稿或测试。',
        '', '## 每个人现在可以做什么','', '| 角色 / 成员 | 当前工作 | 推荐先独立开展（最多三项） |','| --- | --- | --- |']
    for role in snapshot['members']:
        current=[t for t in tasks if t['role']==role and t['status'] in {'in_progress','blocked','review'}]
        ready=[t for t in tasks if t['role']==role and t['status']=='todo' and not t.get('start_waiting_for',t['waiting_for'])][:3]
        links=lambda items:'；'.join(f"[{t['id']} {t['title']}]({t['issue_url']})" for t in items) or '无'
        lines.append(f"| {role} / {snapshot['members'].get(role) or '待加入'} | {links(current)} | {links(ready)} |")
    lines += ['', '## 最近上报与回执','',
        '[完整机器可读回执](data/receipts.json) · [上报方法](docs/reporting.md)','',
        '| 任务 / 操作 | 操作者 | 处理与状态 | 证据与回执 |','| --- | --- | --- | --- |']
    for receipt in reversed(snapshot.get('recent_receipts',[])):
        reference=receipt.get('submission');evidence='—'
        if reference:
            prefix=f"https://github.com/{snapshot['repository']}/blob/{reference['commit']}/"
            evidence=f"[{reference['verification_result']} · 执行记录]({prefix+urllib.parse.quote(reference['run_log'],safe='/')})"
        url=receipt.get('receipt_url');ack=f'[回执]({url})' if url else '历史回执'
        lines.append(f"| {receipt['task_id']} / {text_cell(receipt.get('command'))} | {text_cell(receipt.get('actor'))} | {receipt['outcome']} / {STATUS.get(receipt.get('status_after'),'历史记录')} | {evidence} · {ack} |")
    if not snapshot.get('recent_receipts'):lines.append('| 暂无上报 | — | — | — |')
    for status in ['in_progress','blocked','review','todo','done','skipped']:
        group=[t for t in tasks if t['status']==status]
        lines += ['',f'## {STATUS[status]} · {len(group)}','', '| 任务 | 负责人 / 角色 | 内部目标日期 | 等待什么 / 最近记录 |','| --- | --- | --- | --- |']
        for task in group:
            note=('完成前需 '+','.join(task['waiting_for'])+'；' if task['waiting_for'] else '')+task['last_note']
            lines.append(f"| [{task['id']} {text_cell(task['title'])}]({task['issue_url']}) | {task.get('owner') or '未认领'} / {task['role']} | {task['due']} | {text_cell(note)} |")
        if not group: lines.append('| — | — | — | — |')
    lines += ['', '## 建议时间安排','', '```mermaid','gantt','    title 四人共同推进（内部建议）','    dateFormat YYYY-MM-DD',
        '    section A 网络部署','    权限与网络 :2026-11-01, 3d','    双实例与入口 :2026-11-04, 3d','    安全与故障配合 :2026-11-07, 4d','    架构图与复核 :2026-11-11, 6d',
        '    section B 应用数据','    约定与数据库 :2026-11-01, 3d','    共享数据验证 :2026-11-04, 3d','    修复与部署步骤 :2026-11-07, 4d','    报告与复核 :2026-11-11, 6d',
        '    section C 测试证据','    测试与成本假设 :2026-11-01, 3d','    分流与监控 :2026-11-04, 3d','    告警与故障测试 :2026-11-07, 4d','    成本与复核 :2026-11-11, 6d',
        '    section D English report and presentation','    Objectives and evidence audit :2026-11-08, 2d','    Integrated draft :2026-11-10, 2d','    Report and video :2026-11-12, 2d','    Cross-check and freeze :2026-11-14, 3d','```','',
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
        for dep in set(required_dependencies(by_id[key],config)+start_dependencies(by_id[key])):
            if dep not in ids:raise ValueError('Unknown dependency '+dep)
            visit(dep)
        visiting.remove(key);visited.add(key)
    for task in tasks:
        if task['role'] not in config['members']:raise ValueError('Unknown role')
        if task['start']>task['due']:raise ValueError('Invalid dates')
        visit(task['id'])

if __name__=='__main__':main()
