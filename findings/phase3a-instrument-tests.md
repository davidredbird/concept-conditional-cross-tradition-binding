# Phase 3a — instrument due-diligence (power, second model, granularity, RSA)

**Date:** 2026-05-24  **Status:** pre-registration prep, firewall-safe (Phase 2 data only; no embedding/CCB on the sealed Plato…Zhuxi gradient). These tests were run BEFORE committing the Phase 3a pre-registration, to check whether the cross-language CCB instrument can carry the structural claim. Verdict: **it cannot as-is; RSA on within-language geometry is the model-robust redesign.**

## 1. Power analysis (`phase3a_power_analysis.py`)
Calibrated CCB sampling SE from Phase 2c (cross-language SUBSTRATE Δ=0.0058, σ_null=0.0017 at n_both=612k). Need ~302k both-tagged pairs for 80% power at Δ=0.006 (~1.2M at Δ=0.003).
- SUBSTRATE prevalence (Phase 2c proxy): classical Chinese 0.56, Greek 0.23 — high, asymmetric.
- **Pooled** cross-sphere China×Greek (corrected corpus: Chinese nondual ~3,376 chunks, Greek ~6,455) is plausibly powered at realistic asymmetric prevalence for Δ=0.006.
- **Per-cell** (the age-gradient diff-in-diff) is the binding constraint — independent cell ≈ Plato 1,263 × Daoist ~931 chunks → marginal; pair-count scaling is *optimistic* (effective n = tagged chunks, not pairs), so true power is lower; and if independent-tradition convergence is smaller than the contacted 0.006, even pooled gets shaky.
- Lever: **sentence-level** (~5–6× units). Cap the giant files (Proclus ~1M, Alexander ~1.88M).
- Fixed metadata: 10 gradient metas lacked sphere/char_count (Plato/Aristotle/Plotinus/Clement; TTC/Zhuangzi/Analects/Platform/faju) — patched (`patch_gradient_meta.py` + char backfill). john_chinese left unsphere'd (scripture, not gradient).

## 2. Second-model viability — OpenAI text-embedding-3-large (`phase3a_second_model_viability.py`)
- **Anisotropy: PASSES.** Healthy spread on all 6 non-English languages (within-language cos means 0.31–0.54, std 0.07–0.11; cross 0.176/0.065). No e5-style cone-collapse. So a viable, *different-objective* second model exists.
- **But the dissociation does NOT replicate.** Pooled cross-language: AWARENESS +0.0131, ULTIMATE +0.0112, RECOGNITION +0.0211 all BIND (LaBSE had them flat/name-bound); SUBSTRATE +0.0076 (binds, but middling, not special). The LaBSE "AWARENESS=vocab / SUBSTRATE=structural" dissociation is **LaBSE-specific**, not model-robust. RECOGNITION (nirvāṇa/mokṣa — maximally name-bound) binding strongest is the tell: OpenAI aligns spiritual *topics* across languages aggressively.

## 3. Granularity / discrimination test (`phase3a_granularity_test.py`)
Control concepts (governance/eating/drinking/warfare) vs SUBSTRATE/AWARENESS on the **Chinese↔Greek** Phase 2c pair (control dicts cover en/gr/zh only), both models.
- **"OpenAI binds everything" was a POOLED artifact.** On the specific Chinese↔Greek pair, OpenAI is *conservative* (only AWARENESS + weak EATING bind). The pooled over-binding came from easy shared-lineage pairs. **Pooled cross-language CCB is a heterogeneous mush** — vindicates per-language-pair Δ-baseline.
- **CONCRETENESS is the real cross-language axis:** concrete concepts (eating/drinking/warfare) bind, abstract ones (governance, SUBSTRATE) flat — on both models. Cross-language CCB on an abstract concept fights an alignment penalty concrete ones don't. So eating binding ≠ "shared experience converges"; it may be "concrete vocabulary aligns."
- **Control revision:** GOVERNANCE (abstract+contingent) is the right matched null for SUBSTRATE (abstract+structural); WARFARE binds via concreteness → bad cross-language null (reverses the earlier within-Bible "warfare cleaner" call).
- **Firewall note:** by control-dict coverage this computed a Chinese↔Greek SUBSTRATE value (flat both models) — adjacent to the sealed question. Mitigated: Phase 2c *contacted-era mystical* texts (Plotinus/TTC), NOT the Axial gradient; Greek SUBSTRATE ὕλη-confounded. Flagged to David.

## 4. RSA prototype — the redesign (`phase3a_rsa_prototype.py`, `phase3a_rsa_facet.py`)
Compare *relational* structure (within-language concept RDMs), not absolute position. Per-language concept×concept RDM in each language's own space, correlate RDMs across languages (second-order isomorphism). No cross-lingual alignment ever happens.
- **MODEL-ROBUST: LaBSE↔OpenAI pattern Pearson = +0.79**, similar magnitudes (mean RDM-corr +0.363 LaBSE / +0.432 OpenAI). The two models that *disagreed* on raw CCB *agree* on RSA. This addresses BOTH the alignment confound (RSA never aligns) AND single-model-dependence (corroborated across models). OpenAI slightly better for RSA (null p .031 vs .052).
- **Signal modest, power-limited at K=7** (null p ≈ .03–.05). Facet-decomposition was the proposed power lever (see §4a).
- **Reframes the concept hierarchy:** RSA-stable backbone = ULTIMATE/AWARENESS/SELF (low cross-language variance in relative position); SUBSTRATE/RECOGNITION/NONSEP peripheral + variable. The model-robust method does NOT crown SUBSTRATE. "Which concept converges" is method-dependent (English→AWARENESS/RECOGNITION; LaBSE cross-lang→SUBSTRATE; OpenAI→everything; Chinese↔Greek→AWARENESS; RSA→ULTIMATE/AWARENESS/SELF) — **the method-dependence is itself a finding**; do NOT pre-register SUBSTRATE-is-structural as established.
- Caveat: concept centroids are close (cos 0.93–0.99); RSA reads fine rank structure.

### 4a. Facet-RSA + degeneracy (`phase3a_rsa_facet.py`, 2026-05-24)
- **Facet lever DEAD.** SUBSTRATE facet sub-centroids near-degenerate (mean pairwise cos 0.94 LaBSE / 0.89 OpenAI) and too sparse to form in all 6 languages. Facets add near-duplicate noise, not RSA resolution. Use more *systems* (per-tradition RDMs) + more *distinct* concepts for power, not sub-concepts.
- **Dropping SUBSTRATE RAISES isomorphism:** 6-concept backbone (no SUBSTRATE) mean RDM-corr +0.460 LaBSE / +0.541 OpenAI vs the 7-concept +0.363 / +0.432. SUBSTRATE is the *least* cross-tradition-consistent concept relationally — it drags the isomorphism down. The model-robust relational signal lives in the AWARENESS/ULTIMATE/WORLD/SELF/RECOGNITION/NONSEP backbone, and is stronger than the first prototype showed.
- **Caveat (could rescue SUBSTRATE):** confounded by the known Greek ὕλη mis-mapping (harmonized Greek SUBSTRATE keys on ὕλη=matter, not emptiness). The SUBSTRATE-outlier reading is NOT trustworthy until the Greek SUBSTRATE dict is fixed (drop ὕλη, proper emptiness terms) and re-tested — a concrete firewall-safe next step.

### 4b. Greek SUBSTRATE ὕλη fix + RSA re-check (`phase3a_rsa_recheck.py`, 2026-05-24)
Dropped ὕλη (matter), added κενό (void); Greek SUBSTRATE tagging halved (0.23→0.11, ὕλη was firing on ~half — Plotinus is matter-heavy). **RSA result essentially UNCHANGED** (7-concept +0.363→+0.392 LaBSE / +0.432→+0.435 OpenAI; drop-SUBSTRATE identical; SUBSTRATE std unchanged). So the SUBSTRATE-outlier result is **robust to the ὕλη fix — not a dictionary artifact.** But SUBSTRATE not uniquely the outlier: variable cluster = {SUBSTRATE, RECOGNITION, NONSEP} (the rarer, distinctively-nondual concepts), stable backbone = {AWARENESS, ULTIMATE, WORLD, SELF}.

### 4c. EQUAL-N control — the resolver (`phase3a_rsa_equalN.py`, 2026-05-24)
Subsampled every concept×language cell to the common floor (F=8, set by Hebrew NONSEP), bootstrap 200×, both models. **TWO decisive results:**
- **Per-concept gap CLOSES at equal n:** backbone std 0.026 vs distinctive 0.028 (LaBSE); 0.040 vs 0.049 (OpenAI). The "distinctive concepts diverge / SUBSTRATE is the outlier" finding was a **sample-size artifact** (those concepts are rarer → noisier centroids). KILLED.
- **The isomorphism is LOW-SNR:** collapses from ~0.4 (full n) to +0.023 LaBSE / +0.009 OpenAI at n=8. The real, model-robust signal lives in fine structure needing large per-concept samples.

**Resolution of the whole "which concept converges keeps changing" confusion:** per-concept attribution was never reliable (sample-size/frequency-confounded). Only the **holistic concept-geometry isomorphism** (~0.4, model-robust r=0.79) is a robust signal — RSA shows the *overall arrangement* of contemplative concepts is moderately isomorphic across independent linguistic traditions, but **cannot reliably attribute it to specific concepts** at current power. Neither CCB's "SUBSTRATE is special" nor RSA's "SUBSTRATE diverges" survives.

**Phase 3a consequence:** pre-register the HOLISTIC RSA isomorphism + age-gradient (not a concept-specific claim); the signal needs large n per centroid so per-era cells are RSA-underpowered (same power wall as CCB) → pooled holistic primary, gradient secondary, sentence-level, big corpora. Refinement available: SNR curve (isomorphism vs n at F=20/50/100) to size the corpus requirement.

## 5. RSA vs CCB head-to-head — model-robustness (`phase3a_rsa_vs_ccb.py`, #72 installment 1)
On identical Phase 2c data + harmonized tags, cross-model (LaBSE vs OpenAI) agreement:
- **CCB per-concept, cross-language: r = −0.426** (the published "dissociation" lives here)
- **CCB per-concept, within-language: r = −0.964** (the "clean" CCB — nearly perfectly REVERSED)
- **RSA holistic isomorphism: r = +0.783** (means +0.392 / +0.435)

In the cross-lingual Phase 2 data CCB's per-concept conclusions ANTI-correlate across models; only RSA is model-robust there.

**Installment 2 (Phase 1 English, `phase1_rsa_vs_ccb.py`) CORRECTS installment 1's over-generalization.** On the 6009-chunk English corpus, cross-model agreement: **CCB per-concept r = +0.879**, **RSA r = +0.965** (mean iso +0.67). So **CCB is NOT generally model-fragile — it is model-robust MONOLINGUALLY (English) and fragile only CROSS-LINGUALLY (Phase 2).** The dividing line is the cross-lingual alignment step (model-specific), not CCB-vs-RSA. Consequences:
- **The English Phase 0/1 findings are solid** — both methods, both models agree (CCB r=0.88, RSA r=0.97); RSA even corroborates them (English cross-tradition concept-geometry isomorphism +0.67, model-robust). Do NOT walk these back.
- **Only the Phase 2 *cross-lingual* per-concept dissociation is the model artifact** (Draft 7's multilingual headline). That is the narrow thing to correct.
- **RSA is the robust instrument everywhere** — and the only robust one in the cross-lingual regime → mandatory for Phase 3a (China×Greece).

Honest paper framing: "per-concept CCB convergence is robust *within* a language but NOT *across* languages (where the embedding model's alignment dominates); representational-geometry (RSA) is robust in both regimes — strong within-language and moderate cross-language cross-tradition structural convergence." Coarse-r caveat (7 concepts) still applies.

## Bottom line for Phase 3a
Three checks converge: cross-language CCB for the abstract structural concept is (a) per-cell underpowered, (b) model-fragile in pooled form, (c) concreteness/ὕλη-confounded — and the per-pair patterns are heterogeneous. **RSA on within-language geometry is the model-robust, alignment-free redesign** and should be the Phase 3a instrument: China×Greece test = "is Daoist/Confucian-Chinese concept-geometry isomorphic to Platonist/Aristotelian-Greek?"; age-gradient = "does isomorphism rise with contact?"; pre-register the *method* (report which concepts/facets are stable) rather than a favored concept. Standing task: re-run all Phase 1 + 2 with RSA vs CCB (#72).
