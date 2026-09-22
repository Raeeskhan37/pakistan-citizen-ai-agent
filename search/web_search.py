from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

from search.ddgs_search import search_ddgs
from search.source_filter import filter_and_rank_sources

============================================================

SETTINGS

============================================================

SEARCH_WORKERS = 6
PAGE_WORKERS = 5

SEARCH_TIMEOUT = 8
PAGE_TIMEOUT = 6

MAX_OFFICIAL_PAGES_TO_FETCH = 5

============================================================

FETCH OFFICIAL PAGE

============================================================

def fetch_page_text(
url,
max_chars=12000,
):
"""
Fetch readable text from an official government page.

A short timeout is intentional. A slow government website
must not hold the entire citizen agent indefinitely.
"""

try:

    response = requests.get(
        url,
        timeout=PAGE_TIMEOUT,
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

    clean_text = "\n".join(
        lines
    )

    return clean_text[:max_chars]

except Exception:
    return ""

============================================================

RUN ONE SEARCH

============================================================

def _run_single_search(query):
"""
Execute one DDGS search independently.

This function is used by the thread pool so multiple
queries can run at the same time.
"""

try:

    return search_ddgs(
        query=query,
        max_results=8,
    )

except Exception:
    return []

============================================================

FETCH ONE OFFICIAL SOURCE

============================================================

def _fetch_official_source(source):
"""
Fetch one official page independently.
"""

if not isinstance(
    source,
    dict,
):
    return source

url = source.get(
    "url",
    "",
)

if not url:
    return source

page_text = fetch_page_text(
    url
)

if page_text:

    source["page_text"] = page_text

    source["snippet"] = page_text

return source

============================================================

MAIN SEARCH

============================================================

def perform_search(
queries,
official_domains,
max_results=8,
):
"""
Fast official-government search.

Improvements:

1. Search queries run in parallel.
2. Official pages are fetched in parallel.
3. Only the best official pages are downloaded.
4. Slow government websites do not block the whole agent.
5. Duplicate URLs are removed early.
"""

if not queries:
    return []

# --------------------------------------------------------
# CLEAN QUERIES
# --------------------------------------------------------

cleaned_queries = []

seen_queries = set()

for query in queries:

    query = (
        str(query)
        .strip()
    )

    if not query:
        continue

    if query in seen_queries:
        continue

    seen_queries.add(
        query
    )

    cleaned_queries.append(
        query
    )

if not cleaned_queries:
    return []

# --------------------------------------------------------
# PARALLEL SEARCH
# --------------------------------------------------------

all_results = []

worker_count = min(
    SEARCH_WORKERS,
    len(cleaned_queries),
)

with ThreadPoolExecutor(
    max_workers=worker_count
) as executor:

    future_map = {
        executor.submit(
            _run_single_search,
            query,
        ): query
        for query in cleaned_queries
    }

    for future in as_completed(
        future_map
    ):

        try:

            results = future.result()

        except Exception:

            results = []

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

# --------------------------------------------------------
# FILTER / RANK
# --------------------------------------------------------

sources = filter_and_rank_sources(
    all_results,
    official_domains,
)

# --------------------------------------------------------
# REMOVE DUPLICATES
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
# SPLIT OFFICIAL / OTHER
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

# --------------------------------------------------------
# ONLY FETCH A SMALL NUMBER OF OFFICIAL PAGES
# --------------------------------------------------------
#
# Search snippets are already available.
# We only need actual page text for the best few
# official sources.
# --------------------------------------------------------

official_sources = official_sources[
    :MAX_OFFICIAL_PAGES_TO_FETCH
]

# --------------------------------------------------------
# PARALLEL PAGE FETCH
# --------------------------------------------------------

if official_sources:

    worker_count = min(
        PAGE_WORKERS,
        len(official_sources),
    )

    with ThreadPoolExecutor(
        max_workers=worker_count
    ) as executor:

        futures = [
            executor.submit(
                _fetch_official_source,
                source,
            )
            for source in official_sources
        ]

        fetched_sources = []

        for future in as_completed(
            futures
        ):

            try:

                source = future.result()

            except Exception:

                continue

            if source:
                fetched_sources.append(
                    source
                )

    # Preserve official-source priority.
    official_sources = fetched_sources

# --------------------------------------------------------
# RETURN
# --------------------------------------------------------

return (
    official_sources
    + other_sources
)
