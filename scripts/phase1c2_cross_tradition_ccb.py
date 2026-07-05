"""
Phase 1c.2 cross-tradition CCB on Sanskrit-Pali corpus.

Runs concept-conditional cross-tradition binding (CCB) analysis on the
multilingual Phase 1c corpus, filtered to Sanskrit (Advaita) + Pali (Theravada)
chunks. Tests whether the Phase 1a five-of-seven concept-binding result
survives multilingual analysis on original-language sources.

Inputs:
  - corpus/chunks_with_multilingual_tags_<model>.jsonl (from
    multilingual_concept_tagger.py)
  - results/phase1c/chunk_embeddings_<model>.npy (cached embeddings)

For each pre-specified concept C:
  CCB(C) = mean_cos(both passages tagged C, cross-tradition Sanskrit-Pali)
         - mean_cos(only one passage tagged C, cross-tradition Sanskrit-Pali)

Permutation null: shuffle multilingual_concepts[C] assignment across the
filtered chunk set, recompute CCB, 1000 permutations. One-sided p-value for
observed CCB > null distribution.

Output:
  - results/phase1c/phase1c2_ccb_<model>.json with per-concept CCB,
    p-values, n_with_concept counts, top sanskrit-text x pali-text similarity
    pairs by concept.

Usage:
  python scripts/phase1c2_cross_tradition_ccb.py \\
    --tags corpus/chunks_with_multilingual_tags_intfloat__multilingual_e5_large.jsonl \\
    --embeddings results/phase1c/chunk_embeddings_intfloat__multilingual_e5_large.npy
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from concept_analysis import CONCEPT_PATTERNS  # noqa: E402


def regex_tags(text: str) -> list[str]:
    """English CONCEPT_PATTERNS tagging (same tagger Phase 1a/the gate use)."""
    out = []
    for concept, patterns in CONCEPT_PATTERNS.items():
        if any(re.search(p, text, re.IGNORECASE) for p in patterns):
            out.append(concept)
    return out


def load_chunks_and_embeddings(tags_path: Path, emb_path: Path) -> tuple[list[dict], np.ndarray]:
    chunks = []
    with tags_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    emb = np.load(emb_path)
    if emb.shape[0] != len(chunks):
        raise ValueError(
            f"Chunk/embedding count mismatch: {len(chunks)} chunks vs {emb.shape[0]} embeddings"
        )
    return chunks, emb


def compute_ccb_vec(sim: np.ndarray, has_c: np.ndarray, cross_mask: np.ndarray) -> tuple[float, float, float, int, int]:
    both = has_c[:, None] & has_c[None, :] & cross_mask
    only = (has_c[:, None] ^ has_c[None, :]) & cross_mask
    n_both = int(both.sum())
    n_only = int(only.sum())
    if n_both == 0 or n_only == 0:
        return float("nan"), float("nan"), float("nan"), n_both, n_only
    both_mean = float((sim * both).sum() / n_both)
    only_mean = float((sim * only).sum() / n_only)
    return both_mean, only_mean, both_mean - only_mean, n_both, n_only


def permutation_pval(
    sim: np.ndarray,
    has_c: np.ndarray,
    cross_mask: np.ndarray,
    n_perm: int = 1000,
    seed: int = 0,
) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    n = len(has_c)
    n_with = int(has_c.sum())
    if n_with == 0 or n_with == n:
        return float("nan"), float("nan"), float("nan")
    _, _, observed, n_both0, n_only0 = compute_ccb_vec(sim, has_c, cross_mask)
    if np.isnan(observed) or n_both0 == 0 or n_only0 == 0:
        # degenerate (e.g. one tradition has zero tags for this concept) -> untestable,
        # NOT significant. Guards against comparing diffs >= nan giving a spurious p=0.
        return observed, float("nan"), float("nan")
    diffs = []
    for _ in range(n_perm):
        m = np.zeros(n, dtype=bool)
        m[rng.permutation(n)[:n_with]] = True
        _, _, d, _, _ = compute_ccb_vec(sim, m, cross_mask)
        if not np.isnan(d):
            diffs.append(d)
    diffs = np.asarray(diffs)
    if len(diffs) == 0:
        return observed, float("nan"), float("nan")
    p_one = float((diffs >= observed).mean())
    return observed, float(diffs.mean()), p_one


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tags", type=Path, required=True)
    parser.add_argument("--embeddings", type=Path, required=True)
    parser.add_argument("--tag-field", default="multilingual_concepts",
                        help="Chunk field holding concept tags "
                        "(multilingual_concepts=Option B prototype, "
                        "option_a_concepts=Option A manual regex)")
    parser.add_argument("--tag-mode", choices=["field", "regex"], default="field",
                        help="field=use --tag-field; regex=tag from text with English "
                        "CONCEPT_PATTERNS (for the English LaBSE run)")
    parser.add_argument("--languages", default="sanskrit,pali",
                        help="Comma-separated language filter (default Phase 1c.2 "
                        "sanskrit,pali; e.g. classical_chinese for the Chinese run)")
    parser.add_argument("--traditions", default=None,
                        help="Optional comma-separated tradition filter (e.g. "
                        "theravada,daoism to match the Chinese Buddhist×Daoist pair)")
    parser.add_argument("--n-perm", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    chunks, emb = load_chunks_and_embeddings(args.tags, args.embeddings)
    print(f"Loaded {len(chunks):,} chunks; embeddings {emb.shape}")

    target_langs = {s.strip() for s in args.languages.split(",") if s.strip()}
    target_trads = {s.strip() for s in args.traditions.split(",")} if args.traditions else None
    idxs = [i for i, c in enumerate(chunks)
            if c.get("language") in target_langs
            and (target_trads is None or c.get("tradition") in target_trads)]
    print(f"  Filtered to {len(idxs)} chunks in {sorted(target_langs)}"
          + (f" / traditions {sorted(target_trads)}" if target_trads else ""))
    if len(idxs) < 20:
        print("WARNING: very few chunks; results may be underpowered")

    sub_chunks = [chunks[i] for i in idxs]
    sub_emb = emb[idxs]

    # Build cross-tradition mask
    trads = np.asarray([c["tradition"] for c in sub_chunks])
    n = len(sub_chunks)
    trad_eq = trads[:, None] == trads[None, :]
    upper = np.triu(np.ones_like(trad_eq, dtype=bool), k=1)
    cross_mask = (~trad_eq) & upper

    n_cross_pairs = int(cross_mask.sum())
    print(f"  Cross-tradition pair count: {n_cross_pairs:,}")
    by_trad: dict[str, int] = {}
    for t in trads:
        by_trad[t] = by_trad.get(t, 0) + 1
    print(f"  By tradition: {by_trad}")

    # Similarity matrix
    print("\nBuilding similarity matrix...")
    t0 = time.time()
    sim = sub_emb @ sub_emb.T
    print(f"  done in {time.time()-t0:.2f}s, shape {sim.shape}")

    # CCB per concept
    concepts = list(CONCEPT_PATTERNS.keys())
    if args.tag_mode == "regex":
        tags_per_chunk = [set(regex_tags(c["text"])) for c in sub_chunks]
    else:
        tags_per_chunk = [set(c.get(args.tag_field) or []) for c in sub_chunks]
    print(f"\nRunning CCB for {len(concepts)} concepts with {args.n_perm} permutations each "
          f"(tag-mode={args.tag_mode})...")
    print()
    print(f"{'concept':<14} {'n_with':>6} {'n_both':>8} {'n_only':>8} "
          f"{'both_mn':>9} {'only_mn':>9} {'CCB':>9} {'null_mn':>9} {'p_one':>8}")
    print("-" * 92)
    results = []
    for concept in concepts:
        has_c = np.asarray([concept in t for t in tags_per_chunk])
        n_with = int(has_c.sum())
        bm, om, diff, n_both, n_only = compute_ccb_vec(sim, has_c, cross_mask)
        obs, null_mn, p_one = permutation_pval(sim, has_c, cross_mask, args.n_perm, args.seed)
        row = {
            "concept": concept,
            "n_with": n_with,
            "n_both": n_both,
            "n_only": n_only,
            "both_mean": bm,
            "only_one_mean": om,
            "CCB": diff,
            "null_mean": null_mn,
            "p_one_sided": p_one,
            "n_perm": args.n_perm,
        }
        results.append(row)
        bm_s = f"{bm:+.4f}" if not np.isnan(bm) else "  nan"
        om_s = f"{om:+.4f}" if not np.isnan(om) else "  nan"
        diff_s = f"{diff:+.4f}" if not np.isnan(diff) else "  nan"
        null_s = f"{null_mn:+.4f}" if not np.isnan(null_mn) else "  nan"
        p_s = f"{p_one:.4f}" if not np.isnan(p_one) else "  nan"
        print(f"{concept:<14} {n_with:>6} {n_both:>8} {n_only:>8} "
              f"{bm_s:>9} {om_s:>9} {diff_s:>9} {null_s:>9} {p_s:>8}")

    # Decision summary
    print()
    print("=== Phase 1c.2 decision summary ===")
    phase1a_binding = {"AWARENESS", "RECOGNITION", "WORLD", "ULTIMATE", "SUBSTRATE"}
    n_bind = 0
    bindings = {}
    for r in results:
        if r["concept"] not in phase1a_binding:
            continue
        if np.isnan(r["CCB"]) or np.isnan(r["p_one_sided"]):
            bindings[r["concept"]] = "untestable (no cross-tradition both-tagged pairs)"
        elif r["p_one_sided"] < 0.05 and r["CCB"] > 0:
            n_bind += 1
            bindings[r["concept"]] = "BIND p<0.05"
        else:
            bindings[r["concept"]] = f"no (p={r['p_one_sided']:.3f})"
    print(f"  Phase 1a-binding concepts that bind here: {n_bind} / 5")
    for c in ("AWARENESS", "RECOGNITION", "WORLD", "ULTIMATE", "SUBSTRATE"):
        print(f"    {c:14s} {bindings.get(c, 'untestable')}")
    print()
    print(f"  H1c.2.a (>= 2 of 5 bind): {'SUPPORTED' if n_bind >= 2 else 'NOT SUPPORTED'}")
    if "AWARENESS" in bindings and "RECOGNITION" in bindings:
        h1c2b = "SUPPORTED" if (
            "BIND" in bindings.get("AWARENESS", "")
            and "BIND" in bindings.get("RECOGNITION", "")
        ) else "NOT SUPPORTED"
        print(f"  H1c.2.b (AWARENESS + RECOGNITION both bind): {h1c2b}")

    # Save
    if args.out is None:
        slug = args.tags.stem.replace("chunks_with_multilingual_tags_", "")
        args.out = REPO_ROOT / "results" / "phase1c" / f"phase1c2_ccb_{slug}.json"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out = {
        "input_tags": str(args.tags),
        "input_embeddings": str(args.embeddings),
        "n_total_chunks": len(chunks),
        "n_filtered_chunks": len(sub_chunks),
        "n_cross_tradition_pairs": n_cross_pairs,
        "by_tradition": by_trad,
        "n_perm": args.n_perm,
        "seed": args.seed,
        "per_concept": results,
        "phase1a_binding_concepts_that_bind_here": n_bind,
        "phase1a_binding_decisions": bindings,
    }
    args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
