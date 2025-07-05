"""Simple JSON lines audit log writer."""

from __future__ import annotations

import json
import os
from datetime import datetime

from cybersecurity.integrity import generate_hash

AUDIT_LOG = os.getenv("AUDIT_LOG", "audit.log")


def log_audit_event(
    event_type: str,
    details: dict,
    data: bytes | None = None,
    include_hash: bool = False,
) -> None:
    """Append an audit entry to the log file.

    When ``include_hash`` is ``True`` and ``data`` is provided, a SHA-256 hash
    of the data will be stored alongside the event details.
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event": event_type,
        "details": details,
    }
    if include_hash and data is not None:
        entry["hash"] = generate_hash(data)
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def log_data_stored(data: bytes, include_hash: bool = False) -> None:
    """Log a ``data_stored`` event, optionally including a data hash."""
    log_audit_event("data_stored", {}, data=data, include_hash=include_hash)


def log_data_retrieved(data: bytes, include_hash: bool = False) -> None:
    """Log a ``data_retrieved`` event, optionally including a data hash."""
    log_audit_event("data_retrieved", {}, data=data, include_hash=include_hash)
