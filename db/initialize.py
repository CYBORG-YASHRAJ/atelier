"""Refresh core defaults without replacing learned registry/map entries."""
import json
import sqlite3
from contextlib import closing
from pathlib import Path


def merge(connection, seed, table, keys):
    columns = [row[1] for row in seed.execute(f"PRAGMA table_info({table})") if row[1] != "id"]
    fields = ",".join(columns)
    where = " AND ".join(f"{key}=?" for key in keys)
    for row in seed.execute(f"SELECT {fields} FROM {table}"):
        identity = tuple(row[columns.index(key)] for key in keys)
        marker = f"seed:{table}:{json.dumps(identity)}"
        previous = connection.execute("SELECT value FROM meta WHERE key=?", (marker,)).fetchone()
        existing = connection.execute(f"SELECT {fields} FROM {table} WHERE {where}", identity).fetchone()
        if existing is None:
            placeholders = ",".join("?" for _ in columns)
            connection.execute(f"INSERT INTO {table} ({fields}) VALUES ({placeholders})", row)
        elif previous and list(existing) == json.loads(previous[0]):
            assignments = ",".join(f"{col}=?" for col in columns)
            connection.execute(f"UPDATE {table} SET {assignments} WHERE {where}", (*row, *identity))
        connection.execute("INSERT OR REPLACE INTO meta VALUES (?,?)", (marker, json.dumps(row)))


def initialize(connection):
    root = Path(__file__).resolve().parent
    tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    if tables:
        version = connection.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()
        if version != ("1",):
            raise ValueError("Incompatible store schema; run Atelier doctor before updating")
    schema = (root / "schema.sql").read_text(encoding="utf-8")
    connection.executescript(schema)
    with closing(sqlite3.connect(":memory:")) as seed:
        seed.executescript(schema)
        seed.executescript((root / "seed/seed.sql").read_text(encoding="utf-8"))
        with connection:
            connection.execute("DELETE FROM rules WHERE source='core'")
            connection.executemany(
                "INSERT INTO rules(domain,key,value,source,active) VALUES (?,?,?,?,?)",
                seed.execute("SELECT domain,key,value,source,active FROM rules"))
            merge(connection, seed, "registry", ("kind", "name"))
            merge(connection, seed, "framework_map", ("path",))
            connection.execute("DELETE FROM framework_map WHERE path='docs/IMPLEMENTATION-PLAN.md'")
