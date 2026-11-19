#!/usr/bin/env python3
"""For verified papers without a local PDF, look for an arXiv preprint with the same title
(arXiv API, title search) and download it. Writes research/arxiv_hits.json."""
import csv, json, re, sys, time, urllib.parse, urllib.request, difflib, os
import xml.etree.ElementTree as ET

here = os.path.dirname(os.path.abspath(__file__))
pdf_dir = os.path.join(os.path.dirname(here), "downloads", "papers")
rows = list(csv.DictReader(open(os.path.join(here, "papers.csv"), encoding="utf-8", newline="")))
norm = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
NS = {"a": "http://www.w3.org/2005/Atom"}
hits = {}
for r in rows:
    if r["local_pdf"] or not r["year"].isdigit() or int(r["year"]) < 1993:
        continue
    title = re.sub(r"<[^>]+>", "", r["title"])
    q = 'ti:"%s"' % title.replace('"', " ").replace("\\", " ")[:200]
    url = "http://export.arxiv.org/api/query?max_results=5&search_query=" + urllib.parse.quote(q)
    try:
        xml = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "course-builder/1.0"}), timeout=40).read()
        root = ET.fromstring(xml)
    except Exception as e:
        print(r["key"], "query failed", e, flush=True); time.sleep(3); continue
    best = None
    for e in root.findall("a:entry", NS):
        t = " ".join(e.find("a:title", NS).text.split())
        ratio = difflib.SequenceMatcher(None, norm(t), norm(title)).ratio()
        authors = " ".join(a.find("a:name", NS).text for a in e.findall("a:author", NS)).lower()
        first = norm(r["authors"].split(";")[0]).split(" ")[0]
        if ratio >= 0.92 and first and first in norm(authors):
            best = (e.find("a:id", NS).text.strip(), t, ratio); break
    if best:
        aid = best[0].rsplit("/abs/", 1)[-1]
        aid = re.sub(r"v\d+$", "", aid)
        slug = "_".join(norm(title).split()[:3])
        fn = f"{r['key']}_{slug}_arxiv.pdf"
        dest = os.path.join(pdf_dir, fn)
        ok = False
        try:
            data = urllib.request.urlopen(urllib.request.Request("https://arxiv.org/pdf/" + aid, headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read()
            if data[:4] == b"%PDF" and len(data) > 50000:
                open(dest, "wb").write(data); ok = True
        except Exception as e:
            print(r["key"], "download failed", e, flush=True)
        hits[r["key"]] = {"arxiv": aid, "abs": "https://arxiv.org/abs/" + aid, "title": best[1], "ratio": round(best[2], 3), "file": fn if ok else ""}
        print(r["key"], "HIT", aid, ok, flush=True)
    else:
        print(r["key"], "-", flush=True)
    json.dump(hits, open(os.path.join(here, "arxiv_hits.json"), "w", encoding="utf-8"), indent=1)
    time.sleep(3.2)
print("done", len(hits))
