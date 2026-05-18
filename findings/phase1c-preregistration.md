# Phase 1c Pre-registration: Multilingual Source Analysis

**Pre-registration date:** 2026-05-18
**Author:** T. David Kinlaw, ORCID [0009-0008-5213-1017](https://orcid.org/0009-0008-5213-1017)
**External timestamping mechanisms:**
- Public GitHub commit on this document (timestamp visible on the commit page; controlled by GitHub infrastructure, not the author)
- Zenodo release `v1.3-prereg-phase1c` cut at the same commit (third-party DOI-resolved timestamp via DataCite)

**Status:** Pre-registered prior to running any Phase 1c main analysis. The embedding-quality validation gate has passed for both candidate models on the validation pair set (`corpus/phase1c_validation_pairs.jsonl`; both models scored 5/5 cross-lingual same-verse matching, decision PASS — see `results/phase1c/embedding_validation.json`). The corpus has not yet been fetched; the analysis scripts have not yet been authored; predictions are committed before observation.

---

## 1. Motivation and design

Phase 1b bounded the *between-translator* component of translator-as-confound at 19.5% of total within/cross-tradition variance, on two source families (Bhagavad Gita and Tao Te Ching). The complementary objection — that the anglophone scholar-translator tradition itself imposes structural conformity *across* its individual translators, invisible to within-tradition between-translator variance — remains unaddressed. This is Katz (1978)'s broader form of the constructivist position applied to NLP-on-religious-texts.

Phase 1c tests this objection directly by running CCB on non-English source texts using multilingual embedding models, in two parallel sub-experiments:

- **Phase 1c.1: Cross-lingual within-source variance decomposition.** Mirrors Phase 1b's structure. Adds Sanskrit Bhagavad Gita and Classical Chinese Tao Te Ching as additional "translators" within the existing multi-translator source families. Tests whether multilingual embedding preserves source identity across translation language at a level comparable to within-language between-translator variance.

- **Phase 1c.2: Cross-tradition non-English CCB.** Mirrors Phase 1a's structure. Pure non-English corpus: Sanskrit Advaita (Bhagavad Gita + principal Upanishads) on one side, Pali Theravada (Dhammapada + selected Suttas) on the other. Tests whether the cross-tradition CCB signal that Phase 1a measured on English translations survives on original-language sources via multilingual embedding and prototype-based concept tagging.

Both sub-experiments use **cross-model replication**: each runs with both `intfloat/multilingual-e5-large` (ONNX, mean-pool, `passage:` prefix) and `sentence-transformers/LaBSE` (canonical CLS + tanh + dense + L2norm via sentence-transformers). Validation passed on both at 5/5 same-verse cross-lingual matching with separations +0.055 and +0.247 respectively.

This pre-registration mirrors the Phase 1b discipline: external timestamping via public GitHub commit and Zenodo DOI before main analysis. The author has explicitly triple-checked predictions against the test mechanism (§5 operationalization sanity check below) to avoid the H1b.3-style inequality-direction error documented in Appendix C of Draft 6.

---

## 2. Pre-specified corpus

### 2.1 Phase 1c.1 corpus additions to Phase 1b

| Source family | New book | Language | Provenance |
|---|---|---|---|
| Bhagavad Gita (`source_id: bhagavad_gita`) | Sanskrit Bhagavad Gita (Devanagari, verses only, no commentary) | sanskrit | GRETIL `gretil/corpustei/transformations/html/sa_bhagavadgItA-comm.htm`, filtered to verse-only |
| Tao Te Ching (`source_id: tao_te_ching`) | Classical Chinese Tao Te Ching | classical_chinese | ctext.org `/dao-de-jing/zh` |

Chunks tagged with a new `language` metadata field: `english`, `sanskrit`, `classical_chinese`. Existing Phase 1b chunks default to `english`. Fallback URLs documented if primary sources fail (sanskritdocuments.org, sa.wikisource.org).

### 2.2 Phase 1c.2 corpus

| Tradition | Texts | Language | Provenance |
|---|---|---|---|
| advaita | Bhagavad Gita | sanskrit | GRETIL (same as 1c.1) |
| advaita | Mundaka Upanishad, Katha Upanishad, Mandukya Upanishad | sanskrit | GRETIL `corpustei` HTML transformations |
| theravada | Dhammapada (Pali) | pali | SuttaCentral API `/api/bilarasuttas/dhp1-20/pli`, `dhp21-32/pli`, ..., concatenated |
| theravada | Selected Pali Suttas (DN 22 Mahasatipatthana, MN 10 Satipatthana, MN 118 Anapanasati) | pali | SuttaCentral API |

**Minimum acceptable corpus:** Sanskrit Bhagavad Gita + 2 Upanishads, Pali Dhammapada + 1 Sutta. If fewer texts are successfully fetched, Phase 1c.2 reports as underpowered and the failure is documented; no result-driven corpus revision is permitted.

Chunking: same `scripts/chunk_books.py` pipeline as Phase 1b, ~500-token chunks at paragraph boundaries, with adjustments for short-verse texts (sentence boundaries where paragraphs aren't apparent).

### 2.3 Embeddings

All Phase 1c chunks (plus the Phase 1b multi-translator subset for variance comparison in 1c.1) are re-embedded with both:
- `intfloat/multilingual-e5-large` via ONNX Runtime (`scripts/multilingual_embedder.py` backend `onnx`), with `passage: ` prefix on all inputs
- `sentence-transformers/LaBSE` via sentence-transformers (`scripts/multilingual_embedder.py` backend `sentence_transformers`), canonical pipeline

Cosine similarities computed on unit-normalized embeddings. Per-model results reported separately; cross-model agreement is reported.

---

## 3. Concept tagging design

### 3.1 Option B: multilingual prototype embedding

For each of the seven pre-specified structural concepts (ULTIMATE, SUBSTRATE, AWARENESS, WORLD, SELF, RECOGNITION, NONSEP), construct a multilingual prototype phrase by concatenating the existing English regex pattern dictionary terms (from `scripts/concept_analysis.py`). Embed the prototype phrase with the same multilingual model used for chunk embedding. Tag each chunk with concept *C* if the cosine similarity between the chunk embedding and the *C* prototype embedding exceeds a per-concept threshold.

The prototype phrase for each concept is **pre-specified before validation runs** and constructed mechanically from existing pattern dictionaries — no result-driven prototype tuning is permitted post-hoc.

Prototype construction rule: take the union of the technical-only and full pattern dictionary terms for each concept (as in `scripts/concept_analysis.py` and `TECHNICAL_ONLY_PATTERNS`), strip regex syntax, deduplicate, and concatenate space-separated. Prototype is the same across both models (same input text, different embedding).

### 3.2 Threshold calibration (pre-registered procedure)

Per-concept threshold is calibrated to match the per-concept tag rate observed in Phase 1a English regex tagging:

1. For each concept *C*, count the fraction *r(C)* of Phase 1a English chunks that were regex-tagged as containing *C*.
2. On the Phase 1c corpus, sort chunks by cosine similarity to the *C* prototype embedding.
3. Set the threshold so that the top *r(C)* fraction of chunks are tagged with *C*.

This produces a tag-rate-matched multilingual tagger. Calibration is performed once per model per concept, before main analysis.

### 3.3 Option A spot-check (validation of Option B)

Before Phase 1c.2 main analysis runs, the Option B tagger is validated against manually-constructed Sanskrit and Pali concept dictionaries for **two specific concepts** chosen for their Phase 1a strength: **AWARENESS** and **RECOGNITION**.

Manual dictionaries are constructed from standard scholarly sources:
- **Sanskrit AWARENESS terms** (from Monier-Williams Sanskrit-English Dictionary): `cit`, `caitanya`, `cetana`, `vijñāna`, `jñāna`, `bodha`, `prajñā`, `anubhava`, `vimarśa`
- **Sanskrit RECOGNITION terms**: `mokṣa`, `mukti`, `kaivalya`, `nirvāṇa` (in Hindu usage), `jīvanmukti`, `bodhi`, `samādhi`, `pratyabhijñā`, `siddhi`
- **Pali AWARENESS terms** (from Pali Text Society Pali-English Dictionary): `citta`, `viññāṇa`, `paññā`, `ñāṇa`, `sati`, `sampajañña`
- **Pali RECOGNITION terms**: `nibbāna`, `bodhi`, `nirodha`, `mokkha`, `cetovimutti`, `paññāvimutti`, `samādhi`

Regex tagging is applied with these dictionaries on the Phase 1c.2 corpus (script-aware for Devanagari vs IAST). For each of AWARENESS and RECOGNITION:
- Compute the set of chunks tagged by Option A (manual regex)
- Compute the set of chunks tagged by Option B (prototype embedding)
- Report Cohen's kappa and percent agreement

**Decision rule:** If kappa < 0.5 OR percent agreement < 70% on either of AWARENESS or RECOGNITION, Option B is not validated and Phase 1c.2 results are reported as exploratory rather than confirmatory. If kappa ≥ 0.5 AND agreement ≥ 70% on both, Option B is validated and Phase 1c.2 results are reported as confirmatory.

---

## 4. Hypotheses and predictions

### 4.1 Phase 1c.1 hypotheses (cross-lingual within-source variance)

Pair-type masks extend Phase 1b's by adding a *language* dimension. To avoid the H1b.3-style operationalization ambiguity, X-S-W-T and X-T in Phase 1c.1 are explicitly restricted to **same-language** pairs (English-English for the existing Phase 1b corpus). Cross-lingual pairs appear only in the W-S-B-T-X-L mask (the new Phase 1c.1 addition). Cross-lingual cross-source-within-tradition pairs (e.g., Sanskrit Gita × English Upanishads) and cross-lingual cross-tradition pairs (e.g., Sanskrit Gita × English Dhammapada) are computed separately and reported, but are NOT used in the H1c.1 hypothesis tests.

| Mask | Definition | Language constraint |
|---|---|---|
| W-S-S-T | Same book_id (chunks within a single book/translator) | (single book, single language by construction) |
| W-S-B-T-W-L | Same source_id, different book_id | **same language** (English × English) |
| W-S-B-T-X-L | Same source_id, different book_id | **different language** (English × Sanskrit, English × Chinese) |
| X-S-W-T | Different source_id, same tradition | **same language only** (English × English) |
| X-T | Different tradition | **same language only** (English × English) |

Auxiliary masks (reported, not used in hypothesis tests):
- X-S-W-T-X-L: cross-source, within-tradition, cross-language (e.g., Sanskrit Gita × English Müller-Upanishads)
- X-T-X-L: cross-tradition, cross-language

**H1c.1.a (cross-lingual preserves source identity vs cross-source):** The mean cosine similarity for W-S-B-T-X-L pairs exceeds the mean for X-S-W-T pairs at *p* < 0.05 (permutation null over shuffled `source_id` assignments while preserving `tradition`).

**H1c.1.b (cross-lingual approaches within-language between-translator):** The gap between W-S-B-T-X-L and W-S-B-T-W-L means is small relative to total within-source variance:

    |mean(W-S-B-T-X-L) - mean(W-S-B-T-W-L)| / (mean(W-S-S-T) - mean(X-T)) < 0.20

I.e., cross-lingual same-source pairs differ from within-language between-translator pairs by less than 20% of the total within-source-to-cross-tradition variance range.

**H1c.1.c (variance ordering extends):** The Phase 1b variance ordering holds with the new layer inserted: W-S-S-T > W-S-B-T-W-L ≥ W-S-B-T-X-L > X-S-W-T > X-T. Strict inequality where confirmed numerically; ≥ where cross-lingual may match within-language.

### 4.2 Phase 1c.2 hypotheses (cross-tradition non-English CCB)

For each of the five Phase 1a-binding concepts (AWARENESS, RECOGNITION, WORLD, ULTIMATE, SUBSTRATE), compute CCB on the Sanskrit-Pali corpus:

    CCB(C) = mean_cos(pairs where both passages tagged C, cross-tradition) 
           - mean_cos(pairs where only one passage tagged C, cross-tradition)

Permutation null: shuffle concept tags within each chunk's existing tag-set across all chunks; observed CCB(C) compared to null distribution. One-sided *p*-value for observed > null.

**H1c.2.a (some Phase 1a-binding concepts survive multilingual):** At least 2 of the 5 Phase 1a-binding concepts show *p* < 0.05 (one-sided, observed > null) on the Sanskrit-Pali cross-tradition CCB analysis under at least one of the two multilingual models.

**H1c.2.b (AWARENESS and RECOGNITION specifically):** AWARENESS and RECOGNITION — the two strongest Phase 1a-binding concepts at sentence level — each show *p* < 0.05 in the Sanskrit-Pali analysis under at least one of the two multilingual models.

**H1c.2.c (cross-model agreement on direction):** For concepts that bind under both models, the direction of CCB (sign) agrees across models. Magnitude need not match (different absolute cosine scales between models).

### 4.3 Non-hypothesized but pre-specified controls

The two non-binding concepts from Phase 1a (SELF, NONSEP) are also computed and reported for control. No prediction is made for these; null results are expected but not pre-registered. Reporting them documents the full picture.

---

## 5. Operationalization sanity check (triple-check)

This section explicitly walks through what each prediction direction means at the level of test arithmetic, to avoid the H1b.3-style inequality-direction error documented in Draft 6 Appendix C.

### 5.1 H1c.1.a direction check

**Claim:** W-S-B-T-X-L mean > X-S-W-T mean.

**Translation:** Pairs that share source content but differ in language are *more* similar than pairs that share tradition but differ in source content.

**Why this direction predicts the substantive hypothesis (multilingual works):**
- If multilingual embedding preserves source-content semantics, English-Gita ↔ Sanskrit-Gita pairs cluster tightly (~ same content; W-S-B-T-X-L)
- X-S-W-T pairs as defined here are *English-English* different-source same-tradition (e.g., English-Gita ↔ English-Upanishad). They cluster less tightly than same-source pairs because content differs even though tradition vocabulary is shared.
- The substantive picture: source content is more determinative of similarity than tradition vocabulary, even when comparing *across language* (W-S-B-T-X-L) vs *within language but across source* (X-S-W-T).
- Therefore: cross-lingual same-source (higher) > same-language different-source (lower)
- Observed > null in the permutation test (shuffling source_id within tradition while preserving language and book_id) means the cross-lingual same-source pairs are non-randomly higher than cross-source same-language baselines.

**Failure direction:** If observed ≤ null, multilingual embedding is NOT preserving source content adequately. The signal would be tradition-vocabulary-mediated, not source-mediated. Refutation in this direction would suggest re-examining the embedding choice or admitting Phase 1c is not feasible.

### 5.2 H1c.1.b direction check

**Claim:** |mean(W-S-B-T-X-L) - mean(W-S-B-T-W-L)| / total-variance < 0.20.

**Translation:** Cross-lingual same-source similarity is close (in absolute value) to within-language between-translator similarity. The two means differ by less than 20% of the total within-source-to-cross-tradition range.

**Why this direction predicts the substantive hypothesis:**
- If multilingual embedding fully eliminates language as a confound, English-Gita ↔ Sanskrit-Gita should be as similar as Arnold-Gita ↔ Telang-Gita (or close to it)
- A small gap means language is not a major additional source of variance beyond translator stylistic differences
- A large gap would mean language IS a major additional confound, beyond translator differences

**Failure direction:** If the gap exceeds 20%, multilingual embedding adds a substantial language-specific signal that's not source content. This would be informative — the broad form of translator-as-confound has a real cousin (language-as-confound) at the multilingual embedding level — but would qualify Phase 1c's positive claim.

**Absolute value note:** Predicting absolute value < 20% is direction-agnostic because the gap could go either way. Cross-lingual could be lower than within-language (most plausible) OR higher (theoretically possible if e.g., the Sanskrit text is unusually similar to itself across translators). Both are accommodated.

### 5.3 H1c.2.a direction check

**Claim:** At least 2 of 5 Phase 1a-binding concepts show *p* < 0.05 (one-sided, observed CCB > null CCB).

**Translation:** For at least 2 concepts, the observed difference between "both-have-C" and "only-one-has-C" cross-tradition pair similarities exceeds the difference you'd see if concept tags were randomly assigned, by enough to be statistically significant.

**Why this direction predicts the substantive hypothesis:**
- CCB > 0 means concept-shared pairs are MORE similar than concept-asymmetric pairs
- If the concept genuinely binds across traditions, both-have-C should cluster (same topic) more tightly than only-one-has-C (different topic)
- Observed CCB > null CCB means the observed binding is not explainable by random tag assignment
- This is the canonical CCB direction — same as Phase 0, Phase 1a, Phase 1b

**Failure direction:** If observed CCB ≤ null CCB, concepts do not bind significantly. Substantive interpretation depends on what fails:
- All 5 fail → cross-tradition signal was anglophone-tradition artifact. Major qualification to Phase 1a's positive claim required.
- Some fail (1-4 of 5) → partial preservation. Phase 1c.2 surfaces which concepts are robust to multilingual analysis and which are not.

### 5.4 H1c.2.b direction check

**Claim:** Each of AWARENESS and RECOGNITION individually shows *p* < 0.05 under at least one model.

This is a stricter version of 5.3. AWARENESS and RECOGNITION are the two specific concepts that bind most strongly in Phase 1a sentence-level analysis and on Mahayana × Theravada / advaita × theravada pairs. They are the "canonical" cross-tradition concept-binding finding the paper headlines.

**Failure direction:** If AWARENESS or RECOGNITION fails, the paper's canonical cross-tradition finding does not survive multilingual analysis. The mysticism application's positive claim weakens; the methodology paper remains because we ran the test honestly.

### 5.5 H1c.2.c direction check

**Claim:** For concepts that bind under both models (LaBSE and e5-large), the sign of CCB(C) is the same.

**Translation:** Cross-model replication requires that both models agree binding-direction, even if absolute magnitudes differ. CCB > 0 in one and CCB > 0 in the other is agreement. CCB > 0 in one and CCB < 0 in the other is disagreement.

**Failure direction:** If cross-model disagreement is common, the result is unreliable. Substantively this would mean either the prototype tagging is unstable across models (more likely cause) or the underlying signal is genuinely model-dependent (less likely but possible).

---

## 6. Decision rules

### 6.1 Phase 1c.1

| Outcome | H1c.1.a | H1c.1.b | H1c.1.c | Decision |
|---|---|---|---|---|
| All confirmed | TRUE | TRUE | TRUE | Multilingual embedding preserves source identity well; cross-lingual variance is bounded; cross-translator language-confound is small. Strong Phase 1c success. |
| H1c.1.a only | TRUE | FALSE | partial | Source identity preserved, but cross-lingual pairs are substantially less similar than within-language. Language is a real additional confound beyond translator. Methodology paper position qualified. |
| H1c.1.a fails | FALSE | irrelevant | FALSE | Multilingual embedding does not adequately preserve source identity. Phase 1c.2 results must be treated with caution; embedding limitation is the headline finding. |

### 6.2 Phase 1c.2

| Outcome | H1c.2.a | H1c.2.b | Decision |
|---|---|---|---|
| Strong | ≥4/5 bind | both | Cross-tradition CCB signal robustly survives multilingual analysis. Anglophone-scholar-tradition broad-form objection substantially weakened. |
| Moderate | 2-3/5 bind | one or both | Partial survival. Specific concepts robust, others not. Honest qualified position. |
| Weak | 1/5 binds | neither | Most cross-tradition signal does not survive multilingual analysis. Anglophone-tradition-mediation hypothesis supported. Phase 1a application result substantially qualified. |
| Null | 0/5 bind | neither | Cross-tradition signal does not survive multilingual analysis at all. Major qualification; mysticism application's positive claim withdrawn. CCB methodology paper stands (the test worked). |

### 6.3 Option B validation gate (precondition to 6.2)

If Option A vs Option B agreement is below threshold (kappa < 0.5 or accuracy < 70%) on AWARENESS or RECOGNITION, Phase 1c.2 results are reported as exploratory; H1c.2.a/b decisions are noted as conditional on tagger validity rather than final.

---

## 7. Anticipated failure modes

Named in advance, transparent reporting required if observed:

1. **Cross-lingual same-source pairs cluster much lower than within-language between-translator.** Most likely failure mode for H1c.1.b. Multilingual embedding adds language-specific signal beyond translator differences. Honest report; potentially mitigated by trying additional multilingual models in Phase 1d.
2. **Prototype tagging diverges substantially from manual Sanskrit/Pali regex tagging.** Option B is not validated on the spot-check. Phase 1c.2 reported as exploratory. Discussion of why prototype-based tagging may not transfer across script systems.
3. **CCB null distribution is too narrow or unstable.** With smaller corpora than Phase 1a, permutation null may not have enough variance for meaningful *p*-values. Report effective sample size and confidence intervals.
4. **Cross-model disagreement (H1c.2.c failure) is widespread.** Suggests either tagging instability or genuine model dependence. Report which model produced which result; do not silently pick the favorable one.
5. **The H1b.3-style inequality-direction error.** Each prediction has been checked twice (§5 sanity check). A third pass at execution time will verify the test's arithmetic direction matches the prediction. If a discrepancy is found, it is reported in the next paper draft's appendix (mirroring Draft 6 Appendix C) rather than silently revised.
6. **Corpus acquisition partial failures.** Some sources may not parse cleanly (GRETIL HTML has commentary mixed with verses; SuttaCentral chunking may need adjustments). Document what was successfully fetched; if minimum acceptable corpus (§2.2) not met, report Phase 1c.2 as underpowered rather than reducing the prediction set to fit available data.

---

## 8. Note on the H1b.3 lesson informing this prereg

Draft 6 Appendix C documents the H1b.3 inequality-direction error in Phase 1b's pre-registration: the underlying scientific hypothesis was correct but the predicted test-arithmetic direction was inverted, because the researcher had not traced through what the specific permutation null actually computes.

This prereg has been written with explicit operationalization sanity checks (§5) for each hypothesis, walking through the substantive scientific claim, the predicted test-direction, and what each failure direction would mean. The Phase 1c hypotheses use canonical CCB tests (observed > null on permutation of concept tags) where the direction is unambiguous, and permutation-on-source-id (not on translator labels) for H1c.1.a where the direction is checked explicitly in §5.1.

The expectation is that this prereg does not have an analogous direction error. If one is nonetheless surfaced at execution time, it will be reported in the appendix of the Phase 1c paper draft transparently, not silently revised.

---

## 9. Pre-commitment statement

The hypotheses (H1c.1.a/b/c, H1c.2.a/b/c), predicted outcomes, corpus composition, concept tagging methodology, decision rules, and anticipated failure modes are committed to the public repository on this date, prior to fetching the Phase 1c source texts and prior to running any Phase 1c analysis. The author commits to reporting outcomes transparently against these predictions, including refutations or unexpected results, in `findings/phase1c-multilingual.md` and in a §6.10 section of the next paper draft (Draft 7).

If predictions are refuted in informative ways, the writeup documents this transparently rather than silently revising predictions, mirroring the treatment of the §6.8 ULTIMATE refutation in Draft 5/6 and the H1b.3 inequality-direction issue in Draft 6 Appendix C.

---

*This document is the load-bearing pre-registration for Phase 1c. External timestamping is provided by (i) the public GitHub commit on this document, (ii) the Zenodo release `v1.3-prereg-phase1c` to be cut at the same commit. The GitHub commit timestamp on this document precedes any execution of Phase 1c main analyses.*
