# Methodology Notes

Running log of methodological issues, biases, and design decisions identified during the project. Each entry should be honest about what we know, don't know, and how each issue affects which findings.

---

## 2026-05-14: The shared-placeholder bias in vocabulary substitution

### The issue

The vocabulary-substitution experiment in `findings/phase0-v0.5-substituted.md` replaces tradition-specific terms with shared gibberish placeholders. The intent was to remove vocabulary as a source of artificial *separation* between traditions describing the same structural feature.

**But this also introduces a tautological source of *similarity*.** After substitution:

- *"Brahman alone is real"* → *"[qntrx] alone is real"*
- *"God is everywhere"* → *"[qntrx] is everywhere"*

These two sentences now contain the *same token* `[qntrx]`, which the embedding model will treat as identical. Any pair of passages from any two traditions that mention an ULTIMATE-role term now share at least one token — and embedding similarity is partly a function of shared tokens.

So the substituted-corpus result has a bias *toward* finding cross-tradition similarity, exactly inverse to the bias *against* it in the unsubstituted corpus (where each tradition's distinctive terms pushed embeddings apart).

### Why this matters

The genuine question is not "do passages contain the same tokens after substitution" (trivially yes — we forced that). It's:

> When each tradition uses its concept-X word, do the *surrounding contexts and structural relations* converge across traditions — independent of which token we chose to denote concept-X?

The substituted-corpus experiment as run partly answered the surface question instead of the real one.

### What the v0.5-substituted finding still tells us — and what it doesn't

**Still defensible:**

- The H1 historical-convergence result (nondual_cross > nondual_to_dualistic, p<0.0001) holds in all three runs (v0, v0.5, v0.5-substituted). Triply confirmed.
- The cluster *structure* (three clusters: historical-nondual, modern-computational, dualistic+analytic) is preserved across substitution. Substitution did not collapse the clusters.
- **The fact that most of the gap did *not* close after substitution is informative *despite* the bias** — the bias should have closed the gap if there were nothing else there. The gap mostly persisting means there's a real factor (style/register/content) beyond what the bias can manufacture.

**Less defensible than v0.5-substituted findings doc implied:**

- The specific "vocabulary accounts for ~25% of the gap" claim was estimated by comparing substituted to unsubstituted similarities. That estimate is inflated by the placeholder-sharing artifact, so the true vocabulary share is *less* than 25%.
- Specific pair shifts (e.g., simulation_theory × analytic_idealism +0.049) are partly real content convergence revealed and partly placeholder-sharing artifact. Hard to say what the split is without a cleaner experiment.

### What experiment would have been unbiased

Several options, in increasing rigor:

1. **Per-tradition placeholders.** Use distinct gibberish for each tradition's version of each concept. E.g., Advaita's "Brahman" → `[adv_q]`, Christian "God" → `[chr_q]`, etc. No shared placeholder = no placeholder-induced similarity. Any cross-tradition similarity that remains must come from context or style.
2. **Mask-and-compare.** Replace tradition-specific terms with a uniform `[MASK]` token. Embedding can't gain similarity from the masked positions (they all look the same regardless of source), so any cross-tradition similarity must come from the surrounding contexts.
3. **Concept-conditional similarity from the unsubstituted corpus.** Use the original (unsubstituted) embeddings, but compute statistics conditioned on whether each pair of passages shares a concept-role (via regex tagging from the substitution rules). Ask: "Are passages from different traditions that share concept C more similar than passages from different traditions that don't share C, all else equal?" This avoids substitution entirely.

Approach (3) is cleanest and is what's planned next.

### How this should be cited going forward

When discussing the v0.5-substituted result:

- Cite the headline ("most of the gap remained after substitution") because the bias would have *closed* the gap, so its persistence is genuine signal.
- *Don't* cite specific pair shifts as evidence of content convergence without acknowledging the bias.
- Cite the *upper bound* for vocabulary share of the gap (~25%) but flag that the true share is lower.
- Treat the concept-level analysis (next experiment) as the primary test of concept-level convergence.

---

## 2026-05-15: Priorities escalated after Phase 0 paper review

A review of `paper/paper-draft.md` Drafts 1 and 2 escalated three Phase 1 priorities from the secondary list to the load-bearing list. Recording the escalations here so they survive into Phase 1 corpus design.

### Adversarial passage selection — escalated

Original framing: "the strongest single defense against selection bias" but listed under future methodological controls. Reviewer position: this is not a future-work bullet, it is **the test that converts the result from 'interesting under the investigator's view of the field' to 'interesting from a neutral starting point.'** A constructivist-leaning scholar must independently select the *least*-nondual passages from the same authors; the analysis is re-run on the union and the difference. Phase 1 should not proceed to publication without this control.

### Held-out human-validated concept tagging — escalated

Original framing: §4.2 of Draft 2 acknowledges regex tagging as a hidden degree of freedom and says the concept-binding analysis is bias-free *of the shared-placeholder artifact* but not *in the absolute*. Reviewer position: the implications are larger than the §4.2 acknowledgment. Patterns and corpus came from the same glossary built by the same person who believes in convergence. **Someone with a different theory of nondualism would build a different glossary, tag different passages, and might get a different answer.** Held-out human-validated tagging on a randomly sampled subset is exactly parallel to adversarial inclusion for passage selection, and belongs at the same priority tier (alongside translators and paraphrases).

### Translator-variance baseline — already escalated in Draft 2, prediction recorded

Already named in Draft 2 §5 as the strongest constructivist objection and the largest unaddressed threat to Phase 0 validity. Reviewer's specific prior to keep visible during Phase 1 design: **within-source translator variance, once measured, is likely to be substantial — possibly approaching the magnitude of some of the smaller cross-tradition bindings.** If that turns out to be true, several of the smaller bindings deflate and the paper's center of gravity shifts toward AWARENESS and RECOGNITION as the only signals that survive. Phase 1 corpus design should aim to make this measurement clean (multiple translations per source where available) rather than treat it as a sensitivity check at the end.

### The combined-coupling concern

These three escalations share a structural worry that Draft 2 names component-by-component but does not surface as a single object: the Phase 0 pipeline has the form *English translation → glossary by believer → regex from glossary → paraphrases by same believer → analysis*. Each component has a defense; the combined chain has a coupling that no single defense addresses. The Phase 1 priorities listed above are designed to break the chain at every link rather than reinforce any single one. This is the right shape but it deserves stating as a single principle: **Phase 1's purpose is to break the pipeline-coupling chain, not to scale up Phase 0.**

### Phase 1 priors to test against

Reviewer's stated priors for outcomes after the escalated controls are in place:

- ~60 % probability AWARENESS and RECOGNITION survive Phase 1 controls at *p* ≤ 0.01.
- ~40 % probability the full five-concept pattern survives.

Recording these so that Phase 1 results can be compared against a stated prior rather than retrofitted to a post-hoc narrative.

### Project-level reframing

The most useful version of the project is not "we resolve the Stace–Katz debate" but "we produce a new class of evidence both sides have to engage with on the merits." The current methodological care is unusual for either parent discipline, and that combination is what makes the work worth doing. The framework's value does not depend on which way the nondualism finding lands.

---

## 2026-05-15 (later): Phase 1a observations

The whole-book replication (Phase 1a; see `findings/phase1-whole-books.md`) ran and produced two methodologically substantive findings that this notes-document should preserve.

### Vocabulary breadth as noise floor

Passage-level concept tagging dilutes the signal when the pattern dictionary contains common English terms that appear in non-technical contexts. Phase 0 paraphrases were investigator-curated to use those terms only when the passage was actually engaging the concept; Phase 1a published prose uses them everywhere. Result: AWARENESS, ULTIMATE, and WORLD bindings deflated 3–4× at passage-level in Phase 1a, while SUBSTRATE (whose pattern dictionary is entirely technical — `emptiness`, `śūnyatā`, `implicate order`, `holographic`, `integrated information`, `holomovement`, `noumenon`) did not deflate at all (+0.054 vs +0.053).

The mechanism is the casual-usage noise floor at passage granularity. When tagging filters to sentences actually using the pattern (sentence-level analysis), deflation drops to 25–30% — much smaller. **This means sentence-level should be the default granularity for future analyses**, and technical-only-vocabulary variants of the patterns should be tested in a held-out follow-on.

Pre-registered predictions for the technical-only-tagging test (written before running, so the result is a clean confirmation/refutation rather than post-hoc rationalization):

| Concept | Phase 1a current | Prediction (technical-only) |
|---|---|---|
| AWARENESS | +0.026 | +0.08 to +0.11 |
| ULTIMATE | +0.014 | +0.04 to +0.06 |
| WORLD | +0.022 | +0.06 to +0.08 |
| RECOGNITION | +0.025 | +0.03 to +0.05 |
| SUBSTRATE | +0.054 | +0.054 (unchanged) |

### Phase 1a result above reviewer prior

The subsequent-review Phase 1 priors (recorded above) were ~60% AWARENESS+RECOGNITION survive, ~40% full five-concept pattern survives. Phase 1a observed: **all five binding concepts survived** at *p* ≤ 0.0015 on verified-non-paraphrase whole-book text.

Per the "resist framing drift after evocative results" caution: the result is above prior, but each binding is smaller than in Phase 0. The §7.3 decomposition still places genuine concept-level binding as the smallest and best-controlled component of the apparent signal. Cite affirmatively but do not over-promote.

### Phase 1a does not address what Phase 1 still needs

For the avoidance of doubt: Phase 1a corresponds to *one* of the four pipeline-coupling concerns the subsequent review identified — paraphrases. Translator-as-confound, regex-tagging-as-hidden-degree-of-freedom, and adversarial-passage-selection all remain unaddressed. Phase 1a should not be cited as "Phase 1 results" without these qualifiers. The label "Phase 1a" exists precisely to mark this incompleteness. Full Phase 1 includes multi-translator inclusion, non-English source analysis with multilingual embeddings, modern computational sources via arxiv, adversarial-passage-selection by a constructivist-leaning scholar, and held-out human-validated concept tagging — see `paper/paper-draft-v5.md` §10.

---

## 2026-05-15 (still later): Pre-registered technical-only-tagger result refines the §6.8 mechanism

The Draft 4 §6.8 vocabulary-breadth-as-noise-floor mechanism was tested via a pre-registered technical-only-tagger variant (Draft 4 §6.8 predictions; implementation in `scripts/concept_analysis.py --technical-only` using `TECHNICAL_ONLY_PATTERNS`; results in `findings/phase1a-technical-only-tagger.md`).

The predictions were partially confirmed, partially refuted in informative directions, and partially untestable on the Phase 1a corpus:

- **SUBSTRATE control: confirmed exactly** (unchanged at +0.054). The technical-only-tagger experiment is methodologically clean.
- **RECOGNITION: dramatically exceeded prediction** (+0.110 observed vs +0.03–0.05 predicted; advaita × theravada at 0.531 as top cross-tradition pair). This is the strongest single cross-tradition concept-binding result the project has produced.
- **ULTIMATE: failed in unexpected direction** (+0.008 observed vs +0.04–0.06 predicted recovery; binding *decreased* under technical-only restriction). The dropped common-English terms (`God`, `the divine`, `lord`) were tagging dualistic-tradition passages; the remaining technical terms (`Brahman`, `Tao`, `Buddha-nature`, `Ein Sof`) tag only nondual traditions; cross-tradition pair coverage shifted nondual-heavy and binding shrank.
- **AWARENESS, WORLD: untestable** on Phase 1a. After dropping common-English terms, n_with dropped to 1 and 5 respectively. Phase 1a corpus lacks the required technical-vocabulary coverage (Dzogchen `rigpa`, Sanskrit Advaita `chit`, IIT `phi` for AWARENESS; concentrated `samsara`/`ten thousand things` for WORLD).

The §6.8 mechanism refines to two components:

1. **Casual-usage noise floor** (the Draft 4 single-component claim): common-English terms tagged in non-technical passages dilute passage-level binding. Technical-only restriction increases binding when concept's technical vocabulary is well-represented across traditions in the corpus.
2. **Coverage-distribution asymmetry** (new component): some concepts' technical vocabulary concentrates in fewer tradition categories. Dropping common-English terms shifts pair coverage asymmetrically and *decreases* cross-tradition binding when only one category retains coverage.

Both components are present in any vocabulary-breadth analysis; net direction depends on which dominates and on the corpus's tradition-coverage distribution of technical terminology. This is corpus-dependent, which is itself a methodological caveat for future CCB applications.

**Pre-registration practice value confirmed:** Without writing the §6.8 single-component prediction into Draft 4 *before* implementing and running the test, the (b) component coverage-asymmetry refinement would read as post-hoc rationalization rather than a falsifier-driven mechanism update. The pre-registration practice surfaced the limitation cleanly.

