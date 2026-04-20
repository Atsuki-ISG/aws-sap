#!/usr/bin/env python3
"""
Multi-region / DR テーマの解説に「📌 判断ポイント」セクションを追記するスクリプト。

対象:
  - tags に "multi-region-dr" を含む問題
  - 問題文 / 選択肢に DR / マルチリージョン関連のキーワードを含む問題

修正ポリシー:
  - explanation.detail のみ更新可（answer / question / choices / id / num / tags / source は変更禁止）
  - 既に "📌 判断ポイント" を含む detail はスキップ
  - 末尾に <br><br>📌 判断ポイント<br>... を追記

書き込み直前にファイルを再読み込みし、対象問題のみ差し替えて保存する。
"""

import json
import re
from pathlib import Path

QUESTIONS_PATH = Path('/Users/aki/aws-sap/docs/data/questions.json')

# ----------------------------------------------------------------------------
# 対象問題の選定
# ----------------------------------------------------------------------------

DR_PATTERNS = [
    r'multi-region-dr',
    r'Disaster Recovery',
    r'ディザスタリカバリ',
    r'災害復旧',
    r'\bRTO\b',
    r'\bRPO\b',
    r'フェイルオーバー',
    r'fail.?over',
    r'Aurora Global',
    r'Aurora\s*グローバル',
    r'Pilot Light',
    r'パイロットライト',
    r'Warm Standby',
    r'ウォームスタンバイ',
    r'Multi-Site',
    r'マルチサイト',
    r'CloudEndure',
    r'Elastic Disaster Recovery',
    r'\bAWS DRS\b',
    r'DynamoDB Global Tables',
    r'グローバルテーブル',
    r'マルチリージョン',
    r'リージョン障害',
    r'リージョン全体.{0,10}障害',
    r'リージョン.{0,10}(ダウン|停止|ロスト|喪失|障害|消失)',
    r'リージョンを跨',
    r'別リージョン',
    r'別の.{0,3}リージョン',
    r'他リージョン.{0,5}(レプリ|複製|コピー)',
    r'(2|二|複数).{0,3}つの.{0,3}リージョン',
    r'セカンダリリージョン',
    r'プライマリリージョン.{0,30}(セカンダリ|別|障害)',
    r'クロスリージョン.*(レプリ|コピー|複製|スナップショット|バックアップ)',
    r'Cross-Region Replication',
    r'Route 53.*(failover|フェイル|レイテンシ|geolocation|地理)',
    r'\bCRR\b',
    r'cross.region',
]

DR_PATTERN_RE = re.compile('|'.join(DR_PATTERNS), re.IGNORECASE)


def extract_choice_text(choice):
    if isinstance(choice, dict):
        return choice.get('text', '')
    return str(choice)


def is_dr_question(q):
    """DR / マルチリージョン関連かを判定."""
    tags = q.get('tags', [])
    if 'multi-region-dr' in tags:
        return True
    q_text = q.get('question', '')
    choices_text = ' '.join(extract_choice_text(c) for c in q.get('choices', []))
    combined = q_text + ' ' + choices_text
    return bool(DR_PATTERN_RE.search(combined))


# ----------------------------------------------------------------------------
# 「📌 判断ポイント」テンプレート
# ----------------------------------------------------------------------------

JUDGMENT_TIPS_HTML = (
    "<br><br>"
    "<strong>📌 判断ポイント — マルチリージョン・DR 設計</strong>"
    "<br><br>"
    "<strong>① RTO / RPO 別 DR 戦略選定表</strong>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>戦略</th><th>RTO 目安</th><th>RPO 目安</th><th>コスト</th><th>典型構成</th></tr>"
    "<tr><td>Backup &amp; Restore</td><td>数時間〜1日</td><td>数時間（バックアップ間隔依存）</td><td>最安</td><td>AWS Backup / EBS スナップショット / S3 へのバックアップ。DR 時に IaC で再構築</td></tr>"
    "<tr><td>Pilot Light</td><td>数十分〜数時間</td><td>分〜秒</td><td>低</td><td>DB は常時レプリケーション、アプリ層は停止 or 最小。発動時に AMI / IaC で起動・スケール</td></tr>"
    "<tr><td>Warm Standby</td><td>数分〜十数分</td><td>秒</td><td>中</td><td>本番の縮小版を常時稼働。Route 53 フェイルオーバー＋ Auto Scaling で本番規模へ拡大</td></tr>"
    "<tr><td>Multi-Site Active/Active</td><td>数秒〜1分</td><td>秒〜0</td><td>高（≒2倍）</td><td>両リージョンで同等構成を稼働。Aurora Global / DynamoDB Global Tables / Route 53 レイテンシ or 加重</td></tr>"
    "</table>"
    "<br>"
    "<strong>② DB 種別ごとのマルチリージョン構成パターン</strong>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>用途</th><th>選ぶサービス</th><th>RPO / RTO の目安</th><th>注意点</th></tr>"
    "<tr><td>同一リージョン HA のみ</td><td>RDS Multi-AZ（同期）</td><td>RPO≒0 / RTO 1〜2分（自動フェイルオーバー）</td><td>AZ 障害用。<strong>リージョン障害には対応不可</strong></td></tr>"
    "<tr><td>読み取り負荷分散 / 軽い DR</td><td>RDS クロスリージョンリードレプリカ（非同期）</td><td>RPO 数秒〜分 / RTO 数十分（<strong>手動昇格</strong>）</td><td>昇格は手動。昇格後は独立 DB となり元プライマリへの自動戻しは不可</td></tr>"
    "<tr><td>本格マルチリージョン DR（MySQL/PostgreSQL）</td><td>Aurora Global Database</td><td>RPO 通常 &lt;1秒 / RTO &lt;1分（Managed フェイルオーバー）</td><td>セカンダリは読み取り専用。書き込みは Write Forwarding か昇格後。最大 5 セカンダリ</td></tr>"
    "<tr><td>NoSQL マルチリージョン Active/Active</td><td>DynamoDB Global Tables</td><td>RPO 1秒未満 / RTO ほぼ 0（双方向レプリケーション）</td><td>競合は <strong>LWW（Last Writer Wins）</strong>でタイムスタンプ最新が勝つ。強整合読み取りはローカルリージョンのみ</td></tr>"
    "<tr><td>S3 オブジェクト</td><td>S3 CRR / SRR</td><td>RPO 通常分単位（非同期）</td><td><strong>有効化以降の新規オブジェクトのみ</strong>レプリ。既存はバッチレプリケーション必要。バージョニング必須</td></tr>"
    "</table>"
    "<br>"
    "<strong>③ Route 53 ルーティングポリシー早見表</strong>"
    "<table border='1' cellpadding='4'>"
    "<tr><th>ポリシー</th><th>典型用途</th><th>挙動の要点</th></tr>"
    "<tr><td>Failover</td><td>Active/Passive DR</td><td>Primary 健全時のみ Primary、不健全時のみ Secondary。<strong>ヘルスチェック必須</strong></td></tr>"
    "<tr><td>Latency</td><td>Active/Active 低遅延</td><td>各レコードのリージョン基準で最も低レイテンシのエンドポイントへ</td></tr>"
    "<tr><td>Geolocation</td><td>地域別コンテンツ / 法規制</td><td>クライアント IP の国・大陸で振分。デフォルトレコード推奨</td></tr>"
    "<tr><td>Geoproximity</td><td>地理的近接 + バイアス</td><td>Traffic Flow 必須。Bias で割合を調整可</td></tr>"
    "<tr><td>Weighted</td><td>カナリア / A-B テスト</td><td>重み比でトラフィック分配</td></tr>"
    "<tr><td>Multivalue Answer</td><td>軽量な簡易冗長化</td><td>最大 8 件の健全レコードを返す。LB ではない</td></tr>"
    "</table>"
    "<br>"
    "<strong>Evaluate Target Health の挙動：</strong> Alias レコードでこれを <em>有効</em> にすると、ALB/NLB 配下のターゲット健全性に応じて Route 53 が自動で除外。CloudFront ディストリビューションの Alias では <em>必ず Yes</em> でも問題ないが、ALB Alias で No にするとフェイルオーバーが効かなくなる典型的な設定ミス。"
    "<br><br>"
    "<strong>④ よくある引っ掛けポイント</strong>"
    "<ul>"
    "<li><strong>S3 CRR は新規オブジェクトのみ</strong>：有効化前のオブジェクトは S3 Batch Replication で別途コピーが必要。バージョニングが両バケットで有効でないと CRR 自体構成不可</li>"
    "<li><strong>RDS クロスリージョンリードレプリカは手動昇格</strong>：自動フェイルオーバーは Aurora Global Database のみ。Aurora でも Managed Failover は &lt;1分、Unplanned は数分かかる</li>"
    "<li><strong>RDS Multi-AZ ≠ DR</strong>：同期レプリは AZ 間のみ。リージョン障害には無力</li>"
    "<li><strong>Aurora Write Forwarding</strong>：セカンダリリージョンから書き込みリクエストをプライマリへ転送できるが、レイテンシは増加。書き込み主体のワークロードには不向き</li>"
    "<li><strong>DynamoDB Global Tables の整合性</strong>：書き込みは結果整合（双方向）。同一キーへの同時書き込みは LWW で片方が消える可能性</li>"
    "<li><strong>Route 53 Failover にはヘルスチェック必須</strong>：単に Failover ポリシーを設定しただけでは切替らない。Primary レコードに HC を関連付ける</li>"
    "<li><strong>CloudFront はリージョンレス</strong>：オリジンフェイルオーバー（Origin Group）で 2 リージョンの ALB/S3 を切替可能。Route 53 の前段に置けば DNS TTL 影響を回避</li>"
    "<li><strong>Pilot Light の本質</strong>：DB は常時レプリ、アプリ層は停止または最小。発動後に AMI/IaC でスケールアップ。Backup &amp; Restore より速いが、Warm Standby より遅い</li>"
    "<li><strong>AWS Elastic Disaster Recovery (DRS)</strong>：旧 CloudEndure の後継。ブロックレベルの継続レプリで RPO 秒〜分、RTO 数分。オンプレ→AWS / リージョン間 DR 両対応。フェイルバック機能あり</li>"
    "<li><strong>Backup &amp; Restore は最安だが RTO 長い</strong>：RTO 数時間以上を許容できる場合のみ。RTO 1時間以下を求められたら不適切</li>"
    "</ul>"
)


# ----------------------------------------------------------------------------
# 実行
# ----------------------------------------------------------------------------

def main():
    # 対象 num を確定
    with QUESTIONS_PATH.open('r', encoding='utf-8') as f:
        data = json.load(f)

    target_nums = [q['num'] for q in data if is_dr_question(q)]
    print(f'[INFO] 対象問題数: {len(target_nums)}')

    # 書き込み直前にもう一度ファイルを再読み込みし、対象問題のみ差し替える
    with QUESTIONS_PATH.open('r', encoding='utf-8') as f:
        data = json.load(f)

    target_set = set(target_nums)
    appended = 0
    skipped_already = 0
    skipped_no_explanation = 0

    for q in data:
        if q['num'] not in target_set:
            continue
        explanation = q.get('explanation')
        if not isinstance(explanation, dict):
            skipped_no_explanation += 1
            continue
        detail = explanation.get('detail', '')
        if '📌 判断ポイント' in detail:
            skipped_already += 1
            continue
        explanation['detail'] = detail + JUDGMENT_TIPS_HTML
        appended += 1

    # JSON として書き戻し
    with QUESTIONS_PATH.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'[OK] 加筆した問題数 : {appended}')
    print(f'[OK] 既に判断ポイント有でスキップ: {skipped_already}')
    print(f'[OK] explanation 欠落でスキップ : {skipped_no_explanation}')
    print(f'[OK] 対象問題数（合計）       : {len(target_nums)}')


if __name__ == '__main__':
    main()
