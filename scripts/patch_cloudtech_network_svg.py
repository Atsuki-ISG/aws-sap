#!/usr/bin/env python3
"""
Replace `<!-- svg_added -->` ... in explanation.detail with drawio SVG img
for the selected CloudTech network questions.
"""
import json, re, sys

JSON_PATH = "/Users/aki/aws-sap/docs/data/questions.json"

IDS = [
    "SAP-2","SAP-15","SAP-21","SAP-35","SAP-48","SAP-61","SAP-66","SAP-70",
    "SAP-73","SAP-78","SAP-106","SAP-108","SAP-112","SAP-121","SAP-139",
    "SAP-162","SAP-165","SAP-167","SAP-180","SAP-202","SAP-222","SAP-227",
    "SAP-239","SAP-258","SAP-280","SAP-290",
]

def replacement_html(qid):
    return (
        f'<!-- drawio_svg --><strong>📊 構成図（AWS公式アイコン）</strong><br>\n'
        f'<img src="./diagrams/per-question/{qid}.svg" alt="構成図" '
        f'style="max-width:100%;height:auto;background:#fff;border:1px solid #ccc;'
        f'border-radius:6px;margin-top:6px;"/>\n'
        f'</div>'
    )

def wrap_block(qid):
    # full wrapper block: <div style="margin-top:16px;">...</div>
    return (
        f'<div style="margin-top:16px;">{replacement_html(qid)}'
    )

def main():
    with open(JSON_PATH) as f:
        data = json.load(f)
    by_id = {q["id"]: q for q in data}
    count = 0
    missing = []
    for qid in IDS:
        q = by_id.get(qid)
        if not q:
            missing.append(qid)
            continue
        exp = q.get("explanation", {})
        if not isinstance(exp, dict):
            missing.append(qid + "(no dict)")
            continue
        detail = exp.get("detail", "")
        if "<!-- drawio_svg -->" in detail:
            # Already replaced; skip or keep idempotent
            # Replace existing drawio_svg block with fresh one too
            pattern = re.compile(r'<div style="margin-top:16px;"><!-- drawio_svg -->.*?</div>', re.DOTALL)
            new_detail = pattern.sub(wrap_block(qid), detail)
            if new_detail != detail:
                exp["detail"] = new_detail
                count += 1
            continue
        # Look for svg_added marker
        idx = detail.find("<!-- svg_added -->")
        if idx < 0:
            missing.append(qid + "(no marker)")
            continue
        # Replace everything from <!-- svg_added --> to end of the surrounding block.
        # The svg_added marker is inside a <div style="margin-top:16px;">...</div> wrapper.
        # We replace from the wrapper <div start to its closing </div>.
        # Find the wrapping <div style="margin-top:16px;">. Search backwards from idx.
        div_start_pat = re.compile(r'<div[^>]*margin-top:16px[^>]*>', re.IGNORECASE)
        m = None
        for mm in div_start_pat.finditer(detail, 0, idx + 1):
            m = mm
        if not m:
            # Fallback: just replace svg_added..end of a nearby </div>
            tail_end = detail.find("</div>", idx)
            if tail_end < 0:
                missing.append(qid + "(no </div>)")
                continue
            new_detail = detail[:idx] + replacement_html(qid) + detail[tail_end+6:]
        else:
            # find matching </div> from m.end()
            tail_end = detail.find("</div>", m.end())
            if tail_end < 0:
                missing.append(qid + "(no div close)")
                continue
            new_detail = detail[:m.start()] + wrap_block(qid) + detail[tail_end+6:]
        exp["detail"] = new_detail
        count += 1
    with open(JSON_PATH, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"replaced: {count}")
    if missing:
        print("missing/errors:", missing)

if __name__ == "__main__":
    main()
