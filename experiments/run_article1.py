"""Run the article1 retrieval-routing experiment end to end.

    .venv/bin/python experiments/run_article1.py --config configs/article1.json

Every query is answered once with each retriever (the "base runs"). The policies then
choose among those base runs, so a policy's answer is exactly the answer its chosen
retriever produced; a policy's cost is its own decision overhead plus the retrieval and
generation it would have performed. Judge calls are evaluation overhead and are excluded
from policy cost, but count toward the budget.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from src.corpus import Query, chunk_document, corpus_sha256, load_corpus, load_queries  # noqa: E402
from src.evaluation.failures import categorize, oracle_set, routing_scope  # noqa: E402
from src.evaluation.generation import generate_answer  # noqa: E402
from src.evaluation.judge import judge_answer  # noqa: E402
from src.llm import BudgetExceeded, LLMClient, Usage  # noqa: E402
from src.policies.agent import run_agent  # noqa: E402
from src.policies.llm_router import llm_route  # noqa: E402
from src.policies.rule_router import rule_route  # noqa: E402
from src.retrievers.base import RetrievalResult  # noqa: E402
from src.retrievers.bm25 import BM25Retriever  # noqa: E402
from src.retrievers.graph import GraphRetriever  # noqa: E402
from src.retrievers.pageindex import PageIndexRetriever  # noqa: E402
from src.retrievers.vector import VectorRetriever  # noqa: E402

PREVIEW_CHARS = 160


def build_retrievers(config: dict, documents, chunks, llm: LLMClient) -> tuple[dict, dict]:
    top_k = config["retrieval_top_k"]
    cache_dir = config["cache_dir"]
    started = time.perf_counter()
    vector = VectorRetriever(chunks, llm, str(Path(cache_dir) / "chroma"), top_k)
    graph = GraphRetriever(
        chunks, config["llm"]["model"], cache_dir, top_k,
        config["graph"]["traversal_depth"], config["graph"]["max_seed_entities"], config["graph"]["max_extraction_chunks"],
    )
    retrievers = {
        "bm25": BM25Retriever(chunks, top_k, config["bm25"]["k1"], config["bm25"]["b"]),
        "vector": vector,
        "graph": graph,
        "pageindex": PageIndexRetriever(documents, llm, top_k, config["pageindex"]["max_unit_chars"]),
    }
    build_info = {
        "build_seconds": time.perf_counter() - started,
        "vector_embedding_usage": vars(vector.build_usage),
        "graph_statistics": graph.statistics,
        "graph_new_extraction_calls": graph.new_extraction_calls,
        "graph_extraction_cost_note": "extraction calls go through graph/extractor.py and are not token-metered here",
    }
    return {name: retrievers[name] for name in config["retrievers"]}, build_info


def base_run(llm: LLMClient, query: Query, retriever) -> dict:
    run = {"retriever": retriever.name, "error": None}
    try:
        retrieval = retriever.retrieve(query.query)
        answer, generation_usage = generate_answer(llm, query.query, retrieval)
        score, judge_reason, judge_usage = judge_answer(llm, query, answer)
    except BudgetExceeded:
        raise
    except Exception as exc:  # recorded per run so one failure does not hide the others
        retrieval = RetrievalResult(retriever.name, [], 0.0, note="retrieval or generation failed")
        answer, generation_usage, score, judge_reason, judge_usage = "", Usage(), 0, "", Usage()
        run["error"] = f"{type(exc).__name__}: {exc}"
    covered = retrieval.covered_units()
    evidence = query.evidence_units
    run.update(
        retrieval=retrieval,
        answer=answer,
        generation_usage=generation_usage,
        answer_score=score,
        judge_reason=judge_reason,
        judge_usage=judge_usage,
        evidence_recall=sum(unit in covered for unit in evidence) / len(evidence),
    )
    return run


def serialize_base_run(query: Query, run: dict) -> dict:
    retrieval: RetrievalResult = run["retrieval"]
    return {
        "query_id": query.id,
        "query_type": query.query_type,
        "retriever": run["retriever"],
        "retrieved_unit_ids": [item.unit_id for item in retrieval.items],
        "retrieved_document_ids": retrieval.doc_ids,
        "scores": [round(item.score, 6) for item in retrieval.items],
        "retrieval_note": retrieval.note,
        "evidence_recall": run["evidence_recall"],
        "generated_answer": run["answer"],
        "answer_score": run["answer_score"],
        "judge_reason": run["judge_reason"],
        "retrieval_latency_ms": retrieval.latency_ms,
        "generation_latency_ms": run["generation_usage"].latency_ms,
        "retrieval_usage": vars(retrieval.usage),
        "generation_usage": vars(run["generation_usage"]),
        "judge_usage": vars(run["judge_usage"]),
        "error": run["error"],
    }


def policy_row(query: Query, policy: str, final: dict, tried: list[dict], decision_usage: Usage, **extra) -> dict:
    retrieval: RetrievalResult = final["retrieval"]
    retrieval_usage = Usage()
    retrieval_latency = 0.0
    for run in tried:
        retrieval_usage = retrieval_usage + run["retrieval"].usage
        retrieval_latency += run["retrieval"].latency_ms
    generation_usage: Usage = final["generation_usage"]
    total_usage = decision_usage + retrieval_usage + generation_usage
    errors = [run["error"] for run in tried if run["error"]]
    row = {
        "query_id": query.id,
        "query": query.query,
        "query_type": query.query_type,
        "policy": policy,
        "selected_retriever": final["retriever"],
        "initial_retriever": tried[0]["retriever"],
        "router_reasoning": None,
        "router_confidence": None,
        "retrieved_document_ids": retrieval.doc_ids,
        "retrieved_unit_ids": [item.unit_id for item in retrieval.items],
        "retrieved_text_preview": " | ".join(f"[{item.unit_id}] {item.text[:PREVIEW_CHARS]}" for item in retrieval.items),
        "generated_answer": final["answer"],
        "answer_score": final["answer_score"],
        "judge_reason": final["judge_reason"],
        "evidence_recall": final["evidence_recall"],
        "decision_latency_ms": decision_usage.latency_ms,
        "retrieval_latency_ms": retrieval_latency,
        "generation_latency_ms": generation_usage.latency_ms,
        "total_latency_ms": decision_usage.latency_ms + retrieval_latency + generation_usage.latency_ms,
        "input_tokens": total_usage.input_tokens,
        "output_tokens": total_usage.output_tokens,
        "estimated_cost": total_usage.cost_usd,
        "retrieval_count": len(tried),
        "retry_count": len(tried) - 1,
        "tool_switch_count": len(tried) - 1,
        "error": "; ".join(errors) or None,
    }
    row.update(extra)
    return row


def run_query(config: dict, llm: LLMClient, retrievers: dict, query: Query) -> tuple[list[dict], list[dict]]:
    names = list(retrievers)
    base = {name: base_run(llm, query, retrievers[name]) for name in names}
    answer_scores = {name: base[name]["answer_score"] for name in names}
    answer_oracle = oracle_set(answer_scores)
    evidence_oracle = oracle_set({name: base[name]["evidence_recall"] for name in names})
    shared = {"oracle_retriever": answer_oracle, "evidence_oracle": evidence_oracle, "routing_scope": routing_scope(answer_scores)}

    rows = [policy_row(query, "fixed_vector", base["vector"], [base["vector"]], Usage(), router_reasoning="always vector", **shared)]

    rule = rule_route(query.query)
    rows.append(policy_row(query, "rule_router", base[rule.selected_retriever], [base[rule.selected_retriever]], Usage(), router_reasoning=rule.reasoning, **shared))

    router = llm_route(llm, query.query, names)
    rows.append(policy_row(
        query, "llm_router", base[router.selected_retriever], [base[router.selected_retriever]], router.usage,
        router_reasoning=router.reasoning, router_confidence=router.confidence, **shared,
    ))

    trace = run_agent(
        llm, query.query, router.selected_retriever, names, lambda name: base[name]["retrieval"],
        config["agent"]["max_switches"], config["agent"]["max_context_chars_per_item"],
    )
    rows.append(policy_row(
        query, "agent", base[trace.final_retriever], [base[name] for name in trace.tried], router.usage + trace.check_usage,
        router_reasoning=router.reasoning, router_confidence=router.confidence,
        agent_trace=[vars(step) for step in trace.steps], **shared,
    ))

    oracle_choice = answer_oracle[0] if answer_oracle else "vector"
    rows.append(policy_row(
        query, "oracle", base[oracle_choice], [base[oracle_choice]], Usage(),
        router_reasoning="highest answer_score after the fact" if answer_oracle else "no retriever answered correctly; vector shown as placeholder",
        **shared,
    ))

    for row in rows:
        row["routing_correct"] = (row["selected_retriever"] in answer_oracle) if answer_oracle else None
        row["failure_category"] = categorize(row, answer_oracle, evidence_oracle, answer_scores)
    return rows, [serialize_base_run(query, base[name]) for name in names]


def file_sha256(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/article1.json")
    parser.add_argument("--limit", type=int, help="run only the first N queries (smoke test)")
    parser.add_argument("--output-dir", help="override the configured output directory")
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    random.seed(config["seed"])
    documents = load_corpus(config["corpus_dir"])
    queries = load_queries(config["dataset_path"], documents)
    if args.limit:
        queries = queries[: args.limit]
    chunks = [chunk for document in documents for chunk in chunk_document(document, config["chunk_size"], config["chunk_overlap"])]
    output_dir = Path(args.output_dir or config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    llm = LLMClient(config)
    metadata = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "config": config,
        "config_path": args.config,
        "dataset_sha256": file_sha256(config["dataset_path"]),
        "corpus_sha256": corpus_sha256(documents),
        "document_count": len(documents),
        "chunk_count": len(chunks),
        "query_count": len(queries),
        "limit": args.limit,
    }
    retrievers, metadata["build"] = build_retrievers(config, documents, chunks, llm)

    policy_rows: list[dict] = []
    base_rows: list[dict] = []
    status = "completed"
    try:
        for number, query in enumerate(queries, 1):
            rows, runs = run_query(config, llm, retrievers, query)
            policy_rows.extend(rows)
            base_rows.extend(runs)
            print(f"[{number}/{len(queries)}] {query.id} spend={llm.total.cost_usd:.4f} USD", flush=True)
    except BudgetExceeded as exc:
        status = f"stopped: {exc}"
        print(status, file=sys.stderr)
    finally:
        metadata.update(finished_at=datetime.now(timezone.utc).isoformat(), status=status, total_usage=vars(llm.total))
        write_jsonl(output_dir / "raw_results.jsonl", policy_rows)
        write_jsonl(output_dir / "retriever_runs.jsonl", base_rows)
        (output_dir / "run_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "rows": len(policy_rows), "total_usage": vars(llm.total)}, indent=2))


if __name__ == "__main__":
    main()
