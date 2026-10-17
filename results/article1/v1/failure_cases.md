# Failure cases

Categories are assigned automatically by src/evaluation/failures.py. Up to three examples each.

## A. LLM Router chose graph, but vector was in the answer oracle (graph was not)

Total: 0

## B. LLM Router chose vector, but graph or pageindex was in the answer oracle (vector was not)

Total: 0

## C. LLM Router missed the evidence oracle, but the final answer was correct

Total: 0

## D. LLM Router chose an evidence-oracle retriever, but the final answer was wrong

Total: 6

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
- Router reasoning: The question asks for a specific sensor associated with a person, which likely involves understanding relationships between entities (the person and the company). The graph strategy is best suited for this as it can leverage the connections between entities to find the relevant information.
- Answer oracle: []; evidence oracle: ['graph']
- Per-retriever answer scores: bm25=0, vector=0, graph=0, pageindex=0
- Retrieved units: ['chain03_researcher#c0', 'chain03_partnership#c0', 'chain03_product#c0']
- Answer (score 0): The documents do not contain this information.

### q21 (multi_hop, policy=llm_router)

- Query: When a Northstar alert fires, which team starts the investigation?
- Initial / final retriever: pageindex / pageindex (confidence 0.9)
- Router reasoning: The question is specific and likely requires a direct reference to a policy or procedure document that outlines the response to a Northstar alert. The pageindex strategy is best suited for this as it can navigate through structured documents like handbooks or policies to find the relevant section that directly answers the question.
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

- Agent trace: pageindex: sufficient=False -> bm25 (The retrieved context does not provide any information about the conditions or requirements for closing a restore ticket. It discusses postmortems, incident severity levels, and on-call rotations, but none of these sections mention restore tickets or their closure process. Therefore, the context is insufficient to answer the question.); bm25: sufficient=True -> none (The retrieved context clearly states the conditions under which a restore ticket can be closed, specifically mentioning that it can only be closed after the service owner has verified the checksums of the restored data and has run read validation against it for at least 24 hours. Therefore, the context is sufficient to answer the question.)

## F. Agent retried without improving the answer (extra cost only)

Total: 4

### q19 (multi_hop, policy=agent)

- Query: Which sensor was developed by the company that Dr. Elena Vasquez is connected to?
- Initial / final retriever: graph / pageindex (confidence 0.9)
- Router reasoning: The question requires identifying a specific sensor associated with a person, which suggests a need for understanding relationships and entities. The graph strategy is best suited for this as it can leverage the connections between Dr. Elena Vasquez and the company to find relevant information about the sensor.
- Answer oracle: []; evidence oracle: ['graph']
- Per-retriever answer scores: bm25=0, vector=0, graph=0, pageindex=0
- Retrieved units: ['chain01_researcher', 'chain01_product', 'chain02_researcher', 'chain02_product']
- Answer (score 0): The documents do not contain this information.

- Agent trace: graph: sufficient=False -> bm25 (The context mentions that Acmetric Systems developed the L7 LiDAR sensor, but it does not explicitly state that Dr. Elena Vasquez is connected to Acmetric Systems or that she is involved with the L7 LiDAR sensor. Therefore, the context does not provide a clear answer to the question about which sensor is connected to Dr. Elena Vasquez.); bm25: sufficient=False -> pageindex (The context does not provide a direct connection between Dr. Elena Vasquez and any specific sensor developed by a company. While it mentions two sensors developed by Acmetric Systems and Borealis Dynamics, it does not indicate which, if any, of these companies Dr. Vasquez is associated with. Therefore, the retrieved context is insufficient to answer the question.)

### q21 (multi_hop, policy=agent)

- Query: When a Northstar alert fires, which team starts the investigation?
- Initial / final retriever: pageindex / graph (confidence 0.9)
- Router reasoning: The question is specific and likely requires a direct reference to a policy or procedure document that outlines the response to a Northstar alert. The pageindex strategy is best suited for this as it can navigate through structured documents like handbooks or policies to find the relevant section that directly answers the question.
- Answer oracle: []; evidence oracle: ['bm25', 'vector', 'graph', 'pageindex']
- Per-retriever answer scores: bm25=0, vector=0, graph=0, pageindex=0
- Retrieved units: ['signals_terminology_note#c0', 'atlas_05_error_catalog#c0', 'atlas_01_signal_registry#c0', 'atlas_02_alert_routing#c0']
- Answer (score 0): The documents do not contain this information.

- Agent trace: pageindex: sufficient=False -> bm25 (The context mentions that Northstar alerts are routed to Atlas Relay, which handles deduplication and creates the investigation queue. However, it does not specify which team is responsible for starting the investigation. Therefore, the context does not provide a clear answer to the question.); bm25: sufficient=False -> graph (The retrieved context does not provide any information about which team starts the investigation when a Northstar alert fires. It discusses the routing of alerts and the investigation process but does not specify the responsible team. Therefore, the context is insufficient to answer the question.)

### q23 (multi_hop, policy=agent)

- Query: A responder finds error code E-74. Which team is responsible for the investigation through recovery confirmation?
- Initial / final retriever: pageindex / bm25 (confidence 0.9)
- Router reasoning: The question specifically asks for a team responsible for investigating a particular error code, which suggests that the answer is likely to be found in a structured document or policy that outlines responsibilities. The pageindex strategy is best suited for this as it can navigate through document titles and section headings to find the relevant section that likely contains this information.
- Answer oracle: ['pageindex']; evidence oracle: ['pageindex']
- Per-retriever answer scores: bm25=0, vector=0, graph=0, pageindex=1
- Retrieved units: ['delta_05_error_catalog#c0', 'atlas_05_error_catalog#c0', 'beacon_05_error_catalog#c0', 'comet_05_error_catalog#c0']
- Answer (score 0): The documents do not contain this information.

- Agent trace: pageindex: sufficient=False -> graph (The context provides information about the error code E-74 and its implications, but it does not directly state which team is responsible for the investigation through recovery confirmation. However, the last document mentions that the Payments Monitoring Team is responsible for starting incident investigations and confirming recovery for the Delta Gateway service, which is related to the Tidepool alerts. Therefore, while the context does not explicitly answer the question, it implies that the Payments Monitoring Team is the responsible party.); graph: sufficient=False -> bm25 (The retrieved context does not provide information about which team is responsible for investigating error code E-74. It mentions that a first responder checks where the signal is routed but does not specify the responsible team or service. Therefore, the context is insufficient to answer the question.)
