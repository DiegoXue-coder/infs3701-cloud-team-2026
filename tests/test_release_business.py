"""Offline failure-path checks; not evidence of a live AWS release."""
import ast
from email import policy
from email.parser import BytesParser
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


release = load('release_business', ROOT / 'deployment/release-business.py')
host = load('business_host', ROOT / 'deployment/business-host.py')


class ReleaseChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        release.build(self.directory)
        self.plan = json.loads((self.directory / 'plan.json').read_text())

    def tearDown(self):
        self.temp.cleanup()

    def test_pinned_archive_and_boot_payload(self):
        self.assertEqual(hashlib.sha256((self.directory / 'app.tar.gz').read_bytes()).hexdigest(), self.plan['archive_sha256'])
        for mode in ('release', 'rollback'):
            data = release.user_data(self.plan, 'a', mode, (ROOT / 'deployment/business-host.py').read_text())
            self.assertLess(len(data), 16384)
            msg = BytesParser(policy=policy.default).parsebytes(data)
            part = list(msg.iter_parts())[0]
            self.assertEqual(part.get_content_type(), 'text/x-shellscript-per-boot')
            script = part.get_content()
            python = script.split("<<'HOSTPY'\n", 1)[1].rsplit('\nHOSTPY', 1)[0]
            ast.parse(python)
            self.assertIn('READING_DATA_MODE=dynamodb', python)

    def test_failed_health_restores_previous_and_blocks_retry(self):
        base = self.directory / 'runtime'
        current, env, backup = base / 'current', base / 'app.env', base / 'foundation-backup'
        current.mkdir(parents=True)
        (current / 'app.py').write_text("stage='infrastructure-only'\n")
        env.write_text('APP_INSTANCE=az-a\n')
        client = Mock()
        raw = (self.directory / 'app.tar.gz').read_bytes()
        client.get_object.return_value = {'Body': io.BytesIO(raw)}
        session = Mock()
        session.get_credentials.return_value.method = 'iam-role'
        session.client.return_value = client
        import tarfile
        with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as archive:
            freeze = archive.extractfile('requirements.txt').read().decode()
        with patch.multiple(host, BASE=base, CURRENT=current, ENV=env, BACKUP=backup), patch.object(host.os, 'geteuid', create=True, return_value=0), patch.object(host.boto3, 'Session', return_value=session), patch.object(host.subprocess, 'run'), patch.object(host.subprocess, 'check_output', return_value=freeze), patch.object(host, 'switch') as switch, patch.object(host, 'restart') as restart, patch.object(host, 'check', side_effect=RuntimeError('simulated database unavailable')):
            with self.assertRaisesRegex(RuntimeError, 'simulated database'):
                host.main(dict(self.plan, label='az-a', mode='release'))
            self.assertEqual(switch.call_args_list[-1].args[0], backup / 'app')
            self.assertEqual(env.read_text(), 'APP_INSTANCE=az-a\n')
            self.assertEqual(restart.call_count, 2)
            self.assertTrue((base / ('release-blocked-' + release.COMMIT)).exists())
            with self.assertRaisesRegex(RuntimeError, 'blocked'):
                host.main(dict(self.plan, label='az-a', mode='release'))
        with patch.multiple(host, BASE=base, CURRENT=current, ENV=env, BACKUP=backup), patch.object(host.os, 'geteuid', create=True, return_value=0), patch.object(host, 'switch') as switch, patch.object(host, 'restart'), patch.object(host, 'check', return_value={'stage': 'infrastructure-only'}):
            host.main(dict(self.plan, label='az-a', mode='rollback'))
            switch.assert_called_once_with(backup / 'app')
            self.assertEqual(env.read_text(), 'APP_INSTANCE=az-a\n')

    def test_tampered_archive_cannot_switch_service(self):
        base = self.directory / 'runtime'
        current, env, backup = base / 'current', base / 'app.env', base / 'foundation-backup'
        current.mkdir(parents=True)
        (current / 'app.py').write_text("stage='infrastructure-only'\n")
        env.write_text('APP_INSTANCE=az-a\n')
        session = Mock()
        session.get_credentials.return_value.method = 'iam-role'
        session.client.return_value.get_object.return_value = {'Body': io.BytesIO(b'tampered')}
        with patch.multiple(host, BASE=base, CURRENT=current, ENV=env, BACKUP=backup), patch.object(host.os, 'geteuid', create=True, return_value=0), patch.object(host.boto3, 'Session', return_value=session), patch.object(host, 'switch') as switch:
            with self.assertRaises(AssertionError):
                host.main(dict(self.plan, label='az-a', mode='release'))
            switch.assert_not_called()
            self.assertEqual(env.read_text(), 'APP_INSTANCE=az-a\n')


if __name__ == '__main__':
    unittest.main()
