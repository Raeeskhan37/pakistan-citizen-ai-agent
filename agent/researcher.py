from config.departments import DEPARTMENTS
from search.web_search import perform_search


SEARCH_TERMS = {

    "NADRA":
        "NADRA CNIC NICOP POC CRC FRC PakID Pakistan",

    "Passport":
        "Pakistan passport DGI&P DGIP passport renewal application fee requirements",

    "Union Council / Local Government":
        "Pakistan union council local government birth death marriage divorce certificate",

    "Driving Licence":
        "Pakistan driving licence license learner renewal driving test DLIMS",

    "Arms Licence":
        "Pakistan arms licence license official government procedure renewal",

    "Police Clearance":
        "Pakistan police character certificate police clearance certificate official",

    "Protector for Visa":
        "Pakistan protector of emigrants overseas employment BE&OE protector procedure",

    "Vaccination for Travelling Abroad":
        "Pakistan travel vaccination international travel health yellow fever meningitis official",

    "Domicile":
        "Pakistan domicile certificate district government procedure requirements",
}


def build_queries(question, department):

    if department not in DEPARTMENTS:

        return [
            question,
            f"Pakistan government {question}",
        ]

    domains = DEPARTMENTS[
        department
    ]["official_domains"]

    base_terms = SEARCH_TERMS.get(
        department,
        department
    )

    queries = [

        f"{base_terms} {question}",

        f"Pakistan {department} {question}",
    ]

    for domain in domains[:4]:

        queries.append(
            f"site:{domain} {base_terms} {question}"
        )

    return queries


def research_question(
    question,
    department,
):

    if department in DEPARTMENTS:

        official_domains = DEPARTMENTS[
            department
        ]["official_domains"]

    else:

        official_domains = [
            "gov.pk"
        ]

    queries = build_queries(
        question,
        department
    )

    sources = perform_search(
        queries=queries,
        official_domains=official_domains,
        max_results=8,
    )

    return {
        "queries": queries,
        "sources": sources,
    }
