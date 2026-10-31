from pathlib import Path
import sys
import unittest

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

if __name__=='__main__':unittest.main()
