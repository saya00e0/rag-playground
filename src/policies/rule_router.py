"""Hand-written keyword router, frozen before any experiment result was observed."""

from __future__ import annotations

import re
from dataclasses import dataclass

IDENTIFIER = re.compile(
    r"[A-Z]{1,4}-\d+"                 # error codes and tickets: HX-4417, E-74, HLN-2340
    r"|\b\d+\.\d+\.\d+\b"             # versions: 4.12.3
    r"|\b[a-z]+\.[a-z_]+\b"           # config keys: ingest.max_batch_bytes
    r"|(?<!\w)--[a-z][a-z-]*"         # CLI flags: --dry-merge
)
DOCUMENT_CUES = ("according to", "per the", "under the", "handbook", "agreement", "contract")
RELATION_CUES = ("connected to", "partner", "developed by", "routed", "which team", "approv", "responsible", "lead")


@dataclass(frozen=True)
class RuleDecision:
    selected_retriever: str
    reasoning: str


def rule_route(query: str) -> RuleDecision:
    lowered = query.lower()
    if IDENTIFIER.search(query):
        return RuleDecision("bm25", f"identifier-like token {IDENTIFIER.search(query).group(0)!r}")
    cue = next((cue for cue in DOCUMENT_CUES if cue in lowered), None)
    if cue:
        return RuleDecision("pageindex", f"names a specific document ({cue!r})")
    cue = next((cue for cue in RELATION_CUES if cue in lowered), None)
    if cue:
        return RuleDecision("graph", f"relationship cue {cue!r}")
    return RuleDecision("vector", "no rule matched; default to semantic search")
