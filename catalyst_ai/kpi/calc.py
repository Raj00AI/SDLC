from __future__ import annotations

import pandas as pd


def enrollment_rate(actual_cum: int, planned_cum: int) -> float:
    if planned_cum <= 0:
        return 0.0
    return actual_cum / planned_cum


def screen_failure_rate(screen_fail_cum: int, screened_cum: int) -> float:
    if screened_cum <= 0:
        return 0.0
    return screen_fail_cum / screened_cum


def activation_lag_days(planned_date: pd.Timestamp, actual_date: pd.Timestamp | None) -> float:
    if actual_date is None or pd.isna(actual_date):
        return float("nan")
    return float((actual_date - planned_date).days)


def milestone_slippage_days(planned_date: pd.Timestamp, actual_date: pd.Timestamp | None) -> float:
    if actual_date is None or pd.isna(actual_date):
        return 0.0
    return float((actual_date - planned_date).days)


def study_kpi_snapshot(weekly_metrics: pd.DataFrame) -> pd.DataFrame:
    """Return latest-week KPIs per study.

    Expects columns: study_id, week_start, planned_enrolled_cum, actual_enrolled_cum,
    screened_cum, screen_fail_cum, open_queries.
    """
    if weekly_metrics.empty:
        return pd.DataFrame()

    wm = weekly_metrics.sort_values(["study_id", "week_start"])
    latest = wm.groupby("study_id", as_index=False).tail(1)

    latest = latest.copy()
    latest["enrollment_rate"] = latest.apply(
        lambda r: enrollment_rate(int(r.actual_enrolled_cum), int(r.planned_enrolled_cum)), axis=1
    )
    latest["screen_failure_rate"] = latest.apply(
        lambda r: screen_failure_rate(int(r.screen_fail_cum), int(r.screened_cum)), axis=1
    )

    return latest[[
        "study_id",
        "week_start",
        "planned_enrolled_cum",
        "actual_enrolled_cum",
        "enrollment_rate",
        "screen_failure_rate",
        "open_queries",
        "protocol_deviations",
        "vendor_tickets",
    ]]
