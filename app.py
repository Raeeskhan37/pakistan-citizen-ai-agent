import streamlit as st

from agent.citizen_agent import ask_citizen_agent
from config.departments import DEPARTMENTS
from config.settings import APP_NAME, APP_VERSION


st.set_page_config(
    page_title=APP_NAME,
    page_icon="🇵🇰",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title("🇵🇰 Pakistan Citizen AI Agent")
st.subheader("پاکستان سٹیزن AI ایجنٹ")

st.write(
    "Government services information assistant for Pakistani citizens."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🏛️ Government Services")

    st.caption("Select a department")

    if "selected_department" not in st.session_state:
        st.session_state.selected_department = "NADRA"

    for department in DEPARTMENTS:

        if st.button(
            department,
            key=f"department_{department}",
            use_container_width=True,
        ):

            st.session_state.selected_department = department
            st.session_state.pop(
                "last_result",
                None,
            )

            st.rerun()

    st.divider()

    st.caption(
        f"Selected: "
        f"{st.session_state.selected_department}"
    )

    st.divider()

    st.caption(
        f"Version {APP_VERSION}"
    )


selected_department = (
    st.session_state.selected_department
)


# ============================================================
# RIGHT PANE
# ============================================================

st.markdown(
    f"## 🏛️ {selected_department} Citizen Assistant"
)


department_description = DEPARTMENTS[
    selected_department
][
    "description"
]


st.info(
    f"{department_description} "
    "Ask your question in English or Urdu. "
    "The agent will search official government sources."
)


# ============================================================
# LANGUAGE
# ============================================================

language = st.radio(
    "Answer language",
    ["English", "اردو"],
    horizontal=True,
)


# ============================================================
# QUESTION
# ============================================================

question = st.text_area(
    "Type your question:",
    height=150,
    placeholder=(
        "Example:\n"
        "What documents are required?\n\n"
        "یا\n"
        "اس سروس کے لیے کون سے دستاویزات درکار ہیں؟"
    ),
)


# ============================================================
# ASK AGENT
# ============================================================

if st.button(
    "🔍 Find Verified Answer",
    type="primary",
    use_container_width=True,
):

    if not question.strip():

        st.warning(
            "Please type your question first."
        )

    else:

        with st.spinner(
            f"{selected_department} Agent is "
            "researching official sources..."
        ):

            try:

                result = ask_citizen_agent(
                    question=question,
                    selected_department=selected_department,
                    language=language,
                )

                st.session_state.last_result = result

            except Exception as exc:

                st.error(
                    "The agent could not complete the request."
                )

                st.exception(exc)


# ============================================================
# DISPLAY ANSWER
# ============================================================

if "last_result" in st.session_state:

    result = st.session_state.last_result

    st.divider()

    st.markdown("### 💬 Answer")

    st.markdown(
        result.get("answer", ""),
        unsafe_allow_html=True,
    )

    st.markdown("### 🔗 Official Sources")

    sources = result.get(
        "sources",
        [],
    )

    if sources:

        for source in sources:

            title = source.get(
                "title",
                "Official Source",
            )

            url = source.get(
                "url",
                "",
            )

            if url:

                st.markdown(
                    f"- [{title}]({url})"
                )

    else:

        st.warning(
            "No authoritative source could be verified."
        )

    # --------------------------------------------------------
    # Research details
    # --------------------------------------------------------

    with st.expander(
        "🔎 Research details"
    ):

        st.write(
            "Department:",
            result.get(
                "department",
                "",
            ),
        )

        st.write(
            "Research attempts:",
            result.get(
                "research_attempts",
                0,
            ),
        )

        st.write(
            "Official sources found:",
            result.get(
                "official_source_count",
                0,
            ),
        )

        if result.get("warning"):

            st.warning(
                result["warning"]
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "The agent does not invent government information. "
    "If authoritative evidence cannot be verified, "
    "it will say so."
)

st.caption(
    "Developed by Raees Khan"
)
