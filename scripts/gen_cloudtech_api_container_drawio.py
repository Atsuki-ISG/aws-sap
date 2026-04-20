#!/usr/bin/env python3
"""
Generate per-question drawio files for CloudTech (SAP-*) questions
focused on API Gateway / AppSync / Cognito / Lambda / ECS / EKS / Fargate / ECR / IRSA.

1000x600 canvas, white background, AWS official colors, 50x50 icons with labels.
Label y must be >= icon.y + 58.
"""
from pathlib import Path

OUT = Path('/Users/aki/aws-sap/docs/diagrams/per-question')
OUT.mkdir(parents=True, exist_ok=True)

# ===== drawio helpers =====
def drawio_wrap(content_xml, diagram_id, name):
    return f'''<mxfile host="app.diagrams.net" modified="2026-04-20T18:00:00.000Z" agent="Claude" version="24.0.0">
  <diagram id="{diagram_id}" name="{name}">
    <mxGraphModel dx="1422" dy="757" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1000" pageHeight="600" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
{content_xml}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

def title(text, y=14):
    # escape double quotes
    text = text.replace('"', '&quot;')
    return f'''<mxCell id="title" value="{text}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;fontStyle=1;fontColor=#232F3E;" vertex="1" parent="1">
  <mxGeometry x="20" y="{y}" width="960" height="30" as="geometry" />
</mxCell>'''

def subtitle(text, x=20, y=44, w=960, h=22):
    text = text.replace('"', '&quot;')
    return f'''<mxCell id="subtitle_{x}_{y}" value="{text}" style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=11;fontColor=#666666;fontStyle=2;" vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>'''

ICON_COLOR = {
    'api_gateway': '#E7157B', 'appsync': '#E7157B', 'cognito': '#DD344C',
    'lambda': '#ED7100', 'ecs': '#ED7100', 'eks': '#ED7100', 'fargate': '#ED7100',
    'ecr': '#ED7100', 'ec2': '#ED7100', 'batch': '#ED7100',
    's3': '#7AA116', 'dynamodb': '#3B48CC', 'rds': '#3B48CC', 'aurora': '#3B48CC',
    'application_load_balancer': '#8C4FFF', 'cloudfront': '#8C4FFF',
    'route_53': '#8C4FFF', 'eventbridge': '#E7157B', 'sns': '#E7157B', 'sqs': '#E7157B',
    'identity_and_access_management': '#DD344C', 'kms': '#DD344C',
    'secrets_manager': '#DD344C', 'waf': '#DD344C',
    'x_ray': '#E7157B', 'cloudwatch': '#E7157B', 'step_functions': '#E7157B',
    'cloudformation': '#C925D1', 'codedeploy': '#C925D1', 'codepipeline': '#C925D1',
    'mq': '#E7157B', 'rekognition': '#01A88D',
    'elastic_container_registry': '#ED7100', 'elastic_kubernetes_service': '#ED7100',
    'rds_proxy': '#3B48CC',
}

def icon(id_, res_icon, x, y, label=None, w=50, h=50, color=None, label_w=110):
    text_color = '#232F3E'
    fill = color or ICON_COLOR.get(res_icon, '#E7157B')
    elems = []
    style = (f"sketch=0;outlineConnect=0;fontColor={text_color};gradientColor=none;"
             f"fillColor={fill};strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;"
             f"verticalAlign=top;align=center;html=1;fontSize=10;fontStyle=0;aspect=fixed;"
             f"shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{res_icon};")
    elems.append(f'''<mxCell id="{id_}" value="" style="{style}" vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>''')
    if label:
        label = label.replace('"', '&quot;')
        ly = y + 58
        half = label_w // 2
        cx = x + w // 2
        elems.append(f'''<mxCell id="{id_}_l" value="{label}" style="text;html=1;align=center;verticalAlign=top;whiteSpace=wrap;fontSize=10;fontColor=#232F3E;" vertex="1" parent="1">
  <mxGeometry x="{cx - half}" y="{ly}" width="{label_w}" height="34" as="geometry" />
</mxCell>''')
    return '\n'.join(elems)

def user_icon(id_, label, x, y):
    label = label.replace('"', '&quot;')
    return f'''<mxCell id="{id_}" value="{label}" style="sketch=0;points=[[0.5,0,0],[1,1,0],[0,1,0]];outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#232F3E;strokeColor=#232F3E;html=1;verticalLabelPosition=bottom;labelPosition=center;verticalAlign=top;align=center;shape=mxgraph.aws4.user;" vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="40" height="45" as="geometry" />
</mxCell>'''

def arrow(id_, src, tgt, label='', color='#232F3E', dashed=False):
    label = label.replace('"', '&quot;')
    style = f"endArrow=classic;html=1;strokeColor={color};strokeWidth=2;fontSize=10;fontColor=#232F3E;"
    if dashed:
        style += "dashed=1;"
    lbl_attr = f'value="{label}"' if label else 'value=""'
    return f'''<mxCell id="{id_}" {lbl_attr} style="{style}" edge="1" parent="1" source="{src}" target="{tgt}">
  <mxGeometry relative="1" as="geometry" />
</mxCell>'''

def arrow_xy(id_, x1, y1, x2, y2, label='', color='#232F3E', dashed=False):
    label = label.replace('"', '&quot;')
    style = f"endArrow=classic;html=1;strokeColor={color};strokeWidth=2;fontSize=10;fontColor=#232F3E;"
    if dashed:
        style += "dashed=1;"
    lbl_attr = f'value="{label}"' if label else 'value=""'
    return f'''<mxCell id="{id_}" {lbl_attr} style="{style}" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="{x1}" y="{y1}" as="sourcePoint" />
    <mxPoint x="{x2}" y="{y2}" as="targetPoint" />
  </mxGeometry>
</mxCell>'''

def note(id_, text, x, y, w=960, h=50, fill='#FFF5EB', stroke='#FF9900', font_style=1, font_size=11):
    text = text.replace('"', '&quot;')
    return f'''<mxCell id="{id_}" value="{text}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize={font_size};fontStyle={font_style};fontColor=#232F3E;verticalAlign=middle;align=left;spacingLeft=10;spacingRight=10;" vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>'''

def group_rect(id_, label, x, y, w, h, stroke='#4D72F3', fill='none'):
    label = label.replace('"', '&quot;')
    return f'''<mxCell id="{id_}" value="{label}" style="rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=2;fontSize=11;fontStyle=1;fontColor={stroke};verticalAlign=top;align=left;spacingLeft=8;spacingTop=4;dashed=1;" vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>'''


# ===== Diagram builders =====
DIAGRAMS = {}


def make_sap_281():
    t = "SAP-281 / HTTP API + Lambda + DynamoDB サーバーレス公開 API"
    s = "外部パートナーへ安価で低レイテンシな HTTPS API を提供するサーバーレス構成"
    cells = [
        title(t), subtitle(s),
        user_icon('u', '3rd Party\nDevelopers', 60, 130),
        icon('apigw', 'api_gateway', 200, 130, label='API Gateway\n(HTTP API)'),
        icon('lambda', 'lambda', 380, 130, label='Lambda\n(集約・検証)'),
        icon('ddb1', 'dynamodb', 580, 80, label='DynamoDB\n商品在庫テーブル'),
        icon('ddb2', 'dynamodb', 580, 180, label='DynamoDB\n売上統計テーブル'),
        arrow_xy('a1', 105, 150, 200, 150, 'HTTPS'),
        arrow('a2', 'apigw', 'lambda', 'JWT/APIキー'),
        arrow_xy('a3', 435, 145, 580, 105, 'Query'),
        arrow_xy('a4', 435, 160, 580, 205, 'Query'),
        note('good', '✅ 正解 A/B: HTTP API は REST API より 70% 安価・低レイテンシ。Lambda で複数テーブル集約・入力検証が柔軟。完全サーバーレスで運用負荷ゼロ。',
             20, 310, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ API Gateway → DynamoDB 直接統合: JOIN 不可・レスポンス整形困難・パス設計が肥大化',
             20, 370, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ ECS/EKS でホスト: 常時稼働コストと運用工数が過大。パートナー API のトラフィックにフィットしない',
             510, 370, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 HTTP API vs REST API: HTTP API は JWT/OIDC 認可・CORS・低コスト。REST API は WAF/API キー/使用量プラン。要件で選ぶ。',
             20, 435, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 1 Lambda で集約パターン: パラメータ別にテーブル選択 → 複数 GetItem/Query を Promise.all で並列化しレイテンシ最小化',
             20, 485, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'httpapi-lambda-dynamodb'
DIAGRAMS['SAP-281'] = make_sap_281


def make_sap_298():
    t = "SAP-298 / AWS SAM による API Gateway + Lambda + DynamoDB の IaC/CI-CD"
    s = "YAML テンプレートでサーバーレス 3 点セットを定義し、sam deploy でリリース自動化"
    cells = [
        title(t), subtitle(s),
        user_icon('dev', 'Developer', 30, 140),
        icon('git', 'codepipeline', 130, 140, label='Git Repo\n(template.yaml)'),
        icon('cp', 'codepipeline', 290, 140, label='CodePipeline\n(sam build/deploy)'),
        icon('cfn', 'cloudformation', 450, 140, label='CloudFormation\n(SAM 変換)'),
        # deployed stack
        group_rect('stack', 'Deployed Stack', 610, 100, 370, 160, stroke='#7AA116'),
        icon('apigw', 'api_gateway', 635, 135, label='API Gateway'),
        icon('lambda', 'lambda', 775, 135, label='Lambda'),
        icon('ddb', 'dynamodb', 905, 135, label='DynamoDB', label_w=70),
        arrow_xy('f1', 450, 155, 380, 155, '', color='#7AA116'),
        arrow('a1', 'git', 'cp', 'push'),
        arrow('a2', 'cp', 'cfn', 'deploy'),
        arrow_xy('a3', 505, 160, 635, 160, '作成/更新'),
        arrow('a5', 'apigw', 'lambda', ''),
        arrow('a6', 'lambda', 'ddb', ''),
        note('good', '✅ 正解 B: AWS SAM は CloudFormation の拡張で AWS::Serverless::Function/Api/SimpleTable を提供。短い YAML で API+Lambda+DDB を一括定義。',
             20, 290, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ Elastic Beanstalk: サーバーレス向けではなく EC2 ベース。管理外のインフラが生まれる',
             20, 350, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ コンソール手動: 変更履歴追跡不可・複数リージョン複製不可・監査要件を満たさない',
             510, 350, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 SAM の hot reload: sam sync で差分デプロイ高速化、sam local で Lambda をローカル起動可能',
             20, 415, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 CDK vs SAM: CDK はプログラム言語で柔軟、SAM は YAML でシンプル。小規模サーバーレスは SAM が学習コスト低',
             20, 465, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sam-apigw-lambda-ddb'
DIAGRAMS['SAP-298'] = make_sap_298


def make_sap_99():
    t = "SAP-99 / モノリシック EC2 → API Gateway + Lambda サーバーレス化"
    s = "Route 53 DNS 切替で段階移行。モバイル負荷増への弾力的スケール"
    cells = [
        title(t), subtitle(s),
        # before
        group_rect('before', 'BEFORE: モノリシック 5 台 EC2', 20, 80, 440, 210, stroke='#DD344C'),
        user_icon('u1', 'Mobile\nClient', 50, 150),
        icon('r531', 'route_53', 140, 140, label='Route 53\nA レコード', label_w=90),
        icon('ec2a', 'ec2', 280, 110, label='EC2', label_w=60),
        icon('ec2b', 'ec2', 280, 200, label='EC2', label_w=60),
        icon('ec2c', 'ec2', 380, 155, label='EC2', label_w=60),
        arrow('b1', 'u1', 'r531', ''),
        arrow('b2', 'r531', 'ec2a', ''),
        arrow('b3', 'r531', 'ec2b', ''),
        # after
        group_rect('after', 'AFTER: サーバーレス API', 490, 80, 490, 210, stroke='#7AA116'),
        user_icon('u2', 'Mobile\nClient', 510, 150),
        icon('r532', 'route_53', 595, 140, label='Route 53\nCNAME 変更', label_w=100),
        icon('apigw', 'api_gateway', 735, 140, label='API Gateway\nREST'),
        icon('lam', 'lambda', 875, 80, label='Lambda\n認証機能', label_w=90),
        icon('lam2', 'lambda', 875, 160, label='Lambda\n課金機能', label_w=90),
        icon('lam3', 'lambda', 875, 240, label='Lambda\nランキング', label_w=90),
        arrow('c1', 'u2', 'r532', ''),
        arrow('c2', 'r532', 'apigw', ''),
        arrow('c3', 'apigw', 'lam', ''),
        arrow('c4', 'apigw', 'lam2', ''),
        arrow('c5', 'apigw', 'lam3', ''),
        note('good', '✅ 正解 A: 機能単位で Lambda 化 → API Gateway で統合。Route 53 で DNS 切替のみ、クライアント無改修で移行',
             20, 340, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ ALB + EC2 Auto Scaling: 依然として EC2 パッチ・スケジューリング管理が必要',
             20, 400, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ ECS Fargate: マネージドだがコンテナ運用工数あり。API 群は Lambda の方がフィット',
             510, 400, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 モノリス分割のコツ: まず機能境界を特定 → 各 Lambda 専用の IAM ロール・タイムアウト・メモリを個別最適化',
             20, 465, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'ec2-to-apigw-lambda'
DIAGRAMS['SAP-99'] = make_sap_99


def make_sap_29():
    t = "SAP-29 / 間欠アクセス向け: API Gateway + Lambda + Aurora Serverless"
    s = "アイドル時に Aurora を停止、ピーク時は自動スケール。ランニングコスト最小化"
    cells = [
        title(t), subtitle(s),
        user_icon('u', '社内\n従業員', 60, 150),
        icon('r53', 'route_53', 160, 140, label='Route 53\n既存ドメイン', label_w=110),
        icon('apigw', 'api_gateway', 310, 140, label='API Gateway'),
        icon('lam', 'lambda', 460, 140, label='Lambda\nINSERT 処理'),
        icon('aurora', 'aurora', 620, 140, label='Aurora Serverless\n自動停止/起動'),
        icon('bi', 'dynamodb', 800, 140, label='社内 BI ツール\n(SQL 参照)', color='#3B48CC', label_w=110),
        arrow('a1', 'u', 'r53', ''),
        arrow('a2', 'r53', 'apigw', 'DNS'),
        arrow('a3', 'apigw', 'lam', ''),
        arrow('a4', 'lam', 'aurora', 'INSERT'),
        arrow('a5', 'bi', 'aurora', 'SELECT', color='#3B48CC', dashed=True),
        note('good', '✅ 正解 A: Aurora Serverless v1/v2 は使用量に応じ ACU 自動スケール & アイドル時停止。間欠アクセス Web フォームに最適',
             20, 290, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ RDS プロビジョンド: 常時稼働インスタンス料金が発生、アイドル時間コスト削減できない',
             20, 350, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ DynamoDB: SQL 必須要件（社内 BI）に適合しない。JOIN やアドホック SQL 不可',
             510, 350, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 Aurora Serverless v2 は秒単位スケール。v1 は MinACU=0 で完全停止可能（コールドスタート数秒）',
             20, 415, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 API Gateway + Lambda + Aurora Serverless = 「フルマネージド SQL バックエンド」の三種の神器',
             20, 465, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'apigw-lambda-aurora-serverless'
DIAGRAMS['SAP-29'] = make_sap_29


def make_sap_210():
    t = "SAP-210 / API Gateway + Lambda + DynamoDB + SNS モバイルプッシュ"
    s = "スタッフ操作を Lambda で受け、DynamoDB 更新 → SNS で即時通知"
    cells = [
        title(t), subtitle(s),
        user_icon('staff', '倉庫\nスタッフ', 30, 90),
        user_icon('user', 'エンド\nユーザー', 30, 230),
        icon('apigw', 'api_gateway', 150, 150, label='API Gateway\n(両フロント)'),
        icon('lam', 'lambda', 310, 150, label='Lambda\nステータス更新'),
        icon('ddb', 'dynamodb', 470, 150, label='DynamoDB\n注文状態'),
        icon('sns', 'sns', 630, 150, label='SNS Topic\n(発送完了)'),
        icon('push', 'sns', 800, 150, label='モバイルプッシュ\n(APNs/FCM)'),
        arrow('a1', 'staff', 'apigw', '「発送完了」'),
        arrow('a2', 'user', 'apigw', '状態確認'),
        arrow('a3', 'apigw', 'lam', ''),
        arrow('a4', 'lam', 'ddb', 'UpdateItem'),
        arrow('a5', 'lam', 'sns', 'Publish'),
        arrow('a6', 'sns', 'push', ''),
        note('good', '✅ 正解 B: API Gateway+Lambda+DynamoDB で CRUD、SNS モバイルプッシュで即時通知。完全サーバーレスで Auto Scaling',
             20, 290, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ EC2+RDS+自前プッシュサーバ: 運用負荷大・スケール限界',
             20, 350, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ Amazon SES メール通知のみ: 即時性不足、モバイル要件未達',
             510, 350, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 SNS モバイルプッシュ: プラットフォームエンドポイント登録 → Publish で APNs/FCM/ADM に配信',
             20, 415, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 DynamoDB Streams + Lambda でイベント駆動: UpdateItem 後に自動で SNS Publish する設計も可能',
             20, 465, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'apigw-lambda-ddb-sns-push'
DIAGRAMS['SAP-210'] = make_sap_210


def make_sap_77():
    t = "SAP-77 / API Gateway + Lambda + Cognito UserPool (SNS ログイン)"
    s = "Cognito オーソライザーで認証委譲。メール/SNS ログインとサインアップを統合"
    cells = [
        title(t), subtitle(s),
        user_icon('u', 'モバイル\n会員', 30, 150),
        icon('cog', 'cognito', 140, 150, label='Cognito UserPool\n(SNS Federation)'),
        icon('apigw', 'api_gateway', 330, 150, label='API Gateway\nREST API'),
        icon('lam', 'lambda', 490, 150, label='Lambda\n(ビジネスロジック)'),
        icon('ddb', 'dynamodb', 660, 90, label='DynamoDB\n進捗データ'),
        icon('s3', 's3', 660, 210, label='S3\nワークアウト動画'),
        # OAuth flow indicators
        arrow('a1', 'u', 'cog', '① サインイン'),
        arrow_xy('a2', 180, 130, 350, 130, '② JWT (id/access)', color='#7AA116'),
        arrow('a3', 'u', 'apigw', ''),
        arrow('a4', 'apigw', 'lam', 'Cognito Authorizer検証'),
        arrow('a5', 'lam', 'ddb', ''),
        arrow('a6', 'lam', 's3', ''),
        note('good', '✅ 正解 A: Cognito が「メール認証」「SNS フェデレーション」をネイティブに提供。API Gateway 統合で完全マネージド認証',
             20, 310, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ IAM ユーザーで全員管理: 会員規模で破綻。IAM は AWS リソース制御用、人間ユーザーには不向き',
             20, 370, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ 自前認証サーバ: OAuth/OIDC 実装工数大・脆弱性リスク・運用負荷',
             510, 370, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 Cognito UserPool vs IdentityPool: UserPool=認証(JWT発行)、IdentityPool=AWS一時認証情報発行',
             20, 435, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 Cognito Authorizer と Lambda Authorizer の使い分け: 標準は Cognito、カスタム検証ロジックは Lambda',
             20, 485, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'apigw-lambda-cognito'
DIAGRAMS['SAP-77'] = make_sap_77


def make_sap_193():
    t = "SAP-193 / オンプレ Java SaaS → S3 SPA + Cognito(SAML) + APIGW + Fargate + Aurora Serverless"
    s = "AD を SAML フェデレーションで Cognito に委譲、バックエンドはマイクロサービス化"
    cells = [
        title(t), subtitle(s),
        user_icon('u', '従業員', 30, 150),
        # AD
        icon('ad', 'identity_and_access_management', 30, 70, label='既存 AD\n(SAML IdP)', label_w=110, color='#666666'),
        icon('s3', 's3', 160, 150, label='S3 静的\nSPA'),
        icon('cog', 'cognito', 290, 150, label='Cognito\n(SAML 連携)'),
        icon('apigw', 'api_gateway', 440, 150, label='API Gateway\nREST'),
        icon('fg', 'fargate', 600, 150, label='Fargate タスク\n(Java マイクロサービス)'),
        icon('aur', 'aurora', 790, 150, label='Aurora MySQL\nServerless'),
        arrow('a1', 'u', 's3', ''),
        arrow_xy('a2', 50, 115, 290, 160, 'SAML SSO', color='#DD344C', dashed=True),
        arrow('a3', 's3', 'cog', ''),
        arrow('a4', 'cog', 'apigw', 'JWT'),
        arrow('a5', 'apigw', 'fg', ''),
        arrow('a6', 'fg', 'aur', ''),
        note('good', '✅ 正解 A/B/C: SPA は S3 静的配信、AD は Cognito SAML 連携、Java は改修せず Fargate へ、MySQL は Aurora Serverless',
             20, 290, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ EC2 リフト&シフト: OS パッチ・AD 連携コード保守が残存しマネージド化目的達成せず',
             20, 350, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ Lambda 全面書換: Java マイクロサービスは Fargate が無改修・長時間処理に向く',
             510, 350, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 Cognito UserPool は SAML/OIDC/ソーシャルを IdP として統合可能。既存 AD/Azure AD を使い続けられる',
             20, 415, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 マイクロサービスの言語が Java/C# など重めなら Fargate、軽量イベント処理は Lambda。ランタイム特性で使い分け',
             20, 465, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'saml-cognito-apigw-fargate'
DIAGRAMS['SAP-193'] = make_sap_193


def make_sap_25():
    t = "SAP-25 / Lambda コネクション枯渇問題: RDS Proxy による接続プール"
    s = "API Gateway + Lambda + Aurora でピーク時 DB 接続数超過 → RDS Proxy で共有"
    cells = [
        title(t), subtitle(s),
        # before
        group_rect('before', 'BEFORE: Lambda が直接 Aurora 接続', 20, 80, 440, 230, stroke='#DD344C'),
        icon('apigw1', 'api_gateway', 50, 140, label='API Gateway'),
        icon('lam1a', 'lambda', 190, 110, label='Lambda', label_w=70),
        icon('lam1b', 'lambda', 190, 180, label='Lambda', label_w=70),
        icon('lam1c', 'lambda', 190, 250, label='Lambda', label_w=70),
        icon('aur1', 'aurora', 360, 180, label='Aurora\n接続枯渇!', color='#DD344C'),
        arrow('b1', 'apigw1', 'lam1a', ''),
        arrow('b2', 'apigw1', 'lam1b', ''),
        arrow('b3', 'apigw1', 'lam1c', ''),
        arrow('b4', 'lam1a', 'aur1', '', color='#DD344C'),
        arrow('b5', 'lam1b', 'aur1', '', color='#DD344C'),
        arrow('b6', 'lam1c', 'aur1', '', color='#DD344C'),
        # after
        group_rect('after', 'AFTER: RDS Proxy 経由で接続プール共有', 490, 80, 490, 230, stroke='#7AA116'),
        icon('apigw2', 'api_gateway', 510, 140, label='API Gateway'),
        icon('lam2a', 'lambda', 640, 110, label='Lambda', label_w=70),
        icon('lam2b', 'lambda', 640, 180, label='Lambda', label_w=70),
        icon('lam2c', 'lambda', 640, 250, label='Lambda', label_w=70),
        icon('proxy', 'rds', 790, 180, label='RDS Proxy\n(接続プール)', color='#3B48CC'),
        icon('aur2', 'aurora', 910, 180, label='Aurora\n(リーダー)', label_w=80),
        arrow('c1', 'apigw2', 'lam2a', ''),
        arrow('c2', 'apigw2', 'lam2b', ''),
        arrow('c3', 'apigw2', 'lam2c', ''),
        arrow('c4', 'lam2a', 'proxy', ''),
        arrow('c5', 'lam2b', 'proxy', ''),
        arrow('c6', 'lam2c', 'proxy', ''),
        arrow('c7', 'proxy', 'aur2', 'プール済み'),
        note('good', '✅ 正解 B+D: RDS Proxy で接続多重化、Provisioned Concurrency でコールドスタート削減',
             20, 360, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('tip', '📌 RDS Proxy の効果: Lambda の数百〜数千同時実行でも DB 接続を数十で共有 → max_connections 回避',
             20, 420, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 Provisioned Concurrency: 初期化済み実行環境を常備。料金と引き換えに p99 レイテンシを安定化',
             20, 470, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'lambda-rds-proxy-aurora'
DIAGRAMS['SAP-25'] = make_sap_25


def make_sap_245():
    t = "SAP-245 / Lambda RDS 接続問題 + SNS→SQS バッファリング"
    s = "DB CPU 飽和 & 接続失敗 → RDS Proxy と SQS 挟み込みで平準化・再試行保証"
    cells = [
        title(t), subtitle(s),
        icon('s3', 's3', 30, 150, label='S3\n動画アップ'),
        icon('sns', 'sns', 170, 150, label='SNS Topic'),
        icon('sqs', 'sqs', 310, 150, label='SQS 標準\n(バッファ)'),
        icon('lam1', 'lambda', 460, 90, label='Lambda\nメタデータ抽出1', label_w=120),
        icon('lam2', 'lambda', 460, 170, label='Lambda\nメタデータ抽出2', label_w=120),
        icon('lam3', 'lambda', 460, 250, label='Lambda\nメタデータ抽出3', label_w=120),
        icon('proxy', 'rds', 650, 170, label='RDS Proxy\n(接続プール)', color='#3B48CC', label_w=120),
        icon('rds', 'rds', 820, 170, label='RDS PostgreSQL\n(Multi-AZ)'),
        arrow('a1', 's3', 'sns', ''),
        arrow('a2', 'sns', 'sqs', 'Sub'),
        arrow('a3', 'sqs', 'lam1', 'poll'),
        arrow('a4', 'sqs', 'lam2', 'poll'),
        arrow('a5', 'sqs', 'lam3', 'poll'),
        arrow('a6', 'lam1', 'proxy', ''),
        arrow('a7', 'lam2', 'proxy', ''),
        arrow('a8', 'lam3', 'proxy', ''),
        arrow('a9', 'proxy', 'rds', 'プール'),
        note('good', '✅ 正解 A+D: RDS Proxy で DB 接続集約 (CPU 飽和緩和)、SNS→SQS→Lambda でバッファリング＆DLQ で再試行保証',
             20, 340, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ RDS インスタンスサイズアップのみ: 根本原因（Lambda 接続急増）解消せず、コスト増',
             20, 400, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ SNS 直接 Lambda のまま: バースト時に実行数上限、失敗は SNS 側では永続しない',
             510, 400, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 SNS→SQS→Lambda: SNS fan-out に耐久性(SQS)とバッファを追加。DLQ と Visibility Timeout で信頼性確保',
             20, 465, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sns-sqs-lambda-rds-proxy'
DIAGRAMS['SAP-245'] = make_sap_245


def make_sap_248():
    t = "SAP-248 / S3 直接アップ → SQS → Lambda → Rekognition → SNS プッシュ"
    s = "署名付き URL + SQS バッファでスパイク吸収、SNS で即時通知"
    cells = [
        title(t), subtitle(s),
        user_icon('u', 'モバイル\nアプリ', 30, 150),
        icon('s3', 's3', 140, 150, label='S3\n(事前署名URL)'),
        icon('sqs', 'sqs', 290, 150, label='SQS Standard\n(バッファ)'),
        icon('lam', 'lambda', 440, 150, label='Lambda\n(並列消費)'),
        icon('rek', 'rekognition', 590, 150, label='Rekognition\n画像解析'),
        icon('ddb', 'dynamodb', 740, 90, label='DynamoDB\nタグ保存'),
        icon('sns', 'sns', 740, 220, label='SNS モバイル\nプッシュ'),
        user_icon('u2', 'モバイル\n通知', 880, 220),
        arrow('a1', 'u', 's3', '直接 PUT'),
        arrow_xy('a2', 190, 140, 290, 160, 'S3 Event', color='#7AA116'),
        arrow('a3', 'sqs', 'lam', 'poll'),
        arrow('a4', 'lam', 'rek', 'DetectLabels'),
        arrow_xy('a5', 495, 145, 740, 105, '結果保存'),
        arrow_xy('a6', 495, 175, 740, 235, '通知 Publish'),
        arrow('a7', 'sns', 'u2', ''),
        note('good', '✅ 正解 A/B/F: クライアント直 PUT で API 介在なし、SQS でスパイク吸収、SNS プッシュで即時通知',
             20, 310, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ API Gateway 経由でアップ: ペイロード 10MB 制限、転送コスト増、スループット低下',
             20, 370, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ S3 → Lambda 直接: バースト時に同時実行制限・失敗時は SQS のような永続バッファ無し',
             510, 370, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 事前署名 URL: サーバ側で生成 → クライアントが一時的にバケットに直 PUT。認証情報を渡さず安全',
             20, 435, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 S3 → SQS は S3 Event Notification で直接連携可能。Lambda 挟まず低コストで信頼性向上',
             20, 485, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 's3-sqs-lambda-rekognition-sns'
DIAGRAMS['SAP-248'] = make_sap_248


def make_sap_92():
    t = "SAP-92 / 長時間画像処理: Lambda(タイムアウト) → ECR + Fargate RunTask"
    s = "Lambda 15 分制限を超える処理は Fargate タスクへオフロード"
    cells = [
        title(t), subtitle(s),
        icon('s3a', 's3', 30, 150, label='S3 バケット A\n(原画像)'),
        icon('lam', 'lambda', 180, 150, label='Lambda\n(軽量判定)'),
        # Branch to fargate
        icon('ecr', 'ecr', 340, 80, label='ECR\n(画像変換\nコンテナ)', label_w=110),
        icon('fg', 'fargate', 340, 220, label='Fargate タスク\n(変換実行)', label_w=120),
        icon('s3b', 's3', 520, 80, label='S3 バケット B\n(リサイズ済み)'),
        icon('ddb', 'dynamodb', 520, 220, label='DynamoDB\nメタデータ'),
        arrow('a1', 's3a', 'lam', 'Event'),
        arrow_xy('a2', 235, 160, 340, 240, 'RunTask', color='#ED7100'),
        arrow_xy('a3', 380, 140, 380, 200, 'pull image', dashed=True, color='#666'),
        arrow_xy('a4', 395, 240, 520, 105, '書込'),
        arrow_xy('a5', 395, 260, 520, 235, '書込'),
        note('good', '✅ 正解 A+B: コンテナ化→ECR 保存、Lambda から RunTask で Fargate を起動。Lambda の 15 分制限・メモリ制限を回避',
             20, 310, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ Lambda の memory/timeout 増加のみ: 最大 15 分・10GB 制限。ヘビーな画像処理は超過しやすい',
             20, 370, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ EC2 Auto Scaling: 常時稼働コストと AMI 管理。イベント駆動型には重量級すぎる',
             510, 370, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 Lambda から RunTask: boto3/SDK で ecs.run_task() → Fargate は数秒で起動・完了後自動終了',
             20, 435, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 Lambda vs Fargate: 15 分・10GB 以内なら Lambda、それ以上または長時間・大容量は Fargate',
             20, 485, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'lambda-ecr-fargate-runtask'
DIAGRAMS['SAP-92'] = make_sap_92


def make_sap_107():
    t = "SAP-107 / 定期 ETL: ECR + Fargate + EventBridge Schedule"
    s = "4 時間ごとに Fargate 起動 → 20 分で完了 → 自動終了。EC2 常駐ゼロ"
    cells = [
        title(t), subtitle(s),
        icon('eb', 'eventbridge', 100, 160, label='EventBridge\nSchedule\n(4 時間毎)', label_w=120),
        icon('ecr', 'ecr', 290, 80, label='ECR\n(ETL コンテナ)', label_w=110),
        icon('fg', 'fargate', 290, 240, label='Fargate タスク\n(20 分で完了)', label_w=140),
        icon('s3i', 's3', 490, 80, label='S3 入力\n(広告ログ)'),
        icon('s3o', 's3', 490, 240, label='S3 出力\n(変換済み)'),
        icon('dash', 'dynamodb', 720, 160, label='ダッシュボード\n(BI ツール)', color='#3B48CC', label_w=130),
        arrow_xy('a1', 160, 185, 290, 265, 'RunTask', color='#ED7100'),
        arrow_xy('a2', 330, 140, 330, 230, 'pull', dashed=True, color='#666'),
        arrow_xy('a3', 345, 260, 490, 110, 'read'),
        arrow_xy('a4', 345, 275, 490, 270, 'write'),
        arrow_xy('a5', 545, 270, 720, 185, 'load'),
        note('good', '✅ 正解 A: コンテナ化して Fargate 実行、EventBridge cron で起動。バイナリ改修不要、アイドルコストゼロ',
             20, 340, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ Batch: ジョブキュー・コンピュート環境など追加コンポーネントが必要。今回は Fargate 単発で十分',
             20, 400, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ Lambda: シングルスレッド・2GB RAM・CPU 集中型・20 分必要 → Lambda 制限に抵触しやすい',
             510, 400, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 EventBridge Scheduler (2022 新): cron/rate 式で Fargate RunTask を直接起動。Lambda 介在不要',
             20, 465, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'eventbridge-fargate-etl'
DIAGRAMS['SAP-107'] = make_sap_107


def make_sap_82():
    t = "SAP-82 / ECS Fargate + Secrets Manager + RDS SQL Server Multi-AZ"
    s = "シークレットを定義から直接注入、ALB + サービスオートスケールで弾力運用"
    cells = [
        title(t), subtitle(s),
        user_icon('u', '受講者', 30, 150),
        icon('alb', 'application_load_balancer', 130, 150, label='ALB'),
        # Fargate service
        group_rect('svc', 'ECS Service on Fargate (Auto Scaling)', 260, 90, 310, 220, stroke='#ED7100'),
        icon('fg1', 'fargate', 290, 130, label='Fargate\nTask 1', label_w=80),
        icon('fg2', 'fargate', 290, 230, label='Fargate\nTask 2', label_w=80),
        icon('fg3', 'fargate', 440, 130, label='Fargate\nTask 3', label_w=80),
        icon('fg4', 'fargate', 440, 230, label='Fargate\nTask N', label_w=80),
        icon('sec', 'secrets_manager', 620, 90, label='Secrets Manager\nDB資格情報'),
        icon('rds', 'rds', 780, 180, label='RDS SQL Server\nMulti-AZ'),
        arrow('a1', 'u', 'alb', ''),
        arrow_xy('a2', 185, 170, 290, 155, ''),
        arrow_xy('a3', 185, 175, 290, 250, ''),
        arrow_xy('a4', 625, 125, 545, 155, 'secrets 注入', color='#DD344C', dashed=True),
        arrow_xy('a5', 625, 135, 545, 250, 'secrets 注入', color='#DD344C', dashed=True),
        arrow_xy('a6', 550, 175, 780, 195, 'SQL 接続'),
        arrow_xy('a7', 550, 265, 780, 210, 'SQL 接続'),
        note('good', '✅ 正解 B: タスク定義の secrets フィールドが Secrets Manager ARN を環境変数に自動展開。コード側で変更不要',
             20, 340, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ イメージに資格情報を埋め込む: Git に漏れる、ローテーション不可。重大な PCI DSS 違反',
             20, 400, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ 環境変数に平文: タスク定義 JSON や ECR メタデータから漏洩リスク',
             510, 400, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Secrets Manager は Lambda による自動ローテーション対応。RDS は最初から統合あり',
             20, 465, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'fargate-secrets-rds-multiaz'
DIAGRAMS['SAP-82'] = make_sap_82


def make_sap_294():
    t = "SAP-294 / マイクロサービス化: ECR + 1 クラスター + 本番/テスト Fargate サービス"
    s = "本番・テストを同一クラスター内の別サービスとして分離、ALB ターゲットグループで独立運用"
    cells = [
        title(t), subtitle(s),
        icon('ecr', 'ecr', 60, 160, label='ECR\n(共通イメージ)'),
        # ECS cluster
        group_rect('cluster', 'ECS Cluster (1 個)', 220, 80, 530, 280, stroke='#ED7100'),
        group_rect('prod', 'Prod Service (Fargate)', 240, 110, 230, 100, stroke='#7AA116'),
        icon('fp1', 'fargate', 260, 130, label='Task', label_w=60),
        icon('fp2', 'fargate', 380, 130, label='Task', label_w=60),
        group_rect('test', 'Test Service (Fargate)', 240, 230, 230, 100, stroke='#3B48CC'),
        icon('ft1', 'fargate', 260, 250, label='Task', label_w=60),
        icon('ft2', 'fargate', 380, 250, label='Task', label_w=60),
        icon('albp', 'application_load_balancer', 550, 130, label='ALB TG\n(Prod)'),
        icon('albt', 'application_load_balancer', 550, 250, label='ALB TG\n(Test)'),
        user_icon('u1', '本番\nユーザー', 820, 120),
        user_icon('u2', 'テスト\nユーザー', 820, 230),
        arrow_xy('a1', 110, 170, 220, 170, 'pull'),
        arrow_xy('a2', 110, 180, 220, 280, 'pull'),
        arrow_xy('a3', 470, 155, 550, 155, ''),
        arrow_xy('a4', 470, 275, 550, 275, ''),
        arrow_xy('a5', 605, 150, 820, 140, ''),
        arrow_xy('a6', 605, 275, 820, 250, ''),
        note('good', '✅ 正解 B: 1 クラスタ・2 サービス・2 ALB TG 構成。サービスオートスケールで最小/最大を個別制御',
             20, 390, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('tip', '📌 クラスタは論理境界。サービスごとにタスク定義・スケール設定・IAM ロールを独立管理',
             20, 450, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 Fargate サービスオートスケール: ALB RequestCountPerTarget / CPU 利用率 / メモリ で自動増減',
             20, 500, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'ecr-fargate-prod-test'
DIAGRAMS['SAP-294'] = make_sap_294


def make_sap_173():
    t = "SAP-173 / 月次バッチ: 5TB EC2 cron → Fargate + EventBridge"
    s = "5TB EBS 常備を廃止、一時ストレージで圧縮、完了後リソース自動解放"
    cells = [
        title(t), subtitle(s),
        # before
        group_rect('before', 'BEFORE: 常時稼働 EC2 + 5TB EBS', 20, 80, 440, 200, stroke='#DD344C'),
        icon('ec2', 'ec2', 60, 120, label='EC2 (cron)\n月 1 回起動', label_w=110),
        icon('ebs', 'dynamodb', 230, 120, label='5TB EBS\n(常時確保)', color='#DD344C', label_w=100),
        icon('s3b1', 's3', 370, 120, label='S3 入/出力'),
        arrow('b1', 'ec2', 'ebs', ''),
        arrow('b2', 'ec2', 's3b1', ''),
        # after
        group_rect('after', 'AFTER: Fargate + EventBridge', 490, 80, 490, 200, stroke='#7AA116'),
        icon('eb', 'eventbridge', 520, 120, label='EventBridge\n月次 Schedule', label_w=120),
        icon('ecr', 'ecr', 680, 80, label='ECR', label_w=60),
        icon('fg', 'fargate', 680, 180, label='Fargate\n(一時領域で圧縮)', label_w=140),
        icon('s3b2', 's3', 870, 120, label='S3 入/出力'),
        arrow_xy('c1', 585, 160, 680, 210, 'RunTask', color='#ED7100'),
        arrow_xy('c2', 705, 140, 705, 180, 'pull', dashed=True, color='#666'),
        arrow_xy('c3', 735, 210, 870, 155, ''),
        note('good', '✅ 正解 B+E: コンテナ化→Fargate。一時ストレージで圧縮、完了後リソース自動解放で月1回コストのみ',
             20, 320, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ EBS を月 1 回スナップショット/削除: 運用複雑化、スナップショット料金も継続',
             20, 380, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ Lambda: 15 分・10GB 制限。5TB 圧縮は不可能',
             510, 380, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Fargate 一時ストレージ: デフォルト 20GB、最大 200GB まで拡張可。大容量は S3 ストリーミング読み書き',
             20, 445, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'ec2-cron-to-fargate-eventbridge'
DIAGRAMS['SAP-173'] = make_sap_173


def make_sap_272():
    t = "SAP-272 / ECS タスクレベル: awsvpc + Security Group + Task Role"
    s = "タスクごとに ENI 払い出し、SG/IAM を最小権限で分離 (PCI DSS 準拠)"
    cells = [
        title(t), subtitle(s),
        # VPC
        group_rect('vpc', 'VPC', 20, 70, 960, 260, stroke='#248814'),
        # task1
        group_rect('t1', 'ECS Task (awsvpc): 商品カタログサービス', 50, 100, 280, 100, stroke='#ED7100'),
        icon('c1', 'ecs', 70, 120, label='Container', label_w=80),
        icon('sg1', 'identity_and_access_management', 210, 120, label='SG + Task Role\n(S3 Read のみ)', label_w=120),
        # task2
        group_rect('t2', 'ECS Task (awsvpc): 決済サービス (PCI)', 360, 100, 280, 100, stroke='#DD344C'),
        icon('c2', 'ecs', 380, 120, label='Container', label_w=80),
        icon('sg2', 'identity_and_access_management', 520, 120, label='SG + Task Role\n(DDB+KMS のみ)', label_w=130),
        # task3
        group_rect('t3', 'ECS Task (awsvpc): 注文履歴', 670, 100, 280, 100, stroke='#ED7100'),
        icon('c3', 'ecs', 690, 120, label='Container', label_w=80),
        icon('sg3', 'identity_and_access_management', 830, 120, label='SG + Task Role\n(RDS のみ)', label_w=120),
        # services
        icon('s3', 's3', 120, 230, label='S3\n商品画像'),
        icon('ddb', 'dynamodb', 450, 230, label='DynamoDB\n決済 (KMS)'),
        icon('rds', 'rds', 760, 230, label='RDS\n注文履歴'),
        arrow_xy('a1', 170, 170, 170, 230, ''),
        arrow_xy('a2', 500, 170, 500, 230, ''),
        arrow_xy('a3', 810, 170, 810, 230, ''),
        note('good', '✅ 正解 A+D: awsvpc モードでタスク単位 ENI → 各タスクに SG を直接アタッチ。Task Role で最小権限 IAM',
             20, 355, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ bridge モード: インスタンス単位 SG しか付与できず、同居タスク間の分離が甘い',
             20, 415, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ 1 つの広い IAM ロールを全タスクで共有: PCI DSS の最小権限原則に違反',
             510, 415, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 awsvpc は Fargate 必須・EC2 launch でもデフォルト推奨。タスク単位のネットワーク分離が PCI/HIPAA で標準',
             20, 480, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'ecs-awsvpc-sg-task-role'
DIAGRAMS['SAP-272'] = make_sap_272


def make_sap_259():
    t = "SAP-259 / コンテナ近代化: EC2 Kafka → Fargate + MSK + RDS Multi-AZ"
    s = "パブリック EC2 をマネージドに置換。ALB+Fargate / MSK / RDS MAZ で可用性とセキュリティを両立"
    cells = [
        title(t), subtitle(s),
        # before
        group_rect('before', 'BEFORE: パブリック EC2 + 自前 Kafka', 20, 80, 440, 210, stroke='#DD344C'),
        icon('ec2a', 'ec2', 50, 120, label='EC2 (Public)\nコンテナ', label_w=110),
        icon('ec2b', 'ec2', 180, 120, label='EC2 (Public)\nコンテナ', label_w=110),
        icon('kafka', 'ec2', 320, 120, label='EC2\nApache Kafka', label_w=110, color='#DD344C'),
        icon('rdsa', 'rds', 180, 230, label='RDS PostgreSQL\n(Single-AZ)', label_w=130),
        # after
        group_rect('after', 'AFTER: Fargate + MSK + RDS MAZ', 490, 80, 490, 210, stroke='#7AA116'),
        icon('alb', 'application_load_balancer', 510, 120, label='ALB'),
        icon('fg1', 'fargate', 620, 90, label='Fargate\nTask', label_w=70),
        icon('fg2', 'fargate', 620, 175, label='Fargate\nTask', label_w=70),
        icon('msk', 'eventbridge', 760, 90, label='Amazon MSK\n(マネージド Kafka)', label_w=130),
        icon('rdsm', 'rds', 760, 220, label='RDS Multi-AZ\n+ Read Replica', label_w=140),
        arrow_xy('c1', 560, 155, 620, 115, ''),
        arrow_xy('c2', 560, 165, 620, 200, ''),
        arrow_xy('c3', 675, 115, 760, 115, 'Publish'),
        arrow_xy('c4', 675, 200, 760, 240, 'Query'),
        note('good', '✅ 正解 A: Fargate(EKS/ECS)でコンテナのスケール、MSK で Kafka のマネージド化、RDS MAZ で DB 可用性',
             20, 320, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ EC2 のまま Auto Scaling: Kafka 管理・パッチ適用の工数が残存',
             20, 380, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ Kinesis Data Streams: Kafka 互換が必要なら MSK 一択 (API 互換性)',
             510, 380, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 近代化 3 点セット: コンテナ=Fargate、ブローカー=MSK/MQ、DB=RDS MAZ。運用工数を最大削減',
             20, 445, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'ec2-kafka-to-fargate-msk'
DIAGRAMS['SAP-259'] = make_sap_259


def make_sap_56():
    t = "SAP-56 / EKS 5xx トラブルシュート: Pod 遅延 / CrashLoopBackOff"
    s = "CloudFront 502/504 の原因切り分け: Pod レベルか ALB ターゲットか"
    cells = [
        title(t), subtitle(s),
        user_icon('u', 'グローバル\nユーザー', 30, 150),
        icon('cf', 'cloudfront', 130, 150, label='CloudFront\n+ WAF'),
        icon('alb', 'application_load_balancer', 280, 150, label='ALB\n(Health Check)'),
        # EKS
        group_rect('eks', 'Amazon EKS Cluster', 410, 80, 530, 250, stroke='#ED7100'),
        icon('pod1', 'eks', 440, 120, label='Pod OK\n(<1s)', label_w=80),
        icon('pod2', 'eks', 560, 120, label='Pod 遅延\n30秒超', label_w=90, color='#DD344C'),
        icon('pod3', 'eks', 680, 120, label='Pod OK', label_w=80),
        icon('pod4', 'eks', 810, 120, label='Pod\nCrashLoop\nBackOff', label_w=100, color='#DD344C'),
        icon('pod5', 'eks', 440, 240, label='Pod OK', label_w=80),
        icon('pod6', 'eks', 560, 240, label='Pod OK', label_w=80),
        icon('pod7', 'eks', 680, 240, label='Pod OK', label_w=80),
        icon('pod8', 'eks', 810, 240, label='Pod OK', label_w=80),
        arrow('a1', 'u', 'cf', ''),
        arrow('a2', 'cf', 'alb', ''),
        arrow_xy('a3', 335, 175, 440, 140, ''),
        arrow_xy('a4', 335, 175, 560, 140, '', color='#DD344C'),
        arrow_xy('a5', 335, 175, 810, 140, '', color='#DD344C'),
        note('good', '✅ 原因候補 A+B: ①一部 Pod レスポンス 30秒 →CF Origin Timeout(504)、②Pod CrashLoopBackOff →ALB ヘルスチェック失敗(502)',
             20, 340, w=960, h=50, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ CloudFront 自体の障害 / WAF ルール誤検知 は 403/503 の形で出やすく、502/504 の主要原因ではない',
             20, 400, w=960, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 5xx 切り分け: 502=Bad Gateway(Origin 応答異常)、504=Gateway Timeout(Origin 応答遅延)。CloudFront ログと ALB TargetResponseTime を突き合わせる',
             20, 455, w=960, h=50, fill='#FFF5EB', stroke='#FF9900'),
    ]
    return '\n'.join(cells), 'eks-5xx-troubleshoot'
DIAGRAMS['SAP-56'] = make_sap_56


def make_sap_175():
    t = "SAP-175 / ハイブリッド移行: Web=EC2/ALB, MQ=Amazon MQ, K8s=EKS"
    s = "既存プロトコル/コードを維持しつつ基盤だけマネージド化"
    cells = [
        title(t), subtitle(s),
        user_icon('u', 'EC/モバイル\nユーザー', 30, 150),
        icon('alb', 'application_load_balancer', 140, 150, label='ALB'),
        # Web tier
        group_rect('web', 'Web Tier (EC2 ASG from AMI)', 240, 100, 180, 140, stroke='#ED7100'),
        icon('ec2a', 'ec2', 270, 130, label='EC2', label_w=50),
        icon('ec2b', 'ec2', 350, 130, label='EC2', label_w=50),
        # MQ
        icon('mq', 'mq', 470, 150, label='Amazon MQ\n(RabbitMQ)'),
        # EKS
        group_rect('eks', 'Amazon EKS (K8s)', 600, 100, 360, 170, stroke='#ED7100'),
        icon('p1', 'eks', 630, 130, label='Pod\n注文', label_w=60),
        icon('p2', 'eks', 720, 130, label='Pod\n決済', label_w=60),
        icon('p3', 'eks', 810, 130, label='Pod\n在庫', label_w=60),
        icon('p4', 'eks', 870, 210, label='Pod\n発送', label_w=60),
        arrow('a1', 'u', 'alb', ''),
        arrow_xy('a2', 195, 170, 270, 150, ''),
        arrow_xy('a3', 410, 170, 470, 170, ''),
        arrow_xy('a4', 520, 170, 630, 150, 'AMQP'),
        note('good', '✅ 正解 D: AMQP プロトコル維持(RabbitMQ→MQ)、K8s コード維持(EKS)、Web は AMI→ASG でインフラのみマネージド化',
             20, 290, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ SQS/SNS 置換: アプリ側で AMQP → AWS API 書換えが発生。コード改修最小化の要件違反',
             20, 350, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ ECS へ K8s 移行: マニフェスト → タスク定義書換えで工数発生',
             510, 350, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 Amazon MQ は Apache ActiveMQ / RabbitMQ をマネージド提供。既存メッセージング互換で「持ち込み」可能',
             20, 415, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 EKS は Kubernetes 互換、ECS は AWS ネイティブ。既存 K8s 資産があるなら EKS、新規なら ECS がシンプル',
             20, 465, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'ec2-mq-eks-migration'
DIAGRAMS['SAP-175'] = make_sap_175


def make_sap_91():
    t = "SAP-91 / マルチリージョン DR: APIGW + Lambda + DynamoDB Global Table + R53 Failover"
    s = "Route 53 ヘルスチェックで自動切替。コード変更なしで 99.9% SLA"
    cells = [
        title(t), subtitle(s),
        user_icon('u', 'モバイル\nクライアント', 30, 170),
        icon('r53', 'route_53', 140, 170, label='Route 53\nFailover + HC\nweather.example.com', label_w=150),
        # Primary region
        group_rect('pri', 'Primary Region (ap-northeast-1)', 320, 70, 320, 150, stroke='#7AA116'),
        icon('apip', 'api_gateway', 345, 110, label='API GW\n(Primary)', label_w=80),
        icon('lamp', 'lambda', 470, 110, label='Lambda\n(Primary)', label_w=80),
        icon('ddbp', 'dynamodb', 570, 110, label='DDB\nGlobal Table'),
        # Secondary region
        group_rect('sec', 'Secondary Region (us-west-2)', 320, 250, 320, 150, stroke='#3B48CC'),
        icon('apis', 'api_gateway', 345, 290, label='API GW\n(Secondary)', label_w=100),
        icon('lams', 'lambda', 470, 290, label='Lambda\n(Secondary)', label_w=90),
        icon('ddbs', 'dynamodb', 570, 290, label='DDB\nGlobal Table'),
        # replication
        arrow_xy('repl', 595, 170, 595, 290, 'グローバル\nレプリ', color='#8C4FFF', dashed=True),
        arrow('a1', 'u', 'r53', ''),
        arrow_xy('a2', 230, 180, 345, 140, 'Primary (Healthy)', color='#7AA116'),
        arrow_xy('a3', 230, 200, 345, 310, 'Secondary (FO)', color='#DD344C', dashed=True),
        arrow('a4', 'apip', 'lamp', ''),
        arrow('a5', 'lamp', 'ddbp', ''),
        arrow('a6', 'apis', 'lams', ''),
        arrow('a7', 'lams', 'ddbs', ''),
        note('good', '✅ 正解 A: APIGW+Lambda をセカンダリにも複製、DDB Global Table で双方向レプリ、R53 Failover+HC で自動切替',
             20, 415, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('tip', '📌 DDB Global Table は最終整合性。短時間の書込み競合は Last Writer Wins で解決',
             20, 475, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
    ]
    return '\n'.join(cells), 'apigw-lambda-ddb-global-r53'
DIAGRAMS['SAP-91'] = make_sap_91


def make_sap_250():
    t = "SAP-250 / リージョン増設: APIGW リージョナル + Lambda + DDB Global Table"
    s = "別リージョンに複製し両リージョン読み書き可能に"
    cells = [
        title(t), subtitle(s),
        # Primary
        group_rect('pri', 'Primary Region (eu-west-1)', 40, 90, 420, 180, stroke='#7AA116'),
        user_icon('u1', '欧州\n顧客', 60, 160),
        icon('api1', 'api_gateway', 160, 150, label='API GW\nRegional'),
        icon('lam1', 'lambda', 290, 150, label='Lambda\n検索処理'),
        icon('ddb1', 'dynamodb', 420, 150, label='DynamoDB\nGlobal Table', label_w=120),
        # Secondary
        group_rect('sec', 'New Region (us-east-1)', 530, 90, 420, 180, stroke='#3B48CC'),
        user_icon('u2', '北米\n航空会社', 550, 160),
        icon('api2', 'api_gateway', 640, 150, label='API GW\nRegional'),
        icon('lam2', 'lambda', 770, 150, label='Lambda\n検索処理'),
        icon('ddb2', 'dynamodb', 890, 150, label='DynamoDB\nGlobal Table', label_w=120),
        arrow_xy('repl', 470, 170, 940, 170, 'Global Table 双方向レプリ', color='#8C4FFF', dashed=True),
        arrow('a1', 'u1', 'api1', ''),
        arrow('a2', 'api1', 'lam1', ''),
        arrow('a3', 'lam1', 'ddb1', ''),
        arrow('a4', 'u2', 'api2', ''),
        arrow('a5', 'api2', 'lam2', ''),
        arrow('a6', 'lam2', 'ddb2', ''),
        note('good', '✅ 正解 C+D: us-east-1 にも API GW/Lambda を複製、DDB を Global Table 化 → 両リージョン読み書き',
             20, 320, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ API Gateway Edge-Optimized: CloudFront で配信するが、バックエンドは単一リージョンのまま。障害時に切替不可',
             20, 380, w=470, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ DDB クロスリージョンレプリケーション(旧): 非推奨。Global Table が公式',
             510, 380, w=470, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Latency-based Routing を R53 で組めば、ユーザーの最寄りリージョン API へ自動振り分け',
             20, 450, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'multi-region-apigw-global-table'
DIAGRAMS['SAP-250'] = make_sap_250


def make_sap_271():
    t = "SAP-271 / API Gateway AWS_IAM 認可 + X-Ray 分散トレース"
    s = "IAM 署名付きリクエストのみ許可、API→バックエンド間を可視化"
    cells = [
        title(t), subtitle(s),
        user_icon('u', 'IAM User/Role\n(SigV4)', 30, 150),
        icon('apigw', 'api_gateway', 160, 150, label='API Gateway\n(Auth: AWS_IAM)'),
        icon('lam', 'lambda', 330, 150, label='Lambda\n(X-Ray SDK)'),
        icon('svc1', 'dynamodb', 500, 90, label='DynamoDB', label_w=90),
        icon('svc2', 'rds', 500, 210, label='RDS', label_w=60),
        icon('xray', 'x_ray', 720, 150, label='X-Ray\n(サービスマップ)', label_w=130),
        arrow('a1', 'u', 'apigw', 'SigV4 Signed'),
        arrow('a2', 'apigw', 'lam', ''),
        arrow_xy('a3', 385, 150, 500, 115, 'trace'),
        arrow_xy('a4', 385, 170, 500, 225, 'trace'),
        arrow_xy('a5', 215, 210, 720, 210, 'segments', color='#E7157B', dashed=True),
        arrow_xy('a6', 385, 210, 720, 210, 'segments', color='#E7157B', dashed=True),
        note('good', '✅ 正解 A: execute-api 権限持つ IAM のみ許可(SigV4)、X-Ray で API GW〜バックエンドのトレース取得',
             20, 290, w=960, h=46, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ Cognito オーソライザー: エンドユーザー向け JWT 認証。AWS アカウント内部の IAM 認可要件に不適',
             20, 350, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ API キーのみ: 使用量制御用途。認証/認可の強度が低く、署名なしでリプレイ可能',
             510, 350, w=470, h=50, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 API Gateway 認可タイプ: NONE / AWS_IAM / COGNITO_USER_POOLS / CUSTOM(Lambda Authorizer)',
             20, 415, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 X-Ray はステージで有効化 → Lambda SDK を入れれば API→Lambda→DDB の E2E レイテンシが見える',
             20, 465, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'apigw-iam-auth-xray'
DIAGRAMS['SAP-271'] = make_sap_271


# ===== Main =====
def main():
    count = 0
    for qid, fn in DIAGRAMS.items():
        content, name = fn()
        xml = drawio_wrap(content, name, qid)
        outfile = OUT / f'{qid}.drawio'
        if outfile.exists():
            print(f'SKIP (exists): {outfile}')
            continue
        outfile.write_text(xml, encoding='utf-8')
        count += 1
        print(f'Wrote: {outfile}')
    print(f'\nTotal new drawio: {count}')


if __name__ == '__main__':
    main()
