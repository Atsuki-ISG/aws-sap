#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAP-201〜250 の explanation を書き直すスクリプト
"""
import json

NEW_EXPLANATIONS = {
    201: {
        "perspective": "SCP の Allow リスト方式と FullAWSAccess の関係をどう設計すべきか？",
        "detail": "<strong>判断の決め手：「FullAWSAccess SCP が残ったまま」では Allow のみの SCP を追加しても全サービスが許可され続ける。</strong><br><br>SCP は評価式 <em>effective = (IAM_allow) ∩ (SCP_allow)</em> であり、<strong>FullAWSAccess を外して Allow のみの SCP を単独にする</strong>ことで「列挙された3サービス以外は暗黙の Deny」が実現できる。将来の拡張も Allow ステートメント追記で完結し、スケーラブル。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>FullAWSAccess を Deny に書き換えると全サービスが明示的 Deny になり、Allow SCP と共存できない。Deny が常に優先されるため3サービスも利用不可になる。</td></tr><tr><td>B</td><td>SCP の明示的 Deny は IAM Allow で上書き不可。Deny * を追加した後、IAM で許可しても効果なし。</td></tr><tr><td>C</td><td>AWS サービスは200以上あり各サービスに個別 Deny SCP を作るのは非スケーラブルで SCP アタッチ数の上限にも抵触する。</td></tr><tr><td>D</td><td>正解。FullAWSAccess を OU から外し、Allow のみの SCP を単独適用することで暗黙の Deny が機能する。</td></tr></table>",
        "tips": [
            "「SCP で特定サービスのみ許可」→ FullAWSAccess を外して Allow リスト方式の SCP だけ残す",
            "SCP の明示的 Deny → IAM Allow でも覆せない絶対拒否",
            "FullAWSAccess が残っている限り → カスタム Allow SCP を追加しても全サービスが通ってしまう"
        ]
    },
    202: {
        "perspective": "マルチアカウント環境で複数 VPC とオンプレを高帯域で接続するアーキテクチャは何が最適か？",
        "detail": "<strong>判断の決め手：「5 Gbps 以上の帯域」「複数 AWS アカウント」「スケーラブルなガバナンス」という3要件が重なる。</strong><br><br><strong>正解 A</strong>：中央ネットワークアカウントに DX Gateway + Transit Gateway を集約し、各アカウント VPC は TGW にアタッチする。DX 専用線を複数本束ねることで冗長性と帯域を確保しつつ、管理点を一元化できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>正解。中央集権型ネットワーク設計の模範。DX Gateway + TGW で複数 VPC とオンプレを単一管理点で接続。</td></tr><tr><td>B</td><td>VPC ごとに個別 DX 接続を作ると接続数が爆発的に増加し運用不能。帯域の統合もできない。</td></tr><tr><td>C</td><td>DX Gateway と仮想プライベートゲートウェイの組み合わせでは Transit Gateway の中継が使えず、VPC 間通信ができない。</td></tr><tr><td>D</td><td>トランジット VIF は TGW に直接アタッチするが、中央ネットワークアカウントの概念がなく各 VPC の管理が分散する。</td></tr></table>",
        "tips": [
            "複数 VPC ＋オンプレ接続 → Transit Gateway ＋ Direct Connect Gateway の中央集約モデル",
            "DX Gateway は複数 TGW と接続可能・TGW は複数 VPC を束ねる",
            "「帯域 5 Gbps 超」→ 複数本の DX をリンクアグリゲーション（LAG）もしくは並列接続で確保"
        ]
    },
    203: {
        "perspective": "103本のレガシー Web アプリを固定費最小でクラウド移行するには何が最適か？",
        "detail": "<strong>判断の決め手：「固定費削減最優先」「既存アプリ変更最小」「日次リクエスト僅少のアプリが多い」。</strong><br><br><strong>正解 A</strong>：シングルインスタンス Elastic Beanstalk 環境に複数アプリを集約することで、ALB の固定費（時間課金）を排除し、小さいインスタンスに複数アプリを同居させてコストを最小化できる。日次リクエストが僅少なアプリには過剰な高可用性構成は不要。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>正解。ALB なし・シングルインスタンス Beanstalk で最低コスト。リクエストが僅少なアプリには最適。</td></tr><tr><td>B</td><td>ECS Fargate は起動コストが高く、少量トラフィックのアプリ103本をコンテナ化する工数と実行コストがかさむ。</td></tr><tr><td>C</td><td>マルチAZ + ALB + Auto Scaling は高可用性構成だがコストが高く、コスト極小化の方針に反する。</td></tr><tr><td>D</td><td>SMS でリフト＆シフトしても EC2 の OS/MW 管理コストが残り、固定費削減の目標を達成しにくい。</td></tr></table>",
        "tips": [
            "「レガシー Web アプリを低コストで移行」→ Elastic Beanstalk シングルインスタンス集約",
            "ALB は時間課金 → ALB なし構成で固定費を削減できる",
            "「日次リクエスト僅少」→ 高可用性構成は過剰。シングルインスタンスで十分"
        ]
    },
    204: {
        "perspective": "DynamoDB の全変更イベントをリアルタイムに低運用で監査ログへ保存するには？",
        "detail": "<strong>判断の決め手：「30分以内の監査保管」「挿入・更新・削除の全イベント」「少人数運用」「改ざん防止」。</strong><br><br><strong>正解 D</strong>：DynamoDB Streams はテーブルの全変更を順序保証で捕捉できる唯一の仕組み。Lambda で受け取り Firehose 経由で S3 に継続保存、S3 バージョニングで改ざん防止も実現できる。完全マネージドでスケーラブル。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>CloudTrail は API レベルのログであり、アイテムの前後値（変更内容）は記録しない。監査ログとして不十分。</td></tr><tr><td>B</td><td>EventBridge + Lambda は API イベント検知であり、DynamoDB の個別レコード変更内容を取得できない。</td></tr><tr><td>C</td><td>30分バッチ抽出は「30分以内に保管」を満たさない場合があり、増分抽出の実装も複雑。</td></tr><tr><td>D</td><td>正解。DynamoDB Streams → Lambda → Firehose → S3 が最もシンプルかつリアルタイムな監査ログ基盤。</td></tr></table>",
        "tips": [
            "DynamoDB の全変更をリアルタイム捕捉 → DynamoDB Streams 一択",
            "Streams → Lambda → Firehose → S3 のパターンは監査ログの定番",
            "CloudTrail の DynamoDB ログ → API 操作記録のみでアイテム変更内容は含まない"
        ]
    },
    205: {
        "perspective": "グローバル同時リリースで S3 アセット配信とDynamoDB の DR をどう組み合わせるか？",
        "detail": "<strong>判断の決め手：「世界同時リリース」「低レイテンシ」「DR 対応」「マネージドな構成」。</strong><br><br><strong>正解 A</strong>：S3 クロスリージョンレプリケーション + CloudFront オリジンフェイルオーバー + DynamoDB グローバルテーブルの組み合わせが、グローバル配信・フェイルオーバー・マルチリージョン書き込みをすべてマネージドに実現する。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>正解。CRR + CloudFront フェイルオーバー + グローバルテーブルで DR・低レイテンシを一括解決。</td></tr><tr><td>B</td><td>Same-Region Replication はリージョン障害に対応できない。DMS CDC は DynamoDB の DR に不向き。</td></tr><tr><td>C</td><td>同一リージョン2バケットは DR 不可。SRR + CloudFront フェイルオーバーは別リージョン障害に無意味。</td></tr><tr><td>D</td><td>CloudFront のオリジンフェイルオーバーは正しいが、DynamoDB 側に言及がなく DR が不完全。</td></tr></table>",
        "tips": [
            "S3 の DR → クロスリージョンレプリケーション（CRR）+ CloudFront オリジンフェイルオーバー",
            "DynamoDB のマルチリージョン → グローバルテーブルで両リージョン読み書き可能",
            "「Same-Region Replication」→ 同一リージョン内の冗長化のみでリージョン障害には無効"
        ]
    },
    206: {
        "perspective": "「オンプレ HSM 生成キーを AWS KMS で使用する」要件に応えるキーストア設計は？",
        "detail": "<strong>判断の決め手：「オンプレミス HSM で生成したキーマテリアルを一本化」という要件。</strong><br><br><strong>正解 C</strong>：KMS でオリジンが EXTERNAL のカスタマーマネージドキーを作成すると、オンプレミス HSM で生成したキーマテリアルをインポートできる。S3 の SSE-KMS として利用でき、キーの原点をオンプレミスに置きながら KMS の管理性を享受できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>CloudHSM カスタムキーストアは HSM でキー生成・管理するが、CloudHSM クラスター（AWS 上）が必要でオンプレミス HSM とは別物。</td></tr><tr><td>B</td><td>AWS_KMS オリジンのキーに「インポート」はできない。オリジン設定は変更不可。</td></tr><tr><td>C</td><td>正解。EXTERNAL オリジンで KMS キーを作成しオンプレ HSM 生成のキーマテリアルをインポート。要件を満たす最小構成。</td></tr><tr><td>D</td><td>毎回オンプレ HSM へ問い合わせる構成はレイテンシが高く、DX 依存で可用性リスクもある。SSE-S3 と混在して要件を満たさない。</td></tr></table>",
        "tips": [
            "「オンプレ HSM 生成キーを KMS で使う」→ KMS キーのオリジンを EXTERNAL に設定してインポート",
            "CloudHSM カスタムキーストア ≠ オンプレ HSM 連携。CloudHSM は AWS 上の専有 HSM",
            "KMS キーのオリジンは作成時のみ設定可能・後から変更不可"
        ]
    },
    207: {
        "perspective": "プライベートサブネットから S3 へのトラフィックをコスト効率よくセキュアにルーティングするには？",
        "detail": "<strong>判断の決め手：「NAT ゲートウェイコスト削減」「プライベートサブネット → S3」「セキュリティ維持」。</strong><br><br><strong>正解 C</strong>：S3 ゲートウェイエンドポイントはデータ転送コスト無料・NAT GW を経由しないため、プライベートサブネットから S3 へのトラフィックを安全かつ低コストで直結できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>EC2 をパブリックに移動するとセキュリティが低下し、高機密画像処理という要件に反する。</td></tr><tr><td>B</td><td>EFS への変更はアーキテクチャの大幅変更が必要で、S3 からの直接読み込みをやめることはコスト削減の本質ではない。</td></tr><tr><td>C</td><td>正解。S3 ゲートウェイエンドポイントで NAT GW 不要化、コスト削減とセキュリティ強化を同時達成。</td></tr><tr><td>D</td><td>NAT インスタンスへの置き換えはコスト削減効果が限定的で、管理負荷が増加するだけ。</td></tr></table>",
        "tips": [
            "プライベートサブネット → S3/DynamoDB → ゲートウェイエンドポイントでデータ転送コスト無料",
            "S3 ゲートウェイエンドポイント → NAT GW 不要で安全・低コスト",
            "インターフェイスエンドポイント（PrivateLink）は料金あり。ゲートウェイエンドポイントは無料"
        ]
    },
    208: {
        "perspective": "「SMB 互換性を維持しながら段階的に S3 へ移行」する Storage Gateway の使い方は？",
        "detail": "<strong>判断の決め手：「SMB 共有を維持しながら段階的移行」「既存アプリ無改修」「CAPEX 削減」。</strong><br><br><strong>正解 D</strong>：Storage Gateway ファイルゲートウェイは SMB プロトコルのままアクセスさせながら、バックエンドを S3 に置ける。既存のサーバー・アプリ・ユーザーに変更を求めず、物理ストレージの増強も不要になる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>EC2 ファイルサーバーへの移行は SMB は維持できるが、EC2 の運用コストが発生し CAPEX→OPEX 変換にとどまる。</td></tr><tr><td>B</td><td>FSx for Windows + DataSync は SMB 互換性は高いが、FSx の費用が継続的にかかり S3 直接保存より高コスト。</td></tr><tr><td>C</td><td>S3 API 対応まで従来どおりオンプレで運用するのは「段階的移行」の解決にならず中間状態が長引く。</td></tr><tr><td>D</td><td>正解。Storage Gateway ファイルゲートウェイで SMB 共有をそのまま S3 にオフロード。最少変更で移行完了。</td></tr></table>",
        "tips": [
            "「SMB 維持＋S3 バックエンド」→ Storage Gateway ファイルゲートウェイ一択",
            "FSx for Windows は SMB 完全互換だが Storage Gateway より高コスト",
            "DataSync は一括・スケジュール転送向け。リアルタイム共有には不向き"
        ]
    },
    209: {
        "perspective": "10ドメインのリダイレクトを最小コスト・最小管理でサーバーレスに実現する構成は？",
        "detail": "<strong>判断の決め手：「複数ドメインの HTTP/HTTPS リダイレクト」「JSON 設定参照」「サーバーレス」「TLS 必須」。</strong><br><br><strong>正解 A＋B＋E</strong>：CloudFront + Lambda@Edge でリクエストを受け取り、JSON 設定ファイルを参照する Lambda 関数でリダイレクト先を決定（302応答）、ACM の SAN 証明書で10ドメインの TLS を一括対応できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>正解。CloudFront + Lambda@Edge でサーバーレスかつグローバルな HTTP/HTTPS リダイレクトを実現。</td></tr><tr><td>B</td><td>正解。ACM の SAN 証明書で10ドメインを1枚に集約し CloudFront に適用。コストと管理工数を削減。</td></tr><tr><td>C</td><td>API Gateway のカスタムドメインでも可能だが Lambda@Edge より複雑でコストが高い。</td></tr><tr><td>D</td><td>ALB はリスナールールの固定レスポンスでリダイレクト可能だが、ALB の固定費がかかり10ドメインの証明書管理も複雑。</td></tr><tr><td>E</td><td>正解。JSON ドキュメント参照でリダイレクト先を動的決定する Lambda 関数が柔軟性の核心。</td></tr><tr><td>F</td><td>EC2 は管理負荷が高くサーバーレスの目的に反する。</td></tr></table>",
        "tips": [
            "複数ドメインの TLS → ACM の SAN（Subject Alternative Name）証明書で一括対応",
            "CloudFront + Lambda@Edge → サーバーレスでグローバルなリダイレクト処理",
            "「JSON 設定でリダイレクト先を管理」→ Lambda 関数内で S3 から JSON を読み込む設計"
        ]
    },
    210: {
        "perspective": "メールに依存した業務フローをサーバーレスでリアルタイム化・疎結合化するには？",
        "detail": "<strong>判断の決め手：「メール遅延・誤送信による顧客満足度低下」「インフラ運用負荷削減」「リアルタイムなステータス更新」。</strong><br><br><strong>正解 B</strong>：API Gateway + Lambda + DynamoDB + SNS の完全サーバーレス構成で、メール依存をなくしてイベント駆動でリアルタイムに通知できる。オートスケール・運用不要・疎結合を同時に実現。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>ECS + RDS は可用性は高いが管理負荷が大きい。RDS への直接書き込みは疎結合でなく、メール依存の解消に直接つながらない。</td></tr><tr><td>B</td><td>正解。完全サーバーレス + SNS でリアルタイム通知。メール依存ゼロ、運用負荷ゼロで要件をすべて満たす。</td></tr><tr><td>C</td><td>EC2 + DynamoDB は一部改善だが EC2 管理コストが残り、メール依存の解消も不明瞭。</td></tr><tr><td>D</td><td>SES でメール受信して EC2 でポーリングは、メール依存を維持したままで問題の本質を解決していない。</td></tr></table>",
        "tips": [
            "「メール依存の業務フロー」→ SQS/SNS + Lambda でイベント駆動に置き換え",
            "API Gateway + Lambda + DynamoDB → サーバーレス Web アプリの定番構成",
            "SNS からのプッシュ通知 → SES メールよりリアルタイム性が高い"
        ]
    },
    211: {
        "perspective": "Elastic Beanstalk のブルーグリーンデプロイで「数分でロールバック可能」にするには？",
        "detail": "<strong>判断の決め手：「ブルーグリーンデプロイ標準化」「障害発生時に数分でロールバック」。</strong><br><br><strong>正解 A</strong>：Elastic Beanstalk の「Swap Environment URLs」は Blue と Green の URL を瞬時に切り替え、ロールバックも同じ操作で数分以内に完了できる。DNS TTL の影響を最小化する Beanstalk ネイティブな方法。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>正解。Beanstalk の URL Swap は瞬時切り替え＆ロールバックが可能。ブルーグリーンの模範実装。</td></tr><tr><td>B</td><td>ローリングデプロイはブルーグリーンではなく、数分以内のロールバックが困難。</td></tr><tr><td>C</td><td>Route 53 加重ルーティングは徐々に移行するカナリアリリース向け。即時切り替えには不向き。</td></tr><tr><td>D</td><td>DNS レコードの手動変更は DNS 伝播に時間がかかり「数分でロールバック」を保証できない。</td></tr></table>",
        "tips": [
            "Elastic Beanstalk のブルーグリーン → Swap Environment URLs で瞬時切り替え",
            "Route 53 加重ルーティング → カナリアリリース（段階的移行）向け。即時切替ではない",
            "DNS 手動切り替え → TTL の影響で即時反映を保証できない"
        ]
    },
    212: {
        "perspective": "S3 静的アセットのリージョン障害対策として最もシンプルかつ自動なフェイルオーバー設計は？",
        "detail": "<strong>判断の決め手：「単一リージョン障害による UI 崩壊が許容不可」「マネージドな自動フェイルオーバー」。</strong><br><br><strong>正解 B</strong>：S3 クロスリージョンレプリケーション（CRR）で自動的にセカンダリリージョンへ複製し、CloudFront のオリジンフェイルオーバーで障害時に自動で切り替わる。コード変更不要で運用が最もシンプル。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>アプリから両バケットへ同時書き込みはコード変更が必要で、Route 53 加重ルーティングは S3 バケットへの適用が複雑。</td></tr><tr><td>B</td><td>正解。CRR + CloudFront オリジンフェイルオーバーで自動 DR。コード変更不要で最もシンプル。</td></tr><tr><td>C</td><td>障害時に手動でコードを更新するのは RTO が長くなり「UI 崩壊が許容不可」の要件に反する。</td></tr><tr><td>D</td><td>Lambda でコピーする方式は CRR と同等だが、Lambda の運用コストと複雑さが増す。CloudFront フェイルオーバーの活用が欠ける。</td></tr></table>",
        "tips": [
            "S3 の自動クロスリージョン複製 → CRR（クロスリージョンレプリケーション）",
            "CloudFront オリジンフェイルオーバー → プライマリ障害時にセカンダリへ自動切替",
            "「コード変更なしで DR」→ CRR + CloudFront フェイルオーバーの組み合わせ"
        ]
    },
    213: {
        "perspective": "マルチアカウント環境でセキュリティチームが全アカウントを横断監査するクロスアカウント設計は？",
        "detail": "<strong>判断の決め手：「セキュリティアカウントから全アカウントの設定・ログを横断的に参照」「スケーラブル」。</strong><br><br><strong>正解 A</strong>：各メンバーアカウントに共通名称の読み取り専用 IAM ロールを作成し、セキュリティアカウントから AssumeRole でアクセスするのが最もシンプルで直接的なクロスアカウントアクセスパターン。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>正解。クロスアカウントロールパターンの模範。セキュリティアカウントから直接 AssumeRole で横断アクセス。</td></tr><tr><td>B</td><td>メンバーアカウントのユーザーがセキュリティアカウントへアクセスは逆方向。監査目的の設計として不適切。</td></tr><tr><td>C</td><td>管理アカウントを経由する二段階 AssumeRole は不必要に複雑。直接 AssumeRole で十分。</td></tr><tr><td>D</td><td>管理アカウントの OrganizationAccountAccessRole 経由は、セキュリティアカウントからの直接アクセスより迂回が多い。</td></tr></table>",
        "tips": [
            "「複数アカウントを横断監査」→ 共通名称のクロスアカウント読み取り専用ロール＋AssumeRole",
            "セキュリティアカウント → メンバーアカウントへ直接 AssumeRole が最もシンプル",
            "OrganizationAccountAccessRole → 管理アカウント専用の管理ロール。日常監査には不向き"
        ]
    },
    214: {
        "perspective": "AMI の脆弱性スキャンと承認済みリスト管理を自動化するパイプラインは？",
        "detail": "<strong>判断の決め手：「CVE 評価に合格した AMI のみ本番採用」「PCI DSS 準拠」「自動化」。</strong><br><br><strong>正解 B＋D</strong>：Amazon Inspector で EC2（AMI から起動）の CVE スキャンを自動実行し、合格した AMI の ID を Parameter Store に格納して承認済みリストとして管理する。Lambda で自動承認ロジックを実装することで、人手を介さない CI/CD パイプラインが構築できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>Config マネージドルールは設定コンプライアンス監視向けで CVE スキャンは行えない。</td></tr><tr><td>B</td><td>正解。Inspector は EC2 の CVE 評価を自動実行できる AWS ネイティブサービス。</td></tr><tr><td>C</td><td>CloudTrail は API 操作ログであり CVE 評価には使用できない。</td></tr><tr><td>D</td><td>正解。承認済み AMI ID を Parameter Store で一元管理することで、デプロイパイプラインが参照しやすい。</td></tr><tr><td>E</td><td>SSM エージェントによる独自アセスメントは手動確認が残り、自動承認の要件を満たさない。</td></tr></table>",
        "tips": [
            "EC2/AMI の CVE スキャン自動化 → Amazon Inspector",
            "承認済みリストの一元管理 → Systems Manager Parameter Store",
            "「Config マネージドルール」→ 設定コンプライアンス監視。脆弱性スキャンではない"
        ]
    },
    215: {
        "perspective": "組織全体の CIDR 変更を一元管理しセキュリティグループ更新コストを最小化するには？",
        "detail": "<strong>判断の決め手：「新規拠点 IP 追加のたびに全アカウントのセキュリティグループを更新」「運用コスト最小化」。</strong><br><br><strong>正解 B</strong>：セキュリティチームのアカウントでプレフィックスリストを一元作成し、RAM（Resource Access Manager）で組織共有する。各アカウントは共有プレフィックスリストをセキュリティグループに参照させるため、CIDR 追加はプレフィックスリストの更新だけで全アカウントに即時反映される。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>各アカウントでプレフィックスリストを個別管理するのは手動作業が分散し、運用コストが高い。</td></tr><tr><td>B</td><td>正解。RAM 共有プレフィックスリストで一元管理。CIDR 追加が即時全アカウントへ伝播する最小運用設計。</td></tr><tr><td>C</td><td>Lambda で全アカウントのセキュリティグループを直接更新するのは API 呼び出しが多く、失敗リスクも高い。</td></tr><tr><td>D</td><td>SNS + Lambda による各アカウント個別更新は障害発生時に一貫性が保てず、運用が複雑になる。</td></tr></table>",
        "tips": [
            "「組織全体で CIDR を一元管理」→ マネージドプレフィックスリスト + RAM 組織共有",
            "プレフィックスリストはセキュリティグループのインバウンド/アウトバウンドで直接参照可能",
            "RAM（Resource Access Manager）→ VPC、プレフィックスリスト等をクロスアカウント共有"
        ]
    },
    216: {
        "perspective": "CloudFront + ALB 構成でオリジン障害時にカスタムエラーページを表示するには？",
        "detail": "<strong>判断の決め手：「オリジン（ALB）障害時にブランドロゴ入りエラーページ」「CloudFront を活用」。</strong><br><br><strong>正解 B＋E</strong>：S3 にカスタムエラーページ HTML を配置し（B）、CloudFront でオリジンからの 5xx エラー時にこの S3 コンテンツを返すカスタムエラー応答を設定する（E）。完全マネージドで ALB 障害時でもユーザーに最適な体験を提供できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>Route 53 で S3 に切り替えても CloudFront キャッシュが残り、DNS TTL の影響で即時切替が困難。</td></tr><tr><td>B</td><td>正解。S3 静的ホスティングでエラーページを配置。CloudFront のエラー応答のソースとして最適。</td></tr><tr><td>C</td><td>CloudWatch アラーム → Lambda でスケールアップは障害の根本対処だが、カスタムエラーページ表示とは別の話。</td></tr><tr><td>D</td><td>ALB ターゲットグループの書き換えは複雑で確実性が低く、CloudFront のネイティブ機能を使う方が簡潔。</td></tr><tr><td>E</td><td>正解。CloudFront のカスタムエラー応答設定が本命。5xx 受信時に S3 の静的ページを返す設定が最小構成。</td></tr></table>",
        "tips": [
            "CloudFront でオリジン障害時のカスタムページ → カスタムエラー応答（Custom Error Response）",
            "エラーページのホスト先 → S3 静的ウェブサイトホスティング",
            "ALB + CloudFront 構成 → CloudFront の機能を最大活用してオリジン障害を吸収"
        ]
    },
    217: {
        "perspective": "DB パスワードの自動ローテーションと IaC 管理を両立させる最適な認証情報管理設計は？",
        "detail": "<strong>判断の決め手：「自動ローテーション」「CloudFormation での IaC 管理」「監査対応」。</strong><br><br><strong>正解 B</strong>：Secrets Manager はネイティブに RDS パスワードの自動ローテーションをサポートし、CloudFormation テンプレートでシークレット・ローテーション Lambda・アタッチメントをすべて定義でき、IaC との親和性が最も高い。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>Parameter Store の SecureString は自動ローテーションを標準でサポートしない。Lambda で自前実装が必要で複雑。</td></tr><tr><td>B</td><td>正解。Secrets Manager はローテーション機能組み込み、CloudFormation 対応も充実。最小実装で要件全充足。</td></tr><tr><td>C</td><td>Parameter Store はローテーション非対応。CloudFormation 定義のみでローテーションは実現できない。</td></tr><tr><td>D</td><td>Secrets Manager + Lambda 手動実装は B より複雑。Secrets Manager のネイティブローテーションを使う B が優先。</td></tr></table>",
        "tips": [
            "DB パスワードの自動ローテーション → Secrets Manager（Lambda ローテーターを組み込み）",
            "Parameter Store SecureString → ローテーション機能なし。静的シークレット管理向け",
            "Secrets Manager vs Parameter Store → ローテーション・バージョン管理が必要なら Secrets Manager"
        ]
    },
    218: {
        "perspective": "ステートフルセッションを持つ Web アプリをスケーラブルにするには何を組み合わせるか？",
        "detail": "<strong>判断の決め手：「セッションをメモリに保持するステートフル構成」「需要急増への自動スケール」「コスト最適」。</strong><br><br><strong>正解 D</strong>：ALB のスティッキーセッションで同一ユーザーを同一インスタンスに固定しつつ、Auto Scaling でスケールアウト。Aurora Auto Scaling でリードレプリカを動的増減させ、ピーク時の読み取り負荷を分散する。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>NLB はレイヤー4のため HTTP セッションの概念がなく、スティッキーセッションのサポートが ALB と異なる。Web アプリに NLB は不適切。</td></tr><tr><td>B</td><td>ラウンドロビン + スティッキーなしでは、スケールアウト時にセッションが別インスタンスに割り当てられセッション喪失が起きる。</td></tr><tr><td>C</td><td>スケールアップ（垂直）のみでは需要変動への柔軟な対応ができず、コスト効率も悪い。</td></tr><tr><td>D</td><td>正解。ALB スティッキーセッション + Auto Scaling + Aurora Auto Scaling の三要素が揃った最適解。</td></tr></table>",
        "tips": [
            "「セッションをメモリに保持するステートフル Web アプリ」→ ALB のスティッキーセッション",
            "Aurora の読み取りスケール → Aurora Auto Scaling でリードレプリカを自動増減",
            "NLB はレイヤー4（TCP）→ HTTP セッションのスティッキーには不適切"
        ]
    },
    219: {
        "perspective": "数千 TB の S3 コンテンツのバックアップ先として RTO 6時間を満たすストレージクラスは？",
        "detail": "<strong>判断の決め手：「RTO 6時間以内」「災害復旧」「バックアップコスト最適化」。</strong><br><br><strong>正解 B＋C</strong>：B はレプリケーション先を Standard-IA（30日後）→ Glacier Flexible Retrieval（90日後）へ段階移行。Glacier Flexible Retrieval の標準取り出しは3〜5時間でRTO 6時間に収まる。C はプライマリバケットを Intelligent-Tiering で自動階層化しコスト最適化。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>Glacier Deep Archive は取り出しに12〜48時間かかり、RTO 6時間を超える可能性が高い。</td></tr><tr><td>B</td><td>正解。Glacier Flexible Retrieval（3〜5時間）でRTO 6時間以内を達成。段階移行でコスト最適化。</td></tr><tr><td>C</td><td>正解。Intelligent-Tiering はアクセスパターン不明のプライマリバケットに最適な自動階層化。</td></tr><tr><td>D</td><td>Glacier Deep Archive（180日後移行）はコスト安だがRTO 6時間の要件を満たせない。</td></tr><tr><td>E</td><td>プライマリバケットを Intelligent-Tiering に移行させるのは C と重複。ライフサイクルで同日移行は意味がない。</td></tr></table>",
        "tips": [
            "RTO 6時間以内 → Glacier Flexible Retrieval（3〜5時間取り出し）が上限",
            "Glacier Deep Archive → 取り出し12〜48時間。RTO 6時間未満には不適",
            "「アクセスパターン不明な大量データ」→ Intelligent-Tiering で自動コスト最適化"
        ]
    },
    220: {
        "perspective": "「1時間に数回のデプロイ」「障害時に即時切り戻し」を実現する CI/CD 設計は？",
        "detail": "<strong>判断の決め手：「高頻度デプロイ」「即時ロールバック」「ダウンタイムゼロ」。</strong><br><br><strong>正解 D</strong>：CodePipeline + CodeBuild + CodeDeploy ブルーグリーンデプロイの組み合わせが、フルマネージドな CI/CD とゼロダウンタイム・即時ロールバックを同時に実現する AWS ネイティブな最適解。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>AMI 作成ごとにビルドするローリングデプロイは時間がかかり「1時間に数回」のデプロイには不向き。即時ロールバックも困難。</td></tr><tr><td>B</td><td>Run Command でコードを置き換えるのはインプレース更新であり、障害時のロールバックが複雑。</td></tr><tr><td>C</td><td>Beanstalk ブルーグリーンは URL Swap で切り替えできるが、CodeDeploy のブルーグリーンより柔軟性が低い。</td></tr><tr><td>D</td><td>正解。CodeDeploy ブルーグリーンは即時切り替え・即時ロールバックが可能。高頻度デプロイの最適解。</td></tr></table>",
        "tips": [
            "ゼロダウンタイム＋即時ロールバック → CodeDeploy ブルーグリーンデプロイ",
            "CodePipeline + CodeBuild + CodeDeploy → AWS ネイティブフルマネージド CI/CD の三点セット",
            "AMI 再作成ローリング → ビルド時間が長くなり高頻度デプロイに不適"
        ]
    },
    221: {
        "perspective": "VPC 内から AWS パブリックサービスへ「プライベート IP のみで接続」するには何が必要か？",
        "detail": "<strong>判断の決め手：「インターネット経由禁止」「プライベート IP で完結」「KMS・Secrets Manager 接続」。</strong><br><br><strong>正解 A</strong>：インターフェイスエンドポイントのプライベート DNS を有効にすると、KMS や Secrets Manager の標準 FQDN が VPC 内でエンドポイントのプライベート IP に解決される。アプリのコード変更なしにプライベート接続が実現する。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>正解。プライベート DNS 有効化でサービスの FQDN をプライベート IP に解決。コード変更不要。</td></tr><tr><td>B</td><td>インターフェイスエンドポイントへのルートは自動追加される。専用ルートの手動追加は不要で、これだけでは DNS 解決が変わらない。</td></tr><tr><td>C</td><td>セキュリティグループの設定は通信許可に必要だが、DNS 解決の問題は解決しない。単独では不十分。</td></tr><tr><td>D</td><td>Route 53 プライベートホストゾーンで手動 A レコードを登録するのは、プライベート DNS 有効化の代替だが管理が複雑で IP 変更に対応できない。</td></tr></table>",
        "tips": [
            "VPC → AWS サービスをプライベート接続 → インターフェイスエンドポイント（PrivateLink）",
            "プライベート DNS 有効化 → 標準 FQDN がエンドポイントのプライベート IP に解決",
            "ゲートウェイエンドポイント（S3/DynamoDB）→ ルートテーブル変更。DNS 設定は不要"
        ]
    },
    222: {
        "perspective": "プライベートサブネットの Fargate タスクがパブリック IP なしで ECR からイメージを取得するには？",
        "detail": "<strong>判断の決め手：「パブリック IP なし」「プライベートサブネット」「ECR からのイメージ取得」「セキュリティ要件」。</strong><br><br><strong>正解 B</strong>：ECR へのインターフェイスエンドポイント（PrivateLink）を作成することで、Fargate タスクはパブリック IP なしでプライベートネットワーク経由でイメージを取得できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>Fargate のネットワークモードは awsvpc のみ対応。bridge モードには変更できない。</td></tr><tr><td>B</td><td>正解。ECR の VPC エンドポイント（PrivateLink）でインターネット不使用のプライベートイメージ取得が可能。</td></tr><tr><td>C</td><td>パブリック IP を有効化するとインターネット経由になり、「パブリック IP なし」のセキュリティ要件に反する。</td></tr><tr><td>D</td><td>NAT Gateway 経由はインターネットを通るため、「パブリック IP なし」「プライベート通信完結」の要件に反する。</td></tr></table>",
        "tips": [
            "プライベートサブネットの Fargate → ECR 接続 → VPC インターフェイスエンドポイント",
            "Fargate は awsvpc ネットワークモードのみ。bridge/host は使用不可",
            "ECR の PrivateLink → ecr.dkr と ecr.api の2つのエンドポイントが必要"
        ]
    },
    223: {
        "perspective": "オンプレミス DNS からクロス VPC の Route 53 プライベートホストゾーンを解決するには？",
        "detail": "<strong>判断の決め手：「オンプレミス DNS が外部問い合わせ禁止」「複数 VPC の AWS ドメインをオンプレから解決」。</strong><br><br><strong>正解 D</strong>：プライベートホストゾーンを全 VPC に関連付け、Route 53 インバウンドリゾルバーエンドポイントをオンプレミスからの DNS 転送先として設定する。TGW で VPC 間をルーティングする組み合わせが最もシンプルで高可用。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A/C</td><td>アウトバウンドエンドポイントは VPC からオンプレへ問い合わせる方向。オンプレからの問い合わせ受付にはインバウンドエンドポイントが必要。</td></tr><tr><td>B</td><td>EC2 DNS フォワーダーは単一障害点になり、マネージドなインバウンドエンドポイントより可用性が低い。</td></tr><tr><td>D</td><td>正解。インバウンドエンドポイントがオンプレからの DNS クエリを受け付け、プライベートホストゾーンで解決する正しい方向性。</td></tr></table>",
        "tips": [
            "オンプレ → AWS ドメイン解決 → Route 53 インバウンドリゾルバーエンドポイント",
            "AWS → オンプレ DNS 解決 → Route 53 アウトバウンドリゾルバーエンドポイント",
            "プライベートホストゾーンの関連付け → クエリを受ける VPC すべてに関連付けが必要"
        ]
    },
    224: {
        "perspective": "100 MB 超の大容量アップロードを認証付きで高速化する最小変更のアーキテクチャは？",
        "detail": "<strong>判断の決め手：「100 MB 超の動画アップロードが遅い」「認証済みユーザーのみ許可」「最小運用」。</strong><br><br><strong>正解 B</strong>：S3 Transfer Acceleration はエッジロケーション経由で大容量アップロードを高速化し、マルチパートアップロードとの組み合わせで信頼性も向上する。最小の設定変更で既存の事前署名 URL の仕組みを維持できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>API Gateway の 10 MB ペイロード制限により、100 MB 超のファイルアップロードは不可。</td></tr><tr><td>B</td><td>正解。Transfer Acceleration + マルチパートで大容量を高速・確実にアップロード。既存の認証フローを変更不要。</td></tr><tr><td>C</td><td>API Gateway エッジ最適化 + S3 統合も 10 MB 制限が障壁。大容量転送には向かない。</td></tr><tr><td>D</td><td>CloudFront は PUT/POST を有効化できるが、OAI と s3:PutObject の組み合わせは設定が複雑で Transfer Acceleration より利点が少ない。</td></tr></table>",
        "tips": [
            "S3 大容量アップロードの高速化 → Transfer Acceleration + マルチパートアップロード",
            "API Gateway のペイロード制限 → 最大 10 MB。それ以上のファイル転送には使用不可",
            "Transfer Acceleration → S3 バケットで有効化するだけ。アクセラレータエンドポイントを使用"
        ]
    },
    225: {
        "perspective": "マルチリージョン DR 構成を最小コードで自動化するための IaC・DNS・DB の三点セットは？",
        "detail": "<strong>判断の決め手：「少人数運用」「IaC 自動展開」「マルチリージョン DR」「DynamoDB レプリケーション」。</strong><br><br><strong>正解 B＋E＋F</strong>：CloudFormation でインフラをコード化（E）、DynamoDB グローバルテーブルでマルチリージョン同期（B）、Route 53 レイテンシーベースルーティングで近いリージョンに自動誘導（F）という三要素が揃う。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>手動での環境構築はヒューマンエラーのリスクが高く、IaC 方針に反する。</td></tr><tr><td>B</td><td>正解。DynamoDB Streams を有効化してグローバルテーブルに拡張するのが公式推奨の移行手順。</td></tr><tr><td>C</td><td>新しいテーブルを作って全コピーは移行中のデータ整合性リスクがある。既存テーブルのグローバルテーブル化が優先。</td></tr><tr><td>D</td><td>50%均等振り分けは一方のリージョンに問題があっても半分のトラフィックが流れ続ける。フェイルオーバーが不完全。</td></tr><tr><td>E</td><td>正解。CloudFormation でリージョン差分をパラメータ化し、同一テンプレートで複数リージョン展開。</td></tr><tr><td>F</td><td>正解。レイテンシーベースルーティングでユーザーに近いリージョンへ自動誘導し、DR 時はフェイルオーバーを構成。</td></tr></table>",
        "tips": [
            "DynamoDB のマルチリージョン → Streams 有効化 → グローバルテーブルへの拡張",
            "CloudFormation マルチリージョン → リージョンをパラメータ化して同一テンプレートを再利用",
            "Route 53 レイテンシーベースルーティング → 最も近いリージョンへ自動誘導"
        ]
    },
    226: {
        "perspective": "全 AWS アカウントで S3 アクセスポイントを VPC 経由のみに強制するガバナンス設計は？",
        "detail": "<strong>判断の決め手：「数百アカウントに一律に適用」「チームは自由に S3 アクセスポイントを作成できる」「VPC 以外のアクセスポイントを禁止」。</strong><br><br><strong>正解 A</strong>：Organizations の SCP で s3:CreateAccessPoint に条件キー s3:AccessPointNetworkOrigin を VPC に限定する制御を付けることで、全アカウントに一律かつスケーラブルに適用できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>正解。SCP で一元的に VPC 以外のアクセスポイント作成を禁止。数百アカウントに即時適用。</td></tr><tr><td>B</td><td>S3 バケットポリシーは個々のバケットへの手動設定が必要で、スケーラブルでない。</td></tr><tr><td>C</td><td>アクセスポイントポリシーの手動編集は、作成後の後付け対応であり予防的制御にならない。</td></tr><tr><td>D</td><td>IAM ポリシーの配布は CloudFormation StackSets でも可能だが、開発者のロール設定漏れで迂回できる。SCP が最も強制力がある。</td></tr></table>",
        "tips": [
            "「全アカウントに一律強制」→ Organizations の SCP が最も強力で漏れなし",
            "s3:AccessPointNetworkOrigin 条件キー → VPC / Internet を区別",
            "SCP は IAM ポリシーより優先。個人のロールでは回避できない"
        ]
    },
    227: {
        "perspective": "5リージョン・75VPC以上の大規模マルチリージョン接続を「数分で拡張可能」にするには？",
        "detail": "<strong>判断の決め手：「5リージョン・各15 VPC以上」「数分で新規ネットワーク拡張」「オンプレとの接続も必要」。</strong><br><br><strong>正解 C</strong>：各リージョンに Transit Gateway を配置し TGW ピアリングでリージョン間を接続、オンプレとは Direct Connect を中心リージョン TGW に集約する設計が、スケーラブルで運用効率が高い。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>オンプレにトラフィックを集約するヘアピンルーティングは遅延が増大し、DC が帯域ボトルネックになる。</td></tr><tr><td>B</td><td>VPC ピアリングフルメッシュは n*(n-1)/2 の接続数が必要で、75 VPC では 2775 接続が必要になる。非現実的。</td></tr><tr><td>C</td><td>正解。TGW + TGW ピアリングはハブ＆スポーク型で最もスケーラブル。新規 VPC の追加が最小手順で完了。</td></tr><tr><td>D</td><td>VPN 中心でクラウド内ハブを使わないと、VPC 間通信がオンプレ経由になり非効率。</td></tr></table>",
        "tips": [
            "大規模マルチ VPC 接続 → Transit Gateway（TGW）がスケーラブルな唯一解",
            "リージョン間の TGW 接続 → TGW ピアリング（Transit Gateway Peering）",
            "VPC ピアリングフルメッシュ → n*(n-1)/2 の接続数になり大規模では管理不能"
        ]
    },
    228: {
        "perspective": "分単位で数百万件の IoT ログを低レイテンシ検索＋自動削除で管理するには？",
        "detail": "<strong>判断の決め手：「1分あたり数百万件」「4 KB 未満」「低レイテンシ検索」「完全マネージド・自動スケール」「120日後自動削除」。</strong><br><br><strong>正解 C</strong>：DynamoDB は書き込みスループットを自動スケールし、TTL で期限切れデータを自動削除できる。パーティションキー設計でミリ秒の低レイテンシ読み取りを実現できる唯一のフルマネージドサービス。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>RDS は接続数・書き込みスループットに上限があり、毎分数百万件の大量書き込みはスケールアウトできない。</td></tr><tr><td>B</td><td>レコードを1件ずつ CSV として S3 に保存するのはオブジェクト数が膨大になり、検索も極めて非効率。</td></tr><tr><td>C</td><td>正解。DynamoDB + TTL が自動スケール・低レイテンシ・自動削除の三要件を全て満たす。</td></tr><tr><td>D</td><td>S3 + Athena は分析クエリに向くが、ミリ秒以下の「直近データの即時検索」には不向き。</td></tr></table>",
        "tips": [
            "「高スループット書き込み＋低レイテンシ検索」→ DynamoDB が最適",
            "DynamoDB TTL → 指定属性の Unix タイムスタンプで期限切れ項目を自動削除（コスト無料）",
            "S3 + Athena → 大規模分析向き。ミリ秒レイテンシの即時検索には不向き"
        ]
    },
    229: {
        "perspective": "Lambda から RDS への大量接続によるコネクション枯渇を解決する最適な方法は？",
        "detail": "<strong>判断の決め手：「Lambda の大量同時接続で DB 接続上限に達する」「接続管理のマネージド化」。</strong><br><br><strong>正解 B</strong>：RDS Proxy は Lambda からの大量接続をプールして DB 側の接続数を削減する専用マネージドサービス。Aurora と組み合わせることで読み取り負荷分散も実現できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>Lambda ハンドラ外の接続プールは同一コンテナ再利用時には有効だが、大量の同時 Lambda 実行では各コンテナが独立した接続を持つため、接続数の問題は解決しない。</td></tr><tr><td>B</td><td>正解。RDS Proxy が接続プールをマネージドに管理。Lambda 大量実行時の接続数爆発を根本解決。</td></tr><tr><td>C</td><td>リードレプリカを手動追加する方法は接続数問題の直接解決にならず、手動スケールは運用負荷が高い。</td></tr><tr><td>D</td><td>Route 53 加重レコードでレプリカへ直接振り分けるのは DNS の特性上タイムラグがあり、接続管理にはなっていない。</td></tr></table>",
        "tips": [
            "Lambda → RDS の接続数爆発 → RDS Proxy でコネクションプーリング",
            "RDS Proxy は Lambda の同時実行数に関わらず DB への接続数を一定に保つ",
            "Aurora Replica → 読み取りスケール。接続数問題の解決には RDS Proxy が必要"
        ]
    },
    230: {
        "perspective": "WorkSpaces への接続を特定拠点 IP からのみに制限するには何を使うか？",
        "detail": "<strong>判断の決め手：「支店などの特定 IP アドレスからのみ WorkSpaces に接続を許可」。</strong><br><br><strong>正解 B</strong>：WorkSpaces の IP アクセスコントロールグループは、許可する IP レンジを定義してディレクトリに関連付けることで、指定 IP 以外からのアクセスを WorkSpaces レベルで制限できる専用機能。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>Firewall Manager は WAF ルールやセキュリティグループポリシーの管理ツール。WorkSpaces のアクセス制御には直接使用しない。</td></tr><tr><td>B</td><td>正解。IP アクセスコントロールグループが WorkSpaces 専用のネイティブな IP 制限機能。</td></tr><tr><td>C</td><td>クライアント証明書は WorkSpaces の標準機能では対応しておらず、実装が複雑で現実的でない。</td></tr><tr><td>D</td><td>OS レベルの Windows ファイアウォールは WorkSpaces イメージに組み込めるが、管理が分散し更新が困難。</td></tr></table>",
        "tips": [
            "WorkSpaces の接続元 IP 制限 → IP アクセスコントロールグループをディレクトリに関連付け",
            "Firewall Manager → WAF・セキュリティグループの組織横断管理。WorkSpaces 直接制御ではない",
            "WorkSpaces → AD ディレクトリ単位でのアクセス制御が基本単位"
        ]
    },
    231: {
        "perspective": "マルチアカウント・マルチサービス環境で最も柔軟かつコスト効率の高い割引プランは？",
        "detail": "<strong>判断の決め手：「EC2・Fargate・Lambda を使用」「負荷変動が大きい」「組織全体での適用」。</strong><br><br><strong>正解 B</strong>：Compute Savings Plans は EC2・Fargate・Lambda を横断して適用でき、インスタンスタイプ・リージョン・OS を問わず自動適用される。組織全体への3年契約で最大割引を得ながら柔軟性も高い。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>Standard RI は特定インスタンスタイプに固定され、負荷変動が大きい環境では余らせるリスクが高い。</td></tr><tr><td>B</td><td>正解。Compute Savings Plans は EC2/Fargate/Lambda 横断適用で最も柔軟。組織全体で恩恵を受けられる。</td></tr><tr><td>C</td><td>EC2 Instance Savings Plans はインスタンスファミリーとリージョンに縛られる。Fargate/Lambda には適用されない。</td></tr><tr><td>D</td><td>Standard RI をメンバーアカウントから購入すると管理が分散し、組織全体最適化の機会を逸する。</td></tr></table>",
        "tips": [
            "Compute Savings Plans → EC2・Fargate・Lambda に横断適用。最も柔軟",
            "EC2 Instance Savings Plans → 特定ファミリー・リージョン限定。Fargate/Lambda には不適用",
            "Standard RI → 最大割引だがインスタンスタイプ固定で柔軟性ゼロ"
        ]
    },
    232: {
        "perspective": "「インターネット経由禁止」という金融規制下で5TBのDB をオンプレから RDS へ継続レプリケーション移行するには？",
        "detail": "<strong>判断の決め手：「インターネット経由禁止」「継続的なレプリケーション（CDC）」「ダウンタイム最小化」。</strong><br><br><strong>正解 C</strong>：DMS を Direct Connect 経由でプライベートサブネットにデプロイし、継続的な変更データキャプチャ（CDC）でオンプレ MySQL から RDS へ切れ目なくレプリケーションする。インターネット不使用かつ本番稼働中の移行が実現できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>File Gateway + S3 + バックアップリストアは一時点のデータしか移行できず、継続的な CDC にならない。</td></tr><tr><td>B</td><td>Snowball はインターネット不使用だがオフライン転送のため、継続的な変更レプリケーションには対応できない。</td></tr><tr><td>C</td><td>正解。DMS + Direct Connect は継続 CDC かつプライベート接続。金融規制とダウンタイム最小化を両立。</td></tr><tr><td>D</td><td>DataSync は大量ファイル転送向け。MySQL の CDC（増分レプリケーション）はサポートしない。</td></tr></table>",
        "tips": [
            "「インターネット禁止＋継続 CDC」→ DMS + Direct Connect プライベートサブネット",
            "DMS CDC → binlog レプリケーションで本番稼働中の DB を継続的に同期",
            "Snowball/DataSync → 一括・スケジュール転送向き。リアルタイム CDC には不適"
        ]
    },
    233: {
        "perspective": "RPO/RTO を短くしつつ Aurora と DynamoDB を両方マルチリージョン DR 対応するには？",
        "detail": "<strong>判断の決め手：「2サービスのデータを両方セカンダリリージョンへ」「低 RPO」「DR 対応」。</strong><br><br><strong>正解 B</strong>：AWS Backup でのクロスリージョンコピーは運用シンプルで両サービスに対応し、障害時はバックアップからリストアして両リージョンで起動できる。RPO はバックアップ頻度に依存するが、実装の確実性が高い。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>DMS による継続レプリケーションは有効だが、DynamoDB についてのレプリケーションに DMS は不適。設計が不完全。</td></tr><tr><td>B</td><td>正解。AWS Backup のクロスリージョンコピーは Aurora と DynamoDB 両方に対応し、一元管理できる。</td></tr><tr><td>C</td><td>Aurora Global Database + DynamoDB グローバルテーブルは RPO をほぼゼロにできるが、コストが高くオーバースペックになりやすい。</td></tr><tr><td>D</td><td>マルチ AZ は単一リージョン内の障害対応のみ。リージョン障害への DR にはならない。</td></tr></table>",
        "tips": [
            "Aurora と DynamoDB の両方をクロスリージョン DR → AWS Backup のクロスリージョンコピー",
            "Aurora Global Database → RPO ほぼゼロだがコスト高",
            "DynamoDB グローバルテーブル → マルチリージョン書き込み可能だが Aurora と別管理になる"
        ]
    },
    234: {
        "perspective": "「金曜夜集中・SQL 集計・API 24時間稼働」という3要件を満たすサーバーレスアーキテクチャは？",
        "detail": "<strong>判断の決め手：「提出受付は24時間停止不可」「自動スケール」「SQL 形式の集計レポート」「コスト最適」。</strong><br><br><strong>正解 B＋C</strong>：Parquet/ORC + S3 + Athena で SQL 集計を実現（B）、API Gateway + Lambda + DynamoDB のサーバーレスで24時間自動スケールの受付 API を構築（C）。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>Redshift は大規模 DWH 向きで、タイムシート程度のデータに対してはオーバースペックかつ高コスト。</td></tr><tr><td>B</td><td>正解。S3 + Athena は SQL クエリ対応のサーバーレス分析基盤。Parquet 形式で低コストかつ高速。</td></tr><tr><td>C</td><td>正解。API Gateway + Lambda + DynamoDB は24時間自動スケール可能なサーバーレス受付 API の模範解答。</td></tr><tr><td>D</td><td>EC2 は常時起動で固定コストが高く、「通常時コストを抑えたい」要件に反する。手動スケールも手間。</td></tr><tr><td>E</td><td>ECS EC2 起動タイプはサーバーレスではなく、スケジュール起動も手動管理が残る。</td></tr></table>",
        "tips": [
            "「タイムシート集計を SQL で」→ S3（Parquet/ORC）+ Athena のサーバーレス分析",
            "「24時間停止不可 API」→ API Gateway + Lambda + DynamoDB のサーバーレス三点セット",
            "Redshift → TB 規模の継続的 DWH 向き。小規模集計には Athena の方が低コスト"
        ]
    },
    235: {
        "perspective": "ALB 背後の EC2 へのリクエストを「クライアント IP・ユーザーエージェント含め」最小コストで記録するには？",
        "detail": "<strong>判断の決め手：「クライアント IP・接続タイプ・ユーザーエージェント」「最小コスト・管理負荷」。</strong><br><br><strong>正解 B</strong>：ALB アクセスログには X-Forwarded-For（クライアント IP）・ユーザーエージェント・接続タイプなどの HTTP 情報が含まれる。S3 保存後に Athena でクエリできる最低コストな構成。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>詳細モニタリング + Kinesis + OpenSearch は高機能だがコストが大幅に増加する。要件に対してオーバースペック。</td></tr><tr><td>B</td><td>正解。ALB アクセスログは必要情報を全て含み、S3 + Athena で低コストにクエリ可能。</td></tr><tr><td>C</td><td>トラフィックミラーリングは全パケットをコピーするため、コストと処理負荷が非常に高い。HTTP ヘッダーの分析には ALB ログで十分。</td></tr><tr><td>D</td><td>VPC Flow Logs は IP/ポートレベルのネットワーク情報のみ。ユーザーエージェントなどの HTTP ヘッダー情報は含まない。</td></tr></table>",
        "tips": [
            "HTTP アクセスログ（クライアント IP・UA 含む） → ALB アクセスログ + S3 + Athena",
            "VPC Flow Logs → IP/ポート/プロトコルのネットワーク層情報のみ。HTTP ヘッダーは含まない",
            "トラフィックミラーリング → 全パケットキャプチャ。コスト高でセキュリティ調査用途が多い"
        ]
    },
    236: {
        "perspective": "ミリ秒単位の低レイテンシが求められる9ノードの分散インメモリDBクラスタに最適な配置は？",
        "detail": "<strong>判断の決め手：「ミリ秒単位の応答」「9ノードのインメモリクラスタ」「ネットワーク待ち時間の最小化」。</strong><br><br><strong>正解 D</strong>：クラスタープレイスメントグループは同一 AZ の同一ラック近傍に EC2 を集約し、ノード間のネットワーク遅延を最小化する。メモリ最適化インスタンスで大容量のインメモリ DB を確保できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>スプレッドプレイスメントグループは障害分離向きで、ノードを分散配置するため逆にレイテンシが増大する。</td></tr><tr><td>B</td><td>マルチ AZ のパーティションプレイスメントグループはレイテンシが AZ 間通信分増加し、低レイテンシ要件に反する。</td></tr><tr><td>C</td><td>パーティションプレイスメントグループのコンピュート最適化は、インメモリ DB よりも計算負荷向け。大容量メモリには不適。</td></tr><tr><td>D</td><td>正解。クラスタープレイスメントグループ + メモリ最適化インスタンスが低レイテンシ・大容量インメモリDBの最適解。</td></tr></table>",
        "tips": [
            "ノード間レイテンシ最小化 → クラスタープレイスメントグループ（同一 AZ 集約）",
            "スプレッドプレイスメントグループ → 障害分離目的。レイテンシは向上しない",
            "インメモリ DB → メモリ最適化インスタンス（r 系・x 系）を選択"
        ]
    },
    237: {
        "perspective": "特定 IP から大量ログイン失敗が続く場合の WAF 自動ブロックの最適実装は？",
        "detail": "<strong>判断の決め手：「500 ユニーク IP から大量ログイン失敗」「自動対処」「ALB 前段での制御」。</strong><br><br><strong>正解 C</strong>：WAF のレートベースルールは一定時間内にしきい値を超えたリクエスト元 IP を自動的にブロックする機能で、クレデンシャルスタッフィング攻撃への自動対応に最適。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>手動で IP を登録するのでは、500 ユニーク IP に対応するのが追いつかず、根本解決にならない。</td></tr><tr><td>B</td><td>Firewall Manager でセキュリティグループを管理する方式は、IP 個別拒否ルールを手動追加するもので自動化できない。</td></tr><tr><td>C</td><td>正解。WAF レートベースルールで自動的にしきい値超えの IP をブロック。管理不要で即効性がある。</td></tr><tr><td>D</td><td>全インターネットアクセスを遮断すると一般ユーザーも使えなくなり、ビジネス要件に反する。</td></tr></table>",
        "tips": [
            "「特定 IP から大量リクエスト → 自動ブロック」→ WAF レートベースルール",
            "WAF IP セットルール → 手動 IP 登録。自動検出・自動ブロックには使えない",
            "WAF レートベースルール → しきい値（例: 5分で1000件）超過した IP を自動ブロック"
        ]
    },
    238: {
        "perspective": "単一 AZ 構成・大型インスタンス2台のシステムをスケーラブルかつコスト効率よく高可用化するには？",
        "detail": "<strong>判断の決め手：「単一 AZ」「大型インスタンス2台」「コスト最適化」「高可用性」。</strong><br><br><strong>正解 C</strong>：Aurora MySQL（自動フェイルオーバー）+ Aurora レプリカ（読み取りスケール）と、小さなインスタンスを複数 AZ に分散した Auto Scaling グループの組み合わせが、可用性・スケール・コスト効率を同時に最適化する。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>RDS Multi-AZ は DB の可用性を上げるが、EC2 を2台に固定して Auto Scaling なしでは Web 層のスケーラビリティがない。</td></tr><tr><td>B</td><td>マルチリージョンは費用が高く、単一リージョン高可用化には過剰投資。リードレプリカだけでは DB フェイルオーバーが自動化されない。</td></tr><tr><td>C</td><td>正解。Aurora 自動フェイルオーバー + 小インスタンス多数の ASG でコスト効率最高かつ高可用。</td></tr><tr><td>D</td><td>DynamoDB は KV/ドキュメント型。複雑な SQL クエリを持つ既存 RDS MySQL の置き換えには大幅なコード変更が必要。</td></tr></table>",
        "tips": [
            "RDS → Aurora 移行のメリット → 自動フェイルオーバー・読み取りレプリカ・ストレージ自動拡張",
            "「大型インスタンス2台」→ 小インスタンス複数 + Auto Scaling に変えてコスト削減",
            "Aurora レプリカ → リードレプリカ + フェイルオーバーターゲットを兼ねる"
        ]
    },
    239: {
        "perspective": "10 VPC から単一サービス VPC への接続を CIDR 重複リスクなく疎結合に実現するには？",
        "detail": "<strong>判断の決め手：「最大10 VPC のクライアント」「CIDR 重複の可能性」「サービス提供側 NLB を公開」。</strong><br><br><strong>正解 D</strong>：NLB をエンドポイントサービス（AWS PrivateLink）として公開することで、CIDR 重複に関わらず各 VPC から安全にアクセスできる。ホワイトリストで接続 VPC を制御でき、疎結合な設計が実現する。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>VPC ピアリングは CIDR が重複すると接続できない。また双方向のルートテーブル更新が必要で管理が複雑。</td></tr><tr><td>B</td><td>Transit Gateway は VPC 間通信を可能にするが、接続した VPC が全て互いに通信できてしまい過剰なアクセス権限を与える。</td></tr><tr><td>C</td><td>Site-to-Site VPN は BGP 設定など運用が複雑で、VPC 間内部接続には不適切。</td></tr><tr><td>D</td><td>正解。PrivateLink はエンドポイントサービスとして公開し、ホワイトリスト制御付きで CIDR 重複なしに接続可能。</td></tr></table>",
        "tips": [
            "「CIDR 重複の可能性がある VPC 間で単方向サービス公開」→ AWS PrivateLink（エンドポイントサービス）",
            "VPC ピアリング → CIDR 重複不可・双方向通信になる",
            "PrivateLink → 片方向のサービス公開。消費者 VPC はサービス VPC の内部に直接アクセスできない"
        ]
    },
    240: {
        "perspective": "クロスアカウントで Route 53 プライベートホストゾーンを VPC に関連付ける正しい手順は？",
        "detail": "<strong>判断の決め手：「アカウント A のプライベートホストゾーン」「アカウント B の新 VPC からの名前解決」。</strong><br><br><strong>正解 B＋E</strong>：まず E でアカウント A のホストゾーンにアカウント B の VPC の関連付け許可（association authorization）を作成し、次に B でアカウント B 側から関連付けを実行する。完了後は許可を削除しても関連付けは維持される。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>IP アドレスをローカル設定に書き込む方式は RDS エンドポイントの IP 変更（フェイルオーバー等）に対応できない。</td></tr><tr><td>B</td><td>正解。関連付け許可（E）を受けた後、アカウント B 側から関連付けを実行する。完了後に許可を削除してもよい。</td></tr><tr><td>C</td><td>新しく EC2 MySQL を構築することは要件（RDS エンドポイントのプライベートホストゾーン登録）と全く異なる。</td></tr><tr><td>D</td><td>プライベートホストゾーンで NS レコードによる委任設定はサポートされていない。</td></tr><tr><td>E</td><td>正解。アカウント A 側でまず関連付け許可を作成する。これが先決条件。</td></tr></table>",
        "tips": [
            "クロスアカウントのホストゾーン関連付け → 許可作成（アカウントA）→ 関連付け実行（アカウントB）の2ステップ",
            "関連付け許可は完了後に削除可能（関連付け自体は維持される）",
            "プライベートホストゾーンの NS 委任 → サポートされていない（パブリックとは異なる）"
        ]
    },
    241: {
        "perspective": "6時間の夜間バッチを最低コストで処理するEMRクラスタ設計は？",
        "detail": "<strong>判断の決め手：「夜間のみ稼働」「完了速度は最重要でない」「コスト削減」「既存ジョブ定義変更なし」。</strong><br><br><strong>正解 A</strong>：マスター/コアはオンデマンドで信頼性を確保し、タスクノード（処理容量）はスポットで大幅コスト削減。バッチ完了後はクラスター全体を自動終了することで24時間分の無駄な課金をなくす。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>正解。マスター/コア オンデマンド + タスク スポット + 自動終了 + Savings Plans が最適コスト設計。</td></tr><tr><td>B</td><td>マスター/コアをスポットにすると突然の中断でクラスタ全体が失敗するリスクがある。</td></tr><tr><td>C</td><td>タスクノードのみ終了してマスター/コアを24時間稼働させると、停止コストの削減効果が限定的。</td></tr><tr><td>D</td><td>全ノードオンデマンドの手動終了では Savings Plans の効果が小さく、手動運用コストが残る。</td></tr></table>",
        "tips": [
            "EMR タスクノード → スポットインスタンスで大幅コスト削減（失敗しても HDFS に影響なし）",
            "EMR マスター/コアノード → スポット中断でクラスタが壊れるためオンデマンドが原則",
            "バッチ完了後の自動終了 → EMR の自動終了設定（--auto-terminate）で24時間課金を防止"
        ]
    },
    242: {
        "perspective": "「一件も失わず」「突発的大量書き込み」を既存テーブル変更なしに吸収するアーキテクチャは？",
        "detail": "<strong>判断の決め手：「既存テーブル変更不可」「秒間数万件の書き込みスパイク」「一件も失えない（永続化保証）」。</strong><br><br><strong>正解 C</strong>：SQS でリクエストをバッファリングし、Lambda が自動スケールしながら順次 RDS に書き込む。キューによりピーク負荷を平滑化でき、SQS の耐久性でデータロストも防止できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>DynamoDB 移行はテーブル・アプリケーションの大幅変更が必要で「既存テーブル変更不可」に反する。</td></tr><tr><td>B</td><td>スケールアップは上限があり、秒間数万件のスパイクを確実に処理できる保証がない。直接書き込みでの負荷吸収は限界がある。</td></tr><tr><td>C</td><td>正解。SQS で書き込みをバッファリングし Lambda が平滑化処理。データロストなし・スパイク吸収・テーブル変更不要。</td></tr><tr><td>D</td><td>ElastiCache Memcached は永続化機能がなく、キャッシュから RDS へのライトスルーの実装も複雑。データ喪失リスクがある。</td></tr></table>",
        "tips": [
            "「突発的書き込みスパイク＋データロストゼロ」→ SQS でバッファリング + Lambda で順次処理",
            "SQS の耐久性 → メッセージを複数 AZ に冗長保存。喪失リスクなし",
            "ElastiCache → キャッシュ（読み取り高速化）。ライトバッファとしては永続化保証なし"
        ]
    },
    243: {
        "perspective": "既存10アカウントを Organizations に統合し EC2 のみ許可するガバナンスを手作業ゼロで実現するには？",
        "detail": "<strong>判断の決め手：「既存アカウントの招待・統合」「EC2 以外を禁止する SCP」「追加アカウントも自動適用」。</strong><br><br><strong>正解 A＋C</strong>：Organizations を作成し既存アカウントを招待・OU に移動（C）、その OU に EC2 Allow のみの SCP をアタッチ（A）することで、追加アカウントを同じ OU に入れるだけで自動適用できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>正解。SCP で EC2 フルアクセスのみ許可・他を Deny する制御を OU レベルで一括適用。</td></tr><tr><td>B</td><td>OU を切るだけでは制御ポリシー（SCP）がなく、EC2 以外を禁止できない。単独では不完全。</td></tr><tr><td>C</td><td>正解。既存アカウントを招待して OU に配置するフローの確立が基盤。追加アカウントも同じ OU へ。</td></tr><tr><td>D</td><td>クロスアカウントロールだけでは他サービス利用を禁止できない。SCP によるサービス制限が必要。</td></tr><tr><td>E</td><td>VPC ピアリングはネットワーク接続のみ。サービス利用制御とは無関係。</td></tr></table>",
        "tips": [
            "既存アカウントを Organizations に統合 → 招待（Invite）してメンバーアカウントとして参加",
            "OU へのSCP アタッチ → その OU 配下の全アカウントに自動適用",
            "EC2 のみ許可する SCP → FullAWSAccess を外して EC2 Allow のみの SCP を適用"
        ]
    },
    244: {
        "perspective": "フィーチャーブランチを別アカウントでテストし本番品質を守る CI/CD 設計は？",
        "detail": "<strong>判断の決め手：「フィーチャーブランチごとのテスト自動化」「本番可用性の保護」「クロスアカウント分離」。</strong><br><br><strong>正解 A</strong>：フィーチャーブランチをトリガーに別 CodePipeline を起動し、CodeBuild でユニットテストを自動実行し、テスト用アカウントの S3 にステージングする設計が、本番を汚さずテストと本番を分離する最適解。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>正解。フィーチャーブランチ → 別パイプライン → CodeBuild テスト → テストアカウント S3 ステージング。本番との分離が完全。</td></tr><tr><td>B</td><td>Lambda でユニットテストを実装するのは複雑で、CodeBuild より実行環境の柔軟性が低い。</td></tr><tr><td>C</td><td>テストを通過したビルド成果物を本番アカウントの S3 に置くのは本番汚染リスクがある。</td></tr><tr><td>D</td><td>外部 Jenkins サーバーは管理負荷が高く、AWS ネイティブ環境から外れる。CodeBuild で十分。</td></tr></table>",
        "tips": [
            "フィーチャーブランチごとに別パイプライン → CodeCommit ブランチ → CodePipeline トリガー",
            "テスト環境 → 本番アカウントと分離した別アカウントで実行が理想",
            "CodeBuild → テスト実行・ビルド・Docker ビルドのフルマネージド環境"
        ]
    },
    245: {
        "perspective": "SNS → Lambda 経由で RDS への接続数爆発と処理失敗を同時に解決するには？",
        "detail": "<strong>判断の決め手：「Lambda からの大量接続で DB CPU 飽和」「5分以内の SLA 達成」「メッセージ欠落防止」。</strong><br><br><strong>正解 A＋D</strong>：RDS Proxy で接続数を制御（A）、SNS → SQS 標準キュー → Lambda でバッファリングと再試行を確保（D）。接続数問題と処理失敗の両方を同時に解決できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>正解。RDS Proxy が Lambda → DB 間のコネクションプールを管理し、接続数爆発を根本解決。</td></tr><tr><td>B</td><td>SNS の配信ポリシーによる再試行は Lambda 呼び出し失敗時のリトライであり、DB 側の接続数問題を解決しない。</td></tr><tr><td>C</td><td>FIFO キューは順序保証が目的。順序が必要なユースケースでなければ、スループットが標準キューより低く SLA 達成に不利。</td></tr><tr><td>D</td><td>正解。SNS → SQS 標準キューを挟むことで Lambda の同時実行数をキュー深度で制御でき、失敗時の再試行も自動化。</td></tr><tr><td>E</td><td>RDS Data API は Serverless v2 向けの HTTP API。接続数問題の解決にはならない。</td></tr></table>",
        "tips": [
            "「Lambda → RDS 接続数爆発」→ RDS Proxy でコネクションプール管理",
            "SNS → SQS → Lambda → DB のパターンでバッファリング＋再試行を確保",
            "SNS → Lambda 直結 → Lambda 同時実行数制限に達するとメッセージが失われる"
        ]
    },
    246: {
        "perspective": "NACL でプライベートサブネットの HTTP 受信と応答返却を正しく許可するルールは？",
        "detail": "<strong>判断の決め手：「NACL はステートレス」「プライベートサブネット NACL に ALB からの HTTP インバウンドと応答アウトバウンドが必要」。</strong><br><br><strong>正解 B＋D</strong>：B はALB（10.0.0.0/24）からのポート80インバウンドを許可。D は応答パケットをエフェメラルポート（1024-65535）でALB宛にアウトバウンド許可する。NACL はステートレスなのでインバウンドとアウトバウンドの両方を明示的に許可する必要がある。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>アウトバウンドで 0.0.0.0/0 のポート80を許可するのはインターネットへの HTTP 送信になり不要かつ過剰。</td></tr><tr><td>B</td><td>正解。ALB サブネット（10.0.0.0/24）からのポート80インバウンドを許可。最小権限で正確。</td></tr><tr><td>C</td><td>0.0.0.0/0 からのポート80を許可すると外部からも直接接続できてしまいセキュリティ監査の指摘に反する。</td></tr><tr><td>D</td><td>正解。NACL はステートレスなので応答パケット（エフェメラルポート）のアウトバウンドも明示的に許可が必要。</td></tr><tr><td>E</td><td>ALB宛のポート80アウトバウンドはリクエスト送信方向であり意図しない通信。応答にはエフェメラルポートを使う。</td></tr></table>",
        "tips": [
            "NACL はステートレス → インバウンドとアウトバウンドの両方を明示的に設定",
            "HTTP 応答パケット → 送信元はエフェメラルポート（1024-65535）",
            "セキュリティグループはステートフル → インバウンドを許可すれば応答は自動許可"
        ]
    },
    247: {
        "perspective": "読み取り主体のランキングクエリを既存 RDS 運用フローを変えずに高速化するには？",
        "detail": "<strong>判断の決め手：「SELECT クエリの遅延」「書き込みフローは変えない」「瞬間的読み取り負荷を自動吸収」「高可用性維持」。</strong><br><br><strong>正解 D</strong>：ElastiCache（Redis/Valkey）にランキングデータをキャッシュすることで、DB への読み取り負荷を大幅削減。RDS Multi-AZ の書き込みフローを変えずに読み取りのみを高速化できる。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>DynamoDB への移行は既存の複雑な SQL クエリ・テーブル設計の大幅変更が必要で「RDS 運用フローを変えない」に反する。</td></tr><tr><td>B</td><td>RDS 読み取りレプリカ + RDS Proxy は読み取りスケールに有効だが、レプリカラグやコストの面でキャッシュより劣る場合がある。</td></tr><tr><td>C</td><td>Kinesis + Redshift はリアルタイムクエリではなく分析向け。ランキング表示の低レイテンシ要件に不適。</td></tr><tr><td>D</td><td>正解。ElastiCache キャッシュは RDS への読み取りを削減し、ミリ秒レスポンスを実現。Multi-AZ で高可用性も維持。</td></tr></table>",
        "tips": [
            "「読み取り高速化・DB 負荷削減」→ ElastiCache（Redis/Memcached）でキャッシュ",
            "ElastiCache Redis の Sorted Set → リーダーボード（ランキング）の実装に最適",
            "RDS 読み取りレプリカ → 秒単位のレプリカラグあり。ミリ秒応答が必要な用途には ElastiCache が優先"
        ]
    },
    248: {
        "perspective": "S3 アップロード → Rekognition 解析 → モバイルプッシュ通知のサーバーレスパイプラインを組み立てるには？",
        "detail": "<strong>判断の決め手：「リアルタイム処理」「営業時間外のコスト抑制」「自動スケール」「即時プッシュ通知」。</strong><br><br><strong>正解 A＋B＋F</strong>：S3 → SQS 標準キュー（B）→ Lambda で Rekognition 解析（A）→ SNS モバイルプッシュ通知（F）の流れがサーバーレスかつ自動スケール・コスト最適のパイプライン。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>正解。Lambda が SQS をポーリングして Rekognition を呼び出す。自動スケール・停止コスト最小。</td></tr><tr><td>B</td><td>正解。S3 イベント → SQS キューでバッファリング。ピーク時のスパイクを吸収し Lambda に安定供給。</td></tr><tr><td>C</td><td>メールでプレビューを通知するのは「即時プレビュー」ではなく、体験が悪い。</td></tr><tr><td>D</td><td>Amazon MQ は S3 イベントのネイティブターゲットではなく、設定が複雑。SQS で十分。</td></tr><tr><td>E</td><td>S3 Batch Operations は既存オブジェクトへのバッチ処理向け。リアルタイム処理には不向き。</td></tr><tr><td>F</td><td>正解。SNS モバイルプッシュ通知（APNs/FCM）で処理完了を即座にアプリへ通知。</td></tr></table>",
        "tips": [
            "S3 イベント → SQS → Lambda が「イベント駆動リアルタイム処理」の定番パターン",
            "SNS モバイルプッシュ → APNs（iOS）/ FCM（Android）へのプッシュ通知",
            "S3 Batch Operations → 既存オブジェクトへの一括操作向け。新規アップロードのリアルタイム処理には不適"
        ]
    },
    249: {
        "perspective": "複数アカウントの EMR コストを部門単位で予算管理・通知するスケーラブルな仕組みは？",
        "detail": "<strong>判断の決め手：「部門単位で月次予算」「通知のみ（強制停止なし）」「IaC 化」「アカウント追加に自動対応」。</strong><br><br><strong>正解 C＋D</strong>：Service Catalog で標準 EMR テンプレートをセルフサービス提供（C）、CloudFormation テンプレートに AWS Budgets リソースを含めて予算と通知設定をコード化（D）。新規アカウントも同じテンプレートから展開するだけで自動適用。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>CloudWatch ダッシュボードの手動監視はスケーラブルでなく、予算超過の自動通知が得られない。</td></tr><tr><td>B</td><td>ブートストラップアクションから Cost Explorer API を呼ぶのは非標準で信頼性が低く、強制終了はビジネス要件に反する。</td></tr><tr><td>C</td><td>正解。Service Catalog で標準化したテンプレートを提供することで、チームが自律的に正しい設定で起動できる。</td></tr><tr><td>D</td><td>正解。AWS Budgets を CloudFormation でコード化することで、アカウント追加時も同じテンプレートで予算設定が自動化。</td></tr><tr><td>E</td><td>CloudTrail から独自コスト計算するのは精度が低く、予算管理機能としては不完全。</td></tr></table>",
        "tips": [
            "コスト予算管理と通知の自動化 → AWS Budgets の CloudFormation リソース化",
            "Service Catalog → 標準化されたインフラテンプレートのセルフサービス提供",
            "「アカウント追加に手作業ゼロで対応」→ CloudFormation StackSets または Service Catalog が選択肢"
        ]
    },
    250: {
        "perspective": "サーバーレス API をマルチリージョン展開し DynamoDB データをグローバルに同期するには？",
        "detail": "<strong>判断の決め手：「us-east-1 に同一 API を展開」「両リージョンから同一データへ即時アクセス」「Lambda は既存活用」。</strong><br><br><strong>正解 C＋D</strong>：us-east-1 に新しいリージョナル API Gateway + Lambda をデプロイ（C）、既存 DynamoDB テーブルをグローバルテーブルに変換して両リージョンで同一データに読み書きできるようにする（D）。<br><br><table border='1' cellpadding='4'><tr><th>選択肢</th><th>判定</th></tr><tr><td>A</td><td>DynamoDB に「読み取り専用レプリカ」は存在しない。グローバルテーブルは各リージョンで読み書き可能。</td></tr><tr><td>B</td><td>エッジ最適化エンドポイントへの変更は CloudFront 経由になるが、us-east-1 に独立した API をデプロイせず待機時間の短縮効果が限定的。</td></tr><tr><td>C</td><td>正解。us-east-1 に独立したリージョナル API Gateway + Lambda を展開。低レイテンシと冗長性を確保。</td></tr><tr><td>D</td><td>正解。DynamoDB グローバルテーブルで両リージョンがアクティブ-アクティブで読み書き可能。</td></tr><tr><td>E</td><td>DAX はリージョン内のキャッシュサービス。クロスリージョンのグローバルキャッシュとしては使用できない。</td></tr></table>",
        "tips": [
            "DynamoDB のマルチリージョン読み書き → グローバルテーブル（各リージョンがアクティブ-アクティブ）",
            "「API のマルチリージョン展開」→ 各リージョンにリージョナル API Gateway を独立デプロイ",
            "DAX → シングルリージョン内のメモリキャッシュ。グローバル共有キャッシュにはならない"
        ]
    }
}

# 書き込み直前にファイルを再読み込み
with open('/Users/aki/aws-sap/docs/data/questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# num 201〜250 の explanation のみ差し替え
updated_count = 0
for q in data:
    num = q.get('num', 0)
    if 201 <= num <= 250 and num in NEW_EXPLANATIONS:
        q['explanation'] = NEW_EXPLANATIONS[num]
        updated_count += 1

print(f'Updated {updated_count} questions')

# 保存
with open('/Users/aki/aws-sap/docs/data/questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Done.')
