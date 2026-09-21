import os
import sys
from unittest.mock import patch
from support import Project, ROOT
sys.path.insert(0, str(ROOT / "scripts"))
from mcp_transport import Client


class MCP(Project):
    def test_protocol_and_environment_inheritance(self):
        with patch.dict(os.environ, {"ATELIER_TEST_TOKEN": "fixture-not-secret"}):
            client = Client([sys.executable, str(ROOT / "tests/fake_mcp.py")], self.project)
        try:
            result = client.request(1, "initialize", {})
            self.assertEqual(result["protocolVersion"], "2024-11-05")
            client.send({"method": "notifications/initialized"})
            result = client.request(2, "tools/list", {})
            self.assertTrue(result["credentialInherited"])
            self.assertEqual(result["tools"][0]["name"], "fixture")
            self.assertNotIn("fixture-not-secret", str(result))
        finally:
            client.close()
