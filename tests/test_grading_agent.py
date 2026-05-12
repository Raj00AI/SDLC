from catalyst_ai.agents.grading import grade_markdown


def test_grade_markdown_detects_missing_sections():
    md = "# Design\n\n## Architecture\nHello"
    score, gaps = grade_markdown("design", md)
    assert score.overall < 1.0
    assert any("missing section" in g.lower() for g in gaps)
