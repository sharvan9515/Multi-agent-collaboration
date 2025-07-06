# language_model/lm.py
import os
import logging
try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    def load_dotenv(*args, **kwargs):
        return False
try:
    import requests
except ImportError:  # pragma: no cover - optional dependency
    requests = None
from .base import LanguageModel

logger = logging.getLogger(__name__)

# load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
# if not api_key:
#     raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in a .env file.")
# # Load API key from .env
# client = OpenAI(api_key=api_key)
# print("🔑 OPENAI API KEY:", os.getenv("OPENAI_API_KEY")[:10], "***")


# OPENAI_MODEL = "gpt-3.5-turbo"

# def generate_answer(prompt: str) -> str:
#     """Call OpenAI API to generate an answer given a prompt (context + question)."""
#     try:
#         response = client.chat.completions.create(
#             model=OPENAI_MODEL,
#             messages=[
#                 {"role": "system", "content": "You are a helpful medical insurance claims assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=512,
#             temperature=0.2
#         )
#         # ✅ Access message content correctly
#         answer = response.choices[0].message.content
#         return answer.strip()
#     except Exception as e:
#         return f"Error generating answer: {e}"
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    logger.debug("GROQ API key loaded from environment variables")
else:
    logger.warning(
        "GROQ_API_KEY not found. Falling back to local echo language model."
    )


class GroqLanguageModel(LanguageModel):
    """Language model wrapper around the Groq API."""

    def __init__(self, model: str = "llama3-8b-8192", max_tokens: int = 200):
        self.model = model
        self.max_tokens = max_tokens

    def generate(self, messages: list) -> str:
        if requests is None:
            raise RuntimeError("requests package is required for Groq API calls")
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            }
            body = {
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": 0.2,
            }

            response = requests.post(url, headers=headers, json=body, timeout=10)
            response.raise_for_status()
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            return answer.strip()
        except Exception as e:
            logger.error("Groq API call failed: %s", e)
            raise


class EchoLanguageModel(LanguageModel):
    """Very simple offline language model that echoes the last user message."""

    def generate(self, messages: list) -> str:
        user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        return (
            "🤖 (offline mode) I'm unable to reach the language model service. "
            f"You said: '{user_msg}'."
        )


if GROQ_API_KEY:
    _default_lm = GroqLanguageModel()
else:
    _default_lm = EchoLanguageModel()


def generate_answer(messages: list) -> str:
    """Compatibility helper that delegates to the default language model."""
    try:
        return _default_lm.generate(messages)
    except Exception:
        logger.warning("Falling back to echo model due to API failure")
        echo_lm = EchoLanguageModel()
        return echo_lm.generate(messages)
