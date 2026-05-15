"""
Concept-level cross-tradition convergence analysis.

Addresses the shared-placeholder bias in the v0.5-substituted experiment
(see methodology-notes.md). Instead of clustering whole substituted documents
(which artificially share placeholder tokens), this analysis:

  1. Uses the UNSUBSTITUTED corpus and its original embeddings — no
     substitution-induced similarity inflation.
  2. Tags each passage with which structural-role concepts it mentions
     (ULTIMATE, SUBSTRATE, AWARENESS, WORLD, SELF, RECOGNITION, NONSEP)
     using the same regex patterns from scripts/substitute.py.
  3. For each concept C, asks: are passages from DIFFERENT traditions
     that BOTH mention C more similar than passages from different
     traditions that DON'T share C?

The cleanly-interpretable headline is:

  concept_binding[C] = mean_sim( cross-tradition pairs where both mention C )
                       − mean_sim( cross-tradition pairs where exactly one mentions C )

If concept_binding[C] > 0 and statistically significant, then sharing
concept C does cross-tradition work beyond merely co-occurring in some
text. This is the cleaner test of "do these traditions converge on
*concept C* in particular?"

Also reports:
  - Per-concept "tradition coverage": which traditions mention C and how often.
  - Per-pair-of-traditions concept-binding scores: which tradition pairs
    are bound by which concepts.

Outputs to results/concept_analysis/.
"""

from __future__ import annotations

import csv
import json
import re
from itertools import combinations
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CORPUS = REPO_ROOT / "corpus" / "passages.jsonl"
DEFAULT_EMB = REPO_ROOT / "results" / "text-embedding-3-large" / "embeddings.npy"
DEFAULT_OUT = REPO_ROOT / "results" / "concept_analysis"


# Technical-only pattern variants.
# Drops common-English vocabulary from AWARENESS, ULTIMATE, WORLD, and
# RECOGNITION pattern dictionaries. Tests the §6.8 prediction from
# paper-draft-v4.md that the Phase 1a passage-level effect-size deflation
# is largely a vocabulary-breadth noise floor: passages tagged because
# they contain a common-English term ("consciousness", "God", "world")
# in non-technical context dilute the binding signal. Restricting tags
# to technical-only terms should recover effect sizes toward Phase 0 levels.
#
# SUBSTRATE, SELF, and NONSEP are unchanged — their dictionaries already
# contain only technical vocabulary; they serve as control baselines.
#
# Pre-registered predictions from paper-draft-v4.md §6.8:
#   AWARENESS: +0.026 → +0.08 to +0.11 (recovers toward Phase 0)
#   ULTIMATE: +0.014 → +0.04 to +0.06 (partial recovery)
#   WORLD:    +0.022 → +0.06 to +0.08 (substantial recovery)
#   RECOGNITION: +0.025 → +0.03 to +0.05 (already mostly technical)
#   SUBSTRATE: +0.054 → +0.054 (unchanged — no casual terms to drop)
TECHNICAL_ONLY_PATTERNS: dict[str, list[str]] = {
    "ULTIMATE": [
        # KEPT: tradition-specific divine names and technical philosophical terms
        # that never appear in casual English usage.
        r"\bbrahman\b",
        r"\btao\b",
        r"\bdao\b",
        r"\ballah\b",
        r"\bein sof\b",
        r"\bha[-\s]?shem\b",
        r"\bdharmakaya\b",
        r"\bdharma[-\s]?body\b",
        r"\bbuddha[-\s]?nature\b",
        r"\bthe one(?=\b)(?!\s+(who|that|which))",
        r"\bthe real\b",
        r"\bultimate reality\b",
        r"\bthe absolute\b",
        r"\bthe infinite\b",
        r"\bdivine ground\b",
        r"\bdivine essence\b",
        r"\bground of being\b",
        r"\bbasic ground\b",
        r"\bgroundless ground\b",
        r"\bsuchness\b",
        r"\btathata\b",
        r"\bcomputational substrate\b",
        r"\bmathematical structure\b",
        r"\bmathematical universe\b",
        # DROPPED: god, god's, gods, the divine, divine, lord, the creator,
        #          the holy one, holy spirit  (all common English)
    ],
    "SUBSTRATE": [
        # UNCHANGED: every term is already technical-only.
        r"\bthe implicate order\b",
        r"\bimplicate order\b",
        r"\bthe holomovement\b",
        r"\bholomovement\b",
        r"\bthe quantum vacuum\b",
        r"\bthe holographic principle\b",
        r"\bholographic\b",
        r"\bdependent origination\b",
        r"\bdependently arisen\b",
        r"\bbasic space\b",
        r"\bintegrated information\b",
        r"\bemptiness\b",
        r"\bshunyata\b",
        r"\b(s|ś)ūnyatā\b",
        r"\bsvabhava\b",
        r"\bnoumenon\b",
        r"\bnoumena\b",
        r"\bthing[-\s]?in[-\s]?itself\b",
    ],
    "AWARENESS": [
        # KEPT: tradition-specific consciousness terminology only.
        r"\bprimordial awareness\b",
        r"\bpure consciousness\b",
        r"\bpure awareness\b",
        r"\bbare awareness\b",
        r"\bnaked awareness\b",
        r"\brigpa\b",
        r"\bsat[-\s]?cit[-\s]?ananda\b",
        r"\bchit\b",
        r"\bchitta\b",
        r"\bcitta\b",
        r"\bnous\b",
        r"\bphi\b",
        # DROPPED: consciousness, awareness, sentience  (all common English)
    ],
    "WORLD": [
        # KEPT: tradition-specific names for the manifest/phenomenal world.
        r"\bthe ten thousand things\b",
        r"\bthe manifold of phenomena\b",
        r"\bthe simulation\b",
        r"\bancestor simulation\b",
        r"\ba simulation\b",
        r"\bsimulations\b",
        r"\bsimulation\b",
        r"\bsamsara\b",
        r"\bphenomenal world\b",
        r"\bphenomenal universe\b",
        r"\bthe ten thousand\b",
        # DROPPED: phenomenal (alone), creation, the cosmos, cosmos, the universe,
        #          spacetime, physical universe, physical reality, physical objects,
        #          appearance, appearances  (all common English)
    ],
    "SELF": [
        # UNCHANGED: dictionary is already small and tradition-specific.
        r"\batman\b",
        r"\bjiva\b",
        r"\bthe ego\b",
        r"\bthe empirical self\b",
        r"\bthe individual self\b",
        r"\bthe apparent self\b",
        r"\bthe agent\b",
        r"\bconscious agent\b",
        r"\bmarkov blanket\b",
    ],
    "RECOGNITION": [
        # KEPT: tradition-specific names for liberation/awakening.
        r"\bmoksha\b",
        r"\bmukti\b",
        r"\bnirvana\b",
        r"\bnibbana\b",
        r"\bsatori\b",
        r"\bbodhi\b",
        r"\btheosis\b",
        r"\bdeification\b",
        r"\bfana\b",
        r"\bbaqa\b",
        r"\bgnosis\b",
        r"\bjnana\b",
        r"\bself[-\s]realization\b",
        r"\bbeatific vision\b",
        # DROPPED: enlightenment, awakening, liberation, salvation  (common English)
    ],
    "NONSEP": [
        # UNCHANGED.
        r"\bnon[-\s]?duality\b",
        r"\bnon[-\s]?dual\b",
        r"\badvaita\b",
        r"\bwahdat al[-\s]?wujud\b",
        r"\bunity of being\b",
    ],
}


# Mapping from concept role to the set of regex patterns that detect it.
# Patterns are case-insensitive, word-boundary anchored where appropriate.
# Drawn from scripts/substitute.py.
CONCEPT_PATTERNS: dict[str, list[str]] = {
    "ULTIMATE": [
        r"\bthe holy one\b",
        r"\bthe one(?=\b)(?!\s+(who|that|which))",
        r"\bthe real\b",
        r"\bultimate reality\b",
        r"\bthe absolute\b",
        r"\bthe infinite\b",
        r"\bthe divine\b",
        r"\bdivine ground\b",
        r"\bdivine essence\b",
        r"\bground of being\b",
        r"\bbasic ground\b",
        r"\bgroundless ground\b",
        r"\bbuddha[-\s]?nature\b",
        r"\bdharma[-\s]?body\b",
        r"\bdharmakaya\b",
        r"\bein sof\b",
        r"\bha[-\s]?shem\b",
        r"\bthe creator\b",
        r"\bgod's\b",
        r"\bgods\b",
        r"\bgod\b",
        r"\ballah\b",
        r"\bbrahman\b",
        r"\btao\b",
        r"\bdao\b",
        r"\bsuchness\b",
        r"\btathata\b",
        r"\bdivine\b",
        r"\blord\b",
        r"\bcomputational substrate\b",
        r"\bmathematical structure\b",
        r"\bmathematical universe\b",
        r"\bholy spirit\b",
    ],
    "SUBSTRATE": [
        r"\bthe implicate order\b",
        r"\bimplicate order\b",
        r"\bthe holomovement\b",
        r"\bholomovement\b",
        r"\bthe quantum vacuum\b",
        r"\bthe holographic principle\b",
        r"\bholographic\b",
        r"\bdependent origination\b",
        r"\bdependently arisen\b",
        r"\bbasic space\b",
        r"\bintegrated information\b",
        r"\bemptiness\b",
        r"\bshunyata\b",
        r"\b(s|ś)ūnyatā\b",
        r"\bsvabhava\b",
        r"\bnoumenon\b",
        r"\bnoumena\b",
        r"\bthing[-\s]?in[-\s]?itself\b",
    ],
    "AWARENESS": [
        r"\bprimordial awareness\b",
        r"\bpure consciousness\b",
        r"\bpure awareness\b",
        r"\bbare awareness\b",
        r"\bnaked awareness\b",
        r"\brigpa\b",
        r"\bsat[-\s]?cit[-\s]?ananda\b",
        r"\bchit\b",
        r"\bchitta\b",
        r"\bcitta\b",
        r"\bnous\b",
        r"\bphi\b",
        r"\bconsciousness\b",
        r"\bawareness\b",
        r"\bsentience\b",
    ],
    "WORLD": [
        r"\bthe ten thousand things\b",
        r"\bthe manifold of phenomena\b",
        r"\bthe simulation\b",
        r"\bancestor simulation\b",
        r"\ba simulation\b",
        r"\bsimulations\b",
        r"\bsimulation\b",
        r"\bsamsara\b",
        r"\bphenomenal world\b",
        r"\bphenomenal universe\b",
        r"\bphenomenal\b",
        r"\bcreation\b",
        r"\bthe cosmos\b",
        r"\bcosmos\b",
        r"\bthe universe\b",
        r"\bspacetime\b",
        r"\bphysical universe\b",
        r"\bphysical reality\b",
        r"\bphysical objects?\b",
        r"\bappearances\b",
        r"\bappearance\b",
        r"\bthe ten thousand\b",
    ],
    "SELF": [
        r"\batman\b",
        r"\bjiva\b",
        r"\bthe ego\b",
        r"\bthe empirical self\b",
        r"\bthe individual self\b",
        r"\bthe apparent self\b",
        r"\bthe agent\b",
        r"\bconscious agent\b",
        r"\bmarkov blanket\b",
    ],
    "RECOGNITION": [
        r"\bmoksha\b",
        r"\bmukti\b",
        r"\bnirvana\b",
        r"\bnibbana\b",
        r"\benlightenment\b",
        r"\bawakening\b",
        r"\bsatori\b",
        r"\bbodhi\b",
        r"\btheosis\b",
        r"\bdeification\b",
        r"\bfana\b",
        r"\bbaqa\b",
        r"\bgnosis\b",
        r"\bjnana\b",
        r"\bself[-\s]realization\b",
        r"\bliberation\b",
        r"\bsalvation\b",
        r"\bbeatific vision\b",
    ],
    "NONSEP": [
        r"\bnon[-\s]?duality\b",
        r"\bnon[-\s]?dual\b",
        r"\badvaita\b",
        r"\bwahdat al[-\s]?wujud\b",
        r"\bunity of being\b",
    ],
}


def compile_concept_patterns() -> dict[str, re.Pattern]:
    return {
        c: re.compile("|".join(f"(?:{p})" for p in pats), flags=re.IGNORECASE)
        for c, pats in CONCEPT_PATTERNS.items()
    }


def tag_passages(passages: list[dict]) -> list[set[str]]:
    compiled = compile_concept_patterns()
    return [
        {c for c, pat in compiled.items() if pat.search(p["passage"])}
        for p in passages
    ]


def concept_binding_stats(
    sim: np.ndarray,
    passages: list[dict],
    tags: list[set[str]],
    concept: str,
) -> dict[str, float]:
    """
    For one concept C, compute:
      both_have:     mean cross-tradition similarity, both passages mention C
      only_one_has:  mean cross-tradition similarity, one passage mentions C
      neither_has:   mean cross-tradition similarity, neither mentions C

    The "concept binding" score = both_have - only_one_has. Positive means
    sharing C makes cross-tradition pairs more similar than pairs where
    only one passage mentions C (controlling for one-side mention).
    """
    n = len(passages)
    both_have, only_one_has, neither_has = [], [], []
    for i, j in combinations(range(n), 2):
        if passages[i]["tradition"] == passages[j]["tradition"]:
            continue  # only cross-tradition pairs
        has_i = concept in tags[i]
        has_j = concept in tags[j]
        s = float(sim[i, j])
        if has_i and has_j:
            both_have.append(s)
        elif has_i ^ has_j:
            only_one_has.append(s)
        else:
            neither_has.append(s)

    def m(xs):
        return float(np.mean(xs)) if xs else float("nan")

    def sd(xs):
        return float(np.std(xs, ddof=1)) if len(xs) > 1 else float("nan")

    return {
        "concept": concept,
        "n_passages_with": int(sum(1 for t in tags if concept in t)),
        "n_both_have": len(both_have),
        "both_have_mean": m(both_have),
        "both_have_sd": sd(both_have),
        "n_only_one_has": len(only_one_has),
        "only_one_has_mean": m(only_one_has),
        "only_one_has_sd": sd(only_one_has),
        "n_neither_has": len(neither_has),
        "neither_has_mean": m(neither_has),
        "concept_binding": m(both_have) - m(only_one_has),
    }


def permutation_test(
    sim: np.ndarray,
    passages: list[dict],
    tags: list[set[str]],
    concept: str,
    n_perm: int = 5000,
    seed: int = 0,
) -> dict[str, float]:
    """
    Null hypothesis: passages mentioning C are randomly distributed across
    cross-tradition similarity. Shuffle the concept-tag assignments (keeping
    counts the same), recompute concept_binding, build a null distribution.
    """
    rng = np.random.default_rng(seed)
    n = len(passages)

    # Indices of passages tagged with C in the real data
    real_idx = np.asarray([i for i, t in enumerate(tags) if concept in t])
    n_with = len(real_idx)
    if n_with == 0 or n_with == n:
        return {"observed": float("nan"), "p_one_sided": float("nan"), "n_perm": 0}

    def cb_from_mask(has_c: np.ndarray) -> float:
        both, only_one = [], []
        for i, j in combinations(range(n), 2):
            if passages[i]["tradition"] == passages[j]["tradition"]:
                continue
            hi, hj = has_c[i], has_c[j]
            if hi and hj:
                both.append(float(sim[i, j]))
            elif hi ^ hj:
                only_one.append(float(sim[i, j]))
        if not both or not only_one:
            return float("nan")
        return float(np.mean(both) - np.mean(only_one))

    real_mask = np.zeros(n, dtype=bool)
    real_mask[real_idx] = True
    observed = cb_from_mask(real_mask)

    perm_diffs = []
    indices = np.arange(n)
    for _ in range(n_perm):
        perm = rng.permutation(indices)
        permuted_idx = perm[:n_with]
        m = np.zeros(n, dtype=bool)
        m[permuted_idx] = True
        d = cb_from_mask(m)
        if not np.isnan(d):
            perm_diffs.append(d)

    null = np.asarray(perm_diffs)
    p_one_sided = float((null >= observed).mean())
    p_two_sided = float((np.abs(null) >= abs(observed)).mean())
    return {
        "observed": observed,
        "null_mean": float(null.mean()),
        "null_std": float(null.std()),
        "p_one_sided": p_one_sided,
        "p_two_sided": p_two_sided,
        "n_perm": int(len(null)),
    }


def per_tradition_concept_coverage(
    passages: list[dict], tags: list[set[str]]
) -> dict[str, dict[str, int]]:
    """Tradition × concept → count."""
    out: dict[str, dict[str, int]] = {}
    for p, t in zip(passages, tags):
        trad = p["tradition"]
        if trad not in out:
            out[trad] = {c: 0 for c in CONCEPT_PATTERNS}
        for c in t:
            out[trad][c] += 1
    return out


def per_pair_concept_binding(
    sim: np.ndarray,
    passages: list[dict],
    tags: list[set[str]],
    concept: str,
) -> dict[tuple[str, str], float]:
    """
    For each ordered pair of traditions (A, B) with A < B, compute mean
    similarity of cross-tradition passage pairs where both passages
    mention C.
    """
    out: dict[tuple[str, str], list[float]] = {}
    n = len(passages)
    for i, j in combinations(range(n), 2):
        ti, tj = passages[i]["tradition"], passages[j]["tradition"]
        if ti == tj:
            continue
        if concept not in tags[i] or concept not in tags[j]:
            continue
        key = tuple(sorted([ti, tj]))
        out.setdefault(key, []).append(float(sim[i, j]))
    return {k: float(np.mean(v)) for k, v in out.items()}


def main() -> None:
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--embeddings", type=Path, default=DEFAULT_EMB)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument(
        "--technical-only",
        action="store_true",
        help="Use TECHNICAL_ONLY_PATTERNS instead of CONCEPT_PATTERNS. "
        "Drops common-English vocabulary from AWARENESS, ULTIMATE, WORLD, "
        "RECOGNITION tag dictionaries; SUBSTRATE/SELF/NONSEP unchanged. "
        "Tests the §6.8 vocabulary-breadth-as-noise-floor prediction from "
        "paper-draft-v4.md.",
    )
    args = p.parse_args()

    CORPUS_PATH = args.corpus
    EMB_PATH = args.embeddings
    OUT_DIR = args.out

    # Swap in technical-only patterns if requested
    global CONCEPT_PATTERNS
    if args.technical_only:
        CONCEPT_PATTERNS = TECHNICAL_ONLY_PATTERNS
        print("Using TECHNICAL_ONLY_PATTERNS (drops common-English vocabulary)")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load
    passages: list[dict] = []
    with CORPUS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                passages.append(json.loads(line))
    emb = np.load(EMB_PATH)
    sim = emb @ emb.T

    print(f"Loaded {len(passages)} passages, embeddings shape {emb.shape}")

    # Tag
    tags = tag_passages(passages)
    n_tagged = sum(1 for t in tags if t)
    print(f"Tagged {n_tagged}/{len(passages)} passages with at least one concept")
    print()

    # Concept coverage by tradition
    coverage = per_tradition_concept_coverage(passages, tags)
    print("=== Per-tradition concept coverage (passage counts) ===")
    concepts_ordered = list(CONCEPT_PATTERNS.keys())
    header = ["tradition"] + concepts_ordered + ["total_passages"]
    rows = [header]
    for trad in sorted(coverage):
        row = [trad] + [coverage[trad].get(c, 0) for c in concepts_ordered]
        n_in_trad = sum(1 for p in passages if p["tradition"] == trad)
        row.append(n_in_trad)
        rows.append(row)
    col_widths = [max(len(str(r[i])) for r in rows) for i in range(len(header))]
    for r in rows:
        print("  " + "  ".join(str(v).ljust(w) for v, w in zip(r, col_widths)))
    print()

    with (OUT_DIR / "tradition_concept_coverage.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for r in rows:
            w.writerow(r)

    # Per-concept binding stats + permutation tests
    print("=== Per-concept binding (cross-tradition pairs only) ===")
    print(
        f"{'concept':<14} {'n_with':>6} {'both_n':>7} {'one_n':>7} "
        f"{'both_mn':>8} {'one_mn':>8} {'binding':>9} {'p1':>8} {'n_perm':>7}"
    )

    concept_results: list[dict] = []
    for c in CONCEPT_PATTERNS:
        stats = concept_binding_stats(sim, passages, tags, c)
        perm = permutation_test(sim, passages, tags, c, n_perm=2000)
        merged = {**stats, **{"p_one_sided": perm["p_one_sided"], "n_perm": perm["n_perm"]}}
        concept_results.append(merged)
        print(
            f"{c:<14} "
            f"{stats['n_passages_with']:>6} "
            f"{stats['n_both_have']:>7} "
            f"{stats['n_only_one_has']:>7} "
            f"{stats['both_have_mean']:>8.4f} "
            f"{stats['only_one_has_mean']:>8.4f} "
            f"{stats['concept_binding']:>+9.4f} "
            f"{perm['p_one_sided']:>8.4f} "
            f"{perm['n_perm']:>7}"
        )

    with (OUT_DIR / "concept_binding.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        keys = list(concept_results[0].keys())
        w.writerow(keys)
        for r in concept_results:
            w.writerow([r.get(k, "") for k in keys])

    # For the most strongly-binding concepts, write the tradition-pair breakdown
    print()
    print("=== Tradition-pair binding for top concepts ===")
    sorted_concepts = sorted(
        concept_results,
        key=lambda r: (r["concept_binding"] if not np.isnan(r["concept_binding"]) else -1),
        reverse=True,
    )
    for r in sorted_concepts:
        c = r["concept"]
        if r["n_both_have"] < 5:
            continue
        pair_means = per_pair_concept_binding(sim, passages, tags, c)
        top = sorted(pair_means.items(), key=lambda kv: kv[1], reverse=True)[:10]
        print(f"\n  {c} (binding={r['concept_binding']:+.4f}, p={r['p_one_sided']:.4f}):")
        for (a, b), v in top:
            print(f"    {a:<22} x {b:<22} {v:.4f}")

    print()
    print(f"\nOutputs written to {OUT_DIR}")


if __name__ == "__main__":
    main()
