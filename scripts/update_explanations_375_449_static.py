#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
num 375〜449 の udemy 問題の explanation に perspective と tips を追加するスクリプト
"""

import json

DATA_PATH = "/Users/aki/aws-sap/docs/data/questions.json"

NEW_DATA = {
    375: {
        "perspective": "VM 大量移行＋大容量ファイルサーバーを最短でAWSに移すには何を選ぶか？",
        "tips": [
            "VM の継続的レプリケーション→ダウンタイム最小移行 → AWS MGN（Application Migration Service）一択",
            "Windows ファイルサーバー移行 → FSx for Windows File Server ＋ DataSync の組み合わせ",
            "Snowball Edge は大容量オフライン転送向け。DX 接続があれば DataSync + DX の方が速い"
        ]
    },
    376: {
        "perspective": "CloudFront 経由でフィールドレベル暗号化を実現するには対称と非対称どちらを選ぶか？",
        "tips": [
            "CloudFront フィールドレベル暗号化 → RSA キーペアで公開鍵を CloudFront にアップロード",
            "特定マイクロサービスだけが復号 → 秘密鍵はそのサービスだけが保持",
            "KMS 対称キーは CloudFront フィールドレベル暗号化に対応していない → RSA 必須"
        ]
    },
    377: {
        "perspective": "VPC でプライベートホストゾーンとパブリックホスト名の両方を有効にする設定順序は？",
        "tips": [
            "プライベートホストゾーン使用 → Route 53 Private Hosted Zone を VPC に関連付けが必須",
            "DNS ホスト名有効化 → パブリック IP を持つインスタンスにホスト名が付与される",
            "DHCP オプションセット = AmazonProvidedDNS → VPC 組み込み DNS を使い続ける設定"
        ]
    },
    378: {
        "perspective": "RI 購入済み Redshift クラスターで突発的な読み取り需要急増を最小コストで対処するには？",
        "tips": [
            "Redshift の突発的読み取り増加 → 同時実行スケーリング（Concurrency Scaling）を有効化",
            "同時実行スケーリング → 自動スケール・24h稼働ごとに1時間無料枠あり",
            "エラスティックリサイズ/クラシックリサイズ → 所要時間が長く突発対応には不向き"
        ]
    },
    379: {
        "perspective": "S3 上の個人フォルダへのアクセス制御と監査ログを最小運用で実現するには？",
        "tips": [
            "「自分のフォルダのみアクセス」→ IAM ポリシー条件で aws:username プレフィックスを使う",
            "S3 オブジェクトレベルのアクセス監査 → CloudTrail データイベント ＋ Athena クエリ",
            "S3 サーバーアクセスログ vs CloudTrail → CloudTrail の方が詳細でリクエスターの IAM 情報が取れる"
        ]
    },
    380: {
        "perspective": "組織全体の ECR コンテナイメージアクセス制限と古いイメージ自動削除を最小構成で実現するには？",
        "tips": [
            "Organizations 内アカウントのみ許可 → aws:PrincipalOrgID 条件キーをリソースポリシーに付与",
            "ECR の古いイメージ自動削除 → ECR ライフサイクルポリシーで設定（Lambda 不要）",
            "パブリック ECR ではなくプライベート ECR → 組織外アクセスをデフォルト拒否できる"
        ]
    },
    381: {
        "perspective": "Organizations 全アカウントのRDSバックアップを一元管理・可視化するには？",
        "tips": [
            "マルチアカウントのバックアップ一元管理 → AWS Backup のクロスアカウント管理機能",
            "AWS Backup + タグベース適用 → 対象リソースへのバックアッププランを自動適用",
            "バックアップ状況の統合ビュー → AWS Backup コンソールの一元ダッシュボード"
        ]
    },
    382: {
        "perspective": "クロスアカウントの IAM ロール引き受けに必要な3つの設定要素を正しく組み合わせられるか？",
        "tips": [
            "クロスアカウントロール引き受け → ①呼び出し元の IAM ポリシー（sts:AssumeRole）②ロールの信頼ポリシー ③SCPの確認",
            "アカウントBのロール信頼ポリシー → アカウントA の Principal を明示的に許可する",
            "SCP は最上位の許可境界 → SCP が許可していなければ IAM ポリシーがあっても拒否"
        ]
    },
    383: {
        "perspective": "SMB プロトコルを維持しながら48時間RTO の DR を最低コストで実現するストレージ選択は？",
        "tips": [
            "SMB 対応 ＋ S3 バックエンド → Storage Gateway ファイルゲートウェイ",
            "48時間以内取り出し許容 → S3 Glacier Deep Archive が最安（取り出し 12〜48時間）",
            "ボリュームゲートウェイ・テープゲートウェイは SMB 非対応"
        ]
    },
    384: {
        "perspective": "EC2 固定利用・Lambda 変動利用・MemoryDB に対して最安コスト最適化の組み合わせは？",
        "tips": [
            "EC2 特定インスタンスタイプ固定利用 → EC2 インスタンス Savings Plan（最大割引率）",
            "Lambda と Fargate のコスト削減 → Compute Savings Plan（EC2・Lambda・Fargate 横断適用）",
            "MemoryDB/ElastiCache の予約 → 予約ノード購入（リザーブドインスタンスに相当）"
        ]
    },
    385: {
        "perspective": "3リージョンのグローバルゲームで自動的に最低レイテンシへルーティングし一貫性を保つには？",
        "tips": [
            "グローバルユーザーの最低レイテンシルーティング → Route 53 レイテンシーベースルーティング",
            "マルチリージョン書き込み可能DB → DynamoDB グローバルテーブル",
            "ジオロケーション vs レイテンシー → 最低遅延ならレイテンシー、地域制限ならジオロケーション"
        ]
    },
    386: {
        "perspective": "サードパーティFWアプライアンスを高可用性で集中検査させるには何のロードバランサーを使うか？",
        "tips": [
            "サードパーティ仮想アプライアンス ＋ 高可用性 → Gateway Load Balancer（GWLB）＋ GWLB エンドポイント",
            "GWLB → インライン透過検査・GENEVE プロトコルでパケットをアプライアンスに転送",
            "ALB は L7 HTTP/HTTPS 向け。FW アプライアンスにはトランスペアレントな GWLB が適切"
        ]
    },
    387: {
        "perspective": "MAC アドレス紐付きライセンスとDB静的IPの2つの制約でどう高可用性を実現するか？",
        "tips": [
            "MAC アドレス固定ライセンス → ENI プールを事前作成しライセンスを紐付け、起動時にアタッチ",
            "静的 IP の設定ファイル → Parameter Store に IP を保存してブートストラップ時に動的注入",
            "ENI は EC2 とは独立して作成・保持できる → MAC アドレスも固定される"
        ]
    },
    388: {
        "perspective": "95%が読み取りのグローバル DB で EU 拡張のレイテンシを最小コストで改善するには？",
        "tips": [
            "読み取り多い DB のリージョン拡張 → RDS クロスリージョンリードレプリカ",
            "ユーザーを最低レイテンシ API へ誘導 → Route 53 レイテンシーベースルーティング",
            "位置情報ルーティング → 地域固定。レイテンシーベース → 実際の応答時間で動的選択"
        ]
    },
    389: {
        "perspective": "1日80環境・平均45分の短命テスト環境をTGW経由でオンプレと通信させる最小運用設計は？",
        "tips": [
            "短命テスト環境を大量作成・削除 → 単一VPCに集約し CloudFormation で環境ごとにデプロイ",
            "新VPCごとにTGWアタッチメントを作ると管理爆発 → 共有VPC＋TGWが運用コスト最小",
            "Step Functions → CloudFormation の作成・削除ライフサイクル自動化に適切"
        ]
    },
    390: {
        "perspective": "マルチリージョンのアクティブ-アクティブで Secrets Manager と KMS をどう複製するか？",
        "tips": [
            "KMS キーのマルチリージョン化 → マルチリージョンキーを作成してレプリカをリージョンに展開",
            "Secrets Manager シークレットのマルチリージョン複製 → レプリケーション機能で他リージョンにコピー",
            "マルチリージョン KMS キー → 同じキー ID で複数リージョンでの暗号化・復号が可能"
        ]
    },
    391: {
        "perspective": "EHR の KVS データ・マルチリージョン書き込み・セッション管理を最適に組み合わせるには？",
        "tips": [
            "マルチリージョン書き込み低レイテンシ DB → Aurora Global Database（プライマリで書き込み・セカンダリで読み込み高速化）",
            "セッションデータのマルチリージョン共有 → DynamoDB グローバルテーブル",
            "Aurora Global Database の RPO → 約1秒、RTO → 約1分でフェイルオーバー可能"
        ]
    },
    392: {
        "perspective": "既存オンプレADを使い、インターネット経由RDPをコスト最小でセキュアに実現するには？",
        "tips": [
            "オンプレAD認証をAWSで使う → AD Connector（プロキシ型・AD を AWS 側に作らない）",
            "踏み台EC2なしのセキュアRDP → Systems Manager Fleet Manager で RDP（ポート開放不要）",
            "AWS Managed Microsoft AD vs AD Connector → AD をそのまま使うなら AD Connector がコスト低"
        ]
    },
    393: {
        "perspective": "全EBSボリュームの自動暗号化を最小運用で強制するには何を設定するか？",
        "tips": [
            "EBS 暗号化を全リージョンで自動適用 → アカウントの「EBS 暗号化のデフォルト有効化」設定",
            "この設定で以降作成される全 EBS は自動暗号化 → Lambda や Config ルールは不要",
            "既存の非暗号化ボリュームには遡及適用されない → 別途スナップショットから再作成が必要"
        ]
    },
    394: {
        "perspective": "一意認証情報での SSH ＋ CloudTrail 記録を最小運用で実現するには何を使うか？",
        "tips": [
            "接続ごとに一意の一時 SSH キー → EC2 Instance Connect（IAM 認証で都度キー発行）",
            "EC2 Instance Connect のアクセスは CloudTrail に自動記録",
            "Session Manager も CloudTrail 記録可能だが SSH ではなくセッション。SSH 要件には Instance Connect"
        ]
    },
    395: {
        "perspective": "AWS上のコンテナからオンプレDNSを参照するために最小運用でフォワーディングするには？",
        "tips": [
            "VPC → オンプレ DNS フォワーディング → Route 53 Resolver アウトバウンドエンドポイント ＋ 条件付きフォワーディングルール",
            "Route 53 Resolver → マネージドな DNS フォワーディング。EC2 DNS サーバー不要",
            "インバウンドエンドポイント → オンプレ → AWS 方向。アウトバウンド → AWS → オンプレ方向"
        ]
    },
    396: {
        "perspective": "IoT センサーデータをミリ秒以内にリアルタイム処理・即時可視化するには何を選ぶか？",
        "tips": [
            "IoT データのミリ秒リアルタイム処理 → IoT Core → Kinesis Data Streams → Lambda → OpenSearch",
            "Firehose vs Kinesis Data Streams → Firehose はバッファリングあり（最短60秒遅延）。リアルタイムは KDS",
            "OpenSearch ＋ OpenSearch Dashboard → ミリ秒検索・リアルタイムダッシュボード"
        ]
    },
    397: {
        "perspective": "プライベートサブネットから DynamoDB への接続でコスト最適なエンドポイント種別はどちらか？",
        "tips": [
            "プライベートサブネット → DynamoDB/S3 へコスト無料で接続 → ゲートウェイ VPC エンドポイント",
            "インターフェースエンドポイント（PrivateLink）は時間課金あり。ゲートウェイは無料",
            "DynamoDB ゲートウェイエンドポイント → ルートテーブルにエントリが追加されるだけ"
        ]
    },
    398: {
        "perspective": "オンプレ Cassandra を最小ダウンタイムで Amazon Keyspaces に移行するには何を使うか？",
        "tips": [
            "Cassandra → Amazon Keyspaces 移行 → AWS Glue ETL（DMS は Cassandra 非対応）",
            "AWS DMS の Cassandra ソース/Keyspaces ターゲット → 2024年現在非サポート",
            "Glue ETL で CDC 相当の変更同期を実装してカットオーバー前のデータ差分を吸収"
        ]
    },
    399: {
        "perspective": "AWS Managed AD による一元管理と MFA を最小運用で実現するには何を組み合わせるか？",
        "tips": [
            "AWS上の集中AD管理 ＋ MFA → AWS Managed Microsoft AD ＋ Amazon WorkSpaces（MFA統合）",
            "WorkSpaces は MFA に対応した仮想デスクトップ → ADの管理ツールも実行可能",
            "Simple AD は MFA・信頼関係・完全なAD機能に制限あり → 大規模企業には Managed AD"
        ]
    },
    400: {
        "perspective": "部品データ（マスタ）とセッションデータ（トランザクション）のDR設計をどう分けるか？",
        "tips": [
            "リレーショナル構造データのDR → RDS ＋ クロスリージョンリードレプリカ（RPO/RTO 調整可能）",
            "変動トランザクションデータのマルチリージョン → DynamoDB グローバルテーブル",
            "RTO 1時間・RPO 24時間 → パイロットライト相当。ホットスタンバイは不要"
        ]
    },
    401: {
        "perspective": "Control Tower でバースト可能インスタンス以外の起動を強制的に防ぐ制御方式は何か？",
        "tips": [
            "Control Tower の予防制御（Preventive Control）→ SCP を使って特定アクションを拒否",
            "検出制御（Detective Control）→ Config ルールで「検出」のみ。拒否はしない",
            "Control Tower ガードレール = 予防制御（SCP）+ 検出制御（Config）の組み合わせ"
        ]
    },
    402: {
        "perspective": "S3 バケットが空でないと CloudFormation スタック削除が失敗する問題をどう解決するか？",
        "tips": [
            "CloudFormation 削除時に S3 バケットを空にする → カスタムリソース（Lambda）でスタック削除前に実行",
            "DependsOn 属性 → リソースの作成・削除順序を制御",
            "S3 バケットの DeletionPolicy=Delete でも中にオブジェクトがあれば削除失敗"
        ]
    },
    403: {
        "perspective": "既存REST APIモデルを変更せずAPIキー管理・スケーリング・低レイテンシを実現するには？",
        "tips": [
            "REST API ＋ APIキー管理 ＋ スロットリング → Amazon API Gateway が唯一の選択肢",
            "API Gateway ＋ Lambda → サーバーレスで変動負荷に自動対応",
            "ALB は APIキー管理・スロットリング機能を持たない"
        ]
    },
    404: {
        "perspective": "オンプレ NFS から EFS への継続的レプリケーションを最小運用で設定するには？",
        "tips": [
            "オンプレ NFS → EFS への継続同期 → DataSync エージェント ＋ プライベート VIF ＋ PrivateLink",
            "DataSync のプライベート通信 → Direct Connect プライベート VIF ＋ インターフェースエンドポイント",
            "DataSync スケジュールタスク → 毎日・毎時などの定期増分転送を自動化"
        ]
    },
    405: {
        "perspective": "CloudFront 経由のみ ALB へのアクセスを許可するには何を使って制限するか？",
        "tips": [
            "CloudFront からのみ ALB アクセス許可 → CloudFront managed prefix list を SG で参照",
            "aws マネージドプレフィックスリスト → AWS が自動更新するため手動 IP 管理不要",
            "IP 範囲手動管理（ip-ranges.json）→ CloudFront IP は頻繁に変わるため管理負荷大"
        ]
    },
    406: {
        "perspective": "RTO 12時間・RPO 4時間を最小コストで満たす DR 戦略はどのパターンか？",
        "tips": [
            "RTO 12h・RPO 4h → パイロットライト戦略（最小構成をセカンダリに準備・障害時にCloudFormationで展開）",
            "RPO 4時間 → 4時間ごとのスナップショット ＋ クロスリージョンコピー",
            "ウォームスタンバイ → 常時縮小スケールで起動。パイロットライトより高コスト"
        ]
    },
    407: {
        "perspective": "マルチアカウント・コンプライアンス要件・AD FS 統合を最小運用でまとめて実現するには？",
        "tips": [
            "マルチアカウント基盤の標準化 → AWS Control Tower ＋ Organizations",
            "AD FS との SSO 統合 → IAM Identity Center（SAML フェデレーション）",
            "コンプライアンス一元管理 → AWS Config ＋ Security Hub で集中監視"
        ]
    },
    408: {
        "perspective": "EU 展開で静的コンテンツ・Aurora・ルーティングを最小コストでグローバル対応するには？",
        "tips": [
            "Aurora マルチリージョン低レイテンシ読み取り → Aurora Global Database（物理レプリケーション）",
            "静的コンテンツのグローバル配信 → S3 CRR ＋ CloudFront",
            "地理的近接性ルーティング → Route 53 Geoproximity または CloudFront でエッジ配信"
        ]
    },
    409: {
        "perspective": "常時稼働システムと中断可能な分析システムで購入モデルをどう使い分けるか？",
        "tips": [
            "24/365 固定稼働 EC2 → Savings Plan（最大72%割引）またはリザーブドインスタンス",
            "中断可能な分析バッチ → スポットインスタンス（最大90%割引）",
            "EC2 インスタンス Savings Plan → 特定インスタンスタイプ・リージョン固定で最大割引"
        ]
    },
    410: {
        "perspective": "ランサムウェアによる特権アカウント侵害でもバックアップを保護するには何を組み合わせるか？",
        "tips": [
            "バックアップの改ざん・削除防止（管理者も不可）→ AWS Backup Vault Lock コンプライアンスモード",
            "バックアップの侵害アカウントからの分離 → クロスアカウントバックアップ（専用バックアップアカウント）",
            "Organizations レベルでのバックアップ操作制限 → SCP でボールト変更を禁止"
        ]
    },
    411: {
        "perspective": "マルチアカウントのCloudWatchログをリージョン内に保持しながら中央集約・SIEM転送するには？",
        "tips": [
            "マルチアカウントログ集約 → CloudWatch Logs サブスクリプションフィルター → Kinesis Data Streams（中央アカウント）",
            "CloudWatch → Kinesis の設定 → 中央アカウントで CloudWatch Logs Destination を作成しサブスクリプション",
            "Lambda で正規化・SIEM 転送 → Kinesis からトリガーして中央アカウントで処理"
        ]
    },
    412: {
        "perspective": "750TB の VM（アプリ＋DB）を最小ダウンタイムで移行するには何を組み合わせるか？",
        "tips": [
            "VM のリフト＆シフト移行・最小ダウンタイム → AWS MGN（継続的レプリケーション）",
            "PostgreSQL → Aurora PostgreSQL の最小ダウンタイム移行 → AWS DMS（CDC モード）",
            "VM Import/Export は継続レプリケーション非対応 → カットオーバー時のダウンタイムが大きい"
        ]
    },
    413: {
        "perspective": "数百VPCとオンプレを細粒度ルーティング制御で接続しながら最小運用で統合するには？",
        "tips": [
            "大量VPC＋オンプレの集中管理 → Transit Gateway ＋ RAM で組織共有",
            "TGW のルーティング分離 → TGW ルートテーブルで VPC グループ間通信を制御",
            "推移的ピアリング → TGW で実現できる。VPC ピアリングは推移的通信不可"
        ]
    },
    414: {
        "perspective": "予測不能なスパイクを持つ取引DBとLambda/Fargateのコスト最適化をどう組み合わせるか？",
        "tips": [
            "予測不能トラフィックのDB → Aurora Serverless v2（需要に応じて自動スケール）",
            "Lambda ＋ Fargate のコスト削減 → Compute Savings Plan（両方カバー）",
            "Aurora マルチマスター → 2023年で廃止（Aurora Serverless v2 の Multi-AZ を使う）"
        ]
    },
    415: {
        "perspective": "複数コンテナで静的コンテンツを共有しながら読み取りDBボトルネックを解消するには？",
        "tips": [
            "複数コンテナ間で共有ファイルシステム → EFS（複数タスクから同時マウント可能）",
            "DBの読み取りボトルネック解消 → Aurora Serverless v2 ＋ リーダーノード追加",
            "EBS は単一EC2インスタンスにのみアタッチ可能（マルチアタッチは限定的）→ 共有には不向き"
        ]
    },
    416: {
        "perspective": "API GatewayのIAM認証・レイテンシ分析・サービスマップを同時に実現するには？",
        "tips": [
            "API Gateway の IAM 認証 → AWS_IAM 設定 ＋ execute-api:Invoke 権限 ＋ Signature V4",
            "API Gateway のトレース・レイテンシ・サービスマップ → AWS X-Ray",
            "X-Ray → 分散トレーシング・サービス依存関係マップ・レイテンシ分析が一体化"
        ]
    },
    417: {
        "perspective": "CloudFormation 変更に伴うサービス中断を最小化するCI/CDパイプライン改善は何か？",
        "tips": [
            "CloudFormation 変更の影響事前確認 → 変更セット（Change Set）で差分プレビュー",
            "ダウンタイムゼロデプロイ → CodeDeploy ブルー/グリーン ＋ 自動ロールバック",
            "変更セット → 実際に適用前にどのリソースが変更・削除されるか確認できる"
        ]
    },
    418: {
        "perspective": "アクティブ-パッシブDRでRoute 53のフェイルオーバーとALB/ASGをどう組み合わせるか？",
        "tips": [
            "アクティブ-パッシブ DR → Route 53 フェイルオーバールーティング ＋ ヘルスチェック",
            "ALB は単一リージョン内のみ。リージョン間フェイルオーバー → Route 53 で制御",
            "VPC ピアリングで ALB をまたいでルーティングはできない → 各リージョンに個別 ALB が必要"
        ]
    },
    419: {
        "perspective": "MSMQ 互換・SQL Server 維持・コンテナオーケストレーション完全制御を満たすには？",
        "tips": [
            "MSMQ の AWS 代替 → Amazon SQS（非同期メッセージキュー互換）",
            "SQL Server ライセンス維持 → Amazon RDS for SQL Server",
            "ネットワーク・ホスト完全制御のコンテナ → ECS EC2 起動タイプ（Fargate は管理層を隠蔽）"
        ]
    },
    420: {
        "perspective": "クラスタプレースメントグループの INSUFFICIENT_CAPACITY エラーを解決するには？",
        "tips": [
            "クラスタPGの容量不足エラー → グループ内の全インスタンスを停止して再起動（ハードウェア再割当て）",
            "クラスタPGは同一AZ内で物理的に近接 → ホスト側の空きがないと INSUFFICIENT CAPACITY",
            "全停止再起動でAWSが新しいホスト群を確保し直す → 空き容量が取れる可能性が高まる"
        ]
    },
    421: {
        "perspective": "ASGのパッチ後再起動で未パッチインスタンスに置き換えられる問題を防ぐには？",
        "tips": [
            "パッチ済みAMIでのASG更新 → 新AMIで起動設定を更新してインスタンスリフレッシュ",
            "Oldest Launch Configuration 終了ポリシー → 古い設定のインスタンスを先に入れ替える",
            "AMI へのパッチ適用 → 毎回インスタンスをパッチするのではなく AMI を更新してロールアウト"
        ]
    },
    422: {
        "perspective": "インターネット分離VPC内のSageMakerからPyPIへ安全にアクセスするには？",
        "tips": [
            "インターネット非接続VPCからPyPIへアクセス → CodeArtifact ＋ VPC エンドポイント",
            "CodeArtifact の外部接続 → public:pypi アップストリームを設定してパッケージを中継取得",
            "NAT GW/インスタンスはインターネット経由 → 分離要件に違反"
        ]
    },
    423: {
        "perspective": "EBSスナップショットを2リージョンに自動保存する最小運用ソリューションは何か？",
        "tips": [
            "EBS スナップショットのクロスリージョン自動コピー → Amazon DLM ポリシー",
            "DLM → スナップショット作成・保持・削除・クロスリージョンコピーを一元自動化",
            "AWS Backup でも可能だが S3 CRR は EBS スナップショットに直接は使わない"
        ]
    },
    424: {
        "perspective": "Organizations 外アカウントで特定リージョン・特定インスタンスタイプに制限するには？",
        "tips": [
            "Organizations 外アカウント → SCP は使えない → IAM ポリシーで制御",
            "IAM ポリシーの条件でインスタンスタイプとリージョンを制限 → ec2:InstanceType / aws:RequestedRegion",
            "SCP はアカウントが Organizations に所属している場合のみ適用可能"
        ]
    },
    425: {
        "perspective": "特定プレフィックスのS3レプリケーションをSLA付きで保証するには何を有効化するか？",
        "tips": [
            "S3 レプリケーションの SLA 保証（99.99% を15分以内） → S3 Replication Time Control（RTC）",
            "特定プレフィックスのみ優先レプリケーション → プレフィックスフィルター付きレプリケーションルール",
            "RTC → レプリケーション時間メトリクスも提供。EventBridge でアラート設定可能"
        ]
    },
    426: {
        "perspective": "多様な環境の大規模移行前に依存関係と組織準備状況を評価するには何を使うか？",
        "tips": [
            "オンプレ環境の依存関係・インベントリ調査 → AWS Application Discovery Service",
            "組織のクラウド移行準備状況評価 → AWS Cloud Adoption Framework（CAF）",
            "Application Discovery Service → Agentless / Agent 方式でサーバー情報を自動収集"
        ]
    },
    427: {
        "perspective": "プライベートサブネットのEC2とRDSをマルチAZ・高可用性構成に最小変更でするには？",
        "tips": [
            "NAT GW の AZ 冗長化 → 各 AZ に個別 NAT GW を配置してルートテーブルを分ける",
            "RDS の高可用性 → Multi-AZ 配置（同期レプリケーション・自動フェイルオーバー）",
            "Auto Scaling グループのマルチAZ → 最小・最大を増やして複数AZにインスタンスを分散"
        ]
    },
    428: {
        "perspective": "既存DockerコンテナをAWSに移行し共有ストレージとリアルタイムトランザクションを維持するには？",
        "tips": [
            "コンテナ間共有ストレージ → EFS（Fargate タスクからマウント可能）",
            "Fargate → インフラ管理不要でコンテナをそのまま実行",
            "EBS は Fargate では使用不可 → Fargate の共有ストレージは EFS のみ"
        ]
    },
    429: {
        "perspective": "M&A後の混在環境で移行戦略を決める前に何を使ってデータ収集と分析を行うか？",
        "tips": [
            "大規模混在環境の移行前調査 → Application Discovery Service Agent（詳細な依存関係収集）",
            "Migration Hub Strategy Recommendations → 収集データから移行戦略（7R）を自動推薦",
            "Agentless Collector は VMware 環境向け。物理/仮想混在にはエージェント方式が確実"
        ]
    },
    430: {
        "perspective": "Organizations全アカウントのCloudTrailを最小運用で中央集約し改ざん防止するには？",
        "tips": [
            "Organizations 全アカウントの CloudTrail 一元化 → 管理アカウントで組織トレイルを作成",
            "ログの改ざん防止 → S3 バージョニング ＋ MFA 削除 ＋ 暗号化",
            "組織トレイル → 全メンバーアカウントのログを自動で単一 S3 バケットに集約"
        ]
    },
    431: {
        "perspective": "インメモリ分散DBの全ノード間低レイテンシ通信を確保するプレースメントグループは何か？",
        "tips": [
            "ノード間低レイテンシ・高スループット → クラスタプレースメントグループ（同一AZ内近接配置）",
            "インメモリDB → メモリ最適化型インスタンス（Rファミリー）を選択",
            "スプレッドPG → 物理分散で可用性重視。パーティションPG → 大規模分散DB向け（耐障害性）"
        ]
    },
    432: {
        "perspective": "高セキュリティVM上の40TB+週次増分データを暗号化バックアップするには何を使うか？",
        "tips": [
            "高セキュリティ環境からの継続的暗号化転送 → DataSync エージェント（VM形式でハイパーバイザーに展開）",
            "DataSync → 初回フルコピー ＋ 以降の差分増分を自動化・フィルタリング対応",
            "Snowball は40TBくらいなら不要（DX接続や DataSync で十分）。DX があれば DataSync が最適"
        ]
    },
    433: {
        "perspective": "Redshiftへのアクセスをスタッフ役割別に厳密に制御しコンプライアンスを確保するには？",
        "tips": [
            "承認済み構成のみ展開・役割別制御 → AWS Service Catalog（ポートフォリオ・製品管理）",
            "Service Catalog → IT 管理者が事前定義した Redshift 構成のみ展開させてガバナンスを確保",
            "タグポリシーとSCPとの違い → Service Catalog は「展開できるもの」を制限"
        ]
    },
    434: {
        "perspective": "異リージョン顧客向けに既存EC2を再デプロイせずPrivateLinkでサービス提供するには？",
        "tips": [
            "別リージョンからの PrivateLink 経由アクセス → 顧客リージョンに NLB を作成し既存IPをターゲットに",
            "NLB の IP ターゲットグループ → 別リージョンの IP アドレスも登録可能",
            "PrivateLink はリージョンサービス → リージョン跨ぎには NLB を経由させてローカル PrivateLink を構成"
        ]
    },
    435: {
        "perspective": "マルチリージョンのS3暗号化状況をリアルタイムに最小運用でダッシュボード化するには？",
        "tips": [
            "S3 のマルチリージョン一元メトリクス監視 → S3 Storage Lens デフォルトダッシュボード",
            "Storage Lens → バケット数・暗号化率・ストレージ使用量等をリージョン横断で集計",
            "EventBridge + Lambda カスタム実装は可能だが運用コストが高い → Storage Lens が最小運用"
        ]
    },
    436: {
        "perspective": "脆弱性パッチを最速ゼロダウンタイムで適用し自動ロールバックできるCI/CDパターンは？",
        "tips": [
            "EC2 への最速ゼロダウンタイムパッチ → CodeDeploy ブルー/グリーンデプロイメント",
            "ブルー/グリーン → 新環境（グリーン）を検証後に切り替え。問題があれば即ロールバック",
            "インプレースデプロイ → ダウンタイムあり。脆弱性対応の緊急パッチには不向き"
        ]
    },
    437: {
        "perspective": "Organizations全アカウントでEC2にタグなしの起動を強制的に防ぐには何を使うか？",
        "tips": [
            "タグなしEC2起動を拒否 → SCP（aws:RequestTag/TagKey の Null 条件で Deny）",
            "SCP を Organizations ルートに適用 → 全アカウントに強制適用",
            "タグポリシー → 大文字小文字の統一などコンプライアンスチェック。起動拒否はできない"
        ]
    },
    438: {
        "perspective": "プライベートサブネットの EC2 に IPv6 アウトバウンド接続のみ許可するには何を使うか？",
        "tips": [
            "IPv6 アウトバウンドのみ許可（インバウンド拒否） → Egress-Only Internet Gateway",
            "NAT GW は IPv4 のみ。IPv6 に NAT は不要（全てグローバルユニキャスト）",
            "Egress-Only IGW → IPv6 専用の片方向ゲートウェイ（NAT GW の IPv6 版）"
        ]
    },
    439: {
        "perspective": "VPC内からのみプライベート API Gatewayを呼び出せるようにするには何を設定するか？",
        "tips": [
            "VPC 内からのみ API Gateway アクセス → インターフェース VPC エンドポイント（execute-api）",
            "API リソースポリシー → VPC エンドポイントからのみ許可する aws:SourceVpce 条件",
            "プライベート DNS 有効化 → VPC 内から通常の API ドメイン名でアクセス可能になる"
        ]
    },
    440: {
        "perspective": "Organizations に招待したメンバーアカウントに中央管理アカウントからアクセスするには？",
        "tips": [
            "招待したメンバーアカウントへのクロスアカウントアクセス → OrganizationAccountAccessRole を各メンバーに作成",
            "このロールを管理アカウントから AssumeRole して管理操作を実行",
            "Organizations で新規作成したアカウントは自動でこのロールが作られる。招待は手動作成が必要"
        ]
    },
    441: {
        "perspective": "ゲームサーバーの突発スケール・Kafka 移行・S3+CloudFront 配信を最適に組み合わせるには？",
        "tips": [
            "コンテナ化ゲームサーバーの自動スケール → EKS ＋ Fargate（Kubernetes の水平スケール）",
            "Kafka の AWS マネージド化 → Amazon MSK（管理不要・高スループット保証）",
            "ゲームアセット配信 → S3 ＋ CloudFront（グローバルエッジキャッシュで低レイテンシ）"
        ]
    },
    442: {
        "perspective": "リモートワーク拡大で VPN ボトルネックとWindowsファイルアクセス遅延を解消するには？",
        "tips": [
            "オンプレミス VPN の限界 → AWS Client VPN（マネージドで大規模スケーリング可能）",
            "Windows ホームディレクトリのクラウド移行 → FSx for Windows File Server（SMB・AD統合）",
            "Storage Gateway File Gateway → S3 バックエンドでオンプレ SMB 共有を提供。完全移行には FSx"
        ]
    },
    443: {
        "perspective": "マルチアカウントの暗号化されていないEBSを組織レベルで今後も防止するには？",
        "tips": [
            "マルチアカウントのEBS暗号化強制 → Control Tower ガードレール（強く推奨される制御）",
            "Control Tower 強く推奨される制御 → 暗号化非対応 EBS 作成の検出・防止を含む",
            "既存の非暗号化ボリューム → スナップショット作成→暗号化コピー→アタッチ替えで対処"
        ]
    },
    444: {
        "perspective": "既存ADでALBのweb認証をサポートするには何をIDプロバイダーとして使うか？",
        "tips": [
            "ALB での認証 → authenticate-cognito または authenticate-oidc アクションのみサポート",
            "AD を Cognito と連携 → Cognito ユーザープールを SAML IdP として AD と統合",
            "ALB の authenticate-oidc → OIDC 対応 IdP が必要。AD は直接 OIDC 非対応のため Cognito 経由"
        ]
    },
    445: {
        "perspective": "CloudFrontで単一ディストリビューションを使ってDRリージョンへ自動フェイルオーバーするには？",
        "tips": [
            "CloudFront のオリジン冗長化 → Origin Group（プライマリ＋セカンダリ）でオリジンフェイルオーバー",
            "CloudFront フェイルオーバー → DNS 伝搬なしで即座に切り替え（TTL の影響を受けない）",
            "Route 53 フェイルオーバーは DNS ベース → フェイルオーバーに数秒〜数分かかる場合あり"
        ]
    },
    446: {
        "perspective": "マルチアカウントで使用していないサービスを中央から制限しコスト管理するには？",
        "tips": [
            "組織全体のサービス制限 → SCP（拒否リスト戦略で高リスク・高コストサービスを Deny）",
            "OU 設計 → 環境・製品ライン別に OU を作り SCP を階層適用",
            "FullAWSAccess SCP ＋ 拒否 SCP の組み合わせ → 必要なサービスのみ残す拒否リスト方式"
        ]
    },
    447: {
        "perspective": "スケジュール済みの市場イベント前にスパイクを予測しDBをスケールアップするには？",
        "tips": [
            "事前にわかっているスパイク → EC2 スケジュールスケーリングポリシー（時刻指定でスケール）",
            "Aurora DB のスケールアップ → EventBridge ＋ Lambda で Aurora レプリカを大きいタイプに変更してフェイルオーバー",
            "予測スケーリング → 過去データから ML 予測（突発イベントには不向き）"
        ]
    },
    448: {
        "perspective": "Elastic Disaster Recovery でオンプレからのレプリケーションをパブリックインターネット非経由にするには？",
        "tips": [
            "パブリックインターネット非経由のDR replication → Direct Connect ＋ Elastic DR のプライベートIPオプション",
            "Elastic DR のプライベート IP 設定 → レプリケーションサーバーへのアクセスを VPC 内に限定",
            "VPC はプライベートサブネット ＋ VGW（仮想プライベートゲートウェイ）で DX 接続を受ける"
        ]
    },
    449: {
        "perspective": "S3アップロードの大量画像を非同期でリサイズしS3ライフサイクルと組み合わせるには？",
        "tips": [
            "S3 イベント → Lambda の非同期バッファリング → SQS キュー経由でLambda 呼び出し",
            "SQS → Lambda のデカップリング。突発的な大量アップロードでもキューでバッファリング",
            "S3 ライフサイクルポリシー → 1年後に Glacier Deep Archive へ自動移動"
        ]
    },
}

def main():
    print(f"対象問題数: {len(NEW_DATA)}")

    # ファイルを読み込んで差し替え
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    success_count = 0
    skip_count = 0

    for q in data:
        num = q.get("num")
        if num in NEW_DATA:
            q["explanation"]["perspective"] = NEW_DATA[num]["perspective"]
            q["explanation"]["tips"] = NEW_DATA[num]["tips"]
            success_count += 1

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"完了: 更新={success_count}問")


if __name__ == "__main__":
    main()
