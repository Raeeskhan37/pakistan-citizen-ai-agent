from config.departments import DEPARTMENTS
from search.web_search import perform_search

from rag.nadra_retriever import (
    retrieve_nadra,
    has_useful_evidence,
)


NADRA_SEARCH_DOMAINS = [
    "nadra.gov.pk",
]


def build_department_queries(
    question,
    department,
    attempt,
):
    official_domains = DEPARTMENTS.get(
        department,
        {},
    ).get(
        "official_domains",
        ["gov.pk"],
    )

    domain = official_domains[0]

    if attempt == 1:
        return [
            f"site:{domain} {question}",
            f"site:{domain} {question} requirements",
            f"site:{domain} {question} procedure",
        ]

    if attempt == 2:
        return [
            f"site:{domain} {question} documents",
            f"site:{domain} {question} fee",
            f"site:{domain} {question} application",
            f"site:{domain} {question} process",
        ]

    return [
        f"site:{domain} {question} official",
        f"site:{domain} {question} FAQ",
        f"site:{domain} {question} rules",
        f"site:{domain} {question} policy",
    ]


def build_nadra_queries(
    question,
    attempt,
):
    if attempt == 1:
        return [
            f"site:nadra.gov.pk {question}",
            f"site:nadra.gov.pk {question} requirements",
        ]

    if attempt == 2:
        return [
            f"site:nadra.gov.pk {question} procedure",
            f"site:nadra.gov.pk {question} documents",
            f"site:nadra.gov.pk {question} requirements fee",
        ]

    return [
        f"site:nadra.gov.pk {question} FAQ",
        f"site:nadra.gov.pk {question} official",
        f"site:nadra.gov.pk {question} application",
        f"site:nadra.gov.pk {question} policy",
    ]


def research_nadra(
    question,
    language="English",
):
    all_sources = []
    rag_results = []
    attempts = 0

    for attempt in range(1, 4):

        attempts = attempt

        try:
            current_rag = retrieve_nadra(
                question=question,
                language=language,
                top_k=6,
            )

            if current_rag:
                rag_results.extend(
                    current_rag
                )

        except Exception:
            current_rag = []

        queries = build_nadra_queries(
            question,
            attempt,
        )

        try:
            sources = perform_search(
                queries=queries,
                official_domains=NADRA_SEARCH_DOMAINS,
                max_results=8,
            )

        except Exception:
            sources = []

        for source in sources:

            url = source.get(
                "url",
                "",
            )

            if not url:
                continue

            if not any(
                existing.get("url") == url
                for existing in all_sources
            ):
                all_sources.append(
                    source
                )

        official_sources = [
            source
            for source in all_sources
            if source.get("official")
        ]

        if (
            has_useful_evidence(
                current_rag
            )
            and official_sources
        ):
            break

    unique_rag = []
    seen_rag = set()

    for item in rag_results:

        index_number = item.get(
            "index"
        )

        if index_number in seen_rag:
            continue

        seen_rag.add(
            index_number
        )

        unique_rag.append(
            item
        )

    unique_rag.sort(
        key=lambda item: item.get(
            "score",
            0,
        ),
        reverse=True,
    )

    return {
        "sources": all_sources,
        "rag_results": unique_rag[:6],
        "attempts": attempts,
    }


def research_department(
    question,
    department,
):
    all_sources = []
    attempts = 0

    for attempt in range(1, 4):

        attempts = attempt

        queries = build_department_queries(
            question,
            department,
            attempt,
        )

        try:
            sources = perform_search(
                queries=queries,
                official_domains=DEPARTMENTS[
                    department
                ][
                    "official_domains"
                ],
                max_results=8,
            )

        except Exception:
            sources = []

        for source in sources:

            url = source.get(
                "url",
                "",
            )

            if not url:
                continue

            if not any(
                existing.get("url") == url
                for existing in all_sources
            ):
                all_sources.append(
                    source
                )

        official_sources = [
            source
            for source in all_sources
            if source.get("official")
        ]

        if official_sources:
            break

    return {
        "sources": all_sources,
        "rag_results": [],
        "attempts": attempts,
    }


def research_question(
    question,
    department,
    language="English",
):

    if department == "NADRA":

        return research_nadra(
            question,
            language,
        )

    if department in DEPARTMENTS:

        return research_department(
            question,
            department,
        )

    return {
        "sources": [],
        "rag_results": [],
        "attempts": 3,
    }
