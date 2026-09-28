"""Generate a fixed, evidence-labelled dataset for the large synthetic corpus."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from generate_large_synthetic_corpus import PROJECTS


def document_path(index: int, project: str, topic: str) -> str:
    return f"experiments/large_synthetic_corpus/docs/{index:02d}_{project.lower()}_{topic}.txt"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="experiments/large_synthetic_corpus/eval/dataset.jsonl")
    args = parser.parse_args()
    output = Path(args.output)
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing dataset: {output}")
    output.parent.mkdir(parents=True, exist_ok=False)

    records = []
    for index, values in enumerate(PROJECTS, 1):
        project, lead, technical, security, operations, procurement = values
        release = f"{project} 3.{index}"
        service = f"{project} Catalog Service"
        policy = f"{project} Policy Service"
        gateway = f"{project} Gateway API"
        vector = f"{project} Vector Index"
        department = f"第{index}調達部"
        paths = {topic: document_path(index, project, topic) for topic in ("01_overview", "02_team", "03_architecture", "04_release", "05_incident", "06_governance", "07_operations", "08_acceptance")}
        records.extend(
            [
                {"question": f"{release} の公開予定日はいつですか？", "type": "factual", "relevant_docs": [paths["04_release"]], "evidence": "リリース計画に公開予定日を明記。"},
                {"question": f"{department} の公開規則に問題がある場合、最終的に公開可否を判断するのは誰ですか？", "type": "factual", "relevant_docs": [paths["06_governance"]], "evidence": "公開ガバナンスに最終判断者を明記。"},
                {"question": f"{gateway} または {service} の技術問題は誰にエスカレーションしますか？", "type": "relationship", "relevant_docs": [paths["02_team"], paths["07_operations"]], "evidence": "担当者一覧と運用手順が同じ技術エスカレーション先を裏付ける。"},
                {"question": f"{policy} の公開前レビュー責任者は誰ですか？", "type": "relationship", "relevant_docs": [paths["02_team"], paths["03_architecture"]], "evidence": "担当者一覧とアーキテクチャがセキュリティ責任者を裏付ける。"},
                {"question": f"{release} の公開前に必要な {service} の負荷試験と {policy} のアクセス規則レビューは、それぞれ誰が担当しますか？", "type": "multi_hop", "relevant_docs": [paths["03_architecture"], paths["04_release"], paths["08_acceptance"]], "evidence": "アーキテクチャで各サービスの役割、リリース計画と受入条件で試験・レビュー担当を確認する。"},
                {"question": f"{gateway} の証明書更新障害では、誰が一次対応し、誰が技術調査を担当し、なぜ {policy} の臨時レビューが不要でしたか？", "type": "multi_hop", "relevant_docs": [paths["02_team"], paths["05_incident"], paths["07_operations"]], "evidence": "障害報告の実績、担当者一覧と運用手順の通常役割を照合する。"},
            ]
        )

    for number, record in enumerate(records, 1):
        record["id"] = f"lq{number:03d}"
    output.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records), encoding="utf-8")
    distribution = {kind: sum(record["type"] == kind for record in records) for kind in ("factual", "relationship", "multi_hop")}
    print(json.dumps({"question_count": len(records), "distribution": distribution, "output": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
