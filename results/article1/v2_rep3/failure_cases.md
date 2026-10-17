# Failure cases

Categories are assigned automatically by src/evaluation/failures.py. Up to three examples each.

## A. LLM Router chose graph, but vector was in the answer oracle (graph was not)

Total: 0

## B. LLM Router chose vector, but graph or pageindex was in the answer oracle (vector was not)

Total: 0

## C. LLM Router missed the evidence oracle, but the final answer was correct

Total: 0

## D. LLM Router chose an evidence-oracle retriever, but the final answer was wrong

Total: 7

### q19 (multi_hop, policy=llm_router)

- Query: Which sensor was developed by the company that Dr. Elena Vasquez is connected to?
- Initial / final retriever: graph / graph (confidence 0.9)
- Router reasoning: The question requires identifying a specific sensor associated with a person, which suggests a need for understanding relationships and entities. The graph strategy is best suited for this as it can leverage the connections between Dr. Elena Vasquez and the company to find relevant information about the sensor.
- Answer oracle: []; evidence oracle: ['graph']
- Per-retriever answer scores: bm25=0, vector=0, graph=0, pageindex=0
- Retrieved units: ['chain01_researcher#c0', 'chain01_partnership#c0', 'chain01_product#c0']
- Answer (score 0): The documents do not contain this information.

### q20 (multi_hop, policy=llm_router)

- Query: Which sensor was developed by the company that Dr. Hana Lindqvist is connected to?
- Initial / final retriever: graph / graph (confidence 0.9)
- Router reasoning: The question asks for a specific sensor associated with a person, which suggests that a knowledge-graph search would be most effective. This strategy can leverage the relationships between entities (like Dr. Hana Lindqvist and the company) to find relevant information about the sensor.
- Answer oracle: []; evidence oracle: ['graph']
- Per-retriever answer scores: bm25=0, vector=0, graph=0, pageindex=0
- Retrieved units: ['chain03_researcher#c0', 'chain03_partnership#c0', 'chain03_product#c0']
- Answer (score 0): The documents do not contain this information.

### q21 (multi_hop, policy=llm_router)

- Query: When a Northstar alert fires, which team starts the investigation?
- Initial / final retriever: pageindex / pageindex (confidence 0.9)
- Router reasoning: The question is looking for specific information about a process related to alerts, which is likely to be found in structured documents or policies. The pageindex strategy is best suited for this as it can navigate through document titles and headings to find the relevant section that outlines the investigation process for Northstar alerts.
- Answer oracle: []; evidence oracle: ['bm25', 'vector', 'graph', 'pageindex']
- Per-retriever answer scores: bm25=0, vector=0, graph=0, pageindex=0
- Retrieved units: ['atlas_02_alert_routing']
- Answer (score 0): The documents do not contain this information.

## E. Agent recovered from a wrong initial routing by retrying

Total: 1

### q31 (long_doc_navigation, policy=agent)

- Query: According to the Platform Operations Handbook, what has to happen before a restore ticket can be closed?
- Initial / final retriever: pageindex / bm25 (confidence 0.9)
- Router reasoning: The question specifically refers to a structured document, the Platform Operations Handbook, and asks for a specific procedural detail. The pageindex strategy is most suitable here as it can navigate through the document's sections and headings to find the relevant information directly related to the question.
- Answer oracle: ['bm25', 'vector', 'graph']; evidence oracle: ['bm25', 'vector', 'graph']
- Per-retriever answer scores: bm25=1, vector=1, graph=1, pageindex=0
- Retrieved units: ['long_operations_handbook#c8', 'long_operations_handbook#c0', 'long_operations_handbook#c7', 'atlas_03_service_ownership#c0']
- Answer (score 1): Before a restore ticket can be closed, the service owner must verify the checksums of the restored data and run read validation against it for at least 24 hours. If the restore was performed due to an incident, the restore ticket must also be linked to the postmortem.

- Agent trace: pageindex: sufficient=False -> bm25 (The retrieved context does not provide any information about the process or requirements for closing a restore ticket. It discusses postmortems, incident severity levels, on-call rotations, and escalation procedures, but none of these sections mention the specific conditions or actions needed to close a restore ticket.); bm25: sufficient=True -> none (The retrieved context clearly states that a restore ticket may be closed only after the service owner has verified the checksums of the restored data and has run read validation against it for at least 24 hours. This directly answers the question about what has to happen before a restore ticket can be closed.)

## F. Agent retried without improving the answer (extra cost only)

Total: 2

### q21 (multi_hop, policy=agent)

- Query: When a Northstar alert fires, which team starts the investigation?
- Initial / final retriever: pageindex / graph (confidence 0.9)
- Router reasoning: The question is looking for specific information about a process related to alerts, which is likely to be found in structured documents or policies. The pageindex strategy is best suited for this as it can navigate through document titles and headings to find the relevant section that outlines the investigation process for Northstar alerts.
- Answer oracle: []; evidence oracle: ['bm25', 'vector', 'graph', 'pageindex']
- Per-retriever answer scores: bm25=0, vector=0, graph=0, pageindex=0
- Retrieved units: ['signals_terminology_note#c0', 'atlas_01_signal_registry#c0', 'atlas_02_alert_routing#c0', 'atlas_05_error_catalog#c0']
- Answer (score 0): The documents do not contain this information.

- Agent trace: pageindex: sufficient=False -> bm25 (The context mentions that Northstar alerts are routed to Atlas Relay, which creates the investigation queue, but it does not specify which team starts the investigation. Therefore, the context does not provide a clear answer to the question.); bm25: sufficient=False -> graph (The retrieved context does not explicitly state which team starts the investigation when a Northstar alert fires. It mentions that Northstar alerts are routed to Atlas Relay and that a first responder checks where the signal is routed to start the investigation, but it does not specify which team that first responder belongs to or which team is responsible for the investigation itself.)

### q23 (multi_hop, policy=agent)

- Query: A responder finds error code E-74. Which team is responsible for the investigation through recovery confirmation?
- Initial / final retriever: graph / bm25 (confidence 0.85)
- Router reasoning: The question specifically asks for information related to an error code and the team responsible for investigating it. The graph strategy is likely the best choice here, as it can leverage the relationships between entities (like error codes and teams) to find the relevant information, which may not be directly stated in the text but can be inferred through connections.
- Answer oracle: []; evidence oracle: ['pageindex']
- Per-retriever answer scores: bm25=0, vector=0, graph=0, pageindex=0
- Retrieved units: ['delta_05_error_catalog#c0', 'atlas_05_error_catalog#c0', 'beacon_05_error_catalog#c0', 'comet_05_error_catalog#c0']
- Answer (score 0): The documents do not contain this information.

- Agent trace: graph: sufficient=False -> pageindex (The retrieved context provides information about error code E-74, indicating that it relates to input latency on Tidepool. However, it does not specify which team is responsible for the investigation or recovery confirmation. The context mentions that a first responder checks where the signal is routed to start the investigation, but it does not clarify the responsible team. Therefore, the context is insufficient to answer the question about which team is responsible for the investigation.); pageindex: sufficient=False -> bm25 (The context does not explicitly state which team is responsible for investigating error code E-74. It mentions that a first responder checks where the signal is routed but does not link this to the Payments Monitoring Team's responsibilities. Therefore, the retrieved context is insufficient to answer the question about which team is responsible for the investigation through recovery confirmation.)
