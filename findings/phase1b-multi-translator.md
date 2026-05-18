# Phase 1b: Multi-Translator Within-Source Variance Test

**Date:** 2026-05-18
**Pre-registration:** `findings/phase1b-preregistration.md` (committed at public commit `d16fc8c` prior to running this analysis; Zenodo `v1.2-prereg-phase1b` release at the same commit)
**Analysis script:** `scripts/phase1b_within_source_variance.py`
**Results file:** `results/phase1b/within_source_variance.json`
**Embeddings cache:** `results/phase1b/embeddings.npy` (5,777 chunks × 384-dim MiniLM)
**Embedding model:** `sentence-transformers/all-MiniLM-L6-v2` via ONNX Runtime
**Author:** T. David Kinlaw (Independent Researcher / Redbird Software LLC), ORCID 0009-0008-5213-1017

---

## TL;DR

The pre-registered variance ordering (H1b.1) and translator-bound (H1b.2) hypotheses were **confirmed**. The pre-registered permutation-test direction (H1b.3) was **refuted in an informative way**: real cross-translator pairs are highly significantly *less* similar than label-permuted pairs (z ≈ −17.9), the opposite direction from what was pre-registered. The pre-registered absolute cosine magnitudes were systematically too low (calibration error); the relative structure was correctly predicted.

**Headline finding:** Translator-as-confound is bounded. Translator effect accounts for 19.5% of total within/cross-tradition variance — well below the 35% pre-registered threshold. Source-content and tradition effects are each approximately twice as large as the translator effect.

**For the paper:** §9 limitation 1 (translator-as-confound) moves from "unaddressed" to "tested and bounded at 19.5% on two source families." The cross-tradition CCB signal measured in Phase 1a is **not** primarily a translator artifact.

**What this does not show:** Phase 1b tests *between-translator* variance within the anglophone scholar-translator tradition. It does not test whether that tradition itself imposes structural conformity invisible to within-tradition variance partitioning. That is the explicit target of Phase 1c (multilingual source analysis).

---

## Method

### Corpus

6 books across 2 source families, sampled to 447 multi-translator chunks (of 5,777 total chunks in the corpus):

| Source family | Translator | Chunks |
|---|---|---|
| Bhagavad Gita | Edwin Arnold (1885) | 51 |
| Bhagavad Gita | Kâshinâth T. Telang (1882, SBE 8) | 106 (Gita-only portion; Sanatsujâtîya + Anugîtâ excluded) |
| Bhagavad Gita | Swami Swarupananda (1909) | 105 |
| Tao Te Ching | James Legge (1891) | 27 |
| Tao Te Ching | Goddard / Borel (1919) | 82 |
| Tao Te Ching | Suzuki / Carus (1913) | 76 |

Sources: Project Gutenberg (Arnold, Legge) and sacred-texts.com (the other 4) via the extended `fetch_books.py` with `sacred_texts` source-type support added in this commit. All texts public domain; verification by content inspection (translator name appears in fetched HTML) and chapter-count cross-check.

### Analysis

For each pair of chunks (upper-triangle, 5777 × 5777 / 2 = ~16.7M pairs), classify into one of four pair types:

- **W-S-S-T (within-source same-translator):** same book_id (e.g., Arnold-Arnold). Upper bound on similarity from shared source content + shared translator style.
- **W-S-B-T (within-source between-translator):** same source_id, different book_id (e.g., Arnold-Telang on Gita). Tests whether source content survives different translators.
- **X-S-W-T (cross-source within-tradition):** different source_id, same tradition (e.g., Arnold-Gita vs Müller-Upanishads, both advaita). Tests whether tradition convention survives different sources.
- **X-T (cross-tradition):** different tradition. Phase 1a baseline reference.

Mean cosine similarity computed under each mask. Variance decomposition derived: translator-effect = W-S-S-T − W-S-B-T; source-content-effect = W-S-B-T − X-S-W-T; tradition-effect = X-S-W-T − X-T; total = W-S-S-T − X-T; translator-share = translator-effect / total.

Permutation null: shuffle book_id assignments within each source family (preserving the set of book_ids within each source), recompute W-S-B-T, 1,000 permutations.

### Predictions (from pre-registration, committed prior to analysis)

| Quantity | Predicted central value | Predicted range |
|---|---|---|
| W-S-S-T | 0.55 | 0.45-0.65 |
| W-S-B-T | 0.45 | 0.35-0.55 |
| X-S-W-T | 0.32 | 0.25-0.40 |
| X-T | 0.30 | 0.25-0.35 |
| Translator effect | +0.08 | +0.04 to +0.12 |
| Tradition+source effect (W-S-B-T − X-T) | +0.15 | +0.10 to +0.25 |
| Translator share | 0.30 | 0.20 to 0.40 |

---

## Observed results

```
pair_type     mean_cos      n_pairs       description
W_S_S_T       0.6683         18,822       within-source same-translator (upper bound)
W_S_B_T       0.6236         32,389       within-source between-translator (target)
X_S_W_T       0.5341      2,341,136       cross-source within-tradition (intermediate)
X_T           0.4393     14,291,629       cross-tradition (Phase 1a reference)

Translator effect (W-S-S-T - W-S-B-T):     +0.0447
Source/content effect (W-S-B-T - X-S-W-T): +0.0895
Tradition effect (X-S-W-T - X-T):          +0.0948
Total variance (W-S-S-T - X-T):            +0.2291
Translator share of total:                  19.5%
```

Permutation test (1,000 perms, seed=0):
- Observed W-S-B-T: 0.6236
- Null mean: 0.6397 (sd 0.0009)
- p (one-sided observed >= null): 1.0000
- z-score of observed relative to null: ≈ −17.9
- p (one-sided observed < null): << 0.0001

---

## Predicted vs observed: full transparent comparison

| Quantity | Predicted (range) | Observed | Verdict |
|---|---|---|---|
| W-S-S-T | 0.55 (0.45-0.65) | **0.6683** | Outside range (above) — calibration error |
| W-S-B-T | 0.45 (0.35-0.55) | **0.6236** | Outside range (above) — calibration error |
| X-S-W-T | 0.32 (0.25-0.40) | **0.5341** | Outside range (above) — calibration error |
| X-T | 0.30 (0.25-0.35) | **0.4393** | Outside range (above) — calibration error |
| Translator effect | +0.08 (+0.04 to +0.12) | **+0.0447** | Inside range (low end) |
| Tradition+source effect | +0.15 (+0.10 to +0.25) | **+0.1843** | Inside range |
| Translator share | 0.30 (0.20-0.40) | **0.195** | Just below range — confirms direction; even stronger than predicted |

### H1b.1 (variance ordering): CONFIRMED

The pre-registered ordering W-S-S-T > W-S-B-T > X-S-W-T > X-T holds exactly: 0.6683 > 0.6236 > 0.5341 > 0.4393. Each successive step represents one additional source of variance being introduced (translator → source content → tradition).

### H1b.2 (translator-bound): CONFIRMED, stronger than predicted

Pre-registered: translator share < 35%. Observed: **19.5%**. The translator effect is not just bounded; it is substantially smaller than predicted, accounting for roughly one-fifth of total within/cross-tradition variance. Source-content effect (~39%) and tradition effect (~41%) are each approximately twice as large.

### H1b.3 (permutation null direction): REFUTED in pre-registered direction; INFORMATIVELY supported in opposite direction

The pre-registration specified: "the observed W-S-B-T value exceeds the permutation null mean (translator labels randomly reassigned within source family) at p < 0.05 one-sided." This prediction is refuted in its specified direction (p = 1.0).

The pre-registration got the direction of the permutation test backwards, for a methodologically interesting reason that the test itself surfaces:

- The permutation shuffles book_id labels within each source family.
- After shuffling, "between-translator" pairs include some pairs that are *really* same-translator but mislabeled as between-translator.
- Same-translator pairs are *more* similar than between-translator pairs (we directly observe this in W-S-S-T > W-S-B-T).
- So shuffled "between-translator" pairs have a *higher* mean than real between-translator pairs.

The correct direction of the test is therefore: real W-S-B-T < null mean = translator labels are non-random = translators produce statistically distinct styles. The observed z-score of −17.9 (observed 0.0161 cosines below null) is overwhelming evidence that translators *do* impose detectable stylistic conventions on shared source content. This is consistent with the H1b.1 and H1b.2 findings (translator effect is real but bounded).

The directional error in the pre-registration is itself a small methodological object lesson, retained transparently rather than silently revised: pre-registration discipline does not only catch post-hoc fitting; it also catches researcher misunderstanding of what their own permutation null actually compares. Had H1b.3 not been pre-registered, the reformulated test would have been reported without acknowledging the original directionality confusion, which would have hidden a real reasoning error.

### Absolute magnitudes: PARTIALLY REFUTED (calibration error)

All four pre-registered absolute cosine values were systematically below the observed values. MiniLM-L6-v2 produces tighter cosines than the author anticipated for short multi-paragraph chunks. The *ratios* and *ordering* of the predictions were correct; the *absolute calibration* was not.

This carries a methodology lesson worth surfacing in the paper: **CCB results should be reported in relative terms (effect sizes, variance partitions, ordering) rather than absolute cosines.** Absolute cosine values are embedding-model-specific and corpus-character-specific; relative differences are what generalize across models and corpora. Cross-model replicability of *binding magnitude differences* is what makes CCB defensible; cross-model replicability of *absolute cosines* is not the right benchmark.

---

## Per-source breakdown

### Bhagavad Gita

| Pair type | Pair | Mean cos | n |
|---|---|---|---|
| Same translator | Arnold-Arnold | 0.6990 | 1,275 |
| Same translator | Swarupananda-Swarupananda | 0.6672 | 5,460 |
| Same translator | Telang-Telang | 0.6104 | 5,565 |
| Between translator | Arnold ↔ Swarupananda | 0.6262 | 5,355 |
| Between translator | Arnold ↔ Telang | **0.5862** (lowest within Gita) | 5,406 |
| Between translator | Swarupananda ↔ Telang | 0.6267 | 11,130 |

The Arnold-Telang gap (0.586) is the widest within-source between-translator divergence in the entire experiment. Arnold's verse adaptation and Telang's SBE academic prose are stylistically very different; Telang and Swarupananda are both prose but with different theological frames (Indological vs. Vedantic); Arnold and Swarupananda interestingly cluster more tightly (both more accessible English styles) than Arnold and Telang.

### Tao Te Ching

| Pair type | Pair | Mean cos | n |
|---|---|---|---|
| Same translator | Carus-Carus | 0.7460 | 2,850 |
| Same translator | Legge-Legge | 0.7465 | 351 |
| Same translator | Goddard-Goddard | 0.6808 | 3,321 |
| Between translator | Carus ↔ Goddard | 0.6490 | 6,232 |
| Between translator | Carus ↔ Legge | 0.6214 | 2,052 |
| Between translator | Goddard ↔ Legge | 0.6242 | 2,214 |

TTC translations cluster tightly (all between-translator means ~0.62-0.65), reflecting the aphoristic, short-chapter structure of the source — there's less room for translator divergence when each unit is 4-8 lines. The translator effect on TTC (W-S-S-T median 0.72 − W-S-B-T median 0.63 = 0.09) is slightly larger than on Gita (0.66 − 0.61 = 0.05), but in absolute terms both are bounded.

---

## What this means for the paper

### §9 limitation 1 update

Previously (Draft 5): "Translator-as-confound (§5). All passages English-translated by a small set of anglophone scholar-translators. The largest single unaddressed threat to validity in the present application."

Draft 6 should read approximately: "Translator-as-confound (§5). All passages English-translated by anglophone scholar-translators. Phase 1b tested the *between-translator* component of this confound on two multi-source families (3 translators each of Bhagavad Gita and Tao Te Ching) and found it bounded at 19.5% of total within/cross-tradition variance (§6.9). The complementary *within-anglophone-tradition shared-consensus* component remains unaddressed and is the target of Phase 1c (multilingual source analysis on Sanskrit / Pali / Chinese / Tibetan / Greek / Arabic / Hebrew originals)."

### New §6.9 Phase 1b section

Adds the variance decomposition methodology and result, the prediction-vs-observed table, the H1b.3 directional error transparency, and the calibration error methodology lesson.

### Abstract update

Add one sentence: "Phase 1b extends Phase 1a with multi-translator coverage of two source families and partitions cosine similarity variance into translator (~20%), source-content (~39%), and tradition (~41%) components; the cross-tradition CCB signal is not primarily a translator artifact."

### §8 methodology lesson

Add: "Report CCB results in relative terms (effect sizes, variance partitions, ordering) rather than absolute cosines. Absolute cosine values depend on the embedding model and corpus character; relative differences are what generalize."

### §10 Phase 1 priorities reordering

Phase 1b completes priority 1 (multi-translator). Phase 1c priorities, in order:
1. Non-English source analysis with multilingual embeddings (the deepest defense against the *broad* constructivist objection — anglophone-scholar-tradition uniformity).
2. Modern computational + bridge thinkers on verified text (closes the §10 priority 3 gap for the canonical three-cluster Phase 0 finding).
3. Adversarial passage selection by a constructivist-leaning scholar.
4. Held-out human-validated concept tagging on a randomly sampled subset.
5. Formal OSF preregistration if access is restored, or continued public-Git + Zenodo + OpenTimestamps pre-registration mechanism for Phase 1c.

---

## What we have NOT shown

The translator effect we measured (~20% of variance) is the variance *between individual anglophone translators*. It does not measure:

1. **Shared-anglophone-scholar conformity.** Western academic / theosophical / Sanskritist conventions that all our translators inherit. A century of mutual citation may have imposed a tradition-wide structural template on how Hindu / Buddhist / Daoist texts are rendered in English. Phase 1b's between-translator test is blind to this.

2. **Source-text editorial selection.** Different translators may render different recensions of the source text. The Telang SBE 8 Gita is one critical edition; Arnold's source was likely a different Sanskrit edition. Phase 1b treats source-content as fixed, but in practice it varies slightly.

3. **Concept-conditional binding directly.** Phase 1b reports overall mean cosine similarities, not concept-conditional CCB. A natural follow-up is to compute concept-conditional CCB restricted to within-source between-translator pairs, then compare to cross-tradition CCB. This is straightforward with the existing infrastructure and may be added in a Phase 1b.1 update.

4. **Robustness to embedding model choice.** Phase 1b uses ONNX MiniLM only. The Draft 5 cross-model claim (OpenAI text-embedding-3-large agrees with MiniLM on Phase 1a) does not automatically extend to Phase 1b. Cross-model replication for Phase 1b is straightforward to add and should be a follow-up.

These are not paper-killing limitations — they are the natural next questions, and are documented honestly so the reader can calibrate.

---

## Reproducibility

```bash
# From repo root:
python scripts/phase1b_within_source_variance.py \
  --chunks corpus/chunks.jsonl \
  --backend onnx \
  --model sentence-transformers/all-MiniLM-L6-v2 \
  --out results/phase1b/within_source_variance.json
```

Expected runtime: ~8 minutes on CPU (ONNX embedding of 5,777 chunks). Cache at `results/phase1b/embeddings.npy` reuses on re-run. Results bit-exact reproducible with seed=0.

---

*This document reports the Phase 1b experimental results transparently against the pre-registration. Predictions that were refuted or refined are reported as such, not silently revised.*
