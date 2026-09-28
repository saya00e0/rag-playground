"""Semantic node matching experiment; traversal and ranking remain unchanged."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dotenv import load_dotenv

from graph.retriever import GraphRetriever, GraphRetrievedChunk


EMBEDDING_MODEL = "text-embedding-3-small"


def cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = sum(value * value for value in left) ** 0.5
    right_norm = sum(value * value for value in right) ** 0.5
    return numerator / (left_norm * right_norm) if left_norm and right_norm else 0.0


class SemanticSeedMatcher:
    def __init__(self, node_ids: list[str], node_names: list[str], node_vectors: list[list[float]]) -> None:
        self.node_ids = node_ids
        self.node_names = node_names
        self.node_vectors = node_vectors

    def match(self, query_vector: list[float], maximum: int) -> list[tuple[str, str, float]]:
        scored = [
            (node_id, node_name, cosine_similarity(query_vector, node_vector))
            for node_id, node_name, node_vector in zip(self.node_ids, self.node_names, self.node_vectors)
        ]
        return sorted(scored, key=lambda item: (-item[2], item[0]))[:maximum]


def graph_fingerprint(graph: dict) -> str:
    nodes = [{"id": node["id"], "name": node["name"]} for node in graph["nodes"]]
    return hashlib.sha256(json.dumps(nodes, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def load_or_create_matcher(graph: dict, cache_dir: str = "eval/results/semantic_seed_cache") -> SemanticSeedMatcher:
    fingerprint = graph_fingerprint(graph)
    cache_path = Path(cache_dir) / f"{fingerprint}.json"
    if cache_path.exists():
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        if cached.get("model") == EMBEDDING_MODEL and cached.get("fingerprint") == fingerprint:
            return SemanticSeedMatcher(cached["node_ids"], cached["node_names"], cached["node_vectors"])

    from openai import OpenAI

    load_dotenv()
    nodes = sorted(graph["nodes"], key=lambda node: node["id"])
    response = OpenAI().embeddings.create(input=[node["name"] for node in nodes], model=EMBEDDING_MODEL)
    cached = {
        "model": EMBEDDING_MODEL,
        "fingerprint": fingerprint,
        "node_ids": [node["id"] for node in nodes],
        "node_names": [node["name"] for node in nodes],
        "node_vectors": [item.embedding for item in response.data],
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cached, ensure_ascii=False) + "\n", encoding="utf-8")
    return SemanticSeedMatcher(cached["node_ids"], cached["node_names"], cached["node_vectors"])


class SemanticGraphRetriever:
    def __init__(self, graph: dict, matcher: SemanticSeedMatcher) -> None:
        self.graph_retriever = GraphRetriever(graph)
        self.matcher = matcher

    def seed_entities(self, question: str, maximum: int) -> list[tuple[str, str, float]]:
        from openai import OpenAI

        load_dotenv()
        vector = OpenAI().embeddings.create(input=[question], model=EMBEDDING_MODEL).data[0].embedding
        return self.matcher.match(vector, maximum)

    def retrieve(self, question: str, depth: int = 2, max_entities: int = 5, max_chunks: int = 5) -> list[GraphRetrievedChunk]:
        seeds = self.seed_entities(question, max_entities)
        return self.graph_retriever.retrieve_from_seeds([node_id for node_id, _, _ in seeds], depth, max_entities, max_chunks)
