"""
Prepare Japanese tradition texts for the Phase 2a within-language gate +
cross-tradition CCB. Japanese analog of chinese_gate_prep.py (char-based chunking,
no inter-word spaces). Pair: Tannishō (Pure Land Buddhist) × Chūyō / Doctrine of
the Mean (Confucian) -- two separate lineages rendered in Japanese, a parallel to
the Chinese Buddhist×Daoist separate-lineage test.

Concept dictionary: kanji + kana, pooled Buddhist + Confucian vocabulary. Same
hidden-DoF + broad-tagging caveat as the Chinese/Arabic Option-A dicts.

Usage:
  python scripts/japanese_gate_prep.py --book tannisho_japanese --model sentence-transformers/LaBSE
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

# Japanese concept dictionary (substring match on kanji+kana); Buddhist + Confucian pooled
JP_PATTERNS: dict[str, list[str]] = {
    "ULTIMATE": ["道", "天命", "仏", "佛", "如来", "如來", "法身", "阿弥陀", "弥陀", "本願", "誠", "太極", "上帝"],
    "SUBSTRATE": ["空", "無為", "虚", "理", "性", "無常", "寂"],
    "AWARENESS": ["心", "意識", "智慧", "悟", "覚", "念", "信心", "知", "明", "思"],
    "WORLD": ["世界", "世間", "万物", "萬物", "天下", "衆生", "諸法", "三界"],
    "SELF": ["自己", "自身", "己", "我", "身"],
    "RECOGNITION": ["涅槃", "解脱", "解脱", "往生", "成仏", "成佛", "菩提", "悟り", "至誠"],
    "NONSEP": ["不二", "一如", "一体", "一體", "一味"],
}

# residual furigana/markup junk to drop
JUNK = re.compile(r"(コレクション|info:ndljp|新漢字版|styles\.css|mw-parser|の処理でエラー)")


def clean_jp(text: str) -> str:
    text = re.sub(r"（\s*）", "", text)        # empty furigana parens
    text = re.sub(r"\(\s*\)", "", text)
    text = re.sub(r"[〈〉]", "", text)
    return text


def chunk_japanese(text: str, target_chars: int = 300) -> list[str]:
    lines = [ln.strip() for ln in text.split("\n") if ln.strip() and not JUNK.search(ln)]
    chunks, cur, n = [], [], 0
    for ln in lines:
        cur.append(ln)
        n += len(ln)
        if n >= target_chars:
            chunks.append("".join(cur))
            cur, n = [], 0
    if cur:
        chunks.append("".join(cur))
    return chunks


def tag_jp(text: str) -> list[str]:
    return [c for c, terms in JP_PATTERNS.items() if any(t in text for t in terms)]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", required=True)
    ap.add_argument("--model", default="sentence-transformers/LaBSE")
    ap.add_argument("--target-chars", type=int, default=300)
    args = ap.parse_args()

    clean = clean_jp((REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.txt").read_text(encoding="utf-8"))
    meta = json.loads((REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.meta.json").read_text(encoding="utf-8"))

    chunk_texts = chunk_japanese(clean, args.target_chars)
    chunks = [{
        "id": f"{args.book}::{i:04d}", "book_id": args.book,
        "tradition": meta["tradition"], "language": "japanese",
        "text": ct, "option_a_concepts": tag_jp(ct),
    } for i, ct in enumerate(chunk_texts)]
    print(f"Chunked {args.book} into {len(chunks)} chunks (tradition={meta['tradition']})")
    print("Tag counts: " + ", ".join(f"{k}={v}" for k, v in
          Counter(t for c in chunks for t in c["option_a_concepts"]).most_common()))

    chunks_path = REPO_ROOT / "corpus" / f"chunks_japanese_{args.book}.jsonl"
    with chunks_path.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    from multilingual_embedder import MultilingualEmbedder
    emb = MultilingualEmbedder(args.model)
    vecs = emb.encode([c["text"] for c in chunks], batch_size=16)
    slug = args.model.replace("/", "__").replace("-", "_")
    emb_path = REPO_ROOT / "results" / "phase2a" / f"japanese_{args.book}_{slug}.npy"
    emb_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(emb_path, vecs)
    print(f"Embedded {vecs.shape} -> {emb_path.name}; wrote {chunks_path.name}")


if __name__ == "__main__":
    main()
