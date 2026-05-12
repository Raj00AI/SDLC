from catalyst_ai.narrative.meeting_pack import generate_meeting_pack


def test_meeting_pack_renders_html():
    study = {"study_id": "STUDY-1000", "title": "Test"}
    kpi = {
        "week_start": "2025-01-06",
        "planned_enrolled_cum": 100,
        "actual_enrolled_cum": 80,
        "enrollment_rate": 0.8,
        "screen_failure_rate": 0.2,
        "open_queries": 10,
        "protocol_deviations": 1,
        "vendor_tickets": 2,
    }
    pack = generate_meeting_pack(study, kpi, risks=[])
    assert "<html>" in pack.html.lower()
    assert "Traceability" in pack.html
