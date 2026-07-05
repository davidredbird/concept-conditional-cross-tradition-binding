# Phase 3a — design & planning record (pre-registration scaffold)

**Status:** PRE-REGISTERED test, NOT YET RUN. Exploratory work (Phase 2a–2d) is being
consolidated; this document captures the design discussion that will be distilled into
the formal pre-registration. **Firewall:** no embedding/chunking/CCB/peeking at any
China×Greece convergence value until the pre-registration is written and git/Zenodo
timestamped. Sourcing, scripture-baseline infrastructure, and control-concept *design* are
firewall-safe; **embedding the philosophical (Plato…Zhuxi) corpus is not — bright line
affirmed (decision (b), 2026-05-21): even within-group coverage of *control* concepts on
the philosophical corpus waits for pre-reg execution.** Control dictionaries are validated
on scripture only until then.

Date opened: 2026-05-21.

---

## 1. The central question

Every cross-tradition convergence the project has measured (Phase 0–2d) is confounded by
**relatedness/contact** — without exception. Within-language pairs share a language and
usually a region/era; Bible×Quran share Abrahamic lineage and centuries of contact; even
Chinese Buddhist×Daoist converged *in contact* (Chan is the Buddhist–Daoist fusion). We
have never measured structural convergence between genuinely **independent** traditions.
3a targets exactly and only that gap.

Four candidate causes of an observed convergence, and their status:

| cause | status going into 3a |
|---|---|
| **Vocabulary** (shared lexicon, native or translated) | **ruled out for SUBSTRATE** — it binds across original languages where AWARENESS (the vocabulary concept) goes flat (Phase 2c) |
| **Method artifact** (model/tagging/selection) | largely controlled (paraphrase removal, technical-only tagging, gate-first, within-language); residual = single model, tagging DoF, cross-lingual alignment objective |
| **Genealogical diffusion** (ideas flowed) | **THE live question** — never separated from structure because every pair was related |
| **Structural universality** (a real feature of reality/mind, independently sensed) | **THE live question** |

3a is the structural-vs-diffusion discriminator.

---

## 2. What the data establishes so far (the synthesis)

Concept behavior across the controls, easiest → harshest:

| Concept | P0→P1 English | 2c within-orig | **2c cross-lang originals** (no vocab, no translation) | Bible×Quran baseline | class |
|---|---|---|---|---|---|
| **SUBSTRATE** | +.053→+.054 (stable) | +.033 | **+.0066 BIND** | +.02–.08 | **STRUCTURAL** |
| AWARENESS | +.113→+.026 (defl 4×) | +.023 | **+.0005 FLAT** | +.02–.08 | VOCABULARY |
| ULTIMATE | +.057→+.014 | +.028 | −.004 flat | +.02–.08 | ROLE / name-bound |
| RECOGNITION | +.079 (tech +.110) | −.011 flat | −.0035 flat | na (no fire) | ROLE / soteriology |
| WORLD | +.077→+.022 | −.006 flat | +.0063 bind | +.02–.08 | NOISY |
| SELF | −.058 ns | +.023 BIND | +.0042 bind | ≈0 | CONTEXT-DEPENDENT |
| NONSEP | — | +.012 | +.0047 marginal | — | secondary |

**The discovery is not "traditions converge" — it's that convergence decomposes into
separable mechanisms, and only SUBSTRATE survives the harshest control.** CCB is a
dissociation instrument.

Key supporting results:
- **Bible×Quran, ULTIMATE is only middling despite the literally-shared God** (+.047 mean,
  below AWARENESS, ~tied SUBSTRATE) because God-talk *saturates* scripture (≈31k both-tagged
  pairs vs SUBSTRATE's 280) → ubiquity destroys specificity. **Proves CCB is not a
  shared-reference / doctrinal-agreement detector** — which inoculates the SUBSTRATE result
  against "they're just naming the same thing."
- **Profile-fit reliability metric** (correlation of a language's concept-CCB profile to the
  40-language consensus on the fixed Bible×Quran corpus): the first reliability check with a
  built-in ground truth. Consensus order AWARENESS>ULTIMATE>SUBSTRATE>WORLD>SELF; 35/40
  languages fit ≥0.83. Outliers (Burmese −0.08, Japanese 0.08, Indic/Dravidian) are
  low-resource → below some resolution the *profile itself* goes unreliable, not just
  smaller. Caught Japanese, whose WORLD also failed in Phase 2a. Limits: conflates
  embedding- vs translation-quality; coarse (5 concepts); scripture-register; consensus is
  high-resource-anchored.
- **Register reliability** (greekkoine/greekmodern/chineseclassical/chinese on John+Gen+Ecc,
  verse-ID-projected tags): SUBSTRATE binds ~0.08 in **every** register incl. ancient Koine
  and classical Chinese; register penalty small (SUBSTRATE koine−modern −.001, classical−modern
  −.013). greekmodern profile-fit r=0.86; chinese reproduces 0.92 (validation). **Greek
  systematically under-binds AWARENESS** (Phase 2a + within-Bible + profile) → the vocabulary
  concept is naturally suppressed in Greek, which *helps* the SUBSTRATE structural test.

---

## 3. Measurement philosophy: relative-only / difference-in-differences

A LaBSE cosine has no absolute zero or unit — only contrasts within one space (where the
nuisance offset is shared) are interpretable. So **every quantity is a difference**, and
the design is a difference-in-differences generalized to a factorial. Cancellation ladder:

| nuisance | netted by |
|---|---|
| generic semantic similarity / register | both-tagged − one-tagged (CCB itself) |
| language clustering | restrict to cross-language pairs |
| per-language embedding resolution | Δ vs same-work Bible×Quran baseline (per language *pair* for cross-lingual) |
| "is there any convergence" → "does it change" | the era/contact gradient |
| concept-nonspecific binding | the control concepts (below) |

The estimator is a regression of concept-specific Δ-CCB on design factors:

`Δ-CCB(pair, concept) ~ contact_level + vocab_overlap + genealogical_distance + transmission + concept terms (+ interactions)`

with predicted signs frozen in advance per hypothesis. Phase 2 supplies the parameters that
make this quantitative (see §8); China×Greece values stay sealed so 3a isn't fit to its own
outcome.

---

## 4. Structural convergence = the invariant residual

Write convergence additively:

`CCB_C(gᵢ,gⱼ) = S_C + V_C·vocab + D_C·contact + R_C(coverage) + ε`

`S_C` (structural) is hypothesized **constant for concept C across all group-pairs** — a
property of the concept/reality, not the pair. So as the era gradient climbs, total↑,
vocab↑, contact↑, but the adjusted leftover should be **flat and equal across cells**.
**Invariance of the residual is the signature of structure** (like extracting a physical
constant across experiments with condition-dependent systematics).

- **Identification:** within-sphere-across-era cells (Greek-ancient × Greek-late) hold
  sphere/language/lineage fixed and vary only era → they *pin down* V_C and D_C without any
  cross-cultural signal. Subtract those calibrated loadings from cross-sphere cells to expose
  S_C. The within-sphere cells are the instrument; without them the cross-sphere residual is
  uninterpretable.
- **Two different "contacts":** within-sphere across-era is **lineage continuity**;
  cross-sphere is **inter-cultural diffusion**. Separate regressors, or late-Greek-descends-
  from-early gets misread as diffusion.
- **Operationalizing "similar across runs":** random-effects **meta-analysis** across the
  group-matrix cells — each cell → an adjusted S_C with a CI; pool; the **heterogeneity
  statistic (Q/I²)** is the invariance test, and it separates "S_C truly varies" from "S_C
  noisily estimated in low-power cells." Verdict: structural ⇔ pooled S_C>0 with LOW
  heterogeneity, control nulls ≈0, cross-category (nondual×dual) S_C≈0.

---

## 5. The coverage confound (the deepest one — it sits *on* the residual)

Vocabulary/contact confound the *raw* convergence; coverage confounds the *residual itself*.

1. **Prevalence asymmetry** — if a concept barely fires on one group, the cross-CCB measures
   absence. This is exactly the mechanism that sank ULTIMATE in the Phase-1c technical-tagger
   test. Control: per-group × per-concept screen — prevalence above a floor *and* the concept
   demonstrably binds *within* each group, before any cross-pair is trusted. (The within-Bible
   binding run is the template; SUBSTRATE passes everywhere, AWARENESS is poorly covered in
   scripture.)
2. **Facet coverage** (deep) — a text can deploy SUBSTRATE yet sample a *non-convergent
   facet* (Daoist unmanifest vs Madhyamaka dependent-origination vs Greek ὕλη prime-matter —
   which we know mis-maps). The corpus is a **detector with finite acceptance**: if it doesn't
   cover the region where the signal lives, you see nothing regardless of whether the signal
   exists. Mitigations: (a) **facet/sub-concept decomposition** — run CCB per facet, turning
   the problem into a measurement of *which* facet carries the signal; (b) **broad multi-work
   sampling** per group — this is *why* "expand the corpus broadly" was correct (facet
   coverage, not just power). Consequence: **S_C is always a lower bound** — we show
   convergence is present and robust, never that we sampled the whole structural core.

---

## 6. The control architecture (positive + negative anchors)

We replace the arbitrary zero with **real reference concepts** that bracket the scale.
Tiers by *why* a concept converges:

| tier | mechanism | reference concept | expected convergence |
|---|---|---|---|
| L1 | pure chance / arbitrary | **permutation null** (already in CCB) | ~0 |
| L2 | functional / convergent-evolution | **governance** (+ warfare/trade) | moderate, problem-driven |
| L3 | shared embodied experience | **eating, drinking** (+ sleep) | high, experience-driven |
| L4? | shared deep/introspective reality | **SUBSTRATE** (+ structural candidates) | the unknown |

**The reframed thesis:** *if structural/spiritual truths are features of reality accessible
to all humans, SUBSTRATE should converge like eating; if they are cultural inventions, like
governance.* The finding is **which cluster SUBSTRATE joins**, measured against real anchors
rather than an abstract zero.

- **Eating = positive control**, dual role: (a) calibration ceiling for "shared-reality
  convergence with zero diffusion"; (b) **instrument QC** — a known-positive; if the method
  can't see eating converge across independent cultures, it can't see anything (stop, fix).
- **Governance = functional-convergence anchor, NOT a zero-floor.** Governments converge by
  *convergent evolution* (limited stable solutions to the coordination problem — like eyes
  evolving independently many times). This is the **hardest skeptical alternative**:
  "contemplatives converge on emptiness-talk not because it's real but because contemplative
  practice yields similar states with limited descriptive solutions — convergent evolution of
  phenomenology." Governance is the reference for exactly that mechanism.
- **Concreteness confound:** eating is concrete (LaBSE aligns concrete vocabulary better);
  SUBSTRATE is abstract. So eating is an *upper bracket*, not a matched control. Fix: a
  **universality gradient** (eating/drinking → sleep/body → **SELF** (abstract universal) → SUBSTRATE).
  Eating and drinking should converge near each other — a built-in consistency check on the
  positive bracket.
  SELF, rejected as a decoy, is the natural mid-point. If convergence tracks universality even
  as abstraction rises, and SUBSTRATE sits in the universal cluster, the confound is handled
  by the gradient's shape.
- **Literal vs metaphorical:** use *literal* eating (hunger/food/meals/digestion), not
  metaphor (心齋 "fasting of the mind", feeding-on-truth, Eucharist). Coverage screen must
  confirm literal capture.
- **Rigor:** control choice is a researcher DoF — controls and their selection rule must be
  **pre-registered**, not tuned to flatter SUBSTRATE.
- **Honesty ceiling (perennialism):** even SUBSTRATE-patterns-with-eating establishes only
  **experiential-universal vs cultural-invention** (the Stace/Forman-vs-Katz crux — a strong
  result). It does NOT establish access to external metaphysical reality, because shared
  experience could be shared *neurology* rather than shared *world*. The instrument reaches
  the former; the latter is beyond it. (This is the timid-scientism / unmoored-mysticism line
  the project must walk.)

Draft term lists (first pass — to be refined + frozen) are in `scripts/control_concepts.py`.
**Scripture validation outcome (2026-05-21, `validate_control_concepts.py`):** EATING,
DRINKING, SLEEP, WARFARE fire and cohere (within-Bible binding +.017–.039, all p≤.02;
eating≈drinking consistency check passed). GOVERNANCE is flat in scripture (+.005, p≈.2)
and prevalence-inflated in Greek by *register* (δικαιοσύνη=righteousness, βασιλεία=kingdom-
of-God, νόμος=Torah — not dictionary errors) — so it CANNOT be validated on scripture; its
validation is the (gated) philosophical corpus. WARFARE is the lexically-cleaner functional
anchor; consider promoting it to primary, governance secondary. Freeze-time dict decisions:
DRINKING water-inclusion (literal-drink vs water-as-substance over-fires in Greek/Genesis);
GOVERNANCE dropped 法 (=dharma in Buddhist texts; loses Legalist sense) + the δικαι
justice/righteousness register split.

---

## 7. The group-pair matrix (what 3a actually computes)

CCB between every distinct group (sphere × era × category), four cell-types:

| cell-type | holds constant / varies | isolates |
|---|---|---|
| same sphere, era, category, diff work | all fixed | **coverage ceiling / normalizer** |
| same sphere, diff era | sphere/lineage fixed, era varies | **confound-loading instrument** + lineage drift |
| diff sphere, same era | era/category fixed, sphere varies | **the cross-cultural target** |
| cross-category (nondual × dual) | category varies | **concept-specificity negative control** |

The gradient corpus (§8 of CLAUDE.md state) — Greek and Chinese at three eras, nondual+dual,
transmission-tagged — populates all four.

---

## 8. The five design parameters Phase 2 supplies (before pre-reg)

1. **vocab-overlap coefficient prior** — from the AWARENESS dissociation magnitude.
2. **Δ normalization constants + eligible cells** — from the Bible×Quran baseline (incl. the
   new ancient-register Greek/Chinese cross-lingual normalizer, built by verse-ID alignment).
3. **minimum corpus size per cell** — from the Chinese-flip instability (within-language CCB
   unstable below some n; cross-language is the stable contrast).
4. **concept roles** — SUBSTRATE/NONSEP test; AWARENESS = vocabulary positive-control;
   ULTIMATE/RECOGNITION role-bound; SELF = universality-gradient mid-point; eating/governance
   = the bracketing controls; permutation = floor.
5. **power + collinearity** — realistic cross-language Δ magnitude (~0.006) → power analysis;
   factor correlations → which cells to engineer to break contact×vocab collinearity.

---

## 9. Open decisions before the pre-registration is frozen

- Finalize + freeze the control term lists (eating, drinking, sleep, governance, warfare)
  via a pre-committed selection rule; scripture-validate the dictionaries now. The
  within-group coverage screen on the philosophical corpus is **pre-reg execution step 1**
  (decision (b), 2026-05-21) — it requires embedding the sealed corpus, which is gated.
- Decide facet decomposition of SUBSTRATE (which facets; multiple-testing/power tradeoff).
- Quantify `genealogical_distance` (ordinal era×documented-contact vs binary).
- Build the cross-lingual Chinese↔Greek Δ normalizer (verse-ID alignment; the Quran has no
  ancient register — Bible-only anchor vs register-mixed; decide).
- Second, non-bitext embedding model for corroboration — in 3a or follow-on?
- Power analysis → cell sizes; cap the giant files (Proclus ~1M, Alexander ~1.88M).
- Write predicted heterogeneity pattern + signs, then commit + timestamp.

---

## Appendix — corpus inventory & caveats

See CLAUDE.md "Current state" and task #68 for the full sourced gradient corpus (Greek +
Chinese, 3 eras, nondual+dual, transmission factor) and the scripture reference cache
(greekkoine/greekmodern/chineseclassical + Greek Quran modern). Caveats: Proclus =
Commentary on the Republic (Elements of Theology unavailable); Alexander = Metaphysics
commentary (De Anima unavailable), ~1.88M chars; Heart Sūtra trimmed of a Ming preface;
classical-Chinese Bible renders Logos as 道 (a vocabulary-imposition specimen);
LXX/Wenli versification merges require verse-ID (not chunk-index) tag projection.
