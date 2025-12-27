from pathlib import Path

AURA_DIR = Path.home() / ".aura"
IDENTITY_DIR = AURA_DIR / "identity"

USER_ID_FILE = IDENTITY_DIR / "user_id.txt"
PRIVATE_KEY_FILE = IDENTITY_DIR / "private_key.pem"
PUBLIC_KEY_FILE = IDENTITY_DIR / "public_key.pem"

ENCRYPTED_KEY_FILE = IDENTITY_DIR / "private_key.enc"
SALT_FILE = IDENTITY_DIR / "salt.bin"
