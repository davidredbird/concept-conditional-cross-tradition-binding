# Phase 2a Stage-1: language representation-quality screen

**Date:** 2026-05-20
**Script:** `scripts/phase2a_representation_screen.py`
**Aggregate output (committed):** `results/phase2a/representation_screen.json`
**Source data (local-only, gitignored):** `corpus/flores/dev_*.jsonl` (FLORES+ dev, 997 parallel sentences/language)

## Purpose

Before paying for a full within-language concept-binding gate on each candidate
translation-target language, screen them cheaply for representation quality, to
(a) rule out any language too poorly represented to trust, and (b) build the
continuous *representation-quality covariate* the westernization triangulation
needs (β₂ in the covariate-adjustment decomposition; see `phase2a-design-sketch.md` §3c).

Candidates screened (user's list): english, modern_chinese (cmn_Hans), hindi,
japanese, french, spanish, german, korean, hebrew, arabic, persian, plus
**sanskrit (san_Deva) as a known-FAIL calibration anchor** (within-language
concept gate: 2/7). Classical Chinese and Pali are not FLORES+ languages, but we
already hold direct gate ground-truth for both (法句經 passed 6/7; Pali failed
alongside Sanskrit), so they need no proxy.

## Method

Two metrics with deliberately different contamination profiles, on the same 997
professionally-translated parallel sentences (semantic content held constant):

1. **Tokenizer fertility — PRIMARY, contamination-immune.** Mean subword tokens
   per parallel sentence, per model tokenizer (XLM-R for e5-large; BERT-multilingual
   WordPiece for LaBSE). More tokens for the *same content* = poorer vocabulary
   coverage. Depends only on the learned tokenizer vocabulary, never on whether
   the model saw FLORES — immune to evaluation contamination. Reported as a ratio
   vs English (relative ranking only).

2. **Cross-lingual retrieval P@1 / MRR — SECONDARY, contamination-susceptible.**
   For each lang-X sentence, retrieve nearest English sentence; score the rank of
   the true translation. Directly measures cross-lingual semantic alignment but is
   OPTIMISTIC if FLORES leaked into pretraining.

**Compliance:** FLORES+ text read only from the gitignored cache; only aggregate
per-language numbers written to `results/`. No FLORES sentence is ever emitted.

## Results

### Fertility (tokens/sentence, ratio vs English; lower = better coverage)

| language | e5 ratio | LaBSE ratio |
|---|---|---|
| modern_chinese | **0.98** | 1.50 |
| english (baseline) | 1.00 | 1.00 |
| japanese | 1.11 | 1.53 |
| persian | 1.11 | 1.16 |
| hebrew | 1.13 | 1.16 |
| korean | 1.16 | 1.16 |
| german | 1.17 | 1.21 |
| arabic | 1.18 | 1.22 |
| spanish | 1.20 | 1.24 |
| hindi | 1.26 | 1.31 |
| french | 1.29 | 1.29 |
| **sanskrit (FAIL anchor)** | **1.44** | **1.78** |

### Retrieval P@1 (X → English)

All 11 modern candidates score 0.995–1.000 under e5 and **1.000** under LaBSE.
Sanskrit is the only language below ceiling: **e5 0.944, LaBSE 0.989**.

## Interpretation — two failure modes, one conclusion

**The single calibration anchor lands correctly in both metrics.** Sanskrit is
worst on fertility (both models) and lowest on retrieval (both models), matching
its gate failure. So both proxies do detect genuine Sanskrit-class under-resourcing.

**But neither proxy discriminates among the well-resourced moderns, for opposite reasons:**

- **Fertility is non-monotonic with representation quality.** French (1.29 in e5)
  ranks *worse* than Chinese (0.98) and near the bottom of the modern pack — yet
  French is obviously well-represented. Raw cross-script fertility conflates
  "this language uses more tokens per proposition / its script packs less per
  token" with "the tokenizer under-covers it." The decisive case: modern Chinese
  has the **worst** modern-language fertility under LaBSE (1.50) — but Classical
  Chinese **passed the LaBSE concept gate 6/7**. High fertility coexists with
  gate-pass. Fertility-as-eligibility-gate would wrongly disqualify Chinese.

- **Retrieval is ceiling-saturated.** Dynamic range is 0.944→1.000 (e5) and
  0.989→1.000 (LaBSE) — no usable separation. Sentence-level parallel retrieval
  is simply too easy: distinctive sentences get matched even in a language whose
  *concept structure* the model cannot resolve. For LaBSE this is doubly
  uninformative — bitext retrieval *is* LaBSE's training objective, so P@1≈1.0 is
  guaranteed by construction and says nothing about concept resolution.

**Core result — the proxies are necessary-but-not-sufficient.** Sanskrit posts
0.944 retrieval and only moderately-bad fertility, yet fails the concept-binding
gate 2/7. That gap *is* the finding: tokenizer coverage and sentence-matching do
not imply the model resolves cross-tradition *concept* structure in a language.
**The screen can rule a language OUT (fails both floors → hopeless) but cannot
rule one IN.** Eligibility for the triangulation must be decided by the actual
within-language concept-binding gate — it is irreducible, not shortcuttable by a
cheap proxy. This kills the tempting "just screen by fertility/retrieval" shortcut
and belongs in the paper's methods limitations.

## Operational consequences

1. **No modern candidate is ruled out.** All 11 clear the Sanskrit floor on both
   metrics under both models. So the screen excludes nothing here; it only
   confirms none are in Sanskrit-class under-resourcing.

2. **Eligibility = run the within-language concept gate** on each modern language
   we actually want to use, prioritized by what we can source. The screen does
   not replace it.

3. **Fertility becomes the representation-quality covariate (β₂).** It is the
   contamination-immune, continuous, all-FLORES-language metric the triangulation
   decomposition needs. Retrieval is too saturated to serve as a continuous
   regressor and is dropped to a reported-but-unused diagnostic.

## Caveats

- Cross-script fertility is not absolutely comparable; used as relative ranking
  and as a covariate, not as a hard threshold.
- Retrieval is contamination-susceptible and, for LaBSE, confounded with its
  training objective; reported for completeness only.
- FLORES+ license: text kept local; only these aggregate numbers are committed.
  If retrieval is ever cited, caveat possible training-set contamination.

## Next

- Source + gate the highest-value modern languages for the
  Advaita-vs-Theravada-vs-Daoist triangulation (Hindi sourcing still the blocker).
- Run the first cross-tradition CCB in a gate-passing language (Classical Chinese
  法句經 Buddhist vs Daoist TTC) — runnable now with existing data.
- Fold β₂ = fertility-ratio into the `phase2a-design-sketch.md` decomposition spec.
