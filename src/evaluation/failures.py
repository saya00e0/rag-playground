"""Oracle sets and failure categories.

Two oracles are computed per query:

* answer oracle (article definition): retrievers with the highest answer_score.
* evidence oracle: retrievers with the highest evidence recall (labelled sections or docs).

With an answer-defined oracle, categories C and D are impossible for a single-shot router,
because the router's answer *is* its chosen retriever's answer. C and D are therefore
judged against the evidence oracle; this is recorded in every row's failure_category.
"""

from __future__ import annotations

CATEGORY_LABELS = {
    "A": "LLM Router chose graph, but vector was in the answer oracle (graph was not)",
    "B": "LLM Router chose vector, but graph or pageindex was in the answer oracle (vector was not)",
    "C": "LLM Router missed the evidence oracle, but the final answer was correct",
    "D": "LLM Router chose an evidence-oracle retriever, but the final answer was wrong",
    "E": "Agent recovered from a wrong initial routing by retrying",
    "F": "Agent retried without improving the answer (extra cost only)",
}


def oracle_set(scores: dict[str, float]) -> list[str]:
    best = max(scores.values())
    if best <= 0:
        return []
    return [name for name, score in scores.items() if score == best]


def routing_scope(answer_scores: dict[str, float]) -> str:
    correct = sum(score > 0 for score in answer_scores.values())
    if correct == 0:
        return "none_correct"
    if correct == len(answer_scores):
        return "all_correct"
    return "routing_sensitive"


def categorize(row: dict, answer_oracle: list[str], evidence_oracle: list[str], answer_scores: dict[str, float]) -> list[str]:
    categories: list[str] = []
    policy = row["policy"]
    selected = row["selected_retriever"]
    if policy == "llm_router":
        if selected == "graph" and "vector" in answer_oracle and "graph" not in answer_oracle:
            categories.append("A")
        if selected == "vector" and "vector" not in answer_oracle and ({"graph", "pageindex"} & set(answer_oracle)):
            categories.append("B")
        if evidence_oracle and selected not in evidence_oracle and row["answer_score"] > 0:
            categories.append("C")
        if evidence_oracle and selected in evidence_oracle and row["answer_score"] == 0:
            categories.append("D")
    if policy == "agent" and row["retry_count"] > 0:
        initial = row["initial_retriever"]
        if answer_scores[initial] == 0 and row["answer_score"] > 0:
            categories.append("E")
        if row["answer_score"] <= answer_scores[initial]:
            categories.append("F")
    return categories
