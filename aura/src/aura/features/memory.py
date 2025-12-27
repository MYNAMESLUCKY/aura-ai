import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / ".aura" / "aura.db"


def get_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER,
        role TEXT,
        content TEXT,
        created_at TEXT
    )
    """)

    db.commit()
    db.close()


def create_conversation():
    db = get_db()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO conversations (created_at) VALUES (?)",
        (datetime.utcnow().isoformat(),)
    )

    cid = cur.lastrowid
    db.commit()
    db.close()
    return cid


def save_message(conversation_id, role, content):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        """
        INSERT INTO messages (conversation_id, role, content, created_at)
        VALUES (?,?,?,?)
        """,
        (conversation_id, role, content, datetime.utcnow().isoformat())
    )

    db.commit()
    db.close()


def load_messages(conversation_id, limit=10):
    """
    Returns a list of (role, content) tuples in chronological order.
    """
    db = get_db()
    cur = db.cursor()

    cur.execute(
        """
        SELECT role, content FROM messages
        WHERE conversation_id=?
        ORDER BY id DESC
        LIMIT ?
        """,
        (conversation_id, limit)
    )

    rows = cur.fetchall()
    db.close()

    return list(reversed(rows))
