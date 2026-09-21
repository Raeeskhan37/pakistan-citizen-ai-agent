from urllib.parse import urlparse


def get_domain(url):

    try:

        parsed = urlparse(url)

        return parsed.netloc.lower().replace(
            "www.",
            "",
        )

    except Exception:

        return ""


def domain_matches(url, official_domains):

    domain = get_domain(url)

    for official in official_domains:

        official = official.lower().replace(
            "www.",
            "",
        )

        if (
            domain == official
            or domain.endswith("." + official)
        ):

            return True

    return False


def filter_and_rank_sources(
    results,
    official_domains,
):

    cleaned = []

    for result in results:

        if not isinstance(result, dict):
            continue

        url = result.get("href") or result.get("url")

        if not url:
            continue

        title = result.get(
            "title",
            "Web result",
        )

        body = result.get(
            "body",
            result.get("snippet", ""),
        )

        is_official = domain_matches(
            url,
            official_domains,
        )

        cleaned.append(
            {
                "title": title,
                "url": url,
                "snippet": body,
                "official": is_official,
            }
        )

    cleaned.sort(
        key=lambda item: not item["official"]
    )

    return cleaned
