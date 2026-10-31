import base64
import copy
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('team_sync',Path(__file__).resolve().parents[1]/'scripts/team_sync.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class Files:
    def __init__(self,manifest=None):
        self.manifest=manifest or {'task_id':'T01','actor':'alice','tested_at':datetime.now(timezone.utc).isoformat(),
            'environment':'repository; no AWS test','summary':'Documented actual team decision',
            'tests':[{'action':'read decision','expected':'fields present','actual':'verified'}],
            'evidence':['docs/decision-result.md'],'limitations':'No cloud test','next_step':'network','ai_use':'assisted, human checked'}
        self.changed=False
    def head(self):return 'commit1'
    def get_file(self,path,ref='main'):
        if path.startswith('deliveries/'):
            raw=json.dumps(self.manifest).encode()
            return {'type':'file','size':len(raw),'content':base64.b64encode(raw).decode(),'sha':'changed' if self.changed else 'manifest1'}
        if path=='docs/decision-result.md':return {'type':'file','size':100,'sha':'evidence1'}
        raise RuntimeError('GitHub HTTP 404: Not Found')

class Rules(unittest.TestCase):
    def setUp(self):
        self.config={'repository':'test/repo','members':{'A':'alice','B':'bob','C':'carol'},'maintainers':['admin'],'enhancements_enabled':False}
        self.task={'id':'T01','title':'team decision','role':'A','reviewer_role':'B','optional':False,'depends_on':[],
            'steps':['real decision'],'acceptance':['reviewed'],'start':'2026-10-31','due':'2026-10-31'}
        self.state=module.initial_state(self.task,self.config);self.states={'T01':self.state};self.api=Files()
    def command(self,actor,command,args='',state=None):
        source=state or self.state
        return module.apply_command(self.api,self.task,source,self.states,self.config,actor,command,args,'2026-10-31T12:00:00Z')[0]
    def claimed(self):return self.command('alice','claim','A')
    def submitted(self):return self.command('alice','submit','deliveries/T01/actual.json',self.claimed())
    def test_plan_has_no_cycle(self):module.validate_plan(module.load_tasks(),module.load_config())
    def test_role_cannot_be_impersonated(self):
        with self.assertRaises(ValueError):self.command('bob','claim','A')
    def test_no_claim_before_dependency(self):
        self.task['depends_on']=['T00'];self.states['T00']={'status':'todo'}
        with self.assertRaises(ValueError):self.claimed()
    def test_two_people_cannot_claim_same_task(self):
        with self.assertRaises(ValueError):self.command('admin','claim','A',self.claimed())
    def test_submit_requires_real_manifest(self):
        with self.assertRaises(ValueError):self.command('alice','submit','templates/delivery.json',self.claimed())
    def test_manifest_actor_must_match(self):
        self.api.manifest['actor']='bob'
        with self.assertRaises(ValueError):self.submitted()
    def test_evidence_must_exist(self):
        self.api.manifest['evidence']=['docs/missing.md']
        with self.assertRaises(RuntimeError):self.submitted()
    def test_progress_does_not_complete(self):
        state=self.command('alice','progress','actually tested read/write',self.claimed())
        self.assertEqual(state['status'],'in_progress')
    def test_submit_only_enters_review(self):self.assertEqual(self.submitted()['status'],'review')
    def test_cannot_approve_without_submission(self):
        with self.assertRaises(ValueError):self.command('bob','approve','checked',self.claimed())
    def test_cannot_approve_self(self):
        with self.assertRaises(ValueError):self.command('alice','approve','checked',self.submitted())
    def test_independent_review_completes(self):self.assertEqual(self.command('bob','approve','actually checked decision',self.submitted())['status'],'done')
    def test_changed_delivery_needs_resubmit(self):
        state=self.submitted();self.api.changed=True
        with self.assertRaises(ValueError):self.command('bob','approve','checked',state)
    def test_changes_reopens_done(self):
        done=self.command('bob','approve','checked',self.submitted())
        self.assertEqual(self.command('carol','changes','missing actual evidence',done)['status'],'in_progress')
    def test_block_resume(self):
        blocked=self.command('alice','block','permission unavailable',self.claimed())
        self.assertEqual(blocked['status'],'blocked')
        self.assertEqual(self.command('alice','resume','permission confirmed',blocked)['status'],'in_progress')
    def test_skipped_optional_is_not_completed(self):
        self.task['optional']=True;self.state=module.initial_state(self.task,self.config)
        self.assertEqual(self.state['status'],'skipped')
        with self.assertRaises(ValueError):self.claimed()
    def test_json_state_round_trip(self):
        body=module.issue_body(self.task,self.claimed(),self.config)
        self.assertEqual(module.parse_state(body)['owner'],'alice')
    def test_paths_reject_external_or_traversal(self):
        for path in ['../secret','https://example.com','/root/a','docs/../a','docs\\file']:
            with self.assertRaises(ValueError):module.validate_path(path)
    def test_status_does_not_claim(self):self.assertIsNone(self.command('bob','status')['owner'])
    def test_config_rejects_duplicate_identities(self):
        config=module.load_config();config['members']={'A':'same','B':'same','C':None}
        with self.assertRaises(ValueError):module.validate_plan(module.load_tasks(),config)
    def test_task_materials_are_linked_to_the_private_repo(self):
        self.task['materials']=[{'source_id':'S14','title':'lecture.pdf','path':'sources/original/course/week_05/lecture.pdf'}]
        body=module.issue_body(self.task,self.state,self.config)
        self.assertIn('https://github.com/test/repo/blob/main/sources/original/course/week_05/lecture.pdf',body)

if __name__=='__main__':unittest.main()
