# Hard multi-hop corpus: Vector vs Graph baseline

Both systems used the frozen 24-question dataset at document relevance and
`top_k=5`. The fictional corpus contains 32 one-chunk documents. Multi-hop
questions require a two- or three-document chain and do not name the
intermediate service or responsible person in the question.

| Scope | Metric | Vector | Graph auto v2 |
| --- | --- | ---: | ---: |
| aggregate | Recall@1 | 0.562 | 0.285 |
| aggregate | Recall@3 | 0.743 | 0.299 |
| aggregate | Recall@5 | 0.743 | 0.319 |
| aggregate | MRR | 0.847 | 0.425 |
| factual | Recall@5 | 1.000 | 1.000 |
| multi_hop | Recall@5 | 0.486 | 0.222 |
| relationship | Recall@5 | 1.000 | 0.125 |

Graph construction used `gpt-4o-mini`, temperature 0, depth 2, and at most
five lexical seed entities. The graph has 32 nodes and 57 edges. This is a
measured baseline; retrieval code, parameters, and the dataset were not tuned
after observing the Vector result.
