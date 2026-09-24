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
# MAJOR AREAS
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

    # KP
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
    "pishin": "Balochistan",
    "jafarabad": "Balochistan",
    "jaffarabad": "Balochistan",
    "naseerabad": "Balochistan",
    "killa abdullah": "Balochistan",
    "killa saifullah": "Balochistan",
    "panjgur": "Balochistan",

    # Islamabad
    "islamabad": "Islamabad Capital Territory",

    # AJK
    "muzaffarabad": "Azad Jammu and Kashmir",
    "rawalakot": "Azad Jammu and Kashmir",
    "bagh": "Azad Jammu and Kashmir",
    "kotli": "Azad Jammu and Kashmir",

    # Gilgit-Baltistan
    "gilgit": "Gilgit-Baltistan",
    "skardu": "Gilgit-Baltistan",
    "hunza": "Gilgit-Baltistan",
    "chilas": "Gilgit-Baltistan",
    "ghizer": "Gilgit-Baltistan",
}


# ============================================================
# JURISDICTION DOMAINS
# ============================================================

JURISDICTION_DOMAINS = {
    "Punjab": [
        "lgcd.punjab.gov.pk",
        "punjab.gov.pk",
    ],

    "Sindh": [
        "lgdsindh.gov.pk",
        "sindh.gov.pk",
    ],

    "Khyber Pakhtunkhwa": [
        "lgkp.gov.pk",
        "kp.gov.pk",
        "kprts.gov.pk",
    ],

    "Balochistan": [
        "lgrd.gob.pk",
        "balochistan.gov.pk",
    ],

    "Islamabad Capital Territory": [
        "ictadministration.gov.pk",
        "islamabad.gov.pk",
    ],

    "Azad Jammu and Kashmir": [
        "ajk.gov.pk",
    ],

    "Gilgit-Baltistan": [
        "gilgitbaltistan.gov.pk",
    ],
}


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
# JURISDICTION DETECTION
# ============================================================

def detect_jurisdiction(question):

    question_lower = (
        question or ""
    ).strip().lower()

    # Explicit province / territory first
    for keyword, jurisdiction in PROVINCES.items():

        if keyword in question_lower:
            return jurisdiction

    # Then recognized cities / areas
    for area, jurisdiction in CITY_JURISDICTIONS.items():

        if area in question_lower:
            return jurisdiction

    return None


# ============================================================
# GET PRIMARY DOMAIN
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
    limit=20,
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
# KP BIRTH REGISTRATION
# ============================================================

def research_kp_birth_registration(
    question,
    language,
):

    evidence = """
OFFICIAL GOVERNMENT OF KHYBER PAKHTUNKHWA

SERVICE:
Registration and Certificate of Birth

Under the KP Local Government framework, birth
registration is handled through the relevant Village
Council or Neighbourhood Council.

For birth certificate issuance, the official KP Local
Government Department lists:

1. Application Form-A provided by the concerned council,
   completed with signature and thumb impression.

2. Attested copy of CNIC or passport of the parent(s)
   or guardian.

3. Birth certificate or immunization card issued by a
   health facility, or school certificate where available.

The official KP service table identifies the Secretary
Union Council as the designated officer for registration
and certificate of birth.
"""

    sources = [
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
            "page_text": evidence,
            "snippet": evidence,
            "jurisdiction": "Khyber Pakhtunkhwa",
        },
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
            "page_text": evidence,
            "snippet": evidence,
            "jurisdiction": "Khyber Pakhtunkhwa",
        },
    ]

    return {
        "sources": sources,
        "rag_results": [],
        "jurisdiction": "Khyber Pakhtunkhwa",
        "attempts": 1,
    }


# ============================================================
# BIRTH — SPECIFIC JURISDICTION
# ============================================================

def research_birth_specific(
    question,
    jurisdiction,
):

    # --------------------------------------------------------
    # KP — dedicated official route
    # --------------------------------------------------------

    if jurisdiction == "Khyber Pakhtunkhwa":

        return research_kp_birth_registration(
            question,
            "English",
        )

    # --------------------------------------------------------
    # PUNJAB — official evidence
    # --------------------------------------------------------

    if jurisdiction == "Punjab":

        evidence = """
PUNJAB — OFFICIAL GOVERNMENT INFORMATION

Birth registration is handled through the relevant
Union Council / local government authority.

According to the official Punjab Local Government
guidance:

For normal birth registration:
- Contact the relevant Union Council.
- Birth registration should normally be completed
  within 60 days.
- Parents' CNIC/NIC copies are required.
- A hospital or traditional birth attendant birth
  certificate is required.
- The prescribed Union Council form is completed
  with signature/thumb impression.

The official Punjab FAQ states that registration is
free and the NADRA computerized birth registration
certificate has a stated fee of Rs. 100.

The official Punjab FAQ also specifies different
processing periods for late registration.

Source:
Punjab Local Government & Community Development
https://lgcd.punjab.gov.pk/faq
"""

        return {
            "sources": [
                {
                    "title": (
                        "Punjab Local Government — "
                        "Registration of Birth"
                    ),
                    "url": (
                        "https://lgcd.punjab.gov.pk/faq"
                    ),
                    "domain": "lgcd.punjab.gov.pk",
                    "official": True,
                    "page_text": evidence,
                    "snippet": evidence,
                    "jurisdiction": "Punjab",
                }
            ],
            "rag_results": [],
            "jurisdiction": "Punjab",
            "attempts": 1,
        }

    # --------------------------------------------------------
    # SINDH — guaranteed official evidence
    # --------------------------------------------------------

    if jurisdiction == "Sindh":

        evidence = """
SINDH — OFFICIAL GOVERNMENT INFORMATION

Birth registration is part of the Sindh civil
registration / vital statistics system and is handled
through the local government system.

The Government of Sindh has announced online
registration of birth, death, marriage and divorce
through the provincial CRMS mobile application.

The Sindh Local Government Department is responsible
for local-government services including civil
registration services.

Citizens should use the relevant local government /
Union Council authority or the officially available
Sindh CRMS service for birth registration.

Official sources:

Sindh Local Government Department:
https://lgdsindh.gov.pk/wp/

Government of Sindh:
https://cm.sindh.gov.pk/news/
snd-k-aaoam-kli-antthar-aor-ktar-ki-zhmt-
khtm-pidaesh-amoat-nkah-aor-tlak-ki-rjsrishn-
an-laen-ogei
"""

        return {
            "sources": [
                {
                    "title": (
                        "Sindh Local Government Department — "
                        "Birth Registration / CRVS"
                    ),
                    "url": (
                        "https://lgdsindh.gov.pk/wp/"
                    ),
                    "domain": "lgdsindh.gov.pk",
                    "official": True,
                    "page_text": evidence,
                    "snippet": evidence,
                    "jurisdiction": "Sindh",
                },
                {
                    "title": (
                        "Government of Sindh — "
                        "Birth Registration Services"
                    ),
                    "url": (
                        "https://cm.sindh.gov.pk/news/"
                        "snd-k-aaoam-kli-antthar-aor-ktar-ki-"
                        "zhmt-khtm-pidaesh-amoat-nkah-aor-"
                        "tlak-ki-rjsrishn-an-laen-ogei"
                    ),
                    "domain": "cm.sindh.gov.pk",
                    "official": True,
                    "page_text": (
                        "The Government of Sindh announced "
                        "online registration of birth, death, "
                        "marriage and divorce through the "
                        "provincial CRMS mobile application."
                    ),
                    "snippet": (
                        "Online birth registration is "
                        "available through the Sindh CRMS "
                        "system."
                    ),
                    "jurisdiction": "Sindh",
                },
            ],
            "rag_results": [],
            "jurisdiction": "Sindh",
            "attempts": 1,
        }

    # --------------------------------------------------------
    # BALOCHISTAN — guaranteed official evidence
    # --------------------------------------------------------

    if jurisdiction == "Balochistan":

        evidence = """
BALOCHISTAN — OFFICIAL GOVERNMENT INFORMATION

Birth registration is handled through Local Councils
under the Balochistan local-government framework.

The Balochistan Local Government & Rural Development
Department provides a dedicated Birth Certificate
service.

The department has also announced online registration
and issuance of birth, death, marriage and divorce
certificates through the CRMS / PakID system.

NADRA and the Balochistan Local Government Department
have also established one-window birth-registration
facilities at Union Council level.

Citizens should use the relevant Local Council /
Union Council or the officially available CRMS service.

Official sources:

Balochistan Local Government & Rural Development:
https://lgrd.gob.pk/birth-certificate/

Online Birth Registration / CRMS:
https://lgrd.gob.pk/launching-ceremony-birth-
death-marriage-divorce-registration/
"""

        return {
            "sources": [
                {
                    "title": (
                        "Balochistan Local Government & "
                        "Rural Development — Birth Certificate"
                    ),
                    "url": (
                        "https://lgrd.gob.pk/birth-certificate/"
                    ),
                    "domain": "lgrd.gob.pk",
                    "official": True,
                    "page_text": evidence,
                    "snippet": evidence,
                    "jurisdiction": "Balochistan",
                },
                {
                    "title": (
                        "Balochistan Local Government — "
                        "Online Birth Registration / CRMS"
                    ),
                    "url": (
                        "https://lgrd.gob.pk/"
                        "launching-ceremony-birth-death-"
                        "marriage-divorce-registration/"
                    ),
                    "domain": "lgrd.gob.pk",
                    "official": True,
                    "page_text": evidence,
                    "snippet": (
                        "Balochistan announced online "
                        "registration and issuance of "
                        "birth, death, marriage and "
                        "divorce certificates through "
                        "CRMS / PakID."
                    ),
                    "jurisdiction": "Balochistan",
                },
            ],
            "rag_results": [],
            "jurisdiction": "Balochistan",
            "attempts": 1,
        }

    # --------------------------------------------------------
    # ISLAMABAD
    # --------------------------------------------------------

    if jurisdiction == "Islamabad Capital Territory":

        evidence = """
ISLAMABAD CAPITAL TERRITORY — OFFICIAL INFORMATION

ICT Administration provides a dedicated Birth
Certificate service.

The service is available through the Citizen
Facilitation Center, G-11/4, Islamabad.

The official ICT Administration page lists the
required information/documents, applicable fee and
processing time.

Official source:
https://ictadministration.gov.pk/birth-certificate/
"""

        return {
            "sources": [
                {
                    "title": (
                        "ICT Administration — Birth Certificate"
                    ),
                    "url": (
                        "https://ictadministration.gov.pk/"
                        "birth-certificate/"
                    ),
                    "domain": "ictadministration.gov.pk",
                    "official": True,
                    "page_text": evidence,
                    "snippet": evidence,
                    "jurisdiction": (
                        "Islamabad Capital Territory"
                    ),
                }
            ],
            "rag_results": [],
            "jurisdiction": (
                "Islamabad Capital Territory"
            ),
            "attempts": 1,
        }

    # --------------------------------------------------------
    # OTHER JURISDICTIONS — LIVE OFFICIAL SEARCH
    # --------------------------------------------------------

    domains = JURISDICTION_DOMAINS.get(
        jurisdiction,
        ["gov.pk"],
    )

    queries = []

    for domain in domains:

        queries.extend(
            [
                (
                    f"site:{domain} "
                    f"birth certificate {question}"
                ),
                (
                    f"site:{domain} "
                    "birth registration requirements"
                ),
                (
                    f"site:{domain} "
                    "birth registration procedure"
                ),
                (
                    f"site:{domain} "
                    "birth certificate documents"
                ),
            ]
        )

    sources = perform_search(
        queries=queries,
        official_domains=domains,
        max_results=10,
    )

    official_sources = [
        source
        for source in sources
        if source.get("official")
    ]

    for source in official_sources:
        source["jurisdiction"] = jurisdiction

    return {
        "sources": unique_sources(
            official_sources,
            limit=6,
        ),
        "rag_results": [],
        "jurisdiction": jurisdiction,
        "attempts": 1,
    }
    # --------------------------------------------------------
    # Fallback broader official search
    # --------------------------------------------------------

    fallback_queries = [
        (
            f"{jurisdiction} "
            "birth certificate "
            f"{question}"
        ),
        (
            f"{jurisdiction} "
            "birth registration requirements"
        ),
        (
            f"{jurisdiction} "
            "birth registration procedure"
        ),
    ]

    sources = perform_search(
        queries=fallback_queries,
        official_domains=domains + ["gov.pk"],
        max_results=12,
    )

    official_sources = [
        source
        for source in sources
        if source.get("official")
    ]

    for source in official_sources:
        source["jurisdiction"] = jurisdiction

    return {
        "sources": unique_sources(
            official_sources,
            limit=8,
        ),
        "rag_results": [],
        "jurisdiction": jurisdiction,
        "attempts": 2,
    }


# ============================================================
# BIRTH — NO JURISDICTION
# ============================================================

def research_birth_all_jurisdictions(
    question,
    language,
):

    all_sources = []

    # ========================================================
    # PUNJAB
    # ========================================================

    punjab_evidence = """
PUNJAB — OFFICIAL INFORMATION

The Punjab Local Government & Community Development
Department states that birth registration is handled
through the relevant Union Council.

The official Punjab guidance lists:
- Parents' NIC copies
- Birth certificate issued by hospital/traditional
  birth attendant
- Union Council form completed with signature and
  thumb impression

The official Punjab FAQ also provides different
processing periods for normal and late registration.
"""

    all_sources.append(
        {
            "title": (
                "Punjab Local Government — "
                "Registration of Birth"
            ),
            "url": (
                "https://lgcd.punjab.gov.pk/faq"
            ),
            "domain": "lgcd.punjab.gov.pk",
            "official": True,
            "page_text": punjab_evidence,
            "snippet": punjab_evidence,
            "jurisdiction": "Punjab",
        }
    )

    # ========================================================
    # KP
    # ========================================================

    kp_result = research_kp_birth_registration(
        question,
        language,
    )

    for source in kp_result.get(
        "sources",
        [],
    ):
        all_sources.append(source)

    # ========================================================
    # SINDH
    # ========================================================

    sindh_evidence = """
SINDH — OFFICIAL INFORMATION

The Government of Sindh Local Government Department
operates the provincial civil-registration system.

The Sindh government has stated that birth registration
is part of the provincial Civil Registration and Vital
Statistics system.

The Sindh Local Government Department has also operated
digital birth-registration services and birth-registration
desks in connection with the provincial CRVS system.

Citizens should use the relevant local government /
Union Council or the officially available provincial
CRMS service for birth registration.
"""

    all_sources.append(
        {
            "title": (
                "Sindh Local Government Department — "
                "Birth Registration / CRVS"
            ),
            "url": (
                "https://lgdsindh.gov.pk/wp/"
            ),
            "domain": "lgdsindh.gov.pk",
            "official": True,
            "page_text": sindh_evidence,
            "snippet": sindh_evidence,
            "jurisdiction": "Sindh",
        }
    )

    all_sources.append(
        {
            "title": (
                "Government of Sindh — "
                "Birth Registration Services"
            ),
            "url": (
                "https://cm.sindh.gov.pk/news/"
                "snd-k-aaoam-kli-antthar-aor-ktar-ki-zhmt-"
                "khtm-pidaesh-amoat-nkah-aor-tlak-ki-rjsrishn-"
                "an-laen-ogei"
            ),
            "domain": "cm.sindh.gov.pk",
            "official": True,
            "page_text": (
                "The Government of Sindh announced "
                "online registration of birth, death, "
                "marriage and divorce through the "
                "provincial CRMS mobile application."
            ),
            "snippet": (
                "Birth registration is available through "
                "the provincial CRMS system."
            ),
            "jurisdiction": "Sindh",
        }
    )

    # ========================================================
    # BALOCHISTAN
    # ========================================================

    balochistan_evidence = """
BALOCHISTAN — OFFICIAL INFORMATION

The Balochistan Local Government & Rural Development
Department states that registration of vital events,
including births, falls under Local Councils.

The department provides an official Birth Certificate
service.

The department has also announced CRMS / PakID-based
online issuance of Birth, Death, Marriage and Divorce
Certificates.

A one-window birth-registration facility has also been
established at Union Council level through cooperation
between NADRA and the Local Government & Rural Development
Department.

Citizens should use the relevant Local Council /
Union Council or the officially available CRMS service.
"""

    all_sources.append(
        {
            "title": (
                "Balochistan Local Government & Rural "
                "Development — Birth Certificate"
            ),
            "url": (
                "https://lgrd.gob.pk/"
                "birth-certificate/"
            ),
            "domain": "lgrd.gob.pk",
            "official": True,
            "page_text": balochistan_evidence,
            "snippet": balochistan_evidence,
            "jurisdiction": "Balochistan",
        }
    )

    all_sources.append(
        {
            "title": (
                "Balochistan Local Government — "
                "Online Birth Registration / CRMS"
            ),
            "url": (
                "https://lgrd.gob.pk/"
                "launching-ceremony-birth-death-"
                "marriage-divorce-registration/"
            ),
            "domain": "lgrd.gob.pk",
            "official": True,
            "page_text": balochistan_evidence,
            "snippet": (
                "Balochistan announced online issuance "
                "of birth, death, marriage and divorce "
                "certificates through CRMS."
            ),
            "jurisdiction": "Balochistan",
        }
    )

    # ========================================================
    # ISLAMABAD
    # ========================================================

    islamabad_evidence = """
ISLAMABAD CAPITAL TERRITORY — OFFICIAL INFORMATION

The ICT Administration provides a dedicated Birth
Certificate service.

The official procedure requires completing the
application and submitting it with the required
information/documents at the Citizen Facilitation
Center, Mauve Area, G-11/4, Islamabad.

The ICT Administration page lists the required
birth and parent information, processing fee and
processing time.
"""

    all_sources.append(
        {
            "title": (
                "ICT Administration — Birth Certificate"
            ),
            "url": (
                "https://ictadministration.gov.pk/"
                "birth-certificate/"
            ),
            "domain": "ictadministration.gov.pk",
            "official": True,
            "page_text": islamabad_evidence,
            "snippet": islamabad_evidence,
            "jurisdiction": (
                "Islamabad Capital Territory"
            ),
        }
    )

    # ========================================================
    # AJK
    # ========================================================

    ajk_queries = [
        "site:ajk.gov.pk birth registration",
        "site:ajk.gov.pk birth certificate",
        "site:ajk.gov.pk birth certificate requirements",
        "site:ajk.gov.pk birth registration procedure",
    ]

    ajk_sources = perform_search(
        queries=ajk_queries,
        official_domains=[
            "ajk.gov.pk",
        ],
        max_results=8,
    )

    for source in ajk_sources:

        if source.get("official"):
            source["jurisdiction"] = (
                "Azad Jammu and Kashmir"
            )
            all_sources.append(source)

    # ========================================================
    # GILGIT-BALTISTAN
    # ========================================================

    gb_queries = [
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
            "birth certificate requirements"
        ),
        (
            "site:gilgitbaltistan.gov.pk "
            "birth registration procedure"
        ),
    ]

    gb_sources = perform_search(
        queries=gb_queries,
        official_domains=[
            "gilgitbaltistan.gov.pk",
        ],
        max_results=8,
    )

    for source in gb_sources:

        if source.get("official"):
            source["jurisdiction"] = (
                "Gilgit-Baltistan"
            )
            all_sources.append(source)

    # ========================================================
    # NATIONAL CRVS EVIDENCE
    # ========================================================

    national_evidence = """
PAKISTAN-WIDE CIVIL REGISTRATION

Pakistan's civil-registration ecosystem covers vital
events including birth, death, marriage and divorce.

NADRA states that the foundational layer is the
Provincial Civil Registration and Management System
(CRMS), deployed across Union Councils in Pakistan.

The exact birth-registration procedure, responsible
local office, documents, fees and processing time can
vary by province/territory.

Therefore, when the citizen does not specify an area,
the answer must be presented separately by jurisdiction
rather than applying one province's procedure to the
whole country.

A NADRA CRC must not be substituted for a civil birth
certificate.
"""

    all_sources.append(
        {
            "title": (
                "NADRA — Pakistan Registration Ecosystem"
            ),
            "url": (
                "https://www.nadra.gov.pk/ecosystem"
            ),
            "domain": "nadra.gov.pk",
            "official": True,
            "page_text": national_evidence,
            "snippet": national_evidence,
            "jurisdiction": "Pakistan-wide",
        }
    )

    # ========================================================
    # FINAL DEDUPLICATION
    # ========================================================

    final_sources = unique_sources(
        all_sources,
        limit=20,
    )

    return {
        "sources": final_sources,
        "rag_results": [],
        "jurisdiction": None,
        "all_jurisdictions": True,
        "jurisdictions_searched": ALL_JURISDICTIONS,
        "attempts": 1,
    }


# ============================================================
# BIRTH REGISTRATION ROUTER
# ============================================================

def research_birth_registration(
    question,
    language,
):

    jurisdiction = detect_jurisdiction(
        question
    )

    # Specific province / city
    if jurisdiction:

        return research_birth_specific(
            question,
            jurisdiction,
        )

    # No area specified
    return research_birth_all_jurisdictions(
        question,
        language,
    )


# ============================================================
# MARRIAGE REGISTRATION
# ============================================================

def research_marriage_registration(
    question,
    language,
):

    jurisdiction = detect_jurisdiction(
        question
    )

    if jurisdiction:

        domains = JURISDICTION_DOMAINS.get(
            jurisdiction,
            ["gov.pk"],
        )

        queries = []

        for domain in domains:

            queries.extend(
                [
                    (
                        f"site:{domain} "
                        f"marriage registration {question}"
                    ),
                    (
                        f"site:{domain} "
                        f"marriage certificate {question}"
                    ),
                    (
                        f"site:{domain} "
                        f"nikah registration {question}"
                    ),
                    (
                        f"site:{domain} "
                        "marriage registration requirements"
                    ),
                ]
            )

        sources = perform_search(
            queries=queries,
            official_domains=domains,
            max_results=12,
        )

        official_sources = [
            source
            for source in sources
            if source.get("official")
        ]

        for source in official_sources:
            source["jurisdiction"] = jurisdiction

        return {
            "sources": unique_sources(
                official_sources,
                limit=8,
            ),
            "rag_results": [],
            "jurisdiction": jurisdiction,
            "attempts": 1,
        }

    # No area — search all jurisdictions
    all_sources = []

    for region in ALL_JURISDICTIONS:

        domains = JURISDICTION_DOMAINS.get(
            region,
            ["gov.pk"],
        )

        queries = []

        for domain in domains:

            queries.extend(
                [
                    (
                        f"site:{domain} "
                        "marriage registration"
                    ),
                    (
                        f"site:{domain} "
                        "marriage certificate"
                    ),
                    (
                        f"site:{domain} "
                        "nikah registration"
                    ),
                ]
            )

        sources = perform_search(
            queries=queries,
            official_domains=domains,
            max_results=6,
        )

        for source in sources:

            if source.get("official"):

                source["jurisdiction"] = region

                all_sources.append(
                    source
                )

    return {
        "sources": unique_sources(
            all_sources,
            limit=20,
        ),
        "rag_results": [],
        "jurisdiction": None,
        "all_jurisdictions": True,
        "jurisdictions_searched": ALL_JURISDICTIONS,
        "attempts": 1,
    }


# ============================================================
# PASSPORT
# ============================================================

def research_passport(
    question,
    language,
):

    q = (
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
        term in q
        for term in fresh_terms
    )

    is_renewal = any(
        term in q
        for term in renewal_terms
    )

    is_modification = any(
        term in q
        for term in modification_terms
    )

    domains = [
        "dgip.gov.pk",
    ]

    if is_fresh:

        queries = [
            f"site:dgip.gov.pk {question}",
            (
                "site:dgip.gov.pk "
                "new passport first time requirements"
            ),
            (
                "site:dgip.gov.pk "
                "ordinary passport documents"
            ),
            (
                "site:dgip.gov.pk "
                "new passport application process"
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
                "passport correction"
            ),
        ]

    else:

        queries = [
            f"site:dgip.gov.pk {question}",
            (
                "site:dgip.gov.pk "
                "passport requirements"
            ),
            (
                "site:dgip.gov.pk "
                "passport process"
            ),
        ]

    sources = perform_search(
        queries=queries,
        official_domains=domains,
        max_results=10,
    )

    official_sources = [
        source
        for source in sources
        if source.get("official")
    ]

    if not official_sources:

        sources = perform_search(
            queries=[
                (
                    "site:dgip.gov.pk "
                    "ordinary passport requirements"
                ),
                (
                    "site:dgip.gov.pk "
                    "passport application process"
                ),
            ],
            official_domains=domains,
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
        "jurisdiction": None,
        "attempts": 1,
    }


# ============================================================
# VACCINATION
# ============================================================

def research_vaccination(
    question,
    language,
):

    q = (
        question or ""
    ).lower()

    hajj = any(
        x in q
        for x in [
            "hajj",
            "haj",
            "حج",
        ]
    )

    umrah = any(
        x in q
        for x in [
            "umrah",
            "umra",
            "عمرہ",
        ]
    )

    saudi = any(
        x in q
        for x in [
            "saudi",
            "saudia",
            "saudi arabia",
            "سعودی",
        ]
    )

    work = any(
        x in q
        for x in [
            "work visa",
            "employment visa",
            "employment",
            "work permit",
            "working",
            "job visa",
            "job in saudi",
            "iqama",
            "ملازمت",
            "ورک ویزا",
            "اقامہ",
        ]
    )

    if hajj:

        evidence = """
OFFICIAL SAUDI MINISTRY OF HEALTH — HAJJ

Saudi MOH publishes official health requirements for Hajj.
The applicable meningococcal and country-specific
requirements must be followed according to the current
official Hajj document.
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
                "page_text": evidence,
                "snippet": evidence,
            }
        ]

        return {
            "sources": sources,
            "rag_results": [],
            "jurisdiction": None,
            "attempts": 1,
        }

    if umrah:

        evidence = """
OFFICIAL SAUDI MINISTRY OF HEALTH — UMRAH

Saudi MOH publishes official health requirements for Umrah.
The applicable vaccination and certificate requirements
must be checked against the current official document.
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
                "page_text": evidence,
                "snippet": evidence,
            }
        ]

        return {
            "sources": sources,
            "rag_results": [],
            "jurisdiction": None,
            "attempts": 1,
        }

    if saudi and work:

        evidence = """
OFFICIAL EVIDENCE — ORDINARY SAUDI WORK VISA

The supplied official evidence does not establish that
every Pakistani travelling on an ordinary Saudi employment
visa must receive a specific vaccine.

Do not transfer Hajj or Umrah vaccination requirements
to ordinary employment visas.

Current medical and health-screening requirements should
be checked with the relevant Saudi and Pakistani authorities.
"""

        sources = [
            {
                "title": (
                    "Government of Pakistan / BEOE — "
                    "Work Visa Vaccination Policy"
                ),
                "url": (
                    "https://beoe.gov.pk/"
                    "files/policyguideliness/51.pdf"
                ),
                "domain": "beoe.gov.pk",
                "official": True,
                "page_text": evidence,
                "snippet": evidence,
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
                "page_text": evidence,
                "snippet": evidence,
            },
        ]

        return {
            "sources": sources,
            "rag_results": [],
            "jurisdiction": "Saudi Arabia",
            "attempts": 1,
        }

    domains = [
        "nhsrc.gov.pk",
        "nih.org.pk",
        "moh.gov.sa",
    ]

    sources = perform_search(
        queries=[
            f"site:nhsrc.gov.pk {question}",
            f"site:nih.org.pk {question}",
        ],
        official_domains=domains,
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

    sources = perform_search(
        queries=[
            f"site:nadra.gov.pk {question}",
            f"site:nadra.gov.pk {question} NADRA",
        ],
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
# PROTECTOR
# ============================================================

def research_protector(
    question,
    language,
):

    sources = perform_search(
        queries=[
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
        ],
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
# DRIVING LICENCE
# ============================================================

DRIVING_LICENSE_CATEGORIES = {
    "motorcycle": [
        "motorcycle",
        "motor cycle",
        "bike",
        "موٹر سائیکل",
        "موٹر بائیک",
    ],

    "motor car": [
        "motor car",
        "motorcar",
        "car licence",
        "car license",
        "car/jeep",
        "car",
        "jeep",
        "موٹر کار",
        "کار",
        "جیپ",
    ],

    "LTV": [
        "ltv",
        "light transport vehicle",
        "light transport",
        "لائٹ ٹرانسپورٹ",
        "ایل ٹی وی",
    ],

    "HTV": [
        "htv",
        "heavy transport vehicle",
        "heavy transport",
        "ہیوی ٹرانسپورٹ",
        "ایچ ٹی وی",
    ],

    "PSV": [
        "psv",
        "public service vehicle",
        "پبلک service vehicle",
        "پبلک سروس وہیکل",
        "پی ایس وی",
    ],

    "learner": [
        "learner",
        "learner licence",
        "learner license",
        "learner permit",
        "learning licence",
        "learning license",
        "لرنر",
        "لرنر لائسنس",
        "لرنر پرمٹ",
    ],

    "regular": [
        "regular licence",
        "regular license",
        "driving licence",
        "driving license",
        "new licence",
        "new license",
        "fresh licence",
        "fresh license",
        "new driving licence",
        "new driving license",
        "fresh driving licence",
        "fresh driving license",
        "نیا لائسنس",
        "ڈرائیونگ لائسنس",
    ],

    "renewal": [
        "renew",
        "renewal",
        "renew licence",
        "renew license",
        "licence renewal",
        "license renewal",
        "تجدید",
        "لائسنس کی تجدید",
    ],

    "duplicate": [
        "duplicate",
        "lost licence",
        "lost license",
        "replacement licence",
        "replacement license",
        "ڈپلیکیٹ",
        "گمشدہ لائسنس",
    ],

    "international": [
        "international driving permit",
        "international driving licence",
        "international driving license",
        "idp",
        "بین الاقوامی ڈرائیونگ",
    ],
}


DRIVING_JURISDICTION_DOMAINS = {
    "Punjab": [
        "dlims.punjab.gov.pk",
        "punjab.gov.pk",
    ],

    "Sindh": [
        "dls.gos.pk",
        "dlsonline.sindhpolice.gov.pk",
        "sindhpolice.gov.pk",
    ],

    "Khyber Pakhtunkhwa": [
        "kppolice.gov.pk",
        "ptpkp.gov.pk",
        "kp.gov.pk",
    ],

    "Balochistan": [
        "pkm.balochistanpolice.gov.pk",
        "balochistanpolice.gov.pk",
        "balochistan.gov.pk",
    ],

    "Islamabad Capital Territory": [
        "islamabadpolice.gov.pk",
        "dlims.islamabadpolice.gov.pk",
    ],

    "Azad Jammu and Kashmir": [
        "trafficpolice.ajk.gov.pk",
        "ajk.gov.pk",
    ],

    "Gilgit-Baltistan": [
        "dlmis.gbp.gov.pk",
        "gbp.gov.pk",
        "gilgitbaltistan.gov.pk",
    ],
}


def detect_driving_categories(question):

    q = (
        question or ""
    ).strip().lower()

    detected = []

    for category, terms in DRIVING_LICENSE_CATEGORIES.items():

        if any(
            term in q
            for term in terms
        ):
            detected.append(category)

    if not detected:
        detected.append(
            "general driving licence"
        )

    return detected


def build_driving_query_text(
    question,
    categories,
):

    return (
        f"{question} "
        f"Driving licence category: "
        f"{', '.join(categories)}"
    )


def driving_source(
    title,
    url,
    domain,
    jurisdiction,
    evidence,
):

    return {
        "title": title,
        "url": url,
        "domain": domain,
        "official": True,
        "page_text": evidence,
        "snippet": evidence,
        "jurisdiction": jurisdiction,
    }


def get_driving_official_evidence(
    jurisdiction,
    categories,
):

    category_text = ", ".join(categories)

    # ========================================================
    # PUNJAB
    # ========================================================

    if jurisdiction == "Punjab":

        evidence = f"""
JURISDICTION: PUNJAB

RESPONSIBLE AUTHORITY:
Government of Punjab — Driving Licence Information
Management System (DLIMS 2.0).

OFFICIAL PORTAL:
https://dlims.punjab.gov.pk/

NEW DRIVING LICENCE:
The official Punjab DLIMS provides Learner, Regular
and International driving licence services.

The online application process includes:

1. Create an account and log in.
2. Fill the application form.
3. Generate the PSID.
4. Complete payment.
5. Follow the official processing/approval steps.
6. Print the relevant learner/approval/processing
   information as instructed by DLIMS.

REGULAR LICENCE CATEGORIES:
Motorcycle, Car/Jeep, LTV, HTV and PSV combinations
are included in the official fee/category structure.

IMPORTANT:
The exact fee depends on the selected category and
should be checked on the current official DLIMS fee
structure.

USER REQUESTED CATEGORY:
{category_text}
"""

        return [
            driving_source(
                "Punjab DLIMS 2.0 — Official Driving Licence Portal",
                "https://dlims.punjab.gov.pk/",
                "dlims.punjab.gov.pk",
                "Punjab",
                evidence,
            ),
            driving_source(
                "Punjab DLIMS 2.0 — Official Fee Structure",
                "https://dlims.punjab.gov.pk/fee_structure",
                "dlims.punjab.gov.pk",
                "Punjab",
                evidence,
            ),
        ]

    # ========================================================
    # SINDH
    # ========================================================

    if jurisdiction == "Sindh":

        evidence = f"""
JURISDICTION: SINDH

RESPONSIBLE AUTHORITY:
Sindh Police — Driving License Sindh (DLS).

OFFICIAL PORTAL:
https://dls.gos.pk/

NEW DRIVING LICENCE:
The official computerized licence procedure includes:

1. DLS online application/registration.
2. Appearance at the DLS front desk.
3. Screening and registration.
4. Medical examination.
5. Fee payment.
6. Written/oral computer test.
7. Road test where applicable.
8. Final licence receipt.

GENERAL REQUIREMENTS:
The official source identifies a valid original CNIC,
physical fitness and a minimum age of 18 for the general
licence process.

CATEGORIES:
Motorcycle, Motor Car, LTV and HTV are covered.

USER REQUESTED CATEGORY:
{category_text}
"""

        return [
            driving_source(
                "Driving License Sindh — Official DLS",
                "https://dls.gos.pk/",
                "dls.gos.pk",
                "Sindh",
                evidence,
            ),
            driving_source(
                "Driving License Sindh — Computerized Licence Process",
                "https://dls.gos.pk/pro-comp-lic.html",
                "dls.gos.pk",
                "Sindh",
                evidence,
            ),
        ]

    # ========================================================
    # KHYBER PAKHTUNKHWA
    # ========================================================

    if jurisdiction == "Khyber Pakhtunkhwa":

        evidence = f"""
JURISDICTION: KHYBER PAKHTUNKHWA

RESPONSIBLE AUTHORITIES:
Khyber Pakhtunkhwa Transport Department,
Khyber Pakhtunkhwa Information Technology Board (KPITB),
and relevant licensing authorities.

PRIMARY DIGITAL APPLICATION:
Dastak App

OFFICIAL KP TRANSPORT DIGITAL LICENSING:
The KP transport licensing workflow uses the Dastak App
for online driving licence services.

Dastak is an important official digital route for
KP driving licence applications and related services.

LICENCE CATEGORIES:
The official KP transport licensing system covers:

- Learner Driving Licence
- LTV Driving Licence
- HTV Driving Licence
- International Driving Licence

NEW LICENCE:
For a new driving licence, applicants can use the
Dastak digital workflow where the relevant service
is available.

The digital workflow may include:
- Applicant profile
- CNIC/NADRA verification
- Required documents or attachments
- Officer verification/approval
- Payment
- Licence processing

RENEWAL:
KP Transport Department also provides notified services
for driving licence renewal, including LTV/PSV and
HTV/PSV categories.

IMPORTANT:
The exact online steps may vary according to the licence
category and the service currently available through
Dastak.

POLICE SAHULAT MARKAZ:
KP Police's official Police Sahulat Markaz also provides
specific driving-related services including:

- Learner permit
- Traffic learner certificate
- Duplicate driving licence

Therefore:
- Dastak should be identified as the primary digital
  route for the KP transport/driving licence workflow.
- Police Sahulat Markaz may be mentioned for the specific
  services it officially provides.
- Do not state that Dastak is unrelated to driving licences.

USER REQUESTED CATEGORY:
{category_text}
"""

        return [
            driving_source(
                "KP Transport Department — Official Public Services",
                "https://transport.kp.gov.pk/public-service.php",
                "transport.kp.gov.pk",
                "Khyber Pakhtunkhwa",
                evidence,
            ),
            driving_source(
                "KP Government / KPITB — Transport License System",
                "https://ecitizen.kp.gov.pk/storage/yearbook/KPITBAnnualReport2025.pdf",
                "ecitizen.kp.gov.pk",
                "Khyber Pakhtunkhwa",
                evidence,
            ),
            driving_source(
                "KP Government — Driving Licence Digitization / Dastak",
                "https://dgipr.kp.gov.pk/09012025-11/",
                "dgipr.kp.gov.pk",
                "Khyber Pakhtunkhwa",
                evidence,
            ),
            driving_source(
                "KP Police — Police Sahulat Markaz",
                "https://apipsm.kppolice.gov.pk/psm/VideoTutorial",
                "apipsm.kppolice.gov.pk",
                "Khyber Pakhtunkhwa",
                evidence,
            ),
        ]
    # ========================================================
    # BALOCHISTAN
    # ========================================================

    if jurisdiction == "Balochistan":

        evidence = f"""
JURISDICTION: BALOCHISTAN

RESPONSIBLE AUTHORITY:
Balochistan Police / Police Mobile Khidmat Markaz.

OFFICIAL SERVICE:
Police Mobile Khidmat Markaz provides driving licence
services.

The official service includes:

- Learner Driving Licence
- Driving Licence Renewal
- International Driving Licence
- Duplicate Driving Licence
- Endorsement of Licence

LEARNER LICENCE:
The official service lists:

- Original CNIC and one copy
- Traffic rules/code book
- Medical certificate for applicants aged 50 or above

Published learner age requirements include:

- Motorcycle / Motor Car: 18 years
- LTV: 21 years

The learner licence is valid for six months.

IMPORTANT:
Do not present learner requirements as the complete
regular-licence procedure unless the official evidence
supports the additional regular-licence steps.

USER REQUESTED CATEGORY:
{category_text}
"""

        return [
            driving_source(
                "Balochistan Police — Police Mobile Khidmat Markaz",
                "https://pkm.balochistanpolice.gov.pk/public/home/services",
                "pkm.balochistanpolice.gov.pk",
                "Balochistan",
                evidence,
            ),
            driving_source(
                "Balochistan Police — Official PKM",
                "https://pkm.balochistanpolice.gov.pk/",
                "pkm.balochistanpolice.gov.pk",
                "Balochistan",
                evidence,
            ),
        ]

    # ========================================================
    # ISLAMABAD
    # ========================================================

    if jurisdiction == "Islamabad Capital Territory":

        evidence = f"""
JURISDICTION: ISLAMABAD CAPITAL TERRITORY

RESPONSIBLE AUTHORITY:
Islamabad Traffic Police (ITP).

OFFICIAL ONLINE PORTAL:
https://dlims.islamabadpolice.gov.pk/

LICENSING SERVICES:
Islamabad Traffic Police provides:

- New driving licence
- Learner permit
- Driving tests
- Renewal
- Duplicate licence
- International driving permit

ONLINE SERVICE:
The official ITP-DLIMS portal provides online driving
licence facilities.

IMPORTANT:
Specific documents, fees and processing times should only
be stated when supported by the current official ITP
evidence.

USER REQUESTED CATEGORY:
{category_text}
"""

        return [
            driving_source(
                "Islamabad Traffic Police — Licensing Services",
                "https://www.islamabadpolice.gov.pk/division.php?slug=islamabad-traffic-police",
                "islamabadpolice.gov.pk",
                "Islamabad Capital Territory",
                evidence,
            ),
            driving_source(
                "ITP-DLIMS — Official Driving Licence Portal",
                "https://dlims.islamabadpolice.gov.pk/",
                "dlims.islamabadpolice.gov.pk",
                "Islamabad Capital Territory",
                evidence,
            ),
        ]

    # ========================================================
    # AJK
    # ========================================================

    if jurisdiction == "Azad Jammu and Kashmir":

        evidence = f"""
JURISDICTION: AZAD JAMMU AND KASHMIR

RESPONSIBLE AUTHORITY:
Traffic Police AJ&K.

OFFICIAL PORTAL:
https://trafficpolice.ajk.gov.pk/

The official Traffic Police AJ&K portal provides:

- Licence procedure
- Licence verification
- Application tracking
- Licence issuance office locations
- DLMS application forms
- Medical form
- Fee challan form
- Licence fee details
- Theory book for test
- Traffic signs

Applicants should use the official Traffic Police AJ&K
procedure and forms for the selected licence category.

USER REQUESTED CATEGORY:
{category_text}
"""

        return [
            driving_source(
                "Traffic Police AJ&K — Official Licence Portal",
                "https://trafficpolice.ajk.gov.pk/",
                "trafficpolice.ajk.gov.pk",
                "Azad Jammu and Kashmir",
                evidence,
            ),
        ]

    # ========================================================
    # GILGIT-BALTISTAN
    # ========================================================

    if jurisdiction == "Gilgit-Baltistan":

        evidence = f"""
JURISDICTION: GILGIT-BALTISTAN

RESPONSIBLE AUTHORITY:
Gilgit-Baltistan Driving License Issuance Management
System (DLMIS).

OFFICIAL PORTAL:
https://dlmis.gbp.gov.pk/

The official system provides:

- Regular Driving Licence application
- Driving Licence renewal
- Duplicate licence
- International driving licence
- Medical form
- Licensing centre information

The official regular licence application form includes
categories such as:

- Motorcycle
- Motor Car
- LTV
- HTV
- Motor Rickshaw
- Tractor
- Motor Cab
- Other specified vehicle classes

USER REQUESTED CATEGORY:
{category_text}
"""

        return [
            driving_source(
                "Gilgit-Baltistan DLMIS — Official Driving Licence System",
                "https://dlmis.gbp.gov.pk/",
                "dlmis.gbp.gov.pk",
                "Gilgit-Baltistan",
                evidence,
            ),
            driving_source(
                "Gilgit-Baltistan DLMIS — Regular Licence Form",
                "https://dlmis.gbp.gov.pk/public/downloads/regular.pdf",
                "dlmis.gbp.gov.pk",
                "Gilgit-Baltistan",
                evidence,
            ),
        ]

    return []


def research_driving_license(
    question,
    language,
):

    jurisdiction = detect_jurisdiction(
        question
    )

    categories = detect_driving_categories(
        question
    )

    # ========================================================
    # SPECIFIC JURISDICTION
    # ========================================================

    if jurisdiction:

        sources = get_driving_official_evidence(
            jurisdiction,
            categories,
        )

        return {
            "sources": unique_sources(
                sources,
                limit=10,
            ),
            "rag_results": [],
            "jurisdiction": jurisdiction,
            "all_jurisdictions": False,
            "driving_categories": categories,
            "attempts": 1,
        }

    # ========================================================
    # NO JURISDICTION
    # ========================================================

    all_sources = []

    for region in ALL_JURISDICTIONS:

        region_sources = (
            get_driving_official_evidence(
                region,
                categories,
            )
        )

        all_sources.extend(
            region_sources
        )

    return {
        "sources": unique_sources(
            all_sources,
            limit=30,
        ),
        "rag_results": [],
        "jurisdiction": None,
        "all_jurisdictions": True,
        "jurisdictions_searched": ALL_JURISDICTIONS,
        "driving_categories": categories,
        "attempts": 1,
    }
# ============================================================
# GENERAL DEPARTMENT
# ============================================================

def research_department(
    question,
    department,
    language,
):

    from config.departments import DEPARTMENTS

    config = DEPARTMENTS.get(
        department,
        {},
    )

    domains = config.get(
        "official_domains",
        [],
    )

    jurisdiction = detect_jurisdiction(
        question
    )

    keywords = config.get(
        "keywords",
        [],
    )

    keyword_text = " ".join(
        keywords[:6]
    )

    queries = []

    if jurisdiction:

        primary = get_jurisdiction_domain(
            jurisdiction
        )

        if primary:

            queries.append(
                f"site:{primary} {question}"
            )

            queries.append(
                f"site:{primary} "
                f"{keyword_text} "
                f"{question}"
            )

    if not queries and domains:

        queries.append(
            f"site:{domains[0]} {question}"
        )

    if domains:

        queries.append(
            f"site:{domains[0]} "
            f"{keyword_text} "
            f"{question}"
        )

    sources = perform_search(
        queries=queries,
        official_domains=domains,
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
                limit=8,
            ),
            "rag_results": [],
            "jurisdiction": jurisdiction,
            "attempts": 1,
        }

    return {
        "sources": [],
        "rag_results": [],
        "jurisdiction": jurisdiction,
        "attempts": 2,
    }


# ============================================================
# MAIN ROUTER
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

    if department == "Passport":

        return research_passport(
            question,
            language,
        )

    if department == "Protector for Visa":

        return research_protector(
            question,
            language,
        )

    if department == "Vaccination for Travelling Abroad":

        return research_vaccination(
            question,
            language,
        )

    if department == "Driving Licence":

        return research_driving_license(
            question,
            language,
        )

    if department == "Union Council / Local Government":

        q = (
            question or ""
        ).strip().lower()

        # ----------------------------------------------------
        # BIRTH REGISTRATION / BIRTH CERTIFICATE
        # ----------------------------------------------------

        birth_terms = [
            "birth certificate",
            "birth registration",
            "birth registration certificate",
            "new birth certificate",
            "newborn registration",
            "child birth registration",
            "register a birth",
            "registration of birth",
            "birth certificate requirements",
            "birth registration requirements",
            "birth certificate documents",
            "birth registration documents",
            "پیدائش سرٹیفکیٹ",
            "پیدائش کا سرٹیفکیٹ",
            "پیدائش رجسٹریشن",
            "پیدائش کا اندراج",
            "پیدائش کی رجسٹریشن",
        ]

        if any(
            term in q
            for term in birth_terms
        ):

            return research_birth_registration(
                question,
                language,
            )

        # ----------------------------------------------------
        # MARRIAGE REGISTRATION / MARRIAGE CERTIFICATE
        # ----------------------------------------------------

        marriage_terms = [
            "marriage",
            "marriage certificate",
            "marriage registration",
            "register marriage",
            "registration of marriage",
            "marriage registration requirements",
            "marriage certificate requirements",
            "marriage documents",
            "marriage document",
            "nikah",
            "nikah registration",
            "nikah nama",
            "nikahnama",
            "nikah nama registration",
            "marriage registration certificate",
            "شادی",
            "شادی رجسٹریشن",
            "شادی کا سرٹیفکیٹ",
            "شادی کی رجسٹریشن",
            "نکاح",
            "نکاح رجسٹریشن",
            "نکاح نامہ",
            "نکاح نامہ رجسٹریشن",
        ]

        if any(
            term in q
            for term in marriage_terms
        ):

            return research_marriage_registration(
                question,
                language,
            )

    return research_department(
        question,
        department,
        language,
    )
