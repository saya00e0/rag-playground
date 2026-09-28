# GraphRAG failure analysis

Frozen Graph auto v2; depth=2, maximum seed entities=5, top-k=5. This report does not modify retrieval, parameters, or the dataset.

Graph failures: 27. 5. traversal/ranking failure: 27

Multi-hop questions where Vector retrieved every required document without graph traversal: lq006, lq011, lq012, lq017, lq018, lq024, lq029, lq030, lq036, lq042, lq048, lq054, lq060

## lq003 — relationship

- Question: Aurora Gateway API または Aurora Catalog Service の技術問題は誰にエスカレーションしますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/01_aurora_02_team.txt`, `experiments/large_synthetic_corpus/docs/01_aurora_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/01_aurora_03_architecture.txt` (0.652)<br>`experiments/large_synthetic_corpus/docs/01_aurora_02_team.txt` (0.650)<br>`experiments/large_synthetic_corpus/docs/01_aurora_10_decision_log.txt` (0.604)<br>`experiments/large_synthetic_corpus/docs/01_aurora_07_operations.txt` (0.597)<br>`experiments/large_synthetic_corpus/docs/01_aurora_09_integration.txt` (0.589)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/01_aurora_07_operations.txt` (18.000); path: Aurora Catalog Service<br>`experiments/large_synthetic_corpus/docs/01_aurora_02_team.txt` (17.500); path: Aurora Catalog Service<br>`experiments/large_synthetic_corpus/docs/01_aurora_05_incident.txt` (16.667); path: Aurora Gateway API<br>`experiments/large_synthetic_corpus/docs/08_harbor_07_operations.txt` (16.667); path: Aurora Gateway API → メンテナンス<br>`experiments/large_synthetic_corpus/docs/01_aurora_10_decision_log.txt` (16.000); path: Aurora Catalog Service
- Detected seed entities: Aurora Catalog Service, Aurora Gateway API, Catalog Service, Gateway API, og Service
- Required documents missed by Graph: なし
- Vector retrieves all required evidence: yes
- Graph failure category: なし（必要文書をすべて取得）

## lq004 — relationship

- Question: Aurora Policy Service の公開前レビュー責任者は誰ですか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/01_aurora_02_team.txt`, `experiments/large_synthetic_corpus/docs/01_aurora_03_architecture.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/01_aurora_03_architecture.txt` (0.680)<br>`experiments/large_synthetic_corpus/docs/01_aurora_02_team.txt` (0.613)<br>`experiments/large_synthetic_corpus/docs/01_aurora_07_operations.txt` (0.596)<br>`experiments/large_synthetic_corpus/docs/01_aurora_05_incident.txt` (0.568)<br>`experiments/large_synthetic_corpus/docs/01_aurora_10_decision_log.txt` (0.567)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/01_aurora_01_overview.txt` (23.833); path: Aurora<br>`experiments/large_synthetic_corpus/docs/01_aurora_10_decision_log.txt` (20.000); path: Aurora Policy Service<br>`experiments/large_synthetic_corpus/docs/01_aurora_02_team.txt` (19.167); path: Aurora<br>`experiments/large_synthetic_corpus/docs/01_aurora_05_incident.txt` (16.500); path: Aurora Policy Service<br>`experiments/large_synthetic_corpus/docs/01_aurora_07_operations.txt` (16.500); path: Aurora Policy Service
- Detected seed entities: Aurora Policy Service, Service, Aurora
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/01_aurora_03_architecture.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq005 — multi_hop

- Question: Aurora 3.1 の公開前に必要な Aurora Catalog Service の負荷試験と Aurora Policy Service のアクセス規則レビューは、それぞれ誰が担当しますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/01_aurora_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/01_aurora_04_release.txt`, `experiments/large_synthetic_corpus/docs/01_aurora_08_acceptance.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/01_aurora_03_architecture.txt` (0.749)<br>`experiments/large_synthetic_corpus/docs/01_aurora_02_team.txt` (0.671)<br>`experiments/large_synthetic_corpus/docs/01_aurora_10_decision_log.txt` (0.647)<br>`experiments/large_synthetic_corpus/docs/01_aurora_04_release.txt` (0.643)<br>`experiments/large_synthetic_corpus/docs/01_aurora_10_decision_log.txt` (0.641)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/01_aurora_01_overview.txt` (20.833); path: Aurora 3.1<br>`experiments/large_synthetic_corpus/docs/01_aurora_10_decision_log.txt` (20.333); path: Aurora Catalog Service<br>`experiments/large_synthetic_corpus/docs/01_aurora_02_team.txt` (19.333); path: Aurora Catalog Service<br>`experiments/large_synthetic_corpus/docs/01_aurora_07_operations.txt` (18.167); path: Aurora Catalog Service<br>`experiments/large_synthetic_corpus/docs/01_aurora_08_acceptance.txt` (17.500); path: Aurora 3.1
- Detected seed entities: Aurora Catalog Service, Aurora Policy Service, Catalog Service, Aurora 3.1, アクセス規則レビュー
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/01_aurora_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/01_aurora_04_release.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq006 — multi_hop

- Question: Aurora Gateway API の証明書更新障害では、誰が一次対応し、誰が技術調査を担当し、なぜ Aurora Policy Service の臨時レビューが不要でしたか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/01_aurora_02_team.txt`, `experiments/large_synthetic_corpus/docs/01_aurora_05_incident.txt`, `experiments/large_synthetic_corpus/docs/01_aurora_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/01_aurora_05_incident.txt` (0.710)<br>`experiments/large_synthetic_corpus/docs/01_aurora_03_architecture.txt` (0.709)<br>`experiments/large_synthetic_corpus/docs/01_aurora_07_operations.txt` (0.649)<br>`experiments/large_synthetic_corpus/docs/01_aurora_02_team.txt` (0.637)<br>`experiments/large_synthetic_corpus/docs/01_aurora_07_operations.txt` (0.622)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/01_aurora_01_overview.txt` (25.333); path: Aurora<br>`experiments/large_synthetic_corpus/docs/01_aurora_02_team.txt` (20.667); path: Aurora<br>`experiments/large_synthetic_corpus/docs/01_aurora_05_incident.txt` (20.333); path: Aurora Gateway API<br>`experiments/large_synthetic_corpus/docs/01_aurora_10_decision_log.txt` (20.000); path: Aurora Policy Service<br>`experiments/large_synthetic_corpus/docs/01_aurora_07_operations.txt` (19.333); path: Aurora Gateway API
- Detected seed entities: Aurora Policy Service, Aurora Gateway API, Gateway API, Service, Aurora
- Required documents missed by Graph: なし
- Vector retrieves all required evidence: yes
- Graph failure category: なし（必要文書をすべて取得）

## lq009 — relationship

- Question: Borealis Gateway API または Borealis Catalog Service の技術問題は誰にエスカレーションしますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/02_borealis_02_team.txt`, `experiments/large_synthetic_corpus/docs/02_borealis_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/02_borealis_03_architecture.txt` (0.681)<br>`experiments/large_synthetic_corpus/docs/02_borealis_02_team.txt` (0.678)<br>`experiments/large_synthetic_corpus/docs/02_borealis_07_operations.txt` (0.653)<br>`experiments/large_synthetic_corpus/docs/02_borealis_09_integration.txt` (0.617)<br>`experiments/large_synthetic_corpus/docs/02_borealis_05_incident.txt` (0.608)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/02_borealis_02_team.txt` (17.500); path: Borealis Catalog Service<br>`experiments/large_synthetic_corpus/docs/02_borealis_01_overview.txt` (17.333); path: Borealis Catalog Service<br>`experiments/large_synthetic_corpus/docs/02_borealis_09_integration.txt` (16.333); path: Borealis Catalog Service<br>`experiments/large_synthetic_corpus/docs/02_borealis_04_release.txt` (14.833); path: Borealis Catalog Service<br>`experiments/large_synthetic_corpus/docs/08_harbor_07_operations.txt` (14.500); path: Borealis Gateway API → メンテナンス
- Detected seed entities: Borealis Catalog Service, Borealis Gateway API, Catalog Service, Gateway API, og Service
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/02_borealis_07_operations.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq010 — relationship

- Question: Borealis Policy Service の公開前レビュー責任者は誰ですか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/02_borealis_02_team.txt`, `experiments/large_synthetic_corpus/docs/02_borealis_03_architecture.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/02_borealis_03_architecture.txt` (0.673)<br>`experiments/large_synthetic_corpus/docs/02_borealis_02_team.txt` (0.650)<br>`experiments/large_synthetic_corpus/docs/02_borealis_05_incident.txt` (0.607)<br>`experiments/large_synthetic_corpus/docs/02_borealis_06_governance.txt` (0.591)<br>`experiments/large_synthetic_corpus/docs/02_borealis_10_decision_log.txt` (0.579)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/02_borealis_01_overview.txt` (20.500); path: Borealis<br>`experiments/large_synthetic_corpus/docs/02_borealis_02_team.txt` (19.333); path: Borealis<br>`experiments/large_synthetic_corpus/docs/02_borealis_04_release.txt` (19.333); path: Borealis Policy Service<br>`experiments/large_synthetic_corpus/docs/02_borealis_05_incident.txt` (18.833); path: Borealis<br>`experiments/large_synthetic_corpus/docs/02_borealis_06_governance.txt` (15.333); path: Borealis Policy Service
- Detected seed entities: Borealis Policy Service, Borealis, Service
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/02_borealis_03_architecture.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq011 — multi_hop

- Question: Borealis 3.2 の公開前に必要な Borealis Catalog Service の負荷試験と Borealis Policy Service のアクセス規則レビューは、それぞれ誰が担当しますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/02_borealis_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/02_borealis_04_release.txt`, `experiments/large_synthetic_corpus/docs/02_borealis_08_acceptance.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/02_borealis_03_architecture.txt` (0.785)<br>`experiments/large_synthetic_corpus/docs/02_borealis_02_team.txt` (0.703)<br>`experiments/large_synthetic_corpus/docs/02_borealis_04_release.txt` (0.666)<br>`experiments/large_synthetic_corpus/docs/02_borealis_08_acceptance.txt` (0.660)<br>`experiments/large_synthetic_corpus/docs/02_borealis_07_operations.txt` (0.660)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/02_borealis_01_overview.txt` (23.833); path: Borealis 3.2<br>`experiments/large_synthetic_corpus/docs/02_borealis_04_release.txt` (23.667); path: Borealis 3.2<br>`experiments/large_synthetic_corpus/docs/02_borealis_02_team.txt` (18.833); path: Borealis Catalog Service<br>`experiments/large_synthetic_corpus/docs/02_borealis_09_integration.txt` (16.833); path: Borealis Catalog Service<br>`experiments/large_synthetic_corpus/docs/08_harbor_07_operations.txt` (16.500); path: Catalog Service → 三浦陽
- Detected seed entities: Borealis Catalog Service, Borealis Policy Service, Catalog Service, Borealis 3.2, アクセス規則レビュー
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/02_borealis_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/02_borealis_08_acceptance.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq012 — multi_hop

- Question: Borealis Gateway API の証明書更新障害では、誰が一次対応し、誰が技術調査を担当し、なぜ Borealis Policy Service の臨時レビューが不要でしたか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/02_borealis_02_team.txt`, `experiments/large_synthetic_corpus/docs/02_borealis_05_incident.txt`, `experiments/large_synthetic_corpus/docs/02_borealis_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/02_borealis_03_architecture.txt` (0.723)<br>`experiments/large_synthetic_corpus/docs/02_borealis_05_incident.txt` (0.720)<br>`experiments/large_synthetic_corpus/docs/02_borealis_07_operations.txt` (0.678)<br>`experiments/large_synthetic_corpus/docs/02_borealis_02_team.txt` (0.658)<br>`experiments/large_synthetic_corpus/docs/02_borealis_07_operations.txt` (0.641)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/02_borealis_01_overview.txt` (22.000); path: Borealis<br>`experiments/large_synthetic_corpus/docs/02_borealis_05_incident.txt` (21.500); path: Borealis<br>`experiments/large_synthetic_corpus/docs/02_borealis_02_team.txt` (20.833); path: Borealis<br>`experiments/large_synthetic_corpus/docs/02_borealis_04_release.txt` (19.333); path: Borealis Policy Service<br>`experiments/large_synthetic_corpus/docs/02_borealis_07_operations.txt` (17.333); path: Borealis
- Detected seed entities: Borealis Policy Service, Borealis Gateway API, Gateway API, Borealis, Service
- Required documents missed by Graph: なし
- Vector retrieves all required evidence: yes
- Graph failure category: なし（必要文書をすべて取得）

## lq015 — relationship

- Question: Cirrus Gateway API または Cirrus Catalog Service の技術問題は誰にエスカレーションしますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/03_cirrus_02_team.txt`, `experiments/large_synthetic_corpus/docs/03_cirrus_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/03_cirrus_02_team.txt` (0.660)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_03_architecture.txt` (0.624)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_07_operations.txt` (0.610)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_09_integration.txt` (0.602)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_05_incident.txt` (0.582)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/03_cirrus_02_team.txt` (17.500); path: Cirrus Catalog Service<br>`experiments/large_synthetic_corpus/docs/03_cirrus_01_overview.txt` (17.333); path: Cirrus Catalog Service<br>`experiments/large_synthetic_corpus/docs/03_cirrus_07_operations.txt` (17.000); path: Cirrus Catalog Service<br>`experiments/large_synthetic_corpus/docs/03_cirrus_10_decision_log.txt` (14.667); path: Cirrus Catalog Service<br>`experiments/large_synthetic_corpus/docs/03_cirrus_09_integration.txt` (14.167); path: Cirrus Catalog Service
- Detected seed entities: Cirrus Catalog Service, Cirrus Gateway API, Catalog Service, Gateway API, og Service
- Required documents missed by Graph: なし
- Vector retrieves all required evidence: yes
- Graph failure category: なし（必要文書をすべて取得）

## lq016 — relationship

- Question: Cirrus Policy Service の公開前レビュー責任者は誰ですか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/03_cirrus_02_team.txt`, `experiments/large_synthetic_corpus/docs/03_cirrus_03_architecture.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/03_cirrus_03_architecture.txt` (0.700)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_02_team.txt` (0.661)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_05_incident.txt` (0.615)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_10_decision_log.txt` (0.597)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_02_team.txt` (0.596)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/03_cirrus_01_overview.txt` (20.667); path: Cirrus<br>`experiments/large_synthetic_corpus/docs/03_cirrus_07_operations.txt` (18.333); path: Cirrus<br>`experiments/large_synthetic_corpus/docs/03_cirrus_02_team.txt` (18.167); path: Cirrus<br>`experiments/large_synthetic_corpus/docs/03_cirrus_10_decision_log.txt` (17.167); path: Cirrus Policy Service<br>`experiments/large_synthetic_corpus/docs/03_cirrus_06_governance.txt` (16.333); path: Cirrus Policy Service
- Detected seed entities: Cirrus Policy Service, Service, Cirrus
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/03_cirrus_03_architecture.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq017 — multi_hop

- Question: Cirrus 3.3 の公開前に必要な Cirrus Catalog Service の負荷試験と Cirrus Policy Service のアクセス規則レビューは、それぞれ誰が担当しますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/03_cirrus_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/03_cirrus_04_release.txt`, `experiments/large_synthetic_corpus/docs/03_cirrus_08_acceptance.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/03_cirrus_03_architecture.txt` (0.737)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_02_team.txt` (0.680)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_04_release.txt` (0.661)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_09_integration.txt` (0.645)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_08_acceptance.txt` (0.643)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/03_cirrus_01_overview.txt` (23.833); path: Cirrus 3.3<br>`experiments/large_synthetic_corpus/docs/03_cirrus_02_team.txt` (18.667); path: Cirrus Catalog Service<br>`experiments/large_synthetic_corpus/docs/03_cirrus_10_decision_log.txt` (18.333); path: Cirrus Catalog Service<br>`experiments/large_synthetic_corpus/docs/03_cirrus_06_governance.txt` (16.833); path: Cirrus Catalog Service<br>`experiments/large_synthetic_corpus/docs/03_cirrus_08_acceptance.txt` (16.500); path: Cirrus 3.3
- Detected seed entities: Cirrus Catalog Service, Cirrus Policy Service, Catalog Service, アクセス規則レビュー, Cirrus 3.3
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/03_cirrus_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/03_cirrus_04_release.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq018 — multi_hop

- Question: Cirrus Gateway API の証明書更新障害では、誰が一次対応し、誰が技術調査を担当し、なぜ Cirrus Policy Service の臨時レビューが不要でしたか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/03_cirrus_02_team.txt`, `experiments/large_synthetic_corpus/docs/03_cirrus_05_incident.txt`, `experiments/large_synthetic_corpus/docs/03_cirrus_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/03_cirrus_05_incident.txt` (0.717)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_03_architecture.txt` (0.690)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_07_operations.txt` (0.652)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_02_team.txt` (0.643)<br>`experiments/large_synthetic_corpus/docs/03_cirrus_07_operations.txt` (0.638)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/03_cirrus_01_overview.txt` (22.167); path: Cirrus<br>`experiments/large_synthetic_corpus/docs/03_cirrus_07_operations.txt` (21.333); path: Cirrus<br>`experiments/large_synthetic_corpus/docs/03_cirrus_02_team.txt` (19.833); path: Cirrus<br>`experiments/large_synthetic_corpus/docs/03_cirrus_10_decision_log.txt` (17.167); path: Cirrus Policy Service<br>`experiments/large_synthetic_corpus/docs/03_cirrus_06_governance.txt` (16.833); path: Cirrus Gateway API
- Detected seed entities: Cirrus Policy Service, Cirrus Gateway API, Gateway API, Service, Cirrus
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/03_cirrus_05_incident.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq021 — relationship

- Question: Drift Gateway API または Drift Catalog Service の技術問題は誰にエスカレーションしますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/04_drift_02_team.txt`, `experiments/large_synthetic_corpus/docs/04_drift_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/04_drift_02_team.txt` (0.664)<br>`experiments/large_synthetic_corpus/docs/04_drift_03_architecture.txt` (0.659)<br>`experiments/large_synthetic_corpus/docs/04_drift_07_operations.txt` (0.605)<br>`experiments/large_synthetic_corpus/docs/04_drift_05_incident.txt` (0.590)<br>`experiments/large_synthetic_corpus/docs/04_drift_09_integration.txt` (0.590)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/04_drift_10_decision_log.txt` (22.333); path: Drift Catalog Service<br>`experiments/large_synthetic_corpus/docs/04_drift_05_incident.txt` (19.500); path: Drift Gateway API<br>`experiments/large_synthetic_corpus/docs/04_drift_07_operations.txt` (19.500); path: Drift Catalog Service<br>`experiments/large_synthetic_corpus/docs/04_drift_02_team.txt` (18.667); path: Drift Catalog Service<br>`experiments/large_synthetic_corpus/docs/04_drift_01_overview.txt` (18.167); path: Drift Catalog Service
- Detected seed entities: Drift Catalog Service, Drift Gateway API, Catalog Service, Gateway API, og Service
- Required documents missed by Graph: なし
- Vector retrieves all required evidence: yes
- Graph failure category: なし（必要文書をすべて取得）

## lq022 — relationship

- Question: Drift Policy Service の公開前レビュー責任者は誰ですか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/04_drift_02_team.txt`, `experiments/large_synthetic_corpus/docs/04_drift_03_architecture.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/04_drift_03_architecture.txt` (0.704)<br>`experiments/large_synthetic_corpus/docs/04_drift_02_team.txt` (0.646)<br>`experiments/large_synthetic_corpus/docs/04_drift_07_operations.txt` (0.622)<br>`experiments/large_synthetic_corpus/docs/04_drift_02_team.txt` (0.603)<br>`experiments/large_synthetic_corpus/docs/04_drift_10_decision_log.txt` (0.593)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/04_drift_01_overview.txt` (24.000); path: Drift<br>`experiments/large_synthetic_corpus/docs/04_drift_10_decision_log.txt` (21.833); path: Drift Policy Service<br>`experiments/large_synthetic_corpus/docs/04_drift_07_operations.txt` (21.000); path: Drift<br>`experiments/large_synthetic_corpus/docs/04_drift_02_team.txt` (20.333); path: Drift<br>`experiments/large_synthetic_corpus/docs/04_drift_05_incident.txt` (19.000); path: Drift
- Detected seed entities: Drift Policy Service, Service, Drift
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/04_drift_03_architecture.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq023 — multi_hop

- Question: Drift 3.4 の公開前に必要な Drift Catalog Service の負荷試験と Drift Policy Service のアクセス規則レビューは、それぞれ誰が担当しますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/04_drift_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/04_drift_04_release.txt`, `experiments/large_synthetic_corpus/docs/04_drift_08_acceptance.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/04_drift_03_architecture.txt` (0.783)<br>`experiments/large_synthetic_corpus/docs/04_drift_02_team.txt` (0.704)<br>`experiments/large_synthetic_corpus/docs/04_drift_10_decision_log.txt` (0.670)<br>`experiments/large_synthetic_corpus/docs/04_drift_04_release.txt` (0.650)<br>`experiments/large_synthetic_corpus/docs/04_drift_07_operations.txt` (0.634)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/04_drift_10_decision_log.txt` (23.667); path: Drift Catalog Service<br>`experiments/large_synthetic_corpus/docs/04_drift_07_operations.txt` (19.833); path: Drift Catalog Service<br>`experiments/large_synthetic_corpus/docs/04_drift_02_team.txt` (19.667); path: Drift Catalog Service<br>`experiments/large_synthetic_corpus/docs/04_drift_01_overview.txt` (18.333); path: Drift Catalog Service<br>`experiments/large_synthetic_corpus/docs/04_drift_05_incident.txt` (18.333); path: Drift Policy Service
- Detected seed entities: Drift Catalog Service, Drift Policy Service, Catalog Service, アクセス規則レビュー, og Service
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/04_drift_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/04_drift_04_release.txt`, `experiments/large_synthetic_corpus/docs/04_drift_08_acceptance.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq024 — multi_hop

- Question: Drift Gateway API の証明書更新障害では、誰が一次対応し、誰が技術調査を担当し、なぜ Drift Policy Service の臨時レビューが不要でしたか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/04_drift_02_team.txt`, `experiments/large_synthetic_corpus/docs/04_drift_05_incident.txt`, `experiments/large_synthetic_corpus/docs/04_drift_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/04_drift_03_architecture.txt` (0.728)<br>`experiments/large_synthetic_corpus/docs/04_drift_05_incident.txt` (0.721)<br>`experiments/large_synthetic_corpus/docs/04_drift_07_operations.txt` (0.665)<br>`experiments/large_synthetic_corpus/docs/04_drift_02_team.txt` (0.663)<br>`experiments/large_synthetic_corpus/docs/04_drift_07_operations.txt` (0.642)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/04_drift_05_incident.txt` (22.167); path: Drift Gateway API<br>`experiments/large_synthetic_corpus/docs/04_drift_10_decision_log.txt` (22.000); path: Drift Gateway API<br>`experiments/large_synthetic_corpus/docs/04_drift_07_operations.txt` (21.000); path: Drift Gateway API<br>`experiments/large_synthetic_corpus/docs/04_drift_01_overview.txt` (18.333); path: Drift Gateway API<br>`experiments/large_synthetic_corpus/docs/04_drift_02_team.txt` (18.333); path: Drift Gateway API
- Detected seed entities: Drift Policy Service, Drift Gateway API, Gateway API, Service, 証明書更新
- Required documents missed by Graph: なし
- Vector retrieves all required evidence: yes
- Graph failure category: なし（必要文書をすべて取得）

## lq027 — relationship

- Question: Ember Gateway API または Ember Catalog Service の技術問題は誰にエスカレーションしますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/05_ember_02_team.txt`, `experiments/large_synthetic_corpus/docs/05_ember_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/05_ember_02_team.txt` (0.613)<br>`experiments/large_synthetic_corpus/docs/05_ember_03_architecture.txt` (0.599)<br>`experiments/large_synthetic_corpus/docs/05_ember_09_integration.txt` (0.561)<br>`experiments/large_synthetic_corpus/docs/05_ember_07_operations.txt` (0.535)<br>`experiments/large_synthetic_corpus/docs/05_ember_10_decision_log.txt` (0.534)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/05_ember_02_team.txt` (19.167); path: Ember Catalog Service<br>`experiments/large_synthetic_corpus/docs/05_ember_09_integration.txt` (19.000); path: Ember Catalog Service<br>`experiments/large_synthetic_corpus/docs/05_ember_05_incident.txt` (18.667); path: Ember Gateway API<br>`experiments/large_synthetic_corpus/docs/05_ember_10_decision_log.txt` (18.500); path: Ember Catalog Service<br>`experiments/large_synthetic_corpus/docs/05_ember_01_overview.txt` (18.333); path: Ember Catalog Service
- Detected seed entities: Ember Catalog Service, Ember Gateway API, Catalog Service, Gateway API, og Service
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/05_ember_07_operations.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq028 — relationship

- Question: Ember Policy Service の公開前レビュー責任者は誰ですか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/05_ember_02_team.txt`, `experiments/large_synthetic_corpus/docs/05_ember_03_architecture.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/05_ember_03_architecture.txt` (0.679)<br>`experiments/large_synthetic_corpus/docs/05_ember_02_team.txt` (0.639)<br>`experiments/large_synthetic_corpus/docs/05_ember_02_team.txt` (0.599)<br>`experiments/large_synthetic_corpus/docs/05_ember_07_operations.txt` (0.591)<br>`experiments/large_synthetic_corpus/docs/05_ember_06_governance.txt` (0.588)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/05_ember_09_integration.txt` (21.167); path: Ember<br>`experiments/large_synthetic_corpus/docs/05_ember_01_overview.txt` (20.500); path: Ember<br>`experiments/large_synthetic_corpus/docs/05_ember_05_incident.txt` (18.500); path: Ember Policy Service<br>`experiments/large_synthetic_corpus/docs/05_ember_10_decision_log.txt` (17.167); path: Ember Policy Service<br>`experiments/large_synthetic_corpus/docs/05_ember_02_team.txt` (16.667); path: Ember Policy Service
- Detected seed entities: Ember Policy Service, Service, Ember
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/05_ember_03_architecture.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq029 — multi_hop

- Question: Ember 3.5 の公開前に必要な Ember Catalog Service の負荷試験と Ember Policy Service のアクセス規則レビューは、それぞれ誰が担当しますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/05_ember_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/05_ember_04_release.txt`, `experiments/large_synthetic_corpus/docs/05_ember_08_acceptance.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/05_ember_03_architecture.txt` (0.745)<br>`experiments/large_synthetic_corpus/docs/05_ember_02_team.txt` (0.655)<br>`experiments/large_synthetic_corpus/docs/05_ember_04_release.txt` (0.617)<br>`experiments/large_synthetic_corpus/docs/05_ember_10_decision_log.txt` (0.616)<br>`experiments/large_synthetic_corpus/docs/05_ember_08_acceptance.txt` (0.602)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/05_ember_09_integration.txt` (21.167); path: Ember Catalog Service<br>`experiments/large_synthetic_corpus/docs/05_ember_02_team.txt` (20.167); path: Ember Catalog Service<br>`experiments/large_synthetic_corpus/docs/05_ember_10_decision_log.txt` (19.667); path: Ember Catalog Service<br>`experiments/large_synthetic_corpus/docs/05_ember_04_release.txt` (19.167); path: Ember Catalog Service<br>`experiments/large_synthetic_corpus/docs/05_ember_05_incident.txt` (18.500); path: Ember Policy Service
- Detected seed entities: Ember Catalog Service, Ember Policy Service, Catalog Service, アクセス規則レビュー, og Service
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/05_ember_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/05_ember_08_acceptance.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq030 — multi_hop

- Question: Ember Gateway API の証明書更新障害では、誰が一次対応し、誰が技術調査を担当し、なぜ Ember Policy Service の臨時レビューが不要でしたか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/05_ember_02_team.txt`, `experiments/large_synthetic_corpus/docs/05_ember_05_incident.txt`, `experiments/large_synthetic_corpus/docs/05_ember_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/05_ember_05_incident.txt` (0.694)<br>`experiments/large_synthetic_corpus/docs/05_ember_03_architecture.txt` (0.685)<br>`experiments/large_synthetic_corpus/docs/05_ember_07_operations.txt` (0.659)<br>`experiments/large_synthetic_corpus/docs/05_ember_02_team.txt` (0.622)<br>`experiments/large_synthetic_corpus/docs/05_ember_02_team.txt` (0.616)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/05_ember_05_incident.txt` (22.333); path: Ember Gateway API<br>`experiments/large_synthetic_corpus/docs/05_ember_09_integration.txt` (19.500); path: Ember Gateway API<br>`experiments/large_synthetic_corpus/docs/05_ember_01_overview.txt` (18.167); path: Ember Gateway API<br>`experiments/large_synthetic_corpus/docs/05_ember_02_team.txt` (17.333); path: Ember Gateway API<br>`experiments/large_synthetic_corpus/docs/05_ember_10_decision_log.txt` (16.333); path: Ember Gateway API
- Detected seed entities: Ember Policy Service, Ember Gateway API, Gateway API, Service, 証明書更新
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/05_ember_07_operations.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq033 — relationship

- Question: Fjord Gateway API または Fjord Catalog Service の技術問題は誰にエスカレーションしますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/06_fjord_02_team.txt`, `experiments/large_synthetic_corpus/docs/06_fjord_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/06_fjord_03_architecture.txt` (0.639)<br>`experiments/large_synthetic_corpus/docs/06_fjord_02_team.txt` (0.622)<br>`experiments/large_synthetic_corpus/docs/06_fjord_07_operations.txt` (0.582)<br>`experiments/large_synthetic_corpus/docs/06_fjord_05_incident.txt` (0.564)<br>`experiments/large_synthetic_corpus/docs/06_fjord_09_integration.txt` (0.554)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/06_fjord_10_decision_log.txt` (23.167); path: Fjord Catalog Service<br>`experiments/large_synthetic_corpus/docs/06_fjord_08_acceptance.txt` (19.667); path: Fjord Catalog Service<br>`experiments/large_synthetic_corpus/docs/06_fjord_02_team.txt` (18.667); path: Fjord Catalog Service<br>`experiments/large_synthetic_corpus/docs/06_fjord_01_overview.txt` (18.167); path: Fjord Catalog Service<br>`experiments/large_synthetic_corpus/docs/06_fjord_07_operations.txt` (15.667); path: Fjord Catalog Service
- Detected seed entities: Fjord Catalog Service, Fjord Gateway API, Catalog Service, Gateway API, og Service
- Required documents missed by Graph: なし
- Vector retrieves all required evidence: yes
- Graph failure category: なし（必要文書をすべて取得）

## lq034 — relationship

- Question: Fjord Policy Service の公開前レビュー責任者は誰ですか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/06_fjord_02_team.txt`, `experiments/large_synthetic_corpus/docs/06_fjord_03_architecture.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/06_fjord_03_architecture.txt` (0.656)<br>`experiments/large_synthetic_corpus/docs/06_fjord_02_team.txt` (0.600)<br>`experiments/large_synthetic_corpus/docs/06_fjord_02_team.txt` (0.569)<br>`experiments/large_synthetic_corpus/docs/06_fjord_07_operations.txt` (0.536)<br>`experiments/large_synthetic_corpus/docs/06_fjord_10_decision_log.txt` (0.534)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/06_fjord_10_decision_log.txt` (23.833); path: Fjord Policy Service<br>`experiments/large_synthetic_corpus/docs/06_fjord_01_overview.txt` (20.500); path: Fjord<br>`experiments/large_synthetic_corpus/docs/06_fjord_02_team.txt` (20.333); path: Fjord<br>`experiments/large_synthetic_corpus/docs/06_fjord_08_acceptance.txt` (18.500); path: Fjord Policy Service<br>`experiments/large_synthetic_corpus/docs/06_fjord_06_governance.txt` (17.333); path: Fjord Policy Service
- Detected seed entities: Fjord Policy Service, Service, Fjord
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/06_fjord_03_architecture.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq035 — multi_hop

- Question: Fjord 3.6 の公開前に必要な Fjord Catalog Service の負荷試験と Fjord Policy Service のアクセス規則レビューは、それぞれ誰が担当しますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/06_fjord_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/06_fjord_04_release.txt`, `experiments/large_synthetic_corpus/docs/06_fjord_08_acceptance.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/06_fjord_03_architecture.txt` (0.760)<br>`experiments/large_synthetic_corpus/docs/06_fjord_02_team.txt` (0.673)<br>`experiments/large_synthetic_corpus/docs/06_fjord_04_release.txt` (0.640)<br>`experiments/large_synthetic_corpus/docs/06_fjord_10_decision_log.txt` (0.635)<br>`experiments/large_synthetic_corpus/docs/06_fjord_09_integration.txt` (0.619)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/06_fjord_10_decision_log.txt` (25.667); path: Fjord Catalog Service<br>`experiments/large_synthetic_corpus/docs/06_fjord_08_acceptance.txt` (19.833); path: Fjord Catalog Service<br>`experiments/large_synthetic_corpus/docs/06_fjord_02_team.txt` (19.667); path: Fjord Catalog Service<br>`experiments/large_synthetic_corpus/docs/06_fjord_01_overview.txt` (18.167); path: Fjord Catalog Service<br>`experiments/large_synthetic_corpus/docs/06_fjord_06_governance.txt` (17.667); path: Fjord Catalog Service
- Detected seed entities: Fjord Catalog Service, Fjord Policy Service, Catalog Service, アクセス規則レビュー, og Service
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/06_fjord_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/06_fjord_04_release.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq036 — multi_hop

- Question: Fjord Gateway API の証明書更新障害では、誰が一次対応し、誰が技術調査を担当し、なぜ Fjord Policy Service の臨時レビューが不要でしたか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/06_fjord_02_team.txt`, `experiments/large_synthetic_corpus/docs/06_fjord_05_incident.txt`, `experiments/large_synthetic_corpus/docs/06_fjord_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/06_fjord_03_architecture.txt` (0.719)<br>`experiments/large_synthetic_corpus/docs/06_fjord_05_incident.txt` (0.713)<br>`experiments/large_synthetic_corpus/docs/06_fjord_02_team.txt` (0.630)<br>`experiments/large_synthetic_corpus/docs/06_fjord_07_operations.txt` (0.627)<br>`experiments/large_synthetic_corpus/docs/06_fjord_07_operations.txt` (0.626)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/06_fjord_10_decision_log.txt` (24.000); path: Fjord Gateway API<br>`experiments/large_synthetic_corpus/docs/06_fjord_05_incident.txt` (21.500); path: Fjord Gateway API<br>`experiments/large_synthetic_corpus/docs/06_fjord_08_acceptance.txt` (19.333); path: Fjord Gateway API<br>`experiments/large_synthetic_corpus/docs/06_fjord_02_team.txt` (18.333); path: Fjord Gateway API<br>`experiments/large_synthetic_corpus/docs/06_fjord_01_overview.txt` (18.167); path: Fjord Gateway API
- Detected seed entities: Fjord Policy Service, Fjord Gateway API, Gateway API, Service, 証明書更新
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/06_fjord_07_operations.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq039 — relationship

- Question: Grove Gateway API または Grove Catalog Service の技術問題は誰にエスカレーションしますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/07_grove_02_team.txt`, `experiments/large_synthetic_corpus/docs/07_grove_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/07_grove_02_team.txt` (0.648)<br>`experiments/large_synthetic_corpus/docs/07_grove_03_architecture.txt` (0.640)<br>`experiments/large_synthetic_corpus/docs/07_grove_09_integration.txt` (0.597)<br>`experiments/large_synthetic_corpus/docs/07_grove_07_operations.txt` (0.597)<br>`experiments/large_synthetic_corpus/docs/07_grove_10_decision_log.txt` (0.569)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/07_grove_07_operations.txt` (21.500); path: Grove Catalog Service<br>`experiments/large_synthetic_corpus/docs/07_grove_02_team.txt` (18.667); path: Grove Catalog Service<br>`experiments/large_synthetic_corpus/docs/07_grove_10_decision_log.txt` (18.667); path: Grove Catalog Service<br>`experiments/large_synthetic_corpus/docs/07_grove_01_overview.txt` (18.167); path: Grove Catalog Service<br>`experiments/large_synthetic_corpus/docs/07_grove_05_incident.txt` (17.667); path: Grove Gateway API
- Detected seed entities: Grove Catalog Service, Grove Gateway API, Catalog Service, Gateway API, og Service
- Required documents missed by Graph: なし
- Vector retrieves all required evidence: yes
- Graph failure category: なし（必要文書をすべて取得）

## lq040 — relationship

- Question: Grove Policy Service の公開前レビュー責任者は誰ですか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/07_grove_02_team.txt`, `experiments/large_synthetic_corpus/docs/07_grove_03_architecture.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/07_grove_03_architecture.txt` (0.698)<br>`experiments/large_synthetic_corpus/docs/07_grove_02_team.txt` (0.663)<br>`experiments/large_synthetic_corpus/docs/07_grove_02_team.txt` (0.627)<br>`experiments/large_synthetic_corpus/docs/07_grove_10_decision_log.txt` (0.622)<br>`experiments/large_synthetic_corpus/docs/07_grove_07_operations.txt` (0.613)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/07_grove_07_operations.txt` (21.833); path: Grove<br>`experiments/large_synthetic_corpus/docs/07_grove_01_overview.txt` (20.667); path: Grove<br>`experiments/large_synthetic_corpus/docs/07_grove_02_team.txt` (20.333); path: Grove<br>`experiments/large_synthetic_corpus/docs/07_grove_10_decision_log.txt` (19.167); path: Grove Policy Service<br>`experiments/large_synthetic_corpus/docs/07_grove_05_incident.txt` (17.667); path: Grove Policy Service
- Detected seed entities: Grove Policy Service, Service, Grove
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/07_grove_03_architecture.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq041 — multi_hop

- Question: Grove 3.7 の公開前に必要な Grove Catalog Service の負荷試験と Grove Policy Service のアクセス規則レビューは、それぞれ誰が担当しますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/07_grove_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/07_grove_04_release.txt`, `experiments/large_synthetic_corpus/docs/07_grove_08_acceptance.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/07_grove_03_architecture.txt` (0.769)<br>`experiments/large_synthetic_corpus/docs/07_grove_02_team.txt` (0.695)<br>`experiments/large_synthetic_corpus/docs/07_grove_10_decision_log.txt` (0.656)<br>`experiments/large_synthetic_corpus/docs/07_grove_09_integration.txt` (0.650)<br>`experiments/large_synthetic_corpus/docs/07_grove_07_operations.txt` (0.634)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/07_grove_07_operations.txt` (21.333); path: Grove Catalog Service<br>`experiments/large_synthetic_corpus/docs/07_grove_02_team.txt` (19.667); path: Grove Catalog Service<br>`experiments/large_synthetic_corpus/docs/07_grove_10_decision_log.txt` (19.667); path: Grove Catalog Service<br>`experiments/large_synthetic_corpus/docs/07_grove_01_overview.txt` (18.333); path: Grove Catalog Service<br>`experiments/large_synthetic_corpus/docs/07_grove_05_incident.txt` (17.500); path: Grove Policy Service
- Detected seed entities: Grove Catalog Service, Grove Policy Service, Catalog Service, アクセス規則レビュー, og Service
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/07_grove_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/07_grove_04_release.txt`, `experiments/large_synthetic_corpus/docs/07_grove_08_acceptance.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq042 — multi_hop

- Question: Grove Gateway API の証明書更新障害では、誰が一次対応し、誰が技術調査を担当し、なぜ Grove Policy Service の臨時レビューが不要でしたか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/07_grove_02_team.txt`, `experiments/large_synthetic_corpus/docs/07_grove_05_incident.txt`, `experiments/large_synthetic_corpus/docs/07_grove_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/07_grove_03_architecture.txt` (0.724)<br>`experiments/large_synthetic_corpus/docs/07_grove_05_incident.txt` (0.721)<br>`experiments/large_synthetic_corpus/docs/07_grove_07_operations.txt` (0.679)<br>`experiments/large_synthetic_corpus/docs/07_grove_07_operations.txt` (0.664)<br>`experiments/large_synthetic_corpus/docs/07_grove_02_team.txt` (0.661)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/07_grove_07_operations.txt` (22.833); path: Grove Gateway API<br>`experiments/large_synthetic_corpus/docs/07_grove_05_incident.txt` (21.167); path: Grove Gateway API<br>`experiments/large_synthetic_corpus/docs/07_grove_01_overview.txt` (18.333); path: Grove Gateway API<br>`experiments/large_synthetic_corpus/docs/07_grove_02_team.txt` (18.333); path: Grove Gateway API<br>`experiments/large_synthetic_corpus/docs/07_grove_10_decision_log.txt` (18.333); path: Grove Gateway API
- Detected seed entities: Grove Policy Service, Grove Gateway API, Gateway API, Service, 証明書更新
- Required documents missed by Graph: なし
- Vector retrieves all required evidence: yes
- Graph failure category: なし（必要文書をすべて取得）

## lq045 — relationship

- Question: Harbor Gateway API または Harbor Catalog Service の技術問題は誰にエスカレーションしますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/08_harbor_02_team.txt`, `experiments/large_synthetic_corpus/docs/08_harbor_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/08_harbor_02_team.txt` (0.644)<br>`experiments/large_synthetic_corpus/docs/08_harbor_03_architecture.txt` (0.636)<br>`experiments/large_synthetic_corpus/docs/08_harbor_09_integration.txt` (0.603)<br>`experiments/large_synthetic_corpus/docs/08_harbor_07_operations.txt` (0.597)<br>`experiments/large_synthetic_corpus/docs/08_harbor_01_overview.txt` (0.579)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/08_harbor_07_operations.txt` (22.500); path: Harbor Catalog Service<br>`experiments/large_synthetic_corpus/docs/08_harbor_08_acceptance.txt` (18.667); path: Harbor Catalog Service<br>`experiments/large_synthetic_corpus/docs/08_harbor_10_decision_log.txt` (17.667); path: Harbor Catalog Service<br>`experiments/large_synthetic_corpus/docs/08_harbor_02_team.txt` (16.000); path: Harbor Catalog Service<br>`experiments/large_synthetic_corpus/docs/08_harbor_05_incident.txt` (15.500); path: Harbor Gateway API
- Detected seed entities: Harbor Catalog Service, Harbor Gateway API, Catalog Service, Gateway API, og Service
- Required documents missed by Graph: なし
- Vector retrieves all required evidence: yes
- Graph failure category: なし（必要文書をすべて取得）

## lq046 — relationship

- Question: Harbor Policy Service の公開前レビュー責任者は誰ですか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/08_harbor_02_team.txt`, `experiments/large_synthetic_corpus/docs/08_harbor_03_architecture.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/08_harbor_03_architecture.txt` (0.628)<br>`experiments/large_synthetic_corpus/docs/08_harbor_02_team.txt` (0.584)<br>`experiments/large_synthetic_corpus/docs/08_harbor_07_operations.txt` (0.562)<br>`experiments/large_synthetic_corpus/docs/08_harbor_05_incident.txt` (0.535)<br>`experiments/large_synthetic_corpus/docs/08_harbor_06_governance.txt` (0.529)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/08_harbor_07_operations.txt` (23.000); path: Harbor<br>`experiments/large_synthetic_corpus/docs/08_harbor_08_acceptance.txt` (19.000); path: Harbor<br>`experiments/large_synthetic_corpus/docs/08_harbor_02_team.txt` (18.333); path: Harbor<br>`experiments/large_synthetic_corpus/docs/08_harbor_05_incident.txt` (18.167); path: Harbor<br>`experiments/large_synthetic_corpus/docs/08_harbor_10_decision_log.txt` (17.167); path: Harbor Policy Service
- Detected seed entities: Harbor Policy Service, Service, Harbor
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/08_harbor_03_architecture.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq047 — multi_hop

- Question: Harbor 3.8 の公開前に必要な Harbor Catalog Service の負荷試験と Harbor Policy Service のアクセス規則レビューは、それぞれ誰が担当しますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/08_harbor_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/08_harbor_04_release.txt`, `experiments/large_synthetic_corpus/docs/08_harbor_08_acceptance.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/08_harbor_03_architecture.txt` (0.736)<br>`experiments/large_synthetic_corpus/docs/08_harbor_02_team.txt` (0.690)<br>`experiments/large_synthetic_corpus/docs/08_harbor_09_integration.txt` (0.662)<br>`experiments/large_synthetic_corpus/docs/08_harbor_10_decision_log.txt` (0.658)<br>`experiments/large_synthetic_corpus/docs/08_harbor_04_release.txt` (0.657)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/08_harbor_07_operations.txt` (22.833); path: Harbor Catalog Service<br>`experiments/large_synthetic_corpus/docs/08_harbor_08_acceptance.txt` (18.833); path: Harbor Catalog Service<br>`experiments/large_synthetic_corpus/docs/08_harbor_10_decision_log.txt` (18.833); path: Harbor Catalog Service<br>`experiments/large_synthetic_corpus/docs/08_harbor_02_team.txt` (17.167); path: Harbor Catalog Service<br>`experiments/large_synthetic_corpus/docs/08_harbor_06_governance.txt` (16.167); path: Harbor Catalog Service
- Detected seed entities: Harbor Catalog Service, Harbor Policy Service, Catalog Service, アクセス規則レビュー, og Service
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/08_harbor_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/08_harbor_04_release.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq048 — multi_hop

- Question: Harbor Gateway API の証明書更新障害では、誰が一次対応し、誰が技術調査を担当し、なぜ Harbor Policy Service の臨時レビューが不要でしたか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/08_harbor_02_team.txt`, `experiments/large_synthetic_corpus/docs/08_harbor_05_incident.txt`, `experiments/large_synthetic_corpus/docs/08_harbor_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/08_harbor_05_incident.txt` (0.712)<br>`experiments/large_synthetic_corpus/docs/08_harbor_03_architecture.txt` (0.700)<br>`experiments/large_synthetic_corpus/docs/08_harbor_07_operations.txt` (0.654)<br>`experiments/large_synthetic_corpus/docs/08_harbor_09_integration.txt` (0.641)<br>`experiments/large_synthetic_corpus/docs/08_harbor_02_team.txt` (0.633)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/08_harbor_07_operations.txt` (25.667); path: Harbor<br>`experiments/large_synthetic_corpus/docs/08_harbor_08_acceptance.txt` (20.500); path: Harbor<br>`experiments/large_synthetic_corpus/docs/08_harbor_02_team.txt` (19.833); path: Harbor<br>`experiments/large_synthetic_corpus/docs/08_harbor_05_incident.txt` (19.667); path: Harbor<br>`experiments/large_synthetic_corpus/docs/08_harbor_01_overview.txt` (18.833); path: Harbor
- Detected seed entities: Harbor Policy Service, Harbor Gateway API, Gateway API, Service, Harbor
- Required documents missed by Graph: なし
- Vector retrieves all required evidence: yes
- Graph failure category: なし（必要文書をすべて取得）

## lq051 — relationship

- Question: Indigo Gateway API または Indigo Catalog Service の技術問題は誰にエスカレーションしますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/09_indigo_02_team.txt`, `experiments/large_synthetic_corpus/docs/09_indigo_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/09_indigo_02_team.txt` (0.648)<br>`experiments/large_synthetic_corpus/docs/09_indigo_03_architecture.txt` (0.647)<br>`experiments/large_synthetic_corpus/docs/09_indigo_07_operations.txt` (0.615)<br>`experiments/large_synthetic_corpus/docs/09_indigo_09_integration.txt` (0.608)<br>`experiments/large_synthetic_corpus/docs/09_indigo_05_incident.txt` (0.572)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/09_indigo_02_team.txt` (18.667); path: Indigo Catalog Service<br>`experiments/large_synthetic_corpus/docs/09_indigo_07_operations.txt` (18.500); path: Indigo Catalog Service<br>`experiments/large_synthetic_corpus/docs/09_indigo_01_overview.txt` (18.167); path: Indigo Catalog Service<br>`experiments/large_synthetic_corpus/docs/09_indigo_05_incident.txt` (17.667); path: Indigo Gateway API<br>`experiments/large_synthetic_corpus/docs/09_indigo_10_decision_log.txt` (16.167); path: Indigo Catalog Service
- Detected seed entities: Indigo Catalog Service, Indigo Gateway API, Catalog Service, Gateway API, og Service
- Required documents missed by Graph: なし
- Vector retrieves all required evidence: yes
- Graph failure category: なし（必要文書をすべて取得）

## lq052 — relationship

- Question: Indigo Policy Service の公開前レビュー責任者は誰ですか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/09_indigo_02_team.txt`, `experiments/large_synthetic_corpus/docs/09_indigo_03_architecture.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/09_indigo_03_architecture.txt` (0.647)<br>`experiments/large_synthetic_corpus/docs/09_indigo_02_team.txt` (0.623)<br>`experiments/large_synthetic_corpus/docs/09_indigo_02_team.txt` (0.609)<br>`experiments/large_synthetic_corpus/docs/09_indigo_05_incident.txt` (0.566)<br>`experiments/large_synthetic_corpus/docs/09_indigo_10_decision_log.txt` (0.562)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/09_indigo_01_overview.txt` (24.000); path: Indigo<br>`experiments/large_synthetic_corpus/docs/09_indigo_02_team.txt` (20.500); path: Indigo<br>`experiments/large_synthetic_corpus/docs/09_indigo_07_operations.txt` (19.833); path: Indigo<br>`experiments/large_synthetic_corpus/docs/09_indigo_05_incident.txt` (19.333); path: Indigo<br>`experiments/large_synthetic_corpus/docs/09_indigo_06_governance.txt` (17.500); path: Indigo Policy Service
- Detected seed entities: Indigo Policy Service, Service, Indigo
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/09_indigo_03_architecture.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq053 — multi_hop

- Question: Indigo 3.9 の公開前に必要な Indigo Catalog Service の負荷試験と Indigo Policy Service のアクセス規則レビューは、それぞれ誰が担当しますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/09_indigo_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/09_indigo_04_release.txt`, `experiments/large_synthetic_corpus/docs/09_indigo_08_acceptance.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/09_indigo_03_architecture.txt` (0.719)<br>`experiments/large_synthetic_corpus/docs/09_indigo_02_team.txt` (0.661)<br>`experiments/large_synthetic_corpus/docs/09_indigo_04_release.txt` (0.628)<br>`experiments/large_synthetic_corpus/docs/09_indigo_09_integration.txt` (0.624)<br>`experiments/large_synthetic_corpus/docs/09_indigo_10_decision_log.txt` (0.623)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/09_indigo_02_team.txt` (19.833); path: Indigo Catalog Service<br>`experiments/large_synthetic_corpus/docs/09_indigo_10_decision_log.txt` (19.333); path: Indigo Catalog Service<br>`experiments/large_synthetic_corpus/docs/09_indigo_05_incident.txt` (18.833); path: Indigo Policy Service<br>`experiments/large_synthetic_corpus/docs/09_indigo_07_operations.txt` (18.833); path: Indigo Catalog Service<br>`experiments/large_synthetic_corpus/docs/09_indigo_01_overview.txt` (18.333); path: Indigo Catalog Service
- Detected seed entities: Indigo Catalog Service, Indigo Policy Service, Catalog Service, アクセス規則レビュー, og Service
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/09_indigo_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/09_indigo_04_release.txt`, `experiments/large_synthetic_corpus/docs/09_indigo_08_acceptance.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq054 — multi_hop

- Question: Indigo Gateway API の証明書更新障害では、誰が一次対応し、誰が技術調査を担当し、なぜ Indigo Policy Service の臨時レビューが不要でしたか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/09_indigo_02_team.txt`, `experiments/large_synthetic_corpus/docs/09_indigo_05_incident.txt`, `experiments/large_synthetic_corpus/docs/09_indigo_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/09_indigo_05_incident.txt` (0.698)<br>`experiments/large_synthetic_corpus/docs/09_indigo_03_architecture.txt` (0.689)<br>`experiments/large_synthetic_corpus/docs/09_indigo_07_operations.txt` (0.639)<br>`experiments/large_synthetic_corpus/docs/09_indigo_07_operations.txt` (0.638)<br>`experiments/large_synthetic_corpus/docs/09_indigo_02_team.txt` (0.623)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/09_indigo_01_overview.txt` (25.500); path: Indigo<br>`experiments/large_synthetic_corpus/docs/09_indigo_05_incident.txt` (22.333); path: Indigo<br>`experiments/large_synthetic_corpus/docs/09_indigo_02_team.txt` (22.000); path: Indigo<br>`experiments/large_synthetic_corpus/docs/09_indigo_07_operations.txt` (21.333); path: Indigo<br>`experiments/large_synthetic_corpus/docs/09_indigo_06_governance.txt` (18.000); path: Indigo Gateway API
- Detected seed entities: Indigo Policy Service, Indigo Gateway API, Gateway API, Service, Indigo
- Required documents missed by Graph: なし
- Vector retrieves all required evidence: yes
- Graph failure category: なし（必要文書をすべて取得）

## lq057 — relationship

- Question: Juniper Gateway API または Juniper Catalog Service の技術問題は誰にエスカレーションしますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/10_juniper_02_team.txt`, `experiments/large_synthetic_corpus/docs/10_juniper_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/10_juniper_02_team.txt` (0.644)<br>`experiments/large_synthetic_corpus/docs/10_juniper_03_architecture.txt` (0.595)<br>`experiments/large_synthetic_corpus/docs/10_juniper_09_integration.txt` (0.594)<br>`experiments/large_synthetic_corpus/docs/10_juniper_07_operations.txt` (0.592)<br>`experiments/large_synthetic_corpus/docs/10_juniper_10_decision_log.txt` (0.584)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/10_juniper_08_acceptance.txt` (18.667); path: Juniper Catalog Service<br>`experiments/large_synthetic_corpus/docs/10_juniper_01_overview.txt` (18.167); path: Juniper Catalog Service<br>`experiments/large_synthetic_corpus/docs/10_juniper_05_incident.txt` (16.500); path: Juniper Gateway API<br>`experiments/large_synthetic_corpus/docs/10_juniper_02_team.txt` (15.667); path: Juniper Catalog Service<br>`experiments/large_synthetic_corpus/docs/10_juniper_09_integration.txt` (14.667); path: Juniper Catalog Service
- Detected seed entities: Juniper Catalog Service, Juniper Gateway API, Catalog Service, Gateway API, og Service
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/10_juniper_07_operations.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq058 — relationship

- Question: Juniper Policy Service の公開前レビュー責任者は誰ですか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/10_juniper_02_team.txt`, `experiments/large_synthetic_corpus/docs/10_juniper_03_architecture.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/10_juniper_03_architecture.txt` (0.657)<br>`experiments/large_synthetic_corpus/docs/10_juniper_02_team.txt` (0.642)<br>`experiments/large_synthetic_corpus/docs/10_juniper_07_operations.txt` (0.612)<br>`experiments/large_synthetic_corpus/docs/10_juniper_06_governance.txt` (0.597)<br>`experiments/large_synthetic_corpus/docs/10_juniper_02_team.txt` (0.594)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/10_juniper_01_overview.txt` (20.500); path: Juniper<br>`experiments/large_synthetic_corpus/docs/10_juniper_02_team.txt` (18.833); path: Juniper<br>`experiments/large_synthetic_corpus/docs/10_juniper_08_acceptance.txt` (17.500); path: Juniper Policy Service<br>`experiments/large_synthetic_corpus/docs/10_juniper_05_incident.txt` (17.000); path: Juniper Policy Service<br>`experiments/large_synthetic_corpus/docs/10_juniper_10_decision_log.txt` (16.833); path: Juniper Policy Service
- Detected seed entities: Juniper Policy Service, Service, Juniper
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/10_juniper_03_architecture.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq059 — multi_hop

- Question: Juniper 3.10 の公開前に必要な Juniper Catalog Service の負荷試験と Juniper Policy Service のアクセス規則レビューは、それぞれ誰が担当しますか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/10_juniper_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/10_juniper_04_release.txt`, `experiments/large_synthetic_corpus/docs/10_juniper_08_acceptance.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/10_juniper_03_architecture.txt` (0.739)<br>`experiments/large_synthetic_corpus/docs/10_juniper_02_team.txt` (0.669)<br>`experiments/large_synthetic_corpus/docs/10_juniper_04_release.txt` (0.642)<br>`experiments/large_synthetic_corpus/docs/10_juniper_10_decision_log.txt` (0.636)<br>`experiments/large_synthetic_corpus/docs/10_juniper_09_integration.txt` (0.635)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/10_juniper_01_overview.txt` (24.333); path: Juniper 3.10<br>`experiments/large_synthetic_corpus/docs/10_juniper_08_acceptance.txt` (20.500); path: Juniper 3.10<br>`experiments/large_synthetic_corpus/docs/10_juniper_02_team.txt` (18.833); path: Juniper Catalog Service<br>`experiments/large_synthetic_corpus/docs/10_juniper_10_decision_log.txt` (18.333); path: Juniper Catalog Service<br>`experiments/large_synthetic_corpus/docs/10_juniper_05_incident.txt` (17.000); path: Juniper Policy Service
- Detected seed entities: Juniper Catalog Service, Juniper Policy Service, Catalog Service, Juniper 3.10, アクセス規則レビュー
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/10_juniper_03_architecture.txt`, `experiments/large_synthetic_corpus/docs/10_juniper_04_release.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.

## lq060 — multi_hop

- Question: Juniper Gateway API の証明書更新障害では、誰が一次対応し、誰が技術調査を担当し、なぜ Juniper Policy Service の臨時レビューが不要でしたか？
- Required relevant documents: `experiments/large_synthetic_corpus/docs/10_juniper_02_team.txt`, `experiments/large_synthetic_corpus/docs/10_juniper_05_incident.txt`, `experiments/large_synthetic_corpus/docs/10_juniper_07_operations.txt`
- Vector top-5 documents and scores: `experiments/large_synthetic_corpus/docs/10_juniper_05_incident.txt` (0.703)<br>`experiments/large_synthetic_corpus/docs/10_juniper_03_architecture.txt` (0.687)<br>`experiments/large_synthetic_corpus/docs/10_juniper_07_operations.txt` (0.662)<br>`experiments/large_synthetic_corpus/docs/10_juniper_07_operations.txt` (0.650)<br>`experiments/large_synthetic_corpus/docs/10_juniper_02_team.txt` (0.627)
- Graph top-5 documents: `experiments/large_synthetic_corpus/docs/10_juniper_01_overview.txt` (22.000); path: Juniper<br>`experiments/large_synthetic_corpus/docs/10_juniper_05_incident.txt` (19.667); path: Juniper Gateway API<br>`experiments/large_synthetic_corpus/docs/10_juniper_08_acceptance.txt` (19.000); path: Juniper Gateway API<br>`experiments/large_synthetic_corpus/docs/10_juniper_02_team.txt` (18.833); path: Juniper<br>`experiments/large_synthetic_corpus/docs/10_juniper_10_decision_log.txt` (16.833); path: Juniper Policy Service
- Detected seed entities: Juniper Policy Service, Juniper Gateway API, Gateway API, Service, Juniper
- Required documents missed by Graph: `experiments/large_synthetic_corpus/docs/10_juniper_07_operations.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: At least one missed required document has a chunk reference on a node reached within the configured depth, but it was not returned in the top-5.
