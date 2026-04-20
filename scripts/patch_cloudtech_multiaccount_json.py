#!/usr/bin/env python3
"""Replace <!-- svg_added --> block in explanation.detail with drawio SVG img for
the 25 CloudTech multi-account SAP-xxx questions."""
import json
import re

JSON_PATH = '/Users/aki/aws-sap/docs/data/questions.json'

TARGETS = [
    'SAP-33','SAP-36','SAP-49','SAP-60','SAP-63',
    'SAP-72','SAP-75','SAP-81','SAP-94','SAP-97',
    'SAP-101','SAP-103','SAP-111','SAP-126','SAP-140',
    'SAP-149','SAP-153','SAP-157','SAP-172','SAP-185',
    'SAP-201','SAP-213','SAP-252','SAP-284','SAP-289',
]

def new_block(qid: str) -> str:
    return (
        '<div style="margin-top:16px;"><!-- drawio_svg --><strong>'
        '📊 構成図（AWS公式アイコン）</strong><br>\n'
        f'<img src="./diagrams/per-question/{qid}.svg" alt="構成図" '
        'style="max-width:100%;height:auto;background:#fff;border:1px solid #ccc;'
        'border-radius:6px;margin-top:6px;"/>\n'
        '</div>'
    )

# Pattern: matches from <div style="margin-top:16px;"><!-- svg_added --> through the
# closing </div> that follows the inline SVG. It must be non-greedy and end at the
# first </svg></div> occurrence.
PATTERN = re.compile(
    r'<div style="margin-top:16px;"><!--\s*svg_added\s*-->.*?</svg></div>',
    re.DOTALL,
)

def main():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    by_id = {q['id']: q for q in data}
    replaced = 0
    missing = []
    already = []
    for qid in TARGETS:
        q = by_id.get(qid)
        if not q:
            missing.append(qid); continue
        detail = (q.get('explanation') or {}).get('detail', '') or ''
        if f'/{qid}.svg' in detail and '<!-- drawio_svg -->' in detail:
            already.append(qid); continue
        new_detail, n = PATTERN.subn(new_block(qid), detail, count=1)
        if n == 0:
            missing.append(qid + ' (pattern not found)')
            continue
        q['explanation']['detail'] = new_detail
        replaced += 1
        print(f'OK {qid}: replaced')

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'\nReplaced: {replaced}')
    if already:
        print('Already updated (skipped):', already)
    if missing:
        print('Missing:', missing)

if __name__ == '__main__':
    main()
