# Phase 2b: the Dhammapada × Tao Te Ching language gradient

**Date:** 2026-05-20  **Status:** EXPLORATORY (Phase 2b opening result)
**Outputs:** `results/phase2b/french_dh_tao_ccb_labse.json` + the ZH/EN runs from Phase 2a
**Design:** the SAME tradition-pair (Buddhist Dhammapada × Daoist Tao Te Ching),
held fixed, run across languages. Tradition AND text are constant; only **language /
translation** varies. This generalizes the single EN-vs-ZH control from Phase 2a into
a gradient — the core Phase 2b experiment.

## The gradient (LaBSE, broad Option-A tags per language)

| language (translation) | AWARENESS | SUBSTRATE | WORLD |
|---|---|---|---|
| **classical Chinese (original)** | −0.013 (flat) | **+0.054 (p=.001)** | +0.034 |
| English — Legge | **+0.014 (p=.012)** | +0.028 (p=.05) | +0.011 |
| English — Goddard | **+0.012 (p=.02)** | +0.013 (n.s.) | +0.017 |
| English — Carus | −0.011 (n.s.) | +0.010 (n.s.) | +0.034 |
| **French — Julien** | **+0.021 (p<.0001)** | **−0.009 (flat)** | +0.012 |

(Chinese = faju × taote_chinese; English = dhammapada_radhakrishnan/Müller ×
taote_{legge,goddard,carus}; French = Le Dhammapada × taote_french/Julien.)

## Result: AWARENESS and SUBSTRATE move in OPPOSITE directions under translation

- **AWARENESS — manufactured by translation.** Flat in the original Chinese (the
  Buddhist 識/覺 and Daoist 心/神 awareness-lexicons don't converge), but BINDS once
  translated (French +0.021; English 2/3 translators). Translators render both
  traditions' awareness-language with a shared target-language vocabulary
  (conscience/esprit; mind/consciousness), creating convergence that wasn't there.

- **SUBSTRATE — native to the original, destroyed by translation.** Strong in the
  original Chinese (+0.054: 空/無/無為 genuinely converge Buddhist↔Daoist), weak in
  English, and gone in French (−0.009). Translators render the Buddhist and Daoist
  emptiness-terms with *different* French/English words, so the native convergence
  is lost.

These are **mirror-image gradients on a single fixed pair** — the cleanest
demonstration the project has of the Phase 2a thesis:

> Cross-tradition AWARENESS "convergence" is a translation/shared-vocabulary
> artifact; SUBSTRATE convergence is a genuine original-language structural signal
> that translation degrades.

## Why it matters

This is the experiment Phase 2b was designed for, and the very first pair already
yields a clean monotone story. It converts the Phase 2a claim from a
cross-sectional inference (different pairs in different languages) into a
**within-pair, language-controlled gradient** — tradition, text, model, and
tagging-breadth all fixed.

## Second fixed pair — Bhagavad Gītā × Dhammapada (Hindu × Buddhist)

Built from texts already in hand (EN: Arnold Gītā × Müller Dhammapada; FR: Burnouf
Gītā × Le Dhammapada). **Translation-only — no original anchor** (Sanskrit Gītā and
Pali Dhammapada both FAIL the LaBSE gate, so there is no original cell).

| language | AWARENESS | WORLD | SUBSTRATE |
|---|---|---|---|
| English | **+0.025 (p<.0001)** | +0.013 (p=.02) | +0.054 (n_both=6, unreliable) |
| French | +0.010 (p=.051, marginal) | +0.016 (p<.0001) | +0.012 (n.s.) |

Confirms the translation-side behavior on a *new* pair: in translation, AWARENESS
binds (strong in EN, marginal in FR). Without an original anchor it cannot show the
mirror gradient, but it is consistent — translation manufactures AWARENESS convergence.

## Sourcing ceiling (honest state)

Clean PD *parallel* tradition text caps at **EN / FR / ZH** for these works:
- TTC: only EN (Legge/Carus/Goddard), FR (Julien), ZH (original) are clean. German/
  Italian/Russian/Portuguese Wikisource have no TTC; archive.org has only a German
  *audio* Daodejing (no Wilhelm text); the Japanese 老子道徳経 is **kanbun** (classical
  Chinese w/ reading marks), not modern Japanese.
- Dhammapada: many languages exist (SuttaCentral bilara-data, 33 langs), but the
  pair needs the *TTC* in the same language, which is the binding constraint.

So the gold gradient is **complete at ZH/EN/FR** and not cheaply extensible. Further
points would require: (a) German via archive.org Fraktur OCR (Wilhelm TTC + Neumann
Dhammapada) + a German dict — real effort, OCR risk; or (b) accept the 3-language
gradient as the result.

## Third fixed pair — Dhammapada × Gospel of John (Buddhist × Christian) — THE SCALABLE ONE

The Bible is verse-aligned in **108 languages** (christos-c/bible-corpus); the
Dhammapada in **33** (SuttaCentral). So Dhammapada×Gospel is the maximally-multilingual
cross-tradition pair. John chosen as the most contemplative Gospel (Logos/light/
indwelling). Proven in 3 languages (LaBSE; my existing Dhammapadas × raw-fetched John):

| language | AWARENESS | WORLD | SUBSTRATE |
|---|---|---|---|
| English | +0.016 (p=.003) ✓ | +0.021 (p<.0001) ✓ | untestable (John has no emptiness) |
| French | +0.019 (p=.006) ✓ | +0.032 (p<.0001) ✓ | untestable |
| Chinese (faju × Union-Version John) | +0.019 (p=.006) ✓ | untestable | untestable |

AWARENESS binds in all three. The Chinese case binds (unlike faju×TTC where it was
flat) because the Chinese John is the *modern Union Version* — a translation whose
心/靈/明 vocabulary overlaps the Buddhist lexicon. Consistent with the
vocabulary-overlap mechanism. SUBSTRATE is untestable (John lacks an emptiness concept) —
the cost of using the Bible as the Christian backbone.

## SCALING PLAN — "as many languages as possible" (the path)

The route to many languages, **without hand-building a dictionary per language**:
1. **Verse-tag projection.** Tag the English Dhammapada verses and English John verses
   ONCE (broad English dict); project each tag to every language **by verse ID**
   (SuttaCentral `dhpN:M.K` and Bible `b.JOH.C.V` are verse-stable across languages).
   No per-language dictionary needed.
2. **Fetch** John per language from bible-corpus (raw XML, one file/language — works now)
   and the Dhammapada per language from SuttaCentral bilara-data (33 langs, verse JSON).
3. **Embed** (LaBSE) + per-language Dhammapada×John CCB; assemble the gradient over ~15-20 languages.

### Verse-tag-projection scaling executed (EN/DE/VI) — German added

Built `phase2b_dhp_john_multiling.py`: tag English Dhammapada + John verses once,
group into 8-verse aligned chunks, project tags by chunk index to each language
(no per-language dict). bilara has a COMPLETE Dhammapada in only en/de/et/vi/ka;
of those, German is the valuable add.

| language | AWARENESS | WORLD | ULTIMATE |
|---|---|---|---|
| English (sujato) | flat (−0.001) | +0.033 (p<.001) | +0.014 (p=.008) |
| **German** | flat (+0.003) | +0.021 (p<.001) | +0.021 (p<.001) |
| Vietnamese | flat | flat | flat (gate-unverified) |

Findings: (1) **German works** (WORLD/ULTIMATE bind) — long-sought language now a
data point. (2) **AWARENESS flipped** vs the earlier Müller/chunk-dict English
Dhammapada×John (+0.016 → flat with sujato/verse-projection) — translator+method
sensitivity = more evidence AWARENESS binding is vocabulary-fragile, not structural;
WORLD robust across both. (3) **Vietnamese all-flat incl. ULTIMATE** → likely a
resolution failure under LaBSE (or projection misalignment); inconclusive, needs a
within-Vietnamese gate before trusting. (4) SUBSTRATE untestable (John lacks an
emptiness concept — the Bible-backbone cost). Output: `results/phase2b/dhp_john_multiling.json`.

**Original blocker (now resolved):** the multilingual Dhammapada fetch needs the GitHub *API* to
discover each language's translator/author dir under `bilara-data/translation/{lang}/`,
and I hit the unauthenticated API rate-limit (60/hr) this session. Raw file fetches
still work, so this resumes once the limit resets (hourly) or with a GitHub token —
target ~15-20 languages for the Dhammapada×John gradient. This is the immediate Phase 2b
continuation.

## Next options

- **Quantify**: regress CCB(AWARENESS), CCB(SUBSTRATE) on a translation score
  (original=0, translation=1) across the 5 Dhammapada×TTC variants — direction is
  already unambiguous (AWARENESS↑, SUBSTRATE↓ with translation); a formal fit is
  underpowered at n=5 but documents the slope.
- **German** (only remaining clean-ish extension) if Fraktur OCR proves usable.
- Otherwise **consolidate Phase 2b** — the gold gradient + second-pair confirmation
  is a complete, clean result.

## Caveats

- Original cell exists only for Chinese (Pali Dhammapada + the Sanskrit originals fail
  the LaBSE gate), so the "original" anchor is single-language for now.
- Per-language Option-A dicts (hidden DoF); SUBSTRATE especially tagging-sensitive.
- Single model (LaBSE); small effects; exploratory, not pre-registered.
