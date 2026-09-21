"""Read a single active plan and its criteria: python plan.py [ID]."""
import json
import sqlite3
import sys
from contextlib import closing
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import runtime


def selected(connection, plan_id=None):
    plans = connection.execute(
        "SELECT id,title,body_md FROM plans WHERE status='active' ORDER BY id"
    ).fetchall()
    if plan_id is not None:
        plans = [plan for plan in plans if plan[0] == plan_id]
    if not plans:
        raise ValueError("No matching active plan; run Atelier plan.")
    if len(plans) != 1:
        raise ValueError(f"Select an active plan ID: {[(p[0], p[1]) for p in plans]}")
    plan = plans[0]
    criteria = connection.execute(
        "SELECT id,criterion,check_kind,passed,evidence FROM done_criteria WHERE plan_id=? ORDER BY id",
        (plan[0],),
    ).fetchall()
    return {"id": plan[0], "title": plan[1], "body_md": plan[2], "criteria": criteria}


if __name__ == "__main__":
    try:
        with closing(runtime.connect()) as connection:
            print(json.dumps(selected(connection, int(sys.argv[1]) if len(sys.argv) > 1 else None)))
    except (ValueError, OSError, sqlite3.Error) as error:
        sys.exit(f"Atelier: {error}")
