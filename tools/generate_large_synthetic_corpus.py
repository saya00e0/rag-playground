"""Generate a non-sensitive, cross-document corpus for retrieval experiments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PROJECTS = [
    ("Aurora", "佐藤真央", "田中健", "鈴木梨奈", "高橋悠", "伊藤彩"),
    ("Borealis", "山本花", "中村陸", "小林葵", "加藤湊", "森優衣"),
    ("Cirrus", "渡辺紬", "吉田蓮", "斎藤結", "岡田晴", "石井凛"),
    ("Drift", "清水葵", "山田蒼", "藤田澪", "橋本湊", "阿部紗良"),
    ("Ember", "井上楓", "松本陽", "池田紬", "前田陸", "木村結衣"),
    ("Fjord", "林真央", "斉藤陽菜", "坂本蓮", "村上葵", "近藤凛"),
    ("Grove", "石川澪", "後藤蒼", "西村楓", "藤井晴", "福田紬"),
    ("Harbor", "岡本結", "長谷川陸", "原田葵", "三浦陽", "竹内凛"),
    ("Indigo", "中川楓", "小川蒼", "平野澪", "川口晴", "青木紬"),
    ("Juniper", "松田結", "遠藤蓮", "菅原葵", "野口陽", "大野凛"),
]


def document_header(project: str, topic: str) -> str:
    return f"""合成ベンチマーク文書 — {project} プログラム {topic}

この文書は Vector RAG と GraphRAG の評価専用に作成した架空資料です。実在の組織、人物、顧客、認証情報、秘密情報は含みません。各事実は複数文書に意図的に分散しています。

"""


def documents_for_project(index: int, values: tuple[str, str, str, str, str, str]) -> dict[str, str]:
    project, lead, technical, security, operations, procurement = values
    service = f"{project} Catalog Service"
    policy = f"{project} Policy Service"
    gateway = f"{project} Gateway API"
    vector = f"{project} Vector Index"
    release = f"{project} 3.{index}"
    department = f"第{index}調達部"
    incident_date = f"2026年{index}月{(index + 2):02d}日"
    maintenance = f"毎月第{(index % 4) + 1}日曜日の午前{(index % 3) + 1}時から{(index % 3) + 3}時"

    return {
        "01_overview": document_header(project, "概要") + f"""{project} は {department} の製品仕様書検索を改善する社内プログラムです。プログラム責任者は {lead}、技術責任者は {technical} です。最初の公開対象は、調達部が更新する仕様書と承認済みの付属資料です。

最初のリリースは {release} です。{release} は {service}、{policy}、{vector}、{gateway} を利用します。検索候補の生成は {vector}、公開規則の判定は {policy}、利用者への応答は {gateway} が担当します。

成功指標は上位3件再現率、平均検索応答時間、未承認文書を返さないことです。公開可否は {lead} が最終判断しますが、判断前には技術、セキュリティ、調達確認が必要です。

このプログラムでは文書名、担当者名、サービス名が文書ごとに別の表現で現れることがあります。評価では、同一プロジェクトの関係を結びつける検索能力だけを確認し、別プロジェクトの同名概念を正解とみなしません。
""",
        "02_team": document_header(project, "担当者と連絡経路") + f"""{lead} は {project} の公開判断、優先順位、{department} との調整を担当します。{technical} は {service} と {vector} の設計、性能問題の技術調査、負荷試験を担当します。

{security} は {policy} のアクセス規則、公開前レビュー、規則違反時の判断材料の整理を担当します。{operations} は監視、一次対応、定期メンテナンス、復旧確認を担当します。{procurement} は {department} の窓口であり、仕様書更新とサンプル確認を担当します。

{gateway} または {service} の技術問題は {technical} へエスカレーションします。{policy} のアクセス規則問題は {security} へエスカレーションします。公開延期の連絡は {lead} が {procurement} に行います。

担当者一覧は役割を示すための文書であり、障害の詳細や公開条件そのものは別文書にあります。したがって、担当者と具体的な手順を同時に問う質問では、少なくとも二つの文書を必要とします。
""",
        "03_architecture": document_header(project, "アーキテクチャ") + f"""利用者の検索要求は {gateway} を通り {service} に渡されます。{service} は {vector} に候補検索を依頼し、候補の文書IDを受け取ります。その後、{service} は候補を {policy} に渡します。

{policy} は利用者の所属と文書の公開規則を照合し、許可した候補だけを {gateway} に返します。{vector} は公開可否を判定しません。アクセス規則の変更は {vector} ではなく {policy} に反映する必要があります。

{service} の所有チームはプラットフォーム部で、設計責任者は {technical} です。{policy} の公開前レビュー責任者は {security} です。{gateway} の稼働状況は {operations} が監視します。

この構成では、候補検索、規則判定、応答送信は別サービスです。質問が「どのサービスが候補を作るか」を尋ねる場合と、「どのサービスが未承認文書を除外するか」を尋ねる場合では、異なる証拠文書が必要になります。
""",
        "04_release": document_header(project, "リリース計画") + f"""{release} の公開予定日は 2026年{index}月{(index + 10):02d}日です。公開前には {service} の負荷試験、{policy} のアクセス規則レビュー、{department} による仕様書サンプル確認を完了しなければなりません。

負荷試験の担当は {technical}、アクセス規則レビューの担当は {security}、仕様書サンプル確認の担当は {procurement} です。三つすべての完了報告を受けた後、{lead} が公開可否を決定します。

公開判定前日までに未解決の高優先度障害がある場合、公開は延期されます。延期の連絡は {lead} が {procurement} に行い、{procurement} は {department} の関係者へ連絡します。

リリース計画は日付と前提条件を示しますが、各前提条件の技術的な実装方法はアーキテクチャ文書、各担当者の通常業務は担当者一覧を参照します。
""",
        "05_incident": document_header(project, "障害報告") + f"""{incident_date}、{gateway} の証明書更新失敗により {project} の検索要求が失敗しました。{vector} と {policy} は正常でした。{operations} が監視通知を受けて一次対応を開始し、証明書設定の技術調査を {technical} へエスカレーションしました。

{technical} は {gateway} の証明書設定を修正し、同日中に検索要求の復旧を確認しました。アクセス規則に変更はなかったため、{security} による {policy} の臨時レビューは不要でした。

この障害は公開判定前の高優先度障害として記録されましたが、復旧確認後に解決済みとなりました。再発防止として {operations} は証明書期限の監視を追加します。

障害報告は一次対応と技術調査の実績を示します。通常時の技術エスカレーション経路は担当者一覧、公開延期の規則はリリース計画にあります。
""",
        "06_governance": document_header(project, "公開ガバナンス") + f"""{department} の製品仕様書は、{procurement} が更新を確認した後に公開候補となります。公開候補は {service} に登録される前に {policy} のアクセス規則レビューを受けます。レビュー責任者は {security} です。

公開規則には「{department}のみ」「全社公開」「指定プロジェクトのみ」の三種類があります。規則が未設定の文書は公開してはなりません。{policy} が拒否した文書IDは {gateway} から利用者へ返してはなりません。

公開規則に問題が見つかった場合、{security} は {lead} へ報告します。公開可否の最終判断は {lead} が行います。{procurement} は判断後の仕様書状態を {department} に確認します。

ガバナンス文書は公開規則と判断経路を示します。候補検索の仕組みはアーキテクチャ文書、公開日の前提条件はリリース計画にあります。
""",
        "07_operations": document_header(project, "運用手順") + f"""{project} の定期メンテナンスは {maintenance} です。メンテナンス中、{gateway} は計画停止し、検索要求を受け付けません。{operations} は開始前に社内ポータルへ告知を掲載し、完了後に疎通確認を行います。

検索失敗の一次対応は {operations} が担当します。{gateway} または {service} の技術問題は {technical} へ、{policy} のアクセス規則問題は {security} へエスカレーションします。

平均検索応答時間が2秒を超える状態が15分続いた場合、{operations} は性能障害として記録します。{vector} の候補検索時間と {policy} の判定時間を分けて確認します。

運用手順は監視と一次対応を説明します。障害の発生日時や原因は障害報告、公開延期の判断はリリース計画にあります。
""",
        "08_acceptance": document_header(project, "受入条件") + f"""{release} は {department} の製品仕様書を対象に受入試験を行います。試験では、{service} が {vector} から候補を取得し、{policy} が未設定規則の文書を除外することを確認します。

合格条件は、定義済み評価セットに対する上位3件再現率が0.80以上、平均検索応答時間が2秒以下、規則が未設定の文書IDを {gateway} が返さないことです。

{technical} は性能と候補検索の試験結果を、{security} はアクセス規則の試験結果を提出します。{lead} は両方の結果と {procurement} の仕様書サンプル確認を受けて、公開可否を決定します。

受入条件は合格基準を示します。実際の公開予定日と延期条件はリリース計画、サービス間の経路はアーキテクチャ文書を参照します。
""",
        "09_integration": document_header(project, "外部連携記録") + f"""{project} は {department} の仕様書更新を毎営業日に受け取ります。{procurement} が更新通知を確認した後、{service} の登録候補一覧に文書IDを追加します。登録候補が公開される前には、{policy} の規則レビューが必要です。

{service} は候補検索時に {vector} を利用しますが、公開規則を保存または上書きしません。規則の状態は {policy} が管理し、利用者への返却可否は {gateway} の応答直前に確認されます。

連携停止が発生した場合、{operations} が一次対応を記録し、技術的な原因は {technical} が調査します。規則誤りが原因の場合は {security} が確認します。

この記録は更新通知とサービス連携の関係を示します。公開の最終判断者と公開延期の連絡先は担当者・リリース文書で確認します。
""",
        "10_decision_log": document_header(project, "判断ログ") + f"""{project} の公開判断会議では、{lead}、{technical}、{security}、{procurement} が確認結果を共有します。{technical} は {service} の負荷試験と {vector} の候補検索結果を説明します。{security} は {policy} の規則レビューを説明します。

{procurement} は {department} の仕様書サンプル確認を説明します。未解決の高優先度障害がある場合、{lead} は公開を延期し、{procurement} を通じて {department} へ連絡します。

検索結果に未承認文書が含まれた場合、{security} は {policy} の設定を再確認します。{gateway}、{service}、{vector} の性能問題は {technical} と {operations} が切り分けます。

判断ログは複数の役割と確認結果を結びつけますが、各事実の一次資料はリリース計画、受入条件、障害報告、公開ガバナンスにあります。
""",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="experiments/large_synthetic_corpus")
    args = parser.parse_args()
    root = Path(args.output)
    documents_dir = root / "docs"
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"refusing to write into non-empty directory: {root}")
    documents_dir.mkdir(parents=True, exist_ok=False)

    manifest = []
    for index, project in enumerate(PROJECTS, 1):
        for topic, content in documents_for_project(index, project).items():
            relative_path = Path("docs") / f"{index:02d}_{project[0].lower()}_{topic}.txt"
            destination = root / relative_path
            destination.write_text(content, encoding="utf-8")
            manifest.append({"project": project[0], "topic": topic, "path": str(relative_path)})
    (root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(manifest)} documents in {documents_dir}")


if __name__ == "__main__":
    main()
