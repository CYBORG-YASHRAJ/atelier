#!/usr/bin/env python3
"""Atelier store CLI. Token-lean pipe-row output (TOON-style), not JSON.

  store.py init                      create db + schema + seed
  store.py rules <domain>            active rules for a domain
  store.py registry <kind>           registry rows of a kind
  store.py map [topic]               framework graph: which file to load for a topic
  store.py sql "<SELECT ...>"        read query
  store.py exec "<INSERT/UPDATE>"    write statement
"""
import sqlite3, sys, os
from contextlib import closing
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import runtime
from initialize import initialize

ROOT = os.path.dirname(os.path.abspath(__file__))
DB = runtime.database()


def connect(writable=False, create=False):
    return runtime.connect(DB, writable=writable, create=create)


def init():
    with closing(connect(writable=True, create=True)) as c:
        initialize(c)
    print(f"ok|{DB}")


def rows(c, q, args=()):
    cur = c.execute(q, args)
    cols = [d[0] for d in cur.description]
    print("|".join(cols))
    for r in cur.fetchall():
        print("|".join("" if v is None else str(v).replace("\n", "\\n") for v in r))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "init":
        return init()
    if cmd == "help":
        return print(__doc__)
    with closing(connect(writable=cmd == "exec")) as c:
        dispatch(c, cmd)


def dispatch(c, cmd):
    if cmd == "rules":
        rows(c, "SELECT key,value,source FROM rules WHERE domain=? AND active=1", (sys.argv[2],))
    elif cmd == "registry":
        rows(c, "SELECT name,source,install,usage,meta FROM registry WHERE kind=?", (sys.argv[2],))
    elif cmd == "map":
        q = f"%{sys.argv[2]}%" if len(sys.argv) > 2 else "%"
        rows(c, "SELECT path,purpose,load_when,links FROM framework_map"
                " WHERE purpose LIKE ? OR load_when LIKE ? OR path LIKE ?", (q, q, q))
    elif cmd == "sql":
        rows(c, sys.argv[2])
    elif cmd == "exec":
        c.execute(sys.argv[2]); c.commit(); print("ok")
    else:
        print(__doc__)


if __name__ == "__main__":
    try:
        main()
    except (sqlite3.Error, OSError, IndexError, ValueError) as error:
        sys.exit(f"Atelier store: {error}. Run Atelier doctor for diagnostics.")
