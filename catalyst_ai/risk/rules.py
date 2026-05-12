from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import pandas as pd

from catalyst_ai.kpi.calc import enrollment_rate, screen_failure_rate


@dataclass(frozen=True)
class RiskRuleResult:
    rule_id: str
    title: str
    severity: str
    score: float
    drivers: list[str]
    recommendation: str
    evidence: dict


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slow_enrollment(weekly_metrics_latest: pd.Series) -> RiskRuleResult | None:
    rate = enrollment_rate(int(weekly_metrics_latest.actual_enrolled_cum), int(weekly_metrics_latest.planned_enrolled_cum))
    if rate >= 0.85:
        return None
    score = float((0.85 - rate) * 100)
    return RiskRuleResult(
        rule_id="RISK_SLOW_ENROLL",
        title="Slow enrollment vs plan",
        severity="High" if rate < 0.7 else "Medium",
        score=score,
        drivers=[f"Enrollment rate {rate:.0%} vs planned"],
        recommendation="Review site enrollment by country; trigger recruitment mitigations and reforecast.",
        evidence={
            "kpi": {"enrollment_rate": rate},
            "data_slice": {
                "week_start": str(weekly_metrics_latest.week_start),
                "actual_enrolled_cum": int(weekly_metrics_latest.actual_enrolled_cum),
                "planned_enrolled_cum": int(weekly_metrics_latest.planned_enrolled_cum),
            },
            "generated_at": _now_iso(),
        },
    )


def high_screen_failure(weekly_metrics_latest: pd.Series) -> RiskRuleResult | None:
    sfr = screen_failure_rate(int(weekly_metrics_latest.screen_fail_cum), int(weekly_metrics_latest.screened_cum))
    if sfr <= 0.35:
        return None
    score = float((sfr - 0.35) * 100)
    return RiskRuleResult(
        rule_id="RISK_SCREEN_FAIL",
        title="High screen failure rate",
        severity="High" if sfr > 0.45 else "Medium",
        score=score,
        drivers=[f"Screen failure {sfr:.0%} above threshold"],
        recommendation="Review inclusion/exclusion criteria interpretation and screening workflow; add pre-screening.",
        evidence={
            "kpi": {"screen_failure_rate": sfr},
            "data_slice": {
                "week_start": str(weekly_metrics_latest.week_start),
                "screened_cum": int(weekly_metrics_latest.screened_cum),
                "screen_fail_cum": int(weekly_metrics_latest.screen_fail_cum),
            },
            "generated_at": _now_iso(),
        },
    )


def query_backlog(weekly_metrics_latest: pd.Series) -> RiskRuleResult | None:
    open_q = int(weekly_metrics_latest.open_queries)
    if open_q <= 30:
        return None
    score = float(open_q - 30)
    return RiskRuleResult(
        rule_id="RISK_QUERY_BACKLOG",
        title="Data query backlog",
        severity="High" if open_q > 60 else "Medium",
        score=score,
        drivers=[f"Open queries = {open_q}"],
        recommendation="Triage and assign DM cleanup; agree SLA; focus on top sites contributing to backlog.",
        evidence={
            "kpi": {"open_queries": open_q},
            "data_slice": {"week_start": str(weekly_metrics_latest.week_start)},
            "generated_at": _now_iso(),
        },
    )


def vendor_ticket_spike(weekly_metrics_latest: pd.Series) -> RiskRuleResult | None:
    tickets = int(weekly_metrics_latest.vendor_tickets)
    if tickets <= 18:
        return None
    score = float(tickets - 18)
    return RiskRuleResult(
        rule_id="RISK_VENDOR_TICKETS",
        title="Vendor ticket spike",
        severity="Medium",
        score=score,
        drivers=[f"Vendor tickets (latest week) = {tickets}"],
        recommendation="Engage vendor; review ticket categories; set 2-week stabilization plan.",
        evidence={
            "kpi": {"vendor_tickets": tickets},
            "data_slice": {"week_start": str(weekly_metrics_latest.week_start)},
            "generated_at": _now_iso(),
        },
    )


def protocol_deviation_spike(weekly_metrics_latest: pd.Series) -> RiskRuleResult | None:
    dev = int(weekly_metrics_latest.protocol_deviations)
    if dev <= 6:
        return None
    score = float(dev - 6)
    return RiskRuleResult(
        rule_id="RISK_DEVIATIONS",
        title="Protocol deviation spike",
        severity="High" if dev > 10 else "Medium",
        score=score,
        drivers=[f"Protocol deviations (latest week) = {dev}"],
        recommendation="Investigate root cause by site; retrain and reinforce protocol adherence.",
        evidence={
            "kpi": {"protocol_deviations": dev},
            "data_slice": {"week_start": str(weekly_metrics_latest.week_start)},
            "generated_at": _now_iso(),
        },
    )


ALL_RULES = [slow_enrollment, high_screen_failure, query_backlog, vendor_ticket_spike, protocol_deviation_spike]
