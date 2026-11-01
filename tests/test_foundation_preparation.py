"""Offline boundaries only; these tests do not prove private AWS connectivity."""
import contextlib
import email
import importlib.util
import io
import os
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_launcher():
    spec = importlib.util.spec_from_file_location("foundation_launcher", ROOT / "deployment/launch-foundation.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FoundationPreparation(unittest.TestCase):
    def test_boot_diagnostics_are_per_boot_and_contain_no_business_write(self):
        spec = importlib.util.spec_from_file_location("maintenance", ROOT / "deployment/maintain-foundation.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for label in ("a", "b"):
            message = email.message_from_string(module.user_data(label))
            part = message.get_payload()[0]
            self.assertEqual(part.get_content_type(), "text/x-shellscript-per-boot")
            script = part.get_payload(decode=True).decode()
            self.assertIn("APP_INSTANCE=az-" + label, script)
            self.assertNotIn("put_item", script)
            self.assertNotIn("delete_item", script)
            self.assertNotIn("AWS_ACCESS_KEY_ID", script)
            self.assertIn("INFS3701_BOOT_CHECK_OK=", script)

    def test_default_command_cannot_connect_to_aws(self):
        module = load_launcher()
        output = io.StringIO()
        with patch.object(sys, "argv", ["launch-foundation.py"]), \
                patch.object(module.boto3, "Session", side_effect=AssertionError("Offline plan touched AWS")), \
                contextlib.redirect_stdout(output):
            module.main()
        self.assertIn("OFFLINE_PLAN=", output.getvalue())
        self.assertIn('"approval_required": true', output.getvalue())

    def test_placeholder_identifies_instance_and_does_not_claim_business_ready(self):
        script = (ROOT / "deployment/runtime-builder.sh").read_text(encoding="utf-8")
        code = re.search(r"<<'PYAPP'\n(.*?)\nPYAPP", script, re.S).group(1)
        namespace = {"__name__": "__main__"}
        with patch.dict(os.environ, {"APP_INSTANCE": "test-az-a"}):
            exec(compile(code, "<actual runtime placeholder>", "exec"), namespace)
            client = namespace["app"].test_client()
            health = client.get("/health")
            self.assertEqual(health.status_code, 200)
            self.assertEqual(health.json["stage"], "infrastructure-only")
            self.assertEqual(health.headers["X-App-Instance"], "test-az-a")
            self.assertIn(b"has not been deployed", client.get("/").data)

    def test_endpoint_policy_is_bound_to_role_transport_and_resource(self):
        module = load_launcher()
        statement = module.endpoint_policy(["dynamodb:GetItem"], module.TABLE)["Statement"][0]
        self.assertEqual(statement["Action"], ["dynamodb:GetItem"])
        self.assertEqual(statement["Resource"], [module.TABLE])
        self.assertEqual(statement["Condition"]["ArnEquals"]["aws:PrincipalArn"], module.ROLE)
        self.assertEqual(statement["Condition"]["Bool"]["aws:SecureTransport"], "true")


if __name__ == "__main__":
    unittest.main()
