#!/usr/bin/env python3
"""
Build drawio files for 25 selected network/hybrid connectivity questions.
Canvas: 1000x600, white background, AWS official icons.
Label y offset: icon.y + 58 minimum (to avoid overlap).
"""
import os

OUT = "/Users/aki/aws-sap/docs/diagrams/per-question"
os.makedirs(OUT, exist_ok=True)

# ---------- mxgraph helpers ----------
def aws_icon(cid, x, y, resIcon, w=60, h=60, fill="#FFFFFF"):
    """AWS official resourceIcon shape."""
    return f'''<mxCell id="{cid}" value="" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={fill};strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{resIcon};" vertex="1" parent="1">
      <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def aws_icon_color(cid, x, y, resIcon, color, w=60, h=60):
    return f'''<mxCell id="{cid}" value="" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={color};strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{resIcon};" vertex="1" parent="1">
      <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def label(cid, x, y, text, w=160, h=18, bold=True, size=11, color="#232F3E"):
    weight = 1 if bold else 0
    return f'''<mxCell id="{cid}" value="{text}" style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize={size};fontStyle={weight};fontColor={color};" vertex="1" parent="1">
      <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def title(cid, x, y, text, w=1000, h=28, size=16):
    return f'''<mxCell id="{cid}" value="{text}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize={size};fontStyle=1;fontColor=#232F3E;" vertex="1" parent="1">
      <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def box(cid, x, y, w, h, title_text, fill="#EBF1FF", stroke="#3B48CC"):
    """Colored rounded rectangle container (label at top)."""
    return f'''<mxCell id="{cid}" value="{title_text}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=2;fontSize=12;fontStyle=1;fontColor=#232F3E;verticalAlign=top;spacingTop=6;" vertex="1" parent="1">
      <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def vpc_group(cid, x, y, w, h, name):
    return f'''<mxCell id="{cid}" value="{name}" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;strokeColor=#248814;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0;" vertex="1" parent="1">
      <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def region_group(cid, x, y, w, h, name):
    return f'''<mxCell id="{cid}" value="{name}" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;strokeColor=#147EBA;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=1;" vertex="1" parent="1">
      <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def dc_group(cid, x, y, w, h, name):
    return f'''<mxCell id="{cid}" value="{name}" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_corporate_data_center;strokeColor=#7D7D7D;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0;" vertex="1" parent="1">
      <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def edge(cid, src, tgt, color="#666666", dashed=False, w=2, label_text=""):
    d = "dashed=1;" if dashed else ""
    val = f' value="{label_text}"' if label_text else ""
    return f'''<mxCell id="{cid}"{val} style="endArrow=classic;startArrow=classic;html=1;strokeColor={color};strokeWidth={w};{d}fontSize=10;fontColor=#232F3E;" edge="1" parent="1" source="{src}" target="{tgt}">
      <mxGeometry relative="1" as="geometry" /></mxCell>'''

def arrow(cid, src, tgt, color="#666666", dashed=False, w=2, label_text=""):
    """One-way arrow."""
    d = "dashed=1;" if dashed else ""
    val = f' value="{label_text}"' if label_text else ""
    return f'''<mxCell id="{cid}"{val} style="endArrow=classic;startArrow=none;html=1;strokeColor={color};strokeWidth={w};{d}fontSize=10;fontColor=#232F3E;" edge="1" parent="1" source="{src}" target="{tgt}">
      <mxGeometry relative="1" as="geometry" /></mxCell>'''

def note(cid, x, y, w, h, text, fill="#FFFBE6", stroke="#D4AC0D"):
    return f'''<mxCell id="{cid}" value="{text}" style="text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;fontSize=10;fontStyle=0;fontColor=#232F3E;fillColor={fill};strokeColor={stroke};strokeWidth=1;spacing=6;rounded=1;" vertex="1" parent="1">
      <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def wrap(diagram_id, diagram_name, body_cells, width=1000, height=600):
    body = "\n        ".join(body_cells)
    return f'''<mxfile host="app.diagrams.net" modified="2026-04-20T00:00:00.000Z" agent="Claude" version="24.0.0">
  <diagram id="{diagram_id}" name="{diagram_name}">
    <mxGraphModel dx="1422" dy="757" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{width}" pageHeight="{height}" math="0" shadow="0" background="#FFFFFF">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        {body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

# =========================================================
# DIAGRAM BUILDERS (one per question id)
# =========================================================

# Color palette
CLR_TGW = "#8C4FFF"          # Networking purple
CLR_DX  = "#E7157B"          # Pink
CLR_VPN = "#7AA116"          # Green
CLR_NAT = "#FF9900"          # Orange
CLR_NFW = "#DD344C"          # Red
CLR_EP  = "#3B48CC"          # Blue
CLR_EC2 = "#FF9900"

def diag_305():
    """DX + Transit VIF + DX GW + Multi-region TGW (retail global)"""
    cells = [
        title("t", 0, 10, "UDEMY-006 / num=305: DX + Transit VIF + DX Gateway + マルチリージョン TGW"),
        # On-prem (store HQ)
        dc_group("dc", 20, 70, 220, 180, "本社 / 主要店舗ネットワーク"),
        aws_icon("dc_srv", 80, 100, "corporate_data_center_2", 50, 50),
        label("dc_srv_l", 50, 160, "オンプレ DC", 110),
        label("dc_srv_l2", 50, 178, "店舗ネットワーク", 110, bold=False),
        # DX + Transit VIF
        aws_icon_color("dx", 290, 130, "direct_connect", CLR_DX, 60, 60),
        label("dx_l", 260, 198, "Direct Connect", 120),
        label("dx_l2", 260, 216, "(1Gbps / 10Gbps)", 120, bold=False),
        # DX Gateway
        aws_icon_color("dxgw", 420, 130, "direct_connect", CLR_DX, 60, 60),
        label("dxgw_l", 390, 198, "Direct Connect GW", 120),
        label("dxgw_l2", 390, 216, "(Transit VIF)", 120, bold=False),
        # Region 1 - us-east
        region_group("r1", 560, 70, 200, 210, "Region: us-east-1"),
        aws_icon_color("tgw1", 620, 120, "transit_gateway", CLR_TGW, 60, 60),
        label("tgw1_l", 590, 188, "Transit Gateway", 120),
        vpc_group("r1v1", 580, 220, 70, 50, "VPC"),
        vpc_group("r1v2", 680, 220, 70, 50, "VPC"),
        # Region 2 - eu-west
        region_group("r2", 780, 70, 200, 210, "Region: eu-west-1"),
        aws_icon_color("tgw2", 840, 120, "transit_gateway", CLR_TGW, 60, 60),
        label("tgw2_l", 810, 188, "Transit Gateway", 120),
        vpc_group("r2v1", 800, 220, 70, 50, "VPC"),
        vpc_group("r2v2", 900, 220, 70, 50, "VPC"),
        # Links
        arrow("e1", "dc_srv", "dx", CLR_DX, w=3),
        arrow("e2", "dx", "dxgw", CLR_DX, w=3, label_text="Transit VIF"),
        arrow("e3", "dxgw", "tgw1", CLR_TGW, w=3),
        arrow("e4", "dxgw", "tgw2", CLR_TGW, w=3),
        arrow("e5", "tgw1", "r1v1", CLR_TGW),
        arrow("e6", "tgw1", "r1v2", CLR_TGW),
        arrow("e7", "tgw2", "r2v1", CLR_TGW),
        arrow("e8", "tgw2", "r2v2", CLR_TGW),
        # TGW peering
        edge("e9", "tgw1", "tgw2", CLR_TGW, dashed=True, w=2, label_text="Inter-Region Peering"),
        # Notes
        note("n1", 20, 310, 960, 50,
             "ポイント: 1 本の DX + Transit VIF から DX Gateway 経由で 最大 3 リージョンまでの TGW に接続できる。推移ルーティングで全 VPC が相互通信可能。"),
        note("n2", 20, 370, 470, 110,
             "◎ 正解 B: Direct Connect + Transit VIF + DX Gateway → 各リージョン TGW 接続。推移ルーティング ○、コスト最適、安定帯域。",
             fill="#EBF5E8", stroke="#7AA116"),
        note("n3", 510, 370, 470, 110,
             "✕ 誤答: ・サイト間 VPN のみ (帯域不安定 / DX が要件)\n・各リージョンに個別 VPN (管理負荷 / 推移なし)\n・Inter-Region VPC Peering (N×N 爆発 / オンプレ接続別建て)",
             fill="#FDEBE9", stroke="#DD344C"),
        note("n4", 20, 492, 960, 90,
             "Transit VIF vs Private VIF vs Public VIF:\n ・Private VIF = 単一 VPC の VGW に直結 (シンプル・小規模)\n ・Transit VIF = DX GW + TGW アタッチ (複数 VPC / 複数リージョン)\n ・Public VIF = AWS パブリック IP 空間 (S3/DynamoDB 等への直接アクセス)"),
    ]
    return wrap("d305", "DX + Transit VIF + DX GW + Multi-Region TGW", cells)


def diag_320():
    """Central Egress VPC + TGW + NAT GW for hub-and-spoke"""
    cells = [
        title("t", 0, 10, "UDEMY-021 / num=320: ハブ&スポーク — 中央 Egress VPC + TGW + NAT GW"),
        # Spoke VPCs
        vpc_group("s1", 30, 80, 180, 110, "Spoke VPC 1 (アカウント A)"),
        aws_icon("s1_ec2", 80, 110, "ec2", 40, 40),
        label("s1_l", 50, 160, "EC2 (private)", 100, bold=False),
        vpc_group("s2", 30, 220, 180, 110, "Spoke VPC 2 (アカウント B)"),
        aws_icon("s2_ec2", 80, 250, "ec2", 40, 40),
        label("s2_l", 50, 300, "EC2 (private)", 100, bold=False),
        vpc_group("s3", 30, 360, 180, 110, "Spoke VPC 3 (アカウント C)"),
        aws_icon("s3_ec2", 80, 390, "ec2", 40, 40),
        label("s3_l", 50, 440, "EC2 (private)", 100, bold=False),
        # TGW center
        aws_icon_color("tgw", 340, 250, "transit_gateway", CLR_TGW, 70, 70),
        label("tgw_l", 300, 324, "Transit Gateway", 150),
        label("tgw_l2", 300, 342, "(RAM で全アカウント共有)", 150, bold=False, size=10),
        # Egress VPC
        vpc_group("egvpc", 500, 130, 260, 330, "Egress VPC (中央)"),
        aws_icon_color("natgw", 560, 200, "nat_gateway", CLR_NAT, 60, 60),
        label("natgw_l", 530, 268, "NAT Gateway", 120),
        aws_icon("igw", 660, 200, "internet_gateway", 60, 60),
        label("igw_l", 630, 268, "Internet Gateway", 120),
        aws_icon_color("nfw", 610, 340, "network_firewall", CLR_NFW, 60, 60),
        label("nfw_l", 580, 408, "Network Firewall", 120),
        label("nfw_l2", 580, 426, "(任意追加)", 120, bold=False, size=10),
        # Internet
        aws_icon("inet", 820, 230, "internet_gateway", 50, 50),
        label("inet_l", 790, 288, "インターネット", 110),
        label("inet_l2", 790, 306, "外部サプライヤー", 110, bold=False),
        # Edges
        arrow("e1", "s1", "tgw", CLR_TGW, w=2),
        arrow("e2", "s2", "tgw", CLR_TGW, w=2),
        arrow("e3", "s3", "tgw", CLR_TGW, w=2),
        arrow("e4", "tgw", "natgw", CLR_NAT, w=3, label_text="0.0.0.0/0"),
        arrow("e5", "natgw", "igw", CLR_NAT, w=2),
        arrow("e6", "igw", "inet", "#666", w=2),
        # Notes
        note("n1", 20, 490, 960, 50,
             "◎ 正解 B: TGW を RAM 共有 → 全 Spoke VPC をアタッチ。Egress VPC の NAT GW に 0.0.0.0/0 を集約 → NAT GW 数百個 → 数個に削減しコスト最適。",
             fill="#EBF5E8", stroke="#7AA116"),
        note("n2", 20, 548, 960, 50,
             "✕ VPC Peering で Egress 集約 = 推移不可で NG ／ PrivateLink は Egress 用途ではない ／ アカウントごとに TGW は過剰 (1 TGW + RAM 共有が正解)"),
    ]
    return wrap("d320", "Central Egress VPC Hub-and-Spoke", cells)


def diag_337():
    """NAT GW HA across 3 AZs"""
    cells = [
        title("t", 0, 10, "UDEMY-038 / num=337: NAT Gateway の高可用性 — AZ ごとに 1 台配置"),
        vpc_group("vpc", 30, 60, 940, 450, "VPC (3 AZ)"),
        # AZ-a
        box("az1", 60, 110, 290, 380, "AZ-a", fill="#FFF5EB", stroke="#FF9900"),
        aws_icon_color("ngw1", 130, 150, "nat_gateway", CLR_NAT),
        label("ngw1_l", 100, 218, "NAT GW (a)", 120),
        vpc_group("pub1", 70, 260, 270, 60, "Public Subnet a"),
        vpc_group("prv1", 70, 340, 270, 130, "Private Subnet a"),
        aws_icon("ec1", 170, 370, "ec2", 40, 40),
        label("ec1_l", 140, 418, "EC2 a", 100, bold=False),
        # AZ-b
        box("az2", 370, 110, 290, 380, "AZ-b", fill="#FFF5EB", stroke="#FF9900"),
        aws_icon_color("ngw2", 440, 150, "nat_gateway", CLR_NAT),
        label("ngw2_l", 410, 218, "NAT GW (b)", 120),
        vpc_group("pub2", 380, 260, 270, 60, "Public Subnet b"),
        vpc_group("prv2", 380, 340, 270, 130, "Private Subnet b"),
        aws_icon("ec2b", 480, 370, "ec2", 40, 40),
        label("ec2b_l", 450, 418, "EC2 b", 100, bold=False),
        # AZ-c
        box("az3", 680, 110, 290, 380, "AZ-c", fill="#FFF5EB", stroke="#FF9900"),
        aws_icon_color("ngw3", 750, 150, "nat_gateway", CLR_NAT),
        label("ngw3_l", 720, 218, "NAT GW (c)", 120),
        vpc_group("pub3", 690, 260, 270, 60, "Public Subnet c"),
        vpc_group("prv3", 690, 340, 270, 130, "Private Subnet c"),
        aws_icon("ec3", 790, 370, "ec2", 40, 40),
        label("ec3_l", 760, 418, "EC2 c", 100, bold=False),
        # Edges
        arrow("e1", "ec1", "ngw1", CLR_NAT),
        arrow("e2", "ec2b", "ngw2", CLR_NAT),
        arrow("e3", "ec3", "ngw3", CLR_NAT),
        # Note
        note("n1", 20, 525, 960, 60,
             "◎ 正解 C: 各 AZ にそれぞれ NAT GW を配置 + ルートテーブルは同一 AZ の NAT GW 向き。AZ 障害時も他 AZ に影響しない。Multi-AZ 障害耐性 ○ / Lambda 自動復旧不要 / コスト最適化 (AZ 跨ぎデータ転送料回避)。",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d337", "NAT GW HA across 3 AZs", cells)


def diag_342():
    """Gateway VPC Endpoint for S3 (cost optimization)"""
    cells = [
        title("t", 0, 10, "UDEMY-043 / num=342: S3 Gateway Endpoint でデータ転送コスト削減"),
        # Before
        box("before", 30, 60, 450, 440, "Before: NAT GW 経由 (高コスト)", fill="#FDEBE9", stroke="#DD344C"),
        vpc_group("vpc1", 60, 100, 380, 260, "VPC"),
        aws_icon("ec_a", 100, 140, "ec2", 50, 50),
        label("ec_a_l", 70, 200, "EC2", 110),
        aws_icon_color("ngw_a", 260, 140, "nat_gateway", CLR_NAT, 50, 50),
        label("ngw_a_l", 230, 200, "NAT Gateway", 110),
        aws_icon("igw_a", 370, 140, "internet_gateway", 50, 50),
        label("igw_a_l", 340, 200, "IGW", 110),
        aws_icon("s3_a", 360, 260, "simple_storage_service", 50, 50),
        label("s3_a_l", 330, 320, "Amazon S3", 110),
        arrow("e_a1", "ec_a", "ngw_a", CLR_NAT, w=2, label_text="1.5 TB/day"),
        arrow("e_a2", "ngw_a", "igw_a", CLR_NAT, w=2),
        arrow("e_a3", "igw_a", "s3_a", "#666", w=2),
        note("nb1", 55, 370, 400, 115,
             "問題: NAT GW のデータ処理料 $0.045/GB × 1.5TB/日 = 膨大\nS3 は同リージョンでも NAT GW + IGW を経由するため課金される"),
        # After
        box("after", 520, 60, 450, 440, "After: Gateway Endpoint (無料)", fill="#EBF5E8", stroke="#7AA116"),
        vpc_group("vpc2", 550, 100, 380, 260, "VPC"),
        aws_icon("ec_b", 590, 140, "ec2", 50, 50),
        label("ec_b_l", 560, 200, "EC2", 110),
        aws_icon_color("gep", 750, 140, "endpoint", CLR_EP, 50, 50),
        label("gep_l", 710, 200, "S3 Gateway EP", 130),
        aws_icon("s3_b", 820, 260, "simple_storage_service", 50, 50),
        label("s3_b_l", 790, 320, "Amazon S3", 110),
        arrow("e_b1", "ec_b", "gep", CLR_EP, w=2, label_text="1.5 TB/day"),
        arrow("e_b2", "gep", "s3_b", CLR_EP, w=2),
        note("na1", 545, 370, 400, 115,
             "◎ 正解 C: Service Catalog + S3 Gateway Endpoint を標準化。\n・Gateway Endpoint 利用料 無料\n・データ転送料 無料 (同リージョン)\n・経路 = VPC → Gateway EP → S3 (IGW/NAT 経由せず)"),
        # Bottom
        note("bot", 30, 515, 940, 60,
             "Gateway EP 対象 = S3 / DynamoDB のみ (無料)。それ以外は Interface Endpoint (PrivateLink, 時間課金あり)。Route Table にプレフィックスリストを追加して有効化。"),
    ]
    return wrap("d342", "S3 Gateway Endpoint Cost Optimization", cells)


def diag_356():
    """DX + Private VIF + DX Gateway to multi-account S3"""
    cells = [
        title("t", 0, 10, "UDEMY-057 / num=356: DX + Private VIF + DX GW で複数アカウント S3 へプライベート転送"),
        # Research sites
        dc_group("dc1", 20, 80, 150, 140, "研究施設 1"),
        aws_icon("dc1_s", 55, 110, "corporate_data_center_2", 50, 50),
        label("dc1_l", 30, 170, "臨床試験データ", 130, bold=False),
        dc_group("dc2", 20, 240, 150, 140, "研究施設 2"),
        aws_icon("dc2_s", 55, 270, "corporate_data_center_2", 50, 50),
        label("dc2_l", 30, 330, "臨床試験データ", 130, bold=False),
        # DX
        aws_icon_color("dx", 220, 190, "direct_connect", CLR_DX, 60, 60),
        label("dx_l", 190, 258, "Direct Connect", 120),
        # DX GW
        aws_icon_color("dxgw", 360, 190, "direct_connect", CLR_DX, 60, 60),
        label("dxgw_l", 320, 258, "DX Gateway", 130),
        label("dxgw_l2", 320, 276, "(Private VIF)", 130, bold=False, size=10),
        # Networking account VPC
        vpc_group("netvpc", 490, 100, 220, 320, "Network アカウント VPC"),
        aws_icon_color("vgw", 560, 140, "vpn_gateway", CLR_TGW, 60, 60),
        label("vgw_l", 530, 208, "VGW", 120),
        aws_icon_color("gw_s3", 560, 270, "endpoint", CLR_EP, 60, 60),
        label("gw_s3_l", 520, 338, "S3 Gateway EP", 140),
        # S3 across 3 accounts
        box("acc_box", 750, 80, 230, 440, "S3 を持つ 3 つの別アカウント", fill="#EBF1FF", stroke="#3B48CC"),
        aws_icon("s3_1", 840, 130, "simple_storage_service", 50, 50),
        label("s3_1_l", 780, 190, "S3 バケット 1", 170),
        aws_icon("s3_2", 840, 260, "simple_storage_service", 50, 50),
        label("s3_2_l", 780, 320, "S3 バケット 2", 170),
        aws_icon("s3_3", 840, 390, "simple_storage_service", 50, 50),
        label("s3_3_l", 780, 450, "S3 バケット 3", 170),
        # Links
        arrow("e1", "dc1_s", "dx", CLR_DX, w=2),
        arrow("e2", "dc2_s", "dx", CLR_DX, w=2),
        arrow("e3", "dx", "dxgw", CLR_DX, w=3, label_text="Private VIF"),
        arrow("e4", "dxgw", "vgw", CLR_DX, w=3),
        arrow("e5", "vgw", "gw_s3", CLR_EP, w=2),
        arrow("e6", "gw_s3", "s3_1", "#666", w=2),
        arrow("e7", "gw_s3", "s3_2", "#666", w=2),
        arrow("e8", "gw_s3", "s3_3", "#666", w=2),
        # Note
        note("n1", 30, 495, 700, 90,
             "◎ 正解 AC: Networking 専用アカウントに VPC を作り DX + Private VIF + DX GW で接続。S3 Gateway EP 経由でプライベート通信。\nパブリックインターネット不経由 / 複数アカウント S3 を単一 DX でカバー。",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d356", "DX Private VIF to Multi-account S3", cells)


def diag_386():
    """Shared Services VPC + GWLB + 3rd party FW HA"""
    cells = [
        title("t", 0, 10, "UDEMY-087 / num=386: GWLB で サードパーティ FW を透過挿入 (HA構成)"),
        # App VPC
        vpc_group("app", 30, 70, 220, 380, "App VPC (スポーク)"),
        aws_icon("app_ec2", 90, 100, "ec2", 50, 50),
        label("app_ec2_l", 60, 160, "EC2 (Private)", 110),
        aws_icon_color("gwlbe", 90, 280, "endpoint", CLR_EP, 50, 50),
        label("gwlbe_l", 50, 340, "GWLB Endpoint", 130),
        label("gwlbe_l2", 50, 358, "(VPC Endpoint)", 130, bold=False, size=10),
        # Shared Services VPC
        vpc_group("svc", 290, 70, 440, 380, "共有サービス VPC (検査集約)"),
        box("az_a", 310, 110, 170, 310, "AZ-a", fill="#FFF5EB", stroke="#FF9900"),
        aws_icon("fw1", 350, 150, "ec2", 50, 50, fill="#DD344C"),
        label("fw1_l", 320, 210, "3rd Party FW a", 130, bold=False),
        box("az_b", 540, 110, 170, 310, "AZ-b", fill="#FFF5EB", stroke="#FF9900"),
        aws_icon("fw2", 580, 150, "ec2", 50, 50, fill="#DD344C"),
        label("fw2_l", 550, 210, "3rd Party FW b", 130, bold=False),
        aws_icon("gwlb", 480, 300, "elastic_load_balancing", 60, 60, fill="#8C4FFF"),
        label("gwlb_l", 440, 368, "Gateway Load Balancer", 170),
        # Internet
        aws_icon("igw", 790, 130, "internet_gateway", 50, 50),
        label("igw_l", 760, 190, "IGW", 110),
        aws_icon("net", 790, 300, "internet_gateway", 50, 50, fill="#666"),
        label("net_l", 760, 360, "Internet", 110),
        # Edges
        arrow("e1", "app_ec2", "gwlbe", CLR_EP, w=2, label_text="0.0.0.0/0"),
        arrow("e2", "gwlbe", "gwlb", "#8C4FFF", w=3, label_text="GENEVE"),
        arrow("e3", "gwlb", "fw1", "#DD344C", w=2),
        arrow("e4", "gwlb", "fw2", "#DD344C", w=2),
        arrow("e5", "fw1", "gwlb", "#DD344C", w=2, dashed=True),
        arrow("e6", "fw2", "gwlb", "#DD344C", w=2, dashed=True),
        arrow("e7", "gwlb", "igw", "#8C4FFF", w=3),
        arrow("e8", "igw", "net", "#666", w=2),
        # Note
        note("n1", 20, 470, 960, 115,
             "◎ 正解 A: 共有サービス VPC に 2 台の FW を 別 AZ に配置 → GWLB 背後に Target Group 登録。\n各スポーク VPC に GWLB Endpoint (GWLBE) を置き、ルートテーブルで 0.0.0.0/0 を GWLBE へ。GENEVE カプセル化で透過挿入。\nFW 障害時は GWLB が他 AZ へフェイルオーバー (AZ 耐障害 ○)。ALB/NLB では L3 透過挿入不可。",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d386", "GWLB Third-party FW HA", cells)


def diag_413():
    """Multi-country DC + TGW + Route Table segmentation"""
    cells = [
        title("t", 0, 10, "UDEMY-114 / num=413: TGW Route Table でセキュリティゾーン分離"),
        # Onprem
        dc_group("dc1", 20, 70, 140, 100, "DC 米国"),
        aws_icon("dc1_s", 50, 90, "corporate_data_center_2", 50, 50),
        dc_group("dc2", 20, 200, 140, 100, "DC 欧州"),
        aws_icon("dc2_s", 50, 220, "corporate_data_center_2", 50, 50),
        dc_group("dc3", 20, 330, 140, 100, "DC アジア"),
        aws_icon("dc3_s", 50, 350, "corporate_data_center_2", 50, 50),
        # VPN
        aws_icon_color("vpn", 200, 230, "site_to_site_vpn", CLR_VPN, 60, 60),
        label("vpn_l", 170, 298, "Site-to-Site VPN", 120),
        # TGW
        aws_icon_color("tgw", 340, 230, "transit_gateway", CLR_TGW, 70, 70),
        label("tgw_l", 310, 305, "Transit Gateway", 130),
        label("tgw_l2", 310, 323, "(RAM 共有)", 130, bold=False, size=10),
        # Route Tables
        box("rt_prod", 480, 70, 250, 160, "RT: Production", fill="#FDEBE9", stroke="#DD344C"),
        vpc_group("v_prod1", 500, 110, 95, 100, "Prod VPC 1"),
        vpc_group("v_prod2", 615, 110, 95, 100, "Prod VPC 2"),
        box("rt_dev", 480, 250, 250, 160, "RT: Dev / Test", fill="#EBF5E8", stroke="#7AA116"),
        vpc_group("v_dev1", 500, 290, 95, 100, "Dev VPC 1"),
        vpc_group("v_dev2", 615, 290, 95, 100, "Dev VPC 2"),
        box("rt_shared", 760, 150, 220, 220, "RT: Shared (全関連)", fill="#EBF1FF", stroke="#3B48CC"),
        vpc_group("v_shared", 785, 200, 170, 140, "共有 VPC (監査/ログ/管理)"),
        # Arrows
        arrow("e1", "dc1_s", "vpn", CLR_VPN, w=2),
        arrow("e2", "dc2_s", "vpn", CLR_VPN, w=2),
        arrow("e3", "dc3_s", "vpn", CLR_VPN, w=2),
        arrow("e4", "vpn", "tgw", CLR_VPN, w=3),
        arrow("e5", "tgw", "v_prod1", CLR_TGW, w=2),
        arrow("e6", "tgw", "v_prod2", CLR_TGW, w=2),
        arrow("e7", "tgw", "v_dev1", CLR_TGW, w=2),
        arrow("e8", "tgw", "v_dev2", CLR_TGW, w=2),
        arrow("e9", "tgw", "v_shared", CLR_TGW, w=2),
        # Note
        note("n1", 20, 440, 960, 140,
             "◎ 正解 C: TGW に 複数 Route Table を作成し VPC/VPN を関連付け → セキュリティ境界を厳格に分離。\n・Prod RT = Prod VPC 同士 + Shared のみ。Dev と疎通しない\n・Dev RT = Dev VPC 同士 + Shared のみ。Prod と疎通しない\n・Shared RT = 全 VPC から参照可 (監査/ログ集約)\n1 台の TGW で数百 VPC を集約 + 細粒度の分離が可能。AWS PrivateLink や VPC Peering では推移/スケールで不足。",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d413", "TGW Route Table Segmentation", cells)


def diag_427():
    """NAT GW in each AZ + Multi-AZ RDS + ASG"""
    cells = [
        title("t", 0, 10, "UDEMY-128 / num=427: マルチ AZ 可用性パターン (NAT GW / RDS / ASG)"),
        vpc_group("vpc", 30, 60, 940, 450, "VPC"),
        # AZ-a
        box("az1", 60, 110, 430, 380, "AZ-a", fill="#FFF5EB", stroke="#FF9900"),
        aws_icon_color("ngw1", 130, 150, "nat_gateway", CLR_NAT),
        label("ngw1_l", 100, 218, "NAT GW a", 120),
        aws_icon("alb1", 310, 150, "elastic_load_balancing", 60, 60, fill="#8C4FFF"),
        label("alb1_l", 280, 218, "ALB (a)", 120),
        aws_icon("ec1", 130, 280, "ec2", 50, 50),
        label("ec1_l", 100, 340, "EC2 ASG a", 120),
        aws_icon("rds1", 300, 280, "rds", 50, 50, fill="#3B48CC"),
        label("rds1_l", 270, 340, "RDS (Primary)", 120),
        # AZ-b
        box("az2", 510, 110, 430, 380, "AZ-b", fill="#FFF5EB", stroke="#FF9900"),
        aws_icon_color("ngw2", 580, 150, "nat_gateway", CLR_NAT),
        label("ngw2_l", 550, 218, "NAT GW b", 120),
        aws_icon("alb2", 760, 150, "elastic_load_balancing", 60, 60, fill="#8C4FFF"),
        label("alb2_l", 730, 218, "ALB (b)", 120),
        aws_icon("ec2b", 580, 280, "ec2", 50, 50),
        label("ec2b_l", 550, 340, "EC2 ASG b", 120),
        aws_icon("rds2", 750, 280, "rds", 50, 50, fill="#3B48CC"),
        label("rds2_l", 720, 340, "RDS (Standby)", 120),
        # Edges
        arrow("e1", "ec1", "ngw1", CLR_NAT),
        arrow("e2", "ec2b", "ngw2", CLR_NAT),
        edge("e3", "rds1", "rds2", "#3B48CC", dashed=True, w=2, label_text="Multi-AZ 同期レプリ"),
        arrow("e4", "alb1", "ec1", "#8C4FFF"),
        arrow("e5", "alb2", "ec2b", "#8C4FFF"),
        # Note
        note("n1", 20, 525, 960, 60,
             "◎ 正解 A: 追加 AZ に NAT GW を配置 + ルートテーブル更新 / RDS Multi-AZ / ASG を複数 AZ 分散。単一 AZ 障害でもアプリ継続。",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d427", "Multi-AZ HA Pattern", cells)


def diag_442():
    """Client VPN for remote workforce (vs Site-to-Site VPN scaling)"""
    cells = [
        title("t", 0, 10, "UDEMY-143 / num=442: Client VPN で個人デバイスを AWS VPC に直接接続"),
        # Remote users
        box("users", 20, 60, 240, 450, "リモートワーカー (自宅)", fill="#F5F5F5", stroke="#666"),
        aws_icon("u1", 80, 100, "corporate_data_center_2", 40, 40),
        label("u1_l", 50, 150, "Laptop A", 110, bold=False),
        aws_icon("u2", 80, 220, "corporate_data_center_2", 40, 40),
        label("u2_l", 50, 270, "Laptop B", 110, bold=False),
        aws_icon("u3", 80, 340, "corporate_data_center_2", 40, 40),
        label("u3_l", 50, 390, "Laptop C", 110, bold=False),
        # Client VPN Endpoint
        aws_icon_color("cvpn", 300, 240, "site_to_site_vpn", CLR_VPN, 70, 70),
        label("cvpn_l", 260, 315, "Client VPN", 150),
        label("cvpn_l2", 260, 333, "Endpoint (TLS)", 150, bold=False, size=10),
        # VPC A
        vpc_group("vpc", 450, 80, 520, 420, "VPC A (内部アプリケーション)"),
        aws_icon("app1", 520, 130, "ec2", 50, 50),
        label("app1_l", 490, 190, "内部アプリ EC2", 120),
        aws_icon("app2", 650, 130, "ec2", 50, 50),
        label("app2_l", 620, 190, "RDS / DB", 120),
        aws_icon("ad", 800, 130, "identity_and_access_management", 50, 50, fill="#DD344C"),
        label("ad_l", 770, 190, "AD / SAML IdP", 130),
        aws_icon("sg", 650, 280, "identity_and_access_management", 50, 50),
        label("sg_l", 620, 340, "Security Group", 130),
        label("sg_l2", 620, 358, "(認証ユーザーのみ)", 130, bold=False, size=10),
        # Edges
        arrow("e1", "u1", "cvpn", CLR_VPN),
        arrow("e2", "u2", "cvpn", CLR_VPN),
        arrow("e3", "u3", "cvpn", CLR_VPN),
        arrow("e4", "cvpn", "app1", CLR_VPN, w=2),
        arrow("e5", "cvpn", "app2", CLR_VPN, w=2),
        edge("e6", "cvpn", "ad", "#DD344C", dashed=True, label_text="SAML 認証"),
        # Note
        note("n1", 20, 525, 960, 60,
             "◎ 正解 D: Client VPN Endpoint は個人デバイスから VPC へ TLS 接続。ユーザー認証は SAML/Cert。Site-to-Site VPN と違い個別端末向け。\nS2S VPN は『拠点ネットワーク間』で、端末数スケール不向き。Client VPN は端末単位で従量課金、スケール容易。",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d442", "Client VPN for Remote Workforce", cells)


def diag_461():
    """Interface VPC Endpoint to SaaS via PrivateLink"""
    cells = [
        title("t", 0, 10, "UDEMY-162 / num=461: PrivateLink Interface EP で SaaS プロバイダに接続"),
        # Consumer VPC
        vpc_group("cvpc", 30, 80, 360, 400, "Consumer VPC (分析システム)"),
        aws_icon("ec", 90, 140, "ec2", 60, 60),
        label("ec_l", 60, 208, "EC2 分析ワーカー", 130),
        aws_icon_color("iep", 260, 140, "endpoint", CLR_EP, 60, 60),
        label("iep_l", 220, 208, "Interface EP (ENI)", 140),
        vpc_group("priv", 60, 270, 310, 180, "Private Subnet"),
        aws_icon("sg", 180, 310, "identity_and_access_management", 50, 50),
        label("sg_l", 150, 370, "Security Group", 120),
        # SaaS Provider
        vpc_group("pvpc", 620, 80, 360, 400, "Provider VPC (SaaS)"),
        aws_icon_color("eps", 680, 140, "endpoint", CLR_EP, 60, 60),
        label("eps_l", 640, 208, "Endpoint Service", 140),
        aws_icon("nlb", 820, 140, "elastic_load_balancing", 60, 60, fill="#8C4FFF"),
        label("nlb_l", 790, 208, "NLB", 120),
        aws_icon("saas", 820, 280, "ec2", 60, 60, fill="#E7157B"),
        label("saas_l", 790, 348, "SaaS App", 120),
        # PrivateLink pipe
        aws_icon_color("pl", 470, 160, "endpoint", "#6B1B9A", 60, 60),
        label("pl_l", 420, 228, "AWS PrivateLink", 160),
        # Edges
        arrow("e1", "ec", "iep", CLR_EP, w=2),
        arrow("e2", "iep", "pl", "#6B1B9A", w=3),
        arrow("e3", "pl", "eps", "#6B1B9A", w=3),
        arrow("e4", "eps", "nlb", "#8C4FFF", w=2),
        arrow("e5", "nlb", "saas", "#E7157B", w=2),
        # Note
        note("n1", 20, 500, 960, 85,
             "◎ 正解 A: Consumer VPC に Interface VPC Endpoint (ENI) を作成し Provider の Endpoint Service に接続。パブリックインターネット経由せずプライベート通信。\nPrivateLink は片方向接続で CIDR 重複可。Provider 側は NLB がバックエンド。SG/EP ポリシーで細粒度制御。",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d461", "PrivateLink Interface EP to SaaS", cells)


def diag_466():
    """DX redundancy with DX Gateway + 2 DX connections"""
    cells = [
        title("t", 0, 10, "UDEMY-167 / num=466: DX 冗長化 — 2 本の DX + DX Gateway"),
        # Onprem
        dc_group("dc", 30, 80, 220, 300, "オンプレミスネットワーク"),
        aws_icon("dc_s", 100, 120, "corporate_data_center_2", 60, 60),
        label("dc_s_l", 70, 188, "オンプレサーバ", 130),
        aws_icon("cgw1", 60, 250, "customer_gateway", 50, 50),
        label("cgw1_l", 30, 310, "Router (Loc1)", 110, bold=False),
        aws_icon("cgw2", 170, 250, "customer_gateway", 50, 50),
        label("cgw2_l", 140, 310, "Router (Loc2)", 110, bold=False),
        # DX connections - 2 geographically separated
        aws_icon_color("dx1", 310, 130, "direct_connect", CLR_DX, 60, 60),
        label("dx1_l", 270, 198, "DX 接続 A", 140),
        label("dx1_l2", 270, 216, "(ロケ 1 / 1Gbps)", 140, bold=False, size=10),
        aws_icon_color("dx2", 310, 260, "direct_connect", CLR_DX, 60, 60),
        label("dx2_l", 270, 328, "DX 接続 B", 140),
        label("dx2_l2", 270, 346, "(ロケ 2 / 1Gbps)", 140, bold=False, size=10),
        # DX Gateway
        aws_icon_color("dxgw", 470, 190, "direct_connect", "#6B1B9A", 70, 70),
        label("dxgw_l", 430, 265, "DX Gateway", 150),
        label("dxgw_l2", 430, 283, "(Private VIF x2)", 150, bold=False, size=10),
        # VPC
        vpc_group("vpc", 620, 90, 340, 330, "VPC (単一 / 会社リソース)"),
        aws_icon_color("vgw", 680, 140, "vpn_gateway", CLR_TGW, 60, 60),
        label("vgw_l", 650, 208, "VGW", 120),
        aws_icon("ec", 820, 140, "ec2", 60, 60),
        label("ec_l", 790, 208, "EC2 ワークロード", 130),
        aws_icon("rds", 820, 280, "rds", 60, 60, fill="#3B48CC"),
        label("rds_l", 790, 348, "RDS", 120),
        # Edges
        arrow("e1", "cgw1", "dx1", CLR_DX, w=3),
        arrow("e2", "cgw2", "dx2", CLR_DX, w=3),
        arrow("e3", "dx1", "dxgw", CLR_DX, w=3, label_text="Private VIF 1"),
        arrow("e4", "dx2", "dxgw", CLR_DX, w=3, label_text="Private VIF 2"),
        arrow("e5", "dxgw", "vgw", "#6B1B9A", w=3),
        # Note
        note("n1", 20, 440, 960, 140,
             "◎ 正解 A: 既存 PVIF を削除 → DX Gateway を導入 → 2 本目 DX を敷設 → 各 DX に PVIF を作り DX Gateway へアタッチ → DX Gateway を VPC の VGW に接続。\n・2 本目 DX は別ロケ / 別キャリアで地理冗長\n・BGP で経路フェイルオーバー自動 (Active/Active or Active/Passive)\n・片方障害時も継続通信\n・DX Gateway があることで将来 TGW へ拡張容易 (Transit VIF)",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d466", "DX Redundancy with DX Gateway", cells)


def diag_479():
    """TGW RAM share + StackSet for 100 accounts"""
    cells = [
        title("t", 0, 10, "UDEMY-180 / num=479: TGW RAM 共有 + StackSet で 100 アカウント自動化"),
        # Mgmt account
        box("mgmt", 30, 80, 300, 420, "管理アカウント", fill="#EBF1FF", stroke="#3B48CC"),
        aws_icon_color("tgw", 120, 130, "transit_gateway", CLR_TGW, 70, 70),
        label("tgw_l", 80, 205, "Transit Gateway", 150),
        aws_icon_color("ram", 120, 260, "resource_access_manager", "#3B48CC", 70, 70),
        label("ram_l", 80, 335, "AWS RAM", 150),
        label("ram_l2", 80, 353, "TGW 共有", 150, bold=False, size=10),
        aws_icon("ssets", 120, 400, "cloudformation", 70, 70, fill="#E7157B"),
        label("ssets_l", 80, 475, "CloudFormation", 150),
        label("ssets_l2", 80, 490, "StackSet", 150, bold=False, size=10),
        # Member accounts
        box("memb", 380, 80, 600, 420, "Organizations メンバーアカウント (x 100)", fill="#F5F5F5", stroke="#666"),
        # Account 1
        vpc_group("a1v", 410, 130, 160, 140, "Acc1 VPC"),
        aws_icon_color("a1tga", 440, 200, "transit_gateway", CLR_TGW, 50, 50),
        label("a1tga_l", 410, 260, "TGW Attach", 120),
        # Account 2
        vpc_group("a2v", 600, 130, 160, 140, "Acc2 VPC"),
        aws_icon_color("a2tga", 630, 200, "transit_gateway", CLR_TGW, 50, 50),
        label("a2tga_l", 600, 260, "TGW Attach", 120),
        # Account N
        vpc_group("aNv", 790, 130, 160, 140, "AccN VPC"),
        aws_icon_color("aNtga", 820, 200, "transit_gateway", CLR_TGW, 50, 50),
        label("aNtga_l", 790, 260, "TGW Attach", 120),
        # More line
        label("dots", 410, 310, "...", 540, bold=True, size=20),
        # Automation flow
        aws_icon("org", 500, 360, "cloudformation", 60, 60, fill="#E7157B"),
        label("org_l", 470, 428, "StackSet 自動展開", 130),
        label("org_l2", 470, 446, "(新アカウント作成→VPC+Attach 作成)", 200, bold=False, size=10),
        # Arrows
        arrow("r1", "tgw", "ram", "#3B48CC", dashed=True, w=2),
        arrow("r2", "ram", "a1tga", "#3B48CC", w=2, label_text="Share TGW"),
        arrow("r3", "ram", "a2tga", "#3B48CC", w=2),
        arrow("r4", "ram", "aNtga", "#3B48CC", w=2),
        arrow("r5", "ssets", "org", "#E7157B", w=2),
        arrow("r6", "org", "a1tga", "#E7157B", dashed=True),
        arrow("r7", "org", "a2tga", "#E7157B", dashed=True),
        arrow("r8", "org", "aNtga", "#E7157B", dashed=True),
        # Note
        note("n1", 20, 520, 960, 65,
             "◎ 正解 CA: 管理アカウントで TGW を RAM 共有 + StackSet を全メンバーに展開 → 新アカウント追加時に VPC+TGW Attach を自動作成。\nSCP や手動アタッチ不要で線形スケール。",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d479", "TGW RAM + StackSet Automation", cells)


def diag_489():
    """S3 Gateway EP for private S3 access from VPC"""
    cells = [
        title("t", 0, 10, "UDEMY-190 / num=489: S3 Gateway Endpoint で VPC から S3 へプライベート直通"),
        vpc_group("vpc", 30, 70, 700, 420, "VPC (2 AZ / 分析サービス)"),
        # AZ a
        box("az1", 60, 110, 320, 340, "AZ-a", fill="#FFF5EB", stroke="#FF9900"),
        vpc_group("priv1", 80, 150, 280, 120, "Private Subnet"),
        aws_icon("ec1", 180, 180, "ec2", 50, 50),
        label("ec1_l", 150, 240, "EC2 分析ノード a", 130),
        vpc_group("pub1", 80, 290, 280, 130, "Public Subnet"),
        aws_icon_color("ngw1", 190, 320, "nat_gateway", CLR_NAT, 40, 40),
        label("ngw1_l", 160, 370, "NAT GW a", 110, bold=False),
        # AZ b
        box("az2", 400, 110, 320, 340, "AZ-b", fill="#FFF5EB", stroke="#FF9900"),
        vpc_group("priv2", 420, 150, 280, 120, "Private Subnet"),
        aws_icon("ec2b", 520, 180, "ec2", 50, 50),
        label("ec2b_l", 490, 240, "EC2 分析ノード b", 130),
        vpc_group("pub2", 420, 290, 280, 130, "Public Subnet"),
        aws_icon_color("ngw2", 530, 320, "nat_gateway", CLR_NAT, 40, 40),
        label("ngw2_l", 500, 370, "NAT GW b", 110, bold=False),
        # Gateway Endpoint (spans VPC)
        aws_icon_color("gep", 360, 390, "endpoint", CLR_EP, 60, 60),
        label("gep_l", 320, 460, "S3 Gateway EP", 140),
        # S3
        aws_icon("s3", 820, 240, "simple_storage_service", 70, 70),
        label("s3_l", 770, 315, "Amazon S3 バケット", 170),
        label("s3_l2", 770, 333, "(バケットポリシー = EP 限定)", 190, bold=False, size=10),
        # Edges
        arrow("e1", "ec1", "gep", CLR_EP, w=2),
        arrow("e2", "ec2b", "gep", CLR_EP, w=2),
        arrow("e3", "gep", "s3", CLR_EP, w=3, label_text="プライベート経路"),
        # Note
        note("n1", 20, 500, 960, 85,
             "◎ 正解 C: S3 Gateway Endpoint を VPC に作成 → Route Table に S3 プレフィックスリストを追加 → EC2 はプライベートのまま S3 に到達。\n・Gateway EP は 無料 / 同リージョン S3・DynamoDB 専用\n・バケットポリシーで aws:sourceVpce 条件 → EP 経由のみ許可\n・NAT GW / IGW を経由しないため転送コストとセキュリティが大幅改善",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d489", "S3 Gateway Endpoint", cells)


def diag_502():
    """VPC Prefix List + RAM share for multi-account SG rules"""
    cells = [
        title("t", 0, 10, "UDEMY-203 / num=502: VPC プレフィックスリスト + RAM 共有 で SG 一元管理"),
        # Central management
        box("mgmt", 30, 80, 300, 420, "中央管理アカウント", fill="#EBF1FF", stroke="#3B48CC"),
        aws_icon("plist", 120, 130, "vpc", 70, 70, fill="#3B48CC"),
        label("plist_l", 80, 205, "Prefix List", 150),
        label("plist_l2", 80, 223, "(全社内 IP 範囲)", 150, bold=False, size=10),
        aws_icon_color("ram", 120, 270, "resource_access_manager", "#3B48CC", 70, 70),
        label("ram_l", 80, 345, "AWS RAM", 150),
        aws_icon_color("tgw", 120, 400, "transit_gateway", CLR_TGW, 60, 60),
        label("tgw_l", 80, 468, "TGW (VPN 終端)", 150),
        # Office
        dc_group("office", 30, 510, 300, 70, "オフィス / リモート (Site-to-Site VPN)"),
        # Member accounts
        box("memb", 380, 80, 600, 420, "他のメンバーアカウント (複数)", fill="#F5F5F5", stroke="#666"),
        vpc_group("va", 400, 130, 180, 160, "Acc A VPC"),
        aws_icon("sga", 460, 170, "identity_and_access_management", 50, 50),
        label("sga_l", 430, 230, "SG (Prefix List)", 130),
        aws_icon("eca", 460, 250, "ec2", 40, 40),
        vpc_group("vb", 610, 130, 180, 160, "Acc B VPC"),
        aws_icon("sgb", 670, 170, "identity_and_access_management", 50, 50),
        label("sgb_l", 640, 230, "SG (Prefix List)", 130),
        aws_icon("ecb", 670, 250, "ec2", 40, 40),
        vpc_group("vc", 820, 130, 140, 160, "Acc C VPC"),
        aws_icon("sgc", 860, 170, "identity_and_access_management", 50, 50),
        label("sgc_l", 830, 230, "SG", 120),
        aws_icon("ecc", 860, 250, "ec2", 40, 40),
        # Arrows
        arrow("e1", "ram", "sga", "#3B48CC", w=2, label_text="Share Prefix List"),
        arrow("e2", "ram", "sgb", "#3B48CC", w=2),
        arrow("e3", "ram", "sgc", "#3B48CC", w=2),
        # Note
        note("n1", 20, 325, 350, 160,
             "問題: Config/パッチ更新など中央管理システムから\n全 VPC の EC2 へアクセス許可が必要。\n各 SG を個別メンテはスケールしない。"),
        note("n2", 380, 520, 600, 65,
             "◎ 正解 C: 中央アカウントで Prefix List を作成 → RAM で全アカウントに共有 → 各 SG のソースに PL を指定。\nオンプレ IP 追加時は PL を更新するだけで全 SG に自動反映。",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d502", "VPC Prefix List + RAM", cells)


def diag_505():
    """BYOIP + NAT GW with Elastic IP for allowlist"""
    cells = [
        title("t", 0, 10, "UDEMY-206 / num=505: BYOIP + NAT Gateway で固定 IP から外部 API 呼び出し"),
        # Company public IP block
        dc_group("co", 30, 80, 180, 160, "会社所有 IP ブロック"),
        aws_icon("ipblk", 70, 110, "route_53", 50, 50, fill="#E7157B"),
        label("ipblk_l", 40, 170, "PUBLIC /24", 140),
        label("ipblk_l2", 40, 188, "(BYOIP 登録)", 140, bold=False, size=10),
        # VPC
        vpc_group("vpc", 260, 80, 420, 370, "VPC"),
        vpc_group("priv", 280, 130, 220, 280, "Private Subnet"),
        aws_icon("ec", 350, 170, "ec2", 50, 50),
        label("ec_l", 320, 230, "EC2 Web App", 120),
        vpc_group("pub", 520, 130, 150, 280, "Public Subnet"),
        aws_icon_color("ngw", 550, 170, "nat_gateway", CLR_NAT, 60, 60),
        label("ngw_l", 520, 238, "NAT GW", 120),
        label("ngw_l2", 520, 256, "EIP = BYOIP", 120, bold=False, size=10),
        aws_icon("eip", 550, 310, "route_53", 50, 50, fill="#E7157B"),
        label("eip_l", 520, 370, "Elastic IP", 120),
        # IGW
        aws_icon("igw", 720, 170, "internet_gateway", 60, 60),
        label("igw_l", 690, 238, "IGW", 120),
        # 3rd party API
        dc_group("api", 810, 80, 170, 160, "3rd Party API"),
        aws_icon("fw", 840, 110, "security_hub", 50, 50, fill="#DD344C"),
        label("fw_l", 810, 170, "Firewall", 140),
        label("fw_l2", 810, 188, "(許可 IP = 1 つ)", 140, bold=False, size=10),
        # Edges
        arrow("e1", "ipblk", "eip", "#E7157B", dashed=True, w=2, label_text="Register"),
        arrow("e2", "ec", "ngw", CLR_NAT, w=2),
        arrow("e3", "ngw", "igw", CLR_NAT, w=2),
        arrow("e4", "igw", "fw", "#666", w=2, label_text="BYOIP 発信"),
        # Note
        note("n1", 20, 470, 960, 120,
             "◎ 正解 B: 自社所有のパブリック /24 を BYOIP で AWS に登録 → そのブロックから EIP を作成 → NAT GW に割り当て。\n・NAT GW 経由の発信トラフィックは BYOIP の EIP がソース IP になる\n・既存の許可 IP を変更せず AWS に移行できる\n・「AWS に移行後もパートナーの許可リストが 1 つしかない」「EIP を何度も変えたくない」ケースの定石",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d505", "BYOIP + NAT GW", cells)


def diag_526():
    """TGW + Site-to-Site VPN + VPC-A/B"""
    cells = [
        title("t", 0, 10, "UDEMY-227 / num=526: TGW に VPN + 複数 VPC を集約"),
        # Onprem DC
        dc_group("dc", 30, 80, 200, 260, "オンプレ DC (金融情報 要保管)"),
        aws_icon("dcs", 80, 120, "corporate_data_center_2", 50, 50),
        label("dcs_l", 50, 180, "機密システム", 110),
        aws_icon("cgw", 80, 230, "customer_gateway", 50, 50),
        label("cgw_l", 50, 290, "CGW (Router)", 110, bold=False),
        # VPN
        aws_icon_color("vpn", 280, 190, "site_to_site_vpn", CLR_VPN, 60, 60),
        label("vpn_l", 250, 258, "Site-to-Site VPN", 120),
        # TGW
        aws_icon_color("tgw", 430, 190, "transit_gateway", CLR_TGW, 70, 70),
        label("tgw_l", 390, 265, "Transit Gateway", 150),
        # VPC A
        vpc_group("vpcA", 600, 80, 360, 180, "VPC A (既存 / オンプレ連携)"),
        aws_icon("ecA", 680, 130, "ec2", 50, 50),
        label("ecA_l", 650, 190, "EC2 / RDS 既存", 120),
        aws_icon_color("tgwaA", 830, 130, "transit_gateway", CLR_TGW, 50, 50),
        label("tgwaA_l", 800, 190, "TGW Attach", 120),
        # VPC B
        vpc_group("vpcB", 600, 290, 360, 180, "VPC B (新規)"),
        aws_icon("ecB", 680, 340, "ec2", 50, 50),
        label("ecB_l", 650, 400, "EC2 新システム", 120),
        aws_icon_color("tgwaB", 830, 340, "transit_gateway", CLR_TGW, 50, 50),
        label("tgwaB_l", 800, 400, "TGW Attach", 120),
        # Edges
        arrow("e1", "cgw", "vpn", CLR_VPN, w=3),
        arrow("e2", "vpn", "tgw", CLR_VPN, w=3),
        arrow("e3", "tgw", "tgwaA", CLR_TGW, w=3),
        arrow("e4", "tgw", "tgwaB", CLR_TGW, w=3),
        # Note
        note("n1", 20, 490, 960, 95,
             "◎ 正解 A: TGW を新規作成 → VPN + VPC A + VPC B を全てアタッチ → TGW RT で相互ルート。\n・VPC Peering では VPN がオンプレ→VPC B へ推移しない (VPC A を経由できない)\n・TGW なら推移ルーティング ○ で全区間疎通\n・将来 VPC 増えても TGW アタッチ追加だけで拡張",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d526", "TGW + VPN + VPC-A/B", cells)


def diag_547():
    """Client VPN for remote access to VPC A (replacing Site-to-Site VPN from office)"""
    cells = [
        title("t", 0, 10, "UDEMY-248 / num=547: 在宅勤務へ Client VPN で VPC 直接アクセス"),
        # Home users
        box("home", 20, 60, 220, 420, "自宅リモートワーカー", fill="#F5F5F5", stroke="#666"),
        aws_icon("u1", 80, 100, "corporate_data_center_2", 40, 40),
        label("u1_l", 50, 150, "Laptop A", 110, bold=False),
        aws_icon("u2", 80, 200, "corporate_data_center_2", 40, 40),
        label("u2_l", 50, 250, "Laptop B", 110, bold=False),
        aws_icon("u3", 80, 300, "corporate_data_center_2", 40, 40),
        label("u3_l", 50, 350, "Laptop C", 110, bold=False),
        # Client VPN
        aws_icon_color("cvpn", 290, 240, "site_to_site_vpn", CLR_VPN, 70, 70),
        label("cvpn_l", 250, 315, "Client VPN", 150),
        label("cvpn_l2", 250, 333, "Endpoint", 150, bold=False, size=10),
        # Office (existing S2S VPN - still there)
        dc_group("office", 20, 500, 220, 70, "オフィス (既存 S2S VPN)"),
        # VPC A
        vpc_group("vpc", 440, 70, 540, 420, "VPC A (内部アプリ)"),
        aws_icon("app1", 510, 120, "ec2", 50, 50),
        label("app1_l", 480, 180, "内部 App EC2", 120),
        aws_icon("app2", 680, 120, "ec2", 50, 50),
        label("app2_l", 650, 180, "Web Front", 120),
        aws_icon("db", 850, 120, "rds", 50, 50, fill="#3B48CC"),
        label("db_l", 820, 180, "RDS", 120),
        aws_icon("sg", 680, 280, "identity_and_access_management", 50, 50),
        label("sg_l", 650, 340, "SG / NACL", 120),
        aws_icon("s2svgw", 500, 380, "vpn_gateway", 50, 50, fill="#7AA116"),
        label("s2svgw_l", 470, 440, "VGW (S2S 用)", 120),
        # Edges
        arrow("e1", "u1", "cvpn", CLR_VPN),
        arrow("e2", "u2", "cvpn", CLR_VPN),
        arrow("e3", "u3", "cvpn", CLR_VPN),
        arrow("e4", "cvpn", "app1", CLR_VPN, w=2),
        arrow("e5", "cvpn", "app2", CLR_VPN, w=2),
        edge("e6", "office", "s2svgw", "#7AA116", dashed=True, w=2, label_text="既存 S2S 継続"),
        # Note
        note("n1", 260, 400, 170, 95,
             "✕ Site-to-Site VPN は\n『オフィス ⇔ AWS』向け。\n自宅ルータ台数を張れず\n端末単位では使えない。",
             fill="#FDEBE9", stroke="#DD344C"),
        note("n2", 20, 520, 960, 60,
             "◎ 正解 B: Client VPN Endpoint を追加配置 → 各従業員端末から TLS 接続 → VPC A へルーティング。SG/EP認可で細粒度制御。",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d547", "Client VPN to VPC A", cells)


def diag_564():
    """Multi-region: Transit VIF + DX Gateway + 2 Region TGWs"""
    cells = [
        title("t", 0, 10, "UDEMY-265 / num=564: マルチリージョン Transit VIF + DX Gateway"),
        # Onprem
        dc_group("dc", 20, 80, 180, 240, "オンプレミス DC"),
        aws_icon("dcs", 60, 120, "corporate_data_center_2", 50, 50),
        label("dcs_l", 30, 180, "社内システム", 120),
        aws_icon("cgw1", 30, 230, "customer_gateway", 40, 40),
        label("cgw1_l", 0, 280, "Loc1", 100, bold=False),
        aws_icon("cgw2", 130, 230, "customer_gateway", 40, 40),
        label("cgw2_l", 100, 280, "Loc2", 100, bold=False),
        # DX x2
        aws_icon_color("dxA", 230, 130, "direct_connect", CLR_DX, 60, 60),
        label("dxA_l", 200, 198, "DX-A", 120),
        aws_icon_color("dxB", 230, 240, "direct_connect", CLR_DX, 60, 60),
        label("dxB_l", 200, 308, "DX-B", 120),
        # DX Gateway
        aws_icon_color("dxgw", 380, 180, "direct_connect", "#6B1B9A", 70, 70),
        label("dxgw_l", 340, 255, "DX Gateway", 150),
        label("dxgw_l2", 340, 273, "(Transit VIF x2)", 150, bold=False, size=10),
        # Region 1 - ap-ne-2
        region_group("r1", 530, 70, 210, 220, "Region: ap-northeast-2"),
        aws_icon_color("tgw1", 580, 120, "transit_gateway", CLR_TGW, 60, 60),
        label("tgw1_l", 550, 188, "TGW ap-ne-2", 130),
        vpc_group("r1v", 550, 220, 170, 60, "VPC (ap-ne-2)"),
        # Region 2 - ap-se-1
        region_group("r2", 770, 70, 210, 220, "Region: ap-southeast-1"),
        aws_icon_color("tgw2", 820, 120, "transit_gateway", CLR_TGW, 60, 60),
        label("tgw2_l", 790, 188, "TGW ap-se-1", 130),
        vpc_group("r2v", 790, 220, 170, 60, "VPC (ap-se-1)"),
        # Edges
        arrow("e1", "cgw1", "dxA", CLR_DX, w=3),
        arrow("e2", "cgw2", "dxB", CLR_DX, w=3),
        arrow("e3", "dxA", "dxgw", CLR_DX, w=3, label_text="Transit VIF-A"),
        arrow("e4", "dxB", "dxgw", CLR_DX, w=3, label_text="Transit VIF-B (HA)"),
        arrow("e5", "dxgw", "tgw1", CLR_TGW, w=3, label_text="Association"),
        arrow("e6", "dxgw", "tgw2", CLR_TGW, w=3, label_text="Association"),
        arrow("e7", "tgw1", "r1v", CLR_TGW),
        arrow("e8", "tgw2", "r2v", CLR_TGW),
        edge("e9", "tgw1", "tgw2", CLR_TGW, dashed=True, w=2, label_text="Inter-Region Peering"),
        # Note
        note("n1", 20, 340, 960, 60,
             "◎ 正解 D: 2 本の DX 上に Transit VIF を作成 → 1 つの DX Gateway に集約 → 両リージョンの TGW を DX GW に Association。\nDX 片方障害時は BGP で自動フェイルオーバー (Active/Active)。"),
        note("n2", 20, 405, 960, 180,
             "Transit VIF + DX GW の強み:\n・1 つの DX GW に 最大 3 リージョンの TGW をアタッチ可能\n・Transit VIF は TGW 専用 (DX Gateway 経由でないと TGW には届かない)\n・Private VIF だと単一 VPC の VGW にしか接続できず、マルチリージョン非対応\n・TGW 間は Inter-Region Peering で相互疎通 → オンプレ ↔ 全リージョン VPC 推移ルーティング\n・BGP / MED / ASN で優先パス制御可能",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d564", "Multi-region Transit VIF", cells)


def diag_569():
    """GWLB inbound inspection with 3rd party security tool"""
    cells = [
        title("t", 0, 10, "UDEMY-270 / num=569: GWLB で インバウンドトラフィックをセキュリティツールへ透過挿入"),
        # Internet
        aws_icon("inet", 30, 170, "internet_gateway", 60, 60, fill="#666"),
        label("inet_l", 0, 238, "インターネット", 120),
        label("inet_l2", 0, 256, "(顧客)", 120, bold=False, size=10),
        # IGW + inbound entry
        aws_icon("igw", 170, 170, "internet_gateway", 60, 60),
        label("igw_l", 140, 238, "IGW", 120),
        # GWLB Endpoint
        aws_icon_color("gwlbe", 310, 170, "endpoint", CLR_EP, 60, 60),
        label("gwlbe_l", 270, 238, "GWLB Endpoint", 140),
        label("gwlbe_l2", 270, 256, "(GWLBE)", 140, bold=False, size=10),
        # Security VPC
        vpc_group("svpc", 460, 60, 300, 400, "Security VPC (検査)"),
        aws_icon("gwlb", 560, 110, "elastic_load_balancing", 60, 60, fill="#8C4FFF"),
        label("gwlb_l", 510, 178, "GWLB (L3 透過)", 170),
        box("az1", 480, 210, 130, 210, "AZ-a", fill="#FFF5EB", stroke="#FF9900"),
        aws_icon("sec1", 510, 240, "ec2", 50, 50, fill="#DD344C"),
        label("sec1_l", 480, 300, "SecTool a", 120, bold=False),
        label("sec1_l2", 480, 318, "(ASG)", 120, bold=False, size=10),
        box("az2", 620, 210, 130, 210, "AZ-b", fill="#FFF5EB", stroke="#FF9900"),
        aws_icon("sec2", 650, 240, "ec2", 50, 50, fill="#DD344C"),
        label("sec2_l", 620, 300, "SecTool b", 120, bold=False),
        label("sec2_l2", 620, 318, "(ASG)", 120, bold=False, size=10),
        # Application VPC
        vpc_group("avpc", 790, 60, 190, 400, "App VPC"),
        aws_icon("app", 850, 150, "ec2", 50, 50),
        label("app_l", 820, 210, "App ASG", 110),
        aws_icon("alb", 850, 300, "elastic_load_balancing", 50, 50, fill="#8C4FFF"),
        label("alb_l", 820, 360, "ALB", 110),
        # Edges
        arrow("e1", "inet", "igw", "#666", w=3),
        arrow("e2", "igw", "gwlbe", CLR_EP, w=3, label_text="0.0.0.0/0"),
        arrow("e3", "gwlbe", "gwlb", "#8C4FFF", w=3, label_text="GENEVE"),
        arrow("e4", "gwlb", "sec1", "#DD344C", w=2),
        arrow("e5", "gwlb", "sec2", "#DD344C", w=2),
        arrow("e6", "sec1", "gwlb", "#DD344C", w=2, dashed=True),
        arrow("e7", "sec2", "gwlb", "#DD344C", w=2, dashed=True),
        arrow("e8", "gwlb", "app", "#8C4FFF", w=3),
        # Note
        note("n1", 20, 470, 960, 115,
             "◎ 正解 AD: 既存の独自セキュリティツールを EC2 ASG でデプロイ + 各 AZ に GWLB。GWLB Endpoint を経由してトラフィックを透過挿入。\n・L4/L7 LB の ALB/NLB では透過挿入できない (L3/L4 透過は GWLB 一択)\n・GENEVE カプセル化で Source IP が保持される → ログの送信元 IP が正しく見える\n・ASG で水平スケール + AZ 分散で HA 構成",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d569", "GWLB Inbound Inspection", cells)


def diag_571():
    """Central DX + TGW share to many accounts"""
    cells = [
        title("t", 0, 10, "UDEMY-272 / num=571: 中央管理 DX + TGW 共有 で数百 VPC のハイブリッド接続"),
        # Onprem
        dc_group("dc", 20, 80, 160, 170, "オンプレ DC"),
        aws_icon("dcs", 60, 110, "corporate_data_center_2", 50, 50),
        label("dcs_l", 30, 170, "既存システム", 120),
        # DX + DX GW (central mgmt)
        box("mgmt", 210, 80, 300, 380, "中央管理アカウント", fill="#EBF1FF", stroke="#3B48CC"),
        aws_icon_color("dx", 240, 120, "direct_connect", CLR_DX, 60, 60),
        label("dx_l", 210, 188, "DX 接続", 120),
        aws_icon_color("dxgw", 240, 220, "direct_connect", "#6B1B9A", 60, 60),
        label("dxgw_l", 210, 288, "DX Gateway", 120),
        label("dxgw_l2", 210, 306, "(Transit VIF)", 120, bold=False, size=10),
        aws_icon_color("tgw", 390, 220, "transit_gateway", CLR_TGW, 60, 60),
        label("tgw_l", 360, 288, "Transit Gateway", 120),
        aws_icon_color("ram", 300, 380, "resource_access_manager", "#3B48CC", 60, 60),
        label("ram_l", 270, 448, "AWS RAM で共有", 140),
        # Member accounts - many VPCs
        box("memb", 560, 80, 420, 480, "メンバーアカウント (将来 数百 VPC)", fill="#F5F5F5", stroke="#666"),
        vpc_group("v1", 580, 130, 180, 120, "App VPC 1"),
        aws_icon("ec1", 640, 170, "ec2", 40, 40),
        vpc_group("v2", 780, 130, 180, 120, "App VPC 2"),
        aws_icon("ec2b", 840, 170, "ec2", 40, 40),
        vpc_group("v3", 580, 280, 180, 120, "App VPC 3"),
        aws_icon("ec3", 640, 320, "ec2", 40, 40),
        vpc_group("v4", 780, 280, 180, 120, "App VPC N"),
        aws_icon("ec4", 840, 320, "ec2", 40, 40),
        label("dots", 580, 420, "... (数百 VPC まで拡張)", 380, bold=False, size=12),
        # Edges
        arrow("e1", "dcs", "dx", CLR_DX, w=3),
        arrow("e2", "dx", "dxgw", CLR_DX, w=3),
        arrow("e3", "dxgw", "tgw", "#6B1B9A", w=3),
        arrow("e4", "tgw", "v1", CLR_TGW, w=2),
        arrow("e5", "tgw", "v2", CLR_TGW, w=2),
        arrow("e6", "tgw", "v3", CLR_TGW, w=2),
        arrow("e7", "tgw", "v4", CLR_TGW, w=2),
        # Note
        note("n1", 20, 475, 500, 110,
             "◎ 正解 DB: 中央管理 TGW を RAM で一般アカウントに共有 → 各 VPC を TGW にアタッチ。\nDX は中央に 1 本で済み、将来 VPC が増えても線形スケール。",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d571", "Central DX + TGW Share", cells)


def diag_609():
    """NLB static IP for firewall allowlist (VPN + DX)"""
    cells = [
        title("t", 0, 10, "UDEMY-310 / num=609: NLB 静的 IP でオンプレ FW 許可リストを維持"),
        # Onprem
        dc_group("dc", 20, 80, 220, 300, "オンプレミス DC"),
        aws_icon("dcs", 70, 110, "corporate_data_center_2", 50, 50),
        label("dcs_l", 40, 170, "クライアント", 120),
        aws_icon_color("fw", 70, 220, "network_firewall", CLR_NFW, 50, 50),
        label("fw_l", 40, 280, "FW (許可リスト)", 120),
        label("fw_l2", 40, 298, "静的 IP x2", 120, bold=False, size=10),
        # VPN & DX connections
        aws_icon_color("vpn", 280, 110, "site_to_site_vpn", CLR_VPN, 50, 50),
        label("vpn_l", 255, 168, "VPN", 100),
        aws_icon_color("dx", 280, 220, "direct_connect", CLR_DX, 50, 50),
        label("dx_l", 255, 278, "DX", 100),
        # VPC
        vpc_group("vpc", 420, 60, 560, 440, "VPC (複数 AZ)"),
        aws_icon("nlb", 480, 120, "elastic_load_balancing", 60, 60, fill="#6B1B9A"),
        label("nlb_l", 440, 188, "NLB (静的 IP)", 140),
        label("nlb_l2", 440, 206, "AZ-a, AZ-b に 1 IP ずつ", 170, bold=False, size=10),
        aws_icon("alb", 680, 120, "elastic_load_balancing", 60, 60, fill="#8C4FFF"),
        label("alb_l", 640, 188, "ALB (L7 ルーティング)", 160),
        # EC2 multi-AZ
        box("az1", 480, 260, 220, 200, "AZ-a", fill="#FFF5EB", stroke="#FF9900"),
        aws_icon("ec1", 560, 300, "ec2", 50, 50),
        label("ec1_l", 530, 360, "EC2 App a", 110),
        box("az2", 720, 260, 220, 200, "AZ-b", fill="#FFF5EB", stroke="#FF9900"),
        aws_icon("ec2b", 800, 300, "ec2", 50, 50),
        label("ec2b_l", 770, 360, "EC2 App b", 110),
        # Edges
        arrow("e1", "dcs", "vpn", CLR_VPN, w=2),
        arrow("e2", "vpn", "nlb", CLR_VPN, w=2),
        edge("e3", "dx", "nlb", CLR_DX, dashed=True, w=2, label_text="別経路"),
        arrow("e4", "nlb", "alb", "#8C4FFF", w=2, label_text="ALB-as-target"),
        arrow("e5", "alb", "ec1", "#8C4FFF"),
        arrow("e6", "alb", "ec2b", "#8C4FFF"),
        # Note
        note("n1", 20, 495, 960, 90,
             "◎ 正解 B: NLB を作成 → NLB を各 AZ で静的 IP 割り当て → ALB を NLB の Target Group にアタッチ (ALB-as-target)。\nオンプレ FW は NLB の静的 IP のみ許可リストに入れればよい (ALB の動的 IP を追いかけ不要)。\nクライアントは NLB 接続先 → NLB → ALB → EC2 にトラフィックが流れる。VPN/DX どちらを使っても到達点は同じ。",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d609", "NLB Static IP for Allowlist", cells)


def diag_620():
    """PrivateLink cross-account endpoint service"""
    cells = [
        title("t", 0, 10, "UDEMY-321 / num=620: PrivateLink Endpoint Service で全事業部門に内部アプリを公開"),
        # Provider (marketing)
        box("prov", 30, 70, 360, 430, "プロバイダー: マーケティング部門", fill="#EBF1FF", stroke="#3B48CC"),
        vpc_group("pvpc", 60, 110, 300, 370, "Provider VPC"),
        aws_icon("app", 150, 150, "ec2", 60, 60),
        label("app_l", 120, 218, "エンゲージメント App", 140),
        aws_icon("nlb", 150, 260, "elastic_load_balancing", 60, 60, fill="#8C4FFF"),
        label("nlb_l", 120, 328, "NLB", 140),
        aws_icon_color("epsvc", 150, 380, "endpoint", CLR_EP, 60, 60),
        label("epsvc_l", 100, 448, "VPC Endpoint Service", 170),
        # Consumers
        box("con", 430, 70, 550, 430, "コンシューマー: 他事業部門 (複数アカウント)", fill="#F5F5F5", stroke="#666"),
        vpc_group("c1", 460, 110, 240, 160, "営業アカウント VPC"),
        aws_icon_color("ep1", 540, 150, "endpoint", CLR_EP, 50, 50),
        label("ep1_l", 510, 210, "Interface EP", 120),
        aws_icon("ec1", 600, 150, "ec2", 50, 50),
        vpc_group("c2", 720, 110, 240, 160, "経理アカウント VPC"),
        aws_icon_color("ep2", 800, 150, "endpoint", CLR_EP, 50, 50),
        label("ep2_l", 770, 210, "Interface EP", 120),
        aws_icon("ec2b", 860, 150, "ec2", 50, 50),
        vpc_group("c3", 460, 290, 240, 160, "サポートアカウント VPC"),
        aws_icon_color("ep3", 540, 330, "endpoint", CLR_EP, 50, 50),
        label("ep3_l", 510, 390, "Interface EP", 120),
        aws_icon("ec3", 600, 330, "ec2", 50, 50),
        vpc_group("c4", 720, 290, 240, 160, "他 VPC"),
        aws_icon_color("ep4", 800, 330, "endpoint", CLR_EP, 50, 50),
        label("ep4_l", 770, 390, "Interface EP", 120),
        aws_icon("ec4", 860, 330, "ec2", 50, 50),
        # Edges
        arrow("e1", "app", "nlb", "#8C4FFF", w=2),
        arrow("e2", "nlb", "epsvc", CLR_EP, w=2),
        arrow("e3", "epsvc", "ep1", CLR_EP, w=2, label_text="PrivateLink"),
        arrow("e4", "epsvc", "ep2", CLR_EP, w=2),
        arrow("e5", "epsvc", "ep3", CLR_EP, w=2),
        arrow("e6", "epsvc", "ep4", CLR_EP, w=2),
        # Note
        note("n1", 20, 510, 960, 75,
             "◎ 正解 C: NLB を プロバイダー VPC に置き、VPC Endpoint Service として公開。各コンシューマーアカウントで Interface VPC Endpoint を作成 → プライベート IP で呼び出し。\nCIDR 重複 OK / 一方向接続 / Allowed Principals で許可アカウント制御。TGW よりスケールが良く、アカウント跨ぎセキュリティも強い。",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d620", "PrivateLink Cross-account", cells)


def diag_629():
    """TGW per-OU + RAM share within OU"""
    cells = [
        title("t", 0, 10, "UDEMY-330 / num=629: OU ごとに TGW を持つ (Dev/Stg/Prod 完全分離)"),
        # Dev OU
        box("dev", 20, 60, 310, 250, "Dev OU (100+ アカウント)", fill="#EBF5E8", stroke="#7AA116"),
        aws_icon("dev_net", 60, 90, "organizations", 50, 50, fill="#7AA116"),
        label("dev_net_l", 30, 150, "Dev Net Acc", 110),
        aws_icon_color("dev_tgw", 180, 90, "transit_gateway", CLR_TGW, 50, 50),
        label("dev_tgw_l", 150, 150, "TGW (Dev)", 110),
        vpc_group("dv1", 40, 180, 120, 100, "Dev VPC A"),
        vpc_group("dv2", 180, 180, 120, 100, "Dev VPC B"),
        arrow("de1", "dev_tgw", "dv1", CLR_TGW, w=2),
        arrow("de2", "dev_tgw", "dv2", CLR_TGW, w=2),
        # Stg OU
        box("stg", 345, 60, 310, 250, "Staging OU (100+ アカウント)", fill="#FFF5EB", stroke="#FF9900"),
        aws_icon("stg_net", 385, 90, "organizations", 50, 50, fill="#FF9900"),
        label("stg_net_l", 355, 150, "Stg Net Acc", 110),
        aws_icon_color("stg_tgw", 505, 90, "transit_gateway", CLR_TGW, 50, 50),
        label("stg_tgw_l", 475, 150, "TGW (Stg)", 110),
        vpc_group("sv1", 365, 180, 120, 100, "Stg VPC A"),
        vpc_group("sv2", 505, 180, 120, 100, "Stg VPC B"),
        arrow("se1", "stg_tgw", "sv1", CLR_TGW, w=2),
        arrow("se2", "stg_tgw", "sv2", CLR_TGW, w=2),
        # Prod OU
        box("prod", 670, 60, 310, 250, "Production OU (100+ アカウント)", fill="#FDEBE9", stroke="#DD344C"),
        aws_icon("prod_net", 710, 90, "organizations", 50, 50, fill="#DD344C"),
        label("prod_net_l", 680, 150, "Prod Net Acc", 110),
        aws_icon_color("prod_tgw", 830, 90, "transit_gateway", CLR_TGW, 50, 50),
        label("prod_tgw_l", 800, 150, "TGW (Prod)", 110),
        vpc_group("pv1", 690, 180, 120, 100, "Prod VPC A"),
        vpc_group("pv2", 830, 180, 120, 100, "Prod VPC B"),
        arrow("pe1", "prod_tgw", "pv1", CLR_TGW, w=2),
        arrow("pe2", "prod_tgw", "pv2", CLR_TGW, w=2),
        # RAM
        aws_icon_color("ram", 460, 380, "resource_access_manager", "#3B48CC", 70, 70),
        label("ram_l", 420, 455, "AWS RAM で OU 内限定共有", 200),
        arrow("r1", "ram", "dev_tgw", "#3B48CC", dashed=True, w=2),
        arrow("r2", "ram", "stg_tgw", "#3B48CC", dashed=True, w=2),
        arrow("r3", "ram", "prod_tgw", "#3B48CC", dashed=True, w=2),
        # Note
        note("n1", 20, 490, 960, 95,
             "◎ 正解 C: OU ごとに Network 管理用アカウントを作成 → OU 専用 TGW を構築 → RAM で OU 内アカウントにだけ共有 → 各 VPC が TGW に Attach。\n・Dev/Stg/Prod が完全ネットワーク分離 (別 TGW なので推移ルーティングも遮断)\n・コンプライアンス要件に適合\n・1 TGW で全 OU を共有すると分離不足",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d629", "TGW per-OU with RAM", cells)


def diag_646():
    """Public VIF + VPN to 3 regional VPCs (DX in one region, VPN to others)"""
    cells = [
        title("t", 0, 10, "UDEMY-347 / num=646: DX + Public VIF 経由で他リージョン VPC にも VPN 延長"),
        # Asia DC
        dc_group("dc", 20, 80, 180, 180, "アジア データセンター"),
        aws_icon("dcs", 60, 110, "corporate_data_center_2", 50, 50),
        label("dcs_l", 30, 170, "設計 / 製造サーバ", 140),
        aws_icon("cgw", 60, 200, "customer_gateway", 40, 40),
        label("cgw_l", 30, 250, "CGW", 100, bold=False),
        # DX
        aws_icon_color("dx", 230, 140, "direct_connect", CLR_DX, 60, 60),
        label("dx_l", 200, 208, "Direct Connect", 120),
        # Public VIF
        aws_icon_color("pvif", 370, 140, "direct_connect", "#F7B500", 60, 60),
        label("pvif_l", 340, 208, "Public VIF", 120),
        label("pvif_l2", 340, 226, "(AWS Public IP)", 120, bold=False, size=10),
        # Asia region (direct)
        region_group("rA", 500, 70, 170, 160, "Region: アジア (近接)"),
        aws_icon_color("vgwA", 540, 110, "vpn_gateway", CLR_TGW, 50, 50),
        label("vgwA_l", 510, 170, "VGW (Asia)", 110),
        vpc_group("vA", 540, 175, 90, 50, "VPC Asia"),
        # Europe (via VPN over Public VIF)
        region_group("rE", 690, 70, 170, 160, "Region: ヨーロッパ"),
        aws_icon_color("vgwE", 730, 110, "vpn_gateway", CLR_TGW, 50, 50),
        label("vgwE_l", 700, 170, "VGW (Europe)", 110),
        vpc_group("vE", 730, 175, 90, 50, "VPC EU"),
        # North America (via VPN over Public VIF)
        region_group("rN", 880, 70, 100, 160, "NA"),
        aws_icon_color("vgwN", 900, 110, "vpn_gateway", CLR_TGW, 50, 50),
        label("vgwN_l", 870, 170, "VGW (NA)", 110),
        vpc_group("vN", 900, 175, 60, 50, "VPC NA"),
        # Edges
        arrow("e1", "cgw", "dx", CLR_DX, w=3),
        arrow("e2", "dx", "pvif", "#F7B500", w=3),
        arrow("e3", "pvif", "vgwA", CLR_DX, w=3, label_text="Private接続"),
        edge("e4", "pvif", "vgwE", CLR_VPN, dashed=True, w=2, label_text="S2S VPN"),
        edge("e5", "pvif", "vgwN", CLR_VPN, dashed=True, w=2, label_text="S2S VPN"),
        # Note
        note("n1", 20, 280, 960, 120,
             "◎ 正解 DA: Public VIF は AWS パブリック IP 空間へのアクセスを可能にする → VPN エンドポイント (VGW) も AWS パブリック IP。\nPublic VIF 経由で他リージョンの VGW と Site-to-Site VPN を張れる → DX の低レイテンシ & プライベート通信を複数リージョンに拡張。\n・近接リージョンは DX 直結 (Private VIF / Transit VIF)\n・遠方リージョンは Public VIF + VPN で帯域とプライベート性の両立\n・代替は Transit VIF + DX Gateway + TGW (より拡張性あり)",
             fill="#EBF5E8", stroke="#7AA116"),
        note("n2", 20, 410, 960, 175,
             "VIF タイプの整理:\n・Private VIF = 単一 VPC の VGW へ直結。シンプルだが 1 VPC のみ\n・Public VIF = AWS パブリック IP 空間へ (S3/DynamoDB/VPN) . 他リージョンへの VPN 延長も可\n・Transit VIF = DX Gateway + TGW 専用。複数 VPC / 複数リージョン / マルチアカウントに最適\n本問では『既存 DX 1 本で 3 リージョン VPC に届かせる最小構成』が要件 → Public VIF + VPN が最安。"),
    ]
    return wrap("d646", "Public VIF + VPN multi-region", cells)


def diag_664():
    """Central Egress VPC + TGW + Network Firewall"""
    cells = [
        title("t", 0, 10, "UDEMY-365 / num=664: 中央 Egress VPC + TGW + Network Firewall"),
        # Spoke accounts
        vpc_group("s1", 30, 80, 170, 110, "Spoke VPC 1"),
        aws_icon("s1e", 80, 110, "ec2", 40, 40),
        label("s1_l", 50, 160, "ワークロード", 110, bold=False),
        vpc_group("s2", 30, 210, 170, 110, "Spoke VPC 2"),
        aws_icon("s2e", 80, 240, "ec2", 40, 40),
        label("s2_l", 50, 290, "ワークロード", 110, bold=False),
        vpc_group("s3", 30, 340, 170, 110, "Spoke VPC N (100+)"),
        aws_icon("s3e", 80, 370, "ec2", 40, 40),
        label("s3_l", 50, 420, "ワークロード", 110, bold=False),
        # TGW
        aws_icon_color("tgw", 280, 240, "transit_gateway", CLR_TGW, 70, 70),
        label("tgw_l", 240, 315, "Transit Gateway", 150),
        # Egress VPC (new)
        vpc_group("egvpc", 430, 70, 370, 430, "Egress VPC (新設)"),
        box("az1", 450, 110, 160, 370, "AZ-a", fill="#FFF5EB", stroke="#FF9900"),
        aws_icon_color("nfw1", 475, 140, "network_firewall", CLR_NFW, 50, 50),
        label("nfw1_l", 445, 200, "NFW EP (a)", 110, bold=False),
        aws_icon_color("ngw1", 475, 260, "nat_gateway", CLR_NAT, 50, 50),
        label("ngw1_l", 445, 320, "NAT GW (a)", 110, bold=False),
        box("az2", 620, 110, 160, 370, "AZ-b", fill="#FFF5EB", stroke="#FF9900"),
        aws_icon_color("nfw2", 645, 140, "network_firewall", CLR_NFW, 50, 50),
        label("nfw2_l", 615, 200, "NFW EP (b)", 110, bold=False),
        aws_icon_color("ngw2", 645, 260, "nat_gateway", CLR_NAT, 50, 50),
        label("ngw2_l", 615, 320, "NAT GW (b)", 110, bold=False),
        # IGW + Internet
        aws_icon("igw", 830, 180, "internet_gateway", 60, 60),
        label("igw_l", 800, 248, "IGW", 120),
        aws_icon("inet", 830, 350, "internet_gateway", 50, 50, fill="#666"),
        label("inet_l", 800, 410, "Internet", 120),
        # Edges
        arrow("e1", "s1", "tgw", CLR_TGW, w=2),
        arrow("e2", "s2", "tgw", CLR_TGW, w=2),
        arrow("e3", "s3", "tgw", CLR_TGW, w=2),
        arrow("e4", "tgw", "nfw1", CLR_NFW, w=2, label_text="0.0.0.0/0"),
        arrow("e5", "tgw", "nfw2", CLR_NFW, w=2),
        arrow("e6", "nfw1", "ngw1", CLR_NAT, w=2),
        arrow("e7", "nfw2", "ngw2", CLR_NAT, w=2),
        arrow("e8", "ngw1", "igw", CLR_NAT, w=2),
        arrow("e9", "ngw2", "igw", CLR_NAT, w=2),
        arrow("e10", "igw", "inet", "#666", w=2),
        # Note
        note("n1", 20, 510, 960, 75,
             "◎ 正解 B: 新しい Egress VPC を作成 → TGW に Attach → 全スポークのデフォルトルートを TGW 経由へ → Egress VPC 内に Network Firewall EP を AZ ごとに配置 → NAT GW → IGW。\n組織全体のアウトバウンドを 1 箇所のルール (FQDN/Suricata) で集中フィルタ。IGW/NAT 数百個 → 2 個に集約。",
             fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d664", "Egress VPC + TGW + NFW", cells)


# =========================================================
# Build all
# =========================================================

BUILDERS = {
    "UDEMY-006": diag_305,
    "UDEMY-021": diag_320,
    "UDEMY-038": diag_337,
    "UDEMY-043": diag_342,
    "UDEMY-057": diag_356,
    "UDEMY-087": diag_386,
    "UDEMY-114": diag_413,
    "UDEMY-128": diag_427,
    "UDEMY-143": diag_442,
    "UDEMY-162": diag_461,
    "UDEMY-167": diag_466,
    "UDEMY-180": diag_479,
    "UDEMY-190": diag_489,
    "UDEMY-203": diag_502,
    "UDEMY-206": diag_505,
    "UDEMY-227": diag_526,
    "UDEMY-248": diag_547,
    "UDEMY-265": diag_564,
    "UDEMY-270": diag_569,
    "UDEMY-272": diag_571,
    "UDEMY-310": diag_609,
    "UDEMY-321": diag_620,
    "UDEMY-330": diag_629,
    "UDEMY-347": diag_646,
    "UDEMY-365": diag_664,
}

for qid, fn in BUILDERS.items():
    path = os.path.join(OUT, f"{qid}.drawio")
    if os.path.exists(path):
        print(f"SKIP (exists): {path}")
        continue
    xml = fn()
    with open(path, "w") as f:
        f.write(xml)
    print(f"WROTE: {path}")

print("Done.")
