from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from catalyst_ai.api.deps import get_con
from catalyst_ai.data.store import read_df

router = APIRouter(prefix="/actions", tags=["actions"])


class ActionCreate(BaseModel):
    study_id: str
    linked_risk_id: str | None = None
    title: str
    owner: str
    due_date: str  # ISO date
    status: str = "Open"
    created_by: str = "demo-user"


@router.get("")
def list_actions(study_id: str | None = None, con=Depends(get_con)):
    if study_id:
        df = read_df(con, "SELECT * FROM actions WHERE study_id = ? ORDER BY due_date", (study_id,))
    else:
        df = read_df(con, "SELECT * FROM actions ORDER BY due_date")
    return json.loads(df.to_json(orient="records", date_format="iso"))


@router.post("")
def create_action(payload: ActionCreate, con=Depends(get_con)):
    action_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    con.execute(
        """
        INSERT INTO actions(action_id, study_id, linked_risk_id, title, owner, due_date, status, created_by, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            action_id,
            payload.study_id,
            payload.linked_risk_id,
            payload.title,
            payload.owner,
            payload.due_date,
            payload.status,
            payload.created_by,
            created_at,
        ),
    )
    df = read_df(con, "SELECT * FROM actions WHERE action_id = ?", (action_id,))
    return json.loads(df.to_json(orient="records", date_format="iso"))[0]
