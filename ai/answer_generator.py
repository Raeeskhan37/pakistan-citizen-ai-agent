from groq import Groq
from groq import RateLimitError

from ai.prompts import (
    build_system_prompt,
    build_user_prompt,
)

from config.settings import GROQ_MODEL


def get_client():
    import streamlit as st

    return Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )


def generate_answer(
    question,
    department,
    evidence,
    language,
):
    client = get_client()

    system_prompt = build_system_prompt(
        department=department,
        language=language,
    )

    user_prompt = build_user_prompt(
        question=question,
        department=department,
        evidence=evidence,
        language=language,
    )

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
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
            temperature=0.1,
            max_tokens=1000,
        )

        return response.choices[0].message.content.strip()

    except RateLimitError:
        return (
            "The AI answer service has temporarily reached "
            "its usage limit. The official government sources "
            "were successfully searched, but the final AI "
            "response could not be generated right now. "
            "Please try again later."
        )

    except Exception:
        return (
            "The AI answer could not be generated at this time. "
            "Please try again later."
        )
