#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Udemy問題 num 600〜674 の explanation に perspective と tips を追加するスクリプト
（ハードコード版）
- detail はそのまま維持
- perspective と tips のみ追加
"""

import json

DATA_PATH = "/Users/aki/aws-sap/docs/data/questions.json"

NEW_EXPLANATIONS = {
    600: {
        "perspective": "EKSのコスト最適化において、コンピューティング・データベース・ストレージの各レイヤーでどの割引・節約手段を組み合わせるか？",
        "tips": [
            "「EKS + 長期コミットメント」→ Compute Savings Plans（EC2 Instance SavingsよりEKS対応が広い）",
            "「スパイク対応 + コスト削減」→ Spot インスタンス（中断耐性ワークロード前提）",
            "「RDS長期利用」→ Reserved Instances（1年/3年）で最大65%割引"
        ]
    },
    601: {
        "perspective": "S3をオリジンとするCloudFrontで、メンテナンス時にS3の別バケットにトラフィックを切り替えるにはどのアーキテクチャが適切か？",
        "tips": [
            "「CloudFront + S3プライベートアクセス」→ OAI（Origin Access Identity）またはOAC（Origin Access Control）",
            "「CloudFrontでオリジン切り替え」→ オリジングループ（プライマリ失敗時にセカンダリへフェイルオーバー）",
            "「メンテナンスページの切り替え」→ セカンダリオリジンにS3静的サイト、CloudFrontオリジングループで自動切替"
        ]
    },
    602: {
        "perspective": "Lambdaの新バージョンを段階的にリリースしてロールバックも容易にするには、どのデプロイ戦略が最適か？",
        "tips": [
            "「Lambda段階的リリース」→ エイリアス + 加重トラフィック設定（例: v2に10%、v1に90%）",
            "「Lambdaバージョン固定参照」→ エイリアス（$LATESTではなく固定バージョン番号を使う）",
            "「ロールバック容易性」→ エイリアスの加重を0に変更するだけで即時切り戻し可能"
        ]
    },
    603: {
        "perspective": "マルチリージョンで低レイテンシかつ高可用性が必要なアプリに、グローバルネットワーク加速とデータ複製をどう組み合わせるか？",
        "tips": [
            "「TCP/UDP + グローバル低レイテンシ」→ Global Accelerator（Anycastで最近傍エッジ経由）",
            "「マルチリージョンDynamoDB」→ グローバルテーブル（マルチアクティブ、自動レプリケーション）",
            "「CloudFront vs Global Accelerator」→ HTTP静的コンテンツ=CloudFront、TCP/動的API=Global Accelerator"
        ]
    },
    604: {
        "perspective": "複数のLambda関数で共通ライブラリを一元管理・共有するための最適な仕組みは何か？",
        "tips": [
            "「Lambda共有ライブラリ」→ Lambda レイヤー（複数関数で同一レイヤーを参照）",
            "「Lambdaコンテナイメージ」→ 共有ライブラリをベースイメージに組み込み、ECRで管理",
            "「ライブラリの更新管理」→ レイヤーはバージョン管理あり、古いバージョンへの参照も維持可能"
        ]
    },
    605: {
        "perspective": "インターネット接続なしのエッジデバイスでMLモデルを実行・更新するには、どのAWSサービスが適切か？",
        "tips": [
            "「エッジML実行（オフライン）」→ AWS IoT Greengrass（ローカル推論、クラウド同期）",
            "「IoTエッジデプロイ」→ Greengrass コンポーネント（モデル・コードをデバイスにデプロイ）",
            "「SageMaker vs Greengrass」→ SageMakerはクラウド学習、Greengrassはエッジ推論"
        ]
    },
    606: {
        "perspective": "既存オンプレミス資産（CMDBデータ）を活用してAWS移行のビジネスケースを作成するには、どのツールが最適か？",
        "tips": [
            "「移行コスト試算 + 既存CMDBデータ活用」→ Migration Evaluator（CMDBインポート対応）",
            "「Migration Evaluator vs Application Discovery Service」→ Evaluatorは財務分析・TCO比較、ADSはサーバー依存関係検出",
            "「移行フェーズ別ツール」→ 評価: Evaluator、検出: ADS、移行実行: Migration Hub"
        ]
    },
    607: {
        "perspective": "大規模・組織全体のDDoS対策で、コスト保護やSRTサポートなど高度な機能が必要な場合はどのサービスを選ぶか？",
        "tips": [
            "「DDoS + コスト保護 + SRTサポート」→ Shield Advanced（月額固定＋DDoS関連コスト免除）",
            "「Shield Standard vs Advanced」→ Standard=無料・自動・L3/L4基本保護、Advanced=有料・L7対応・専門チームサポート",
            "「WAF + Shield Advanced」→ セットで使うとL7アプリ層まで総合DDoS対策が可能"
        ]
    },
    608: {
        "perspective": "グローバルにアクティブ-アクティブ構成で、RDBとNoSQLの両方をマルチリージョン対応させる構成はどれか？",
        "tips": [
            "「Auroraマルチリージョン（書き込み可）」→ Aurora グローバルデータベース（プライマリ1、読み取り専用セカンダリ複数）",
            "「DynamoDBマルチリージョン書き込み」→ DynamoDB グローバルテーブル（全リージョンで書き込み可）",
            "「RPO/RTO最小化」→ Aurora Global DB（RPO<1秒）+ DynamoDB Global Table の組み合わせ"
        ]
    },
    609: {
        "perspective": "ALBの前に静的IPアドレスが必要な要件で、かつL7ロードバランシングも維持するにはどう構成するか？",
        "tips": [
            "「ALB + 静的IP」→ ALB単独では静的IP不可、NLBを前段に置くかGlobal Acceleratorを使う",
            "「NLB → ALB構成」→ NLBのターゲットにALBを指定（IPターゲット）して静的IP + L7を実現",
            "「Global Accelerator + ALB」→ 静的AnyCast IP + ALBのL7機能を組み合わせる別解"
        ]
    },
    610: {
        "perspective": "ALBへのアクセスをCloudFront経由に限定するセキュリティ制御を、IPアドレス管理の手間なく実現するには？",
        "tips": [
            "「CloudFrontのIPレンジをALBで許可」→ CloudFront管理プレフィックスリスト（AWSが自動更新）をALBのSGに設定",
            "「CloudFront → ALBの直接アクセス防止」→ カスタムヘッダー検証またはプレフィックスリストによるSG制御",
            "「プレフィックスリスト」→ AWSマネージドのIPリスト、手動更新不要でSG参照可能"
        ]
    },
    611: {
        "perspective": "ElastiCacheの認証・通信暗号化・クレデンシャル管理を、運用負担を最小化しながら安全に実装するには？",
        "tips": [
            "「ElastiCache Redis認証」→ AUTH トークン（パスワード設定）",
            "「ElastiCache通信暗号化」→ TLS（転送中暗号化）を有効化",
            "「認証情報の安全な保管」→ Parameter Store（SecureString）またはSecrets Managerに格納"
        ]
    },
    612: {
        "perspective": "Spotインスタンスの中断リスクを減らすため、特定インスタンスタイプへの依存を避けるベストプラクティスは何か？",
        "tips": [
            "「Spot可用性向上」→ 複数インスタンスタイプを指定（容量プールを分散）",
            "「属性ベースインスタンスタイプ選択」→ vCPU/メモリ要件を指定、ASGが適合する複数タイプを自動選択",
            "「Spot Fleet vs ASG」→ ASGで「属性ベース選択 + Spot」が現代的・推奨アプローチ"
        ]
    },
    613: {
        "perspective": "オンプレミスのNFSファイルサーバーをAWSに移行する際、EC2インスタンスが透過的にNFSアクセスできる構成はどれか？",
        "tips": [
            "「オンプレNFS → AWSクラウドへ移行、NFSのまま使いたい」→ S3ファイルゲートウェイ（NFSマウントでS3に格納）",
            "「Storage Gateway種類」→ ファイル=S3/FSxゲートウェイ、ボリューム=iSCSI、テープ=仮想テープ",
            "「EFS vs S3ファイルゲートウェイ」→ EFSはEC2ネイティブNFS（オンプレ不要）、S3GWはオンプレNFS移行に最適"
        ]
    },
    614: {
        "perspective": "マイクロサービス間でユーザーIDの変更イベントを非同期・疎結合で伝達するアーキテクチャはどれが最適か？",
        "tips": [
            "「サービス間イベント駆動連携」→ EventBridge（イベントバス）でソースサービスからターゲットへルーティング",
            "「EventBridge vs SNS vs SQS」→ EventBridge=複雑ルーティング・多対多、SNS=Pub/Sub、SQS=キュー（ポーリング）",
            "「マイクロサービス間ID同期」→ EventBridgeルールで特定イベントパターンを他サービスのLambdaへルーティング"
        ]
    },
    615: {
        "perspective": "複数リージョンのALBに対して静的IPで単一エントリポイントを提供し、レイテンシを最小化するには何を使うか？",
        "tips": [
            "「静的IP + マルチリージョンALB」→ Global Accelerator（2つの静的AnyCast IP）",
            "「Global Acceleratorエンドポイント」→ ALB, NLB, EC2, Elastic IPを指定可能",
            "「CloudFront vs Global Accelerator」→ HTTP/HTTPS静的・動的コンテンツ=CloudFront、TCP/非HTTP=Global Accelerator"
        ]
    },
    616: {
        "perspective": "AWS Organizationsの全アカウントで、EBSボリューム暗号化を必須化するガバナンス制御をどう実装するか？",
        "tips": [
            "「組織全体の強制ポリシー」→ Control Tower（ガードレール）またはOrganizations SCP",
            "「EBS暗号化の強制」→ SCP で `ec2:CreateVolume` に `ec2:Encrypted: true` 条件を付与",
            "「新規アカウントへの適用」→ Control Tower のカスタマイズ（CfCT）またはSCPをOUルートに適用"
        ]
    },
    617: {
        "perspective": "RPO/RTOが数分以内のDR要件で、EC2ワークロードとRDSを別リージョンに迅速にフェイルオーバーするには？",
        "tips": [
            "「EC2のDR（数分RTO）」→ Elastic Disaster Recovery（AWS DRS）：継続的レプリケーション＋ワンクリック起動",
            "「RDSのDR」→ クロスリージョンリードレプリカ（フェイルオーバー時に昇格）",
            "「Pilot Light vs Warm Standby vs Multi-Site」→ DRS=ほぼPilot Light（コスト低）、Warm=常時起動、Multi-Site=最速・最高コスト"
        ]
    },
    618: {
        "perspective": "EC2インスタンスのライトサイジングに必要なOSレベルメトリクス収集と、推奨サイズ提案を最小運用で実現するには？",
        "tips": [
            "「EC2 OSレベルメトリクス」→ CloudWatchエージェント（メモリ・ディスク使用率など標準外メトリクスを収集）",
            "「ライトサイジング推奨」→ Compute Optimizer（過去メトリクスを分析して最適インスタンスタイプを提案）",
            "「Compute Optimizer有効化条件」→ 14日以上のメトリクスデータが必要、CloudWatchエージェントでリッチデータ収集推奨"
        ]
    },
    619: {
        "perspective": "CodeCommitリポジトリへのプッシュを検知して自動的にS3やECRにバックアップを取るCI/CDパイプラインをどう構築するか？",
        "tips": [
            "「CodeCommitイベントトリガー」→ EventBridge（CodeCommit PushイベントをCodeBuildへルーティング）",
            "「Gitリポジトリバックアップ」→ CodeBuild でgit cloneしてS3にアーカイブ（またはECRにイメージ保存）",
            "「CodeCommit廃止注意」→ 新規ユーザーへのCodeCommit提供停止（2024年〜）、移行はGitHubやCodeCatalyst推奨"
        ]
    },
    620: {
        "perspective": "別アカウントのVPCにあるサービスをプライベートに公開する際、インターネットを経由せずセキュアに接続するには？",
        "tips": [
            "「クロスアカウントプライベートサービス公開」→ AWS PrivateLink（VPCエンドポイントサービス）",
            "「PrivateLink構成」→ サービス側: NLB → エンドポイントサービス、消費側: VPCインターフェースエンドポイント",
            "「VPCピアリング vs PrivateLink」→ ピアリング=双方向・CIDR重複不可、PrivateLink=単方向・CIDR重複OK"
        ]
    },
    621: {
        "perspective": "S3バケットが意図せずパブリックに公開された場合に、自動検知してセキュリティチームに通知するアーキテクチャはどれか？",
        "tips": [
            "「S3公開設定の継続監視」→ IAM Access Analyzer for S3（パブリックアクセス・クロスアカウント共有を検出）",
            "「検出→通知自動化」→ EventBridge（Access Analyzerの検出イベント）→ SNS → メール/Slack通知",
            "「Config vs Access Analyzer」→ Configはルール評価、Access Analyzerはリソースポリシーのアクセス到達性分析"
        ]
    },
    622: {
        "perspective": "オンプレミスサーバーの移行計画策定において、サーバー依存関係の把握とTCO比較の両方を行うにはどのツールが適切か？",
        "tips": [
            "「移行前サーバー依存関係マッピング」→ Application Discovery Service（エージェントまたはエージェントレスでサーバー情報収集）",
            "「移行TCO・コスト試算」→ Migration Evaluator（既存コストとAWSコストを比較）",
            "「ADS → Migration Hub」→ ADSで収集したデータをMigration Hubに統合して移行追跡"
        ]
    },
    623: {
        "perspective": "複数のKubernetesポッドが同一ファイルシステムを読み書き共有する必要がある場合、EKSで使うべきストレージは？",
        "tips": [
            "「EKSマルチポッド共有ストレージ（ReadWriteMany）」→ EFS（NFS互換、複数EC2/Podから同時マウント可）",
            "「EBS vs EFS vs S3」→ EBS=単一EC2アタッチ（RWO）、EFS=マルチEC2共有（RWX）、S3=オブジェクト",
            "「EKS + EFS」→ EFS CSIドライバーを使いPersistentVolumeとして利用"
        ]
    },
    624: {
        "perspective": "既存のコンタクトセンターをAWSに刷新し、アウトバウンドキャンペーン（SMS/メール）も含めたソリューションはどれか？",
        "tips": [
            "「クラウドコンタクトセンター」→ Amazon Connect（インバウンド・アウトバウンド音声・チャット対応）",
            "「アウトバウンドSMS/メールキャンペーン」→ Amazon Pinpoint（マーケティングキャンペーン・アウトリーチ）",
            "「Connect vs Pinpoint」→ Connect=コンタクトセンター（エージェント応対）、Pinpoint=マーケティング送信（大量通知）"
        ]
    },
    625: {
        "perspective": "Amazon Connectのコンタクトセンターを別リージョンにフェイルオーバーさせるDR構成はどう実現するか？",
        "tips": [
            "「Amazon Connect DR」→ クロスリージョンにバックアップConnectインスタンスを作成、Route 53フェイルオーバーで切り替え",
            "「Connect設定の複製」→ Connect設定をコードで管理（Infrastructure as Code）してDRリージョンに展開",
            "「Route 53ヘルスチェック + フェイルオーバー」→ プライマリ障害時にDNSレベルでバックアップへ自動切り替え"
        ]
    },
    626: {
        "perspective": "サードパーティのデータセットをAWSマーケットプレイス経由で取得し、自社Redshiftで分析するには何を使うか？",
        "tips": [
            "「外部データセット取得」→ AWS Data Exchange（データ提供者からサブスクリプション形式でS3/Redshiftに配信）",
            "「Redshift外部データ統合」→ Redshift Data Sharingまたは外部スキーマ（Spectrum）でS3データをクエリ",
            "「Data Exchange → Redshift」→ Data ExchangeでサブスクライブしたデータセットをRedshiftに直接ロード可能"
        ]
    },
    627: {
        "perspective": "Lambda処理失敗時にメッセージを失わず、後で再処理できるようにするデッドレターキュー設計はどうすべきか？",
        "tips": [
            "「Lambda非同期失敗処理」→ DLQ（SQS）またはEventBridge失敗ルールに失敗メッセージを送る",
            "「SNS → Lambda失敗時」→ Lambdaに直接DLQを設定（SQS）、失敗メッセージをDLQに移動",
            "「SQS → Lambda失敗時」→ SQSのソースキューにDLQを設定（maxReceiveCount超過後にDLQへ）"
        ]
    },
    628: {
        "perspective": "大量のIoTデバイスからのHTTPリクエストを非同期で受け付けてバックエンド処理に渡すサーバーレス構成はどれか？",
        "tips": [
            "「IoT大量リクエスト受付」→ API Gateway + SQS（同期処理不要なら直接SQSに入れてLambdaが処理）",
            "「API Gateway統合先」→ Lambda（同期）/ SQS（非同期デカップリング）/ Kinesis（ストリーミング）",
            "「IoT Core vs API Gateway」→ MQTT/CoAP=IoT Core、HTTP REST=API Gateway"
        ]
    },
    629: {
        "perspective": "AWS Organizationsの組織単位（OU）間のネットワークを分離しつつ、各OU内のVPCを接続するにはどう設計するか？",
        "tips": [
            "「OU内VPC接続 + OU間分離」→ Transit Gateway を OU単位で作成（クロスOU共有しない）",
            "「Transit Gateway共有」→ RAM（Resource Access Manager）でTGWを同一OU内アカウントに共有",
            "「OU間通信が必要な場合」→ 特定OU間のみTGWピアリングで接続（細かい制御が可能）"
        ]
    },
    630: {
        "perspective": "S3に保存するドキュメントを暗号化し、転送中も保護するための最小構成はどれか？",
        "tips": [
            "「S3保存時暗号化」→ SSE-S3（デフォルト）またはSSE-KMS（CMK管理・監査証跡）",
            "「S3転送中暗号化強制」→ バケットポリシーで `aws:SecureTransport: false` を Deny",
            "「SSE-S3 vs SSE-KMS vs SSE-C」→ S3管理=SSE-S3、KMS管理=SSE-KMS、顧客管理キー=SSE-C"
        ]
    },
    631: {
        "perspective": "ECS Fargateで動くWebアプリへのSQLインジェクション攻撃を防ぐためのAWSサービス選択はどれか？",
        "tips": [
            "「SQLインジェクション防御」→ AWS WAF（マネージドルール: SQL インジェクション検知）",
            "「WAFのアタッチ先」→ ALB / CloudFront / API Gateway（ECSの前段に配置）",
            "「WAF マネージドルール」→ AWS管理ルールグループ（無料）でSQLi/XSS等を簡単に有効化"
        ]
    },
    632: {
        "perspective": "IoTデバイスが接続するMQTTエンドポイントをマルチリージョンでDR対応させ、データもリージョン間で同期するには？",
        "tips": [
            "「IoT CoreのDR」→ Route 53フェイルオーバー（IoT Coreカスタムエンドポイント）でリージョン切り替え",
            "「IoTデータのマルチリージョン同期」→ DynamoDBグローバルテーブル（IoT Coreルール→DynamoDB→グローバルレプリケーション）",
            "「IoT Core + Route 53」→ カスタムドメインをIoT Coreに設定してRoute 53でヘルスチェック・フェイルオーバー"
        ]
    },
    633: {
        "perspective": "クロスアカウントでDynamoDBテーブルへのアクセスを許可する際、特定の属性のみに絞ったきめ細かな制御はどう実装するか？",
        "tips": [
            "「クロスアカウントDynamoDBアクセス」→ リソースベースポリシー（現在DynamoDBはリソースポリシー非対応）→ IAMロール + STSクロスアカウント",
            "「DynamoDB属性レベルアクセス制御」→ IAMポリシーの `dynamodb:Attributes` 条件キーで特定属性のみ許可",
            "「クロスアカウントIAM」→ ターゲットアカウントにロール作成、ソースアカウントからAssumeRole"
        ]
    },
    634: {
        "perspective": "複数リージョンのS3バケット間でデータを自動複製し、最も近いリージョンから低レイテンシでアクセスさせるには？",
        "tips": [
            "「S3マルチリージョン複製」→ S3 CRR（Cross-Region Replication）で複数リージョンに自動コピー",
            "「マルチリージョンS3の統一アクセスポイント」→ S3マルチリージョンアクセスポイント（最近傍リージョンへ自動ルーティング）",
            "「CRR + マルチリージョンAP」→ CRRでデータ複製 + マルチリージョンAPで透過的アクセスの組み合わせが定番"
        ]
    },
    635: {
        "perspective": "IoTデバイスからのMQTTデータをリアルタイム処理してドキュメントDBに格納し、グローバルにコンテンツ配信するアーキテクチャは？",
        "tips": [
            "「MQTT大量デバイスデータ受付」→ IoT Core（MQTT）→ IoT Rulesでルーティング",
            "「柔軟スキーマのドキュメント格納」→ Amazon DocumentDB（MongoDB互換）",
            "「グローバルコンテンツ配信」→ CloudFront（静的・動的コンテンツのエッジキャッシュ）"
        ]
    },
    636: {
        "perspective": "データ主権やコンプライアンスでオンプレミス処理が必要なワークロードと、インターネット接続なしのエッジ処理をどう実現するか？",
        "tips": [
            "「オンプレミスでAWSサービス実行」→ AWS Outposts（AWSマネージドハードウェアをオンプレに設置）",
            "「インターネット非接続エッジ処理」→ Snowball Edge（オフラインデータ処理・収集）",
            "「Outposts vs Snowball Edge」→ Outposts=常設・低レイテンシ、Snowball Edge=移動・バッチ収集・オフライン"
        ]
    },
    637: {
        "perspective": "ECSで動くWebアプリをWAFで保護し、L7攻撃（SQLi/XSS等）をブロックしつつグローバル配信するには？",
        "tips": [
            "「ECSアプリのL7セキュリティ」→ CloudFront + WAF（エッジでフィルタリング）またはALB + WAF",
            "「WAFのエッジ適用」→ CloudFrontにWAFをアタッチするとグローバルエッジでブロック（最も早い段階）",
            "「マネージドWAFルール」→ AWSマネージドルールグループでSQLi/XSS/既知悪意IPをすぐに有効化可能"
        ]
    },
    638: {
        "perspective": "CloudFrontのオリジン（ALB）が障害時に自動的にS3のフォールバックコンテンツを返すにはどう設定するか？",
        "tips": [
            "「CloudFrontオリジン障害時フォールバック」→ オリジングループ（プライマリ=ALB、セカンダリ=S3）",
            "「オリジングループのフェイルオーバー条件」→ 5xx エラー時にセカンダリへ自動切り替え",
            "「S3静的サイトホスティング vs S3オリジン」→ フェイルオーバー先にはS3静的ウェブサイトエンドポイントを使う"
        ]
    },
    639: {
        "perspective": "ECS Fargateのコンテナ間で永続化された共有ファイルシステムが必要な場合、適切なストレージサービスはどれか？",
        "tips": [
            "「ECS Fargate共有永続ストレージ」→ Amazon EFS（NFS、Fargateから直接マウント可能）",
            "「EFS vs EBS（ECS）」→ EBS=EC2起動型ECS（Fargateは非対応）、EFS=Fargate対応・タスク間共有",
            "「ECS + EFSマウント」→ タスク定義のvolumeでEFSを指定、複数タスクが同時アクセス可能"
        ]
    },
    640: {
        "perspective": "新バージョンのアプリを本番環境に段階的に展開して問題があれば即座に切り戻すカナリアデプロイをALBで実現するには？",
        "tips": [
            "「ALBカナリアデプロイ」→ 加重ターゲットグループ（例: 新バージョン10%、旧バージョン90%）",
            "「加重ルーティング調整」→ 問題なければ比率を徐々に100%に移行、問題あれば0%に戻すだけ",
            "「CodeDeployブルー/グリーン vs ALB加重」→ CodeDeploy=自動化・スケジュール、ALB加重=手動・細かい制御"
        ]
    },
    641: {
        "perspective": "FSxファイルシステムの障害復旧や、ストレージパフォーマンス向上のために既存データを移行するには何を使うか？",
        "tips": [
            "「FSxのバックアップ・復元」→ AWS Backup（FSx対応、クロスリージョンバックアップも可能）",
            "「FSx for Windows → FSx for Lustreへの移行」→ DataSync（ファイル単位の高速移行）",
            "「FSx復元」→ バックアップからの新規FSx作成（インプレース復元はFSxのポイントインタイム復元）"
        ]
    },
    642: {
        "perspective": "グローバルなメディア配信でS3データを複数リージョンに複製し、ユーザーが最も近いリージョンから自動的に取得できるようにするには？",
        "tips": [
            "「S3グローバル配信 + 自動リージョン選択」→ S3マルチリージョンアクセスポイント + CRR",
            "「CRR（Cross-Region Replication）」→ ソースバケットから複数のデスティネーションバケットへ自動複製",
            "「マルチリージョンAPの利点」→ 単一ARN/エンドポイントで複数リージョンに透過的ルーティング"
        ]
    },
    643: {
        "perspective": "オンプレ.NETアプリをAWSにリホストする際、高スループットNICが必要な計算集約型ワークロードに適したEC2インスタンスと、セッション管理の外部化はどうすべきか？",
        "tips": [
            "「高ネットワークスループット要件」→ c5n インスタンスファミリー（最大100Gbpsネットワーク帯域）",
            "「.NETセッション外部管理」→ ElastiCache Redis（セッションをRedisに移して水平スケール可能に）",
            "「リホスト vs リアーキテクチャ」→ リホスト=Lift & Shift（最速）、セッション外部化は最小限の変更で可用性向上"
        ]
    },
    644: {
        "perspective": "オンプレのWebサーバー・DBサーバー構成をサーバーレス化してコスト削減・スケール改善し、データ分析基盤も整備するには？",
        "tips": [
            "「サーバーレスWeb + API」→ S3+CloudFront（静的）+ API Gateway + Lambda（動的）",
            "「サーバーレスデータ分析」→ Athena（S3のデータをSQLクエリ）+ QuickSight（BIダッシュボード）",
            "「Aurora Serverless」→ 可変負荷のRDBをサーバーレス化、最小時は0スケール"
        ]
    },
    645: {
        "perspective": "S3バケットへのアクセスをCloudTrailで記録し、特定操作（例: PutObject）を検知してリアルタイムに通知する仕組みはどれか？",
        "tips": [
            "「S3操作のリアルタイム通知」→ CloudTrail（データイベント記録）→ EventBridge → SNS",
            "「CloudTrail管理イベント vs データイベント」→ 管理=API操作全般、データ=S3オブジェクト操作（追加設定が必要）",
            "「S3イベント通知 vs CloudTrail」→ S3イベント=シンプル・オブジェクト操作限定、CloudTrail=全AWS API記録・監査向け"
        ]
    },
    646: {
        "perspective": "オンプレミスからDirect Connectを経由して複数AWSリージョンのVPCに接続するには、どのDirect Connect構成が必要か？",
        "tips": [
            "「DX + マルチリージョンVPC接続」→ Direct Connect Gateway（単一DX接続から複数リージョンのVGWに接続）",
            "「パブリックサービス（S3等）へのDX経由アクセス」→ パブリックVIF（Public Virtual Interface）",
            "「DX Gateway vs Transit VIF」→ DX Gateway=VGW経由（VPC直結）、Transit VIF=Transit Gateway経由（スケーラブル）"
        ]
    },
    647: {
        "perspective": "組織全体のCloudFrontディストリビューションにWAFルールを一元管理・強制適用するガバナンス構成はどれか？",
        "tips": [
            "「組織全体WAF一元管理」→ AWS Firewall Manager（OrganizationsとWAFを統合、ポリシー自動適用）",
            "「Firewall Manager対象サービス」→ WAF, Shield Advanced, Security Groups, Network Firewall, Route 53 Resolver",
            "「Config + Firewall Manager」→ ConfigでコンプライアンスチェックしFirewall Managerで自動修復・強制"
        ]
    },
    648: {
        "perspective": "SAMLフェデレーション経由でAWSコンソールにSSO接続できない場合、IAM側とIdP側のどこを確認・修正すべきか？",
        "tips": [
            "「SAML SSO失敗の切り分け」→ IAMロールの信頼ポリシー（SAML IdPを信頼しているか）を最初に確認",
            "「SAMLアサーション検証」→ IdPのSAMLレスポンスに `sts:RoleArn` と `sts:RoleSessionName` 属性が含まれているか",
            "「AssumeRoleWithSAML」→ SAML認証後にSTSで一時クレデンシャルを取得するフロー"
        ]
    },
    649: {
        "perspective": "Lambdaなどサーバーレスから大量の同時接続が発生するAurora DB接続を効率化し、接続数上限エラーを防ぐには？",
        "tips": [
            "「Lambda → Aurora接続数問題」→ RDS Proxy（接続プーリングでDB接続数を削減）",
            "「RDS Proxy利点」→ 接続の多重化（Multiplexing）、フェイルオーバー時の接続維持、Secrets Manager統合",
            "「RDS Proxy対応DB」→ Aurora MySQL/PostgreSQL, RDS MySQL/PostgreSQL/SQL Server（MariaDB一部対応）"
        ]
    },
    650: {
        "perspective": "CloudFormationでインフラを管理しているEC2アプリを、別リージョンにDRとして展開してRoute 53で自動フェイルオーバーさせるには？",
        "tips": [
            "「CloudFormationマルチリージョン展開」→ StackSets（組織単位で複数リージョン・アカウントに同時デプロイ）",
            "「EC2のDR展開」→ Elastic Disaster Recovery（継続的レプリケーション）またはCloudFormationでスタック複製",
            "「Route 53自動フェイルオーバー」→ ヘルスチェック付きフェイルオーバーレコード（プライマリ障害時にセカンダリに切り替え）"
        ]
    },
    651: {
        "perspective": "100TB規模のオンプレミスデータベースをインターネット帯域の制約なしにAWSへ移行するには、どのアプローチが現実的か？",
        "tips": [
            "「大容量データ（数十〜数百TB）をAWSへ転送」→ Snowball Edge（物理輸送、ペタバイト規模まで対応）",
            "「DB移行（スキーマ + データ変換）」→ AWS DMS（Database Migration Service）",
            "「Snowball + DMS組み合わせ」→ Snowballでバルクデータ転送後、DMSで差分同期・スキーマ変換"
        ]
    },
    652: {
        "perspective": "EC2インスタンスとそのデータをクロスリージョンでバックアップし、障害時に別リージョンへ迅速に復元するには？",
        "tips": [
            "「EC2クロスリージョンバックアップ」→ AWS Backup（クロスリージョンコピー設定、自動スケジュール）",
            "「CloudFormationでインフラ復元」→ DRリージョンにも同じCloudFormationテンプレートをデプロイ",
            "「AWS Backup対応リソース」→ EC2, EBS, RDS, Aurora, DynamoDB, EFS, FSx, S3等"
        ]
    },
    653: {
        "perspective": "S3に保存するメディアファイルの暗号化と、CloudFront経由での安全な配信を両立させる最小構成はどれか？",
        "tips": [
            "「S3暗号化 + CloudFront HTTPS」→ SSE-KMS（S3暗号化）+ CloudFront HTTPS Only（ViewerProtocolPolicy: redirect-to-https）",
            "「CloudFront + S3のプライベート配信」→ OAC/OAIでS3を非公開、CloudFront経由のみアクセス許可",
            "「メディアファイルの保護」→ S3暗号化（保存時）+ HTTPS（転送時）+ CloudFront署名付きURL（アクセス制御）"
        ]
    },
    654: {
        "perspective": "Lambdaがデータベース接続に使うクレデンシャルを安全に管理し、自動ローテーションも実現するには何を使うか？",
        "tips": [
            "「DBクレデンシャルの安全管理 + 自動ローテーション」→ Secrets Manager（自動ローテーション設定可能）",
            "「Lambda → Secrets Manager」→ 実行時にGetSecretValueで取得、環境変数にハードコードしない",
            "「Secrets Manager + KMS CMK」→ シークレットをCMKで暗号化、KMSへのアクセス制御でシークレット保護を強化"
        ]
    },
    655: {
        "perspective": "SQL Server上の.NETアプリをAWSに移行する際、SQL ServerライセンスコストをなくしてPostgreSQL互換にするには？",
        "tips": [
            "「SQL Server → PostgreSQL移行（.NET対応）」→ Aurora PostgreSQL + Babelfish（T-SQLをそのまま実行可能）",
            "「Babelfish利点」→ .NETアプリのSQL Server接続コードをほぼ変更せずにAurora PostgreSQLで動作",
            "「SCT（Schema Conversion Tool）」→ SQL ServerスキーマをPostgreSQL互換に変換するツール"
        ]
    },
    656: {
        "perspective": "HTTPSのカスタムメソッド（非標準）を含むトラフィックをグローバルに最適なエンドポイントへルーティングするには何を使うか？",
        "tips": [
            "「非標準HTTPメソッド + グローバルルーティング」→ Global Accelerator（任意のTCP/UDP対応）",
            "「CloudFront vs Global Accelerator（HTTPメソッド）」→ CloudFrontはGET/HEAD/POST等標準メソッドのみ、GAは任意TCP",
            "「Global Accelerator利点」→ Anycast静的IP + AWSバックボーン + 任意プロトコル対応"
        ]
    },
    657: {
        "perspective": "既存のMQTTブローカーをAWS IoT Coreに移行する際、デバイス側の接続先変更を最小化するにはどう設定するか？",
        "tips": [
            "「IoT CoreカスタムMQTTエンドポイント」→ IoT Coreカスタムドメイン設定（既存ドメインをIoT Coreに向ける）",
            "「Route 53 + IoT Core」→ カスタムドメインのCNAMEをIoT Coreエンドポイントに設定",
            "「IoT Core移行ポイント」→ デバイス証明書の移行、カスタムエンドポイント設定、既存トピック構造の維持"
        ]
    },
    658: {
        "perspective": "EC2インスタンスへのSSHキーを定期的にローテーションして、古いキーでのアクセスを無効化するには何が最適か？",
        "tips": [
            "「SSHキーの自動ローテーション」→ Secrets Manager（SSHキーペアを保管、ローテーションLambdaで自動更新）",
            "「EC2 Instance Connect」→ 一時的なSSHキーを発行（ローテーション管理不要）",
            "「Systems Manager Session Manager」→ SSHキー不要でEC2にアクセス（最もセキュア・キー管理不要）"
        ]
    },
    659: {
        "perspective": "VMware vSphereで動くオンプレミスサーバーのインベントリをエージェントなしで収集してAWS移行計画を立てるには？",
        "tips": [
            "「VMware環境のエージェントレス収集」→ Migration Evaluator エージェントレスコレクター（vSphere API経由で収集）",
            "「ADS vs Migration Evaluator」→ ADSエージェント=OSレベル詳細収集、Migration Evaluatorエージェントレス=VMware棚卸し・TCO分析",
            "「移行計画のステップ」→ 収集（ADS/Evaluator）→ 分析（Migration Hub）→ 実行（MGN/DMS）"
        ]
    },
    660: {
        "perspective": "Lambda関数の同時実行数が急増してDB接続数上限に達するリスクを、SQSを使ってコントロールするにはどう設定するか？",
        "tips": [
            "「Lambda同時実行数の制限」→ Lambdaの予約済み同時実行数（Reserved Concurrency）を設定",
            "「SQS + Lambda + DB接続数制御」→ Lambdaの予約済み同時実行でDB接続数の上限に合わせてスロットリング",
            "「SQS バッチサイズ」→ SQSイベントソースの `BatchSize` でLambdaが一度に処理するメッセージ数を調整"
        ]
    },
    661: {
        "perspective": "オンプレで運用中のGrafanaをAWSに移行する際、高可用性・管理負担軽減を最優先にするなら何を使うか？",
        "tips": [
            "「マネージドGrafana on AWS」→ Amazon Managed Grafana（HAが自動、バージョンアップも不要）",
            "「データソース統合」→ CloudWatch, Prometheus, X-Ray等をManaged Grafanaのデータソースとして接続",
            "「Managed Grafana vs 自己管理EC2 Grafana」→ Managed=HA自動・パッチ自動、自己管理=柔軟だが運用負担大"
        ]
    },
    662: {
        "perspective": "RDS for Oracleのマスターパスワードを定期的に自動ローテーションし、アプリ側の更新も自動化するには？",
        "tips": [
            "「RDSパスワード自動ローテーション」→ Secrets Manager（RDS統合：ローテーションLambda自動生成）",
            "「ローテーション中の可用性」→ Secrets ManagerはローテーションのたびにRDS新パスワードを設定し、古いパスワードと並行して有効期間を持たせる",
            "「RDS + Secrets Manager統合」→ CreateSecretにRDS DBインスタンスARNを指定すると自動ローテーションLambdaが作成される"
        ]
    },
    663: {
        "perspective": "マルチアカウントで複数VPCを使う場合に、サブネットを各アカウントで共有することでネットワーク管理を一元化するには？",
        "tips": [
            "「VPCサブネット共有」→ VPC Sharing（RAM経由で共有VPCのサブネットを他アカウントに共有）",
            "「共有VPCの利点」→ サブネット・ルートテーブル管理を一元化、各アカウントはサブネットにリソースをデプロイするだけ",
            "「RAM（Resource Access Manager）」→ VPC, Transit Gateway, Route 53 Resolver, License Manager等を組織内共有"
        ]
    },
    664: {
        "perspective": "マルチアカウント環境でインターネット向けのエグレストラフィックを集中管理してネットワーク検査を行うには？",
        "tips": [
            "「集中エグレス + ネットワーク検査」→ Transit Gateway（スポーク→TGW→集中VPC）+ AWS Network Firewall",
            "「Network Firewall集中配置」→ 専用Inspection VPCにNetwork Firewallを配置、TGW経由で全スポークのトラフィックを通過",
            "「エグレス集中化パターン」→ Internet GatewayをInspection VPCのみに配置、他VPCはNAT GW不要"
        ]
    },
    665: {
        "perspective": "ALBとWAFのアクセスログをリアルタイムで収集してS3に長期保存するには、どのサービスの組み合わせが最適か？",
        "tips": [
            "「ALB/WAFログのリアルタイム配信」→ Kinesis Data Firehose（ストリーム→S3/Redshift/OpenSearchへ配信）",
            "「WAFログ設定」→ WAFのWebACLにFirehoseを設定してログを送信",
            "「ALBアクセスログ」→ S3に直接出力可能（Firehoseは不要）、Athenaでクエリ分析"
        ]
    },
    666: {
        "perspective": "API Gatewayのプライベートエンドポイントへのアクセスを特定VPCからのみに制限するセキュリティ設計はどれか？",
        "tips": [
            "「API Gatewayプライベートエンドポイント」→ VPCエンドポイント（インターフェース型）を作成してVPC内からアクセス",
            "「VPCエンドポイントポリシー」→ 特定API GatewayのARNのみ許可するリソースポリシーを設定",
            "「リソースポリシー + VPCエンドポイントポリシー」→ 二重制御でAPIへのアクセスをVPC限定に絞り込む"
        ]
    },
    667: {
        "perspective": "セキュリティグループのルール変更を検知して、自動的にセキュリティチームに通知する仕組みをどう実装するか？",
        "tips": [
            "「SG変更の検知・通知」→ AWS Config（SG変更ルール）→ EventBridge → SNS → メール通知",
            "「CloudTrail vs Config（SG監視）」→ CloudTrail=API呼び出し記録、Config=リソース状態変更の評価・追跡",
            "「Config自動修復」→ Config RemediationでSG変更を自動元に戻す（SSM Automationを使用）"
        ]
    },
    668: {
        "perspective": "Kinesisストリームでコンシューマーの処理が追いつかない場合、スループットを向上させる2つのアプローチはどれか？",
        "tips": [
            "「Kinesisコンシューマーのスループット向上」→ Enhanced Fan-Out（2MB/s/シャード/コンシューマー、プッシュ配信）",
            "「Kinesisシャードのスループット増加」→ リシャーディング（シャード数増加で総スループット拡大）",
            "「Enhanced Fan-Out vs 通常GetRecords」→ 通常=2MB/s共有・ポーリング、EFO=2MB/s専有・プッシュ（低レイテンシ）"
        ]
    },
    669: {
        "perspective": "組織全体の全EC2インスタンスのOSメトリクスを収集して、ライトサイジング推奨をコスト観点で一元管理するには？",
        "tips": [
            "「組織全体EC2メトリクス収集」→ CloudWatchエージェント（各インスタンスにインストール、Systems Manager配布が効率的）",
            "「コスト最適化推奨」→ AWS Cost Explorer（RI/Savings Plans推奨）またはCompute Optimizer（インスタンスサイズ推奨）",
            "「Compute Optimizer vs Cost Explorer」→ Optimizer=インスタンスタイプ・サイズの技術的推奨、Cost Explorer=コスト・割引の財務推奨"
        ]
    },
    670: {
        "perspective": "EC2インスタンスのカスタムメトリクス（例: アプリキュー長）に基づいてASGのルートテーブルを自動更新するイベント駆動の仕組みは？",
        "tips": [
            "「カスタムメトリクスベースの自動化」→ CloudWatchカスタムメトリクス → CloudWatchアラーム → EventBridge → Lambda",
            "「Lambda + EC2 API」→ Lambdaからec2:ReplaceRouteを呼び出してルートテーブルを更新",
            "「ASGイベント + ルートテーブル」→ ASGのライフサイクルフック + Lambdaで新インスタンスのルート設定を自動化"
        ]
    },
    671: {
        "perspective": "ECSサービスの新バージョンをゼロダウンタイムでデプロイし、トラフィック急増にも自動スケールできる構成はどれか？",
        "tips": [
            "「ECSゼロダウンタイムデプロイ」→ ブルー/グリーンデプロイ（CodeDeploy + ALB加重）",
            "「ECSオートスケーリング」→ Application Auto Scaling（ECSサービスのタスク数を自動調整）",
            "「ECSブルー/グリーン」→ CodeDeployがALBのトラフィックを旧タスク→新タスクに段階的に切り替え"
        ]
    },
    672: {
        "perspective": "コンテナイメージのプッシュ時に脆弱性スキャンを自動実行し、高リスクな脆弱性が検出されたら自動でデプロイを停止するには？",
        "tips": [
            "「ECR脆弱性スキャン自動化」→ ECRスキャンオンプッシュ → EventBridge（スキャン完了イベント）→ Lambda/Step Functions",
            "「脆弱性検出後の自動対応」→ Step Functions（ワークフロー）でCVSSスコア評価→高リスクならECSデプロイ停止",
            "「Inspector vs ECRスキャン」→ Inspectorは実行中EC2/コンテナの継続スキャン、ECRスキャンはイメージのビルド時スキャン"
        ]
    },
    673: {
        "perspective": "EC2だけでなくFargateやLambdaも含む組織全体の計算コストを、一括でコミットメント割引するにはどのプランが最適か？",
        "tips": [
            "「EC2+Fargate+Lambdaまとめて割引」→ Compute Savings Plans（最も柔軟、複数サービス対応）",
            "「Savings Plansの種類」→ Compute SP=EC2+Fargate+Lambda対応・最大66%割引、EC2 Instance SP=特定ファミリー限定・最大72%",
            "「Reserved Instances vs Savings Plans」→ RI=特定インスタンスタイプ固定、SP=柔軟（インスタンスタイプ・OS・リージョン変更可）"
        ]
    },
    674: {
        "perspective": "AWS コストが日次で予算超過した場合に即座にアラートを受け取り、担当者に通知する最小構成はどれか？",
        "tips": [
            "「コスト予算超過アラート」→ AWS Budgets（日次・月次予算、閾値でSNS通知）",
            "「Budgets + SNS」→ 予算アラートのアクションにSNSトピックを設定してメール/Slack通知",
            "「Cost Anomaly Detection vs Budgets」→ Anomaly Detection=異常検知（機械学習）、Budgets=固定閾値アラート"
        ]
    },
}


def main():
    print("Loading questions.json...")
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    # 対象問題を確認
    target_nums = set(NEW_EXPLANATIONS.keys())
    found = sum(1 for q in data if q.get("source") == "udemy" and q.get("num") in target_nums)
    print(f"Target questions defined: {len(target_nums)}, Found in JSON: {found}")

    updated = 0
    skipped = 0
    not_found = []

    for i, q in enumerate(data):
        if q.get("source") != "udemy":
            continue
        num = q.get("num")
        if num not in target_nums:
            continue

        expl = NEW_EXPLANATIONS[num]

        # perspective/tips のみ更新（detail は変更しない）
        data[i]["explanation"]["perspective"] = expl["perspective"]
        data[i]["explanation"]["tips"] = expl["tips"]
        updated += 1

    for num in target_nums:
        found_in_data = any(
            q.get("source") == "udemy" and q.get("num") == num
            for q in data
        )
        if not found_in_data:
            not_found.append(num)

    if not_found:
        print(f"WARNING: Not found in JSON: {sorted(not_found)}")

    print(f"Writing {DATA_PATH} ({updated} questions updated, {skipped} skipped)...")
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Done! updated={updated}")


if __name__ == "__main__":
    main()
