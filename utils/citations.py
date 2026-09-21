def format_sources(sources):

    lines = []

    for source in sources:

        title = source.get(
            "title",
            "Source",
        )

        url = source.get(
            "url",
            "",
        )

        if url:

            lines.append(
                f"- [{title}]({url})"
            )

    return "\n".join(lines)
