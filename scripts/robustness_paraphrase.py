"""
Robustness check: does the H1 signal survive on the non-paraphrase subset of the v0.5 corpus?

Loads the cached embeddings and reruns the headline H1 permutation test:
  - on the full v0.5 corpus (baseline)
  - on the quote-only subset
  - on the quote-OR-approximate subset (paraphrase-excluded)
  - on the paraphrase-only subset (for comparison)

Also reports concept-binding for the five binding concepts on each subset.

Addresses reviewer concern that paraphrases may carry the investigator's prior
beliefs and inflate the convergence signal.
"""

from __future__ import annotations

import json
import re
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS = REPO_ROOT / "corpus" / "passages.jsonl"
EMB = REPO_ROOT / "results" / "text-embedding-3-large" / "embeddings.npy"

# Reuse the concept-binding patterns from concept_analysis.py
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from concept_analysis import CONCEPT_PATTERNS  # noqa: E402


def compile_patterns():
    return {
        c: re.compile("|".join(f"(?:{p})" for p in pats), flags=re.IGNORECASE)
        for c, pats in CONCEPT_PATTERNS.items()
    }


# Same nondual/dualistic split the prototype.py uses.
NONDUAL_CATEGORIES = {"nondual"}
DUALISTIC_CATEGORIES = {"dualistic"}

HISTORICAL_NONDUAL_TRADS = {
    "advaita",
    "dzogchen",
    "christian_mystical",
    "sufi",
    "neoplatonism",
    "kabbalah",
    "daoism",
    "mahayana",
}


def load() -> tuple[list[dict], np.ndarray]:
    passages: list[dict] = []
    with CORPUS.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                passages.append(json.loads(line))
    emb = np.load(EMB)
    # Just in case: ensure unit-normalized for cosine
    emb = emb / np.linalg.norm(emb, axis=1, keepdims=True)
    return passages, emb


def pair_means(passages, sim, idx_mask):
    """Compute key pairwise means restricted to passages whose mask is True."""
    idx = [i for i, m in enumerate(idx_mask) if m]
    nondual_cross = []
    nondual_to_dual = []
    dual_dual = []
    same_trad = []
    for i, j in combinations(idx, 2):
        pi, pj = passages[i], passages[j]
        ci, cj = pi["category"], pj["category"]
        ti, tj = pi["tradition"], pj["tradition"]
        s = float(sim[i, j])
        if ti == tj:
            same_trad.append(s)
            continue
        ci_n = ci in NONDUAL_CATEGORIES
        cj_n = cj in NONDUAL_CATEGORIES
        ci_d = ci in DUALISTIC_CATEGORIES
        cj_d = cj in DUALISTIC_CATEGORIES
        if ci_n and cj_n:
            # Only count historical nondual × historical nondual for H1
            if ti in HISTORICAL_NONDUAL_TRADS and tj in HISTORICAL_NONDUAL_TRADS:
                nondual_cross.append(s)
        elif (ci_n and cj_d) or (ci_d and cj_n):
            if (ci_n and ti in HISTORICAL_NONDUAL_TRADS) or (cj_n and tj in HISTORICAL_NONDUAL_TRADS):
                nondual_to_dual.append(s)
        elif ci_d and cj_d:
            dual_dual.append(s)
    return {
        "n_passages": len(idx),
        "n_same_trad_pairs": len(same_trad),
        "same_trad_mean": float(np.mean(same_trad)) if same_trad else float("nan"),
        "n_nondual_cross": len(nondual_cross),
        "nondual_cross_mean": float(np.mean(nondual_cross)) if nondual_cross else float("nan"),
        "n_nondual_to_dual": len(nondual_to_dual),
        "nondual_to_dual_mean": float(np.mean(nondual_to_dual)) if nondual_to_dual else float("nan"),
        "n_dual_dual": len(dual_dual),
        "dual_dual_mean": float(np.mean(dual_dual)) if dual_dual else float("nan"),
        "delta_H1": (
            (float(np.mean(nondual_cross)) - float(np.mean(nondual_to_dual)))
            if nondual_cross and nondual_to_dual
            else float("nan")
        ),
    }


def permutation_test_h1(passages, sim, idx_mask, n_perm=5000, seed=0):
    """
    Permute (tradition, category) labels among the active indices and recompute Δ_H1.
    """
    rng = np.random.default_rng(seed)
    active_idx = [i for i, m in enumerate(idx_mask) if m]
    n = len(active_idx)
    if n < 4:
        return {"observed": float("nan"), "p_one_sided": float("nan"), "n_perm": 0}
    # Real labels
    labels = [(passages[i]["tradition"], passages[i]["category"]) for i in active_idx]
    sub_sim = sim[np.ix_(active_idx, active_idx)]

    def delta_from_labels(labs):
        nondual_cross = []
        nondual_to_dual = []
        for i, j in combinations(range(n), 2):
            ti, ci = labs[i]
            tj, cj = labs[j]
            if ti == tj:
                continue
            s = float(sub_sim[i, j])
            ci_n = ci in NONDUAL_CATEGORIES
            cj_n = cj in NONDUAL_CATEGORIES
            ci_d = ci in DUALISTIC_CATEGORIES
            cj_d = cj in DUALISTIC_CATEGORIES
            if ci_n and cj_n:
                if ti in HISTORICAL_NONDUAL_TRADS and tj in HISTORICAL_NONDUAL_TRADS:
                    nondual_cross.append(s)
            elif (ci_n and cj_d) or (ci_d and cj_n):
                if (ci_n and ti in HISTORICAL_NONDUAL_TRADS) or (cj_n and tj in HISTORICAL_NONDUAL_TRADS):
                    nondual_to_dual.append(s)
        if not nondual_cross or not nondual_to_dual:
            return float("nan")
        return float(np.mean(nondual_cross) - np.mean(nondual_to_dual))

    observed = delta_from_labels(labels)
    null = []
    arr = np.arange(n)
    for _ in range(n_perm):
        perm = rng.permutation(arr)
        permuted = [labels[k] for k in perm]
        d = delta_from_labels(permuted)
        if not np.isnan(d):
            null.append(d)
    null_arr = np.asarray(null)
    p_one = float((null_arr >= observed).mean()) if len(null_arr) else float("nan")
    return {
        "observed": observed,
        "null_mean": float(null_arr.mean()) if len(null_arr) else float("nan"),
        "null_std": float(null_arr.std()) if len(null_arr) else float("nan"),
        "p_one_sided": p_one,
        "n_perm": int(len(null_arr)),
    }


def concept_binding_subset(passages, sim, idx_mask, concept_pat):
    """Compute concept binding restricted to active indices."""
    tagged = [bool(concept_pat.search(p["passage"])) for p in passages]
    idx = [i for i, m in enumerate(idx_mask) if m]
    both, only_one = [], []
    for i, j in combinations(idx, 2):
        if passages[i]["tradition"] == passages[j]["tradition"]:
            continue
        ti = tagged[i]
        tj = tagged[j]
        s = float(sim[i, j])
        if ti and tj:
            both.append(s)
        elif ti ^ tj:
            only_one.append(s)
    if not both or not only_one:
        return {"n_both": len(both), "n_only_one": len(only_one), "binding": float("nan")}
    return {
        "n_both": len(both),
        "n_only_one": len(only_one),
        "both_mean": float(np.mean(both)),
        "only_one_mean": float(np.mean(only_one)),
        "binding": float(np.mean(both) - np.mean(only_one)),
    }


def main():
    passages, emb = load()
    sim = emb @ emb.T
    statuses = [p["source_status"] for p in passages]

    subsets = {
        "all": [True] * len(passages),
        "quote_only": [s == "quote" for s in statuses],
        "quote_or_approximate": [s in ("quote", "approximate") for s in statuses],
        "paraphrase_only": [s == "paraphrase" for s in statuses],
    }

    print("=" * 78)
    print("H1 robustness across source_status subsets (historical nondual cross-tradition)")
    print("=" * 78)
    print(f"{'subset':<24s} {'n':>4s} {'nxn':>6s} {'nxd':>6s} {'mn_nd':>7s} {'mn_dl':>7s} {'dH1':>7s} {'p':>7s}")
    for name, mask in subsets.items():
        pm = pair_means(passages, sim, mask)
        if pm["n_nondual_cross"] < 2 or pm["n_nondual_to_dual"] < 2:
            print(f"{name:<24s} {pm['n_passages']:>4d}  insufficient pairs")
            continue
        perm = permutation_test_h1(passages, sim, mask, n_perm=5000)
        print(
            f"{name:<24s} {pm['n_passages']:>4d} "
            f"{pm['n_nondual_cross']:>6d} "
            f"{pm['n_nondual_to_dual']:>6d} "
            f"{pm['nondual_cross_mean']:>7.4f} "
            f"{pm['nondual_to_dual_mean']:>7.4f} "
            f"{pm['delta_H1']:>+7.4f} "
            f"{perm['p_one_sided']:>7.4f}"
        )

    print()
    print("=" * 78)
    print("Concept-binding by subset (cross-tradition pairs only)")
    print("=" * 78)
    patterns = compile_patterns()
    for concept in ("AWARENESS", "RECOGNITION", "WORLD", "ULTIMATE", "SUBSTRATE"):
        pat = patterns[concept]
        print(f"\n{concept}:")
        print(f"  {'subset':<24s} {'n_both':>7s} {'n_one':>7s} {'binding':>9s}")
        for name, mask in subsets.items():
            r = concept_binding_subset(passages, sim, mask, pat)
            if np.isnan(r["binding"]):
                print(f"  {name:<24s} {r['n_both']:>7d} {r['n_only_one']:>7d}   n/a")
            else:
                print(f"  {name:<24s} {r['n_both']:>7d} {r['n_only_one']:>7d} {r['binding']:>+9.4f}")


if __name__ == "__main__":
    main()
