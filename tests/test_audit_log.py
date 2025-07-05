import json
import os
import sys

project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from storage import audit_log  # noqa: E402
from cybersecurity import integrity  # noqa: E402


def test_log_data_stored_with_hash(monkeypatch, tmp_path):
    log_file = tmp_path / "audit.log"
    monkeypatch.setenv("AUDIT_LOG", str(log_file))
    monkeypatch.setattr(audit_log, "AUDIT_LOG", str(log_file), raising=False)

    audit_log.log_data_stored(b"hello", include_hash=True)

    entry = json.loads(log_file.read_text().splitlines()[0])
    assert entry["event"] == "data_stored"
    expected = integrity.generate_hash(b"hello")
    assert entry["hash"] == expected
