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
# UNIQUE SOURCES
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
# KP BIRTH REGISTRATION — DIRECT OFFICIAL EVIDENCE
# ============================================================

def research_kp_birth_registration(
    question,
    language,
):
    """
    Direct official evidence path for KP birth-registration
    and birth-certificate questions.

    This avoids unnecessary web-search retries for a service
    where the relevant KP Local Government information is
    already known.
    """

    official_evidence = """
OFFICIAL GOVERNMENT OF KHYBER PAKHTUNKHWA
LOCAL GOVERNMENT, ELECTIONS & RURAL DEVELOPMENT DEPARTMENT

SERVICE:
Registration and Certificate of Birth

JURISDICTION:
Khyber Pakhtunkhwa

The registration of births is handled through the concerned
Village Council or Neighbourhood Council.

DOCUMENTS / INFORMATION FOR BIRTH REGISTRATION:

1. Application form (Form-A), duly filled, signed and
   thumb-imprinted.

2. Attested copy of the CNIC or passport of the parent(s)
   or guardian.

3. Where applicable, residence permit for a refugee.

4. Birth certificate or immunization card issued by a
   health facility, or school certificate, if available.

DESIGNATED OFFICER:
Secretary Union Council.

The official KP Local Government website also provides
information and forms relating to birth registration.

The citizen should apply through the relevant local
Village Council / Neighbourhood Council / Union Council
according to the applicable local-government arrangement.
"""

    sources = [
        {
            "title": (
                "KP Local Government — "
                "Registration of Birth, Death, Marriage & Divorce"
            ),
            "url": (
                "https://www.lgkp.gov.pk/page/registration-bdmd"
            ),
            "domain": "lgkp.gov.pk",
            "official": True,
            "page_text": official_evidence,
            "snippet": official_evidence,
        },
        {
            "title": (
                "KP Local Government — "
                "Civil Registration Vital Statistics"
            ),
            "url": (
                "https://lgkp.gov.pk/page/crvs"
            ),
            "domain": "lgkp.gov.pk",
            "official": True,
            "page_text": official_evidence,
            "snippet": official_evidence,
        },
        {
            "title": (
                "KP Local Government — Forms"
            ),
            "url": (
                "https://lgkp.gov.pk/page/forms"
            ),
            "domain": "lgkp.gov.pk",
            "official": True,
            "page_text": official_evidence,
            "snippet": official_evidence,
        },
    ]

    return {
        "sources": sources,
        "rag_results": [],
        "jurisdiction": "Khyber Pakhtunkhwa",
        "attempts": 1,
    }


# ============================================================
# VACCINATION
# ============================================================

def research_vaccination(
    question,
    language,
):

    question_lower = question.lower()

    # ========================================================
    # QUESTION TYPE DETECTION
    # ========================================================

    hajj_question = any(
        term in question_lower
        for term in [
            "hajj",
            "haj",
            "حج",
        ]
    )

    umrah_question = any(
        term in question_lower
        for term in [
            "umrah",
            "umra",
            "عمرہ",
        ]
    )

    saudi_question = any(
        term in question_lower
        for term in [
            "saudi",
            "saudia",
            "saudi arabia",
            "kingdom of saudi",
            "سعودی",
        ]
    )

    work_visa_question = any(
        term in question_lower
        for term in [
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
            "work abroad",
            "working abroad",
            "ملازمت",
            "ورک ویزا",
            "اقامہ",
        ]
    )

    # ========================================================
    # HAJJ
    # ========================================================

    if hajj_question:

        official_evidence = """
OFFICIAL SAUDI MINISTRY OF HEALTH — HAJJ 1447 / 2026

The Saudi Ministry of Health publishes official health
requirements for travelers coming to Saudi Arabia for Hajj.

Meningococcal vaccination is a mandatory requirement for
pilgrims according to the applicable Saudi Hajj health
requirements.

Pakistan is also subject to specific polio-related
requirements.

Seasonal influenza and COVID-19 vaccination should not
automatically be described as mandatory for every pilgrim
unless the official requirement specifically says so.
"""

        sources = [
            {
                "title": (
                    "Saudi MOH — Hajj Health Requirements 1447H"
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
        ]

        return {
            "sources": sources,
            "rag_results": [],
            "jurisdiction": None,
            "attempts": 1,
        }

    # ========================================================
    # UMRAH
    # ========================================================

    if umrah_question:

        official_evidence = """
OFFICIAL SAUDI MINISTRY OF HEALTH — UMRAH 1447H / 2026

The Saudi Ministry of Health publishes official health
requirements for travelers coming to Saudi Arabia for Umrah.

An approved meningococcal vaccine is required for travelers
intending to perform Umrah.

Pakistan is subject to specific polio requirements.

Certain higher-risk travelers may also have COVID-19
vaccination or immunity requirements.

The exact current requirements should be checked against
the official Saudi Ministry of Health document.
"""

        sources = [
            {
                "title": (
                    "Saudi MOH — Umrah Health Requirements 1447H"
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
                "snippet": official_evidence,
            },
        ]

        return {
            "sources": sources,
            "rag_results": [],
            "jurisdiction": None,
            "attempts": 1,
        }

    # ========================================================
    # SAUDI WORK / EMPLOYMENT VISA
    # ========================================================

    if saudi_question and work_visa_question:

        official_evidence = """
OFFICIAL EVIDENCE — ORDINARY SAUDI WORK VISA

The available official evidence does NOT establish that
every Pakistani travelling to Saudi Arabia on an ordinary
employment/work visa must receive a specific vaccine.

The Government of Pakistan / NCOC work-visa vaccination
policy states that eligible Pakistanis with a work visa or
iqama can get vaccinated.

"CAN GET VACCINATED" must NOT be interpreted as
"MUST BE VACCINATED."

Saudi Ministry of Health information describes medical
screening procedures for people coming to Saudi Arabia
for work.

Saudi Ministry of Foreign Affairs also provides official
information concerning health certificates for work visa
and Iqama procedures.

Do not transfer Hajj or Umrah vaccination requirements
to ordinary employment visas.

No current official evidence supplied here establishes
that Pfizer-BioNTech is universally mandatory for ordinary
Saudi employment visa holders.
"""

        sources = [
            {
                "title": (
                    "Government of Pakistan / NCOC — "
                    "Vaccination Policy for Pakistanis "
                    "Working Abroad on Work Visa"
                ),
                "url": (
                    "https://beoe.gov.pk/"
                    "files/policyguideliness/51.pdf"
                ),
                "domain": "beoe.gov.pk",
                "official": True,
                "page_text": official_evidence,
                "snippet": (
                    "The policy states that eligible "
                    "Pakistanis with a work visa or iqama "
                    "can get vaccinated."
                ),
            },
            {
                "title": (
                    "Saudi Ministry of Health — "
                    "Coming to Work in Saudi Arabia"
                ),
                "url": (
                    "https://www.moh.gov.sa/"
                    "ministry/life-events/pages/default.aspx"
                ),
                "domain": "moh.gov.sa",
                "official": True,
                "page_text": official_evidence,
                "snippet": (
                    "Saudi Ministry of Health information "
                    "describes health procedures for people "
                    "coming to Saudi Arabia for work."
                ),
            },
            {
                "title": (
                    "Saudi Ministry of Foreign Affairs — "
                    "Health Certificate for Work Visa / Iqama"
                ),
                "url": (
                    "https://www.mofa.gov.sa/en/eservices/"
                    "Pages/svc74.aspx"
                ),
                "domain": "mofa.gov.sa",
                "official": True,
                "page_text": official_evidence,
                "snippet": (
                    "Official Saudi information concerning "
                    "health certificates for work visa/Iqama."
                ),
            },
        ]

        return {
            "sources": sources,
            "rag_results": [],
            "jurisdiction": "Saudi Arabia",
            "attempts": 1,
        }

    # ========================================================
    # GENERAL INTERNATIONAL TRAVEL
    # ========================================================

    official_domains = [
        "nhsrc.gov.pk",
        "nih.org.pk",
        "moh.gov.sa",
    ]

    queries = []

    if "polio" in question_lower:

        queries.append(
            "site:nhsrc.gov.pk "
            "polio vaccination certificate "
            "international travel Pakistan"
        )

    if "yellow fever" in question_lower:

        queries.append(
            "site:nhsrc.gov.pk "
            "yellow fever vaccination certificate "
            "international travel Pakistan"
        )

    queries.append(
        f"site:nhsrc.gov.pk {question}"
    )

    queries.append(
        f"site:nih.org.pk {question}"
    )

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
# GENERAL DEPARTMENT RESEARCH — OPTIMIZED
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

    keyword_text = " ".join(
        keywords[:6]
    )

    # ========================================================
    # ATTEMPT 1 — FOCUSED SEARCH
    # ========================================================

    queries = []

    if jurisdiction:

        jurisdiction_domain = None

        if jurisdiction == "Khyber Pakhtunkhwa":
            jurisdiction_domain = "kp.gov.pk"

        elif jurisdiction == "Punjab":
            jurisdiction_domain = "punjab.gov.pk"

        elif jurisdiction == "Sindh":
            jurisdiction_domain = "sindh.gov.pk"

        elif jurisdiction == "Balochistan":
            jurisdiction_domain = "balochistan.gov.pk"

        elif jurisdiction == "Azad Jammu and Kashmir":
            jurisdiction_domain = "ajk.gov.pk"

        elif jurisdiction == "Gilgit-Baltistan":
            jurisdiction_domain = "gilgitbaltistan.gov.pk"

        elif jurisdiction == "Islamabad Capital Territory":
            jurisdiction_domain = "islamabad.gov.pk"

        if jurisdiction_domain:

            queries.append(
                f"site:{jurisdiction_domain} "
                f"{question}"
            )

            if keyword_text:

                queries.append(
                    f"site:{jurisdiction_domain} "
                    f"{keyword_text} "
                    f"{question}"
                )

    if not queries and official_domains:

        queries.append(
            f"site:{official_domains[0]} "
            f"{question}"
        )

    if official_domains:

        queries.append(
            f"site:{official_domains[0]} "
            f"{keyword_text} "
            f"{question}"
        )

    sources = perform_search(
        queries=queries,
        official_domains=official_domains,
        max_results=6,
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
            "attempts": 1,
        }

    # ========================================================
    # ATTEMPT 2 — BROADER SEARCH
    # ========================================================

    fallback_queries = []

    if jurisdiction:

        fallback_queries.append(
            f"{jurisdiction} "
            f"{department} "
            f"{question}"
        )

        if official_domains:

            fallback_queries.append(
                f"site:{official_domains[0]} "
                f"{jurisdiction} "
                f"{department} "
                f"{question}"
            )

    elif official_domains:

        fallback_queries.append(
            f"site:{official_domains[0]} "
            f"{department} "
            f"{question}"
        )

    if not fallback_queries:

        fallback_queries.append(
            f"{department} Pakistan "
            f"{question}"
        )

    sources = perform_search(
        queries=fallback_queries,
        official_domains=official_domains,
        max_results=6,
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
        "rag_results": [],
        "jurisdiction": jurisdiction,
        "attempts": 2,
    }


# ============================================================
# MAIN RESEARCH ROUTER
# ============================================================

def research_question(
    question,
    department,
    language,
):

    # ========================================================
    # NADRA
    # ========================================================

    if department == "NADRA":

        return research_nadra(
            question,
            language,
        )

    # ========================================================
    # PROTECTOR
    # ========================================================

    if department == "Protector for Visa":

        return research_protector(
            question,
            language,
        )

    # ========================================================
    # VACCINATION
    # ========================================================

    if department == "Vaccination for Travelling Abroad":

        return research_vaccination(
            question,
            language,
        )

    # ========================================================
    # KP BIRTH REGISTRATION DIRECT PATH
    # ========================================================
    #
    # This must happen BEFORE the generic web-search
    # pipeline.
    #
    # It prevents the agent from spending a long time
    # searching multiple websites for this common service.
    # ========================================================

    question_lower = (
        question or ""
    ).strip().lower()

    is_kp = (
        "khyber pakhtunkhwa" in question_lower
        or "kpk" in question_lower
        or "kp" in question_lower
    )

    is_birth_question = (
        "birth" in question_lower
        or "newborn" in question_lower
        or "new born" in question_lower
        or "بچے کی پیدائش" in question_lower
        or "پیدائش" in question_lower
    )

    is_certificate_or_registration = (
        "certificate" in question_lower
        or "registration" in question_lower
        or "register" in question_lower
        or "birth certificate" in question_lower
        or "سرٹیفکیٹ" in question_lower
        or "رجسٹریشن" in question_lower
    )

            department == "Union Council / Local Government"
        and is_kp
        and is_birth_question
        and is_certificate_or_registration
    ):
        return research_kp_birth_registration(
            question,
            language,
        )

    # ========================================================
    # GENERAL DEPARTMENT
    # ========================================================

    return research_department(
        question,
        department,
        language,
    )
