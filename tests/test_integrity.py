import os
import sys

project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from cybersecurity import integrity  # noqa: E402


def test_hash_generation_and_verification():
    data = b"secret"
    digest = integrity.generate_hash(data)
    assert isinstance(digest, str)
    assert integrity.verify_hash(data, digest)
    assert not integrity.verify_hash(b"other", digest)
