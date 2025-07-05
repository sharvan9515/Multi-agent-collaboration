from __future__ import annotations

from .base import Agent
from cybersecurity import encryption, integrity, monitor


class SecurityAgent(Agent):
    """Agent that validates message integrity and service health."""

    def act(self, message: str, context: dict) -> tuple[str, dict]:
        """Decrypt the message, verify its hash and re-encrypt the result."""
        # Attempt to decrypt the incoming message
        try:
            plaintext = encryption.decrypt_data(message)
            context["decrypted"] = True
        except Exception:
            plaintext = message
            context["decrypted"] = False

        # Verify hash when provided
        expected = context.get("hash")
        if expected is not None:
            context["hash_valid"] = integrity.verify_hash(plaintext.encode(), expected)

        # Confirm services are healthy
        monitor.check_services()
        context["services_checked"] = True

        # Re-encrypt outgoing message
        try:
            encrypted = encryption.encrypt_data(plaintext)
            context["encrypted"] = True
        except Exception:
            encrypted = plaintext
            context["encrypted"] = False

        return encrypted, context
