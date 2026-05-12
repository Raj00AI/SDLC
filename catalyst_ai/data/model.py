from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class Study(BaseModel):
    study_id: str
    title: str
    phase: str
    status: str
    condition: str
    planned_enrollment: int
    start_date: date


class Site(BaseModel):
    site_id: str
    study_id: str
    country: str
    investigator: str
    planned_activation_date: date
    actual_activation_date: date | None


class WeeklyMetrics(BaseModel):
    study_id: str
    site_id: str
    week_start: date
    planned_enrolled_cum: int
    actual_enrolled_cum: int
    screened_cum: int
    screen_fail_cum: int
    open_queries: int
    protocol_deviations: int
    vendor_tickets: int


class Milestone(BaseModel):
    study_id: str
    name: str
    planned_date: date
    actual_date: date | None


class ActionItem(BaseModel):
    action_id: str
    study_id: str
    linked_risk_id: str | None = None
    title: str
    owner: str
    due_date: date
    status: str
    created_by: str
    created_at: str


class Risk(BaseModel):
    risk_id: str
    study_id: str
    rule_id: str
    title: str
    severity: str
    score: float
    drivers: list[str]
    recommendation: str
    evidence: dict
    created_at: str
