from datetime import datetime

from ai.answer_generator import generate_answer
from agent.researcher import research_question
from agent.router import detect_department
from agent.verifier import verify_sources
from rag.nadra_retriever import build_nadra_evidence


# ============================================================
# WEB EVIDENCE
# ============================================================

def format_web_evidence(sources):

    if not sources:

        return "No authoritative web evidence was retrieved."

    evidence_parts = []

    for index, source in enumerate(
        sources,
        start=1,
    ):

        evidence_parts.append(
            f"""
WEB SOURCE {index}

Title:
{source.get("title", "")}

URL:
{source.get("url", "")}

Official government source:
{source.get("official", False)}

Information:
{source.get("snippet", "")}
"""
        )

    return "\n".join(
        evidence_parts
    )


# ============================================================
# MAIN CITIZEN AGENT
# ============================================================

def ask_citizen_agent(
    question,
    selected_department,
    language,
):

    # --------------------------------------------------------
    # DETECT DEPARTMENT
    # --------------------------------------------------------

    department = detect_department(
        question,
        selected_department,
    )


    # --------------------------------------------------------
    # RESEARCH
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


    # --------------------------------------------------------
    # VERIFY WEB SOURCES
    # --------------------------------------------------------

    verification = verify_sources(
        web_sources
    )

    verified_sources = verification[
        "verified"
    ]


    # --------------------------------------------------------
    # BUILD NADRA POLICY EVIDENCE
    # --------------------------------------------------------

    if department == "NADRA":

        policy_evidence = (
            build_nadra_evidence(
                rag_results
            )
        )

    else:

        policy_evidence = (
            "No department-specific RAG "
            "evidence was used."
        )


    # --------------------------------------------------------
    # BUILD WEB EVIDENCE
    # --------------------------------------------------------

    web_evidence = format_web_evidence(
    verified_sources[:3]
    )


    # --------------------------------------------------------
    # COMBINE ALL EVIDENCE
    # --------------------------------------------------------

    combined_evidence = f"""
============================================================
NADRA / GOVERNMENT POLICY EVIDENCE
============================================================

{policy_evidence}


============================================================
VERIFIED OFFICIAL WEB EVIDENCE
============================================================

{web_evidence}
"""


    # --------------------------------------------------------
    # CHECK WHETHER ANY VERIFIED EVIDENCE EXISTS
    # --------------------------------------------------------

    has_policy_evidence = bool(
        rag_results
    )

    has_web_evidence = bool(
        verified_sources
    )


    # --------------------------------------------------------
    # GENERATE ANSWER
    # --------------------------------------------------------

    if not has_policy_evidence and not has_web_evidence:

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
    # COUNT OFFICIAL SOURCES
    # --------------------------------------------------------

    official_count = sum(
        1
        for source in verified_sources
        if source.get("official")
    )


    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {
        "department": department,

        "answer": answer,

        "sources": verified_sources,

        "source_count": len(
            verified_sources
        ),

        "official_source_count": (
            official_count
        ),

        "research_attempts": (
            research.get(
                "attempts",
                1,
            )
        ),

        "rag_result_count": len(
            rag_results
        ),

        "checked_date": (
            datetime.now().strftime(
                "%d %B %Y"
            )
        ),

        "warning": verification.get(
            "warning",
            "",
        ),
    }
