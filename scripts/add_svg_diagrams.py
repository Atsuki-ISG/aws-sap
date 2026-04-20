#!/usr/bin/env python3
"""
AWS SAP 問題集の explanation.detail に構成図 SVG を追加するスクリプト。

方針:
  - 優先度が高いカテゴリから処理
  - トピックごとにテンプレート化された SVG を生成（キーワードベースで判定）
  - 冪等性: `<!-- svg_added -->` マーカーでスキップ判定
  - 10問ごとに保存（中断可能）

カテゴリとテンプレート:
  1. Multi-region DR (Primary/Secondary + レプリケーション)
  2. Multi-account (Organizations + OU + Member accounts)
  3. Network TGW/VPC (Transit Gateway Hub-Spoke)
  4. Hybrid DX/VPN (On-prem <-> DX/VPN <-> VPC)
  5. VPC Endpoints (Interface/Gateway EP)
  6. Data Pipeline (Source -> Kinesis/Firehose -> S3 -> Athena)
  7. Event Driven (EventBridge/SQS/SNS fan-out)
  8. API Architecture (CloudFront/APIGW/Lambda/DB)
  9. Storage Lifecycle (S3 Standard -> IA -> Glacier)
  10. Container Network (ECS/EKS + ALB + Backend)
"""
import json
import re
from pathlib import Path

JSON_PATH = Path('/Users/aki/aws-sap/docs/data/questions.json')
MARKER = '<!-- svg_added -->'

# ----------------- SVG defs helper -----------------
ARROW_DEFS = (
    '<defs>'
    '<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
    '<path d="M0,0 L10,5 L0,10 Z" fill="#666"/>'
    '</marker>'
    '<marker id="arrRed" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
    '<path d="M0,0 L10,5 L0,10 Z" fill="#DD344C"/>'
    '</marker>'
    '<marker id="arrGreen" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
    '<path d="M0,0 L10,5 L0,10 Z" fill="#7AA116"/>'
    '</marker>'
    '</defs>'
)


def svg_wrap(title, inner, viewbox="0 0 700 320"):
    """Return HTML snippet wrapping the SVG with the constituent marker."""
    return (
        f'<div style="margin-top:16px;">{MARKER}<strong>構成図: {title}</strong><br>'
        f'<svg viewBox="{viewbox}" xmlns="http://www.w3.org/2000/svg" '
        f'style="max-width:100%;height:auto;background:#fff;border:1px solid #ccc;border-radius:6px;margin-top:6px;">'
        f'{ARROW_DEFS}{inner}</svg></div>'
    )


# ----------------- SVG templates -----------------

def svg_multi_region_dr():
    inner = (
        # Title
        '<text x="350" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#232F3E">マルチリージョン DR 構成</text>'
        # Primary region box
        '<rect x="20" y="40" width="300" height="250" fill="#EBF1FF" stroke="#3B48CC" stroke-width="2" rx="8"/>'
        '<text x="170" y="60" text-anchor="middle" font-size="12" font-weight="bold" fill="#3B48CC">Primary Region (ap-northeast-1)</text>'
        # Primary app
        '<rect x="50" y="80" width="110" height="50" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="4"/>'
        '<text x="105" y="100" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Application</text>'
        '<text x="105" y="115" text-anchor="middle" font-size="10" fill="#666">EC2/ECS/Lambda</text>'
        # Primary DB
        '<rect x="180" y="80" width="120" height="50" fill="#EBF5E8" stroke="#7AA116" stroke-width="2" rx="4"/>'
        '<text x="240" y="100" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Aurora / RDS</text>'
        '<text x="240" y="115" text-anchor="middle" font-size="10" fill="#666">(Primary Writer)</text>'
        # Primary S3
        '<rect x="50" y="160" width="110" height="50" fill="#EBF5E8" stroke="#7AA116" stroke-width="2" rx="4"/>'
        '<text x="105" y="180" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">S3 Bucket</text>'
        '<text x="105" y="195" text-anchor="middle" font-size="10" fill="#666">primary data</text>'
        # Route53
        '<rect x="180" y="160" width="120" height="50" fill="#FCE7F3" stroke="#E7157B" stroke-width="2" rx="4"/>'
        '<text x="240" y="180" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Route 53</text>'
        '<text x="240" y="195" text-anchor="middle" font-size="10" fill="#666">Failover Routing</text>'
        # Secondary region box
        '<rect x="360" y="40" width="320" height="250" fill="#FEF3F2" stroke="#DD344C" stroke-width="2" rx="8"/>'
        '<text x="520" y="60" text-anchor="middle" font-size="12" font-weight="bold" fill="#DD344C">Secondary Region (us-west-2)</text>'
        # Secondary app
        '<rect x="390" y="80" width="110" height="50" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" stroke-dasharray="4,2" rx="4"/>'
        '<text x="445" y="100" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Standby App</text>'
        '<text x="445" y="115" text-anchor="middle" font-size="10" fill="#666">(Warm/Pilot Light)</text>'
        # Secondary DB
        '<rect x="520" y="80" width="140" height="50" fill="#EBF5E8" stroke="#7AA116" stroke-width="2" rx="4"/>'
        '<text x="590" y="100" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Aurora Replica</text>'
        '<text x="590" y="115" text-anchor="middle" font-size="10" fill="#666">(Global DB)</text>'
        # Secondary S3
        '<rect x="390" y="160" width="110" height="50" fill="#EBF5E8" stroke="#7AA116" stroke-width="2" rx="4"/>'
        '<text x="445" y="180" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">S3 Bucket</text>'
        '<text x="445" y="195" text-anchor="middle" font-size="10" fill="#666">(CRR destination)</text>'
        # Replication arrows
        '<line x1="300" y1="105" x2="520" y2="105" stroke="#7AA116" stroke-width="2" marker-end="url(#arrGreen)"/>'
        '<text x="410" y="98" text-anchor="middle" font-size="10" fill="#7AA116">DB replication</text>'
        '<line x1="160" y1="185" x2="390" y2="185" stroke="#7AA116" stroke-width="2" marker-end="url(#arrGreen)"/>'
        '<text x="275" y="178" text-anchor="middle" font-size="10" fill="#7AA116">S3 CRR</text>'
        # Users
        '<text x="350" y="260" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">User DNS: Route 53 ヘルスチェック失敗 → Secondary へ切替</text>'
        '<text x="350" y="278" text-anchor="middle" font-size="10" fill="#666">RTO: 分〜時間 / RPO: 秒〜分（設計依存）</text>'
    )
    return svg_wrap('マルチリージョン DR', inner)


def svg_multi_account():
    inner = (
        '<text x="350" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#232F3E">AWS Organizations マルチアカウント構成</text>'
        # Management account
        '<rect x="250" y="40" width="200" height="55" fill="#FCE7F3" stroke="#E7157B" stroke-width="2" rx="6"/>'
        '<text x="350" y="62" text-anchor="middle" font-size="12" font-weight="bold" fill="#232F3E">Management Account</text>'
        '<text x="350" y="80" text-anchor="middle" font-size="10" fill="#666">Organizations / SCP / 請求統合</text>'
        # OUs
        '<line x1="200" y1="125" x2="350" y2="95" stroke="#666" stroke-width="1.5"/>'
        '<line x1="500" y1="125" x2="350" y2="95" stroke="#666" stroke-width="1.5"/>'
        # Security OU
        '<rect x="30" y="125" width="180" height="45" fill="#FEF3F2" stroke="#DD344C" stroke-width="2" rx="6"/>'
        '<text x="120" y="145" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Security OU</text>'
        '<text x="120" y="160" text-anchor="middle" font-size="10" fill="#666">Log Archive / Audit</text>'
        # Workload OU
        '<rect x="250" y="125" width="200" height="45" fill="#EBF1FF" stroke="#3B48CC" stroke-width="2" rx="6"/>'
        '<text x="350" y="145" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Workload OU</text>'
        '<text x="350" y="160" text-anchor="middle" font-size="10" fill="#666">Prod / Dev / Staging</text>'
        # Shared OU
        '<rect x="490" y="125" width="180" height="45" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="6"/>'
        '<text x="580" y="145" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Shared Services OU</text>'
        '<text x="580" y="160" text-anchor="middle" font-size="10" fill="#666">Network / DNS / AD</text>'
        # Accounts under Workload OU
        '<rect x="260" y="200" width="80" height="40" fill="#FFF" stroke="#3B48CC" stroke-width="1.5" rx="4"/>'
        '<text x="300" y="220" text-anchor="middle" font-size="10" font-weight="bold" fill="#232F3E">Prod Acc</text>'
        '<text x="300" y="234" text-anchor="middle" font-size="9" fill="#666">VPC / 本番</text>'
        '<rect x="355" y="200" width="80" height="40" fill="#FFF" stroke="#3B48CC" stroke-width="1.5" rx="4"/>'
        '<text x="395" y="220" text-anchor="middle" font-size="10" font-weight="bold" fill="#232F3E">Dev Acc</text>'
        '<text x="395" y="234" text-anchor="middle" font-size="9" fill="#666">VPC / 開発</text>'
        # Connector
        '<line x1="350" y1="170" x2="300" y2="200" stroke="#666" stroke-width="1"/>'
        '<line x1="350" y1="170" x2="395" y2="200" stroke="#666" stroke-width="1"/>'
        # SCP arrow
        '<path d="M 350 95 Q 120 100 120 125" fill="none" stroke="#DD344C" stroke-width="1.5" stroke-dasharray="3,2" marker-end="url(#arrRed)"/>'
        '<text x="180" y="108" font-size="9" fill="#DD344C">SCP 適用</text>'
        # Legend
        '<text x="350" y="275" text-anchor="middle" font-size="10" fill="#666">管理: Control Tower / AFT / Identity Center (SSO)</text>'
        '<text x="350" y="293" text-anchor="middle" font-size="10" fill="#666">集約: CloudTrail Organization Trail / Config Aggregator / GuardDuty 委任管理</text>'
    )
    return svg_wrap('マルチアカウント (Organizations + OU)', inner)


def svg_transit_gateway():
    inner = (
        '<text x="350" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#232F3E">Transit Gateway Hub-and-Spoke 構成</text>'
        # TGW center
        '<rect x="280" y="130" width="140" height="60" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="8"/>'
        '<text x="350" y="155" text-anchor="middle" font-size="12" font-weight="bold" fill="#232F3E">Transit Gateway</text>'
        '<text x="350" y="172" text-anchor="middle" font-size="10" fill="#666">(中心ハブ)</text>'
        '<text x="350" y="185" text-anchor="middle" font-size="9" fill="#666">Route Tables で分離</text>'
        # VPC A
        '<rect x="40" y="50" width="140" height="60" fill="#EBF1FF" stroke="#3B48CC" stroke-width="2" rx="6"/>'
        '<text x="110" y="72" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">VPC A (Prod)</text>'
        '<text x="110" y="90" text-anchor="middle" font-size="10" fill="#666">10.0.0.0/16</text>'
        # VPC B
        '<rect x="40" y="210" width="140" height="60" fill="#EBF1FF" stroke="#3B48CC" stroke-width="2" rx="6"/>'
        '<text x="110" y="232" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">VPC B (Dev)</text>'
        '<text x="110" y="250" text-anchor="middle" font-size="10" fill="#666">10.1.0.0/16</text>'
        # VPC C
        '<rect x="520" y="50" width="140" height="60" fill="#EBF1FF" stroke="#3B48CC" stroke-width="2" rx="6"/>'
        '<text x="590" y="72" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">VPC C (Shared)</text>'
        '<text x="590" y="90" text-anchor="middle" font-size="10" fill="#666">10.2.0.0/16</text>'
        # On-prem
        '<rect x="520" y="210" width="140" height="60" fill="#F5F5F5" stroke="#232F3E" stroke-width="2" rx="6"/>'
        '<text x="590" y="232" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">On-premises</text>'
        '<text x="590" y="250" text-anchor="middle" font-size="10" fill="#666">DX / VPN 経由</text>'
        # Arrows (bidirectional shown as lines with two markers via two lines each)
        '<line x1="180" y1="80" x2="280" y2="140" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="280" y1="160" x2="180" y2="240" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="420" y1="140" x2="520" y2="80" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="520" y1="240" x2="420" y2="170" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<text x="230" y="115" font-size="9" fill="#666">attach</text>'
        '<text x="455" y="115" font-size="9" fill="#666">attach</text>'
        '<text x="455" y="218" font-size="9" fill="#666">DX/VPN attach</text>'
    )
    return svg_wrap('Transit Gateway Hub-and-Spoke', inner)


def svg_hybrid_dx_vpn():
    inner = (
        '<text x="350" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#232F3E">ハイブリッド接続 (DX / VPN)</text>'
        # On-prem
        '<rect x="30" y="90" width="170" height="120" fill="#F5F5F5" stroke="#232F3E" stroke-width="2" rx="6"/>'
        '<text x="115" y="115" text-anchor="middle" font-size="12" font-weight="bold" fill="#232F3E">On-premises</text>'
        '<rect x="50" y="130" width="130" height="30" fill="#FFF" stroke="#666" rx="4"/>'
        '<text x="115" y="150" text-anchor="middle" font-size="10" fill="#232F3E">Customer Router</text>'
        '<rect x="50" y="170" width="130" height="30" fill="#FFF" stroke="#666" rx="4"/>'
        '<text x="115" y="190" text-anchor="middle" font-size="10" fill="#232F3E">Servers / Database</text>'
        # DX / VPN path
        '<rect x="240" y="60" width="220" height="50" fill="#FEF3F2" stroke="#DD344C" stroke-width="2" rx="6"/>'
        '<text x="350" y="82" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Direct Connect</text>'
        '<text x="350" y="100" text-anchor="middle" font-size="10" fill="#666">専用線 / 低レイテンシ (Primary)</text>'
        '<rect x="240" y="130" width="220" height="50" fill="#FEF3F2" stroke="#DD344C" stroke-width="2" stroke-dasharray="4,2" rx="6"/>'
        '<text x="350" y="152" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Site-to-Site VPN</text>'
        '<text x="350" y="170" text-anchor="middle" font-size="10" fill="#666">Internet 経由 (Backup / IPsec)</text>'
        # DXGW / TGW
        '<rect x="240" y="200" width="220" height="40" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="6"/>'
        '<text x="350" y="225" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Direct Connect Gateway / Transit Gateway</text>'
        # AWS VPC
        '<rect x="500" y="90" width="170" height="120" fill="#EBF1FF" stroke="#3B48CC" stroke-width="2" rx="6"/>'
        '<text x="585" y="115" text-anchor="middle" font-size="12" font-weight="bold" fill="#232F3E">AWS VPC</text>'
        '<rect x="520" y="130" width="130" height="30" fill="#FFF" stroke="#666" rx="4"/>'
        '<text x="585" y="150" text-anchor="middle" font-size="10" fill="#232F3E">Private Subnet</text>'
        '<rect x="520" y="170" width="130" height="30" fill="#FFF" stroke="#666" rx="4"/>'
        '<text x="585" y="190" text-anchor="middle" font-size="10" fill="#232F3E">RDS / EC2 / EKS</text>'
        # Arrows
        '<line x1="200" y1="85" x2="240" y2="85" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="460" y1="85" x2="500" y2="130" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="200" y1="155" x2="240" y2="155" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="460" y1="155" x2="500" y2="160" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        # Legend
        '<text x="350" y="265" text-anchor="middle" font-size="10" fill="#666">DX: 専用線・安定した帯域／VPN: インターネット経由・迅速構築・DR用途に最適</text>'
        '<text x="350" y="282" text-anchor="middle" font-size="10" fill="#666">BGP で経路広告 / DXGW 経由で複数リージョンの VPC へ接続可</text>'
    )
    return svg_wrap('ハイブリッド接続 (DX/VPN)', inner)


def svg_vpc_endpoints():
    inner = (
        '<text x="350" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#232F3E">VPC Endpoints (Gateway / Interface)</text>'
        # VPC box
        '<rect x="30" y="50" width="420" height="240" fill="#EBF1FF" stroke="#3B48CC" stroke-width="2" rx="8"/>'
        '<text x="240" y="72" text-anchor="middle" font-size="12" font-weight="bold" fill="#3B48CC">VPC</text>'
        # Private subnet
        '<rect x="50" y="90" width="180" height="180" fill="#FFF" stroke="#666" stroke-dasharray="3,2" rx="4"/>'
        '<text x="140" y="108" text-anchor="middle" font-size="10" font-weight="bold" fill="#666">Private Subnet</text>'
        # EC2
        '<rect x="70" y="125" width="140" height="40" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="4"/>'
        '<text x="140" y="150" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">EC2 / Lambda</text>'
        # Interface EP
        '<rect x="70" y="185" width="140" height="75" fill="#FCE7F3" stroke="#E7157B" stroke-width="2" rx="4"/>'
        '<text x="140" y="205" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Interface EP (ENI)</text>'
        '<text x="140" y="222" text-anchor="middle" font-size="9" fill="#666">PrivateLink</text>'
        '<text x="140" y="237" text-anchor="middle" font-size="9" fill="#666">SSM / KMS / ECR /</text>'
        '<text x="140" y="250" text-anchor="middle" font-size="9" fill="#666">SQS / STS ...</text>'
        # Gateway EP
        '<rect x="260" y="130" width="170" height="80" fill="#EBF5E8" stroke="#7AA116" stroke-width="2" rx="4"/>'
        '<text x="345" y="150" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Gateway EP</text>'
        '<text x="345" y="168" text-anchor="middle" font-size="9" fill="#666">Route Table にルート追加</text>'
        '<text x="345" y="185" text-anchor="middle" font-size="10" font-weight="bold" fill="#7AA116">S3 / DynamoDB のみ</text>'
        '<text x="345" y="200" text-anchor="middle" font-size="9" fill="#666">無料</text>'
        # External services
        '<rect x="490" y="100" width="180" height="60" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="6"/>'
        '<text x="580" y="125" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">AWS Service</text>'
        '<text x="580" y="143" text-anchor="middle" font-size="10" fill="#666">(SSM/ECR/SQS...)</text>'
        '<rect x="490" y="175" width="180" height="60" fill="#EBF5E8" stroke="#7AA116" stroke-width="2" rx="6"/>'
        '<text x="580" y="200" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">S3 / DynamoDB</text>'
        '<text x="580" y="218" text-anchor="middle" font-size="10" fill="#666">(Regional Service)</text>'
        # Arrows
        '<line x1="210" y1="145" x2="260" y2="170" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="210" y1="220" x2="490" y2="130" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="430" y1="175" x2="490" y2="200" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        # Legend
        '<text x="350" y="308" text-anchor="middle" font-size="10" fill="#666">Gateway EP = S3/DynamoDB 専用・無料／Interface EP = ENI 配置・時間課金</text>'
    )
    return svg_wrap('VPC Endpoints', inner)


def svg_data_pipeline():
    inner = (
        '<text x="350" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#232F3E">データパイプライン構成</text>'
        # Source
        '<rect x="20" y="100" width="110" height="60" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="6"/>'
        '<text x="75" y="125" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Sources</text>'
        '<text x="75" y="142" text-anchor="middle" font-size="9" fill="#666">App / IoT / Logs</text>'
        # Kinesis Streams
        '<rect x="160" y="100" width="110" height="60" fill="#FCE7F3" stroke="#E7157B" stroke-width="2" rx="6"/>'
        '<text x="215" y="120" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Kinesis</text>'
        '<text x="215" y="137" text-anchor="middle" font-size="10" fill="#232F3E">Data Streams</text>'
        '<text x="215" y="152" text-anchor="middle" font-size="9" fill="#666">shard / retention</text>'
        # Firehose
        '<rect x="300" y="100" width="110" height="60" fill="#FCE7F3" stroke="#E7157B" stroke-width="2" rx="6"/>'
        '<text x="355" y="120" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Kinesis Firehose</text>'
        '<text x="355" y="137" text-anchor="middle" font-size="9" fill="#666">変換/バッファ</text>'
        '<text x="355" y="152" text-anchor="middle" font-size="9" fill="#666">Parquet 変換可</text>'
        # S3
        '<rect x="440" y="100" width="110" height="60" fill="#EBF5E8" stroke="#7AA116" stroke-width="2" rx="6"/>'
        '<text x="495" y="120" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">S3 Data Lake</text>'
        '<text x="495" y="137" text-anchor="middle" font-size="9" fill="#666">パーティション</text>'
        '<text x="495" y="152" text-anchor="middle" font-size="9" fill="#666">(year/month/day)</text>'
        # Athena
        '<rect x="580" y="60" width="100" height="50" fill="#EBF1FF" stroke="#3B48CC" stroke-width="2" rx="6"/>'
        '<text x="630" y="82" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Athena</text>'
        '<text x="630" y="98" text-anchor="middle" font-size="9" fill="#666">SQL 分析</text>'
        # Glue
        '<rect x="580" y="130" width="100" height="50" fill="#EBF1FF" stroke="#3B48CC" stroke-width="2" rx="6"/>'
        '<text x="630" y="152" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Glue Catalog</text>'
        '<text x="630" y="168" text-anchor="middle" font-size="9" fill="#666">スキーマ管理</text>'
        # QuickSight
        '<rect x="580" y="200" width="100" height="50" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="6"/>'
        '<text x="630" y="222" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">QuickSight</text>'
        '<text x="630" y="238" text-anchor="middle" font-size="9" fill="#666">BI ダッシュ</text>'
        # Arrows
        '<line x1="130" y1="130" x2="160" y2="130" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="270" y1="130" x2="300" y2="130" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="410" y1="130" x2="440" y2="130" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="550" y1="120" x2="580" y2="95" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="550" y1="140" x2="580" y2="155" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="630" y1="180" x2="630" y2="200" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        # Legend
        '<text x="350" y="260" text-anchor="middle" font-size="10" fill="#666">ストリーミング: Kinesis Data Streams (ms遅延)／ニアリアルタイム配信: Firehose (60秒〜)</text>'
        '<text x="350" y="278" text-anchor="middle" font-size="10" fill="#666">S3 + Glue + Athena = サーバーレス分析基盤 (Lakehouse)</text>'
    )
    return svg_wrap('データパイプライン', inner)


def svg_event_driven():
    inner = (
        '<text x="350" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#232F3E">イベント駆動 (EventBridge / SNS / SQS fan-out)</text>'
        # Producer
        '<rect x="20" y="140" width="120" height="60" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="6"/>'
        '<text x="80" y="165" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Producer</text>'
        '<text x="80" y="183" text-anchor="middle" font-size="9" fill="#666">App / Service</text>'
        # EventBridge
        '<rect x="170" y="140" width="140" height="60" fill="#F3E8FF" stroke="#8C4FFF" stroke-width="2" rx="6"/>'
        '<text x="240" y="163" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">EventBridge</text>'
        '<text x="240" y="180" text-anchor="middle" font-size="9" fill="#666">ルール + Pattern</text>'
        '<text x="240" y="193" text-anchor="middle" font-size="9" fill="#666">(JSON マッチ)</text>'
        # SNS (fan-out)
        '<rect x="170" y="40" width="140" height="55" fill="#F3E8FF" stroke="#8C4FFF" stroke-width="2" rx="6"/>'
        '<text x="240" y="62" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">SNS Topic</text>'
        '<text x="240" y="80" text-anchor="middle" font-size="9" fill="#666">fan-out / 複数サブスク</text>'
        # SQS queues (multiple)
        '<rect x="360" y="60" width="120" height="45" fill="#F3E8FF" stroke="#8C4FFF" stroke-width="2" rx="4"/>'
        '<text x="420" y="80" text-anchor="middle" font-size="10" font-weight="bold" fill="#232F3E">SQS Queue #1</text>'
        '<text x="420" y="95" text-anchor="middle" font-size="9" fill="#666">(buffer)</text>'
        '<rect x="360" y="120" width="120" height="45" fill="#F3E8FF" stroke="#8C4FFF" stroke-width="2" rx="4"/>'
        '<text x="420" y="140" text-anchor="middle" font-size="10" font-weight="bold" fill="#232F3E">SQS Queue #2</text>'
        '<text x="420" y="155" text-anchor="middle" font-size="9" fill="#666">(DLQ 連携)</text>'
        '<rect x="360" y="180" width="120" height="45" fill="#F3E8FF" stroke="#8C4FFF" stroke-width="2" rx="4"/>'
        '<text x="420" y="200" text-anchor="middle" font-size="10" font-weight="bold" fill="#232F3E">Lambda Target</text>'
        '<text x="420" y="215" text-anchor="middle" font-size="9" fill="#666">(直接)</text>'
        # Consumers
        '<rect x="520" y="60" width="140" height="45" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="4"/>'
        '<text x="590" y="80" text-anchor="middle" font-size="10" font-weight="bold" fill="#232F3E">Consumer A</text>'
        '<text x="590" y="95" text-anchor="middle" font-size="9" fill="#666">Lambda / ECS</text>'
        '<rect x="520" y="120" width="140" height="45" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="4"/>'
        '<text x="590" y="140" text-anchor="middle" font-size="10" font-weight="bold" fill="#232F3E">Consumer B</text>'
        '<text x="590" y="155" text-anchor="middle" font-size="9" fill="#666">Step Functions</text>'
        '<rect x="520" y="180" width="140" height="45" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="4"/>'
        '<text x="590" y="200" text-anchor="middle" font-size="10" font-weight="bold" fill="#232F3E">Consumer C</text>'
        '<text x="590" y="215" text-anchor="middle" font-size="9" fill="#666">API Destination</text>'
        # Arrows
        '<line x1="140" y1="170" x2="170" y2="170" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="140" y1="170" x2="170" y2="80" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="310" y1="70" x2="360" y2="82" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="310" y1="170" x2="360" y2="140" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="310" y1="185" x2="360" y2="200" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="480" y1="82" x2="520" y2="82" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="480" y1="142" x2="520" y2="142" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="480" y1="202" x2="520" y2="202" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        # Legend
        '<text x="350" y="253" text-anchor="middle" font-size="10" fill="#666">EventBridge: SaaS/AWS イベントのルーティング＋Schema Registry</text>'
        '<text x="350" y="270" text-anchor="middle" font-size="10" fill="#666">SNS+SQS fan-out: 各Consumer は自分のキューで独立処理・リトライ・DLQ</text>'
    )
    return svg_wrap('イベント駆動アーキテクチャ', inner)


def svg_api_architecture():
    inner = (
        '<text x="350" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#232F3E">API サーバーレス構成</text>'
        # User
        '<rect x="20" y="130" width="90" height="50" fill="#F5F5F5" stroke="#232F3E" stroke-width="2" rx="6"/>'
        '<text x="65" y="152" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Client</text>'
        '<text x="65" y="168" text-anchor="middle" font-size="9" fill="#666">Web / Mobile</text>'
        # CloudFront
        '<rect x="140" y="130" width="110" height="50" fill="#FCE7F3" stroke="#E7157B" stroke-width="2" rx="6"/>'
        '<text x="195" y="152" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">CloudFront</text>'
        '<text x="195" y="168" text-anchor="middle" font-size="9" fill="#666">+ WAF / Shield</text>'
        # Cognito
        '<rect x="140" y="55" width="110" height="50" fill="#FEF3F2" stroke="#DD344C" stroke-width="2" rx="6"/>'
        '<text x="195" y="77" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Cognito</text>'
        '<text x="195" y="93" text-anchor="middle" font-size="9" fill="#666">User Pool (JWT)</text>'
        # API Gateway
        '<rect x="280" y="130" width="130" height="50" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="6"/>'
        '<text x="345" y="152" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">API Gateway</text>'
        '<text x="345" y="168" text-anchor="middle" font-size="9" fill="#666">REST / HTTP / WS</text>'
        # Lambda Authorizer
        '<rect x="280" y="55" width="130" height="50" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="6"/>'
        '<text x="345" y="77" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Lambda Authorizer</text>'
        '<text x="345" y="93" text-anchor="middle" font-size="9" fill="#666">JWT 検証 / カスタム認可</text>'
        # Backend Lambda
        '<rect x="440" y="80" width="130" height="50" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="6"/>'
        '<text x="505" y="102" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Lambda (API)</text>'
        '<text x="505" y="118" text-anchor="middle" font-size="9" fill="#666">Business Logic</text>'
        # Backend ECS/EC2
        '<rect x="440" y="150" width="130" height="50" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="6"/>'
        '<text x="505" y="172" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">ECS / ALB</text>'
        '<text x="505" y="188" text-anchor="middle" font-size="9" fill="#666">長時間処理</text>'
        # DB
        '<rect x="600" y="80" width="90" height="50" fill="#EBF5E8" stroke="#7AA116" stroke-width="2" rx="6"/>'
        '<text x="645" y="102" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">DynamoDB</text>'
        '<text x="645" y="118" text-anchor="middle" font-size="9" fill="#666">KV Store</text>'
        '<rect x="600" y="150" width="90" height="50" fill="#EBF5E8" stroke="#7AA116" stroke-width="2" rx="6"/>'
        '<text x="645" y="172" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Aurora</text>'
        '<text x="645" y="188" text-anchor="middle" font-size="9" fill="#666">Relational</text>'
        # Arrows
        '<line x1="110" y1="155" x2="140" y2="155" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="250" y1="155" x2="280" y2="155" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="345" y1="130" x2="345" y2="105" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="410" y1="150" x2="440" y2="105" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="410" y1="160" x2="440" y2="175" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="570" y1="105" x2="600" y2="105" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="570" y1="175" x2="600" y2="175" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        # Legend
        '<text x="350" y="235" text-anchor="middle" font-size="10" fill="#666">CloudFront + API Gateway: エッジキャッシュ + リージョナル API</text>'
        '<text x="350" y="252" text-anchor="middle" font-size="10" fill="#666">Cognito で JWT 発行 → API GW で直接検証 または Lambda Authorizer で拡張制御</text>'
    )
    return svg_wrap('API サーバーレス構成', inner, viewbox='0 0 700 270')


def svg_storage_lifecycle():
    inner = (
        '<text x="350" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#232F3E">S3 ライフサイクル / ストレージクラス遷移</text>'
        # Standard
        '<rect x="20" y="100" width="120" height="70" fill="#EBF5E8" stroke="#7AA116" stroke-width="2" rx="6"/>'
        '<text x="80" y="120" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">S3 Standard</text>'
        '<text x="80" y="138" text-anchor="middle" font-size="9" fill="#666">頻繁アクセス</text>'
        '<text x="80" y="152" text-anchor="middle" font-size="9" fill="#666">ms 取得</text>'
        '<text x="80" y="164" text-anchor="middle" font-size="9" fill="#7AA116">基準コスト</text>'
        # Standard-IA
        '<rect x="170" y="100" width="120" height="70" fill="#EBF5E8" stroke="#7AA116" stroke-width="2" rx="6"/>'
        '<text x="230" y="120" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">S3 Standard-IA</text>'
        '<text x="230" y="138" text-anchor="middle" font-size="9" fill="#666">アクセス稀</text>'
        '<text x="230" y="152" text-anchor="middle" font-size="9" fill="#666">ms 取得 (即時)</text>'
        '<text x="230" y="164" text-anchor="middle" font-size="9" fill="#7AA116">30日〜</text>'
        # Glacier Instant
        '<rect x="320" y="100" width="120" height="70" fill="#EBF5E8" stroke="#7AA116" stroke-width="2" rx="6"/>'
        '<text x="380" y="120" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Glacier Instant</text>'
        '<text x="380" y="138" text-anchor="middle" font-size="9" fill="#666">アーカイブ即時</text>'
        '<text x="380" y="152" text-anchor="middle" font-size="9" fill="#666">ms 取得</text>'
        '<text x="380" y="164" text-anchor="middle" font-size="9" fill="#7AA116">90日〜</text>'
        # Glacier Flexible
        '<rect x="470" y="100" width="120" height="70" fill="#EBF5E8" stroke="#7AA116" stroke-width="2" rx="6"/>'
        '<text x="530" y="120" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Glacier Flexible</text>'
        '<text x="530" y="138" text-anchor="middle" font-size="9" fill="#666">分〜時間</text>'
        '<text x="530" y="152" text-anchor="middle" font-size="9" fill="#666">復元要</text>'
        '<text x="530" y="164" text-anchor="middle" font-size="9" fill="#7AA116">90日〜</text>'
        # Glacier Deep Archive
        '<rect x="20" y="200" width="120" height="70" fill="#EBF5E8" stroke="#7AA116" stroke-width="2" rx="6"/>'
        '<text x="80" y="220" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">Deep Archive</text>'
        '<text x="80" y="238" text-anchor="middle" font-size="9" fill="#666">最安</text>'
        '<text x="80" y="252" text-anchor="middle" font-size="9" fill="#666">12時間〜</text>'
        '<text x="80" y="264" text-anchor="middle" font-size="9" fill="#7AA116">180日〜</text>'
        # Intelligent-Tiering
        '<rect x="170" y="200" width="420" height="70" fill="#EBF1FF" stroke="#3B48CC" stroke-width="2" rx="6"/>'
        '<text x="380" y="220" text-anchor="middle" font-size="11" font-weight="bold" fill="#3B48CC">S3 Intelligent-Tiering (自動階層化)</text>'
        '<text x="380" y="238" text-anchor="middle" font-size="9" fill="#666">Frequent / Infrequent / Archive Instant / Archive / Deep Archive 階層</text>'
        '<text x="380" y="254" text-anchor="middle" font-size="10" fill="#3B48CC">アクセス不明・変動する場合に最適 (監視料のみ)</text>'
        # Arrows (transitions)
        '<line x1="140" y1="135" x2="170" y2="135" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<text x="155" y="128" text-anchor="middle" font-size="8" fill="#666">30d</text>'
        '<line x1="290" y1="135" x2="320" y2="135" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<text x="305" y="128" text-anchor="middle" font-size="8" fill="#666">90d</text>'
        '<line x1="440" y1="135" x2="470" y2="135" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<text x="455" y="128" text-anchor="middle" font-size="8" fill="#666">90d</text>'
        '<path d="M 80 170 Q 50 185 80 200" fill="none" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<text x="30" y="190" font-size="8" fill="#666">180d</text>'
        # Legend
        '<text x="350" y="300" text-anchor="middle" font-size="10" fill="#666">ライフサイクルルールで日数後に自動遷移 / 即時取得必須なら Glacier Flexible/Deep Archive は NG</text>'
    )
    return svg_wrap('S3 ライフサイクル', inner, viewbox='0 0 700 310')


def svg_container_network():
    inner = (
        '<text x="350" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#232F3E">コンテナ + ネットワーク構成</text>'
        # VPC
        '<rect x="30" y="45" width="640" height="250" fill="#EBF1FF" stroke="#3B48CC" stroke-width="2" rx="8"/>'
        '<text x="350" y="65" text-anchor="middle" font-size="12" font-weight="bold" fill="#3B48CC">VPC</text>'
        # Public subnet (ALB)
        '<rect x="50" y="80" width="180" height="200" fill="#FFF" stroke="#666" stroke-dasharray="3,2" rx="4"/>'
        '<text x="140" y="98" text-anchor="middle" font-size="10" font-weight="bold" fill="#666">Public Subnet</text>'
        '<rect x="70" y="120" width="140" height="50" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="4"/>'
        '<text x="140" y="142" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">ALB / NLB</text>'
        '<text x="140" y="158" text-anchor="middle" font-size="9" fill="#666">TLS 終端 / ヘルスチェック</text>'
        # Private subnet (ECS/EKS)
        '<rect x="260" y="80" width="220" height="200" fill="#FFF" stroke="#666" stroke-dasharray="3,2" rx="4"/>'
        '<text x="370" y="98" text-anchor="middle" font-size="10" font-weight="bold" fill="#666">Private Subnet</text>'
        '<rect x="280" y="115" width="180" height="60" fill="#FFF5EB" stroke="#FF9900" stroke-width="2" rx="4"/>'
        '<text x="370" y="138" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">ECS / EKS Service</text>'
        '<text x="370" y="155" text-anchor="middle" font-size="10" fill="#666">Fargate / EC2 起動タイプ</text>'
        '<text x="370" y="168" text-anchor="middle" font-size="9" fill="#666">Auto Scaling / Task Definition</text>'
        '<rect x="280" y="190" width="180" height="60" fill="#EBF5E8" stroke="#7AA116" stroke-width="2" rx="4"/>'
        '<text x="370" y="212" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">RDS / DynamoDB</text>'
        '<text x="370" y="228" text-anchor="middle" font-size="9" fill="#666">Backend データストア</text>'
        '<text x="370" y="242" text-anchor="middle" font-size="9" fill="#666">SG: ECS から 3306/etc</text>'
        # ECR
        '<rect x="510" y="115" width="140" height="60" fill="#FCE7F3" stroke="#E7157B" stroke-width="2" rx="4"/>'
        '<text x="580" y="138" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">ECR</text>'
        '<text x="580" y="155" text-anchor="middle" font-size="9" fill="#666">コンテナレジストリ</text>'
        '<text x="580" y="168" text-anchor="middle" font-size="9" fill="#666">Image Scan / Lifecycle</text>'
        # CloudWatch
        '<rect x="510" y="190" width="140" height="60" fill="#FCE7F3" stroke="#E7157B" stroke-width="2" rx="4"/>'
        '<text x="580" y="212" text-anchor="middle" font-size="11" font-weight="bold" fill="#232F3E">CloudWatch</text>'
        '<text x="580" y="228" text-anchor="middle" font-size="9" fill="#666">Logs / Container Insights</text>'
        # Arrows
        '<line x1="210" y1="145" x2="280" y2="145" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="460" y1="220" x2="460" y2="220" stroke="#666" stroke-width="2"/>'
        '<line x1="370" y1="175" x2="370" y2="190" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="510" y1="145" x2="460" y2="145" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        '<line x1="460" y1="220" x2="510" y2="220" stroke="#666" stroke-width="2" marker-end="url(#arr)"/>'
        # External user
        '<rect x="30" y="300" width="640" height="0" fill="none"/>'
    )
    return svg_wrap('コンテナ + ネットワーク', inner, viewbox='0 0 700 310')


# ---------- dispatcher ----------

def determine_svg(q):
    """Return (svg_str, category) or (None, None) if no diagram."""
    text = (q['question'] + ' ' + ' '.join(c['text'] for c in q['choices']) + ' ' +
            q.get('explanation', {}).get('detail', '')).lower()

    # Keyword-driven routing; earlier matches win.
    # 1. Multi-region DR
    if any(k in text for k in ['マルチリージョン', 'リージョン間', 'aurora global', 'クロスリージョン', 'cross-region', 's3 cross-region', 'フェールオーバー ', 'フェイルオーバー']) or \
       ('rto' in text and 'rpo' in text) or \
       ('disaster recovery' in text) or \
       ('pilot light' in text) or ('warm standby' in text) or ('multi-site' in text):
        return svg_multi_region_dr(), 'multi_region_dr'

    # 2. Multi-account (Organizations)
    if any(k in text for k in ['aws organizations', 'organizations の', 'マルチアカウント', 'control tower', ' scp ', 'iam identity center', 'sso (', 'organizations を']) or \
       ('organizations' in text and ('ou' in text or 'scp' in text)):
        return svg_multi_account(), 'multi_account'

    # 3. Transit Gateway / VPC Peering hub-spoke
    if any(k in text for k in ['transit gateway', 'tgw', 'vpc peering', 'hub and spoke', 'hub-and-spoke', 'トランジットゲートウェイ']):
        return svg_transit_gateway(), 'network_tgw_vpc'

    # 4. Hybrid DX / VPN
    if any(k in text for k in ['direct connect', 'site-to-site vpn', 'client vpn', 'dx ', 'dxgw', 'direct connect gateway', 'ダイレクト接続', 'ハイブリッド']):
        return svg_hybrid_dx_vpn(), 'hybrid_dx_vpn'

    # 5. VPC Endpoints
    if any(k in text for k in ['vpc endpoint', 'privatelink', 'gateway endpoint', 'interface endpoint', 'プライベートリンク', 'vpcエンドポイント']):
        return svg_vpc_endpoints(), 'vpc_endpoints'

    # 6. Data pipeline
    if any(k in text for k in ['kinesis data firehose', 'kinesis firehose', 'firehose', 'data pipeline', 'etl パイプライン', 'emr', 'quicksight', 'redshift', 'glue catalog', 'glue ']) or \
       ('kinesis' in text and ('s3' in text or 'athena' in text)):
        return svg_data_pipeline(), 'data_pipeline'

    # 7. Event driven
    if any(k in text for k in ['eventbridge', 'event bridge', 'fan-out', 'fanout', 'ファンアウト', 'step functions']) or \
       ('sns' in text and 'sqs' in text):
        return svg_event_driven(), 'event_driven'

    # 8. API architecture
    if any(k in text for k in ['api gateway', 'appsync', 'lambda authorizer', 'cognito user pool']) or \
       ('cloudfront' in text and 'api' in text):
        return svg_api_architecture(), 'api_architecture'

    # 9. Storage lifecycle
    if any(k in text for k in ['ライフサイクル', 's3 lifecycle', 'intelligent-tiering', 'glacier deep archive', 'ストレージクラス']) or \
       ('s3 standard' in text and ('ia' in text or 'glacier' in text)):
        return svg_storage_lifecycle(), 'storage_lifecycle'

    # 10. Container network
    if any(k in text for k in ['ecs', 'eks', 'fargate', 'kubernetes', 'コンテナ']):
        return svg_container_network(), 'container_network'

    return None, None


def main():
    import sys
    data = json.loads(JSON_PATH.read_text(encoding='utf-8'))
    added = 0
    skipped_existing = 0
    skipped_nomatch = 0
    per_category = {}

    # Processing order: Udemy first (num 300-674), then CloudTech (num 1-299)
    # Filter via CLI flag: default is udemy only. pass 'all' to include cloudtech too.
    mode = sys.argv[1] if len(sys.argv) > 1 else 'udemy'
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9

    if mode == 'udemy':
        targets = [q for q in data if q.get('source') == 'udemy']
    elif mode == 'cloudtech':
        targets = [q for q in data if q.get('source') == 'cloudtech']
    else:
        # all: udemy first, cloudtech second
        udemy = [q for q in data if q.get('source') == 'udemy']
        cloudtech = [q for q in data if q.get('source') == 'cloudtech']
        targets = udemy + cloudtech

    print(f'mode={mode}, targets={len(targets)}, limit={limit}')

    for q in targets:
        if added >= limit:
            break
        detail = q.get('explanation', {}).get('detail', '')
        if MARKER in detail:
            skipped_existing += 1
            continue
        svg, cat = determine_svg(q)
        if svg is None:
            skipped_nomatch += 1
            continue
        q['explanation']['detail'] = detail + svg
        added += 1
        per_category[cat] = per_category.get(cat, 0) + 1

        # periodic save every 25 additions
        if added % 25 == 0:
            JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f'[checkpoint] added={added}')

    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print('=== DONE ===')
    print(f'added: {added}')
    print(f'skipped(existing): {skipped_existing}')
    print(f'skipped(no-match/unsuitable): {skipped_nomatch}')
    print('per category:')
    for k, v in sorted(per_category.items(), key=lambda x: -x[1]):
        print(f'  {k}: {v}')


if __name__ == '__main__':
    main()
