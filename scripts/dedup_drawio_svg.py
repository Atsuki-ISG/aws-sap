#!/usr/bin/env python3
"""Remove duplicate drawio_svg divs (keep only the last occurrence per question)."""
import json, re

JSON_PATH = "/Users/aki/aws-sap/docs/data/questions.json"

# Match one drawio_svg div block (non-greedy)
DIV_RE = re.compile(r'<div[^>]*><!--\s*drawio_svg\s*-->.*?</div>', re.DOTALL)

def dedup(detail):
    matches = list(DIV_RE.finditer(detail))
    if len(matches) < 2:
        return detail, False
    # Keep the LAST match (which is our clean append), remove earlier ones
    # Actually — we should dedupe: keep one, drop the rest. Since both point to same SVG,
    # keep the first and remove rest OR keep last. It's safer to keep the last one (ours).
    # Remove earlier matches (indexes 0..n-2).
    # Build new string by concatenating slices between matches, skipping earlier ones.
    last = matches[-1]
    new_parts = []
    last_end = 0
    for m in matches[:-1]:
        new_parts.append(detail[last_end:m.start()])
        last_end = m.end()
    new_parts.append(detail[last_end:])  # from last_end to end includes the last match
    new_detail = "".join(new_parts)
    return new_detail, True


def main():
    with open(JSON_PATH) as f:
        data = json.load(f)
    fixed = 0
    for q in data:
        detail = q.get("explanation",{}).get("detail","")
        if not detail or '<!-- drawio_svg -->' not in detail:
            continue
        new_detail, changed = dedup(detail)
        if changed:
            q["explanation"]["detail"] = new_detail
            fixed += 1
    with open(JSON_PATH, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Fixed duplicates in {fixed} questions")

if __name__ == "__main__":
    main()
