# GraphRAG failure analysis

Frozen Graph auto v2; depth=2, maximum seed entities=5, top-k=5. This report does not modify retrieval, parameters, or the dataset.

## q009 — relationship

- Question: アクセス規則に問題が見つかった場合、最終的に公開可否を判断するのは誰ですか？
- Required relevant documents: `docs/benchmark_06_governance.txt`
- Vector top-5 documents and scores: `docs/benchmark_06_governance.txt` (0.484)<br>`docs/benchmark_05_incident_report.txt` (0.433)<br>`docs/benchmark_08_acceptance_criteria.txt` (0.409)<br>`docs/benchmark_03_architecture.txt` (0.388)<br>`docs/sample.txt` (0.384)
- Graph top-5 documents: なし
- Detected seed entities: なし
- Required documents missed by Graph: `docs/benchmark_06_governance.txt`
- Graph failure category: 1. entity extraction failure
- Classification rationale: The access-rule and decision concepts in the question were not retained as graph entities.

## q010 — relationship

- Question: Catalog Service の設計責任者は誰ですか？
- Required relevant documents: `docs/benchmark_03_architecture.txt`, `docs/benchmark_02_team_roles.txt`
- Vector top-5 documents and scores: `docs/benchmark_02_team_roles.txt` (0.526)<br>`docs/benchmark_03_architecture.txt` (0.460)<br>`docs/benchmark_04_release_plan.txt` (0.423)<br>`docs/benchmark_06_governance.txt` (0.407)<br>`docs/benchmark_01_program_overview.txt` (0.365)
- Graph top-5 documents: `docs/benchmark_07_operations.txt` (19.667); path: Catalog Service<br>`docs/benchmark_03_architecture.txt` (14.833); path: Catalog Service<br>`docs/benchmark_05_incident_report.txt` (13.833); path: Catalog Service → Gateway API<br>`docs/benchmark_04_release_plan.txt` (13.333); path: Catalog Service<br>`docs/benchmark_06_governance.txt` (13.167); path: Catalog Service
- Detected seed entities: Catalog Service
- Required documents missed by Graph: `docs/benchmark_02_team_roles.txt`
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: Catalog Service is a seed and has provenance for the missed document, but it was ranked below top-5.

## q011 — relationship

- Question: Policy Service の公開前レビュー責任者は誰ですか？
- Required relevant documents: `docs/benchmark_03_architecture.txt`, `docs/benchmark_02_team_roles.txt`
- Vector top-5 documents and scores: `docs/benchmark_06_governance.txt` (0.484)<br>`docs/benchmark_02_team_roles.txt` (0.462)<br>`docs/benchmark_03_architecture.txt` (0.400)<br>`docs/benchmark_04_release_plan.txt` (0.397)<br>`docs/benchmark_05_incident_report.txt` (0.382)
- Graph top-5 documents: `docs/benchmark_07_operations.txt` (19.833); path: Policy Service<br>`docs/benchmark_05_incident_report.txt` (16.833); path: Policy Service<br>`docs/benchmark_06_governance.txt` (15.667); path: Policy Service<br>`docs/benchmark_01_program_overview.txt` (14.833); path: Policy Service<br>`docs/benchmark_04_release_plan.txt` (13.333); path: Policy Service
- Detected seed entities: Policy Service
- Required documents missed by Graph: `docs/benchmark_02_team_roles.txt`, `docs/benchmark_03_architecture.txt`
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: Policy Service is a seed and has provenance for both missed documents, but neither appeared in top-5.

## q012 — relationship

- Question: 検索失敗の一次対応を担当するのは誰ですか？
- Required relevant documents: `docs/benchmark_07_operations.txt`, `docs/benchmark_02_team_roles.txt`
- Vector top-5 documents and scores: `docs/benchmark_02_team_roles.txt` (0.458)<br>`docs/benchmark_07_operations.txt` (0.420)<br>`docs/benchmark_05_incident_report.txt` (0.412)<br>`docs/benchmark_08_acceptance_criteria.txt` (0.389)<br>`docs/sample.txt` (0.383)
- Graph top-5 documents: `docs/benchmark_07_operations.txt` (18.500); path: 検索失敗<br>`docs/benchmark_05_incident_report.txt` (9.167); path: 検索失敗 → 高橋悠<br>`docs/benchmark_02_team_roles.txt` (5.167); path: 検索失敗 → 高橋悠<br>`docs/benchmark_03_architecture.txt` (4.333); path: 検索失敗 → 高橋悠 → Catalog Service<br>`docs/benchmark_06_governance.txt` (3.333); path: 検索失敗 → 高橋悠 → Catalog Service
- Detected seed entities: 検索失敗
- Required documents missed by Graph: なし
- Graph failure category: なし（必要文書をすべて取得）

## q013 — relationship

- Question: 調達部で製品仕様書の更新確認を担当するのは誰ですか？
- Required relevant documents: `docs/benchmark_02_team_roles.txt`, `docs/benchmark_06_governance.txt`
- Vector top-5 documents and scores: `docs/benchmark_02_team_roles.txt` (0.522)<br>`docs/benchmark_06_governance.txt` (0.509)<br>`docs/benchmark_08_acceptance_criteria.txt` (0.430)<br>`docs/benchmark_04_release_plan.txt` (0.424)<br>`docs/benchmark_07_operations.txt` (0.383)
- Graph top-5 documents: `docs/benchmark_04_release_plan.txt` (6.167); path: 調達部<br>`docs/benchmark_01_program_overview.txt` (3.833); path: 調達部<br>`docs/benchmark_02_team_roles.txt` (1.333); path: 調達部 → 仕様書サンプル確認 → 伊藤彩<br>`docs/benchmark_08_acceptance_criteria.txt` (1.333); path: 調達部 → 仕様書サンプル確認 → 伊藤彩<br>`docs/benchmark_06_governance.txt` (0.667); path: 調達部 → 仕様書サンプル確認 → 伊藤彩
- Detected seed entities: 調達部
- Required documents missed by Graph: なし
- Graph failure category: なし（必要文書をすべて取得）

## q014 — relationship

- Question: Gateway API または Catalog Service の技術問題は誰にエスカレーションしますか？
- Required relevant documents: `docs/benchmark_07_operations.txt`, `docs/benchmark_02_team_roles.txt`
- Vector top-5 documents and scores: `docs/benchmark_03_architecture.txt` (0.520)<br>`docs/benchmark_07_operations.txt` (0.487)<br>`docs/benchmark_05_incident_report.txt` (0.441)<br>`docs/benchmark_01_program_overview.txt` (0.415)<br>`docs/benchmark_02_team_roles.txt` (0.411)
- Graph top-5 documents: `docs/benchmark_07_operations.txt` (23.333); path: Catalog Service<br>`docs/benchmark_05_incident_report.txt` (17.833); path: Gateway API<br>`docs/benchmark_03_architecture.txt` (16.333); path: Catalog Service<br>`docs/benchmark_06_governance.txt` (14.667); path: Catalog Service<br>`docs/benchmark_04_release_plan.txt` (14.333); path: Catalog Service
- Detected seed entities: Catalog Service, Gateway API
- Required documents missed by Graph: `docs/benchmark_02_team_roles.txt`
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: Both service names are seeds and the missed team-role document is reachable, but it was ranked below top-5.

## q015 — relationship

- Question: アクセス規則に関するエスカレーション先は誰ですか？
- Required relevant documents: `docs/benchmark_07_operations.txt`, `docs/benchmark_02_team_roles.txt`
- Vector top-5 documents and scores: `docs/benchmark_05_incident_report.txt` (0.366)<br>`docs/benchmark_03_architecture.txt` (0.362)<br>`docs/benchmark_06_governance.txt` (0.360)<br>`docs/benchmark_07_operations.txt` (0.353)<br>`docs/sample.txt` (0.340)
- Graph top-5 documents: なし
- Detected seed entities: なし
- Required documents missed by Graph: `docs/benchmark_02_team_roles.txt`, `docs/benchmark_07_operations.txt`
- Graph failure category: 1. entity extraction failure
- Classification rationale: The source discusses access rules, but no matching access-rule entity exists in the graph.

## q016 — relationship

- Question: 公開延期の連絡を調達部の窓口へ行うのは誰ですか？
- Required relevant documents: `docs/benchmark_04_release_plan.txt`, `docs/benchmark_02_team_roles.txt`
- Vector top-5 documents and scores: `docs/sample.txt` (0.466)<br>`docs/benchmark_07_operations.txt` (0.438)<br>`docs/benchmark_02_team_roles.txt` (0.432)<br>`docs/benchmark_06_governance.txt` (0.417)<br>`docs/benchmark_05_incident_report.txt` (0.388)
- Graph top-5 documents: `docs/benchmark_04_release_plan.txt` (6.167); path: 調達部<br>`docs/benchmark_01_program_overview.txt` (3.833); path: 調達部<br>`docs/benchmark_02_team_roles.txt` (1.333); path: 調達部 → 仕様書サンプル確認 → 伊藤彩<br>`docs/benchmark_08_acceptance_criteria.txt` (1.333); path: 調達部 → 仕様書サンプル確認 → 伊藤彩<br>`docs/benchmark_06_governance.txt` (0.667); path: 調達部 → 仕様書サンプル確認 → 伊藤彩
- Detected seed entities: 調達部
- Required documents missed by Graph: なし
- Graph failure category: なし（必要文書をすべて取得）

## q017 — multi_hop

- Question: Orion 2.1 の公開前に完了が必要な三つの確認は何ですか？
- Required relevant documents: `docs/benchmark_04_release_plan.txt`
- Vector top-5 documents and scores: `docs/benchmark_04_release_plan.txt` (0.619)<br>`docs/benchmark_08_acceptance_criteria.txt` (0.530)<br>`docs/benchmark_03_architecture.txt` (0.408)<br>`docs/benchmark_02_team_roles.txt` (0.345)<br>`docs/benchmark_01_program_overview.txt` (0.344)
- Graph top-5 documents: `docs/benchmark_01_program_overview.txt` (17.000); path: Orion 2.1<br>`docs/benchmark_04_release_plan.txt` (14.500); path: Orion 2.1<br>`docs/benchmark_08_acceptance_criteria.txt` (10.833); path: Orion 2.1<br>`docs/benchmark_02_team_roles.txt` (10.667); path: Orion 2.1 → Atlas<br>`docs/benchmark_05_incident_report.txt` (10.167); path: Orion 2.1 → Atlas
- Detected seed entities: Orion 2.1
- Required documents missed by Graph: なし
- Graph failure category: なし（必要文書をすべて取得）
- Benchmark note: does not require graph traversal

## q018 — multi_hop

- Question: 未設定の公開規則を持つ文書が検索結果に返らないようにするコンポーネントは何ですか？
- Required relevant documents: `docs/benchmark_03_architecture.txt`, `docs/benchmark_06_governance.txt`, `docs/benchmark_08_acceptance_criteria.txt`
- Vector top-5 documents and scores: `docs/benchmark_06_governance.txt` (0.540)<br>`docs/benchmark_03_architecture.txt` (0.463)<br>`docs/benchmark_08_acceptance_criteria.txt` (0.438)<br>`docs/benchmark_05_incident_report.txt` (0.419)<br>`docs/benchmark_01_program_overview.txt` (0.388)
- Graph top-5 documents: `docs/sample.txt` (13.833); path: 文書<br>`docs/sample.txt` (11.833); path: 文書
- Detected seed entities: 文書
- Required documents missed by Graph: `docs/benchmark_03_architecture.txt`, `docs/benchmark_06_governance.txt`, `docs/benchmark_08_acceptance_criteria.txt`
- Graph failure category: 3. seed entity matching failure
- Classification rationale: The generic word document matched only the unrelated sample-document node instead of the intended policy entities.

## q019 — multi_hop

- Question: Gateway API の証明書障害では、誰が一次対応し、誰が技術調査を担当しましたか？
- Required relevant documents: `docs/benchmark_05_incident_report.txt`, `docs/benchmark_02_team_roles.txt`
- Vector top-5 documents and scores: `docs/benchmark_05_incident_report.txt` (0.606)<br>`docs/benchmark_07_operations.txt` (0.540)<br>`docs/benchmark_02_team_roles.txt` (0.504)<br>`docs/benchmark_06_governance.txt` (0.458)<br>`docs/benchmark_03_architecture.txt` (0.411)
- Graph top-5 documents: `docs/benchmark_07_operations.txt` (21.833); path: Gateway API<br>`docs/benchmark_05_incident_report.txt` (17.333); path: Gateway API<br>`docs/benchmark_03_architecture.txt` (12.500); path: Gateway API<br>`docs/benchmark_06_governance.txt` (10.333); path: Gateway API<br>`docs/benchmark_02_team_roles.txt` (10.000); path: Gateway API → Catalog Service
- Detected seed entities: Gateway API
- Required documents missed by Graph: なし
- Graph failure category: なし（必要文書をすべて取得）

## q020 — multi_hop

- Question: 公開判定前日に未解決の高優先度障害がある場合、公開と調達部連絡はどうなりますか？
- Required relevant documents: `docs/benchmark_04_release_plan.txt`
- Vector top-5 documents and scores: `docs/sample.txt` (0.452)<br>`docs/benchmark_05_incident_report.txt` (0.399)<br>`docs/benchmark_06_governance.txt` (0.382)<br>`docs/benchmark_04_release_plan.txt` (0.347)<br>`docs/benchmark_07_operations.txt` (0.333)
- Graph top-5 documents: `docs/benchmark_04_release_plan.txt` (13.000); path: 調達部<br>`docs/benchmark_05_incident_report.txt` (4.833); path: 高優先度障害<br>`docs/benchmark_01_program_overview.txt` (4.167); path: 調達部<br>`docs/benchmark_08_acceptance_criteria.txt` (2.000); path: 高優先度障害 → 証明書更新失敗 → Gateway API<br>`docs/benchmark_02_team_roles.txt` (1.333); path: 高優先度障害 → 公開予定日 → 伊藤彩
- Detected seed entities: 高優先度障害, 調達部
- Required documents missed by Graph: なし
- Graph failure category: なし（必要文書をすべて取得）
- Benchmark note: does not require graph traversal

## q021 — multi_hop

- Question: 平均応答時間が2秒を超える状態が15分続いた場合、誰が何として記録しますか？
- Required relevant documents: `docs/benchmark_07_operations.txt`, `docs/benchmark_02_team_roles.txt`
- Vector top-5 documents and scores: `docs/benchmark_07_operations.txt` (0.388)<br>`docs/sample.txt` (0.336)<br>`docs/benchmark_02_team_roles.txt` (0.296)<br>`docs/benchmark_05_incident_report.txt` (0.295)<br>`docs/sample.txt` (0.279)
- Graph top-5 documents: なし
- Detected seed entities: なし
- Required documents missed by Graph: `docs/benchmark_02_team_roles.txt`, `docs/benchmark_07_operations.txt`
- Graph failure category: 1. entity extraction failure
- Classification rationale: Average response time was not extracted as an entity even though the operations source contains the concept.

## q022 — multi_hop

- Question: Vector Index が公開可否を判断しないため、アクセス規則の変更はどこへ反映しますか？
- Required relevant documents: `docs/benchmark_03_architecture.txt`
- Vector top-5 documents and scores: `docs/benchmark_03_architecture.txt` (0.420)<br>`docs/benchmark_05_incident_report.txt` (0.406)<br>`docs/benchmark_07_operations.txt` (0.371)<br>`docs/benchmark_01_program_overview.txt` (0.365)<br>`docs/benchmark_06_governance.txt` (0.360)
- Graph top-5 documents: `docs/benchmark_01_program_overview.txt` (15.000); path: Vector Index<br>`docs/benchmark_05_incident_report.txt` (12.500); path: Vector Index<br>`docs/benchmark_02_team_roles.txt` (11.500); path: Vector Index<br>`docs/benchmark_03_architecture.txt` (10.667); path: Vector Index<br>`docs/benchmark_08_acceptance_criteria.txt` (8.500); path: Vector Index
- Detected seed entities: Vector Index
- Required documents missed by Graph: なし
- Graph failure category: なし（必要文書をすべて取得）
- Benchmark note: does not require graph traversal

## q023 — multi_hop

- Question: Orion 2.1 の公開可否を佐藤真央が判断する前に、田中健と鈴木梨奈はそれぞれ何の結果を提出しますか？
- Required relevant documents: `docs/benchmark_08_acceptance_criteria.txt`, `docs/benchmark_04_release_plan.txt`
- Vector top-5 documents and scores: `docs/benchmark_04_release_plan.txt` (0.648)<br>`docs/benchmark_08_acceptance_criteria.txt` (0.542)<br>`docs/benchmark_02_team_roles.txt` (0.428)<br>`docs/benchmark_03_architecture.txt` (0.428)<br>`docs/benchmark_06_governance.txt` (0.374)
- Graph top-5 documents: `docs/benchmark_04_release_plan.txt` (28.167); path: Orion 2.1<br>`docs/benchmark_07_operations.txt` (21.500); path: 田中健<br>`docs/benchmark_02_team_roles.txt` (21.000); path: 佐藤真央<br>`docs/benchmark_01_program_overview.txt` (20.667); path: Orion 2.1<br>`docs/benchmark_05_incident_report.txt` (20.667); path: 田中健
- Detected seed entities: Orion 2.1, 佐藤真央, 鈴木梨奈, 田中健
- Required documents missed by Graph: `docs/benchmark_08_acceptance_criteria.txt`
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: Named seeds exist and the acceptance-criteria document is reachable, but it was ranked below top-5.

## q024 — multi_hop

- Question: 2026年6月の障害で Policy Service のレビューが不要だった理由は何ですか？
- Required relevant documents: `docs/benchmark_05_incident_report.txt`
- Vector top-5 documents and scores: `docs/benchmark_05_incident_report.txt` (0.551)<br>`docs/benchmark_06_governance.txt` (0.434)<br>`docs/benchmark_04_release_plan.txt` (0.432)<br>`docs/sample.txt` (0.411)<br>`docs/benchmark_02_team_roles.txt` (0.365)
- Graph top-5 documents: `docs/benchmark_07_operations.txt` (19.833); path: Policy Service<br>`docs/benchmark_05_incident_report.txt` (16.833); path: Policy Service<br>`docs/benchmark_06_governance.txt` (15.667); path: Policy Service<br>`docs/benchmark_01_program_overview.txt` (14.833); path: Policy Service<br>`docs/benchmark_04_release_plan.txt` (13.333); path: Policy Service
- Detected seed entities: Policy Service
- Required documents missed by Graph: なし
- Graph failure category: なし（必要文書をすべて取得）
- Benchmark note: does not require graph traversal
