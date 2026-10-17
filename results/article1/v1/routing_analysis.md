# Routing analysis

## Per-retriever answer accuracy (base runs)

Cell = answer accuracy / mean evidence recall.

| query_type | bm25 | vector | graph | pageindex |
|---|---|---|---|---|
| keyword_exact | 1.00 / ev 1.00 | 1.00 / ev 1.00 | 1.00 / ev 1.00 | 1.00 / ev 1.00 |
| semantic_paraphrase | 0.83 / ev 0.83 | 1.00 / ev 1.00 | 0.17 / ev 0.17 | 1.00 / ev 1.00 |
| relationship | 1.00 / ev 1.00 | 1.00 / ev 1.00 | 0.83 / ev 0.83 | 1.00 / ev 1.00 |
| multi_hop | 0.00 / ev 0.50 | 0.00 / ev 0.56 | 0.00 / ev 0.61 | 0.17 / ev 0.61 |
| reasoning_heavy | 1.00 / ev 1.00 | 0.67 / ev 1.00 | 0.50 / ev 0.67 | 0.83 / ev 1.00 |
| long_doc_navigation | 1.00 / ev 1.00 | 1.00 / ev 1.00 | 0.50 / ev 0.83 | 0.67 / ev 0.83 |
| all | 0.81 / ev 0.89 | 0.78 / ev 0.93 | 0.50 / ev 0.69 | 0.78 / ev 0.91 |

## Routing scope of queries

| scope | queries |
|---|---|
| all_correct | 15 |
| none_correct | 5 |
| routing_sensitive | 16 |

| query_type | routing_sensitive | all_correct | none_correct |
|---|---|---|---|
| keyword_exact | 0 | 6 | 0 |
| semantic_paraphrase | 5 | 1 | 0 |
| relationship | 1 | 5 | 0 |
| multi_hop | 1 | 0 | 5 |
| reasoning_heavy | 4 | 2 | 0 |
| long_doc_navigation | 5 | 1 | 0 |

## llm_router: query_type x selected retriever

| query_type | bm25 | vector | graph | pageindex |
|---|---|---|---|---|
| keyword_exact | 2 | 1 | 1 | 2 |
| semantic_paraphrase | 0 | 0 | 0 | 6 |
| relationship | 0 | 0 | 1 | 5 |
| multi_hop | 0 | 0 | 2 | 4 |
| reasoning_heavy | 0 | 0 | 0 | 6 |
| long_doc_navigation | 0 | 0 | 0 | 6 |

## llm_router: answer-oracle set x selected retriever (routing-sensitive queries)

| oracle set | bm25 | vector | graph | pageindex |
|---|---|---|---|---|
| bm25 | 0 | 0 | 0 | 1 |
| bm25+graph+pageindex | 0 | 0 | 0 | 1 |
| bm25+vector+graph | 0 | 0 | 0 | 2 |
| bm25+vector+pageindex | 0 | 0 | 0 | 10 |
| pageindex | 0 | 0 | 0 | 1 |
| vector+pageindex | 0 | 0 | 0 | 1 |

## rule_router: query_type x selected retriever

| query_type | bm25 | vector | graph | pageindex |
|---|---|---|---|---|
| keyword_exact | 6 | 0 | 0 | 0 |
| semantic_paraphrase | 0 | 6 | 0 | 0 |
| relationship | 0 | 1 | 5 | 0 |
| multi_hop | 2 | 0 | 4 | 0 |
| reasoning_heavy | 1 | 2 | 3 | 0 |
| long_doc_navigation | 0 | 0 | 0 | 6 |

## rule_router: answer-oracle set x selected retriever (routing-sensitive queries)

| oracle set | bm25 | vector | graph | pageindex |
|---|---|---|---|---|
| bm25 | 0 | 1 | 0 | 0 |
| bm25+graph+pageindex | 0 | 0 | 1 | 0 |
| bm25+vector+graph | 0 | 0 | 0 | 2 |
| bm25+vector+pageindex | 1 | 4 | 2 | 3 |
| pageindex | 1 | 0 | 0 | 0 |
| vector+pageindex | 0 | 1 | 0 | 0 |

## LLM router confidence

| subset | n | mean confidence |
|---|---|---|
| routing correct (sensitive) | 13 | 0.90 |
| routing wrong (sensitive) | 3 | 0.87 |
| wrong with confidence >= 0.8 | 3 |  |

## LLM router: evidence-oracle routing vs answer correctness

Against the answer oracle, routing correctness and answer correctness coincide by construction for a single-shot router, so the evidence oracle is used here.

|  | answer correct | answer wrong |
|---|---|---|
| chose evidence-oracle retriever | 28 | 6 |
| missed evidence oracle | 0 | 2 |
