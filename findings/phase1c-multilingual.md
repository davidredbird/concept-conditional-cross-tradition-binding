# Phase 1c: Multilingual Source Analysis (first pass, multilingual-e5-large)

**Date:** 2026-05-18 (analysis), documented 2026-05-20
**Pre-registration:** `findings/phase1c-preregistration.md` (committed at public commit `abac25c`, Zenodo `v1.3-prereg-phase1c`, prior to running any Phase 1c main analysis)
**Embedding model (this pass):** `intfloat/multilingual-e5-large` via ONNX Runtime
**Author:** T. David Kinlaw, ORCID 0009-0008-5213-1017

---

## TL;DR

The Phase 1c embedding-quality validation gate **passed** for both candidate models (e5-large and LaBSE) on parallel Sanskrit-English Bhagavad Gita verses (5/5 cross-lingual same-verse matching). But the two main hypothesis tests surfaced **three substantive methodology findings, none of which were on the original Phase 1c plan**:

1. **Multilingual prototype concept tagging (Option B) fails across language boundaries.** The Option A spot-check against manual Sanskrit/Pali regex dictionaries returned Cohen's κ ≈ 0 (−0.06 for AWARENESS, +0.01 for RECOGNITION). Multilingual embeddings preserve coarse-grained topic similarity but not fine-grained concept-specificity across languages. Per the prereg, **Phase 1c.2 is reported as EXPLORATORY**.

2. **Phase 1c.1's cross-lingual variance hypotheses are NOT SUPPORTED in their strong pre-registered form**, but the permutation test still finds cross-lingual same-source pairs preserve source identity significantly above chance (p < 0.0001). Language is a stronger feature than source content in e5-large's embedding space; cross-lingual same-source pairs (0.8377) are less similar than same-language cross-source pairs (0.8509).

3. **Embedding model choice substantively shapes the variance decomposition.** e5-large compresses all cosines into 0.82–0.89 (total variance range 0.0639) versus MiniLM's 0.44–0.67 range in Phase 1b (range 0.2291). The Phase 1a five-of-seven binding result was measured with MiniLM; a generalist multilingual retrieval model gives materially different magnitudes. This argues that cross-model replication is not optional for Phase 1c — it is the load-bearing control.

**The exploratory Phase 1c.2 result is directionally consistent with Phase 1a** (AWARENESS and RECOGNITION both bind cross-tradition at p < 0.0001 on Sanskrit-Pali, even under the failed Option B tagging), but cannot be claimed as confirmation. Confirmatory Phase 1c.2 requires Option A (manual per-language regex) tagging and ideally LaBSE embeddings.

---

## 1. Embedding-quality validation gate (PASSED)

The prereg required a validation gate before main analysis: do multilingual embeddings cleanly distinguish parallel Sanskrit-English Gita verses? Both models passed (`results/phase1c/embedding_validation.json`):

| Model | Script | Same-verse mean | Diff-verse mean | Separation | Correct matches |
|---|---|---|---|---|---|
| multilingual-e5-large | Devanagari | 0.8535 | 0.7983 | +0.0552 | **5/5** |
| multilingual-e5-large | IAST | 0.8013 | 0.7967 | +0.0046 | 2/5 (FAIL) |
| LaBSE (canonical) | Devanagari | 0.3508 | 0.1035 | +0.2472 | **5/5** |
| LaBSE | IAST | 0.4607 | 0.4392 | +0.0215 | 1/5 (FAIL) |

Two sub-findings from validation:
- **Devanagari script substantially outperforms IAST transliteration** across all models. Multilingual models have far more Devanagari Sanskrit in training data than IAST. All Phase 1c Sanskrit sources use Devanagari accordingly.
- **LaBSE's separation (0.247) is 4.5× e5-large's (0.055).** LaBSE is purpose-built for cross-lingual sentence similarity; e5-large is a generalist retrieval model. This foreshadowed the embedding-compression issue in Phase 1c.1.

## 2. Corpus

After cleaning, chunking, and source verification (one source — Katha Upanishad from Sanskrit Wikisource — was found to be MediaWiki navigation chrome rather than transcribed verses, and dropped):

| Language | Tradition | Texts | Chunks |
|---|---|---|---|
| sanskrit | advaita | Bhagavad Gita, Mandukya, Mundaka, Kena | 176 |
| pali | theravada | Dhammapada, DN 22 Mahasatipatthana, MN 10 Satipatthana | 27 |
| classical_chinese | daoism | Tao Te Ching | 29 |
| english | (Phase 0/1a/1b) | — | 5,777 |

Phase 1c.2 (cross-tradition CCB) uses the 176 Sanskrit + 27 Pali chunks (4,752 cross-tradition pairs). Phase 1c.1 (variance decomposition) uses the full 6,009-chunk corpus embedded with the multilingual model.

## 3. Concept tagger calibration (multilingual-e5-large, Option B)

English regex tag rates (calibration target, computed on 5,777 English chunks) and resulting multilingual tag rates after threshold calibration:

| Concept | English (regex) | Sanskrit | Chinese | Pali |
|---|---|---|---|---|
| ULTIMATE | 63.7% | 100.0% | 89.7% | 100.0% |
| SUBSTRATE | 1.7% | 14.8% | 0.0% | 3.7% |
| AWARENESS | 4.0% | 90.9% | 20.7% | 81.5% |
| WORLD | 16.5% | 76.1% | 44.8% | 40.7% |
| SELF | 2.4% | 22.2% | 0.0% | 0.0% |
| RECOGNITION | 5.7% | 94.9% | 0.0% | 92.6% |
| NONSEP | 0.1% | 9.1% | 0.0% | 0.0% |

**The over-tagging is severe and systematic.** Sanskrit and Pali chunks have higher cosine similarity to nearly all concept prototypes than English chunks do. They cluster generically as "religious-philosophical content" in multilingual embedding space, so the English-calibrated threshold sweeps in 80–100% of them for the high-frequency concepts. The threshold calibrated to a 4.0% English AWARENESS rate tags 90.9% of Sanskrit chunks.

## 4. Option A spot-check (FAILED — Phase 1c.2 is EXPLORATORY)

Per prereg §3.3, Option B was validated against manual Sanskrit/Pali regex dictionaries (constructed from Monier-Williams Sanskrit-English Dictionary and the PTS Pali-English Dictionary) for AWARENESS and RECOGNITION (`results/phase1c/option_a_spot_check_*.json`):

| Concept | Language | Option A tagged | Option B tagged | Agreement | Cohen's κ |
|---|---|---|---|---|---|
| AWARENESS | sanskrit | 32 / 176 | 160 / 176 | 19.3% | −0.061 |
| AWARENESS | pali | 15 / 27 | 22 / 27 | 59.3% | +0.124 |
| AWARENESS | combined | 47 / 203 | 182 / 203 | 24.6% | −0.057 |
| RECOGNITION | sanskrit | 11 / 176 | 167 / 176 | 11.4% | +0.007 |
| RECOGNITION | pali | 0 / 27 | 25 / 27 | 7.4% | +0.000 |
| RECOGNITION | combined | 11 / 203 | 192 / 203 | 10.8% | +0.007 |

**Decision rule (pre-registered): κ < 0.5 OR agreement < 70% → FAIL → Phase 1c.2 reported as EXPLORATORY.** Both concepts fail decisively. Cohen's κ near zero means Option B prototype tagging has essentially no correlation with the hand-curated scholarly term lists.

**This is the central methodology finding of the Phase 1c first pass.** Multilingual embeddings preserve coarse semantic topic (validation passed: parallel verses match across language) but do not preserve fine-grained concept-specificity (a Sanskrit passage about AWARENESS specifically is not distinguishable from a Sanskrit passage about religion generically, when the prototype is an English concept phrase). The prereg's Option A spot-check existed precisely to catch this, and it did.

## 5. Phase 1c.1: cross-lingual within-source variance decomposition

`results/phase1c/phase1c1_variance_*.json`. Pair-type means (e5-large, full 6,009-chunk corpus):

| Mask | Definition | Mean cosine | n_pairs |
|---|---|---|---|
| W-S-S-T | same-translator same-source | 0.8854 | 27,485 |
| W-S-B-T-W-L | between-translator, same language | 0.8527 | 32,389 |
| W-S-B-T-X-L | between-translator, cross language | 0.8377 | 38,901 |
| X-S-W-T | cross-source, within-tradition, same-language | 0.8509 | 2,348,630 |
| X-T | cross-tradition, same-language | 0.8215 | 14,291,629 |

### Hypothesis outcomes

**H1c.1.a (W-S-B-T-X-L > X-S-W-T): NOT SUPPORTED.** Observed W-S-B-T-X-L (0.8377) is *below* X-S-W-T (0.8509). Cross-lingual same-source pairs are less similar than same-language cross-source pairs. *However*, the permutation test (shuffling source_id within tradition+language) finds observed source-preservation significantly above the null (observed contrast −0.0133 vs null mean −0.0187, p < 0.0001). Interpretation: multilingual e5-large DOES preserve some source identity across language — significantly more than random source assignment — but not enough to overcome the language barrier relative to same-language cross-source baselines. **Language is a stronger feature than source content in this embedding space.**

**H1c.1.b (cross-lingual gap small): NOT SUPPORTED, narrowly.** |W-S-B-T-X-L − W-S-B-T-W-L| = 0.0151; total variance (W-S-S-T − X-T) = 0.0639; ratio = 0.236, just above the 0.20 threshold.

**H1c.1.c (variance ordering): NOT SUPPORTED.** The ordering breaks at W-S-B-T-X-L (0.8377) < X-S-W-T (0.8509). The predicted chain W-S-S-T > W-S-B-T-W-L ≥ W-S-B-T-X-L > X-S-W-T > X-T fails because cross-lingual same-source slips below same-language cross-source.

### The embedding-compression finding

The total variance range is **0.0639** with e5-large, versus **0.2291** with MiniLM in Phase 1b — a 3.6× compression. Decomposing:

| Effect | e5-large (Phase 1c.1) | MiniLM (Phase 1b) |
|---|---|---|
| Translator (W-S-S-T − W-S-B-T-W-L) | 0.0327 | 0.0447 |
| Source-content within-language (W-S-B-T-W-L − X-S-W-T) | **0.0018** | (n/a, English-only) |
| Tradition (X-S-W-T − X-T) | 0.0294 | 0.0948 |

The striking number is **source-content-within-language at 0.0018** — in e5-large's space, English translations of the *same* Hindu text are barely more similar to each other than English translations of *different* Hindu texts. e5-large, optimized for retrieval, captures coarse topic ("this is a Hindu text") but compresses fine-grained source distinctions. This directly explains why Option B concept tagging fails: the model that can't distinguish Gita-content from Upanishad-content within English certainly can't distinguish AWARENESS-content from generic-religious-content within Sanskrit.

**This makes cross-model replication the load-bearing control for Phase 1c, not an optional add-on.** LaBSE, with 4.5× the validation separation, may preserve fine-grained content where e5-large does not.

## 6. Phase 1c.2: cross-tradition CCB (EXPLORATORY)

`results/phase1c/phase1c2_ccb_*.json`. Sanskrit Advaita (176 chunks) vs Pali Theravada (27 chunks), 4,752 cross-tradition pairs, Option B tags, e5-large embeddings:

| Concept | n_both | n_only | CCB | p (one-sided) | Verdict |
|---|---|---|---|---|---|
| RECOGNITION | 4,175 | 559 | +0.0312 | < 0.0001 | BIND |
| AWARENESS | 3,520 | 1,152 | +0.0228 | < 0.0001 | BIND |
| WORLD | 1,474 | 2,606 | +0.0048 | 0.011 | BIND (small) |
| SUBSTRATE | 26 | 826 | −0.0089 | 0.98 | not significant |
| ULTIMATE | 4,752 | 0 | n/a | n/a | untestable (all tagged) |
| SELF | 0 | 1,053 | n/a | n/a | untestable (0 Pali tags) |
| NONSEP | 0 | 432 | n/a | n/a | untestable |

**3 of 5 Phase 1a-binding concepts bind at p < 0.05** (AWARENESS, RECOGNITION, WORLD). H1c.2.a (≥ 2 of 5) and H1c.2.b (AWARENESS + RECOGNITION both bind) are both nominally SUPPORTED.

**But this is EXPLORATORY, not confirmatory** (Option B failed validation, §4). The result is suggestive rather than dispositive:
- The *direction* is consistent with Phase 1a — AWARENESS and RECOGNITION bind cross-tradition, the same two concepts that headline the English analysis.
- The *magnitudes* are much smaller (CCB +0.02 to +0.03 vs Phase 1a's +0.05 to +0.11), consistent with the e5-large compression in §5.
- The fact that significant CCB emerges *despite* 90%+ over-tagging is itself interesting: even when most chunks are spuriously tagged, the both-tagged pairs cluster slightly tighter than one-tagged pairs. Something survives. But "something survives despite broken tagging" is not a result we can report confirmatorily.

## 7. What this means for the project

**The CCB methodology is unaffected — these are findings about applying it across languages, which is exactly what Phase 1c set out to test.** The honest decomposition:

- **Confirmed:** Multilingual embeddings can match parallel content across language (validation, coarse-grained).
- **Refuted:** Multilingual embeddings cannot tag fine-grained concepts across language via English prototypes (Option B failure).
- **Refuted (strong form):** Cross-lingual same-source pairs do not exceed same-language cross-source similarity in e5-large; the strong "multilingual embedding sees through translation" claim fails for this model.
- **Confirmed (weak form):** Cross-lingual same-source pairs preserve significant source identity above chance.
- **Exploratory, suggestive:** Cross-tradition AWARENESS and RECOGNITION CCB survive multilingual analysis directionally, even with broken tagging.
- **Newly surfaced:** Embedding-model choice substantively determines the variance decomposition; the Phase 1a result is model-dependent.

For the broad-form constructivist objection (anglophone scholar-tradition shared consensus), Phase 1c does NOT yet deliver a verdict. The exploratory result is encouraging for the perennialist reading, but the tagging failure and embedding compression mean we cannot make the strong claim. A confirmatory Phase 1c.2 (Option A tagging + LaBSE embeddings) is required.

## 7b. Phase 1c.2 second pass: Option A tagging + cross-model (2026-05-20)

Following the Option B validation failure, we ran the more rigorous Option A
analysis: manual Sanskrit/Pali regex dictionaries (`scripts/multilingual_option_a_tagger.py`,
all seven concepts, term lists from Monier-Williams and PTS), with cross-tradition
CCB computed under both embedding models.

**Option A tagging is far more discriminating than Option B** (`results/phase1c/option_a_tag_counts.json`):

| Concept | Sanskrit (Option A) | Pali (Option A) | (Sanskrit Option B for comparison) |
|---|---|---|---|
| ULTIMATE | 135/176 | 3/27 | (100%) |
| SUBSTRATE | 72/176 | 1/27 | (14.8%) |
| AWARENESS | 70/176 | 23/27 | (90.9%) |
| WORLD | 112/176 | 5/27 | (76.1%) |
| SELF | 105/176 | 15/27 | (22.2%) |
| RECOGNITION | 33/176 | 17/27 | (94.9%) |
| NONSEP | 28/176 | 0/27 | (9.1%) |

(A regex bug was found and fixed on the first Option A run: trailing `\b` on
transliterated stems failed on Pali/Sanskrit inflectional endings — "nibbāna" is
inflected as "nibbānaṁ", "nibbāne", etc. The Pali corpus has 30 "nibb" occurrences
but `\bnibbāna\b` matched 0. Stem-prefix matching fixed it.)

**A WDAC environment note:** the workstation's Application-Control policy refreshed
between the first pass (2026-05-18) and this pass (2026-05-20) and began blocking
a pandas DLL imported transitively by sentence-transformers. LaBSE was re-implemented
via the transformers `AutoModel` path (pooler_output + L2-normalize), which
reproduces sentence-transformers LaBSE output exactly (validation: 0.3508 same-verse,
+0.2472 separation, 5/5) and avoids the pandas import chain. `scripts/multilingual_embedder.py`
now uses the transformers backend for LaBSE.

### Cross-tradition CCB, Option A, both models

`results/phase1c/phase1c2_ccb_optionA_e5large.json`, `..._optionA_labse.json`:

| Concept | e5-large CCB (p) | LaBSE CCB (p) |
|---|---|---|
| ULTIMATE | +0.0027 (0.10) | +0.0029 (0.32) |
| SUBSTRATE | +0.0001 (0.48) | +0.0030 (0.33) |
| AWARENESS | −0.0044 (0.99) | +0.0066 (0.16) |
| WORLD | −0.0019 (0.83) | −0.0095 (0.94) |
| SELF | +0.0029 (0.07) | +0.0060 (0.16) |
| RECOGNITION | +0.0017 (0.26) | +0.0018 (0.42) |
| NONSEP | untestable (0 Pali) | untestable (0 Pali) |

**Zero of five Phase 1a-binding concepts bind, under either model.** H1c.2.a and
H1c.2.b are NOT SUPPORTED with Option A tagging. This reverses the exploratory
Option B result and confirms that the Option B "binding" was an over-tagging
artifact (when 90%+ of chunks are tagged, the both-tagged set is nearly all
cross-tradition pairs and the small only-tagged set is biased).

LaBSE's cross-tradition baseline is 0.57 (vs e5-large's compressed 0.89), so the
null result is NOT a dynamic-range artifact — LaBSE has resolution to spare and
still finds nothing. Two independent multilingual models agree.

### Interpretation (stated carefully)

The cross-tradition CCB signal Phase 1a/1b measured on English translations
(advaita × theravada RECOGNITION at +0.110 technical-only) **does not survive on
original-language Sanskrit-Pali text under rigorous concept tagging, replicated
across two embedding models.** This is genuine evidence for the *broad* form of
the constructivist objection: the English-corpus convergence may be substantially
mediated by the anglophone scholar-translation tradition.

Three caveats bound this interpretation — it is NOT "constructivism wins":

1. **Tiny, asymmetric corpus.** 176 Sanskrit (Advaita Vedanta — Gita, Upanishads)
   vs 27 Pali (Dhammapada + two Satipatthana mindfulness-practice suttas, not
   liberation-theology). The two sides may not be discussing the same content
   even within shared concept tags. The Pali side is severely underpowered.
2. **Monolingual vs multilingual embedding mismatch.** Phase 1a used MiniLM
   (monolingual, wide dynamic range). Phase 1c uses multilingual models with
   compressed cross-lingual similarity. The disappearance could be the anglophone
   artifact OR the embedding-model difference; the present data cannot fully
   separate them. A clean test would re-run Phase 1a English RECOGNITION CCB under
   the same multilingual models — if it also vanishes, the cause is the model, not
   the language.
3. **Post-hoc, not pre-registered.** The prereg's primary tagger was Option B
   (which failed validation). Option A CCB is more rigorous but is a post-hoc
   analysis motivated by the Option B failure, reported transparently as such
   rather than as the pre-registered confirmatory test.

This is the project's first result that cuts *against* the perennialist reading.
It substantially qualifies the Phase 1a positive finding and is reported in full
because the project's posture is indifference to which way results go.

### The critical follow-up control

To separate caveat 2 (anglophone artifact vs embedding-model difference): re-run
the Phase 1a English advaita × theravada RECOGNITION CCB using e5-large and LaBSE
embeddings (instead of MiniLM). If the English binding ALSO disappears under the
multilingual models, the Phase 1c.2 null is an embedding-model artifact, not
evidence about translation tradition. If the English binding SURVIVES under
multilingual models but the Sanskrit-Pali binding does not, that isolates the
language/translation effect and strengthens the broad-constructivist reading.
This is the single most important next analysis.

## 8. Next steps (Phase 1c second pass)

1. **Option A confirmatory tagging.** Extend the manual Sanskrit/Pali regex dictionaries (currently AWARENESS + RECOGNITION from the spot-check) to all five Phase 1a-binding concepts. Run Phase 1c.2 CCB with Option A tags. This is the confirmatory test the prereg requires.
2. **LaBSE cross-model replication.** Embed the 203 non-English Phase 1c.2 chunks with LaBSE (~1 min) and re-run Phase 1c.2. Embed the full corpus with LaBSE (~2 hrs background) and re-run Phase 1c.1. LaBSE's higher dynamic range may preserve the source/concept distinctions e5-large compresses.
3. **Report cross-model agreement (H1c.2.c)** once both models are run with Option A.
4. **Paper Draft 7 §6.10** documenting Phase 1c, including the three methodology findings as contributions rather than failures.

---

*This document reports the Phase 1c first-pass results transparently against the pre-registration. Hypotheses refuted in their strong form are reported as such; the Option B tagging failure that the prereg's spot-check was designed to catch is reported as a substantive methodology finding. Confirmatory Phase 1c.2 (Option A + LaBSE) is the documented next step.*
