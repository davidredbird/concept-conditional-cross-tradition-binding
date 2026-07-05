"""
Prepare Hindi tradition texts for the Phase 2a within-language gate + cross-
tradition CCB. Pair: Kabir (Nirguṇa Sant, nondual) × Tulsidas Ramcharitmanas
(Saguṇa Vaishnava Bhakti, devotional) -- both ORIGINAL Hindi/Awadhi.

Hindi has spaces, so char-based ~600 chunks (like Arabic/French). The Devanagari
Option-A dictionary includes medieval spelling variants (निरगुन/निर्गुण,
दरसन/दर्शन, ग्यान/ज्ञान) since the born-digital Sant/Bhakti text preserves them.
Same hidden-DoF + broad-tagging caveat as the other Option-A dicts.

Usage:
  python scripts/hindi_gate_prep.py --book kabir_hindi --model sentence-transformers/LaBSE
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

HINDI_PATTERNS: dict[str, list[str]] = {
    "ULTIMATE": ["राम", "हरि", "ब्रह्म", "ईश्वर", "ईस्वर", "भगवान", "प्रभु", "साहिब", "साईं",
                 "गोविन्द", "गोबिंद", "परमात्मा", "परमातमा", "अलख", "निरंजन", "सिरजनहार"],
    "SUBSTRATE": ["सून्य", "शून्य", "निरगुन", "निर्गुण", "माया", "अव्यक्त", "निराकार"],
    "AWARENESS": ["मन", "ग्यान", "ज्ञान", "सुरति", "सुरत", "सुमिरन", "ध्यान", "बुद्धि",
                  "बिबेक", "विवेक", "चेत", "बोध", "जाग"],
    "WORLD": ["जगत", "संसार", "संसा", "सृष्टि", "लोक", "भव"],
    "SELF": ["आतम", "आत्मा", "जीव", "अहंकार", "अहं", "देह", "काया", "पिंड"],
    "RECOGNITION": ["मोक्ष", "मुक्ति", "मुकति", "निर्वान", "निरवान", "भक्ति", "भगति",
                    "दरसन", "दर्शन", "मिलन", "सहज"],
    "NONSEP": ["अद्वैत", "अभेद", "समता", "अनन्य", "लीन", "एकै"],
}


def chunk_hindi(text: str, target_chars: int = 600) -> list[str]:
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


def tag_hindi(text: str) -> list[str]:
    return [c for c, terms in HINDI_PATTERNS.items() if any(t in text for t in terms)]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", required=True)
    ap.add_argument("--model", default="sentence-transformers/LaBSE")
    ap.add_argument("--target-chars", type=int, default=600)
    args = ap.parse_args()

    clean = (REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.txt").read_text(encoding="utf-8")
    meta = json.loads((REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.meta.json").read_text(encoding="utf-8"))

    chunk_texts = chunk_hindi(clean, args.target_chars)
    chunks = [{
        "id": f"{args.book}::{i:04d}", "book_id": args.book,
        "tradition": meta["tradition"], "language": "hindi",
        "text": ct, "option_a_concepts": tag_hindi(ct),
    } for i, ct in enumerate(chunk_texts)]
    print(f"Chunked {args.book} into {len(chunks)} chunks (tradition={meta['tradition']})")
    print("Tag counts: " + ", ".join(f"{k}={v}" for k, v in
          Counter(t for c in chunks for t in c["option_a_concepts"]).most_common()))

    chunks_path = REPO_ROOT / "corpus" / f"chunks_hindi_{args.book}.jsonl"
    with chunks_path.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    from multilingual_embedder import MultilingualEmbedder
    emb = MultilingualEmbedder(args.model)
    vecs = emb.encode([c["text"] for c in chunks], batch_size=16)
    slug = args.model.replace("/", "__").replace("-", "_")
    emb_path = REPO_ROOT / "results" / "phase2a" / f"hindi_{args.book}_{slug}.npy"
    emb_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(emb_path, vecs)
    print(f"Embedded {vecs.shape} -> {emb_path.name}; wrote {chunks_path.name}")


if __name__ == "__main__":
    main()
