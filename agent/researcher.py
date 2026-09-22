from config.departments import DEPARTMENTS
from search.web_search import perform_search

from rag.nadra_retriever import (
    retrieve_nadra,
    has_useful_evidence,
)


PROVINCE_TERMS = {
    "Punjab": [
        "punjab",
        "پنجاب",
    ],
    "Sindh": [
        "sindh",
        "سندھ",
    ],
    "Khyber Pakhtunkhwa": [
        "khyber pakhtunkhwa",
        "kpk",
        "kp",
        "خیبر پختونخوا",
        "خیبر پختونخواہ",
    ],
    "Balochistan": [
        "balochistan",
        "بلوچستان",
    ],
    "Islamabad": [
        "islamabad",
        "ict",
        "اسلام آباد",
    ],
    "Azad Jammu and Kashmir": [
        "azad kashmir",
        "ajk",
        "آزاد کشمیر",
    ],
    "Gilgit-Baltistan": [
        "gilgit baltistan",
        "gilgit-baltistan",
        "gb",
        "گلگت بلتستان",
    ],
}


PROVINCE_DOMAINS = {
    "Punjab": [
        "punjab.gov.pk",
        "lgcd.punjab.gov.pk",
        "trafficpolice.punjab.gov.pk",
        "dlims.punjab.gov.pk",
        "punjabpolice.gov.pk",
    ],
    "Sindh": [
        "sindh.gov.pk",
        "sindhpolice.gov.pk",
    ],
    "Khyber Pakhtunkhwa": [
        "kp.gov.pk",
        "lgkp.gov.pk",
        "kppolice.gov.pk",
    ],
    "Balochistan": [
        "balochistan.gov.pk",
        "lgd.balochistan.gov.pk",
        "balochistanpolice.gov.pk",
    ],
    "Islamabad": [
        "ictadministration.gov.pk",
        "islamabadpolice.gov.pk",
    ],
    "Azad Jammu and Kashmir": [
        "ajk.gov.pk",
    ],
    "Gilgit-Baltistan": [
        "gilgitbaltistan.gov.pk",
    ],
}


GENERAL_JURISDICTIONS = [
    "Punjab",
    "Sindh",
    "Khyber Pakhtunkhwa",
    "Balochistan",
    "Islamabad",
    "Azad Jammu and Kashmir",
    "Gilgit-Baltistan",
]


def detect_jurisdiction(question):
    question_lower = question.lower()

    for jurisdiction, terms in PROVINCE_TERMS.items():

        for term in terms:

            if term.lower() in question_lower:
                return jurisdiction

    return None


def get_department_domains(
    department,
):
    department_data = DEPARTMENTS.get(
        department,
        {},
    )

    return department_data.get(
        "official_domains",
        ["gov.pk"],
    )


def get_search_domains(
    department,
    jurisdiction=None,
):
    department_domains = get_department_domains(
        department
    )

    if not jurisdiction:
        return department_domains

    jurisdiction_domains = PROVINCE_DOMAINS.get(
        jurisdiction,
        [],
    )

    selected = []

    for domain in (
        jurisdiction_domains
        + department_domains
    ):

        if domain not in selected:
            selected.append(domain)

    return selected


def build_department_queries(
    question,
    department,
    attempt,
    jurisdiction=None,
):
    queries = []

    if jurisdiction:

        domains = get_search_domains(
            department,
            jurisdiction,
        )

        jurisdiction_text = (
            f" {jurisdiction}"
        )

        if attempt == 1:

            for domain in domains:

                queries.append(
                    f"site:{domain} "
                    f"{question}"
                    f"{jurisdiction_text}"
                )

        elif attempt == 2:

            for domain in domains:

                queries.append(
                    f"site:{domain} "
                    f"{question} "
                    f"procedure requirements"
                    f"{jurisdiction_text}"
                )

                queries.append(
                    f"site:{domain} "
                    f"{question} "
                    f"documents fee"
                    f"{jurisdiction_text}"
                )

        else:

            for domain in domains:

                queries.append(
                    f"site:{domain} "
                    f"{question} "
                    f"official rules"
                    f"{jurisdiction_text}"
                )

                queries.append(
                    f"site:{domain} "
                    f"{question} FAQ"
                    f"{jurisdiction_text}"
                )

        return queries

    # ---------------------------------------------------------
    # GENERAL PAKISTAN QUESTION
    # ---------------------------------------------------------

    domains = get_department_domains(
        department
    )

    if attempt == 1:

        for domain in domains:

            queries.append(
                f"site:{domain} "
                f"{question} Pakistan"
            )

    elif attempt == 2:

        for domain in domains:

            queries.append(
                f"site:{domain} "
                f"{question} "
                f"requirements Pakistan"
            )

            queries.append(
                f"site:{domain} "
                f"{question} "
                f"procedure Pakistan"
            )

    else:

        for domain in domains:

            queries.append(
                f"site:{domain} "
                f"{question} "
                f"official rules Pakistan"
            )

            queries.append(
                f"site:{domain} "
                f"{question} FAQ Pakistan"
            )

        # Search major jurisdictions individually
        for jurisdiction in GENERAL_JURISDICTIONS:

            jurisdiction_domains = (
                PROVINCE_DOMAINS.get(
                    jurisdiction,
                    [],
                )
            )

            for domain in jurisdiction_domains:

                queries.append(
                    f"site:{domain} "
                    f"{question} "
                    f"{jurisdiction}"
                )

    return queries


def add_unique_sources(
    destination,
    sources,
):
    existing_urls = {
        item.get("url")
        for item in destination
        if item.get("url")
    }

    for source in sources:

        if not isinstance(
            source,
            dict,
        ):
            continue

        url = source.get(
            "url",
            "",
        )

        if not url:
            continue

        if url not in existing_urls:

            destination.append(
                source
            )

            existing_urls.add(
                url
            )


def research_nadra(
    question,
    language="English",
):
    all_sources = []
    rag_results = []
    attempts = 0

    for attempt in range(
        1,
        4,
    ):

        attempts = attempt

        try:

            current_rag = retrieve_nadra(
                question=question,
                language=language,
                top_k=6,
            )

        except Exception:

            current_rag = []

        if current_rag:

            rag_results.extend(
                current_rag
            )

        if attempt == 1:

            queries = [
                f"site:nadra.gov.pk {question}",
                f"site:nadra.gov.pk "
                f"{question} requirements",
            ]

        elif attempt == 2:

            queries = [
                f"site:nadra.gov.pk "
                f"{question} procedure",
                f"site:nadra.gov.pk "
                f"{question} documents",
                f"site:nadra.gov.pk "
                f"{question} requirements fee",
            ]

        else:

            queries = [
                f"site:nadra.gov.pk "
                f"{question} official",
                f"site:nadra.gov.pk "
                f"{question} FAQ",
                f"site:nadra.gov.pk "
                f"{question} policy",
            ]

        try:

            sources = perform_search(
                queries=queries,
                official_domains=[
                    "nadra.gov.pk",
                ],
                max_results=8,
            )

        except Exception:

            sources = []

        add_unique_sources(
            all_sources,
            sources,
        )

        official_sources = [
            source
            for source in all_sources
            if source.get("official")
        ]

        if (
            has_useful_evidence(
                current_rag
            )
            and official_sources
        ):
            break

    unique_rag = []
    seen = set()

    for item in rag_results:

        index_number = item.get(
            "index"
        )

        if index_number in seen:
            continue

        seen.add(
            index_number
        )

        unique_rag.append(
            item
        )

    unique_rag.sort(
        key=lambda item: item.get(
            "score",
            0,
        ),
        reverse=True,
    )

    return {
        "sources": all_sources,
        "rag_results": unique_rag[:6],
        "attempts": attempts,
        "jurisdiction": None,
    }


def research_department(
    question,
    department,
):
    jurisdiction = detect_jurisdiction(
        question
    )

    all_sources = []
    attempts = 0

    for attempt in range(
        1,
        4,
    ):

        attempts = attempt

        queries = build_department_queries(
            question=question,
            department=department,
            attempt=attempt,
            jurisdiction=jurisdiction,
        )

        try:

            sources = perform_search(
                queries=queries,
                official_domains=get_search_domains(
                    department,
                    jurisdiction,
                ),
                max_results=8,
            )

        except Exception:

            sources = []

        add_unique_sources(
            all_sources,
            sources,
        )

        official_sources = [
            source
            for source in all_sources
            if source.get("official")
        ]

        if official_sources:
            break

    return {
        "sources": all_sources,
        "rag_results": [],
        "attempts": attempts,
        "jurisdiction": jurisdiction,
    }


def research_question(
    question,
    department,
    language="English",
):
    if department == "NADRA":

        return research_nadra(
            question,
            language,
        )

    if department in DEPARTMENTS:

        return research_department(
            question,
            department,
        )

    return {
        "sources": [],
        "rag_results": [],
        "attempts": 3,
        "jurisdiction": None,
    }
