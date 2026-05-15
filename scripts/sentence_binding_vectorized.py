"""
Vectorized concept-binding analysis on already-embedded sentences.

Loads sentences.jsonl + embeddings.npy from a previous run of
sentence_concept_analysis.py, subsamples to a manageable size if needed,
and runs concept-binding + permutation tests using numpy boolean masks
instead of Python itertools.combinations (which is intractable at n=14k).

Vectorization speedup: O(n²) Python iterations per concept becomes a
handful of n×n boolean and float operations. 14k sentences becomes
tractable in seconds per concept rather than years.

Usage:
  python scripts/sentence_binding_vectorized.py --dir results/sentence_concept_analysis/openai/text-embedding-3-large
  python scripts/sentence_binding_vectorized.py --dir results/sentence_concept_analysis/onnx/sentence-transformers__all-MiniLM-L6-v2 --max 3000
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

import numpy as np


def load(dir_path: Path) -> tuple[list[dict], np.ndarray]:
    sentences: list[dict] = []
    with (dir_path / "sentences.jsonl").open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                sentences.append(json.loads(line))
    emb = np.load(dir_path / "embeddings.npy")
    assert len(sentences) == emb.shape[0], (len(sentences), emb.shape)
    return sentences, emb


def stratified_subsample(
    sentences: list[dict], emb: np.ndarray, max_n: int, seed: int = 0
) -> tuple[list[dict], np.ndarray]:
    """Sample uniformly per book to a target total size."""
    if len(sentences) <= max_n:
        return sentences, emb

    rng = np.random.default_rng(seed)
    by_book: dict[str, list[int]] = {}
    for i, s in enumerate(sentences):
        bid = s["passage_id"].rsplit("::", 1)[0] if "::" in s["passage_id"] else s["passage_id"]
        by_book.setdefault(bid, []).append(i)

    per_book_cap = max(1, max_n // len(by_book))

    selected: list[int] = []
    for bid, idxs in by_book.items():
        if len(idxs) <= per_book_cap:
            selected.extend(idxs)
        else:
            selected.extend(rng.choice(idxs, size=per_book_cap, replace=False).tolist())

    # If still over cap (e.g., uneven), trim randomly
    if len(selected) > max_n:
        selected = rng.choice(selected, size=max_n, replace=False).tolist()
    selected.sort()

    return [sentences[i] for i in selected], emb[selected]


CONCEPTS = ["ULTIMATE", "SUBSTRATE", "AWARENESS", "WORLD", "SELF", "RECOGNITION", "NONSEP"]


def concept_binding_vec(
    sim: np.ndarray,
    has_c: np.ndarray,
    cross_mask: np.ndarray,
) -> tuple[float, float, float, int, int]:
    """
    Vectorized concept binding for a single concept.
    has_c: boolean (n,) -- true if sentence mentions the concept
    cross_mask: boolean (n,n) -- true for cross-tradition upper-triangle pairs
    Returns (both_mean, only_one_mean, diff, n_both, n_only_one)
    """
    both_mask = has_c[:, None] & has_c[None, :] & cross_mask
    only_one_mask = (has_c[:, None] ^ has_c[None, :]) & cross_mask

    n_both = int(both_mask.sum())
    n_only_one = int(only_one_mask.sum())

    both_mean = float((sim * both_mask).sum() / max(n_both, 1)) if n_both else float("nan")
    only_one_mean = float((sim * only_one_mask).sum() / max(n_only_one, 1)) if n_only_one else float("nan")
    return both_mean, only_one_mean, both_mean - only_one_mean, n_both, n_only_one


def permutation_pval_vec(
    sim: np.ndarray,
    has_c: np.ndarray,
    cross_mask: np.ndarray,
    n_perm: int = 2000,
    seed: int = 0,
) -> tuple[float, float, float, float]:
    """Permutation test (vectorized within each permutation)."""
    rng = np.random.default_rng(seed)
    n = len(has_c)
    n_with = int(has_c.sum())
    if n_with == 0 or n_with == n:
        return float("nan"), float("nan"), float("nan"), float("nan")

    _, _, observed, _, _ = concept_binding_vec(sim, has_c, cross_mask)

    diffs = np.empty(n_perm, dtype=np.float64)
    for k in range(n_perm):
        m = np.zeros(n, dtype=bool)
        m[rng.permutation(n)[:n_with]] = True
        _, _, d, _, _ = concept_binding_vec(sim, m, cross_mask)
        diffs[k] = d

    null = diffs[~np.isnan(diffs)]
    return (
        observed,
        float(null.mean()),
        float((null >= observed).mean()),
        float((np.abs(null) >= abs(observed)).mean()),
    )


def per_pair_concept_means(
    sim: np.ndarray,
    has_c: np.ndarray,
    cross_mask: np.ndarray,
    trads: np.ndarray,
) -> list[tuple[str, str, float, int]]:
    """For each pair of traditions with both-have-C pairs, mean sim."""
    both_mask = has_c[:, None] & has_c[None, :] & cross_mask
    rows, cols = np.where(both_mask)
    if len(rows) == 0:
        return []
    pair_map: dict[tuple[str, str], list[float]] = {}
    for i, j in zip(rows, cols):
        a, b = trads[i], trads[j]
        if a > b:
            a, b = b, a
        pair_map.setdefault((a, b), []).append(float(sim[i, j]))
    return sorted(
        [(a, b, float(np.mean(v)), len(v)) for (a, b), v in pair_map.items()],
        key=lambda r: r[2],
        reverse=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", type=Path, required=True)
    parser.add_argument("--max", type=int, default=4000)
    parser.add_argument("--n-perm", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out-suffix", type=str, default="vec")
    args = parser.parse_args()

    print(f"Loading from {args.dir}")
    sentences, emb = load(args.dir)
    print(f"  loaded {len(sentences):,} sentences, embeddings {emb.shape}")

    sentences, emb = stratified_subsample(sentences, emb, args.max, args.seed)
    print(f"  subsampled to {len(sentences):,} sentences")

    # Build similarity matrix
    print("Building similarity matrix...")
    t0 = time.time()
    sim = emb @ emb.T
    print(f"  sim {sim.shape}, dtype {sim.dtype}, took {time.time()-t0:.1f}s")

    # Build cross-tradition mask (upper triangle, different traditions)
    trads = np.asarray([s["tradition"] for s in sentences])
    trad_equal = trads[:, None] == trads[None, :]
    upper = np.triu(np.ones_like(trad_equal, dtype=bool), k=1)
    cross_mask = (~trad_equal) & upper

    # Concept tags
    print("Computing concept tags...")
    concept_arrays: dict[str, np.ndarray] = {}
    for c in CONCEPTS:
        arr = np.asarray([c in (s.get("concepts") or []) for s in sentences])
        concept_arrays[c] = arr

    print()
    print(
        f"{'concept':<14} {'n_with':>6} {'n_both':>8} {'n_only_one':>10} "
        f"{'both_mn':>8} {'only_mn':>8} {'binding':>9} {'p1':>8}"
    )
    print("-" * 80)

    rows: list[dict] = []
    pair_data: dict[str, list] = {}
    for c in CONCEPTS:
        has_c = concept_arrays[c]
        n_with = int(has_c.sum())
        bm, om, diff, nb, nho = concept_binding_vec(sim, has_c, cross_mask)
        obs, null_mn, p1, p2 = permutation_pval_vec(sim, has_c, cross_mask, args.n_perm, args.seed)
        rows.append({
            "concept": c, "n_with": n_with,
            "both_mean": bm, "only_one_mean": om,
            "n_both": nb, "n_only_one": nho,
            "binding": diff,
            "p_one_sided": p1, "p_two_sided": p2, "n_perm": args.n_perm,
        })
        print(
            f"{c:<14} {n_with:>6} {nb:>8} {nho:>10} "
            f"{bm:>8.4f} {om:>8.4f} {diff:>+9.4f} {p1:>8.4f}"
        )
        if nb >= 5:
            pair_data[c] = per_pair_concept_means(sim, has_c, cross_mask, trads)[:15]

    # Save
    out_csv = args.dir / f"sentence_concept_binding_{args.out_suffix}.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if rows:
            w.writerow(rows[0].keys())
            for r in rows:
                w.writerow(r.values())
    print(f"\nWrote {out_csv}")

    out_json = args.dir / f"tradition_pair_sentence_sims_{args.out_suffix}.json"
    serializable = {c: [[a, b, m, n] for (a, b, m, n) in pairs] for c, pairs in pair_data.items()}
    with out_json.open("w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)
    print(f"Wrote {out_json}")

    print("\nTop tradition pairs for each significantly-bound concept:")
    for r in sorted(rows, key=lambda r: -(r["binding"] if r["binding"] == r["binding"] else 0)):
        c = r["concept"]
        if c not in pair_data or r["binding"] != r["binding"]:
            continue
        print(f"\n  {c} (binding={r['binding']:+.4f}, p={r['p_one_sided']:.4f}, n_both={r['n_both']}):")
        for (a, b, m, n) in pair_data[c][:8]:
            print(f"    {a:<22} x {b:<22} mean={m:.4f}  n={n}")


if __name__ == "__main__":
    main()
