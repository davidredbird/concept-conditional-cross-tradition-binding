"""
Sentence-level concept-in-context analysis.

Drops granularity from passages to sentences. For each sentence in the
corpus that mentions a structural-role concept (using the same regex
patterns as scripts/substitute.py and scripts/concept_analysis.py), embed
the sentence and ask:

    When Eckhart writes a sentence containing "God" and Shankara writes
    a sentence containing "Brahman", are those sentences more similar
    to each other than random cross-tradition sentence pairs?

At sentence granularity the concept-term and its immediate context
dominate the embedding far more than at passage granularity, so this is
much closer to "do these concepts play the same role" than the
passage-level test was.

Embedding source: --backend openai (default, uses .openai_key file or
$OPENAI_API_KEY) or --backend fastembed (ONNX, no torch).

Output: results/sentence_concept_analysis/<backend>/<model>/
  - sentence_concept_binding.csv  per-concept binding statistics
  - tradition_pair_sentence_sims.json  per-tradition-pair, per-concept
  - sentences.jsonl  the tagged sentence dataset (for reproducibility)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CORPUS = REPO_ROOT / "corpus" / "passages.jsonl"
RESULTS_ROOT = REPO_ROOT / "results" / "sentence_concept_analysis"


# Concept patterns are loaded from scripts/concept_analysis.py to keep
# the tagging consistent across the two analyses. Importing directly is
# brittle (different __main__ path); inline the patterns here instead.
CONCEPT_PATTERNS: dict[str, list[str]] = {
    "ULTIMATE": [
        r"\bthe holy one\b", r"\bthe one(?=\b)(?!\s+(who|that|which))",
        r"\bthe real\b", r"\bultimate reality\b", r"\bthe absolute\b",
        r"\bthe infinite\b", r"\bthe divine\b", r"\bdivine ground\b",
        r"\bdivine essence\b", r"\bground of being\b", r"\bbasic ground\b",
        r"\bgroundless ground\b", r"\bbuddha[-\s]?nature\b",
        r"\bdharma[-\s]?body\b", r"\bdharmakaya\b", r"\bein sof\b",
        r"\bha[-\s]?shem\b", r"\bthe creator\b", r"\bgod's\b", r"\bgods\b",
        r"\bgod\b", r"\ballah\b", r"\bbrahman\b", r"\btao\b", r"\bdao\b",
        r"\bsuchness\b", r"\btathata\b", r"\bdivine\b", r"\blord\b",
        r"\bcomputational substrate\b", r"\bmathematical structure\b",
        r"\bmathematical universe\b", r"\bholy spirit\b",
    ],
    "SUBSTRATE": [
        r"\bthe implicate order\b", r"\bimplicate order\b",
        r"\bthe holomovement\b", r"\bholomovement\b", r"\bthe quantum vacuum\b",
        r"\bthe holographic principle\b", r"\bholographic\b",
        r"\bdependent origination\b", r"\bdependently arisen\b",
        r"\bbasic space\b", r"\bintegrated information\b", r"\bemptiness\b",
        r"\bshunyata\b", r"\b(s|ś)ūnyatā\b", r"\bsvabhava\b", r"\bnoumenon\b",
        r"\bnoumena\b", r"\bthing[-\s]?in[-\s]?itself\b",
    ],
    "AWARENESS": [
        r"\bprimordial awareness\b", r"\bpure consciousness\b",
        r"\bpure awareness\b", r"\bbare awareness\b", r"\bnaked awareness\b",
        r"\brigpa\b", r"\bsat[-\s]?cit[-\s]?ananda\b", r"\bchit\b",
        r"\bchitta\b", r"\bcitta\b", r"\bnous\b", r"\bphi\b",
        r"\bconsciousness\b", r"\bawareness\b", r"\bsentience\b",
    ],
    "WORLD": [
        r"\bthe ten thousand things\b", r"\bthe manifold of phenomena\b",
        r"\bthe simulation\b", r"\bancestor simulation\b", r"\ba simulation\b",
        r"\bsimulations\b", r"\bsimulation\b", r"\bsamsara\b",
        r"\bphenomenal world\b", r"\bphenomenal universe\b", r"\bphenomenal\b",
        r"\bcreation\b", r"\bthe cosmos\b", r"\bcosmos\b", r"\bthe universe\b",
        r"\bspacetime\b", r"\bphysical universe\b", r"\bphysical reality\b",
        r"\bphysical objects?\b", r"\bappearances\b", r"\bappearance\b",
        r"\bthe ten thousand\b",
    ],
    "SELF": [
        r"\batman\b", r"\bjiva\b", r"\bthe ego\b", r"\bthe empirical self\b",
        r"\bthe individual self\b", r"\bthe apparent self\b", r"\bthe agent\b",
        r"\bconscious agent\b", r"\bmarkov blanket\b",
    ],
    "RECOGNITION": [
        r"\bmoksha\b", r"\bmukti\b", r"\bnirvana\b", r"\bnibbana\b",
        r"\benlightenment\b", r"\bawakening\b", r"\bsatori\b", r"\bbodhi\b",
        r"\btheosis\b", r"\bdeification\b", r"\bfana\b", r"\bbaqa\b",
        r"\bgnosis\b", r"\bjnana\b", r"\bself[-\s]realization\b",
        r"\bliberation\b", r"\bsalvation\b", r"\bbeatific vision\b",
    ],
    "NONSEP": [
        r"\bnon[-\s]?duality\b", r"\bnon[-\s]?dual\b", r"\badvaita\b",
        r"\bwahdat al[-\s]?wujud\b", r"\bunity of being\b",
    ],
}


def compile_concept_patterns() -> dict[str, re.Pattern]:
    return {
        c: re.compile("|".join(f"(?:{p})" for p in pats), flags=re.IGNORECASE)
        for c, pats in CONCEPT_PATTERNS.items()
    }


# Sentence splitting. Naive but fine for our short passages.
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\[])")


def split_sentences(text: str) -> list[str]:
    """Split a passage into rough sentences. Trim and drop empties."""
    parts = SENT_SPLIT.split(text)
    return [p.strip() for p in parts if p.strip()]


@dataclass
class TaggedSentence:
    passage_id: str
    tradition: str
    category: str
    sentence_index: int
    text: str
    concepts: frozenset[str]


def tag_sentences(passages: list[dict]) -> list[TaggedSentence]:
    compiled = compile_concept_patterns()
    out: list[TaggedSentence] = []
    for p in passages:
        for i, s in enumerate(split_sentences(p["passage"])):
            concepts = frozenset(
                c for c, pat in compiled.items() if pat.search(s)
            )
            out.append(
                TaggedSentence(
                    passage_id=p["id"],
                    tradition=p["tradition"],
                    category=p["category"],
                    sentence_index=i,
                    text=s,
                    concepts=concepts,
                )
            )
    return out


# ===== embedding backends =====

def embed_openai(texts: list[str], model: str) -> np.ndarray:
    from openai import OpenAI

    client = OpenAI()
    embs: list[list[float]] = []
    for i in range(0, len(texts), 100):
        chunk = texts[i : i + 100]
        resp = client.embeddings.create(model=model, input=chunk)
        embs.extend(d.embedding for d in resp.data)
    arr = np.asarray(embs)
    arr = arr / np.linalg.norm(arr, axis=1, keepdims=True)
    return arr


def embed_onnx(texts: list[str], model: str) -> np.ndarray:
    """
    Local BERT-class embedding via ONNX Runtime (no torch — sidesteps WDAC).
    Default model: sentence-transformers/all-MiniLM-L6-v2 (384-dim, fast).
    For higher quality, try sentence-transformers/all-mpnet-base-v2 (768-dim).
    """
    from onnx_embedder import ONNXEmbedder

    embedder = ONNXEmbedder(model)
    return embedder.encode(texts)


# ===== analysis =====

def concept_binding_at_sentence_level(
    sim: np.ndarray,
    sents: list[TaggedSentence],
    concept: str,
) -> dict[str, float]:
    """
    Same metric as concept_analysis.py but on sentences, not passages.

    For cross-tradition sentence pairs only:
      both_have:    mean sim, both sentences mention C
      only_one_has: mean sim, one sentence mentions C
      neither_has:  mean sim, neither mentions C

    Binding = both_have - only_one_has.
    """
    n = len(sents)
    both, only_one, neither = [], [], []
    for i, j in combinations(range(n), 2):
        if sents[i].tradition == sents[j].tradition:
            continue
        hi = concept in sents[i].concepts
        hj = concept in sents[j].concepts
        s = float(sim[i, j])
        if hi and hj:
            both.append(s)
        elif hi ^ hj:
            only_one.append(s)
        else:
            neither.append(s)

    def m(xs):
        return float(np.mean(xs)) if xs else float("nan")

    return {
        "concept": concept,
        "n_sentences_with": int(sum(1 for s in sents if concept in s.concepts)),
        "n_both": len(both), "both_mean": m(both),
        "n_only_one": len(only_one), "only_one_mean": m(only_one),
        "n_neither": len(neither), "neither_mean": m(neither),
        "binding": m(both) - m(only_one),
    }


def permutation_test(
    sim: np.ndarray,
    sents: list[TaggedSentence],
    concept: str,
    n_perm: int = 2000,
    seed: int = 0,
) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    n = len(sents)
    has_c = np.asarray([concept in s.concepts for s in sents])
    n_with = int(has_c.sum())
    if n_with == 0 or n_with == n:
        return {"p_one_sided": float("nan"), "n_perm": 0}

    trads = [s.tradition for s in sents]

    def cb(mask: np.ndarray) -> float:
        both, only = [], []
        for i, j in combinations(range(n), 2):
            if trads[i] == trads[j]:
                continue
            hi, hj = mask[i], mask[j]
            if hi and hj:
                both.append(float(sim[i, j]))
            elif hi ^ hj:
                only.append(float(sim[i, j]))
        if not both or not only:
            return float("nan")
        return float(np.mean(both) - np.mean(only))

    observed = cb(has_c)
    diffs = []
    indices = np.arange(n)
    for _ in range(n_perm):
        perm = rng.permutation(indices)
        m = np.zeros(n, dtype=bool)
        m[perm[:n_with]] = True
        d = cb(m)
        if not np.isnan(d):
            diffs.append(d)
    null = np.asarray(diffs)
    return {
        "observed": float(observed),
        "null_mean": float(null.mean()),
        "null_std": float(null.std()),
        "p_one_sided": float((null >= observed).mean()),
        "p_two_sided": float((np.abs(null) >= abs(observed)).mean()),
        "n_perm": int(len(null)),
    }


def per_pair_concept_sim(
    sim: np.ndarray,
    sents: list[TaggedSentence],
    concept: str,
) -> dict[tuple[str, str], dict]:
    out: dict[tuple[str, str], list[float]] = {}
    n = len(sents)
    for i, j in combinations(range(n), 2):
        ti, tj = sents[i].tradition, sents[j].tradition
        if ti == tj:
            continue
        if concept not in sents[i].concepts or concept not in sents[j].concepts:
            continue
        key = tuple(sorted([ti, tj]))
        out.setdefault(key, []).append(float(sim[i, j]))
    return {
        f"{a}|{b}": {"mean": float(np.mean(v)), "n": len(v), "max": float(np.max(v))}
        for (a, b), v in out.items()
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--backend", choices=["openai", "onnx"], default="openai")
    p.add_argument(
        "--model",
        default=None,
        help="Model name. Default: 'text-embedding-3-large' for openai, "
        "'sentence-transformers/all-MiniLM-L6-v2' for onnx",
    )
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--key-file", type=Path, default=REPO_ROOT / ".openai_key")
    args = p.parse_args()

    if args.backend == "openai":
        model = args.model or "text-embedding-3-large"
        if not os.environ.get("OPENAI_API_KEY") and args.key_file.exists():
            os.environ["OPENAI_API_KEY"] = args.key_file.read_text().strip()
    else:
        model = args.model or "sentence-transformers/all-MiniLM-L6-v2"

    out_dir = args.out or (RESULTS_ROOT / args.backend / model.replace("/", "__"))
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load corpus
    passages: list[dict] = []
    with args.corpus.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                passages.append(json.loads(line))
    print(f"Loaded {len(passages)} passages from {args.corpus}")

    # Split + tag
    sents = tag_sentences(passages)
    n_tagged = sum(1 for s in sents if s.concepts)
    print(f"Split into {len(sents)} sentences; {n_tagged} tagged with at least one concept")

    # Save sentence dataset
    with (out_dir / "sentences.jsonl").open("w", encoding="utf-8") as f:
        for s in sents:
            f.write(
                json.dumps(
                    {
                        "passage_id": s.passage_id,
                        "tradition": s.tradition,
                        "category": s.category,
                        "sentence_index": s.sentence_index,
                        "text": s.text,
                        "concepts": sorted(s.concepts),
                    }
                )
                + "\n"
            )

    # Embed
    print(f"Embedding with backend={args.backend} model={model} ...")
    texts = [s.text for s in sents]
    if args.backend == "openai":
        emb = embed_openai(texts, model)
    else:
        emb = embed_onnx(texts, model)
    np.save(out_dir / "embeddings.npy", emb)
    print(f"Embeddings shape {emb.shape}; saved")

    sim = emb @ emb.T

    # Per-concept binding + permutation test
    print(
        f"\n{'concept':<14} {'n_with':>6} {'both_n':>7} {'only_n':>7} "
        f"{'both_mn':>8} {'only_mn':>8} {'binding':>9} {'p1':>8}"
    )
    rows: list[dict] = []
    for c in CONCEPT_PATTERNS:
        stats = concept_binding_at_sentence_level(sim, sents, c)
        perm = permutation_test(sim, sents, c, n_perm=2000)
        merged = {**stats, "p_one_sided": perm.get("p_one_sided", float("nan"))}
        rows.append(merged)
        print(
            f"{c:<14} {stats['n_sentences_with']:>6} "
            f"{stats['n_both']:>7} {stats['n_only_one']:>7} "
            f"{stats['both_mean']:>8.4f} {stats['only_one_mean']:>8.4f} "
            f"{stats['binding']:>+9.4f} {merged['p_one_sided']:>8.4f}"
        )

    with (out_dir / "sentence_concept_binding.csv").open(
        "w", encoding="utf-8", newline=""
    ) as f:
        w = csv.writer(f)
        if rows:
            w.writerow(list(rows[0].keys()))
            for r in rows:
                w.writerow([r.get(k, "") for k in rows[0].keys()])

    # Tradition-pair breakdowns for each meaningful concept
    pair_data: dict[str, dict] = {}
    print("\n=== Top cross-tradition sentence-pair similarities per concept ===")
    for r in sorted(rows, key=lambda r: -r["binding"] if not np.isnan(r["binding"]) else 0):
        if r["n_both"] < 5:
            continue
        c = r["concept"]
        pairs = per_pair_concept_sim(sim, sents, c)
        pair_data[c] = pairs
        top = sorted(pairs.items(), key=lambda kv: kv[1]["mean"], reverse=True)[:8]
        print(f"\n  {c} (binding={r['binding']:+.4f}, p={r['p_one_sided']:.4f}, n_both={r['n_both']}):")
        for k, v in top:
            print(f"    {k:<40} mean={v['mean']:.4f}  n={v['n']}")

    with (out_dir / "tradition_pair_sentence_sims.json").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(pair_data, f, indent=2)

    print(f"\nOutputs written to {out_dir}")


if __name__ == "__main__":
    main()
