import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def ask_ai(message, memories, premium=False):

    model_name = (
        "llama-3.3-70b-versatile"
        if premium
        else "llama3-8b-8192"
    )

    messages = [
        {
            "role": "system",
            "content": (
                "AUREVON isimli premium AI asistansın. "
                "Karizmatik, akıllı ve yardımcı cevaplar ver."
            )
        }
    ]

    messages.extend(memories)

    messages.append(
        {
            "role": "user",
            "content": message
        }
    )

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model_name,
        "messages": messages
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=60
    )

    result = response.json()

    return result["choices"][0]["message"]["content"]
