import pandas as pd

from catalyst_ai.risk.rules import high_screen_failure, slow_enrollment


def test_slow_enrollment_triggers():
    row = pd.Series(
        {
            "week_start": "2025-01-06",
            "actual_enrolled_cum": 50,
            "planned_enrolled_cum": 100,
            "screened_cum": 100,
            "screen_fail_cum": 20,
            "open_queries": 10,
            "protocol_deviations": 0,
            "vendor_tickets": 0,
        }
    )
    r = slow_enrollment(row)
    assert r is not None


def test_high_screen_failure_not_triggered():
    row = pd.Series(
        {
            "week_start": "2025-01-06",
            "actual_enrolled_cum": 80,
            "planned_enrolled_cum": 90,
            "screened_cum": 100,
            "screen_fail_cum": 30,
            "open_queries": 10,
            "protocol_deviations": 0,
            "vendor_tickets": 0,
        }
    )
    r = high_screen_failure(row)
    assert r is None
