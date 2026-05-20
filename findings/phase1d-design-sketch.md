# Phase 1d Design Sketch: High-Resource-Language Translation Triangulation

**Date:** 2026-05-20
**Status:** **Design sketch, not pre-registration.** Captures the experimental design and rationale. A formal pre-registration (`findings/phase1d-preregistration.md`) with specific predictions, decision rules, and per-language resolution gates will be authored and externally timestamped before any Phase 1d main analysis.
**Author:** T. David Kinlaw

---

## Motivation: what Phase 1c established and why it forces this design

Phase 1c set out to test the *broad* constructivist objection (the cross-tradition convergence measured in Phase 1a/1b on English translations could be an artifact of the anglophone scholar-translation tradition) by running CCB on original-language Sanskrit/Pali text. It established three things:

1. Multilingual embeddings coarsely match parallel content across language (validation passed).
2. They cannot tag fine-grained concepts across language via English prototypes (Option B failure).
3. **They do not resolve fine-grained concept structure within classical Sanskrit/Pali at all** — the within-language diagnostic showed 6/7 concepts resolve in English but only 2/7 in Sanskrit, failing on AWARENESS and RECOGNITION specifically, under both e5-large and LaBSE (`findings/phase1c-multilingual.md` §7c).

The original-language approach is therefore blocked: the cross-tradition null is a model-resolution artifact, uninformative about the traditions. The problem is **low-resource language**, not non-English per se.

## The design: independent translation communities as independent measurement methods

Phase 1d separates the two things the original-language approach conflated — escaping the anglophone tradition AND using low-resource languages — by using **high-resource modern languages** the model resolves well, translated by **independent (non-anglophone) translator communities**.

The logic is convergent validity / multitrait-multimethod triangulation:
- Each target language is a *method* with its own *method-variance*: that translator community's conventions, lexical norms, interpretive frame. Anglophone Indologists, Hindi scholars, and Chinese Buddhist translators do not share conventions.
- The cross-tradition structural convergence is the *trait*.
- A trait that appears across methods whose error sources are independent is trait variance (real signal), because independent methods do not share a bias to manufacture the same convergence.

### Three outcomes and their interpretation

1. **Convergence across all three languages (English, Hindi, Chinese):** most parsimonious explanation is source-content convergence — three independent communities are vanishingly unlikely to coincidentally project the same structure. Supports the perennialist reading.
2. **Convergence only in English:** anglophone-community-specific. Supports the narrow-constructivist reading (the Phase 1a result was an artifact of one translation tradition).
3. **Convergence in all three but with *different concept patterns* per language:** each community projects its own structure (different structure each). Supports a broad constructivism that single-language analysis could not have distinguished from case 1.

Case 3 is the subtle one and is the reason the design is powerful: it separates "real shared structure" from "each community imposes structure, but a different one."

## Target languages

| Language | Hindu (Advaita) source coverage | Buddhist (Theravada) source coverage | Resolution prior | Independence caveat |
|---|---|---|---|---|
| English ✓ (done) | Gita, Upanishads (Arnold/Telang/Swarupananda, Müller) | Dhammapada (Radhakrishnan) | high (6/7 resolved) | the tradition under test |
| Hindi | abundant (Gita, Upanishads) | available (20th-c. Indian Buddhist revival) | high (modern Devanagari, large web presence) — VERIFY | shares Sanskrit religious lexicon (ब्रह्म, मोक्ष, निर्वाण); sits "close" to source |
| Modern Chinese | sparse (modern translations exist) | abundant (法句經 = Chinese Dhammapada; 2,000-yr Chinese Buddhist canon) | high — VERIFY | ancient géyì 格義 tradition matched Buddhist terms to Daoist vocabulary; its own deep overlay |

Hindi is the cleanest single addition (both traditions natively translated, high-resource). Chinese adds a linguistically alien third method but with asymmetric coverage (rich Buddhist, thin Hindu).

## Mandatory per-language resolution gate

The Phase 1c lesson is built in as a precondition: **before any language's cross-tradition CCB result counts, that language must pass the within-language concept-binding diagnostic** (`scripts/within_language_concept_binding.py`) — the model must resolve concept structure within that language (target: ≥ the English 6/7, or at minimum significant binding for AWARENESS and RECOGNITION, the headline concepts). If a language fails the gate, its CCB null/positive is uninterpretable and is excluded from the triangulation, reported transparently.

This also guards a subtle confound: if the multilingual model resolves English > Hindi > Chinese by training-data volume, CCB differences across languages could be resolution artifacts rather than translation-community differences. The per-language gate, plus reporting each language's within-language resolution alongside its cross-tradition CCB, controls for this.

## Open questions for the pre-registration

1. **Same multilingual model across all languages, or per-language monolingual models?** Same multilingual model makes the cross-language comparison apples-to-apples but inherits the resolution gradient. Per-language monolingual models (English MiniLM, Hindi BERT, Chinese BERT) resolve each language natively but make cross-model comparison harder. Likely: report both; lead with same-multilingual-model gated by per-language resolution.
2. **Translator independence is partial.** Hindi/Chinese scholars often read anglophone scholarship; some translate *from* English. Pre-register this as a limitation; consider sourcing translations made directly from the original where documented.
3. **Hindi-Sanskrit vocabulary overlap.** Hindi convergence may partly reflect Hindi≈Sanskrit rather than independent confirmation. Chinese (linguistically alien) is the cleaner independence test; weight it accordingly.
4. **Concept tagging per language.** Option A (manual regex) per language, from standard bilingual glossaries. Hindi can largely reuse the Sanskrit Devanagari dictionaries (shared lexicon); Chinese needs a new Hanzi concept dictionary.
5. **Statistical comparison across languages.** Report in relative terms (effect sizes, binding ratios) not absolute cosines, per the Draft 6 §8 methodology lesson, since each language/model has a different cosine range.

## Why this is the strongest version of the project's argument

The English-only Phase 1a/1b result could not address the broad-constructivist objection — it had no way to separate source-content convergence from anglophone-translation-convention convergence. Phase 1d directly attacks that confound by triangulating across independent translation communities. Whichever way it resolves, it is a stronger and more publishable result than the single-language analysis, and it is the natural culmination of the corpus-expansion arc (Phase 1a verified text → Phase 1b multi-translator → Phase 1c original-language → Phase 1d multi-language triangulation).

## Staged plan

1. Source Hindi Gita + Hindi Dhammapada (and Hindi Upanishads, Hindi suttas if available). Source Chinese 法句經 + a modern Chinese Gita.
2. Clean, chunk, language-tag.
3. Per-language within-language resolution diagnostic (the gate).
4. Build Hindi (Devanagari, largely reuses Sanskrit dictionary) and Chinese (Hanzi) Option A concept dictionaries.
5. Pre-register predictions + decision rules + per-language gates. External timestamp.
6. Run cross-tradition CCB per language; compare patterns across languages.
7. Write findings; paper Draft 7/8 §6.x.

---

*Design sketch for Phase 1d. The pre-registration with specific predictions and the per-language resolution gates will be authored separately and externally timestamped before any Phase 1d main analysis.*
