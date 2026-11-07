---
title: Research validation — Stage 5 gap fill
status: living
updated: "2026-11-07"
stage: 5
verifier: stage5-research-validation-agent
---

# Research validation — THE 12-MONTH BODYBUILDER

Independent literature pass against manuscript research gaps. Identifiers were resolved via PubMed / Crossref / manufacturer pages on **2026-11-07**. No DOIs, PMIDs, or statistics were invented. PED / peptide / GLP-1 material stays **educational harm-reduction** (no beginner protocols, no titration).

**Registers updated:** `/cursor/stores/self/bibliography/sources.jsonl` (21 entries) · `/cursor/stores/self/claims/register.jsonl` (13 claims) · `/cursor/stores/self/claims/verification-log.jsonl`

**Internal edit stubs (for writing worker):** `/cursor/stores/self/internal/stage5-manuscript-edit-stubs.md`

## Verdict

Part Two protein / volume / progressive-overload framing is **directionally solid** and now has verified bibliography anchors. Part Four tone (literacy, not protocols) is **appropriate**; creatine, AAS CV/endocrine risk themes, GLP-1 weight + lean-mass caveats, and “retatrutide still investigational” are **supported**. Still thin: full peptide class map beyond BPC-157 exemplars, vitamin D / fish-oil Tier-1 hardening, oral-AAS hepatotoxicity primary papers, and provisional ch-17–20 templates.

---

## What’s verified

| Topic | Manuscript claim (plain) | Status | Evidence | Key bib / claim IDs |
|-------|--------------------------|--------|----------|---------------------|
| Creatine Tier 1 | Best-studied; daily use; loading optional; safety in healthy users | **Supported** | A | `bib_06b671ef36` (Kreider ISSN 2017, PMID 28615996) · `bib_0ad83801ce` (Antonio 2021, PMID 33557850) · `clm_35b78a69d71c` |
| Protein 1.6–2.2 g/kg | Practical Year-1 target; higher end useful in deficit | **Supported** (with nuance) | A | `bib_9914827c24` Morton 2018 (~1.62 g/kg breakpoint, PMID 28698222) · `bib_e498488c33` ISSN protein · `bib_381074aa0f` Helms 2014 (higher **per FFM** in lean deficit) · `clm_ed1a9a266269` |
| Protein powder vs food | Convenience tool; food can meet needs | **Supported** | B | Morton meta (source not primary driver) · ISSN · Antonio 2024 misconceptions `bib_79cbcc75ff` · `clm_808a8b7a439d` |
| Caffeine Tier 1 | Performance aid; mind sleep | **Supported** | A | Guest ISSN 2021 `bib_deb598f2ee` (PMID 33388079) · `clm_b8f879e58769` |
| Progressive overload | Necessary for ongoing hypertrophy | **Supported** | A | Schoenfeld 2010 `bib_6440ad37dd` · volume meta · `clm_b8025c3f5588` |
| ~2×/week per muscle | Practical sweet spot | **Supported** | A | Schoenfeld frequency meta 2016 `bib_beac110f7f` (PMID 27102172) · `clm_a18689f43d1b` |
| Volume dose-response | Modest beginner volume OK; more helps up to recovery | **Supported** | A | Schoenfeld volume meta 2017 `bib_53ed4f6180` · umbrella 2022 `bib_d7651b3639` · `clm_8ce28de51045` |
| AAS CV risk | Heart / lipids / plaque themes | **Educational only** | B | Baggish 2017 Circulation `bib_c8b4eccf53` (PMID 28533317) · `clm_98a0b3336188` |
| AAS endocrine | HPTA/HPG suppression, hypogonadism themes | **Educational only** | B | Kanayama 2008 `bib_9c421ff8dd` · Kanayama 2010 `bib_2334bfb4d8` · `clm_c236e9cc9d29` |
| Peptides (healing folklore) | Human evidence thin vs marketing | **Educational only** | C | BPC-157 narrative + human SR `bib_f9a28d90c7` · `bib_a25fc70d86` · `clm_30a9915f28ab` |
| GLP-1 weight loss | Large clinical weight loss under care | **Educational only** | A | STEP 1 Wilding 2021 `bib_b9b9f34e56` (PMID 33567185) · `clm_6df64d403f7e` |
| GLP-1 lean mass | Absolute lean often falls (~¼ of kg lost in analyses); keep lifting + protein | **Educational only** | B | Karakasis 2025 NMA `bib_68b8ece2a2` · tirzepatide SR `bib_8201260db4` · `clm_79a5c94646d8` |
| Retatrutide status | Emerging / investigational; don’t DIY | **Educational only** | C | Phase 2 NEJM `bib_79834f3227` (PMID 37366315) · Lilly status page `bib_697e1f91ea` · `clm_4c79d63c0a0f` |

### Nuances that matter for prose

- **Protein upper range:** Morton’s average plateau is ~**1.6 g/kg**. The book’s **1.6–2.2** band is still reasonable as a practical Year-1 range; Helms’ higher deficit intakes are **per kg FFM**, not always per kg body weight — don’t imply a universal “2.2 g/kg BW always better” law.
- **Lean mass on GLP-1s:** Absolute lean kg often drops; **relative** lean % can be stable. That is **not** the same as a sarcopenia diagnosis. Keep “skinny-soft” risk framed as behaviour (protein + resistance training), not as a guaranteed disease label.
- **Retatrutide (as of 2026-11-07):** Peer-reviewed Phase 2 obesity RCT exists; manufacturer states **not FDA-approved** and available only via trials. Phase 3 press releases exist; treat regulatory status as time-sensitive and jurisdiction-specific. Still **no titration / dosing** in the manuscript.
- **Baggish AAS CV data** are strong observational evidence, not an RCT of illicit use — evidence class **B** is honest.

---

## What’s still thin

| Gap | Why thin | Recommended next verify |
|-----|----------|-------------------------|
| Vitamin D / fish oil as Tier 1 | Plausible health framing; physique ROI not A-grade | Deficiency-conditional cites only; or demote language to “health insurance if diet/sun poor” |
| Beta-alanine / citrulline Tier 2 | Correctly niche; not re-verified here | Optional ISSN/meta cites later |
| Full peptide class map (GH secretagogues, metabolic peptides, SARMs-adjacent) | Only BPC-157 human thinness locked; other buckets still marketing-heavy | Compound-class table in a later research note; keep suitcase-word frame |
| Oral AAS hepatotoxicity / lipid mechanisms | Manuscript themes OK; primary DOI set not expanded | Add hepatic/lipid reviews before citation-index pass |
| PCT evidence quality | Correctly sceptical; not newly cited | Keep “doesn’t erase CV risk” — don’t harden into protocol language |
| Physique-specific GLP-1 muscle-preservation RCTs | Clinical obesity literature ≠ bodybuilding playbooks | Keep C–E honesty for gym “preserve muscle while on pen” tips |
| ch-17–20 weekly templates | Programming heuristics, not claim-level science | Ground in volume/frequency claims above; no new numbers without logging rationale |
| Insight-row dedupe / YouTube ASR cleanup | Out of this literature pass | Stage 4 ingest hygiene (separate worker) |

---

## Recommended manuscript edits

Apply via writing worker using `/cursor/stores/self/internal/stage5-manuscript-edit-stubs.md`. Do **not** name YouTube creators. Prefer citation IDs over new prose length.

### Safe tightenings (no chapter rewrite needed)

1. **ch-08** — Keep 1.6–2.2 g/kg; optionally add one clause that ~1.6 g/kg is where average FFM returns flatten, and deficit athletes may lean higher (especially if lean). Wire `clm_ed1a9a266269`.
2. **ch-10** — No factual correction. Optionally footnote progressive-overload necessity to `clm_b8025c3f5588`.
3. **ch-11** — Keep ~2×/week and “modest then add” volume. When citation index lands, attach `clm_a18689f43d1b` + `clm_8ce28de51045`. Avoid inventing a rigid “10-set minimum” for beginners.
4. **ch-23** — Creatine + caffeine Tier 1 statements are citation-ready (`clm_35b78a69d71c`, `clm_b8f879e58769`). Protein powder convenience → `clm_808a8b7a439d`. Leave vitamin D / fish oil soft unless deficiency-framed.
5. **ch-24** — Framing is already correct. When hardening, cite CV (`clm_98a0b3336188`) and endocrine (`clm_c236e9cc9d29`) as **risk domains**, never as cycle design. No dosing.
6. **ch-25** — Keep suitcase-word honesty. Add that injury/recovery peptide hype (e.g. widely marketed healing peptides) has **very low-certainty human data** (`clm_30a9915f28ab`). Still no DIY.
7. **ch-26** — Weight-loss magnitude literacy can reference clinical trial class without numbers theatre; lean-mass ~share-of-loss caveat is now literature-backed (`clm_79a5c94646d8`). Retatrutide: keep “investigational / jurisdiction-dependent” (`clm_4c79d63c0a0f`). **Never** add pens, units, or titration.
8. **ch-27** — No science correction; Year-1 drug-free defaults remain the right brake pedal.

### Do not change (unless editorial voice pass)

- Pathways A–D Year-1 **drug-free action plans**
- Absence of YouTube creator names
- Refusal to present PCT / peptide / GLP-1 protocols

### Dangerous-error check

No dangerous factual error requiring emergency chapter rewrite was found in sampled Part Two (ch-08–11) or Part Four (ch-23–27). Harm-reduction frames are intact.

---

## Gap checklist vs `manuscript-status.md`

| Status-doc `[RESEARCH:]` item | Outcome |
|-------------------------------|---------|
| Creatine meta / safety for ch-23 | **Filled** — ISSN + misconceptions review |
| Protein powder vs food | **Filled** — optional cite ready |
| AAS CV/endocrine DOIs for ch-24 | **Filled** — Baggish + Kanayama pair |
| Peptide evidence map by class | **Partial** — BPC-157 exemplar; other classes still thin |
| GLP-1 lean mass + retatrutide status | **Filled** — NMA/STEP 1 + Phase 2 + manufacturer status |
| Hypertrophy set-volume metas | **Filled** — Schoenfeld volume + umbrella |
| Provisional templates ch-17–20 | **Open** — programming hygiene, not new papers |
| Clean/dedupe ASR insights | **Open** — ingest worker |

---

## Method notes

- Preferred human meta-analyses, position stands, and major RCTs.
- `identifiers_verified: true` only after PubMed PMID and/or Crossref DOI resolution (Lilly page verified by live URL).
- PED/GLP-1/peptide claims marked `educational_only` with `harm_reduction` / `beginner_unsafe` flags where appropriate.
- YouTube insights were **not** used as scientific citations for these claims.
