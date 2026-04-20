#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AWS SAP-C02 ネットワーク分離・接続設計テーマの解説を品質チェック+加筆。

- 判断ポイントセクションを末尾に追加
- 明らかな誤りは修正
- 元の説明は保持
"""

import json
import os
from copy import deepcopy

QUESTIONS_PATH = '/Users/aki/aws-sap/docs/data/questions.json'

# ===========================================================================
# 共通の判断ポイントテンプレート（カテゴリごと）
# ===========================================================================

# Peering vs TGW の判断
TIPS_PEERING_VS_TGW = """<br><br>📌 判断ポイント<br>
<strong>VPC Peering vs Transit Gateway の使い分け（最重要）:</strong><br>
<table border='1' cellpadding='4'><tr><th>軸</th><th>VPC Peering</th><th>Transit Gateway</th></tr>
<tr><td>接続数</td><td>N×(N-1)/2 で爆発（10VPC=45本）</td><td>N アタッチで線形（10VPC=10本）</td></tr>
<tr><td>推移的ルーティング</td><td>✕ A→B→C は不可</td><td>○ ハブ経由で全通信可</td></tr>
<tr><td>料金モデル</td><td>接続料金なし、データ転送のみ</td><td>アタッチ時間 + データ処理 GB</td></tr>
<tr><td>適用場面</td><td>2〜3 VPC の単純接続</td><td>VPC 数 ≥ 5 / マルチアカウント / オンプレ含む</td></tr>
<tr><td>CIDR 重複</td><td>不可（接続できない）</td><td>不可（PrivateLink で回避）</td></tr></table><br>
<strong>判断フロー:</strong> 接続数 ≥ 5 または将来増加見込み → TGW。2〜3 VPC で安定 → Peering。CIDR 重複あり → PrivateLink 一択。<br>
<strong>引っ掛け:</strong>「VPC ピアリングで N 個 VPC を接続」「ピアリングで推移的ルーティング」「ピアリングで数百 VPC スケール」はいずれも罠。"""

# DX vs VPN の判断
TIPS_DX_VS_VPN = """<br><br>📌 判断ポイント<br>
<strong>Direct Connect vs Site-to-Site VPN の使い分け:</strong><br>
<table border='1' cellpadding='4'><tr><th>軸</th><th>Site-to-Site VPN</th><th>Direct Connect</th></tr>
<tr><td>帯域</td><td>1.25 Gbps/トンネル（最大 ~5 Gbps）</td><td>1/10/100 Gbps の専用線</td></tr>
<tr><td>レイテンシ・ジッター</td><td>インターネット経由で変動大</td><td>低遅延・安定（一桁 ms）</td></tr>
<tr><td>セットアップ時間</td><td>数十分</td><td>数週間〜数か月（物理敷設）</td></tr>
<tr><td>初期/月額コスト</td><td>低（IPsec のみ）</td><td>高（ポート料金 + クロスコネクト）</td></tr>
<tr><td>暗号化</td><td>IPsec で標準暗号化</td><td>非暗号化（MACsec オプション可）</td></tr>
<tr><td>「インターネット非経由」</td><td>✕ パブリック網経由（暗号化のみ）</td><td>○ 専用線で完全閉域</td></tr></table><br>
<strong>判断フロー:</strong>
<ol>
<li>「インターネット非経由」「閉域要件」→ DX 必須（VPN は NG）</li>
<li>帯域 ≥ 1 Gbps 常時 / レイテンシ厳守 → DX</li>
<li>帯域 < 数百 Mbps / 短期構築 / コスト最優先 → VPN</li>
<li>DR 用バックアップ → DX + VPN（DX 主、VPN 副）</li>
</ol>
<strong>引っ掛け:</strong>「VPN で帯域保証」「DX を即日構築」「50 Mbps 以下に DX」「VPN がインターネット非経由」はすべて罠。"""

# Hub-and-Spoke / Egress 集約の判断
TIPS_HUB_AND_SPOKE = """<br><br>📌 判断ポイント<br>
<strong>Hub-and-Spoke / Egress 集約の構成パターン:</strong><br>
<ul>
<li><strong>中央 Egress VPC + TGW:</strong> NAT GW を 1 か所に集約。全スポークから 0.0.0.0/0 を TGW 経由で Egress VPC へ。NAT GW コストを N 個 → 数個に削減。</li>
<li><strong>+ Network Firewall:</strong> Egress VPC 内に Network Firewall を配置すれば、組織全体のアウトバウンドを単一ポリシーで集中フィルタリング（FQDN/Suricata ルール）。</li>
<li><strong>+ Gateway Load Balancer (GWLB):</strong> サードパーティ製 IDS/IPS/FW アプライアンス（Palo Alto, Check Point 等）を透過挿入する場合に使用。GWLB エンドポイントをルートテーブルの next-hop に指定。</li>
</ul>
<strong>引っ掛け:</strong>「VPC ピアリングで Egress 集約」（推移不可で NG）、「PrivateLink で NAT エクスポート」（不可）、「ALB で集中検査」（L4/L3 検査は NLB/GWLB）。<br>
<strong>スケール基準:</strong> VPC 数 ≥ 数十 → TGW + Egress VPC 一択。NAT GW は AZ ごとに 1 つで AZ 障害対策。"""

# マルチリージョン接続（TGW Peering / Cloud WAN / DX GW）
TIPS_MULTI_REGION = """<br><br>📌 判断ポイント<br>
<strong>マルチリージョン接続の選択肢:</strong><br>
<table border='1' cellpadding='4'><tr><th>方式</th><th>用途</th><th>特徴</th></tr>
<tr><td>Inter-Region VPC Peering</td><td>2〜数 VPC、安定的</td><td>低コスト・推移なし・同一アカウント可</td></tr>
<tr><td>TGW Inter-Region Peering</td><td>各リージョン TGW を接続</td><td>各リージョンで TGW を持つ前提。手動でルート伝播</td></tr>
<tr><td>AWS Cloud WAN</td><td>10+ リージョン / セグメント分離</td><td>マネージドのグローバルネットワーク。ポリシー駆動でルート自動伝播</td></tr>
<tr><td>DX Gateway</td><td>オンプレ → 複数リージョン VPC</td><td>1 本の DX で世界中の VPC へ（中国除く）。最大 30 VPC アソシエーション</td></tr></table><br>
<strong>判断フロー:</strong> リージョン数 ≤ 3 かつシンプル → TGW Peering。リージョン数 ≥ 5 / セグメント要件あり → Cloud WAN。オンプレ起点のマルチリージョン → DX Gateway + TGW。<br>
<strong>引っ掛け:</strong>「ALB でマルチリージョン分散」（不可、Route 53/Global Accelerator が正解）、「DX Gateway で TGW 間ルーティング」（不可、TGW Peering 別途必要）、「DX Gateway なしで複数リージョン VPC へ DX」（不可）。"""

# DNS（Route 53 Resolver）の方向
TIPS_DNS_RESOLVER = """<br><br>📌 判断ポイント<br>
<strong>Route 53 Resolver エンドポイントの方向:</strong><br>
<table border='1' cellpadding='4'><tr><th>方向</th><th>エンドポイント</th><th>用途</th></tr>
<tr><td>VPC → オンプレ</td><td>アウトバウンド + 転送ルール</td><td>VPC 内 EC2 が corp.internal を解決</td></tr>
<tr><td>オンプレ → VPC</td><td>インバウンド</td><td>オンプレ DNS から AWS のプライベートホストゾーンを解決</td></tr></table><br>
<strong>引っ掛け:</strong>「インバウンドで VPC からオンプレ解決」「アウトバウンドでオンプレから AWS 解決」は方向が逆。<br>
<strong>マルチアカウント設計:</strong> Shared Services VPC にエンドポイントを集約 → RAM で転送ルールを各メンバー VPC に共有 → 中央集約で運用。"""

# プレフィックスリスト/SG共有の話
TIPS_PREFIX_LIST = """<br><br>📌 判断ポイント<br>
<strong>マルチアカウントで CIDR/SG を集中管理:</strong><br>
<ul>
<li><strong>VPC マネージドプレフィックスリスト + RAM:</strong> CIDR 集合を 1 か所で管理し RAM で組織共有。各 SG/ルートテーブルがリストを参照するため、追加・削除は中央 1 か所で完結。</li>
<li><strong>SG クロスアカウント参照:</strong> 同一 VPC または同一 RAM 共有 VPC 内のみ可能。リージョン跨ぎ・アカウント跨ぎ（共有 VPC 経由を除く）は不可。</li>
</ul>
<strong>引っ掛け:</strong>「Lambda + SNS で全 SG を更新」（運用負荷大、Config 自動修復も検出ラグあり）、「SG 参照でクロスリージョン」（不可）。"""

# Client VPN
TIPS_CLIENT_VPN = """<br><br>📌 判断ポイント<br>
<strong>Client VPN の設計ポイント:</strong><br>
<ul>
<li><strong>1 Client VPN エンドポイント + TGW:</strong> 単一エンドポイントから TGW 経由で全 VPC へ到達。VPC 追加時は TGW アタッチを増やすだけ。</li>
<li><strong>1 Client VPN エンドポイント + VPC Peering:</strong> 既存ピアリングがある小規模構成では十分。ただし推移ルーティング不可なのでピア先のさらに先には到達不可。</li>
<li><strong>認証:</strong> AD (Directory Service) / 証明書相互認証 / SAML フェデレーション の 3 種。</li>
</ul>
<strong>引っ掛け:</strong>「アカウントごとに別 Client VPN」（コスト・運用負荷増）、「Client VPN → VPC A → VPC B（推移）」（不可、TGW 必要）。"""

# PrivateLink
TIPS_PRIVATELINK = """<br><br>📌 判断ポイント<br>
<strong>AWS PrivateLink を選ぶ条件:</strong><br>
<ul>
<li>「インターネット完全非経由」+「他アカウント/SaaS への一方向公開」+「CIDR 重複可」</li>
<li>サービス側: NLB（または GWLB）+ エンドポイントサービス。許可リストで接続先 AWS アカウントを制御。</li>
<li>クライアント側: インターフェイスエンドポイント（VPCe）。プライベート IP で接続、AZ 固有 DNS でクロス AZ 課金回避可能。</li>
</ul>
<strong>引っ掛け:</strong>「ALB をエンドポイントサービスに」（不可、NLB/GWLB のみ）、「PrivateLink で双方向通信」（不可、片方向のみ）、「PrivateLink で NAT エクスポート」（不可）。<br>
<strong>VPC Peering との違い:</strong> PrivateLink は単一サービスのみ公開、Peering は VPC 全体を相互接続。セキュリティ要件次第で選択。"""

# IPv6 / Egress-Only IGW
TIPS_IPV6_EGRESS = """<br><br>📌 判断ポイント<br>
<strong>IPv6 ネットワーク設計:</strong><br>
<ul>
<li>IPv6 はグローバルアドレスのみ（NAT 概念なし）。プライベート相当の制御は <strong>Egress-Only IGW</strong> で実現。</li>
<li>NAT Gateway は IPv4 専用。IPv6 トラフィックを処理しない。</li>
<li>パブリックサブネット = ::/0 を IGW へ / プライベートサブネット = ::/0 を Egress-Only IGW へ。</li>
</ul>
<strong>引っ掛け:</strong>「IPv6 NAT Gateway」（存在しない）、「全サブネットの ::/0 を IGW へ向ける」（プライベートも公開されてしまう）。"""

# DXのコスト・帯域
TIPS_DX_BANDWIDTH = """<br><br>📌 判断ポイント<br>
<strong>Direct Connect の帯域 / 冗長化パターン:</strong><br>
<ul>
<li><strong>Dedicated 接続:</strong> 1/10/100 Gbps（物理ポート占有）。SLA 99.9% は単一、99.99% は別ロケーション 2 本必要。</li>
<li><strong>Hosted 接続（パートナー経由）:</strong> 50 Mbps〜10 Gbps の細かい帯域。短期間でプロビジョニング可能。</li>
<li><strong>VIF 種別:</strong> Private VIF（VPC へ）/ Public VIF（パブリックサービス・VPN over DX）/ Transit VIF（DX Gateway + TGW）</li>
<li><strong>DX Gateway:</strong> 1 本の DX を複数リージョン・複数 VPC へファンアウト（TGW 経由なら 6 リージョン×3 TGW、VGW 経由なら 30 VPC まで）</li>
</ul>
<strong>引っ掛け:</strong>「DX 1 本で SLA 99.99%」（不可、別ロケーション 2 本必要）、「DX Gateway で TGW 間ルーティング」（不可）、「Public VIF で VPC へ直接接続」（不可、Private VIF 必要）。"""

# NAT GWコスト
TIPS_NAT_COST = """<br><br>📌 判断ポイント<br>
<strong>NAT Gateway コスト削減パターン:</strong><br>
<ul>
<li><strong>S3/DynamoDB へのアクセス:</strong> ゲートウェイ型 VPC エンドポイント（無料、データ転送料金もゼロ）</li>
<li><strong>その他 AWS サービス（Kinesis, KMS, ECR 等）:</strong> インターフェイスエンドポイント（時間課金 + データ処理料金、ただし NAT GW より安価）</li>
<li><strong>マルチアカウントの Egress 集約:</strong> 共有 Egress VPC に NAT GW を集約、TGW で全スポークから経由</li>
</ul>
<strong>NAT Gateway 料金内訳:</strong> 時間課金 + データ処理 GB（AZ ごと）。データ量が多い場合 VPC エンドポイント化で大幅削減。<br>
<strong>引っ掛け:</strong>「NAT インスタンスに変更してコスト削減」（管理負荷増、AZ 障害脆弱）、「Flow Logs 分析」（経路は変わらない）。"""

# SCPやガバナンス（あまりネットワーク本体ではないので軽め）
TIPS_GOVERNANCE = """<br><br>📌 判断ポイント<br>
<strong>マルチアカウントネットワークガバナンス:</strong><br>
<ul>
<li><strong>RAM 共有:</strong> TGW、サブネット（VPC Sharing）、プレフィックスリスト、Resolver ルール、ライセンス等</li>
<li><strong>VPC Sharing:</strong> 共有アカウントで VPC を作成 → サブネットを RAM 共有 → メンバーアカウントが EC2/RDS を起動。ネットワーク変更権限はオーナーのみ。</li>
<li><strong>StackSets + Organizations 統合:</strong> 新アカウント作成時に VPC + TGW Attachment を自動展開。手動申請を排除。</li>
</ul>"""

# VPC共有 / RAM
TIPS_VPC_SHARING = """<br><br>📌 判断ポイント<br>
<strong>VPC Sharing（サブネット共有）vs TGW の使い分け:</strong><br>
<table border='1' cellpadding='4'><tr><th>軸</th><th>VPC Sharing (RAM)</th><th>Transit Gateway</th></tr>
<tr><td>同じ CIDR を共有</td><td>○ 同一サブネットに各アカウントが起動</td><td>✕ 各アカウントが別 VPC を持つ</td></tr>
<tr><td>ネットワーク権限</td><td>オーナーアカウントが集中管理</td><td>各アカウントが自 VPC を管理</td></tr>
<tr><td>コスト</td><td>共有リソース（NAT、VGW 等）を 1 つに集約可能</td><td>TGW 時間課金 + データ処理</td></tr>
<tr><td>適用場面</td><td>同一 CIDR 必須、IP 節約、中央 IT 統制</td><td>各アカウントで独立した VPC 設計が必要</td></tr></table><br>
<strong>引っ掛け:</strong>「RAM で VPC 全体共有」（不可、共有可能なのはサブネット単位）、「VPC Sharing でアカウント分離が崩れる」（IAM 制御は維持）。"""

# Network Firewall
TIPS_NETWORK_FIREWALL = """<br><br>📌 判断ポイント<br>
<strong>AWS Network Firewall の使いどころ:</strong><br>
<ul>
<li>マネージド型（HA・自動スケール、AZ あたり最大 100 Gbps スケール）</li>
<li>ステートフル + Suricata 互換ルール（FQDN フィルタ、IDS/IPS 風シグネチャ）</li>
<li>典型構成: 中央 Egress VPC に配置 → 全スポークの 0.0.0.0/0 を TGW 経由で集約 → Firewall エンドポイント経由で NAT GW へ</li>
</ul>
<strong>vs GWLB:</strong> AWS マネージド標準ルール → Network Firewall。サードパーティ製アプライアンス（Palo Alto/Check Point 等）→ GWLB。<br>
<strong>引っ掛け:</strong>「各 VPC に個別 Network Firewall」（コスト高、集約パターンと矛盾）、「OSS プロキシで代替」（運用負荷大）。"""

# Session Manager（一部問題で出てくる）
TIPS_SESSION_MANAGER = """<br><br>📌 判断ポイント<br>
<strong>SSH/RDP 廃止の選択肢:</strong><br>
<ul>
<li><strong>Systems Manager Session Manager:</strong> ポート 22/3389 を一切開放しない、操作ログを S3/CloudWatch Logs に記録、ポートフォワーディング対応、IAM 権限制御。第一候補。</li>
<li><strong>EC2 Instance Connect:</strong> 一時 SSH 鍵を AWS が発行、ポート 22 開放は必要、操作ログなし。</li>
<li><strong>Bastion Host:</strong> 自前管理、SPOF、攻撃面拡大。基本的に避ける。</li>
</ul>"""


# ===========================================================================
# 各問題ごとの「追加内容（カテゴリ）」マッピング
# ===========================================================================
# キー: 問題ID, 値: 追加するティップスのリスト

CATEGORY_MAP = {
    # SSH/Session Manager 系（ネットワーク要件あり）
    'SAP-2':   [TIPS_SESSION_MANAGER],
    'SAP-150': [TIPS_SESSION_MANAGER],
    'UDEMY-215': [TIPS_SESSION_MANAGER],

    # 大規模 TGW + Egress 集約
    'SAP-15':  [TIPS_DX_VS_VPN, TIPS_VPC_SHARING],
    'SAP-21':  [TIPS_HUB_AND_SPOKE, TIPS_PEERING_VS_TGW],
    'SAP-48':  [TIPS_PEERING_VS_TGW, TIPS_HUB_AND_SPOKE],
    'SAP-49':  [TIPS_VPC_SHARING],
    'SAP-61':  [TIPS_HUB_AND_SPOKE, TIPS_PEERING_VS_TGW],
    'SAP-70':  [TIPS_PEERING_VS_TGW],
    'SAP-121': [TIPS_CLIENT_VPN, TIPS_PEERING_VS_TGW],
    'SAP-142': [TIPS_PEERING_VS_TGW],
    'SAP-165': [TIPS_PEERING_VS_TGW],
    'SAP-167': [TIPS_NETWORK_FIREWALL, TIPS_HUB_AND_SPOKE],
    'SAP-181': [TIPS_PREFIX_LIST],
    'SAP-185': [TIPS_PREFIX_LIST],
    'SAP-202': [TIPS_DX_VS_VPN, TIPS_DX_BANDWIDTH, TIPS_PEERING_VS_TGW],
    'SAP-215': [TIPS_PREFIX_LIST],
    'SAP-227': [TIPS_MULTI_REGION, TIPS_PEERING_VS_TGW],
    'SAP-239': [TIPS_PRIVATELINK, TIPS_PEERING_VS_TGW],
    'SAP-252': [TIPS_GOVERNANCE, TIPS_PEERING_VS_TGW],
    'SAP-254': [TIPS_VPC_SHARING],
    'SAP-258': [TIPS_DX_BANDWIDTH, TIPS_GOVERNANCE],
    'SAP-264': [TIPS_DX_VS_VPN],
    'SAP-280': [TIPS_PEERING_VS_TGW],
    'SAP-290': [TIPS_DX_BANDWIDTH, TIPS_DX_VS_VPN],

    # PrivateLink 系
    'SAP-139': [TIPS_PRIVATELINK],
    'SAP-162': [TIPS_PRIVATELINK],
    'SAP-180': [TIPS_PRIVATELINK, TIPS_PEERING_VS_TGW],
    'SAP-222': [TIPS_PRIVATELINK],

    # DNS Resolver 系
    'SAP-54':  [TIPS_DNS_RESOLVER],
    'SAP-78':  [TIPS_DNS_RESOLVER],
    'SAP-223': [TIPS_DNS_RESOLVER],

    # マルチリージョン系
    'SAP-106': [TIPS_MULTI_REGION, TIPS_DX_BANDWIDTH],

    # NAT Gateway / Endpoints コスト
    'SAP-108': [TIPS_NAT_COST],
    'SAP-116': [TIPS_NAT_COST],
    'SAP-207': [TIPS_NAT_COST],
    'SAP-279': [TIPS_NAT_COST],
    'SAP-288': [TIPS_PRIVATELINK, TIPS_NAT_COST],

    # NAT/EIP/BYOIP
    'SAP-73':  [TIPS_NAT_COST],
    'SAP-112': [TIPS_NAT_COST],
    'SAP-191': [TIPS_NAT_COST],

    # IPv6 / Egress-Only IGW
    'SAP-196': [TIPS_IPV6_EGRESS],

    # VPC + サブネット拡張
    'SAP-84':  [],  # 純粋 VPC 操作。判断ポイント追加で混乱招く

    # その他多めに加筆
    'SAP-104': [TIPS_DX_BANDWIDTH],
    'SAP-178': [TIPS_CLIENT_VPN],  # 後で詳細修正
    'SAP-200': [TIPS_NAT_COST],
    'SAP-232': [TIPS_DX_VS_VPN],

    # UDEMY系
    'UDEMY-005': [TIPS_DX_BANDWIDTH],
    'UDEMY-006': [TIPS_DX_VS_VPN, TIPS_MULTI_REGION, TIPS_PEERING_VS_TGW],
    'UDEMY-021': [TIPS_HUB_AND_SPOKE, TIPS_PEERING_VS_TGW],
    'UDEMY-022': [],
    'UDEMY-049': [TIPS_PEERING_VS_TGW],
    'UDEMY-052': [TIPS_DNS_RESOLVER],
    'UDEMY-053': [TIPS_PEERING_VS_TGW],
    'UDEMY-057': [TIPS_DX_VS_VPN, TIPS_PRIVATELINK],
    'UDEMY-066': [],
    'UDEMY-067': [],
    'UDEMY-076': [],
    'UDEMY-087': [TIPS_NETWORK_FIREWALL, TIPS_HUB_AND_SPOKE],
    'UDEMY-090': [TIPS_PEERING_VS_TGW],
    'UDEMY-093': [TIPS_SESSION_MANAGER],
    'UDEMY-096': [TIPS_DNS_RESOLVER],
    'UDEMY-099': [],
    'UDEMY-105': [],
    'UDEMY-107': [],
    'UDEMY-113': [],
    'UDEMY-114': [TIPS_PEERING_VS_TGW, TIPS_HUB_AND_SPOKE],
    'UDEMY-119': [TIPS_MULTI_REGION],
    'UDEMY-133': [],
    'UDEMY-135': [TIPS_PRIVATELINK, TIPS_MULTI_REGION],
    'UDEMY-139': [TIPS_IPV6_EGRESS],
    'UDEMY-143': [TIPS_CLIENT_VPN],
    'UDEMY-149': [TIPS_DX_VS_VPN],
    'UDEMY-153': [TIPS_NAT_COST],
    'UDEMY-162': [TIPS_PRIVATELINK],
    'UDEMY-167': [TIPS_DX_BANDWIDTH, TIPS_MULTI_REGION],
    'UDEMY-170': [TIPS_PRIVATELINK],
    'UDEMY-171': [],
    'UDEMY-180': [TIPS_GOVERNANCE, TIPS_PEERING_VS_TGW],
    'UDEMY-185': [],
    'UDEMY-190': [TIPS_NAT_COST],
    'UDEMY-197': [TIPS_NAT_COST],
    'UDEMY-203': [TIPS_PREFIX_LIST],
    'UDEMY-206': [TIPS_NAT_COST],
    'UDEMY-219': [TIPS_MULTI_REGION],
    'UDEMY-227': [TIPS_PEERING_VS_TGW],
    'UDEMY-242': [],
    'UDEMY-248': [TIPS_CLIENT_VPN, TIPS_PEERING_VS_TGW],
    'UDEMY-263': [],
    'UDEMY-264': [TIPS_NAT_COST],
    'UDEMY-265': [TIPS_DX_BANDWIDTH, TIPS_MULTI_REGION],
    'UDEMY-267': [TIPS_GOVERNANCE, TIPS_HUB_AND_SPOKE],
    'UDEMY-270': [TIPS_NETWORK_FIREWALL],
    'UDEMY-272': [TIPS_DX_BANDWIDTH, TIPS_GOVERNANCE],
    'UDEMY-277': [TIPS_PEERING_VS_TGW],
    'UDEMY-287': [],
    'UDEMY-297': [],
    'UDEMY-310': [],
    'UDEMY-321': [TIPS_PRIVATELINK, TIPS_PEERING_VS_TGW],
    'UDEMY-330': [TIPS_PEERING_VS_TGW, TIPS_GOVERNANCE],
    'UDEMY-337': [],
    'UDEMY-347': [TIPS_DX_BANDWIDTH, TIPS_MULTI_REGION],
    'UDEMY-352': [TIPS_DX_VS_VPN],
    'UDEMY-361': [],
    'UDEMY-364': [TIPS_DX_VS_VPN, TIPS_VPC_SHARING],
    'UDEMY-365': [TIPS_NETWORK_FIREWALL, TIPS_HUB_AND_SPOKE],
    'UDEMY-367': [TIPS_PRIVATELINK],
    'UDEMY-128': [],
    'UDEMY-029': [],
    'UDEMY-038': [TIPS_NAT_COST],
    'UDEMY-043': [TIPS_NAT_COST],
    'UDEMY-060': [],
    'UDEMY-123': [],
    'UDEMY-238': [],
    'UDEMY-239': [],
    'UDEMY-004': [TIPS_PRIVATELINK],
}

# ===========================================================================
# 明示的に detail を上書きするケース（誤り修正）
# ===========================================================================

DETAIL_OVERRIDES = {
    # SAP-178: PERSPECTIVE と DETAIL が完全に的外れ（CloudFront/S3/ALB の話に
    # なっているが、設問は「VPN 経由 + MFA + AD ベースで隔離環境にアクセス」）
    'SAP-178': {
        'perspective': '機密ワークロードへのアクセスを VPN 経由 + MFA に限定し、既存 AD 認証を活かしてスケールさせるには？',
        'detail': """<b>判断の決め手：</b>「<b>VPN 経由のみアクセス</b>」+「<b>MFA 強制</b>」+「<b>既存 Windows AD 認証を活かす</b>」+「<b>マネージドで自動スケール</b>」。AWS Client VPN + AD 認証 + MFA が唯一の構成。<br><br><b>正解 A：</b>AWS Client VPN エンドポイントを作成し、認証方式に AWS Directory Service (AD Connector or Managed AD) を指定。AD 側で MFA 連携（RADIUS）を構成。Client VPN はマネージドで自動スケールし、エンドポイント単位でルートと認可ルールを集中管理できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>◎ Client VPN + AD 統合認証 + MFA。マネージドで自動スケールし、既存 AD のグループ制御をそのまま流用可能</td></tr><tr><td>B</td><td>EC2 ベースの自前 VPN サーバーは管理負荷大、SPOF、自動スケール困難</td></tr><tr><td>C</td><td>Site-to-Site VPN は拠点間接続用。個別ユーザー認証や MFA 強制には不適</td></tr><tr><td>D</td><td>パブリックエンドポイント直公開は「VPN 経由でのみ」要件に違反</td></tr></table>"""
    },
    # UDEMY-180: 「ピアリングトランジットゲートウェイアタッチメント」が
    # 存在しないという誤った断定がある。実際にはTGW Peering Attachmentは存在する。
    # ただし、選択肢Dの問題は「TGWサービスリンクロールでアカウント間共有」が誤り。
    'UDEMY-180': {
        'perspective': 'CloudFormation StackSets を使ってマルチアカウント・マルチリージョンにネットワークを一括展開する方法をどう判断するか？',
        'detail': """<p><strong>A. 管理アカウントから、AWS Resource Access Manager を使用してメンバーアカウントとトランジットゲートウェイを共有します。</strong></p><p>AWS Resource Access Manager (RAM) を使用すると、トランジットゲートウェイのようなリソースを AWS アカウント間で共有できる。管理アカウントからトランジットゲートウェイを共有することで、メンバーアカウントは共有されたトランジットゲートウェイに VPC を接続できる。</p><p><br></p><p><strong>C. 管理アカウントから AWS CloudFormation StackSet を起動し、メンバーアカウントに新しい VPC と VPC トランジットゲートウェイアタッチメントを自動的に作成します。トランジットゲートウェイ ID を使用して、管理アカウントのトランジットゲートウェイにアタッチメントを関連付けます。</strong></p><p>AWS CloudFormation StackSets を使用すると、複数の AWS アカウントとリージョンにまたがる CloudFormation スタックをデプロイできる。管理アカウントから StackSet を使用して、新しい VPC とトランジットゲートウェイアタッチメントを自動的に作成し、これらをトランジットゲートウェイに接続できる。</p><p><br></p><p><strong>他の選択肢：</strong></p><p><strong>B. 管理アカウントから、AWS Organizations SCP を使用してメンバーアカウントとトランジットゲートウェイを共有します。</strong></p><p>SCP は組織内のアカウントの最大許可（ガードレール）を定義するためのものであり、リソースを共有する機能はない。リソース共有には RAM を使う。</p><p><br></p><p><strong>D. 管理アカウントから AWS CloudFormation StackSet を起動し、メンバーアカウントに新しい VPC とピアリングトランジットゲートウェイアタッチメントを自動的に作成します。トランジットゲートウェイサービスリンクロールを使用して、管理アカウントのトランジットゲートウェイとアタッチメントを共有します。</strong></p><p>本問の要件は「同一の TGW にメンバー VPC を接続する」ことなので、必要なのは <strong>VPC アタッチメント</strong>であり、ピアリングアタッチメントではない（TGW Peering Attachment 自体は実在するが、リージョン間 TGW 接続用で本問とは用途が異なる）。また「サービスリンクロールで共有する」という記述も誤りで、クロスアカウントでの TGW 共有は <strong>RAM</strong> で行う。</p><p><br></p><p><strong>E. 管理アカウントから、AWS Service Catalog を使用してメンバーアカウントとトランジットゲートウェイを共有します。</strong></p><p>AWS Service Catalog は承認済み IT サービスのカタログを管理するためのサービスである。リソース共有自体には RAM を使うのが正しい。</p><p><br></p><p><strong>参考 URL:</strong></p><p>https://docs.aws.amazon.com/ram/latest/userguide/what-is.html</p><p>https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html</p><p>https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-concepts.html</p>"""
    },
    # UDEMY-149: NAT GW を 2 つ持つ意義が説明不足。レプリケーションサーバーの
    # アウトバウンド通信用に NAT GW が必要。
    'UDEMY-149': {
        'perspective': 'Elastic Disaster Recovery でオンプレからのレプリケーションをパブリックインターネット非経由にし、帯域も制御するには？',
        'detail': """<p><strong>A. 少なくとも 2 つのプライベートサブネット、2 つの NAT ゲートウェイ、および仮想プライベートゲートウェイを持つ VPC を AWS 上に作成する。</strong></p><p>レプリケーションサーバー（DRS が AWS 側に自動展開する EC2）はプライベートサブネットに配置し、外部から直接到達不可とする。一方で、これらのサーバーは AWS DRS のコントロールプレーン（パブリックエンドポイント）に接続する必要があるため、NAT Gateway 経由のアウトバウンドが必要となる（または DRS 用の VPC エンドポイント構成）。AZ 障害対策で NAT GW は 2 つ。仮想プライベートゲートウェイ（VGW）は次項の Direct Connect / VPN を VPC へ収容するために必要。</p><p><br></p><p><strong>D. オンプレミスネットワークと AWS のターゲットネットワーク間に AWS Direct Connect 接続と Direct Connect ゲートウェイを設定する。</strong></p><p>Direct Connect は専用線でレプリケーションを「インターネット非経由」にする。さらに帯域が確保されているため、他業務トラフィックを圧迫しない。Direct Connect Gateway は将来のリージョン追加にも対応。</p><p><br></p><p><strong>E. AWS Elastic Disaster Recovery のレプリケーションサーバーの設定時に、データレプリケーションにプライベート IP アドレスを使用するオプションを選択する。</strong></p><p>このオプションにより、レプリケーショントラフィックがインターネット経由（パブリック IP）ではなく、プライベートネットワーク経路（DX/VPN）を通過することが保証される。デフォルトはパブリック IP 経由なので、明示的に設定が必要。</p><p><br></p><p><strong>他の選択肢：</strong></p><p><strong>B. 少なくとも 2 つのパブリックサブネット、仮想プライベートゲートウェイ、およびインターネットゲートウェイを持つ VPC を AWS 上に作成する。</strong></p><p>パブリックサブネット + IGW はリカバリ後のサーバーをインターネットに露出する設計であり、要件に反する。</p><p><br></p><p><strong>C. オンプレミスネットワークと AWS のターゲットネットワーク間に AWS Site-to-Site VPN 接続を確立する。</strong></p><p>VPN はパブリックインターネットを暗号化して通過するため、「インターネット非経由」要件を満たさない。また帯域も Direct Connect ほど安定せず、他業務帯域を圧迫する可能性がある。</p><p><br></p><p><strong>F. ターゲットサーバーの起動設定時に、復旧インスタンスのプライベート IP アドレスがソースサーバーのプライベート IP アドレスと一致することを確認するオプションを選択する。</strong></p><p>これは復旧後の IP 一致設定であり、レプリケーション経路のセキュリティ要件には無関係。</p><p><br></p><p><strong>参考 URL:</strong></p><p>https://docs.aws.amazon.com/drs/latest/userguide/Network-Requirements.html</p><p>https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html</p>"""
    },
    # UDEMY-270: 解説末尾に「選択肢DとEの組み合わせも正答」と書かれており
    # 利用者を混乱させる。これは削除し、解説を整える
    'UDEMY-270': {
        'perspective': 'アプリの全インバウンド/アウトバウンドトラフィックに透過的にセキュリティ検査ツールを挟み込むには何を使うか？',
        'detail': """<p><strong>A. 既存の VPC に新しい Auto Scaling グループでセキュリティツールを EC2 インスタンスにデプロイします。</strong></p><p>セキュリティツールを Auto Scaling グループ内の EC2 インスタンスにデプロイすることで、スケーラビリティと高可用性を確保する。</p><p><br></p><p><strong>D. 各アベイラビリティゾーンに Gateway Load Balancer をプロビジョニングし、トラフィックをセキュリティツールにリダイレクトします。</strong></p><p>Gateway Load Balancer（GWLB）は、ファイアウォール・IDS/IPS・パケット検査などのサードパーティ仮想アプライアンスを透過的に挿入するための L3 ロードバランサーである。GWLB エンドポイント（GWLBe）をルートテーブルの next-hop に指定することで、すべての IP プロトコル・ポートのトラフィックがアプライアンスを通過する。GENEVE プロトコルでカプセル化され、フローアフィニティが保たれるためアプライアンス側でステートフル検査が可能。</p><p><br></p><p><strong>他の選択肢：</strong></p><p><strong>B. Web アプリケーションを Network Load Balancer の背後にデプロイします。</strong></p><p>NLB は L4 のロードバランサーであり、トラフィックを「セキュリティツールに迂回させる」ような透過挿入はできない。</p><p><br></p><p><strong>C. セキュリティツールのインスタンスの前に Application Load Balancer をデプロイします。</strong></p><p>ALB は L7（HTTP/HTTPS）専用。問題文は「すべてのパケットを検査」と要求しており、L7 以外のプロトコルを扱えない ALB は不適。</p><p><br></p><p><strong>E. VPC 間の通信を容易にするためにトランジットゲートウェイをプロビジョニングします。</strong></p><p>TGW は VPC・VPN・DX を相互接続するルーティングサービスであり、パケット検査機能は持たない。検査アプライアンスの透過挿入には GWLB が必要。</p><p><br></p><p><strong>参考 URL：</strong></p><p>https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html</p>"""
    },
    # UDEMY-119: タイトル(perspective)と内容が「Active-Active」と「Active-Passive」で食い違っている
    # → 問題自体は active-passive (DR) なので perspective を修正
    'UDEMY-219': {
        'perspective': 'マルチリージョンのアクティブ-パッシブ DR 構成で Route 53 フェイルオーバーをどう設計するか？',
        'detail': None,  # detailは保持
    },
    # UDEMY-128: title says "active-active" but problem is "active-passive"
    'UDEMY-128': None,
}


# ===========================================================================
# 実行
# ===========================================================================

def append_tips(detail: str, tips_list: list) -> str:
    """detail の末尾に tips_list を結合"""
    if not tips_list:
        return detail
    # 重複防止: 各 tip ブロックの冒頭シグネチャで個別チェック
    pieces_to_add = []
    for tip in tips_list:
        # 各ティップスの冒頭から判定キーワードを抜き出して重複チェック
        # 例: "<strong>VPC Peering vs Transit Gateway の使い分け（最重要）:</strong>"
        # など、各 TIP に固有のフレーズで重複検出
        signatures = {
            'VPC Peering vs Transit Gateway': '<strong>VPC Peering vs Transit Gateway',
            'Direct Connect vs Site-to-Site VPN': '<strong>Direct Connect vs Site-to-Site VPN',
            'Hub-and-Spoke / Egress 集約': '<strong>Hub-and-Spoke / Egress 集約',
            'マルチリージョン接続の選択肢': '<strong>マルチリージョン接続の選択肢',
            'Route 53 Resolver エンドポイントの方向': '<strong>Route 53 Resolver エンドポイントの方向',
            'マルチアカウントで CIDR/SG を集中管理': '<strong>マルチアカウントで CIDR/SG を集中管理',
            'Client VPN の設計ポイント': '<strong>Client VPN の設計ポイント',
            'AWS PrivateLink を選ぶ条件': '<strong>AWS PrivateLink を選ぶ条件',
            'IPv6 ネットワーク設計': '<strong>IPv6 ネットワーク設計',
            'Direct Connect の帯域 / 冗長化パターン': '<strong>Direct Connect の帯域 / 冗長化パターン',
            'NAT Gateway コスト削減パターン': '<strong>NAT Gateway コスト削減パターン',
            'マルチアカウントネットワークガバナンス': '<strong>マルチアカウントネットワークガバナンス',
            'VPC Sharing（サブネット共有）vs TGW': '<strong>VPC Sharing（サブネット共有）vs TGW',
            'AWS Network Firewall の使いどころ': '<strong>AWS Network Firewall の使いどころ',
            'SSH/RDP 廃止の選択肢': '<strong>SSH/RDP 廃止の選択肢',
        }
        # tip 内に存在するシグネチャを探し、それが detail に既出ならスキップ
        skip = False
        for key, sig in signatures.items():
            if sig in tip:
                # 該当するシグネチャを持つ tip
                if sig in detail:
                    skip = True
                break
        if not skip:
            pieces_to_add.append(tip)
    if not pieces_to_add:
        return detail
    return detail + ''.join(pieces_to_add)


def main():
    # ファイル再読込（書き込み直前）
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    target_ids = set(CATEGORY_MAP.keys()) | set(DETAIL_OVERRIDES.keys())
    print(f"Target questions: {len(target_ids)}")

    modified_count = 0
    appended_count = 0
    overridden_count = 0

    for q in data:
        qid = q['id']
        if qid not in target_ids:
            continue

        original_detail = q['explanation'].get('detail', '')
        original_perspective = q['explanation'].get('perspective', '')
        new_detail = original_detail
        new_perspective = original_perspective

        # 1. detail オーバーライド（誤り修正）
        if qid in DETAIL_OVERRIDES:
            override = DETAIL_OVERRIDES[qid]
            if override is not None:
                if 'perspective' in override and override['perspective']:
                    new_perspective = override['perspective']
                if 'detail' in override and override['detail']:
                    new_detail = override['detail']
                overridden_count += 1

        # 2. 判断ポイントの追記
        tips = CATEGORY_MAP.get(qid, [])
        if tips:
            updated = append_tips(new_detail, tips)
            if updated != new_detail:
                new_detail = updated
                appended_count += 1

        # 変更があった場合のみ反映
        if new_detail != original_detail or new_perspective != original_perspective:
            q['explanation']['detail'] = new_detail
            q['explanation']['perspective'] = new_perspective
            modified_count += 1

    # JSON valid 性チェックの代わりに json.dumps で直列化テスト
    json_str = json.dumps(data, ensure_ascii=False, indent=2)

    # バックアップ
    backup_path = QUESTIONS_PATH + '.bak.network'
    if not os.path.exists(backup_path):
        with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
            with open(backup_path, 'w', encoding='utf-8') as bf:
                bf.write(f.read())
        print(f"Backup created: {backup_path}")

    # 書き込み
    with open(QUESTIONS_PATH, 'w', encoding='utf-8') as f:
        f.write(json_str)

    print(f"\n=== Summary ===")
    print(f"Total target questions: {len(target_ids)}")
    print(f"Modified questions: {modified_count}")
    print(f"  - Detail overridden (corrections): {overridden_count}")
    print(f"  - Tips appended (additions): {appended_count}")


if __name__ == '__main__':
    main()
