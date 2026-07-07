# Concept-Conditional Cross-Tradition Binding in Semantic Embedding Space: A Method, Its Model-Robustness Limits, and a Pre-Registered Test of Mysticism Convergence

**T. David Kinlaw**
*Independent Researcher · Redbird Software LLC · david@redbirdsoftwarellc.com*
*ORCID: [0009-0008-5213-1017](https://orcid.org/0009-0008-5213-1017)*

**Working preprint — Draft 8.1 (public release)**
**Date:** 2026-07-05 (rev. 2026-07-07: restores the AI-use disclosure inadvertently dropped from Draft 8)
**Status:** Public working draft accompanying the formal Phase 3a pre-registration
(`findings/phase3a-preregistration.md`, registered by the public commit and Zenodo DOI of
this release). Phases 0–2 are exploratory and complete; Phase 3a is confirmatory,
registered, and **not yet run**. Findings are reported as proof-of-concept and an
invitation to extend, replicate, or refute. This draft incorporates revisions from an
independent blind review of the release candidate; the experiment-level demands that review
raised (lexical-overlap baselines, RSA noise ceilings) are recorded in §10 as open
controls rather than silently deferred.

**Changes from Draft 7 (private).** Draft 7 added Phase 2 (multilingual originals) and
framed its headline as a per-concept dissociation: AWARENESS convergence
vocabulary-mediated, SUBSTRATE convergence translation-free. Draft 8 makes three major
updates. **(1) A robustness correction (§6.9):** cross-model due-diligence (LaBSE vs OpenAI
`text-embedding-3-large`) shows the per-concept cross-lingual dissociation is
model-specific. Per-concept CCB conclusions fail to agree across embedding models in the
multilingual regime, and on identical within-language data they reverse almost perfectly.
The English Phase 0/1 results are unaffected (model-robust on both methods). **(2) The
model-robust replacement (§6.10):** representational-similarity analysis (RSA) of
within-language concept geometry, which never aligns embeddings across languages, agrees
across models (r ≈ 0.78) and shows a moderate holistic isomorphism of contemplative
concept-geometry across original-language traditions. An equal-N control shows per-concept
attribution is sample-size-confounded, so the isomorphism cannot currently be assigned to
any single concept, including SUBSTRATE. **(3) The Phase 3a confirmatory design (§8),
rebuilt on RSA and now public:** publishing it in this release *is* the pre-registration.
Draft 8 also adds Phase 2b (§6.4b), the same-works-across-languages gradient in which
AWARENESS and SUBSTRATE move in opposite directions under translation on a single fixed
text pair. It is the cleanest single-model demonstration of the vocabulary-vs-structure
mechanism, and it is explicitly scoped as a LaBSE-observed result.

---

## Abstract

We introduce **concept-conditional cross-tradition binding (CCB)**, an embedding-based
statistic that tests whether passages from different source traditions are more similar
when both mention a shared structural concept than when only one does, over cross-tradition
pairs with a permutation null. CCB is bias-aware (it avoids the shared-placeholder artifact
of vocabulary substitution), tractable at >10⁴ sentences, and, within English, cross-model
replicable.

We stress-test it on the 65-year mysticism convergence debate (Stace, 1960; Katz, 1978;
Forman, 1990; Hood, 1975). Across an English paraphrase corpus (Phase 0) and a verified
whole-book English corpus (Phase 1a), five of seven pre-specified concepts (AWARENESS,
RECOGNITION, WORLD, ULTIMATE, SUBSTRATE) bind cross-tradition at *p* ≤ 0.0015, replicating
across two embedding models and two granularities and surviving a battery of
lexical-overlap controls (binding retains 64–90% of its magnitude with the tag terms
themselves deleted, §6.1b). **Phase 1b** (multi-translator,
pre-registered) bounds the between-translator share of similarity variance at ~20%:
translators differ, but the cross-tradition signal is not primarily a translator artifact.
**Phase 2** removes English translation entirely, using original-language corpora across
nine languages, and initially yielded a striking per-concept dissociation on LaBSE:
AWARENESS convergence vocabulary-mediated, SUBSTRATE convergence translation-free, with a
same-works control (Dhammapada × Tao Te Ching) in which translation *manufactures*
AWARENESS convergence and *destroys* SUBSTRATE convergence.

We then report what a second embedding model does to this picture, as a methodological
result in its own right: **in the multilingual regime, per-concept CCB conclusions do not
survive a change of embedding model.** Across models the per-concept scores disagree
(cross-language r = −0.43 over 7 concepts, not itself significant at that n) and on
identical within-language data they reverse almost perfectly (r = −0.96), while both
methods are model-robust on the English corpus (CCB r = +0.88, RSA r = +0.97). The
per-concept dissociation is therefore a model-specific finding. The remaining multilingual
candidate is holistic: RSA over within-language concept geometry, which never aligns
across languages, agrees across models (r = +0.78), rejects a concept-label permutation
null (mean cross-language RDM correlation ≈ +0.39–0.44, *p* ≈ .03–.05), and is reliably
measured (split-half ceiling 0.93–0.95). Two controls added in this draft then discipline
that claim sharply: the isomorphism shrinks to non-significance under an equal-N control,
and it does **not** exceed an arbitrary word-set baseline matched for per-language
prevalence (12th–14th percentile of the baseline distribution, §6.10b). The current
multilingual evidence therefore does not establish contemplative-specific structural
convergence in either per-concept or holistic form. A 40-language Bible×Quran baseline
supplies reliability references and a diagnostic negative result: ULTIMATE is only middling
between two traditions worshipping the *same God*, so CCB measures contextual co-location,
not shared reference.

We make no claim about whether perennialism is correct. We claim (i) a method and its
honestly-mapped validity domain: per-concept CCB within a language, holistic RSA across
languages, with the controls that domain requires; (ii) a substantive negative finding:
once model-robustness and prevalence-matched baselines are demanded, no multilingual
cross-tradition convergence claim survives at current corpus power, and the concept-label
permutation null standardly used for such claims is demonstrably too weak; and (iii) a
**formally pre-registered confirmatory test** (Phase 3a) of genealogical relatedness,
using genealogically independent Axial-Age traditions (pre-Buddhist China × pre-contact
Greece), an age/contact gradient, tiered experiential/functional control concepts, RSA as
the registered instrument, and the matched word-set baseline of §6.10b as the registered
null. The registration is frozen in this release; the test has not been run. Code,
corpora, and baselines are MIT.

---

## 1. Introduction

### 1.1 What the paper proposes
CCB operationalizes a sharper convergence claim than "everything converges": *specific
structural axes bind specific traditions when those traditions discuss those axes.* For
each pre-specified concept *C* and each cross-tradition passage pair, we compare the mean
similarity of pairs where both mention *C* to pairs where only one does; the difference is
the binding of *C*, with a permutation-null *p*-value (§4.3). The construction avoids the
failure modes of document-level similarity (register/vocabulary domination) and vocabulary
substitution (shared-placeholder bias).

### 1.2 The mysticism convergence debate as test case
Perennialists (Stace, Forman) claim contemplatives from unconnected traditions report a
shared structural description of reality; constructivists (Katz) claim apparent convergence
is conceptual mediation and scholarly projection. The debate is textual, the sides make
divergent predictions about observable text, and it has resisted qualitative resolution for
65 years. That makes it an apt CCB test case: hard, contested, and equipped with a
literature that predicts both outcomes.

### 1.3 The confound ladder
English-only data cannot separate structural convergence in source content from convergence
imposed by translators. The program climbs a ladder of confounds, each phase removing one:
paraphrase (Phase 1a), between-translator variance (Phase 1b), translation itself
(Phase 2), **the embedding model** (§6.9, a rung we did not originally draw and added after
it broke), and finally genealogical relatedness (Phase 3a, pre-registered here).

### 1.4 What the paper does *not* claim
Nothing here bears on whether convergence reflects (a) shared reality, (b) shared
cognition, (c) shared writing conventions, or (d) shared translator conventions. The method
answers the prior question: *is there cross-tradition signal beyond what shared vocabulary,
register, translators, embedding-model geometry, and (in Phase 3a) shared lineage can
explain?* We do not claim perennialism settled or constructivism refuted.

### 1.5 Contributions
1. **CCB** with vectorized permutation testing (§4.3, Algorithm 1) and its validity domain
   mapped: model-robust within-language, model-fragile across languages (§6.9).
2. **Two translator-confound defenses**: Phase 1b variance decomposition (§6.2b); Phase 2
   multilingual originals (§6.3–6.5).
3. **The same-works translation gradient** (§6.4b): on one fixed tradition pair, AWARENESS
   and SUBSTRATE move in opposite directions under translation. A single-model (LaBSE)
   design demonstration, pending second-model replication.
4. **The model-robustness result** (§6.9): per-concept multilingual conclusions do not
   survive a change of embedding model. This is a cautionary result for any multilingual
   embedding-based comparative claim, well beyond this project.
5. **Holistic RSA as the model-robust multilingual instrument, and its limits** (§6.10):
   equal-N and SNR analyses show per-concept attribution is sample-size-confounded, a
   split-half noise ceiling shows the instrument is reliable, and an arbitrary-word-set
   baseline (§6.10b) shows the current isomorphism is not concept-specific — motivating
   the stronger null the Phase 3a registration adopts.
6. **Reliability/normalization apparatus** (§4.4–4.6): gate-first protocol; a profile-fit
   reliability metric with built-in ground truth; per-language Δ-baseline; the LaBSE-vs-e5
   anisotropy finding.
7. **A formally pre-registered confirmatory design** (§8) isolating genealogical
   relatedness, registered by this release.
8. **Open-source release** of code, corpora, and baselines.

---

## 2. Related work
Hutchinson et al. (2024) survey NLP on religious text, which is dominated by
translation/parallel-corpus use, with little cross-tradition embedding-based structural
comparison. The components have precedent: sentence embeddings (Reimers & Gurevych, 2019),
permutation testing, and representational similarity analysis (Kriegeskorte, Mur &
Bandettini, 2008); the assembly is the contribution. The §6.9 model-fragility finding
connects to the embedding-stability literature (Antoniak & Mimno, 2018) and extends it to
the multilingual per-concept regime. Debate landmarks: Stace (1960); Katz (1978); Forman
(1990); Hood (1975, the M-Scale); Trivedi (2025); SEP Mysticism (2025). Multilingual
embeddings: LaBSE (Feng et al., 2022); multilingual-e5 (Wang et al., 2024), tested and
rejected for CCB (§4.1); OpenAI `text-embedding-3-large` as the second model (§6.9).
Bridge thinkers (Bohm, Rovelli, Kastrup, Tononi/Koch, Hoffman, Tegmark, Bostrom, Lloyd,
Wheeler) appear only in the Phase 0 corpus and are deferred pending verified-text sourcing.

---

## 3. Corpora and concepts

### 3.1 The seven pre-specified concepts
All analyses use seven structural concepts fixed before Phase 0 and carried unchanged
through every phase. Tagging is by per-concept pattern dictionaries (§4.2); representative
terms below are examples, not the full dictionaries (which ship in the repository).

| concept | neutral definition | example tag terms |
|---|---|---|
| ULTIMATE | the tradition's absolute / ground-of-being | God, Brahman, Dao, the One, Ein Sof, Allah |
| SUBSTRATE | what underlies manifest phenomena, esp. via emptiness/non-being | emptiness, śūnyatā, 空/無, faná, ayin, nada, implicate order |
| AWARENESS | consciousness / the knowing capacity as topic | consciousness, awareness, rigpa, chit, nous, 識/心 |
| WORLD | the status of the manifest/phenomenal world | world, phenomena, saṃsāra, the ten thousand things, māyā |
| SELF | the self and its nature or negation | self, soul, ego, ātman, anattā |
| RECOGNITION | liberation/awakening as recognizing what already is | awakening, enlightenment, mokṣa, nirvāṇa, realization |
| NONSEP | non-separability of observer and observed | nonduality, not-two, union, oneness, tat tvam asi |

Five of the seven (AWARENESS, RECOGNITION, WORLD, ULTIMATE, SUBSTRATE) bind significantly
in the English phases (§6.1); SELF and NONSEP do not, and NONSEP additionally has low
prevalence in most corpora. The Bible×Quran reference corpus tracks only five concepts
because RECOGNITION and NONSEP rarely fire in scripture (§4.5).

### 3.2 Phase 0 (English, paraphrase-heavy)
143 passages, 23 traditions, 68% investigator paraphrase; built for fast iteration and
superseded for evidential purposes by Phase 1a.

### 3.3 Phase 1a (English, verified whole-book)
20 public-domain books, ~2.85M tokens, 14,173 sentences, 920 balanced passages, 11
traditions, a single named translator per source, license and provenance recorded in
`corpus/books_manifest.json`.

### 3.4 Phase 1b (multi-translator, two source families)
Bhagavad Gītā and Tao Te Ching, three published translators each, for a within-source
between-translator variance test. Pre-registered before analysis (public commit `d16fc8c`;
Zenodo `v1.2-prereg-phase1b`). (§6.2b.)

### 3.5 Phase 2 multilingual corpora
- **Phase 2a — within-language cross-tradition**, nine languages: Chinese
  (Buddhist×Daoist), Arabic (Sufi×Falsafa), Hindi (Kabīr×Tulsīdās), Hebrew
  (Hasidic×rationalist), Spanish (Quietist×Carmelite), French (translated 3-tradition),
  Japanese (Buddhist×Confucian), Greek (Neoplatonist×Christian), English (Dhammapada×TTC).
  Sanskrit/Pali were screened and **excluded** (failed the gate, §4.5).
- **Phase 2b — same works across languages**: the Dhammapada × Tao Te Ching pair held
  fixed across classical Chinese (original), three English translators, and French; a
  second pair (Gītā × Dhammapada, EN/FR); a third, maximally-scalable pair (Dhammapada ×
  Gospel of John) with verse-ID tag projection (EN/DE/VI proven).
- **Phase 2c — originals only**: classical Chinese, Arabic, Greek, Hindi, Spanish, Hebrew;
  translation-free by construction.
- **Phase 2d — harmonized**: re-tagged with one frozen cross-language dictionary plus
  corpus bulking.

### 3.6 Scripture reference corpus
A fixed parallel corpus (John, Genesis, Ecclesiastes, Qur'an) across up to 40 languages,
used as a per-language **reliability/resolution reference**, never as a convergence target
(§4.5–4.6, §6.7). English-projected verse tags hold concept assignment identical across
languages so only the embedding varies. Extended with ancient-register Greek (Koine NT +
Septuagint) and classical-Chinese (Wenli) editions for Phase 3a (§6.8).

### 3.7 Corpus selection is a method parameter
Corpus composition is an input that bounds claim strength; every claim in this paper is
conditional on the corpora named above (§6.2, §8).

---

## 4. Method

### 4.1 Embedding
Phase 0/1 use OpenAI `text-embedding-3-large` and ONNX `all-MiniLM-L6-v2`. Phase 2's
primary multilingual model is **LaBSE**. multilingual-e5 was **rejected for CCB**: it
anisotropically collapses non-English text into a ~0.84 cosine cone (std ~0.02), far below
the concept signal, while LaBSE keeps spread (~0.45–0.65). OpenAI `text-embedding-3-large`
passes the same anisotropy screen on all six Phase 2c languages and serves as the second
model for every §6.9–6.10 robustness analysis. We report anisotropy with every multilingual
gate.

### 4.2 Concept tagging
Per-concept pattern dictionaries (case-insensitive regex for Latin scripts; normalized
substring matching for Han, Arabic, Hebrew, Devanagari, and Greek): per-language
dictionaries for Phase 2a, and a single frozen harmonized cross-language dictionary
(`harmonized_concepts.py`) for Phase 2d and all §6.9–6.10 analyses, including the Greek
SUBSTRATE fix (dropping ὕλη "matter", a known concept mis-mapping, §6.10). Tagging is a
pre-specifiable hidden degree of freedom (§10).

### 4.3 The CCB statistic

$$\text{CCB}(C) = \overline{\text{sim}}(\text{both mention } C) - \overline{\text{sim}}(\text{exactly one mentions } C)$$

computed over cross-tradition passage pairs only. The contrast against "exactly one
mentions C" (rather than "neither") controls for concept-mentioning passages being
systematically more similar for reasons unrelated to *C*, such as length or elaboration.
Significance is a permutation test at the passage-tag level: tag assignments are shuffled
across passages (preserving the tagged count), the statistic is recomputed, and 2,000
permutations (5,000 for document-level tests) build the null; *p* is the fraction of
permutations at or above the observed value, one-sided. Permuting tags rather than pairs
respects the non-independence of pairs sharing a passage.

**Algorithm 1: Concept-Conditional Cross-Tradition Binding**

```
Input:  passages P = [p_1, ..., p_n]; each p_i has tradition(p_i), text(p_i)
        embedding model E producing unit-normalized vectors
        concept C with pattern dictionary D_C
        permutation count K
Output: binding score CCB(C), p-value

1.  Compute embeddings v_i = E(text(p_i)) for all i
2.  Compute similarity matrix S where S[i,j] = v_i · v_j
3.  For each i, tag t_i = 1 if any pattern in D_C matches text(p_i), else 0
4.  Compute boolean mask M_cross where M_cross[i,j] = 1 iff
        i < j and tradition(p_i) != tradition(p_j)
5.  Compute both-have mask M_both = M_cross AND (t outer-and t)
6.  Compute one-has mask  M_one  = M_cross AND (t outer-xor t)
7.  binding_obs = mean(S[M_both]) - mean(S[M_one])
8.  For k in 1..K:
        shuffle t to t' (preserving sum(t)); recompute masks;
        binding_perm_k = mean(S[M'_both]) - mean(S[M'_one])
9.  p = (count(binding_perm >= binding_obs) + 1) / (K + 1)
```

The vectorized implementation (`scripts/sentence_binding_vectorized.py`) keeps each
permutation to a handful of numpy boolean and float operations, making the test tractable
at n = 14,173 sentences. For sentence-level analysis, passages are split on punctuation and
the same tagger is applied per sentence.

### 4.4 Within-language vs. cross-lingual CCB
**Within-language** CCB (a single language, so the model performs no cross-lingual
alignment) is the cleaner test. **Cross-lingual** CCB (pool languages, restrict to
cross-language pairs so the language baseline cancels) is weaker: a bitext-trained model's
cross-language same-topic clustering partly reflects the model. §6.9 sharpens this from
"weaker" to "model-dominated": per-concept cross-lingual CCB does not survive a change of
embedding model.

### 4.5 Gate-first protocol + profile-fit reliability metric
**Within-language gate:** before any CCB in a language is trusted, the model must resolve
concept structure within that language, operationalized as significant within-tradition
binding for at least 6 of the 7 concepts on a within-language run. All nine Phase 2
languages passed (6–7/7); Sanskrit and Pali failed (2/7) and were excluded. **Profile-fit
metric:** on the fixed Bible×Quran corpus, each language's concept-CCB profile (scale
removed) is correlated with the 40-language consensus, giving a reliability check with a
known-correct answer. The consensus tracks the five scripture-active concepts
(AWARENESS > ULTIMATE > SUBSTRATE > WORLD > SELF; RECOGNITION and NONSEP rarely fire in
scripture). 35/40 languages fit *r* ≥ 0.83; outliers are low-resource (Burmese, Japanese,
Indic), where the profile itself degrades rather than merely shrinking. The metric
independently flagged Japanese, whose WORLD result had also failed in Phase 2a. Limits: it
conflates embedding and translation quality; it is coarse (five concepts); it is
scripture-register and high-resource-anchored.

### 4.6 Per-language Δ-baseline
Per-language resolution varies ~4× (§6.7), so absolute CCBs are not comparable across
languages. The Bible×Quran CCB for a concept in a language(-pair) serves as the normalizer:
Δ_C = CCB_C(test) − CCB_C(baseline).

### 4.7 Document-level, substitution, and clustering analyses
Retained as secondary/descriptive. The vocabulary-substitution analysis in particular has a
known shared-placeholder bias (documented in `methodology-notes.md`); CCB on unsubstituted
text supersedes it.

### 4.8 Representational-similarity analysis (RSA) of concept geometry
For each language (or tradition-system), compute per-concept centroids from tagged chunks
*in that language's own embedding space*, form the concept×concept cosine
representational-dissimilarity matrix (RDM), and correlate RDM upper triangles across
languages or systems (second-order isomorphism; Kriegeskorte et al., 2008). The embeddings
are never aligned across languages; each geometry is measured internally and only the
relational structure is compared. The null permutes concept labels within a system. One
important scope note: the *harmonized tagging dictionary* is itself an investigator-made
cross-language correspondence, so RSA removes the model's alignment step but not the
dictionary's (§6.10, §10). This is the instrument that survives the §6.9 model-robustness
test and is the registered Phase 3a primary (§8).

---

## 5. The translator confound and the two-defense response
A small anglophone-translator cohort produced most of the English translation tradition;
convergent conventions would make a portion of any English-only cross-tradition similarity
a property of translation, not source. Draft 5 named this the load-bearing limitation and
prescribed two defenses; this draft reports both.

- **Phase 1b (between-translator variance).** On two source families with three translators
  each, cosine-similarity variance across pair types partitions into translator (~20%),
  source-content (~39%), and tradition (~41%) components, estimated from the ordered
  within-source/cross-source pair-type means. Translators are statistically distinguishable
  (a permutation test on translator labels gives z ≈ −17.9, i.e., same-translator pairs are
  far more self-similar than the shuffled null) but the cross-tradition signal is **not
  primarily a translator artifact** (§6.2b).
- **Phase 2 (remove translation).** Original-language analysis attacks the broader
  objection that the scholar-tradition as a whole imposes conformity invisible to
  between-translator tests, by having no English translator at all. What survives
  translation-removal, once the second embedding model is consulted, is the holistic
  geometry result (§6.10); the per-concept dissociation does not (§6.9).

The confound that remains after translation is removed, shared *lineage/contact* among the
surviving traditions, is the registered target of §8.

---

## 6. Results

Effect sizes are raw cosine differences; we avoid "σ-above-null" language because the
permutation null is non-parametric. Exploratory phases report uncorrected *p*-values; see
§6.11 for the multiple-comparisons policy.

### 6.1 Phase 0 / 1a (English) — recap
Five of seven concepts (AWARENESS, RECOGNITION, WORLD, ULTIMATE, SUBSTRATE) bind at
*p* ≤ 0.0015 in both corpora, replicating across two embedding models and two
granularities; SELF and NONSEP do not bind. Canonical pair results: Mahāyāna×Theravāda
AWARENESS 0.518; Advaita×Theravāda RECOGNITION 0.531 under the technical-only tagger. These
English results are model-robust (§6.9: cross-model per-concept agreement r = +0.88 CCB,
+0.97 RSA) and nothing in this draft walks them back; the lexical-overlap controls a blind
review of this draft demanded were then run and substantially defend them (§6.1b).

### 6.1b Lexical-overlap controls (new)
Both-tagged passages share dictionary terms by construction, and embedding similarity is
partly lexical, so positive CCB could in principle reduce to shared surface strings. Three
controls were run on the Phase 1a passages (full write-up
`findings/phase1a-lexical-controls.md`; script `scripts/phase1a_lexical_controls.py`).
**Tag-term masking (decisive):** deleting every dictionary-matched substring from tagged
passages and re-embedding leaves all five binding concepts significant at 64–90% of their
original magnitude — the binding is carried by surrounding context, not the tag strings.
**Bag-of-words baseline:** a tf-idf model produces binding too, but with a *different*
concept profile (r = −0.23 vs the embedding profile); RECOGNITION binds semantically but
not lexically, and SELF binds lexically but not semantically (the embedding statistic
correctly refuses a binding the lexical statistic would grant). **Frequency-matched
random-word floor:** arbitrary same-prevalence word sets yield a generic positive CCB
floor (+0.004 to +0.021), above which the real concepts sit at the 84th–100th percentile
(WORLD and ULTIMATE decisive; AWARENESS, SUBSTRATE, RECOGNITION above the median but short
of the 95th percentile at 50 draws). Consequence: raw CCB magnitudes include a generic
lexical component and should be reported against the matched-random floor for the
concept's prevalence; the binding itself is not a surface-string artifact.

### 6.2 Vocabulary-breadth mechanism — recap
Passage-level effect sizes deflated 3–4× between Phase 0 and 1a for broad-vocabulary
concepts but **not** for technical-only SUBSTRATE (+0.053→+0.054); sentence-level deflation
was only ~25%, confirming a casual-usage noise floor. A pre-specified technical-only-tagger
test confirmed a two-component mechanism (noise floor + coverage asymmetry): RECOGNITION
rose to +0.110; SUBSTRATE was unchanged (the control); ULTIMATE decreased because its
technical vocabulary concentrates in nondual traditions, shifting pair coverage.

### 6.2b Phase 1b — between-translator variance decomposition
Pre-registered (commit `d16fc8c`, Zenodo `v1.2-prereg-phase1b`). The predicted variance
ordering across pair types was confirmed (H1b.1); the translator share was 19.5%, below the
pre-registered 35% threshold (H1b.2); the translator effect is strongly detectable (H1b.3;
the pre-registration stated that hypothesis's inequality in the inverted direction, an
operationalization error documented in the Phase 1b findings file and repeated here for
transparency). Conclusion: **Phase 1a's cross-tradition signal is not primarily a
between-translator artifact.**

### 6.3 Phase 2a — the LaBSE per-concept picture
Within-language cross-tradition CCB, nine languages (LaBSE):

| configuration | language type | AWARENESS | SUBSTRATE | ULTIMATE | WORLD |
|---|---|---|---|---|---|
| Chinese (Buddhist×Daoist) | orig, separate lineage | **flat** | binds | binds | binds |
| Hebrew (Hasidic×Rationalist) | orig, divergent register | **flat** | binds | binds | no |
| Greek (Neoplatonist×Christian) | orig, low-contrast | **flat** | (ὕλη artifact) | binds | binds |
| Arabic (Sufi×Falsafa) | orig, shared lineage | binds | binds | binds | binds |
| Hindi (Kabīr×Tulsīdās) | orig, shared lexicon | binds | binds | binds | binds |
| Spanish (Quietist×Carmelite) | orig, max overlap | binds (+.037) | binds | binds | binds |
| French (3-tradition) | translated | binds | flat | binds | binds |
| English (Dhammapada×TTC) | translated | binds | weak | mixed | binds |
| Japanese (Buddhist×Confucian) | rendered | binds | binds | binds | no |

On LaBSE the pattern reads cleanly: AWARENESS binds exactly where awareness-lexicons
overlap (lineage, school, or translation) and goes flat where they diverge; ULTIMATE binds
within-language everywhere but is name-bound across languages; SUBSTRATE binds in the
original emptiness-traditions. **§6.9 scopes this reading.** It is internally consistent
and language-controlled, but per-concept multilingual CCB does not survive a change of
embedding model, so the dissociation is reported as a LaBSE-geometry finding, not a
model-independent fact.

### 6.4 Phase 2c — originals only (LaBSE)
**Cross-language** (translation-free): SUBSTRATE +0.0066 (*p*=.004), WORLD +0.0063 (.004),
SELF +0.0042 (.02), **AWARENESS +0.0005 (.38, flat)**, ULTIMATE −0.004, RECOGNITION
−0.0035. **Within-language**: SUBSTRATE +0.0334, ULTIMATE +0.0277, AWARENESS +0.0228, SELF
+0.0230 (all *p*<.0001). On LaBSE, with translation banned, SUBSTRATE converges across
languages and AWARENESS does not. Same scoping as §6.3. (The cross-language magnitudes are
small in absolute terms; on the Δ-baseline scale of §4.6 they are comparable to the
per-language Bible×Quran resolution floor, which is why the within-language column and the
§6.10 holistic test carry the evidential weight.)

### 6.4b Phase 2b — the same-works translation gradient
The strongest single-model demonstration of the vocabulary mechanism: hold the tradition
pair and the *texts* fixed (Dhammapada × Tao Te Ching) and vary only language/translation
(LaBSE):

| language (translation) | AWARENESS | SUBSTRATE | WORLD |
|---|---|---|---|
| classical Chinese (original) | −0.013 (flat) | **+0.054 (p=.001)** | +0.034 |
| English — Legge | **+0.014 (p=.012)** | +0.028 (p=.05) | +0.011 |
| English — Goddard | **+0.012 (p=.02)** | +0.013 (n.s.) | +0.017 |
| English — Carus | −0.011 (n.s.) | +0.010 (n.s.) | +0.034 |
| French — Julien | **+0.021 (p<.0001)** | **−0.009 (flat)** | +0.012 |

AWARENESS and SUBSTRATE move in **opposite directions** under translation. AWARENESS is
flat in the original Chinese (the Buddhist 識/覺 and Daoist 心/神 lexicons do not converge)
and is *manufactured* by translation, which renders both traditions with a shared
mind/consciousness vocabulary. SUBSTRATE is strong in the original (空/無/無為 genuinely
converge) and is *destroyed* by translation, which renders the two emptiness-vocabularies
divergently. A second pair (Gītā × Dhammapada, EN/FR, translation-only) confirms the
translation-side behavior. A third, maximally-scalable pair (Dhammapada × Gospel of John,
verse-ID tag projection, 108-language Bible backbone) is proven in EN/DE/VI, adds German,
and exposes translator-sensitivity even within English (AWARENESS binds with the Müller
Dhammapada, flat with the Sujato). All of this is single-model (LaBSE); by the paper's own
§6.9 standard it is a design demonstration awaiting second-model replication, which is the
natural follow-on.

### 6.5 Phase 2d — operationalization-freeze (LaBSE)
Harmonized dictionary plus bulked corpora: cross-language SUBSTRATE +0.0059 (*p*=.0025),
AWARENESS +0.0013 (*p*=.21). Within-language CCB proved corpus-composition-sensitive at
small n (a Chinese cell flipped on bulking); the cross-language contrast is the stable one,
on this model.

### 6.6 Cross-lingual pooled CCB
On LaBSE, all seven concepts bind weakly cross-language (NONSEP/SUBSTRATE strongest at
~+.010–.012; ULTIMATE weakest). §6.9 shows the pooled statistic is additionally
composition-dominated (easy shared-lineage pairs carry it). We treat pooled cross-lingual
CCB as unusable for inference; where §6.9 reports pooled values, they are used only
diagnostically, to characterize model behavior.

### 6.7 Bible×Quran baseline — CCB is not a doctrinal-agreement detector
40 languages: AWARENESS/ULTIMATE/SUBSTRATE/WORLD bind at +.045–.049 (40-language means),
SELF ≈ 0. **(a)** ULTIMATE is only middling **despite the literally-shared God**: mean
+.047, below AWARENESS, top concept in only 10/40 languages. God-talk saturates scripture
(≈31,000 both-tagged pairs vs SUBSTRATE's ~280) and ubiquity destroys discrimination. This
is a within-language comparison (the same word "God" on both sides), so it is not a naming
artifact. **CCB measures contextual co-location of deployment, not shared reference.**
**(b)** A 4× per-language resolution gradient (English ~.08 → Arabic/Indic ~.02) justifies
the Δ-baseline and the reliability metric. (The English-scale value ~.08 is the one quoted
in §6.8's register results; per-language scales differ, which is the point of §4.6.)

### 6.8 Reliability and register (Phase 3a infrastructure)
Modern Greek profile-fit *r*=0.86; Chinese reproduces at *r*=0.92 (cross-check). Register
run: SUBSTRATE binds at ~0.08 (English-scale Bible×Quran units) in **every** register
including ancient Koine and classical Chinese (penalty Koine−modern −.001,
classical−modern −.013), so the ancient registers Phase 3a uses are reliable for
concept-structure. Greek systematically under-binds AWARENESS across independent checks.

### 6.9 Instrument due-diligence: the model-robustness result (the correction)
Before freezing the Phase 3a design we asked whether its instrument would survive a change
of embedding model, using OpenAI `text-embedding-3-large` (different training objective,
not bitext-trained, passes the anisotropy screen on all six Phase 2c languages). On
identical Phase 2c data and identical harmonized tags, cross-model agreement of per-concept
conclusions:

| statistic | cross-model agreement (LaBSE vs OpenAI) | n |
|---|---|---|
| CCB per-concept, **cross-language** (the Draft 7 dissociation) | r = −0.43 | 7 concepts |
| CCB per-concept, **within-language** (Phase 2c originals) | **r = −0.96** | 7 concepts |
| RSA holistic isomorphism (§6.10) | **r = +0.78** | 15 language pairs |
| CCB per-concept, English Phase 1 corpus | **r = +0.88** | 7 concepts |
| RSA, English Phase 1 corpus | **r = +0.97** | tradition pairs |

Interpretive cautions first: the per-concept correlations are over only seven points, so
the cross-language r = −0.43 is not itself significant and should be read as "no
agreement", not "significant anti-correlation"; the within-language r = −0.96 is the strong
reversal, and even it warrants a leverage check across concepts (per-concept values ship in
the repository). With that said, three consequences follow.

**(1)** In the multilingual regime, per-concept CCB conclusions do not transfer across
models, and on the cleanest (within-language) data they reverse. On OpenAI, pooled
cross-language CCB binds AWARENESS (+0.0131), ULTIMATE (+0.0112), and RECOGNITION (+0.0211;
the maximally name-bound concept binding strongest is a tell that the model aligns
spiritual *topics* aggressively), with SUBSTRATE middling (+0.0076). LaBSE's
"AWARENESS=vocabulary / SUBSTRATE=structural" dissociation is a property of LaBSE's
geometry. A granularity test on the specific Chinese↔Greek pair adds a **concreteness
axis**: concrete control concepts (eating/drinking/warfare) bind cross-language on both
models while abstract ones (governance, SUBSTRATE) go flat, so cross-language CCB on
abstract concepts fights an alignment penalty concrete concepts don't pay.

**(2)** The English Phase 0/1 findings are unaffected: both methods and both models agree
monolingually. The fragility is specific to the multilingual regime. Why within-language
non-English CCB flips across models remains only partially diagnosed: candidate mechanisms
are per-language geometry differences between the models and a tagging-dictionary × model
interaction (harmonized-dictionary quality varies by language), and we have not yet
separated them. This diagnosis is open work, not a settled explanation.

**(3)** "Which concept converges" was, in retrospect, method-dependent across our own
exploratory phases (English CCB → AWARENESS/RECOGNITION; LaBSE cross-language → SUBSTRATE;
OpenAI pooled → everything; RSA → see §6.10). We report this method-dependence as a finding
with a general moral: **any multilingual embedding-based comparative-culture claim made on
a single model should be presumed model-specific until shown otherwise.**

### 6.10 The model-robust multilingual result: holistic RSA isomorphism
RSA over within-language concept geometry (§4.8) is robust exactly where CCB is fragile:
LaBSE↔OpenAI agreement r = +0.78 on the cross-language-pair pattern, with similar
magnitudes (mean cross-language RDM correlation +0.39 LaBSE / +0.44 OpenAI at full,
unequal cell sizes; permutation *p* ≈ .03–.05 at K=7 concepts over 6 languages). The result
is robust to the Greek SUBSTRATE dictionary fix (dropping the ὕλη "matter" mis-mapping
moves it only to +0.392/+0.435). Reading: **the overall relational arrangement of
contemplative concepts is moderately isomorphic across original-language traditions, on
both models, at marginal significance.**

Three controls and three caveats discipline the interpretation. **Equal-N control:**
subsampling every concept×language cell to a common floor collapses per-concept
differences. The apparent "SUBSTRATE is the relational outlier" (and equally its earlier
"SUBSTRATE is special" CCB counterpart) is a **sample-size artifact**: rarer concepts have
noisier centroids. At the cell sizes the current corpus supports (n ≤ 91 per concept per
language), the equal-N isomorphism does not clear the permutation null (best *p* = .085,
OpenAI, n=91). The full-n headline and the equal-N result are the same finding at two
power levels, and the abstract states both. **SNR/target-n curves:** the isomorphism rises
monotonically with per-concept n on both models and has not plateaued at n=91; a linear
extrapolation of the trend (shipped with the analysis scripts) puts reliable per-run
significance at roughly **n ≈ 150–250 chunks per concept per system**, which directly sets
the Phase 3a corpus-sizing floor (§8), with the explicit caveat that an extrapolated,
unplateaued curve is a floor estimate, not a measurement. **Granularity/facets:**
sentence-level splitting does not help (the binding constraint is the rarest-concept ×
smallest-tradition cell, and shorter units degrade centroids); facet decomposition of
SUBSTRATE is degenerate (facet sub-centroids at cosine 0.89–0.94). Power must come from
more *systems* and bigger per-system corpora.

Two remaining caveats: (i) the harmonized dictionary is itself a cross-language
correspondence built by the investigator, so isomorphism attributable to the texts and to
the dictionary are not yet separated; (ii) the permutation *p* over pooled language pairs
does not model the non-independence of pairs sharing a language. The two controls a blind
review of this draft demanded (noise ceiling, arbitrary-concept-set baseline) were then
run, and §6.10b reports them: one clears the instrument, the other substantially demotes
the finding.

### 6.10b The RSA controls: reliable instrument, non-specific signal (new)
Full write-up: `findings/phase2c-rsa-controls.md`; script
`scripts/phase2c_rsa_controls.py`; seed-fixed, both models, Phase 2c originals.

**Noise ceiling (clean).** Split-half RDM reliability per language (100 resamples,
Spearman-Brown corrected) is high everywhere: 0.88–0.97 on both models. The resulting
ceiling for the cross-language isomorphism is 0.93 (LaBSE) / 0.95 (OpenAI), so the
published +0.39/+0.44 recovers 42–46% of what the instrument could show. The isomorphism
is not a noisy measurement of nothing; the instrument is reliable.

**Arbitrary-word-set baseline (the demotion).** Per language, 50 pseudo-concept sets were
built: seven word sets each, sampled from that language's own vocabulary (excluding all
real dictionary terms), each matched to the corresponding real concept's tagged-chunk
count within ±20%, and sampled *independently per language* so no cross-language
correspondence exists. The cross-language isomorphism of these meaning-free pseudo-concept
geometries averages **+0.49 (LaBSE) / +0.53 (OpenAI)** — and the real concept set falls at
the **12th–14th percentile** of that distribution, below the baseline median on both
models. Arbitrary prevalence-matched word groupings routinely produce as much or more
cross-language RDM isomorphism than the real contemplative concepts do.

**Reading.** The weak claim survives: some cross-language geometric correlation exists,
it is real relative to chance (permutation *p* ≈ .03–.05) and relative to measurement
noise (high ceiling), and it is model-robust. The strong claim dies, for now:
*contemplative concept geometry is not detectably more isomorphic across traditions than
arbitrary word sets of the same prevalence profile.* A specific mechanism is proposed and
not yet isolated: prevalence rank order is similar across languages for content-free
reasons, and centroid noise scales with sample size, so any prevalence-matched concept
set inherits a shared noise-magnitude fingerprint that RSA partly reads. This mechanism
also explains the equal-N collapse. Consequences: the concept-label permutation null is
too weak for this family of claims, and the matched word-set baseline replaces it as the
**registered null for Phase 3a** (§8). The natural follow-ups (a rank-shuffled prevalence
variant to isolate the mechanism; an equal-N version of the baseline) are named in §10.

### 6.11 Multiple comparisons
Phases 0–2 are exploratory and report uncorrected *p*-values across many
concept×language×model cells; individually marginal results there (e.g., SELF at *p*=.02 in
§6.4, the RSA *p*≈.03–.05) should be read as screening evidence, not confirmed findings.
The confirmatory phase carries exactly one primary test (§8, H3a.1); everything else in it
is tiered as gating QC, secondary, or exploratory and carries no α.

---

## 7. Discussion

### 7.1 What we have shown
Draft 7's contribution statement, "CCB dissociates structural from vocabulary-driven
convergence," was itself dissociated by the second model. What survives is more precise
and, we argue, more valuable: **a validity map for embedding-based cross-tradition
comparison.** Per-concept CCB is a real, model-robust instrument *within a language* (the
English results, the same-works gradients), now defended directly against the
lexical-overlap mechanism (§6.1b masking). Across languages, per-concept scores belong to
the model, not the traditions; the holistic RSA isomorphism is model-robust and reliably
measured but is not yet distinguishable from prevalence-matched arbitrary word sets
(§6.10b). The honest multilingual scorecard: instrument validated, convergence claim
open, and the test that could settle it now registered with a properly hardened null (§8).

### 7.2 The mechanism picture that survives
The vocabulary mechanism itself is not retracted; it is re-scoped. The Phase 2b
mirror-gradient (translation manufactures AWARENESS convergence and destroys SUBSTRATE
convergence on fixed texts) and the vocabulary-breadth mechanism (§6.2) are concrete,
replicable-by-design observations of how lexicon and translation shape embedding-space
convergence, currently demonstrated on one model. What we no longer claim is the
model-independent per-concept taxonomy ("structural SUBSTRATE / vocabulary AWARENESS")
built on them.

### 7.3 What we have *not* shown
Not perennialism. Not a model-independent per-concept dissociation (§6.9). Not a
contemplative-specific holistic isomorphism: the current cross-language signal does not
exceed the matched word-set baseline (§6.10b). Not the elimination of **genealogical
relatedness**: every tradition pair in Phases 0–2 shares lineage or contact, and that is
the registered Phase 3a target. Not external metaphysical reality (§7.5).

### 7.4 The updated decomposition
(1) vocabulary/translation — *demonstrated* as a mechanism (Phase 2b gradient), per-concept
attribution model-scoped; (2) register/style; (3) translator-tradition — *bounded* (Phase
1b, ~20%); (4) **embedding-model geometry — newly isolated** (§6.9), handled going forward
by RSA plus mandatory two-model reporting; (5) genealogical relatedness — the largest
remaining unbounded component (§8); (6) structural convergence — the holistic isomorphism
residual, a *lower bound* given finite coverage.

### 7.5 The interpretive ceiling
Even a maximally successful Phase 3a establishes at most that the surviving convergence is
**experientially/cognitively universal rather than culturally transmitted** (the
Stace/Forman-vs-Katz crux). It does not establish access to external reality; shared
experience could be shared *neurology*. The instrument reaches the former; the latter is
beyond any text-only method.

---

## 8. Phase 3a: the pre-registered independence test (registered by this release; not run)

The full frozen protocol is `findings/phase3a-preregistration.md`; its publication in this
release **is** the act of pre-registration, timestamped by the public git commit and the
Zenodo version DOI (Zenodo archives are immutable once published, which is what makes a
self-hosted registration auditable). Summary:

**Question.** Genealogically independent Axial-Age spheres — pre-Buddhist China
(Daoist/Confucian) × pre-contact Greece (Platonist/Aristotelian), original languages — with
an age/contact gradient within each sphere and imported Chinese Buddhism as a
known-diffusion internal reference. Structural universality predicts cross-sphere
convergence *before* contact; diffusion predicts none. (We note the "genealogical
independence" of Axial China and Greece is a historiographic premise with a literature of
its own; the registration treats documented-contact level as a graded factor rather than an
absolute, and the gradient design is the sensitivity analysis for it.)

**Instrument.** Holistic RSA isomorphism of within-language concept geometry (§4.8), the
only instrument that survived §6.9. OpenAI `text-embedding-3-large` primary with pinned
model version and released embeddings (mitigating proprietary-endpoint drift), LaBSE as the
open corroborator, frozen harmonized and control dictionaries, chunk-level. **The
registered null is the §6.10b prevalence-matched arbitrary-word-set baseline computed on
the same systems** — Phase 2c showed it to be far stricter than the concept-label
permutation, which is retained only as a floor; H3a.1 requires clearing both. **Per-concept
claims are pre-declared exploratory** (the equal-N result).

**Registered hypotheses.** H3a.1 (primary): pooled pre-contact cross-sphere isomorphism
exceeds the permutation null at *p* < .05. That null-rejection is the sole pass criterion;
the accompanying magnitude prediction (+0.10 to +0.40, below the contacted-era reference of
~+0.44 measured on the Phase 2c grid, a cross-corpus reference rather than a strict
ceiling) is a falsifiable forecast, not part of the criterion. H3a.2 (secondary, declared
underpowered): flat-vs-rising isomorphism across the contact gradient separates a
structural floor from a diffusion increment. H3a.3 (gating QC): the controls-only RDM
(eating/drinking/sleep/governance/warfare) must itself clear the null cross-sphere; if the
instrument cannot see known human universals converge, the run stops and the result is
declared uninterpretable rather than evidential. H3a.4 (exploratory): does
contemplative-concept geometry pattern with the experiential anchors (shared-experience
convergence) or the functional anchors (convergent evolution)? H3a.5: the imported-Buddhism
diffusion reference.

**Power honesty, frozen.** The corpus is enlarged *after* registration under a frozen
sizing rule (≥150 tagged chunks/concept/system; ≥3 school-systems per sphere; canon-slot
selection, meaning texts are added by school/era slot from the standard canon and never
selected by content inspection), with a pre-registered adequacy gate on within-sphere cells
and a pre-declared descriptive fallback if the gate fails. A prior-exposure disclosure in
the registration lists every adjacent computation ever run.

---

## 9. Methodological lessons (updated)
Carried forward from earlier phases: report CCB in relative terms (Δ, orderings, variance
shares), never absolute cosines; gate-first per language (representation proxies rule out,
not in); match tagging breadth across compared cells; build a fixed-content reliability
reference with a known-correct answer. New and load-bearing: **single-model multilingual
results are presumptively model-specific — always run a second, differently-trained
embedding model before interpreting**; per-concept multilingual CCB is not rescued by
pooling (composition-dominated) or by sentence-splitting (centroid degradation); RSA on
within-language geometry is the alignment-free, model-robust formulation; per-concept
attribution requires per-cell n the corpus must be *sized* for in advance (roughly 150–250
chunks per concept per system); power planning must target the rarest-concept ×
smallest-tradition cell, not the mean.

## 10. Limitations (updated)
1. **Genealogical relatedness** — unaddressed until Phase 3a runs (registered, not run).
2. **Lexical overlap as a driver of CCB — now bounded, not eliminated.** The three direct
   controls were run (§6.1b): masking and the bag-of-words divergence defend the English
   claims, and the random-word control quantifies a generic lexical floor that raw CCB
   values include. Residuals: the controls are passage-level and single-model so far
   (sentence-level and second-model replication pending), and three concepts clear the
   matched-random floor at only the 84th–88th percentile at 50 draws.
3. **Model dependence** — now measured rather than unknown: everything multilingual and
   per-concept is LaBSE-scoped (§6.9); the RSA result is two-model, but a third, open,
   non-bitext model is desirable, and the within-language cross-model flip is not yet
   mechanistically diagnosed.
4. **RSA specificity** — the noise ceiling and arbitrary-word-set baseline were run
   (§6.10b): the instrument is reliable but the isomorphism does not exceed the matched
   baseline, so the holistic convergence claim is currently open, not established.
   Remaining: a language-pair-dependence-aware null; isolating the prevalence-fingerprint
   mechanism (rank-shuffled and equal-N baseline variants); separating
   dictionary-contributed from text-contributed isomorphism; and the corpus power the
   Phase 3a sizing rule specifies.
5. **Concept dictionaries as hidden DoF** — mitigated by harmonization and freezing, not
   eliminated; the harmonized dictionary is itself a cross-language correspondence
   (§4.8); no held-out human validation of tagging yet.
6. **Corpus/adversarial selection** — passage and work selection by a single investigator;
   adversarial selection by a constructivist-leaning scholar remains open.
7. **The Phase 2b gradient is single-model**, and modern computational sources (Bostrom,
   Tegmark, Kastrup, Bohm, Rovelli) remain Phase-0-only pending verified-text sourcing.
8. **Reproducibility of the proprietary embedding endpoint** — mitigated by releasing all
   embeddings and RDMs and by the open corroborator model, not eliminated.

## 11. Code and data availability
MIT at **https://github.com/davidredbird/concept-conditional-cross-tradition-binding**.
This release adds: the Phase 2a per-language findings and gate/CCB scripts, Phase 2b
gradient scripts and findings, the harmonized and control dictionaries
(`harmonized_concepts.py`, `control_concepts.py`), the full Phase 3a instrument
due-diligence suite (`phase3a_*` scripts: power analysis, second-model viability,
granularity, RSA prototype/facet/equal-N/SNR/target-n, RSA-vs-CCB), the review-driven
control suites (`phase1a_lexical_controls.py`, `phase2c_rsa_controls.py`, with findings
`phase1a-lexical-controls.md` and `phase2c-rsa-controls.md` and results under
`results/robustness/`), aggregate results JSONs,
**`findings/phase3a-preregistration.md`** (the registration of record), and the Phase 3a
design and due-diligence trail (`phase3a-design.md`, `phase3a-instrument-tests.md`,
`phase3a-rsa-snr-sizing.md`). Corpus texts ship where licenses permit (public-domain and CC
sources with attribution); restrictive-license source text (FLORES+, modern Bible/Quran
translations, ctext/CBETA-restricted material) is excluded and documented. Phase 1b
pre-registration at commit `d16fc8c` / Zenodo `v1.2-prereg-phase1b`.

---

## Appendices
- **Appendix A** — Pre-specified candidate features and status: see `glossary.md` in the
  repository (the pre-registered feature seed) and §3.1 for the concept set used here.
- **Appendix B** — Per-concept robustness matrix across phases and models: shipped as
  aggregate JSONs under `results/` in the repository.
- **Appendix C** — Phase 1b pre-registration and the H1b.3 operationalization-direction
  note: `findings/phase1b-preregistration.md` and `findings/phase1b-multi-translator.md`.
- **Appendix D** — The Phase 3a pre-registration: `findings/phase3a-preregistration.md`,
  public as of this release.

---

## Acknowledgments

### Use of AI assistance

The author used Claude (Anthropic) extensively throughout this project: for methodology design discussions, prose drafting across multiple paper revisions, and writing code under the author's direction. All research questions, experimental design decisions, methodological commitments, interpretations of results, and claims in this paper are the author's; the AI's role was that of a capable but supervised research assistant.

---

## References

Antoniak, M., & Mimno, D. (2018). Evaluating the stability of embedding-based word
similarities. *Transactions of the Association for Computational Linguistics*, 6, 107–119.

Bohm, D. (1980). *Wholeness and the Implicate Order*. Routledge.

Bostrom, N. (2003). Are you living in a computer simulation? *Philosophical Quarterly*,
53(211), 243–255.

Feng, F., Yang, Y., Cer, D., Arivazhagan, N., & Wang, W. (2022). Language-agnostic BERT
sentence embedding. *Proceedings of ACL 2022*.

Forman, R. K. C. (1990). *The Problem of Pure Consciousness: Mysticism and Philosophy*.
Oxford University Press.

Forman, R. K. C. (1999). *Mysticism, Mind, Consciousness*. SUNY Press.

Hoffman, D. (2019). *The Case Against Reality*. W. W. Norton.

Hood, R. W. (1975). The construction and preliminary validation of a measure of reported
mystical experience. *Journal for the Scientific Study of Religion*, 14(1), 29–41.

Hood, R. W., Ghorbani, N., Watson, P. J., Ghramaleki, A. F., Bing, M. N., Davison, H. K.,
Morris, R. J., & Williamson, W. P. (2001). Dimensions of the Mysticism Scale: Confirming
the three-factor structure in the United States and Iran. *Journal for the Scientific
Study of Religion*, 40(4), 691–705.

Hutchinson, B., et al. (2024). Modeling the sacred: Considerations when using religious
texts in natural language processing. *Findings of NAACL 2024*.

Kastrup, B. (2019). *The Idea of the World*. iff Books.

Katz, S. T. (Ed.). (1978). *Mysticism and Philosophical Analysis*. Oxford University Press.

Kriegeskorte, N., Mur, M., & Bandettini, P. (2008). Representational similarity analysis —
connecting the branches of systems neuroscience. *Frontiers in Systems Neuroscience*, 2, 4.

Lloyd, S. (2006). *Programming the Universe*. Knopf.

Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using siamese
BERT-networks. *Proceedings of EMNLP-IJCNLP 2019*.

Rovelli, C. (2022). *Helgoland: Making Sense of the Quantum Revolution*. Riverhead Books.

Stace, W. T. (1960). *Mysticism and Philosophy*. Macmillan.

Stanford Encyclopedia of Philosophy. (2025). Mysticism (Fall 2025 edition).
https://plato.stanford.edu/archives/fall2025/entries/mysticism/

Streib, H., Klein, C., Keller, B., & Hood, R. W. (2020). The Mysticism Scale as a measure
for subjective spirituality. In *Assessing Spirituality in a Diverse World* (pp. 467–491).
Springer.

Tegmark, M. (2014). *Our Mathematical Universe*. Knopf.

Tononi, G., & Koch, C. (2015). Consciousness: Here, there and everywhere? *Philosophical
Transactions of the Royal Society B*, 370(1668).

Trivedi, H. P. (2025). A comparative model of mysticism: Cognitive neuroscience, phenomenal
experiences, and noetic accounts. *Archive for the Psychology of Religion*, 47(2), 133–156.

Wang, L., Yang, N., Huang, X., Yang, L., Majumder, R., & Wei, F. (2024). Multilingual E5
text embeddings: A technical report. *arXiv:2402.05672*.

Wheeler, J. A. (1990). Information, physics, quantum: The search for links. In W. H. Zurek
(Ed.), *Complexity, Entropy, and the Physics of Information* (pp. 309–336). Addison-Wesley.
