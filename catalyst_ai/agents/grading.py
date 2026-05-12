from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Scorecard:
    completeness: float
    consistency: float
    feasibility: float
    testability: float

    @property
    def overall(self) -> float:
        return round((self.completeness + self.consistency + self.feasibility + self.testability) / 4.0, 3)


REQUIRED_SECTIONS = {
    "discover": ["Glossary", "KPI Dictionary", "Initial Backlog"],
    "define": ["Questionnaire", "Assumptions"],
    "design": ["Architecture", "Data Model", "API Contract", "Risk Rules"],
    "plan": ["Sprint 1", "Sprint 2"],
}


def grade_markdown(doc_type: str, md: str) -> tuple[Scorecard, list[str]]:
    missing = []
    for section in REQUIRED_SECTIONS.get(doc_type, []):
        if section.lower() not in md.lower():
            missing.append(section)

    completeness = 1.0 if not missing else max(0.0, 1.0 - 0.2 * len(missing))

    # Simple heuristics for demo (deterministic + fast)
    consistency = 1.0 if "tbd" not in md.lower() else 0.7
    feasibility = 1.0 if "local" in md.lower() or "duckdb" in md.lower() else 0.8
    testability = 1.0 if "acceptance" in md.lower() or "tests" in md.lower() else 0.75

    gaps = [f"Add missing section: {m}" for m in missing]
    return Scorecard(completeness, consistency, feasibility, testability), gaps
