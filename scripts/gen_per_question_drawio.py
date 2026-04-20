#!/usr/bin/env python3
"""
Generate per-question drawio files for AWS SAP diagram set (msg-heavy category).
1000x600 canvas, white background, AWS official colors, 50x50 icons (label offset +58).
"""
import os
import json
from pathlib import Path

OUT = Path('/Users/aki/aws-sap/docs/diagrams/per-question')
OUT.mkdir(parents=True, exist_ok=True)

# ----- Helpers -----
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

# AWS official service colors for icon fill
ICON_COLOR = {
    'eventbridge':       '#E7157B',  # EventBridge pink
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
    'fargate':           '#ED7100',
    'cloudfront':        '#8C4FFF',
    'cloudwatch':        '#E7157B',
    'cloudtrail':        '#E7157B',
    'iam':               '#C925D1',
    'iot_core':          '#3B48CC',
    'opensearch_service':'#005F83',
    'redshift':          '#3B48CC',
    'emr':               '#8C4FFF',
    'appsync':           '#E7157B',
    'rds':               '#3B48CC',
    'aurora':            '#3B48CC',
    'batch':             '#ED7100',
    'codebuild':         '#C925D1',
    'codecommit':        '#C925D1',
    'ecr':               '#ED7100',
    'elastic_container_service': '#ED7100',
    'documentdb':        '#3B48CC',
    'datasync':          '#7AA116',
    'systems_manager':   '#E7157B',
    'eks':               '#ED7100',
    'firewall_manager':  '#DD344C',
    'waf':               '#DD344C',
    'access_analyzer':   '#DD344C',
    'secrets_manager':   '#DD344C',
    'kms':               '#DD344C',
    'simple_notification_service': '#E7157B',
    'simple_queue_service': '#E7157B',
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
        # label must be at icon.y + 58 or more
        ly = y + 58
        elems.append(f'''<mxCell id="{id_}_l" value="{label}" style="text;html=1;align=center;verticalAlign=top;whiteSpace=wrap;fontSize=10;fontColor=#232F3E;" vertex="1" parent="1">
  <mxGeometry x="{x-25}" y="{ly}" width="{w+50}" height="28" as="geometry" />
</mxCell>''')
    return '\n'.join(elems)

def generic_icon(id_, value, x, y, w=80, h=40, fill='#F2F2F2', stroke='#666666', font_size=10):
    return f'''<mxCell id="{id_}" value="{value}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize={font_size};fontColor=#232F3E;verticalAlign=middle;align=center;" vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>'''

def arrow(id_, src, tgt, label='', color='#232F3E', dashed=False):
    style = f"endArrow=classic;html=1;strokeColor={color};strokeWidth=2;fontSize=10;fontColor=#232F3E;"
    if dashed:
        style += "dashed=1;"
    lbl_attr = f'value="{label}"' if label else 'value=""'
    return f'''<mxCell id="{id_}" {lbl_attr} style="{style}" edge="1" parent="1" source="{src}" target="{tgt}">
  <mxGeometry relative="1" as="geometry" />
</mxCell>'''

def arrow_xy(id_, x1, y1, x2, y2, label='', color='#232F3E', dashed=False):
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

def note(id_, text, x, y, w=960, h=50, fill='#FFF5EB', stroke='#FF9900'):
    return f'''<mxCell id="{id_}" value="{text}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize=11;fontStyle=1;fontColor=#232F3E;verticalAlign=middle;align=left;spacingLeft=10;spacingRight=10;" vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>'''

def group_rect(id_, label, x, y, w, h, stroke='#4D72F3', fill='none'):
    return f'''<mxCell id="{id_}" value="{label}" style="rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=2;fontSize=11;fontStyle=1;fontColor={stroke};verticalAlign=top;align=left;spacingLeft=8;spacingTop=4;dashed=1;" vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>'''

def client(id_, value, x, y, w=70, h=40):
    return f'''<mxCell id="{id_}" value="{value}" style="shape=mscae/user;html=1;fillColor=#232F3E;strokeColor=#232F3E;fontColor=#232F3E;verticalAlign=bottom;verticalLabelPosition=bottom;labelPosition=center;align=center;fontSize=10;" vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>'''

# ----- Diagram definitions -----
DIAGRAMS = {}


def make_udemy_050():
    """SQS DLQ -> EventBridge -> Lambda -> SNS/ops notify"""
    title_text = "UDEMY-050 / SQS 処理失敗メッセージを DLQ で分離 → EventBridge → Lambda で分析・通知"
    sub = "注文処理失敗を隔離し、再処理可能な形で監視運用チームに通知"
    cells = [
        title(title_text),
        subtitle(sub),
        # flow: Producer -> Main SQS -> Lambda consumer
        generic_icon('prod', 'Order API\n(Producer)', 40, 140, w=110, h=50, fill='#FFF5EB', stroke='#FF9900'),
        icon('mainsqs', 'sqs', 200, 135, label='Main Queue'),
        icon('consumer', 'lambda', 320, 135, label='Consumer Lambda'),
        # DLQ
        icon('dlq', 'sqs', 440, 135, label='Dead Letter Queue\n(maxReceiveCount 超過)', color='#DD344C'),
        # EventBridge rule
        icon('eb', 'eventbridge', 580, 135, label='EventBridge Rule\n(DLQ 深度監視)'),
        # Lambda analyzer
        icon('analyzer', 'lambda', 720, 135, label='Analyzer Lambda\n(原因分析)'),
        # SNS notification
        icon('sns', 'sns', 860, 135, label='SNS → Ops Email'),
        # arrows
        arrow('a1', 'prod', 'mainsqs', '送信'),
        arrow('a2', 'mainsqs', 'consumer', 'poll'),
        arrow('a3', 'consumer', 'dlq', '失敗→隔離', color='#DD344C'),
        arrow('a4', 'dlq', 'eb', 'CW Alarm/Rule'),
        arrow('a5', 'eb', 'analyzer'),
        arrow('a6', 'analyzer', 'sns', '通知'),
        # compare box
        note('good', '✅ 正解パターン: DLQ で失敗メッセージを失わずに隔離 → EventBridge ルール（ApproximateNumberOfMessagesVisible など）で Lambda 起動 → 分析後 SNS 通知',
             20, 280, w=960, h=50, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ SNS に直接送信だけ: 失敗メッセージを永続保持できず再処理不能',
             20, 350, w=470, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ SQS → Lambda で try/catch: 関数ごとの永続隔離が難しくメッセージ消失のリスク',
             510, 350, w=470, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 DLQ の選定: 送信元キューと同タイプ (Standard/FIFO) を指定。maxReceiveCount はビジネスリトライ許容回数に合わせる。',
             20, 410, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 DLQ に溜まり続ける事象は「バグの痕跡」— メッセージ本体を S3 にアーカイブ、監視は CloudWatch Metric で自動通知が鉄板',
             20, 470, w=960, h=50, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sqs-dlq-eventbridge-lambda'


def make_udemy_328():
    """Lambda on-failure destination -> SNS / SQS DLQ"""
    title_text = "UDEMY-328 / Lambda 失敗時の Destination 設定 + SNS トピック + DLQ での確実再処理"
    sub = "非同期 Lambda で失敗時メッセージを失わない設計 — SNS サブスク経路と Destinations の違い"
    cells = [
        title(title_text),
        subtitle(sub),
        # Main flow: Event source -> SNS -> Lambda -> (success/failure) Destinations
        generic_icon('src', 'Event Source\n(S3/API/etc)', 40, 140, w=110, h=50, fill='#FFF5EB', stroke='#FF9900'),
        icon('sns', 'sns', 200, 135, label='SNS Topic'),
        icon('lambda', 'lambda', 360, 135, label='Subscriber Lambda'),
        # Success destination
        icon('succ', 'eventbridge', 520, 60, label='On-Success →\nEventBridge Bus'),
        # Failure destination
        icon('fail', 'sqs', 520, 220, label='On-Failure →\nSQS (DLQ)', color='#DD344C'),
        # Reprocessor
        icon('reproc', 'lambda', 700, 220, label='Reprocessor Lambda'),
        icon('archive', 's3', 860, 220, label='Audit Archive'),
        arrow('a1', 'src', 'sns', 'publish'),
        arrow('a2', 'sns', 'lambda', 'fanout'),
        arrow('a3', 'lambda', 'succ', 'success', color='#7AA116'),
        arrow('a4', 'lambda', 'fail', 'failure', color='#DD344C'),
        arrow('a5', 'fail', 'reproc', '再処理'),
        arrow('a6', 'reproc', 'archive', '保管'),
        note('good', '✅ Lambda Destinations (On-Failure) → SQS: 失敗メッセージの本体 + エラー情報を SQS に自動保存。DLQ よりもリッチなコンテキスト保持',
             20, 320, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('cmp1', '📌 Destinations vs DLQ:\n• DLQ = 古い機能。呼び出しメタデータのみ\n• Destinations = Event JSON + 応答・エラー・コンテキスト丸ごと\n• Destinations は 成功と失敗で別ターゲット (SQS/SNS/Lambda/EB) に振り分け可能',
             20, 380, w=500, h=110, fill='#FFF5EB', stroke='#FF9900'),
        note('cmp2', '❌ SNS トピックに失敗情報を送るだけ: 購読者がオフラインだとロスト。SQS なら永続バッファ\n❌ Lambda リトライのみ依存: 最大 2回 → その後消失',
             540, 380, w=440, h=110, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 非同期呼び出し (Event invocation) でのみ Destinations が動作。同期呼び出しには効かない点に注意',
             20, 510, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'lambda-destinations-dlq'


def make_udemy_045():
    """S3/CF + AppSync + SQS + Lambda + DLQ"""
    title_text = "UDEMY-045 / サーバーレス注文システム: CloudFront+S3 → AppSync → SQS → Lambda + DLQ"
    sub = "モノリス刷新パターン — フロント/API/非同期処理/失敗隔離を疎結合で構築"
    cells = [
        title(title_text),
        subtitle(sub),
        icon('cf', 'cloudfront', 40, 120, label='CloudFront'),
        icon('s3', 's3', 170, 120, label='S3 Static\n(SPA)'),
        icon('appsync', 'appsync', 310, 120, label='AppSync\n(GraphQL)'),
        icon('sqs', 'sqs', 460, 120, label='SQS Queue\n(Order)'),
        icon('lambda', 'lambda', 600, 120, label='Order Lambda'),
        icon('ddb', 'dynamodb', 750, 120, label='DynamoDB'),
        icon('dlq', 'sqs', 600, 280, label='SQS DLQ\n(失敗注文)', color='#DD344C'),
        icon('sns', 'sns', 750, 280, label='SNS → Ops'),
        arrow('a1', 'cf', 's3', ''),
        arrow('a2', 's3', 'appsync', 'GraphQL'),
        arrow('a3', 'appsync', 'sqs', 'SendMessage'),
        arrow('a4', 'sqs', 'lambda', 'ESM'),
        arrow('a5', 'lambda', 'ddb', 'PutItem'),
        arrow('a6', 'lambda', 'dlq', '失敗', color='#DD344C'),
        arrow('a7', 'dlq', 'sns', '監視通知'),
        note('good', '✅ 疎結合の要: SQS がフロント API と処理 Lambda を切り離し。失敗は DLQ に永続化 → 運用チーム通知',
             20, 380, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('cmp', '📌 vs API Gateway + Lambda 同期呼び出し: リクエスト中の失敗がそのままクライアントエラーに。SQS バッファ挟むと「必ず処理完了」を約束できる',
             20, 440, w=960, h=50, fill='#FFF5EB', stroke='#FF9900'),
        note('tip', '💡 AppSync は GraphQL Resolver から直接 SQS/Lambda/DDB へ書込可。変更イベントは Subscription で即時プッシュ',
             20, 510, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'serverless-order-sqs-dlq'


def make_udemy_065():
    """Firehose -> S3 -> Batch Spot -> EventBridge schedule"""
    title_text = "UDEMY-065 / 夜間バッチ: Firehose→S3 + AWS Batch Spot + EventBridge スケジュール"
    sub = "リアルタイム取込と低コストの夜間処理を分離 — Spot × EventBridge でコスト 40%"
    cells = [
        title(title_text),
        subtitle(sub),
        icon('src', 'api_gateway', 40, 140, label='取込 API'),
        icon('firehose', 'kinesis_data_firehose', 180, 140, label='Kinesis Data\nFirehose'),
        icon('s3', 's3', 320, 140, label='S3 (Raw)\nPartitioned by hour'),
        icon('eb', 'eventbridge', 470, 140, label='EventBridge\nSchedule (夜間)'),
        icon('batch', 'batch', 610, 140, label='AWS Batch\n(Spot 40%)', color='#ED7100'),
        icon('s3r', 's3', 770, 140, label='S3 (Result)'),
        icon('athena', 'athena', 870, 300, label='Athena (Query)'),
        arrow('a1', 'src', 'firehose'),
        arrow('a2', 'firehose', 's3', 'buffer 5min'),
        arrow('a3', 'eb', 'batch', 'cron(0 22 * * ? *)'),
        arrow('a4', 's3', 'batch', 'read', dashed=True),
        arrow('a5', 'batch', 's3r', 'write'),
        arrow('a6', 's3r', 'athena', 'SQL'),
        note('good', '✅ 正解: 取込は Firehose で S3 ランディング → EventBridge が夜間 Batch Job を起動 → Spot で最大 60% 削減',
             20, 310, w=830, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ EC2 常時起動でバッチ: 夜間のみ稼働なので EC2 を常駐 → 無駄コスト',
             20, 370, w=460, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('bad2', '❌ Kinesis Data Analytics だけ: リアルタイム集計用で 6 時間バッチの重計算には不向き',
             500, 370, w=470, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Spot 中断対策: Batch は自動でフォールバック / リトライ。EventBridge Scheduler (新) なら ONE_TIME / RATE / CRON 併用',
             20, 430, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '📌 Firehose は「コードレス取込」: Lambda 変換・動的パーティショニング・圧縮・KMS・Parquet 変換まで一発',
             20, 490, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'firehose-batch-eventbridge'


def make_udemy_015():
    """IoT Core -> Firehose -> S3 + Kinesis Analytics"""
    title_text = "UDEMY-015 / IoT 車両: IoT Core → Firehose → S3 + Kinesis Data Analytics (異常検知)"
    sub = "MQTT 受信を Firehose で S3 に永続化、同時に Analytics で SQL リアルタイム異常検知"
    cells = [
        title(title_text),
        subtitle(sub),
        generic_icon('iot', 'Vehicle MQTT', 40, 140, w=110, h=50, fill='#E8F2FD', stroke='#3B48CC'),
        icon('iotcore', 'iot_core', 190, 130, label='IoT Core\n(Rules Engine)'),
        icon('firehose', 'kinesis_data_firehose', 340, 130, label='Firehose'),
        icon('s3', 's3', 490, 130, label='S3\n(Archive)'),
        icon('kda', 'kinesis_data_analytics', 340, 280, label='Kinesis Data\nAnalytics'),
        icon('sns', 'sns', 490, 280, label='SNS\n(Anomaly Alert)'),
        arrow('a1', 'iot', 'iotcore', 'MQTT/TLS'),
        arrow('a2', 'iotcore', 'firehose', 'Rule Action'),
        arrow('a3', 'firehose', 's3', 'buffered 60s'),
        arrow('a4', 'iotcore', 'kda', 'Rule Action', dashed=True),
        arrow('a5', 'kda', 'sns', '閾値超過'),
        note('good', '✅ 正解: IoT Core Rules で Firehose (S3 アーカイブ) と Kinesis Data Analytics (異常検知) に同時振り分け',
             20, 370, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ EC2 で MQTT 受信: 認証・スケーリング・TLS 管理を自前実装 → 運用負荷大\n❌ Lambda 直接呼び出し: 秒間数万件超えでスロットリング発生しやすい',
             20, 430, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 IoT Rule SQL: SELECT ... FROM topic WHERE ... で条件ルーティング可。複数アクションで「アーカイブ+分析」を両立',
             20, 510, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'iot-firehose-analytics'


def make_udemy_097():
    """IoT Core -> Kinesis Data Streams -> OpenSearch"""
    title_text = "UDEMY-097 / ミリ秒リアルタイム: IoT Core → Kinesis Data Streams → OpenSearch Serverless"
    sub = "Firehose のバッファ遅延 (最小60s) を排除し、ミリ秒レベルの可視化を実現"
    cells = [
        title(title_text),
        subtitle(sub),
        generic_icon('iot', 'IoT Sensors', 60, 140, w=100, h=50, fill='#E8F2FD', stroke='#3B48CC'),
        icon('iotcore', 'iot_core', 200, 130, label='IoT Core'),
        icon('kds', 'kinesis_data_streams', 360, 130, label='Kinesis Data\nStreams'),
        icon('os', 'opensearch_service', 520, 130, label='OpenSearch\nServerless'),
        generic_icon('dash', 'OpenSearch Dashboards', 700, 140, w=180, h=50, fill='#E8F5E9', stroke='#005F83'),
        arrow('a1', 'iot', 'iotcore'),
        arrow('a2', 'iotcore', 'kds'),
        arrow('a3', 'kds', 'os'),
        arrow('a4', 'os', 'dash'),
        note('cmp1', '✅ KDS 選定理由: <70ms 遅延 / 複数 Consumer 並列 / Enhanced Fan-out で専用スループット',
             20, 290, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('cmp2', '❌ Firehose: 最小バッファ 60 秒 (または 1MB) → リアルタイムではない',
             20, 350, w=470, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('cmp3', '❌ SNS/SQS 経由: 時系列分析やストリーム処理には不向き',
             510, 350, w=470, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '📌 選定軸: 遅延許容 >60s → Firehose / <1s → Kinesis Data Streams / 高スループット共有 → Enhanced Fan-out',
             20, 410, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '💡 OpenSearch Serverless = キャパシティ自動スケール・管理不要。Dashboards で即時可視化',
             20, 470, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'iot-kds-opensearch'


def make_udemy_011():
    """IoT Core -> Firehose -> Lambda -> S3"""
    title_text = "UDEMY-011 / 大量 IoT MQTT: IoT Core → Firehose + Lambda 変換 → S3"
    sub = "コードレス取込 + 可変変換のハイブリッド — サーバーレス完結の IoT パイプライン"
    cells = [
        title(title_text),
        subtitle(sub),
        generic_icon('iot', 'MQTT Devices', 40, 140, w=100, h=50, fill='#E8F2FD', stroke='#3B48CC'),
        icon('iotcore', 'iot_core', 180, 130, label='IoT Core\n(Rules)'),
        icon('firehose', 'kinesis_data_firehose', 340, 130, label='Kinesis Data\nFirehose'),
        icon('lambda', 'lambda', 500, 130, label='Lambda\n(Transform)'),
        icon('s3', 's3', 660, 130, label='S3\n(Parquet)'),
        icon('athena', 'athena', 820, 130, label='Athena'),
        arrow('a1', 'iot', 'iotcore'),
        arrow('a2', 'iotcore', 'firehose', 'Rule'),
        arrow('a3', 'firehose', 'lambda', 'invoke', dashed=True),
        arrow('a4', 'lambda', 'firehose', 'transformed', dashed=True),
        arrow('a5', 'firehose', 's3'),
        arrow('a6', 's3', 'athena'),
        note('good', '✅ 正解: Firehose で「スケール」+ Lambda で「変換」。IoT Core Rule が取込ハブ',
             20, 290, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ EC2 で MQTT 受信 → Kinesis: スケールと運用コストが増大。IoT Core 直差しで省く\n❌ Lambda を IoT Core 直接バインド: 高 TPS 時のスロットリング + 部分重複',
             20, 350, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Firehose + Lambda 変換: レコードごとに 6MB まで加工可。Parquet/ORC 変換で Athena コスト最小化',
             20, 430, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '📌 IoT Core Rule Action は 1 メッセージを複数 AWS サービスへ並列ルーティング可 (Firehose + Lambda + SNS 等)',
             20, 490, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'iot-firehose-lambda-s3'


def make_udemy_013():
    """Kinesis Data Streams -> EMR -> Redshift"""
    title_text = "UDEMY-013 / リアルタイム収集 → 分析: KDS + EMR (Spark) → Redshift DWH"
    sub = "ストリーム収集 + 重集計 + 列指向 DWH の正統パイプライン"
    cells = [
        title(title_text),
        subtitle(sub),
        generic_icon('sensors', 'Sensors (大量)', 40, 140, w=130, h=50, fill='#E8F2FD', stroke='#3B48CC'),
        icon('kds', 'kinesis_data_streams', 200, 130, label='Kinesis Data\nStreams'),
        icon('emr', 'emr', 360, 130, label='EMR\n(Spark Streaming)'),
        icon('s3', 's3', 520, 130, label='S3\n(ステージング)'),
        icon('redshift', 'redshift', 680, 130, label='Redshift\n(DWH)'),
        generic_icon('bi', 'QuickSight / BI', 840, 140, w=130, h=50, fill='#E8F5E9', stroke='#7AA116'),
        arrow('a1', 'sensors', 'kds'),
        arrow('a2', 'kds', 'emr', 'KCL'),
        arrow('a3', 'emr', 's3'),
        arrow('a4', 's3', 'redshift', 'COPY'),
        arrow('a5', 'redshift', 'bi'),
        note('good', '✅ 正解: KDS で収集 → EMR で前処理/集計 → S3 経由で Redshift に COPY ロード',
             20, 290, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ Kinesis → Redshift 直接: スループットと複雑変換に不向き (Firehose 経由なら別だが古い問題文では EMR 正解)\n❌ Firehose → DynamoDB: DWH の時系列分析に適さない',
             20, 350, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 今の定番は「KDS → Firehose → Redshift」または「KDS → Glue Streaming → S3 + Athena」。試験では設問の制約に合わせて選択',
             20, 430, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '📌 EMR は Spark/Hadoop/Hive/Presto など長時間バッチ/ストリーム処理に強み。クラスタ寿命と料金モデルを把握',
             20, 490, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'kds-emr-redshift'


def make_udemy_018():
    """VPC Flow Logs -> CW Logs -> Firehose -> Lambda anonymize -> Splunk"""
    title_text = "UDEMY-018 / VPC Flow Logs → CloudWatch Logs Subscription → Firehose + Lambda 匿名化 → Splunk"
    sub = "Splunk 連携の黄金パターン: Subscription Filter → Firehose + Lambda で PII マスク"
    cells = [
        title(title_text),
        subtitle(sub),
        generic_icon('vpc', 'VPC Flow Logs', 40, 140, w=130, h=50, fill='#E8F2FD', stroke='#3B48CC'),
        icon('cwl', 'cloudwatch', 200, 130, label='CloudWatch Logs\n(Subscription)'),
        icon('firehose', 'kinesis_data_firehose', 360, 130, label='Firehose'),
        icon('lambda', 'lambda', 520, 130, label='Lambda\n(Mask PII)'),
        generic_icon('splunk', 'Splunk HEC\n(HTTPS)', 680, 140, w=130, h=50, fill='#F5E7D5', stroke='#8C4FFF'),
        icon('s3', 's3', 840, 130, label='S3\n(Backup)'),
        arrow('a1', 'vpc', 'cwl'),
        arrow('a2', 'cwl', 'firehose', 'Subscription Filter'),
        arrow('a3', 'firehose', 'lambda', 'Transform', dashed=True),
        arrow('a4', 'lambda', 'firehose', 'anonymized', dashed=True),
        arrow('a5', 'firehose', 'splunk'),
        arrow('a6', 'firehose', 's3', 'エラー Backup', dashed=True),
        note('good', '✅ Firehose は Splunk を Destination としてネイティブ対応。Lambda 変換で IP / MAC / ユーザー名をマスク',
             20, 290, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ EC2 上の Forwarder → Splunk: スケーリングと HA を自前運用\n❌ Lambda が Splunk に直接送信: HTTP リトライ / 背圧処理を実装しなければならない',
             20, 350, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Firehose の Backup 設定で Splunk 送信失敗を S3 に自動保存。再送可能',
             20, 430, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '📌 CloudWatch Logs Subscription は Destination (KDS / Firehose / Lambda) に直接配信可。中間 EC2 不要',
             20, 490, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'flowlogs-firehose-splunk'


def make_udemy_026():
    """Aurora Activity Stream -> KDS -> Firehose -> S3"""
    title_text = "UDEMY-026 / Aurora DB Activity Stream → Kinesis Data Streams → Firehose → S3 監査"
    sub = "DB 監査証跡のニアリアルタイム配信 — KDS にプッシュ → Firehose で暗号化 S3 保存"
    cells = [
        title(title_text),
        subtitle(sub),
        icon('aurora', 'aurora', 40, 130, label='Aurora MySQL\n(Activity Stream)'),
        icon('kds', 'kinesis_data_streams', 200, 130, label='Kinesis Data\nStreams'),
        icon('firehose', 'kinesis_data_firehose', 360, 130, label='Firehose\n(+KMS Encrypt)'),
        icon('s3', 's3', 520, 130, label='S3\n(Audit Log)'),
        icon('athena', 'athena', 680, 130, label='Athena\n(Query)'),
        generic_icon('qs', 'QuickSight', 830, 140, w=130, h=50, fill='#E8F5E9', stroke='#7AA116'),
        arrow('a1', 'aurora', 'kds', 'DAS Push'),
        arrow('a2', 'kds', 'firehose'),
        arrow('a3', 'firehose', 's3'),
        arrow('a4', 's3', 'athena'),
        arrow('a5', 'athena', 'qs'),
        note('good', '✅ DB Activity Streams は KDS 前提で設計。Firehose で S3 の列指向変換 (Parquet) + KMS 暗号化',
             20, 290, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ CloudTrail だけで監査: データプレーン SQL (SELECT など) の記録は不可\n❌ RDS Audit Plugin + CW Logs: Aurora 固有 DAS のほうが遅延少・統合容易',
             20, 350, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 DAS = 非同期で DB パフォーマンス影響ほぼゼロ。KMS で暗号化された非同期ストリームが KDS に到達',
             20, 430, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '📌 Athena + Parquet + パーティショニングで長期ログを低コスト検索可能',
             20, 490, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'aurora-das-kds-firehose-s3'


def make_udemy_373():
    """ECR scan on push -> EventBridge -> Step Functions (gate) -> CodePipeline"""
    title_text = "UDEMY-373 / ECR Scan on Push → EventBridge → Step Functions (ゲート判定) → CodePipeline 停止/続行"
    sub = "ECR Basic Scan の Finding を EventBridge が検知し、Step Functions で自動判定"
    cells = [
        title(title_text),
        subtitle(sub),
        icon('ecr', 'ecr', 40, 130, label='ECR Repo\n(Scan on Push)'),
        icon('eb', 'eventbridge', 200, 130, label='EventBridge\n(Scan Complete)'),
        icon('sfn', 'step_functions', 360, 130, label='Step Functions\n(判定ワークフロー)'),
        generic_icon('choice', 'Choice:\nCRITICAL/HIGH ?', 520, 130, w=140, h=50, fill='#FFF5EB', stroke='#FF9900'),
        generic_icon('stop', 'Stop CodePipeline', 700, 70, w=150, h=50, fill='#FDECEA', stroke='#DD344C'),
        generic_icon('deploy', 'Continue Deploy\n(CodeDeploy)', 700, 190, w=150, h=50, fill='#EAF5E0', stroke='#7AA116'),
        icon('sns', 'sns', 870, 70, label='SNS Notify\n(SecOps)'),
        arrow('a1', 'ecr', 'eb', 'Finding Event'),
        arrow('a2', 'eb', 'sfn'),
        arrow('a3', 'sfn', 'choice'),
        arrow('a4', 'choice', 'stop', 'Yes', color='#DD344C'),
        arrow('a5', 'choice', 'deploy', 'No', color='#7AA116'),
        arrow('a6', 'stop', 'sns'),
        note('good', '✅ 正解: ECR Scan 結果は EventBridge で「Image Scan Completed」として発行 → Step Functions の判定で High/Critical を自動ゲート',
             20, 280, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad1', '❌ Inspector で自動停止: 検知はできても CI/CD パイプラインを直接停止する統合は Step Functions 経由が安定',
             20, 340, w=960, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Step Functions の StopPipelineExecution API 呼び出しで CodePipeline 実行を停止可能',
             20, 400, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '📌 ECR Enhanced Scanning (Inspector v2) なら継続スキャン + Package 脆弱性も検知',
             20, 460, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'ecr-scan-eventbridge-stepfn'


def make_udemy_287():
    """DataSync -> S3 -> Lambda -> Step Functions -> ECS Fargate"""
    title_text = "UDEMY-287 / ゲノム分析: DataSync → S3 → Lambda → Step Functions → ECS Fargate バッチ"
    sub = "大容量転送 + イベント駆動 + 並列コンテナバッチのサーバーレス設計"
    cells = [
        title(title_text),
        subtitle(sub),
        generic_icon('onprem', 'On-prem\nGenomics', 40, 140, w=100, h=50, fill='#F2F2F2', stroke='#666'),
        icon('ds', 'datasync', 180, 130, label='DataSync\n(+TLS)'),
        icon('s3', 's3', 340, 130, label='S3 Raw\n(Landing)'),
        icon('lambda', 'lambda', 500, 130, label='Trigger\nLambda'),
        icon('sfn', 'step_functions', 660, 130, label='Step Functions\n(並列/条件分岐)'),
        icon('ecs', 'ecs', 820, 130, label='ECS Fargate\n(Docker Analysis)'),
        icon('s3r', 's3', 820, 280, label='S3 Result'),
        arrow('a1', 'onprem', 'ds'),
        arrow('a2', 'ds', 's3'),
        arrow('a3', 's3', 'lambda', 'ObjectCreated'),
        arrow('a4', 'lambda', 'sfn'),
        arrow('a5', 'sfn', 'ecs', 'RunTask'),
        arrow('a6', 'ecs', 's3r'),
        note('good', '✅ DataSync = オンプレ-S3 の高速 (最大 10Gbps) / 暗号化 / チェックサム検証付き転送の標準',
             20, 370, w=830, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ S3 CLI スクリプト転送: 大容量・定期・再開のハンドリングを自前実装\n❌ Snowball: 継続転送には向かない (一括移行向け)',
             20, 430, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Step Functions で「ファイル分割 → Map State で並列 Fargate 実行 → 結果集約」が定番パターン',
             20, 510, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
    ]
    return '\n'.join(cells), 'datasync-sfn-fargate'


def make_udemy_336():
    """IoT Core -> Step Functions + Lambda -> DocumentDB, CloudFront"""
    title_text = "UDEMY-336 / IoT MQTT → Step Functions + Lambda → DocumentDB (+ CloudFront 配信)"
    sub = "デバイスデータを複雑ワークフロー処理 → NoSQL 保存 → 配信 CDN"
    cells = [
        title(title_text),
        subtitle(sub),
        generic_icon('dev', 'IoT Devices', 40, 140, w=100, h=50, fill='#E8F2FD', stroke='#3B48CC'),
        icon('iot', 'iot_core', 180, 130, label='IoT Core\n(Rules)'),
        icon('sfn', 'step_functions', 340, 130, label='Step Functions'),
        icon('lambda', 'lambda', 500, 130, label='Lambda Tasks\n(Validate/Enrich)'),
        icon('ddoc', 'documentdb', 660, 130, label='DocumentDB\n(JSON Store)'),
        icon('s3', 's3', 660, 280, label='S3 Report'),
        icon('cf', 'cloudfront', 820, 280, label='CloudFront\n(Global)'),
        arrow('a1', 'dev', 'iot'),
        arrow('a2', 'iot', 'sfn', 'Rule Action'),
        arrow('a3', 'sfn', 'lambda'),
        arrow('a4', 'lambda', 'ddoc'),
        arrow('a5', 'sfn', 's3', 'Generate Report'),
        arrow('a6', 's3', 'cf'),
        note('good', '✅ Step Functions: 条件分岐 / 並列 / リトライ / エラー捕捉を宣言的に記述 → 複雑な IoT フローに最適',
             20, 370, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ Lambda を Chain 実装: 状態管理・例外処理が爆発。Step Functions で可視化＆運用性確保',
             20, 430, w=960, h=40, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 IoT Core Rule → Step Functions StartExecution で直接起動可能 (Lambda 不要)',
             20, 480, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'iot-stepfn-documentdb'


def make_udemy_315():
    """EventBridge Bus -> multiple microservices fanout"""
    title_text = "UDEMY-315 / マイクロサービス間 ID 変更を EventBridge カスタムバスで疎結合 Fan-out"
    sub = "各サービスが自前のルールで必要なイベントだけ購読 — 1対多 + フィルタで拡張容易"
    cells = [
        title(title_text),
        subtitle(sub),
        icon('core', 'api_gateway', 40, 140, label='Core System\n(ID Update)'),
        icon('eb', 'eventbridge', 210, 140, label='Custom\nEvent Bus'),
        # rule per microservice
        generic_icon('r1', 'Rule 1: Billing', 380, 70, w=140, h=40, fill='#FFF5EB', stroke='#FF9900'),
        generic_icon('r2', 'Rule 2: CRM', 380, 140, w=140, h=40, fill='#FFF5EB', stroke='#FF9900'),
        generic_icon('r3', 'Rule 3: Notification', 380, 210, w=140, h=40, fill='#FFF5EB', stroke='#FF9900'),
        generic_icon('r4', 'Rule 4: Analytics', 380, 280, w=140, h=40, fill='#FFF5EB', stroke='#FF9900'),
        icon('ms1', 'lambda', 570, 50, label='Billing Svc'),
        icon('ms2', 'lambda', 570, 130, label='CRM Svc'),
        icon('ms3', 'sns', 570, 210, label='Notify Svc'),
        icon('ms4', 'kinesis_data_streams', 570, 290, label='Analytics Svc'),
        icon('db1', 'dynamodb', 740, 50, label='Billing DB'),
        icon('db2', 'dynamodb', 740, 130, label='CRM DB'),
        generic_icon('email', 'Email/SMS', 740, 220, w=100, h=40, fill='#E8F2FD', stroke='#3B48CC'),
        icon('s3', 's3', 740, 290, label='Data Lake'),
        arrow('a1', 'core', 'eb', 'PutEvents'),
        arrow('a2', 'eb', 'r1'),
        arrow('a3', 'eb', 'r2'),
        arrow('a4', 'eb', 'r3'),
        arrow('a5', 'eb', 'r4'),
        arrow('a6', 'r1', 'ms1'),
        arrow('a7', 'r2', 'ms2'),
        arrow('a8', 'r3', 'ms3'),
        arrow('a9', 'r4', 'ms4'),
        arrow('a10', 'ms1', 'db1'),
        arrow('a11', 'ms2', 'db2'),
        arrow('a12', 'ms3', 'email'),
        arrow('a13', 'ms4', 's3'),
        note('good', '✅ EventBridge Custom Bus: 新しいマイクロサービスはルール追加のみで参加可能 → 強疎結合',
             20, 380, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ SNS Topic: Fan-out は可能だがイベントスキーマ/フィルタ/Schema Registry の機能は EventBridge が上\n❌ SQS 直列: 1対1 なので複数サービス配信に不向き',
             20, 440, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Schema Registry + コード生成で各 MS の契約ずれを防止。Archive + Replay でトラブル時の再処理',
             20, 520, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'eventbridge-ms-fanout'


def make_udemy_164():
    """ASG Lifecycle Hook -> EventBridge -> SSM RunCommand -> S3"""
    title_text = "UDEMY-164 / ASG ライフサイクルフック → EventBridge → SSM Run Command → S3 ログ集約"
    sub = "Terminating:Wait でインスタンスをホールド → SSM がログを S3 送信 → Complete"
    cells = [
        title(title_text),
        subtitle(sub),
        icon('asg', 'ec2', 40, 130, label='ASG Instance\n(Terminating:Wait)'),
        icon('eb', 'eventbridge', 210, 130, label='EventBridge\n(Lifecycle Event)'),
        icon('ssm', 'systems_manager', 380, 130, label='SSM\nRun Command'),
        icon('doc', 'systems_manager', 540, 130, label='SSM Document\n(copy to S3)'),
        icon('s3', 's3', 710, 130, label='S3 Log Archive'),
        generic_icon('complete', 'CompleteLifecycleAction\n→ Terminate OK', 870, 140, w=120, h=50, fill='#EAF5E0', stroke='#7AA116'),
        arrow('a1', 'asg', 'eb', 'Lifecycle Hook'),
        arrow('a2', 'eb', 'ssm'),
        arrow('a3', 'ssm', 'doc'),
        arrow('a4', 'doc', 's3'),
        arrow('a5', 'doc', 'complete'),
        note('good', '✅ Lifecycle Hook で「終了前に待機」→ EventBridge で検知 → SSM でログを S3 に送信してから CompleteLifecycleAction',
             20, 270, w=960, h=50, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ UserData の shutdown trap: AMI ごとに実装 + 再現性低\n❌ CloudWatch Agent のみ: 終了直前のログが未送信で消失するリスク',
             20, 340, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Hook の Heartbeat Timeout を超えると強制 Continue/Abandon。スクリプトの最大実行時間に注意',
             20, 420, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '📌 ASG イベント種別: instance-launch / instance-terminate / instance-refresh → EventBridge で検知可能',
             20, 480, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'asg-eventbridge-ssm-s3'


def make_udemy_322():
    """IAM Access Analyzer -> EventBridge -> SNS"""
    title_text = "UDEMY-322 / S3 意図せぬ公開検知: IAM Access Analyzer → EventBridge (isPublic:true) → SNS"
    sub = "パブリック公開発見を EventBridge パターンでフィルタし、セキュリティチームに即時通知"
    cells = [
        title(title_text),
        subtitle(sub),
        icon('s3', 's3', 40, 130, label='S3 Buckets\n(監査対象)'),
        icon('aa', 'access_analyzer', 210, 130, label='IAM Access\nAnalyzer'),
        icon('eb', 'eventbridge', 380, 130, label='EventBridge Rule\n"isPublic: true"'),
        icon('sns', 'sns', 550, 130, label='SNS Topic'),
        generic_icon('sec', 'SecOps Team\n(Email/Slack)', 720, 140, w=150, h=50, fill='#FDECEA', stroke='#DD344C'),
        icon('lambda', 'lambda', 550, 280, label='Lambda\n(Auto Remediate)'),
        arrow('a1', 's3', 'aa', 'continuous scan'),
        arrow('a2', 'aa', 'eb', 'Finding'),
        arrow('a3', 'eb', 'sns'),
        arrow('a4', 'sns', 'sec'),
        arrow('a5', 'eb', 'lambda', 'auto-fix'),
        note('good', '✅ Access Analyzer は「外部アクセス」をポリシー解析で自動発見 → EventBridge の Finding イベントで監視',
             20, 360, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ CloudTrail だけを監視: 公開設定済みバケットの「現状」検出は困難\n❌ Config ルール: Access Analyzer の方が論理到達可能性を数学的に検証',
             20, 420, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 EventBridge Pattern: {"detail":{"isPublic":[true]}} で pub 化のみ抽出。Lambda で BlockPublicAccess を自動適用も可能',
             20, 500, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'access-analyzer-eb-sns'


def make_udemy_346():
    """S3 Object-level -> CloudTrail -> EventBridge -> SNS"""
    title_text = "UDEMY-346 / S3 API 操作検知: CloudTrail Data Events → EventBridge → SNS 通知"
    sub = "PutObject / DeleteObject をリアルタイム検知 — オブジェクトレベル監査の標準形"
    cells = [
        title(title_text),
        subtitle(sub),
        icon('s3', 's3', 40, 130, label='S3 Bucket'),
        icon('ct', 'cloudtrail', 210, 130, label='CloudTrail\n(Data Event ON)'),
        icon('eb', 'eventbridge', 380, 130, label='EventBridge\n(eventName: PutObject)'),
        icon('sns', 'sns', 550, 130, label='SNS Topic'),
        generic_icon('sec', 'SecOps / Slack', 710, 140, w=150, h=50, fill='#FDECEA', stroke='#DD344C'),
        icon('lambda', 'lambda', 550, 280, label='Lambda\n(Context Enrich)'),
        icon('s3log', 's3', 710, 280, label='S3 Archive'),
        arrow('a1', 's3', 'ct', 'Data Event'),
        arrow('a2', 'ct', 'eb'),
        arrow('a3', 'eb', 'sns'),
        arrow('a4', 'sns', 'sec'),
        arrow('a5', 'eb', 'lambda'),
        arrow('a6', 'lambda', 's3log'),
        note('good', '✅ CloudTrail Data Events は S3 オブジェクトレベル API をキャプチャ → EventBridge で eventName 条件フィルタ',
             20, 360, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ S3 Event Notification 単体: ユーザー特定情報・認証経路が不足\n❌ CloudTrail → CloudWatch Logs → Metric Filter: ほぼリアルタイムだが、EventBridge のほうが配信が直接的',
             20, 420, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Data Events は管理イベントと別課金。必要なバケットのみ ON にしてコスト最適化',
             20, 500, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'cloudtrail-eb-sns-s3'


def make_udemy_268():
    """EventBridge scheduled -> Lambda -> EC2 start/stop"""
    title_text = "UDEMY-268 / EventBridge スケジュール → Lambda が EC2 停止/起動 (夜間・週末コスト削減)"
    sub = "タグで対象を絞り、cron 式でスケジュール管理 — ASG 不要の軽量パターン"
    cells = [
        title(title_text),
        subtitle(sub),
        icon('eb1', 'eventbridge', 80, 130, label='EventBridge Rule\n(平日 20:00 停止)'),
        icon('eb2', 'eventbridge', 80, 280, label='EventBridge Rule\n(平日 8:00 起動)'),
        icon('l1', 'lambda', 280, 130, label='Stop Lambda\n(tag=env:dev)'),
        icon('l2', 'lambda', 280, 280, label='Start Lambda\n(tag=env:dev)'),
        icon('ec2_1', 'ec2', 480, 130, label='EC2 Dev Instance\n(StopInstances)'),
        icon('ec2_2', 'ec2', 480, 280, label='EC2 Dev Instance\n(StartInstances)'),
        generic_icon('cost', '💰 月 60% コスト削減\n(平日夜 + 週末 48h)', 680, 200, w=200, h=80, fill='#EAF5E0', stroke='#7AA116'),
        arrow('a1', 'eb1', 'l1', 'cron(0 20 ? * MON-FRI *)'),
        arrow('a2', 'l1', 'ec2_1'),
        arrow('a3', 'eb2', 'l2', 'cron(0 8 ? * MON-FRI *)'),
        arrow('a4', 'l2', 'ec2_2'),
        note('good', '✅ EventBridge Scheduler / Rule = サーバーレス cron。Lambda が AWS SDK で Stop/Start API を呼ぶのが最小構成',
             20, 380, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ Systems Manager Maintenance Window: リソースの補修向け、停止/起動の定期運用には EventBridge が軽量\n❌ CloudFormation + Lambda 直書き: スケジュール定義がコードに埋没して変更しづらい',
             20, 440, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Instance Scheduler (AWS Solutions) を使えばタグ "Schedule=office-hours" だけで完結。EB + Lambda の管理コードが不要',
             20, 520, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'eb-schedule-lambda-ec2'


def make_udemy_283():
    """EventBridge scheduled -> Fargate RunTask"""
    title_text = "UDEMY-283 / 8時間毎バッチ: EventBridge → Fargate RunTask (最小管理・最小コスト)"
    sub = "Fargate タスクを EventBridge が直接起動 — EC2 管理ゼロ・分単位課金"
    cells = [
        title(title_text),
        subtitle(sub),
        icon('eb', 'eventbridge', 140, 130, label='EventBridge\ncron(0 */8 * * ? *)'),
        icon('ecs', 'ecs', 320, 130, label='ECS Cluster\n(Fargate)'),
        icon('task', 'fargate', 500, 130, label='Fargate Task\n(Batch Image)'),
        icon('s3in', 's3', 680, 130, label='S3 Input'),
        icon('s3out', 's3', 680, 280, label='S3 Output'),
        icon('ddb', 'dynamodb', 840, 200, label='DynamoDB\n(Job Status)'),
        arrow('a1', 'eb', 'ecs', 'RunTask API'),
        arrow('a2', 'ecs', 'task'),
        arrow('a3', 'task', 's3in', 'read', dashed=True),
        arrow('a4', 'task', 's3out', 'write'),
        arrow('a5', 'task', 'ddb', 'status'),
        note('good', '✅ EventBridge は Fargate/ECS タスクをターゲットとして直接起動可能 → Lambda 不要・実行時間制限なし',
             20, 380, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ Lambda で 15 分超バッチ: 制限超過で失敗。Fargate なら長時間 OK\n❌ 常時 EC2: アイドルコスト発生',
             20, 440, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Fargate Spot 併用で最大 70% 削減。EventBridge の input 変換でタスク引数を動的注入可能',
             20, 520, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'eb-schedule-fargate'


def make_udemy_249():
    """Decouple: Lambda -> SQS -> external API call"""
    title_text = "UDEMY-249 / 外部 API 遅延を吸収: Lambda → SQS キュー → Worker Lambda → External API"
    sub = "遅い API の応答待ちでフロント Lambda が詰まらない — バッファ + 非同期が基本"
    cells = [
        title(title_text),
        subtitle(sub),
        generic_icon('client', 'Web Client', 40, 140, w=100, h=50, fill='#E8F2FD', stroke='#3B48CC'),
        icon('apigw', 'api_gateway', 170, 130, label='API Gateway'),
        icon('l1', 'lambda', 320, 130, label='Front Lambda\n(即時 Ack)'),
        icon('sqs', 'sqs', 470, 130, label='SQS Queue'),
        icon('l2', 'lambda', 620, 130, label='Worker Lambda'),
        generic_icon('ext', 'External API\n(遅い/不安定)', 780, 140, w=140, h=50, fill='#F2F2F2', stroke='#666'),
        icon('dlq', 'sqs', 620, 280, label='DLQ', color='#DD344C'),
        arrow('a1', 'client', 'apigw'),
        arrow('a2', 'apigw', 'l1'),
        arrow('a3', 'l1', 'sqs', 'SendMessage'),
        arrow('a4', 'sqs', 'l2', 'poll'),
        arrow('a5', 'l2', 'ext', 'HTTP'),
        arrow('a6', 'l2', 'dlq', '失敗', color='#DD344C'),
        note('good', '✅ SQS が「緩衝材」— 外部 API 障害時もメッセージ保持。Worker 側リトライで最終整合性',
             20, 360, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ Lambda 同期呼び出し: 外部 API の遅延分ユーザー待ち + タイムアウト連鎖\n❌ SNS: メッセージ消失リスク、キュー永続化特性なし',
             20, 420, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 SQS Visibility Timeout = Worker 処理時間 × 1.5 が目安。Batch 処理で ESM の maxBatchingWindow を活用',
             20, 500, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sqs-decouple-external-api'


def make_udemy_062():
    """S3 upload -> SQS -> Lambda video processing -> S3 -> CloudFront"""
    title_text = "UDEMY-062 / 動画アップロード: S3 → SQS → Lambda 並列処理 → S3 → CloudFront 配信"
    sub = "S3 イベント通知を SQS で受け、スパイクを吸収して Lambda を安定起動"
    cells = [
        title(title_text),
        subtitle(sub),
        icon('s3u', 's3', 40, 130, label='S3 Upload\nBucket'),
        icon('sqs', 'sqs', 200, 130, label='SQS Queue\n(Event Buffer)'),
        icon('lambda', 'lambda', 360, 130, label='Lambda\n(Process+Tag)'),
        icon('s3p', 's3', 520, 130, label='S3 Processed\nBucket'),
        icon('cf', 'cloudfront', 680, 130, label='CloudFront'),
        generic_icon('user', 'Global Viewers', 840, 140, w=140, h=50, fill='#E8F2FD', stroke='#3B48CC'),
        icon('dlq', 'sqs', 360, 280, label='SQS DLQ', color='#DD344C'),
        arrow('a1', 's3u', 'sqs', 'ObjectCreated'),
        arrow('a2', 'sqs', 'lambda', 'ESM batch=10'),
        arrow('a3', 'lambda', 's3p'),
        arrow('a4', 's3p', 'cf'),
        arrow('a5', 'cf', 'user'),
        arrow('a6', 'lambda', 'dlq', '失敗', color='#DD344C'),
        note('good', '✅ S3→SNS→SQS や S3→SQS 直は公式対応。SQS 経由で突発スパイク時の Lambda スロットリング対策',
             20, 360, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ S3 → Lambda 直: 瞬間的に数千件発火すると同時実行数上限を超え失敗\n❌ EC2 + Cron: 常駐コスト + スケール遅延',
             20, 420, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Lambda 同時実行数の Reserved Concurrency 設定でダウンストリーム保護。バッチサイズ最大 10000 (KDS) / 10 (SQS)',
             20, 500, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'video-s3-sqs-lambda'


def make_udemy_150():
    """S3 upload -> SQS -> Lambda image resize -> S3 IA"""
    title_text = "UDEMY-150 / 画像リサイズ: S3 Upload → SQS → Lambda Resize → S3 Standard-IA + LC"
    sub = "非同期処理でレスポンスを即返し、ストレージクラス遷移でコスト最適化"
    cells = [
        title(title_text),
        subtitle(sub),
        generic_icon('user', 'User Upload', 40, 140, w=100, h=50, fill='#E8F2FD', stroke='#3B48CC'),
        icon('s3u', 's3', 180, 130, label='S3 Upload\n(Standard)'),
        icon('sqs', 'sqs', 340, 130, label='SQS Queue'),
        icon('lambda', 'lambda', 500, 130, label='Resize Lambda\n(Sharp/ImageMagick)'),
        icon('s3ia', 's3', 660, 130, label='S3 Standard-IA\n(Resized)'),
        generic_icon('lc', 'Lifecycle:\nStandard→IA 30日\n→ Glacier 90日\n→ Deep Archive 365日', 830, 130, w=150, h=90, fill='#FFF5EB', stroke='#FF9900'),
        arrow('a1', 'user', 's3u', 'PUT'),
        arrow('a2', 's3u', 'sqs', 'Event Notify'),
        arrow('a3', 'sqs', 'lambda'),
        arrow('a4', 'lambda', 's3ia'),
        arrow('a5', 's3ia', 'lc', 'age', dashed=True),
        note('good', '✅ SQS で非同期化 → Lambda スパイク対応。リサイズ済画像は IA へ (アクセス頻度低)',
             20, 290, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ 同期 Lambda: 数秒〜数十秒の処理でユーザー待ち。S3→Lambda 直でもバースト弱い\n❌ S3 Intelligent-Tiering: 小サイズ画像は最低保管日数コストが割高',
             20, 350, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 ライフサイクル遷移は最短 30 日 (Standard→IA)。128KB 未満オブジェクトは IA 移行非推奨',
             20, 430, w=960, h=40, fill='#FFF5EB', stroke='#FF9900'),
        note('tip2', '📌 サイズ別バリエーションが必要なら Lambda@Edge + CloudFront でオンデマンド生成も選択肢',
             20, 490, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'image-s3-sqs-lambda-lc'


def make_udemy_192():
    """SQS + ASG EC2 workers"""
    title_text = "UDEMY-192 / SQS + EC2 ASG で疎結合: Web → SQS → Auto Scaling Worker"
    sub = "キュー深度ベースの ASG で負荷に応じた水平スケール — 古典的・王道の非同期処理"
    cells = [
        title(title_text),
        subtitle(sub),
        generic_icon('client', 'Web Clients', 40, 140, w=100, h=50, fill='#E8F2FD', stroke='#3B48CC'),
        icon('alb', 'api_gateway', 170, 130, label='ALB / API'),
        icon('web', 'ec2', 320, 130, label='Web EC2\n(Producer)'),
        icon('sqs', 'sqs', 470, 130, label='SQS Queue'),
        icon('worker', 'ec2', 620, 130, label='Worker ASG\n(Consumer)'),
        icon('ddb', 'dynamodb', 780, 130, label='DynamoDB\n(結果)'),
        generic_icon('cw', 'CloudWatch\nApproximateNumberOfMessages', 470, 280, w=260, h=60, fill='#FFF5EB', stroke='#FF9900'),
        arrow('a1', 'client', 'alb'),
        arrow('a2', 'alb', 'web'),
        arrow('a3', 'web', 'sqs', 'SendMessage'),
        arrow('a4', 'sqs', 'worker', 'ReceiveMessage'),
        arrow('a5', 'worker', 'ddb'),
        arrow('a6', 'sqs', 'cw', 'depth metric', dashed=True),
        arrow('a7', 'cw', 'worker', 'Scale Out/In', dashed=True),
        note('good', '✅ SQS が Web と Worker を完全分離。Worker 障害でもメッセージは Visibility Timeout 後に復活',
             20, 370, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ Web が Worker を直接呼ぶ: Worker ダウンで Web も影響、スケーリング整合性が崩れる\n❌ SNS: メッセージの再配信制御や Visibility Timeout がない',
             20, 430, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 Target Tracking Scaling: ApproximateNumberOfMessagesVisible / Instance 数で目標値を保つ',
             20, 510, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'sqs-asg-ec2-decouple'


def make_udemy_059():
    """AppSync + DDB Streams + Lambda + WebSocket subscriptions"""
    title_text = "UDEMY-059 / AppSync + DynamoDB Streams + Lambda で WebSocket リアルタイム配信"
    sub = "DB 変更 → Streams → Lambda → AppSync Mutation → Subscription で全クライアント Push"
    cells = [
        title(title_text),
        subtitle(sub),
        generic_icon('client', 'Mobile / Web\n(WebSocket)', 40, 140, w=110, h=50, fill='#E8F2FD', stroke='#3B48CC'),
        icon('apsy', 'appsync', 190, 130, label='AppSync\nGraphQL API'),
        icon('ddb', 'dynamodb', 350, 130, label='DynamoDB\n(Reaction Table)'),
        icon('strm', 'dynamodb', 510, 130, label='DynamoDB Streams', color='#C925D1'),
        icon('lambda', 'lambda', 670, 130, label='Lambda\n(Publish Mutation)'),
        icon('apsy2', 'appsync', 830, 130, label='AppSync\nSubscription'),
        generic_icon('clients', 'All Readers\n(Real-time Push)', 670, 300, w=180, h=60, fill='#E8F2FD', stroke='#3B48CC'),
        arrow('a1', 'client', 'apsy', 'Mutation\n(Add Reaction)'),
        arrow('a2', 'apsy', 'ddb', 'PutItem'),
        arrow('a3', 'ddb', 'strm'),
        arrow('a4', 'strm', 'lambda', 'Event Source'),
        arrow('a5', 'lambda', 'apsy2', 'GraphQL Mutation'),
        arrow('a6', 'apsy2', 'clients', 'Subscription'),
        note('good', '✅ 正解: DDB Streams → Lambda → AppSync Mutation で全サブスクライバに WebSocket Push',
             20, 380, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ API Gateway WebSocket で自前配信: 接続管理・スケーリング・再接続ロジックを実装\n❌ SNS Mobile Push のみ: リアルタイム双方向通信ではない',
             20, 440, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 AppSync の Subscription は Mutation 名とフィルタで対象絞込可能。接続管理は完全マネージド',
             20, 520, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'appsync-ddbstream-realtime'


def make_udemy_366():
    """ALB/WAF logs -> Kinesis Data Streams -> third-party audit + S3"""
    title_text = "UDEMY-366 / ALB + WAF ログ: Kinesis Data Streams → 3rd Party Audit + Firehose → S3"
    sub = "WAF ログは Firehose ネイティブ、ALB ログは S3 経由 — リアルタイム監査にストリーム分岐"
    cells = [
        title(title_text),
        subtitle(sub),
        icon('alb', 'api_gateway', 40, 130, label='ALB\n(Access Logs)'),
        icon('waf', 'waf', 40, 280, label='WAF\n(Web ACL Logs)'),
        icon('kds', 'kinesis_data_streams', 240, 200, label='Kinesis Data\nStreams'),
        icon('firehose', 'kinesis_data_firehose', 420, 120, label='Firehose'),
        generic_icon('audit', '3rd Party\nAudit App', 420, 280, w=130, h=50, fill='#F2F2F2', stroke='#666'),
        icon('s3', 's3', 600, 120, label='S3 Long-term\n(Audit Archive)'),
        icon('athena', 'athena', 770, 120, label='Athena\n(Forensics)'),
        generic_icon('soc', 'SOC Team\nDashboard', 600, 280, w=130, h=50, fill='#E8F2FD', stroke='#3B48CC'),
        arrow('a1', 'alb', 'kds', 'Access Log'),
        arrow('a2', 'waf', 'kds', 'WAF Log'),
        arrow('a3', 'kds', 'firehose'),
        arrow('a4', 'kds', 'audit'),
        arrow('a5', 'firehose', 's3'),
        arrow('a6', 's3', 'athena'),
        arrow('a7', 'audit', 'soc'),
        note('good', '✅ Kinesis Data Streams が「ストリーム分岐ハブ」— 複数 Consumer に同時配信 (Enhanced Fan-out)',
             20, 380, w=960, h=40, fill='#EAF5E0', stroke='#7AA116'),
        note('bad', '❌ CloudWatch Logs だけ: サブスクリプションフィルタ経由にしても Firehose 直のほうがスループット高\n❌ ALB ログを S3 だけ: 3rd Party へのリアルタイム連携ができない',
             20, 440, w=960, h=60, fill='#FDECEA', stroke='#DD344C'),
        note('tip', '💡 WAF は Firehose への直接ログ配信対応。ALB アクセスログは 5 分バッファで S3 へ',
             20, 520, w=960, h=40, fill='#E8F2FD', stroke='#3B48CC'),
    ]
    return '\n'.join(cells), 'alb-waf-kds-firehose'


# Register all
REGISTRY = [
    ('UDEMY-050', make_udemy_050),
    ('UDEMY-328', make_udemy_328),
    ('UDEMY-045', make_udemy_045),
    ('UDEMY-065', make_udemy_065),
    ('UDEMY-015', make_udemy_015),
    ('UDEMY-097', make_udemy_097),
    ('UDEMY-011', make_udemy_011),
    ('UDEMY-013', make_udemy_013),
    ('UDEMY-018', make_udemy_018),
    ('UDEMY-026', make_udemy_026),
    ('UDEMY-373', make_udemy_373),
    ('UDEMY-287', make_udemy_287),
    ('UDEMY-336', make_udemy_336),
    ('UDEMY-315', make_udemy_315),
    ('UDEMY-164', make_udemy_164),
    ('UDEMY-322', make_udemy_322),
    ('UDEMY-346', make_udemy_346),
    ('UDEMY-268', make_udemy_268),
    ('UDEMY-283', make_udemy_283),
    ('UDEMY-249', make_udemy_249),
    ('UDEMY-062', make_udemy_062),
    ('UDEMY-150', make_udemy_150),
    ('UDEMY-192', make_udemy_192),
    ('UDEMY-059', make_udemy_059),
    ('UDEMY-366', make_udemy_366),
]


def main():
    created = 0
    skipped = 0
    for qid, fn in REGISTRY:
        fp = OUT / f'{qid}.drawio'
        if fp.exists():
            print(f'SKIP {qid}: exists')
            skipped += 1
            continue
        content, diag_id = fn()
        xml = drawio_wrap(content, diag_id, qid)
        fp.write_text(xml)
        print(f'WROTE {fp}')
        created += 1
    print(f'\nCreated: {created}, Skipped: {skipped}')


if __name__ == '__main__':
    main()
