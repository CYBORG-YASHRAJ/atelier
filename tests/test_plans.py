import json
from support import Project


class Plans(Project):
    def test_selection_and_criterion_isolation(self):
        self.initialize()
        with self.connection(self.db) as connection:
            connection.executemany("INSERT INTO plans(id,title,status) VALUES (?,?,'active')",
                                   [(1, "First"), (2, "Second")])
            connection.executemany("INSERT INTO done_criteria(plan_id,criterion) VALUES (?,?)",
                                   [(1, "one"), (2, "two")])
        result = self.run_script("db/plan.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Select an active plan ID", result.stderr)
        result = self.run_script("db/plan.py", 2)
        self.assertEqual(result.returncode, 0, result.stderr)
        state = json.loads(result.stdout)
        self.assertEqual(state["id"], 2)
        self.assertEqual([row[1] for row in state["criteria"]], ["two"])
        result = self.run_script("hooks/session_start.py", data={"cwd": str(self.project)})
        self.assertIn("multiple active plans", result.stdout)
        self.assertNotEqual(self.run_script("db/plan.py", 99).returncode, 0)

    def test_no_active_plan(self):
        self.initialize()
        result = self.run_script("db/plan.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No matching active plan", result.stderr)
