# Concept-Conditional Cross-Tradition Convergence in Nondual Contemplative Literature: A First Empirical Test

**Preliminary preprint — Phase 0, draft 2**
**Date:** 2026-05-15
**Status:** Exploratory; not yet pre-registered. Findings are reported as a proof-of-concept and an invitation to replicate, not as final claims.

---

## Abstract

The cross-cultural convergence thesis in the study of mysticism — that contemplatives from unconnected traditions converge on a shared structural description of reality — has been debated qualitatively for sixty-five years (Stace, 1960; Katz, 1978; Forman, 1990) and tested empirically through survey instruments administered to contemporary respondents (Hood, 1975; Hood et al., 2001). To our knowledge, no published work performs a direct *textual* test using modern semantic embeddings on historical sources, with controls adequate to the constructivist critique. We report a first such test.

The primary result is a **concept-conditional cross-tradition binding analysis** on a 143-passage, 23-tradition corpus. Each passage is tagged for the structural concepts it explicitly mentions (drawn from a pre-registered glossary: AWARENESS, RECOGNITION, ULTIMATE, WORLD, SUBSTRATE, SELF, and an observer-substrate non-separation marker NONSEP). For each concept *C* we ask whether cross-tradition passage pairs that both mention *C* are more similar in embedding space than cross-tradition pairs that don't share *C*. Five of seven concepts show statistically significant binding under permutation testing on the unsubstituted corpus: AWARENESS (+0.113, *p* < 0.0001), RECOGNITION (+0.079, *p* = 0.001), WORLD (+0.077, *p* < 0.0001), ULTIMATE (+0.057, *p* < 0.0001), SUBSTRATE (+0.053, *p* = 0.01). The same five concepts bind across passage and sentence granularity and across two unrelated embedding models (OpenAI `text-embedding-3-large`, 3072-dim; `sentence-transformers/all-MiniLM-L6-v2`, 384-dim, via ONNX). Top tradition pairs replicate cross-model.

A document-level cross-cluster test recovers the classical perennialist signal at *p* < 0.0001 across three independent corpus revisions, but the same analysis shows that document-level embedding similarity is dominated by vocabulary and register: bridge thinkers (Bohm, Whitehead, Friston, Tononi/Koch, Rovelli) cluster decisively with the modern scientific cohort despite explicit engagement with contemplative content. We therefore treat the document-level result as a methodological cautionary tale and read the concept-conditional analysis as the primary test.

A robustness check restricted to the 46 corpus passages that are *not* pure paraphrases shows the document-level H1 signal surviving at *p* = 0.014 with an effect size approximately half that of the paraphrase-inclusive subset. Concept-binding on the non-paraphrase subset is only measurable for ULTIMATE (+0.062, similar to the full +0.057); the four other binding concepts do not have enough non-paraphrase coverage in the v0.5 corpus to be evaluated independently. This is the most serious load-bearing limitation of Phase 0 and the top Phase 1 priority.

We interpret these results cautiously. Translator-as-confound is currently unaddressed: all passages are English-translated by a small set of scholarly translators whose conventions may carry cross-tradition similarity that pre-dates any embedding analysis. Concept tagging is regex-based and derived from the same glossary that drove corpus design, so the "bias-free" framing of the concept-conditional analysis is partial rather than absolute. Selection bias in passage choice was guided by the investigator's prior model of what convergence looks like. None of these caveats invalidates the signal; all of them bound how strongly it should be cited.

Among individual pairings, when both passages discuss the substrate underlying appearance, Mahayana Buddhist sources and Rovelli's relational quantum mechanics bind at cosine 0.455. We note that Rovelli (2022) published an argument that these two frameworks make structurally identical claims and that his text is part of our corpus, so the binding confirms his qualitative claim is detectable rather than independently establishing the structural identity.

This is to our knowledge the first direct textual test of cross-tradition convergence using semantic embeddings on historical sources, and the first reported case where a pre-registered set of structural concepts produces statistically significant cross-tradition binding under controls adequate to identify and partially mitigate the shared-vocabulary artifact. We release the corpus, code, and full result tables under MIT license.

---

## 1. Introduction

### 1.1 The convergence question

Walter Stace's *Mysticism and Philosophy* (1960) introduced the modern form of the cross-cultural convergence claim: that introspective inquirers from culturally and historically unconnected traditions report a common structural description of reality — typically a non-separation of observer and observed, the absence of a privileged self, the primacy of awareness, and a unity beneath apparent multiplicity. Robert Forman (1990) extended the claim with the "pure consciousness event" thesis. Steven Katz (1978) led the constructivist counter: there is no unmediated experience; every mystical report is shaped by the conceptual context of its author, so apparent convergence is hermeneutic projection.

The debate has run for sixty-five years on largely textual and philosophical grounds. The empirical literature is dominated by Ralph Hood's Mysticism Scale (Hood, 1975), which operationalizes Stace's categories into a 32-item survey and has been cross-culturally validated against Christian, Muslim, and Hindu respondents (Hood et al., 2001; Anthony et al., 2010; Streib et al., 2020). Hood's work is genuine empirical leverage on a closely related question: it tests whether self-reports of mystical experience by *contemporary* respondents converge across cultures. It does not test whether the *historical texts* produced by unconnected contemplatives converge in semantic structure, because survey data and textual semantics are different objects and contemporary respondents share a globalized culture in ways the historical authors did not. A direct textual test using semantic embeddings on historical sources, with controls adequate to the constructivist critique, has not appeared in the published literature.

A recent ACL survey of NLP work on religious texts (Hutchinson et al., 2024) confirms the gap: the field has focused on machine translation (the Bible and Quran as parallel corpora) and intra-tradition topic modeling. Cross-tradition embedding-based comparison of contemplative literature is largely absent. The technical tools — modern dense embeddings, permutation testing, sparse interpretability methods — have matured over the last five years; the philosophical question has been waiting.

### 1.2 What this paper tests

We test one primary hypothesis and frame it carefully.

**Primary (concept-conditional).** For each of seven pre-registered structural concepts, cross-tradition passage pairs that both mention the concept are more similar in semantic embedding space than cross-tradition pairs that don't share the concept. This is the bias-aware version of the perennialist claim: not "everything converges" but "specific structural axes bind specific traditions when those traditions are discussing those axes."

We also report two secondary descriptive analyses:

**Document-level (classical H1).** Texts from unconnected historical nondual contemplative traditions are more similar to each other than to dualistic texts. This was the original framing in our pre-analysis design document, and we report it because the result is striking, but we treat it as a methodological cautionary tale: as §6 will show, document-level embedding similarity is dominated by register and vocabulary, and the same statistical method does not separate genuine structural agreement from those confounds.

**Extended document-level (H1').** Historical nondual texts and modern scientific/computational framings of structurally nondual claims (simulation theory, information physics, the mathematical universe hypothesis, analytic idealism, interface theory) form a unified cluster distinct from controls. We report this hypothesis as *falsified at the document level* — modern thinkers cluster decisively with their vocabulary cohort — but find that a weaker concept-level version of the same claim is supported: when conditioned on shared structural concepts, modern and historical wings do converge on specific axes.

### 1.3 What this paper does not claim, and what would still need work to claim

Nothing in this analysis bears on whether any cross-tradition structural convergence reflects:

(a) a shared truth about the structure of reality;
(b) a shared feature of human cognition under trained introspection;
(c) a shared feature of how literate contemplative cultures end up writing about introspection, independent of what they observe;
(d) a shared feature of how the small set of anglophone scholar-translators who produced our English source texts render contemplative content.

Distinguishing (a)–(d) is downstream of the empirical question we are answering, which is the prior question "is there any cross-tradition signal in textual embedding space beyond what shared vocabulary and shared register can explain?" Our affirmative answer to that question is necessary but not sufficient for any of (a)–(d), and we make no progress toward (a)–(d) here.

We will not claim that the perennialist thesis has been settled. We will not claim that the constructivist critique has been refuted; in fact, our findings show that vocabulary and register do substantial work in apparent document-level convergence, which is exactly what the constructivists predicted. We will claim, and only claim, that a concept-level structural signal beyond shared vocabulary is detectable, statistically significant under permutation, and replicated across embedding models and granularities. That claim is interesting because no prior empirical work has been able to formulate, let alone test, it.

---

## 2. Related work

### 2.1 The philosophical debate

Stace (1960) distinguishes *introvertive* mysticism (pure consciousness without content) from *extrovertive* mysticism (unity perceived in the phenomenal world) and argues both forms recur cross-culturally. Forman (1990, 1999) extends with the pure-consciousness-event thesis, which claims that contentless awareness is a cross-cultural phenomenon precisely because it has no content to be culturally shaped. Katz (1978) argues that every mystical experience is mediated by prior conceptual structure, so apparent cross-cultural convergence is the product of cross-cultural conceptual contamination. Forman's "decontextualism" attempts to identify experiences that escape Katzian mediation; Katzian "hard constructivism" denies such experiences exist.

The Stanford Encyclopedia of Philosophy entry on Mysticism (2025) characterizes the present state of the debate as unresolved on philosophical grounds, and its survey mentions no computational, NLP, or embedding-based methods applied to mystical literature.

Our methodology engages directly with the Katzian objection: vocabulary substitution (§6.6) tests for vocabulary-driven false convergence; concept-conditional binding (§6.1) tests for convergence at specific pre-registered structural axes rather than diffuse "they all sound similar" similarity; cross-model replication tests for embedding-model artifacts. We do not engage adequately with the strongest form of the Katzian objection — that translation conventions in anglophone scholarship may carry the convergence — and we flag this prominently as the load-bearing limitation of Phase 0 (§9).

### 2.2 The empirical psychology of mysticism

Hood (1975) introduced the Mysticism Scale (M-Scale), a 32-item self-report instrument with three confirmed factors (introvertive, extrovertive, interpretation) operationalizing Stace's categories. The M-Scale has been validated cross-culturally:

- Hood et al. (2001): US Christian (n=188) vs. Iranian Muslim (n=185); measurement invariance held across samples.
- Anthony et al. (2010): comparative study of Christian, Muslim, and Hindu students in Tamil Nadu, supporting cross-tradition similarity of reported mystical experience.
- Streib et al. (2020): comparative US/German short-form study, replicating the factor structure.

Hood's work is genuine empirical leverage on the convergence claim. It measures contemporary self-reports rather than historical texts, and its respondents share a globalized culture, but it is not philosophical argument and we do not characterize it as such.

### 2.3 NLP on religious texts

Hutchinson et al. (2024) survey the field. The vast majority of NLP work on religious texts treats them as parallel corpora for machine translation; some intra-tradition topic modeling exists (Wieringa on Seventh-day Adventist periodicals; Choiński & Rybicki on Puritan stylometry). No published cross-tradition embedding-based comparison of contemplative texts appears to exist. The methodological frontier is genuinely open.

### 2.4 Bridge thinkers and the modern wing

Several contemporary thinkers explicitly compare structurally nondual claims in modern scientific frameworks to historical contemplative claims. Bohm's *Wholeness and the Implicate Order* (1980) draws on his collaboration with Krishnamurti. Rovelli's *Helgoland* (2022) explicitly argues that relational quantum mechanics and Nagarjuna's emptiness doctrine make structurally identical claims. Kastrup (2019) defends analytic idealism in vocabulary continuous with Advaita Vedanta. Tononi and Koch (2015) develop integrated information theory with consciousness as fundamental. Hoffman (2019) defends interface theory of perception. Tegmark (2014), Bostrom (2003), Wheeler (1990), Susskind, Lloyd (2006), and others develop information-theoretic and computational ontologies that have been compared to nondual contemplative claims with varying rigor.

These authors function as a test case for our methodology. **Important caveat:** Rovelli's *Helgoland* is in the corpus and explicitly argues toward the Mahayana–relational-QM correspondence we report quantitatively in §6.1. The cosine-0.455 binding does not independently establish the structural identity; it establishes that an embedding model can detect the correspondence Rovelli argued for *given the text he wrote in service of arguing for it*. Independent establishment would require modern physics texts that did not write toward the comparison, which we do not have in the v0.5 corpus.

---

## 3. Corpus

### 3.1 Composition

The Phase 0 v0.5 corpus contains **143 English passages across 23 traditions in 3 categories**, distributed as follows.

**Historical contemplative nondual (n = 58):**

| Tradition | n | Era | Representative authors |
|---|---|---|---|
| Advaita Vedanta | 10 | 8c–20c | Shankara, Ramana Maharshi, Nisargadatta Maharaj |
| Dzogchen | 7 | 10c–contemporary | Longchenpa, Tilopa, modern teachers |
| Christian mystical | 10 | 5c–14c | Pseudo-Dionysius, Eckhart, John of the Cross |
| Sufi | 7 | 12c–13c | Ibn Arabi, Rumi (nondual selections) |
| Neoplatonism | 6 | 3c | Plotinus |
| Kabbalah | 6 | 13c–18c | Zohar, Tanya |
| Daoism | 6 | 4c BCE–5c CE | Zhuangzi, classical Daoist sources |
| Mahayana | 6 | 2c–8c | Heart Sutra, Diamond Sutra, Nagarjuna, Avatamsaka |

**Modern scientific/computational nondual (n = 25):** simulation theory (6), information physics (6), mathematical universe (5), analytic idealism (4), interface theory (4).

**Bridge thinkers (n = 24):** implicate order / Bohm (5), process philosophy / Whitehead (5), predictive processing / Friston, Clark, Seth (5), integrated information theory / Tononi, Koch (4), relational QM / Rovelli (5).

**Dualistic contemplative controls (n = 24):** Catholic scholastic (8), Theravada Abhidhamma (8), Kantian (8).

**Non-contemplative philosophy controls (n = 12):** Humean (6), analytic / Russell (6).

### 3.2 Source status: the paraphrase problem

Each passage carries a `source_status` field with three values:

- `quote` — high-confidence direct quotation from a published English source.
- `approximate` — close to a published quotation with possible minor wording variation.
- `paraphrase` — doctrinally faithful rendering of a recurring teaching, not lifted from a specific edition.

The v0.5 distribution is:

| Status | Count | Fraction |
|---|---|---|
| `quote` | 6 | 4.2 % |
| `approximate` | 40 | 28.0 % |
| `paraphrase` | 97 | 67.8 % |

**The corpus is dominated by paraphrases.** Each paraphrase was written or selected by the lead investigator with prior beliefs about what convergence looks like, which is a direct constructivist threat to the validity of any convergence measurement: if paraphrased content is encoded in vocabulary the investigator associates with structural agreement, an embedding model can recover that vocabulary alignment without anything real about cross-tradition structure being measured.

We address this directly with a paraphrase-exclusion robustness check (§6.3) and report the result honestly: the H1 signal survives non-paraphrase restriction at lower significance, and the concept-binding signal is testable on the non-paraphrase subset only for one of the five binding concepts. The paper does not claim more than that result supports.

### 3.3 Inclusion rationale

The historical nondual sources were selected for *cultural independence* — no plausible cultural contact at time of authorship between, e.g., 8th-century Advaita and 14th-century Rhineland mysticism, or between 3rd-century Plotinus and Tang-dynasty Chan Buddhism. The single notable exception is documented Andalusian Sufi/Kabbalist contact (12c–13c), which we re-flag at point of use in §6.1 wherever Kabbalah × Sufi appears in the top results.

Bridge thinkers were chosen because each writes with one foot in scientific vocabulary and one in contemplative content; the prediction was that if document-level convergence is content-driven, they sit between clusters. This prediction failed (§6.5), which is itself informative.

Dualistic controls test whether the convergence signal tracks "religious genre" or "contemplative-nondual content." Several traditions in this category are doctrinally complex — Theravada Abhidhamma is rigorously contemplative and asserts non-self while denying observer-substrate identification, so it sits on a doctrinal boundary the experimental design treats as binary. We discuss this in §7.

### 3.4 Selection bias and what would bound it

Passages were chosen by the lead investigator informed by secondary scholarship. The strongest single defense against selection bias — having a constructivist-leaning scholar independently select passages from the same authors that they consider *least* nondual, then re-running the analysis — was not done in Phase 0 and is the top non-paraphrase Phase 1 priority. We note where it would have changed our claims.

Several traditions have n < 8 passages (Neoplatonism, Daoism, Mahayana, Kabbalah at n = 6; Dzogchen and Sufi at n = 7). The most-cited individual cross-tradition pairings in §6 rest on small per-tradition samples; per-tradition bootstrap confidence intervals would be the right uncertainty measure for individual pair similarities and are deferred to Phase 1.

---

## 4. Methods

### 4.1 Embedding

Texts are embedded with two independent models:

- **OpenAI `text-embedding-3-large`** (3,072-dim, proprietary), via the OpenAI API.
- **`sentence-transformers/all-MiniLM-L6-v2`** (384-dim, open-source), via ONNX Runtime locally. ONNX inference was used because the local development environment is subject to Windows Defender Application Control, which blocks torch but admits the Microsoft-signed ONNX Runtime DLLs. The two models share no training data, architecture, or organization.

Embeddings are unit-normalized; pairwise similarity is cosine.

### 4.2 Concept tagging and the regex-as-hidden-degree-of-freedom caveat

The seven pre-registered structural concepts — ULTIMATE, SUBSTRATE, AWARENESS, WORLD, SELF, RECOGNITION, NONSEP — are tagged on each passage by a manually curated dictionary of case-insensitive regex patterns. The patterns are listed in full in `scripts/concept_analysis.py` and derived from the project glossary, which was constructed before the analyses and lists the tradition-specific terminology each concept was expected to be expressed in.

**This is a hidden degree of freedom.** The same person who built the glossary built the corpus. Patterns that fire on "consciousness," "awareness," "rigpa," "chit," "phi," "nous" reflect prior beliefs about which terms denote AWARENESS. A pattern set chosen by someone with a different model of convergence would tag different passages and could produce different binding scores. We therefore characterize the concept-binding analysis as **bias-free of the shared-placeholder substitution artifact** (which is the artifact it was designed to eliminate) rather than as **bias-free in the absolute sense** (which it is not). Held-out human-validated tagging on a randomly sampled subset is a Phase 1 priority.

### 4.3 Concept-conditional binding statistic

For each pre-registered concept *C*, restricted to cross-tradition passage pairs only:

$$
\text{binding}(C) = \overline{\text{sim}}\bigl(\text{pairs both mentioning } C\bigr) - \overline{\text{sim}}\bigl(\text{pairs where exactly one mentions } C\bigr)
$$

We compare against a permutation null in which concept-tag assignments are shuffled across passages (preserving the total count of tagged passages), 2,000 permutations. The reported *p*-value is the fraction of permutations whose binding statistic exceeds the observed value.

For sentence-level analysis, passages are split on punctuation, the same regex tagger is applied per sentence, and the same statistic is computed across sentences rather than passages.

### 4.4 Document-level statistic for the secondary descriptive analysis

For the document-level H1 (reported as a methodological cautionary tale in §6.4), we compute:

$$
\Delta_{H1} = \overline{\text{sim}}_{\text{historical-nondual cross-tradition}} - \overline{\text{sim}}_{\text{nondual-to-dualistic cross-tradition}}
$$

Significance is assessed by a 5,000-permutation test that shuffles (tradition, category) labels and recomputes the statistic. Effect-size language in this paper uses raw cosine differences and *p*-values. We avoid expressing effect sizes in "σ-above-null" units because the permutation null is non-parametric and readers from physics may mis-read such phrasing as Gaussian tail probability.

### 4.5 Vocabulary substitution and its known bias

For the substitution analysis (§6.6) we replace tradition-specific terms with role-based shared placeholders (`[qntrx]` for ULTIMATE, `[vpbkz]` for SUBSTRATE, `[mljfd]` for AWARENESS, etc.). This procedure has a **known bias toward finding cross-tradition similarity**: substituting distinct tradition-specific terms with a shared placeholder forces token-level similarity across substituted texts. The bias was identified by the lead investigator during the substitution run and is documented in `methodology-notes.md`. The substitution analysis is retained because the *failure* of the bias to fully close the modern–historical gap is itself informative, and because the H1 effect size in the substituted corpus is essentially identical to the unsubstituted result. The concept-conditional analysis on the unsubstituted corpus supersedes substitution as the canonical bias-corrected test of concept-level convergence.

### 4.6 Clustering and visualization

UMAP (n_neighbors=15, min_dist=0.1) and t-SNE (perplexity=30) are reported for descriptive purposes only. K-means and agglomerative clustering at k=3 with Adjusted Rand Index against the (nondual, dualistic, non-contemplative) labels are reported as cluster-recovery quality, again descriptive only; the primary tests are the explicit pairwise-similarity permutation tests, which are sensitive to signals that low-dimensional projection may obscure.

---

## 5. The translator-as-confound, named here rather than in future work

A single named limitation is sufficiently load-bearing to warrant its own section.

All 143 passages are in English regardless of the original language. A small set of anglophone scholar-translators is responsible for the great majority of the English-translation tradition for these texts. These translators have, over more than a century of comparative-religion scholarship, developed shared conventions for rendering tradition-specific contemplative vocabulary: how to translate Sanskrit *cit* and Pali *citta* and Tibetan *rigpa* and Greek *nous* and Arabic *qalb* and Hebrew *ruach* into English, how to handle apophatic constructions, how to phrase non-self formulations.

If these conventions converge — and there is no reason in principle they should not, given how much these scholars have read each other — then a portion of any cross-tradition similarity we measure is a property of the *English translation tradition*, not of the source texts. An embedding model cannot distinguish "Eckhart and Shankara are saying the same thing" from "Eckhart's translators and Shankara's translators are using the same English words to render different things."

**Phase 0 has no defense against this confound.** Vocabulary substitution partially addresses it by stripping the tradition-specific terminology that scholarly translators argue most about, but substitution introduces its own bias (§4.5) and does not affect the broader register and phrasing choices that translators converge on. Concept-conditional analysis partially addresses it by computing binding within concept categories rather than across the document, but the patterns used to tag concepts are themselves derived from scholarly translation conventions.

The proper defense is multi-translator inclusion: for each source where multiple English translations exist (and there are many — Eckhart has at least Walshe, McGinn, Smith; Plotinus has MacKenna, Armstrong, Gerson; the Heart Sutra has Conze, Red Pine, Tanahashi; Shankara has Madhavananda, Sastry, several others), the corpus should include all major translations and the analysis should report within-source translator variance as a baseline for between-source convergence. This is the largest single Phase 1 priority alongside replacing paraphrases with verified primary-source quotations.

We name this here, prominently, rather than in §9 (limitations) because it is the strongest constructivist objection to any positive convergence finding using textual data, and because Phase 0 simply has not addressed it. Readers should treat every Phase 0 result through this lens.

---

## 6. Results

### 6.1 Primary result: concept-conditional cross-tradition binding

For each pre-registered structural concept *C*, the concept-binding score on cross-tradition passage pairs using *unsubstituted* embeddings:

| Concept | n passages with *C* | both-have mean | one-has mean | **binding** | *p* (one-sided, 2,000 perms) |
|---|---|---|---|---|---|
| AWARENESS | 19 | 0.4195 | 0.3061 | **+0.1133** | **< 0.0001** |
| RECOGNITION | 9 | 0.3321 | 0.2528 | **+0.0793** | **0.001** |
| WORLD | 32 | 0.3752 | 0.2983 | **+0.0769** | **< 0.0001** |
| ULTIMATE | 36 | 0.3283 | 0.2712 | **+0.0571** | **< 0.0001** |
| SUBSTRATE | 10 | 0.3604 | 0.3078 | **+0.0526** | **0.01** |
| SELF | 3 | 0.2315 | 0.2890 | −0.0575 | 0.90 (NS) |
| NONSEP | 0 | n/a | n/a | n/a | not measurable |

**Five of seven pre-registered concepts show statistically significant cross-tradition binding.** The shared-placeholder substitution bias (§4.5) does not apply: no token sharing was forced. Effect sizes are substantial (≈ +0.05 to +0.11 in cosine similarity, on a base of ≈ 0.30 cross-tradition mean similarity).

Two non-significant results are corpus-limited: only 3 passages used explicit SELF markers (`atman`, `jiva`, `the agent`, `Markov blanket`) — most passages discuss self in unmarked English the regex tagger does not catch — and no passages used the explicit NONSEP labels (`nondual`, `advaita`, `wahdat al-wujud`) despite expressing observer-substrate non-separability throughout the nondual category. SELF and NONSEP are unmeasured in Phase 0 rather than refuted.

The strongest individual results within concepts:

**AWARENESS** (consciousness, awareness, rigpa, chit, phi, nous). Top cross-tradition pairs:

| Pair | mean similarity (both passages mention AWARENESS) |
|---|---|
| analytic_idealism × implicate_order | 0.624 |
| analytic_idealism × interface_theory | 0.585 |
| implicate_order × interface_theory | 0.561 |
| mahayana × theravada | 0.518 |
| analytic_idealism × iit | 0.511 |
| iit × implicate_order | 0.509 |

The modern wing dominates by volume, but Buddhist intra-Buddhist consciousness-talk (Mahayana × Theravada at 0.518) clusters as tightly as the modern thinkers do among themselves.

**RECOGNITION** (liberation, enlightenment, theosis, fana, gnosis, jnana). Top cross-tradition pairs:

| Pair | mean similarity |
|---|---|
| advaita × dzogchen | 0.528 |
| dzogchen × sufi | 0.440 |
| dzogchen × theravada | 0.439 |
| daoism × dzogchen | 0.438 |
| advaita × sufi | 0.429 |
| advaita × neoplatonism | 0.390 |

This is the Stace–Forman classical perennialist signal, quantitatively confirmed across historical contemplative traditions when those traditions are specifically discussing liberation/awakening. The pairs span eras and cultures with no plausible historical contact: 8th-century Advaita, 11th-century Dzogchen, 13th-century Sufism, 3rd-century Neoplatonism, 4th-century BCE Daoism, all converging on a recognizable conceptual axis. *Caveat: Sufi → Advaita is one of the pairs where translation-tradition convergence in anglophone scholarship (§5) is least mitigated.*

**SUBSTRATE** (emptiness, dependent origination, implicate order, integrated information, holographic). Top cross-tradition pairs:

| Pair | mean similarity |
|---|---|
| dzogchen × mahayana | 0.469 |
| mahayana × relational_qm | 0.455 |
| iit × implicate_order | 0.453 |
| dzogchen × relational_qm | 0.438 |
| dzogchen × implicate_order | 0.437 |

The Mahayana × relational_qm SUBSTRATE binding of 0.455 is the bias-free quantitative correlate of the structural correspondence Rovelli (2022) argued for qualitatively. **Important caveat reiterated from §2.4:** Rovelli's *Helgoland* is in the corpus, and the relational_qm passages were authored by him in service of arguing for the very correspondence we measure. The 0.455 binding confirms his argument is detectable by an embedding model that has read his argument; it does not independently establish the structural identity, because no relational-QM authors who were not writing toward this comparison are in the corpus. Reading the result as confirmation requires accepting the directionality.

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

### 6.2 Cross-model and cross-granularity replication

The concept-binding analysis is rerun at sentence granularity (322 sentences from the 143 passages, 123 sentences tagged with at least one concept) with both embedding models.

| Concept | OpenAI passage | OpenAI sentence | BERT (MiniLM) sentence |
|---|---|---|---|
| AWARENESS | +0.1133 *** | +0.1139 *** | **+0.2042 *** |
| RECOGNITION | +0.0793 ** | +0.0822 *** | +0.0725 *** |
| WORLD | +0.0769 *** | +0.0821 *** | +0.0733 *** |
| ULTIMATE | +0.0571 *** | +0.0668 *** | +0.0793 *** |
| SUBSTRATE | +0.0526 ** | +0.0514 ** | +0.0497 ** |

*** *p* < 0.0001, ** *p* < 0.01, all permutation tests.

**The five binding concepts replicate across both granularities (passage → sentence) and both embedding models (OpenAI 3072-dim, proprietary → MiniLM-L6-v2 384-dim, open-source).** Two embedding spaces with no shared architecture, training data, or organization, applied at two different granularities, agree on which structural concepts bind traditions, on the rank order of binding strength (AWARENESS strongest), and on the identity of the top tradition pairs within each concept.

AWARENESS binding is approximately twice as strong in the smaller BERT model. Plausible interpretation: MiniLM is more sensitive to lexical-structural cues from concept terms in its smaller embedding space, while the larger OpenAI model captures finer distinctions between different kinds of consciousness-talk that lower the average binding. The directional result is preserved.

The top tradition-pairs are essentially identical across models. For AWARENESS, both models place analytic_idealism × implicate_order at the top (Kastrup ↔ Bohm) and rank Buddhist-modern bridges via Theravada and Mahayana highly. For RECOGNITION, both models place advaita × dzogchen at the top. For SUBSTRATE, both models confirm mahayana × relational_qm.

### 6.3 Robustness check: does the signal survive paraphrase exclusion?

The paraphrase issue (§3.2) is potentially load-bearing. We rerun the headline statistics on three subsets of the corpus and compare.

| Subset | n passages | n historical-nondual cross-trad pairs | n nondual-to-dual pairs | mean nd cross | mean nd→du | Δ_H1 | *p* (5,000 perms) |
|---|---|---|---|---|---|---|---|
| Full corpus | 143 | 1461 | 1392 | 0.337 | 0.275 | **+0.062** | < 0.0001 |
| Quote-only | 6 | — | — | — | — | insufficient | — |
| Quote + approximate (non-paraphrase) | 46 | 374 | 210 | 0.314 | 0.274 | **+0.040** | **0.014** |
| Paraphrase-only | 97 | 331 | 476 | 0.371 | 0.287 | +0.084 | < 0.0001 |

**Findings.** Paraphrases roughly double the document-level H1 effect size (+0.084 vs +0.040), and the H1 signal does survive paraphrase exclusion at *p* = 0.014 with a smaller effect. This is partial confirmation of the reviewer concern: paraphrases are inflating the signal, but the signal is not entirely an artifact of paraphrases. The quote-only subset (n = 6 passages) is too small for a meaningful test in isolation.

Concept-binding on the same subsets:

| Concept | full | non-paraphrase (n_both, binding) | paraphrase-only |
|---|---|---|---|
| AWARENESS | +0.113 *** | (0 cross-trad both-have pairs) — not measurable | +0.103 *** |
| RECOGNITION | +0.079 ** | (1 pair, +0.022) — not measurable | +0.092 *** |
| WORLD | +0.077 *** | (6 pairs, +0.016) — too few | +0.063 *** |
| ULTIMATE | +0.057 *** | **(53 pairs, +0.062)** — survives | +0.051 *** |
| SUBSTRATE | +0.053 ** | (0 pairs) — not measurable | +0.039 |

**The only concept binding whose non-paraphrase survival can be evaluated in Phase 0 is ULTIMATE, where it survives unchanged (+0.062 vs +0.057 full).** Four of the five binding concepts (AWARENESS, RECOGNITION, WORLD, SUBSTRATE) have too few non-paraphrase passages mentioning them to evaluate cross-tradition binding without paraphrases. This is a serious gap and the top Phase 1 priority alongside translator multiplication: replacing paraphrases with verified primary-source quotations for the structural-concept-mentioning passages is what would convert these results from "supported in the full corpus but unverified on the verified-only subset" to "supported under the strongest available control."

We report this limitation directly because it is the test the reviewer flagged and because the answer is mixed. The H1 signal partially survives. One of five concept bindings survives evaluably. Four of five are currently unevaluable. The honest summary of Phase 0 is that the signal exists, the design exposes inflation, and a corpus with verified non-paraphrase coverage on concept-tagged passages is required for the stronger claim.

### 6.4 Document-level H1 (cautionary descriptive result)

| Statistic | v0 (n=107) | v0.5 (n=143) | v0.5-substituted (n=143) |
|---|---|---|---|
| historical-nondual cross mean | — | 0.315 | 0.336 |
| nondual_to_dualistic mean | — | 0.270 | 0.292 |
| observed Δ_H1 | +0.047 | +0.045 | +0.044 |
| permutation null mean | −0.008 | −0.008 | −0.008 |
| one-sided *p* (5,000 perms) | < 0.0001 | < 0.0001 | < 0.0001 |

The classical document-level perennialist signal replicates across three independent runs and survives the shared-placeholder substitution (note: §4.5 explains why substitution survival is weak evidence). Dualistic-religious traditions exhibit lower within-category cohesion (0.296) than nondual traditions exhibit cross-tradition (0.315), which is the standard check against "all religious-sounding language clusters together."

**We treat this as a cautionary tale rather than the main result**, for three reasons developed in §6.5–§6.6:

1. Bridge thinkers cluster decisively with their vocabulary cohort rather than their content cohort.
2. Vocabulary substitution closes only a fraction of the modern–historical gap.
3. The concept-conditional analysis (§6.1) provides a sharper test that is partially robust to vocabulary and register effects.

The document-level result is a successful sanity check that *something* is in the data, but it is not the right test for the question that matters. The headline concept-conditional analysis is.

### 6.5 The bridge-thinker design and what it teaches

UMAP projection of v0.5 embeddings shows three macro-clusters: historical contemplative nondual; modern scientific/computational nondual + bridge thinkers; dualistic + analytic controls. Bridge thinkers (Bohm, Whitehead, Friston/Clark/Seth, Tononi/Koch, Rovelli) were chosen as a critical test: if document-level convergence is content-driven, they sit between the modern and historical clusters; if vocabulary-driven, they sit with their vocabulary cohort.

| Bridge thinker | mean sim to historical-nondual | mean sim to modern-computational | gap (h − m) |
|---|---|---|---|
| Bohm | 0.315 | 0.403 | −0.088 |
| Whitehead | 0.296 | 0.394 | −0.098 |
| Friston/Clark/Seth | 0.210 | 0.352 | −0.142 |
| Tononi/Koch | 0.255 | 0.426 | −0.171 |
| Rovelli | 0.282 | 0.415 | −0.133 |

**Every bridge thinker clusters with the modern cohort at the document level**, including Bohm (who explicitly developed his thinking with Krishnamurti) and Rovelli (who explicitly argued the Mahayana correspondence we measure in §6.1). This is a clean falsification of H1' *as originally formulated* — modern scientific framings of nondual structure do not form a unified cluster with historical contemplative nondual texts at the document level.

The reconciliation with the concept-binding result is straightforward: document-level embedding similarity attends to everything in the passage — the technical apparatus, citation patterns, academic register, syntactic structure — and these features dominate the similarity computation. Conditioning on a shared concept focuses the comparison on the content that the concept-bearing context contributes, and convergence becomes visible. The Mahayana × relational_qm document-level similarity is 0.327 (modest); their SUBSTRATE-conditioned similarity is 0.455 (high). The same texts, the same model, two different statistics, two different answers.

The **weaker concept-level version of H1'** — that modern and historical wings converge on specific shared structural axes when conditioned on those axes — is supported, with the caveats from §6.1.

### 6.6 Vocabulary substitution: partial closure, biased measurement

We retain the vocabulary-substitution analysis from earlier Phase 0 work because the *direction* of the result remains informative even given the bias. Substituting tradition-specific terms with shared placeholders raises every cross-similarity by roughly 0.015–0.030 (an artifact of forced placeholder sharing). The modern × historical similarity rises by 0.030, slightly more than the across-the-board lift, suggesting that some genuine content convergence was being masked by vocabulary. But the bulk of the gap remains: the modern cluster's within-similarity (0.468) is still well above its similarity to the historical cluster (0.304). The vocabulary share of the modern–historical gap is best estimated at 15–30%, with the true value almost certainly below the upper bound given the shared-placeholder bias.

Individual pairs that **converge** under substitution are candidates for genuine vocabulary-masked content convergence: simulation_theory × analytic_idealism (+0.049), simulation_theory × advaita (+0.039), iit × mahayana (+0.031). Individual pairs that **diverge** under substitution are candidates for vocabulary-driven false convergence: mahayana × theravada (−0.014) (shared Buddhist vocabulary), mahayana × relational_qm (−0.011) (Rovelli's explicit Nagarjuna naming removed). Substitution does not transmute dualism into nondualism: Aquinas's structural claim "[ULTIMATE] is not the world; the world is a [WORLD] distinct from its Creator" survives substitution as a structural assertion of distinction.

The substitution analysis is consistent with the concept-conditional result but is a noisier and more biased estimator of the same underlying signal. The concept-conditional analysis is preferred.

---

## 7. Discussion

### 7.1 What is supported

A concept-level structural signal beyond shared vocabulary is detectable in textual embedding space and is replicated across two unrelated embedding models and two granularities. Five of seven pre-registered concepts bind cross-tradition pairs at *p* ≤ 0.01: AWARENESS, RECOGNITION, WORLD, ULTIMATE, SUBSTRATE. The classical Stace–Forman RECOGNITION signal across historical contemplative traditions (Advaita ↔ Dzogchen ↔ Sufi ↔ Daoism ↔ Neoplatonism) is the cleanest quantitative correlate of what the perennialist tradition has argued for qualitatively for sixty-five years.

The document-level Δ_H1 result is robust enough to survive paraphrase exclusion at *p* = 0.014 with a smaller effect, indicating the signal is not exclusively an artifact of investigator-authored paraphrases.

One pre-registered concept binding (ULTIMATE) survives paraphrase exclusion essentially unchanged (+0.062 vs +0.057 full).

### 7.2 What is not supported or not yet testable

H1' as originally formulated — that modern scientific framings and historical contemplative texts form a single unified cluster at the document level — is falsified. Bridge thinkers, including those who explicitly argue cross-period structural correspondences, cluster decisively with their vocabulary cohort at the document level. A weaker concept-level version of H1' is supported by §6.1, with the caveats from that section.

Four of five concept bindings (AWARENESS, RECOGNITION, WORLD, SUBSTRATE) cannot currently be evaluated on the non-paraphrase subset of the corpus due to insufficient non-paraphrase coverage of concept-mentioning passages. This does not falsify them — the full-corpus binding remains the headline result — but it does mean that the strongest available robustness check has only been passed for ULTIMATE.

The translator-as-confound (§5) is unaddressed in Phase 0. Every signal reported here is consistent both with structural convergence in source content and with shared scholarly translation conventions, and Phase 0 cannot distinguish.

The Rovelli–Nagarjuna binding does not independently establish the structural correspondence; it confirms that an embedding model can detect the correspondence Rovelli argued for, given his text in the corpus.

### 7.3 The decomposition that is defensible

The honest current picture decomposes apparent cross-tradition similarity into:

1. **Concept-level structural binding** on five pre-registered axes, detectable in *p* ≤ 0.01 binding scores, replicated cross-model, partially (1/5) verified paraphrase-free. This is the part of the convergence picture that survives the controls Phase 0 was able to apply.

2. **Document-level vocabulary effect**, partially closed by substitution (~15–30% of the modern–historical gap, upper-bounded by the shared-placeholder bias). Vocabulary matters, exactly as constructivists predicted.

3. **Document-level register and style effect** (~50–70% of the modern–historical gap), not closed by current methods, plausibly the dominant factor in document-level cluster separation.

4. **Translator-tradition effect** (unbounded in Phase 0), likely material, requires multi-translator inclusion to estimate.

5. **Paraphrase-author effect** (partially bounded by §6.3), inflates the H1 effect roughly 2× but does not invent it from nothing.

6. **Genuine content difference** between modern computational nondualism and historical contemplative nondualism (probably real and small), most plausibly representing differences in level of description: the moderns reason about substrate, information, computation; the historical contemplatives report about awareness, perception, recognition.

The Phase 0 result is consistent with this decomposition. Each component is bounded above by what its applicable control measures and bounded below by zero. The signal-of-interest — (1), genuine concept-level convergence — is the smallest and best-controlled component, and is the only one we cite affirmatively.

### 7.4 What we are not claiming and what would still need work to claim

Per §1.3, no result here distinguishes among the four interpretations: shared truth about reality, shared cognitive feature of trained introspection, shared writing convention of literate contemplative cultures, or shared translation convention of anglophone scholars. We make no progress toward any of these and do not gesture at any of them.

The reviewer concern that the paper "sits awkwardly between disciplines" is well-taken. We have written a methodologically-careful paper aimed at NLP and computational humanities readers; comparative religion scholars will want more philological care and more direct engagement with Katz beyond a single paragraph; philosophy of mind readers will want either the metaphysical interpretation pursued or more firmly disowned. Future drafts targeted at specific venues should adapt accordingly.

---

## 8. Methodological lessons for Phase 1

Phase 0 has produced both substantive findings and methodological discoveries that should shape Phase 1.

- **Document-level embedding similarity is inadequate** for testing cross-tradition structural convergence when the corpus mixes registers. Concept-conditional similarity is the appropriate bias-aware alternative.
- **Shared-placeholder vocabulary substitution introduces a tautological similarity bias.** Per-tradition placeholders or mask-and-compare schemes should replace shared placeholders.
- **Sentence-level granularity** preserves the signal and in some cases sharpens it. Token-level extraction of contextualized embeddings (extractable from ONNX BERT pipelines) is the natural next refinement.
- **Cross-model replication** is cheap and should be the default. The OpenAI run cost dollars; the ONNX BERT run was free and ran on a Windows machine with torch blocked by Application Control, sidestepped via Microsoft-signed ONNX Runtime DLLs.
- **Regex-based concept tagging** is reproducible and pre-specifiable but is a hidden degree of freedom. Phase 1 should add learned concept taggers and human-validated tags on a held-out sample.
- **Sparse autoencoder probes** of the embedding space (planned for Phase 1) should identify interpretable structural axes that survive both vocabulary and register noise, complementing the regex-based concept analysis.

---

## 9. Limitations

Named explicitly because the work is exploratory and the substantive claims, if taken further than we take them here, would be large.

1. **Translator-as-confound.** All passages English-translated by a small set of anglophone scholar-translators with shared conventions. See §5. The largest single unaddressed threat to validity in Phase 0. Multi-translator inclusion is the top Phase 1 priority alongside (2).
2. **Paraphrase dominance.** 68 % of v0.5 passages are paraphrases written or selected by the lead investigator with prior beliefs about convergence. The robustness check (§6.3) partially mitigates this for the H1 result but leaves four of five concept-binding signals untestable on the non-paraphrase subset. Verified primary-source quotation is the second top Phase 1 priority.
3. **Selection bias.** Passages were chosen by the lead investigator informed by secondary scholarship; an adversarial inclusion process (a constructivist-leaning scholar independently selecting *least-nondual* passages from the same authors) was not performed.
4. **Regex concept tagging.** Patterns derive from a glossary the lead investigator built before the analyses. The concept-conditional analysis is bias-free *of the shared-placeholder artifact*, not bias-free *in the absolute*. Held-out human-validated tagging is required for the stronger claim.
5. **Small per-tradition n.** Several traditions have n < 8 passages. Per-tradition bootstrap confidence intervals on top cross-tradition pair similarities should be computed in Phase 1; we have not computed them in Phase 0, and individual pair numbers (e.g., Mahayana × Relational QM SUBSTRATE = 0.455) should be cited as point estimates from underpowered subsamples.
6. **Single language.** All passages in English. See §5.
7. **Single non-Rovelli relational-QM source absent.** The Mahayana × Relational QM result depends on text Rovelli wrote in service of arguing for the correspondence. Independent confirmation requires modern physics texts that did not write toward the comparison.
8. **No formal pre-registration.** Pre-registered candidate concepts were specified before the analyses, but the corpus composition, statistical tests, and decision rules were not committed to an OSF pre-registration. Phase 1 must remedy this.
9. **Naive sentence splitting.** Punctuation-based, adequate for the short well-formed passages here but inadequate for the longer texts a Phase 1 whole-book corpus would include.
10. **No interpretability layer.** We have established that concepts bind traditions but have not characterized *what structural feature* the binding measures beyond the regex patterns used to detect it. Sparse autoencoder probes and contrastive direction analysis are deferred to Phase 1.
11. **No adversarial controls.** Synthetic mystical writing generated by language models in the style of each tradition is the natural adversarial test (real cross-tradition clustering should be tighter than synthetic clusters; otherwise the convergence is "stylistic mysticism" rather than structural agreement). Not run in Phase 0.

---

## 10. Future work

The Phase 0 findings define a concrete Phase 1 program.

**Top priorities (load-bearing).**

- Multi-translator inclusion for every source with multiple English translations available. Within-source translator-variance baseline becomes the denominator for between-source convergence.
- Verified primary-source quotations replacing all paraphrases, especially for concept-tagged passages. The corpus-construction pipeline currently under development (`corpus/books_manifest.json`, `scripts/fetch_books.py`, `scripts/chunk_books.py`) targets whole-book sources for Phase 1.
- OSF pre-registration of corpus, pipeline, tests, and decision rules.

**Methodological controls.**

- Per-tradition or mask-and-compare placeholder schemes to replace shared-placeholder substitution.
- Adversarial synthetic texts.
- Style-normalized rewrites (LM-mediated, lossy but tractable) to test the style-and-register share of the modern–historical gap.
- Held-out human-validated concept tagging.
- Adversarial inclusion: constructivist-leaning scholar independently selects least-nondual passages from the same authors.

**Interpretability.**

- Sparse autoencoder probes on the embedding space.
- Contrastive direction extraction within and across traditions.
- Token-level contextualized embeddings comparing concept terms in context across traditions.

**Generalization to other claimed convergent concepts.** The methodology is concept-agnostic. Candidate concepts for separate convergence tests on the same framework include the Golden Rule, the Hero's Journey, non-attachment, the ineffability of the ultimate, the dependence of perception on the perceiver, mystical death and rebirth, eternal recurrence, the great chain of being, the threefold path. The deliverable from running the framework on a suite of candidates is a *meta-table*: for each tested concept, was convergence detected? With what controls? What survived? The meta-table is what would move the perennialism debate forward as a field, not a single positive result on nondualism.

---

## 11. Code and data availability

All code, corpus, results, and methodology documents are MIT-licensed and version-controlled. The repository is structured for independent reproduction.

- `scripts/concept_analysis.py` — concept-conditional binding (primary analysis).
- `scripts/sentence_concept_analysis.py` — sentence-level concept binding, OpenAI and ONNX BERT backends.
- `scripts/onnx_embedder.py` — local BERT-class inference via ONNX Runtime.
- `scripts/prototype.py` — document-level embedding, clustering, visualization.
- `scripts/substitute.py` — structural-role vocabulary substitution.
- `scripts/robustness_paraphrase.py` — paraphrase-exclusion robustness check used in §6.3.

The OpenAI run requires an API key; the ONNX BERT run is fully local with only `onnxruntime`, `tokenizers`, and `numpy` as external dependencies.

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

Wheeler, J. A. (1990). Information, physics, quantum: The search for links. In W. H. Zurek (Ed.), *Complexity, Entropy, and the Physics of Information* (pp. 309–336). Addison-Wesley.

---

## Appendix A. Pre-registered candidate features and current status

The seven candidate structural features were specified in `glossary.md` before any analysis. Their concept-tag counterparts are the categories in §4.2.

| # | Feature | Concept tag overlap | Phase 0 status |
|---|---|---|---|
| 1 | Observer-substrate non-separability | NONSEP (no explicit-label coverage) | unmeasured |
| 2 | Absence of a privileged self | SELF (n = 3) | unmeasured |
| 3 | Immanence | overlaps WORLD ∩ ULTIMATE | indirect; not directly tested |
| 4 | Groundless ground | overlaps SUBSTRATE ∩ ULTIMATE | indirect; both bind |
| 5 | Non-temporal nature of ultimate reality | no concept-tag coverage | unmeasured |
| 6 | Equivalence of becoming and recognition | overlaps RECOGNITION | binding +0.079, *p* = 0.001 |
| 7 | Primacy of consciousness/awareness | overlaps AWARENESS | binding +0.113, *p* < 0.0001; strongest signal |
| 8 | Compression to unity | overlaps NONSEP ∩ ULTIMATE | unmeasured |

The feature taxonomy and the concept-tag schema are not fully reconciled. Phase 1 will refine operational definitions in light of the binding results and pre-register the reconciled feature set.

---

## Appendix B. Per-concept robustness summary

For each binding concept, status under the robustness checks performed in Phase 0.

| Concept | Full-corpus | Sentence-level | Cross-model (BERT) | Paraphrase-excluded |
|---|---|---|---|---|
| AWARENESS | +0.113 *** | +0.114 *** | +0.204 *** | not measurable (0 pairs) |
| RECOGNITION | +0.079 ** | +0.082 *** | +0.073 *** | not measurable (1 pair) |
| WORLD | +0.077 *** | +0.082 *** | +0.073 *** | underpowered (6 pairs) |
| ULTIMATE | +0.057 *** | +0.067 *** | +0.079 *** | **+0.062, survives** |
| SUBSTRATE | +0.053 ** | +0.051 ** | +0.050 ** | not measurable (0 pairs) |

ULTIMATE is currently the only concept with a complete robustness track: significant in the full corpus, replicated at sentence-level, replicated cross-model, and surviving paraphrase exclusion. The remaining four bindings are well-supported within the full corpus and replicated cross-model and cross-granularity, but their paraphrase-free survival is a Phase 1 question.

---

*Draft 2, Phase 0 preliminary preprint. Comments and replications welcomed. Contact: david@redbirdsoftwarellc.com.*
