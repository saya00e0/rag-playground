"""Trace frozen GraphRAG retrieval results without changing retrieval behavior."""

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from typing import Optional

from eval.dataset import load_dataset
from graph.retriever import GraphRetriever
from graph.store import load_graph


MANUAL_FAILURE_CLASSIFICATIONS = {
    "q009": ("1. entity extraction failure", "The access-rule and decision concepts in the question were not retained as graph entities."),
    "q010": ("5. traversal/ranking failure", "Catalog Service is a seed and has provenance for the missed document, but it was ranked below top-5."),
    "q011": ("5. traversal/ranking failure", "Policy Service is a seed and has provenance for both missed documents, but neither appeared in top-5."),
    "q014": ("5. traversal/ranking failure", "Both service names are seeds and the missed team-role document is reachable, but it was ranked below top-5."),
    "q015": ("1. entity extraction failure", "The source discusses access rules, but no matching access-rule entity exists in the graph."),
    "q018": ("3. seed entity matching failure", "The generic word document matched only the unrelated sample-document node instead of the intended policy entities."),
    "q021": ("1. entity extraction failure", "Average response time was not extracted as an entity even though the operations source contains the concept."),
    "q023": ("5. traversal/ranking failure", "Named seeds exist and the acceptance-criteria document is reachable, but it was ranked below top-5."),
}


def shortest_paths(graph: dict, seeds: list[str], depth: int) -> dict[str, list[str]]:
    """Reconstruct deterministic shortest node paths for analysis only."""
    neighbors: dict[str, set[str]] = {node["id"]: set() for node in graph["nodes"]}
    for edge in graph["edges"]:
        neighbors[edge["source"]].add(edge["target"])
        neighbors[edge["target"]].add(edge["source"])
    paths = {seed: [seed] for seed in seeds}
    queue = deque(seeds)
    while queue:
        current = queue.popleft()
        if len(paths[current]) - 1 >= depth:
            continue
        for neighbor in sorted(neighbors[current]):
            if neighbor not in paths:
                paths[neighbor] = paths[current] + [neighbor]
                queue.append(neighbor)
    return paths


def path_for_chunk(graph: dict, paths: dict[str, list[str]], source: str, chunk_idx: int) -> list[str]:
    chunk_ref = f"{source}#{chunk_idx}"
    candidates = [node["id"] for node in graph["nodes"] if chunk_ref in node["chunk_refs"] and node["id"] in paths]
    if not candidates:
        return []
    chosen = min(candidates, key=lambda node_id: (len(paths[node_id]), node_id))
    names = {node["id"]: node["name"] for node in graph["nodes"]}
    return [names[node_id] for node_id in paths[chosen]]


def suggested_failure_category(required: set[str], retrieved: set[str], seeds: list[str], paths: dict[str, list[str]], graph: dict) -> Optional[str]:
    missed = required.difference(retrieved)
    if not missed:
        return None
    if not seeds:
        return "3. seed entity matching failure"
    visited_refs = {
        chunk_ref
        for node in graph["nodes"]
        if node["id"] in paths
        for chunk_ref in node["chunk_refs"]
    }
    if any(any(chunk_ref.startswith(document + "#") for chunk_ref in visited_refs) for document in missed):
        return "5. traversal/ranking failure"
    graph_refs = {chunk_ref for node in graph["nodes"] for chunk_ref in node["chunk_refs"]}
    if any(not any(chunk_ref.startswith(document + "#") for chunk_ref in graph_refs) for document in missed):
        return "1. entity extraction failure"
    return "4. missing graph edge"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", default="eval/results/graph_v2.json")
    parser.add_argument("--graph-raw", default="eval/results/graph_auto_v2_raw.json")
    parser.add_argument("--vector-raw", default="eval/results/vector_raw.json")
    parser.add_argument("--dataset", default="eval/dataset.jsonl")
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--max-entities", type=int, default=5)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--output", default="eval/results/graph_failure_analysis.json")
    args = parser.parse_args()

    artifact = load_graph(args.graph)
    graph = artifact["graph"]
    retriever = GraphRetriever(graph)
    dataset = [item for item in load_dataset(args.dataset) if item.type in {"multi_hop", "relationship"}]
    vector_rows = {row["id"]: row for row in json.loads(Path(args.vector_raw).read_text(encoding="utf-8"))}
    graph_rows = {row["id"]: row for row in json.loads(Path(args.graph_raw).read_text(encoding="utf-8"))}

    records = []
    for item in dataset:
        seeds = retriever.seed_entities(item.question, args.max_entities)
        paths = shortest_paths(graph, seeds, args.depth)
        graph_chunks = retriever.retrieve(item.question, depth=args.depth, max_entities=args.max_entities, max_chunks=args.top_k)
        required = set(item.relevant_docs)
        retrieved = {chunk.source for chunk in graph_chunks}
        inferred = suggested_failure_category(required, retrieved, seeds, paths, graph)
        manual = MANUAL_FAILURE_CLASSIFICATIONS.get(item.id)
        records.append(
            {
                "id": item.id,
                "type": item.type,
                "question": item.question,
                "required_relevant_documents": list(item.relevant_docs),
                "vector_top_5": [
                    {"document": document, "score": score}
                    for document, score in zip(vector_rows[item.id]["retrieved_doc_ids"], vector_rows[item.id]["scores"])
                ],
                "graph_top_5": [
                    {
                        "document": chunk.source,
                        "chunk_idx": chunk.chunk_idx,
                        "score": chunk.score,
                        "traversal_path": path_for_chunk(graph, paths, chunk.source, chunk.chunk_idx),
                    }
                    for chunk in graph_chunks
                ],
                "seed_entities": [next(node["name"] for node in graph["nodes"] if node["id"] == seed) for seed in seeds],
                "required_documents_missed_by_graph": sorted(required.difference(retrieved)),
                "failure_category": manual[0] if manual else inferred,
                "classification_rationale": manual[1] if manual else None,
                "benchmark_note": "does not require graph traversal" if item.type == "multi_hop" and len(item.relevant_docs) == 1 else None,
            }
        )

    output = {
        "graph_variant": "auto_v2",
        "graph_path": args.graph,
        "depth": args.depth,
        "max_entities": args.max_entities,
        "top_k": args.top_k,
        "records": records,
    }
    Path(args.output).write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"record_count": len(records), "output": args.output}, ensure_ascii=False))


if __name__ == "__main__":
    main()
