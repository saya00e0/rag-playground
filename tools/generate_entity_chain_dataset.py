"""Generate frozen questions for the fictional entity-chain corpus.

`relevant_docs` holds document IDs. A multi-hop question lists every document
needed to derive the answer, so partial retrieval scores as a fraction of the
required chain. The one-hop controls name the anchor entity directly and exist
to show whether any graph advantage is specific to the chained question shape.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from generate_entity_chain_corpus import CHAINS


def doc(index: int, suffix: str) -> str:
    return f"experiments/entity_chain_corpus/docs/chain{index:02d}_{suffix}.txt"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="experiments/entity_chain_corpus/eval/dataset.jsonl")
    args = parser.parse_args()
    output = Path(args.output)
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing dataset: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, (person, project, company, sensor) in enumerate(CHAINS, 1):
        rows.extend(
            [
                {
                    "id": f"cq{index:02d}a",
                    "type": "multi_hop",
                    "question": f"{person}氏が関係する企業が開発したセンサーは？",
                    "relevant_docs": [doc(index, "01_researcher"), doc(index, "02_partnership"), doc(index, "03_product")],
                    "evidence": "研究員からプロジェクト、プロジェクトから企業、企業から製品を順に接続する。質問はプロジェクト名も企業名も含まない。",
                },
                {
                    "id": f"cq{index:02d}b",
                    "type": "relationship",
                    "question": f"{company} が開発したセンサーは何ですか？",
                    "relevant_docs": [doc(index, "03_product")],
                    "evidence": "製品資料に開発元と製品名を明記。質問が企業名を直接含む一ホップの対照。",
                },
                {
                    "id": f"cq{index:02d}c",
                    "type": "factual",
                    "question": f"{person}氏はどのプロジェクトの主任研究員ですか？",
                    "relevant_docs": [doc(index, "01_researcher")],
                    "evidence": "研究員資料に担当プロジェクトを明記。質問が人物名を直接含む一ホップの対照。",
                },
            ]
        )
    output.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    print(f"generated {len(rows)} questions")


if __name__ == "__main__":
    main()
