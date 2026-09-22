from ddgs import DDGS


def search_ddgs(query: str, max_results: int = 8):
    try:
        results = DDGS().text(
            query,
            region="pk-en",
            safesearch="moderate",
            max_results=max_results,
        )

        return results or []

    except Exception as exc:
        return [
            {
                "error": str(exc),
            }
        ]
