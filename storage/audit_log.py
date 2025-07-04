"""Simple JSON lines audit log writer."""

from __future__ import annotations

import json
import os
from datetime import datetime

AUDIT_LOG = os.getenv("AUDIT_LOG", "audit.log")


def log_audit_event(event_type: str, details: dict) -> None:
    """Append an audit entry to the log file."""
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event": event_type,
        "details": details,
    }
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
