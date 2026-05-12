from __future__ import annotations

from dataclasses import dataclass

from catalyst_ai.agents.agents import define_agent, design_agent, discover_agent, plan_agent
from catalyst_ai.agents.base import AgentConfig, AgentResult
from catalyst_ai.agents.grading import grade_markdown


@dataclass(frozen=True)
class PipelineRun:
    discover: AgentResult
    define: AgentResult
    design: AgentResult
    plan: AgentResult
    scorecards: dict


def run_pipeline(*, problem_statement: str, config: AgentConfig) -> PipelineRun:
    context: dict = {}

    discover = discover_agent(problem_statement=problem_statement, config=config, context=context, iteration=1)
    define = define_agent(discover_md=discover.content_md, config=config, context=context, iteration=1)

    # Quality gate loop on design+plan (fast for demo)
    design_best: AgentResult | None = None
    plan_best: AgentResult | None = None
    scorecards: dict = {}

    for i in range(1, config.max_iterations + 1):
        design = design_agent(
            discover_md=discover.content_md,
            define_md=define.content_md,
            config=config,
            context=context,
            iteration=i,
        )
        sc_d, gaps_d = grade_markdown("design", design.content_md)
        scorecards[f"design_{i}"] = {"scorecard": sc_d.__dict__, "overall": sc_d.overall, "gaps": gaps_d}

        if design_best is None or sc_d.overall > scorecards[f"design_{design_best.iteration}"]["overall"]:
            design_best = design

        if sc_d.overall >= config.quality_threshold:
            break

    assert design_best is not None

    for i in range(1, config.max_iterations + 1):
        plan = plan_agent(
            discover_md=discover.content_md,
            define_md=define.content_md,
            design_md=design_best.content_md,
            config=config,
            context=context,
            iteration=i,
        )
        sc_p, gaps_p = grade_markdown("plan", plan.content_md)
        scorecards[f"plan_{i}"] = {"scorecard": sc_p.__dict__, "overall": sc_p.overall, "gaps": gaps_p}

        if plan_best is None or sc_p.overall > scorecards[f"plan_{plan_best.iteration}"]["overall"]:
            plan_best = plan

        if sc_p.overall >= config.quality_threshold:
            break

    assert plan_best is not None

    return PipelineRun(discover=discover, define=define, design=design_best, plan=plan_best, scorecards=scorecards)
