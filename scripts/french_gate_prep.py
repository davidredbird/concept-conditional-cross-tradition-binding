"""
Prepare French tradition texts for the Phase 2a within-language gate + cross-
tradition CCB. French analog of chinese_gate_prep.py: space-delimited chunking
(~600 chars) + a manual French concept dictionary (Option A).

The French concept dictionary is glossary-level and carries the same hidden-DoF
caveat as every Option-A dictionary, PLUS a known Christian/European vocabulary
lean (two of the three texts and the mystical register tilt that way). It only
needs to discriminate concept-bearing chunks for the gate; all CCB results that
use it are EXPLORATORY. Terms are pooled across the three traditions so each
concept is taggable in Daoist, Vedantic, and Christian text.

Usage:
  python scripts/french_gate_prep.py --book taote_french --model intfloat/multilingual-e5-large
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

# French Option-A concept dictionary (regex, case-insensitive). Pooled across
# Daoist / Vedantic / Christian vocabulary. Hidden-DoF + Christian-lean caveat applies.
FRENCH_PATTERNS: dict[str, list[str]] = {
    "ULTIMATE": [r"\bTao\b", r"\bla voie\b", r"\bDieu\b", r"\bBrahma", r"\babsolu",
                 r"\bsuprême", r"\bSeigneur\b", r"\bbien[- ]?aimé", r"\bépoux\b", r"\bdivin", r"\btrès[- ]?haut"],
    "SUBSTRATE": [r"\bvide\b", r"\bnéant", r"\bnon[- ]?être", r"\bnon[- ]?agir", r"\bsans nom",
                  r"\borigine\b", r"\babîme", r"\ble fond\b", r"\bsans forme"],
    "AWARENESS": [r"\bconscience", r"\besprit\b", r"\bintelligence", r"\bentendement",
                  r"\bcontemplation", r"\bconnaissance", r"\bperception", r"\bintellect", r"\blumière"],
    "WORLD": [r"\bmonde\b", r"\bunivers", r"\btoutes choses", r"\bcréation", r"\bcréatures?",
              r"\bciel et", r"\bêtres\b", r"\bphénomène"],
    "SELF": [r"\bsoi[- ]?même", r"\ble moi\b", r"\bego\b", r"\bla personne\b", r"\ble corps\b", r"\bmon âme\b"],
    "RECOGNITION": [r"\bunion\b", r"\blibération", r"\bdélivrance", r"\billumination", r"\bréalisation",
                    r"\bsalut\b", r"\bextase", r"\bravissement", r"\bdéification", r"\bbéatitude"],
    "NONSEP": [r"\bunité\b", r"\bnon[- ]?dualité", r"\bindistinct", r"\bfusion\b", r"\bidentité",
               r"\bne faire qu['’]un", r"\bun seul\b"],
}


def chunk_french(text: str, target_chars: int = 600) -> list[str]:
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


def tag_french(text: str) -> list[str]:
    tags = []
    for concept, pats in FRENCH_PATTERNS.items():
        if any(re.search(p, text, re.IGNORECASE) for p in pats):
            tags.append(concept)
    return tags


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", required=True)
    ap.add_argument("--model", default="intfloat/multilingual-e5-large")
    ap.add_argument("--target-chars", type=int, default=600)
    args = ap.parse_args()

    clean = (REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.txt").read_text(encoding="utf-8")
    meta = json.loads((REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.meta.json").read_text(encoding="utf-8"))

    chunk_texts = chunk_french(clean, args.target_chars)
    chunks = [{
        "id": f"{args.book}::{i:04d}", "book_id": args.book,
        "tradition": meta["tradition"], "language": meta["language"],
        "text": ct, "option_a_concepts": tag_french(ct),
    } for i, ct in enumerate(chunk_texts)]
    print(f"Chunked {args.book} into {len(chunks)} chunks (~{args.target_chars} chars)")
    tc = Counter(t for c in chunks for t in c["option_a_concepts"])
    print("Tag counts: " + ", ".join(f"{k}={v}" for k, v in tc.most_common()))

    chunks_path = REPO_ROOT / "corpus" / f"chunks_french_{args.book}.jsonl"
    with chunks_path.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    from multilingual_embedder import MultilingualEmbedder
    emb = MultilingualEmbedder(args.model)
    vecs = emb.encode([c["text"] for c in chunks], batch_size=16)
    slug = args.model.replace("/", "__").replace("-", "_")
    emb_path = REPO_ROOT / "results" / "phase2a" / f"french_{args.book}_{slug}.npy"
    emb_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(emb_path, vecs)
    print(f"Embedded with {args.model}: {vecs.shape}")
    print(f"Wrote {chunks_path} and {emb_path.name}")


if __name__ == "__main__":
    main()
