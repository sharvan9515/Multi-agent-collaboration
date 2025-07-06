import os
import sys

project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from cybersecurity import monitor  # noqa: E402


class DummyResp:
    def __init__(self, status_code=200):
        self.status_code = status_code


def test_check_service_success(monkeypatch):
    def fake_get(url, timeout=5.0):
        return DummyResp(200)
    monkeypatch.setattr(monitor.httpx, "get", fake_get)
    assert monitor.check_service("http://x")


def test_check_service_failure(monkeypatch):
    def fake_get(url, timeout=5.0):
        raise monitor.httpx.RequestError("boom")
    monkeypatch.setattr(monitor.httpx, "get", fake_get)
    assert not monitor.check_service("http://x")


def test_check_services_logs(monkeypatch):
    messages = []
    monkeypatch.setattr(monitor, "_check_vector_store", lambda url: False)
    monkeypatch.setattr(monitor, "_check_broker", lambda url: False)
    monkeypatch.setattr(monitor, "log", lambda msg: messages.append(msg))
    monitor.check_services("vec", "bro")
    assert any("vec" in m for m in messages)
    assert any("bro" in m for m in messages)
