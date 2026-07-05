# Phase 2a: English cross-tradition CCB under LaBSE (model control)

**Date:** 2026-05-20  **Status:** EXPLORATORY
**Scripts:** `embed_chunks_labse.py`, `phase1c2_cross_tradition_ccb.py` (+ `--tag-mode regex`, `--traditions`)
**Outputs:** `results/phase2a/english_{buddhist_daoist,histnondual}_ccb_labse.json`

## Why this run exists

Every prior English cross-tradition CCB used OpenAI `text-embedding-3-large`
(Phase 0/1a) or MiniLM (sentence replication). LaBSE had only ever embedded
non-English text. So the cross-linguistic comparison drawn from the Chinese and
French runs (both LaBSE) vs the English Phase 1a headline (OpenAI) was
**model-confounded**. We embedded the 5,777-chunk English corpus with LaBSE to
remove that confound. English resolves cleanly under LaBSE (cross-tradition
cosine 0.652 ± 0.107 — healthy spread, not cone-collapsed like e5).

## Result 1 — broad historical-nondual English, LaBSE (5 traditions: advaita, theravada, daoism, christian_mystical, sufi)

| concept | CCB (LaBSE) | p |
|---|---|---|
| ULTIMATE | +0.023 | <.0001 BIND |
| **AWARENESS** | **+0.023** | **<.0001 BIND** |
| WORLD | +0.013 | <.0001 BIND |
| RECOGNITION | +0.012 | .013 BIND |
| SUBSTRATE | +0.004 | .36 no |
| (SELF, non-1a) | +0.071 | <.0001 |

**4/5 bind incl. AWARENESS + RECOGNITION.** **The Phase 1a "AWARENESS is a top
binder" headline SURVIVES the swap off OpenAI** — it is not an embedding-model
artifact. And the profile is **identical to French (LaBSE)**:
AWARENESS/RECOGNITION/ULTIMATE/WORLD bind, SUBSTRATE does not.

## Result 2 — DECISIVE test attempt: English theravada × daoism, LaBSE (same pair as the Chinese run)

| concept | n_with | n_both | CCB | verdict |
|---|---|---|---|---|
| RECOGNITION | 27 | 182 | +0.021 (p=.043) | BIND |
| ULTIMATE | 399 | 5018 | +0.002 (p=.37) | no |
| AWARENESS | 10 | **0** | nan | **untestable** |
| WORLD | 109 | **0** | nan | **untestable** |
| SUBSTRATE | 14 | **0** | nan | **untestable** |

**The clean "hold tradition fixed, vary language" test is data-blocked.** The
English theravada corpus is only 31 chunks, and English regex-tagging puts
AWARENESS/WORLD/SUBSTRATE tags almost entirely on the daoism side (n_both=0), so
those concepts have no cross-tradition both-tagged pairs. AWARENESS — the concept
we most wanted to compare against the Chinese null — is **untestable** here.
RECOGNITION (the one testable phenomenological concept) **does bind** (+0.021,
p=.043), a weak hint toward a language effect, but n is small.

## Model-controlled cross-linguistic picture (ALL LaBSE)

| concept | English (5 trad, Western) | French (3 trad, Western tr.) | classical Chinese (Buddhist×Daoist, original) |
|---|---|---|---|
| AWARENESS | **+0.023** | **+0.026** | **flat (−0.000)** |
| RECOGNITION | +0.012 | +0.029 | untestable |
| ULTIMATE | +0.023 | +0.019 | binds |
| WORLD | +0.013 | +0.021 | binds |
| SUBSTRATE | flat | flat | **binds (cleanest)** |

Now that the model is held constant, the pattern sharpens:
- **English and French agree** (phenomenological concepts bind, emptiness doesn't).
- **Classical Chinese is the mirror image** (emptiness binds, awareness flat).

## What this resolves, and what it doesn't

**Resolved:** the AWARENESS result is **not** an OpenAI/model artifact (it
replicates under LaBSE), and the English↔French agreement is now model-clean.

**Still confounded — language vs tradition-composition.** English and French both
include the *mystical-union* family (advaita/vedanta + christian + sufi); classical
Chinese is *Buddhist + Daoist*. So the AWARENESS-vs-SUBSTRATE swap could be driven
by **which traditions are in the set**, not by language/translation:
- SUBSTRATE (emptiness, 空/無為) may be a **Buddhist–Daoist (East-Asian)** shared structure.
- AWARENESS/RECOGNITION (consciousness, union, liberation) may be a
  **Vedanta–Christian–Sufi (mystical-union)** shared structure.

The decisive disambiguator — Buddhist×Daoist AWARENESS in a *Western language* —
came out **untestable** because the English Buddhist corpus is tiny and
AWARENESS-sparse. So we cannot yet attribute the Chinese exception to language.

## Next step to nail it

Enlarge the **Western-language Buddhist** corpus so Buddhist×Daoist AWARENESS
becomes testable in English/French:
- chunk the full English Dhammapada (`dhammapada_radhakrishnan`), and/or
- add an AWARENESS-rich English Mahayana/Chan text (the Chinese Platform Sutra was
  AWARENESS-saturated; an English Chan/Zen or Heart/Diamond Sutra is the analog).

Then re-run English Buddhist×Daoist:
- if AWARENESS **binds** → language/translation effect (Chinese null is about original-language East-Asian rendering);
- if AWARENESS **flat** like Chinese → tradition-composition effect (Buddhist–Daoist genuinely don't converge on awareness, in any language).

## Result 3 — THE LANGUAGE-CONTROLLED DECIDER: same works, vary only language

The earlier Buddhist×Daoist attempt was blocked by (a) tiny theravada n and (b) a
tagging-asymmetry — the English regex is *technical-only* (`consciousness`,
`citta`, `rigpa`) and ignored the Müller Dhammapada's "mind" (38×) / "thought"
(13×), whereas the Chinese Hanzi dict *did* tag those (心/明). Comparing
broad-Chinese vs technical-English tagging was apples-to-oranges.

Fixed by using the **full English Dhammapada (Max Müller, 103 chunks)** and the
**English Tao Te King (Legge, 91 chunks)** — the *same two works* as the Chinese
faju × Chinese TTC run — with a **breadth-matched English Option-A dictionary**
(English glosses of the Hanzi terms). Now tradition, work, model (LaBSE), and
tagging-breadth are all held fixed; only **language** varies.

| concept | English Dhammapada × TTC | Chinese faju × TTC | varies by language? |
|---|---|---|---|
| **AWARENESS** | **binds +0.014 (p=.012)** | **flat −0.013 (p=.76)** | **YES — flips** |
| SUBSTRATE | binds +0.028 (p=.048) | binds +0.054 (p=.001) | no — binds in both |
| WORLD | binds +0.011 (p=.039) | binds +0.034 (p=.02) | no — binds in both |
| ULTIMATE | flat (p=.74) | binds (p=.02) | flips other way |
| RECOGNITION | flat (n_both=23, ~untestable) | untestable | — |

**The decider:** holding the Buddhist×Daoist works, traditions, model, and
tagging-breadth fixed and varying ONLY language, **AWARENESS converges in the
English translation but is flat in the original classical Chinese.** This is direct
evidence that the AWARENESS cross-tradition convergence is **language/translation-
mediated** — it rides on shared English awareness-vocabulary
(mind/consciousness/thought/wisdom) that the original-language Buddhist (識/覺/念)
and Daoist (心/明/神) terms do not share in the embedding space.

### Result 3b — robustness across THREE English TTC translations (corrects 3a)

Re-running Dhammapada × {Carus, Goddard, Legge} TTC (all LaBSE, broad Option-A)
shows the single-translation (Legge) story was too clean. CCB by translation:

| concept | Carus | Goddard | Legge | Chinese faju×TTC |
|---|---|---|---|---|
| **AWARENESS** | −0.011 (no) | +0.012 (bind) | +0.014 (bind) | flat (−0.013) |
| **SUBSTRATE** | +0.010 (no) | +0.013 (no) | +0.028 (bind) | **+0.054 (strong)** |
| **WORLD** | +0.034 ✓ | +0.017 ✓ | +0.011 ✓ | +0.034 ✓ |
| ULTIMATE | +0.011 bind | +0.015 bind | no | +0.052 bind |
| RECOGNITION | +0.048 bind | +0.014 marg | no | untestable |

**Corrected interpretation — the two concepts have OPPOSITE language profiles, and
only WORLD is robust:**

- **WORLD**: binds in all three English translations AND Chinese → genuinely
  robust, language- and translation-invariant cross-tradition convergence.
- **AWARENESS: translation-MANUFACTURED.** Binds in 2/3 English translations
  (Goddard, Legge) but NOT Carus, and flat in the Chinese original. It varies by
  *translator* — strong evidence the convergence rides on the particular English
  awareness-vocabulary (mind/consciousness/thought) a translator chooses, not on
  language-invariant structure.
- **SUBSTRATE: original-language-NATIVE.** Strongest in the original Chinese
  (+0.054), and weak/null in English (only Legge marginal at +0.028). The
  emptiness convergence (空/無為 shared Buddhist–Daoist) is *diluted* by translation
  into varied English (emptiness/void/vacancy/non-being). The mirror image of AWARENESS.
- ULTIMATE, RECOGNITION: translation-sensitive / inconsistent.

So the earlier "SUBSTRATE is language-invariant" was wrong — SUBSTRATE is
original-language-native (translation weakens it), AWARENESS is
translation-manufactured (translation creates it), and **WORLD is the only
translation-robust binder.** This is a sharper qualification of the Phase 1a
headline than 3a alone: most Buddhist×Daoist concept-binding is translation-
sensitive; the AWARENESS signal in particular is partly a translator artifact.

### Caveats on Result 3
- "Same work" is approximate: the English Dhammapada (Müller, from Pali) and the
  Chinese faju (from Sanskrit/Prakrit via Chinese) are different recensions/source
  languages of the Dharmapada; the TTC is the same work across renderings.
- Effects are small (+0.01–0.05) and some n's are modest.
- English broad Option-A dict and Chinese Hanzi dict are both broad but not term-for-term identical.
- Single model (LaBSE), exploratory, not pre-registered.

## Caveats

- Result 2 underpowered (theravada n=31; AWARENESS untestable).
- English regex tagging vs the Option-A dictionaries used for Chinese/French — tagging
  method differs across the cross-linguistic cells (a residual confound on top of model,
  now controlled). A fully clean comparison would harmonize tagging too.
- EXPLORATORY, not pre-registered.
