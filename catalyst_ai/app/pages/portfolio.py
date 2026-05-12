from __future__ import annotations

import pandas as pd
import streamlit as st

from catalyst_ai.config import get_paths
from catalyst_ai.data.store import connect, read_df
from catalyst_ai.kpi.calc import study_kpi_snapshot


def render() -> None:
    st.header("Portfolio Overview")
    st.caption(f"Persona: {st.session_state.get('persona')}")

    paths = get_paths()
    con = connect(paths.db_path)
    try:
        studies = read_df(con, "SELECT * FROM studies ORDER BY study_id")
        weekly = read_df(con, "SELECT * FROM weekly_metrics")
        risks = read_df(con, "SELECT study_id, COUNT(*) as risk_count, MAX(score) as top_risk_score FROM risks GROUP BY study_id")
    finally:
        con.close()

    if studies.empty:
        st.warning("No data found. Run the data generator from the CLI.")
        return

    kpis = study_kpi_snapshot(weekly)
    view = studies.merge(kpis, on="study_id", how="left").merge(risks, on="study_id", how="left")
    view["risk_count"] = view["risk_count"].fillna(0).astype(int)
    view["top_risk_score"] = view["top_risk_score"].fillna(0.0)

    st.dataframe(
        view[[
            "study_id",
            "title",
            "phase",
            "status",
            "planned_enrollment",
            "enrollment_rate",
            "screen_failure_rate",
            "open_queries",
            "risk_count",
            "top_risk_score",
        ]],
        use_container_width=True,
    )

    selected = st.selectbox("Select a study", options=view["study_id"].tolist())
    st.session_state["selected_study_id"] = selected

    st.info("Go to Study Detail / Risk Register / Meeting Pack for the selected study.")
