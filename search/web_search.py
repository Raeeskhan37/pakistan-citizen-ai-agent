from search.ddgs_search import search_ddgs
from search.source_filter import (
    filter_and_rank_sources,
)


def perform_search(
    queries,
    official_domains,
    max_results=8,
):
    all_results = []

    for query in queries:

        results = search_ddgs(
            query=query,
            max_results=max_results,
        )

        if not results:
            continue

        for result in results:

            if not isinstance(
                result,
                dict,
            ):
                continue

            if result.get("error"):
                continue

            all_results.append(
                result
            )

    sources = filter_and_rank_sources(
        all_results,
        official_domains,
    )

    # --------------------------------------------------------
    # Remove duplicate URLs
    # --------------------------------------------------------

    unique = {}

    for source in sources:

        url = source.get(
            "url",
            "",
        )

        if not url:
            continue

        if url not in unique:
            unique[url] = source

    sources = list(
        unique.values()
    )

    # --------------------------------------------------------
    # Official sources first
    # --------------------------------------------------------

    official_sources = [
        source
        for source in sources
        if source.get("official")
    ]

    other_sources = [
        source
        for source in sources
        if not source.get("official")
    ]

    return (
        official_sources
        + other_sources
    )
