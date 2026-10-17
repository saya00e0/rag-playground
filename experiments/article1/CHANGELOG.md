# article1 corpus and dataset changelog

## v2 (2026-10-06): remove negative-scope sentences from multi-hop documents

**Why.** In the v1 run (`results/article1/v1/`), 5 of the 6 `multi_hop` queries were answered
incorrectly by every retriever, so they contributed nothing to the routing analysis.
On q19 and q20, graph retrieval returned all three chain documents (evidence recall 1.0),
yet the generator still replied "The documents do not contain this information." Each chain
document carried a sentence such as "This note does not record her employer or the
products she works on." These sentences were inherited from the Japanese entity-chain
corpus, where they existed to block single-document shortcuts. They read as explicit
statements that the answer is absent, and they are a corpus artifact, not a property of
any retriever.

**Rule (fixed before the v2 run).** Delete every sentence of the form
"This <note|record|announcement|document|catalog> does not ..." from the corpus. Exactly
20 sentences match, all in multi-hop documents:

- `chain0N_researcher.md` (4): "This note does not record her/his employer or the products she/he works on."
- `chain0N_partnership.md` (4): "This record does not list the project's researchers or its deliverables."
- `chain0N_product.md` (4): "This announcement does not describe the sensor's customers or the research team behind it."
- `<program>_02_alert_routing.md` (4): "This document does not record which team operates the receiving service."
- `<program>_05_error_catalog.md` (4): "This catalog does not name the service or the responsible team."

**Unchanged.** Queries, gold answers, key facts, relevance labels, every other document
sentence (including "Approval authority is defined in a separate approval register." and
"The signal name does not indicate ..."), configuration values other than
`dataset_version` and `output_dir`, prompts, and code.

**Outcome (recorded after the v2 run).** The hypothesis was wrong. On q19 and q20, graph
retrieval again returned all three chain documents, and the generator again answered
"The documents do not contain this information." The refusal therefore does not come from
the removed sentences. It most likely comes from the generator declining to bridge the
hops implied by "connected to". `multi_hop` went from 5 to 4 none-correct queries (q22
pageindex flipped 0 -> 1). In addition, q36 pageindex flipped 0 -> 1 although none of its
documents changed, which shows run-to-run variance at temperature 0. The v2 corpus is kept
because the rule was fixed in advance; v1 and v2 results are both preserved.

**Known v1 limitations not addressed here.** All six `keyword_exact` queries were answered
correctly by every retriever. Signal-family multi-hop queries lose intermediate documents
at `retrieval_top_k = 4`. Both are left as they are, because changing them would mean
tuning the dataset to the results.

## v1 (2026-10-06): initial corpus and dataset

44 fictional English documents and 36 queries (6 query types × 6). Corpus sha256 and
dataset sha256 are recorded in `results/article1/v1/run_metadata.json`.
