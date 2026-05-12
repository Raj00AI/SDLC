from __future__ import annotations

import os
from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class LLMResponse:
    text: str
    raw: dict


class LLMClient:
    """Minimal LLM client.

    Supports:
      - OpenAI-compatible Chat Completions endpoint (default)

    Env vars:
      - CATALYST_LLM_BASE_URL (optional) e.g. https://api.openai.com/v1
      - CATALYST_LLM_API_KEY
      - CATALYST_LLM_MODEL (optional)

    This avoids adding heavy agent frameworks while still enabling agentic orchestration.
    """

    def __init__(self) -> None:
        self.base_url = os.getenv("CATALYST_LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.api_key = os.getenv("CATALYST_LLM_API_KEY", "")
        self.model = os.getenv("CATALYST_LLM_MODEL", "gpt-4.1-mini")

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def chat(self, *, system: str, user: str, temperature: float = 0.2) -> LLMResponse:
        if not self.api_key:
            raise RuntimeError(
                "LLM is not configured. Set CATALYST_LLM_API_KEY (and optionally CATALYST_LLM_BASE_URL / CATALYST_LLM_MODEL)."
            )

        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }

        with httpx.Client(timeout=60) as client:
            resp = client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            raw = resp.json()
            text = raw["choices"][0]["message"]["content"]
            return LLMResponse(text=text, raw=raw)
