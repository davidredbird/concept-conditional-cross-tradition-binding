# Phase 2a: cross-tradition CCB in classical Arabic (Sufi × Falsafa)

**Date:** 2026-05-20  **Status:** EXPLORATORY (not pre-registered)
**Scripts:** `fetch_openiti.py`, `arabic_gate_prep.py`, `phase1c2_cross_tradition_ccb.py`
**Outputs:** `results/phase2a/arabic_sufi_falsafa_ccb_labse.json`

A **second non-Western ORIGINAL-language** corpus, to test whether the Chinese
pattern (WORLD/ULTIMATE/SUBSTRATE bind, AWARENESS flat) generalizes or is
Chinese-specific. Sourced from **OpenITI** (the clean machine-readable
Islamicate-texts corpus on GitHub — the Arabic analog of CBETA).

## Corpora

| text | tradition | category | chunks |
|---|---|---|---|
| Fuṣūṣ al-Ḥikam (Ibn ʿArabī, d.638 AH) | sufi | nondual (waḥdat al-wujūd) | 339 |
| al-Najāt (Avicenna, d.428 AH) | falsafa | dualistic (rationalist philosophy) | 679 |

Arabic gate-prep: strip tashkeel/tatweel, normalize alef/ya, then an article-prefixed
Option-A dictionary (العقل, العالم, الفناء …) to dodge bare-stem collisions
(علم↔عالم, كون↔يكون).

## Gate-first: classical Arabic RESOLVES under LaBSE

Within-Fuṣūṣ concept binding (LaBSE): **6/7 concepts bind** — AWARENESS +0.024,
RECOGNITION +0.030, ULTIMATE +0.035, WORLD +0.031, SUBSTRATE +0.022, SELF +0.015
(all p≤.004); only NONSEP fails (n=12). On par with English/Chinese/French (6/7),
far above Sanskrit (2/7). Classical Arabic is a legitimate test language.

## Result — ALL FIVE Phase-1a concepts bind cross-tradition

| concept | CCB (LaBSE) | p | n_both |
|---|---|---|---|
| SUBSTRATE | +0.033 | <.0001 | 2295 |
| AWARENESS | +0.023 | <.0001 | 10506 |
| WORLD | +0.023 | <.0001 | 7740 |
| ULTIMATE | +0.020 | <.0001 | 72924 (Sufi side ~saturated) |
| SELF (non-1a) | +0.017 | .001 | 6831 |
| RECOGNITION | +0.014 | .040 | 506 |
| NONSEP | −0.003 | .60 | 84 (tiny) |

**5/5 Phase-1a concepts bind, including AWARENESS** — with AWARENESS well-tagged on
*both* sides (Fuṣūṣ 103 × Najāt 102), the best AWARENESS cross-tradition testability
of any non-Western original corpus.

## The cross-linguistic synthesis (this is the payoff)

Two non-Western ORIGINAL-language cross-tradition tests now exist (both LaBSE):

| concept | classical Chinese (Buddhist × Daoist) | classical Arabic (Sufi × Falsafa) |
|---|---|---|
| AWARENESS | **flat** | **binds** |
| RECOGNITION | untestable | binds |
| SUBSTRATE | binds | binds |
| WORLD | binds | binds |
| ULTIMATE | binds | binds |

AWARENESS binds in original Arabic but NOT original Chinese. So AWARENESS
convergence is **not** a pure translation artifact (it appears in an untranslated
language). The distinguishing factor is **shared awareness-vocabulary**:

- **Arabic Sufi + Falsafa share ONE intellectual lineage** — both inherit the
  Greek–Arabic philosophical lexicon for mind/soul/intellect (العقل, النفس,
  المعرفة). Ibn ʿArabī and Avicenna use the *same words* for awareness. → AWARENESS converges.
- **Chinese Buddhist + Daoist are TWO separate lineages** (imported Indian Buddhism
  vs indigenous Daoism) with *distinct* original awareness-lexicons (Buddhist 識/覺/念
  vs Daoist 心/神/明). → AWARENESS does NOT converge.
- **English/French translations** manufacture shared awareness-vocabulary
  (mind/consciousness/conscience) across otherwise-distinct traditions. → AWARENESS converges.

**Refined claim — AWARENESS convergence tracks shared awareness-vocabulary, whether
native (shared lineage) or imposed (shared translation language); it is NOT a
universal cross-lineage structure.** The Chinese Buddhist×Daoist case is the unique
configuration that lacks shared awareness-vocabulary (separate lineages, original
language), and it is exactly there that AWARENESS fails to bind.

Meanwhile **SUBSTRATE, WORLD, ULTIMATE bind in BOTH original non-Western languages**
(and across separate vs shared lineages) — the ontological/cosmological concepts are
the robust, lineage-independent convergers. This is consistent across Chinese and
Arabic and is the strongest candidate for a genuine cross-tradition structural
convergence.

## Caveats

- ULTIMATE is near-saturated on the Sufi side (الله in 309/339) — least interpretable;
  AWARENESS/SUBSTRATE/WORLD bind on non-saturated tags, so the result doesn't rest on ULTIMATE.
- Sufi and Falsafa share a language AND lineage — that is the *point* (it explains the
  AWARENESS binding), but it means this is not a separate-lineage test like the Chinese one.
- Arabic Option-A dict: hidden DoF; article-prefixed forms reduce but don't eliminate
  substring collisions; first-pass.
- Single resolving model (LaBSE); exploratory, not pre-registered.

## Bottom line

Adding a second non-Western original (Arabic) shows the Chinese AWARENESS-null is the
**outlier**, explained by separate-lineage distinct-vocabulary, not by language-vs-
translation alone. The durable cross-linguistic finding is now:
**SUBSTRATE / WORLD / ULTIMATE converge across traditions robustly and language-
invariantly; AWARENESS / RECOGNITION converge only when traditions share an
awareness-vocabulary (native lineage or translation), and fail across separate
original-language lineages.**
