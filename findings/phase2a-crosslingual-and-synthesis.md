# Phase 2a: cross-lingual CCB + 9-language synthesis

**Date:** 2026-05-20  **Status:** EXPLORATORY (not pre-registered)
**Scripts:** `phase2a_crosslingual_ccb.py` (+ the per-language gate-preps and `phase1c2_cross_tradition_ccb.py`)
**Outputs:** `results/phase2a/*_ccb_labse.json`

## Greek (Plotinus Neoplatonism × Clement Christian) — completes the per-language set

Source First1KGreek; Plotinus passed the within-language gate 7/7 (tiny effects,
n=1863). Cross-tradition CCB (LaBSE): only **WORLD (+0.009) and ULTIMATE (+0.004)
bind**; AWARENESS/SUBSTRATE/RECOGNITION flat.

Caveats specific to Greek: (a) effect sizes are ~5× smaller than other languages
(LaBSE compresses Greek; broad dict near-saturates), so only the strongest
convergers clear significance; (b) the Greek SUBSTRATE dict keys on ὕλη (*matter*),
which is NOT the emptiness/non-being "ground" SUBSTRATE captures elsewhere
(śūnyatā/ʿadam/ayin) — so the SUBSTRATE null is a concept-mapping artifact, not
clean evidence. AWARENESS flat is consistent with the divergent-register reading
(pagan-philosophical νοῦς vs Christian), à la Hebrew.

## Cross-LINGUAL cross-tradition CCB (the pooled capstone)

Pooled all 9 languages into the shared LaBSE space (3,756 chunks, capped 300/book;
6.1M cross-language pairs). CCB on **cross-language pairs only** (so the
language-clustering baseline cancels in the both−one contrast):

| concept | CCB (cross-language) | p |
|---|---|---|
| NONSEP | +0.0124 | <.0001 |
| SUBSTRATE | +0.0100 | <.0001 |
| SELF | +0.0092 | <.0001 |
| WORLD | +0.0087 | <.0001 |
| AWARENESS | +0.0086 | <.0001 |
| RECOGNITION | +0.0067 | <.0001 |
| ULTIMATE | +0.0042 | .002 |

**All 7 concepts show small but significant cross-language binding.** Two readings:

- **ULTIMATE is weakest cross-language** (reverse of within-language, where it was
  most robust) — because ULTIMATE is carried by tradition-specific *names* (God /
  Allah / Dao / Brahman / τὸ ἕν) that LaBSE does NOT co-locate across languages. The
  abstract concepts (NONSEP, SUBSTRATE) converge best cross-language precisely
  because they are not name-bound.
- **AWARENESS binds cross-language** despite being flat *within* Chinese/Hebrew/Greek
  — the pool is dominated by the 6 languages where it binds.

**Load-bearing caveat — the cross-lingual CCB is a WEAKER test than within-language.**
LaBSE is explicitly trained for cross-lingual semantic alignment, so
"concept-C passages cluster across languages" partly reflects the model aligning
same-topic text (νοῦς↔mind↔心↔conciencia), NOT necessarily tradition convergence.
Compounded by tag-harmonization (different per-language dictionaries fired). Within
a single language the model is not doing cross-lingual alignment, so the
within-language CCBs are cleaner evidence of tradition convergence. The cross-lingual
result is suggestive, not decisive.

## Full within-language synthesis (9 languages, all LaBSE)

| configuration | language type | AWARENESS | SUBSTRATE | ULTIMATE | WORLD |
|---|---|---|---|---|---|
| Chinese (Buddhist×Daoist) | orig, separate lineage | **flat** | binds | binds | binds |
| Hebrew (Hasidic×Rationalist) | orig, divergent register | **flat** | binds | binds | no |
| Greek (Neoplatonism×Christian) | orig, low-contrast | **flat** | (ὕλη artifact) | binds | binds |
| Arabic (Sufi×Falsafa) | orig, shared lineage | binds | binds | binds | binds |
| Hindi (Kabir×Tulsidas) | orig, shared lexicon | binds | binds | binds | binds |
| Spanish (Quietist×Carmelite) | orig, max overlap | binds (+.037) | binds | binds | binds |
| French (3-tradition) | translated | binds | flat | binds | binds |
| English (Dhammapada×TTC) | translated | binds (2/3) | weak | mixed | binds |
| Japanese (Buddhist×Confucian) | rendered | binds | binds | binds | no |

## The two robust claims after 9 languages + cross-lingual

1. **ULTIMATE binds within-language in all 9 configurations** (most robust
   within-language), BUT is the *weakest* cross-language (name-bound). So
   ULTIMATE-convergence is about *role* (each tradition's absolute occupies the
   analogous structural position) not shared embedding location.

2. **AWARENESS convergence is a vocabulary-overlap effect.** It binds wherever
   traditions share an awareness-lexicon (shared lineage: Arabic/Hindi; shared
   school: Spanish; translation/rendering: English/French/Japanese) and fails where
   the lexicons diverge — by separate lineage (Chinese), by register (Hebrew), or in
   low-contrast Greek. This dissociation — surfaced only by going multilingual — is
   the project's sharpest methodological result: it separates likely-structural
   convergence (the ontological concepts, esp. SUBSTRATE in original languages with a
   genuine emptiness-concept) from vocabulary-driven convergence (AWARENESS).

## Open / next

- Tibetan Buddhist×Bön (ideal 2nd separate-lineage original) remains a sourcing wall.
- Cross-lingual result needs a non-LaBSE corroboration to separate tradition
  convergence from the embedder's alignment objective (a model NOT trained on bitext).
- Consolidate into paper §6.10 + pre-register the vocabulary-overlap hypothesis.
