#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAP-300〜374（source=udemy）の explanation に perspective と tips を追加するスクリプト。
ハードコードされた辞書を使って各問題の perspective と tips を設定する。
"""

import json

JSON_PATH = "/Users/aki/aws-sap/docs/data/questions.json"
TARGET_SOURCE = "udemy"
TARGET_MIN = 300
TARGET_MAX = 374

NEW_EXPLANATIONS = {
    300: {
        "perspective": "地理的に遠いユーザーからS3へのアップロード速度を最適化するにはどのサービスを選ぶか？",
        "tips": [
            "S3への遠距離アップロードが遅いと来たら→S3 Transfer Acceleration（CloudFrontエッジ経由で最適経路転送）",
            "S3 Transfer Accelerationと来たら→マルチパートアップロードとの併用で大容量ファイルも高速転送可能",
            "CloudFront vs Transfer Accelerationと来たら→ダウンロード配信はCloudFront、アップロード高速化はTransfer Acceleration"
        ]
    },
    301: {
        "perspective": "コンテナ化されたマルチティアアプリをAWSへ移行する際、セッション管理と共有ストレージをどう設計するか？",
        "tips": [
            "コンテナ化+セッション管理と来たら→DynamoDB（外部セッションストア）でステートレス化",
            "複数コンテナ間の共有ファイルと来たら→EFS（マルチAZ対応の共有NFS）をマウント",
            "Kubernetesマネージドと来たら→EKS＋マネージドノードグループで運用負荷軽減"
        ]
    },
    302: {
        "perspective": "本番稼働中のOracleデータベースをダウンタイム最小化でRDSへ移行するにはどのツールを使うか？",
        "tips": [
            "Oracleからの移行+ダウンタイム最小化と来たら→Oracle GoldenGate（双方向レプリケーション）",
            "Oracle Data Pumpと来たら→初期データ移行（エクスポート/インポート）に使用、継続レプリケーションはGoldenGate",
            "双方向レプリケーションと来たら→カットオーバー前に両環境を同期し、切替リスクを低減"
        ]
    },
    303: {
        "perspective": "VPC内のエンドポイントサービス利用時にクロスAZデータ転送コストを削減するにはどう設定するか？",
        "tips": [
            "NLBのクロスAZコスト削減と来たら→クロスゾーンロードバランシングをオフにしてAZ内通信を維持",
            "エンドポイントサービスのAZ固有アクセスと来たら→エンドポイントのローカルDNS名（AZ固有）を使用",
            "PrivateLinkのデータ転送コストと来たら→AZをまたぐ通信を最小化する設計が重要"
        ]
    },
    304: {
        "perspective": "オンプレミスからS3へのデータバックアップをDirect Connect経由で安全に行うにはどのサービスを使うか？",
        "tips": [
            "オンプレミス→S3バックアップ+Direct Connectと来たら→Storage Gateway ファイルゲートウェイ（NFS共有→S3）",
            "Storage Gateway ファイルゲートウェイと来たら→既存NFSアプリをそのまま利用してS3に透過的にバックアップ",
            "毎晩の定期バックアップ+大容量と来たら→NFS共有に書き込むだけでS3に自動転送（アプリ変更不要）"
        ]
    },
    305: {
        "perspective": "多数の実店舗と複数リージョンのVPCを単一のDirect Connect接続でどう接続するか？",
        "tips": [
            "Direct Connect+複数リージョンVPCと来たら→Transit VIF＋Direct Connect GW＋各リージョンのTransit Gateway",
            "Transit Gateway+マルチリージョンと来たら→Direct Connect GWを介して複数TGWに接続可能",
            "実店舗→AWS接続の集約と来たら→Direct Connect＋Transit VIFでハブアンドスポーク構成"
        ]
    },
    306: {
        "perspective": "AWS Organizations内でクロスアカウントの管理作業を最小権限で実施するにはどう構成するか？",
        "tips": [
            "クロスアカウント管理+最小権限と来たら→クロスアカウントロール＋信頼ポリシーでアクセス制御",
            "管理アカウントのIAMユーザー+メンバーアカウントと来たら→AssumeRoleで権限委任（共有クレデンシャル不要）",
            "Organizations内のメンテナンス操作と来たら→必要操作のみ許可した専用IAMロールを各アカウントに作成"
        ]
    },
    307: {
        "perspective": "大量のLinuxサーバーとNFSファイルシステムを持つ本番環境をAWSでどう災害復旧するか？",
        "tips": [
            "オンプレミスサーバー群のDRと来たら→AWS Elastic Disaster Recovery（継続的レプリケーション）",
            "NFS共有のDRと来たら→AWS DataSync＋EFS（定期同期でファイルシステムを複製）",
            "フェイルオーバー+フェイルバックと来たら→Elastic Disaster Recoveryで両方向の切り替えをサポート"
        ]
    },
    308: {
        "perspective": "HPCクラスターのネットワーク遅延とI/Oスループットを最大化するにはどの構成を選ぶか？",
        "tips": [
            "HPC+低遅延ネットワークと来たら→EFA（Elastic Fabric Adapter）対応インスタンス＋単一AZ配置",
            "HPC+高スループットストレージと来たら→FSx for Lustre（EFSより高性能なHPC向けファイルシステム）",
            "クラスタープレイスメントグループと来たら→同一ラック内配置で最低レイテンシを実現"
        ]
    },
    309: {
        "perspective": "Organizations全体でリソース作成時のタグ付けを強制するにはSCPとタグポリシーをどう組み合わせるか？",
        "tips": [
            "タグなしリソースの作成拒否と来たら→SCP（サービスコントロールポリシー）で未タグリソース作成をDeny",
            "タグ値の標準化と来たら→タグポリシー（許可値リストをOUにアタッチ）",
            "SCP vs タグポリシーと来たら→SCPは作成拒否の強制、タグポリシーは値の標準化（両方併用が強力）"
        ]
    },
    310: {
        "perspective": "大量のIoTセンサーからのMQTTデータをリアルタイム処理してS3やLambdaに連携するにはどう構成するか？",
        "tips": [
            "IoTデバイス+MQTTと来たら→AWS IoT Core（マネージドMQTTブローカー）",
            "IoT Core+ストリーミング処理と来たら→Kinesis Data Firehose（→S3）またはKinesis Data Streams（→Lambda）",
            "IoTデータ+Lambda処理と来たら→IoT Core ルール→Lambda（リアルタイムフィルタリング・変換）"
        ]
    },
    311: {
        "perspective": "複数サービス（EC2/EFS/RDS等）のバックアップを一元管理し、規制要件に準拠するにはどうするか？",
        "tips": [
            "複数AWSサービスの統合バックアップと来たら→AWS Backup（一元的なバックアッププラン管理）",
            "バックアップのクロスリージョンコピーと来たら→AWS Backup プランでコピー先リージョンを設定",
            "バックアップ失敗の自動通知と来たら→EventBridge→SNS（BACKUP_JOB_COMPLETED以外のステータスを通知）"
        ]
    },
    312: {
        "perspective": "大量のセンサーデータをリアルタイム収集・分析してデータウェアハウスに格納するにはどのサービスを選ぶか？",
        "tips": [
            "ストリーミングデータ+リアルタイム分析と来たら→Kinesis Data Streams（リアルタイム）またはFirehose（バッファ型）",
            "大規模データ分析+Redshiftと来たら→EMR（MapReduce）またはKinesis Data Analytics",
            "センサーデータ+継続分析と来たら→Kinesis Data Streams→EMR→Redshift（リアルタイム→バッチ→DWH）"
        ]
    },
    313: {
        "perspective": "グローバルなeコマースプラットフォームで高可用性・DR・コスト最適化を同時に実現する構成は何か？",
        "tips": [
            "グローバルNoSQL+マルチリージョンと来たら→DynamoDB グローバルテーブル（Active-Active）",
            "Route 53 フェイルオーバー+低TTLと来たら→TTL 20秒で素早いDNSフェイルオーバー（RTO短縮）",
            "Auto Scaling+コスト最適化と来たら→最小台数はリザーブドインスタンス、追加スケールはオンデマンド"
        ]
    },
    314: {
        "perspective": "IoT車両データをMQTTで受信しリアルタイム異常検知とS3アーカイブを両立するにはどう構成するか？",
        "tips": [
            "IoT+MQTT+リアルタイム異常検知と来たら→IoT Core→Kinesis Data Firehose→S3＋Kinesis Data Analytics",
            "Kinesis Data Analyticsと来たら→ストリーミングデータのSQL分析・異常検知（機械学習オプションあり）",
            "IoTデータのアーカイブ+分析と来たら→Firehose→S3（永続化）＋Analytics（リアルタイム処理）の組み合わせ"
        ]
    },
    315: {
        "perspective": "CodeCommitにコミットされたIAMキーを自動検出・無効化・通知するにはどのアーキテクチャを使うか？",
        "tips": [
            "コードに含まれた機密情報の自動検出と来たら→CodeCommitトリガー→Lambda（スキャン＋IAM無効化）",
            "アクセスキーの漏洩対応と来たら→IAM APIでキー無効化→SNS通知（即時対応の自動化）",
            "CodeCommitイベント→自動修復と来たら→Lambdaトリガー（プッシュごとに実行、リアルタイム対応）"
        ]
    },
    316: {
        "perspective": "複数アカウントの多数のVPCが中央S3バケットにプライベートかつアクセス制御された状態でアクセスするにはどうするか？",
        "tips": [
            "VPCからS3プライベートアクセスと来たら→S3ゲートウェイエンドポイント（インターネット不要・無料）",
            "複数アカウント+S3アクセス制御と来たら→S3アクセスポイント（VPC単位の細かなアクセス制御）",
            "S3アクセスポイント+ゲートウェイエンドポイントと来たら→エンドポイントポリシーでアクセスポイントを指定して組み合わせ"
        ]
    },
    317: {
        "perspective": "VPCフローログをリアルタイムでSplunkに転送しつつ機密情報を匿名化するにはどう構成するか？",
        "tips": [
            "VPCフローログ+Splunk転送と来たら→CloudWatch Logs→Firehose→Splunk（サブスクリプションフィルタで連携）",
            "ログの匿名化処理と来たら→Firehose+Lambda（前処理）でデータ変換・匿名化してから転送",
            "リアルタイムログ転送+変換と来たら→CloudWatch Logsサブスクリプション→Firehose（準リアルタイム）"
        ]
    },
    318: {
        "perspective": "複数アカウントのコストを財務部門が一元管理し、かつリージョン制限も実施するにはどう構成するか？",
        "tips": [
            "複数アカウントの統合コスト管理と来たら→AWS Organizations+統合請求（Cost ExplorerでアカウントごとのコストをUI表示）",
            "財務部門のクロスアカウントアクセスと来たら→管理アカウントのIAMロール+Billing権限（AssumeRoleで安全にアクセス）",
            "EU外リージョン禁止と来たら→SCPで対象OUにリージョン制限を適用"
        ]
    },
    319: {
        "perspective": "Organizations内のメンバーアカウントにコンプライアンス監査用の読み取り専用アクセスをどう安全に付与するか？",
        "tips": [
            "クロスアカウント読み取り専用アクセスと来たら→OrganizationAccountAccessRoleを使ってメンバーアカウントにIAMロール作成",
            "監査アカウントからメンバーアカウントへと来たら→信頼ポリシー（監査アカウントからAssumeRole）で安全な委任",
            "読み取り専用+マルチアカウントと来たら→各アカウントに個別IAMロール（最小権限）＋信頼関係で一元管理"
        ]
    },
    320: {
        "perspective": "数百VPCを持つ複数アカウント環境で外部サプライヤーへの接続を一元管理するにはどうするか？",
        "tips": [
            "複数VPC+アカウント間接続の集約と来たら→Transit Gateway（ハブアンドスポーク構成）",
            "Transit Gateway+複数アカウントと来たら→Resource Access Manager (RAM)でTGWを共有",
            "外部サプライヤーへのルーティング制御と来たら→TGWルートテーブル＋NACL（きめ細かなトラフィック制御）"
        ]
    },
    321: {
        "perspective": "ALBの前段でDDoS・レートベース攻撃をブロックし、異常トラフィックを監視するにはどうするか？",
        "tips": [
            "ALB+レートリミット+ブロックと来たら→AWS WAF（レートベースルール）をALBにアタッチ",
            "WAF+監視と来たら→CloudWatchメトリクス（ブロック数・リクエスト数）で異常パターン検知",
            "DDoS対策と来たら→WAF（アプリ層L7）＋Shield Standard（自動保護）の組み合わせ"
        ]
    },
    322: {
        "perspective": "顧客承認済みIPを維持したままSFTPサービスをAWSに移行し、ファイルをS3に安全保存するにはどうするか？",
        "tips": [
            "既存Elastic IPを維持したままSFTP移行と来たら→AWS Transfer Family＋BYOIP（既存IPをAWSに持ち込み）",
            "SFTP+S3保存+暗号化と来たら→Transfer Family（S3バックエンド）＋KMS暗号化",
            "顧客の既存IPホワイトリスト維持と来たら→BYOIPでElastic IPを継続利用（顧客側設定変更不要）"
        ]
    },
    323: {
        "perspective": "同一リージョン内の複数EC2インスタンス間で超低レイテンシ通信を実現するにはどう構成するか？",
        "tips": [
            "EC2インスタンス間の低レイテンシと来たら→クラスタープレイスメントグループ（同一ラック内配置）",
            "強化ネットワーキング+ジャンボフレームと来たら→ENA（Elastic Network Adapter）対応インスタンスタイプ選択",
            "HFT（高頻度取引）+低レイテンシと来たら→クラスタープレイスメント＋ENA＋ジャンボフレーム（9001バイト）"
        ]
    },
    324: {
        "perspective": "特定IPからのみアクセス可能なREST APIをリクエスト数制限付きで顧客に提供するにはどう設計するか？",
        "tips": [
            "API Gateway+IPホワイトリストと来たら→AWS WAF（IPベースルール）をAPIに関連付け",
            "API Gateway+レート制限と来たら→使用量プラン（クォータ＋スロットリング）＋APIキー",
            "顧客ごとのAPI制限と来たら→使用量プランを顧客ごとに作成してAPIキーを紐付け"
        ]
    },
    325: {
        "perspective": "Aurora MySQLのデータベース操作を監査証跡として記録・分析・可視化するにはどう構成するか？",
        "tips": [
            "Aurora監査ログ+リアルタイムと来たら→データベースアクティビティストリーム→Kinesisストリーム",
            "Kinesis→S3+暗号化と来たら→Kinesis Data Firehose（S3配信＋暗号化）",
            "データレイク+可視化と来たら→Lake Formation（データレイク構築）＋QuickSight（可視化）"
        ]
    },
    326: {
        "perspective": "高価なGPUインスタンスの需要変動に対してコストを最小化しながら適切なスケールを維持するにはどうするか？",
        "tips": [
            "GPU高コストインスタンス+コスト最適化と来たら→安価な汎用GPUインスタンス（p4d→p3）でコスト削減",
            "最小台数+スケールアップと来たら→リザーブドインスタンス（最小容量）＋オンデマンド（追加スケール）",
            "Auto Scaling+GPU高コストと来たら→希望・最小・最大容量を適切に設定してオーバープロビジョニング防止"
        ]
    },
    327: {
        "perspective": "DynamoDBの読み取りコストを削減しつつ急激なトラフィック変動にも対応するにはどう構成するか？",
        "tips": [
            "DynamoDB読み取りコスト削減と来たら→DAX（DynamoDB Accelerator）でキャッシュ（マイクロ秒レイテンシ）",
            "DynamoDBの予測可能なトラフィックと来たら→プロビジョンドキャパシティ＋Auto Scaling（オンデマンドより安価）",
            "オンデマンド→プロビジョンドへの切替と来たら→使用パターン分析後にプロビジョンド＋DAXで最適化"
        ]
    },
    328: {
        "perspective": "NLBの背後にあるEC2サービスへのインバウンドトラフィックが届かない場合のネットワーク設定を何から確認するか？",
        "tips": [
            "NLB+EC2トラフィック疎通問題と来たら→NACLでNLBサブネットCIDRからのインバウンドを許可確認",
            "EC2セキュリティグループ+NLBと来たら→NLBのプライベートIPアドレスからのインバウンドを許可",
            "NLBはプロキシなしでパケット転送と来たら→セキュリティグループにNLB自体のIPを許可（NLBはSGを持たない）"
        ]
    },
    329: {
        "perspective": "既存S3データをHIPAAコンプライアンスに準拠した暗号化と監査証跡を確保しながら移行するにはどうするか？",
        "tips": [
            "S3データの再暗号化+移行と来たら→S3バッチオペレーション（大量オブジェクトの一括コピー・変換）",
            "HIPAA+S3監査証跡と来たら→CloudTrail（APIレベルの操作ログ）＋S3サーバーアクセスログ",
            "SSE-S3 vs SSE-KMSと来たら→SSE-S3（S3管理キー・シンプル）、SSE-KMS（顧客管理キー・監査証跡強化）"
        ]
    },
    330: {
        "perspective": "S3トリガーのLambda関数でDynamoDB書き込みエラーが発生する場合のスケーリングとリトライ設計はどうするか？",
        "tips": [
            "Lambda+DynamoDB書き込み失敗と来たら→DynamoDB WCUのプロビジョンド＋Auto Scaling（スロットリング防止）",
            "Lambdaの非同期処理+リトライと来たら→SQS（バッファ）＋Step Functions（ワークフロー管理）でオーケストレーション",
            "S3→Lambda直接起動のリスクと来たら→SQSキューを挟んでバックプレッシャー制御（過負荷防止）"
        ]
    },
    331: {
        "perspective": "オンプレミスLMSをAWSに移行し、認証・静的配信・ファイル保存・自動処理を統合するにはどう設計するか？",
        "tips": [
            "静的ウェブサイト+グローバル配信と来たら→S3＋CloudFront（またはAmplify Hosting）",
            "ユーザー認証+MFAと来たら→Amazon Cognito（マネージド認証、MFA対応）",
            "ファイルアップロード時の自動処理と来たら→S3イベント→Lambda（ウイルススキャン・メタデータ抽出等）"
        ]
    },
    332: {
        "perspective": "ALB背後のEC2インスタンスのアプリケーションログを収集・分析するにはどのサービスを使うか？",
        "tips": [
            "EC2アプリログ収集と来たら→CloudWatchエージェント→CloudWatch Logs（集中ログ管理）",
            "CloudWatch Logsの分析と来たら→CloudWatch Logs Insights（クエリ言語で異常検出）",
            "ALBアクセスログ vs アプリログと来たら→ALBログはHTTPリクエスト記録、アプリログはCloudWatchエージェントで収集"
        ]
    },
    333: {
        "perspective": "S3ホスト静的サイトからAPI GatewayのAPIをJavaScriptで呼び出す際のCORSエラーをどう解消するか？",
        "tips": [
            "CORSエラー+API Gatewayと来たら→API GatewayでCORS有効化（Access-Control-Allow-Originヘッダー設定）",
            "プリフライトリクエスト（OPTIONS）と来たら→API GatewayにOPTIONSメソッドのモック統合を設定",
            "S3静的サイト→API Gateway呼び出しと来たら→CORSはAPI Gateway側の設定が必要（S3側ではない）"
        ]
    },
    334: {
        "perspective": "複数の独立したAWSアカウントをOrganizationsに統合しAD連携のSSO＋コスト一元管理を実現するにはどうするか？",
        "tips": [
            "複数アカウント統合+SSO+ADと来たら→Organizations＋IAM Identity Center（旧SSO）＋AD連携",
            "IAM Identity Center+権限設定と来たら→パーミッションセット（アカウント×グループに最小権限付与）",
            "Organizations招待と来たら→既存アカウントを組織に招待（管理アカウントから招待→各アカウントが承認）"
        ]
    },
    335: {
        "perspective": "使用頻度の低い25の内部アプリのコストを最適化しながら必要時に可用性を確保するにはどう設計するか？",
        "tips": [
            "多数の低頻度アプリ+コスト最適化と来たら→ECS on EC2（コンテナで集約、インスタンス共有）",
            "コンテナ+Auto Scalingと来たら→メモリ使用率ベースのスケーリング（低頻度アプリに適切）",
            "EC2上のECS vs Fargateと来たら→EC2（コスト重視・常時起動）、Fargate（オペレーション重視・従量課金）"
        ]
    },
    336: {
        "perspective": "S3をHDFSとして使うEMRクラスターでコアノードの安定性とコスト最適化をどう両立するか？",
        "tips": [
            "EMR+S3ストレージ+コスト最適化と来たら→プライマリ・コアはオンデマンド、タスクノードはスポット",
            "EMRタスクノード+スポットと来たら→タスクノードはHDFSデータを持たないためスポット中断の影響が少ない",
            "EMR自動終了保護と来たら→意図しないクラスター削除を防ぐ（長時間ジョブの安全性確保）"
        ]
    },
    337: {
        "perspective": "固定Elastic IPが要件のNATゲートウェイで単一障害点を排除しつつコストを最小化するにはどうするか？",
        "tips": [
            "NAT GW+Elastic IP固定+単一障害点排除と来たら→Lambda自動化（障害検知→新NATを別サブネットに作成→EIP付け替え）",
            "NAT GW障害+CloudWatch監視と来たら→カスタムメトリクス（NAT GW可用性）でアラーム設定",
            "マルチAZ NAT GW vs 単一NAT GWと来たら→マルチAZ（完全冗長・コスト高）、単一（低コスト・自動復旧）の選択"
        ]
    },
    338: {
        "perspective": "既存のOrganizationsから研究者アカウントを別の新しいOrganizationsに移行するにはどの手順を踏むか？",
        "tips": [
            "アカウントを別Organizationsに移行と来たら→既存組織からRemoveAccountFromOrganization→新組織からInviteAccountToOrganization→承認",
            "Organizations間のアカウント移動と来たら→必ずLeave（退出）してから新組織に参加（直接移行は不可）",
            "Organizations APIと来たら→RemoveAccount（既存）→Invite（新）→Accept（本人承認）の3ステップが必須"
        ]
    },
    339: {
        "perspective": "S3にアップロードされたファイルがCloudFrontのキャッシュに反映されるよう自動でキャッシュ無効化するにはどうするか？",
        "tips": [
            "S3更新→CloudFrontキャッシュ無効化と来たら→S3イベント通知→Lambda（CloudFront Invalidation API呼び出し）",
            "CloudFrontキャッシュの自動更新と来たら→S3イベント（PUT/DELETE）トリガーでLambdaを起動",
            "CloudFront Invalidation vs バージョン管理と来たら→Invalidation（即時無効化）、バージョン管理（URLに版数を含める）"
        ]
    },
    340: {
        "perspective": "Auto ScalingグループのEC2インスタンスにCodeDeployで新しいインスタンスへも自動デプロイするにはどう設定するか？",
        "tips": [
            "CodeDeploy+Auto Scalingと来たら→デプロイメントグループをAuto Scaling「グループ」に関連付け（インスタンスではなく）",
            "新しいAMI+CodeDeployと来たら→エージェントプリインストールAMIで起動テンプレートを更新",
            "Auto Scaling+CodeDeploy自動デプロイと来たら→スケールアウト時に新インスタンスへ自動でコードがデプロイされる"
        ]
    },
    341: {
        "perspective": "既存EC2インスタンスをAuto Scalingグループに組み込みつつALBとの接続を維持するにはどう移行するか？",
        "tips": [
            "既存EC2+Auto Scaling移行と来たら→Auto Scalingグループに既存インスタンスを登録（段階的移行可能）",
            "Auto Scaling+ALB連携と来たら→Auto ScalingグループをALBにアタッチ（ターゲットグループ経由）",
            "起動テンプレートとAuto Scalingと来たら→新インスタンス起動の設定を起動テンプレートで一元管理"
        ]
    },
    342: {
        "perspective": "研究者がコスト増加のリスクなく承認済みのリソース構成のみプロビジョニングできるようにするにはどうするか？",
        "tips": [
            "承認済み構成のみ利用可能にすると来たら→AWS Service Catalog（承認済みポートフォリオを共有）",
            "S3ゲートウェイエンドポイント強制と来たら→Service Catalogのポートフォリオにエンドポイント付きVPCを含む",
            "研究者のIAM権限制限と来たら→Service Catalogを通じた作成のみ許可（直接リソース作成を制限）"
        ]
    },
    343: {
        "perspective": "多数のアカウントとリージョンに展開する際にデータ主権要件（特定リージョン限定）をどう強制するか？",
        "tips": [
            "マルチアカウント+リージョン制限の一元管理と来たら→AWS Control Tower（ランディングゾーン）",
            "承認外リージョン禁止と来たら→SCP（aws:RequestedRegionで許可リージョン外をDeny）",
            "Control Tower vs Organizations直接管理と来たら→Control Towerは初期設定・ガードレール・ログが自動化されて大規模向け"
        ]
    },
    344: {
        "perspective": "モノリシックな注文管理システムをサーバーレスに刷新し、失敗した注文も確実に処理するにはどう設計するか？",
        "tips": [
            "API+サーバーレス+モバイルフレンドリーと来たら→AppSync（GraphQL・リアルタイム・WebSocket対応）",
            "非同期注文キューイング+失敗処理と来たら→SQS（バッファ）＋デッドレターキュー（DLQ）",
            "配送ロジック+オーケストレーションと来たら→Lambda＋Step Functions（複雑なワークフロー管理）"
        ]
    },
    345: {
        "perspective": "東京リージョンのAurora DBを大阪リージョンにDR用にレプリケートし秒単位のRTOを実現するにはどうするか？",
        "tips": [
            "Auroraのクロスリージョンレプリケーションと来たら→Aurora グローバルデータベース（1秒以下のレプリケーション遅延）",
            "東京→大阪のDRと来たら→Aurora グローバルDB（プライマリ:東京、セカンダリ:大阪）",
            "Aurora グローバルDB vs リードレプリカと来たら→グローバルDB（クロスリージョン・高速フェイルオーバー）、リードレプリカ（同リージョン）"
        ]
    },
    346: {
        "perspective": "特定のOrganizations子会社アカウントだけリージョン制限＋タグ付け標準化を強制するにはどうするか？",
        "tips": [
            "特定アカウントのリージョン制限と来たら→専用OUを作成してSCP（aws:RequestedRegion条件）をアタッチ",
            "組織全体のタグ標準化と来たら→ルートレベルのタグポリシー（大文字小文字・値リストの統一）",
            "SCP vs タグポリシーの対象と来たら→SCP（アクション制限）、タグポリシー（タグ値の標準化）は用途が異なる"
        ]
    },
    347: {
        "perspective": "S3の医療データへのアクセスを一部承認済みユーザーのみ許可しつつパブリックアクセスを完全遮断するにはどうするか？",
        "tips": [
            "S3完全プライベート化と来たら→パブリックアクセスブロックの全オプションをTRUE（BlockPublicAcls等4つ）",
            "承認済みロールのみアクセスと来たら→バケットポリシーで特定IAMロールのみを許可",
            "S3署名付きURL+プライベートと来たら→パブリックアクセスブロック＋バケットポリシーで保護した上で署名付きURLを生成"
        ]
    },
    348: {
        "perspective": "異なるAWSアカウント間でOracleからAurora PostgreSQLへの移行をVPCピアリング＋DMSで実施するにはどう手順を踏むか？",
        "tips": [
            "クロスアカウントDB移行+接続と来たら→VPCピアリング（異なるアカウント間のプライベート接続）",
            "Oracle→Aurora PostgreSQL移行と来たら→SCT（スキーマ変換）＋DMS（データ移行・CDC）の組み合わせ",
            "カットオーバー+ダウンタイム最小化と来たら→CDC（変更データキャプチャ）で同期後にCNAME切り替え"
        ]
    },
    349: {
        "perspective": "SQSキューで処理失敗した注文メッセージを分離・分析・通知するデッドレターキューの仕組みをどう構築するか？",
        "tips": [
            "SQS処理失敗+分離と来たら→デッドレターキュー（DLQ）に失敗メッセージを転送",
            "DLQ+自動通知と来たら→EventBridgeルール（DLQへのメッセージ到着）→Lambda（分析・通知）",
            "DLQ vs 標準キューと来たら→DLQは失敗メッセージの保管・分析専用（最大受信回数超過で自動転送）"
        ]
    },
    350: {
        "perspective": "Step Functionsワークフローの任意のステップ失敗時にチームへ通知するエラーハンドリングをどう設計するか？",
        "tips": [
            "Step Functions全ステップのエラー通知と来たら→全Task/Map/ParallelにCatch（States.ALL）を追加→通知ステートへ",
            "SNS+メール+SMSと来たら→SNSトピックに複数サブスクリプション（Email・SMS）を追加",
            "Step Functionsのエラー伝播と来たら→CatchブロックのNextで共通エラー処理ステートに集約"
        ]
    },
    351: {
        "perspective": "VPC内のEC2からDirect Connect経由でオンプレミスのプライベートDNS名を解決するにはどう設定するか？",
        "tips": [
            "VPC→オンプレミスDNS解決と来たら→Route 53 Resolver アウトバウンドエンドポイント＋転送ルール",
            "Route 53 Resolver転送ルールと来たら→特定ドメイン（factory.internal等）をオンプレミスネームサーバーに転送",
            "Direct Connect+DNS解決と来たら→VPCのDNSホスト名有効化＋Resolverエンドポイントが必須"
        ]
    },
    352: {
        "perspective": "Transit Gateway使用時に特定VPC間のみ通信を許可し、不要なVPC間通信を遮断するにはどう設計するか？",
        "tips": [
            "TGW+VPC間通信制御と来たら→VPCアタッチメントごとに専用TGWルートテーブルを作成",
            "TGWルートテーブル+ブラックホールと来たら→不要ルートをブラックホール化（通信を明示的に遮断）",
            "新VPC追加+TGW更新と来たら→関連するルートテーブルにルートを追加（最小権限の通信設計）"
        ]
    },
    353: {
        "perspective": "GPUを必要とするCADソフトをリモートワーカーにセキュアにストリーミング提供するにはどのサービスを使うか？",
        "tips": [
            "Windowsデスクトップアプリ+ブラウザストリーミングと来たら→Amazon AppStream 2.0（マネージドストリーミング）",
            "AppStream 2.0+GPU要件と来たら→グラフィックス最適化フリート（GPU搭載インスタンス）",
            "AppStream 2.0認証と来たら→IAM＋ユーザープール（SAMLフェデレーション対応）"
        ]
    },
    354: {
        "perspective": "永続的EMRクラスターで処理していたIoTデータをよりコスト効率よくクエリ可能なアーキテクチャに移行するにはどうするか？",
        "tips": [
            "EMR永続クラスター→コスト削減と来たら→S3＋Glueカタログ＋Athena（サーバーレス・クエリ課金）",
            "IoTデータ+S3ライフサイクルと来たら→古いデータをS3 Glacier Deep Archiveに自動移行（コスト削減）",
            "Hadoop→S3への移行と来たら→EMR分析をAthena（標準SQL）に移行でクラスター維持コスト不要"
        ]
    },
    355: {
        "perspective": "AWSリソースのコスト配分タグ付けを強制しタグなしリソース作成を阻止するにはどう統制するか？",
        "tips": [
            "タグなしリソース作成防止と来たら→SCP（条件キーでタグ必須化）またはConfig Rules（検出）",
            "コスト配分タグと来たら→AWSコンソールでコスト配分タグを有効化（Cost Explorerで部門別コスト分析）",
            "タグコンプライアンス監視と来たら→AWS Config（required-tags ルール）で継続的に準拠状況をチェック"
        ]
    },
    356: {
        "perspective": "複数アカウントのS3バケットへのアクセスをオンプレミスからDirect Connect経由でプライベートに実現するにはどうするか？",
        "tips": [
            "オンプレミス→S3プライベートアクセスと来たら→Direct Connect＋専用VPC＋S3インターフェイスエンドポイント",
            "複数アカウントのS3エンドポイント共有と来たら→PrivateLinkでエンドポイントを他アカウントと共有",
            "Direct Connect GW+複数アカウントと来たら→ネットワーキングアカウントに集約してDirect Connect GWで接続"
        ]
    },
    357: {
        "perspective": "タイムゾーンによって複数のピーク帯があるグローバルLMSのDynamoDB負荷をコスト効率よく管理するにはどうするか？",
        "tips": [
            "DynamoDB+予測可能なスパイクと来たら→プロビジョンドキャパシティ＋Auto Scaling（目標使用率設定）",
            "DynamoDB Auto Scaling+監視と来たら→CloudWatch（スケーリングイベント監視）で設定を継続的に最適化",
            "オンデマンド vs プロビジョンド+Auto Scalingと来たら→パターンが読める場合はプロビジョンド＋Auto Scalingがコスト優位"
        ]
    },
    358: {
        "perspective": "リアルタイムでクライアントに読者の反応をプッシュ通知するAPIをどのサービスで実現するか？",
        "tips": [
            "リアルタイムプッシュ+GraphQLと来たら→AWS AppSync（WebSocket対応・サブスクリプション機能）",
            "DynamoDB変更→クライアント配信と来たら→DynamoDB Streams→Lambda→AppSync（変更をリアルタイムにプッシュ）",
            "AppSync vs API Gatewayと来たら→AppSync（GraphQL・リアルタイムサブスクリプション向き）、API GW（REST・WebSocket手動管理）"
        ]
    },
    359: {
        "perspective": "Redshiftクラスターをパブリックサブネットでのみ作成させず承認済みプライベートサブネットに限定するSCPをどう書くか？",
        "tips": [
            "Redshiftのサブネット制限と来たら→SCP（redshift:CreateCluster拒否＋サブネットグループ名の条件キー）",
            "redshift:ClusterSubnetGroupNameと来たら→SCPの条件キーで承認済みサブネットグループ名のみ許可",
            "Organizations全体のリソース配置制限と来たら→SCPの条件キー（aws:RequestedRegion、リソース固有キー）で強制"
        ]
    },
    360: {
        "perspective": "Elastic Beanstalkのブルー/グリーンデプロイメントでURLを切り替えるにはどの操作を使うか？",
        "tips": [
            "Elastic Beanstalk+ブルー/グリーンと来たら→「Swap Environment URLs」（コンソールのクリック一発で切り替え）",
            "Elastic Beanstalk URL切り替えと来たら→CNAME Swapでトラフィックをゼロダウンタイムで移行",
            "Route 53 vs Elastic Beanstalk URL Swapと来たら→Beanstalk URL Swap（DNS切り替え）が最もシンプルなBlue/Green手法"
        ]
    },
    361: {
        "perspective": "大量の動画アップロードをSQSでバッファリングしLambdaでスケーラブルに処理してCloudFrontで配信するにはどう設計するか？",
        "tips": [
            "S3→Lambda非同期処理+スケーリングと来たら→SQS（バッファ）＋Lambdaでキュー深さに応じた自動スケール",
            "動画処理+CloudFront配信と来たら→処理済みS3バケットをCloudFrontオリジンに設定（グローバル低レイテンシ配信）",
            "S3イベント→SQS→Lambdaと来たら→SQSがバックプレッシャーを吸収（Lambda過負荷防止）"
        ]
    },
    362: {
        "perspective": "RDS for PostgreSQLからAurora PostgreSQL GlobalDatabaseに最小ダウンタイムで移行するにはどの手順を踏むか？",
        "tips": [
            "RDS→Aurora移行+ダウンタイム最小化と来たら→AuroraレプリカをRDSに作成→スタンドアロンクラスターに昇格",
            "Aurora Global Database追加と来たら→既存クラスターにセカンダリリージョンを追加してグローバルDB化",
            "Aurora PostgreSQL vs RDS PostgreSQLと来たら→Aurora（高速フェイルオーバー・グローバルDB対応）、RDS（シンプルだがグローバルDB非対応）"
        ]
    },
    363: {
        "perspective": "既存のElastic IPを維持しながらオンプレミスSFTPサーバーをAWSに移行してS3にファイル保存するにはどうするか？",
        "tips": [
            "SFTP移行+既存ElasticIP維持と来たら→Transfer Family（VPCエンドポイント）に既存Elastic IPを割り当て",
            "Transfer Family+S3と来たら→SFTPバックエンドにS3を設定（KMS暗号化、CloudTrail監査）",
            "パートナーIP制限と来たら→Transfer Familyエンドポイントにセキュリティグループ（承認済みIPのみ許可）"
        ]
    },
    364: {
        "perspective": "夜間6時間の定期的なリスク分析バッチ処理をコスト最小化しながらスケジュール管理するにはどうするか？",
        "tips": [
            "夜間バッチ+コスト最適化と来たら→AWS Batch＋Spotインスタンス（オンデマンドの最大90%割引）",
            "バッチスケジューリング+ワークフローと来たら→EventBridge（スケジュール）＋Step Functions（フロー管理）",
            "Kinesis Firehose→S3+バッチと来たら→データをS3に蓄積→夜間バッチで処理（ストリーミング+バッチの組み合わせ）"
        ]
    },
    365: {
        "perspective": "マルチAZ対応のSFTPサービスをEFS共有ストレージで構築し既存NFSシステムとも連携するにはどうするか？",
        "tips": [
            "SFTP+マルチAZ+固定ElasticIP と来たら→Transfer Family（VPCエンドポイント・各AZにElasticIP割当）",
            "Transfer Family+EFSと来たら→NFSベースのEFS（既存NFS共有システムと互換性）をバックエンドに使用",
            "既存NFSシステムとの統合と来たら→EFSをマウント（Transfer FamilyとオンプレNFSシステムがEFSを共有）"
        ]
    },
    366: {
        "perspective": "既存VPCのサブネットを拡張しながらAuto ScalingグループのEC2インスタンスの可用性を維持するにはどの手順で行うか？",
        "tips": [
            "サブネット再設計+AZ維持と来たら→一方のAZに絞ってインスタンス終了→サブネット再作成→Auto Scaling拡張を交互に実施",
            "サブネット拡張+ゼロダウンタイムと来たら→AZ単位の段階的移行（片方ずつ実施してトラフィックを維持）",
            "VPCサブネットの制約と来たら→既存サブネットのCIDR変更は不可→削除して再作成が必要"
        ]
    },
    367: {
        "perspective": "CloudFormationスタックの作成にビジネスコードタグを強制するSCPとタグポリシーをどう組み合わせるか？",
        "tips": [
            "CloudFormation作成+タグ強制と来たら→SCP（cloudformation:CreateStack拒否＋タグキー条件）",
            "タグ値の標準化と来たら→タグポリシー（承認済みビジネスコード値を定義）",
            "SCP+タグポリシーの役割分担と来たら→SCP（タグなし作成を拒否）、タグポリシー（値の標準化）を組み合わせて強制"
        ]
    },
    368: {
        "perspective": "Auto ScalingグループでCPU・メモリ要件を満たす最適インスタンスタイプをAWSに自動選択させるにはどう設定するか？",
        "tips": [
            "インスタンスタイプ未指定+属性ベース選択と来たら→属性ベースのインスタンス選択（vCPU数・メモリ量を指定）",
            "Auto Scaling+コスト最適化と来たら→複数インスタンスタイプを候補にしてAWSが最安値を自動選択",
            "特定インスタンスタイプ固定のリスクと来たら→属性ベース選択で在庫切れ・コスト上昇リスクを回避"
        ]
    },
    369: {
        "perspective": "ECS+API GatewayのグローバルマイクロサービスでDRを実現しRTOを最小化するにはどう設計するか？",
        "tips": [
            "グローバルDR+データ複製と来たら→Aurora グローバルDB＋DynamoDB グローバルテーブル（マルチリージョンActive-Active）",
            "API Gateway+マルチリージョンフェイルオーバーと来たら→リージョナルエンドポイント＋Route 53フェイルオーバールーティング",
            "RTO最小化+DR設計と来たら→データはグローバル複製、DNSフェイルオーバーで自動切り替え（RTOを秒単位に短縮）"
        ]
    },
    370: {
        "perspective": "CloudFrontでキャッシュキーを正規化してキャッシュヒット率を上げるにはどのLambda@Edgeトリガーを使うか？",
        "tips": [
            "CloudFrontキャッシュキー正規化と来たら→Lambda@Edge（ビューアリクエストトリガー）でクエリパラメータをソート・小文字化",
            "Lambda@Edgeのトリガー選択と来たら→ビューアリクエスト（キャッシュ前に正規化）がキャッシュヒット率最大化に最適",
            "クエリパラメータの大文字小文字差異と来たら→Lambda@Edgeで正規化（?A=1 と ?a=1 を同じキャッシュキーに統一）"
        ]
    },
    371: {
        "perspective": "単一リージョン運用のAurora DBを1時間RTO/RPOのDR要件に対応させるにはどのバックアップ戦略を使うか？",
        "tips": [
            "Aurora+1時間RPO+クロスリージョンと来たら→AWS Backup（1時間間隔）＋クロスリージョンコピー",
            "AWS Backup+Auroraと来たら→バックアッププランでバックアップルール（頻度・保持期間）を設定してAurora DBをリソースに割り当て",
            "Aurora グローバルDB vs AWS Backupと来たら→グローバルDB（リアルタイムレプリケーション・秒単位RPO）、Backup（1時間RPOでコスト最適）"
        ]
    },
    372: {
        "perspective": "レガシーな単一EC2インスタンス構成をAuto Scaling＋Aurora MySQLで高可用性かつ保守性を高めた構成に移行するにはどうするか？",
        "tips": [
            "単一EC2→Auto Scaling移行と来たら→SSM Agent入りAMI＋起動テンプレート＋Auto Scaling グループ＋ALB",
            "MySQL→Aurora MySQLへの移行と来たら→互換性が高くフェイルオーバーが高速（RDSより優れた可用性）",
            "SSM Agent+Auto Scalingと来たら→Systems Managerでインスタンス管理（SSHキー不要・パッチ自動化）"
        ]
    },
    373: {
        "perspective": "アプリケーション依存関係が不明な場合にMigration Hubでどうサーバーを発見・分類して移行グループを定義するか？",
        "tips": [
            "移行対象サーバーの依存関係発見と来たら→AWS Migration Hub（ネットワーク依存関係グラフ）",
            "Migration Hub+特定ポートのサーバー抽出と来たら→Athena（S3に蓄積された通信データをSQLクエリで分析）",
            "依存関係グラフ→移行グループ定義と来たら→Migration Hubで関連サーバーをグループ化して波別移行計画を作成"
        ]
    },
    374: {
        "perspective": "複数顧客に対してAPIの利用制限（クォータ）を顧客ごとに設定して管理するにはAPI Gatewayのどの機能を使うか？",
        "tips": [
            "API Gateway+顧客ごとのレート制限と来たら→使用量プラン（クォータ＋スロットリング）＋APIキーで顧客別管理",
            "使用量プランの設計と来たら→プランごとに月次クォータ・1秒あたりリクエスト数を設定→APIキーを顧客に配布",
            "Lambda直接呼び出し vs API Gateway使用量プランと来たら→API GW（認証・制限・監視を一元管理）が顧客向けSaaS APIに最適"
        ]
    }
}


def load_questions():
    with open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_questions(data):
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    print("questions.json を読み込み中...")
    data = load_questions()

    # 対象問題を確認
    targets = [
        (i, q) for i, q in enumerate(data)
        if q.get("source") == TARGET_SOURCE
        and TARGET_MIN <= q.get("num", 0) <= TARGET_MAX
    ]
    print(f"対象問題数: {len(targets)}問 (num={TARGET_MIN}〜{TARGET_MAX}, source={TARGET_SOURCE})")

    update_count = 0
    skip_count = 0
    error_count = 0

    for i, q in targets:
        num = q.get("num")
        if num not in NEW_EXPLANATIONS:
            print(f"  [SKIP] num={num}: NEW_EXPLANATIONSに定義なし")
            skip_count += 1
            continue

        exp = NEW_EXPLANATIONS[num]
        existing_perspective = q.get("explanation", {}).get("perspective", "").strip()

        if existing_perspective:
            print(f"  [SKIP] num={num}: 既にperspectiveが設定済み")
            skip_count += 1
            continue

        # perspective と tips を設定
        if "explanation" not in data[i]:
            data[i]["explanation"] = {}

        data[i]["explanation"]["perspective"] = exp["perspective"]
        data[i]["explanation"]["tips"] = exp["tips"]
        print(f"  [OK] num={num}: perspective/tips を設定")
        update_count += 1

    print(f"\nファイルを保存中...")
    save_questions(data)

    print(f"\n=== 完了 ===")
    print(f"更新: {update_count}問")
    print(f"スキップ: {skip_count}問")
    print(f"エラー: {error_count}問")


if __name__ == "__main__":
    main()
