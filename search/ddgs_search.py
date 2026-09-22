from ddgs import DDGS


def search_ddgs(
    query: str,
    max_results: int = 8,
):
    try:
        results = DDGS(
            timeout=10,
        ).text(
            query,
            region="pk-en",
            safesearch="moderate",
            max_results=max_results,
            backend="bing",
        )

        return results or []

    except Exception as exc:
        return [
            {
                "error": str(exc),
            }
        ]
