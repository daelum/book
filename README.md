# THE 12-MONTH BODYBUILDER

Practical beginner transform guide — train, eat, recover, track, and decide what to ignore over twelve months.

## Manuscript

- Chapters: [`book/chapters/`](book/chapters/)
- Outline: [`book/outline/00-complete-outline.md`](book/outline/00-complete-outline.md)

## Web preview reader

A static long-form reader lives in [`preview/`](preview/).

### Read on GitHub (PR branch)

- Cover / reader: [`preview/index.html`](https://github.com/daelum/book/blob/cursor/book-preview-reader-390b/preview/index.html)
- Chapter 1: [`preview/chapters/ch-01-what-bodybuilding-involves.md`](https://github.com/daelum/book/blob/cursor/book-preview-reader-390b/preview/chapters/ch-01-what-bodybuilding-involves.md)
- All chapters: [`preview/chapters/`](https://github.com/daelum/book/tree/cursor/book-preview-reader-390b/preview/chapters)
- PR: https://github.com/daelum/book/pull/1

Agent how-to (always current): Project store `docs/book-preview.md`.

### Add a chapter

1. Drop a new `.md` file into `preview/chapters/` (and mirror under `book/chapters/`).
2. Regenerate the auto-discovery list:

```bash
node preview/scripts/build-manifest.mjs
```

The reader loads `preview/chapters/manifest.json` — new chapters appear in the table of contents after that step. No app rewrite required.

### GitHub Pages

In the repo **Settings → Pages**:

1. Source: **Deploy from a branch**
2. Branch: `main` (or this preview branch), folder: `/preview`  
   — or keep serving from root and open `/preview/`.

A workflow at [`.github/workflows/pages.yml`](.github/workflows/pages.yml) can publish the `preview/` folder automatically when enabled.
