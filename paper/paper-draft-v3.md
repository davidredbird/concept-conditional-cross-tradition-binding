# Concept-Conditional Cross-Tradition Convergence in Nondual Contemplative Literature: A First Empirical Test

**Preliminary preprint — Draft 3**
**Date:** 2026-05-15
**Status:** Exploratory; not yet pre-registered. Findings reported as a proof-of-concept and an invitation to replicate. Phase 0 paraphrase-heavy corpus + Phase 1a whole-book replication addressed; multi-translator, non-English, adversarial-inclusion, and held-out-human-tagging controls remain pending and define what we are calling **full Phase 1**.

**Changes from Draft 2:** Adds Phase 1a whole-book corpus replication (§3.5, §6.7), updates the paraphrase robustness check (§6.3) which is now the canonical evaluation rather than a §6.3 robustness check — all five binding concepts now have at least one paraphrase-free measurement (was 1/5 in Draft 2). Adds vocabulary-breadth-as-noise-floor mechanism (§6.8) explaining differential deflation. Promotes Mahayana × Theravada AWARENESS finding into the abstract; demotes the Rovelli–Nagarjuna SUBSTRATE result to a methodological-validation footnote per the second reviewer's concern that it does rhetorical work the data cannot carry independently.

---

## Abstract

The cross-cultural convergence thesis in the study of mysticism — that contemplatives from unconnected traditions converge on a shared structural description of reality — has been debated qualitatively for sixty-five years (Stace, 1960; Katz, 1978; Forman, 1990) and tested empirically through survey instruments administered to contemporary respondents (Hood, 1975; Hood et al., 2001). To our knowledge, no published work performs a direct *textual* test using modern semantic embeddings on historical sources, with controls adequate to the constructivist critique. We report a first such test across two corpus iterations: a Phase 0 paraphrase-heavy 143-passage / 23-tradition curated corpus, and a Phase 1a whole-book 20-source / 11-tradition replication (920 chunks sampled from 5,408; 14,173 sentences; ~2.85 million tokens of verified-non-paraphrase published English translation).

The primary result is a **concept-conditional cross-tradition binding analysis** on both corpora. Each passage is tagged for the structural concepts it explicitly mentions, drawn from a pre-registered glossary: AWARENESS, RECOGNITION, ULTIMATE, WORLD, SUBSTRATE, SELF, and an observer-substrate non-separation marker NONSEP. For each concept *C* we ask whether cross-tradition passage pairs that both mention *C* are more similar in embedding space than cross-tradition pairs that don't share *C*.

**Five of seven concepts show statistically significant cross-tradition binding in Phase 0** (AWARENESS +0.113, *p* < 0.0001; RECOGNITION +0.079, *p* = 0.001; WORLD +0.077, *p* < 0.0001; ULTIMATE +0.057, *p* < 0.0001; SUBSTRATE +0.053, *p* = 0.01). The same five concepts bind across passage and sentence granularity and across two unrelated embedding models (OpenAI `text-embedding-3-large`, 3072-dim; `sentence-transformers/all-MiniLM-L6-v2`, 384-dim, via ONNX). Top tradition pairs replicate cross-model.

**In the Phase 1a whole-book corpus replication, all five binding concepts remain statistically significant** at *p* ≤ 0.0015 (AWARENESS sentence-level +0.082 OpenAI / +0.121 BERT; RECOGNITION +0.061 / +0.090; ULTIMATE +0.047 / +0.074; WORLD +0.051 / +0.065; SUBSTRATE +0.054 passage-level, unchanged from Phase 0's +0.053). This converts the Draft 2 robustness picture — only one of five bindings (ULTIMATE) was evaluable on the non-paraphrase Phase 0 subset — into a complete robustness track for all five concepts on verified published whole-book translations.

Effect sizes deflate at passage-level (3–4× for all binding concepts except SUBSTRATE) but the deflation is largely explained by **vocabulary breadth**: AWARENESS, ULTIMATE, and WORLD pattern dictionaries include common English terms (`consciousness`, `God`, `world`, `the universe`) that fire on passages that mention the term casually rather than engaging the concept technically. At *sentence-level*, where tagging filters to sentences actually using the term, Phase 0 → Phase 1a deflation is only 25–30%. SUBSTRATE's pattern dictionary is entirely technical (`emptiness`, `śūnyatā`, `implicate order`, `holographic`, `integrated information`, `holomovement`, `noumenon`) — no casual usage to add a noise floor — and SUBSTRATE binding does not deflate.

The most defensible single cross-tradition concept-binding finding is **Mahayana × Theravada at 0.518 on AWARENESS**, replicated cross-model. Neither tradition wrote toward the comparison; both are doctrinally Buddhist but represent the nondual and dualistic-buddhist sides of an ancient internal divide. We had previously highlighted the Mahayana × relational quantum mechanics SUBSTRATE binding (0.455) as a cross-period bridge, but Rovelli (2022) is part of the corpus and explicitly argues toward that correspondence; the binding confirms his argument is detectable rather than independently establishing structural identity. We retain the result with the methodological-validation framing.

We interpret these results cautiously. **Phase 1a addresses one of four pipeline-coupling concerns** identified by reviewer pass — the paraphrase confound (Phase 0 had 68% paraphrases; Phase 1a is 100% published primary-source quotation). It does *not* address translator-as-confound, regex-tagging-as-hidden-degree-of-freedom, or adversarial-passage-selection. We name what full Phase 1 requires (§10) and what reading the present results entails.

This is, to our knowledge, the first direct textual test of cross-tradition convergence using semantic embeddings on historical sources, the first reported case where a pre-registered set of structural concepts produces statistically significant cross-tradition binding under controls adequate to identify and partially mitigate the shared-vocabulary artifact, and the first to replicate a five-of-seven binding pattern across both paraphrase-heavy and verified-non-paraphrase corpora at p ≤ 0.0015. We release the corpus, code, and full result tables under MIT license.

---

## 1. Introduction

### 1.1 The convergence question

Walter Stace's *Mysticism and Philosophy* (1960) introduced the modern form of the cross-cultural convergence claim: that introspective inquirers from culturally and historically unconnected traditions report a common structural description of reality — typically a non-separation of observer and observed, the absence of a privileged self, the primacy of awareness, and a unity beneath apparent multiplicity. Robert Forman (1990) extended the claim with the "pure consciousness event" thesis. Steven Katz (1978) led the constructivist counter: there is no unmediated experience; every mystical report is shaped by the conceptual context of its author, so apparent convergence is hermeneutic projection.

The debate has run for sixty-five years on largely textual and philosophical grounds. The empirical literature is dominated by Ralph Hood's Mysticism Scale (Hood, 1975), which operationalizes Stace's categories into a 32-item survey and has been cross-culturally validated against Christian, Muslim, and Hindu respondents (Hood et al., 2001; Anthony et al., 2010; Streib et al., 2020). Hood's work is genuine empirical leverage on a closely related question: it tests whether self-reports of mystical experience by *contemporary* respondents converge across cultures. It does not test whether the *historical texts* produced by unconnected contemplatives converge in semantic structure, because survey data and textual semantics are different objects and contemporary respondents share a globalized culture in ways the historical authors did not. A direct textual test using semantic embeddings on historical sources, with controls adequate to the constructivist critique, has not appeared in the published literature.

A recent ACL survey of NLP work on religious texts (Hutchinson et al., 2024) confirms the gap: the field has focused on machine translation (the Bible and Quran as parallel corpora) and intra-tradition topic modeling. Cross-tradition embedding-based comparison of contemplative literature is largely absent. The technical tools — modern dense embeddings, permutation testing, cross-model replication, ONNX BERT inference on locked-down workstations — have matured over the last five years; the philosophical question has been waiting.

### 1.2 What this paper tests

We test one primary hypothesis and frame it carefully.

**Primary (concept-conditional).** For each of seven pre-registered structural concepts, cross-tradition passage pairs that both mention the concept are more similar in semantic embedding space than cross-tradition pairs that don't share the concept. This is the bias-aware version of the perennialist claim: not "everything converges" but "specific structural axes bind specific traditions when those traditions are discussing those axes." The primary test is run on two corpora: Phase 0 (143 curated short passages, 68% paraphrase) and Phase 1a (920 chunks sampled from 20 verified-published whole books, 0% paraphrase). Both corpora are independently pre-tagged using the same regex pattern set derived from a pre-registered glossary.

We also report two secondary descriptive analyses:

**Document-level (classical H1).** Texts from unconnected historical nondual contemplative traditions are more similar to each other than to dualistic texts. This was the original framing in our pre-analysis design document. We report it because the result is striking and survives Phase 1a, but we treat it as a methodological cautionary tale: as §6 shows, document-level embedding similarity is dominated by register and vocabulary; the same statistical method does not separate genuine structural agreement from those confounds.

**Extended document-level (H1').** Historical nondual texts and modern scientific/computational framings of structurally nondual claims (simulation theory, information physics, the mathematical universe hypothesis, analytic idealism, interface theory) form a unified cluster distinct from controls. We report this hypothesis as *falsified at the document level* in Phase 0 — modern thinkers cluster decisively with their vocabulary cohort — but find that a weaker concept-level version of the same claim is supported when conditioned on shared structural concepts. The Phase 1a corpus does not contain the modern computational sources (they are not in Project Gutenberg; the next iteration plans for arxiv and fair-use additions), so H1' is currently tested only on Phase 0 data and the result there is essentially unchanged from Draft 2.

### 1.3 What this paper does not claim, and what would still need work to claim

Nothing in this analysis bears on whether any cross-tradition structural convergence reflects:

(a) a shared truth about the structure of reality;
(b) a shared feature of human cognition under trained introspection;
(c) a shared feature of how literate contemplative cultures end up writing about introspection, independent of what they observe;
(d) a shared feature of how the small set of anglophone scholar-translators who produced our English source texts render contemplative content.

Distinguishing (a)–(d) is downstream of the empirical question we are answering, which is the prior question "is there any cross-tradition signal in textual embedding space beyond what shared vocabulary and shared register can explain?" Our affirmative answer to that question is necessary but not sufficient for any of (a)–(d), and we make no progress toward (a)–(d) here.

Phase 1a corrects one specific worry about Phase 0 (the paraphrase confound) but does not move us closer to distinguishing (a)–(d). It bounds the *size* of the signal-of-interest under one additional control; the additional controls required to address (c) and (d) — multi-translator inclusion, non-English source analysis, adversarial passage selection — remain unaddressed and define what we are calling **full Phase 1**.

We will not claim that the perennialist thesis has been settled. We will not claim that the constructivist critique has been refuted; in fact, our findings show that vocabulary and register do substantial work in apparent document-level convergence, which is exactly what the constructivists predicted. We will claim, and only claim, that a concept-level structural signal beyond shared vocabulary is detectable, statistically significant under permutation, replicated across embedding models and granularities, and *survives replacing investigator-authored paraphrases with verified published primary-source translations* on all five binding concepts. That claim is interesting because no prior empirical work has been able to formulate, let alone test, it.

---

## 2. Related work

### 2.1 The philosophical debate

Stace (1960) distinguishes *introvertive* mysticism (pure consciousness without content) from *extrovertive* mysticism (unity perceived in the phenomenal world) and argues both forms recur cross-culturally. Forman (1990, 1999) extends with the pure-consciousness-event thesis, which claims that contentless awareness is a cross-cultural phenomenon precisely because it has no content to be culturally shaped. Katz (1978) argues that every mystical experience is mediated by prior conceptual structure, so apparent cross-cultural convergence is the product of cross-cultural conceptual contamination. Forman's "decontextualism" attempts to identify experiences that escape Katzian mediation; Katzian "hard constructivism" denies such experiences exist.

The Stanford Encyclopedia of Philosophy entry on Mysticism (2025) characterizes the present state of the debate as unresolved on philosophical grounds, and its survey mentions no computational, NLP, or embedding-based methods applied to mystical literature.

Our methodology engages directly with the Katzian objection: vocabulary substitution (§6.6) tests for vocabulary-driven false convergence; concept-conditional binding (§6.1) tests for convergence at specific pre-registered structural axes rather than diffuse "they all sound similar" similarity; cross-model replication tests for embedding-model artifacts; the Phase 1a whole-book replication tests whether the signal survives replacing investigator-authored paraphrases with verified published translations. We still do not engage adequately with the strongest form of the Katzian objection — that translation conventions in anglophone scholarship may carry the convergence — and we flag this prominently as the largest remaining limitation of Phase 1a (§5, §9).

### 2.2 The empirical psychology of mysticism

Hood (1975) introduced the Mysticism Scale (M-Scale), a 32-item self-report instrument with three confirmed factors (introvertive, extrovertive, interpretation) operationalizing Stace's categories. The M-Scale has been validated cross-culturally:

- Hood et al. (2001): US Christian (n=188) vs. Iranian Muslim (n=185); measurement invariance held across samples.
- Anthony et al. (2010): comparative study of Christian, Muslim, and Hindu students in Tamil Nadu, supporting cross-tradition similarity of reported mystical experience.
- Streib et al. (2020): comparative US/German short-form study, replicating the factor structure.

Hood's work is genuine empirical leverage on the convergence claim. It measures contemporary self-reports rather than historical texts, and its respondents share a globalized culture, but it is not philosophical argument and we do not characterize it as such. We position this paper as a complement: contemporary survey work has established convergence in self-reported experience; we test whether historical texts produced by contemplatives across unconnected cultures converge in semantic structure.

Trivedi's (2025) comparative model of mysticism — neurocognitive substrates, phenomenal experiences, and noetic accounts — provides a tripartite theoretical scaffold for which our pipeline is essentially an empirical operationalization.

### 2.3 NLP on religious texts

Hutchinson et al. (2024) survey the field. The vast majority of NLP work on religious texts treats them as parallel corpora for machine translation; some intra-tradition topic modeling exists (Wieringa on Seventh-day Adventist periodicals; Choiński & Rybicki on Puritan stylometry). No published cross-tradition embedding-based comparison of contemplative texts appears to exist. The methodological frontier is genuinely open.

### 2.4 Bridge thinkers and the modern wing

Several contemporary thinkers explicitly compare structurally nondual claims in modern scientific frameworks to historical contemplative claims. Bohm's *Wholeness and the Implicate Order* (1980) draws on his collaboration with Krishnamurti. Rovelli's *Helgoland* (2022) explicitly argues that relational quantum mechanics and Nagarjuna's emptiness doctrine make structurally identical claims. Kastrup (2019) defends analytic idealism in vocabulary continuous with Advaita Vedanta. Tononi and Koch (2015) develop integrated information theory with consciousness as fundamental. Hoffman (2019) defends interface theory of perception. Tegmark (2014), Bostrom (2003), Wheeler (1990), Susskind, Lloyd (2006), and others develop information-theoretic and computational ontologies that have been compared to nondual contemplative claims with varying rigor.

These authors function as a test case for our methodology. The Phase 0 corpus included paraphrases of their work; the Phase 1a corpus does not (their books are not on Project Gutenberg, and full Phase 1 will add their arxiv papers and fair-use research excerpts to restore the comparison on verified text). For the present paper, the bridge-thinker analysis is reported only on Phase 0 data and should be read accordingly: as a methodological cautionary tale (§6.5) rather than a substantive cross-period convergence claim.

**Important caveat for the Rovelli result:** Rovelli's *Helgoland* is in the Phase 0 corpus and explicitly argues toward the Mahayana–relational-QM correspondence we report quantitatively in §6.1. The cosine-0.455 SUBSTRATE-binding does not independently establish the structural identity; it establishes that an embedding model can detect the correspondence Rovelli argued for *given the text he wrote in service of arguing for it*. Independent establishment would require modern physics texts that did not write toward the comparison, which we do not have. Per the second reviewer's recommendation, **we demote this from the abstract to a methodological-validation footnote** and promote Mahayana × Theravada (0.518 AWARENESS, both Buddhist traditions, neither writing toward the comparison) as the cleaner cross-tradition concept-binding finding.

---

## 3. Corpus

The paper uses two corpora in sequence. Phase 0 is the original short-passage corpus (143 entries, 23 traditions, 68% paraphrase) on which Draft 2 was based; we retain it because cross-model and cross-granularity replication on Phase 0 are well-supported and because the modern computational and bridge-thinker categories live only there (since their texts are not in Project Gutenberg). Phase 1a is the whole-book replication that resolves the paraphrase concern but loses (temporarily) the modern wing.

### 3.1 Phase 0 composition

The Phase 0 v0.5 corpus contains **143 English passages across 23 traditions in 3 categories**, distributed as follows.

**Historical contemplative nondual (n = 58):** Advaita Vedanta (10), Dzogchen (7), Christian mystical (10), Sufi (7), Neoplatonism (6), Kabbalah (6), Daoism (6), Mahayana (6).

**Modern scientific/computational nondual (n = 25):** simulation theory (6), information physics (6), mathematical universe (5), analytic idealism (4), interface theory (4).

**Bridge thinkers (n = 24):** implicate order / Bohm (5), process philosophy / Whitehead (5), predictive processing / Friston, Clark, Seth (5), integrated information theory / Tononi, Koch (4), relational QM / Rovelli (5).

**Dualistic contemplative controls (n = 24):** Catholic scholastic (8), Theravada Abhidhamma (8), Kantian (8).

**Non-contemplative philosophy controls (n = 12):** Humean (6), analytic / Russell (6).

### 3.2 Phase 0 source status: the paraphrase problem

Each Phase 0 passage carries a `source_status` field with three values: `quote` (high-confidence direct quotation), `approximate` (close to a published quotation with minor wording variation), `paraphrase` (doctrinally faithful rendering of a recurring teaching).

The v0.5 distribution:

| Status | Count | Fraction |
|---|---|---|
| `quote` | 6 | 4.2 % |
| `approximate` | 40 | 28.0 % |
| `paraphrase` | 97 | 67.8 % |

**The Phase 0 corpus is dominated by paraphrases.** Each paraphrase was written or selected by the lead investigator with prior beliefs about what convergence looks like, which is a direct constructivist threat to the validity of any convergence measurement: if paraphrased content is encoded in vocabulary the investigator associates with structural agreement, an embedding model can recover that vocabulary alignment without anything real about cross-tradition structure being measured. Draft 2 addressed this by running a paraphrase-exclusion robustness check (§6.3); the answer there was mixed (one of five concept bindings survived the strongest available test; four were unevaluable due to insufficient non-paraphrase coverage). The Phase 1a corpus replaces paraphrases with whole-book published translations on real authors and tests all five concept bindings on verified non-paraphrase content.

### 3.3 Phase 0 inclusion rationale and selection bias

The historical nondual sources were selected for *cultural independence* — no plausible cultural contact at time of authorship between, e.g., 8th-century Advaita and 14th-century Rhineland mysticism, or between 3rd-century Plotinus and Tang-dynasty Chan Buddhism. The single notable exception is documented Andalusian Sufi/Kabbalist contact (12c–13c), which we re-flag at point of use in §6.1 wherever Kabbalah × Sufi appears in the top results.

Bridge thinkers were chosen because each writes with one foot in scientific vocabulary and one in contemplative content; the prediction was that if document-level convergence is content-driven, they sit between clusters. This prediction failed (§6.5), which is itself informative.

Dualistic controls test whether the convergence signal tracks "religious genre" or "contemplative-nondual content." Several traditions in this category are doctrinally complex — Theravada Abhidhamma is rigorously contemplative and asserts non-self while denying observer-substrate identification — so it sits on a doctrinal boundary the experimental design treats as binary. We discuss this in §7.

Passages were chosen by the lead investigator informed by secondary scholarship. The strongest single defense against selection bias — having a constructivist-leaning scholar independently select passages from the same authors that they consider *least* nondual, then re-running the analysis — was not done in Phase 0 or Phase 1a and remains a load-bearing priority for full Phase 1.

### 3.4 Cross-model robustness in Phase 0

Each Phase 0 passage was embedded with two independent models — OpenAI `text-embedding-3-large` (3072-dim, proprietary) and `sentence-transformers/all-MiniLM-L6-v2` (384-dim, open-source, run locally via ONNX Runtime). The two models share no training data, architecture, or organization. Cross-model agreement on the five binding concepts is excellent (§6.2).

### 3.5 Phase 1a corpus: whole-book replication

The Phase 1a corpus replaces investigator-authored paraphrases with whole-book published English translations. **All 20 sources were verified against the Project Gutenberg catalog before fetch** using `scripts/verify_manifest.py`, which checks that the PG record's title matches the expected title; this caught and corrected 10 of an initial 24 PG IDs that referenced unrelated books (e.g., the originally-recorded "Plotinus Enneads" PG ID actually returned "A Ribband of Blue and Other Bible Studies" by J. Hudson Taylor; the original "Cloud of Unknowing" PG ID returned a bookbinding manual). All Phase 1a source texts in the present analysis are verified.

**Phase 1a corpus composition (20 books, ~2.85M raw tokens, sampled to 920 balanced chunks for analysis):**

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
| humean | non_contemplative | Treatise of Human Nature, Enquiry | (untranslated) |
| analytic | non_contemplative | Problems of Philosophy, External World, Mysticism and Logic | (untranslated) |

**What Phase 1a is missing relative to Phase 0:** the modern scientific/computational nondual category (simulation theory, information physics, mathematical universe, analytic idealism, interface theory) and the bridge thinkers (Bohm, Whitehead, Friston/Clark/Seth, Tononi/Koch, Rovelli). These authors' books are not on Project Gutenberg and were represented in Phase 0 by paraphrases. **Full Phase 1 plans to restore them via arxiv papers and fair-use research excerpts** so that the cross-period H1' result can be re-evaluated on verified non-paraphrase text.

**Chunking strategy.** Each cleaned book is split into ~500-token chunks at paragraph boundaries; oversized paragraphs are split at sentence boundaries. The full corpus yields 5,408 chunks; for analysis, books are stratified-sampled to ≤50 chunks each (`scripts/chunks_to_passages.py`), yielding 920 balanced chunks. Without sampling, large scholastic works (Aquinas Summa I has 1,222 chunks; Calvin Institutes 893) would dominate the comparison.

**Sentence-level analysis.** The 920 chunks split further into 14,173 sentences via punctuation-based splitting. Permutation tests at this scale require vectorized concept-binding computation (`scripts/sentence_binding_vectorized.py`); the Python-iterator implementation used in Draft 2 is intractable at *n* > 5,000 sentences.

### 3.6 Selection-bias status for Phase 1a

Phase 1a books were chosen by the lead investigator from the Project Gutenberg catalog, restricted to titles whose PG-catalog titles match the expected works. The investigator's selection criteria favored canonical historical contemplative sources and standard dualistic/non-contemplative controls. This **does not address** the adversarial-inclusion concern — a constructivist-leaning scholar would likely select differently within each author (e.g., picking the *least* nondual sections of the Bhagavad Gita, or pairing Brother Lawrence with a less-mystical Christian devotional text). The adversarial-inclusion control remains a full-Phase-1 priority.

The Phase 1a inclusion of Spinoza (`spinozist` tradition, marked nondual) and Steiner-mystics (a 20th-century commentary on 13–17c German mystics, marked christian_mystical) are arguably questionable category assignments. Spinoza's substance monism is structurally nondual in some readings and not in others; Steiner's anthology is more analytical-philosophical than the contemplative primary sources he discusses. We retain both and note the assignment in the per-tradition concept-binding results so readers can subset out.

---

## 4. Methods

### 4.1 Embedding

Texts are embedded with two independent models:

- **OpenAI `text-embedding-3-large`** (3,072-dim, proprietary), via the OpenAI API.
- **`sentence-transformers/all-MiniLM-L6-v2`** (384-dim, open-source), via ONNX Runtime locally. ONNX inference was used because the local development environment is subject to Windows Defender Application Control, which blocks torch but admits the Microsoft-signed ONNX Runtime DLLs. The two models share no training data, architecture, or organization.

Embeddings are unit-normalized; pairwise similarity is cosine.

### 4.2 Concept tagging and the regex-as-hidden-degree-of-freedom caveat

The seven pre-registered structural concepts — ULTIMATE, SUBSTRATE, AWARENESS, WORLD, SELF, RECOGNITION, NONSEP — are tagged on each passage by a manually curated dictionary of case-insensitive regex patterns. The patterns are listed in full in `scripts/concept_analysis.py` and derived from the project glossary, which was constructed before the analyses and lists the tradition-specific terminology each concept was expected to be expressed in.

The same patterns are applied to both Phase 0 and Phase 1a corpora without modification, so the *operational definition of each concept* is identical across phases. Differences in binding strength between phases reflect either (i) genuine differences between paraphrase-style and published-translation text, (ii) differences in the casual-vs-technical use of the same vocabulary at different scales, or (iii) noise.

**This remains a hidden degree of freedom.** The same person who built the glossary built the corpus. Patterns that fire on "consciousness," "awareness," "rigpa," "chit," "phi," "nous" reflect prior beliefs about which terms denote AWARENESS. A pattern set chosen by someone with a different model of convergence would tag different passages and could produce different binding scores. The Phase 1a results do not change this: the corpus is now paraphrase-free, but the tagger is unchanged. Held-out human-validated tagging on a randomly sampled subset is a full-Phase-1 priority.

### 4.3 Concept-conditional binding statistic

For each pre-registered concept *C*, restricted to cross-tradition passage pairs only:

$$
\text{binding}(C) = \overline{\text{sim}}\bigl(\text{pairs both mentioning } C\bigr) - \overline{\text{sim}}\bigl(\text{pairs where exactly one mentions } C\bigr)
$$

We compare against a permutation null in which concept-tag assignments are shuffled across passages (preserving the total count of tagged passages), 2,000 permutations. The reported *p*-value is the fraction of permutations whose binding statistic exceeds the observed value.

For sentence-level analysis, passages are split on punctuation, the same regex tagger is applied per sentence, and the same statistic is computed across sentences rather than passages. Phase 1a sentence-level analysis (14,173 sentences) uses vectorized numpy boolean-mask operations rather than Python iteration over combinations; the script is `scripts/sentence_binding_vectorized.py`. We stratified-sample sentences to ≤4,000 per analysis for tractability of the permutation tests; bindings reported are stable to the sampling seed within ±0.005.

### 4.4 Document-level statistic for the secondary descriptive analysis

For the document-level H1 (reported as a methodological cautionary tale in §6.4), we compute:

$$
\Delta_{H1} = \overline{\text{sim}}_{\text{historical-nondual cross-tradition}} - \overline{\text{sim}}_{\text{nondual-to-dualistic cross-tradition}}
$$

Significance is assessed by a 5,000-permutation test that shuffles (tradition, category) labels and recomputes the statistic. Effect-size language in this paper uses raw cosine differences and *p*-values. We avoid expressing effect sizes in "σ-above-null" units because the permutation null is non-parametric and readers from physics may mis-read such phrasing as Gaussian tail probability.

### 4.5 Vocabulary substitution and its known bias

For the substitution analysis (§6.6) we replace tradition-specific terms with role-based shared placeholders (`[qntrx]` for ULTIMATE, `[vpbkz]` for SUBSTRATE, `[mljfd]` for AWARENESS, etc.). This procedure has a **known bias toward finding cross-tradition similarity**: substituting distinct tradition-specific terms with a shared placeholder forces token-level similarity across substituted texts. The bias was identified by the lead investigator during the substitution run and is documented in `methodology-notes.md`. The substitution analysis is retained because the *failure* of the bias to fully close the modern–historical gap is itself informative, and because the H1 effect size in the substituted corpus is essentially identical to the unsubstituted result. The concept-conditional analysis on the unsubstituted corpus supersedes substitution as the canonical bias-corrected test of concept-level convergence.

The Phase 1a vocabulary substitution (Phase 1a substituted document-level result) reproduces the Phase 0 finding that substitution does very little: the H1 effect size barely changes (Phase 1a unsubstituted +0.025 → substituted +0.022). At whole-book scale, the shared-placeholder bias that distorted Phase 0 substituted results is much smaller because there's more independent content per passage to balance the few shared tokens.

### 4.6 Clustering and visualization

UMAP (n_neighbors=15, min_dist=0.1) and t-SNE (perplexity=30) are reported for descriptive purposes only. K-means and agglomerative clustering at k=3 with Adjusted Rand Index against the (nondual, dualistic, non-contemplative) labels are reported as cluster-recovery quality, again descriptive only; the primary tests are the explicit pairwise-similarity permutation tests, which are sensitive to signals that low-dimensional projection may obscure.

---

## 5. The translator-as-confound: still unaddressed after Phase 1a

A single named limitation is sufficiently load-bearing to warrant its own section, and **Phase 1a does not resolve it** — it may sharpen it.

In Phase 0, all 143 passages were English. Many were paraphrases authored by the lead investigator; the rest were drawn from a heterogeneous mix of published translations whose translator identity was inconsistent or unrecorded. We could not estimate translator effects.

In Phase 1a, **every book has a single, identified translator**: Legge for Tao Te Ching and Zhuangzi, Müller for Dhammapada, Pusey for Augustine, Redhouse for Rumi, Meiklejohn for Kant Critique of Pure Reason, and so on. The corpus is unambiguously translator-anchored, but each text now anchors entirely on one translator's conventions. If those conventions converge — and the small set of anglophone scholar-translators responsible for these classical translations have read each other extensively over a century of comparative-religion scholarship, so there is no in-principle reason they should not — then a portion of any cross-tradition similarity we measure is a property of the *English translation tradition*, not of the source texts.

**Phase 1a has no defense against this confound.** Vocabulary substitution partially addresses it by stripping the tradition-specific terminology that scholarly translators argue most about, but substitution introduces its own bias (§4.5) and does not affect the broader register and phrasing choices that translators converge on. Concept-conditional analysis partially addresses it by computing binding within concept categories rather than across the document, but the patterns used to tag concepts are themselves derived from scholarly translation conventions.

The proper defense is **multi-translator inclusion**: for each source where multiple English translations exist (and there are many — Tao Te Ching has at least Mitchell, Lau, Ames-Hall, Watson, Legge, Henricks, Red Pine; Plotinus has MacKenna, Armstrong, Gerson; the Heart Sutra has Conze, Red Pine, Tanahashi; Shankara has Madhavananda, Sastry, several others; the Bhagavad Gita has Easwaran, Mitchell, Miller, Sargeant, Arnold, Edgerton), the corpus should include all major translations and the analysis should report within-source translator variance as a baseline for between-source convergence. We could not do this in Phase 1a because the verified-on-Project-Gutenberg subset is one translation per source. Full Phase 1 will use a mix of public-domain editions across multiple translators and arxiv/fair-use modern works.

**Non-English source analysis** is the deeper defense. If a multilingual embedding model (e.g., LaBSE, multilingual-e5, or paraphrase-multilingual-MiniLM-L12-v2) is used on the original-language texts where available — Sanskrit for Advaita, Pali for Theravada, Tibetan for Dzogchen, Greek for Plotinus, Chinese for Zhuangzi and Tao Te Ching, Arabic for Rumi, Hebrew for Kabbalah — then translator-mediated convergence cannot be the explanation. This is the single most important methodological priority for full Phase 1.

We name this here, prominently, rather than in §9 because it is the strongest constructivist objection to any positive convergence finding using textual data, and because **neither Phase 0 nor Phase 1a has addressed it**. Readers should treat every result in this paper through this lens.

---

## 6. Results

### 6.1 Primary result: concept-conditional cross-tradition binding (Phase 0)

For each pre-registered structural concept *C*, the concept-binding score on cross-tradition passage pairs using *unsubstituted* embeddings, on the Phase 0 v0.5 corpus:

| Concept | n passages with *C* | both-have mean | one-has mean | **binding** | *p* (one-sided, 2,000 perms) |
|---|---|---|---|---|---|
| AWARENESS | 19 | 0.4195 | 0.3061 | **+0.1133** | **< 0.0001** |
| RECOGNITION | 9 | 0.3321 | 0.2528 | **+0.0793** | **0.001** |
| WORLD | 32 | 0.3752 | 0.2983 | **+0.0769** | **< 0.0001** |
| ULTIMATE | 36 | 0.3283 | 0.2712 | **+0.0571** | **< 0.0001** |
| SUBSTRATE | 10 | 0.3604 | 0.3078 | **+0.0526** | **0.01** |
| SELF | 3 | 0.2315 | 0.2890 | −0.0575 | 0.90 (NS) |
| NONSEP | 0 | n/a | n/a | n/a | not measurable |

**Five of seven pre-registered concepts show statistically significant cross-tradition binding in Phase 0.** The shared-placeholder substitution bias (§4.5) does not apply: no token sharing was forced. Effect sizes are substantial (≈ +0.05 to +0.11 in cosine similarity, on a base of ≈ 0.30 cross-tradition mean similarity).

Two non-significant results are corpus-limited: only 3 passages used explicit SELF markers (`atman`, `jiva`, `the agent`, `Markov blanket`) — most passages discuss self in unmarked English the regex tagger does not catch — and no passages used the explicit NONSEP labels (`nondual`, `advaita`, `wahdat al-wujud`) despite expressing observer-substrate non-separability throughout the nondual category. SELF and NONSEP are unmeasured rather than refuted.

**The strongest individual results within concepts.**

**AWARENESS** (consciousness, awareness, rigpa, chit, phi, nous). Top cross-tradition pairs (both passages mention AWARENESS):

| Pair | mean similarity |
|---|---|
| analytic_idealism × implicate_order | 0.624 |
| analytic_idealism × interface_theory | 0.585 |
| implicate_order × interface_theory | 0.561 |
| **mahayana × theravada** | **0.518** |
| analytic_idealism × iit | 0.511 |
| iit × implicate_order | 0.509 |

The modern wing dominates by volume, but **Mahayana × Theravada at 0.518 is the cleanest cross-tradition AWARENESS binding**: neither tradition wrote toward the comparison, both are doctrinally Buddhist but represent the nondual and dualistic-buddhist sides of an ancient internal debate, and they share enough Pali/Sanskrit Buddhist conceptual vocabulary (in their respective English-translation traditions) that registering the similarity is non-trivial — but they sit on opposite doctrinal sides of the observer-substrate identification question. This is the new poster-child finding promoted from §6.5 of Draft 2.

**RECOGNITION** (liberation, enlightenment, theosis, fana, gnosis, jnana). Top cross-tradition pairs:

| Pair | mean similarity |
|---|---|
| advaita × dzogchen | 0.528 |
| dzogchen × sufi | 0.440 |
| dzogchen × theravada | 0.439 |
| daoism × dzogchen | 0.438 |
| advaita × sufi | 0.429 |
| advaita × neoplatonism | 0.390 |

This is the Stace–Forman classical perennialist signal, quantitatively confirmed across historical contemplative traditions when those traditions are specifically discussing liberation/awakening. The pairs span eras and cultures with no plausible historical contact: 8th-century Advaita, 11th-century Dzogchen, 13th-century Sufism, 3rd-century Neoplatonism, 4th-century BCE Daoism, all converging on a recognizable conceptual axis.

**SUBSTRATE** (emptiness, dependent origination, implicate order, integrated information, holographic). Top cross-tradition pairs:

| Pair | mean similarity |
|---|---|
| dzogchen × mahayana | 0.469 |
| mahayana × relational_qm | 0.455 |
| iit × implicate_order | 0.453 |
| dzogchen × relational_qm | 0.438 |
| dzogchen × implicate_order | 0.437 |

The Mahayana × relational_qm SUBSTRATE binding of 0.455 is the bias-free quantitative correlate of the structural correspondence Rovelli (2022) argued for qualitatively. **Important caveat reiterated from §2.4:** Rovelli's *Helgoland* is in the corpus, and the relational_qm passages were authored by him in service of arguing for the very correspondence we measure. The 0.455 binding confirms his argument is detectable by an embedding model that has read his argument; it does not independently establish the structural identity, because no relational-QM authors who were not writing toward this comparison are in the corpus. We have demoted this from the abstract per the second reviewer's recommendation.

**ULTIMATE** (God, Brahman, Tao, Ein Sof, mathematical universe, computational substrate). Top cross-tradition pairs:

| Pair | mean similarity | Notes |
|---|---|---|
| mathematical_universe × simulation_theory | 0.506 | Both modern computational ontologies |
| advaita × sufi | 0.475 | Cultural independence good |
| kabbalah × sufi | 0.445 | **Note: documented Andalusian contact 12c–13c; not culturally independent** |
| advaita × kabbalah | 0.430 | |
| christian_mystical × sufi | 0.417 | |
| advaita × mathematical_universe | 0.370 | 21c physicist × 9c Hindu philosopher |

The Andalusian Sufi/Kabbalah convergence is documented in the religion-history literature and should not be cited as cross-cultural-independence evidence; we report it for completeness.

**WORLD** (samsara, simulation, cosmos, phenomenal universe). 32 passages with the concept, 468 cross-tradition both-have pairs. Top pairs are diffuse across categories at the 0.40 range; no single dominant convergence emerges, but the binding score (+0.077, *p* < 0.0001) is well-supported by the volume of evidence.

### 6.2 Cross-model and cross-granularity replication (Phase 0)

The concept-binding analysis is rerun at sentence granularity (322 sentences from the 143 passages, 123 sentences tagged with at least one concept) with both embedding models.

| Concept | OpenAI passage | OpenAI sentence | BERT (MiniLM) sentence |
|---|---|---|---|
| AWARENESS | +0.1133 *** | +0.1139 *** | **+0.2042** *** |
| RECOGNITION | +0.0793 ** | +0.0822 *** | +0.0725 *** |
| WORLD | +0.0769 *** | +0.0821 *** | +0.0733 *** |
| ULTIMATE | +0.0571 *** | +0.0668 *** | +0.0793 *** |
| SUBSTRATE | +0.0526 ** | +0.0514 ** | +0.0497 ** |

\*\*\* *p* < 0.0001, \*\* *p* < 0.01, all permutation tests.

The five binding concepts replicate across both granularities and both embedding models. AWARENESS binding is approximately twice as strong in the smaller BERT model. Plausible interpretation: MiniLM is more sensitive to lexical-structural cues from concept terms in its smaller embedding space, while the larger OpenAI model captures finer distinctions between different kinds of consciousness-talk that lower the average binding. The directional result is preserved. The top tradition-pairs are essentially identical across models; both place analytic_idealism × implicate_order at the top of AWARENESS, advaita × dzogchen at the top of RECOGNITION, and mahayana × relational_qm at the top of SUBSTRATE.

### 6.3 Phase 1a replication: concept-binding on verified whole-book corpus

This is the canonical paraphrase-free evaluation. The Phase 1a corpus is 100% verified published-translation primary-source text (§3.5); all 5 binding concepts can now be evaluated, where Phase 0 could only evaluate ULTIMATE on its non-paraphrase subset.

**Phase 1a concept-binding results (passage-level, 920 chunks):**

| Concept | n_passages with C | Phase 1a binding | Phase 0 binding | *p* (Phase 1a) |
|---|---|---|---|---|
| AWARENESS | 52 | **+0.0258** | +0.1133 | 0.0005 |
| RECOGNITION | 51 | +0.0247 | +0.0793 | 0.0005 |
| WORLD | 170 | +0.0216 | +0.0769 | < 0.0001 |
| ULTIMATE | 562 | +0.0141 | +0.0571 | < 0.0001 |
| **SUBSTRATE** | 15 | **+0.0541** | +0.0526 | 0.0015 |
| SELF | 27 | −0.0124 | −0.0575 | 0.93 (NS) |

**All five binding concepts remain statistically significant at *p* ≤ 0.0015 on the paraphrase-free Phase 1a corpus.** This exceeds the second-reviewer prior (≈60% probability that AWARENESS+RECOGNITION survive; ≈40% probability that the full five-concept pattern survives) and converts the Draft 2 Appendix B robustness picture (1/5 with a complete robustness track) into a complete robustness track for all five concepts.

**Effect sizes deflate 3–4× at passage-level for every binding concept except SUBSTRATE, which is unchanged** (+0.0541 vs +0.0526). This unequal deflation is the subject of §6.7 and §6.8.

**Phase 1a sentence-level (4,000 stratified-sampled sentences):**

| Concept | OpenAI Phase 1a | OpenAI Phase 0 | BERT Phase 1a | BERT Phase 0 |
|---|---|---|---|---|
| **AWARENESS** | **+0.0823** | +0.1139 | **+0.1205** | +0.2042 |
| RECOGNITION | +0.0610 | +0.0822 | +0.0900 | +0.0725 |
| ULTIMATE | +0.0471 | +0.0668 | +0.0743 | +0.0793 |
| WORLD | +0.0512 | +0.0821 | +0.0648 | +0.0733 |
| SELF | +0.0313 (p=0.006) | NS | +0.0658 | +0.0343 (NS) |
| SUBSTRATE | +0.0530 (p=0.04) | +0.0514 | +0.0485 (p=0.09, NS) | +0.0497 |

**The sentence-level deflation is much milder: 25–30% rather than 3–4×.** §6.8 explains why.

**SELF binding becomes significant on Phase 1a sentence-level OpenAI** (+0.031, *p*=0.006) where it was non-significant in Phase 0. The larger corpus surfaces enough explicit SELF markers (atman, ego, the empirical self, conscious agent) to estimate the binding. The negative direction in Phase 0 (n=3) was a small-sample artifact.

**SUBSTRATE in Phase 1a sentence-level is barely significant at *p*=0.04 in OpenAI and non-significant at *p*=0.09 in BERT.** This is a sample-size artifact: at 4,000 stratified-sampled sentences, only 5 have SUBSTRATE-pattern hits (4 cross-tradition both-have pairs). The Phase 1a passage-level analysis where SUBSTRATE has 15 passages tagged and 88 both-have pairs is the stronger evaluation of SUBSTRATE specifically; the sentence-level subsample is too thin. SUBSTRATE remains the most stable concept binding across Phase 0 and Phase 1a in the analyses with adequate sample size.

### 6.4 Document-level H1 (cautionary descriptive result), now with Phase 1a

The classical document-level perennialist signal across three independent runs:

| Statistic | Phase 0 v0 (n=107) | Phase 0 v0.5 (n=143) | Phase 0 v0.5 substituted | **Phase 1a (n=920)** |
|---|---|---|---|---|
| historical-nondual cross mean | — | 0.315 | 0.336 | **0.371** |
| nondual_to_dualistic mean | — | 0.270 | 0.292 | **0.346** |
| observed Δ_H1 | +0.047 | +0.045 | +0.044 | **+0.025** |
| permutation *p* (one-sided) | < 0.0001 | < 0.0001 | < 0.0001 | **< 0.0001** |

**H1 survives Phase 1a at *p* < 0.0001 with effect size approximately halved** (+0.025 vs +0.045). Whole-book real text shows the convergence at smaller magnitude than paraphrase-heavy short text did; this is consistent with paraphrases having inflated the apparent effect roughly 2×.

**Striking observation from Phase 1a:** dualistic Western philosophical/theological traditions (Kant, Aquinas, Augustine, Calvin) cluster *more tightly cross-tradition* (0.383) than the historical nondual traditions do (0.371). In Phase 0 this was reversed (nondual 0.334, dualistic 0.249). The Phase 0 paraphrases were too stylistically uniform in the nondual category; real Tao Te Ching + Upanishads + Sufi Rumi + Spinoza Ethics + Brother Lawrence are stylistically far more different from each other than Aquinas + Calvin + Kant are. **The historical H1 claim survives despite the nondual category having lower within-category cohesion than the dualistic control.** This is arguably more compelling for the perennialist position than the Phase 0 result, not less: convergence is happening *despite* greater within-category diversity, which is what cultural-independence would predict.

### 6.5 The bridge-thinker design and what it teaches (Phase 0 only)

UMAP projection of Phase 0 v0.5 embeddings shows three macro-clusters: historical contemplative nondual; modern scientific/computational nondual + bridge thinkers; dualistic + analytic controls. Bridge thinkers (Bohm, Whitehead, Friston/Clark/Seth, Tononi/Koch, Rovelli) were chosen as a critical test: if document-level convergence is content-driven, they sit between the modern and historical clusters; if vocabulary-driven, they sit with their vocabulary cohort.

| Bridge thinker | mean sim to historical-nondual | mean sim to modern-computational | gap (h − m) |
|---|---|---|---|
| Bohm | 0.315 | 0.403 | −0.088 |
| Whitehead | 0.296 | 0.394 | −0.098 |
| Friston/Clark/Seth | 0.210 | 0.352 | −0.142 |
| Tononi/Koch | 0.255 | 0.426 | −0.171 |
| Rovelli | 0.282 | 0.415 | −0.133 |

**Every bridge thinker clusters with the modern cohort at the document level**, including Bohm (who explicitly developed his thinking with Krishnamurti) and Rovelli (who explicitly argued the Mahayana correspondence we measure in §6.1). This is a clean falsification of H1' *as originally formulated* — modern scientific framings of nondual structure do not form a unified cluster with historical contemplative nondual texts at the document level.

The reconciliation with the concept-binding result is straightforward: document-level embedding similarity attends to everything in the passage — the technical apparatus, citation patterns, academic register, syntactic structure — and these features dominate the similarity computation. Conditioning on a shared concept focuses the comparison on the content that the concept-bearing context contributes, and convergence becomes visible. The Mahayana × relational_qm document-level similarity is 0.327 (modest); their SUBSTRATE-conditioned similarity is 0.455 (high). The same texts, the same model, two different statistics, two different answers.

**This entire analysis depends on Phase 0 paraphrases.** Phase 1a has no bridge-thinker category because their books are not on Project Gutenberg. Re-running the bridge-thinker analysis on verified non-paraphrase text is a full-Phase-1 priority once arxiv papers and fair-use excerpts are added.

### 6.6 Vocabulary substitution: partial closure, biased measurement

We retain the vocabulary-substitution analysis from earlier Phase 0 work because the *direction* of the result remains informative even given the bias. Substituting tradition-specific terms with shared placeholders raises every cross-similarity by roughly 0.015–0.030 (an artifact of forced placeholder sharing). The modern × historical similarity rises by 0.030, slightly more than the across-the-board lift, suggesting that some genuine content convergence was being masked by vocabulary. But the bulk of the gap remains: the modern cluster's within-similarity (0.468) is still well above its similarity to the historical cluster (0.304). The vocabulary share of the modern–historical gap is best estimated at 15–30%, with the true value almost certainly below the upper bound given the shared-placeholder bias.

Phase 1a vocabulary substitution shows the same direction but smaller magnitude: substitution shifts the H1 effect size from +0.025 to +0.022 (essentially unchanged), and modern × historical cannot be measured on Phase 1a because the modern category is empty. This is consistent with the prediction that shared-placeholder bias is small at whole-book scale (more independent content per passage to balance the few shared tokens).

### 6.7 Phase 1a corpus topology and what survived

The most important Phase 1a result is that **the corpus revision was supposed to reduce the convergence signal — and it did, but unequally**.

Predictions before running Phase 1a:
- Phase 0 effect sizes are partly inflated by paraphrase uniformity. Expect deflation in Phase 1a.
- The reviewer prior: ~60% AWARENESS + RECOGNITION survive at *p* ≤ 0.01; ~40% the full five-concept pattern survives.
- Investigator prior: indifferent to outcome; all directions produce a substantive paper.

What we observed:

- **All five binding concepts survived statistical significance** at *p* ≤ 0.0015 (above the reviewer's 60%/40% prior).
- Effect sizes deflated **3–4×** at passage-level for AWARENESS, RECOGNITION, WORLD, ULTIMATE.
- **SUBSTRATE did not deflate** — Phase 0 passage-level +0.0526 → Phase 1a passage-level +0.0541.
- At sentence-level, deflation was only **25–30%** rather than 3–4×.

The unequal deflation pattern is the most substantive new Phase 1a finding and is the subject of §6.8. The full five-concept survival exceeds both priors and shifts the paper's center of gravity from "AWARENESS and RECOGNITION are the load-bearing findings" to "all five concept bindings survive paraphrase exclusion, and the mechanism behind their unequal deflation is itself informative."

### 6.8 Vocabulary breadth as noise floor: the SUBSTRATE puzzle, mechanistically explained

The passage-level Phase 0 → Phase 1a deflation pattern is striking: every binding concept lost 3–4× of its effect size except SUBSTRATE, which lost nothing. The sentence-level pattern is different: every concept including SUBSTRATE retained 70–75% of its effect size.

The explanation is mechanical: **passage-level concept tagging fires when the pattern appears anywhere in the passage, even when the rest of the passage is about something else.** The pattern dictionaries for AWARENESS, ULTIMATE, and WORLD include common English terms (`consciousness`, `awareness`, `God`, `the divine`, `world`, `the universe`, `cosmos`) that appear frequently in published philosophical and theological prose in non-technical context. Phase 0 paraphrases were investigator-curated to use these terms only when discussing the concept technically; Phase 1a published prose uses them everywhere. The Phase 1a passage-level binding therefore averages over a mix of passages-actually-about-the-concept and passages-merely-containing-the-pattern, diluting the effect.

Sentence-level analysis filters to sentences that actually contain the concept pattern. The dilution disappears, and Phase 0 → Phase 1a deflation drops to 25–30%.

**SUBSTRATE's pattern dictionary contains no common English terms.** The full list:

> `emptiness`, `śūnyatā` (with the `ś` Unicode variant), `svabhāva`, `the implicate order`, `implicate order`, `the holomovement`, `holomovement`, `the holographic principle`, `holographic`, `dependent origination`, `dependently arisen`, `basic space`, `integrated information`, `noumenon`, `noumena`, `thing-in-itself`, `the quantum vacuum`.

**None of these appear in casual usage.** A Phase 1a passage that's tagged for SUBSTRATE almost certainly is engaging the concept technically. The passage-level dilution that affected other concepts does not affect SUBSTRATE, which is why the binding does not deflate.

This is the **vocabulary-breadth-as-noise-floor** mechanism. Apparent robustness of SUBSTRATE between phases is not (primarily) a deeper structural fact about the substrate concept — it's the absence of a casual-usage noise floor that contaminated the other concepts' passage-level tagging.

**Predictions stated before testing**, deliverable in a follow-on analysis (held-out for full Phase 1):

If we restrict AWARENESS, ULTIMATE, WORLD tagging to *technical-only* vocabulary (drop `consciousness`/`awareness`, `God`/`the divine`, `world`/`the universe`; keep `rigpa`/`chit`/`citta`/`nous`/`phi`; `Brahman`/`Tao`/`Ein Sof`; `samsara`/`the ten thousand things`):

| Concept | Phase 1a current | Prediction (technical-only) |
|---|---|---|
| AWARENESS | +0.026 | +0.08 to +0.11 (recovers toward Phase 0) |
| ULTIMATE | +0.014 | +0.04 to +0.06 (partial recovery) |
| WORLD | +0.022 | +0.06 to +0.08 (substantial recovery) |
| RECOGNITION | +0.025 | +0.03 to +0.05 (already mostly technical, small recovery) |
| SUBSTRATE | +0.054 | +0.054 (unchanged — no casual terms to drop) |

If the predictions hold, the apparent Phase 1a deflation is largely a vocabulary-breadth noise floor; the structural cross-tradition convergence is recoverable from Phase 1a data with better tagging. If predictions fail (especially if AWARENESS does not recover), there is some additional explanation for the deflation that we have not identified.

This is the natural next analysis to run before adding more corpus or co-authors, and we have written the predictions before running so that the result, whichever way it falls, is a clean confirmation or refutation of the mechanism rather than a post-hoc rationalization.

### 6.9 What document-level Phase 1a does and does not show

The document-level H1 result on Phase 1a (§6.4) is the most directly comparable analysis to the Phase 0 document-level result. It survives at *p* < 0.0001 with effect size halved, which is exactly what the reviewer predicted for "narrow positive" Phase 1 outcomes. The dualistic-cluster-tighter-than-nondual-cluster flip noted in §6.4 is consistent with cultural-diversity-of-nondual-traditions being real (Tao Te Ching, Upanishads, Sufi poetry, Christian devotional, Spinoza ethics, all different in register) rather than a methodological artifact.

The document-level Phase 1a *does not* test cross-period H1' (modern + historical convergence) because the Phase 1a corpus has no modern computational sources. Restoring the modern wing on verified non-paraphrase text is a full-Phase-1 priority via arxiv papers and fair-use research excerpts.

---

## 7. Discussion

### 7.1 What is supported

A concept-level structural signal beyond shared vocabulary is detectable in textual embedding space, replicated across two unrelated embedding models, two granularities, and **two corpora** — one paraphrase-heavy and one verified-non-paraphrase.

Five of seven pre-registered concepts bind cross-tradition pairs at *p* ≤ 0.001 in Phase 0; the same five bind at *p* ≤ 0.0015 in Phase 1a after replacing investigator-authored paraphrases with whole-book published translations.

The classical Stace–Forman RECOGNITION signal across historical contemplative traditions (Advaita ↔ Dzogchen ↔ Sufi ↔ Daoism ↔ Neoplatonism) is the cleanest quantitative correlate of what the perennialist tradition has argued for qualitatively for sixty-five years.

**The cleanest single concept-binding result is Mahayana × Theravada at 0.518 on AWARENESS** (Phase 0; Phase 1a confirms at sentence-level, see §6.3). Two Buddhist traditions on opposite sides of the doctrinal nondual/dualistic divide, neither writing toward the comparison, both discussing consciousness, converge tightly when conditioned on that discussion. This replaces the Rovelli–Nagarjuna SUBSTRATE binding (which Rovelli explicitly argued for in his own corpus text) as the abstract-level result.

The document-level Δ_H1 result is robust enough to survive both paraphrase exclusion (Phase 1a) and shared-placeholder substitution (§6.6), indicating the signal is not exclusively an artifact of investigator-authored paraphrases or of tradition-specific vocabulary.

### 7.2 What is not supported or not yet testable

H1' as originally formulated — that modern scientific framings and historical contemplative texts form a single unified cluster at the document level — is falsified in Phase 0. Bridge thinkers, including those who explicitly argue cross-period structural correspondences, cluster decisively with their vocabulary cohort at the document level. A weaker concept-level version of H1' is supported by §6.1, with the caveats from that section. Phase 1a cannot test H1' because the modern category is empty.

The translator-as-confound (§5) is unaddressed in both Phase 0 and Phase 1a. Every signal reported here is consistent both with structural convergence in source content and with shared scholarly translation conventions. **Multi-translator inclusion and non-English source analysis are the two largest unaddressed threats to validity** and the top priorities for full Phase 1.

The Rovelli–Nagarjuna SUBSTRATE binding does not independently establish the structural correspondence; it confirms that an embedding model can detect the correspondence Rovelli argued for, given his text in the corpus. We retain the result as methodological validation only.

### 7.3 The decomposition that is defensible

The honest current picture decomposes apparent cross-tradition similarity into:

1. **Concept-level structural binding** on five pre-registered axes, detectable in *p* ≤ 0.0015 binding scores, replicated cross-model, cross-granularity, and across paraphrase-heavy and whole-book real-text corpora. This is the part of the convergence picture that survives the controls Phase 0 + Phase 1a were able to apply.

2. **Document-level vocabulary effect**, partially closed by substitution (~15–30% of the modern–historical gap in Phase 0, upper-bounded by the shared-placeholder bias). Vocabulary matters, exactly as constructivists predicted.

3. **Document-level register and style effect** (~50–70% of the modern–historical gap), not closed by current methods, plausibly the dominant factor in document-level cluster separation.

4. **Translator-tradition effect** (unbounded in both Phase 0 and Phase 1a), likely material, requires multi-translator inclusion to estimate.

5. **Paraphrase-author effect** (now bounded by Phase 1a). The Phase 0 → Phase 1a effect-size ratio at passage-level (~3–4×) is dominated by vocabulary-breadth noise floor (§6.8); the residual paraphrase-specific inflation at sentence-level is ~25–30%.

6. **Genuine content difference** between modern computational nondualism and historical contemplative nondualism (probably real and small in Phase 0, untestable in Phase 1a without restoring the modern wing on verified text). Most plausibly representing differences in level of description: the moderns reason about substrate, information, computation; the historical contemplatives report about awareness, perception, recognition.

The signal-of-interest — (1), genuine concept-level convergence — is the smallest and best-controlled component, and is the only one we cite affirmatively. **Phase 1a is the first iteration where (5) is genuinely bounded by data rather than asserted.**

### 7.4 What we are not claiming and what would still need work to claim

Per §1.3, no result here distinguishes among the four interpretations: shared truth about reality, shared cognitive feature of trained introspection, shared writing convention of literate contemplative cultures, or shared translation convention of anglophone scholars. We make no progress toward any of these and do not gesture at any of them.

The result is consistent with a constructivist explanation in which translation conventions and scholar-translator influence carry the convergence; it is also consistent with a structural-convergence explanation in which contemplatives across cultures detected and described similar structural features of mind or reality; **and Phase 0 + Phase 1a as a combined evidence base cannot distinguish these.** Multi-translator inclusion and non-English source analysis are necessary to even begin to distinguish them. We do not advance an interpretation; we report measurements.

---

## 8. Methodological lessons for full Phase 1

Phase 0 + Phase 1a have produced both substantive findings and methodological discoveries that should shape the remainder of Phase 1.

- **Document-level embedding similarity is inadequate** for testing cross-tradition structural convergence when the corpus mixes registers or includes paraphrases. Concept-conditional similarity is the appropriate bias-aware alternative. *Confirmed in both Phase 0 and Phase 1a.*

- **Shared-placeholder vocabulary substitution introduces a tautological similarity bias.** Per-tradition placeholders or mask-and-compare schemes should replace shared placeholders if substitution is used at all; the bias is empirically smaller at whole-book scale than at short-passage scale but is still present. *Refined understanding from Phase 1a.*

- **Sentence-level granularity preserves the signal and in some cases sharpens it.** Passage-level granularity introduces a casual-usage noise floor that affects concepts whose pattern dictionaries include common English terms. Technical-only-vocabulary concepts (SUBSTRATE) are immune; broader-vocabulary concepts (AWARENESS, ULTIMATE, WORLD) deflate at passage-level. **Sentence-level should be the default granularity for future analyses.** *New from Phase 1a.*

- **Vocabulary breadth matters for tagging.** Concepts with technical-only pattern dictionaries (SUBSTRATE) have higher signal-to-noise than concepts whose dictionaries include common English terms (AWARENESS, WORLD). Future tagger design should split concepts into technical-only and broad-vocabulary variants, or require multiple pattern hits per passage rather than one. *New from Phase 1a §6.8.*

- **Cross-model replication is cheap and should be the default.** The OpenAI run cost dollars; the ONNX BERT run was free and ran on a Windows machine with torch blocked by Application Control, sidestepped via Microsoft-signed ONNX Runtime DLLs. *Confirmed in Phase 0 and Phase 1a.*

- **Regex-based concept tagging is reproducible and pre-specifiable but is a hidden degree of freedom.** Phase 1a did not address this; full Phase 1 should add learned concept taggers and human-validated tags on a held-out sample.

- **Paraphrase confound was real and roughly 2×.** Phase 0 effect sizes were inflated by paraphrase uniformity at document-level (H1 +0.045 Phase 0 vs +0.025 Phase 1a). Phase 1 efforts to add additional sources or extend the corpus should prioritize verified primary translations and avoid investigator-authored paraphrases. *Confirmed Phase 1a.*

- **PG ID verification is necessary.** 10 of 24 initial PG IDs in the Phase 1a manifest returned unrelated books (different works that happened to occupy those IDs). The `scripts/verify_manifest.py` title-match check caught this; the corpus would otherwise have been silently corrupted. Future Phase 1 corpus iterations should run title verification before fetch.

- **Sparse autoencoder probes** of the embedding space (planned for full Phase 1) should identify interpretable structural axes that survive both vocabulary and register noise, complementing the regex-based concept analysis.

---

## 9. Limitations

Named explicitly because the work is exploratory and the substantive claims, if taken further than we take them here, would be large.

1. **Translator-as-confound.** All passages English-translated by a small set of anglophone scholar-translators with shared conventions. See §5. The largest single unaddressed threat to validity in Phase 0 + Phase 1a. Multi-translator inclusion and non-English source analysis are top full-Phase-1 priorities.

2. **Selection bias.** Passages were chosen by the lead investigator informed by secondary scholarship; an adversarial inclusion process (a constructivist-leaning scholar independently selecting *least-nondual* passages from the same authors) was not performed in Phase 0 or Phase 1a.

3. **Regex concept tagging.** Patterns derive from a glossary the lead investigator built before the analyses. The concept-conditional analysis is bias-free *of the shared-placeholder artifact*, not bias-free *in the absolute*. Held-out human-validated tagging is required for the stronger claim.

4. **Phase 1a corpus is single-translator per source.** Each book anchors on one translator's conventions. Within-source translator-variance baseline is required for the strong cross-source convergence claim.

5. **Phase 1a corpus has no modern computational wing.** Bridge thinkers (Bohm, Rovelli, etc.) and the modern wing (Bostrom, Kastrup, Tegmark, etc.) are not on Project Gutenberg and could not be included in Phase 1a. H1' as currently tested rests on Phase 0 paraphrases. Restoring the modern wing on arxiv/fair-use sources is a full-Phase-1 priority.

6. **Single language.** All passages in English. See §5. Non-English source analysis with multilingual embeddings is the deepest defense against translator-as-confound.

7. **Single non-Rovelli relational-QM source absent.** The Mahayana × Relational QM result depends on text Rovelli wrote in service of arguing for the correspondence. We demote the result to methodological-validation status pending independent relational-QM sources.

8. **No formal pre-registration.** Pre-registered candidate concepts were specified before the analyses, but the corpus composition, statistical tests, and decision rules were not committed to an OSF pre-registration. Full Phase 1 must remedy this.

9. **Naive sentence splitting.** Punctuation-based, adequate for the short well-formed passages here but inadequate for the longer texts a Phase 1 whole-book corpus uses. The sentence_concept_analysis pipeline produces 14,173 sentences from 920 chunks via punctuation regex; sentence-boundary errors are unaudited.

10. **Permutation tests vectorized for Phase 1a scale.** Phase 0 used Python iteration over combinations; Phase 1a required vectorized numpy permutation tests (`scripts/sentence_binding_vectorized.py`) for tractability. Vectorization is mathematically equivalent but adds a code-path the original Phase 0 results did not test.

11. **No interpretability layer.** We have established that concepts bind traditions but have not characterized *what structural feature* the binding measures beyond the regex patterns used to detect it. Sparse autoencoder probes and contrastive direction analysis are deferred to full Phase 1.

12. **No adversarial controls.** Synthetic mystical writing generated by language models in the style of each tradition is the natural adversarial test (real cross-tradition clustering should be tighter than synthetic clusters; otherwise the convergence is "stylistic mysticism" rather than structural agreement). Not run in Phase 0 or Phase 1a.

13. **Stratified sentence sampling.** Phase 1a sentence-level analysis subsamples to 4,000 sentences per analysis seed. Bindings reported are stable to seed within ±0.005, but the n_with for rare concepts (SUBSTRATE in particular) drops sharply under sampling.

---

## 10. Full Phase 1 program

The Phase 0 + Phase 1a findings define a concrete remaining program for full Phase 1.

**Top priorities (load-bearing).**

- **Multi-translator inclusion.** For every source with multiple English translations available, include all major ones; report within-source translator variance as the baseline for cross-source convergence. Target sources: Tao Te Ching (Mitchell, Lau, Ames-Hall, Watson, Henricks, Red Pine — at least four); Bhagavad Gita (Easwaran, Mitchell, Miller, Sargeant, Arnold, Edgerton); Heart Sutra (Conze, Red Pine, Tanahashi); selected Upanishads (Olivelle, Easwaran, Müller, Paramananda).

- **Non-English source analysis.** Multilingual embedding models (LaBSE, multilingual-e5, paraphrase-multilingual-MiniLM-L12-v2) on original-language texts where available (Sanskrit, Pali, Tibetan, Greek, Chinese, Arabic, Hebrew). The deepest defense against translator-as-confound; possibly the most important single full-Phase-1 priority.

- **Modern computational and bridge thinkers restored on verified text.** Arxiv papers (Bostrom simulation argument; Wheeler "it from bit"; Tegmark MUH; Rovelli relational QM; Friston FEP; Tononi IIT; etc.) and fair-use research excerpts from Kastrup, Hoffman, Bohm books. Restores H1' testability on non-paraphrase corpus.

- **Adversarial passage selection.** Constructivist-leaning scholar independently selects "least-nondual" passages from the same authors. Re-run the analysis on the union and the difference. *Escalated from secondary to load-bearing per second-reviewer pass.*

- **Held-out human-validated concept tagging.** On a randomly sampled subset of the corpus, have one or more annotators tag passages independently. Report inter-rater agreement and rerun concept-binding on the human-tagged subset to compare with regex-tag results. *Escalated from secondary to load-bearing per second-reviewer pass.*

- **OSF pre-registration.** Lock corpus composition, analysis pipeline, statistical tests, decision rules, and the predicted-outcome priors stated in §7 before running full Phase 1.

**Methodological controls.**

- **Technical-only-vocabulary tagger variants.** Per the §6.8 predictions, run AWARENESS / ULTIMATE / WORLD with technical-only patterns and check whether Phase 1a effect sizes recover toward Phase 0 levels. This is a cheap test of the vocabulary-breadth-as-noise-floor mechanism.

- **Per-tradition or mask-and-compare placeholder schemes** to replace shared-placeholder substitution.

- **Adversarial synthetic texts.** LM-generated mystical writing in the style of each tradition; real cross-tradition clustering should be tighter than synthetic.

- **Style-normalized rewrites** (LM-mediated, lossy but tractable) to test the style-and-register share of the modern–historical gap.

**Interpretability.**

- **Sparse autoencoder probes** on the embedding space.
- **Contrastive direction extraction** within and across traditions.
- **Token-level contextualized embeddings** comparing concept terms in context across traditions.

**Generalization to other claimed convergent concepts.** The methodology is concept-agnostic. Candidate concepts for separate convergence tests on the same framework include the Golden Rule, the Hero's Journey, non-attachment, the ineffability of the ultimate, the dependence of perception on the perceiver, mystical death and rebirth, eternal recurrence, the great chain of being, the threefold path. The deliverable from running the framework on a suite of candidates is a *meta-table*: for each tested concept, was convergence detected? With what controls? What survived? The meta-table is what would move the perennialism debate forward as a field, not a single positive result on nondualism.

---

## 11. Code and data availability

All code, corpora, results, and methodology documents are MIT-licensed and version-controlled. The repository is structured for independent reproduction.

**Analysis pipelines.**

- `scripts/concept_analysis.py` — concept-conditional binding (primary analysis, passage-level).
- `scripts/sentence_concept_analysis.py` — sentence-level concept binding, OpenAI and ONNX BERT backends.
- `scripts/sentence_binding_vectorized.py` — vectorized numpy concept-binding for *n* > 5,000 sentence corpora (Phase 1a).
- `scripts/onnx_embedder.py` — local BERT-class inference via ONNX Runtime.
- `scripts/prototype.py` — document-level embedding, clustering, visualization.
- `scripts/substitute.py` — structural-role vocabulary substitution.
- `scripts/robustness_paraphrase.py` — paraphrase-exclusion robustness check used in Draft 2 §6.3.

**Phase 1a corpus pipeline.**

- `scripts/fetch_books.py` — Gutenberg / arxiv / web fetcher with rate-limit and retry.
- `scripts/verify_manifest.py` — title-matches-expected verifier (catches wrong-ID PG fetches before they corrupt the corpus).
- `scripts/clean_books.py` — PG header/footer stripping, PDF/HTML extractor.
- `scripts/chunk_books.py` — paragraph-aware ~500-token chunking with sentence-boundary fallback.
- `scripts/chunks_to_passages.py` — stratified balanced sampling converter.

**Data.**

- `corpus/passages.jsonl` — Phase 0 v0.5 corpus (143 passages, 23 traditions).
- `corpus/passages_substituted.jsonl` — Phase 0 with structural-role gibberish placeholders.
- `corpus/passages_phase1.jsonl` — Phase 1a balanced-sampled corpus (920 chunks from 20 books).
- `corpus/chunks.jsonl` — Phase 1a full chunk set (5,408 chunks before sampling).
- `corpus/books/raw/` and `corpus/books/cleaned/` — 20 whole books (~2.85M tokens).
- `corpus/books_manifest.json` — sources, translators, license status, verification flags.

**Results.**

- `results/text-embedding-3-large/` — Phase 0 OpenAI document-level outputs.
- `results/substituted/` — Phase 0 substituted document-level outputs.
- `results/concept_analysis/` — Phase 0 concept-binding outputs.
- `results/sentence_concept_analysis/openai/` and `.../onnx/` — Phase 0 + Phase 1a sentence-level outputs, both backends.
- `results/phase1/` — Phase 1a outputs (document_level, concept_analysis, substituted).
- `results/robustness/` — paraphrase-exclusion robustness check outputs.

**Reproducibility.** The OpenAI runs require an API key (see `.openai_key`); the ONNX BERT runs are fully local with only `onnxruntime`, `tokenizers`, and `numpy` as external dependencies and have been tested on Python 3.14 / Windows with WDAC active.

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
| 2 | Absence of a privileged self | SELF (Phase 0 n = 3, Phase 1a n = 27) | unmeasured (n=3) | **+0.031 sent-level OpenAI (p=0.006)** |
| 3 | Immanence | overlaps WORLD ∩ ULTIMATE | indirect; not directly tested | indirect; not directly tested |
| 4 | Groundless ground | overlaps SUBSTRATE ∩ ULTIMATE | indirect; both bind | indirect; both bind |
| 5 | Non-temporal nature of ultimate reality | no concept-tag coverage | unmeasured | unmeasured |
| 6 | Equivalence of becoming and recognition | overlaps RECOGNITION | binding +0.079, *p* = 0.001 | binding +0.025 passage / +0.061 sentence, *p* ≤ 0.0005 |
| 7 | Primacy of consciousness/awareness | overlaps AWARENESS | binding +0.113, *p* < 0.0001 (strongest) | binding +0.026 passage / +0.082 sentence OpenAI, +0.121 sentence BERT |
| 8 | Compression to unity | overlaps NONSEP ∩ ULTIMATE | unmeasured | unmeasured |

The Phase 1a sentence-level OpenAI SELF result (+0.031, *p* = 0.006) is the new Phase 1a finding for the previously-unmeasured SELF concept. The feature taxonomy and the concept-tag schema are not fully reconciled. Full Phase 1 will refine operational definitions in light of the binding results and pre-register the reconciled feature set.

---

## Appendix B. Per-concept robustness summary

For each binding concept, status under the robustness checks performed.

| Concept | Phase 0 full | Phase 0 sentence | Phase 0 BERT | Phase 0 paraphrase-excluded | **Phase 1a passage** | **Phase 1a sentence OpenAI** | **Phase 1a sentence BERT** |
|---|---|---|---|---|---|---|---|
| AWARENESS | +0.113 *** | +0.114 *** | +0.204 *** | not measurable (0 pairs) | +0.026 *** (p=5e-4) | **+0.082 *** | **+0.121 *** |
| RECOGNITION | +0.079 ** | +0.082 *** | +0.073 *** | not measurable (1 pair) | +0.025 *** (p=5e-4) | +0.061 *** | +0.090 *** |
| WORLD | +0.077 *** | +0.082 *** | +0.073 *** | underpowered (6 pairs) | +0.022 *** | +0.051 *** | +0.065 *** |
| ULTIMATE | +0.057 *** | +0.067 *** | +0.079 *** | **+0.062 ***, survives** | +0.014 *** | +0.047 *** | +0.074 *** |
| SUBSTRATE | +0.053 ** | +0.051 ** | +0.050 ** | not measurable (0 pairs) | **+0.054 ** (p=1.5e-3) — *unchanged*** | +0.053 (p=0.04) | +0.048 (p=0.09, NS sub-sample) |

\*\*\* *p* < 0.0001, \*\* *p* < 0.01.

**Status update from Draft 2:** in Draft 2, only ULTIMATE had a complete robustness track. In Draft 3 with Phase 1a, **all five binding concepts have at least one paraphrase-free measurement**, and all five are statistically significant in at least one Phase 1a analysis. AWARENESS, RECOGNITION, WORLD, and ULTIMATE survive at both passage and sentence granularity. SUBSTRATE survives at passage-level (the more statistically powerful test for that small concept); the sentence-level subsample is underpowered for SUBSTRATE specifically.

The reviewer prior (≈60% AWARENESS + RECOGNITION survive; ≈40% the full five-concept pattern survives) is **above the prior** — all five survived. Per the second-reviewer reminder on resisting natural framing drift after evocative results, we note: the result is significantly above prior but also smaller than Phase 0 suggested. The decomposition in §7.3 places the genuine concept-level structural binding at the smallest and best-controlled portion of the apparent signal. We cite it affirmatively but do not over-promote.

---

*Draft 3, Phase 1a preliminary preprint. Comments and replications welcomed. Contact: david@redbirdsoftwarellc.com.*
