#!/usr/bin/env python3
"""Collect every item of every symbol list ("legend") of the lessons into one CSV.

    python3 research/collect_symbols.py

Writes research/symbols_raw.csv with the columns
    module   number of the lesson (0 for pages without a number)
    file     source file
    section  heading under which the list stands
    symbol   the text before the first colon of the item (LaTeX kept)
    meaning  the text after it
"""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODS = ROOT / "src" / "modules"
OUT = ROOT / "research" / "symbols_raw.csv"


def main():
    rows = []
    for p in sorted(MODS.glob("*.md")):
        raw = p.read_text(encoding="utf-8")
        m = re.search(r"^num:\s*(\d+)", raw, flags=re.M)
        num = int(m.group(1)) if m else 0
        section, inside, item = "", False, None

        def flush():
            nonlocal item
            if item:
                text = " ".join(item.split())
                # split at the first colon that is not inside $...$
                depth, cut = False, -1
                for i, ch in enumerate(text):
                    if ch == "$":
                        depth = not depth
                    elif ch == ":" and not depth:
                        cut = i
                        break
                if cut > 0:
                    rows.append([num, p.name, section, text[:cut].strip(), text[cut + 1:].strip()])
                else:
                    rows.append([num, p.name, section, "", text])
            item = None

        for ln in raw.splitlines():
            s = ln.strip()
            h = re.match(r"#{2,4} (.+)", s)
            if h and not inside:
                section = re.sub(r"\s*\{#.*\}$", "", h.group(1))
            if s.startswith('<div class="legend"'):
                inside = True
                continue
            if inside and s.startswith("</div"):
                flush()
                inside = False
                continue
            if inside:
                if s.startswith("- "):
                    flush()
                    item = s[2:]
                elif s and item is not None:
                    item += " " + s
        flush()
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["module", "file", "section", "symbol", "meaning"])
        w.writerows(rows)
    per = {}
    for r in rows:
        per[r[1]] = per.get(r[1], 0) + 1
    print(f"{len(rows)} items from {len(per)} files -> {OUT.name}")
    for k in sorted(per):
        print(f"  {per[k]:4d}  {k}")


if __name__ == "__main__":
    main()
