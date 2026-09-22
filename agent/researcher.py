from config.departments import DEPARTMENTS
from search.web_search import perform_search

from rag.nadra_retriever import (
    retrieve_nadra,
    has_useful_evidence,
)


NADRA_SEARCH_DOMAINS = [
    "nadra.gov.pk",
]


def get_department_domains(
    department,
):

    return DEPARTMENTS.get(
        department,
        {},
    ).get(
        "official_domains",
        ["gov.pk"],
    )


def build_department_queries(
    question,
    department,
    attempt,
):

    domains = get_department_domains(
        department
    )

    queries = []

    # --------------------------------------------------------
    # Attempt 1 — direct question
    # --------------------------------------------------------

    if attempt == 1:

        for domain in domains:

            queries.append(
                f"site:{domain} {question}"
            )

            queries.append(
                f"site:{domain} {question} requirements"
            )

    # --------------------------------------------------------
    # Attempt 2 — procedure/documents/fees
    # --------------------------------------------------------

    elif attempt == 2:

        for domain in domains:

            queries.append(
                f"site:{domain} {question} procedure"
            )

            queries.append(
                f"site:{domain} {question} documents"
            )

            queries.append(
                f"site:{domain} {question} fee"
            )

    # --------------------------------------------------------
    # Attempt 3 — official/FAQ/rules
    # --------------------------------------------------------

    else:

        for domain in domains:

            queries.append(
                f"site:{domain} {question} official"
            )

            queries.append(
                f"site:{domain} {question} FAQ"
            )

            queries.append(
                f"site:{domain} {question} rules"
            )

    return queries


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


def add_unique_sources(
    destination,
    sources,
):

    for source in sources:

        url = source.get(
            "url",
            "",
        )

        if not url:
            continue

        already_exists = any(
            existing.get("url") == url
            for existing in destination
        )

        if not already_exists:

            destination.append(
                source
            )


def research_nadra(
    question,
    language="English",
):

    all_sources = []
    rag_results = []
    attempts = 0

    for attempt in range(1, 4):

        attempts = attempt

        # ----------------------------------------------------
        # RAG search
        # ----------------------------------------------------

        try:

            current_rag = retrieve_nadra(
                question=question,
                language=language,
                top_k=6,
            )

        except Exception:

            current_rag = []

        if current_rag:

            rag_results.extend(
                current_rag
            )

        # ----------------------------------------------------
        # Official NADRA web search
        # ----------------------------------------------------

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

        add_unique_sources(
            all_sources,
            sources,
        )

        official_sources = [
            source
            for source in all_sources
            if source.get("official")
        ]

        useful_rag = has_useful_evidence(
            current_rag
        )

        # ----------------------------------------------------
        # Stop when BOTH evidence layers are useful
        # ----------------------------------------------------

        if (
            useful_rag
            and official_sources
        ):

            break

    # --------------------------------------------------------
    # Remove duplicate RAG results
    # --------------------------------------------------------

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
                official_domains=get_department_domains(
                    department
                ),
                max_results=8,
            )

        except Exception:

            sources = []

        add_unique_sources(
            all_sources,
            sources,
        )

        official_sources = [
            source
            for source in all_sources
            if source.get("official")
        ]

        # ----------------------------------------------------
        # Stop once an official source is found
        # ----------------------------------------------------

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
