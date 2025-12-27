import os
from getpass import getpass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization
from argon2.low_level import hash_secret_raw, Type

from aura.identity_paths import (
    IDENTITY_DIR,
    PRIVATE_KEY_FILE,
    ENCRYPTED_KEY_FILE,
    SALT_FILE,
)


def derive_key(password: str, salt: bytes) -> bytes:
    return hash_secret_raw(
        secret=password.encode(),
        salt=salt,
        time_cost=3,
        memory_cost=64 * 1024,  # 64 MB
        parallelism=2,
        hash_len=32,
        type=Type.ID,
    )


def lock_identity():
    if ENCRYPTED_KEY_FILE.exists():
        return

    if not PRIVATE_KEY_FILE.exists():
        raise RuntimeError("Private key not found")

    password = getpass("🔐 Create a password to protect your Aura identity: ")
    confirm = getpass("🔁 Confirm password: ")

    if password != confirm or len(password) < 6:
        raise RuntimeError("Passwords do not match or are too short")

    salt = os.urandom(16)
    key = derive_key(password, salt)

    private_bytes = PRIVATE_KEY_FILE.read_bytes()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)

    encrypted = aesgcm.encrypt(nonce, private_bytes, None)

    ENCRYPTED_KEY_FILE.write_bytes(nonce + encrypted)
    SALT_FILE.write_bytes(salt)

    PRIVATE_KEY_FILE.unlink()

    print("✅ Aura identity locked successfully.")


def unlock_identity():
    if not ENCRYPTED_KEY_FILE.exists():
        raise RuntimeError("Encrypted identity not found")

    password = getpass("🔓 Enter Aura password: ")

    salt = SALT_FILE.read_bytes()
    key = derive_key(password, salt)

    data = ENCRYPTED_KEY_FILE.read_bytes()
    nonce, ciphertext = data[:12], data[12:]

    aesgcm = AESGCM(key)

    try:
        private_bytes = aesgcm.decrypt(nonce, ciphertext, None)
    except Exception:
        raise RuntimeError("❌ Invalid password")

    return serialization.load_pem_private_key(
        private_bytes,
        password=None,
    )
