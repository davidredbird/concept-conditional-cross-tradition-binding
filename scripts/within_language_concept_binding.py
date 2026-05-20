"""
Within-language concept-binding diagnostic for Phase 1c.

Tests whether a multilingual embedding model resolves concept structure WITHIN
a single language at all — the prerequisite for interpreting the Phase 1c.2
cross-tradition null. If the model cannot detect that (e.g.) Sanskrit
AWARENESS-tagged passages cluster more tightly with each other than with
non-AWARENESS Sanskrit passages, then the cross-tradition null is uninformative
(it reflects the model's lack of Sanskrit concept resolution, not the absence
of cross-tradition convergence).

The diagnostic separates three confounded explanations of the Phase 1c.2 null:
  (1) translation-tradition artifact (convergence was anglophone projection)
  (2) model resolution, language-symmetric (model resolves all languages poorly)
  (3) model resolution, language-ASYMMETRIC (model resolves English finely,
      Sanskrit/Pali coarsely — English is ~40% of training data, Sanskrit/Pali
      <<1%)

By comparing within-Sanskrit concept binding to within-English-Advaita concept
binding UNDER THE SAME MODEL, we test (3) directly: if English shows binding and
Sanskrit does not, the model's concept resolution is language-asymmetric and the
Phase 1c.2 cross-tradition null cannot be attributed to translation tradition.

For each concept C, within a single-language single-tradition subset:
  binding(C) = mean_cos(pairs where both tagged C) - mean_cos(pairs where one tagged C)
(all upper-triangle pairs within the subset; NOT cross-tradition).

Tag modes:
  regex     — tag with English CONCEPT_PATTERNS (for English chunks)
  option_a  — use the option_a_concepts field (for Sanskrit/Pali chunks)

Usage:
  # within-Sanskrit (Option A tags), e5-large embeddings
  python scripts/within_language_concept_binding.py \\
    --chunks corpus/chunks_with_option_a_tags.jsonl \\
    --embeddings results/phase1c/chunk_embeddings_intfloat__multilingual_e5_large.npy \\
    --language sanskrit --tag-mode option_a --label "within-Sanskrit (e5-large)"

  # within-English-Advaita (regex tags), e5-large embeddings
  python scripts/within_language_concept_binding.py \\
    --chunks corpus/chunks_with_option_a_tags.jsonl \\
    --embeddings results/phase1c/chunk_embeddings_intfloat__multilingual_e5_large.npy \\
    --language english --tradition advaita --tag-mode regex --label "within-English-Advaita (e5-large)"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from concept_analysis import CONCEPT_PATTERNS  # noqa: E402


def regex_tags(text: str) -> list[str]:
    tags = []
    for concept, patterns in CONCEPT_PATTERNS.items():
        for p in patterns:
            if re.search(p, text, re.IGNORECASE):
                tags.append(concept)
                break
    return tags


def binding_vec(sim: np.ndarray, has_c: np.ndarray) -> tuple[float, float, float, int, int]:
    n = len(has_c)
    upper = np.triu(np.ones((n, n), dtype=bool), k=1)
    both = has_c[:, None] & has_c[None, :] & upper
    only = (has_c[:, None] ^ has_c[None, :]) & upper
    nb, no = int(both.sum()), int(only.sum())
    if nb == 0 or no == 0:
        return float("nan"), float("nan"), float("nan"), nb, no
    bm = float((sim * both).sum() / nb)
    om = float((sim * only).sum() / no)
    return bm, om, bm - om, nb, no


def perm_pval(sim: np.ndarray, has_c: np.ndarray, n_perm: int, seed: int) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    n = len(has_c)
    nw = int(has_c.sum())
    if nw == 0 or nw == n:
        return float("nan"), float("nan"), float("nan")
    _, _, obs, _, _ = binding_vec(sim, has_c)
    diffs = []
    for _ in range(n_perm):
        m = np.zeros(n, dtype=bool)
        m[rng.permutation(n)[:nw]] = True
        _, _, d, _, _ = binding_vec(sim, m)
        if not np.isnan(d):
            diffs.append(d)
    diffs = np.asarray(diffs)
    return obs, float(diffs.mean()) if len(diffs) else float("nan"), \
        float((diffs >= obs).mean()) if len(diffs) else float("nan")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--chunks", type=Path, required=True)
    ap.add_argument("--embeddings", type=Path, required=True)
    ap.add_argument("--language", required=True)
    ap.add_argument("--tradition", default=None)
    ap.add_argument("--tag-mode", choices=["regex", "option_a"], required=True)
    ap.add_argument("--label", default="")
    ap.add_argument("--n-perm", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    chunks = [json.loads(l) for l in args.chunks.read_text(encoding="utf-8").splitlines() if l.strip()]
    emb = np.load(args.embeddings)
    if emb.shape[0] != len(chunks):
        raise ValueError(f"chunk/emb mismatch {len(chunks)} vs {emb.shape[0]}")

    idxs = [i for i, c in enumerate(chunks)
            if c.get("language") == args.language
            and (args.tradition is None or c.get("tradition") == args.tradition)]
    print(f"{args.label}")
    print(f"  subset: language={args.language} tradition={args.tradition} -> {len(idxs)} chunks")
    if len(idxs) < 10:
        print("  WARNING: very small subset")

    sub = [chunks[i] for i in idxs]
    sub_emb = emb[idxs]
    sim = sub_emb @ sub_emb.T

    concepts = list(CONCEPT_PATTERNS.keys())
    # Tag
    if args.tag_mode == "regex":
        tags_per_chunk = [set(regex_tags(c["text"])) for c in sub]
    else:
        tags_per_chunk = [set(c.get("option_a_concepts") or []) for c in sub]

    print(f"  {'concept':<14} {'n_with':>6} {'n_both':>7} {'n_only':>7} {'both_mn':>9} {'only_mn':>9} {'binding':>9} {'p':>8}")
    print("  " + "-" * 78)
    results = []
    for concept in concepts:
        has_c = np.asarray([concept in t for t in tags_per_chunk])
        nw = int(has_c.sum())
        bm, om, diff, nb, no = binding_vec(sim, has_c)
        obs, nullm, p = perm_pval(sim, has_c, args.n_perm, args.seed)
        results.append({"concept": concept, "n_with": nw, "n_both": nb, "n_only": no,
                        "both_mean": bm, "only_mean": om, "binding": diff, "p_one_sided": p})
        bm_s = f"{bm:+.4f}" if not np.isnan(bm) else "  nan"
        om_s = f"{om:+.4f}" if not np.isnan(om) else "  nan"
        d_s = f"{diff:+.4f}" if not np.isnan(diff) else "  nan"
        p_s = f"{p:.4f}" if not np.isnan(p) else "  nan"
        print(f"  {concept:<14} {nw:>6} {nb:>7} {no:>7} {bm_s:>9} {om_s:>9} {d_s:>9} {p_s:>8}")

    n_bind = sum(1 for r in results if not np.isnan(r["p_one_sided"]) and r["p_one_sided"] < 0.05 and r["binding"] > 0)
    print(f"\n  Concepts with significant within-language binding (p<0.05, binding>0): {n_bind}/{len(concepts)}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({
            "label": args.label, "language": args.language, "tradition": args.tradition,
            "tag_mode": args.tag_mode, "n_chunks": len(idxs),
            "embeddings": str(args.embeddings), "per_concept": results,
            "n_significant_binding": n_bind,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  wrote {args.out}")


if __name__ == "__main__":
    main()
