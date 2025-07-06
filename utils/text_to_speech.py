import base64
import io

try:
    from gtts import gTTS
except Exception as exc:  # pragma: no cover - import-time
    raise ImportError(
        "gtts package is required for text-to-speech. Install it via `pip install gTTS`."
    ) from exc


def text_to_speech_base64(text: str, lang: str = "en") -> str:
    """Return base64-encoded MP3 audio for the given text."""
    buffer = io.BytesIO()
    gTTS(text=text, lang=lang).write_to_fp(buffer)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")

