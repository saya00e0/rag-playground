"""Generate frozen questions for the fictional hard-multihop corpus."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from generate_hard_multihop_corpus import PROGRAMS


def doc(program: str, suffix: str) -> str:
    return f"experiments/hard_multihop_corpus/docs/{program.lower()}_{suffix}.txt"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="experiments/hard_multihop_corpus/eval/dataset.jsonl")
    args = parser.parse_args()
    output = Path(args.output)
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing dataset: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, (program, signal, service, team, approver, code) in enumerate(PROGRAMS, 1):
        rows.extend(
            [
                {"id": f"hq{index:02d}a", "type": "multi_hop", "question": f"{signal} の警報が出たとき、調査を開始する運用責任組織はどこですか？", "relevant_docs": [doc(program, "02_signal_routing"), doc(program, "03_service_ownership")], "evidence": "信号のルーティング先と、そのサービスの運用責任を接続する。"},
                {"id": f"hq{index:02d}b", "type": "multi_hop", "question": f"{signal} の警報を理由に公開例外を申請するときの最終承認者は誰ですか？", "relevant_docs": [doc(program, "02_signal_routing"), doc(program, "04_exception_register")], "evidence": "信号からサービスを特定し、サービス別の承認台帳を参照する。"},
                {"id": f"hq{index:02d}c", "type": "multi_hop", "question": f"障害コード {code} を見つけた場合、復旧確認まで担当する組織はどこですか？", "relevant_docs": [doc(program, "05_error_catalog"), doc(program, "02_signal_routing"), doc(program, "03_service_ownership")], "evidence": "障害コード、信号のルーティング、サービス所有を順に接続する。"},
                {"id": f"hq{index:02d}d", "type": "relationship", "question": f"{service} の運用責任組織はどこですか？", "relevant_docs": [doc(program, "03_service_ownership")], "evidence": "サービス所有資料に運用責任を明記。"},
                {"id": f"hq{index:02d}e", "type": "relationship", "question": f"{service} の公開例外の最終承認者は誰ですか？", "relevant_docs": [doc(program, "04_exception_register")], "evidence": "承認台帳にサービス別の最終承認者を明記。"},
                {"id": f"hq{index:02d}f", "type": "factual", "question": f"障害コード {code} は何を意味しますか？", "relevant_docs": [doc(program, "05_error_catalog")], "evidence": "障害コード台帳に意味を明記。"},
            ]
        )
    output.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    print(f"generated {len(rows)} questions")


if __name__ == "__main__":
    main()
