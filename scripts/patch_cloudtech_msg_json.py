#!/usr/bin/env python3
"""
Replace <!-- svg_added --> (and everything after, if any) in explanation.detail
for CloudTech msg/stream/pipeline questions with a drawio SVG <img> block.
"""
import json
from pathlib import Path

JSON_PATH = Path('/Users/aki/aws-sap/docs/data/questions.json')

TARGETS = [7, 14, 69, 108, 135, 141, 144, 154, 161, 176, 204, 245, 248, 268, 269, 282]

MARKER = '<!-- svg_added -->'

def build_block(qid):
    return (
        f'<div style="margin-top:16px;"><!-- drawio_svg --><strong>📊 構成図（AWS公式アイコン）</strong><br>\n'
        f'<img src="./diagrams/per-question/{qid}.svg" alt="構成図" '
        f'style="max-width:100%;height:auto;background:#fff;border:1px solid #ccc;border-radius:6px;margin-top:6px;"/>\n'
        f'</div>'
    )

def main():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    patched = []
    missing = []
    for q in data:
        if q.get('source') != 'cloudtech':
            continue
        if q.get('num') not in TARGETS:
            continue
        qid = q['id']  # e.g. "SAP-7"
        expl = q.get('explanation', '')
        if isinstance(expl, dict):
            detail = expl.get('detail', '')
            if MARKER not in detail:
                missing.append(qid)
                continue
            # The existing SVG block is wrapped in <div style="margin-top:16px;">
            # that opens immediately before the marker. The new block brings its
            # own wrapper div, so drop the preceding div opener if present to
            # avoid leaving a dangling wrapper.
            idx = detail.index(MARKER)
            prefix = detail[:idx]
            open_tag = '<div style="margin-top:16px;">'
            if prefix.endswith(open_tag):
                prefix = prefix[:-len(open_tag)]
            new_detail = prefix + build_block(qid)
            expl['detail'] = new_detail
            q['explanation'] = expl
            patched.append(qid)
        else:
            missing.append(qid)

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'patched: {len(patched)} -> {patched}')
    print(f'missing marker: {len(missing)} -> {missing}')


if __name__ == '__main__':
    main()
