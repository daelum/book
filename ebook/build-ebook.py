#!/usr/bin/env python3
"""Build a self-contained HTML ebook from manuscript markdown chapters."""
from __future__ import annotations

import html
import re
from datetime import date
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
STORE = Path("/cursor/stores/self/book")
# Prefer live store; fall back to repo mirrors.
CHAPTER_DIRS = [
    STORE / "chapters",
    ROOT / "book" / "chapters",
    ROOT / "preview" / "chapters",
]
OUTLINE_CANDIDATES = [
    STORE / "outline" / "00-complete-outline.md",
    ROOT / "book" / "outline" / "00-complete-outline.md",
    ROOT / "preview" / "chapters" / "00-complete-outline.md",
]
OUT = ROOT / "ebook" / "the-12-month-bodybuilder.html"

PART_TITLES = {
    1: "Understanding Your Body",
    2: "Building Your Foundation",
    3: "Your 12-Month Roadmap",
    4: "Supplements & Advanced Tools Literacy",
    5: "Identity, Longevity, After Month Twelve",
}


def parse_frontmatter(raw: str) -> tuple[dict, str]:
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", raw, re.S)
    if not m:
        return {}, raw
    meta: dict = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if not km:
            continue
        key, value = km.group(1), km.group(2).strip()
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        elif value.startswith("[") and value.endswith("]"):
            value = [s.strip() for s in value[1:-1].split(",") if s.strip()]
        elif re.fullmatch(r"\d+", value):
            value = int(value)
        meta[key] = value
    return meta, raw[m.end() :]


def chapter_dir() -> Path:
    for d in CHAPTER_DIRS:
        if d.is_dir() and list(d.glob("ch-*.md")):
            return d
    raise SystemExit("No chapter directory found")


def load_outline() -> Path | None:
    for p in OUTLINE_CANDIDATES:
        if p.is_file():
            return p
    return None


def order_from_name(name: str) -> int:
    m = re.match(r"ch-(\d+)", name)
    return int(m.group(1)) if m else 999


def collect_chapters() -> list[dict]:
    d = chapter_dir()
    files = sorted(d.glob("ch-*.md"), key=lambda p: order_from_name(p.name))
    # Prefer canonical neat over neats duplicate
    by_order: dict[int, Path] = {}
    for f in files:
        order = order_from_name(f.name)
        if order == 14 and "neats" in f.name and (d / "ch-14-cardio-steps-neat.md").exists():
            continue
        prev = by_order.get(order)
        if prev is None or f.stat().st_size >= prev.stat().st_size:
            by_order[order] = f
    entries = []
    for order in sorted(by_order):
        path = by_order[order]
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        title = meta.get("title") or path.stem
        part = meta.get("part")
        part_title = meta.get("part_title") or PART_TITLES.get(part)
        slug = meta.get("chapter_id") or meta.get("id") or path.stem
        entries.append(
            {
                "order": order,
                "title": title,
                "part": part,
                "part_title": part_title,
                "slug": slug,
                "body": body,
                "file": path.name,
                "mtime": path.stat().st_mtime,
            }
        )
    return entries


def md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["extra", "sane_lists", "tables", "smarty"],
        output_format="html5",
    )


CSS = """
:root {
  --bg: #e4e7ec;
  --paper: #f7f6f3;
  --ink: #16191e;
  --muted: #5a6270;
  --accent: #1a473c;
  --rule: #c5cad3;
  --font-brand: "Bebas Neue", "Arial Narrow", Impact, sans-serif;
  --font-display: Georgia, "Iowan Old Style", "Palatino Linotype", Palatino, serif;
  --font-body: Georgia, "Iowan Old Style", "Palatino Linotype", Palatino, serif;
  --font-ui: system-ui, -apple-system, "Segoe UI", sans-serif;
  --measure: 38rem;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 1.125rem;
  line-height: 1.7;
  background:
    radial-gradient(100% 70% at 0% 0%, rgba(26,71,60,.12), transparent 50%),
    linear-gradient(180deg, var(--bg), # rec5cad3);
}
a { color: var(--accent); text-underline-offset: .15em; }
a:hover { color: #8f2f22; }
.wrap { max-width: 48rem; margin: 0 auto; padding: 1.25rem clamp(1rem,3vw,2rem) 4rem; }
.cover {
  background: var(--paper);
  border: 1px solid var(--rule);
  padding: clamp(2rem,6vw,3.5rem) clamp(1.25rem,4vw,2.5rem);
  margin-bottom: 2rem;
}
.kicker {
  font-family: var(--font-ui);
  font-size: .75rem;
  letter-spacing: .16em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0 0 1rem;
}
.brand {
  font-family: var(--font-brand);
  font-size: clamp(2.8rem, 10vw, 5.5rem);
  line-height: .92;
  letter-spacing: .02em;
  margin: 0 0 1rem;
  max-width: 12ch;
}
.lede {
  font-family: var(--font-display);
  font-size: 1.2rem;
  line-height: 1.45;
  color: #3d4450;
  max-width: 34rem;
  margin: 0 0 1.25rem;
}
.meta {
  font-family: var(--font-ui);
  font-size: .85rem;
  color: var(--muted);
}
.toc {
  background: var(--paper);
  border: 1px solid var(--rule);
  padding: clamp(1.25rem,3vw,2rem);
  margin-bottom: 2.5rem;
}
.toc h2 {
  font-family: var(--font-ui);
  font-size: .75rem;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0 0 1rem;
  padding-bottom: .75rem;
  border-bottom: 1px solid var(--rule);
}
.toc .part {
  font-family: var(--font-display);
  font-size: 1.05rem;
  color: var(--accent);
  margin: 1.25rem 0 .5rem;
}
.toc ol { list-style: none; margin: 0; padding: 0; }
.toc li { border-bottom: 1px solid rgba(197,202,211,.7); }
.toc a {
  display: grid;
  grid-template-columns: 2.5rem 1fr;
  gap: .75rem;
  padding: .7rem 0;
  text-decoration: none;
  color: inherit;
}
.toc a:hover { color: var(--accent); }
.toc .n {
  font-family: var(--font-brand);
  font-size: 1.2rem;
  color: var(--muted);
}
.chapter {
  background: var(--paper);
  border: 1px solid var(--rule);
  padding: clamp(1.5rem,4vw,2.75rem) clamp(1.15rem,4vw,2.5rem);
  margin-bottom: 1.75rem;
}
.chapter-part {
  font-family: var(--font-ui);
  font-size: .72rem;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0 0 .4rem;
}
.chapter > h1 {
  font-family: var(--font-display);
  font-size: clamp(1.7rem, 4vw, 2.35rem);
  line-height: 1.15;
  margin: 0 0 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--rule);
  max-width: 18ch;
}
.prose { max-width: var(--measure); }
.prose > :first-child { margin-top: 0; }
.prose h1 { display: none; }
.prose h2 {
  font-family: var(--font-ui);
  font-size: .8rem;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 2.2rem 0 .75rem;
}
.prose h3 {
  font-family: var(--font-display);
  font-size: 1.2rem;
  margin: 1.6rem 0 .5rem;
}
.prose p { margin: 0 0 1.05rem; }
.prose ul, .prose ol { margin: 0 0 1.1rem; padding-left: 1.2rem; }
.prose li { margin: .3rem 0; }
.prose hr { border: 0; border-top: 1px solid var(--rule); margin: 1.75rem 0; }
.prose blockquote {
  margin: 1.25rem 0;
  padding-left: 1rem;
  border-left: 3px solid var(--accent);
  color: #3d4450;
  font-style: italic;
}
.prose table {
  width: 100%;
  border-collapse: collapse;
  font-size: .95rem;
  margin: 0 0 1.25rem;
  display: block;
  overflow-x: auto;
}
.prose th, .prose td {
  border: 1px solid var(--rule);
  padding: .45rem .6rem;
  text-align: left;
  vertical-align: top;
}
.prose th { background: rgba(26,71,60,.08); font-family: var(--font-ui); font-size: .8rem; }
.back-toc {
  font-family: var(--font-ui);
  font-size: .85rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--rule);
}
.footer {
  font-family: var(--font-ui);
  font-size: .8rem;
  color: var(--muted);
  text-align: center;
  padding: 1rem 0 2rem;
}
@media print {
  body { background: #fff; font-size: 11pt; }
  .chapter, .cover, .toc { border: none; box-shadow: none; page-break-inside: avoid; }
  .chapter { page-break-before: always; }
  .cover { page-break-after: always; }
  .back-toc { display: none; }
}
"""


def build() -> Path:
    chapters = collect_chapters()
    outline_path = load_outline()
    outline_html = ""
    outline_toc = ""
    if outline_path:
        raw = outline_path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        outline_html = f"""
<section class="chapter" id="outline">
  <p class="chapter-part">Front matter</p>
  <h1>{html.escape(meta.get('title') or 'Complete Outline')}</h1>
  <div class="prose">{md_to_html(body)}</div>
  <p class="back-toc"><a href="#contents">↑ Contents</a></p>
</section>
"""
        outline_toc = (
            '<p class="part">Front matter</p><ol>'
            f'<li><a href="#outline"><span class="n">○</span>'
            f"<span>{html.escape(meta.get('title') or 'Complete Outline')}</span></a></li>"
            "</ol>"
        )

    toc_parts: list[str] = [outline_toc] if outline_toc else []
    body_parts: list[str] = [outline_html] if outline_html else []
    current_part = object()
    for ch in chapters:
        if ch["part"] != current_part:
            current_part = ch["part"]
            label = (
                f"Part {ch['part']} — {ch['part_title']}"
                if ch["part"] and ch["part_title"]
                else (f"Part {ch['part']}" if ch["part"] else "Chapters")
            )
            toc_parts.append(f'<p class="part">{html.escape(label)}</p><ol>')
            # close previous ol if needed — simpler: close after each part group
        # We'll rebuild TOC cleanly below

    # Clean TOC build
    toc_parts = []
    if outline_toc:
        toc_parts.append(outline_toc)
    current_part = None
    open_ol = False
    for ch in chapters:
        if ch["part"] != current_part:
            if open_ol:
                toc_parts.append("</ol>")
                open_ol = False
            current_part = ch["part"]
            label = (
                f"Part {ch['part']} — {ch['part_title']}"
                if ch["part"] and ch["part_title"]
                else (f"Part {ch['part']}" if ch["part"] else "Chapters")
            )
            toc_parts.append(f'<p class="part">{html.escape(str(label))}</p>')
            toc_parts.append("<ol>")
            open_ol = True
        toc_parts.append(
            f'<li><a href="#{html.escape(ch["slug"])}">'
            f'<span class="n">{ch["order"]:02d}</span>'
            f'<span>{html.escape(ch["title"])}</span></a></li>'
        )
        part_line = (
            f"Part {ch['part']} — {ch['part_title']}"
            if ch["part"] and ch["part_title"]
            else (f"Part {ch['part']}" if ch["part"] else "")
        )
        body_parts.append(
            f"""
<section class="chapter" id="{html.escape(ch['slug'])}">
  <p class="chapter-part">{html.escape(part_line)}</p>
  <h1>{html.escape(ch['title'])}</h1>
  <div class="prose">{md_to_html(ch['body'])}</div>
  <p class="back-toc"><a href="#contents">↑ Contents</a></p>
</section>
"""
        )
    if open_ol:
        toc_parts.append("</ol>")

    newest = max((c["mtime"] for c in chapters), default=0)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>THE 12-MONTH BODYBUILDER</title>
<meta name="description" content="A practical beginner transform guide — train, eat, recover, track, and decide what to ignore over twelve months."/>
<style>
{CSS}
</style>
</head>
<body>
<div class="wrap">
  <header class="cover" id="cover">
    <p class="kicker">Draft manuscript · HTML ebook</p>
    <h1 class="brand">THE 12-MONTH BODYBUILDER</h1>
    <p class="lede">Teach someone starting or restarting how to train, eat, recover, track, and decide what to ignore — so they can change their physique over twelve months with evidence-aware methods, not hype.</p>
    <p class="meta">{len(chapters)} chapters · generated {date.today().isoformat()} · open Contents below or save this file to read offline</p>
  </header>

  <nav class="toc" id="contents" aria-label="Table of contents">
    <h2>Contents</h2>
    {''.join(toc_parts)}
  </nav>

  {''.join(body_parts)}

  <p class="footer">THE 12-MONTH BODYBUILDER · draft ebook · {len(chapters)} chapters</p>
</div>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, {len(chapters)} chapters, newest_mtime={newest})")
    return OUT


if __name__ == "__main__":
    build()
