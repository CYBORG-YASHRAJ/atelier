"""Resolve project state independently of the installed plugin directory."""
import os
import sqlite3
from pathlib import Path


def database(cwd=None):
    root = Path(cwd or os.getcwd()).resolve()
    configured = os.environ.get("ATELIER_DB")
    path = Path(configured).expanduser() if configured else Path("workspace/atelier.db")
    return (root / path).resolve()


def connect(path=None, *, writable=False, create=False):
    path = Path(path) if path else database()
    if create:
        path.parent.mkdir(parents=True, exist_ok=True)
    elif not path.is_file():
        raise FileNotFoundError(f"No Atelier store at {path}; run Atelier bootstrap.")
    mode = "rwc" if create else "rw" if writable else "ro"
    connection = sqlite3.connect(path.as_uri() + f"?mode={mode}", uri=True, timeout=10)
    if writable:
        connection.execute("PRAGMA journal_mode=WAL")
    return connection
