import sys
from support import Project, ROOT
sys.path.insert(0, str(ROOT / "scripts"))
from size_audit import audit


class Audit(Project):
    def test_catches_shell_written_source_and_skips_dependencies(self):
        self.source("src/large.ts", 400)
        self.source("node_modules/large.ts", 400)
        self.source(".venv/test.py", 400)
        result = self.run_script("scripts/size_audit.py", self.project)
        self.assertEqual(result.returncode, 1)
        self.assertIn("large.ts", result.stdout)
        self.assertNotIn("node_modules", result.stdout)
        self.assertEqual(len(audit(self.project)), 1)

    def test_soft_limit_is_warning(self):
        self.source("src/warning.py", 300)
        result = self.run_script("scripts/size_audit.py", self.project)
        self.assertEqual(result.returncode, 0)
        self.assertIn("warn:", result.stdout)
