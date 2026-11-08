import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).resolve().parents[1] / "chemflow.db"

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL,
                input_text TEXT NOT NULL,
                result_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

@contextmanager
def connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def save_history(kind: str, input_text: str, result_json: str):
    with connection() as conn:
        conn.execute(
            "INSERT INTO analysis_history(kind, input_text, result_json) VALUES (?, ?, ?)",
            (kind, input_text, result_json),
        )

def get_history(limit: int = 20):
    with connection() as conn:
        rows = conn.execute(
            "SELECT id, kind, input_text, result_json, created_at "
            "FROM analysis_history ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [
        {"id": r[0], "kind": r[1], "input": r[2], "result": r[3], "created_at": r[4]}
        for r in rows
    ]
