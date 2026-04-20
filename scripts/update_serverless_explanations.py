#!/usr/bin/env python3
"""
AWS SAP-C02 「サーバーレス移行・モダナイゼーション」テーマの解説に
判断ポイントを加筆するスクリプト。

仕様:
- explanation.detail の末尾に「📌 判断ポイント」セクションを追加
- 既に追加済みのものはスキップ
- answer/question/choices/id/num/tags/source は変更しない
- サブカテゴリ別に異なる判断ポイントを追加
- 書き込み直前にファイルを再読み込みして対象問題のみ差し替え
"""

import json
import re
from pathlib import Path

QUESTIONS_PATH = Path("/Users/aki/aws-sap/docs/data/questions.json")

# ===== 対象抽出ロジック =====

MODERNIZATION_KWS = [
    "サーバーレス",
    "モノリス",
    "モダナイ",
    "Strangler",
    "マイクロサービス",
    "リファクタリング",
    "リプラットフォーム",
    "コンテナ化",
    "段階的移行",
]

SERVERLESS_SERVICES = [
    "Lambda",
    "Step Functions",
    "Fargate",
    "EventBridge",
    "API Gateway",
    "Aurora Serverless",
    "App Runner",
]


def get_choice_text(c):
    if isinstance(c, dict):
        return c.get("text", "")
    return str(c)


def get_choice_label(c):
    if isinstance(c, dict):
        return c.get("label", "")
    m = re.match(r"^([A-E])\.", str(c))
    return m.group(1) if m else ""


def is_target(q):
    tags = q.get("tags", [])
    if "serverless" in tags:
        return True
    question = q.get("question", "")
    if any(kw in question for kw in MODERNIZATION_KWS):
        return True
    answer_labels = q.get("answer", [])
    correct_text = ""
    for c in q.get("choices", []):
        if get_choice_label(c) in answer_labels:
            correct_text += " " + get_choice_text(c)
    if any(kw in correct_text for kw in SERVERLESS_SERVICES):
        # かつ選択肢に少なくとも 1 つサーバーレス系が登場
        for c in q.get("choices", []):
            ctext = get_choice_text(c)
            if any(kw in ctext for kw in SERVERLESS_SERVICES):
                return True
    return False


# ===== サブカテゴリ判定 =====

def classify(q):
    question = q.get("question", "")
    answer_labels = q.get("answer", [])
    correct_text = ""
    all_choices_text = ""
    for c in q.get("choices", []):
        ctext = get_choice_text(c)
        all_choices_text += " " + ctext
        if get_choice_label(c) in answer_labels:
            correct_text += " " + ctext
    full = question + " " + all_choices_text

    cats = []
    # Lambda 15 分制限・長時間処理の判断
    if re.search(
        r"15\s*分|15-?minute|長時間.*(バッチ|処理|ジョブ)|数時間|数十分|タイムアウト|処理時間.{0,10}超",
        full,
    ) and ("Lambda" in full or "Fargate" in full or "Step Functions" in full):
        cats.append("lambda_limit")
    # Fargate vs Lambda / EC2 のコンピュート選択
    if "Fargate" in full and ("Lambda" in full or "EC2" in full or "ECS" in full):
        cats.append("fargate_choice")
    # Step Functions オーケストレーション
    if "Step Functions" in full or "Step Function" in full:
        cats.append("step_functions")
    # EventBridge vs SNS の使い分け
    if "EventBridge" in full and "SNS" in full:
        cats.append("eventbridge_vs_sns")
    # SQS FIFO vs Standard
    if "FIFO" in full and "SQS" in full:
        cats.append("sqs_fifo")
    # Aurora Serverless v1/v2
    if "Aurora Serverless" in full or "Aurora serverless" in full:
        cats.append("aurora_serverless")
    # モノリス分割 (Strangler Fig)
    if any(kw in full for kw in ["モノリス", "Strangler", "マイクロサービス化", "段階的移行"]):
        cats.append("monolith_split")
    # サーバーレス採用 vs 既存維持
    if (
        ("Lambda" in correct_text or "Fargate" in correct_text)
        and ("EC2" in all_choices_text or "オンプレ" in full)
    ):
        cats.append("serverless_adoption")
    # API Gateway + Lambda (REST API モダナイゼーション)
    if "API Gateway" in full and "Lambda" in full:
        cats.append("api_gateway_lambda")
    return cats


# ===== 判断ポイント HTML テンプレート =====

JUDGE_HEADER = "<br><br><strong>📌 判断ポイント</strong><br>"

# 共通: コンピュート選定マトリクス（一度だけ表示するために短縮版を用意）
COMPUTE_MATRIX_FULL = (
    "<table border='1' cellpadding='4'>"
    "<tr><th>ワークロード特性</th><th>第一候補</th><th>理由</th></tr>"
    "<tr><td>短時間（〜15分）・イベント駆動・断続的負荷</td><td>Lambda</td><td>使用時間課金・自動スケール・運用ゼロ</td></tr>"
    "<tr><td>長時間（15分超）・バッチ・コンテナ化済み</td><td>Fargate (ECS/EKS)</td><td>Lambda 15 分制限を超える。サーバー管理不要</td></tr>"
    "<tr><td>常時稼働・高 CPU/GPU・既存ワークロード</td><td>EC2 (Auto Scaling)</td><td>長時間連続稼働ではコスト効率が逆転、特殊ハードも選べる</td></tr>"
    "<tr><td>HTTP API・コンテナで自動スケール（運用簡素化）</td><td>App Runner / Fargate</td><td>App Runner は HTTPS のみ・スケーリング設定最小</td></tr>"
    "</table>"
)

# Lambda 制限早見表
LAMBDA_LIMITS = (
    "<br><strong>Lambda 制限の落とし穴:</strong><br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>項目</th><th>上限</th><th>回避策</th></tr>"
    "<tr><td>実行時間</td><td>15 分</td><td>Step Functions で分割／Fargate / Batch へ移行</td></tr>"
    "<tr><td>メモリ</td><td>128 MB 〜 10,240 MB</td><td>大きすぎる場合は Fargate（vCPU/メモリの自由度大）</td></tr>"
    "<tr><td>/tmp ストレージ</td><td>標準 512 MB（最大 10 GB まで拡張可）</td><td>大容量ファイルは EFS マウント or S3 ストリーミング</td></tr>"
    "<tr><td>同期ペイロード</td><td>6 MB（リクエスト/レスポンス）</td><td>S3 経由 or 非同期化</td></tr>"
    "<tr><td>非同期ペイロード</td><td>256 KB（イベント）</td><td>S3 にアップロードしてイベントには参照キーのみ渡す</td></tr>"
    "<tr><td>同時実行数</td><td>デフォルト 1,000 / リージョン</td><td>予約済み同時実行で重要関数を保護、引き上げ申請</td></tr>"
    "</table>"
)

# Fargate vs Lambda 判断
FARGATE_LAMBDA_DECISION = (
    "<br><strong>Lambda vs Fargate vs EC2 の判断軸:</strong><br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>条件</th><th>選定</th></tr>"
    "<tr><td>処理時間 ≤ 15 分かつイベント駆動 / 断続実行</td><td><strong>Lambda</strong></td></tr>"
    "<tr><td>処理時間 > 15 分、または常時稼働コンテナ</td><td><strong>Fargate</strong>（サーバー管理不要、Spot 併用可）</td></tr>"
    "<tr><td>GPU / 特殊 AMI / 巨大インスタンス / 既存 AMI 移行</td><td><strong>EC2</strong></td></tr>"
    "<tr><td>1 日 24 時間フル稼働で高負荷</td><td><strong>EC2 (RI/Savings Plans)</strong> がコスト最安になる場合あり</td></tr>"
    "</table>"
    "<br>※ Lambda は <strong>使用時間課金</strong>、Fargate/EC2 は <strong>稼働時間課金</strong>。"
    "1 日数分しか動かないなら Lambda、1 日中動くなら EC2/Fargate が安い。"
)

# Step Functions 判断
STEP_FUNCTIONS_DECISION = (
    "<br><strong>Step Functions の使いどころ:</strong><br>"
    "<ul>"
    "<li><strong>長時間ワークフロー</strong>（Standard: 最大 1 年）→ Lambda 15 分制限を超える処理を分割</li>"
    "<li><strong>状態管理・分岐・並列実行・リトライ</strong>を宣言的に書ける（コードで実装するより安全）</li>"
    "<li><strong>サービス統合</strong>（Lambda / ECS / SNS / SQS / DynamoDB など）でグルー Lambda が不要</li>"
    "<li><strong>Standard vs Express の選択:</strong>"
    "<table border='1' cellpadding='4'>"
    "<tr><th></th><th>Standard</th><th>Express</th></tr>"
    "<tr><td>最大実行時間</td><td>1 年</td><td>5 分</td></tr>"
    "<tr><td>課金</td><td>状態遷移ごと</td><td>実行回数 + 実行時間</td></tr>"
    "<tr><td>用途</td><td>ヒューマン承認・長時間バッチ・監査要件</td><td>高頻度の短時間ストリーム処理（IoT、API バック）</td></tr>"
    "<tr><td>実行履歴</td><td>個別に確認可</td><td>CloudWatch Logs に集約</td></tr>"
    "</table></li>"
    "</ul>"
)

# EventBridge vs SNS
EVENTBRIDGE_VS_SNS = (
    "<br><strong>EventBridge vs SNS の使い分け:</strong><br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th></th><th>EventBridge</th><th>SNS</th></tr>"
    "<tr><td>配信モデル</td><td>イベントバス（ルーティング）</td><td>Pub/Sub（トピック単位）</td></tr>"
    "<tr><td>フィルタリング</td><td>JSON パターンで属性ベースの<strong>細かいルーティング</strong>可</td><td>メッセージ属性での簡易フィルタのみ</td></tr>"
    "<tr><td>SaaS 連携</td><td>標準で SaaS イベント受信可（Zendesk, Datadog 等）</td><td>不可</td></tr>"
    "<tr><td>ターゲット種類</td><td>20 以上の AWS サービスへ直接配信</td><td>Lambda / SQS / HTTP / Email / SMS</td></tr>"
    "<tr><td>スループット / レイテンシ</td><td>やや高レイテンシ（数百 ms）</td><td>低レイテンシ（数十 ms）、高スループット</td></tr>"
    "<tr><td>典型用途</td><td>イベント駆動の<strong>マイクロサービス連携</strong>、SaaS 連携</td><td>大量の<strong>同一メッセージファンアウト</strong>（Eメール通知）</td></tr>"
    "</table>"
    "<br>※ 「ルールでルーティング」「SaaS イベント」→ EventBridge、「単純なファンアウト」「低レイテンシ」→ SNS。"
)

# SQS FIFO vs Standard
SQS_FIFO = (
    "<br><strong>SQS Standard vs FIFO:</strong><br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th></th><th>Standard</th><th>FIFO</th></tr>"
    "<tr><td>順序保証</td><td>ベストエフォート</td><td>MessageGroupId 単位で<strong>厳密順序保証</strong></td></tr>"
    "<tr><td>重複排除</td><td>少なくとも 1 回（重複あり）</td><td>5 分以内の重複を自動排除（exactly-once）</td></tr>"
    "<tr><td>スループット</td><td>ほぼ無制限</td><td>標準 300 msg/s（高スループット FIFO で 3,000+）</td></tr>"
    "<tr><td>用途</td><td>高スループット・順序不問</td><td>金融取引・在庫更新・順序が重要な処理</td></tr>"
    "</table>"
)

# Aurora Serverless v1 vs v2
AURORA_SERVERLESS = (
    "<br><strong>Aurora Serverless v1 vs v2:</strong><br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th></th><th>v1</th><th>v2</th></tr>"
    "<tr><td>スケーリング粒度</td><td>ACU 倍々（粗い）</td><td>0.5 ACU 単位の<strong>細粒度</strong></td></tr>"
    "<tr><td>スケーリング速度</td><td>分単位（コールドスタート遅い）</td><td>秒単位（即時）</td></tr>"
    "<tr><td>Aurora 機能</td><td>一部の機能が非対応</td><td>ほぼ全機能対応（Global DB / RDS Proxy / IAM 認証等）</td></tr>"
    "<tr><td>停止</td><td>0 ACU まで縮退可（再起動コールドスタートあり）</td><td>最小 0.5 ACU（v2.11 以降は 0 ACU 自動一時停止可）</td></tr>"
    "<tr><td>用途</td><td>断続利用・開発環境 (現在は v2 推奨)</td><td>本番ワークロード全般</td></tr>"
    "</table>"
    "<br>※ 新規構築は基本 <strong>v2</strong>。v1 は段階的に廃止方向。"
)

# モノリス分割 (Strangler Fig)
MONOLITH_SPLIT = (
    "<br><strong>モノリス → マイクロサービス段階的移行（Strangler Fig パターン）:</strong><br>"
    "<ol>"
    "<li><strong>API Gateway / ALB をフロントに配置</strong> し、トラフィックを既存モノリスにルーティング</li>"
    "<li>移行する機能を選び、新規マイクロサービス（Lambda / Fargate）として切り出す</li>"
    "<li>API Gateway / ALB のルーティングルールで、その機能だけ新サービスへ徐々に振り向ける</li>"
    "<li>カナリア / 重み付けで段階的に 100% 切り替え、旧コードを削除</li>"
    "<li>残りの機能を順次同様に切り出し、最終的にモノリスを除去</li>"
    "</ol>"
    "<strong>判断軸:</strong> "
    "ビッグバン書き換えはリスク大。<strong>API Gateway による前段ルーティング + 機能単位の切り出し</strong>が定石。"
    "データベースは共有のまま開始し、最後に分離するのが現実的。"
)

# サーバーレス採用判断
SERVERLESS_ADOPTION = (
    "<br><strong>「サーバーレス化すべきか」の判断フロー:</strong><br>"
    "<ol>"
    "<li><strong>負荷パターン</strong>: 断続的・予測不能 → サーバーレス有利。常時高負荷 → EC2/Fargate でも可</li>"
    "<li><strong>処理時間</strong>: ≤15 分 → Lambda 可。> 15 分 → Fargate / Batch / Step Functions で分割</li>"
    "<li><strong>状態</strong>: ステートレス → Lambda 適合。ステートフル長時間セッション → コンテナ / EC2</li>"
    "<li><strong>レイテンシ要件</strong>: 厳密な低レイテンシ（< 数 ms）→ プロビジョンド同時実行 or EC2/Fargate</li>"
    "<li><strong>移行コスト</strong>: 既存コンテナ済 → Fargate が最短。コード書き換え許容 → Lambda</li>"
    "</ol>"
    "<strong>運用負荷比較（低 → 高）:</strong> Lambda < App Runner < Fargate < ECS on EC2 < EC2 自前管理"
)

# API Gateway + Lambda
API_GATEWAY_LAMBDA = (
    "<br><strong>API Gateway + Lambda の典型構成:</strong><br>"
    "<ul>"
    "<li>REST API（フル機能）: 使用量プラン・APIキー・キャッシュが必要なケース</li>"
    "<li>HTTP API（軽量）: コスト 1/3、レイテンシ低、シンプルな OAuth/JWT 認証で十分なケース</li>"
    "<li>WebSocket API: 双方向リアルタイム通信（チャット、通知）</li>"
    "<li>レスポンス &gt; 6 MB or 30 秒超: API Gateway 制限に注意（同期 6 MB / タイムアウト 29 秒）→ "
    "S3 Presigned URL / 非同期化 / Step Functions で回避</li>"
    "</ul>"
)

# 共通フッター（その他カテゴリ向け）
GENERIC_SERVERLESS = (
    "<br><strong>サーバーレス・モダナイゼーション 一般原則:</strong><br>"
    "<ul>"
    "<li><strong>イベント駆動・断続負荷</strong> → Lambda + SQS / EventBridge</li>"
    "<li><strong>長時間・コンテナ既存</strong> → Fargate（ECS/EKS）</li>"
    "<li><strong>常時高負荷・特殊要件</strong> → EC2（Savings Plans でコスト最適化）</li>"
    "<li><strong>運用負荷</strong>: Lambda < Fargate < EC2。サーバー管理コスト含めて TCO 評価</li>"
    "<li><strong>データストア</strong>: アクセスパターン明確 → DynamoDB、SQL 必須 → Aurora Serverless v2</li>"
    "</ul>"
)


def build_judge_section(cats):
    """カテゴリ集合から判断ポイント HTML を組み立てる。重複排除のため最大 2 セクション。"""
    sections = []
    seen = set()

    # 優先順位（ユーザーの苦手ポイント優先）
    priority = [
        "lambda_limit",
        "monolith_split",
        "fargate_choice",
        "step_functions",
        "serverless_adoption",
        "eventbridge_vs_sns",
        "sqs_fifo",
        "aurora_serverless",
        "api_gateway_lambda",
    ]

    cat_to_html = {
        "lambda_limit": LAMBDA_LIMITS + FARGATE_LAMBDA_DECISION,
        "monolith_split": MONOLITH_SPLIT,
        "fargate_choice": FARGATE_LAMBDA_DECISION,
        "step_functions": STEP_FUNCTIONS_DECISION,
        "serverless_adoption": SERVERLESS_ADOPTION,
        "eventbridge_vs_sns": EVENTBRIDGE_VS_SNS,
        "sqs_fifo": SQS_FIFO,
        "aurora_serverless": AURORA_SERVERLESS,
        "api_gateway_lambda": API_GATEWAY_LAMBDA,
    }

    for cat in priority:
        if cat in cats and cat not in seen:
            sections.append(cat_to_html[cat])
            seen.add(cat)
            if len(sections) >= 2:
                break

    if not sections:
        sections.append(GENERIC_SERVERLESS)

    return JUDGE_HEADER + "".join(sections)


# ===== 既存 detail の品質チェック（軽微な誤りを修正） =====

def fix_detail_errors(detail):
    """既存 detail の明らかな誤りを修正。修正したら True を返す。"""
    fixed = detail
    changed = False
    # Lambda 5分 / 10分 → 15分（明らかな誤記）
    new = re.sub(
        r"(Lambda[^。]{0,40}?最大\s*)(5|10)\s*分",
        r"\g<1>15分",
        fixed,
    )
    if new != fixed:
        changed = True
        fixed = new
    # Lambda メモリ 3008 MB / 3 GB（古い上限）→ 10,240 MB / 10 GB
    new = re.sub(
        r"(Lambda[^。]{0,40}?メモリ[^。]{0,20}?)(3008\s*MB|3\s*GB)(?!.*10\s*GB)",
        r"\g<1>10,240 MB（10 GB）",
        fixed,
    )
    if new != fixed:
        changed = True
        fixed = new
    return fixed, changed


# ===== メイン処理 =====

def main():
    # 1. 対象抽出（読み込み 1）
    with QUESTIONS_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    targets = []
    for q in data:
        if not is_target(q):
            continue
        cats = classify(q)
        targets.append((q["id"], cats))

    print(f"対象問題数: {len(targets)}")

    # カテゴリ別集計
    from collections import Counter
    cat_counter = Counter()
    for _, cats in targets:
        if cats:
            for c in cats:
                cat_counter[c] += 1
        else:
            cat_counter["(generic)"] += 1
    print("カテゴリ別:")
    for k, v in cat_counter.most_common():
        print(f"  {k}: {v}")

    # 2. 書き込み直前にファイル再読み込み
    with QUESTIONS_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    target_map = dict(targets)  # id -> cats

    fixed_count = 0
    appended_count = 0
    skipped_already = 0

    for q in data:
        qid = q["id"]
        if qid not in target_map:
            continue
        explanation = q.get("explanation", {})
        detail = explanation.get("detail", "")

        # 既に判断ポイントがあればスキップ
        if "📌 判断ポイント" in detail:
            skipped_already += 1
            continue

        # 品質チェック修正
        new_detail, changed = fix_detail_errors(detail)
        if changed:
            fixed_count += 1

        # 加筆
        cats = target_map[qid]
        judge_html = build_judge_section(cats)
        new_detail = new_detail + judge_html
        appended_count += 1

        explanation["detail"] = new_detail
        q["explanation"] = explanation

    # 3. 保存
    with QUESTIONS_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # JSON valid 確認
    with QUESTIONS_PATH.open("r", encoding="utf-8") as f:
        json.load(f)

    print(f"\n=== 完了 ===")
    print(f"対象問題数: {len(targets)}")
    print(f"加筆した問題数: {appended_count}")
    print(f"修正した問題数: {fixed_count}")
    print(f"スキップ（既に判断ポイントあり）: {skipped_already}")


if __name__ == "__main__":
    main()
