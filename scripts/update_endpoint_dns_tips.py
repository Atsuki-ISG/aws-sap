#!/usr/bin/env python3
"""
Add "📌 判断ポイント" section to questions tagged or matching the
"endpoint-dns" theme (VPC Endpoint, PrivateLink, Route 53 Resolver,
Private Hosted Zone, hybrid DNS, etc.).

- Re-reads questions.json before writing, swaps only target items, saves.
- Does NOT modify answer/question/choices/id/num/tags/source.
- Only mutates explanation.detail by appending the tips section.
- Idempotent: skips items where the marker is already present.
- Also performs minor accuracy fixes flagged below.
"""

import json
from pathlib import Path

FILE = Path("/Users/aki/aws-sap/docs/data/questions.json")
MARKER = "📌 判断ポイント"

# -----------------------------------------------------------------------------
# Tip blocks per category
# -----------------------------------------------------------------------------

TIP_HEADER = "<br><br><strong>📌 判断ポイント</strong><br>"

TIP_RESOLVER = (
    TIP_HEADER
    + "Route 53 Resolver の方向は「<strong>誰がクエリを送るか</strong>」で決まる。"
    + "オンプレ機器が AWS 上の DNS 名を引きたい→<strong>Inbound</strong>（AWS 側に DNS 受け口を作る）。"
    + "AWS の EC2/Lambda がオンプレ DNS 名を引きたい→<strong>Outbound + 転送ルール</strong>（オンプレ DNS へ転送）。"
    + "<br><br>"
    + "<table border='1' cellpadding='4'>"
    + "<tr><th>クエリ送信元</th><th>解決したい名前</th><th>使うもの</th></tr>"
    + "<tr><td>AWS の EC2/Lambda</td><td>オンプレの社内 FQDN</td><td>Outbound エンドポイント + 転送ルール</td></tr>"
    + "<tr><td>オンプレのサーバ</td><td>VPC 内の Private Hosted Zone / VPC EP の Private DNS</td><td>Inbound エンドポイント（オンプレ DNS から条件付き転送）</td></tr>"
    + "<tr><td>AWS の EC2</td><td>同 VPC の Private Hosted Zone</td><td>Route 53 PHZ を VPC に関連付け（Resolver 不要）</td></tr>"
    + "</table>"
    + "<br>"
    + "<strong>引っ掛けポイント:</strong> "
    + "①「ゾーンを AWS に複製しない」「権威はオンプレに残す」と来たら PHZ ではなく <strong>Outbound + 転送ルール</strong>。"
    + "②マルチアカウントでは Resolver Rule を <strong>RAM で共有</strong>し、各 VPC に関連付ける。"
    + "③DHCP オプションで全クエリをオンプレ DNS に向けると AWS の内部 DNS（VPC EP の Private DNS など）が壊れるので原則 NG。"
    + "④Inbound と Outbound は方向が逆なので問題文の主語（誰が解決したいか）を最初に確定させる。"
)

TIP_PHZ = (
    TIP_HEADER
    + "Private Hosted Zone（PHZ）は「<strong>VPC 内だけで通用するプライベート DNS ゾーン</strong>」。"
    + "VPC に関連付けて初めて解決される。マルチ VPC では各 VPC（または別アカウントの VPC を承認）に関連付けが必要。"
    + "<br><br>"
    + "<strong>前提となる VPC 設定:</strong> <code>enableDnsSupport=true</code>（VPC のリゾルバを使う）と <code>enableDnsHostnames=true</code>（EC2 にパブリック DNS 名を付与）。"
    + "両方有効でないと PHZ や VPC EP の Private DNS が機能しない。"
    + "<br><br>"
    + "<table border='1' cellpadding='4'>"
    + "<tr><th>やりたいこと</th><th>正解パターン</th></tr>"
    + "<tr><td>VPC 内だけで内部ドメインを解決</td><td>PHZ を作って VPC に関連付け</td></tr>"
    + "<tr><td>同じドメインで AWS／オンプレ両方を解決（split-horizon）</td><td>PHZ + Resolver Outbound 転送ルール</td></tr>"
    + "<tr><td>別アカウントの VPC でも同じ PHZ を引きたい</td><td>create-vpc-association-authorization → associate-vpc-with-hosted-zone</td></tr>"
    + "<tr><td>VPC EP（Interface）の AWS サービス FQDN をプライベート IP に解決</td><td>VPC EP の <strong>プライベート DNS 有効化</strong>（PHZ を手動で作る必要なし）</td></tr>"
    + "</table>"
    + "<br>"
    + "<strong>引っ掛けポイント:</strong> "
    + "①PHZ にゾーンを作っても <strong>VPC 関連付けを忘れる</strong>と解決されない。"
    + "②オンプレ権威 DNS と同名の PHZ を AWS で作るとゾーンが二重化し権威が分裂する → 「複製禁止」要件下では Resolver 転送を選ぶ。"
)

TIP_GATEWAY_EP = (
    TIP_HEADER
    + "<strong>Gateway 型 VPC エンドポイントは S3 と DynamoDB の 2 サービス専用</strong>。それ以外（KMS, Secrets Manager, ECR, SQS, SNS など）は <strong>Interface 型（PrivateLink ベース）</strong>を使う。"
    + "<br><br>"
    + "<table border='1' cellpadding='4'>"
    + "<tr><th>項目</th><th>Gateway EP（S3, DynamoDB）</th><th>Interface EP（その他多数）</th></tr>"
    + "<tr><td>料金</td><td><strong>無料</strong>（データ処理料金なし）</td><td>ENI 1個あたり時間課金 + データ処理料金</td></tr>"
    + "<tr><td>仕組み</td><td>ルートテーブルに prefix list を追加</td><td>サブネットに ENI を作成、Private DNS で FQDN を ENI に解決</td></tr>"
    + "<tr><td>オンプレからの利用</td><td><strong>不可</strong>（VPC 内のリソースからのみ）</td><td>可能（DX/VPN 経由でも引ける）</td></tr>"
    + "<tr><td>アクセス制御</td><td>エンドポイントポリシー / バケットポリシー（aws:SourceVpce）</td><td>エンドポイントポリシー / SG / IAM</td></tr>"
    + "</table>"
    + "<br>"
    + "<strong>典型シナリオ:</strong> "
    + "①「プライベートサブネット → S3 を NAT GW 経由で大量転送」のコストを下げる → <strong>S3 Gateway EP</strong>（無料、データ転送料金もカット）。"
    + "②「KMS / SSM / ECR / Kinesis などへの NAT GW 通信を削りたい」→ <strong>Interface EP + Private DNS 有効化</strong>。"
    + "③「オンプレから DX 経由で S3 にアクセス」→ Gateway EP は使えないので <strong>S3 用 Interface EP</strong>（PrivateLink for S3）を選ぶ。"
    + "<br><br>"
    + "<strong>引っ掛けポイント:</strong> Gateway EP を「KMS や ECR にも使える」と書いた選択肢は誤り。"
    + "Interface EP は <strong>Private DNS を有効化しないと既存 FQDN が公開 IP のまま</strong>になる。"
)

TIP_INTERFACE_EP = (
    TIP_HEADER
    + "Interface 型 VPC エンドポイント（PrivateLink）は AWS パブリックサービス（KMS, SSM, ECR, Kinesis, Secrets Manager, CloudWatch Logs 等）や"
    + "他者公開の VPC Endpoint Service へ <strong>サブネット内 ENI 経由</strong>でプライベート接続するための部品。"
    + "<br><br>"
    + "<strong>使う/使わないの判断軸:</strong>"
    + "<table border='1' cellpadding='4'>"
    + "<tr><th>状況</th><th>判定</th></tr>"
    + "<tr><td>プライベートサブネット内 EC2/Lambda/ECS から AWS API を呼びたい</td><td>Interface EP + <strong>Private DNS 有効化</strong>でコード変更ゼロ</td></tr>"
    + "<tr><td>NAT GW のデータ処理料金を下げたい</td><td>頻度の高いサービスから順に Interface/Gateway EP 化</td></tr>"
    + "<tr><td>S3 / DynamoDB へのアクセス</td><td>原則 <strong>Gateway EP</strong>（無料）。DX 経由なら Interface EP for S3</td></tr>"
    + "<tr><td>Fargate / ECS タスクが ECR からイメージ取得失敗（NAT なし）</td><td><strong>ecr.api / ecr.dkr / S3（layer 取得用）/ logs</strong> の 4 セットを EP 化</td></tr>"
    + "</table>"
    + "<br>"
    + "<strong>引っ掛けポイント:</strong> "
    + "①Private DNS を有効にしないと、AWS SDK が呼ぶ標準 FQDN がパブリック IP に解決され続ける。"
    + "②Interface EP には ENI ごとに <strong>SG が必要</strong>（HTTPS 443 を VPC からインバウンド許可）。"
    + "③ECR は <code>ecr.api</code> と <code>ecr.dkr</code> の 2 種類。イメージレイヤは S3 から取得するので <strong>S3 Gateway EP も併設</strong>が定石。"
)

TIP_PRIVATELINK_SERVICE = (
    TIP_HEADER
    + "別 VPC（別アカウント／SaaS ベンダー）のサービスへ閉域接続する選択肢の整理:"
    + "<br><br>"
    + "<table border='1' cellpadding='4'>"
    + "<tr><th>方式</th><th>得意</th><th>制約・注意</th></tr>"
    + "<tr><td><strong>PrivateLink（VPC EP Service）</strong></td><td>1 サービス単位の片方向公開、CIDR 重複 OK、SaaS 提供に最適</td><td>バックエンドは <strong>NLB（または GWLB）</strong>必須。ALB は不可。TCP/TLS のみ</td></tr>"
    + "<tr><td>VPC Peering</td><td>双方向の L3 接続。少数 VPC 間で簡単</td><td>CIDR 重複 NG、推移ルーティング不可、N×N で管理破綻</td></tr>"
    + "<tr><td>Transit Gateway</td><td>多数 VPC とオンプレを集約。ルーティングが柔軟</td><td>料金高め、CIDR 重複 NG（基本）、TGW 経由でも PrivateLink を併用するパターン多い</td></tr>"
    + "</table>"
    + "<br>"
    + "<strong>選び方の合言葉:</strong> "
    + "「<strong>1 つのサービス API だけ公開／インターネット非経由／CIDR 重複可</strong>」→ PrivateLink。"
    + "「<strong>VPC 全体を相互接続したい／少数で済む</strong>」→ Peering。"
    + "「<strong>多数 VPC＋オンプレを束ねる</strong>」→ TGW（必要なら PrivateLink を上に乗せる）。"
    + "<br><br>"
    + "<strong>引っ掛けポイント:</strong> "
    + "①PrivateLink のバックエンドは <strong>NLB のみ</strong>（GWLB はトランスペアレント挿入用途で別物）。ALB を選択肢に出してきたら誤り。"
    + "②サービス提供側＝ Endpoint Service、利用側＝ Interface VPC Endpoint と方向を取り違えない。"
    + "③Site-to-Site VPN はインターネットを経由する暗号化トンネルなので「インターネット不使用」要件には不適。"
)

TIP_OTHER = (
    TIP_HEADER
    + "VPC 内サービス通信のコスト削減・閉域化の定石:"
    + "<br><br>"
    + "<table border='1' cellpadding='4'>"
    + "<tr><th>接続元 → 接続先</th><th>第一選択</th></tr>"
    + "<tr><td>VPC 内 → S3 / DynamoDB</td><td><strong>Gateway VPC エンドポイント（無料）</strong></td></tr>"
    + "<tr><td>VPC 内 → KMS / SSM / Secrets Manager / ECR / Kinesis / SQS / SNS / CW Logs 等</td><td><strong>Interface VPC エンドポイント + Private DNS</strong></td></tr>"
    + "<tr><td>VPC 内 → 別アカウント／SaaS の API</td><td><strong>PrivateLink（NLB バックエンドの Endpoint Service）</strong></td></tr>"
    + "<tr><td>オンプレ → VPC 内 DNS / VPC EP</td><td>Route 53 Resolver <strong>Inbound</strong> エンドポイント</td></tr>"
    + "<tr><td>VPC 内 → オンプレ DNS</td><td>Route 53 Resolver <strong>Outbound</strong> + 転送ルール</td></tr>"
    + "</table>"
    + "<br>"
    + "<strong>引っ掛けポイント:</strong> "
    + "①Gateway EP は S3/DynamoDB のみ。それ以外は Interface EP。"
    + "②VPC EP の Private DNS を有効化するには VPC の <code>enableDnsHostnames</code> と <code>enableDnsSupport</code> が両方 true である必要がある。"
    + "③NAT Gateway はインターネット向けの送信元 NAT。AWS サービスへの通信を NAT で出し続けると <strong>データ処理料金</strong>がかさむので EP に置き換えるのが王道。"
)

# Mapping num -> tip block
CATEGORY_MAP = {
    'resolver_dns': [54, 61, 78, 139, 162, 187, 223, 320, 328, 351, 377, 386, 395],
    'phz':          [221, 240, 464],
    'gateway_ep':   [25, 99, 116, 200, 207, 233, 271, 288, 316, 342, 397, 439, 468, 494, 497, 555, 590, 642, 666],
    'interface_ep': [66, 108, 222, 380, 404, 422, 563],
    'privatelink':  [35, 180, 239, 303, 356, 434, 461, 620],
    'other':        [42, 102, 129, 232, 276, 279, 291, 322, 359, 365, 450, 452, 489, 559],
}

CATEGORY_TIP = {
    'resolver_dns': TIP_RESOLVER,
    'phz':          TIP_PHZ,
    'gateway_ep':   TIP_GATEWAY_EP,
    'interface_ep': TIP_INTERFACE_EP,
    'privatelink':  TIP_PRIVATELINK_SERVICE,
    'other':        TIP_OTHER,
}

NUM_TO_TIP = {}
for cat, nums in CATEGORY_MAP.items():
    for n in nums:
        NUM_TO_TIP[n] = CATEGORY_TIP[cat]

# -----------------------------------------------------------------------------
# Optional accuracy fixes (technical corrections found while reviewing).
# Only target items where text is clearly wrong/misleading. The replacement
# uses an exact substring of the existing detail. Done as plain string
# .replace(old, new) on the detail string.
# -----------------------------------------------------------------------------
ACCURACY_FIXES = {
    # Q139: "PrivateLinkはNAT Gatewayをエクスポートできない" — the original
    # answer is correct (A=PrivateLink), but choice B's wording in the table
    # is awkward. The user-facing detail is OK as-is. No change.
    # Q303 etc. — leave content alone unless plain wrong.
}

# -----------------------------------------------------------------------------
# Run
# -----------------------------------------------------------------------------
def main():
    target_nums = sorted(NUM_TO_TIP.keys())
    print(f"Target questions: {len(target_nums)}")

    # Re-read just before write
    with FILE.open('r', encoding='utf-8') as f:
        data = json.load(f)

    appended_count = 0
    fixed_count = 0
    skipped_already_done = 0
    not_found = []

    nums_in_data = {q.get('num'): i for i, q in enumerate(data)}

    for num in target_nums:
        if num not in nums_in_data:
            not_found.append(num)
            continue
        idx = nums_in_data[num]
        q = data[idx]
        exp = q.get('explanation') or {}
        detail = exp.get('detail', '') or ''

        # Apply accuracy fix if defined
        if num in ACCURACY_FIXES:
            old, new = ACCURACY_FIXES[num]
            if old in detail and new not in detail:
                detail = detail.replace(old, new)
                fixed_count += 1

        # Append tip if not already
        if MARKER in detail:
            skipped_already_done += 1
        else:
            detail = detail + NUM_TO_TIP[num]
            appended_count += 1

        exp['detail'] = detail
        q['explanation'] = exp
        data[idx] = q

    # Write back
    with FILE.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  Appended 📌 判断ポイント: {appended_count}")
    print(f"  Accuracy fixes:          {fixed_count}")
    print(f"  Already had marker:      {skipped_already_done}")
    if not_found:
        print(f"  NOT FOUND in data:       {not_found}")

if __name__ == '__main__':
    main()
