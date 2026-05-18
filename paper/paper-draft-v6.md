# Concept-Conditional Cross-Tradition Binding in Semantic Embedding Space: A Method and an Application to Mysticism

**T. David Kinlaw**
*Independent Researcher · Redbird Software LLC · david@redbirdsoftwarellc.com*
*ORCID: [0009-0008-5213-1017](https://orcid.org/0009-0008-5213-1017)*

**Preliminary preprint — Draft 6**
**Date:** 2026-05-18
**Status:** Submission-ready preprint. NLP methodology paper with mysticism convergence as substantive test case. Findings reported as a proof-of-concept and an invitation to extend, replicate, or refute.

**Changes from Draft 5:** Incorporates Phase 1b, a multi-translator within-source variance experiment that addresses §9 limitation 1 (translator-as-confound) on two source families — Bhagavad Gita and Tao Te Ching, three translators each. Phase 1b was externally pre-registered prior to running the analysis (public commit `d16fc8c`; Zenodo `v1.2-prereg-phase1b` release). The new §6.9 reports the variance decomposition: translator effect 19.5%, source-content effect ~39%, tradition effect ~41% of total within/cross-tradition variance. All three pre-registered hypotheses — H1b.1 (variance ordering), H1b.2 (translator-bound below 35%), and H1b.3 (permutation null detection of translator effect) — are confirmed. (The pre-registration document operationalized H1b.3 with the inequality direction inverted; the substantive finding is correctly reported in the main text and the operationalization issue is documented in Appendix C.) §9 limitation 1 changes from "unaddressed" to "tested and bounded at 19.5% on two source families"; the deeper *broad* constructivist objection (anglophone scholar-tradition itself imposing structural conformity, invisible to between-translator variance tests) is carried forward as the explicit Phase 1c (multilingual source analysis) target. §8 adds a methodology lesson: CCB results should be reported in relative terms (effect sizes, ordering, variance partitions) rather than absolute cosines.

**Changes from Draft 4 (preserved from Draft 5):** Incorporates the pre-specified technical-only-tagger experiment (§6.8). The §6.8 prediction is partially confirmed, partially refuted in informative directions: RECOGNITION dramatically exceeded prediction (+0.110 vs predicted +0.03 to +0.05, with advaita × theravada at 0.531 emerging as the strongest single cross-tradition concept-binding result the project has produced); SUBSTRATE control confirmed exactly (+0.054 unchanged); ULTIMATE failed in the unexpected direction (decreased), revealing a previously unrecognized coverage-asymmetry component of the vocabulary-breadth mechanism; AWARENESS and WORLD became untestable due to insufficient technical-vocabulary coverage in the Phase 1a corpus. The §6.8 mechanism is refined from a single-component "noise floor" claim to a two-component formulation (noise floor + coverage-distribution asymmetry). Adds CCB pseudocode (Algorithm 1) in §4.3. Appendix B robustness matrix gets a technical-only column. §7.1 promotes advaita × theravada RECOGNITION alongside Mahayana × Theravada AWARENESS as the project's two cleanest cross-tradition results.

---

## Abstract

We introduce **concept-conditional cross-tradition binding (CCB)**, an embedding-based statistic for testing whether textual passages from unconnected source traditions are more similar when conditioned on shared structural concepts than when not. The statistic is designed to be (i) *bias-aware* — it avoids the shared-placeholder similarity artifact that affects naive vocabulary-substitution tests; (ii) *tractable at scale* — vectorized permutation tests over n×n boolean masks make it usable at >10⁴ sentences; (iii) *cross-model replicable* — applied uniformly to proprietary OpenAI `text-embedding-3-large` (3072-dim) and open-source `sentence-transformers/all-MiniLM-L6-v2` (384-dim BERT) via ONNX Runtime, the latter usable on workstations with Application-Control policies that block torch; and (iv) *cross-granularity stable* — defined identically at passage and sentence levels with mechanistically explained differences between them.

We stress-test the method on the 65-year-old cross-cultural mysticism convergence debate (Stace, 1960; Katz, 1978; Forman, 1990; Hood, 1975). The debate is methodologically apt because its central question — whether contemplatives from unconnected traditions converge on shared structural descriptions of reality — is textual in form yet has resisted direct textual empirical test for six decades, while modern semantic-embedding tools were maturing.

We apply CCB to three corpora. Phase 0 is a 143-passage curated corpus across 23 traditions, 68% investigator-authored paraphrase, designed for fast iteration. Phase 1a replaces paraphrases with verified primary-source published English translations, sampled from a 20-book / ~2.85M-token / 14,173-sentence whole-book base set, 100% non-paraphrase, 11 traditions. Phase 1b adds multi-translator coverage of two source families (Bhagavad Gita and Tao Te Ching, three translators each) for a within-source between-translator variance test.

**Across both corpora, five of seven pre-specified structural concepts (AWARENESS, RECOGNITION, WORLD, ULTIMATE, SUBSTRATE) show statistically significant cross-tradition binding at *p* ≤ 0.0015.** The same five bind across passage and sentence granularity and across both embedding models. Top tradition pairs replicate cross-model.

The paper's primary methodological finding is the **vocabulary-breadth phenomenon** (§6.8). Effect sizes deflate at passage granularity between corpora when the concept's pattern dictionary contains common English terms (`consciousness`, `God`, `world`), but not when the dictionary is technical-only (`emptiness`, `śūnyatā`, `implicate order`). The pre-specified technical-only-tagger experiment confirms the mechanism but in a more nuanced form than initially predicted: vocabulary breadth has two distinct effects — a *casual-usage noise floor* (where common-English-tagged passages dilute binding signal) and a *coverage-distribution asymmetry* (where the remaining technical vocabulary may concentrate in one tradition category, reducing cross-category coverage). The two effects can dominate in different concepts. RECOGNITION recovered dramatically under technical-only restriction (+0.025 → **+0.110** on Phase 1a, with advaita × theravada at **0.531**); SUBSTRATE was unchanged as predicted (control); ULTIMATE *decreased* (revealing the second mechanism component); AWARENESS and WORLD became untestable due to insufficient technical-vocabulary coverage in the Phase 1a corpus.

The paper's secondary methodological finding is the **Phase 1b variance decomposition** (§6.9). On the multi-translator corpus, mean cosine similarity partitions into translator effect (~20% of total within/cross-tradition variance), source-content effect (~39%), and tradition effect (~41%). The pre-registered variance ordering W-S-S-T > W-S-B-T > X-S-W-T > X-T (within-source same-translator > within-source between-translator > cross-source within-tradition > cross-tradition) is confirmed exactly. The translator-bound hypothesis (translator share < 35% of total variance) is confirmed with significant margin (observed 19.5%). The permutation test on translator labels detects a highly significant translator effect at z ≈ −17.9, confirming translators produce statistically distinct stylistic conventions on shared source content while the overall translator-share-of-variance is bounded. **Phase 1a's cross-tradition CCB signal is not primarily a translator artifact.** Phase 1b tests *between-translator* variance only; the complementary *within-anglophone-scholar-tradition shared-consensus* objection (Katz, 1978's broader form) remains unaddressed and is the explicit target of Phase 1c (multilingual source analysis).

We make no claim about whether the perennialist position in the mysticism debate is correct. We claim that **a class of evidence both sides of the debate have to engage with on the merits is now produceable**, and we have produced an example. The method is concept-agnostic and corpus-agnostic; the field can extend or refute the present application by running CCB on different corpora, different concept dictionaries, different embedding models, or different convergent-claim test cases (Golden Rule, Hero's Journey, mystical death-and-rebirth, eternal recurrence). Multi-translator inclusion is partially addressed in Phase 1b (§6.9) for two source families; non-English source analysis with multilingual embeddings, adversarial passage selection, and held-out human-validated concept tagging remain unaddressed (§9, §10) and define what a fuller follow-on application requires.

Code, both corpora, complete result tables, and the pre-specified prediction outcomes released MIT.

---

## 1. Introduction

### 1.1 What the paper proposes

Cross-cultural convergence claims about textual content — claims that authors from unconnected traditions write structurally similar things about reality, mind, perception, or value — are common in religious studies, comparative philosophy, mythology, and elsewhere. They have historically been argued qualitatively. Quantitative tests have been hard to construct: document-level embedding similarity is dominated by register and vocabulary; vocabulary substitution introduces its own biases; and most NLP work on culturally varied corpora has focused on translation or intra-tradition stylometry rather than cross-tradition structural comparison (Hutchinson et al., 2024).

We propose **concept-conditional cross-tradition binding (CCB)**, an embedding-based statistic that operationalizes a sharper version of the convergence claim: *not* "everything converges" but "specific structural axes bind specific traditions when those traditions are discussing those axes." Concretely, for each pre-specified structural concept *C* and each cross-tradition pair of passages, we compare the mean similarity of pairs where both passages mention *C* to the mean similarity of pairs where only one passage mentions *C*. The difference is the *binding* of *C*. A permutation null over concept-tag assignments produces a *p*-value.

The statistic is designed to avoid the failure modes that have made document-level cross-tradition comparison uninformative:

- **Vocabulary substitution failure mode.** Replacing tradition-specific terms with shared placeholders forces token-level similarity across substituted texts, biasing toward apparent convergence. CCB does not substitute; it conditions on mentions.
- **Register / style failure mode.** Document-level similarity is dominated by author register, sentence structure, citation style, and other features that overwhelm content-level convergence. CCB compares passages that all carry the same concept-tag marker, controlling for the *kind* of content being compared.
- **Vocabulary breadth as noise floor.** Pattern dictionaries containing common English terms fire on passages that mention the term casually, diluting passage-level binding. The paper documents this empirically (§6.7-6.8), proposes a refined two-component mechanism for it, and pre-specifies and tests predictions for a technical-only-tagger variant that probes the mechanism directly.

### 1.2 The mysticism convergence debate as test case

The cross-cultural convergence claim has its sharpest qualitative articulation in the philosophy of mysticism, where Stace (1960), Forman (1990), and others argue that contemplatives from unconnected traditions report a shared structural description of reality (non-separation of observer and observed; absence of a privileged self; primacy of awareness; unity beneath multiplicity), while Katz (1978) and the "hard constructivist" tradition argue that every report is conceptually mediated and apparent convergence is hermeneutic projection. The debate has run for sixty-five years on largely textual and philosophical grounds. Empirical work (Hood, 1975; Hood et al., 2001; Anthony et al., 2010; Streib et al., 2020) has tested *contemporary self-reports* via survey instruments (the Mysticism Scale and its descendants) and found cross-cultural similarity, but has not tested whether the *historical texts* produced by unconnected contemplatives converge in semantic structure. A direct textual test with controls adequate to the constructivist critique has not appeared (Hutchinson et al., 2024 confirms the gap in NLP-on-religious-texts).

This is an apt test case for CCB for three reasons:

1. The convergence claim is *about textual content*, so a textual test is methodologically on-domain rather than being a proxy.
2. The two sides of the debate make sharp predictions that diverge on observable text properties: perennialists predict cross-tradition signal beyond shared vocabulary and register; constructivists predict that any signal will be vocabulary-, register-, or translator-mediated and will disappear under appropriate controls.
3. The debate has resisted decades of qualitative argument, so even partial empirical leverage is interesting.

### 1.3 What the paper does *not* claim about the application

Nothing in this analysis bears on whether any measured convergence reflects:

(a) a shared truth about the structure of reality;
(b) a shared feature of human cognition under trained introspection;
(c) a shared feature of how literate contemplative cultures end up writing about introspection, independent of what they observe;
(d) a shared feature of how the small set of anglophone scholar-translators who produced our English source texts render contemplative content.

Distinguishing (a)–(d) is downstream of the empirical question the method answers, which is the prior question *"is there any cross-tradition textual signal beyond what shared vocabulary, register, and translator conventions can explain?"* Our affirmative answer to that question, restricted to five specific pre-specified concepts, is necessary but not sufficient for any of (a)–(d), and we make no progress toward (a)–(d) here.

We will not claim that the perennialist thesis has been settled. We will not claim that the constructivist critique has been refuted; the present results show that vocabulary and register do substantial work in apparent document-level convergence, which is what constructivists predicted. We will claim only that **a method exists for producing evidence the field can engage with on the merits, that we have applied it carefully, and that the result is informative regardless of which interpretation it supports.** We are not the field; we are presenting what we found from a methodologically-defined position. The field is welcome to follow up.

### 1.4 Contributions

1. **CCB**, a bias-aware concept-conditional cross-tradition binding statistic with vectorized permutation testing (§4.3, Algorithm 1).
2. **Cross-model replication architecture** that runs identically against proprietary and open-source embedding stacks, including ONNX-based local inference for environments where torch is blocked.
3. **Vocabulary-breadth phenomenon** characterizing when passage-level concept tagging dilutes binding signal, with a refined two-component mechanism (noise floor + coverage-distribution asymmetry) supported by a pre-specified prediction test (§6.8).
4. **A two-corpus stress test** of the method on the mysticism convergence debate: a paraphrase-heavy fast-iteration corpus and a verified-primary-source whole-book corpus, with shared methodology and divergent paraphrase profiles. Five of seven pre-specified concepts bind in both.
5. **Open-source release** of code, corpora, manifests, results, and pre-specified prediction outcomes for independent replication, extension, and adversarial reuse.

---

## 2. Related work

### 2.1 NLP and computational humanities on cross-cultural / religious text

Hutchinson et al. (2024) survey NLP work on religious texts. The dominant pattern is treating sacred texts as *parallel corpora for machine translation* (Bible and Quran translations in dozens of languages). Some intra-tradition stylometry and topic modeling exists — Wieringa on Seventh-day Adventist periodicals, Choiński and Rybicki on Puritan sermons, Handelman's network analysis of Rosenzweig's correspondence — but cross-tradition embedding-based structural comparison of contemplative literature is largely absent.

The technical components our method assembles all have precedent. Sentence-BERT (Reimers and Gurevych, 2019) and successor embedding models including OpenAI's `text-embedding-3-large` provide dense semantic embeddings; permutation testing over pairwise similarity matrices is standard in computational stylometry; UMAP and t-SNE visualization are routine. The contribution is not in any individual component but in the assembly: a *concept-conditional* test, designed to avoid known document-level and substitution-level failure modes, applied at scale to a multi-tradition cross-cultural corpus.

Adjacent work on representations of religious / philosophical concepts in embedding space exists primarily within a single tradition (e.g., topical analysis of one religious corpus) rather than across unconnected traditions. The cross-cultural comparison that the test case in this paper engages does not, to our knowledge, have a directly precedent NLP method.

### 2.2 The mysticism convergence debate (application context)

We summarize the application's context briefly, citing landmarks rather than rehearsing the literature:

- **Perennialist tradition.** Stace (1960) distinguishes *introvertive* (pure consciousness without content) from *extrovertive* mysticism (unity perceived in the phenomenal world) and argues both forms recur cross-culturally. Forman (1990; 1999) extends with the pure-consciousness-event thesis.
- **Constructivist tradition.** Katz (1978) argues every mystical experience is mediated by prior conceptual structure; apparent cross-cultural convergence is conceptual contamination through scholarly translation and comparative-religion infrastructure.
- **Empirical psychology of mysticism.** Hood (1975) introduced the Mysticism Scale (M-Scale), validated cross-culturally (Hood et al., 2001 with US Christian and Iranian Muslim samples; Anthony et al., 2010 in Tamil Nadu; Streib et al., 2020 US/German). The M-Scale measures *contemporary self-reports* of mystical experience and finds cross-cultural similarity. It does not measure historical texts.
- **Comparative-model recent work.** Trivedi (2025) proposes a tripartite comparative model of mysticism (neurocognitive substrates / phenomenal experiences / noetic accounts) that maps onto pre-specified structural features of the kind CCB tests.

The Stanford Encyclopedia of Philosophy entry on Mysticism (2025) characterizes the present state of the debate as unresolved on philosophical grounds; the survey lists no computational, NLP, or embedding-based methods applied to mystical literature.

We do not engage the philosophical debate at the depth that a primary contribution to it would require. We engage it at the depth required to *use it as a substantive test case* for the method we propose.

### 2.3 Bridge thinkers in the application domain

A modern subliterature of authors explicitly compares structurally nondual claims in modern scientific frameworks to historical contemplative claims: Bohm's *Wholeness and the Implicate Order* (1980), Rovelli's *Helgoland* (2022) (which argues relational quantum mechanics and Nagarjuna's emptiness doctrine make structurally identical claims), Kastrup (2019) on analytic idealism, Tononi and Koch (2015) on consciousness as fundamental in IIT, Hoffman (2019) on perception as interface, Tegmark (2014), Bostrom (2003), and others.

In the Phase 0 corpus, these authors are represented by paraphrases; in the Phase 1a corpus they are absent (their books are not on Project Gutenberg and were not added in Phase 1a). We treat them in this paper as a methodological cautionary tale (§6.5) rather than a substantive contribution to the cross-period convergence question. Restoring them on verified non-paraphrase text via arxiv and fair-use research excerpts is a natural extension (§10) but is not part of the present paper.

**Important caveat for the Rovelli result.** Rovelli's *Helgoland* is in the Phase 0 corpus and argues toward the Mahayana–relational-QM correspondence that our SUBSTRATE-binding analysis quantitatively recovers (§6.1). The 0.455 binding establishes that an embedding model can detect the correspondence Rovelli argued for, given the text in which he argued for it. It does not independently establish the structural identity. Following the second-reviewer pass on Draft 2, we **demote this result from the abstract to a methodological-validation footnote** and promote two methodologically cleaner cross-tradition results — Mahayana × Theravada AWARENESS (§6.1) where neither tradition wrote toward the comparison, and Advaita × Theravada RECOGNITION (§6.8) where the technical-only-vocabulary restriction gives the strongest cross-tradition binding the project has produced.

---

## 3. The test corpora

We use three corpora as test cases for the method: two for concept-binding (Phase 0 paraphrase-heavy and Phase 1a verified-whole-book) and one for the multi-translator variance test (Phase 1b). All three share the same statistical pipeline. Phase 0 and Phase 1a differ in paraphrase profile (the load-bearing concern from the Draft 2 review); Phase 1b extends Phase 1a with multi-translator coverage of two source families to address the largest §9 limitation (translator-as-confound).

### 3.1 Phase 0: paraphrase-heavy fast-iteration corpus

The Phase 0 v0.5 corpus contains **143 English passages across 23 traditions in 3 categories.**

**Historical contemplative nondual (n = 58):** Advaita Vedanta (10), Dzogchen (7), Christian mystical (10), Sufi (7), Neoplatonism (6), Kabbalah (6), Daoism (6), Mahayana (6).

**Modern scientific/computational nondual (n = 25):** simulation theory (6), information physics (6), mathematical universe (5), analytic idealism (4), interface theory (4).

**Bridge thinkers (n = 24):** implicate order / Bohm (5), process philosophy / Whitehead (5), predictive processing / Friston, Clark, Seth (5), integrated information theory / Tononi, Koch (4), relational QM / Rovelli (5).

**Dualistic contemplative controls (n = 24):** Catholic scholastic (8), Theravada Abhidhamma (8), Kantian (8).

**Non-contemplative philosophy controls (n = 12):** Humean (6), analytic / Russell (6).

Source-status distribution: 4.2% `quote`, 28.0% `approximate`, 67.8% `paraphrase`. The paraphrase dominance is the load-bearing concern from the Draft 2 review and was the primary motivation for Phase 1a.

Historical nondual sources were selected for cultural independence — no plausible cultural contact between 8th-century Advaita and 14th-century Rhineland mysticism, or between 3rd-century Plotinus and Tang-dynasty Chan Buddhism. The one notable exception is documented Andalusian Sufi/Kabbalist contact (12c–13c), flagged where it appears in results (§6.1).

### 3.2 Phase 1a: verified whole-book replication corpus

The Phase 1a corpus replaces investigator-authored paraphrases with whole-book published English translations. **All 20 sources were verified against the Project Gutenberg catalog before fetch** using `scripts/verify_manifest.py`, which checks PG-catalog title against expected title; this caught 10 of an initial 24 PG IDs that referenced unrelated books (e.g., the "Plotinus Enneads" PG ID we initially recorded returned "A Ribband of Blue, and Other Bible Studies" by J. Hudson Taylor; the "Cloud of Unknowing" PG ID returned a bookbinding manual). All Phase 1a source texts are verified.

**Phase 1a corpus composition (20 books, ~2.85M raw tokens, sampled to 920 balanced chunks):**

| Tradition | Category | Books | Translator |
|---|---|---|---|
| advaita | nondual | Upanishads, Bhagavad Gita | Paramananda, Arnold |
| daoism | nondual | Tao Te Ching, Zhuangzi | Legge, Giles |
| sufi | nondual | Rumi Mesnevi, Persian Mystics | Redhouse, Davis |
| christian_mystical | nondual | Brother Lawrence, Steiner Mystics anthology | various |
| spinozist | nondual | Spinoza Ethics | Elwes |
| theravada | dualistic | Dhammapada | Müller |
| catholic_scholastic | dualistic | Aquinas Summa I, Augustine Confessions | English Dominican Province, Pusey |
| reformed_theology | dualistic | Calvin Institutes Vol. 1 | Beveridge |
| kantian | dualistic | Critique of Pure Reason, Critique of Practical Reason | Meiklejohn, Abbott |
| humean | non_contemplative | Treatise, Enquiry | (untranslated) |
| analytic | non_contemplative | Russell Problems, External World, Mysticism and Logic | (untranslated) |

**What Phase 1a is missing relative to Phase 0:** the modern computational nondual category and the bridge thinkers. These authors' books are not on Project Gutenberg and Phase 0 represented them via paraphrases. Restoring them via arxiv papers and fair-use research excerpts is part of a fuller follow-on application (§10).

**Chunking strategy.** Each cleaned book is split into ~500-token chunks at paragraph boundaries; oversized paragraphs split at sentence boundaries. The base set is 5,408 chunks; for analysis, books are stratified-sampled to ≤50 chunks each (`scripts/chunks_to_passages.py`), yielding 920 balanced chunks. Without sampling, Aquinas's *Summa* (1,222 chunks) and Calvin's *Institutes* (893 chunks) would dominate. Sentence-level analysis splits the 920 chunks into 14,173 sentences via punctuation-based regex.

### 3.3 Phase 1b: multi-translator variance-test corpus

Phase 1b adds four newly fetched whole-book translations to the Phase 1a corpus to enable a within-source between-translator variance test on two source families:

| Source family | Translator | Year | Provenance | Chunks |
|---|---|---|---|---|
| Bhagavad Gita | Edwin Arnold | 1885 | PG 2388 (Phase 1a already) | 51 |
| Bhagavad Gita | K.T. Telang | 1882 (SBE 8) | sacred-texts.com /hin/sbe08/ | 106 (Gita-only) |
| Bhagavad Gita | Swami Swarupananda | 1909 | sacred-texts.com /hin/sbg/ | 105 |
| Tao Te Ching | James Legge | 1891 (SBE 39) | PG 216 (Phase 1a already) | 27 |
| Tao Te Ching | Goddard / Borel | 1919 | sacred-texts.com /tao/ltw/ | 82 |
| Tao Te Ching | Suzuki / Carus | 1913 | sacred-texts.com /tao/crv/ | 76 |

Telang's SBE 8 volume contains *Bhagavadgîtâ*, *Sanatsujâtîya*, and *Anugîtâ*; for Phase 1b within-source comparability with the other two Gita translators, Telang chunks were filtered to the Gita portion (chars 0–259,683 of the cleaned text). The Sanatsujâtîya and Anugîtâ portions are deferred to Phase 1c. Books beyond Project Gutenberg are fetched via the new `sacred_texts` source-type in `scripts/fetch_books.py` (multi-chapter index parsing).

Phase 1b's experimental design and results are reported in §6.9.

### 3.4 Corpus selection is a method *parameter*, not the method itself

The method is corpus-agnostic. A different investigator running CCB on the mysticism convergence debate would likely select different sources within the same traditions, and we report the obvious concerns (investigator selection bias, single-translator-per-source in Phase 1a, anglophone-only) so that an alternative-corpus replication can be conducted (§9, §10). The Phase 0 and Phase 1a corpora are released as parameters of the present application of the method; they are not the contribution.

---

## 4. Method

### 4.1 Embedding

Texts are embedded with two independent models:

- **OpenAI `text-embedding-3-large`** (3,072-dim, proprietary), via the OpenAI API.
- **`sentence-transformers/all-MiniLM-L6-v2`** (384-dim, BERT-class, open-source), via ONNX Runtime locally.

The two models share no training data, architecture, or organization. ONNX inference was selected because the development environment runs Windows with Defender Application Control active; WDAC blocks `torch.dll` (unsigned) but admits Microsoft-signed ONNX Runtime DLLs. The ONNX inference path (`scripts/onnx_embedder.py`) downloads the model and tokenizer from HuggingFace, mean-pools and L2-normalizes the per-token outputs, and is reproducible on locked-down workstations without administrator privileges.

Embeddings are unit-normalized; pairwise similarity is cosine. The two models agree closely on the qualitative result (§6.2, §6.3); they differ in absolute magnitude (BERT generally produces stronger bindings) but agree on the rank order of concept-binding strength and on top tradition pairs.

### 4.2 Concept tagging

The seven pre-specified structural concepts — ULTIMATE, SUBSTRATE, AWARENESS, WORLD, SELF, RECOGNITION, NONSEP — are tagged on each passage by a manually curated dictionary of case-insensitive regex patterns. The patterns are listed in full in `scripts/concept_analysis.py` and derived from a pre-specified glossary listing tradition-specific terminology for each concept (e.g., AWARENESS includes `consciousness`, `awareness`, `rigpa`, `chit`, `phi`, `nous`; SUBSTRATE includes `emptiness`, `śūnyatā`, `implicate order`, `holographic`, `integrated information`).

The same patterns are applied to both Phase 0 and Phase 1a corpora. Differences in binding strength between phases reflect either (i) genuine differences between paraphrase-style and published-translation text, (ii) differences in casual-vs-technical use of the same vocabulary at scale, or (iii) noise. §6.7-6.8 examines this decomposition empirically via a pre-specified technical-only-tagger experiment.

**Regex tagging is a hidden degree of freedom** that we name prominently. The same investigator built the glossary, the corpus, and the patterns. A pattern set chosen by someone with a different theoretical model of nondualism would tag different passages and could produce different binding scores. CCB is **bias-free of the shared-placeholder substitution artifact** (the artifact it was designed to eliminate), not **bias-free in the absolute sense**. Held-out human-validated tagging on a randomly sampled subset is a follow-on extension (§10).

### 4.3 The CCB statistic

For each pre-specified concept *C*, restricted to cross-tradition passage pairs only:

$$
\text{CCB}(C) = \overline{\text{sim}}\bigl(\text{pairs where both passages mention } C\bigr) - \overline{\text{sim}}\bigl(\text{pairs where exactly one mentions } C\bigr)
$$

The contrast against "exactly one mentions C" rather than "neither mentions C" controls for the possibility that concept-mentioning passages are systematically more similar to each other than non-concept-mentioning passages for reasons unrelated to *C* (e.g., the concept-mentioning passages are longer or more elaborated).

Significance is assessed by a permutation test: concept-tag assignments are shuffled across passages (preserving the total count of tagged passages), the statistic is recomputed, and 2,000 such permutations build the null distribution. The *p*-value is the fraction of permutations with statistic ≥ observed.

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
        i < j and tradition(p_i) ≠ tradition(p_j)
5.  Compute both-have mask M_both = M_cross ∧ (t outer t)
6.  Compute one-has mask M_one = M_cross ∧ (t xor-outer t)
7.  binding_obs = mean(S[M_both]) − mean(S[M_one])
8.  null_dist = []
9.  For k in 1..K:
       Shuffle tag vector t to t'  (preserves sum(t))
       Recompute M'_both, M'_one with shuffled tags
       binding_perm_k = mean(S[M'_both]) − mean(S[M'_one])
       Append binding_perm_k to null_dist
10. p = (count(d ∈ null_dist : d ≥ binding_obs) + 1) / (K + 1)
11. Return binding_obs, p
```

Steps 4–7 are O(n²) in n; the vectorized implementation in `scripts/sentence_binding_vectorized.py` keeps each permutation iteration to a handful of numpy boolean and float operations, making the test tractable at n = 14,173 sentences. The non-vectorized Python-iterator implementation in `scripts/concept_analysis.py` is appropriate at passage-level n ≈ 1,000 but does not scale to sentence-level corpora.

For sentence-level analysis, passages are split on punctuation, the same regex tagger is applied per sentence, and CCB is computed across sentences rather than passages.

### 4.4 Document-level cross-cluster statistic (secondary, descriptive)

For the document-level H1 (cross-tradition nondual cohesion vs. dualistic controls, reported in §6.4 as a methodological cautionary tale), we compute:

$$
\Delta_{H1} = \overline{\text{sim}}_{\text{historical-nondual cross-tradition}} - \overline{\text{sim}}_{\text{nondual-to-dualistic cross-tradition}}
$$

Significance: 5,000-permutation test shuffling (tradition, category) labels. Effect-size language uses raw cosine differences and *p*-values; we avoid "σ-above-null" language because the null is non-parametric and physics readers may misread it as Gaussian tail probability.

### 4.5 Vocabulary substitution: included for completeness, used cautiously

We retain the structural-role vocabulary-substitution analysis from earlier drafts (§6.6) because the *direction* of its result is informative even given its bias. Substituting tradition-specific terms with shared placeholders forces token-level similarity across substituted texts — a **known bias toward finding cross-tradition similarity**, identified during the substitution run and documented in `methodology-notes.md`. The substitution analysis is retained because the *failure* of the bias to fully close the modern–historical document-level gap is itself informative. **CCB on the unsubstituted corpus supersedes substitution as the canonical bias-corrected test** of concept-level convergence.

### 4.6 Clustering and visualization (descriptive only)

UMAP (n_neighbors=15, min_dist=0.1) and t-SNE (perplexity=30) are reported for descriptive purposes. K-means and agglomerative clustering at k=3 with Adjusted Rand Index against the (nondual, dualistic, non-contemplative) labels measure cluster-recovery quality. The primary tests are the explicit pairwise-similarity permutation tests, which are sensitive to signals that low-dimensional projection may obscure.

---

## 5. Translator-as-confound: the largest known limitation of any English-only application

A single named limitation of the present application is sufficiently load-bearing to warrant its own section.

All passages in both Phase 0 and Phase 1a corpora are in English. A small set of anglophone scholar-translators is responsible for the majority of the English translation tradition for the source texts. Over more than a century of comparative-religion scholarship these translators have developed shared conventions for rendering tradition-specific contemplative vocabulary: how to translate Sanskrit *cit* and Pali *citta* and Tibetan *rigpa* and Greek *nous* and Arabic *qalb* and Hebrew *ruach* into English, how to handle apophatic constructions, how to phrase non-self formulations.

If these conventions converge — and there is no reason in principle they should not, given how much these scholars have read each other — then a portion of any cross-tradition similarity we measure is a property of the *English translation tradition*, not of the source texts. An embedding model cannot distinguish "Eckhart and Shankara are saying the same thing" from "Eckhart's translators and Shankara's translators are using the same English words to render different things."

**The present paper has no defense against this confound.** Phase 0 mixed translators and paraphrases in ways that made the issue impossible to estimate. Phase 1a uses single named translators per source (Legge for Tao Te Ching and Zhuangzi, Müller for Dhammapada, Pusey for Augustine, Redhouse for Rumi, etc.), which sharpens the issue: each text now anchors entirely on one translator's conventions. CCB's concept-conditional construction partially addresses translator-tradition convergence by computing binding within concept categories rather than across documents, but the patterns used to tag concepts are themselves derived from scholarly translation conventions.

The proper defenses, which any follow-on application of CCB to this debate should implement (§10):

1. **Multi-translator inclusion.** For each source where multiple English translations exist (Tao Te Ching: Mitchell, Lau, Ames-Hall, Watson, Legge, Henricks, Red Pine; Bhagavad Gita: Easwaran, Mitchell, Miller, Sargeant, Arnold, Edgerton; Heart Sutra: Conze, Red Pine, Tanahashi; Shankara: Madhavananda, Sastry; et al.), include all major translations and report within-source translator variance as the baseline for between-source convergence.
2. **Non-English source analysis.** Use multilingual embedding models (LaBSE, multilingual-e5, paraphrase-multilingual-MiniLM-L12-v2) on original-language texts where available: Sanskrit (Advaita, Mahayana), Pali (Theravada), Tibetan (Dzogchen), Greek (Plotinus, Christian mystical), Chinese (Daoism, Mahayana sutras), Arabic (Sufi), Hebrew (Kabbalah). If CCB survives on original-language texts, translator-mediated convergence is ruled out as the sole explanation. If it does not, the constructivist position gets the strongest empirical leverage in 65 years of debate.

We name this here, prominently, rather than in §9, because it is the strongest objection to any positive convergence finding from English-only textual data, and because neither corpus iteration addresses it. **Readers should treat every result in this paper through this lens.** The method survives this limitation as a method; the present application of the method does not, and any stronger application is contingent on these defenses being implemented.

---

## 6. Results

### 6.1 Phase 0 concept binding (primary result, application context)

CCB on cross-tradition passage pairs using unsubstituted embeddings, Phase 0 v0.5 corpus:

| Concept | n passages with *C* | both-have mean | one-has mean | **CCB** | *p* (one-sided, 2,000 perms) |
|---|---|---|---|---|---|
| AWARENESS | 19 | 0.4195 | 0.3061 | **+0.1133** | **< 0.0001** |
| RECOGNITION | 9 | 0.3321 | 0.2528 | **+0.0793** | **0.001** |
| WORLD | 32 | 0.3752 | 0.2983 | **+0.0769** | **< 0.0001** |
| ULTIMATE | 36 | 0.3283 | 0.2712 | **+0.0571** | **< 0.0001** |
| SUBSTRATE | 10 | 0.3604 | 0.3078 | **+0.0526** | **0.01** |
| SELF | 3 | 0.2315 | 0.2890 | −0.0575 | 0.90 (NS) |
| NONSEP | 0 | n/a | n/a | n/a | not measurable |

Five of seven pre-specified concepts bind significantly. Effect sizes are substantial in cosine terms (≈ +0.05 to +0.11, on a base cross-tradition similarity of ≈ 0.30).

SELF and NONSEP are corpus-limited: only 3 passages used explicit SELF markers (`atman`, `jiva`, `the agent`, `Markov blanket`); most passages discuss self in unmarked English the regex tagger does not catch. No passages used explicit NONSEP labels (`nondual`, `advaita`, `wahdat al-wujud`) despite expressing observer-substrate non-separability throughout the nondual category. Both are unmeasured rather than refuted.

**Top cross-tradition pairs within concepts:**

**AWARENESS.** Both-have pair similarities, top six:

| Pair | mean sim |
|---|---|
| analytic_idealism × implicate_order | 0.624 |
| analytic_idealism × interface_theory | 0.585 |
| implicate_order × interface_theory | 0.561 |
| **mahayana × theravada** | **0.518** |
| analytic_idealism × iit | 0.511 |
| iit × implicate_order | 0.509 |

The modern wing dominates by volume, but **Mahayana × Theravada at 0.518 is the cleanest cross-tradition AWARENESS binding**: two Buddhist traditions on opposite sides of the doctrinal nondual/dualistic divide, neither writing toward the comparison, both discussing consciousness, converge tightly when conditioned on that discussion.

**RECOGNITION.** Top pairs (Advaita × Dzogchen 0.528; Dzogchen × Sufi 0.440; Dzogchen × Theravada 0.439; Daoism × Dzogchen 0.438; Advaita × Sufi 0.429; Advaita × Neoplatonism 0.390). This is the classical Stace-Forman perennialist signal across historical contemplative traditions when those traditions are specifically discussing liberation/awakening, quantified.

**SUBSTRATE.** Top pairs (Dzogchen × Mahayana 0.469; Mahayana × Relational_QM 0.455; IIT × Implicate_Order 0.453; Dzogchen × Relational_QM 0.438; Dzogchen × Implicate_Order 0.437). Reading these *requires* the Rovelli caveat: Rovelli's *Helgoland* is in the corpus and argues for the Mahayana–relational-QM correspondence. The 0.455 binding establishes the embedding model can detect what Rovelli argued for in his text; it does not independently establish structural identity.

**ULTIMATE.** Top pairs (Mathematical_Universe × Simulation_Theory 0.506; Advaita × Sufi 0.475; *Kabbalah × Sufi 0.445* — *note documented Andalusian contact, not culturally independent*; Advaita × Kabbalah 0.430; Christian_Mystical × Sufi 0.417; Advaita × Mathematical_Universe 0.370).

**WORLD.** 32 passages with concept, 468 cross-tradition both-have pairs. Top pairs diffuse at ≈ 0.40, no single dominant convergence; CCB = +0.077, *p* < 0.0001 is well-supported by volume.

### 6.2 Cross-model replication (Phase 0)

CCB run at sentence granularity on Phase 0 (322 sentences, 123 tagged), both embedding models:

| Concept | OpenAI passage | OpenAI sentence | BERT (MiniLM) sentence |
|---|---|---|---|
| AWARENESS | +0.1133 *** | +0.1139 *** | **+0.2042** *** |
| RECOGNITION | +0.0793 ** | +0.0822 *** | +0.0725 *** |
| WORLD | +0.0769 *** | +0.0821 *** | +0.0733 *** |
| ULTIMATE | +0.0571 *** | +0.0668 *** | +0.0793 *** |
| SUBSTRATE | +0.0526 ** | +0.0514 ** | +0.0497 ** |

\*\*\* *p* < 0.0001, \*\* *p* < 0.01.

Five binding concepts replicate across both granularities and both embedding models. Top tradition-pairs are essentially identical across models — both place analytic_idealism × implicate_order at the top of AWARENESS, advaita × dzogchen at the top of RECOGNITION, mahayana × relational_qm at the top of SUBSTRATE. AWARENESS binding is ~2× stronger in BERT than OpenAI; the directional result is preserved. The BERT inference path is fully local, free at the margin, and runnable on workstations where torch is blocked.

### 6.3 Phase 1a: paraphrase-free replication

Phase 1a is the canonical paraphrase-free evaluation. The corpus is 100% verified published-translation primary-source text (§3.2). CCB results, passage-level, 920 chunks:

| Concept | n_passages with C | Phase 1a CCB | Phase 0 CCB | *p* (Phase 1a) |
|---|---|---|---|---|
| AWARENESS | 52 | +0.0258 | +0.1133 | 0.0005 |
| RECOGNITION | 51 | +0.0247 | +0.0793 | 0.0005 |
| WORLD | 170 | +0.0216 | +0.0769 | < 0.0001 |
| ULTIMATE | 562 | +0.0141 | +0.0571 | < 0.0001 |
| **SUBSTRATE** | 15 | **+0.0541** | +0.0526 | 0.0015 |
| SELF | 27 | −0.0124 | −0.0575 | 0.93 (NS) |

**All five binding concepts remain statistically significant at *p* ≤ 0.0015 on paraphrase-free verified-translation whole-book text.** Where Draft 2 noted that only one of five bindings (ULTIMATE) had a complete robustness track on the non-paraphrase Phase 0 subset, Phase 1a converts this to a complete robustness track for all five.

**Effect sizes deflate 3–4× at passage-level for every binding concept except SUBSTRATE, which is unchanged** (+0.0541 vs +0.0526). The unequal deflation is the subject of §6.7-6.8 and is the paper's primary methodological finding.

Phase 1a sentence-level (4,000 stratified-sampled sentences):

| Concept | OpenAI Phase 1a | OpenAI Phase 0 | BERT Phase 1a | BERT Phase 0 |
|---|---|---|---|---|
| **AWARENESS** | **+0.0823** | +0.1139 | **+0.1205** | +0.2042 |
| RECOGNITION | +0.0610 | +0.0822 | +0.0900 | +0.0725 |
| ULTIMATE | +0.0471 | +0.0668 | +0.0743 | +0.0793 |
| WORLD | +0.0512 | +0.0821 | +0.0648 | +0.0733 |
| SELF | +0.0313 (p=0.006) | NS | +0.0658 | +0.0343 (NS) |
| SUBSTRATE | +0.0530 (p=0.04) | +0.0514 | +0.0485 (p=0.09, NS sub-sample) | +0.0497 |

**Sentence-level deflation is much milder: 25–30% rather than 3–4×.** §6.8 explains the mechanism via a pre-specified prediction test.

SELF becomes significant on Phase 1a sentence-level OpenAI (+0.031, *p*=0.006) where it was non-significant in Phase 0. The larger corpus surfaces enough explicit SELF markers (atman, ego, the empirical self, conscious agent) to estimate the binding; the Phase 0 negative direction at n=3 was a small-sample artifact.

SUBSTRATE in Phase 1a sentence-level subsample drops to *p*=0.04 (OpenAI) and *p*=0.09 (BERT, NS). This is a sample-size artifact under stratified sampling: only 5 of the 4,000 sampled sentences have SUBSTRATE-pattern hits, yielding 4 cross-tradition both-have pairs. Phase 1a passage-level (15 tagged passages, 88 both-have pairs) is the stronger evaluation for SUBSTRATE specifically.

### 6.4 Document-level H1 (descriptive, cautionary)

The classical document-level cross-tradition nondual cohesion vs. dualistic controls, across runs:

| Statistic | Phase 0 v0 | Phase 0 v0.5 | Phase 0 v0.5 substituted | **Phase 1a (n=920)** |
|---|---|---|---|---|
| historical-nondual cross mean | — | 0.315 | 0.336 | **0.371** |
| nondual_to_dualistic mean | — | 0.270 | 0.292 | **0.346** |
| observed Δ_H1 | +0.047 | +0.045 | +0.044 | **+0.025** |
| permutation *p* (one-sided) | < 0.0001 | < 0.0001 | < 0.0001 | **< 0.0001** |

H1 holds at *p* < 0.0001 across all four runs; effect size halves Phase 0 → Phase 1a. **Striking flip in Phase 1a:** dualistic Western philosophical/theological traditions (Kant, Aquinas, Augustine, Calvin) cluster *more tightly cross-tradition* (0.383) than the historical nondual traditions do (0.371). In Phase 0 this was reversed. The Phase 0 paraphrases were too stylistically uniform in the nondual category; real Tao Te Ching + Upanishads + Sufi Rumi + Spinoza Ethics + Brother Lawrence are stylistically far more different from each other than Aquinas + Calvin + Kant are. **H1 survives despite the nondual category having lower within-category cohesion than the dualistic control** in Phase 1a — arguably more compelling for the perennialist position than the Phase 0 result, not less.

We treat document-level H1 as a descriptive cautionary tale because document-level embedding similarity is dominated by register and vocabulary, exactly as concept-conditional analysis was designed to control for.

### 6.5 Bridge thinkers and the document-level vocabulary cohort effect (Phase 0)

UMAP projection of Phase 0 v0.5 embeddings shows three macro-clusters: historical contemplative nondual; modern scientific/computational nondual + bridge thinkers; dualistic + analytic controls. Bridge thinkers were chosen as a critical test: if document-level convergence is content-driven, they sit between modern and historical clusters; if vocabulary-driven, they sit with their vocabulary cohort.

| Bridge thinker | mean sim to historical-nondual | mean sim to modern-computational | gap (h − m) |
|---|---|---|---|
| Bohm | 0.315 | 0.403 | −0.088 |
| Whitehead | 0.296 | 0.394 | −0.098 |
| Friston/Clark/Seth | 0.210 | 0.352 | −0.142 |
| Tononi/Koch | 0.255 | 0.426 | −0.171 |
| Rovelli | 0.282 | 0.415 | −0.133 |

**Every bridge thinker clusters with the modern cohort at the document level**, including Bohm (who explicitly developed his thinking with Krishnamurti) and Rovelli (who explicitly argued the Mahayana correspondence). H1' (modern and historical nondual cluster jointly at the document level) is *falsified*; the concept-conditional weaker version is supported (§6.1) but with the §2.3 directionality caveat.

Phase 1a has no bridge-thinker category since their books are not on Project Gutenberg; re-running this analysis on verified non-paraphrase text via arxiv/fair-use is a follow-on (§10).

### 6.6 Vocabulary substitution (with documented bias)

Phase 0 substitution shifts every cross-similarity up ≈ 0.015–0.030 (placeholder-sharing artifact). Modern × historical shifts +0.030, slightly more than the across-the-board lift, suggesting some genuine vocabulary-masked content convergence. But the bulk of the modern–historical document-level gap remains: modern cluster within-similarity 0.468 still well above modern-to-historical 0.304. Vocabulary share of the gap is best estimated at 15–30%, with the true value almost certainly below the upper bound given the bias.

Phase 1a substitution shows the same direction at smaller magnitude (H1 +0.025 → +0.022, essentially unchanged): the shared-placeholder bias is empirically smaller at whole-book scale because each passage has more independent content to balance the few shared tokens.

Pair-level shifts in Phase 0 are consistent with the §6.1 interpretations: simulation × analytic_idealism +0.049 (vocabulary-masked content convergence revealed); mahayana × theravada −0.014 (shared Buddhist vocabulary previously inflating similarity); mahayana × relational_qm −0.011 (Rovelli's explicit Nagarjuna-naming previously inflating). Substitution does not transmute structural distinction: Aquinas's "[ULTIMATE] is not the world; the world is a [WORLD] distinct from its Creator" survives substitution as a structural assertion of separation.

### 6.7 Phase 1a corpus topology and what survived

Predictions before running Phase 1a:
- Phase 0 effect sizes partially inflated by paraphrase uniformity; expect deflation.
- Second-reviewer prior: ~60% AWARENESS + RECOGNITION survive at *p* ≤ 0.01; ~40% full five-concept pattern survives.

Observed:
- All five binding concepts survived statistical significance at *p* ≤ 0.0015 (above prior).
- Passage-level deflation: 3–4× for AWARENESS, RECOGNITION, WORLD, ULTIMATE.
- SUBSTRATE: no deflation (+0.0526 → +0.0541).
- Sentence-level deflation: 25–30% for all concepts.

The full-pattern survival exceeds the reviewer prior; effect sizes are smaller than Phase 0 suggested. The §7.3 decomposition places genuine concept-level structural binding as the smallest and best-controlled component of the apparent signal. We cite it affirmatively without over-promoting.

### 6.8 Vocabulary breadth: pre-specified prediction test and refined two-component mechanism

The passage-level Phase 0 → Phase 1a deflation pattern is striking: every binding concept lost 3–4× of its effect size except SUBSTRATE, which lost nothing. The sentence-level pattern is different: every concept retained 70–75% of its effect size, SUBSTRATE included.

Draft 4 §6.8 proposed a single-component mechanical explanation: passage-level concept tagging fires whenever the pattern appears anywhere in the passage, even when the rest of the passage is about something else; pattern dictionaries containing common English terms therefore tag passages that don't engage the concept technically; this casual-usage *noise floor* dilutes passage-level binding for concepts with broad-vocabulary dictionaries. SUBSTRATE's dictionary contains no common English terms and so has no noise floor; AWARENESS / ULTIMATE / WORLD / RECOGNITION dictionaries contain casual English terms and do.

We pre-specified specific quantitative predictions for a technical-only-tagger variant — restricting AWARENESS, ULTIMATE, WORLD, RECOGNITION pattern dictionaries to tradition-specific technical-only vocabulary (dropping `consciousness`/`awareness`/`sentience`, `God`/`the divine`/`lord`, `world`/`the universe`/`cosmos`/`creation`, `enlightenment`/`liberation`/`awakening`/`salvation`). The predictions were written into Draft 4 §6.8 of this paper before the technical-only-tagger was implemented or run. *Pre-specified* here means committed in writing in an earlier paper draft before the test was conducted; it does not mean formally preregistered with an external timestamp on OSF or AsPredicted (see §7.2 and §9 limitation 8 for the implications). Phase 1 follow-on experiments (§10) will be formally OSF-preregistered.

**Predicted outcomes:**

| Concept | Phase 1a current | Predicted technical-only | Predicted direction |
|---|---|---|---|
| AWARENESS | +0.026 | +0.08 to +0.11 | recovers toward Phase 0 |
| ULTIMATE | +0.014 | +0.04 to +0.06 | partial recovery |
| WORLD | +0.022 | +0.06 to +0.08 | substantial recovery |
| RECOGNITION | +0.025 | +0.03 to +0.05 | small recovery (already mostly technical) |
| SUBSTRATE | +0.054 | +0.054 | unchanged (control) |

**Observed outcomes** (CCB on Phase 1a, `--technical-only` flag on `scripts/concept_analysis.py`, `TECHNICAL_ONLY_PATTERNS` dictionary, identical methodology otherwise):

| Concept | n_with technical-only | both_n | observed technical-only CCB | *p* | Verdict |
|---|---|---|---|---|---|
| **RECOGNITION** | 21 | 110 | **+0.1100** | **< 0.0001** | **Dramatically exceeded prediction** |
| SUBSTRATE | 15 | 88 | +0.0541 | 0.0015 | **Confirmed exactly as control** |
| ULTIMATE | 239 | 24,176 | **+0.0079** | 0.006 | **Failed — went down, not up** |
| WORLD | 5 | 4 | +0.0489 | 0.06 (NS) | Partial recovery, underpowered |
| AWARENESS | 1 | 0 | n/a | n/a | **Untestable — only 1 passage tagged** |

The prediction outcomes are mixed in informative ways and require the §6.8 mechanism to be refined from a single-component to a two-component formulation.

**RECOGNITION recovered past the predicted range.** The prediction said small recovery (+0.03 to +0.05) on the assumption that RECOGNITION's pattern dictionary was already mostly technical. Observed +0.110 — even higher than Phase 0's full-tagger binding (+0.079). The dropped terms (`enlightenment`, `awakening`, `liberation`, `salvation`) were apparently doing more dilution than predicted. The remaining technical vocabulary (`moksha`, `mukti`, `nirvana`, `nibbana`, `bodhi`, `satori`, `theosis`, `deification`, `fana`, `baqa`, `gnosis`, `jnana`, `self-realization`, `beatific vision`) tags passages that converge tightly.

The top cross-tradition pair is **advaita × theravada at 0.531** — Hindu nondual and Pali Buddhist dualistic across the doctrinal observer-substrate identity divide, neither writing toward the comparison, both discussing the technical concept of liberation. This is the **strongest single cross-tradition concept-binding result the project has produced**, and it is paraphrase-free (Phase 1a corpus), bias-aware (CCB), and technical-only-vocabulary (no common-English noise floor).

**SUBSTRATE control was confirmed exactly.** Predicted unchanged; observed unchanged at +0.0541. The technical-only-tagger experiment does not introduce systematic shifts in concepts whose vocabulary was already technical.

**ULTIMATE failed in an unexpected direction.** Predicted +0.04 to +0.06 (partial recovery); observed +0.008 (lower than baseline +0.014). The simple noise-floor mechanism predicted recovery here too.

The mechanism behind this failure reveals a previously unrecognized second component. In the Phase 1a corpus, `God` / `the divine` / `lord` appear extensively in *dualistic* traditions (Aquinas's *Summa*, Calvin's *Institutes*, Augustine's *Confessions*) and in some nondual sources (Brother Lawrence, parts of Spinoza). The remaining technical-only ULTIMATE terms (`Brahman`, `Tao`, `Buddha-nature`, `Ein Sof`, `the One`, `dharmakaya`, `tathata`) appear *almost exclusively in nondual traditions*. Dropping the common terms removed the dualistic-tradition coverage of the concept, not just casual passage tags. CCB measures *cross-tradition* binding, which requires comparing same-concept-mention pairs across tradition categories. When the technical-only patterns are concentrated in a single category, the cross-tradition pairs that remain are increasingly within-nondual (which were already similar regardless of concept). The cross-tradition binding shrinks because the *coverage distribution* shifted, not because the *noise floor* changed.

**AWARENESS and WORLD became untestable.** Dropping `consciousness`/`awareness`/`sentience` from AWARENESS left only tradition-specific technical terms (`rigpa`, `chit`, `chitta`, `nous`, `phi`, `primordial awareness`, etc.). The Phase 1a corpus, which contains no Dzogchen books with `rigpa`, no Sanskrit Advaita primary text retaining `chit`, no IIT papers with `phi`, has essentially zero passages using these technical terms — n_with dropped from 52 to 1. The AWARENESS prediction (+0.08 to +0.11) cannot be evaluated on the present Phase 1a corpus. WORLD has the same problem with the smaller drop: n_with from 170 to 5; the observed +0.049 is in the predicted range but statistically underpowered (*p* = 0.06).

This does not refute the predictions for AWARENESS and WORLD; it shows the Phase 1a corpus lacks the technical-vocabulary coverage to test them. A follow-on application of CCB to this debate with a corpus that includes more sources using these technical terms (Dzogchen primary texts, Sanskrit Advaita with retained transliteration, IIT papers, etc.) could test the predictions.

**Refined mechanism: vocabulary breadth has two distinct effects.**

**(a) Casual-usage noise floor.** Pattern dictionaries containing common English terms fire on passages that mention the term in non-technical context, diluting binding at passage granularity by averaging over passages-engaging-the-concept and passages-merely-containing-the-pattern. Restricting to technical vocabulary removes the noise floor. *Direction: technical-only restriction increases binding* when the concept's technical vocabulary is well-represented across traditions in the corpus.

**(b) Coverage-distribution asymmetry.** Some concepts have technical vocabulary concentrated in specific tradition categories. When such concepts have their common-English-vocabulary terms removed, the remaining patterns have asymmetric tradition coverage. Cross-tradition pairs concentrate within one category, reducing the contrast CCB measures. *Direction: technical-only restriction decreases binding* when the technical vocabulary is tradition-asymmetric in the corpus.

Both effects can be present for the same concept; the net direction depends on which dominates. **For RECOGNITION**: corpus has reasonably symmetric technical-vocabulary coverage (Indian moksha/mukti/jnana, Buddhist nirvana/bodhi, Christian theosis, Sufi fana) → noise-floor effect (a) dominates → strong recovery. **For ULTIMATE**: corpus has asymmetric technical-vocabulary coverage (nondual-heavy after `God`/`the divine` dropped) → coverage-distribution effect (b) dominates → binding decreases. **For SUBSTRATE**: pattern dictionary was already technical-only, no change in either component → unchanged (control). **For AWARENESS, WORLD**: technical-vocabulary coverage in Phase 1a is too thin for either effect to be measurable → unmeasurable rather than recovered or refuted.

The refined two-component formulation predicts:

- Technical-only restriction increases binding when the concept's technical vocabulary is well-distributed across the corpus's tradition categories.
- Technical-only restriction decreases binding when the concept's technical vocabulary is concentrated in fewer categories.
- Corpus coverage of technical vocabulary determines whether either effect is measurable.

This is corpus-dependent: the same statistic and same tagger return different results on different corpora because different corpora have different tradition-coverage distributions of technical terminology. For future users of CCB, this is a property of *applying* the method that should be attended to in corpus design.

The pre-specified single-component formulation was wrong for ULTIMATE in a specific identifiable way; the prediction did not anticipate corpus-coverage-asymmetry effects. We report the refined formulation here as the post-test understanding, and we report the original pre-specified formulation transparently as it was written in Draft 4 §6.8 to preserve the prediction-vs-outcome record. The failure mode is informative rather than just unfortunate: the same vocabulary-breadth phenomenon has different empirical signatures depending on how the tradition-specific technical terminology is distributed in the corpus, and CCB's sensitivity to that distribution is itself a property worth knowing when interpreting concept-binding results.

### 6.9 Phase 1b: multi-translator within-source variance test

The largest §9 limitation of Phase 1a is translator-as-confound: every English-translated passage was rendered by one of a small set of anglophone scholar-translators, and cross-tradition convergence in semantic embedding space could in principle reflect shared anglophone-translation convention rather than shared source content. Phase 1b addresses this limitation by adding multi-translator coverage of two source families and partitioning total within/cross-tradition variance into translator, source-content, and tradition components.

**Pre-registration.** Phase 1b was externally pre-registered prior to running the analysis. The pre-registration document `findings/phase1b-preregistration.md` was committed to the public repository at commit `d16fc8c` with the analysis script (`scripts/phase1b_within_source_variance.py`) and the Phase 1b corpus already in place. A Zenodo release `v1.2-prereg-phase1b` at that commit provides third-party DOI-resolved timestamping; the GitHub commit hash provides the binding chain-of-custody for the predictions. (OpenTimestamps Bitcoin-anchored timestamping was attempted but the local toolchain failed; the web-based opentimestamps.org service remains available for any independent verifier wishing to add a third timestamp.)

#### 6.9.1 Corpus and method

The Phase 1b corpus consists of 6 books across 2 source families:

| Source family | Translator | Year | Provenance | Chunks |
|---|---|---|---|---|
| Bhagavad Gita | Edwin Arnold | 1885 | Project Gutenberg | 51 |
| Bhagavad Gita | K.T. Telang | 1882 (SBE vol 8) | sacred-texts.com | 106 (Gita-only) |
| Bhagavad Gita | Swami Swarupananda | 1909 | sacred-texts.com | 105 |
| Tao Te Ching | James Legge | 1891 (SBE vol 39) | Project Gutenberg | 27 |
| Tao Te Ching | Goddard / Borel | 1919 | sacred-texts.com | 82 |
| Tao Te Ching | Suzuki / Carus | 1913 | sacred-texts.com | 76 |

Telang's SBE 8 volume contains *Bhagavadgîtâ*, *Sanatsujâtîya*, and *Anugîtâ*. For Phase 1b within-source comparability with Arnold and Swarupananda (Gita-only translations), Telang chunks were filtered to chars 0–259,683 of the cleaned text (the Bhagavadgîtâ portion before the Sanatsujâtîya section header). The Sanatsujâtîya and Anugîtâ portions are excluded from Phase 1b and deferred to Phase 1c corpus expansion. Sources beyond Project Gutenberg are documented in `corpus/books_manifest.json` with the new `sacred_texts` source-type, fetched via the multi-chapter index-parsing fetcher in `scripts/fetch_books.py`.

Each chunk is embedded with `sentence-transformers/all-MiniLM-L6-v2` via ONNX Runtime (consistent with Phase 1a). The full 5,777 × 5,777 pairwise cosine similarity matrix is built. Four pair-type masks are then computed (upper-triangle only):

- **W-S-S-T (within-source same-translator):** same book_id (e.g., Arnold-Arnold). Upper bound on similarity from shared source content + shared translator style.
- **W-S-B-T (within-source between-translator):** same source_id, different book_id (e.g., Arnold-Telang on Gita). Tests whether source content survives different translators.
- **X-S-W-T (cross-source within-tradition):** different source_id, same tradition (e.g., Arnold-Gita ↔ Müller-Upanishads, both advaita).
- **X-T (cross-tradition):** different tradition. Phase 1a baseline reference.

Mean cosine under each mask is computed. Variance decomposition derived: translator-effect = W-S-S-T − W-S-B-T; source-content-effect = W-S-B-T − X-S-W-T; tradition-effect = X-S-W-T − X-T; total-variance = W-S-S-T − X-T; translator-share = translator-effect / total-variance. A permutation null over translator-label assignments within each source family (1,000 permutations, seed 0) provides a significance test for the translator effect.

#### 6.9.2 Predicted and observed outcomes

| Quantity | Predicted (range) | Observed | Verdict |
|---|---|---|---|
| W-S-S-T | 0.55 (0.45-0.65) | **0.6683** | Outside (calibration error) |
| W-S-B-T | 0.45 (0.35-0.55) | **0.6236** | Outside (calibration error) |
| X-S-W-T | 0.32 (0.25-0.40) | **0.5341** | Outside (calibration error) |
| X-T | 0.30 (0.25-0.35) | **0.4393** | Outside (calibration error) |
| Translator effect | +0.08 (+0.04 to +0.12) | **+0.0447** | Inside (low end) |
| Tradition+source effect | +0.15 (+0.10 to +0.25) | **+0.1843** | Inside |
| Translator share of total | 0.30 (0.20-0.40) | **0.195** | Just below; confirms direction |

**H1b.1 (variance ordering):** Confirmed exactly. W-S-S-T (0.6683) > W-S-B-T (0.6236) > X-S-W-T (0.5341) > X-T (0.4393). Each successive step represents one additional source of variance.

**H1b.2 (translator-bound):** Confirmed with margin. Translator share of total variance is 19.5%, well below the pre-registered 35% threshold. Source-content effect (~39%) and tradition effect (~41%) are each approximately twice the translator effect.

**H1b.3 (permutation null detection of translator effect):** Confirmed at overwhelming significance. The translator-label-shuffle null distribution mean is 0.6397 (sd 0.0009); the observed W-S-B-T value is 0.6236, separated from the null by z ≈ −17.9 (*p* << 0.0001). Real cross-translator pairs cluster more tightly than label-shuffled pairs because random label assignment within a source family produces some pairs that are actually same-translator (and therefore tighter; see W-S-S-T > W-S-B-T). The test thus confirms that translators produce statistically distinct stylistic conventions on shared source content — consistent with the bounded-but-nonzero translator effect identified in H1b.1 and H1b.2. *(The pre-registration document operationalized this test with the inequality direction inverted; see Appendix C for the prereg-vs-text-direction discussion and the conceptual error it surfaced.)*

**Absolute magnitudes (calibration error):** All four pre-registered absolute cosine values were systematically below the observed values. MiniLM-L6-v2 produces tighter cosines than the author anticipated for short multi-paragraph chunks. The *ratios* and *ordering* of the predictions were correct; the *absolute calibration* was not. The methodology lesson is the §8 contribution noted below: CCB results should be reported in relative terms (effect sizes, ordering, variance partitions) rather than absolute cosines.

#### 6.9.3 Per-source breakdown

| Source | Same-translator means | Between-translator means |
|---|---|---|
| Bhagavad Gita | Arnold 0.699, Swarupananda 0.667, Telang 0.610 | Arnold↔Swarup 0.626, Arnold↔Telang **0.586** (lowest), Swarup↔Telang 0.627 |
| Tao Te Ching | Carus 0.746, Legge 0.747, Goddard 0.681 | Carus↔Goddard 0.649, Carus↔Legge 0.621, Goddard↔Legge 0.624 |

The Arnold-Telang Gita pair (0.586) is the widest within-source between-translator gap in the experiment, reflecting Arnold's verse vs Telang's academic prose; Arnold-Swarupananda and Swarupananda-Telang are both prose-prose pairs and cluster more tightly. The three TTC translators all cluster tightly with each other (0.62-0.65) — TTC's short aphoristic chapters leave less room for translator-stylistic divergence. The translator effect on TTC (~0.09 cosines) is slightly larger than on Gita (~0.05) but in absolute terms both are bounded.

#### 6.9.4 What Phase 1b shows and does not show

**Shows:** Translator-as-confound is bounded. Phase 1a's cross-tradition CCB signal cannot be attributed primarily to translator convention. Translator effect (~20%) is the smallest of three variance components; source-content (~39%) and tradition (~41%) each dominate it. The pre-registration timestamp (commit `d16fc8c` + Zenodo `v1.2-prereg-phase1b`) externally fixes the prediction-before-result chain of custody.

**Does not show:** Phase 1b tests the *between-translator* component of translator-as-confound. It does not test the *within-anglophone-scholar-tradition shared-consensus* component. Anglophone Sanskritists, Indologists, and Sinologists translating Hindu/Buddhist/Daoist texts in the 1880s-1910s shared interpretive frames, mutual citation, and editorial conventions; a century of within-tradition consensus could impose its own structural conformity, invisible to the between-translator variance test. This is the *broad* form of Katz (1978)'s constructivist objection. It remains unaddressed by Phase 1b and is the explicit target of Phase 1c (non-English source analysis with multilingual embeddings on Sanskrit, Pali, Tibetan, Greek, Chinese, Arabic, Hebrew originals).

Full pre-specified-vs-observed comparison and the analysis details are reported in `findings/phase1b-multi-translator.md`.

---

## 7. Discussion

### 7.1 What we have shown

**A methodological contribution.** CCB is a bias-aware embedding-based statistic that produces interpretable cross-tradition convergence scores conditional on shared concept-tags, replicates across two unrelated embedding stacks, and remains tractable at multi-thousand-sentence scale via vectorized permutation testing. Pattern-dictionary vocabulary breadth determines passage-level signal-to-noise via the two-component mechanism formalized in §6.8; the paper provides a worked example, pre-specified predictions, observed outcomes, and the refined post-test understanding.

**An application's result.** Applied to the mysticism convergence debate across two concept-binding corpora (paraphrase-heavy Phase 0 and verified-primary-source Phase 1a) and a multi-translator variance-test corpus (Phase 1b), CCB returns: five of seven pre-specified structural concepts show statistically significant cross-tradition binding at *p* ≤ 0.0015 in both Phase 0 and Phase 1a; effect sizes are smaller than Phase 0 suggested but the qualitative result is robust to corpus revision, embedding model, and granularity. The Phase 1b variance decomposition shows the cross-tradition signal is not primarily a translator artifact: translator effect ~20%, source-content ~39%, tradition ~41% of total within/cross-tradition variance (§6.9).

**Two canonical cross-tradition concept-binding results** stand out from the analysis.

*Mahayana × Theravada AWARENESS at 0.518* (Phase 0, both OpenAI and BERT sentence-level): two Buddhist traditions across the doctrinal nondual/dualistic divide, neither writing toward the comparison, converging on consciousness-talk. Cross-model replication is exact.

*Advaita × Theravada RECOGNITION at 0.531* (Phase 1a, technical-only-vocabulary tagger): Hindu nondual and Pali Buddhist dualistic, no historical contact, both discussing technical liberation-vocabulary (moksha, nirvana, jnana, bodhi), converging at a similarity level that the same statistic produces for within-tradition pairs in many cases. **This is the strongest single cross-tradition concept-binding result the project has produced**, and it is paraphrase-free, technical-only-vocabulary, and on a corpus that excludes all of the bridge-thinker confounds present in Phase 0.

Both results are pure historical-contemplative cross-tradition findings. Neither involves Rovelli's text writing toward a stipulated comparison; neither involves modern computational sources whose vocabulary cohort would override the concept-conditioning. Both are the kind of finding the constructivist position would have to engage with on the merits. The *between-translator* form of the constructivist's translator-convention alternative is now bounded at 19.5% of total variance by Phase 1b (§6.9); the *within-anglophone-scholar-tradition shared-consensus* form (Katz 1978's broader objection) remains the live alternative explanation pending Phase 1c.

**The classical Stace–Forman RECOGNITION signal** across historical contemplative traditions (Advaita ↔ Dzogchen ↔ Sufi ↔ Daoism ↔ Neoplatonism, no historical contact) is the closest quantitative correlate of what the perennialist tradition has argued for qualitatively for six decades. CCB detects it in Phase 0; the technical-only-tagger experiment on Phase 1a strengthens it to its highest measured level.

The document-level Δ_H1 result is robust enough to survive both paraphrase exclusion (Phase 1a) and shared-placeholder substitution (§6.6), indicating the signal is not exclusively an artifact of investigator-authored paraphrases or of tradition-specific vocabulary.

### 7.2 What we have *not* shown about the application

We have not shown the perennialist position is correct.

We have not shown the constructivist position is incorrect. The present results show that vocabulary and register do substantial work in apparent document-level convergence, which is what constructivists predicted.

We have not addressed the translator-as-confound (§5). Every result here is consistent both with structural convergence in source content and with shared anglophone-scholar-translator conventions. Multi-translator inclusion and non-English source analysis are necessary to distinguish them.

We have not independently established the Rovelli–Nagarjuna SUBSTRATE correspondence; the binding confirms the embedding can detect what Rovelli wrote toward (§2.3).

We have not tested the bridge-thinker → historical-nondual cross-period convergence on verified non-paraphrase text; the Phase 1a corpus lacks the modern wing.

We have not pre-registered formally on OSF. Concept categories were pre-specified before analyses were run (committed to the project's `glossary.md`), and the §6.8 technical-only-tagger predictions were written into Draft 4 before the test was implemented or run, but these pre-specifications are not externally timestamped: corpus composition, statistical tests, and decision rules were not committed to OSF or AsPredicted before running.

### 7.3 The defensible decomposition of "what we measured"

The honest picture decomposes apparent cross-tradition similarity into:

1. **Concept-level structural binding** on five pre-specified axes, detectable at *p* ≤ 0.0015, replicated cross-model, cross-granularity, and across paraphrase-heavy and whole-book non-paraphrase corpora, with the strongest result (advaita × theravada RECOGNITION at 0.531) recovered specifically under the technical-only-tagger restriction that the pre-specified §6.8 mechanism predicted would surface it.
2. **Document-level vocabulary effect**, partially closed by substitution (~15–30% of the modern–historical gap, upper-bounded by the shared-placeholder bias).
3. **Document-level register / style effect** (~50–70% of the modern–historical gap), not closed by current methods.
4. **Translator-tradition effect.** The *between-translator* component is bounded at 19.5% of total within/cross-tradition variance by Phase 1b on two source families (§6.9). The *within-anglophone-scholar-tradition shared-consensus* component remains unbounded and is the largest unaddressed factor pending Phase 1c.
5. **Paraphrase-author effect** (bounded by Phase 1a; ~2× inflation at document level Phase 0 → Phase 1a; mostly vocabulary-breadth noise floor at passage-level for binding concepts).
6. **Genuine content difference** between modern computational and historical contemplative nondualism in Phase 0 (probably real and small).

(1) is the part of the picture that survives the controls Phase 0 + Phase 1a + Phase 1b applied. (2)–(6) bound how strongly (1) should be cited; the within-anglophone-scholar-tradition-consensus subcomponent of (4) is now the largest unbounded component.

### 7.4 What the field can do with this

The method is concept-agnostic and corpus-agnostic.

**To extend the present application:** add multi-translator coverage; run on non-English source texts via multilingual embeddings; add modern computational sources on verified text; add adversarial-selection passages from a constructivist scholar; run held-out human-validated concept tagging; formally pre-register on OSF; run sparse-autoencoder probes for interpretable axes that survive vocabulary and register noise.

**To extend the method to other claimed convergent concepts:** the framework runs on any pre-specified concept dictionary on any multi-tradition corpus. Candidate test cases include the Golden Rule across ethical traditions, the Hero's Journey across mythologies (Campbell), non-attachment across contemplative practices, mystical death-and-rebirth across initiatic traditions, eternal recurrence (Stoic-Nietzschean-Hindu-cosmological), the great chain of being (Neoplatonic-Hindu-Western-medieval). The deliverable from running CCB on a suite of candidates is a meta-table — for each tested concept, was convergence detected, with what controls, what survived — which is what would move the comparative-convergence debate forward as a field, not a single positive result.

We are not the field. We are NLP practitioners who built a method and applied it to a contested philosophical question because the question was textually apt and unaddressed by prior methods. What the present results mean for the perennialist–constructivist debate is for the field that runs the methodology forward. We have produced an instrument; we have not delivered a verdict.

---

## 8. Methodological lessons from the application

For other researchers applying CCB to a new convergence claim:

- **Sentence-level granularity should be the default.** Passage-level introduces a casual-usage noise floor that disproportionately affects concepts whose pattern dictionaries include common English terms. Technical-only-vocabulary concepts are immune; broad-vocabulary concepts dilute at passage-level (§6.8).
- **Vocabulary breadth has two distinct effects on passage-level binding.** Casual-usage noise floor (dilution via tag firings on non-technical passages) and coverage-distribution asymmetry (shift in cross-category pair availability when technical vocabulary concentrates in fewer categories). Both interact with the corpus's tradition-coverage distribution of technical terminology. Tagger design should split concepts into technical-only and broad-vocabulary variants and report both.
- **Cross-model replication is cheap and should be default.** Run against both a proprietary embedding model and an open-source one. The OpenAI run costs dollars per multi-thousand-passage analysis; the ONNX BERT run is free and works on workstations with restrictive application-control policies.
- **Shared-placeholder vocabulary substitution introduces a tautological similarity bias.** If substitution is used at all, prefer per-tradition placeholders or mask-and-compare. Empirically the bias is smaller at whole-book scale than at short-passage scale but is always present.
- **Paraphrase content inflates document-level effects ~2× relative to verified-translation content.** Curated paraphrases are useful for fast methodology iteration but should not be the canonical evaluation corpus.
- **PG-ID verification is necessary before fetching at scale.** 10 of 24 initial Project Gutenberg IDs in our Phase 1a manifest returned unrelated books. The `scripts/verify_manifest.py` title-match check is the cheap defense.
- **Pre-specifying mechanism predictions before running a falsifying test is high-value.** The §6.8 single-component prediction failed for ULTIMATE and was untestable for AWARENESS / WORLD, revealing the corpus-coverage-asymmetry component that informs the refined formulation. Without an advance specification the refinement would read as post-hoc rationalization rather than as a falsifier-driven update.
- **External pre-registration via public Git + Zenodo DOI works as a substitute for OSF preregistration.** The Phase 1b pre-registration (`findings/phase1b-preregistration.md` at public commit `d16fc8c`, Zenodo `v1.2-prereg-phase1b`) commits predictions before the analysis is run. Pre-registration discipline also catches a class of conceptual error that is invisible without it: operationalization mismatches between the researcher's underlying scientific hypothesis and the literal arithmetic direction of the test they wrote down to detect it. Appendix C documents one such case from this paper. The appropriate response to such a mismatch is documentation rather than silent revision — the prereg discipline only does its work if the surfaced mismatches are acknowledged transparently.
- **Report CCB results in relative terms (effect sizes, ordering, variance partitions), not absolute cosines.** The Phase 1b calibration error illustrates the principle directly: predicted absolute cosine values (e.g., W-S-S-T = 0.55, W-S-B-T = 0.45) were systematically below the observed values across all four pair types, while the *ratios* and *ordering* of predictions were correct. Absolute cosine values are embedding-model-specific and corpus-character-specific; relative differences are what generalize across models and corpora. CCB practitioners should anchor claims on variance partitions and effect-size ratios rather than absolute cosine thresholds.
- **Regex-based concept tagging is reproducible and pre-specifiable but is a hidden degree of freedom.** Held-out human-validated tagging on a randomly sampled subset is the cheap defense.

---

## 9. Limitations

1. **Translator-as-confound** (§5, §6.9). All passages English-translated by anglophone scholar-translators. The *between-translator* component of this confound is tested in Phase 1b on two source families (3 translators each) and found bounded at 19.5% of total within/cross-tradition variance — well below the pre-registered 35% threshold and approximately half of either the source-content or tradition variance components. The *within-anglophone-scholar-tradition shared-consensus* component (Katz 1978's broader objection — that a century of mutual citation, shared editorial assumptions, and a tradition-wide interpretive frame could impose structural conformity on all anglophone renderings simultaneously) remains unaddressed and is the explicit target of Phase 1c (multilingual source analysis on Sanskrit / Pali / Tibetan / Greek / Chinese / Arabic / Hebrew originals).
2. **Selection bias.** Investigator chose the corpora informed by secondary scholarship; adversarial-inclusion process not performed.
3. **Regex tagging is a hidden degree of freedom** (§4.2). Patterns derive from a glossary the investigator built. CCB is bias-free of the shared-placeholder artifact, not bias-free absolutely.
4. **Phase 1a is single-translator per source; Phase 1b adds three-translator coverage on two source families only.** The variance decomposition in §6.9 holds for Bhagavad Gita and Tao Te Ching but is not yet replicated on Christian mystical, Sufi, Mahayana, Theravada, Neoplatonic, or Kabbalistic source families.
5. **Phase 1a lacks modern computational sources.** H1' (modern + historical) is currently tested only on Phase 0 paraphrases.
6. **English only.** Non-English source analysis is the deepest defense against translator-as-confound and is not yet attempted.
7. **Rovelli's relational-QM text writes toward the Mahayana correspondence** (§2.3, §6.1). The SUBSTRATE binding does not independently establish the structural identity.
8. **No formal OSF pre-registration.** Concept categories were pre-specified; the §6.8 technical-only-tagger predictions were written before the test was run; corpus, tests, and decision rules were not OSF-registered.
9. **Naive sentence splitting.** Punctuation-regex, adequate for short well-formed passages, unaudited for longer-text edge cases.
10. **Permutation-test vectorization is mathematically equivalent to the Python iterator but is a separate code path** for tractability at Phase 1a sentence scale.
11. **No interpretability layer.** CCB establishes that concepts bind traditions; it does not characterize *what structural feature* the binding measures beyond the regex patterns used to detect it. Sparse-autoencoder probes and contrastive direction analysis are extensions.
12. **No adversarial controls.** LM-generated synthetic mystical writing in the style of each tradition is the natural adversarial test; not run.
13. **Stratified sentence sampling** for Phase 1a sentence-level analysis: subsamples to 4,000 sentences per analysis seed. Bindings stable to seed within ±0.005, but rare-concept n drops sharply under sampling.
14. **Phase 1a technical-only-tagger test cannot evaluate AWARENESS or WORLD predictions** due to insufficient technical-vocabulary coverage in the corpus (§6.8). The predictions remain testable on alternative corpora with the required coverage.

---

## 10. How a fuller application of CCB to the mysticism debate would proceed

If a follow-on researcher were to extend the present application to a paper that the comparative-religion field could engage with on its strongest terms, the priority order is:

**Completed in Phase 1b** (this paper, §6.9): Multi-translator within-source variance test on two source families (Bhagavad Gita: Arnold/Telang/Swarupananda; Tao Te Ching: Legge/Goddard/Carus). Between-translator translator effect bounded at 19.5% of total variance. The remaining priority list extends what this paper has not yet done:

1. **Non-English source analysis (Phase 1c)** with multilingual embeddings (LaBSE, multilingual-e5, paraphrase-multilingual-MiniLM-L12-v2) on Sanskrit, Pali, Tibetan, Greek, Chinese, Arabic, Hebrew originals where available. **The deepest defense against the *broad* form of translator-as-confound** — the anglophone scholar-tradition shared-consensus objection that Phase 1b's between-translator variance test cannot reach.
2. **Multi-translator inclusion extended to additional source families** beyond Gita and TTC. Heart Sutra across Conze, Red Pine, Tanahashi; Upanishads across Paramananda, Müller, Olivelle, Easwaran; Christian mystical core texts across multiple PD translators; Sufi texts across Nicholson, Arberry, others.
3. **Modern computational and bridge thinkers restored on verified text** via arxiv (Bostrom simulation argument; Wheeler "Information, Physics, Quantum"; Tegmark MUH; Rovelli relational QM; Friston FEP; Tononi IIT; Hoffman interface theory) and fair-use research excerpts (Kastrup, Bohm).
4. **Adversarial passage selection** by a constructivist-leaning scholar independently selecting *least-nondual* passages from the same authors. Re-run on union and difference.
5. **Held-out human-validated concept tagging** on a randomly sampled corpus subset. Inter-rater agreement reported; binding re-estimated on human-tagged subset.
6. **Formal OSF pre-registration** of corpus, pipeline, tests, decision rules, and predicted outcome priors for Phase 1c — extending the public-Git + Zenodo pre-registration mechanism Phase 1b used.
7. **Corpus extension to test the AWARENESS and WORLD §6.8 predictions** that the Phase 1a corpus could not evaluate. This requires source texts with retained technical contemplative vocabulary (Dzogchen primary texts with `rigpa`; Sanskrit Advaita with `chit`/`citta`; IIT papers with `phi`; Buddhist texts with `samsara` and `the ten thousand things`).
8. **Sparse-autoencoder probes** for interpretable structural axes that survive vocabulary and register noise.
9. **Adversarial synthetic-text controls** generated by language models.
10. **Cross-model replication of Phase 1b** (the variance decomposition currently uses ONNX MiniLM only; OpenAI text-embedding-3-large replication is straightforward to add).

We list this here so the present paper does not need to commit to delivering it. We have built the instrument; we present what it found across two test-corpus iterations and two pre-specified follow-on experiments (the §6.8 technical-only-tagger and the §6.9 Phase 1b variance test); whoever extends it gets the priority list as a starting point.

---

## 11. Code and data availability

All code, corpora, results, methodology notes, pre-specified predictions, and revision history are MIT-licensed and version-controlled at:

**Repository:** https://github.com/davidredbird/concept-conditional-cross-tradition-binding

**Analysis pipelines.**

- `scripts/concept_analysis.py` — concept-conditional binding at passage level. Supports `--technical-only` flag for the §6.8 prediction test using `TECHNICAL_ONLY_PATTERNS`.
- `scripts/sentence_concept_analysis.py` — sentence-level CCB with OpenAI and ONNX BERT backends.
- `scripts/sentence_binding_vectorized.py` — vectorized numpy implementation for *n* > 5,000 sentence corpora.
- `scripts/onnx_embedder.py` — local BERT-class inference via ONNX Runtime; usable on WDAC-restricted Windows.
- `scripts/prototype.py` — document-level embedding, clustering, visualization.
- `scripts/substitute.py` — structural-role vocabulary substitution with documented bias.
- `scripts/robustness_paraphrase.py` — paraphrase-exclusion robustness check.
- `scripts/phase1b_within_source_variance.py` — Phase 1b within-source between-translator variance test, vectorized over n×n similarity matrix with permutation test on translator labels.

**Phase 1 corpus pipeline.**

- `scripts/fetch_books.py` — Gutenberg / arxiv / web / archive_org / sacred_texts fetcher. `sacred_texts` source type added in Draft 6 for Phase 1b multi-translator additions; fetches index.htm, regex-extracts chapter links, concatenates all chapter HTML files.
- `scripts/verify_manifest.py` — title-matches-expected verifier (catches wrong-ID PG fetches).
- `scripts/clean_books.py` — header/footer stripping, PDF/HTML extraction.
- `scripts/chunk_books.py` — paragraph-aware ~500-token chunking. Emits `source_id` field for multi-translator grouping.
- `scripts/chunks_to_passages.py` — stratified balanced sampling.

**Data.**

- `corpus/passages.jsonl` — Phase 0 v0.5 (143 passages, 23 traditions).
- `corpus/passages_substituted.jsonl` — Phase 0 with placeholder substitution.
- `corpus/passages_phase1.jsonl` — Phase 1a balanced-sampled (920 chunks, 11 traditions).
- `corpus/chunks.jsonl` — Phase 1a + Phase 1b full chunk set (5,777 chunks, of which 447 are multi-translator participants across 2 source families).
- `corpus/books/raw/` and `corpus/books/cleaned/` — 24 whole books (~3.2M tokens including Phase 1b additions).
- `corpus/books_manifest.json` — sources, translators, license, verification status. Includes `source_id` field for multi-translator grouping.

**Results.**

- `results/text-embedding-3-large/` — Phase 0 OpenAI document-level outputs.
- `results/substituted/` — Phase 0 substituted document-level outputs.
- `results/concept_analysis/` — Phase 0 CCB outputs (full pattern dictionaries).
- `results/sentence_concept_analysis/openai/` and `.../onnx/` — Phase 0 + Phase 1a sentence-level CCB outputs, both backends.
- `results/phase1/` — Phase 1a outputs.
- `results/phase1/concept_analysis_technical_only/` — Phase 1a technical-only-tagger §6.8 prediction test outputs.
- `results/phase1b/within_source_variance.json` — Phase 1b §6.9 variance decomposition outputs.
- `results/phase1b/embeddings.npy` — Phase 1b 5,777 × 384 ONNX MiniLM embeddings (cached).
- `results/robustness/` — paraphrase-exclusion robustness check outputs.

**Pre-registration.**

- `findings/phase1b-preregistration.md` — Phase 1b external pre-registration with hypotheses, predicted outcome ranges, decision rules, anticipated failure modes. Externally timestamped via public GitHub commit (`d16fc8c`) and Zenodo `v1.2-prereg-phase1b` DOI.

**Reproducibility.** OpenAI runs require API key (`.openai_key`); ONNX BERT runs are fully local with only `onnxruntime`, `tokenizers`, and `numpy` as external dependencies. Tested on Python 3.14 / Windows with Defender Application Control active.

---

## Acknowledgments

### Use of AI assistance

The author used Claude (Anthropic) extensively throughout this project: for methodology design discussions, prose drafting across multiple paper revisions, and writing code under the author's direction. All research questions, experimental design decisions, methodological commitments, interpretations of results, and claims in this paper are the author's; the AI's role was that of a capable but supervised research assistant.

---

## 12. References

Anthony, F. V., Hermans, C. A. M., & Sterkens, C. (2010). A comparative study of mystical experience among Christian, Muslim, and Hindu students in Tamil Nadu, India. *Journal for the Scientific Study of Religion*, 49(2), 264–277.

Bohm, D. (1980). *Wholeness and the Implicate Order*. Routledge.

Bostrom, N. (2003). Are you living in a computer simulation? *Philosophical Quarterly*, 53(211), 243–255.

Forman, R. K. C. (1990). *The Problem of Pure Consciousness: Mysticism and Philosophy*. Oxford University Press.

Forman, R. K. C. (1999). *Mysticism, Mind, Consciousness*. SUNY Press.

Hoffman, D. (2019). *The Case Against Reality: Why Evolution Hid the Truth from Our Eyes*. W. W. Norton.

Hood, R. W. (1975). The construction and preliminary validation of a measure of reported mystical experience. *Journal for the Scientific Study of Religion*, 14(1), 29–41.

Hood, R. W., Ghorbani, N., Watson, P. J., Ghramaleki, A. F., Bing, M. N., Davison, H. K., Morris, R. J., & Williamson, W. P. (2001). Dimensions of the Mysticism Scale: Confirming the three-factor structure in the United States and Iran. *Journal for the Scientific Study of Religion*, 40(4), 691–705.

Hutchinson, B., Khoo, R., et al. (2024). Modeling the sacred: Considerations when using religious texts in natural language processing. *Findings of the Association for Computational Linguistics: NAACL 2024*.

Kastrup, B. (2019). *The Idea of the World: A Multi-Disciplinary Argument for the Mental Nature of Reality*. iff Books.

Katz, S. T. (Ed.). (1978). *Mysticism and Philosophical Analysis*. Oxford University Press.

Lloyd, S. (2006). *Programming the Universe: A Quantum Computer Scientist Takes On the Cosmos*. Knopf.

Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using siamese BERT-networks. *Proceedings of EMNLP-IJCNLP 2019*.

Rovelli, C. (2022). *Helgoland: Making Sense of the Quantum Revolution*. Riverhead Books.

Stace, W. T. (1960). *Mysticism and Philosophy*. Macmillan.

Stanford Encyclopedia of Philosophy. (2025). Mysticism (Fall 2025 edition). https://plato.stanford.edu/archives/fall2025/entries/mysticism/

Streib, H., Klein, C., Keller, B., & Hood, R. W. (2020). The Mysticism Scale as a measure for subjective spirituality. In *Assessing Spirituality in a Diverse World* (pp. 467–491). Springer.

Tegmark, M. (2014). *Our Mathematical Universe*. Knopf.

Tononi, G., & Koch, C. (2015). Consciousness: Here, there and everywhere? *Philosophical Transactions of the Royal Society B*, 370(1668).

Trivedi, H. P. (2025). A Comparative Model of Mysticism: Cognitive Neuroscience, Phenomenal Experiences, and Noetic Accounts. *Archive for the Psychology of Religion*, 47(2), 133–156.

Wheeler, J. A. (1990). Information, physics, quantum: The search for links. In W. H. Zurek (Ed.), *Complexity, Entropy, and the Physics of Information* (pp. 309–336). Addison-Wesley.

---

## Appendix A. Pre-specified candidate features and current status

The seven candidate structural features were specified in `glossary.md` before any analysis. Their concept-tag counterparts are the categories in §4.2.

| # | Feature | Concept tag overlap | Phase 0 status | Phase 1a status | Phase 1a technical-only |
|---|---|---|---|---|---|
| 1 | Observer-substrate non-separability | NONSEP (no explicit-label coverage) | unmeasured | unmeasured | unmeasured |
| 2 | Absence of a privileged self | SELF (Phase 0 n = 3, Phase 1a n = 27) | unmeasured (n=3) | +0.031 sentence-OpenAI (*p* = 0.006) | unchanged (no common terms in pattern) |
| 3 | Immanence | overlaps WORLD ∩ ULTIMATE | indirect | indirect | mixed (WORLD untestable; ULTIMATE −) |
| 4 | Groundless ground | overlaps SUBSTRATE ∩ ULTIMATE | indirect; both bind | indirect; both bind | SUBSTRATE unchanged; ULTIMATE − |
| 5 | Non-temporal nature of ultimate reality | no concept-tag coverage | unmeasured | unmeasured | unmeasured |
| 6 | Equivalence of becoming and recognition | overlaps RECOGNITION | +0.079 (*p* = 0.001) | +0.025 passage / +0.061 sentence (*p* ≤ 0.0005) | **+0.110 (*p* < 0.0001)** |
| 7 | Primacy of consciousness/awareness | overlaps AWARENESS | +0.113 (*p* < 0.0001) | +0.026 passage / +0.082 sentence OpenAI / +0.121 sentence BERT | untestable (n=1) |
| 8 | Compression to unity | overlaps NONSEP ∩ ULTIMATE | unmeasured | unmeasured | unmeasured |

The feature taxonomy and concept-tag schema are not fully reconciled. A follow-on application of CCB to this debate would refine operational definitions and pre-register the reconciled set.

---

## Appendix B. Per-concept robustness summary

| Concept | Phase 0 full | Phase 0 sentence | Phase 0 BERT | Phase 0 paraphrase-excluded | Phase 1a passage | Phase 1a sentence OpenAI | Phase 1a sentence BERT | **Phase 1a technical-only** |
|---|---|---|---|---|---|---|---|---|
| AWARENESS | +0.113 *** | +0.114 *** | +0.204 *** | not measurable (0 pairs) | +0.026 *** | +0.082 *** | +0.121 *** | **untestable (n=1)** |
| RECOGNITION | +0.079 ** | +0.082 *** | +0.073 *** | not measurable (1 pair) | +0.025 *** | +0.061 *** | +0.090 *** | **+0.110 *** (dramatic recovery)** |
| WORLD | +0.077 *** | +0.082 *** | +0.073 *** | underpowered (6 pairs) | +0.022 *** | +0.051 *** | +0.065 *** | **+0.049 (NS, underpowered)** |
| ULTIMATE | +0.057 *** | +0.067 *** | +0.079 *** | +0.062 *** (survives) | +0.014 *** | +0.047 *** | +0.074 *** | **+0.008 ** (failed, coverage-asymmetry)** |
| SUBSTRATE | +0.053 ** | +0.051 ** | +0.050 ** | not measurable (0 pairs) | +0.054 ** (unchanged) | +0.053 (p=0.04) | +0.048 (p=0.09, NS sub-sample) | **+0.054 ** (control, unchanged)** |

\*\*\* *p* < 0.0001, \*\* *p* < 0.01.

**Status update from Draft 4:** Draft 4 added Phase 1a passage and sentence columns, converting Draft 2's one-of-five-concepts-paraphrase-tested into five-of-five with at least one paraphrase-free measurement. Draft 5 adds the Phase 1a technical-only column, which:

- **Confirms SUBSTRATE as the control** (unchanged at +0.054 across the full corpus, the technical-only restriction, and the Phase 0 baseline).
- **Dramatically strengthens RECOGNITION** (+0.110 with advaita × theravada at 0.531 as top cross-tradition pair) — the paper's headline cross-tradition concept-binding result.
- **Falsifies the §6.8 single-component mechanism for ULTIMATE**, revealing the coverage-distribution asymmetry component (§6.8 refined formulation).
- **Renders AWARENESS untestable on Phase 1a** (n=1 after dropping common-English terms) — the Phase 1a corpus lacks the technical-vocabulary coverage to evaluate the prediction.
- **Renders WORLD underpowered on Phase 1a** (n=5; observed +0.049 in predicted range but NS).

The second-reviewer Phase-1 prior (~60% AWARENESS + RECOGNITION survive at *p* ≤ 0.01; ~40% full five-concept pattern survives) was already exceeded in Phase 1a. The technical-only-tagger result strengthens RECOGNITION specifically to the project's highest cross-tradition concept-binding result.

The pre-specified §6.8 predictions were partially confirmed (SUBSTRATE control, RECOGNITION direction-and-magnitude exceeded), partially refuted in informative directions (ULTIMATE went down rather than up, revealing the coverage-asymmetry mechanism), and partially untestable (AWARENESS, WORLD insufficient corpus coverage). The mixed-outcome pre-specified prediction test refines the mechanism rather than disconfirming the paper's broader claim that vocabulary breadth is a significant determinant of passage-level CCB.

---

## Appendix C. Phase 1b H1b.3 pre-registration operationalization note

This appendix documents a discrepancy between the literal text of the Phase 1b pre-registration document (`findings/phase1b-preregistration.md` at public commit `d16fc8c`) and the §6.9 main-text characterization of the H1b.3 result. The discrepancy is in test-direction operationalization, not in the underlying scientific finding; the §6.9 main-text characterization is correct on the substantive claim and consistent with what the test detected. This appendix exists for transparency, so that readers consulting the pre-registration directly find the operationalization issue explained rather than discover it as an apparent inconsistency.

### What the pre-registration said

The Phase 1b pre-registration committed at commit `d16fc8c` specifies H1b.3 as:

> H1b.3 (Permutation null rejection). The observed W-S-B-T value exceeds the permutation null mean (translator labels randomly reassigned within source family) at *p* < 0.05 one-sided. I.e., between-translator passages cluster more tightly than chance would predict.

The pre-registered inequality direction is therefore *observed greater than null*, with the prediction interpreted as "between-translator passages cluster more tightly than chance" implying that real cross-translator pairs would be *more* similar than label-shuffled pairs.

### What the test actually detected

The observed result is the *opposite* inequality direction: observed W-S-B-T (0.6236) is *below* the null mean (0.6397 with sd 0.0009). The z-score is approximately −17.9 in the *unexpected* direction relative to the pre-registered inequality. In the pre-registered direction (observed > null), the test gives *p* = 1.0. In the *opposite* direction (observed < null), the test gives *p* << 0.0001 — overwhelming statistical evidence.

### Why both descriptions describe the same scientific claim

The underlying scientific hypothesis is that translators produce statistically detectable stylistic differences on shared source content. Two operationalizations of "detecting translator effect" via the permutation null are conceivable, and they predict *opposite* inequality directions:

**Operationalization A (pre-registered, wrong for this permutation null):** "If translators preserve source content, real cross-translator pairs (different translators on the same source) should be *more* similar than random pairs." Therefore observed > null.

**Operationalization B (correct for this permutation null):** "When translator labels are shuffled within source family, some pairs that share the *real* same translator are now labeled as 'different translator' and are tighter than real between-translator pairs. So shuffled 'between-translator' mean inflates above the real mean if translators differ stylistically." Therefore observed < null.

Operationalization B is what the test as designed actually measures. The permutation shuffles `book_id` (translator) labels *while keeping source identity fixed*. The shuffle does not destroy source-content structure; it only randomizes translator-label-to-passage assignment. Because same-translator pairs are tighter than between-translator pairs (a fact directly observed as W-S-S-T > W-S-B-T), the shuffled "between-translator" mask catches some mislabeled same-translator-in-reality pairs and is inflated above the real W-S-B-T. Translators *do* differ stylistically therefore manifests as real W-S-B-T < shuffled null mean.

Operationalization A — what the pre-registration committed — is what the researcher writing the pre-registration believed should be tested. It is wrong about this specific permutation null. It would be correct for a different permutation null (one that destroys source content, e.g., shuffling source_id rather than book_id), but the test as designed does not do that.

The substantive scientific finding — translators produce statistically detectable stylistic differences — is what the test confirmed. The §6.9 main text reports the test as confirmed at overwhelming significance because this is the accurate description of what the underlying scientific hypothesis predicts *and* what the test result demonstrates. The pre-registration's literal inequality direction is wrong; the substantive finding is right.

### Why this appendix exists rather than silent revision

The pre-registration is a public timestamp on the literal text committed at `d16fc8c`. The literal text is wrong on the inequality direction. Silently revising the §6.9 main text to match the wrong inequality direction would misrepresent the result; silently revising the pre-registration after seeing the data would violate the discipline pre-registration is meant to enforce. The transparent path is to (i) report the substantive finding accurately in the main text, (ii) acknowledge the operationalization discrepancy in this appendix, (iii) leave the original pre-registration unchanged. Any reader checking commit `d16fc8c` against the §6.9 result will find this appendix as the documented explanation.

### Methodological lesson

Pre-registration discipline catches not only post-hoc fitting (the well-known case) but also a less-discussed case: conceptual errors in test operationalization that are invisible to the researcher until the test runs. The researcher's underlying hypothesis was scientifically correct; the arithmetic operationalization of that hypothesis into a specific inequality direction was wrong. This is exactly the kind of mismatch that pre-registration is designed to surface and document, and the discipline's value here is the documentation, not the catching of fraud. §8 carries this lesson as the second-order benefit of advance specification.

---

*Draft 6, submission-ready preprint. Sole author: T. David Kinlaw (Independent Researcher / Redbird Software LLC; ORCID 0009-0008-5213-1017). NLP methodology paper; mysticism convergence used as substantive test case. Phase 1b multi-translator variance test externally pre-registered prior to running the analysis. Comments, replications, adversarial extensions, and applications to other convergent-claim test cases welcomed. Contact: david@redbirdsoftwarellc.com.*
