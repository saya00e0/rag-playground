"""Shared result types so every retriever returns comparable, inspectable output."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.llm import Usage


@dataclass(frozen=True)
class RetrievedItem:
    unit_id: str
    doc_id: str
    text: str
    score: float
    section_ids: tuple[str, ...]


@dataclass
class RetrievalResult:
    retriever: str
    items: list[RetrievedItem]
    latency_ms: float
    usage: Usage = field(default_factory=Usage)
    note: str = ""

    @property
    def doc_ids(self) -> list[str]:
        return list(dict.fromkeys(item.doc_id for item in self.items))

    def covered_units(self) -> set[str]:
        return {item.doc_id for item in self.items} | {sid for item in self.items for sid in item.section_ids}
