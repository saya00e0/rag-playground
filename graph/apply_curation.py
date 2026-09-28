"""Create a separately stored curated graph from a frozen automatic graph."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from graph.builder import graph_statistics
from graph.curation import apply_curation
from graph.store import load_graph, save_graph


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="eval/results/graph_v2.json")
    parser.add_argument("--curation", default="eval/curation_v1.json")
    parser.add_argument("--output", default="eval/results/graph_curated_v1.json")
    args = parser.parse_args()

    source = load_graph(args.source)
    curation = json.loads(Path(args.curation).read_text(encoding="utf-8"))
    graph, change_log = apply_curation(source["graph"], curation)
    metadata = {
        "source_graph": args.source,
        "source_prompt_version": source["metadata"]["prompt_version"],
        "curation": change_log,
        "statistics": graph_statistics(graph),
    }
    save_graph(args.output, graph, metadata)
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
