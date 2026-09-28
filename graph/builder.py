"""Build a provenance-preserving graph from chunk extractions."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from graph.extractor import Extraction, normalize_entity


@dataclass(frozen=True)
class ChunkRef:
    source: str
    chunk_idx: int

    def key(self) -> str:
        return f"{self.source}#{self.chunk_idx}"


class GraphBuilder:
    def __init__(self) -> None:
        self.nodes: dict[str, dict] = {}
        self.edges: list[dict] = []

    def add_extraction(self, chunk: ChunkRef, extraction: Extraction) -> None:
        entity_names: set[str] = set()
        for entity in extraction.entities:
            node_id = normalize_entity(entity.name)
            if not node_id:
                continue
            entity_names.add(node_id)
            node = self.nodes.setdefault(
                node_id,
                {"id": node_id, "name": entity.name, "types": [], "chunk_refs": []},
            )
            if entity.type not in node["types"]:
                node["types"].append(entity.type)
            if chunk.key() not in node["chunk_refs"]:
                node["chunk_refs"].append(chunk.key())

        for relation in extraction.relations:
            source_id = normalize_entity(relation.source)
            target_id = normalize_entity(relation.target)
            if not source_id or not target_id:
                continue
            for node_id, display_name in ((source_id, relation.source), (target_id, relation.target)):
                node = self.nodes.setdefault(
                    node_id,
                    {"id": node_id, "name": display_name, "types": ["unknown"], "chunk_refs": []},
                )
                if chunk.key() not in node["chunk_refs"]:
                    node["chunk_refs"].append(chunk.key())
            edge = {
                "source": source_id,
                "target": target_id,
                "type": relation.type,
                "chunk_ref": chunk.key(),
            }
            if edge not in self.edges:
                self.edges.append(edge)

    def build(self) -> dict:
        return {"nodes": list(self.nodes.values()), "edges": self.edges}


def graph_statistics(graph: dict) -> dict:
    nodes = graph["nodes"]
    edges = graph["edges"]
    neighbors: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        neighbors[edge["source"]].add(edge["target"])
        neighbors[edge["target"]].add(edge["source"])

    visited: set[str] = set()
    components = 0
    for node in nodes:
        node_id = node["id"]
        if node_id in visited:
            continue
        components += 1
        stack = [node_id]
        visited.add(node_id)
        while stack:
            current = stack.pop()
            for neighbor in neighbors[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
    relation_types = sorted({edge["type"] for edge in edges})
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "relation_types": relation_types,
        "connected_components": components,
        "average_degree": (2 * len(edges) / len(nodes)) if nodes else 0.0,
        "isolated_node_count": sum(not neighbors[node["id"]] for node in nodes),
    }
