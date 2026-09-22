from urllib.parse import urlparse


def verify_sources(
    sources,
    minimum_sources=1,
):
    verified = []

    for source in sources:

        if not isinstance(
            source,
            dict,
        ):
            continue

        url = source.get(
            "url",
            "",
        )

        if not url:
            continue

        try:
            parsed = urlparse(url)
        except Exception:
            continue

        if parsed.scheme not in (
            "http",
            "https",
        ):
            continue

        # ----------------------------------------------------
        # A source is considered usable when:
        #
        # 1. It is an official government domain
        # 2. It has either page_text OR snippet
        # ----------------------------------------------------

        if source.get("official") is not True:
            continue

        page_text = source.get(
            "page_text",
            "",
        )

        snippet = source.get(
            "snippet",
            "",
        )

        if not page_text and not snippet:
            continue

        verified.append(
            source
        )

    if len(verified) >= minimum_sources:

        return {
            "verified": verified,
            "has_verified_source": True,
            "warning": "",
        }

    return {
        "verified": [],
        "has_verified_source": False,
        "warning": (
            "Official government sources were found, "
            "but their content could not be retrieved."
        ),
    }
