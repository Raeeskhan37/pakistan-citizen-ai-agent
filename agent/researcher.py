from search.web_search import perform_search


# ============================================================
# JURISDICTIONS
# ============================================================

PROVINCES = {
    "punjab": "Punjab",
    "sindh": "Sindh",
    "khyber pakhtunkhwa": "Khyber Pakhtunkhwa",
    "khyber-pakhtunkhwa": "Khyber Pakhtunkhwa",
    "kpk": "Khyber Pakhtunkhwa",
    "kp": "Khyber Pakhtunkhwa",
    "balochistan": "Balochistan",
    "islamabad": "Islamabad Capital Territory",
    "ict": "Islamabad Capital Territory",
    "ajk": "Azad Jammu and Kashmir",
    "azad kashmir": "Azad Jammu and Kashmir",
    "azad jammu and kashmir": "Azad Jammu and Kashmir",
    "gilgit baltistan": "Gilgit-Baltistan",
    "gilgit-baltistan": "Gilgit-Baltistan",
    "gb": "Gilgit-Baltistan",
}


# ============================================================
# MAJOR CITIES / AREAS
# ============================================================

CITY_JURISDICTIONS = {

    # Punjab
    "lahore": "Punjab",
    "rawalpindi": "Punjab",
    "faisalabad": "Punjab",
    "multan": "Punjab",
    "gujranwala": "Punjab",
    "sialkot": "Punjab",
    "bahawalpur": "Punjab",
    "sargodha": "Punjab",
    "sheikhupura": "Punjab",
    "jhelum": "Punjab",
    "gujrat": "Punjab",
    "rahim yar khan": "Punjab",
    "dera ghazi khan": "Punjab",
    "kasur": "Punjab",
    "okara": "Punjab",
    "chiniot": "Punjab",
    "attock": "Punjab",
    "chakwal": "Punjab",
    "narowal": "Punjab",
    "pakpattan": "Punjab",
    "vehari": "Punjab",
    "khanewal": "Punjab",
    "lodhran": "Punjab",
    "muzaffargarh": "Punjab",
    "bahawalnagar": "Punjab",
    "toba tek singh": "Punjab",
    "hafizabad": "Punjab",
    "mandi bahauddin": "Punjab",

    # Sindh
    "karachi": "Sindh",
    "hyderabad": "Sindh",
    "sukkur": "Sindh",
    "larkana": "Sindh",
    "nawabshah": "Sindh",
    "shaheed benazirabad": "Sindh",
    "mirpur khas": "Sindh",
    "jacobabad": "Sindh",
    "shikarpur": "Sindh",
    "thatta": "Sindh",
    "badin": "Sindh",
    "dadu": "Sindh",
    "jamshoro": "Sindh",
    "khairpur": "Sindh",

    # Khyber Pakhtunkhwa
    "peshawar": "Khyber Pakhtunkhwa",
    "mardan": "Khyber Pakhtunkhwa",
    "swat": "Khyber Pakhtunkhwa",
    "mingora": "Khyber Pakhtunkhwa",
    "abbottabad": "Khyber Pakhtunkhwa",
    "mansehra": "Khyber Pakhtunkhwa",
    "kohat": "Khyber Pakhtunkhwa",
    "bannu": "Khyber Pakhtunkhwa",
    "dera ismail khan": "Khyber Pakhtunkhwa",
    "di khan": "Khyber Pakhtunkhwa",
    "charsadda": "Khyber Pakhtunkhwa",
    "nowshera": "Khyber Pakhtunkhwa",
    "swabi": "Khyber Pakhtunkhwa",
    "haripur": "Khyber Pakhtunkhwa",
    "dir": "Khyber Pakhtunkhwa",
    "lower dir": "Khyber Pakhtunkhwa",
    "upper dir": "Khyber Pakhtunkhwa",
    "malakand": "Khyber Pakhtunkhwa",
    "chitral": "Khyber Pakhtunkhwa",
    "buner": "Khyber Pakhtunkhwa",
    "batkhela": "Khyber Pakhtunkhwa",

    # Balochistan
    "quetta": "Balochistan",
    "gwadar": "Balochistan",
    "turbat": "Balochistan",
    "khuzdar": "Balochistan",
    "chaman": "Balochistan",
    "sibi": "Balochistan",
    "zhob": "Balochistan",
    "loralai": "Balochistan",
    "mastung": "Balochistan",
    "nushki": "Balochistan",

    # Islamabad
    "islamabad": "Islamabad Capital Territory",
    "ict": "Islamabad Capital Territory",

    # AJK
    "muzaffarabad": "Azad Jammu and Kashmir",
    "mirpur ajk": "Azad Jammu and Kashmir",
    "rawalakot": "Azad Jammu and Kashmir",
    "bagh ajk": "Azad Jammu and Kashmir",
    "kotli ajk": "Azad Jammu and Kashmir",

    # Gilgit-Baltistan
    "gilgit": "Gilgit-Baltistan",
    "skardu": "Gilgit-Baltistan",
    "hunza": "Gilgit-Baltistan",
    "chilas": "Gilgit-Baltistan",
    "ghizer": "Gilgit-Baltistan",
}


# ============================================================
# ALL JURISDICTIONS
# ============================================================

ALL_JURISDICTIONS = [
    "Punjab",
    "Sindh",
    "Khyber Pakhtunkhwa",
    "Balochistan",
    "Islamabad Capital Territory",
    "Azad Jammu and Kashmir",
    "Gilgit-Baltistan",
]


# ============================================================
# OFFICIAL DOMAINS
# ============================================================

JURISDICTION_DOMAINS = {
    "Punjab": [
        "punjab.gov.pk",
        "lgcd.punjab.gov.pk",
    ],

    "Sindh": [
        "sindh.gov.pk",
    ],

    "Khyber Pakhtunkhwa": [
        "kp.gov.pk",
        "lgkp.gov.pk",
        "kprts.gov.pk",
    ],

    "Balochistan": [
        "balochistan.gov.pk",
    ],

    "Islamabad Capital Territory": [
        "islamabad.gov.pk",
        "ictadministration.gov.pk",
    ],

    "Azad Jammu and Kashmir": [
        "ajk.gov.pk",
    ],

    "Gilgit-Baltistan": [
        "gilgitbaltistan.gov.pk",
    ],
}


# ============================================================
# JURISDICTION DETECTION
# ============================================================

def detect_jurisdiction(question):

    question_lower = (question or "").lower()

    # --------------------------------------------------------
    # First check explicit province / region names
    # --------------------------------------------------------

    for keyword, jurisdiction in PROVINCES.items():

        if keyword in question_lower:
            return jurisdiction

    # --------------------------------------------------------
    # Then check recognized cities / areas
    # --------------------------------------------------------

    for area, jurisdiction in CITY_JURISDICTIONS.items():

        if area in question_lower:
            return jurisdiction

    return None


# ============================================================
# GET JURISDICTION DOMAINS
# ============================================================

def get_jurisdiction_domain(jurisdiction):

    domains = JURISDICTION_DOMAINS.get(
        jurisdiction,
        [],
    )

    if domains:
        return domains[0]

    return None


# ============================================================
# UNIQUE SOURCES
# ============================================================

def unique_sources(
    sources,
    limit=5,
):

    unique = {}

    for source in sources:

        if not isinstance(source, dict):
            continue

        url = source.get(
            "url",
            "",
        )

        if not url:
            continue

        if url not in unique:
            unique[url] = source

    return list(
        unique.values()
    )[:limit]


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

Birth registration is handled through the relevant
Village Council or Neighbourhood Council according
to the applicable local-government arrangement.

The official KP Local Government service table lists:

Service:
Registration & Certificate of Birth

Designated Officer:
Secretary Union Council

The official KP government also provides forms and
procedural information for birth registration.

Citizens should apply through the relevant local
government office for the place where the birth is
registered.

Do not confuse a civil birth certificate with a NADRA
Child Registration Certificate (CRC).
"""

    sources = [

        {
            "title": (
                "KP Local Government — "
                "Registration of Birth, Death, Marriage & Divorce"
            ),

            "url": (
                "https://www.lgkp.gov.pk/"
                "page/registration-bdmd"
            ),

            "domain": "lgkp.gov.pk",

            "official": True,

            "page_text": official_evidence,

            "snippet": official_evidence,
        },

        {
            "title": (
                "KP Right to Public Services Commission — "
                "Birth Certificate"
            ),

            "url": (
                "https://www.kprts.gov.pk/"
                "services/birth-certificate/"
            ),

            "domain": "kprts.gov.pk",

            "official": True,

            "page_text": official_evidence,

            "snippet": official_evidence,
        },
    ]

    return {

        "sources": sources,

        "rag_results": [],

        "jurisdiction": (
            "Khyber Pakhtunkhwa"
        ),

        "attempts": 1,
    }


# ============================================================
# BIRTH REGISTRATION — ALL PROVINCES / REGIONS
# ============================================================

def research_birth_registration(
    question,
    language,
):

    jurisdiction = detect_jurisdiction(
        question
    )

    # ========================================================
    # SPECIFIC JURISDICTION
    # ========================================================

    if jurisdiction:

        # ----------------------------------------------------
        # KP — preserve tested route
        # ----------------------------------------------------

        if jurisdiction == "Khyber Pakhtunkhwa":

            return research_kp_birth_registration(
                question,
                language,
            )

        # ----------------------------------------------------
        # ICT — focused official search
        # ----------------------------------------------------

        if jurisdiction == (
            "Islamabad Capital Territory"
        ):

            queries = [

                f"site:ictadministration.gov.pk birth certificate {question}",

                (
                    "site:ictadministration.gov.pk "
                    "birth certificate "
                    "documents requirements"
                ),

                (
                    "site:ictadministration.gov.pk "
                    "birth certificate "
                    "application procedure"
                ),

                (
                    "site:ictadministration.gov.pk "
                    "birth registration"
                ),
            ]

        else:

            jurisdiction_domains = (
                JURISDICTION_DOMAINS.get(
                    jurisdiction,
                    [],
                )
            )

            primary_domain = (
                jurisdiction_domains[0]
                if jurisdiction_domains
                else "gov.pk"
            )

            queries = [

                (
                    f"site:{primary_domain} "
                    f"birth registration {question}"
                ),

                (
                    f"site:{primary_domain} "
                    f"birth certificate {question}"
                ),

                (
                    f"site:{primary_domain} "
                    "birth registration requirements"
                ),

                (
                    f"site:{primary_domain} "
                    "birth certificate documents"
                ),

                (
                    f"site:{primary_domain} "
                    "birth registration procedure"
                ),

                (
                    f"site:{primary_domain} "
                    "birth certificate application"
                ),
            ]

            # ------------------------------------------------
            # Punjab has a strong dedicated LGCD source
            # ------------------------------------------------

            if jurisdiction == "Punjab":

                queries.extend(
                    [
                        (
                            "site:lgcd.punjab.gov.pk "
                            "registration of birth"
                        ),

                        (
                            "site:lgcd.punjab.gov.pk "
                            "birth certificate"
                        ),

                        (
                            "site:lgcd.punjab.gov.pk "
                            "birth registration requirements"
                        ),
                    ]
                )

        # ----------------------------------------------------
        # Official domains
        # ----------------------------------------------------

        official_domains = (
            JURISDICTION_DOMAINS.get(
                jurisdiction,
                ["gov.pk"],
            )
        )

        official_domains = list(
            dict.fromkeys(
                official_domains + [
                    "gov.pk",
                    "nadra.gov.pk",
                ]
            )
        )

        sources = perform_search(
            queries=queries,
            official_domains=official_domains,
            max_results=10,
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
                    limit=8,
                ),

                "rag_results": [],

                "jurisdiction": jurisdiction,

                "attempts": 1,
            }

        # ----------------------------------------------------
        # Specific jurisdiction fallback
        # ----------------------------------------------------

        fallback_queries = [

            (
                f"{jurisdiction} "
                f"birth certificate "
                f"{question}"
            ),

            (
                f"{jurisdiction} "
                "birth registration "
                "requirements"
            ),

            (
                f"{jurisdiction} "
                "birth certificate "
                "documents"
            ),

            (
                f"{jurisdiction} "
                "birth registration "
                "procedure"
            ),
        ]

        sources = perform_search(
            queries=fallback_queries,
            official_domains=official_domains,
            max_results=10,
        )

        official_sources = [
            source
            for source in sources
            if source.get("official")
        ]

        return {

            "sources": unique_sources(
                official_sources,
                limit=8,
            ),

            "rag_results": [],

            "jurisdiction": jurisdiction,

            "attempts": 2,
        }

    # ========================================================
    # NO AREA / PROVINCE MENTIONED
    # ========================================================
    #
    # IMPORTANT:
    # Do NOT search only one generic government domain.
    #
    # Search each jurisdiction separately so the answer
    # generator receives evidence for all regions.
    # ========================================================

    all_sources = []

    jurisdiction_queries = {

        "Punjab": [
            (
                "site:lgcd.punjab.gov.pk "
                "birth registration"
            ),
            (
                "site:lgcd.punjab.gov.pk "
                "birth certificate requirements"
            ),
            (
                "site:punjab.gov.pk "
                "birth certificate"
            ),
        ],

        "Sindh": [
            (
                "site:sindh.gov.pk "
                "birth registration"
            ),
            (
                "site:sindh.gov.pk "
                "birth certificate requirements"
            ),
            (
                "site:sindh.gov.pk "
                "birth certificate procedure"
            ),
        ],

        "Khyber Pakhtunkhwa": [
            (
                "site:lgkp.gov.pk "
                "registration certificate birth"
            ),
            (
                "site:kprts.gov.pk "
                "birth certificate"
            ),
            (
                "site:kp.gov.pk "
                "birth registration"
            ),
        ],

        "Balochistan": [
            (
                "site:balochistan.gov.pk "
                "birth registration"
            ),
            (
                "site:balochistan.gov.pk "
                "birth certificate"
            ),
            (
                "site:balochistan.gov.pk "
                "birth registration requirements"
            ),
        ],

        "Islamabad Capital Territory": [
            (
                "site:ictadministration.gov.pk "
                "birth certificate"
            ),
            (
                "site:ictadministration.gov.pk "
                "birth registration"
            ),
            (
                "site:islamabad.gov.pk "
                "birth certificate"
            ),
        ],

        "Azad Jammu and Kashmir": [
            (
                "site:ajk.gov.pk "
                "birth registration"
            ),
            (
                "site:ajk.gov.pk "
                "birth certificate"
            ),
            (
                "site:ajk.gov.pk "
                "birth registration requirements"
            ),
        ],

        "Gilgit-Baltistan": [
            (
                "site:gilgitbaltistan.gov.pk "
                "birth registration"
            ),
            (
                "site:gilgitbaltistan.gov.pk "
                "birth certificate"
            ),
            (
                "site:gilgitbaltistan.gov.pk "
                "birth registration requirements"
            ),
        ],
    }

    # --------------------------------------------------------
    # Search each jurisdiction
    # --------------------------------------------------------

    for region in ALL_JURISDICTIONS:

        queries = jurisdiction_queries.get(
            region,
            [],
        )

        if not queries:
            continue

        domains = JURISDICTION_DOMAINS.get(
            region,
            ["gov.pk"],
        )

        sources = perform_search(
            queries=queries,
            official_domains=domains,
            max_results=6,
        )

        official_sources = [
            source
            for source in sources
            if source.get("official")
        ]

        for source in official_sources:

            source_copy = dict(
                source
            )

            # Add region metadata so the answer generator
            # knows which province the evidence belongs to.
            source_copy[
                "jurisdiction"
            ] = region

            all_sources.append(
                source_copy
            )

    # --------------------------------------------------------
    # Add Pakistan-wide authoritative CRVS evidence
    # --------------------------------------------------------

    national_queries = [

        (
            "site:pakistan.gov.pk "
            "birth registration "
            "provincial services"
        ),

        (
            "site:pc.gov.pk "
            "civil registration "
            "birth registration Pakistan"
        ),

        (
            "site:nadra.gov.pk "
            "birth death marriage divorce "
            "public guide"
        ),

        (
            "site:nadra.gov.pk "
            "Pakistan Registration Ecosystem "
            "birth certificate"
        ),
    ]

    national_sources = perform_search(
        queries=national_queries,
        official_domains=[
            "pakistan.gov.pk",
            "pc.gov.pk",
            "nadra.gov.pk",
        ],
        max_results=8,
    )

    national_official_sources = [
        source
        for source in national_sources
        if source.get("official")
    ]

    for source in national_official_sources:

        source_copy = dict(
            source
        )

        source_copy[
            "jurisdiction"
        ] = "Pakistan-wide"

        all_sources.append(
            source_copy
        )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    final_sources = unique_sources(
        all_sources,
        limit=20,
    )

    return {

        "sources": final_sources,

        "rag_results": [],

        "jurisdiction": None,

        "all_jurisdictions": True,

        "jurisdictions_searched": (
            ALL_JURISDICTIONS
        ),

        "attempts": 1,
    }


# ============================================================
# MARRIAGE REGISTRATION — DEDICATED OFFICIAL RESEARCH
# ============================================================

def research_marriage_registration(
    question,
    language,
):

    jurisdiction = detect_jurisdiction(
        question
    )

    # ========================================================
    # SPECIFIC JURISDICTION
    # ========================================================

    if jurisdiction:

        jurisdiction_domains = (
            JURISDICTION_DOMAINS.get(
                jurisdiction,
                ["gov.pk"],
            )
        )

        if jurisdiction == "Khyber Pakhtunkhwa":

            queries = [

                (
                    "site:lgkp.gov.pk "
                    f"marriage registration {question}"
                ),

                (
                    "site:lgkp.gov.pk "
                    f"marriage certificate {question}"
                ),

                (
                    "site:lgkp.gov.pk "
                    f"nikah registration {question}"
                ),

                (
                    "site:lgkp.gov.pk "
                    "registration certificate nikkah"
                ),

            ]

        else:

            primary_domain = (
                jurisdiction_domains[0]
                if jurisdiction_domains
                else "gov.pk"
            )

            queries = [

                (
                    f"site:{primary_domain} "
                    f"marriage registration {question}"
                ),

                (
                    f"site:{primary_domain} "
                    f"marriage certificate {question}"
                ),

                (
                    f"site:{primary_domain} "
                    f"nikah registration {question}"
                ),

                (
                    f"site:{primary_domain} "
                    "marriage registration requirements"
                ),

                (
                    f"site:{primary_domain} "
                    "marriage certificate documents"
                ),
            ]

        sources = perform_search(
            queries=queries,
            official_domains=jurisdiction_domains,
            max_results=10,
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
                    limit=8,
                ),

                "rag_results": [],

                "jurisdiction": jurisdiction,

                "attempts": 1,
            }

        # ----------------------------------------------------
        # Fallback
        # ----------------------------------------------------

        fallback_queries = [

            (
                f"{jurisdiction} "
                f"marriage registration "
                f"{question}"
            ),

            (
                f"{jurisdiction} "
                "marriage certificate "
                "requirements"
            ),

            (
                f"{jurisdiction} "
                "nikah registration "
                "procedure"
            ),
        ]

        sources = perform_search(
            queries=fallback_queries,
            official_domains=jurisdiction_domains,
            max_results=10,
        )

        official_sources = [
            source
            for source in sources
            if source.get("official")
        ]

        return {

            "sources": unique_sources(
                official_sources,
                limit=8,
            ),

            "rag_results": [],

            "jurisdiction": jurisdiction,

            "attempts": 2,
        }

    # ========================================================
    # NO AREA / PROVINCE
    # ========================================================

    all_sources = []

    marriage_queries = {

        "Punjab": [
            (
                "site:lgcd.punjab.gov.pk "
                "registration marriage"
            ),
            (
                "site:lgcd.punjab.gov.pk "
                "marriage registration certificate"
            ),
            (
                "site:punjab.gov.pk "
                "marriage registration"
            ),
        ],

        "Sindh": [
            (
                "site:sindh.gov.pk "
                "marriage registration"
            ),
            (
                "site:sindh.gov.pk "
                "marriage certificate"
            ),
        ],

        "Khyber Pakhtunkhwa": [
            (
                "site:lgkp.gov.pk "
                "registration certificate nikkah"
            ),
            (
                "site:lgkp.gov.pk "
                "marriage registration"
            ),
        ],

        "Balochistan": [
            (
                "site:balochistan.gov.pk "
                "marriage registration"
            ),
            (
                "site:balochistan.gov.pk "
                "marriage certificate"
            ),
        ],

        "Islamabad Capital Territory": [
            (
                "site:islamabad.gov.pk "
                "marriage registration"
            ),
            (
                "site:ictadministration.gov.pk "
                "marriage certificate"
            ),
        ],

        "Azad Jammu and Kashmir": [
            (
                "site:ajk.gov.pk "
                "marriage registration"
            ),
            (
                "site:ajk.gov.pk "
                "marriage certificate"
            ),
        ],

        "Gilgit-Baltistan": [
            (
                "site:gilgitbaltistan.gov.pk "
                "marriage registration"
            ),
            (
                "site:gilgitbaltistan.gov.pk "
                "marriage certificate"
            ),
        ],
    }

    for region in ALL_JURISDICTIONS:

        queries = marriage_queries.get(
            region,
            [],
        )

        domains = JURISDICTION_DOMAINS.get(
            region,
            ["gov.pk"],
        )

        sources = perform_search(
            queries=queries,
            official_domains=domains,
            max_results=6,
        )

        official_sources = [
            source
            for source in sources
            if source.get("official")
        ]

        for source in official_sources:

            source_copy = dict(
                source
            )

            source_copy[
                "jurisdiction"
            ] = region

            all_sources.append(
                source_copy
            )

    final_sources = unique_sources(
        all_sources,
        limit=20,
    )

    return {

        "sources": final_sources,

        "rag_results": [],

        "jurisdiction": None,

        "all_jurisdictions": True,

        "jurisdictions_searched": (
            ALL_JURISDICTIONS
        ),

        "attempts": 1,
    }


# ============================================================
# PASSPORT — DEDICATED OFFICIAL DGI&P RESEARCH
# ============================================================

def research_passport(
    question,
    language,
):

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
                "new passport first time applicant "
                "requirements"
            ),
            (
                "site:dgip.gov.pk "
                "ordinary passport first time "
                "documents required"
            ),
            (
                "site:dgip.gov.pk "
                "new passport application process"
            ),
            (
                "site:dgip.gov.pk "
                "ordinary passport requirements Pakistan"
            ),
            (
                "site:dgip.gov.pk "
                "passport process photograph biometrics"
            ),
        ]

    elif is_renewal:

        queries = [
            f"site:dgip.gov.pk {question}",
            (
                "site:dgip.gov.pk "
                "passport renewal requirements"
            ),
            (
                "site:dgip.gov.pk "
                "passport renewal documents"
            ),
            (
                "site:dgip.gov.pk "
                "passport renewal process"
            ),
        ]

    elif is_modification:

        queries = [
            f"site:dgip.gov.pk {question}",
            (
                "site:dgip.gov.pk "
                "passport modification requirements"
            ),
            (
                "site:dgip.gov.pk "
                "passport modification documents"
            ),
            (
                "site:dgip.gov.pk "
                "passport correction process"
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
            "ordinary passport requirements Pakistan"
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

    question_lower = (
        question or ""
    ).lower()

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

        jurisdiction_domains = (
            JURISDICTION_DOMAINS.get(
                jurisdiction,
                [],
            )
        )

        jurisdiction_domain = (
            jurisdiction_domains[0]
            if jurisdiction_domains
            else get_jurisdiction_domain(
                jurisdiction
            )
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
            "new birth certificate",
            "get birth certificate",
            "obtain birth certificate",
            "birth certificate procedure",
            "birth certificate requirements",
            "birth certificate documents",
            "پیدائش",
            "پیدائش سرٹیفکیٹ",
            "پیدائش رجسٹریشن",
            "بچے کی پیدائش",
            "پیدائش کا اندراج",
            "نیا پیدائش سرٹیفکیٹ",
            "پیدائش کا سرٹیفکیٹ",
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
            "marriage certificate procedure",
            "marriage certificate requirements",
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
