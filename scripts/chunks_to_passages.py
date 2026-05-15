"""
Convert corpus/chunks.jsonl (book-derived chunks) to corpus/passages_phase1.jsonl
in the schema the Phase 0 analysis scripts expect.

Also samples chunks per book to balance the corpus — without this, large
scholastic works (Aquinas Summa, Calvin Institutes) dominate and the
cross-tradition statistics get pulled toward them.

Sampling: deterministic stratified random sample, capped at --max-per-book.
Each book contributes min(its_chunks, max-per-book) chunks, uniformly spaced
across the book (so a sample spans the whole work rather than just the start).
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IN_PATH = REPO_ROOT / "corpus" / "chunks.jsonl"
OUT_PATH = REPO_ROOT / "corpus" / "passages_phase1.jsonl"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-per-book", type=int, default=50)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--in-path", type=Path, default=IN_PATH)
    parser.add_argument("--out-path", type=Path, default=OUT_PATH)
    args = parser.parse_args()

    # Load and group by book
    by_book: dict[str, list[dict]] = {}
    with args.in_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            by_book.setdefault(r["book_id"], []).append(r)

    rng = random.Random(args.seed)

    selected: list[dict] = []
    for bid, chunks in by_book.items():
        if len(chunks) <= args.max_per_book:
            selected.extend(chunks)
            continue
        # Uniformly-spaced sample over the book
        step = len(chunks) / args.max_per_book
        idxs = sorted({int(i * step) for i in range(args.max_per_book)})
        # Backfill if rounding dropped any
        while len(idxs) < args.max_per_book:
            extra = rng.randrange(len(chunks))
            if extra not in idxs:
                idxs.append(extra)
        idxs = sorted(set(idxs))[: args.max_per_book]
        selected.extend(chunks[i] for i in idxs)

    # Sort by book then index for stable ordering
    selected.sort(key=lambda r: (r["book_id"], r["chunk_index"]))

    # Convert to passage schema
    with args.out_path.open("w", encoding="utf-8") as f:
        for r in selected:
            out = {
                "id": r["id"],
                "tradition": r["tradition"],
                "category": r["category"],
                "author": r["author"],
                "source": r["book_id"],
                "translator": r.get("translator") or "n/a",
                "era": r.get("era") or "unknown",
                "source_status": "quote",
                "passage": r["text"],
            }
            f.write(json.dumps(out, ensure_ascii=False) + "\n")

    counts: dict[str, int] = {}
    cat_counts: dict[str, int] = {}
    for r in selected:
        counts[r["book_id"]] = counts.get(r["book_id"], 0) + 1
        cat_counts[r["category"]] = cat_counts.get(r["category"], 0) + 1

    print(f"Wrote {len(selected):,} passages from {len(by_book)} books to {args.out_path}")
    print(f"Category counts: {cat_counts}")
    print(f"Per-book sampled counts:")
    for bid in sorted(counts):
        print(f"  {bid:<40} {counts[bid]:>4}")


if __name__ == "__main__":
    main()
