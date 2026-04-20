#!/usr/bin/env python3
"""
Udemy問題 num 450〜524 に perspective と tips を追加するスクリプト
"""

import json

# perspective と tips のデータ（num をキーとする辞書）
ANNOTATIONS = {
    450: {
        "perspective": "クロスアカウント環境で S3 へのネットワークアクセス制御とポリシーベースのアクセス制限をどう組み合わせるかを判断できるか？",
        "tips": [
            "クロスアカウント S3 アクセス + ネットワーク制限 → ゲートウェイ VPC エンドポイント + S3 アクセスポイント + バケットポリシーの組み合わせ",
            "S3 バケットポリシーで特定のアクセスポイント ARN のみ許可 → s3:DataAccessPointArn 条件キーを使用",
            "IAM ロール条件（EC2側）ではなく バケットポリシー（S3側）でアクセスポイント制限を定義する",
        ]
    },
    451: {
        "perspective": "AWS への移行前の TCO 見積もりに最適なサービスをどう選択するかを判断できるか？",
        "tips": [
            "移行前の TCO 見積もり → Migration Evaluator（Quick Insights レポートで比較分析）",
            "DMS は移行ツール、TCO 評価ツールではない",
            "AWS Pricing Calculator は手動見積もり向け、実環境データの自動収集は不可",
        ]
    },
    452: {
        "perspective": "既知のトラフィックパターンとコスト最適化の要件に対して、スケーリング戦略と通信経路の最適化をどう判断するか？",
        "tips": [
            "繁忙期が事前に分かっている → 予測スケーリングではなくスケジュールドスケーリングを選択",
            "同一リージョン・同一アカウントの ECS → S3 トラフィックが NAT ゲートウェイを通過 → ゲートウェイ VPC エンドポイントでコスト削減",
            "S3 Transfer Acceleration は外部からのアップロード高速化用、同一リージョン内では効果なし",
        ]
    },
    453: {
        "perspective": "ステートフルアプリケーションの ALB スティッキーセッションと Aurora の読み取りスケーリングをどう正しく組み合わせるかを判断できるか？",
        "tips": [
            "ステートフルアプリ + スケールアウト → ALB + スティッキーセッション（同一サーバーにルーティング継続）",
            "Aurora の読み取りスケール → リードレプリカのオートスケーリング（ライターのスケーリングは不可）",
            "NLB はレイヤー4、スティッキーセッション（レイヤー7機能）は ALB で設定する",
        ]
    },
    454: {
        "perspective": "レスポンスヘッダーを User-Agent に基づいて動的に削除する要件に対して、CloudFront 関数と Lambda@Edge のどちらが適切かを判断できるか？",
        "tips": [
            "レスポンスヘッダーの動的削除（User-Agent 判定） → Lambda@Edge（ビューアレスポンス/オリジンレスポンストリガーで処理）",
            "CloudFront 関数はビューアリクエスト/レスポンスのみ対応、実行時間制限が短くロジックが限定的",
            "サーバーレス移行 + CloudFront + ヘッダー操作 → Lambda@Edge が最適解",
        ]
    },
    455: {
        "perspective": "クロスアカウントで Assume Role する際の信頼ポリシーとリソースポリシーの設定場所をどう判断するか？",
        "tips": [
            "クロスアカウントの Assume Role → 信頼ポリシーは引き受けられる側アカウントのロールに設定",
            "ロール A（Account A）がロール B（Account B）を引き受ける → Account B のロール B の信頼ポリシーに Account A のロール A を指定",
            "Permission boundary と信頼ポリシーは別物、混同しないこと",
        ]
    },
    456: {
        "perspective": "オンプレミスの Java アプリケーションを最小限の変更でコンテナ化してサーバーレスに移行するにはどう判断するか？",
        "tips": [
            "コンテナ化 + サーバーレス → ECR（イメージ格納）+ Fargate（サーバーレス実行）",
            "Fargate はサーバー管理不要、スポットインスタンスと組み合わせてコスト削減も可能",
            "EC2 ベースの ECS は Fargate より管理コストが高い、サーバーレス要件には Fargate を選択",
        ]
    },
    457: {
        "perspective": "マルチリージョン DR 構成で RDS フェイルオーバーと Auto Scaling の切り替えを自動化する方法をどう判断するか？",
        "tips": [
            "DR リージョンへの自動フェイルオーバー → Lambda + Route 53 ヘルスチェック + リードレプリカの昇格",
            "RDS リードレプリカの昇格は手動 or Lambda で自動化、Multi-AZ とは別概念",
            "Route 53 フェイルオーバーポリシー + ヘルスチェック → プライマリ障害時に自動的にセカンダリに切り替え",
        ]
    },
    458: {
        "perspective": "高トラフィックの読み書きが混在するアプリケーションのデータベース層とキャッシュ層の可用性をどう確保するかを判断できるか？",
        "tips": [
            "ElastiCache for Redis + 高可用性 → マルチ AZ 有効化 + レプリケーショングループ",
            "RDS 読み取りスケール + フェイルオーバー → マルチ AZ DB クラスター or リードレプリカ",
            "セッションストアとキャッシュ両用途 → Redis（データ永続性あり）を選択、Memcached は永続性なし",
        ]
    },
    459: {
        "perspective": "オリジンサーバー障害時にユーザーへカスタムエラーページを返す CloudFront の設定をどう判断するか？",
        "tips": [
            "ALB が 502 返す → CloudFront カスタムエラーレスポンス → S3 の静的ページにリダイレクト",
            "CloudFront のカスタムエラーレスポンスは特定 HTTP ステータスコードに対して代替 URL を返せる",
            "オリジン障害時の対応 → CloudFront + S3 静的サイトの組み合わせでフォールバック実現",
        ]
    },
    460: {
        "perspective": "AWS Organizations でサブネットを共有して複数アカウントのワークロードを同一 VPC にデプロイする設計をどう判断するか？",
        "tips": [
            "複数アカウントで同一 VPC サブネット共有 → AWS RAM（Resource Access Manager）でサブネットを共有",
            "インフラアカウントが VPC・サブネット所有、プロダクトアカウントは共有サブネットにリソースデプロイ",
            "VPC ピアリングは別 VPC 間の接続、同一 VPC サブネットの共有には RAM を使う",
        ]
    },
    461: {
        "perspective": "サードパーティの SaaS サービスをプライベートネットワーク経由で安全に利用するための接続方式をどう判断するか？",
        "tips": [
            "サードパーティ SaaS へのプライベート接続 → AWS PrivateLink（インターフェース VPC エンドポイント）",
            "PrivateLink はインターネットを経由せず、トラフィックは AWS ネットワーク内に留まる",
            "VPC ピアリングはアドレス重複不可、PrivateLink はアドレス重複を気にせず利用可能",
        ]
    },
    462: {
        "perspective": "オンプレミスとクラウド混在環境で統一的なパッチ管理を実現するサービスをどう判断するか？",
        "tips": [
            "オンプレミス + EC2 の統合パッチ管理 → AWS Systems Manager Patch Manager（ハイブリッド対応）",
            "オンプレミスサーバーに SSM エージェントをインストール → マネージドインスタンスとして管理可能",
            "SSM は EC2 だけでなくオンプレミスサーバーも管理対象にできる（ハイブリッドアクティベーション）",
        ]
    },
    463: {
        "perspective": "Auto Scaling グループ内の EC2 インスタンスからログを S3 に集約する運用自動化をどう実装するかを判断できるか？",
        "tips": [
            "EC2 ログを S3 に定期転送 → SSM ドキュメント + Run Command / Maintenance Window で自動化",
            "Auto Scaling 環境でインスタンスが増減 → SSM でインスタンス IDではなくタグベースでターゲット指定",
            "CloudWatch Logs Agent でストリーミング送信 vs SSM で定期バッチ転送 → 要件に応じて選択",
        ]
    },
    464: {
        "perspective": "クロスアカウントで Route 53 プライベートホストゾーンを共有して DNS 名前解決を行う設定をどう判断するか？",
        "tips": [
            "クロスアカウントでプライベートホストゾーン共有 → ホストゾーンの VPC 関連付け承認 + Route 53 での関連付け",
            "手順：ホストゾーン所有アカウントで承認作成 → もう一方のアカウントで VPC を関連付け",
            "RAM ではプライベートホストゾーンは共有できない、Route 53 API での承認フローを使う",
        ]
    },
    465: {
        "perspective": "画像処理ワークフローを CloudFront + Lambda@Edge でオンデマンド変換する設計をどう判断するか？",
        "tips": [
            "画像をオンデマンドで変換 → CloudFront + Lambda@Edge（オリジンリクエスト時に変換処理）",
            "変換済み画像を S3 にキャッシュ → 2回目以降は CloudFront キャッシュから返すためコスト削減",
            "EFS → S3 への画像移行 + CloudFront 配信でグローバルキャッシュ効果を最大化",
        ]
    },
    466: {
        "perspective": "Direct Connect の冗長性を高めてシングルポイント障害を排除するための構成をどう判断するか？",
        "tips": [
            "Direct Connect の冗長化 → 2つの Direct Connect 接続 + Direct Connect ゲートウェイ",
            "Direct Connect ゲートウェイは複数 VPC・複数リージョンへの接続を1つのゲートウェイで管理",
            "冗長化には異なるロケーション or 異なる接続から2本引く、LAG はバンドル障害リスクあり",
        ]
    },
    467: {
        "perspective": "動画のアップロード・変換・配信のサーバーレスパイプラインをどう設計するかを判断できるか？",
        "tips": [
            "動画アップロード → 変換 → 配信 → S3 + S3 イベント通知 + MediaConvert + CloudFront",
            "S3 イベント通知でアップロードを検知 → Lambda が MediaConvert ジョブをトリガー",
            "動画配信は CloudFront で大規模配信、直接 S3 公開は避けコスト・セキュリティを改善",
        ]
    },
    468: {
        "perspective": "Lambda の新バージョンデプロイ時にトラフィックを段階的に移行してリスクを最小化する手法をどう判断するか？",
        "tips": [
            "Lambda カナリアデプロイ → AWS SAM + CodeDeploy でエイリアスウェイトを徐々に移行",
            "SAM の AutoPublishAlias + DeploymentPreference で Canary/Linear デプロイを簡単設定",
            "Lambda エイリアスの routing-config で旧バージョンと新バージョンのトラフィック割合を制御",
        ]
    },
    469: {
        "perspective": "長期保存が必要なアーカイブデータのコスト最小化ストレージ戦略をどう選択するかを判断できるか？",
        "tips": [
            "長期アーカイブ（取り出し頻度低）+ コスト最小 → S3 Glacier Deep Archive",
            "S3 バケットのデフォルトストレージクラス設定 → 新規オブジェクトを自動的に指定クラスで保存",
            "Glacier Instant Retrieval（ms）、Glacier Flexible Retrieval（数分〜時間）、Deep Archive（12時間）",
        ]
    },
    470: {
        "perspective": "既存の Active Directory を使って AWS アカウントへの SSO アクセスをどう実装するかを判断できるか？",
        "tips": [
            "オンプレミス AD + AWS SSO → IAM Identity Center + AD Connector でフェデレーション",
            "AD Connector は既存 AD との連携に使用、AWS Managed Microsoft AD は AD の AWS 移行用",
            "IAM Identity Center（旧 AWS SSO）で複数アカウントの権限管理を一元化",
        ]
    },
    471: {
        "perspective": "API Gateway のスロットリングと使用量プランを使ってピーク時の負荷を制御する設計をどう判断するか？",
        "tips": [
            "API のレート制限・クォータ管理 → API Gateway 使用量プランでスロットリング上限を設定",
            "使用量プランは API キーと紐付け、クライアントごとに異なるレート設定が可能",
            "バーストリミット（瞬間）とレートリミット（秒あたり）の2つの制限を使用量プランで設定",
        ]
    },
    472: {
        "perspective": "アクセスパターンが不明な共有ファイルシステムのデータを S3 に移行する際のストレージクラス選択をどう判断するか？",
        "tips": [
            "アクセスパターン不明のデータ移行 → S3 Intelligent-Tiering（自動的に最適なティアに移動）",
            "EFS/共有ファイルシステム → S3 移行 → DataSync または AWS Transfer Family を検討",
            "Intelligent-Tiering はモニタリング料金あり、アクセス頻度が完全に不明な場合に最適",
        ]
    },
    473: {
        "perspective": "固定 IP アドレスが必要なマルチ AZ 構成のロードバランシングをどう設計するかを判断できるか？",
        "tips": [
            "固定 IP + ロードバランサー → Network Load Balancer（各 AZ に Elastic IP を割り当て可能）",
            "ALB は固定 IP を持てない（DNS ベース）、固定 IP 要件は NLB を選択",
            "NLB + Elastic IP → ホワイトリスト登録が必要な企業顧客向けシナリオに最適",
        ]
    },
    474: {
        "perspective": "可用性要件（AZ 障害耐性）とコスト効率を両立するインスタンス配置とキャパシティ予約の戦略をどう判断するか？",
        "tips": [
            "AZ 障害耐性 + コスト最適化 → 3 AZ にインスタンスを分散 + Capacity Reservation で余裕を持たせる",
            "1 AZ 障害時に残り 2 AZ でサービス継続 → 各 AZ のキャパシティを n+余裕で確保",
            "Capacity Reservation はリージョン問わず特定 AZ のキャパシティを保証する",
        ]
    },
    475: {
        "perspective": "データベース認証情報の安全な管理と自動ローテーションをどうサービス選択するかを判断できるか？",
        "tips": [
            "DB パスワードの安全な保存 + 自動ローテーション → AWS Secrets Manager",
            "Secrets Manager は RDS 統合で自動ローテーション Lambda を内蔵、設定が簡単",
            "SSM Parameter Store（SecureString）はローテーション機能なし、Secrets Manager を選択",
        ]
    },
    476: {
        "perspective": "API Gateway から DynamoDB に直接統合してサーバーレスアーキテクチャを構築する際の統合タイプをどう判断するか？",
        "tips": [
            "API Gateway → DynamoDB 直接統合 → AWS サービス統合（AWS 統合タイプ）を使用",
            "Lambda を介さず API Gateway が直接 DynamoDB API を呼び出せる、レイテンシ削減・コスト削減",
            "マッピングテンプレートで API Gateway リクエストを DynamoDB リクエスト形式に変換",
        ]
    },
    477: {
        "perspective": "複数ドメインを1つの SSL 証明書でカバーし CloudFront と ALB で使用する証明書管理をどう判断するか？",
        "tips": [
            "複数ドメイン対応の SSL 証明書 → ACM でワイルドカード証明書 or SAN 証明書を作成",
            "CloudFront で使う ACM 証明書 → us-east-1 リージョンで作成必須（グローバルサービスのため）",
            "ALB で使う ACM 証明書 → ALB と同一リージョンで作成",
        ]
    },
    478: {
        "perspective": "AWS Organizations で部門ごとのコストを追跡・レポートする仕組みをどう設計するかを判断できるか？",
        "tips": [
            "組織全体のコスト追跡 → 管理アカウントでコスト配分タグを有効化 + CUR で詳細レポート",
            "CUR（Cost and Usage Report）は最も詳細なコストデータ、タグ別・アカウント別集計が可能",
            "タグのアクティベーションは管理アカウントの Billing で行う、メンバーアカウントでは不可",
        ]
    },
    479: {
        "perspective": "CloudFormation StackSets を使ってマルチアカウント・マルチリージョンにネットワークを一括展開する方法をどう判断するか？",
        "tips": [
            "複数アカウント・複数リージョンへの一括デプロイ → CloudFormation StackSets",
            "StackSets の権限モード：セルフマネージド（個別 IAM ロール設定）vs サービスマネージド（Organizations 連携）",
            "Transit Gateway + StackSets で組織全体の VPC ネットワーク構成を一元管理",
        ]
    },
    480: {
        "perspective": "AWS Private Marketplace を使って組織内での承認済みソフトウェア調達を管理する方法をどう判断するか？",
        "tips": [
            "社内承認済みマーケットプレイス → AWS Private Marketplace で承認済み製品カタログを作成",
            "Private Marketplace 管理者ロール → AWSPrivateMarketplaceAdminFullAccess ポリシーが必要",
            "SCP でマーケットプレイス購入を制限 + Private Marketplace で承認済み製品のみ許可",
        ]
    },
    481: {
        "perspective": "SCP（Service Control Policy）でデフォルト許可から明示的な許可ベースの制御に切り替える方法をどう判断するか？",
        "tips": [
            "SCP のデフォルト → FullAWSAccess SCP が暗黙的に全アクション許可、これをデタッチすると全拒否になる",
            "FullAWSAccess SCP をデタッチ → 明示的な Allow SCP がないと全アクションが拒否される",
            "SCP は許可の上限を設定、IAM との AND 条件で有効なアクセス権限が決まる",
        ]
    },
    482: {
        "perspective": "モノリシック API を Lambda 関数に分割してスケーラビリティとコスト効率を改善する設計をどう判断するか？",
        "tips": [
            "モノリス API → マイクロサービス化 → API Gateway + 個別 Lambda 関数に分割",
            "REST API でリソース・メソッドごとに異なる Lambda をバックエンドに設定可能",
            "Lambda は関数単位でスケール、独立デプロイ・独立スケールが可能になる",
        ]
    },
    483: {
        "perspective": "AWS Organizations 全体のコストを CUR で集約し、チームごとに分析できる環境をどう設計するかを判断できるか？",
        "tips": [
            "組織全体のコスト集約 → 管理アカウントから CUR を作成、全メンバーアカウントのコストを含む",
            "Athena + QuickSight で CUR データを分析・可視化 → SQLクエリでタグ・アカウント別集計",
            "コストカテゴリ vs タグ → タグは各サービスに付与、コストカテゴリは CUR 上での論理的な分類",
        ]
    },
    484: {
        "perspective": "オンプレミス Windows ファイルサーバーと Amazon FSx 間でデータを同期するサービスをどう判断するか？",
        "tips": [
            "オンプレミス → FSx for Windows へのデータ同期 → AWS DataSync でスケジュール転送",
            "DataSync は S3, EFS, FSx などに対応、暗号化・整合性チェック込みで転送",
            "Storage Gateway（File Gateway）は常時マウント用途、DataSync は移行・同期バッチ用途",
        ]
    },
    485: {
        "perspective": "S3 クロスリージョンレプリケーションとマルチリージョンアクセスポイントで DR を実現する設計をどう判断するか？",
        "tips": [
            "S3 のマルチリージョン DR → S3 CRR（クロスリージョンレプリケーション）でセカンダリに複製",
            "S3 マルチリージョンアクセスポイント → 最も近いリージョンの S3 バケットに自動ルーティング",
            "CRR + マルチリージョンアクセスポイント → 可用性とパフォーマンスを両立したグローバル S3 構成",
        ]
    },
    486: {
        "perspective": "CloudFormation で ALB + Auto Scaling の標準 Web 構成をコード化する際の設計をどう判断するか？",
        "tips": [
            "ALB + Auto Scaling + EC2 の標準 Web 層構成 → CloudFormation で IaC 化",
            "Auto Scaling グループは LaunchTemplate または LaunchConfiguration で EC2 設定を定義",
            "CloudFormation でマルチ AZ 配置 → サブネットに複数 AZ を指定、ALB もマルチ AZ 有効化",
        ]
    },
    487: {
        "perspective": "CloudFormation StackSets のサービスマネージドモードで Organizations 全体に自動デプロイする設定をどう判断するか？",
        "tips": [
            "Organizations の全アカウントに自動デプロイ → StackSets のサービス管理権限 + 組織全体をターゲット",
            "サービスマネージドモード → 新規メンバーアカウント追加時に自動でスタックをデプロイできる",
            "セルフマネージドモードは手動で各アカウントに AWSCloudFormationStackSetAdministrationRole が必要",
        ]
    },
    488: {
        "perspective": "大規模オンプレミス環境の移行前評価に Application Discovery Service と Migration Hub をどう組み合わせるかを判断できるか？",
        "tips": [
            "移行前の依存関係・性能評価 → Application Discovery Agent をインストールして情報収集",
            "Migration Hub で全移行状況を一元管理 → Discovery データを基に移行計画を立案",
            "Agentless Discovery（VMware環境）vs Agent-based Discovery（物理機・非VMware）の使い分け",
        ]
    },
    489: {
        "perspective": "S3 へのアクセスをプライベートネットワーク経由に限定しつつエンドポイントポリシーで制御する設計をどう判断するか？",
        "tips": [
            "VPC から S3 へのプライベートアクセス + アクセス制限 → ゲートウェイ VPC エンドポイント + エンドポイントポリシー",
            "エンドポイントポリシーで特定 S3 バケット・アクション・プリンシパルを制限可能",
            "ゲートウェイエンドポイントはルートテーブルにエントリを追加、インターフェースエンドポイントは DNS 経由",
        ]
    },
    490: {
        "perspective": "ECS サービスの読み取りベースのオートスケーリングをターゲット追跡で実装する方法をどう判断するか？",
        "tips": [
            "ECS タスクのオートスケーリング → Application Auto Scaling + ターゲット追跡スケーリングポリシー",
            "ターゲット追跡 → CPU使用率やリクエスト数などのメトリクスを目標値に維持するよう自動調整",
            "ECS の Auto Scaling は EC2 の Auto Scaling とは別、Application Auto Scaling を使う",
        ]
    },
    491: {
        "perspective": "Web サーバーの負荷分散と非同期処理を SQS で実現してシステムを疎結合化する設計をどう判断するか？",
        "tips": [
            "リクエスト急増 + 処理遅延 → SQS キューで受け取り、コンシューマー（EC2/Lambda）が非同期処理",
            "SQS で疎結合化 → Web サーバーとバックエンド処理を分離、独立スケール可能",
            "SQS FIFO vs Standard → 順序保証が必要なら FIFO、高スループット優先なら Standard",
        ]
    },
    492: {
        "perspective": "OpenSearch Service のコスト最適化でホットデータとウォームデータを分離するノード構成をどう判断するか？",
        "tips": [
            "OpenSearch コスト削減 → 古いデータを UltraWarm ノードへ移動（ストレージコスト大幅削減）",
            "UltraWarm は S3 ベースのストレージ、クエリ頻度の低いデータに最適",
            "データノード数を減らして UltraWarm 追加 → ホット/ウォームティアで用途別コスト最適化",
        ]
    },
    493: {
        "perspective": "SCP でセキュリティグループの 0.0.0.0/0 インバウンドルール作成を特定 OU に制限する方法をどう判断するか？",
        "tips": [
            "EC2 セキュリティグループの 0.0.0.0/0 禁止 → SCP で ec2:AuthorizeSecurityGroupIngress を条件付き拒否",
            "aws:SourceIp や条件キーで特定の CIDR を含む場合のみ拒否するポリシーを作成",
            "SCP は OU に適用、配下の全アカウントに継承される",
        ]
    },
    494: {
        "perspective": "Webhook を受け取って処理する GitHub Apps をサーバーレスで実装する際のサービス選択をどう判断するか？",
        "tips": [
            "Webhook 受信 + サーバーレス処理 → API Gateway HTTP API + Lambda（低コスト・低レイテンシ）",
            "HTTP API は REST API よりシンプルで安価、Webhook のような単純な HTTP エンドポイントに最適",
            "GitHub Apps の Webhook → HMAC 署名検証を Lambda で実装してセキュリティを確保",
        ]
    },
    495: {
        "perspective": "移行前に各サーバーのスペック・依存関係・ネットワーク通信を把握する Discovery の方法をどう判断するか？",
        "tips": [
            "オンプレミスサーバーの移行前調査 → Application Discovery Agent で CPU・メモリ・ネットワーク接続情報を収集",
            "Migration Hub でデータを可視化、グループ化して移行ウェーブを計画",
            "Agent ベース vs Agentless：エージェントなしで VMware 環境から収集するなら vCenter 経由",
        ]
    },
    496: {
        "perspective": "プライベートサブネットのインスタンスからインターネットへのアウトバウンド通信を可能にするための構成をどう判断するか？",
        "tips": [
            "プライベートサブネット → インターネットへのアウトバウンド → NAT ゲートウェイ + Elastic IP",
            "NAT ゲートウェイはパブリックサブネットに配置、プライベートサブネットのルートテーブルから参照",
            "NAT ゲートウェイは AZ 障害に備えて各 AZ に1つ配置することを推奨",
        ]
    },
    497: {
        "perspective": "Lambda からRDSへの接続数増加問題を解決するためのデータベース接続管理をどう判断するか？",
        "tips": [
            "Lambda + RDS の接続数問題 → RDS Proxy で接続プールを管理（接続数を大幅削減）",
            "Lambda ハンドラー外でDB接続を初期化 → コンテナ再利用時に接続を再利用してオーバーヘッド削減",
            "RDS Proxy + Lambda → 最大接続数を超えないように制御、IAM 認証対応",
        ]
    },
    498: {
        "perspective": "EC2 インスタンスで HTTPS を終端して ACM 証明書を使う標準的な Web 構成をどう判断するか？",
        "tips": [
            "HTTPS + EC2 + 証明書管理 → ALB で TLS 終端 + ACM 証明書（EC2 に証明書不要）",
            "ACM 証明書は ALB/CloudFront/API Gateway にアタッチ可能、EC2 には直接使えない",
            "ALB で HTTPS 終端 → バックエンド EC2 との通信は HTTP（内部ネットワーク）でも可",
        ]
    },
    499: {
        "perspective": "オンプレミスの MySQL を Aurora MySQL に最小ダウンタイムで移行する方法をどう判断するか？",
        "tips": [
            "MySQL → Aurora MySQL 移行 + 最小ダウンタイム → AWS DMS でレプリケーション",
            "DMS の全ロード + CDC（継続的変更キャプチャ）でライブマイグレーション可能",
            "移行後の切り替えはDNS変更 or アプリの接続先変更で短時間のダウンタイムのみ",
        ]
    },
    500: {
        "perspective": "S3 バケットへのアップロード時に KMS 暗号化を強制するポリシー設定をどう判断するか？",
        "tips": [
            "S3 への暗号化強制 → バケットポリシーで aws:SecureTransport + 暗号化ヘッダーなしの PutObject を拒否",
            "SSE-KMS 強制 → s3:x-amz-server-side-encryption が aws:kms でない場合は拒否",
            "デフォルト暗号化設定だけでは強制できない、バケットポリシーでの明示的な拒否が必要",
        ]
    },
    501: {
        "perspective": "マルチリージョンの Web アプリケーションでグローバルな低レイテンシ配信をどう設計するかを判断できるか？",
        "tips": [
            "グローバル配信 + 低レイテンシ → CloudFront + 複数リージョン ALB/EC2 でオリジングループ",
            "CloudFront のオリジングループ → プライマリ障害時にセカンダリリージョンへ自動フェイルオーバー",
            "Route 53 レイテンシルーティング vs CloudFront → 静的コンテンツはCloudFront、動的はRoute 53",
        ]
    },
    502: {
        "perspective": "AWS RAM でプレフィックスリストを共有して内部 IP 範囲の管理を一元化する設計をどう判断するか？",
        "tips": [
            "複数アカウントで共通のセキュリティグループルール → マネージドプレフィックスリスト + RAM で共有",
            "プレフィックスリストを更新するだけで全アカウントのセキュリティグループルールが自動更新",
            "RAM でプレフィックスリスト共有 → 受け取り側アカウントはセキュリティグループで参照するだけ",
        ]
    },
    503: {
        "perspective": "Lambda 関数のリソース設定（メモリ・CPU）を最適化してコストパフォーマンスを改善する方法をどう判断するか？",
        "tips": [
            "Lambda のサイジング最適化 → AWS Compute Optimizer の Lambda 推奨事項を利用",
            "ExportLambdaFunctionRecommendations API で推奨事項を一括エクスポートし分析",
            "Compute Optimizer は EC2、ECS、EBS、Lambda の最適なリソースサイズを機械学習で推奨",
        ]
    },
    504: {
        "perspective": "複数アプリケーションのコストを可視化・追跡するための Cost Explorer とコストカテゴリの活用をどう判断するか？",
        "tips": [
            "アプリ別コスト追跡 → Cost Explorer 有効化 + コストカテゴリでアプリ単位に分類",
            "コストカテゴリ → タグ・アカウント・サービスなどの条件でコストをグループ化",
            "CUR + Athena は詳細分析向け、Cost Explorer は即時可視化・ダッシュボード向け",
        ]
    },
    505: {
        "perspective": "会社所有の IP アドレスレンジを AWS で使い Elastic IP として割り当てる BYOIP の手順をどう判断するか？",
        "tips": [
            "自社所有 IP を AWS で使用 → BYOIP（Bring Your Own IP）でアドレスブロックを AWS に登録",
            "BYOIP 手順：ROA 作成 → AWS へのアドバタイズ承認 → Elastic IP として割り当て",
            "BYOIP は IP アドレスの所有権を維持しながら AWS 環境で利用可能",
        ]
    },
    506: {
        "perspective": "Lambda の新バージョンに対してエイリアスを使いトラフィックを段階的に移行するデプロイ戦略をどう判断するか？",
        "tips": [
            "Lambda カナリアデプロイ → エイリアスに routing-config で新旧バージョンの重みを設定",
            "update-alias --routing-config でトラフィック割合を指定（例：新版10%、旧版90%）",
            "CodeDeploy との違い：エイリアス直接操作は手動制御、CodeDeploy は自動的に段階移行",
        ]
    },
    507: {
        "perspective": "SFTP サーバーをクラウドに移行しつつ既存の DNS レコードを変更せずに引き継ぐ方法をどう判断するか？",
        "tips": [
            "SFTP サーバーの AWS 移行 → AWS Transfer for SFTP（マネージド SFTP サービス）",
            "カスタムホスト名 → Route 53 の CNAME を Transfer Family のエンドポイントに変更",
            "ユーザー認証は IAM、Cognito、またはカスタム ID プロバイダーで対応可能",
        ]
    },
    508: {
        "perspective": "VMware 上の仮想マシンを AWS EC2 にリフト&シフト移行する際の移行ツール選択をどう判断するか？",
        "tips": [
            "VMware VM の AWS 移行 → OVF/OVA エクスポート → VM Import/Export または AWS MGN",
            "VM Import/Export：OVF 形式で S3 にアップロードし AMI に変換",
            "AWS MGN（Application Migration Service）は継続的レプリケーションでダウンタイム最小化",
        ]
    },
    509: {
        "perspective": "アプリケーションをコンテナ化して ECS/EKS に移行する際のイメージ管理とデプロイ自動化をどう設計するかを判断できるか？",
        "tips": [
            "コンテナ化 + AWS デプロイ → Docker イメージ → ECR に Push → ECS/EKS でデプロイ",
            "CI/CD パイプライン → CodePipeline + CodeBuild でイメージビルド・ECR Push・ECS デプロイを自動化",
            "ECR はプライベートレジストリ、ECR Public は公開用、用途に応じて使い分ける",
        ]
    },
    510: {
        "perspective": "S3 バケットへのアクセス権限が不足している開発者に対して最小権限で権限を追加する方法をどう判断するか？",
        "tips": [
            "S3 アクセス権限不足 → IAM ポリシーまたは S3 バケットポリシーで s3 アクションを許可",
            "最小権限の原則 → 必要な S3 アクション（GetObject、PutObject 等）のみを明示的に許可",
            "IAM エンティティへの権限追加 vs バケットポリシー → 管理しやすい方を選択（クロスアカウントはバケットポリシー必須）",
        ]
    },
    511: {
        "perspective": "EBS スナップショットのライフサイクル管理と長期アーカイブを自動化する方法をどう判断するか？",
        "tips": [
            "EBS スナップショットの自動作成・保持・削除 → Amazon DLM（Data Lifecycle Manager）",
            "DLM でスナップショットの作成スケジュール・保持期間・削除を自動管理",
            "古いスナップショットをアーカイブ → EBS スナップショットアーカイブ（低コストストレージ層）",
        ]
    },
    512: {
        "perspective": "クロスアカウント S3 バケット間でデータをコピーする際の IAM 権限設定をどう判断するか？",
        "tips": [
            "クロスアカウント S3 コピー → 宛先アカウントのユーザーが実行、ソースバケットポリシーで読み取りを許可",
            "aws s3 sync でクロスアカウントコピー → 実行者はソース・宛先両方への権限が必要",
            "宛先バケットの所有権設定 → Object Ownership で「BucketOwnerPreferred」に設定するとコピー先が所有者になる",
        ]
    },
    513: {
        "perspective": "Control Tower のガードレールを使って本番環境への予防的・発見的コントロールを適用する方法をどう判断するか？",
        "tips": [
            "Control Tower ガードレール → 強く推奨（予防的）・推奨（発見的）・必須の3段階",
            "特定 OU への適用 → ガードレールを選択して OU を指定、配下の全アカウントに適用",
            "予防的ガードレール（SCP）→ アクションを禁止、発見的ガードレール（Config）→ 違反を検出",
        ]
    },
    514: {
        "perspective": "EC2 インスタンスを SSH なしで安全にアクセス・管理する方法をどう判断するか？",
        "tips": [
            "SSH レスの EC2 管理 → AWS Systems Manager Session Manager（SSM）",
            "SSM エージェント + AmazonSSMManagedInstanceCore ポリシー付き IAM ロールで有効化",
            "Session Manager はポート開放不要、踏み台不要、操作ログを CloudTrail/S3 に記録可能",
        ]
    },
    515: {
        "perspective": "予算超過時にアラートを出してリソースを自動的に停止・削除する仕組みをどう判断するか？",
        "tips": [
            "予算超過 → 自動アクション → AWS Budgets アクション（SNS 通知 + IAM ポリシー適用 or Lambda 呼び出し）",
            "Budgets アクション → IAM ポリシーをアタッチして権限を剥奪 or Lambda で削除処理を実行",
            "Cost Anomaly Detection は異常検出、Budgets は閾値ベースのアラート・アクション",
        ]
    },
    516: {
        "perspective": "Lambda 関数を別 AWS アカウントに移行する際のデプロイパッケージと設定の移行手順をどう判断するか？",
        "tips": [
            "Lambda のクロスアカウント移行 → デプロイメントパッケージをダウンロードして Target アカウントで再作成",
            "Lambda レイヤー・環境変数・IAM ロール・VPC 設定も合わせて移行が必要",
            "AWS Migration Hub + Application Migration Service では Lambda の移行は非対応",
        ]
    },
    517: {
        "perspective": "S3 へのファイルアップロードをトリガーにした ETL 処理をサーバーレスで実装する方法をどう判断するか？",
        "tips": [
            "S3 アップロード → 自動処理 → S3 イベント通知 + Lambda（サーバーレス ETL）",
            "S3 イベント通知の宛先：Lambda、SQS、SNS から選択",
            "大規模データ処理には Lambda より Glue や EMR が適切、小〜中規模なら Lambda で十分",
        ]
    },
    518: {
        "perspective": "マルチリージョンの Active-Active 構成で高可用性を実現するネットワーク設計をどう判断するか？",
        "tips": [
            "マルチリージョン Active-Active → 各リージョンに VPC + ALB + EC2 Auto Scaling を配置",
            "グローバルトラフィック分散 → Route 53 レイテンシルーティング or Global Accelerator",
            "データ同期 → DynamoDB Global Tables or Aurora Global Database でマルチリージョン書き込み",
        ]
    },
    519: {
        "perspective": "AWS Organizations と IAM Identity Center でオンプレミス AD と SSO を統合する方法をどう判断するか？",
        "tips": [
            "Organizations + オンプレミス AD + SSO → IAM Identity Center + AD Connector（or AWS Managed AD）",
            "AD Connector → 既存 AD の認証情報をそのまま利用、AD のデータは AWS に同期されない",
            "AWS Managed Microsoft AD → AD データを AWS に持ち込む場合、AD 信頼関係でオンプレミスと連携",
        ]
    },
    520: {
        "perspective": "大容量動画ファイルを S3 に効率よくアップロードするための転送最適化をどう判断するか？",
        "tips": [
            "大容量ファイルの S3 アップロード → マルチパートアップロード（部分失敗時の再送が可能）",
            "S3 Transfer Acceleration → CloudFront エッジ経由でアップロード、地理的に遠い場合に有効",
            "マルチパートアップロードは 100MB 以上のファイルに推奨、1ファイルあたり最大 10,000 パート",
        ]
    },
    521: {
        "perspective": "Lambda や EC2 からの大量DB接続によるRDS接続数枯渇をRDS Proxyで解決する方法をどう判断するか？",
        "tips": [
            "RDS への接続数過多 → RDS Proxy で接続プールを共有、接続数を大幅削減",
            "RDS Proxy エンドポイントにアプリの接続先を変更するだけで適用可能",
            "RDS Proxy は IAM 認証対応、Secrets Manager でDB認証情報を管理できる",
        ]
    },
    522: {
        "perspective": "大量の IoT デバイスを安全に認証・接続管理するサービス選択をどう判断するか？",
        "tips": [
            "IoT デバイスの安全な接続管理 → AWS IoT Core（MQTT/HTTPS 対応、証明書ベース認証）",
            "デバイスごとに IoT Thing + 証明書 + ポリシーを作成してきめ細かいアクセス制御",
            "IoT Core ルールエンジン → デバイスデータを S3/DynamoDB/Lambda/Kinesis に転送",
        ]
    },
    523: {
        "perspective": "開発者が CloudFormation 経由でのみリソースをプロビジョニングできるよう IAM 権限を制限する方法をどう判断するか？",
        "tips": [
            "CloudFormation 経由のみリソース作成を許可 → IAM ポリシーで CloudFormation アクションのみ許可 + ロールを制限",
            "Service Control Policy（SCP）または Permission Boundary でさらに制限可能",
            "CloudFormation スタックのロールを指定 → スタック作成者ではなくロールの権限でリソース作成",
        ]
    },
    524: {
        "perspective": "大量のレコードを高スループットで書き込みつつ TTL で自動削除する設計をどう判断するか？",
        "tips": [
            "大量データの高スループット書き込み + 自動期限切れ → DynamoDB + TTL 属性",
            "DynamoDB TTL → 指定した UNIX タイムスタンプの属性値に基づいて期限切れアイテムを自動削除",
            "DynamoDB はサーバーレス・スケーラブル、定期的なバッチ削除より TTL の方が運用コストが低い",
        ]
    },
}


def main():
    json_path = "/Users/aki/aws-sap/docs/data/questions.json"

    # ファイルを再読み込み
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 対象問題数の確認
    targets = [q for q in data if q.get("source") == "udemy" and 450 <= q.get("num", 0) <= 524]
    print(f"対象問題数: {len(targets)}")

    # ANNOTATIONS に含まれる num のセット
    annotation_nums = set(ANNOTATIONS.keys())
    target_nums = set(q["num"] for q in targets)
    missing = target_nums - annotation_nums
    if missing:
        print(f"WARNING: ANNOTATIONS に未定義の num があります: {sorted(missing)}")
        return

    # 各問題を更新
    updated_count = 0
    for q in data:
        num = q.get("num", 0)
        if q.get("source") == "udemy" and 450 <= num <= 524:
            ann = ANNOTATIONS[num]
            q["explanation"]["perspective"] = ann["perspective"]
            q["explanation"]["tips"] = ann["tips"]
            updated_count += 1

    print(f"更新した問題数: {updated_count}")

    # 保存
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("保存完了！")

    # 確認
    with open(json_path, "r", encoding="utf-8") as f:
        verify = json.load(f)

    sample = [q for q in verify if q.get("source") == "udemy" and q.get("num") == 450][0]
    print(f"\n--- 検証（num=450）---")
    print(f"perspective: {sample['explanation']['perspective']}")
    print(f"tips: {sample['explanation']['tips']}")


if __name__ == "__main__":
    main()
