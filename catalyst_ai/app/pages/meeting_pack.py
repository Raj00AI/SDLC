from __future__ import annotations

from pathlib import Path

import streamlit as st

from catalyst_ai.config import get_paths
from catalyst_ai.data.store import connect, read_df
from catalyst_ai.kpi.calc import study_kpi_snapshot
from catalyst_ai.narrative.meeting_pack import generate_meeting_pack


def render() -> None:
    st.header("Meeting Pack Generator")
    study_id = st.session_state.get("selected_study_id")
    if not study_id:
        st.warning("Select a study from Portfolio Overview first.")
        return

    paths = get_paths()
    con = connect(paths.db_path)
    try:
        study = read_df(con, "SELECT * FROM studies WHERE study_id = ?", (study_id,))
        weekly = read_df(con, "SELECT * FROM weekly_metrics WHERE study_id = ?", (study_id,))
        risks = read_df(con, "SELECT * FROM risks WHERE study_id = ? ORDER BY score DESC", (study_id,))
    finally:
        con.close()

    if weekly.empty or study.empty:
        st.warning("Missing data for selected study")
        return

    kpi = study_kpi_snapshot(weekly)
    kpi_row = kpi.to_dict(orient="records")[0]

    risks_list = risks.to_dict(orient="records")

    if st.button("Generate meeting pack"):
        pack = generate_meeting_pack(study.to_dict(orient="records")[0], kpi_row, risks_list)
        html = pack.html
        out_path = paths.artifacts_dir / f"meeting-pack-{study_id}.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")

        st.success(f"Generated: {out_path}")
        st.download_button(
            "Download meeting pack (HTML)",
            data=html,
            file_name=f"meeting-pack-{study_id}.html",
            mime="text/html",
        )

        st.markdown("### Preview")
        st.components.v1.html(html, height=600, scrolling=True)

    st.markdown("### Traceability")
    st.write(
        {
            "narrative_inputs": {
                "study": "studies",
                "kpis": "weekly_metrics latest week",
                "risks": "risks computed from rule engine",
            }
        }
    )
