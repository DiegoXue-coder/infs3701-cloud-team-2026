"""Independent C tests: execute the original function without Flask, boto3 or AWS."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'app/reading_tracker.py'
FIXTURES = json.loads(Path(__file__).with_name('fixtures.json').read_text(encoding='utf-8'))


def original_function():
    tree = ast.parse(SOURCE.read_text(encoding='utf-8'))
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'compute_stats')
    namespace = {}
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(SOURCE), 'exec'), namespace)
    return namespace['compute_stats']


class StatisticsTests(unittest.TestCase):
    def setUp(self):
        self.stats = original_function()

    def test_fixture_expectations(self):
        for case in FIXTURES['statistics_cases']:
            with self.subTest(case=case['name']):
                self.assertEqual(self.stats(case['records']), case['expected'])

    def test_read_pages_not_book_lengths(self):
        self.assertEqual(self.stats([{'pages_read': 7, 'total_pages': 999}])['total_pages'], 7)

    def test_unrated_records_do_not_dilute_average(self):
        self.assertEqual(self.stats([{'rating': 5}, {}, {'rating': None}])['avg_rating'], 5.0)

    def test_missing_legacy_fields(self):
        self.assertEqual(self.stats([{}]), {'total': 1, 'reading': 0, 'finished': 0, 'want': 0, 'total_pages': 0, 'avg_rating': None})

    def test_legacy_numeric_strings(self):
        actual = self.stats([{'status': 'reading', 'pages_read': '29', 'rating': '4'}])
        self.assertEqual((actual['total_pages'], actual['avg_rating']), (29, 4.0))

    def test_permutation_invariance(self):
        records = FIXTURES['statistics_cases'][1]['records']
        self.assertEqual(self.stats(records), self.stats(list(reversed(records))))

    def test_repeating_records_scales_counts_and_pages(self):
        records = FIXTURES['statistics_cases'][1]['records']
        once, twice = self.stats(records), self.stats(records * 2)
        for field in ['total', 'reading', 'finished', 'want', 'total_pages']:
            self.assertEqual(twice[field], once[field] * 2)
        self.assertEqual(twice['avg_rating'], once['avg_rating'])

    def test_inputs_are_not_mutated(self):
        records = copy.deepcopy(FIXTURES['statistics_cases'][1]['records'])
        before = copy.deepcopy(records)
        self.stats(records)
        self.assertEqual(records, before)

    def test_invalid_numeric_legacy_value_raises(self):
        # Characterization, not HTTP validation: B must reject these before storage.
        for record in [{'pages_read': 'abc'}, {'rating': 'not-a-rating'}]:
            with self.subTest(record=record), self.assertRaises(ValueError):
                self.stats([record])

    def test_unknown_legacy_status_is_not_counted_as_known(self):
        result = self.stats([{'status': 'paused', 'pages_read': 1}])
        self.assertEqual(result['total'], 1)
        self.assertEqual(result['reading'] + result['want'] + result['finished'], 0)


if __name__ == '__main__':
    print(json.dumps({'source': 'app/reading_tracker.py', 'sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(), 'scope': 'isolated original compute_stats; no AWS; no HTTP acceptance'}), flush=True)
    unittest.main(verbosity=2)
