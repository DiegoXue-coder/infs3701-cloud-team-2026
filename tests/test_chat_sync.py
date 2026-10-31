from pathlib import Path
import sys
import unittest
import base64
import json
import hashlib

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import team

class LockAPI:
    def __init__(self):self.lock=None;self.deleted=False
    def head(self):return 'main-head'
    def path(self,path):return path
    def request(self,method,path,data=None):
        if method=='GET' and path=='/git/commits/main-head':return {'tree':{'sha':'tree'}}
        if method=='POST' and path=='/git/commits':return {'sha':'lock-commit'}
        if method=='POST' and path=='/git/refs':
            if self.lock:raise RuntimeError('GitHub HTTP 422: Reference already exists')
            self.lock=data['sha'];return {}
        if method=='GET' and path=='/git/ref/heads/team-sync-lock':return {'object':{'sha':self.lock}}
        if method=='DELETE' and path=='/git/refs/heads/team-sync-lock':self.deleted=True;self.lock=None;return {}
        raise AssertionError((method,path))

class LockRules(unittest.TestCase):
    def test_lock_is_released_after_success(self):
        api=LockAPI()
        with team.repository_lock(api,'alice'):self.assertEqual(api.lock,'lock-commit')
        self.assertTrue(api.deleted)
    def test_lock_is_released_after_failure(self):
        api=LockAPI()
        with self.assertRaises(ValueError):
            with team.repository_lock(api,'alice'):raise ValueError('failed test')
        self.assertTrue(api.deleted)
    def test_other_sync_cannot_steal_lock(self):
        api=LockAPI();api.lock='other-user-lock'
        with self.assertRaises(RuntimeError):
            with team.repository_lock(api,'alice'):pass
        self.assertEqual(api.lock,'other-user-lock')
        self.assertFalse(api.deleted)
    def test_changed_lock_is_not_deleted(self):
        api=LockAPI()
        with team.repository_lock(api,'alice'):api.lock='different-lock'
        self.assertFalse(api.deleted)

class ReadOnlyDiagnosis(unittest.TestCase):
    def test_diagnosis_never_mutates_progress(self):
        class ReadAPI:
            def path(self,path):return path
            def get_file(self,path):
                values={'project/config.json':{'repository':'test/repo','members':{'A':None,'B':'alice','C':None}},
                    'sources/manifest.json':[{'source_origin':'source_materials/INFS3701/example.pdf'}],
                    'data/snapshot.json':{'generated_at':'2026-10-31T00:00:00Z'}}
                return {'type':'file','content':base64.b64encode(json.dumps(values.get(path,{})).encode()).decode()}
            def issue_list(self):return [{'body':'<!-- team-state\n{"task_id":"T01"}\n-->'}]
            def request(self,method,path,data=None):
                if method!='GET':raise AssertionError('Diagnosis attempted a write')
                return {'state':'disabled_manually'}
        report=team.diagnose(ReadAPI(),'alice')
        self.assertEqual(report['mode'],'read_only_no_progress_changed')
        self.assertEqual(report['role'],'B')
        self.assertEqual(report['task_cards'],1)
    def test_all_archived_sources_match_manifest(self):
        root=Path(__file__).resolve().parents[1]
        rows=json.loads((root/'sources/manifest.json').read_text(encoding='utf-8'))
        for row in rows:
            self.assertTrue(row['source_origin'].startswith('source_materials/INFS3701/'))
            self.assertEqual(hashlib.sha256((root/row['original_path']).read_bytes()).hexdigest(),row['sha256'])


if __name__=='__main__':unittest.main()
