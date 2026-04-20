"""Generate 25 drawio files for VPC Endpoints / PrivateLink / Route53 Resolver / PHZ topics
covering UDEMY questions (num 300-674).
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drawio_builder import Diagram, Colors

OUT_DIR = "/Users/aki/aws-sap/docs/diagrams/per-question"
os.makedirs(OUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# UDEMY-017 (num 316) — S3 Gateway EP + aws:sourceVpce bucket policy
# ---------------------------------------------------------------------------
def make_017():
    d = Diagram("UDEMY-017: S3 Gateway Endpoint + aws:sourceVpce (VPC限定アクセス)", 1000, 600, "udemy-017")

    # Left: VPC with EC2 + GW EP
    d.group_vpc(60, 70, 420, 360, "VPC A (App Account)")
    d.text(80, 100, 200, 20, "Private Subnet", bold=True, align="left")
    ec2 = d.icon("ec2", 100, 140, label="EC2 (App)")
    rt = d.rect(230, 140, 160, 60,
                value="Route Table&#10;S3 prefix list → vpce-abc",
                fill="#FFFFFF", stroke=Colors.GREEN, stroke_width=2,
                fontsize=10, bold=True)
    gw_ep = d.icon("endpoint", 410, 140, label="Gateway EP\n(S3用/無料)")
    d.arrow(ec2, rt, color=Colors.GREEN)
    d.arrow(rt, gw_ep, color=Colors.GREEN)

    # Right: S3 bucket
    d.group_account(540, 70, 400, 360, "Data Repo Account")
    s3 = d.icon("s3", 740, 140, label="S3 Bucket\n(中央データ)")
    d.arrow(gw_ep, s3, color=Colors.GREEN, label="プライベート経路")

    # Bucket policy
    d.note(560, 230, 380, 170,
           value=("Bucket Policy (aws:sourceVpce 条件):\n\n"
                  '{\n'
                  '  "Effect": "Allow",\n'
                  '  "Principal": "*",\n'
                  '  "Action": "s3:GetObject",\n'
                  '  "Condition": {\n'
                  '    "StringEquals": {\n'
                  '      "aws:sourceVpce": "vpce-abc"\n'
                  '    }\n'
                  '  }\n'
                  '}\n'
                  "→ 特定 VPCEからのみ許可"),
           stroke=Colors.GREEN)

    # Bottom note
    d.note(60, 450, 880, 130,
           value=("◾ 解法: VPC Gateway Endpoint + バケットポリシーで aws:sourceVpce を条件付け\n"
                  "  ・パブリック経路を使わずに S3 にアクセス → セキュリティ要件\n"
                  "  ・最小権限: VPC 毎に固有の VPCE ID を許可リストに\n"
                  "  ・Gateway EP は S3 / DynamoDB のみ対応 (無料)\n"
                  "◾ 誤答: IAM ポリシー単独では「VPC縛り」ができない / NAT GW 経由 = パブリック経路"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-017.drawio")


# ---------------------------------------------------------------------------
# UDEMY-021 (num 320) — Interface EP Hub-and-Spoke (Centralized VPC Endpoint)
# ---------------------------------------------------------------------------
def make_021():
    d = Diagram("UDEMY-021: Interface EP 集約 (Central VPC + TGW Hub-Spoke)", 1000, 600, "udemy-021")

    # Central shared-services VPC
    d.group_vpc(340, 70, 320, 250, "Shared Services VPC")
    d.icon("endpoint", 400, 130, label="Interface EP\nKMS/SSM/ECR/...")
    d.icon("endpoint", 530, 130, label="PHZ\n(Private DNS)")
    d.rect(360, 230, 280, 60,
           value="Route 53 Private Hosted Zone\n各EP の Private DNS を共有",
           fill="#FFFFFF", stroke=Colors.BLUE, stroke_width=2, fontsize=10, bold=True)

    # TGW in center bottom
    tgw = d.icon("transit_gateway", 475, 370, label="Transit Gateway")

    # Left VPCs (Spokes)
    d.group_vpc(40, 80, 260, 200, "Spoke VPC A")
    ec2a = d.icon("ec2", 100, 140, label="EC2")
    d.group_vpc(40, 310, 260, 170, "Spoke VPC B")
    ec2b = d.icon("ec2", 100, 370, label="EC2")

    # Right VPCs
    d.group_vpc(700, 80, 260, 200, "Spoke VPC C")
    ec2c = d.icon("ec2", 810, 140, label="EC2")
    d.group_vpc(700, 310, 260, 170, "Spoke VPC D")
    ec2d = d.icon("ec2", 810, 370, label="EC2")

    # Arrows to TGW
    d.arrow(ec2a, tgw, color=Colors.BLUE)
    d.arrow(ec2b, tgw, color=Colors.BLUE)
    d.arrow(ec2c, tgw, color=Colors.BLUE)
    d.arrow(ec2d, tgw, color=Colors.BLUE)
    # TGW -> shared VPC
    d.arrow_xy(500, 370, 500, 320, color=Colors.BLUE, label="共有EP利用")

    d.note(40, 500, 920, 85,
           value=("◾ 解法: 各 VPC に Interface EP を個別設置せず、Shared VPC に集約 → TGW で共有\n"
                  "  ・コスト削減: EP は有料 ($0.01/h × AZ) なので N倍削減\n"
                  "  ・Private DNS を PHZ 化して各 VPC に Associate → AWS API FQDN が解決できる\n"
                  "◾ 誤答: 各 VPC で個別EP = N倍コスト / NAT GW 経由 = データ転送料金 + パブリック経路"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-021.drawio")


# ---------------------------------------------------------------------------
# UDEMY-023 (num 322) — Transfer Family + NLB + PrivateLink (static IP SFTP)
# ---------------------------------------------------------------------------
def make_023():
    d = Diagram("UDEMY-023: SFTP 移行 — Transfer Family + NLB で固定 IP 維持", 1000, 600, "udemy-023")

    # On-prem customer
    d.group_onprem(40, 80, 240, 260, "顧客 (許可リスト)")
    d.rect(70, 140, 180, 50,
           value="Firewall\n許可リスト:\n固定 IP のみ")
    d.rect(70, 210, 180, 50,
           value="SFTP Client\n既存IPを変更不可",
           bold=True)

    # AWS side
    d.group_vpc(320, 80, 640, 360, "VPC")
    # public subnet
    d.text(340, 110, 200, 20, "Public Subnet", bold=True, align="left")
    nlb = d.icon("nlb", 380, 140, label="NLB\n(Elastic IP 固定)")
    d.text(340, 250, 200, 20, "Private Subnet", bold=True, align="left")
    tf = d.rect(380, 280, 120, 60,
                value="AWS Transfer\nFamily (SFTP)",
                fill="#FFF5EB", stroke=Colors.ORANGE, stroke_width=2, bold=True)
    d.arrow_xy(430, 195, 430, 280, color=Colors.BLUE, label="TCP 22")
    s3 = d.icon("s3", 700, 300, label="S3 Bucket\n(ファイル保存先)")
    d.arrow_xy(500, 310, 700, 325, color=Colors.GREEN)

    d.note(320, 460, 640, 120,
           value=("◾ 要件: SFTP の IP アドレス変更不可 (顧客ファイアウォール許可リスト)\n"
                  "◾ 解法: AWS Transfer Family (VPC_ENDPOINT) + NLB + Elastic IP\n"
                  "  ・Transfer Family は VPC_ENDPOINT モードにより NLB 背後に配置可能\n"
                  "  ・NLB に Elastic IP を静的に割り当て → 顧客側の許可リストを維持\n"
                  "  ・バックエンド S3 はゲートウェイ EP でプライベート接続\n"
                  "◾ 誤答: Transfer Family の PUBLIC モード = IP が変わる可能性 / ALB = TCP/SFTP非対応"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-023.drawio")


# ---------------------------------------------------------------------------
# UDEMY-029 (num 328) — PrivateLink log service (producer side setup)
# ---------------------------------------------------------------------------
def make_029():
    d = Diagram("UDEMY-029: PrivateLink サービスプロバイダ側 — EC2/NLB サブネット分離", 1000, 600, "udemy-029")

    # Provider VPC
    d.group_vpc(50, 70, 600, 440, "Log Service VPC (Provider)")

    # Service subnets
    d.rect(80, 110, 250, 180, value="", fill="#FFFFFF",
           stroke=Colors.GRAY, dashed=True)
    d.text(90, 115, 230, 20, "Log Service Subnets (複数AZ)", bold=True, align="left")
    d.icon("ec2", 110, 155, label="EC2 (Log)")
    d.icon("ec2", 230, 155, label="EC2 (Log)")
    d.icon("ec2", 170, 235, label="EC2 (Log)")

    # Endpoint service subnets (NLB)
    d.rect(360, 110, 260, 180, value="", fill="#FFFFFF",
           stroke=Colors.GRAY, dashed=True)
    d.text(370, 115, 230, 20, "Endpoint Subnets (NLB専用)", bold=True, align="left")
    nlb = d.icon("nlb", 450, 165, label="NLB")

    # Endpoint Service
    d.rect(120, 340, 460, 60,
           value="Endpoint Service (PrivateLink / com.amazonaws.vpce.xxx)",
           fill=Colors.LIGHT_BLUE_BG, stroke=Colors.BLUE, stroke_width=2, bold=True, fontsize=11)
    d.arrow_xy(475, 290, 300, 340, color=Colors.BLUE, label="NLBを紐付け")

    # Consumer VPC
    d.group_vpc(700, 70, 260, 270, "Consumer VPC (顧客側)")
    d.icon("endpoint", 810, 140, label="Interface EP")
    d.icon("ec2", 810, 240, label="EC2 Client")
    d.arrow_xy(840, 190, 840, 235, color=Colors.BLUE)

    d.arrow_xy(580, 370, 830, 170, color=Colors.BLUE, label="PrivateLink")

    d.note(50, 430, 910, 150,
           value=("◾ 要件: 数百顧客からのログを PrivateLink で受ける → プロバイダ側 VPC の設計\n"
                  "◾ 解法: サービスの EC2 と Endpoint 用 Subnet を分離 (NLBをEP用Subnetに)\n"
                  "  A. NLB を「Endpoint Subnets」に配置 → 1 AZ あたり 1 NLB ENI (IP 消費の想定が立てやすい)\n"
                  "  B. EC2 ログサービスは「Log Service Subnets」で独立させる → スケール/セキュリティ分離\n"
                  "  C. Endpoint Service(PrivateLink) に NLB を紐付け → 顧客は Interface EP で接続\n"
                  "◾ 誤答: EC2 と同じ Subnet に NLB 置く = IP 競合 / ALB = Endpoint Service 非対応"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-029.drawio")


# ---------------------------------------------------------------------------
# UDEMY-043 (num 342) — Gateway EP for S3 (NAT GW cost reduction)
# ---------------------------------------------------------------------------
def make_043():
    d = Diagram("UDEMY-043: S3 Gateway Endpoint で NAT GW データ処理料金を削減", 1000, 600, "udemy-043")

    # BEFORE (left)
    d.text(60, 60, 460, 24, "BEFORE: NAT GW 経由 (コスト高)", bold=True, fontsize=13, color=Colors.RED)
    d.group_vpc(60, 90, 460, 340, "VPC — EC2 が毎日 1.5TB を S3 ダウンロード")
    d.text(90, 125, 200, 20, "Private Subnet", bold=True, align="left")
    ec2_b = d.icon("ec2", 100, 160, label="EC2 (R&D)")
    d.text(90, 245, 200, 20, "Public Subnet", bold=True, align="left")
    nat_b = d.icon("nat_gateway", 230, 275, label="NAT GW")
    igw_b = d.rect(380, 280, 100, 50, value="IGW",
                   fill="#FFF5EB", stroke=Colors.ORANGE, stroke_width=2, bold=True)
    s3_b = d.icon("s3", 380, 160, label="S3")
    d.arrow(ec2_b, nat_b, color=Colors.RED)
    d.arrow(nat_b, igw_b, color=Colors.RED)
    d.arrow_xy(430, 280, 430, 210, color=Colors.RED, label="$0.045/GB\n× 1.5TB/日")

    # AFTER (right)
    d.text(540, 60, 420, 24, "AFTER: Gateway EP 経由 (コスト0)", bold=True, fontsize=13, color=Colors.GREEN)
    d.group_vpc(540, 90, 420, 340, "VPC")
    d.text(570, 125, 200, 20, "Private Subnet", bold=True, align="left")
    ec2_a = d.icon("ec2", 580, 160, label="EC2 (R&D)")
    rt = d.rect(690, 170, 150, 50,
                value="Route Table\nS3 prefix list\n→ vpce-xxx",
                fill="#FFFFFF", stroke=Colors.GREEN, stroke_width=2, bold=True, fontsize=9)
    gw = d.icon("endpoint", 870, 160, label="Gateway EP\n(無料)")
    d.arrow(ec2_a, rt, color=Colors.GREEN)
    d.arrow(rt, gw, color=Colors.GREEN)
    s3_a = d.icon("s3", 870, 290, label="S3")
    d.arrow(gw, s3_a, color=Colors.GREEN, label="プライベート経路")

    d.note(60, 450, 900, 130,
           value=("◾ 判断軸: S3 / DynamoDB 大量通信で NAT GW コスト爆発 → Gateway EP (無料) に置換\n"
                  "  ・Gateway EP: 時間課金なし、データ転送料金なし、Route Table にルート追加するだけ\n"
                  "  ・Interface EP for S3 (PrivateLink) は時間課金 + $0.01/GB → 同一 VPC 内からは無料の Gateway EP を選ぶ\n"
                  "  ・オンプレから S3 を使う時だけ Interface EP を併用"),
           stroke=Colors.GREEN)
    d.save(f"{OUT_DIR}/UDEMY-043.drawio")


# ---------------------------------------------------------------------------
# UDEMY-052 (num 351) — Route 53 Outbound Resolver (hybrid DNS to on-prem)
# ---------------------------------------------------------------------------
def make_052():
    d = Diagram("UDEMY-052: Route 53 Outbound Resolver — ハイブリッド DNS 転送", 1000, 600, "udemy-052")

    # AWS VPC
    d.group_vpc(40, 80, 460, 380, "VPC")
    d.text(70, 110, 200, 20, "Private Subnet", bold=True, align="left")
    ec2 = d.icon("ec2", 80, 145, label="EC2\n(Factory App)")
    r53 = d.rect(220, 145, 120, 50,
                 value="Route 53\nResolver (VPC)",
                 fill="#FFFFFF", stroke=Colors.PURPLE, stroke_width=2, bold=True, fontsize=10)
    d.arrow(ec2, r53, color=Colors.PURPLE, label="①DNS query\nfactory.internal")

    out_ep = d.rect(380, 145, 100, 50,
                    value="Outbound\nResolver EP",
                    fill="#FFFFFF", stroke=Colors.PURPLE, stroke_width=2, bold=True, fontsize=10)
    d.arrow(r53, out_ep, color=Colors.PURPLE, label="② 条件付き転送\n(Resolver Rule)")

    d.rect(80, 260, 400, 130,
           value=("Resolver Rule:\n"
                  "  domain = factory.internal\n"
                  "  type   = FORWARD\n"
                  "  target = 10.0.1.53, 10.0.1.54 (オンプレDNS)\n"
                  "  associate with VPC"),
           fill="#FFFFFF", stroke=Colors.PURPLE, bold=True, fontsize=10, align="left")

    # DX connection + on-prem
    dx = d.icon("direct_connect", 560, 150, label="Direct Connect")

    d.group_onprem(700, 80, 280, 380, "オンプレミス Factory NW")
    dns = d.rect(730, 180, 220, 70,
                 value="DNS Server (factory.internal)\nホスト: factory.internal",
                 fill="#FFFFFF", stroke=Colors.GRAY, bold=True, fontsize=11)
    d.arrow_xy(480, 170, 560, 170, color=Colors.PURPLE, label="③")
    d.arrow_xy(610, 170, 730, 200, color=Colors.PURPLE, label="④")

    d.note(40, 485, 940, 95,
           value=("◾ 要件: AWS の EC2 からオンプレの DNS (factory.internal) を解決したい\n"
                  "◾ 解法: Route 53 Outbound Resolver Endpoint + Resolver Rule (FORWARD)\n"
                  "  ・Outbound EP は VPC 内に ENI を置き、DX/VPN 経由でオンプレ DNS にクエリを転送\n"
                  "  ・逆方向 (オンプレ → AWS の PHZ 解決) には Inbound Resolver EP を併用"),
           stroke=Colors.PURPLE)
    d.save(f"{OUT_DIR}/UDEMY-052.drawio")


# ---------------------------------------------------------------------------
# UDEMY-057 (num 356) — S3 Interface EP from on-prem via DX / cross-account
# ---------------------------------------------------------------------------
def make_057():
    d = Diagram("UDEMY-057: オンプレ → S3 を PrivateLink (Interface EP for S3) で到達", 1000, 600, "udemy-057")

    d.group_onprem(40, 80, 220, 360, "研究施設 (On-Prem)")
    on_app = d.rect(70, 180, 160, 80,
                    value="臨床試験データ\nアップロードクライアント")

    dx = d.icon("direct_connect", 300, 200, label="Direct Connect\nor Site-to-Site VPN")
    d.arrow_xy(230, 220, 300, 220, color=Colors.BLUE)

    # AWS hub VPC with EP
    d.group_vpc(420, 80, 260, 360, "Hub VPC")
    if_ep = d.icon("endpoint", 500, 160, label="Interface EP\nfor S3")
    resv = d.rect(450, 260, 200, 60,
                  value="Inbound Resolver\nEP (オンプレから\nEP FQDN 解決)",
                  fill="#FFFFFF", stroke=Colors.PURPLE, stroke_width=2, bold=True, fontsize=10)
    d.arrow_xy(380, 220, 500, 185, color=Colors.BLUE, label="①PrivateLink")
    d.arrow_xy(380, 260, 450, 290, color=Colors.PURPLE, label="DNSクエリ")

    # S3 buckets in 3 accounts
    d.group_account(720, 80, 240, 100, "Acct 1")
    d.icon("s3", 830, 100, label="S3 (試験A)")
    d.group_account(720, 190, 240, 100, "Acct 2")
    d.icon("s3", 830, 210, label="S3 (試験B)")
    d.group_account(720, 300, 240, 100, "Acct 3")
    d.icon("s3", 830, 320, label="S3 (試験C)")
    d.arrow_xy(550, 185, 720, 125, color=Colors.GREEN)
    d.arrow_xy(550, 185, 720, 230, color=Colors.GREEN)
    d.arrow_xy(550, 185, 720, 335, color=Colors.GREEN)

    d.note(40, 470, 920, 110,
           value=("◾ 要件: 複数アカウントのS3 へオンプレからプライベート (非インターネット) で書き込み\n"
                  "◾ 解法: (A) Direct Connect / VPN を確立、(C) Hub VPC に Interface EP for S3 を作成\n"
                  "  ・Gateway EP はオンプレから到達不可 → Interface EP for S3 (PrivateLink) が必須\n"
                  "  ・DX未構築 = インターネット経由 NG → 要件未達\n"
                  "  ・S3 バケットポリシーで aws:sourceVpce による制限で最小権限化"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-057.drawio")


# ---------------------------------------------------------------------------
# UDEMY-066 (num 365) — AWS Transfer Family + PrivateLink (SFTP)
# ---------------------------------------------------------------------------
def make_066():
    d = Diagram("UDEMY-066: SFTP 移行 — AWS Transfer Family (VPC_ENDPOINT 型)", 1000, 600, "udemy-066")

    d.group_onprem(40, 80, 200, 360, "Supplier\n(1000+ 店舗)")
    d.rect(60, 180, 160, 70, value="SFTP Client\n(許可リスト固定IP)")

    # Internet / Customer Gateway
    igw = d.rect(280, 200, 80, 40, value="Internet",
                 fill=Colors.LIGHT_GRAY_BG, stroke=Colors.GRAY, bold=True)
    d.arrow_xy(240, 220, 280, 220, color=Colors.GRAY)

    # AWS VPC
    d.group_vpc(400, 80, 560, 360, "VPC")
    d.text(430, 110, 200, 20, "Public Subnet", bold=True, align="left")
    nlb = d.icon("nlb", 450, 140, label="NLB\n(Elastic IP 固定)")
    d.arrow_xy(360, 220, 450, 180, color=Colors.BLUE)

    d.text(430, 250, 200, 20, "Private Subnet", bold=True, align="left")
    tf = d.rect(430, 280, 160, 60,
                value="AWS Transfer\nFamily (SFTP)",
                fill="#FFF5EB", stroke=Colors.ORANGE, stroke_width=2, bold=True)
    d.arrow_xy(475, 195, 475, 280, color=Colors.BLUE, label="TCP 22")
    s3 = d.icon("s3", 800, 180, label="S3\n(日次データ)")
    d.arrow_xy(590, 310, 800, 215, color=Colors.GREEN)

    d.note(40, 460, 920, 120,
           value=("◾ 要件: オンプレ SFTP → AWS 移行、管理最小化、1000 拠点から日次アップロード、IP 変更可否は固定が理想\n"
                  "◾ 解法: AWS Transfer Family + NLB (Elastic IP) + S3 バケット\n"
                  "  ・Transfer Family はマネージド SFTP → サーバ管理不要、自動スケール、IAM ベースで認証\n"
                  "  ・VPC_ENDPOINT モード + NLB により固定 IP を実現\n"
                  "◾ 誤答: EC2 自前 SFTP = 管理負荷大 / API Gateway = SFTP 非対応 / S3 直接 = SFTPでない"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-066.drawio")


# ---------------------------------------------------------------------------
# UDEMY-078 (num 377) — VPC DNS attributes + PHZ
# ---------------------------------------------------------------------------
def make_078():
    d = Diagram("UDEMY-078: VPC DNS 設定 — enableDnsHostnames/enableDnsSupport + PHZ", 1000, 600, "udemy-078")

    d.group_vpc(40, 80, 600, 400, "VPC (172.31.0.0/16)")
    ec2_pub = d.icon("ec2", 110, 140, label="EC2\n(Public IP)")
    ec2_priv = d.icon("ec2", 110, 280, label="EC2\n(Private)")
    r53 = d.rect(280, 200, 200, 80,
                 value="Route 53 Resolver\n(.2 リゾルバー)",
                 fill="#FFFFFF", stroke=Colors.PURPLE, stroke_width=2, bold=True)
    d.arrow(ec2_pub, r53, color=Colors.PURPLE)
    d.arrow(ec2_priv, r53, color=Colors.PURPLE)
    phz = d.rect(520, 220, 100, 40, value="PHZ",
                 fill=Colors.LIGHT_BLUE_BG, stroke=Colors.BLUE, bold=True)
    d.arrow(r53, phz, color=Colors.BLUE)

    # Requirements / settings box
    d.note(680, 80, 280, 200,
           value=("必要な VPC 設定 (両方 true):\n\n"
                  "① enableDnsSupport = true\n"
                  "   → .2 リゾルバーが動作\n"
                  "   → PHZ/AWS 標準 DNS 解決\n\n"
                  "② enableDnsHostnames = true\n"
                  "   → Public IP を持つ EC2 に\n"
                  "     Public DNS 名が付与\n"
                  "   → PHZ を利用する前提"),
           stroke=Colors.BLUE)

    d.note(680, 300, 280, 180,
           value=("PHZ を利用する前提:\n"
                  "・VPC の両属性が true\n"
                  "・PHZ を VPC に Associate\n\n"
                  "引っ掛け:\n"
                  "・Support のみ = PHZ OK だが\n"
                  "  Public DNS 名がつかない\n"
                  "・Hostnames のみ = 不可\n"
                  "  (Support 前提のため)"),
           stroke=Colors.RED)

    d.note(40, 500, 920, 80,
           value=("◾ 要件: パブリックホスト名付与 + PHZ で DNS 解決\n"
                  "◾ 解法: enableDnsSupport=true && enableDnsHostnames=true\n"
                  "  Support のみだと public DNS 名が付与されない。Hostnames のみは Support を前提とするため無効。"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-078.drawio")


# ---------------------------------------------------------------------------
# UDEMY-087 (num 386) — GWLB Endpoint Service (centralized egress firewall)
# ---------------------------------------------------------------------------
def make_087():
    d = Diagram("UDEMY-087: Gateway Load Balancer Endpoint で共有ファイアウォール集約", 1000, 600, "udemy-087")

    # Spoke VPCs
    d.group_vpc(40, 80, 240, 180, "Spoke VPC A")
    d.icon("ec2", 100, 130, label="EC2")
    gwlbe_a = d.rect(50, 200, 220, 40, value="GWLB Endpoint (GWLBE)",
                     fill=Colors.LIGHT_BLUE_BG, stroke=Colors.BLUE, bold=True)

    d.group_vpc(40, 290, 240, 180, "Spoke VPC B")
    d.icon("ec2", 100, 340, label="EC2")
    gwlbe_b = d.rect(50, 410, 220, 40, value="GWLB Endpoint (GWLBE)",
                     fill=Colors.LIGHT_BLUE_BG, stroke=Colors.BLUE, bold=True)

    # Shared Services VPC (firewall appliances)
    d.group_vpc(340, 80, 320, 380, "Shared Services VPC")
    gwlb = d.rect(400, 140, 200, 50,
                  value="Gateway Load Balancer\n(Appliance側)",
                  fill=Colors.LIGHT_YELLOW_BG, stroke=Colors.YELLOW, bold=True, stroke_width=2)
    d.icon("ec2", 380, 230, label="FW Appliance AZ-a")
    d.icon("ec2", 500, 230, label="FW Appliance AZ-b")
    es = d.rect(380, 340, 240, 60,
                value="Endpoint Service\n(GWLB をバックエンドに)",
                fill="#FFFFFF", stroke=Colors.BLUE, stroke_width=2, bold=True)
    d.arrow_xy(500, 190, 500, 340, color=Colors.BLUE)

    d.arrow_xy(280, 220, 380, 365, color=Colors.BLUE, label="PrivateLink")
    d.arrow_xy(280, 430, 380, 370, color=Colors.BLUE, label="PrivateLink")

    # Egress
    igw = d.rect(720, 250, 100, 50, value="IGW",
                 fill="#FFF5EB", stroke=Colors.ORANGE, stroke_width=2, bold=True)
    d.arrow(es, igw, color=Colors.ORANGE, label="検査後 Egress")
    d.rect(850, 250, 120, 50, value="Internet",
           fill=Colors.LIGHT_GRAY_BG, stroke=Colors.GRAY, bold=True)

    d.note(40, 500, 930, 80,
           value=("◾ 要件: 全 Spoke VPC の Egress を 1 つの 3rd Party FW Appliance で検査 (単一リージョン、高可用)\n"
                  "◾ 解法: GWLB + GWLB Endpoint (PrivateLink) の集中検査パターン\n"
                  "  Spoke VPC に GWLBE (ENI) → Shared VPC の GWLB → FW Appliance (複数 AZ) → IGW"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-087.drawio")


# ---------------------------------------------------------------------------
# UDEMY-096 (num 395) — Hybrid DNS with Inbound & Outbound Resolver + PHZ
# ---------------------------------------------------------------------------
def make_096():
    d = Diagram("UDEMY-096: ハイブリッド DNS — Inbound/Outbound Resolver + PHZ", 1000, 600, "udemy-096")

    d.group_vpc(40, 70, 520, 420, "VPC")
    d.icon("ec2", 80, 140, label="ECS Task\n(App)")
    d.rect(220, 140, 280, 60,
           value="Route 53 Resolver (.2)\n+ PHZ: app.internal",
           fill="#FFFFFF", stroke=Colors.PURPLE, stroke_width=2, bold=True, fontsize=10)

    in_ep = d.rect(80, 280, 200, 70,
                   value="Inbound Resolver EP\n(オンプレ→AWS名前解決)",
                   fill="#FFFFFF", stroke=Colors.PURPLE, stroke_width=2, bold=True, fontsize=10)
    out_ep = d.rect(320, 280, 200, 70,
                    value="Outbound Resolver EP\n(AWS→オンプレ名前解決)",
                    fill="#FFFFFF", stroke=Colors.PURPLE, stroke_width=2, bold=True, fontsize=10)

    dx = d.icon("direct_connect", 600, 270, label="Direct Connect")

    d.group_onprem(720, 70, 240, 420, "オンプレ DC")
    d.rect(750, 140, 180, 70, value="Customer DB\ninventory.corp")
    d.rect(750, 280, 180, 70, value="On-Prem DNS\n(corp ドメイン)", bold=True)

    d.arrow_xy(280, 315, 600, 295, color=Colors.PURPLE, label="オンプレ→AWS問合せ")
    d.arrow_xy(520, 315, 600, 295, color=Colors.PURPLE)
    d.arrow_xy(650, 295, 750, 315, color=Colors.PURPLE)

    d.note(40, 510, 920, 70,
           value=("◾ Inbound EP  = オンプレ → AWS の PHZ (app.internal) を解決可能にする\n"
                  "◾ Outbound EP + Resolver Rule = AWS → オンプレ DNS (corp) へ条件付き転送\n"
                  "◾ PHZ  = VPC 内限定の DNS 名前空間。Associate した VPC からのみ解決可"),
           stroke=Colors.PURPLE)
    d.save(f"{OUT_DIR}/UDEMY-096.drawio")


# ---------------------------------------------------------------------------
# UDEMY-105 (num 404) — Interface EP for SMB/EFS access from on-prem? Actually 404 is about EFS.
# Skipping; focus elsewhere.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# UDEMY-106 (num 405) — Interface EP for KMS (PrivateLink)
# ---------------------------------------------------------------------------
def make_106():
    d = Diagram("UDEMY-106: KMS を Interface EP (PrivateLink) でプライベート利用", 1000, 600, "udemy-106")

    d.group_vpc(60, 80, 460, 400, "VPC")
    d.text(90, 110, 200, 20, "Private Subnet (AZ-a)", bold=True, align="left")
    ec2 = d.icon("ec2", 100, 140, label="ECS Task / EC2")
    d.text(90, 240, 200, 20, "Private Subnet (AZ-b)", bold=True, align="left")
    ec2b = d.icon("ec2", 100, 270, label="ECS Task / EC2")

    # Interface EP
    eni_a = d.icon("endpoint", 350, 140, label="Interface EP\n(KMS AZ-a ENI)")
    eni_b = d.icon("endpoint", 350, 270, label="Interface EP\n(KMS AZ-b ENI)")
    d.arrow(ec2, eni_a, color=Colors.BLUE)
    d.arrow(ec2b, eni_b, color=Colors.BLUE)

    # KMS service
    kms = d.rect(620, 200, 240, 80,
                 value="AWS KMS Service\n(com.amazonaws.region.kms)",
                 fill="#FFF5EB", stroke=Colors.ORANGE, stroke_width=2, bold=True)
    d.arrow_xy(400, 165, 620, 230, color=Colors.BLUE, label="PrivateLink")
    d.arrow_xy(400, 295, 620, 260, color=Colors.BLUE)

    d.note(60, 500, 900, 80,
           value=("◾ 要件: CloudFront → ALB → ECS のアプリが KMS を使う。パブリック経路なし、コンプラ要件\n"
                  "◾ 解法: com.amazonaws.region.kms の Interface EP を複数 AZ に作成 + Private DNS 有効化\n"
                  "  → アプリの SDK が既存 FQDN で解決 → ENI の私有IP へルーティング (PrivateLink)"),
           stroke=Colors.BLUE)
    d.save(f"{OUT_DIR}/UDEMY-106.drawio")


# ---------------------------------------------------------------------------
# UDEMY-114 (num 413) — 多VPC × オンプレ ハイブリッド接続 (TGW + DX の最適化)
# ---------------------------------------------------------------------------
def make_114():
    d = Diagram("UDEMY-114: 多数 VPC + オンプレ 接続最適化 — TGW + DX Gateway", 1000, 600, "udemy-114")

    # On-prem
    d.group_onprem(40, 80, 200, 360, "複数国 On-Prem DC")
    d.rect(60, 180, 160, 70, value="DC-1", bold=True)
    d.rect(60, 280, 160, 70, value="DC-2 / DC-3", bold=True)

    # DX Gateway
    dxgw = d.rect(280, 200, 160, 70,
                  value="Direct Connect\nGateway (Global)",
                  fill=Colors.LIGHT_YELLOW_BG, stroke=Colors.YELLOW, bold=True, stroke_width=2)
    d.arrow_xy(240, 230, 280, 230, color=Colors.YELLOW)

    # TGW
    tgw = d.icon("transit_gateway", 530, 215, label="Transit Gateway\n(Hub)")
    d.arrow_xy(440, 235, 530, 235, color=Colors.PURPLE, label="Transit VIF")

    # Shared Services VPC
    d.group_vpc(680, 80, 280, 120, "Shared Services VPC")
    d.icon("endpoint", 810, 100, label="Interface EP")

    # Spoke VPCs
    d.group_account(680, 220, 280, 100, "Acct A — VPC")
    d.icon("ec2", 810, 230, label="EC2")
    d.group_account(680, 340, 280, 100, "Acct B — VPC")
    d.icon("ec2", 810, 350, label="EC2")

    d.arrow_xy(580, 240, 680, 130, color=Colors.PURPLE)
    d.arrow_xy(580, 260, 680, 265, color=Colors.PURPLE)
    d.arrow_xy(580, 260, 680, 385, color=Colors.PURPLE)

    d.note(40, 470, 920, 110,
           value=("◾ 要件: 多国籍 + 多 VPC + 多アカウント → スケーラブルで管理しやすい接続\n"
                  "◾ 解法: Transit Gateway (RAM 共有) + Direct Connect Gateway を組合せ\n"
                  "  A. TGW を RAM で Organizations 全体に共有\n"
                  "  B. 各 VPC に TGW Attachment を作成\n"
                  "  C. DX Gateway 経由で多リージョン/多拠点からの接続を集約\n"
                  "◾ 誤答: 個別 VPN で N 対 M 接続 = 管理破綻"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-114.drawio")


# ---------------------------------------------------------------------------
# UDEMY-135 (num 434) — PrivateLink Provider w/ NLB cross-region
# ---------------------------------------------------------------------------
def make_135():
    d = Diagram("UDEMY-135: PrivateLink プロバイダ側 — NLB + Endpoint Service (クロスリージョン)", 1000, 600, "udemy-135")

    # Frankfurt provider
    d.group_vpc(40, 80, 460, 380, "Provider VPC (eu-central-1)")
    d.text(70, 110, 200, 20, "Private Subnets (複数AZ)", bold=True, align="left")
    d.icon("ec2", 80, 140, label="ERP EC2")
    d.icon("ec2", 180, 140, label="ERP EC2")
    d.icon("ec2", 280, 140, label="ERP EC2")
    nlb = d.icon("nlb", 380, 140, label="NLB")
    es = d.rect(80, 260, 380, 70,
                value="VPC Endpoint Service\n(com.amazonaws.vpce.eu-central-1.xxx)\n"
                      "→ 顧客アカウント ID を allowlist に追加",
                fill=Colors.LIGHT_BLUE_BG, stroke=Colors.BLUE, bold=True, fontsize=10)
    d.arrow_xy(410, 195, 270, 260, color=Colors.BLUE)

    # Consumer
    d.group_account(560, 80, 400, 380, "顧客 (別リージョンでも可)")
    d.group_vpc(580, 130, 360, 300, "Consumer VPC")
    d.icon("endpoint", 620, 180, label="Interface EP\n(com.amazonaws.vpce..)")
    d.icon("ec2", 770, 180, label="EC2 Client")
    d.arrow_xy(670, 200, 770, 200, color=Colors.BLUE)
    d.rect(600, 300, 320, 100,
           value=("Consumer 側の手順:\n"
                  "1. Service Name をプロバイダから受取\n"
                  "2. Interface EP 作成 → 承認されると接続\n"
                  "3. Private DNS (Private Hosted Zone) を付与で透過利用"),
           fill="#FFFFFF", stroke=Colors.BLUE, fontsize=10, align="left")
    d.arrow_xy(470, 295, 600, 205, color=Colors.BLUE, label="PrivateLink")

    d.note(40, 475, 920, 105,
           value=("◾ 要件: ERP を他社顧客にプライベート提供。ALB は Endpoint Service 非対応 → NLB が必須\n"
                  "◾ 解法: プロバイダ側 = NLB + Endpoint Service (承認制)\n"
                  "  ・Endpoint Service の allowlist に顧客のアカウント ARN を追加\n"
                  "  ・Private DNS 名を設定するとドメイン検証後に顧客 VPC で透過解決可\n"
                  "  ・Provider NLB Target は TCP/TLS。ALB は Endpoint Service のバックエンド不可"),
           stroke=Colors.BLUE)
    d.save(f"{OUT_DIR}/UDEMY-135.drawio")


# ---------------------------------------------------------------------------
# UDEMY-140 (num 439) — Private API Gateway + Interface EP + resource policy
# ---------------------------------------------------------------------------
def make_140():
    d = Diagram("UDEMY-140: Private API Gateway — Interface EP + リソースポリシー必須", 1000, 600, "udemy-140")

    d.group_vpc(60, 80, 420, 380, "VPC")
    d.text(90, 110, 200, 20, "Private Subnet", bold=True, align="left")
    ec2 = d.icon("ec2", 100, 140, label="HR EC2")
    if_ep = d.icon("endpoint", 290, 140, label="Interface EP\n(execute-api)")
    d.arrow(ec2, if_ep, color=Colors.BLUE)

    # API Gateway Private
    api = d.rect(540, 130, 240, 70,
                 value="API Gateway\n(Private エンドポイント)",
                 fill="#FFF5EB", stroke=Colors.ORANGE, stroke_width=2, bold=True)
    lam = d.rect(540, 230, 240, 70,
                 value="Lambda (HRバックエンド)",
                 fill="#FFF5EB", stroke=Colors.ORANGE, stroke_width=2, bold=True)
    d.arrow_xy(340, 165, 540, 165, color=Colors.BLUE, label="PrivateLink")
    d.arrow(api, lam, color=Colors.ORANGE)

    # Resource policy box (critical!)
    d.note(540, 320, 400, 140,
           value=("🔑 API Gateway Resource Policy (必須):\n\n"
                  '{\n'
                  '  "Effect": "Allow",\n'
                  '  "Principal": "*",\n'
                  '  "Action": "execute-api:Invoke",\n'
                  '  "Resource": "execute-api:/*/*/*",\n'
                  '  "Condition": {\n'
                  '    "StringEquals": {\n'
                  '      "aws:SourceVpce": "vpce-xxx"\n'
                  '    }\n'
                  '  }\n'
                  "}"),
           stroke=Colors.RED)

    d.note(60, 470, 900, 110,
           value=("◾ 症状: Private API 作成済みだが接続失敗\n"
                  "◾ 原因候補: ① VPC Interface EP 未作成 (execute-api)、② API Gateway リソースポリシー未設定\n"
                  "◾ 解法: Interface EP を作成 + API Gateway リソースポリシーで aws:SourceVpce を許可\n"
                  "◾ 追加確認: Private DNS 有効化、SG がポート 443 を許可、EP の SG も 443 許可"),
           stroke=Colors.RED)
    d.save(f"{OUT_DIR}/UDEMY-140.drawio")


# ---------------------------------------------------------------------------
# UDEMY-151 (num 450) — Cross-account S3 via Gateway EP + bucket policy
# ---------------------------------------------------------------------------
def make_151():
    d = Diagram("UDEMY-151: クロスアカウント S3 — Gateway EP + バケットポリシー", 1000, 600, "udemy-151")

    d.group_account(60, 70, 420, 420, "Analytics Account")
    d.group_vpc(90, 110, 360, 360, "VPC (Analytics)")
    d.text(110, 140, 200, 20, "Public Subnet", bold=True, align="left")
    ec2 = d.icon("ec2", 110, 170, label="EC2 分析\n(IAM Role あり)")
    rt = d.rect(260, 170, 160, 50,
                value="Route Table\n→ vpce-xxx",
                fill="#FFFFFF", stroke=Colors.GREEN, stroke_width=2, bold=True, fontsize=10)
    gw = d.icon("endpoint", 260, 260, label="Gateway EP (S3)")

    d.arrow(ec2, rt, color=Colors.GREEN)
    d.arrow_xy(340, 220, 290, 260, color=Colors.GREEN)

    d.group_account(540, 70, 420, 420, "Data Lake Account")
    s3 = d.icon("s3", 680, 170, label="S3 Data Lake Bucket")
    d.arrow_xy(310, 310, 680, 200, color=Colors.GREEN, label="Cross-Acct")

    d.note(560, 260, 380, 210,
           value=("Bucket Policy (両方の許可が必要):\n"
                  "1) aws:sourceVpce = vpce-xxx\n"
                  "   → 特定 VPCE からのみ\n\n"
                  "2) Principal: {\n"
                  "     \"AWS\": \"arn:aws:iam::ANALYTICS_ACCT:role/EC2Role\"\n"
                  "   }\n"
                  "   → 相手アカウントの IAM Role\n\n"
                  "※ IAM Role 側にも s3:GetObject 許可が必要\n"
                  "※ KMS 使用時は KMS Key Policy も両側許可"),
           stroke=Colors.GREEN)

    d.note(60, 505, 900, 75,
           value=("◾ 解法: (A) S3 Gateway EP を作成 + (E) バケットポリシーで aws:sourceVpce と 相手アカウント Principal を許可\n"
                  "◾ ポイント: クロスアカウント S3 アクセスは IAM (ロール側) + Bucket Policy の 双方向許可が必須"),
           stroke=Colors.GREEN)
    d.save(f"{OUT_DIR}/UDEMY-151.drawio")


# ---------------------------------------------------------------------------
# UDEMY-161 (num 460) — Shared VPC (RAM) + Resolver
# ---------------------------------------------------------------------------
def make_161():
    d = Diagram("UDEMY-161: Shared VPC (VPC共有) — Hub/Spoke + Resolver 集約", 1000, 600, "udemy-161")

    # Infrastructure (Hub) account
    d.group_account(40, 60, 480, 430, "Infrastructure (Hub) Account")
    d.group_vpc(70, 100, 420, 380, "Central VPC (Shared via RAM)")
    d.text(100, 130, 200, 20, "Subnet (RAM で共有)", bold=True, align="left")

    # Resolver endpoints in central VPC
    in_ep = d.rect(100, 160, 160, 60, value="Inbound\nResolver EP",
                   fill="#FFFFFF", stroke=Colors.PURPLE, stroke_width=2, bold=True, fontsize=10)
    out_ep = d.rect(290, 160, 160, 60, value="Outbound\nResolver EP",
                    fill="#FFFFFF", stroke=Colors.PURPLE, stroke_width=2, bold=True, fontsize=10)
    d.icon("endpoint", 195, 260, label="Interface EP")
    tgw = d.icon("transit_gateway", 330, 260, label="TGW Attach")

    # Spoke accounts sharing the VPC subnets
    d.group_account(560, 60, 400, 210, "Spoke Account A (同VPC)")
    d.rect(580, 110, 360, 140,
           value=("同じ Shared VPC のサブネットを利用\n"
                  "(RAM 共有されたサブネット内で ENI 作成)\n"
                  "EC2 / RDS / Lambda 等をデプロイ"),
           fill="#FFFFFF", stroke=Colors.BLUE, fontsize=11)

    d.group_account(560, 290, 400, 200, "Spoke Account B")
    d.rect(580, 340, 360, 130,
           value=("同じ Shared VPC を共有 → 同じ Resolver/EP を使える\n"
                  "アカウント分離しつつネットワーク集約"),
           fill="#FFFFFF", stroke=Colors.BLUE, fontsize=11)

    d.note(40, 505, 920, 75,
           value=("◾ 解法: (D) Central VPC 作成 → (A) RAM でサブネットを各メンバーアカウントに共有 → (B) 各アカウントが EC2 等をデプロイ\n"
                  "◾ 利点: Resolver/EP/NAT GW を1セットで集約、マルチアカウント運用のネットワーク集中管理"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-161.drawio")


# ---------------------------------------------------------------------------
# UDEMY-162 (num 461) — PrivateLink Consumer to SaaS
# ---------------------------------------------------------------------------
def make_162():
    d = Diagram("UDEMY-162: SaaS 利用側 — Interface EP (PrivateLink Consumer)", 1000, 600, "udemy-162")

    d.group_account(60, 80, 420, 380, "自社 Account")
    d.group_vpc(90, 120, 360, 320, "分析 VPC")
    d.icon("ec2", 120, 180, label="分析 EC2")
    eni = d.icon("endpoint", 270, 180, label="Interface EP\n(Consumer 側)")
    d.arrow_xy(170, 205, 270, 205, color=Colors.BLUE)
    d.rect(110, 300, 320, 100,
           value=("Consumer 側設定:\n"
                  "1. SaaS から Endpoint Service 名を受領\n"
                  "2. VPC Endpoint 作成 (Interface 型)\n"
                  "3. Private DNS で SaaS ドメイン解決"),
           fill="#FFFFFF", stroke=Colors.BLUE, fontsize=11, align="left")

    d.group_account(540, 80, 420, 380, "SaaS Provider (別 AWS アカウント)")
    d.group_vpc(570, 120, 360, 320, "SaaS VPC")
    d.icon("nlb", 610, 180, label="NLB")
    d.icon("ec2", 760, 180, label="SaaS API\nBackend")
    d.arrow_xy(660, 205, 760, 205, color=Colors.BLUE)
    d.rect(590, 300, 320, 100,
           value=("Provider 側設定:\n"
                  "・Endpoint Service (NLB ベース)\n"
                  "・Consumer アカウント ID 承認\n"
                  "・Private DNS 名 (ドメイン検証)"),
           fill="#FFFFFF", stroke=Colors.BLUE, fontsize=11, align="left")

    d.arrow_xy(320, 205, 610, 205, color=Colors.BLUE, label="PrivateLink\n(片方向: Consumer → Provider)")

    d.note(60, 475, 900, 105,
           value=("◾ 要件: サードパーティ SaaS の API を プライベート に利用 (VPC Peering より疎結合)\n"
                  "◾ 解法: AWS PrivateLink 方式\n"
                  "  ・CIDR 衝突を気にせず利用可 (Peering と異なりルーティング不要)\n"
                  "  ・一方向 (Consumer → Provider) のみ通信 → 攻撃面が小さい\n"
                  "  ・Shared VPC や Transit Gateway と異なり、L7 API だけ公開できる"),
           stroke=Colors.BLUE)
    d.save(f"{OUT_DIR}/UDEMY-162.drawio")


# ---------------------------------------------------------------------------
# UDEMY-170 (num 469) — Low cost: S3 Glacier + Interface EP via Client VPN
# ---------------------------------------------------------------------------
def make_170():
    d = Diagram("UDEMY-170: 低コスト文書保管 — S3 Glacier Deep Archive + Interface EP", 1000, 600, "udemy-170")

    d.group_onprem(40, 80, 220, 360, "社内 (Remote)")
    d.rect(70, 180, 160, 80, value="従業員\n(Client VPN)", bold=True)

    d.group_vpc(300, 80, 660, 360, "VPC (社内接続用)")
    d.rect(330, 130, 150, 60,
           value="Client VPN\nEndpoint",
           fill="#FFF5EB", stroke=Colors.ORANGE, stroke_width=2, bold=True)
    d.arrow_xy(260, 220, 330, 160, color=Colors.BLUE, label="VPN")

    if_ep = d.icon("endpoint", 550, 140, label="Interface EP\nfor S3")
    d.arrow_xy(480, 160, 550, 160, color=Colors.BLUE)

    s3 = d.icon("s3", 750, 140, label="S3 バケット")
    d.arrow_xy(600, 165, 750, 165, color=Colors.GREEN, label="PrivateLink")

    # Storage class box
    d.note(500, 240, 420, 180,
           value=("🗄 ストレージクラス選択:\n"
                  "・アクセス頻度: 非常に低い\n"
                  "・取得まで 数時間〜数十時間 許容\n"
                  "→ 🎯 S3 Glacier Deep Archive (Bulk取得は12〜48h)\n\n"
                  "コスト比較 ($/GB-月):\n"
                  "  Standard:              $0.023\n"
                  "  Standard-IA:            $0.0125\n"
                  "  Glacier Instant:        $0.004\n"
                  "  Glacier Flexible:       $0.0036\n"
                  "  Deep Archive:           $0.00099 ← 最安"),
           stroke=Colors.GREEN)

    d.note(40, 460, 920, 120,
           value=("◾ 要件: ① インターネット非公開、② アクセス頻度 極低、③ 取得時間許容、④ 最低コスト\n"
                  "◾ 解法: (D) S3 Glacier Deep Archive + Interface EP for S3 + Client VPN\n"
                  "  ・Client VPN → VPC → Interface EP → S3 (全経路プライベート)\n"
                  "  ・ストレージクラスは Deep Archive が最安 (取得時間要件を満たすため選択可)"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-170.drawio")


# ---------------------------------------------------------------------------
# UDEMY-190 (num 489) — Interface EP for S3 (vs Gateway EP) from analytics
# ---------------------------------------------------------------------------
def make_190():
    d = Diagram("UDEMY-190: S3 アクセス — Gateway EP vs Interface EP (PrivateLink)", 1000, 600, "udemy-190")

    # Left: Gateway EP (in-VPC)
    d.text(60, 55, 400, 24, "同一 VPC 内 → Gateway EP", bold=True, fontsize=13, color=Colors.GREEN)
    d.group_vpc(60, 90, 420, 260, "VPC (Analytics)")
    ec2 = d.icon("ec2", 100, 140, label="EC2 Analytics")
    d.rect(220, 140, 160, 50,
           value="Route Table\n→ vpce-xxx",
           fill="#FFFFFF", stroke=Colors.GREEN, stroke_width=2, bold=True, fontsize=10)
    d.icon("endpoint", 400, 140, label="Gateway EP\n($0, 無料)")
    s3l = d.icon("s3", 220, 260, label="S3")

    # Right: Interface EP for external consumption
    d.text(540, 55, 400, 24, "外部 (他VPC/オンプレ) → Interface EP", bold=True, fontsize=13, color=Colors.BLUE)
    d.group_vpc(540, 90, 420, 260, "Other VPC or On-Prem")
    d.icon("ec2", 580, 140, label="クライアント")
    if_ep = d.icon("endpoint", 740, 140, label="Interface EP\nfor S3\n($0.01/h + $/GB)")
    s3r = d.icon("s3", 870, 260, label="S3")
    d.arrow_xy(630, 165, 740, 165, color=Colors.BLUE)
    d.arrow_xy(770, 195, 870, 260, color=Colors.BLUE, label="PrivateLink")

    d.note(60, 385, 900, 195,
           value=("◾ 判断軸:\n"
                  "  ・同一 VPC から S3 ⇒ Gateway EP (無料、Route Table にルート追加)\n"
                  "  ・オンプレ / 別 VPC / 別リージョン から S3 ⇒ Interface EP for S3 (有料、PrivateLink)\n\n"
                  "◾ セキュリティ強化:\n"
                  "  ・バケットポリシーに aws:sourceVpce 条件 (特定 VPCE からのみ許可)\n"
                  "  ・IAM Role に最小権限の s3: アクション\n\n"
                  "◾ ハイブリッド時は Interface EP を Hub VPC に集約し、Inbound Resolver で名前解決を統一"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-190.drawio")


# ---------------------------------------------------------------------------
# UDEMY-198 (num 497) — Regional API + RDS Proxy + EP
# ---------------------------------------------------------------------------
def make_198():
    d = Diagram("UDEMY-198: Regional API Gateway + Lambda — VPC/EP 設計", 1000, 600, "udemy-198")

    # Internet
    d.rect(40, 100, 100, 40, value="Customer",
           fill=Colors.LIGHT_GRAY_BG, stroke=Colors.GRAY, bold=True)
    api = d.rect(180, 100, 200, 60,
                 value="API Gateway\n(Regional)",
                 fill="#FFF5EB", stroke=Colors.ORANGE, stroke_width=2, bold=True)
    d.arrow_xy(140, 120, 180, 120, color=Colors.GRAY)

    d.group_vpc(40, 200, 920, 280, "VPC")
    lam = d.rect(120, 250, 180, 70,
                 value="Lambda\n(VPC Attached)",
                 fill="#FFF5EB", stroke=Colors.ORANGE, stroke_width=2, bold=True)
    d.arrow_xy(280, 160, 210, 250, color=Colors.ORANGE, label="Invoke")

    proxy = d.rect(360, 250, 180, 70,
                   value="RDS Proxy",
                   fill="#FFFFFF", stroke=Colors.BLUE, stroke_width=2, bold=True)
    d.arrow(lam, proxy, color=Colors.BLUE, label="DB Conn")

    aur = d.rect(600, 250, 200, 70,
                 value="Aurora MySQL\n(Multi-AZ)",
                 fill=Colors.LIGHT_BLUE_BG, stroke=Colors.BLUE, stroke_width=2, bold=True)
    d.arrow(proxy, aur, color=Colors.BLUE)

    secrets = d.rect(360, 370, 180, 60,
                     value="Secrets Manager\n(DB Credentials)",
                     fill="#FFFFFF", stroke=Colors.BLUE, stroke_width=2, bold=True)
    if_ep = d.icon("endpoint", 620, 370, label="Interface EP\n(Secrets)")
    d.arrow_xy(300, 320, 450, 370, color=Colors.BLUE, label="取得")
    d.arrow_xy(540, 400, 620, 400, color=Colors.BLUE)

    d.note(40, 500, 920, 80,
           value=("◾ 解法: Lambda を VPC にアタッチ + RDS Proxy で接続プール + Secrets Manager を Interface EP で取得\n"
                  "  ・Lambda のコールドスタート時の DB 新規接続乱立 → RDS Proxy で吸収\n"
                  "  ・資格情報は Secrets Manager → VPC 内 Lambda から Interface EP で private 取得"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-198.drawio")


# ---------------------------------------------------------------------------
# UDEMY-203 (num 502) — Route 53 Resolver for VPN connected office IPs
# ---------------------------------------------------------------------------
def make_203():
    d = Diagram("UDEMY-203: Route 53 Resolver で TGW/VPN 越しの名前解決", 1000, 600, "udemy-203")

    d.group_onprem(40, 80, 220, 360, "Office")
    d.rect(70, 160, 160, 70, value="クライアント")
    d.rect(70, 260, 160, 70, value="On-Prem DNS\n(corp.internal)", bold=True)

    vpn = d.rect(280, 200, 120, 60,
                 value="Site-to-Site\nVPN",
                 fill=Colors.LIGHT_YELLOW_BG, stroke=Colors.YELLOW, bold=True)
    d.arrow_xy(230, 220, 280, 220, color=Colors.YELLOW)

    tgw = d.icon("transit_gateway", 440, 205, label="Transit Gateway")
    d.arrow_xy(400, 235, 445, 235, color=Colors.PURPLE)

    d.group_vpc(560, 80, 400, 360, "Central VPC")
    in_ep = d.rect(600, 130, 160, 70,
                   value="Inbound\nResolver EP",
                   fill="#FFFFFF", stroke=Colors.PURPLE, stroke_width=2, bold=True, fontsize=11)
    out_ep = d.rect(790, 130, 160, 70,
                    value="Outbound\nResolver EP",
                    fill="#FFFFFF", stroke=Colors.PURPLE, stroke_width=2, bold=True, fontsize=11)
    d.icon("route_53", 720, 250, label="PHZ\napp.internal")
    d.arrow_xy(495, 235, 600, 165, color=Colors.PURPLE, label="オンプレ→AWS 解決")
    d.arrow_xy(870, 200, 870, 260, color=Colors.PURPLE)
    d.arrow_xy(870, 290, 495, 240, color=Colors.PURPLE, label="AWS→オンプレ 解決", dashed=True)

    d.note(40, 470, 920, 110,
           value=("◾ 要件: オフィス(TGW/VPN経由)から AWS 側の Private Hosted Zone を解決、逆向きも必要\n"
                  "◾ 解法:\n"
                  "  1. Inbound Resolver EP  → オンプレの DNS から AWS の PHZ へ問合せ (ENI の IP を On-Prem DNS に forwarder 設定)\n"
                  "  2. Outbound Resolver EP + Resolver Rule (FORWARD) → AWS から corp.internal をオンプレに転送\n"
                  "  3. TGW でオンプレ←→Central VPC 間のネットワーク確立"),
           stroke=Colors.PURPLE)
    d.save(f"{OUT_DIR}/UDEMY-203.drawio")


# ---------------------------------------------------------------------------
# UDEMY-206 (num 505) — NLB + PrivateLink consumer (固定 Egress IP for 3rd party API)
# ---------------------------------------------------------------------------
def make_206():
    d = Diagram("UDEMY-206: サードパーティ API 許可リスト — NAT GW (Elastic IP) で送信元 IP 固定", 1000, 600, "udemy-206")

    d.group_vpc(60, 80, 500, 380, "VPC")
    d.text(90, 110, 200, 20, "Private Subnet (複数AZ)", bold=True, align="left")
    ec2a = d.icon("ec2", 100, 140, label="EC2 (ALBターゲット)")
    ec2b = d.icon("ec2", 240, 140, label="EC2 (ALBターゲット)")
    alb = d.rect(390, 140, 140, 50, value="ALB",
                 fill="#FFFFFF", stroke=Colors.PURPLE, stroke_width=2, bold=True)

    d.text(90, 240, 200, 20, "Public Subnet", bold=True, align="left")
    nat = d.icon("nat_gateway", 200, 270, label="NAT GW\n+ Elastic IP")
    igw = d.rect(380, 270, 140, 50, value="IGW",
                 fill="#FFF5EB", stroke=Colors.ORANGE, stroke_width=2, bold=True)
    d.arrow(ec2a, nat, color=Colors.GREEN, label="API Call")
    d.arrow(nat, igw, color=Colors.GREEN)

    # 3rd party
    d.rect(600, 180, 180, 60,
           value="3rd Party API\nFirewall",
           fill=Colors.LIGHT_GRAY_BG, stroke=Colors.GRAY, stroke_width=2, bold=True)
    d.rect(820, 180, 120, 60,
           value="API Backend",
           fill=Colors.LIGHT_GRAY_BG, stroke=Colors.GRAY, bold=True)
    d.arrow_xy(520, 295, 690, 240, color=Colors.GREEN, label="Elastic IP\n(許可リスト登録)")
    d.arrow_xy(780, 210, 820, 210, color=Colors.GRAY)

    d.note(60, 480, 900, 95,
           value=("◾ 要件: 3rd Party API は 1 つのパブリック CIDR 許可リストのみ受理 → 送信元 IP を固定する必要\n"
                  "◾ 解法: (B) NAT GW に Elastic IP を割当 → Private Subnet からの Egress は常にその EIP\n"
                  "  ・3rd Party 側は EIP CIDR を許可リストに登録\n"
                  "◾ 誤答: VPC Endpoint ≠ 送信元 IP 固定 (AWS サービス向けのみ) / ALB は受信側"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-206.drawio")


# ---------------------------------------------------------------------------
# UDEMY-247 (num 546) — Route 53 Resolver Rule shared via RAM
# ---------------------------------------------------------------------------
def make_247():
    d = Diagram("UDEMY-247: Route 53 Resolver Rule を RAM で組織全体に共有", 1000, 600, "udemy-247")

    # Network Account
    d.group_account(40, 60, 420, 440, "Network Account (Hub)")
    d.group_vpc(70, 100, 360, 380, "Central VPC")
    out_ep = d.rect(100, 140, 220, 70,
                    value="Outbound Resolver EP",
                    fill="#FFFFFF", stroke=Colors.PURPLE, stroke_width=2, bold=True)
    rule = d.rect(100, 240, 300, 80,
                  value=("Resolver Rule:\n"
                         "  domain = corp.internal\n"
                         "  target = 10.1.0.10 (On-Prem DNS)\n"
                         "  type   = FORWARD"),
                  fill=Colors.LIGHT_BLUE_BG, stroke=Colors.BLUE, stroke_width=2, align="left", fontsize=10)
    ram = d.rect(100, 350, 300, 70,
                 value="RAM Share → Org ARN\n(全メンバーアカウントに共有)",
                 fill="#FFFFFF", stroke=Colors.YELLOW, stroke_width=2, bold=True)
    d.arrow(rule, ram, color=Colors.YELLOW)

    # Spoke accounts
    d.group_account(500, 60, 460, 205, "Member Account A")
    d.group_vpc(530, 100, 400, 150, "VPC (Associate した Rule で解決)")
    d.icon("ec2", 620, 150, label="EC2")

    d.group_account(500, 280, 460, 220, "Member Account B")
    d.group_vpc(530, 320, 400, 165, "VPC")
    d.icon("ec2", 620, 360, label="EC2")

    d.arrow_xy(400, 385, 530, 175, color=Colors.BLUE, label="RAM共有→Associate")
    d.arrow_xy(400, 385, 530, 385, color=Colors.BLUE)

    d.note(40, 510, 920, 70,
           value=("◾ 解法: (C) 中央アカウントで Resolver Rule を作成 → RAM で Organizations に共有 → 各 VPC に Associate\n"
                  "  ・個別アカウントでルール重複を避けられる (セキュリティ標準を一元管理)\n"
                  "  ・Outbound Endpoint は Hub VPC に1つ置けば良い (アカウント分離は維持)"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-247.drawio")


# ---------------------------------------------------------------------------
# UDEMY-248 (num 547) — Client VPN + PrivateLink for internal app
# ---------------------------------------------------------------------------
def make_248():
    d = Diagram("UDEMY-248: リモートワーク — AWS Client VPN + 社内アプリ (VPC A)", 1000, 600, "udemy-248")

    # remote workers
    d.rect(40, 140, 180, 70,
           value="在宅ワーカー\n(自宅PC)",
           fill=Colors.LIGHT_GRAY_BG, stroke=Colors.GRAY, bold=True)
    d.rect(40, 260, 180, 70,
           value="Client VPN\nソフトウェア",
           fill=Colors.LIGHT_GRAY_BG, stroke=Colors.GRAY, bold=True)

    # VPC C - Client VPN Endpoint
    d.group_vpc(260, 80, 340, 400, "VPC (Client VPN)")
    cvpn = d.rect(290, 150, 260, 70,
                  value="Client VPN Endpoint\n(複数 Subnet 関連付け)",
                  fill="#FFF5EB", stroke=Colors.ORANGE, stroke_width=2, bold=True)
    d.arrow_xy(220, 190, 290, 190, color=Colors.ORANGE, label="TLS")

    tgw = d.icon("transit_gateway", 395, 290, label="TGW\n(VPC A も attach)")

    d.group_vpc(640, 80, 300, 400, "VPC A (社内アプリ)")
    d.icon("ec2", 730, 200, label="内部アプリ EC2")
    d.icon("ec2", 730, 350, label="内部アプリ EC2")
    d.arrow_xy(445, 315, 730, 230, color=Colors.PURPLE, label="TGW 経由")

    d.note(40, 500, 920, 80,
           value=("◾ 要件: オフィス外 (自宅) から VPC A の社内アプリにアクセス\n"
                  "◾ 解法: (B) AWS Client VPN Endpoint を VPC にデプロイ + TGW で VPC A に到達\n"
                  "  ・Site-to-Site VPN は拠点間接続用 (個人 PC には不向き)\n"
                  "  ・Direct Connect は物理接続で個人利用には非現実的"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-248.drawio")


# ---------------------------------------------------------------------------
# UDEMY-276 (num 575) — ECS Fargate + Interface EP for ECR/Secrets/Logs
# ---------------------------------------------------------------------------
def make_276():
    d = Diagram("UDEMY-276: ECS Fargate 用 Interface EP (ECR/Secrets/Logs/S3)", 1000, 600, "udemy-276")

    d.group_vpc(40, 80, 920, 400, "VPC (Delivery 最適化)")
    d.text(80, 110, 200, 20, "Private Subnet", bold=True, align="left")
    task1 = d.rect(80, 140, 150, 60,
                   value="ECS Task\n(Fargate)",
                   fill="#FFF5EB", stroke=Colors.ORANGE, stroke_width=2, bold=True)
    task2 = d.rect(80, 220, 150, 60,
                   value="ECS Task\n(Fargate)",
                   fill="#FFF5EB", stroke=Colors.ORANGE, stroke_width=2, bold=True)

    # Endpoints list
    ep_x = 320
    labels = [
        ("ECR API", "com.amazonaws.region.ecr.api"),
        ("ECR DKR", "com.amazonaws.region.ecr.dkr"),
        ("CloudWatch Logs", "com.amazonaws.region.logs"),
        ("Secrets Manager", "com.amazonaws.region.secretsmanager"),
    ]
    for i, (name, fqdn) in enumerate(labels):
        y = 130 + i * 70
        d.icon("endpoint", ep_x, y, label=name)
        d.rect(ep_x + 80, y + 10, 340, 36,
               value=fqdn, fill="#FFFFFF", stroke=Colors.BLUE, fontsize=9)

    # S3 Gateway EP
    d.icon("endpoint", 760, 140, label="Gateway EP\nS3 (無料)")

    d.arrow_xy(230, 170, ep_x - 10, 170, color=Colors.BLUE)
    d.arrow_xy(230, 250, ep_x - 10, 380, color=Colors.BLUE)

    d.note(40, 500, 920, 80,
           value=("◾ 解法: Fargate を Private Subnet に配置 + 必要な Interface EP を作成 (ECR API/DKR, Logs, Secrets) + S3 は Gateway EP\n"
                  "  ・Fargate の Awsvpc モードでタスク毎に ENI 割当 → Interface EP を介して AWS API を呼ぶ\n"
                  "  ・NAT GW なしでデプロイ可能 (コスト削減 & プライベート要件)"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-276.drawio")


# ---------------------------------------------------------------------------
# UDEMY-295 (num 594) — ECS Fargate Aurora via Interface EP for Secrets
# ---------------------------------------------------------------------------
def make_295():
    d = Diagram("UDEMY-295: ECS Fargate → Aurora — 認証情報を Secrets Manager + EP", 1000, 600, "udemy-295")

    d.group_vpc(60, 80, 880, 380, "VPC")
    d.text(90, 110, 200, 20, "Private Subnet (App)", bold=True, align="left")
    task = d.rect(80, 150, 150, 70,
                  value="Fargate Task\n(ECS)",
                  fill="#FFF5EB", stroke=Colors.ORANGE, stroke_width=2, bold=True)

    ep_secrets = d.icon("endpoint", 290, 150, label="Interface EP\nSecretsManager")
    ep_kms = d.icon("endpoint", 290, 270, label="Interface EP\nKMS")
    d.arrow_xy(230, 180, 290, 180, color=Colors.BLUE, label="GetSecret")
    d.arrow_xy(230, 220, 290, 290, color=Colors.BLUE)

    secrets = d.rect(440, 130, 220, 70,
                     value="AWS Secrets Manager\n(DB 資格情報)",
                     fill="#FFFFFF", stroke=Colors.BLUE, stroke_width=2, bold=True)
    kms = d.rect(440, 250, 220, 70,
                 value="AWS KMS (暗号鍵)",
                 fill="#FFFFFF", stroke=Colors.BLUE, stroke_width=2, bold=True)
    d.arrow_xy(380, 175, 440, 165, color=Colors.BLUE)
    d.arrow_xy(380, 290, 440, 285, color=Colors.BLUE)
    d.arrow(secrets, kms, color=Colors.BLUE, label="Decrypt")

    aur = d.rect(720, 180, 200, 80,
                 value="Aurora MySQL\n(自動ローテーション)",
                 fill=Colors.LIGHT_BLUE_BG, stroke=Colors.BLUE, stroke_width=2, bold=True)
    d.arrow_xy(150, 220, 720, 220, color=Colors.BLUE, label="DB接続\n(認証: Secrets Manager)")

    d.note(60, 480, 880, 100,
           value=("◾ 要件: Fargate から Aurora への接続情報を安全に管理 (コンプラ: パブリック経路なし)\n"
                  "◾ 解法: Secrets Manager + 自動ローテーション + Secrets/KMS 用 Interface EP\n"
                  "  ・Task Execution Role に secretsmanager:GetSecretValue と kms:Decrypt を付与\n"
                  "  ・VPC から Secrets Manager / KMS を PrivateLink で呼ぶ → NAT GW 不要"),
           stroke=Colors.NAV)
    d.save(f"{OUT_DIR}/UDEMY-295.drawio")


# ---------------------------------------------------------------------------
# UDEMY-343 (num 642) — Multi-region S3 with Gateway EP
# ---------------------------------------------------------------------------
def make_343():
    d = Diagram("UDEMY-343: マルチリージョン S3 — Cross-Region Replication + 地域別 Gateway EP", 1000, 600, "udemy-343")

    # us-east-1 (master)
    d.group_vpc(40, 80, 280, 380, "VPC us-east-1 (Origin)")
    d.icon("ec2", 90, 140, label="EC2")
    d.icon("endpoint", 210, 140, label="Gateway EP")
    d.icon("s3", 150, 280, label="S3 (Origin)\n北米")

    # eu
    d.group_vpc(360, 80, 280, 380, "VPC eu-west-1")
    d.icon("ec2", 410, 140, label="EC2")
    d.icon("endpoint", 530, 140, label="Gateway EP")
    d.icon("s3", 470, 280, label="S3 (EU Replica)")

    # ap
    d.group_vpc(680, 80, 280, 380, "VPC ap-northeast-1")
    d.icon("ec2", 730, 140, label="EC2")
    d.icon("endpoint", 850, 140, label="Gateway EP")
    d.icon("s3", 790, 280, label="S3 (JP Replica)")

    # CRR arrows
    d.arrow_xy(320, 310, 360, 310, color=Colors.GREEN, label="CRR")
    d.arrow_xy(640, 310, 680, 310, color=Colors.GREEN, label="CRR")

    d.note(40, 480, 920, 100,
           value=("◾ 解法: (B) 各リージョンに S3 バケットを作成 + Cross-Region Replication (CRR) でデータを複製\n"
                  "  ・各リージョンの VPC では Gateway EP を介して自リージョンの S3 へアクセス (低遅延 & 無料)\n"
                  "  ・Gateway EP は同一リージョン内の S3/DDB にしか使えない → リージョン毎に必要\n"
                  "◾ 誤答: CloudFront 単体では書込みができない / Transfer Acceleration は移行用途"),
           stroke=Colors.GREEN)
    d.save(f"{OUT_DIR}/UDEMY-343.drawio")


# ---------------------------------------------------------------------------
# UDEMY-348 (num 647) — Resolver Query Logs (monitoring)
# ---------------------------------------------------------------------------
def make_348():
    d = Diagram("UDEMY-348: Route 53 Resolver Query Logs — マルチアカウント DNS 監査", 1000, 600, "udemy-348")

    # Org 管理アカウント
    d.group_account(40, 70, 920, 170, "AWS Organizations")
    d.group_account(60, 120, 280, 100, "Member Acct A")
    d.icon("ec2", 170, 150, label="EC2 (DNS)")
    d.group_account(360, 120, 280, 100, "Member Acct B")
    d.icon("ec2", 470, 150, label="EC2 (DNS)")
    d.group_account(660, 120, 280, 100, "Member Acct C")
    d.icon("ec2", 770, 150, label="EC2 (DNS)")

    # Resolver Query Log config
    qlog = d.rect(260, 280, 480, 70,
                  value="Route 53 Resolver Query Logging Configuration\n(RAM で Org に共有 / 複数 VPC を Associate)",
                  fill="#FFFFFF", stroke=Colors.PURPLE, stroke_width=2, bold=True)
    d.arrow_xy(170, 220, 280, 290, color=Colors.PURPLE)
    d.arrow_xy(470, 220, 500, 290, color=Colors.PURPLE)
    d.arrow_xy(770, 220, 720, 290, color=Colors.PURPLE)

    # Destinations
    cwlogs = d.rect(100, 400, 220, 80,
                    value="CloudWatch Logs",
                    fill=Colors.LIGHT_BLUE_BG, stroke=Colors.BLUE, bold=True)
    s3 = d.icon("s3", 480, 410, label="S3\n(長期アーカイブ)")
    firehose = d.rect(660, 400, 240, 80,
                      value="Kinesis Data Firehose\n→ OpenSearch/外部SIEM",
                      fill=Colors.LIGHT_BLUE_BG, stroke=Colors.BLUE, bold=True)
    d.arrow_xy(400, 350, 200, 400, color=Colors.BLUE)
    d.arrow_xy(500, 350, 500, 410, color=Colors.BLUE)
    d.arrow_xy(600, 350, 780, 400, color=Colors.BLUE)

    d.note(40, 495, 920, 85,
           value=("◾ 解法: (A) Resolver Query Logging Configuration を作成、(C) RAM で組織全体に共有、(D) 各 VPC を Associate\n"
                  "  ・DNS クエリ名・レスポンス・リゾルバ EP 等を記録 → セキュリティ監査に必須\n"
                  "  ・出力先: CloudWatch Logs / S3 / Firehose が選択可能"),
           stroke=Colors.PURPLE)
    d.save(f"{OUT_DIR}/UDEMY-348.drawio")


# ---------------------------------------------------------------------------
# Main dispatch
# ---------------------------------------------------------------------------
GENERATORS = [
    ("UDEMY-017", make_017),
    ("UDEMY-021", make_021),
    ("UDEMY-023", make_023),
    ("UDEMY-029", make_029),
    ("UDEMY-043", make_043),
    ("UDEMY-052", make_052),
    ("UDEMY-057", make_057),
    ("UDEMY-066", make_066),
    ("UDEMY-078", make_078),
    ("UDEMY-087", make_087),
    ("UDEMY-096", make_096),
    ("UDEMY-106", make_106),
    ("UDEMY-114", make_114),
    ("UDEMY-135", make_135),
    ("UDEMY-140", make_140),
    ("UDEMY-151", make_151),
    ("UDEMY-161", make_161),
    ("UDEMY-162", make_162),
    ("UDEMY-170", make_170),
    ("UDEMY-190", make_190),
    ("UDEMY-198", make_198),
    ("UDEMY-203", make_203),
    ("UDEMY-206", make_206),
    ("UDEMY-247", make_247),
    ("UDEMY-248", make_248),
    ("UDEMY-276", make_276),
    ("UDEMY-295", make_295),
    ("UDEMY-343", make_343),
    ("UDEMY-348", make_348),
]


def main():
    for name, fn in GENERATORS:
        out = f"{OUT_DIR}/{name}.drawio"
        if os.path.exists(out):
            print(f"  SKIP (exists) {out}")
            continue
        fn()
        print(f"  OK  {out}")


if __name__ == "__main__":
    main()
