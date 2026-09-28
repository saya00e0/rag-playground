"""Apply a reviewed, declarative graph curation without overwriting its source."""

from __future__ import annotations

import copy


EDGE_FIELDS = ("source", "type", "target", "chunk_ref")


def _find_edge(edges: list[dict], selector: dict) -> int:
    matches = [
        index for index, edge in enumerate(edges)
        if all(edge.get(field) == selector[field] for field in EDGE_FIELDS)
    ]
    if len(matches) != 1:
        raise ValueError(f"curation selector must match exactly one edge: {selector}")
    return matches[0]


def apply_curation(graph: dict, curation: dict) -> tuple[dict, dict]:
    """Return a curated copy and a machine-readable, auditable change log."""
    curated = copy.deepcopy(graph)
    nodes = {node["id"]: node for node in curated["nodes"]}
    changes: list[dict] = []

    for operation in curation.get("set_node_types", []):
        node = nodes.get(operation["id"])
        if node is None:
            raise ValueError(f"curation references missing node {operation['id']!r}")
        before = list(node["types"])
        node["types"] = list(operation["types"])
        changes.append({"operation": "set_node_types", "id": operation["id"], "before": before, "after": node["types"], "reason": operation["reason"]})

    for operation in curation.get("reverse_edges", []):
        edge = curated["edges"][_find_edge(curated["edges"], operation)]
        edge["source"], edge["target"] = edge["target"], edge["source"]
        changes.append({"operation": "reverse_edge", "edge": operation, "reason": operation["reason"]})

    for operation in curation.get("remove_edges", []):
        index = _find_edge(curated["edges"], operation)
        curated["edges"].pop(index)
        changes.append({"operation": "remove_edge", "edge": operation, "reason": operation["reason"]})

    return curated, {"curation_id": curation["id"], "operations": changes}
