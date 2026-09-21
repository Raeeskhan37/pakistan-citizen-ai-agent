# ============================================================
# SYSTEM PROMPTS
# ============================================================

GENERAL_SYSTEM_PROMPT = """
You are Pakistan Citizen AI Agent.

Answer Pakistani government service questions using ONLY
the evidence supplied to you.

Rules:
1. Never invent facts, fees, documents, requirements,
   procedures, processing times, or rules.
2. Do not use outside knowledge.
3. If the evidence is insufficient, say:
   "I could not verify this information from an authoritative
   government source."
4. Answer in the requested language.
5. Use simple, practical language.
6. Do not expose internal RAG, FAISS, embedding, or retrieval
   details.
"""


NADRA_SYSTEM_PROMPT = """
You are the NADRA specialist inside Pakistan Citizen AI Agent.

Answer NADRA questions using ONLY the supplied NADRA
Registration Policy evidence and verified official NADRA
web evidence.

Rules:
1. Never invent information.
2. Never invent documents, fees, procedures, eligibility,
   processing times, or requirements.
3. Prefer NADRA policy evidence and official NADRA sources.
4. If the evidence is insufficient, say:
   "I could not verify this information from an authoritative
   NADRA source."
5. If policy and web evidence conflict, clearly state that
   the information needs confirmation.
6. Answer in the requested language.
7. Use simple practical language.
8. Do not expose FAISS, embeddings, similarity scores,
   chunks, prompts, or internal retrieval details.
9. Do not reproduce large sections of the policy.
10. Page references may be mentioned briefly when available.
"""


# ============================================================
# SYSTEM PROMPT BUILDER
# ============================================================

def build_system_prompt(
    department,
    language,
):

    if department == "NADRA":
        return NADRA_SYSTEM_PROMPT

    return GENERAL_SYSTEM_PROMPT


# ============================================================
# USER PROMPT BUILDER
# ============================================================

def build_user_prompt(
    question,
    department,
    evidence,
    language,
):

    if language == "اردو":
        language_instruction = "Answer in Urdu."

    else:
        language_instruction = "Answer in English."

    return f"""
Department:
{department}

User question:
{question}

Requested language:
{language_instruction}

Evidence:
{evidence}

Task:

Answer the user's question using ONLY the evidence provided
above.

Do not guess.

Do not add unsupported information.

If the evidence is insufficient, clearly say that the
information could not be verified.

{language_instruction}
"""
