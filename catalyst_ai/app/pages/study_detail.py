from __future__ import annotations

import pandas as pd
import streamlit as st

from catalyst_ai.config import get_paths
from catalyst_ai.data.store import connect, read_df


def render() -> None:
    st.header("Study Detail")
    study_id = st.session_state.get("selected_study_id")
    if not study_id:
        st.warning("Select a study from Portfolio Overview first.")
        return

    paths = get_paths()
    con = connect(paths.db_path)
    try:
        study = read_df(con, "SELECT * FROM studies WHERE study_id = ?", (study_id,))
        weekly = read_df(con, "SELECT * FROM weekly_metrics WHERE study_id = ? ORDER BY week_start", (study_id,))
        sites = read_df(con, "SELECT * FROM sites WHERE study_id = ? ORDER BY site_id", (study_id,))
        milestones = read_df(con, "SELECT * FROM milestones WHERE study_id = ? ORDER BY planned_date", (study_id,))
    finally:
        con.close()

    st.subheader(f"{study_id} — {study.iloc[0]['title'] if not study.empty else ''}")

    if weekly.empty:
        st.warning("No weekly metrics found")
        return

    # KPI trends
    weekly = weekly.copy()
    weekly["enrollment_rate"] = weekly["actual_enrolled_cum"] / weekly["planned_enrolled_cum"].replace({0: pd.NA})
    weekly["screen_failure_rate"] = weekly["screen_fail_cum"] / weekly["screened_cum"].replace({0: pd.NA})

    c1, c2, c3 = st.columns(3)
    with c1:
        st.line_chart(weekly.set_index("week_start")["enrollment_rate"])
    with c2:
        st.line_chart(weekly.set_index("week_start")["screen_failure_rate"])
    with c3:
        st.line_chart(weekly.set_index("week_start")["open_queries"])

    st.subheader("Sites")
    st.dataframe(sites, use_container_width=True)

    st.subheader("Milestones")
    st.dataframe(milestones, use_container_width=True)

    st.subheader("Traceability")
    st.markdown(
        """
Each chart is computed from `weekly_metrics` filtered by `study_id`.
KPIs used in narratives and risks are computed from the **latest** `week_start`.
"""
    )
