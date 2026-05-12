from __future__ import annotations

import datetime as dt

import streamlit as st

from catalyst_ai.config import get_paths
from catalyst_ai.data.store import connect, read_df


def render() -> None:
    st.header("Actions & Decisions")
    study_id = st.session_state.get("selected_study_id")
    if not study_id:
        st.warning("Select a study from Portfolio Overview first.")
        return

    paths = get_paths()

    con = connect(paths.db_path)
    try:
        risks = read_df(con, "SELECT risk_id, title FROM risks WHERE study_id = ? ORDER BY score DESC", (study_id,))
        actions = read_df(con, "SELECT * FROM actions WHERE study_id = ? ORDER BY due_date", (study_id,))
    finally:
        con.close()

    st.subheader("Create action")
    with st.form("create_action"):
        title = st.text_input("Title")
        owner = st.text_input("Owner", value="Study Lead")
        due = st.date_input("Due date", value=dt.date.today() + dt.timedelta(days=14))
        linked = st.selectbox(
            "Link to risk (optional)",
            options=[None] + (risks["risk_id"].tolist() if not risks.empty else []),
            format_func=lambda x: "(none)" if x is None else f"{x} — {risks.set_index('risk_id').loc[x,'title']}",
        )
        status = st.selectbox("Status", options=["Open", "In Progress", "Done"], index=0)
        submitted = st.form_submit_button("Add")

    if submitted:
        con = connect(paths.db_path)
        try:
            con.execute(
                """
                INSERT INTO actions(action_id, study_id, linked_risk_id, title, owner, due_date, status, created_by, created_at)
                VALUES (uuid(), ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    study_id,
                    linked,
                    title,
                    owner,
                    str(due),
                    status,
                    "demo-user",
                    dt.datetime.utcnow().isoformat(),
                ),
            )
        finally:
            con.close()
        st.success("Created")
        st.rerun()

    st.subheader("Open actions")
    st.dataframe(actions, use_container_width=True)

    st.subheader("Traceability")
    st.markdown("Actions can be linked to a `risk_id` and store `created_by/created_at` for audit.")
