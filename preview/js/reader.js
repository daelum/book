/**
 * THE 12-MONTH BODYBUILDER — static chapter reader
 * Loads preview/chapters/manifest.json (built by scripts/build-manifest.mjs)
 * and renders markdown with marked.
 */
(function () {
  const MANIFEST_URL = "./chapters/manifest.json";

  const els = {
    cover: document.getElementById("cover"),
    reader: document.getElementById("reader"),
    toc: document.getElementById("toc"),
    article: document.getElementById("article"),
    articlePart: document.getElementById("article-part"),
    articleTitle: document.getElementById("article-title"),
    prose: document.getElementById("prose"),
    sideNav: document.getElementById("side-nav-list"),
    chapterNav: document.getElementById("chapter-nav"),
    status: document.getElementById("status"),
  };

  let manifest = null;
  let readingOrder = [];

  function parseFrontmatter(raw) {
    const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
    if (!match) return { meta: {}, body: raw };
    const meta = {};
    for (const line of match[1].split(/\r?\n/)) {
      const m = line.match(/^([A-Za-z0-9_]+):\s*(.*)$/);
      if (!m) continue;
      let value = m[2].trim();
      if (
        (value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))
      ) {
        value = value.slice(1, -1);
      }
      meta[m[1]] = value;
    }
    return { meta, body: raw.slice(match[0].length) };
  }

  function route() {
    const hash = location.hash.replace(/^#\/?/, "");
    if (!hash || hash === "contents") {
      showCover();
      return;
    }
    openChapter(decodeURIComponent(hash));
  }

  function showCover() {
    els.cover.classList.add("is-active");
    els.reader.classList.remove("is-active");
    document.title = "THE 12-MONTH BODYBUILDER";
    window.scrollTo(0, 0);
  }

  function chapterNumber(ch) {
    if (ch.outline) return "○";
    if (typeof ch.order === "number" && ch.order > 0) {
      return String(ch.order).padStart(2, "0");
    }
    return "·";
  }

  function renderToc() {
    const parts = new Map();
    for (const ch of readingOrder) {
      const key = ch.outline
        ? "__outline__"
        : `part-${ch.part ?? "x"}-${ch.part_title || "Chapters"}`;
      if (!parts.has(key)) {
        parts.set(key, {
          label: ch.outline
            ? "Front matter"
            : ch.part
              ? `Part ${ch.part} — ${ch.part_title || ""}`
              : "Chapters",
          items: [],
        });
      }
      parts.get(key).items.push(ch);
    }

    const frag = document.createDocumentFragment();
    for (const part of parts.values()) {
      const block = document.createElement("div");
      block.className = "part-block";
      const h = document.createElement("h3");
      h.className = "part-label";
      h.textContent = part.label;
      block.appendChild(h);

      const ul = document.createElement("ul");
      ul.className = "toc-list";
      for (const ch of part.items) {
        const li = document.createElement("li");
        li.className = "toc-item" + (ch.outline ? " is-outline" : "");
        li.innerHTML = `
          <a href="#/${encodeURIComponent(ch.slug)}">
            <span class="toc-num">${chapterNumber(ch)}</span>
            <span class="toc-title">${escapeHtml(ch.title)}</span>
            <span class="toc-meta">${escapeHtml(ch.status || "")}</span>
          </a>`;
        ul.appendChild(li);
      }
      block.appendChild(ul);
      frag.appendChild(block);
    }
    els.toc.replaceChildren(frag);
  }

  function renderSideNav(currentSlug) {
    const frag = document.createDocumentFragment();
    for (const ch of readingOrder) {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = `#/${encodeURIComponent(ch.slug)}`;
      a.textContent = ch.outline ? ch.title : `${chapterNumber(ch)}. ${ch.title}`;
      if (ch.slug === currentSlug) a.classList.add("is-current");
      li.appendChild(a);
      frag.appendChild(li);
    }
    els.sideNav.replaceChildren(frag);
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  async function openChapter(slug) {
    const ch = readingOrder.find((c) => c.slug === slug);
    if (!ch) {
      els.status.textContent = `Chapter not found: ${slug}`;
      showCover();
      return;
    }

    els.cover.classList.remove("is-active");
    els.reader.classList.add("is-active");
    els.status.textContent = "Loading…";
    els.prose.innerHTML = "";

    try {
      const res = await fetch(`./chapters/${encodeURIComponent(ch.file)}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const raw = await res.text();
      const { meta, body } = parseFrontmatter(raw);
      const title = meta.title || ch.title;
      const partLine =
        ch.outline
          ? "Outline"
          : ch.part
            ? `Part ${ch.part}${ch.part_title ? ` — ${ch.part_title}` : ""}`
            : "";

      els.articlePart.textContent = partLine;
      els.articleTitle.textContent = title;
      document.title = `${title} · THE 12-MONTH BODYBUILDER`;

      if (window.marked) {
        marked.setOptions({ gfm: true, breaks: false });
        els.prose.innerHTML = marked.parse(body);
      } else {
        els.prose.innerHTML = `<pre>${escapeHtml(body)}</pre>`;
      }

      renderSideNav(slug);
      renderChapterNav(slug);
      els.status.textContent = ch.status ? `Status: ${ch.status}` : "";
      window.scrollTo(0, 0);
    } catch (err) {
      els.status.textContent = "";
      els.prose.innerHTML = `<div class="error-box">Couldn’t load this chapter. ${escapeHtml(
        err.message || String(err)
      )}</div>`;
    }
  }

  function renderChapterNav(slug) {
    const idx = readingOrder.findIndex((c) => c.slug === slug);
    const prev = idx > 0 ? readingOrder[idx - 1] : null;
    const next = idx >= 0 && idx < readingOrder.length - 1 ? readingOrder[idx + 1] : null;

    let html = "";
    if (prev) {
      html += `<a class="prev" href="#/${encodeURIComponent(prev.slug)}"><span class="label">Previous</span>${escapeHtml(
        prev.title
      )}</a>`;
    } else {
      html += `<span></span>`;
    }
    if (next) {
      html += `<a class="next" href="#/${encodeURIComponent(next.slug)}"><span class="label">Next</span>${escapeHtml(
        next.title
      )}</a>`;
    }
    els.chapterNav.innerHTML = html;
  }

  async function discoverChaptersFallback() {
    // If manifest is missing, try a small hardcoded probe of known filenames —
    // kept empty intentionally; manifest is the source of truth for discovery.
    return { title: "THE 12-MONTH BODYBUILDER", chapters: [] };
  }

  async function init() {
    try {
      const res = await fetch(MANIFEST_URL, { cache: "no-store" });
      if (!res.ok) throw new Error(`manifest ${res.status}`);
      manifest = await res.json();
    } catch (err) {
      console.warn("manifest load failed", err);
      manifest = await discoverChaptersFallback();
      els.status.textContent =
        "Chapter list missing — run node preview/scripts/build-manifest.mjs";
    }

    readingOrder = Array.isArray(manifest.chapters) ? manifest.chapters : [];
    renderToc();

    const firstChapter = readingOrder.find((c) => !c.outline) || readingOrder[0];
    const startBtn = document.getElementById("start-reading");
    if (startBtn && firstChapter) {
      startBtn.href = `#/${encodeURIComponent(firstChapter.slug)}`;
    }

    window.addEventListener("hashchange", route);
    route();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
