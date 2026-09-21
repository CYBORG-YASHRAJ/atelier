import json
from support import Project


class State(Project):
    def test_missing_reads_do_not_create_store(self):
        result = self.run_script("db/store.py", "sql", "SELECT 1")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.db.parent.exists())
        result = self.run_script("hooks/session_start.py", data={"cwd": str(self.project)})
        self.assertEqual(result.stdout, "")
        self.assertFalse(self.db.exists())

    def test_override_shared_by_store_and_recovery(self):
        self.env["ATELIER_DB"] = "custom space/state.db"
        self.initialize()
        path = self.project / self.env["ATELIER_DB"]
        with self.connection(path) as connection:
            connection.execute("INSERT INTO plans(id,title,status) VALUES (7,'Resume me','active')")
            connection.execute("INSERT INTO done_criteria(plan_id,criterion) VALUES (7,'Check this')")
        result = self.run_script("hooks/session_start.py", data={"cwd": str(self.project)})
        self.assertIn("Resume me", result.stdout)
        self.assertIn("Check this", result.stdout)
        self.assertFalse(self.db.exists())

    def test_reads_cannot_write(self):
        self.initialize()
        result = self.run_script("db/store.py", "sql", "DELETE FROM rules")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("readonly", result.stderr)

    def test_corruption_and_version(self):
        self.db.parent.mkdir()
        self.db.write_text("not sqlite")
        result = self.run_script("hooks/session_start.py", data={"cwd": str(self.project)})
        self.assertIn("needs attention", result.stdout)
        self.db.unlink()
        self.initialize()
        with self.connection(self.db) as connection:
            connection.execute("UPDATE meta SET value='999' WHERE key='schema_version'")
        result = self.run_script("db/store.py", "init")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Incompatible", result.stderr)
