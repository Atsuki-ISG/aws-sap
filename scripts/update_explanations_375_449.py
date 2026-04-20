#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
num 375〜449 の udemy 問題の explanation に perspective と tips を追加するスクリプト
Claude API を使って各問題の perspective と tips を生成する
"""

import json
import re
import sys
import time
import anthropic

DATA_PATH = "/Users/aki/aws-sap/docs/data/questions.json"
TARGET_START = 375
TARGET_END = 449

def strip_html(html: str) -> str:
    """HTMLタグを除去してプレーンテキストを返す"""
    return re.sub(r'<[^>]+>', '', html).strip()

def generate_perspective_and_tips(client: anthropic.Anthropic, question: dict) -> dict:
    """Claude API を使って perspective と tips を生成する"""
    q_text = question["question"]
    choices = "\n".join(question["choices"])
    answer = question["answer"]
    detail_plain = strip_html(question["explanation"]["detail"])

    prompt = f"""以下はAWS SAP-C02試験の問題です。この問題の解説に追加する「perspective」と「tips」を生成してください。

## 問題
{q_text}

## 選択肢
{choices}

## 正解
{answer}

## 解説（参考）
{detail_plain[:800]}

---

以下の形式でJSONのみを返してください（他の文言は一切不要）：

{{
  "perspective": "この問題で試されている判断力を問いかけ形式で1行（例：「〜するには何を選ぶべきか？」「〜と〜の使い分けをどう判断するか？」）",
  "tips": [
    "〇〇と来たら→△△（試験で即使える判断パターン）",
    "〇〇と来たら→△△（試験で即使える判断パターン）",
    "〇〇と来たら→△△（試験で即使える判断パターン）"
  ]
}}

条件：
- perspective は日本語で1行、問いかけ形式
- tips は2〜3個、「〇〇と来たら→△△」形式、試験で即使えるショートカット知識
- JSONのみ返す（```json などのマークダウン記法も不要）"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    # マークダウンのコードブロックがあれば除去
    raw = re.sub(r'^```(?:json)?\n?', '', raw)
    raw = re.sub(r'\n?```$', '', raw)
    raw = raw.strip()

    return json.loads(raw)


def main():
    # 対象問題を取得
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    targets = [q for q in data if q.get("source") == "udemy" and TARGET_START <= q.get("num", 0) <= TARGET_END]
    print(f"対象問題数: {len(targets)}")

    # 既に perspective が入っている問題をスキップ可能
    pending = [q for q in targets if not q["explanation"].get("perspective")]
    done = [q for q in targets if q["explanation"].get("perspective")]
    print(f"  うち処理済み: {len(done)}問, 未処理: {len(pending)}問")

    if not pending:
        print("全問処理済みです。")
        return

    client = anthropic.Anthropic()

    results = {}  # num -> {perspective, tips}

    for i, q in enumerate(pending):
        num = q["num"]
        print(f"[{i+1}/{len(pending)}] num={num} 処理中...", end=" ", flush=True)
        try:
            generated = generate_perspective_and_tips(client, q)
            results[num] = generated
            print(f"OK - perspective={generated['perspective'][:40]}...")
        except json.JSONDecodeError as e:
            print(f"JSON解析エラー: {e}")
            results[num] = None
        except Exception as e:
            print(f"エラー: {e}")
            results[num] = None

        # API制限回避のため少し待機
        if i < len(pending) - 1:
            time.sleep(0.3)

    # ファイルを再読み込みして対象問題のみ差し替え
    print("\nファイルを再読み込みして保存中...")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data_fresh = json.load(f)

    success_count = 0
    error_count = 0
    skip_count = 0

    for q in data_fresh:
        if q.get("source") == "udemy" and TARGET_START <= q.get("num", 0) <= TARGET_END:
            num = q["num"]
            if num in results:
                if results[num] is not None:
                    q["explanation"]["perspective"] = results[num]["perspective"]
                    q["explanation"]["tips"] = results[num]["tips"]
                    success_count += 1
                else:
                    error_count += 1
            # results に num がない = 処理済みでスキップした問題
            else:
                skip_count += 1

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data_fresh, f, ensure_ascii=False, indent=2)

    print(f"\n完了: 成功={success_count}, スキップ(既処理)={skip_count}, エラー={error_count}")
    if error_count > 0:
        print("エラーのあった問題は手動で確認してください。")


if __name__ == "__main__":
    main()
