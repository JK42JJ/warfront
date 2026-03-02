"""warfront/data/progress.py — SQLite-backed progress manager (replaces JSON)"""
from __future__ import annotations
import json
import os
import sqlite3
from typing import Dict, List, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _db_path() -> str:
    from warfront.config import cfg
    return os.path.join(BASE_DIR, cfg.paths.db_file)


def _conn() -> sqlite3.Connection:
    con = sqlite3.connect(_db_path())
    con.execute("PRAGMA journal_mode=WAL")
    return con


def init_db() -> None:
    """Create tables if they don't exist."""
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                file        TEXT PRIMARY KEY,
                completed   INTEGER NOT NULL DEFAULT 0,
                attempts    INTEGER NOT NULL DEFAULT 0,
                first_solve TEXT,
                last_attempt TEXT
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS meta (
                key   TEXT PRIMARY KEY,
                value TEXT
            )
        """)


def mark_complete(filename: str) -> None:
    """Record a successful solve for *filename*."""
    import datetime
    now = datetime.datetime.utcnow().isoformat()
    with _conn() as con:
        con.execute("""
            INSERT INTO progress (file, completed, attempts, first_solve, last_attempt)
            VALUES (?, 1, COALESCE((SELECT attempts FROM progress WHERE file=?), 0) + 1, ?, ?)
            ON CONFLICT(file) DO UPDATE SET
                completed    = 1,
                attempts     = attempts + 1,
                first_solve  = COALESCE(first_solve, excluded.first_solve),
                last_attempt = excluded.last_attempt
        """, (filename, filename, now, now))


def increment_attempts(filename: str) -> None:
    """Record an execution attempt (save) for *filename*."""
    import datetime
    now = datetime.datetime.utcnow().isoformat()
    with _conn() as con:
        con.execute("""
            INSERT INTO progress (file, completed, attempts, last_attempt)
            VALUES (?, 0, 1, ?)
            ON CONFLICT(file) DO UPDATE SET
                attempts     = attempts + 1,
                last_attempt = excluded.last_attempt
        """, (filename, now))


def get_progress() -> Dict:
    """Return dict with 'completed' list and 'attempts' dict (mirrors v1 JSON schema)."""
    init_db()
    with _conn() as con:
        rows = con.execute(
            "SELECT file, completed, attempts FROM progress"
        ).fetchall()
    completed = [r[0] for r in rows if r[1]]
    attempts = {r[0]: r[2] for r in rows}
    return {"completed": completed, "attempts": attempts}


def get_all_rows() -> List[Dict]:
    """Return full row data for analytics."""
    init_db()
    with _conn() as con:
        rows = con.execute(
            "SELECT file, completed, attempts, first_solve, last_attempt FROM progress"
        ).fetchall()
    return [
        {
            "file": r[0],
            "completed": bool(r[1]),
            "attempts": r[2],
            "first_solve": r[3],
            "last_attempt": r[4],
        }
        for r in rows
    ]


def migrate_from_json(json_path: Optional[str] = None) -> int:
    """One-time migration: read v1 JSON progress → insert into SQLite.
    Returns number of rows migrated."""
    if json_path is None:
        from warfront.config import cfg
        json_path = os.path.join(BASE_DIR, cfg.paths.progress_file)
    if not os.path.exists(json_path):
        return 0
    try:
        with open(json_path) as f:
            data = json.load(f)
    except Exception:
        return 0

    init_db()
    completed = set(data.get("completed", []))
    attempts_map = data.get("attempts", {})
    all_files = completed | set(attempts_map.keys())

    count = 0
    with _conn() as con:
        for fname in all_files:
            comp = 1 if fname in completed else 0
            atts = attempts_map.get(fname, 1 if fname in completed else 0)
            con.execute("""
                INSERT OR IGNORE INTO progress (file, completed, attempts)
                VALUES (?, ?, ?)
            """, (fname, comp, atts))
            count += 1
    return count
