#!/usr/bin/env node
/**
 * Scans preview/chapters/*.md, parses YAML frontmatter, writes manifest.json.
 * Run after adding or updating chapter files:
 *   node preview/scripts/build-manifest.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const chaptersDir = path.resolve(__dirname, "../chapters");
const outPath = path.join(chaptersDir, "manifest.json");

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
    if (value.startsWith("[") && value.endsWith("]")) {
      value = value
        .slice(1, -1)
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);
    } else if (/^\d+$/.test(value)) {
      value = Number(value);
    }
    meta[m[1]] = value;
  }
  return { meta, body: raw.slice(match[0].length) };
}

function slugFromFilename(name) {
  return name.replace(/\.md$/i, "");
}

function isOutline(meta, file) {
  if (meta.chapter_id) return false;
  if (/outline/i.test(file) || /outline/i.test(String(meta.title || ""))) return true;
  return !meta.order && !/^ch-/i.test(file);
}

const files = fs
  .readdirSync(chaptersDir)
  .filter((f) => f.endsWith(".md"))
  .sort((a, b) => a.localeCompare(b, "en"));

const entries = files.map((file) => {
  const raw = fs.readFileSync(path.join(chaptersDir, file), "utf8");
  const { meta } = parseFrontmatter(raw);
  const slug = meta.chapter_id || slugFromFilename(file);
  const outline = isOutline(meta, file);
  return {
    file,
    slug,
    title: meta.title || slug,
    part: meta.part ?? null,
    part_title: meta.part_title || null,
    order: typeof meta.order === "number" ? meta.order : outline ? 0 : 999,
    status: meta.status || "draft",
    outline,
  };
});

entries.sort((a, b) => {
  if (a.outline !== b.outline) return a.outline ? -1 : 1;
  if (a.order !== b.order) return a.order - b.order;
  return a.file.localeCompare(b.file, "en");
});

const manifest = {
  title: "THE 12-MONTH BODYBUILDER",
  generated: new Date().toISOString().slice(0, 10),
  chapters: entries,
};

fs.writeFileSync(outPath, JSON.stringify(manifest, null, 2) + "\n");
console.log(`Wrote ${entries.length} entries → ${path.relative(process.cwd(), outPath)}`);
