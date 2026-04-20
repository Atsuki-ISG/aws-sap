#!/usr/bin/env python3
"""
Generate per-question drawio files for DR / Multi-Region questions.
Each diagram is 1000x600, white background, AWS official icons & colors.
Icon 50x50 labels placed at icon.y + 58 or below to avoid overlap.
"""
import os
from textwrap import dedent

OUT_DIR = '/Users/aki/aws-sap/docs/diagrams/per-question'
os.makedirs(OUT_DIR, exist_ok=True)

AWS_ORANGE = '#FF9900'   # Compute
AWS_BLUE   = '#3B48CC'   # DB
AWS_GREEN  = '#7AA116'   # Storage / Network
AWS_RED    = '#DD344C'   # Security / alerts
AWS_PINK   = '#E7157B'   # Integration
AWS_PURPLE = '#8C4FFF'   # Mgmt
NAVY       = '#232F3E'

# -------- helpers ----------
def header(title, width=1000, height=600):
    return f'''<mxfile host="app.diagrams.net" modified="2026-04-20T00:00:00.000Z" agent="Claude" version="24.0.0">
  <diagram id="d" name="diagram">
    <mxGraphModel dx="1422" dy="757" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{width}" pageHeight="{height}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="title" value="{esc(title)}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;fontColor={NAVY};" vertex="1" parent="1">
          <mxGeometry x="0" y="8" width="{width}" height="28" as="geometry" />
        </mxCell>
'''

FOOTER = '''      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;').replace('\n', '&#10;'))

# region container
def region(id_, label, x, y, w, h, color=AWS_BLUE):
    return f'''        <mxCell id="{id_}" value="{esc(label)}" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;strokeColor={color};fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor={color};dashed=0;" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
        </mxCell>
'''

# on-prem DC container
def dc(id_, label, x, y, w, h, color='#666666'):
    return f'''        <mxCell id="{id_}" value="{esc(label)}" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_corporate_data_center;strokeColor={color};fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor={color};dashed=0;" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
        </mxCell>
'''

# icon - uses resIcon shape
def icon(id_, x, y, res, fill, label='', label_w=120, label_offset=58, font_size=10, bold=False):
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
          <mxGeometry x="{lx}" y="{ly}" width="{label_w}" height="28" as="geometry" />
        </mxCell>
'''
    return out

def text_box(id_, x, y, w, h, text, color=NAVY, font_size=10, bold=False, align='left', bg=None, stroke=None):
    style = f'text;html=1;align={align};verticalAlign=top;whiteSpace=wrap;fontSize={font_size};fontColor={color};'
    if bold:
        style += 'fontStyle=1;'
    if bg:
        style = f'rounded=1;whiteSpace=wrap;html=1;fillColor={bg};strokeColor={stroke or color};strokeWidth=1;fontSize={font_size};fontColor={color};verticalAlign=top;align={align};spacingTop=6;spacingLeft=8;spacingRight=8;'
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

# -------- question-specific builders ----------

def write(qid, content):
    path = os.path.join(OUT_DIR, f'{qid}.drawio')
    with open(path, 'w') as f:
        f.write(content)
    print(f'wrote {path}')


# =====================================================================
# UDEMY-351 (num=650) RPO 15s / RTO 5min EC2+RDS DR
# Answer B: Elastic DR + Cross-Region Read Replica + Route 53 Failover
# =====================================================================
def q_udemy_351():
    s = header('UDEMY-351 / 正解B: Elastic DR + RDSクロスリージョンRR + Route 53 Failover')
    # Region primary
    s += region('rp', 'Primary: us-east-1 (本番)', 20, 60, 460, 420, AWS_BLUE)
    # Route 53 global
    s += icon('r53', 700, 80, 'route_53', AWS_PURPLE, 'Route 53\nFailover', 110, 58, 10, True)
    s += text_box('r53_note', 810, 88, 170, 60, '・Primary ヘルスチェック\n・異常時 Secondary へ切替', AWS_PURPLE, 9)
    # Primary: EC2 ASG + ALB + RDS
    s += icon('alb_p', 60, 130, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('ec2_p1', 160, 130, 'ec2', AWS_ORANGE, 'EC2 ASG (Multi-AZ)', 140, 58, 9, True)
    s += icon('rds_p', 300, 130, 'rds', AWS_BLUE, 'RDS MySQL\n(Primary)', 130, 58, 9, True)
    s += text_box('prim_note', 40, 220, 420, 70,
                  '稼働中:\n・ALB + EC2 Auto Scaling(Multi-AZ)\n・RDS for MySQL プライマリ (書き込み)', AWS_BLUE, 10)
    # Elastic DR replica continuous
    s += icon('drs_p', 60, 310, 'cloudendure_disaster_recovery', AWS_RED, 'Elastic DR\nAgent (継続レプリ)', 170, 58, 9)
    s += text_box('drs_note', 40, 380, 420, 80,
                  'AWS Elastic Disaster Recovery:\n・EC2 をブロックレベルで継続レプリ\n・RPO 秒〜分／RTO 数分', AWS_RED, 9)
    # Region DR
    s += region('rd', 'DR: us-west-2 (待機)', 520, 60, 460, 420, AWS_GREEN)
    s += icon('alb_d', 560, 130, 'application_load_balancer', AWS_PURPLE, 'ALB (待機)')
    s += icon('ec2_d', 660, 130, 'ec2', AWS_ORANGE, 'EC2 ASG\n(最小構成)', 140, 58, 9, True)
    s += icon('rds_d', 800, 130, 'rds', AWS_BLUE, 'RDS Cross-Region\nRead Replica', 160, 58, 9, True)
    s += icon('drs_d', 560, 310, 'cloudendure_disaster_recovery', AWS_RED, 'DRS Target\n(レプリ先)', 140, 58, 9)
    s += text_box('sec_note', 540, 380, 420, 80,
                  'DR時:\n・ASG 希望容量を増加 → フル稼働\n・RR を Promote → プライマリ化\n・Route 53 がセカンダリへ切替', AWS_GREEN, 9)
    # Replication arrows
    s += arrow('rds_repl', 'rds_p', 'rds_d', AWS_PINK, 3, False, 'Cross-Region Read Replica')
    s += arrow('drs_repl', 'drs_p', 'drs_d', AWS_RED, 3, True, 'EBS ブロックレベル継続レプリ')
    s += arrow('r53_p', 'r53', 'alb_p', AWS_PURPLE, 2, False, 'Primary (Active)')
    s += arrow('r53_d', 'r53', 'alb_d', AWS_PURPLE, 2, True, 'Failover')
    # Comparison
    s += text_box('cmp', 20, 500, 960, 90,
                  '✅ 正解B=Pilot Light: 継続レプリ+最小構成 → RTO5分/RPO15秒を満たす最安解\n'
                  '❌ A: AWS Backupは15秒RPOを満たせない／位置情報ルーティング=フェイルオーバー用途ではない\n'
                  '❌ C: Backup→手動復元はRTO5分に収まらない／シンプルルーティングは自動切替不可\n'
                  '❌ D: フル容量ASG＋Aurora Global=Warm Standby相当で要件に対し過剰コスト',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-351', s)


# =====================================================================
# UDEMY-008 (num=307) NFS オンプレ→AWS DR, RTO 20min/RPO 10min
# Answer D: Elastic DR for servers + DataSync to EFS for NFS data
# =====================================================================
def q_udemy_008():
    s = header('UDEMY-008 / 正解D: Elastic DR (サーバ) + DataSync→EFS (NFS)')
    s += dc('op', 'オンプレミス DC', 20, 60, 420, 420)
    s += icon('srv', 60, 120, 'ec2', '#666666', 'Linuxサーバー群\n(数百台)', 130, 58, 9, True)
    s += icon('nfs', 220, 120, 'backup', '#666666', 'NFS 共有', 100, 58, 9, True)
    s += icon('drs_agent', 60, 240, 'cloudendure_disaster_recovery', AWS_RED, 'DRS Agent', 100, 58, 9)
    s += icon('ds_agent', 220, 240, 'backup', AWS_GREEN, 'DataSync\nAgent', 100, 58, 9)
    s += text_box('op_note', 40, 340, 380, 110,
                  '【要件】\n・RTO 20分／RPO 10分\n・AWSネイティブでフェイルオーバー＋フェイルバック\n・共通NFS共有をLinuxサーバー群がマウント', '#333333', 10)

    s += region('aws', 'AWS Region (DR先)', 480, 60, 500, 420, AWS_BLUE)
    s += icon('drs_svc', 520, 120, 'cloudendure_disaster_recovery', AWS_RED, 'Elastic DR\n(継続ブロックレプリ)', 160, 58, 9, True)
    s += icon('ec2_dr', 700, 120, 'ec2', AWS_ORANGE, 'DR EC2 起動\n(Launch時のみ課金)', 160, 58, 9)
    s += icon('efs', 520, 260, 's3', AWS_GREEN, 'EFS ファイルシステム', 160, 58, 9, True)
    # use Amazon EFS icon? Use backup for visual
    s += icon('ds_svc', 700, 260, 'backup', AWS_GREEN, 'DataSync\n(10分毎同期)', 140, 58, 9)
    s += text_box('aws_note', 500, 360, 460, 110,
                  '【DR発動時】\n・Elastic DR で EC2 を数分で起動 → RTO 20分達成\n・EFS 上の最新 NFS データをマウント\n・復旧後は Elastic DR でフェイルバック可能', AWS_BLUE, 10)

    s += arrow('a1', 'drs_agent', 'drs_svc', AWS_RED, 3, False, 'サーバーブロックレプリ(継続)')
    s += arrow('a2', 'ds_agent', 'ds_svc', AWS_GREEN, 3, False, 'NFSデータ同期(10分毎)')
    s += arrow('a3', 'drs_svc', 'ec2_dr', AWS_RED, 2, True, '障害時に起動')
    s += arrow('a4', 'ds_svc', 'efs', AWS_GREEN, 2, True, '書込み')
    s += arrow('a5', 'ec2_dr', 'efs', NAVY, 2, False, 'NFSマウント')

    s += text_box('cmp', 20, 490, 960, 100,
                  '✅ 正解D: Elastic DR(サーバ継続レプリ) + DataSync→EFS(NFSデータ定期同期) の組み合わせ\n'
                  '❌ A: Storage Gateway+6時間バックアップ → RPO10分を満たせない／フェイルバックがネイティブでない\n'
                  '❌ B: 障害時にCodePipelineでデプロイ → 起動に時間がかかりRTO20分を超過\n'
                  '❌ C: rsyncは手動運用／マルチサイトActive-Activeは過剰でコスト高',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-008', s)


# =====================================================================
# UDEMY-046 (num=345) Tokyo→Osaka PostgreSQL DR RTO<3min RPO<30s
# Answer B: Aurora Global Database
# =====================================================================
def q_udemy_046():
    s = header('UDEMY-046 / 正解B: Aurora PostgreSQL Global Database (東京↔大阪)')
    s += region('rt', 'Primary: ap-northeast-1 (東京)', 20, 60, 460, 400, AWS_BLUE)
    s += icon('alb_t', 60, 120, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('ec2_t', 170, 120, 'ec2', AWS_ORANGE, 'App 3AZ分散', 130, 58, 9, True)
    s += icon('awr_t', 310, 120, 'aurora', AWS_BLUE, 'Aurora PG\nWriter', 130, 58, 9, True)
    s += icon('awr_r', 310, 240, 'aurora', AWS_BLUE, 'Reader', 130, 58, 9)
    s += arrow('ta1', 'alb_t', 'ec2_t', NAVY, 2)
    s += arrow('ta2', 'ec2_t', 'awr_t', AWS_BLUE, 2)
    s += arrow('ta3', 'awr_t', 'awr_r', AWS_BLUE, 1, True)
    s += text_box('tn', 40, 340, 420, 100,
                  '書き込み: プライマリクラスタへ\nストレージ6コピー(3AZ×2)\n同リージョンリーダー付与可', AWS_BLUE, 10)

    s += icon('r53', 500, 70, 'route_53', AWS_PURPLE, 'Route 53\nHealth+Failover', 160, 58, 10, True)

    s += region('ro', 'Secondary: ap-northeast-3 (大阪)', 520, 140, 460, 320, AWS_GREEN)
    s += icon('alb_o', 560, 200, 'application_load_balancer', AWS_PURPLE, 'ALB (稼働)')
    s += icon('ec2_o', 670, 200, 'ec2', AWS_ORANGE, 'App (配置済)', 130, 58, 9, True)
    s += icon('awr_o', 810, 200, 'aurora', AWS_BLUE, 'Global DB\nSecondary', 130, 58, 9, True)
    s += text_box('on', 540, 310, 430, 130,
                  '読み取り: ローカル低レイテンシ\n【DR発動】数秒〜1分で Secondary を Promote → 書込可\nRPO < 1秒／RTO < 1分 達成', AWS_GREEN, 10)

    # cross region replication arrow
    s += arrow('repl', 'awr_t', 'awr_o', AWS_PINK, 4, False, 'ストレージ物理レプリ(典型<1秒)')
    s += arrow('r53_p', 'r53', 'alb_t', AWS_PURPLE, 2, False, 'Primary')
    s += arrow('r53_s', 'r53', 'alb_o', AWS_PURPLE, 2, True, 'Failover')

    s += text_box('cmp', 20, 480, 960, 110,
                  '✅ 正解B: Aurora Global Database (物理レプリ<1秒) → RPO<30秒/RTO<3分を余裕で達成\n'
                  '❌ A: RDS cross-region read replica ＋ DMS は非同期ログレプリでRPO保証が弱い／DMSは重複\n'
                  '❌ C: 定期バックアップはRPO 30秒不可 (スナップショット間隔以上)\n'
                  '❌ D: EC2上PostgreSQL+DataSync=ファイル同期でDBトランザクション整合性なし',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-046', s)


# =====================================================================
# UDEMY-309 (num=608) DynamoDB + Aurora MySQL マルチリージョン
# Answer A: Aurora Global DB + DynamoDB Global Tables
# =====================================================================
def q_udemy_309():
    s = header('UDEMY-309 / 正解A: Aurora Global DB + DynamoDB Global Tables')
    s += region('r1', 'Region 1 (Primary)', 20, 60, 460, 460, AWS_BLUE)
    s += icon('app1', 60, 120, 'ec2', AWS_ORANGE, 'アプリ層', 110, 58, 10, True)
    s += icon('aw1', 200, 120, 'aurora', AWS_BLUE, 'Aurora MySQL\nWriter (Primary)', 150, 58, 9, True)
    s += icon('ddb1', 370, 120, 'dynamodb', AWS_BLUE, 'DynamoDB\n(グローバルテーブル)', 150, 58, 9, True)
    s += arrow('c1a', 'app1', 'aw1', AWS_BLUE, 2, False, '書込')
    s += bi_arrow('c1b', 'app1', 'ddb1', AWS_BLUE, 2, False, '読書')
    s += text_box('n1', 40, 240, 420, 260,
                  '【データ層要件】\n・RTO/RPO 数分以内\n・アプリ層は既に2リージョン展開済み\n\n'
                  '【正解Aの構成】\n① Aurora Global Database をPrimary→Secondaryに構成\n'
                  '　 - 物理ストレージレプリ、RPO<1秒\n'
                  '　 - Primaryで書込、Secondaryで低レイテンシ読取\n\n'
                  '② DynamoDB を既存テーブルから\n　 Global Tables に変換、別リージョン追加\n'
                  '　 - Active-Active、RPO数秒、RTOほぼ0',
                  AWS_BLUE, 10)

    s += region('r2', 'Region 2 (Secondary)', 520, 60, 460, 460, AWS_GREEN)
    s += icon('app2', 560, 120, 'ec2', AWS_ORANGE, 'アプリ層\n(配置済)', 130, 58, 9, True)
    s += icon('aw2', 710, 120, 'aurora', AWS_BLUE, 'Aurora MySQL\nSecondary (R)', 150, 58, 9, True)
    s += icon('ddb2', 870, 120, 'dynamodb', AWS_BLUE, 'DynamoDB\nレプリカ', 130, 58, 9, True)
    s += arrow('c2a', 'app2', 'aw2', AWS_GREEN, 2, True, '読取 / 昇格後書込')
    s += bi_arrow('c2b', 'app2', 'ddb2', AWS_GREEN, 2, False, '読書 (ローカル)')
    s += text_box('n2', 540, 240, 430, 260,
                  '【Aurora】Secondary は読み取り専用\n → 障害時に Promote して書込可\n\n'
                  '【DynamoDB】Global Tables で\n  全リージョン読み書き可\n  (Active-Active)\n\n'
                  '💡 Aurora = Primary1+Secondary\n💡 DynamoDB = 全リージョン書込',
                  AWS_GREEN, 10)

    s += arrow('rep1', 'aw1', 'aw2', AWS_PINK, 4, False, 'Aurora物理レプリ <1秒')
    s += bi_arrow('rep2', 'ddb1', 'ddb2', AWS_PINK, 4, False, 'DynamoDB Streams 双方向レプリ')

    s += text_box('cmp', 20, 530, 960, 60,
                  '✅ 正解A: Aurora Global DB(書込1リージョン) + DynamoDB Global Tables(全リージョン書込)\n'
                  '❌ B: 「クラスター内の各テーブルに別リージョン」 表現が誤り (Aurora GlobalDBはクラスタ単位)\n'
                  '❌ C: クロスリージョンバックアップのみ → RPO/RTOが秒〜分単位にならない    ❌ D: Route53 ARCはDB複製機能ではない',
                  NAVY, 9, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-309', s)


# =====================================================================
# UDEMY-318 (num=617) EduTech DR — Video / Interactive, Route53 + Elastic DR
# Read to know answer
# =====================================================================
def q_udemy_318():
    s = header('UDEMY-318 / EduTech DR: S3 CRR + Route 53 Failover + Elastic DR')
    s += region('rp', 'Primary Region', 20, 60, 460, 440, AWS_BLUE)
    s += icon('cf', 60, 120, 'cloudfront', AWS_PURPLE, 'CloudFront', 110, 58, 9, True)
    s += icon('alb_p', 180, 120, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('ec2_p', 300, 120, 'ec2', AWS_ORANGE, 'App Server', 120, 58, 9, True)
    s += icon('rds_p', 420, 120, 'rds', AWS_BLUE, 'RDS\nPrimary', 90, 58, 9, True)
    s += icon('s3_p', 60, 250, 's3', AWS_GREEN, 'S3 ビデオ教材', 130, 58, 9, True)
    s += icon('drs_p', 220, 250, 'cloudendure_disaster_recovery', AWS_RED, 'Elastic DR Agent', 140, 58, 9)
    s += text_box('pn', 40, 340, 420, 150,
                  '【通常運用】\n・CloudFrontで教材配信 (キャッシュ)\n・ALB→EC2→RDS\n・S3ビデオ教材格納\n'
                  '・Elastic DR で EC2 継続レプリ\n・RDS クロスリージョンリードレプリカ', AWS_BLUE, 10)

    s += icon('r53', 500, 70, 'route_53', AWS_PURPLE, 'Route 53 Failover', 160, 58, 10, True)

    s += region('rs', 'DR Region', 520, 140, 460, 360, AWS_GREEN)
    s += icon('alb_s', 560, 200, 'application_load_balancer', AWS_PURPLE, 'ALB (待機)')
    s += icon('ec2_s', 680, 200, 'ec2', AWS_ORANGE, 'EC2 最小', 110, 58, 9)
    s += icon('rds_s', 800, 200, 'rds', AWS_BLUE, 'RDS RR\n→Promote', 130, 58, 9, True)
    s += icon('s3_s', 560, 320, 's3', AWS_GREEN, 'S3 CRR ターゲット', 150, 58, 9, True)
    s += icon('drs_s', 720, 320, 'cloudendure_disaster_recovery', AWS_RED, 'DRS Target', 120, 58, 9)
    s += text_box('sn', 540, 410, 430, 80,
                  '【DR発動】DRSでEC2を起動／RR Promote／ASG希望容量増／S3は既に同期済', AWS_GREEN, 10)

    s += arrow('ar1', 'r53', 'alb_p', AWS_PURPLE, 2, False, 'Primary')
    s += arrow('ar2', 'r53', 'alb_s', AWS_PURPLE, 2, True, 'Failover')
    s += arrow('ar3', 's3_p', 's3_s', AWS_PINK, 3, False, 'S3 CRR')
    s += arrow('ar4', 'rds_p', 'rds_s', AWS_PINK, 3, False, 'Cross-Region RR')
    s += arrow('ar5', 'drs_p', 'drs_s', AWS_RED, 3, True, 'ブロック継続レプリ')

    s += text_box('cmp', 20, 520, 960, 70,
                  '✅ 教材(S3)＝CRR／EC2＝Elastic DR／RDS＝Cross-Region RR／DNS＝Route 53 Failover が王道構成\n'
                  '💡 ビデオ配信はCloudFrontで世界中にキャッシュ、障害時もエッジから配信継続',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-318', s)


# =====================================================================
# UDEMY-070 (num=369) Fintech ECS+API Gateway Multi-Region Global
# =====================================================================
def q_udemy_070():
    s = header('UDEMY-070 / Fintech: API Gateway + ECS + Aurora Global + DynamoDB GT')
    s += icon('r53', 460, 20, 'route_53', AWS_PURPLE, 'Route 53 レイテンシールーティング', 260, 58, 10, True)

    s += region('r1', 'Region A (us-east-1)', 20, 90, 460, 420, AWS_BLUE)
    s += icon('apig1', 60, 150, 'ec2', AWS_PINK, 'API Gateway\n(Regional)', 130, 58, 9, True)  # APIGW icon not listed; use ec2 fallback with pink
    s += icon('ecs1', 210, 150, 'ec2', AWS_ORANGE, 'ECS Fargate', 130, 58, 9, True)
    s += icon('aw1', 360, 150, 'aurora', AWS_BLUE, 'Aurora Global\nPrimary', 130, 58, 9, True)
    s += icon('ddb1', 60, 280, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 140, 58, 9, True)
    s += icon('elc1', 220, 280, 'rds', AWS_BLUE, 'ElastiCache\n(リージョン内)', 140, 58, 9)
    s += text_box('n1', 40, 380, 430, 120,
                  '【構成】\n・API Gateway (Regional) + ECS Fargate\n・Aurora Global DB — 書込Primary\n・DynamoDB Global Tables — Active-Active\n・Route 53 レイテンシーで最寄りへ', AWS_BLUE, 10)

    s += region('r2', 'Region B (eu-west-1)', 520, 90, 460, 420, AWS_GREEN)
    s += icon('apig2', 560, 150, 'ec2', AWS_PINK, 'API Gateway', 130, 58, 9, True)
    s += icon('ecs2', 710, 150, 'ec2', AWS_ORANGE, 'ECS Fargate', 130, 58, 9, True)
    s += icon('aw2', 860, 150, 'aurora', AWS_BLUE, 'Aurora Global\nSecondary', 130, 58, 9, True)
    s += icon('ddb2', 560, 280, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 140, 58, 9, True)
    s += icon('elc2', 720, 280, 'rds', AWS_BLUE, 'ElastiCache', 130, 58, 9)
    s += text_box('n2', 540, 380, 430, 120,
                  '【ポイント】\n・Aurora Secondary 読取(ローカル)／書込はPrimary転送\n'
                  '・DynamoDB Global Tables は全Region書込可\n・障害時Aurora Secondaryを昇格', AWS_GREEN, 10)

    s += arrow('rep1', 'aw1', 'aw2', AWS_PINK, 4, False, 'Aurora物理レプリ <1秒')
    s += bi_arrow('rep2', 'ddb1', 'ddb2', AWS_PINK, 4, False, 'Global Tables 双方向レプリ')
    s += arrow('u1', 'r53', 'apig1', AWS_PURPLE, 2, False, '低レイテンシ')
    s += arrow('u2', 'r53', 'apig2', AWS_PURPLE, 2, False, '低レイテンシ')

    s += text_box('cmp', 20, 525, 960, 65,
                  '💡 Aurora Global DB (書込1箇所) + DynamoDB Global Tables (全Region書込) の使い分けが鍵\n'
                  '・ACIDトランザクション → Aurora Global DB    ・KVで全Region書込 → DynamoDB Global Tables',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-070', s)


# =====================================================================
# UDEMY-091 (num=390) e-commerce inventory — multi-region active-active
# Answer A: Route53 latency + KMS multi-region + Secrets replicated
# =====================================================================
def q_udemy_091():
    s = header('UDEMY-091 / 正解A: Route 53 Latency + KMS マルチリージョンキー + Secrets レプリカ')
    s += icon('r53', 430, 20, 'route_53', AWS_PURPLE, 'Route 53 レイテンシールーティング (カスタムドメイン)', 320, 58, 10, True)

    s += region('r1', 'Region A', 20, 90, 460, 430, AWS_BLUE)
    s += icon('apig1', 60, 150, 'ec2', AWS_PINK, 'API Gateway\n(Regional)', 130, 58, 9, True)
    s += icon('lam1', 220, 150, 'ec2', AWS_ORANGE, 'Lambda', 100, 58, 9, True)
    s += icon('ddb1', 340, 150, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 140, 58, 9, True)
    s += icon('kms1', 60, 280, 'cloudwatch', AWS_RED, 'KMS マルチRegionキー\n(Primary)', 170, 58, 9, True)
    s += icon('sm1', 260, 280, 'backup', AWS_RED, 'Secrets Manager\n(Primary)', 160, 58, 9, True)
    s += text_box('n1', 40, 390, 430, 110,
                  '【正解Aの肝】\n1) KMS マルチRegionキー (同じキーIDでリージョン展開)\n'
                  '2) Secrets Manager シークレットをレプリカ作成\n'
                  '3) API Gateway は Regional + Route 53 で配布', AWS_BLUE, 10)

    s += region('r2', 'Region B', 520, 90, 460, 430, AWS_GREEN)
    s += icon('apig2', 560, 150, 'ec2', AWS_PINK, 'API Gateway\n(Regional)', 130, 58, 9, True)
    s += icon('lam2', 720, 150, 'ec2', AWS_ORANGE, 'Lambda', 100, 58, 9, True)
    s += icon('ddb2', 840, 150, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 140, 58, 9, True)
    s += icon('kms2', 560, 280, 'cloudwatch', AWS_RED, 'KMS マルチRegion\nレプリカキー', 170, 58, 9, True)
    s += icon('sm2', 760, 280, 'backup', AWS_RED, 'Secrets Manager\nレプリカ', 150, 58, 9, True)
    s += text_box('n2', 540, 390, 430, 110,
                  '【アクティブ-アクティブ】\n・両Regionで API+Lambda 稼働\n'
                  '・DynamoDB Global Tables で書込共有\n・マルチRegionキーで同一キーID利用\n・シークレットは自動レプリ', AWS_GREEN, 10)

    s += arrow('u1', 'r53', 'apig1', AWS_PURPLE, 2, False, '低レイテンシ')
    s += arrow('u2', 'r53', 'apig2', AWS_PURPLE, 2, False, '低レイテンシ')
    s += bi_arrow('repd', 'ddb1', 'ddb2', AWS_PINK, 3, False, 'Global Tables 双方向')
    s += arrow('repk', 'kms1', 'kms2', AWS_RED, 3, True, 'マルチRegionキー同期')
    s += arrow('reps', 'sm1', 'sm2', AWS_RED, 3, True, 'シークレット自動レプリ')

    s += text_box('cmp', 20, 530, 960, 60,
                  '❌ B: 各Region独立KMS/Secrets→運用煩雑、Global AcceleratorはAPI Gatewayと組み合わない\n'
                  '❌ C: エッジ最適化APIGW+単一Region Lambda → アクティブ-アクティブにならない\n'
                  '❌ D: Aurora Global DBではDynamoDB要件を満たせない／KMS手動レプリは煩雑',
                  NAVY, 9, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-091', s)


# =====================================================================
# UDEMY-107 (num=406) CAD RTO 12h RPO 4h → Pilot Light
# Answer B: Docker to 2-region ECR + AWS Backup RDS 4h + CloudFormation
# =====================================================================
def q_udemy_107():
    s = header('UDEMY-107 / 正解B: Pilot Light (RTO 12h/RPO 4h) - ECR 2Region + RDS Backup + CFn')
    s += region('rp', 'Primary Region (稼働)', 20, 60, 460, 440, AWS_BLUE)
    s += icon('alb_p', 60, 120, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('ecs_p', 180, 120, 'ec2', AWS_ORANGE, 'ECS (Docker)', 130, 58, 9, True)
    s += icon('ecr_p', 320, 120, 's3', AWS_GREEN, 'ECR\n(レンダリングEng)', 140, 58, 9, True)
    s += icon('rds_p', 60, 260, 'rds', AWS_BLUE, 'RDS MySQL', 110, 58, 9, True)
    s += icon('bk_p', 220, 260, 'backup', AWS_RED, 'AWS Backup\n4時間ごと', 140, 58, 9, True)
    s += text_box('pn', 40, 340, 430, 150,
                  '【通常運用】\n・ALB → ECS コンテナで CAD プロジェクト\n・RDS MySQL にデータ\n'
                  '・ECR にレンダリングイメージ\n・AWS Backup で RDS スナップ 4h 間隔', AWS_BLUE, 10)

    s += region('rs', 'Secondary Region (Pilot Light)', 520, 60, 460, 440, AWS_GREEN)
    s += icon('cfn_s', 560, 120, 'cloudwatch', AWS_PURPLE, 'CloudFormation\nテンプレ', 150, 58, 9, True)
    s += icon('ecr_s', 720, 120, 's3', AWS_GREEN, 'ECR\n(同期)', 100, 58, 9, True)
    s += icon('bk_s', 840, 120, 'backup', AWS_RED, 'Backup Vault\n(コピー先)', 130, 58, 9, True)
    s += text_box('sn', 540, 210, 430, 270,
                  '【DR発動】\n① CloudFormation で\n　 ALB/ECS/RDS を展開\n'
                  '② 最新スナップショットから\n　 RDS 復元\n'
                  '③ ECR からイメージ取得\n　 してコンテナ起動\n'
                  '④ DNS 切替\n\n'
                  '→ RTO 12h・RPO 4h を満たす最安解\n(Pilot Light = 最小データのみ同期、\n 障害時にフルデプロイ)', AWS_GREEN, 10)

    s += arrow('x1', 'ecr_p', 'ecr_s', AWS_PINK, 3, False, 'ECR クロスリージョンレプリ')
    s += arrow('x2', 'bk_p', 'bk_s', AWS_PINK, 3, False, 'Backup クロスリージョンコピー 4h')
    s += arrow('x3', 'cfn_s', 'ecr_s', AWS_PURPLE, 2, True, 'デプロイ参照')

    s += text_box('cmp', 20, 510, 960, 80,
                  '✅ 正解B=Pilot Light: 最小構成(ECR+Backup)を常時同期、障害時に CloudFormation でフル展開\n'
                  '❌ A: 手動CLIで復元 → RTO長過ぎ／❌ C: Aurora Global=過剰コスト・要件以上\n'
                  '❌ D: DataSync→S3はRDS復元方法が不明瞭で実運用困難',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-107', s)


# =====================================================================
# UDEMY-158 (num=457) ASG min/max=0 in backup region, RDS RR, RTO<10min
# Answer B: Route 53 health check + SNS + Lambda promotes RR + ASG resize
# =====================================================================
def q_udemy_158():
    s = header('UDEMY-158 / 正解B: Route 53 ヘルスチェック→SNS→Lambda で RR 昇格 + ASG 起動')
    s += region('rp', 'Primary Region', 20, 60, 460, 440, AWS_BLUE)
    s += icon('r53', 180, 0, 'route_53', AWS_PURPLE, 'Route 53 Failover レコード', 260, 58, 10, True)
    # actually place r53 at top center outside regions
    s += icon('alb_p', 60, 120, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('asg_p', 180, 120, 'ec2', AWS_ORANGE, 'Auto Scaling\n(稼働)', 130, 58, 9, True)
    s += icon('rds_p', 320, 120, 'rds', AWS_BLUE, 'RDS Multi-AZ', 130, 58, 9, True)
    s += icon('hc', 60, 260, 'cloudwatch', AWS_PURPLE, 'Route 53\nヘルスチェック', 140, 58, 9, True)
    s += icon('sns', 220, 260, 'backup', AWS_PINK, 'SNS Topic', 100, 58, 9, True)
    s += text_box('pn', 40, 360, 430, 130,
                  '【Primary】\n・ALB/ASG/RDS Multi-AZ 稼働\n・Route 53 ヘルスチェックで監視\n'
                  '・ダウン時 SNS 通知 → Lambda 起動\n・RDS Cross-Region Read Replica', AWS_BLUE, 10)

    s += region('rs', 'Backup Region (コスト最小化)', 520, 60, 460, 440, AWS_GREEN)
    s += icon('alb_s', 560, 120, 'application_load_balancer', AWS_PURPLE, 'ALB (構築済)')
    s += icon('asg_s', 680, 120, 'ec2', AWS_ORANGE, 'ASG min=max=0\n(起動ゼロ)', 150, 58, 9, True)
    s += icon('rds_s', 850, 120, 'rds', AWS_BLUE, 'RDS Read\nReplica', 130, 58, 9, True)
    s += icon('lam', 560, 260, 'ec2', AWS_ORANGE, 'Lambda\n(昇格+ASG増)', 150, 58, 9, True)
    s += text_box('sn', 540, 360, 430, 130,
                  '【DR発動 (10分以内)】\n① SNS → Lambda 起動\n'
                  '② RR を Promote (書込可)\n③ ASG 希望容量 >0 に変更\n'
                  '④ Route 53 が Secondary へ切替', AWS_GREEN, 10)

    s += arrow('x1', 'rds_p', 'rds_s', AWS_PINK, 3, False, 'クロスリージョンRR')
    s += arrow('x2', 'hc', 'sns', AWS_PURPLE, 2, False, '異常検知')
    s += arrow('x3', 'sns', 'lam', AWS_PINK, 2, False, '通知')
    s += arrow('x4', 'lam', 'asg_s', AWS_ORANGE, 2, True, 'ASG 増加')
    s += arrow('x5', 'lam', 'rds_s', AWS_BLUE, 2, True, 'RR Promote')
    s += arrow('x6', 'r53', 'alb_p', AWS_PURPLE, 2, False, 'Primary')
    s += arrow('x7', 'r53', 'alb_s', AWS_PURPLE, 2, True, 'Failover')

    s += text_box('cmp', 20, 510, 960, 80,
                  '✅ B=アクティブ-パッシブ DR: ASG min/max=0 でコストゼロ → 障害時 Lambda で起動\n'
                  '❌ A/D: レイテンシー/Global Accelerator はアクティブ-アクティブ向きでコスト増\n'
                  '❌ C: ASG常時稼働 + DBスタンドアロン → 予算超過',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-158', s)


# =====================================================================
# UDEMY-014 (num=313) グローバル e-commerce 3層 RTO 30秒
# Answer E+C+B: ASG hot standby (RI+Spot) + DynamoDB Global Tables + Route53 Failover TTL 20s
# =====================================================================
def q_udemy_014():
    s = header('UDEMY-014 / 正解E+C+B: ホットスタンバイ + DynamoDB GT + Route 53 Failover TTL20s')
    s += icon('r53', 390, 20, 'route_53', AWS_PURPLE, 'Route 53 Failover (TTL 20秒)', 280, 58, 10, True)

    s += region('r1', 'Region 1 (Primary)', 20, 90, 460, 430, AWS_BLUE)
    s += icon('alb1', 60, 150, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('asg1', 180, 150, 'ec2', AWS_ORANGE, 'ASG\n(RI+オンデマンド)', 150, 58, 9, True)
    s += icon('ddb1', 350, 150, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 140, 58, 9, True)
    s += text_box('n1', 40, 260, 430, 230,
                  '【フロント/API層 (E)】\n・ASG (複数AZ)\n・最小台数は Reserved Instance\n・追加は On-Demand\n→ 高可用+コスト最適化\n\n'
                  '【NoSQL層 (C)】\n・DynamoDB Global Tables\n・全Region 書込可\n・レプリ数秒', AWS_BLUE, 10)

    s += region('r2', 'Region 2 (DR)', 520, 90, 460, 430, AWS_GREEN)
    s += icon('alb2', 560, 150, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('asg2', 680, 150, 'ec2', AWS_ORANGE, 'ASG ホットスタンバイ\n(RI+オンデマンド)', 160, 58, 9, True)
    s += icon('ddb2', 860, 150, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 140, 58, 9, True)
    s += text_box('n2', 540, 260, 430, 230,
                  '【ホットスタンバイ】\n・両Regionで同時稼働\n・障害時 Route 53 で即切替\n　(TTL20秒で伝播速い)\n\n'
                  '【DynamoDB GT】\n・どちらのRegionも書込継続\n・RPO数秒/RTOほぼ0', AWS_GREEN, 10)

    s += arrow('u1', 'r53', 'alb1', AWS_PURPLE, 2, False, 'Primary')
    s += arrow('u2', 'r53', 'alb2', AWS_PURPLE, 2, True, 'Failover')
    s += bi_arrow('rep', 'ddb1', 'ddb2', AWS_PINK, 4, False, 'DynamoDB Global Tables 双方向')

    s += text_box('cmp', 20, 530, 960, 60,
                  '❌ A: レイテンシー+TTL300 → RTO30秒未達成\n❌ D: DynamoDBを30分ごとS3→CRR→復元スクリプト → RTO/RPOともに不足\n'
                  '❌ F: 全Spot → 取得失敗リスク高くDR用途に不向き',
                  NAVY, 9, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-014', s)


# =====================================================================
# UDEMY-086 (num=385) World Wonders game 3-region Active-Active
# Answer C: ASG+ALB per region + Route 53 latency + DynamoDB Global Tables
# =====================================================================
def q_udemy_086():
    s = header('UDEMY-086 / 正解C: 3リージョン ASG+ALB + Route 53 レイテンシー + DynamoDB Global Tables')
    s += icon('r53', 390, 20, 'route_53', AWS_PURPLE, 'Route 53 レイテンシーベース (世界中最寄り)', 320, 58, 10, True)

    s += region('r1', 'us-east-1 (北米)', 20, 90, 310, 420, AWS_BLUE)
    s += icon('alb1', 60, 150, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('asg1', 160, 150, 'ec2', AWS_ORANGE, 'EC2 ASG', 110, 58, 9, True)
    s += icon('ddb1', 160, 260, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 140, 58, 9, True)
    s += text_box('n1', 40, 340, 270, 150,
                  'リーダーボード/\nインベントリ/\nリアルタイムイベント\n\n→ DynamoDB GT で\n全Region書込', AWS_BLUE, 10)

    s += region('r2', 'eu-central-1 (EU)', 350, 90, 310, 420, AWS_BLUE)
    s += icon('alb2', 390, 150, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('asg2', 490, 150, 'ec2', AWS_ORANGE, 'EC2 ASG', 110, 58, 9, True)
    s += icon('ddb2', 490, 260, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 140, 58, 9, True)
    s += text_box('n2', 370, 340, 270, 150,
                  '各Region 読み書き可\nRPO 数秒\nRTO ≒ 0', AWS_BLUE, 10)

    s += region('r3', 'ap-northeast-1 (AP)', 680, 90, 310, 420, AWS_BLUE)
    s += icon('alb3', 720, 150, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('asg3', 820, 150, 'ec2', AWS_ORANGE, 'EC2 ASG', 110, 58, 9, True)
    s += icon('ddb3', 820, 260, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 140, 58, 9, True)
    s += text_box('n3', 700, 340, 270, 150,
                  '最寄りRegionへ\nルーティング\n→低レイテンシ\n\n衝突: LWW\n(Last Writer Wins)', AWS_BLUE, 10)

    s += arrow('u1', 'r53', 'alb1', AWS_PURPLE, 2)
    s += arrow('u2', 'r53', 'alb2', AWS_PURPLE, 2)
    s += arrow('u3', 'r53', 'alb3', AWS_PURPLE, 2)
    s += bi_arrow('r12', 'ddb1', 'ddb2', AWS_PINK, 3, False, 'GT')
    s += bi_arrow('r23', 'ddb2', 'ddb3', AWS_PINK, 3, False, 'GT')
    s += bi_arrow('r13', 'ddb1', 'ddb3', AWS_PINK, 3, False, '双方向')

    s += text_box('cmp', 20, 520, 960, 70,
                  '❌ A: Aurora Global=書込1Region→ゲームの全Region書込要件に不適合\n'
                  '❌ B: ジオロケーション→地域制限向き、低レイテンシはレイテンシーベースが正解\n'
                  '❌ D: ElastiCache Redis Global Datastoreは書込1Primary→要件不一致',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-086', s)


# =====================================================================
# UDEMY-109 (num=408) 旅行代理店 北米→EU拡張
# Answer D+E: Aurora Global DB + S3 CRR + Route53 geoproximity + CloudFront
# =====================================================================
def q_udemy_109():
    s = header('UDEMY-109 / 正解D+E: Aurora Global + S3 CRR + CloudFront + Route 53 Geoproximity')
    s += icon('r53', 340, 20, 'route_53', AWS_PURPLE, 'Route 53 地理的近接性ルーティング + CloudFront エッジ配信', 420, 58, 10, True)

    s += region('r1', 'us-east-1 (北米)', 20, 90, 460, 430, AWS_BLUE)
    s += icon('cf1', 60, 150, 'cloudfront', AWS_PURPLE, 'CloudFront', 110, 58, 9, True)
    s += icon('alb1', 180, 150, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('asg1', 290, 150, 'ec2', AWS_ORANGE, 'ASG (予約処理)', 140, 58, 9, True)
    s += icon('aw1', 430, 150, 'aurora', AWS_BLUE, 'Aurora\nGlobal (P)', 110, 58, 9, True)
    s += icon('s3_1', 60, 280, 's3', AWS_GREEN, 'S3 静的コンテンツ', 150, 58, 9, True)
    s += text_box('n1', 40, 380, 430, 120,
                  '【正解D+E】\n・Aurora Global DB 物理レプリ (Primary)\n'
                  '・S3 CRR で静的コンテンツを EU に複製\n・ASG 配置\n・CloudFront + Route 53 で最寄り配信', AWS_BLUE, 10)

    s += region('r2', 'eu-central-1 (EU)', 520, 90, 460, 430, AWS_GREEN)
    s += icon('cf2', 560, 150, 'cloudfront', AWS_PURPLE, 'CloudFront\nエッジ', 110, 58, 9)
    s += icon('alb2', 680, 150, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('asg2', 790, 150, 'ec2', AWS_ORANGE, 'ASG (配置済)', 130, 58, 9, True)
    s += icon('aw2', 920, 150, 'aurora', AWS_BLUE, 'Aurora\nGlobal (S)', 110, 58, 9, True)
    s += icon('s3_2', 560, 280, 's3', AWS_GREEN, 'S3 CRR ターゲット', 150, 58, 9, True)
    s += text_box('n2', 540, 380, 430, 120,
                  '【EU読み取り】\n・Aurora Secondary ローカル読取 (低レイテンシ)\n'
                  '・S3 静的コンテンツ EU コピー\n・CloudFront+ALB で応答\n・書込は北米 Primary へ', AWS_GREEN, 10)

    s += arrow('u1', 'r53', 'cf1', AWS_PURPLE, 2)
    s += arrow('u2', 'r53', 'cf2', AWS_PURPLE, 2)
    s += arrow('rep1', 'aw1', 'aw2', AWS_PINK, 4, False, 'Aurora物理レプリ <1秒')
    s += arrow('rep2', 's3_1', 's3_2', AWS_PINK, 3, False, 'S3 CRR')

    s += text_box('cmp', 20, 530, 960, 60,
                  '❌ A: 論理レプリは遅い／S3にWebサーバ置換は非現実\n❌ B: Global Accelerator は TCP/UDPレベル、ウェブ動的+静的に CloudFront の方が良い\n'
                  '❌ C: RDB→DynamoDBへの単純移行は現実的でない (関係性スキーマ要件)',
                  NAVY, 9, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-109', s)


# =====================================================================
# UDEMY-284 (num=583) Game - S3 CRR + CloudFront Origin Failover + DynamoDB GT
# Answer C
# =====================================================================
def q_udemy_284():
    s = header('UDEMY-284 / 正解C: S3 CRR + CloudFront Origin Failover + DynamoDB Global Tables')
    s += icon('cf', 360, 20, 'cloudfront', AWS_PURPLE, 'CloudFront (Origin Group で2バケット切替)', 360, 58, 10, True)

    s += region('r1', 'ap-northeast-1', 20, 90, 460, 430, AWS_BLUE)
    s += icon('s3_1', 60, 150, 's3', AWS_GREEN, 'S3 バケット\n(Primary)', 120, 58, 9, True)
    s += icon('ddb1', 210, 150, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 150, 58, 9, True)
    s += icon('str1', 210, 280, 'dynamodb', AWS_BLUE, 'DynamoDB Streams', 150, 58, 9)
    s += text_box('n1', 40, 370, 430, 130,
                  '【Primary】\n・S3 にキャラクター画像\n・DynamoDB にプレイヤー属性\n'
                  '・Streams 有効化 (GT必須)\n・CloudFrontオリジン1', AWS_BLUE, 10)

    s += region('r2', 'us-east-1 (新Region)', 520, 90, 460, 430, AWS_GREEN)
    s += icon('s3_2', 560, 150, 's3', AWS_GREEN, 'S3 バケット\n(CRR先)', 120, 58, 9, True)
    s += icon('ddb2', 710, 150, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 150, 58, 9, True)
    s += icon('str2', 710, 280, 'dynamodb', AWS_BLUE, 'DynamoDB Streams', 150, 58, 9)
    s += text_box('n2', 540, 370, 430, 130,
                  '【新Region】\n・S3 CRR で自動複製\n・DynamoDB GT 書き込み可\n'
                  '・CloudFront Origin Group の\n　セカンダリオリジン', AWS_GREEN, 10)

    s += arrow('cf1', 'cf', 's3_1', AWS_PURPLE, 2, False, 'Primary Origin')
    s += arrow('cf2', 'cf', 's3_2', AWS_PURPLE, 2, True, 'Failover Origin')
    s += arrow('cr', 's3_1', 's3_2', AWS_PINK, 3, False, 'S3 CRR')
    s += bi_arrow('dr', 'str1', 'str2', AWS_PINK, 3, False, 'Global Tables 双方向')

    s += text_box('cmp', 20, 530, 960, 60,
                  '❌ A: S3 CRRだが CloudFront Origin Failover なし → バケット障害時フェイルオーバーなし\n'
                  '❌ B: DMSはDynamoDBレプリに使わない／同一Region S3レプリは意味がない\n'
                  '❌ D: 同一Region S3複製ではリージョン障害対策にならない',
                  NAVY, 9, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-284', s)


# =====================================================================
# UDEMY-333 (num=632) IoT Core multi-region + DynamoDB Global Table
# Answer C: IoT Core domains + Route53 health check + failover + DynamoDB GT
# =====================================================================
def q_udemy_333():
    s = header('UDEMY-333 / 正解C: IoT Core ドメイン + Route 53 ヘルスチェック Failover + DynamoDB GT')
    s += icon('sensor', 40, 30, 'backup', '#666666', '工場センサー群 (MQTT)', 180, 58, 10, True)
    s += icon('r53', 340, 30, 'route_53', AWS_PURPLE, 'Route 53 Failover (カスタムドメイン)', 320, 58, 10, True)

    s += region('r1', 'Region 1 (Primary)', 20, 120, 460, 400, AWS_BLUE)
    s += icon('iot1', 60, 180, 'cloudendure_disaster_recovery', AWS_PINK, 'IoT Core\nドメイン構成', 150, 58, 9, True)
    # use a substitute; IoT Core icon may not be in list, use fallback
    s += icon('ddb1', 220, 180, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 150, 58, 9, True)
    s += icon('hc1', 380, 180, 'cloudwatch', AWS_PURPLE, 'HealthCheck', 100, 58, 9, True)
    s += text_box('n1', 40, 290, 430, 200,
                  '【Primary】\n・IoT Core にカスタムドメイン割当\n'
                  '・MQTT メッセージ受信\n・IoT Ruleで DynamoDB に書込\n'
                  '・DynamoDB は Global Tables 有効', AWS_BLUE, 10)

    s += region('r2', 'Region 2 (Failover)', 520, 120, 460, 400, AWS_GREEN)
    s += icon('iot2', 560, 180, 'cloudendure_disaster_recovery', AWS_PINK, 'IoT Core\nドメイン構成', 150, 58, 9, True)
    s += icon('ddb2', 720, 180, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 150, 58, 9, True)
    s += icon('hc2', 880, 180, 'cloudwatch', AWS_PURPLE, 'HealthCheck', 100, 58, 9, True)
    s += text_box('n2', 540, 290, 430, 200,
                  '【Failover】\n・同じカスタムドメイン\n・Route 53 ヘルスチェック異常時\n　Failoverレコードで切替\n'
                  '・DynamoDB Global Tables で\n　データ即時利用可', AWS_GREEN, 10)

    s += arrow('s1', 'sensor', 'r53', NAVY, 2, False, 'MQTT')
    s += arrow('r1a', 'r53', 'iot1', AWS_PURPLE, 2, False, 'Primary')
    s += arrow('r1b', 'r53', 'iot2', AWS_PURPLE, 2, True, 'Failover')
    s += arrow('w1', 'iot1', 'ddb1', AWS_BLUE, 2)
    s += arrow('w2', 'iot2', 'ddb2', AWS_BLUE, 2)
    s += bi_arrow('rep', 'ddb1', 'ddb2', AWS_PINK, 3, False, 'Global Tables 双方向')

    s += text_box('cmp', 20, 530, 960, 60,
                  '❌ A: Aurora "グローバルテーブル"という用語は誤り(Aurora Global DatabaseならOK、ただしDynamoDB要件のまま)\n'
                  '❌ B: MemoryDB Redis はクロスリージョンレプリに正式対応せず、耐久性も弱い\n'
                  '❌ D: レイテンシーはフェイルオーバー用途でない／DynamoDB Streams=リージョン内',
                  NAVY, 9, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-333', s)


# =====================================================================
# UDEMY-072 (num=371) Aurora MySQL single region → global
# We'll show Aurora Global DB cross-region for retail ecom
# =====================================================================
def q_udemy_072():
    s = header('UDEMY-072 / Aurora Global Database 移行 (小売 eコマース)')
    s += region('rp', 'Primary Region (現行)', 20, 60, 460, 430, AWS_BLUE)
    s += icon('app_p', 60, 120, 'ec2', AWS_ORANGE, 'アプリ層 (書込)', 130, 58, 9, True)
    s += icon('aw_p', 200, 120, 'aurora', AWS_BLUE, 'Aurora MySQL\nWriter', 140, 58, 9, True)
    s += icon('ar_p', 350, 120, 'aurora', AWS_BLUE, 'Aurora\nReader×4', 120, 58, 9)
    s += arrow('p1', 'app_p', 'aw_p', AWS_BLUE, 2)
    s += arrow('p2', 'aw_p', 'ar_p', AWS_BLUE, 1, True)
    s += text_box('pn', 40, 250, 430, 230,
                  '【要件】\n・顧客プロフィール/注文履歴/在庫\n・5ノードAurora MySQLクラスタ\n・グローバル顧客\n・地域別低レイテンシ読取\n\n'
                  '【改善】Aurora Global Database 化\n → Secondary リージョンで 読取/DR', AWS_BLUE, 10)

    s += region('rs', 'Secondary Region', 520, 60, 460, 430, AWS_GREEN)
    s += icon('app_s', 560, 120, 'ec2', AWS_ORANGE, 'アプリ (読取)', 130, 58, 9, True)
    s += icon('aw_s', 700, 120, 'aurora', AWS_BLUE, 'Aurora Global\nSecondary Reader', 160, 58, 9, True)
    s += icon('ar_s', 870, 120, 'aurora', AWS_BLUE, 'ローカル\nReader', 110, 58, 9)
    s += arrow('s1', 'app_s', 'aw_s', AWS_GREEN, 2, False, 'ローカル読取')
    s += arrow('s2', 'aw_s', 'ar_s', AWS_GREEN, 1, True)
    s += text_box('sn', 540, 250, 430, 230,
                  '【ポイント】\n・物理ストレージレプリ、RPO <1秒\n'
                  '・書込は Primary のみ(Write Forwarding可)\n'
                  '・障害時 Managed Failover で Promote\n'
                  '　(RTO <1分)\n\n→ 低レイテンシ読取＋クロスリージョンDR 両立', AWS_GREEN, 10)

    s += arrow('rep', 'aw_p', 'aw_s', AWS_PINK, 4, False, 'Aurora物理レプリ <1秒')

    s += text_box('cmp', 20, 500, 960, 90,
                  '💡 Aurora Global Database の特徴\n'
                  '・Primary 1 + Secondary 最大5リージョン／読取Endpointで低レイテンシ\n'
                  '・RPO <1秒 / RTO <1分 (Managed Failover)\n'
                  '・Write Forwarding (Aurora MySQLのみ) — SecondaryからPrimaryへ書込転送',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-072', s)


# =====================================================================
# UDEMY-092 (num=391) EHR medical multi-region DR
# We'll show Aurora Global DB + DynamoDB Global Tables for EHR
# =====================================================================
def q_udemy_092():
    s = header('UDEMY-092 / 医療EHR: DynamoDB Global Tables + Aurora Global DB')
    s += region('r1', 'Region 1 (Primary)', 20, 60, 460, 440, AWS_BLUE)
    s += icon('app1', 60, 120, 'ec2', AWS_ORANGE, 'EHR/予約\nアプリ', 110, 58, 9, True)
    s += icon('ddb1', 190, 120, 'dynamodb', AWS_BLUE, 'DynamoDB GT\n(患者識別/予約)', 160, 58, 9, True)
    s += icon('aw1', 370, 120, 'aurora', AWS_BLUE, 'Aurora Global\n(EHR 本体)', 140, 58, 9, True)
    s += text_box('n1', 40, 240, 430, 260,
                  '【設計判断】\n\n'
                  '① 患者識別ID/予約テーブル(KVベース)\n'
                  ' → DynamoDB Global Tables\n'
                  '  (Active-Active、低レイテンシ、耐障害性)\n\n'
                  '② 医療記録本体 (関係/トランザクション)\n'
                  ' → Aurora Global Database\n'
                  '  (RPO<1秒、ACID保証)\n\n'
                  '③ マルチリージョンで常時待機\n'
                  '  災害時も閉院なし', AWS_BLUE, 10)

    s += region('r2', 'Region 2 (DR/Active)', 520, 60, 460, 440, AWS_GREEN)
    s += icon('app2', 560, 120, 'ec2', AWS_ORANGE, 'EHR/予約\nアプリ', 110, 58, 9, True)
    s += icon('ddb2', 690, 120, 'dynamodb', AWS_BLUE, 'DynamoDB GT\nレプリカ', 140, 58, 9, True)
    s += icon('aw2', 860, 120, 'aurora', AWS_BLUE, 'Aurora Global\nSecondary', 140, 58, 9, True)
    s += text_box('n2', 540, 240, 430, 260,
                  '【セカンダリ】\n・DynamoDB: どちら書込でもOK\n  （LWWで衝突解決）\n\n'
                  '・Aurora: 低レイテンシ読取\n  障害時 Promote で書込\n\n'
                  '・コンプライアンス: 暗号化/監査\n  (KMSマルチRegionキー推奨)', AWS_GREEN, 10)

    s += bi_arrow('rep1', 'ddb1', 'ddb2', AWS_PINK, 3, False, 'Global Tables 双方向')
    s += arrow('rep2', 'aw1', 'aw2', AWS_PINK, 4, False, 'Aurora物理レプリ')

    s += text_box('cmp', 20, 510, 960, 80,
                  '💡 KVベースの参照データ → DynamoDB Global Tables、関係トランザクション → Aurora Global DB が定石\n'
                  '⚠️ HIPAA: 医療データはKMS暗号化/CloudTrail/VPC分離が必須',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-092', s)


# =====================================================================
# UDEMY-219 (num=518) Active-passive DR — 2 VPCs + Route 53 with health checks
# Answer B (presumed): dual VPCs in 2 regions, Route 53 health check with failover
# =====================================================================
def q_udemy_219():
    s = header('UDEMY-219 / 銀行DR: 2VPC + Route 53 ヘルスチェックフェイルオーバー')
    s += icon('r53', 340, 20, 'route_53', AWS_PURPLE, 'Route 53 Failover + ヘルスチェック', 320, 58, 10, True)

    s += region('rp', 'us-east-1 (Primary)', 20, 90, 460, 430, AWS_BLUE)
    s += icon('alb_p', 60, 150, 'application_load_balancer', AWS_PURPLE, 'ALB (Multi-AZ)')
    s += icon('asg_p', 200, 150, 'ec2', AWS_ORANGE, 'EC2 ASG\n(動的スケール)', 150, 58, 9, True)
    s += icon('rds_p', 360, 150, 'rds', AWS_BLUE, 'RDS', 80, 58, 9, True)
    s += text_box('pn', 40, 270, 430, 230,
                  '【Primary VPC】\n・ALB + Auto Scaling (3AZ)\n・高可用性\n・動的スケール\n\n'
                  '【Route 53】\n・ヘルスチェックでALB監視\n・異常時 Secondary VPC へ\n　自動フェイルオーバー', AWS_BLUE, 10)

    s += region('rs', 'us-west-1 (DR Passive)', 520, 90, 460, 430, AWS_GREEN)
    s += icon('alb_s', 560, 150, 'application_load_balancer', AWS_PURPLE, 'ALB (Multi-AZ)')
    s += icon('asg_s', 700, 150, 'ec2', AWS_ORANGE, 'EC2 ASG\n(待機)', 130, 58, 9, True)
    s += icon('rds_s', 860, 150, 'rds', AWS_BLUE, 'RDS', 80, 58, 9, True)
    s += text_box('sn', 540, 270, 430, 230,
                  '【DR VPC (us-west-1)】\n・同構成を複製\n・通常は最小台数または停止\n\n'
                  '【切替】\n・Route 53 レコードをPrimary+Secondary\n'
                  '・ヘルスチェック失敗時Secondaryへ', AWS_GREEN, 10)

    s += arrow('r1', 'r53', 'alb_p', AWS_PURPLE, 2, False, 'Primary')
    s += arrow('r2', 'r53', 'alb_s', AWS_PURPLE, 2, True, 'Failover')

    s += text_box('cmp', 20, 530, 960, 60,
                  '❌ A: VPCピアリング不要(Route53でDNS切替のみ)、SecondaryVPCの冗長性も不足\n'
                  '❌ C/D: Global Acceleratorやアクティブ-アクティブは要件 "アクティブ-パッシブ" と一致しない',
                  NAVY, 9, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-219', s)


# =====================================================================
# UDEMY-297 (num=596) 貿易会社ハイブリッド — Elastic DR
# =====================================================================
def q_udemy_297():
    s = header('UDEMY-297 / ハイブリッドDR: Elastic Disaster Recovery (オンプレ→AWS)')
    s += dc('op', 'オンプレミス DC', 20, 60, 440, 430)
    s += icon('srv', 60, 130, 'ec2', '#666666', '通関関連サーバー\n(法令によりオンプレ)', 170, 58, 9, True)
    s += icon('drs_a', 250, 130, 'cloudendure_disaster_recovery', AWS_RED, 'DRS Agent\n(継続レプリ)', 140, 58, 9, True)
    s += text_box('op_n', 40, 260, 400, 220,
                  '【オンプレ要件】\n・法令でインターネット接続可\n  通関ファイルはオンプレ\n'
                  '・AWS とハイブリッドに統合\n\n'
                  '【DR戦略】\n・Elastic DRをオンプレにインストール\n'
                  '・ブロックレベル継続レプリ\n・RPO 秒〜分／RTO 数分', '#333333', 10)

    s += region('aws', 'AWS Region', 480, 60, 500, 430, AWS_BLUE)
    s += icon('drs_s', 520, 130, 'cloudendure_disaster_recovery', AWS_RED, 'Elastic DR\n(ステージング)', 150, 58, 9, True)
    s += icon('ec2_dr', 700, 130, 'ec2', AWS_ORANGE, 'DR EC2 起動', 130, 58, 9, True)
    s += icon('s3', 840, 130, 's3', AWS_GREEN, 'EBS\nスナップショット', 140, 58, 9)
    s += text_box('aws_n', 500, 260, 460, 230,
                  '【フェイルオーバー】\n・障害検知 → Elastic DR で数分以内に\n　EC2 起動 (AMIベース)\n'
                  '・EBS ボリュームは最新ステートで提供\n\n'
                  '【フェイルバック】\n・同じDRSでオンプレに戻す\n・双方向動作が強み', AWS_BLUE, 10)

    s += arrow('rep', 'drs_a', 'drs_s', AWS_RED, 4, False, '継続ブロックレプリ')
    s += arrow('fo', 'drs_s', 'ec2_dr', AWS_RED, 2, True, 'フェイルオーバー起動')

    s += text_box('cmp', 20, 510, 960, 80,
                  '💡 Elastic Disaster Recovery (DRS) = CloudEndure の後継\n'
                  '・オンプレ→AWS、AWS Region間の両方で動作／フェイルバック対応／RPO秒〜分・RTO分',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-297', s)


# =====================================================================
# UDEMY-320 (num=619) CodeCommit cross-region backup
# =====================================================================
def q_udemy_320():
    s = header('UDEMY-320 / CodeCommit クロスリージョンバックアップ (EventBridge+Lambda)')
    s += region('r1', 'Primary Region', 20, 60, 460, 420, AWS_BLUE)
    s += icon('cc', 60, 130, 'cloudwatch', AWS_ORANGE, 'CodeCommit\nリポジトリ', 130, 58, 9, True)
    s += icon('eb', 220, 130, 'cloudwatch', AWS_PINK, 'EventBridge\n(スケジュール)', 140, 58, 9, True)
    s += icon('lam', 380, 130, 'ec2', AWS_ORANGE, 'Lambda\n(git clone→S3)', 130, 58, 9, True)
    s += icon('s3_p', 60, 260, 's3', AWS_GREEN, 'S3 (Primary)', 130, 58, 9, True)
    s += text_box('n1', 40, 340, 430, 130,
                  '【構成】\n・EventBridge 定期スケジュール\n'
                  '・Lambda で git clone → S3 にダンプ\n'
                  '・S3 クロスリージョンレプリで2Region化', AWS_BLUE, 10)

    s += region('r2', '地理的に離れた Region', 520, 60, 460, 420, AWS_GREEN)
    s += icon('s3_s', 560, 260, 's3', AWS_GREEN, 'S3 (CRR 先)\nVersioning 有効', 160, 58, 9, True)
    s += text_box('n2', 540, 340, 430, 130,
                  '【バックアップ先】\n・リージョンレベル耐障害性\n・Versioning 有効で履歴保持\n'
                  '・別アカウント/MFA Delete 併用で堅牢化', AWS_GREEN, 10)

    s += arrow('a1', 'eb', 'lam', AWS_PINK, 2)
    s += arrow('a2', 'lam', 'cc', NAVY, 2, False, 'git clone')
    s += arrow('a3', 'lam', 's3_p', AWS_GREEN, 2, False, '書込')
    s += arrow('a4', 's3_p', 's3_s', AWS_PINK, 3, False, 'S3 CRR')

    s += text_box('cmp', 20, 490, 960, 100,
                  '💡 CodeCommit 自体はリージョナルサービスでマネージドクロスリージョン機能なし\n'
                  '・EventBridge スケジュール＋Lambda で git clone → S3 アーカイブ\n'
                  '・S3 CRR で地理的に離れたRegionへ複製\n'
                  '・バージョニング/MFA Deleteで改ざん対策も推奨',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-320', s)


# =====================================================================
# UDEMY-335 (num=634) S3 CRR + CloudFront + 北米/アジア
# =====================================================================
def q_udemy_335():
    s = header('UDEMY-335 / メディア配信: S3 クロスリージョンレプリ + CloudFront')
    s += icon('cf', 360, 20, 'cloudfront', AWS_PURPLE, 'CloudFront (世界中のエッジロケーション)', 360, 58, 10, True)

    s += region('r1', 'Region 1 (北米: us-east-1)', 20, 90, 460, 420, AWS_BLUE)
    s += icon('s3_1', 180, 170, 's3', AWS_GREEN, 'S3 Source Bucket\n(高解像度画像/動画)', 160, 58, 9, True)
    s += text_box('n1', 40, 280, 430, 220,
                  '【ソース】\n・高解像度画像と動画を格納\n・ライフサイクルルール推奨\n\n'
                  '【CloudFront 統合】\n・Origin に S3 指定\n'
                  '・世界中のエッジでキャッシュ配信\n・OAI/OAC で S3 直アクセス防止', AWS_BLUE, 10)

    s += region('r2', 'Region 2 (アジア: ap-northeast-1)', 520, 90, 460, 420, AWS_GREEN)
    s += icon('s3_2', 680, 170, 's3', AWS_GREEN, 'S3 Replica Bucket\n(CRR で自動複製)', 170, 58, 9, True)
    s += text_box('n2', 540, 280, 430, 220,
                  '【CRR】\n・バージョニング必須\n・IAMロール経由で複製\n・自動で新規オブジェクトを\n　レプリカ先に複製\n\n'
                  '【メリット】\n・リージョン障害耐性\n・コンプライアンス要件対応', AWS_GREEN, 10)

    s += arrow('c1', 'cf', 's3_1', AWS_PURPLE, 2, False, 'Primary Origin')
    s += arrow('c2', 'cf', 's3_2', AWS_PURPLE, 2, True, 'Failover Origin\n(Origin Group)')
    s += arrow('crr', 's3_1', 's3_2', AWS_PINK, 4, False, 'S3 CRR 自動複製')

    s += text_box('cmp', 20, 520, 960, 70,
                  '💡 配信パターン:\n'
                  '  ① CloudFront + 単一S3 で十分な地域   → エッジキャッシュのみ\n'
                  '  ② 地理的DR/低レイテンシ読取          → CRR + CloudFront Origin Failover',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-335', s)


# =====================================================================
# UDEMY-343 (num=642) media S3 CRR
# =====================================================================
def q_udemy_343():
    s = header('UDEMY-343 / メディア全世界配信: マルチRegion S3 + CloudFront')
    s += icon('cf', 360, 20, 'cloudfront', AWS_PURPLE, 'CloudFront (エッジキャッシュ) + Origin Group', 380, 58, 10, True)

    s += region('r1', 'Region A (北米/現行)', 20, 90, 300, 430, AWS_BLUE)
    s += icon('s3_1', 120, 180, 's3', AWS_GREEN, 'S3 オリジナル\n(動画/音楽)', 130, 58, 9, True)
    s += text_box('n1', 40, 300, 270, 200,
                  '【ソース】\n・既存 S3 バケット\n・メディアコンテンツ\n\n'
                  '【CloudFront】\n・既存利用中\n・origin=このバケット', AWS_BLUE, 10)

    s += region('r2', 'Region B (EU)', 340, 90, 300, 430, AWS_GREEN)
    s += icon('s3_2', 440, 180, 's3', AWS_GREEN, 'S3 レプリカ\n(EU)', 120, 58, 9, True)
    s += text_box('n2', 360, 300, 270, 200,
                  'CRR で自動複製\nレイテンシ低減\nリージョン障害対応', AWS_GREEN, 10)

    s += region('r3', 'Region C (AP)', 660, 90, 320, 430, AWS_GREEN)
    s += icon('s3_3', 770, 180, 's3', AWS_GREEN, 'S3 レプリカ\n(AP)', 120, 58, 9, True)
    s += text_box('n3', 680, 300, 290, 200,
                  'CRR で自動複製\nアジアユーザー向け\n低レイテンシ', AWS_GREEN, 10)

    s += arrow('cf1', 'cf', 's3_1', AWS_PURPLE, 2, False, 'Primary')
    s += arrow('cf2', 'cf', 's3_2', AWS_PURPLE, 2, True, 'Origin Group')
    s += arrow('cf3', 'cf', 's3_3', AWS_PURPLE, 2, True, 'Origin Group')
    s += arrow('r12', 's3_1', 's3_2', AWS_PINK, 3, False, 'CRR')
    s += arrow('r13', 's3_1', 's3_3', AWS_PINK, 3, False, 'CRR')

    s += text_box('cmp', 20, 530, 960, 60,
                  '💡 S3 Replication の選び方: 1対1なら CRR、1対多なら S3 Multi-Region Access Point または複数CRR\n'
                  '・CloudFront Origin Failover で Region障害時の自動切替も可能',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-343', s)


# =====================================================================
# UDEMY-146 (num=445) CloudFront Origin Group failover (<45s)
# Answer D
# =====================================================================
def q_udemy_146():
    s = header('UDEMY-146 / 正解D: CloudFront Origin Group によるオリジンフェイルオーバー')
    s += icon('cf', 370, 20, 'cloudfront', AWS_PURPLE, 'CloudFront (Origin Group = Primary + Secondary)', 420, 58, 10, True)

    s += region('rp', 'Primary Region', 20, 90, 460, 430, AWS_BLUE)
    s += icon('alb_p', 60, 170, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('app_p', 180, 170, 'ec2', AWS_ORANGE, 'Backend サービス', 150, 58, 9, True)
    s += text_box('n1', 40, 290, 430, 210,
                  '【Origin Group】\n・Primary Origin = Primary ALB\n・Secondary Origin = DR ALB\n\n'
                  '【動作】\n・500/502/503/504など設定したステータスコードや\n'
                  '  接続失敗時に CloudFront が即座に\n  Secondary へ切替\n\n'
                  '・DNS伝搬(TTL)に依存しない → 数秒以内', AWS_BLUE, 10)

    s += region('rs', 'DR Region', 520, 90, 460, 430, AWS_GREEN)
    s += icon('alb_s', 560, 170, 'application_load_balancer', AWS_PURPLE, 'ALB')
    s += icon('app_s', 680, 170, 'ec2', AWS_ORANGE, 'Backend サービス', 150, 58, 9, True)
    s += text_box('n2', 540, 290, 430, 210,
                  '【従来構成との違い】\n・Route 53 Failover は DNS TTL 依存 (45秒以上)\n'
                  '・CloudFront Origin Group はTCP接続レベルで\n  即座にフェイルオーバー\n\n'
                  '・顧客データの可用性を最速で確保\n・TTL短縮(案B)は改善しても不十分', AWS_GREEN, 10)

    s += arrow('o1', 'cf', 'alb_p', AWS_PURPLE, 2, False, 'Primary Origin')
    s += arrow('o2', 'cf', 'alb_s', AWS_PURPLE, 2, True, 'Secondary Origin (失敗時)')

    s += text_box('cmp', 20, 530, 960, 60,
                  '❌ A: CloudFront 2個 → 冗長だが Route 53 DNS TTL 制約残る\n'
                  '❌ B: TTL=5秒 → リゾルバキャッシュで45秒未満は保証されない\n❌ C: レイテンシーはDR用途ではない',
                  NAVY, 9, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-146', s)


# =====================================================================
# UDEMY-353 (num=652) AWS Backup EC2+EBS cross-region RTO12h RPO24h
# Answer C: AWS Backup plan + cross-region copy
# =====================================================================
def q_udemy_353():
    s = header('UDEMY-353 / 正解C: AWS Backup プラン + クロスリージョンボールト (RTO12h/RPO24h)')
    s += region('rp', 'us-east-1 (Primary)', 20, 60, 460, 420, AWS_BLUE)
    s += icon('ec2', 60, 120, 'ec2', AWS_ORANGE, 'EC2 ×10\n(c5.2xlarge)', 130, 58, 9, True)
    s += icon('ebs', 210, 120, 'backup', AWS_GREEN, '複数 EBS\nボリューム', 120, 58, 9)
    s += icon('bk', 340, 120, 'backup', AWS_RED, 'AWS Backup\n(日次)', 130, 58, 9, True)
    s += icon('vault_p', 340, 260, 'backup', AWS_RED, 'Backup Vault', 130, 58, 9, True)
    s += text_box('pn', 40, 340, 430, 130,
                  '【要件】\n・広告プラットフォーム運用\n・RPO 24h / RTO 12h\n'
                  '・us-east-1 → us-west-2\n・CloudFormation で復元可', AWS_BLUE, 10)

    s += region('rs', 'us-west-2 (Secondary)', 520, 60, 460, 420, AWS_GREEN)
    s += icon('vault_s', 560, 120, 'backup', AWS_RED, 'Backup Vault\n(コピー先)', 140, 58, 9, True)
    s += icon('cfn', 720, 120, 'cloudwatch', AWS_PURPLE, 'CloudFormation', 160, 58, 9, True)
    s += icon('ec2_s', 900, 120, 'ec2', AWS_ORANGE, 'EC2 復元', 100, 58, 9, True)
    s += text_box('sn', 540, 260, 430, 220,
                  '【DR発動】\n① CloudFormationを起動\n  → ALB/ASG/ネットワーク作成\n\n'
                  '② Vault からボリュームを復元\n  → EC2 にアタッチ\n\n'
                  '③ アプリ移行完了\n\n'
                  '→ RTO 12h 余裕あり', AWS_GREEN, 10)

    s += arrow('a1', 'ec2', 'bk', AWS_RED, 2, False, '日次バックアップ')
    s += arrow('a2', 'bk', 'vault_p', AWS_RED, 2)
    s += arrow('a3', 'vault_p', 'vault_s', AWS_PINK, 3, False, 'クロスリージョンコピー')
    s += arrow('a4', 'vault_s', 'ec2_s', AWS_RED, 2, True, '復元')

    s += text_box('cmp', 20, 490, 960, 100,
                  '✅ 正解C: AWS Backup は EC2/EBS/RDS/EFS/FSx 等を統合管理、クロスリージョンコピー設定可\n'
                  '❌ A: Systems Manager Automationでマルチボリュームスナップショットは可だがAWS Backupの方が運用楽\n'
                  '❌ B: DLMはクロスリージョンコピーの運用がAWS Backupより煩雑\n'
                  '❌ D: DataSyncはファイル同期用、EBSブロック複製には不向き',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-353', s)


# =====================================================================
# UDEMY-282 (num=581) serverless SNS/SQS/Lambda multi-region
# Answer C+A
# =====================================================================
def q_udemy_282():
    s = header('UDEMY-282 / 正解C+A: 各Region SQS+Lambda + SNS に各SQSをサブスクライブ')
    s += region('r1', 'Primary Region (SNS発行元)', 20, 60, 460, 500, AWS_BLUE)
    s += icon('sns', 60, 120, 'cloudwatch', AWS_PINK, 'SNS Topic\n(URL発行)', 140, 58, 9, True)
    s += icon('sqs_p', 220, 120, 'backup', AWS_PINK, 'SQS (既存)', 120, 58, 9, True)
    s += icon('lam_p', 360, 120, 'ec2', AWS_ORANGE, 'Lambda', 100, 58, 9, True)
    s += icon('s3', 220, 280, 's3', AWS_GREEN, 'S3 (結果)\n※現Regionのみ', 150, 58, 9, True)
    s += arrow('a1', 'sns', 'sqs_p', AWS_PINK, 2, False, 'サブスクライブ')
    s += arrow('a2', 'sqs_p', 'lam_p', AWS_PINK, 2)
    s += arrow('a3', 'lam_p', 's3', AWS_GREEN, 2, False, '結果書込')
    s += text_box('n1', 40, 380, 430, 170,
                  '【制約】\n・URL は既存 Region で発行\n・結果は既存 S3 に書き込み\n\n'
                  '【変更C】各リージョンの SQS キューを\n  SNS トピックにサブスクライブ', AWS_BLUE, 10)

    s += region('r2', '追加 Region 1', 520, 60, 230, 500, AWS_GREEN)
    s += icon('sqs_2', 575, 120, 'backup', AWS_PINK, 'SQS', 80, 58, 9, True)
    s += icon('lam_2', 575, 260, 'ec2', AWS_ORANGE, 'Lambda', 80, 58, 9, True)
    s += arrow('b1', 'sqs_2', 'lam_2', AWS_PINK, 2)
    s += text_box('n2', 540, 380, 210, 170,
                  '【変更A】\nSQS+Lambda を\n他Regionにデプロイ', AWS_GREEN, 9)

    s += region('r3', '追加 Region 2', 760, 60, 220, 500, AWS_GREEN)
    s += icon('sqs_3', 810, 120, 'backup', AWS_PINK, 'SQS', 80, 58, 9, True)
    s += icon('lam_3', 810, 260, 'ec2', AWS_ORANGE, 'Lambda', 80, 58, 9, True)
    s += arrow('c1', 'sqs_3', 'lam_3', AWS_PINK, 2)
    s += text_box('n3', 770, 380, 210, 170,
                  '全Regionの Lambdaは\nPrimaryのS3に書込', AWS_GREEN, 9)

    s += arrow('sub1', 'sns', 'sqs_2', AWS_PINK, 2, True, 'サブスクライブ(クロスRegion)')
    s += arrow('sub2', 'sns', 'sqs_3', AWS_PINK, 2, True, 'サブスクライブ')
    s += arrow('w1', 'lam_2', 's3', AWS_GREEN, 2, True)
    s += arrow('w2', 'lam_3', 's3', AWS_GREEN, 2, True)

    s += text_box('cmp', 20, 560, 960, 30,
                  '💡 SNS はクロスRegion サブスクリプション対応 — SQS/Lambda はRegion固有なので明示デプロイ必要',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-282', s)


# =====================================================================
# UDEMY-304 (num=603) DynamoDB Global Tables global consistent RW
# =====================================================================
def q_udemy_304():
    s = header('UDEMY-304 / DynamoDB Global Tables (複数Region一貫した読み書き)')
    s += region('r1', 'Region A (北米)', 20, 70, 310, 440, AWS_BLUE)
    s += icon('app1', 120, 130, 'ec2', AWS_ORANGE, 'アプリ', 100, 58, 9, True)
    s += icon('ddb1', 120, 260, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 150, 58, 9, True)
    s += bi_arrow('a1', 'app1', 'ddb1', AWS_BLUE, 2, False, '読み書き(ローカル)')
    s += text_box('n1', 40, 370, 270, 130,
                  '・各Region読み書き可\n・ローカル低レイテンシ\n・RPO 数秒／RTO ≒ 0', AWS_BLUE, 10)

    s += region('r2', 'Region B (EU)', 350, 70, 310, 440, AWS_BLUE)
    s += icon('app2', 450, 130, 'ec2', AWS_ORANGE, 'アプリ', 100, 58, 9, True)
    s += icon('ddb2', 450, 260, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 150, 58, 9, True)
    s += bi_arrow('a2', 'app2', 'ddb2', AWS_BLUE, 2, False, '読み書き')
    s += text_box('n2', 370, 370, 270, 130,
                  '・結果整合性\n・衝突: Last Writer Wins\n・Streams 有効必須', AWS_BLUE, 10)

    s += region('r3', 'Region C (AP)', 680, 70, 300, 440, AWS_BLUE)
    s += icon('app3', 780, 130, 'ec2', AWS_ORANGE, 'アプリ', 100, 58, 9, True)
    s += icon('ddb3', 780, 260, 'dynamodb', AWS_BLUE, 'DynamoDB\nGlobal Table', 150, 58, 9, True)
    s += bi_arrow('a3', 'app3', 'ddb3', AWS_BLUE, 2, False, '読み書き')
    s += text_box('n3', 700, 370, 270, 130,
                  '・テーブル作成後にRegion追加可\n・全Region同一スキーマ/GSI', AWS_BLUE, 10)

    # star topology
    s += bi_arrow('r12', 'ddb1', 'ddb2', AWS_PINK, 3)
    s += bi_arrow('r23', 'ddb2', 'ddb3', AWS_PINK, 3)
    s += bi_arrow('r13', 'ddb1', 'ddb3', AWS_PINK, 3)

    s += text_box('cmp', 20, 520, 960, 70,
                  '💡 DynamoDB Global Tables — マルチRegion Active-Active の定石\n'
                  '・ACID/関係モデル必要なら Aurora Global DB／KV+全Region書込なら DynamoDB GT',
                  NAVY, 10, False, 'left', '#FFFDE7', AWS_ORANGE)
    s += FOOTER
    write('UDEMY-304', s)


# =====================================================================
# UDEMY-011 (num=310) MQTT→IoT Core+Kinesis Firehose→S3
# Answer C (not classical DR but multi-AZ HA/scalability)
# Keep as multi-AZ architectural diagram with replacement messaging
# =====================================================================
def q_udemy_011():
    s = header('UDEMY-011 / 正解C: IoT Core + Kinesis Firehose + Lambda + S3 (HA)')
    s += icon('sensors', 40, 40, 'backup', '#666666', '土壌センサー ×15,000 (MQTT)', 250, 58, 10, True)
    s += region('aws', 'AWS (リージョンスコープ、マルチAZ)', 20, 130, 960, 400, AWS_BLUE)
    s += icon('iot', 60, 200, 'cloudendure_disaster_recovery', AWS_PINK, 'AWS IoT Core\n(マネージドMQTT)', 170, 58, 9, True)
    s += icon('fh', 260, 200, 'backup', AWS_ORANGE, 'Kinesis Data\nFirehose', 140, 58, 9, True)
    s += icon('lam', 420, 200, 'ec2', AWS_ORANGE, 'Lambda\n(処理/変換)', 130, 58, 9, True)
    s += icon('s3', 580, 200, 's3', AWS_GREEN, 'S3 (CSV)', 100, 58, 9, True)
    s += icon('cw', 720, 200, 'cloudwatch', AWS_PURPLE, 'CloudWatch\nLogs/Metrics', 140, 58, 9)

    s += arrow('a1', 'sensors', 'iot', NAVY, 2, False, 'MQTT')
    s += arrow('a2', 'iot', 'fh', AWS_PINK, 2, False, 'IoT Rule')
    s += arrow('a3', 'fh', 'lam', AWS_ORANGE, 2)
    s += arrow('a4', 'lam', 's3', AWS_GREEN, 2)

    s += text_box('n1', 40, 330, 920, 190,
                  '【なぜこの構成か】\n'
                  '・RabbitMQ サーバー単一障害 → マネージドMQTTで冗長化必須 → IoT Core\n'
                  '・15,000デバイスのスケーラビリティ → IoT Core は水平スケール\n'
                  '・リアルタイム CSV 書出 → Firehose で S3 バッファリング/バッチ書込\n'
                  '・複雑変換 → Lambda で柔軟\n\n'
                  '❌ A: RabbitMQ on EC2 は自前運用でスケーリングと可用性が弱い\n'
                  '❌ B: Amazon MQ は既存ブローカー互換のみ／15000デバイスに最適化されていない\n'
                  '❌ D: AWS IoT Core→EC2→RabbitMQは冗長で無意味', AWS_BLUE, 10)

    s += FOOTER
    write('UDEMY-011', s)


# =====================================================================
# UDEMY-222 (num=521) RDS Proxy for reconnection after failover
# Keep as a DR-reconnection diagram (Multi-AZ failover + RDS Proxy)
# =====================================================================
def q_udemy_222():
    s = header('UDEMY-222 / 正解B: RDS Proxy (Multi-AZ フェイルオーバー後の自動再接続)')
    s += region('aws', 'us-east-1 (Multi-AZ)', 20, 60, 960, 500, AWS_BLUE)
    s += icon('app', 60, 130, 'ec2', AWS_ORANGE, 'アプリ\n(再起動不要)', 130, 58, 9, True)
    s += icon('proxy', 230, 130, 'rds', AWS_PINK, 'RDS Proxy', 110, 58, 9, True)
    s += icon('az1', 400, 80, 'rds', AWS_BLUE, 'RDS MySQL\nPrimary (AZ-a)', 150, 58, 9, True)
    s += icon('az2', 400, 220, 'rds', AWS_BLUE, 'RDS MySQL\nStandby (AZ-b)', 150, 58, 9, True)
    s += arrow('p1', 'app', 'proxy', AWS_ORANGE, 2, False, 'Endpoint = Proxy')
    s += arrow('p2', 'proxy', 'az1', AWS_PINK, 2, False, 'Active')
    s += arrow('p3', 'proxy', 'az2', AWS_PINK, 2, True, 'Failover 時')
    s += arrow('repl', 'az1', 'az2', AWS_BLUE, 2, True, '同期レプリ')

    s += text_box('n1', 40, 300, 920, 240,
                  '【問題】Multi-AZ フェイルオーバー後に接続切断 → アプリ再起動が必要\n\n'
                  '【原因】アプリがRDSエンドポイント (DNS) を直接使用 → フェイルオーバー後のDNS切替を\n'
                  '           持続接続プールが追従できない\n\n'
                  '【正解Bの仕組み】\n'
                  '・RDS Proxy が接続プールを管理\n'
                  '・フェイルオーバー時、Proxy が新Primary に接続を振り直す\n'
                  '・アプリから見るとエンドポイントは不変 → 再起動不要\n\n'
                  '❌ A: Aurora Serverless v1 への全面移行は大掛かり ／ Readerエンドポイントは書込不可\n'
                  '❌ C: Auroraクラスタへの移行もオーバースペック\n'
                  '❌ D: S3→Athenaは分析用途、RDSワークロード非互換', AWS_BLUE, 10)

    s += FOOTER
    write('UDEMY-222', s)


# =====================================================================
# UDEMY-115 (num=414) Aurora Serverless v2 + Compute Savings Plans
# =====================================================================
def q_udemy_115():
    s = header('UDEMY-115 / 正解D: Aurora Serverless v2 + Compute Savings Plans')
    s += region('aws', 'AWS Region', 20, 60, 960, 500, AWS_BLUE)
    s += icon('lam', 60, 130, 'ec2', AWS_ORANGE, 'Lambda\n(取引分析)', 130, 58, 9, True)
    s += icon('fg', 220, 130, 'ec2', AWS_ORANGE, 'ECS on Fargate\n(コンテナ)', 140, 58, 9, True)
    s += icon('auv2', 400, 130, 'aurora', AWS_BLUE, 'Aurora PostgreSQL\nServerless v2', 170, 58, 9, True)
    s += icon('sp', 600, 130, 'cloudwatch', AWS_PURPLE, 'Compute\nSavings Plans', 160, 58, 9, True)

    s += arrow('a1', 'lam', 'auv2', AWS_BLUE, 2)
    s += arrow('a2', 'fg', 'auv2', AWS_BLUE, 2)
    s += arrow('a3', 'sp', 'lam', AWS_PURPLE, 2, True, '割引')
    s += arrow('a4', 'sp', 'fg', AWS_PURPLE, 2, True, '割引')

    s += text_box('n1', 40, 280, 920, 260,
                  '【要件】\n・利用パターン変動大 (低利用長期 + 突発スパイク)\n・コスト最適化\n\n'
                  '【正解Dの構成】\n'
                  '・Aurora PostgreSQL Serverless v2\n  → ACU単位で秒〜分単位に自動スケール、アイドル時は最小まで縮退\n'
                  '・Compute Savings Plans\n  → Lambda と Fargate の両方に割引適用 (計算系全般)\n\n'
                  '❌ A: リードレプリカ追加ではスパイクのライト負荷に対応できない\n'
                  '❌ B: Aurora マルチマスターは2023年廃止\n'
                  '❌ C: Aurora Global DB は地理的分散用途でコスト最適化目的に不適合', AWS_BLUE, 10)

    s += FOOTER
    write('UDEMY-115', s)


# Execute all generators
if __name__ == '__main__':
    q_udemy_351(); q_udemy_008(); q_udemy_046(); q_udemy_309(); q_udemy_318()
    q_udemy_070(); q_udemy_091(); q_udemy_107(); q_udemy_158(); q_udemy_014()
    q_udemy_086(); q_udemy_109(); q_udemy_284(); q_udemy_333(); q_udemy_072()
    q_udemy_092(); q_udemy_219(); q_udemy_297(); q_udemy_320(); q_udemy_335()
    q_udemy_343(); q_udemy_146(); q_udemy_353(); q_udemy_282(); q_udemy_304()
    q_udemy_011(); q_udemy_222(); q_udemy_115()
    print('\nAll drawio files generated.')
