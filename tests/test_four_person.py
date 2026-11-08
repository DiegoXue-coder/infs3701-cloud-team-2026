"""Four-role authorization and English workflow, with isolated fake GitHub only."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
import team
import team_sync as core
from test_enrollment import ConfigAPI
from test_receipts import ReceiptAPI
from test_team_sync import Files


class FourPersonRules(unittest.TestCase):
    def setUp(self):
        self.config=core.load_config()
        self.tasks=core.load_tasks()
        self.task=next(t for t in self.tasks if t['id']=='T25')

    def test_only_reserved_d_identity_can_claim_and_not_other_roles(self):
        state=core.initial_state(self.task,self.config)
        states={t['id']:core.initial_state(t,self.config) for t in self.tasks}
        after,_=core.apply_command(Files(),self.task,state,states,self.config,'wyend12','claim','D','2026-11-08T00:00:00Z')
        self.assertEqual(after['owner'],'wyend12')
        self.assertEqual(after['owner_role'],'D')
        with self.assertRaises(ValueError):
            core.apply_command(Files(),self.task,state,states,self.config,'Marina057','claim','D','2026-11-08T00:00:00Z')
        other=next(t for t in self.tasks if t['id']=='T07')
        with self.assertRaises(ValueError):
            core.apply_command(Files(),other,states['T07'],states,self.config,'wyend12','claim','B','2026-11-08T00:00:00Z')

    def test_reserved_join_is_idempotent_and_cannot_overwrite_people(self):
        people={'A':'alice','B':'bob','C':'carol','D':'wyend12'}
        api=ConfigAPI(people)
        team.enroll(api,'WYEND12','D')
        self.assertFalse(api.writes)
        self.assertEqual(api.config['members'],people)
        with self.assertRaises(ValueError): team.enroll(api,'someone-else','D')
        with self.assertRaises(ValueError): team.enroll(api,'wyend12','B')
        with self.assertRaises(ValueError): team.enroll(ConfigAPI(),'new-user','D')

    def test_d_prepares_now_but_cannot_bypass_final_report_dependencies(self):
        task=next(t for t in self.tasks if t['id']=='T19')
        states={t['id']:core.initial_state(t,self.config) for t in self.tasks}
        state,_=core.apply_command(Files(),task,states['T19'],states,self.config,'wyend12','claim','D','2026-11-08T00:00:00Z')
        self.assertEqual(state['status'],'in_progress')
        with self.assertRaises(ValueError):
            core.apply_command(Files(),task,state,states,self.config,'wyend12','submit','deliveries/T19/result.json','2026-11-08T00:00:00Z')
        with self.assertRaises(ValueError):
            core.apply_command(Files(),task,state,states,self.config,'wyend12','approve','I checked my own work','2026-11-08T00:00:00Z')

    def test_english_claim_receipt_dashboard_and_retry_preserve_identity(self):
        api=ReceiptAPI()
        api.config=copy.deepcopy(self.config)
        api.task=copy.deepcopy(self.task)
        state=core.initial_state(api.task,api.config)
        api.issue.update(title='[T25] '+api.task['title'],body=core.issue_body(api.task,state,api.config),labels=[{'name':n} for n in ['task','role:D','status:todo']])
        api.rows=[{'id':10,'body':'/team claim D','user':{'login':'wyend12'},'created_at':'2026-11-08T00:00:00Z','html_url':'https://github.com/test/repo/issues/1#issuecomment-10'}]
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            core.synchronize(api,[api.task],api.config,root=root)
            core.synchronize(api,[api.task],api.config,root=root)
            final=core.parse_state(api.issue['body'])
            self.assertEqual(final['owner'],'wyend12')
            self.assertEqual(final['processed_comments'],[10])
            self.assertIn('## Start now',api.issue['body'])
            receipts=[r for r in api.rows if core.parse_receipt(r['body'])]
            self.assertEqual(len(receipts),1)
            self.assertIn('English receipt summary',receipts[0]['body'])
            self.assertIn('In progress',receipts[0]['body'])
            self.assertIn('任务同步回执',receipts[0]['body'])
            self.assertEqual(core.parse_receipt(receipts[0]['body'])['actor'],'wyend12')
            self.assertIn('D / wyend12',(root/'DASHBOARD.md').read_text(encoding='utf-8'))

    def test_existing_roles_and_authorship_inputs_preserved(self):
        self.assertEqual({r:self.config['members'][r] for r in 'ABC'}, {'A':'DiegoXue-coder','B':'Alex4325Li','C':'Marina057'})
        self.assertEqual({t['id'] for t in self.tasks if t['role']=='D'},{'T19','T20','T25'})
        core.validate_plan(self.tasks,self.config)
        for path in ['docs/b-design-report-draft.md','docs/c-t20-video-script-2026-11-07.md','deliveries/T08/2026-11-04-Marina057.json']:
            self.assertTrue((core.ROOT/path).is_file(),path)

    def test_english_partial_report_uses_real_delivery_validation_and_receipt(self):
        api=Files()
        api.manifest.update(task_id='T25',actor='wyend12',verification_result='partial',summary='Reviewed original brief; objective draft and evidence matrix started.')
        state=core.initial_state(self.task,self.config)
        states={'T25':state}
        claimed,_=core.apply_command(api,self.task,state,states,self.config,'wyend12','claim','D','2026-11-08T00:00:00Z')
        reported,note=core.apply_command(api,self.task,claimed,states,self.config,'wyend12','report','deliveries/T25/first.json','2026-11-08T00:01:00Z')
        self.assertEqual(reported['status'],'in_progress')
        self.assertEqual(reported['last_report']['submitted_by'],'wyend12')
        self.assertEqual(reported['last_report']['verification_result'],'partial')
        comment={'id':222,'user':{'login':'wyend12'},'created_at':'2026-11-08T00:01:00Z','html_url':'https://github.com/test/repo/issues/25#issuecomment-222'}
        receipt=core.make_receipt('T25',comment,'report',True,claimed,reported,note)
        body=core.receipt_body(receipt,self.config)
        self.assertIn('Actual result: **partial**',body)
        self.assertIn(api.manifest['summary'],body)
        self.assertEqual(core.parse_receipt(body)['actor'],'wyend12')

    def test_reallocation_cannot_overwrite_an_existing_other_role_claim(self):
        api=ReceiptAPI()
        api.config=copy.deepcopy(self.config)
        api.task=next(t for t in self.tasks if t['id']=='T19')
        state=core.initial_state(api.task,api.config)
        state.update(owner='Alex4325Li',owner_role='B',status='in_progress')
        api.issue['body']=core.issue_body(api.task,state,api.config)
        api.rows=[]
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(RuntimeError,'existing claim'):
                core.synchronize(api,[api.task],api.config,root=Path(folder))
        self.assertEqual(core.parse_state(api.issue['body'])['owner'],'Alex4325Li')

    def test_legacy_administrative_role_migration_keeps_historical_owner_role(self):
        api=ReceiptAPI()
        state=core.initial_state(api.task,api.config)
        state.update(owner='alice',owner_role='B',status='in_progress',last_note='Historical role migration, preserved')
        api.issue['body']=core.issue_body(api.task,state,api.config)
        api.rows=[]
        with tempfile.TemporaryDirectory() as folder:
            core.synchronize(api,[api.task],api.config,root=Path(folder))
        final=core.parse_state(api.issue['body'])
        self.assertEqual(final['owner'],'alice')
        self.assertEqual(final['owner_role'],'B')
        self.assertEqual(final['last_note'],state['last_note'])


if __name__=='__main__': unittest.main()
