from datetime import datetime

from ai.answer_generator import generate_answer
from agent.researcher import research_question
from agent.router import detect_department
from agent.verifier import verify_sources
from rag.nadra_retriever import build_nadra_evidence


# ============================================================
# WEB EVIDENCE FORMATTER
# ============================================================

def format_web_evidence(sources):

    if not sources:
        return "No authoritative web evidence was retrieved."

    evidence_parts = []

    for index, source in enumerate(sources, start=1):

        page_text = source.get("page_text", "")

        if not page_text:
            page_text = source.get("snippet", "")

        evidence_parts.append(
            f"""
WEB SOURCE {index}

Title:
{source.get("title", "")}

URL:
{source.get("url", "")}

Official government source:
{source.get("official", False)}

Information from official government page:
{page_text}
"""
        )

    return "\n".join(evidence_parts)


# ============================================================
# FAST PILGRIM QUESTION DETECTION
# ============================================================

def is_pilgrim_question(question, selected_department):

    if selected_department != "Vaccination for Travelling Abroad":
        return False

    q = (question or "").strip().lower()
    print("PILGRIM DEBUG QUESTION:", repr(q))
    pilgrim_terms = [
        "hajj",
        "haj",
        "umrah",
        "umra",
        "حج",
        "عمرہ",
    ]

    return any(term in q for term in pilgrim_terms)


def is_umrah_question(question):

    q = (question or "").strip().lower()

    return any(
        term in q
        for term in [
            "umrah",
            "umra",
            "عمرہ",
        ]
    )


# ============================================================
# OFFICIAL HAJJ SOURCES
# ============================================================

HAJJ_SOURCES = [
    {
        "title": "Saudi MOH — Health Requirements for Hajj 1447H (2026)",
        "url": (
            "https://www.moh.gov.sa/"
            "HealthAwareness/Pilgrims-Health/"
            "Documents/Hajj-Health-Requirements-English-language.pdf"
        ),
        "domain": "moh.gov.sa",
        "official": True,
    },
    {
        "title": "Saudi MOH — Hajj 1447H Vaccination Campaign",
        "url": (
            "https://www.moh.gov.sa/en/ministry/"
            "mediacenter/news/pages/"
            "news-2026-02-27-001.aspx"
        ),
        "domain": "moh.gov.sa",
        "official": True,
    },
    {
        "title": (
            "Pakistan Ministry of Religious Affairs — "
            "Saudi Government Health Instructions for Hajj 2026"
        ),
        "url": (
            "https://www.mora.gov.pk/NewsDetail/"
            "N2ExNTM0OTItNjNlMC00YTU0LWE4N2Mt"
            "MzcxNjI1Yjk4Zjk2"
        ),
        "domain": "mora.gov.pk",
        "official": True,
    },
]


# ============================================================
# OFFICIAL UMRAH SOURCES
# ============================================================

UMRAH_SOURCES = [
    {
        "title": (
            "Saudi MOH — Health Requirements and "
            "Recommendations for Travelers to Saudi Arabia "
            "for Umrah - 1447H (2026)"
        ),
        "url": (
            "https://www.moh.gov.sa/"
            "en/HealthAwareness/Pilgrims-Health/"
            "Documents/Health-Regulations-Umrah-EN.pdf"
        ),
        "domain": "moh.gov.sa",
        "official": True,
    },
    {
        "title": "Saudi MOH — Pilgrim's Health",
        "url": (
            "https://www.moh.gov.sa/"
            "en/healthawareness/pilgrims-health/"
            "pages/default.aspx"
        ),
        "domain": "moh.gov.sa",
        "official": True,
    },
]


# ============================================================
# HAJJ ANSWER
# ============================================================

def build_hajj_answer(language):

    if language == "اردو":

        return """
### حج 2026 کے لیے ویکسینیشن

سعودی وزارتِ صحت کی حج 1447ھ / 2026 کی سرکاری
Health Requirements کے مطابق:

**میننجوکوکل ویکسین**

میننجوکوکل ویکسین ان عازمین کے لیے لازمی ہے جنہوں نے
گزشتہ پانچ سال کے اندر یہ ویکسین نہیں لگوائی۔

سعودی رہنمائی کے مطابق ویکسین حج سے کم از کم 10 دن پہلے
لگائی جانی چاہیے۔

**پولیو**

پاکستان سے آنے والے مسافروں کے لیے سعودی حج صحت کی
سرکاری دستاویز میں پولیو سے متعلق مخصوص شرائط موجود ہیں۔

**فلو اور COVID-19**

سعودی وزارتِ صحت موسمی فلو اور COVID-19 ویکسینیشن کی
بھی سفارش کرتی ہے۔ انہیں ہر عازم کے لیے لازمی نہیں
کہا جانا چاہیے۔

یہ سعودی حج صحت کی ضروریات ہیں، پاکستان کی عمومی
ویکسینیشن پالیسی نہیں۔
"""

    return """
### Hajj 2026 Vaccination Requirements

According to the Saudi Ministry of Health's official
Hajj 1447H / 2026 health requirements:

**Meningococcal vaccine**

The meningococcal vaccine is mandatory for pilgrims who
have not received it within the previous five years.

Saudi guidance states that the vaccine should be received
at least 10 days before Hajj.

**Polio**

For travelers arriving from Pakistan, the Saudi Hajj
health requirements contain specific polio requirements.

The applicable vaccination and certificate requirements
should be followed according to the official Saudi document.

**Influenza and COVID-19**

Saudi MOH also recommends seasonal influenza and
COVID-19 vaccination. These should not automatically be
described as mandatory for every pilgrim.

These are Saudi Hajj health requirements, not Pakistan's
general vaccination policy.
"""


# ============================================================
# UMRAH ANSWER
# ============================================================

def build_umrah_answer(language):

    if language == "اردو":

        return """
### عمرہ 2026 کے لیے ویکسینیشن

سعودی وزارتِ صحت کی عمرہ 1447ھ / 2026 کی سرکاری
Health Requirements کے مطابق:

**1. میننجوکوکل ویکسین**

عمرہ کے لیے آنے والے مسافروں کے لیے منظور شدہ
میننجوکوکل ویکسین ضروری ہے۔

Conjugate ویکسین گزشتہ 5 سال کے اندر اور سعودی عرب
پہنچنے سے کم از کم 10 دن پہلے لگائی گئی ہونی چاہیے۔

Polysaccharide ویکسین گزشتہ 3 سال کے اندر اور سعودی
عرب پہنچنے سے کم از کم 10 دن پہلے لگائی گئی ہونی چاہیے۔

ویکسین کا نام اور لگانے کی تاریخ سرٹیفکیٹ پر واضح ہونی
چاہیے۔

**2. پولیو — پاکستان سے آنے والے مسافر**

سعودی وزارتِ صحت کی 1447ھ / 2026 کی عمرہ دستاویز میں
پاکستان سے آنے والے مسافروں کے لیے پولیو سے متعلق
مخصوص شرط موجود ہے۔

پاکستان سے عمرہ کے لیے آنے والے مسافروں کے لیے متعلقہ
پولیو ویکسین اور سرٹیفکیٹ کی شرط پوری کرنا ضروری ہے۔

**3. COVID-19**

کچھ مخصوص زیادہ خطرے والے عمرہ مسافروں کے لیے
COVID-19 ویکسینیشن یا immunity کا ثبوت درکار ہو سکتا ہے۔

یہ شرائط سعودی وزارتِ صحت کی سرکاری عمرہ
1447ھ / 2026 دستاویز کے مطابق ہیں۔
"""

    return """
### Umrah 2026 Vaccination Requirements

According to the Saudi Ministry of Health's official
Health Requirements for Umrah 1447H (2026):

**1. Meningococcal vaccine**

An approved meningococcal vaccine is required for
travelers intending to perform Umrah.

For a conjugate meningococcal vaccine, it must have been
received within the previous 5 years and at least 10 days
before arrival.

For a polysaccharide meningococcal vaccine, it must have
been received within the previous 3 years and at least
10 days before arrival.

The vaccine name and administration date should be clearly
shown on the vaccination certificate.

**2. Polio — travelers from Pakistan**

The Saudi Ministry of Health's 1447H / 2026 Umrah document
contains specific polio requirements for travelers arriving
from Pakistan.

The applicable polio vaccination and certificate
requirements should be completed before travel.

**3. COVID-19**

Certain higher-risk Umrah travelers may need proof of
COVID-19 vaccination or immunity.

These requirements are based on the Saudi Ministry of
Health's official Umrah 1447H / 2026 document.
"""


# ============================================================
# INSTANT PILGRIM RESPONSE
# ============================================================

def build_special_pilgrim_response(question, language):

    if is_umrah_question(question):

        answer = build_umrah_answer(language)
        sources = UMRAH_SOURCES

    else:

        answer = build_hajj_answer(language)
        sources = HAJJ_SOURCES

    return {
        "department": "Vaccination for Travelling Abroad",
        "jurisdiction": "Saudi Arabia",
        "answer": answer,
        "sources": sources,
        "source_count": len(sources),
        "official_source_count": len(sources),
        "research_attempts": 0,
        "rag_result_count": 0,
        "checked_date": datetime.now().strftime("%d %B %Y"),
        "warning": "",
    }


# ============================================================
# MAIN CITIZEN AGENT
# ============================================================

def ask_citizen_agent(
    question,
    selected_department,
    language,
):

    # ========================================================
    # CRITICAL FAST PATH
    # ========================================================
    #
    # Use SELECTED department directly.
    #
    # Do NOT call detect_department() first.
    # Do NOT call research_question().
    #
    # This makes Hajj/Umrah responses immediate.
    # ========================================================

    if is_pilgrim_question(
        question,
        selected_department,
    ):

        return build_special_pilgrim_response(
            question=question,
            language=language,
        )

    # ========================================================
    # NORMAL DEPARTMENT ROUTING
    # ========================================================

    department = detect_department(
        question,
        selected_department,
    )

    # ========================================================
    # NORMAL RESEARCH PIPELINE
    # ========================================================

    research = research_question(
        question,
        department,
        language,
    )

    web_sources = research.get(
        "sources",
        [],
    )

    rag_results = research.get(
        "rag_results",
        [],
    )

    jurisdiction = research.get(
        "jurisdiction"
    )

    verification = verify_sources(
        web_sources
    )

    verified_sources = verification.get(
        "verified",
        [],
    )

    # ========================================================
    # NADRA RAG
    # ========================================================

    if department == "NADRA":

        policy_evidence = build_nadra_evidence(
            rag_results
        )

    else:

        policy_evidence = (
            "No department-specific "
            "policy evidence was used."
        )

    # ========================================================
    # WEB EVIDENCE
    # ========================================================

    web_evidence = format_web_evidence(
        verified_sources[:5]
    )

    jurisdiction_text = (
        jurisdiction
        if jurisdiction
        else "Not specified"
    )

    combined_evidence = f"""
============================================================
GOVERNMENT POLICY EVIDENCE
============================================================

Department:
{department}

Jurisdiction:
{jurisdiction_text}

{policy_evidence}


============================================================
VERIFIED OFFICIAL WEB EVIDENCE
============================================================

{web_evidence}
"""

    has_policy_evidence = bool(
        rag_results
    )

    has_web_evidence = bool(
        verified_sources
    )

    if (
        not has_policy_evidence
        and not has_web_evidence
    ):

        answer = (
            "I could not verify this information "
            "from an authoritative government source."
        )

    else:

        answer = generate_answer(
            question=question,
            department=department,
            evidence=combined_evidence,
            language=language,
        )

    official_count = sum(
        1
        for source in verified_sources
        if source.get("official")
    )

    return {
        "department": department,
        "jurisdiction": jurisdiction,
        "answer": answer,
        "sources": verified_sources[:5],
        "source_count": len(
            verified_sources
        ),
        "official_source_count": official_count,
        "research_attempts": research.get(
            "attempts",
            1,
        ),
        "rag_result_count": len(
            rag_results
        ),
        "checked_date": datetime.now().strftime(
            "%d %B %Y"
        ),
        "warning": verification.get(
            "warning",
            "",
        ),
    }
