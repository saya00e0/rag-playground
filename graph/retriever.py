"""Lexical seed matching and bounded graph traversal for source retrieval."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass

from graph.extractor import normalize_entity


@dataclass(frozen=True)
class GraphRetrievedChunk:
    source: str
    chunk_idx: int
    score: float


class GraphRetriever:
    def __init__(self, graph: dict) -> None:
        self.nodes = {node["id"]: node for node in graph["nodes"]}
        self.neighbors: dict[str, set[str]] = defaultdict(set)
        self.edge_refs: dict[tuple[str, str], list[str]] = defaultdict(list)
        for edge in graph["edges"]:
            self.neighbors[edge["source"]].add(edge["target"])
            self.neighbors[edge["target"]].add(edge["source"])
            self.edge_refs[(edge["source"], edge["target"])].append(edge["chunk_ref"])
            self.edge_refs[(edge["target"], edge["source"])].append(edge["chunk_ref"])

    def seed_entities(self, question: str, maximum: int) -> list[str]:
        normalized_question = normalize_entity(question)
        matches = [
            node_id for node_id in self.nodes
            if len(node_id) > 1 and node_id in normalized_question
        ]
        return sorted(matches, key=len, reverse=True)[:maximum]

    def retrieve(self, question: str, depth: int = 2, max_entities: int = 5, max_chunks: int = 5) -> list[GraphRetrievedChunk]:
        if depth < 0 or max_entities < 1 or max_chunks < 1:
            raise ValueError("depth, max_entities, and max_chunks must be positive")
        seeds = self.seed_entities(question, max_entities)
        return self.retrieve_from_seeds(seeds, depth=depth, max_entities=max_entities, max_chunks=max_chunks)

    def retrieve_from_seeds(self, seeds: list[str], depth: int = 2, max_entities: int = 5, max_chunks: int = 5) -> list[GraphRetrievedChunk]:
        """Traverse from supplied node IDs using the baseline ranking behavior."""
        if depth < 0 or max_entities < 1 or max_chunks < 1:
            raise ValueError("depth, max_entities, and max_chunks must be positive")
        seeds = seeds[:max_entities]
        distances: dict[str, int] = {seed: 0 for seed in seeds}
        queue = deque(seeds)
        while queue:
            current = queue.popleft()
            if distances[current] >= depth:
                continue
            for neighbor in self.neighbors[current]:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)

        chunk_scores: dict[str, float] = defaultdict(float)
        for node_id, distance in distances.items():
            for chunk_ref in self.nodes[node_id]["chunk_refs"]:
                chunk_scores[chunk_ref] += 1 / (distance + 1)
        for (source, target), refs in self.edge_refs.items():
            if source in distances and target in distances:
                edge_distance = min(distances[source], distances[target])
                for chunk_ref in refs:
                    chunk_scores[chunk_ref] += 1 / (edge_distance + 1)

        results = []
        for chunk_ref, score in sorted(chunk_scores.items(), key=lambda item: (-item[1], item[0]))[:max_chunks]:
            source, chunk_idx = chunk_ref.rsplit("#", 1)
            results.append(GraphRetrievedChunk(source=source, chunk_idx=int(chunk_idx), score=score))
        return results
