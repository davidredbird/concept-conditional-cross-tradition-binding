"""
Prepare Chinese text for the within-language resolution gate (Phase 2a).

Chinese has no inter-word spaces, so the space-based chunk_books.py pipeline does
not apply. This script: (1) loads cleaned Chinese text, (2) chunks by ~250-Han-char
windows respecting line boundaries, (3) tags each chunk with a manual Hanzi concept
dictionary (Option A for Chinese), (4) embeds with the chosen multilingual model,
(5) writes a chunks file + embeddings aligned for within_language_concept_binding.py.

Hanzi concept dictionary (Buddhist + Daoist relevant; substring match since no word
boundaries). First-pass, glossary-level — same hidden-DoF caveat as all Option A
dictionaries; for the gate it only needs to discriminate concept-bearing chunks.

Usage:
  python scripts/chinese_gate_prep.py --book faju_jing_chinese --model intfloat/multilingual-e5-large
  python scripts/chinese_gate_prep.py --book faju_jing_chinese --model sentence-transformers/LaBSE
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

# Hanzi concept dictionary — distinctive compounds preferred over ambiguous single chars
HANZI_PATTERNS: dict[str, list[str]] = {
    "ULTIMATE": ["道", "真如", "第一義", "法身", "佛性", "如來"],
    "SUBSTRATE": ["空", "緣起", "無常", "寂滅", "無為"],
    "AWARENESS": ["識", "覺", "念", "智慧", "明", "心識", "意"],
    "WORLD": ["世間", "世界", "萬物", "諸法", "輪迴", "三界"],
    "SELF": ["無我", "我", "身"],
    "RECOGNITION": ["涅槃", "解脱", "解脫", "菩提", "覺悟", "寂滅", "漏盡", "證"],
    "NONSEP": ["不二", "一如", "平等"],
}


def chunk_chinese(text: str, target_han: int = 250) -> list[str]:
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    chunks, cur, cur_han = [], [], 0
    for ln in lines:
        han = sum(1 for c in ln if "一" <= c <= "鿿")
        cur.append(ln)
        cur_han += han
        if cur_han >= target_han:
            chunks.append("".join(cur))
            cur, cur_han = [], 0
    if cur:
        chunks.append("".join(cur))
    return chunks


def tag_hanzi(text: str) -> list[str]:
    tags = []
    for concept, terms in HANZI_PATTERNS.items():
        if any(t in text for t in terms):
            tags.append(concept)
    return tags


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", default="faju_jing_chinese")
    ap.add_argument("--model", default="intfloat/multilingual-e5-large")
    ap.add_argument("--target-han", type=int, default=250)
    args = ap.parse_args()

    clean = (REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.txt").read_text(encoding="utf-8")
    meta = json.loads((REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.meta.json").read_text(encoding="utf-8"))

    chunk_texts = chunk_chinese(clean, args.target_han)
    chunks = []
    for i, ct in enumerate(chunk_texts):
        chunks.append({
            "id": f"{args.book}::{i:04d}", "book_id": args.book,
            "tradition": meta["tradition"], "language": meta["language"],
            "text": ct, "option_a_concepts": tag_hanzi(ct),
        })
    print(f"Chunked {args.book} into {len(chunks)} chunks (~{args.target_han} Han each)")
    # tag rates
    from collections import Counter
    tc = Counter(t for c in chunks for t in c["option_a_concepts"])
    print("Tag counts: " + ", ".join(f"{k}={v}" for k, v in tc.most_common()))

    chunks_path = REPO_ROOT / "corpus" / f"chunks_chinese_{args.book}.jsonl"
    with chunks_path.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    from multilingual_embedder import MultilingualEmbedder
    emb = MultilingualEmbedder(args.model)
    vecs = emb.encode([c["text"] for c in chunks], batch_size=16)
    slug = args.model.replace("/", "__").replace("-", "_")
    emb_path = REPO_ROOT / "results" / "phase2a" / f"chinese_{args.book}_{slug}.npy"
    emb_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(emb_path, vecs)
    print(f"Embedded with {args.model}: {vecs.shape}")
    print(f"Wrote {chunks_path}")
    print(f"Wrote {emb_path}")
    print(f"\nRun gate: python scripts/within_language_concept_binding.py --chunks {chunks_path} --embeddings {emb_path} --language {meta['language']} --tag-mode option_a --label 'within-Chinese-Buddhist ({slug})'")


if __name__ == "__main__":
    main()
