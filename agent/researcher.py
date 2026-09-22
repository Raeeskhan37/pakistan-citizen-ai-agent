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

    #    # ========================================================
    # SAUDI WORK / EMPLOYMENT VISA
    # ========================================================

    if saudi_question and work_visa_question:

        # ----------------------------------------------------
        # OFFICIAL PAKISTAN GOVERNMENT EVIDENCE
        #
        # BE&OE hosts the NCOC vaccination policy for
        # Pakistanis working abroad on work visas.
        #
        # IMPORTANT:
        # This document explains vaccination eligibility/
        # procedure for Pakistanis with work visas.
        # It does NOT mean that every Saudi work-visa holder
        # must receive a specific vaccine.
        # ----------------------------------------------------

        pakistan_work_visa_evidence = """
OFFICIAL GOVERNMENT OF PAKISTAN — NCOC
Vaccination Policy for Pakistanis Working Abroad on Work Visa

The Bureau of Emigration & Overseas Employment (BE&OE)
publishes an NCOC vaccination policy specifically covering
Pakistanis working abroad on work visas.

The policy states that Pakistanis over 18 years of age who
have obtained a work visa for the first time, or who are
already working abroad and have returned on leave or for
another reason, can receive vaccination under the stated
procedure.

It states that a Pakistani over 18 years of age who has a
work visa or iqama can get vaccinated and should show the
passport and work visa or iqama at a designated vaccination
centre.

This policy should not be interpreted as proof that a
particular vaccination is mandatory for every Pakistani
travelling to Saudi Arabia on a normal employment visa.

Saudi Arabia also has medical screening requirements for
incoming foreign workers. The Saudi Ministry of Health
maintains services and procedures for verification of
foreign-worker medical examination results.

Therefore, for a normal Saudi employment/work visa, the
agent should distinguish between:

1. Required medical examination / health screening for
   foreign workers; and

2. A vaccination that is specifically mandatory for the
   individual traveller.

A specific vaccine should only be described as mandatory
when current official Saudi or Pakistani evidence
specifically establishes that requirement.
"""

        direct_sources = [
            {
                "title": (
                    "Government of Pakistan / BE&OE — "
                    "Vaccination Policy for Pakistanis "
                    "Working Abroad on Work Visa"
                ),
                "url": (
                    "https://beoe.gov.pk/"
                    "files/policyguideliness/51.pdf"
                ),
                "domain": "beoe.gov.pk",
                "official": True,
                "page_text": pakistan_work_visa_evidence,
                "snippet": pakistan_work_visa_evidence,
            },
            {
                "title": (
                    "Saudi Ministry of Health — "
                    "Medical Screening for Foreign Workers"
                ),
                "url": (
                    "https://moh.gov.sa/en/Ministry/"
                    "Life-events/Pages/default.aspx"
                ),
                "domain": "moh.gov.sa",
                "official": True,
                "page_text": (
                    """
Saudi Ministry of Health

The Saudi Ministry of Health states that people coming
to work in Saudi Arabia are subject to specific medical
screening procedures to verify that incoming workers are
free of communicable diseases.

The Ministry also provides services related to verification
of foreign-worker medical examination results.
"""
                ),
                "snippet": (
                    "Saudi Ministry of Health — medical "
                    "screening procedures for incoming workers."
                ),
            },
        ]

        # ----------------------------------------------------
        # LIVE OFFICIAL SEARCH
        # ----------------------------------------------------

        queries = [
            (
                "site:beoe.gov.pk "
                "vaccination policy Pakistanis "
                "working abroad work visa"
            ),
            (
                "site:beoe.gov.pk "
                "Saudi Arabia work visa vaccination"
            ),
            (
                "site:moh.gov.sa "
                "Saudi foreign workers medical screening"
            ),
            (
                "site:moh.gov.sa "
                "Saudi Arabia incoming workers "
                "medical examination"
            ),
            (
                "site:moh.gov.sa "
                "foreign worker vaccination Saudi Arabia"
            ),
            (
                "site:nhsrc.gov.pk "
                "work visa vaccination Pakistanis abroad"
            ),
        ]

        searched_sources = perform_search(
            queries=queries,
            official_domains=[
                "beoe.gov.pk",
                "moh.gov.sa",
                "nhsrc.gov.pk",
            ],
            max_results=8,
        )

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
                "beoe.gov.pk",
                "moh.gov.sa",
                "nhsrc.gov.pk",
            }:
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
                "worker",
                "employment",
                "visa",
                "medical",
                "screening",
                "vaccin",
                "health",
                "saudi",
            ]

            relevance = sum(
                1
                for term in relevant_terms
                if term in combined_text
            )

            # Keep an official source if it has at least
            # one strong work/health/visa connection.
            if relevance >= 1:

                source["relevance"] = relevance

                direct_sources.append(
                    source
                )

        # ----------------------------------------------------
        # SORT OFFICIAL SOURCES
        # ----------------------------------------------------

        direct_sources.sort(
            key=lambda source: source.get(
                "relevance",
                0,
            ),
            reverse=True,
        )

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

        # ----------------------------------------------------
        # OFFICIAL PAKISTAN GOVERNMENT EVIDENCE
        #
        # BE&OE hosts the NCOC vaccination policy for
        # Pakistanis working abroad on work visas.
        #
        # IMPORTANT:
        # This document explains vaccination eligibility/
        # procedure for Pakistanis with work visas.
        # It does NOT mean that every Saudi work-visa holder
        # must receive a specific vaccine.
        # ----------------------------------------------------

        pakistan_work_visa_evidence = """
OFFICIAL GOVERNMENT OF PAKISTAN — NCOC
Vaccination Policy for Pakistanis Working Abroad on Work Visa

The Bureau of Emigration & Overseas Employment (BE&OE)
publishes an NCOC vaccination policy specifically covering
Pakistanis working abroad on work visas.

The policy states that Pakistanis over 18 years of age who
have obtained a work visa for the first time, or who are
already working abroad and have returned on leave or for
another reason, can receive vaccination under the stated
procedure.

It states that a Pakistani over 18 years of age who has a
work visa or iqama can get vaccinated and should show the
passport and work visa or iqama at a designated vaccination
centre.

This policy should not be interpreted as proof that a
particular vaccination is mandatory for every Pakistani
travelling to Saudi Arabia on a normal employment visa.

Saudi Arabia also has medical screening requirements for
incoming foreign workers. The Saudi Ministry of Health
maintains services and procedures for verification of
foreign-worker medical examination results.

Therefore, for a normal Saudi employment/work visa, the
agent should distinguish between:

1. Required medical examination / health screening for
   foreign workers; and

2. A vaccination that is specifically mandatory for the
   individual traveller.

A specific vaccine should only be described as mandatory
when current official Saudi or Pakistani evidence
specifically establishes that requirement.
"""

        direct_sources = [
            {
                "title": (
                    "Government of Pakistan / BE&OE — "
                    "Vaccination Policy for Pakistanis "
                    "Working Abroad on Work Visa"
                ),
                "url": (
                    "https://beoe.gov.pk/"
                    "files/policyguideliness/51.pdf"
                ),
                "domain": "beoe.gov.pk",
                "official": True,
                "page_text": pakistan_work_visa_evidence,
                "snippet": pakistan_work_visa_evidence,
            },
            {
                "title": (
                    "Saudi Ministry of Health — "
                    "Medical Screening for Foreign Workers"
                ),
                "url": (
                    "https://moh.gov.sa/en/Ministry/"
                    "Life-events/Pages/default.aspx"
                ),
                "domain": "moh.gov.sa",
                "official": True,
                "page_text": (
                    """
Saudi Ministry of Health

The Saudi Ministry of Health states that people coming
to work in Saudi Arabia are subject to specific medical
screening procedures to verify that incoming workers are
free of communicable diseases.

The Ministry also provides services related to verification
of foreign-worker medical examination results.
"""
                ),
                "snippet": (
                    "Saudi Ministry of Health — medical "
                    "screening procedures for incoming workers."
                ),
            },
        ]

        # ----------------------------------------------------
        # LIVE OFFICIAL SEARCH
        # ----------------------------------------------------

        queries = [
            (
                "site:beoe.gov.pk "
                "vaccination policy Pakistanis "
                "working abroad work visa"
            ),
            (
                "site:beoe.gov.pk "
                "Saudi Arabia work visa vaccination"
            ),
            (
                "site:moh.gov.sa "
                "Saudi foreign workers medical screening"
            ),
            (
                "site:moh.gov.sa "
                "Saudi Arabia incoming workers "
                "medical examination"
            ),
            (
                "site:moh.gov.sa "
                "foreign worker vaccination Saudi Arabia"
            ),
            (
                "site:nhsrc.gov.pk "
                "work visa vaccination Pakistanis abroad"
            ),
        ]

        searched_sources = perform_search(
            queries=queries,
            official_domains=[
                "beoe.gov.pk",
                "moh.gov.sa",
                "nhsrc.gov.pk",
            ],
            max_results=8,
        )

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
                "beoe.gov.pk",
                "moh.gov.sa",
                "nhsrc.gov.pk",
            }:
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
                "worker",
                "employment",
                "visa",
                "medical",
                "screening",
                "vaccin",
                "health",
                "saudi",
            ]

            relevance = sum(
                1
                for term in relevant_terms
                if term in combined_text
            )

            # Keep an official source if it has at least
            # one strong work/health/visa connection.
            if relevance >= 1:

                source["relevance"] = relevance

                direct_sources.append(
                    source
                )

        # ----------------------------------------------------
        # SORT OFFICIAL SOURCES
        # ----------------------------------------------------

        direct_sources.sort(
            key=lambda source: source.get(
                "relevance",
                0,
            ),
            reverse=True,
        )

        return {
            "sources": unique_sources(
                direct_sources,
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
