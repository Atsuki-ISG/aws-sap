#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Udemy問題 num 600〜674 の explanation に perspective と tips を追加するスクリプト
- detail はそのまま維持
- perspective と tips のみ Claude API で生成して追加
"""

import json
import time
import anthropic

DATA_PATH = "/Users/aki/aws-sap/docs/data/questions.json"
MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = """あなたはAWS SAP-C02試験の専門家です。
与えられた問題・選択肢・正解・解説を読み、以下を日本語で生成してください。

1. perspective（1文）: 「この問題で試されている判断力は何か」を問いかけ形式で。
   例: 「コスト最適化とパフォーマンスのトレードオフをどう判断するか？」
   ※ 問題の核心的な判断ポイントを端的に問いかける形式にする。

2. tips（配列、2〜3個）: 「〇〇と来たら→△△」形式の判断パターン。
   試験で即使えるショートカット知識。
   例: ["「マルチリージョン + 低レイテンシ」→ Global Accelerator または CloudFront",
        "「既存アーキテクチャを変更したくない」→ Auto Scaling + Spot の混合が定番"]

必ずJSON形式で返してください（マークダウンなし、コードブロックなし）:
{"perspective": "...", "tips": ["...", "...", "..."]}"""


def generate_perspective_tips(client, question_data):
    """Claude API を使って perspective と tips を生成"""

    # 問題テキストの組み立て
    q_text = question_data["question"][:500]  # 長すぎる場合は切り詰め
    choices_text = "\n".join(question_data["choices"])
    answer_text = str(question_data["answer"])[:300]

    # detail から HTML タグを除去して短縮
    detail = question_data["explanation"]["detail"]
    import re
    detail_plain = re.sub(r'<[^>]+>', '', detail)[:600]

    user_content = f"""問題:
{q_text}

選択肢:
{choices_text}

正解:
{answer_text}

解説（要約）:
{detail_plain}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}]
    )

    result_text = response.content[0].text.strip()

    # JSONパース
    parsed = json.loads(result_text)
    return parsed["perspective"], parsed["tips"]


def main():
    client = anthropic.Anthropic()

    # questions.json を読み込む
    print("Loading questions.json...")
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    # 対象問題を抽出（num 600〜674 かつ source=udemy）
    target_indices = [
        i for i, q in enumerate(data)
        if q.get("source") == "udemy" and 600 <= q.get("num", 0) <= 674
    ]

    print(f"Target questions: {len(target_indices)} (num 600-674, source=udemy)")

    # すでに perspective が入っているものをスキップするかチェック
    already_done = sum(
        1 for i in target_indices
        if data[i]["explanation"].get("perspective", "")
    )
    print(f"Already has perspective: {already_done}")

    errors = []
    success_count = 0

    for idx_count, i in enumerate(target_indices):
        q = data[i]
        num = q["num"]

        # すでに perspective が入っていればスキップ
        if q["explanation"].get("perspective", ""):
            print(f"  [SKIP] num={num} (already has perspective)")
            continue

        print(f"Processing num={num} ({idx_count+1}/{len(target_indices)})...", end=" ", flush=True)

        try:
            perspective, tips = generate_perspective_tips(client, q)

            # データを更新（detailはそのまま）
            data[i]["explanation"]["perspective"] = perspective
            data[i]["explanation"]["tips"] = tips

            print(f"OK | {perspective[:60]}...")
            success_count += 1

            # API レート制限対策：少し待つ
            if (idx_count + 1) % 10 == 0:
                print(f"  --- {idx_count+1} done, brief pause... ---")
                time.sleep(2)
            else:
                time.sleep(0.5)

        except Exception as e:
            print(f"ERROR: {e}")
            errors.append((num, str(e)))
            time.sleep(2)

    # 書き込み直前にファイルを再読み込みして対象問題のみ差し替え
    print(f"\nRe-reading file before write...")
    with open(DATA_PATH, encoding="utf-8") as f:
        latest_data = json.load(f)

    # 対象問題の explanation を差し替え
    replaced = 0
    for q_new in data:
        if q_new.get("source") == "udemy" and 600 <= q_new.get("num", 0) <= 674:
            for j, q_orig in enumerate(latest_data):
                if q_orig.get("num") == q_new["num"] and q_orig.get("source") == "udemy":
                    latest_data[j]["explanation"]["perspective"] = q_new["explanation"]["perspective"]
                    latest_data[j]["explanation"]["tips"] = q_new["explanation"]["tips"]
                    replaced += 1
                    break

    print(f"Writing {DATA_PATH} ({replaced} questions updated)...")
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(latest_data, f, ensure_ascii=False, indent=2)

    print(f"\nDone! success={success_count}, errors={len(errors)}")
    if errors:
        print("Errors:")
        for num, err in errors:
            print(f"  num={num}: {err}")


if __name__ == "__main__":
    main()
