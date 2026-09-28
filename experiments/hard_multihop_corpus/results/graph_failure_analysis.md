# GraphRAG failure analysis

Frozen Graph auto v2; depth=2, maximum seed entities=5, top-k=5. This report does not modify retrieval, parameters, or the dataset.

Graph failures: 19. 3. seed entity matching failure: 15, 5. traversal/ranking failure: 4

Multi-hop questions where Vector retrieved every required document without graph traversal: hq02b

## hq01a — multi_hop

- Question: Northstar の警報が出たとき、調査を開始する運用責任組織はどこですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/atlas_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/atlas_03_service_ownership.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/atlas_01_signal_registry.txt` (0.591)<br>`experiments/hard_multihop_corpus/docs/atlas_02_signal_routing.txt` (0.586)<br>`experiments/hard_multihop_corpus/docs/atlas_05_error_catalog.txt` (0.550)<br>`experiments/hard_multihop_corpus/docs/atlas_06_change_note.txt` (0.487)<br>`experiments/hard_multihop_corpus/docs/atlas_08_release_note.txt` (0.459)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/beacon_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/comet_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/delta_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/atlas_05_error_catalog.txt` (7.500); path: Northstar
- Detected seed entities: Northstar, 警報, 調査
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/atlas_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/atlas_03_service_ownership.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 3. seed entity matching failure
- Classification rationale: The generic seeds 調査 and 警報 connect to repeated similar-terms documents across all programs and outrank the Northstar path.

## hq01b — multi_hop

- Question: Northstar の警報を理由に公開例外を申請するときの最終承認者は誰ですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/atlas_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/atlas_04_exception_register.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/atlas_01_signal_registry.txt` (0.542)<br>`experiments/hard_multihop_corpus/docs/delta_04_exception_register.txt` (0.507)<br>`experiments/hard_multihop_corpus/docs/atlas_02_signal_routing.txt` (0.504)<br>`experiments/hard_multihop_corpus/docs/atlas_05_error_catalog.txt` (0.499)<br>`experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (0.485)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (9.833); path: 公開例外<br>`experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (7.833); path: 例外<br>`experiments/hard_multihop_corpus/docs/beacon_07_similar_terms.txt` (7.833); path: 例外<br>`experiments/hard_multihop_corpus/docs/comet_07_similar_terms.txt` (7.833); path: 例外<br>`experiments/hard_multihop_corpus/docs/delta_07_similar_terms.txt` (7.833); path: 例外
- Detected seed entities: Northstar, 公開例外, 警報, 例外
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/atlas_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/atlas_04_exception_register.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 3. seed entity matching failure
- Classification rationale: 公開例外 and 例外 match generic cross-program nodes, so the Atlas-specific route and approval documents are displaced.

## hq01c — multi_hop

- Question: 障害コード E-41 を見つけた場合、復旧確認まで担当する組織はどこですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/atlas_05_error_catalog.txt`, `experiments/hard_multihop_corpus/docs/atlas_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/atlas_03_service_ownership.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/atlas_05_error_catalog.txt` (0.510)<br>`experiments/hard_multihop_corpus/docs/delta_05_error_catalog.txt` (0.497)<br>`experiments/hard_multihop_corpus/docs/beacon_05_error_catalog.txt` (0.474)<br>`experiments/hard_multihop_corpus/docs/comet_05_error_catalog.txt` (0.459)<br>`experiments/hard_multihop_corpus/docs/delta_07_similar_terms.txt` (0.403)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/atlas_05_error_catalog.txt` (7.333); path: E-41<br>`experiments/hard_multihop_corpus/docs/beacon_05_error_catalog.txt` (3.833); path: E-41 → 一次対応者<br>`experiments/hard_multihop_corpus/docs/delta_05_error_catalog.txt` (3.833); path: E-41 → 一次対応者<br>`experiments/hard_multihop_corpus/docs/atlas_08_release_note.txt` (2.833); path: E-41 → Northstar<br>`experiments/hard_multihop_corpus/docs/atlas_01_signal_registry.txt` (1.833); path: E-41 → Northstar
- Detected seed entities: E-41
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/atlas_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/atlas_03_service_ownership.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: E-41 reaches Northstar and Atlas Relay, but the shared 一次対応者 node brings other error-catalog chunks above the required routing and ownership documents.

## hq01d — relationship

- Question: Atlas Relay の運用責任組織はどこですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/atlas_03_service_ownership.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/atlas_03_service_ownership.txt` (0.589)<br>`experiments/hard_multihop_corpus/docs/atlas_06_change_note.txt` (0.520)<br>`experiments/hard_multihop_corpus/docs/atlas_04_exception_register.txt` (0.512)<br>`experiments/hard_multihop_corpus/docs/atlas_02_signal_routing.txt` (0.473)<br>`experiments/hard_multihop_corpus/docs/beacon_03_service_ownership.txt` (0.467)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (8.500); path: Atlas<br>`experiments/hard_multihop_corpus/docs/atlas_08_release_note.txt` (6.500); path: Atlas<br>`experiments/hard_multihop_corpus/docs/atlas_02_signal_routing.txt` (6.000); path: Atlas Relay<br>`experiments/hard_multihop_corpus/docs/atlas_05_error_catalog.txt` (4.833); path: Atlas<br>`experiments/hard_multihop_corpus/docs/beacon_07_similar_terms.txt` (4.833); path: Atlas → 例外
- Detected seed entities: Atlas Relay, Atlas
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/atlas_03_service_ownership.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 3. seed entity matching failure
- Classification rationale: The exact service seed is accompanied by the broad Atlas seed, whose repeated provenance outranks the ownership document.

## hq01e — relationship

- Question: Atlas Relay の公開例外の最終承認者は誰ですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/atlas_04_exception_register.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/atlas_04_exception_register.txt` (0.575)<br>`experiments/hard_multihop_corpus/docs/atlas_03_service_ownership.txt` (0.545)<br>`experiments/hard_multihop_corpus/docs/atlas_06_change_note.txt` (0.534)<br>`experiments/hard_multihop_corpus/docs/atlas_08_release_note.txt` (0.477)<br>`experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (0.471)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (9.833); path: 公開例外<br>`experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (9.000); path: Atlas<br>`experiments/hard_multihop_corpus/docs/atlas_08_release_note.txt` (6.500); path: Atlas<br>`experiments/hard_multihop_corpus/docs/beacon_07_similar_terms.txt` (6.500); path: 例外<br>`experiments/hard_multihop_corpus/docs/comet_07_similar_terms.txt` (6.500); path: 例外
- Detected seed entities: Atlas Relay, Atlas, 公開例外, 例外
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/atlas_04_exception_register.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 3. seed entity matching failure
- Classification rationale: The broad Atlas, 公開例外, and 例外 seeds displace the Atlas-specific approval document.

## hq02a — multi_hop

- Question: Lighthouse の警報が出たとき、調査を開始する運用責任組織はどこですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/beacon_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/beacon_03_service_ownership.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/beacon_02_signal_routing.txt` (0.598)<br>`experiments/hard_multihop_corpus/docs/beacon_01_signal_registry.txt` (0.577)<br>`experiments/hard_multihop_corpus/docs/beacon_05_error_catalog.txt` (0.562)<br>`experiments/hard_multihop_corpus/docs/beacon_06_change_note.txt` (0.528)<br>`experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (0.482)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/beacon_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/comet_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/delta_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/beacon_05_error_catalog.txt` (7.500); path: Lighthouse
- Detected seed entities: Lighthouse, 警報, 調査
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/beacon_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/beacon_03_service_ownership.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 3. seed entity matching failure
- Classification rationale: The generic seeds 調査 and 警報 connect to repeated similar-terms documents across all programs and outrank the Lighthouse path.

## hq02b — multi_hop

- Question: Lighthouse の警報を理由に公開例外を申請するときの最終承認者は誰ですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/beacon_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (0.532)<br>`experiments/hard_multihop_corpus/docs/beacon_01_signal_registry.txt` (0.530)<br>`experiments/hard_multihop_corpus/docs/beacon_02_signal_routing.txt` (0.523)<br>`experiments/hard_multihop_corpus/docs/beacon_06_change_note.txt` (0.515)<br>`experiments/hard_multihop_corpus/docs/beacon_05_error_catalog.txt` (0.508)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (9.833); path: 公開例外<br>`experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (7.833); path: 例外<br>`experiments/hard_multihop_corpus/docs/beacon_07_similar_terms.txt` (7.833); path: 例外<br>`experiments/hard_multihop_corpus/docs/comet_07_similar_terms.txt` (7.833); path: 例外<br>`experiments/hard_multihop_corpus/docs/delta_07_similar_terms.txt` (7.833); path: 例外
- Detected seed entities: Lighthouse, 公開例外, 警報, 例外
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/beacon_02_signal_routing.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 3. seed entity matching failure
- Classification rationale: 公開例外 and 例外 match generic cross-program nodes, so the Beacon-specific routing document is displaced.

## hq02c — multi_hop

- Question: 障害コード E-52 を見つけた場合、復旧確認まで担当する組織はどこですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/beacon_05_error_catalog.txt`, `experiments/hard_multihop_corpus/docs/beacon_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/beacon_03_service_ownership.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/beacon_05_error_catalog.txt` (0.515)<br>`experiments/hard_multihop_corpus/docs/delta_05_error_catalog.txt` (0.508)<br>`experiments/hard_multihop_corpus/docs/atlas_05_error_catalog.txt` (0.490)<br>`experiments/hard_multihop_corpus/docs/comet_05_error_catalog.txt` (0.477)<br>`experiments/hard_multihop_corpus/docs/delta_07_similar_terms.txt` (0.398)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/beacon_05_error_catalog.txt` (7.333); path: E-52<br>`experiments/hard_multihop_corpus/docs/atlas_05_error_catalog.txt` (3.833); path: E-52 → 一次対応者<br>`experiments/hard_multihop_corpus/docs/delta_05_error_catalog.txt` (3.833); path: E-52 → 一次対応者<br>`experiments/hard_multihop_corpus/docs/beacon_08_release_note.txt` (2.833); path: E-52 → Lighthouse<br>`experiments/hard_multihop_corpus/docs/beacon_01_signal_registry.txt` (1.833); path: E-52 → Lighthouse
- Detected seed entities: E-52
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/beacon_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/beacon_03_service_ownership.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: E-52 reaches Lighthouse and Beacon Bridge, but the shared 一次対応者 node brings other error-catalog chunks above the required routing and ownership documents.

## hq02d — relationship

- Question: Beacon Bridge の運用責任組織はどこですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/beacon_03_service_ownership.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/beacon_03_service_ownership.txt` (0.687)<br>`experiments/hard_multihop_corpus/docs/beacon_06_change_note.txt` (0.663)<br>`experiments/hard_multihop_corpus/docs/beacon_02_signal_routing.txt` (0.621)<br>`experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (0.604)<br>`experiments/hard_multihop_corpus/docs/beacon_08_release_note.txt` (0.592)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/beacon_07_similar_terms.txt` (8.500); path: Beacon<br>`experiments/hard_multihop_corpus/docs/beacon_08_release_note.txt` (6.500); path: Beacon<br>`experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (6.167); path: Beacon Bridge<br>`experiments/hard_multihop_corpus/docs/beacon_05_error_catalog.txt` (4.833); path: Beacon<br>`experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (4.833); path: Beacon → 例外
- Detected seed entities: Beacon Bridge, Beacon
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/beacon_03_service_ownership.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 3. seed entity matching failure
- Classification rationale: The exact service seed is accompanied by the broad Beacon seed, whose repeated provenance outranks the ownership document.

## hq02e — relationship

- Question: Beacon Bridge の公開例外の最終承認者は誰ですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/beacon_06_change_note.txt` (0.648)<br>`experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (0.642)<br>`experiments/hard_multihop_corpus/docs/beacon_03_service_ownership.txt` (0.641)<br>`experiments/hard_multihop_corpus/docs/beacon_08_release_note.txt` (0.602)<br>`experiments/hard_multihop_corpus/docs/beacon_02_signal_routing.txt` (0.568)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (10.333); path: Beacon Bridge<br>`experiments/hard_multihop_corpus/docs/beacon_07_similar_terms.txt` (9.000); path: Beacon<br>`experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (6.500); path: 例外<br>`experiments/hard_multihop_corpus/docs/beacon_08_release_note.txt` (6.500); path: Beacon<br>`experiments/hard_multihop_corpus/docs/comet_07_similar_terms.txt` (6.500); path: 例外
- Detected seed entities: Beacon Bridge, Beacon, 公開例外, 例外
- Required documents missed by Graph: なし
- Vector retrieves all required evidence: yes
- Graph failure category: なし（必要文書をすべて取得）

## hq03a — multi_hop

- Question: Tailwind の警報が出たとき、調査を開始する運用責任組織はどこですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/comet_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/comet_03_service_ownership.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/comet_01_signal_registry.txt` (0.550)<br>`experiments/hard_multihop_corpus/docs/comet_02_signal_routing.txt` (0.529)<br>`experiments/hard_multihop_corpus/docs/comet_05_error_catalog.txt` (0.493)<br>`experiments/hard_multihop_corpus/docs/comet_06_change_note.txt` (0.422)<br>`experiments/hard_multihop_corpus/docs/delta_02_signal_routing.txt` (0.421)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/beacon_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/comet_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/delta_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/comet_02_signal_routing.txt` (5.000); path: Tailwind
- Detected seed entities: Tailwind, 警報, 調査
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/comet_03_service_ownership.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 3. seed entity matching failure
- Classification rationale: The generic seeds 調査 and 警報 connect to repeated similar-terms documents across all programs and outrank the Tailwind path.

## hq03b — multi_hop

- Question: Tailwind の警報を理由に公開例外を申請するときの最終承認者は誰ですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/comet_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/comet_04_exception_register.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/comet_01_signal_registry.txt` (0.536)<br>`experiments/hard_multihop_corpus/docs/comet_02_signal_routing.txt` (0.481)<br>`experiments/hard_multihop_corpus/docs/comet_05_error_catalog.txt` (0.470)<br>`experiments/hard_multihop_corpus/docs/comet_06_change_note.txt` (0.432)<br>`experiments/hard_multihop_corpus/docs/atlas_04_exception_register.txt` (0.425)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (9.833); path: 公開例外<br>`experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (7.833); path: 例外<br>`experiments/hard_multihop_corpus/docs/beacon_07_similar_terms.txt` (7.833); path: 例外<br>`experiments/hard_multihop_corpus/docs/comet_07_similar_terms.txt` (7.833); path: 例外<br>`experiments/hard_multihop_corpus/docs/delta_07_similar_terms.txt` (7.833); path: 例外
- Detected seed entities: Tailwind, 公開例外, 警報, 例外
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/comet_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/comet_04_exception_register.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 3. seed entity matching failure
- Classification rationale: 公開例外 and 例外 match generic cross-program nodes, so the Comet-specific route and approval documents are displaced.

## hq03c — multi_hop

- Question: 障害コード E-63 を見つけた場合、復旧確認まで担当する組織はどこですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/comet_05_error_catalog.txt`, `experiments/hard_multihop_corpus/docs/comet_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/comet_03_service_ownership.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/delta_05_error_catalog.txt` (0.499)<br>`experiments/hard_multihop_corpus/docs/comet_05_error_catalog.txt` (0.491)<br>`experiments/hard_multihop_corpus/docs/atlas_05_error_catalog.txt` (0.465)<br>`experiments/hard_multihop_corpus/docs/beacon_05_error_catalog.txt` (0.464)<br>`experiments/hard_multihop_corpus/docs/delta_07_similar_terms.txt` (0.397)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/comet_05_error_catalog.txt` (6.000); path: E-63<br>`experiments/hard_multihop_corpus/docs/comet_07_similar_terms.txt` (4.500); path: E-63 → Comet<br>`experiments/hard_multihop_corpus/docs/comet_02_signal_routing.txt` (3.333); path: E-63 → Comet<br>`experiments/hard_multihop_corpus/docs/comet_08_release_note.txt` (3.333); path: E-63 → Comet<br>`experiments/hard_multihop_corpus/docs/comet_01_signal_registry.txt` (2.000); path: E-63 → Comet
- Detected seed entities: E-63
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/comet_03_service_ownership.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: E-63 reaches Tailwind and Comet Router, but the shared 一次対応者 node brings other error-catalog chunks above the ownership document.

## hq03d — relationship

- Question: Comet Router の運用責任組織はどこですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/comet_03_service_ownership.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/comet_03_service_ownership.txt` (0.696)<br>`experiments/hard_multihop_corpus/docs/comet_06_change_note.txt` (0.639)<br>`experiments/hard_multihop_corpus/docs/comet_04_exception_register.txt` (0.628)<br>`experiments/hard_multihop_corpus/docs/comet_02_signal_routing.txt` (0.604)<br>`experiments/hard_multihop_corpus/docs/comet_08_release_note.txt` (0.583)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/comet_07_similar_terms.txt` (8.500); path: Comet<br>`experiments/hard_multihop_corpus/docs/comet_02_signal_routing.txt` (6.500); path: Comet<br>`experiments/hard_multihop_corpus/docs/comet_08_release_note.txt` (6.500); path: Comet<br>`experiments/hard_multihop_corpus/docs/comet_05_error_catalog.txt` (5.000); path: Comet<br>`experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (4.833); path: Comet → 例外
- Detected seed entities: Comet Router, Comet
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/comet_03_service_ownership.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 3. seed entity matching failure
- Classification rationale: The exact service seed is accompanied by the broad Comet seed, whose repeated provenance outranks the ownership document.

## hq03e — relationship

- Question: Comet Router の公開例外の最終承認者は誰ですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/comet_04_exception_register.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/comet_04_exception_register.txt` (0.700)<br>`experiments/hard_multihop_corpus/docs/comet_06_change_note.txt` (0.673)<br>`experiments/hard_multihop_corpus/docs/comet_03_service_ownership.txt` (0.670)<br>`experiments/hard_multihop_corpus/docs/comet_08_release_note.txt` (0.621)<br>`experiments/hard_multihop_corpus/docs/comet_02_signal_routing.txt` (0.597)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (9.833); path: 公開例外<br>`experiments/hard_multihop_corpus/docs/comet_07_similar_terms.txt` (9.000); path: Comet<br>`experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (6.500); path: 例外<br>`experiments/hard_multihop_corpus/docs/beacon_07_similar_terms.txt` (6.500); path: 例外<br>`experiments/hard_multihop_corpus/docs/comet_02_signal_routing.txt` (6.500); path: Comet
- Detected seed entities: Comet Router, Comet, 公開例外, 例外
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/comet_04_exception_register.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 3. seed entity matching failure
- Classification rationale: The broad Comet, 公開例外, and 例外 seeds displace the Comet-specific approval document.

## hq04a — multi_hop

- Question: Tidepool の警報が出たとき、調査を開始する運用責任組織はどこですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/delta_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/delta_03_service_ownership.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/delta_02_signal_routing.txt` (0.576)<br>`experiments/hard_multihop_corpus/docs/delta_01_signal_registry.txt` (0.568)<br>`experiments/hard_multihop_corpus/docs/delta_05_error_catalog.txt` (0.548)<br>`experiments/hard_multihop_corpus/docs/delta_06_change_note.txt` (0.471)<br>`experiments/hard_multihop_corpus/docs/beacon_02_signal_routing.txt` (0.436)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/beacon_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/comet_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/delta_07_similar_terms.txt` (7.833); path: 調査<br>`experiments/hard_multihop_corpus/docs/delta_05_error_catalog.txt` (7.500); path: Tidepool
- Detected seed entities: Tidepool, 警報, 調査
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/delta_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/delta_03_service_ownership.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 3. seed entity matching failure
- Classification rationale: The generic seeds 調査 and 警報 connect to repeated similar-terms documents across all programs and outrank the Tidepool path.

## hq04b — multi_hop

- Question: Tidepool の警報を理由に公開例外を申請するときの最終承認者は誰ですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/delta_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/delta_04_exception_register.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/delta_01_signal_registry.txt` (0.513)<br>`experiments/hard_multihop_corpus/docs/delta_02_signal_routing.txt` (0.506)<br>`experiments/hard_multihop_corpus/docs/delta_05_error_catalog.txt` (0.493)<br>`experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (0.471)<br>`experiments/hard_multihop_corpus/docs/delta_06_change_note.txt` (0.461)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (9.833); path: 公開例外<br>`experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (7.833); path: 例外<br>`experiments/hard_multihop_corpus/docs/beacon_07_similar_terms.txt` (7.833); path: 例外<br>`experiments/hard_multihop_corpus/docs/comet_07_similar_terms.txt` (7.833); path: 例外<br>`experiments/hard_multihop_corpus/docs/delta_07_similar_terms.txt` (7.833); path: 例外
- Detected seed entities: Tidepool, 公開例外, 警報, 例外
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/delta_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/delta_04_exception_register.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 3. seed entity matching failure
- Classification rationale: 公開例外 and 例外 match generic cross-program nodes, so the Delta-specific route and approval documents are displaced.

## hq04c — multi_hop

- Question: 障害コード E-74 を見つけた場合、復旧確認まで担当する組織はどこですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/delta_05_error_catalog.txt`, `experiments/hard_multihop_corpus/docs/delta_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/delta_03_service_ownership.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/delta_05_error_catalog.txt` (0.553)<br>`experiments/hard_multihop_corpus/docs/atlas_05_error_catalog.txt` (0.482)<br>`experiments/hard_multihop_corpus/docs/beacon_05_error_catalog.txt` (0.474)<br>`experiments/hard_multihop_corpus/docs/comet_05_error_catalog.txt` (0.467)<br>`experiments/hard_multihop_corpus/docs/delta_07_similar_terms.txt` (0.410)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/delta_05_error_catalog.txt` (7.333); path: E-74<br>`experiments/hard_multihop_corpus/docs/atlas_05_error_catalog.txt` (3.833); path: E-74 → 一次対応者<br>`experiments/hard_multihop_corpus/docs/beacon_05_error_catalog.txt` (3.833); path: E-74 → 一次対応者<br>`experiments/hard_multihop_corpus/docs/delta_08_release_note.txt` (2.833); path: E-74 → Tidepool<br>`experiments/hard_multihop_corpus/docs/delta_01_signal_registry.txt` (1.833); path: E-74 → Tidepool
- Detected seed entities: E-74
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/delta_02_signal_routing.txt`, `experiments/hard_multihop_corpus/docs/delta_03_service_ownership.txt`
- Vector retrieves all required evidence: no
- Graph failure category: 5. traversal/ranking failure
- Classification rationale: E-74 reaches Tidepool and Delta Gateway, but the shared 一次対応者 node brings other error-catalog chunks above the required routing and ownership documents.

## hq04d — relationship

- Question: Delta Gateway の運用責任組織はどこですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/delta_03_service_ownership.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/delta_03_service_ownership.txt` (0.603)<br>`experiments/hard_multihop_corpus/docs/delta_06_change_note.txt` (0.551)<br>`experiments/hard_multihop_corpus/docs/delta_02_signal_routing.txt` (0.516)<br>`experiments/hard_multihop_corpus/docs/delta_04_exception_register.txt` (0.509)<br>`experiments/hard_multihop_corpus/docs/delta_08_release_note.txt` (0.484)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/delta_07_similar_terms.txt` (8.500); path: Delta<br>`experiments/hard_multihop_corpus/docs/delta_04_exception_register.txt` (6.500); path: Delta<br>`experiments/hard_multihop_corpus/docs/delta_08_release_note.txt` (6.500); path: Delta<br>`experiments/hard_multihop_corpus/docs/delta_05_error_catalog.txt` (4.833); path: Delta<br>`experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (4.833); path: Delta → 例外
- Detected seed entities: Delta Gateway, Delta
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/delta_03_service_ownership.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 3. seed entity matching failure
- Classification rationale: The exact service seed is accompanied by the broad Delta seed, whose repeated provenance outranks the ownership document.

## hq04e — relationship

- Question: Delta Gateway の公開例外の最終承認者は誰ですか？
- Required relevant documents: `experiments/hard_multihop_corpus/docs/delta_04_exception_register.txt`
- Vector top-5 documents and scores: `experiments/hard_multihop_corpus/docs/delta_04_exception_register.txt` (0.575)<br>`experiments/hard_multihop_corpus/docs/delta_06_change_note.txt` (0.555)<br>`experiments/hard_multihop_corpus/docs/delta_03_service_ownership.txt` (0.540)<br>`experiments/hard_multihop_corpus/docs/delta_08_release_note.txt` (0.496)<br>`experiments/hard_multihop_corpus/docs/delta_02_signal_routing.txt` (0.484)
- Graph top-5 documents: `experiments/hard_multihop_corpus/docs/beacon_04_exception_register.txt` (9.833); path: 公開例外<br>`experiments/hard_multihop_corpus/docs/delta_07_similar_terms.txt` (9.000); path: Delta<br>`experiments/hard_multihop_corpus/docs/atlas_07_similar_terms.txt` (6.500); path: 例外<br>`experiments/hard_multihop_corpus/docs/beacon_07_similar_terms.txt` (6.500); path: 例外<br>`experiments/hard_multihop_corpus/docs/comet_07_similar_terms.txt` (6.500); path: 例外
- Detected seed entities: Delta Gateway, Delta, 公開例外, 例外
- Required documents missed by Graph: `experiments/hard_multihop_corpus/docs/delta_04_exception_register.txt`
- Vector retrieves all required evidence: yes
- Graph failure category: 3. seed entity matching failure
- Classification rationale: The broad Delta, 公開例外, and 例外 seeds displace the Delta-specific approval document.
