"""Generate a fictional corpus whose multi-hop answers are split across documents."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PROGRAMS = (
    ("Atlas", "Northstar", "Atlas Relay", "運用基盤チーム", "山岸紬", "E-41"),
    ("Beacon", "Lighthouse", "Beacon Bridge", "データ信頼性チーム", "小野寺蓮", "E-52"),
    ("Comet", "Tailwind", "Comet Router", "顧客運用チーム", "川村結", "E-63"),
    ("Delta", "Tidepool", "Delta Gateway", "決済監視チーム", "藤原蒼", "E-74"),
)


def documents_for(program: str, signal: str, service: str, team: str, approver: str, code: str) -> dict[str, str]:
    header = f"架空の hard-multihop 評価資料 — {program}\n実在の組織、人物、顧客、認証情報は含まれません。\n\n"
    return {
        "01_signal_registry": header + f"{signal} は {program} の配信遅延を検知する監視信号です。{signal} の警報は利用者向け通知を止める根拠になります。信号名は担当組織や承認者を表しません。\n",
        "02_signal_routing": header + f"{signal} の警報は {service} へルーティングされます。{service} は警報の重複を除去し、調査キューを作ります。信号を受け取るサービスの担当組織は、この資料には記載しません。\n",
        "03_service_ownership": header + f"{service} の運用責任は {team} にあります。{team} はサービス障害の調査開始と復旧確認を担当します。承認権限は別の承認台帳で定義します。\n",
        "04_exception_register": header + f"{service} の警報を理由に公開例外を申請する場合、最終承認者は {approver} です。{approver} は運用調査の担当者ではありません。例外申請にはルーティング済みの警報IDが必要です。\n",
        "05_error_catalog": header + f"障害コード {code} は {signal} の入力遅延を意味します。コードを見つけた一次対応者は、該当信号のルーティング先を確認して調査を開始します。この資料にはサービス名と担当組織を記載しません。\n",
        "06_change_note": header + f"{service} は今期、監視ログの保存先を変更しました。変更後も {signal} の警報経路と運用責任は変わりません。保存先変更の承認者は公開例外の承認者とは別です。\n",
        "07_similar_terms": header + f"{program} では「警報」「例外」「調査」という語を使いますが、単語だけで担当組織を決めてはいけません。担当を確認するにはサービス名、承認者を確認するにはサービス別の承認台帳が必要です。\n",
        "08_release_note": header + f"{program} の次回リリースは監視表示の改善を含みます。{signal} のしきい値、{service} の担当、例外承認の規則はリリースノートでは変更しません。\n",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="experiments/hard_multihop_corpus")
    args = parser.parse_args()
    root = Path(args.output)
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"refusing to write into non-empty directory: {root}")
    docs = root / "docs"
    docs.mkdir(parents=True)
    manifest = []
    for program, signal, service, team, approver, code in PROGRAMS:
        for suffix, content in documents_for(program, signal, service, team, approver, code).items():
            name = f"{program.lower()}_{suffix}.txt"
            (docs / name).write_text(content, encoding="utf-8")
            manifest.append({"program": program, "path": f"docs/{name}"})
    (root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(manifest)} documents")


if __name__ == "__main__":
    main()
