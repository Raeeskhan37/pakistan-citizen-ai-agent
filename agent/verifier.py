from urllib.parse import urlparse


def verify_sources(
    sources,
    minimum_sources=1,
):

    verified = []

    for source in sources:

        url = source.get("url", "")

        if not url:
            continue

        parsed = urlparse(url)

        if parsed.scheme not in (
            "http",
            "https",
        ):
            continue

        if source.get("official"):
            verified.append(source)

    if verified:

        return {
            "verified": verified,
            "has_verified_source": True,
            "warning": "",
        }

    fallback = sources[:5]

    if len(fallback) >= minimum_sources:

        return {
            "verified": fallback,
            "has_verified_source": False,
            "warning": (
                "No authoritative official source was found "
                "among the retrieved results. The information "
                "should be independently verified."
            ),
        }

    return {
        "verified": [],
        "has_verified_source": False,
        "warning": (
            "I could not find enough reliable information "
            "to verify an answer."
        ),
    }
