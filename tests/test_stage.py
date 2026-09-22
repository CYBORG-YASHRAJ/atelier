import json
import shutil
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from stage_codex_plugin import stage


class StagedPlugin(unittest.TestCase):
    def setUp(self):
        self.output = ROOT / "dist" / "test-marketplace"
        self.plugin = self.output / "plugins" / "atelier"

    def tearDown(self):
        if self.output.exists():
            shutil.rmtree(self.output)

    def test_runtime_package_is_clean_and_resolvable(self):
        stage(self.output)
        forbidden = {
            ".git",
            ".claude-plugin",
            "agents",
            "commands",
            "node_modules",
            "playwright-report",
            "test-results",
            "tests",
            "workspace",
        }
        self.assertFalse(forbidden.intersection(p.name for p in self.plugin.iterdir()))

        catalog_path = self.output / ".agents/plugins/marketplace.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        source = catalog["plugins"][0]["source"]["path"]
        self.assertEqual((self.output / source).resolve(), self.plugin.resolve())

        manifest = json.loads(
            (self.plugin / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        for key in ("skills", "mcpServers"):
            self.assertTrue((self.plugin / manifest[key]).exists())
        for key in ("logo", "composerIcon"):
            self.assertTrue((self.plugin / manifest["interface"][key]).is_file())


if __name__ == "__main__":
    unittest.main()
