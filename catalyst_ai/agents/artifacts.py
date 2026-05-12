from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from catalyst_ai.agents.base import AgentConfig
from catalyst_ai.agents.pipeline import PipelineRun, run_pipeline
from catalyst_ai.artifacts.generator import write_text
from catalyst_ai.config import get_paths


def write_agentic_artifacts(*, problem_statement: str, config: AgentConfig) -> dict[str, Path]:
    paths = get_paths()
    out: dict[str, Path] = {}

    run: PipelineRun = run_pipeline(problem_statement=problem_statement, config=config)

    out["discover"] = write_text(paths.artifacts_dir, "agent-discover", run.discover.content_md).path
    out["define"] = write_text(paths.artifacts_dir, "agent-define", run.define.content_md).path
    out["design"] = write_text(paths.artifacts_dir, "agent-design", run.design.content_md).path
    out["plan"] = write_text(paths.artifacts_dir, "agent-plan", run.plan.content_md).path

    score_path = paths.artifacts_dir / "agent-scorecards.json"
    score_path.write_text(json.dumps(run.scorecards, indent=2), encoding="utf-8")
    out["scorecards"] = score_path

    cfg_path = paths.artifacts_dir / "agent-config.json"
    cfg_path.write_text(json.dumps(asdict(config), indent=2), encoding="utf-8")
    out["config"] = cfg_path

    return out
