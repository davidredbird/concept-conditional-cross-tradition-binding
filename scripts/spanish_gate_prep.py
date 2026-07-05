"""
Spanish gate-prep for Phase 2a: chunk + Spanish Option-A dictionary + embed.
Molinos (Quietist, nondual) × Teresa (Carmelite affective, devotional).
Hidden-DoF + Christian-lean caveat as all Option-A dicts.

Usage:
  python scripts/spanish_gate_prep.py --book molinos_spanish --model sentence-transformers/LaBSE
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

SPANISH_PATTERNS: dict[str, list[str]] = {
    "ULTIMATE": [r"\bDios\b", r"\bel Señor\b", r"\bdivin", r"\babsoluto\b", r"\bla Divinidad\b",
                 r"\bel Amado\b", r"\bel Esposo\b", r"\bCristo\b", r"\bsumo bien\b"],
    "SUBSTRATE": [r"\bnada\b", r"\bvacío\b", r"\babismo\b", r"\bno[- ]?ser\b", r"\bel fondo\b", r"\baniquila"],
    "AWARENESS": [r"\bconciencia\b", r"\balma\b", r"\bentendimiento\b", r"\bmente\b", r"\bcontemplaci",
                  r"\bconocimiento\b", r"\brazón\b", r"\bintelecto\b", r"\badvertencia\b", r"\bespíritu\b"],
    "WORLD": [r"\bmundo\b", r"\buniverso\b", r"\bcriaturas?\b", r"\bcreación\b", r"\btodas las cosas\b", r"\blo creado\b"],
    "SELF": [r"\bsí mismo\b", r"\bel yo\b", r"\bego\b", r"\bla persona\b", r"\bel cuerpo\b", r"\bpropia voluntad\b"],
    "RECOGNITION": [r"\bunión\b", r"\béxtasis\b", r"\barrobamiento\b", r"\btransformaci", r"\bsalvación\b",
                    r"\bdeificaci", r"\bperfección\b", r"\bgracia\b"],
    "NONSEP": [r"\bunidad\b", r"\buno\b", r"\bfusión\b", r"\bindistint", r"\bno hay distinción\b"],
}


def chunk_es(text: str, target_chars: int = 600) -> list[str]:
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    chunks, cur, n = [], [], 0
    for ln in lines:
        cur.append(ln); n += len(ln)
        if n >= target_chars:
            chunks.append(" ".join(cur)); cur, n = [], 0
    if cur:
        chunks.append(" ".join(cur))
    return chunks


def tag_es(text: str) -> list[str]:
    return [c for c, pats in SPANISH_PATTERNS.items() if any(re.search(p, text, re.IGNORECASE) for p in pats)]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", required=True)
    ap.add_argument("--model", default="sentence-transformers/LaBSE")
    ap.add_argument("--target-chars", type=int, default=600)
    args = ap.parse_args()

    clean = (REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.txt").read_text(encoding="utf-8")
    meta = json.loads((REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.meta.json").read_text(encoding="utf-8"))

    chunk_texts = chunk_es(clean, args.target_chars)
    chunks = [{
        "id": f"{args.book}::{i:04d}", "book_id": args.book,
        "tradition": meta["tradition"], "language": "spanish",
        "text": ct, "option_a_concepts": tag_es(ct),
    } for i, ct in enumerate(chunk_texts)]
    print(f"Chunked {args.book} into {len(chunks)} chunks (tradition={meta['tradition']})")
    print("Tag counts: " + ", ".join(f"{k}={v}" for k, v in
          Counter(t for c in chunks for t in c["option_a_concepts"]).most_common()))

    chunks_path = REPO_ROOT / "corpus" / f"chunks_spanish_{args.book}.jsonl"
    with chunks_path.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    from multilingual_embedder import MultilingualEmbedder
    emb = MultilingualEmbedder(args.model)
    vecs = emb.encode([c["text"] for c in chunks], batch_size=16)
    slug = args.model.replace("/", "__").replace("-", "_")
    emb_path = REPO_ROOT / "results" / "phase2a" / f"spanish_{args.book}_{slug}.npy"
    emb_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(emb_path, vecs)
    print(f"Embedded {vecs.shape} -> {emb_path.name}; wrote {chunks_path.name}")


if __name__ == "__main__":
    main()
