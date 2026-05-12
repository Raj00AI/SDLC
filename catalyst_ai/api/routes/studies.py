from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from catalyst_ai.api.deps import get_con
from catalyst_ai.data.store import read_df
from catalyst_ai.kpi.calc import study_kpi_snapshot
from catalyst_ai.risk.engine import recompute_risks_for_study

router = APIRouter(prefix="/studies", tags=["studies"])


@router.get("")
def list_studies(con=Depends(get_con)):
    studies = read_df(con, "SELECT * FROM studies ORDER BY study_id")
    weekly = read_df(con, "SELECT * FROM weekly_metrics")
    kpis = study_kpi_snapshot(weekly)
    out = studies.merge(kpis, on="study_id", how="left")
    return json.loads(out.to_json(orient="records", date_format="iso"))


@router.get("/{study_id}")
def get_study(study_id: str, con=Depends(get_con)):
    df = read_df(con, "SELECT * FROM studies WHERE study_id = ?", (study_id,))
    if df.empty:
        return None
    return json.loads(df.to_json(orient="records", date_format="iso"))[0]


@router.get("/{study_id}/metrics")
def get_metrics(study_id: str, con=Depends(get_con)):
    weekly = read_df(
        con,
        "SELECT * FROM weekly_metrics WHERE study_id = ? ORDER BY week_start",
        (study_id,),
    )
    return json.loads(weekly.to_json(orient="records", date_format="iso"))


@router.post("/{study_id}/risks/recompute")
def recompute_risks(study_id: str, con=Depends(get_con)):
    risks = recompute_risks_for_study(con, study_id)
    return {
        "study_id": study_id,
        "recomputed_at": datetime.now(timezone.utc).isoformat(),
        "count": len(risks),
        "risks": risks,
    }


@router.get("/{study_id}/risks")
def list_risks(study_id: str, con=Depends(get_con)):
    df = read_df(con, "SELECT * FROM risks WHERE study_id = ? ORDER BY score DESC", (study_id,))
    return json.loads(df.to_json(orient="records", date_format="iso"))
