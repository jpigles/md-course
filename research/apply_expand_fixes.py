#!/usr/bin/env python3
"""Apply reviewed corrections to the rewritten lessons.

    python3 research/apply_expand_fixes.py [--dry] research/expand_review/03-..._fixes.txt [more files]

Format of a fix file (one or more blocks):

    <file name in src/modules>
    @@OLD
    <text that occurs exactly once>
    @@NEW
    <replacement>
    @@END
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODS = ROOT / "src" / "modules"

BLOCK = re.compile(r"^[ \t]*(\S+\.md)[ \t]*\r?\n@@OLD\r?\n(.*?)\r?\n@@NEW\r?\n(.*?)\r?\n@@END", re.S | re.M)


def main():
    args = [a for a in sys.argv[1:] if a != "--dry"]
    dry = "--dry" in sys.argv
    if not args:
        sys.exit(__doc__)
    n_ok = n_skip = n_bad = 0
    for fx in args:
        text = Path(fx).read_text(encoding="utf-8").replace("\r\n", "\n")
        blocks = BLOCK.findall(text)
        print(f"{fx}: {len(blocks)} block(s)")
        for name, old, new in blocks:
            p = MODS / name
            if not p.exists():
                print(f"  NO SUCH FILE {name}")
                n_bad += 1
                continue
            s = p.read_text(encoding="utf-8")
            c = s.count(old)
            if new in s and (c == 0 or old in new):
                print(f"  already applied: {old[:60]!r}")
                n_skip += 1
            elif c != 1:
                print(f"  NOT MATCHED ({c} occurrences): {old[:70]!r}")
                n_bad += 1
            else:
                if not dry:
                    p.write_text(s.replace(old, new), encoding="utf-8", newline="\n")
                print(f"  ok: {name}: {old[:60]!r}")
                n_ok += 1
    print(f"applied {n_ok}, already there {n_skip}, failed {n_bad}" + (" (dry run)" if dry else ""))


if __name__ == "__main__":
    main()
