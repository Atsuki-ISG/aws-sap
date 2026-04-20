#!/usr/bin/env python3
"""
Generate per-question drawio files for CloudTech (SAP-*) DR / Multi-Region questions.
1000x600, white background, AWS official icons.
Icon 50x50, labels at icon.y + 58 to avoid overlap.
"""
import os

OUT_DIR = '/Users/aki/aws-sap/docs/diagrams/per-question'
os.makedirs(OUT_DIR, exist_ok=True)

AWS_ORANGE = '#FF9900'
AWS_BLUE   = '#3B48CC'
AWS_GREEN  = '#7AA116'
AWS_RED    = '#DD344C'
AWS_PINK   = '#E7157B'
AWS_PURPLE = '#8C4FFF'
NAVY       = '#232F3E'
GRAY       = '#666666'


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;').replace('\n', '&#10;'))


def header(title, width=1000, height=600):
    return f'''<mxfile host="app.diagrams.net" modified="2026-04-20T00:00:00.000Z" agent="Claude" version="24.0.0">
  <diagram id="d" name="diagram">
    <mxGraphModel dx="1422" dy="757" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{width}" pageHeight="{height}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="title" value="{esc(title)}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=15;fontStyle=1;fontColor={NAVY};" vertex="1" parent="1">
          <mxGeometry x="0" y="6" width="{width}" height="26" as="geometry" />
        </mxCell>
'''

FOOTER = '''      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''


def region(id_, label, x, y, w, h, color=AWS_BLUE):
    return f'''        <mxCell id="{id_}" value="{esc(label)}" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;strokeColor={color};fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor={color};dashed=0;" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
        </mxCell>
'''


def dc(id_, label, x, y, w, h, color=GRAY):
    return f'''        <mxCell id="{id_}" value="{esc(label)}" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_corporate_data_center;strokeColor={color};fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor={color};dashed=0;" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
        </mxCell>
'''


def icon(id_, x, y, res, fill, label='', label_w=140, label_offset=58, font_size=10, bold=False):
    out = f'''        <mxCell id="{id_}" value="" style="sketch=0;outlineConnect=0;fontColor={NAVY};gradientColor=none;fillColor={fill};strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=10;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{res};" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="50" height="50" as="geometry" />
        </mxCell>
'''
    if label:
        style = f'text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize={font_size};fontColor={NAVY};'
        if bold:
            style += 'fontStyle=1;'
        lx = x + 25 - label_w // 2
        ly = y + label_offset
        out += f'''        <mxCell id="{id_}_l" value="{esc(label)}" style="{style}" vertex="1" parent="1">
          <mxGeometry x="{lx}" y="{ly}" width="{label_w}" height="30" as="geometry" />
        </mxCell>
'''
    return out


def text_box(id_, x, y, w, h, text, color=NAVY, font_size=10, bold=False, align='left', bg=None, stroke=None):
    if bg:
        style = f'rounded=1;whiteSpace=wrap;html=1;fillColor={bg};strokeColor={stroke or color};strokeWidth=1;fontSize={font_size};fontColor={color};verticalAlign=top;align={align};spacingTop=6;spacingLeft=8;spacingRight=8;'
        if bold:
            style += 'fontStyle=1;'
    else:
        style = f'text;html=1;align={align};verticalAlign=top;whiteSpace=wrap;fontSize={font_size};fontColor={color};'
        if bold:
            style += 'fontStyle=1;'
    return f'''        <mxCell id="{id_}" value="{esc(text)}" style="{style}" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
        </mxCell>
'''


def arrow(id_, src, tgt, color=NAVY, width=2, dashed=False, label='', label_bg='#FFFFFF'):
    dash_attr = 'dashed=1;' if dashed else ''
    out = f'''        <mxCell id="{id_}" style="endArrow=classic;html=1;strokeColor={color};strokeWidth={width};{dash_attr}" edge="1" parent="1" source="{src}" target="{tgt}">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
'''
    if label:
        out += f'''        <mxCell id="{id_}_l" value="{esc(label)}" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=9;fontColor={color};labelBackgroundColor={label_bg};" vertex="1" connectable="0" parent="{id_}">
          <mxGeometry x="-0.05" relative="1" as="geometry"><mxPoint as="offset"/></mxGeometry>
        </mxCell>
'''
    return out


def bi_arrow(id_, src, tgt, color=NAVY, width=2, dashed=False, label=''):
    dash_attr = 'dashed=1;' if dashed else ''
    out = f'''        <mxCell id="{id_}" style="endArrow=classic;startArrow=classic;html=1;strokeColor={color};strokeWidth={width};{dash_attr}" edge="1" parent="1" source="{src}" target="{tgt}">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
'''
    if label:
        out += f'''        <mxCell id="{id_}_l" value="{esc(label)}" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=9;fontColor={color};labelBackgroundColor=#FFFFFF;" vertex="1" connectable="0" parent="{id_}">
          <mxGeometry x="-0.05" relative="1" as="geometry"><mxPoint as="offset"/></mxGeometry>
        </mxCell>
'''
    return out


def write(qid, content):
    path = os.path.join(OUT_DIR, f'{qid}.drawio')
    with open(path, 'w') as f:
        f.write(content)
    print(f'wrote {path}')


# =====================================================================
# SAP-3  Answer A: AWS Elastic Disaster Recovery
# =====================================================================
def sap_003():
    s = header('SAP-3 / 正解A: AWS Elastic DR (継続レプリ+ワンクリックフェールバック)')
    s += dc('op', 'オンプレミス DC (vSphere VM)', 20, 60, 420, 440)
    s += icon('win', 70, 120, 'ec2', GRAY, 'Windows Server\n(医療アプリ)', 140, 58, 9, True)
    s += icon('disk', 230, 120, 'backup', GRAY, '独自形式データ\n(ローカルディスク)', 150, 58, 9, True)
    s += icon('drs_agt', 70, 250, 'cloudendure_disaster_recovery', AWS_RED, 'DRS Agent\n(継続ブロックレプリ)', 170, 58, 9, True)
    s += text_box('op_note', 40, 360, 380, 120,
                  '【要件】\n・RPO 最大15分\n・継続レプリケーション\n・ワンクリックでフェールバック\n・平常時は運用コスト最小', GRAY, 10)

    s += region('aws', 'AWS Region (DR先)', 480, 60, 500, 440, AWS_BLUE)
    s += icon('stage', 540, 130, 'cloudendure_disaster_recovery', AWS_RED,
              'Elastic DR\nステージング領域', 170, 58, 9, True)
    s += icon('ec2_dr', 740, 130, 'ec2', AWS_ORANGE,
              'DR EC2\n(障害時に起動)', 150, 58, 9, True)
    s += text_box('aws_note', 500, 260, 460, 100,
                  '【DR発動】\n・ワンクリックで EC2 を起動 → RPO<15分達成\n・Launch 時のみ課金 (平常時は安価なステージングのみ)\n・復旧後はフェールバック機能でオンプレへ戻す', AWS_BLUE, 10)

    s += arrow('r1', 'drs_agt', 'stage', AWS_RED, 3, False, 'ブロックレベル継続レプリ')
    s += arrow('r2', 'stage', 'ec2_dr', AWS_RED, 2, True, '障害時に起動')
    s += arrow('fb', 'ec2_dr', 'drs_agt', AWS_PURPLE, 2, True, 'フェールバック')

    s += text_box('cmp', 20, 510, 960, 80,
                  '✅ A=AWS Elastic DR: 3要件(継続レプリ/RPO15分/ワンクリックFB)を全て満たす唯一解\n'
                  '❌ B: CloudEndure Migration は移行ツール (DR/フェールバック機能なし)\n'
                  '❌ C: AWS Backup は RPO 15分/継続レプリ非対応 (スナップショット間隔以上)\n'
                  '❌ D: Storage Gateway はストレージ統合、DR オーケストレーション機能なし',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-3', s)


# =====================================================================
# SAP-39  Answer D: Organizations + CloudFormation StackSets
# =====================================================================
def sap_039():
    s = header('SAP-39 / 正解D: Organizations + CloudFormation StackSets (マルチアカウント×マルチリージョン展開)')

    s += region('mgmt', '管理アカウント', 20, 60, 260, 200, AWS_PURPLE)
    s += icon('cfn', 80, 130, 'cloudwatch', AWS_PURPLE, 'CloudFormation\nStackSets', 150, 58, 9, True)
    s += text_box('mnote', 40, 220, 220, 30, '単一テンプレート→一括デプロイ', AWS_PURPLE, 9)

    # targets per OU
    s += region('r1', 'アカウントA / us-east-1', 320, 60, 320, 150, AWS_BLUE)
    s += icon('s1', 370, 110, 'cloudwatch', AWS_BLUE, 'Stack (同一)', 120, 58, 9)

    s += region('r2', 'アカウントA / eu-west-1', 660, 60, 320, 150, AWS_GREEN)
    s += icon('s2', 710, 110, 'cloudwatch', AWS_GREEN, 'Stack (同一)', 120, 58, 9)

    s += region('r3', 'アカウントB / us-east-1', 320, 230, 320, 150, AWS_BLUE)
    s += icon('s3', 370, 280, 'cloudwatch', AWS_BLUE, 'Stack (同一)', 120, 58, 9)

    s += region('r4', 'アカウントB / eu-west-1', 660, 230, 320, 150, AWS_GREEN)
    s += icon('s4', 710, 280, 'cloudwatch', AWS_GREEN, 'Stack (同一)', 120, 58, 9)

    s += arrow('a1', 'cfn', 's1', AWS_PURPLE, 2, False)
    s += arrow('a2', 'cfn', 's2', AWS_PURPLE, 2, False)
    s += arrow('a3', 'cfn', 's3', AWS_PURPLE, 2, False)
    s += arrow('a4', 'cfn', 's4', AWS_PURPLE, 2, False)

    s += text_box('cmp', 20, 400, 960, 180,
                  '✅ D=Organizations + StackSets: OU指定で「マルチアカウント × マルチリージョン」を単一テンプレートから展開。バージョン更新時もスタックセットの更新で全ターゲットへ自動反映。\n\n'
                  '❌ A: 各リージョンに手動スタック展開 → スケールしない／更新時の差分発生リスク\n'
                  '❌ B: Terraform は AWS ネイティブではなく、既存 CFn 資産から乗り換えが必要 (運用コスト増)\n'
                  '❌ C: CodePipeline での個別デプロイ → テンプレート更新の一括適用が難しく、差分管理が煩雑\n\n'
                  '💡 StackSets の強み: 「デプロイ対象 = OU or アカウントリスト」×「リージョンリスト」で直積一括管理',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-39', s)


# =====================================================================
# SAP-71  Answer D: AWS Global Accelerator (UDP ゲーム)
# =====================================================================
def sap_071():
    s = header('SAP-71 / 正解D: AWS Global Accelerator (UDP グローバルゲーム / 固定Anycast IP)')

    # User clients
    s += text_box('user', 20, 60, 140, 60, 'ゲームクライアント\n(世界中のプレイヤー)\nUDP接続', NAVY, 10, True, 'center', '#EAF4FF', AWS_BLUE)

    s += icon('ga', 200, 70, 'route_53', AWS_PURPLE, 'Global Accelerator\n(固定Anycast IP×2)', 170, 58, 10, True)

    s += region('r1', 'eu-west-1 (EU)', 420, 60, 260, 160, AWS_GREEN)
    s += icon('alb1', 470, 130, 'application_load_balancer', AWS_PURPLE, 'NLB / ALB')
    s += icon('ec2_1', 580, 130, 'ec2', AWS_ORANGE, 'ゲームサーバ')

    s += region('r2', 'us-east-1 (NA)', 700, 60, 260, 160, AWS_GREEN)
    s += icon('alb2', 750, 130, 'application_load_balancer', AWS_PURPLE, 'NLB / ALB')
    s += icon('ec2_2', 860, 130, 'ec2', AWS_ORANGE, 'ゲームサーバ')

    s += region('r3', 'ap-northeast-1 (Asia)', 560, 240, 260, 160, AWS_GREEN)
    s += icon('alb3', 610, 310, 'application_load_balancer', AWS_PURPLE, 'NLB / ALB')
    s += icon('ec2_3', 720, 310, 'ec2', AWS_ORANGE, 'ゲームサーバ')

    s += arrow('u1', 'user', 'ga', NAVY, 3, False, 'UDP')
    s += arrow('g1', 'ga', 'alb1', AWS_PURPLE, 2, False, '最寄り')
    s += arrow('g2', 'ga', 'alb2', AWS_PURPLE, 2, False, '最寄り')
    s += arrow('g3', 'ga', 'alb3', AWS_PURPLE, 2, False, '最寄り')

    s += text_box('cmp', 20, 420, 960, 170,
                  '✅ D=Global Accelerator: UDP/TCP 対応、AWSバックボーン経由で低遅延、固定Anycast IP を維持したままリージョン追加可能\n\n'
                  '❌ A: Route 53 レイテンシールーティング = DNS解決時のみ最適化。IP変動・セッション中の経路最適化なし\n'
                  '❌ B: CloudFront = HTTP/HTTPS 専用、UDPゲームトラフィックには非対応\n'
                  '❌ C: Route 53 + CloudFront 組合せも UDP 非対応\n\n'
                  '💡 GA vs CloudFront: GA=L4(TCP/UDP)+Anycast IP、CloudFront=L7 HTTPキャッシュ',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-71', s)


# =====================================================================
# SAP-106  Answer A: Direct Connect Gateway + Transit Gateway (マルチリージョン閉域)
# =====================================================================
def sap_106():
    s = header('SAP-106 / 正解A: DX Gateway + TGW (マルチリージョン閉域接続)')

    s += dc('op', 'オンプレミス (企業WAN)', 20, 60, 300, 260)
    s += icon('dx1', 60, 130, 'backup', GRAY, 'DX1 (冗長)', 120, 58, 9, True)
    s += icon('dx2', 180, 130, 'backup', GRAY, 'DX2 (冗長)', 120, 58, 9, True)

    s += icon('dxgw', 360, 140, 'route_53', AWS_PURPLE,
              'Direct Connect\nGateway', 160, 58, 10, True)

    s += region('r1', 'us-east-1', 560, 60, 200, 150, AWS_BLUE)
    s += icon('tgw1', 600, 120, 'route_53', AWS_PURPLE, 'TGW', 90, 58, 9, True)
    s += icon('vpc1', 690, 120, 's3', AWS_GREEN, 'VPC/S3')

    s += region('r2', 'eu-west-1', 780, 60, 200, 150, AWS_BLUE)
    s += icon('tgw2', 820, 120, 'route_53', AWS_PURPLE, 'TGW', 90, 58, 9, True)
    s += icon('vpc2', 910, 120, 's3', AWS_GREEN, 'VPC/S3')

    s += region('r3', 'ap-northeast-1', 560, 240, 200, 150, AWS_BLUE)
    s += icon('tgw3', 600, 300, 'route_53', AWS_PURPLE, 'TGW', 90, 58, 9, True)
    s += icon('vpc3', 690, 300, 's3', AWS_GREEN, 'VPC/S3')

    s += region('r4', 'ap-southeast-1', 780, 240, 200, 150, AWS_BLUE)
    s += icon('tgw4', 820, 300, 'route_53', AWS_PURPLE, 'TGW', 90, 58, 9, True)
    s += icon('vpc4', 910, 300, 's3', AWS_GREEN, 'VPC/S3')

    s += arrow('d1', 'dx1', 'dxgw', GRAY, 2, False, '冗長DX')
    s += arrow('d2', 'dx2', 'dxgw', GRAY, 2, False)
    s += arrow('gw1', 'dxgw', 'tgw1', AWS_PURPLE, 2)
    s += arrow('gw2', 'dxgw', 'tgw2', AWS_PURPLE, 2)
    s += arrow('gw3', 'dxgw', 'tgw3', AWS_PURPLE, 2)
    s += arrow('gw4', 'dxgw', 'tgw4', AWS_PURPLE, 2)

    s += text_box('cmp', 20, 410, 960, 180,
                  '✅ A=DX Gateway + TGW: 冗長DX2本を DX Gateway に束ねて各リージョン TGW へ接続。全トラフィックは企業WAN内閉域。リージョン追加は TGW 追加のみ\n\n'
                  '❌ B: 各リージョンに個別DX → 高コスト／スケーラビリティ不足\n'
                  '❌ C: VPCピアリング = リージョン間 1:1、N×N で爆発／オンプレ非対応\n'
                  '❌ D: VPN はパブリックIP経由 = 閉域要件違反\n\n'
                  '💡 DX Gateway: 単一 DX から最大 50 VPC (複数リージョン) に閉域接続可能',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-106', s)


# =====================================================================
# SAP-125  Answer A, B: Aurora Global DB + Route 53 (地理的近接+フェイルオーバー)
# =====================================================================
def sap_125():
    s = header('SAP-125 / 正解A+B: Route 53 Geolocation+FO × Aurora Global DB (世界ログイン低遅延)')

    s += icon('r53', 450, 50, 'route_53', AWS_PURPLE,
              'Route 53\n地理的近接 + FO', 170, 58, 10, True)

    s += region('rna', 'us-east-1 (北米)', 20, 140, 440, 260, AWS_BLUE)
    s += icon('alb_na', 60, 200, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('ec2_na', 160, 200, 'ec2', AWS_ORANGE, '認証App', 110, 58, 9)
    s += icon('aw_na', 290, 200, 'aurora', AWS_BLUE,
              'Aurora Global DB\nPrimary (書込)', 170, 58, 9, True)
    s += text_box('nna', 40, 290, 420, 90,
                  '・全世界のユーザー書込はここへ集約\n・ストレージ6コピー(3AZ×2)\n・ローカル読取はRegionalリーダー', AWS_BLUE, 9)

    s += region('rap', 'ap-northeast-1 (アジア)', 520, 140, 440, 260, AWS_GREEN)
    s += icon('alb_ap', 560, 200, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('ec2_ap', 660, 200, 'ec2', AWS_ORANGE, '認証App', 110, 58, 9)
    s += icon('aw_ap', 790, 200, 'aurora', AWS_BLUE,
              'Aurora Global DB\nSecondary (R/昇格可)', 180, 58, 9, True)
    s += text_box('nap', 540, 290, 420, 90,
                  '・アジアユーザーの読取はローカルで数ms\n・障害時は Secondary を Promote → 書込可\n・RPO<1秒 / RTO<1分', AWS_GREEN, 9)

    s += arrow('r_na', 'r53', 'alb_na', AWS_PURPLE, 2, False, '北米ユーザー')
    s += arrow('r_ap', 'r53', 'alb_ap', AWS_PURPLE, 2, False, 'アジアユーザー')
    s += arrow('rep', 'aw_na', 'aw_ap', AWS_PINK, 4, False, 'ストレージ物理レプリ <1秒')

    s += text_box('cmp', 20, 420, 960, 170,
                  '✅ A=Route 53 地理的近接+フェイルオーバー: 平常時は最寄り、障害時は別リージョンへ自動切替\n'
                  '✅ B=Aurora Global Database: 単一書込リージョン + 各リージョン低遅延読取 + RPO<1秒\n\n'
                  '❌ C: 複数値回答ルーティング = クライアント選択依存、最寄り保証なし\n'
                  '❌ D: DynamoDB Global Tables = RDB のトランザクションセマンティクスなし (要件違反)\n'
                  '❌ E: RDS Multi-AZ のみ = 単一リージョン内HA、マルチリージョンDR非対応\n\n'
                  '💡 「RDBトランザクション維持 + マルチリージョン」= Aurora Global DB 一択',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-125', s)


# =====================================================================
# SAP-130  Answer A: Route 53 FO + Lambda (Pilot Light / RTO 15min)
# =====================================================================
def sap_130():
    s = header('SAP-130 / 正解A: Route 53 FO + Lambda 自動化 (Pilot Light / RTO 15分)')

    s += icon('r53', 450, 50, 'route_53', AWS_PURPLE,
              'Route 53\nフェイルオーバー', 170, 58, 10, True)

    s += region('rp', 'Primary Region', 20, 140, 440, 280, AWS_BLUE)
    s += icon('alb_p', 60, 200, 'application_load_balancer', AWS_PURPLE, 'ALB (稼働)')
    s += icon('ec2_p', 170, 200, 'ec2', AWS_ORANGE, 'EC2 ASG\n(本番容量)', 130, 58, 9, True)
    s += icon('rds_p', 310, 200, 'rds', AWS_BLUE, 'RDS Multi-AZ\n(書込)', 140, 58, 9, True)
    s += text_box('pn', 40, 290, 420, 120,
                  '平常時:\n・ALB + Auto Scaling で本番トラフィック処理\n・RDS Multi-AZ で AZ 障害に耐える\n・Read Replica を DR リージョンへ送出', AWS_BLUE, 9)

    s += region('rd', 'Secondary (Pilot Light)', 520, 140, 440, 280, AWS_GREEN)
    s += icon('alb_d', 560, 200, 'application_load_balancer', AWS_PURPLE, 'ALB (複製済)')
    s += icon('ec2_d', 670, 200, 'ec2', AWS_ORANGE,
              'ASG Min/Max=0\n(コスト0)', 130, 58, 9, True)
    s += icon('rds_d', 810, 200, 'rds', AWS_BLUE,
              'RDS RR\n(昇格待機)', 140, 58, 9, True)
    s += icon('lmb', 560, 310, 'cloudwatch', AWS_PURPLE,
              'Lambda\n(DR Orchestrator)', 160, 58, 9, True)
    s += text_box('dn', 720, 310, 240, 90,
                  'DR発動:\n①RR を Promote\n②ASG 容量引上\n③DNS切替\nRTO<15分', AWS_GREEN, 9)

    s += arrow('p_rep', 'rds_p', 'rds_d', AWS_PINK, 3, False, 'Cross-Region RR')
    s += arrow('r_p', 'r53', 'alb_p', AWS_PURPLE, 2, False, 'Primary')
    s += arrow('r_d', 'r53', 'alb_d', AWS_PURPLE, 2, True, 'Failover')
    s += arrow('l_d', 'lmb', 'ec2_d', AWS_PURPLE, 2, True, '容量UP')
    s += arrow('l_r', 'lmb', 'rds_d', AWS_PURPLE, 2, True, 'Promote')

    s += text_box('cmp', 20, 430, 960, 160,
                  '✅ A=Route 53 FO + Lambda: Pilot Light の王道。スタンバイ側 ASG Min=0 でコスト0、障害時に Lambda が自動拡張\n\n'
                  '❌ B: DynamoDB Global Tables は RDS MySQL からの移行が必要 (要件外)\n'
                  '❌ C: Warm Standby (常時本番容量) → SLA 15分に過剰、コスト増\n'
                  '❌ D: Backup & Restore = RTO 数時間。15分には間に合わない\n\n'
                  '💡 Pilot Light: 最小リソースを常時起動 + 障害時に Lambda でスケールアップ',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-130', s)


# =====================================================================
# SAP-155  Answer B: S3 CRR + CloudFront Origin Group + DynamoDB Global Tables
# =====================================================================
def sap_155():
    s = header('SAP-155 / 正解B: S3 CRR + CloudFront Origin FO + DynamoDB Global Tables (ゲーム世界同時配信)')

    s += text_box('pl', 20, 60, 130, 60, 'プレイヤー\n(世界中)', NAVY, 10, True, 'center', '#EAF4FF', AWS_BLUE)
    s += icon('cf', 190, 70, 'cloudfront', AWS_PURPLE,
              'CloudFront\nOrigin Group (FO)', 170, 58, 10, True)

    s += region('r1', 'us-east-1 (Primary)', 20, 170, 470, 260, AWS_BLUE)
    s += icon('s3_1', 60, 230, 's3', AWS_GREEN, 'S3 アセット\n(Primary)', 140, 58, 9, True)
    s += icon('ddb_1', 220, 230, 'dynamodb', AWS_BLUE,
              'DynamoDB GT\nスコア', 140, 58, 9, True)
    s += icon('ec2_1', 380, 230, 'ec2', AWS_ORANGE, 'ゲームAPI', 110, 58, 9)
    s += text_box('n1', 40, 330, 430, 80,
                  '・S3 にゲームアセット (数GB)\n・DynamoDB にスコア (ランキング)', AWS_BLUE, 9)

    s += region('r2', 'ap-northeast-1 (Secondary)', 510, 170, 470, 260, AWS_GREEN)
    s += icon('s3_2', 550, 230, 's3', AWS_GREEN,
              'S3 アセット\n(CRR レプリカ)', 150, 58, 9, True)
    s += icon('ddb_2', 720, 230, 'dynamodb', AWS_BLUE,
              'DynamoDB GT\nレプリカ', 140, 58, 9, True)
    s += icon('ec2_2', 880, 230, 'ec2', AWS_ORANGE, 'ゲームAPI', 110, 58, 9)
    s += text_box('n2', 530, 330, 430, 80,
                  '・S3 CRR で非同期レプリ (数分)\n・DynamoDB Global Tables = 全リージョン書込 (Active-Active)', AWS_GREEN, 9)

    s += arrow('c_s1', 'cf', 's3_1', AWS_PURPLE, 2, False, 'Primary Origin')
    s += arrow('c_s2', 'cf', 's3_2', AWS_PURPLE, 2, True, 'Failover Origin')
    s += arrow('u_cf', 'pl', 'cf', NAVY, 2)
    s += arrow('s_rep', 's3_1', 's3_2', AWS_PINK, 3, False, 'S3 CRR')
    s += bi_arrow('d_rep', 'ddb_1', 'ddb_2', AWS_PINK, 3, False, 'DynamoDB Streams 双方向')

    s += text_box('cmp', 20, 440, 960, 150,
                  '✅ B=S3 CRR + CloudFront Origin Group + DynamoDB Global Tables: 3要件すべて自動化\n'
                  '   - S3 CRR: アセットを別リージョンに自動レプリ\n'
                  '   - CloudFront Origin FO: Primary 障害時に Secondary S3 へ自動切替\n'
                  '   - DynamoDB GT: スコアを全リージョンで低遅延 R/W\n\n'
                  '❌ A: SRR (Same-Region Replication) = 同一リージョン内のみ。マルチリージョンにならない\n'
                  '❌ C: Global Accelerator は S3 のオリジン切替を行わない (L4 IP ルーティングのみ)\n'
                  '❌ D: 手動スクリプトでの S3 同期 = 運用負荷増＋整合性保証なし',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-155', s)


# =====================================================================
# SAP-160  Answer C: EBS Snapshot + DLM クロスリージョンコピー
# =====================================================================
def sap_160():
    s = header('SAP-160 / 正解C: Amazon DLM (EBSスナップショット複数リージョン自動コピー)')

    s += region('rp', 'Primary Region', 20, 70, 260, 280, AWS_BLUE)
    s += icon('ec2', 60, 140, 'ec2', AWS_ORANGE, 'EC2 (防災DB)', 130, 58, 9, True)
    s += icon('ebs', 180, 140, 'backup', AWS_GREEN, 'EBS Volume', 110, 58, 9, True)
    s += icon('snap', 60, 250, 'backup', AWS_BLUE,
              'EBS Snapshot\n(日次)', 120, 58, 9, True)

    s += icon('dlm', 340, 140, 'cloudwatch', AWS_PURPLE,
              'Data Lifecycle\nManager (DLM)', 170, 58, 10, True)
    s += text_box('dlm_note', 320, 220, 210, 90,
                  '単一ポリシーで:\n・日次スナップショット取得\n・複数リージョンへ自動コピー\n・保持期間管理', AWS_PURPLE, 9)

    s += region('r1', 'DR Region 1 (法令追加1)', 570, 70, 200, 150, AWS_GREEN)
    s += icon('snap1', 610, 130, 'backup', AWS_GREEN,
              'Snapshot Copy', 130, 58, 9, True)

    s += region('r2', 'DR Region 2 (法令追加2)', 790, 70, 200, 150, AWS_GREEN)
    s += icon('snap2', 830, 130, 'backup', AWS_GREEN,
              'Snapshot Copy', 130, 58, 9, True)

    s += region('r3', '(将来追加リージョン)', 680, 240, 260, 120, GRAY)
    s += icon('snap3', 770, 280, 'backup', GRAY,
              'Policy 変更のみ', 140, 58, 9)

    s += arrow('s1', 'ebs', 'snap', AWS_BLUE, 2, False, '日次')
    s += arrow('s2', 'dlm', 'snap', AWS_PURPLE, 2, False)
    s += arrow('c1', 'dlm', 'snap1', AWS_PURPLE, 2, False, '自動コピー')
    s += arrow('c2', 'dlm', 'snap2', AWS_PURPLE, 2, False, '自動コピー')
    s += arrow('c3', 'dlm', 'snap3', AWS_PURPLE, 2, True, 'ポリシーに追記だけ')

    s += text_box('cmp', 20, 380, 960, 210,
                  '✅ C=DLM クロスリージョンコピー: 単一ポリシーで「複数リージョンへの自動コピー」をネイティブサポート。スクリプト不要、リージョン追加はポリシー編集のみ\n\n'
                  '❌ A: Lambda + CloudWatch Events で独自スクリプト → 保守工数・権限管理が煩雑\n'
                  '❌ B: AWS Backup も候補だが、EBS専用最適・ライフサイクルポリシー制御の観点で DLM が本問の正解\n'
                  '❌ D: EC2 AMI を手動コピー → 完全手動、法令要件の「自動化」に反する\n\n'
                  '💡 DLM: EBS スナップショット＆AMI のライフサイクル（作成／世代保持／削除／クロスRegionコピー）を宣言的に管理',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-160', s)


# =====================================================================
# SAP-168  Answer D: Aurora Global Database (RPO 30秒以内)
# =====================================================================
def sap_168():
    s = header('SAP-168 / 正解D: Aurora Global Database (RPO 30秒以内 / MySQL 8.0 互換)')

    s += region('rp', 'Primary: us-east-1', 20, 70, 460, 360, AWS_BLUE)
    s += icon('alb_p', 60, 140, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('ec2_p', 170, 140, 'ec2', AWS_ORANGE, 'App (Auto Scaling)', 140, 58, 9, True)
    s += icon('aw_p', 320, 140, 'aurora', AWS_BLUE,
              'Aurora MySQL 8.0\nGlobal DB Writer', 170, 58, 9, True)
    s += text_box('pn', 40, 240, 420, 180,
                  '【要件】\n・RPO ≦ 30秒\n・アプリ/スキーマの大幅改修不可\n・MySQL 互換\n\n【現状】\n・RDS for MySQL 8.0 単一プライマリ\n・DR 先: us-west-2', AWS_BLUE, 10)

    s += icon('r53', 500, 70, 'route_53', AWS_PURPLE,
              'Route 53\nFailover', 150, 58, 10, True)

    s += region('rd', 'Secondary: us-west-2', 520, 160, 460, 270, AWS_GREEN)
    s += icon('alb_d', 560, 230, 'application_load_balancer', AWS_PURPLE, 'ALB (待機)')
    s += icon('ec2_d', 670, 230, 'ec2', AWS_ORANGE, 'App (待機)', 110, 58, 9, True)
    s += icon('aw_d', 820, 230, 'aurora', AWS_BLUE,
              'Aurora Global DB\nSecondary (R)', 160, 58, 9, True)
    s += text_box('dn', 540, 330, 430, 90,
                  '・ストレージ物理レプリ 通常<1秒\n・DR時は Secondary を Promote → 書込可\n・アプリはエンドポイント変更のみ', AWS_GREEN, 10)

    s += arrow('rep', 'aw_p', 'aw_d', AWS_PINK, 4, False, '物理レプリ <1秒 (RPO)')
    s += arrow('r_p', 'r53', 'alb_p', AWS_PURPLE, 2, False, 'Primary')
    s += arrow('r_d', 'r53', 'alb_d', AWS_PURPLE, 2, True, 'Failover')

    s += text_box('cmp', 20, 440, 960, 150,
                  '✅ D=Aurora Global Database: 物理ストレージレプリケーションで通常 RPO < 1秒 (要件30秒を余裕で達成)、MySQL 互換でアプリ改修不要\n\n'
                  '❌ A: RDS Cross-Region RR = 非同期ログレプリ、RPO ≒ 数分 (30秒保証困難)\n'
                  '❌ B: DMS 継続レプリケーション = トランザクション単位、RPO 数秒だが運用複雑\n'
                  '❌ C: 定期スナップショット = スナップ間隔分のロス発生 (30秒不可能)\n\n'
                  '💡 Aurora Global DB = 「MySQL/PostgreSQL 互換 × マルチリージョン RPO<1秒」を実現する唯一の AWS ネイティブ',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-168', s)


# =====================================================================
# SAP-174  Answer C: Warm Standby (RTO 2h / セカンダリ常時起動)
# =====================================================================
def sap_174():
    s = header('SAP-174 / 正解C: Warm Standby (RTO 2時間 / セカンダリ小容量常時起動)')

    s += region('rp', 'Primary (本番)', 20, 70, 440, 340, AWS_BLUE)
    s += icon('elb_p', 60, 140, 'application_load_balancer', AWS_PURPLE, 'ELB')
    s += icon('ec2_p', 170, 140, 'ec2', AWS_ORANGE,
              'EC2 ASG\n(本番容量)', 130, 58, 9, True)
    s += icon('rds_p', 310, 140, 'rds', AWS_BLUE,
              'RDS MySQL\nMulti-AZ (書込)', 150, 58, 9, True)
    s += text_box('pn', 40, 240, 420, 160,
                  '【要件】\n・RTO ≦ 2時間\n・RPO 最小\n・セカンダリは本番同等稼働は避ける (コスト)\n・勤怠: 2時間超停止は法令違反リスク', AWS_BLUE, 10)

    s += icon('r53', 500, 70, 'route_53', AWS_PURPLE,
              'Route 53\nFailover', 150, 58, 10, True)

    s += region('rd', 'Secondary (Warm Standby)', 520, 160, 440, 250, AWS_GREEN)
    s += icon('elb_d', 560, 220, 'application_load_balancer', AWS_PURPLE, 'ELB (稼働)')
    s += icon('ec2_d', 670, 220, 'ec2', AWS_ORANGE,
              'ASG 小容量\n(常時稼働)', 140, 58, 9, True)
    s += icon('rds_d', 820, 220, 'rds', AWS_BLUE,
              'RDS Cross-Region\nRead Replica', 160, 58, 9, True)
    s += text_box('dn', 540, 310, 430, 90,
                  'DR発動時:\n・ASG 容量を本番規模へ拡大\n・RR を Promote → 書込可\n・DNS切替で即時サービス再開', AWS_GREEN, 10)

    s += arrow('rep', 'rds_p', 'rds_d', AWS_PINK, 3, False, 'Cross-Region RR (RPO最小)')
    s += arrow('r_p', 'r53', 'elb_p', AWS_PURPLE, 2, False, 'Primary')
    s += arrow('r_d', 'r53', 'elb_d', AWS_PURPLE, 2, True, 'Failover')

    s += text_box('cmp', 20, 420, 960, 170,
                  '✅ C=Warm Standby: セカンダリに「小容量 ELB+ASG+RR」を常時配置。DR 時に容量拡大で 2時間以内復旧、RR で RPO 最小\n\n'
                  '❌ A: Pilot Light (アプリ層停止) → 起動に時間、RTO 2時間がギリギリ／本問は「本番と同様の常時稼働は不要だが、ある程度の常時稼働」を要求\n'
                  '❌ B: Multi-Site Active-Active = 本番同等×2 で過剰コスト (要件「高コストは避ける」違反)\n'
                  '❌ D: Backup & Restore = RTO 数時間、2時間達成困難\n\n'
                  '💡 DR4戦略: Backup&Restore (RTO時間) < Pilot Light (RTO分〜時間) < Warm Standby (RTO分) < Multi-Site (RTO秒)',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-174', s)


# =====================================================================
# SAP-219  Answer B+C: S3 CRR + Lifecycle (Standard-IA→Glacier) + Intelligent-Tiering
# =====================================================================
def sap_219():
    s = header('SAP-219 / 正解B+C: S3 CRR+Lifecycle(Glacier) × Intelligent-Tiering (RTO 6h 最安DR)')

    s += region('rp', 'Primary Region', 20, 70, 460, 360, AWS_BLUE)
    s += icon('app_p', 60, 140, 'ec2', AWS_ORANGE,
              'SNS 写真/動画App', 140, 58, 9, True)
    s += icon('s3_p', 220, 140, 's3', AWS_GREEN,
              'S3 Standard\n(Primary)', 140, 58, 9, True)
    s += icon('it_p', 360, 140, 's3', AWS_PINK,
              'Intelligent-\nTiering (C)', 130, 58, 9, True)
    s += text_box('pn', 40, 240, 420, 180,
                  '【C】プライマリバケットを\nIntelligent-Tiering に設定\n・アクセスパターン不明でもOK\n・自動階層化でコスト最適\n・頻繁アクセス→Frequent、\n 未アクセス→IA→Archive',
                  AWS_PINK, 10)

    s += region('rd', 'DR Region', 520, 70, 460, 360, AWS_GREEN)
    s += icon('s3_d', 560, 140, 's3', AWS_GREEN,
              'S3 Standard\n(CRR レプリカ)', 150, 58, 9, True)
    s += icon('ia', 720, 140, 's3', AWS_BLUE,
              'S3 Standard-IA\n(30日後)', 150, 58, 9, True)
    s += icon('glc', 870, 140, 's3', AWS_PURPLE,
              'Glacier Flexible\n(90日後)', 150, 58, 9, True)
    s += text_box('dn', 540, 240, 430, 180,
                  '【B】S3 CRR + Lifecycle\n・Standard → IA (30日)\n・IA → Glacier Flexible Retrieval (90日)\n・Glacier 標準取り出し 3-5時間\n・RTO 6時間内に収まる\n・保管コスト最安', AWS_GREEN, 10)

    s += arrow('rep', 's3_p', 's3_d', AWS_PINK, 3, False, 'S3 CRR')
    s += arrow('l1', 's3_d', 'ia', AWS_BLUE, 2, True, '30日')
    s += arrow('l2', 'ia', 'glc', AWS_PURPLE, 2, True, '90日')

    s += text_box('cmp', 20, 440, 960, 150,
                  '✅ B+C=CRR+Lifecycle×Intelligent-Tiering: RTO 6時間を満たしつつ保管コスト最安\n   - Glacier Flexible Retrieval の標準取り出し 3-5時間 ≦ 6時間 ✓\n   - Intelligent-Tiering はパターン不明データに最適\n\n'
                  '❌ A: Glacier Deep Archive = 取り出し12時間以上 → RTO 6時間違反\n'
                  '❌ D: レプリカ側で Intelligent-Tiering → アクセスパターンのない DR 先では無駄 (最小30日固定料金)\n'
                  '❌ E: プライマリを IA に即移行 → ユーザー体験を損なう (取り出し料金)',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-219', s)


# =====================================================================
# SAP-225  Answer B+E+F: DynamoDB GT + Route 53 Latency + CloudFormation
# =====================================================================
def sap_225():
    s = header('SAP-225 / 正解B+E+F: DynamoDB GT + Route 53 レイテンシ + CloudFormation (マルチリージョン)')

    s += icon('r53', 450, 50, 'route_53', AWS_PURPLE,
              'Route 53\nレイテンシールーティング (F)', 200, 58, 10, True)

    s += region('r1', 'Region 1 (us-east-1)', 20, 150, 470, 280, AWS_BLUE)
    s += icon('alb_1', 60, 210, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('ec2_1', 170, 210, 'ec2', AWS_ORANGE,
              'EC2 ASG\n(CFnで展開)', 130, 58, 9, True)
    s += icon('ddb_1', 320, 210, 'dynamodb', AWS_BLUE,
              'DynamoDB\nGlobal Tables', 150, 58, 9, True)
    s += icon('cfn_1', 400, 310, 'cloudwatch', AWS_PURPLE,
              'CFn Stack (E)', 120, 58, 9)
    s += text_box('n1', 40, 330, 360, 90,
                  '【E】CloudFormation で\n両リージョンに同一スタックを展開\n→ IaC 自動デプロイ', AWS_BLUE, 9)

    s += region('r2', 'Region 2 (eu-west-1)', 510, 150, 470, 280, AWS_GREEN)
    s += icon('alb_2', 550, 210, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('ec2_2', 660, 210, 'ec2', AWS_ORANGE,
              'EC2 ASG\n(CFnで展開)', 130, 58, 9, True)
    s += icon('ddb_2', 810, 210, 'dynamodb', AWS_BLUE,
              'DynamoDB GT\n(Active-Active)', 160, 58, 9, True)
    s += text_box('n2', 530, 330, 440, 90,
                  '【B】DynamoDB Global Tables\n・全リージョンで書込可\n・RPO 数秒、RTO ほぼ0', AWS_GREEN, 9)

    s += arrow('r1_a', 'r53', 'alb_1', AWS_PURPLE, 2, False, '北米ユーザー')
    s += arrow('r2_a', 'r53', 'alb_2', AWS_PURPLE, 2, False, '欧州ユーザー')
    s += bi_arrow('rep', 'ddb_1', 'ddb_2', AWS_PINK, 3, False, 'DynamoDB Streams 双方向')

    s += text_box('cmp', 20, 440, 960, 150,
                  '✅ B+E+F=DynamoDB GT × CFn × Route 53 レイテンシ: マルチリージョン DR + 低遅延 + IaC の3拍子\n'
                  '   - B: DynamoDB Global Tables で DB をマルチリージョン同期 (Active-Active)\n'
                  '   - E: CloudFormation でインフラコード化、両リージョンへ一貫展開\n'
                  '   - F: Route 53 レイテンシー = 最も近いリージョンへ自動誘導\n\n'
                  '❌ A: DynamoDB バックアップのみ = レプリではなく復元、RTO長い\n'
                  '❌ C: Aurora 移行 = DynamoDB を RDB に変える大規模改修 (要件逸脱)\n'
                  '❌ D: Route 53 シンプルルーティング = 遅延最適化なし',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-225', s)


# =====================================================================
# SAP-233  Answer B: AWS Backup クロスリージョンコピー (Aurora+DynamoDB)
# =====================================================================
def sap_233():
    s = header('SAP-233 / 正解B: AWS Backup クロスリージョンコピー (RPO 2h / RTO 4h / コスト最小)')

    s += region('rp', 'Primary Region', 20, 70, 460, 360, AWS_BLUE)
    s += icon('ecs', 60, 140, 'ec2', AWS_ORANGE, 'ECS (App)', 110, 58, 9)
    s += icon('aurora', 180, 140, 'aurora', AWS_BLUE, 'Aurora', 110, 58, 9, True)
    s += icon('ddb', 300, 140, 'dynamodb', AWS_BLUE, 'DynamoDB', 110, 58, 9, True)
    s += icon('bk', 420, 140, 'backup', AWS_GREEN, 'AWS Backup', 110, 58, 9, True)
    s += text_box('pn', 40, 240, 420, 180,
                  '【要件】\n・2サービス (Aurora + DynamoDB)\n・RPO 2時間 / RTO 4時間\n・平常コスト最小 (常時稼働リソース不可)\n\n【B】AWS Backup で両サービスを\n統合バックアップ + 自動クロスRegionコピー', AWS_BLUE, 10)

    s += region('rd', 'Secondary Region', 520, 70, 460, 360, AWS_GREEN)
    s += icon('bk_d', 560, 140, 'backup', AWS_GREEN,
              'AWS Backup Vault\n(コピー先)', 150, 58, 9, True)
    s += icon('aurora_d', 720, 140, 'aurora', AWS_BLUE,
              'Aurora Restored\n(DR時のみ)', 160, 58, 9)
    s += icon('ddb_d', 880, 140, 'dynamodb', AWS_BLUE,
              'DDB Restored\n(DR時のみ)', 130, 58, 9)
    s += text_box('dn', 540, 240, 430, 180,
                  '【DR発動時】\n・Backup Vault からリストア\n・RTO 4時間内で両DBを起動\n\n平常時:\n・ECSアプリは停止、バックアップのみ保管\n・最小コスト', AWS_GREEN, 10)

    s += arrow('b1', 'aurora', 'bk', AWS_GREEN, 2, False)
    s += arrow('b2', 'ddb', 'bk', AWS_GREEN, 2, False)
    s += arrow('rep', 'bk', 'bk_d', AWS_PINK, 3, False, 'クロスRegionコピー (2h毎)')
    s += arrow('rs1', 'bk_d', 'aurora_d', AWS_GREEN, 2, True, 'Restore')
    s += arrow('rs2', 'bk_d', 'ddb_d', AWS_GREEN, 2, True, 'Restore')

    s += text_box('cmp', 20, 440, 960, 150,
                  '✅ B=AWS Backup クロスリージョンコピー: 「Aurora + DynamoDB」を単一サービスで統合バックアップ、Vault→Vault コピーで DR 先へ自動転送。平常コスト最小 (リストアは DR 時のみ)\n\n'
                  '❌ A: DMS による継続レプリケーション = 常時稼働リソース必要、コスト最小要件に反する\n'
                  '❌ C: Aurora Global DB + DynamoDB GT = RPO/RTO は優秀だがコスト過剰 (本問は RTO 4h でよい)\n'
                  '❌ D: 手動スクリプトでスナップショット → 運用負荷増、2サービス統合管理不可',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-233', s)


# =====================================================================
# SAP-251  Answer A: RDS Multi-AZ + Cross-Region Read Replica
# =====================================================================
def sap_251():
    s = header('SAP-251 / 正解A: RDS MySQL Multi-AZ + Cross-Region Read Replica (改修なしで高可用)')

    s += region('rp', 'Primary: 北米リージョン', 20, 70, 460, 360, AWS_BLUE)
    s += icon('elb_p', 60, 140, 'application_load_balancer', AWS_PURPLE, 'ELB')
    s += icon('ec2_p', 170, 140, 'ec2', AWS_ORANGE, 'EC2 (EC)', 110, 58, 9)
    s += icon('rds_p', 280, 140, 'rds', AWS_BLUE,
              'RDS MySQL\nPrimary', 130, 58, 9, True)
    s += icon('rds_s', 410, 140, 'rds', AWS_BLUE,
              'Standby\n(別AZ)', 110, 58, 9, True)
    s += text_box('pn', 40, 240, 420, 180,
                  '【Multi-AZ】\n・同期レプリ (別AZ Standby)\n・AZ障害時は自動フェイルオーバー\n・通常 30-60秒で切替\n\n【制約】\n・アプリ改修不可 (Aurora移行は避ける)\n・MySQLのまま運用継続', AWS_BLUE, 10)

    s += region('rd', 'Secondary: アジアリージョン', 520, 70, 460, 360, AWS_GREEN)
    s += icon('elb_d', 560, 140, 'application_load_balancer', AWS_PURPLE, 'ELB')
    s += icon('ec2_d', 670, 140, 'ec2', AWS_ORANGE, 'EC2 (EC)', 110, 58, 9)
    s += icon('rr', 800, 140, 'rds', AWS_BLUE,
              'Cross-Region\nRead Replica', 150, 58, 9, True)
    s += text_box('dn', 540, 240, 430, 180,
                  '【Cross-Region RR】\n・非同期レプリ (RPO 数秒〜分)\n・リージョン障害時は Promote → 書込可\n・アプリは接続先エンドポイント変更のみ\n・改修なしで DR 達成', AWS_GREEN, 10)

    s += arrow('ma', 'rds_p', 'rds_s', AWS_BLUE, 3, False, '同期 (Multi-AZ)')
    s += arrow('crr', 'rds_p', 'rr', AWS_PINK, 3, False, '非同期 Cross-Region RR')
    s += arrow('rs', 'rr', 'rds_p', AWS_PURPLE, 2, True, 'Promote (DR時)')

    s += text_box('cmp', 20, 440, 960, 150,
                  '✅ A=RDS Multi-AZ + Cross-Region RR: AZ障害は Multi-AZ で、リージョン障害は Cross-Region RR で対応。RDS for MySQL のまま、アプリ改修不要\n\n'
                  '❌ B: Single-AZ にして複製 = 要件「単一点障害排除」に反する\n'
                  '❌ C: Aurora 移行 = 性能は最高だが「アプリ改修を伴う大規模移行は避けたい」に反する\n'
                  '❌ D: オンプレ DC へのバックアップ = マルチリージョン要件・自動FO要件に合わない\n\n'
                  '💡 RDS Multi-AZ = HA (AZ障害対応)、Cross-Region RR = DR (リージョン障害対応)',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-251', s)


# =====================================================================
# SAP-263  Answer B+D+E: AWS Backup 統合管理 + クロスリージョンコピー + SNS通知
# =====================================================================
def sap_263():
    s = header('SAP-263 / 正解B+D+E: AWS Backup 統合管理 + クロスリージョンコピー + SNS通知')

    s += region('rp', 'Primary Region', 20, 70, 460, 340, AWS_BLUE)
    s += icon('ec2', 60, 140, 'ec2', AWS_ORANGE, 'EC2', 80, 58, 9)
    s += icon('efs', 150, 140, 'backup', AWS_GREEN, 'EFS', 80, 58, 9)
    s += icon('rds', 240, 140, 'rds', AWS_BLUE, 'RDS', 80, 58, 9)
    s += icon('bk', 350, 140, 'backup', AWS_GREEN,
              'AWS Backup\n(E:統合管理)', 140, 58, 9, True)
    s += text_box('pn', 40, 240, 420, 160,
                  '【E】バックアッププラン\n・日次/週次/月次の保持要件を定義\n・EC2/EFS/RDS を単一画面で一元管理\n・Backup Dashboard で全状況を可視化', AWS_GREEN, 10)

    s += region('rd', 'DR Region', 520, 70, 460, 200, AWS_GREEN)
    s += icon('bk_d', 700, 140, 'backup', AWS_GREEN,
              'Backup Vault\n(D: クロスRegion)', 160, 58, 9, True)
    s += text_box('dn', 540, 210, 430, 50,
                  '【D】バックアップ完了直後に別リージョンへコピー (ルール設定のみで自動)', AWS_GREEN, 9)

    s += icon('sns', 700, 320, 'cloudwatch', AWS_RED,
              'SNS Topic\n(B: 失敗通知)', 160, 58, 9, True)
    s += icon('mail', 900, 320, 'cloudwatch', AWS_RED, 'Ops\nメール', 90, 58, 9)
    s += text_box('bn', 520, 410, 460, 30,
                  '【B】Backup イベント→SNS→即時通知 (失敗検知)', AWS_RED, 9)

    s += arrow('b1', 'ec2', 'bk', AWS_GREEN, 2)
    s += arrow('b2', 'efs', 'bk', AWS_GREEN, 2)
    s += arrow('b3', 'rds', 'bk', AWS_GREEN, 2)
    s += arrow('xrc', 'bk', 'bk_d', AWS_PINK, 3, False, 'クロスRegionコピー')
    s += arrow('sn1', 'bk', 'sns', AWS_RED, 2, True, 'Failure Event')
    s += arrow('sn2', 'sns', 'mail', AWS_RED, 2)

    s += text_box('cmp', 20, 450, 960, 140,
                  '✅ B+D+E=AWS Backup ネイティブ 3 機能の組合せで 4 要件を完全自動化\n'
                  '   - E: バックアッププラン (日次/週次/月次保持、EC2+EFS+RDS統合)\n'
                  '   - D: バックアップルールにクロスリージョンコピー設定 (取得直後)\n'
                  '   - B: Backup イベント SNS 通知 (失敗時即時)\n\n'
                  '❌ A/C/F: EC2スクリプト・個別DLM・個別RDSスナップショット = サービス横断の単一画面管理ができない',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-263', s)


# =====================================================================
# SAP-275  Answer D: CloudFormation + Aurora MySQL Multi-AZ (RPO0 / RTO1h)
# =====================================================================
def sap_275():
    s = header('SAP-275 / 正解D: CFn + Aurora MySQL Multi-AZ (.NET/MySQL 互換 / RPO0)')

    s += dc('op', 'オンプレミス (3層 .NET)', 20, 70, 260, 260)
    s += icon('web_op', 60, 140, 'ec2', GRAY, 'Webサーバ')
    s += icon('db_op', 170, 140, 'backup', GRAY, 'MySQL')

    s += icon('cfn', 340, 140, 'cloudwatch', AWS_PURPLE,
              'CloudFormation\n(IaC)', 150, 58, 10, True)
    s += text_box('cn', 320, 230, 190, 100,
                  '【D】CFn テンプレート\n・EC2 ASG + ALB\n・Aurora MySQL Multi-AZ\n・DeletionPolicy=Retain', AWS_PURPLE, 9)

    s += region('aws', 'AWS Region', 540, 70, 440, 340, AWS_BLUE)
    s += icon('alb', 580, 140, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('ec2_a', 680, 140, 'ec2', AWS_ORANGE,
              'EC2 ASG\n(.NET/複数AZ)', 140, 58, 9, True)
    s += icon('aw_w', 840, 140, 'aurora', AWS_BLUE,
              'Aurora MySQL\nWriter', 130, 58, 9, True)
    s += icon('aw_r', 840, 260, 'aurora', AWS_BLUE,
              'Reader\n(別AZ)', 130, 58, 9)
    s += text_box('an', 560, 240, 260, 160,
                  '【Aurora MySQL Multi-AZ】\n・ストレージ6コピー(3AZ×2)\n・自動フェイルオーバー30秒以内\n・MySQL完全互換で.NETから接続\n・RPO 0 (同期レプリ)\n・RTO 1時間以内を容易達成', AWS_BLUE, 9)

    s += arrow('m1', 'web_op', 'cfn', GRAY, 2, True, 'Lift & Shift')
    s += arrow('d1', 'cfn', 'alb', AWS_PURPLE, 2, False, 'Deploy')
    s += arrow('d2', 'cfn', 'aw_w', AWS_PURPLE, 2, False)
    s += arrow('rep', 'aw_w', 'aw_r', AWS_BLUE, 2, False, '同期')

    s += text_box('cmp', 20, 430, 960, 160,
                  '✅ D=CloudFormation × Aurora MySQL Multi-AZ: IaC で展開 + RPO0 (同期レプリ) + 自動FO + MySQL互換で .NET 接続\n   DeletionPolicy=Retain で DB 誤削除防止\n\n'
                  '❌ A: EC2 に自前 MySQL = マネージド要件違反、自動FO無し\n'
                  '❌ B: RDS for MySQL (Single-AZ) = RPO>0、単一点障害\n'
                  '❌ C: Lambda 移行 = .NET ランタイム制約大、大改修\n\n'
                  '💡 Aurora Multi-AZ は 3AZ×2 コピーの分散ストレージで「RPO 0 = 同期」を実現',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-275', s)


# =====================================================================
# SAP-278  Answer A: Global Accelerator (マルチリージョン自動 FO)
# =====================================================================
def sap_278():
    s = header('SAP-278 / 正解A: AWS Global Accelerator (世界同時対戦 / グローバル自動FO)')

    s += text_box('pl', 20, 60, 140, 60, 'プレイヤー\n(世界中)\nUDP+TCP', NAVY, 10, True, 'center', '#EAF4FF', AWS_BLUE)

    s += icon('ga', 200, 70, 'route_53', AWS_PURPLE,
              'Global Accelerator\nヘルスチェック + 動的ルーティング', 240, 58, 10, True)

    s += region('r1', 'us-east-1', 480, 60, 240, 150, AWS_BLUE)
    s += icon('alb_1', 520, 130, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('ec2_1', 620, 130, 'ec2', AWS_ORANGE, 'ASG EC2', 110, 58, 9)

    s += region('r2', 'eu-west-1', 740, 60, 240, 150, AWS_GREEN)
    s += icon('alb_2', 780, 130, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('ec2_2', 880, 130, 'ec2', AWS_ORANGE, 'ASG EC2', 110, 58, 9)

    s += region('r3', 'ap-northeast-1', 480, 240, 240, 150, AWS_GREEN)
    s += icon('alb_3', 520, 310, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('ec2_3', 620, 310, 'ec2', AWS_ORANGE, 'ASG EC2', 110, 58, 9)

    s += region('r4', 'ap-southeast-2 (障害)', 740, 240, 240, 150, AWS_RED)
    s += icon('alb_4', 780, 310, 'application_load_balancer', AWS_PURPLE, 'ALB (DOWN)')
    s += icon('ec2_4', 880, 310, 'ec2', AWS_RED, '停止', 110, 58, 9)

    s += arrow('u_ga', 'pl', 'ga', NAVY, 3, False, 'Anycast IP')
    s += arrow('g1', 'ga', 'alb_1', AWS_PURPLE, 2)
    s += arrow('g2', 'ga', 'alb_2', AWS_PURPLE, 2)
    s += arrow('g3', 'ga', 'alb_3', AWS_PURPLE, 2)
    s += arrow('g4', 'ga', 'alb_4', AWS_RED, 2, True, '除外')

    s += text_box('cmp', 20, 400, 960, 190,
                  '✅ A=Global Accelerator: 3要件を単一サービスで解決\n'
                  '   ①各リージョンエンドポイントを継続監視\n   ②ヘルシーかつ最低遅延リージョンへ動的ルーティング (Anycast)\n   ③クライアント設定変更不要 (Anycast IP 固定)\n\n'
                  '❌ B: Route 53 レイテンシー = DNSキャッシュで反映遅延、UDP セッション中の経路最適化なし\n'
                  '❌ C: CloudFront = HTTP/HTTPS 専用、ゲーム UDP 非対応\n'
                  '❌ D: ALB のみ = リージョン単位の自動フェイルオーバー機能なし\n\n'
                  '💡 GA: DNS に依存せず、クライアント→ GA の経路で動的選択。フェイルオーバーは数十秒',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-278', s)


# =====================================================================
# SAP-285  Answer B: Backup & Restore (RTO 24h / RPO 8h / 最安)
# =====================================================================
def sap_285():
    s = header('SAP-285 / 正解B: Backup & Restore 戦略 (RTO 24h / RPO 8h / 平常コスト最小)')

    s += region('rp', 'Primary Region', 20, 70, 460, 360, AWS_BLUE)
    s += icon('alb_p', 60, 140, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('ecs_p', 170, 140, 'ec2', AWS_ORANGE,
              'ECS (Docker)', 130, 58, 9, True)
    s += icon('ecr_p', 310, 140, 's3', AWS_GREEN,
              'ECR\nDockerイメージ', 150, 58, 9, True)
    s += icon('rds_p', 60, 280, 'rds', AWS_BLUE,
              'RDS MySQL', 110, 58, 9, True)
    s += icon('snap_p', 200, 280, 'backup', AWS_GREEN,
              'Snapshot\n(8時間毎)', 130, 58, 9, True)
    s += text_box('pn', 40, 360, 420, 60,
                  '8時間毎スナップショット = RPO 8h', AWS_BLUE, 10)

    s += region('rd', 'Secondary Region (平常時リソース0)', 520, 70, 460, 360, AWS_GREEN)
    s += icon('ecr_d', 560, 140, 's3', AWS_GREEN,
              'ECR\nDockerイメージ', 150, 58, 9, True)
    s += icon('snap_d', 720, 140, 'backup', AWS_GREEN,
              'Snapshot Copy\n(事前転送)', 150, 58, 9, True)
    s += icon('cfn_d', 870, 140, 'cloudwatch', AWS_PURPLE,
              'CloudFormation\n(テンプレ)', 120, 58, 9, True)
    s += text_box('dn', 540, 240, 430, 150,
                  '【DR発動時】\n・CloudFormation 実行 → ALB/ECS/RDS を構築\n・RDS スナップショットから復元\n・ECR からコンテナ起動\n・RTO 24時間以内で復旧完了\n\n平常時: インフラ0 → コスト最小', AWS_GREEN, 10)

    s += arrow('i1', 'ecr_p', 'ecr_d', AWS_PINK, 3, False, 'イメージ事前配置')
    s += arrow('s1', 'snap_p', 'snap_d', AWS_PINK, 3, False, 'クロスRegionコピー (8h毎)')

    s += text_box('cmp', 20, 440, 960, 150,
                  '✅ B=Backup & Restore: RTO 24h で OK なので「平常時はスナップショット + コンテナイメージのみ保管」で最安\n'
                  '   DR時に CloudFormation で一から構築 → RDS スナップから復元、ECR からコンテナ起動\n\n'
                  '❌ A: Aurora Global DB + 常時 ECS = RTO 秒レベルだがコスト過剰\n'
                  '❌ C: Pilot Light (最小インフラ常時起動) = 24h 許容の本問には過剰投資\n'
                  '❌ D: Warm Standby (容量縮小で常時起動) = 同上、最安要件に反する',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-285', s)


# =====================================================================
# SAP-290  Answer C: Direct Connect Gateway (冗長DX + マルチリージョン)
# =====================================================================
def sap_290():
    s = header('SAP-290 / 正解C: DX Gateway (冗長DX + 将来の北米リージョン接続)')

    s += dc('op', 'オンプレミス (世界10拠点)', 20, 70, 300, 260)
    s += icon('dx1', 60, 140, 'backup', GRAY, 'DX1 (1Gbps)', 130, 58, 9, True)
    s += icon('dx2', 60, 240, 'backup', GRAY, 'DX2 (冗長・追加)', 150, 58, 9, True)
    s += icon('pvif', 220, 180, 'backup', GRAY, 'Private VIF\n(両方)', 120, 58, 9)

    s += icon('dxgw', 400, 180, 'route_53', AWS_PURPLE,
              'Direct Connect\nGateway', 160, 58, 10, True)

    s += region('tk', 'ap-northeast-1 (東京)', 600, 70, 380, 150, AWS_BLUE)
    s += icon('vpc_tk', 660, 130, 's3', AWS_GREEN, '現行VPC\n(API+RDB)', 130, 58, 9, True)
    s += icon('tgw_tk', 820, 130, 'route_53', AWS_PURPLE, 'TGW (任意)', 120, 58, 9)

    s += region('na', 'us-east-1 (北米・将来)', 600, 240, 380, 150, AWS_GREEN)
    s += icon('vpc_na', 660, 300, 's3', AWS_GREEN,
              '新VPC\n(将来)', 110, 58, 9)
    s += text_box('na_n', 800, 290, 170, 90,
                  '同じ DX Gateway に追加するだけで北米へ拡張', AWS_GREEN, 9)

    s += arrow('d1', 'dx1', 'pvif', GRAY, 2)
    s += arrow('d2', 'dx2', 'pvif', GRAY, 2)
    s += arrow('p1', 'pvif', 'dxgw', GRAY, 2)
    s += arrow('gt', 'dxgw', 'vpc_tk', AWS_PURPLE, 2, False, 'Association')
    s += arrow('gn', 'dxgw', 'vpc_na', AWS_PURPLE, 2, True, 'Future')

    s += text_box('cmp', 20, 410, 960, 180,
                  '✅ C=DX Gateway: 2本DX→Private VIF→DX Gateway→複数リージョンの VPC に関連付け。冗長化と将来拡張を一挙に解決\n\n'
                  '❌ A: DX1本＋VPN バックアップ = VPNは公共IP経由、帯域/SLA劣化／DX冗長にならない\n'
                  '❌ B: 新DXを追加して VPC に直接接続 = DX Gateway なしでは複数リージョンへ拡張不可\n'
                  '❌ D: VPC ピアリング = リージョン内のみ／オンプレ非対応\n\n'
                  '💡 DX Gateway: 1つのゲートウェイから最大 50 VPC (複数リージョン) に閉域接続。リージョン拡張は関連付け追加のみ',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-290', s)


# =====================================================================
# SAP-296  Answer C: Route 53 Failover (Active-Passive / RTO 1h)
# =====================================================================
def sap_296():
    s = header('SAP-296 / 正解C: Route 53 Failover + 両リージョン ALB+ASG (Active-Passive DR)')

    s += icon('r53', 450, 50, 'route_53', AWS_PURPLE,
              'Route 53\nフェイルオーバー + ヘルスチェック', 250, 58, 10, True)

    s += region('rp', 'us-east-1 (Active)', 20, 140, 460, 290, AWS_BLUE)
    s += icon('alb_p', 60, 210, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('asg_p', 170, 210, 'ec2', AWS_ORANGE,
              'ASG (マルチAZ)', 140, 58, 9, True)
    s += icon('rds_p', 320, 210, 'rds', AWS_BLUE,
              'RDS Multi-AZ\n(書込)', 140, 58, 9, True)
    s += text_box('pn', 40, 310, 420, 110,
                  '平常時:\n・ALB + ASG で本番トラフィック処理\n・Auto Scaling が需要に応じて自動増減\n・RDS Multi-AZ で AZ 障害対応', AWS_BLUE, 10)

    s += region('rd', 'us-west-1 (Passive)', 520, 140, 460, 290, AWS_GREEN)
    s += icon('alb_d', 560, 210, 'application_load_balancer', AWS_PURPLE, 'ALB (構築済)')
    s += icon('asg_d', 670, 210, 'ec2', AWS_ORANGE,
              'ASG (待機)', 130, 58, 9, True)
    s += icon('rds_d', 810, 210, 'rds', AWS_BLUE,
              'RDS Cross-Region\nRR', 160, 58, 9, True)
    s += text_box('dn', 540, 310, 430, 110,
                  'DR発動:\n・Route 53 ヘルスチェック異常 → DNS 切替\n・RR を Promote → 書込可\n・ASG 容量を拡張\n・RTO 1時間以内達成', AWS_GREEN, 10)

    s += arrow('rep', 'rds_p', 'rds_d', AWS_PINK, 3, False, 'Cross-Region RR')
    s += arrow('r_p', 'r53', 'alb_p', AWS_PURPLE, 2, False, 'Primary (Active)')
    s += arrow('r_d', 'r53', 'alb_d', AWS_PURPLE, 2, True, 'Failover (Passive)')

    s += text_box('cmp', 20, 440, 960, 150,
                  '✅ C=Route 53 Failover + 両リージョン ALB+ASG: 「Active-Passive 構成 × RTO 1h」の王道解\n   プライマリ異常時にDNSレベルで自動切替、セカンダリは最小容量で常時起動 (Warm Standby寄り)\n\n'
                  '❌ A: Multi-AZ 内のみ = リージョン障害非対応 (SLA 違反)\n'
                  '❌ B: us-west-1 に空 VPC のみ = インフラがないため RTO 1h 達成困難 (Backup&Restore 相当で時間超過リスク)\n'
                  '❌ D: Active-Active (両リージョン常時書込) = RTO 秒だが本問の要件 (SLA 1h) に対し過剰コスト',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-296', s)


# =====================================================================
# SAP-253  Answer A+D+E: Aurora 移行 + RDS Proxy + Read Replica
# =====================================================================
def sap_253():
    s = header('SAP-253 / 正解A+D+E: Aurora MySQL (高速FO) + RDS Proxy + Reader (40秒→20秒未満)')

    s += region('aws', 'AWS Region (単一)', 20, 60, 960, 380, AWS_BLUE)

    s += icon('app', 60, 130, 'ec2', AWS_ORANGE, 'App層\n(EC/モバイル)', 130, 58, 9, True)

    s += icon('proxy', 250, 130, 'rds', AWS_PURPLE,
              'RDS Proxy (D)\n接続プール維持', 180, 58, 10, True)

    s += icon('aw_w', 460, 130, 'aurora', AWS_BLUE,
              'Aurora MySQL (A)\nWriter', 150, 58, 9, True)

    s += icon('aw_r1', 650, 100, 'aurora', AWS_BLUE,
              'Reader 1 (E)', 120, 58, 9)
    s += icon('aw_r2', 650, 180, 'aurora', AWS_BLUE,
              'Reader 2 (E)', 120, 58, 9)
    s += icon('aw_r3', 820, 130, 'aurora', AWS_BLUE,
              'Reader 3 (E)', 120, 58, 9)

    s += text_box('an', 40, 240, 940, 190,
                  '【A】RDS for MySQL → Aurora MySQL 移行\n   - フェイルオーバー通常30秒以内 (40秒→20秒未満の目標達成)\n   - ストレージ自動スケール (要件の自動スケール対応)\n\n'
                  '【D】RDS Proxy: 接続プールを Proxy 側で維持 → フェイルオーバー中も接続断なし\n   - アプリからは Proxy エンドポイントへ接続するだけで、Writer が切替わっても透過\n\n'
                  '【E】Aurora Reader (Read Replica): 読み取りを分散し書込への負荷を軽減',
                  AWS_BLUE, 10)

    s += arrow('a1', 'app', 'proxy', AWS_PURPLE, 3, False)
    s += arrow('a2', 'proxy', 'aw_w', AWS_BLUE, 3)
    s += arrow('a3', 'aw_w', 'aw_r1', AWS_BLUE, 1)
    s += arrow('a4', 'aw_w', 'aw_r2', AWS_BLUE, 1)
    s += arrow('a5', 'aw_w', 'aw_r3', AWS_BLUE, 1)

    s += text_box('cmp', 20, 450, 960, 140,
                  '✅ A+D+E: 「RPO維持 × フェイルオーバー高速化 × 接続断回避 × 読取負荷分散」の要件を3層で実現\n\n'
                  '❌ B: Multi-AZ のまま増強 = フェイルオーバー時間は短縮されず40秒のまま\n'
                  '❌ C: 単一AZ化 = HA 後退、要件違反\n'
                  '❌ F: Global Accelerator = ネットワーク層、DB フェイルオーバー時間には関与しない\n\n'
                  '💡 Aurora = MySQL互換のまま高速FO、RDS Proxy = アプリ無改修で接続プール継続',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('SAP-253', s)


if __name__ == '__main__':
    sap_003()
    sap_039()
    sap_071()
    sap_106()
    sap_125()
    sap_130()
    sap_155()
    sap_160()
    sap_168()
    sap_174()
    sap_219()
    sap_225()
    sap_233()
    sap_251()
    sap_253()
    sap_263()
    sap_275()
    sap_278()
    sap_285()
    sap_290()
    sap_296()
    print('\nDone: 21 drawio files generated')
