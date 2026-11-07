---
title: Manuscript status
status: living
updated: "2026-11-07"
---

# Manuscript status — THE 12-MONTH BODYBUILDER

**GitHub home (canonical):** https://github.com/daelum/book  
**Branch (working):** `cursor/manuscript-home-17d4`  
**Context mirror:** `/cursor/stores/self/book/` + `/cursor/stores/self/docs/manuscript-status.md`  
**Voice:** `docs/author-voice.md` in Project store (Daelum mentality; not named repeatedly in prose)  
**Attribution:** YouTube creators/channels never named in manuscript; provenance in research DB + `book/maps/chapter-sources.json` only.

## Layout in repo

```
book/outline/00-complete-outline.md
book/chapters/ch-NN-slug.md
book/maps/chapter-sources.json
docs/manuscript-status.md
README.md
```

## Drafted

### Outline
- `book/outline/00-complete-outline.md` — Parts 1–5, pathways A–D, provisional 12-month roadmap, chapter IDs

### Part One — Understanding Your Body (`status: draft`) — synced from store
| File | Chapter |
|------|---------|
| `book/chapters/ch-01-what-bodybuilding-involves.md` | What Bodybuilding Actually Involves |
| `book/chapters/ch-02-how-muscle-grows.md` | How Muscle Grows |
| `book/chapters/ch-03-body-fat.md` | Body Fat |
| `book/chapters/ch-04-recomposition.md` | Recomposition |
| `book/chapters/ch-05-realistic-expectations.md` | Realistic Expectations |
| `book/chapters/ch-06-measuring-your-starting-point.md` | Measuring Your Starting Point |

### Part Two — in progress
| File | Chapter | Source |
|------|---------|--------|
| `book/chapters/ch-07-nutrition-fundamentals.md` | Nutrition Fundamentals | synced from store |
| `book/chapters/ch-08-protein-calories-macros.md` | Protein, Calories, and Macros | drafted in repo |
| `book/chapters/ch-09-resistance-training-fundamentals.md` | Resistance Training Fundamentals | drafted in repo |
| `book/chapters/ch-10-progressive-overload.md` | Progressive Overload | drafted in repo |
| `ch-11` … `ch-15` | Programme, form/effort, recovery, cardio/NEAT, habits | queued / drafting |

All drafted chapters use the standard scaffold (WHAT YOU NEED TO KNOW → … → WHAT’S NEXT) and pathway A–D notes where relevant.

## Research grounding used

- Coverage snapshot: 18 channels catalogued; **242** insight rows in store `research/insights/*.jsonl`. See store `youtube/logs/coverage-report.md`.
- Insights are largely transcript-backed excerpts (many evidence class D/E). Prose synthesizes themes in book voice; does **not** quote-attribute creators.
- Themes pulled into Part One/Two drafts: proximity to failure; volume/frequency by training age; track reps to detect plateaus; photos/measurements + weight; calories+protein tracking pair; protein ~g/lb heuristic; ego aborting bulks early; hardgainer patience; short layoffs ≠ total loss; NEAT with surplus; lifestyle adherence.

## What’s next (writing)

1. Finish Part Two: `ch-11` through `ch-15`  
2. Part Three month chapters once weekly templates firm up from research  
3. Part Four only as educational harm-reduction (no beginner drug protocols)

## Research gaps to fill later `[RESEARCH: …]`

Keep these **out of reader chapter body** until verified; listed here for Stage 3–4 workers:

- `[RESEARCH: hypertrophy set-volume dose-response meta numbers for beginners vs intermediates — cite verified papers]`
- `[RESEARCH: protein meta target bands g/kg lean mass vs total BW — bib entries]`
- `[RESEARCH: realistic natural monthly muscle gain ranges by training age / sex — transformations insights still thin/noisy]`
- `[RESEARCH: recomposition evidence conditions (novice, overweight, returnee) — literature + cleaned insights]`
- `[RESEARCH: waist/photo protocol reliability; best minimal tracking stack]`
- `[RESEARCH: NEAT compensation ranges in surplus/deficit — tighten ch-07/ch-14 figures]`
- `[RESEARCH: GLP-1 / retatrutide muscle-preservation themes for Part Four only — do not bleed protocols into Part One action plans]`
- `[RESEARCH: clean/dedupe insight extractions — many rows are stuttery ASR segments; need Stage 4 claim verification]`
- `[RESEARCH: priority transcript backlog — coverage report shows gaps on several catalogued channels]`

## Sync log

- 2026-11-07: Synced store outline + ch-01…ch-07 + maps + status into `daelum/book` on `cursor/manuscript-home-17d4`. Repo continues Part Two (ch-08+). Mirror key finished files back to store after pushes.
