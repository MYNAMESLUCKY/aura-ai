# aura/identity.py

from pathlib import Path
import uuid

AURA_DIR = Path.home() / ".aura"
IDENTITY_DIR = AURA_DIR / "identity"
USER_ID_FILE = IDENTITY_DIR / "user_id.txt"


def ensure_identity():
    """
    Ensure a persistent Aura identity exists.
    Creates one if missing.
    """
    if USER_ID_FILE.exists():
        return load_identity_metadata()

    IDENTITY_DIR.mkdir(parents=True, exist_ok=True)

    user_id = str(uuid.uuid4())
    USER_ID_FILE.write_text(user_id)

    return {"user_id": user_id}


def load_identity_metadata():
    if not USER_ID_FILE.exists():
        raise RuntimeError("Aura identity not found")

    return {
        "user_id": USER_ID_FILE.read_text().strip()
    }
