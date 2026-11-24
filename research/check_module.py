#!/usr/bin/env python3
"""Check one rewritten lesson against its original.

    python3 research/check_module.py 03-statistical-mechanics.md

new  = src/modules/<file>
old  = research/modules_before_expand/<file>

FAIL lines must be fixed. WARN lines must be looked at (some are acceptable).
Also writes research/expand_notes/<stem>_changed_sentences.txt : sentences of the
original that are no longer present word for word (for the reviewer).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import build  # noqa: E402  (md_to_html, parse_front)

OLD_DIR = ROOT / "research" / "modules_before_expand"
NEW_DIR = ROOT / "src" / "modules"
NOTES = ROOT / "research" / "expand_notes"

KATEX_OK = set("""
frac dfrac tfrac sqrt sum prod int oint partial nabla infty cdot cdots ldots dots times pm mp approx equiv
propto sim simeq neq ne le leq ge geq ll gg to rightarrow leftarrow Rightarrow Leftrightarrow leftrightarrow mapsto
langle rangle left right big Big bigg Bigg bigl bigr Bigl Bigr mathbf mathrm mathcal mathbb boldsymbol bm text textbf
textit operatorname hat tilde bar vec dot ddot overline underline underbrace overbrace alpha beta gamma delta epsilon
varepsilon zeta eta theta vartheta kappa lambda mu nu xi pi rho sigma tau phi varphi chi psi omega Gamma Delta Theta
Lambda Xi Pi Sigma Phi Psi Omega ln log exp sin cos tan sinh cosh tanh arccos arcsin arctan min max lim det
quad qquad begin end aligned cases matrix pmatrix bmatrix array displaystyle ell hbar in notin forall exists
binom Vert vert lvert rvert lVert rVert mid circ ast star dagger prime top perp parallel angle degree
underset overset stackrel substack tag nonumber boxed cancel color phantom hspace vphantom not land lor
cup cap subset setminus emptyset mathsf mathit erf erfc Re Im arg deg sup inf gcd Pr argmin argmax
iint iiint oplus otimes wedge vee uparrow downarrow longrightarrow implies iff tr
""".split())


def split_math(text):
    """Return (display list, inline list, prose with math removed)."""
    fence = re.compile(r"^```.*?^```[ \t]*$", re.S | re.M)
    t = fence.sub(" ", text)
    t = re.sub(r"`[^`\n]+`", " ", t)
    disp = [m.group(1) for m in build.DISPLAY.finditer(t)]
    t2 = build.DISPLAY.sub(" @@D@@ ", t)
    inl = [m.group(1) for m in build.INLINE.finditer(t2)]
    prose = build.INLINE.sub(" @@I@@ ", t2)
    return disp, inl, prose


def norm(s):
    return re.sub(r"\s+", "", s)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    name = sys.argv[1]
    new_p, old_p = NEW_DIR / name, OLD_DIR / name
    fails, warns = [], []
    if not new_p.exists():
        sys.exit(f"no such file: {new_p}")
    has_old = old_p.exists()
    new_meta, new_raw = build.parse_front(new_p)
    if has_old:
        old_meta, old_raw = build.parse_front(old_p)
    else:
        old_meta, old_raw = dict(new_meta), ""

    # 1 front matter
    if has_old and old_meta != new_meta:
        for k in sorted(set(old_meta) | set(new_meta)):
            if old_meta.get(k) != new_meta.get(k):
                fails.append(f"front matter changed: {k}: {old_meta.get(k)!r} -> {new_meta.get(k)!r}")

    # 2 renders
    try:
        body, _ = build.md_to_html(new_raw)
    except Exception as e:  # pragma: no cover
        sys.exit(f"FAIL: the Markdown does not convert: {e}")

    nd, ni, nprose = split_math(new_raw)
    od, oi, oprose = split_math(old_raw)

    # 3 things that must survive
    def find(pat, s):
        return re.findall(pat, s)

    for label, pat in (("video strip", r'<div data-videos="([^"]*)"></div>'),
                       ("widget", r'data-widget="([^"]+)"'),
                       ("placeholder", r"\{\{([A-Z_]+)\}\}")):
        o, n = find(pat, old_raw), find(pat, new_raw)
        for x in o:
            if o.count(x) > n.count(x):
                fails.append(f"{label} missing or changed: {x}")
        for x in n:
            if has_old and n.count(x) > o.count(x) and label != "placeholder":
                fails.append(f"{label} added (not allowed): {x}")
    oc, nc = find(r"\]\(cite:([A-Za-z0-9_-]+)\)", old_raw), find(r"\]\(cite:([A-Za-z0-9_-]+)\)", new_raw)
    for k in sorted(set(oc)):
        if nc.count(k) < oc.count(k):
            fails.append(f"citation link lost: cite:{k} ({oc.count(k)} before, {nc.count(k)} now)")
    for k in sorted(set(nc) - set(oc)):
        if has_old:
            fails.append(f"new citation key (not allowed): cite:{k}")
    oh = find(r"^## (.+)$", re.sub(r"^```.*?^```[ \t]*$", "", old_raw, flags=re.S | re.M))
    nh = find(r"^## (.+)$", re.sub(r"^```.*?^```[ \t]*$", "", new_raw, flags=re.S | re.M))
    for h in oh:
        if h.strip() == "Watch first":
            if "Lectures for this module" not in [x.strip() for x in nh]:
                fails.append('heading "## Watch first" must become "## Lectures for this module"')
        elif h not in nh:
            fails.append(f"a ## heading of the original is gone or reworded: {h}")
    oh3 = find(r"^### (.+)$", old_raw)
    nh3 = find(r"^### (.+)$", new_raw)
    for h in oh3:
        if h not in nh3:
            warns.append(f"a ### heading of the original is gone or reworded: {h}")

    # 4 every original display equation is still there, unchanged
    nd_norm = {norm(x) for x in nd}
    for x in od:
        if norm(x) not in nd_norm:
            fails.append("display equation of the original missing or altered: " + " ".join(x.split())[:110])

    # 5 numbers of the original
    numpat = re.compile(r"(?<![A-Za-z_\\])\d+(?:[.,]\d+)*")
    onum = numpat.findall(old_raw)
    new_all = new_raw
    lost = sorted({x for x in onum if len(x) >= 2 and x not in new_all})
    if lost:
        warns.append("numbers of the original that no longer appear anywhere: " + ", ".join(lost[:40]))

    # 6 sentences of the original no longer present verbatim (for the reviewer)
    def sentences(s):
        s = re.sub(r"^```.*?^```[ \t]*$", " ", s, flags=re.S | re.M)
        s = re.sub(r"\$\$.+?\$\$", " ", s, flags=re.S)
        out = []
        for para in re.split(r"\n\s*\n", s):
            para = " ".join(para.split())
            if not para or para.startswith(("<div", "</div", "{{", "---", "|")):
                continue
            out += [x.strip() for x in re.split(r"(?<=[.!?])\s+(?=[A-Z*$(\[])", para) if len(x.strip()) > 25]
        return out
    if has_old:
        flat_new = " ".join(new_raw.split())
        changed = [x for x in sentences(old_raw) if x not in flat_new]
        NOTES.mkdir(exist_ok=True)
        (NOTES / (Path(name).stem + "_changed_sentences.txt")).write_text(
            "\n\n".join(changed) + "\n", encoding="utf-8")
        n_old_sent = len(sentences(old_raw))
        if n_old_sent and len(changed) > 0.35 * n_old_sent:
            warns.append(f"{len(changed)} of {n_old_sent} original sentences are no longer present word for word "
                         f"(keep the checked sentences where you can)")

    # 7 legends
    lines = new_raw.splitlines()
    in_details = in_box = in_disp = False
    sec, sec_formulas, sec_legends = "(top)", 0, 0
    total_formulas = total_legends = 0
    first_formula = ""

    def close_section():
        if sec_formulas and not sec_legends:
            warns.append(f'section "{sec}" has {sec_formulas} displayed formula(s) and no legend '
                         f'(first: {first_formula[:70]})')
    for ln in lines:
        s = ln.strip()
        if s.startswith("<details"):
            in_details = True
        if s.startswith("</details"):
            in_details = False
            continue
        if s.startswith('<div class="box'):
            in_box = True
        elif s.startswith("</div") and in_box:
            in_box = False
        if re.match(r"#{2,3} ", s) and not in_disp:
            close_section()
            sec, sec_formulas, sec_legends, first_formula = s.lstrip("# "), 0, 0, ""
        if s.startswith('<div class="legend"'):
            total_legends += 1
            sec_legends += 1
            if 'markdown="1"' not in s:
                fails.append("a legend div without markdown=\"1\"")
        if s.startswith("$$"):
            single = s.count("$$") == 2 and len(s) > 4          # $$ ... $$ on one line
            if single or not in_disp:
                if not (in_details or in_box):
                    total_formulas += 1
                    sec_formulas += 1
                    if not first_formula:
                        first_formula = s if single else "(multi-line)"
            if not single:
                in_disp = not in_disp
        elif in_disp and not first_formula.strip("(multi-line)"):
            first_formula = s
    close_section()
    if total_formulas and total_legends < 0.6 * total_formulas:
        warns.append(f"{total_formulas} displayed formulas outside boxes but only {total_legends} legends")

    # 8 syntax hazards
    if new_raw.count("$$") % 2:
        fails.append("odd number of $$ markers")
    for x in nd:
        if "cite:" in x:
            fails.append("a cite link inside a display formula")
    known = set(KATEX_OK)
    for x in od + oi:
        known |= set(re.findall(r"\\([A-Za-z]+)", x))
    for p in OLD_DIR.glob("*.md"):
        d, i, _ = split_math(p.read_text(encoding="utf-8"))
        for x in d + i:
            known |= set(re.findall(r"\\([A-Za-z]+)", x))
    unknown = {}
    for x in nd + ni:
        for c in re.findall(r"\\([A-Za-z]+)", x):
            if c not in known:
                unknown.setdefault(c, x)
        y = re.sub(r"\\[{}]", "", x)
        if y.count("{") != y.count("}"):
            fails.append("unbalanced { } in formula: " + " ".join(x.split())[:100])
        if len(re.findall(r"\\left(?![A-Za-z])", x)) != len(re.findall(r"\\right(?![A-Za-z])", x)):
            fails.append("\\left and \\right do not pair up in: " + " ".join(x.split())[:100])
        if sorted(re.findall(r"\\begin\{(\w+\*?)\}", x)) != sorted(re.findall(r"\\end\{(\w+\*?)\}", x)):
            fails.append("\\begin and \\end do not pair up in: " + " ".join(x.split())[:100])
    for c, x in sorted(unknown.items()):
        warns.append(f"LaTeX command \\{c} was not used in the course before: make sure KaTeX supports it "
                     f"(in: {' '.join(x.split())[:60]})")
    if "\\dddot" in new_raw:
        fails.append("\\dddot is not supported by KaTeX")

    # stray dollars / unconverted markers in the HTML
    text_only = re.sub(r"<pre.*?</pre>|<code.*?</code>", " ", body, flags=re.S)
    text_only = re.sub(r'<span class="math-(?:display|inline)">.*?</span>', " ", text_only, flags=re.S)
    for m in re.finditer(r"\$", text_only):
        ctx = " ".join(text_only[max(0, m.start() - 60): m.start() + 60].split())
        warns.append("a $ sign survived as text (an inline formula did not match; no line break inside $...$, "
                     "no space next to the $ signs, closing $ not followed by a digit): ..." + ctx + "...")
        if len(warns) > 60:
            break
    if "@@MATH" in body:
        fails.append("internal math marker left in the output")
    if 'markdown="1"' in body:
        warns.append('markdown="1" survived in the output: a <div ... markdown="1"> block was not parsed '
                     "(it must start at the beginning of a line with a blank line before it)")
    for m in re.finditer(r"\*\*[^*<]{1,80}\*\*", text_only):
        warns.append("bold markers survived as text (Markdown not parsed there): " + m.group(0)[:70])

    # toolbox links
    anchors_file = ROOT / "research" / "toolbox_anchors.md"
    allowed = set(re.findall(r"`((?:maths|physics)\.html#[a-z0-9-]+)`", anchors_file.read_text(encoding="utf-8"))) \
        if anchors_file.exists() else set()
    for a in sorted(set(re.findall(r"\]\(((?:maths|physics)\.html#[a-z0-9-]+)\)", new_raw))):
        if allowed and a not in allowed:
            fails.append(f"link to a toolbox anchor that is not in research/toolbox_anchors.md: {a}")
    for a in sorted(set(re.findall(r"\]\(([0-9a-z-]+\.html)(?:#[^)]*)?\)", new_raw))):
        if not (NEW_DIR / a.replace(".html", ".md")).exists() and a not in ("maths.html", "physics.html", "symbols.html"):
            fails.append(f"link to a page that does not exist: {a}")

    # the two background pages must contain every anchor the lessons may link to
    stem = Path(name).stem
    if stem in ("maths", "physics"):
        have = re.findall(r"^## .+\{#([a-z0-9-]+)\}\s*$", new_raw, flags=re.M)
        want = [a.split("#")[1] for a in re.findall(r"`((?:maths|physics)\.html#[a-z0-9-]+)`",
                anchors_file.read_text(encoding="utf-8")) if a.startswith(stem + ".html")]
        for a in want:
            if a not in have:
                fails.append(f"section missing: ## ... {{#{a}}}")
        if [a for a in have if a in want] != want and not [a for a in want if a not in have]:
            warns.append("the sections are not in the order of research/toolbox_anchors.md")
        for a in re.findall(r"\]\(#([a-z0-9-]+)\)", new_raw):
            if a not in have:
                fails.append(f"link to a section that is not on this page: #{a}")

    ow, nw = len(old_raw.split()), len(new_raw.split())
    print(f"{name}: words {ow} -> {nw} ({(nw / ow if ow else 0):.2f}x); displayed formulas {len(od)} -> {len(nd)}; "
          f"legends {total_legends}; maths boxes {new_raw.count('class=\"box maths\"')}")
    for f in fails:
        print("FAIL:", f)
    for w in warns:
        print("WARN:", w)
    if not fails and not warns:
        print("OK")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
