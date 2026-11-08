#!/usr/bin/env python3
"""Build a self-contained HTML ebook from STRIPLINE manuscript stages."""
from __future__ import annotations

import html
import re
from datetime import date
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
STORE = Path("/cursor/stores/self/book")
CHAPTER_DIRS = [
    STORE / "chapters",
    ROOT / "book" / "chapters",
]
OUTLINE_CANDIDATES = [
    STORE / "outline" / "00-complete-outline.md",
    ROOT / "book" / "outline" / "00-complete-outline.md",
]
OUT = ROOT / "ebook" / "the-12-month-body.html"
# Title locked 2026-11-08
BOOK_TITLE = "The 12-Month Body"
BOOK_SUBTITLE = "The STRIPLINE Method"
LEDE = (
    "In twelve months you’ll change how you look by stripping fat first, "
    "locking one plan, and building under accountability — The STRIPLINE Method."
)


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
        elif value in ("true", "false"):
            value = value == "true"
        elif re.fullmatch(r"\d+", value):
            value = int(value)
        meta[key] = value
    return meta, raw[m.end() :]


def chapter_dir() -> Path:
    for d in CHAPTER_DIRS:
        if not d.is_dir():
            continue
        stages = list(d.glob("stage-*.md")) + list(d.glob("appendix-*.md"))
        if stages:
            return d
    raise SystemExit("No stage/appendix chapter directory found")


def load_outline() -> Path | None:
    for p in OUTLINE_CANDIDATES:
        if p.is_file() and "legacy" not in str(p):
            return p
    return None


def order_key(path: Path, meta: dict) -> int:
    if "order" in meta and isinstance(meta["order"], int):
        return meta["order"]
    m = re.match(r"(?:stage|appendix)-(\d+)", path.name)
    if m:
        return int(m.group(1))
    if path.name.startswith("appendix"):
        return 90
    return 999


def collect_chapters() -> list[dict]:
    d = chapter_dir()
    files = sorted(set(d.glob("stage-*.md")) | set(d.glob("appendix-*.md")))
    entries = []
    for path in files:
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        title = meta.get("title") or path.stem
        slug = meta.get("stage_id") or meta.get("id") or path.stem
        part_title = meta.get("part_title") or (
            "Ebook Appendix" if "appendix" in path.name else "Stage"
        )
        stage = meta.get("stage", part_title)
        entries.append(
            {
                "order": order_key(path, meta),
                "title": title,
                "stage": stage,
                "part_title": part_title,
                "slug": slug,
                "body": body,
                "file": path.name,
                "mtime": path.stat().st_mtime,
                "ebook_only": bool(meta.get("ebook_only")) or path.name.startswith("appendix"),
            }
        )
    entries.sort(key=lambda e: e["order"])
    return entries


def md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["extra", "sane_lists", "tables", "smarty"],
        output_format="html5",
    )


CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,600;0,9..40,700;1,9..40,400&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');
:root {
  --bg: #e8ece8;
  --paper: #fbfaf7;
  --ink: #1a1f1c;
  --muted: #5c6560;
  --accent: #1f4d3a;
  --accent-2: #2f6b4f;
  --rule: #c5cad3;
  --warm: #c45c26;
  --font-brand: "Fraunces", Georgia, "Times New Roman", serif;
  --font-display: "Fraunces", Georgia, serif;
  --font-body: "DM Sans", system-ui, sans-serif;
  --font-ui: "DM Sans", system-ui, sans-serif;
  --measure: 40rem;
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
    radial-gradient(90% 60% at 100% 0%, rgba(31,77,58,.10), transparent 55%),
    radial-gradient(70% 50% at 0% 100%, rgba(196,92,38,.06), transparent 50%),
    linear-gradient(180deg, var(--bg), #c5cad3);
}
a { color: var(--accent); text-underline-offset: .15em; }
a:hover { color: var(--warm); }
.wrap { max-width: 48rem; margin: 0 auto; padding: 1.25rem clamp(1rem,3vw,2rem) 4rem; }
.cover {
  background: var(--paper);
  border: 1px solid var(--rule);
  padding: clamp(2rem,6vw,3.5rem) clamp(1.25rem,4vw,2.5rem);
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}
.cover::before {
  content: "";
  position: absolute;
  inset: 0 auto 0 0;
  width: 6px;
  background: linear-gradient(180deg, var(--accent), var(--warm));
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
  font-size: clamp(2.4rem, 9vw, 4.4rem);
  line-height: 1.02;
  letter-spacing: -0.01em;
  margin: 0 0 1rem;
  max-width: 16ch;
  color: var(--accent);
}
.lede {
  font-family: var(--font-body);
  font-size: 1.15rem;
  line-height: 1.5;
  color: #3a433e;
  max-width: 36rem;
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
  font-size: 1.15rem;
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
  max-width: 22ch;
  color: var(--ink);
}
.prose { max-width: var(--measure); }
.prose > :first-child { margin-top: 0; }
.prose h1 { display: none; }
.prose h2 {
  font-family: var(--font-ui);
  font-size: .78rem;
  letter-spacing: .12em;
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
  padding: .85rem 1rem;
  border-left: 3px solid var(--accent);
  background: rgba(31,77,58,.05);
  color: #3a433e;
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
.prose th { background: rgba(31,77,58,.08); font-family: var(--font-ui); font-size: .8rem; }
.callout {
  border: 1px solid var(--rule);
  background: rgba(31,77,58,.06);
  padding: 1rem 1.1rem;
  margin: 1.25rem 0;
}
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
@media (max-width: 640px) {
  body { font-size: 1.05rem; }
  .brand { max-width: 14ch; }
}
@media print {
  body { background: #fff; font-size: 11pt; }
  .chapter, .cover, .toc { border: none; box-shadow: none; break-inside: avoid; }
  .chapter { break-before: page; }
  .cover { break-after: page; }
  .back-toc { display: none; }
  a { color: inherit; text-decoration: none; }
}
"""


def build() -> Path:
    chapters = collect_chapters()
    if not chapters:
        raise SystemExit("No stages found to build")

    # Reader outline: skip legacy drafting docs; prefer short outline if present
    outline_path = load_outline()
    outline_html = ""
    outline_toc = ""
    if outline_path:
        raw = outline_path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        # Skip if outline still contains internal drafting leakage
        if "Drafting status" in body or "Attribution reminder" in body:
            outline_path = None
        else:
            outline_html = f"""
<section class="chapter" id="outline">
  <p class="chapter-part">Front matter</p>
  <h1>{html.escape(meta.get('title') or 'How to use this book')}</h1>
  <div class="prose">{md_to_html(body)}</div>
  <p class="back-toc"><a href="#contents">↑ Contents</a></p>
</section>
"""
            outline_toc = (
                '<p class="part">Front matter</p><ol>'
                f'<li><a href="#outline"><span class="n">○</span>'
                f"<span>{html.escape(meta.get('title') or 'How to use this book')}</span></a></li>"
                "</ol>"
            )

    toc_parts: list[str] = []
    if outline_toc:
        toc_parts.append(outline_toc)

    body_parts: list[str] = []
    if outline_html:
        body_parts.append(outline_html)

    current_part = None
    open_ol = False
    for ch in chapters:
        if ch["part_title"] != current_part:
            if open_ol:
                toc_parts.append("</ol>")
                open_ol = False
            current_part = ch["part_title"]
            toc_parts.append(f'<p class="part">{html.escape(str(current_part))}</p>')
            toc_parts.append("<ol>")
            open_ol = True
        n = "A" if ch["ebook_only"] else f"{ch['order']:02d}"
        toc_parts.append(
            f'<li><a href="#{html.escape(ch["slug"])}">'
            f'<span class="n">{n}</span>'
            f'<span>{html.escape(ch["title"])}</span></a></li>'
        )
        part_line = str(ch["part_title"])
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

    stage_count = sum(1 for c in chapters if not c["ebook_only"])
    appendix_count = sum(1 for c in chapters if c["ebook_only"])
    meta_line = f"{stage_count} stages"
    if appendix_count:
        meta_line += f" + {appendix_count} appendix"
    meta_line += f" · generated {date.today().isoformat()} · The STRIPLINE Method · save this file to read offline"

    doc = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html.escape(BOOK_TITLE)}</title>
<meta name="description" content="{html.escape(LEDE)}"/>
<style>
{CSS}
</style>
</head>
<body>
<div class="wrap">
  <header class="cover" id="cover">
    <p class="kicker">{html.escape(BOOK_SUBTITLE)} · HTML ebook</p>
    <h1 class="brand">{html.escape(BOOK_TITLE)}</h1>
    <p class="lede">{html.escape(LEDE)}</p>
    <p class="meta">{html.escape(meta_line)}</p>
  </header>

  <nav class="toc" id="contents" aria-label="Table of contents">
    <h2>Contents</h2>
    {''.join(toc_parts)}
  </nav>

  {''.join(body_parts)}

  <p class="footer">{html.escape(BOOK_TITLE)} · {html.escape(BOOK_SUBTITLE)} · {meta_line.split('·')[0].strip()}</p>
</div>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, {len(chapters)} sections)")
    return OUT


if __name__ == "__main__":
    build()
