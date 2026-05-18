"""
Phase 1b within-source between-translator variance analysis.

Tests whether the cross-tradition CCB signal measured in Phase 1a is robust to
translator variance, by computing mean pairwise cosine similarity under four
pair-type masks and contrasting their magnitudes.

The four pair types:
  W-S-S-T  within-source same-translator      (same book_id, upper-tri pairs)
  W-S-B-T  within-source between-translator   (same source_id, different book_id)
  X-S-W-T  cross-source within-tradition      (different source_id, same tradition)
  X-T      cross-tradition                    (different tradition)

Pre-registered prediction (see findings/phase1b-preregistration.md):
  W-S-S-T > W-S-B-T > X-S-W-T > X-T

Decision rules:
  - Translator-as-confound is bounded if (W-S-B-T - X-T) >> (W-S-B-T - W-S-S-T),
    i.e., between-translator within-source similarity is much closer to the
    same-translator ceiling than to the cross-tradition floor.
  - Translator-as-confound dominates if W-S-B-T ~= X-T or W-S-B-T < X-S-W-T.

Permutation null for each contrast: shuffle the translator labels within each
source family and recompute W-S-B-T. The observed-vs-null distribution gives
a p-value for whether the cross-translator clustering exceeds chance.

Usage:
  python scripts/phase1b_within_source_variance.py \
      --chunks corpus/chunks.jsonl \
      --backend onnx \
      --model sentence-transformers/all-MiniLM-L6-v2 \
      --out results/phase1b/within_source_variance.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def load_chunks(path: Path) -> list[dict]:
    chunks: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    return chunks


def embed_chunks(chunks: list[dict], backend: str, model: str, cache_path: Path | None = None) -> np.ndarray:
    """Embed chunk text. Caches to cache_path if provided."""
    if cache_path and cache_path.exists():
        cached = np.load(cache_path)
        if cached.shape[0] == len(chunks):
            print(f"  loaded cached embeddings from {cache_path}: {cached.shape}")
            return cached
        print(f"  cache size mismatch ({cached.shape[0]} vs {len(chunks)}), re-embedding")

    texts = [c["text"] for c in chunks]
    if backend == "onnx":
        from onnx_embedder import ONNXEmbedder
        embedder = ONNXEmbedder(model)
        print(f"  embedding {len(texts):,} chunks with ONNX {model}...")
        t0 = time.time()
        emb = embedder.encode(texts, batch_size=32)
        print(f"  done in {time.time()-t0:.1f}s, shape {emb.shape}")
    elif backend == "openai":
        raise NotImplementedError("OpenAI backend not wired in this script; use onnx for Phase 1b.")
    else:
        raise ValueError(f"Unknown backend: {backend}")

    # Unit-normalize
    norms = np.linalg.norm(emb, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    emb = emb / norms

    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        np.save(cache_path, emb)
        print(f"  cached embeddings to {cache_path}")

    return emb


def build_masks(chunks: list[dict]) -> dict[str, np.ndarray]:
    """Build the four pair-type boolean masks on the chunk universe."""
    n = len(chunks)
    sources = np.asarray([c.get("source_id") or "" for c in chunks])
    books = np.asarray([c.get("book_id") for c in chunks])
    trads = np.asarray([c.get("tradition") for c in chunks])

    upper = np.triu(np.ones((n, n), dtype=bool), k=1)

    # Equality matrices
    has_src = sources != ""
    src_pair_valid = has_src[:, None] & has_src[None, :]
    src_eq = (sources[:, None] == sources[None, :]) & src_pair_valid
    book_eq = books[:, None] == books[None, :]
    trad_eq = trads[:, None] == trads[None, :]

    masks = {
        "W_S_S_T": src_eq & book_eq & upper,
        "W_S_B_T": src_eq & (~book_eq) & upper,
        "X_S_W_T": (~src_eq) & trad_eq & upper,
        "X_T": (~trad_eq) & upper,
    }
    return masks


def mean_under_mask(sim: np.ndarray, mask: np.ndarray) -> tuple[float, int]:
    n = int(mask.sum())
    if n == 0:
        return float("nan"), 0
    return float((sim * mask).sum() / n), n


def permutation_test_translator_label(
    chunks: list[dict],
    sim: np.ndarray,
    n_perm: int = 1000,
    seed: int = 0,
) -> dict:
    """Permute translator-of-chunk labels within each source family, recompute W-S-B-T.

    Tests whether the observed W-S-B-T similarity is higher than would be expected
    if translator labels were random within each source family.
    """
    rng = np.random.default_rng(seed)
    n = len(chunks)
    sources = np.asarray([c.get("source_id") or "" for c in chunks])
    books_orig = np.asarray([c.get("book_id") for c in chunks])
    has_src = sources != ""

    # Observed
    masks = build_masks(chunks)
    obs_wsb_t, n_wsb_t = mean_under_mask(sim, masks["W_S_B_T"])

    # Permuted: for each chunk with a source_id, randomly reassign its book_id
    # from the pool of book_ids within that same source family
    null_vals = np.empty(n_perm, dtype=np.float64)
    unique_sources = sorted(set(s for s in sources if s))
    src_to_idxs = {s: np.where(sources == s)[0] for s in unique_sources}

    upper = np.triu(np.ones((n, n), dtype=bool), k=1)
    src_pair_valid = has_src[:, None] & has_src[None, :]
    src_eq = (sources[:, None] == sources[None, :]) & src_pair_valid

    for k in range(n_perm):
        books_perm = books_orig.copy()
        for s in unique_sources:
            idxs = src_to_idxs[s]
            books_perm[idxs] = rng.permutation(books_orig[idxs])
        book_eq_perm = books_perm[:, None] == books_perm[None, :]
        mask_perm = src_eq & (~book_eq_perm) & upper
        null_vals[k] = float((sim * mask_perm).sum() / max(int(mask_perm.sum()), 1))

    null = null_vals[~np.isnan(null_vals)]
    p_one = float((null >= obs_wsb_t).mean()) if len(null) > 0 else float("nan")
    return {
        "observed_W_S_B_T": obs_wsb_t,
        "n_pairs_W_S_B_T": int(n_wsb_t),
        "null_mean": float(null.mean()) if len(null) > 0 else float("nan"),
        "null_std": float(null.std()) if len(null) > 0 else float("nan"),
        "p_one_sided": p_one,
        "n_perm": n_perm,
    }


def per_source_breakdown(chunks: list[dict], sim: np.ndarray) -> dict:
    """Per-source-family W-S-S-T and W-S-B-T means, with per-translator-pair detail."""
    sources = np.asarray([c.get("source_id") or "" for c in chunks])
    books = np.asarray([c.get("book_id") for c in chunks])
    unique_sources = sorted(set(s for s in sources if s))
    upper = np.triu(np.ones((len(chunks), len(chunks)), dtype=bool), k=1)

    out: dict = {}
    for s in unique_sources:
        s_idx = np.where(sources == s)[0]
        s_books = sorted(set(books[s_idx].tolist()))
        same_t_pairs = []
        cross_t_pairs = {}
        for b in s_books:
            b_idx = np.where((sources == s) & (books == b))[0]
            # within-translator pairs
            m = np.zeros_like(sim, dtype=bool)
            m[np.ix_(b_idx, b_idx)] = True
            m &= upper
            mean_v, n_v = mean_under_mask(sim, m)
            if n_v > 0:
                same_t_pairs.append({"translator_book": b, "mean": mean_v, "n_pairs": n_v})
        for i, b1 in enumerate(s_books):
            for b2 in s_books[i + 1:]:
                b1_idx = np.where((sources == s) & (books == b1))[0]
                b2_idx = np.where((sources == s) & (books == b2))[0]
                m = np.zeros_like(sim, dtype=bool)
                m[np.ix_(b1_idx, b2_idx)] = True
                # already upper-triangle since b1 != b2 indexes don't overlap
                mean_v = float(sim[np.ix_(b1_idx, b2_idx)].mean()) if (len(b1_idx) and len(b2_idx)) else float("nan")
                n_v = len(b1_idx) * len(b2_idx)
                cross_t_pairs[f"{b1}__{b2}"] = {"mean": mean_v, "n_pairs": n_v}
        out[s] = {
            "n_books": len(s_books),
            "books": s_books,
            "same_translator_within_source": same_t_pairs,
            "between_translator_within_source": cross_t_pairs,
        }
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunks", type=Path, default=REPO_ROOT / "corpus" / "chunks.jsonl")
    parser.add_argument("--backend", choices=["onnx", "openai"], default="onnx")
    parser.add_argument("--model", type=str, default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "results" / "phase1b" / "within_source_variance.json")
    parser.add_argument("--cache", type=Path, default=REPO_ROOT / "results" / "phase1b" / "embeddings.npy")
    parser.add_argument("--n-perm", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    chunks = load_chunks(args.chunks)
    print(f"Loaded {len(chunks):,} chunks from {args.chunks}")
    n_with_source = sum(1 for c in chunks if c.get("source_id"))
    print(f"  {n_with_source} chunks have source_id (multi-translator participants)")

    emb = embed_chunks(chunks, args.backend, args.model, args.cache)

    print("Building similarity matrix...")
    t0 = time.time()
    sim = emb @ emb.T
    print(f"  {sim.shape}, took {time.time()-t0:.1f}s")

    print("Building pair-type masks...")
    masks = build_masks(chunks)

    print()
    print(f"{'pair_type':<10} {'mean_cos':>10} {'n_pairs':>14}  {'description'}")
    print("-" * 80)
    pair_summary: dict = {}
    for k, mask in masks.items():
        mn, n = mean_under_mask(sim, mask)
        pair_summary[k] = {"mean": mn, "n_pairs": n}
        desc = {
            "W_S_S_T": "within-source same-translator (upper bound)",
            "W_S_B_T": "within-source between-translator (target)",
            "X_S_W_T": "cross-source within-tradition (intermediate)",
            "X_T": "cross-tradition (Phase 1a reference)",
        }[k]
        print(f"  {k:<8} {mn:>10.4f} {n:>14,}  {desc}")

    print()
    print("Variance decomposition (smaller is more confounded):")
    wsst = pair_summary["W_S_S_T"]["mean"]
    wsbt = pair_summary["W_S_B_T"]["mean"]
    xswt = pair_summary["X_S_W_T"]["mean"]
    xt = pair_summary["X_T"]["mean"]
    print(f"  Translator effect (W-S-S-T - W-S-B-T):     {wsst - wsbt:+.4f}")
    print(f"  Source/content effect (W-S-B-T - X-S-W-T): {wsbt - xswt:+.4f}")
    print(f"  Tradition effect (X-S-W-T - X-T):          {xswt - xt:+.4f}")
    print(f"  Total variance (W-S-S-T - X-T):            {wsst - xt:+.4f}")
    print(f"  Translator share of total: {(wsst - wsbt) / max(wsst - xt, 1e-6):.1%}")

    print()
    print("Running permutation test on translator labels...")
    perm = permutation_test_translator_label(chunks, sim, args.n_perm, args.seed)
    print(f"  observed W-S-B-T = {perm['observed_W_S_B_T']:.4f}")
    print(f"  null mean        = {perm['null_mean']:.4f}  (sd = {perm['null_std']:.4f})")
    print(f"  p (one-sided)    = {perm['p_one_sided']:.4f}")

    print()
    print("Per-source breakdown:")
    per_source = per_source_breakdown(chunks, sim)
    for s, info in per_source.items():
        print(f"  {s}: {info['n_books']} translators ({', '.join(info['books'])})")
        for entry in info["same_translator_within_source"]:
            print(f"    same-translator {entry['translator_book']:35s} mean={entry['mean']:.4f}  n={entry['n_pairs']:,}")
        for key, entry in info["between_translator_within_source"].items():
            print(f"    between-translator {key:35s} mean={entry['mean']:.4f}  n={entry['n_pairs']:,}")

    # Save results
    results = {
        "pair_summary": pair_summary,
        "variance_decomposition": {
            "translator_effect": wsst - wsbt,
            "source_content_effect": wsbt - xswt,
            "tradition_effect": xswt - xt,
            "total_variance": wsst - xt,
            "translator_share_of_total": (wsst - wsbt) / max(wsst - xt, 1e-6),
        },
        "permutation_test_translator_labels": perm,
        "per_source_breakdown": per_source,
        "config": {
            "chunks_path": str(args.chunks),
            "backend": args.backend,
            "model": args.model,
            "n_chunks": len(chunks),
            "n_chunks_with_source_id": n_with_source,
            "n_perm": args.n_perm,
            "seed": args.seed,
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
