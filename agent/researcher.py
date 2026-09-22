from search.web_search import perform_search


# ============================================================
# JURISDICTIONS
# ============================================================

PROVINCES = {
    "punjab": "Punjab",
    "sindh": "Sindh",
    "khyber pakhtunkhwa": "Khyber Pakhtunkhwa",
    "kpk": "Khyber Pakhtunkhwa",
    "kp": "Khyber Pakhtunkhwa",
    "balochistan": "Balochistan",
    "islamabad": "Islamabad Capital Territory",
    "ict": "Islamabad Capital Territory",
    "ajk": "Azad Jammu and Kashmir",
    "azad kashmir": "Azad Jammu and Kashmir",
    "gilgit baltistan": "Gilgit-Baltistan",
    "gb": "Gilgit-Baltistan",
}


def detect_jurisdiction(question):
    """
    Detect an explicitly mentioned Pakistani
    province or territory.
    """

    question_lower = question.lower()

    for keyword, jurisdiction in PROVINCES.items():

        if keyword in question_lower:
            return jurisdiction

    return None


# ============================================================
# VACCINATION
# ============================================================

def research_vaccination(
    question,
    language,
):
    """
    Targeted official research for:

    1. International travel vaccination
    2. Hajj / Umrah vaccination and health requirements

    Hajj / Umrah questions use official sources from:
    - Saudi Ministry of Health
    - Pakistan Ministry of Religious Affairs

    International travel questions use:
    - Pakistan Ministry of National Health Services
    - National Institute of Health Pakistan
    """

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

        queries = [
            (
                "site:moh.gov.sa "
                "Hajj 1447 2026 health requirements "
                "Pakistan polio vaccination"
            ),
            (
                "site:moh.gov.sa "
                "Hajj 2026 Pakistan polio vaccine certificate"
            ),
            (
                "site:moh.gov.sa "
                "Hajj 1447 2026 meningococcal vaccine"
            ),
            (
                "site:moh.gov.sa "
                "Health Requirements Hajj 1447 2026"
            ),
            (
                "site:moh.gov.sa "
                "Pakistan pilgrims Hajj 2026 vaccination"
            ),
            (
                "site:mora.gov.pk "
                "Hajj 2026 vaccination health requirements"
            ),
            (
                "site:mora.gov.pk "
                "Saudi health instructions Hajj 2026"
            ),
            (
                "site:mora.gov.pk "
                "Hajj Policy and Plan 2026"
            ),
            f"site:moh.gov.sa {question}",
            f"site:mora.gov.pk {question}",
        ]

        sources = perform_search(
            queries=queries,
            official_domains=[
                "moh.gov.sa",
                "mora.gov.pk",
            ],
            max_results=8,
        )

        allowed_domains = {
            "moh.gov.sa",
            "mora.gov.pk",
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
                "hajj",
                "1447",
                "2026",
                "vaccin",
                "polio",
                "mening",
                "health",
                "certificate",
                "pakistan",
                "pilgrim",
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

        # Highest relevance first
        official_sources.sort(
            key=lambda source: source.get(
                "relevance",
                0,
            ),
            reverse=True,
        )

        # Remove duplicate URLs
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

    # ========================================================
    # INTERNATIONAL TRAVEL VACCINATION
    # ========================================================

    official_domains = [
        "nhsrc.gov.pk",
        "nih.org.pk",
    ]

    queries = []

    # --------------------------------------------------------
    # POLIO
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # YELLOW FEVER
    # --------------------------------------------------------

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

    # General official searches
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

    # Remove duplicate URLs
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
# NADRA
# ============================================================

def research_nadra(
    question,
    language,
):
    from rag.nadra_retriever import retrieve_nadra

    # --------------------------------------------------------
    # NADRA RAG
    # --------------------------------------------------------

    rag_results = retrieve_nadra(
        question,
        language=language,
    )

    # --------------------------------------------------------
    # NADRA OFFICIAL WEBSITE
    # --------------------------------------------------------

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

    official_sources = []

    for source in sources:

        if source.get("official"):
            official_sources.append(
                source
            )

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
        (
            "site:beoe.gov.pk "
            "protector of emigrants "
            f"{question}"
        ),
        (
            "site:beoe.gov.pk "
            "emigrant protection documents"
        ),
        (
            "site:beoe.gov.pk "
            "protector clearance procedure"
        ),
        (
            "site:beoe.gov.pk "
            "direct emigrants registration"
        ),
    ]

    sources = perform_search(
        queries=queries,
        official_domains=[
            "beoe.gov.pk",
        ],
        max_results=8,
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

        if domain != "beoe.gov.pk":
            continue

        official_sources.append(
            source
        )

    # Remove duplicate URLs
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
# GENERAL DEPARTMENT RESEARCH
# ============================================================

def research_department(
    question,
    department,
    language,
):
    """
    General official government research.

    Uses the department's configured official domains.
    """

    from config.departments import DEPARTMENTS

    department_config = DEPARTMENTS.get(
        department,
        {},
    )

    official_domains = department_config.get(
        "official_domains",
        [],
    )

    jurisdiction = detect_jurisdiction(
        question
    )

    keywords = department_config.get(
        "keywords",
        [],
    )

    queries = []

    # --------------------------------------------------------
    # Primary query
    # --------------------------------------------------------

    queries.append(
        f"site:{official_domains[0] if official_domains else 'gov.pk'} "
        f"{question}"
    )

    # --------------------------------------------------------
    # Department keywords
    # --------------------------------------------------------

    keyword_text = " ".join(
        keywords[:8]
    )

    if keyword_text:
        queries.append(
            f"{keyword_text} {question}"
        )

    # --------------------------------------------------------
    # Explicit jurisdiction
    # --------------------------------------------------------

    if jurisdiction:

        queries.append(
            f"{jurisdiction} {question}"
        )

        for domain in official_domains:

            queries.append(
                f"site:{domain} "
                f"{jurisdiction} "
                f"{question}"
            )

    # --------------------------------------------------------
    # General official searches
    # --------------------------------------------------------

    for domain in official_domains:

        queries.append(
            f"site:{domain} {question}"
        )

    # --------------------------------------------------------
    # Three research attempts
    # --------------------------------------------------------

    for attempt in range(1, 4):

        sources = perform_search(
            queries=queries,
            official_domains=official_domains,
            max_results=8,
        )

        official_sources = []

        for source in sources:

            if not source.get("official"):
                continue

            official_sources.append(
                source
            )

        if official_sources:

            return {
                "sources": official_sources[:5],
                "rag_results": [],
                "jurisdiction": jurisdiction,
                "attempts": attempt,
            }

        # Broaden the next attempt
        queries.append(
            f"{department} Pakistan {question}"
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
    """
    Route the question to the appropriate
    specialized researcher.
    """

    # --------------------------------------------------------
    # NADRA
    # --------------------------------------------------------

    if department == "NADRA":

        return research_nadra(
            question,
            language,
        )

    # --------------------------------------------------------
    # PROTECTOR
    # --------------------------------------------------------

    if department == "Protector for Visa":

        return research_protector(
            question,
            language,
        )

    # --------------------------------------------------------
    # VACCINATION
    # --------------------------------------------------------

    if (
        department
        == "Vaccination for Travelling Abroad"
    ):

        return research_vaccination(
            question,
            language,
        )

    # --------------------------------------------------------
    # ALL OTHER DEPARTMENTS
    # --------------------------------------------------------

    return research_department(
        question,
        department,
        language,
    )
