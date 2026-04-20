#!/usr/bin/env python3
"""Generate per-question drawio files for remaining 12 questions."""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from drawio_helper import (
    icon, text_box, box, multitext, group_vpc, group_cloud, group_az,
    group_account, arrow, wrap,
)

OUT_DIR = '/Users/aki/aws-sap/docs/diagrams/per-question'


# =================================================================
# [456] UDEMY-157 - ECS Fargate + ECR + ALB (prod/test separation)
# =================================================================
def diag_456():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))

    body.append(icon('ecr', 80, 100, 'ECR\n(Container Image)', res_id='ecr'))
    body.append(multitext('ecrn', 50, 170, 130, 40,
        'Java マイクロサービス&#10;イメージを一元管理', size=9))

    # Test env
    body.append(box('test', 240, 90, 340, 200, 'テスト環境',
                    stroke='#3B48CC', color='#3B48CC', sw=2, fsize=12))
    body.append(icon('alb1', 280, 120, 'ALB (test)', res_id='application_load_balancer'))
    body.append(icon('ecs1', 430, 120, 'ECS Fargate\nCluster (test)', res_id='fargate'))
    body.append(multitext('testn', 280, 220, 280, 40,
        '本番と分離 → テストデプロイの影響を隔離', size=10))

    # Prod env
    body.append(box('prod', 620, 90, 340, 200, '本番環境',
                    stroke='#DD344C', color='#DD344C', sw=2, fsize=12))
    body.append(icon('alb2', 660, 120, 'ALB (prod)', res_id='application_load_balancer'))
    body.append(icon('ecs2', 810, 120, 'ECS Fargate\nCluster (prod)', res_id='fargate'))
    body.append(multitext('prodn', 660, 220, 280, 40,
        'SLA 厳守／顧客影響あり', size=10))

    body.append(arrow('a1', 130, 130, 280, 150, label='pull', dashed=True))
    body.append(arrow('a2', 130, 130, 660, 150, label='pull', dashed=True))
    body.append(arrow('a3', 330, 150, 430, 150))
    body.append(arrow('a4', 710, 150, 810, 150))

    body.append(box('cmp', 40, 320, 920, 240, '🧭 最小変更でコンテナ化サーバーレス移行',
                    stroke='#666666', color='#232F3E', fill='#FAFAFA', sw=1, fsize=12))
    body.append(multitext('cmpn', 60, 355, 900, 200,
        '✓ ECS Fargate + ECR + ALB = 既存 Java アプリの最小変更でのコンテナ化移行&#10;&#10;'
        '• Fargate = サーバーレス (EC2 不要、インフラ管理ゼロ)&#10;'
        '• ECR = コンテナレジストリ (プライベート、IAM 連携、イメージスキャン)&#10;'
        '• ALB = L7 ロードバランサー ／ ターゲットとして ECS タスクを自動登録&#10;&#10;'
        '⚠ 本番／テスト環境を別 ALB・別 ECS クラスターで物理的に分離 (推奨プラクティス)&#10;'
        '    テストデプロイによる本番への影響を完全遮断できる',
        size=11, color='#232F3E'))

    return wrap('[Q456] コンテナ化移行: ECR + ECS Fargate + ALB (prod/test分離)', '\n'.join(body))


# =================================================================
# [482] UDEMY-183 - Monolith → Lambda + API Gateway
# =================================================================
def diag_482():
    body = []

    body.append(text_box('tb', 20, 60, 960, 30,
                         'モノリシック REST API → Lambda 分割 + API Gateway',
                         size=13, bold=True))

    # Before
    body.append(box('before', 40, 100, 440, 460, '❌ 現行: EC2 フリート上のモノリシック API',
                    stroke='#DD344C', color='#DD344C', sw=2, fsize=12))
    body.append(icon('alb0', 80, 150, 'ALB', res_id='application_load_balancer'))
    body.append(icon('ec21', 220, 150, 'EC2', res_id='ec2'))
    body.append(icon('ec22', 340, 150, 'EC2', res_id='ec2'))
    body.append(multitext('bn', 60, 260, 400, 280,
        '• 使用量が大きく変動 → EC2 は常時稼働コスト&#10;'
        '• アイドル時も VM 料金発生&#10;'
        '• パッチ・スケーリング設定が必要&#10;&#10;'
        '欠点:&#10;'
        '  • オーバープロビジョニング&#10;'
        '  • モノリシックで API ごとの個別スケール不可&#10;'
        '  • 障害が全APIへ伝搬', size=10, color='#DD344C'))

    # After
    body.append(box('after', 510, 100, 470, 460, '✓ サーバーレス: API GW + Lambda',
                    stroke='#7AA116', color='#7AA116', sw=2, fsize=12))
    body.append(icon('r53', 550, 150, 'Route 53', res_id='route_53'))
    body.append(icon('apigw', 700, 150, 'API Gateway\nREST API', res_id='api_gateway'))
    body.append(icon('l1', 880, 130, 'Lambda\n/users', res_id='lambda'))
    body.append(icon('l2', 880, 220, 'Lambda\n/orders', res_id='lambda'))
    body.append(icon('l3', 880, 310, 'Lambda\n/payments', res_id='lambda'))

    body.append(arrow('a1', 600, 180, 700, 180))
    body.append(arrow('a2', 750, 180, 880, 160))
    body.append(arrow('a3', 750, 200, 880, 245))
    body.append(arrow('a4', 750, 220, 880, 335))

    body.append(multitext('an', 530, 400, 430, 140,
        '✓ 従量課金 (リクエスト数 × 実行時間)&#10;'
        '✓ API 毎に独立スケール (機能ごとに最適化)&#10;'
        '✓ パッチ・OS 管理不要 (完全マネージド)&#10;'
        '✓ デプロイは Lambda 関数単位で迅速&#10;&#10;'
        '注意: コールドスタート (Provisioned Concurrency 可)',
        size=10, color='#7AA116'))

    return wrap('[Q482] モノリス→サーバーレス: API Gateway + Lambda 分割', '\n'.join(body))


# =================================================================
# [494] UDEMY-195 - Webhook: API Gateway HTTP API + Lambda
# =================================================================
def diag_494():
    body = []

    body.append(box('src', 40, 100, 200, 200, 'オンプレミス Git サーバー',
                    stroke='#3B48CC', color='#3B48CC', sw=2, fsize=12))
    body.append(multitext('srcn', 60, 140, 160, 140,
        'Webhook 発火:&#10;• push&#10;• pull_request&#10;• issues&#10;• release&#10;&#10;HTTPS POST', size=10))

    body.append(icon('apigw', 320, 150, 'API Gateway\nHTTP API', res_id='api_gateway'))
    body.append(multitext('apin', 290, 220, 130, 60,
        'HTTP API:&#10;• 低レイテンシ&#10;• 低コスト&#10;• REST より高速', size=9, color='#E7157B'))

    body.append(icon('l1', 540, 100, 'Lambda\n/push', res_id='lambda'))
    body.append(icon('l2', 540, 200, 'Lambda\n/pr', res_id='lambda'))
    body.append(icon('l3', 540, 300, 'Lambda\n/release', res_id='lambda'))

    body.append(icon('ddb', 780, 200, 'DynamoDB\nイベント記録', res_id='dynamodb'))

    body.append(arrow('a0', 240, 180, 320, 180, label='webhook'))
    body.append(arrow('a1', 370, 180, 540, 130, dashed=True, label='route /push'))
    body.append(arrow('a2', 370, 180, 540, 230))
    body.append(arrow('a3', 370, 180, 540, 330, dashed=True))
    body.append(arrow('a4', 590, 220, 780, 225))

    body.append(box('cmp', 40, 340, 920, 230, '🧭 REST API vs HTTP API vs Lambda 直URL',
                    stroke='#666666', color='#232F3E', fill='#FAFAFA', sw=1, fsize=12))
    body.append(multitext('cmpn', 60, 375, 900, 190,
        '✓ API Gateway HTTP API: Webhook 受信に最適&#10;'
        '  • REST API より最大 70% 低コスト / 低レイテンシ&#10;'
        '  • Lambda プロキシ統合・JWT 認証をサポート&#10;'
        '  • Webhook は単純なルーティング+処理で OK → HTTP API で十分&#10;&#10;'
        '✗ REST API: 使用量プラン/API キー/SDK 生成などフル機能が不要な場合は過剰&#10;'
        '✗ Lambda Function URL: 単一関数のみ。複数 Webhook ルートには不適&#10;'
        '✗ ALB + Lambda: 常時稼働の ALB 料金発生',
        size=11, color='#232F3E'))

    return wrap('[Q494] Webhook受信: API GW HTTP API + Lambda 個別関数', '\n'.join(body))


# =================================================================
# [543] UDEMY-244 - Lift&shift: EC2 ASG + Amazon MQ + EKS
# =================================================================
def diag_543():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))

    # Onprem -> AWS
    # Web frontend: EC2 ASG + ALB
    body.append(box('web', 40, 100, 440, 200, 'Web フロントエンド (VM ベース)',
                    stroke='#FF9900', color='#FF9900', sw=2, fsize=12))
    body.append(icon('alb', 80, 140, 'ALB', res_id='application_load_balancer'))
    body.append(icon('asg', 230, 140, 'EC2 Auto Scaling\n(AMI から)', res_id='ec2'))
    body.append(multitext('webn', 60, 220, 400, 60,
        'AMI = オンプレ VM から作成 ／ 最小変更で移行 ／ Auto Scaling で弾力性',
        size=10))

    # Amazon MQ
    body.append(icon('mq', 540, 140, 'Amazon MQ\n(RabbitMQ/Active MQ)', res_id='mq'))
    body.append(multitext('mqn', 510, 220, 130, 60,
        '既存プロトコル&#10;互換維持&#10;(AMQP/STOMP/JMS)', size=9))

    # EKS backend
    body.append(box('ekb', 700, 100, 260, 200, 'バックエンド (コンテナ化)',
                    stroke='#7AA116', color='#7AA116', sw=2, fsize=12))
    body.append(icon('eks', 740, 140, 'EKS', res_id='eks'))
    body.append(icon('pod', 850, 140, 'Pods\n注文処理', res_id='fargate'))

    body.append(arrow('f1', 280, 170, 540, 170))
    body.append(arrow('f2', 590, 170, 740, 170))

    body.append(box('cmp', 40, 330, 920, 240, '🧭 選択肢の判断軸',
                    stroke='#666666', color='#232F3E', fill='#FAFAFA', sw=1, fsize=12))
    body.append(multitext('cmpn', 60, 365, 900, 200,
        'フロントエンド: 既存 Web サーバー VM → AMI 作成 → EC2 Auto Scaling + ALB (リホスト戦略)&#10;'
        '   ✓ コード変更ゼロ (Rehost = 最速・低リスク)&#10;&#10;'
        'メッセージキュー: 既存オンプレ MQ (AMQP/STOMP 等) → Amazon MQ (RabbitMQ/Active MQ)&#10;'
        '   ✓ プロトコル互換 → アプリ修正不要&#10;'
        '   ✗ SQS だと API 書き換えが必要&#10;&#10;'
        'バックエンド: 注文処理をコンテナオーケストレーションで → EKS (または ECS)&#10;'
        '   Kubernetes 資産がある or マルチクラウド志向なら EKS、AWS 特化なら ECS',
        size=11, color='#232F3E'))

    return wrap('[Q543] ハイブリッド移行: EC2 ASG + Amazon MQ + EKS', '\n'.join(body))


# =================================================================
# [554] UDEMY-255 - App2Container → ECS Fargate + ECR
# =================================================================
def diag_554():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))

    body.append(box('src', 40, 100, 180, 220, 'オンプレ Java アプリ',
                    stroke='#3B48CC', color='#3B48CC', sw=2, fsize=11))
    body.append(multitext('srcn', 60, 140, 140, 160,
        'レガシー Java&#10;オンプレミス VM&#10;最小変更で移行要', size=10, align='center'))

    # App2Container
    body.append(icon('a2c', 280, 150, 'AWS App2Container\n(自動コンテナ化)',
                     res_id='app2container'))
    body.append(multitext('a2cn', 250, 220, 140, 60,
        '自動検出・解析&#10;Dockerfile生成&#10;ECS task定義生成', size=9))

    # ECR
    body.append(icon('ecr', 480, 150, 'ECR\n(Image)', res_id='ecr'))

    # ECS
    body.append(icon('ecs', 640, 150, 'ECS Fargate', res_id='fargate'))

    # ALB
    body.append(icon('alb', 800, 150, 'ALB', res_id='application_load_balancer'))

    body.append(arrow('a1', 220, 175, 280, 175))
    body.append(arrow('a2', 330, 175, 480, 175, label='push image'))
    body.append(arrow('a3', 530, 175, 640, 175, label='pull (実行ロール)'))
    body.append(arrow('a4', 690, 175, 800, 175))

    # User from right
    body.append(box('user', 820, 340, 130, 50, 'ユーザー',
                    stroke='#3B48CC', color='#3B48CC', sw=2))
    body.append(arrow('u1', 825, 200, 825, 340))

    body.append(box('cmp', 40, 380, 920, 190, '🧭 App2Container とは?',
                    stroke='#666666', color='#232F3E', fill='#FAFAFA', sw=1, fsize=12))
    body.append(multitext('cmpn', 60, 415, 900, 150,
        'AWS App2Container (A2C) = Java/.NET アプリを自動でコンテナ化するツール&#10;&#10;'
        '1. オンプレで A2C CLI を実行 → 実行中アプリを検出&#10;'
        '2. Dockerfile と ECS/EKS 用タスク定義を自動生成&#10;'
        '3. ECR へ push → ECS/EKS にデプロイ&#10;&#10;'
        '✓ 最小変更でコンテナ化移行 (コード修正不要のケース多し)&#10;'
        '✗ 手動 Docker 化は工数が大きい',
        size=11, color='#232F3E'))

    return wrap('[Q554] レガシー移行: App2Container → ECR + ECS Fargate + ALB',
                '\n'.join(body))


# =================================================================
# [575] UDEMY-276 - ECS Fargate + Task Tags (cost allocation)
# =================================================================
def diag_575():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))

    body.append(icon('ecs', 80, 130, 'ECS Cluster\n(Fargate)', res_id='ecs'))

    # 3 tasks
    body.append(box('t1', 260, 100, 200, 100, 'タスク A (ドライバーAアプリ)',
                    stroke='#FF9900', color='#FF9900', sw=2, fsize=11))
    body.append(icon('task1', 290, 130, 'Task', res_id='fargate'))
    body.append(multitext('t1n', 350, 150, 110, 40,
        'tag: driver=A&#10;tag: route=R1', size=9))

    body.append(box('t2', 260, 220, 200, 100, 'タスク B (ドライバーBアプリ)',
                    stroke='#FF9900', color='#FF9900', sw=2, fsize=11))
    body.append(icon('task2', 290, 250, 'Task', res_id='fargate'))
    body.append(multitext('t2n', 350, 270, 110, 40,
        'tag: driver=B&#10;tag: route=R2', size=9))

    body.append(box('t3', 260, 340, 200, 100, 'タスク C (ドライバーCアプリ)',
                    stroke='#FF9900', color='#FF9900', sw=2, fsize=11))
    body.append(icon('task3', 290, 370, 'Task', res_id='fargate'))
    body.append(multitext('t3n', 350, 390, 110, 40,
        'tag: driver=C&#10;tag: route=R3', size=9))

    body.append(arrow('a1', 130, 160, 260, 150))
    body.append(arrow('a2', 130, 160, 260, 270))
    body.append(arrow('a3', 130, 160, 260, 390))

    # Cost explorer
    body.append(icon('ce', 600, 220, 'Cost Explorer\n+ コスト配分タグ',
                     res_id='cloudwatch'))
    body.append(multitext('cen', 570, 290, 130, 60,
        'タグ別コスト集計&#10;(driver / route)', size=9))

    body.append(arrow('a4', 470, 250, 600, 250))

    body.append(box('cmp', 40, 460, 920, 120, '🧭 ECS タスクへのタグ付与方法',
                    stroke='#666666', color='#232F3E', fill='#FAFAFA', sw=1, fsize=12))
    body.append(multitext('cmpn', 60, 495, 900, 85,
        'AWS CLI で aws ecs run-task --tags key=driver,value=A を指定→ タスク単位でカスタムタグ&#10;'
        'Billing コンソールで「コスト配分タグ」を有効化 → Cost Explorer で "driver" 別の費用レポート可能&#10;'
        '⚠ サービスレベルのタグ継承 (propagateTags: SERVICE) も活用可能',
        size=10, color='#232F3E'))

    return wrap('[Q575] ECS Fargate: タスクタグでコスト追跡', '\n'.join(body))


# =================================================================
# [590] UDEMY-291 - Private API Gateway endpoint transition
# =================================================================
def diag_590():
    body = []

    # Before (Regional)
    body.append(box('before', 20, 60, 470, 510, '❌ 現行: Regional エンドポイント',
                    stroke='#DD344C', color='#DD344C', sw=2, fsize=12))
    body.append(icon('int', 180, 110, 'インターネット', res_id='cloudfront'))
    body.append(icon('apigw1', 180, 230, 'API Gateway\n(Regional)', res_id='api_gateway'))
    body.append(icon('lam1', 180, 360, 'Lambda', res_id='lambda'))
    body.append(arrow('b1', 230, 165, 230, 230, color='#DD344C'))
    body.append(arrow('b2', 230, 290, 230, 360))
    body.append(multitext('bn', 40, 450, 430, 110,
        '問題:&#10;• インターネットから呼出可能 = 外部への意図せぬ公開&#10;• リソースポリシーのみでは VPC 制限が弱い&#10;• IP 制限は WAF 必須 → 複雑',
        size=10, color='#DD344C'))

    # After (Private)
    body.append(box('after', 510, 60, 470, 510, '✓ Private エンドポイント化',
                    stroke='#7AA116', color='#7AA116', sw=2, fsize=12))
    body.append(group_vpc('vpc', 540, 110, 420, 300, 'VPC'))
    body.append(icon('ec2', 580, 160, 'EC2 (内部)', res_id='ec2'))
    body.append(icon('vpce', 750, 160, 'Interface\nVPC Endpoint', res_id='api_gateway'))
    body.append(icon('apigw2', 750, 310, 'Private API', res_id='api_gateway'))
    body.append(icon('lam2', 580, 310, 'Lambda', res_id='lambda'))
    body.append(arrow('f1', 630, 185, 750, 185, label='prv'))
    body.append(arrow('f2', 775, 215, 775, 310))
    body.append(arrow('f3', 750, 335, 630, 335))

    body.append(multitext('an', 530, 450, 430, 110,
        '手順:&#10;① エンドポイントタイプ Private に変更&#10;② Interface VPC Endpoint 作成 (execute-api)&#10;③ リソースポリシー: Condition=sourceVpce で制限&#10;→ VPC 内からのみアクセス (インターネット不可)',
        size=10, color='#7AA116'))

    return wrap('[Q590] API Gateway: Regional → Private エンドポイント移行',
                '\n'.join(body))


# =================================================================
# [604] UDEMY-305 - Lambda container image via ECR
# =================================================================
def diag_604():
    body = []

    # Before
    body.append(box('before', 20, 60, 470, 510, '❌ 現行: 複数 Lambda 関数で共通ライブラリ重複',
                    stroke='#DD344C', color='#DD344C', sw=2, fsize=12))
    body.append(icon('apigw0', 180, 110, 'API Gateway', res_id='api_gateway'))
    body.append(icon('lL1', 60, 230, 'Lambda 1', res_id='lambda'))
    body.append(icon('lL2', 180, 230, 'Lambda 2', res_id='lambda'))
    body.append(icon('lL3', 300, 230, 'Lambda 3', res_id='lambda'))
    body.append(icon('lL4', 60, 360, 'Lambda 4', res_id='lambda'))
    body.append(icon('lL5', 180, 360, 'Lambda 5', res_id='lambda'))
    body.append(icon('lL6', 300, 360, 'Lambda 6', res_id='lambda'))
    body.append(multitext('bn', 40, 440, 430, 120,
        '問題:&#10;• 各関数に共通ライブラリをコピーデプロイ&#10;• Layer だと 250MB 制限 ／ 最大5レイヤー&#10;• カスタムランタイムの再利用が煩雑&#10;• デプロイパッケージが重い',
        size=10, color='#DD344C'))

    # After
    body.append(box('after', 510, 60, 470, 510, '✓ Lambda コンテナイメージ (ECR)',
                    stroke='#7AA116', color='#7AA116', sw=2, fsize=12))
    body.append(icon('docker', 680, 100, 'Docker Image\n(共有ライブラリ+&#10;カスタムランタイム+&#10;関数コード)',
                     res_id='ec2'))
    body.append(icon('ecr', 680, 240, 'ECR', res_id='ecr'))
    body.append(icon('lf', 680, 380, 'Lambda\n(Image Package)', res_id='lambda'))

    body.append(arrow('a1', 705, 155, 705, 240, label='push'))
    body.append(arrow('a2', 705, 295, 705, 380, label='deploy'))

    body.append(multitext('an', 530, 470, 430, 95,
        '✓ 10 GB までの大きなイメージをサポート&#10;'
        '✓ 共通依存を Docker レイヤーで共有&#10;'
        '✓ カスタムランタイム (OS依存のバイナリ等) も一つのイメージに&#10;'
        '✓ ECR スキャン／IAM でアクセス制御',
        size=10, color='#7AA116'))

    return wrap('[Q604] Lambda 共通ライブラリ共有: ECR コンテナイメージ',
                '\n'.join(body))


# =================================================================
# [623] UDEMY-324 - EKS + EFS shared filesystem
# =================================================================
def diag_623():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))
    body.append(group_vpc('vpc', 60, 100, 830, 390, 'VPC (EKS Cluster)'))

    body.append(group_az('az1', 100, 150, 240, 300, 'AZ-a'))
    body.append(group_az('az2', 360, 150, 240, 300, 'AZ-b'))
    body.append(group_az('az3', 620, 150, 240, 300, 'AZ-c'))

    body.append(icon('node1', 130, 200, 'Node', res_id='ec2'))
    body.append(icon('pod1', 230, 200, 'Pod A', res_id='fargate'))
    body.append(icon('mt1', 170, 350, 'Mount\nTarget', res_id='elastic_file_system'))

    body.append(icon('node2', 390, 200, 'Node', res_id='ec2'))
    body.append(icon('pod2', 490, 200, 'Pod B', res_id='fargate'))
    body.append(icon('mt2', 430, 350, 'Mount\nTarget', res_id='elastic_file_system'))

    body.append(icon('node3', 650, 200, 'Node', res_id='ec2'))
    body.append(icon('pod3', 750, 200, 'Pod C', res_id='fargate'))
    body.append(icon('mt3', 690, 350, 'Mount\nTarget', res_id='elastic_file_system'))

    body.append(arrow('m1', 195, 260, 195, 350, dashed=True))
    body.append(arrow('m2', 455, 260, 455, 350, dashed=True))
    body.append(arrow('m3', 715, 260, 715, 350, dashed=True))

    # AWS Backup
    body.append(icon('bk', 910, 200, 'AWS Backup\n1年保持', res_id='backup'))
    body.append(arrow('b1', 890, 370, 910, 230, dashed=True))

    body.append(box('cmp', 20, 510, 960, 70, fill='#FFF8E1', stroke='#FFA726',
                    color='#E65100', rounded=True, sw=1, fsize=11, bold=False,
                    title=''))
    body.append(multitext('cmpn', 40, 520, 920, 55,
        '要点: 複数 Pod が同一 FS を同時読み書き → EFS (NFS v4 POSIX / 共有マウント対応)&#10;'
        '     EBS は ReadWriteOnce (単一 Pod のみ) ／ S3 は POSIX 非互換 ／ FSx for Lustre は HPC 向け&#10;'
        '     各 AZ にマウントターゲット必須 (低レイテンシ＆高可用性)。AWS Backup で自動バックアップ。',
        size=11, color='#E65100'))

    return wrap('[Q623] EKS 共有ストレージ: EFS + 各AZ Mount Target + AWS Backup',
                '\n'.join(body))


# =================================================================
# [666] UDEMY-367 - Private API Gateway via VPCE + Resource Policy
# =================================================================
def diag_666():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))

    # VPC with microservices (EC2)
    body.append(group_vpc('vpc', 60, 100, 450, 400, 'VPC (多数のマイクロサービス)'))
    body.append(group_az('az1', 100, 150, 180, 160, 'AZ-1'))
    body.append(icon('ms1', 130, 200, 'EC2 μsvc', res_id='ec2'))
    body.append(group_az('az2', 300, 150, 180, 160, 'AZ-2'))
    body.append(icon('ms2', 330, 200, 'EC2 μsvc', res_id='ec2'))
    body.append(icon('vpce', 250, 360, 'Interface\nVPC Endpoint', res_id='api_gateway'))

    # API Gateway Private
    body.append(box('api', 560, 100, 400, 400, 'API Gateway (Private)',
                    stroke='#E7157B', color='#E7157B', sw=2, fsize=12))
    body.append(icon('apigw', 720, 140, 'Private API', res_id='api_gateway'))
    body.append(multitext('rp', 580, 230, 360, 260,
        'リソースポリシー (抜粋):&#10;&#10;'
        '{ "Effect": "Allow",&#10;'
        '  "Principal": "*",&#10;'
        '  "Action": "execute-api:Invoke",&#10;'
        '  "Resource": "execute-api:/*",&#10;'
        '  "Condition": {&#10;'
        '    "StringEquals": {&#10;'
        '      "aws:sourceVpce":&#10;'
        '        "vpce-0abcdef1234"&#10;'
        '    } } }&#10;&#10;'
        '→ VPC エンドポイント経由のみ許可',
        size=10, color='#232F3E', align='left'))

    body.append(arrow('a1', 180, 250, 280, 380, dashed=True, label='VPCE'))
    body.append(arrow('a2', 380, 250, 280, 380, dashed=True, label='VPCE'))
    body.append(arrow('a3', 350, 385, 720, 170, label='Private 経路', color='#7AA116', sw=3))

    body.append(box('note', 20, 520, 960, 60, fill='#FFF8E1', stroke='#FFA726',
                    color='#E65100', rounded=True, sw=1, fsize=11,
                    title='要点: Private API は Interface VPCE 必須 ／ sourceVpce 条件で特定 VPC 限定 ／ エンドポイントポリシーも重ねて最小権限'))

    return wrap('[Q666] Private API Gateway: VPCE + Resource Policy sourceVpce',
                '\n'.join(body))


# =================================================================
# [671] UDEMY-372 - ECS Blue/Green + Service Auto Scaling
# =================================================================
def diag_671():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))

    body.append(icon('cd', 80, 100, 'CodeDeploy\n(Blue/Green)', res_id='systems_manager'))

    body.append(icon('alb', 250, 150, 'ALB', res_id='application_load_balancer'))
    body.append(multitext('albn', 220, 210, 120, 40,
        '2つの TG を管理&#10;トラフィック切替', size=9))

    body.append(box('blue', 400, 90, 240, 140, 'Blue (旧バージョン)',
                    stroke='#3B48CC', color='#3B48CC', sw=2, fsize=11))
    body.append(icon('b1', 430, 130, 'Task', res_id='fargate'))
    body.append(icon('b2', 520, 130, 'Task', res_id='fargate'))

    body.append(box('green', 700, 90, 240, 140, 'Green (新バージョン)',
                    stroke='#7AA116', color='#7AA116', sw=2, fsize=11))
    body.append(icon('g1', 730, 130, 'Task', res_id='fargate'))
    body.append(icon('g2', 820, 130, 'Task', res_id='fargate'))

    body.append(arrow('a1', 130, 130, 250, 170, dashed=True, label='deploy'))
    body.append(arrow('a2', 300, 170, 400, 170, color='#3B48CC', label='100%'))
    body.append(arrow('a3', 300, 180, 700, 160, dashed=True, color='#7AA116',
                      label='切替後 100%'))

    # Service Auto Scaling
    body.append(box('sas', 40, 310, 920, 250, '📈 サービス Auto Scaling (Target Tracking / Step)',
                    stroke='#666666', color='#232F3E', fill='#FAFAFA', sw=1, fsize=12))
    body.append(icon('cw', 80, 360, 'CloudWatch', res_id='cloudwatch'))
    body.append(icon('sas_i', 240, 360, 'Application\nAuto Scaling', res_id='cloudwatch'))
    body.append(icon('ecs', 420, 360, 'ECS Service', res_id='ecs'))

    body.append(arrow('s1', 130, 385, 240, 385, label='CPU/Mem メトリクス'))
    body.append(arrow('s2', 290, 385, 420, 385, label='desired count 調整'))

    body.append(multitext('sasn', 600, 350, 360, 180,
        'ターゲット追跡 (例: CPU 50%):&#10;→ ECS が Task 数を自動増減&#10;&#10;'
        'ブルー/グリーン + Auto Scaling の利点:&#10;  ✓ ゼロダウンタイム (トラフィックは Blue が保持)&#10;'
        '  ✓ 問題時に即ロールバック可能&#10;'
        '  ✓ スパイク時は新Task自動追加&#10;'
        '  ✓ CodeDeploy フック検証ステップ可',
        size=10))

    return wrap('[Q671] ECS ゼロダウンタイム: Blue/Green + Service Auto Scaling',
                '\n'.join(body))


# =================================================================
# [672] UDEMY-373 - ECR Scan on Push + EventBridge + Step Functions
# =================================================================
def diag_672():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))

    body.append(icon('dev', 60, 100, 'CI/CD\n(push image)', res_id='systems_manager'))
    body.append(icon('ecr', 210, 100, 'ECR\nScan on Push', res_id='ecr'))
    body.append(icon('eb', 370, 100, 'EventBridge', res_id='eventbridge'))
    body.append(icon('sfn', 530, 100, 'Step Functions', res_id='step_functions'))
    body.append(icon('lam', 700, 50, 'Lambda\n(タグ削除)', res_id='lambda'))
    body.append(icon('sns', 700, 170, 'SNS\n開発チーム通知', res_id='simple_notification_service'))

    body.append(arrow('a1', 110, 125, 210, 125, label='push'))
    body.append(arrow('a2', 260, 125, 370, 125, label='スキャン完了'))
    body.append(arrow('a3', 420, 125, 530, 125, label='findings'))
    body.append(arrow('a4', 580, 125, 700, 80, color='#DD344C', label='CRITICAL/HIGH'))
    body.append(arrow('a5', 580, 125, 700, 195, color='#DD344C', label='通知'))

    # What happens
    body.append(box('decision', 40, 250, 920, 320, '🔍 脆弱性スキャン結果による分岐',
                    stroke='#666666', color='#232F3E', fill='#FAFAFA', sw=1, fsize=12))
    body.append(multitext('ddetail', 60, 290, 900, 270,
        '1) ECR で「スキャンオンプッシュ」を有効 → image push 時に自動スキャン&#10;&#10;'
        '2) EventBridge ルール: source=aws.ecr, detail-type="ECR Image Scan"&#10;   → スキャン完了イベントで Step Functions を起動&#10;&#10;'
        '3) Step Functions 内で Severity を判定 (Choice ステート)&#10;'
        '   ・CRITICAL / HIGH → Lambda 呼出 → ECR image タグを削除 (デプロイ停止)&#10;'
        '   ・同時に SNS トピックで開発チームへ通知&#10;'
        '   ・LOW / MEDIUM のみなら通知のみ (運用判断)&#10;&#10;'
        '✓ スキャンとデプロイゲート・通知を疎結合で実装（CI/CD に非侵襲）&#10;'
        '✓ Step Functions で複数条件の判定ロジックを宣言的に記述・可視化',
        size=11))

    return wrap('[Q672] ECR 脆弱性対策: Scan on Push + EventBridge + Step Functions + SNS',
                '\n'.join(body))


if __name__ == '__main__':
    diagrams = {
        'UDEMY-157': diag_456,
        'UDEMY-183': diag_482,
        'UDEMY-195': diag_494,
        'UDEMY-244': diag_543,
        'UDEMY-255': diag_554,
        'UDEMY-276': diag_575,
        'UDEMY-291': diag_590,
        'UDEMY-305': diag_604,
        'UDEMY-324': diag_623,
        'UDEMY-367': diag_666,
        'UDEMY-372': diag_671,
        'UDEMY-373': diag_672,
    }
    for qid, fn in diagrams.items():
        path = os.path.join(OUT_DIR, f'{qid}.drawio')
        if os.path.exists(path):
            print(f'SKIP (exists): {path}')
            continue
        with open(path, 'w') as f:
            f.write(fn())
        print(f'WROTE: {path}')
