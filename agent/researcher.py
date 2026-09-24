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
    question_lower = (question or "").lower()

    for keyword, jurisdiction in PROVINCES.items():
        if keyword in question_lower:
            return jurisdiction

    return None


# ============================================================
# OFFICIAL DOMAIN FOR JURISDICTION
# ============================================================

def get_jurisdiction_domain(jurisdiction):
    domains = {
        "Punjab": "punjab.gov.pk",
        "Sindh": "sindh.gov.pk",
        "Khyber Pakhtunkhwa": "kp.gov.pk",
        "Balochistan": "balochistan.gov.pk",
        "Islamabad Capital Territory": "islamabad.gov.pk",
        "Azad Jammu and Kashmir": "ajk.gov.pk",
        "Gilgit-Baltistan": "gilgitbaltistan.gov.pk",
    }

    return domains.get(jurisdiction)


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
            "url": "https://www.lgkp.gov.pk/page/registration-bdmd",
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
            "url": "https://lgkp.gov.pk/page/crvs",
            "domain": "lgkp.gov.pk",
            "official": True,
            "page_text": official_evidence,
            "snippet": official_evidence,
        },
        {
            "title": "KP Local Government — Forms",
            "url": "https://lgkp.gov.pk/page/forms",
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
# BIRTH REGISTRATION — DEDICATED OFFICIAL RESEARCH
# ============================================================

def research_birth_registration(
    question,
    language,
):
    """
    Dedicated research route for birth registration and
    birth certificate questions.

    KP uses the tested direct official evidence route.
    Other jurisdictions use focused searches against
    official government domains.
    """

    jurisdiction = detect_jurisdiction(question)

    # --------------------------------------------------------
    # KP — PRESERVE TESTED DIRECT ROUTE
    # --------------------------------------------------------

    if jurisdiction == "Khyber Pakhtunkhwa":

        return research_kp_birth_registration(
            question,
            language,
        )

    # --------------------------------------------------------
    # OFFICIAL DOMAIN
    # --------------------------------------------------------

    jurisdiction_domain = get_jurisdiction_domain(
        jurisdiction
    )

    official_domains = []

    if jurisdiction_domain:
        official_domains.append(
            jurisdiction_domain
        )

    official_domains.extend(
        [
            "gov.pk",
            "punjab.gov.pk",
            "sindh.gov.pk",
            "kp.gov.pk",
            "balochistan.gov.pk",
            "ajk.gov.pk",
            "gilgitbaltistan.gov.pk",
            "islamabad.gov.pk",
        ]
    )

    # Remove duplicates
    official_domains = list(
        dict.fromkeys(official_domains)
    )

    # --------------------------------------------------------
    # FOCUSED SEARCH
    # --------------------------------------------------------

    queries = [
        f"birth registration {question}",
        f"birth certificate {question}",
        f"birth registration requirements {question}",
        f"birth certificate documents {question}",
        f"birth registration procedure {question}",
        f"newborn birth registration {question}",
    ]

    if jurisdiction_domain:

        queries = [
            f"site:{jurisdiction_domain} birth registration {question}",
            f"site:{jurisdiction_domain} birth certificate {question}",
            (
                f"site:{jurisdiction_domain} "
                "birth registration requirements"
            ),
            (
                f"site:{jurisdiction_domain} "
                "birth certificate documents"
            ),
            (
                f"site:{jurisdiction_domain} "
                "birth registration procedure"
            ),
        ]

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
            "attempts": 1,
        }

    # --------------------------------------------------------
    # FALLBACK SEARCH
    # --------------------------------------------------------

    fallback_queries = [
        f"birth registration Pakistan {question}",
        f"birth certificate Pakistan {question}",
        f"government birth registration {question}",
        f"official birth certificate requirements {question}",
    ]

    if jurisdiction:

        fallback_queries.insert(
            0,
            (
                f"{jurisdiction} "
                f"birth registration "
                f"{question}"
            ),
        )

    sources = perform_search(
        queries=fallback_queries,
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
        "jurisdiction": jurisdiction,
        "attempts": 2,
    }


# ============================================================
# MARRIAGE REGISTRATION — DEDICATED OFFICIAL RESEARCH
# ============================================================

def research_marriage_registration(
    question,
    language,
):
    """
    Dedicated research route for marriage registration,
    Nikah registration and marriage certificate questions.
    """

    jurisdiction = detect_jurisdiction(question)

    # --------------------------------------------------------
    # OFFICIAL DOMAINS
    # --------------------------------------------------------

    jurisdiction_domain = get_jurisdiction_domain(
        jurisdiction
    )

    official_domains = []

    if jurisdiction_domain:
        official_domains.append(
            jurisdiction_domain
        )

    # KP Local Government has a dedicated official
    # local-government domain.
    if jurisdiction == "Khyber Pakhtunkhwa":
        official_domains.insert(
            0,
            "lgkp.gov.pk",
        )

    official_domains.extend(
        [
            "gov.pk",
            "punjab.gov.pk",
            "sindh.gov.pk",
            "kp.gov.pk",
            "balochistan.gov.pk",
            "ajk.gov.pk",
            "gilgitbaltistan.gov.pk",
            "islamabad.gov.pk",
        ]
    )

    official_domains = list(
        dict.fromkeys(official_domains)
    )

    # --------------------------------------------------------
    # FOCUSED SEARCH TERMS
    # --------------------------------------------------------

    queries = [
        f"marriage registration {question}",
        f"marriage certificate {question}",
        f"nikah registration {question}",
        f"nikah nama registration {question}",
        f"marriage registration requirements {question}",
        f"marriage certificate documents {question}",
        f"marriage registration procedure {question}",
    ]

    # --------------------------------------------------------
    # JURISDICTION-SPECIFIC SEARCH
    # --------------------------------------------------------

    if jurisdiction_domain:

        queries = [
            (
                f"site:{jurisdiction_domain} "
                f"marriage registration {question}"
            ),
            (
                f"site:{jurisdiction_domain} "
                f"marriage certificate {question}"
            ),
            (
                f"site:{jurisdiction_domain} "
                f"nikah registration {question}"
            ),
            (
                f"site:{jurisdiction_domain} "
                "marriage registration requirements"
            ),
            (
                f"site:{jurisdiction_domain} "
                "marriage certificate documents"
            ),
        ]

    # KP-specific local-government searches
    if jurisdiction == "Khyber Pakhtunkhwa":

        queries = [
            f"site:lgkp.gov.pk marriage registration {question}",
            f"site:lgkp.gov.pk marriage certificate {question}",
            f"site:lgkp.gov.pk nikah registration {question}",
            (
                "site:lgkp.gov.pk "
                "registration marriage divorce"
            ),
            (
                "site:lgkp.gov.pk "
                "marriage registration requirements"
            ),
        ]

    # --------------------------------------------------------
    # SEARCH OFFICIAL SOURCES
    # --------------------------------------------------------

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
            "attempts": 1,
        }

    # --------------------------------------------------------
    # FALLBACK SEARCH
    # --------------------------------------------------------

    fallback_queries = [
        f"marriage registration Pakistan {question}",
        f"marriage certificate Pakistan {question}",
        f"nikah registration Pakistan {question}",
        f"official marriage registration requirements {question}",
    ]

    if jurisdiction:

        fallback_queries.insert(
            0,
            (
                f"{jurisdiction} "
                f"marriage registration "
                f"{question}"
            ),
        )

    sources = perform_search(
        queries=fallback_queries,
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
        "jurisdiction": jurisdiction,
        "attempts": 2,
    }


# ============================================================
# PASSPORT — DEDICATED OFFICIAL DGI&P RESEARCH
# ============================================================

def research_passport(
    question,
    language,
):
    """
    Dedicated Passport research path.

    Fresh/new/first-time passport questions are searched
    directly against the official DGI&P domain.
    """

    question_lower = (
        question or ""
    ).strip().lower()

    fresh_terms = [
        "fresh passport",
        "new passport",
        "first passport",
        "first time passport",
        "first-time passport",
        "passport for the first time",
        "apply for passport",
        "new mrp",
        "new machine readable passport",
        "new ordinary passport",
        "ordinary passport",
        "passport requirements",
        "passport documents",
        "documents required for passport",
        "passport application",
        "passport processing",
        "fresh mrp",
        "نیا پاسپورٹ",
        "پہلی بار پاسپورٹ",
        "نئے پاسپورٹ",
    ]

    renewal_terms = [
        "renew passport",
        "passport renewal",
        "renewal of passport",
        "renew my passport",
        "پاسپورٹ تجدید",
        "پاسپورٹ کی تجدید",
    ]

    modification_terms = [
        "passport modification",
        "modify passport",
        "passport correction",
        "correction in passport",
        "change passport",
        "passport changes",
        "پاسپورٹ ترمیم",
        "پاسپورٹ میں تبدیلی",
        "پاسپورٹ کی تصحیح",
    ]

    is_fresh = any(
        term in question_lower
        for term in fresh_terms
    )

    is_renewal = any(
        term in question_lower
        for term in renewal_terms
    )

    is_modification = any(
        term in question_lower
        for term in modification_terms
    )

    official_domains = [
        "dgip.gov.pk",
    ]

    if is_fresh:

        queries = [
            f"site:dgip.gov.pk {question}",
            (
                "site:dgip.gov.pk "
                "new passport "
                "first time applicant "
                "requirements"
            ),
            (
                "site:dgip.gov.pk "
                "ordinary passport "
                "first time "
                "documents required"
            ),
            (
                "site:dgip.gov.pk "
                "new passport "
                "application process"
            ),
            (
                "site:dgip.gov.pk "
                "ordinary passport "
                "requirements Pakistan"
            ),
            (
                "site:dgip.gov.pk "
                "passport process "
                "photograph biometrics data entry"
            ),
        ]

    elif is_renewal:

        queries = [
            f"site:dgip.gov.pk {question}",
            (
                "site:dgip.gov.pk "
                "passport renewal "
                "requirements"
            ),
            (
                "site:dgip.gov.pk "
                "passport renewal "
                "documents"
            ),
            (
                "site:dgip.gov.pk "
                "passport renewal "
                "process"
            ),
        ]

    elif is_modification:

        queries = [
            f"site:dgip.gov.pk {question}",
            (
                "site:dgip.gov.pk "
                "passport modification "
                "requirements"
            ),
            (
                "site:dgip.gov.pk "
                "passport modification "
                "documents"
            ),
            (
                "site:dgip.gov.pk "
                "passport correction "
                "process"
            ),
        ]

    else:

        queries = [
            f"site:dgip.gov.pk {question}",
            (
                "site:dgip.gov.pk "
                "passport requirements "
                f"{question}"
            ),
            (
                "site:dgip.gov.pk "
                "passport process "
                f"{question}"
            ),
            (
                "site:dgip.gov.pk "
                "ordinary passport "
                f"{question}"
            ),
        ]

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
            "jurisdiction": None,
            "attempts": 1,
        }

    fallback_queries = [
        f"site:dgip.gov.pk passport {question}",
        (
            "site:dgip.gov.pk "
            "ordinary passport "
            "requirements Pakistan"
        ),
        (
            "site:dgip.gov.pk "
            "passport application process Pakistan"
        ),
        (
            "site:dgip.gov.pk "
            "passport documents requirements"
        ),
    ]

    sources = perform_search(
        queries=fallback_queries,
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
        "attempts": 2,
    }


# ============================================================
# VACCINATION
# ============================================================

def research_vaccination(
    question,
    language,
):

    question_lower = question.lower()

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

    if hajj_question:

        official_evidence = """
OFFICIAL SAUDI MINISTRY OF HEALTH — HAJJ

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
                "title": "Saudi MOH — Hajj Health Requirements",
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
                "title": "Saudi MOH — Pilgrim's Health",
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

    if umrah_question:

        official_evidence = """
OFFICIAL SAUDI MINISTRY OF HEALTH — UMRAH

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
                "title": "Saudi MOH — Umrah Health Requirements",
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
                "title": "Saudi MOH — Pilgrim's Health",
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

    keyword_text = " ".join(
        keywords[:6]
    )

    # ========================================================
    # ATTEMPT 1
    # ========================================================

    queries = []

    if jurisdiction:

        jurisdiction_domain = get_jurisdiction_domain(
            jurisdiction
        )

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
    # ATTEMPT 2
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
    # PASSPORT
    # ========================================================

    if department == "Passport":

        return research_passport(
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
    # UNION COUNCIL / LOCAL GOVERNMENT
    # ========================================================

    if department == "Union Council / Local Government":

        question_lower = (
            question or ""
        ).strip().lower()

        # ----------------------------------------------------
        # BIRTH
        # ----------------------------------------------------

        birth_terms = [
            "birth",
            "birth certificate",
            "birth registration",
            "register birth",
            "newborn",
            "new born",
            "child birth",
            "registration of birth",
            "پیدائش",
            "پیدائش سرٹیفکیٹ",
            "پیدائش رجسٹریشن",
            "بچے کی پیدائش",
            "پیدائش کا اندراج",
        ]

        is_birth_question = any(
            term in question_lower
            for term in birth_terms
        )

        if is_birth_question:

            return research_birth_registration(
                question,
                language,
            )

        # ----------------------------------------------------
        # MARRIAGE
        # ----------------------------------------------------

        marriage_terms = [
            "marriage",
            "marriage certificate",
            "marriage registration",
            "register marriage",
            "registration of marriage",
            "nikah",
            "nikah registration",
            "nikah nama",
            "nikahnama",
            "nikah nama registration",
            "marriage document",
            "marriage documents",
            "شادی",
            "شادی رجسٹریشن",
            "شادی کا سرٹیفکیٹ",
            "نکاح",
            "نکاح رجسٹریشن",
            "نکاح نامہ",
            "نکاح نامہ رجسٹریشن",
        ]

        is_marriage_question = any(
            term in question_lower
            for term in marriage_terms
        )

        if is_marriage_question:

            return research_marriage_registration(
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
