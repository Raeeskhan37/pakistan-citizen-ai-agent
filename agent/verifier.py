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
        # An official government source is considered
        # authoritative when its domain has already been
        # verified by source_filter.py.
        #
        # Page download failure must NOT turn an official
        # government source into an unofficial source.
        # ----------------------------------------------------

        if source.get("official") is not True:
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
            "No authoritative official source "
            "could be verified for this question."
        ),
    }
