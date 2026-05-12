from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SyntheticSpec:
    n_studies: int = 7
    min_sites: int = 4
    max_sites: int = 12
    n_weeks: int = 20
    start_date: date = date(2025, 1, 6)  # Monday


PHASES = ["Phase 1", "Phase 2", "Phase 3"]
STATUSES = ["Recruiting", "Active", "Completed"]
CONDITIONS = ["Oncology", "Cardiology", "Dermatology", "Neurology"]
COUNTRIES = ["US", "DE", "IN", "UK", "FR", "ES", "BR", "JP"]


def generate_all(seed: int, spec: SyntheticSpec = SyntheticSpec()) -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(seed)

    studies = []
    sites = []
    weekly = []
    milestones = []

    for i in range(spec.n_studies):
        study_id = f"STUDY-{1000 + i}"
        planned_enrollment = int(rng.integers(80, 320))
        phase = str(rng.choice(PHASES))
        status = str(rng.choice(STATUSES, p=[0.6, 0.3, 0.1]))
        condition = str(rng.choice(CONDITIONS))
        start_dt = spec.start_date + timedelta(weeks=int(rng.integers(0, 10)))

        studies.append(
            {
                "study_id": study_id,
                "title": f"{condition} Study {i+1}",
                "phase": phase,
                "status": status,
                "condition": condition,
                "planned_enrollment": planned_enrollment,
                "start_date": start_dt,
            }
        )

        n_sites = int(rng.integers(spec.min_sites, spec.max_sites + 1))
        site_ids = [f"{study_id}-SITE-{j+1:02d}" for j in range(n_sites)]

        for sid in site_ids:
            country = str(rng.choice(COUNTRIES))
            planned_activation = start_dt + timedelta(days=int(rng.integers(7, 42)))
            delay_days = int(max(0, rng.normal(10, 12)))
            activated = rng.random() > 0.1
            actual_activation = planned_activation + timedelta(days=delay_days) if activated else None

            sites.append(
                {
                    "site_id": sid,
                    "study_id": study_id,
                    "country": country,
                    "investigator": f"Dr {country}-{sid[-2:]}",
                    "planned_activation_date": planned_activation,
                    "actual_activation_date": actual_activation,
                }
            )

        # milestones
        for name, weeks_out in [
            ("FPI", 2),
            ("LPI", 14),
            ("DBL", 18),
        ]:
            planned = start_dt + timedelta(weeks=weeks_out)
            slip_days = int(max(0, rng.normal(7, 10))) if rng.random() < 0.35 else 0
            actual = planned + timedelta(days=slip_days) if (status != "Recruiting" and rng.random() < 0.6) else None
            milestones.append(
                {
                    "study_id": study_id,
                    "name": name,
                    "planned_date": planned,
                    "actual_date": actual,
                }
            )

        # weekly metrics per site
        weeks = [start_dt + timedelta(weeks=w) for w in range(spec.n_weeks)]
        # enrollment curve target
        weekly_target = planned_enrollment / spec.n_weeks

        for sid in site_ids:
            actual_cum = 0
            planned_cum = 0
            screened_cum = 0
            fail_cum = 0
            open_q = int(rng.integers(0, 15))

            base_rate = float(rng.uniform(0.4, 1.6))  # relative speed
            fail_rate = float(rng.uniform(0.18, 0.45))

            for wstart in weeks:
                planned_inc = max(0, int(rng.normal(weekly_target / n_sites, 0.8)))
                planned_cum += planned_inc

                # actual lower than planned sometimes
                slowdown = 0.6 if rng.random() < 0.18 else 1.0
                actual_inc = max(0, int(rng.normal((weekly_target / n_sites) * base_rate * slowdown, 1.1)))
                actual_cum += actual_inc

                screened_inc = max(actual_inc, int(actual_inc / (1 - fail_rate + 1e-6)))
                screened_cum += screened_inc
                fail_cum += max(0, screened_inc - actual_inc)

                # queries trend
                open_q = max(0, int(open_q + rng.normal(0.3, 2.0)))
                deviations = max(0, int(rng.poisson(0.3)))
                vendor_tickets = max(0, int(rng.poisson(1.2)))

                weekly.append(
                    {
                        "study_id": study_id,
                        "site_id": sid,
                        "week_start": wstart,
                        "planned_enrolled_cum": planned_cum,
                        "actual_enrolled_cum": actual_cum,
                        "screened_cum": screened_cum,
                        "screen_fail_cum": fail_cum,
                        "open_queries": open_q,
                        "protocol_deviations": deviations,
                        "vendor_tickets": vendor_tickets,
                    }
                )

    return {
        "studies": pd.DataFrame(studies),
        "sites": pd.DataFrame(sites),
        "weekly_metrics": pd.DataFrame(weekly),
        "milestones": pd.DataFrame(milestones),
    }
