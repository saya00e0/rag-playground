"""Schema validation and loading for the retrieval benchmark dataset."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Union


VALID_TYPES = frozenset({"factual", "multi_hop", "relationship"})


@dataclass(frozen=True)
class EvaluationQuestion:
    id: str
    question: str
    type: str
    relevant_docs: tuple[str, ...]
    evidence: str


def load_dataset(path: Union[str, Path]) -> list[EvaluationQuestion]:
    """Load a JSONL dataset and reject incomplete or ambiguous records."""
    records: list[EvaluationQuestion] = []
    seen_ids: set[str] = set()

    for line_number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_number}: invalid JSON") from exc

        required = {"id", "question", "type", "relevant_docs", "evidence"}
        missing = required.difference(raw)
        if missing:
            raise ValueError(f"line {line_number}: missing fields {sorted(missing)}")
        if not isinstance(raw["id"], str) or not raw["id"].strip():
            raise ValueError(f"line {line_number}: id must be a non-empty string")
        if raw["id"] in seen_ids:
            raise ValueError(f"line {line_number}: duplicate id {raw['id']}")
        if not isinstance(raw["question"], str) or not raw["question"].strip():
            raise ValueError(f"line {line_number}: question must be a non-empty string")
        if raw["type"] not in VALID_TYPES:
            raise ValueError(f"line {line_number}: unsupported type {raw['type']!r}")
        if not isinstance(raw["relevant_docs"], list) or not raw["relevant_docs"]:
            raise ValueError(f"line {line_number}: relevant_docs must be a non-empty list")
        if not all(isinstance(item, str) and item.strip() for item in raw["relevant_docs"]):
            raise ValueError(f"line {line_number}: relevant_docs must contain non-empty strings")
        if not isinstance(raw["evidence"], str) or not raw["evidence"].strip():
            raise ValueError(f"line {line_number}: evidence must be a non-empty string")

        seen_ids.add(raw["id"])
        records.append(
            EvaluationQuestion(
                id=raw["id"],
                question=raw["question"],
                type=raw["type"],
                relevant_docs=tuple(raw["relevant_docs"]),
                evidence=raw["evidence"],
            )
        )

    if not records:
        raise ValueError("dataset contains no records")
    return records
