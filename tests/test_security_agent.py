import os
import sys

project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agents.security_agent import SecurityAgent  # noqa: E402
from cybersecurity import encryption, integrity, monitor  # noqa: E402


def _setup_key(monkeypatch):
    """Utility to reset and generate an encryption key."""
    monkeypatch.delenv(encryption.ENV_KEY, raising=False)
    encryption.generate_key()


def test_encrypt_decrypt_cycle(monkeypatch):
    _setup_key(monkeypatch)
    plaintext = "secret"
    token = encryption.encrypt_data(plaintext)

    called = {}
    monkeypatch.setattr(monitor, "check_services", lambda: called.setdefault("called", True))

    agent = SecurityAgent()
    out, ctx = agent.act(token, {})

    assert ctx["decrypted"] is True
    assert ctx["encrypted"] is True
    assert ctx["services_checked"] is True
    assert "hash_valid" not in ctx
    assert called.get("called") is True
    assert encryption.decrypt_data(out) == plaintext


def test_hash_verification(monkeypatch):
    _setup_key(monkeypatch)
    plaintext = "verify"
    token = encryption.encrypt_data(plaintext)
    expected = integrity.generate_hash(plaintext.encode())

    monkeypatch.setattr(monitor, "check_services", lambda: None)

    agent = SecurityAgent()
    out, ctx = agent.act(token, {"hash": expected})

    assert ctx["hash_valid"] is True
    assert encryption.decrypt_data(out) == plaintext

    wrong = integrity.generate_hash(b"bad")
    out2, ctx2 = agent.act(token, {"hash": wrong})
    assert ctx2["hash_valid"] is False
    assert encryption.decrypt_data(out2) == plaintext


def test_service_health_called(monkeypatch):
    _setup_key(monkeypatch)
    monkeypatch.setattr(monitor, "check_services", lambda: setattr(monitor, "_called", True))

    agent = SecurityAgent()
    agent.act("hello", {})

    assert getattr(monitor, "_called", False)
