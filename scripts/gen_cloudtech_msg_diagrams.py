#!/usr/bin/env python3
"""
Generate per-question drawio files for CloudTech msg/stream/pipeline category.
1000x600 canvas, white background, AWS official colors, 50x50 icons (label at icon.y+58).
Does NOT overwrite existing drawio files.
"""
import os
from pathlib import Path

OUT = Path('/Users/aki/aws-sap/docs/diagrams/per-question')
OUT.mkdir(parents=True, exist_ok=True)

# ---------- Base helpers ----------
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

def title(text, y=20):
    return f'''<mxCell id="title" value="{text}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;fontColor=#232F3E;" vertex="1" parent="1">
  <mxGeometry x="20" y="{y}" width="960" height="30" as="geometry" />
</mxCell>'''

def subtitle(text, x=20, y=52, w=960, h=22):
    return f'''<mxCell id="subtitle_{x}_{y}" value="{text}" style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=11;fontColor=#666666;fontStyle=2;" vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>'''

ICON_COLOR = {
    'eventbridge':       '#E7157B',
    'sns':               '#E7157B',
    'sqs':               '#E7157B',
    'lambda':            '#ED7100',
    'step_functions':    '#E7157B',
    'kinesis_data_streams': '#8C4FFF',
    'kinesis_data_firehose': '#8C4FFF',
    'kinesis_data_analytics': '#8C4FFF',
    's3':                '#7AA116',
    'dynamodb':          '#3B48CC',
    'glue':              '#8C4FFF',
    'athena':            '#8C4FFF',
    'api_gateway':       '#E7157B',
    'ec2':               '#ED7100',
    'ecs':               '#ED7100',
    'cloudfront':        '#8C4FFF',
    'cloudwatch':        '#E7157B',
    'cloudtrail':        '#E7157B',
    'iam':               '#C925D1',
    'iot_core':          '#3B48CC',
    'opensearch_service':'#005F83',
    'redshift':          '#3B48CC',
    'emr':               '#8C4FFF',
    'rds':               '#3B48CC',
    'ecr':               '#ED7100',
    'auto_scaling':      '#ED7100',
    'rekognition':       '#4D72F3',
    'route_53':          '#8C4FFF',
}

def icon(id_, res_icon, x, y, label=None, w=50, h=50, color=None):
    fill = color or ICON_COLOR.get(res_icon, '#E7157B')
    elems = []
    style = (f"sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;"
             f"fillColor={fill};strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;"
             f"verticalAlign=top;align=center;html=1;fontSize=10;fontStyle=0;aspect=fixed;"
             f"shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{res_icon};")
    elems.append(f'''<mxCell id="{id_}" value="" style="{style}" vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>''')
    if label:
        ly = y + 58
        elems.append(f'''<mxCell id="{id_}_l" value="{label}" style="text;html=1;align=center;verticalAlign=top;whiteSpace=wrap;fontSize=10;fontColor=#232F3E;" vertex="1" parent="1">
  <mxGeometry x="{x-25}" y="{ly}" width="{w+50}" height="28" as="geometry" />
</mxCell>''')
    return '\n'.join(elems)

def generic(id_, value, x, y, w=100, h=46, fill='#F2F2F2', stroke='#666666', font_size=10):
    return f'''<mxCell id="{id_}" value="{value}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize={font_size};fontColor=#232F3E;verticalAlign=middle;align=center;" vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>'''

def arrow(id_, src, tgt, label='', color='#232F3E', dashed=False):
    style = f"endArrow=classic;html=1;strokeColor={color};strokeWidth=2;fontSize=10;fontColor=#232F3E;"
    if dashed:
        style += "dashed=1;"
    lbl = f'value="{label}"' if label else 'value=""'
    return f'''<mxCell id="{id_}" {lbl} style="{style}" edge="1" parent="1" source="{src}" target="{tgt}">
  <mxGeometry relative="1" as="geometry" />
</mxCell>'''

def note(id_, text, x, y, w=960, h=50, fill='#FFF5EB', stroke='#FF9900'):
    return f'''<mxCell id="{id_}" value="{text}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize=11;fontStyle=1;fontColor=#232F3E;verticalAlign=middle;align=left;spacingLeft=10;spacingRight=10;" vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>'''

def group_rect(id_, label, x, y, w, h, stroke='#4D72F3', fill='none'):
    return f'''<mxCell id="{id_}" value="{label}" style="rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=2;fontSize=11;fontStyle=1;fontColor={stroke};verticalAlign=top;align=left;spacingLeft=8;spacingTop=4;dashed=1;" vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>'''


# ---------- Diagrams ----------
def d_sap_7():
    t = "SAP-7 / 注文スパイク対応: API Gateway → SQS → Lambda → DynamoDB + DLQ"
    s = "フルマネージド・疎結合・失敗再処理の三点で数十倍スパイクを吸収"
    cells = [
        title(t), subtitle(s),
        generic('u', 'User / Mobile', 40, 145, fill='#E8F2FD', stroke='#3B48CC'),
        icon('api', 'api_gateway', 170, 135, label='API Gateway'),
        icon('sqs', 'sqs', 320, 135, label='SQS Queue\n(バッファ)'),
        icon('lam', 'lambda', 470, 135, label='Order Lambda\n(自動スケール)'),
        icon('ddb', 'dynamodb', 620, 135, label='DynamoDB\n(On-Demand)'),
        icon('dlq', 'sqs', 470, 290, label='Dead Letter Queue\n(失敗注文)', color='#DD344C'),
        icon('sns', 'sns', 620, 290, label='SNS → Ops'),
        arrow('a1', 'u', 'api', '注文'),
        arrow('a2', 'api', 'sqs', 'SendMessage'),
        arrow('a3', 'sqs', 'lam', 'ESM'),
        arrow('a4', 'lam', 'ddb', 'PutItem'),
        arrow('a5', 'lam', 'dlq', '失敗→隔離', color='#DD344C'),
        arrow('a6', 'dlq', 'sns', '通知'),
        note('good', '✅ 正解: SQS でスパイクをバッファ → Lambda が自動スケールで処理 → DLQ で失敗注文を捕捉して後から再処理',
             20, 370, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ EC2 手動スケール: スパイク追従が遅い / ❌ 同期 API 直接 DynamoDB 書込: 失敗が即エラー、再処理機構なし',
             20, 430, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 「バッファ + 自動スケール + DLQ」= SAP での疎結合の王道。DLQ は本番とは別の監視・再処理対象',
             20, 490, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sap7-sqs-lambda-dlq'


def d_sap_14():
    t = "SAP-14 / 水位センサー可視化: IoT Core → Firehose → Lambda 変換 → S3 → Athena"
    s = "サーバーレスで SQL 分析 — アナリストは既存 SQL スキルを継続利用できる"
    cells = [
        title(t), subtitle(s),
        generic('sens', '1万台超\n水位センサー', 40, 140, fill='#E8F2FD', stroke='#3B48CC'),
        icon('iot', 'iot_core', 180, 130, label='IoT Core\n(Rules)'),
        icon('fh', 'kinesis_data_firehose', 340, 130, label='Firehose\n(バッファ)'),
        icon('lam', 'lambda', 500, 130, label='Transform Lambda\n(可読変換)'),
        icon('s3', 's3', 660, 130, label='S3\n(Parquet)'),
        icon('ath', 'athena', 820, 130, label='Athena\n(SQL)'),
        generic('bi', 'ダッシュボード\n(QuickSight)', 820, 290, fill='#E8F5E9', stroke='#7AA116'),
        arrow('a1', 'sens', 'iot', 'MQTT'),
        arrow('a2', 'iot', 'fh', 'Rule'),
        arrow('a3', 'fh', 'lam', 'invoke', dashed=True),
        arrow('a4', 'lam', 'fh', 'transformed', dashed=True),
        arrow('a5', 'fh', 's3'),
        arrow('a6', 's3', 'ath'),
        arrow('a7', 'ath', 'bi'),
        note('good', '✅ 正解: 完全サーバーレスで取り込み・変換・永続化・SQL 分析を統合。運用/パッチ/スケール全てマネージド',
             20, 370, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ EC2 上でストリーム受信: パッチ/スケール自前 / ❌ RDS 直書き: 10k+ センサー書込でスループット不足',
             20, 430, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 Firehose は最小 60s or 1MB バッファ。リアルタイム (ms) 要件なら Kinesis Data Streams を選ぶ',
             20, 490, fill='#FFF5EB', stroke='#FF9900'),
    ]
    return '\n'.join(cells), 'sap14-iot-firehose-athena'


def d_sap_69():
    t = "SAP-69 / 終了前ログ保全: ASG ライフサイクルフック + EventBridge + SSM Run Command"
    s = "Terminating 遷移を一時停止し、S3 転送完了後に解除する確実なパターン"
    cells = [
        title(t), subtitle(s),
        generic('asg', 'Auto Scaling\nGroup (EC2)', 40, 140, fill='#FFF5EB', stroke='#FF9900'),
        generic('hook', 'Lifecycle Hook\n(Terminating:Wait)', 180, 140, fill='#FFF5EB', stroke='#FF9900'),
        icon('eb', 'eventbridge', 340, 130, label='EventBridge\n(Hook Event)'),
        generic('ssm', 'SSM Run\nCommand', 480, 140, fill='#E7157B', stroke='#E7157B', font_size=10),
        icon('ec2', 'ec2', 620, 130, label='EC2\n(ログコピー)'),
        icon('s3', 's3', 780, 130, label='S3\n(中央ログ)'),
        arrow('a1', 'asg', 'hook', '終了発生'),
        arrow('a2', 'hook', 'eb', 'HookEvent'),
        arrow('a3', 'eb', 'ssm', 'invoke'),
        arrow('a4', 'ssm', 'ec2', 'exec'),
        arrow('a5', 'ec2', 's3', 'log 転送'),
        arrow('a6', 'ec2', 'hook', 'complete-\nlifecycle-action', color='#7AA116'),
        note('good', '✅ 正解: Hook で終了を遷移停止 → EventBridge が SSM Document を発火 → ログ完了後に complete コール',
             20, 300, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ 5 分間隔コピー短縮: 終了タイミング次第で欠落',
             20, 360, w=470, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ SNS 通知 + 手動対応: 自動化の崩壊',
             510, 360, w=470, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Terminating:Wait 中のインスタンスはタイムアウト (最大 100 min) まで待機可能。タイムアウト超過で自動終了',
             20, 420, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '📌 EventBridge → SSM パターンは「終了前処理」の鉄板。Lambda でも可だが Run Command が EC2 内で実行できて直感的',
             20, 480, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sap69-asg-lifecycle-hook-ssm'


def d_sap_105():
    t = "SAP-105 / SQS 誤 DLQ 行き: スケールイン保護で処理中ワーカー継続"
    s = "maxReceiveCount=1 + スケールインで受信カウント超過 → DLQ 誤検知の根本原因を断つ"
    cells = [
        title(t), subtitle(s),
        icon('sqs', 'sqs', 40, 140, label='SQS Queue\n(可視性 60min)'),
        generic('asg', 'EC2 Auto Scaling\nGroup (Worker)', 200, 145, fill='#FFF5EB', stroke='#FF9900'),
        icon('ec2', 'ec2', 360, 140, label='Worker EC2\n(30 min 処理)'),
        generic('prot', 'スケールイン保護\n(処理中のみ)', 510, 145, fill='#EAF5E0', stroke='#7AA116'),
        icon('dlq', 'sqs', 680, 140, label='DLQ\n(maxReceive=1)', color='#DD344C'),
        icon('cw', 'cloudwatch', 820, 140, label='CloudWatch\nAlarm'),
        arrow('a1', 'sqs', 'ec2', 'poll'),
        arrow('a2', 'asg', 'ec2', 'scale'),
        arrow('a3', 'ec2', 'prot', 'set protected', color='#7AA116'),
        arrow('a4', 'prot', 'sqs', 'Delete 正常完了', color='#7AA116'),
        arrow('a5', 'sqs', 'dlq', '未処理→受信超過', dashed=True, color='#DD344C'),
        arrow('a6', 'dlq', 'cw', '誤報が増える', dashed=True, color='#DD344C'),
        note('prob', '❌ 問題: スケールインで処理中ワーカーが終了 → メッセージが再度 Visible → 次ワーカーが受信 → maxReceive=1 超過 → DLQ 送り',
             20, 310, fill='#FDECEA', stroke='#DD344C'),
        note('good', '✅ 正解 D: 処理中インスタンスにスケールイン保護 → Auto Scaling 終了対象から除外 → 処理完了後に解除',
             20, 370, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ maxReceive を上げる = 問題の先送り / ❌ 終了保護 = API/コンソール終了のみ ASG スケールインには効かず / ❌ 可視性延長 = 根本未解決',
             20, 430, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 「Instance Scale-In Protection」と「Termination Protection」は別モノ。ASG 終了対策は前者のみ有効',
             20, 490, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sap105-scale-in-protection-sqs'


def d_sap_108():
    t = "SAP-108 / NAT GW コスト削減: Kinesis VPC Interface Endpoint"
    s = "プライベート EC2 → Kinesis Data Streams の通信を VPC 内で完結させる"
    cells = [
        title(t), subtitle(s),
        group_rect('vpc', 'VPC', 30, 90, 700, 410, stroke='#4D72F3'),
        group_rect('pub', 'Public Subnet', 50, 130, 300, 150, stroke='#888'),
        generic('natgw', 'NAT Gateway\n(高額な転送料金)', 90, 180, fill='#FDECEA', stroke='#DD344C'),
        group_rect('priv', 'Private Subnet', 50, 300, 660, 180, stroke='#888'),
        icon('ec2', 'ec2', 90, 340, label='App EC2'),
        icon('vpce', 'api_gateway', 280, 340, label='Interface VPC\nEndpoint (Kinesis)', color='#005F83'),
        icon('kds', 'kinesis_data_streams', 770, 130, label='Kinesis Data\nStreams'),
        arrow('a1', 'ec2', 'natgw', '❌ 旧: 高額', dashed=True, color='#DD344C'),
        arrow('a2', 'natgw', 'kds', 'NAT 課金', dashed=True, color='#DD344C'),
        arrow('a3', 'ec2', 'vpce', '✅ 新: 内部経由', color='#7AA116'),
        arrow('a4', 'vpce', 'kds', 'PrivateLink', color='#7AA116'),
        note('good', '✅ 正解 A: Kinesis Data Streams 用の Interface VPC Endpoint (PrivateLink) を作成しプライベート DNS 有効化 → NAT 経由をバイパス',
             20, 510, fill='#EAF5E0', stroke='#7AA116'),
    ]
    return '\n'.join(cells), 'sap108-kinesis-vpc-endpoint'


def d_sap_135():
    t = "SAP-135 / Athena クエリ高速化: Firehose → S3 (日付パーティション + Parquet/Snappy)"
    s = "パーティションプルーニング + 列指向 + 圧縮の 3 重効果でスキャン量 10% 以下に"
    cells = [
        title(t), subtitle(s),
        generic('waf', 'AWS WAF\nLogs', 40, 140, fill='#FDECEA', stroke='#DD344C'),
        icon('fh', 'kinesis_data_firehose', 180, 130, label='Firehose\n(Parquet 変換)'),
        icon('s3', 's3', 340, 130, label='S3\n(dt=YYYY-MM-DD)'),
        icon('ath', 'athena', 500, 130, label='Athena\n(MSCK REPAIR)'),
        generic('sec', 'Sec チーム\n毎朝 24h 集計', 660, 140, fill='#E8F2FD', stroke='#3B48CC'),
        arrow('a1', 'waf', 'fh'),
        arrow('a2', 'fh', 's3', '日毎 partition'),
        arrow('a3', 's3', 'ath', 'Partition Prune'),
        arrow('a4', 'ath', 'sec'),
        note('good', '✅ 正解 D: (1) Firehose で日付パーティション出力 → (2) Parquet + Snappy 圧縮で列指向化 → (3) Athena は対象日のみスキャン',
             20, 260, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ パーティション再設計だけ: 行指向 JSON の非効率は残る',
             20, 320, w=470, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ Athena → Redshift: オーバースペック+コスト増',
             510, 320, w=470, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 Athena コスト = スキャンされた $5/TB。スキャン量削減の 3 大テク: (A) パーティション、(B) 列指向 (Parquet/ORC)、(C) 圧縮',
             20, 380, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 Firehose は Parquet/ORC 変換 + 動的パーティショニングをネイティブサポート (Lambda 変換無しで完結)',
             20, 440, fill='#E8F2FD', stroke='#3B48CC'),
        note('tip3', '⚠️ 列指向にしても SELECT * は全列読む → 必要列だけ指定することも重要',
             20, 500, fill='#FFF5EB', stroke='#FF9900'),
    ]
    return '\n'.join(cells), 'sap135-firehose-parquet-athena'


def d_sap_141():
    t = "SAP-141 / マルチリージョン Fan-out: SNS クロスリージョン → 各リージョン SQS + Lambda"
    s = "単一 SNS ハブから複数リージョンへネイティブサブスク — 書込先 S3 は既存リージョンへ集約"
    cells = [
        title(t), subtitle(s),
        group_rect('r1', 'Region A (ハブ)', 30, 90, 260, 400, stroke='#3B48CC'),
        generic('urlsrc', 'URL 投入\n(コンテンツ管理)', 50, 130, fill='#E8F2FD', stroke='#3B48CC'),
        icon('sns', 'sns', 110, 220, label='SNS Topic\n(Cross-Region Sub)'),
        icon('s3', 's3', 110, 380, label='S3\n(抽出結果を集約)'),
        group_rect('r2', 'Region B', 320, 90, 200, 400, stroke='#7AA116'),
        icon('sqs2', 'sqs', 370, 150, label='SQS (B)'),
        icon('lam2', 'lambda', 370, 260, label='Lambda (B)\n抽出処理'),
        group_rect('r3', 'Region C', 550, 90, 200, 400, stroke='#7AA116'),
        icon('sqs3', 'sqs', 600, 150, label='SQS (C)'),
        icon('lam3', 'lambda', 600, 260, label='Lambda (C)'),
        group_rect('r4', 'Region D', 780, 90, 200, 400, stroke='#7AA116'),
        icon('sqs4', 'sqs', 830, 150, label='SQS (D)'),
        icon('lam4', 'lambda', 830, 260, label='Lambda (D)'),
        arrow('a1', 'urlsrc', 'sns', 'publish'),
        arrow('b1', 'sns', 'sqs2', 'X-Region Sub'),
        arrow('b2', 'sns', 'sqs3', 'X-Region Sub'),
        arrow('b3', 'sns', 'sqs4', 'X-Region Sub'),
        arrow('c1', 'sqs2', 'lam2', ''),
        arrow('c2', 'sqs3', 'lam3', ''),
        arrow('c3', 'sqs4', 'lam4', ''),
        arrow('d1', 'lam2', 's3', 'put'),
        arrow('d2', 'lam3', 's3', 'put'),
        arrow('d3', 'lam4', 's3', 'put'),
        note('tip', '✅ 正解 B+D: SNS → 各リージョン SQS (ネイティブ X-Region Sub) / 各リージョンに SQS+Lambda を展開 → ローカル処理',
             20, 510, fill='#EAF5E0', stroke='#7AA116'),
    ]
    return '\n'.join(cells), 'sap141-sns-xregion-sqs-lambda'


def d_sap_144():
    t = "SAP-144 / マルチアカウント集中ログ: CW Logs → Firehose → OpenSearch (ニアリアル)"
    s = "CloudWatch Logs サブスクリプションフィルタをクロスアカウントで Firehose に流し込む"
    cells = [
        title(t), subtitle(s),
        group_rect('a1', 'App Account 1', 30, 100, 220, 180),
        icon('ct1', 'cloudtrail', 60, 140, label='CloudTrail'),
        icon('cwl1', 'cloudwatch', 170, 140, label='CW Logs'),
        arrow('p1', 'ct1', 'cwl1', ''),
        group_rect('a2', 'App Account 2', 30, 300, 220, 180),
        icon('ct2', 'cloudtrail', 60, 340, label='VPC Flow Logs'),
        icon('cwl2', 'cloudwatch', 170, 340, label='CW Logs'),
        arrow('p2', 'ct2', 'cwl2', ''),
        group_rect('log', 'Logging Account', 300, 100, 660, 380, stroke='#7AA116'),
        generic('sub', 'Subscription Filter\n(Cross-Account)', 320, 230, w=160, h=50, fill='#FFF5EB', stroke='#FF9900'),
        icon('fh', 'kinesis_data_firehose', 520, 220, label='Firehose'),
        icon('os', 'opensearch_service', 680, 220, label='OpenSearch\nService'),
        generic('sec', 'Security Dashboards\n(5 min 対応)', 840, 230, w=110, h=50, fill='#E8F5E9', stroke='#005F83'),
        arrow('b1', 'cwl1', 'sub', ''),
        arrow('b2', 'cwl2', 'sub', ''),
        arrow('b3', 'sub', 'fh', ''),
        arrow('b4', 'fh', 'os', ''),
        arrow('b5', 'os', 'sec', ''),
        note('good', '✅ 正解 D: CW Logs クロスアカウントサブスクリプションで Firehose → OpenSearch へ直接ストリーミング。5 分 SLA を達成',
             20, 500, fill='#EAF5E0', stroke='#7AA116'),
    ]
    return '\n'.join(cells), 'sap144-xacct-cwlogs-firehose-opensearch'


def d_sap_154():
    t = "SAP-154 / 静的・動画分離: CloudFront+S3 + S3 Event → SQS → Lambda"
    s = "スパイクするフロントは CloudFront 配信、重い動画処理は非同期サーバーレスで剥がす"
    cells = [
        title(t), subtitle(s),
        generic('u', 'User', 40, 145, w=80, fill='#E8F2FD', stroke='#3B48CC'),
        icon('cf', 'cloudfront', 140, 135, label='CloudFront'),
        icon('s3s', 's3', 280, 135, label='S3 (静的 HTML\n/ サムネイル)'),
        icon('s3v', 's3', 440, 135, label='S3 (投稿動画)'),
        icon('sqs', 'sqs', 600, 135, label='SQS\n(非同期)'),
        icon('lam', 'lambda', 760, 135, label='Lambda\n(解析・分類)'),
        icon('ddb', 'dynamodb', 900, 135, label='DynamoDB\n(メタ)', w=50, h=50),
        arrow('a1', 'u', 'cf', ''),
        arrow('a2', 'cf', 's3s', 'cache'),
        arrow('a3', 'u', 's3v', 'upload'),
        arrow('a4', 's3v', 'sqs', 'S3 Event'),
        arrow('a5', 'sqs', 'lam', 'ESM'),
        arrow('a6', 'lam', 'ddb', 'tag'),
        note('good', '✅ 正解 D: スパイクする静的 = CloudFront/S3 / 重い処理 = S3 Event → SQS → Lambda の非同期分離。EC2 ASG 廃止で運用負荷激減',
             20, 290, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ Beanstalk のまま: EC2 静的配信のスパイクコスト残存 / ❌ 動画を EBS に保持: スケールとコスト面で不利',
             20, 350, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 「静的」= エッジキャッシュへ / 「非同期」= キュー + Lambda が SAP の基本方針',
             20, 410, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 S3 → SQS は 直接イベント通知可 (2021~)。Lambda 直バインドより「バッファ + 再試行 + DLQ」が追加可能で堅牢',
             20, 470, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sap154-cf-s3-sqs-lambda'


def d_sap_161():
    t = "SAP-161 / 毒メッセージ隔離: SQS 標準キュー + maxReceiveCount → DLQ"
    s = "1 件の異常メッセージで全キューが止まる古典問題 — Redrive Policy で隔離する"
    cells = [
        title(t), subtitle(s),
        generic('prod', 'Order API\n(Producer)', 40, 145, fill='#FFF5EB', stroke='#FF9900'),
        icon('main', 'sqs', 170, 135, label='Main SQS\n(VisTO 30s)'),
        icon('cons', 'lambda', 320, 135, label='Order Consumer'),
        icon('ddb', 'dynamodb', 470, 135, label='DynamoDB'),
        icon('dlq', 'sqs', 320, 290, label='DLQ\n(maxReceive=5)', color='#DD344C'),
        icon('cw', 'cloudwatch', 470, 290, label='CloudWatch\nAlarm'),
        icon('sns', 'sns', 620, 290, label='SNS → Ops'),
        arrow('a1', 'prod', 'main', ''),
        arrow('a2', 'main', 'cons', 'poll'),
        arrow('a3', 'cons', 'ddb', ''),
        arrow('a4', 'main', 'dlq', '5 回失敗→隔離', color='#DD344C'),
        arrow('a5', 'dlq', 'cw', '深度監視'),
        arrow('a6', 'cw', 'sns', '通知'),
        note('good', '✅ 正解 A: Redrive Policy で maxReceiveCount を設定 → 超過メッセージを自動で DLQ へ → 本番キュー継続 + 隔離調査が両立',
             20, 370, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ エラーログ記録だけ: 毒メッセージがキューに残存 / ❌ VisTO 延長: 隔離されず詰まりは解消しない',
             20, 430, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 DLQ は「同じ種類」(Standard/FIFO) を指定。maxReceiveCount はビジネスリトライ許容回数に合わせる',
             20, 490, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sap161-sqs-dlq-redrive'


def d_sap_176():
    t = "SAP-176 / 遺伝子リアルタイム: Kinesis Data Streams → Lambda → Redshift + S3"
    s = "毎秒 8KB × N デバイス。即時集計 + 生データ永続化 + DWH 集約の三本立て"
    cells = [
        title(t), subtitle(s),
        generic('dev', '遺伝子スキャナ\n(多数デバイス)', 40, 140, fill='#E8F2FD', stroke='#3B48CC'),
        icon('kds', 'kinesis_data_streams', 200, 130, label='Kinesis Data\nStreams'),
        icon('lam', 'lambda', 360, 130, label='Aggregator\nLambda'),
        icon('rs', 'redshift', 520, 130, label='Redshift\n(集計 DWH)'),
        generic('dash', 'BI Dashboard\n(QuickSight)', 680, 140, fill='#E8F5E9', stroke='#7AA116'),
        icon('fh', 'kinesis_data_firehose', 360, 290, label='Firehose'),
        icon('s3', 's3', 520, 290, label='S3\n(生データ耐久)'),
        arrow('a1', 'dev', 'kds'),
        arrow('a2', 'kds', 'lam', 'KCL'),
        arrow('a3', 'lam', 'rs', 'write'),
        arrow('a4', 'rs', 'dash'),
        arrow('a5', 'kds', 'fh', '並列 consumer'),
        arrow('a6', 'fh', 's3', 'archive'),
        note('good', '✅ 正解 A: KDS で取込 → Lambda 集計 → Redshift で BI。並列 consumer として Firehose 経由で生データも S3 永続化',
             20, 370, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ バッチ S3 経由 Redshift COPY: 「ほぼ即時」の要件を満たさない / ❌ SQS+RDS: 時系列分析や高スループット取込に不向き',
             20, 430, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 KDS は Enhanced Fan-out で複数 Consumer の並列スループット確保。データ保持 24h〜365 日で再処理も可能',
             20, 490, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sap176-kds-lambda-redshift'


def d_sap_204():
    t = "SAP-204 / DynamoDB 監査 30 分 SLA: DynamoDB Streams → Lambda → Firehose → S3"
    s = "テーブルの全変更 (挿入/更新/削除) を順序保証で捕捉 — フルマネージド改ざん防止"
    cells = [
        title(t), subtitle(s),
        generic('app', 'EC App\n(購入 API)', 40, 145, fill='#FFF5EB', stroke='#FF9900'),
        icon('ddb', 'dynamodb', 180, 135, label='DynamoDB\n(単一テーブル)'),
        generic('str', 'DynamoDB\nStreams', 330, 145, fill='#3B48CC', stroke='#3B48CC', font_size=10),
        icon('lam', 'lambda', 470, 135, label='Lambda\n(整形)'),
        icon('fh', 'kinesis_data_firehose', 620, 135, label='Firehose'),
        icon('s3', 's3', 770, 135, label='S3 (監査)\nVersioning'),
        icon('ath', 'athena', 900, 135, label='Athena\n(監査クエリ)', w=50, h=50),
        arrow('a1', 'app', 'ddb', 'Put/Update/Del'),
        arrow('a2', 'ddb', 'str', '全変更'),
        arrow('a3', 'str', 'lam', 'ESM'),
        arrow('a4', 'lam', 'fh'),
        arrow('a5', 'fh', 's3', '継続保存'),
        arrow('a6', 's3', 'ath'),
        note('good', '✅ 正解 D: DynamoDB Streams が挿入・更新・削除を順序保証で捕捉できる唯一の仕組み。S3 バージョニングで改ざん防止も達成',
             20, 300, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ CloudTrail: API レベルで変更前後値は記録されない',
             20, 360, w=470, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ EventBridge 単体: テーブルアイテム変更を直接イベント化できない',
             510, 360, w=470, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 DynamoDB Streams 保持 24h。Lambda は最大 12 h 遅延まで許容。Kinesis Data Streams アダプタで並列 consumer も可',
             20, 420, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 30 分 SLA は Streams + Lambda + Firehose buffer (max 900s) で充分達成可能',
             20, 480, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sap204-ddb-streams-lambda-firehose'


def d_sap_245():
    t = "SAP-245 / 5 分 SLA 動画メタ: S3 → SNS → SQS → Lambda + RDS Proxy"
    s = "Lambda 大量接続で DB CPU 飽和 → 接続プールを RDS Proxy に集約 + SQS で再試行確保"
    cells = [
        title(t), subtitle(s),
        icon('s3', 's3', 40, 135, label='S3\n(動画アップロード)'),
        icon('sns', 'sns', 190, 135, label='SNS Topic\n(Fan-out)'),
        icon('sqs', 'sqs', 340, 135, label='SQS Queue\n(バッファ+再試行)'),
        icon('lam', 'lambda', 490, 135, label='Meta Lambda\n(多数並列)'),
        icon('prox', 'rds', 640, 135, label='RDS Proxy\n(接続プール)', color='#005F83'),
        icon('rds', 'rds', 790, 135, label='RDS PostgreSQL'),
        arrow('a1', 's3', 'sns', 'S3 Event'),
        arrow('a2', 'sns', 'sqs', 'Subscription'),
        arrow('a3', 'sqs', 'lam', 'ESM'),
        arrow('a4', 'lam', 'prox', 'Borrow Conn'),
        arrow('a5', 'prox', 'rds', 'Pooled'),
        note('good', '✅ 正解 A+D: (A) RDS Proxy で接続数集約 → CPU 飽和解消。(D) SNS → SQS 標準キューで欠落防止・再試行確保',
             20, 290, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ SNS 配信ポリシー再試行のみ: Lambda 呼び出し失敗には効く。DB 側の接続枯渇は解決しない',
             20, 350, w=470, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ RDS インスタンス増設: 根本は接続数。Proxy が本質的解決',
             510, 350, w=470, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 Lambda は呼び出し数だけ DB コネクション消費 → RDS Proxy で共有プール化が定石',
             20, 410, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 SNS 直 Lambda より SNS → SQS → Lambda: バッファ + 再試行 + DLQ が追加できる疎結合パターン',
             20, 470, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sap245-s3-sns-sqs-lambda-rdsproxy'


def d_sap_248():
    t = "SAP-248 / リアルタイム画像解析: S3 → SQS → Lambda (Rekognition) → SNS Push"
    s = "営業時間ピーク対応のサーバーレス ETL、夜間ゼロスケールでコスト最小"
    cells = [
        title(t), subtitle(s),
        generic('u', 'User\n(Mobile)', 40, 145, fill='#E8F2FD', stroke='#3B48CC'),
        icon('s3', 's3', 160, 135, label='S3\n(原画)'),
        icon('sqs', 'sqs', 310, 135, label='SQS Queue'),
        icon('lam', 'lambda', 460, 135, label='Lambda'),
        icon('rek', 'rekognition', 610, 135, label='Rekognition\n(自動タグ)', color='#4D72F3'),
        icon('sns', 'sns', 760, 135, label='SNS\n(Mobile Push)'),
        generic('dev', 'Device Push\n(iOS/Android)', 880, 145, w=100, fill='#E8F5E9', stroke='#7AA116'),
        arrow('a1', 'u', 's3', 'upload'),
        arrow('a2', 's3', 'sqs', 'S3 Event'),
        arrow('a3', 'sqs', 'lam', 'ESM'),
        arrow('a4', 'lam', 'rek', 'DetectLabels'),
        arrow('a5', 'lam', 'sns', '結果 publish'),
        arrow('a6', 'sns', 'dev', 'Mobile Push'),
        note('good', '✅ 正解 A+B+F: S3 → SQS (B) → Lambda で Rekognition (A) → SNS モバイルプッシュ (F)。自動スケール・停止コスト最小',
             20, 290, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ EC2 常駐: 夜間アイドル課金 / ❌ Step Functions 毎件起動: 単純 ETL には過剰',
             20, 350, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 SQS を挟むことで毎分数千件のスパイク吸収 + 再試行 + DLQ。Lambda 直 S3 バインドより堅牢',
             20, 410, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 SNS モバイルプッシュ = APNs / FCM / ADM / Baidu へダイレクト配信。カスタム実装不要',
             20, 470, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sap248-s3-sqs-lambda-sns'


def d_sap_268():
    t = "SAP-268 / IAM 作成時の自動権限剥奪: CloudTrail → EventBridge → Step Functions + SNS"
    s = "新規 IAM ユーザー作成を検知し、承認前に権限を剥奪 + 即時レビュー通知"
    cells = [
        title(t), subtitle(s),
        icon('iam', 'iam', 40, 135, label='IAM CreateUser'),
        icon('ct', 'cloudtrail', 180, 135, label='CloudTrail'),
        icon('eb', 'eventbridge', 320, 135, label='EventBridge Rule\n(CreateUser)'),
        icon('sfn', 'step_functions', 480, 135, label='Step Functions\n(権限剥奪 WF)'),
        icon('iam2', 'iam', 640, 135, label='Detach/Delete\nPolicy & Group', color='#DD344C'),
        icon('sns', 'sns', 480, 290, label='SNS Topic'),
        generic('sec', 'Security Ops\n(即時レビュー)', 640, 300, fill='#E8F2FD', stroke='#3B48CC'),
        arrow('a1', 'iam', 'ct', 'API ログ'),
        arrow('a2', 'ct', 'eb', ''),
        arrow('a3', 'eb', 'sfn', 'StartExecution'),
        arrow('a4', 'sfn', 'iam2', 'Detach/Delete', color='#DD344C'),
        arrow('a5', 'eb', 'sns', 'SNS ターゲット'),
        arrow('a6', 'sns', 'sec', 'Email'),
        note('good', '✅ 正解 A+E+F: (E) EventBridge で CreateUser 検知 / (A) Step Functions で権限剥奪 WF / (F) SNS で即時通知',
             20, 380, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ Config ルールのみ: 検知は可能だが自動権限剥奪が弱い / ❌ Lambda 単発: 複数ステップ・リトライ・監査が弱い',
             20, 440, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 EventBridge はイベント発生から数秒で発火 → Step Functions の Error Retry/Catch で堅牢な剥奪ワークフローを構築',
             20, 500, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sap268-eventbridge-stepfunctions-iam'


def d_sap_269():
    t = "SAP-269 / 1 万人同時アップロード: S3 → SQS → ASG EC2 ワーカー → CloudFront"
    s = "Lambda 15 分制限を超える画像加工 + キャッシュ無効化で削除要件も両立"
    cells = [
        title(t), subtitle(s),
        generic('u', 'User (1 万人)', 40, 145, fill='#E8F2FD', stroke='#3B48CC'),
        icon('s3u', 's3', 170, 135, label='S3\n(原画 Upload)'),
        icon('sqs', 'sqs', 310, 135, label='SQS Queue\n(スパイク吸収)'),
        generic('asg', 'EC2 ASG\n(Queue長スケール)', 450, 145, fill='#FFF5EB', stroke='#FF9900'),
        icon('ec2', 'ec2', 590, 135, label='Worker EC2\n(合成処理)'),
        icon('s3p', 's3', 730, 135, label='S3\n(処理済)'),
        icon('cf', 'cloudfront', 870, 135, label='CloudFront\n(配信+Invalidation)'),
        arrow('a1', 'u', 's3u', 'upload'),
        arrow('a2', 's3u', 'sqs', 'S3 Event'),
        arrow('a3', 'sqs', 'asg', 'Queue 長'),
        arrow('a4', 'asg', 'ec2', 'scale'),
        arrow('a5', 'ec2', 's3p', 'put'),
        arrow('a6', 's3p', 'cf', 'origin'),
        arrow('a7', 'cf', 'u', 'view'),
        note('good', '✅ 正解 A: S3→SQS→ASG EC2 で非同期疎結合。Queue 長ベースでスケール、CloudFront Invalidation で削除即時反映',
             20, 290, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ Lambda: 15 分制限で合成処理が重い場合タイムアウト / ❌ 同期 EC2 直: 1 万スパイクで遅延→売上機会損失',
             20, 350, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 削除指示への即応 = CreateInvalidation API (パスで一括無効化)。TTL 0 よりコスト効率的',
             20, 410, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 「EC2 vs Lambda」の分岐点 = 実行時間 15 分と CPU/メモリ要件。画像大量合成は EC2 が無難',
             20, 470, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sap269-s3-sqs-asg-cloudfront'


def d_sap_282():
    t = "SAP-282 / EMR コスト削減: マスター/コア オンデマンド + タスク Spot + Auto Scaling"
    s = "Spark Streaming on EMR — 25% 使用率のアイドル時間を Spot タスクノードで圧縮"
    cells = [
        title(t), subtitle(s),
        icon('sqs', 'sqs', 40, 135, label='SQS Queues\n(入力)'),
        icon('sfn', 'step_functions', 180, 135, label='Step Functions\nExpress WF'),
        icon('emr', 'emr', 320, 135, label='EMR Cluster\n(Spark)'),
        generic('core', 'Master + Core\n(オンデマンド 固定)', 470, 135, w=170, h=50, fill='#EAF5E0', stroke='#7AA116'),
        generic('spot', 'Task Nodes\n(Spot Fleet)', 670, 135, w=160, h=50, fill='#FFF5EB', stroke='#FF9900'),
        icon('cw', 'cloudwatch', 860, 135, label='CloudWatch\nAuto Scaling'),
        arrow('a1', 'sqs', 'sfn', ''),
        arrow('a2', 'sfn', 'emr', 'Spark Job'),
        arrow('a3', 'emr', 'core', ''),
        arrow('a4', 'emr', 'spot', ''),
        arrow('a5', 'cw', 'spot', 'ピーク追従', dashed=True, color='#7AA116'),
        note('good', '✅ 正解 D: マスター/コア = オンデマンドで安定性確保 / タスク = Spot Fleet + CW Auto Scaling で 25% → 75% 時間コスト削減',
             20, 290, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ RI 固定クラスター: アイドル時間のコスト浪費 / ❌ 常時一定台数: 変動トラフィックに追従できず',
             20, 350, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 EMR のベストプラクティス: Master/Core = オンデマンド or RI、Task = Spot が鉄板',
             20, 410, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 Task ノードは HDFS を持たないので中断に強い。Spot 中断時は別 AZ に再投入',
             20, 470, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sap282-emr-spot-autoscaling'


DIAGRAMS = {
    'SAP-7':   d_sap_7,
    'SAP-14':  d_sap_14,
    'SAP-69':  d_sap_69,
    'SAP-108': d_sap_108,
    'SAP-135': d_sap_135,
    'SAP-141': d_sap_141,
    'SAP-144': d_sap_144,
    'SAP-154': d_sap_154,
    'SAP-161': d_sap_161,
    'SAP-176': d_sap_176,
    'SAP-204': d_sap_204,
    'SAP-245': d_sap_245,
    'SAP-248': d_sap_248,
    'SAP-268': d_sap_268,
    'SAP-269': d_sap_269,
    'SAP-282': d_sap_282,
}


def main():
    created = []
    skipped = []
    for qid, fn in DIAGRAMS.items():
        path = OUT / f"{qid}.drawio"
        if path.exists():
            skipped.append(qid)
            continue
        body, name = fn()
        content = drawio_wrap(body, qid.lower(), name)
        path.write_text(content, encoding='utf-8')
        created.append(qid)
    print(f"created: {len(created)} -> {created}")
    print(f"skipped: {len(skipped)} -> {skipped}")


if __name__ == '__main__':
    main()
