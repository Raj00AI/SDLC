import pandas as pd

from catalyst_ai.kpi.calc import enrollment_rate, screen_failure_rate


def test_enrollment_rate():
    assert enrollment_rate(85, 100) == 0.85
    assert enrollment_rate(0, 0) == 0.0


def test_screen_failure_rate():
    assert screen_failure_rate(20, 100) == 0.2
    assert screen_failure_rate(1, 0) == 0.0
