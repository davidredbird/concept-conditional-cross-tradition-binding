"""
Prepare a classical Arabic text for the Phase 2a within-language gate + cross-
tradition CCB. Arabic analog of chinese_gate_prep.py.

Arabic needs normalization before substring tagging: strip tashkeel (harakat),
tatweel, and normalize alef/ya variants. The Option-A dictionary leans on
article-prefixed distinctive forms (العقل, العالم, ...) to avoid the severe
substring collisions of bare stems (علم 'knowledge' vs عالم 'world'; كون 'cosmos'
vs يكون 'to be'). Same hidden-DoF + first-pass caveat as every Option-A dict; for
the gate it only needs to discriminate concept-bearing chunks.

Usage:
  python scripts/arabic_gate_prep.py --book fusus_arabic --model sentence-transformers/LaBSE
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

TASHKEEL = re.compile(r"[ً-ْٰـ]")  # harakat, tanwin, superscript-alef, tatweel


def normalize_ar(text: str) -> str:
    text = TASHKEEL.sub("", text)
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = text.replace("ى", "ي")
    return text


# normalized (post-normalize_ar) Arabic concept stems; substring match
ARABIC_PATTERNS: dict[str, list[str]] = {
    "ULTIMATE": ["الله", "الحق", "الحقيقه", "الذات", "الالهيه", "الربوبيه", "الاسماء", "الواجب"],
    "SUBSTRATE": ["العدم", "العماء", "الغيب", "البطون", "الامكان", "الممكن"],
    "AWARENESS": ["العقل", "القلب", "المعرفه", "الشهود", "المشاهده", "البصيره", "العلم", "الذوق"],
    "WORLD": ["العالم", "الكون", "الاكوان", "الخلق", "المخلوق", "الموجودات", "الطبيعه"],
    "SELF": ["النفس", "الروح", "الانا", "العبد"],
    "RECOGNITION": ["الفناء", "البقاء", "الكشف", "التجلي", "الوصول", "الفتح", "الولايه"],
    "NONSEP": ["التوحيد", "الوحده", "الاتحاد", "الجمع"],
}


def chunk_arabic(text: str, target_chars: int = 600) -> list[str]:
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


def tag_arabic(text: str) -> list[str]:
    norm = normalize_ar(text)
    return [c for c, terms in ARABIC_PATTERNS.items() if any(t in norm for t in terms)]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", required=True)
    ap.add_argument("--model", default="sentence-transformers/LaBSE")
    ap.add_argument("--target-chars", type=int, default=600)
    args = ap.parse_args()

    clean = (REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.txt").read_text(encoding="utf-8")
    meta = json.loads((REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.meta.json").read_text(encoding="utf-8"))

    chunk_texts = chunk_arabic(clean, args.target_chars)
    chunks = [{
        "id": f"{args.book}::{i:04d}", "book_id": args.book,
        "tradition": meta["tradition"], "language": "arabic",
        "text": ct, "option_a_concepts": tag_arabic(ct),
    } for i, ct in enumerate(chunk_texts)]
    print(f"Chunked {args.book} into {len(chunks)} chunks (tradition={meta['tradition']})")
    print("Tag counts: " + ", ".join(f"{k}={v}" for k, v in
          Counter(t for c in chunks for t in c["option_a_concepts"]).most_common()))

    chunks_path = REPO_ROOT / "corpus" / f"chunks_arabic_{args.book}.jsonl"
    with chunks_path.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    from multilingual_embedder import MultilingualEmbedder
    emb = MultilingualEmbedder(args.model)
    vecs = emb.encode([c["text"] for c in chunks], batch_size=16)
    slug = args.model.replace("/", "__").replace("-", "_")
    emb_path = REPO_ROOT / "results" / "phase2a" / f"arabic_{args.book}_{slug}.npy"
    emb_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(emb_path, vecs)
    print(f"Embedded {vecs.shape} -> {emb_path.name}; wrote {chunks_path.name}")


if __name__ == "__main__":
    main()
