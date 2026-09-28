"""Local JSON graph persistence; stored artifacts contain no chunk text."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Union


def save_graph(path: Union[str, Path], graph: dict, metadata: dict) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps({"metadata": metadata, "graph": graph}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def load_graph(path: Union[str, Path]) -> dict:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if set(raw) != {"metadata", "graph"} or not isinstance(raw["graph"], dict):
        raise ValueError("invalid graph store")
    return raw
