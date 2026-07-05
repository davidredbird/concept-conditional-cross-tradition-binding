"""
Chunk + embed an English text with LaBSE for the language-controlled
Buddhist×Daoist test. Pairs the English Dhammapada (Max Müller) against the
English Tao Te King (Legge) -- the SAME two works as the Chinese faju × Chinese
TTC run -- so a Buddhist×Daoist CCB in English vs Chinese holds tradition, text,
and embedding model fixed and varies only language. Tagging is done downstream by
the CCB script in --tag-mode regex (English CONCEPT_PATTERNS); we still store
regex tags here for inspection.

Usage:
  python scripts/english_gate_prep.py --book dhammapada_radhakrishnan
  python scripts/english_gate_prep.py --book taote_legge
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

from concept_analysis import CONCEPT_PATTERNS  # noqa: E402

# Broad English Option-A dictionary, breadth-matched to the Chinese HANZI_PATTERNS
# and French dictionaries (NOT the paper's technical-only regex). English glosses of
# the same terms the Hanzi dict tags, so the Buddhist×Daoist cross-linguistic test is
# broad-vs-broad rather than broad(Chinese)-vs-technical(English). Same hidden-DoF +
# casual-usage-noise caveat as every broad Option-A dictionary.
ENGLISH_OPTION_A: dict[str, list[str]] = {
    "ULTIMATE": [r"\btao\b", r"\bthe way\b", r"\bsuchness\b", r"\bbuddha[- ]?nature\b", r"\bdharma[- ]?body\b",
                 r"\btathagata\b", r"\bgod\b", r"\blord\b", r"\bdivine\b", r"\bbrahman\b", r"\bthe absolute\b",
                 r"\bthe supreme\b", r"\bthe eternal\b", r"\bthe holy\b", r"\bthe real\b", r"\bheaven\b"],
    "SUBSTRATE": [r"\bemptiness\b", r"\bvoid\b", r"\bdependent origination\b", r"\bimpermanen", r"\bcessation\b",
                  r"\bnon[- ]?action\b", r"\bnon[- ]?being\b", r"\bthe nameless\b", r"\bthe formless\b", r"\buncarved\b"],
    "AWARENESS": [r"\bconsciousness\b", r"\bawareness\b", r"\bmind\b", r"\bmindful", r"\bthought\b", r"\bthinking\b",
                  r"\bwisdom\b", r"\bclarity\b", r"\billumination\b", r"\bintellect", r"\bintelligence\b",
                  r"\bperception\b", r"\bunderstanding\b", r"\bspirit\b", r"\bknowing\b"],
    "WORLD": [r"\bworld\b", r"\bmyriad\b", r"\bten thousand things\b", r"\ball things\b", r"\ball dharmas\b",
              r"\bsamsara\b", r"\bthree realms\b", r"\bcreation\b", r"\bbeings\b", r"\bheaven and earth\b",
              r"\buniverse\b", r"\bphenomen"],
    "SELF": [r"\bnon[- ]?self\b", r"\bthe self\b", r"\bself\b", r"\bego\b", r"\bthe body\b", r"\bthe soul\b", r"\bthe person\b"],
    "RECOGNITION": [r"\bnirvana\b", r"\bnibbana\b", r"\bliberation\b", r"\bbodhi\b", r"\bawakening\b", r"\benlightenment\b",
                    r"\brealization\b", r"\bsalvation\b", r"\bdeliverance\b", r"\bdeathless\b", r"\bfreedom\b"],
    "NONSEP": [r"\bnon[- ]?dual", r"\boneness\b", r"\bunity\b", r"\bsameness\b", r"\bequality\b", r"\bundivided\b", r"\bbecome one\b"],
}


def chunk_english(text: str, target_chars: int = 600) -> list[str]:
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


def regex_tags(text: str, patterns: dict = ENGLISH_OPTION_A) -> list[str]:
    return [c for c, pats in patterns.items()
            if any(re.search(p, text, re.IGNORECASE) for p in pats)]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", required=True)
    ap.add_argument("--model", default="sentence-transformers/LaBSE")
    ap.add_argument("--tradition", default=None, help="override the meta tradition label")
    ap.add_argument("--target-chars", type=int, default=600)
    args = ap.parse_args()

    clean = (REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.txt").read_text(encoding="utf-8")
    meta_path = REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    tradition = args.tradition or meta.get("tradition", "unknown")

    chunk_texts = chunk_english(clean, args.target_chars)
    chunks = [{
        "id": f"{args.book}::{i:04d}", "book_id": args.book,
        "tradition": tradition, "language": "english",
        "text": ct, "option_a_concepts": regex_tags(ct),
    } for i, ct in enumerate(chunk_texts)]
    print(f"Chunked {args.book} into {len(chunks)} chunks (tradition={tradition})")
    print("Tag counts: " + ", ".join(f"{k}={v}" for k, v in
          Counter(t for c in chunks for t in c["option_a_concepts"]).most_common()))

    chunks_path = REPO_ROOT / "corpus" / f"chunks_english_{args.book}.jsonl"
    with chunks_path.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    from multilingual_embedder import MultilingualEmbedder
    emb = MultilingualEmbedder(args.model)
    vecs = emb.encode([c["text"] for c in chunks], batch_size=16)
    slug = args.model.replace("/", "__").replace("-", "_")
    emb_path = REPO_ROOT / "results" / "phase2a" / f"english_{args.book}_{slug}.npy"
    emb_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(emb_path, vecs)
    print(f"Embedded {vecs.shape} -> {emb_path.name}; wrote {chunks_path.name}")


if __name__ == "__main__":
    main()
