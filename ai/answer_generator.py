from ai.groq_client import generate_text
from ai.prompts import SYSTEM_PROMPT, build_user_prompt


def generate_answer(
    question,
    department,
    evidence,
    language,
):

    prompt = build_user_prompt(
        question=question,
        department=department,
        evidence=evidence,
        language=language,
    )

    return generate_text(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
        temperature=0.1,
    )
