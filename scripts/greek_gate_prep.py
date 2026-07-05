"""
Prepare Greek tradition texts for the Phase 2a within-language gate + cross-
tradition CCB. Plotinus Enneads (Neoplatonism, nondual) is the first text; a
Christian Greek text is the planned contrast (pagan-philosophical vs Christian =
a separate-lineage pair, though sharing Greek philosophical vocabulary).

Polytonic Greek normalization: NFD-decompose, drop combining accents/breathings/
iota-subscript, lowercase, fold final sigma. The Option-A dictionary uses
distinctive stems and avoids collisions (ἕν 'one' normalizes to εν = 'in').

Usage:
  python scripts/greek_gate_prep.py --book plotinus_greek --model sentence-transformers/LaBSE
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")


def normalize_gr(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower().replace("ς", "σ")


# normalized (diacritic-free, lowercase, final-sigma folded) Greek stems; substring match
GREEK_PATTERNS: dict[str, list[str]] = {
    "ULTIMATE": ["θεο", "αγαθο", "θειο", "δημιουργ", "το εν", "το πρωτον"],
    "SUBSTRATE": ["υλη", "στερησι", "απειρ", "ανειδε", "μη ον"],
    "AWARENESS": ["νουσ", "νοησ", "διανοι", "αισθησ", "γνωσ", "θεωρι", "συνειδ", "φρονησ"],
    "WORLD": ["κοσμο", "φυσι", "αισθητ", "τα οντα", "το παν"],
    "SELF": ["ψυχ", "σωμα", "εγω", "ζωον"],
    "RECOGNITION": ["ενωσι", "εκστασι", "επιστροφ", "σωτηρι", "ομοιωσι"],
    "NONSEP": ["απλοτη", "ομου", "ταυτον"],
}


def chunk_greek(text: str, target_chars: int = 600) -> list[str]:
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


def tag_greek(text: str) -> list[str]:
    norm = normalize_gr(text)
    return [c for c, terms in GREEK_PATTERNS.items() if any(normalize_gr(t) in norm for t in terms)]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", required=True)
    ap.add_argument("--model", default="sentence-transformers/LaBSE")
    ap.add_argument("--target-chars", type=int, default=600)
    args = ap.parse_args()

    clean = (REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.txt").read_text(encoding="utf-8")
    meta = json.loads((REPO_ROOT / "corpus" / "books" / "cleaned" / f"{args.book}.meta.json").read_text(encoding="utf-8"))

    chunk_texts = chunk_greek(clean, args.target_chars)
    chunks = [{
        "id": f"{args.book}::{i:04d}", "book_id": args.book,
        "tradition": meta["tradition"], "language": "greek",
        "text": ct, "option_a_concepts": tag_greek(ct),
    } for i, ct in enumerate(chunk_texts)]
    print(f"Chunked {args.book} into {len(chunks)} chunks (tradition={meta['tradition']})")
    print("Tag counts: " + ", ".join(f"{k}={v}" for k, v in
          Counter(t for c in chunks for t in c["option_a_concepts"]).most_common()))

    chunks_path = REPO_ROOT / "corpus" / f"chunks_greek_{args.book}.jsonl"
    with chunks_path.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    from multilingual_embedder import MultilingualEmbedder
    emb = MultilingualEmbedder(args.model)
    vecs = emb.encode([c["text"] for c in chunks], batch_size=16)
    slug = args.model.replace("/", "__").replace("-", "_")
    emb_path = REPO_ROOT / "results" / "phase2a" / f"greek_{args.book}_{slug}.npy"
    emb_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(emb_path, vecs)
    print(f"Embedded {vecs.shape} -> {emb_path.name}; wrote {chunks_path.name}")


if __name__ == "__main__":
    main()
