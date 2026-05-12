import pytest

from catalyst_ai.agents.base import AgentConfig
from catalyst_ai.agents.llm import LLMClient


def test_llm_requires_key():
    llm = LLMClient()
    if llm.is_configured():
        pytest.skip("LLM key available in environment; offline check not applicable")

    with pytest.raises(RuntimeError):
        llm.chat(system="s", user="u")


def test_agent_config_defaults():
    cfg = AgentConfig()
    assert cfg.quality_threshold == 0.8
    assert cfg.max_iterations == 3
