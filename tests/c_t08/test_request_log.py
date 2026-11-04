"""Real loopback HTTP fixture only; no Reading Tracker or ALB behavior is simulated as evidence."""
import importlib.util
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('c_request_log', ROOT / 'scripts/c_request_log.py')
LOGGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LOGGER)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/slow':
            time.sleep(0.2)
        self.send_response(503 if self.path == '/fail' else 200)
        if self.path != '/no-id':
            self.send_header('X-App-Instance', 'local-fixture-only')
        self.end_headers()

    def log_message(self, *args):
        pass


class RequestLoggerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = 'http://127.0.0.1:' + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / 'requests.jsonl'

    def run_sample(self, path, count=1, timeout=1):
        return LOGGER.sample(self.url + path, count, 0.1, timeout, self.output, 'local-fixture')

    def test_real_success_request_fields_and_bound(self):
        summary = self.run_sample('/health', count=3)
        rows = [json.loads(line) for line in self.output.read_text().splitlines()]
        self.assertEqual(summary['requests'], 3)
        self.assertEqual(summary['successful_2xx'], 3)
        self.assertEqual(summary['instances'], {'local-fixture-only': 3})
        self.assertEqual([row['sequence'] for row in rows], [1, 2, 3])
        self.assertTrue(all(row['elapsed_ms'] >= 0 and row['time_utc'].endswith('+00:00') for row in rows))

    def test_http_error_retains_status_and_instance(self):
        summary = self.run_sample('/fail')
        row = json.loads(self.output.read_text())
        self.assertEqual((row['status'], row['error'], summary['failures']), (503, 'http_error', 1))
        self.assertEqual(row['instance'], 'local-fixture-only')

    def test_timeout_keeps_record_and_failure(self):
        summary = self.run_sample('/slow', timeout=0.05)
        row = json.loads(self.output.read_text())
        self.assertEqual(summary['failures'], 1)
        self.assertIsNone(row['status'])
        self.assertIsNotNone(row['error'])

    def test_missing_instance_is_explicit(self):
        self.assertEqual(self.run_sample('/no-id')['missing_instance'], 1)

    def test_refuses_overwriting_evidence(self):
        self.output.write_text('original\n')
        with self.assertRaises(FileExistsError):
            self.run_sample('/health')
        self.assertEqual(self.output.read_text(), 'original\n')

    def test_invalid_bounds_and_credential_urls_rejected(self):
        for url, count, interval, timeout in [(self.url, 0, 1, 1), (self.url, 601, 1, 1), (self.url, 1, 0, 1), (self.url, 1, 1, 0), ('http://user:secret@localhost/', 1, 1, 1), ('http://localhost/?token=test', 1, 1, 1)]:
            with self.subTest(count=count, interval=interval, timeout=timeout), self.assertRaises(ValueError):
                LOGGER.sample(url, count, interval, timeout, self.output, 'local-fixture')

    def test_base_url_cli_and_persistent_sample(self):
        # This file is persistent evidence, clearly labelled local-fixture.
        output = ROOT / 'evidence/T08/2026-11-04-local-fixture-requests.jsonl'
        if output.exists():
            output = self.output
        run = subprocess.run([sys.executable, str(ROOT / 'scripts/c_request_log.py'), '--count', '4', '--interval', '0.1', '--output', str(output), '--stage', 'local-fixture'], env=dict(os.environ, BASE_URL=self.url + '/health'), capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        summary = json.loads(run.stdout)
        self.assertEqual((summary['requests'], summary['successful_2xx']), (4, 4))
        print('BASE_URL CLI EVIDENCE: ' + run.stdout.strip(), flush=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
