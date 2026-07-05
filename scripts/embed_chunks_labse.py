"""
Embed the English Phase-1a/1c corpus chunks with LaBSE so the English
cross-tradition CCB can be run under the SAME model as the Chinese/French Phase
2a runs. Until now LaBSE had only ever embedded non-English text, so every
English CCB result used OpenAI text-embedding-3-large or MiniLM -- making any
cross-linguistic comparison model-confounded. This removes that confound.

Reads the existing 6009-chunk corpus, keeps the requested language, writes the
filtered chunk file (order preserved) + an aligned LaBSE .npy.

Usage:
  python scripts/embed_chunks_labse.py --language english
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", type=Path, default=REPO_ROOT / "corpus" / "chunks_with_option_a_tags.jsonl")
    ap.add_argument("--language", default="english")
    ap.add_argument("--model", default="sentence-transformers/LaBSE")
    args = ap.parse_args()

    chunks = [json.loads(l) for l in args.source.read_text(encoding="utf-8").splitlines() if l.strip()]
    sub = [c for c in chunks if c.get("language") == args.language]
    print(f"{args.language}: {len(sub)} chunks of {len(chunks)} total")

    out_chunks = REPO_ROOT / "corpus" / f"chunks_{args.language}_phase1a.jsonl"
    with out_chunks.open("w", encoding="utf-8") as f:
        for c in sub:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    from multilingual_embedder import MultilingualEmbedder
    emb = MultilingualEmbedder(args.model)
    vecs = emb.encode([c["text"] for c in sub], batch_size=16)
    slug = args.model.replace("/", "__").replace("-", "_")
    out_emb = REPO_ROOT / "results" / "phase2a" / f"{args.language}_phase1a_{slug}.npy"
    out_emb.parent.mkdir(parents=True, exist_ok=True)
    np.save(out_emb, vecs)
    print(f"Embedded {vecs.shape} -> {out_emb.name}")
    print(f"Wrote {out_chunks.name}")


if __name__ == "__main__":
    main()
