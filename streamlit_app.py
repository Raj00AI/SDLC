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
    st.set_page_config(
        page_title="Cognizant® Domain-Specific Development Lifecycle Transformation (Catalyst.AI Edition)",
        page_icon="🧪",
        layout="wide",
    )
    init_session_state()

    st.sidebar.markdown(
        """
        <div style='font-size:14px; font-family: Arial, sans-serif; margin-bottom: 10px;'>
            <b>Cognizant® Domain-Specific Development Lifecycle Transformation (Catalyst.AI Edition)</b><br>
            <span style='font-size:12px; color:gray;'>Previously: <i>Engineering Companion</i></span>
        </div>
        """,
        unsafe_allow_html=True
    )

    persona = st.sidebar.selectbox(
        "Select SDLC Persona",
        options=[
            "Business Analyst",
            "Developer",
            "Tester",
            "Project Manager",
            "Architect",
        ],
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
            "SDLC Agents",
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
    elif page == "SDLC Agents":
        from catalyst_ai.app.pages.artifacts import render_sdlc_agents
        render_sdlc_agents()


if __name__ == "__main__":
    main()
