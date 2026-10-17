"""OpenAI wrapper that records tokens, latency, and estimated cost, and enforces the budget."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field

from dotenv import load_dotenv


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    calls: int = 0
    latency_ms: float = 0.0
    cost_usd: float = 0.0

    def __add__(self, other: "Usage") -> "Usage":
        return Usage(
            self.input_tokens + other.input_tokens,
            self.output_tokens + other.output_tokens,
            self.calls + other.calls,
            self.latency_ms + other.latency_ms,
            self.cost_usd + other.cost_usd,
        )


class BudgetExceeded(RuntimeError):
    pass


@dataclass
class LLMClient:
    config: dict
    total: Usage = field(default_factory=Usage)

    def __post_init__(self) -> None:
        from openai import OpenAI

        load_dotenv()
        self._client = OpenAI()
        self.model = self.config["llm"]["model"]
        self.temperature = self.config["llm"]["temperature"]
        self.max_output_tokens = self.config["llm"]["max_output_tokens"]
        self.seed = self.config["seed"]
        self.embedding_model = self.config["embedding_model"]
        self.pricing = self.config["pricing_usd_per_1m_tokens"]
        self.budget = self.config["budget_usd"]

    def _record(self, model: str, input_tokens: int, output_tokens: int, latency_ms: float) -> Usage:
        price = self.pricing[model]
        usage = Usage(
            input_tokens,
            output_tokens,
            1,
            latency_ms,
            (input_tokens * price["input"] + output_tokens * price["output"]) / 1_000_000,
        )
        self.total = self.total + usage
        if self.total.cost_usd > self.budget:
            raise BudgetExceeded(f"estimated spend {self.total.cost_usd:.4f} USD exceeds budget {self.budget} USD")
        return usage

    def chat_json(self, system: str, user: str, schema_name: str, schema: dict) -> tuple[dict, Usage]:
        """One chat call with strict JSON-schema output."""
        started = time.perf_counter()
        response = self._client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            seed=self.seed,
            max_tokens=self.max_output_tokens,
            response_format={"type": "json_schema", "json_schema": {"name": schema_name, "strict": True, "schema": schema}},
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        usage = self._record(
            self.model,
            response.usage.prompt_tokens,
            response.usage.completion_tokens,
            (time.perf_counter() - started) * 1000,
        )
        content = response.choices[0].message.content
        if not content:
            raise ValueError(f"{schema_name}: empty response")
        return json.loads(content), usage

    def chat_text(self, system: str, user: str) -> tuple[str, Usage]:
        started = time.perf_counter()
        response = self._client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            seed=self.seed,
            max_tokens=self.max_output_tokens,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        usage = self._record(
            self.model,
            response.usage.prompt_tokens,
            response.usage.completion_tokens,
            (time.perf_counter() - started) * 1000,
        )
        return response.choices[0].message.content or "", usage

    def embed(self, texts: list[str]) -> tuple[list[list[float]], Usage]:
        started = time.perf_counter()
        response = self._client.embeddings.create(input=texts, model=self.embedding_model)
        usage = self._record(self.embedding_model, response.usage.prompt_tokens, 0, (time.perf_counter() - started) * 1000)
        return [item.embedding for item in response.data], usage
