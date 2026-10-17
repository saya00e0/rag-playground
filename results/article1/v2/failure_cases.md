# Failure cases

Categories are assigned automatically by src/evaluation/failures.py. Up to three examples each.

## A. LLM Router chose graph, but vector was in the answer oracle (graph was not)

Total: 0

## B. LLM Router chose vector, but graph or pageindex was in the answer oracle (vector was not)

Total: 0

## C. LLM Router missed the evidence oracle, but the final answer was correct

Total: 0

## D. LLM Router chose an evidence-oracle retriever, but the final answer was wrong

Total: 4

### q19 (multi_hop, policy=llm_router)

- Query: Which sensor was developed by the company that Dr. Elena Vasquez is connected to?
- Initial / final retriever: graph / graph (confidence 0.9)
- Router reasoning: The question asks for a specific sensor developed by a company associated with a particular individual, Dr. Elena Vasquez. The graph strategy is most suitable here as it can leverage the relationships and entities extracted from the corpus to find connections between Dr. Vasquez and the company, leading to the identification of the sensor.
- Answer oracle: []; evidence oracle: ['graph']
- Per-retriever answer scores: bm25=0, vector=0, graph=0, pageindex=0
- Retrieved units: ['chain01_researcher#c0', 'chain01_partnership#c0', 'chain01_product#c0']
- Answer (score 0): The documents do not contain this information.

### q20 (multi_hop, policy=llm_router)

- Query: Which sensor was developed by the company that Dr. Hana Lindqvist is connected to?
- Initial / final retriever: graph / graph (confidence 0.9)
- Router reasoning: The question asks for a specific sensor associated with a person, which suggests that a knowledge-graph search would be most effective. This strategy can leverage the relationships and entities extracted from the corpus to find the relevant connections between Dr. Hana Lindqvist and the sensor developed by her company.
- Answer oracle: []; evidence oracle: ['graph']
- Per-retriever answer scores: bm25=0, vector=0, graph=0, pageindex=0
- Retrieved units: ['chain03_researcher#c0', 'chain03_partnership#c0', 'chain03_product#c0']
- Answer (score 0): The documents do not contain this information.

### q21 (multi_hop, policy=llm_router)

- Query: When a Northstar alert fires, which team starts the investigation?
- Initial / final retriever: pageindex / pageindex (confidence 0.9)
- Router reasoning: The question is looking for specific information about a process related to alerts, which is likely to be found in structured documents or policies. The pageindex strategy is best suited for this as it can navigate through document titles and section headings to find the relevant section that describes the investigation process for Northstar alerts.
- Answer oracle: []; evidence oracle: ['bm25', 'vector', 'graph', 'pageindex']
- Per-retriever answer scores: bm25=0, vector=0, graph=0, pageindex=0
- Retrieved units: ['atlas_02_alert_routing']
- Answer (score 0): The documents do not contain this information.

## E. Agent recovered from a wrong initial routing by retrying

Total: 1

### q31 (long_doc_navigation, policy=agent)

- Query: According to the Platform Operations Handbook, what has to happen before a restore ticket can be closed?
- Initial / final retriever: pageindex / bm25 (confidence 0.9)
- Router reasoning: The question specifically refers to a detail found in the Platform Operations Handbook, which is a structured document. Using the pageindex strategy will allow for efficient navigation through the document's sections and headings to locate the relevant information directly related to restore ticket closure.
- Answer oracle: ['bm25', 'vector', 'graph']; evidence oracle: ['bm25', 'vector', 'graph']
- Per-retriever answer scores: bm25=1, vector=1, graph=1, pageindex=0
- Retrieved units: ['long_operations_handbook#c8', 'long_operations_handbook#c0', 'long_operations_handbook#c7', 'atlas_03_service_ownership#c0']
- Answer (score 1): Before a restore ticket can be closed, the service owner must verify the checksums of the restored data and run read validation against it for at least 24 hours. If the restore was performed due to an incident, the restore ticket must also be linked to the postmortem.

- Agent trace: pageindex: sufficient=False -> bm25 (The retrieved context does not provide any information about the conditions or requirements for closing a restore ticket. It discusses postmortems, incident severity levels, on-call rotations, and capacity planning, none of which are directly related to the process of closing a restore ticket. Therefore, the context is insufficient to answer the question.); bm25: sufficient=True -> none (The retrieved context clearly states the conditions under which a restore ticket can be closed, specifically mentioning that it can only be closed after the service owner has verified the checksums of the restored data and has run read validation against it for at least 24 hours. Therefore, the context is sufficient to answer the question.)

## F. Agent retried without improving the answer (extra cost only)

Total: 3

### q21 (multi_hop, policy=agent)

- Query: When a Northstar alert fires, which team starts the investigation?
- Initial / final retriever: pageindex / graph (confidence 0.9)
- Router reasoning: The question is looking for specific information about a process related to alerts, which is likely to be found in structured documents or policies. The pageindex strategy is best suited for this as it can navigate through document titles and section headings to find the relevant section that describes the investigation process for Northstar alerts.
- Answer oracle: []; evidence oracle: ['bm25', 'vector', 'graph', 'pageindex']
- Per-retriever answer scores: bm25=0, vector=0, graph=0, pageindex=0
- Retrieved units: ['signals_terminology_note#c0', 'atlas_01_signal_registry#c0', 'atlas_02_alert_routing#c0', 'atlas_05_error_catalog#c0']
- Answer (score 0): The documents do not contain this information.

- Agent trace: pageindex: sufficient=False -> bm25 (The retrieved context mentions that Northstar alerts are routed to Atlas Relay, which creates the investigation queue. However, it does not specify which team is responsible for starting the investigation. Therefore, the context does not provide a clear answer to the question.); bm25: sufficient=False -> graph (The retrieved context does not explicitly state which team starts the investigation when a Northstar alert fires. It mentions that Northstar alerts are routed to Atlas Relay and that a first responder checks where the signal is routed to start the investigation, but it does not specify which team that first responder belongs to or which team is responsible for the investigation itself.)

### q24 (multi_hop, policy=agent)

- Query: Who must give final approval for a publication exception tied to error code E-52?
- Initial / final retriever: pageindex / graph (confidence 0.9)
- Router reasoning: The question is specific and likely requires precise information about a policy or procedure related to publication exceptions. The pageindex strategy is best suited for this as it can navigate through structured documents like handbooks or policies to find the relevant section that outlines the approval process for exceptions, which is likely to be organized in a clear manner.
- Answer oracle: []; evidence oracle: ['bm25', 'vector']
- Per-retriever answer scores: bm25=0, vector=0, graph=0, pageindex=0
- Retrieved units: ['signals_terminology_note#c0', 'beacon_05_error_catalog#c0', 'comet_05_error_catalog#c0', 'delta_05_error_catalog#c0']
- Answer (score 0): The documents do not contain this information.

- Agent trace: pageindex: sufficient=False -> bm25 (The retrieved context does not provide any information about who must give final approval for a publication exception related to error code E-52. It only describes the error code and the initial steps a first responder should take. Therefore, the context is insufficient to answer the question.); bm25: sufficient=False -> graph (The retrieved context does not mention who must give final approval for a publication exception tied to error code E-52. It provides information about other error codes and their respective approvers, but does not address E-52 specifically. Therefore, the context is insufficient to answer the question.)

### q23 (multi_hop, policy=agent)

- Query: A responder finds error code E-74. Which team is responsible for the investigation through recovery confirmation?
- Initial / final retriever: graph / bm25 (confidence 0.85)
- Router reasoning: The question specifically asks for information related to an error code (E-74) and the team responsible for investigating it. The graph strategy is likely to be the most effective here, as it can leverage the relationships between entities (like error codes and teams) to find the relevant information. This is more efficient than keyword matching or semantic similarity, which may not capture the specific relationship needed.
- Answer oracle: ['pageindex']; evidence oracle: ['pageindex']
- Per-retriever answer scores: bm25=0, vector=0, graph=0, pageindex=1
- Retrieved units: ['delta_05_error_catalog#c0', 'atlas_05_error_catalog#c0', 'beacon_05_error_catalog#c0', 'comet_05_error_catalog#c0']
- Answer (score 0): The documents do not contain this information.

- Agent trace: graph: sufficient=False -> pageindex (The retrieved context provides information about error code E-74, indicating that it relates to input latency on Tidepool. However, it does not specify which team is responsible for the investigation or recovery confirmation. The context mentions that a first responder checks where the signal is routed to start the investigation, but it does not clarify the responsible team. Therefore, the context is insufficient to answer the question about which team is responsible for the investigation.); pageindex: sufficient=False -> bm25 (The context provides information about the error code E-74 and its implications, but it does not directly state which team is responsible for the investigation through recovery confirmation. However, it does mention that the Payments Monitoring Team is responsible for starting incident investigations and confirming recovery for the Delta Gateway, which is related to the Tidepool alerts. Therefore, while the context does not explicitly answer the question, it implies that the Payments Monitoring Team is the responsible party.)
