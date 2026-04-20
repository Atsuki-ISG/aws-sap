#!/usr/bin/env python3
"""
Build drawio files for selected CloudTech network/hybrid connectivity questions.
Canvas: 1000x600, white background, AWS official icons.
Label y offset: icon.y + 58 minimum.
"""
import os

OUT = "/Users/aki/aws-sap/docs/diagrams/per-question"
os.makedirs(OUT, exist_ok=True)

# ---------- mxgraph helpers ----------
def aws_icon(cid, x, y, resIcon, w=50, h=50, fill="#FFFFFF"):
    return f'''<mxCell id="{cid}" value="" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={fill};strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{resIcon};" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def aws_icon_color(cid, x, y, resIcon, color, w=50, h=50):
    return f'''<mxCell id="{cid}" value="" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={color};strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{resIcon};" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def label(cid, x, y, text, w=140, h=18, bold=True, size=10, color="#232F3E"):
    weight = 1 if bold else 0
    return f'''<mxCell id="{cid}" value="{text}" style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize={size};fontStyle={weight};fontColor={color};" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def title(cid, x, y, text, w=1000, h=28, size=15):
    return f'''<mxCell id="{cid}" value="{text}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize={size};fontStyle=1;fontColor=#232F3E;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def box(cid, x, y, w, h, title_text, fill="#EBF1FF", stroke="#3B48CC"):
    return f'''<mxCell id="{cid}" value="{title_text}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=2;fontSize=11;fontStyle=1;fontColor=#232F3E;verticalAlign=top;spacingTop=6;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def vpc_group(cid, x, y, w, h, name):
    return f'''<mxCell id="{cid}" value="{name}" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;strokeColor=#248814;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def region_group(cid, x, y, w, h, name):
    return f'''<mxCell id="{cid}" value="{name}" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;strokeColor=#147EBA;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=1;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def dc_group(cid, x, y, w, h, name):
    return f'''<mxCell id="{cid}" value="{name}" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_corporate_data_center;strokeColor=#7D7D7D;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def acct_group(cid, x, y, w, h, name):
    return f'''<mxCell id="{cid}" value="{name}" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_account;strokeColor=#CD2264;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

def edge(cid, src, tgt, color="#666666", dashed=False, w=2, label_text=""):
    d = "dashed=1;" if dashed else ""
    val = f' value="{label_text}"' if label_text else ""
    return f'''<mxCell id="{cid}"{val} style="endArrow=classic;startArrow=classic;html=1;strokeColor={color};strokeWidth={w};{d}fontSize=10;fontColor=#232F3E;" edge="1" parent="1" source="{src}" target="{tgt}"><mxGeometry relative="1" as="geometry" /></mxCell>'''

def arrow(cid, src, tgt, color="#666666", dashed=False, w=2, label_text=""):
    d = "dashed=1;" if dashed else ""
    val = f' value="{label_text}"' if label_text else ""
    return f'''<mxCell id="{cid}"{val} style="endArrow=classic;startArrow=none;html=1;strokeColor={color};strokeWidth={w};{d}fontSize=10;fontColor=#232F3E;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="{src}" target="{tgt}"><mxGeometry relative="1" as="geometry" /></mxCell>'''

def note(cid, x, y, w, h, text, fill="#FFFBE6", stroke="#D4AC0D"):
    return f'''<mxCell id="{cid}" value="{text}" style="text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;fontSize=10;fontStyle=0;fontColor=#232F3E;fillColor={fill};strokeColor={stroke};strokeWidth=1;spacing=6;rounded=1;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'''

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

# Colors
CLR_TGW = "#8C4FFF"
CLR_DX  = "#E7157B"
CLR_VPN = "#7AA116"
CLR_NAT = "#ED7100"
CLR_NFW = "#DD344C"
CLR_EP  = "#3B48CC"
CLR_EC2 = "#ED7100"

# =========================================================
# DIAGRAMS
# =========================================================

def diag_2():
    """SAP-2: Client VPN for SSH bastion replacement"""
    cells = [
        title("t", 0, 10, "SAP-2: 踏み台 EC2 廃止 → AWS Client VPN + Session Manager"),
        box("bf", 30, 60, 450, 460, "Before: 踏み台 EC2 (22/tcp 開放)", fill="#FDEBE9", stroke="#DD344C"),
        dc_group("dc_a", 60, 100, 160, 120, "運用チーム PC"),
        aws_icon("op_a", 115, 130, "user", 50, 50),
        label("op_a_l", 90, 188, "SSH クライアント", 130),
        vpc_group("vpc_a", 240, 100, 220, 380, "VPC"),
        aws_icon("bas_a", 310, 140, "ec2", 50, 50),
        label("bas_a_l", 270, 198, "踏み台 EC2 (22)", 140),
        aws_icon("tgt_a", 310, 260, "ec2", 50, 50),
        label("tgt_a_l", 270, 318, "Web/API EC2", 140),
        arrow("ea1", "op_a", "bas_a", "#DD344C", w=2, label_text="22 開放"),
        arrow("ea2", "bas_a", "tgt_a", "#DD344C", w=2),
        note("nb", 55, 380, 400, 95, "問題: ブルートフォース 数千件/日。\n・踏み台 AMI 更新・鍵ローテ運用負荷\n・22/tcp 開放 = 攻撃面大"),

        box("af", 520, 60, 450, 460, "After: Client VPN + Session Manager", fill="#EBF5E8", stroke="#7AA116"),
        aws_icon("op_b", 555, 130, "user", 50, 50),
        label("op_b_l", 530, 188, "運用メンバー", 130),
        aws_icon_color("cvpn", 660, 130, "client_vpn", CLR_VPN, 50, 50),
        label("cvpn_l", 630, 188, "Client VPN EP", 130),
        vpc_group("vpc_b", 760, 100, 200, 380, "VPC"),
        aws_icon("ssm_b", 820, 140, "systems_manager", 50, 50),
        label("ssm_b_l", 780, 198, "SSM Session Mgr", 140),
        aws_icon("tgt_b", 820, 270, "ec2", 50, 50),
        label("tgt_b_l", 780, 328, "Web/API EC2", 140),
        arrow("eb1", "op_b", "cvpn", CLR_VPN, w=2, label_text="MFA"),
        arrow("eb2", "cvpn", "tgt_b", CLR_VPN, w=2),
        arrow("eb3", "ssm_b", "tgt_b", "#3B48CC", w=2, label_text="SSM Agent"),
        note("na", 545, 380, 400, 95, "◎ 正解 D: 踏み台廃止 → Client VPN で閉域に入り、SSM Session Manager で鍵レス・22 閉じ。\n操作ログを S3/CloudWatch に記録可。", fill="#EBF5E8", stroke="#7AA116"),
        note("bot", 30, 530, 940, 50, "ポイント: 22/tcp を公開せず、かつ監査ログを残すには Client VPN (接続) + Session Manager (操作記録) が最適。単なる IP 制限/WAF では監査要件を満たせない。"),
    ]
    return wrap("d_sap2", "SAP-2 Client VPN + SSM", cells)


def diag_15():
    """SAP-15: TGW centralized hybrid, 50Mbps low traffic → VPN + TGW"""
    cells = [
        title("t", 0, 10, "SAP-15: 部門別アカウント + 低帯域 (50Mbps) → TGW + Site-to-Site VPN"),
        dc_group("dc", 30, 80, 180, 200, "オンプレ DC"),
        aws_icon("dcg", 80, 110, "corporate_data_center_2", 50, 50),
        label("dcg_l", 50, 168, "本社 (≤50Mbps)", 140),
        aws_icon_color("cgw", 80, 210, "site_to_site_vpn", CLR_VPN, 50, 50),
        label("cgw_l", 50, 268, "CGW", 140),
        aws_icon_color("vpn", 250, 180, "site_to_site_vpn", CLR_VPN, 50, 50),
        label("vpn_l", 220, 238, "Site-to-Site VPN", 140),
        aws_icon_color("tgw", 430, 180, "transit_gateway", CLR_TGW, 60, 60),
        label("tgw_l", 395, 248, "Transit Gateway", 130),
        label("tgw_l2", 395, 266, "(中央IT / RAM 共有)", 130, bold=False),
        acct_group("a1", 620, 70, 150, 140, "R＆D アカウント"),
        vpc_group("v1", 640, 100, 110, 90, "VPC"),
        aws_icon("e1", 665, 120, "ec2", 40, 40),
        acct_group("a2", 620, 220, 150, 140, "調達 アカウント"),
        vpc_group("v2", 640, 250, 110, 90, "VPC"),
        aws_icon("e2", 665, 270, "ec2", 40, 40),
        acct_group("a3", 620, 370, 150, 140, "営業 アカウント"),
        vpc_group("v3", 640, 400, 110, 90, "VPC"),
        aws_icon("e3", 665, 420, "ec2", 40, 40),
        aws_icon_color("ram", 820, 220, "resource_access_manager", "#C925D1", 50, 50),
        label("ram_l", 790, 278, "AWS RAM 共有", 130),
        arrow("x1", "dcg", "cgw", "#666"),
        arrow("x2", "cgw", "vpn", CLR_VPN, w=3),
        arrow("x3", "vpn", "tgw", CLR_VPN, w=3),
        arrow("x4", "tgw", "v1", CLR_TGW),
        arrow("x5", "tgw", "v2", CLR_TGW),
        arrow("x6", "tgw", "v3", CLR_TGW),
        edge("x7", "tgw", "ram", "#C925D1", dashed=True, label_text="Attach"),
        note("n1", 30, 400, 560, 80, "◎ 正解 B+D: 50Mbps 未満 ＆ 短期増加なし → VPN で十分 (DX は過剰コスト)。\n中央 IT の 1 つの TGW を RAM で部門アカウントに共有し、アタッチのみ各部門が実行。", fill="#EBF5E8", stroke="#7AA116"),
        note("n2", 30, 490, 940, 90, "誤答: \n  ・DX (≥1Gbps) — 要件未達の帯域には過剰投資\n  ・部門ごとに TGW — 経路が増えて管理煩雑\n  ・VPC Peering — 推移不可 / オンプレ接続を各部門で張ると管理負荷"),
    ]
    return wrap("d_sap15", "SAP-15 TGW + VPN", cells)


def diag_21():
    """SAP-21: Central Egress VPC + NAT GW for multi-account outbound"""
    cells = [
        title("t", 0, 10, "SAP-21: マルチアカウント 統合 Egress — Shared Services VPC + NAT GW"),
        acct_group("a1", 30, 70, 180, 150, "Dev アカウント"),
        vpc_group("v1", 50, 100, 140, 110, "VPC"),
        aws_icon("e1", 95, 140, "ec2", 40, 40),
        label("e1l", 60, 188, "Private EC2", 110, bold=False),
        acct_group("a2", 30, 240, 180, 150, "Test アカウント"),
        vpc_group("v2", 50, 270, 140, 110, "VPC"),
        aws_icon("e2", 95, 310, "ec2", 40, 40),
        label("e2l", 60, 358, "Private EC2", 110, bold=False),
        acct_group("a3", 30, 410, 180, 150, "Prod アカウント"),
        vpc_group("v3", 50, 440, 140, 110, "VPC"),
        aws_icon("e3", 95, 480, "ec2", 40, 40),
        label("e3l", 60, 528, "Private EC2", 110, bold=False),
        aws_icon_color("tgw", 280, 280, "transit_gateway", CLR_TGW, 60, 60),
        label("tgw_l", 240, 348, "Transit Gateway", 140),
        label("tgw_l2", 240, 366, "(RAM 共有)", 140, bold=False),
        acct_group("eg", 420, 70, 540, 480, "Shared Services (Egress) アカウント"),
        vpc_group("egv", 450, 110, 480, 420, "Egress VPC (3 AZ)"),
        aws_icon_color("ngw_a", 490, 170, "nat_gateway", CLR_NAT, 50, 50),
        label("ngw_a_l", 460, 228, "NAT GW (AZ-a)", 130),
        aws_icon_color("ngw_b", 680, 170, "nat_gateway", CLR_NAT, 50, 50),
        label("ngw_b_l", 650, 228, "NAT GW (AZ-b)", 130),
        aws_icon_color("ngw_c", 860, 170, "nat_gateway", CLR_NAT, 50, 50),
        label("ngw_c_l", 830, 228, "NAT GW (AZ-c)", 130),
        aws_icon("igw", 680, 350, "internet_gateway", 60, 60),
        label("igw_l", 650, 418, "Internet GW", 130),
        aws_icon("ext", 680, 470, "cloud", 50, 50),
        label("ext_l", 650, 528, "外部 Git Repo", 130, bold=False),
        arrow("r1", "e1", "tgw", CLR_TGW),
        arrow("r2", "e2", "tgw", CLR_TGW),
        arrow("r3", "e3", "tgw", CLR_TGW),
        arrow("r4", "tgw", "ngw_a", CLR_NAT, w=2, label_text="0.0.0.0/0"),
        arrow("r5", "tgw", "ngw_b", CLR_NAT),
        arrow("r6", "tgw", "ngw_c", CLR_NAT),
        arrow("r7", "ngw_b", "igw", CLR_NAT),
        arrow("r8", "igw", "ext", "#666"),
        note("n1", 220, 450, 190, 100, "◎ 正解 A: 3つのアカウント全てを 1 TGW 経由で中央 Egress VPC へルーティング。NAT GW は AZ 毎に 1 つで HA。", fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d_sap21", "SAP-21 Central Egress", cells)


def diag_35():
    """SAP-35: Hybrid connectivity for IoT/SaaS migration — Site-to-Site VPN + TGW"""
    cells = [
        title("t", 0, 10, "SAP-35: 医療機器 IoT → ハイブリッド移行 + Site-to-Site VPN + PrivateLink"),
        dc_group("hosp", 30, 80, 180, 220, "病院 (複数拠点)"),
        aws_icon("dev", 80, 110, "iot_core", 50, 50),
        label("dev_l", 50, 168, "医療機器\n(秒次センサ送信)", 140, bold=False),
        aws_icon_color("cgw", 80, 220, "site_to_site_vpn", CLR_VPN, 50, 50),
        label("cgw_l", 50, 278, "CGW", 140),
        aws_icon_color("vpn", 260, 170, "site_to_site_vpn", CLR_VPN, 50, 50),
        label("vpn_l", 230, 228, "Site-to-Site VPN", 140),
        aws_icon_color("tgw", 420, 170, "transit_gateway", CLR_TGW, 60, 60),
        label("tgw_l", 385, 238, "Transit Gateway", 130),
        vpc_group("saas", 580, 70, 180, 140, "SaaS ベンダ VPC"),
        aws_icon("saas_app", 620, 100, "ec2", 40, 40),
        label("saas_l", 590, 148, "Java App", 130, bold=False),
        vpc_group("own", 580, 230, 180, 140, "自社 VPC"),
        aws_icon_color("nlb", 620, 260, "network_load_balancer", "#8C4FFF", 40, 40),
        label("nlb_l", 590, 308, "NLB", 130, bold=False),
        aws_icon_color("pls", 820, 240, "endpoint", CLR_EP, 50, 50),
        label("pls_l", 790, 298, "PrivateLink EP", 130),
        vpc_group("cons", 820, 370, 150, 140, "利用者 VPC"),
        aws_icon("cons_app", 860, 400, "ec2", 40, 40),
        label("cons_l", 830, 448, "アプリ", 130, bold=False),
        arrow("e1", "dev", "cgw"),
        arrow("e2", "cgw", "vpn", CLR_VPN, w=3),
        arrow("e3", "vpn", "tgw", CLR_VPN, w=3),
        arrow("e4", "tgw", "saas", CLR_TGW),
        arrow("e5", "tgw", "own", CLR_TGW),
        arrow("e6", "nlb", "pls", CLR_EP, w=2, label_text="Endpoint Service"),
        arrow("e7", "cons_app", "pls", CLR_EP),
        note("n1", 30, 370, 560, 90, "◎ 正解 A: TGW + VPN で病院⇄AWS を閉域化。\n・SaaS 側は NLB + PrivateLink (Endpoint Service) で提供\n・オンプレ IoT → AWS 上 SaaS へ「通信方向限定」可"),
        note("n2", 30, 470, 940, 110, "誤答パターン:\n ・VPC Peering — 推移不可、拠点数増加で複雑化\n ・Direct Connect 単独 — 医療機器側帯域は 50Mbps 程度で過剰\n ・PrivateLink だけ — オンプレ接続がない", fill="#FDEBE9", stroke="#DD344C"),
    ]
    return wrap("d_sap35", "SAP-35 Hybrid + PrivateLink", cells)


def diag_48():
    """SAP-48: Cloud WAN for global, policy-driven multi-account networking"""
    cells = [
        title("t", 0, 10, "SAP-48: 数千アカウント / 部門別経路 → AWS Cloud WAN"),
        region_group("r1", 30, 60, 290, 260, "Region: us-east-1"),
        vpc_group("v1a", 50, 100, 110, 80, "Brand A VPC"),
        aws_icon("v1a_e", 80, 120, "ec2", 40, 40),
        vpc_group("v1b", 180, 100, 120, 80, "Brand B VPC"),
        aws_icon("v1b_e", 210, 120, "ec2", 40, 40),
        vpc_group("v1c", 50, 200, 250, 100, "共通 Services VPC"),
        aws_icon("v1c_e", 150, 230, "application_load_balancer", 40, 40),
        region_group("r2", 340, 60, 290, 260, "Region: ap-northeast-1"),
        vpc_group("v2a", 360, 100, 110, 80, "Brand A VPC"),
        aws_icon("v2a_e", 390, 120, "ec2", 40, 40),
        vpc_group("v2b", 490, 100, 120, 80, "Brand B VPC"),
        aws_icon("v2b_e", 520, 120, "ec2", 40, 40),
        vpc_group("v2c", 360, 200, 250, 100, "共通 Services VPC"),
        aws_icon("v2c_e", 460, 230, "application_load_balancer", 40, 40),
        aws_icon_color("cwan", 740, 150, "transit_gateway", "#8C4FFF", 70, 70),
        label("cwan_l", 700, 228, "AWS Cloud WAN", 150),
        label("cwan_l2", 700, 246, "Core Network Policy", 150, bold=False),
        box("seg", 700, 290, 280, 110, "セグメント (YAML ポリシー)", fill="#FFF5EB", stroke="#ED7100"),
        label("seg1", 720, 310, "• Brand A セグメント", 240, bold=False),
        label("seg2", 720, 330, "• Brand B セグメント", 240, bold=False),
        label("seg3", 720, 350, "• 共通 Services セグメント", 240, bold=False),
        label("seg4", 720, 370, "(セグメント間分離 + 共通への allow)", 240, bold=False),
        arrow("a1", "v1a", "cwan", "#8C4FFF"),
        arrow("a2", "v1b", "cwan", "#8C4FFF"),
        arrow("a3", "v1c", "cwan", "#8C4FFF"),
        arrow("a4", "v2a", "cwan", "#8C4FFF"),
        arrow("a5", "v2b", "cwan", "#8C4FFF"),
        arrow("a6", "v2c", "cwan", "#8C4FFF"),
        note("n1", 30, 410, 650, 80, "◎ 正解 C: Cloud WAN = AWS マネージドのグローバルネットワーク。\n・セグメント単位でトラフィックを論理分離、ポリシー (YAML) でルート制御\n・数千 VPC / 複数リージョン を単一ネットワークで可視化", fill="#EBF5E8", stroke="#7AA116"),
        note("n2", 30, 500, 940, 85, "TGW との差:\n ・TGW = リージョン単位、Attach/RT を手動運用\n ・Cloud WAN = グローバル + 宣言的ポリシー、セグメントを中央で管理\n → 事業部/ブランド が数千アカウントに広がる SaaS で運用負荷を最小化"),
    ]
    return wrap("d_sap48", "SAP-48 Cloud WAN", cells)


def diag_61():
    """SAP-61: Central Egress + Hub-and-Spoke TGW + Network Firewall"""
    cells = [
        title("t", 0, 10, "SAP-61: ハブ＆スポーク TGW + 中央 Egress VPC + Network Firewall"),
        acct_group("a1", 30, 70, 170, 130, "Service Acct 1"),
        vpc_group("v1", 50, 100, 130, 90, "Spoke VPC"),
        aws_icon("e1", 90, 120, "ec2", 40, 40),
        acct_group("a2", 30, 220, 170, 130, "Service Acct 2"),
        vpc_group("v2", 50, 250, 130, 90, "Spoke VPC"),
        aws_icon("e2", 90, 270, "ec2", 40, 40),
        acct_group("a3", 30, 370, 170, 130, "Service Acct 3"),
        vpc_group("v3", 50, 400, 130, 90, "Spoke VPC"),
        aws_icon("e3", 90, 420, "ec2", 40, 40),
        aws_icon_color("tgw", 260, 270, "transit_gateway", CLR_TGW, 60, 60),
        label("tgw_l", 220, 338, "Transit Gateway", 140),
        acct_group("egac", 400, 70, 570, 450, "Networking (Egress) アカウント"),
        vpc_group("egv", 430, 110, 510, 390, "Inspection / Egress VPC"),
        aws_icon_color("nfw", 490, 170, "network_firewall", CLR_NFW, 60, 60),
        label("nfw_l", 450, 238, "Network Firewall", 140),
        label("nfw_l2", 450, 256, "(ドメイン/URL 検査)", 140, bold=False),
        aws_icon_color("ngw1", 680, 170, "nat_gateway", CLR_NAT, 50, 50),
        label("ngw1_l", 650, 228, "NAT GW", 130),
        aws_icon("igw", 820, 170, "internet_gateway", 60, 60),
        label("igw_l", 790, 238, "Internet GW", 130),
        aws_icon("ext", 820, 330, "cloud", 50, 50),
        label("ext_l", 790, 388, "外部 API", 130, bold=False),
        arrow("f1", "v1", "tgw", CLR_TGW),
        arrow("f2", "v2", "tgw", CLR_TGW),
        arrow("f3", "v3", "tgw", CLR_TGW),
        arrow("f4", "tgw", "nfw", CLR_NFW, w=3, label_text="0.0.0.0/0"),
        arrow("f5", "nfw", "ngw1", CLR_NAT, w=2),
        arrow("f6", "ngw1", "igw", CLR_NAT),
        arrow("f7", "igw", "ext", "#666"),
        note("n1", 30, 510, 940, 70, "◎ 正解 C: 全 Spoke を TGW で集約 → Inspection VPC の NFW を通して NAT GW + IGW へ。ドメインベースのホワイトリストを 中央で一元管理。\n誤答: 各 VPC に NFW = コスト N 倍 / Proxy 自前 = 運用負荷", fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d_sap61", "SAP-61 Central Inspection Egress", cells)


def diag_66():
    """SAP-66: Client VPN only, closed network (no Internet)"""
    cells = [
        title("t", 0, 10, "SAP-66: 紙バックアップ有り / 閉域のみ → AWS Client VPN + S3 Gateway EP"),
        dc_group("dc", 30, 90, 180, 200, "オンプレ (研究員 PC)"),
        aws_icon("usr", 85, 120, "user", 50, 50),
        label("usr_l", 55, 178, "研究員", 140),
        aws_icon_color("cvpn", 280, 170, "client_vpn", CLR_VPN, 60, 60),
        label("cvpn_l", 250, 238, "Client VPN EP", 120),
        label("cvpn_l2", 250, 256, "(AD 認証)", 120, bold=False),
        vpc_group("vpc", 450, 80, 320, 430, "VPC (閉域)"),
        aws_icon_color("gep", 510, 140, "endpoint", CLR_EP, 60, 60),
        label("gep_l", 470, 208, "S3 Gateway EP", 140),
        aws_icon("s3", 670, 140, "simple_storage_service", 60, 60),
        label("s3_l", 640, 208, "S3 (試験報告書)", 140),
        aws_icon("elb", 510, 300, "application_load_balancer", 50, 50),
        label("elb_l", 480, 358, "内部 ALB", 120),
        aws_icon("ec2", 670, 300, "ec2", 50, 50),
        label("ec2_l", 640, 358, "検索アプリ", 120),
        arrow("r1", "usr", "cvpn", CLR_VPN, w=3, label_text="VPN"),
        arrow("r2", "cvpn", "elb", CLR_VPN, w=2),
        arrow("r3", "elb", "ec2", "#666"),
        arrow("r4", "ec2", "gep", CLR_EP, w=2),
        arrow("r5", "gep", "s3", CLR_EP, w=2),
        note("n1", 800, 110, 170, 200, "◎ 正解 A:\nインターネット非公開 × Client VPN で接続 × S3 Gateway EP で閉域保持。\n・高可用性不要 (紙バックアップ有り)\n・コスト最小構成", fill="#EBF5E8", stroke="#7AA116"),
        note("n2", 30, 520, 940, 65, "誤答: ・CloudFront + S3 — 公開不可\n・NAT GW + Internet — 不要 (閉域要件)\n・Interface EP (KMS/SSM 等) が必要ならここに追加可能"),
    ]
    return wrap("d_sap66", "SAP-66 Client VPN + S3 GEP", cells)


def diag_70():
    """SAP-70: TGW intra-region, high throughput → VPC Peering for new Spoke"""
    cells = [
        title("t", 0, 10, "SAP-70: TGW ハブ＆スポーク 環境 + 高スループット要件 → VPC Peering 追加"),
        aws_icon_color("tgw", 450, 260, "transit_gateway", CLR_TGW, 70, 70),
        label("tgw_l", 410, 338, "Transit Gateway", 150),
        vpc_group("v1", 30, 80, 180, 130, "既存 Spoke VPC A"),
        aws_icon("e1", 90, 110, "ec2", 40, 40),
        label("e1l", 60, 158, "視聴ログ", 120, bold=False),
        vpc_group("v2", 30, 230, 180, 130, "既存 Spoke VPC B"),
        aws_icon("e2", 90, 260, "ec2", 40, 40),
        label("e2l", 60, 308, "メタデータ", 120, bold=False),
        vpc_group("v3", 30, 380, 180, 130, "既存 Spoke VPC C"),
        aws_icon("e3", 90, 410, "ec2", 40, 40),
        label("e3l", 60, 458, "視聴ログ", 120, bold=False),
        vpc_group("vnew", 720, 150, 240, 340, "新 レコメンド VPC"),
        aws_icon("enew", 820, 200, "ec2", 50, 50),
        label("enew_l", 790, 258, "リアルタイム\n推奨エンジン", 130, bold=False),
        aws_icon("ddb", 820, 340, "dynamodb", 50, 50),
        label("ddb_l", 790, 398, "DynamoDB", 130, bold=False),
        arrow("ee1", "v1", "tgw", CLR_TGW),
        arrow("ee2", "v2", "tgw", CLR_TGW),
        arrow("ee3", "v3", "tgw", CLR_TGW),
        arrow("ee4", "tgw", "vnew", CLR_TGW, w=2, label_text="従来経路"),
        edge("pee1", "v1", "vnew", "#248814", w=3, label_text="VPC Peering (高帯域)"),
        edge("pee2", "v3", "vnew", "#248814", w=3, label_text="VPC Peering (高帯域)"),
        note("n1", 30, 520, 940, 65, "◎ 正解 B: 大量ログ転送は TGW ($0.02/GB の処理料) を通らない VPC Peering がコスト・帯域面で有利。\nAWS Private バックボーン (無料・同 AZ 内) 経由で同リージョン広帯域通信 OK。", fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d_sap70", "SAP-70 TGW + VPC Peering", cells)


def diag_73():
    """SAP-73: Fixed public IP outbound — EIP on NAT GW for payment API"""
    cells = [
        title("t", 0, 10, "SAP-73: 決済 API へ固定 IP で発信 → NAT GW + EIP + AWS Global Accelerator"),
        vpc_group("vpc", 60, 90, 520, 420, "VPC"),
        box("prv", 90, 130, 220, 350, "Private Subnet", fill="#E9F3E6", stroke="#248814"),
        aws_icon("app", 140, 180, "ec2", 50, 50),
        label("app_l", 110, 238, "Web App", 120),
        aws_icon("app2", 140, 310, "ec2", 50, 50),
        label("app2_l", 110, 368, "Web App", 120),
        box("pub", 340, 130, 230, 350, "Public Subnet", fill="#FFF5EB", stroke="#ED7100"),
        aws_icon_color("ngw", 390, 180, "nat_gateway", CLR_NAT, 50, 50),
        label("ngw_l", 360, 238, "NAT GW + EIP", 120),
        label("ngw_l2", 360, 256, "(固定IP)", 120, bold=False),
        aws_icon("igw", 390, 310, "internet_gateway", 50, 50),
        label("igw_l", 360, 368, "Internet GW", 120),
        aws_icon_color("ga", 660, 150, "global_accelerator", "#8C4FFF", 50, 50),
        label("ga_l", 630, 208, "Global Accelerator", 140),
        label("ga_l2", 630, 226, "(Anycast 固定 IP)", 140, bold=False),
        aws_icon("payapi", 660, 350, "cloud", 50, 50),
        label("payapi_l", 630, 408, "決済 API\n(IP 許可リスト)", 140, bold=False),
        arrow("e1", "app", "ngw", CLR_NAT),
        arrow("e2", "app2", "ngw", CLR_NAT),
        arrow("e3", "ngw", "igw", CLR_NAT),
        arrow("e4", "igw", "payapi", "#666", w=2, label_text="EIP 固定発信"),
        arrow("e5", "app", "ga", "#8C4FFF", dashed=True, label_text="Inbound (任意)"),
        note("n1", 30, 520, 940, 65, "◎ 正解 A: 送信元 IP 固定 = NAT GW に Elastic IP を付与 (or Global Accelerator で固定 Anycast IP)。\nInstance 個別 EIP は Scale時に増加 → 許可リスト追加運用が必要で NG。", fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d_sap73", "SAP-73 Fixed IP via NAT GW", cells)


def diag_78():
    """SAP-78: TGW failure — redundant TGW + BFD + BGP over DX"""
    cells = [
        title("t", 0, 10, "SAP-78: TGW 障害対策 → 冗長 TGW / DX 冗長 / BFD / BGP"),
        dc_group("dc", 30, 80, 180, 220, "本社 DC"),
        aws_icon("dcg", 80, 130, "corporate_data_center_2", 50, 50),
        label("dcg_l", 50, 188, "本社", 140),
        aws_icon_color("dx1", 280, 100, "direct_connect", CLR_DX, 50, 50),
        label("dx1_l", 250, 158, "DX 接続 1", 130),
        aws_icon_color("dx2", 280, 220, "direct_connect", CLR_DX, 50, 50),
        label("dx2_l", 250, 278, "DX 接続 2 (冗長)", 130),
        aws_icon_color("dxgw", 440, 160, "direct_connect", CLR_DX, 50, 50),
        label("dxgw_l", 410, 218, "DX Gateway", 130),
        aws_icon_color("tgw1", 610, 100, "transit_gateway", CLR_TGW, 50, 50),
        label("tgw1_l", 580, 158, "TGW-1 (Shared)", 130),
        aws_icon_color("tgw2", 610, 220, "transit_gateway", CLR_TGW, 50, 50),
        label("tgw2_l", 580, 278, "TGW-2 (Backup)", 130),
        acct_group("accs", 780, 70, 190, 300, "メンバ アカウント群"),
        vpc_group("v1", 800, 100, 150, 70, "VPC 1"),
        vpc_group("v2", 800, 190, 150, 70, "VPC 2"),
        vpc_group("v3", 800, 280, 150, 70, "VPC 3"),
        arrow("e1", "dcg", "dx1"),
        arrow("e2", "dcg", "dx2"),
        arrow("e3", "dx1", "dxgw", CLR_DX, w=2, label_text="BGP + BFD"),
        arrow("e4", "dx2", "dxgw", CLR_DX, w=2),
        arrow("e5", "dxgw", "tgw1", CLR_TGW, w=2),
        arrow("e6", "dxgw", "tgw2", CLR_TGW, w=2, dashed=True, label_text="フェイルオーバ"),
        arrow("e7", "tgw1", "v1", CLR_TGW),
        arrow("e8", "tgw1", "v2", CLR_TGW),
        arrow("e9", "tgw1", "v3", CLR_TGW),
        note("n1", 30, 380, 940, 90, "◎ 正解 D: DX を 2 本 + 2 つの TGW (Active/Standby) を DX GW に関連付け。\n・BFD (Bidirectional Forwarding Detection) + BGP AS-Path 調整で高速フェイルオーバ\n・TGW 障害時は 2 本目の TGW 経由に自動切替", fill="#EBF5E8", stroke="#7AA116"),
        note("n2", 30, 480, 940, 100, "誤答: \n ・単一 TGW + 単一 DX — 単一障害点\n ・VPN のみ — 帯域/レイテンシ不足\n ・1 DX に BFD のみ — 物理回線障害は救えない"),
    ]
    return wrap("d_sap78", "SAP-78 TGW HA + DX BFD", cells)


def diag_106():
    """SAP-106: Multi-region inter-region TGW peering, closed network"""
    cells = [
        title("t", 0, 10, "SAP-106: マルチリージョン 閉域同期 → Inter-Region TGW Peering"),
        region_group("r1", 30, 60, 300, 300, "us-east-1 (本社)"),
        vpc_group("r1v1", 60, 100, 240, 80, "研究 VPC (米国)"),
        aws_icon("r1e", 120, 120, "ec2", 40, 40),
        label("r1e_l", 90, 168, "解析基盤", 120, bold=False),
        vpc_group("r1v2", 60, 200, 240, 80, "データ VPC"),
        aws_icon("r1s", 120, 220, "simple_storage_service", 40, 40),
        label("r1s_l", 90, 268, "機密データ", 120, bold=False),
        aws_icon_color("r1tgw", 150, 290, "transit_gateway", CLR_TGW, 50, 50),
        label("r1tgw_l", 120, 348, "TGW (us-east-1)", 120),
        region_group("r2", 360, 60, 300, 300, "eu-west-1 (研究所)"),
        vpc_group("r2v1", 390, 100, 240, 80, "研究 VPC (EU)"),
        aws_icon("r2e", 450, 120, "ec2", 40, 40),
        label("r2e_l", 420, 168, "分析", 120, bold=False),
        vpc_group("r2v2", 390, 200, 240, 80, "データ VPC"),
        aws_icon("r2s", 450, 220, "simple_storage_service", 40, 40),
        label("r2s_l", 420, 268, "機密データ", 120, bold=False),
        aws_icon_color("r2tgw", 480, 290, "transit_gateway", CLR_TGW, 50, 50),
        label("r2tgw_l", 450, 348, "TGW (eu-west-1)", 120),
        region_group("r3", 690, 60, 280, 300, "ap-northeast-1 (研究所)"),
        vpc_group("r3v1", 720, 100, 230, 80, "研究 VPC (Asia)"),
        aws_icon("r3e", 780, 120, "ec2", 40, 40),
        label("r3e_l", 750, 168, "分析", 120, bold=False),
        vpc_group("r3v2", 720, 200, 230, 80, "データ VPC"),
        aws_icon("r3s", 780, 220, "simple_storage_service", 40, 40),
        label("r3s_l", 750, 268, "機密データ", 120, bold=False),
        aws_icon_color("r3tgw", 810, 290, "transit_gateway", CLR_TGW, 50, 50),
        label("r3tgw_l", 780, 348, "TGW (Tokyo)", 120),
        edge("pe1", "r1tgw", "r2tgw", CLR_TGW, w=3, label_text="TGW Peering"),
        edge("pe2", "r2tgw", "r3tgw", CLR_TGW, w=3, label_text="TGW Peering"),
        edge("pe3", "r1tgw", "r3tgw", CLR_TGW, w=3, dashed=True, label_text="(フルメッシュ)"),
        note("n1", 30, 400, 940, 80, "◎ 正解 A: TGW Inter-Region Peering。\n・AWS バックボーン経由 = パブリック網を一切通過しない\n・暗号化: AES-256 GCM 自動\n・各リージョン TGW に S3 へ PrivateLink 経由 = 閉域同期 OK", fill="#EBF5E8", stroke="#7AA116"),
        note("n2", 30, 490, 940, 95, "誤答:\n ・S3 クロスリージョンレプリケーション (default) — パブリックエンドポイント経由\n ・Site-to-Site VPN — 帯域不足・管理コスト\n ・VPC Peering — 多対多の爆発・グローバル WAN 要件未達"),
    ]
    return wrap("d_sap106", "SAP-106 Multi-Region TGW Peering", cells)


def diag_108():
    """SAP-108: Private subnet + Gateway EP for S3 + NAT GW cost optimization"""
    cells = [
        title("t", 0, 10, "SAP-108: NAT GW 経由 S3 コスト最適化 → S3 Gateway Endpoint"),
        box("bf", 30, 50, 450, 500, "Before: S3 を NAT GW 経由 (高コスト)", fill="#FDEBE9", stroke="#DD344C"),
        vpc_group("vb", 60, 90, 390, 330, "VPC (2 AZ)"),
        box("pubb", 80, 130, 180, 130, "Public Subnet", fill="#FFF5EB", stroke="#ED7100"),
        aws_icon_color("ngwb", 130, 160, "nat_gateway", CLR_NAT, 50, 50),
        label("ngwb_l", 100, 218, "NAT GW", 130),
        aws_icon("igwb", 300, 160, "internet_gateway", 50, 50),
        label("igwb_l", 270, 218, "IGW", 130),
        box("prvb", 80, 280, 360, 130, "Private Subnet"),
        aws_icon("ecb", 140, 310, "ec2", 50, 50),
        label("ecb_l", 110, 368, "分析 EC2", 130),
        aws_icon("s3b", 370, 310, "simple_storage_service", 50, 50),
        label("s3b_l", 340, 368, "Amazon S3", 130),
        arrow("eb1", "ecb", "ngwb", CLR_NAT, label_text="100GB+/日"),
        arrow("eb2", "ngwb", "igwb", CLR_NAT),
        arrow("eb3", "igwb", "s3b", "#666"),
        note("nb1", 55, 430, 400, 100, "問題:\n・NAT GW: $0.045/GB 処理料 + EIP 転送料\n・S3 は同リージョンでも Internet 経由で課金"),
        box("af", 520, 50, 450, 500, "After: S3 Gateway EP (無料)", fill="#EBF5E8", stroke="#7AA116"),
        vpc_group("va", 550, 90, 390, 330, "VPC (2 AZ)"),
        box("pubaf", 570, 130, 140, 100, "Public Subnet", fill="#FFF5EB", stroke="#ED7100"),
        aws_icon_color("ngwa", 605, 150, "nat_gateway", CLR_NAT, 50, 50),
        label("ngwa_l", 575, 208, "NAT GW", 130),
        box("prva", 570, 250, 360, 160, "Private Subnet"),
        aws_icon("eca", 620, 290, "ec2", 50, 50),
        label("eca_l", 590, 348, "分析 EC2", 130),
        aws_icon_color("geps3", 770, 290, "endpoint", CLR_EP, 50, 50),
        label("geps3_l", 740, 348, "S3 Gateway EP", 140),
        aws_icon("s3a", 870, 290, "simple_storage_service", 50, 50),
        label("s3a_l", 840, 348, "Amazon S3", 130),
        arrow("ea1", "eca", "geps3", CLR_EP, w=2),
        arrow("ea2", "geps3", "s3a", CLR_EP, w=2),
        note("na1", 545, 430, 400, 100, "◎ 正解 A: S3 Gateway Endpoint を作成、RT にプレフィックスリスト追加。\n・EP 利用料 0 円 / データ転送料 0 円\n・NAT GW は引き続き他の外部向けで残す"),
        note("bot", 30, 560, 940, 35, "Gateway EP は S3 と DynamoDB のみ無料。他の AWS サービスは Interface EP (PrivateLink, 有料)。"),
    ]
    return wrap("d_sap108", "SAP-108 S3 Gateway EP", cells)


def diag_112():
    """SAP-112: Lambda in VPC + NAT GW EIP / or Interface Endpoint for fixed source IP"""
    cells = [
        title("t", 0, 10, "SAP-112: Lambda 外部 API 呼び出し + 固定 IP → VPC 配置 + NAT GW + EIP"),
        aws_icon("sched", 60, 110, "eventbridge", 50, 50),
        label("sched_l", 30, 168, "EventBridge\n(10分間隔)", 120, bold=False),
        vpc_group("vpc", 200, 70, 540, 400, "VPC"),
        box("prv", 230, 110, 220, 330, "Private Subnet", fill="#E9F3E6", stroke="#248814"),
        aws_icon("lmb", 290, 150, "lambda", 50, 50),
        label("lmb_l", 260, 208, "Lambda\n(VPC 接続)", 130, bold=False),
        box("pub", 470, 110, 250, 330, "Public Subnet", fill="#FFF5EB", stroke="#ED7100"),
        aws_icon_color("ngw", 520, 150, "nat_gateway", CLR_NAT, 50, 50),
        label("ngw_l", 490, 208, "NAT GW", 130),
        label("ngw_l2", 490, 226, "+ EIP (固定)", 130, bold=False),
        aws_icon("igw", 630, 150, "internet_gateway", 50, 50),
        label("igw_l", 600, 208, "IGW", 130),
        aws_icon("ext", 820, 200, "cloud", 60, 60),
        label("ext_l", 790, 268, "外部 API\n(許可リスト)", 130, bold=False),
        arrow("e1", "sched", "lmb"),
        arrow("e2", "lmb", "ngw", CLR_NAT),
        arrow("e3", "ngw", "igw", CLR_NAT, label_text="固定 EIP"),
        arrow("e4", "igw", "ext", "#666"),
        note("n1", 30, 330, 160, 140, "◎ 正解 A+B:\n1) Lambda を VPC に配置\n2) プライベートサブネットから NAT GW (EIP) 経由で発信\n→ 送信元は常に EIP", fill="#EBF5E8", stroke="#7AA116"),
        note("n2", 30, 490, 940, 90, "誤答: \n・Lambda をパブリックサブネットに置く — Lambda は ENI 経由、パブリック割当は自動されず接続不可\n・API Gateway を挟む — 呼び出し元は Lambda のまま、IP は固定されない\n・CloudFront — 外向き通信には使わない"),
    ]
    return wrap("d_sap112", "SAP-112 Lambda + NAT GW EIP", cells)


def diag_121():
    """SAP-121: Client VPN to TGW for distributed workforce"""
    cells = [
        title("t", 0, 10, "SAP-121: 在宅勤務 VPN → AWS Client VPN + TGW + 既存 Site-to-Site VPN"),
        aws_icon("h1", 30, 90, "user", 50, 50),
        label("h1_l", 0, 148, "在宅 社員 A", 110),
        aws_icon("h2", 30, 180, "user", 50, 50),
        label("h2_l", 0, 238, "在宅 社員 B", 110),
        aws_icon("h3", 30, 270, "user", 50, 50),
        label("h3_l", 0, 328, "在宅 社員 C", 110),
        aws_icon_color("cvpn", 180, 160, "client_vpn", CLR_VPN, 60, 60),
        label("cvpn_l", 150, 228, "Client VPN EP", 120),
        label("cvpn_l2", 150, 246, "(AD/SAML 認証)", 120, bold=False),
        aws_icon_color("tgw", 380, 160, "transit_gateway", CLR_TGW, 60, 60),
        label("tgw_l", 345, 228, "Transit Gateway", 130),
        acct_group("accs", 570, 70, 390, 280, "社内 VPC 群 (複数アカウント)"),
        vpc_group("v1", 590, 100, 170, 90, "Repo VPC"),
        aws_icon("v1e", 630, 120, "ec2", 40, 40),
        label("v1el", 590, 168, "Git Repo", 130, bold=False),
        vpc_group("v2", 780, 100, 160, 90, "CI/CD VPC"),
        aws_icon("v2e", 820, 120, "ec2", 40, 40),
        label("v2el", 770, 168, "Jenkins", 130, bold=False),
        vpc_group("v3", 590, 220, 170, 90, "AD VPC"),
        aws_icon("v3e", 630, 240, "directory_service", 40, 40),
        label("v3el", 590, 288, "Managed AD", 130, bold=False),
        vpc_group("v4", 780, 220, 160, 90, "App VPC"),
        aws_icon("v4e", 820, 240, "ec2", 40, 40),
        label("v4el", 770, 288, "社内アプリ", 130, bold=False),
        dc_group("hq", 30, 390, 200, 140, "本社 LAN"),
        aws_icon_color("cgw", 80, 420, "site_to_site_vpn", CLR_VPN, 50, 50),
        label("cgw_l", 50, 478, "CGW (S2S VPN)", 140),
        arrow("a1", "h1", "cvpn", CLR_VPN),
        arrow("a2", "h2", "cvpn", CLR_VPN),
        arrow("a3", "h3", "cvpn", CLR_VPN),
        arrow("a4", "cvpn", "tgw", CLR_VPN, w=3),
        arrow("a5", "cgw", "tgw", CLR_VPN, w=2, label_text="既存 S2S VPN"),
        arrow("a6", "tgw", "v1", CLR_TGW),
        arrow("a7", "tgw", "v2", CLR_TGW),
        arrow("a8", "tgw", "v3", CLR_TGW),
        arrow("a9", "tgw", "v4", CLR_TGW),
        note("n1", 280, 370, 670, 90, "◎ 正解 A: Client VPN エンドポイントを TGW にアタッチ。\n・在宅メンバは OpenVPN クライアントで接続 → TGW 経由で全 VPC へ到達\n・AD と SAML 認証連携で個人単位の MFA/監査可能", fill="#EBF5E8", stroke="#7AA116"),
        note("n2", 280, 470, 670, 75, "誤答: \n ・個別アカウントで Client VPN 立上 — 管理 N 倍\n ・本社 VPN に一旦戻す — レイテンシ大・本社回線が SPOF"),
    ]
    return wrap("d_sap121", "SAP-121 Client VPN + TGW", cells)


def diag_139():
    """SAP-139: Same-region SaaS API without internet — PrivateLink"""
    cells = [
        title("t", 0, 10, "SAP-139: 同一リージョン SaaS API へ閉域アクセス → AWS PrivateLink"),
        acct_group("cons", 30, 70, 400, 460, "自社 アカウント"),
        vpc_group("cv", 60, 110, 340, 380, "Consumer VPC (Internet 不可)"),
        aws_icon("app1", 100, 160, "ec2", 50, 50),
        label("app1_l", 70, 218, "マイクロサービス A", 130),
        aws_icon("app2", 100, 270, "ec2", 50, 50),
        label("app2_l", 70, 328, "マイクロサービス B", 130),
        aws_icon_color("iep", 280, 210, "endpoint", CLR_EP, 50, 50),
        label("iep_l", 250, 268, "Interface EP\n(Private IP)", 130, bold=False),
        acct_group("prov", 540, 70, 430, 460, "SaaS ベンダ アカウント"),
        vpc_group("pv", 570, 110, 380, 380, "Provider VPC"),
        aws_icon_color("nlb", 760, 180, "network_load_balancer", "#8C4FFF", 50, 50),
        label("nlb_l", 730, 238, "NLB", 130),
        aws_icon("papi", 760, 320, "ec2", 50, 50),
        label("papi_l", 720, 378, "SaaS REST API", 140),
        aws_icon_color("pls", 620, 250, "endpoint", CLR_EP, 50, 50),
        label("pls_l", 590, 308, "Endpoint Service", 130),
        arrow("e1", "app1", "iep", CLR_EP),
        arrow("e2", "app2", "iep", CLR_EP),
        arrow("e3", "iep", "pls", CLR_EP, w=3, label_text="PrivateLink\n(AWS bb)"),
        arrow("e4", "pls", "nlb", CLR_EP, w=2),
        arrow("e5", "nlb", "papi", "#666"),
        note("n1", 30, 540, 940, 45, "◎ 正解 A: Provider 側 NLB + VPC Endpoint Service、Consumer 側 Interface EP。\nインターネット通過なし / セキュリティグループと IAM で制御 / 同リージョン内", fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d_sap139", "SAP-139 PrivateLink", cells)


def diag_162():
    """SAP-162: Expose on-prem API to other AWS customers via PrivateLink"""
    cells = [
        title("t", 0, 10, "SAP-162: オンプレ API を外部 AWS 企業へ閉域提供 → PrivateLink (NLB + VPC EP Service)"),
        dc_group("dc", 30, 90, 200, 240, "金融会社 オンプレ DC"),
        aws_icon("risk", 85, 120, "ec2", 50, 50),
        label("risk_l", 55, 178, "リスク計算エンジン", 140),
        aws_icon_color("dx", 85, 220, "direct_connect", CLR_DX, 50, 50),
        label("dx_l", 55, 278, "DX + VPN", 140),
        vpc_group("pv", 290, 70, 360, 400, "金融会社 VPC"),
        aws_icon_color("vgw", 320, 110, "site_to_site_vpn", CLR_VPN, 50, 50),
        label("vgw_l", 290, 168, "VGW", 130),
        aws_icon_color("nlb", 500, 110, "network_load_balancer", "#8C4FFF", 50, 50),
        label("nlb_l", 470, 168, "NLB (内部)", 130),
        aws_icon_color("eps", 500, 250, "endpoint", CLR_EP, 50, 50),
        label("eps_l", 460, 308, "VPC EP Service", 140),
        arrow("a1", "risk", "dx"),
        arrow("a2", "dx", "vgw", CLR_DX),
        arrow("a3", "vgw", "nlb", "#666"),
        arrow("a4", "nlb", "eps", CLR_EP),
        vpc_group("cv1", 700, 70, 260, 180, "外部企業 A VPC"),
        aws_icon_color("ep1", 760, 100, "endpoint", CLR_EP, 50, 50),
        label("ep1_l", 730, 158, "Interface EP", 130),
        aws_icon("c1", 860, 100, "ec2", 40, 40),
        label("c1l", 830, 148, "API Client", 120, bold=False),
        vpc_group("cv2", 700, 270, 260, 200, "外部企業 B VPC"),
        aws_icon_color("ep2", 760, 300, "endpoint", CLR_EP, 50, 50),
        label("ep2_l", 730, 358, "Interface EP", 130),
        aws_icon("c2", 860, 300, "ec2", 40, 40),
        label("c2l", 830, 348, "API Client", 120, bold=False),
        arrow("b1", "eps", "ep1", CLR_EP, w=2, label_text="PrivateLink"),
        arrow("b2", "eps", "ep2", CLR_EP, w=2, label_text="PrivateLink"),
        note("n1", 30, 490, 940, 90, "◎ 正解 C: NLB + VPC Endpoint Service で提供側を公開 → 利用者は Interface EP を作成。\n・インターネット非経由\n・利用者ごとに許可 (accept/reject) 可 → 数百~数千企業に拡張容易", fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d_sap162", "SAP-162 On-prem via PrivateLink", cells)


def diag_165():
    """SAP-165: TGW route tables to isolate departments (segmentation)"""
    cells = [
        title("t", 0, 10, "SAP-165: TGW ルートテーブル分離 → セグメント別ルーティング"),
        aws_icon_color("tgw", 450, 250, "transit_gateway", CLR_TGW, 70, 70),
        label("tgw_l", 410, 325, "Transit Gateway", 150),
        box("rtA", 70, 70, 260, 100, "TGW RT A (支払い系のみ)", fill="#EBF5E8", stroke="#7AA116"),
        label("rtA_l", 80, 100, "• Associate: VPC-A1,A2\n• Propagate: A*", 240, bold=False),
        box("rtB", 70, 190, 260, 100, "TGW RT B (共通 SVC)", fill="#EBF1FF", stroke="#3B48CC"),
        label("rtB_l", 80, 220, "• Associate: VPC-SVC\n• Propagate: All", 240, bold=False),
        box("rtC", 70, 310, 260, 100, "TGW RT C (Egress)", fill="#FFF5EB", stroke="#ED7100"),
        label("rtC_l", 80, 340, "• Associate: VPC-EG\n• Propagate: 0.0.0.0/0", 240, bold=False),
        vpc_group("va1", 580, 70, 160, 80, "VPC-A1 (決済)"),
        aws_icon("va1e", 630, 90, "ec2", 40, 40),
        vpc_group("va2", 760, 70, 160, 80, "VPC-A2 (決済)"),
        aws_icon("va2e", 810, 90, "ec2", 40, 40),
        vpc_group("vsvc", 580, 180, 340, 80, "VPC-SVC (共通)"),
        aws_icon("vsvce", 730, 200, "ec2", 40, 40),
        vpc_group("veg", 580, 290, 340, 100, "VPC-EG (Egress)"),
        aws_icon_color("egn", 730, 320, "nat_gateway", CLR_NAT, 40, 40),
        arrow("ea1", "va1", "tgw", CLR_TGW),
        arrow("ea2", "va2", "tgw", CLR_TGW),
        arrow("ea3", "vsvc", "tgw", CLR_TGW),
        arrow("ea4", "veg", "tgw", CLR_TGW),
        edge("l1", "rtA", "tgw", "#7AA116", dashed=True),
        edge("l2", "rtB", "tgw", "#3B48CC", dashed=True),
        edge("l3", "rtC", "tgw", "#ED7100", dashed=True),
        note("n1", 30, 430, 940, 70, "◎ 正解 C: TGW のルートテーブルを分離して「関連付け (Associate) 」と「伝播 (Propagate) 」を明示設定。\n・既存の 1 本のデフォルト RT から 3 本へ移行 → セグメント単位でトラフィック制御", fill="#EBF5E8", stroke="#7AA116"),
        note("n2", 30, 510, 940, 75, "比較: ・1 つのデフォルト RT — 全 VPC が相互疎通可で監査 NG ／ ・NACL/SG のみ — パスは通っており経路制御の責任分界として不十分"),
    ]
    return wrap("d_sap165", "SAP-165 TGW RT Segmentation", cells)


def diag_167():
    """SAP-167: 100+ accounts centralized egress inspection via AWS Network Firewall"""
    cells = [
        title("t", 0, 10, "SAP-167: 100+ アカウント 統一検査 → TGW + Inspection VPC (Network Firewall)"),
        acct_group("a1", 30, 60, 150, 110, "Acct 1"),
        vpc_group("v1", 50, 90, 110, 70, "VPC"),
        aws_icon("v1e", 80, 105, "ec2", 40, 40),
        acct_group("a2", 30, 190, 150, 110, "Acct 2"),
        vpc_group("v2", 50, 220, 110, 70, "VPC"),
        aws_icon("v2e", 80, 235, "ec2", 40, 40),
        acct_group("a3", 30, 320, 150, 110, "... 100+"),
        vpc_group("v3", 50, 350, 110, 70, "VPC"),
        aws_icon("v3e", 80, 365, "ec2", 40, 40),
        aws_icon_color("tgw", 240, 240, "transit_gateway", CLR_TGW, 60, 60),
        label("tgw_l", 210, 308, "Transit Gateway", 120),
        acct_group("net", 390, 50, 580, 470, "Networking アカウント"),
        vpc_group("iv", 420, 90, 510, 410, "Inspection VPC (3 AZ)"),
        aws_icon_color("nfw1", 470, 140, "network_firewall", CLR_NFW, 50, 50),
        label("nfw1_l", 440, 198, "NFW (a)", 120),
        aws_icon_color("nfw2", 620, 140, "network_firewall", CLR_NFW, 50, 50),
        label("nfw2_l", 590, 198, "NFW (b)", 120),
        aws_icon_color("nfw3", 770, 140, "network_firewall", CLR_NFW, 50, 50),
        label("nfw3_l", 740, 198, "NFW (c)", 120),
        aws_icon_color("ngw1", 470, 250, "nat_gateway", CLR_NAT, 50, 50),
        label("ngw1_l", 440, 308, "NAT GW (a)", 120),
        aws_icon_color("ngw2", 620, 250, "nat_gateway", CLR_NAT, 50, 50),
        label("ngw2_l", 590, 308, "NAT GW (b)", 120),
        aws_icon_color("ngw3", 770, 250, "nat_gateway", CLR_NAT, 50, 50),
        label("ngw3_l", 740, 308, "NAT GW (c)", 120),
        aws_icon("igw", 620, 370, "internet_gateway", 50, 50),
        label("igw_l", 590, 428, "Internet GW", 130),
        arrow("x1", "v1", "tgw", CLR_TGW),
        arrow("x2", "v2", "tgw", CLR_TGW),
        arrow("x3", "v3", "tgw", CLR_TGW),
        arrow("x4", "tgw", "nfw2", CLR_NFW, w=3, label_text="0.0.0.0/0"),
        arrow("x5", "nfw2", "ngw2", CLR_NAT),
        arrow("x6", "ngw2", "igw", CLR_NAT),
        note("n1", 30, 460, 350, 120, "◎ 正解 A: Inspection VPC に Network Firewall + NAT GW を AZ 毎配置。\nTGW の Appliance Mode で同一 AZ 経路を保証。\nドメイン/IP/SNI 検査を中央で一元管理。", fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d_sap167", "SAP-167 Inspection VPC", cells)


def diag_180():
    """SAP-180: Cross-VPC 3rd-party SaaS access via PrivateLink (existing DX)"""
    cells = [
        title("t", 0, 10, "SAP-180: 別 VPC の 3rd-party SaaS を閉域呼び出し → PrivateLink"),
        dc_group("hos", 30, 90, 180, 200, "病院 (院内ポータル)"),
        aws_icon("user", 85, 120, "user", 50, 50),
        label("user_l", 55, 178, "医師ポータル", 140),
        aws_icon_color("dx", 85, 220, "direct_connect", CLR_DX, 50, 50),
        label("dx_l", 55, 278, "既存 DX", 140),
        vpc_group("own", 250, 70, 320, 400, "自社 VPC"),
        aws_icon_color("vgw", 280, 110, "site_to_site_vpn", CLR_VPN, 50, 50),
        label("vgw_l", 250, 168, "VGW/DX Attach", 140),
        aws_icon("app", 280, 240, "ec2", 50, 50),
        label("app_l", 250, 298, "予約解析 App", 140),
        aws_icon_color("iep", 460, 240, "endpoint", CLR_EP, 50, 50),
        label("iep_l", 420, 298, "Interface EP", 140),
        vpc_group("saas", 650, 70, 320, 400, "SaaS ベンダ VPC"),
        aws_icon_color("pls", 680, 240, "endpoint", CLR_EP, 50, 50),
        label("pls_l", 640, 298, "VPC EP Service", 140),
        aws_icon_color("nlb", 830, 160, "network_load_balancer", "#8C4FFF", 50, 50),
        label("nlb_l", 800, 218, "NLB (内部)", 130),
        aws_icon("saasapp", 830, 320, "ec2", 50, 50),
        label("saasapp_l", 800, 378, "SaaS API", 130),
        arrow("e1", "user", "dx"),
        arrow("e2", "dx", "vgw", CLR_DX),
        arrow("e3", "vgw", "app"),
        arrow("e4", "app", "iep", CLR_EP),
        arrow("e5", "iep", "pls", CLR_EP, w=3, label_text="PrivateLink"),
        arrow("e6", "pls", "nlb", CLR_EP),
        arrow("e7", "nlb", "saasapp"),
        note("n1", 30, 490, 940, 90, "◎ 正解 A: 既存 DX はそのまま、SaaS 側の NLB + VPC Endpoint Service に Interface EP で接続。\n・HIPAA 相当: インターネット通過ゼロ\n・VPC Peering/TGW 不要で境界最小化", fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d_sap180", "SAP-180 PrivateLink HC", cells)


def diag_202():
    """SAP-202: 2 DC + 5Gbps continuous → DX + LAG + TGW + Multi-Account"""
    cells = [
        title("t", 0, 10, "SAP-202: 2 拠点 ≥5Gbps 常時帯域 → Direct Connect (LAG) + Transit VIF + TGW"),
        dc_group("dc1", 30, 80, 160, 140, "拠点 DC 1"),
        aws_icon("d1", 85, 110, "corporate_data_center_2", 50, 50),
        label("d1_l", 55, 168, "基幹システム", 130),
        dc_group("dc2", 30, 260, 160, 140, "拠点 DC 2"),
        aws_icon("d2", 85, 290, "corporate_data_center_2", 50, 50),
        label("d2_l", 55, 348, "基幹システム", 130),
        aws_icon_color("dx1", 240, 100, "direct_connect", CLR_DX, 50, 50),
        label("dx1_l", 210, 158, "DX LAG 10G×2", 130),
        aws_icon_color("dx2", 240, 280, "direct_connect", CLR_DX, 50, 50),
        label("dx2_l", 210, 338, "DX LAG 10G×2", 130),
        aws_icon_color("dxgw", 420, 190, "direct_connect", CLR_DX, 60, 60),
        label("dxgw_l", 390, 258, "DX Gateway", 130),
        aws_icon_color("tgw", 600, 190, "transit_gateway", CLR_TGW, 60, 60),
        label("tgw_l", 570, 258, "Transit Gateway", 130),
        acct_group("apps", 770, 70, 200, 350, "API アカウント群"),
        vpc_group("va", 790, 100, 160, 70, "API VPC 1"),
        aws_icon("vae", 830, 120, "ec2", 40, 40),
        vpc_group("vb", 790, 190, 160, 70, "API VPC 2"),
        aws_icon("vbe", 830, 210, "ec2", 40, 40),
        vpc_group("vc", 790, 280, 160, 110, "決済 VPC"),
        aws_icon("vce", 830, 310, "ec2", 40, 40),
        arrow("a1", "d1", "dx1"),
        arrow("a2", "d2", "dx2"),
        arrow("a3", "dx1", "dxgw", CLR_DX, w=3, label_text="Transit VIF"),
        arrow("a4", "dx2", "dxgw", CLR_DX, w=3, label_text="Transit VIF"),
        arrow("a5", "dxgw", "tgw", CLR_TGW, w=3),
        arrow("a6", "tgw", "va", CLR_TGW),
        arrow("a7", "tgw", "vb", CLR_TGW),
        arrow("a8", "tgw", "vc", CLR_TGW),
        note("n1", 30, 430, 940, 140, "◎ 正解 A: DX 接続 × 2 拠点、各拠点で LAG (Link Aggregation Group) により 10Gbps×2 = 20Gbps 確保 (5Gbps 余裕)。\n・Transit VIF + DX Gateway でマルチアカウント TGW に集約 (Private VIF は TGW に直接アタッチ不可)\n・各アカウントは TGW アタッチを AWS RAM 共有で受け取り\n・Site-to-Site VPN は副系として構成可 (要件では不要レベル)", fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d_sap202", "SAP-202 DX LAG + Transit VIF", cells)


def diag_222():
    """SAP-222: Fargate + Interface Endpoints (no Internet)"""
    cells = [
        title("t", 0, 10, "SAP-222: Fargate 閉域化 → Interface Endpoint (ECR/CW/S3 GEP)"),
        vpc_group("vpc", 60, 70, 880, 420, "VPC (Internet なし)"),
        box("prv", 90, 110, 400, 360, "Private Subnet", fill="#E9F3E6", stroke="#248814"),
        aws_icon("farg", 130, 150, "fargate", 60, 60),
        label("farg_l", 100, 218, "Fargate タスク\n(API サーバ)", 120, bold=False),
        aws_icon_color("nlb", 320, 160, "network_load_balancer", "#8C4FFF", 50, 50),
        label("nlb_l", 290, 218, "内部 NLB", 130),
        aws_icon("ddb", 130, 320, "dynamodb", 50, 50),
        label("ddb_l", 100, 378, "DynamoDB (GEP)", 130),
        aws_icon("s3", 320, 320, "simple_storage_service", 50, 50),
        label("s3_l", 290, 378, "S3 (GEP)", 130),
        box("epbox", 520, 110, 400, 360, "Endpoint サブネット (AZ×3)", fill="#EBF1FF", stroke="#3B48CC"),
        aws_icon_color("ecr", 560, 150, "endpoint", CLR_EP, 50, 50),
        label("ecr_l", 530, 208, "ECR API + DKR", 130),
        aws_icon_color("cw", 710, 150, "endpoint", CLR_EP, 50, 50),
        label("cw_l", 680, 208, "CloudWatch Logs", 140),
        aws_icon_color("sts", 560, 280, "endpoint", CLR_EP, 50, 50),
        label("sts_l", 530, 338, "STS / Secrets", 140),
        aws_icon_color("s3g", 710, 280, "endpoint", CLR_EP, 50, 50),
        label("s3g_l", 680, 338, "S3 / DDB Gateway EP", 160),
        arrow("e1", "farg", "ecr", CLR_EP, w=2, label_text="Pull Image"),
        arrow("e2", "farg", "cw", CLR_EP, w=2),
        arrow("e3", "farg", "sts", CLR_EP),
        arrow("e4", "farg", "s3g", CLR_EP),
        arrow("e5", "farg", "ddb", CLR_EP),
        arrow("e6", "farg", "s3", CLR_EP),
        note("n1", 30, 500, 940, 85, "◎ 正解 B: Fargate を VPC 配置し、必要な AWS API 全てを Interface/Gateway EP 経由に。\nFargate がイメージ pull・ログ送信・シークレット取得を閉域で行える。NAT GW / IGW 不要。", fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d_sap222", "SAP-222 Fargate Private", cells)


def diag_227():
    """SAP-227: 5 regions 15+ VPC each, fast scale → AWS Cloud WAN"""
    cells = [
        title("t", 0, 10, "SAP-227: 5 リージョン × 15+ VPC × 買収で増加 → AWS Cloud WAN"),
        region_group("r1", 30, 60, 175, 180, "us-east-1"),
        vpc_group("r1v1", 50, 100, 55, 50, "VPC"),
        vpc_group("r1v2", 115, 100, 55, 50, "VPC"),
        vpc_group("r1v3", 50, 170, 55, 50, "VPC"),
        vpc_group("r1v4", 115, 170, 55, 50, "VPC"),
        region_group("r2", 215, 60, 175, 180, "eu-west-1"),
        vpc_group("r2v1", 235, 100, 55, 50, "VPC"),
        vpc_group("r2v2", 300, 100, 55, 50, "VPC"),
        vpc_group("r2v3", 235, 170, 55, 50, "VPC"),
        vpc_group("r2v4", 300, 170, 55, 50, "VPC"),
        region_group("r3", 400, 60, 175, 180, "ap-northeast-1"),
        vpc_group("r3v1", 420, 100, 55, 50, "VPC"),
        vpc_group("r3v2", 485, 100, 55, 50, "VPC"),
        vpc_group("r3v3", 420, 170, 55, 50, "VPC"),
        vpc_group("r3v4", 485, 170, 55, 50, "VPC"),
        region_group("r4", 585, 60, 175, 180, "sa-east-1"),
        vpc_group("r4v1", 605, 100, 55, 50, "VPC"),
        vpc_group("r4v2", 670, 100, 55, 50, "VPC"),
        vpc_group("r4v3", 605, 170, 55, 50, "VPC"),
        vpc_group("r4v4", 670, 170, 55, 50, "VPC"),
        region_group("r5", 770, 60, 210, 180, "ap-south-1 (新規)"),
        vpc_group("r5v1", 790, 100, 60, 50, "VPC"),
        vpc_group("r5v2", 860, 100, 60, 50, "VPC"),
        vpc_group("r5v3", 790, 170, 60, 50, "VPC"),
        vpc_group("r5v4", 860, 170, 60, 50, "VPC"),
        box("cwan", 30, 270, 950, 130, "AWS Cloud WAN Core Network", fill="#F2E9FF", stroke="#8C4FFF"),
        label("cwan1", 50, 300, "• Global Network 1 つで全リージョンのコアネットワークを管理", 900, bold=False),
        label("cwan2", 50, 325, "• セグメント (例: prod / dev / svc) を YAML ポリシーで宣言", 900, bold=False),
        label("cwan3", 50, 350, "• 新リージョン追加 = Core Edge を 1 行 (数分) で増設", 900, bold=False),
        arrow("a1", "r1", "cwan", "#8C4FFF"),
        arrow("a2", "r2", "cwan", "#8C4FFF"),
        arrow("a3", "r3", "cwan", "#8C4FFF"),
        arrow("a4", "r4", "cwan", "#8C4FFF"),
        arrow("a5", "r5", "cwan", "#8C4FFF"),
        note("n1", 30, 410, 940, 90, "◎ 正解 C: Cloud WAN で全世界 VPC を単一ネットワークとして管理。\n・買収でリージョン/VPC が増えても宣言的に吸収\n・TGW Peering は N(N-1)/2 で爆発 (5 リージョン = 10 ピア + RT 維持)", fill="#EBF5E8", stroke="#7AA116"),
        note("n2", 30, 505, 940, 80, "誤答: \n・全リージョン TGW + Peering — スケール時に管理工数爆発\n・VPN ハブ集約 — 帯域/遅延不足"),
    ]
    return wrap("d_sap227", "SAP-227 Cloud WAN Global", cells)


def diag_239():
    """SAP-239: Shared service VPC → PrivateLink to 10 consumers"""
    cells = [
        title("t", 0, 10, "SAP-239: 共有 API サービス → PrivateLink で 10 VPC に公開"),
        vpc_group("sv", 30, 80, 320, 440, "共有サービス VPC"),
        aws_icon_color("nlb", 150, 120, "network_load_balancer", "#8C4FFF", 60, 60),
        label("nlb_l", 110, 188, "NLB (高負荷対応)", 140),
        aws_icon("ec1", 80, 260, "ec2", 50, 50),
        label("ec1_l", 50, 318, "配送最適化 App", 140),
        aws_icon("ec2", 220, 260, "ec2", 50, 50),
        label("ec2_l", 190, 318, "配送最適化 App", 140),
        aws_icon_color("svc", 150, 400, "endpoint", CLR_EP, 60, 60),
        label("svc_l", 110, 468, "VPC EP Service", 140),
        arrow("x1", "ec1", "nlb", "#666"),
        arrow("x2", "ec2", "nlb", "#666"),
        arrow("x3", "nlb", "svc", CLR_EP),
    ]
    # Consumer grid 10 VPCs
    consumer_positions = [(420,80),(600,80),(790,80),(420,200),(600,200),(790,200),(420,320),(600,320),(790,320),(600,440)]
    for i, (cx, cy) in enumerate(consumer_positions, start=1):
        cells.append(vpc_group(f"cv{i}", cx, cy, 170, 110, f"Consumer VPC {i}"))
        cells.append(aws_icon_color(f"cep{i}", cx+15, cy+35, "endpoint", CLR_EP, 40, 40))
        cells.append(label(f"cep{i}_l", cx+5, cy+83, "Interface EP", 130, bold=False))
        cells.append(aws_icon(f"ccl{i}", cx+100, cy+35, "ec2", 40, 40))
        cells.append(label(f"ccl{i}_l", cx+85, cy+83, "App", 80, bold=False))
        cells.append(arrow(f"ce{i}", f"cep{i}", "svc", CLR_EP, w=2))
    cells.append(note("n1", 30, 540, 940, 45, "◎ 正解 D: 提供側 NLB + VPC Endpoint Service、各 Consumer VPC は Interface Endpoint で接続。推移ルーティング不要 / IP 衝突も解消。", fill="#EBF5E8", stroke="#7AA116"))
    return wrap("d_sap239", "SAP-239 PrivateLink Shared Service", cells)


def diag_258():
    """SAP-258: New project account → TGW/DXGW access to on-prem"""
    cells = [
        title("t", 0, 10, "SAP-258: 新規アカウント VPC → オンプレアクセス (DX Gateway 集約)"),
        dc_group("dc", 30, 80, 180, 240, "社内 データセンター"),
        aws_icon("ds", 85, 110, "corporate_data_center_2", 50, 50),
        label("ds_l", 55, 168, "基幹 SQL Server", 140),
        aws_icon_color("dx", 85, 230, "direct_connect", CLR_DX, 50, 50),
        label("dx_l", 55, 288, "DX", 140),
        aws_icon_color("dxgw", 260, 180, "direct_connect", CLR_DX, 60, 60),
        label("dxgw_l", 230, 248, "DX Gateway", 130),
        label("dxgw_l2", 230, 266, "(共有アカウント)", 130, bold=False),
        aws_icon_color("tgw", 440, 180, "transit_gateway", CLR_TGW, 60, 60),
        label("tgw_l", 410, 248, "Transit Gateway", 130),
        label("tgw_l2", 410, 266, "(RAM 共有)", 130, bold=False),
        acct_group("shared", 220, 70, 280, 330, "共有サービス アカウント"),
        acct_group("proj1", 580, 60, 180, 220, "新規プロジェクト A"),
        vpc_group("pv1", 600, 100, 150, 150, "Project VPC A"),
        aws_icon("p1e", 660, 140, "ec2", 40, 40),
        label("p1e_l", 630, 188, "需要予測 App", 130, bold=False),
        acct_group("proj2", 780, 60, 180, 220, "新規プロジェクト B"),
        vpc_group("pv2", 800, 100, 150, 150, "Project VPC B"),
        aws_icon("p2e", 860, 140, "ec2", 40, 40),
        label("p2e_l", 830, 188, "新規 App", 130, bold=False),
        arrow("e1", "ds", "dx"),
        arrow("e2", "dx", "dxgw", CLR_DX, w=2, label_text="Transit VIF"),
        arrow("e3", "dxgw", "tgw", CLR_TGW, w=3),
        arrow("e4", "tgw", "pv1", CLR_TGW),
        arrow("e5", "tgw", "pv2", CLR_TGW),
        note("n1", 30, 410, 940, 170, "◎ 正解 A+E+F の構成:\n A) TGW と DX Gateway を Transit VIF で関連付け\n E) AWS RAM で TGW アタッチ権限を プロジェクトアカウントに共有\n F) プロジェクト VPC を TGW にアタッチ (各アカウント実行)\n\n誤答: ・アカウント毎に DX 作り直し — 回線追加コスト / 中央統制崩壊\n・VPC Peering で共有アカウントに入る — 推移不可で DX まで届かない", fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d_sap258", "SAP-258 TGW + DXGW + RAM", cells)


def diag_280():
    """SAP-280: Same-region different VPC DB connectivity → VPC Peering (lowest cost)"""
    cells = [
        title("t", 0, 10, "SAP-280: 同リージョン 2 VPC 間 DB 接続 (非重複 CIDR) → VPC Peering"),
        vpc_group("va", 60, 100, 380, 380, "VPC A (10.10.0.0/16) — API"),
        aws_icon("asg", 130, 140, "auto_scaling", 50, 50),
        label("asg_l", 100, 198, "Auto Scaling\n10 台 EC2", 130, bold=False),
        aws_icon("api1", 300, 140, "ec2", 50, 50),
        label("api1_l", 270, 198, "請求書 API", 130),
        aws_icon("api2", 300, 260, "ec2", 50, 50),
        label("api2_l", 270, 318, "請求書 API", 130),
        vpc_group("vb", 560, 100, 380, 380, "VPC B (10.20.0.0/16) — DB"),
        aws_icon("orcl", 720, 180, "rds", 60, 60),
        label("orcl_l", 690, 248, "Oracle DB (EC2)", 140),
        label("orcl_l2", 690, 266, "JDBC 1521", 140, bold=False),
        edge("pe", "va", "vb", "#248814", w=4, label_text="VPC Peering"),
        note("n1", 30, 490, 940, 100, "◎ 正解 C: 同一リージョン ＆ CIDR 非重複 → VPC Peering がコスト最小 ＆ 数分で構築。\n・BGP/VGW/TGW 不要\n・データ転送料 $0.01/GB (AZ またぎ) / TGW は $0.02/GB 処理料 + 転送料で割高\n・負荷試験の 2 週間リリースに間に合う", fill="#EBF5E8", stroke="#7AA116"),
    ]
    return wrap("d_sap280", "SAP-280 VPC Peering 2 VPC", cells)


def diag_290():
    """SAP-290: DX SLA 99.9% → 2 DX in 2 different DX locations + Transit VIF"""
    cells = [
        title("t", 0, 10, "SAP-290: DX SLA 99.9% 達成 → 2 ロケーション × DX + 同一 VIF タイプ"),
        dc_group("site1", 30, 80, 200, 150, "拠点"),
        aws_icon("u1", 85, 110, "user", 50, 50),
        label("u1_l", 55, 168, "利用拠点 (10 都市)", 140),
        aws_icon_color("dxloc1", 270, 90, "direct_connect", CLR_DX, 50, 50),
        label("dxloc1_l", 240, 148, "DX Loc. 1 (既存)", 130),
        label("dxloc1_l2", 240, 166, "1 Gbps", 130, bold=False),
        aws_icon_color("dxloc2", 270, 210, "direct_connect", CLR_DX, 50, 50),
        label("dxloc2_l", 240, 268, "DX Loc. 2 (新設)", 130),
        label("dxloc2_l2", 240, 286, "1 Gbps 別経路", 130, bold=False),
        aws_icon_color("dxgw", 440, 150, "direct_connect", CLR_DX, 60, 60),
        label("dxgw_l", 400, 218, "DX Gateway", 140),
        aws_icon_color("tgw", 620, 150, "transit_gateway", CLR_TGW, 60, 60),
        label("tgw_l", 580, 218, "Transit Gateway", 140),
        vpc_group("tok", 800, 80, 170, 220, "東京 API VPC"),
        aws_icon("api", 850, 110, "ec2", 50, 50),
        label("api_l", 820, 168, "API", 130),
        aws_icon("rdb", 850, 210, "rds", 50, 50),
        label("rdb_l", 820, 268, "RDB", 130),
        arrow("a1", "u1", "dxloc1"),
        arrow("a2", "u1", "dxloc2"),
        arrow("a3", "dxloc1", "dxgw", CLR_DX, w=3, label_text="Transit VIF"),
        arrow("a4", "dxloc2", "dxgw", CLR_DX, w=3, label_text="Transit VIF"),
        arrow("a5", "dxgw", "tgw", CLR_TGW, w=3),
        arrow("a6", "tgw", "tok", CLR_TGW),
        note("n1", 30, 330, 940, 90, "◎ 正解 C: 同じ AWS リージョン内で DX 接続を 2 つの異なる DX ロケーション に分散 → SLA 99.9% 条件を満たす。\n・両経路に Transit VIF を Active/Active で張り、DX GW で TGW へ集約\n・BGP multi-exit で自動フェイルオーバ / BFD で高速切替", fill="#EBF5E8", stroke="#7AA116"),
        note("n2", 30, 430, 940, 150, "誤答: \n・同一 DX ロケーションに接続 2 本 — 物理拠点の単一障害を救えない (SLA 99.9% 未達)\n・VPN をバックアップ — 帯域は落ちるが SLA 99.9% の前提は DX の冗長\n・PublicVIF/PrivateVIF を混在 — Transit VIF 統一が DX GW + TGW 要件"),
    ]
    return wrap("d_sap290", "SAP-290 DX SLA 99.9", cells)


# =========================================================
# Write all
# =========================================================

BUILDERS = {
    "SAP-2":   diag_2,
    "SAP-15":  diag_15,
    "SAP-21":  diag_21,
    "SAP-35":  diag_35,
    "SAP-48":  diag_48,
    "SAP-61":  diag_61,
    "SAP-66":  diag_66,
    "SAP-70":  diag_70,
    "SAP-73":  diag_73,
    "SAP-78":  diag_78,
    "SAP-106": diag_106,
    "SAP-108": diag_108,
    "SAP-112": diag_112,
    "SAP-121": diag_121,
    "SAP-139": diag_139,
    "SAP-162": diag_162,
    "SAP-165": diag_165,
    "SAP-167": diag_167,
    "SAP-180": diag_180,
    "SAP-202": diag_202,
    "SAP-222": diag_222,
    "SAP-227": diag_227,
    "SAP-239": diag_239,
    "SAP-258": diag_258,
    "SAP-280": diag_280,
    "SAP-290": diag_290,
}

def main():
    for qid, fn in BUILDERS.items():
        path = os.path.join(OUT, f"{qid}.drawio")
        with open(path, "w") as f:
            f.write(fn())
        print(f"wrote {path}")
    print(f"total: {len(BUILDERS)}")

if __name__ == "__main__":
    main()
