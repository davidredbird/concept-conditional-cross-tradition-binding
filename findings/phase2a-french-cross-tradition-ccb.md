# Phase 2a: cross-tradition CCB in French (Daoist × Vedanta × Christian)

**Date:** 2026-05-20  **Status:** EXPLORATORY (not pre-registered)
**Scripts:** `fetch_french_texts.py`, `french_gate_prep.py`,
`phase1c2_cross_tradition_ccb.py`, `within_language_concept_binding.py`
**Outputs:** `results/phase2a/french_ccb_{e5,labse}.json`

French = a second high-resource language, but at the **high-westernization** end of
the axis: all three sources are 19th-century Western renderings. This is the
deliberate contrast against classical Chinese (original-language, zero-westernization).

## Corpora (fr.wikisource, all PD)

| text | tradition | chunks | source |
|---|---|---|---|
| Tao Te King (Stanislas Julien, 1842; verse only, commentary cut) | daoism | 92 | Daoist |
| La Bhagavad-Gîtâ (Émile Burnouf, 1861) | vedanta | 158 | Hindu |
| Œuvres spirituelles de Jean de la Croix (core mystical works) | christian | 309 | Christian |

## Result — phenomenological concepts bind in French (LaBSE)

| concept | French CCB (LaBSE) | for contrast: classical Chinese |
|---|---|---|
| **RECOGNITION** | **+0.029 (p<.0001) BIND** | untestable (no Daoist tags) |
| **AWARENESS** | **+0.026 (p<.0001) BIND** | **flat: −0.000 (p=.47)** |
| WORLD | +0.021 (p<.0001) BIND | binds |
| SELF (non-1a) | +0.020 (p=.001) bind | — |
| ULTIMATE | +0.019 (p<.0001) BIND | binds |
| NONSEP | +0.014 (p=.09) no | untestable |
| SUBSTRATE | +0.003 (p=.34) **no** | **binds (cleanest, +.042–.054)** |

**4/5 Phase-1a concepts bind, including BOTH AWARENESS and RECOGNITION (H1c.2.b
SUPPORTED)** — the first original-script... no: the first *non-English* corpus in
which the Phase 1a phenomenological signal reappears. e5 cone-collapsed French too
(0.839 ± 0.020) but still flags AWARENESS/WORLD/SUBSTRATE at tiny effect; LaBSE
(0.429 ± 0.072) is the resolving model.

**Control (within-French-Christian / Jean de la Croix, LaBSE):** AWARENESS +0.021
(p<.0001), RECOGNITION +0.022 (p=.0005), ULTIMATE +0.053, WORLD +0.019, NONSEP
+0.071 — 5/7 resolve within-tradition. So the cross-tradition binding is real, not
a resolution artifact.

## The cross-linguistic dissociation (the headline)

The phenomenological concepts (AWARENESS, RECOGNITION) and the emptiness concept
(SUBSTRATE) **swap** between the two languages:

- **classical Chinese (Buddhist × Daoist):** SUBSTRATE binds cleanly; AWARENESS flat.
- **French (Daoist × Vedanta × Christian):** AWARENESS + RECOGNITION bind; SUBSTRATE flat.
- WORLD and ULTIMATE bind in both.

## Interpretation — and the confound that blocks the clean conclusion

This is the dissociation the multilingual phase was designed to surface. Two
explanations differ between the two tests, and they are **confounded** here:

1. **Language / translation (the artifact hypothesis).** French is three 19th-century
   *Western translations*; their translators may render Daoist/Hindu/Christian
   awareness-language with a shared French vocabulary (conscience, esprit,
   contemplation, intelligence, lumière), manufacturing convergence that the
   original-language Chinese lacks. This would mean the Phase 1a English AWARENESS
   headline is at least partly **translation-mediated**.
2. **Tradition composition (the substantive hypothesis).** French pairs Vedanta +
   Christian — both *union-with-the-divine/Self via awareness* mysticisms that may
   genuinely share phenomenological structure — whereas the Chinese pair is
   Buddhist × Daoist, East-Asian traditions whose emptiness vocabulary (空 / 無為)
   converges instead. On this reading the swap is real: AWARENESS/RECOGNITION are a
   Vedanta–Christian shared structure, SUBSTRATE a Buddhist–Daoist shared structure.

**These cannot be separated by this experiment**, because language and
tradition-composition vary together. The decisive disambiguator is to **hold the
tradition pair fixed and vary only the language**:

> **English Buddhist × Daoist CCB** (same pair as the Chinese test, Western
> language). If AWARENESS binds there but not in Chinese, language/translation is
> implicated with tradition held constant → artifact hypothesis gains strong support.
> We already have the English Buddhist + Daoist corpora (Phase 1a/1b); this needs
> no new sourcing and should be the next run.

## Caveats

- **All three French texts are 19th-c. translations** → shared translator-era French
  prose style is a confound; some cross-tradition similarity is "all 19th-c. French,"
  which is exactly the westernization signal but limits any "structural" claim.
- LaBSE is the only resolving model (e5 collapsed); not a cross-model replication.
- ULTIMATE near-saturated (Dieu/divin/Seigneur everywhere; JdlC 279/309) → its
  binding is the least interpretable.
- French Option-A dictionary: hidden DoF + Christian/European vocabulary lean.
- Minor embedded Spanish canticle stanzas in the Jean de la Croix source.
- Tradition composition differs from the Chinese test (Vedanta + Christian vs
  Buddhist) — the core confound above.
- EXPLORATORY, not pre-registered.

## Where this leaves the AWARENESS question

Two non-English tests now bracket the Phase 1a AWARENESS headline:
- **classical Chinese (original, East-Asian, Buddhist×Daoist):** AWARENESS does NOT bind.
- **French (Western translations, Vedanta/Christian/Daoist):** AWARENESS DOES bind.

The pattern is consistent with — but does not yet prove — the reading that AWARENESS
convergence rides on shared Western/translation vocabulary and/or the Vedanta–Christian
mystical family, not on a universal cross-lineage structure. SUBSTRATE shows the
mirror-image profile. **Next: English Buddhist×Daoist to hold tradition fixed.**
