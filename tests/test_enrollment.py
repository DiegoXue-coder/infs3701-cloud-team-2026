"""Role enrollment must not overwrite people or bypass repository concurrency."""
import base64
import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import team

class ConfigAPI:
    def __init__(self,members=None):
        self.config={'repository':'test/repo','members':members or {'A':'owner','B':None,'C':None},'other_setting':'preserved'}
        self.writes=[]
    def get_file(self,path):
        return {'sha':'current-sha','content':base64.b64encode(json.dumps(self.config).encode()).decode()}
    def path(self,path):return path
    def request(self,method,path,data):
        self.writes.append(copy.deepcopy(data))
        assert method=='PUT' and path=='/contents/project/config.json'
        assert data['sha']=='current-sha' and data['branch']=='main'
        self.config=json.loads(base64.b64decode(data['content']))
        return {}

class EnrollmentRules(unittest.TestCase):
    def test_join_keeps_other_people_and_records_identity(self):
        api=ConfigAPI()
        result=team.enroll(api,'app-member','B')
        self.assertEqual(result['members'],{'A':'owner','B':'app-member','C':None})
        self.assertEqual(result['other_setting'],'preserved')
        self.assertEqual(result['enrollment_history'][0]['actor'],'app-member')
        self.assertEqual(len(api.writes),1)
    def test_repeat_join_is_idempotent_case_insensitive(self):
        api=ConfigAPI({'A':'owner','B':'Alice','C':None})
        team.enroll(api,'alice','B')
        self.assertFalse(api.writes)
    def test_cannot_take_occupied_role(self):
        api=ConfigAPI({'A':'owner','B':'Alice','C':None})
        with self.assertRaises(ValueError):team.enroll(api,'Bob','B')
        self.assertFalse(api.writes)
    def test_cannot_hold_two_roles(self):
        api=ConfigAPI({'A':'owner','B':'Alice','C':None})
        with self.assertRaises(ValueError):team.enroll(api,'ALICE','C')
        self.assertFalse(api.writes)
    def test_cannot_take_operator_role(self):
        api=ConfigAPI()
        with self.assertRaises(ValueError):team.enroll(api,'Bob','A')
        self.assertFalse(api.writes)
    def test_operator_cannot_self_join_another_role(self):
        api=ConfigAPI()
        with self.assertRaises(ValueError):team.enroll(api,'OWNER','B')
        self.assertFalse(api.writes)

if __name__=='__main__':unittest.main()
