from config.departments import DEPARTMENTS
from search.web_search import perform_search

from rag.nadra_retriever import (
    retrieve_nadra,
    has_useful_evidence,
)


NADRA_SEARCH_DOMAINS = [
    "nadra.gov.pk",
]


# ============================================================
# NADRA QUERY BUILDER
# ============================================================

def build_nadra_queries(question, attempt):

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


# ============================================================
# NADRA RAG + WEB RESEARCH
# ============================================================

def research_nadra(
    question,
    language="English",
):

    all_sources = []
    rag_results = []
    attempts = 0

    # --------------------------------------------------------
    # THREE RESEARCH ATTEMPTS
    # --------------------------------------------------------

    for attempt in range(1, 4):

        attempts = attempt

        # ====================================================
        # RAG SEARCH
        # ====================================================

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


        # ====================================================
        # OFFICIAL NADRA WEB SEARCH
        # ====================================================

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


        # ====================================================
        # ADD UNIQUE WEB SOURCES
        # ====================================================

        for source in sources:

            url = source.get(
                "url",
                "",
            )

            if not url:
                continue

            exists = any(
                existing.get("url") == url
                for existing in all_sources
            )

            if not exists:

                all_sources.append(
                    source
                )


        # ====================================================
        # CHECK WHETHER WE HAVE ENOUGH EVIDENCE
        # ====================================================

        official_sources = [
            source
            for source in all_sources
            if source.get("official")
        ]

        useful_rag = has_useful_evidence(
            current_rag
        )

        # ----------------------------------------------------
        # STOP EARLY IF BOTH RAG AND OFFICIAL WEB
        # EVIDENCE ARE AVAILABLE
        # ----------------------------------------------------

        if (
            useful_rag
            and len(official_sources) >= 1
        ):

            break


    # ========================================================
    # REMOVE DUPLICATE RAG RESULTS
    # ========================================================

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


    # Keep strongest six RAG results
    unique_rag = sorted(
        unique_rag,
        key=lambda item: item.get(
            "score",
            0,
        ),
        reverse=True,
    )[:6]


    return {
        "sources": all_sources,
        "rag_results": unique_rag,
        "attempts": attempts,
    }


# ============================================================
# GENERAL RESEARCH
# ============================================================

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


    # ========================================================
    # OTHER DEPARTMENTS
    # ========================================================

    if department in DEPARTMENTS:

        official_domains = (
            DEPARTMENTS[
                department
            ][
                "official_domains"
            ]
        )

    else:

        official_domains = [
            "gov.pk"
        ]


    queries = [
        question,
        f"Pakistan government {question}",
    ]


    try:

        sources = perform_search(
            queries=queries,
            official_domains=official_domains,
            max_results=8,
        )

    except Exception:

        sources = []


    return {
        "sources": sources,
        "rag_results": [],
        "attempts": 1,
    }
