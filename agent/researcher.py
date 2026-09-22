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
    Targeted official search for international-travel
    vaccination information in Pakistan.

    Primary authority:
    Ministry of National Health Services / NIH.

    Do not broaden this search to unrelated government
    departments.
    """

    question_lower = question.lower()

    queries = [
        f"site:nhsrc.gov.pk {question}",
        f"site:nhsrc.gov.pk polio yellow fever vaccination certificate NIMS {question}",
        f"site:nhsrc.gov.pk international travellers vaccination certificate Pakistan",
        f"site:nih.org.pk polio yellow fever vaccination certificate international travel",
        f"site:nih.org.pk designated vaccination center international travelers",
    ]

    # Make specific questions even more targeted.
    if "polio" in question_lower:
        queries.insert(
            0,
            (
                "site:nhsrc.gov.pk "
                "polio vaccination certificate "
                "international travel NIMS Pakistan"
            ),
        )

    if "yellow fever" in question_lower:
        queries.insert(
            0,
            (
                "site:nhsrc.gov.pk "
                "yellow fever vaccination certificate "
                "international travel NIMS Pakistan"
            ),
        )

    if "nims" in question_lower:
        queries.insert(
            0,
            (
                "site:nhsrc.gov.pk "
                "NIMS vaccination certificate "
                "polio yellow fever"
            ),
        )

    if (
        "certificate" in question_lower
        or "certificate" in question_lower
    ):
        queries.insert(
            0,
            (
                "site:nhsrc.gov.pk "
                "digital vaccination certificate "
                "NIMS polio yellow fever"
            ),
        )

    sources = perform_search(
        queries=queries,
        official_domains=[
            "nhsrc.gov.pk",
            "nih.org.pk",
        ],
        max_results=8,
    )

    official_sources = [
def research_vaccination(
    question,
    language,
):
    """
    Targeted official search for international-travel
    vaccination information in Pakistan.

    Only NHSRC and NIH sources are accepted.
    """

    question_lower = question.lower()

    queries = [
        (
            "site:nhsrc.gov.pk "
            "polio vaccination certificate "
            "international travel Pakistan"
        ),
        (
            "site:nhsrc.gov.pk "
            "yellow fever vaccination certificate "
            "international travel Pakistan"
        ),
        (
            "site:nhsrc.gov.pk "
            "NIMS vaccination certificate "
            "polio yellow fever"
        ),
        (
            "site:nih.org.pk "
            "polio vaccination certificate "
            "international travel Pakistan"
        ),
        (
            "site:nih.org.pk "
            "yellow fever vaccination certificate "
            "international travel Pakistan"
        ),
    ]

    # Add the citizen's exact question as a final
    # targeted search.
    queries.append(
        f"site:nhsrc.gov.pk {question}"
    )

    queries.append(
        f"site:nih.org.pk {question}"
    )

    sources = perform_search(
        queries=queries,
        official_domains=[
            "nhsrc.gov.pk",
            "nih.org.pk",
        ],
        max_results=8,
    )

    # HARD FILTER:
    # Vaccination must only use these two domains.
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

        official_sources.append(
            source
        )

    # Remove duplicate URLs.
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
        unique.values()
    )

    return {
        "sources": official_sources[:5],
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
        f"site:beoe.gov.pk emigrant protection documents",
        f"site:beoe.gov.pk protector clearance procedure",
        f"site:beoe.gov.pk direct emigrants registration",
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

    queries = []

    # Main question.
    queries.append(
        question
    )

    # Department-focused search.
    queries.append(
        f"{department} {question}"
    )

    # Add jurisdiction when explicitly specified.
    if jurisdiction:
        queries.append(
            f"{jurisdiction} {department} {question}"
        )

    # Add useful department keywords.
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

        # Broaden only if the first attempt failed.
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

    # NADRA uses RAG + official web search.
    if department == "NADRA":
        return research_nadra(
            question,
            language,
        )

    # Protector has its own targeted official search.
    if department == "Protector for Visa":
        return research_protector(
            question,
            language,
        )

    # Vaccination has its own targeted official search.
    if (
        department
        == "Vaccination for Travelling Abroad"
    ):
        return research_vaccination(
            question,
            language,
        )

    # All remaining departments.
    return research_department(
        question,
        department,
        language,
    )
