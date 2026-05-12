from __future__ import annotations

import streamlit as st


def init_session_state() -> None:
    st.session_state.setdefault("persona", "Study Lead")
    st.session_state.setdefault("selected_study_id", None)
