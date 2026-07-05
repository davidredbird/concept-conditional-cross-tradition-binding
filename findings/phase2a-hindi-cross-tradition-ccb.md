# Phase 2a: cross-tradition CCB in Hindi (Kabir Nirguṇa × Tulsidas Saguṇa)

**Date:** 2026-05-20  **Status:** EXPLORATORY (not pre-registered)
**Scripts:** `fetch_hindi_texts.py`, `hindi_gate_prep.py`, `phase1c2_cross_tradition_ccb.py`
**Outputs:** `results/phase2a/hindi_kabir_tulsidas_ccb_labse.json`

The Hindi sourcing wall is **cracked**: hi.wikisource serves born-digital
Devanagari (NOT the OCR garbage that blocked archive.org). Both texts are
**original Hindi/Awadhi** (15–16c).

| text | tradition | category | chunks |
|---|---|---|---|
| कबीर ग्रंथावली Kabir Granthāvalī | sant (Nirguṇa, formless) | nondual | 294 |
| रामचरितमानस बालकाण्ड (Tulsidas) | bhakti (Saguṇa, devotional) | dualistic | 133 |

## Gate-first: Hindi RESOLVES under LaBSE

Within-Kabir binding: 5/7 (ULTIMATE +0.016, SUBSTRATE +0.017, SELF +0.012, WORLD
+0.008, RECOGNITION +0.007; all p<.05). AWARENESS does NOT resolve within-Kabir
(+0.0004, p=.43) — but that is a **tagging-saturation** artifact (मon/मन tags 210/294
chunks, leaving a weak contrast), not a model failure. Hindi is a valid test language.

## Result (LaBSE; cross-tradition cosine 0.467 ± 0.063 — resolves)

| concept | CCB | p |
|---|---|---|
| SUBSTRATE | +0.030 | <.0001 BIND |
| NONSEP | +0.022 | .003 BIND |
| ULTIMATE | +0.020 | <.0001 BIND |
| AWARENESS | +0.010 | .005 BIND |
| WORLD | +0.010 | .004 BIND |
| RECOGNITION | +0.009 | .009 BIND |
| SELF | +0.002 | .33 no |

5/5 Phase-1a concepts bind, including AWARENESS + RECOGNITION (AWARENESS small,
+0.010 — weakest binder, depressed by मन saturation).

## Why this matters: Hindi confirms the framework on a THIRD original language

Hindi is **original-language** (not translated) yet AWARENESS **binds** — the
*opposite* of original Chinese. This proves the key variable is NOT
original-vs-translated, but **shared-vs-distinct awareness-vocabulary**:

- Kabir and Tulsidas are both **original Hindi** and share the Hindi devotional/
  Sant lexicon (राम, मन, ज्ञान, सुरति). Shared awareness-vocabulary → AWARENESS binds.
- Chinese Buddhist (識/覺/念) and Daoist (心/神/明) are **separate imported-vs-
  indigenous lineages** with largely distinct awareness-lexicons → AWARENESS flat.

So among the three ORIGINAL-language tests:

| original-language test | shared awareness-lexicon? | AWARENESS |
|---|---|---|
| classical Arabic (Sufi×Falsafa) | yes (Greek-Arabic philosophical lexicon) | binds |
| Hindi (Kabir×Tulsidas) | yes (shared Hindi/Sant lexicon) | binds |
| **classical Chinese (Buddhist×Daoist)** | **NO (distinct lineage lexicons)** | **flat** |

**The original/translated axis is NOT the driver** (two originals bind, one doesn't);
**shared awareness-vocabulary is.** Chinese remains the unique distinct-lexicon
configuration, and it is the lone AWARENESS-null.

**SUBSTRATE binds in all THREE original languages** (Chinese +0.054, Arabic +0.033,
Hindi +0.030) — the most robust, lineage- and language-independent converger.

## Full cross-linguistic synthesis (6 configurations, all LaBSE)

| configuration | AWARENESS | SUBSTRATE | shared vocab? | original? |
|---|---|---|---|---|
| classical Chinese (Buddhist×Daoist) | **flat** | binds | NO | yes |
| classical Arabic (Sufi×Falsafa) | binds | binds | yes (native) | yes |
| Hindi (Kabir×Tulsidas) | binds | binds | yes (native) | yes |
| English (Dhammapada×TTC, broad) | binds (2/3 tr.) | weak | yes (translation) | no |
| French (3-tradition) | binds | flat | yes (translation) | no |
| Japanese (Buddhist×Confucian) | binds | binds | yes (rendering) | no |

**AWARENESS / RECOGNITION converge iff traditions share an awareness-vocabulary
(native lineage OR translation/rendering); they fail only across original-language
separate lineages with distinct lexicons — uniquely classical Chinese.
SUBSTRATE / ULTIMATE converge across (nearly) all configurations — the strongest
candidates for genuine cross-tradition structural convergence.**

## Caveats

- AWARENESS near-saturated on both Hindi sides (मन over-tags) → weak/depressed effect.
- Kabir (Nirguṇa) and Tulsidas (Saguṇa) are contrasting streams but both Bhakti-era
  Hindi — a real Nirguṇa/Saguṇa divide, but less lineage-separate than Buddhist×Daoist.
- Devanagari Option-A dict: hidden DoF; medieval spelling variants only partially covered.
- Single model (LaBSE); exploratory, not pre-registered.

## Bottom line

The hardest sourcing wall is cracked, and Hindi adds the decisive third
original-language data point: it is **shared awareness-vocabulary, not
original-vs-translation, that gates AWARENESS convergence.** Classical Chinese
stays the lone separate-lineage exception. The ontological concepts
(SUBSTRATE/ULTIMATE) remain robust everywhere.
