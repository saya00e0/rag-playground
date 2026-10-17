# Article notes: Can an LLM Actually Choose the Right Retrieval Strategy?

Source runs: three independent runs of corpus/dataset `article1-v2` (`results/article1/v2`,
`v2_rep2`, `v2_rep3`) plus the superseded `article1-v1` run (`results/article1/v1`).
Model `gpt-4o-mini`, temperature 0, seed 20261006, `text-embedding-3-small`, chunk 800/100,
top-k 4. 36 queries, 6 query types × 6. Total API spend for all runs: about $0.16.
Numbers below are the mean over the three v2 runs, with the range in brackets.

# Main finding

Asked to pick a retriever from the query alone, gpt-4o-mini sent about three in four
questions to the same strategy (LLM table-of-contents navigation), with ~0.9 confidence
whether it was right or wrong. It matched an always-vector baseline (0.78 vs 0.78) at
~4x the cost and ~3x the latency; adding a retry agent gained about one question in 36.

# Surprising findings

- **One strategy for everything.** The LLM router chose `pageindex` for 27–28 of 36
  queries in every run, including all six paraphrase, all six reasoning-heavy and five of
  six relationship questions. Its stated reasons repeat the same template: "the question is
  specific … pageindex can navigate structured documents … most efficient."
- **Confidence carries no signal.** On routing-sensitive queries, mean confidence was 0.90
  when the router picked an oracle retriever and 0.87–0.90 when it did not. Every wrong
  routing had confidence ≥ 0.85.
- **Knowing the query types did not help the rule router.** The keyword router was
  written by the same person who wrote the queries, and it maps query types to the
  "intuitive" retriever almost perfectly. It was still the worst policy in every run
  (0.69–0.72), below the always-vector baseline (0.78).
- **The "relationship → graph" intuition fails.** Graph retrieval was the weakest
  retriever overall (0.50). On paraphrased questions it usually returns nothing: 5 of 6
  queries contained no entity name that matched a graph node. When the LLM router did pick
  graph for "Which team is responsible for error code E-74?", reasoning that graph "can
  leverage the relationships between entities (like error codes and teams)", graph
  retrieved four error catalogs and the answer failed.
- **Retrieval found the evidence; generation refused.** On q19/q20 graph retrieval returned
  all three documents of the researcher → project → company → product chain, and the
  generator still answered "The documents do not contain this information." Removing the
  "this document does not record …" sentences (v1 → v2) did not change this; that
  hypothesis was falsified (see `experiments/article1/CHANGELOG.md`).
- **Navigation can miss a section whose heading names the topic.** For "what has to happen
  before a restore ticket can be closed?", the TOC navigator picked Postmortems, Severity,
  On-call and Capacity, and skipped the section titled "Backup and Restore".

# Numbers worth publishing

| policy | answer accuracy | routing acc. (routing-sensitive) | mean cost / query | mean latency | retrievals |
|---|---|---|---|---|---|
| fixed vector | 0.778 [0.778–0.778] | 0.81 [0.75–0.87] | $0.00010 | 1.1 s | 1.00 |
| rule router | 0.704 [0.694–0.722] | 0.65 [0.62–0.67] | $0.00013 | 1.2 s | 1.00 |
| LLM router | 0.778 [0.750–0.806] | 0.81 [0.80–0.82] | $0.00038 | 3.7 s | 1.00 |
| agent (router + check + ≤2 switches) | 0.806 [0.778–0.833] | 0.88 [0.87–0.88] | $0.00052 | 5.4 s | 1.14–1.19 |
| oracle (best retriever, after the fact) | 0.861 [0.833–0.889] | 1.00 | — | — | 1.00 |

- Routing only matters for 15–17 of 36 queries. On 14–16 queries all four retrievers are
  correct, and on 4–6 none is.
- The router's choice is stable across runs: only 2 of 36 queries changed retriever.
- Per-retriever accuracy: BM25 0.78–0.81, vector 0.78, pageindex 0.75–0.83, graph 0.50.
- The agent retried on 3–4 queries per run and recovered exactly one (the same query, q31,
  every run). The other retries added cost without changing the answer.
- Run-to-run noise at temperature 0: 4 of 144 query × retriever answers flipped between
  runs. Policy differences of one or two queries are within this noise.

# Best failure cases

1. **q23, the intuitive graph pick** (`multi_hop`, LLM router → graph, confidence 0.85):
   "A responder finds error code E-74. Which team is responsible …?" Graph returned the
   error catalogs of all four programs; only pageindex answered correctly.
2. **q31, the one recovery** (agent): pageindex chose four wrong handbook sections; the
   sufficiency check said "nothing about closing a restore ticket"; switching to BM25
   found the exact sentence. This is the best illustration of when retry helps.
3. **q19, right evidence, no answer**: graph returned exactly the three chain documents. The
   generator refused, and in v1 the agent's sufficiency check also judged the context
   insufficient ("does not explicitly state that Dr. Elena Vasquez is connected"). The
   checker shares the generator's blind spot.
4. **q28, right section, wrong reasoning**: pageindex retrieved the equipment policy, and
   the answer still concluded "No" for an 8 GB laptop at 30 months, misapplying the
   early-replacement rule.

# Interpretation

- On this corpus the router's job is mostly easy or impossible. Fewer than half the
  queries are routing-sensitive, so the ceiling for any router over a fixed baseline is
  small (oracle 0.86 vs fixed 0.78, about 3 queries).
- The LLM router behaves like a prior over strategy names, not a per-query judgment. It
  prefers the description that sounds most capable. That happened to be harmless here
  because pageindex is roughly as accurate as vector on this corpus. It would not be
  harmless where the favoured strategy is weak.
- Self-reported confidence cannot be used to decide when to fall back or retry.
- Failures concentrate where no single-shot retriever plus the generator succeeds
  (multi-hop). That is a generation or composition problem that routing cannot fix.

# What we cannot conclude

- Anything about routing in general. This is one small synthetic corpus (44 documents),
  36 queries, one model (gpt-4o-mini), and one prompt for the router. The same person wrote
  the corpus, queries, rules and retriever descriptions.
- That the LLM router or the agent is better or worse than fixed vector. The differences are
  one or two queries, inside the observed run-to-run noise.
- Whether the pageindex preference comes from the model or from the wording of the
  strategy descriptions; prompt sensitivity was not tested.
- Anything about the real PageIndex library. A simplified single-call TOC navigator was used.
- Human-level answer quality. Scores come from an LLM judge against gold key facts and
  were not human-validated.
- Anything about Jev (TypeSafe AI). It was not run.

# Next experiment

For "My RAG Agent Can Search Again. But Does That Actually Help?":

- H1: retry helps only for *navigation misses*, where the first retriever returns
  plausible but wrong sections (q31), and not for composition failures (q19–q24).
- H2: the sufficiency checker inherits the generator's blind spots. When the context
  contains every hop but no hop is stated explicitly, it judges the context "insufficient"
  and switches away from the right evidence. Measure its precision and recall against the
  evidence oracle.
- H3: merging contexts across retries, instead of replacing them, converts some
  multi-hop failures into successes at a predictable token cost.
- H4: a non-generative decision model (Jev) gives a different confidence distribution than
  self-reported LLM confidence. Check whether its probabilities predict routing correctness.
