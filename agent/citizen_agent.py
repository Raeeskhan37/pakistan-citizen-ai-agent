from datetime import datetime

from ai.answer_generator import generate_answer
from agent.researcher import research_question
from agent.router import detect_department
from agent.verifier import verify_sources


def format_evidence(sources):

    if not sources:

        return "No reliable evidence was retrieved."

    evidence_parts = []

    for index, source in enumerate(
        sources,
        start=1,
    ):

        evidence_parts.append(
            f"""
SOURCE {index}

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

    return "\n".join(evidence_parts)


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
    )

    sources = research["sources"]

    verification = verify_sources(
        sources
    )

    verified_sources = verification[
        "verified"
    ]

    evidence = format_evidence(
        verified_sources
    )

    answer = generate_answer(
        question=question,
        department=department,
        evidence=evidence,
        language=language,
    )

    official_count = sum(
        1
        for source in verified_sources
        if source.get("official")
    )

    return {
        "department": department,
        "answer": answer,
        "sources": verified_sources,
        "source_count": len(verified_sources),
        "official_source_count": official_count,
        "checked_date": datetime.now().strftime(
            "%d %B %Y"
        ),
        "warning": verification["warning"],
    }
