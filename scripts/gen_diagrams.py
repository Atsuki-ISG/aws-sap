#!/usr/bin/env python3
"""Generate per-question drawio files for 25 selected questions."""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from drawio_helper import (
    icon, text_box, box, multitext, group_vpc, group_cloud, group_az,
    group_account, arrow, wrap,
)

OUT_DIR = '/Users/aki/aws-sap/docs/diagrams/per-question'
os.makedirs(OUT_DIR, exist_ok=True)

# =================================================================
# [301] UDEMY-002 - EKS コンテナ化マルチティア (EFS+DynamoDB+EKS)
# =================================================================
def diag_301():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))
    body.append(group_vpc('vpc', 60, 90, 640, 430, 'VPC (EKS Cluster)'))

    # EKS icon
    body.append(icon('eks', 100, 140, 'EKS マネージドノード'))
    body.append(icon('fargate', 100, 250, 'Fargate (オプション)'))

    # Three layers as pod
    body.append(box('pod1', 240, 120, 430, 60, 'Pod: ビデオストリーミング層',
                    stroke='#FF9900', color='#FF9900', sw=2))
    body.append(multitext('pod1t', 260, 150, 380, 30,
        'Deployment + HPA ／ ALB ターゲット', size=10))

    body.append(box('pod2', 240, 200, 430, 60, 'Pod: コンテンツ管理層',
                    stroke='#FF9900', color='#FF9900', sw=2))
    body.append(multitext('pod2t', 260, 230, 380, 30,
        'Deployment + HPA', size=10))

    body.append(box('pod3', 240, 280, 430, 60, 'Pod: 学習データベース層',
                    stroke='#FF9900', color='#FF9900', sw=2))
    body.append(multitext('pod3t', 260, 310, 380, 30,
        'StatefulSet ／ 永続ボリューム要', size=10))

    # EFS for shared
    body.append(icon('efs', 500, 400, 'EFS 共有ストレージ',
                     res_id='elastic_file_system'))
    # DynamoDB for session
    body.append(icon('ddb', 760, 140, 'DynamoDB\nセッション',
                     res_id='dynamodb'))
    # ALB
    body.append(icon('alb', 760, 280, 'ALB',
                     res_id='application_load_balancer'))

    # Arrows
    body.append(arrow('a1', 700, 310, 760, 310))
    body.append(arrow('a2', 670, 150, 760, 165, label='セッション保存'))
    body.append(arrow('a3', 525, 400, 400, 340, dashed=True, label='共有マウント'))

    # Key points
    body.append(box('note', 20, 550, 960, 40, fill='#FFF8E1', stroke='#FFA726',
                    color='#E65100', rounded=True, sw=1, fsize=11, bold=True,
                    title='要点: ストリーミング=ALB+HPA／セッション=DynamoDB（ステートレス化）／共有ファイル=EFS マルチAZマウント'))

    return wrap('[Q301] EKS マルチティア: セッション=DynamoDB, 共有=EFS', '\n'.join(body))


# =================================================================
# [324] UDEMY-025 - API Gateway + WAF + Usage Plan/API Key
# =================================================================
def diag_324():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))

    # 3 research institutions (left)
    body.append(box('inst', 40, 100, 200, 180, '3つの医療研究機関',
                    stroke='#3B48CC', color='#3B48CC', sw=2))
    body.append(multitext('insta', 60, 130, 160, 140,
        '研究機関A (IP: x.x.x.1)&#10;研究機関B (IP: x.x.x.2)&#10;研究機関C (IP: x.x.x.3)&#10;&#10;毎日1回アクセス&#10;匿名化患者データ送信', size=10))

    # 悪意のあるボット (bottom left)
    body.append(box('bot', 40, 310, 200, 120, '悪意あるボットネット',
                    stroke='#DD344C', color='#DD344C', sw=2))
    body.append(multitext('bota', 60, 340, 160, 80,
        '1,000 IP から&#10;毎秒 2,000 req&#10;&#10;✗ ブロック対象', size=10, color='#DD344C'))

    # AWS WAF
    body.append(icon('waf', 310, 170, 'AWS WAF', res_id='waf'))
    body.append(multitext('wafn', 280, 230, 130, 60,
        'IP 許可リスト&#10;(3機関のみ)', size=10, color='#DD344C', align='center'))

    # API Gateway
    body.append(icon('apigw', 510, 170, 'API Gateway\n(REST Regional)',
                     res_id='api_gateway'))
    body.append(multitext('apin', 480, 240, 130, 80,
        '• 使用量プラン&#10;• API キー&#10;• レート制限&#10;• スロットル', size=10, color='#232F3E', align='center'))

    # Lambda / backend
    body.append(icon('lam', 770, 170, 'Lambda\n分析処理', res_id='lambda'))

    # Arrows
    body.append(arrow('a1', 240, 200, 310, 200, color='#7AA116', label='許可', sw=3))
    body.append(arrow('a2', 240, 370, 310, 230, color='#DD344C', label='✗ ブロック',
                      sw=2, dashed=True))
    body.append(arrow('a3', 360, 200, 510, 200))
    body.append(arrow('a4', 560, 200, 770, 200))

    body.append(box('note', 20, 470, 960, 100, fill='#E3F2FD', stroke='#1976D2',
                    color='#0D47A1', rounded=True, sw=1, fsize=11, bold=False,
                    title=''))
    body.append(multitext('noteinner', 40, 485, 920, 80,
        '要点:&#10;'
        '  ① WAF（IP セット）= ネットワーク層で不正 IP を遮断（DDoS / ボット対策）&#10;'
        '  ② API キー + 使用量プラン = 認証された正規顧客ごとにレート上限・クォータを付与&#10;'
        '  ③ WAF だけでは顧客別レート制御はできない。API キーだけでは IP 制限はできない → 両方必須',
        size=11, color='#0D47A1'))

    return wrap('[Q324] API Gateway セキュリティ: WAF(IP) + 使用量プラン(レート)', '\n'.join(body))


# =================================================================
# [331] UDEMY-032 - LMS: Amplify + Cognito + S3 + Lambda
# =================================================================
def diag_331():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))

    # Users
    body.append(box('users', 40, 90, 150, 80, '学生・教職員',
                    stroke='#3B48CC', color='#3B48CC', sw=2))
    body.append(multitext('userst', 60, 120, 110, 40,
        '北米・欧州&#10;（グローバル）', size=10, align='center'))

    # Cognito (auth)
    body.append(icon('cog', 240, 90, 'Cognito\n(MFA)', res_id='cognito'))

    # CloudFront
    body.append(icon('cf', 400, 90, 'CloudFront', res_id='cloudfront'))

    # Amplify Hosting + S3 static
    body.append(icon('amp', 560, 90, 'Amplify Hosting',
                     res_id='amplify', fill='#E7157B'))
    body.append(icon('s3s', 720, 90, 'S3 静的サイト',
                     res_id='simple_storage_service'))

    # Arrow from user to Cognito to CF to Amplify
    body.append(arrow('a1', 190, 115, 240, 115, label='① 認証'))
    body.append(arrow('a2', 290, 115, 400, 115, label='JWT'))
    body.append(arrow('a3', 450, 115, 560, 115))
    body.append(arrow('a4', 610, 115, 720, 115))

    # Upload flow (bottom)
    body.append(box('flow', 40, 220, 920, 280, 'ファイルアップロード・処理フロー',
                    stroke='#666666', color='#232F3E', fill='#FAFAFA', sw=1, fsize=12))

    # Upload file -> S3 files
    body.append(icon('s3f', 80, 280, 'S3 ファイル保存',
                     res_id='simple_storage_service'))
    body.append(multitext('s3fn', 50, 340, 140, 40,
        'Lifecycle:&#10;古いファイルを&#10;アーカイブ', size=9))

    # EventBridge
    body.append(icon('eb', 260, 280, 'EventBridge', res_id='eventbridge'))

    # Lambda
    body.append(icon('lam', 420, 280, 'Lambda', res_id='lambda'))
    body.append(multitext('lamn', 390, 340, 120, 40,
        'ウイルススキャン&#10;メタデータ抽出', size=9))

    # DynamoDB
    body.append(icon('ddb', 600, 280, 'DynamoDB\nメタデータ', res_id='dynamodb'))

    # SNS
    body.append(icon('sns', 780, 280, 'SNS 通知',
                     res_id='simple_notification_service'))

    body.append(arrow('b1', 130, 305, 260, 305))
    body.append(arrow('b2', 310, 305, 420, 305))
    body.append(arrow('b3', 470, 305, 600, 305))
    body.append(arrow('b4', 650, 305, 780, 305))

    # Points
    body.append(box('note', 20, 530, 960, 50, fill='#E8F5E9', stroke='#388E3C',
                    color='#1B5E20', rounded=True, sw=1, fsize=11,
                    title='要点: 認証=Cognito+MFA／静的配信=Amplify+CloudFront／ファイル=S3+Lifecycle／イベント駆動処理=EventBridge+Lambda（フルマネージド）'))

    return wrap('[Q331] LMS AWS化: Cognito + Amplify + S3 + EventBridge + Lambda', '\n'.join(body))


# =================================================================
# [344] UDEMY-045 - AppSync + SQS + DLQ + Lambda
# =================================================================
def diag_344():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))

    # User
    body.append(box('u', 40, 100, 120, 60, '顧客・店舗',
                    stroke='#3B48CC', color='#3B48CC', sw=2))

    # CloudFront
    body.append(icon('cf', 190, 100, 'CloudFront', res_id='cloudfront'))

    # S3 static
    body.append(icon('s3', 350, 100, 'S3 静的サイト',
                     res_id='simple_storage_service'))

    body.append(arrow('a1', 160, 130, 190, 130))
    body.append(arrow('a2', 240, 130, 350, 130))

    # AppSync - the order API
    body.append(icon('as', 510, 100, 'AppSync\n注文管理 API',
                     res_id='appsync'))
    body.append(multitext('asn', 480, 160, 130, 30,
        'GraphQL / 単一EP', size=9))

    body.append(arrow('a3', 240, 130, 510, 115, dashed=True, label='注文 API'))

    # SQS
    body.append(icon('sqs', 700, 100, 'SQS\n注文キュー',
                     res_id='simple_queue_service'))

    # Lambda (processor)
    body.append(icon('lam', 700, 250, 'Lambda\n配送ロジック',
                     res_id='lambda'))

    # DLQ
    body.append(icon('dlq', 500, 380, 'SQS DLQ\n失敗注文管理',
                     res_id='simple_queue_service', fill='#DD344C'))

    # DB
    body.append(icon('ddb', 860, 250, 'DynamoDB', res_id='dynamodb'))

    body.append(arrow('a4', 560, 130, 700, 130))
    body.append(arrow('a5', 725, 155, 725, 250))
    body.append(arrow('a6', 750, 275, 860, 275))
    body.append(arrow('a7', 700, 285, 550, 385, dashed=True, color='#DD344C',
                      label='処理失敗→DLQ'))

    body.append(box('note', 20, 470, 960, 100, fill='#E3F2FD', stroke='#1976D2',
                    color='#0D47A1', rounded=True, sw=1, fsize=11,
                    title=''))
    body.append(multitext('noteinner', 40, 485, 920, 80,
        '要点: AppSync（GraphQL）がリアルタイム通知 & サブスクリプションに最適。API Gateway+REST より注文状態のプッシュ通知に有利。&#10;'
        '     SQS = 処理の平滑化／バックエンド保護。DLQ = 失敗した注文を可視化・後追い処理可能。AppSync vs API Gateway: 複数クライアントへのプッシュが必要なら AppSync。',
        size=11, color='#0D47A1'))

    return wrap('[Q344] サーバーレス注文: AppSync + SQS/DLQ + Lambda', '\n'.join(body))


# =================================================================
# [358] UDEMY-059 - AppSync WebSocket + DynamoDB Streams
# =================================================================
def diag_358():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))

    # Before / After
    body.append(box('before', 40, 90, 440, 460, '❌ 現行: API Gateway + ポーリング',
                    stroke='#DD344C', color='#DD344C', sw=2, fsize=12))
    body.append(icon('apigw', 170, 150, 'API Gateway', res_id='api_gateway'))
    body.append(icon('lamb', 170, 260, 'Lambda', res_id='lambda'))
    body.append(icon('ddbb', 170, 370, 'DynamoDB', res_id='dynamodb'))
    body.append(box('client1', 300, 160, 130, 340, '読者クライアント',
                    stroke='#3B48CC', color='#3B48CC', sw=1, fsize=10))
    body.append(multitext('beforen', 310, 190, 115, 300,
        '定期的に&#10;/reactions を&#10;ポーリング&#10;&#10;→ 遅延が大きい&#10;→ 無駄なリクエスト&#10;→ スケール困難', size=10, color='#DD344C', align='center'))
    body.append(arrow('b1', 220, 200, 300, 230, dashed=True, color='#DD344C',
                      label='poll'))

    body.append(box('after', 500, 90, 460, 460, '✓ AppSync + WebSocket',
                    stroke='#7AA116', color='#7AA116', sw=2, fsize=12))
    body.append(icon('ddb', 540, 150, 'DynamoDB\n+ Streams', res_id='dynamodb'))
    body.append(icon('lam', 540, 280, 'Lambda', res_id='lambda'))
    body.append(icon('as', 730, 150, 'AppSync', res_id='appsync'))
    body.append(box('client2', 830, 160, 110, 300, '読者クライアント',
                    stroke='#3B48CC', color='#3B48CC', sw=1, fsize=10))
    body.append(multitext('aftern', 840, 200, 90, 240,
        'Subscribe&#10;&#10;→ 即時プッシュ&#10;→ WebSocket&#10;→ 接続維持', size=10, color='#7AA116', align='center'))

    body.append(arrow('f1', 590, 200, 590, 280, label='Stream'))
    body.append(arrow('f2', 590, 335, 730, 200, label='Mutation'))
    body.append(arrow('f3', 780, 200, 830, 200, label='push'))

    body.append(box('note', 20, 560, 960, 30, fill='#FFF8E1', stroke='#FFA726',
                    color='#E65100', rounded=True, sw=1, fsize=11, bold=True,
                    title='要点: リアルタイム配信 → AppSync(Subscription/WebSocket)。API Gateway(REST)はリクエスト/レスポンス型、プッシュ配信には不向き'))

    return wrap('[Q358] リアルタイム反応配信: AppSync + DDB Streams', '\n'.join(body))


# =================================================================
# [369] UDEMY-070 - ECS+APIGW マルチリージョン DR (Route53 Failover)
# =================================================================
def diag_369():
    body = []

    body.append(icon('r53', 450, 60, 'Route 53\nFailover', res_id='route_53'))

    # Primary region
    body.append(group_cloud('pri', 20, 170, 460, 400, 'プライマリ Region'))
    body.append(icon('apigw1', 60, 230, 'API GW Regional', res_id='api_gateway'))
    body.append(icon('ecs1', 240, 230, 'ECS Fargate', res_id='fargate'))
    body.append(icon('aur1', 60, 400, 'Aurora Global\n(Writer)', res_id='aurora'))
    body.append(icon('ddb1', 240, 400, 'DynamoDB\nGlobal Table', res_id='dynamodb'))

    # Secondary region
    body.append(group_cloud('sec', 500, 170, 460, 400, 'セカンダリ Region'))
    body.append(icon('apigw2', 540, 230, 'API GW Regional', res_id='api_gateway'))
    body.append(icon('ecs2', 720, 230, 'ECS Fargate', res_id='fargate'))
    body.append(icon('aur2', 540, 400, 'Aurora Global\n(Reader→Writer昇格)', res_id='aurora'))
    body.append(icon('ddb2', 720, 400, 'DynamoDB\nGlobal Table', res_id='dynamodb'))

    body.append(arrow('r1', 475, 95, 110, 230, label='Primary'))
    body.append(arrow('r2', 525, 95, 590, 230, dashed=True, label='Failover',
                      color='#DD344C'))
    body.append(arrow('g1', 110, 400, 590, 400, color='#7AA116', sw=3,
                      label='Aurora Global レプリケーション (<1秒)'))
    body.append(arrow('g2', 290, 440, 770, 440, color='#7AA116', sw=3,
                      label='DDB Global Table 双方向レプリ'))

    body.append(arrow('p1', 110, 260, 240, 260))
    body.append(arrow('p2', 590, 260, 720, 260))

    body.append(box('note', 20, 10, 960, 40, fill='#FFEBEE', stroke='#C62828',
                    color='#B71C1C', rounded=True, sw=1, fsize=11, bold=True,
                    title='要点: API GW=Regional（Edgeはカスタム不可） / Aurora Global=<1秒RPO / DDB Global=双方向 / Route53=ヘルスチェックベース自動切替'))

    return wrap('[Q369] マルチリージョン DR: APIGW Regional + Aurora Global + Route53', '\n'.join(body))


# =================================================================
# [388] UDEMY-089 - API GW Latency-Based Routing + RDS Read Replica
# =================================================================
def diag_388():
    body = []

    body.append(icon('r53', 450, 50, 'Route 53\nLatency-based', res_id='route_53'))

    # NA user
    body.append(box('nau', 40, 130, 130, 60, '北米ユーザー',
                    stroke='#3B48CC', color='#3B48CC', sw=2))

    # EU user
    body.append(box('euu', 830, 130, 130, 60, '欧州ユーザー',
                    stroke='#3B48CC', color='#3B48CC', sw=2))

    # NA region
    body.append(group_cloud('na', 20, 220, 460, 340, '北米リージョン (us-east-1)'))
    body.append(icon('apigw1', 60, 260, 'API GW', res_id='api_gateway'))
    body.append(icon('lam1', 210, 260, 'Lambda', res_id='lambda'))
    body.append(icon('rds1', 360, 260, 'RDS Primary', res_id='rds'))

    # EU region
    body.append(group_cloud('eu', 500, 220, 460, 340, '欧州リージョン (eu-west-1)'))
    body.append(icon('apigw2', 540, 260, 'API GW', res_id='api_gateway'))
    body.append(icon('lam2', 690, 260, 'Lambda', res_id='lambda'))
    body.append(icon('rds2', 840, 260, 'RDS Read Replica\n(95% Read OK)', res_id='rds'))

    body.append(arrow('l1', 450, 90, 110, 260, label='近い方へ'))
    body.append(arrow('l2', 525, 90, 590, 260, label='近い方へ'))
    body.append(arrow('na1', 170, 155, 450, 85, dashed=True))
    body.append(arrow('eu1', 830, 155, 550, 85, dashed=True))

    body.append(arrow('repl', 410, 400, 840, 400, color='#7AA116', sw=3,
                      label='非同期リードレプリカ複製'))

    body.append(arrow('na2', 110, 290, 210, 290))
    body.append(arrow('na3', 260, 290, 360, 290))
    body.append(arrow('eu2', 590, 290, 690, 290))
    body.append(arrow('eu3', 740, 290, 840, 290))

    body.append(box('note', 20, 570, 960, 25, fill='#E8F5E9', stroke='#388E3C',
                    color='#1B5E20', rounded=True, sw=1, fsize=11, bold=True,
                    title='要点: 95%が Read → RDS リードレプリカで十分（Aurora Global より低コスト） / Route53=Latency-based で近いリージョンへ'))

    return wrap('[Q388] EU低レイテンシ化: Route53 Latency + RDS リードレプリカ', '\n'.join(body))


# =================================================================
# [416] UDEMY-117 - API GW IAM認証 + SigV4 + X-Ray
# =================================================================
def diag_416():
    body = []

    body.append(box('client', 40, 100, 180, 300, 'API クライアント\n(他AWSアカウント)',
                    stroke='#3B48CC', color='#3B48CC', sw=2, fsize=12))
    body.append(icon('iam', 80, 150, 'IAM User/Role\n(execute-api:Invoke)',
                     res_id='identity_and_access_management'))
    body.append(multitext('sig', 55, 260, 150, 120,
        '① IAM 認証情報&#10;② AWS SigV4 で&#10;   リクエスト署名&#10;③ Authorization&#10;   ヘッダー付与&#10;④ API GW へ送信', size=10, color='#232F3E', align='left'))

    body.append(icon('apigw', 340, 200, 'API Gateway\n認証: AWS_IAM',
                     res_id='api_gateway'))
    body.append(multitext('apigwn', 310, 280, 130, 40,
        'IAM 検証&#10;+ X-Ray トレース', size=10, color='#232F3E', align='center'))

    body.append(icon('lam', 550, 200, 'Lambda\nバックエンド', res_id='lambda'))

    body.append(icon('xray', 750, 200, 'X-Ray\nサービスマップ', res_id='x_ray',
                     fill='#E7157B'))

    body.append(arrow('a1', 220, 225, 340, 225, label='SigV4 署名済'))
    body.append(arrow('a2', 390, 225, 550, 225))
    body.append(arrow('a3', 365, 250, 775, 250, dashed=True, label='trace', color='#E7157B'))
    body.append(arrow('a4', 575, 250, 775, 250, dashed=True, color='#E7157B'))

    body.append(box('cmp', 40, 440, 920, 140, '📊 認証方式の比較',
                    stroke='#666666', color='#232F3E', fill='#FAFAFA', sw=1, fsize=12))
    body.append(multitext('cmpn', 60, 475, 900, 100,
        '• AWS_IAM 認証: 他AWSサービス/他アカウントからのマシン間呼び出しに最適。SigV4 で署名。CloudTrail にも記録。&#10;'
        '• Cognito User Pool 認証: エンドユーザー（モバイル/Web） → JWT 発行型&#10;'
        '• Lambda Authorizer: カスタムロジック（OAuth/SAML 等）&#10;'
        '• API Key: 使用量プランのみ（認証目的では使わない）',
        size=11, color='#232F3E'))

    return wrap('[Q416] API Gateway 認証: IAM (SigV4) + X-Ray 分析', '\n'.join(body))


# =================================================================
# [419] UDEMY-120 - .NET Core on ECS EC2 + RDS SQL Server + SQS
# =================================================================
def diag_419():
    body = []

    body.append(box('goal', 20, 50, 960, 60, '要件: MSMQ 互換メッセージング + SQL Server 維持 + コンテナオーケストレーション完全制御',
                    stroke='#3B48CC', color='#3B48CC', fill='#E3F2FD', sw=2, fsize=12))

    body.append(group_cloud('cloud', 20, 130, 960, 440))

    # ECS EC2
    body.append(icon('ecs', 80, 190, 'ECS (EC2 起動)', res_id='ecs'))
    body.append(multitext('ecsn', 50, 250, 120, 40,
        'EC2 完全制御&#10;OS/ネットワーク', size=9))

    body.append(icon('ec2a', 230, 190, '.NET Core&#10;Publisher', res_id='ec2'))
    body.append(icon('sqs', 430, 190, 'SQS\n(MSMQ代替)', res_id='simple_queue_service'))
    body.append(icon('ec2b', 630, 190, '.NET Core&#10;Consumer', res_id='ec2'))
    body.append(icon('rds', 830, 190, 'RDS\nSQL Server', res_id='rds'))

    body.append(arrow('a1', 280, 215, 430, 215, label='送信'))
    body.append(arrow('a2', 480, 215, 630, 215, label='受信'))
    body.append(arrow('a3', 680, 215, 830, 215, label='永続化'))

    body.append(box('cmp', 40, 320, 920, 220, '🧭 選択肢の比較',
                    stroke='#666666', color='#232F3E', fill='#FAFAFA', sw=1, fsize=12))
    body.append(multitext('cmpn', 60, 355, 900, 180,
        '✓ ECS EC2 起動: EC2 インスタンスへの完全制御 (OS/ENI/ドライバ) — 正解&#10;'
        '✗ ECS Fargate: インスタンスは見えない (管理を AWS に委譲) → "完全制御" 要件を満たさない&#10;'
        '✗ EKS: オーバースペック (.NET Core コンポーネント数個にはコスト/運用重い)&#10;'
        '✗ Lambda: MSMQ 互換の長時間実行/状態管理が不適合&#10;'
        '&#10;SQS: MSMQ 相当の非同期キュー。FIFO が必要なら FIFO キューで順序保証。&#10;'
        'RDS for SQL Server: SQL Server 互換ライセンスを維持したまま AWS 管理へ。',
        size=11, color='#232F3E'))

    return wrap('[Q419] .NET 移行: ECS EC2 + RDS SQL Server + SQS', '\n'.join(body))


# =================================================================
# [428] UDEMY-129 - ECS Fargate + EFS
# =================================================================
def diag_428():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))

    # Store containers
    body.append(box('store', 40, 100, 420, 200, '小売店舗: PoS / 在庫管理',
                    stroke='#3B48CC', color='#3B48CC', sw=2, fsize=12))
    body.append(icon('ecs', 80, 150, 'ECS Fargate', res_id='fargate'))
    body.append(icon('d1', 230, 150, 'Docker\nContainer', res_id='ec2'))
    body.append(icon('d2', 360, 150, 'Docker\nContainer', res_id='ec2'))

    body.append(icon('efs', 600, 160, 'EFS\n共有ファイル', res_id='elastic_file_system'))
    body.append(multitext('efsn', 570, 230, 130, 40,
        'NFS 互換&#10;マルチAZ', size=10, align='center'))

    body.append(icon('rds', 780, 160, 'RDS\nリアルタイムTX', res_id='rds'))

    body.append(arrow('a1', 410, 180, 600, 180, label='NFS mount'))
    body.append(arrow('a2', 410, 210, 780, 210, label='TX'))

    body.append(box('cmp', 40, 340, 920, 220, '📊 ストレージ選択の判断軸',
                    stroke='#666666', color='#232F3E', fill='#FAFAFA', sw=1, fsize=12))
    body.append(multitext('cmpn', 60, 375, 900, 180,
        '🎯 ECS Fargate + EFS = 既存 Docker コンテナ用共有ファイル＋サーバーレス運用&#10;&#10;'
        '• EFS: NFS 互換、複数タスク同時マウント、Posix — 既存アプリの変更最小で移行可能&#10;'
        '• FSx for Windows: SMB プロトコル（Windows 系）&#10;'
        '• S3: オブジェクトストア、POSIX 非互換 → ファイル共有アクセスには不適&#10;'
        '• EBS: 1 タスクにしかアタッチできない（ECS Fargate は EFS/S3 のみが共有ストレージ選択肢）&#10;'
        '&#10;⚠ Fargate は EC2 不要／タスクをサーバーレスで実行。Auto Scaling 設定も簡単。',
        size=11, color='#232F3E'))

    return wrap('[Q428] コンテナ移行: ECS Fargate + EFS (共有FS)', '\n'.join(body))


# =================================================================
# [439] UDEMY-140 - Private REST API via VPC Endpoint
# =================================================================
def diag_439():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))
    body.append(group_vpc('vpc', 60, 100, 500, 400, 'HR VPC'))

    body.append(icon('ec2', 120, 160, 'HR システム (EC2)', res_id='ec2'))

    # Interface VPC Endpoint
    body.append(box('vpce', 100, 270, 400, 180, 'Interface VPC Endpoint',
                    stroke='#7AA116', color='#7AA116', sw=2, fsize=12))
    body.append(icon('vpcei', 150, 310, 'execute-api EP', res_id='api_gateway'))
    body.append(multitext('vpcen', 120, 380, 360, 60,
        '• Private DNS 有効化 ON&#10;• エンドポイントポリシー: execute-api:Invoke 許可&#10;• 標準 DNS名で呼出 (execute-api.region.amazonaws.com)',
        size=10, align='left'))

    body.append(arrow('a1', 170, 210, 220, 310, dashed=True, label='Private DNS'))

    # Private API
    body.append(box('papi', 600, 140, 340, 330, 'API Gateway (Private エンドポイント)',
                    stroke='#E7157B', color='#E7157B', sw=2, fsize=12))
    body.append(icon('api', 750, 180, 'Private REST API', res_id='api_gateway'))
    body.append(multitext('resp', 620, 260, 300, 180,
        'リソースポリシー:&#10;'
        '{&#10;'
        '  "Effect": "Allow",&#10;'
        '  "Principal": "*",&#10;'
        '  "Action": "execute-api:Invoke",&#10;'
        '  "Condition": {&#10;'
        '    "StringEquals": {&#10;'
        '      "aws:sourceVpce": "vpce-xxx"&#10;'
        '    }&#10;'
        '  }&#10;'
        '}', size=10, align='left', color='#232F3E'))

    body.append(arrow('a2', 280, 360, 750, 200, label='VPC内通信のみ', color='#7AA116', sw=3))

    body.append(box('note', 20, 520, 960, 60, fill='#FFF8E1', stroke='#FFA726',
                    color='#E65100', rounded=True, sw=1, fsize=11,
                    title='要点: Private API → Interface VPCE 必須 ／ リソースポリシーで aws:sourceVpce 条件 ／ Private DNS 有効で標準DNS名が使える'))

    return wrap('[Q439] Private API Gateway: VPC Endpoint + リソースポリシー', '\n'.join(body))


# =================================================================
# [441] UDEMY-142 - EKS Fargate + ALB + MSK + S3/CloudFront
# =================================================================
def diag_441():
    body = []
    body.append(group_cloud('cloud', 20, 50, 960, 510))

    # Users
    body.append(box('users', 40, 100, 100, 50, 'ゲーマー',
                    stroke='#3B48CC', color='#3B48CC', sw=2))
    body.append(icon('cf', 170, 100, 'CloudFront', res_id='cloudfront'))
    body.append(icon('s3', 320, 100, 'S3\nゲームアセット', res_id='simple_storage_service'))

    body.append(arrow('u1', 140, 125, 170, 125))
    body.append(arrow('u2', 220, 125, 320, 125, label='static'))

    # ALB
    body.append(icon('alb', 470, 100, 'ALB', res_id='application_load_balancer'))
    body.append(arrow('u3', 140, 125, 470, 125, dashed=True, label='API'))

    # EKS Fargate
    body.append(box('eksbox', 620, 80, 340, 170, 'EKS + Fargate',
                    stroke='#FF9900', color='#FF9900', sw=2, fsize=12))
    body.append(icon('eks', 660, 120, 'EKS', res_id='eks'))
    body.append(icon('fg', 790, 120, 'Fargate Pods\n(Auto Scale)', res_id='fargate'))

    body.append(arrow('a1', 520, 125, 620, 125))

    # MSK
    body.append(icon('msk', 340, 330, 'MSK\n(Apache Kafka)', res_id='managed_streaming_for_apache_kafka'))
    body.append(icon('rds', 600, 330, 'RDS + Read Replica', res_id='rds'))

    body.append(arrow('a2', 790, 175, 420, 355, dashed=True, label='イベント'))
    body.append(arrow('a3', 790, 175, 650, 355, dashed=True, label='Read/Write'))

    body.append(box('cmp', 40, 430, 920, 140, '🧭 なぜ EKS + Fargate が最適？',
                    stroke='#666666', color='#232F3E', fill='#FAFAFA', sw=1, fsize=12))
    body.append(multitext('cmpn', 60, 465, 900, 110,
        '• 突発スケール: EKS Fargate は Pod 単位でサーバーレススケール (ノード不要)&#10;'
        '• Kafka 移行: MSK はフルマネージド Kafka → 既存のブローカー運用をオフロード&#10;'
        '• S3+CloudFront: ゲームアセットの全世界低レイテンシ配信に最適&#10;'
        '• パブリック IP の EC2 直接公開 (現行) = 運用負荷/セキュリティリスク高 → ALB 配下のコンテナへ',
        size=11, color='#232F3E'))

    return wrap('[Q441] ゲームサーバー: EKS Fargate + ALB + MSK + CloudFront/S3', '\n'.join(body))


# =================================================================
# [452] UDEMY-153 - ECS Capacity Provider (Spot) + Predictive Scaling
# =================================================================
def diag_452():
    body = []

    body.append(box('sit', 20, 50, 960, 60, 'シーン: 繁忙期（イースター・独立記念日）トラフィック急増／オンデマンドのみでは高コスト',
                    stroke='#3B48CC', color='#3B48CC', fill='#E3F2FD', sw=2, fsize=12))

    body.append(group_cloud('cloud', 20, 130, 960, 440))

    # ECS Cluster
    body.append(box('ecscl', 40, 170, 920, 220, 'ECS Cluster',
                    stroke='#FF9900', color='#FF9900', sw=2, fsize=12))
    body.append(icon('ecs', 80, 210, 'ECS', res_id='ecs'))

    # Capacity Provider 1: On-Demand
    body.append(box('cp1', 200, 210, 340, 160, '① On-Demand Capacity Provider (既存)',
                    stroke='#666666', color='#666666', sw=2, fsize=11))
    body.append(icon('asg1', 230, 240, 'ASG (OD)', res_id='ec2'))
    body.append(multitext('cp1n', 290, 260, 240, 80,
        '重み: 1 (例)&#10;安定性重視&#10;予測可能な負荷用', size=10))

    # Capacity Provider 2: Spot (NEW)
    body.append(box('cp2', 570, 210, 360, 160, '② Spot Capacity Provider (追加)',
                    stroke='#7AA116', color='#7AA116', sw=2, fsize=11))
    body.append(icon('asg2', 600, 240, 'ASG (Spot)', res_id='ec2'))
    body.append(multitext('cp2n', 660, 260, 260, 80,
        '重み: 1 (同じ)&#10;⭐ コスト最大 90% 削減&#10;中断許容可能なワークロード', size=10, color='#7AA116'))

    # Predictive scaling
    body.append(box('ps', 40, 410, 460, 150, 'E. 予測スケーリングポリシー',
                    stroke='#3B48CC', color='#3B48CC', sw=2, fsize=11))
    body.append(multitext('psn', 60, 445, 420, 110,
        '• スケジュールドスケーリング → 固定時刻&#10;'
        '• 予測スケーリング → ML で過去のパターン予測&#10;&#10;'
        '  → 繁忙期前にプロアクティブにキャパシティ確保&#10;'
        '  → スパイク遅延を回避',
        size=10))

    body.append(box('ans', 520, 410, 440, 150, '✓ 正解: A + E',
                    stroke='#7AA116', color='#7AA116', sw=2, fsize=11))
    body.append(multitext('ansn', 540, 445, 400, 110,
        'A. Spot ECS キャパシティプロバイダ追加 (重み同じ)&#10;E. 予測スケーリングポリシーを使う&#10;&#10;'
        '✗ C (オンデマンドキャパシティ予約) はコスト削減にはならない&#10;'
        '✗ S3 Transfer Acceleration は関係ない',
        size=10))

    return wrap('[Q452] ECS Capacity Provider: Spot + 予測スケーリング', '\n'.join(body))


if __name__ == '__main__':
    diagrams = {
        'UDEMY-002': diag_301,
        'UDEMY-025': diag_324,
        'UDEMY-032': diag_331,
        'UDEMY-045': diag_344,
        'UDEMY-059': diag_358,
        'UDEMY-070': diag_369,
        'UDEMY-089': diag_388,
        'UDEMY-117': diag_416,
        'UDEMY-120': diag_419,
        'UDEMY-129': diag_428,
        'UDEMY-140': diag_439,
        'UDEMY-142': diag_441,
        'UDEMY-153': diag_452,
    }
    for qid, fn in diagrams.items():
        path = os.path.join(OUT_DIR, f'{qid}.drawio')
        if os.path.exists(path):
            print(f'SKIP (exists): {path}')
            continue
        with open(path, 'w') as f:
            f.write(fn())
        print(f'WROTE: {path}')
