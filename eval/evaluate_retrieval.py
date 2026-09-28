"""Run the existing Vector RAG retriever against a frozen JSONL benchmark."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import time
from collections import defaultdict
from pathlib import Path
from typing import Callable, Iterable, Optional

from eval.dataset import EvaluationQuestion, load_dataset
DEFAULT_KS = (1, 3, 5)


def corpus_hash(document_paths: Iterable[str]) -> str:
    """Hash the evaluated source files in a stable path/content order."""
    digest = hashlib.sha256()
    for document_path in sorted(set(document_paths)):
        path = Path(document_path)
        digest.update(document_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def score_question(relevant_docs: set[str], retrieved_docs: list[str], ks: tuple[int, ...] = DEFAULT_KS) -> dict:
    """Calculate document-level recall and reciprocal rank for one query."""
    if not relevant_docs:
        raise ValueError("relevant_docs must not be empty")

    unique_retrieved = list(dict.fromkeys(retrieved_docs))
    metrics = {
        f"recall_at_{k}": len(relevant_docs.intersection(unique_retrieved[:k])) / len(relevant_docs)
        for k in ks
    }
    metrics["reciprocal_rank"] = next(
        (1 / rank for rank, document in enumerate(unique_retrieved, 1) if document in relevant_docs),
        0.0,
    )
    return metrics


def summarize(rows: list[dict], ks: tuple[int, ...] = DEFAULT_KS) -> dict:
    """Aggregate per-question metrics overall and by question type."""
    if not rows:
        raise ValueError("cannot summarize zero rows")

    def aggregate(group: list[dict]) -> dict:
        result = {
            f"Recall@{k}": statistics.fmean(row[f"recall_at_{k}"] for row in group)
            for k in ks
        }
        result["MRR"] = statistics.fmean(row["reciprocal_rank"] for row in group)
        result["mean_latency_ms"] = statistics.fmean(row["latency_ms"] for row in group)
        result["question_count"] = len(group)
        return result

    by_type: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_type[row["type"]].append(row)
    return {
        "aggregate": aggregate(rows),
        "by_type": {question_type: aggregate(group) for question_type, group in sorted(by_type.items())},
    }


def run_vector_evaluation(
    dataset: list[EvaluationQuestion],
    top_k: int,
    retrieve_fn: Optional[Callable] = None,
) -> list[dict]:
    if retrieve_fn is None:
        # Delay OpenAI/Chroma initialization so metric and schema tests are offline.
        from retriever import retrieve

        retrieve_fn = retrieve
    rows: list[dict] = []
    for item in dataset:
        started = time.perf_counter()
        chunks = retrieve_fn(item.question, top_k=top_k)
        latency_ms = (time.perf_counter() - started) * 1000
        retrieved = [chunk.source for chunk in chunks]
        metrics = score_question(set(item.relevant_docs), retrieved)
        rows.append(
            {
                "id": item.id,
                "type": item.type,
                "question": item.question,
                "expected_doc_ids": list(item.relevant_docs),
                "retrieved_doc_ids": retrieved,
                "scores": [chunk.score for chunk in chunks],
                "latency_ms": latency_ms,
                **metrics,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="eval/dataset.jsonl")
    parser.add_argument("--output-dir", default="eval/results")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()
    if args.top_k < max(DEFAULT_KS):
        parser.error("--top-k must be at least 5 to calculate Recall@5")

    dataset = load_dataset(args.dataset)
    rows = run_vector_evaluation(dataset, args.top_k)
    summary = {
        "system": "vector",
        "dataset_path": args.dataset,
        "dataset_question_count": len(dataset),
        "relevance_unit": "document_id",
        "top_k": args.top_k,
        "corpus_sha256": corpus_hash(
            doc for item in dataset for doc in item.relevant_docs
        ),
        **summarize(rows),
    }
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "vector_raw.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "vector_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
