import sqlite3
import json
import math
from pathlib import Path
from datetime import datetime
from typing import List

from aura.embeddings import embed_text

# ---------------- PATH ----------------
DB_PATH = Path.home() / ".aura" / "aura.db"


# ---------------- DB ----------------
def get_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_vector_memory():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS vector_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        content TEXT NOT NULL,
        embedding TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    db.commit()
    db.close()


# ---------------- STORE ----------------
def store_memory(user_id: str, text: str):
    text = text.strip()
    if not text:
        return

    try:
        embedding = embed_text(text)
    except Exception as e:
        print("⚠️ Embedding failed, memory not stored:", e)
        return

    db = get_db()
    cur = db.cursor()

    cur.execute(
        """
        INSERT INTO vector_memory (user_id, content, embedding, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            text,
            json.dumps(embedding),
            datetime.utcnow().isoformat(),
        )
    )

    db.commit()
    db.close()


# ---------------- SIMILARITY ----------------
def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b + 1e-9)


# ---------------- RETRIEVE ----------------
def retrieve_memories(
    user_id: str,
    query: str,
    limit: int = 5,
    min_score: float = 0.25,   # 🔒 prevents garbage recall
) -> List[str]:

    try:
        query_embedding = embed_text(query)
    except Exception:
        return []

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT content, embedding FROM vector_memory WHERE user_id = ?",
        (user_id,)
    )

    rows = cur.fetchall()
    db.close()

    scored = []
    for content, emb_json in rows:
        emb = json.loads(emb_json)
        score = cosine_similarity(query_embedding, emb)
        if score >= min_score:
            scored.append((score, content))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [content for _, content in scored[:limit]]
#--------------------------SAFE WRAPPER--------------------------------------#
def maybe_store_memory(user_id: str, text: str):
    """
    Store only meaningful, personal information.
    """
    text = text.strip()

    if len(text) < 8:
        return

    # Avoid questions & commands
    if text.endswith("?"):
        return

    store_memory(user_id, text)
