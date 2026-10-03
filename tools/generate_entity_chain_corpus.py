"""Generate a fictional corpus whose answers require a researcher-company-product chain.

Each chain splits one fact across three documents and never names the
intermediate project or company in the final product document, so a question
anchored on the researcher cannot be answered from any single document.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CHAINS = (
    ("田中", "Project Falcon", "Acme社", "LiDARセンサー L7"),
    ("佐々木", "Project Mistral", "Borealis社", "音響センサー A3"),
    ("村上", "Project Kestrel", "Cindermark社", "熱画像センサー T9"),
    ("岡田", "Project Lumen", "Dravnic社", "近接センサー P2"),
)


def documents_for(index: int, person: str, project: str, company: str, sensor: str) -> dict[str, str]:
    header = f"架空の entity-chain 評価資料 — chain{index:02d}\n実在の企業、人物、製品は含まれません。\n\n"
    return {
        "01_researcher": header + f"{person}氏は {project} の主任研究員である。{person}氏の所属企業名と担当製品はこの資料には記載しない。\n",
        "02_partnership": header + f"{project} は {company} との共同プロジェクトである。{project} の研究員名簿と成果物の一覧はこの資料には含まれない。\n",
        "03_product": header + f"{company} は新しい {sensor} を開発した。{sensor} の納入先と研究体制はこの資料には記載しない。\n",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="experiments/entity_chain_corpus")
    args = parser.parse_args()
    root = Path(args.output)
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"refusing to write into non-empty directory: {root}")
    docs = root / "docs"
    docs.mkdir(parents=True)
    manifest = []
    for index, (person, project, company, sensor) in enumerate(CHAINS, 1):
        for suffix, content in documents_for(index, person, project, company, sensor).items():
            name = f"chain{index:02d}_{suffix}.txt"
            (docs / name).write_text(content, encoding="utf-8")
            manifest.append({"chain": f"chain{index:02d}", "path": f"docs/{name}"})
    (root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(manifest)} documents")


if __name__ == "__main__":
    main()
