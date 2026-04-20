#!/usr/bin/env python3
"""
AWS SAP-C02 問題集 — 「API設計のサービス選定」テーマの解説を品質チェック + 加筆。

対象: tags に api-design を含む、または問題文/選択肢に API Gateway/AppSync/Cognito/
Lambda Authorizer/WebSocket/HTTP API/REST API/Usage Plan などのキーワードを含む問題。

加筆: 「📌 判断ポイント」を末尾に追加（API サービス選定が判断軸となる問題のみ）。
"""

import json
from pathlib import Path

QUESTIONS_PATH = Path("/Users/aki/aws-sap/docs/data/questions.json")


# ===== 判断ポイントテンプレート =====
# それぞれ問題の文脈に合わせて選択する。

TIP_REST_VS_HTTP = (
    "<br><br>📌 判断ポイント — REST API vs HTTP API<br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>要件</th><th>選ぶべき API Gateway タイプ</th></tr>"
    "<tr><td>API キー / Usage Plan / リクエスト検証 / X-Ray 完全対応 / WAF 連携 / プライベートエンドポイント / AWS サービス直接統合（DynamoDB 等）</td><td><b>REST API</b></td></tr>"
    "<tr><td>JWT 認証 / 低コスト・低レイテンシ / シンプルな Lambda・HTTP プロキシ統合 / OIDC / CORS 自動</td><td><b>HTTP API</b>（最大 71% 安価・最大 60% 低レイテンシ）</td></tr>"
    "<tr><td>双方向通信 / リアルタイムプッシュ / チャット・通知</td><td><b>WebSocket API</b></td></tr>"
    "</table>"
    "<br>判断のコツ: <b>「API キー＋Usage Plan」「DynamoDB/Kinesis などへの直接統合（Lambda 不要）」「リソースポリシーでプライベート公開」のいずれかが要件にあれば REST API 一択</b>。要件が単純な HTTPS 公開のみなら HTTP API がコスト最適。"
)

TIP_APIGW_VS_APPSYNC = (
    "<br><br>📌 判断ポイント — API Gateway vs AppSync<br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>要件</th><th>選ぶべきサービス</th></tr>"
    "<tr><td>REST/CRUD・外部公開・スロットリング・API キー課金・OpenAPI 仕様</td><td><b>API Gateway</b>（REST/HTTP）</td></tr>"
    "<tr><td>双方向のサーバープッシュ・チャット・株価ティッカー（WebSocket プロトコルが必須）</td><td><b>API Gateway WebSocket</b></td></tr>"
    "<tr><td>GraphQL・複数データソース（DynamoDB/Lambda/RDS/OpenSearch）を 1 クエリで集約・モバイルのオフライン同期・リアルタイム購読（Subscriptions）</td><td><b>AWS AppSync</b></td></tr>"
    "</table>"
    "<br>判断のコツ: <b>モバイル/SPA で「複数のテーブルや関数を 1 リクエストで叩きたい」「オフライン中の更新を後でマージしたい」「クライアントが必要なフィールドだけ取りたい」</b>のいずれかがあれば AppSync。それ以外の素直な HTTP API 公開は API Gateway。"
)

TIP_COGNITO_AUTH = (
    "<br><br>📌 判断ポイント — API の認証/認可 方式選定<br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>要件</th><th>選ぶべき方式</th></tr>"
    "<tr><td>エンドユーザー（モバイル/Web）の登録・ログイン・SNS／メール認証・MFA・JWT 発行</td><td><b>Cognito User Pool</b>（API Gateway/AppSync と直接統合）</td></tr>"
    "<tr><td>認証済みユーザーに一時的な AWS 認証情報（IAM ロール）を発行して S3/DynamoDB に直接アクセスさせたい</td><td><b>Cognito Identity Pool</b></td></tr>"
    "<tr><td>呼び出し元が AWS の IAM ユーザー/ロールに限定（社内システム間連携・SigV4 署名）</td><td><b>API Gateway IAM 認可</b>（AWS_IAM）</td></tr>"
    "<tr><td>独自トークン（OAuth/サードパーティ JWT/API キー）の検証・カスタムロジック</td><td><b>Lambda Authorizer</b>（TOKEN/REQUEST 型・キャッシュ可）</td></tr>"
    "<tr><td>パートナー識別と従量課金/レート制限</td><td><b>API キー＋Usage Plan</b>（REST API のみ）</td></tr>"
    "</table>"
    "<br>判断のコツ: <b>「ユーザー登録/ソーシャルログインが要件 → Cognito User Pool」「AWS 内部間 → IAM 認可」「独自トークン検証 → Lambda Authorizer」</b>。Lambda Authorizer は <b>結果をキャッシュ（既定 TTL 300 秒）</b>できるので Lambda コストも抑えられる。"
)

TIP_THROTTLING = (
    "<br><br>📌 判断ポイント — API Gateway スロットリング/Usage Plan<br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>レイヤー</th><th>用途</th></tr>"
    "<tr><td>アカウントレベル（リージョンごと既定 10,000 req/s, 5,000 burst）</td><td>AWS 全体の保護上限。サポート申請で引き上げ可</td></tr>"
    "<tr><td>ステージ/メソッドレベル</td><td>API ステージ単位の上限。全クライアント共通</td></tr>"
    "<tr><td><b>Usage Plan + API キー</b></td><td><b>クライアント（API キー）ごと</b>に Rate/Burst/Quota（日次・月次）を設定。テナント別課金や暴走クライアントの隔離に最適</td></tr>"
    "</table>"
    "<br>判断のコツ: <b>「特定パートナーの暴走を他クライアントから隔離したい」「テナント別の従量課金」なら Usage Plan＋API キーが正解</b>。Usage Plan は <b>REST API のみ対応</b>（HTTP API は未対応）。送信元 IP 制限なら WAF。"
)

TIP_WEBSOCKET_VS_APPSYNC_SUB = (
    "<br><br>📌 判断ポイント — リアルタイム配信のサービス選定<br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>要件</th><th>選ぶべきサービス</th></tr>"
    "<tr><td>クライアントが GraphQL を使える / モバイルでオフライン対応 / DynamoDB Streams 等を直接トリガーにしたい</td><td><b>AWS AppSync Subscriptions</b>（MQTT over WebSocket、自動スケール、認可も統合）</td></tr>"
    "<tr><td>純粋な WebSocket プロトコルで双方向通信したい / GraphQL は不要 / カスタムバイナリやシンプルな JSON メッセージ</td><td><b>API Gateway WebSocket API</b>（$connect/$disconnect/$default ルート）</td></tr>"
    "<tr><td>サーバー → 多数クライアントへの一方向プッシュ（数十〜数千万）</td><td><b>IoT Core (MQTT)</b> / SNS モバイルプッシュ</td></tr>"
    "</table>"
    "<br>判断のコツ: <b>「モバイルアプリ＋オフライン＋複数データソース」なら AppSync。「シンプルな双方向 WebSocket だけ」なら API Gateway WebSocket。</b> AppSync は購読ロジックを GraphQL スキーマで宣言するだけで済む。"
)

TIP_APPSYNC_OFFLINE = (
    "<br><br>📌 判断ポイント — モバイル/オフライン同期 + 複数データソース統合<br>"
    "<b>AppSync</b> が決定打になるサイン:<br>"
    "・モバイル/Web SPA から <b>複数の DynamoDB テーブル/Lambda/RDS/OpenSearch</b> を 1 クエリで取得したい<br>"
    "・<b>オフライン中の更新</b>をローカルに溜め、再接続時に自動マージ（Amplify DataStore + AppSync）<br>"
    "・<b>リアルタイム購読</b>（Subscriptions）でデータ変更をクライアントへ自動プッシュ<br>"
    "・クライアントが必要なフィールドだけ取得して <b>レスポンス転送量を削減</b>（GraphQL の特長）<br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>シナリオ</th><th>正解パターン</th></tr>"
    "<tr><td>REST/CRUD・サーバー間連携</td><td>API Gateway + Lambda</td></tr>"
    "<tr><td>モバイルアプリ・複数ソース統合・リアルタイム・オフライン</td><td><b>AppSync</b> + DynamoDB/Lambda リゾルバー + Cognito</td></tr>"
    "<tr><td>シンプルな双方向プロトコル</td><td>API Gateway WebSocket</td></tr>"
    "</table>"
)

TIP_GENERAL_API_MATRIX = (
    "<br><br>📌 判断ポイント — API 公開サービスの早見表<br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>要件キーワード</th><th>選ぶべきサービス/タイプ</th></tr>"
    "<tr><td>REST/CRUD・外部公開・API キー・Usage Plan・WAF・X-Ray</td><td><b>API Gateway REST API</b></td></tr>"
    "<tr><td>シンプルな HTTPS・JWT・低コスト/低レイテンシ・OIDC</td><td><b>API Gateway HTTP API</b>（REST より最大 71% 安）</td></tr>"
    "<tr><td>双方向（チャット・通知・株価ティッカー）</td><td><b>API Gateway WebSocket API</b></td></tr>"
    "<tr><td>GraphQL・複数データソース統合・モバイルのオフライン同期・リアルタイム購読</td><td><b>AWS AppSync</b></td></tr>"
    "<tr><td>VPC 内部からのみ呼び出す（インターネット非公開）</td><td>API Gateway <b>プライベートエンドポイント</b>＋インターフェース VPC エンドポイント</td></tr>"
    "<tr><td>グローバル低レイテンシ</td><td>API Gateway <b>エッジ最適化</b> または CloudFront＋REST API</td></tr>"
    "</table>"
)


# ===== 問題ごとに追加する 判断ポイントを指定 =====
# キー: 問題 id / 値: 上記テンプレートの組み合わせ（複数追加可）
# None または未登録 → 加筆なし（レビューのみ）
TIPS_BY_ID = {
    # ---- SAP 問題（api-design タグ含む & 真に API 設計選定）----
    "SAP-16": TIP_THROTTLING,                                # API Gateway 過剰呼び出し
    "SAP-77": TIP_COGNITO_AUTH + TIP_GENERAL_API_MATRIX,     # Lambda+APIGW+Cognito
    "SAP-91": TIP_GENERAL_API_MATRIX,                        # マルチリージョン APIGW
    "SAP-169": TIP_THROTTLING,                               # API キー保護 / WAF
    "SAP-176": TIP_APPSYNC_OFFLINE,                          # リアルタイム IoT/SaaS（Kinesis 系だが補助）
    "SAP-192": TIP_COGNITO_AUTH,                             # Lambda 認証 → Cognito 提案
    "SAP-193": TIP_COGNITO_AUTH,                             # AD 認証 → Cognito フェデレーション
    "SAP-195": TIP_THROTTLING,                               # Usage Plan
    "SAP-224": TIP_COGNITO_AUTH,                             # 大容量アップロード（S3 直接）
    "SAP-250": TIP_GENERAL_API_MATRIX,                       # マルチリージョン APIGW
    "SAP-260": TIP_GENERAL_API_MATRIX,                       # APIGW Lambda CodeDeploy（API 設計タグ）
    "SAP-271": TIP_COGNITO_AUTH,                             # IAM 認可 + X-Ray
    "SAP-281": TIP_REST_VS_HTTP + TIP_GENERAL_API_MATRIX,    # HTTP API + Lambda or REST + DynamoDB 統合
    "SAP-298": TIP_GENERAL_API_MATRIX,                       # APIGW Lambda DynamoDB SAM（API 設計タグ）

    # ---- UDEMY 問題 ----
    "UDEMY-025": TIP_THROTTLING + TIP_COGNITO_AUTH,          # WAF + Usage Plan + API キー
    "UDEMY-032": TIP_COGNITO_AUTH,                           # Cognito + Amplify
    "UDEMY-045": TIP_APIGW_VS_APPSYNC,                       # AppSync 注文管理
    "UDEMY-059": TIP_WEBSOCKET_VS_APPSYNC_SUB + TIP_APPSYNC_OFFLINE,  # AppSync WebSocket
    "UDEMY-070": TIP_GENERAL_API_MATRIX,                     # マルチリージョン APIGW
    "UDEMY-075": TIP_THROTTLING,                             # Usage Plan + API キー
    "UDEMY-089": TIP_GENERAL_API_MATRIX,                     # マルチリージョン APIGW
    "UDEMY-091": TIP_GENERAL_API_MATRIX,                     # マルチリージョン APIGW
    "UDEMY-104": TIP_APIGW_VS_APPSYNC,                       # APIGW vs AppSync
    "UDEMY-117": TIP_COGNITO_AUTH,                           # IAM 認可 + X-Ray
    "UDEMY-140": TIP_GENERAL_API_MATRIX,                     # プライベート API
    "UDEMY-155": TIP_REST_VS_HTTP,                           # CloudFront + Lambda@Edge
    "UDEMY-172": TIP_THROTTLING,                             # Usage Plan
    "UDEMY-176": None,                                       # Secrets Manager 中心。API 設計ではない
    "UDEMY-177": TIP_REST_VS_HTTP + TIP_GENERAL_API_MATRIX,  # REST直接統合 vs HTTP+Lambda
    "UDEMY-183": TIP_GENERAL_API_MATRIX,                     # EC2 → APIGW + Lambda
    "UDEMY-195": TIP_REST_VS_HTTP,                           # HTTP API + Lambda（Webhook）
    "UDEMY-256": TIP_GENERAL_API_MATRIX,                     # マルチリージョン APIGW
    "UDEMY-269": TIP_THROTTLING,                             # APIGW スロットル制限
    "UDEMY-291": TIP_GENERAL_API_MATRIX,                     # APIGW プライベート
    "UDEMY-329": TIP_REST_VS_HTTP,                           # HTTP API + SQS 統合
    "UDEMY-345": TIP_GENERAL_API_MATRIX,                     # APIGW + Lambda 倉庫アプリ
    "UDEMY-367": TIP_GENERAL_API_MATRIX,                     # APIGW プライベート
}


# ===== 技術的に誤った記述の修正（detail 内文字列置換）=====
# キー: 問題 id / 値: [(old_str, new_str), ...]
FIXES_BY_ID = {
    # SAP-281: HTTP API は DynamoDB のダイレクト統合を サポートしていない
    # （DynamoDB との AWS サービス統合は REST API のみ）
    "SAP-281": [
        (
            "<tr><td>C</td><td>HTTP APIのAWSサービス統合はDynamoDBダイレクト接続が正しいが、機能的にBのREST APIと重複</td></tr>",
            "<tr><td>C</td><td>不正解。<b>HTTP API は DynamoDB へのダイレクト AWS サービス統合をサポートしない</b>（HTTP API の AWS サービス統合は SQS/Step Functions/Kinesis/EventBridge/AppConfig など限定。DynamoDB 直接統合は REST API のみ）</td></tr>",
        ),
    ],
}


def main():
    # 直前再読み込み（指示通り）
    with QUESTIONS_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    appended = 0
    appended_ids = []
    skipped = 0
    fixed_ids = []
    target_total = len(TIPS_BY_ID)

    # 候補問題一覧（タグまたはキーワードマッチ）
    keyword_candidates = []
    strict_kw = [
        "API Gateway", "AppSync", "GraphQL", "Lambda Authorizer", "Lambdaオーソライザー",
        "Lambda オーソライザー", "IAM 認可", "IAM認可", "WebSocket", "REST API",
        "HTTP API", "WebSocket API", "Usage Plan", "使用量プラン", "API Key", "APIキー",
    ]

    def get_text(item):
        text = item.get("question", "") or ""
        for c in item.get("choices", []) or []:
            if isinstance(c, dict):
                text += " " + (c.get("text", "") or "")
            elif isinstance(c, str):
                text += " " + c
        return text

    for item in data:
        has_tag = isinstance(item.get("tags"), list) and "api-design" in item["tags"]
        text = get_text(item)
        matched = any(kw in text for kw in strict_kw)
        # Cognito alone needs API context
        if not matched:
            if any(kw in text for kw in ["Cognito", "ユーザープール", "Identity Pool"]):
                if "API Gateway" in text or "AppSync" in text:
                    matched = True
        if has_tag or matched:
            keyword_candidates.append(item.get("id"))

    # 修正処理（技術的誤りの訂正）
    for item in data:
        qid = item.get("id")
        if qid not in FIXES_BY_ID:
            continue
        explanation = item.get("explanation") or {}
        detail = explanation.get("detail", "") or ""
        original = detail
        for old_s, new_s in FIXES_BY_ID[qid]:
            if old_s in detail:
                detail = detail.replace(old_s, new_s)
        if detail != original:
            explanation["detail"] = detail
            item["explanation"] = explanation
            fixed_ids.append(qid)

    # 加筆処理
    for item in data:
        qid = item.get("id")
        if qid not in TIPS_BY_ID:
            continue
        tip = TIPS_BY_ID[qid]
        if tip is None:
            skipped += 1
            continue
        explanation = item.get("explanation") or {}
        detail = explanation.get("detail", "") or ""

        # 既に同じトピックの 判断ポイントがある場合のみ skip
        # tip テンプレート固有の見出し（"判断ポイント — XXX"）の "— XXX" 部分で重複検出
        topic_marker = None
        if "判断ポイント — REST API vs HTTP API" in tip:
            topic_marker = "判断ポイント — REST API vs HTTP API"
        elif "判断ポイント — API Gateway vs AppSync" in tip:
            topic_marker = "判断ポイント — API Gateway vs AppSync"
        elif "判断ポイント — API の認証/認可" in tip:
            topic_marker = "判断ポイント — API の認証/認可"
        elif "判断ポイント — API Gateway スロットリング" in tip:
            topic_marker = "判断ポイント — API Gateway スロットリング"
        elif "判断ポイント — リアルタイム配信" in tip:
            topic_marker = "判断ポイント — リアルタイム配信"
        elif "判断ポイント — モバイル/オフライン" in tip:
            topic_marker = "判断ポイント — モバイル/オフライン"
        elif "判断ポイント — API 公開サービスの早見表" in tip:
            topic_marker = "判断ポイント — API 公開サービスの早見表"

        if topic_marker and topic_marker in detail:
            skipped += 1
            continue

        new_detail = detail + tip
        explanation["detail"] = new_detail
        item["explanation"] = explanation
        appended += 1
        appended_ids.append(qid)

    # 書き込み
    with QUESTIONS_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"対象候補（キーワード/タグ一致）: {len(keyword_candidates)} 問")
    print(f"  うち api-design タグ付き: {sum(1 for it in data if isinstance(it.get('tags'), list) and 'api-design' in it['tags'])} 問")
    print(f"加筆対象として登録: {target_total} 問")
    print(f"加筆実行: {appended} 問")
    print(f"スキップ（既加筆 or 加筆対象外指定）: {skipped} 問")
    print(f"技術的誤りを修正: {len(fixed_ids)} 問")
    print()
    print("加筆した問題 ID:")
    for qid in appended_ids:
        print(f"  - {qid}")
    print()
    print("修正した問題 ID:")
    for qid in fixed_ids:
        print(f"  - {qid}")


if __name__ == "__main__":
    main()
