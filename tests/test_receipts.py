from pathlib import Path
import copy
import json
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import team_sync as core
from capture_run import redact

class ReceiptAPI:
    def __init__(self,fail_once=False):
        self.config={'repository':'test/repo','members':{'A':'alice','B':'bob','C':'carol'},'maintainers':['alice'],
            'enhancements_enabled':False,'timezone':'Australia/Sydney','service':{'status':'pending'}}
        self.task={'id':'T01','title':'Prepare actual result','role':'A','reviewer_role':'B','optional':False,
            'depends_on':[],'start_after':[],'early_steps':['prepare'],'steps':['execute'],
            'acceptance':['checked'],'start':'2026-10-31','due':'2026-11-01'}
        state=core.initial_state(self.task,self.config)
        self.issue={'number':1,'html_url':'https://github.com/test/repo/issues/1','state':'open',
            'body':core.issue_body(self.task,state,self.config),'labels':[{'name':name} for name in ['task','role:A','status:todo']]}
        self.rows=[{'id':10,'body':'/team claim A','user':{'login':'alice'},'created_at':'2026-10-31T10:00:00Z','html_url':'https://github.com/test/repo/issues/1#issuecomment-10'}]
        self.fail_once=fail_once
    def path(self,path):return path
    def issue_list(self):return [copy.deepcopy(self.issue)]
    def comments(self,number):return copy.deepcopy(self.rows)
    def permission(self,user):return 'admin'
    def request(self,method,path,data=None):
        if method=='GET' and path=='/issues/1':return copy.deepcopy(self.issue)
        if method=='PATCH' and path=='/issues/1':
            self.issue.update(data)
            self.issue['labels']=[{'name':name} for name in data['labels']]
            return copy.deepcopy(self.issue)
        if method=='POST' and path=='/issues/1/comments':
            if self.fail_once:self.fail_once=False;raise RuntimeError('simulated acknowledgment interruption')
            comment={'id':len(self.rows)+100,'body':data['body'],'user':{'login':'alice'},'created_at':'2026-10-31T10:01:00Z',
                'html_url':f'https://github.com/test/repo/issues/1#issuecomment-{len(self.rows)+100}'}
            self.rows.append(comment);return copy.deepcopy(comment)
        raise AssertionError((method,path))

class ReceiptRules(unittest.TestCase):
    def test_interrupt_after_state_write_recovers_exactly_one_receipt(self):
        api=ReceiptAPI(fail_once=True)
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            with self.assertRaises(RuntimeError):core.synchronize(api,[api.task],api.config,root=root)
            state=core.parse_state(api.issue['body'])
            self.assertEqual(state['owner'],'alice')
            self.assertIn('pending_receipt',state)
            core.synchronize(api,[api.task],api.config,root=root)
            core.synchronize(api,[api.task],api.config,root=root)
            state=core.parse_state(api.issue['body'])
            self.assertNotIn('pending_receipt',state)
            self.assertEqual(state['processed_comments'],[10])
            self.assertEqual(sum(core.parse_receipt(row['body']) is not None for row in api.rows),1)
            archive=json.loads((root/'data/receipts.json').read_text(encoding='utf-8'))
            self.assertEqual(len(archive['receipts']),1)
            self.assertEqual(archive['receipts'][0]['receipt_id'],'R-T01-10')
    def test_old_receipts_are_kept_without_inventing_previous_state(self):
        rows=[{'id':1,'body':'/team status','user':{'login':'alice'},'created_at':'2026-10-31T00:00:00Z'},
            {'id':2,'body':'old receipt\n<!-- team-receipt:1 -->','created_at':'2026-10-31T00:00:01Z','html_url':'ack'}]
        receipt=core.collect_receipts('T01',rows)[0]
        self.assertTrue(receipt['legacy'])
        self.assertIsNone(receipt['status_after'])
    def test_sensitive_assignment_line_is_redacted(self):
        self.assertNotIn('example-secret',redact('AWS_SECRET_ACCESS_KEY=example-secret'))

if __name__=='__main__':unittest.main()
