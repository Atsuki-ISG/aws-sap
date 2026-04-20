#!/usr/bin/env python3
"""
SAP-C02 questions.json: マルチアカウント設計テーマの解説を品質チェック+加筆。

仕様:
- tags に "multi-account" を含む、または問題文/選択肢に SCP/Organizations/OU/Control Tower/
  クロスアカウント/IAM Identity Center/委任管理 等のキーワードを含む問題が対象。
- detail のみ更新可能。answer/question/choices/id/num/tags/source は触らない。
- 末尾に <br><br>📌 判断ポイント<br>... の形式で「判断ポイント」セクションを追加。
- 元のスタイル(<p>系/<br>系) に応じて整形を合わせる。
- 明らかな技術的誤りがあれば修正（パターンマッチで検出）。
- 書き込み直前に再読み込みし、対象問題のみ差し替えて保存。
"""

import json
import re
from pathlib import Path

QUESTIONS_PATH = Path('/Users/aki/aws-sap/docs/data/questions.json')


# ============================================================
# 1. 対象問題判定
# ============================================================

def get_choice_text(c):
    if isinstance(c, dict):
        return c.get('text', '')
    return str(c)


def has_multi_account_keyword(text):
    if not text:
        return False
    jp_kw = [
        'サービスコントロールポリシー', 'クロスアカウント', 'アカウント分離',
        '委任管理', 'タグポリシー', 'バックアップポリシー',
        'ランディングゾーン', 'マルチアカウント', 'アカウントファクトリー',
        '委任管理者',
    ]
    for kw in jp_kw:
        if kw in text:
            return True
    patterns = [
        r'\bSCP\b', r'\bSCPs\b', r'Service Control Polic',
        r'\bOrganizations\b', r'\bOU\b', r'\bOUs\b',
        r'organizational unit',
        r'Control Tower', r'IAM Identity Center',
        r'Delegated Administrator',
        r'AWS SSO', r'AWS RAM', r'Resource Access Manager',
        r'Account Factory', r'Landing Zone', r'landing zone',
        r'multi-account', r'multi account',
        r'tag polic', r'backup polic', r'org trail',
        r'Organization Trail', r'org-level',
    ]
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False


def find_targets(data):
    targets = []
    for q in data:
        tags = q.get('tags', [])
        has_tag = isinstance(tags, list) and 'multi-account' in tags
        text_blob = q.get('question', '') + '\n'
        for c in q.get('choices', []):
            text_blob += get_choice_text(c) + '\n'
        if has_tag or has_multi_account_keyword(text_blob):
            targets.append(q['id'])
    return targets


# ============================================================
# 2. テーマ分類（どの判断ポイントテンプレを当てるか）
# ============================================================

def classify_topics(q):
    """問題文と選択肢からテーマフラグの集合を返す"""
    blob = q.get('question', '') + '\n'
    for c in q.get('choices', []):
        blob += get_choice_text(c) + '\n'
    blob_lower = blob.lower()

    topics = set()

    # SCP
    if (re.search(r'\bSCP\b', blob) or re.search(r'\bSCPs\b', blob)
            or 'Service Control Polic' in blob or 'サービスコントロールポリシー' in blob):
        topics.add('scp')

    # AWS Organizations 一般機能（CloudTrail org trail, tag policies, backup policies）
    if 'タグポリシー' in blob or 'tag polic' in blob_lower:
        topics.add('tag_policy')
    if 'バックアップポリシー' in blob or 'backup polic' in blob_lower:
        topics.add('backup_policy')
    if ('CloudTrail' in blob and ('Organization' in blob or '組織' in blob)) \
            or 'org trail' in blob_lower or 'organization trail' in blob_lower:
        topics.add('org_trail')

    # Control Tower / Landing Zone / Account Factory
    if ('Control Tower' in blob or 'Landing Zone' in blob or 'landing zone' in blob
            or 'ランディングゾーン' in blob or 'Account Factory' in blob
            or 'アカウントファクトリー' in blob):
        topics.add('control_tower')

    # IAM Identity Center / SSO
    if ('IAM Identity Center' in blob or 'AWS SSO' in blob
            or 'シングルサインオン' in blob or 'SSO' in blob):
        topics.add('idc')

    # AWS RAM
    if ('AWS RAM' in blob or 'Resource Access Manager' in blob
            or 'リソース共有' in blob or 'ResourceShare' in blob):
        topics.add('ram')

    # クロスアカウント (リソースポリシー / AssumeRole)
    if ('クロスアカウント' in blob or 'cross-account' in blob_lower
            or 'cross account' in blob_lower
            or 'AssumeRole' in blob or 'リソースポリシー' in blob
            or 'resource policy' in blob_lower or 'バケットポリシー' in blob
            or 'KMS' in blob and ('共有' in blob or '別アカウント' in blob)):
        topics.add('cross_account')

    # 委任管理
    if ('委任管理' in blob or '委任管理者' in blob
            or 'Delegated Administrator' in blob or 'delegated admin' in blob_lower):
        topics.add('delegated_admin')

    # Organizations OU 階層
    if (re.search(r'\bOU\b', blob) or re.search(r'\bOUs\b', blob)
            or 'organizational unit' in blob_lower or '組織単位' in blob):
        topics.add('ou')

    # Organizations 一般（OU 言及がなくとも Organizations 自体に触れている）
    if (re.search(r'\bOrganizations\b', blob) or 'AWS Organizations' in blob
            or '組織アカウント' in blob or '管理アカウント' in blob
            or 'メンバーアカウント' in blob or '組織全体' in blob):
        topics.add('organizations')

    # Service Catalog（マルチアカウント文脈で頻出）
    if 'Service Catalog' in blob or 'サービスカタログ' in blob:
        topics.add('service_catalog')

    # フェデレーション (SAML, OIDC, IdP)
    if ('SAML' in blob or 'OIDC' in blob or 'IdP' in blob
            or 'フェデレーション' in blob or 'federation' in blob_lower):
        topics.add('federation')

    return topics


# ============================================================
# 3. 判断ポイントテンプレート
# ============================================================

# 各テーマの「判断ポイント」本文（HTMLフラグメント、外側の包装はあとで）
TIPS = {
    'scp': (
        "<b>SCP（Service Control Policy）の核心:</b><br>"
        "・SCP は <b>権限を付与しない</b>。OU/アカウント内の IAM プリンシパルが行使できる<b>最大権限の境界（ガードレール）</b>を定義する。<br>"
        "・実効権限 = <code>SCP_Allow ∩ IAM_Allow</code>。SCP に Allow があっても IAM 側で許可しないと使えない。<br>"
        "・<b>明示的 Deny は IAM Allow を上書き</b>する。逆方向の上書きは不可。<br>"
        "・<b>許可リスト戦略</b>（FullAWSAccess を外して Allow のみの SCP を当てる）と <b>拒否リスト戦略</b>（FullAWSAccess を残し Deny を追加）の使い分けを意識。<br>"
        "・SCP は <b>管理アカウント自身には適用されない</b>。サービスリンクロール、ルートユーザーアクションの一部にも例外あり。<br>"
        "<b>引っ掛け:</b> 「SCP に s3:* を Allow したのに使えない」→ IAM 側で許可していない/FullAWSAccess を外していない、が定番。"
    ),
    'tag_policy': (
        "<b>Tag Policies（タグポリシー）:</b><br>"
        "・Organizations の機能で、<b>タグキー/値の標準化（命名規則・大文字小文字・許可値）</b>を強制。<br>"
        "・<b>違反タグの作成自体をブロックするには、SCP 側で <code>aws:RequestTag</code> 条件付き Deny が必要</b>（タグポリシー単体では準拠状況の検出が中心）。<br>"
        "・既存の不正タグの是正は手動 or 自動化（Config + SSM 等）。"
    ),
    'backup_policy': (
        "<b>Backup Policies（バックアップポリシー）:</b><br>"
        "・Organizations の機能で、AWS Backup のバックアッププランを <b>OU 単位で集中強制</b>。<br>"
        "・各メンバーアカウントで個別にバックアッププランを作る運用を、組織レベルで統一できる。<br>"
        "・対象サービスは AWS Backup がサポートするものに限る（EBS/EFS/RDS/DynamoDB/Storage Gateway 等）。"
    ),
    'org_trail': (
        "<b>CloudTrail Organization Trail:</b><br>"
        "・管理アカウント or 委任管理アカウントで作成すると、<b>全メンバーアカウントのイベントを自動収集</b>。<br>"
        "・メンバーアカウント側からは <b>削除・無効化できない</b>（証跡保護）。<br>"
        "・ログ集約用の S3 バケット/KMS キーへのクロスアカウント書き込み許可がポリシーで必要。<br>"
        "<b>引っ掛け:</b> 各アカウントで個別に証跡を作る案は「管理工数が増える/抜け漏れリスク」で外れる。"
    ),
    'control_tower': (
        "<b>AWS Control Tower の役割:</b><br>"
        "・<b>マルチアカウントのランディングゾーンを自動構築</b>するマネージドサービス。Organizations + SSO + Config + CloudTrail + S3 を組み合わせて初期設定。<br>"
        "・<b>ガードレール</b>: 予防的（SCPで実装）と発見的（AWS Configルールで実装）の2種。必須/強く推奨/選択的の3レベル。<br>"
        "・<b>Account Factory</b>: 標準化されたアカウントを Service Catalog 経由でセルフサービス払い出し。<br>"
        "・<b>カスタマイズ</b>: CfCT (Customizations for Control Tower) で CloudFormation/SCP の追加が可能。<br>"
        "<b>引っ掛け:</b> 「ゼロから組織設計」なら Control Tower、「既存組織への部分適用」なら Organizations + 個別設定の方が柔軟なケースもある。"
    ),
    'idc': (
        "<b>IAM Identity Center (旧 AWS SSO):</b><br>"
        "・<b>Organizations 配下の全アカウントへのフェデレーション SSO を一元化</b>。permission set をアカウント×グループにマッピング。<br>"
        "・ID ソースは内蔵ディレクトリ / Active Directory / 外部 IdP（Okta/Azure AD 等の SAML/SCIM）。<br>"
        "・各アカウントには permission set に応じた <b>IAM ロールが自動作成</b>される（手動ロール作成不要）。<br>"
        "<b>引っ掛け:</b><br>"
        "・「IAM ユーザーを各アカウントに作る案」は最小権限・運用工数の観点でほぼ不正解。<br>"
        "・SAML 直接連携（旧来パターン）と IAM Identity Center の使い分け: Organizations を使うなら IDC が標準解。"
    ),
    'ram': (
        "<b>AWS RAM (Resource Access Manager):</b><br>"
        "・<b>特定リソース（VPC サブネット、Transit Gateway、Route 53 Resolver ルール、License Manager、Aurora 等）を別アカウントに共有</b>。<br>"
        "・Organizations と統合すると <b>OU/組織全体に一括共有</b>可能（招待不要）。<br>"
        "・SCP は「禁止」、RAM は「共有」。役割が異なる。<br>"
        "<b>引っ掛け:</b><br>"
        "・「VPC を共有したい」→ RAM (Shared VPC)。各アカウントで VPC ピアリング/Transit Gateway を別建てする案より低コスト。<br>"
        "・S3/DynamoDB は RAM 対象外 → リソースベースポリシーで共有する。"
    ),
    'cross_account': (
        "<b>クロスアカウントアクセスの設計パターン:</b><br>"
        "・<b>IAM ロール + AssumeRole</b>: もっとも汎用的。信頼ポリシーで委任元アカウント/プリンシパルを指定。<br>"
        "・<b>リソースベースポリシー</b>（S3 バケットポリシー、KMS キーポリシー、Lambda リソースポリシー、SQS/SNS、ECR 等）: 別アカウントの Principal を直接記述可能。<br>"
        "・<b>クロスアカウント KMS</b>: キーポリシーで利用側アカウントを許可 + 利用側 IAM でも kms 権限が必要（両方必須）。<br>"
        "・S3 でクロスアカウント書き込みされたオブジェクトは <b>所有者が書き込んだアカウントのまま</b>になりやすい → <b>Bucket Owner Enforced (Object Ownership)</b> で所有権を統一。<br>"
        "<b>引っ掛け:</b> 「リソース所有アカウントの IAM だけ許可」では不足。リソースポリシー側でも明示許可が必要なサービスが多い。"
    ),
    'delegated_admin': (
        "<b>Delegated Administrator（委任管理者）:</b><br>"
        "・特定のサービス（Security Hub / GuardDuty / Config / Macie / Detective / IAM Access Analyzer / CloudTrail / Backup / Service Catalog / Audit Manager 等）の組織レベル管理を、<b>管理アカウント以外のメンバーアカウントに委任</b>できる仕組み。<br>"
        "・ベストプラクティスは <b>管理アカウントを請求/最小操作に限定</b>し、<b>セキュリティ運用は委任先（例: Security アカウント）</b>に寄せる。<br>"
        "<b>引っ掛け:</b> 「管理アカウントで全部やる」案はベストプラクティス違反として除外されやすい。"
    ),
    'ou': (
        "<b>OU 設計の基本:</b><br>"
        "・OU は <b>SCP 適用の単位</b>。本番/非本番、ワークロード/共有/Sandbox/Security/Log Archive など <b>用途ごとに分割</b>するのが定石。<br>"
        "・SCP は <b>OU から子 OU/アカウントへ継承</b>される。継承された Deny は外せない。<br>"
        "・Control Tower の標準 OU 構成: Security OU（Log Archive + Audit）、Sandbox OU、Workloads OU など。"
    ),
    'service_catalog': (
        "<b>Service Catalog のマルチアカウント運用:</b><br>"
        "・<b>標準化されたインフラ（CloudFormation テンプレ）をポートフォリオ化し、利用者にセルフサービス提供</b>。<br>"
        "・<b>起動制約（Launch Constraint）</b>で「実行時に引き受けるロール」を指定 → 利用者には Service Catalog 操作権限のみ付与で OK（リソース作成権限を直接渡さない）。<br>"
        "・Organizations と統合してポートフォリオを <b>OU/組織全体に共有</b>可能。<br>"
        "<b>引っ掛け:</b> 「テスターに CloudFormation/EC2 権限をフルで渡す」案は最小権限違反。"
    ),
    'organizations': (
        "<b>AWS Organizations の主要機能（俯瞰）:</b><br>"
        "・<b>一括請求（Consolidated Billing）</b>: 管理アカウントに請求集約。ボリュームディスカウントや RI/SP の組織内シェアが効く。<br>"
        "・<b>SCP / Tag Policy / Backup Policy / AI Services Opt-out Policy</b>: OU 単位のガバナンス。<br>"
        "・<b>サービスへの「Trusted access」</b>: Organizations と統合可能なサービス（CloudTrail / Config / Security Hub / GuardDuty / RAM / Service Catalog 等）で組織機能が解放される。<br>"
        "・<b>アカウントの作成/招待/移動</b>: 別組織への移動は <b>旧組織からの除外 → 招待 → 受諾</b> の手順（直接移動は不可）。<br>"
        "・<b>Cost Allocation Tags + AWS Cost Explorer / AWS Budgets</b>: 部門別コスト配賦と予算アラート。<br>"
        "<b>引っ掛け:</b><br>"
        "・「アカウントを別組織に直接移動」はできない。一旦切り離して招待し直す必要がある。<br>"
        "・部門別コスト把握は「タグ + Cost Allocation Tags の有効化 + Cost Explorer / CUR」が定番。"
    ),
    'federation': (
        "<b>外部 IdP フェデレーション (SAML / OIDC):</b><br>"
        "・Organizations 配下なら <b>IAM Identity Center 経由</b>が現代の標準（permission set + 自動ロール作成）。<br>"
        "・直接 SAML 連携する場合: 各アカウントに <b>SAML プロバイダーを登録</b> + IAM ロールの信頼ポリシーで SAML プロバイダー ARN をプリンシパル指定 + IdP 側で <code>https://signin.aws.amazon.com/saml</code> 宛の SAML アサーションに <b>Role 属性</b>を含める。<br>"
        "・呼ばれる API は <code>AssumeRoleWithSAML</code>（OIDC は <code>AssumeRoleWithWebIdentity</code>）。<br>"
        "<b>引っ掛け:</b> SAML フェデレーションでは <b>IAM ユーザーを使わない</b>。テストユーザーに IAM ユーザーで権限を付ける選択肢は外れる。"
    ),
}

# テーマ間の優先度（多すぎると冗長になるので、最大3テーマに絞る）
TOPIC_PRIORITY = [
    'scp',           # SCP は最重要
    'control_tower',
    'idc',
    'ram',
    'cross_account',
    'delegated_admin',
    'org_trail',
    'tag_policy',
    'backup_policy',
    'federation',
    'service_catalog',
    'organizations',  # 一般 Organizations 機能
    'ou',
]


def select_topics(topics):
    """優先度順に最大3つまで採用"""
    picked = []
    for t in TOPIC_PRIORITY:
        if t in topics:
            picked.append(t)
        if len(picked) >= 3:
            break
    return picked


# ============================================================
# 4. 既存解説のサニティチェック・修正
# ============================================================

# パターンマッチで明確な誤りを修正する
ERROR_PATTERNS = [
    # 「SCP は権限を付与する」と書かれていたら誤り
    # ただし「SCP は権限を付与しない」と否定しているのは OK なので慎重に
]


def fix_known_errors(detail):
    """明らかな技術的誤りを修正。修正があれば (new_detail, True) を返す。"""
    fixed = detail
    changed = False

    # 1. typo: "ある" の重複（"必要があある" など）
    for bad, good in [
        ('必要があある', '必要がある'),
        ('統合でる。', '統合できる。'),
        ('統合でる</p>', '統合できる</p>'),
        ('できなお。', 'できない。'),
        ('できなお</p>', 'できない</p>'),
    ]:
        if bad in fixed:
            fixed = fixed.replace(bad, good)
            changed = True

    return fixed, changed


# ============================================================
# 5. 判断ポイント挿入
# ============================================================

def build_tip_block(picked_topics, style):
    """選択テーマの判断ポイントブロックを HTML として組み立てる"""
    if not picked_topics:
        return ''
    sections = [TIPS[t] for t in picked_topics]
    body = '<br><br>'.join(sections)

    # 共通チェックリスト
    checklist = (
        "<br><br><b>試験で迷ったときのチェックリスト:</b><br>"
        "1. <b>「禁止/制限」</b>か <b>「許可/共有」</b>か → 禁止なら SCP、許可ならリソースポリシー/RAM/IAM。<br>"
        "2. <b>「組織横断」</b>か <b>「単一アカウント」</b>か → 組織横断なら Organizations + IDC + Control Tower 系を疑う。<br>"
        "3. <b>「IAM ユーザーを各アカウントに作る」案はほぼ不正解</b>。集中管理 + フェデレーション/AssumeRole が現代標準。<br>"
        "4. <b>「管理アカウントで全部運用」案はベストプラクティス違反</b>。Security/Log Archive/Audit などに委任管理。"
    )

    full = "📌 判断ポイント — マルチアカウント設計<br><br>" + body + checklist

    if style == 'p':
        return f'<p><br></p><p>{full}</p>'
    else:  # br style
        return f'<br><br>{full}'


def detect_style(detail):
    """元の detail のスタイルを判定: 'p' or 'br'"""
    if '<p>' in detail:
        return 'p'
    return 'br'


# ============================================================
# 6. メイン処理
# ============================================================

def main():
    # 対象抽出は元データから
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        data_for_targets = json.load(f)
    targets = find_targets(data_for_targets)
    target_set = set(targets)

    # 各対象問題に対する更新内容を構築
    updates = {}  # id -> new_detail
    fixed_count = 0

    for q in data_for_targets:
        if q['id'] not in target_set:
            continue
        det = q.get('explanation', {}).get('detail', '')
        if not det:
            continue
        # 既存に「判断ポイント」がある場合でも、マルチアカウント観点のテンプレが
        # 含まれていなければ追記する（テーマ別の補強）
        multi_acct_markers = [
            'SCP（Service Control Policy）の核心',
            'AWS Organizations の主要機能（俯瞰）',
            'AWS Control Tower の役割',
            'IAM Identity Center (旧 AWS SSO)',
            'AWS RAM (Resource Access Manager)',
            'Delegated Administrator（委任管理者）',
            'クロスアカウントアクセスの設計パターン',
            'OU 設計の基本',
            'Service Catalog のマルチアカウント運用',
            'CloudTrail Organization Trail',
            'Tag Policies（タグポリシー）',
            'Backup Policies（バックアップポリシー）',
            '外部 IdP フェデレーション',
        ]
        if any(m in det for m in multi_acct_markers):
            # 既にマルチアカウント観点のテンプレあり → スキップ
            continue

        new_det, did_fix = fix_known_errors(det)
        if did_fix:
            fixed_count += 1

        topics = classify_topics(q)
        picked = select_topics(topics)
        # 何もテーマが拾えなかった場合のフォールバック
        if not picked:
            picked = ['ou']  # 最低でも OU 設計

        style = detect_style(det)
        tip_block = build_tip_block(picked, style)
        new_det = new_det + tip_block
        updates[q['id']] = new_det

    print(f'対象: {len(targets)} 問')
    print(f'更新生成: {len(updates)} 問')
    print(f'明示的誤り修正: {fixed_count} 問')

    # ===== 書き込み直前に再読み込みし、対象のみ差し替え =====
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    applied = 0
    for q in data:
        if q['id'] in updates:
            q['explanation']['detail'] = updates[q['id']]
            applied += 1

    print(f'適用: {applied} 問')

    # 書き戻し（ensure_ascii=False, indent=2 で元のフォーマットを維持）
    with open(QUESTIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print('保存完了')

    # JSON 妥当性検証
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        verify = json.load(f)
    print(f'検証: {len(verify)} 問読み込み成功')

    return len(targets), fixed_count, applied


if __name__ == '__main__':
    main()
