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
    return [r for r in rows if r.get("verified", "").lower() == "yes" and r.get("doi")]


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
    if p.get("oa_url"):
        oa = f' <a class="tag free" href="{E(p["oa_url"])}" target="_blank" rel="noopener">open access</a>'
    vol = p.get("volume")
    pages = p.get("pages")
    cite = E(p.get("journal"))
    if vol:
        cite += f" <b>{E(vol)}</b>"
    if pages:
        cite += f", {E(pages)}"
    return (
        f'<li class="res"><span class="res-auth">{E(p.get("authors"))} ({E(p.get("year"))}).</span> '
        f'<a href="https://doi.org/{E(p["doi"])}" target="_blank" rel="noopener">{E(p.get("title"))}</a>. '
        f'<i>{cite}</i>.{oa}</li>'
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
  <nav class="toplinks"><a href="library.html">Library</a><a href="formula-sheet.html">Formula sheet</a>
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
    order = {"index": 0, "projects": 1, "formula-sheet": 2, "library": 3}
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
    }

    allpages = mods + extras
    for m in allpages:
        raw = m["raw"]
        vt = [int(x) for x in re.findall(r"\d+", m.get("videos", ""))]
        pg = [x for x in re.findall(r"[A-M]", m.get("papers", ""))]
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
        for k, v in blocks.items():
            body = body.replace("<p>{{" + k + "}}</p>", v).replace("{{" + k + "}}", v)

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

    for f in ("style.css", "course.js"):
        shutil.copyfile(SRC / f, SITE / f)
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    print(f"built {len(allpages)} pages; videos={len(videos)} books={len(books['books'])} "
          f"notes={len(books['notes_courses'])} tutorials={len(books['tutorials_docs'])} papers={len(papers)}")


if __name__ == "__main__":
    build()
