# Phase 1a — lexical-overlap controls: random-word, bag-of-words, and tag-masking

**Date:** 2026-07-05  **Status:** robustness follow-up (English Phase 1a passages only;
firewall-safe). Script: `scripts/phase1a_lexical_controls.py` (`--control
random|bow|mask|all`, seed=1908). Raw numbers: `results/robustness/lexical_controls.json`.

**Why this exists.** A blind review of Draft 8 named the deepest untreated threat to the
English CCB results: both-tagged passages share dictionary terms *by construction*, and
embedding similarity is partly lexical, so positive CCB could reduce to "documents sharing
words are more similar." The permutation null tests chance, not this mechanism. Three
direct controls were prescribed and are run here on the Phase 1a passage corpus (920
passages, OpenAI text-embedding-3-large cached embeddings, 379,468 cross-tradition pairs).
NONSEP has zero tagged passages in this corpus and is untestable throughout; SELF does not
bind in the real data and serves as an internal reference.

## Control 1 — frequency-matched random-word CCB

For each concept, 50 pseudo-concepts were built from random corpus vocabulary (real
dictionary terms excluded), each matched to the real concept's tagged-passage count within
±10%. CCB computed on the same embeddings.

| concept | real CCB | pseudo mean ± sd | real percentile |
|---|---|---|---|
| WORLD | +0.0216 | +0.0043 ± ~0.003 | **100** |
| ULTIMATE | +0.0141 | +0.0048 ± 0.0050 | **98** |
| AWARENESS | +0.0258 | +0.0069 ± 0.0144 | 88 |
| SUBSTRATE | +0.0541 | +0.0208 ± 0.0263 | 86 |
| RECOGNITION | +0.0247 | +0.0114 | 84 |
| SELF | −0.0124 | +0.0120 | 4 |

Two readings. First, **a generic lexical-overlap floor exists**: arbitrary same-prevalence
word sets produce positive CCB on average (+0.004 to +0.021), so raw CCB values should
never be read as pure concept signal. Second, the real concepts sit in the upper tail of
the matched-random distribution (84th–100th percentile), with WORLD and ULTIMATE clearing
it decisively and AWARENESS/SUBSTRATE/RECOGNITION above the median but short of the 95th
percentile at 50 draws. SELF, which does not bind in the real data, sits at the 4th
percentile: the tagger fires but the contexts do not converge, which is what a
non-converging concept should look like.

## Control 2 — bag-of-words (tf-idf) CCB baseline

Same tags, same permutation test, similarity from L2-normalized tf-idf vectors instead of
embeddings. This measures how much binding a purely lexical model reproduces.

| concept | embedding CCB (p) | tf-idf CCB (p) |
|---|---|---|
| ULTIMATE | +0.0141 (<.001) | +0.0094 (<.001) |
| SUBSTRATE | +0.0541 (<.001) | +0.0327 (.003) |
| AWARENESS | +0.0258 (<.001) | +0.0332 (<.001) |
| WORLD | +0.0216 (<.001) | +0.0161 (<.001) |
| SELF | −0.0124 (n.s.) | **+0.0463 (<.001)** |
| RECOGNITION | +0.0247 (<.001) | **+0.0063 (.14, n.s.)** |

Correlation of the two profiles across the 6 testable concepts: **r = −0.23**. A lexical
model does produce binding (there is a real lexical component), but it produces a
*different concept profile* than the embeddings do. The two dissociations are the
informative part: RECOGNITION binds in embedding space but not lexically (its binding is
carried by context, not shared strings), while SELF binds lexically but NOT in embedding
space (shared self-vocabulary whose surrounding contexts do not converge — the embedding
statistic correctly refuses a binding that a lexical statistic would have granted).
Embedding CCB is therefore not reducible to tf-idf overlap.

## Control 3 — tag-term masking

Every substring matched by a concept's dictionary was deleted from that concept's tagged
passages; the masked passages were re-embedded (same model); CCB recomputed with the
original tags. Binding that survives is carried by surrounding context, not the tag
strings.

| concept | original CCB | masked CCB (p) | retained |
|---|---|---|---|
| SUBSTRATE | +0.0541 | +0.0456 (.003) | 84% |
| AWARENESS | +0.0258 | +0.0231 (<.001) | 90% |
| RECOGNITION | +0.0247 | +0.0210 (<.001) | 85% |
| WORLD | +0.0216 | +0.0171 (<.001) | 79% |
| ULTIMATE | +0.0141 | +0.0090 (.0015) | 64% |
| SELF | −0.0124 | −0.0085 (n.s.) | (n.s. both) |

**All five binding concepts remain significant with their tag terms deleted**, retaining
64–90% of the original magnitude. This is the strongest of the three controls and the most
direct answer to the reviewer's threat model: the shared dictionary strings are not what
the binding is made of.

## Bottom line

The English Phase 1a CCB results substantially survive the lexical-overlap challenge:

1. **Masking (decisive):** binding survives deletion of the tag terms themselves, at
   64–90% magnitude, all five concepts still significant.
2. **BoW (supporting):** the lexical-model profile diverges from the embedding profile
   (r = −0.23), with RECOGNITION semantic-not-lexical and SELF lexical-not-semantic.
3. **Random-word (calibrating):** a generic positive lexical floor exists and real
   concepts sit above it (84th–100th percentile), though three concepts fall short of the
   95th percentile at 50 draws; raw CCB magnitudes overstate concept-specific signal by
   roughly the pseudo-mean for that prevalence.

Going forward, CCB results should be reported alongside the matched-random floor for the
concept's prevalence, and masking should be the standard robustness check for any new
corpus.

## Caveats

- Passage-level only (n=920); the sentence-level replication of these controls is future
  work (the claims they defend replicate at sentence level, the controls do not yet).
- Single embedding model for the controls (text-embedding-3-large); the underlying English
  findings are two-model, the controls are not yet.
- 50 pseudo-draws per concept bounds percentile resolution at 2%.
- NONSEP untestable on this corpus (zero tagged passages at passage granularity).
- Control 3 re-embeds only tagged passages (untagged rows unchanged), which is exactly the
  comparison the threat model requires but means masked and unmasked rows mix in the
  matrix.
- This experiment was specified by an external blind review before any of its results were
  seen; the script and spec were written before Control 1's first output.
