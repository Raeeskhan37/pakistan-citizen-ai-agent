from search.ddgs_search import search_ddgs
from search.source_filter import filter_and_rank_sources


def perform_search(
    queries,
    official_domains,
    max_results=8,
):

    all_results = []

    for query in queries:

        results = search_ddgs(
            query,
            max_results=max_results,
        )

        all_results.extend(results)

    sources = filter_and_rank_sources(
        all_results,
        official_domains,
    )

    unique = {}

    for source in sources:

        url = source["url"]

        if url not in unique:
            unique[url] = source

    return list(unique.values())
