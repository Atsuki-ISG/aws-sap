#!/usr/bin/env python3
"""
Replace the inline SVG following <!-- svg_added --> in selected questions with a drawio SVG img tag.
Only touches the 25 selected IDs.
"""
import json
import re
from pathlib import Path

DATA = Path('/Users/aki/aws-sap/docs/data/questions.json')
PER_DIR = Path('/Users/aki/aws-sap/docs/diagrams/per-question')

SELECTED = [
    'UDEMY-050','UDEMY-328','UDEMY-045',
    'UDEMY-065','UDEMY-015','UDEMY-097','UDEMY-011','UDEMY-013','UDEMY-018','UDEMY-026',
    'UDEMY-373','UDEMY-287','UDEMY-336',
    'UDEMY-315','UDEMY-164','UDEMY-322','UDEMY-346','UDEMY-268','UDEMY-283',
    'UDEMY-249','UDEMY-062','UDEMY-150','UDEMY-192','UDEMY-059','UDEMY-366',
]

def build_img_block(qid: str) -> str:
    return (
        f'<div style="margin-top:16px;"><!-- drawio_svg --><strong>📊 構成図（AWS公式アイコン）</strong><br>\n'
        f'<img src="./diagrams/per-question/{qid}.svg" alt="構成図" '
        f'style="max-width:100%;height:auto;background:#fff;border:1px solid #ccc;border-radius:6px;margin-top:6px;"/>\n'
        f'</div>'
    )


def process():
    data = json.loads(DATA.read_text())
    changed = 0
    by_id = {q['id']: q for q in data}
    for qid in SELECTED:
        q = by_id.get(qid)
        if not q:
            print(f'MISSING question {qid}')
            continue
        # svg file must exist
        if not (PER_DIR / f'{qid}.svg').exists():
            print(f'SVG MISSING {qid}, skip')
            continue
        exp = q.get('explanation')
        if not isinstance(exp, dict) or 'detail' not in exp:
            print(f'No detail for {qid}')
            continue
        detail = exp['detail']
        marker = '<!-- svg_added -->'
        if marker not in detail:
            print(f'NO marker {qid}, skip')
            continue
        # Locate: the div that wraps svg_added starts at the preceding <div style="margin-top:16px;">
        # We want to keep everything up to (and including) that wrapping div's opening and then replace
        # the inner contents with our new block's inner contents. Actually simpler: find the <div ...><!-- svg_added --> block
        # and replace from there through the end (since the SVG block is at the tail).
        # First find the div that contains svg_added
        pattern = r'<div [^>]*?><!-- svg_added -->[\s\S]*$'
        new_detail, n = re.subn(pattern, build_img_block(qid), detail)
        if n == 0:
            # fallback: replace from marker to end
            idx = detail.find(marker)
            # Search backwards for nearest preceding <div
            pre = detail[:idx]
            div_open = pre.rfind('<div')
            if div_open == -1:
                print(f'Cannot locate wrap div for {qid}')
                continue
            new_detail = detail[:div_open] + build_img_block(qid)
        exp['detail'] = new_detail
        changed += 1
        print(f'REPLACED {qid}')

    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f'\nTotal replaced: {changed}')


if __name__ == '__main__':
    process()
