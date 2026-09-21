import streamlit as st

from agent.citizen_agent import ask_citizen_agent
from config.departments import DEPARTMENTS
from config.settings import APP_NAME, APP_VERSION


st.set_page_config(
    page_title=APP_NAME,
    page_icon="🇵🇰",
    layout="wide",
)


st.title("🇵🇰 Pakistan Citizen AI Agent")
st.subheader("پاکستان سٹیزن AI ایجنٹ")

st.write(
    "Government services information assistant for Pakistani citizens."
)

st.info(
    "The agent searches current online information and prioritizes "
    "official government sources. Always verify important matters "
    "with the relevant government department."
)


with st.sidebar:

    st.header("🔎 Citizen Assistant")

    language = st.radio(
        "Answer language",
        ["English", "اردو"],
    )

    department_names = [
        "Automatic"
    ] + list(DEPARTMENTS.keys())

    selected_department = st.selectbox(
        "Department / Service",
        department_names,
    )

    st.divider()

    st.markdown("### Departments")

    for department in DEPARTMENTS:

        st.write(
            f"• {department}"
        )

    st.divider()

    st.caption(
        f"Version {APP_VERSION}"
    )


st.markdown(
    "### Ask your question"
)

question = st.text_area(
    "Describe your problem or question:",
    height=140,
    placeholder=(
        "Example:\n"
        "How can I renew my CNIC?\n\n"
        "یا\n"
        "میرا CNIC expire ہو گیا ہے، میں اسے کیسے renew کر سکتا ہوں؟"
    ),
)


if st.button(
    "🔍 Find Verified Answer",
    type="primary",
):

    if not question.strip():

        st.warning(
            "Please enter your question first."
        )

    else:

        with st.spinner(
            "Searching current information and verifying sources..."
        ):

            try:

                result = ask_citizen_agent(
                    question=question,
                    selected_department=selected_department,
                    language=language,
                )

                st.markdown(
                    "### 🏛️ Department"
                )

                st.write(
                    result["department"]
                )

                st.markdown(
                    "### 💬 Answer"
                )

                st.markdown(
                    result["answer"]
                )

                st.markdown(
                    "### 🔗 Sources"
                )

                sources = result.get(
                    "sources",
                    [],
                )

                if sources:

                    for source in sources:

                        title = source.get(
                            "title",
                            "Source",
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
                        "No verified source links were returned."
                    )

                with st.expander(
                    "ℹ️ Search and verification details"
                ):

                    st.write(
                        f"Sources reviewed: "
                        f"{result.get('source_count', 0)}"
                    )

                    st.write(
                        f"Official sources found: "
                        f"{result.get('official_source_count', 0)}"
                    )

                    st.write(
                        f"Information checked: "
                        f"{result.get('checked_date', '')}"
                    )

                    if result.get("warning"):

                        st.warning(
                            result["warning"]
                        )

            except Exception as exc:

                st.error(
                    "The agent could not complete the request."
                )

                st.exception(exc)


st.divider()

st.caption(
    "Pakistan Citizen AI Agent • "
    "Always confirm critical information with the "
    "relevant official government authority."
)

st.caption(
    "Developed by Raees Khan"
)
