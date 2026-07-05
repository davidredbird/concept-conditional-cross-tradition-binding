# Phase 2c -- RSA robustness controls: noise ceiling + arbitrary-word-set baseline

**Date:** 2026-07-05  **Status:** robustness follow-up, firewall-safe (Phase 2c originals
only -- classical_chinese, arabic, greek, hindi, spanish, hebrew; no China x Greece, no
Axial gradient corpus, no new embedding runs). Script: `scripts/phase2c_rsa_controls.py`
(`--control ceiling|baseline|all`, seed=1908). Raw numbers: `results/robustness/rsa_controls.json`.

**Why this exists.** A peer review of the headline cross-language RSA result -- concept
geometry (7 harmonized concepts, K=7 RDM) is moderately isomorphic across independent
linguistic/contemplative traditions, mean isomorphism **+0.392 (LaBSE) / +0.435 (OpenAI)**,
permutation-null p ~= .03-.05 (`phase3a_rsa_recheck.py`, post-hyle-fix) -- flagged that the
number has no instrument ceiling (how much of the *possible* signal is this?) and no
arbitrary-concept-set baseline (would any 7 similarly-prevalent word-groupings show
comparable isomorphism?). Both are computed here. The real isomorphism was recomputed
independently in this script as a sanity check and matches published to 3 decimals
(+0.3916 LaBSE, +0.4345 OpenAI) -- confirms the method transplant is faithful.

## Method recap

Per language, per concept: centroid of tagged-chunk embeddings (harmonized dictionary,
on-the-fly tagging via `harmonized_concepts.tag()`, post Greek-hyle-fix -- the same tagging
`phase3a_rsa_recheck.py` uses). Concept x concept RDM (1 - cosine of centroids) within each
language's own embedding space. Isomorphism = mean Spearman correlation of RDM upper
triangles over all 15 language pairs (6 languages). No cross-lingual alignment of absolute
embeddings ever happens (RSA is alignment-free by construction).

## Control A -- split-half noise ceiling

Per language, per model: split each concept's tagged chunks in half (seed=1908, 100
resamples), build RDM_half1 / RDM_half2, Spearman-correlate the halves, average over
resamples, Spearman-Brown correct (2r/(1+r)) to estimate full-data within-language
reliability.

| language | LaBSE rel (SB) | OpenAI rel (SB) |
|---|---|---|
| classical_chinese | 0.965 | 0.965 |
| hebrew | 0.954 | 0.952 |
| greek | 0.953 | 0.971 |
| arabic | 0.924 | 0.963 |
| hindi | 0.915 | 0.940 |
| spanish | 0.875 | 0.924 |

All six languages show high within-language RDM reliability (0.875-0.971) -- the
instrument itself is not noisy; a given language's concept geometry is stable across
random halves of its own tagged chunks.

**Ceiling** (mean of sqrt(rel_i x rel_j) over the same 15 language pairs used for the
published number):

| model | mean ceiling | published iso | iso / ceiling |
|---|---|---|---|
| LaBSE | 0.931 | +0.392 | **0.421** |
| OpenAI | 0.952 | +0.435 | **0.457** |

**Reading:** the instrument could in principle support isomorphism up to ~0.93-0.95 (if
the true cross-language geometric correspondence were perfect); the observed +0.39/+0.44
recovers **42-46% of that ceiling**. That is a moderate, not saturating, fraction -- the
isomorphism is real headroom-adjusted signal, not an instrument artificially depressed by
noise (the ceiling is high), but it is also nowhere near maximal. This control clears the
"is the instrument too noisy to see anything" worry; it does not by itself say whether
0.42-0.46 of ceiling is a lot or a little in absolute terms -- that's what Control B is for.

## Control B -- arbitrary-word-set RSA baseline

Per language: 50 pseudo-concept-sets, each with 7 pseudo-concepts. A pseudo-concept is a
token set sampled from that language's own chunk text (whitespace tokens length>=3 for
arabic/greek/hindi/spanish/hebrew; single/bigram Han characters for classical_chinese),
greedily grown to match the tagged-chunk count of the *corresponding* real concept (same
slot, same language) within +/-20%, excluding any token overlapping the harmonized
dictionaries (regex cores for Latin-script dicts, normalized substrings for
arabic/hebrew/greek). Hapax tokens (freq=1 in-language) dropped for stability. QC: 2,100
pseudo-concepts built across 50 draws x 6 languages x 7 slots; 99.1% landed within the
+/-20% prevalence tolerance (mean |relative deviation| 0.152, i.e. draws that missed the
window typically sat just outside it). Pseudo-concepts are sampled **independently per
language** -- no cross-language correspondence is constructed for them, unlike the real
concepts.

| model | baseline mean | baseline sd | range | real iso (recomputed) | percentile of real in baseline |
|---|---|---|---|---|---|
| LaBSE | +0.490 | 0.097 | +0.243 .. +0.682 | +0.392 | **14.0** |
| OpenAI | +0.531 | 0.082 | +0.344 .. +0.702 | +0.435 | **12.0** |

**Reading -- and this is the uncomfortable part.** The real, hand-curated 7-concept
isomorphism does **not** exceed the arbitrary-word-set baseline. It sits *below* the
baseline's median in both models (12th-14th percentile out of 50 draws): a randomly
assembled 7-pseudo-concept geometry, matched only for per-language prevalence, typically
produces **higher** cross-language RDM isomorphism than the real contemplative-concept
dictionary does. This is not a marginal miss -- roughly 6 of 7 arbitrary baseline draws
beat the real value.

## Why the baseline comes in this high -- a mechanism, not just a caveat

The task's own design already flags the headline interpretive subtlety (below), but the
result here points at a more specific, testable mechanism: **prevalence-rank confound.**
Pseudo-concept target counts are matched, slot-by-slot, to the real concepts' per-language
prevalence -- and prevalence rank order is fairly consistent across languages for reasons
that have nothing to do with word meaning (e.g. ULTIMATE/AWARENESS are the most-tagged
concepts and NONSEP/RECOGNITION the least-tagged in nearly every one of the six languages,
because scripture-adjacent devotional/philosophical prose talks about the divine and the
mind far more often than it talks explicitly about non-duality). A centroid built from
averaging N chunks has residual noise that shrinks with N; concepts with small N (in every
language, by construction) will therefore sit systematically farther from the corpus mean
than concepts with large N, in *every* language, independent of content. Because the
pseudo-concepts inherit the real concepts' per-language sample-size ranks, their RDMs can
reproduce a chunk of the real geometry's cross-language correlation purely through this
shared noise-magnitude fingerprint, with zero semantic correspondence built in. This would
explain why arbitrary word-sets match or beat the real signal: the baseline is not a clean
"meaningless words" null, it is a "meaningless words at matched sample-size-noise
structure" null, and that structure alone appears to carry a substantial share of what
RSA is picking up. This mechanism is a natural next thing to isolate (e.g. an equal-N
version of Control B, or reshuffling prevalence ranks across languages independently of
the real concepts) but was not run here -- flagged as follow-up, not resolved.

## The interpretive subtlety, stated plainly (per the pre-registration instruction)

The real concepts carry an **investigator-made cross-language correspondence**: the
harmonized dictionary asserts, by construction, that "AWARENESS" in classical Chinese
picks out the same latent thing as "AWARENESS" in Greek, Arabic, Hindi, Spanish, and
Hebrew. The pseudo-concepts deliberately carry **no such correspondence** -- slot 3 in
Greek and slot 3 in Hindi share nothing except that both were built to hit a similar chunk
count in their own language. So Control B tests "hand-matched semantic correspondence +
whatever geometric structure that correspondence produces" against "no correspondence, same
prevalence profile." A real value that beat the baseline decisively would not, by itself,
prove that the *geometry* (as opposed to the *correspondence itself*, or the shared
prevalence-noise structure above) is what's doing the work. Here the real value does not
even clear that bar in the first place, which is the more serious problem: it says the
investigator-made correspondence, at current N, is not obviously buying anything over an
arbitrary same-prevalence grouping, on this particular test.

## Bottom line

- **Ceiling (Control A):** the instrument is not noise-limited. Per-language reliability is
  high (0.88-0.97 both models); the published isomorphism recovers 42% (LaBSE) / 46%
  (OpenAI) of the achievable ceiling. This part of the review is answered cleanly.
- **Baseline (Control B):** the published isomorphism does **not** clear an arbitrary
  prevalence-matched word-set null -- it falls at the 12th-14th percentile, i.e. below the
  baseline median in both models. This is a genuine negative result for the strong reading
  of the RSA headline ("contemplative concept geometry is specially isomorphic across
  independent traditions"). The weaker reading survives -- *some* geometric correlation
  across languages exists and is not zero (Control A shows it's real signal relative to
  measurement noise, and the earlier permutation-null test in `phase3a_rsa_recheck.py`
  rejects pure chance at p~.03-.05) -- but this baseline shows that signal is not
  distinguishable from what any similarly-sized, similarly-prevalent arbitrary word
  grouping produces. The most likely mechanism is the prevalence-rank/sample-size-noise
  confound described above, which is shared between the real and pseudo concept sets by
  the matching design itself.

## Caveats / deviations from spec

- Used the **current** (post-2026-05-24 Greek-hyle-fix) `harmonized_concepts.tag()` for
  on-the-fly tagging rather than the chunks' baked-in `option_a_concepts` field, matching
  `phase3a_rsa_recheck.py` (the source of the published +0.392/+0.435 numbers) rather than
  the older `phase3a_rsa_prototype.py` (+0.363/+0.432, pre-fix). This is the correct
  comparison target, not a deviation in substance, but noted because the two scripts give
  different "published" baselines.
- Pseudo-vocabulary drops hapax tokens (frequency 1 within-language) for stability and
  runtime; documented, not spec'd.
- Harmonized-dictionary exclusion for Spanish (regex-based dict) uses a crude
  metacharacter-stripping approximation (`regex_core()`) to get literal cores for
  substring-overlap exclusion, rather than true regex matching -- close enough to keep
  dictionary terms out of the pseudo-vocabulary but not exact.
- The greedy prevalence-matching allows a documented fallback (relax the +/-20% ceiling)
  when a language's vocabulary can't hit the window in the primary pass; this fired
  rarely (99.1% of the 2,100 pseudo-concepts landed in-window on the first pass).
- Both LaBSE and OpenAI were computed for both controls -- the OpenAI cache aligns
  positionally with the chunk-loading order (verified: n=5,585 rows match exactly, as in
  the existing RSA scripts), so no fallback to LaBSE-only was needed.
- Did not isolate the prevalence-rank-confound mechanism proposed above (e.g. an
  equal-N or rank-shuffled version of Control B); flagged as a natural follow-up, not
  executed, to keep this task scoped to the two specified controls.
