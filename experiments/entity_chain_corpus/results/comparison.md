# Entity-chain corpus: Vector vs Graph baseline

The first corpus in this series on which Graph retrieval outperforms Vector
retrieval.

Both systems used the frozen 12-question dataset at document relevance and
`top_k=5`. The corpus contains 12 one-chunk fictional documents forming four
independent three-document chains (researcher → project → company → product).
The `multi_hop` question names only the researcher, so neither the project nor
the company appears in the query, and `relevant_docs` lists all three documents
of the chain. The `relationship` and `factual` questions are one-hop controls
that name their anchor entity directly; they exist to show whether any graph
advantage is specific to the chained question shape.

| Scope | Metric | Vector | Graph auto v2 |
| --- | --- | ---: | ---: |
| aggregate | Recall@1 | 0.694 | 0.778 |
| aggregate | Recall@3 | 0.833 | 1.000 |
| aggregate | Recall@5 | 0.889 | 1.000 |
| aggregate | MRR | 0.875 | 1.000 |
| aggregate | mean latency (ms) | 247.400 | 0.114 |
| multi_hop | Recall@1 | 0.083 | 0.333 |
| multi_hop | Recall@3 | 0.500 | 1.000 |
| multi_hop | Recall@5 | 0.667 | 1.000 |
| multi_hop | MRR | 0.625 | 1.000 |
| relationship | Recall@5 | 1.000 | 1.000 |
| factual | Recall@5 | 1.000 | 1.000 |

`multi_hop` questions have three relevant documents, so 0.333 is the ceiling
for Recall@1 on that category. Graph reached that ceiling on all four
questions; Vector reached it on one.

## Observed mechanism

On every `multi_hop` question Graph returned exactly the three required
documents and nothing else. Lexical seed matching found the single researcher
node, and depth-2 traversal reached the project node at distance 1 and the
company node at distance 2. The product document was collected through the
company node's provenance rather than through the product node, which sits at
distance 3 and was never visited. Depth 2 was the parameter already frozen by
the earlier runs and was not tuned for this corpus.

Vector never retrieved the middle partnership document for any of the four
chains. That document shares almost no vocabulary with a question anchored on
the researcher. Vector retrieved the researcher document and usually some
product document, but the query carries no signal to choose the correct
chain's product document over the other three.

## Artifacts and caveats

- The per-document disclaimer header used to keep every document above the
  50-character chunk filter was itself extracted as a `document` entity in
  three of the four product documents, bridging chains 1-3 into one connected
  component (19 nodes, 16 edges, 3 components where 4 were intended). It sits
  at distance 4 from any researcher seed and distance 2 from a company seed,
  so it did not displace a required document in this run, but it is corpus
  design contamination, not a property of the corpus being modelled.
- Vector ranked `chain04_03_product.txt` first on all four `multi_hop`
  questions regardless of which researcher was named. This is unexplained and
  worth a separate look.
- The four chains are generated from one template with substituted proper
  nouns. The result shows that graph traversal recovers a chain whose
  intermediate entities are absent from the query; it does not show that this
  holds for natural prose.
- 12 questions across three categories is four questions per category. These
  numbers are a demonstration of a mechanism, not a measurement with
  meaningful statistical power.
- The frozen relation vocabulary has no `develops` relation, so
  company-to-product edges were labelled `responsible_for`. Retrieval scoring
  ignores relation labels, so this affects graph semantics but not any metric
  reported here.

Graph construction used `gpt-4o-mini`, temperature 0, 12 input chunks, with
depth 2 and at most five lexical seed entities during retrieval. No retrieval
code, parameter, or dataset was changed after observing either result. The raw
graph, per-question outputs, and extraction cache are retained locally and are
ignored because they contain material derived from source chunks.
