"""Create a compact CSV comparison from already executed retrieval summaries."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


METRICS = ("Recall@1", "Recall@3", "Recall@5", "MRR", "mean_latency_ms")


def load_summary(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vector", default="eval/results/vector_summary.json")
    parser.add_argument("--auto", default="eval/results/graph_auto_v2_summary.json")
    parser.add_argument("--curated", default="eval/results/graph_curated_v1_summary.json")
    parser.add_argument("--output", default="eval/results/comparison.csv")
    args = parser.parse_args()
    summaries = {"vector": load_summary(args.vector), "graph_auto_v2": load_summary(args.auto), "graph_curated_v1": load_summary(args.curated)}
    scopes = ("aggregate", "factual", "multi_hop", "relationship")

    with Path(args.output).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("scope", "metric", *summaries), lineterminator="\n")
        writer.writeheader()
        for scope in scopes:
            for metric in METRICS:
                writer.writerow(
                    {
                        "scope": scope,
                        "metric": metric,
                        **{name: summary["aggregate"][metric] if scope == "aggregate" else summary["by_type"][scope][metric] for name, summary in summaries.items()},
                    }
                )


if __name__ == "__main__":
    main()
