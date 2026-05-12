from __future__ import annotations

from dataclasses import dataclass

from catalyst_ai.agents.base import AgentConfig, AgentResult
from catalyst_ai.agents.llm import LLMClient


_SYSTEM = """You are Catalyst.AI SDLC Accelerator Agent.
You must produce privacy-safe content using only public/synthetic data.
Ensure explainability/traceability: every insight/risk should reference KPIs + underlying data slice.
Prefer structured, testable outputs.
"""


@dataclass(frozen=True)
class PromptSpec:
    name: str
    doc_type: str
    instructions: str


def _run_llm(name: str, doc_type: str, prompt: str, config: AgentConfig, context: dict, iteration: int) -> AgentResult:
    llm = LLMClient()
    text = llm.chat(system=_SYSTEM, user=prompt, temperature=0.2).text
    return AgentResult(
        name=name,
        iteration=iteration,
        content_md=text.strip(),
        metadata={"doc_type": doc_type, "iteration": iteration, "llm_model": llm.model},
    )


def discover_agent(*, problem_statement: str, config: AgentConfig, context: dict, iteration: int) -> AgentResult:
    prompt = f"""
Create a DISCOVER (Research Agent) output for the following problem statement.

Problem statement:
{problem_statement}

Output must be Markdown with sections:
- Problem Decomposition
- Glossary
- KPI Dictionary (include definition, formula, source table, grain)
- Initial Backlog (epics + 8-12 user stories + acceptance criteria)
- Assumptions

Keep it demo-ready and consistent with a Streamlit+FastAPI+DuckDB prototype.
""".strip()
    return _run_llm("Discover", "discover", prompt, config, context, iteration)


def define_agent(*, discover_md: str, config: AgentConfig, context: dict, iteration: int) -> AgentResult:
    prompt = f"""
Create a DEFINE (SME Questionnaire Agent) output.

Inputs (Discover output):
{discover_md}

Output must be Markdown with sections:
- Questionnaire (10-15 focused questions on KPI thresholds, workflows, meeting cadence, decision rights, action tracking)
- Synthesized Answers (simulate plausible SME answers for demo; clearly labeled as assumptions)
- Assumptions (updated)
- Updated Stories / Acceptance Criteria (only deltas)

Ensure KPI thresholds are explicit for at least 5 risk rules.
""".strip()
    return _run_llm("Define", "define", prompt, config, context, iteration)


def design_agent(*, discover_md: str, define_md: str, config: AgentConfig, context: dict, iteration: int) -> AgentResult:
    prompt = f"""
Create a DESIGN (Architecture Agent) output for Catalyst.AI.

Inputs:
[Discover]
{discover_md}

[Define]
{define_md}

Output must be Markdown with sections:
- Architecture (include components and data flow)
- Data Model
- API Contract
- Risk Rules Catalog (at least 5 rules with thresholds)
- NFRs
- Traceability Approach (story->design->code->tests)

Include a diagram description; diagrams can be ASCII if needed.
""".strip()
    return _run_llm("Design", "design", prompt, config, context, iteration)


def plan_agent(*, discover_md: str, define_md: str, design_md: str, config: AgentConfig, context: dict, iteration: int) -> AgentResult:
    prompt = f"""
Create a PLAN (Sprint Planning Agent) output.

Inputs:
[Discover]
{discover_md}

[Define]
{define_md}

[Design]
{design_md}

Output must be Markdown with sections:
- Sprint 1 (tasks, dependencies, DoD, demo checkpoint)
- Sprint 2
- Sprint 3
- Risks to delivery + mitigations

Make it achievable for a small team and align to acceptance criteria.
""".strip()
    return _run_llm("Plan", "plan", prompt, config, context, iteration)
