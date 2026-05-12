from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from catalyst_ai.api.deps import get_con
from catalyst_ai.data.store import read_df
from catalyst_ai.kpi.calc import study_kpi_snapshot
from catalyst_ai.narrative.meeting_pack import generate_meeting_pack

router = APIRouter(prefix="/studies", tags=["meeting-pack"])


@router.post("/{study_id}/meeting-pack")
def build_meeting_pack(study_id: str, con=Depends(get_con)):
    studies = read_df(con, "SELECT * FROM studies WHERE study_id = ?", (study_id,))
    if studies.empty:
        return HTMLResponse("Study not found", status_code=404)

    weekly = read_df(con, "SELECT * FROM weekly_metrics WHERE study_id = ?", (study_id,))
    if weekly.empty:
        return HTMLResponse("No metrics", status_code=400)

    kpi = study_kpi_snapshot(weekly)
    kpi_row = kpi.to_dict(orient="records")[0]

    risks = read_df(con, "SELECT * FROM risks WHERE study_id = ? ORDER BY score DESC", (study_id,))
    risks_list = risks.to_dict(orient="records")

    pack = generate_meeting_pack(studies.to_dict(orient="records")[0], kpi_row, risks_list)
    return HTMLResponse(pack.html)
