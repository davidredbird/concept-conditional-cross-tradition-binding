"""
Multilingual concept tagger via prototype embedding (Phase 1c Option B).

Per the Phase 1c pre-registration (findings/phase1c-preregistration.md §3),
this implements Option B concept tagging:

  1. Build a prototype phrase per concept by stripping regex syntax from the
     existing English CONCEPT_PATTERNS in scripts/concept_analysis.py,
     deduplicating terms, and space-concatenating them. The prototype is the
     same string across both multilingual models; the difference is the
     embedding.

  2. Embed the prototypes and all chunks with the chosen multilingual model.

  3. Calibrate per-concept threshold against the regex tag rate on English
     chunks: for each concept C, count r_C = (English chunks regex-tagged
     with C) / (all English chunks). On the full corpus, sort chunks by
     cosine similarity to prototype C, set threshold so the top r_C fraction
     of chunks are tagged with C. This matches multilingual tag rate to
     English regex tag rate per concept.

  4. Tag each chunk with all concepts whose cosine exceeds that concept's
     threshold.

  5. Output chunks_with_multilingual_tags.jsonl augmented with a
     `multilingual_concepts` field per chunk.

Usage:
  python scripts/multilingual_concept_tagger.py \\
    --model intfloat/multilingual-e5-large \\
    --chunks corpus/chunks.jsonl \\
    --out corpus/chunks_with_multilingual_tags_e5.jsonl

Per-concept calibration thresholds and tag rates are saved to
results/phase1c/tagger_calibration_<model_slug>.json.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from concept_analysis import CONCEPT_PATTERNS  # noqa: E402


def regex_to_term(pattern: str) -> str:
    """Strip regex syntax to recover the surface term.

    Handles common patterns from concept_analysis.py:
      \\b → ''
      [-\\s]? → '-'  (compact form)
      (s|ś) → 's'   (alternation; take first alternative)
      ūnyatā → as-is (unicode preserved)
      (?=\\b)(?!...) → '' (zero-width assertions stripped)
    """
    s = pattern
    # Drop word boundary anchors
    s = s.replace(r"\b", "")
    # Drop zero-width assertions (negative/positive lookahead/lookbehind)
    s = re.sub(r"\(\?[=!][^)]+\)", "", s)
    # Drop alternation groups — keep the first alternative as a representative
    def _first_alt(m: re.Match) -> str:
        body = m.group(1)
        return body.split("|")[0]
    s = re.sub(r"\(([^)]+)\)", _first_alt, s)
    # Collapse character class [-\s] to '-'
    s = re.sub(r"\[[^\]]*\]\??", "-", s)
    # Collapse remaining regex meta
    s = s.replace("\\s", " ").replace("\\.", ".")
    s = re.sub(r"\?$", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def build_prototype(concept: str, patterns: list[str]) -> str:
    """Build a single prototype phrase from a list of regex patterns."""
    terms = []
    seen = set()
    for p in patterns:
        t = regex_to_term(p)
        if t and t not in seen:
            terms.append(t)
            seen.add(t)
    return " ".join(terms)


def regex_tag(text: str, patterns: list[str]) -> bool:
    """Return True if any pattern matches in text (case-insensitive)."""
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False


def calibrate_thresholds(
    sim: np.ndarray,
    chunks: list[dict],
    english_indices: np.ndarray,
    target_rates: dict[str, float],
    concepts: list[str],
) -> dict[str, float]:
    """For each concept, find threshold so the top r_C English fraction is tagged.

    Threshold is computed on English chunks only, then applied to the whole corpus.
    """
    thresholds = {}
    for ci, concept in enumerate(concepts):
        en_sims = sim[english_indices, ci]
        r = target_rates[concept]
        if r <= 0 or r >= 1:
            # Degenerate: no tags or all tags
            thresholds[concept] = float("inf") if r <= 0 else float("-inf")
            continue
        # Threshold = top r fraction percentile
        threshold = float(np.quantile(en_sims, 1.0 - r))
        thresholds[concept] = threshold
    return thresholds


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="intfloat/multilingual-e5-large")
    parser.add_argument("--chunks", type=Path, default=REPO_ROOT / "corpus" / "chunks.jsonl")
    parser.add_argument("--out", type=Path, default=None,
                        help="Output augmented chunks file (default: derived from model)")
    parser.add_argument("--cache", type=Path, default=None,
                        help="Cached embeddings .npy (default: derived from model)")
    parser.add_argument("--calibration-out", type=Path, default=None)
    args = parser.parse_args()

    # Derive default paths
    model_slug = args.model.replace("/", "__").replace("-", "_")
    if args.out is None:
        args.out = REPO_ROOT / "corpus" / f"chunks_with_multilingual_tags_{model_slug}.jsonl"
    if args.cache is None:
        args.cache = REPO_ROOT / "results" / "phase1c" / f"chunk_embeddings_{model_slug}.npy"
    if args.calibration_out is None:
        args.calibration_out = REPO_ROOT / "results" / "phase1c" / f"tagger_calibration_{model_slug}.json"

    # Load chunks
    chunks: list[dict] = []
    with args.chunks.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    print(f"Loaded {len(chunks):,} chunks from {args.chunks}")

    # Compute English regex tag rates per concept (calibration target)
    concepts = list(CONCEPT_PATTERNS.keys())
    english_idx_list = [i for i, c in enumerate(chunks) if c.get("language", "english") == "english"]
    english_indices = np.asarray(english_idx_list)
    print(f"  {len(english_indices)} English chunks for calibration")

    print("Computing English regex tag rates...")
    target_rates: dict[str, float] = {}
    english_regex_tags: dict[str, set[int]] = {}  # for spot-check vs Option A later
    for concept in concepts:
        patterns = CONCEPT_PATTERNS[concept]
        tagged = set()
        for i in english_idx_list:
            if regex_tag(chunks[i]["text"], patterns):
                tagged.add(i)
        rate = len(tagged) / max(len(english_idx_list), 1)
        target_rates[concept] = rate
        english_regex_tags[concept] = tagged
        print(f"  {concept:14s} {len(tagged):>5}/{len(english_idx_list):>5} = {100*rate:.1f}%")

    # Build prototypes
    print()
    print("Building prototypes...")
    prototypes = {c: build_prototype(c, CONCEPT_PATTERNS[c]) for c in concepts}
    for c, p in prototypes.items():
        print(f"  {c:14s} (n_chars={len(p)}): {p[:120]!r}{'...' if len(p) > 120 else ''}")

    # Embed: chunks (cached) + prototypes
    from multilingual_embedder import MultilingualEmbedder
    embedder = MultilingualEmbedder(args.model)

    if args.cache.exists():
        chunk_emb = np.load(args.cache)
        if chunk_emb.shape[0] == len(chunks):
            print(f"\nLoaded cached chunk embeddings: {chunk_emb.shape}")
        else:
            print(f"\nCache shape mismatch ({chunk_emb.shape[0]} vs {len(chunks)}); re-embedding")
            chunk_emb = None
    else:
        chunk_emb = None

    if chunk_emb is None:
        print(f"\nEmbedding {len(chunks):,} chunks with {args.model} ...")
        t0 = time.time()
        chunk_emb = embedder.encode([c["text"] for c in chunks], batch_size=8)
        print(f"  done in {time.time()-t0:.1f}s, shape {chunk_emb.shape}")
        args.cache.parent.mkdir(parents=True, exist_ok=True)
        np.save(args.cache, chunk_emb)
        print(f"  cached to {args.cache}")

    # Embed prototypes (no caching; tiny)
    print()
    print("Embedding prototypes...")
    proto_texts = [prototypes[c] for c in concepts]
    proto_emb = embedder.encode(proto_texts)  # default prefix applied
    print(f"  shape {proto_emb.shape}")

    # Cosine matrix: chunks x concepts
    sim = chunk_emb @ proto_emb.T  # both unit-normalized
    print(f"\nSimilarity matrix: {sim.shape}")

    # Calibrate thresholds
    print()
    print("Calibrating per-concept thresholds on English chunks...")
    thresholds = calibrate_thresholds(sim, chunks, english_indices, target_rates, concepts)
    for c in concepts:
        print(f"  {c:14s} target_rate={100*target_rates[c]:5.1f}%  threshold={thresholds[c]:+.4f}")

    # Tag each chunk
    print()
    print("Tagging chunks...")
    tag_counts_by_lang_concept: dict[tuple[str, str], int] = {}
    lang_counts: dict[str, int] = {}
    for i, c in enumerate(chunks):
        tags = []
        for ci, concept in enumerate(concepts):
            if sim[i, ci] > thresholds[concept]:
                tags.append(concept)
        c["multilingual_concepts"] = tags
        lang = c.get("language", "english")
        lang_counts[lang] = lang_counts.get(lang, 0) + 1
        for t in tags:
            key = (lang, t)
            tag_counts_by_lang_concept[key] = tag_counts_by_lang_concept.get(key, 0) + 1

    # Print tag rates by language x concept
    print()
    print(f"{'language':<22} " + " ".join(f"{c:>10}" for c in concepts))
    print("-" * (22 + 11 * len(concepts)))
    for lang in sorted(lang_counts.keys(), key=lambda l: -lang_counts[l]):
        n = lang_counts[lang]
        row = [f"{lang:<22} (n={n:>5})"]
        for concept in concepts:
            n_tagged = tag_counts_by_lang_concept.get((lang, concept), 0)
            row.append(f"{100*n_tagged/max(n,1):>9.1f}%")
        print(" ".join(row))

    # Save augmented chunks
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"\nWrote {args.out}")

    # Save calibration info
    cal = {
        "model": args.model,
        "concepts": concepts,
        "target_rates_english": target_rates,
        "thresholds": thresholds,
        "prototypes": prototypes,
        "n_chunks": len(chunks),
        "n_english_chunks": int(len(english_indices)),
        "tag_counts_by_language_concept": {
            f"{lang}|{c}": v for (lang, c), v in tag_counts_by_lang_concept.items()
        },
        "language_chunk_counts": lang_counts,
    }
    args.calibration_out.parent.mkdir(parents=True, exist_ok=True)
    args.calibration_out.write_text(json.dumps(cal, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {args.calibration_out}")


if __name__ == "__main__":
    main()
