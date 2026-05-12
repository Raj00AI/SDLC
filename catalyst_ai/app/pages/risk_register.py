from __future__ import annotations

import json
import streamlit as st

from catalyst_ai.config import get_paths
from catalyst_ai.data.store import connect, read_df
from catalyst_ai.risk.engine import recompute_risks_for_study


def render() -> None:
    st.header("Risk Register")
    study_id = st.session_state.get("selected_study_id")
    if not study_id:
        st.warning("Select a study from Portfolio Overview first.")
        return

    paths = get_paths()

    if st.button("Recompute risks"):
        con = connect(paths.db_path)
        try:
            recompute_risks_for_study(con, study_id)
        finally:
            con.close()
        st.success("Recomputed")

    con = connect(paths.db_path)
    try:
        risks = read_df(con, "SELECT * FROM risks WHERE study_id = ? ORDER BY score DESC", (study_id,))
    finally:
        con.close()

    st.subheader(f"Study: {study_id}")
    if risks.empty:
        st.info("No risks triggered.")
        return

    st.dataframe(risks[["rule_id", "title", "severity", "score", "drivers", "recommendation", "created_at"]], use_container_width=True)

    idx = st.selectbox("Inspect a risk", options=list(range(len(risks))))
    r = risks.iloc[int(idx)].to_dict()

    st.markdown("### Evidence / Traceability")
    try:
        ev = json.loads(r["evidence"]) if isinstance(r["evidence"], str) else r["evidence"]
    except Exception:
        ev = r["evidence"]

    st.json(ev)
