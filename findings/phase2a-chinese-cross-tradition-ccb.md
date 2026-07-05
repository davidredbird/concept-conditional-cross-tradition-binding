# Phase 2a: cross-tradition CCB in classical Chinese (Buddhist × Daoist)

**Date:** 2026-05-20  **Status:** EXPLORATORY (not pre-registered)
**Script:** `scripts/phase1c2_cross_tradition_ccb.py` (generalized with `--languages`);
control via `scripts/within_language_concept_binding.py`
**Outputs:** `results/phase2a/{chinese_cross_tradition_ccb,chan_dao_ccb}_{e5,labse}.json`

First cross-tradition CCB runs in a non-English language that resolves concept
structure. Two independent Buddhist texts paired against the Daoist Tao Te Ching,
both embedding models, 2000-permutation null, Option-A Hanzi concept tags.

## Corpora

| text | tradition | category | chunks |
|---|---|---|---|
| 法句經 / Chinese Dharmapada (T0210) | theravada | **dualistic** | 68 |
| 六祖壇經 / Platform Sutra (T2008) | chan | **nondual** | 106 |
| 道德經 / Tao Te Ching (ctext) | daoism | **nondual** | 33 |

Pairing both a *dualistic* (Dharmapada) and a *nondual* (Platform Sutra) Buddhist
text against the TTC tests whether the result depends on the three-cluster
category distinction.

## Headline result: concept-stratified cross-tradition convergence

Under **LaBSE** (the model that resolves classical Chinese — see geometry note), the
two Buddhist×Daoist pairs give the **same** answer:

| concept | faju × TTC (LaBSE) | Platform Sutra × TTC (LaBSE) |
|---|---|---|
| SUBSTRATE | +0.054 (p=.001) **BIND** | +0.042 (p=.0045) **BIND** |
| ULTIMATE | +0.052 (p=.020) **BIND** | +0.047 (p=.014) **BIND** |
| WORLD | +0.034 (p=.019) **BIND** | +0.039 (p=.015) **BIND** |
| SELF (non-1a) | +0.030 (p=.029) bind | +0.042 (p=.005) bind |
| **AWARENESS** | **−0.013 (p=.76) no** | **−0.0004 (p=.47) no** |
| RECOGNITION | untestable | untestable |
| NONSEP | untestable | untestable |

**The cosmological/ontological concepts converge across the Buddhist–Daoist gap;
the phenomenological concept AWARENESS does not** — replicated across two
independent Buddhist texts and robust to the nondual/dualistic category split.

## The decisive control: the AWARENESS null is a real divergence, not a model failure

Within-language concept binding on the **Platform Sutra alone** (Chan-only, LaBSE):

| concept | within-Chan binding | p |
|---|---|---|
| **AWARENESS** | **+0.109** | **0.0000** |
| WORLD | +0.049 | 0.0015 |
| ULTIMATE | +0.038 | 0.007 |
| RECOGNITION | +0.029 | 0.003 |
| SELF | +0.027 | 0.011 |
| SUBSTRATE | +0.0005 | 0.55 |
| NONSEP | +0.016 | 0.24 |

**AWARENESS is the single strongest-resolved concept *within* Chan (+0.109)** — yet
its *cross-tradition* binding with Daoism is exactly zero (−0.0004). The model sees
awareness-structure fine; Buddhist and Daoist awareness-vocabulary simply do not
occupy convergent regions of the space. This rules out "the model can't resolve
AWARENESS" and establishes the cross-tradition null as a **genuine structural
divergence**. (RECOGNITION binds within-Chan at +0.029 but is untestable
cross-tradition because the TTC has no 涅槃/菩提 vocabulary.)

## Embedding geometry: e5 is uninformative here

| model | cross-tradition cosine (Chan×Dao) |
|---|---|
| e5-large | 0.841 ± **0.015** (cone-collapsed) |
| LaBSE | 0.553 ± **0.101** (~7× the range) |

e5-large anisotropically collapses classical Chinese into a ~0.84 cone; its
concept signal is ±0.002, an order of magnitude under the cone's own noise, so e5
returns 0/5 on both pairs — **uninformative, not negative**. All positive findings
rest on LaBSE. (Note e5 still separates the two *traditions*; it just cannot resolve
*concepts* on top.) **Fertility inverts the right choice**: e5 had the best Chinese
fertility (0.98), LaBSE the worst modern fertility (1.50) — yet LaBSE is the one
that resolves. Reinforces Stage-1: pick the model whose geometry resolves the
language, never the tightest tokenizer.

## Interpretation

**Novel, falsifiable hypothesis — convergence is stratified by abstraction type.**
Ontological/cosmological vocabulary (the ground/ultimate 道·佛性·法身; emptiness/
non-doing 空·無為; the world/myriad-things 萬物·世間) converges across even a very
distant lineage gap (Indic Buddhist ↔ Chinese Daoist). Phenomenological/awareness
vocabulary (覺·般若·識 vs 心·神·明) does **not** converge across that gap, despite
resolving strongly *within* each tradition.

**Relation to the Phase 1a English AWARENESS headline — careful.** In English,
AWARENESS was the *strongest* cross-tradition binder. Here it is the *only*
non-binder. But this is **not a direct refutation**, because:
- Phase 1a's AWARENESS signal was *intra-Indic* (Mahayana × Theravada;
  Advaita × Theravada). This is *cross-lineage* (Indic Buddhist × Chinese Daoist).
- So two readings remain open: (a) AWARENESS converges only within a shared lineage
  or shared translation language (English translators imposing
  "awareness/consciousness" across traditions) — i.e. the Phase 1a signal was partly
  translation-mediated; or (b) awareness is genuinely lineage-specific in structure
  while cosmology is universal. This test cannot separate (a) from (b) — that needs
  an *Indic-language* Buddhist × Hindu AWARENESS test, which failed the resolution
  gate (Sanskrit/Pali, 2/7). What it *does* establish: AWARENESS does not bridge the
  Buddhist–Daoist gap, while cosmological vocabulary does.

**Prediction (testable):** a same-lineage cross-language AWARENESS test (e.g. Chinese
Buddhist × Tibetan/Indic Buddhist) should bind; the cross-lineage gap is what breaks it.

## Caveats

- Single resolving model (LaBSE); e5 uninformative → not a cross-model replication.
- Buddhist-leaning Hanzi dictionary: RECOGNITION/NONSEP untestable cross-tradition
  (TTC vocabulary gap); ULTIMATE near-saturated on the Daoist side (道). Option-A
  hidden DoF. Expanding RECOGNITION with Daoist realization terms (得道·歸根·復命)
  would add hidden DoF and is deferred.
- Small Daoist n (33 chunks); Platform Sutra includes a short table-of-contents.
- EXPLORATORY, not pre-registered.

## Follow-ups

1. Anisotropy/effect-size guard on the within-language gate (task #55): e5's reported
   faju 6/7 pass is suspect given its 0.015-std cone — a permutation test can call a
   +0.002 shift "significant." Require effect size relative to dynamic range.
2. Same-lineage cross-language AWARENESS test to separate the translation-artifact vs
   lineage-specificity readings.
3. Pre-register the concept-stratification hypothesis (cosmological binds cross-lineage,
   phenomenological does not) before testing on a new tradition pair.

## Bottom line

In classical Chinese, under the model that resolves it, **cosmological concepts
(ULTIMATE, SUBSTRATE, WORLD) bind across the Buddhist–Daoist boundary; AWARENESS
does not** — and the within-Chan control proves the AWARENESS null is a real
cross-tradition divergence, not a resolution artifact (AWARENESS is the
best-resolved concept *within* Chan, +0.109). This stratifies the convergence
claim by abstraction type and puts a sharp, falsifiable question to the Phase 1a
AWARENESS headline.
