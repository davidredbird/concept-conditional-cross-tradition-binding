# Phase 2b — design sketch: same-works-across-languages (parallel corpus)

**Status:** DESIGN (not started)  **Premise:** Phase 2a's cleanest single result was
the *language-controlled* test — the **same works** (Dhammapada × Tao Te Ching) bind
AWARENESS in English translation but not in the original classical Chinese.
Phase 2b **generalizes that control to many works × many languages**, turning the
language/translation effect into something measured rather than inferred.

## Why this is the right next move

Phase 2a's per-language CCBs each used *different* tradition-pairs in different
languages, so language and tradition-composition were confounded (we untangled it
only partially, via the one Dhammapada×TTC control). A parallel corpus of the SAME
works across languages **holds tradition AND text fixed and varies only language** —
the clean experimental design for the central question:

> Is cross-tradition concept-binding (esp. AWARENESS) structural, or manufactured by
> shared translation vocabulary?

It also operationalizes the westernization triangulation sketched in
`phase2a-design-sketch.md` (convergence = β₀ + β₁·westernization + β₂·representation):
westernization is now cleanly defined per (work, language, translation-chain).

## The parallel-text backbone (works available in many languages)

Target a matrix of {work × language}. Priority works (most multilingual, PD):

| work | tradition | original | translations we have / to get |
|---|---|---|---|
| **Tao Te Ching** | daoism | classical Chinese ✓ | EN ✓×3 (Carus/Goddard/Legge), FR ✓ (Julien); add DE (Wilhelm), ES, RU, more |
| **Dhammapada** | Buddhist | Pali (gate-fails) | ZH ✓ (faju), EN ✓ (Müller); add DE (Neumann), FR, HI, JA, ES |
| **Bhagavad Gītā** | vedanta | Sanskrit (gate-fails) | EN ✓×3, FR ✓ (Burnouf); add DE (Deussen/Schroeder), HI, ES |
| **Heart / Diamond Sutra** | Mahayana | Sanskrit/Chinese | EN, ZH, JA, multiple — short, easy |
| **Upaniṣads** (Kena/Mundaka/Mandukya) | vedanta | Sanskrit | EN, DE (Deussen), FR |
| **Gospels / Bible** | Christian | Greek | ~every language (huge parallel anchor) |

**Key source — SuttaCentral**: the same suttas + Dhammapada in MANY modern languages
via its API (we already coded `fetch_suttacentral_api`). This is the cheapest way to
get one Buddhist work across EN/DE/FR/ES/PT/etc. Combine with per-language TTC for the
Buddhist×Daoist pair in each language.

## Analyses Phase 2b enables

1. **Fixed-pair cross-language CCB (the headline).** Buddhist(Dhammapada) × Daoist(TTC)
   in each language: ZH (orig×orig), EN, FR, DE, ES, ... Plot CCB(AWARENESS) and
   CCB(SUBSTRATE) vs language. Prediction from Phase 2a: AWARENESS rises with
   translation/westernization (flat in original ZH, positive in Western translations);
   SUBSTRATE stays high in originals, dilutes in translation. A clean gradient would
   confirm the vocabulary-overlap mechanism quantitatively.

2. **Within-work cross-language concept-structure stability.** For a single work (e.g.
   the TTC), does its within-text concept-binding profile survive translation? Compare
   within-TTC binding in ZH vs EN vs FR vs DE. Tests whether translation preserves or
   reshapes a single text's structure.

3. **Translator-variance band (extends Phase 1b).** We have TTC×3 and Gītā×3 English
   translations; widen to more translators per work to bound translator noise as a
   reference scale against which the cross-language effect is judged.

4. **Westernization covariate-adjustment decomposition.** With (work, language,
   translation-chain) tuples, fit convergence = β₀ + β₁·westernization +
   β₂·representation + ε (the `phase2a-design-sketch.md` model), now with real
   parallel data. β₂ (representation) = the contamination-immune FLORES fertility
   from Stage-1.

## Build plan

1. **Corpus expansion** — assemble {work × language} matrix; reuse per-language fetchers
   (Wikisource fetchers for FR/ES/HI/JA, OpenITI/Sefaria/First1KGreek where relevant)
   + SuttaCentral multilingual for the Buddhist works; add German (Wilhelm TTC, Neumann
   Dhammapada, Deussen Upaniṣads — sourcing TBD, archive.org Fraktur risk).
2. **Reuse the Phase 2a per-language Option-A dicts** (Chinese/Arabic/Hindi/Hebrew/
   Greek/French/Spanish/English/Japanese) — tagging is far more comparable when the
   *content* is the same work across languages.
3. **Gate-first** each new language (already cleared for the 9; clear DE/RU/etc. as added).
4. Run analyses 1–4; pre-register the AWARENESS-gradient prediction first.

## Caveats to carry

- Originals for Dhammapada (Pali) and Gītā/Upaniṣads (Sanskrit) FAIL the LaBSE gate —
  so the "original" cell for those works is unavailable; classical Chinese (TTC, faju)
  remains the load-bearing original. Seek other gate-passing originals where possible.
- Same single embedding model (LaBSE); per-language tagging hidden DoF persists.
- Translation provenance/era must be tracked per text (the westernization tuple).
