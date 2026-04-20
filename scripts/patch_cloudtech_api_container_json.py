#!/usr/bin/env python3
"""
Replace `<!-- svg_added -->...` section in CloudTech (SAP-*) questions' explanation.detail
with a new <img> referencing the per-question drawio-generated SVG.
"""
import json
import re
from pathlib import Path

JSON_PATH = Path('/Users/aki/aws-sap/docs/data/questions.json')
SVG_DIR = Path('/Users/aki/aws-sap/docs/diagrams/per-question')

# Target question IDs (SAP-<num>)
TARGETS = [
    'SAP-281', 'SAP-298', 'SAP-99', 'SAP-29', 'SAP-210',
    'SAP-77', 'SAP-193', 'SAP-25', 'SAP-92', 'SAP-107',
    'SAP-82', 'SAP-294', 'SAP-173', 'SAP-272', 'SAP-259',
    'SAP-56', 'SAP-175', 'SAP-91', 'SAP-250', 'SAP-271',
]

def new_block(qid):
    return (
        f'<div style="margin-top:16px;"><!-- drawio_svg --><strong>📊 構成図（AWS公式アイコン）</strong><br>'
        f'<img src="./diagrams/per-question/{qid}.svg" alt="構成図" style="max-width:100%;height:auto;background:#fff;border:1px solid #ccc;border-radius:6px;margin-top:6px;"/>'
        f'</div>'
    )


def main():
    data = json.loads(JSON_PATH.read_text(encoding='utf-8'))
    replaced = 0
    skipped = 0
    for q in data:
        if q.get('source') != 'cloudtech':
            continue
        qid = q.get('id')
        if qid not in TARGETS:
            continue
        svg_file = SVG_DIR / f'{qid}.svg'
        if not svg_file.exists():
            print(f'SKIP (no svg): {qid}')
            skipped += 1
            continue
        expl = q.get('explanation')
        if not isinstance(expl, dict):
            print(f'SKIP (explanation not dict): {qid}')
            skipped += 1
            continue
        detail = expl.get('detail', '')
        marker = '<!-- svg_added -->'
        idx = detail.find(marker)
        if idx < 0:
            print(f'SKIP (no svg_added marker): {qid}')
            skipped += 1
            continue
        # Replace everything from marker to end of string with new block
        before = detail[:idx]
        new_detail = before + new_block(qid)
        expl['detail'] = new_detail
        replaced += 1
        print(f'Replaced: {qid}')
    # Write back
    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\nTotal replaced: {replaced}, skipped: {skipped}')


if __name__ == '__main__':
    main()
