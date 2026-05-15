# Corpus Notes (v0)

Phase 0 prototype corpus. This is *not* the rigorous corpus — it's the smallest plausible test of whether the signal is detectable at all. Read this before drawing conclusions from any results.

## Contents

`passages.jsonl` — one JSON object per line, with fields:

- `id` — stable identifier
- `tradition` — `advaita`, `dzogchen`, `christian_mystical`, `sufi`, `neoplatonism`, `kabbalah`, `daoism` (nondual); `catholic_scholastic`, `theravada`, `kantian` (dualistic); `humean`, `analytic` (non-contemplative)
- `category` — `nondual` | `dualistic` | `non_contemplative`
- `author` — primary author or tradition attribution
- `source` — text title or compilation reference
- `translator` — when known; otherwise `n/a` or `various`
- `era` — approximate century (e.g. `3c`, `13c`, `18c`)
- `source_status` — see below
- `passage` — the text itself

### `source_status` values

- `quote` — high-confidence direct quotation from a published English source. Verify before any rigorous run.
- `approximate` — close to a published quotation, with potential minor variation in wording. Verify before any rigorous run.
- `paraphrase` — a doctrinally faithful rendering of a recurring teaching, not lifted from a specific edition. Useful for embeddings (semantics dominate) but should be replaced with verified quotations before a rigorous run.

Approximately one-third to half of the v0 corpus is `paraphrase` or `approximate`. This is acceptable for Phase 0 (the goal is to detect signal in semantic space, not to publish quotations), but it would not survive peer review. Phase 1 must use verified sources.

## Counts (v0.5)

**Nondual: 107 passages across 18 traditions**

- *Historical contemplative (58):* Advaita 10, Dzogchen 7, Christian mystical 10, Sufi 7, Neoplatonism 6, Kabbalah 6, Daoism 6, Mahayana 6 (new in v0.5)
- *Modern scientific/computational (25):* Simulation theory 6, Information physics 6, Mathematical universe 5, Analytic idealism 4, Interface theory 4
- *Bridge thinkers (24, new in v0.5):* Implicate order / Bohm 5, Process philosophy / Whitehead 5, Predictive processing / Friston-Clark-Seth 5, IIT / Tononi-Koch 4, Relational QM / Rovelli 5

**Dualistic: 24 passages across 3 traditions** — Catholic scholastic 8, Theravada 8, Kantian 8

**Non-contemplative: 12 passages across 2 traditions** — Humean 6, Analytic/Russell 6

**Grand total: 143**

### v0 vs v0.5 changes

v0.5 added 36 passages, focused on the open question raised by the v0 result: *is the modern-historical cluster gap real content or vocabulary effect?*

- **Bridge thinkers** (Bohm, Whitehead, Friston/Clark/Seth, Tononi/Koch, Rovelli) — these authors write with one foot in scientific vocabulary and one in contemplative content. Their cluster position will be informative: if they sit between modern-computational and historical-nondual, the gap is real and there's a gradient. If they fall to one side based on vocabulary, the gap is mostly vocabulary.
- **Mahayana** — adds a major historical nondual tradition (Heart Sutra, Diamond Sutra, Nagarjuna, Avatamsaka) that was missing in v0.
- **Within-tradition additions** for advaita, christian_mystical, sufi, dzogchen — stronger per-tradition statistics; tests whether v0 results are stable to within-tradition variation.

The methodology and analysis pipeline are unchanged from v0. This is a "more data, same method" comparison run.

## Known limitations

These are intentional for the v0 prototype but must be addressed for any rigorous run:

1. **English-only.** All texts are in English, regardless of original language. Conflates "convergence in source content" with "convergence of English-language translation conventions." Mitigation in v1: vocabulary-substitution test; multi-translator inclusion.
2. **Single-translator per source.** v1 needs multiple translations of the same source to control for translator style.
3. **Paraphrases present.** v1 needs all quotations verified against primary editions.
4. **Selection bias.** Passages were chosen for representativeness, but "representative" is a judgment call. v1 needs explicit inclusion/exclusion criteria, ideally informed by secondary scholarship (Stace, Forman, Hood, tradition-specific scholars).
5. **Coverage gaps.** Important nondual sources are missing: Tibetan Mahamudra texts beyond Tilopa, Christian mystics beyond Eckhart/John of the Cross/Pseudo-Dionysius (Cloud of Unknowing, Boehme, Teresa, etc.), more Sufi sources, more Hasidic sources, Mahayana sutras (Heart Sutra, Diamond Sutra) which are arguably nondual.
6. **No translator metadata on some legacy sources.** Several Daoism passages list "various" — v1 should pin specific editions.

## Verification before rigorous use

Before any pre-registration or publication-track analysis, every passage marked `quote` or `approximate` should be checked against the primary source. Every `paraphrase` should be replaced with a verified quotation from the same author covering the same doctrinal point, *or* clearly labeled as a paraphrase in any writeup.

## License / use

Passages are excerpts and paraphrases used for non-commercial research. Many sources are public domain (Plotinus, Eckhart, Shankara, Kant, Hume); some modern translations are under copyright and used here under fair-use research excerpts. For redistribution or rigorous publication, the corpus needs a clean rights review.

## Reproducing

```
pip install -r ../requirements.txt
python ../scripts/prototype.py
```

Outputs land in `../results/<model_name>/`. Inspect `summary.txt` first, then the UMAP plot.
