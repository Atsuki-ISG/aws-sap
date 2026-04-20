#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Udemy問題 num=525〜599 の explanation に perspective と tips を追加するスクリプト。
Claude API (claude-sonnet-4-6) を使用して自動生成する。
"""

import json
import time
import re
import anthropic

QUESTIONS_PATH = "/Users/aki/aws-sap/docs/data/questions.json"
TARGET_SOURCE = "udemy"
TARGET_NUM_MIN = 525
TARGET_NUM_MAX = 599

SYSTEM_PROMPT = """あなたはAWS認定ソリューションアーキテクト プロフェッショナル（SAP-C02）の試験対策専門家です。
問題を分析し、受験者の「比較判断力」を強化するための解説要素を日本語で作成してください。"""

USER_PROMPT_TEMPLATE = """以下のAWS SAPの問題を分析し、perspective と tips を作成してください。

## 問題
{question}

## 選択肢
{choices}

## 正解
{answer}

## 既存の解説（detail）
{detail}

---

以下のJSON形式のみで回答してください（他の文章は不要）:

{{
  "perspective": "この問題で試されている判断力を問いかけ形式で1行（例：「AとBをどの基準で選び分けるか？」）",
  "tips": [
    "〇〇と来たら→△△（試験で即使えるショートカット知識）",
    "〇〇と来たら→△△",
    "〇〇と来たら→△△"
  ]
}}

### perspective の条件
- 1行・問いかけ形式
- この問題で何を判断する力が試されているかを端的に
- 「〜はどう選ぶか？」「〜と〜の違いをどう判断するか？」などの形式

### tips の条件
- 2〜3個
- 「〇〇と来たら→△△」の形式
- 試験本番で即使える判断パターン
- この問題の正解選択に直結するポイント"""


def extract_json(text: str) -> dict:
    """レスポンステキストからJSONを抽出する。"""
    # コードブロックを除去
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    text = text.strip()

    # JSON部分を抽出
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        json_str = text[start:end+1]
        return json.loads(json_str)
    raise ValueError(f"JSONが見つかりません: {text[:200]}")


def generate_perspective_and_tips(client: anthropic.Anthropic, question_data: dict) -> dict:
    """Claude APIを呼び出してperspectiveとtipsを生成する。"""
    choices_text = "\n".join(question_data["choices"])

    # HTMLタグを除去してdetailをテキスト化
    detail_html = question_data["explanation"].get("detail", "")
    detail_text = re.sub(r'<[^>]+>', '', detail_html)
    detail_text = detail_text.strip()[:1000]  # 長すぎる場合は切り詰め

    user_message = USER_PROMPT_TEMPLATE.format(
        question=question_data["question"],
        choices=choices_text,
        answer=question_data["answer"],
        detail=detail_text
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}]
    )

    response_text = response.content[0].text
    return extract_json(response_text)


def main():
    client = anthropic.Anthropic()

    # JSONファイル読み込み
    print(f"JSONファイルを読み込み中: {QUESTIONS_PATH}")
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 対象問題を特定
    targets = [
        (i, q) for i, q in enumerate(data)
        if q.get('source') == TARGET_SOURCE
        and TARGET_NUM_MIN <= q.get('num', 0) <= TARGET_NUM_MAX
    ]

    print(f"対象問題数: {len(targets)}")

    # すでにperspectiveが埋まっているものはスキップ
    todo = [
        (i, q) for i, q in targets
        if not q["explanation"].get("perspective")
    ]
    already_done = len(targets) - len(todo)
    print(f"未処理: {len(todo)}問 / スキップ済み: {already_done}問")

    if not todo:
        print("全問処理済みです。")
        return

    success_count = 0
    error_count = 0

    for idx, (data_index, q) in enumerate(todo):
        num = q["num"]
        print(f"\n[{idx+1}/{len(todo)}] num={num} を処理中...")

        try:
            result = generate_perspective_and_tips(client, q)

            # バリデーション
            if not result.get("perspective"):
                raise ValueError("perspectiveが空です")
            if not result.get("tips") or len(result["tips"]) < 2:
                raise ValueError(f"tipsが不足しています: {result.get('tips')}")

            print(f"  perspective: {result['perspective'][:60]}...")
            print(f"  tips[0]: {result['tips'][0][:60]}...")

            # データを更新（ファイルの再読み込みは最後にまとめて行う）
            data[data_index]["explanation"]["perspective"] = result["perspective"]
            data[data_index]["explanation"]["tips"] = result["tips"]

            success_count += 1

            # 5問ごとにファイルに書き込む（途中経過を保存）
            if success_count % 5 == 0:
                print(f"\n  --- 途中保存中 ({success_count}問完了) ---")
                with open(QUESTIONS_PATH, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"  保存完了")

            # API レート制限対策（0.5秒待機）
            time.sleep(0.5)

        except Exception as e:
            print(f"  エラー (num={num}): {e}")
            error_count += 1
            # エラーが続く場合は少し待機
            time.sleep(2)
            continue

    # 最終保存（ファイルを再読み込みして対象問題のみ差し替え）
    print(f"\n最終保存中...")
    # 最新の状態を再読み込み
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        final_data = json.load(f)

    # メモリ上の更新結果をマージ
    num_to_update = {
        data[i]["num"]: data[i]["explanation"]
        for i, _ in targets
        if data[i]["explanation"].get("perspective")
    }

    for i, q in enumerate(final_data):
        if q.get("num") in num_to_update:
            final_data[i]["explanation"]["perspective"] = num_to_update[q["num"]]["perspective"]
            final_data[i]["explanation"]["tips"] = num_to_update[q["num"]]["tips"]

    with open(QUESTIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print(f"\n完了!")
    print(f"  成功: {success_count}問")
    print(f"  失敗: {error_count}問")
    print(f"  ファイル保存: {QUESTIONS_PATH}")


if __name__ == "__main__":
    main()
