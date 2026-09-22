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

def is_saudi_work_visa_vaccination_question(
question,
department,
):
"""
Detect ordinary Saudi employment/work-visa
vaccination questions.

This is intentionally separate from Hajj/Umrah.
"""

if department != "Vaccination for Travelling Abroad":
    return False

q = (question or "").lower()

saudi_terms = [
    "saudi",
    "saudia",
    "saudi arabia",
    "سعودی",
]

work_terms = [
    "work visa",
    "employment visa",
    "employment",
    "work permit",
    "worker",
    "working",
    "job visa",
    "iqama",
    "job",
    "ملازمت",
    "ورک ویزا",
    "اقامہ",
]

vaccination_terms = [
    "vaccine",
    "vaccination",
    "vaccinated",
    "immunization",
    "immunisation",
    "ویکسین",
    "ویکسینیشن",
]

has_saudi = any(
    term in q
    for term in saudi_terms
)

has_work = any(
    term in q
    for term in work_terms
)

has_vaccination = any(
    term in q
    for term in vaccination_terms
)

return (
    has_saudi
    and has_work
    and has_vaccination
)

def add_work_visa_guardrail(
system_prompt,
):
"""
Prevent the model from converting historical
vaccination-availability guidance into a current
mandatory vaccination requirement.
"""

guardrail = """

CRITICAL EVIDENCE RULE — ORDINARY SAUDI WORK VISA

If the user's question concerns an ORDINARY Saudi
employment/work visa, do NOT treat it as Hajj or Umrah.

Do NOT state that a specific vaccine is mandatory unless
the supplied evidence explicitly establishes that the
specific vaccine is currently mandatory for ordinary Saudi
employment/work-visa travellers.

IMPORTANT:

The Government of Pakistan / NCOC document about Pakistanis
working abroad on work visas says eligible people with a
work visa or iqama CAN GET VACCINATED.

"CAN GET VACCINATED" does NOT mean:

"MUST BE VACCINATED."

Do not convert permission, availability, eligibility,
procedure, recommendation, or historical policy into a
mandatory requirement.

Do NOT claim that Pfizer-BioNTech is currently mandatory
for every ordinary Saudi work-visa traveller unless a
CURRENT authoritative source explicitly says so.

Do NOT use a historical COVID/Pfizer policy as proof of a
CURRENT mandatory vaccination requirement.

Do NOT claim that Saudi Arabia currently rejects Chinese
vaccines unless the supplied CURRENT official evidence
explicitly establishes that fact.

Distinguish carefully between:

1. Ordinary employment/work visa
2. Hajj
3. Umrah
4. Seasonal Hajj employment

Hajj and Umrah may have separate vaccination requirements.
Those requirements must not be transferred to ordinary
employment visas.

For an ordinary Saudi employment visa, current official
evidence may establish medical examination, health
certification, or screening without establishing a
mandatory vaccination.

If the supplied official evidence does not establish a
specific mandatory vaccination requirement, say so clearly.

Preferred wording:

"No specific vaccination requirement for an ordinary
Saudi employment visa could be verified from the current
official sources reviewed. However, Saudi employment visa
applicants are subject to the required medical/health
screening procedures. Requirements can vary by visa
category and current Saudi regulations."

Never invent a vaccination requirement.
Never turn "can get vaccinated" into "must be vaccinated."
"""

return (
    system_prompt
    + "\n\n"
    + guardrail
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

# --------------------------------------------------------
# SPECIAL SAFETY GUARDRAIL
# --------------------------------------------------------
#
# Ordinary Saudi work-visa vaccination questions require
# extra protection because historical vaccination policy
# can easily be misinterpreted as a current mandatory rule.
#
if is_saudi_work_visa_vaccination_question(
    question=question,
    department=department,
):
    system_prompt = add_work_visa_guardrail(
        system_prompt
    )

# --------------------------------------------------------
# Keep evidence reasonably small.
# --------------------------------------------------------

max_evidence_chars = 30000

if len(evidence) > max_evidence_chars:
    evidence = evidence[:max_evidence_chars]

user_prompt = build_user_prompt(
    question=question,
    department=department,
    evidence=evidence,
    language=language,
)

# --------------------------------------------------------
# Add a direct instruction to the USER prompt as well.
#
# This gives the model the rule immediately before the
# evidence, reducing the chance that an old source will
# override the safety instruction.
# --------------------------------------------------------

if is_saudi_work_visa_vaccination_question(
    question=question,
    department=department,
):
    user_prompt = (
        """

SPECIAL INSTRUCTION FOR THIS QUESTION:

This is an ordinary Saudi employment/work-visa
vaccination question.

Before answering, follow these rules:

- Do not treat Hajj or Umrah requirements as ordinary
  employment-visa requirements.
- Do not claim Pfizer is mandatory unless a CURRENT official
  source explicitly proves it.
- Do not interpret "can get vaccinated" as "must be
  vaccinated."
- Do not use historical COVID vaccination policy as proof of
  a current mandatory requirement.
- Do not claim Chinese vaccines are rejected unless current
  official evidence explicitly proves it.
- If no current official source establishes a mandatory
  vaccine, clearly say that no specific mandatory vaccination
  requirement could be verified.

Answer only from the supplied official evidence.

"""
+ user_prompt
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

    answer = answer.strip()

    # ----------------------------------------------------
    # FINAL OUTPUT GUARD
    #
    # If the model nevertheless produces the known
    # dangerous interpretation, replace it with a safe
    # evidence-based answer.
    # ----------------------------------------------------

    if is_saudi_work_visa_vaccination_question(
        question=question,
        department=department,
    ):

        answer_lower = answer.lower()

        dangerous_phrases = [
            "must be vaccinated",
            "must receive a vaccine",
            "mandatory vaccination",
            "mandatory vaccine",
            "you need to be vaccinated",
            "you are required to be vaccinated",
            "pfizer is mandatory",
            "pfizer-biontech is mandatory",
            "pfizer is required",
            "pfizer-biontech is required",
            "need to receive pfizer",
            "required to receive pfizer",
            "chinese vaccines are not accepted",
            "china vaccines are not accepted",
            "chinese-manufactured vaccines are not accepted",
        ]

        if any(
            phrase in answer_lower
            for phrase in dangerous_phrases
        ):
            if language == "Urdu":
                return (
                    "موجودہ سرکاری ذرائع کی بنیاد پر "
                    "عام سعودی ورک یا ایمپلائمنٹ ویزا "
                    "کے لیے کسی مخصوص ویکسین کی لازمی "
                    "ضرورت کی تصدیق نہیں ہو سکی۔ "
                    "البتہ سعودی ورک ویزا کے لیے مطلوبہ "
                    "میڈیکل اور ہیلتھ اسکریننگ کے مراحل "
                    "ہوتے ہیں۔ ویزا کی قسم اور موجودہ "
                    "سعودی قواعد کے مطابق تقاضے مختلف "
                    "ہو سکتے ہیں، اس لیے سفر سے پہلے "
                    "متعلقہ سعودی اور پاکستانی سرکاری "
                    "حکام سے موجودہ تقاضوں کی تصدیق کریں۔"
                )

            return (
                "No specific vaccination requirement for "
                "an ordinary Saudi employment/work visa "
                "could be verified from the current "
                "official sources reviewed. However, "
                "Saudi employment visa applicants are "
                "subject to the required medical and "
                "health screening procedures. Requirements "
                "can vary by visa category and current "
                "Saudi regulations, so the traveller "
                "should confirm the current requirements "
                "with the relevant Saudi and Pakistani "
                "authorities before travel."
            )

    return answer

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
        "found. Please try the question again."
    )
