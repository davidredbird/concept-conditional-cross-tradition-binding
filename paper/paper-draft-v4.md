# Concept-Conditional Cross-Tradition Binding in Semantic Embedding Space: A Method and an Application to Mysticism

**Preliminary preprint — Draft 4**
**Date:** 2026-05-15
**Status:** Exploratory; not yet pre-registered. Methodology paper with mysticism convergence as test case. Findings reported as a proof-of-concept and an invitation to extend, replicate, or refute.

**Changes from Draft 3:** Reframes the contribution from "first empirical test of the mysticism convergence claim" to "concept-conditional cross-tradition binding as an NLP method, stress-tested on the mysticism convergence debate as a substantive application." Title leads with the method. Abstract and §1 lead with the methodological contribution; the mysticism debate is the test case, not the thesis. §2 reorganized so NLP / computational humanities is the field positioning and the philosophical debate is the application domain. §7 sharpens what is and is not claimed about the application. All empirical content unchanged from Draft 3; framing adjusted throughout.

---

## Abstract

We introduce **concept-conditional cross-tradition binding (CCB)**, an embedding-based statistic for testing whether textual passages from unconnected source traditions are more similar when conditioned on shared structural concepts than when not. The statistic is designed to be (i) *bias-aware* — it avoids the shared-placeholder similarity artifact that affects naive vocabulary-substitution tests; (ii) *tractable at scale* — vectorized permutation tests over n×n boolean masks make it usable at >10⁴ sentences; (iii) *cross-model replicable* — applied uniformly to proprietary OpenAI `text-embedding-3-large` (3072-dim) and open-source `sentence-transformers/all-MiniLM-L6-v2` (384-dim BERT) via ONNX Runtime, the latter usable on workstations with Application-Control policies that block torch; and (iv) *cross-granularity stable* — defined identically at passage and sentence levels with mechanistically explained differences between them.

We stress-test the method on the 65-year-old cross-cultural mysticism convergence debate (Stace, 1960; Katz, 1978; Forman, 1990; Hood, 1975). This debate is methodologically apt for our purposes because its central question — whether contemplatives from unconnected traditions converge on shared structural descriptions of reality — is textual in form yet has resisted direct textual empirical test for six decades, while modern semantic-embedding tools were maturing.

We apply CCB to two corpora. Phase 0 is a 143-passage curated corpus across 23 traditions, 68% investigator-authored paraphrase, designed for fast iteration. Phase 1a replaces paraphrases with verified primary-source published English translations, sampled from a 20-book / ~2.85M-token / 14,173-sentence whole-book base set, 100% non-paraphrase, 11 traditions.

**Across both corpora, five of seven pre-registered structural concepts (AWARENESS, RECOGNITION, WORLD, ULTIMATE, SUBSTRATE) show statistically significant cross-tradition binding at *p* ≤ 0.0015.** The same five bind across passage and sentence granularity and across both embedding models. Top tradition pairs replicate cross-model.

A methodological finding: effect sizes deflate 3–4× from Phase 0 to Phase 1a at passage granularity but only 25–30% at sentence granularity, and not at all for SUBSTRATE at either granularity. We show this differential deflation is mechanistically explained by **vocabulary breadth in the concept-tag dictionaries**: dictionaries containing common English terms (`consciousness`, `God`, `world`) fire on passages that *mention* the term in non-technical context; technical-only dictionaries (`emptiness`, `śūnyatā`, `implicate order`, `holographic`, `integrated information`) do not. The casual-usage noise floor at passage granularity dilutes binding for broad-vocabulary concepts; sentence-level filtering or technical-only-vocabulary variants recover the signal. We state predictions for the technical-only-tagging follow-on in §6.8.

We make no claim about whether the perennialist position in the mysticism debate is correct. We claim that **a class of evidence both sides of the debate have to engage with on the merits is now produceable**, and we have produced an example. The method is concept-agnostic and corpus-agnostic; the field can extend or refute the present application by running it on different corpora, different concept dictionaries, different embedding models, or different convergent-claim test cases (Golden Rule, Hero's Journey, mystical death-and-rebirth, eternal recurrence). Multi-translator inclusion, non-English source analysis with multilingual embeddings, adversarial passage selection, and held-out human-validated concept tagging remain unaddressed (§9) and define what a fuller follow-on application requires.

Code, both corpora, and complete result tables released under MIT.

---

## 1. Introduction

### 1.1 What the paper proposes

Cross-cultural convergence claims about textual content — claims that authors from unconnected traditions write structurally similar things about reality, mind, perception, or value — are common in religious studies, comparative philosophy, mythology, and elsewhere. They have historically been argued qualitatively. Quantitative tests have been hard to construct: document-level embedding similarity is dominated by register and vocabulary; vocabulary substitution introduces its own biases; and most NLP work on culturally varied corpora has focused on translation or intra-tradition stylometry rather than cross-tradition structural comparison (Hutchinson et al., 2024).

We propose **concept-conditional cross-tradition binding (CCB)**, an embedding-based statistic that operationalizes a sharper version of the convergence claim: *not* "everything converges" but "specific structural axes bind specific traditions when those traditions are discussing those axes." Concretely, for each pre-registered structural concept *C* and each cross-tradition pair of passages, we compare the mean similarity of pairs where both passages mention *C* to the mean similarity of pairs where only one passage mentions *C*. The difference is the *binding* of *C*. A permutation null over concept-tag assignments produces a *p*-value.

The statistic is designed to avoid the failure modes that have made document-level cross-tradition comparison uninformative:

- **Vocabulary substitution failure mode.** Replacing tradition-specific terms with shared placeholders forces token-level similarity across substituted texts, biasing toward apparent convergence. CCB does not substitute; it conditions on mentions.
- **Register / style failure mode.** Document-level similarity is dominated by author register, sentence structure, citation style, and other features that overwhelm content-level convergence. CCB compares passages that all carry the same concept-tag marker, controlling for the *kind* of content being compared.
- **Vocabulary breadth as noise floor.** Pattern dictionaries containing common English terms fire on passages that mention the term casually, diluting passage-level binding. The paper documents this empirically (§6.7-6.8) and characterizes the conditions under which the failure occurs.

### 1.2 The mysticism convergence debate as test case

The cross-cultural convergence claim has its sharpest qualitative articulation in the philosophy of mysticism, where Stace (1960), Forman (1990), and others argue that contemplatives from unconnected traditions report a shared structural description of reality (non-separation of observer and observed; absence of a privileged self; primacy of awareness; unity beneath multiplicity), while Katz (1978) and the "hard constructivist" tradition argue that every report is conceptually mediated and apparent convergence is hermeneutic projection. The debate has run for sixty-five years on largely textual and philosophical grounds. Empirical work (Hood, 1975; Hood et al., 2001; Anthony et al., 2010; Streib et al., 2020) has tested *contemporary self-reports* via survey instruments (the Mysticism Scale and its descendants) and found cross-cultural similarity, but has not tested whether the *historical texts* produced by unconnected contemplatives converge in semantic structure. A direct textual test with controls adequate to the constructivist critique has not appeared (Hutchinson et al., 2024 confirms the gap in NLP-on-religious-texts).

This is an apt test case for CCB for three reasons:

1. The convergence claim is *about textual content*, so a textual test is methodologically on-domain rather than being a proxy.
2. The two sides of the debate make sharp predictions that diverge on observable text properties: perennialists predict cross-tradition signal beyond shared vocabulary and register; constructivists predict that any signal will be vocabulary, register, or translator-mediated and will disappear under appropriate controls.
3. The debate has resisted decades of qualitative argument, so even partial empirical leverage is interesting.

### 1.3 What the paper does *not* claim about the application

Nothing in this analysis bears on whether any measured convergence reflects:

(a) a shared truth about the structure of reality;
(b) a shared feature of human cognition under trained introspection;
(c) a shared feature of how literate contemplative cultures end up writing about introspection, independent of what they observe;
(d) a shared feature of how the small set of anglophone scholar-translators who produced our English source texts render contemplative content.

Distinguishing (a)–(d) is downstream of the empirical question the method answers, which is the prior question *"is there any cross-tradition textual signal beyond what shared vocabulary, register, and translator conventions can explain?"* Our affirmative answer to that question, restricted to five specific pre-registered concepts, is necessary but not sufficient for any of (a)–(d), and we make no progress toward (a)–(d) here.

We will not claim that the perennialist thesis has been settled. We will not claim that the constructivist critique has been refuted; the present results show that vocabulary and register do substantial work in apparent document-level convergence, which is what constructivists predicted. We will claim only that **a method exists for producing evidence the field can engage with on the merits, that we have applied it carefully, and that the result is informative regardless of which interpretation it supports.** We are not the field; we are presenting what we found from a methodologically-defined position. The field is welcome to follow up.

### 1.4 Contributions

1. **CCB**, a bias-aware concept-conditional cross-tradition binding statistic with vectorized permutation testing.
2. **Cross-model replication architecture** that runs identically against proprietary and open-source embedding stacks, including ONNX-based local inference for environments where torch is blocked.
3. **Vocabulary-breadth-as-noise-floor mechanism** characterizing when passage-level concept tagging dilutes binding signal and when sentence-level filtering recovers it (§6.8).
4. **A two-corpus stress test** of the method on the mysticism convergence debate: a paraphrase-heavy fast-iteration corpus and a verified-primary-source whole-book corpus, with shared methodology and divergent paraphrase profiles. Five of seven pre-registered concepts bind in both.
5. **Open-source release of code, corpora, manifests, and results** for independent replication, extension, and adversarial reuse.

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
- **Comparative-model recent work.** Trivedi (2025) proposes a tripartite comparative model of mysticism (neurocognitive substrates / phenomenal experiences / noetic accounts) that maps onto pre-registered structural features of the kind CCB tests.

The Stanford Encyclopedia of Philosophy entry on Mysticism (2025) characterizes the present state of the debate as unresolved on philosophical grounds; the survey lists no computational, NLP, or embedding-based methods applied to mystical literature.

We do not engage the philosophical debate at the depth that a primary contribution to it would require. We engage it at the depth required to *use it as a substantive test case* for the method we propose.

### 2.3 Bridge thinkers in the application domain

A modern subliterature of authors explicitly compares structurally nondual claims in modern scientific frameworks to historical contemplative claims: Bohm's *Wholeness and the Implicate Order* (1980), Rovelli's *Helgoland* (2022) (which argues relational quantum mechanics and Nagarjuna's emptiness doctrine make structurally identical claims), Kastrup (2019) on analytic idealism, Tononi and Koch (2015) on consciousness as fundamental in IIT, Hoffman (2019) on perception as interface, Tegmark (2014), Bostrom (2003), and others.

In the Phase 0 corpus, these authors are represented by paraphrases; in the Phase 1a corpus they are absent (their books are not on Project Gutenberg and were not added in Phase 1a). We treat them in this paper as a methodological cautionary tale (§6.5) rather than a substantive contribution to the cross-period convergence question. Restoring them on verified non-paraphrase text via arxiv and fair-use research excerpts is a natural extension (§10) but is not part of the present paper.

**Important caveat for the Rovelli result.** Rovelli's *Helgoland* is in the Phase 0 corpus and argues toward the Mahayana–relational-QM correspondence that our SUBSTRATE-binding analysis quantitatively recovers (§6.1). The 0.455 binding establishes that an embedding model can detect the correspondence Rovelli argued for, given the text in which he argued for it. It does not independently establish the structural identity. Following the second-reviewer pass on Draft 2, we **demote this result from the abstract to a methodological-validation footnote** and promote the methodologically cleaner Mahayana × Theravada AWARENESS binding (§6.1) — where neither tradition wrote toward the comparison — as the canonical cross-tradition finding.

---

## 3. The two test corpora

We use two corpora as test cases for the method. They differ in paraphrase profile (the load-bearing concern from the Draft 2 review) but use the same statistical pipeline.

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

### 3.3 Corpus selection is a method *parameter*, not the method itself

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

The seven pre-registered structural concepts — ULTIMATE, SUBSTRATE, AWARENESS, WORLD, SELF, RECOGNITION, NONSEP — are tagged on each passage by a manually curated dictionary of case-insensitive regex patterns. The patterns are listed in full in `scripts/concept_analysis.py` and derived from a pre-registered glossary listing tradition-specific terminology for each concept (e.g., AWARENESS includes `consciousness`, `awareness`, `rigpa`, `chit`, `phi`, `nous`; SUBSTRATE includes `emptiness`, `śūnyatā`, `implicate order`, `holographic`, `integrated information`).

The same patterns are applied to both Phase 0 and Phase 1a corpora. Differences in binding strength between phases reflect either (i) genuine differences between paraphrase-style and published-translation text, (ii) differences in casual-vs-technical use of the same vocabulary at scale, or (iii) noise.

**Regex tagging is a hidden degree of freedom** that we name prominently. The same investigator built the glossary, the corpus, and the patterns. A pattern set chosen by someone with a different theoretical model of nondualism would tag different passages and could produce different binding scores. CCB is **bias-free of the shared-placeholder substitution artifact** (the artifact it was designed to eliminate), not **bias-free in the absolute sense**. Held-out human-validated tagging on a randomly sampled subset is a follow-on extension (§10).

### 4.3 The CCB statistic

For each pre-registered concept *C*, restricted to cross-tradition passage pairs only:

$$
\text{CCB}(C) = \overline{\text{sim}}\bigl(\text{pairs where both passages mention } C\bigr) - \overline{\text{sim}}\bigl(\text{pairs where exactly one mentions } C\bigr)
$$

The contrast against "exactly one mentions C" rather than "neither mentions C" controls for the possibility that concept-mentioning passages are systematically more similar to each other than non-concept-mentioning passages for reasons unrelated to *C* (e.g., the concept-mentioning passages are longer or more elaborated).

Significance is assessed by a permutation test: concept-tag assignments are shuffled across passages (preserving the total count of tagged passages), the statistic is recomputed, and 2,000 such permutations build the null distribution. The *p*-value is the fraction of permutations with statistic ≥ observed.

For sentence-level analysis, passages are split on punctuation, the same regex tagger is applied per sentence, and CCB is computed across sentences rather than passages. At Phase 1a sentence scale (14,173 sentences), the Python-iterator implementation used in earlier drafts is intractable (≈12.5M pairs per permutation × 2,000 perms × 7 concepts). We vectorize via numpy boolean masks (`scripts/sentence_binding_vectorized.py`): each permutation becomes O(n²) numpy operations rather than O(n²) Python iterations, reducing runtime from infeasible to seconds per concept.

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

Five of seven pre-registered concepts bind significantly. Effect sizes are substantial in cosine terms (≈ +0.05 to +0.11, on a base cross-tradition similarity of ≈ 0.30).

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

The modern wing dominates by volume, but **Mahayana × Theravada at 0.518 is the cleanest cross-tradition AWARENESS binding**: two Buddhist traditions on opposite sides of the doctrinal nondual/dualistic divide, neither writing toward the comparison, both discussing consciousness, converge tightly when conditioned on that discussion. The Phase 0 paper Draft 2 highlighted Rovelli's Mahayana × relational_qm SUBSTRATE binding; we promote Mahayana × Theravada AWARENESS to the canonical position because Rovelli wrote his text toward the comparison and the embedding model is detecting that targeting (see §2.3 caveat).

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

**Sentence-level deflation is much milder: 25–30% rather than 3–4×.** §6.8 explains the mechanism.

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

### 6.8 Vocabulary breadth as noise floor (the paper's primary methodological finding)

The passage-level Phase 0 → Phase 1a deflation pattern is striking: every binding concept lost 3–4× of its effect size except SUBSTRATE, which lost nothing. The sentence-level pattern is different: every concept retained 70–75% of its effect size, SUBSTRATE included.

The mechanical explanation: **passage-level concept tagging fires when the pattern appears anywhere in the passage, even when the rest of the passage is about something else.** Pattern dictionaries for AWARENESS, ULTIMATE, and WORLD include common English terms (`consciousness`, `awareness`, `God`, `the divine`, `world`, `the universe`, `cosmos`) that appear frequently in published philosophical and theological prose in non-technical context. Phase 0 paraphrases were investigator-curated to use these terms only when discussing the concept technically; Phase 1a published prose uses them everywhere. Passage-level binding therefore averages over a mix of passages-actually-about-the-concept and passages-merely-containing-the-pattern, diluting the effect.

Sentence-level analysis filters to sentences that actually contain the concept pattern. The dilution disappears; deflation drops to 25–30%.

**SUBSTRATE's pattern dictionary contains no common English terms.** The full SUBSTRATE pattern list:

> `emptiness`, `śūnyatā` (with Unicode `ś`), `svabhāva`, `the implicate order`, `implicate order`, `the holomovement`, `holomovement`, `the holographic principle`, `holographic`, `dependent origination`, `dependently arisen`, `basic space`, `integrated information`, `noumenon`, `noumena`, `thing-in-itself`, `the quantum vacuum`.

None of these appear in casual usage. A Phase 1a passage tagged for SUBSTRATE almost certainly is engaging the concept technically. Passage-level dilution does not affect SUBSTRATE.

**This is the paper's primary methodological finding.** For NLP practitioners running concept-conditional analyses on real-text corpora, the result is: pattern-dictionary vocabulary breadth determines passage-level signal-to-noise. Technical-only vocabularies give clean signal at any granularity; broad-vocabulary concept tags require sentence-level granularity or technical-only variants to recover signal that passage-level tagging dilutes.

**Predictions written before testing the technical-only-tagger variant**, deliverable in a follow-on analysis:

If we restrict AWARENESS, ULTIMATE, WORLD tagging to *technical-only* vocabulary (drop `consciousness`/`awareness`, `God`/`the divine`, `world`/`the universe`; keep `rigpa`/`chit`/`citta`/`nous`/`phi`; `Brahman`/`Tao`/`Ein Sof`; `samsara`/`the ten thousand things`):

| Concept | Phase 1a passage-level current | Prediction (technical-only) |
|---|---|---|
| AWARENESS | +0.026 | +0.08 to +0.11 (recovers toward Phase 0 levels) |
| ULTIMATE | +0.014 | +0.04 to +0.06 (partial recovery) |
| WORLD | +0.022 | +0.06 to +0.08 (substantial recovery) |
| RECOGNITION | +0.025 | +0.03 to +0.05 (already mostly technical, small recovery) |
| SUBSTRATE | +0.054 | +0.054 (unchanged — no casual terms to drop) |

If predictions hold, the apparent Phase 1a deflation is largely vocabulary-breadth noise floor and the structural cross-tradition convergence is recoverable from Phase 1a data with better tagging. If predictions fail — particularly if AWARENESS does not recover even when restricted to technical terms — there is some additional explanation for the deflation we have not identified.

We have written the predictions before running, so the result, whichever way it falls, is a clean confirmation or refutation of the mechanism rather than post-hoc rationalization.

---

## 7. Discussion

### 7.1 What we have shown

**A methodological contribution.** CCB is a bias-aware embedding-based statistic that produces interpretable cross-tradition convergence scores conditional on shared concept-tags, replicates across two unrelated embedding stacks, and remains tractable at multi-thousand-sentence scale via vectorized permutation testing. Pattern-dictionary vocabulary breadth determines passage-level signal-to-noise; the paper provides a worked example and pre-registered predictions for the recovery analysis.

**An application's result.** Applied to the mysticism convergence debate across two corpora (paraphrase-heavy Phase 0 and verified-primary-source Phase 1a), CCB returns: five of seven pre-registered structural concepts show statistically significant cross-tradition binding at *p* ≤ 0.0015 in both corpora; effect sizes are smaller than Phase 0 suggested but the qualitative result is robust to corpus revision, embedding model, and granularity.

**The cleanest single concept-binding result** is **Mahayana × Theravada AWARENESS at 0.518**, replicated cross-model — two Buddhist traditions across the doctrinal nondual/dualistic divide, neither writing toward the comparison, converging on consciousness-talk.

**The classical Stace–Forman RECOGNITION signal** across historical contemplative traditions (Advaita ↔ Dzogchen ↔ Sufi ↔ Daoism ↔ Neoplatonism, no historical contact) is the closest quantitative correlate of what the perennialist tradition has argued for qualitatively for six decades. CCB detects it in both corpora.

### 7.2 What we have *not* shown about the application

We have not shown the perennialist position is correct.

We have not shown the constructivist position is incorrect. In fact, the present results show that vocabulary and register do substantial work in apparent document-level convergence, which is what constructivists predicted.

We have not addressed the translator-as-confound (§5). Every result here is consistent both with structural convergence in source content and with shared anglophone-scholar-translator conventions. Multi-translator inclusion and non-English source analysis are necessary to distinguish them.

We have not independently established the Rovelli–Nagarjuna SUBSTRATE correspondence; the binding confirms the embedding can detect what Rovelli wrote toward (§2.3).

We have not tested the bridge-thinker → historical-nondual cross-period convergence on verified non-paraphrase text; the Phase 1a corpus lacks the modern wing.

We have not pre-registered. Pre-registered concept categories were specified before analyses, but corpus composition, statistical tests, and decision rules were not committed to OSF before running.

### 7.3 The defensible decomposition of "what we measured"

The honest picture decomposes apparent cross-tradition similarity into:

1. **Concept-level structural binding** on five pre-registered axes, detectable at *p* ≤ 0.0015, replicated cross-model, cross-granularity, and across paraphrase-heavy and whole-book non-paraphrase corpora.
2. **Document-level vocabulary effect**, partially closed by substitution (~15–30% of the modern–historical gap, upper-bounded by the shared-placeholder bias).
3. **Document-level register / style effect** (~50–70% of the modern–historical gap), not closed by current methods.
4. **Translator-tradition effect** (unbounded in either Phase 0 or Phase 1a; likely material).
5. **Paraphrase-author effect** (bounded by Phase 1a; ~2× inflation at document level Phase 0 → Phase 1a; mostly vocabulary-breadth noise floor at passage-level for binding concepts).
6. **Genuine content difference** between modern computational and historical contemplative nondualism in Phase 0 (probably real and small).

(1) is the part of the picture that survives the controls Phase 0 + Phase 1a applied. (2)–(6) bound how strongly (1) should be cited; (4) is the largest unbounded component.

### 7.4 What the field can do with this

The method is concept-agnostic and corpus-agnostic.

**To extend the present application:** add multi-translator coverage, run on non-English source texts via multilingual embeddings, add modern computational sources on verified text, add adversarial-selection passages from a constructivist scholar, run held-out human-validated concept tagging, formally pre-register, run sparse-autoencoder probes for interpretable axes that survive vocabulary and register noise.

**To extend the method to other claimed convergent concepts:** the framework runs on any pre-registered concept dictionary on any multi-tradition corpus. Candidate test cases include the Golden Rule across ethical traditions, the Hero's Journey across mythologies (Campbell), non-attachment across contemplative practices, mystical death-and-rebirth across initiatic traditions, eternal recurrence (Stoic-Nietzschean-Hindu-cosmological), the great chain of being (Neoplatonic-Hindu-Western-medieval). The deliverable from running CCB on a suite of candidates is a meta-table — for each tested concept, was convergence detected, with what controls, what survived — which is what would move the comparative-convergence debate forward as a field, not a single positive result.

We are not the field. We are NLP practitioners who built a method and applied it to a contested philosophical question because the question was textually apt and unaddressed by prior methods. What the present results mean for the perennialist–constructivist debate is for the field that runs the methodology forward. We have produced an instrument; we have not delivered a verdict.

---

## 8. Methodological lessons from the application

For other researchers applying CCB to a new convergence claim:

- **Sentence-level granularity should be the default.** Passage-level introduces a casual-usage noise floor that disproportionately affects concepts whose pattern dictionaries include common English terms. Technical-only-vocabulary concepts are immune; broad-vocabulary concepts dilute at passage-level (§6.8).
- **Vocabulary breadth matters for tagging.** Concepts with technical-only pattern dictionaries have higher signal-to-noise than those with broad dictionaries. Tagger design should either split concepts into technical-only and broad-vocabulary variants, or require multiple pattern hits per passage rather than one.
- **Cross-model replication is cheap and should be default.** Run against both a proprietary embedding model and an open-source one. The OpenAI run costs dollars per multi-thousand-passage analysis; the ONNX BERT run is free and works on workstations with restrictive application-control policies.
- **Shared-placeholder vocabulary substitution introduces a tautological similarity bias.** If substitution is used at all, prefer per-tradition placeholders or mask-and-compare. Empirically the bias is smaller at whole-book scale than at short-passage scale but is always present.
- **Paraphrase content inflates document-level effects ~2× relative to verified-translation content.** Curated paraphrases are useful for fast methodology iteration but should not be the canonical evaluation corpus.
- **PG-ID verification is necessary before fetching at scale.** 10 of 24 initial Project Gutenberg IDs in our Phase 1a manifest returned unrelated books. The `scripts/verify_manifest.py` title-match check is the cheap defense.
- **Regex-based concept tagging is reproducible and pre-specifiable but is a hidden degree of freedom.** Held-out human-validated tagging on a randomly sampled subset is the cheap defense.
- **Effect sizes deflate honestly when paraphrases are removed.** The Phase 1a result is smaller than Phase 0 suggested; future preliminary work should use a verified-translation corpus from the start or report paraphrase-share alongside effect sizes.

---

## 9. Limitations

1. **Translator-as-confound** (§5). All passages English-translated by a small set of anglophone scholar-translators. The largest single unaddressed threat to validity in the present application.
2. **Selection bias.** Investigator chose the corpora informed by secondary scholarship; adversarial-inclusion process not performed.
3. **Regex tagging is a hidden degree of freedom** (§4.2). Patterns derive from a glossary the investigator built. CCB is bias-free of the shared-placeholder artifact, not bias-free absolutely.
4. **Phase 1a is single-translator per source.** Within-source translator variance is unestimated.
5. **Phase 1a lacks modern computational sources.** H1' (modern + historical) is currently tested only on Phase 0 paraphrases.
6. **English only.** Non-English source analysis is the deepest defense against translator-as-confound and is not yet attempted.
7. **Rovelli's relational-QM text writes toward the Mahayana correspondence** (§2.3, §6.1). The SUBSTRATE binding does not independently establish the structural identity.
8. **No formal pre-registration.** Concept categories were pre-specified; corpus, tests, decision rules were not OSF-registered.
9. **Naive sentence splitting.** Punctuation-regex, adequate for short well-formed passages, unaudited for longer-text edge cases.
10. **Permutation-test vectorization is mathematically equivalent to the Python iterator but is a separate code path** for tractability at Phase 1a sentence scale.
11. **No interpretability layer.** CCB establishes that concepts bind traditions; it does not characterize *what structural feature* the binding measures beyond the regex patterns used to detect it. Sparse-autoencoder probes and contrastive direction analysis are extensions.
12. **No adversarial controls.** LM-generated synthetic mystical writing in the style of each tradition is the natural adversarial test; not run.
13. **Stratified sentence sampling** for Phase 1a sentence-level analysis: subsamples to 4,000 sentences per analysis seed. Bindings stable to seed within ±0.005, but rare-concept n drops sharply under sampling.

---

## 10. How a fuller application of CCB to the mysticism debate would proceed

If a follow-on researcher were to extend the present application to a paper that the comparative-religion field could engage with on its strongest terms, the priority order is:

1. **Multi-translator inclusion** + within-source translator-variance baseline. Tao Te Ching across Legge, Mitchell, Lau, Ames-Hall, Watson, Henricks, Red Pine; Bhagavad Gita across Easwaran, Mitchell, Miller, Sargeant, Arnold, Edgerton; Heart Sutra across Conze, Red Pine, Tanahashi; Upanishads across Paramananda, Müller, Olivelle, Easwaran.
2. **Non-English source analysis** with multilingual embeddings (LaBSE, multilingual-e5, paraphrase-multilingual-MiniLM-L12-v2) on Sanskrit, Pali, Tibetan, Greek, Chinese, Arabic, Hebrew originals where available. **The deepest defense against translator-as-confound.**
3. **Modern computational and bridge thinkers restored on verified text** via arxiv (Bostrom simulation argument; Wheeler "Information, Physics, Quantum"; Tegmark MUH; Rovelli relational QM; Friston FEP; Tononi IIT; Hoffman interface theory) and fair-use research excerpts (Kastrup, Bohm).
4. **Adversarial passage selection** by a constructivist-leaning scholar independently selecting *least-nondual* passages from the same authors. Re-run on union and difference.
5. **Held-out human-validated concept tagging** on a randomly sampled corpus subset. Inter-rater agreement reported; binding re-estimated on human-tagged subset.
6. **OSF pre-registration** of corpus, pipeline, tests, decision rules, and predicted outcome priors before running.
7. **Technical-only-vocabulary tagger variants** (§6.8 predictions) on Phase 1a as a cheap diagnostic.
8. **Sparse-autoencoder probes** for interpretable structural axes that survive vocabulary and register noise.
9. **Adversarial synthetic-text controls** generated by language models.

We list this here so the present paper does not need to commit to delivering it. We have built the instrument; we present what it found in two test-corpus iterations; whoever extends it gets the priority list as a starting point.

---

## 11. Code and data availability

All code, corpora, results, methodology notes, and revision history are MIT-licensed and version-controlled.

**Analysis pipelines.**

- `scripts/concept_analysis.py` — concept-conditional binding at passage level.
- `scripts/sentence_concept_analysis.py` — sentence-level CCB with OpenAI and ONNX BERT backends.
- `scripts/sentence_binding_vectorized.py` — vectorized numpy implementation for *n* > 5,000 sentence corpora.
- `scripts/onnx_embedder.py` — local BERT-class inference via ONNX Runtime; usable on WDAC-restricted Windows.
- `scripts/prototype.py` — document-level embedding, clustering, visualization.
- `scripts/substitute.py` — structural-role vocabulary substitution with documented bias.
- `scripts/robustness_paraphrase.py` — paraphrase-exclusion robustness check.

**Phase 1a corpus pipeline.**

- `scripts/fetch_books.py` — Gutenberg / arxiv / web fetcher.
- `scripts/verify_manifest.py` — title-matches-expected verifier (catches wrong-ID PG fetches).
- `scripts/clean_books.py` — header/footer stripping, PDF/HTML extraction.
- `scripts/chunk_books.py` — paragraph-aware ~500-token chunking.
- `scripts/chunks_to_passages.py` — stratified balanced sampling.

**Data.**

- `corpus/passages.jsonl` — Phase 0 v0.5 (143 passages, 23 traditions).
- `corpus/passages_substituted.jsonl` — Phase 0 with placeholder substitution.
- `corpus/passages_phase1.jsonl` — Phase 1a balanced-sampled (920 chunks, 11 traditions).
- `corpus/chunks.jsonl` — Phase 1a full chunk set (5,408 chunks).
- `corpus/books/raw/` and `corpus/books/cleaned/` — 20 whole books (~2.85M tokens).
- `corpus/books_manifest.json` — sources, translators, license, verification status.

**Results.**

- `results/text-embedding-3-large/` — Phase 0 OpenAI document-level outputs.
- `results/substituted/` — Phase 0 substituted document-level outputs.
- `results/concept_analysis/` — Phase 0 CCB outputs.
- `results/sentence_concept_analysis/openai/` and `.../onnx/` — Phase 0 + Phase 1a sentence-level CCB outputs, both backends.
- `results/phase1/` — Phase 1a outputs.
- `results/robustness/` — paraphrase-exclusion robustness check outputs.

**Reproducibility.** OpenAI runs require API key (`.openai_key`); ONNX BERT runs are fully local with only `onnxruntime`, `tokenizers`, and `numpy` as external dependencies. Tested on Python 3.14 / Windows with Defender Application Control active.

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

## Appendix A. Pre-registered candidate features and current status

The seven candidate structural features were specified in `glossary.md` before any analysis. Their concept-tag counterparts are the categories in §4.2.

| # | Feature | Concept tag overlap | Phase 0 status | Phase 1a status |
|---|---|---|---|---|
| 1 | Observer-substrate non-separability | NONSEP (no explicit-label coverage) | unmeasured | unmeasured |
| 2 | Absence of a privileged self | SELF (Phase 0 n = 3, Phase 1a n = 27) | unmeasured (n=3) | **+0.031 sentence-OpenAI (*p* = 0.006)** |
| 3 | Immanence | overlaps WORLD ∩ ULTIMATE | indirect; not directly tested | indirect |
| 4 | Groundless ground | overlaps SUBSTRATE ∩ ULTIMATE | indirect; both bind | indirect; both bind |
| 5 | Non-temporal nature of ultimate reality | no concept-tag coverage | unmeasured | unmeasured |
| 6 | Equivalence of becoming and recognition | overlaps RECOGNITION | +0.079 (*p* = 0.001) | +0.025 passage / +0.061 sentence (*p* ≤ 0.0005) |
| 7 | Primacy of consciousness/awareness | overlaps AWARENESS | +0.113 (*p* < 0.0001) | +0.026 passage / +0.082 sentence OpenAI / +0.121 sentence BERT |
| 8 | Compression to unity | overlaps NONSEP ∩ ULTIMATE | unmeasured | unmeasured |

The feature taxonomy and concept-tag schema are not fully reconciled. A follow-on application of CCB to this debate would refine operational definitions and pre-register the reconciled set.

---

## Appendix B. Per-concept robustness summary

| Concept | Phase 0 full | Phase 0 sentence | Phase 0 BERT | Phase 0 paraphrase-excluded | **Phase 1a passage** | **Phase 1a sentence OpenAI** | **Phase 1a sentence BERT** |
|---|---|---|---|---|---|---|---|
| AWARENESS | +0.113 *** | +0.114 *** | +0.204 *** | not measurable (0 pairs) | +0.026 *** (p=5e-4) | **+0.082 *** | **+0.121 *** |
| RECOGNITION | +0.079 ** | +0.082 *** | +0.073 *** | not measurable (1 pair) | +0.025 *** (p=5e-4) | +0.061 *** | +0.090 *** |
| WORLD | +0.077 *** | +0.082 *** | +0.073 *** | underpowered (6 pairs) | +0.022 *** | +0.051 *** | +0.065 *** |
| ULTIMATE | +0.057 *** | +0.067 *** | +0.079 *** | **+0.062 *** (survives)** | +0.014 *** | +0.047 *** | +0.074 *** |
| SUBSTRATE | +0.053 ** | +0.051 ** | +0.050 ** | not measurable (0 pairs) | **+0.054 ** (p=1.5e-3) — *unchanged*** | +0.053 (p=0.04) | +0.048 (p=0.09, NS sub-sample) |

\*\*\* *p* < 0.0001, \*\* *p* < 0.01.

**Where Draft 2 reported one of five concepts (ULTIMATE) with a complete robustness track, Draft 4 reports all five with at least one paraphrase-free measurement.** The second-reviewer Phase-1 prior (~60% AWARENESS+RECOGNITION survive at *p* ≤ 0.01; ~40% full five-concept pattern survives) is exceeded: all five survived. Effect sizes are smaller than Phase 0 suggested. The §7.3 decomposition places genuine concept-level structural binding as the smallest and best-controlled component of the apparent signal; we cite affirmatively without over-promoting.

---

*Draft 4, methodological reframing of Drafts 2 and 3. Single-author preprint by an NLP researcher; mysticism convergence used as substantive test case. Comments, replications, adversarial extensions, and applications to other convergent-claim test cases welcomed. Contact: david@redbirdsoftwarellc.com.*
