#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
コンテナ起動タイプ・基盤選定テーマの解説を品質チェック＋加筆するスクリプト。

対象: questions.json 内のコンテナ関連70問
- ECS / EKS / Fargate / EC2起動タイプの選定
- IRSA / タスクロール / インスタンスロール
- Capacity Provider / Spot / Service Auto Scaling
- ECR (PrivateLink, ライフサイクル, クロスアカウント)
- awsvpc ネットワークモード

書き込み直前にファイルを再読み込みし、対象問題のみ差し替えて保存。
"""

import json
import os
import sys

JSON_PATH = '/Users/aki/aws-sap/docs/data/questions.json'

# ============================================================
# 共通の判断ポイント部品（4象限マトリクス・キーワードマッピング）
# ============================================================

QUADRANT_TABLE = (
    "<table border='1' cellpadding='4'>"
    "<tr><th>象限</th><th>運用負荷</th><th>柔軟性/コスト</th><th>典型ユースケース</th></tr>"
    "<tr><td><b>ECS × Fargate</b></td><td>最小（サーバー管理ゼロ）</td><td>柔軟性低・単価高</td>"
    "<td>AWS固有・少人数チーム・短期/バースト・タスク単発実行（RunTask）</td></tr>"
    "<tr><td><b>ECS × EC2</b></td><td>中（EC2/AMI管理あり）</td><td>柔軟性中・コスト最適化可（Spot/RI）</td>"
    "<td>GPU/特殊AMI/高密度配置・長時間稼働・Spot活用したい</td></tr>"
    "<tr><td><b>EKS × Fargate</b></td><td>低〜中（K8s制御プレーンはマネージド・データプレーンはサーバーレス）</td>"
    "<td>K8s資産流用可・Fargate制約あり（DaemonSet/PV制限）</td>"
    "<td>既存K8sマニフェスト・Helm資産あり＋ノード管理を避けたい</td></tr>"
    "<tr><td><b>EKS × EC2</b></td><td>高（ノードグループ・OS/CNI管理）</td>"
    "<td>柔軟性最大・GPU/Spot/Karpenter全部使える</td>"
    "<td>マルチクラウド/オンプレ移行・K8sエコシステム最大活用・kubectl/Helm/Operator必須</td></tr>"
    "</table>"
)

KEYWORD_MAP = (
    "<b>要件キーワード → 推奨構成マッピング:</b><br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>キーワード</th><th>推奨</th><th>理由</th></tr>"
    "<tr><td>「サーバー管理ゼロ」「インフラ運用最小」「少人数チーム」</td><td><b>ECS × Fargate</b></td>"
    "<td>EC2/AMI/パッチ全部AWS任せ。ECSはEKSより学習コスト低い</td></tr>"
    "<tr><td>「既存Kubernetes資産」「kubectl/Helm/Operator」「マルチクラウド」「ポータビリティ」</td>"
    "<td><b>EKS</b>（×Fargate or EC2）</td><td>K8s API互換が必須要件のサイン</td></tr>"
    "<tr><td>「GPU」「特殊インスタンスタイプ」「Spotで大幅コスト削減」「Bottlerocket等カスタムAMI」</td>"
    "<td><b>EC2起動タイプ</b>（ECS or EKS）</td><td>FargateはGPU/Spot不可、AMI選択不可</td></tr>"
    "<tr><td>「単発バッチ」「定期実行」「イベント駆動」「Lambdaの15分/メモリ制限超え」</td>"
    "<td><b>ECS × Fargate</b>（RunTask）または <b>AWS Batch</b></td>"
    "<td>常駐サービス不要。Batchはジョブキュー/リトライ/優先度が標準装備</td></tr>"
    "<tr><td>「awsvpcネットワークモード」「タスク単位ENI/SG」「PCI DSS最小権限」</td>"
    "<td><b>ECS awsvpcモード + タスクロール</b></td>"
    "<td>FargateはawsvpcのみでbridgeやhostNG。タスク単位でIAMロール/SG付与可能</td></tr>"
    "</table>"
)

IAM_ROLE_TIP = (
    "<b>IAMロールの使い分け（要暗記）:</b><br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>種類</th><th>付与対象</th><th>用途</th></tr>"
    "<tr><td><b>ECSタスクロール</b>（taskRoleArn）</td><td>タスク内コンテナのアプリ</td>"
    "<td>アプリがS3/DynamoDB等を呼ぶ権限。最小権限はここで設計</td></tr>"
    "<tr><td><b>ECSタスク実行ロール</b>（executionRoleArn）</td><td>ECSエージェント/Fargate基盤</td>"
    "<td>ECRからイメージpull、Secrets Manager/SSMから秘匿値取得、CloudWatch Logs書き込み</td></tr>"
    "<tr><td><b>EC2インスタンスロール</b></td><td>ECS on EC2のホストEC2</td>"
    "<td>ホスト全体の権限（ECSエージェント用）。タスクが共有してしまうのでPCI/最小権限要件には不適</td></tr>"
    "<tr><td><b>IRSA</b>（IAM Roles for Service Accounts）</td><td>EKSのKubernetes ServiceAccount</td>"
    "<td>Pod単位でIAMロール紐付け。OIDCプロバイダ経由でSTS AssumeRoleWithWebIdentity。EKSにおける「タスクロール相当」</td></tr>"
    "</table>"
)

PITFALL_TIP = (
    "<b>よくある引っ掛け:</b><br>"
    "・<b>Fargateはbridge/hostネットワークモード不可</b>（awsvpcのみ）→「bridgeに変更」は誤答<br>"
    "・<b>Fargateはdaemon種別タスク・GPU・SpotはECS Fargate Spotとして別概念</b>（純粋Spot AMI不可）<br>"
    "・<b>Fargateの一時ストレージは20GB（追加最大200GB）</b>。永続データは EFS マウント必須<br>"
    "・<b>EC2インスタンスロールにDynamoDB権限を付ける</b>と同じホスト上の全タスクが共有→最小権限違反<br>"
    "・<b>EKSでPodにIAM</b>を付けたい時はIRSA（OIDC紐付け）。EC2ノードロール流用は最小権限違反<br>"
    "・<b>Fargateタスクのプライベートサブネット配置</b>でECRイメージpullするには <b>ECR API/DKR + S3 + Logs</b>のVPCエンドポイント必須（NAT GW不要だが3種以上必要）"
)

# 4象限マトリクス＋キーワードマッピング＋IAMロール＋引っ掛け（フル版）
FULL_TIP = (
    "<br><br>"
    "<b>📌 判断ポイント — ECS/EKS × Fargate/EC2 の選定</b><br><br>"
    "<b>4象限マトリクス:</b><br>"
    + QUADRANT_TABLE + "<br>"
    + KEYWORD_MAP + "<br>"
    + IAM_ROLE_TIP + "<br>"
    + PITFALL_TIP
)

# 軽量版（オーケストレータ選定がメインでない問題用）
LITE_TIP_QUADRANT = (
    "<br><br>"
    "<b>📌 判断ポイント — コンテナ基盤の選択</b><br>"
    + QUADRANT_TABLE
    + "<br><b>覚え方:</b> 「ECS/EKS」軸はAPI互換性（AWS独自 vs K8s）で決まり、"
    "「Fargate/EC2」軸は運用負荷とコスト/柔軟性のトレードオフ。"
    "<b>「サーバー管理を最小化」と書いてあれば原則 Fargate</b>、"
    "<b>「既存Kubernetes資産・kubectl/Helm」「マルチクラウド」と書いてあれば EKS</b> を選ぶ。"
)

LITE_TIP_FARGATE_VS_LAMBDA = (
    "<br><br>"
    "<b>📌 判断ポイント — Fargate vs Lambda の境目</b><br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>判断軸</th><th>Lambda</th><th>Fargate（タスク）</th></tr>"
    "<tr><td>最大実行時間</td><td><b>15分</b>（ハードリミット）</td><td>制限なし</td></tr>"
    "<tr><td>メモリ</td><td>最大10,240MB</td><td>最大120GB（vCPU 16）</td></tr>"
    "<tr><td>一時ストレージ</td><td>512MB〜10GB（/tmp）</td><td>20GB（追加で最大200GB）</td></tr>"
    "<tr><td>起動オーバーヘッド</td><td>ms〜数秒（コールドスタート）</td><td>数十秒〜分</td></tr>"
    "<tr><td>課金粒度</td><td>1ms単位</td><td>秒単位（最小1分）</td></tr>"
    "<tr><td>コンテナイメージ</td><td>OK（最大10GB）</td><td>OK（無制限・ECR）</td></tr>"
    "</table>"
    "<b>使い分け:</b> 「<b>15分超え</b>」「<b>大容量メモリ</b>」「<b>既存コンテナバイナリそのまま</b>」"
    "なら Fargate。短時間イベント駆動なら Lambda。"
)

LITE_TIP_IRSA = (
    "<br><br>"
    "<b>📌 判断ポイント — EKSのIAM権限付与</b><br>"
    + IAM_ROLE_TIP +
    "<b>EKSでPodがS3/DynamoDB等にアクセスする時:</b> "
    "<b>IRSA（IAM Roles for Service Accounts）</b>を使い ServiceAccount にアノテーション "
    "<code>eks.amazonaws.com/role-arn</code> を付ける。"
    "EC2ノードのインスタンスロールに権限を付けるとノード上の全Podが共有してしまうため、"
    "PCI DSS等の最小権限要件を満たさない。"
)

LITE_TIP_TASKROLE = (
    "<br><br>"
    "<b>📌 判断ポイント — ECSタスクの権限とネットワーク分離</b><br>"
    + IAM_ROLE_TIP +
    "<b>awsvpcネットワークモード:</b> タスクごとにENI（弾性ネットワークインタフェース）が払い出され、"
    "VPCのサブネット内で <b>EC2インスタンスと同等のネットワーク制御</b>（SG・ルートテーブル・NACL）が可能。"
    "Fargateは <b>awsvpcのみ</b>サポート。ECS on EC2では bridge/host/awsvpc から選択可能だが、"
    "PCI DSS等の最小権限/分離要件があるなら awsvpc 一択。"
)

LITE_TIP_ECR_PRIVATELINK = (
    "<br><br>"
    "<b>📌 判断ポイント — プライベートサブネットからECRへアクセスする</b><br>"
    "Fargate/ECSタスクをプライベートサブネット（NAT GW なし）に置く場合、"
    "ECRからイメージをpullするには <b>3種類以上のVPCエンドポイント</b>が必要：<br>"
    "・<b>com.amazonaws.&lt;region&gt;.ecr.api</b>（インターフェース型）— ECR制御API用<br>"
    "・<b>com.amazonaws.&lt;region&gt;.ecr.dkr</b>（インターフェース型）— Dockerレジストリ操作用<br>"
    "・<b>com.amazonaws.&lt;region&gt;.s3</b>（<b>ゲートウェイ型</b>）— ECRはイメージレイヤをS3に格納するため必須<br>"
    "・<b>com.amazonaws.&lt;region&gt;.logs</b>（インターフェース型）— CloudWatch Logsへの書き込み用<br>"
    "・Secrets Manager/SSMから秘匿値を取る場合はそれらのエンドポイントも追加<br>"
    "<b>引っ掛け:</b> ECR APIエンドポイントだけでは不十分（S3エンドポイントなしだとイメージレイヤ取得失敗）。"
    "「awsvpcモードでpull失敗」と聞かれたら、まず <b>S3ゲートウェイエンドポイント漏れ</b>を疑う。"
)

LITE_TIP_ECR_CROSS = (
    "<br><br>"
    "<b>📌 判断ポイント — ECRのクロスアカウント/クロスリージョン共有</b><br>"
    "・<b>クロスアカウント共有</b>: ECRリポジトリポリシーで他アカウントのプリンシパル（例: aws:PrincipalOrgID）"
    "に <code>ecr:GetDownloadUrlForLayer</code> 等を許可。Organizations全体共有なら "
    "<code>aws:PrincipalOrgID</code> 条件キー一発で済む<br>"
    "・<b>クロスリージョンレプリケーション</b>: ECRレプリケーション設定で送信先リージョンを指定。"
    "DRリージョンに常時最新イメージを保持（Pilot Light等のDR戦略の前提）<br>"
    "・<b>ライフサイクルポリシー</b>: 古いイメージタグを自動削除（Lambdaで自前実装するのは <b>運用負荷大の典型誤答</b>）<br>"
    "・<b>イメージスキャン</b>: スキャンオンプッシュ → EventBridge（ECR Image Scan Complete イベント）"
    "→ Step Functions/Lambdaで脆弱性対応の自動化が定石"
)

LITE_TIP_SPOT_CAPACITY = (
    "<br><br>"
    "<b>📌 判断ポイント — Spot/Capacity Providerでのコスト最適化</b><br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>環境</th><th>Spot活用方法</th></tr>"
    "<tr><td>ECS on EC2</td><td><b>Capacity Provider</b>でEC2 Spot ASGを定義し、weightで"
    "オンデマンドとSpotの混合比率を制御。中断耐性のあるワークロード向け</td></tr>"
    "<tr><td>ECS on Fargate</td><td><b>FARGATE_SPOT</b>キャパシティプロバイダ。最大70%割引だが"
    "中断時はSIGTERM＋120秒猶予。バッチ・非同期処理向け</td></tr>"
    "<tr><td>EKS on EC2</td><td><b>マネージドノードグループ</b>でSpot指定、または"
    "<b>Karpenter</b>で動的にSpotノードをプロビジョン。Cluster Autoscalerと組み合わせ</td></tr>"
    "<tr><td>EKS on Fargate</td><td>Fargate Spotは<b>EKSでは未対応</b>（ECSのみ）</td></tr>"
    "</table>"
    "<b>Cluster Autoscaler vs Service Auto Scaling:</b> "
    "前者は<b>ノード数（Pod/タスクを載せる器）</b>、後者は<b>タスク/Pod数（コンテナそのもの）</b>を増減。"
    "両方を組み合わせて初めて完全な自動スケールになる。"
)

LITE_TIP_SERVICE_ASG = (
    "<br><br>"
    "<b>📌 判断ポイント — Service Auto Scalingのメトリクス選定</b><br>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>メトリクス</th><th>用途</th></tr>"
    "<tr><td><b>ECSServiceAverageCPUUtilization</b></td><td>CPUバウンドな汎用ワークロード</td></tr>"
    "<tr><td><b>ECSServiceAverageMemoryUtilization</b></td><td>メモリバウンドなワークロード（JVM等）</td></tr>"
    "<tr><td><b>ALBRequestCountPerTarget</b></td><td>HTTP/HTTPS APIで「タスク当たり何リクエスト捌くか」"
    "を直接制御したい時。最も予測精度が高い</td></tr>"
    "<tr><td>SQSキュー長（ApproximateNumberOfMessagesVisible）</td>"
    "<td>SQSコンシューマ型ワーカー。ターゲットトラッキングではなくステップスケーリング推奨</td></tr>"
    "</table>"
    "<b>覚え方:</b> 「APIサービス」ならALBRequestCountPerTarget、「キューワーカー」ならSQSキュー長、"
    "「リソース効率最適化」ならCPU/Memory。スケジュールが事前に分かっているなら<b>スケジュールドスケーリング</b>を併用。"
)

# ============================================================
# 問題ごとの分類（どのTIPを末尾に追加するか）
# ============================================================
# キー: 問題num
# 値: 追加TIPコード（FULL/LITE_QUADRANT/LITE_FARGATE_VS_LAMBDA/LITE_IRSA/
#                LITE_TASKROLE/LITE_ECR_PRIVATELINK/LITE_ECR_CROSS/LITE_SPOT_CAPACITY/LITE_SERVICE_ASG/NONE）
# 「FULL」は4象限選定がメインの問題、「LITE_*」はサブテーマ、「NONE」は加筆不要
# ============================================================

# 4象限選定が判断の核（FULL_TIP適用）
FULL_TIPS = {
    19,   # Lambda vs Fargate vs Glue/EMR
    27,   # ECS vs Batch (Fargate含む)
    31,   # Fargate移行（コード変更最小）
    77,   # API実装でEKS vs Lambda+Cognito比較
    82,   # ECS Fargate + Secrets Manager (Fargate前提)
    92,   # Lambda限界 → Fargate（互換性タイプの違い）
    99,   # Lambda vs EKS vs EC2 ASG
    107,  # Lambda 15分超 → Fargate
    131,  # ECS Service Auto Scaling
    143,  # Aurora Serverless（Fargate環境）
    173,  # Fargate月次バッチ（EBS不要化）
    175,  # EKS（既存Kubernetes資産）
    193,  # Fargate（Java マイクロサービス）
    203,  # 多数アプリのコスト最適化（Beanstalk vs Fargate）
    234,  # ECS EC2起動タイプ vs Lambda
    259,  # Fargate + MSK
    261,  # Fargate vs EC2ワーカー
    272,  # ECS awsvpc + タスクロール
    285,  # ECRレプリケーション + DR
    294,  # ECS Fargate vs EKS vs Lambda（環境分離）
    301,  # EKS（マルチティア・セッション継続性）
    406,  # Pilot Light DR（ECR + ECS）
    414,  # Compute Savings Plan（Fargate/Lambda）
    419,  # ECS on EC2（インフラ制御要件）
    428,  # Fargate + EFS共有ストレージ
    441,  # EKS + Fargate（運用負荷削減）
    456,  # Fargate（20分超バッチ）
    543,  # EKS（既存K8s資産）
    575,  # Fargate（インフラ管理最小）
    594,  # ECS Fargate + Aurora DR
    600,  # EKS + Spot（Pod再スケジュール）
    639,  # Fargate + EFS（NFSマイグレ）
    671,  # ECS Fargate + Blue/Green
}

# サブテーマ別（LITE_*）
LITE_TIPS = {
    7:   None,    # SQS+Lambda問題（コンテナはディストラクタ） → NONE
    12:  None,    # NLB問題（ECS言及はディストラクタ） → NONE
    29:  None,    # Aurora Serverless（コンテナはディストラクタ）
    56:  None,    # EKS Pod問題だがCloudFront 5xx診断 → NONE
    79:  'TASKROLE',   # ECS タスクロール権限削除（要修正＋IAMロール解説）
    90:  None,    # Glacier保管問題（コンテナはディストラクタ）
    124: None,    # コスト配分タグ問題
    154: None,    # S3+CloudFront移行（ECS言及はディストラクタ）
    158: None,    # CloudFront OAI（ECSは無関係）
    210: None,    # サーバーレス化（ECSはディストラクタ）
    222: 'ECR_PRIVATELINK',  # Fargate awsvpc + ECR PrivateLink（メインテーマ）
    231: 'SPOT_CAPACITY',  # Compute Savings Plan
    233: None,    # DR戦略（ECSはディストラクタ）
    237: None,    # WAF Rate Based Rule（ECS環境だがWAFが本題）
    262: None,    # Transfer Family（コンテナ案は誤答候補）
    268: None,    # IAMユーザー検知（ECSは誤答候補に出るのみ）
    275: None,    # CloudFormation IaC（ECSは誤答候補）
    281: None,    # API GW + DynamoDB（ECSは誤答候補）
    300: None,    # S3 Transfer Acceleration（ECS言及はディストラクタ）
    321: None,    # WAF Rate Based（EKS環境だがWAFが本題）
    332: None,    # CloudWatch Logs（ECS環境だがログ管理が本題）
    355: 'IRSA',  # EKSコスト配分タグ → タグ運用 + IRSAも触れる
    369: None,    # Aurora Global + DynamoDB Global（ECSは背景）
    376: None,    # CloudFront FLE（ECSは背景）
    380: 'ECR_CROSS',  # ECR Organizations共有
    395: None,    # Route 53 Resolver（ECS環境だがDNSが本題）
    405: None,    # CloudFront prefix list（ECS環境だがネットワークが本題）
    451: None,    # Migration Evaluator（EKS言及は背景）
    452: 'SPOT_CAPACITY',  # ECS Capacity Provider/スケジュールドスケーリング
    504: None,    # コスト配分タグ
    586: None,    # DataSync + Batch（コンテナは構成要素）
    623: 'IRSA',  # EKS + EFS（PodストレージとIRSA関連付け）
    631: None,    # WAF SQL Injection（ECS環境だがWAFが本題）
    637: None,    # WAF + CloudFront（ECS環境だが本題はセキュリティ）
    656: None,    # Global Accelerator（EKSは背景）
    672: 'ECR_CROSS',  # ECRイメージスキャン自動化
    673: 'SPOT_CAPACITY',  # Compute Savings Plan
}

# tip_codeから実際のtip文字列を取得
def get_lite_tip(code):
    if code is None:
        return None
    mapping = {
        'QUADRANT': LITE_TIP_QUADRANT,
        'FARGATE_VS_LAMBDA': LITE_TIP_FARGATE_VS_LAMBDA,
        'IRSA': LITE_TIP_IRSA,
        'TASKROLE': LITE_TIP_TASKROLE,
        'ECR_PRIVATELINK': LITE_TIP_ECR_PRIVATELINK,
        'ECR_CROSS': LITE_TIP_ECR_CROSS,
        'SPOT_CAPACITY': LITE_TIP_SPOT_CAPACITY,
        'SERVICE_ASG': LITE_TIP_SERVICE_ASG,
    }
    return mapping.get(code)

# 222 は ECR PrivateLink がメイン → FULLに加えてLITE_ECR_PRIVATELINKも併用したいが、
# FULL_TIPの最後に PITFALL_TIP として ECR エンドポイントの記述があるので、222 は LITE 側で上書きする。
# シンプルにするため: FULL_TIPSに含まれる問題はLITE_TIPSの設定を無視してFULLを適用する。

# ============================================================
# 個別の修正（明らかな間違い）
# ============================================================
# Q79: detail が別問題（サムネイル生成のLambda DLQ/DynamoDB WCU）の解説になっている。
# 実際のQ79は「ECSタスクロールからDynamoDB UpdateItem権限が削除された」がansB。
# 完全に書き直す。

REWRITE_DETAILS = {
    79: (
        "<b>判断の決め手：</b>「<b>IAMポリシー見直しの直後</b>」＋「<b>HTTP 400で AccessDeniedException</b>」"
        "＋「<b>キュー滞留（処理失敗が継続）</b>」が同時発生。これはサービス障害ではなく権限設定ミスのサイン。"
        "<br><br>"
        "<b>正解（B）:</b> ECSタスクロール（taskRoleArn）から <code>dynamodb:UpdateItem</code> 権限が剥奪されたことが原因。"
        "DynamoDB は権限不足の場合 <b>HTTP 400 + AccessDeniedException</b> を返す（HTTP 403 ではなく 400 という点に注意）。"
        "ECSエージェントが取得した一時クレデンシャルは正常に渡っているが、その認証情報に紐づくロールに必要な権限がないため、"
        "全リクエストが一律失敗してキューが滞留する。"
        "<br><br>"
        "<table border='1' cellpadding='4'>"
        "<tr><th>選択肢</th><th>判定</th></tr>"
        "<tr><td>A</td><td>サービス障害なら HTTP <b>5xx</b> が返る。HTTP 400 とは矛盾する</td></tr>"
        "<tr><td>B</td><td>◯ 権限剥奪 → AccessDeniedException → HTTP 400。"
        "「IAM見直し直後」「キュー滞留」の症状にぴたり一致</td></tr>"
        "<tr><td>C</td><td>タスクロールが引き当てられない場合は <b>credential取得自体が失敗</b>し、"
        "AccessDeniedException ではなく credential エラー（NoCredentialsProviderError 等）になる</td></tr>"
        "<tr><td>D</td><td>KMS復号権限不足の場合は <b>KMSAccessDeniedException</b>（KMS側のエラー）になり、"
        "DynamoDB自体のAccessDeniedExceptionとはエラー種別が異なる</td></tr>"
        "</table>"
    ),
}

# ============================================================
# メイン処理
# ============================================================

def build_updated_detail(num, original_detail):
    """対象問題のdetailを更新版で返す。修正がない場合はNoneを返す。"""
    # 1. まず明らかな間違いの書き直し
    if num in REWRITE_DETAILS:
        new_detail = REWRITE_DETAILS[num]
    else:
        new_detail = original_detail

    # 2. 末尾の判断ポイント追記
    tip_to_append = None
    if num in FULL_TIPS:
        tip_to_append = FULL_TIP
    elif num in LITE_TIPS:
        code = LITE_TIPS[num]
        tip_to_append = get_lite_tip(code)

    if tip_to_append:
        # 冪等性: 同じ見出し（コンテナ特化の📌セクション）が既にあれば再追加しない
        # 既存の汎用「📌 判断ポイント」セクション（Lambda vs Fargate等）はそのまま残し、
        # その後ろに新しいコンテナ特化セクションを追加する
        marker_full = '📌 判断ポイント — ECS/EKS'
        marker_quadrant = '📌 判断ポイント — コンテナ基盤の選択'
        marker_fargate_lambda = '📌 判断ポイント — Fargate vs Lambda'
        marker_irsa = '📌 判断ポイント — EKSのIAM権限付与'
        marker_taskrole = '📌 判断ポイント — ECSタスクの権限とネットワーク分離'
        marker_ecr_pl = '📌 判断ポイント — プライベートサブネットからECRへアクセス'
        marker_ecr_cross = '📌 判断ポイント — ECRのクロスアカウント'
        marker_spot = '📌 判断ポイント — Spot/Capacity Provider'
        marker_svc_asg = '📌 判断ポイント — Service Auto Scaling'
        existing_markers = [marker_full, marker_quadrant, marker_fargate_lambda, marker_irsa,
                            marker_taskrole, marker_ecr_pl, marker_ecr_cross, marker_spot,
                            marker_svc_asg]
        if any(m in new_detail for m in existing_markers):
            # 既に新しいコンテナ特化セクションが追加済みの場合のみスキップ
            return new_detail if new_detail != original_detail else None
        new_detail = new_detail + tip_to_append

    return new_detail if new_detail != original_detail else None


def main():
    target_nums = sorted(set(FULL_TIPS) | set(LITE_TIPS.keys()))
    print(f'[INFO] 対象問題数: {len(target_nums)}')

    # 書き込み直前にファイルを再読み込み
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    num_to_idx = {q['num']: i for i, q in enumerate(data)}

    modified = 0
    appended = 0
    skipped = 0
    rewrite_only = 0

    for num in target_nums:
        if num not in num_to_idx:
            print(f'[WARN] num={num} がJSONに見つかりません')
            skipped += 1
            continue
        q = data[num_to_idx[num]]
        original = q['explanation'].get('detail', '')
        new_detail = build_updated_detail(num, original)
        if new_detail is None:
            skipped += 1
            continue
        # detail更新
        q['explanation']['detail'] = new_detail
        # detailが書き直された&加筆もされたか分類
        if num in REWRITE_DETAILS and num in (FULL_TIPS | set(LITE_TIPS.keys())):
            # 加筆あり
            tip_added = num in FULL_TIPS or (num in LITE_TIPS and LITE_TIPS[num] is not None)
            if tip_added:
                rewrite_only += 1
                appended += 1
            else:
                rewrite_only += 1
        else:
            tip_added = num in FULL_TIPS or (num in LITE_TIPS and LITE_TIPS[num] is not None)
            if tip_added:
                appended += 1
        modified += 1

    # JSONとして検証
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    # 書き戻し
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        f.write(json_str)

    print(f'[DONE] 対象問題: {len(target_nums)}, 修正(detail書き直し): {len(REWRITE_DETAILS)}, '
          f'加筆(判断ポイント追加): {appended}, スキップ: {skipped}')

if __name__ == '__main__':
    main()
