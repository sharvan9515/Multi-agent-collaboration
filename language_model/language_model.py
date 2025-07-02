# language_model/lm.py
import os
from dotenv import load_dotenv
import requests
from .base import LanguageModel

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
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")

print("🔑 GROQ API KEY:", GROQ_API_KEY[:10], "***")


class GroqLanguageModel(LanguageModel):
    """Language model wrapper around the Groq API."""

    def __init__(self, model: str = "llama3-8b-8192"):
        self.model = model

    def generate(self, messages: list) -> str:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            }
            body = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 512,
                "temperature": 0.2,
            }

            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            return answer.strip()
        except Exception as e:
            return f"❌ Error generating answer: {e}"


_default_lm = GroqLanguageModel()


def generate_answer(messages: list) -> str:
    """Compatibility helper that delegates to the default language model."""
    return _default_lm.generate(messages)
