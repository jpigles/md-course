#!/usr/bin/env python3
"""Build the MD course site.

    python3 build.py

Reads  src/modules/*.md  (front matter + Markdown with $...$ / $$...$$ math),
       research/videos.json, research/books_notes_tutorials.json, research/papers.csv
Writes site/*.html (flat folder, ready for GitHub Pages).
"""
import csv
import html
import json
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
SITE = ROOT / "site"
RESEARCH = ROOT / "research"

VIDEO_TOPICS = {
    1: "Whole courses on molecular simulation",
    2: "Classical mechanics background",
    3: "Statistical mechanics",
    4: "Numerical integrators",
    5: "Force fields and water models",
    6: "Periodic boundaries, cutoffs, neighbour lists",
    7: "Ewald summation and PME",
    8: "Thermostats and barostats",
    9: "Constraints",
    10: "Practical set-up and software tutorials",
    11: "Trajectory analysis and error estimates",
    12: "Free energy calculations",
    13: "Enhanced sampling",
    14: "Coarse-grained and implicit-solvent models",
    15: "Markov state models and kinetics",
    16: "Machine-learned potentials and the big picture",
    17: "Alchemical free energy and non-equilibrium work",
    18: "Force-field parameterisation and polarizable models",
}
PAPER_GROUPS = {
    "A": "History and overviews",
    "B": "Integrators",
    "C": "Constraints",
    "D": "Thermostats and barostats",
    "E": "Electrostatics and cutoffs",
    "F": "Force fields",
    "G": "Water and ion models",
    "H": "Free energy",
    "I": "Enhanced sampling",
    "J": "Coarse-graining and implicit solvent",
    "K": "Kinetics and Markov models",
    "L": "Machine-learned potentials",
    "M": "Software",
    "N": "Machine-learning models trained on MD data",
}

# ----------------------------------------------------------------------------
# research data
# ----------------------------------------------------------------------------

def load_videos():
    f = RESEARCH / "videos.json"
    if not f.exists():
        return []
    data = json.loads(f.read_text(encoding="utf-8"))
    return [v for v in data if v.get("verified") and v.get("url")]


def load_books():
    f = RESEARCH / "books_notes_tutorials.json"
    if not f.exists():
        return {"books": [], "notes_courses": [], "tutorials_docs": []}
    d = json.loads(f.read_text(encoding="utf-8"))
    for k in ("books", "notes_courses", "tutorials_docs"):
        d.setdefault(k, [])
    return d


def load_papers():
    f = RESEARCH / "papers.csv"
    if not f.exists():
        return []
    with open(f, encoding="utf-8", newline="") as fh:
        rows = [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(fh)]
    rows = [r for r in rows if r.get("verified", "").lower() == "yes" and r.get("doi")]
    # arXiv preprints found by title (research/arxiv_lookup.py): a free copy when there is no other
    hits = RESEARCH / "arxiv_hits.json"
    if hits.exists():
        arx = json.loads(hits.read_text(encoding="utf-8"))
        for r in rows:
            h = arx.get(r["key"])
            if h:
                r["preprint_url"] = h["abs"]
    extra = RESEARCH / "papers_ml.csv"          # the papers read for Module 18
    if extra.exists():
        with open(extra, encoding="utf-8", newline="") as fh:
            rows += [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(fh)]
    notes = load_paper_notes()
    for r in rows:
        n = notes.get(r["key"], {})
        r["read"] = n.get("read", r.get("read", ""))
        r["annotation"] = n.get("annotation", r.get("annotation", ""))
        r["read_guide"] = n.get("read_guide", r.get("read_guide", ""))
    return rows


def load_paper_notes():
    """What was learned from reading each paper: {key: {read, annotation, read_guide}} (research/paper_notes.json)."""
    f = RESEARCH / "paper_notes.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def load_video_registry(videos):
    """Every YouTube video the site may link to: the catalogued single videos and every lecture
    listed inside a catalogued playlist (read from YouTube by research/video_metadata.py)."""
    reg = {}
    f = RESEARCH / "video_meta.json"
    meta = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    for v in videos:
        who = v.get("lecturer") or v.get("channel") or ""
        if v.get("kind") == "playlist":
            for it in meta.get(v["url"], {}).get("items", []):
                reg.setdefault(it["id"], {"title": it["title"], "seconds": it.get("seconds"), "by": who, "course": v["title"]})
        else:
            m = re.search(r"[?&]v=([A-Za-z0-9_-]{11})", v["url"])
            if m:
                reg[m.group(1)] = {"title": v["title"], "seconds": meta.get(v["url"], {}).get("seconds"), "by": who, "course": ""}
    return reg


def minutes(seconds):
    if not seconds:
        return ""
    m = round(seconds / 60)
    return f"{m // 60} h {m % 60:02d} min" if m >= 60 else f"{max(1, m)} min"


E = lambda s: html.escape(str(s if s is not None else ""), quote=True)


def video_li(v):
    kind = "Playlist" if v.get("kind") == "playlist" else "Video"
    meta = [kind]
    if v.get("n_videos"):
        meta.append(f"{v['n_videos']} videos")
    if v.get("duration_min"):
        meta.append(f"{int(v['duration_min'])} min")
    if v.get("level"):
        meta.append(v["level"])
    who = v.get("lecturer") or v.get("channel") or ""
    chan = v.get("channel") or ""
    by = E(who) + (f" &middot; channel: {E(chan)}" if chan and chan != who else "")
    return (
        f'<li class="res"><a href="{E(v["url"])}" target="_blank" rel="noopener">{E(v.get("title"))}</a>'
        f'<span class="res-meta">{by} &middot; {E(", ".join(meta))}</span>'
        f'<span class="res-why">{E(v.get("why"))}</span></li>'
    )


def videos_block(videos, topics):
    out = []
    for t in topics:
        vs = [v for v in videos if int(v.get("topic", 0)) == t]
        vs.sort(key=lambda v: (v.get("kind") != "playlist", {"intro": 0, "intermediate": 1, "advanced": 2}.get(v.get("level"), 1)))
        if not vs:
            continue
        if len(topics) > 1:
            out.append(f"<h4>{E(VIDEO_TOPICS[t])}</h4>")
        out.append('<ul class="reslist">' + "".join(video_li(v) for v in vs) + "</ul>")
    if not out:
        return '<p class="muted">The video list for this module is in the <a href="library.html">library</a>.</p>'
    return "\n".join(out)


def book_li(b, with_chapters=True):
    url = b.get("free_url") or b.get("url") or ""
    title = E(b.get("title"))
    link = f'<a href="{E(url)}" target="_blank" rel="noopener">{title}</a>' if url else title
    meta = [x for x in (b.get("authors"), b.get("edition_year"), b.get("publisher_or_host")) if x]
    free = ' <span class="tag free">free</span>' if b.get("free") else ""
    ch = b.get("best_chapters") or ""
    ch_html = f'<span class="res-why"><b>Where to read:</b> {E(ch)}</span>' if (ch and with_chapters) else ""
    return (
        f'<li class="res">{link}{free}<span class="res-meta">{E(" · ".join(str(m) for m in meta))}</span>'
        f'<span class="res-why">{E(b.get("why"))}</span>{ch_html}</li>'
    )


def books_block(books, tags, limit=7):
    def pick(arr):
        hits = [b for b in arr if set(b.get("covers") or []) & set(tags)]
        # most specific first: fewer tags = more focused resource
        hits.sort(key=lambda b: (not b.get("free"), len(b.get("covers") or [])))
        return hits
    out = []
    bk = pick(books["books"])[:limit]
    nt = pick(books["notes_courses"])[:limit]
    tu = pick(books["tutorials_docs"])[:limit]
    if bk:
        out.append("<h4>Textbooks</h4><ul class='reslist'>" + "".join(book_li(b) for b in bk) + "</ul>")
    if nt:
        out.append("<h4>Free notes and open courses</h4><ul class='reslist'>" + "".join(book_li(b) for b in nt) + "</ul>")
    if tu:
        out.append("<h4>Tutorials and documentation</h4><ul class='reslist'>" + "".join(book_li(b) for b in tu) + "</ul>")
    return "\n".join(out)


def paper_li(p):
    oa = ""
    oa_url = p.get("oa_url") or ""
    pre = p.get("preprint_url") or (oa_url if "arxiv.org" in oa_url else "")
    if oa_url and "arxiv.org" not in oa_url:
        oa = f' <a class="tag free" href="{E(oa_url)}" target="_blank" rel="noopener">open access</a>'
    if pre:
        oa += f' <a class="tag free" href="{E(pre)}" target="_blank" rel="noopener">arXiv preprint</a>'
    vol = p.get("volume")
    pages = p.get("pages")
    cite = E(p.get("journal"))
    if vol:
        cite += f" <b>{E(vol)}</b>"
    if pages:
        cite += f", {E(pages)}"
    badge = ""
    if p.get("read") == "full":
        badge = ' <span class="tag read" title="The full text of this paper was read while checking the course">read in full</span>'
    elif p.get("read") == "part":
        badge = ' <span class="tag read" title="Parts of this paper were read while checking the course">read in part</span>'
    note = ""
    if p.get("annotation"):
        note += f'<span class="res-why">{E(p["annotation"])}</span>'
    if p.get("read_guide"):
        note += f'<span class="res-why"><b>What to read in it:</b> {E(p["read_guide"])}</span>'
    link = p.get("url") or ("https://doi.org/" + p["doi"] if p.get("doi") else "")
    return (
        f'<li class="res" id="ref-{E(p["key"])}"><span class="res-auth">{E(p.get("authors"))} ({E(p.get("year"))}).</span> '
        f'<a href="{E(link)}" target="_blank" rel="noopener">{E(p.get("title"))}</a>. '
        f'<i>{cite}</i>.{oa}{badge}{note}</li>'
    )


def papers_block(papers, groups):
    out = []
    for g in groups:
        ps = [p for p in papers if p.get("group", "").upper() == g]
        ps.sort(key=lambda p: (p.get("year") or "0", p.get("authors") or ""))
        if not ps:
            continue
        if len(groups) > 1:
            out.append(f"<h4>{E(PAPER_GROUPS[g])}</h4>")
        out.append('<ul class="reslist papers">' + "".join(paper_li(p) for p in ps) + "</ul>")
    return "\n".join(out)

# ----------------------------------------------------------------------------
# markdown with protected math
# ----------------------------------------------------------------------------

FENCE = re.compile(r"(^```.*?^```[ \t]*$)", re.S | re.M)
INLINE_CODE = re.compile(r"(`[^`\n]+`)")
DISPLAY = re.compile(r"\$\$(.+?)\$\$", re.S)
INLINE = re.compile(r"(?<![\\$])\$(?!\s)([^$\n]+?)(?<![\\\s])\$(?!\d)")


def protect_math(text, store):
    def keep(kind):
        def f(m):
            store.append((kind, m.group(1)))
            return f"@@MATH{len(store) - 1}@@"
        return f

    parts = FENCE.split(text)
    for i in range(0, len(parts), 2):  # even = outside fenced code
        sub = INLINE_CODE.split(parts[i])
        for j in range(0, len(sub), 2):
            s = DISPLAY.sub(keep("d"), sub[j])
            s = INLINE.sub(keep("i"), s)
            sub[j] = s
        parts[i] = "".join(sub)
    return "".join(parts)


def restore_math(htmltext, store):
    def f(m):
        kind, tex = store[int(m.group(1))]
        tex = html.escape(tex.strip(), quote=False)
        if kind == "d":
            return f'<span class="math-display">\\[{tex}\\]</span>'
        return f'<span class="math-inline">\\({tex}\\)</span>'
    return re.sub(r"@@MATH(\d+)@@", f, htmltext)


def md_to_html(text):
    store = []
    text = protect_math(text, store)
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "toc", "attr_list", "md_in_html", "sane_lists", "codehilite"],
        extension_configs={
            "toc": {"toc_depth": "2-2", "permalink": False},
            "codehilite": {"guess_lang": False, "css_class": "code"},
        },
    )
    body = md.convert(text)
    body = body.replace("\\$", "$")
    toc_tokens = getattr(md, "toc_tokens", [])
    return restore_math(body, store), toc_tokens


def parse_front(path):
    raw = path.read_text(encoding="utf-8")
    meta = {}
    if raw.startswith("---"):
        _, fm, raw = raw.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta, raw.lstrip("\n")

# ----------------------------------------------------------------------------
# the list of symbols, collected from the lists under the formulas
# ----------------------------------------------------------------------------

GREEK = ("alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi pi rho sigma tau "
         "upsilon phi chi psi omega").split()
GREEK_CANON = {"varepsilon": "epsilon", "vartheta": "theta", "varphi": "phi", "varrho": "rho"}
GREEK_CAPS = {"gamma", "delta", "theta", "lambda", "xi", "pi", "sigma", "phi", "psi", "omega"}
SYM_STRIP = re.compile(
    r"\\(?:mathbf|boldsymbol|bm|mathrm|mathcal|mathbb|mathsf|mathit|tilde|hat|bar|dot|ddot|vec|overline|underline|"
    r"left|right|big|Big|bigg|Bigg|bigl|bigr|Bigl|Bigr|tfrac|dfrac|frac|sqrt|text|operatorname|displaystyle|"
    r"partial|ln|log|exp|min|max|quad|qquad)(?![A-Za-z])")
SYM_OPS = set("sum prod int oint nabla equiv approx propto cdot times langle le leq ge geq ll gg sim simeq to infty pm "
              "mp in ne neq leftarrow rightarrow ldots dots cdots lvert lVert vert Vert mid circ".split())


def symbol_group(head):
    """(sort key, label) of the group a symbol is filed under, or None when the item is not a symbol."""
    m = re.search(r"(?<!\\)\$(.+?)(?<!\\)\$", head)
    if not m:
        return None
    tex = m.group(1).strip()
    first = re.match(r"\\([A-Za-z]+)", tex)
    if (first and first.group(1) in SYM_OPS) or tex[:1] in "|{[(<=+-/\\" and not first:
        return ("~", "Signs and operators")
    t = SYM_STRIP.sub(" ", tex)
    t = re.sub(r"\\Delta\s*(?=[A-Za-z\\])", " ", t)      # Delta G is filed under G
    for tok in re.finditer(r"\\([A-Za-z]+)|([A-Za-z])", t):
        if tok.group(1):
            name = tok.group(1)
            canon = GREEK_CANON.get(name.lower(), name.lower())
            if canon in GREEK:
                return (f"zz{GREEK.index(canon):02d}", canon)
            if name == "ell":
                return ("l", "L")
            if name == "hbar":
                return ("h", "H")
            continue
        return (tok.group(2).lower(), tok.group(2).upper())
    return ("~", "Signs and operators")


def collect_symbols(mods):
    """One row per symbol and lesson: the first definition of that symbol in that lesson."""
    from markdown.extensions.toc import slugify
    rows, seen = [], set()
    for m in mods:
        section, sec_slug, inside, item, used = "", "", False, None, {}

        def flush():
            nonlocal item
            if item:
                text = " ".join(item.split())
                in_math, cut = False, -1
                for i, ch in enumerate(text):
                    if ch == "$" and (i == 0 or text[i - 1] != "\\"):
                        in_math = not in_math
                    elif ch == ":" and not in_math:
                        cut = i
                        break
                if cut > 0:
                    head, meaning = text[:cut].strip(), text[cut + 1:].strip()
                    g = symbol_group(head)
                    key = (re.sub(r"\s+", "", head), m["slug"])
                    if g and meaning and key not in seen:
                        seen.add(key)
                        rows.append({"head": head, "meaning": meaning, "group": g, "num": int(m["num"]),
                                     "slug": m["slug"], "section": section, "anchor": sec_slug})
            item = None

        in_fence = False
        for ln in m["raw"].splitlines():
            s = ln.strip()
            if s.startswith("```"):
                in_fence = not in_fence
            if in_fence:
                continue
            h = re.match(r"#{1,6} (.+)", s)
            if h and not inside:
                title = re.sub(r"\s*\{[#.][^}]*\}\s*$", "", h.group(1)).strip()
                if "$" in title:
                    section, sec_slug = "", ""
                else:
                    base = slugify(html.unescape(re.sub(r"[*`]", "", title)), "-")
                    n = used.get(base, 0)
                    used[base] = n + 1
                    section, sec_slug = re.sub(r"[*`]", "", title), (base if n == 0 else f"{base}_{n}")
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
    return rows


def cells_to_html(cells):
    """Convert many short Markdown fragments (with maths) in one pass."""
    body, _ = md_to_html("\n\n@@CELLSEP@@\n\n".join(cells))
    parts = [re.sub(r"^<p>|</p>$", "", p.strip()) for p in re.split(r"<p>@@CELLSEP@@</p>", body)]
    if len(parts) != len(cells):                      # a fragment was read as a block: convert one by one
        parts = [re.sub(r"^<p>|</p>$", "", md_to_html(c)[0].strip()) for c in cells]
    return parts


def symbol_table(mods, built):
    rows = collect_symbols(mods)
    rows.sort(key=lambda r: (r["group"][0], re.sub(r"[^a-z0-9]", "", r["head"].lower()), r["head"], r["num"]))
    cells = cells_to_html([r["head"] for r in rows] + [r["meaning"] for r in rows])
    heads, means = cells[:len(rows)], cells[len(rows):]
    groups, order = {}, []
    for r, hd, mn in zip(rows, heads, means):
        if r["group"] not in groups:
            groups[r["group"]] = []
            order.append(r["group"])
        frag = f'#{r["anchor"]}' if r["anchor"] and f'id="{r["anchor"]}"' in built.get(r["slug"], "") else ""
        where = f'Module {r["num"]}' + (f': {E(r["section"])}' if r["section"] else "")
        groups[r["group"]].append(
            f'<tr data-s="{E((r["head"] + " " + r["meaning"]).lower())}"><td class="sym">{hd}</td><td>{mn}</td>'
            f'<td class="where"><a href="{r["slug"]}.html{frag}">{where}</a></td></tr>')

    def label(g):
        key, name = g
        if key.startswith("zz"):
            cap = f' <span class="math-inline">\\(\\{name.capitalize()}\\)</span>' if name in GREEK_CAPS else ""
            return f'<span class="math-inline">\\(\\{name}\\)</span>{cap} {name}'
        return E(name)

    def gid(g):
        return "sym-" + re.sub(r"[^a-z]", "", g[1].lower() if g[0] != "~" else "signs")

    out = ['<div class="symfilter"><input id="symFilter" type="search" autocomplete="off" '
           'placeholder="Type a letter or a name: lambda, sigma, k_B, tau" aria-label="Filter the list of symbols">'
           '<span id="symCount"></span></div>',
           '<p class="symjump">' + " ".join(
               f'<a href="#{gid(g)}">{label(g) if g[0].startswith("zz") else E(g[1] if g[0] != "~" else "signs")}</a>'
               for g in order) + "</p>"]
    for g in order:
        out.append(f'<div class="symgroup"><h3 id="{gid(g)}">{label(g)}</h3><table class="symtab"><thead><tr>'
                   f'<th>Symbol</th><th>Meaning</th><th>Defined in</th></tr></thead><tbody>'
                   + "".join(groups[g]) + "</tbody></table></div>")
    return "\n".join(out), len(rows)

# ----------------------------------------------------------------------------
# page template
# ----------------------------------------------------------------------------

KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Molecular Dynamics: a course</title>
<meta name="description" content="{desc}">
<script>try{{var t=localStorage.getItem('mdc-theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}</script>
<link rel="stylesheet" href="{katex}/katex.min.css">
<link rel="stylesheet" href="style.css">
</head>
<body data-page="{slug}">
<header class="topbar">
  <button class="menu-btn" id="menuBtn" aria-label="Open the module list">&#9776;</button>
  <a class="brand" href="index.html">Molecular Dynamics <span>a course from Newton to free energies</span></a>
  <nav class="toplinks"><a class="wide" href="maths.html">Maths</a><a class="wide" href="physics.html">Physics</a><a class="wide" href="symbols.html">Symbols</a><a href="library.html">Library</a><a href="formula-sheet.html">Formula sheet</a>
  <button id="themeBtn" class="theme-btn" aria-label="Switch between light and dark">&#9680;</button></nav>
</header>
<div class="layout">
<aside class="sidebar" id="sidebar">
  <div class="progress"><div class="progress-bar"><div id="progressFill"></div></div><span id="progressText"></span></div>
  <ol class="modlist">{nav}</ol>
  <ul class="extralist">{extra}</ul>
</aside>
<main class="content">
{hero}
{toc}
<article>
{body}
</article>
{donebox}
<div class="prevnext">{prev}{next}</div>
<footer>Written for self-study. Linked videos, books and papers belong to their authors and publishers.</footer>
</main>
</div>
<script defer src="{katex}/katex.min.js"></script>
<script defer src="{katex}/contrib/auto-render.min.js"></script>
<script defer src="course.js"></script>
<script defer src="demos2.js"></script>
</body>
</html>
"""


def build():
    SITE.mkdir(exist_ok=True)
    videos, books, papers = load_videos(), load_books(), load_papers()
    mods, extras = [], []
    for p in sorted((SRC / "modules").glob("*.md")):
        meta, raw = parse_front(p)
        meta["raw"] = raw
        meta.setdefault("slug", p.stem)
        (mods if meta.get("num") else extras).append(meta)
    mods.sort(key=lambda m: int(m["num"]))
    order = {"index": 0, "maths": 1, "physics": 2, "symbols": 3, "toy-data": 4, "projects": 5,
             "formula-sheet": 6, "library": 7, "sources": 8}
    registry = load_video_registry(videos)
    by_key = {p["key"]: p for p in papers}
    extras.sort(key=lambda m: order.get(m["slug"], 9))

    def nav_html(current):
        items = []
        for m in mods:
            cls = ' class="current"' if m["slug"] == current else ""
            items.append(
                f'<li{cls} data-slug="{m["slug"]}"><a href="{m["slug"]}.html"><span class="tick"></span>'
                f'<span class="n">{int(m["num"])}</span>{E(m.get("short") or m["title"])}</a></li>'
            )
        return "".join(items)

    def extra_html(current):
        items = []
        for m in extras:
            cls = ' class="current"' if m["slug"] == current else ""
            items.append(f'<li{cls}><a href="{m["slug"]}.html">{E(m.get("short") or m["title"])}</a></li>')
        return "".join(items)

    # blocks that pages can pull in
    def module_table():
        rows = []
        part = None
        for m in mods:
            if m.get("part") and m["part"] != part:
                part = m["part"]
                rows.append(f'<tr class="part"><td colspan="4">{E(part)}</td></tr>')
            rows.append(
                f'<tr data-slug="{m["slug"]}"><td class="num"><span class="tick"></span>{int(m["num"])}</td>'
                f'<td><a href="{m["slug"]}.html">{E(m["title"])}</a></td>'
                f'<td>{E(m.get("summary", ""))}</td><td class="num">{E(m.get("hours", ""))}</td></tr>'
            )
        return (
            '<div class="tablewrap"><table class="syllabus"><thead><tr><th>#</th><th>Module</th>'
            "<th>What you will be able to do</th><th>Hours</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table></div>"
        )

    def course_playlists():
        vs = [v for v in videos if int(v.get("topic", 0)) == 1 and v.get("kind") == "playlist"]
        if not vs:
            return '<p class="muted">See the <a href="library.html">library</a>.</p>'
        return '<ul class="reslist">' + "".join(video_li(v) for v in vs) + "</ul>"

    def library_videos():
        out = []
        for t in VIDEO_TOPICS:
            vs = [v for v in videos if int(v.get("topic", 0)) == t]
            if not vs:
                continue
            vs.sort(key=lambda v: (v.get("kind") != "playlist",))
            out.append(f'<h3 id="v{t}">{E(VIDEO_TOPICS[t])} <span class="count">{len(vs)}</span></h3>')
            out.append('<ul class="reslist">' + "".join(video_li(v) for v in vs) + "</ul>")
        return "\n".join(out) or '<p class="muted">No videos listed yet.</p>'

    def library_books(key):
        arr = books[key]
        if not arr:
            return '<p class="muted">Nothing listed yet.</p>'
        return '<ul class="reslist">' + "".join(book_li(b) for b in arr) + "</ul>"

    def library_papers():
        out = []
        for g in PAPER_GROUPS:
            ps = [p for p in papers if p.get("group", "").upper() == g]
            if not ps:
                continue
            ps.sort(key=lambda p: (p.get("year") or "0", p.get("authors") or ""))
            out.append(f'<h3 id="p{g}">{E(PAPER_GROUPS[g])} <span class="count">{len(ps)}</span></h3>')
            out.append('<ul class="reslist papers">' + "".join(paper_li(p) for p in ps) + "</ul>")
        return "\n".join(out) or '<p class="muted">No papers listed yet.</p>'

    counts = {
        "N_VIDEOS": str(len(videos)),
        "N_BOOKS": str(len(books["books"])),
        "N_NOTES": str(len(books["notes_courses"]) + len(books["tutorials_docs"])),
        "N_PAPERS": str(len(papers)),
        "N_MODULES": str(len(mods)),
        "N_HOURS": str(sum(int(m.get("hours", 0) or 0) for m in mods)),
        "N_WIDGETS": str(sum(m["raw"].count('data-widget="') for m in mods)),
        "N_LECTURES": str(len(registry)),
        "N_READ_FULL": str(sum(1 for p in papers if p.get("read") == "full")),
        "N_READ_PART": str(sum(1 for p in papers if p.get("read") == "part")),
        "N_NOT_READ": str(sum(1 for p in papers if p.get("read") not in ("full", "part"))),
    }

    used_videos = set()

    def section_videos(match):
        ids = re.findall(r"[A-Za-z0-9_-]{11}", match.group(1))
        items = []
        for vid in ids:
            if vid not in registry:
                raise SystemExit(f"a section names a video that is not in the verified list: {vid}")
            r = registry[vid]
            used_videos.add(vid)
            meta = " · ".join(x for x in (minutes(r["seconds"]), r["by"]) if x)
            items.append(
                f'<a class="sv" data-yt="{vid}" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener" '
                f'title="{E(r["course"])}"><span class="sv-play">&#9654;</span><span class="sv-t">{E(r["title"])}</span>'
                f'<span class="sv-m">{E(meta)}</span></a>')
        return '<div class="secvideos"><span class="sv-label">Lectures on this part (optional)</span>' + "".join(items) + "</div>"

    def cite_link(match):
        key = match.group(1)
        if key not in by_key:
            raise SystemExit(f"citation to a paper that is not in the verified list: {key}")
        p = by_key[key]
        link = p.get("url") or "https://doi.org/" + p["doi"]
        tip = f'{p["authors"]} ({p["year"]}). {p["title"]}. {p["journal"]}'
        return f'href="{E(link)}" class="cite" target="_blank" rel="noopener" title="{E(tip)}"'

    allpages = mods + extras
    built = {}
    for m in allpages:
        raw = m["raw"]
        vt = [int(x) for x in re.findall(r"\d+", m.get("videos", ""))]
        pg = [x for x in re.findall(r"[A-Z]", m.get("papers", ""))]
        tags = [x.strip() for x in m.get("tags", "").split(",") if x.strip()]
        body, toc_tokens = md_to_html(raw)
        blocks = {
            "WATCH": videos_block(videos, vt) if vt else "",
            "READ": books_block(books, tags) if tags else "",
            "PAPERS": papers_block(papers, pg) if pg else "",
            "MODULE_TABLE": module_table(),
            "COURSE_PLAYLISTS": course_playlists(),
            "LIB_VIDEOS": library_videos(),
            "LIB_BOOKS": library_books("books"),
            "LIB_NOTES": library_books("notes_courses"),
            "LIB_TUTORIALS": library_books("tutorials_docs"),
            "LIB_PAPERS": library_papers(),
        }
        blocks.update(counts)
        if "{{SYMBOL_TABLE}}" in raw or "{{N_SYMBOLS}}" in raw:
            table, n_sym = symbol_table(mods, built)
            blocks["SYMBOL_TABLE"], blocks["N_SYMBOLS"] = table, f"{n_sym:,}"
        for k, v in blocks.items():
            body = body.replace("<p>{{" + k + "}}</p>", v).replace("{{" + k + "}}", v)
        body = re.sub(r'<div data-videos="([^"]*)"></div>', section_videos, body)
        body = re.sub(r'href="cite:([A-Za-z0-9_-]+)"', cite_link, body)
        left = re.findall(r"\{\{[A-Z_]+[:}]", body)
        if left:
            raise SystemExit(f"unfilled placeholder in {m['slug']}: {left[:3]}")

        built[m["slug"]] = body
        is_mod = bool(m.get("num"))
        if is_mod:
            i = mods.index(m)
            hero = (
                f'<div class="hero"><div class="eyebrow">{E(m.get("part", ""))} &middot; Module {int(m["num"])} of {len(mods)}'
                f' &middot; about {E(m.get("hours", "?"))} hours</div><h1>{E(m["title"])}</h1>'
                f'<p class="lede">{E(m.get("summary", ""))}</p></div>'
            )
            prev = f'<a class="prev" href="{mods[i-1]["slug"]}.html">&larr; {E(mods[i-1]["title"])}</a>' if i > 0 else '<a class="prev" href="index.html">&larr; Course home</a>'
            nxt = f'<a class="next" href="{mods[i+1]["slug"]}.html">{E(mods[i+1]["title"])} &rarr;</a>' if i < len(mods) - 1 else '<a class="next" href="library.html">Library &rarr;</a>'
            donebox = '<div class="donebox"><label><input type="checkbox" id="doneChk"> I have finished this module</label></div>'
            toc = ""
            if toc_tokens:
                toc = '<nav class="toc"><b>In this module</b><ol>' + "".join(
                    f'<li><a href="#{t["id"]}">{t["name"]}</a></li>' for t in toc_tokens) + "</ol></nav>"
        else:
            hero = f'<div class="hero"><h1>{E(m["title"])}</h1><p class="lede">{E(m.get("summary", ""))}</p></div>'
            prev = nxt = donebox = toc = ""
            if m["slug"] == "index":
                nxt = f'<a class="next" href="{mods[0]["slug"]}.html">Start: {E(mods[0]["title"])} &rarr;</a>'
        page = PAGE.format(
            title=E(m["title"]), desc=E(m.get("summary", "")), slug=m["slug"], katex=KATEX,
            nav=nav_html(m["slug"]), extra=extra_html(m["slug"]), hero=hero, toc=toc, body=body,
            donebox=donebox, prev=prev, next=nxt,
        )
        (SITE / f'{m["slug"]}.html').write_text(page, encoding="utf-8", newline="\n")

    for f in ("style.css", "course.js", "demos2.js"):
        shutil.copyfile(SRC / f, SITE / f)
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    print(f"built {len(allpages)} pages; videos={len(videos)} books={len(books['books'])} "
          f"notes={len(books['notes_courses'])} tutorials={len(books['tutorials_docs'])} papers={len(papers)}; "
          f"lectures placed in sections: {len(used_videos)} of {len(registry)} known")


if __name__ == "__main__":
    build()
