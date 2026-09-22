import requests

from bs4 import BeautifulSoup

from search.ddgs_search import search_ddgs

from search.source_filter import (
    filter_and_rank_sources,
)


def fetch_page_text(
    url,
    max_chars=12000,
):
    """
    Fetch readable text from an official government page.
    """

    try:

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(compatible; PakistanCitizenAI/1.0)"
                )
            },
        )

        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(
            response.text,
            "lxml",
        )

        # Remove unnecessary page elements
        for element in soup(
            [
                "script",
                "style",
                "noscript",
                "header",
                "footer",
                "nav",
            ]
        ):
            element.decompose()

        text = soup.get_text(
            separator="\n",
        )

        lines = []

        for line in text.splitlines():

            line = line.strip()

            if line:
                lines.append(line)

        clean_text = "\n".join(lines)

        return clean_text[:max_chars]

    except Exception:
        return ""


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

            if result.get(
                "error"
            ):
                continue

            all_results.append(
                result
            )

    sources = filter_and_rank_sources(
        all_results,
        official_domains,
    )

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

    # ---------------------------------------------------------
    # READ ACTUAL OFFICIAL GOVERNMENT PAGES
    # ---------------------------------------------------------

    for source in official_sources:

        url = source.get(
            "url",
            "",
        )

        page_text = fetch_page_text(
            url
        )

        if page_text:

            source["page_text"] = page_text

            # Use actual page content as the evidence
            # instead of relying only on the search snippet.
            source["snippet"] = page_text

    return (
        official_sources
        + other_sources
    )
