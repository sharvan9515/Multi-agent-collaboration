"""Data integrity utilities using SHA-256."""

from __future__ import annotations

import hashlib


def generate_hash(data: bytes) -> str:
    """Return the SHA-256 hex digest of ``data``."""
    return hashlib.sha256(data).hexdigest()


def verify_hash(data: bytes, expected_hash: str) -> bool:
    """Check that ``data`` matches the given SHA-256 ``expected_hash``."""
    return generate_hash(data) == expected_hash.lower()
