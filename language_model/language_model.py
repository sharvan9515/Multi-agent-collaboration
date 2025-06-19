# language_model/lm.py
import os
from openai import OpenAI
from dotenv import load_dotenv
import requests

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

GROQ_MODEL = "llama3-8b-8192"  # Or try mixtral-8x7b-32768 or gemma-7b-it

def generate_answer(messages: list) -> str:
    """Call Groq API to generate an answer given a prompt (context + question)."""
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": GROQ_MODEL,
            "messages": messages,
            "max_tokens": 512,
            "temperature": 0.2
        }

        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        return answer.strip()
    except Exception as e:
        return f"❌ Error generating answer: {e}"
