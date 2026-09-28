"""Render the frozen graph failure-analysis JSON as a reviewable Markdown report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def document_list(items: list[dict], include_path: bool = False) -> str:
    if not items:
        return "なし"
    rendered = []
    for item in items:
        text = f"`{item['document']}` ({item['score']:.3f})"
        if include_path:
            path = " → ".join(item["traversal_path"]) or "seed なし"
            text += f"; path: {path}"
        rendered.append(text)
    return "<br>".join(rendered)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="eval/results/graph_failure_analysis.json")
    parser.add_argument("--output", default="eval/results/graph_failure_analysis.md")
    args = parser.parse_args()
    analysis = json.loads(Path(args.input).read_text(encoding="utf-8"))
    lines = [
        "# GraphRAG failure analysis",
        "",
        "Frozen Graph auto v2; depth=2, maximum seed entities=5, top-k=5. This report does not modify retrieval, parameters, or the dataset.",
        "",
    ]
    failures = [record for record in analysis["records"] if record["failure_category"]]
    vector_complete_multi_hop = [
        record["id"]
        for record in analysis["records"]
        if record["type"] == "multi_hop" and record["vector_retrieves_all_required_evidence"]
    ]
    lines.extend(
        [
            f"Graph failures: {len(failures)}. " + ", ".join(
                f"{category}: {sum(record['failure_category'] == category for record in failures)}"
                for category in sorted({record["failure_category"] for record in failures})
            ),
            "",
            "Multi-hop questions where Vector retrieved every required document without graph traversal: "
            + (", ".join(vector_complete_multi_hop) or "none"),
            "",
        ]
    )
    for record in analysis["records"]:
        lines.extend(
            [
                f"## {record['id']} — {record['type']}",
                "",
                f"- Question: {record['question']}",
                f"- Required relevant documents: {', '.join(f'`{item}`' for item in record['required_relevant_documents'])}",
                f"- Vector top-5 documents and scores: {document_list(record['vector_top_5'])}",
                f"- Graph top-5 documents: {document_list(record['graph_top_5'], include_path=True)}",
                f"- Detected seed entities: {', '.join(record['seed_entities']) or 'なし'}",
                f"- Required documents missed by Graph: {', '.join(f'`{item}`' for item in record['required_documents_missed_by_graph']) or 'なし'}",
                f"- Vector retrieves all required evidence: {'yes' if record['vector_retrieves_all_required_evidence'] else 'no'}",
                f"- Graph failure category: {record['failure_category'] or 'なし（必要文書をすべて取得）'}",
            ]
        )
        if record["classification_rationale"]:
            lines.append(f"- Classification rationale: {record['classification_rationale']}")
        if record["benchmark_note"]:
            lines.append(f"- Benchmark note: {record['benchmark_note']}")
        lines.append("")
    Path(args.output).write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
