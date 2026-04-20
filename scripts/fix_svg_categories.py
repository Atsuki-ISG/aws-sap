#!/usr/bin/env python3
"""
カテゴリ誤分類を補正するスクリプト。
既に追加された SVG から、問題文と合わない図を差し替える。

アプローチ:
  - detail の末尾の「<div style="margin-top:16px;"><!-- svg_added -->...</div>」を抽出
  - 問題文から「正しい分類」を再評価
  - 不一致なら SVG を置換
"""
import json
import re
from pathlib import Path
import importlib.util

JSON_PATH = Path('/Users/aki/aws-sap/docs/data/questions.json')

# Import SVG functions from add_svg_diagrams
spec = importlib.util.spec_from_file_location('add_svg', '/Users/aki/aws-sap/scripts/add_svg_diagrams.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

MARKER = '<!-- svg_added -->'

SVG_BLOCK_RE = re.compile(
    r'<div style="margin-top:16px;"><!-- svg_added -->.*?</svg></div>',
    re.DOTALL,
)


def strip_svg(detail):
    return SVG_BLOCK_RE.sub('', detail)


def classify(q):
    """Return (svg, cat, title_key) for a question. More careful than initial classifier."""
    qtext = q['question'].lower()
    choices = ' '.join(c['text'] for c in q['choices']).lower()
    det = q.get('explanation', {}).get('detail', '')
    # detail without SVG
    det_clean = strip_svg(det).lower()
    full = qtext + ' ' + choices + ' ' + det_clean

    # More specific keyword routing (priority matters)

    # 1. PrivateLink / VPC Endpoints (must come before DX/hybrid since privatelink is often in on-prem scenarios too)
    if any(k in full for k in ['privatelink', 'プライベートリンク', 'private link']) or \
       'vpc endpoint' in full or 'vpcエンドポイント' in full or \
       'interface endpoint' in full or 'gateway endpoint' in full:
        return mod.svg_vpc_endpoints(), 'vpc_endpoints', '構成図: VPC Endpoints'

    # 2. Multi-region DR (needs multiple region indicators)
    if any(k in full for k in ['マルチリージョン', 'リージョン間', 'クロスリージョン', 'cross-region', 'aurora global database', 'pilot light', 'warm standby', 'multi-site']) or \
       ('disaster recovery' in full) or \
       ('rto' in full and 'rpo' in full) or \
       ('プライマリリージョン' in full and 'セカンダリ' in full) or \
       ('primary region' in full and 'secondary' in full) or \
       (full.count('リージョン') >= 3 and 'フェイルオーバー' in full):
        return mod.svg_multi_region_dr(), 'multi_region_dr', '構成図: マルチリージョン DR'

    # 3. Multi-account Organizations
    if any(k in full for k in ['aws organizations', 'マルチアカウント', 'control tower', ' scp ', 'iam identity center', 'aws sso']) or \
       'service control policy' in full or \
       (' ou ' in full and 'organizations' in full) or \
       ('複数アカウント' in full and ('organizations' in full or '組織' in full)):
        return mod.svg_multi_account(), 'multi_account', '構成図: マルチアカウント (Organizations + OU)'

    # 4. Transit Gateway / VPC Peering
    if any(k in full for k in ['transit gateway', 'tgw', 'トランジットゲートウェイ', 'vpc peering', 'vpcピアリング', 'vpc ピアリング', 'hub-and-spoke', 'hub and spoke']):
        return mod.svg_transit_gateway(), 'network_tgw_vpc', '構成図: Transit Gateway Hub-and-Spoke'

    # 5. Hybrid DX / VPN (explicit on-prem + DX/VPN keywords)
    hybrid_keys = ['direct connect', 'ダイレクト接続', 'ダイレクトコネクト', 'site-to-site vpn', 'サイト間vpn', 'client vpn', 'direct connect gateway', 'dxgw']
    onprem_keys = ['オンプレミス', 'オンプレ', 'on-premise', 'on-prem', 'データセンター', 'customer gateway', 'カスタマーゲートウェイ']
    if any(k in full for k in hybrid_keys) or \
       (any(k in full for k in onprem_keys) and ('vpn' in full or 'bgp' in full)):
        return mod.svg_hybrid_dx_vpn(), 'hybrid_dx_vpn', '構成図: ハイブリッド接続 (DX/VPN)'

    # 6. Data pipeline (streaming/analytics)
    if any(k in full for k in ['kinesis data firehose', 'kinesis firehose', 'firehose', 'emr クラスター', 'quicksight', 'redshift', 'glue catalog']) or \
       ('kinesis' in full and ('s3' in full or 'athena' in full)) or \
       ('athena' in full and 's3' in full) or \
       ('glue' in full and 's3' in full):
        return mod.svg_data_pipeline(), 'data_pipeline', '構成図: データパイプライン'

    # 7. Event driven (multiple messaging services)
    if 'eventbridge' in full or 'event bridge' in full or \
       'fan-out' in full or 'fanout' in full or 'ファンアウト' in full or \
       'step functions' in full or \
       ('sns' in full and 'sqs' in full):
        return mod.svg_event_driven(), 'event_driven', '構成図: イベント駆動アーキテクチャ'

    # 8. API architecture
    if 'api gateway' in full or 'appsync' in full or 'lambda authorizer' in full or \
       ('cognito' in full and 'user pool' in full) or \
       ('cloudfront' in full and ' api ' in full):
        return mod.svg_api_architecture(), 'api_architecture', '構成図: API サーバーレス構成'

    # 9. Storage lifecycle
    if 'ライフサイクル' in full or 's3 lifecycle' in full or \
       'intelligent-tiering' in full or 'glacier deep archive' in full or \
       'ストレージクラス' in full or \
       ('s3 standard' in full and ('glacier' in full or 's3 ia' in full or '-ia' in full)):
        return mod.svg_storage_lifecycle(), 'storage_lifecycle', '構成図: S3 ライフサイクル'

    # 10. Container network
    if any(k in full for k in ['ecs', 'eks', 'fargate', 'kubernetes', 'コンテナ', 'docker', 'ecr']):
        return mod.svg_container_network(), 'container_network', '構成図: コンテナ + ネットワーク'

    return None, None, None


def main():
    data = json.loads(JSON_PATH.read_text(encoding='utf-8'))
    replaced = 0
    removed = 0
    kept = 0

    for q in data:
        if q.get('source') != 'udemy':
            continue
        det = q.get('explanation', {}).get('detail', '')
        if MARKER not in det:
            continue

        # Find current title key in the existing block
        m = re.search(r'構成図: ([^<]+)<', det)
        if not m:
            continue
        current_title = '構成図: ' + m.group(1)

        svg, cat, new_title = classify(q)
        if new_title is None:
            # Remove SVG – doesn't really need one
            new_detail = strip_svg(det)
            q['explanation']['detail'] = new_detail
            removed += 1
        elif new_title != current_title:
            new_detail = strip_svg(det) + svg
            q['explanation']['detail'] = new_detail
            replaced += 1
        else:
            kept += 1

    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'replaced: {replaced}')
    print(f'removed: {removed}')
    print(f'kept: {kept}')


if __name__ == '__main__':
    main()
