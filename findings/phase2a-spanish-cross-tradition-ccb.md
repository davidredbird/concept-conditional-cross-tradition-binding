# Phase 2a: cross-tradition CCB in Spanish (Quietist × Carmelite)

**Date:** 2026-05-20  **Status:** EXPLORATORY (not pre-registered)
**Scripts:** `fetch_spanish_texts.py`, `spanish_gate_prep.py`, `phase1c2_cross_tradition_ccb.py`
**Outputs:** `results/phase2a/spanish_molinos_teresa_ccb_labse.json`

Source: es.wikisource (original Castilian).

| text | tradition | category | chunks |
|---|---|---|---|
| Guía Espiritual (Molinos) | quietist (passive union / "nada") | nondual | 287 |
| Su Vida (Teresa de Ávila) | carmelite (affective mysticism) | dualistic | 586 |

Note: Spain's Muslim/Jewish traditions wrote in Arabic/Hebrew, so native Castilian
tradition text is overwhelmingly Christian. This is an **intra-Christian-school**
contrast (Quietist vs Carmelite), not separate lineages — high vocabulary overlap.

## Result (LaBSE; cross-tradition cosine 0.584 ± 0.070 — resolves)

| concept | CCB | p |
|---|---|---|
| ULTIMATE | +0.040 | <.0001 BIND |
| AWARENESS | +0.037 | <.0001 BIND |
| WORLD | +0.023 | <.0001 BIND |
| SELF | +0.020 | .001 BIND |
| SUBSTRATE | +0.020 | <.0001 BIND |
| RECOGNITION | +0.015 | <.0001 BIND |
| NONSEP | +0.007 | .085 no |

5/5 Phase-1a concepts bind, AWARENESS strongly (+0.037 — among the largest
AWARENESS effects of any configuration).

## Fit: confirms the vocabulary-overlap GRADIENT

Spanish is the **highest-overlap** configuration tested — Molinos and Teresa share
essentially the entire Spanish Catholic mystical lexicon (alma, conciencia,
contemplación, entendimiento, unión). Per the framework, maximal awareness-
vocabulary overlap → strongest AWARENESS binding, and indeed AWARENESS is +0.037.

This sits cleanly on the gradient:
- **Spanish (two mystical schools, max overlap):** AWARENESS +0.037 (strongest)
- **Arabic / Hindi (shared lineage):** AWARENESS +0.01–0.02
- **English / French / Japanese (translation-imposed overlap):** AWARENESS binds
- **Hebrew (mystical vs RATIONALIST — divergent register):** AWARENESS flat
- **Chinese (separate lineage, distinct lexicon):** AWARENESS flat

The gap that kills AWARENESS binding is *vocabulary divergence* — by register
(Hebrew) or lineage (Chinese). Where the awareness-lexicon overlaps (everywhere
else), AWARENESS binds, more strongly the more it overlaps.

## Spanish option #2 (same-author translation test) — BLOCKED

The plan to compare original-Spanish vs French-translated **John of the Cross**
(same author) is blocked: John of the Cross's *prose* is not on es.wikisource (only
his poems). Would require cervantesvirtual scraping. Deferred.

## Caveats

- Intra-Christian-school contrast (Quietist vs Carmelite) — weaker "cross-tradition"
  than the lineage-separate pairs; high overlap is expected and explains the strong AWARENESS.
- ULTIMATE near-saturated (Dios everywhere).
- Spanish Option-A dict: hidden DoF, Christian-lean.
- Single model (LaBSE); exploratory.
