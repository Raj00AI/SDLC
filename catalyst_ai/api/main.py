from __future__ import annotations

from fastapi import FastAPI

from catalyst_ai.api.routes import actions, meeting_pack, studies

app = FastAPI(title="Catalyst.AI API", version="0.1.0")

app.include_router(studies.router)
app.include_router(meeting_pack.router)
app.include_router(actions.router)
