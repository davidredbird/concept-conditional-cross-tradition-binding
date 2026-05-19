"""
Phase 1c.1 cross-lingual within-source variance analysis.

Extends Phase 1b's variance decomposition by adding a language dimension.
Per the Phase 1c pre-registration §4.1, the mask layer is:

  W-S-S-T            same book_id (single book, single language by construction)
  W-S-B-T-W-L        same source_id, different book_id, SAME language
  W-S-B-T-X-L        same source_id, different book_id, DIFFERENT language (new)
  X-S-W-T            different source_id, same tradition, SAME LANGUAGE only
  X-T                different tradition, SAME LANGUAGE only

Same-language restriction on X-S-W-T and X-T removes the cross-lingual /
cross-source ambiguity (see prereg §5.1).

Hypotheses tested (per prereg):
  H1c.1.a: W-S-B-T-X-L > X-S-W-T (permutation null over shuffled source_id
           assignments within tradition + language); cross-lingual same-source
           pairs are MORE similar than same-language cross-source pairs within
           tradition.
  H1c.1.b: |mean(W-S-B-T-X-L) - mean(W-S-B-T-W-L)| / (W-S-S-T - X-T) < 0.20
           (gap between cross-lingual and within-language same-source pairs is
           small relative to total within-source variance).
  H1c.1.c: W-S-S-T > W-S-B-T-W-L >= W-S-B-T-X-L > X-S-W-T > X-T (ordering).

Inputs:
  - chunks_with_multilingual_tags_<model>.jsonl (output of
    multilingual_concept_tagger.py; we use the chunks but not the
    multilingual_concepts here)
  - chunk_embeddings_<model>.npy (cached embeddings from same)

Output:
  - results/phase1c/phase1c1_variance_<model>.json

Usage:
  python scripts/phase1c1_cross_lingual_variance.py \\
    --chunks corpus/chunks_with_multilingual_tags_intfloat__multilingual_e5_large.jsonl \\
    --embeddings results/phase1c/chunk_embeddings_intfloat__multilingual_e5_large.npy
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_chunks_and_embeddings(chunks_path: Path, emb_path: Path) -> tuple[list[dict], np.ndarray]:
    chunks = []
    with chunks_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    emb = np.load(emb_path)
    assert emb.shape[0] == len(chunks), (emb.shape, len(chunks))
    return chunks, emb


def build_masks(chunks: list[dict]) -> dict[str, np.ndarray]:
    n = len(chunks)
    sources = np.asarray([c.get("source_id") or "" for c in chunks])
    books = np.asarray([c.get("book_id") for c in chunks])
    trads = np.asarray([c["tradition"] for c in chunks])
    langs = np.asarray([c.get("language", "english") for c in chunks])

    has_src = sources != ""
    src_pair_valid = has_src[:, None] & has_src[None, :]
    src_eq = (sources[:, None] == sources[None, :]) & src_pair_valid
    book_eq = books[:, None] == books[None, :]
    trad_eq = trads[:, None] == trads[None, :]
    lang_eq = langs[:, None] == langs[None, :]
    upper = np.triu(np.ones((n, n), dtype=bool), k=1)

    return {
        "W_S_S_T":      src_eq & book_eq & upper,
        "W_S_B_T_W_L":  src_eq & (~book_eq) & lang_eq & upper,
        "W_S_B_T_X_L":  src_eq & (~book_eq) & (~lang_eq) & upper,
        # X-S-W-T and X-T are same-language only per prereg
        "X_S_W_T":      (~src_eq) & trad_eq & lang_eq & upper,
        "X_T":          (~trad_eq) & lang_eq & upper,
        # Auxiliary (reported, not used in hypothesis tests)
        "X_S_W_T_X_L":  (~src_eq) & trad_eq & (~lang_eq) & upper,
        "X_T_X_L":      (~trad_eq) & (~lang_eq) & upper,
    }


def mean_under_mask(sim: np.ndarray, mask: np.ndarray) -> tuple[float, int]:
    n = int(mask.sum())
    if n == 0:
        return float("nan"), 0
    return float((sim * mask).sum() / n), n


def permutation_h1c1a(
    chunks: list[dict],
    sim: np.ndarray,
    n_perm: int = 1000,
    seed: int = 0,
) -> dict:
    """Permutation null for H1c.1.a.

    Shuffle source_id labels within each (tradition, language) cell, recompute
    W-S-B-T-X-L vs X-S-W-T contrast. We test whether observed (W-S-B-T-X-L - X-S-W-T)
    > null distribution.
    """
    rng = np.random.default_rng(seed)
    n = len(chunks)
    sources = np.asarray([c.get("source_id") or "" for c in chunks])
    trads = np.asarray([c["tradition"] for c in chunks])
    langs = np.asarray([c.get("language", "english") for c in chunks])

    masks = build_masks(chunks)
    obs_wsbx, _ = mean_under_mask(sim, masks["W_S_B_T_X_L"])
    obs_xswt, _ = mean_under_mask(sim, masks["X_S_W_T"])
    observed = obs_wsbx - obs_xswt

    # Group chunks by (tradition, language), shuffle source_id within each group
    from collections import defaultdict
    groups: dict[tuple[str, str], list[int]] = defaultdict(list)
    for i, c in enumerate(chunks):
        groups[(c["tradition"], c.get("language", "english"))].append(i)

    null_vals = []
    for _ in range(n_perm):
        sources_perm = sources.copy()
        for grp_idx in groups.values():
            shuffled = sources[np.asarray(grp_idx)].copy()
            rng.shuffle(shuffled)
            for orig_i, val in zip(grp_idx, shuffled):
                sources_perm[orig_i] = val
        # Rebuild W_S_B_T_X_L and X_S_W_T with shuffled sources
        has_src = sources_perm != ""
        src_pair_valid = has_src[:, None] & has_src[None, :]
        src_eq = (sources_perm[:, None] == sources_perm[None, :]) & src_pair_valid
        books = np.asarray([c.get("book_id") for c in chunks])
        book_eq = books[:, None] == books[None, :]
        trad_eq = trads[:, None] == trads[None, :]
        lang_eq = langs[:, None] == langs[None, :]
        upper = np.triu(np.ones((n, n), dtype=bool), k=1)

        wsbx_mask = src_eq & (~book_eq) & (~lang_eq) & upper
        xswt_mask = (~src_eq) & trad_eq & lang_eq & upper
        wsbx_n = wsbx_mask.sum()
        xswt_n = xswt_mask.sum()
        if wsbx_n == 0 or xswt_n == 0:
            continue
        wsbx_m = (sim * wsbx_mask).sum() / wsbx_n
        xswt_m = (sim * xswt_mask).sum() / xswt_n
        null_vals.append(wsbx_m - xswt_m)

    null = np.asarray(null_vals)
    p_one = float((null >= observed).mean()) if len(null) > 0 else float("nan")
    return {
        "observed_contrast": float(observed),
        "observed_W_S_B_T_X_L": obs_wsbx,
        "observed_X_S_W_T": obs_xswt,
        "null_mean": float(null.mean()) if len(null) else float("nan"),
        "null_std": float(null.std()) if len(null) else float("nan"),
        "n_perm_used": len(null),
        "p_one_sided": p_one,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunks", type=Path, required=True)
    parser.add_argument("--embeddings", type=Path, required=True)
    parser.add_argument("--n-perm", type=int, default=500)  # 500 is plenty
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    chunks, emb = load_chunks_and_embeddings(args.chunks, args.embeddings)
    print(f"Loaded {len(chunks):,} chunks; embeddings {emb.shape}")

    # Quick summary
    from collections import Counter
    lang_count = Counter(c.get("language", "english") for c in chunks)
    print(f"  By language: {dict(lang_count)}")

    print("\nBuilding similarity matrix...")
    t0 = time.time()
    sim = emb @ emb.T
    print(f"  shape {sim.shape}, took {time.time()-t0:.1f}s")

    print("\nBuilding masks...")
    masks = build_masks(chunks)

    print()
    print(f"{'mask':<14} {'mean_cos':>10} {'n_pairs':>14}")
    print("-" * 50)
    pair_summary = {}
    for k, mask in masks.items():
        mn, n = mean_under_mask(sim, mask)
        pair_summary[k] = {"mean": mn, "n_pairs": n}
        print(f"  {k:<12} {mn:>10.4f} {n:>14,}")

    wsst = pair_summary["W_S_S_T"]["mean"]
    wsbtwl = pair_summary["W_S_B_T_W_L"]["mean"]
    wsbtxl = pair_summary["W_S_B_T_X_L"]["mean"]
    xswt = pair_summary["X_S_W_T"]["mean"]
    xt = pair_summary["X_T"]["mean"]

    print()
    print("Hypothesis tests:")
    # H1c.1.a: W-S-B-T-X-L > X-S-W-T (with permutation)
    print(f"\n  H1c.1.a — W-S-B-T-X-L ({wsbtxl:.4f}) > X-S-W-T ({xswt:.4f})?")
    perm = permutation_h1c1a(chunks, sim, args.n_perm, args.seed)
    print(f"    observed contrast: {perm['observed_contrast']:+.4f}")
    print(f"    null mean (sd):    {perm['null_mean']:+.4f} ({perm['null_std']:.4f})")
    print(f"    p one-sided:       {perm['p_one_sided']:.4f}")
    h1c1a_supported = perm["p_one_sided"] < 0.05 and perm["observed_contrast"] > 0
    print(f"    decision: {'SUPPORTED' if h1c1a_supported else 'NOT SUPPORTED'}")

    # H1c.1.b: cross-lingual gap small
    total = wsst - xt
    gap = abs(wsbtxl - wsbtwl)
    ratio = gap / max(total, 1e-9) if total > 0 else float("inf")
    print(f"\n  H1c.1.b — |W-S-B-T-X-L - W-S-B-T-W-L| / (W-S-S-T - X-T) < 0.20?")
    print(f"    gap:                  {gap:.4f}")
    print(f"    total variance:       {total:.4f}")
    print(f"    ratio:                {ratio:.4f}")
    h1c1b_supported = ratio < 0.20 and total > 0
    print(f"    decision: {'SUPPORTED' if h1c1b_supported else 'NOT SUPPORTED'}")

    # H1c.1.c: ordering
    print(f"\n  H1c.1.c — W-S-S-T > W-S-B-T-W-L >= W-S-B-T-X-L > X-S-W-T > X-T?")
    ordering = wsst > wsbtwl and wsbtwl >= wsbtxl and wsbtxl > xswt and xswt > xt
    print(f"    {wsst:.4f} > {wsbtwl:.4f} >= {wsbtxl:.4f} > {xswt:.4f} > {xt:.4f}")
    print(f"    decision: {'SUPPORTED' if ordering else 'NOT SUPPORTED'}")

    out = {
        "input_chunks": str(args.chunks),
        "input_embeddings": str(args.embeddings),
        "n_chunks": len(chunks),
        "language_counts": dict(lang_count),
        "pair_summary": pair_summary,
        "h1c1a_permutation": perm,
        "h1c1a_supported": h1c1a_supported,
        "h1c1b_gap": gap,
        "h1c1b_total_variance": total,
        "h1c1b_ratio": ratio,
        "h1c1b_supported": h1c1b_supported,
        "h1c1c_ordering": [wsst, wsbtwl, wsbtxl, xswt, xt],
        "h1c1c_supported": ordering,
        "config": {"n_perm": args.n_perm, "seed": args.seed},
    }
    if args.out is None:
        slug = args.chunks.stem.replace("chunks_with_multilingual_tags_", "")
        args.out = REPO_ROOT / "results" / "phase1c" / f"phase1c1_variance_{slug}.json"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
