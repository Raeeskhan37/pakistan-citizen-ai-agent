from groq import Groq
from groq import RateLimitError

import streamlit as st

from ai.prompts import (
    build_system_prompt,
    build_user_prompt,
)

from config.settings import GROQ_MODEL


# ============================================================
# GROQ CLIENT
# ============================================================

def get_client():

    return Groq(
        api_key=st.secrets["GROQ_API_KEY"],
        timeout=45.0,
    )


# ============================================================
# SAUDI WORK VISA DETECTION
# ============================================================

def is_saudi_work_visa_vaccination_question(
    question,
    department,
):

    if department != "Vaccination for Travelling Abroad":
        return False

    q = (
        question or ""
    ).lower()

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

    return (
        any(
            term in q
            for term in saudi_terms
        )
        and
        any(
            term in q
            for term in work_terms
        )
        and
        any(
            term in q
            for term in vaccination_terms
        )
    )


# ============================================================
# SAUDI GUARDRAIL
# ============================================================

def add_work_visa_guardrail(
    system_prompt,
):

    guardrail = """
CRITICAL EVIDENCE RULE — ORDINARY SAUDI WORK VISA

If the user's question concerns an ordinary Saudi
employment/work visa, do not treat it as Hajj or Umrah.

Do not state that a specific vaccine is mandatory unless
the supplied CURRENT official evidence explicitly proves
that requirement.

Do not convert "can get vaccinated" into "must be vaccinated".

Do not transfer Hajj or Umrah requirements to ordinary
employment visas.

Answer only from the supplied official evidence.
"""

    return (
        system_prompt
        + "\n\n"
        + guardrail
    )


# ============================================================
# BIRTH CERTIFICATE FALLBACK
# ============================================================

def build_birth_fallback(
    question,
    evidence,
    language,
):

    q = (
        question or ""
    ).lower()

    # --------------------------------------------------------
    # Specific jurisdiction
    # --------------------------------------------------------

    if "sindh" in q:

        if language in ("Urdu", "اردو"):
            return """
سندھ میں پیدائش کا نیا سرٹیفکیٹ حاصل کرنے کے لیے
متعلقہ مقامی حکومت / یونین کونسل کے ذریعے پیدائش
کی رجسٹریشن کرائی جاتی ہے۔

حکومت سندھ نے پیدائش، وفات، شادی اور طلاق کی
رجسٹریشن کے لیے CRMS کے ذریعے آن لائن سہولت بھی
متعارف کرائی ہے۔

درخواست دینے سے پہلے متعلقہ یونین کونسل یا سندھ
کے سرکاری CRMS نظام سے موجودہ طریقہ کار کی تصدیق کریں۔
"""

        return """
For a new birth certificate in Sindh, birth registration
is handled through the relevant local-government /
Union Council authority.

The Government of Sindh has also announced online
birth registration through the provincial CRMS system.

Before applying, confirm the current procedure with the
relevant Union Council/local-government authority or the
official Sindh CRMS service.
"""

    if "balochistan" in q:

        if language in ("Urdu", "اردو"):
            return """
بلوچستان میں پیدائش کا نیا سرٹیفکیٹ متعلقہ لوکل
کونسل / یونین کونسل کے ذریعے حاصل کیا جا سکتا ہے۔

بلوچستان لوکل گورنمنٹ اینڈ رورل ڈویلپمنٹ ڈیپارٹمنٹ
نے پیدائش کے سرٹیفکیٹ کی سرکاری سروس اور CRMS /
PakID کے ذریعے آن لائن رجسٹریشن کی سہولت بھی بیان
کی ہے۔

درخواست دینے سے پہلے متعلقہ لوکل کونسل یا سرکاری
CRMS سروس سے موجودہ طریقہ کار کی تصدیق کریں۔
"""

        return """
For a new birth certificate in Balochistan, birth
registration is handled through the relevant Local
Council / Union Council.

The Balochistan Local Government & Rural Development
Department provides a Birth Certificate service and has
also announced online registration through CRMS/PakID.

Confirm the current procedure with the relevant Local
Council or the official CRMS service before applying.
"""

    if "kp" in q or "kpk" in q or "khyber pakhtunkhwa" in q:

        if language in ("Urdu", "اردو"):
            return """
خیبر پختونخوا میں پیدائش کا سرٹیفکیٹ متعلقہ
ویلج کونسل یا نیبرہڈ کونسل کے ذریعے رجسٹر کیا جاتا ہے۔

عام طور پر Form-A، والدین یا سرپرست کے CNIC/پاسپورٹ
کی تصدیق شدہ کاپی اور دستیاب ہونے کی صورت میں
ہسپتال کا برتھ سرٹیفکیٹ، ویکسینیشن کارڈ یا اسکول
سرٹیفکیٹ درکار ہوتا ہے۔
"""

        return """
In Khyber Pakhtunkhwa, birth registration is handled
through the relevant Village Council or Neighbourhood
Council.

The official KP guidance lists Form-A, an attested CNIC
or passport copy of the parent(s)/guardian, and where
available a health-facility birth certificate,
immunization card or school certificate.
"""

    if "lahore" in q or "punjab" in q:

        if language in ("Urdu", "اردو"):
            return """
پنجاب، بشمول لاہور، میں پیدائش کی رجسٹریشن متعلقہ
یونین کونسل کے ذریعے کی جاتی ہے۔

پنجاب کی سرکاری رہنمائی کے مطابق والدین کے شناختی
کارڈز کی نقول، پیدائش کا ثبوت اور مقررہ یونین کونسل
فارم درکار ہوتا ہے۔ معمول کی رجسٹریشن اور تاخیر سے
رجسٹریشن کے لیے الگ طریقہ کار اور مدت مقرر ہے۔
"""

        return """
In Punjab, including Lahore, birth registration is
handled through the relevant Union Council.

Punjab's official guidance lists parents' CNIC copies,
proof of birth and the prescribed Union Council form.
Normal and late registration have different procedures
and processing periods.
"""

    # --------------------------------------------------------
    # General Pakistan answer
    # --------------------------------------------------------

    if language in ("Urdu", "اردو"):

        return """
پاکستان میں نیا پیدائش سرٹیفکیٹ حاصل کرنے کا طریقہ
صوبے یا علاقے کے مطابق مختلف ہو سکتا ہے۔

پیدائش کی سول رجسٹریشن عام طور پر متعلقہ یونین کونسل،
لوکل کونسل، میونسپل کمیٹی یا متعلقہ مقامی حکومت کے
ذریعے ہوتی ہے۔

اہم بات یہ ہے کہ NADRA کا CRC / B-Form پیدائش کے
سول سرٹیفکیٹ سے الگ دستاویز ہے۔

درخواست دینے سے پہلے اپنے علاقے کی متعلقہ مقامی
حکومت یا یونین کونسل سے موجودہ طریقہ کار، مطلوبہ
دستاویزات، فیس اور آن لائن سہولت کی تصدیق کریں۔
"""

    return """
In Pakistan, the procedure for obtaining a new birth
certificate varies by province and territory.

Civil birth registration is generally handled through
the relevant Union Council, Local Council, Municipal
Committee or other local-government authority.

Important: a NADRA CRC/B-Form is a separate identity
document and should not be treated as a replacement for
the civil birth certificate.

Before applying, confirm the current procedure,
documents, fees and any online option with the relevant
local-government authority in your area.
"""


# ============================================================
# MAIN ANSWER GENERATOR
# ============================================================

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

    if is_saudi_work_visa_vaccination_question(
        question=question,
        department=department,
    ):
        system_prompt = add_work_visa_guardrail(
            system_prompt
        )

    # --------------------------------------------------------
    # IMPORTANT:
    # Keep evidence controlled so large multi-jurisdiction
    # searches do not cause Groq failures.
    # --------------------------------------------------------

    max_evidence_chars = 18000

    if len(evidence) > max_evidence_chars:

        evidence = (
            evidence[:max_evidence_chars]
            + "\n\n[Additional evidence omitted for "
              "answer-generation efficiency.]"
        )

    user_prompt = build_user_prompt(
        question=question,
        department=department,
        evidence=evidence,
        language=language,
    )

    # --------------------------------------------------------
    # Generate
    # --------------------------------------------------------

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
            max_tokens=1200,
        )

        answer = (
            response.choices[0]
            .message.content
        )

        if answer:

            return answer.strip()

        # ----------------------------------------------------
        # Empty response
        # ----------------------------------------------------

        if (
            department
            == "Union Council / Local Government"
            and any(
                term in (
                    question or ""
                ).lower()
                for term in [
                    "birth",
                    "birth certificate",
                    "birth registration",
                    "پیدائش",
                ]
            )
        ):

            return build_birth_fallback(
                question,
                evidence,
                language,
            )

        return (
            "The official government sources were found, "
            "but the AI returned an empty answer. "
            "Please try the question again."
        )

    except RateLimitError:

        # ----------------------------------------------------
        # Important: do not leave the citizen without an answer
        # when official evidence already exists.
        # ----------------------------------------------------

        if (
            department
            == "Union Council / Local Government"
            and any(
                term in (
                    question or ""
                ).lower()
                for term in [
                    "birth",
                    "birth certificate",
                    "birth registration",
                    "پیدائش",
                ]
            )
        ):

            return build_birth_fallback(
                question,
                evidence,
                language,
            )

        return (
            "The AI answer service has temporarily "
            "reached its usage limit. The official "
            "government sources were found. Please "
            "try again later."
        )

    except Exception as exc:

        error_text = str(
            exc
        ).lower()

        # ----------------------------------------------------
        # Birth certificate fallback
        # ----------------------------------------------------

        if (
            department
            == "Union Council / Local Government"
            and any(
                term in (
                    question or ""
                ).lower()
                for term in [
                    "birth",
                    "birth certificate",
                    "birth registration",
                    "newborn",
                    "پیدائش",
                ]
            )
        ):

            return build_birth_fallback(
                question,
                evidence,
                language,
            )

        # ----------------------------------------------------
        # Timeout
        # ----------------------------------------------------

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
