#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Udemy問題 num=525〜599 の perspective と tips を直接書き込むスクリプト。
"""
import json

QUESTIONS_PATH = "/Users/aki/aws-sap/docs/data/questions.json"

EXPLANATIONS = {
    525: {
        "perspective": "RDS のクロスリージョン DR で、自動バックアップとリードレプリカのどちらを選ぶか？",
        "tips": [
            "RDS の DR でダウンタイム最小化 → クロスリージョン リードレプリカを昇格（バックアップ復元より高速）",
            "「グローバルテーブル」→ RDS ではなく DynamoDB の機能。RDS に混入した選択肢は即排除",
            "リードレプリカ昇格後 → 新しいリードレプリカを再作成して DR 構成を維持"
        ]
    },
    526: {
        "perspective": "VPN + 複数 VPC の相互接続を最もシンプルに実現するには TGW か VPC ピアリングか？",
        "tips": [
            "「既存 VPN + 複数 VPC を一元管理」→ Transit Gateway でハブ＆スポーク構成",
            "VPC ピアリングは推移的ルーティング不可。3拠点以上の相互接続には TGW が必須",
            "TGW ルートテーブルにすべての IP 範囲を追加 → 一つのゲートウェイで全トラフィック制御"
        ]
    },
    527: {
        "perspective": "TLS 非対応の SMTP レガシーアプリを SES 経由に移行するには何を設定するか？",
        "tips": [
            "レガシー SMTP + TLS 必須 → STARTTLS 拡張を使って SES の SMTP インターフェースに接続",
            "SES SMTP 認証 → IAM ユーザーではなく SES 専用 SMTP 認証情報（ユーザー名/パスワード）を取得",
            "ポート 587（STARTTLS）が使えない場合 → ポート 465（SSL/TLS）または 2587 を検討"
        ]
    },
    528: {
        "perspective": "Organizations 配下の複数アカウントのコストを部門別・タグ別に可視化するベストな組み合わせは？",
        "tips": [
            "組織全体のコスト詳細分析 → AWS Cost and Usage Report（CUR）が最も詳細なソース",
            "CUR + Athena + QuickSight → S3 に出力した CUR を Athena でクエリし QuickSight で可視化する定番構成",
            "タグ＋コストカテゴリ → 部門・プロジェクト別にコストをグルーピングして比較可能にする"
        ]
    },
    529: {
        "perspective": "大量 IoT データを EC2 で直接受けるボトルネックを解消するアーキテクチャをどう選ぶか？",
        "tips": [
            "IoT 大量データの取り込みスケールアウト → Kinesis Data Streams でバッファリング・EC2 の負荷を分離",
            "読み取り負荷が高い非構造 IoT データ → RDS（リレーショナル）より DynamoDB（NoSQL）が適切",
            "「EC2 で直接受ける OLTP」→ スケール困難。Kinesis→Lambda のサーバーレスパターンで分離"
        ]
    },
    530: {
        "perspective": "グローバルユーザーのアップロード速度を改善するには S3 Transfer Acceleration か API GW エッジ最適化か？",
        "tips": [
            "S3 へのグローバルアップロード高速化 → S3 Transfer Acceleration（CloudFront エッジ経由）",
            "API Gateway のグローバル最適化 → エッジ最適化エンドポイントに変更（CloudFront 統合）",
            "Transfer Acceleration の署名付き URL → アップロード先 URL を加速エンドポイントに変更するだけで有効"
        ]
    },
    531: {
        "perspective": "アクセスパターンが不明な動画ファイルのストレージコストを自動最適化するには何を選ぶか？",
        "tips": [
            "アクセスパターン不明のオブジェクト → S3 Intelligent-Tiering で自動的に頻度に応じた階層に移動",
            "S3 ライフサイクル → アクセスパターンが予測可能な場合に有効。不明な場合は Intelligent-Tiering が優先",
            "Intelligent-Tiering → 取り出しコスト不要・ミリ秒レイテンシを維持しながら自動コスト最適化"
        ]
    },
    532: {
        "perspective": "Organizations 配下の複数 S3 バケットのコスト増加原因を分析するには何を使うか？",
        "tips": [
            "複数 S3 バケットのコスト傾向分析 → S3 Storage Lens（組織全体のストレージメトリクスを可視化）",
            "S3 Storage Lens の高度なメトリクス → ダッシュボードをアップグレードして詳細な使用状況を取得",
            "S3 コスト分析ツール比較：Storage Lens（ストレージ傾向）vs Cost Explorer（コスト集計）"
        ]
    },
    533: {
        "perspective": "マルチアカウントで IaC テンプレートを一括デプロイ・更新するには何を組み合わせるか？",
        "tips": [
            "複数アカウントへの CloudFormation 一括デプロイ → StackSets（Organizations 統合で自動展開）",
            "StackSets + Organizations → 新しいアカウント追加時も自動でスタックが展開される",
            "単一アカウントの CFn スタック vs StackSets → マルチアカウント管理には StackSets 一択"
        ]
    },
    534: {
        "perspective": "モノリスアプリを最小変更でブルーグリーンデプロイするには Elastic Beanstalk の何を使うか？",
        "tips": [
            "Elastic Beanstalk のゼロダウンタイムデプロイ → セカンダリ環境を作成して URL スワップ（ブルーグリーン）",
            "Beanstalk URL スワップ → ステージング→本番の切り替えをワンクリックで実現",
            "「CI/CD パイプラインのデプロイ先にセカンダリ環境」→ 本番に影響なくデプロイしてスワップする安全なパターン"
        ]
    },
    535: {
        "perspective": "EC2 から Aurora へのアクセスをセキュリティグループで最小権限で制御するには何を設定するか？",
        "tips": [
            "EC2→Aurora の最小権限 → EC2 SG にアウトバウンド（Aurora SG 宛）＋ Aurora SG にインバウンド（EC2 SG 宛）の2ルール",
            "セキュリティグループはステートフル → インバウンドを許可すれば戻りのアウトバウンドは自動許可",
            "CIDR ではなくセキュリティグループ ID を指定 → インスタンス IP が変わっても自動適用・最小権限を維持"
        ]
    },
    536: {
        "perspective": "事業部門別のクラウドコストを明確化・アラート通知するには Budgets と何を組み合わせるか？",
        "tips": [
            "部門別コスト追跡 → AWS Budgets にタグ・アプリケーション・環境でグループ化した予算アラートを設定",
            "コスト超過通知 → Budgets アラート → SNS → 各部門の担当者に通知",
            "月次レポート → Cost Explorer で事業部門別のコストレポートを定期的に生成"
        ]
    },
    537: {
        "perspective": "CloudFormation スタック削除時に RDS・EBS を誤削除から保護するには何を設定するか？",
        "tips": [
            "CFn スタック削除でリソース保持 → DeletionPolicy: Retain を RDS/EBS に設定",
            "DeletionPolicy の選択肢：Delete（デフォルト）/ Retain（保持）/ Snapshot（スナップショット後削除）",
            "RDS なら Snapshot も有効：スタック削除前にスナップショットを自動取得して削除"
        ]
    },
    538: {
        "perspective": "VPC フローログで特定 IP への大量送信を調査するには CloudWatch Logs Insights をどう使うか？",
        "tips": [
            "VPC フローログの分析 → CloudWatch Logs Insights で stats コマンドを使って宛先別の転送量を集計",
            "「送信元・宛先でフィルタ後に集計」→ filter + stats コマンドの組み合わせで効率的に調査",
            "NAT GW の ENI とプライベートインスタンスの ENI を含むロググループを対象に検索"
        ]
    },
    539: {
        "perspective": "既存 S3 オブジェクトを最小運用で一括暗号化するには S3 バッチ操作と何を組み合わせるか？",
        "tips": [
            "既存 S3 オブジェクトの一括暗号化 → S3 バッチ操作で「同じ場所にコピー」して SSE-S3 を適用",
            "SSE-S3 vs SSE-KMS：管理オーバーヘッド最小は SSE-S3（AWS 管理キー・追加コストなし）",
            "「バケットで暗号化有効にしても既存オブジェクトは変わらない」→ S3 バッチ操作で遡及適用が必要"
        ]
    },
    540: {
        "perspective": "サーバーレスでアドホッククエリ＋長期データをコスト最小で保管するには何を選ぶか？",
        "tips": [
            "S3 上のデータをサーバーレスでアドホッククエリ → Athena + Glue Data Catalog の定番構成",
            "長期保管コスト削減 → S3 ライフサイクルで S3 Glacier Deep Archive に自動移行",
            "Athena はクエリ実行分だけ課金 → 頻度低・データ量大のケースでコスト最小"
        ]
    },
    541: {
        "perspective": "200TB の大容量データを限られたネットワーク帯域内で期日までに AWS に転送するには？",
        "tips": [
            "大量データ（数十〜数百 TB）＋ 低帯域 → Snowball/Snowball Edge での物理転送が最速",
            "転送可否の計算：データ量（TB）÷ 帯域（Mbps）→ 日数を算出してネットワーク転送の実現性を判断",
            "Snowball Edge Storage Optimized → 80TB の使用可能容量・複数台同時に注文可能"
        ]
    },
    542: {
        "perspective": "スキャン文書から構造化データを抽出してシステム連携するには Textract と何を組み合わせるか？",
        "tips": [
            "PDF・画像からのテキスト抽出 → Amazon Textract（OCR + フォームフィールド構造化抽出）",
            "テキストの感情・エンティティ分析 → Amazon Comprehend（Textract との組み合わせが定番）",
            "Textract の特徴：単純な OCR より構造化（キーバリューペア・テーブル）の抽出が得意"
        ]
    },
    543: {
        "perspective": "オンプレ VM・メッセージキュー・バックエンドをリフト&シフトで AWS 移行するには何を選ぶか？",
        "tips": [
            "オンプレ VM からの AMI 作成移行 → AMI ベースの EC2 Auto Scaling グループで最小変更移行",
            "オンプレのメッセージキュー置き換え → Amazon MQ（ActiveMQ/RabbitMQ 互換のマネージドブローカー）",
            "既存コンテナ化されたバックエンド → EKS でオーケストレーションしてスケーラビリティを確保"
        ]
    },
    544: {
        "perspective": "S3 クライアントサイド暗号化で KMS から DEK を取得するのに必要な IAM 権限は何か？",
        "tips": [
            "クライアントサイド暗号化でデータ暗号化キー生成 → kms:GenerateDataKey が必要",
            "kms:Encrypt（既存キーで暗号化）vs kms:GenerateDataKey（新しい DEK を生成）→ クライアントサイドは GenerateDataKey",
            "S3 クライアントサイド暗号化の流れ：GenerateDataKey → DEK で S3 オブジェクトを暗号化 → 暗号化 DEK を S3 に保存"
        ]
    },
    545: {
        "perspective": "WAF ルールの誤検知を最小化しながら段階的にブロックを有効化するには何の手順が正しいか？",
        "tips": [
            "WAF ルール導入の段階的アプローチ → まず Count モードで誤検知を分析し、修正後に Block に切り替え",
            "WAF のアクション：Allow → 許可 / Count → カウントのみ（ブロックなし）/ Block → 拒否",
            "WAF ログ分析 → CloudWatch Logs や S3 に出力した WAF ログで誤検知パターンを特定"
        ]
    },
    546: {
        "perspective": "Organizations 全体のセキュリティグループに共通 CIDR を効率よく管理・配布するには何を使うか？",
        "tips": [
            "複数アカウントで共通 CIDR ルールを管理 → マネージドプレフィックスリスト + RAM で組織全体に共有",
            "RAM（Resource Access Manager）→ Organizations 内でリソース（プレフィックスリスト等）をクロスアカウント共有",
            "プレフィックスリスト更新 → 一箇所で CIDR を変更するだけで参照しているすべての SG に反映"
        ]
    },
    547: {
        "perspective": "複数 VPC にまたがるリモートアクセスを低コストで一元管理するには Client VPN をどこに配置するか？",
        "tips": [
            "複数 VPC へのリモートアクセス一元化 → 単一の Client VPN エンドポイントを作成して VPC ピアリング経由でルーティング",
            "Client VPN のコスト → エンドポイント時間課金 + 接続時間課金。エンドポイントを集約して削減",
            "「各 VPC に別々の Client VPN」→ コスト増・管理増。一つのエンドポイントでルーティングを工夫"
        ]
    },
    548: {
        "perspective": "外部 API 呼び出しの遅延がアプリに影響しないよう疎結合にするには何を使うか？",
        "tips": [
            "同期 API 呼び出しを非同期化 → SQS でメッセージをキューに入れ Lambda が非同期処理",
            "疎結合パターン：アプリは SQS に送信してすぐ応答 → Lambda がポーリングして外部 API を呼び出す",
            "SQS の特徴：メッセージを永続保存・処理失敗時は DLQ に移動・可視性タイムアウトで多重処理防止"
        ]
    },
    549: {
        "perspective": "クロスアカウントで S3 + KMS 暗号化データにアクセスするには何の権限が必要か？",
        "tips": [
            "クロスアカウント S3 アクセス → バケットポリシーで相手アカウントのロールを許可",
            "KMS 暗号化データのクロスアカウント復号 → KMS キーポリシーまたは KMS グラントで復号権限を付与",
            "QuickSight クロスアカウント：QuickSight ロールに S3 アクセス権限 + KMS 復号権限の両方が必要"
        ]
    },
    550: {
        "perspective": "MS SQL Server から RDS MySQL への異種 DB 移行で使うべきツールの組み合わせは何か？",
        "tips": [
            "異種 DB 移行（スキーマ変換） → AWS Schema Conversion Tool（SCT）でスキーマを変換",
            "データ移行 → AWS Database Migration Service（DMS）で継続レプリケーション",
            "SCT + DMS の役割分担：SCT はスキーマ変換・DMS はデータ移送。同種 DB なら DMS だけでも可"
        ]
    },
    551: {
        "perspective": "クロスアカウントで IAM ロールを引き受けて別アカウントの S3 にアクセスするには何が必要か？",
        "tips": [
            "クロスアカウントアクセスのセット：本番アカウントに IAM ロール作成 + 開発アカウントを信頼エンティティに設定",
            "開発アカウント側：sts:AssumeRole 権限を持つポリシーを IAM グループにアタッチ",
            "信頼ポリシー（誰がロールを引き受けられるか）+ 権限ポリシー（何ができるか）の2つが必要"
        ]
    },
    552: {
        "perspective": "Beanstalk のシングルインスタンスを最小変更でロードバランス・オートスケールに変更するには？",
        "tips": [
            "Beanstalk の環境タイプ変更 → シングルインスタンス → ロードバランス環境に既存環境の設定を変更",
            "Beanstalk の Auto Scaling → CPU 使用率などのメトリクスに基づくスケールアウトルールを追加",
            "新しい環境を作成するより既存環境の設定変更が運用オーバーヘッド最小"
        ]
    },
    553: {
        "perspective": "月末のスパイクに対応するため EC2 DB をマネージドサービスに移行するには何が最適か？",
        "tips": [
            "月末スパイクの読み取り負荷対策 → RDS リードレプリカを月末だけ追加してスケールアウト",
            "EC2 上の DB → RDS に移行することで自動バックアップ・フェイルオーバー・パッチ適用を自動化",
            "RDS リードレプリカ → 読み取りトラフィックを分散。プライマリの書き込み負荷は軽減しない"
        ]
    },
    554: {
        "perspective": "レガシー Java アプリを最小変更でコンテナ化して ECS Fargate に移行するには何を使うか？",
        "tips": [
            "既存アプリのコンテナ化自動変換 → AWS App2Container（EC2/オンプレ上の Java/.NET アプリを自動コンテナ化）",
            "コンテナイメージ管理 → Amazon ECR（プライベートコンテナレジストリ）に保存",
            "Fargate → インフラ管理不要のサーバーレスコンテナ。EKS との違い：Fargate はノード管理不要"
        ]
    },
    555: {
        "perspective": "サーバーレス API のリージョン障害に対してフェイルオーバーを実装するには何を組み合わせるか？",
        "tips": [
            "Lambda + API Gateway のマルチリージョン DR → 別リージョンに同構成をデプロイして Route 53 フェイルオーバールーティング",
            "Route 53 フェイルオーバー → ヘルスチェック失敗時にプライマリからセカンダリへ自動切り替え",
            "API Gateway はリージョナルサービス → 自動フェイルオーバーはなし。Route 53 でルーティング制御が必要"
        ]
    },
    556: {
        "perspective": "Organizations 内で RI/Savings Plans の共有を特定アカウントのみ無効化するには何の設定か？",
        "tips": [
            "RI/Savings Plans の共有をアカウントレベルで無効化 → 管理アカウントから Organizations の割引枠共有をオフ",
            "割引枠共有デフォルト：Organizations 内で RI・Savings Plans を全アカウントで自動共有",
            "「特定アカウントの RI を他と共有させたくない」→ 管理アカウントからそのアカウントの共有をオフ"
        ]
    },
    557: {
        "perspective": "Auto Scaling が不健全インスタンスを終了する前にログを取得するには何を一時停止するか？",
        "tips": [
            "ASG の自動終了を一時停止してトラブルシュート → Terminate プロセスを Suspend（一時停止）",
            "停止中インスタンスへのログインアクセス → Session Manager（SSM）でインターネット不要・SSH 不要",
            "ASG プロセスの一時停止対象：Terminate（終了）/ Launch（起動）/ HealthCheck（ヘルスチェック）等"
        ]
    },
    558: {
        "perspective": "Organizations 全体の WAF ルールを一元管理・自動適用するには何のサービスを使うか？",
        "tips": [
            "Organizations 全体の WAF ルール一元管理 → AWS Firewall Manager（WAF・SG・Shield の集中管理）",
            "管理するアカウント/OU リスト → Parameter Store に保存して EventBridge で変更をトリガー",
            "Firewall Manager の前提条件：Organizations の管理アカウントで有効化 + AWS Config の有効化"
        ]
    },
    559: {
        "perspective": "Lambda から Aurora への接続でパスワードを使わずセキュアに認証するには何を設定するか？",
        "tips": [
            "Lambda→Aurora のパスワードレス認証 → IAM データベース認証（IAM ロールで DB 接続可能）",
            "VPC 内から S3 へのセキュアアクセス → S3 ゲートウェイ VPC エンドポイント（インターネット経由を回避）",
            "IAM DB 認証 → Aurora/RDS に IAM トークンでログイン。ハードコードされたパスワードが不要"
        ]
    },
    560: {
        "perspective": "開発者が起動できる EC2 インスタンスタイプを制限するには IAM でどう設定するか？",
        "tips": [
            "EC2 インスタンスタイプ制限 → IAM ポリシーの Condition に ec2:InstanceType を指定して許可リストを定義",
            "IAM グループにポリシーをアタッチ → 開発者グループ全員に一括適用",
            "AWS Config ルール（desired-instance-types）→ 起動後の検出・通知に使う。IAM は起動前の予防的制御"
        ]
    },
    561: {
        "perspective": "Organizations 配下で特定タグが付いていないリソースを横断的に検出・強制するには何を使うか？",
        "tips": [
            "Organizations 全体のタグ欠落リソース検出 → Config アグリゲーター + required-tags ルールで横断チェック",
            "新規リソースへのタグ強制 → SCP（Service Control Policy）でタグなし起動を拒否",
            "Config ルール vs SCP：Config は検出（事後）/ SCP は予防（事前）。両方組み合わせが完全"
        ]
    },
    562: {
        "perspective": "Oracle DB のリアルタイムログを分析・可視化するのに最適なパイプラインは何か？",
        "tips": [
            "リアルタイムログ分析・可視化 → OpenSearch Service（Kibana 付き）がログ検索・ダッシュボードに最適",
            "ログ取り込みパイプライン → Kinesis Data Firehose でバッファリングして OpenSearch に配信",
            "DMS CDC → Oracle の変更データを継続的にキャプチャして移行・連携に使用"
        ]
    },
    563: {
        "perspective": "VPC 内の EC2 から Kinesis へのトラフィックで NAT GW コストを削減するには何を使うか？",
        "tips": [
            "VPC 内から Kinesis にアクセス → インターフェース VPC エンドポイント（NAT GW 不要・プライベート通信）",
            "VPC エンドポイントポリシー → エンドポイント経由のトラフィックをアプリケーション単位で制御",
            "NAT GW コスト削減 → インターフェース VPC エンドポイントで AWS サービスへのトラフィックをプライベート化"
        ]
    },
    564: {
        "perspective": "マルチリージョンの TGW を単一の Direct Connect で高可用性接続するにはどう設計するか？",
        "tips": [
            "複数リージョンの TGW を DX 一本で接続 → Direct Connect Gateway + トランジット VIF",
            "高可用性 → 2本の DX（DX-A と DX-B）から同じ DX Gateway にトランジット VIF を作成",
            "DX Gateway → 複数リージョンの TGW を関連付け可能。リージョン間の通信も TGW 間ピアリングで実現"
        ]
    },
    565: {
        "perspective": "IAM ユーザー作成イベントを検知してセキュリティチームに承認フローを作るには何を使うか？",
        "tips": [
            "IAM ユーザー作成イベント検知 → EventBridge ルール（CloudTrail 経由の CreateUser イベント）",
            "「AWS API Call via CloudTrail」+ eventName: CreateUser → IAM ユーザー作成の CloudTrail イベントをトリガー",
            "承認フロー → EventBridge → SNS/Lambda → セキュリティチームに通知・承認を自動化"
        ]
    },
    566: {
        "perspective": "マルチアカウントのトラフィックを一元管理しつつ AWS への移行基盤を整備するには何から始めるか？",
        "tips": [
            "マルチアカウント基盤の自動構築 → AWS Control Tower でランディングゾーンをデプロイ",
            "プライベートネットワーク一元管理 → TGW + TGW VPC アタッチメントでアカウント間の集約ルーティング",
            "Control Tower → Organizations・SSO・ガードレール（SCP）を自動設定。手動より標準化が速い"
        ]
    },
    567: {
        "perspective": "開発・テスト環境の EC2 を平日夜間に自動停止・起動してコストを削減するには何を使うか？",
        "tips": [
            "EC2 の時間ベースの自動停止・起動 → EventBridge（cron スケジュール）→ Lambda でタグ別に制御",
            "タグベースの対象指定 → 環境タグ（dev/test）を付けた EC2 を Lambda で絞り込んで停止・起動",
            "Instance Scheduler（AWS Solutions）→ 同様の機能をフルマネージドで提供する代替手段"
        ]
    },
    568: {
        "perspective": "API Gateway + Lambda で 429 Too Many Requests が発生する原因をどう特定するか？",
        "tips": [
            "API GW の 429 エラー → メソッドレベルのスロットリング上限（デフォルト 10,000 RPS/アカウント）に到達",
            "Lambda が呼び出されていない + 429 → API GW レベルでスロットリング。Lambda の同時実行数制限とは別",
            "対策 → API GW の使用量プランでクォータを増加、または API GW クォータの引き上げを申請"
        ]
    },
    569: {
        "perspective": "アプリのインバウンドトラフィックに透過的にセキュリティ検査ツールを挟み込むには何を使うか？",
        "tips": [
            "インライン型のセキュリティ検査（トラフィック透過） → Gateway Load Balancer（GWLB）で検査ツールを中継",
            "GWLB → ターゲットグループのセキュリティアプライアンスを通してから宛先に転送する透過的な構成",
            "セキュリティツール自体のスケールアウト → 新しい Auto Scaling グループで EC2 にデプロイして GWLB にアタッチ"
        ]
    },
    570: {
        "perspective": "IoT センサーデータを AWS に取り込んでリアルタイム分析・可視化するには何を組み合わせるか？",
        "tips": [
            "IoT デバイス → AWS 接続 → AWS IoT Core（デバイス管理・ルールエンジン・セキュアな MQTT 接続）",
            "IoT データの分析パイプライン → IoT Core → Lambda → S3 → Glue → Athena → QuickSight",
            "IoT Core のルールアクション → Lambda・S3・DynamoDB・Kinesis など多様なターゲットに直接ルーティング"
        ]
    },
    571: {
        "perspective": "複数のハイブリッドアカウントを単一の DX で接続するには DX Gateway と TGW をどう組み合わせるか？",
        "tips": [
            "複数 VPC + オンプレを単一 DX で接続 → DX Gateway + TGW + トランジット VIF の組み合わせ",
            "DX Gateway → 複数アカウントの TGW を一つの DX に関連付け可能（リージョンをまたいでも OK）",
            "プライベートサブネットのみ + TGW ルート → インターネット GW 不要でオンプレと AWS を安全に接続"
        ]
    },
    572: {
        "perspective": "複数顧客アカウントで EC2 購入タイプを制限するには Organizations の何を使うか？",
        "tips": [
            "複数アカウントへの EC2 購入タイプ制限 → SCP で ec2:PurchaseReservedInstancesOffering などを拒否",
            "SCP の適用 → Organizations に参加しているすべての機能が有効なアカウントに適用",
            "顧客アカウントへの制御 → SCP で On-Demand/RI 以外の購入（スポット等）を禁止してコスト管理"
        ]
    },
    573: {
        "perspective": "Aurora の高可用性をさらに強化して接続フェイルオーバー時間を短縮するには何を組み合わせるか？",
        "tips": [
            "Aurora フェイルオーバーの接続断を最小化 → RDS Proxy（接続プールで切り替え中も接続を維持）",
            "Aurora → Aurora MySQL に移行するメリット：並列クエリ・グローバルデータベース・フェイルオーバー高速化",
            "ElastiCache → 読み取りキャッシュでフェイルオーバー中の読み取り負荷を軽減"
        ]
    },
    574: {
        "perspective": "クロスアカウントアクセスで「混乱した代理人問題」を防ぐためのベストプラクティスは何か？",
        "tips": [
            "クロスアカウントアクセスの混乱した代理人対策 → IAM ロールの信頼ポリシーに外部 ID を必須条件として設定",
            "外部 ID → サードパーティ（org1）がロールを引き受ける際に提示する秘密のトークン",
            "外部 ID なしのクロスアカウントロール → 同じロール ARN を知る悪意のある第三者が不正アクセス可能"
        ]
    },
    575: {
        "perspective": "コンテナタスクにカスタムタグを割り当ててコスト追跡するには ECS のどの機能を使うか？",
        "tips": [
            "ECS タスクへのカスタムタグ付与 → タスク定義またはタスク実行時に --tags オプションでタグを指定",
            "Fargate タスクのコスト追跡 → タグに基づいてコスト配分タグを有効化して Cost Explorer で分析",
            "Fargate vs EC2 起動タイプ：Fargate はインフラ管理不要・EC2 は柔軟な制御が可能"
        ]
    },
    576: {
        "perspective": "VPC ピアリングが失敗する原因として CIDR 重複をどう確認・判断するか？",
        "tips": [
            "VPC ピアリング失敗の最多原因 → CIDR ブロックの重複（ピアリングは重複 CIDR を許可しない）",
            "サブネット CIDR が親 VPC CIDR に含まれる → 重複と判定されてピアリング不可",
            "CIDR 重複の解決策 → VPC の CIDR は変更不可。Transit Gateway + NAT 変換か VPC 再作成が必要"
        ]
    },
    577: {
        "perspective": "過剰権限の Lambda ロールを実際の使用実績に基づいて最小化するには何を使うか？",
        "tips": [
            "実際のアクセスに基づく IAM ポリシー生成 → IAM Access Analyzer が CloudTrail ログから最小権限ポリシーを自動生成",
            "CloudTrail ログを有効化 → Access Analyzer がアクティビティを分析してポリシーを提案",
            "「最小権限」実践 → Access Analyzer のポリシー生成 → レビュー → 適用の3ステップ"
        ]
    },
    578: {
        "perspective": "EC2 と EBS の適正サイズを実際のメトリクスに基づいて推奨させるには何を使うか？",
        "tips": [
            "EC2/EBS の適正サイズ（rightsizing）推奨 → AWS Compute Optimizer（CloudWatch メトリクスを分析して推奨）",
            "Compute Optimizer 有効化の前提 → CloudWatch エージェントをインストールしてメモリ使用率を取得",
            "Trusted Advisor vs Compute Optimizer：Trusted Advisor は広範な推奨 / Compute Optimizer は詳細な機械学習ベース"
        ]
    },
    579: {
        "perspective": "クロスアカウントで Secrets Manager のシークレットを共有する際 KMS キーをどう扱うか？",
        "tips": [
            "Secrets Manager のクロスアカウント共有 → カスタマーマネージドキーで暗号化 + KMS キーポリシーで他アカウントに復号権限付与",
            "AWS 管理キーではクロスアカウント共有不可 → カスタマーマネージドキーが必須",
            "アプリアカウントのロール → シークレットへの GetSecretValue + KMS の Decrypt 権限の両方が必要"
        ]
    },
    580: {
        "perspective": "Organizations 全体のリソースを特定のリージョンのみに制限するには SCP をどこに適用するか？",
        "tips": [
            "全アカウントをリージョン制限 → SCP で aws:RequestedRegion 条件を使い対象外リージョンへのアクセスを拒否",
            "SCP をルート OU に適用 → Organizations 配下のすべてのアカウント・OU に継承される",
            "グローバルサービス（IAM・Route53 等）→ リージョン制限 SCP の対象外。除外リストに追加が必要"
        ]
    },
    581: {
        "perspective": "単一リージョンの SQS+Lambda を複数リージョンに展開して並列処理するには何を使うか？",
        "tips": [
            "複数リージョンへの SQS+Lambda 展開 → 各リージョンに SQS キューと Lambda をデプロイ",
            "URL をリージョンに振り分け → SNS トピックに各リージョンの SQS キューをサブスクライブ",
            "SQS・Lambda はリージョンサービス → グローバルには展開されない。明示的に各リージョンにデプロイ必要"
        ]
    },
    582: {
        "perspective": "8時間ごとに1回だけ実行するバッチ処理を最小コスト・最小管理で実装するには何を選ぶか？",
        "tips": [
            "定時バッチ処理（8時間ごと）→ EventBridge スケジュール → Fargate タスクが最もシンプル",
            "Fargate の特徴：使用時間だけ課金・インフラ管理不要。Lambda の15分制限を超えるバッチに最適",
            "EC2（常時起動）vs Fargate（タスク実行時のみ課金）→ 短時間・定期実行ならFargate がコスト有利"
        ]
    },
    583: {
        "perspective": "グローバルゲームの S3 コンテンツとDynamoDB データをマルチリージョンに展開するには何を組み合わせるか？",
        "tips": [
            "S3 のマルチリージョン配信 → CRR（クロスリージョンレプリケーション）+ CloudFront オリジンフェイルオーバー",
            "DynamoDB のマルチリージョン → グローバルテーブル（両リージョンで読み書き可能）",
            "「新規リージョンへの低レイテンシ配信」→ S3 CRR + CloudFront の組み合わせが定番"
        ]
    },
    584: {
        "perspective": "JavaScript オブジェクトをそのまま保存する MongoDB 互換の DB を AWS マネージドで使うには？",
        "tips": [
            "MongoDB 互換のマネージド DB → Amazon DocumentDB（フルマネージド・マルチ AZ 対応）",
            "DocumentDB の特徴：JSON ドキュメント形式・MongoDB API 互換・Aurora と同様のストレージアーキテクチャ",
            "MongoDB → DocumentDB の移行：mongodump/mongorestore またはDMS で移行可能"
        ]
    },
    585: {
        "perspective": "クロスアカウントで KMS 暗号化 S3 へのアクセスを設定するには何の権限が必要か？",
        "tips": [
            "クロスアカウント S3+KMS アクセスの3セット：S3 バケットポリシー + KMS キーポリシー（またはグラント）+ IAM ロール権限",
            "viewer_access ロールに必要な権限 → S3 読み取り + KMS 復号（kms:Decrypt）の両方",
            "カスタム KMS キーのクロスアカウント → キーポリシーで他アカウントのロール ARN を Principal に追加"
        ]
    },
    586: {
        "perspective": "大量のゲノムデータを S3 に転送してバッチ分析するには DataSync と何を組み合わせるか？",
        "tips": [
            "大量ファイルのオンプレ→S3 転送 → AWS DataSync（高速・スケジュール転送・転送後に検証）",
            "バッチ分析のオーケストレーション → Step Functions + AWS Batch でコンテナジョブを制御",
            "S3 イベント → Lambda → Step Functions のトリガーパターンでデータ到着時に自動分析開始"
        ]
    },
    587: {
        "perspective": "Windows 共有ファイルシステムを複数 AZ の EC2 から共有するには何を使うか？",
        "tips": [
            "Windows の共有ファイルシステム（SMB プロトコル）→ Amazon FSx for Windows File Server",
            "複数 AZ の EC2 から共有マウント → FSx for Windows（Multi-AZ 構成）をマウントポイントとして使用",
            "FSx for Windows の特徴：Active Directory 統合・SMB 互換・DFS（分散ファイルシステム）サポート"
        ]
    },
    588: {
        "perspective": "テンプレートを使ったパーソナライズメール一括送信を最もシンプルに実装するには何を使うか？",
        "tips": [
            "テンプレートベースのパーソナライズメール送信 → SES の SendTemplatedEmail API（テンプレート + 顧客データで自動差し込み）",
            "Lambda → SES の SendTemplatedEmail → 顧客データを引数として渡してメール送信を自動化",
            "SES テンプレート → Handlebars 形式で変数を埋め込み。大量送信はバルクメール送信 API も利用可能"
        ]
    },
    589: {
        "perspective": "SQS → EC2 の処理でメッセージが DLQ に早く移動してしまう原因は maxReceiveCount のどこか？",
        "tips": [
            "SQS の DLQ 移動条件 → maxReceiveCount を超えると DLQ に移動（1回失敗 → maxReceiveCount=1 なら即 DLQ）",
            "スケールイン中のインスタンス終了 → 処理中断 → 受信カウント増加 → maxReceiveCount が低いと DLQ に移動",
            "maxReceiveCount を増やす → 一時的な処理失敗（インスタンス終了等）でも再試行できる回数が増加"
        ]
    },
    590: {
        "perspective": "VPC 内からのみアクセス可能な API GW を構築するには何のエンドポイントタイプを使うか？",
        "tips": [
            "VPC 内部専用 API → API Gateway のプライベートエンドポイント + インターフェース VPC エンドポイント",
            "リソースポリシー → VPC エンドポイントからのアクセスのみ許可（インターネットからのアクセスを拒否）",
            "リージョナル → エッジ最適化 → プライベートの3種類：プライベートは VPC 内からのみアクセス可能"
        ]
    },
    591: {
        "perspective": "日本のユーザーのコンテンツを北米ユーザーに低レイテンシで配信するには CRR と何を組み合わせるか？",
        "tips": [
            "別リージョンへの S3 コンテンツ複製 → CRR（クロスリージョンレプリケーション）で自動同期",
            "CloudFront + 複数オリジン → 地理的に近い S3 バケットをオリジンにしてレイテンシを削減",
            "Lambda@Edge → CloudFront のリクエスト時にオリジンを動的に切り替え（リージョンベースルーティング）"
        ]
    },
    592: {
        "perspective": "FSx for Windows の容量が不足したときに自動で拡張するには何を組み合わせるか？",
        "tips": [
            "FSx for Windows のストレージ容量拡張 → update-file-system コマンドで容量を増加",
            "容量監視の自動拡張 → CloudWatch メトリクス（FreeStorageCapacity）→ EventBridge → Lambda で自動拡張",
            "FSx の容量拡張はオンラインで実施可能（インスタンス停止不要）→ 一定の冷却期間（6時間）が必要"
        ]
    },
    593: {
        "perspective": "FTP でファイルを受け取って S3 に保存し Lambda でリアルタイム処理するには何を使うか？",
        "tips": [
            "FTP → S3 のマネージドブリッジ → AWS Transfer Family（FTP/SFTP/FTPS を S3/EFS に中継）",
            "S3 アップロードトリガー → S3 イベント通知 → SNS → Lambda で処理を自動化",
            "Transfer Family の利点：FTP クライアント変更不要で S3 のスケーラビリティ・耐久性を活用"
        ]
    },
    594: {
        "perspective": "ECS + Aurora の DR で RPO を最小化するにはリードレプリカとグローバルデータベースどちらが優れるか？",
        "tips": [
            "Aurora の別リージョン DR → Aurora グローバルデータベース（Aurora レプリカを別リージョンにプロビジョニング）",
            "Aurora グローバルデータベース → 通常1秒未満のレプリケーション遅延・フェイルオーバー時間 < 1分",
            "Aurora レプリカ（同一リージョン）vs グローバルデータベース（別リージョン）→ DR はグローバルデータベース"
        ]
    },
    595: {
        "perspective": "複数形式の金融データフィードを統一 JSON に変換して分析に渡すには Glue の何を使うか？",
        "tips": [
            "多様な形式のデータを分類・変換 → Glue クローラー（スキーマ自動検出）+ カスタム分類子（独自形式に対応）",
            "ETL 変換 → Glue ETL ジョブ（PySpark ベース）で変換・正規化を実施",
            "Lambda トリガー → ファイル到着 → Lambda → Glue ETL ジョブ起動のサーバーレスパターン"
        ]
    },
    596: {
        "perspective": "オンプレの MySQL をほぼリアルタイムで AWS に DR レプリケーションするには何を使うか？",
        "tips": [
            "オンプレサーバーの AWS への DR → AWS Elastic Disaster Recovery（旧 CloudEndure）+ Replication Agent",
            "Elastic Disaster Recovery → エージェントが継続的に変更をレプリケート・任意の時点にフェイルオーバー可能",
            "DMS vs Elastic DR：DMS はデータ移行向け・Elastic DR はサーバーの DR（OS・アプリ・データを丸ごと）"
        ]
    },
    597: {
        "perspective": "外部監査人に自社 AWS アカウントへの読み取りアクセスをセキュアに付与するには何を使うか？",
        "tips": [
            "クロスアカウントアクセスのベストプラクティス → IAM ロール（長期的な IAM ユーザー認証情報は使わない）",
            "外部 ID を信頼ポリシーに追加 → 混乱した代理人攻撃（confused deputy）を防御",
            "監査人のアクセス → ReadOnlyAccess ポリシーをアタッチしたロールを引き受けさせる"
        ]
    },
    598: {
        "perspective": "DynamoDB の読み取りレイテンシを改善しつつ書き込みもキャッシュに反映するには DAX をどう使うか？",
        "tips": [
            "DynamoDB の読み取り高速化 → DAX（インメモリキャッシュ）でマイクロ秒レベルのレイテンシ",
            "DAX の Write-Through → DAX を経由して書き込むことでキャッシュとDBを同時に更新（整合性維持）",
            "DAX が有効なケース：読み取り多・同じアイテムへの繰り返しアクセス。書き込み多・ strongly consistent は向かない"
        ]
    },
    599: {
        "perspective": "EC2+ALB のフロントエンドとバックエンドを最小コストで最適化するには何に移行すべきか？",
        "tips": [
            "静的コンテンツのフロントエンド → S3 静的 Web サイトホスティング（EC2+ALB のコストを削減）",
            "バーストパフォーマンスインスタンス（T3/T2）→ CPU クレジットで一時的な高負荷に対応・通常時コスト低",
            "「コア数が同じ汎用バーストパフォーマンス」→ 同等の処理能力を維持しながら通常時のコストを下げる"
        ]
    }
}


def main():
    print(f"JSONファイルを読み込み中: {QUESTIONS_PATH}")
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated = 0
    for i, q in enumerate(data):
        num = q.get('num')
        if q.get('source') != 'udemy':
            continue
        if num not in EXPLANATIONS:
            continue

        exp = EXPLANATIONS[num]
        data[i]['explanation']['perspective'] = exp['perspective']
        data[i]['explanation']['tips'] = exp['tips']
        updated += 1
        print(f"  num={num}: perspective={exp['perspective'][:50]}...")

    print(f"\n{updated}問を更新しました。ファイルに書き込み中...")
    with open(QUESTIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"完了: {QUESTIONS_PATH}")


if __name__ == "__main__":
    main()
