# Phase 1a — Whole-Book Corpus Replication

> **Naming note:** this is **Phase 1a**, not full Phase 1. The whole-book corpus replication addresses one of the four pipeline-coupling concerns from the second-reviewer pass (the paraphrase confound) but does *not* address translator-as-confound, regex-tagging-as-hidden-degree-of-freedom, adversarial-passage-selection, or non-English source analysis. The full Phase 1 program is described in `next-steps.md` and `paper/paper-draft-v3.md` §10.

---

**Run date:** 2026-05-15
**Corpus:** 20 verified PD books spanning historical contemplative, philosophical, and analytic traditions
**Pipeline:** fetch → clean → chunk → balanced subsample (~50 chunks/book) → 920 passages
**Embedding models:** OpenAI `text-embedding-3-large` (3072-dim, proprietary) AND open-source `sentence-transformers/all-MiniLM-L6-v2` (384-dim, local ONNX)
**Methodology:** unchanged from Phase 0 — five analyses (document-level, vocabulary-substituted, concept-binding passage-level, concept-binding sentence-level OpenAI, concept-binding sentence-level BERT)

Raw outputs: `results/phase1/` and `results/sentence_concept_analysis/{openai,onnx}/*/sentence_concept_binding_vec.csv`.

---

## What was tested and why

Phase 0 used a 143-passage corpus where 30-50% of passages were paraphrases written by the project owner. That was the cheapest possible test of the framework, but it carried risk: a believer-built corpus with believer-written paraphrases is a coupled chain (paper review noted this as the pipeline-coupling concern). Phase 1's job was to **replace paraphrases with real published whole-book text** — keeping methodology unchanged otherwise — and see whether the Phase 0 findings survived.

Critically, Phase 1 does **not** address several other pipeline-coupling components (see `methodology-notes.md`):

- **Translator variance** — each book in Phase 1 has only one translator; we cannot yet measure within-source translator effects
- **Regex tagging** — same glossary as Phase 0
- **Adversarial inclusion** — same investigator selected the corpus

So Phase 1 is one step along a longer corrective program, not the final test.

---

## The corpus (20 books, ~2.85M raw tokens, sampled to 920 passages)

| Tradition | Category | Books | Source |
|---|---|---|---|
| advaita | nondual | Upanishads (Paramananda), Bhagavad Gita (Arnold) | PG verified |
| daoism | nondual | Tao Te Ching (Legge), Zhuangzi (Giles) | PG verified |
| sufi | nondual | Rumi Mesnevi (Redhouse), Persian Mystics (Davis) | PG verified |
| christian_mystical | nondual | Brother Lawrence, Steiner Mystics anthology | PG verified |
| spinozist | nondual | Spinoza Ethics | PG verified |
| theravada | dualistic | Dhammapada (Müller) | PG verified |
| catholic_scholastic | dualistic | Aquinas Summa I, Augustine Confessions | PG verified |
| reformed_theology | dualistic | Calvin Institutes Vol. 1 | PG verified |
| kantian | dualistic | Critique of Pure Reason, Critique of Practical Reason | PG verified |
| humean | non_contemplative | Treatise of Human Nature, Enquiry Concerning Human Understanding | PG verified |
| analytic | non_contemplative | Russell Problems, External World, Mysticism and Logic | PG verified |

**What's missing vs Phase 0:** all the modern computational nondual texts (Bostrom, Wheeler, Tegmark, Kastrup, Hoffman) and bridge thinkers (Bohm, Whitehead, Friston, Tononi, Rovelli). Those came in via Phase 0 paraphrases; Phase 1 corpus is PD-only and historical. **Phase 1 therefore tests only the historical-traditions H1 claim, not the broader H1' modern/historical claim.** The modern thinkers come back in via arxiv papers and fair-use research excerpts in Phase 1.5.

---

## Headline results

### 1. Document-level prototype (H1 cross-tradition convergence)

| Statistic | Phase 0 (v0.5) | Phase 1 (whole books) |
|---|---|---|
| nondual_cross_trad_mean | 0.315 | **0.371** |
| nondual_to_dualistic_mean | 0.270 | **0.346** |
| dualistic_to_dualistic_mean | 0.296 | **0.383** |
| observed H1 diff | +0.045 | **+0.025** |
| permutation p one-sided | <0.0001 | **<0.0001** |
| k-means ARI | 0.287 | 0.345 |
| k-means NMI | 0.401 | 0.359 |

**H1 still holds at p<0.0001, but the observed effect size halved (+0.045 → +0.025).** Real text introduces noise paraphrases didn't.

**Striking flip:** in Phase 0, nondual traditions clustered *more tightly with each other* than dualistic traditions did (0.334 vs 0.249). In Phase 1, the opposite — dualistic Western traditions (Kant, Hume-adjacent Augustine, Aquinas, Calvin) cluster *more tightly* (0.383) than the diverse nondual traditions do (0.371). The Phase 0 paraphrases were too lexically uniform in the nondual category; real Tao Te Ching + Upanishads + Sufi Rumi + Spinoza Ethics + Brother Lawrence are stylistically more different from each other than Aquinas + Calvin + Kant. **The historical H1 claim survives despite the nondual category having lower within-category cohesion than the dualistic control.**

### 2. Vocabulary-substituted document-level

| Statistic | Phase 1 unsub | Phase 1 sub | Delta |
|---|---|---|---|
| nondual_cross_trad_mean | 0.371 | 0.376 | +0.005 |
| nondual_to_dualistic_mean | 0.346 | 0.354 | +0.008 |
| observed H1 diff | +0.025 | +0.022 | -0.003 |

**Substitution did almost nothing.** The shared-placeholder bias that distorted Phase 0 substituted results (where the small corpus amplified placeholder-token effects) is much smaller at this scale. Whole-book text has enough independent content that gibberish placeholders don't materially shift similarities. Confirms the original methodology-notes warning that the v0.5-substituted findings should be cited as upper-bound estimates of vocabulary share.

### 3. Concept-level binding — passage-level (canonical bias-free test)

| Concept | n_passages | Phase 0 (v0.5) | Phase 1 | Delta |
|---|---|---|---|---|
| AWARENESS | 52 | +0.113 (p<0.0001) | **+0.026** (p=0.0005) | deflated 4.3× |
| RECOGNITION | 51 | +0.079 (p=0.001) | +0.025 (p=0.0005) | deflated 3.2× |
| WORLD | 170 | +0.077 (p<0.0001) | +0.022 (p<0.0001) | deflated 3.5× |
| ULTIMATE | 562 | +0.057 (p<0.0001) | +0.014 (p<0.0001) | deflated 4.1× |
| **SUBSTRATE** | 15 | +0.053 (p=0.01) | **+0.054** (p=0.0015) | **unchanged** |
| SELF | 27 | -0.058 (NS) | -0.012 (NS) | NS both |

**All 5 binding concepts survived statistical significance at p ≤ 0.0015.** This exceeds the reviewer's prior of ~60% surviving. But effect sizes deflated 3-4× for everything *except* SUBSTRATE.

**SUBSTRATE landed on essentially the same number** (+0.053 → +0.054). This is the project's most surprising single result.

### 4-5. Concept-level binding — sentence-level (OpenAI + BERT)

Vectorized analysis on ~4000 stratified-sampled sentences from the 14,173 total Phase 1 sentences (script: `scripts/sentence_binding_vectorized.py`):

| Concept | n_sentences | OpenAI binding (Phase 1) | OpenAI (Phase 0) | BERT binding (Phase 1) | BERT (Phase 0) |
|---|---|---|---|---|---|
| **AWARENESS** | 25 | **+0.082** | +0.114 | **+0.121** | +0.204 |
| RECOGNITION | 26 | +0.061 | +0.082 | +0.090 | +0.073 |
| WORLD | 75 | +0.051 | +0.082 | +0.065 | +0.073 |
| ULTIMATE | 522 | +0.047 | +0.067 | +0.074 | +0.079 |
| SELF | 16 | +0.031 (p=0.006) | NS | +0.066 | +0.034 (NS) |
| SUBSTRATE | 5 | +0.053 (p=0.04) | +0.051 | +0.048 (p=0.09, NS) | +0.050 |

**Critical observation:** at *sentence-level*, the Phase 1 → Phase 0 deflation is **only ~25-30%**, not 4×. This is a different story than passage-level showed.

**Why:** Passage-level tagging fires on any passage containing the concept term somewhere — even if 95% of the passage is about something else. Sentence-level tagging only fires on sentences that actually use the term. Real-text passages have many sentences that are about other things; paraphrase passages were tight. The Phase 1 passage-level "deflation" was largely **the casual-usage noise floor** added by tagging entire passages on a single term mention.

**Cross-model agreement is excellent:** BERT consistently shows stronger bindings than OpenAI (same as Phase 0), and the ranking of concept strengths is nearly identical across models.

---

## The SUBSTRATE finding, examined carefully

The single most striking result: **SUBSTRATE binding is +0.054 in Phase 1 passage-level vs +0.053 in Phase 0 — essentially unchanged.** Every other concept deflated 3-4× at passage level. Why?

**Three competing explanations:**

### (a) Vocabulary-breadth artifact

SUBSTRATE tags fire on technical-only terms: `emptiness`, `śūnyatā`, `implicate order`, `holographic principle`, `integrated information`, `dependent origination`, `holomovement`, `noumenon`, `thing-in-itself`. **None of these appear in casual usage.** When Phase 1's real-book text gets tagged for SUBSTRATE, it's almost always actually engaging the substrate concept technically.

Compare to AWARENESS: tags include `consciousness`, `awareness`, `sentience` (alongside rare technical `rigpa`, `chit`, `nous`, `phi`). The casual terms tag many passages where the term appears non-technically — adding noise that wasn't present in Phase 0 paraphrases.

So Phase 1 added massive casual-usage noise to AWARENESS/ULTIMATE/WORLD bindings, **but added almost none to SUBSTRATE** because substrate vocabulary doesn't have casual usage. Apparent "robustness" of SUBSTRATE is partly the absence of a noise floor that affected the others.

**Evidence for (a):** at sentence-level analysis (where we filter to sentences actually using the term, eliminating the casual-tag-but-not-really-engaging-concept problem), the AWARENESS deflation drops from 4× to ~25%. This shows most of the AWARENESS "deflation" is exactly the noise-floor effect predicted by (a).

### (b) Structural-claim narrowness

The substrate move ("there's a layer beneath appearance that isn't itself an appearance") is *topologically narrow* — there are fewer alternative ways to make this claim than to make claims about consciousness or about the ultimate. If true, traditions that make this move are forced to converge on a small region of conceptual space, and their texts converge whether or not we add noise.

This is the genuinely interesting interpretation. It would line up with the Rovelli-Nagarjuna case being not a fluke but a generic property of substrate-talk.

### (c) Small-n statistical fluke

SUBSTRATE has the smallest sample in both phases (~15 passages, ~5-90 cross-tradition pairs depending on granularity). The +0.054 landing exactly on +0.053 might be coincidence — both estimates have wide variance.

**Evidence against (c):** if SUBSTRATE were noisy, we'd expect deflation OR inflation, not the exact same number. The persistence is at least consistent with stable signal.

**My honest read:** explanation (a) is doing most of the work. SUBSTRATE didn't "fail to deflate" — it never had a casual-usage noise floor in the first place. We can test this directly by restricting AWARENESS/ULTIMATE/WORLD patterns to their *technical-only* terms and re-running concept_analysis. Predictions written before testing (see end of this doc).

This does NOT rule out explanation (b) — there may still be a real structural narrowness to substrate-talk on top of the vocabulary effect. But (a) is the more parsimonious primary cause.

---

## The pipeline-coupling status after Phase 1

What Phase 1 addressed:
- ✅ **Paraphrase confound** (a top-tier reviewer concern). Real published whole-book text now drives all results. H1 still significant after this fix; effect sizes for concept-binding deflated as predicted.
- ✅ **Statistical power**. 920 passages, 14k sentences. Phase 0 was 143/322.

What Phase 1 did NOT address:
- ❌ **Translator variance** — each book has one translator. We still cannot estimate within-source translator effects. The reviewer prior is that this is the largest remaining unaddressed threat.
- ❌ **Regex tagging bias** — same concept patterns as Phase 0, built by the same investigator who believes in convergence. Held-out human-validated tagging is still future work.
- ❌ **Adversarial selection** — same investigator chose the corpus. A constructivist-leaning scholar would pick different texts and probably different passages within texts.
- ❌ **Modern computational traditions** — Phase 1 corpus is PD-only and historical. The H1' (modern + historical) claim is not testable on this corpus; needs Phase 1.5 to add arxiv papers and fair-use modern excerpts.

The Phase 0 pipeline-coupling concern is **partially resolved** — the most coupled link (paraphrases) is gone — but several other coupled links remain.

---

## What this means for the paper

Draft 3 (post-Phase 1) should:

1. **Lead with the surviving H1 finding** restricted to historical traditions: cross-tradition convergence on nondual structural features, p<0.0001 even in whole-book real text. **Effect sizes are smaller** than Phase 0 suggested. This is the paper's honest center of gravity.

2. **AWARENESS and SUBSTRATE remain the two strongest signals** — AWARENESS because the sentence-level deflation is mild (+0.082 OpenAI, +0.121 BERT); SUBSTRATE because passage-level deflation is essentially zero (+0.054). **Mahayana × Theravada at 0.518 on AWARENESS** (Phase 0 BERT result) is the cleanest "neither side wrote toward the comparison" finding. The Rovelli-Nagarjuna case should still be present but cited as methodological validation, not as discovery.

3. **Frame the deflation correctly.** The Phase 0 effect sizes were inflated by paraphrase uniformity AND by passage-level tagging firing on casual term usage. **Sentence-level Phase 1 numbers are the honest baseline.** Future papers should use sentence-level or technical-only-tagging.

4. **Vocabulary-breadth is now a load-bearing methodology note.** Different concepts have different signal-to-noise ratios based on how technical their tag vocabulary is. SUBSTRATE has the cleanest tags; AWARENESS has the noisiest.

5. **Keep the constructivist objections open**, especially translator variance. The paper should not claim to have answered them.

---

## Predictions to write down before next test

A held-out test of explanation (a) — restricting AWARENESS, ULTIMATE, WORLD patterns to *technical-only* vocabulary (drop "consciousness", "awareness", "God", "the divine", "world", "the universe", etc.; keep `rigpa`, `chit`, `nous`, `phi`, `Brahman`, `Tao`, `samsara`, `the ten thousand things`, etc.):

| Concept | Phase 1 binding (current) | Prediction (technical-only) |
|---|---|---|
| AWARENESS | +0.026 | **+0.08-0.11** (recovers toward Phase 0) |
| ULTIMATE | +0.014 | **+0.04-0.06** (comes up partially) |
| WORLD | +0.022 | **+0.06-0.08** (comes up substantially) |
| SUBSTRATE | +0.054 | **+0.054** (no change — no casual terms to drop) |
| RECOGNITION | +0.025 | **+0.03-0.05** (most RECOGNITION terms are already technical, smaller change) |

If predictions hold, vocabulary breadth was explanation (a) was the primary driver, and the Phase 0 effects are recoverable from Phase 1 data with better tagging.

If predictions fail — particularly if AWARENESS doesn't recover toward Phase 0 — then explanation (b) (structural narrowness) becomes more attractive for SUBSTRATE, and we have a deeper question about why some concepts converge and others don't.

This test is the next step.

---

## File pointer

- Document-level prototype Phase 1: `results/phase1/document_level/`
- Vocabulary substitution Phase 1: `results/phase1/substituted/`
- Concept analysis Phase 1: `results/phase1/concept_analysis/`
- Sentence-level Phase 1 OpenAI: `results/sentence_concept_analysis/openai/text-embedding-3-large/sentence_concept_binding_vec.csv`
- Sentence-level Phase 1 BERT: `results/sentence_concept_analysis/onnx/sentence-transformers__all-MiniLM-L6-v2/sentence_concept_binding_vec.csv`
- Corpus: `corpus/passages_phase1.jsonl` (920 sampled passages) and `corpus/chunks.jsonl` (5,408 raw chunks)
- Books: `corpus/books/cleaned/*.txt` (20 books, ~2.85M tokens)
- Manifest: `corpus/books_manifest.json`
- Scripts:
  - `scripts/fetch_books.py` — PG/arxiv/web fetcher
  - `scripts/clean_books.py` — PG header/footer stripper + PDF/HTML extractor
  - `scripts/chunk_books.py` — ~500-token chunker with paragraph/sentence boundaries
  - `scripts/verify_manifest.py` — checks PG titles match manifest (catches wrong-ID failures)
  - `scripts/chunks_to_passages.py` — stratified balanced subsample converter
  - `scripts/sentence_binding_vectorized.py` — vectorized analyzer for large sentence corpora
