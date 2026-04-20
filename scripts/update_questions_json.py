"""Update docs/data/questions.json: replace content from <!-- svg_added --> onward
with the drawio-generated image block for the selected IDs.
"""
import json
import os
import re
import sys

JSON_PATH = "/Users/aki/aws-sap/docs/data/questions.json"

TARGET_IDS = [
    "UDEMY-017", "UDEMY-021", "UDEMY-023", "UDEMY-029", "UDEMY-043",
    "UDEMY-052", "UDEMY-057", "UDEMY-066", "UDEMY-078", "UDEMY-087",
    "UDEMY-096", "UDEMY-106", "UDEMY-114", "UDEMY-135", "UDEMY-140",
    "UDEMY-151", "UDEMY-161", "UDEMY-162", "UDEMY-170", "UDEMY-190",
    "UDEMY-198", "UDEMY-203", "UDEMY-206", "UDEMY-247", "UDEMY-248",
    "UDEMY-276", "UDEMY-295", "UDEMY-343", "UDEMY-348",
]


def build_block(qid: str) -> str:
    return (
        '<div style="margin-top:16px;"><!-- drawio_svg --><strong>📊 構成図（AWS公式アイコン）</strong><br>\n'
        f'<img src="./diagrams/per-question/{qid}.svg" alt="構成図" '
        'style="max-width:100%;height:auto;background:#fff;border:1px solid #ccc;border-radius:6px;margin-top:6px;"/>\n'
        '</div>'
    )


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    targets_set = set(TARGET_IDS)
    replaced = []
    missing = []
    no_marker = []

    for q in data:
        qid = q.get("id")
        if qid not in targets_set:
            continue
        # Verify svg file exists
        svg_path = f"/Users/aki/aws-sap/docs/diagrams/per-question/{qid}.svg"
        if not os.path.exists(svg_path):
            missing.append(qid)
            continue
        expl = q.get("explanation") or {}
        detail = expl.get("detail", "") or ""
        marker = "<!-- svg_added -->"
        idx = detail.find(marker)
        if idx < 0:
            no_marker.append(qid)
            continue
        # The marker sits inside a wrapping div like:
        #   <div style="margin-top:16px;"><!-- svg_added -->....
        # We want to drop the wrapper and everything after it, then append
        # the fresh drawio_svg block.
        before = detail[:idx]
        # Find the nearest preceding opening tag that contains margin-top:16px
        # (search from end of `before`).
        wrapper_re = re.compile(r'<div[^<>]*margin-top:16px[^<>]*>')
        last_match = None
        for mm in wrapper_re.finditer(before):
            last_match = mm
        if last_match is not None:
            new_before = before[:last_match.start()]
        else:
            new_before = before

        new_detail = new_before.rstrip() + "\n" + build_block(qid)
        expl["detail"] = new_detail
        q["explanation"] = expl
        replaced.append(qid)

    # Write back with stable formatting (2-space indent, keep unicode)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Replaced: {len(replaced)}")
    for x in replaced: print(f"  {x}")
    if missing:
        print(f"Missing SVG: {missing}")
    if no_marker:
        print(f"No marker: {no_marker}")


if __name__ == "__main__":
    main()
