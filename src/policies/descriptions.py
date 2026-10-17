"""Retriever descriptions shown to the LLM router and the agent.

They describe mechanisms only. No query type labels or dataset metadata are exposed.
"""

RETRIEVER_DESCRIPTIONS = {
    "bm25": "Lexical keyword search (BM25) over text chunks. Matches exact words, identifiers, codes, and rare terms; does not understand synonyms.",
    "vector": "Dense semantic search over text chunks using embeddings. Finds passages with similar meaning even when wording differs; can confuse near-identical identifiers.",
    "graph": "Knowledge-graph search. An LLM extracted entities and relations from every chunk; the search starts from entity names that appear literally in the question and follows relations up to two hops, returning the source chunks.",
    "pageindex": "Table-of-contents navigation. An LLM reads document titles and section headings and picks the sections most likely to contain the answer, returning whole sections.",
}

CORPUS_DESCRIPTION = (
    "The collection contains short internal notes, HR and expense policies, technical reference "
    "pages, and a few long structured documents such as a handbook and a contract."
)


def describe_retrievers(names: list[str]) -> str:
    return "\n".join(f"- {name}: {RETRIEVER_DESCRIPTIONS[name]}" for name in names)
