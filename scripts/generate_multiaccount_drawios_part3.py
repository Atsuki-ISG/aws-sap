#!/usr/bin/env python3
"""Generate drawio files - Part 3 (UDEMY-217, 220, 250, 259, 267, 330)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from generate_multiaccount_drawios import (
    aws_icon, label, box, arrow, arrow_pts, title_cell, write_diag,
    C_ORANGE, C_BLUE, C_GREEN, C_RED, C_PINK, C_PURPLE, C_DARK
)


# ==========================================================================
# UDEMY-217 (num=516) - RAM Aurora クロスアカウント + Lambda 移行
# ==========================================================================
def diag_udemy_217():
    body = [title_cell("UDEMY-217: RAM で Aurora をクロスアカウント共有 + Lambda は デプロイパッケージ再利用")]
    # Source account
    body.append(box('src', 40, 60, 420, 480, 'Source アカウント (現行)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('lam_s', 80, 90, 'mxgraph.aws4.lambda', fill=C_ORANGE))
    body.append(label('lam_s_l', 60, 145, 100, 15, 'Lambda 関数', bold=True, fs=10))
    body.append(aws_icon('pkg', 200, 90, 'mxgraph.aws4.s3', fill=C_GREEN))
    body.append(label('pkg_l', 180, 145, 140, 15, 'デプロイパッケージ', bold=True, fs=10))
    body.append(label('pkg_zip', 180, 165, 140, 15, '(.zip / .jar)', fs=9))
    body.append(aws_icon('au', 340, 90, 'mxgraph.aws4.aurora', fill=C_BLUE))
    body.append(label('au_l', 320, 145, 100, 15, 'Aurora DB', bold=True, fs=10))
    body.append(label('au_d', 310, 165, 120, 30, '在庫データ\\n+ 自動バックアップ', fs=9))

    body.append(box('ram_box', 60, 220, 380, 150, 'RAM リソース共有', fill="#F0E8F8", stroke=C_PURPLE, fs=11))
    body.append(aws_icon('ram', 200, 250, 'mxgraph.aws4.resource_access_manager', fill=C_PURPLE))
    body.append(label('ram_l', 170, 305, 120, 20, 'AWS RAM Share', bold=True, fs=10, color=C_PURPLE))
    body.append(label('ram_d', 70, 325, 360, 40,
        'Aurora クラスターを Target アカウントと共有\\nクローン権限 (aurora-clone-permissions) を付与', fs=9, align="left"))

    body.append(label('src_flow', 60, 390, 400, 140,
        '手順:\\n'
        '① デプロイパッケージをダウンロード\\n'
        '② RAM で Aurora クラスターを Target と共有\\n'
        '   (クローン権限を付与)\\n'
        '③ Target 側で Aurora クラスターをクローン\\n'
        '   → 元クラスターのデータをそのまま継承\\n'
        '④ Target 側でカットオーバー → Source 削除',
        fs=10, align="left"))

    # Target account
    body.append(box('tgt', 500, 60, 460, 480, 'Target アカウント (新規)', fill="#F0F8E8", stroke=C_GREEN))
    body.append(aws_icon('lam_t', 540, 90, 'mxgraph.aws4.lambda', fill=C_ORANGE))
    body.append(label('lam_t_l', 520, 145, 100, 15, 'Lambda 関数 (新)', bold=True, fs=10))
    body.append(label('lam_t_d', 510, 165, 120, 30, '同じ パッケージで\\n別アカウントに作成', fs=9))

    body.append(aws_icon('au_c', 680, 90, 'mxgraph.aws4.aurora', fill=C_BLUE))
    body.append(label('au_c_l', 650, 145, 120, 20, 'Aurora クローン', bold=True, fs=10))
    body.append(label('au_c_d', 640, 170, 140, 50, 'コピーオンライト\\n高速コピー\\n元DB に影響なし', fs=9))

    body.append(arrow_pts('ar_share', 440, 280, 680, 115, C_PURPLE, label_text="クローン"))

    body.append(label('tgt_note', 540, 250, 420, 280,
        '✓ クローン = コピーオンライト → 実データ複製なしで即時利用可能 → ダウンタイム最小\\n\\n'
        '✗ バックアップ復元 (Snapshot Restore) =\\n'
        '  復元に時間がかかる / ダウンタイム長い\\n\\n'
        '✗ Target 側で Lambda を新しく書き直す =\\n'
        '  コード再利用できない\\n\\n'
        '✗ DMS でデータ移行 =\\n'
        '  変更キャプチャの設定が必要 / 同一エンジン同一リージョン ではオーバーヘッド\\n\\n'
        '✓ RAM + Aurora Clone + 既存パッケージ再デプロイ =\\n'
        '  最小ダウンタイムで最速アカウント移行',
        fs=10, align="left"))

    write_diag('UDEMY-217', '\n'.join(body), w=1000, h=580)


# ==========================================================================
# UDEMY-220 (num=519) - Organizations + AD Connector + Identity Center + 権限セット
# ==========================================================================
def diag_udemy_220():
    body = [title_cell("UDEMY-220: Org 作成 + AD Connector + Identity Center + 権限セット (AD グループ紐付け)")]
    # Onprem AD
    body.append(box('onprem', 40, 70, 240, 180, 'オンプレミス', fill="#F5F5F5", stroke=C_DARK, fs=11))
    body.append(label('ad', 60, 105, 200, 40, 'Active Directory\\n(既存 従業員)', bold=True, fs=11))
    body.append(label('grp', 55, 160, 220, 80,
        'AD グループ:\\n  • IT-Admins\\n  • Developers\\n  • ReadOnly-Users', fs=10, align="left"))

    # AD Connector + Identity Center
    body.append(box('aws_mgmt', 320, 70, 340, 340, 'AWS 管理アカウント (新規作成)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 340, 100, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('org_l', 320, 155, 100, 15, 'Organizations', bold=True, fs=10))
    body.append(label('org_d', 320, 175, 100, 30, 'すべての機能\\n有効化', fs=9))

    body.append(aws_icon('adc', 470, 100, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
    body.append(label('adc_l', 450, 155, 100, 15, 'AD Connector', bold=True, fs=10))
    body.append(label('adc_d', 440, 175, 130, 30, 'IDソースとして\\n指定', fs=9))

    body.append(aws_icon('ic', 590, 100, 'mxgraph.aws4.single_sign_on', fill=C_RED))
    body.append(label('ic_l', 555, 155, 130, 15, 'IAM Identity Center', bold=True, fs=10))

    body.append(box('ps', 340, 220, 320, 180, 'Permission Sets (権限セット)', fill="#FFFFFF", stroke=C_BLUE, fs=10))
    body.append(label('ps_d', 355, 250, 300, 150,
        '• AdminAccess → AD グループ「IT-Admins」\\n\\n'
        '• PowerUserAccess → AD グループ「Developers」\\n\\n'
        '• ReadOnlyAccess → AD グループ「ReadOnly-Users」\\n\\n'
        '→ AD グループ ≡ 権限セット を IDaS で設定\\n    追加のIAM ユーザは一切作らない', fs=10, align="left"))

    # AWS account (single)
    body.append(box('acc', 700, 70, 260, 340, 'AWS アカウント (組織の本体)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    body.append(aws_icon('cons', 780, 110, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('cons_l', 760, 165, 100, 15, 'Management Console', bold=True, fs=10))
    body.append(label('acc_d', 720, 200, 220, 200,
        'IT 担当者は:\\n  ① AWS SSO ポータル へアクセス\\n  ② AD 資格情報 でログイン\\n  ③ 自分のAD グループに対応する\\n     権限セットで コンソール セッション開始\\n\\n'
        '→ IAM ユーザ や 長期アクセスキー は不要\\n→ パスワード変更は AD 側で 一元管理\\n→ MFA も Identity Center で強制可',
        fs=10, align="left"))

    # Arrows
    body.append(arrow('ar1', 'ad', 'adc', C_DARK, label_text="LDAP"))
    body.append(arrow('ar2', 'adc', 'ic', C_BLUE))
    body.append(arrow('ar3', 'ic', 'cons', C_GREEN, label_text="SSO"))

    # Key
    body.append(box('key', 40, 430, 920, 140, '🔑 重要: 単一アカウントでも「Organizations 有効化」が必要な理由', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 460, 900, 110,
        '✓ IAM Identity Center は Organizations の全機能モード が 前提\\n'
        '  → 単一アカウントであっても まず Organizations で 組織を作成 / 全機能を有効化\\n'
        '✓ AD Connector 選定理由: AWS 側にユーザDB複製なし → 運用コスト最小 (完全なマネージド AD 不要)\\n'
        '✗ IAM フェデレーション (SAML) 個別設定 = アカウントごとに IdP 設定が必要で 運用負荷増\\n'
        '✗ AWS Managed Microsoft AD = AWS 側に 新しいAD を作成 → 既存AD との二重管理', fs=10, align="left"))

    write_diag('UDEMY-220', '\n'.join(body), w=1000, h=600)


# ==========================================================================
# UDEMY-250 (num=549) - クロスアカウントS3 + KMS Grant + QuickSight IAMロール
# ==========================================================================
def diag_udemy_250():
    body = [title_cell("UDEMY-250: クロスアカウント S3 + KMS Grant (QuickSight が 営業S3を参照)")]
    # Sales account
    body.append(box('sales', 40, 70, 450, 470, '営業アカウント (S3所有)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('s3', 80, 110, 'mxgraph.aws4.s3', fill=C_GREEN))
    body.append(label('s3_l', 60, 165, 100, 15, 'S3 (営業データ)', bold=True, fs=10))
    body.append(label('s3_d', 55, 185, 120, 30, 'ペタバイト規模\\nSSE-KMS 暗号化', fs=9))

    body.append(aws_icon('kms', 240, 110, 'mxgraph.aws4.key_management_service', fill=C_RED))
    body.append(label('kms_l', 220, 165, 100, 15, 'KMS CMK', bold=True, fs=10))
    body.append(label('kms_d', 210, 185, 130, 50, 'カスタマー管理\\nキー (CMK)\\n暗号化キー', fs=9))

    body.append(box('bp', 60, 250, 420, 110, 'S3 バケットポリシー', fill="#FFFFFF", stroke=C_BLUE, fs=10))
    body.append(label('bp_t', 75, 280, 400, 80,
        '{"Effect": "Allow",\\n'
        ' "Principal":\\n'
        '   "arn:aws:iam::MarketingAcct:role/QS-Role",\\n'
        ' "Action": ["s3:GetObject", "s3:ListBucket"],\\n'
        ' "Resource": ["arn:aws:s3:::sales/*"]}', fs=9, align="left"))

    body.append(box('kp', 60, 370, 420, 150, 'KMS キーポリシー (Grant 必須!)', fill="#FFFFFF", stroke=C_RED, fs=10))
    body.append(label('kp_t', 75, 400, 400, 120,
        '{"Effect": "Allow",\\n'
        ' "Principal":\\n'
        '   "arn:aws:iam::MarketingAcct:role/QS-Role",\\n'
        ' "Action": ["kms:Decrypt",\\n'
        '            "kms:GenerateDataKey"]}\\n\\n'
        '⚠ これが無いと KMS 暗号化された S3 を復号できない', fs=9, align="left"))

    # Marketing account
    body.append(box('mkt', 530, 70, 430, 470, 'マーケティングアカウント (QuickSight)', fill="#F0F8E8", stroke=C_GREEN))
    body.append(aws_icon('qs', 580, 110, 'mxgraph.aws4.cloudwatch', fill=C_PINK))
    body.append(label('qs_l', 560, 165, 100, 15, 'QuickSight', bold=True, fs=10))

    body.append(aws_icon('qsrole', 740, 110, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
    body.append(label('qsrole_l', 720, 165, 120, 15, 'QS-Role (IAM)', bold=True, fs=10))

    body.append(box('qspol', 550, 220, 390, 160, 'QS-Role の IAM ポリシー', fill="#FFFFFF", stroke=C_GREEN, fs=10))
    body.append(label('qspol_t', 565, 250, 370, 130,
        '{"Effect": "Allow",\\n'
        ' "Action": [\\n'
        '   "s3:GetObject", "s3:ListBucket",\\n'
        '   "kms:Decrypt"\\n'
        ' ],\\n'
        ' "Resource": ["arn:aws:s3:::sales/*",\\n'
        '               "arn:aws:kms:*:SalesAcct:key/*"]}', fs=9, align="left"))

    body.append(box('qs_d', 550, 390, 390, 140, 'QuickSight 権限追加', fill="#FFFFFF", stroke=C_GREEN, fs=10))
    body.append(label('qs_d_t', 565, 420, 370, 110,
        'QuickSight 管理コンソールで\\n'
        '「マネージャー用の AWS リソース」で\\n'
        '対象 S3 バケットへのアクセスを有効化\\n\\n'
        'QuickSight → QS-Role → クロスアカウント →\\n'
        '営業アカウントの S3 + KMS で復号 → 分析',
        fs=9, align="left"))

    body.append(arrow_pts('ar1', 490, 300, 550, 300, C_ORANGE, width=3, label_text="Cross-Account Access"))

    write_diag('UDEMY-250', '\n'.join(body), w=1000, h=580)


# ==========================================================================
# UDEMY-259 (num=558) - Firewall Manager + Organizations の横断WAFルール管理
# ==========================================================================
def diag_udemy_259():
    body = [title_cell("UDEMY-259: AWS Firewall Manager + Organizations で 横断 WAF ルール管理")]
    # Management account
    body.append(box('mgmt', 40, 60, 920, 170, 'Management Account (Organizations + Firewall Manager 管理者)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 80, 80, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('org_l', 60, 135, 130, 15, 'Organizations', bold=True, fs=10))
    body.append(aws_icon('fm', 230, 80, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
    body.append(label('fm_l', 195, 135, 180, 15, 'AWS Firewall Manager', bold=True, fs=10))
    body.append(label('fm_d', 195, 155, 180, 80, 'WAF ポリシー定義\\n(組織横断)', fs=9))

    body.append(aws_icon('ssm', 410, 80, 'mxgraph.aws4.identity_and_access_management', fill=C_ORANGE))
    body.append(label('ssm_l', 380, 135, 160, 15, 'SSM Parameter Store', bold=True, fs=10))
    body.append(label('ssm_d', 380, 155, 180, 80, 'パラメータ:\\n  /fm/target-accounts\\n  /fm/target-ous', fs=9))

    body.append(aws_icon('eb', 580, 80, 'mxgraph.aws4.eventbridge', fill=C_PINK))
    body.append(label('eb_l', 560, 135, 130, 15, 'EventBridge ルール', bold=True, fs=10))
    body.append(label('eb_d', 560, 155, 180, 80, 'パラメータ変更を検知', fs=9))

    body.append(aws_icon('lam', 740, 80, 'mxgraph.aws4.lambda', fill=C_ORANGE))
    body.append(label('lam_l', 720, 135, 120, 15, 'Lambda 関数', bold=True, fs=10))
    body.append(label('lam_d', 720, 155, 180, 80, 'FM ポリシー更新\\n(add/remove)', fs=9))

    body.append(arrow('ar_ssm_eb', 'ssm', 'eb', C_PINK))
    body.append(arrow('ar_eb_lam', 'eb', 'lam', C_PINK))
    body.append(arrow('ar_lam_fm', 'lam', 'fm', C_ORANGE))

    # Target OUs
    body.append(box('ou1', 40, 260, 300, 240, 'OU A (Production)', fill="#F0F8E8", stroke=C_GREEN, fs=11))
    for i in range(4):
        col = i % 2
        row = i // 2
        x = 60 + col*130
        y = 300 + row*90
        body.append(aws_icon(f'pa{i}', x, y, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
        body.append(aws_icon(f'paw{i}', x+10, y+50, 'mxgraph.aws4.identity_and_access_management', fill=C_RED, w=25, h=25))
        body.append(label(f'paw{i}_l', x-15, y+75, 70, 15, 'WAF ACL', fs=8))
    body.append(label('ou1_d', 50, 465, 280, 30, 'FM が WAF ACL を 自動適用\\n(非準拠は自動修復)', fs=9, align="left", color=C_DARK))

    body.append(box('ou2', 360, 260, 300, 240, 'OU B (Staging)', fill="#FFEFD5", stroke=C_ORANGE, fs=11))
    for i in range(4):
        col = i % 2
        row = i // 2
        x = 380 + col*130
        y = 300 + row*90
        body.append(aws_icon(f'sa{i}', x, y, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
        body.append(aws_icon(f'saw{i}', x+10, y+50, 'mxgraph.aws4.identity_and_access_management', fill=C_RED, w=25, h=25))

    body.append(box('ou3', 680, 260, 280, 240, 'OU C (Development)', fill="#EBF1FF", stroke=C_BLUE, fs=11))
    for i in range(4):
        col = i % 2
        row = i // 2
        x = 700 + col*120
        y = 300 + row*90
        body.append(aws_icon(f'da{i}', x, y, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))

    body.append(arrow_pts('ar_fm_ou1', 280, 230, 200, 260, C_ORANGE, width=2))
    body.append(arrow_pts('ar_fm_ou2', 280, 230, 500, 260, C_ORANGE, width=2))
    body.append(arrow_pts('ar_fm_ou3', 280, 230, 820, 260, C_ORANGE, width=2))

    # Key
    body.append(box('key', 40, 520, 920, 120, '🔑 Firewall Manager の価値', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 550, 900, 90,
        '✓ FM = 組織横断で WAF / Security Group / Network Firewall / Shield を ポリシーとして適用\\n'
        '  非準拠リソースの 自動修復 (ポリシー再適用) が組み込み\\n'
        '✓ Parameter Store + EventBridge + Lambda で 対象アカウント/OU の動的変更を自動化\\n'
        '✗ 個別 AWS WAF を各アカウントで手作業 = スケールしない / 非準拠時の修復が自動化できない', fs=10, align="left"))

    write_diag('UDEMY-259', '\n'.join(body), w=1000, h=670)


# ==========================================================================
# UDEMY-267 (num=566) - Control Tower ランディングゾーン + OU別アクセス + MFA
# ==========================================================================
def diag_udemy_267():
    body = [title_cell("UDEMY-267: Control Tower + 4 OU (Dev/Stg/Prd/Shared) + MFA + 限定ネット接続")]
    # Management / Control Tower
    body.append(box('mgmt', 40, 60, 920, 90, 'Management Account', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('ct', 80, 75, 'mxgraph.aws4.control_tower', fill=C_RED))
    body.append(label('ct_l', 60, 130, 130, 15, 'AWS Control Tower', bold=True, fs=10))
    body.append(aws_icon('ic', 230, 75, 'mxgraph.aws4.single_sign_on', fill=C_RED))
    body.append(label('ic_l', 210, 130, 130, 15, 'IAM Identity Center', bold=True, fs=10))
    body.append(label('ic_d', 210, 150, 130, 30, '・MFA 必須 強制\\n・権限セット別割当', fs=9, color=C_BLUE))
    body.append(aws_icon('tgw', 400, 75, 'mxgraph.aws4.transit_gateway', fill=C_PINK))
    body.append(label('tgw_l', 380, 130, 130, 15, 'Shared Transit Gateway', bold=True, fs=10))
    body.append(label('mgmt_d', 550, 75, 400, 70,
        'Control Tower のランディングゾーン =\\n  Organizations + OU 構造 + Config + CloudTrail + Identity Center\\n  を自動セットアップ → マルチアカウント基盤を最短で構築', fs=10, align="left"))

    # OU boxes
    body.append(box('dev_ou', 40, 180, 215, 220, 'Dev OU', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    body.append(aws_icon('dev_a', 110, 215, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('dev_d', 55, 280, 190, 110,
        '・開発者向け\\n・Dev ↔ Stg アカウント間のみ\\n  TGW ルート で相互アクセス可\\n・Prd とは 分離', fs=10, align="left"))

    body.append(box('stg_ou', 275, 180, 215, 220, 'Staging OU', fill="#FFEFD5", stroke=C_ORANGE, fs=12))
    body.append(aws_icon('stg_a', 345, 215, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('stg_d', 290, 280, 190, 110,
        '・QA / UAT 環境\\n・Dev ↔ Stg 相互接続\\n・本番向け検証', fs=10, align="left"))

    body.append(box('prd_ou', 510, 180, 215, 220, 'Production OU', fill="#F0E8F8", stroke=C_PURPLE, fs=12))
    body.append(aws_icon('prd_a', 580, 215, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('prd_d', 525, 280, 190, 110,
        '・本番アカウント\\n・Shared Net + TGW 経由で\\n  全アカウントと通信可\\n・Dev/Stg からは直接アクセス×', fs=10, align="left"))

    body.append(box('sn_ou', 745, 180, 215, 220, 'Shared Network OU', fill="#EBF1FF", stroke=C_BLUE, fs=12))
    body.append(aws_icon('sn_a', 815, 215, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(aws_icon('sn_tgw', 815, 275, 'mxgraph.aws4.transit_gateway', fill=C_PINK, w=40, h=40))
    body.append(label('sn_d', 760, 330, 190, 60,
        '・TGW 管理 / DNS / PHZ\\n・全OU と接続可', fs=10, align="left"))

    # Connections
    body.append(arrow_pts('dev_stg', 255, 290, 275, 290, C_GREEN, label_text=""))
    body.append(arrow_pts('stg_prd', 490, 290, 510, 290, C_GREEN, label_text="×", width=1))
    body.append(arrow_pts('sn_all', 815, 180, 815, 160, C_BLUE))
    body.append(arrow_pts('sn_dev', 745, 230, 255, 230, C_BLUE, width=1, label_text="TGW"))
    body.append(arrow_pts('sn_prd', 745, 290, 725, 290, C_BLUE, width=1, label_text="TGW"))

    # Key
    body.append(box('key', 40, 420, 920, 170, '🔑 CT ランディングゾーン設計ポイント', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 450, 900, 140,
        '✓ Control Tower = Organizations + OU + 組織CloudTrail + AWS Config + Identity Center + 既定ガードレール を\\n'
        '  ボタン1つでセットアップ → 自力で組む よりも圧倒的に運用負荷が低い\\n'
        '✓ MFA 強制 = Identity Center 側で 権限セット付与時の MFA 必須化 を設定\\n'
        '✓ OU 別アクセス制御 = Dev/Stg は相互通信 / Prd はサービス通信のみ →\\n'
        '  TGW ルートテーブル + SCP で 実装 (プライベートネット維持)\\n'
        '✗ 個別に VPC Peering / 個別に IAM Identity Provider = ランディングゾーンの価値を活かせない', fs=10, align="left"))

    write_diag('UDEMY-267', '\n'.join(body), w=1000, h=620)


# ==========================================================================
# UDEMY-330 (num=629) - OU単位のTransit Gateway + RAM
# ==========================================================================
def diag_udemy_330():
    body = [title_cell("UDEMY-330: OU 単位の TGW + RAM → 同一 OU 内だけで VPC 間通信")]
    # Management / Org
    body.append(box('mgmt', 40, 60, 920, 70, 'Organization Root', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 80, 75, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
    body.append(label('org_l', 65, 120, 100, 15, 'Organizations', bold=True, fs=10))
    body.append(label('rule', 200, 70, 750, 60,
        'ネットワークアーキテクチャ要件:\\n'
        '  ✓ 同じ OU 内の VPC 同士は通信可能\\n'
        '  ✗ 異なる OU の VPC 間は通信不可', fs=10, align="left"))

    # Dev OU
    body.append(box('dev', 40, 150, 295, 430, 'Dev OU (100+ アカウント)', fill="#F0F8E8", stroke=C_GREEN, fs=11))
    body.append(box('dev_net', 55, 180, 260, 160, 'Dev ネット管理アカウント', fill="#FFFFFF", stroke=C_GREEN, fs=10))
    body.append(aws_icon('dev_tgw', 155, 205, 'mxgraph.aws4.transit_gateway', fill=C_PINK))
    body.append(label('dev_tgw_l', 125, 260, 120, 15, 'Dev 専用 TGW', bold=True, fs=10))
    body.append(aws_icon('dev_ram', 155, 290, 'mxgraph.aws4.resource_access_manager', fill=C_PURPLE, w=35, h=35))
    body.append(label('dev_ram_l', 130, 325, 120, 15, 'RAM → Dev OU 配下', fs=9, color=C_PURPLE))

    for i, y in enumerate([360, 430, 500]):
        body.append(box(f'dev_v{i}', 55, y, 260, 60, f'Dev VPC {i+1}', fill="#FFFFFF", stroke=C_GREEN, fs=9))
        body.append(aws_icon(f'dev_vi{i}', 70, y+10, 'mxgraph.aws4.vpc', fill=C_BLUE, w=35, h=35))
        body.append(label(f'dev_va{i}', 115, y+20, 190, 30, f'TGW アタッチメント (dev-tgw)', fs=9))

    # Stg OU
    body.append(box('stg', 355, 150, 295, 430, 'Staging OU (100+ アカウント)', fill="#FFEFD5", stroke=C_ORANGE, fs=11))
    body.append(box('stg_net', 370, 180, 260, 160, 'Stg ネット管理アカウント', fill="#FFFFFF", stroke=C_ORANGE, fs=10))
    body.append(aws_icon('stg_tgw', 470, 205, 'mxgraph.aws4.transit_gateway', fill=C_PINK))
    body.append(label('stg_tgw_l', 440, 260, 120, 15, 'Stg 専用 TGW', bold=True, fs=10))
    body.append(aws_icon('stg_ram', 470, 290, 'mxgraph.aws4.resource_access_manager', fill=C_PURPLE, w=35, h=35))
    body.append(label('stg_ram_l', 445, 325, 120, 15, 'RAM → Stg OU 配下', fs=9, color=C_PURPLE))

    for i, y in enumerate([360, 430, 500]):
        body.append(box(f'stg_v{i}', 370, y, 260, 60, f'Stg VPC {i+1}', fill="#FFFFFF", stroke=C_ORANGE, fs=9))
        body.append(aws_icon(f'stg_vi{i}', 385, y+10, 'mxgraph.aws4.vpc', fill=C_BLUE, w=35, h=35))
        body.append(label(f'stg_va{i}', 430, y+20, 190, 30, f'TGW アタッチメント (stg-tgw)', fs=9))

    # Prd OU
    body.append(box('prd', 670, 150, 295, 430, 'Production OU (100+ アカウント)', fill="#F0E8F8", stroke=C_PURPLE, fs=11))
    body.append(box('prd_net', 685, 180, 260, 160, 'Prd ネット管理アカウント', fill="#FFFFFF", stroke=C_PURPLE, fs=10))
    body.append(aws_icon('prd_tgw', 785, 205, 'mxgraph.aws4.transit_gateway', fill=C_PINK))
    body.append(label('prd_tgw_l', 755, 260, 120, 15, 'Prd 専用 TGW', bold=True, fs=10))
    body.append(aws_icon('prd_ram', 785, 290, 'mxgraph.aws4.resource_access_manager', fill=C_PURPLE, w=35, h=35))
    body.append(label('prd_ram_l', 760, 325, 120, 15, 'RAM → Prd OU 配下', fs=9, color=C_PURPLE))

    for i, y in enumerate([360, 430, 500]):
        body.append(box(f'prd_v{i}', 685, y, 260, 60, f'Prd VPC {i+1}', fill="#FFFFFF", stroke=C_PURPLE, fs=9))
        body.append(aws_icon(f'prd_vi{i}', 700, y+10, 'mxgraph.aws4.vpc', fill=C_BLUE, w=35, h=35))
        body.append(label(f'prd_va{i}', 745, y+20, 190, 30, f'TGW アタッチメント (prd-tgw)', fs=9))

    # Key
    body.append(box('key', 40, 600, 920, 110, '🔑 なぜ OU ごとに TGW を分けるのか', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 630, 900, 80,
        '✓ TGW は同じ TGW にアタッチされている VPC 間が 到達可能 (ルートテーブル設計)\\n'
        '✓ OU ごとに TGW を分ける = 物理的に異なる TGW → 異 OU への通信経路が存在しない\\n'
        '✓ RAM で TGW を OU に共有 → 同一 OU 内のアカウントが自アカウントで TGW アタッチメントを作れる\\n'
        '✗ 単一 TGW + ルートテーブル分割 でも実現可能だが、誤設定で異 OU 通信が発生するリスク', fs=10, align="left"))

    write_diag('UDEMY-330', '\n'.join(body), w=1000, h=730)


if __name__ == '__main__':
    diag_udemy_217()
    diag_udemy_220()
    diag_udemy_250()
    diag_udemy_259()
    diag_udemy_267()
    diag_udemy_330()
    print("Phase 3 done")
