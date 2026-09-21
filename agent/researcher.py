from config.departments import DEPARTMENTS
from search.web_search import perform_search


NADRA_SEARCH_DOMAINS = [
    "nadra.gov.pk",
]


def build_nadra_queries(
    question,
    attempt,
):

    if attempt == 1:

        return [
            f"site:nadra.gov.pk {question}",
            f"site:nadra.gov.pk Pakistan NADRA {question}",
        ]

    if attempt == 2:

        return [
            f"site:nadra.gov.pk/identityDocument {question}",
            f"site:nadra.gov.pk {question} requirements procedure",
            f"site:nadra.gov.pk {question} fee processing time",
        ]

    return [
        f"site:nadra.gov.pk/pakIdentityFaqs {question}",
        f"site:nadra.gov.pk {question} FAQ",
        f"site:nadra.gov.pk {question} official",
        f"site:nadra.gov.pk {question} application",
    ]


def research_nadra(
    question,
):

    all_sources = []

    attempts = 0

    for attempt in range(1, 4):

        attempts = attempt

        queries = build_nadra_queries(
            question,
            attempt,
        )

        sources = perform_search(
            queries=queries,
            official_domains=NADRA_SEARCH_DOMAINS,
            max_results=8,
        )

        for source in sources:

            url = source.get(
                "url",
                "",
            )

            if not url:
                continue

            already_exists = any(
                existing.get("url") == url
                for existing in all_sources
            )

            if not already_exists:

                all_sources.append(source)

        # Stop early if we have enough official evidence
        official_sources = [
            source
            for source in all_sources
            if source.get("official")
        ]

        if len(official_sources) >= 2:

            break

    return {
        "sources": all_sources,
        "attempts": attempts,
    }


def research_question(
    question,
    department,
):

    if department == "NADRA":

        return research_nadra(
            question
        )

    if department in DEPARTMENTS:

        official_domains = DEPARTMENTS[
            department
        ]["official_domains"]

    else:

        official_domains = [
            "gov.pk"
        ]

    queries = [
        question,
        f"Pakistan government {question}",
    ]

    sources = perform_search(
        queries=queries,
        official_domains=official_domains,
        max_results=8,
    )

    return {
        "sources": sources,
        "attempts": 1,
    }
