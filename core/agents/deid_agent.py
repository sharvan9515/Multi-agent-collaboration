from .base import Agent


class DeidAgent(Agent):
    """Agent that deidentifies PHI from the message."""

    def act(self, message: str, context: dict) -> tuple[str, dict]:
        # Import lazily to avoid heavy startup cost
        from utilities.storage.deidentifier import deidentify_text

        cleaned = deidentify_text(message)
        context["deidentified"] = cleaned
        return cleaned, context
