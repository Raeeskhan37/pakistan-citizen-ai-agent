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

    for index, source in enumerate(
        sources,
        start=1,
    ):

        page_text = source.get(
            "page_text",
            "",
        )

        if not page_text:
            page_text = source.get(
                "snippet",
                "",
            )

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

    return "\n".join(
        evidence_parts
    )


# ============================================================
# DETECT HAJJ / UMRAH
# ============================================================

def is_hajj_or_umrah_question(
    question,
    department,
):
    """
    Identify Hajj / Umrah questions only for the
    Vaccination department.

    This special path does NOT affect:
    - NADRA
    - Passport
    - Protector
    - other departments
    """

    if (
        department
        != "Vaccination for Travelling Abroad"
    ):
        return False

    question_lower = question.lower()

    return any(
        term in question_lower
        for term in [
            "hajj",
            "haj",
            "umrah",
            "umra",
        ]
    )


# ============================================================
# HAJJ 2026 FINAL ANSWER
# ============================================================

def build_hajj_answer(
    question,
    language,
):
    """
    Final answer for Hajj / Umrah vaccination questions.

    This uses only documented official information.

    Important:
    Saudi requirements are identified as Saudi requirements.
    They are NOT presented as Pakistani domestic policy.
    """

    if language == "اردو":

        return """
### حج 2026 کے لیے ویکسینیشن

حج 1447ھ / 2026 کے لیے سعودی عرب کی وزارتِ صحت نے
سرکاری صحت کی ضروریات جاری کی ہیں۔

**میننجوکوکل (Meningococcal / Neisseria) ویکسین**

سعودی وزارتِ صحت کے مطابق یہ ویکسین ان تمام عازمین کے
لیے لازمی ہے جنہوں نے گزشتہ پانچ سال کے اندر یہ ویکسین
نہیں لگوائی۔

**پولیو**

سعودی وزارتِ صحت کی حج 2026 کی سرکاری Health Requirements
میں پولیو سے متعلق مخصوص ممالک اور داخلے کی صحت کی
ضروریات بھی بیان کی گئی ہیں۔ پاکستان سے آنے والے مسافروں
کے لیے متعلقہ پولیو شرائط اسی سرکاری دستاویز کے مطابق
دیکھی جانی چاہئیں۔

**دیگر ویکسینز**

سعودی وزارتِ صحت نے 2026 کے لیے موسمی فلو اور COVID-19
ویکسینیشن کی بھی سفارش کی ہے، لیکن ہر تجویز کردہ ویکسین
کو لازمی قرار نہیں دیا گیا۔

### سرٹیفکیٹ کے بارے میں

حتمی ویکسینیشن/صحت کی دستاویزات کے لیے:

1. سعودی وزارتِ صحت کی Hajj 1447/2026 Health Requirements
2. پاکستان وزارتِ مذہبی امور کی
   "Saudi Government Health Instructions for Hajj - 2026"

کو بنیادی سرکاری ذرائع سمجھا جائے۔

یہ معلومات سعودی حج صحت کی ضروریات سے متعلق ہیں؛ انہیں
پاکستان کی عمومی ویکسینیشن پالیسی نہیں سمجھنا چاہیے۔
"""

    return """
### Hajj 2026 Vaccination Requirements

For Hajj 1447H / 2026, the Saudi Ministry of Health
published official health requirements for pilgrims.

**Meningococcal (Neisseria) vaccine**

According to the Saudi Ministry of Health, this vaccine is
mandatory for pilgrims who have not received it within the
previous five years. Vaccination status can be verified
through the Saudi Sehhaty system.

**Polio**

The Saudi Ministry of Health's official Hajj 2026 Health
Requirements also specify polio-related requirements for
travellers from relevant countries. For pilgrims travelling
from Pakistan, the applicable polio requirements should be
followed according to that official Saudi document.

**Other vaccines**

The Saudi Ministry of Health also recommended seasonal
influenza and COVID-19 vaccination for the 2026 Hajj season.
These recommendations should not automatically be treated
as mandatory requirements.

### What certificate should I have?

For the exact vaccination/health documentation applicable
to a Pakistani Hajj pilgrim, the authoritative references
are:

1. Saudi Ministry of Health — Health Requirements for
   Hajj 1447H (2026)
2. Pakistan Ministry of Religious Affairs —
   "Saudi Government Health Instructions for Hajj - 2026"

These are Saudi Hajj health requirements and should not be
described as Pakistan's general vaccination policy.
"""


# ============================================================
# MAIN CITIZEN AGENT
# ============================================================

def ask_citizen_agent(
    question,
    selected_department,
    language,
):

    # --------------------------------------------------------
    # Department detection
    # --------------------------------------------------------

    department = detect_department(
        question,
        selected_department,
    )

    # --------------------------------------------------------
    # Research
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Verify official sources
    # --------------------------------------------------------

    verification = verify_sources(
        web_sources
    )

    verified_sources = verification.get(
        "verified",
        [],
    )

    # ========================================================
    # SPECIAL HAJJ / UMRAH FINAL-STAGE PATH
    # ========================================================
    #
    # IMPORTANT:
    #
    # This is the ONLY new final-stage branch.
    #
    # NADRA remains unchanged.
    # Passport remains unchanged.
    # Protector remains unchanged.
    # All other departments remain unchanged.
    #
    # ========================================================

    hajj_question = is_hajj_or_umrah_question(
        question,
        department,
    )

    if hajj_question:

        answer = build_hajj_answer(
            question=question,
            language=language,
        )

        # ----------------------------------------------------
        # Keep only official sources.
        # ----------------------------------------------------

        official_sources = []

        for source in web_sources:

            if not isinstance(
                source,
                dict,
            ):
                continue

            if source.get(
                "official"
            ) is True:

                official_sources.append(
                    source
                )

        # ----------------------------------------------------
        # Remove duplicate URLs
        # ----------------------------------------------------

        unique_sources = []

        seen_urls = set()

        for source in official_sources:

            url = (
                source.get(
                    "url",
                    "",
                )
                or ""
            ).strip()

            if not url:
                continue

            if url in seen_urls:
                continue

            seen_urls.add(url)

            unique_sources.append(
                source
            )

        return {
            "department": department,
            "jurisdiction": jurisdiction,
            "answer": answer,
            "sources": unique_sources[:5],
            "source_count": len(
                unique_sources
            ),
            "official_source_count": len(
                unique_sources
            ),
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
            "warning": "",
        }

    # ========================================================
    # EXISTING GENERAL PIPELINE
    # ========================================================
    #
    # Everything below remains the normal pipeline.
    #
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
        if source.get(
            "official"
        )
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
