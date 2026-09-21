"""Isolated projects for host and state contract tests."""
import json
import sqlite3
from contextlib import closing, contextmanager
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_TEMP = ROOT / ".test-work"
sys.path[:0] = [str(ROOT), str(ROOT / "hooks"), str(ROOT / "db"), str(ROOT / "mcp/assets")]


class Project(unittest.TestCase):
    def setUp(self):
        TEST_TEMP.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(
            prefix="atelier space ", dir=TEST_TEMP
        )
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.env = dict(os.environ, PYTHONUTF8="1")
        self.env.pop("ATELIER_DB", None)
        self.db = self.project / "workspace/atelier.db"

    def run_script(self, path, *args, data=None):
        return subprocess.run(
            [sys.executable, str(ROOT / path), *map(str, args)],
            cwd=self.project, env=self.env,
            input=json.dumps(data) if data is not None else "",
            capture_output=True, text=True, encoding="utf-8",
        )

    @contextmanager
    def connection(self, path=None):
        with closing(sqlite3.connect(path or self.db)) as connection:
            with connection:
                yield connection

    def initialize(self):
        result = self.run_script("db/store.py", "init")
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def source(self, name, words):
        path = self.project / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("x " * words, encoding="utf-8")
        return path
