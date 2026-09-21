"""Read-only recovery for startup, resume and compaction on either host."""
import json
import sqlite3
import sys
from contextlib import closing
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import runtime


def context(cwd=None):
    path = runtime.database(cwd)
    if not path.exists():
        return ""
    try:
        with closing(runtime.connect(path)) as connection:
            version = connection.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()
            if version != ("1",):
                return "Atelier schema is incompatible; run Atelier doctor."
            plans = connection.execute(
                "SELECT id,title FROM plans WHERE status='active' ORDER BY id DESC"
            ).fetchall()
            if not plans:
                return "Atelier store present; use Atelier plan to start."
            if len(plans) > 1:
                return f"Atelier has multiple active plans; select an ID: {plans}"
            plan = plans[0]
            unmet = connection.execute(
                "SELECT criterion FROM done_criteria WHERE plan_id=? AND passed=0", (plan[0],)
            ).fetchall()
            return "\n".join([f"Atelier active plan #{plan[0]}: {plan[1]}",
                              f"Unmet done-criteria ({len(unmet)}):",
                              *[f"- {row[0]}" for row in unmet[:12]]])
    except (sqlite3.Error, OSError) as error:
        return f"Atelier store needs attention: {error}. Run Atelier doctor."


def main():
    try:
        data = json.load(sys.stdin)
    except (ValueError, OSError):
        data = {}
    out = context(data.get("cwd") if isinstance(data, dict) else None)
    if out:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart", "additionalContext": out}}))


if __name__ == "__main__":
    if "--test" in sys.argv:
        assert isinstance(context(), str)
        print("self-check ok")
    else:
        main()
