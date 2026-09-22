import json
from support import Project


class Hooks(Project):
    def invoke(self, tool, payload):
        return self.run_script("hooks/file_size_gate.py", data={
            "cwd": str(self.project), "tool_name": tool, "tool_input": payload})

    def test_claude_thresholds(self):
        for words, code, warning in [(250, 0, False), (251, 0, True),
                                      (350, 0, True), (351, 2, True)]:
            self.source("sample.py", words)
            result = self.invoke("Write", {"file_path": "sample.py"})
            self.assertEqual(result.returncode, code, result.stderr)
            self.assertEqual(bool(result.stdout), warning)
            if warning:
                self.assertIn("additionalContext", json.loads(result.stdout)["hookSpecificOutput"])

    def test_codex_multi_file_move_delete(self):
        self.source("small.py", 20)
        self.source("space moved.py", 351)
        self.source("café.py", 400)
        patch = ("*** Begin Patch\n*** Add File: small.py\n+x\n"
                 "*** Update File: old.py\n*** Move to: space moved.py\n"
                 "*** Delete File: deleted.py\n*** Update File: café.py\n*** End Patch")
        result = self.invoke("apply_patch", {"command": patch})
        self.assertEqual(result.returncode, 2)
        self.assertIn("space moved.py", result.stderr)
        self.assertIn("café.py", result.stderr)
        self.assertNotIn("deleted.py", result.stderr)

    def test_exempt_and_nonmatching(self):
        for name in ["notes.md", "generated/code.py", "node_modules/test.js"]:
            self.source(name, 400)
            self.assertEqual(self.invoke("Edit", {"file_path": name}).stdout, "")
        self.assertEqual(self.invoke("Bash", {"command": "anything"}).stdout, "")

    def test_malformed_payload(self):
        result = self.run_script("hooks/file_size_gate.py", data=[])
        self.assertEqual(result.returncode, 0)
        self.assertIn("invalid hook payload", result.stdout)
