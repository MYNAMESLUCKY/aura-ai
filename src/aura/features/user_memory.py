import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / ".aura" / "aura.db"


# ---------------- DB ----------------
def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_user_memory():
    """
    Stores SMALL, explicit, profile-like facts.
    Not used for semantic recall (that's vector_memory).
    """
    db = get_db()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_memory (
        user_id TEXT NOT NULL,
        key TEXT NOT NULL,
        value TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        PRIMARY KEY (user_id, key)
    )
    """)

    db.commit()
    db.close()


# ---------------- WRITE ----------------
def save_fact(user_id: str, key: str, value: str):
    key = key.strip().lower()
    value = value.strip()

    if not key or not value:
        return

    db = get_db()
    cur = db.cursor()

    cur.execute(
        """
        INSERT INTO user_memory (user_id, key, value, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, key)
        DO UPDATE SET
            value = excluded.value,
            updated_at = excluded.updated_at
        """,
        (user_id, key, value, datetime.utcnow().isoformat())
    )

    db.commit()
    db.close()


# ---------------- READ ----------------
def load_facts(user_id: str) -> dict:
    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT key, value FROM user_memory WHERE user_id = ?",
        (user_id,)
    )

    rows = cur.fetchall()
    db.close()

    return {key: value for key, value in rows}
