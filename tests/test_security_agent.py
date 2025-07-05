import os
import sys

project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agents.security_agent import SecurityAgent  # noqa: E402
from cybersecurity import encryption, integrity, monitor  # noqa: E402


def test_security_agent_cycle(monkeypatch):
    # Setup encryption key
    monkeypatch.delenv(encryption.ENV_KEY, raising=False)
    encryption.generate_key()

    plaintext = "secure"
    token = encryption.encrypt_data(plaintext)
    expected = integrity.generate_hash(plaintext.encode())

    called = {}
    monkeypatch.setattr(monitor, "check_services", lambda: called.setdefault("called", True))

    agent = SecurityAgent()
    out, ctx = agent.act(token, {"hash": expected})

    assert ctx["decrypted"] is True
    assert ctx["hash_valid"] is True
    assert ctx["encrypted"] is True
    assert ctx["services_checked"] is True
    assert called.get("called") is True

    assert encryption.decrypt_data(out) == plaintext
