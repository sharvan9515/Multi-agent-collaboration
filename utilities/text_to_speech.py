import base64
import io


def text_to_speech_base64(text: str, lang: str = "en") -> str:
    """Return base64-encoded MP3 audio for the given text."""
    from gtts import gTTS

    buffer = io.BytesIO()
    gTTS(text=text, lang=lang).write_to_fp(buffer)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")

