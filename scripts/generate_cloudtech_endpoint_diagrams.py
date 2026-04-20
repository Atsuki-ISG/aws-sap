"""Generate drawio files for CloudTech SAP questions covering
VPC Endpoints / PrivateLink / Route 53 Resolver / Private Hosted Zone topics.

Output:
    docs/diagrams/per-question/SAP-<n>.drawio
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawio_builder import Diagram, Colors

OUT_DIR = "/Users/aki/aws-sap/docs/diagrams/per-question"
os.makedirs(OUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# SAP-54 — Route 53 Resolver Outbound: オンプレ DNS (corp.internal) を EC2 から解決
# ---------------------------------------------------------------------------
def make_sap_54():
    d = Diagram("SAP-54: Route 53 Resolver Outbound — EC2 → オンプレ DNS 解決", 1000, 600, "sap-54")

    # AWS VPC
    d.group_vpc(40, 70, 520, 420, "AWS VPC (10.0.0.0/16)")
    ec2 = d.icon("ec2", 100, 150, label="EC2 アプリ")
    d.rect(220, 150, 180, 60,
           value="Resolver Rule&#10;corp.internal → On-prem",
           fill="#FFFFFF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    outbound = d.icon("route_53", 440, 150, label="Outbound&#10;Resolver EP")
    d.rect(220, 240, 180, 60,
           value="Route 53 Resolver&#10;(AmazonProvidedDNS)",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)

    d.arrow(ec2, outbound, color=Colors.BLUE, label="1. corp.internal?")

    # Hybrid connectivity
    d.rect(580, 170, 100, 40,
           value="DX / VPN",
           fill="#FEF3F2", stroke=Colors.RED, stroke_width=2, fontsize=10, bold=True)
    d.arrow_xy(495, 170, 580, 190, color=Colors.BLUE, label="2. 転送")

    # On-prem
    d.group_onprem(700, 70, 260, 420, "On-premises")
    onprem_dns = d.rect(740, 150, 180, 60,
           value="オンプレ DNS&#10;corp.internal ゾーン",
           fill="#FFFFFF", stroke=Colors.GRAY, stroke_width=2, fontsize=10, bold=True)
    d.rect(740, 240, 180, 50,
           value="Internal Servers",
           fill="#FFFFFF", stroke=Colors.GRAY, stroke_width=1, fontsize=10)

    d.arrow_xy(680, 190, 740, 180, color=Colors.BLUE, label="3. DNS query")

    d.note(40, 510, 920, 80,
           value=("◾ 解法: VPC → オンプレ DNS を解決 = Outbound Resolver Endpoint + Forwarding Rule\n"
                  "  ・EC2 の /etc/resolv.conf は AmazonProvidedDNS のまま。Resolver Rule で条件転送\n"
                  "  ・オンプレ DNS は Outbound EP ENI の IP からのクエリを許可\n"
                  "◾ 混同注意: Inbound EP は『オンプレ→AWS PHZ 解決』で方向が逆"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-54.drawio")


# ---------------------------------------------------------------------------
# SAP-78 — 共有 TGW 経由で複数アカウント VPC がオンプレ DNS 解決 (Outbound + RAM 共有)
# ---------------------------------------------------------------------------
def make_sap_78():
    d = Diagram("SAP-78: 共有 TGW + Resolver Rule (RAM 共有) によるオンプレ DNS 解決", 1000, 600, "sap-78")

    # Shared services account
    d.group_account(40, 70, 340, 450, "Network / Shared Account")
    d.group_vpc(60, 110, 300, 240, "Shared Services VPC")
    outbound = d.icon("route_53", 90, 170, label="Outbound&#10;Resolver EP")
    d.rect(180, 170, 160, 60,
           value="Resolver Rule&#10;corp.local → on-prem",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    d.rect(80, 260, 260, 70,
           value="Rule を RAM で共有&#10;→ Spoke VPC に Associate&#10;→ 各アカウントの VPC で有効化",
           fill="#FFF8E1", stroke=Colors.YELLOW, stroke_width=2, fontsize=10, bold=True)
    tgw = d.icon("transit_gateway", 170, 370, label="Transit Gateway")

    # Spoke VPCs
    d.group_account(420, 70, 260, 200, "Account A")
    ec2a = d.icon("ec2", 490, 140, label="EC2")
    d.group_account(420, 290, 260, 200, "Account B")
    ec2b = d.icon("ec2", 490, 360, label="EC2")
    d.arrow(ec2a, tgw, color=Colors.BLUE, dashed=True, label="RAM共有Rule")
    d.arrow(ec2b, tgw, color=Colors.BLUE, dashed=True, label="RAM共有Rule")

    # DX + Onprem
    d.rect(720, 240, 100, 40,
           value="DX / VPN",
           fill="#FEF3F2", stroke=Colors.RED, stroke_width=2, fontsize=10, bold=True)
    d.arrow_xy(220, 370, 770, 280, color=Colors.BLUE, label="DNSクエリ")
    d.group_onprem(840, 70, 140, 450, "On-prem")
    d.rect(855, 240, 110, 40,
           value="オンプレ DNS",
           fill="#FFFFFF", stroke=Colors.GRAY, stroke_width=2, fontsize=10, bold=True)
    d.arrow_xy(820, 260, 855, 260, color=Colors.BLUE)

    d.note(40, 530, 940, 60,
           value=("◾ 解法: Outbound Resolver EP + Rule を RAM 共有 → 各 Spoke VPC に Associate\n"
                  "  ・EP は Network Account にだけ作る (コスト削減)。TGW でトラフィック到達\n"
                  "  ・Route 53 Resolver Rule は AWS RAM でクロスアカウント共有できる"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-78.drawio")


# ---------------------------------------------------------------------------
# SAP-108 — VPC Endpoint で NAT Gateway コスト削減
# ---------------------------------------------------------------------------
def make_sap_108():
    d = Diagram("SAP-108: Gateway + Interface EP で NAT GW コスト削減", 1000, 600, "sap-108")

    # Before (NAT heavy)
    d.group_vpc(40, 70, 440, 220, "Before: 全トラフィックが NAT GW 経由")
    ec2b = d.icon("ec2", 90, 140, label="EC2 (Private)")
    natb = d.icon("nat_gateway", 220, 140, label="NAT GW&#10;($0.045/h + データ転送)")
    d.rect(370, 140, 90, 50, value="Internet",
           fill="#FEF3F2", stroke=Colors.RED, stroke_width=2, fontsize=10, bold=True)
    d.arrow(ec2b, natb, color=Colors.RED)
    d.arrow_xy(280, 160, 370, 160, color=Colors.RED, label="S3/DDB/KMS")

    # After (EP optimized)
    d.group_vpc(40, 320, 920, 230, "After: AWS サービス宛は VPC Endpoint 経由")
    ec2a = d.icon("ec2", 90, 380, label="EC2 (Private)")
    gw_ep = d.icon("endpoint", 240, 360, label="Gateway EP&#10;(S3/DDB 無料)")
    if_ep = d.icon("endpoint", 240, 460, label="Interface EP&#10;(KMS/SSM/STS)")
    s3 = d.icon("s3", 420, 360, label="S3")
    ddb = d.icon("dynamodb", 520, 360, label="DynamoDB")
    d.rect(420, 440, 200, 60,
           value="KMS / Secrets Manager&#10;SSM / STS / Logs など&#10;(AWS PrivateLink 対応)",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    nat_small = d.icon("nat_gateway", 780, 380, label="NAT GW&#10;(外部 API だけ)")
    d.rect(870, 395, 70, 40, value="Internet", fill="#FEF3F2", stroke=Colors.GRAY, fontsize=10)

    d.arrow(ec2a, gw_ep, color=Colors.GREEN)
    d.arrow(ec2a, if_ep, color=Colors.BLUE)
    d.arrow(gw_ep, s3, color=Colors.GREEN)
    d.arrow(gw_ep, ddb, color=Colors.GREEN)
    d.arrow_xy(290, 470, 420, 470, color=Colors.BLUE)
    d.arrow(ec2a, nat_small, color=Colors.GRAY, dashed=True, label="外部SaaS のみ")
    d.arrow_xy(830, 415, 870, 415, color=Colors.GRAY)

    d.note(40, 560, 920, 35,
           value=("◾ Gateway EP は S3/DynamoDB のみ・無料 / Interface EP は AZ 毎 $0.01/h + データ転送 $0.01/GB (NAT より安価)"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-108.drawio")


# ---------------------------------------------------------------------------
# SAP-112 — Lambda from VPC + NAT Gateway で送信元 IP 固定
# ---------------------------------------------------------------------------
def make_sap_112():
    d = Diagram("SAP-112: Lambda 送信元 IP を固定 — VPC Lambda + NAT GW + EIP", 1000, 600, "sap-112")

    d.group_vpc(40, 80, 620, 430, "VPC")
    # Private subnet for Lambda
    d.rect(70, 120, 260, 200,
           value="Private Subnet",
           fill="#FFFFFF", stroke=Colors.GREEN, stroke_width=2, fontsize=10, bold=True, valign="top")
    lam = d.rect(100, 170, 200, 60, value="Lambda (VPC 内 ENI)",
                 fill="#FFF5EB", stroke=Colors.YELLOW, stroke_width=2, fontsize=11, bold=True)
    d.rect(100, 240, 200, 40, value="Subnet RT → 0.0.0.0/0 → NAT",
           fill="#FFFFFF", stroke=Colors.GREEN, fontsize=10)

    # Public subnet with NAT
    d.rect(380, 120, 260, 200,
           value="Public Subnet",
           fill="#FFFFFF", stroke=Colors.GREEN, stroke_width=2, fontsize=10, bold=True, valign="top")
    nat = d.icon("nat_gateway", 420, 170, label="NAT Gateway")
    d.rect(510, 180, 120, 40, value="EIP 固定",
           fill="#FFF8E1", stroke=Colors.YELLOW, stroke_width=2, fontsize=10, bold=True)
    d.rect(400, 250, 220, 40, value="Route: 0.0.0.0/0 → IGW",
           fill="#FFFFFF", stroke=Colors.GREEN, fontsize=10)

    igw = d.rect(290, 370, 120, 40, value="Internet Gateway",
                 fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    d.arrow_xy(200, 230, 420, 195, color=Colors.ORANGE, label="外部 API")
    d.arrow_xy(445, 220, 350, 370, color=Colors.ORANGE)

    # External API
    d.rect(700, 210, 240, 80,
           value="外部 API プロバイダ&#10;許可リスト: EIP のみ",
           fill="#FEF3F2", stroke=Colors.RED, stroke_width=2, fontsize=11, bold=True)
    d.arrow_xy(410, 390, 820, 290, color=Colors.ORANGE, label="EIP 固定元IP")

    d.note(40, 520, 920, 75,
           value=("◾ 解法: Lambda を VPC 内 (Private Subnet) に配置 → NAT GW 経由で送信\n"
                  "  ・NAT GW に EIP を割り当てれば 送信元 IP が固定され、外部 API 許可リスト登録可\n"
                  "  ・Public Subnet 配置 + パブリック IP 自動割当は Lambda では不可 (ENI はプライベートのみ)\n"
                  "◾ 誤答: PrivateLink は外部第三者に到達不可 / CloudFront は Lambda 送信元 IP を固定しない"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-112.drawio")


# ---------------------------------------------------------------------------
# SAP-116 — S3 Gateway Endpoint (インターネット非経由)
# ---------------------------------------------------------------------------
def make_sap_116():
    d = Diagram("SAP-116: S3 Gateway Endpoint + ライフサイクル (プライベート転送)", 1000, 600, "sap-116")

    d.group_vpc(40, 70, 520, 400, "VPC")
    d.rect(60, 110, 480, 300, value="Private Subnet",
           fill="#FFFFFF", stroke=Colors.GREEN, stroke_width=2, fontsize=10, bold=True, valign="top")
    ec2 = d.icon("ec2", 90, 170, label="EC2 (ログ出力)")
    d.rect(210, 170, 170, 60,
           value="Route Table&#10;pl-xxx (S3) → vpce-xxx",
           fill="#FFFFFF", stroke=Colors.GREEN, stroke_width=2, fontsize=10, bold=True)
    gw_ep = d.icon("endpoint", 420, 170, label="Gateway EP&#10;(S3 / 無料)")
    d.arrow(ec2, gw_ep, color=Colors.GREEN, label="プライベート経路")

    # S3 with lifecycle
    s3 = d.icon("s3", 650, 170, label="S3 Bucket")
    d.arrow(gw_ep, s3, color=Colors.GREEN)

    # Lifecycle
    d.rect(620, 260, 340, 160,
           value="ライフサイクルポリシー",
           fill="#F5F5F5", stroke=Colors.NAV, stroke_width=2, fontsize=11, bold=True, valign="top")
    d.rect(640, 295, 140, 30, value="S3 Standard (0-30d)",
           fill="#FFFFFF", stroke=Colors.S3_GREEN, fontsize=10)
    d.rect(640, 335, 140, 30, value="Standard-IA (30-90d)",
           fill="#FFFFFF", stroke=Colors.S3_GREEN, fontsize=10)
    d.rect(640, 375, 140, 30, value="Glacier Instant (90d+)",
           fill="#FFFFFF", stroke=Colors.S3_GREEN, fontsize=10)
    d.rect(800, 295, 140, 110,
           value="分析時は即時取得可&#10;コストは最大 83%削減",
           fill="#EBF5E8", stroke=Colors.S3_GREEN, stroke_width=2, fontsize=10)

    d.note(40, 490, 920, 100,
           value=("◾ 解法: S3 Gateway Endpoint で VPC からインターネット非経由で転送 + ライフサイクルで低コスト化\n"
                  "  ・Gateway EP は S3/DynamoDB 専用、無料、ルートテーブル編集で有効化\n"
                  "  ・要件『90日後に低コスト』= Standard-IA or Glacier Instant Retrieval (即時)\n"
                  "  ・Glacier Flexible/Deep Archive は復元時間があり『即時』要件に合わない\n"
                  "◾ 誤答: NAT GW 経由 = データ転送料金が発生、インターネットを経由"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-116.drawio")


# ---------------------------------------------------------------------------
# SAP-121 — AWS Client VPN: リモートワーカー → マルチアカウント VPC
# ---------------------------------------------------------------------------
def make_sap_121():
    d = Diagram("SAP-121: AWS Client VPN — マルチアカウント VPC へ安全アクセス", 1000, 600, "sap-121")

    # Remote worker
    d.group_onprem(40, 100, 220, 280, "Remote Workers")
    d.rect(60, 140, 180, 50,
           value="Laptops&#10;(AWS VPN Client)",
           fill="#FFFFFF", stroke=Colors.GRAY, stroke_width=2, fontsize=10, bold=True)
    d.rect(60, 210, 180, 50,
           value="MFA / SAML / AD",
           fill="#FFF8E1", stroke=Colors.YELLOW, stroke_width=2, fontsize=10, bold=True)
    d.rect(60, 280, 180, 50,
           value="自宅/出張先",
           fill="#FFFFFF", stroke=Colors.GRAY, fontsize=10)

    # Client VPN Endpoint
    d.group_account(310, 80, 280, 430, "Network Account (Hub)")
    d.rect(340, 130, 220, 70,
           value="Client VPN Endpoint&#10;(Associate: Hub VPC Subnet)",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=11, bold=True)
    d.rect(340, 220, 220, 70,
           value="Authorization Rules&#10;→ Spoke VPC CIDR 群",
           fill="#FFF8E1", stroke=Colors.YELLOW, stroke_width=2, fontsize=10, bold=True)
    tgw = d.icon("transit_gateway", 410, 320, label="Transit Gateway")

    d.arrow_xy(260, 240, 340, 160, color=Colors.BLUE, label="mTLS/SAML")

    # Spokes
    d.group_account(640, 80, 320, 200, "Account A / VPC")
    ec2a = d.icon("ec2", 720, 140, label="Private Resources")
    d.group_account(640, 320, 320, 200, "Account B / VPC")
    ec2b = d.icon("ec2", 720, 380, label="Private Resources")
    d.arrow(tgw, ec2a, color=Colors.BLUE)
    d.arrow(tgw, ec2b, color=Colors.BLUE)

    d.note(40, 530, 920, 60,
           value=("◾ 解法: AWS Client VPN Endpoint を Hub VPC に作成 + TGW で全アカウント VPC へルーティング\n"
                  "  ・認証: MFA/SAML/AD 連携。Authorization Rule で到達可能な CIDR を制限\n"
                  "  ・Site-to-Site VPN は拠点向け (常設)、個人端末向けは Client VPN"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-121.drawio")


# ---------------------------------------------------------------------------
# SAP-139 — Interface Endpoint (VPC) から SaaS / AWS サービス API へ
# ---------------------------------------------------------------------------
def make_sap_139():
    d = Diagram("SAP-139: Interface EP (PrivateLink) — アウトバウンド閉鎖 VPC から API", 1000, 600, "sap-139")

    d.group_vpc(40, 80, 440, 420, "Consumer VPC (IGW/NAT なし)")
    ec2 = d.icon("ec2", 90, 160, label="EC2 (Private)")
    d.rect(200, 140, 250, 100,
           value="Private DNS 自動解決&#10;api.example.com → EP ENI",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    ep = d.icon("endpoint", 250, 280, label="Interface EP&#10;(PrivateLink ENI)")
    sg = d.rect(100, 380, 340, 70,
           value="Security Group (EP ENI 用)&#10;HTTPS 443 を Consumer SG から許可",
           fill="#FFF8E1", stroke=Colors.YELLOW, stroke_width=2, fontsize=10, bold=True)
    d.arrow(ec2, ep, color=Colors.BLUE, label="443 プライベート")

    # Provider
    d.group_account(540, 80, 420, 420, "Provider (AWS Service or SaaS)")
    nlb = d.icon("nlb", 580, 160, label="NLB")
    d.rect(680, 150, 260, 70,
           value="VPC Endpoint Service&#10;(service name: com.amazonaws.vpce.<id>)",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    app = d.rect(680, 260, 260, 80,
           value="Backend (EC2/Fargate/Lambda)&#10;SaaS API 本体",
           fill="#FFFFFF", stroke=Colors.NAV, stroke_width=2, fontsize=11, bold=True)
    d.arrow(nlb, app, color=Colors.NAV)
    d.arrow_xy(300, 305, 580, 185, color=Colors.BLUE, label="AWS バックボーン")

    d.note(40, 520, 920, 70,
           value=("◾ 解法: Consumer VPC に Interface Endpoint (ENI) を配置 → SaaS の Endpoint Service に接続\n"
                  "  ・インターネット/NAT 不要、AWS バックボーンで閉じる (PrivateLink)\n"
                  "  ・SaaS 提供者は NLB の前段に Endpoint Service を作成、Consumer Account ID を許可\n"
                  "  ・Private DNS Enable で既存ドメインをそのまま利用可能"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-139.drawio")


# ---------------------------------------------------------------------------
# SAP-162 — オンプレ DC の API を AWS 上の外部企業に非公開提供 (PrivateLink)
# ---------------------------------------------------------------------------
def make_sap_162():
    d = Diagram("SAP-162: オンプレ API を PrivateLink で外部企業へ提供", 1000, 600, "sap-162")

    # On-prem provider
    d.group_onprem(40, 80, 260, 400, "自社 On-prem DC")
    d.rect(60, 130, 220, 70,
           value="API Server&#10;(社内資産)",
           fill="#FFFFFF", stroke=Colors.GRAY, stroke_width=2, fontsize=11, bold=True)
    d.rect(60, 220, 220, 60,
           value="Direct Connect / VPN",
           fill="#FEF3F2", stroke=Colors.RED, stroke_width=2, fontsize=10, bold=True)

    # Provider VPC
    d.group_account(330, 80, 310, 400, "Provider VPC (自社)")
    nlb = d.icon("nlb", 370, 140, label="NLB (Target=on-prem IP)")
    d.arrow_xy(290, 250, 395, 170, color=Colors.RED, label="DX バックホール")
    eps = d.rect(470, 240, 150, 70,
           value="Endpoint Service",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=11, bold=True)
    d.rect(360, 340, 260, 90,
           value="許可リスト (Allow principal)&#10;外部企業の AWS Account ID / ARN",
           fill="#FFF8E1", stroke=Colors.YELLOW, stroke_width=2, fontsize=10, bold=True)
    d.arrow(nlb, eps, color=Colors.BLUE)

    # Consumer
    d.group_account(680, 80, 280, 400, "Consumer VPC (外部企業)")
    ep = d.icon("endpoint", 730, 220, label="Interface EP")
    app = d.icon("ec2", 860, 220, label="Consumer App")
    d.arrow_xy(620, 275, 755, 245, color=Colors.BLUE, label="PrivateLink")
    d.arrow(ep, app, color=Colors.BLUE)

    d.note(40, 510, 920, 80,
           value=("◾ 解法: NLB + VPC Endpoint Service で PrivateLink 提供 → 外部企業アカウントへ非公開公開\n"
                  "  ・NLB のターゲットは DX 経由のオンプレ IP でも可 (target type: IP)\n"
                  "  ・Consumer は Interface EP で ENI を取得。AWS バックボーンだけで完結\n"
                  "◾ 誤答: API Gateway Public / IGW 経由 = インターネット公開 → 要件違反"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-162.drawio")


# ---------------------------------------------------------------------------
# SAP-180 — 医療 SaaS API を PrivateLink で接続 (インターネット不使用)
# ---------------------------------------------------------------------------
def make_sap_180():
    d = Diagram("SAP-180: 患者情報を Interface EP (PrivateLink) で SaaS へ送信", 1000, 600, "sap-180")

    # Hospital VPC
    d.group_account(40, 80, 380, 420, "Hospital AWS Account / VPC")
    ec2 = d.icon("ec2", 90, 160, label="EC2 / Fargate&#10;(EMR Integration)")
    ep = d.icon("endpoint", 250, 160, label="Interface EP&#10;(ENI)")
    d.rect(70, 260, 330, 60,
           value="Private DNS: api.saas.example.com&#10;→ EP ENI Private IP",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    d.rect(70, 340, 330, 80,
           value="✓ IGW/NAT 不要&#10;✓ AWS バックボーン経路 (インターネット不使用)&#10;✓ HIPAA BAA 対応容易",
           fill="#EBF5E8", stroke=Colors.S3_GREEN, stroke_width=2, fontsize=10, bold=True)
    d.arrow(ec2, ep, color=Colors.BLUE, label="HTTPS 443")

    # Provider side
    d.group_account(460, 80, 500, 420, "SaaS Provider AWS")
    d.rect(490, 160, 180, 60,
           value="VPC Endpoint Service",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=11, bold=True)
    nlb = d.icon("nlb", 720, 150, label="NLB")
    d.rect(830, 150, 110, 70,
           value="SaaS API&#10;(Fargate)",
           fill="#FFFFFF", stroke=Colors.NAV, stroke_width=2, fontsize=11, bold=True)
    d.arrow_xy(670, 185, 745, 175, color=Colors.BLUE)
    d.arrow_xy(770, 175, 830, 185, color=Colors.BLUE)
    d.arrow_xy(300, 185, 490, 185, color=Colors.BLUE, label="PrivateLink")

    d.rect(480, 260, 460, 60,
           value="Allow-listed Principal: arn:aws:iam::<hospital>:root",
           fill="#FFF8E1", stroke=Colors.YELLOW, stroke_width=2, fontsize=10, bold=True)
    d.rect(480, 340, 460, 80,
           value="◾ HIPAA / 医療データ要件を満たす典型パターン&#10;◾ データはテナント VPC → AWS バックボーン → Provider VPC へ直接",
           fill="#F5F5F5", stroke=Colors.NAV, fontsize=10)

    d.note(40, 510, 920, 70,
           value=("◾ 解法: Interface Endpoint (AWS PrivateLink) で SaaS API にプライベート接続\n"
                  "  ・VPC CIDR 重複も無関係、インターネット非経由、単方向 (Consumer → Service)\n"
                  "  ・Site-to-Site VPN は SaaS 向けに非現実的、PrivateLink が標準解"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-180.drawio")


# ---------------------------------------------------------------------------
# SAP-187 — Route 53 Resolver Outbound (オンプレ名前解決継続 + 段階移行)
# ---------------------------------------------------------------------------
def make_sap_187():
    d = Diagram("SAP-187: Route 53 Resolver で段階的 DNS 移行 (中断なし)", 1000, 600, "sap-187")

    # VPC
    d.group_vpc(40, 80, 440, 420, "AWS VPC")
    ec2 = d.icon("ec2", 90, 160, label="EC2 アプリ")
    outbound = d.icon("route_53", 260, 160, label="Outbound&#10;Resolver EP")
    d.rect(50, 260, 420, 80,
           value="Resolver Rules&#10;corp.legacy → オンプレ DNS&#10;corp.new.private → Route 53 PHZ",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    d.rect(50, 360, 420, 80,
           value="Route 53 PHZ (corp.new.private)&#10;→ AWS 上に新規作成した名前空間",
           fill="#FFF8E1", stroke=Colors.YELLOW, stroke_width=2, fontsize=10, bold=True)
    d.arrow(ec2, outbound, color=Colors.BLUE)

    # DX
    d.rect(510, 180, 80, 40, value="DX / VPN",
           fill="#FEF3F2", stroke=Colors.RED, stroke_width=2, fontsize=10, bold=True)
    d.arrow_xy(310, 185, 510, 195, color=Colors.BLUE, label="条件転送")

    # On-prem
    d.group_onprem(620, 80, 340, 420, "On-premises (段階縮小)")
    d.rect(660, 140, 260, 60,
           value="オンプレ DNS (corp.legacy)",
           fill="#FFFFFF", stroke=Colors.GRAY, stroke_width=2, fontsize=11, bold=True)
    d.rect(660, 220, 260, 100,
           value="レガシー社内サーバ群&#10;(一部のサービスが残存)",
           fill="#FFFFFF", stroke=Colors.GRAY, fontsize=10)
    d.rect(660, 340, 260, 100,
           value="移行済サービス&#10;→ AWS の PHZ で解決",
           fill="#EBF5E8", stroke=Colors.S3_GREEN, stroke_width=2, fontsize=10, bold=True)
    d.arrow_xy(590, 200, 660, 170, color=Colors.BLUE)

    d.note(40, 510, 920, 70,
           value=("◾ 解法: Outbound Resolver Endpoint + 条件付き転送ルール で既存オンプレ DNS を残したまま段階移行\n"
                  "  ・PHZ を別名前空間 (corp.new.private) で作成すればレガシーと共存可能\n"
                  "  ・完全移行後は Outbound EP とルールを削除 → DNS 切断なし"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-187.drawio")


# ---------------------------------------------------------------------------
# SAP-200 — Lambda → Neptune (Interface) + DynamoDB (Gateway) セキュア接続
# ---------------------------------------------------------------------------
def make_sap_200():
    d = Diagram("SAP-200: Lambda → Neptune + DynamoDB を EP で閉域化", 1000, 600, "sap-200")

    d.group_vpc(40, 80, 920, 420, "VPC (PrivateLink 構成)")
    # Lambda in VPC
    d.rect(70, 120, 260, 340, value="Private Subnet (Lambda)",
           fill="#FFFFFF", stroke=Colors.GREEN, stroke_width=2, fontsize=10, bold=True, valign="top")
    lam = d.rect(100, 170, 200, 70, value="Lambda (VPC ENI)",
                 fill="#FFF5EB", stroke=Colors.YELLOW, stroke_width=2, fontsize=11, bold=True)

    # Neptune interface EP
    d.rect(360, 120, 280, 340, value="Neptune (Cluster Endpoint)",
           fill="#FFFFFF", stroke=Colors.GREEN, stroke_width=2, fontsize=10, bold=True, valign="top")
    neptune = d.rect(400, 170, 200, 70, value="Neptune DB (Graph)",
                     fill="#FFFFFF", stroke=Colors.NAV, stroke_width=2, fontsize=11, bold=True)
    d.rect(400, 260, 200, 50, value="SG: Lambda SG → 8182",
           fill="#FFF8E1", stroke=Colors.YELLOW, fontsize=10)
    d.rect(400, 330, 200, 60, value="Private 経路で直接接続&#10;(VPC 内 ENI)",
           fill="#EBF5E8", stroke=Colors.S3_GREEN, stroke_width=2, fontsize=10, bold=True)

    # DynamoDB via Gateway EP
    d.rect(680, 120, 260, 340, value="DynamoDB (Gateway EP)",
           fill="#FFFFFF", stroke=Colors.GREEN, stroke_width=2, fontsize=10, bold=True, valign="top")
    gw_ep = d.icon("endpoint", 700, 170, label="Gateway EP")
    ddb = d.icon("dynamodb", 830, 170, label="DynamoDB")
    d.rect(700, 260, 220, 60,
           value="Route Table: pl-ddb → vpce",
           fill="#FFFFFF", stroke=Colors.GREEN, fontsize=10)
    d.rect(700, 330, 220, 60,
           value="無料 / インターネット非経由",
           fill="#EBF5E8", stroke=Colors.S3_GREEN, stroke_width=2, fontsize=10, bold=True)

    d.arrow(lam, neptune, color=Colors.BLUE, label="Bolt/Gremlin")
    d.arrow_xy(300, 210, 700, 195, color=Colors.GREEN, label="PutItem")
    d.arrow(gw_ep, ddb, color=Colors.GREEN)

    d.note(40, 520, 920, 70,
           value=("◾ 解法: Lambda を VPC 内に配置し Neptune へ直接 ENI 接続 + DynamoDB は Gateway EP 経由\n"
                  "  ・Neptune 自体が VPC 内 DB (パブリック公開不可) → Lambda を VPC に入れる必要あり\n"
                  "  ・VPC Lambda からの DynamoDB アクセスは Gateway EP で NAT 不要・無料化"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-200.drawio")


# ---------------------------------------------------------------------------
# SAP-207 — S3 Gateway Endpoint (コスト最適)
# ---------------------------------------------------------------------------
def make_sap_207():
    d = Diagram("SAP-207: S3 Gateway Endpoint (Private Subnet コスト最適)", 1000, 600, "sap-207")

    # BAD path
    d.rect(40, 80, 920, 40, value="比較: NAT GW 経由 vs Gateway Endpoint 経由",
           fill="#F5F5F5", stroke=Colors.NAV, stroke_width=1, fontsize=12, bold=True)

    d.group_vpc(40, 140, 920, 180, "Case A: NAT GW 経由 (悪い例)")
    ec2a = d.icon("ec2", 100, 200, label="EC2 (Private)")
    nat = d.icon("nat_gateway", 280, 200, label="NAT GW ($0.045/h)")
    igw = d.rect(440, 210, 100, 40, value="IGW",
                 fill="#FEF3F2", stroke=Colors.RED, stroke_width=2, fontsize=10, bold=True)
    s3a = d.icon("s3", 680, 200, label="S3")
    d.arrow(ec2a, nat, color=Colors.RED)
    d.arrow_xy(330, 220, 440, 230, color=Colors.RED)
    d.arrow_xy(540, 230, 680, 220, color=Colors.RED, label="データ転送料金")

    d.group_vpc(40, 330, 920, 180, "Case B: Gateway Endpoint 経由 (推奨)")
    ec2b = d.icon("ec2", 100, 390, label="EC2 (Private)")
    rt = d.rect(240, 390, 170, 60,
                value="Route Table&#10;pl-s3 → vpce-xxx",
                fill="#FFFFFF", stroke=Colors.GREEN, stroke_width=2, fontsize=10, bold=True)
    gw = d.icon("endpoint", 450, 390, label="Gateway EP&#10;(S3 / 無料)")
    s3b = d.icon("s3", 680, 390, label="S3")
    d.arrow(ec2b, rt, color=Colors.GREEN)
    d.arrow(rt, gw, color=Colors.GREEN)
    d.arrow(gw, s3b, color=Colors.GREEN, label="AWS ネットワーク内")

    d.note(40, 525, 920, 60,
           value=("◾ 解法: S3/DynamoDB は Gateway Endpoint (無料) 一択 → NAT GW 転送料金を削減しセキュリティも強化\n"
                  "  ・ルートテーブルに Prefix List → VPCE を追加するだけで有効化"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-207.drawio")


# ---------------------------------------------------------------------------
# SAP-221 — Interface Endpoint でプライベート IP のみでサービス接続
# ---------------------------------------------------------------------------
def make_sap_221():
    d = Diagram("SAP-221: Interface Endpoint — プライベート IP のみでサービス接続", 1000, 600, "sap-221")

    d.group_vpc(40, 80, 540, 440, "VPC (NAT/IGW なし)")
    # Private subnets (2 AZ)
    d.rect(70, 130, 240, 280, value="Private Subnet A",
           fill="#FFFFFF", stroke=Colors.GREEN, stroke_width=2, fontsize=10, bold=True, valign="top")
    ec2a = d.icon("ec2", 100, 180, label="EC2 AZ-a")
    epa = d.icon("endpoint", 220, 180, label="EP ENI (AZ-a)&#10;Private IP")
    d.rect(310, 130, 250, 280, value="Private Subnet B",
           fill="#FFFFFF", stroke=Colors.GREEN, stroke_width=2, fontsize=10, bold=True, valign="top")
    ec2b = d.icon("ec2", 340, 180, label="EC2 AZ-b")
    epb = d.icon("endpoint", 460, 180, label="EP ENI (AZ-b)&#10;Private IP")
    d.rect(70, 310, 490, 90,
           value="Private DNS 有効化&#10;secretsmanager.<region>.amazonaws.com → EP ENI&#10;(標準 FQDN がそのまま使える)",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    d.arrow(ec2a, epa, color=Colors.BLUE)
    d.arrow(ec2b, epb, color=Colors.BLUE)

    # AWS services
    d.rect(620, 80, 340, 440, value="AWS Public Services",
           fill="#F5F5F5", stroke=Colors.NAV, stroke_width=2, fontsize=11, bold=True, valign="top")
    d.rect(640, 130, 300, 50, value="Secrets Manager",
           fill="#FFFFFF", stroke=Colors.MAGENTA, fontsize=10, bold=True)
    d.rect(640, 190, 300, 50, value="SSM (Session Manager, Parameter Store)",
           fill="#FFFFFF", stroke=Colors.MAGENTA, fontsize=10, bold=True)
    d.rect(640, 250, 300, 50, value="KMS / STS / CloudWatch Logs",
           fill="#FFFFFF", stroke=Colors.MAGENTA, fontsize=10, bold=True)
    d.rect(640, 310, 300, 90,
           value="Interface Endpoint 対応サービス&#10;→ PrivateLink で直接接続",
           fill="#EBF5E8", stroke=Colors.S3_GREEN, stroke_width=2, fontsize=10, bold=True)
    d.arrow_xy(510, 205, 640, 205, color=Colors.BLUE, label="AWS バックボーン")

    d.note(40, 530, 920, 60,
           value=("◾ 解法: Interface VPC Endpoint (PrivateLink) を AZ 毎に配置 → Private DNS 有効化\n"
                  "  ・VPC 内 EC2 はプライベート IP だけで AWS パブリックサービスに到達\n"
                  "  ・Gateway EP は S3/DDB 専用、それ以外は Interface EP"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-221.drawio")


# ---------------------------------------------------------------------------
# SAP-222 — ECR Interface Endpoints + S3 Gateway (Fargate パブリック IP なし)
# ---------------------------------------------------------------------------
def make_sap_222():
    d = Diagram("SAP-222: Fargate (Private) が ECR から Pull — 4 つの EP 必須", 1000, 600, "sap-222")

    d.group_vpc(40, 80, 560, 420, "VPC (Private Subnets only)")
    d.rect(70, 130, 260, 340, value="Private Subnet",
           fill="#FFFFFF", stroke=Colors.GREEN, stroke_width=2, fontsize=10, bold=True, valign="top")
    fg = d.rect(100, 180, 200, 70, value="Fargate Task&#10;(awsvpc ENI)",
                fill="#FFF5EB", stroke=Colors.YELLOW, stroke_width=2, fontsize=11, bold=True)
    d.rect(100, 270, 200, 60, value="assignPublicIp=DISABLED",
           fill="#FEF3F2", stroke=Colors.RED, stroke_width=2, fontsize=10, bold=True)

    d.rect(360, 130, 220, 340, value="VPC Endpoints (4 個)",
           fill="#F5F5F5", stroke=Colors.NAV, stroke_width=2, fontsize=11, bold=True, valign="top")
    d.rect(380, 170, 180, 50, value="Interface EP: ecr.api",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    d.rect(380, 230, 180, 50, value="Interface EP: ecr.dkr",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    d.rect(380, 290, 180, 50, value="Interface EP: logs",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    d.rect(380, 350, 180, 50, value="Gateway EP: S3 (layer 取得)",
           fill="#EBF5E8", stroke=Colors.S3_GREEN, stroke_width=2, fontsize=10, bold=True)
    d.arrow_xy(300, 215, 380, 195, color=Colors.BLUE, label="API 呼び出し")
    d.arrow_xy(300, 220, 380, 255, color=Colors.BLUE, label="レジストリ認証")
    d.arrow_xy(300, 230, 380, 315, color=Colors.BLUE, label="ログ")
    d.arrow_xy(300, 250, 380, 375, color=Colors.GREEN, label="イメージ層 (S3)")

    # ECR + S3
    d.rect(640, 80, 320, 420, value="AWS Managed Services",
           fill="#F5F5F5", stroke=Colors.NAV, stroke_width=2, fontsize=11, bold=True, valign="top")
    d.rect(660, 130, 280, 80, value="ECR (api + dkr)",
           fill="#FFFFFF", stroke=Colors.MAGENTA, stroke_width=2, fontsize=11, bold=True)
    d.rect(660, 220, 280, 80, value="CloudWatch Logs",
           fill="#FFFFFF", stroke=Colors.MAGENTA, stroke_width=2, fontsize=11, bold=True)
    d.icon("s3", 790, 330, label="S3 (image layers)")

    d.note(40, 520, 920, 70,
           value=("◾ 解法: Fargate (awsvpc) のイメージ Pull には ECR を PrivateLink 化する必要あり\n"
                  "  ・ecr.api (認証) + ecr.dkr (レジストリ) の 2 つ + CloudWatch Logs + S3 (レイヤ格納先)\n"
                  "  ・S3 だけは Gateway EP (無料)、他は Interface EP。これで PubIP 不要・NAT 不要"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-222.drawio")


# ---------------------------------------------------------------------------
# SAP-223 — Route 53 Resolver Inbound: オンプレ → AWS PHZ 解決 (クロス VPC)
# ---------------------------------------------------------------------------
def make_sap_223():
    d = Diagram("SAP-223: Route 53 Resolver Inbound + PHZ Association (クロス VPC)", 1000, 600, "sap-223")

    # On-prem
    d.group_onprem(40, 80, 240, 420, "On-premises")
    d.rect(60, 150, 200, 60,
           value="オンプレ DNS",
           fill="#FFFFFF", stroke=Colors.GRAY, stroke_width=2, fontsize=11, bold=True)
    d.rect(60, 230, 200, 60,
           value="条件転送設定&#10;aws.internal → Inbound EP IP",
           fill="#FFF8E1", stroke=Colors.YELLOW, stroke_width=2, fontsize=10, bold=True)
    d.rect(60, 310, 200, 60, value="DX / VPN",
           fill="#FEF3F2", stroke=Colors.RED, stroke_width=2, fontsize=10, bold=True)

    # Network VPC (Inbound EP)
    d.group_vpc(310, 80, 280, 420, "Network VPC")
    inbound = d.icon("route_53", 420, 160, label="Inbound&#10;Resolver EP")
    d.rect(340, 240, 220, 90,
           value="各 AZ にENI&#10;2 つのプライベート IP&#10;(オンプレ DNS から参照)",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    d.rect(340, 350, 220, 90,
           value="PHZ aws.internal を&#10;Network VPC に Associate&#10;→ Resolver が応答",
           fill="#FFF8E1", stroke=Colors.YELLOW, stroke_width=2, fontsize=10, bold=True)
    d.arrow_xy(260, 270, 420, 180, color=Colors.BLUE, label="DNS Query")

    # Other VPC
    d.group_vpc(620, 80, 340, 420, "App VPC (Other)")
    d.rect(650, 140, 280, 60,
           value="Route 53 PHZ (aws.internal)&#10;所有者 = Central Account",
           fill="#FFF8E1", stroke=Colors.YELLOW, stroke_width=2, fontsize=10, bold=True)
    d.rect(650, 220, 280, 80,
           value="A レコード群&#10;api.aws.internal → NLB Private IP",
           fill="#FFFFFF", stroke=Colors.NAV, fontsize=10)
    d.rect(650, 320, 280, 80,
           value="Network VPC と App VPC の両方に&#10;PHZ を Associate",
           fill="#EBF5E8", stroke=Colors.S3_GREEN, stroke_width=2, fontsize=10, bold=True)
    d.arrow_xy(590, 400, 650, 360, color=Colors.S3_GREEN, dashed=True, label="共有アソシエーション")

    d.note(40, 520, 920, 70,
           value=("◾ 解法: オンプレ → AWS PHZ の解決には Inbound Resolver EP + PHZ を Network VPC に Associate\n"
                  "  ・オンプレ DNS は Inbound EP の IP へ条件転送 (aws.internal ゾーン)\n"
                  "  ・PHZ は複数 VPC に Associate 可能 (所有 Account + 他 VPC)"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-223.drawio")


# ---------------------------------------------------------------------------
# SAP-239 — 10 VPC → 単一サービス VPC を PrivateLink で (CIDR 重複回避)
# ---------------------------------------------------------------------------
def make_sap_239():
    d = Diagram("SAP-239: 10 VPC → Service VPC を PrivateLink で疎結合化", 1000, 600, "sap-239")

    # Consumers
    d.group_account(40, 80, 300, 420, "Consumer Accounts (×10 VPC)")
    for i in range(3):
        d.group_vpc(60, 120 + i * 110, 260, 100, f"Consumer VPC #{i+1} (CIDR 重複許容)")
        d.icon("endpoint", 110, 160 + i * 110, label="Interface EP")
        d.icon("ec2", 240, 160 + i * 110, label="App")
    d.rect(60, 460, 260, 30,
           value="…… 残り 7 VPC も同様",
           fill="#F5F5F5", stroke=Colors.GRAY, fontsize=10)

    # Service VPC
    d.group_account(380, 80, 580, 420, "Service Provider VPC")
    eps = d.rect(420, 140, 220, 70,
                 value="VPC Endpoint Service",
                 fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=11, bold=True)
    nlb = d.icon("nlb", 700, 150, label="NLB")
    d.rect(800, 150, 140, 70,
           value="Backend App&#10;(EC2/Fargate)",
           fill="#FFFFFF", stroke=Colors.NAV, stroke_width=2, fontsize=11, bold=True)
    d.rect(420, 250, 520, 80,
           value="Allow-list: 10 個の Consumer Account を追加&#10;(Principal = arn:aws:iam::<acct>:root)",
           fill="#FFF8E1", stroke=Colors.YELLOW, stroke_width=2, fontsize=10, bold=True)
    d.rect(420, 350, 520, 130,
           value="★ メリット&#10;• CIDR 重複を気にしなくてよい (NAT/Peering 不要)&#10;• 疎結合: Provider 側で Endpoint Service の許可リスト管理だけ&#10;• TGW ルーティング・SG 参照不要",
           fill="#EBF5E8", stroke=Colors.S3_GREEN, stroke_width=2, fontsize=10, bold=True)

    d.arrow_xy(340, 170, 420, 170, color=Colors.BLUE, label="PrivateLink (単方向)")
    d.arrow(eps, nlb, color=Colors.BLUE)
    d.arrow_xy(750, 185, 800, 185, color=Colors.NAV)

    d.note(40, 520, 920, 70,
           value=("◾ 解法: Service VPC に NLB + Endpoint Service を構成 → Consumer VPC は Interface EP で接続\n"
                  "  ・Transit Gateway / VPC Peering と異なり CIDR 重複を考慮する必要なし\n"
                  "  ・一方向 (Consumer → Service) だが API コール用途には十分"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-239.drawio")


# ---------------------------------------------------------------------------
# SAP-240 — クロスアカウント PHZ 関連付け (手順)
# ---------------------------------------------------------------------------
def make_sap_240():
    d = Diagram("SAP-240: クロスアカウント PHZ を VPC に関連付ける手順", 1000, 600, "sap-240")

    # Account A
    d.group_account(40, 80, 420, 430, "Account A (PHZ 所有)")
    d.rect(70, 130, 360, 80,
           value="Route 53 Private Hosted Zone&#10;example.internal",
           fill="#FFF8E1", stroke=Colors.YELLOW, stroke_width=2, fontsize=11, bold=True)
    d.rect(70, 230, 360, 80,
           value="STEP 1: create-vpc-association-authorization&#10;→ Account B の VPC ID を認可",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    d.rect(70, 330, 360, 80,
           value="STEP 3 (任意): delete-authorization (後片付け)",
           fill="#F5F5F5", stroke=Colors.GRAY, fontsize=10)
    d.rect(70, 420, 360, 70,
           value="※ マネージドコンソールでは不可&#10;CLI/SDK/CloudFormation のみ",
           fill="#FEF3F2", stroke=Colors.RED, stroke_width=2, fontsize=10, bold=True)

    # Account B
    d.group_account(500, 80, 460, 430, "Account B (VPC 所有)")
    d.group_vpc(520, 130, 420, 150, "VPC (例: 10.10.0.0/16)")
    d.icon("ec2", 560, 180, label="EC2")
    d.rect(700, 175, 220, 60, value="EC2 は PHZ FQDN を解決可",
           fill="#EBF5E8", stroke=Colors.S3_GREEN, stroke_width=2, fontsize=10, bold=True)
    d.rect(520, 300, 420, 80,
           value="STEP 2: associate-vpc-with-hosted-zone&#10;(Account B 側で実行 / --hosted-zone-id = Acct A のゾーン)",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    d.rect(520, 400, 420, 80,
           value="結果: Account B VPC の EC2 が Account A の PHZ レコードを解決できる",
           fill="#FFF8E1", stroke=Colors.YELLOW, stroke_width=2, fontsize=10, bold=True)

    d.arrow_xy(430, 270, 520, 340, color=Colors.BLUE, label="VPC 認可")
    d.arrow_xy(430, 170, 520, 200, color=Colors.S3_GREEN, label="解決レコード提供")

    d.note(40, 530, 920, 60,
           value=("◾ 手順: (A) create-vpc-association-authorization → (B) associate-vpc-with-hosted-zone\n"
                  "  ・同一アカウントなら単純な『Associate』のみで完結。クロスアカウントの場合だけ認可が必要"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-240.drawio")


# ---------------------------------------------------------------------------
# SAP-288 — S3 データレイクへ VPC Endpoint + EP ポリシーで最小権限
# ---------------------------------------------------------------------------
def make_sap_288():
    d = Diagram("SAP-288: 複数アカウント → データレイク S3 を Gateway EP で閉域化", 1000, 600, "sap-288")

    # Consumer accounts
    d.group_account(40, 80, 300, 430, "Consumer Accounts (複数)")
    for i in range(3):
        d.group_vpc(60, 120 + i * 115, 260, 105, f"Consumer VPC #{i+1}")
        d.icon("ec2", 90, 160 + i * 115, label="Analytics App")
        d.icon("endpoint", 230, 160 + i * 115, label="Gateway EP (S3)")

    # Data Lake account
    d.group_account(380, 80, 580, 430, "Data Lake Account")
    s3 = d.icon("s3", 430, 150, label="S3 Bucket&#10;(data-lake)")
    d.rect(530, 130, 420, 100,
           value="Bucket Policy: aws:sourceVpce = vpce-xxx (Consumer 毎)&#10;+ aws:PrincipalOrgID = o-xxx で Organizations 統制",
           fill="#FFF8E1", stroke=Colors.YELLOW, stroke_width=2, fontsize=10, bold=True)
    d.rect(430, 250, 520, 90,
           value="VPC Endpoint Policy&#10;各 Consumer の EP に『自テナントの prefix のみ許可』を設定",
           fill="#EBF1FF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)
    d.rect(430, 360, 520, 140,
           value="★ 多層防御の4点セット&#10;1) Gateway EP (無料・プライベート経路)&#10;2) EP ポリシー (Consumer 側・持ち出し制限)&#10;3) Bucket Policy: aws:sourceVpce 条件 (Provider 側)&#10;4) Bucket Policy: aws:PrincipalOrgID 条件 (Org 限定)",
           fill="#EBF5E8", stroke=Colors.S3_GREEN, stroke_width=2, fontsize=10, bold=True)
    d.arrow_xy(340, 200, 430, 175, color=Colors.GREEN, label="プライベート経路")

    d.note(40, 530, 920, 60,
           value=("◾ 解法: Gateway EP + EP ポリシー + Bucket ポリシー (aws:sourceVpce / PrincipalOrgID) の 4 層防御\n"
                  "  ・インターネット非経由で複数アカウントから安全にデータレイクへアクセス"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/SAP-288.drawio")


if __name__ == "__main__":
    make_sap_54()
    make_sap_78()
    make_sap_108()
    make_sap_112()
    make_sap_116()
    make_sap_121()
    make_sap_139()
    make_sap_162()
    make_sap_180()
    make_sap_187()
    make_sap_200()
    make_sap_207()
    make_sap_221()
    make_sap_222()
    make_sap_223()
    make_sap_239()
    make_sap_240()
    make_sap_288()
    print("Generated 18 drawio files in", OUT_DIR)
