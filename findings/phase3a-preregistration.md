# Phase 3a — Formal Pre-Registration: The China × Greece Independence Test

**Document status: FROZEN PRE-REGISTRATION.** Publication of this document in the public
repository (git commit + Zenodo DOI) constitutes the act of pre-registration. No analysis
described in §7 (Execution) has been run at freeze time. The timestamp of record is the
public git commit and the Zenodo version DOI of the release that first contains this file.

**Author:** T. David Kinlaw (ORCID 0009-0008-5213-1017)
**Date frozen:** 2026-07-05
**Supersedes:** the CCB-based design sketched in `findings/phase3a-design.md` §3–§4
(instrument replaced after due-diligence; see §4 below and `findings/phase3a-instrument-tests.md`).
**Design record:** `findings/phase3a-design.md` (planning trail),
`findings/phase3a-instrument-tests.md` (instrument due-diligence),
`findings/phase3a-rsa-snr-sizing.md` (power analysis). These documents are published
alongside this registration.

---

## 1. The question

Every cross-tradition convergence this project has measured (Phases 0–2) is confounded by
**genealogical relatedness or documented contact**, without exception. Within-language
tradition pairs share language and usually region/era; Bible×Quran share Abrahamic lineage;
even Chinese Buddhist×Daoist converged *in contact* (Chan is their fusion). Phase 3a is the
project's first **confirmatory** test, on the one comparison that separates the two live
hypotheses:

- **H-structural:** contemplative/philosophical traditions converge on shared structure
  because they independently describe something universally accessible (shared experience,
  shared cognition, or shared world; see the interpretive ceiling, §9).
- **H-diffusion:** apparent convergence is transmitted (ideas flowed, directly or through
  intermediaries) and vanishes between genuinely independent traditions.

**The test pair:** Axial-Age China (pre-Buddhist Daoist and Confucian corpora) × Axial-Age
Greece (Platonist and Aristotelian corpora), in original languages (classical Chinese,
ancient Greek), before documented contact, with an **age/contact gradient** within each
sphere (Greece: Plato → Hellenistic → Neoplatonist; China: pre-Buddhist → early-contact →
Buddhist-era/Neo-Confucian) and an imported-vs-indigenous **transmission factor** (Chinese
Buddhism is a *known-diffusion* internal reference).

*Historiographic caveat, registered up front:* "genealogical independence" of Axial-Age
China and Greece is a premise with a contested literature (long-distance contact debates).
The design does not rest on absolute independence: documented-contact level enters as a
graded factor, and the age/contact gradient is the built-in sensitivity analysis. If the
independence premise is wrong in degree, the gradient is where it shows up.

## 2. Prior-exposure disclosure (what has and has not been seen)

A firewall has been maintained since 2026-05-21: **the sealed Axial gradient corpus
(Plato…Zhuxi) has never been embedded, tagged for analysis, chunk-screened for concept
prevalence, or entered into any CCB/RSA computation.** Corpus sourcing, cleaning, and
metadata patching are the only operations performed on it.

Known adjacencies, disclosed:

1. `phase3a-instrument-tests.md` §3 (granularity test, 2026-05-24) computed control-concept
   and SUBSTRATE/AWARENESS **CCB** on the **Phase 2c contacted-era** Chinese↔Greek pair
   (TTC/Platform Sutra × Plotinus/Clement: *mystical-era, contact-confounded texts, not the
   Axial gradient*). SUBSTRATE was flat on both models there. This is adjacent to, but not,
   the sealed question: different corpus (contacted era), different instrument (cross-language
   CCB, since abandoned), and the Greek cell was ὕλη-confounded. It was flagged at the time.
2. The Phase 2c originals grid (6 languages including classical Chinese and ancient Greek,
   contacted-era texts) underlies all instrument calibration below, including RSA prototypes
   in which Chinese and Greek systems appear *among* pooled languages.
3. Scripture-register reliability runs (Koine/classical-Chinese Bibles) used the fixed
   Bible×Quran reference corpus, not the gradient corpus.
4. Two review-driven control suites were run on 2026-07-05, before this freeze, on
   non-sealed data only: lexical-overlap controls on the English Phase 1a corpus
   (`findings/phase1a-lexical-controls.md`) and RSA noise-ceiling/arbitrary-word-set
   baseline controls on the Phase 2c originals (`findings/phase2c-rsa-controls.md`). The
   second of these motivated the two-tier null in §4: the exploratory Phase 2c isomorphism
   cleared concept-label permutation but not the matched word-set baseline. This
   registration therefore adopts the stricter null *knowing the exploratory data would
   fail it*; the confirmatory test is registered against the standard the exploratory
   result could not meet.

No cross-sphere China×Greece value on the Axial (pre-contact) cells exists anywhere in the
project's results as of this freeze.

## 3. Corpus

**Sealed gradient corpus (sourced, uncleaned analysis):** Greek and Chinese spheres × three
eras × nondual/dual category × transmission tag, as inventoried in `phase3a-design.md`
Appendix (Plato, Aristotle, Alcinous, Alexander of Aphrodisias, Plotinus, Proclus, Clement;
TTC, Zhuangzi, Analects, Awakening of Faith, Platform Sutra, faju, Zhuxi, et al.).
Oversize files (Proclus ~1M chars, Alexander ~1.88M chars) are capped by random
chunk subsampling to the per-system target (§5) *before* any analysis, seeded (seed=3401).

**Pre-registered corpus enlargement (executes after this freeze, before unsealing):** the
power analysis (`phase3a-rsa-snr-sizing.md`) shows the instrument needs (i) more text per
cell and (ii) more *systems*. The enlargement rule is frozen now so corpus growth cannot be
tuned to the result:

- **Sizing target:** ≥150 tagged chunks per concept per school-system for the
  high-prevalence concepts (floor from the target-n curve; the curve had not plateaued at
  n=91, so 150 is a floor, not an optimum). **Inclusion floor:** a concept enters a system's
  RDM only if n ≥ 50 tagged chunks in that system; below that, centroids are unstable
  (equal-N control, `phase3a-instrument-tests.md` §4c).
- **Systems rule:** decompose each sphere into schools, each its own system:
  China ≥3 of {Daoist, Confucian, Buddhist (imported), Neo-Confucian};
  Greece ≥3 of {Platonist, Aristotelian, Stoic, Neoplatonist}.
  A school qualifies as a system only if ≥3 concepts pass the inclusion floor.
- **Selection rule for added texts:** public-domain, original-language, standard-canon works
  of the named schools, added by school/era slot until the sizing target is met or the
  available canon is exhausted, never selected by content inspection against the concepts.
  Sentence-level splitting is **not** used as a power lever (ruled out: it degrades centroid
  quality; `phase3a-rsa-snr-sizing.md`).

## 4. Instrument (frozen)

**Primary instrument: holistic representational-similarity analysis (RSA) of
within-language concept geometry.** Rationale (`phase3a-instrument-tests.md`): cross-language
per-concept CCB is per-cell underpowered, model-fragile (LaBSE↔OpenAI per-concept
agreement r = −0.43 cross-language on Phase 2c), and concreteness-confounded. RSA never
performs cross-lingual alignment and is the only instrument that is model-robust in the
cross-language regime (LaBSE↔OpenAI holistic agreement r = +0.78).

Procedure, frozen:

1. Chunk-level embedding of each system's corpus. **Primary model: OpenAI
   `text-embedding-3-large`** (dominates LaBSE for RSA at every n; `phase3a-rsa-snr-sizing.md`).
   **Corroboration model: LaBSE** (open-source; mandatory report). Proprietary-endpoint
   drift mitigation: the model identifier is pinned, all Phase 3a embeddings are produced
   in one contiguous window and released with the results together with all RDMs, so every
   downstream statistic is recomputable from the released artifacts without the endpoint.
   The open corroborator (LaBSE, pinned checkpoint) provides the fully reproducible leg.
2. Concept tagging with the **frozen harmonized dictionaries**: `scripts/harmonized_concepts.py`
   (7 contemplative concepts: ULTIMATE, SUBSTRATE, AWARENESS, WORLD, SELF, RECOGNITION,
   NONSEP, including the Greek SUBSTRATE ὕλη fix of 2026-05-24) and
   `scripts/control_concepts.py` (5 controls: EATING, DRINKING, SLEEP, GOVERNANCE, WARFARE,
   with the freeze-time decisions recorded there: literal-eating only, DRINKING water-term
   restriction, GOVERNANCE 法 dropped, δικαι register split). The dictionaries in the
   registered commit are the frozen versions; any later edit is a documented amendment (§8).
3. Per system: per-concept centroid (mean of tagged chunk embeddings, concepts passing the
   inclusion floor) → concept×concept cosine RDM in that system's own space.
4. **Isomorphism statistic:** Pearson correlation of RDM upper triangles between two
   systems. **Null (two tiers, both required):**
   - *Primary null — prevalence-matched arbitrary-word-set baseline.* Per system, ≥200
     pseudo-concept sets: seven word sets each, sampled from that system's own vocabulary
     (all frozen-dictionary terms excluded), each matched to the corresponding real
     concept's tagged-chunk count within ±20%, sampled independently per system so no
     cross-system correspondence exists. The baseline distribution is the pooled
     cross-sphere isomorphism of each pseudo draw; the real value must exceed its 95th
     percentile. Rationale: on Phase 2c originals this baseline proved far stricter than
     concept-label permutation — the exploratory isomorphism cleared permutation (p≈.03–.05)
     yet fell at the 12th–14th percentile of the matched baseline
     (`findings/phase2c-rsa-controls.md`, 2026-07-05, run before this freeze). A null this
     result showed to be too weak cannot be the registered criterion.
   - *Floor — concept-label permutation* within one system (all label arrangements for
     K ≤ 7; ≥10,000 samples otherwise), retained as the chance floor.
5. **Reliability gates (must pass before any cross-sphere unsealing):** the ancient-register
   scripture reliability results already in hand (SUBSTRATE binds in Koine and classical
   Chinese registers; profile-fit r = 0.86/0.92) qualify the two languages; each *system*
   additionally passes the within-system gate (concept structure resolvable within the
   system, per the Phase 2a gate-first protocol).

**Per-concept claims are pre-declared exploratory.** The equal-N control showed per-concept
attribution is sample-size-confounded on both models; no concept-specific hypothesis
(including SUBSTRATE) is registered as confirmatory. Which concepts appear stable will be
reported descriptively.

## 5. Registered hypotheses and frozen predictions

Reference values from the *contacted-era* Phase 2c originals grid (the calibration ceiling):
holistic 7-concept isomorphism +0.39 (LaBSE) / +0.44 (OpenAI), null p ≈ .03–.05 at K=7
over 6 languages.

**H3a.1 — PRIMARY (independence test).** Pooled cross-sphere isomorphism over all
{pre-contact Chinese system} × {pre-contact Greek system} pairs, 7-concept contemplative RDM:

- **H-structural predicts:** significantly above the permutation null (p < .05), with
  magnitude *below* the contacted-era reference — point prediction **+0.10 to +0.40** (OpenAI).
- **H-diffusion predicts:** indistinguishable from the null (|iso| below the null's 95% band).
- **Decision rule (explicit):** H3a.1 passes iff, on the primary model, the pooled
  pre-contact cross-sphere isomorphism (a) exceeds the 95th percentile of the
  prevalence-matched arbitrary-word-set baseline (§4, primary null) and (b) clears the
  concept-label permutation floor at p < .05. Clearing (b) but not (a) is registered in
  advance as **no support for H-structural** (that pattern is exactly what the Phase 2c
  exploratory data produced and what the prevalence-fingerprint mechanism predicts). The
  +0.10 to +0.40 band is a falsifiable magnitude *forecast*, not part of the criterion: a
  passing result outside the band counts as support for H-structural with the forecast
  recorded as missed. The contacted-era reference (~+0.44) was measured on the Phase 2c
  grid (different languages and corpora), so it is a reference point, not a strict
  ceiling; cross-corpus comparability is a stated assumption, not a demonstrated fact.

**H3a.2 — SECONDARY, pre-declared underpowered (the gradient discriminator).** Cross-sphere
isomorphism as a function of era/contact level (pre-contact → contact-era cells):

- **H-structural predicts:** flat in era (the invariant-residual signature; heterogeneity
  across era cells consistent with sampling noise, assessed by random-effects meta-analytic
  Q/I² over cell estimates).
- **H-diffusion predicts:** rising with contact (positive slope, contact-era > pre-contact).
- Per the power analysis the per-era cells are below target power; this readout is
  **exploratory-within-confirmatory**, not co-primary, and cannot overturn H3a.1.

**H3a.3 — INSTRUMENT QC (gating, not evidential).** Controls-only RDM (5 control concepts)
cross-sphere isomorphism must exceed the permutation null, and EATING/DRINKING must be
nearest neighbors in ≥ half the systems (the experiential-consistency check). **If this
fails, the instrument cannot see known-shared human universals at this power; the run stops
and H3a.1 is reported as UNINTERPRETABLE (not as evidence for either hypothesis).**

**H3a.4 — EXPLORATORY (the bracketing thesis).** On the extended 12-concept RDM: does the
contemplative sub-geometry's cross-sphere consistency pattern with the experiential anchors
(EATING/DRINKING/SLEEP, shared-experience convergence) or with the functional anchors
(GOVERNANCE/WARFARE, convergent evolution)? Reported descriptively with the universality
gradient (eating → SELF → contemplative concepts).

**H3a.5 — SECONDARY (known-diffusion internal reference).** Within-China, the imported
Buddhist system's isomorphism to Greek systems vs the indigenous Daoist/Confucian systems'.
Buddhism arrived by documented diffusion from a third sphere, so it calibrates what
diffusion looks like in this instrument.

**Decision table (frozen):**

| H3a.1 (pre-contact cross-sphere) | H3a.2 (gradient) | reading |
|---|---|---|
| clears null | flat | structural convergence; diffusion unnecessary |
| clears null | rising | structural floor + diffusion increment (both real) |
| null | rising | diffusion-only; no independent convergence |
| null | flat | no cross-sphere signal at this power (see §7 adequacy gate) |

## 6. Analysis plan details (frozen)

- **Cross-sphere pooling:** the primary statistic is the mean isomorphism over all
  qualifying pre-contact cross-sphere system pairs; its null is the same statistic under
  concept-label permutation. Within-sphere pairs (Greek×Greek, Chinese×Chinese schools) are
  reported as the coverage/upper-reference tier, not pooled into the primary.
- **Missing concepts:** RDMs are compared on the intersection of concepts passing the
  inclusion floor in both systems; a pair qualifies only if K ≥ 5 shared concepts.
- **Prevalence/coverage screen** (execution step 1): per-system × per-concept tagged-chunk
  counts and within-system binding, published before any cross-sphere computation. This is
  the ULTIMATE-failure control (prevalence asymmetry) from `phase3a-design.md` §5.
- **Multiple comparisons:** one primary test (H3a.1). Everything else is labeled by its
  tier above and carries no α.
- **Coverage honesty:** any positive result is a **lower bound** on structural convergence
  (finite facet coverage); any null is relative to the instrument's demonstrated resolution
  (H3a.3 and the adequacy gate, §7).

## 7. Execution order and the adequacy gate

1. **Prevalence screen** on the (now unsealed for screening) gradient corpus: counts only,
   no cross-sphere geometry.
2. **Corpus enlargement** to the §3 rule; re-screen.
3. **Adequacy gate:** re-run the target-n SNR curve *on within-sphere cells only*
   (Greek×Greek, Chinese×Chinese school pairs) to confirm the instrument clears the
   two-tier null of §4 (matched word-set baseline + permutation floor) on
   contacted/related systems at achieved n. If it cannot, the pre-declared **fallback**
   activates: Phase 3a is reported as a *descriptive measurement* (option (c) of
   `phase3a-rsa-snr-sizing.md`), the confirmatory discriminator deferred, and no
   hypothesis-level claim is made. Cross-sphere cells stay unexamined until this gate passes.
4. **QC unsealing:** H3a.3 controls-only cross-sphere run. Stop on failure.
5. **Primary unsealing:** H3a.1, then H3a.2/H3a.4/H3a.5, then the corroboration model, in
   one scripted pass (`phase3a_run.py`, to be written to this specification before step 4).

## 8. Amendments

Any deviation (dictionary edit, corpus substitution, threshold change) after this freeze is
recorded in a dated amendment section appended below, committed publicly *before* the
affected analysis step runs. Deviations discovered after running are reported as such.

## 9. Interpretive ceiling (registered up front)

A fully successful structural result establishes that the convergence is
**experientially/cognitively universal rather than culturally transmitted**, the
Stace/Forman-vs-Katz crux. It does **not** establish access to a mind-independent
metaphysical reality: shared experience could be shared neurology. No claim beyond the
former will be made from Phase 3a data. Conversely, a diffusion-only result does not refute
contemplative claims; it bounds what this instrument, on these corpora, can detect.

---

*Amendments: none at freeze.*
