#!/usr/bin/env python3
"""Generate drawio files for 27 CloudTech SAP-xxx multi-account questions.

Outputs to /Users/aki/aws-sap/docs/diagrams/per-question/SAP-NNN.drawio
Uses AWS official icons (mxgraph.aws4.*), white bg, JP labels.
"""
import os

OUT_DIR = '/Users/aki/aws-sap/docs/diagrams/per-question'
os.makedirs(OUT_DIR, exist_ok=True)

# ---- Helpers ---------------------------------------------------------------

def _esc(s):
    if s is None:
        return ''
    s = str(s).replace('\\n', '\x01')
    s = (s.replace('&', '&amp;')
          .replace('<', '&lt;')
          .replace('>', '&gt;')
          .replace('"', '&quot;'))
    return s.replace('\x01', '&#xa;')

def aws_icon(cid, x, y, res, fill="#FF9900", w=50, h=50):
    return f'''        <mxCell id="{cid}" value="" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={fill};strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon={res};" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
        </mxCell>'''

def label(cid, x, y, w, h, text, fs=10, bold=False, color="#232F3E", align="center"):
    fs_style = 1 if bold else 0
    return f'''        <mxCell id="{cid}" value="{_esc(text)}" style="text;html=1;align={align};verticalAlign=middle;whiteSpace=wrap;fontSize={fs};fontStyle={fs_style};fontColor={color};" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
        </mxCell>'''

def box(cid, x, y, w, h, title, fill="#FFFFFF", stroke="#3B48CC", fs=12, sw=2):
    return f'''        <mxCell id="{cid}" value="{_esc(title)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth={sw};fontSize={fs};fontStyle=1;fontColor=#232F3E;verticalAlign=top;spacingTop=6;" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
        </mxCell>'''

def arrow(cid, src, tgt, color="#3B48CC", w=2, extra="", text=""):
    lbl = f' value="{_esc(text)}"' if text else ' value=""'
    return f'''        <mxCell id="{cid}"{lbl} style="endArrow=classic;html=1;strokeColor={color};strokeWidth={w};fontSize=10;fontColor={color};{extra}" edge="1" parent="1" source="{src}" target="{tgt}">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>'''

def arrow_pts(cid, x1, y1, x2, y2, color="#3B48CC", w=2, text=""):
    lbl = f' value="{_esc(text)}"' if text else ' value=""'
    return f'''        <mxCell id="{cid}"{lbl} style="endArrow=classic;html=1;strokeColor={color};strokeWidth={w};fontSize=10;fontColor={color};" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{x1}" y="{y1}" as="sourcePoint" />
            <mxPoint x="{x2}" y="{y2}" as="targetPoint" />
          </mxGeometry>
        </mxCell>'''

def title_cell(text, w=1000, fs=18):
    return f'''        <mxCell id="title" value="{_esc(text)}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize={fs};fontStyle=1;fontColor=#232F3E;" vertex="1" parent="1">
          <mxGeometry x="0" y="10" width="{w}" height="30" as="geometry" />
        </mxCell>'''

def wrap_mx(body, w=1000, h=600, name="d"):
    return f'''<mxfile host="app.diagrams.net" modified="2026-04-20T00:00:00.000Z" agent="Claude" version="24.0.0">
  <diagram id="d1" name="{name}">
    <mxGraphModel dx="1422" dy="757" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{w}" pageHeight="{h}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

{body}

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

def write_diag(qid, body, w=1000, h=600):
    path = os.path.join(OUT_DIR, f'{qid}.drawio')
    if os.path.exists(path):
        print(f'SKIP (exists): {path}')
        return
    with open(path, 'w', encoding='utf-8') as f:
        f.write(wrap_mx(body, w, h, qid))
    print(f'wrote {path}')

# AWS colors
C_ORANGE = "#FF9900"
C_BLUE   = "#3B48CC"
C_GREEN  = "#7AA116"
C_RED    = "#DD344C"
C_PURPLE = "#8C4FFF"
C_PINK   = "#E7157B"
C_DARK   = "#232F3E"

# Common icon shorthands
I_ORG  = 'mxgraph.aws4.organizations'
I_CT   = 'mxgraph.aws4.control_tower'
I_SSO  = 'mxgraph.aws4.single_sign_on'
I_IAM  = 'mxgraph.aws4.identity_and_access_management'
I_STS  = 'mxgraph.aws4.sts'
I_RAM  = 'mxgraph.aws4.resource_access_manager'
I_S3   = 'mxgraph.aws4.s3'
I_KMS  = 'mxgraph.aws4.key_management_service'
I_CFG  = 'mxgraph.aws4.config'
I_CTR  = 'mxgraph.aws4.cloudtrail'
I_EC2  = 'mxgraph.aws4.ec2'
I_VPC  = 'mxgraph.aws4.vpc'
I_TGW  = 'mxgraph.aws4.transit_gateway'
I_LAMB = 'mxgraph.aws4.lambda'
I_RDS  = 'mxgraph.aws4.rds'
I_DDB  = 'mxgraph.aws4.dynamodb'

# ==========================================================================
# SAP-33 CloudFormation StackSets + Organizations (全アカウント + 新規自動)
# ==========================================================================
def diag_sap_33():
    body = [title_cell("SAP-33: StackSets + Organizations 信頼アクセス (全アカウント + 新規自動展開)")]
    body.append(box('mgmt', 30, 60, 360, 480, 'Management Account (管理アカウント)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 70, 100, I_ORG, fill=C_RED))
    body.append(label('org_l', 50, 158, 110, 20, 'AWS Organizations', bold=True))
    body.append(aws_icon('cfn', 240, 100, 'mxgraph.aws4.cloudformation', fill=C_PURPLE))
    body.append(label('cfn_l', 200, 158, 160, 20, 'CloudFormation StackSets', bold=True))
    body.append(label('cfn_d', 50, 195, 320, 120, '信頼アクセス (Service-managed):\\n・配置先: すべての OU / 全アカウント\\n・自動配置 (auto-deployment) ON\\n  → 新規アカウント作成時に自動適用\\n・管理アカウントに1テンプレ\\n  登録のみで全体へ展開', fs=10, align="left"))
    body.append(label('cfn_s', 50, 330, 320, 90, 'テンプレ例:\\n・CloudTrail を外部S3 (別アカウント) へ\\n・Config ルール\\n・IAM ロール (監査用)\\n・GuardDuty 有効化', fs=10, align="left", color=C_BLUE))
    body.append(label('cfn_note', 50, 430, 320, 90, '× Lambda + CLI 自動化は再発明で運用コスト大\\n× 各アカウント手動実行は漏れる\\n× CloudFormation 単体は単一アカウント向け', fs=10, align="left", color=C_RED))

    # Member accounts
    body.append(box('mems', 430, 60, 540, 480, 'メンバーアカウント群 (OU 配下 + 将来追加)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    positions = [(470,110),(600,110),(730,110),(860,110),(470,230),(600,230),(730,230),(860,230)]
    for i,(x,y) in enumerate(positions):
        body.append(aws_icon(f'a{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))
        body.append(label(f'al{i}', x-10, y+42, 60, 18, f'Acct {i+1}', fs=9))
    # New account
    body.append(aws_icon('new', 700, 360, I_ORG, fill=C_ORANGE, w=50, h=50))
    body.append(label('new_l', 640, 418, 180, 20, '新規アカウント (自動適用)', bold=True, fs=10, color=C_ORANGE))
    body.append(label('mem_note', 450, 460, 500, 60, '・StackSets がテンプレを一括デプロイ\\n・新規アカウントも OU に入れるだけで即時プロビジョニング\\n・ドリフト検知も一元化', fs=10, align="left"))

    body.append(arrow_pts('ar1', 290, 150, 470, 150, C_BLUE, 2, "① 一括展開"))
    body.append(arrow_pts('ar2', 290, 150, 700, 370, C_ORANGE, 2, "② 自動配置"))

    write_diag('SAP-33', '\n'.join(body), 1000, 580)

# ==========================================================================
# SAP-36 RAM AMI 共有 (ゴールデンAMI中央管理)
# ==========================================================================
def diag_sap_36():
    body = [title_cell("SAP-36: 共有サービスアカウントで Golden AMI → RAM で組織全アカウントへ共有")]
    body.append(box('shared', 30, 60, 320, 460, 'Shared Services Account', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('ec2b', 70, 110, I_EC2, fill=C_ORANGE))
    body.append(label('ec2b_l', 45, 165, 110, 20, 'ベース AMI ビルド', bold=True))
    body.append(aws_icon('img', 200, 110, 'mxgraph.aws4.ec2_ami', fill=C_ORANGE))
    body.append(label('img_l', 170, 165, 110, 20, 'Golden AMI', bold=True))
    body.append(aws_icon('ram', 135, 230, I_RAM, fill=C_RED))
    body.append(label('ram_l', 90, 288, 200, 20, 'Resource Access Manager', bold=True))
    body.append(label('ram_d', 50, 320, 280, 180, '・AMI をリソース共有に追加\\n・Principal: AWS Organizations\\n  または 特定 OU\\n・組織内の全アカウントに自動共有\\n・Consumer 側は何もせず\\n  launch-permission を持つ\\n\\n(EC2 Image Builder で定期再ビルド+配布)', fs=10, align="left"))

    body.append(box('mems', 400, 60, 570, 460, 'メンバーアカウント (本番 / 検証 / 開発 …)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    ids = [(440,110),(600,110),(760,110),(440,240),(600,240),(760,240),(440,370),(600,370),(760,370)]
    for i,(x,y) in enumerate(ids):
        body.append(aws_icon(f'ma{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))
        body.append(label(f'mal{i}', x-15, y+42, 70, 18, f'Acct {i+1}', fs=9))

    body.append(arrow_pts('r1', 340, 260, 440, 130, C_GREEN, 2, "共有 AMI 使用"))
    body.append(arrow_pts('r2', 340, 280, 440, 260, C_GREEN, 2))

    body.append(box('note', 400, 450, 570, 65, '× AMI を全アカウントにコピー → コストと運用負荷 / × 個別Principalで指定 → 追加のたび更新', fill="#FFF0F0", stroke=C_RED, fs=10))
    write_diag('SAP-36', '\n'.join(body), 1000, 560)

# ==========================================================================
# SAP-49 VPC / サブネット共有 (RAM)
# ==========================================================================
def diag_sap_49():
    body = [title_cell("SAP-49: Network アカウントで VPC を所有、RAM でサブネットを各事業部へ共有")]
    body.append(box('netacc', 30, 60, 430, 480, 'Network アカウント (VPC オーナー)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('vpc', 90, 110, I_VPC, fill=C_PURPLE))
    body.append(label('vpc_l', 55, 165, 140, 20, 'VPC (10.0.0.0/16)', bold=True))
    body.append(box('sn1', 200, 90, 240, 60, 'Subnet A (10.0.1.0/24)', fill="#F0F8E8", stroke=C_GREEN, fs=10, sw=1))
    body.append(box('sn2', 200, 160, 240, 60, 'Subnet B (10.0.2.0/24)', fill="#F0F8E8", stroke=C_GREEN, fs=10, sw=1))
    body.append(box('sn3', 200, 230, 240, 60, 'Subnet C (10.0.3.0/24)', fill="#F0F8E8", stroke=C_GREEN, fs=10, sw=1))
    body.append(aws_icon('ram', 70, 310, I_RAM, fill=C_RED))
    body.append(label('ram_l', 30, 368, 180, 20, 'Resource Access Manager', bold=True))
    body.append(label('ram_d', 30, 395, 400, 130, 'サブネットをリソース共有\\n・Principal: 事業部アカウント (または OU)\\n・VPC/RouteTable/NACL/DNS は VPC オーナーが集中管理\\n・参加者は自アカウントで EC2/ENI/RDS/Lambda を起動するだけ\\n・ネットワーク設計のガバナンスを一元化', fs=10, align="left"))

    body.append(box('parts', 500, 60, 470, 480, '事業部アカウント (Participant)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    for i,(x,y,nm) in enumerate([(530,110,'事業部A'),(720,110,'事業部B'),(530,230,'事業部C'),(720,230,'事業部D')]):
        body.append(aws_icon(f'ec{i}', x, y, I_EC2, fill=C_ORANGE))
        body.append(label(f'ec{i}_l', x-20, y+58, 100, 20, f'{nm} EC2', bold=True, fs=10))

    body.append(label('parts_d', 520, 340, 440, 180, '・共有サブネット上で直接 EC2/RDS/Lambda ENI を起動\\n・各事業部は自アカウント課金で管理\\n・× 各事業部で VPC を作って VPC Peering → 管理爆発\\n・× TGW だけでは「同一サブネット」には入れない\\n・× クロスアカウント ENI attach は不可', fs=10, align="left"))
    write_diag('SAP-49', '\n'.join(body), 1000, 580)

# ==========================================================================
# SAP-60 CUR + Cost Allocation Tag + Athena (クロスアカウント チャージバック)
# ==========================================================================
def diag_sap_60():
    body = [title_cell("SAP-60: Organizations 統合請求 + Cost Allocation Tag + CUR → Athena で部門別集計")]
    body.append(box('mgmt', 30, 60, 360, 480, 'Management Account (統合請求)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 70, 100, I_ORG, fill=C_RED))
    body.append(label('org_l', 50, 158, 110, 20, 'AWS Organizations', bold=True))
    body.append(aws_icon('cur', 220, 100, 'mxgraph.aws4.cost_and_usage_report', fill=C_PINK))
    body.append(label('cur_l', 190, 158, 130, 20, 'Cost & Usage Report', bold=True))
    body.append(label('tag', 50, 200, 320, 80, '① Cost Allocation Tag を有効化\\n  ・ユーザ定義: CostCenter, Project, Env\\n  ・Organizations ルート全体で統一', fs=10, align="left"))
    body.append(aws_icon('s3', 70, 300, I_S3, fill=C_GREEN))
    body.append(label('s3_l', 40, 358, 120, 20, 'CUR → S3', bold=True))
    body.append(aws_icon('ath', 220, 300, 'mxgraph.aws4.athena', fill=C_PURPLE))
    body.append(label('ath_l', 195, 358, 100, 20, 'Athena クエリ', bold=True))
    body.append(label('flow', 50, 395, 320, 120, '② CUR が日次で詳細明細を S3 に出力\\n③ Athena で SQL: SUM(cost) GROUP BY tag\\n④ 結果を BI (QuickSight) へ連携\\n\\n・タグ未付与リソースは検出して是正\\n・"Cost Categories" で部門ビューを定義可', fs=10, align="left"))

    body.append(box('mems', 430, 60, 540, 480, 'メンバーアカウント (事業部 / サービス別)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    for i,(x,y,nm) in enumerate([(470,110,'事業部A'),(620,110,'事業部B'),(770,110,'事業部C'),(470,240,'運用基盤'),(620,240,'分析基盤'),(770,240,'ML基盤')]):
        body.append(aws_icon(f'a{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))
        body.append(label(f'al{i}', x-15, y+42, 70, 18, nm, fs=9, bold=True))
    body.append(label('mem_d', 450, 330, 510, 190, '各アカウントの全リソースにタグを付与:\\n  CostCenter=C001, Project=Alpha, Env=prod\\n↓\\nCUR にタグ列が出力され、\\nAthena で部門別 / プロジェクト別 / 環境別集計\\n\\n× 各アカウントで Cost Explorer を個別集計 → 手間大\\n× 手動でスプレッドシート集計 → ミス多発', fs=10, align="left"))

    write_diag('SAP-60', '\n'.join(body), 1000, 580)

# ==========================================================================
# SAP-63 IAM Identity Center + AD Connector (既存AD 少人数 / 最小コスト)
# ==========================================================================
def diag_sap_63():
    body = [title_cell("SAP-63: 既存 Microsoft AD + AD Connector + IAM Identity Center (最小コスト SSO)")]
    body.append(box('onprem', 30, 60, 280, 220, 'オンプレミス', fill="#F5F5F5", stroke=C_DARK, fs=11))
    body.append(label('ad', 60, 100, 220, 40, 'Microsoft Active Directory\\n(既存ユーザ / グループ)', bold=True, fs=11))
    body.append(label('ad_d', 60, 150, 220, 120, '・既存の ID ソースを継続利用\\n・ユーザ追加/無効化はオンプレ側\\n・MFA もオンプレで強制', fs=10, align="left"))

    body.append(aws_icon('adc', 350, 140, I_IAM, fill=C_RED))
    body.append(label('adc_l', 320, 198, 120, 20, 'AD Connector', bold=True))
    body.append(label('adc_d', 310, 225, 140, 40, '(Managed AD の\\n プロキシ役)', fs=9))

    body.append(box('mgmt', 480, 60, 240, 220, 'Management Account', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('ic', 570, 100, I_SSO, fill=C_RED))
    body.append(label('ic_l', 530, 158, 140, 20, 'IAM Identity Center', bold=True))
    body.append(label('ic_d', 495, 190, 220, 80, '・権限セット割当\\n・SAML 2.0 で各アカウントへ一時クレデンシャル\\n・AWSコンソール/CLI から SSO', fs=9, align="left"))

    body.append(box('accs', 750, 60, 220, 490, 'メンバーアカウント', fill="#F0F8E8", stroke=C_GREEN, fs=11))
    for i, y in enumerate([110, 200, 290, 380, 470]):
        body.append(aws_icon(f'a{i}', 840, y, I_ORG, fill=C_RED, w=40, h=40))
        body.append(label(f'al{i}', 790, y+42, 140, 18, f'アカウント {i+1}', fs=9, bold=True))

    body.append(arrow_pts('r1', 310, 165, 350, 165, C_BLUE))
    body.append(arrow_pts('r2', 400, 165, 570, 125, C_BLUE))
    body.append(arrow_pts('r3', 620, 150, 840, 290, C_GREEN, 2, "SAML"))

    body.append(box('cmp', 30, 300, 680, 250, '✓ なぜこの構成が最小コストか', fill="#FFF9E6", stroke=C_ORANGE, fs=12))
    body.append(label('cmp_d', 50, 340, 640, 200,
        '・AD Connector は Managed AD (数万円/月) より安価 = 既存 AD の窓口に徹する\\n'
        '・IAM Identity Center 本体は無料 (使用量に応じたメトリクスもなし)\\n'
        '・ユーザ ID は AD 側で一元 → IAM ユーザを各アカウントに作らない\\n\\n'
        '× 各アカウントに IAM ユーザ: 長期クレデンシャル + ID 分散で NG\\n'
        '× ADFS 自前構築: SAML IdP を運用する手間 / 冗長化コスト\\n'
        '× Cognito User Pool: B2E の社内ユーザ ID 統合には不向き (B2C 用)',
        fs=10, align="left"))
    write_diag('SAP-63', '\n'.join(body), 1000, 570)

# ==========================================================================
# SAP-72 SCP の管理アカウント例外
# ==========================================================================
def diag_sap_72():
    body = [title_cell("SAP-72: SCP は管理アカウントには適用されない — 重要な例外")]
    # 上段: 管理アカウント
    body.append(box('mgmt', 30, 60, 940, 150, 'Management Account (管理アカウント)', fill="#FFF9E6", stroke=C_ORANGE, fs=12))
    body.append(aws_icon('org', 80, 100, I_ORG, fill=C_RED))
    body.append(label('org_l', 60, 158, 100, 20, 'Organizations', bold=True))
    body.append(aws_icon('scp', 260, 100, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
    body.append(label('scp_l', 220, 158, 180, 20, 'SCP (組織ルートに添付)', bold=True))
    body.append(label('mgmt_note', 430, 90, 530, 110, '⚠️ SCP は「管理アカウント」には適用されない\\n  ・管理アカウントはルート権限のまま\\n  ・誤って全API禁止を管理アカウントに設定しても影響なし\\n  ・本番ワークロードは管理アカウントに置かないのが原則', fs=11, bold=True, color=C_RED, align="left"))

    # 下段: OU と member
    body.append(box('ou_root', 30, 230, 940, 250, 'Root OU', fill="#EBF1FF", stroke=C_BLUE, fs=12))
    body.append(box('ou1', 60, 270, 280, 190, 'Production OU (SCP 適用)', fill="#F0F8E8", stroke=C_GREEN, fs=11))
    for i, x in enumerate([80, 180, 80, 180]):
        y = 310 if i < 2 else 390
        body.append(aws_icon(f'p{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))
    body.append(box('ou2', 360, 270, 280, 190, 'Dev OU (SCP 適用)', fill="#F0F8E8", stroke=C_GREEN, fs=11))
    for i, x in enumerate([380, 480, 380, 480]):
        y = 310 if i < 2 else 390
        body.append(aws_icon(f'd{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))
    body.append(box('ou3', 660, 270, 280, 190, 'Sandbox OU (SCP 適用)', fill="#F0F8E8", stroke=C_GREEN, fs=11))
    for i, x in enumerate([680, 780, 680, 780]):
        y = 310 if i < 2 else 390
        body.append(aws_icon(f's{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))

    body.append(box('key', 30, 500, 940, 75, '覚え方: SCP は "管理アカウント以外" に効く。管理アカウントを要塞化するならIAMポリシー/MFA/CloudTrailで統制', fill="#FFF0F0", stroke=C_RED, fs=11))
    write_diag('SAP-72', '\n'.join(body), 1000, 600)

# ==========================================================================
# SAP-75 クロスアカウント Secrets Manager (Lambda が別アカウントのシークレットを取得)
# ==========================================================================
def diag_sap_75():
    body = [title_cell("SAP-75: クロスアカウント Secrets Manager — Lambda が本番アカウントのシークレットを取得")]
    # Dev/Lambda
    body.append(box('dev', 30, 60, 360, 480, '開発アカウント (Lambda 実行側)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('lam', 130, 110, I_LAMB, fill=C_ORANGE))
    body.append(label('lam_l', 95, 168, 120, 20, 'Lambda 関数', bold=True))
    body.append(aws_icon('role', 270, 110, I_IAM, fill=C_RED))
    body.append(label('role_l', 240, 168, 100, 20, '実行ロール', bold=True))
    body.append(label('role_p', 50, 210, 330, 100, '実行ロール IAM ポリシー:\\n  Action:\\n    secretsmanager:GetSecretValue\\n    kms:Decrypt\\n  Resource:\\n    arn:aws:secretsmanager:REGION:PROD-ACCT:secret:DBCreds-*', fs=9, align="left"))
    body.append(aws_icon('sts', 200, 350, I_STS, fill=C_RED))
    body.append(label('sts_l', 165, 405, 110, 20, 'STS で一時クレデンシャル', bold=True, fs=9))
    body.append(label('dev_note', 50, 430, 330, 100, '・長期クレデンシャルを Lambda に置かない\\n・本番シークレット本体は本番アカウントで保持\\n・KMS キーポリシーで開発アカウントの Lambda ロールに Decrypt を許可', fs=10, align="left", color=C_BLUE))

    # Prod / Secrets Manager
    body.append(box('prod', 430, 60, 540, 480, '本番アカウント (シークレット所有)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    body.append(aws_icon('sec', 500, 110, 'mxgraph.aws4.secrets_manager', fill=C_RED))
    body.append(label('sec_l', 460, 168, 140, 20, 'Secrets Manager', bold=True))
    body.append(label('sec_p', 450, 200, 170, 80, 'リソースポリシー:\\n  Principal:\\n    arn:aws:iam::DEV:role/LambdaRole\\n  Action: GetSecretValue', fs=9, align="left"))

    body.append(aws_icon('kms', 750, 110, I_KMS, fill=C_RED))
    body.append(label('kms_l', 720, 168, 100, 20, 'KMS CMK', bold=True))
    body.append(label('kms_p', 640, 200, 310, 120, 'キーポリシー:\\n  Principal:\\n    arn:aws:iam::DEV:role/LambdaRole\\n  Action: kms:Decrypt\\n\\n※ カスタマー管理キー (CMK) でないと\\n  クロスアカウント暗号化データは復号不可', fs=9, align="left"))

    body.append(aws_icon('rds', 580, 360, I_RDS, fill=C_PURPLE))
    body.append(label('rds_l', 540, 418, 140, 20, 'RDS (本番DB)', bold=True))

    body.append(arrow_pts('r1', 330, 135, 500, 135, C_BLUE, 2, "① GetSecretValue"))
    body.append(arrow_pts('r2', 550, 160, 750, 135, C_PURPLE, 2, "② Decrypt"))
    body.append(arrow_pts('r3', 525, 155, 600, 360, C_GREEN, 2, "③ DB接続"))

    body.append(box('note', 450, 440, 510, 90, '× シークレット本体を開発にコピー → 機密が拡散\\n× 環境変数にパスワード直書き → アンチパターン\\n× IAM ユーザの長期キー共有 → 漏洩リスク', fill="#FFF0F0", stroke=C_RED, fs=10))
    write_diag('SAP-75', '\n'.join(body), 1000, 580)

# ==========================================================================
# SAP-78 Multi-account TGW + Route 53 Resolver (オンプレDNS解決)
# ==========================================================================
def diag_sap_78():
    body = [title_cell("SAP-78: 複数アカウント VPC → 共有 TGW → R53 Resolver Outbound Endpoint → オンプレ DNS")]
    body.append(box('nacc', 30, 60, 340, 480, 'Network (共有サービス) アカウント', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('tgw', 80, 120, I_TGW, fill=C_PURPLE))
    body.append(label('tgw_l', 50, 178, 120, 20, 'Transit Gateway', bold=True))
    body.append(aws_icon('rvpc', 220, 120, I_VPC, fill=C_PURPLE))
    body.append(label('rvpc_l', 190, 178, 110, 20, 'Resolver VPC', bold=True))
    body.append(aws_icon('out', 220, 230, 'mxgraph.aws4.route_53', fill=C_PURPLE))
    body.append(label('out_l', 170, 288, 200, 20, 'R53 Outbound Endpoint', bold=True, fs=10))
    body.append(label('out_d', 50, 320, 300, 120, 'Resolver Rule:\\n  domain: corp.example.com\\n  → forward to オンプレ DNS\\n  (10.0.0.53, 10.0.0.54)\\n\\nRAM で各アカウントに Rule を共有', fs=10, align="left"))
    body.append(aws_icon('ram', 80, 350, I_RAM, fill=C_RED))
    body.append(label('ram_l', 45, 408, 130, 20, 'Resource Access Manager', bold=True, fs=9))

    body.append(box('accs', 400, 60, 280, 480, 'アプリアカウント × N', fill="#F0F8E8", stroke=C_GREEN, fs=11))
    for i, y in enumerate([110, 260, 410]):
        body.append(aws_icon(f'vpc{i}', 440, y, I_VPC, fill=C_PURPLE, w=40, h=40))
        body.append(label(f'vpc{i}_l', 420, y+42, 80, 18, f'VPC {i+1}', bold=True, fs=9))
        body.append(aws_icon(f'ec{i}', 540, y, I_EC2, fill=C_ORANGE, w=40, h=40))
        body.append(label(f'ec{i}_l', 520, y+42, 80, 18, f'EC2 {i+1}', fs=9))

    body.append(box('on', 710, 60, 260, 480, 'オンプレミス DC', fill="#F5F5F5", stroke=C_DARK, fs=11))
    body.append(label('dns', 750, 150, 180, 50, 'オンプレ DNS\\n(権威: corp.example.com)', bold=True, fs=11))
    body.append(label('dx', 740, 220, 210, 60, 'Direct Connect / VPN\\n経由で TGW と接続', fs=10))
    body.append(label('on_note', 740, 300, 210, 180, '・EC2 → VPC Resolver (.2)\\n→ Resolver Rule にマッチ\\n→ Outbound EP\\n→ TGW\\n→ DX\\n→ オンプレ DNS\\n→ 権威応答', fs=10, align="left"))

    body.append(arrow_pts('a1', 580, 130, 220, 155, C_GREEN, 2))
    body.append(arrow_pts('a2', 260, 255, 260, 300, C_PURPLE, 2))
    body.append(arrow_pts('a3', 130, 145, 90, 400, C_RED, 2))
    body.append(arrow_pts('a4', 260, 260, 710, 170, C_ORANGE, 2, "DNS 転送"))

    body.append(box('pt', 30, 550, 940, 40, '× Conditional Forwarder を各VPCに個別設定 → スケーラブルでない  /  × VPC Peering メッシュ → 管理爆発', fill="#FFF0F0", stroke=C_RED, fs=10))
    write_diag('SAP-78', '\n'.join(body), 1000, 600)

# ==========================================================================
# SAP-81 サンドボックスアカウント SCP + Budgets (支出統制)
# ==========================================================================
def diag_sap_81():
    body = [title_cell("SAP-81: Sandbox OU に SCP + AWS Budgets で支出上限を組織全体にスケーラブルに適用")]
    body.append(box('mgmt', 30, 60, 360, 480, 'Management Account', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 70, 100, I_ORG, fill=C_RED))
    body.append(label('org_l', 50, 158, 110, 20, 'Organizations', bold=True))
    body.append(aws_icon('scp', 220, 100, I_IAM, fill=C_RED))
    body.append(label('scp_l', 190, 158, 130, 20, 'SCP (Sandbox OU)', bold=True))
    body.append(label('scp_d', 50, 200, 320, 120, 'Deny:\\n  ec2:RunInstances で\\n   instance type > m5.large を禁止\\n  高額 GPU インスタンス禁止\\n  RDS 大型クラス禁止\\n  (安価インスタンスのみ許可)', fs=9, align="left", color=C_RED))

    body.append(aws_icon('bud', 70, 340, 'mxgraph.aws4.budgets', fill=C_PINK))
    body.append(label('bud_l', 50, 398, 110, 20, 'AWS Budgets', bold=True))
    body.append(aws_icon('sns', 220, 340, 'mxgraph.aws4.simple_notification_service', fill=C_RED))
    body.append(label('sns_l', 195, 398, 110, 20, 'SNS / ChatOps', bold=True))
    body.append(label('bud_d', 50, 430, 320, 100, 'Budgets Action:\\n  閾値超過時に IAM Deny ポリシーを\\n  自動アタッチ → 新規リソース作成停止\\n  ・アカウントごとに予算上限を設定', fs=10, align="left"))

    body.append(box('sb', 430, 60, 540, 220, 'Sandbox OU (開発者セルフサービスで払い出し)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    for i,(x,y) in enumerate([(460,110),(560,110),(660,110),(760,110),(860,110),(460,210),(560,210),(660,210),(760,210),(860,210)]):
        body.append(aws_icon(f'sa{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))
        body.append(label(f'sal{i}', x-10, y+42, 60, 18, f'Dev{i+1}', fs=9))

    body.append(box('other', 430, 300, 540, 240, '他 OU (本番 / 検証)', fill="#FFF9E6", stroke=C_ORANGE, fs=12))
    body.append(label('other_d', 450, 340, 510, 200,
        'SCP は Sandbox OU のみに適用。\\n本番 OU は別 SCP (広めの許可) を利用。\\n\\n重要ポイント:\\n・SCP + Budgets Actions + Service Catalog の 3 点セットが正攻法\\n・× 手動で毎月チェック → 人手で破綻\\n・× EC2 単体の Instance Type 制限は IAM では制御しにくい\\n  (SCP の Condition: ec2:InstanceType が強力)', fs=10, align="left"))
    write_diag('SAP-81', '\n'.join(body), 1000, 580)

# ==========================================================================
# SAP-94 Organization Trail + CloudTrail S3 Data Events
# ==========================================================================
def diag_sap_94():
    body = [title_cell("SAP-94: Organization Trail + S3 Data Events で組織横断のオブジェクトアクセスを自動記録")]
    body.append(box('mgmt', 30, 60, 360, 470, 'Management Account (Trail オーナー)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 70, 100, I_ORG, fill=C_RED))
    body.append(label('org_l', 50, 158, 110, 20, 'Organizations', bold=True))
    body.append(aws_icon('ctr', 220, 100, I_CTR, fill=C_GREEN))
    body.append(label('ctr_l', 185, 158, 150, 20, 'Organization Trail', bold=True))
    body.append(label('ctr_d', 50, 200, 330, 150, '・IsMultiRegionTrail: true\\n・IsOrganizationTrail: true\\n・DataResources:\\n    type: AWS::S3::Object\\n    values: ["arn:aws:s3"]\\n  → 全アカウントの全 S3 バケット\\n    のオブジェクトレベル操作を記録', fs=10, align="left"))
    body.append(aws_icon('log', 180, 370, I_S3, fill=C_PURPLE))
    body.append(label('log_l', 120, 428, 220, 20, 'ログ集約 S3 (別アカウント推奨)', bold=True, fs=10))

    body.append(box('mems', 430, 60, 540, 470, 'メンバーアカウント群 (S3 バケット保有)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    for i,(x,y) in enumerate([(460,110),(620,110),(780,110),(460,240),(620,240),(780,240),(460,370),(620,370),(780,370)]):
        body.append(aws_icon(f's{i}', x, y, I_S3, fill=C_GREEN, w=40, h=40))
        body.append(label(f'sl{i}', x-15, y+42, 70, 18, f'Bucket {i+1}', fs=9))

    body.append(arrow_pts('a1', 390, 135, 460, 130, C_ORANGE, 2, "GetObject/PutObject を記録"))
    body.append(arrow_pts('a2', 205, 350, 205, 370, C_PURPLE, 2))

    body.append(box('note', 30, 545, 940, 40, '新規アカウント追加時も自動対象。× 各アカウント個別Trailだと設定漏れ / × ManagementEventsのみだとオブジェクト操作は記録されない', fill="#FFF0F0", stroke=C_RED, fs=10))
    write_diag('SAP-94', '\n'.join(body), 1000, 600)

# ==========================================================================
# SAP-97 外部パートナー STS AssumeRole + External ID
# ==========================================================================
def diag_sap_97():
    body = [title_cell("SAP-97: 外部パートナー → Customer アカウントへの AssumeRole + External ID (混乱した代理人対策)")]
    body.append(box('partner', 30, 60, 320, 480, 'パートナー Organization (org1)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('pu', 130, 110, I_IAM, fill=C_RED))
    body.append(label('pu_l', 90, 168, 140, 20, 'パートナー IAM ロール', bold=True))
    body.append(label('pu_p', 50, 200, 280, 120, '実行プリンシパル:\\n  ec2:i-xxx (監視サービス)\\nIAM ポリシー:\\n  Action: sts:AssumeRole\\n  Resource:\\n    arn:aws:iam::CUST:role/ReadOnly', fs=9, align="left"))
    body.append(aws_icon('sts', 130, 360, I_STS, fill=C_RED))
    body.append(label('sts_l', 100, 418, 110, 20, 'STS AssumeRole', bold=True))
    body.append(label('sts_d', 50, 445, 280, 80, '+ ExternalId (顧客固有文字列)\\n+ RoleSessionName (監査用)\\n+ DurationSeconds 3600 以下', fs=10, align="left"))

    body.append(aws_icon('stsr', 480, 250, I_STS, fill=C_RED))

    body.append(box('cust', 650, 60, 320, 480, '顧客 Organization (org2)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    body.append(aws_icon('role', 740, 110, I_IAM, fill=C_RED))
    body.append(label('role_l', 715, 168, 120, 20, 'ReadOnly Role', bold=True))
    body.append(label('trust', 670, 200, 280, 160, '信頼ポリシー:\\n  Principal:\\n    arn:aws:iam::PARTNER:root\\n  Condition:\\n    StringEquals:\\n      sts:ExternalId: "CUST-12345"\\n\\n許可ポリシー:\\n  CloudWatch/EC2 ReadOnly', fs=9, align="left"))
    for i,(x,y) in enumerate([(680,370),(780,370),(880,370),(680,450),(780,450),(880,450)]):
        body.append(aws_icon(f'a{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))

    body.append(arrow('r1', 'pu', 'sts', C_BLUE))
    body.append(arrow_pts('r2', 180, 395, 480, 275, C_ORANGE, 2, "+ ExternalId"))
    body.append(arrow_pts('r3', 530, 275, 740, 140, C_GREEN, 2, "一時クレデンシャル"))

    body.append(box('note', 30, 550, 940, 40, 'External ID はパートナーが顧客ごとに共有; 第三者が誤って同パートナーロールを引けなくする (混乱した代理人攻撃対策)', fill="#FFF9E6", stroke=C_ORANGE, fs=10))
    write_diag('SAP-97', '\n'.join(body), 1000, 610)

# ==========================================================================
# SAP-101 クロスアカウント KMS + S3 (3箇所の許可)
# ==========================================================================
def diag_sap_101():
    body = [title_cell("SAP-101: クロスアカウント S3 + KMS — 3 箇所のポリシーを揃える必要")]
    body.append(box('prod', 30, 60, 420, 480, '制作アカウント (オブジェクト所有 + KMS)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('s3', 90, 110, I_S3, fill=C_GREEN))
    body.append(label('s3_l', 50, 168, 130, 20, 'S3 バケット', bold=True))
    body.append(label('s3_p', 50, 200, 180, 130, '① バケットポリシー\\n  Principal:\\n    arn:aws:iam::OPS:role/X\\n  Action:\\n    s3:GetObject\\n  Resource: bucket/*', fs=9, align="left", color=C_GREEN))
    body.append(aws_icon('kms', 280, 110, I_KMS, fill=C_RED))
    body.append(label('kms_l', 245, 168, 120, 20, 'KMS CMK', bold=True))
    body.append(label('kms_p', 240, 200, 190, 130, '② KMS キーポリシー\\n  Principal:\\n    arn:aws:iam::OPS:role/X\\n  Action:\\n    kms:Decrypt\\n    kms:GenerateDataKey', fs=9, align="left", color=C_RED))
    body.append(label('prod_note', 50, 350, 390, 170, '・オブジェクトは SSE-KMS で暗号化\\n・カスタマー管理 KMS (CMK) 必須\\n  (AWS 管理キーは別アカウントに共有不可)\\n・バケットポリシーで Get 許可だけでは\\n  復号できない → KMS 側も必要', fs=10, align="left"))

    body.append(box('ops', 490, 60, 480, 480, '運用アカウント (Lambda 読み取り側)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    body.append(aws_icon('lam', 550, 110, I_LAMB, fill=C_ORANGE))
    body.append(label('lam_l', 510, 168, 130, 20, 'Lambda 関数', bold=True))
    body.append(aws_icon('role', 720, 110, I_IAM, fill=C_RED))
    body.append(label('role_l', 690, 168, 100, 20, '実行ロール', bold=True))
    body.append(label('role_p', 510, 200, 440, 150, '③ 実行ロールの IAM ポリシー\\n  Action:\\n    s3:GetObject\\n    kms:Decrypt\\n  Resource:\\n    arn:aws:s3:::PROD-bucket/*\\n    arn:aws:kms:REGION:PROD:key/ID', fs=9, align="left"))

    body.append(label('ops_note', 510, 360, 440, 160, '3 点セットが揃って初めて読み取り可能:\\n  ① バケットポリシー (PROD 側)\\n  ② KMS キーポリシー (PROD 側)\\n  ③ IAM ロールポリシー (OPS 側)\\n\\n× どれか1つでも欠けると AccessDenied', fs=10, align="left", color=C_RED))

    body.append(arrow_pts('a1', 670, 140, 340, 140, C_PURPLE, 2, "Decrypt"))
    body.append(arrow_pts('a2', 670, 160, 160, 160, C_PURPLE, 2, "GetObject"))
    write_diag('SAP-101', '\n'.join(body), 1000, 580)

# ==========================================================================
# SAP-103 Cost Explorer + OU 単位コスト可視化
# ==========================================================================
def diag_sap_103():
    body = [title_cell("SAP-103: AWS Cost Explorer で OU 単位のコスト分析 (ネイティブ機能)")]
    body.append(box('mgmt', 30, 60, 420, 480, 'Management Account (支払者)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 70, 100, I_ORG, fill=C_RED))
    body.append(label('org_l', 50, 158, 110, 20, 'Organizations', bold=True))
    body.append(aws_icon('ce', 220, 100, 'mxgraph.aws4.cost_explorer', fill=C_PINK))
    body.append(label('ce_l', 190, 158, 130, 20, 'Cost Explorer', bold=True))
    body.append(label('ce_d', 50, 200, 390, 310, 'グループ化: "Organizational unit"\\n  ・OU 単位でフィルタ / グループ化\\n  ・連結アカウントの全コストを集計\\n\\nCost Categories:\\n  ・独自ビジネス分類 (事業部 × 環境)\\n  ・SCP / OU を跨ぐ論理集計\\n\\n× 各アカウントで個別 Cost Explorer\\n  → 横断比較ができない\\n× CUR だけでは即時の可視化に向かず\\n  (Athena やダッシュボード整備が必要)\\n× サードパーティ導入は運用/コスト大', fs=10, align="left"))

    body.append(box('ous', 490, 60, 480, 480, 'OU 階層', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    body.append(box('ou_eng', 510, 110, 440, 130, 'Engineering OU', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    for i,(x,y,nm) in enumerate([(530,155,'Web'),(650,155,'API'),(770,155,'ML'),(870,155,'Data')]):
        body.append(aws_icon(f'e{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))
        body.append(label(f'el{i}', x-15, y+42, 70, 18, nm, fs=9))
    body.append(box('ou_biz', 510, 250, 440, 130, 'Business OU', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    for i,(x,y,nm) in enumerate([(530,295,'営業'),(650,295,'財務'),(770,295,'HR'),(870,295,'法務')]):
        body.append(aws_icon(f'b{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))
        body.append(label(f'bl{i}', x-15, y+42, 70, 18, nm, fs=9))
    body.append(box('ou_inf', 510, 390, 440, 120, 'Infrastructure OU', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    for i,(x,y,nm) in enumerate([(530,430,'Network'),(690,430,'Security'),(850,430,'Log')]):
        body.append(aws_icon(f'i{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))
        body.append(label(f'il{i}', x-20, y+42, 80, 18, nm, fs=9))
    write_diag('SAP-103', '\n'.join(body), 1000, 580)

# ==========================================================================
# SAP-111 AWS Managed Microsoft AD + IAM Identity Center (3000名 Organizations)
# ==========================================================================
def diag_sap_111():
    body = [title_cell("SAP-111: AWS Managed Microsoft AD + Trust + IAM Identity Center (既存 AD 3,000 名)")]
    body.append(box('onprem', 30, 60, 280, 220, 'オンプレミス', fill="#F5F5F5", stroke=C_DARK, fs=11))
    body.append(label('ad', 60, 100, 220, 40, '既存 Microsoft AD\\n(3,000 ユーザ)', bold=True, fs=11))
    body.append(label('ad_d', 60, 150, 220, 120, '・フォレスト/ドメイン既存\\n・双方向/単方向 Trust 可能\\n・MFA もオンプレ強制', fs=10, align="left"))

    body.append(aws_icon('mad', 340, 140, I_IAM, fill=C_RED))
    body.append(label('mad_l', 290, 198, 180, 20, 'AWS Managed Microsoft AD', bold=True, fs=10))
    body.append(label('mad_d', 290, 220, 180, 50, '・フォレスト Trust\\n  でオンプレと連携', fs=9))

    body.append(box('mgmt', 490, 60, 250, 220, 'Management Account', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('ic', 580, 100, I_SSO, fill=C_RED))
    body.append(label('ic_l', 540, 158, 140, 20, 'IAM Identity Center', bold=True))
    body.append(label('ic_d', 500, 195, 230, 80, '・ID ソース: Managed AD\\n・権限セットを OU/アカウント\\n  に割当\\n・SAML で一時クレデンシャル', fs=9, align="left"))

    body.append(box('accs', 770, 60, 200, 490, 'メンバーアカウント', fill="#F0F8E8", stroke=C_GREEN, fs=11))
    for i, y in enumerate([110, 200, 290, 380, 470]):
        body.append(aws_icon(f'a{i}', 850, y, I_ORG, fill=C_RED, w=40, h=40))
        body.append(label(f'al{i}', 800, y+42, 140, 18, f'アカウント {i+1}', fs=9, bold=True))

    body.append(arrow_pts('r1', 310, 160, 340, 160, C_BLUE, 2, "Trust"))
    body.append(arrow_pts('r2', 390, 165, 580, 125, C_BLUE, 2))
    body.append(arrow_pts('r3', 630, 150, 850, 290, C_GREEN, 2, "SAML"))

    body.append(box('cmp', 30, 310, 730, 280, '比較: なぜ Managed AD + Identity Center か', fill="#FFF9E6", stroke=C_ORANGE, fs=12))
    body.append(label('cmp_d', 50, 350, 690, 230,
        '✓ Managed MAD: Kerberos/LDAP が必要な Windows ワークロード (RDS SQL Server, FSx) も統合\\n'
        '✓ 3,000 ユーザ規模ではフォレスト Trust が最も柔軟\\n'
        '✓ IAM Identity Center は Organizations 全体の権限一元管理の標準\\n\\n'
        '× AD Connector だけ: Windows 統合認証が必要ならフル MAD が良い / 最大接続数に注意\\n'
        '× IAM Federation を各アカウントに個別構築: 3000名 × Nアカウントで破綻\\n'
        '× Cognito User Pool: 社内 B2E 認証には不向き', fs=10, align="left"))
    write_diag('SAP-111', '\n'.join(body), 1000, 610)

# ==========================================================================
# SAP-126 S3 Requester Pays + クロスアカウント
# ==========================================================================
def diag_sap_126():
    body = [title_cell("SAP-126: S3 Requester Pays — データ取得コストをアクセス側に負担させる")]
    body.append(box('owner', 30, 60, 400, 480, '研究所 A (データオーナー)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('s3', 100, 110, I_S3, fill=C_GREEN))
    body.append(label('s3_l', 60, 168, 160, 20, 'S3 バケット (2PB)', bold=True))
    body.append(label('s3_p', 60, 200, 340, 120, 'Requester Pays を ON:\\n  GET/HEAD のデータ転送/APIコストは\\n  リクエスタ側の請求になる\\n\\nバケットポリシー:\\n  Principal: 各大学/病院アカウント', fs=10, align="left"))
    body.append(aws_icon('iam', 300, 110, I_IAM, fill=C_RED))
    body.append(label('iam_l', 270, 168, 100, 20, 'IAM Policy', bold=True))
    body.append(label('own_note', 60, 340, 360, 180, '・大量データの保管コストは所有者負担\\n・取得側は RequestPayer: requester\\n  を付けて取得 → 請求はリクエスタへ\\n\\n× 全コストを所有者負担 → 共同研究で不公平\\n× 各大学にバケットコピー → 2PB 重複で非現実', fs=10, align="left"))

    body.append(box('reqs', 470, 60, 500, 480, 'リクエスタ (大学 / 病院) アカウント', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    for i,(x,y,nm) in enumerate([(520,110,'大学A'),(720,110,'大学B'),(870,110,'大学C'),(520,260,'病院X'),(720,260,'病院Y'),(870,260,'病院Z')]):
        body.append(aws_icon(f'r{i}', x, y, I_ORG, fill=C_RED))
        body.append(label(f'rl{i}', x-20, y+58, 90, 20, nm, bold=True, fs=10))
    body.append(label('req_d', 490, 370, 460, 150, 'aws s3 cp --request-payer requester\\n  s3://BUCKET/FILE .\\n\\n・取得トラフィック/APIコストは自アカウント課金\\n・IAM ポリシーに s3:GetObject と\\n  s3:GetObjectVersion が必要', fs=10, align="left"))

    body.append(arrow_pts('a1', 440, 140, 520, 140, C_ORANGE, 2, "GetObject (RequestPayer)"))
    write_diag('SAP-126', '\n'.join(body), 1000, 580)

# ==========================================================================
# SAP-140 SCP 階層 + 明示的 Deny + OU 単位の例外
# ==========================================================================
def diag_sap_140():
    body = [title_cell("SAP-140: SCP 階層 — ルートで Deny + 特定 OU/アカウントで許可 (買収アカウント例外)")]
    body.append(box('root', 30, 60, 940, 100, 'Root OU (組織全体)', fill="#FFEFEF", stroke=C_RED, fs=12))
    body.append(label('root_d', 50, 95, 900, 60, 'ルート SCP (すべて継承):\\n  Deny config:* (AWS Config 変更を禁止)\\n  ← Config を勝手に無効化できないセキュリティ統制', fs=10, align="left", color=C_RED))

    body.append(box('prodou', 30, 180, 450, 160, 'Production OU (標準運用)', fill="#F0F8E8", stroke=C_GREEN, fs=11))
    body.append(label('prod_d', 50, 215, 410, 120, '・ルート SCP を継承 → Config 変更不可\\n・本番アカウントはセキュリティ統制順守\\n・FullAWSAccess + ルート Deny が基本', fs=10, align="left"))
    for i, x in enumerate([60, 160, 260, 360]):
        body.append(aws_icon(f'p{i}', x, 290, I_ORG, fill=C_RED, w=40, h=40))

    body.append(box('acqou', 500, 180, 470, 160, 'Acquired OU (買収アカウント — Config 設定作業中)', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('acq_d', 520, 215, 430, 120, '・OU 専用 SCP で Config 許可を上書き\\n  (Allow config:*)\\n・ただし SCP は IAM "Deny + Allow の AND"\\n  → ルート Deny を OU で「上書き許可」\\n  するには適切な Allow SCP のみでは不可\\n  → Deny 条件に Account の NotIn を使う', fs=10, align="left"))
    for i, x in enumerate([530, 630, 730]):
        body.append(aws_icon(f'q{i}', x, 290, I_ORG, fill=C_ORANGE, w=40, h=40))

    body.append(box('detail', 30, 360, 940, 220, 'ルート SCP 実装パターン (買収アカウント除外)', fill="#EBF1FF", stroke=C_BLUE, fs=12))
    body.append(label('detail_d', 50, 400, 900, 170,
        'ルート SCP:\\n'
        '{\\n'
        '  "Effect": "Deny",\\n'
        '  "Action": ["config:*"],\\n'
        '  "Resource": "*",\\n'
        '  "Condition": {\\n'
        '    "StringNotEquals": {\\n'
        '      "aws:PrincipalAccount": ["買収アカウントID1", "買収アカウントID2"]\\n'
        '    }\\n'
        '  }\\n'
        '}\\n'
        '× OU 専用 Allow SCP だけ足しても Deny が勝つ → Deny 側の例外条件で除外が正解',
        fs=10, align="left"))
    write_diag('SAP-140', '\n'.join(body), 1000, 600)

# ==========================================================================
# SAP-149 Private Marketplace + SCP
# ==========================================================================
def diag_sap_149():
    body = [title_cell("SAP-149: Private Marketplace 管理権限を特定ロールのみに限定 (組織全体 SCP)")]
    body.append(box('mgmt', 30, 60, 420, 480, 'Management Account (購買部門)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('pmp', 80, 110, 'mxgraph.aws4.marketplace_dark', fill=C_ORANGE))
    body.append(label('pmp_l', 40, 168, 140, 20, 'Private Marketplace', bold=True))
    body.append(aws_icon('role', 230, 110, I_IAM, fill=C_RED))
    body.append(label('role_l', 180, 168, 160, 20, 'ProcurementAdmin Role', bold=True, fs=10))
    body.append(aws_icon('scp', 370, 110, I_IAM, fill=C_RED))
    body.append(label('scp_l', 355, 168, 90, 20, 'SCP', bold=True))
    body.append(label('scp_d', 50, 200, 390, 220,
        'SCP (組織ルート):\\n'
        '{\\n'
        '  "Effect": "Deny",\\n'
        '  "Action": [\\n'
        '    "aws-marketplace:Associate*",\\n'
        '    "aws-marketplace:Disassociate*",\\n'
        '    "aws-marketplace:ModifyPrivateMarketplace"\\n'
        '  ],\\n'
        '  "Resource": "*",\\n'
        '  "Condition": {\\n'
        '    "StringNotLike": {\\n'
        '      "aws:PrincipalArn":\\n'
        '        "arn:aws:iam::*:role/ProcurementAdmin"\\n'
        '    }\\n'
        '  }\\n'
        '}', fs=9, align="left", color=C_RED))
    body.append(label('mgmt_note', 50, 430, 390, 90, 'これを組織ルートに付与すれば、すべての\\n現行/将来のメンバーアカウントに自動適用される', fs=10, align="left", color=C_BLUE))

    body.append(box('mems', 490, 60, 480, 480, 'メンバーアカウント (開発 / 本番)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    for i,(x,y,nm) in enumerate([(540,110,'Dev1'),(700,110,'Dev2'),(860,110,'Dev3'),(540,260,'Prod1'),(700,260,'Prod2'),(860,260,'Prod3')]):
        body.append(aws_icon(f'a{i}', x, y, I_ORG, fill=C_RED))
        body.append(label(f'al{i}', x-15, y+58, 80, 20, nm, bold=True, fs=10))
    body.append(label('mem_d', 510, 380, 450, 150, '開発者ユーザ: Private Marketplace 変更不可\\n(SCP で Deny)\\n\\nProcurementAdmin を AssumeRole した場合のみ許可\\n\\n× IAM ポリシーで各アカウント個別設定 → 追加時に漏れる\\n× 監査ログだけ → 事後検知で防止できない', fs=10, align="left"))
    write_diag('SAP-149', '\n'.join(body), 1000, 580)

# ==========================================================================
# SAP-153 Organization 間のアカウント移管 3 ステップ
# ==========================================================================
def diag_sap_153():
    body = [title_cell("SAP-153: AWS アカウントを別 Organization に移管する正しい 3 ステップ")]
    body.append(box('src', 30, 60, 420, 480, '移行元 Organization', fill="#FFEFEF", stroke=C_RED, fs=12))
    body.append(aws_icon('srcorg', 70, 110, I_ORG, fill=C_RED))
    body.append(label('src_l', 40, 168, 140, 20, '移行元 Organizations', bold=True))
    body.append(aws_icon('srcacc', 230, 110, I_ORG, fill=C_ORANGE))
    body.append(label('srcacc_l', 190, 168, 140, 20, '移動対象アカウント', bold=True))
    body.append(label('step1', 50, 210, 390, 120,
        '① 移行元で RemoveAccountFromOrganization\\n  ・前提: 該当アカウントが "招待で参加" した\\n    アカウントのみ可能\\n  ・Organizations で作成したアカウントは\\n    事前に Standalone 化が必要', fs=10, align="left", color=C_RED))
    body.append(label('step1b', 50, 340, 390, 170,
        '注意事項:\\n・支払方法がアカウントに設定されているか確認\\n  (なければ一時的に課金が止まる)\\n・RemoveAccountFromOrganization は\\n  管理アカウントからのみ実行可\\n・連結請求アカウントから外れ、\\n  ボリューム割引等は受けられなくなる', fs=10, align="left"))

    body.append(box('dst', 490, 60, 480, 480, '移行先 Organization', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    body.append(aws_icon('dstorg', 530, 110, I_ORG, fill=C_GREEN))
    body.append(label('dst_l', 500, 168, 130, 20, '移行先 Organizations', bold=True))
    body.append(label('step2', 510, 210, 450, 140,
        '② 移行先の管理アカウントから Invite 送信\\n  ・対象アカウントのメール/アカウントID を指定\\n  ・target 側で招待を Accept\\n  ・(標準で 15 日間有効)', fs=10, align="left", color=C_GREEN))
    body.append(label('step3', 510, 360, 450, 170,
        '③ 受信側で AcceptHandshake を実行\\n  ・AWS Organizations コンソールで承認\\n  ・Accept すると即座に移行先 Organization へ\\n  ・その後 OU 配置 / SCP 付与を行う\\n\\n順序: ① Remove → ② Invite → ③ Accept\\n   (Remove を先にしないと新組織へ入れない)', fs=10, align="left"))

    body.append(arrow_pts('r1', 270, 135, 530, 135, C_BLUE, 2, "移管フロー"))
    write_diag('SAP-153', '\n'.join(body), 1000, 580)

# ==========================================================================
# SAP-157 SCP — 組織全体リージョン制限 + OU 個別 EC2 タイプ制限
# ==========================================================================
def diag_sap_157():
    body = [title_cell("SAP-157: SCP 多層防御 — ルートでリージョン制限 + OU で EC2 InstanceType 制限")]
    body.append(box('root', 30, 60, 940, 130, 'Root SCP: aws:RequestedRegion 制限 (全アカウント共通)', fill="#FFF9E6", stroke=C_ORANGE, fs=12))
    body.append(aws_icon('scpr', 70, 100, I_IAM, fill=C_RED))
    body.append(label('scpr_l', 50, 158, 110, 20, 'Root SCP', bold=True))
    body.append(label('scpr_d', 190, 100, 760, 80, '{\\n  "Effect": "Deny", "Action": "*", "Resource": "*",\\n  "Condition": { "StringNotEquals": { "aws:RequestedRegion": ["ap-northeast-1","us-east-1"] } }\\n}', fs=10, align="left", color=C_RED))

    body.append(box('ou_res', 30, 210, 450, 250, 'Research OU (研究開発 — 小型インスタンスのみ)', fill="#F0F8E8", stroke=C_GREEN, fs=11))
    body.append(aws_icon('scp_r', 60, 245, I_IAM, fill=C_RED))
    body.append(label('scp_rl', 40, 300, 100, 20, 'OU SCP', bold=True, fs=10))
    body.append(label('ou_res_d', 170, 245, 300, 180,
        '{\\n  "Effect": "Deny",\\n  "Action": "ec2:RunInstances",\\n  "Condition": {\\n    "StringNotEquals": {\\n      "ec2:InstanceType":\\n        ["t3.*","m5.large"]\\n    }\\n  }\\n}', fs=9, align="left"))
    for i,x in enumerate([50,170,290,410]):
        body.append(aws_icon(f'ra{i}', x, 410, I_ORG, fill=C_RED, w=30, h=30))

    body.append(box('ou_prod', 500, 210, 470, 250, 'Production OU (本番 — 制限なし)', fill="#EBF1FF", stroke=C_BLUE, fs=11))
    body.append(label('ou_prod_d', 520, 245, 430, 180,
        '・本番 OU では EC2 InstanceType 制限を設けない\\n  (ルート SCP のリージョン制限のみ適用)\\n\\n・ルート = 組織全体の「下限」\\n・OU SCP = 下位スコープの追加制約\\n\\n重要: SCP は "Deny のフィルタ"。\\n  上位で Deny されたら下位で Allow 不可', fs=10, align="left"))
    for i,x in enumerate([520,650,780,910]):
        body.append(aws_icon(f'pa{i}', x, 410, I_ORG, fill=C_RED, w=30, h=30))

    body.append(box('key', 30, 480, 940, 110, 'ベストプラクティス: "大きい制限は上位 OU に / 細かい制限は下位 OU に"', fill="#EBF1FF", stroke=C_BLUE, fs=12))
    body.append(label('key_d', 50, 515, 900, 70, '× IAM ポリシーで各アカウント個別設定 → ドリフトと漏れ\\n× Config ルール単体 → 違反リソースの検知のみで作成は防げない\\n○ SCP は予防的統制 = AWS API レベルで拒否する', fs=10, align="left"))
    write_diag('SAP-157', '\n'.join(body), 1000, 610)

# ==========================================================================
# SAP-172 Firewall Manager + WAF 組織全体
# ==========================================================================
def diag_sap_172():
    body = [title_cell("SAP-172: AWS Firewall Manager で WAF ルールを組織全体に自動適用")]
    body.append(box('mgmt', 30, 60, 380, 480, 'Management Account (Firewall Manager 管理)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 60, 100, I_ORG, fill=C_RED))
    body.append(label('org_l', 40, 158, 110, 20, 'Organizations', bold=True))
    body.append(aws_icon('fms', 200, 100, 'mxgraph.aws4.firewall_manager', fill=C_RED))
    body.append(label('fms_l', 155, 158, 180, 20, 'AWS Firewall Manager', bold=True))
    body.append(label('fms_note', 40, 195, 360, 130, '前提:\\n・AWS Config が全アカウントで有効\\n・Security Hub or Firewall Manager\\n  の委任管理者を設定\\n・Policy を 1 つ作成するだけで\\n  組織全体の ALB/CF/API-GW に反映', fs=10, align="left"))

    body.append(aws_icon('waf', 100, 340, 'mxgraph.aws4.waf', fill=C_RED))
    body.append(label('waf_l', 70, 398, 110, 20, 'AWS WAF Rule Group', bold=True, fs=10))
    body.append(label('waf_d', 40, 425, 360, 110, '・Managed Rule / Custom Rule\\n・AWS Managed Rules — Core\\n・SQLi / XSS / レート制限\\n・1 つの Rule Group を共有', fs=10, align="left"))

    body.append(box('mems', 440, 60, 530, 480, 'メンバーアカウント (ALB / CloudFront)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    for i,(x,y,nm) in enumerate([(470,110,'アカウントA'),(670,110,'アカウントB'),(860,110,'アカウントC'),(470,260,'新規 OU'),(670,260,'新規 OU'),(860,260,'新規 OU')]):
        body.append(aws_icon(f'a{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))
        body.append(aws_icon(f'alb{i}', x, y+80, 'mxgraph.aws4.application_load_balancer', fill=C_PURPLE, w=30, h=30))
        body.append(label(f'al{i}', x-20, y+58, 90, 18, nm, fs=9))
    body.append(label('mem_d', 460, 370, 490, 160,
        '・FMS Policy が自動で各 ALB/CF に WAF WebACL を付与\\n・新規作成されたリソースも自動取り込み\\n・違反リソースは Config で検出\\n\\n× Config ルールだけでは作成はブロックされない\\n× 手動で各アカウント WAF を構成 → 運用破綻\\n× CloudFormation StackSets は良いが WAF ルール自動更新が手作業', fs=10, align="left"))

    body.append(arrow_pts('a1', 410, 370, 470, 130, C_ORANGE, 2, "Policy 配布"))
    write_diag('SAP-172', '\n'.join(body), 1000, 580)

# ==========================================================================
# SAP-185 RAM + Prefix List 共有
# ==========================================================================
def diag_sap_185():
    body = [title_cell("SAP-185: マネージド Prefix List + RAM 共有 — SG 参照の内部 IP を一元管理")]
    body.append(box('nacc', 30, 60, 350, 480, 'Network (共有サービス) アカウント', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('pl', 90, 110, I_VPC, fill=C_PURPLE))
    body.append(label('pl_l', 50, 168, 140, 20, 'Managed Prefix List', bold=True))
    body.append(label('pl_d', 50, 200, 300, 160, 'Prefix List: "AllOffices"\\n  10.0.0.0/16\\n  10.2.0.0/16\\n  192.168.0.0/20\\n\\n・最大エントリ数: 1,000\\n・バージョン管理あり\\n・更新 = エントリ追加/削除のみで伝播', fs=10, align="left"))
    body.append(aws_icon('ram', 90, 380, I_RAM, fill=C_RED))
    body.append(label('ram_l', 55, 438, 200, 20, 'Resource Access Manager', bold=True))
    body.append(label('ram_d', 50, 460, 300, 60, 'Principal: AWS Organizations\\n  (または特定 OU)', fs=10, align="left"))

    body.append(box('mems', 400, 60, 570, 480, 'メンバーアカウント (SG で参照)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    for i,(x,y,nm) in enumerate([(440,110,'アカウントA'),(640,110,'アカウントB'),(840,110,'アカウントC')]):
        body.append(aws_icon(f'a{i}', x, y, I_ORG, fill=C_RED))
        body.append(label(f'al{i}', x-20, y+58, 90, 20, nm, bold=True))
        body.append(aws_icon(f'sg{i}', x, y+100, I_EC2, fill=C_ORANGE, w=30, h=30))
    body.append(label('mem_d', 420, 270, 530, 250,
        'SG ルール例:\\n  Inbound 443 from pl-0123abc (AllOffices)\\n\\n・CIDR 変更時は Prefix List を更新するだけ\\n・各 SG は自動で追従\\n・新規アカウントも RAM 共有 → 即時利用\\n\\n× 各 SG に CIDR を直接書く → 変更のたび数百のSG更新\\n× EventBridge + Lambda 自動同期 → 実装/運用コスト大\\n× セキュリティグループ参照 (別SGをソース) はアカウント跨ぎ不可', fs=10, align="left"))

    body.append(arrow_pts('a1', 340, 410, 440, 130, C_PURPLE, 2, "RAM 共有"))
    write_diag('SAP-185', '\n'.join(body), 1000, 580)

# ==========================================================================
# SAP-201 SCP Allow リスト方式と FullAWSAccess
# ==========================================================================
def diag_sap_201():
    body = [title_cell("SAP-201: SCP Allow リスト方式 — FullAWSAccess を外すと全 API が拒否される")]
    body.append(box('default', 30, 60, 450, 250, '既定 (Allow: FullAWSAccess)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    body.append(label('def_d', 50, 100, 410, 200,
        '組織作成時に自動でアタッチ:\\n'
        '  FullAWSAccess = { "Effect":"Allow", "Action":"*", "Resource":"*" }\\n\\n'
        '・SCP は「IAM との AND」で判定\\n'
        '・SCP 側で Allow が必要\\n'
        '・FullAWSAccess があるから IAM ポリシーの範囲内で動作\\n\\n'
        '→ 通常 OU では FullAWSAccess + ルート Deny の組合せが基本', fs=10, align="left"))

    body.append(box('allowlist', 510, 60, 460, 250, 'Allow リスト方式 (FullAWSAccess を外す)', fill="#FFEFEF", stroke=C_RED, fs=12))
    body.append(label('al_d', 530, 100, 420, 200,
        'FullAWSAccess をデタッチし、独自 Allow SCP を付与\\n\\n'
        '例:\\n'
        '  { "Effect":"Allow", "Action":["ec2:*","s3:*"], "Resource":"*" }\\n\\n'
        '・SCP Allow に列挙されたアクションだけが通る\\n'
        '・列挙漏れは IAM で Allow しても SCP で Deny 扱い\\n'
        '・後から API 追加時の運用負荷大', fs=10, align="left", color=C_RED))

    body.append(box('flow', 30, 330, 940, 170, 'SCP 評価フロー', fill="#EBF1FF", stroke=C_BLUE, fs=12))
    body.append(label('flow_d', 50, 370, 900, 130,
        '1. 明示的 Deny (SCP) ? → 即 Deny\\n'
        '2. 明示的 Allow (SCP) ? → IAM 側の評価へ\\n'
        '3. IAM で Allow + Resource/Condition 合致? → 許可\\n\\n'
        'つまり SCP Allow に載っていない API は、IAM で Allow していても Deny\\n'
        '→ 「Allow リスト方式は列挙コストが高く、運用ミスで全 API 停止のリスク」', fs=10, align="left"))

    body.append(box('bp', 30, 520, 940, 70, '推奨: Deny リスト方式 (FullAWSAccess はそのまま + 禁止アクションだけ Deny)', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    write_diag('SAP-201', '\n'.join(body), 1000, 610)

# ==========================================================================
# SAP-213 クロスアカウント監査 (Security OU / 委任管理者)
# ==========================================================================
def diag_sap_213():
    body = [title_cell("SAP-213: Security アカウント委任管理 + クロスアカウント ReadOnly ロールで横断監査")]
    body.append(box('sec', 30, 60, 350, 480, 'Security アカウント (委任管理者)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('sh', 80, 110, 'mxgraph.aws4.security_hub', fill=C_RED))
    body.append(label('sh_l', 50, 168, 110, 20, 'Security Hub', bold=True))
    body.append(aws_icon('gd', 220, 110, 'mxgraph.aws4.guardduty', fill=C_RED))
    body.append(label('gd_l', 195, 168, 100, 20, 'GuardDuty', bold=True))
    body.append(aws_icon('cfg', 80, 240, I_CFG, fill=C_RED))
    body.append(label('cfg_l', 40, 298, 140, 20, 'Config Aggregator', bold=True))
    body.append(aws_icon('ctr', 220, 240, I_CTR, fill=C_GREEN))
    body.append(label('ctr_l', 180, 298, 140, 20, 'CloudTrail 集約', bold=True))
    body.append(aws_icon('role', 150, 370, I_IAM, fill=C_RED))
    body.append(label('role_l', 100, 428, 200, 20, 'SecurityAuditRole (IAM)', bold=True))
    body.append(label('sec_d', 50, 455, 320, 70, '・Organizations 信頼アクセスで委任管理者化\\n・Config / GuardDuty / Security Hub を\\n  組織アカウントとして集約', fs=10, align="left"))

    body.append(box('mems', 400, 60, 570, 480, 'メンバーアカウント', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    for i,(x,y) in enumerate([(440,110),(620,110),(800,110),(440,250),(620,250),(800,250),(440,390),(620,390),(800,390)]):
        body.append(aws_icon(f'a{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))
        body.append(aws_icon(f'r{i}', x+60, y, I_IAM, fill=C_RED, w=30, h=30))
        body.append(label(f'rl{i}', x+30, y+42, 100, 18, 'AuditRole', fs=8))

    body.append(arrow_pts('ar1', 380, 400, 440, 130, C_ORANGE, 2, "AssumeRole (ReadOnly)"))
    body.append(label('note', 460, 460, 490, 70, '各アカウントに ReadOnly な AuditRole を StackSets で\\n自動配布 (信頼 = SecurityAuditRole)。監査員は Security\\nから AssumeRole で一時クレデンシャルを取得。', fs=10, align="left"))
    write_diag('SAP-213', '\n'.join(body), 1000, 580)

# ==========================================================================
# SAP-240 Route 53 Private Hosted Zone クロスアカウント関連付け
# ==========================================================================
def diag_sap_240():
    body = [title_cell("SAP-240: Private Hosted Zone をクロスアカウント VPC に関連付ける正しい手順")]
    body.append(box('gov', 30, 60, 420, 260, 'ガバナンス部門アカウント (PHZ 所有)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('phz', 80, 110, 'mxgraph.aws4.route_53', fill=C_PURPLE))
    body.append(label('phz_l', 50, 168, 130, 20, 'Private Hosted Zone', bold=True))
    body.append(label('phz_d', 230, 105, 210, 70, 'corp.internal\\n  api.corp.internal → ALB IP\\n  db.corp.internal → RDS', fs=9, align="left"))
    body.append(label('step1', 50, 200, 390, 110,
        '① PHZ 所有者が AuthorizeVPCAssociation:\\n  aws route53 create-vpc-association-authorization\\n    --hosted-zone-id Z123\\n    --vpc VPCRegion=...,VPCId=vpc-other', fs=10, align="left", color=C_BLUE))

    body.append(box('app', 30, 340, 420, 260, 'アプリ部門アカウント (VPC 所有)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    body.append(aws_icon('vpc', 80, 390, I_VPC, fill=C_PURPLE))
    body.append(label('vpc_l', 50, 448, 130, 20, 'アプリ VPC', bold=True))
    body.append(label('step2', 50, 480, 390, 110,
        '② VPC 所有者が AssociateVPCWithHostedZone:\\n  aws route53 associate-vpc-with-hosted-zone\\n    --hosted-zone-id Z123\\n    --vpc VPCRegion=...,VPCId=vpc-self', fs=10, align="left", color=C_GREEN))

    body.append(box('done', 490, 60, 480, 540, '関連付け成立後', fill="#FFF9E6", stroke=C_ORANGE, fs=12))
    body.append(label('done_d', 510, 100, 440, 500,
        '・VPC 内の EC2/Lambda から PHZ の名前解決可\\n  → EC2 が db.corp.internal → RDS IP\\n\\n必要な手順 (順序必須):\\n  ① Authorize (PHZ 側)  ← 両方要る\\n  ② Associate (VPC 側)\\n\\n便利な考え方:\\n  "AWS が両アカウントから合意を取るため、\\n   招待 (Authorize) → 受諾 (Associate) の 2 段"\\n\\n× PHZ 所有者だけで完結しない\\n× VPC 所有者だけで完結しない\\n× Private Link / VPC Peering は別問題\\n\\n完了後のクリーンアップ:\\n  DeleteVPCAssociationAuthorization を実行\\n  (Authorize だけ残すとセキュリティ上 NG)', fs=10, align="left"))
    write_diag('SAP-240', '\n'.join(body), 1000, 640)

# ==========================================================================
# SAP-252 Organizations + TGW + RAM 自動統合
# ==========================================================================
def diag_sap_252():
    body = [title_cell("SAP-252: Organizations 統合 + TGW を RAM でルート共有 (VPC 自動接続)")]
    body.append(box('nacc', 30, 60, 340, 480, 'Network アカウント (TGW オーナー)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('tgw', 130, 110, I_TGW, fill=C_PURPLE))
    body.append(label('tgw_l', 100, 168, 120, 20, 'Transit Gateway', bold=True))
    body.append(label('tgw_d', 50, 200, 280, 140, 'Auto Accept Attachments: ON\\n  (組織内の VPC からの attach 要求を自動承認)\\n\\nDefault Route Table / Propagation ON', fs=10, align="left"))
    body.append(aws_icon('ram', 130, 360, I_RAM, fill=C_RED))
    body.append(label('ram_l', 80, 418, 220, 20, 'Resource Access Manager', bold=True))
    body.append(label('ram_d', 50, 445, 280, 80, 'Principal: Organizations または OU\\n  → TGW を全アカウントに共有\\n(Principal を Organization にすると新規アカウントも自動共有)', fs=10, align="left"))

    body.append(box('mems', 390, 60, 580, 480, '50 メンバーアカウント', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    for i,(x,y) in enumerate([(420,110),(560,110),(700,110),(840,110),(420,220),(560,220),(700,220),(840,220),(420,330),(560,330),(700,330),(840,330)]):
        body.append(aws_icon(f'vpc{i}', x, y, I_VPC, fill=C_PURPLE, w=40, h=40))
        body.append(label(f'vl{i}', x-15, y+42, 70, 18, f'VPC{i+1}', fs=9))

    body.append(label('mem_d', 410, 400, 550, 130,
        '各アカウントで CreateTransitGatewayVpcAttachment\\n  → TGW 共有済みなので追加承認不要\\n  → Auto Accept ON で即座にアタッチ完了\\n\\n× VPC Peering 総当たり = N*(N-1)/2 メッシュで破綻\\n× TGW Peering = リージョン間の話で同一Orgには不要', fs=10, align="left"))

    body.append(arrow_pts('a1', 330, 380, 420, 130, C_ORANGE, 2, "RAM 共有"))
    write_diag('SAP-252', '\n'.join(body), 1000, 580)

# ==========================================================================
# SAP-284 3 アカウント ELB ログ集約 S3
# ==========================================================================
def diag_sap_284():
    body = [title_cell("SAP-284: 3 アカウント ELB アクセスログ → 中央 S3 バケット (暗号化集約)")]
    body.append(box('log', 30, 60, 360, 480, 'Logging アカウント (中央 S3)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('s3', 130, 110, I_S3, fill=C_GREEN))
    body.append(label('s3_l', 90, 168, 140, 20, '中央ログ S3 バケット', bold=True))
    body.append(aws_icon('kms', 270, 110, I_KMS, fill=C_RED))
    body.append(label('kms_l', 245, 168, 100, 20, 'KMS CMK (SSE-KMS)', bold=True, fs=9))
    body.append(label('bp', 50, 200, 330, 220,
        'S3 バケットポリシー:\\n  Principal: ELB サービスアカウント ID\\n    (各リージョンの固定値)\\n  Action: s3:PutObject\\n  Resource: bucket/AWSLogs/ACCT-A/*\\n            bucket/AWSLogs/ACCT-B/*\\n            bucket/AWSLogs/ACCT-C/*\\n\\nKMS キーポリシー:\\n  Principal: ELB Delivery Service\\n  Action: kms:GenerateDataKey', fs=9, align="left"))
    body.append(label('log_note', 50, 430, 330, 100, '・ELB は書き込み先 S3 とクロスアカウント可\\n・バケットポリシーで各 ELB アカウントを許可\\n・プレフィックスでアカウント別に分離', fs=10, align="left", color=C_BLUE))

    body.append(box('accs', 410, 60, 560, 480, 'ソースアカウント × 3', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    for i,(x,y,nm) in enumerate([(450,110,'決済本番'),(640,110,'分析用'),(830,110,'監査用')]):
        body.append(aws_icon(f'elb{i}', x, y, 'mxgraph.aws4.elastic_load_balancing', fill=C_PURPLE))
        body.append(label(f'el{i}', x-20, y+58, 90, 20, nm, bold=True))
        body.append(aws_icon(f'ec{i}', x, y+100, I_EC2, fill=C_ORANGE, w=30, h=30))
    body.append(label('acc_d', 430, 280, 540, 240,
        '各 ELB の「アクセスログ出力先」に中央 S3 バケットを指定\\n  s3://central-logs/AWSLogs/ACCT-X/...\\n\\n認可フロー:\\n  ① ELB → S3 PUT\\n    (S3 バケットポリシーで ELB サービス AWS ID を許可)\\n  ② SSE-KMS で暗号化\\n    (KMS キーポリシーで ELB Delivery サービスに Encrypt 許可)\\n\\n× IAM ロールで集めようとする → ELB はロール引き受けに対応していない\\n× CloudWatch Logs 経由 → 可能だがコスト高 / 本問は S3 に直送が要件', fs=10, align="left"))

    body.append(arrow_pts('a1', 450, 130, 390, 130, C_ORANGE, 2, "ログ PUT"))
    write_diag('SAP-284', '\n'.join(body), 1000, 580)

# ==========================================================================
# SAP-289 EU 限定 SCP
# ==========================================================================
def diag_sap_289():
    body = [title_cell("SAP-289: Organizations ルート SCP で EU リージョン限定 (RequestedRegion)")]
    body.append(box('mgmt', 30, 60, 940, 140, 'Management Account + ルート SCP', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 80, 100, I_ORG, fill=C_RED))
    body.append(label('org_l', 60, 158, 100, 20, 'Organizations', bold=True))
    body.append(aws_icon('scp', 230, 100, I_IAM, fill=C_RED))
    body.append(label('scp_l', 210, 158, 80, 20, 'SCP', bold=True))
    body.append(label('scp_d', 340, 90, 620, 100,
        '{\\n  "Effect": "Deny", "Action": "*", "Resource": "*",\\n  "Condition": { "StringNotEquals": {\\n    "aws:RequestedRegion": ["eu-west-1","eu-central-1","eu-north-1","eu-west-2","eu-west-3","eu-south-1"]\\n  } } }', fs=9, align="left", color=C_RED))

    body.append(box('ous', 30, 220, 940, 220, 'Organizations 配下の全 OU / 全アカウント', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    body.append(box('prod', 50, 260, 280, 170, 'Production OU', fill="#FFF9E6", stroke=C_ORANGE, fs=10))
    for i,(x,y) in enumerate([(70,295),(180,295),(70,370),(180,370)]):
        body.append(aws_icon(f'p{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))
    body.append(box('stg', 350, 260, 280, 170, 'Staging OU', fill="#FFF9E6", stroke=C_ORANGE, fs=10))
    for i,(x,y) in enumerate([(370,295),(480,295),(370,370),(480,370)]):
        body.append(aws_icon(f's{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))
    body.append(box('dev', 650, 260, 300, 170, 'Development OU', fill="#FFF9E6", stroke=C_ORANGE, fs=10))
    for i,(x,y) in enumerate([(670,295),(790,295),(670,370),(790,370)]):
        body.append(aws_icon(f'd{i}', x, y, I_ORG, fill=C_RED, w=40, h=40))

    body.append(box('note', 30, 460, 940, 130, 'スケーラビリティのポイント', fill="#FFF0F0", stroke=C_RED, fs=12))
    body.append(label('note_d', 50, 500, 900, 90,
        '○ ルート SCP に 1 箇所書くだけで現行/将来の全アカウントに自動適用\\n'
        '× 各 IAM ユーザに SCP 相当の Deny を個別設定 → 新規メンバーアカウントに展開忘れ\\n'
        '× Config ルールで検知のみ → 作成そのものは止まらない (事後検知)\\n'
        '× CloudFormation StackSets で VPC 削除ポリシー → API リージョン制限にはならない', fs=10, align="left"))
    write_diag('SAP-289', '\n'.join(body), 1000, 610)


# ---- Main ------------------------------------------------------------------
if __name__ == '__main__':
    funcs = [
        diag_sap_33, diag_sap_36, diag_sap_49, diag_sap_60, diag_sap_63,
        diag_sap_72, diag_sap_75, diag_sap_78, diag_sap_81, diag_sap_94,
        diag_sap_97, diag_sap_101, diag_sap_103, diag_sap_111, diag_sap_126,
        diag_sap_140, diag_sap_149, diag_sap_153, diag_sap_157, diag_sap_172,
        diag_sap_185, diag_sap_201, diag_sap_213, diag_sap_240, diag_sap_252,
        diag_sap_284, diag_sap_289,
    ]
    for fn in funcs:
        fn()
    print(f'\nTotal: {len(funcs)} drawio files')
