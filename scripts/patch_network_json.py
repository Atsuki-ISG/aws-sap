#!/usr/bin/env python3
"""
Patch docs/data/questions.json for 25 selected network/hybrid questions.

Rule:
- If detail contains `<div ...><!-- svg_added -->...</div>`: replace that whole div
  with the new drawio_svg div pointing to ./diagrams/per-question/<ID>.svg.
- If detail has no svg_added marker: append the new drawio_svg div at the end.
- All other fields (answer/question/choices/id/num/tags/source/perspective/tips)
  are untouched.
"""
import json
import re
import os

JSON_PATH = "/Users/aki/aws-sap/docs/data/questions.json"

# num -> id
TARGETS = {
    305: "UDEMY-006",
    320: "UDEMY-021",
    337: "UDEMY-038",
    342: "UDEMY-043",
    356: "UDEMY-057",
    386: "UDEMY-087",
    413: "UDEMY-114",
    427: "UDEMY-128",
    442: "UDEMY-143",
    461: "UDEMY-162",
    466: "UDEMY-167",
    479: "UDEMY-180",
    489: "UDEMY-190",
    502: "UDEMY-203",
    505: "UDEMY-206",
    526: "UDEMY-227",
    547: "UDEMY-248",
    564: "UDEMY-265",
    569: "UDEMY-270",
    571: "UDEMY-272",
    609: "UDEMY-310",
    620: "UDEMY-321",
    629: "UDEMY-330",
    646: "UDEMY-347",
    664: "UDEMY-365",
}

def build_div(qid):
    return (
        '<div style="margin-top:16px;"><!-- drawio_svg --><strong>📊 構成図（AWS公式アイコン）</strong><br>\n'
        f'<img src="./diagrams/per-question/{qid}.svg" alt="構成図" style="max-width:100%;height:auto;background:#fff;border:1px solid #ccc;border-radius:6px;margin-top:6px;"/>\n'
        '</div>'
    )

# Regex: match the entire svg_added wrapper div (single level, no nested divs inside).
SVG_DIV_RE = re.compile(
    r'<div[^>]*><!--\s*svg_added\s*-->.*?</div>\s*$',
    re.DOTALL,
)

def patch_detail(detail, qid):
    new_div = build_div(qid)
    if '<!-- svg_added -->' in detail:
        # Replace wrapper div
        new_detail, n = SVG_DIV_RE.subn(new_div, detail, count=1)
        if n == 0:
            # fallback: non-greedy, not at end
            fallback = re.compile(r'<div[^>]*><!--\s*svg_added\s*-->.*?</div>', re.DOTALL)
            new_detail, n = fallback.subn(new_div, detail, count=1)
        return new_detail, n > 0, "replaced"
    else:
        # No marker - append
        return detail.rstrip() + '\n' + new_div, True, "appended"


def main():
    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    replaced = 0
    appended = 0
    failed = []
    for q in data:
        num = q.get("num")
        if num not in TARGETS:
            continue
        qid = TARGETS[num]
        if q.get("id") != qid:
            # safety: id must match expected qid
            failed.append((num, qid, q.get("id")))
            continue
        detail = q["explanation"]["detail"]
        new_detail, ok, mode = patch_detail(detail, qid)
        if not ok:
            failed.append((num, qid, "no-change"))
            continue
        q["explanation"]["detail"] = new_detail
        if mode == "replaced":
            replaced += 1
        else:
            appended += 1

    # Write back
    with open(JSON_PATH, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Replaced: {replaced}")
    print(f"Appended: {appended}")
    print(f"Failed:   {failed}")
    print(f"Total target: {len(TARGETS)}")

if __name__ == "__main__":
    main()
