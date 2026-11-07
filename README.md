# THE 12-MONTH BODYBUILDER

Practical beginner transform guide — train, eat, recover, track, and decide what to ignore over twelve months.

## Manuscript

- Chapters: [`book/chapters/`](book/chapters/)
- Outline: [`book/outline/00-complete-outline.md`](book/outline/00-complete-outline.md)

## Web preview reader

A static long-form reader lives in [`preview/`](preview/).

### Open locally

```bash
cd preview
python3 -m http.server 8765 --bind 127.0.0.1
```

Then open [http://127.0.0.1:8765/](http://127.0.0.1:8765/).

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
