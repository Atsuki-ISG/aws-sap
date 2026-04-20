#!/usr/bin/env python3
"""Generate drawio files for selected Udemy multi-account/Organizations questions - Part 2."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from generate_multiaccount_drawios import (
    aws_icon, label, box, arrow, arrow_pts, title_cell, write_diag,
    C_ORANGE, C_BLUE, C_GREEN, C_RED, C_PINK, C_PURPLE, C_DARK
)


# ==========================================================================
# UDEMY-112 (num=411) - Control Tower + CloudWatchログ中央集約
# ==========================================================================
def diag_udemy_112():
    body = [title_cell("UDEMY-112: 複数アカウントの CloudWatch Logs を中央監査アカウントに集約 (地域保持)")]
    # Control Tower
    body.append(box('ct_box', 40, 60, 920, 80, 'Management Account (AWS Control Tower ランディングゾーン)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('ct', 80, 80, 'mxgraph.aws4.control_tower', fill=C_RED))
    body.append(label('ct_l', 60, 135, 130, 15, 'Control Tower', bold=True, fs=10))
    body.append(label('ct_d', 230, 75, 720, 60,
        '・各メンバーアカウント用に組織トレイル / Log Archive アカウントを自動作成\\n・SCP + ガードレールでログ設定の強制',
        fs=10, align="left"))

    # Source accounts (region A, B)
    body.append(box('rA', 40, 160, 440, 260, 'リージョン A (例: ap-northeast-1)', fill="#F0F8E8", stroke=C_GREEN, fs=11))
    body.append(aws_icon('cwA', 60, 195, 'mxgraph.aws4.cloudwatch', fill=C_PINK))
    body.append(label('cwA_l', 50, 250, 80, 15, 'CloudWatch Logs', bold=True, fs=9))
    body.append(label('cwA_src', 50, 270, 80, 15, '(各アカウント)', fs=9))
    body.append(aws_icon('ksA', 180, 195, 'mxgraph.aws4.cloudwatch', fill=C_PURPLE))
    body.append(label('ksA_l', 155, 250, 130, 15, 'Subscription Filter', bold=True, fs=9))
    body.append(aws_icon('kA', 310, 195, 'mxgraph.aws4.eventbridge', fill=C_PINK))
    body.append(label('kA_l', 290, 250, 100, 15, 'Kinesis Data Streams\\n(監査アカウント)', fs=9))
    body.append(arrow_pts('arA1', 110, 220, 180, 220, C_GREEN))
    body.append(arrow_pts('arA2', 230, 220, 310, 220, C_GREEN))
    body.append(label('rA_n', 60, 300, 400, 120,
        '・各メンバーアカウントの CloudWatch Logs に Subscription Filter を設定\\n'
        '・送信先 = 監査アカウント (同一リージョン) の Kinesis Data Streams\\n'
        '・KMS 暗号化 + クロスアカウント権限 (送信先Kinesis の ResourcePolicy)\\n'
        '・ログは リージョン内 に留まる (規制要件)',
        fs=9, align="left"))

    body.append(box('rB', 500, 160, 460, 260, 'リージョン B (例: eu-west-1)', fill="#FFEFD5", stroke=C_ORANGE, fs=11))
    body.append(aws_icon('cwB', 520, 195, 'mxgraph.aws4.cloudwatch', fill=C_PINK))
    body.append(label('cwB_l', 510, 250, 80, 15, 'CloudWatch Logs', bold=True, fs=9))
    body.append(aws_icon('ksB', 640, 195, 'mxgraph.aws4.cloudwatch', fill=C_PURPLE))
    body.append(label('ksB_l', 615, 250, 130, 15, 'Subscription Filter', bold=True, fs=9))
    body.append(aws_icon('kB', 770, 195, 'mxgraph.aws4.eventbridge', fill=C_PINK))
    body.append(label('kB_l', 750, 250, 100, 15, 'Kinesis Data Streams', fs=9))
    body.append(arrow_pts('arB1', 570, 220, 640, 220, C_GREEN))
    body.append(arrow_pts('arB2', 690, 220, 770, 220, C_GREEN))
    body.append(label('rB_n', 520, 300, 420, 120,
        '・同じ仕組みをリージョン B でも展開\\n'
        '・各リージョン別に Kinesis を配置 → ログは生成リージョン内に留まる\\n'
        '・自動スケール (Kinesis Data Streams 容量モード=On-Demand)\\n'
        '・変動する負荷に追従',
        fs=9, align="left"))

    # Central audit
    body.append(box('audit', 40, 440, 920, 150, '中央監査アカウント (Log Archive)', fill="#F0E8F8", stroke=C_PURPLE, fs=12))
    body.append(aws_icon('lam', 80, 470, 'mxgraph.aws4.lambda', fill=C_ORANGE))
    body.append(label('lam_l', 60, 525, 100, 15, 'Lambda (正規化)', bold=True, fs=9))
    body.append(aws_icon('s3', 220, 470, 'mxgraph.aws4.s3', fill=C_GREEN))
    body.append(label('s3_l', 210, 525, 100, 15, 'S3 (保存)', bold=True, fs=9))
    body.append(aws_icon('sm', 360, 470, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
    body.append(label('sm_l', 340, 525, 130, 15, 'SIEM (オンプレ/外部)', bold=True, fs=9))
    body.append(arrow('aud1', 'lam', 's3', C_PURPLE))
    body.append(arrow('aud2', 's3', 'sm', C_PURPLE))
    body.append(label('aud_d', 510, 460, 430, 130,
        '・Kinesis → Lambda: 各地域共通フォーマットに正規化\\n'
        '・S3: 耐久性・長期保持・オブジェクトロックで改ざん防止\\n'
        '・SIEM: Kinesis または S3 からストリーミング出力\\n'
        '・Control Tower の Log Archive アカウントの位置付け',
        fs=10, align="left"))

    body.append(arrow_pts('ar_to_audit1', 340, 220, 200, 470, C_DARK))
    body.append(arrow_pts('ar_to_audit2', 800, 220, 200, 470, C_DARK))

    write_diag('UDEMY-112', '\n'.join(body), w=1000, h=620)


# ==========================================================================
# UDEMY-141 (num=440) - Organizations招待 + OrganizationAccountAccessRole
# ==========================================================================
def diag_udemy_141():
    body = [title_cell("UDEMY-141: Organizations 招待 + OrganizationAccountAccessRole で一元管理")]
    # Central
    body.append(box('central', 40, 70, 340, 380, '中央管理アカウント', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 150, 110, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('org_l', 90, 165, 240, 20, 'AWS Organizations (管理)', bold=True, fs=10))
    body.append(label('central_d', 60, 200, 300, 240,
        '① Organizations で中央管理アカウントを作成\\n'
        '② 既存の各事業部アカウントに 招待 (Invite) を送信\\n'
        '③ 各事業部が 招待を承諾\\n\\n'
        '請求の一元化 (Consolidated Billing):\\n'
        '  ・すべての事業部の請求が中央アカウントに集約\\n'
        '  ・ボリューム割引も組織全体で適用\\n\\n'
        'アクセスポリシー一元管理:\\n'
        '  ・SCP で制限を適用\\n'
        '  ・OrganizationAccountAccessRole で管理アクセス', fs=10, align="left"))

    # Arrow
    body.append(arrow_pts('ar1', 390, 200, 620, 200, C_BLUE, label_text="sts:AssumeRole"))

    # Member accounts
    body.append(box('mem', 620, 70, 340, 380, '各事業部メンバーアカウント', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    body.append(aws_icon('role', 640, 110, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
    body.append(label('role_l', 630, 165, 80, 15, 'OrganizationAccount\\nAccessRole', bold=True, fs=9))
    body.append(label('role_t', 740, 105, 200, 130,
        '信頼ポリシー:\\n  Principal:\\n    arn:aws:iam::中央acct:root\\n  Action: sts:AssumeRole\\n\\n'
        '権限ポリシー:\\n  AdministratorAccess\\n  (AWS 管理ポリシー)',
        fs=9, align="left"))

    # Member 1, 2, 3
    for i, y in enumerate([260, 330, 400]):
        body.append(aws_icon(f'biz{i}', 650, y, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
        body.append(label(f'biz{i}_l', 700, y+10, 250, 20, f'事業部 {i+1} アカウント (買収した人材紹介会社)', fs=10))

    # Key
    body.append(box('key', 40, 470, 920, 140, '🔑 招待 vs Control Tower vs 手動', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 500, 900, 110,
        '✓ 既存アカウントを組織に入れる = 「招待」方式 (InviteAccountToOrganization)\\n'
        '  → 招待を承諾する 必要がある (両方の同意)\\n'
        '✓ OrganizationAccountAccessRole = Organizations が作成/招待したメンバーに自動で作られる IAM ロール\\n'
        '  (管理アカウントからAssumeRoleで Admin 操作できる共通ロール)\\n'
        '  → 招待方式でも メンバーアカウントで 手動で作成する 必要がある (自動作成は Organizations 「作成」時のみ)\\n'
        '✗ 作成 vs 招待 の区別が問われる (招待では自動で作られない) — 試験頻出ポイント', fs=10, align="left"))

    write_diag('UDEMY-141', '\n'.join(body), w=1000, h=640)


# ==========================================================================
# UDEMY-147 (num=446) - OU分離 + 拒否SCP
# ==========================================================================
def diag_udemy_147():
    body = [title_cell("UDEMY-147: OU 分離 (本番/非本番) + 特定サービス拒否 SCP")]
    # Root
    body.append(box('root', 40, 60, 920, 70, 'Organization Root', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 80, 75, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
    body.append(label('org_l', 65, 120, 100, 15, 'Organizations', bold=True, fs=10))
    body.append(label('root_d', 200, 70, 750, 55,
        '✓ まず OU でアカウントを 製品ライン / 開発フェーズ 別に分離\\n'
        '✓ 次に OU 単位で SCP を適用 → 未使用/高コスト/リスクの高い AWS サービスを一括で Deny', fs=10, align="left"))

    # Prod OU
    body.append(box('prod', 40, 150, 440, 250, '本番 OU', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    body.append(label('scp_prod', 55, 180, 420, 180,
        'SCP (本番用):\\n'
        '{\\n'
        '  "Effect": "Deny",\\n'
        '  "Action": [\\n'
        '    "machinelearning:*",\\n'
        '    "iot:*",\\n'
        '    "glacier:*",\\n'
        '    "gamelift:*"\\n'
        '  ],\\n'
        '  "Resource": "*"\\n}',
        fs=10, align="left", color=C_RED))
    for i, x in enumerate([60, 160, 260, 360]):
        body.append(aws_icon(f'prd{i}', x, 360, 'mxgraph.aws4.organizations', fill=C_RED, w=35, h=35))

    # Non-prod OU
    body.append(box('nprod', 520, 150, 440, 250, '非本番 OU (開発/ステージング)', fill="#FFEFD5", stroke=C_ORANGE, fs=12))
    body.append(label('scp_nprod', 535, 180, 420, 180,
        'SCP (非本番用):\\n'
        '{\\n'
        '  "Effect": "Deny",\\n'
        '  "Action": [\\n'
        '    "directconnect:*",\\n'
        '    "route53domains:*"\\n'
        '  ],\\n'
        '  "Resource": "*"\\n}\\n(コストリスクの高い操作を拒否)',
        fs=10, align="left", color=C_RED))
    for i, x in enumerate([540, 640, 740, 840]):
        body.append(aws_icon(f'np{i}', x, 360, 'mxgraph.aws4.organizations', fill=C_RED, w=35, h=35))

    # Key
    body.append(box('key', 40, 420, 920, 130, '🔑 SCP の書き方パターン (許可リスト / 拒否リスト)', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 450, 900, 100,
        '✓ 拒否リスト方式 (Deny list): 既定で全許可 + 特定サービスのみ Deny → シンプル / 新サービスは自動で許可される\\n'
        '✓ 許可リスト方式 (Allow list): FullAWSAccess をデタッチ + Allow を明示列挙 → 厳格だが 新サービス出るたびに更新必要\\n'
        '✓ OU 単位で適用可能 → 本番/非本番 で異なる制限を持てる\\n'
        '✗ IAM ポリシーだけ では 組織横断の一括管理が不可 / ✗ 全部を root にまとめると 細かい制御ができない', fs=10, align="left"))

    write_diag('UDEMY-147', '\n'.join(body), w=1000, h=580)


# ==========================================================================
# UDEMY-161 (num=460) - ハブVPCサブネットをRAMでスポークアカウント共有
# ==========================================================================
def diag_udemy_161():
    body = [title_cell("UDEMY-161: インフラハブアカウントの VPC サブネットを RAM で各スポークアカウントに共有")]
    # Organizations/Management
    body.append(box('mgmt', 40, 60, 920, 70, 'Management Account (組織全体で信頼されたアクセスを有効化)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 80, 75, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
    body.append(label('org_l', 65, 120, 100, 15, 'Organizations', bold=True, fs=10))
    body.append(label('mgmt_d', 230, 80, 720, 45,
        '① RAM で 組織との信頼アクセス を有効化 → 招待不要でOU/アカウントに共有可能', fs=10, align="left", color=C_DARK))

    # Hub (Infra account)
    body.append(box('hub', 40, 160, 380, 380, 'インフラハブアカウント', fill="#FFEFD5", stroke=C_ORANGE, fs=12))
    body.append(aws_icon('vpc', 60, 190, 'mxgraph.aws4.vpc', fill=C_BLUE))
    body.append(label('vpc_l', 45, 245, 100, 15, '集約 VPC', bold=True, fs=10))
    # 4 subnets
    for i, y in enumerate([280, 340, 400, 460]):
        body.append(box(f'sn{i}', 60, y, 320, 50, f'Subnet AZ{(i%2)+1}  (10.0.{i}.0/24)', fill="#FFFFFF", stroke=C_BLUE, fs=10))
    body.append(aws_icon('ram', 290, 190, 'mxgraph.aws4.resource_access_manager', fill=C_PURPLE))
    body.append(label('ram_l', 260, 245, 120, 15, 'RAM リソース共有', bold=True, fs=10, color=C_PURPLE))

    # Arrows to spokes
    for i, y in enumerate([210, 300, 390]):
        body.append(arrow_pts(f'ar_sp{i}', 420, 215, 580, y, C_PURPLE))

    # Spoke accounts
    body.append(box('sp_box', 560, 160, 400, 380, 'スポークアカウント群 (アプリ運用)', fill="#F0F8E8", stroke=C_GREEN, fs=12))

    for i, y in enumerate([190, 280, 370]):
        body.append(box(f'spa{i}', 580, y, 360, 80, f'スポーク アカウント {i+1}', fill="#FFFFFF", stroke=C_GREEN, fs=10))
        body.append(aws_icon(f'ec2{i}', 600, y+15, 'mxgraph.aws4.ec2', fill=C_ORANGE, w=40, h=40))
        body.append(aws_icon(f'ecs{i}', 670, y+15, 'mxgraph.aws4.ecs', fill=C_ORANGE, w=40, h=40))
        body.append(aws_icon(f'lam{i}', 740, y+15, 'mxgraph.aws4.lambda', fill=C_ORANGE, w=40, h=40))
        body.append(label(f'spa{i}_d', 800, y+25, 130, 50, '共有されたサブネット\\n内でリソース作成\\n(ネット管理不要)', fs=9, align="left"))

    body.append(label('note', 560, 475, 400, 60,
        '・スポークアカウントは サブネット内で EC2/ECS/Lambda を作成できる\\n'
        '・VPC/Subnet 自体の 管理権限は付与されない → 中央でネット管理\\n'
        '・同一VPCに見えるのでレイテンシ最小', fs=9, align="left"))

    # Key
    body.append(box('key', 40, 560, 920, 110, '🔑 VPC Sharing (Shared VPC) の利点', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 590, 900, 80,
        '✓ ハブアカウントが Subnet を RAM で共有 → スポーク側は 自アカウントのように Subnet を参照できる\\n'
        '✓ Subnet / VPC 自体は ハブ側が所有 = ネットワーク管理を 中央に集約\\n'
        '✓ VPC ピアリングも Transit Gateway も不要 (同一 VPC 内扱い) → データ転送料も削減\\n'
        '✗ スポーク側で CIDR を作る → 管理分散 / ✗ 全員 PrivateLink → 用途がそもそも違う', fs=10, align="left"))

    write_diag('UDEMY-161', '\n'.join(body), w=1000, h=700)


# ==========================================================================
# UDEMY-171 (num=470) - IAM Identity Center + AD Connector + VPN
# ==========================================================================
def diag_udemy_171():
    body = [title_cell("UDEMY-171: オンプレAD を そのまま使う SSO (Identity Center + AD Connector)")]
    # On-prem
    body.append(box('onprem', 40, 70, 260, 300, 'オンプレミス', fill="#F5F5F5", stroke=C_DARK, fs=11))
    body.append(label('ad', 55, 100, 230, 40, 'Active Directory\\n(ユーザ/グループ の正本)', bold=True, fs=11))
    body.append(label('users', 60, 160, 220, 30, '• 人事データと同期済み\\n• MFA も AD 側で設定可', fs=10, align="left"))
    body.append(label('ad_grp', 60, 200, 220, 100,
        'AD グループ:\\n  • aws-admins\\n  • aws-dev-readonly\\n  • aws-db-ops\\n  (各 AWS アカウント/権限に紐付け)', fs=10, align="left"))

    # VPN
    body.append(aws_icon('vpn', 330, 200, 'mxgraph.aws4.site_to_site_vpn', fill=C_PURPLE))
    body.append(label('vpn_l', 310, 255, 100, 30, 'Site-to-Site\\nVPN', bold=True, fs=10))

    # AD Connector
    body.append(box('ic_box', 440, 70, 260, 300, 'Management Account', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('adc', 460, 105, 'mxgraph.aws4.identity_and_access_management', fill=C_RED))
    body.append(label('adc_l', 445, 160, 100, 15, 'AD Connector', bold=True, fs=10))
    body.append(label('adc_d', 445, 180, 100, 30, '(LDAP プロキシ)', fs=9))
    body.append(aws_icon('ic', 580, 105, 'mxgraph.aws4.single_sign_on', fill=C_RED))
    body.append(label('ic_l', 560, 160, 130, 15, 'IAM Identity Center', bold=True, fs=10))
    body.append(label('ic_ps', 460, 220, 220, 140,
        'Permission Set:\\n  • AdministratorAccess\\n  • ReadOnlyAccess\\n  • DatabaseOperator (custom)\\n\\n'
        'AD グループ → 権限セット → AWS アカウントへ\\n割当 (3者マッピング)',
        fs=10, align="left"))

    # AWS accounts
    body.append(box('accs', 740, 70, 220, 300, '組織内 AWS アカウント', fill="#F0F8E8", stroke=C_GREEN, fs=11))
    for i, y in enumerate([100, 175, 250, 325]):
        body.append(aws_icon(f'a{i}', 820, y, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
        body.append(label(f'a{i}_l', 790, y-20, 100, 15, f'アカウント{i+1}', fs=9))

    # Arrows
    body.append(arrow('ar1', 'ad', 'vpn', C_DARK))
    body.append(arrow('ar2', 'vpn', 'adc', C_PURPLE, label_text="LDAP over VPN"))
    body.append(arrow('ar3', 'adc', 'ic', C_BLUE))
    body.append(arrow('ar4', 'ic', 'a0', C_GREEN, label_text="SSO"))
    body.append(arrow('ar5', 'ic', 'a1', C_GREEN))
    body.append(arrow('ar6', 'ic', 'a2', C_GREEN))
    body.append(arrow('ar7', 'ic', 'a3', C_GREEN))

    # Key
    body.append(box('key', 40, 400, 920, 150, '🔑 AD Connector を選ぶ理由 (試験頻出)', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 430, 900, 120,
        '✓ AD Connector = 単なる「LDAPプロキシ」 → AWS 側にユーザDBを複製しない (最小運用)\\n'
        '✓ オンプレAD のパスワード変更/削除 が AWS 側に即時反映 (二重管理が発生しない)\\n'
        '✓ Identity Center の ID ソースに AD Connector を指定 → AD グループベースで権限セット割当\\n'
        '✗ AWS Managed Microsoft AD = AWS 側に新しいAD 作成 = 二重管理\\n'
        '✗ IAM ユーザを各アカウントに作成 = 一元管理不可\\n'
        '✗ Cognito = アプリ側 のID 基盤 で 管理アクセスには向かない', fs=10, align="left"))

    write_diag('UDEMY-171', '\n'.join(body), w=1000, h=580)


# ==========================================================================
# UDEMY-179 (num=478) - dept タグアクティベート + CUR + S3タグ別集計
# ==========================================================================
def diag_udemy_179():
    body = [title_cell("UDEMY-179: dept タグ → AWS Cost and Usage Report (CUR) による 部門別集計")]
    # Management
    body.append(box('mgmt', 40, 60, 920, 100, 'Management Account (Organizations)', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 80, 80, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('org_l', 60, 135, 130, 15, 'Organizations', bold=True, fs=10))
    body.append(label('tag_act', 230, 75, 710, 75,
        '① Billing コンソールで「ユーザ定義タグ」 dept をアクティベート\\n'
        '   (タグ作成から 最大24時間 でコスト配分タグとして利用可能に)\\n'
        '② CUR (Cost and Usage Report) を 管理アカウントの S3 に出力するよう設定',
        fs=10, align="left"))

    # Member account with tagged EC2
    body.append(box('mem', 40, 180, 440, 220, 'メンバーアカウント (事業部X)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    body.append(aws_icon('ec2_1', 70, 215, 'mxgraph.aws4.ec2', fill=C_ORANGE))
    body.append(label('ec2_1_l', 60, 270, 80, 15, 'EC2 (セキュリティツール)', fs=9, bold=True))
    body.append(label('tag_1', 60, 290, 180, 50, 'Tag: dept=compliance', fs=10, color=C_PURPLE, bold=True))
    body.append(aws_icon('ec2_2', 220, 215, 'mxgraph.aws4.ec2', fill=C_ORANGE))
    body.append(label('ec2_2_l', 210, 270, 80, 15, 'EC2 (業務アプリ)', fs=9))
    body.append(label('tag_2', 210, 290, 180, 50, 'Tag: dept=business', fs=10, color=C_DARK))
    body.append(aws_icon('rds', 370, 215, 'mxgraph.aws4.rds', fill=C_BLUE))
    body.append(label('rds_l', 360, 270, 80, 15, 'RDS (compliance)', fs=9))
    body.append(label('tag_3', 360, 290, 180, 50, 'Tag: dept=compliance', fs=10, color=C_PURPLE, bold=True))

    # S3 + Athena
    body.append(box('report', 520, 180, 440, 220, '管理アカウント: CUR 出力先', fill="#FFEFD5", stroke=C_ORANGE, fs=12))
    body.append(aws_icon('s3', 560, 215, 'mxgraph.aws4.s3', fill=C_GREEN))
    body.append(label('s3_l', 540, 270, 100, 15, 'S3 (CUR parquet)', bold=True, fs=9))
    body.append(aws_icon('ath', 700, 215, 'mxgraph.aws4.lambda', fill=C_ORANGE))
    body.append(label('ath_l', 680, 270, 120, 15, 'Athena / QuickSight', bold=True, fs=9))
    body.append(label('rep_q', 540, 300, 400, 90,
        'クエリ例:\\nSELECT resource_tags_user_dept, SUM(unblended_cost)\\nFROM cur\\nWHERE year=\'2026\' AND month=\'04\'\\nGROUP BY 1',
        fs=9, align="left"))

    body.append(arrow('ar1', 'mem', 's3', C_ORANGE, label_text="タグ付きコストが CUR に反映"))

    # Key
    body.append(box('key', 40, 420, 920, 140, '🔑 タグ別コスト精度を最大化する方法', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 450, 900, 110,
        '✓ CUR = 最も詳細なビリングデータ (1時間粒度 / リソース粒度 / タグ列)\\n'
        '  → 特定タグを持つリソースのコストだけを正確に抽出可能\\n'
        '✓ タグは 管理アカウントで「ユーザ定義タグ」として アクティベート が必須\\n'
        '✓ S3 + Athena + QuickSight で 可視化 / 事業部への配賦レポート\\n'
        '✗ Cost Explorer のみ = 日次粒度で 1年超の長期分析がしにくい\\n'
        '✗ Resource Groups / 手動リストは 正確な コスト集計にならない', fs=10, align="left"))

    write_diag('UDEMY-179', '\n'.join(body), w=1000, h=590)


# ==========================================================================
# UDEMY-184 (num=483) - OU × CUR + QuickSight 部門別可視化
# ==========================================================================
def diag_udemy_184():
    body = [title_cell("UDEMY-184: OU別 CUR + QuickSight 可視化 (部門別コスト内訳)")]
    # Management
    body.append(box('mgmt', 40, 60, 920, 90, 'Management Account', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 80, 75, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('org_l', 60, 130, 130, 15, 'Organizations', bold=True, fs=10))
    body.append(aws_icon('cur', 230, 75, 'mxgraph.aws4.config', fill=C_ORANGE))
    body.append(label('cur_l', 210, 130, 130, 15, 'Cost & Usage Report', bold=True, fs=10))
    body.append(aws_icon('s3c', 380, 75, 'mxgraph.aws4.s3', fill=C_GREEN))
    body.append(label('s3c_l', 360, 130, 130, 15, 'S3 (CUR parquet)', bold=True, fs=10))
    body.append(aws_icon('ath', 530, 75, 'mxgraph.aws4.lambda', fill=C_ORANGE))
    body.append(label('ath_l', 510, 130, 130, 15, 'Athena', bold=True, fs=10))
    body.append(aws_icon('qs', 680, 75, 'mxgraph.aws4.cloudwatch', fill=C_PINK))
    body.append(label('qs_l', 660, 130, 130, 15, 'QuickSight', bold=True, fs=10))
    body.append(arrow('ar_cur', 'cur', 's3c', C_ORANGE))
    body.append(arrow('ar_s3', 's3c', 'ath', C_ORANGE))
    body.append(arrow('ar_ath', 'ath', 'qs', C_PINK))

    # OU structure
    body.append(box('ou1', 40, 170, 440, 180, 'エンジニア部門OU A (各 OU が自分のコストを参照)', fill="#F0F8E8", stroke=C_GREEN, fs=11))
    for i, x in enumerate([60, 150, 240, 330]):
        body.append(aws_icon(f'oa{i}', x, 210, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
        body.append(label(f'oa{i}_l', x-10, 255, 60, 15, f'ACCT {i+1}', fs=9))
    body.append(label('ou1_d', 60, 285, 400, 60,
        'OU A: 数百アカウント\\n各アカウントのコストは CUR に集約', fs=10, align="left"))

    body.append(box('ou2', 520, 170, 440, 180, 'エンジニア部門OU B', fill="#FFEFD5", stroke=C_ORANGE, fs=11))
    for i, x in enumerate([540, 630, 720, 810]):
        body.append(aws_icon(f'ob{i}', x, 210, 'mxgraph.aws4.organizations', fill=C_RED, w=40, h=40))
        body.append(label(f'ob{i}_l', x-10, 255, 60, 15, f'ACCT {i+1}', fs=9))
    body.append(label('ou2_d', 540, 285, 400, 60,
        'OU B: 数百アカウント\\n各アカウントのコストは CUR に集約', fs=10, align="left"))

    # Dashboards
    body.append(box('dash', 40, 370, 920, 180, 'QuickSight ダッシュボード (OU別)', fill="#F0E8F8", stroke=C_PURPLE, fs=12))
    body.append(box('dashA', 60, 405, 420, 130, '【OU A 向け】月次コスト推移 / サービス別内訳', fill="#FFFFFF", stroke=C_PURPLE, fs=10))
    body.append(label('dashA_d', 75, 435, 400, 100,
        '・PAYER_ACCOUNT_ID / LINKED_ACCOUNT フィルタで\\n  自OU アカウントだけを抽出\\n・TOP サービス別棒グラフ\\n・ボーディング向け要約ビュー', fs=10, align="left"))
    body.append(box('dashB', 500, 405, 440, 130, '【OU B 向け】同様のダッシュボード', fill="#FFFFFF", stroke=C_PURPLE, fs=10))
    body.append(label('dashB_d', 515, 435, 420, 100,
        '・Row-Level Security (RLS) で 他OU のデータは見せない\\n・経理部門は全OU 横断ビュー可能\\n・CSV エクスポートで社内レポート化', fs=10, align="left"))

    # Key
    body.append(box('key', 40, 570, 920, 80, '🔑 部門別コスト可視化の王道', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 595, 900, 50,
        '✓ CUR → S3 → Athena → QuickSight (標準パイプライン)\\n'
        '✗ CloudWatch メトリクスだけ = 詳細な個別リソース粒度なし / ✗ 各アカウント個別に CSV ダウンロード = 手作業', fs=10, align="left"))

    write_diag('UDEMY-184', '\n'.join(body), w=1000, h=680)


# ==========================================================================
# UDEMY-188 (num=487) - CloudFormation StackSets + サービスマネージド + 自動デプロイ
# ==========================================================================
def diag_udemy_188():
    body = [title_cell("UDEMY-188: CloudFormation StackSets (組織サービスマネージド + 自動デプロイ)")]
    # Mgmt
    body.append(box('mgmt', 40, 60, 920, 180, 'Management Account', fill="#EBF1FF", stroke=C_BLUE))
    body.append(aws_icon('org', 80, 80, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('org_l', 60, 135, 130, 15, 'Organizations', bold=True, fs=10))
    body.append(label('ta', 55, 155, 140, 80, '「信頼されたアクセス」有効\\n(StackSets と統合)', fs=9, color=C_DARK))

    body.append(aws_icon('ss', 240, 80, 'mxgraph.aws4.cloudtrail', fill=C_RED))
    body.append(label('ss_l', 210, 135, 180, 15, 'CloudFormation StackSets', bold=True, fs=10))
    body.append(label('ss_d', 210, 155, 200, 80,
        '・サービス管理の権限 (Org連携)\\n・自動デプロイ: 新アカウント作成時\\n  自動でスタックインスタンス展開\\n・OU を 対象に指定可能', fs=9, align="left"))

    body.append(aws_icon('tpl', 460, 80, 'mxgraph.aws4.cloudtrail', fill=C_BLUE))
    body.append(label('tpl_l', 430, 135, 180, 15, 'CloudFormation Template', bold=True, fs=10))
    body.append(label('tpl_d', 430, 155, 200, 80,
        'Resources:\\n  SecurityTopic:\\n    Type: AWS::SNS::Topic\\n  (サードパーティアラート連携)', fs=9, align="left"))

    body.append(aws_icon('tgt', 680, 80, 'mxgraph.aws4.organizations', fill=C_RED))
    body.append(label('tgt_l', 660, 135, 150, 15, 'Deploy Target: OU', bold=True, fs=10))
    body.append(label('tgt_d', 660, 155, 230, 80,
        'Deploy Option:\\n  ・Organization へデプロイ\\n  ・自動デプロイ ON\\n  ・新規アカウントでも自動展開', fs=9, align="left"))

    body.append(arrow('ar_ss', 'ss', 'tpl', C_BLUE))
    body.append(arrow('ar_tpl', 'tpl', 'tgt', C_ORANGE))

    # Member accounts
    body.append(box('mem', 40, 270, 920, 230, '組織配下 すべての メンバーアカウント (既存 + 新規)', fill="#F0F8E8", stroke=C_GREEN, fs=12))
    for i in range(8):
        col = i % 4
        row = i // 4
        x = 80 + col*220
        y = 310 + row*90
        body.append(box(f'ma{i}', x, y, 200, 70, f'アカウント {i+1}', fill="#FFFFFF", stroke=C_GREEN, fs=9))
        body.append(aws_icon(f'sns{i}', x+10, y+15, 'mxgraph.aws4.sns', fill=C_RED, w=40, h=40))
        body.append(label(f'sns{i}_l', x+55, y+25, 140, 30, 'SNS Topic\\n(スタックセット展開)', fs=9, align="left"))

    # Key
    body.append(box('key', 40, 520, 920, 130, '🔑 StackSets の 2種類の権限モデル', fill="#FFF9E6", stroke=C_ORANGE, fs=11))
    body.append(label('key_t', 55, 550, 900, 100,
        '✓ サービス管理権限 (Service-managed) = Organizations と統合 → 自動デプロイで 新規アカウントにも自動展開\\n'
        '  → 信頼されたアクセスを有効にして「組織へのデプロイ」を選択 (OU / 組織全体)\\n'
        '✗ セルフ管理権限 (Self-managed) = 各ターゲットアカウントに AWSCloudFormationStackSetExecutionRole を\\n'
        '  手動で用意する必要がある → 1500+ アカウントだと現実的でない\\n'
        '✓ 自動デプロイ を ON にすると、アカウントが OU に追加された瞬間にスタックインスタンスが自動作成される', fs=10, align="left"))

    write_diag('UDEMY-188', '\n'.join(body), w=1000, h=680)


if __name__ == '__main__':
    diag_udemy_112()
    diag_udemy_141()
    diag_udemy_147()
    diag_udemy_161()
    diag_udemy_171()
    diag_udemy_179()
    diag_udemy_184()
    diag_udemy_188()
    print("Phase 2 done")
