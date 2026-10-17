"""Summarize article1 raw results: summary.csv, routing_analysis.md, failure_cases.md, charts.

    .venv/bin/python scripts/analyze_article1.py --results-dir results/article1

Reads only the files written by experiments/run_article1.py; makes no API calls.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from src.evaluation.failures import CATEGORY_LABELS  # noqa: E402

POLICIES = ["fixed_vector", "rule_router", "llm_router", "agent", "oracle"]
RETRIEVERS = ["bm25", "vector", "graph", "pageindex"]
QUERY_TYPES = ["keyword_exact", "semantic_paraphrase", "relationship", "multi_hop", "reasoning_heavy", "long_doc_navigation"]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def mean(values) -> float:
    values = list(values)
    return statistics.fmean(values) if values else float("nan")


def aggregate(rows: list[dict]) -> dict:
    with_oracle = [row for row in rows if row["routing_correct"] is not None]
    sensitive = [row for row in rows if row["routing_scope"] == "routing_sensitive"]
    return {
        "n": len(rows),
        "answer_accuracy": mean(row["answer_score"] for row in rows),
        "routing_accuracy_sensitive": mean(row["routing_correct"] for row in sensitive),
        "n_routing_sensitive": len(sensitive),
        "routing_accuracy_any_oracle": mean(row["routing_correct"] for row in with_oracle),
        "n_with_oracle": len(with_oracle),
        "mean_total_latency_ms": mean(row["total_latency_ms"] for row in rows),
        "mean_input_tokens": mean(row["input_tokens"] for row in rows),
        "mean_output_tokens": mean(row["output_tokens"] for row in rows),
        "mean_estimated_cost_usd": mean(row["estimated_cost"] for row in rows),
        "mean_retrieval_count": mean(row["retrieval_count"] for row in rows),
        "error_count": sum(bool(row["error"]) for row in rows),
    }


def write_summary(rows: list[dict], path: Path) -> list[dict]:
    summary = []
    for policy in POLICIES:
        group = [row for row in rows if row["policy"] == policy]
        if group:
            summary.append({"scope": "policy", "policy": policy, "query_type": "all", **aggregate(group)})
    for policy in POLICIES:
        for query_type in QUERY_TYPES:
            group = [row for row in rows if row["policy"] == policy and row["query_type"] == query_type]
            if group:
                summary.append({"scope": "policy_x_query_type", "policy": policy, "query_type": query_type, **aggregate(group)})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0]))
        writer.writeheader()
        for record in summary:
            writer.writerow({key: (round(value, 4) if isinstance(value, float) else value) for key, value in record.items()})
    return summary


def table(header: list[str], body: list[list]) -> str:
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    lines += ["| " + " | ".join(str(cell) for cell in row) + " |" for row in body]
    return "\n".join(lines)


def fmt(value: float) -> str:
    return "n/a" if value != value else f"{value:.2f}"


def write_routing_analysis(rows: list[dict], base: list[dict], path: Path) -> None:
    parts = ["# Routing analysis\n"]

    parts.append("## Per-retriever answer accuracy (base runs)\n")
    body = []
    for query_type in QUERY_TYPES + ["all"]:
        cells = [query_type]
        for retriever in RETRIEVERS:
            group = [r for r in base if r["retriever"] == retriever and (query_type == "all" or r["query_type"] == query_type)]
            cells.append(f"{fmt(mean(r['answer_score'] for r in group))} / ev {fmt(mean(r['evidence_recall'] for r in group))}")
        body.append(cells)
    parts.append("Cell = answer accuracy / mean evidence recall.\n\n" + table(["query_type"] + RETRIEVERS, body) + "\n")

    oracle_rows = [row for row in rows if row["policy"] == "oracle"]
    scope_counts = Counter(row["routing_scope"] for row in oracle_rows)
    parts.append("## Routing scope of queries\n")
    parts.append(table(["scope", "queries"], [[scope, count] for scope, count in sorted(scope_counts.items())]) + "\n")
    by_type_scope = defaultdict(Counter)
    for row in oracle_rows:
        by_type_scope[row["query_type"]][row["routing_scope"]] += 1
    parts.append(table(
        ["query_type", "routing_sensitive", "all_correct", "none_correct"],
        [[qt, by_type_scope[qt]["routing_sensitive"], by_type_scope[qt]["all_correct"], by_type_scope[qt]["none_correct"]] for qt in QUERY_TYPES],
    ) + "\n")

    for policy in ["llm_router", "rule_router"]:
        group = [row for row in rows if row["policy"] == policy]
        parts.append(f"## {policy}: query_type x selected retriever\n")
        counts = Counter((row["query_type"], row["selected_retriever"]) for row in group)
        parts.append(table(["query_type"] + RETRIEVERS, [[qt] + [counts[(qt, r)] for r in RETRIEVERS] for qt in QUERY_TYPES]) + "\n")
        parts.append(f"## {policy}: answer-oracle set x selected retriever (routing-sensitive queries)\n")
        sensitive = [row for row in group if row["routing_scope"] == "routing_sensitive"]
        oracle_labels = sorted({"+".join(row["oracle_retriever"]) for row in sensitive})
        counts = Counter(("+".join(row["oracle_retriever"]), row["selected_retriever"]) for row in sensitive)
        parts.append(table(["oracle set"] + RETRIEVERS, [[label] + [counts[(label, r)] for r in RETRIEVERS] for label in oracle_labels]) + "\n")

    router = [row for row in rows if row["policy"] == "llm_router"]
    sensitive = [row for row in router if row["routing_scope"] == "routing_sensitive"]
    parts.append("## LLM router confidence\n")
    parts.append(table(
        ["subset", "n", "mean confidence"],
        [
            ["routing correct (sensitive)", sum(r["routing_correct"] for r in sensitive), fmt(mean(r["router_confidence"] for r in sensitive if r["routing_correct"]))],
            ["routing wrong (sensitive)", sum(not r["routing_correct"] for r in sensitive), fmt(mean(r["router_confidence"] for r in sensitive if not r["routing_correct"]))],
            ["wrong with confidence >= 0.8", sum((not r["routing_correct"]) and r["router_confidence"] >= 0.8 for r in sensitive), ""],
        ],
    ) + "\n")

    evidence_hit = [r for r in router if r["evidence_oracle"]]
    pairs = Counter((r["selected_retriever"] in r["evidence_oracle"], r["answer_score"] > 0) for r in evidence_hit)
    parts.append("## LLM router: evidence-oracle routing vs answer correctness\n")
    parts.append(
        "Against the answer oracle, routing correctness and answer correctness coincide by construction "
        "for a single-shot router, so the evidence oracle is used here.\n\n"
        + table(
            ["", "answer correct", "answer wrong"],
            [
                ["chose evidence-oracle retriever", pairs[(True, True)], pairs[(True, False)]],
                ["missed evidence oracle", pairs[(False, True)], pairs[(False, False)]],
            ],
        )
        + "\n"
    )
    path.write_text("\n".join(parts), encoding="utf-8")


def representative(rows: list[dict], category: str, limit: int = 3) -> list[dict]:
    hits = [row for row in rows if category in row["failure_category"]]
    # Cases where intuition about the query shape misleads come first.
    hits.sort(key=lambda row: (row["query_type"] not in ("multi_hop", "relationship"), -(row["router_confidence"] or 0), row["query_id"]))
    return hits[:limit]


def write_failure_cases(rows: list[dict], base: list[dict], path: Path) -> None:
    base_index = {(r["query_id"], r["retriever"]): r for r in base}
    parts = ["# Failure cases\n", "Categories are assigned automatically by src/evaluation/failures.py. Up to three examples each.\n"]
    for category, label in CATEGORY_LABELS.items():
        hits = [row for row in rows if category in row["failure_category"]]
        parts.append(f"## {category}. {label}\n\nTotal: {len(hits)}\n")
        for row in representative(rows, category):
            scores = ", ".join(f"{r}={base_index[(row['query_id'], r)]['answer_score']}" for r in RETRIEVERS if (row["query_id"], r) in base_index)
            parts.append(
                f"### {row['query_id']} ({row['query_type']}, policy={row['policy']})\n\n"
                f"- Query: {row['query']}\n"
                f"- Initial / final retriever: {row['initial_retriever']} / {row['selected_retriever']}"
                f" (confidence {row['router_confidence']})\n"
                f"- Router reasoning: {row['router_reasoning']}\n"
                f"- Answer oracle: {row['oracle_retriever']}; evidence oracle: {row['evidence_oracle']}\n"
                f"- Per-retriever answer scores: {scores}\n"
                f"- Retrieved units: {row['retrieved_unit_ids']}\n"
                f"- Answer (score {row['answer_score']}): {row['generated_answer']}\n"
            )
            if row.get("agent_trace"):
                steps = "; ".join(f"{s['retriever']}: sufficient={s['sufficient']} -> {s['next_retriever']} ({s['reasoning']})" for s in row["agent_trace"])
                parts.append(f"- Agent trace: {steps}\n")
    path.write_text("\n".join(parts), encoding="utf-8")


def bar_chart(path: Path, title: str, labels: list[str], values: list[float], value_format: str, max_value: float) -> None:
    """Minimal dependency-free horizontal bar chart."""
    row_height, left, width = 30, 190, 360
    height = 50 + row_height * len(labels)
    bars = []
    for index, (label, value) in enumerate(zip(labels, values)):
        y = 40 + index * row_height
        length = 0 if value != value else width * value / max_value
        text = "n/a" if value != value else value_format.format(value)
        bars.append(
            f'<text x="{left - 8}" y="{y + 15}" text-anchor="end">{label}</text>'
            f'<rect x="{left}" y="{y + 3}" width="{length:.1f}" height="18" fill="#4C6EF5"/>'
            f'<text x="{left + length + 6:.1f}" y="{y + 16}">{text}</text>'
        )
    path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{left + width + 90}" height="{height}" '
        f'font-family="Helvetica, Arial, sans-serif" font-size="13">'
        f'<rect width="100%" height="100%" fill="#ffffff"/>'
        f'<text x="12" y="24" font-size="15" font-weight="bold">{title}</text>{"".join(bars)}</svg>\n',
        encoding="utf-8",
    )


def write_charts(summary: list[dict], output_dir: Path) -> None:
    policy_rows = {record["policy"]: record for record in summary if record["scope"] == "policy"}
    present = [p for p in POLICIES if p in policy_rows]
    bar_chart(output_dir / "chart_answer_accuracy.svg", "Final answer accuracy by policy", present,
              [policy_rows[p]["answer_accuracy"] for p in present], "{:.2f}", 1.0)
    routed = [p for p in present if p != "oracle"]
    bar_chart(output_dir / "chart_routing_accuracy.svg", "Routing accuracy vs answer oracle (routing-sensitive queries)", routed,
              [policy_rows[p]["routing_accuracy_sensitive"] for p in routed], "{:.2f}", 1.0)
    costs = [policy_rows[p]["mean_input_tokens"] + policy_rows[p]["mean_output_tokens"] for p in routed]
    bar_chart(output_dir / "chart_tokens.svg", "Mean tokens per query (decision + retrieval + generation)", routed,
              costs, "{:.0f}", max(costs) or 1.0)
    type_rows = {record["query_type"]: record for record in summary if record["scope"] == "policy_x_query_type" and record["policy"] == "llm_router"}
    types = [qt for qt in QUERY_TYPES if qt in type_rows]
    bar_chart(output_dir / "chart_router_accuracy_by_type.svg", "LLM router: routing accuracy by query type (sensitive queries)", types,
              [type_rows[qt]["routing_accuracy_sensitive"] for qt in types], "{:.2f}", 1.0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results/article1")
    args = parser.parse_args()
    results_dir = Path(args.results_dir)
    rows = read_jsonl(results_dir / "raw_results.jsonl")
    base = read_jsonl(results_dir / "retriever_runs.jsonl")
    summary = write_summary(rows, results_dir / "summary.csv")
    write_routing_analysis(rows, base, results_dir / "routing_analysis.md")
    write_failure_cases(rows, base, results_dir / "failure_cases.md")
    write_charts(summary, results_dir)
    for record in summary:
        if record["scope"] == "policy":
            print(
                f"{record['policy']:>13}: answer={fmt(record['answer_accuracy'])} "
                f"routing(sensitive)={fmt(record['routing_accuracy_sensitive'])} n_sens={record['n_routing_sensitive']} "
                f"latency={record['mean_total_latency_ms']:.0f}ms cost=${record['mean_estimated_cost_usd']:.5f} "
                f"retrievals={record['mean_retrieval_count']:.2f}"
            )


if __name__ == "__main__":
    main()
