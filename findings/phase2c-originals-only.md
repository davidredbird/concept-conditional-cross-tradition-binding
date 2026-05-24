# Phase 2c — originals-only convergence (translation effects impossible)

**Date:** 2026-05-20  **Status:** EXPLORATORY (David's design)
**Script:** `scripts/phase2c_originals_only_ccb.py`
**Premise:** use ONLY texts in their original composition language, so NO
translation effect can appear. Any convergence here is translation-free.

## Corpus (originals only, LaBSE-gate-passing)

2,571 chunks across 6 languages — all composed in-language:
classical_chinese (TTC Daoist + Platform Sutra Chan), arabic (Fuṣūṣ Sufi + Najāt
Falsafa), greek (Plotinus Neoplatonism + Clement Christian), hindi (Kabir Sant +
Tulsidas Bhakti), spanish (Molinos Quietist + Teresa Carmelite), hebrew (Nachman
Hasidic). **Excluded as translations:** faju (ZH tr. from Indic), Maimonides Guide
(HE = Ibn Tibbon tr.), all French/English/Japanese.

## Results

**Cross-language pairs (translation-free; retains the LaBSE cross-lingual-alignment confound):**

| concept | CCB | p |
|---|---|---|
| SUBSTRATE | **+0.0066** | .004 BIND |
| WORLD | +0.0063 | .004 BIND |
| SELF | +0.0042 | .02 BIND |
| NONSEP | +0.0047 | .095 marginal |
| **AWARENESS** | **+0.0005** | **.38 FLAT** |
| ULTIMATE | −0.0040 | .98 flat (name-bound) |
| RECOGNITION | −0.0035 | .91 flat |

**Within-language pairs (cleanest — no translation AND no cross-lingual-alignment confound):**

| concept | CCB | p |
|---|---|---|
| SUBSTRATE | +0.0334 | <.0001 BIND |
| ULTIMATE | +0.0277 | <.0001 BIND |
| AWARENESS | +0.0228 | <.0001 BIND |
| SELF | +0.0230 | <.0001 BIND |
| NONSEP | +0.0116 | .011 BIND |
| WORLD | −0.0064 | .98 flat |
| RECOGNITION | −0.0111 | .999 flat |

## The decisive finding

**Across ORIGINAL languages (no translation possible), SUBSTRATE converges but
AWARENESS is flat.** This is the cleanest evidence yet for the central dissociation:

- **SUBSTRATE convergence is translation-free.** It binds across original Chinese,
  Arabic, Hindi, Hebrew, Greek, Spanish — with zero translation involved. So
  SUBSTRATE convergence is NOT a translation artifact. (It could still be the
  LaBSE alignment objective for the cross-language part — but the within-language
  originals binding [+0.033] has no such confound, so SUBSTRATE convergence is real.)

- **AWARENESS convergence is translation/vocabulary-dependent.** Cross-language and
  translation-free, it vanishes (+0.0005, p=.38) — original-language traditions use
  different awareness-words (識 / عقل / मन / νοῦς / alma) that do not converge.
  AWARENESS *does* bind within-language-originals (+0.023), because traditions
  sharing a language can share its awareness-lexicon (Arabic/Hindi/Spanish). So
  AWARENESS convergence requires shared vocabulary — native (within-language) or
  imposed (translation) — and has no language-independent existence.

- **ULTIMATE** confirms role-convergence: strong within-language (+0.028),
  name-bound cross-language (flat). Each tradition's absolute occupies the analogous
  position in its own discourse but the names don't co-locate across languages.

## Bottom line

Phase 2c isolates the result Phase 2a/2b inferred: **with translations banned,
SUBSTRATE still converges across languages and AWARENESS does not.** SUBSTRATE
(and within-language ULTIMATE/SELF) is the genuine, translation-free
cross-tradition structural signal; AWARENESS convergence is an artifact of shared
awareness-vocabulary (native or translated), with no cross-lingual structural basis.

## Caveats

- Cross-language part still carries the LaBSE alignment-objective confound (the model
  is trained to align same-topic text across languages); the within-language
  originals result does not, and it agrees on SUBSTRATE.
- Per-language Option-A dicts (hidden DoF); 6 languages; single model; exploratory.
- WORLD is inconsistent (binds cross-language, flat within) — noisy; not load-bearing.
