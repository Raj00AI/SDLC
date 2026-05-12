from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import pandas as pd
from jinja2 import Template


@dataclass(frozen=True)
class MeetingPack:
    html: str
    context: dict


_HTML_TEMPLATE = Template(
    """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Meeting Pack - {{ study_id }}</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; }
    .kpi { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .card { border: 1px solid #ddd; border-radius: 8px; padding: 12px; }
    .muted { color: #666; }
    code { background: #f5f5f5; padding: 2px 4px; }
  </style>
</head>
<body>
  <h1>Catalyst.AI - Meeting Pack</h1>
  <h2>{{ title }} ({{ study_id }})</h2>
  <p class="muted">Generated at {{ generated_at }} | Latest week {{ week_start }}</p>

  <h3>Agenda</h3>
  <ol>
    <li>Portfolio/study status</li>
    <li>Recruitment & enrollment</li>
    <li>Site activation & performance</li>
    <li>Data quality & queries</li>
    <li>Key risks & mitigations</li>
    <li>Decisions needed</li>
    <li>Actions & owners</li>
  </ol>

  <h3>Executive Summary</h3>
  <div class="card">
    <p>{{ executive_summary }}</p>
    <p><b>Traceability:</b> This paragraph is driven by KPIs: <code>enrollment_rate</code>, <code>screen_failure_rate</code>, <code>open_queries</code> computed from table <code>weekly_metrics</code> filtered to <code>study_id={{ study_id }}</code> and the latest <code>week_start={{ week_start }}</code>.</p>
  </div>

  <h3>KPIs (latest snapshot)</h3>
  <div class="kpi">
    {% for k, v in kpis.items() %}
      <div class="card"><b>{{ k }}</b><br/>{{ v }}</div>
    {% endfor %}
  </div>

  <h3>Top Risks</h3>
  {% if risks|length == 0 %}
    <p>No open risks triggered by rules.</p>
  {% else %}
    {% for r in risks %}
      <div class="card">
        <b>{{ r.title }}</b> ({{ r.severity }}) - score {{ '%.1f'|format(r.score) }}
        <ul>
          {% for d in r.drivers %}<li>{{ d }}</li>{% endfor %}
        </ul>
        <p><b>Recommendation:</b> {{ r.recommendation }}</p>
        <p class="muted"><b>Traceability:</b> Evidence: {{ r.evidence }}</p>
      </div>
    {% endfor %}
  {% endif %}

  <h3>Decisions Needed (template)</h3>
  <ul>
    <li>Approve revised recruitment targets and mitigation plan?</li>
    <li>Agree DM query closure SLA and escalation path?</li>
    <li>Confirm vendor stabilization plan and KPIs?</li>
  </ul>
</body>
</html>
"""
)


def build_executive_summary(kpi_row: dict, risks: list[dict]) -> str:
    enr = kpi_row.get("enrollment_rate", 0.0)
    sfr = kpi_row.get("screen_failure_rate", 0.0)
    oq = kpi_row.get("open_queries", 0)

    risk_phrase = "No high-priority risks detected by rules." if len(risks) == 0 else f"{len(risks)} risks flagged for review."

    return (
        f"Latest week shows enrollment at {enr:.0%} vs plan, screen failure at {sfr:.0%}, and {oq} open queries. "
        f"{risk_phrase} Focus discussion on the drivers below and confirm mitigations + owners."
    )


def generate_meeting_pack(
    study_row: dict,
    kpi_row: dict,
    risks: list[dict],
) -> MeetingPack:
    ctx = {
        "study_id": study_row["study_id"],
        "title": study_row.get("title", ""),
        "week_start": str(kpi_row.get("week_start", "")),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "kpis": {
            "Planned enrolled (cum)": int(kpi_row.get("planned_enrolled_cum", 0)),
            "Actual enrolled (cum)": int(kpi_row.get("actual_enrolled_cum", 0)),
            "Enrollment rate": f"{float(kpi_row.get('enrollment_rate', 0.0)):.0%}",
            "Screen failure rate": f"{float(kpi_row.get('screen_failure_rate', 0.0)):.0%}",
            "Open queries": int(kpi_row.get("open_queries", 0)),
            "Protocol deviations": int(kpi_row.get("protocol_deviations", 0)),
            "Vendor tickets": int(kpi_row.get("vendor_tickets", 0)),
        },
        "risks": risks,
    }
    ctx["executive_summary"] = build_executive_summary(kpi_row, risks)
    return MeetingPack(html=_HTML_TEMPLATE.render(**ctx), context=ctx)
