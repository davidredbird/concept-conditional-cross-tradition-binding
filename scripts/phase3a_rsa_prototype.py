"""
Phase 3a — RSA (Representational Similarity Analysis) PROTOTYPE (firewall-safe: Phase 2c
originals, NOT the sealed gradient). Tests the "compare relational structure, not absolute
position" redesign.

Per (language) system: build a concept centroid (mean within-language embedding of passages
tagged each concept) and the concept×concept RDM (1 - cosine) IN THAT LANGUAGE'S OWN SPACE.
Then compare languages by correlating their RDMs (second-order isomorphism, Spearman on the
upper triangle). No cross-lingual alignment of absolute embeddings ever happens.

Key questions:
  (1) Are the within-language concept-geometries isomorphic ACROSS languages (RDMs correlate
      above a shuffled-concept null)?  -> structural convergence, alignment-free.
  (2) Is the RSA signal MODEL-ROBUST (LaBSE vs OpenAI agree), where raw cross-language CCB
      flipped between models?
  (3) Which concept occupies the most STABLE structural role across languages?

Usage: python scripts/phase3a_rsa_prototype.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

SLUG = "sentence_transformers__LaBSE"
ORIGINALS = ["chinese_taote_chinese", "chinese_zhuangzi_chinese", "chinese_platform_sutra_chinese",
             "chinese_analects_chinese", "arabic_fusus_arabic", "arabic_najat_arabic",
             "greek_plotinus_greek", "greek_clement_greek", "hindi_kabir_hindi",
             "hindi_tulsidas_hindi", "hindi_surdas_hindi", "spanish_molinos_spanish",
             "spanish_teresa_spanish", "hebrew_nachman_hebrew"]
OPENAI_CACHE = REPO / "results" / "phase3a" / "originals_openai_te3l.npy"
CONCEPTS = ["SUBSTRATE", "AWARENESS", "ULTIMATE", "WORLD", "SELF", "RECOGNITION", "NONSEP"]
MIN_N = 5  # min tagged chunks to form a stable concept centroid


def load():
    chunks, labse = [], []
    for stem in ORIGINALS:
        cs = [json.loads(l) for l in (REPO / "corpus" / f"chunks_{stem}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        e = np.load(REPO / "results" / "phase2a" / f"{stem}_{SLUG}.npy")
        chunks += cs; labse.append(e)
    labse = np.vstack(labse); labse /= (np.linalg.norm(labse, axis=1, keepdims=True) + 1e-12)
    openai = np.load(OPENAI_CACHE)
    assert openai.shape[0] == len(chunks)
    return chunks, labse, openai


def rank(v):
    order = v.argsort(); r = np.empty_like(order, dtype=float); r[order] = np.arange(len(v))
    return r


def spearman(a, b):
    ra, rb = rank(a), rank(b)
    return float(np.corrcoef(ra, rb)[0, 1])


def rdm(emb, chunks, lang, concepts):
    """concept×concept dissimilarity (1-cos of centroids) within one language; None if a concept lacks MIN_N."""
    cents = {}
    for c in concepts:
        idx = [i for i, ch in enumerate(chunks)
               if ch["language"] == lang and c in (ch.get("option_a_concepts") or [])]
        if len(idx) >= MIN_N:
            v = emb[idx].mean(0); cents[c] = v / (np.linalg.norm(v) + 1e-12)
    return cents


def main():
    chunks, labse, openai = load()
    langs = sorted(set(c["language"] for c in chunks))
    print(f"{len(chunks)} chunks; languages: {langs}")

    # common concept set present (>=MIN_N) in ALL languages, per model (use union of presence)
    def build(emb):
        cents = {L: rdm(emb, chunks, L, CONCEPTS) for L in langs}
        common = [c for c in CONCEPTS if all(c in cents[L] for L in langs)]
        return cents, common

    results = {}
    for name, emb in [("LaBSE", labse), ("OpenAI", openai)]:
        cents, common = build(emb)
        K = len(common)
        # RDM upper-triangle per language over the common concept set
        iu = np.triu_indices(K, 1)
        rdms = {}
        for L in langs:
            M = np.array([[1 - float(cents[L][a] @ cents[L][b]) for b in common] for a in common])
            rdms[L] = M[iu]
        # cross-language RDM Spearman matrix
        C = np.array([[spearman(rdms[a], rdms[b]) for b in langs] for a in langs])
        off = C[np.triu_indices(len(langs), 1)]
        # shuffled-concept null: permute common-concept order in one language's RDM
        rng = np.random.default_rng(0)
        null = []
        for _ in range(2000):
            perm = rng.permutation(K)
            # rebuild a permuted RDM upper-tri for each language, recompute mean off-diag corr
            pr = {}
            for L in langs:
                Mp = np.array([[1 - float(cents[L][common[perm[i]]] @ cents[L][common[perm[j]]]) for j in range(K)] for i in range(K)])
                pr[L] = Mp[iu]
            # correlate UNpermuted A vs permuted B is complex; simpler: shuffle one language's labels vs others unshuffled
            a = langs[0]
            cs = [spearman(rdms[a], pr[b]) for b in langs[1:]]
            null.append(np.mean(cs))
        # observed mean corr of langs[0] vs others (matches null construction)
        obs0 = np.mean([C[0, j] for j in range(1, len(langs))])
        p = float((np.array(null) >= obs0).mean())
        results[name] = (common, C, off, obs0, p)
        print(f"\n=== {name}: common concepts (K={K}): {common} ===")
        print(f"  mean cross-language RDM Spearman = {off.mean():+.3f}  (range {off.min():+.3f}..{off.max():+.3f})")
        print(f"  anchor-lang({langs[0]}) vs others mean = {obs0:+.3f}  shuffled-concept null p = {p:.4f}")
        # per-concept stability: variance of each concept's mean dissimilarity-to-others across languages
        print("  per-concept structural-role stability (low std across langs = stable anchor):")
        for ci, c in enumerate(common):
            rowmeans = []
            for L in langs:
                M = np.array([[1 - float(cents[L][a] @ cents[L][b]) for b in common] for a in common])
                rowmeans.append(M[ci].sum() / (K - 1))
            print(f"    {c:11s} mean-dissim={np.mean(rowmeans):.3f}  std-across-langs={np.std(rowmeans):.3f}")

    # cross-MODEL robustness: do LaBSE and OpenAI agree on the cross-language isomorphism pattern?
    if "LaBSE" in results and "OpenAI" in results:
        _, _, offL, _, _ = results["LaBSE"]; _, _, offO, _, _ = results["OpenAI"]
        if len(offL) == len(offO):
            print(f"\n=== MODEL ROBUSTNESS: LaBSE vs OpenAI cross-language RDM-correlation patterns ===")
            print(f"  Pearson(LaBSE off-diag, OpenAI off-diag) = {np.corrcoef(offL, offO)[0,1]:+.3f}")
            print(f"  LaBSE mean={offL.mean():+.3f}  OpenAI mean={offO.mean():+.3f}  (raw cross-language CCB flipped between these models)")


if __name__ == "__main__":
    main()
