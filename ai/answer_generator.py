from groq import Groq

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
    )

    return response.choices[0].message.content.strip()
