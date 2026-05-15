# Literature Review: Prior Work on the Convergence Question

A scan of existing literature for work resembling Experiment 1. Useful for positioning the project, identifying methodological precedents, and confirming the gap we're trying to fill.

## Bottom line

**There is no published computational test of cross-tradition convergence on mystical/contemplative texts using modern NLP embeddings.** The convergence question has been debated philosophically for ~70 years and tested empirically through *survey instruments on living people*, but a direct textual test using semantic embeddings of historical sources across unconnected traditions does not appear to exist. This is a real gap, not a saturated field.

## The philosophical debate (foundational, qualitative)

The convergence claim was systematized by **Walter Stace** in *Mysticism and Philosophy* (1960). Stace distinguished:
- **Introvertive mysticism** — pure consciousness, unity without content, absorption
- **Extrovertive mysticism** — unity *in* the world, all-is-one perception of phenomena

He argued these forms recur cross-culturally, providing the original "common core" thesis.

**Steven Katz** opened the constructivist counter-attack in *Mysticism and Philosophical Analysis* (1978). His thesis: there is no unmediated experience; every mystical experience is shaped by the mystic's cultural and conceptual background. Apparent convergence is hermeneutic projection.

**Robert Forman** countered with the "pure consciousness event" thesis (*The Problem of Pure Consciousness*, 1990; *Mysticism, Mind, Consciousness*, 1999): there are forms of contemplative experience without conceptual content, and these can converge across traditions because they have no traditional content to be shaped by.

The debate split into:
- **Hard constructivism** (Katz): culture fully determines content
- **Soft constructivism**: culture shapes but does not determine
- **Decontextualism / perennialism** (Forman, Stace): a core experience is cross-culturally real

The Stanford Encyclopedia entry on Mysticism (2025 edition) summarizes the current state. Crucially, its survey of the field **contains no mention of computational, NLP, or embedding-based methods** applied to mystical literature. This represents an open methodological frontier.

## Empirical psychology of mysticism (survey-based)

The most important empirical contribution to the convergence question is **Ralph Hood's Mysticism Scale (M-Scale)**, developed in 1975 and extensively validated since.

The M-Scale operationalizes Stace's categories into a 32-item survey, with three confirmed factors:
1. **Introvertive mysticism**
2. **Extrovertive mysticism**
3. **Interpretation** (how subjects frame the experience)

**Cross-cultural validation studies:**
- Hood, Ghorbani et al. (2001): US Christians (n=188) vs. Iranian Muslims (n=185). Confirmatory factor analysis. Measurement invariance held; only the covariance between introvertive and extrovertive factors varied. Supports Stace's claim that a common phenomenology defines the core mystical experience.
- Streib, Klein, Hood et al.: US vs. Germany comparative study; M-Scale predicts subjective spirituality across both samples.
- Anthony et al. (2010): Comparative study of Christian, Muslim, and Hindu students in Tamil Nadu — supports cross-tradition similarity of mystical experience.
- A short-form 8-item version exists (Streib et al., 2020) for inclusion in larger surveys.

**Key implication for our project:** Hood's work supports the convergence hypothesis using *survey data from contemporary respondents*. Our project tests an adjacent but distinct claim: do the *texts* produced by historical contemplatives across unconnected traditions converge in semantic structure? Survey validation is necessary but not sufficient — contemporary respondents share a globalized culture in ways historical authors did not. The textual test is harder and more rigorous.

## NLP on religious texts (mostly orthogonal)

A 2024 ACL Findings paper, ["Modeling the Sacred: Considerations when Using Religious Texts in Natural Language Processing"](https://arxiv.org/html/2404.14740v3) (Hutchinson et al.), surveys the field. Key findings:

- The vast majority of NLP work on religious texts uses the **Bible and Quran**, primarily for **machine translation and parallel corpora** (e.g., JW300 covers 300 languages; MADLAD-400 has Bible data in 141 languages).
- Almost no work treats religious texts as objects of comparative analysis in their own right.
- The paper does **not identify any work on cross-tradition clustering or embedding-based comparison of contemplative texts specifically.**
- Raises important ethical considerations: data provenance, power asymmetries, marginalized community concerns. We should attend to these.

**Other NLP-on-religion work** (digital humanities side):
- Topic modeling has been used on individual traditions (Wieringa on Seventh-day Adventist periodicals; Choiński & Rybicki stylometric analysis of Puritan sermons).
- Network analysis of religious correspondence (Handelman on Rosenzweig).
- These remain *intra-tradition* rather than *cross-tradition*.

## Adjacent computational methods (relevant precedents)

- **Sentence-BERT and modern embedding models** (Reimers & Gurevych, 2019; subsequent work) provide the technical machinery. BERTopic and similar pipelines for embedding-then-clustering are mature.
- **Text Clustering with Large Language Model Embeddings** (arxiv 2024) shows current state-of-the-art for cluster discovery in semantic space.
- **Cross-lingual alignment** methods are well-developed, though we'll mostly work with English translations.

## What's been done with multilingual / classical texts

- Multilingual BERT has been used on parallel Sanskrit/English Ramayana texts to confirm semantic alignment across translation (relevant: shows our methodology is sound, but the task is intra-source rather than cross-tradition).
- Sentiment analysis on classical Chinese literature using BERT + GAT + k-means (relevant methodology, different goal).

## The gap, named precisely

Three claims have been thoroughly investigated and three have not:

| Claim | Status |
|---|---|
| Mystical experiences described by *living respondents* converge across cultures (survey) | Investigated: Hood et al., support for Stace |
| Mystical experiences are *culturally constructed* (philosophical argument) | Debated extensively: Katz vs. Forman |
| Common phenomenological structure exists (philosophical analysis) | Debated extensively: Stace, Forman, et al. |
| **Mystical *texts* from unconnected historical traditions converge in semantic embedding space, beyond translator/vocabulary artifacts** | **No published work found** |
| **The convergent structure (if it exists) can be characterized via interpretable axes (SAE probes, contrastive directions)** | **No published work found** |
| **Convergent features survive vocabulary substitution and adversarial-synthetic-text controls** | **No published work found** |

The methodological tools to test these claims have only been mature for ~3-5 years (modern dense embeddings, sparse autoencoders, adversarial generation with LMs). The field has not yet caught up.

## How this positions Experiment 1

- **Not duplicating prior work.** The closest precedent (Hood's survey work) tests a different but supportive claim.
- **Theoretically well-grounded.** Stace's introvertive/extrovertive distinction and Forman's PCE thesis provide pre-registered candidate features. We can phrase our pre-registered features to map onto these existing categories where relevant.
- **Methodologically novel.** Applying SBERT-class embeddings + interpretability techniques (SAEs, contrastive vectors) + adversarial synthetic controls to the perennialism/constructivism debate is a fresh combination.
- **Citable and defensible.** We can place the work in dialogue with both the philosophical literature (Stace–Katz–Forman) and the psychological literature (Hood et al.), giving the project a clear scholarly home.
- **Reaches an audience.** Religion-studies academics will recognize the question; NLP/ML academics will recognize the methods; philosophy-of-mind academics will care about the implications. Multi-audience papers are higher-impact.

## Risks the literature highlights

1. **Constructivist critique.** Katz's argument applies to our experiment too: if traditions are described in translated English using vocabulary that's been cross-pollinated by centuries of comparative religion scholarship, the corpus may bake in convergence we didn't put there. **Mitigation:** vocabulary substitution test; multiple translators; explicit attention to translator era and provenance.

2. **Ethical and representational concerns.** "Modeling the Sacred" raises legitimate issues about treating religious texts as data. **Mitigation:** treat the texts with care; acknowledge tradition perspectives in writeups; consider community engagement for the rigorous v1 version.

3. **Translator-as-confound.** The largest single threat to the experiment's validity. The English-language scholarly tradition has translation conventions that may produce convergence at the surface level. **Mitigation:** multi-translator inclusion where possible; translator-shuffled control analyses.

4. **Selection bias in corpus.** What counts as "nondual" is itself contested. **Mitigation:** lean on secondary scholarship for inclusion decisions; document criteria; consider sensitivity analyses where borderline texts are moved between categories.

## References to acquire and read

Priority for refining Experiment 1 design:

- Stace, *Mysticism and Philosophy* (1960) — foundational
- Katz, ed., *Mysticism and Philosophical Analysis* (1978) — the constructivist challenge
- Forman, *The Problem of Pure Consciousness* (1990); *Mysticism, Mind, Consciousness* (1999)
- Hood, "The Construction and Preliminary Validation of a Measure of Reported Mystical Experience" (1975)
- Hood et al., "Dimensions of the Mysticism Scale: Confirming the Three-Factor Structure in the United States and Iran" (*Journal for the Scientific Study of Religion*, 2001)
- Streib, Klein, Keller, Hood, "The Mysticism Scale as a Measure for Subjective Spirituality" (2020)
- Hutchinson et al., "Modeling the Sacred" (ACL Findings 2024)
- Stanford Encyclopedia of Philosophy, "Mysticism" (Fall 2025 entry) — current state-of-debate

## Sources

- [Modeling the Sacred (ACL 2024)](https://arxiv.org/html/2404.14740v3)
- [Stanford Encyclopedia of Philosophy: Mysticism (Fall 2025)](https://plato.stanford.edu/archives/fall2025/entries/mysticism/)
- [Hood et al., Dimensions of the Mysticism Scale (2001)](https://nimaghorbani.com/wp-content/uploads/2018/08/Dimensions-of-the-Mysticism-Scale-2001.pdf)
- [Mysticism Scale (Bielefeld)](https://www.uni-bielefeld.de/fakultaeten/theologie/cirrus/forschung/streib/methode-development/mysticism-scale/)
- [Streib et al., M-Scale as Measure for Subjective Spirituality](https://link.springer.com/chapter/10.1007/978-3-030-52140-0_19)
- [Forman, The Construction of Mystical Experience (PhilPapers)](https://philpapers.org/rec/FORTCO-6)
- [Interpreting Mysticism: Evaluation of Katz's Argument (Academia.edu)](https://www.academia.edu/459264/Interpreting_Mysticism_An_Evaluation_of_Steven_T_Katzs_Argument_Against_a_Common_Core_In_Mysticism_and_Mystical_Experience)
- [Anthony et al., Comparative Mystical Experience Tamil Nadu (2010)](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-5906.2010.01508.x)
