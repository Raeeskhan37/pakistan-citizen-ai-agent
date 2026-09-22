from urllib.parse import urlparse


def get_domain(url):

    try:

        parsed = urlparse(
            url
        )

        return (
            parsed.netloc
            .lower()
            .replace(
                "www.",
                "",
            )
            .split(":")[0]
        )

    except Exception:

        return ""


def domain_matches(
    url,
    official_domains,
):

    domain = get_domain(
        url
    )

    if not domain:
        return False

    for official in official_domains:

        official = (
            official
            .lower()
            .replace(
                "www.",
                "",
            )
            .strip()
        )

        if (
            domain == official
            or domain.endswith(
                "." + official
            )
        ):
            return True

    return False


def filter_and_rank_sources(
    results,
    official_domains,
):

    cleaned = []

    for result in results:

        if not isinstance(
            result,
            dict,
        ):
            continue

        url = (
            result.get("href")
            or result.get("url")
            or ""
        )

        if not url:
            continue

        title = (
            result.get("title")
            or "Official Government Source"
        )

        body = (
            result.get("body")
            or result.get("snippet")
            or ""
        )

        domain = get_domain(
            url
        )

        is_official = domain_matches(
            url,
            official_domains,
        )

        cleaned.append(
            {
                "title": title,
                "url": url,
                "domain": domain,
                "snippet": body,
                "official": is_official,
            }
        )

    # --------------------------------------------------------
    # Official sources first
    # --------------------------------------------------------

    cleaned.sort(
        key=lambda item: (
            not item["official"],
            item["domain"],
        )
    )

    return cleaned
