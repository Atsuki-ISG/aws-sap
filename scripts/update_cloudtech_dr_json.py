#!/usr/bin/env python3
"""
Replace the <!-- svg_added --> block in cloudtech DR question details
with a <!-- drawio_svg --> block that references the per-question drawio SVG.

Regex target: <div style="margin-top:16px;"><!-- svg_added -->.*?</div>\s*$
(pattern verified to match 245 cloudtech questions).
"""
import json
import re
import sys

QUESTIONS_PATH = '/Users/aki/aws-sap/docs/data/questions.json'

TARGETS = [
    'SAP-3', 'SAP-39', 'SAP-71', 'SAP-106', 'SAP-125',
    'SAP-130', 'SAP-155', 'SAP-160', 'SAP-168', 'SAP-174',
    'SAP-219', 'SAP-225', 'SAP-233', 'SAP-251', 'SAP-253',
    'SAP-263', 'SAP-275', 'SAP-278', 'SAP-285', 'SAP-290',
    'SAP-296',
]

PATTERN = re.compile(
    r'<div style="margin-top:16px;"><!-- svg_added -->.*?</div>\s*$',
    re.DOTALL,
)


def new_block(qid: str) -> str:
    return (
        '<div style="margin-top:16px;"><!-- drawio_svg -->'
        '<strong>📊 構成図（AWS公式アイコン）</strong><br>\n'
        f'<img src="./diagrams/per-question/{qid}.svg" alt="構成図" '
        'style="max-width:100%;height:auto;background:#fff;border:1px solid #ccc;'
        'border-radius:6px;margin-top:6px;"/>\n'
        '</div>'
    )


def main() -> int:
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    by_id = {q['id']: q for q in data}
    replaced = 0
    skipped = []
    missing = []

    for tid in TARGETS:
        q = by_id.get(tid)
        if not q:
            missing.append(tid)
            continue
        detail = q.get('explanation', {}).get('detail', '') or ''
        if '<!-- drawio_svg -->' in detail:
            skipped.append(f'{tid} (already has drawio_svg)')
            continue
        if '<!-- svg_added -->' not in detail:
            skipped.append(f'{tid} (no svg_added marker)')
            continue
        new_detail, n = PATTERN.subn(new_block(tid), detail)
        if n != 1:
            skipped.append(f'{tid} (pattern match count={n})')
            continue
        q['explanation']['detail'] = new_detail
        replaced += 1

    # Write back atomically by using a temp file and rename
    tmp = QUESTIONS_PATH + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    import os
    os.replace(tmp, QUESTIONS_PATH)

    print(f'Replaced: {replaced}')
    if missing:
        print('MISSING:', missing)
    if skipped:
        print('SKIPPED:', skipped)
    return 0 if replaced == len(TARGETS) else 1


if __name__ == '__main__':
    sys.exit(main())
