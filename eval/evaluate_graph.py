"""Evaluate a frozen graph artifact against the retrieval benchmark."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from eval.dataset import load_dataset
from eval.evaluate_retrieval import DEFAULT_KS, score_question, summarize
from graph.retriever import GraphRetriever
from graph.store import load_graph


def run_graph_evaluation(dataset, retriever: GraphRetriever, depth: int, max_entities: int, top_k: int) -> list[dict]:
    rows: list[dict] = []
    for item in dataset:
        started = time.perf_counter()
        chunks = retriever.retrieve(item.question, depth=depth, max_entities=max_entities, max_chunks=top_k)
        latency_ms = (time.perf_counter() - started) * 1000
        retrieved = [chunk.source for chunk in chunks]
        rows.append(
            {
                "id": item.id,
                "type": item.type,
                "question": item.question,
                "expected_doc_ids": list(item.relevant_docs),
                "retrieved_doc_ids": retrieved,
                "scores": [chunk.score for chunk in chunks],
                "latency_ms": latency_ms,
                **score_question(set(item.relevant_docs), retrieved, DEFAULT_KS),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", required=True)
    parser.add_argument("--variant", required=True, choices=("auto_v2", "curated_v1"))
    parser.add_argument("--dataset", default="eval/dataset.jsonl")
    parser.add_argument("--output-dir", default="eval/results")
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--max-entities", type=int, default=5)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()
    if args.top_k < max(DEFAULT_KS):
        parser.error("--top-k must be at least 5 to calculate Recall@5")

    graph_artifact = load_graph(args.graph)
    dataset = load_dataset(args.dataset)
    rows = run_graph_evaluation(dataset, GraphRetriever(graph_artifact["graph"]), args.depth, args.max_entities, args.top_k)
    summary = {
        "system": "graph",
        "variant": args.variant,
        "graph_path": args.graph,
        "graph_metadata": graph_artifact["metadata"],
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
    (output_dir / f"graph_{args.variant}_raw.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_dir / f"graph_{args.variant}_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
