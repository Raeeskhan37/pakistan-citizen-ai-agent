from config.departments import DEPARTMENTS
from search.web_search import perform_search


def build_queries(
    question,
    department,
):

    if department not in DEPARTMENTS:

        return [
            question,
            f"Pakistan government {question}",
        ]

    domains = DEPARTMENTS[
        department
    ]["official_domains"]

    queries = []

    queries.append(
        f"Pakistan {department} {question}"
    )

    for domain in domains[:3]:

        queries.append(
            f"site:{domain} {question}"
        )

    return queries


def research_question(
    question,
    department,
):

    if department in DEPARTMENTS:

        official_domains = DEPARTMENTS[
            department
        ]["official_domains"]

    else:

        official_domains = [
            "gov.pk"
        ]

    queries = build_queries(
        question,
        department,
    )

    sources = perform_search(
        queries=queries,
        official_domains=official_domains,
        max_results=8,
    )

    return {
        "queries": queries,
        "sources": sources,
    }
