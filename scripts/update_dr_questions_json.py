#!/usr/bin/env python3
"""
Replace the existing <!-- svg_added -->...</svg></div> tail in
selected questions' explanation.detail with a new <!-- drawio_svg --> block
that references ./diagrams/per-question/<ID>.svg
"""
import json
import re
import os
import shutil

QUESTIONS_PATH = '/Users/aki/aws-sap/docs/data/questions.json'

SELECTED = [
    'UDEMY-351','UDEMY-046','UDEMY-309','UDEMY-318','UDEMY-070','UDEMY-091',
    'UDEMY-107','UDEMY-008','UDEMY-158','UDEMY-014','UDEMY-086','UDEMY-109',
    'UDEMY-284','UDEMY-333','UDEMY-072','UDEMY-092','UDEMY-219','UDEMY-297',
    'UDEMY-320','UDEMY-335','UDEMY-343','UDEMY-011','UDEMY-146','UDEMY-222',
    'UDEMY-353','UDEMY-115','UDEMY-282','UDEMY-304',
]


def new_block(qid):
    return (
        '<div style="margin-top:16px;"><!-- drawio_svg --><strong>📊 構成図（AWS公式アイコン）</strong><br>\n'
        f'<img src="./diagrams/per-question/{qid}.svg" alt="構成図" '
        'style="max-width:100%;height:auto;background:#fff;border:1px solid #ccc;border-radius:6px;margin-top:6px;"/>\n'
        '</div>'
    )


def patch_detail(detail: str, qid: str) -> str:
    marker = '<!-- svg_added -->'
    idx = detail.find(marker)
    if idx < 0:
        raise ValueError(f'{qid}: marker not found')
    # The marker pattern in current file is:
    #   <div style="margin-top:16px;"><!-- svg_added --><strong>構成図: ...</strong><br><svg ...></svg></div>
    # We want to find the <div style="margin-top:16px;"> that opens it (just before marker)
    # and replace from there to the trailing </div>.
    # Strategy: find the preceding '<div' whose content contains the marker and ends with the trailing '</svg></div>'.
    # Simpler: detail was confirmed to end with '</svg></div>'. The block starts at the <div> that contains the marker.
    before = detail[:idx]
    # find the opening <div ...> just before marker
    div_open_idx = before.rfind('<div')
    if div_open_idx < 0:
        raise ValueError(f'{qid}: opening <div> before marker not found')
    # Sanity: the <div ...> must close with '>' before marker
    gt = before.find('>', div_open_idx)
    if gt < 0 or gt >= idx:
        raise ValueError(f'{qid}: opening <div> tag malformed')
    # tail must end with </div>
    if not detail.endswith('</div>'):
        raise ValueError(f'{qid}: detail does not end with </div>')
    new_detail = detail[:div_open_idx] + new_block(qid)
    return new_detail


def main():
    # Backup
    backup_path = QUESTIONS_PATH + '.bak_dr_diagrams'
    if not os.path.exists(backup_path):
        shutil.copy2(QUESTIONS_PATH, backup_path)
        print(f'Backup: {backup_path}')

    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    d = {q.get('id'): q for q in data}
    changed = 0
    for sid in SELECTED:
        q = d.get(sid)
        if not q:
            print(f'MISSING: {sid}')
            continue
        detail = q['explanation']['detail']
        if '<!-- drawio_svg -->' in detail:
            print(f'{sid}: already has drawio_svg, skipping')
            continue
        new_detail = patch_detail(detail, sid)
        q['explanation']['detail'] = new_detail
        changed += 1
        print(f'{sid}: replaced ({len(detail)} → {len(new_detail)} chars)')

    # Write back with same formatting (2-space indent, ensure_ascii=False)
    with open(QUESTIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f'\nReplaced {changed}/{len(SELECTED)} questions.')


if __name__ == '__main__':
    main()
