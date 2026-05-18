"""
Phase 1c embedding-quality validation.

Runs the load-bearing decision gate before Phase 1c main analyses can proceed:
do multilingual embeddings produce cleanly separable same-verse vs different-verse
similarities on parallel Sanskrit-English Bhagavad Gita verses?

Decision criterion (pre-specified before validation set was constructed):
  Pass: same-verse mean > different-verse mean AND correct-match rate >= 4/5.
        This is a basic discriminative requirement; if same-verse top-1 match
        rate falls below it the embedding is not preserving source identity
        across language adequately for Phase 1c.
  Fail: correct-match rate < 4/5 or same-verse mean <= different-verse mean.
        Phase 1c is then not feasible with the model and approach as
        configured; design must be revisited (different script encoding,
        different model, larger validation set, or both).

Validation set: corpus/phase1c_validation_pairs.jsonl
  5 famous Bhagavad Gita verses, each with Devanagari Sanskrit, IAST
  transliteration, and a canonical English translation. Hand-curated;
  small but each verse is a well-known stable text.

Models tested:
  - intfloat/multilingual-e5-large (target primary)
  - sentence-transformers/LaBSE (planned cross-model replication; currently
    in mean-pool fallback mode pending proper LaBSE pooling implementation)

Usage:
    python scripts/multilingual_embedding_validation.py
    python scripts/multilingual_embedding_validation.py --model intfloat/multilingual-e5-large
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def load_pairs(path: Path) -> list[dict]:
    pairs = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        pairs.append(json.loads(line))
    return pairs


def evaluate(model_id: str, pairs: list[dict], script: str = "devanagari") -> dict:
    from multilingual_embedder import MultilingualEmbedder

    san_key = {
        "devanagari": "sanskrit_devanagari",
        "iast": "sanskrit_iast",
    }[script]
    san = [p[san_key] for p in pairs]
    eng = [p["english"] for p in pairs]

    print(f"Loading model: {model_id}")
    emb = MultilingualEmbedder(model_id)
    print(f"  output dim: {emb.dim}, pooling: {emb.pooling}")
    print(f"  embedding {len(san)} Sanskrit ({script}) + {len(eng)} English...")
    san_v = emb.encode(san)
    eng_v = emb.encode(eng)

    sim = san_v @ eng_v.T
    diag = np.diag(sim)
    off_diag = sim[~np.eye(len(san), dtype=bool)]
    correct = sum(1 for i in range(len(san)) if int(np.argmax(sim[i])) == i)

    # Top-1 detail per verse
    per_verse = []
    for i, p in enumerate(pairs):
        argmax_j = int(np.argmax(sim[i]))
        per_verse.append({
            "verse_id": p["id"],
            "diag_similarity": float(sim[i, i]),
            "top1_match_idx": argmax_j,
            "top1_match_id": pairs[argmax_j]["id"],
            "top1_match_similarity": float(sim[i, argmax_j]),
            "correct": argmax_j == i,
        })

    result = {
        "model_id": model_id,
        "script": script,
        "n_pairs": len(pairs),
        "same_verse_mean": float(diag.mean()),
        "same_verse_min": float(diag.min()),
        "same_verse_max": float(diag.max()),
        "diff_verse_mean": float(off_diag.mean()),
        "diff_verse_min": float(off_diag.min()),
        "diff_verse_max": float(off_diag.max()),
        "separation": float(diag.mean() - off_diag.mean()),
        "correct_matches": correct,
        "correct_match_rate": correct / len(san),
        "per_verse": per_verse,
        "decision": "PASS" if (
            correct >= 4 and diag.mean() > off_diag.mean()
        ) else "FAIL",
    }
    return result


def print_report(r: dict) -> None:
    print()
    print(f"=== {r['model_id']} ({r['script']}) ===")
    print(f"  same-verse mean: {r['same_verse_mean']:.4f}  "
          f"diff-verse mean: {r['diff_verse_mean']:.4f}  "
          f"separation: {r['separation']:+.4f}")
    print(f"  correct matches: {r['correct_matches']}/{r['n_pairs']} "
          f"({100*r['correct_match_rate']:.0f}%)")
    print(f"  decision: {r['decision']}")
    print(f"  per-verse:")
    for v in r["per_verse"]:
        mark = "[ok]" if v["correct"] else "[X] "
        print(f"    {mark} {v['verse_id']:10s} diag={v['diag_similarity']:.4f}  "
              f"top1={v['top1_match_id']:10s} sim={v['top1_match_similarity']:.4f}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        action="append",
        default=None,
        help="Model ID to test (can specify multiple times). "
        "Default: both multilingual-e5-large and LaBSE.",
    )
    parser.add_argument(
        "--pairs",
        type=Path,
        default=REPO_ROOT / "corpus" / "phase1c_validation_pairs.jsonl",
    )
    parser.add_argument(
        "--scripts",
        default="devanagari",
        help="Comma-separated scripts to test (devanagari, iast)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "results" / "phase1c" / "embedding_validation.json",
    )
    args = parser.parse_args()

    models = args.model or [
        "intfloat/multilingual-e5-large",
        "sentence-transformers/LaBSE",
    ]
    scripts = [s.strip() for s in args.scripts.split(",")]

    pairs = load_pairs(args.pairs)
    print(f"Loaded {len(pairs)} validation pairs from {args.pairs}")

    all_results = []
    for model_id in models:
        for script in scripts:
            r = evaluate(model_id, pairs, script)
            print_report(r)
            all_results.append(r)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(all_results, indent=2, ensure_ascii=False), encoding="utf-8")
    print()
    print(f"Wrote {args.out}")
    print()
    print("=== summary ===")
    for r in all_results:
        print(f"  {r['decision']:4s}  {r['model_id']:45s}  {r['script']:11s}  "
              f"sep={r['separation']:+.4f}  correct={r['correct_matches']}/{r['n_pairs']}")


if __name__ == "__main__":
    main()
