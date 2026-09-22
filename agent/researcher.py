from search.web_search import perform_search


# ============================================================
# JURISDICTION DETECTION
# ============================================================

PROVINCES = {
    "Punjab": [
        "punjab",
        "lahore",
        "rawalpindi",
        "faisalabad",
        "multan",
        "gujranwala",
        "sialkot",
    ],
    "Sindh": [
        "sindh",
        "karachi",
        "hyderabad",
        "sukkur",
        "larkana",
    ],
    "Khyber Pakhtunkhwa": [
        "khyber pakhtunkhwa",
        "kpk",
        "kp",
        "peshawar",
        "mardan",
        "swat",
        "malakand",
        "dir",
    ],
    "Balochistan": [
        "balochistan",
        "quetta",
        "gwadar",
    ],
    "Islamabad": [
        "islamabad",
        "ict",
        "islamabad capital territory",
    ],
    "Azad Jammu and Kashmir": [
        "ajk",
        "azad kashmir",
        "muzaffarabad",
    ],
    "Gilgit-Baltistan": [
        "gilgit",
        "gilgit baltistan",
        "gb",
        "skardu",
    ],
}


def detect_jurisdiction(question):
    question_lower = question.lower()

    for province, keywords in PROVINCES.items():
        for keyword in keywords:
            if keyword in question_lower:
                return province

    return None


# ============================================================
# VACCINATION SEARCH
# ============================================================

def research_vaccination(
    question,
    language,
):
    """
    Targeted official search for vaccination and
    international-travel health requirements.

    Only NHSRC and NIH sources are accepted.
    """

    question_lower = question.lower()

    queries = []

    # --------------------------------------------------------
    # POLIO
    # --------------------------------------------------------
    if "polio" in question_lower:
        queries.extend([
            "site:nhsrc.gov.pk polio vaccination certificate NIMS",
            "site:nhsrc.gov.pk polio international travelers certificate",
            "site:nih.org.pk polio vaccination international travelers",
            "site:nih.org.pk polio vaccination certificate Pakistan",
        ])

    # --------------------------------------------------------
    # YELLOW FEVER
    # --------------------------------------------------------
    if "yellow fever" in question_lower:
        queries.extend([
            "site:nhsrc.gov.pk yellow fever vaccination certificate NIMS",
            "site:nhsrc.gov.pk yellow fever international travelers",
            "site:nih.org.pk yellow fever vaccination certificate Pakistan",
        ])

    # --------------------------------------------------------
    # HAJJ / UMRAH
    # --------------------------------------------------------
    if (
        "hajj" in question_lower
        or "haj" in question_lower
        or "umrah" in question_lower
        or "umra" in question_lower
    ):
        queries.extend([
            "site:nhsrc.gov.pk Hajj vaccination Pakistan",
            "site:nhsrc.gov.pk Hajj vaccine requirements Pakistan",
            "site:nhsrc.gov.pk Hajj health requirements vaccination",
            "site:nih.org.pk Hajj vaccination Pakistan",
            "site:nih.org.pk Hajj health requirements",
        ])

    # --------------------------------------------------------
    # NIMS / CERTIFICATE
    # --------------------------------------------------------
    if (
        "nims" in question_lower
        or "certificate" in question_lower
        or "vaccination certificate" in question_lower
    ):
        queries.extend([
            "site:nhsrc.gov.pk NIMS vaccination certificate",
            "site:nhsrc.gov.pk digital vaccination certificate",
            "site:nhsrc.gov.pk polio yellow fever NIMS",
        ])

    # --------------------------------------------------------
    # GENERAL TRAVEL VACCINATION
    # --------------------------------------------------------
    queries.extend([
        f"site:nhsrc.gov.pk {question}",
        f"site:nih.org.pk {question}",
    ])

    # Remove duplicate queries while preserving order.
    unique_queries = []

    for query in queries:
        if query not in unique_queries:
            unique_queries.append(query)

    sources = perform_search(
        queries=unique_queries,
        official_domains=[
            "nhsrc.gov.pk",
            "nih.org.pk",
        ],
        max_results=8,
    )

    # --------------------------------------------------------
    # HARD DOMAIN FILTER
    # --------------------------------------------------------

    allowed_domains = {
        "nhsrc.gov.pk",
        "nih.org.pk",
    }

    official_sources = []

    for source in sources:

        if not source.get("official"):
            continue

        domain = (
            source.get(
                "domain",
                "",
            )
            .lower()
            .replace(
                "www.",
                "",
            )
        )

        if domain not in allowed_domains:
            continue

        # ----------------------------------------------------
        # RELEVANCE FILTER
        # ----------------------------------------------------

        title = (
            source.get(
                "title",
                "",
            )
            or ""
        ).lower()

        snippet = (
            source.get(
                "snippet",
                "",
            )
            or ""
        ).lower()

        page_text = (
            source.get(
                "page_text",
                "",
            )
            or ""
        ).lower()

        combined_text = (
            title
            + " "
            + snippet
            + " "
            + page_text
        )

        relevant_terms = [
            "vaccin",
            "polio",
            "yellow fever",
            "nims",
            "traveller",
            "traveler",
            "international",
            "hajj",
            "haj",
            "umrah",
        ]

        relevance = sum(
            1
            for term in relevant_terms
            if term in combined_text
        )

        if relevance < 2:
            continue

        source["relevance"] = relevance

        official_sources.append(
            source
        )

    # Highest relevance first.
    official_sources.sort(
        key=lambda source: source.get(
            "relevance",
            0,
        ),
        reverse=True,
    )

    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    unique = {}

    for source in official_sources:

        url = source.get(
            "url",
            "",
        )

        if not url:
            continue

        if url not in unique:
            unique[url] = source

    official_sources = list(
def research_vaccination(
    question,
    language,
):
    """
    Targeted official search for:
    1. International travel vaccination
    2. Hajj / Umrah health requirements

    The search authority is selected from the question.
    """

    question_lower = question.lower()

    # ========================================================
    # SELECT OFFICIAL AUTHORITIES
    # ========================================================

    hajj_question = any(
        term in question_lower
        for term in [
            "hajj",
            "haj",
            "umrah",
            "umra",
        ]
    )

    if hajj_question:

        official_domains = [
            "mora.gov.pk",
            "nhsrc.gov.pk",
            "nih.org.pk",
        ]

        queries = [
            (
                "site:mora.gov.pk "
                "Hajj Policy 2026 vaccination "
                "health requirements"
            ),
            (
                "site:mora.gov.pk "
                "Hajj 2026 Saudi health instructions "
                "vaccination"
            ),
            (
                "site:mora.gov.pk "
                "Hajj 2026 meningitis vaccination"
            ),
            (
                "site:mora.gov.pk "
                "Hajj 2026 polio vaccination"
            ),
            (
                "site:nhsrc.gov.pk "
                "Hajj 2026 vaccination Pakistan"
            ),
            (
                "site:nih.org.pk "
                "Hajj 2026 vaccination Pakistan"
            ),
            f"site:mora.gov.pk {question}",
        ]

    else:

        official_domains = [
            "nhsrc.gov.pk",
            "nih.org.pk",
        ]

        queries = []

        if "polio" in question_lower:
            queries.extend([
                (
                    "site:nhsrc.gov.pk "
                    "polio vaccination certificate "
                    "international travel Pakistan"
                ),
                (
                    "site:nhsrc.gov.pk "
                    "polio international travelers certificate"
                ),
                (
                    "site:nih.org.pk "
                    "polio vaccination international travelers"
                ),
                (
                    "site:nih.org.pk "
                    "polio vaccination certificate Pakistan"
                ),
            ])

        if "yellow fever" in question_lower:
            queries.extend([
                (
                    "site:nhsrc.gov.pk "
                    "yellow fever vaccination certificate "
                    "international travel Pakistan"
                ),
                (
                    "site:nih.org.pk "
                    "yellow fever vaccination certificate Pakistan"
                ),
            ])

        if (
            "nims" in question_lower
            or "certificate" in question_lower
        ):
            queries.extend([
                (
                    "site:nhsrc.gov.pk "
                    "NIMS vaccination certificate"
                ),
                (
                    "site:nhsrc.gov.pk "
                    "digital vaccination certificate"
                ),
                (
                    "site:nhsrc.gov.pk "
                    "polio yellow fever NIMS"
                ),
            ])

        queries.extend([
            f"site:nhsrc.gov.pk {question}",
            f"site:nih.org.pk {question}",
        ])

    # ========================================================
    # SEARCH
    # ========================================================

    sources = perform_search(
        queries=queries,
        official_domains=official_domains,
        max_results=8,
    )

    # ========================================================
    # HARD DOMAIN FILTER
    # ========================================================

    allowed_domains = set(
        domain.lower()
        for domain in official_domains
    )

    official_sources = []

    for source in sources:

        if not source.get("official"):
            continue

        domain = (
            source.get(
                "domain",
                "",
            )
            .lower()
            .replace(
                "www.",
                "",
            )
        )

        if domain not in allowed_domains:
            continue

        # ====================================================
        # RELEVANCE FILTER
        # ====================================================

        title = (
            source.get(
                "title",
                "",
            )
            or ""
        ).lower()

        snippet = (
            source.get(
                "snippet",
                "",
            )
            or ""
        ).lower()

        page_text = (
            source.get(
                "page_text",
                "",
            )
            or ""
        ).lower()

        combined_text = (
            title
            + " "
            + snippet
            + " "
            + page_text
        )

        if hajj_question:

            relevant_terms = [
                "hajj",
                "haj",
                "vaccin",
                "health",
                "saudi",
                "meningitis",
                "polio",
                "certificate",
            ]

def research_vaccination(
    question,
    language,
):
    """
    Targeted official research for:
    - International travel vaccination
    - Hajj / Umrah vaccination and health requirements

    Hajj questions use the official Ministry of Religious
    Affairs sources for Hajj 2026.
    """

    from search.web_search import fetch_page_text

    question_lower = question.lower()

    hajj_question = any(
        term in question_lower
        for term in [
            "hajj",
            "haj",
            "umrah",
            "umra",
        ]
    )

    # ========================================================
    # HAJJ / UMRAH
    # ========================================================

    if hajj_question:

        # These are confirmed official MoRA 2026 pages.
        direct_sources = [
            {
                "title": "Hajj Policy and Plan 2026",
                "url": (
                    "https://www.mora.gov.pk/"
                    "SiteImage/Downloads/"
                    "200825_Hajj-Policy-2026.pdf"
                ),
                "domain": "mora.gov.pk",
                "official": True,
            },
            {
                "title": (
                    "Saudi Government Health Instructions "
                    "for Hajj - 2026"
                ),
                "url": (
                    "https://www.mora.gov.pk/"
                    "NewsDetail/"
                    "N2ExNTM0OTItNjNlMC00YTU0LWE4N2Mt"
                    "MzcxNjI1Yjk4Zjk2"
                ),
                "domain": "mora.gov.pk",
                "official": True,
            },
        ]

        # Fetch the actual official page/PDF text where possible.
        for source in direct_sources:

            try:
                page_text = fetch_page_text(
                    source["url"],
                    max_chars=20000,
                )

                if page_text:
                    source["page_text"] = page_text
                    source["snippet"] = page_text

            except Exception:
                pass

        # Also search the official Ministry site for
        # additional 2026 health information.
        queries = [
            (
                "site:mora.gov.pk "
                "\"Hajj Policy and Plan 2026\" "
                "vaccination"
            ),
            (
                "site:mora.gov.pk "
                "\"Saudi Government Health Instructions "
                "for Hajj - 2026\""
            ),
            (
                "site:mora.gov.pk "
                "Hajj 2026 vaccination certificate"
            ),
            (
                "site:mora.gov.pk "
                "Hajj 2026 meningitis vaccination"
            ),
            (
                "site:mora.gov.pk "
                "Hajj 2026 polio vaccination"
            ),
        ]

        searched_sources = perform_search(
            queries=queries,
            official_domains=[
                "mora.gov.pk",
            ],
            max_results=8,
        )

        # Keep only MoRA sources.
        for source in searched_sources:

            if not source.get("official"):
                continue

            domain = (
                source.get(
                    "domain",
                    "",
                )
                .lower()
                .replace(
                    "www.",
                    "",
                )
            )

            if domain != "mora.gov.pk":
                continue

            url = source.get(
                "url",
                "",
            )

            if not url:
                continue

            # Don't duplicate the two direct sources.
            if any(
                existing["url"] == url
                for existing in direct_sources
            ):
                continue

            direct_sources.append(
                source
            )

        # Remove duplicate URLs.
        unique = {}

        for source in direct_sources:

            url = source.get(
                "url",
                "",
            )

            if url and url not in unique:
                unique[url] = source

        final_sources = list(
            unique.values()
        )

        return {
            "sources": final_sources[:5],
            "rag_results": [],
            "jurisdiction": None,
            "attempts": 1,
        }

    # ========================================================
    # INTERNATIONAL TRAVEL VACCINATION
    # ========================================================

    official_domains = [
        "nhsrc.gov.pk",
        "nih.org.pk",
    ]

    queries = []

    if "polio" in question_lower:

        queries.extend([
            (
                "site:nhsrc.gov.pk "
                "polio vaccination certificate "
                "international travel Pakistan"
            ),
            (
                "site:nhsrc.gov.pk "
                "NIMS polio certificate"
            ),
            (
                "site:nih.org.pk "
                "polio vaccination certificate "
                "international travel"
            ),
        ])

    if "yellow fever" in question_lower:

        queries.extend([
            (
                "site:nhsrc.gov.pk "
                "yellow fever vaccination certificate "
                "international travel Pakistan"
            ),
            (
                "site:nih.org.pk "
                "yellow fever certificate Pakistan"
            ),
        ])

    queries.extend([
        f"site:nhsrc.gov.pk {question}",
        f"site:nih.org.pk {question}",
    ])

    sources = perform_search(
        queries=queries,
        official_domains=official_domains,
        max_results=8,
    )

    allowed_domains = {
        "nhsrc.gov.pk",
        "nih.org.pk",
    }

    official_sources = []

    for source in sources:

        if not source.get("official"):
            continue

        domain = (
            source.get(
                "domain",
                "",
            )
            .lower()
            .replace(
                "www.",
                "",
            )
        )

        if domain not in allowed_domains:
            continue

        title = (
            source.get(
                "title",
                "",
            )
            or ""
        ).lower()

        snippet = (
            source.get(
                "snippet",
                "",
            )
            or ""
        ).lower()

        page_text = (
            source.get(
                "page_text",
                "",
            )
            or ""
        ).lower()

        combined_text = (
            title
            + " "
            + snippet
            + " "
            + page_text
        )

        relevant_terms = [
            "vaccin",
            "polio",
            "yellow fever",
            "nims",
            "international",
            "certificate",
        ]

        relevance = sum(
            1
            for term in relevant_terms
            if term in combined_text
        )

        if relevance < 2:
            continue

        source["relevance"] = relevance
        official_sources.append(
            source
        )

    official_sources.sort(
        key=lambda source: source.get(
            "relevance",
            0,
        ),
        reverse=True,
    )

    unique = {}

    for source in official_sources:

        url = source.get(
            "url",
            "",
        )

        if url and url not in unique:
            unique[url] = source

    return {
        "sources": list(
            unique.values()
        )[:5],
        "rag_results": [],
        "jurisdiction": None,
        "attempts": 1,
                    }


# ============================================================
# NADRA SEARCH
# ============================================================

def research_nadra(
    question,
    language,
):
    from rag.nadra_retriever import retrieve_nadra

    rag_results = retrieve_nadra(
        question,
        language=language,
    )

    queries = [
        f"site:nadra.gov.pk {question}",
        f"site:nadra.gov.pk {question} NADRA",
    ]

    sources = perform_search(
        queries=queries,
        official_domains=[
            "nadra.gov.pk",
        ],
        max_results=8,
    )

    official_sources = [
        source
        for source in sources
        if source.get("official")
    ]

    return {
        "sources": official_sources[:5],
        "rag_results": rag_results,
        "jurisdiction": None,
        "attempts": 1,
    }


# ============================================================
# PROTECTOR FOR VISA
# ============================================================

def research_protector(
    question,
    language,
):
    queries = [
        f"site:beoe.gov.pk {question}",
        f"site:beoe.gov.pk protector of emigrants {question}",
        "site:beoe.gov.pk emigrant protection documents",
        "site:beoe.gov.pk protector clearance procedure",
        "site:beoe.gov.pk direct emigrants registration",
    ]

    sources = perform_search(
        queries=queries,
        official_domains=[
            "beoe.gov.pk",
        ],
        max_results=8,
    )

    official_sources = [
        source
        for source in sources
        if source.get("official")
    ]

    unique = {}

    for source in official_sources:

        url = source.get(
            "url",
            "",
        )

        if not url:
            continue

        if url not in unique:
            unique[url] = source

    return {
        "sources": list(
            unique.values()
        )[:5],
        "rag_results": [],
        "jurisdiction": None,
        "attempts": 1,
    }


# ============================================================
# GENERAL DEPARTMENT SEARCH
# ============================================================

def research_department(
    question,
    department,
    language,
):
    from config.departments import DEPARTMENTS

    department_config = DEPARTMENTS[
        department
    ]

    official_domains = department_config.get(
        "official_domains",
        [],
    )

    keywords = department_config.get(
        "keywords",
        [],
    )

    jurisdiction = detect_jurisdiction(
        question
    )

    queries = [
        question,
        f"{department} {question}",
    ]

    if jurisdiction:
        queries.append(
            f"{jurisdiction} {department} {question}"
        )

    for keyword in keywords[:5]:
        queries.append(
            f"{keyword} {question}"
        )

    for attempt in range(
        1,
        4,
    ):

        sources = perform_search(
            queries=queries,
            official_domains=official_domains,
            max_results=8,
        )

        official_sources = [
            source
            for source in sources
            if source.get("official")
        ]

        if official_sources:
            return {
                "sources": official_sources[:5],
                "rag_results": [],
                "jurisdiction": jurisdiction,
                "attempts": attempt,
            }

        queries.append(
            f"official government {department} {question}"
        )

    return {
        "sources": [],
        "rag_results": [],
        "jurisdiction": jurisdiction,
        "attempts": 3,
    }


# ============================================================
# MAIN RESEARCH ROUTER
# ============================================================

def research_question(
    question,
    department,
    language,
):

    if department == "NADRA":
        return research_nadra(
            question,
            language,
        )

    if department == "Protector for Visa":
        return research_protector(
            question,
            language,
        )

    if (
        department
        == "Vaccination for Travelling Abroad"
    ):
        return research_vaccination(
            question,
            language,
        )

    return research_department(
        question,
        department,
        language,
    )
