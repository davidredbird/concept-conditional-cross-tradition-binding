# Phase 2a: cross-tradition CCB in Japanese (Buddhist × Confucian)

**Date:** 2026-05-20  **Status:** EXPLORATORY (small corpus — supporting result)
**Scripts:** `japanese_gate_prep.py`, `phase1c2_cross_tradition_ccb.py`
**Outputs:** `results/phase2a/japanese_budd_conf_ccb_labse.json`

A third Asian-language data point. Source: ja.wikisource.

| text | tradition | category | chunks | note |
|---|---|---|---|---|
| 歎異抄 Tannishō (意訳聖典) | buddhist (Pure Land) | nondual | 36 | modern-Japanese 意訳 *rendering* |
| 中庸 Chūyō / Doctrine of the Mean (國譯) | confucian | dualistic | 40 | Japanese 國譯 *translation* of the Chinese |

**Important provenance caveat:** unlike the Chinese (faju/TTC) and Arabic
(Fuṣūṣ/Najāt) corpora, which are *original-language* texts, both Japanese texts
are modern Japanese **renderings/translations** (意訳 / 國譯). So Japanese here
patterns with the *translated* corpora (English/French), not the original ones.

## Result (LaBSE; cross-tradition cosine 0.496 ± 0.075 — resolves)

| concept | CCB | p |
|---|---|---|
| ULTIMATE | +0.048 | .0015 BIND |
| AWARENESS | +0.039 | .0095 BIND |
| SUBSTRATE | +0.038 | .003 BIND |
| RECOGNITION | +0.025 | .013 BIND |
| WORLD | +0.011 | .18 no |
| SELF | +0.006 | .31 no |

4/5 Phase-1a concepts bind, including AWARENESS + RECOGNITION.

## Fit to the shared-vocabulary framework

Japanese Buddhist (Indian-origin) and Confucian (Chinese-origin) are *separate
lineages* — like the Chinese Buddhist×Daoist pair where AWARENESS was flat. Yet
**AWARENESS binds here.** The difference is exactly the framework's predictor:
these Japanese texts are **renderings/translations** (意訳/國譯), which homogenize
awareness-vocabulary into shared modern Japanese (心 kokoro, 知, 悟) — the same
mechanism by which the English/French translations manufactured AWARENESS
convergence. So Japanese is a *translated/shared-vocabulary* case, and AWARENESS
binding is consistent with the framework, **not** a counterexample.

The contrast that matters remains: AWARENESS binds in every shared-vocabulary
configuration (Arabic shared-lineage; English/French/Japanese rendered) and fails
only in classical Chinese (original-language, separate-lineage, distinct
awareness-lexicon).

## Phase 2b expansion (2026-05-20): 76 → 600 chunks, result firmed up

Expanded the corpus to fix the small-n inflation: Buddhist side += 蓮如御文章
(Rennyo) + 正信念仏偈 (Pure Land); Confucian side += 大學 (Great Learning) + 論語
(Analects) — all real-Japanese 意訳/國譯 from ja.wikisource. Now 140 buddhist + 460
confucian = 600 chunks.

| concept | small (76 chunks) | expanded (600 chunks) |
|---|---|---|
| AWARENESS | +0.039 (inflated by n=76) | **+0.017 (p=.004)** |
| RECOGNITION | +0.025 | +0.062 (p<.0001) |
| SUBSTRATE | +0.038 | +0.022 (p=.034) |
| ULTIMATE | +0.048 | +0.019 (p=.002) |
| WORLD | +0.011 (n.s.) | +0.025 (p=.0005) |
| SELF | n.s. | +0.014 (p=.014) |
| bind count | 4/5 | **5/5** |

The expansion **corrected the small-corpus inflation** (AWARENESS +0.039→+0.017) and
gave WORLD/SELF the power to resolve. Japanese now binds 5/5, still
framework-consistent (rendered text → shared Japanese vocabulary → AWARENESS binds).
Output: `results/phase2b/japanese_budd_conf_expanded_ccb_labse.json`.

## Caveats

- **Original small corpus** (36 + 40 chunks) — now superseded by the 600-chunk expansion above. — lower-powered than ZH/AR/FR/EN; effects and
  the within-Tannishō gate (AWARENESS +0.356 at n_only=1) are noisy/saturated.
- Both texts are renderings, not originals (provenance caveat above) — so Japanese
  does NOT serve as a clean second *original-language separate-lineage* test
  (classical Chinese remains the only such case).
- Japanese Option-A dict: hidden DoF, broad kanji terms (心/無/知 common).
- Single model (LaBSE); exploratory, not pre-registered.

## Standing of the cross-linguistic synthesis (now 5 configurations, all LaBSE)

| configuration | AWARENESS | SUBSTRATE | shared awareness-vocab? |
|---|---|---|---|
| classical Chinese (orig, separate lineage) | **flat** | binds | NO |
| classical Arabic (orig, shared lineage) | binds | binds | yes (native) |
| English (translated) | binds (2/3) | weak | yes (translation) |
| French (translated) | binds | flat | yes (translation) |
| Japanese (rendered) | binds | binds | yes (rendering) |

**AWARENESS / RECOGNITION convergence requires shared awareness-vocabulary (native
or imposed); it fails only across original-language separate lineages.
SUBSTRATE / ULTIMATE bind across nearly all configurations** (most robust:
ULTIMATE and SUBSTRATE in every original-language test). WORLD is mostly robust
(failed only in the small Japanese set).
