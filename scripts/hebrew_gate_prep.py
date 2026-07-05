"""
Prepare Hebrew tradition texts for the Phase 2a within-language gate + cross-
tradition CCB. Pair: Likutei Moharan (Hasidic mystical, nondual) × Guide for the
Perplexed (Maimonides, rationalist) -- mystical×rationalist, paralleling Arabic
Sufi×Falsafa.

Hebrew needs: strip niqqud/cantillation, normalize final-letter forms (ך→כ …) so
substring matching works across word positions. The Option-A dictionary uses
distinctive stems and avoids function-word collisions (אין 'nothing' vs 'there
isn't'; אל 'God' vs 'to'). Same hidden-DoF + broad-tagging caveat.

Usage:
  python scripts/hebrew_gate_prep.py --book nachman_hebrew --model sentence-transformers/LaBSE
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

NIQQUD = re.compile(r"[֑-ׇ]")
FINALS = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"}


def normalize_he(text: str) -> str:
    text = NIQQUD.sub("", text)
    return "".join(FINALS.get(c, c) for c in text)


# normalized (no niqqud, finals folded) Hebrew concept stems; substring match
HEBREW_PATTERNS: dict[str, list[str]] = {
    "ULTIMATE": ["אלהים", "הבורא", "הקדוש ברוך", "השם", "אדני", "יהוה", "אין סוף", "המקום", "רבונו"],
    "SUBSTRATE": ["העדר", "חומר", "אפס", "תהו", "הראשית"],
    "AWARENESS": ["שכל", "דעת", "בינה", "חכמה", "מחשבה", "הכרה", "השגה", "הבנה", "מוחין"],
    "WORLD": ["עולמ", "בריאה", "יקומ", "טבע", "נבראימ", "מציאות"],
    "SELF": ["נפש", "נשמה", "עצמ", "גופ", "רוח", "אנכי"],
    "RECOGNITION": ["גאולה", "דבקות", "תשובה", "שלמות", "דבק", "השגת"],
    "NONSEP": ["יחוד", "אחדות", "ביטול", "התכללות"],
}


def chunk_hebrew(text: str, target_chars: int = 600) -> list[str]:
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    chunks, cur, n = [], [], 0
    for ln in lines:
        cur.append(ln)
        n += len(ln)
        if n >= target_chars:
            chunks.append(" ".join(cur))
            cur, n = [], 0
    if cur:
        chunks.append(" ".join(cur))
    return chunks


def tag_hebrew(text: str) -> list[str]:
    norm = normalize_he(text)
    return [c for c, terms in HEBREW_PATTERNS.items() if any(normalize_he(t) in norm for t in terms)]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", required=True)
    ap.add_argument("--model", default="sentence-transformers/LaBSE")
    ap.add_argument("--target-chars", type=int, default=600)
    args = ap.parse_args()

    clean = (REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.txt").read_text(encoding="utf-8")
    meta = json.loads((REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.meta.json").read_text(encoding="utf-8"))

    chunk_texts = chunk_hebrew(clean, args.target_chars)
    chunks = [{
        "id": f"{args.book}::{i:04d}", "book_id": args.book,
        "tradition": meta["tradition"], "language": "hebrew",
        "text": ct, "option_a_concepts": tag_hebrew(ct),
    } for i, ct in enumerate(chunk_texts)]
    print(f"Chunked {args.book} into {len(chunks)} chunks (tradition={meta['tradition']})")
    print("Tag counts: " + ", ".join(f"{k}={v}" for k, v in
          Counter(t for c in chunks for t in c["option_a_concepts"]).most_common()))

    chunks_path = REPO_ROOT / "corpus" / f"chunks_hebrew_{args.book}.jsonl"
    with chunks_path.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    from multilingual_embedder import MultilingualEmbedder
    emb = MultilingualEmbedder(args.model)
    vecs = emb.encode([c["text"] for c in chunks], batch_size=16)
    slug = args.model.replace("/", "__").replace("-", "_")
    emb_path = REPO_ROOT / "results" / "phase2a" / f"hebrew_{args.book}_{slug}.npy"
    emb_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(emb_path, vecs)
    print(f"Embedded {vecs.shape} -> {emb_path.name}; wrote {chunks_path.name}")


if __name__ == "__main__":
    main()
