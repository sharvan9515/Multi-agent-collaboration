from .base import Agent
from utilities.text_to_speech import text_to_speech_base64


class TTSAgent(Agent):
    """Agent that converts text replies into speech."""

    def act(self, message: str, context: dict) -> tuple[str, dict]:
        """Generate base64 audio from the message and store it in context."""
        audio = text_to_speech_base64(message)
        context["audio"] = audio
        return message, context
