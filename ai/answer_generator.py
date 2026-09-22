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
        api_key=st.secrets["GROQ_API_KEY"],
        timeout=30.0,
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

    # Keep the evidence reasonably small.
    # This prevents very large government webpages
    # from overwhelming the AI request.
    max_evidence_chars = 30000

    if len(evidence) > max_evidence_chars:
        evidence = evidence[:max_evidence_chars]

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

        answer = response.choices[
            0
        ].message.content

        if not answer:
            return (
                "The official sources were found, "
                "but the AI could not generate an answer. "
                "Please try again."
            )

        return answer.strip()

    except RateLimitError:

        return (
            "The AI answer service has temporarily "
            "reached its usage limit. The official "
            "government sources were found, but the "
            "answer could not be generated right now. "
            "Please try again later."
        )

    except Exception as exc:

        error_text = str(exc).lower()

        if (
            "timeout" in error_text
            or "timed out" in error_text
        ):

            return (
                "The AI request took too long to complete. "
                "The official government sources were found. "
                "Please try the question again."
            )

        return (
            "The AI answer could not be generated at this "
            "time. The official government sources were "
            "found. Please try again."
        )
