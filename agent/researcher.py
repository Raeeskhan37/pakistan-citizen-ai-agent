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
# HELPER — UNIQUE SOURCES
# ============================================================

def unique_sources(sources, limit=5):
    unique = {}

    for source in sources:
        if not isinstance(source, dict):
            continue

        url = source.get("url", "")

        if not url:
            continue

        if url not in unique:
            unique[url] = source

    return list(unique.values())[:limit]


# ============================================================
# VACCINATION
# ============================================================

def research_vaccination(
    question,
    language,
):
    """
    Official vaccination research.

    Supported special cases:

    1. Hajj 2026
       Saudi MOH + Pakistan Ministry of Religious Affairs

    2. Umrah 2026
       Saudi Ministry of Health official Umrah
       health requirements

    3. Saudi work/employment visa
       Searches official Saudi MOH and Pakistan
       government health sources.

    4. General international travel
       Pakistan Ministry of NHSR&C + NIH
    """

    question_lower = question.lower()

    # ========================================================
    # QUESTION TYPE DETECTION
    # ========================================================

    hajj_question = any(
        term in question_lower
        for term in [
            "hajj",
            "haj",
        ]
    )

    umrah_question = any(
        term in question_lower
        for term in [
            "umrah",
            "umra",
        ]
    )

    saudi_question = any(
        term in question_lower
        for term in [
            "saudi",
            "saudi arabia",
            "kingdom of saudi",
        ]
    )

    work_visa_question = any(
        term in question_lower
        for term in [
            "work visa",
            "work visa",
            "employment visa",
            "employment",
            "job visa",
            "work permit",
            "working in saudi",
            "work in saudi",
            "job in saudi",
            "job in saudi arabia",
            "employment in saudi",
            "employment visa",
        ]
    )

    # ========================================================
    # HAJJ 2026
    # ========================================================

    if hajj_question:

        official_evidence = """
OFFICIAL SAUDI MINISTRY OF HEALTH — HAJJ 1447 / 2026

The Saudi Ministry of Health published official health
requirements for travelers coming to Saudi Arabia for
Hajj 1447H (2026).

For Pakistan:

Pakistan is listed in the Saudi Hajj health requirements
in relation to Wild Poliovirus 1 (WPV1).

The official Saudi health requirements state that travelers
from states reporting WPV1 or cVDPV1 may be administered
bivalent oral polio vaccine (bOPV) at points of entry,
according to the applicable Saudi health requirements.

The Saudi Ministry of Health also states that the
meningococcal (Neisseria) vaccine is mandatory for pilgrims
who have not received it within the previous five years.

Seasonal influenza and COVID-19 vaccination are described
as recommendations in the relevant 2026 Hajj material.

Do not describe every vaccine mentioned in the document
as mandatory for every Pakistani pilgrim unless the
official evidence specifically establishes that.
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
                    "Saudi MOH — Pilgrim's Health"
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
Saudi Ministry of Health — 27 February 2026

The meningococcal (Neisseria) vaccine is mandatory
for pilgrims who have not received it within the
previous five years.

Seasonal influenza and COVID-19 vaccination were
also discussed as recommendations.
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
Pakistan Ministry of Religious Affairs

Saudi Government Health Instructions for Hajj - 2026.
"""
                ),
                "snippet": (
                    "Saudi Government Health Instructions "
                    "for Hajj - 2026."
                ),
            },
        ]

        searched_sources = perform_search(
            queries=[
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
                    "Hajj 2026 health instructions"
                ),
            ],
            official_domains=[
                "moh.gov.sa",
                "mora.gov.pk",
            ],
            max_results=8,
        )

        for source in searched_sources:
            if not source.get("official"):
                continue

            domain = (
                source.get("domain", "")
                .lower()
                .replace("www.", "")
            )

            if domain not in {
                "moh.gov.sa",
                "mora.gov.pk",
            }:
                continue

            direct_sources.append(source)

        return {
            "sources": unique_sources(
                direct_sources,
                limit=5,
            ),
            "rag_results": [],
            "jurisdiction": None,
            "attempts": 1,
        }

    # ========================================================
    # UMRAH 1447H / 2026
    # ========================================================

    if umrah_question:

        # ----------------------------------------------------
        # This is the official Saudi MOH Umrah 1447H/2026
        # document. It specifically lists Pakistan under
        # WPV1 countries.
        # ----------------------------------------------------

        official_evidence = """
OFFICIAL SAUDI MINISTRY OF HEALTH
HEALTH REQUIREMENTS FOR UMRAH — 1447H / 2026

The Saudi Ministry of Health's official document is titled:

"Health Requirements and Recommendations for Travelers
to Saudi Arabia for Umrah - 1447H (2026)"

Meningococcal meningitis:

All individuals intending to perform Umrah from all
countries are required to receive an approved meningococcal
vaccine before travelling to Saudi Arabia.

Approved options include:

1. Meningococcal quadrivalent (ACYW) conjugate vaccine
   or pentavalent (ACYWX) conjugate vaccine, received
   within the last 5 years and at least 10 days before
   arrival.

2. Meningococcal quadrivalent (ACYW) polysaccharide
   vaccine, received within the last 3 years and at least
   10 days before arrival.

The vaccine name and administration date should be shown
on the vaccination certificate. If the vaccine type is
not indicated, the certificate is considered valid for
3 years from the administration date.

Polio:

Pakistan is specifically listed under countries reporting
WPV1.

Individuals arriving from Pakistan are required to have
at least one dose of either bivalent oral polio vaccine
(bOPV) or inactivated polio vaccine (IPV) before travelling
to Saudi Arabia.

This requirement applies regardless of age or previous
vaccination status according to the 1447H/2026 Umrah
health document.

COVID-19:

Certain higher-risk Umrah travelers are required to have
proof of COVID-19 vaccination or immunity before travel.
The groups specified by Saudi MOH include people over
65 years of age, pregnant women, and people with certain
chronic diseases or immunodeficiency.

Yellow fever:

This applies to travelers arriving from countries listed
by Saudi MOH as areas at risk of yellow fever transmission.
Pakistan is not listed in that yellow-fever table.

Routine vaccinations are also recommended to be up to date.
"""

        direct_sources = [
            {
                "title": (
                    "Saudi MOH — Health Requirements and "
                    "Recommendations for Travelers to "
                    "Saudi Arabia for Umrah - 1447H (2026)"
                ),
                "url": (
                    "https://www.moh.gov.sa/"
                    "en/HealthAwareness/Pilgrims-Health/"
                    "Documents/Health-Regulations-Umrah-EN.pdf"
                ),
                "domain": "moh.gov.sa",
                "official": True,
                "page_text": official_evidence,
                "snippet": official_evidence,
            },
            {
                "title": (
                    "Saudi MOH — Pilgrim's Health"
                ),
                "url": (
                    "https://www.moh.gov.sa/"
                    "en/healthawareness/pilgrims-health/"
                    "pages/default.aspx"
                ),
                "domain": "moh.gov.sa",
                "official": True,
                "page_text": official_evidence,
                "snippet": (
                    "Saudi Ministry of Health Pilgrim's "
                    "Health page containing the official "
                    "Umrah 1447H/2026 health requirements."
                ),
            },
        ]

        searched_sources = perform_search(
            queries=[
                (
                    "site:moh.gov.sa "
                    "Umrah 1447 2026 "
                    "Health Regulations Pakistan polio"
                ),
                (
                    "site:moh.gov.sa "
                    "Umrah 2026 meningococcal vaccine"
                ),
                (
                    "site:moh.gov.sa "
                    "Umrah 2026 Pakistan vaccination"
                ),
            ],
            official_domains=[
                "moh.gov.sa",
            ],
            max_results=8,
        )

        for source in searched_sources:

            if not source.get("official"):
                continue

            domain = (
                source.get("domain", "")
                .lower()
                .replace("www.", "")
            )

            if domain != "moh.gov.sa":
                continue

            direct_sources.append(source)

        return {
            "sources": unique_sources(
                direct_sources,
                limit=5,
            ),
            "rag_results": [],
            "jurisdiction": None,
            "attempts": 1,
        }

    # ========================================================
    # SAUDI WORK / EMPLOYMENT VISA
    # ========================================================

    if saudi_question and work_visa_question:

        queries = [
            (
                "site:moh.gov.sa "
                "Saudi Arabia work visa "
                "vaccination Pakistan"
            ),
            (
                "site:moh.gov.sa "
                "employment visa vaccination "
                "Saudi Arabia"
            ),
            (
                "site:moh.gov.sa "
                "medical examination foreign workers "
                "Saudi Arabia"
            ),
            (
                "site:gov.sa "
                "work visa vaccination "
                "Saudi Arabia Pakistan"
            ),
            (
                "site:mofa.gov.sa "
                "employment visa health "
                "requirements Pakistan"
            ),
            (
                "site:beoe.gov.pk "
                "Saudi Arabia medical vaccination "
                "work visa"
            ),
            (
                "site:nhsrc.gov.pk "
                "Saudi Arabia work visa vaccination"
            ),
        ]

        sources = perform_search(
            queries=queries,
            official_domains=[
                "moh.gov.sa",
                "gov.sa",
                "mofa.gov.sa",
                "beoe.gov.pk",
                "nhsrc.gov.pk",
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

            allowed_domains = {
                "moh.gov.sa",
                "gov.sa",
                "mofa.gov.sa",
                "beoe.gov.pk",
                "nhsrc.gov.pk",
            }

            if domain not in allowed_domains:
                continue

            combined_text = (
                str(
                    source.get(
                        "title",
                        "",
                    )
                )
                + " "
                + str(
                    source.get(
                        "snippet",
                        "",
                    )
                )
                + " "
                + str(
                    source.get(
                        "page_text",
                        "",
                    )
                )
            ).lower()

            relevant_terms = [
                "work",
                "employment",
                "visa",
                "medical",
                "vaccin",
                "health",
                "saudi",
                "worker",
            ]

            relevance = sum(
                1
                for term in relevant_terms
                if term in combined_text
            )

            if relevance >= 2:

                source["relevance"] = (
                    relevance
                )

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

        # ----------------------------------------------------
        # IMPORTANT:
        # Do not manufacture a work-visa vaccination rule
        # if official current evidence is not available.
        # ----------------------------------------------------

        if not official_sources:

            return {
                "sources": [],
                "rag_results": [],
                "jurisdiction": None,
                "attempts": 3,
            }

        return {
            "sources": unique_sources(
                official_sources,
                limit=5,
            ),
            "rag_results": [],
            "jurisdiction": None,
            "attempts": 1,
        }

    # ========================================================
    # GENERAL INTERNATIONAL TRAVEL VACCINATION
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

    return {
        "sources": unique_sources(
            official_sources,
            limit=5,
        ),
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

    official_sources = [
        source
        for source in sources
        if source.get("official")
    ]

    return {
        "sources": unique_sources(
            official_sources,
            limit=5,
        ),
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

    return {
        "sources": unique_sources(
            official_sources,
            limit=5,
        ),
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

        official_sources = [
            source
            for source in sources
            if source.get("official")
        ]

        if official_sources:

            return {
                "sources": unique_sources(
                    official_sources,
                    limit=5,
                ),
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
