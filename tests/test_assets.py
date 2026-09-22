import os
from unittest.mock import patch
from support import Project
import assets


class Assets(Project):
    def test_manifest_honors_override(self):
        self.env["ATELIER_DB"] = str(self.project / "relocated/state.db")
        self.initialize()
        with patch.dict(os.environ, {"ATELIER_DB": self.env["ATELIER_DB"]}):
            assets.manifest("input", "output", "image", 100, 50)
        with self.connection(self.env["ATELIER_DB"]) as c:
            self.assertEqual(c.execute("SELECT src,out FROM asset_manifest").fetchone(), ("input", "output"))
        self.assertFalse(self.db.exists())

    def test_no_credentials_fallback(self):
        import video
        with patch.dict(os.environ, {}, clear=True):
            rung, prompt = video.generate("a matte black cube")
        self.assertEqual(rung, 3)
        self.assertIn("matte black cube", prompt)
