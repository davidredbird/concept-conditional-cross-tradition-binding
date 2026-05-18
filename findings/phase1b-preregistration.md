# Phase 1b Pre-registration: Multi-Translator Within-Source Variance Test

**Pre-registration date:** 2026-05-18
**Author:** T. David Kinlaw (Independent Researcher / Redbird Software LLC)
**ORCID:** [0009-0008-5213-1017](https://orcid.org/0009-0008-5213-1017)
**External timestamping mechanisms:**
- Public GitHub commit on this document (timestamp visible on the commit page; controlled by GitHub's infrastructure, not the author)
- Zenodo release `v1.2-prereg-phase1b` cut at the same commit (DOI-resolved third-party timestamp via DataCite)

A third independent timestamp via OpenTimestamps (Bitcoin-blockchain anchored) was attempted but the `ots` CLI failed on the local Windows environment due to a `libsecp256k1` loading issue in `python-bitcoinlib`. The web-based OpenTimestamps interface at opentimestamps.org remains available to any independent verifier wishing to add a third timestamp post-publication. The GitHub + Zenodo combination is the binding pre-registration timestamp for this experiment.

**Status:** Pre-registered prior to running any Phase 1b analysis. The corpus has been fetched, cleaned, chunked, and the analysis script (`scripts/phase1b_within_source_variance.py`) has been authored, but the analysis has not yet been executed against the embeddings.

---

## 1. Background and motivation

The §9 limitations of the Draft 5 paper identify translator-as-confound as the largest unaddressed threat to validity in the Phase 1a application of CCB to the mysticism convergence debate. Every Phase 1a passage was English-translated by one of a small set of anglophone scholar-translators, and cross-tradition convergence in semantic embedding space could in principle reflect *shared anglophone-translation convention* rather than *shared source content*.

Phase 1b adds multi-translator coverage of two source families (Bhagavad Gita and Tao Te Ching, three translators each) and runs a within-source between-translator variance test. The test partially defends the Phase 1a results against the translator-as-confound critique, *to the extent that translator variance is bounded relative to cross-tradition variance*.

This pre-registration is a methodology-paper demonstration of CCB applied with proper a-priori commitment to predictions, addressing the load-bearing critique of the §6.8 pre-specification framing in the existing draft. The §6.8 pre-specification was written into Draft 4 of the paper before Draft 5 results were run, but the public repository was rebuilt with a single initial commit and does not externally timestamp the prediction-before-result ordering. Phase 1b corrects this by externally timestamping the predictions via public Git, Zenodo DOI, and OpenTimestamps anchor — three independent layers, the third of which is cryptographically uncontestable.

## 2. Hypotheses

**H1b.1 (Variance ordering).** Mean pairwise cosine similarity decreases monotonically across the four pair types:

    W-S-S-T > W-S-B-T > X-S-W-T > X-T

where:
- W-S-S-T = within-source same-translator (same book_id, upper-tri pairs)
- W-S-B-T = within-source between-translator (same source_id, different book_id)
- X-S-W-T = cross-source within-tradition (different source_id, same tradition)
- X-T = cross-tradition (different tradition)

**H1b.2 (Translator-bound).** The translator share of total within/across-tradition variance is bounded below 35%:

    (W-S-S-T - W-S-B-T) / (W-S-S-T - X-T) < 0.35

This formalizes "translator-as-confound is bounded": even on the same source text, different translators produce passages that cluster much closer to the same-translator ceiling than to the cross-tradition floor.

**H1b.3 (Permutation null rejection).** The observed W-S-B-T value exceeds the permutation null mean (translator labels randomly reassigned within source family) at *p* < 0.05 one-sided. I.e., between-translator passages cluster more tightly than chance would predict.

## 3. Pre-specified corpus

The Phase 1b corpus consists of 6 books (4 newly added, 2 existing from Phase 1a) organized into 2 multi-translator source families:

### Bhagavad Gita (source_id = "bhagavad_gita")
| Translator | Year | Source | Notes |
|---|---|---|---|
| Edwin Arnold | 1885 | Project Gutenberg 2388 | Phase 1a (already in chunks.jsonl) |
| Kâshinâth Trimbak Telang | 1882 | sacred-texts.com /hin/sbe08/ | SBE vol 8. Gita portion only (chars 0-259,683); Sanatsujâtîya + Anugîtâ deferred to Phase 1c |
| Swami Swarupananda | 1909 | sacred-texts.com /hin/sbg/ | Vedantic commentary |

### Tao Te Ching (source_id = "tao_te_ching")
| Translator | Year | Source | Notes |
|---|---|---|---|
| James Legge | 1891 | Project Gutenberg 216 | Phase 1a (already in chunks.jsonl) |
| Dwight Goddard & Henri Borel | 1919 | sacred-texts.com /tao/ltw/ | Contemplative-Western reading |
| D.T. Suzuki & Paul Carus | 1913 | sacred-texts.com /tao/crv/ | Zen-influenced reading |

The remaining 33 single-translator books in `corpus/books_manifest.json` participate in X-S-W-T and X-T comparisons but not W-S-S-T or W-S-B-T.

### Chunk counts (after filtering Telang to Gita-only)

| Source | Translator | Chunks |
|---|---|---|
| Bhagavad Gita | Arnold | 51 |
| Bhagavad Gita | Telang | 106 |
| Bhagavad Gita | Swarupananda | 105 |
| Tao Te Ching | Legge | 27 |
| Tao Te Ching | Goddard | 82 |
| Tao Te Ching | Carus | 76 |

Total multi-translator chunks: 447 across 6 books. Total chunks in `corpus/chunks.jsonl`: 5,777.

## 4. Pre-specified analysis

Analysis script: `scripts/phase1b_within_source_variance.py` (authored at this commit, executed *after* this pre-registration is committed and externally timestamped).

Pipeline:
1. Load `corpus/chunks.jsonl` (all 5,777 chunks).
2. Embed every chunk with `sentence-transformers/all-MiniLM-L6-v2` via ONNX Runtime (`scripts/onnx_embedder.py`). Unit-normalize.
3. Compute the full 5777 × 5777 pairwise cosine similarity matrix.
4. Build four boolean pair-type masks (upper-triangle only): `W_S_S_T`, `W_S_B_T`, `X_S_W_T`, `X_T`.
5. Compute mean cosine under each mask.
6. Compute variance-decomposition derived quantities (translator-effect, source-content-effect, tradition-effect, total-variance, translator-share-of-total).
7. Permutation test on translator labels: shuffle book_id within each source family, recompute W-S-B-T, accumulate null distribution over 1,000 permutations.
8. Per-source breakdown: same-translator-within-source and between-translator-within-source means for each pair within each source family.
9. Output to `results/phase1b/within_source_variance.json`.

Random seed: 0. Permutation count: 1,000.

## 5. Pre-specified predicted outcomes

Specific predictions made before running the analysis:

| Quantity | Predicted | Range |
|---|---|---|
| W-S-S-T (same-translator within source) | 0.55 | 0.45-0.65 |
| W-S-B-T (between-translator within source) | 0.45 | 0.35-0.55 |
| X-S-W-T (cross-source within tradition) | 0.32 | 0.25-0.40 |
| X-T (cross-tradition, Phase 1a baseline) | 0.30 | 0.25-0.35 |
| Translator effect (W-S-S-T − W-S-B-T) | +0.08 | +0.04 to +0.12 |
| Tradition+source effect (W-S-B-T − X-T) | +0.15 | +0.10 to +0.25 |
| Translator share of total (translator-effect / total-variance) | 0.30 | 0.20 to 0.40 |

The Phase 1a baseline X-T for the embedding model used (ONNX MiniLM) is approximately 0.30 from earlier sentence-level analysis; this prediction is therefore well-anchored.

The W-S-S-T prediction is anchored by the intuition that multiple passages from the same translator on the same source share both vocabulary register and source content. The W-S-B-T prediction reflects loss of translator-specific register but preservation of source content semantics. The X-S-W-T prediction reflects loss of specific source semantics but preservation of tradition-vocabulary correlations. The X-T prediction is the existing Phase 1a measurement.

## 6. Decision rules

**Primary decision: is translator-as-confound bounded?**

- **Supported** if H1b.2 holds (translator share < 35%) AND H1b.1 holds (ordering preserved).
- **Refuted** if translator share > 60% OR if W-S-B-T ≤ X-T (translators do not preserve more than tradition convention).
- **Inconclusive** if 35% < translator share < 60%, with explicit decision on what additional Phase 1c work would resolve.

**Secondary decision: does the §6.9 Phase 1b section update the §9 limitation 1 framing?**

- **Strengthen the paper** if H1b.2 holds: §9 limitation 1 changes from "unaddressed" to "partially defended; translator share bounded at <35% on two source families." Methodology paper position is strengthened.
- **Qualify the paper** if H1b.2 fails: §9 limitation 1 changes from "unaddressed" to "tested and found substantial; translator-as-confound likely accounts for a large fraction of cross-tradition signal." Methodology paper still stands (the test mechanism worked), but the mysticism application result requires major qualification.

Both outcomes are publishable. The paper's framing is methodology-first; the test mechanism (CCB with within-source variance partialled out) demonstrates its purpose regardless of whether the result is favorable to the existing Phase 1a finding.

## 7. Anticipated failure modes

Named in advance, so they can be reported transparently if they occur:

1. **Underpowered permutation test.** Only 6 multi-translator books across 2 source families. The permutation null might be too narrow to give meaningful p-values. If observed, report as inconclusive and recommend Phase 1c with more source families.
2. **Source content confound on Telang's Gita portion.** Telang's SBE 8 includes commentary; Arnold's is just verse. Even after filtering Telang to chars 0-259,683, the chunk count imbalance (51 Arnold / 106 Telang / 105 Swarupananda) reflects more commentary in Telang and Swarupananda than in Arnold. Variance-decomposition results might be sensitive to this. Reported transparently.
3. **Vocabulary-breadth interaction with Phase 1b.** The §6.8 vocabulary-breadth-as-noise-floor mechanism could interact with within-source variance: technical-only vocabulary might be more conserved across translators than common-English vocabulary. Not directly tested in Phase 1b; flagged for Phase 1c follow-up.
4. **OCR / sacred-texts cleaning artifacts.** The new books were fetched from sacred-texts.com (HTML multi-chapter) and cleaned via `clean_books.py` HTML extraction. Quality may differ from PG plaintext (Phase 1a books). If results are anomalous, this confound should be investigated.

## 8. Honest note on the pre-registration mechanism

Pre-registration via timestamped public commits is fundamentally honor-system, augmented by external timestamping. The author commits in good faith to having authored these predictions *before* observing any Phase 1b analysis results. The Bitcoin-anchored OpenTimestamps proof prevents retroactive editing of the predictions after results are observed, but it cannot prove the author did not privately run the analysis before pre-registering. The mechanism's value lies in commitment-to-predictions and prevention-of-post-hoc-revision, not in cryptographic fraud-prevention.

This limitation applies to all pre-registration mechanisms, including OSF and AsPredicted. The author does not have access to OSF for this project, so the public Git + Zenodo DOI combination serves as the external pre-registration mechanism. OpenTimestamps Bitcoin-anchored timestamping was attempted but the toolchain failed in the local Windows environment; the web-based opentimestamps.org service remains available to any verifier wishing to add a third independent timestamp.

## 9. Pre-commitment statement

These hypotheses, predicted outcomes, corpus composition, analysis pipeline, and decision rules are committed to the public repository on this date, prior to executing `scripts/phase1b_within_source_variance.py` against the corpus embeddings. The author commits to reporting outcomes transparently against these predictions, including refutations or null results, in `findings/phase1b-multi-translator.md` and in §6.9 of the next paper draft.

If the predictions are refuted in informative ways, the §6.9 writeup will document this transparently rather than silently revising predictions, mirroring the treatment of the §6.8 ULTIMATE refutation in Draft 5.

---

*This document is the load-bearing pre-registration for Phase 1b. External timestamping is provided by the public GitHub commit on this document and the Zenodo DOI minted for the `v1.2-prereg-phase1b` release at the same commit. The GitHub commit timestamp on this document and on the analysis script `scripts/phase1b_within_source_variance.py` precede any execution of the analysis.*
