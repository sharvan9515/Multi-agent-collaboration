"""Logging utility with optional correlation IDs for tracing."""

from __future__ import annotations

import uuid


def log(message: str, correlation_id: str | None = None) -> str:
    """Print a log message with a correlation ID.

    If ``correlation_id`` is not provided, a new short UUID is generated.  The
    correlation ID is returned so callers can reuse it for subsequent log
    entries.
    """

    cid = correlation_id or str(uuid.uuid4())[:8]
    print(f"[{cid}] {message}")
    return cid
