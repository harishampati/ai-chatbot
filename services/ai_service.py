"""
ai_service.py – All OpenAI logic lives here.
Keeps app.py clean and makes it easy to swap AI providers later.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = (
    "You are a helpful, friendly, and concise AI assistant. "
    "Answer questions clearly and accurately. "
    "If you don't know something, say so honestly."
)


def get_ai_response(conversation_history: list) -> str:
    """
    Send the full conversation history to OpenAI and return the assistant reply.
    The client is created here (not at import time) so a missing key gives a
    clean error message instead of crashing on startup.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set. "
            "Create a .env file in the chatbot folder with: OPENAI_API_KEY=sk-..."
        )

    client = OpenAI(api_key=api_key)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        raise RuntimeError(f"OpenAI API error: {exc}") from exc
