"""Simple symmetric encryption helpers using Fernet."""

from __future__ import annotations

import os

try:
    from cryptography.fernet import Fernet
except ImportError:  # pragma: no cover - optional dependency
    Fernet = None


ENV_KEY = "ENCRYPTION_KEY"


def generate_key() -> bytes:
    """Generate and store a new Fernet key in the environment."""
    if Fernet is None:
        raise RuntimeError("cryptography is required for encryption")
    key = Fernet.generate_key()
    os.environ[ENV_KEY] = key.decode()
    return key


def _get_fernet() -> Fernet:
    if Fernet is None:
        raise RuntimeError("cryptography is required for encryption")
    key = os.getenv(ENV_KEY)
    if not key:
        raise ValueError(f"{ENV_KEY} not set. Call generate_key() first.")
    return Fernet(key.encode())


def encrypt_data(data: str | bytes) -> str:
    """Encrypt the provided data and return a token string."""
    f = _get_fernet()
    if isinstance(data, str):
        data = data.encode()
    token = f.encrypt(data)
    return token.decode()


def decrypt_data(token: str | bytes) -> str:
    """Decrypt the token using the stored key and return plaintext."""
    f = _get_fernet()
    if isinstance(token, str):
        token = token.encode()
    plaintext = f.decrypt(token)
    try:
        return plaintext.decode()
    except UnicodeDecodeError:
        return plaintext
