# Large synthetic corpus: Vector vs Graph baseline

Both systems were evaluated against the frozen 60-question dataset at document
relevance and `top_k=5`. The corpus contains 100 documents, chunked into 196
chunks with the repository's 500-character size and 50-character overlap.

| Scope | Metric | Vector | Graph auto v2 |
| --- | --- | ---: | ---: |
| aggregate | Recall@1 | 0.447 | 0.081 |
| aggregate | Recall@3 | 0.758 | 0.342 |
| aggregate | Recall@5 | 0.906 | 0.458 |
| aggregate | MRR | 0.848 | 0.375 |
| factual | Recall@5 | 0.850 | 0.150 |
| factual | MRR | 0.718 | 0.067 |
| multi_hop | Recall@5 | 0.867 | 0.550 |
| multi_hop | MRR | 0.900 | 0.483 |
| relationship | Recall@5 | 1.000 | 0.675 |
| relationship | MRR | 0.925 | 0.577 |

Graph construction used `gpt-4o-mini`, temperature 0, at most 196 input
chunks, with depth 2 and at most five lexical seed entities during retrieval.
The graph has 221 nodes and 1,129 edges. Its raw graph, per-question retrieval
results, and extraction cache are retained locally but are ignored because they
contain extracted material derived from source chunks.

This is a measured baseline, not an optimization result. On this synthetic,
repeated-template corpus, Vector retrieval outperformed Graph retrieval in
every reported category.
