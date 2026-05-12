from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AgentConfig:
    quality_threshold: float = 0.8
    max_iterations: int = 3
    llm_model: str = "gpt-4.1-mini"  # overridable


@dataclass(frozen=True)
class AgentResult:
    name: str
    iteration: int
    content_md: str
    metadata: dict


class Agent(Protocol):
    name: str

    def run(self, *, prompt: str, config: AgentConfig, context: dict, iteration: int) -> AgentResult: ...
