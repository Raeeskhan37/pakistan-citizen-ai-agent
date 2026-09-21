import os

from groq import Groq

from config.settings import GROQ_MODEL


def get_groq_client():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    return Groq(api_key=api_key)


def generate_text(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.1,
):

    client = get_groq_client()

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    return response.choices[0].message.content
