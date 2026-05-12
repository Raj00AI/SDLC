from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import uuid4

import pandas as pd

from catalyst_ai.data.store import read_df
from catalyst_ai.risk.rules import ALL_RULES


def recompute_risks_for_study(con, study_id: str) -> list[dict]:
    weekly = read_df(
        con,
        "SELECT * FROM weekly_metrics WHERE study_id = ? ORDER BY week_start",
        (study_id,),
    )
    if weekly.empty:
        return []

    latest = weekly.sort_values("week_start").tail(1).iloc[0]

    # delete existing
    con.execute("DELETE FROM risks WHERE study_id = ?", (study_id,))

    results = []
    for rule in ALL_RULES:
        out = rule(latest)
        if out is None:
            continue
        risk_id = str(uuid4())
        created_at = datetime.now(timezone.utc).isoformat()
        con.execute(
            """
            INSERT INTO risks(risk_id, study_id, rule_id, title, severity, score, drivers, recommendation, evidence, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                risk_id,
                study_id,
                out.rule_id,
                out.title,
                out.severity,
                float(out.score),
                "|".join(out.drivers),
                out.recommendation,
                json.dumps(out.evidence),
                created_at,
            ),
        )
        results.append(
            {
                "risk_id": risk_id,
                "study_id": study_id,
                "rule_id": out.rule_id,
                "title": out.title,
                "severity": out.severity,
                "score": float(out.score),
                "drivers": out.drivers,
                "recommendation": out.recommendation,
                "evidence": out.evidence,
                "created_at": created_at,
            }
        )

    return sorted(results, key=lambda r: r["score"], reverse=True)
