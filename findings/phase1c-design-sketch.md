# Phase 1c Design Sketch: Non-English Source Analysis

**Date:** 2026-05-18
**Status:** **Design sketch, not pre-registration.** Captures the experimental design, methodology choices, pipeline requirements, and open questions before code is written. The pre-registration document (`findings/phase1c-preregistration.md`, to be written and externally timestamped before any analysis is run) will derive specific predictions and decision rules from this sketch.
**Author:** T. David Kinlaw

---

## Motivation

Phase 1b bounded the *between-translator* component of translator-as-confound at 19.5% of total within/cross-tradition variance, on two source families. The *broad* form of the constructivist objection (Katz, 1978) remains unaddressed: a century of anglophone scholar-tradition mutual citation, shared lexical conventions ("moksha" → "liberation"; "śūnyatā" → "emptiness"; "wu wei" → "non-action"), and shared editorial assumptions could impose a tradition-wide structural template on *all* English renderings simultaneously. Such a template would be invisible to any between-translator variance test within the anglophone tradition, and could in principle account for cross-tradition convergence we measure.

Phase 1c tests this directly by running CCB on non-English source texts using multilingual embeddings. If cross-tradition signal persists on original-language sources, the broad form of the constructivist objection takes a real hit. If it disappears, the cross-tradition signal we measured in Phase 1a may be largely anglophone-scholar-tradition artifact.

---

## Two parallel sub-experiments

### Phase 1c.1: Cross-lingual within-source variance decomposition

**Mirrors Phase 1b structure.** Adds original-language sources as additional "translators" within each source family.

| Source family | Existing English translators (Phase 1b) | Phase 1c.1 addition |
|---|---|---|
| Bhagavad Gita | Arnold, Telang, Swarupananda | Sanskrit original (GRETIL or similar) |
| Tao Te Ching | Legge, Goddard, Carus | Classical Chinese original (Chinese Text Project / Wikisource) |

The Sanskrit Gita and Chinese TTC are treated as additional "books" within the same source_id. The W-S-B-T mask (within-source between-translator) now includes cross-lingual pairs (English × Sanskrit, English × Chinese, etc.).

**Headline test:** does the multilingual embedding preserve source identity across language? Concretely: is `same-source-cross-language` mean cosine within striking distance of `same-source-different-English-translator` mean cosine, or substantially lower?

- If close: multilingual embedding preserves source content across translation language, supporting the methodology choice and bounding the broad form of translator-as-confound.
- If substantially lower: either the multilingual embedding underperforms on classical languages, or English translations *do* impose a register/style overlay that multilingual embedding sees through. Phase 1c.1 would need follow-up disambiguation.

### Phase 1c.2: Cross-tradition non-English CCB

**Mirrors Phase 1a/1b advaita × theravada RECOGNITION result.** The headline cross-tradition finding from the project (Phase 1a technical-only-tagger RECOGNITION advaita × theravada = 0.531) was on English translations: Arnold's Sanskrit-Gita and Müller's Pali-Dhammapada (or similar). Phase 1c.2 tests whether the cross-tradition signal persists on original-language sources.

| Tradition | Phase 1c.2 source candidates | Language |
|---|---|---|
| Advaita Vedanta | Bhagavad Gita, principal Upanishads (Mundaka, Mandukya, Katha) | Sanskrit |
| Theravada Buddhism | Dhammapada, selected Suttas (Dīgha Nikāya, Majjhima Nikāya highlights) | Pali |

CCB applied to a non-English corpus consisting of Sanskrit Advaita texts and Pali Theravada texts. Concept tagging via multilingual prototype-embedding similarity (Option B, see below) with Option A spot-check.

**Headline test:** does RECOGNITION binding (or any of the five Phase 1a-binding concepts) survive on Sanskrit-vs-Pali source texts via multilingual embedding?

---

## Methodology choices

### Embedding models

Two multilingual models for cross-model replication, mirroring the Phase 0/1a OpenAI + ONNX MiniLM strategy:

1. **LaBSE** (Language-agnostic BERT Sentence Embedding, Google). 109 languages. Trained explicitly for cross-lingual sentence similarity using parallel data. Strongest theoretical fit for our use case. Available via Hugging Face / sentence-transformers.
2. **multilingual-e5-large** (Microsoft). 100 languages. General-purpose multilingual embedding with strong retrieval performance. Different architecture and training data from LaBSE; serves as the cross-model replication check.

Both run via ONNX Runtime where available (otherwise sentence-transformers / torch). Embedding dimension: LaBSE 768, multilingual-e5-large 1024. Unit-normalized as in Phase 1a/1b.

**Known limitation:** Both models were trained predominantly on modern web text. Classical Sanskrit and Pali corpora are sparse in training data. We must empirically validate embedding quality on our source texts before drawing methodological conclusions. The validation step (below) is a load-bearing prerequisite.

### Embedding-quality validation (sanity check before main analysis)

Before running Phase 1c.1/1c.2, validate that the multilingual embeddings produce sensible similarities on a controlled known-parallel test set:

- Take ~20 verses from the Bhagavad Gita where we have both Sanskrit original and a high-quality English translation (Arnold or Telang).
- Embed each verse in Sanskrit and in English.
- Check: is the cross-lingual same-verse similarity meaningfully higher than cross-lingual different-verse similarity?
- If yes (≥ 0.4 cosine cross-lingual same-verse with clear separation from different-verse), proceed with main analysis.
- If no (cross-lingual same-verse not distinguishable from random pairs), the multilingual embedding is not capturing classical Sanskrit semantics adequately. Stop and reconsider approach (alternative models, transliteration vs Devanagari script, smaller chunks, etc.).

This validation step is the gate. Without it, the rest of Phase 1c is uninterpretable.

### Concept tagging: Option B with Option A spot-check

**Option B (multilingual prototype embedding):** For each of the seven structural concepts (ULTIMATE, SUBSTRATE, AWARENESS, WORLD, SELF, RECOGNITION, NONSEP), construct an English prototype phrase (or short phrase set) that semantically anchors the concept. Embed each prototype with the multilingual model. Tag any chunk in any language whose cosine similarity to the prototype exceeds a threshold.

Example prototypes (to refine):
- AWARENESS: "consciousness awareness mind cognition perception"
- ULTIMATE: "supreme reality absolute brahman the divine ground of being"
- SUBSTRATE: "emptiness fundamental nature underlying field implicate order"

Thresholds: calibrated on a held-out validation set to match the chunk-tagging rate observed in Phase 1a/1b English regex tagging. Tag rate calibration prevents the multilingual tagger from being either too aggressive (tags everything) or too sparse (tags nothing).

**Option A spot-check (Sanskrit/Pali concept dictionaries):** For 1-2 of the seven concepts (probably AWARENESS and ULTIMATE, the highest-binding in Phase 1a), construct manual Sanskrit and Pali concept term lists from standard scholarly glossaries (Monier-Williams Sanskrit-English Dictionary, Pali Text Society Pali-English Dictionary). Apply regex-style tagging on transliterated text. Compare Option B prototype-tagged chunks vs Option A regex-tagged chunks for the same concept on the same corpus. Report agreement metric (Cohen's κ or simple overlap). If agreement is high, Option B is validated for the broader concept set. If low, methodology needs revisiting.

### Pre-registration plan

After this design sketch is accepted and the embedding-quality validation passes, write `findings/phase1c-preregistration.md` with specific quantitative predictions, decision rules, and corpus composition. Commit and externally timestamp via public GitHub + Zenodo release before running the main analysis (mirroring the Phase 1b pre-registration process).

For the present design sketch, predictions are deferred — they require knowing the embedding-quality calibration first.

---

## Pipeline requirements

New infrastructure needed beyond Phase 1b:

1. **Multilingual embedder script** (`scripts/multilingual_embedder.py`). Loads LaBSE or multilingual-e5-large. Handles Sanskrit Devanagari / IAST transliteration, Pali transliteration, Classical Chinese, etc. Probably via sentence-transformers + ONNX where possible.
2. **Source fetchers for new repositories.** GRETIL (Sanskrit), SuttaCentral (Pali), Chinese Text Project / Wikisource (Classical Chinese). Each likely needs its own `fetch_*` function in `scripts/fetch_books.py`, similar to the `sacred_texts` extension we added for Phase 1b.
3. **Multilingual concept tagger** (`scripts/multilingual_concept_tagger.py`). Implements Option B prototype-embedding tagging. Calibrates thresholds against Phase 1a English tag rates.
4. **Phase 1c.1 analysis script** — extension of `scripts/phase1b_within_source_variance.py` to handle cross-lingual within-source pairs in the variance decomposition.
5. **Phase 1c.2 analysis script** — extension of `scripts/sentence_binding_vectorized.py` / `scripts/concept_analysis.py` to run CCB on non-English chunks with multilingual prototype tagging.
6. **Validation script** (`scripts/multilingual_embedding_validation.py`) — runs the known-parallel test set sanity check before main analyses.

---

## Source acquisition

Candidate primary sources (to verify availability):

| Source | Language | Repository | Format |
|---|---|---|---|
| Bhagavad Gita | Sanskrit (Devanagari + IAST) | GRETIL `1_sanskr/2_epic/mbh/sanskrit/bhg_v.htm` or similar | UTF-8 text or HTML |
| Bhagavad Gita | Sanskrit | sanskritdocuments.org | UTF-8 text |
| Mundaka Upanishad | Sanskrit | GRETIL | UTF-8 |
| Katha Upanishad | Sanskrit | GRETIL | UTF-8 |
| Mandukya Upanishad | Sanskrit | GRETIL | UTF-8 |
| Dhammapada | Pali (Roman transliteration) | SuttaCentral suttacentral.net/dhp | UTF-8 / JSON API |
| Selected Suttas (DN/MN highlights) | Pali | SuttaCentral | UTF-8 / JSON API |
| Tao Te Ching | Classical Chinese | Chinese Text Project ctext.org or Wikisource | UTF-8 |
| Zhuangzi (Inner Chapters) | Classical Chinese | Chinese Text Project | UTF-8 |

All sources public domain (ancient texts; no copyright on the original). The English translations are already in our corpus for cross-language pair comparison.

---

## Open questions

1. **Sanskrit script choice: Devanagari vs IAST transliteration?** Multilingual embedding models likely have more training exposure to Devanagari (Wikipedia Sanskrit is Devanagari) but transliteration might map better to existing Sanskrit-related English text in training. Validation step decides.
2. **Pali transliteration variants.** Pali Text Society convention vs ISO 15919 vs Velthuis vs Harvard-Kyoto. SuttaCentral uses a specific style. Standardize before chunking.
3. **Classical Chinese tokenization.** Modern Chinese tokenizers (jieba etc.) are tuned for Modern Chinese. Classical Chinese is structurally different (no word boundaries, different grammar). Embedding-level may sidestep this, but worth flagging.
4. **Concept prototype phrasing.** The English prototype for each concept must be carefully chosen because it anchors all subsequent cross-lingual tagging. A pilot run on Phase 1a English chunks (comparing prototype-tagging vs regex-tagging) calibrates this.
5. **Chunk size for non-English.** Phase 1b used ~500-token chunks. Token counts differ across languages (Sanskrit verses are often 32 syllables; Pali stanzas vary; Classical Chinese is character-dense). May need language-specific chunking.
6. **Cross-tradition pair construction for Phase 1c.2.** Sanskrit-Sanskrit pairs are within-tradition (Advaita); Pali-Pali pairs are within-tradition (Theravada); Sanskrit-Pali pairs are cross-tradition. The cross-tradition signal is what we're testing. Pair counts need to be balanced.

---

## Anticipated failure modes

Named in advance, to be reported transparently if they occur:

1. **Embedding-quality validation fails.** Multilingual models cannot reliably distinguish same-verse from different-verse pairs across Sanskrit-English. Phase 1c stops at validation. Report this as itself a finding (limit of current multilingual models for classical languages).
2. **Concept prototype tagging diverges substantially from regex tagging on English.** Option B doesn't agree with Option A on the same English chunks. Suggests Option B can't be trusted on non-English where regex isn't available. Phase 1c.2 becomes interpretation-limited.
3. **Classical Chinese embedding is qualitatively different from Sanskrit/Pali embedding.** The TTC half of Phase 1c.1 produces very different patterns from the Gita half. Suggests classical Chinese is poorly served by these models specifically.
4. **Cross-tradition signal persists, but at substantially lower magnitude.** Phase 1c.2 detects nonzero advaita × theravada binding on Sanskrit-vs-Pali, but at ~30% of the English (Phase 1a) magnitude. Ambiguous: could be real partial-signal preservation, or could be lower embedding quality on classical languages. Disambiguation requires concept-prototype agreement spot-check + cross-model replication.
5. **Cross-tradition signal completely disappears.** Phase 1c.2 finds advaita × theravada binding near zero on original-language sources. Major finding: cross-tradition signal in Phase 1a was substantially anglophone-scholar-tradition mediated. The mysticism paper must update to acknowledge this. The CCB methodology is still useful (it's the test that revealed the dependency), but the mysticism application's positive claim weakens.

---

## What this design sketch does *not* commit to

This document is a design sketch, not a pre-registration. The specific predicted numerical outcomes, decision thresholds, and statistical tests will be committed in a separate `findings/phase1c-preregistration.md` to be authored after embedding-quality validation completes. Pre-registration before main-analysis execution maintains the Phase 1b discipline (predictions externally timestamped before data observation).

---

## Phase 1c.1 + 1c.2 staged milestones

1. **Source acquisition + cleaning + chunking** (~ 2-4 days). Fetch Sanskrit Gita, principal Upanishads, Pali Dhammapada / Suttas, Classical Chinese TTC. Build appropriate fetchers; clean and chunk.
2. **Multilingual embedder integration** (~ 1-2 days). Get LaBSE and multilingual-e5-large working via sentence-transformers (and ONNX where possible). Validate dependencies, performance.
3. **Embedding-quality validation** (~ 1 day). Known-parallel test set: Sanskrit-English Gita verse pairs. Decision gate.
4. **Concept prototype construction + tag-rate calibration** (~ 1-2 days). Choose prototypes; pilot on Phase 1a English; calibrate threshold against regex tag rate; report agreement.
5. **Option A spot-check dictionaries** (~ 1 day). Sanskrit and Pali concept term lists for AWARENESS and ULTIMATE.
6. **Pre-registration document** (~ 0.5 day). Predictions, decision rules, corpus composition; external timestamping commit + Zenodo release.
7. **Phase 1c.1 analysis** (~ 1 day). Cross-lingual variance decomposition. Compare to Phase 1b.
8. **Phase 1c.2 analysis** (~ 1 day). CCB on non-English corpus. Compare to Phase 1a.
9. **Writeup** (`findings/phase1c-multilingual.md`, ~ 1-2 days).
10. **Paper Draft 7 with §6.10 Phase 1c section** (~ 1-2 days).

Total realistic: 2-3 weeks at the Phase 1b cadence, longer with research interruptions.

---

*This document is a design sketch for Phase 1c. The pre-registration with specific predictions will be authored separately and externally timestamped before any Phase 1c main analysis is run.*
