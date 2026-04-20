#!/usr/bin/env python3
"""Generate drawio files for selected Udemy multi-account/Organizations questions."""
import os

OUT_DIR = '/Users/aki/aws-sap/docs/diagrams/per-question'
os.makedirs(OUT_DIR, exist_ok=True)

# -- Helpers ----------------------------------------------------------------

def _esc(s):
    """XML-escape a value attribute and convert literal '\\n' to drawio line break."""
    if s is None:
        return ''
    # First protect literal '\n' (two chars) by replacing with a placeholder
    s = str(s)
    s = s.replace('\\n', '\x01')
    s = (s.replace('&', '&amp;')
          .replace('<', '&lt;')
          .replace('>', '&gt;')
          .replace('"', '&quot;'))
    # Restore as drawio linebreak
    s = s.replace('\x01', '&#xa;')
    return s

# AWS icon style templates
def aws_icon(cell_id, x, y, res_icon, fill="#FF9900", w=50, h=50):
    """AWS service icon (50x50 default)."""
    return f'''        <mxCell id="{cell_id}" value="" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={fill};strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon={res_icon};" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
        </mxCell>'''

def label(cell_id, x, y, w, h, text, fs=10, bold=False, color="#232F3E", align="center"):
    fontstyle = 1 if bold else 0
    text_esc = _esc(text)
    return f'''        <mxCell id="{cell_id}" value="{text_esc}" style="text;html=1;align={align};verticalAlign=middle;whiteSpace=wrap;fontSize={fs};fontStyle={fontstyle};fontColor={color};" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
        </mxCell>'''

def box(cell_id, x, y, w, h, title, fill="#FFFFFF", stroke="#3B48CC", fs=12, stroke_width=2):
    t_esc = _esc(title)
    return f'''        <mxCell id="{cell_id}" value="{t_esc}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth={stroke_width};fontSize={fs};fontStyle=1;fontColor=#232F3E;verticalAlign=top;spacingTop=6;" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
        </mxCell>'''

def arrow(cell_id, source, target, color="#3B48CC", width=2, style_extra="", label_text=""):
    lbl = f' value="{_esc(label_text)}"' if label_text else ' value=""'
    return f'''        <mxCell id="{cell_id}"{lbl} style="endArrow=classic;html=1;strokeColor={color};strokeWidth={width};fontSize=10;fontColor={color};{style_extra}" edge="1" parent="1" source="{source}" target="{target}">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>'''

def arrow_pts(cell_id, x1, y1, x2, y2, color="#3B48CC", width=2, label_text=""):
    lbl = f' value="{_esc(label_text)}"' if label_text else ' value=""'
    return f'''        <mxCell id="{cell_id}"{lbl} style="endArrow=classic;html=1;strokeColor={color};strokeWidth={width};fontSize=10;fontColor={color};" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{x1}" y="{y1}" as="sourcePoint" />
            <mxPoint x="{x2}" y="{y2}" as="targetPoint" />
          </mxGeometry>
        </mxCell>'''

def title_cell(text, w=1000, fs=18):
    t_esc = _esc(text)
    return f'''        <mxCell id="title" value="{t_esc}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize={fs};fontStyle=1;fontColor=#232F3E;" vertex="1" parent="1">
          <mxGeometry x="0" y="10" width="{w}" height="30" as="geometry" />
        </mxCell>'''

def wrap_mxfile(body, w=1000, h=600, name="diagram"):
    return f'''<mxfile host="app.diagrams.net" modified="2026-04-20T18:00:00.000Z" agent="Claude" version="24.0.0">
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
    content = wrap_mxfile(body, w=w, h=h, name=qid)
    path = os.path.join(OUT_DIR, f'{qid}.drawio')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'wrote {path}')

# ----- AWS colors -----
C_ORANGE = "#FF9900"
C_BLUE   = "#3B48CC"
C_GREEN  = "#7AA116"
C_RED    = "#DD344C"
C_PINK   = "#E7157B"
C_PURPLE = "#8C4FFF"
C_DARK   = "#232F3E"


# ==========================================================================
# UDEMY-007 (num=306) - 管理アカウントIAMユーザ→メンバーアカウントのクロスアカウントロール
# ==========================================================================
def diag_udemy_007():
    body = [title_cell("UDEMY-007: 管理アカウント IAMユーザ → メンバーアカウントのクロスアカウントロール (最小特権)")]
    # Management account
    body.append(box('mgmt', 40, 70, 300, 340, 'Management Account (管理アカウント)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('mgmt_iam', 140, 130, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
    body.append(label('mgmt_iam_l', 110, 185, 160, 20, 'IAM ユーザ / グループ', bold=True))
    body.append(label('mgmt_iam_p', 55, 215, 270, 80, 'IAM ポリシー:\\n  Action: sts:AssumeRole\\n  Resource:\\n    arn:aws:iam::LMS-acct:role/MaintRole\\n    arn:aws:iam::Admin-acct:role/MaintRole', fs=10, align="left"))
    body.append(label('mgmt_note', 55, 320, 270, 80, '・請求は管理アカウントに集約\\n・ユーザ ID を一元管理\\n・長期クレデンシャル不要\\n  (STS が短期トークン発行)', fs=10, align="left", color=C_BLUE))

    # STS
    body.append(aws_icon('sts', 430, 175, 'mxgraph.aws4.sts', fill=C_RED))
    body.append(label('sts_l', 400, 230, 110, 30, 'AWS STS\\nsts:AssumeRole', bold=True, fs=10))

    # Member Account 1: LMS
    body.append(box('lms', 620, 70, 340, 160, 'Member Account: LMS', fill="#F0F8E8", stroke=C_GREEN))
    body.append(aws_icon('lms_role', 650, 110, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
    body.append(label('lms_role_l', 645, 165, 60, 20, 'MaintRole', bold=True, fs=9))
    body.append(label('lms_trust', 720, 100, 230, 120, '信頼ポリシー:\\n  Principal: Management-acct\\n  Action: sts:AssumeRole\\n\\n許可ポリシー (最小特権):\\n  ec2:StopInstances\\n  ec2:StartInstances\\n  rds:StopDBInstance など', fs=9, align="left"))

    # Member Account 2: Admin
    body.append(box('adm', 620, 250, 340, 160, 'Member Account: 管理システム', fill="#F0F8E8", stroke=C_GREEN))
    body.append(aws_icon('adm_role', 650, 290, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
    body.append(label('adm_role_l', 645, 345, 60, 20, 'MaintRole', bold=True, fs=9))
    body.append(label('adm_trust', 720, 280, 230, 120, '信頼ポリシー:\\n  Principal: Management-acct\\n  Action: sts:AssumeRole\\n\\n許可ポリシー (最小特権):\\n  メンテナンス操作のみ許可\\n  ※ AdministratorAccess は NG', fs=9, align="left"))

    # Arrows
    body.append(arrow('a1', 'mgmt_iam', 'sts', C_BLUE, label_text="① AssumeRole"))
    body.append(arrow('a2', 'sts', 'lms_role', C_GREEN, label_text="② 一時クレデンシャル"))
    body.append(arrow('a3', 'sts', 'adm_role', C_GREEN))

    # Key msg
    body.append(box('key', 40, 440, 920, 120, '🔑 ベストプラクティス', fill="#FFF9E6", stroke=C_ORANGE, fs=12))
    body.append(label('key_t', 60, 475, 880, 80,
        '・管理アカウントの IAM ユーザ/グループに「AssumeRole の権限」だけを付与\\n'
        '・メンバーアカウントには IAM ロール (信頼ポリシー=管理アカウント) を作り、必要最小限のアクションのみ許可\\n'
        '・AdministratorAccess は付けない。メンテナンス用アクションのみに絞る\\n'
        '・ × 管理アカウントで直接リソース操作 (メンバーと別アカウントなので不可) / × 各メンバーに長期 IAM ユーザ (IDが分散)', fs=10, align="left"))

    write_diag('UDEMY-007', '\n'.join(body), w=1000, h=580)


# ==========================================================================
# UDEMY-019 (num=318) - EU限定SCP + 一元請求 + AWS Organizations
# ==========================================================================
def diag_udemy_019():
    body = [title_cell("UDEMY-019: Organizations 一元請求 + リージョン制限 SCP (EU限定)")]
    # Management account
    body.append(box('mgmt', 40, 70, 920, 100, 'Management Account (管理アカウント / 請求統合)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 80, 100, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('org_l', 60, 155, 110, 20, 'AWS Organizations', bold=True, fs=10))
    body.append(label('consol', 220, 95, 330, 70, 'Consolidated Billing:\\n・全アカウントの請求を統一ビューで集計\\n・財務部門が Cost Explorer / CUR で分析\\n・ボリューム割引も組織全体で適用', fs=10, align="left"))
    body.append(label('scp_desc', 580, 95, 360, 70, 'SCP (サービスコントロールポリシー):\\n  Effect: Deny\\n  Action: "*"\\n  Condition: StringNotEquals\\n    aws:RequestedRegion: [eu-west-1, eu-central-1, eu-north-1]', fs=9, align="left", color=C_RED))

    # OU
    body.append(box('rd_ou', 40, 200, 920, 260, 'R&D OU (7研究開発チーム)  ← SCP をアタッチ', fill="#FFEFD5", stroke=C_ORANGE, fs=12))

    # 7 member accounts
    for i, x in enumerate([70, 200, 330, 460, 590, 720, 850]):
        body.append(aws_icon(f'acc{i}', x, 250, 'mxgraph.aws4.organizations', fill=C_RED))
        body.append(label(f'acc{i}_l', x-15, 305, 80, 20, f'研究チーム{i+1}', bold=True, fs=9))

    body.append(label('ou_note', 60, 350, 880, 95,
        '・R&D OU 配下の 7 アカウントには以下 SCP が適用される:\\n'
        '  - eu-* 以外のリージョンで どの AWS API を呼んでも Deny\\n'
        '  - グローバルサービス (IAM 等) は全リージョン許可になるため許可リスト式でも可\\n'
        '・各チームは自アカウント内で自由に開発できるが、誤って他リージョンでリソース作成する事故を予防',
        fs=10, align="left", color=C_DARK))

    # Right side: alternatives rejected
    body.append(box('cmp', 40, 480, 920, 90, '✗ 他の選択肢が NG な理由', fill="#FFF0F0", stroke=C_RED, fs=11))
    body.append(label('cmp_t', 60, 510, 880, 60,
        '× IAMポリシーで制御 → 各アカウント個別設定で抜け漏れ / × Config ルールだけ → 作成は防げず事後検知のみ\\n'
        '× 各チームの手動レポート → 一元化できず / × Cross-Account Role だけでは作成制限にならない', fs=10, align="left"))

    write_diag('UDEMY-019', '\n'.join(body), w=1000, h=590)


# ==========================================================================
# UDEMY-020 (num=319) - 監査専用アカウント→全メンバーへのクロスアカウント読み取り
# ==========================================================================
def diag_udemy_020():
    body = [title_cell("UDEMY-020: 監査アカウント → 全メンバーアカウント 読み取り専用クロスアカウント")]
    # Audit account
    body.append(box('audit', 40, 70, 280, 300, 'コンプライアンス監査アカウント', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('audit_u', 140, 120, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
    body.append(label('audit_u_l', 100, 175, 150, 20, '監査チーム IAM ユーザ', bold=True, fs=10))
    body.append(label('audit_p', 55, 210, 250, 150,
        'IAM ポリシー:\\n  Action: sts:AssumeRole\\n  Resource: arn:aws:iam::*:\\n    role/ReadOnlyAuditRole\\n\\n短期クレデンシャルで\\n各メンバーアカウントにアクセス', fs=10, align="left"))

    # STS center
    body.append(aws_icon('sts', 420, 200, 'mxgraph.aws4.sts', fill=C_RED))
    body.append(label('sts_l', 395, 255, 110, 30, 'STS AssumeRole', bold=True, fs=10))

    # Member accounts (3 example)
    body.append(box('mem_box', 620, 70, 360, 400, 'メンバーアカウント群 (全アカウント)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    for i, y in enumerate([110, 210, 310]):
        body.append(aws_icon(f'mrole{i}', 650, y, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
        body.append(label(f'mrole{i}_l', 640, y+55, 80, 20, 'ReadOnlyAuditRole', bold=True, fs=8))
        body.append(label(f'mtrust{i}', 740, y-5, 230, 90,
            f'アカウント {i+1}:\\n信頼ポリシー:\\n  Principal: 監査-acct\\nアタッチポリシー:\\n  ReadOnlyAccess (マネージド)', fs=9, align="left"))

    # Arrows
    body.append(arrow('a1', 'audit_u', 'sts', C_BLUE))
    body.append(arrow('a2', 'sts', 'mrole0', C_GREEN))
    body.append(arrow('a3', 'sts', 'mrole1', C_GREEN))
    body.append(arrow('a4', 'sts', 'mrole2', C_GREEN))

    # Bottom: Organization feature
    body.append(box('org_box', 40, 390, 560, 80, 'Organizations の既定ロール: OrganizationAccountAccessRole', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('org_t', 55, 418, 540, 50,
        '・Organizations で作成したアカウントには自動で OrganizationAccountAccessRole が作られる\\n'
        '・これを踏み台にして ReadOnlyAuditRole を作成すれば、各メンバーアカウントごとの手作業は最小化', fs=10, align="left"))

    write_diag('UDEMY-020', '\n'.join(body), w=1000, h=500)


# ==========================================================================
# UDEMY-035 (num=334) - IAM Identity Center + AD Connector + 全社SSO + CUR
# ==========================================================================
def diag_udemy_035():
    body = [title_cell("UDEMY-035: Organizations + IAM Identity Center + AD フェデレーション (一時クレデンシャル)")]
    # On-prem AD
    body.append(box('onprem', 40, 70, 240, 180, 'オンプレミス', fill="#F5F5F5", stroke=C_DARK, fs=11))
    body.append(label('ad', 70, 110, 180, 40, 'Microsoft Active Directory\\n(ユーザ / グループの正本)', bold=True, fs=11, color=C_DARK))
    body.append(label('ad_flow', 70, 170, 180, 70, '・既存ユーザを活用\\n・フェデレーション認証\\n・MFA もオンプレ側で強制可', fs=10, align="left"))

    # AD Connector
    body.append(aws_icon('adc', 320, 135, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
    body.append(label('adc_l', 300, 190, 110, 20, 'AD Connector', bold=True, fs=10))

    # IAM Identity Center (center)
    body.append(box('ic_box', 440, 70, 260, 180, 'Management Account', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('ic', 545, 110, 'mxgraph.aws4.single_sign_on', fill=C_RED))
    body.append(label('ic_l', 495, 165, 160, 20, 'IAM Identity Center', bold=True, fs=10))
    body.append(label('ic_desc', 460, 190, 230, 60, '・権限セット (Permission Set)\\n・AD グループ → AWS アカウント/権限セット\\n・SAML/OIDC で連携', fs=9, align="left"))

    # Organizations
    body.append(aws_icon('org', 545, 285, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('org_l', 495, 340, 160, 20, 'AWS Organizations', bold=True, fs=10))
    body.append(label('org_d', 455, 360, 240, 40, 'アカウント群を一元管理\\n(CUR / Consolidated Billing)', fs=9))

    # Member accounts
    body.append(box('accs', 760, 70, 220, 400, '事業部門別メンバーアカウント', fill="#F0F8E8", stroke=C_GREEN, fs=11))
    for i, y in enumerate([110, 200, 290, 380]):
        body.append(aws_icon(f'a{i}', 850, y, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
        body.append(label(f'a{i}_l', 810, y+45, 120, 20, f'事業部門 {i+1}', bold=True, fs=9))

    # Arrows
    body.append(arrow('ar1', 'ad', 'adc', C_DARK, label_text="LDAP"))
    body.append(arrow('ar2', 'adc', 'ic', C_BLUE))
    body.append(arrow('ar3', 'ic', 'a0', C_GREEN, label_text="SSO"))
    body.append(arrow('ar4', 'ic', 'a1', C_GREEN))
    body.append(arrow('ar5', 'ic', 'a2', C_GREEN))
    body.append(arrow('ar6', 'ic', 'a3', C_GREEN))

    # Key
    body.append(box('key', 40, 280, 360, 200, '🔑 要件とマッピング', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 315, 340, 160,
        '✓ 中央集権的コスト管理 → Organizations\\n   (consolidated billing / CUR / Cost Explorer)\\n\\n'
        '✓ アイデンティティ フェデレーション →\\n   IAM Identity Center + AD Connector\\n\\n'
        '✓ 短期クレデンシャル → Identity Center が\\n   SAML + STS で一時クレデンシャル発行\\n   (IAM アクセスキー不要)', fs=10, align="left"))

    write_diag('UDEMY-035', '\n'.join(body), w=1000, h=500)


# ==========================================================================
# UDEMY-039 (num=338) - 620アカウントを別Organizationへ移動
# ==========================================================================
def diag_udemy_039():
    body = [title_cell("UDEMY-039: 620アカウントを既存組織 → 新組織「イノベーションラボ」に移動")]
    # Old org
    body.append(box('old', 40, 80, 360, 400, '既存組織: R&D', fill="#F0F0F0", stroke="#666666", fs=12))
    body.append(aws_icon('old_mgmt', 160, 110, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('old_mgmt_l', 110, 165, 160, 20, '旧管理アカウント', bold=True, fs=10))
    body.append(label('old_mem', 60, 200, 320, 40, 'メンバーアカウント 620 個\\n(研究者アカウント)', bold=True, fs=11, color=C_DARK))

    # 11 representative member accounts
    for i in range(11):
        col = i % 4
        row = i // 4
        x = 70 + col*80
        y = 260 + row*60
        body.append(aws_icon(f'oa{i}', x, y, 'mxgraph.aws4.organizations', fill=C_RED, w=35, h=35))

    # New org
    body.append(box('new', 620, 80, 340, 400, '新組織: イノベーションラボ', fill="#FFEFD5", stroke=C_ORANGE, fs=12))
    body.append(aws_icon('new_mgmt', 750, 110, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('new_mgmt_l', 690, 165, 160, 20, '新管理アカウント', bold=True, fs=10))
    body.append(label('new_desc', 640, 200, 300, 40, 'アカウント移動先\\n(受け入れ側)', bold=True, fs=11))

    # Arrow (bulk migration)
    body.append(arrow_pts('mig', 420, 280, 600, 280, C_ORANGE, 4, "各アカウント移動"))

    # Steps box
    body.append(box('step', 40, 490, 920, 120, '移動手順 (各 620 アカウントに対して実行)', fill="#EBF1FF", stroke=C_BLUE, fs=11))
    body.append(label('step_t', 55, 520, 900, 90,
        '① 旧組織の管理アカウントから 各メンバーアカウントを「組織から削除 (RemoveAccountFromOrganization)」\\n'
        '   ※ 前提: そのメンバーが Standalone 要件を満たす (Support Plan, IAM Role for Billing 等)\\n'
        '② 新組織の管理アカウントから 各メンバーに「招待 (InviteAccountToOrganization)」 → メンバー側で承諾\\n'
        '   → 新組織の配下に移動完了。アカウント設定は維持される (620 件とも同じ手順の繰り返し)',
        fs=10, align="left"))

    write_diag('UDEMY-039', '\n'.join(body), w=1000, h=630)


# ==========================================================================
# UDEMY-044 (num=343) - Control Tower + OU + リージョン制限SCP
# ==========================================================================
def diag_udemy_044():
    body = [title_cell("UDEMY-044: Control Tower ランディングゾーン + OU + リージョン制限 SCP")]
    # Control Tower
    body.append(box('ct', 40, 70, 920, 90, 'Management Account', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('ct_i', 80, 95, 'mxgraph.aws4.control_tower', fill=C_RED))
    body.append(label('ct_l', 60, 150, 130, 15, 'AWS Control Tower', bold=True, fs=10))
    body.append(aws_icon('org', 240, 95, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('org_l', 220, 150, 130, 15, 'AWS Organizations', bold=True, fs=10))
    body.append(label('ct_desc', 400, 85, 540, 70,
        'ランディングゾーンで以下が自動構築される:\\n'
        '・Organizations と 標準 OU (Security / Audit / Log Archive)\\n'
        '・AWS Config アグリゲータ / CloudTrail 組織トレイル\\n'
        '・IAM Identity Center 連携 / 既定ガードレール', fs=10, align="left"))

    # OU structure with SCP
    body.append(box('ou_apac', 60, 190, 280, 260, 'APAC OU', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    body.append(label('scp_apac', 75, 220, 250, 80,
        'SCP (リージョン制限):\\n  Deny *\\n  Condition: StringNotEquals\\n    aws:RequestedRegion:\\n      [ap-northeast-1, ap-southeast-2]',
        fs=9, align="left", color=C_RED))
    for i, x in enumerate([80, 160, 240]):
        body.append(aws_icon(f'apa{i}', x, 340, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
        body.append(label(f'apa{i}_l', x-5, 385, 60, 20, f'APAC-{i+1}', fs=9))

    body.append(box('ou_emea', 360, 190, 280, 260, 'EMEA OU', fill="#FFEFD5", stroke=C_ORANGE, fs=12))
    body.append(label('scp_emea', 375, 220, 250, 80,
        'SCP (リージョン制限):\\n  Deny *\\n  Condition: StringNotEquals\\n    aws:RequestedRegion:\\n      [eu-west-1, eu-central-1]',
        fs=9, align="left", color=C_RED))
    for i, x in enumerate([380, 460, 540]):
        body.append(aws_icon(f'emea{i}', x, 340, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
        body.append(label(f'emea{i}_l', x-5, 385, 60, 20, f'EMEA-{i+1}', fs=9))

    body.append(box('ou_us', 660, 190, 280, 260, 'US OU', fill="#EBF1FF", stroke=C_BLUE, fs=12))
    body.append(label('scp_us', 675, 220, 250, 80,
        'SCP (リージョン制限):\\n  Deny *\\n  Condition: StringNotEquals\\n    aws:RequestedRegion:\\n      [us-east-1, us-west-2]',
        fs=9, align="left", color=C_RED))
    for i, x in enumerate([680, 760, 840]):
        body.append(aws_icon(f'us{i}', x, 340, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
        body.append(label(f'us{i}_l', x-5, 385, 60, 20, f'US-{i+1}', fs=9))

    # Key
    body.append(box('key', 40, 470, 920, 100, '🔑 Control Tower vs 手動Organizations の違い', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 500, 900, 70,
        '✓ Control Tower: ランディングゾーンで「OU構造・ログ集約・監査・Identity Center」が既定で入る → 大規模展開に最適\\n'
        '✓ リージョン制限は SCP で (aws:RequestedRegion 条件キー)。OU 単位で別リージョン許可リストを持てる\\n'
        '✗ IAM ポリシー / Config ルールでは「作成ブロック」にならない、または OU 単位で一元管理できない', fs=10, align="left"))

    write_diag('UDEMY-044', '\n'.join(body), w=1000, h=590)


# ==========================================================================
# UDEMY-047 (num=346) - OU + リージョン制限SCP + ルートのタグポリシー
# ==========================================================================
def diag_udemy_047():
    body = [title_cell("UDEMY-047: 子会社OU に リージョン制限 SCP / ルートに タグポリシー")]
    # Root
    body.append(box('root', 40, 70, 920, 100, 'Organization Root', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 80, 95, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('org_l', 60, 150, 130, 15, 'AWS Organizations', bold=True, fs=10))
    body.append(label('tag', 230, 80, 710, 80,
        'Tag Policy (ルートに適用 → 全アカウント継承):\\n'
        '  必須タグ: { CostCenter: [ALLOWED_VALUES], Environment: [dev|stg|prd] }\\n'
        '  AWS Config Rule "required-tags" と併用することで 全アカウントに一貫したタグ付けを強制\\n'
        '  → グローバルガバナンス基準をルート1箇所で管理', fs=10, align="left", color=C_PURPLE))

    # Child OU: Subsidiary
    body.append(box('sub_ou', 60, 190, 420, 300, '子会社 OU (規制対象 / リージョン制限アリ)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    body.append(label('sub_scp', 75, 220, 400, 100,
        'SCP (この OU だけに追加適用):\\n'
        '{"Effect": "Deny", "Action": "*",\\n'
        ' "Condition": {"StringNotEqualsIfExists":\\n'
        '   {"aws:RequestedRegion": ["ap-northeast-1"]}}}\\n\\n'
        '→ ap-northeast-1 以外での API 呼び出しを拒否',
        fs=9, align="left", color=C_RED))
    for i, x in enumerate([80, 180, 280, 380]):
        body.append(aws_icon(f'sub{i}', x, 370, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
        body.append(label(f'sub{i}_l', x-5, 415, 60, 20, f'子会社{i+1}', fs=9))
    body.append(label('sub_tag_note', 80, 450, 380, 30, '※ ルートのタグポリシーも継承される', fs=9, color=C_PURPLE))

    # Other OU
    body.append(box('other_ou', 500, 190, 440, 300, 'その他の OU (通常運用)', fill="#FFEFD5", stroke=C_ORANGE, fs=12))
    body.append(label('other_scp', 515, 220, 420, 60,
        'SCP の追加なし (リージョン制限なし)\\n'
        '全リージョン利用可能だが タグポリシーは適用される', fs=10, align="left"))
    for i, x in enumerate([520, 620, 720, 820]):
        body.append(aws_icon(f'o{i}', x, 370, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
        body.append(label(f'o{i}_l', x-5, 415, 60, 20, f'通常{i+1}', fs=9))

    # Key
    body.append(box('key', 40, 510, 920, 90, '🔑 SCP と タグポリシーの適用粒度', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 540, 900, 60,
        '✓ SCP = 「許可の上限」を制御 (境界ポリシー) → OU / アカウント単位で粒度を変えられる\\n'
        '✓ タグポリシー = 「タグの命名規則」を強制 → 全社共通ならルートに適用 → 子OU へ継承', fs=10, align="left"))

    write_diag('UDEMY-047', '\n'.join(body), w=1000, h=620)


# ==========================================================================
# UDEMY-083 (num=382) - クロスアカウントAssumeRole 詳細 (3要素)
# ==========================================================================
def diag_udemy_083():
    body = [title_cell("UDEMY-083: クロスアカウント AssumeRole (3つの必須要素)")]
    # Account A
    body.append(box('accA', 40, 70, 380, 440, 'Account A: 開発部門', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('usrA', 150, 110, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
    body.append(label('usrA_l', 100, 165, 160, 20, 'IAM ユーザ (alice)', bold=True, fs=10))

    body.append(box('polA', 60, 210, 340, 280, '① IAM ポリシー (アイデンティティベース)', fill="#FFFFFF", stroke=C_BLUE, fs=11))
    body.append(label('polA_t', 75, 245, 320, 230,
        '{\\n'
        '  "Version": "2012-10-17",\\n'
        '  "Statement": [{\\n'
        '    "Effect": "Allow",\\n'
        '    "Action": "sts:AssumeRole",\\n'
        '    "Resource":\\n'
        '      "arn:aws:iam::BBBB:role/TestRole"\\n'
        '  }]\\n'
        '}\\n\\n'
        'alice に付与するポリシー。\\n'
        '「B の TestRole を引き受けてよい」\\n'
        'という権限。', fs=10, align="left"))

    # STS
    body.append(aws_icon('sts', 500, 280, 'mxgraph.aws4.sts', fill=C_RED))
    body.append(label('sts_l', 475, 335, 110, 30, 'STS AssumeRole\\n(短期クレデンシャル)', bold=True, fs=10))

    # Account B
    body.append(box('accB', 620, 70, 360, 440, 'Account B: テスト環境', fill="#F0F8E8", stroke=C_GREEN))
    body.append(aws_icon('roleB', 770, 110, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
    body.append(label('roleB_l', 740, 165, 120, 20, 'IAM ロール TestRole', bold=True, fs=10))

    body.append(box('trustB', 640, 210, 340, 135, '② 信頼ポリシー (ロールにアタッチ)', fill="#FFFFFF", stroke=C_GREEN, fs=11))
    body.append(label('trustB_t', 655, 240, 320, 105,
        '{\\n'
        '  "Principal": {"AWS":\\n'
        '    "arn:aws:iam::AAAA:user/alice"},\\n'
        '  "Action": "sts:AssumeRole",\\n'
        '  "Condition": {"StringEquals": {\\n'
        '    "sts:ExternalId": "xyz"}}\\n}', fs=10, align="left"))

    body.append(box('permB', 640, 355, 340, 135, '③ 権限ポリシー (ロールにアタッチ)', fill="#FFFFFF", stroke=C_GREEN, fs=11))
    body.append(label('permB_t', 655, 385, 320, 105,
        '{"Effect": "Allow",\\n'
        ' "Action": ["s3:GetObject"],\\n'
        ' "Resource": "arn:aws:s3:::bucket/*"}\\n\\n'
        '→ 最小特権原則 (必要な操作だけ許可)', fs=10, align="left"))

    # Arrows
    body.append(arrow('ar1', 'usrA', 'sts', C_BLUE, label_text="① AssumeRole"))
    body.append(arrow('ar2', 'sts', 'roleB', C_GREEN, label_text="② 信頼判定"))

    # Key
    body.append(box('key', 40, 530, 940, 60, '🔑 3要素すべて必須', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 555, 920, 40,
        '✓ ① A 側の IAM ポリシー (sts:AssumeRole 許可) / ✓ ② B 側の信頼ポリシー (A をプリンシパルに) / ✓ ③ B 側の権限ポリシー (最小特権)\\n'
        '推奨: 外部ID (ExternalId) / MFA 条件を信頼ポリシーに追加してセキュリティ強化', fs=10, align="left"))

    write_diag('UDEMY-083', '\n'.join(body), w=1000, h=610)


# ==========================================================================
# UDEMY-102 (num=401) - Control Tower カスタム予防ガードレール (開発OU)
# ==========================================================================
def diag_udemy_102():
    body = [title_cell("UDEMY-102: Control Tower カスタム予防ガードレール (開発OU / バースト可能インスタンス限定)")]
    # Management
    body.append(box('mgmt', 40, 70, 920, 100, 'Management Account (Control Tower)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('ct', 80, 95, 'mxgraph.aws4.control_tower', fill=C_RED))
    body.append(label('ct_l', 60, 150, 130, 15, 'AWS Control Tower', bold=True, fs=10))
    body.append(aws_icon('org', 230, 95, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('org_l', 215, 150, 130, 15, 'Organizations', bold=True, fs=10))
    body.append(label('desc', 380, 85, 560, 70,
        'カスタム予防ガードレール = OU に SCP を適用:\\n'
        '  Deny ec2:RunInstances if aws:RequestAttribute/ec2:InstanceType ∉ [t3.*, t4g.*]\\n'
        '  Deny rds:CreateDBInstance if rds:DatabaseClass ∉ [db.t3.*, db.t4g.*]\\n'
        '  Deny 関連性のないサービス (glacier:*, sagemaker:*, ...)', fs=9, align="left", color=C_RED))

    # Dev OU
    body.append(box('dev_ou', 40, 190, 920, 260, '開発者 OU (800+ アカウント)  ← カスタム予防ガードレール適用', fill="#FFEFD5", stroke=C_ORANGE, fs=12))

    # Sample accounts inside
    for i in range(8):
        col = i % 4
        row = i // 4
        x = 80 + col*210
        y = 230 + row*100
        body.append(aws_icon(f'dev{i}', x, y, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
        body.append(label(f'dev{i}_l', x-20, y+45, 80, 20, f'開発者{i+1}', fs=9))

    # Examples
    body.append(label('ex_ok', 80, 410, 200, 30, '✓ t3.medium を起動 → 許可', fs=11, color=C_GREEN, bold=True))
    body.append(label('ex_ng1', 300, 410, 250, 30, '✗ m5.2xlarge を起動 → 拒否', fs=11, color=C_RED, bold=True))
    body.append(label('ex_ng2', 570, 410, 350, 30, '✗ SageMaker ノートブック作成 → 拒否', fs=11, color=C_RED, bold=True))

    # Key
    body.append(box('key', 40, 470, 920, 110, '🔑 Control Tower の 予防 vs 発見 ガードレール', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 500, 900, 80,
        '✓ 予防的 (Preventive) = SCP でアクション拒否 → そもそも作れない (今回の要件)\\n'
        '✓ 発見的 (Detective) = AWS Config ルールで違反検出 → 作成後に通知 (事後検知なので今回不適)\\n'
        '✓ 推奨ガードレール (既定) で不足する場合、SCP を書いてカスタム予防ガードレールとして登録\\n'
        '✓ OU 単位で適用なので、本番 OU には別のルールを持たせられる', fs=10, align="left"))

    write_diag('UDEMY-102', '\n'.join(body), w=1000, h=600)


# ==========================================================================
# UDEMY-108 (num=407) - Control Tower + Organizations + IAM Identity Center + AD FS + OU別SCP
# ==========================================================================
def diag_udemy_108():
    body = [title_cell("UDEMY-108: Control Tower + AD FS 連携 + OU別コンプライアンスSCP (研究機関)")]
    # On-prem AD FS
    body.append(box('onprem', 40, 70, 220, 180, 'オンプレミス', fill="#F5F5F5", stroke=C_DARK, fs=11))
    body.append(label('adfs', 60, 105, 180, 40, 'AD FS (Active Directory\\nFederation Services)', bold=True, fs=11, color=C_DARK))
    body.append(label('adfs_d', 55, 155, 190, 80, 'SAML 2.0 IdP として使用\\n既存ユーザ/グループの正本', fs=10, align="left"))

    # Management account (right of onprem)
    body.append(box('mgmt', 300, 70, 280, 300, 'Management Account', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('ct', 320, 100, 'mxgraph.aws4.control_tower', fill=C_RED))
    body.append(label('ct_l', 310, 155, 90, 15, 'Control Tower', bold=True, fs=9))
    body.append(aws_icon('org', 440, 100, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('org_l', 420, 155, 130, 15, 'Organizations', bold=True, fs=9))
    body.append(aws_icon('ic', 320, 200, 'mxgraph.aws4.single_sign_on', fill=C_RED))
    body.append(label('ic_l', 295, 255, 140, 15, 'IAM Identity Center', bold=True, fs=9))
    body.append(aws_icon('cfg', 440, 200, 'mxgraph.aws4.config', fill=C_GREEN))
    body.append(label('cfg_l', 420, 255, 130, 15, 'AWS Config', bold=True, fs=9))
    body.append(aws_icon('sh', 380, 280, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
    body.append(label('sh_l', 355, 335, 120, 15, 'Security Hub', bold=True, fs=9))

    # OUs (projects)
    body.append(box('ou1', 620, 70, 340, 90, 'プロジェクト OU α (HIPAA準拠)', fill="#F0F8E8", stroke=C_GREEN, fs=11))
    body.append(label('scp1', 635, 100, 320, 60, 'SCP: 承認サービスのみ許可\\n           HIPAA BAA 対象外サービスを Deny', fs=9, align="left", color=C_RED))

    body.append(box('ou2', 620, 170, 340, 90, 'プロジェクト OU β (GDPR準拠)', fill="#FFEFD5", stroke=C_ORANGE, fs=11))
    body.append(label('scp2', 635, 200, 320, 60, 'SCP: EU リージョンのみ許可\\n           データ域外送信を Deny', fs=9, align="left", color=C_RED))

    body.append(box('ou3', 620, 270, 340, 90, 'プロジェクト OU γ (データ主権)', fill="#F0E8F8", stroke=C_PURPLE, fs=11))
    body.append(label('scp3', 635, 300, 320, 60, 'SCP: 指定国のリージョン制限\\n           IAM アクセスキー作成 Deny', fs=9, align="left", color=C_RED))

    # Arrows
    body.append(arrow('ar_adfs', 'adfs', 'ic', C_DARK, label_text="SAML"))
    body.append(arrow('ar_ic_ou1', 'ic', 'ou1', C_BLUE))
    body.append(arrow('ar_ic_ou2', 'ic', 'ou2', C_BLUE))
    body.append(arrow('ar_ic_ou3', 'ic', 'ou3', C_BLUE))

    # Key box
    body.append(box('key', 40, 400, 920, 170, '🔑 Control Tower 中心の設計で運用オーバーヘッド最小', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 435, 900, 130,
        '✓ ランディングゾーン = Organizations + OU 構造 + Config / CloudTrail 組織トレイル + Identity Center が既定でセットアップ\\n'
        '✓ AD FS 連携 = Identity Center の外部 IdP に AD FS (SAML) を登録 → 既存AD の資格情報で AWS SSO\\n'
        '✓ OU 別コンプライアンス = 各プロジェクトを異なる OU に配置し、カスタム SCP で規制ごとの差分を表現\\n'
        '✓ 集中コンプライアンス監視 = AWS Config Aggregator + Security Hub (組織全体) で横断的に評価\\n'
        '✗ IAM ユーザを 各アカウントに作る / 手動 CloudFormation で OU 作成 → 運用負荷 大', fs=10, align="left"))

    write_diag('UDEMY-108', '\n'.join(body), w=1000, h=600)


# Execute all so far
if __name__ == '__main__':
    diag_udemy_007()
    diag_udemy_019()
    diag_udemy_020()
    diag_udemy_035()
    diag_udemy_039()
    diag_udemy_044()
    diag_udemy_047()
    diag_udemy_083()
    diag_udemy_102()
    diag_udemy_108()
    print("Phase 1 done")
