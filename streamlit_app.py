import streamlit as st

from catalyst_ai.app.pages import (
    actions_decisions,
    meeting_pack,
    portfolio,
    risk_register,
    study_detail,
)
from catalyst_ai.app.state import init_session_state


def main() -> None:
    st.set_page_config(page_title="Catalyst.AI", page_icon="🧪", layout="wide")
    init_session_state()

    st.sidebar.title("Catalyst.AI")
    persona = st.sidebar.selectbox(
        "Persona",
        options=["Study Lead", "Clinical Ops", "Data Management", "Vendor Manager", "Executive"],
        index=0,
    )
    st.session_state["persona"] = persona

    page = st.sidebar.radio(
        "Navigate",
        options=[
            "Portfolio Overview",
            "Study Detail",
            "Risk Register",
            "Meeting Pack Generator",
            "Actions & Decisions",
            "Artifacts (Requirements/Design/Sprint/CI/CD)",
        ],
        index=0,
    )

    if page == "Portfolio Overview":
        portfolio.render()
    elif page == "Study Detail":
        study_detail.render()
    elif page == "Risk Register":
        risk_register.render()
    elif page == "Meeting Pack Generator":
        meeting_pack.render()
    elif page == "Actions & Decisions":
        actions_decisions.render()
    else:
        from catalyst_ai.app.pages import artifacts

        artifacts.render()


if __name__ == "__main__":
    main()
