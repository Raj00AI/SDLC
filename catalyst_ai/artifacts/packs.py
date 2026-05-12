from __future__ import annotations

from pathlib import Path


def requirements_pack() -> str:
    return r"""
# Requirements Pack — Catalyst.AI (Prototype)

## Epics
1. **Portfolio oversight**: list studies, status, and top risks.
2. **Study drill-down**: KPI trends, site performance, milestones.
3. **Risk register**: ranked risks with evidence + mitigations.
4. **Meeting pack generation**: one-click narrative, agenda, KPIs, traceability.
5. **Actions & decisions**: create/assign/track actions linked to risks.
6. **Quality & traceability**: audit trail, metric definitions, test coverage.

## User Stories (sample)
- As a Study Lead, I can generate a meeting pack in ≤60 seconds so that governance packs are consistent and traceable.
- As Clinical Ops, I can see site activation lag and identify late sites.
- As Data Management, I can track query backlog and trending.
- As Vendor Manager, I can monitor vendor ticket spikes.
- As Executive, I can see cross-study top risks and statuses.

## Acceptance Criteria (demo-ready)
- Portfolio loads ≤5 seconds on sample dataset.
- Meeting pack generated ≤60 seconds.
- At least 5 risk rules implemented (slow enrollment, high screen failure, delayed activation*, query backlog, milestone slippage*).
- Actions include owner + due date + status.
- Every risk and narrative paragraph includes KPI + underlying data slice used.

*Note: activation + milestone slippage are included as schema; rules can be extended.

## KPI Dictionary (core)
- **Enrollment rate** = actual_enrolled_cum / planned_enrolled_cum (latest week)
- **Screen failure %** = screen_fail_cum / screened_cum
- **Query backlog** = open_queries (latest week)
- **Activation lag** = actual_activation_date - planned_activation_date (days)
- **Milestone slippage** = actual_date - planned_date (days)

## Assumptions Log
- No patient-level data; all data is synthetic/public.
- KPI thresholds are illustrative and adjustable.
- Single-user demo (no auth); audit trail stored locally.

## Traceability Matrix (starter)
| Story | Design | Code | Tests |
|---|---|---|---|
| Meeting pack ≤60s | Narrative service | `catalyst_ai/narrative/meeting_pack.py` | `tests/test_narrative.py` |
| Slow enrollment rule | Risk rules catalog | `catalyst_ai/risk/rules.py::slow_enrollment` | `tests/test_risk_rules.py` |
| KPI calc | KPI module | `catalyst_ai/kpi/calc.py` | `tests/test_kpis.py` |
""".strip()


def design_pack() -> str:
    return r"""
# Design Pack — Catalyst.AI (Prototype)

## Solution Design Diagram (graphical)

> This is a self-contained SVG (no external rendering required). You can copy this diagram into any Markdown viewer that supports inline SVG.

<svg width="980" height="520" viewBox="0 0 980 520" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .box { fill:#ffffff; stroke:#2b2b2b; stroke-width:1.2; rx:10; }
      .title { font: 700 14px Arial, sans-serif; fill:#111; }
      .text { font: 12px Arial, sans-serif; fill:#222; }
      .muted { font: 12px Arial, sans-serif; fill:#555; }
      .hdr { fill:#f3f6ff; stroke:#2b2b2b; stroke-width:1.2; rx:10; }
      .arrow { stroke:#1f4fff; stroke-width:2; fill:none; marker-end:url(#arrowHead); }
      .arrow2 { stroke:#444; stroke-width:1.6; fill:none; marker-end:url(#arrowHeadGray); }
      .pill { fill:#eef7ff; stroke:#1f4fff; stroke-width:1; rx:14; }
    </style>
    <marker id="arrowHead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#1f4fff" />
    </marker>
    <marker id="arrowHeadGray" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#444" />
    </marker>
  </defs>

  <!-- Title pill -->
  <rect x="22" y="16" width="360" height="34" class="pill"/>
  <text x="38" y="38" class="title">Catalyst.AI — Logical Solution Design</text>

  <!-- UI block -->
  <rect x="24" y="80" width="260" height="360" class="hdr"/>
  <text x="40" y="110" class="title">Streamlit UI</text>
  <text x="40" y="140" class="text">• Portfolio Overview</text>
  <text x="40" y="162" class="text">• Study Detail</text>
  <text x="40" y="184" class="text">• Risk Register</text>
  <text x="40" y="206" class="text">• Meeting Pack Generator</text>
  <text x="40" y="228" class="text">• Actions & Decisions</text>
  <text x="40" y="250" class="text">• Artifacts Generator</text>
  <text x="40" y="284" class="muted">Persona filter: Study Lead / Ops / DM / Vendor / Exec</text>

  <!-- API block -->
  <rect x="320" y="80" width="300" height="170" class="hdr"/>
  <text x="336" y="110" class="title">FastAPI (optional API layer)</text>
  <text x="336" y="140" class="text">GET /studies</text>
  <text x="336" y="162" class="text">GET /studies/{id}/metrics</text>
  <text x="336" y="184" class="text">POST /studies/{id}/risks/recompute</text>
  <text x="336" y="206" class="text">POST /studies/{id}/meeting-pack</text>
  <text x="336" y="228" class="text">GET/POST /actions</text>

  <!-- Services block -->
  <rect x="320" y="270" width="300" height="170" class="hdr"/>
  <text x="336" y="300" class="title">Core Services (Python modules)</text>
  <text x="336" y="330" class="text">KPI Calculator  → catalyst_ai.kpi</text>
  <text x="336" y="352" class="text">Risk Engine     → catalyst_ai.risk</text>
  <text x="336" y="374" class="text">Narratives      → catalyst_ai.narrative</text>
  <text x="336" y="396" class="text">SDLC Packs      → catalyst_ai.artifacts</text>
  <text x="336" y="426" class="muted">Explainability rule: every insight/risk includes KPI + data slice</text>

  <!-- Store block -->
  <rect x="662" y="80" width="294" height="360" class="hdr"/>
  <text x="678" y="110" class="title">Local Analytics Store</text>
  <text x="678" y="132" class="muted">DuckDB file: .data/catalyst.duckdb</text>

  <rect x="678" y="156" width="260" height="34" class="box"/>
  <text x="694" y="178" class="text">studies</text>

  <rect x="678" y="202" width="260" height="34" class="box"/>
  <text x="694" y="224" class="text">sites</text>

  <rect x="678" y="248" width="260" height="34" class="box"/>
  <text x="694" y="270" class="text">weekly_metrics</text>

  <rect x="678" y="294" width="260" height="34" class="box"/>
  <text x="694" y="316" class="text">milestones</text>

  <rect x="678" y="340" width="260" height="34" class="box"/>
  <text x="694" y="362" class="text">risks</text>

  <rect x="678" y="386" width="260" height="34" class="box"/>
  <text x="694" y="408" class="text">actions</text>

  <!-- Artifacts output -->
  <rect x="662" y="452" width="294" height="48" class="box"/>
  <text x="678" y="480" class="text">Artifacts output: .artifacts/*.md + meeting-pack-*.html</text>

  <!-- Arrows -->
  <path d="M 284 150 C 300 150, 304 150, 320 150" class="arrow"/>
  <text x="286" y="138" class="muted">optional HTTP</text>

  <path d="M 284 330 C 300 330, 304 330, 320 330" class="arrow2"/>
  <text x="286" y="318" class="muted">direct calls</text>

  <path d="M 620 170 C 640 170, 646 170, 662 170" class="arrow"/>
  <path d="M 620 360 C 640 360, 646 360, 662 360" class="arrow"/>

  <path d="M 500 440 C 560 470, 610 470, 662 476" class="arrow2"/>
</svg>

## Target Architecture
- **UI**: Streamlit single app with role persona filter.
- **API**: FastAPI for data + risk + meeting pack endpoints.
- **Store**: DuckDB local file (tables: studies, sites, weekly_metrics, milestones, risks, actions).
- **Services**:
  - KPI calculation module
  - Rule-based risk engine (5+ rules)
  - Narrative generator (HTML meeting pack with traceability)

## Data Model (minimal)
- `studies(study_id, title, phase, status, condition, planned_enrollment, start_date)`
- `sites(site_id, study_id, country, investigator, planned_activation_date, actual_activation_date)`
- `weekly_metrics(study_id, site_id, week_start, planned_enrolled_cum, actual_enrolled_cum, screened_cum, screen_fail_cum, open_queries, protocol_deviations, vendor_tickets)`
- `milestones(study_id, name, planned_date, actual_date)`
- `risks(risk_id, study_id, rule_id, title, severity, score, drivers, recommendation, evidence, created_at)`
- `actions(action_id, study_id, linked_risk_id, title, owner, due_date, status, created_by, created_at)`

## API Contract (v0)
- `GET /studies`
- `GET /studies/{study_id}`
- `GET /studies/{study_id}/metrics`
- `POST /studies/{study_id}/risks/recompute`
- `GET /studies/{study_id}/risks`
- `POST /studies/{study_id}/meeting-pack` -> returns HTML
- `GET /actions?study_id=`
- `POST /actions` (create)

## Risk Rules Catalog (implemented)
- Slow enrollment vs plan
- High screen failure rate
- Query backlog
- Vendor ticket spike
- Protocol deviation spike

## NFRs (demo)
- Portfolio load ≤5s (local store, small dataset)
- Meeting pack generation ≤60s
- Explainability: evidence includes KPI + data slice pointers
""".strip()


def sprint_plan_pack() -> str:
    return r"""
# Sprint Plan — Catalyst.AI (2–3 sprints)

## Sprint Timeline (graphical)

<svg width="980" height="260" viewBox="0 0 980 260" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .t { font: 700 14px Arial, sans-serif; fill:#111; }
      .s { font: 12px Arial, sans-serif; fill:#222; }
      .m { font: 12px Arial, sans-serif; fill:#555; }
      .lane { fill:#ffffff; stroke:#2b2b2b; stroke-width:1.2; rx:12; }
      .hdr { fill:#f3f6ff; stroke:#2b2b2b; stroke-width:1.2; rx:12; }
      .bar1 { fill:#e8f4ff; stroke:#1f4fff; stroke-width:1.4; rx:10; }
      .bar2 { fill:#eafff1; stroke:#1b7f3a; stroke-width:1.4; rx:10; }
      .bar3 { fill:#fff4e8; stroke:#b85a00; stroke-width:1.4; rx:10; }
      .milestone { fill:#111; }
    </style>
  </defs>

  <rect x="20" y="18" width="940" height="40" class="hdr"/>
  <text x="36" y="44" class="t">2–3 Sprint Plan (demo milestones highlighted)</text>

  <!-- axis -->
  <text x="36" y="80" class="m">Week</text>
  <line x1="80" y1="76" x2="940" y2="76" stroke="#2b2b2b" stroke-width="1"/>
  <text x="82" y="96" class="m">1</text>
  <text x="200" y="96" class="m">2</text>
  <text x="318" y="96" class="m">3</text>
  <text x="436" y="96" class="m">4</text>
  <text x="554" y="96" class="m">5</text>
  <text x="672" y="96" class="m">6</text>

  <!-- sprint bars -->
  <rect x="80" y="108" width="240" height="44" class="bar1"/>
  <text x="92" y="134" class="t">Sprint 1</text>
  <text x="92" y="150" class="s">Data + KPIs + Tests</text>

  <rect x="328" y="108" width="240" height="44" class="bar2"/>
  <text x="340" y="134" class="t">Sprint 2</text>
  <text x="340" y="150" class="s">UI + Risks + Meeting Pack</text>

  <rect x="576" y="108" width="240" height="44" class="bar3"/>
  <text x="588" y="134" class="t">Sprint 3</text>
  <text x="588" y="150" class="s">Actions + CI/CD + Hardening</text>

  <!-- milestones markers -->
  <circle cx="320" cy="170" r="5" class="milestone"/>
  <text x="330" y="174" class="m">Demo 1: Portfolio w/ KPI snapshot</text>

  <circle cx="568" cy="192" r="5" class="milestone"/>
  <text x="578" y="196" class="m">Demo 2: Meeting pack generated</text>

  <circle cx="816" cy="214" r="5" class="milestone"/>
  <text x="826" y="218" class="m">Demo 3: Traceability insight → risk → action</text>

  <!-- footer -->
  <text x="36" y="242" class="m">Note: timeline is illustrative; each sprint can be 1–2 weeks based on team capacity.</text>
</svg>

## Sprint 1 — Data + KPIs
- Synthetic data generator + DuckDB schema
- Ingestion CLI
- KPI snapshot + trend endpoints
- Unit tests for KPI calculations
- Demo checkpoint: load portfolio list with KPI snapshot

## Sprint 2 — UI + Risks + Meeting Pack
- Streamlit pages for Portfolio/Study/Risks/Meeting Pack
- Risk rule engine + recompute
- Meeting pack HTML generator + download
- Integration tests for API endpoints
- Demo checkpoint: generate meeting pack from selected study

## Sprint 3 — Actions + Hardening + CI/CD
- Actions CRUD and linkage to risks
- Audit trail (created_by/created_at)
- CI pipeline + Docker Compose
- UI smoke tests
- Demo checkpoint: full traceability from insight->risk->action
""".strip()


def cicd_pack() -> str:
    return """
# CI/CD Integration (prototype)

## GitHub Actions
- Lint (ruff) + format check (black)
- Unit tests (pytest)

## Jenkins (optional)
- Example `Jenkinsfile` provided for pipeline parity.

## Artifacts
- Publish `.artifacts/` and test reports.
""".strip()


def demo_script_pack() -> str:
    return """
# Deployment & Demo Script (10–15 minutes)

1. Show generated artifacts (Requirements/Design/Sprint).
2. Run tests (CI view).
3. Start app (Streamlit) and (optional) API.
4. Portfolio Overview: highlight a study with top risks.
5. Study Detail: review KPI trends and evidence.
6. Risk Register: open risk details and traceability.
7. Meeting Pack: generate and download HTML.
8. Actions: create an action linked to a risk; show owner + due date.
9. Close: explain how traceability supports decisions and mitigations.
""".strip()
