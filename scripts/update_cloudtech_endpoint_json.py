"""Update docs/data/questions.json: for each selected SAP-* question,
replace content after <!-- svg_added --> with drawio_svg img block
(or append if marker missing).
"""
import json
import re
from pathlib import Path

QUESTIONS_PATH = Path("docs/data/questions.json")

TARGET_IDS = [
    "SAP-54", "SAP-78", "SAP-108", "SAP-112", "SAP-116", "SAP-121",
    "SAP-139", "SAP-162", "SAP-180", "SAP-187", "SAP-200", "SAP-207",
    "SAP-221", "SAP-222", "SAP-223", "SAP-239", "SAP-240", "SAP-288",
]


def build_block(qid: str) -> str:
    return (
        '<div style="margin-top:16px;"><!-- drawio_svg --><strong>'
        '\U0001F4CA \u69cb\u6210\u56f3\uff08AWS\u516c\u5f0f\u30a2\u30a4\u30b3\u30f3\uff09'
        '</strong><br>\n'
        f'<img src="./diagrams/per-question/{qid}.svg" alt="\u69cb\u6210\u56f3" '
        'style="max-width:100%;height:auto;background:#fff;border:1px solid #ccc;'
        'border-radius:6px;margin-top:6px;"/>\n'
        '</div>'
    )


def main():
    data = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    replaced = 0
    for q in data:
        if q.get("id") not in TARGET_IDS:
            continue
        detail = q["explanation"].get("detail", "")
        block = build_block(q["id"])

        if "<!-- svg_added -->" in detail:
            # Find the opening <div ...><!-- svg_added --> and replace
            # everything from that <div ...> onward with the new block.
            pattern = re.compile(r'<div[^>]*><!--\s*svg_added\s*-->.*$', re.DOTALL)
            new_detail, n = pattern.subn(block, detail)
            if n == 0:
                # Fallback: marker found but not inside a <div>. Replace
                # from the marker to end.
                idx = detail.index("<!-- svg_added -->")
                new_detail = detail[:idx] + block
            q["explanation"]["detail"] = new_detail
            replaced += 1
        else:
            # Marker not present: append block at end
            q["explanation"]["detail"] = detail + block
            replaced += 1

    QUESTIONS_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Updated: {replaced} questions")


if __name__ == "__main__":
    main()
