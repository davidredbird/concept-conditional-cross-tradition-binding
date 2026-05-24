# Phase 2a — multilingual cross-tradition CCB: complete summary

**Dates:** 2026-05-20 (single intensive session)  **Status:** COMPLETE, EXPLORATORY (not pre-registered)
**Headline:** A 9-language stress-test of the Phase 0/1 concept-binding findings that
**dissociates likely-structural convergence from vocabulary-driven convergence** —
the project's sharpest methodological result, and one that materially revises the
Phase 1 "AWARENESS is the headline" framing.

## Goal

Phase 0/1 found cross-tradition concept-binding in an English corpus
(OpenAI/MiniLM embeddings). The obvious confound: convergence could be an artifact
of shared English translation vocabulary. Phase 2a tests every concept in
**original and translated non-English corpora**, asking which bindings survive a
change of language — and what mechanism drives those that don't.

## Method

- **Within-language cross-tradition CCB**, one language at a time: two traditions
  in the same language, CCB(C) = mean_cos(both-tagged C, cross-tradition) −
  mean_cos(one-tagged C, cross-tradition), permutation null on tags.
- **One embedding model throughout: LaBSE** (`sentence-transformers/LaBSE`). e5-large
  was tested and *abandoned for CCB* — it anisotropically cone-collapses non-English
  (and even French) into a ~0.84 cosine cone (std ~0.02), an order of magnitude below
  the concept signal. LaBSE keeps healthy spread (cross-tradition cosine ~0.45–0.65).
- **Gate-first** (the Phase 1c lesson): before trusting any CCB, confirm LaBSE
  resolves concept structure *within* that language (within-tradition binding). All
  9 languages passed (6–7/7), unlike Sanskrit/Pali (2/7, abandoned).
- **Per-language Option-A concept dictionaries** (Hanzi, Arabic, Devanagari, kana+kanji,
  Hebrew w/ niqqud-stripping, polytonic-Greek, French/Spanish/English regex). Each
  carries the hidden-DoF + broad-tagging caveat.
- **Stage-1 representation screen** (FLORES+ tokenizer fertility + retrieval): showed
  these proxies are necessary-but-not-sufficient — they rule a language *out*, not
  *in*. Eligibility = the within-language gate. (`phase2a-stage1-representation-screen.md`)

## The 9 configurations (all LaBSE, within-language)

| configuration | language type | source | AWARENESS | SUBSTRATE | ULTIMATE | WORLD |
|---|---|---|---|---|---|---|
| Chinese Buddhist×Daoist | orig, separate lineage | CBETA/ctext | **flat** | binds | binds | binds |
| Hebrew Hasidic×Rationalist | orig, divergent register | Sefaria | **flat** | binds | binds | no |
| Greek Neoplatonism×Christian | orig, low-contrast | First1KGreek | **flat** | (ὕλη artifact) | binds | binds |
| Arabic Sufi×Falsafa | orig, shared lineage | OpenITI | binds | binds | binds | binds |
| Hindi Kabir×Tulsidas | orig, shared lexicon | hi.wikisource | binds | binds | binds | binds |
| Spanish Quietist×Carmelite | orig, max overlap | es.wikisource | binds (+.037) | binds | binds | binds |
| French Daoist/Vedanta/Christian | translated | fr.wikisource | binds | flat | binds | binds |
| English Dhammapada×TTC | translated | PG/local | binds (2/3 tr.) | weak | mixed | binds |
| Japanese Buddhist×Confucian | rendered | ja.wikisource | binds | binds | binds | no |

Per-language detail in: `phase2a-{chinese,french,english-labse-model-control,arabic,
japanese,hindi,hebrew,spanish}-cross-tradition-ccb.md` and `phase2a-crosslingual-and-synthesis.md`.

## The two robust claims

**1. ULTIMATE = role-convergence.** Binds within-language in ALL 9 configurations
(most robust within-language), yet is the *weakest* cross-language (pooled CCB
+0.004) — because it is carried by tradition-specific *names* (God / Allah / Dao /
Brahman / τὸ ἕν) that LaBSE does not co-locate across languages. Interpretation:
each tradition's "ultimate" occupies the analogous *structural role* within its own
discourse, not a shared cross-lingual embedding region.

**2. AWARENESS = vocabulary-overlap effect (the key dissociation).** Binds wherever
the two traditions share an awareness-lexicon — shared lineage (Arabic, Hindi),
shared school (Spanish, strongest at +0.037), or translation/rendering imposing
shared terms (English, French, Japanese) — and goes **flat** wherever the
awareness-lexicons diverge: separate lineage (Chinese 識/覺 vs 心/神), register
(Hebrew mystical vs rationalist), or low-contrast Greek. The clean
language-controlled proof: **the SAME works (Dhammapada × Tao Te Ching) bind
AWARENESS in English translation but not in the original classical Chinese.**

**SUBSTRATE** binds in the original-language traditions that have a genuine
emptiness/non-being concept (Chinese 空, Arabic ʿadam/fanāʾ, Hindi, Hebrew ayin,
Spanish nada) and is diluted by translation (French/English) or mis-mapped
(Greek ὕλη=matter≠emptiness). It is the strongest candidate for genuine,
language-independent *structural* convergence, but is concept-mapping-sensitive.

## Cross-lingual capstone

Pooling all 9 languages into the shared LaBSE space and testing cross-language
pairs only: **all 7 concepts bind weakly-but-significantly** (NONSEP/SUBSTRATE
strongest, ULTIMATE weakest). **But this is a weaker test** than within-language —
LaBSE is trained for cross-lingual semantic alignment, so concept-passages
clustering across languages partly reflects the model aligning same-topic text, not
tradition convergence. Needs a non-bitext-trained model to corroborate.

## What it means for the project's central claim

Phase 1 promoted **AWARENESS (Mahayana×Theravada)** as the cleaner poster-child over
the Rovelli–Nagarjuna **SUBSTRATE** convergence. Phase 2a **inverts** this:
- AWARENESS convergence is substantially a shared-vocabulary / translation artifact.
- SUBSTRATE and ULTIMATE are the durable signals — SUBSTRATE as structural
  convergence among emptiness-traditions, ULTIMATE as role-convergence.

The paper's framing should move from "mysticism converges (AWARENESS headline)" to
"CCB *dissociates* structural convergence from vocabulary convergence across 9
languages" — a stronger, more defensible, and more falsifiable methodological contribution.

## Methodological lessons (reusable)

- LaBSE for CCB, never e5-large (anisotropy). Report anisotropy alongside every gate.
- Gate-first per language; representation proxies (fertility/retrieval) rule out, not in.
- Tagging breadth must be matched across the cells being compared (the English
  technical-only regex vs Chinese broad Hanzi dict nearly broke the EN-vs-ZH comparison).
- Sourcing reality: clean ≥2-tradition single-language PD corpora exist for EN, ZH,
  FR, AR (OpenITI), HI (hi.wikisource), HE (Sefaria), ES, EL (First1KGreek), JA.
  Walls: German/modern-Chinese (no clean 2nd tradition), Tibetan/Bön (sparse),
  Sanskrit/Pali (fail the gate). Gutenberg has almost no non-English tradition text.

## Caveats

- Single embedding model (LaBSE); per-language Option-A dicts (hidden DoF, varying
  breadth/saturation); EXPLORATORY, not pre-registered; effect sizes modest;
  cross-lingual result confounded by the embedder's alignment objective.

## Open threads → Phase 2b

- Pre-register the vocabulary-overlap hypothesis before new tradition pairs.
- Non-LaBSE corroboration of the cross-lingual result.
- **Phase 2b: same-works-across-languages** (parallel corpus) — the cleanest design,
  generalizing the Dhammapada×TTC EN-vs-ZH control to many works × many languages.
  See `phase2b-design-sketch.md`.
