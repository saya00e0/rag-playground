"""Run the semantic-seed GraphRAG experiment against the frozen benchmark."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from eval.dataset import load_dataset
from eval.evaluate_graph import run_graph_evaluation
from eval.evaluate_retrieval import summarize
from graph.semantic_seed import EMBEDDING_MODEL, SemanticGraphRetriever, load_or_create_matcher
from graph.store import load_graph


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", default="eval/results/graph_v2.json")
    parser.add_argument("--dataset", default="eval/dataset.jsonl")
    parser.add_argument("--output-dir", default="eval/results")
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--max-entities", type=int, default=5)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    artifact = load_graph(args.graph)
    dataset = load_dataset(args.dataset)
    matcher = load_or_create_matcher(artifact["graph"])
    rows = run_graph_evaluation(
        dataset,
        SemanticGraphRetriever(artifact["graph"], matcher),
        args.depth,
        args.max_entities,
        args.top_k,
    )
    summary = {
        "system": "graph",
        "variant": "semantic_seed_v1",
        "seed_method": "top-5 embedding similarity over frozen graph node names",
        "embedding_model": EMBEDDING_MODEL,
        "graph_path": args.graph,
        "dataset_path": args.dataset,
        "dataset_question_count": len(dataset),
        "relevance_unit": "document_id",
        "top_k": args.top_k,
        "depth": args.depth,
        "max_entities": args.max_entities,
        **summarize(rows),
    }
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "semantic_seed_v1_raw.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_dir / "semantic_seed_v1_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
