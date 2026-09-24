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
        return (
            "No authoritative web evidence was retrieved."
        )

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

        jurisdiction = source.get(
            "jurisdiction",
            "",
        )

        evidence_parts.append(
            f"""
WEB SOURCE {index}

Jurisdiction:
{jurisdiction}

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
# PILGRIM QUESTION
# ============================================================

def is_pilgrim_question(
    question,
    selected_department,
):

    if (
        selected_department
        != "Vaccination for Travelling Abroad"
    ):
        return False

    q = (
        question or ""
    ).strip().lower()

    return any(
        term in q
        for term in [
            "hajj",
            "haj",
            "umrah",
            "umra",
            "حج",
            "عمرہ",
        ]
    )


def is_umrah_question(question):

    q = (
        question or ""
    ).strip().lower()

    return any(
        term in q
        for term in [
            "umrah",
            "umra",
            "عمرہ",
        ]
    )


# ============================================================
# SAUDI WORK VISA
# ============================================================

def is_saudi_work_visa_question(
    question,
    selected_department,
):

    if (
        selected_department
        != "Vaccination for Travelling Abroad"
    ):
        return False

    q = (
        question or ""
    ).strip().lower()

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
# SPECIAL SOURCES
# ============================================================

HAJJ_SOURCES = [
    {
        "title": "Saudi MOH — Hajj Health Requirements",
        "url": (
            "https://www.moh.gov.sa/"
            "HealthAwareness/Pilgrims-Health/"
            "Documents/"
            "Hajj-Health-Requirements-English-language.pdf"
        ),
        "domain": "moh.gov.sa",
        "official": True,
    },
]


UMRAH_SOURCES = [
    {
        "title": "Saudi MOH — Umrah Health Requirements",
        "url": (
            "https://www.moh.gov.sa/"
            "en/HealthAwareness/Pilgrims-Health/"
            "Documents/Health-Regulations-Umrah-EN.pdf"
        ),
        "domain": "moh.gov.sa",
        "official": True,
    },
]


SAUDI_WORK_VISA_SOURCES = [
    {
        "title": (
            "Government of Pakistan / BEOE — "
            "Work Visa Vaccination Policy"
        ),
        "url": (
            "https://beoe.gov.pk/"
            "files/policyguideliness/51.pdf"
        ),
        "domain": "beoe.gov.pk",
        "official": True,
    },
    {
        "title": (
            "Saudi Ministry of Health — "
            "Coming to Work in Saudi Arabia"
        ),
        "url": (
            "https://www.moh.gov.sa/"
            "ministry/life-events/pages/default.aspx"
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
حج کے لیے ویکسینیشن

سعودی وزارتِ صحت کی موجودہ سرکاری حج صحت
ضروریات کے مطابق حج کے لیے متعلقہ ویکسینیشن
اور صحت کی شرائط پوری کرنا ضروری ہے۔

میننجوکوکل ویکسین اور پاکستان سے آنے والے
مسافروں کے لیے متعلقہ پولیو شرائط سرکاری
سعودی دستاویز کے مطابق پوری کی جائیں۔

موسمی فلو اور COVID-19 سے متعلق معلومات کو
صرف اسی صورت میں لازمی قرار دیا جائے جب
موجودہ سرکاری دستاویز واضح طور پر ایسا کہے۔
"""

    return """
Hajj Vaccination Requirements

Follow the current Saudi Ministry of Health official
Hajj health requirements.

The applicable meningococcal vaccination requirement
and Pakistan-specific polio requirements should be
completed according to the current official document.

Influenza and COVID-19 should not automatically be
described as mandatory unless the current official
document explicitly says so.
"""


# ============================================================
# UMRAH ANSWER
# ============================================================

def build_umrah_answer(language):

    if language == "اردو":

        return """
عمرہ کے لیے ویکسینیشن

عمرہ کے لیے موجودہ سعودی وزارتِ صحت کی سرکاری
صحت کی ضروریات پر عمل کرنا ضروری ہے۔

میننجوکوکل ویکسین اور پاکستان سے آنے والے
مسافروں کے لیے متعلقہ پولیو شرائط موجودہ
سرکاری سعودی دستاویز کے مطابق پوری کی جائیں۔
"""

    return """
Umrah Vaccination Requirements

Follow the current Saudi Ministry of Health official
Umrah health requirements.

The applicable meningococcal vaccination and
Pakistan-specific polio requirements should be
completed according to the current official document.
"""


# ============================================================
# SPECIAL PILGRIM RESPONSE
# ============================================================

def build_special_pilgrim_response(
    question,
    language,
):

    if is_umrah_question(question):

        answer = build_umrah_answer(
            language
        )

        sources = UMRAH_SOURCES

    else:

        answer = build_hajj_answer(
            language
        )

        sources = HAJJ_SOURCES

    return {
        "department": (
            "Vaccination for Travelling Abroad"
        ),
        "jurisdiction": "Saudi Arabia",
        "answer": answer,
        "sources": sources,
        "source_count": len(sources),
        "official_source_count": len(sources),
        "research_attempts": 0,
        "rag_result_count": 0,
        "checked_date": datetime.now().strftime(
            "%d %B %Y"
        ),
        "warning": "",
    }


# ============================================================
# WORK VISA FALLBACK
# ============================================================

def build_work_visa_fallback_evidence():

    return """
OFFICIAL EVIDENCE — ORDINARY SAUDI WORK VISA

The available official evidence does not establish that
every Pakistani travelling on an ordinary Saudi employment
visa must receive a specific vaccine.

Do not transfer Hajj or Umrah vaccination requirements
to ordinary employment visas.

Current medical and health-screening requirements should
be checked against current Saudi and Pakistani official
requirements.
"""


# ============================================================
# ALL-PROVINCES DETECTION
# ============================================================

def is_all_jurisdictions_research(
    research,
):

    return bool(
        research.get(
            "all_jurisdictions",
            False,
        )
    )


# ============================================================
# BUILD PROVINCE INSTRUCTION
# ============================================================

def build_all_province_instruction():

    return """
IMPORTANT ANSWERING RULE — ALL PROVINCES

The citizen did NOT specify a province or area.

The answer MUST therefore be organized by jurisdiction.

Do NOT give only one province's procedure.

Use separate headings for:

1. Punjab
2. Sindh
3. Khyber Pakhtunkhwa
4. Balochistan
5. Islamabad Capital Territory
6. Azad Jammu and Kashmir
7. Gilgit-Baltistan

For each jurisdiction:

- Use only the evidence supplied for that jurisdiction.
- Clearly state the responsible local authority where
  supported by official evidence.
- Clearly state documents only where supported by official
  evidence.
- Clearly state online options only where supported by
  official evidence.
- Clearly state fees or processing time only where the
  official evidence supports them.
- Do not copy Punjab requirements into Sindh.
- Do not copy KP requirements into Balochistan.
- Do not assume the same procedure applies everywhere.

If official evidence for a jurisdiction is insufficient,
say:

"Official procedural details could not be fully verified
from the government sources reviewed. The citizen should
contact the relevant local government / Union Council
authority in that jurisdiction."

Do NOT replace a civil birth certificate with NADRA CRC.

CRC/B-Form is a separate NADRA identity document.

The citizen asked about a BIRTH CERTIFICATE, so answer
about CIVIL BIRTH REGISTRATION / BIRTH CERTIFICATE first.
"""


# ============================================================
# MAIN AGENT
# ============================================================

def ask_citizen_agent(
    question,
    selected_department,
    language,
):

    # --------------------------------------------------------
    # Hajj / Umrah
    # --------------------------------------------------------

    if is_pilgrim_question(
        question,
        selected_department,
    ):

        return build_special_pilgrim_response(
            question=question,
            language=language,
        )

    # --------------------------------------------------------
    # Department
    # --------------------------------------------------------

    if (
        selected_department
        == "Vaccination for Travelling Abroad"
    ):

        department = selected_department

    else:

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

    all_jurisdictions = (
        is_all_jurisdictions_research(
            research
        )
    )

    # --------------------------------------------------------
    # Saudi work visa
    # --------------------------------------------------------

    if is_saudi_work_visa_question(
        question,
        selected_department,
    ):

        existing_urls = {
            source.get("url", "")
            for source in web_sources
            if isinstance(source, dict)
        }

        for source in SAUDI_WORK_VISA_SOURCES:

            if source["url"] not in existing_urls:

                web_sources.append(
                    source
                )

        jurisdiction = (
            jurisdiction
            or "Saudi Arabia"
        )

    # --------------------------------------------------------
    # Verify
    # --------------------------------------------------------

    verification = verify_sources(
        web_sources
    )

    verified_sources = verification.get(
        "verified",
        [],
    )

    # --------------------------------------------------------
    # If all-province research, retain ALL verified
    # jurisdiction sources.
    # --------------------------------------------------------

    if all_jurisdictions:

    # Keep all official sources for the UI,
    # but use only a controlled number for AI evidence.
    selected_sources = verified_sources[:10]

    else:

    selected_sources = verified_sources[:8]

    # --------------------------------------------------------
    # Work visa fallback
    # --------------------------------------------------------

    if (
        is_saudi_work_visa_question(
            question,
            selected_department,
        )
        and not verified_sources
    ):

        verified_sources = [
            source
            for source in web_sources
            if (
                isinstance(source, dict)
                and source.get("official") is True
                and source.get("url")
            )
        ]

        selected_sources = (
            verified_sources
            if all_jurisdictions
            else verified_sources[:8]
        )

    # --------------------------------------------------------
    # NADRA RAG
    # --------------------------------------------------------

    if department == "NADRA":

        policy_evidence = (
            build_nadra_evidence(
                rag_results
            )
        )

    else:

        policy_evidence = (
            "No department-specific "
            "policy evidence was used."
        )

    # --------------------------------------------------------
    # Web evidence
    # --------------------------------------------------------

    web_evidence = format_web_evidence(
        selected_sources
    )

    # --------------------------------------------------------
    # All province instruction
    # --------------------------------------------------------

    if all_jurisdictions:

        web_evidence = (
            build_all_province_instruction()
            + "\n\n"
            + web_evidence
        )

    # --------------------------------------------------------
    # Work visa
    # --------------------------------------------------------

    if is_saudi_work_visa_question(
        question,
        selected_department,
    ):

        web_evidence = (
            build_work_visa_fallback_evidence()
            + "\n\n"
            + web_evidence
        )

    jurisdiction_text = (
        jurisdiction
        if jurisdiction
        else (
            "All Pakistan jurisdictions"
            if all_jurisdictions
            else "Not specified"
        )
    )

    # --------------------------------------------------------
    # Combined evidence
    # --------------------------------------------------------

    combined_evidence = f"""
GOVERNMENT POLICY EVIDENCE

Department:
{department}

Jurisdiction:
{jurisdiction_text}

{policy_evidence}

VERIFIED OFFICIAL WEB EVIDENCE

{web_evidence}
"""

    # --------------------------------------------------------
    # Evidence check
    # --------------------------------------------------------

    has_policy_evidence = bool(
        rag_results
    )

    has_web_evidence = bool(
        selected_sources
    )

    if is_saudi_work_visa_question(
        question,
        selected_department,
    ):

        has_web_evidence = True

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

    # --------------------------------------------------------
    # Source count
    # --------------------------------------------------------

    official_count = sum(
        1
        for source in selected_sources
        if source.get("official")
    )

    # --------------------------------------------------------
    # Return
    # --------------------------------------------------------

    return {
    "department": department,

    "jurisdiction": jurisdiction,

    "answer": answer,

    "sources": (
        verified_sources
        if all_jurisdictions
        else selected_sources
    ),

    "source_count": len(
        verified_sources
        if all_jurisdictions
        else selected_sources
    ),

    "official_source_count": (
        sum(
            1
            for source in (
                verified_sources
                if all_jurisdictions
                else selected_sources
            )
            if source.get("official")
        )
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

    "warning": verification.get(
        "warning",
        "",
    ),
}
