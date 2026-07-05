# Phase 3a — RSA SNR sizing: can the model-robust instrument be powered?

**Date:** 2026-05-30  **Status:** pre-registration prep, firewall-safe (Phase 2c originals
only; no embedding/CCB/RSA on the sealed Plato…Zhuxi Axial gradient). Closes the open
"power analysis → cell sizes" item from `phase3a-design.md` §9 for the **RSA** instrument
(the CCB power analysis in `phase3a-instrument-tests.md` §1 is superseded as the binding
constraint, since the instrument pivoted to RSA).

## Why this run

`phase3a-instrument-tests.md` established that the **only model-robust, alignment-free
instrument** is the holistic RSA isomorphism (within-language concept-geometry RDMs,
correlated across traditions; LaBSE↔OpenAI r=0.79), and that per-concept attribution is
sample-size-confounded and must NOT be pre-registered. The equal-N control (§4c) showed the
isomorphism collapsing from ~0.4 (full, unequal n) to ~0.02 at n=8/concept. That left the
sizing question open: **at what per-concept n does the model-robust isomorphism become a
reliable, powered signal — and can the corpus deliver it, especially on the independent
China×Greece cells?** Two SNR curves answer it: chunk-level (both models) and sentence-level
(LaBSE; the proposed power lever).

Grid: 5 concepts {SUBSTRATE, AWARENESS, ULTIMATE, WORLD, SELF} × 5 languages
{classical_chinese, arabic, greek, hindi, spanish}. Rarer concepts (NONSEP, RECOGNITION) and
the smallest language (Hebrew) dropped so cells are large enough to subsample. Every cell
subsampled to common n, RDMs built, mean cross-language isomorphism, bootstrapped.

## Results

### Chunk-level equal-N curve (`phase3a_rsa_snr.py`)

Min cell = 65 (spanish × SELF) — the curve is **data-limited at n=65**; neither model has
plateaued in a way that reaches the full-n value.

| n/concept | LaBSE iso | OpenAI iso |
|---|---|---|
| 8  | +0.004 | −0.019 |
| 12 | −0.012 | +0.020 |
| 20 | −0.014 | +0.018 |
| 35 | +0.028 | +0.045 |
| 60 | +0.027 | +0.061 |
| 65 | +0.022 | +0.061 |

- **LaBSE never leaves the noise floor** (~+0.02, flat — no monotone trend with n).
- **OpenAI rises to ~+0.06 and plateaus** by n≈60.
- Both are **far below the full-n prototype** (+0.392 LaBSE / +0.435 OpenAI, null p .03–.05).

### Sentence-level equal-N curve (`phase3a_rsa_snr_sentence.py`)

33,861 sentences from the Phase 2c originals → 14,550 tagged with ≥1 of the 5 concepts.
**Per-cell minimum only rose 65 → 74** (still spanish × SELF): sentence segmentation does
**not** multiply the binding cell, because the bottleneck is a rare concept in a small
language, not total unit count.

| n_sent/concept | LaBSE iso |
|---|---|
| 20 | −0.024 |
| 50 | −0.064 |
| 74 | −0.064 |

Sentence-level isomorphism is **at or below zero** at every reachable n — shorter units give
**noisier centroids** at fixed n, so the proposed power lever degrades the signal rather than
recovering it.

## Interpretation — what this means for Phase 3a power

1. **Sentence-level is not the power lever.** The "≈5–6× more units" assumption
   (`phase3a-instrument-tests.md` §1, `phase3a-design.md`) is false for this estimator: the
   binding constraint is the *rarest concept × smallest tradition* cell, which sentence
   splitting barely changes, and finer granularity hurts centroid quality. Cross it off the
   list of mitigations.

2. **The full-n ~0.4 isomorphism is carried by the high-prevalence concepts.** At controlled
   equal n it does not reproduce within reachable sample sizes (≤65–74). The signal lives in
   AWARENESS/WORLD/ULTIMATE forming stable, consistently-arranged centroids at their natural
   large n — i.e. the concepts that are NOT the distinctively-nondual structural signal. The
   rare, theoretically-interesting concepts (SUBSTRATE/RECOGNITION/NONSEP) are the weak link:
   their centroids are too noisy to contribute reliable RDM structure at any n the corpus
   supplies.

3. **The holistic claim is the only one with a defensible test, and even it is marginal.**
   At full unequal n on the *exploratory* Phase 2c originals, the holistic isomorphism is
   +0.39/+0.44 at null p .03–.05 (K=7). That is the operative measure (a real permutation-
   tested isomorphism), but "marginally significant on the easier data" is a yellow flag for
   the confirmatory test, where (a) the independent China×Greece cells supply *fewer* units
   than the pooled Phase 2c originals used here, and (b) the predicted effect is *smaller*
   (independent traditions < contacted traditions, by the whole premise of 3a).

4. **The model disagreement at equal n is itself informative.** LaBSE sits at the floor while
   OpenAI reaches +0.06 — the cross-model r=0.79 robustness was a *full-n, across-language-
   pair-pattern* property, not a magnitude agreement at controlled n. The robustness claim
   holds for the holistic pattern, not for any equal-N point estimate.

## Target-n curve (`phase3a_rsa_snr_target.py`, added 2026-06-01)

To find the plateau the basic curve couldn't reach, dropped the two smallest languages
(Spanish, Hebrew) and added a **permutation null** (shuffle each language's concept-label
order, recompute isomorphism) at each n. Grid: 5 concepts × 4 languages
{classical_chinese, arabic, greek, hindi}. Per-cell floor rose 65 → **91** (arabic ×
SUBSTRATE). Per-cell counts: Greek is rich (AWARENESS 1085, SELF 1337); Arabic SUBSTRATE=91
and Hindi SUBSTRATE=155 are the binding constraints.

| n/concept | LaBSE iso (p) | OpenAI iso (p) |
|---|---|---|
| 20 | +0.017 (.385) | +0.065 (.250) |
| 35 | +0.066 (.330) | +0.128 (.235) |
| 60 | +0.123 (.170) | +0.168 (.150) |
| 91 | +0.161 (.155) | +0.224 (**.085**) |

**Findings:**
- The isomorphism is genuinely **n-dependent and rises monotonically** on both models — the
  signal is real, not an artifact, and the equal-N "floor" in the 5-language run was a
  symptom of the n=65 cap, not absence of signal.
- **It does not clear the permutation null even at n=91** (best is OpenAI p=.085). Linear
  extrapolation of the trend puts p<.05 at roughly **n≈150–250 per concept per tradition**;
  the curve has not plateaued, so this is a floor on the target, not the target itself.
- **OpenAI dominates LaBSE for RSA** at every n (higher iso, lower p) — consistent with
  `phase3a-instrument-tests.md` §4. OpenAI should be the primary RSA model; LaBSE the
  corroborator.
- **The binding constraint is the rarest concept (SUBSTRATE) in the lowest-prevalence
  tradition** (Arabic 91, Hindi 155). Corpus sizing is set by this cell, not the mean.

### The deeper structural problem this exposes: systems-count, not just n

The Phase 2c grid pools **4–5 languages** → 6–10 pairwise RDM correlations to average, which
is what makes even n=91 reach p=.085. But the **confirmatory China×Greece test, if spheres
are treated as monolithic, is a SINGLE pairwise RDM correlation** (China-geometry vs
Greece-geometry) — a Spearman over 10 points (K=5) with a 5!=120-arrangement null. That is
drastically lower-powered than the Phase 2c pooled grid that already only reaches p=.085.

RSA power scales with **both** per-centroid n **and** number-of-systems. The instrument-tests
lever "use more *systems* (per-tradition RDMs)" is therefore not optional — it is the only way
the confirmatory test gets enough pairwise correlations to have a null worth testing against.
**Corpus expansion must multiply systems, not just volume:** decompose each sphere into its
schools (China: Daoist / Confucian / Buddhist / Neo-Confucian; Greece: Platonist /
Aristotelian / Stoic / Neoplatonist), each as its own RDM, each with ≥ target-n per concept.
The age-gradient already supplies era-replication; the school-decomposition supplies
within-sphere systems. Together they turn a 2-system test into a many-system one.

## Consequences for the pre-registration

- **Power section must state the constraint honestly:** holistic RSA at **full unequal n,
  pooled-primary**, with the **age-gradient and any per-concept readout pre-declared
  underpowered / exploratory-within-confirmatory** — not co-primary. The gradient cells are
  smaller than the pooled Phase 2c grid that already only reaches marginal significance.
- **Sentence-level removed** as a power mitigation in the design.
- **Open corpus-sizing question is now sharper, not closed:** the operative lever is total
  *high-prevalence-concept* n per tradition at chunk level. Before freezing predictions we
  need the independent-cell chunk counts per concept (firewall-gated — it requires
  prevalence-screening the Axial corpus, which is pre-reg execution step 1) OR a defensible
  argument from the contacted-era Greek/Chinese counts already in hand (Greek nondual ~6,455,
  Chinese nondual ~3,376 chunks; `phase3a-instrument-tests.md` §1) that the *pooled* cell
  clears the n the high-prevalence concepts need (≳hundreds/concept). The age-gradient
  per-cell (Plato ~1,263 × Daoist ~931) almost certainly does not.
- **Decision (David, 2026-06-01): enlarge the independent corpus before pre-reg** (option b),
  preserving the gradient discriminator that motivates 3a. The target-n curve makes this
  concrete and two-dimensional:
  1. **Per-centroal n target ≥ 150–250 chunks/concept/tradition** (floor; curve unplateaued),
     binding on the **rarest concept (SUBSTRATE) in the lowest-prevalence tradition**. At
     SUBSTRATE prevalence ~0.2–0.5 that is ~300–1,250 total chunks/tradition — and more for
     low-SUBSTRATE-prevalence traditions. Verify against actual Axial-cell prevalence at
     prevalence-screen time (gated).
  2. **Multiply systems** by decomposing each sphere into schools (≥3–4 per sphere), each its
     own RDM at target-n — without this the core China×Greece comparison is a single
     underpowered RDM correlation.
  An achievable interim check: re-run the target-n curve at the *enlarged* corpus to confirm
  the isomorphism plateaus and clears p<.05 before committing predictions.
- **Earlier a/c options recorded for the trail:** (a) pooled holistic-only (drops the
  gradient/discriminator — rejected); (c) powered descriptive measurement + deferred
  discriminator (fallback if enlargement can't reach target-n).

## Scripts
- `scripts/phase3a_rsa_snr.py` — chunk-level, both models
- `scripts/phase3a_rsa_snr_sentence.py` — sentence-level, LaBSE
- Inputs: Phase 2c originals (`corpus/chunks_*.jsonl`), LaBSE caches
  (`results/phase2a/*_sentence_transformers__LaBSE.npy`), OpenAI cache
  (`results/phase3a/originals_openai_te3l.npy`), `scripts/harmonized_concepts.py`.
</content>
</invoke>
