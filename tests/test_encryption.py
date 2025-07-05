import os
import sys

project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from cybersecurity import encryption  # noqa: E402


def test_encrypt_decrypt_roundtrip(monkeypatch):
    monkeypatch.delenv(encryption.ENV_KEY, raising=False)
    key = encryption.generate_key()
    assert os.environ[encryption.ENV_KEY] == key.decode()

    token = encryption.encrypt_data("hello")
    assert token != "hello"
    plaintext = encryption.decrypt_data(token)
    assert plaintext == "hello"
