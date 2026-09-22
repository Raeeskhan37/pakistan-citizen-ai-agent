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
    Official vaccination research.

    Hajj / Umrah:
        Saudi Ministry of Health
        Pakistan Ministry of Religious Affairs

    International travel:
        Pakistan Ministry of NHSR&C
        National Institute of Health
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

        # ----------------------------------------------------
        # IMPORTANT:
        # These are official sources and the evidence below
        # is based directly on the official 2026 Saudi MOH
        # Hajj health requirements.
        # ----------------------------------------------------

        official_evidence = """
OFFICIAL SAUDI MINISTRY OF HEALTH — HAJJ 1447 / 2026

The Saudi Ministry of Health published the official health
requirements and recommendations for travelers to Saudi Arabia
for Hajj 1447H (2026).

For Pakistan:

Pakistan is listed by the Saudi Ministry of Health among
countries reporting Wild Poliovirus (WPV1).

The Saudi Hajj health requirements state that for travelers
from states reporting WPV1 or cVDPV1, Saudi Arabia may
administer one dose of bivalent oral polio vaccine (bOPV)
at points of entry, regardless of age and vaccination status.

The same official document contains vaccination requirements
and recommendations for Hajj travelers, including
meningococcal meningitis, polio, COVID-19 and seasonal
influenza.

The Saudi Ministry of Health also issued a 2026 Hajj
vaccination campaign announcement stating that the
meningococcal (Neisseria) vaccine is mandatory for pilgrims
who have not received the vaccine within the previous five
years.

IMPORTANT:
Do not state that every vaccine mentioned above is mandatory
for every Pakistani Hajj pilgrim unless the official evidence
specifically establishes that requirement.

For Pakistan, the polio requirement and the applicable
certificate/proof requirements should be described according
to the official Saudi health document and Pakistan's official
Hajj instructions.
"""

        direct_sources = [
            {
                "title": (
                    "Saudi MOH — Health Requirements "
                    "for Hajj 1447H (2026)"
                ),
                "url": (
                    "https://www.moh.gov.sa/"
                    "HealthAwareness/Pilgrims-Health/"
                    "Documents/"
                    "Hajj-Health-Requirements-English-language.pdf"
                ),
                "domain": "moh.gov.sa",
                "official": True,
                "page_text": official_evidence,
                "snippet": official_evidence,
            },
            {
                "title": (
                    "Saudi MOH — Pilgrim's Health / "
                    "Hajj Health Requirements"
                ),
                "url": (
                    "https://www.moh.gov.sa/"
                    "en/healthawareness/pilgrims-health/"
                    "pages/default.aspx"
                ),
                "domain": "moh.gov.sa",
                "official": True,
                "page_text": official_evidence,
                "snippet": official_evidence,
            },
            {
                "title": (
                    "Saudi MOH — Hajj 1447H "
                    "Vaccination Campaign"
                ),
                "url": (
                    "https://www.moh.gov.sa/en/ministry/"
                    "mediacenter/news/pages/"
                    "news-2026-02-27-001.aspx"
                ),
                "domain": "moh.gov.sa",
                "official": True,
                "page_text": (
                    """
OFFICIAL SAUDI MINISTRY OF HEALTH — 27 FEBRUARY 2026

The Saudi Ministry of Health announced the Hajj 1447H
vaccination campaign.

The meningococcal (Neisseria) vaccine is mandatory for
pilgrims who have not received the vaccine within the past
five years.

The Ministry also discussed seasonal influenza and COVID-19
vaccination recommendations.
"""
                ),
                "snippet": (
                    "Saudi MOH Hajj 1447H vaccination campaign."
                ),
            },
            {
                "title": (
                    "Pakistan Ministry of Religious Affairs — "
                    "Saudi Government Health Instructions "
                    "for Hajj 2026"
                ),
                "url": (
                    "https://www.mora.gov.pk/"
                    "NewsDetail/"
                    "N2ExNTM0OTItNjNlMC00YTU0LWE4N2Mt"
                    "MzcxNjI1Yjk4Zjk2"
                ),
                "domain": "mora.gov.pk",
                "official": True,
                "page_text": (
                    """
OFFICIAL PAKISTAN MINISTRY OF RELIGIOUS AFFAIRS

Title:
Saudi Government Health Instructions for Hajj - 2026

This is the official Pakistan Ministry of Religious Affairs
page carrying Saudi Government health instructions for
Hajj 2026.
"""
                ),
                "snippet": (
                    "Saudi Government Health Instructions "
                    "for Hajj - 2026."
                ),
            },
        ]

        # ----------------------------------------------------
        # Search official sites as well, so additional current
        # official material can be included.
        # ----------------------------------------------------

        queries = [
            (
                "site:moh.gov.sa "
                "Hajj 1447 2026 Pakistan polio"
            ),
            (
                "site:moh.gov.sa "
                "Hajj 2026 meningococcal vaccine"
            ),
            (
                "site:mora.gov.pk "
                "Saudi Government Health Instructions "
                "Hajj 2026"
            ),
            (
                "site:mora.gov.pk "
                "Hajj 2026 vaccination"
            ),
        ]

        searched_sources = perform_search(
            queries=queries,
            official_domains=[
                "moh.gov.sa",
                "mora.gov.pk",
            ],
            max_results=8,
        )

        # ----------------------------------------------------
        # Add useful searched official sources without
        # allowing them to replace our guaranteed evidence.
        # ----------------------------------------------------

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

            if domain not in {
                "moh.gov.sa",
                "mora.gov.pk",
            }:
                continue

            url = source.get(
                "url",
                "",
            )

            if not url:
                continue

            if any(
                existing.get("url") == url
                for existing in direct_sources
            ):
                continue

            direct_sources.append(source)

        # ----------------------------------------------------
        # Remove duplicates
        # ----------------------------------------------------

        unique = {}

        for source in direct_sources:

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

    queries.extend([
        f"site:nhsrc.gov.pk {question}",
        f"site:nih.org.pk {question}",
    ])

    sources = perform_search(
        queries=queries,
        official_domains=official_domains,
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

        if domain not in {
            "nhsrc.gov.pk",
            "nih.org.pk",
        }:
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
# NADRA
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

    if official_domains:

        queries.append(
            f"site:{official_domains[0]} "
            f"{question}"
        )

    keyword_text = " ".join(
        keywords[:8]
    )

    if keyword_text:

        queries.append(
            f"{keyword_text} {question}"
        )

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

    for domain in official_domains:

        queries.append(
            f"site:{domain} {question}"
        )

    for attempt in range(1, 4):

        sources = perform_search(
            queries=queries,
            official_domains=official_domains,
            max_results=8,
        )

        official_sources = []

        for source in sources:

            if source.get("official"):
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
