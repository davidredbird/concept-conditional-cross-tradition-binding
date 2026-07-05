"""
Phase 1a lexical-overlap robustness controls.

A peer reviewer flagged that the CCB (cross-tradition concept-binding)
statistic could be driven by lexical overlap: passages tagged with the same
concept share dictionary terms *by construction*, and cosine similarity
between embeddings is partly a function of shared surface strings. This
script implements three pre-specified controls that quantify how much of
the passage-level CCB result (`scripts/concept_analysis.py`) is explained by
lexical overlap alone, versus context beyond the tag strings.

  --control random   Frequency-matched random-word CCB. For each of the 7
                      concepts, draw 50 pseudo-concepts (random vocabulary
                      word sets, tagged-passage count matched to within
                      +/-10% of the real concept's count) and compute CCB for
                      each on the SAME cached embeddings. If real concepts
                      sit at high percentiles of this null distribution,
                      "any similarly-prevalent word set binds" is ruled out.

  --control bow       Bag-of-words (tf-idf) CCB baseline. Computes CCB for
                      the same 7 real concepts and real tags on a pure
                      lexical (tf-idf cosine) similarity matrix instead of
                      the embedding similarity matrix. This quantifies the
                      purely-lexical share of the binding signal.

  --control mask      Tag-term masking. For each concept, deletes every
                      substring matched by that concept's own pattern
                      dictionary from the passages tagged with it, re-embeds
                      ONLY those masked passages via the OpenAI API,
                      substitutes the masked embeddings into a copy of the
                      cached embedding matrix, and recomputes CCB with the
                      ORIGINAL tags. Binding that survives masking cannot be
                      carried by the tag strings themselves.

  --control all       Run all three (default).

FIREWALL: this script touches ONLY the English Phase 1a passage corpus
(`corpus/passages_phase1.jsonl`) and its cached text-embedding-3-large
embeddings. It does not read, embed, or compare anything from the
Greek/Chinese gradient corpus (Phase 3a) and must not be extended to do so.

Reuses `scripts/concept_analysis.py` for the concept pattern dictionaries
(CONCEPT_PATTERNS) and passage tagging (tag_passages), and follows
`scripts/sentence_concept_analysis.py`'s pattern for calling the OpenAI
embeddings API (.openai_key file, batches of 100).

Outputs:
  results/robustness/lexical_controls.json  (all numbers; sections merge
                                              across separate --control runs)
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import concept_analysis as ca  # noqa: E402  (CONCEPT_PATTERNS, tag_passages, compile_concept_patterns)

DEFAULT_CORPUS = REPO_ROOT / "corpus" / "passages_phase1.jsonl"
DEFAULT_EMB = (
    REPO_ROOT
    / "results"
    / "phase1"
    / "document_level"
    / "text-embedding-3-large"
    / "embeddings.npy"
)
DEFAULT_KEY_FILE = REPO_ROOT / ".openai_key"
OUT_JSON = REPO_ROOT / "results" / "robustness" / "lexical_controls.json"

SEED = 1908
N_PERM = 2000
N_PSEUDO = 50
MAX_PSEUDO_WORDS = 40
MASK_MODEL = "text-embedding-3-large"

CONCEPTS = list(ca.CONCEPT_PATTERNS.keys())  # ULTIMATE, SUBSTRATE, AWARENESS, WORLD, SELF, RECOGNITION, NONSEP

WORD_RE = re.compile(r"[a-zA-Z]{3,}")


# ===================== corpus / cross-pair plumbing =====================


def load_corpus(path: Path) -> list[dict]:
    passages = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                passages.append(json.loads(line))
    return passages


def build_cross_pairs(passages: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    """All (i, j), i<j, index pairs where passages i and j are from
    different traditions."""
    trad = np.array([p["tradition"] for p in passages])
    n = len(passages)
    iu, ju = np.triu_indices(n, k=1)
    cross = trad[iu] != trad[ju]
    return iu[cross], ju[cross]


def ccb(sim_vals: np.ndarray, has: np.ndarray, cross_i: np.ndarray, cross_j: np.ndarray):
    """Vectorized concept-binding score on a precomputed cross-tradition
    pairwise similarity vector `sim_vals` (aligned to cross_i/cross_j)."""
    hi = has[cross_i]
    hj = has[cross_j]
    both = hi & hj
    only = hi ^ hj
    if not both.any() or not only.any():
        return float("nan"), int(both.sum()), int(only.sum())
    return float(sim_vals[both].mean() - sim_vals[only].mean()), int(both.sum()), int(only.sum())


def perm_test(
    sim_vals: np.ndarray,
    has: np.ndarray,
    cross_i: np.ndarray,
    cross_j: np.ndarray,
    n_perm: int = N_PERM,
    seed: int = SEED,
) -> dict:
    """Vectorized permutation null: shuffle the tag vector (preserving
    count), recompute CCB, one-sided p-value."""
    n = len(has)
    n_with = int(has.sum())
    observed, n_both, n_only = ccb(sim_vals, has, cross_i, cross_j)
    if n_with == 0 or n_with == n or math.isnan(observed):
        return {
            "observed": observed,
            "null_mean": float("nan"),
            "null_std": float("nan"),
            "p_one_sided": float("nan"),
            "n_perm": 0,
            "n_both": n_both,
            "n_only": n_only,
        }
    rng = np.random.default_rng(seed)
    idx = np.arange(n)
    null = np.empty(n_perm)
    for k in range(n_perm):
        perm = rng.permutation(idx)
        chosen = perm[:n_with]
        m = np.zeros(n, dtype=bool)
        m[chosen] = True
        d, _, _ = ccb(sim_vals, m, cross_i, cross_j)
        null[k] = d
    valid = null[~np.isnan(null)]
    p = float((valid >= observed).mean()) if len(valid) else float("nan")
    return {
        "observed": observed,
        "null_mean": float(valid.mean()) if len(valid) else float("nan"),
        "null_std": float(valid.std()) if len(valid) else float("nan"),
        "p_one_sided": p,
        "n_perm": int(len(valid)),
        "n_both": n_both,
        "n_only": n_only,
    }


def real_reference(passages, emb, tags, cross_i, cross_j) -> dict:
    """CCB + permutation test for the 7 real concepts on the real cached
    embeddings, using the real tag dictionaries. Serves both as the
    benchmark controls are compared against and as a sanity check that this
    script's vectorized CCB reproduces the published concept_analysis.py
    numbers before any control is computed."""
    sim = emb @ emb.T
    sim_vals = sim[cross_i, cross_j]
    out = {}
    for c in CONCEPTS:
        has = np.array([c in t for t in tags])
        out[c] = {"n_with": int(has.sum()), **perm_test(sim_vals, has, cross_i, cross_j)}
    return out


# ===================== Control 1: frequency-matched random-word CCB =====================


def extract_dictionary_words() -> set[str]:
    """Literal alphabetic words used anywhere in the 7 concept pattern
    dictionaries (all traditions), so Control 1's random pseudo-concept
    vocabulary can exclude every real dictionary term."""
    words: set[str] = set()
    for patterns in ca.CONCEPT_PATTERNS.values():
        for pat in patterns:
            # Strip regex escape sequences (\b, \s, etc.) before extracting
            # word tokens so e.g. r"\bthe one\b" doesn't yield "bthe".
            cleaned = re.sub(r"\\.", " ", pat)
            for w in WORD_RE.findall(cleaned):
                words.add(w.lower())
    return words


def tokenize(text: str) -> set[str]:
    return {w.lower() for w in WORD_RE.findall(text)}


def build_vocab(passages: list[dict], exclude_words: set[str]) -> dict[str, set[int]]:
    """word -> set of passage indices containing that word as a whole
    token (>=3 alphabetic chars, appearing in >=3 passages), excluding
    every real dictionary term of all 7 concepts."""
    occ: dict[str, set[int]] = {}
    for i, p in enumerate(passages):
        for w in tokenize(p["passage"]):
            occ.setdefault(w, set()).add(i)
    return {w: idxs for w, idxs in occ.items() if len(idxs) >= 3 and w not in exclude_words}


def draw_pseudo_concept(
    vocab_words: list[str],
    vocab: dict[str, set[int]],
    n_passages: int,
    lo: int,
    hi: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, list[str], bool]:
    """Sample words one at a time (word-boundary tagging via precomputed
    occurrence sets) until the tagged-passage count reaches [lo, hi], or the
    word-set size hits MAX_PSEUDO_WORDS, or the vocabulary is exhausted.
    Returns (has_mask, chosen_words, reached_window)."""
    order = rng.permutation(len(vocab_words))
    current: set[int] = set()
    chosen: list[str] = []
    reached = False
    for k in order:
        w = vocab_words[k]
        candidate = current | vocab[w]
        if len(candidate) > hi:
            continue  # would overshoot the +/-10% window; try another word
        current = candidate
        chosen.append(w)
        if len(current) >= lo:
            reached = True
            break
        if len(chosen) >= MAX_PSEUDO_WORDS:
            break
    has = np.zeros(n_passages, dtype=bool)
    if current:
        has[list(current)] = True
    return has, chosen, reached


def control_random(passages, emb, tags, cross_i, cross_j, real_ref) -> dict:
    sim = emb @ emb.T
    sim_vals = sim[cross_i, cross_j]
    n = len(passages)

    exclude = extract_dictionary_words()
    vocab = build_vocab(passages, exclude)
    vocab_words = sorted(vocab.keys())
    print(f"[random] vocabulary: {len(vocab_words)} words (df>=3, excluding {len(exclude)} dictionary terms)")

    rng = np.random.default_rng(SEED)
    results = {}
    for concept in CONCEPTS:
        n_c = real_ref[concept]["n_with"]
        real_binding = real_ref[concept]["observed"]
        if n_c == 0:
            results[concept] = {
                "n_c": 0,
                "real_ccb": real_binding,
                "status": "skipped_no_tagged_passages",
            }
            print(f"[random] {concept}: skipped (0 tagged passages)")
            continue

        lo = max(1, math.floor(n_c * 0.9))
        hi = max(n_c, math.ceil(n_c * 1.1))

        pseudo_ccbs = []
        pseudo_counts = []
        n_reached = 0
        for _ in range(N_PSEUDO):
            has, chosen_words, reached = draw_pseudo_concept(vocab_words, vocab, n, lo, hi, rng)
            n_reached += int(reached)
            b, _, _ = ccb(sim_vals, has, cross_i, cross_j)
            pseudo_ccbs.append(b)
            pseudo_counts.append(int(has.sum()))

        pseudo_arr = np.array([b for b in pseudo_ccbs if not math.isnan(b)])
        percentile = float(100.0 * np.mean(pseudo_arr <= real_binding)) if len(pseudo_arr) else float("nan")

        results[concept] = {
            "n_c": n_c,
            "window": [lo, hi],
            "real_ccb": real_binding,
            "real_p_one_sided": real_ref[concept]["p_one_sided"],
            "n_pseudo": len(pseudo_ccbs),
            "n_pseudo_reached_window": n_reached,
            "pseudo_ccb_mean": float(pseudo_arr.mean()) if len(pseudo_arr) else float("nan"),
            "pseudo_ccb_sd": float(pseudo_arr.std(ddof=1)) if len(pseudo_arr) > 1 else float("nan"),
            "pseudo_ccb_min": float(pseudo_arr.min()) if len(pseudo_arr) else float("nan"),
            "pseudo_ccb_max": float(pseudo_arr.max()) if len(pseudo_arr) else float("nan"),
            "real_percentile_in_pseudo_dist": percentile,
            "pseudo_tagged_counts_mean": float(np.mean(pseudo_counts)),
        }
        print(
            f"[random] {concept}: n_c={n_c} real_ccb={real_binding:+.4f} "
            f"pseudo_mean={results[concept]['pseudo_ccb_mean']:+.4f} "
            f"pseudo_sd={results[concept]['pseudo_ccb_sd']:.4f} "
            f"percentile={percentile:.1f} reached_window={n_reached}/{N_PSEUDO}"
        )
    return results


# ===================== Control 2: bag-of-words (tf-idf) CCB baseline =====================


def control_bow(passages, emb, tags, cross_i, cross_j, real_ref) -> dict:
    from sklearn.feature_extraction.text import TfidfVectorizer

    texts = [p["passage"] for p in passages]
    vectorizer = TfidfVectorizer(lowercase=True)
    X = vectorizer.fit_transform(texts)
    # TfidfVectorizer applies L2 row-normalization by default, so the dot
    # product of rows is already cosine similarity.
    sim_bow = (X @ X.T).toarray()
    sim_bow_vals = sim_bow[cross_i, cross_j]

    emb_sim = emb @ emb.T
    emb_sim_vals = emb_sim[cross_i, cross_j]

    results = {}
    emb_ccbs, bow_ccbs = [], []
    for concept in CONCEPTS:
        has = np.array([concept in t for t in tags])
        emb_perm = perm_test(emb_sim_vals, has, cross_i, cross_j)
        bow_perm = perm_test(sim_bow_vals, has, cross_i, cross_j)
        results[concept] = {
            "n_with": int(has.sum()),
            "embedding_ccb": emb_perm["observed"],
            "embedding_p": emb_perm["p_one_sided"],
            "tfidf_ccb": bow_perm["observed"],
            "tfidf_p": bow_perm["p_one_sided"],
        }
        if not math.isnan(emb_perm["observed"]) and not math.isnan(bow_perm["observed"]):
            emb_ccbs.append(emb_perm["observed"])
            bow_ccbs.append(bow_perm["observed"])
        print(
            f"[bow] {concept}: n_with={int(has.sum())} "
            f"embedding_ccb={emb_perm['observed']:+.4f} (p={emb_perm['p_one_sided']:.4f}) "
            f"tfidf_ccb={bow_perm['observed']:+.4f} (p={bow_perm['p_one_sided']:.4f})"
        )

    vocab_size = int(X.shape[1])
    corr = float(np.corrcoef(emb_ccbs, bow_ccbs)[0, 1]) if len(emb_ccbs) >= 2 else float("nan")
    return {
        "per_concept": results,
        "tfidf_vocab_size": vocab_size,
        "correlation_embedding_vs_tfidf_ccb": corr,
        "n_concepts_in_correlation": len(emb_ccbs),
    }


# ===================== Control 3: tag-term masking =====================


def embed_openai(texts: list[str], model: str = MASK_MODEL, key_file: Path = DEFAULT_KEY_FILE) -> np.ndarray:
    """Re-implements scripts/sentence_concept_analysis.py's embed_openai:
    batches of 100, L2-normalized rows."""
    if not os.environ.get("OPENAI_API_KEY") and key_file.exists():
        os.environ["OPENAI_API_KEY"] = key_file.read_text().strip()
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


def mask_text(pattern: re.Pattern, text: str) -> str:
    masked = pattern.sub(" ", text)
    return re.sub(r"\s+", " ", masked).strip()


def control_mask(passages, emb, tags, cross_i, cross_j, real_ref) -> dict:
    compiled = ca.compile_concept_patterns()
    results = {}
    n = len(passages)

    total_to_embed = sum(real_ref[c]["n_with"] for c in CONCEPTS)
    print(f"[mask] will re-embed {total_to_embed} masked passages total across {len(CONCEPTS)} concepts")

    for concept in CONCEPTS:
        n_with = real_ref[concept]["n_with"]
        if n_with == 0:
            results[concept] = {"n_with": 0, "status": "skipped_no_tagged_passages"}
            print(f"[mask] {concept}: skipped (0 tagged passages)")
            continue

        idx_list = [i for i, t in enumerate(tags) if concept in t]
        pattern = compiled[concept]
        masked_texts = [mask_text(pattern, passages[i]["passage"]) for i in idx_list]

        n_empty = sum(1 for t in masked_texts if not t)
        if n_empty:
            print(f"[mask] {concept}: {n_empty}/{len(masked_texts)} passages became empty after masking; using a single space")
            masked_texts = [t if t else " " for t in masked_texts]

        print(f"[mask] {concept}: embedding {len(masked_texts)} masked passages via {MASK_MODEL}...")
        masked_emb = embed_openai(masked_texts)

        emb_masked_full = emb.copy()
        emb_masked_full[idx_list] = masked_emb
        sim_masked = emb_masked_full @ emb_masked_full.T
        sim_masked_vals = sim_masked[cross_i, cross_j]

        has = np.array([concept in t for t in tags])  # ORIGINAL tags, unchanged
        masked_perm = perm_test(sim_masked_vals, has, cross_i, cross_j)

        results[concept] = {
            "n_with": n_with,
            "original_ccb": real_ref[concept]["observed"],
            "original_p": real_ref[concept]["p_one_sided"],
            "masked_ccb": masked_perm["observed"],
            "masked_p": masked_perm["p_one_sided"],
            "retention_fraction": (
                masked_perm["observed"] / real_ref[concept]["observed"]
                if real_ref[concept]["observed"] not in (0, float("nan")) and not math.isnan(real_ref[concept]["observed"])
                else float("nan")
            ),
        }
        print(
            f"[mask] {concept}: original_ccb={real_ref[concept]['observed']:+.4f} "
            f"(p={real_ref[concept]['p_one_sided']:.4f}) -> "
            f"masked_ccb={masked_perm['observed']:+.4f} (p={masked_perm['p_one_sided']:.4f})"
        )
    return results


# ===================== main =====================


def load_existing_json(path: Path) -> dict:
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def main() -> None:
    global SEED
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    p.add_argument("--embeddings", type=Path, default=DEFAULT_EMB)
    p.add_argument("--out", type=Path, default=OUT_JSON)
    p.add_argument("--control", choices=["random", "bow", "mask", "all"], default="all")
    p.add_argument("--seed", type=int, default=SEED)
    args = p.parse_args()

    SEED = args.seed

    passages = load_corpus(args.corpus)
    emb = np.load(args.embeddings)
    assert emb.shape[0] == len(passages), (
        f"Embedding/corpus row-count mismatch: {emb.shape[0]} embeddings vs {len(passages)} passages"
    )
    tags = ca.tag_passages(passages)
    cross_i, cross_j = build_cross_pairs(passages)

    print(f"Loaded {len(passages)} passages, embeddings shape {emb.shape}, {len(cross_i)} cross-tradition pairs")

    real_ref = real_reference(passages, emb, tags, cross_i, cross_j)
    print("\n=== Real CCB reference (this script's vectorized reproduction of concept_analysis.py) ===")
    for c in CONCEPTS:
        r = real_ref[c]
        print(f"  {c:<12} n_with={r['n_with']:>4} ccb={r['observed']:+.4f} p={r['p_one_sided']:.4f}")

    out = load_existing_json(args.out)
    out["meta"] = {
        "date": "2026-07-05",
        "corpus": str(args.corpus.relative_to(REPO_ROOT)),
        "embeddings": str(args.embeddings.relative_to(REPO_ROOT)),
        "n_passages": len(passages),
        "n_cross_tradition_pairs": int(len(cross_i)),
        "seed": SEED,
        "n_perm": N_PERM,
    }
    out["real_ccb_reference"] = real_ref
    out.setdefault("published_phase1a_ccb", {
        "AWARENESS": 0.026,
        "ULTIMATE": 0.014,
        "WORLD": 0.022,
        "RECOGNITION": 0.025,
        "SUBSTRATE": 0.054,
    })

    if args.control in ("random", "all"):
        print("\n=== Control 1: frequency-matched random-word CCB ===")
        out["control_1_random_word"] = control_random(passages, emb, tags, cross_i, cross_j, real_ref)

    if args.control in ("bow", "all"):
        print("\n=== Control 2: bag-of-words (tf-idf) CCB baseline ===")
        bow = control_bow(passages, emb, tags, cross_i, cross_j, real_ref)
        out["control_2_bow_tfidf"] = bow
        print(
            f"\n[bow] correlation across {bow['n_concepts_in_correlation']} concepts "
            f"(embedding CCB vs tf-idf CCB): r={bow['correlation_embedding_vs_tfidf_ccb']:.4f}"
        )

    if args.control in ("mask", "all"):
        print("\n=== Control 3: tag-term masking CCB ===")
        out["control_3_tag_masking"] = control_mask(passages, emb, tags, cross_i, cross_j, real_ref)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
