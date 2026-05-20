# Phase 2a Design Sketch: Multi-Language Translation Triangulation

**Date:** 2026-05-20
**Status:** **Design sketch, not pre-registration.** A formal pre-registration (`findings/phase2a-preregistration.md`) with specific predictions, decision rules, and per-language resolution gates will be authored and externally timestamped before any Phase 2a main analysis.
**Author:** T. David Kinlaw
**Supersedes:** the earlier `phase1d-design-sketch.md` (renamed — see §0).

---

## 0. Why this is Phase 2, not Phase 1d

Phase 1 (1a verified whole-book text, 1b multi-translator variance, 1c original-language) was one kind of thing: stress-testing CCB by improving the corpus, each step asking "does the signal survive a better corpus?" Phase 1c hit a wall — current multilingual embedding models cannot resolve fine-grained concept structure in classical Sanskrit/Pali (the within-language diagnostic: 6/7 concepts resolve in English, 2/7 in Sanskrit, failing on the headline AWARENESS/RECOGNITION; `findings/phase1c-multilingual.md` §7c).

Phase 2a is a different kind of thing: it embeds CCB inside a larger **multi-method causal-inference architecture** to answer a specific question — *is the cross-tradition convergence measured in Phase 1a/1b a translation-tradition artifact, or does it reflect source content?* This is a methodological level-up (CCB becomes a measurement instrument within a convergent-validity design), so it warrants a new phase.

## 1. The design: independent translation communities as independent measurement methods

Translate both traditions (Advaita Hindu, Theravada Buddhist) into multiple **high-resource modern languages** the embedding model resolves well, by **independent translator communities**, and compare cross-tradition CCB across them.

The logic is convergent validity / the multitrait-multimethod (MTMM) matrix. Each target language is a *method* with its own *method-variance* (that community's translation conventions, lexical norms, interpretive frame). The cross-tradition structural convergence is the *trait*. A trait that appears across methods with independent error sources is trait variance, because independent methods do not share a bias to manufacture the same convergence.

### 1.1 Variance-components structure (why ≥2 languages per cluster)

With only English representing the "Western" cluster, a Western-vs-non-Western finding is confounded with English-specific idiosyncrasy — you cannot separate "the Western interpretive tradition causes this" from "English happens to do this." Replication *within* each cluster separates three variance sources:

1. **Trait variance** — the cross-tradition convergence itself (the target)
2. **Cluster variance** — the translation-tradition effect (the constructivist's claim)
3. **Language-specific variance** — individual idiosyncrasy

Decisive pattern: if within-cluster agreement is high, between-cluster difference is large → a real cluster effect (constructivism). If within-cluster spread ≈ between-cluster spread → no coherent tradition effect; each language is idiosyncratic, which argues *against* the strong constructivist reading. **This requires ≥2 languages per cluster.**

## 2. Cluster taxonomy and candidate languages

| Cluster | Languages | Both-tradition coverage | Independence character | Resolution prior |
|---|---|---|---|---|
| Western academic Indology | English ✓, German, French | excellent (German: Deussen Upanishads, Neumann Pali Canon) | shared 19th-c. genealogy; LOW mutual independence | high — verify |
| Indian / source-proximate | Hindi (Bengali?, Tamil?) | good (Hindu native; Buddhist via 20th-c. revival) | living Hindu tradition; shares Sanskrit lexicon (close to source) | high — verify |
| East Asian Buddhist | Chinese, Japanese, Korean | Buddhist-rich, Hindu-thin | living Mahayana lineages | high — verify |
| Living Theravada | Thai, Sinhala, Burmese | Theravada-rich, Hindu-absent | Pali as living scripture | LOW-resource — likely fails gate |

## 3. Translation-chain provenance: the contamination axis

Independence is not binary. Modern translations in *every* language are partly contaminated by Western Indology (modern Hindi/Chinese scholars read Western scholarship; some translate *from* English). "Western influence" is a gradient. Three tiers of independence, by translation-chain provenance:

### Tier 1 — Contaminated-but-resolvable Western
English, German, French. Modern, high-resource, but the tradition under test.

### Tier 2 — Non-Western-chain modern (the key tier)
Modern Eastern-language texts whose translation chain descends from the original languages through **non-Western** hands, never routing through an English/German intermediary:

- **Modern Hindi, both traditions (best both-tradition non-Western-chain option):**
  - Hindu: **Gita Press (Gorakhpur)** editions — traditional devotional publisher translating Gita/Upanishads *directly from Sanskrit* within the pandit tradition.
  - Buddhist: **Dharmanand Kosambi** and **Rahul Sankrityayan** — Indian scholars who translated Pali texts *directly from Pali* (Sankrityayan studied in Sri Lanka/Tibet, not the West, for this material) during the 20th-c. Indian Buddhist revival.
  - Caveat: Hindi shares Sanskrit's religious lexicon, so it scores high on chain-provenance but weakly on *cultural distance* (these are different axes). Soft contamination ("the translator also read Radhakrishnan") is hard to fully exclude.
- **Modern Chinese / Japanese Buddhist (canon-descended):** modern vernacular (白话佛经 / 現代語訳) rendered *from the Classical Chinese canon*, not from English. Buddhist side clean; Hindu (Advaita) side in Chinese is thin and often English-sourced.

### Tier 3 — Uncontaminated ancient (the trump card)
The Classical Chinese Buddhist canon itself (法句經 = Chinese Dhammapada, ~224 CE; broader 大藏經 translated Sanskrit/Pali → Classical Chinese over ~200–1200 CE) is **chronologically guaranteed pre-Western-contact**. No Western convention *could* have entered, by date. Classical Tibetan canon is the same idea, lower-resource.

**The falsification logic:** if cross-tradition convergence appears in a *provably non-Western-chain* text — Hindi-via-pandits, or especially the ancient Chinese canon — the "convergence is a Western-Indology artifact" hypothesis is **dead**, because there was no Western tradition in the chain to project it. This is the single strongest result the project could produce. The ancient canon is the only chain where contamination is *impossible* rather than merely *undocumented* — at the cost of resolution risk (classical Chinese is medium-resource and differs from modern Chinese; the gate decides).

## 3b. Westernization score: from categorical triangulation to continuous decomposition

The discrete provenance tiers (§3) are coarse. A **continuous westernization score
per text** generalizes them and unlocks a far stronger analysis: covariate
adjustment / variance decomposition, turning the binary perennialist-constructivist
question into a quantitative partition.

### 3b.1 The score

A pre-registered weighted composite, leaning on objective measurable components:

*Measurable (computed from text — preferred, not investigator-subjective):*
- European/English loanword density
- Western-philosophical-vocabulary rendering rate (e.g., "Brahman"→"the Absolute"
  [Hegelian], "moksha"→"salvation" [Christian-inflected] vs transliterated technical
  terms) — countable
- Apparatus-style markers (critical-edition footnoting vs traditional commentary)

*Coded (per-text judgment, defensible rules, blind to CCB results):*
- Source of the translation (from original language = low; via English = high)
- Translator training (traditional/native institution vs Western university)
- Date relative to Western contact (ancient canon = 0; modern academic = max)
- Publisher tradition (devotional/traditional vs Western academic press)

The tiers (§3) become validation anchors: ancient canon should score ≈0,
English-academic ≈max. If the score does not reproduce that ordering, it is
miscalibrated.

### 3b.2 The decomposition (the payoff)

Regress convergence on westernization across texts/pairs:

    CCB = β₀ + β₁·westernization + ε

- **β₁ (slope)** — dose-response: how much westernization inflates apparent
  convergence (the "translation-tradition caused THIS" magnitude). A positive
  monotone slope is the constructivist signature; a flat slope supports
  source-content convergence.
- **β₀ (intercept at westernization = 0)** — the convergence predicted for a
  perfectly non-Western chain: the **residual convergence not attributable to
  westernization**.
- Partition: (observed − β₀)/observed = fraction attributable to translation
  tradition; β₀/observed = residual worth quantifying.

The deliverable is not a verdict but a partition (e.g., "≈X% of observed
cross-tradition convergence tracks translation westernization; ≈Y% survives
adjustment"). This is the heritability-style reframing of the 65-year debate:
not "real or artifact" but "what fraction is attributable to each."

### 3b.3 Three constraints (must pre-register)

1. **The ancient canon (Tier 3) is the anchor for β₀.** β₀ is convergence at
   westernization = 0. Without a near-zero-westernization text, β₀ is an
   extrapolation beyond the data and unreliable. The pre-Western Classical Chinese
   canon (~0, chronologically guaranteed) turns β₀ from extrapolation into
   interpolation. The decomposition makes Tier 3 the linchpin, not a nice-to-have.
2. **The covariate is partly confounded.** Westernization correlates with modernity
   and fluency (modern academic = high-West AND standardized; ancient = low-West AND
   archaic). Adjustment removes westernization *plus* entangled nuisance. Mitigated
   by weighting the measurable westernization-specific components; pre-register as a
   limitation.
3. **"Survives adjustment" ≠ "proven source content."** Residual β₀ is convergence
   not explained by the *measured westernization axis*. It could reflect other shared
   artifacts (common target-language structures, embedding-model biases). The honest
   claim is "residual not attributable to translation westernization" — a ceiling on
   the artifact-free signal, not a proof of it.

**Hidden-degree-of-freedom guard:** the score definition, components, weights, and
all per-text codings must be pre-registered and committed **before** the
cross-tradition CCB is run. Per-text westernization codings should be done **blind to
the CCB results** (code all texts' westernization first, then run CCB, then
correlate). Otherwise the score can be unconsciously tuned to produce a desired
correlation.

### 3b.4 Empirical calibration on neutral (off-topic) material

Rather than hand-code the score, calibrate it empirically on material **unrelated to
mysticism**, so no convergence signal can leak into the score. Two components:

1. **Translator fingerprint** — measure each translator's (or, as a noisier proxy,
   each language community's) westernization features on their *neutral* output
   (cooking, travel, technical, news — nothing philosophical/religious/consciousness-
   adjacent, or the "neutral" baseline leaks the target signal). Features:
   European-loanword density, syntactic calques from European languages,
   Western-conceptual framing. Content-independent — a translator's loanword habit on
   a cooking text predicts it on the Gita. Holds modernity/fluency constant (same
   translator), isolating translation tradition from the §3b.3(2) confound.
2. **Text-specific path** — the provenance chain of *this* text, read from its output
   features (an English-intermediated text carries European calques the canon-derived
   one does not). A single modern translator may render one text from English and
   another from the ancient canon: same fingerprint, different path.

**Avoid the language-dominates-the-axis trap:** raw cross-lingual embedding difference
captures *language identity*, not westernization (a Hindi cooking text vs an English
cooking text differ mostly because one is Hindi). Westernization is a *within-language*
axis too (Western-trained-Hindi vs traditional-pandit-Hindi differ at fixed language).
So define the axis either feature-based (component 1) or via within-language
Western-vs-traditional contrast on neutral content — not via raw between-language
distance.

### 3b.5 Known-groups validation of the metric

Validate the calibrated metric by **construct validity / known-groups**: pre-register
an uncontroversial expected ordering and check the metric reproduces it.

- French (Western Indology) → high. Modern Chinese → lower. Etc.
- **Key criterion (same-language, different-path):** Sanskrit→English→modern-Chinese
  must score *higher* than ancient-Chinese→modern-Chinese, though both end in modern
  Chinese. This directly tests whether the metric captures translation tradition vs
  surface language. If both score equally, the metric is detecting only "Chinese" and
  has failed; if the English-intermediated one scores higher, it captures the chain.

Discipline to keep this from becoming circular (tuning to priors):
1. **Pre-register the expected orderings** as validation targets before computing scores.
2. **Held-out validation, then freeze.** Develop/tune the metric on validation texts
   with known orderings; freeze; *then* apply to analysis texts (train/validate/test).
3. **Validate against westernization expectations only — NEVER against convergence.**
   Orderings must be about the covariate, using uncontroversial cases. Tuning the
   metric to produce a convergence result contaminates the whole decomposition.
   Westernization-ordering validation is legitimate construct validation; convergence-
   outcome validation is forbidden.

The ancient canon (Tier 3) has no neutral-content counterpart (only scripture
survives), so its score stays anchored at ≈0 by chronology, not by this empirical
calibration; the calibration governs the modern texts where the regression slope lives.

### 3b.6 Score granularity: the (translator, language-era-chain) tuple

The score unit is **(final translator/community, sequence of (language, era) steps)**.
Any text sharing both gets the same score. This granularity is forced by the
calibration method: the chain must be characterized by *generalizable* properties
that neutral material also possesses, so it can be calibrated on matched off-topic
text. Specifying exact intermediary *editions* would make the score text-specific
(tied to one translation lineage), which neutral material does not share — breaking
calibration. So the chain is coarsened to (language, era) per step, not specific
editions:

- Generic enough to calibrate (neutral 19th-c. colonial English translations exist
  to calibrate the "English(19c colonial)" step).
- Specific enough to capture real variation (colonial-English vs modern-academic-
  English Indology carry different westernization; era distinguishes them).

Example chain-types: Sanskrit(ancient) → English(19c colonial) → Chinese(modern) is
one; Sanskrit(ancient) → Chinese(ancient canon) is another; Sanskrit(ancient) →
Hindi(modern, pandit) is another.

**Composition: max-step.** The chain inherits the westernization of the *most-Western
step it passed through*, because westernization is sticky — once content is rendered
through colonial English, later non-Western steps do not scrub it out. Max-step
reproduces the §3b.5 known-groups orderings automatically (Sanskrit→English→Chinese
scores high via its English step; Sanskrit→ancient-Chinese scores ≈0, no Western
step). Additive/weighted compositions are alternatives; max-step is the defensible
default and easiest to validate. Pre-register the choice.

**Consequence:** texts sharing a tuple are *replicates at one westernization level* —
they pin down the mean convergence at that level (reducing noise); spread *across*
tuples gives the regression its slope leverage. No need for a unique score per text,
just per tuple.

Two assumptions to flag explicitly in the pre-registration: (i) westernization is
roughly constant within a translator's rendering of a text (intro/commentary vs literal
verses may differ — a simplification, not exact); (ii) where a translator's individual
neutral output is unavailable, the unit degrades to (language-community, chain),
noisier but the same logic.

### 3b.7 Calibration feasibility: bucket-level corpora + dual-route cross-check

The practical crux: empirically calibrating the score seems to require matched neutral
material for every distinct tuple ("did Gita Press ever translate a cookbook?"), which
is intractable. The resolution: **calibrate one level down, at the (language, era)
bucket, not the tuple.** Because the chain score composes from its (language, era)
steps, you only need representative neutral material for each distinct *bucket* across
all chains (~5–8: English-19c, English-modern, Hindi-modern, Chinese-modern, …), NOT
per tuple (dozens). Bucket corpora are findable (neutral modern Hindi, 19c English
academic prose, modern Chinese — news/technical/literary/historical archives). The
intractable "specific translator's off-topic output through the same lineage" is never
needed.

**Two independent routes to the chain score, both needing only bucket corpora, that
cross-check each other:**
1. **Compositional (a priori):** compose the (language, era) bucket values (calibrated
   on bucket neutral corpora). Needs bucket corpora only.
2. **Direct (a posteriori):** measure westernization features on the *actual output
   text*, relative to the *target-language-era neutral baseline* (detect calque/framing
   excess beyond what is normal for that language-era). A Sanskrit→English→Chinese text
   should show European-calque density above the modern-Chinese-neutral baseline; a
   canon-derived Chinese text should not. Needs only the target-language-era corpus.

Agreement between routes gives confidence; divergence is informative. The direct route
guards the key risk in the compositional route: max-step assumes the most-Western
step's westernization fully propagates, but a final non-Western translator may
*re-naturalize* it, so max-step can overestimate — the direct measurement catches
exactly that case (re-naturalized text won't show the excess).

### 3b.8 Composition as pre-registered model selection

The step-composition function (§3b.6) is chosen by **model selection from a small
pre-specified candidate set**, each encoding a different theory of how westernization
propagates through a chain:
- **max-step** — fully sticky (most-Western step dominates)
- **mean** — dilutes across steps
- **injecting-step-weighted** — the moment of Western contact dominates
- **exponential decay** — recent steps weighted more

**Selection criterion (load-bearing anti-circularity guard):** the winning composition
is the one that best reproduces the **pre-registered known-groups WESTERNIZATION
orderings (§3b.5) on held-out validation data — NEVER the one that produces a desired
CONVERGENCE result.** Judging composition by the convergence outcome contaminates the
entire decomposition. Select on westernization-construct-validity, freeze, then run the
convergence analysis (train/validate/test). Limit to the ~4 pre-specified candidates to
avoid overfitting the validation set. The winning composition is itself a reportable
finding — it characterizes how westernization propagates through translation chains.

## 4. Mandatory per-language resolution gate

The Phase 1c lesson, built in as a precondition: **before any language's cross-tradition CCB result counts, that language must pass the within-language concept-binding diagnostic** (`scripts/within_language_concept_binding.py`) — the model must resolve concept structure within that language (target: significant within-language binding for AWARENESS and RECOGNITION at minimum). A language that fails the gate is excluded from the triangulation, reported transparently. This also controls the resolution-gradient confound: if the model resolves English > Hindi > Chinese by training-data volume, CCB differences could be resolution artifacts; reporting each language's within-language resolution alongside its CCB guards against this.

**Run the gate FIRST**, before any cross-tradition CCB — the Phase 1c ordering lesson (we ran CCB first, diagnostic second; correct conclusion, wasted effort).

## 5. What a strong Phase 2a set looks like

Balanced, ≥2 per cluster, spanning provenance tiers:

- **Western (Tier 1):** English ✓ + German (German has the best non-English both-tradition coverage; English-vs-German cleanly tests anglophone-specific vs Western-Indology-general). + French if extending.
- **Non-Western-chain (Tier 2):** Hindi (Gita Press + Kosambi/Sankrityayan — both traditions, non-Western chain) + modern Chinese Buddhist (canon-descended).
- **Ancient uncontaminated (Tier 3):** Classical Chinese 法句經 + canon Hindu/Mahayana texts, *if* they pass the gate.

The final set is determined **empirically by which languages clear the resolution gate**, not chosen in advance.

## 6. Open questions for the pre-registration

1. Same multilingual model across all languages (apples-to-apples comparison, inherits resolution gradient) vs per-language monolingual models (native resolution, harder cross-model comparison). Likely: report both; lead with same-multilingual-model gated by per-language resolution.
2. Translator independence is partial and provenance is per-text archival work. Pre-register the contamination tiers; weight Tier 2/3 evidence accordingly.
3. Hindi-Sanskrit lexical overlap — chain-clean but culturally close. Weight Chinese (linguistically alien) more heavily for the cultural-distance axis.
4. Concept tagging: Option A (manual regex) per language. Hindi reuses the Sanskrit Devanagari dictionary (shared lexicon); Chinese needs a new Hanzi dictionary; German/French need new Latin-script dictionaries.
5. Statistical comparison across languages in relative terms (effect sizes, binding ratios), not absolute cosines (Draft 6 §8 lesson).

## 7. Why this is the strongest version of the project's argument

The English-only Phase 1a/1b result could not address the broad-constructivist objection — no way to separate source-content convergence from translation-convention convergence. Phase 2a attacks that confound directly via triangulation across independent translation communities, with the variance-components structure to separate trait/cluster/language variance, and the provenance tiers culminating in a pre-Western-contact chain that no Western convention could have touched. Whichever way it resolves, it is a stronger and more publishable result than any single-language analysis, and it is the natural culmination of the corpus-expansion arc.

## 8. Staged plan

1. Source Tier 2 first: Hindi Gita (Gita Press) + Hindi Dhammapada (Kosambi/Sankrityayan); modern Chinese canon-derived Buddhist text. Add German (Tier 1) for the within-Western replication.
2. Clean, chunk, language-tag, document provenance per text.
3. Per-language within-language resolution diagnostic (the gate). Keep only languages that pass.
4. Build per-language Option A concept dictionaries (Hindi reuses Sanskrit Devanagari; Chinese Hanzi; German Latin).
5. Pre-register predictions, decision rules, per-language gates, provenance tiers. External timestamp.
6. Run cross-tradition CCB per language; compute the variance-components comparison across languages/clusters.
7. Attempt Tier 3 (ancient Chinese canon) if it clears the gate — the trump-card analysis.
8. Write findings; paper §6.x.

---

*Design sketch for Phase 2a. The pre-registration with specific predictions, per-language resolution gates, and provenance-tier weighting will be authored separately and externally timestamped before any Phase 2a main analysis.*
