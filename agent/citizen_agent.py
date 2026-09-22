from datetime import datetime

from ai.answer_generator import generate_answer
from agent.researcher import research_question
from agent.router import detect_department
from agent.verifier import verify_sources
from rag.nadra_retriever import build_nadra_evidence


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
# DIRECT HAJJ 2026 ANSWER
# ============================================================

def build_hajj_2026_answer(
    question,
    language,
):
    """
    Deterministic answer for Hajj 1447H / 2026
    based on official Saudi MOH health requirements.

    This avoids relying on the general LLM answer
    generation step for a highly specific health
    requirement.
    """

    question_lower = question.lower()

    # --------------------------------------------------------
    # ENGLISH
    # --------------------------------------------------------

    if language == "English":

        return """
For Hajj 2026 (1447H), official Saudi Ministry of Health
requirements apply to pilgrims arriving in Saudi Arabia.

For pilgrims coming from Pakistan:

• Pakistan is identified in the Saudi Ministry of Health
  Hajj 1447/2026 health requirements in relation to
  poliovirus circulation.

• Saudi health authorities may administer a single dose of
  bivalent oral polio vaccine (bOPV) at the point of entry,
  based on a risk assessment, regardless of age or previous
  vaccination history.

• The Saudi Ministry of Health also states that the
  meningococcal (Neisseria) vaccine is mandatory for Hajj
  pilgrims who have not received it within the previous
  five years.

• Vaccination status for the meningococcal vaccine can be
  verified through the Saudi Sehhaty system.

For the exact certificate/document requirements applicable
to a Pakistani pilgrim, the official Saudi Hajj health
requirements and the Pakistan Ministry of Religious Affairs'
2026 health instructions should be followed.

I have not assumed that every recommended vaccine is
mandatory. The official sources distinguish between
mandatory requirements, recommendations, and measures that
may be applied at entry.

Official sources:
1. Saudi Ministry of Health — Health Requirements for Hajj
   1447H (2026)
2. Saudi Ministry of Health — Hajj 1447H Vaccination Campaign
3. Pakistan Ministry of Religious Affairs — Saudi Government
   Health Instructions for Hajj 2026
"""

    # --------------------------------------------------------
    # URDU
    # --------------------------------------------------------

    return """
حج 2026 (1447ھ) کے لیے سعودی عرب کی وزارتِ صحت کی
سرکاری صحت کی ہدایات لاگو ہوتی ہیں۔

پاکستان سے حج کے لیے جانے والے عازمین کے بارے میں:

• سعودی وزارتِ صحت کی حج 1447/2026 کی سرکاری ہدایات میں
  پاکستان کو پولیو وائرس کی موجودگی کے حوالے سے متعلقہ
  ممالک میں شامل کیا گیا ہے۔

• سعودی صحت حکام خطرے کے جائزے کی بنیاد پر سعودی عرب
  پہنچنے پر ایک خوراک bivalent oral polio vaccine (bOPV)
  دے سکتے ہیں، عمر یا پہلے ویکسین لگنے کی صورتحال سے قطع
  نظر۔

• سعودی وزارتِ صحت کے مطابق meningococcal (Neisseria)
  ویکسین ان حج عازمین کے لیے لازمی ہے جنہیں گزشتہ پانچ
  سال کے اندر یہ ویکسین نہیں لگی۔

• اس ویکسین کی حیثیت سعودی Sehhaty نظام کے ذریعے بھی
  چیک کی جا سکتی ہے۔

پاکستانی عازم کے لیے درست سرٹیفکیٹ یا دستاویز کی حتمی
ضرورت کے لیے سعودی وزارتِ صحت کی حج 2026 کی سرکاری
صحت کی ہدایات اور پاکستان کی وزارتِ مذہبی امور کی
2026 کی سرکاری صحت ہدایات پر عمل کرنا چاہیے۔

میں نے تجویز کردہ ہر ویکسین کو لازمی قرار نہیں دیا ہے۔
سرکاری ذرائع لازمی تقاضوں، سفارشات اور داخلے کے وقت
ممکنہ اقدامات میں فرق کرتے ہیں۔

سرکاری ذرائع:
1۔ سعودی وزارتِ صحت — حج 1447ھ (2026) کی صحت کی ہدایات
2۔ سعودی وزارتِ صحت — حج 1447ھ ویکسینیشن مہم
3۔ پاکستان وزارتِ مذہبی امور — حج 2026 کی سعودی صحت کی ہدایات
"""


# ============================================================
# MAIN CITIZEN AGENT
# ============================================================

def ask_citizen_agent(
    question,
    selected_department,
    language,
):

    department = detect_department(
        question,
        selected_department,
    )

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
    # SPECIAL CASE:
    # HAJJ / UMRAH VACCINATION
    # ========================================================

    is_hajj_question = (
        department
        == "Vaccination for Travelling Abroad"
        and any(
            term in question.lower()
            for term in [
                "hajj",
                "haj",
                "umrah",
                "umra",
            ]
        )
    )

    if is_hajj_question:

        answer = build_hajj_2026_answer(
            question=question,
            language=language,
        )

    else:

        # ----------------------------------------------------
        # NADRA RAG
        # ----------------------------------------------------

        if department == "NADRA":

            policy_evidence = build_nadra_evidence(
                rag_results
            )

        else:

            policy_evidence = (
                "No department-specific "
                "policy evidence was used."
            )

        # ----------------------------------------------------
        # WEB EVIDENCE
        # ----------------------------------------------------

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

    # ========================================================
    # SOURCE COUNT
    # ========================================================

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
        "warning": "",
    }
