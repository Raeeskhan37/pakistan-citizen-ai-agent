import json
import os
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# ============================================================
# NADRA RAG CONFIGURATION
# ============================================================

ENGLISH_FAISS_URL = (
    "https://raw.githubusercontent.com/"
    "Raeeskhan37/NADRA-Policy-Assistant/main/"
    "nadra_registration_policy.faiss"
)

ENGLISH_METADATA_URL = (
    "https://raw.githubusercontent.com/"
    "Raeeskhan37/NADRA-Policy-Assistant/main/"
    "nadra_registration_policy_metadata.json"
)

ENGLISH_CONFIG_URL = (
    "https://raw.githubusercontent.com/"
    "Raeeskhan37/NADRA-Policy-Assistant/main/"
    "nadra_registration_policy_config.json"
)

URDU_FAISS_URL = (
    "https://raw.githubusercontent.com/"
    "Raeeskhan37/NADRA-Policy-Assistant/main/"
    "urdu/nadra_urdu_6_0_2_v2.faiss"
)

URDU_CHUNKS_URL = (
    "https://raw.githubusercontent.com/"
    "Raeeskhan37/NADRA-Policy-Assistant/main/"
    "urdu/nadra_urdu_6_0_2_v2_chunks.pkl"
)

URDU_CONFIG_URL = (
    "https://raw.githubusercontent.com/"
    "Raeeskhan37/NADRA-Policy-Assistant/main/"
    "urdu/metadata.json"
)


# ============================================================
# LOCAL CACHE DIRECTORY
# ============================================================

CACHE_DIR = os.path.join(
    os.path.dirname(__file__),
    "nadra_cache",
)

os.makedirs(
    CACHE_DIR,
    exist_ok=True,
)


# ============================================================
# LOCAL FILE PATHS
# ============================================================

ENGLISH_FAISS = os.path.join(
    CACHE_DIR,
    "nadra_registration_policy.faiss",
)

ENGLISH_METADATA = os.path.join(
    CACHE_DIR,
    "nadra_registration_policy_metadata.json",
)

ENGLISH_CONFIG = os.path.join(
    CACHE_DIR,
    "nadra_registration_policy_config.json",
)

URDU_FAISS = os.path.join(
    CACHE_DIR,
    "nadra_urdu_6_0_2_v2.faiss",
)

URDU_CHUNKS = os.path.join(
    CACHE_DIR,
    "nadra_urdu_6_0_2_v2_chunks.pkl",
)

URDU_CONFIG = os.path.join(
    CACHE_DIR,
    "metadata.json",
)


# ============================================================
# EMBEDDING MODELS
# ============================================================

ENGLISH_EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

URDU_EMBEDDING_MODEL = (
    "intfloat/multilingual-e5-base"
)


# ============================================================
# DOWNLOAD HELPER
# ============================================================

def download_file(
    url,
    destination,
):
    if os.path.exists(destination):
        return destination

    import requests

    response = requests.get(
        url,
        timeout=60,
    )

    response.raise_for_status()

    with open(
        destination,
        "wb",
    ) as file:
        file.write(
            response.content
        )

    return destination


# ============================================================
# PREPARE ENGLISH DATA
# ============================================================

def prepare_english_data():

    download_file(
        ENGLISH_FAISS_URL,
        ENGLISH_FAISS,
    )

    download_file(
        ENGLISH_METADATA_URL,
        ENGLISH_METADATA,
    )

    download_file(
        ENGLISH_CONFIG_URL,
        ENGLISH_CONFIG,
    )


# ============================================================
# PREPARE URDU DATA
# ============================================================

def prepare_urdu_data():

    download_file(
        URDU_FAISS_URL,
        URDU_FAISS,
    )

    download_file(
        URDU_CHUNKS_URL,
        URDU_CHUNKS,
    )

    download_file(
        URDU_CONFIG_URL,
        URDU_CONFIG,
    )


# ============================================================
# LOAD ENGLISH INDEX
# ============================================================

def load_english_index():

    prepare_english_data()

    return faiss.read_index(
        ENGLISH_FAISS
    )


# ============================================================
# LOAD URDU INDEX
# ============================================================

def load_urdu_index():

    prepare_urdu_data()

    return faiss.read_index(
        URDU_FAISS
    )


# ============================================================
# LOAD ENGLISH METADATA
# ============================================================

def load_english_metadata():

    prepare_english_data()

    with open(
        ENGLISH_METADATA,
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    if isinstance(
        data,
        dict,
    ):

        if "chunks" in data:
            data = data["chunks"]

        elif "metadata" in data:
            data = data["metadata"]

        elif "chunk_metadata" in data:
            data = data["chunk_metadata"]

        else:

            values = list(
                data.values()
            )

            if (
                values
                and isinstance(
                    values[0],
                    dict,
                )
            ):
                data = values

    return data


# ============================================================
# LOAD URDU CHUNKS
# ============================================================

def load_urdu_chunks():

    prepare_urdu_data()

    with open(
        URDU_CHUNKS,
        "rb",
    ) as file:

        return pickle.load(file)


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

def load_embedding_model(
    language="English",
):

    if language == "اردو":

        return SentenceTransformer(
            URDU_EMBEDDING_MODEL
        )

    return SentenceTransformer(
        ENGLISH_EMBEDDING_MODEL
    )


# ============================================================
# EXTRACT CHUNK TEXT
# ============================================================

def get_chunk_text(
    chunk,
):

    if isinstance(
        chunk,
        str,
    ):
        return chunk

    if isinstance(
        chunk,
        dict,
    ):

        for key in [
            "text",
            "content",
            "chunk",
            "page_text",
        ]:

            if key in chunk:
                return str(
                    chunk[key]
                )

    return str(chunk)


# ============================================================
# EXTRACT PAGE
# ============================================================

def get_page(
    chunk,
):

    if isinstance(
        chunk,
        dict,
    ):

        return chunk.get(
            "page",
            "N/A",
        )

    return "N/A"


# ============================================================
# EXTRACT SECTION
# ============================================================

def get_section(
    chunk,
):

    if isinstance(
        chunk,
        dict,
    ):

        return (
            chunk.get(
                "major_section",
                "",
            )
            or chunk.get(
                "section",
                "",
            )
        )

    return ""


# ============================================================
# CRC QUERY EXPANSION
# ============================================================

def expand_nadra_query(
    question,
    language,
):
    """
    Expand common NADRA service terminology before
    embedding the question.

    This does NOT add policy information.
    It only helps the existing RAG retrieve the
    correct policy chunks.
    """

    question = (
        question or ""
    ).strip()

    if not question:
        return question

    question_lower = question.lower()

    crc_terms = [
        "crc",
        "child registration certificate",
        "b-form",
        "b form",
        "child registration",
        "minor registration",
        "under 18",
        "under eighteen",
        "juvenile",
    ]

    is_crc_question = any(
        term in question_lower
        for term in crc_terms
    )

    if language == "اردو":

        urdu_crc_terms = [
            "سی آر سی",
            "چائلڈ رجسٹریشن",
            "ب فارم",
            "ب فارم",
            "بچے کی رجسٹریشن",
            "بچے کا رجسٹریشن",
            "بچوں کی رجسٹریشن",
            "نابالغ",
            "جیوینائل",
        ]

        is_crc_question = (
            is_crc_question
            or any(
                term in question
                for term in urdu_crc_terms
            )
        )

    if not is_crc_question:
        return question

    if language == "اردو":

        return (
            question
            + "\n\n"
            + "CRC / Child Registration Certificate / "
            + "B-Form / minor / under 18 / juvenile "
            + "registration / fresh registration / "
            + "requirements / documents / birth certificate"
        )

    return (
        question
        + "\n\n"
        + "CRC Child Registration Certificate "
        + "B-Form child registration minor "
        + "under 18 juvenile fresh registration "
        + "requirements documents birth certificate"
    )


# ============================================================
# RETRIEVE FROM NADRA RAG
# ============================================================

def retrieve_nadra(
    question,
    language="English",
    top_k=8,
):

    if not question or not question.strip():
        return []

    question = question.strip()

    # --------------------------------------------------------
    # EXPAND QUERY FOR BETTER POLICY RETRIEVAL
    # --------------------------------------------------------

    retrieval_query = expand_nadra_query(
        question,
        language,
    )

    # --------------------------------------------------------
    # LOAD LANGUAGE-SPECIFIC RAG
    # --------------------------------------------------------

    if language == "اردو":

        index = load_urdu_index()

        chunks = load_urdu_chunks()

        model = load_embedding_model(
            "اردو"
        )

        query = (
            "query: "
            + retrieval_query
        )

    else:

        index = load_english_index()

        chunks = load_english_metadata()

        model = load_embedding_model(
            "English"
        )

        query = retrieval_query

    # --------------------------------------------------------
    # CREATE QUERY EMBEDDING
    # --------------------------------------------------------

    embedding = model.encode(
        [query],
        normalize_embeddings=True,
    )

    embedding = np.asarray(
        embedding,
        dtype="float32",
    )

    # --------------------------------------------------------
    # FAISS SEARCH
    # --------------------------------------------------------

    search_k = min(
        max(
            top_k,
            12,
        ),
        index.ntotal,
    )

    scores, indices = index.search(
        embedding,
        search_k,
    )

    results = []

    # --------------------------------------------------------
    # BUILD RESULTS
    # --------------------------------------------------------

    for score, index_number in zip(
        scores[0],
        indices[0],
    ):

        if index_number < 0:
            continue

        if index_number >= len(chunks):
            continue

        chunk = chunks[
            index_number
        ]

        results.append(
            {
                "text": get_chunk_text(
                    chunk
                ),
                "page": get_page(
                    chunk
                ),
                "section": get_section(
                    chunk
                ),
                "score": float(
                    score
                ),
                "index": int(
                    index_number
                ),
                "source": (
                    "NADRA Registration Policy "
                    "RP-6.0.2"
                ),
            }
        )

    return results[:top_k]


# ============================================================
# BUILD POLICY EVIDENCE
# ============================================================

def build_nadra_evidence(
    results,
):

    if not results:

        return (
            "No relevant NADRA Registration Policy "
            "evidence was retrieved."
        )

    evidence = [
        "SOURCE: NADRA Registration Policy",
        "VERSION: RP-6.0.2",
        "EFFECTIVE DATE: 21 September 2026",
        "",
        "RELEVANT POLICY EVIDENCE:",
    ]

    # Send up to 5 strong policy chunks to the AI.
    selected_results = results[:5]

    for number, item in enumerate(
        selected_results,
        start=1,
    ):

        text = item.get(
            "text",
            "",
        )

        text = text[:5000]

        evidence.append(
            f"""
[EVIDENCE {number}]
Page: {item.get("page", "N/A")}
Section: {item.get("section", "")}
Retrieval Score: {item.get("score", 0):.4f}

{text}
"""
        )

    return "\n".join(
        evidence
    )


# ============================================================
# SIMPLE QUALITY CHECK
# ============================================================

def has_useful_evidence(
    results,
    minimum_score=0.45,
):

    if not results:
        return False

    best_score = max(
        item.get(
            "score",
            0,
        )
        for item in results
    )

    return best_score >= minimum_score
