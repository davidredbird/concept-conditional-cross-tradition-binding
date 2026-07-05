"""
Phase 3a — FACET-decomposed RSA prototype (firewall-safe: Phase 2c originals).
Tests whether expanding the RDM with SUBSTRATE facets sharpens cross-language isomorphism,
and FIRST checks the gating question: are the facet sub-centroids distinct enough to add
resolution, or near-degenerate (cos≈1) so they only add noise?

Baseline (7 whole concepts, prior prototype): LaBSE mean RDM-corr +0.363 (null p .052),
OpenAI +0.432 (p .031), model agreement r=0.79.

Usage: python scripts/phase3a_rsa_facet.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")
import harmonized_concepts as hc  # noqa: E402

SLUG = "sentence_transformers__LaBSE"
ORIGINALS = ["chinese_taote_chinese", "chinese_zhuangzi_chinese", "chinese_platform_sutra_chinese",
             "chinese_analects_chinese", "arabic_fusus_arabic", "arabic_najat_arabic",
             "greek_plotinus_greek", "greek_clement_greek", "hindi_kabir_hindi",
             "hindi_tulsidas_hindi", "hindi_surdas_hindi", "spanish_molinos_spanish",
             "spanish_teresa_spanish", "hebrew_nachman_hebrew"]
OPENAI_CACHE = REPO / "results" / "phase3a" / "originals_openai_te3l.npy"
WHOLE = ["AWARENESS", "ULTIMATE", "WORLD", "SELF", "RECOGNITION", "NONSEP"]  # SUBSTRATE faceted out

# SUBSTRATE → 4 cross-lingually shared facets (terms drawn from harmonized_concepts.TERMS)
SUB_FACETS = {
    "S_emptiness": {"classical_chinese": ["空", "虛", "幻"], "greek": ["κενωσι"], "hindi": ["सून्य", "शून्य", "माया"],
                    "arabic": ["الخلاء"], "hebrew": ["תהו"], "spanish": [r"\bnada\b", r"\bvacío\b", r"\babismo\b"]},
    "S_nonbeing": {"classical_chinese": ["無", "無為", "無形"], "greek": ["μη ον", "ανειδε", "απειρ"],
                   "hindi": ["निरगुन", "निर्गुण", "अव्यक्त", "निराकार"], "arabic": ["العدم", "الغيب", "البطون"],
                   "hebrew": ["העדר", "אפס"], "spanish": [r"\bno[- ]?ser\b", r"\binforme\b"]},
    "S_impermanence": {"classical_chinese": ["無常"], "greek": ["ματαιοτη"], "hindi": ["नश्वर", "क्षणिक"],
                       "arabic": ["الزوال"], "hebrew": ["הבל"], "spanish": [r"\bvanidad", r"\bperecedero"]},
    "S_dissolution": {"classical_chinese": ["寂滅"], "greek": ["φθορα"], "hindi": ["लय", "अभाव"],
                      "arabic": ["الفناء", "الهلاك"], "hebrew": ["כליון", "אפיסה"], "spanish": [r"\baniquila", r"\bdisoluci"]},
}


def matches(language, term, text):
    mode = hc._MATCH[language]
    if mode == "regex":
        return re.search(term, text, re.I) is not None
    if mode == "substr":
        return term in text
    _, norm = mode
    return norm(term) in norm(text)


def load():
    chunks, labse = [], []
    for stem in ORIGINALS:
        cs = [json.loads(l) for l in (REPO / "corpus" / f"chunks_{stem}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        e = np.load(REPO / "results" / "phase2a" / f"{stem}_{SLUG}.npy")
        chunks += cs; labse.append(e)
    labse = np.vstack(labse); labse /= (np.linalg.norm(labse, axis=1, keepdims=True) + 1e-12)
    openai = np.load(OPENAI_CACHE)
    return chunks, labse, openai


def rank(v):
    o = v.argsort(); r = np.empty_like(o, float); r[o] = np.arange(len(v)); return r


def spearman(a, b):
    return float(np.corrcoef(rank(a), rank(b))[0, 1])


def centroid(emb, idx):
    if len(idx) < 5:
        return None
    v = emb[idx].mean(0); return v / (np.linalg.norm(v) + 1e-12)


def main():
    chunks, labse, openai = load()
    langs = sorted(set(c["language"] for c in chunks))

    for name, emb in [("LaBSE", labse), ("OpenAI", openai)]:
        # build conditions per language: whole concepts + SUBSTRATE facets
        cond_cent = {L: {} for L in langs}
        for L in langs:
            for c in WHOLE:
                idx = [i for i, ch in enumerate(chunks) if ch["language"] == L and c in (ch.get("option_a_concepts") or [])]
                v = centroid(emb, idx)
                if v is not None:
                    cond_cent[L][c] = v
            for fname, fmap in SUB_FACETS.items():
                terms = fmap.get(L, [])
                idx = [i for i, ch in enumerate(chunks) if ch["language"] == L and any(matches(L, t, ch["text"]) for t in terms)]
                v = centroid(emb, idx)
                if v is not None:
                    cond_cent[L][fname] = v
        common = [c for c in (WHOLE + list(SUB_FACETS)) if all(c in cond_cent[L] for L in langs)]
        K = len(common)
        iu = np.triu_indices(K, 1)
        rdms = {L: np.array([[1 - float(cond_cent[L][a] @ cond_cent[L][b]) for b in common] for a in common])[iu] for L in langs}
        C = np.array([[spearman(rdms[a], rdms[b]) for b in langs] for a in langs])
        off = C[np.triu_indices(len(langs), 1)]

        # degeneracy: mean pairwise cosine among the 4 SUBSTRATE facet-centroids, per language
        deg = []
        for L in langs:
            fs = [cond_cent[L][f] for f in SUB_FACETS if f in cond_cent[L]]
            if len(fs) >= 2:
                cc = [float(fs[i] @ fs[j]) for i in range(len(fs)) for j in range(i + 1, len(fs))]
                deg.append(np.mean(cc))
        print(f"\n=== {name}: FACET-RSA (K={K} conditions: {common}) ===")
        print(f"  facets present: {[f for f in SUB_FACETS if all(f in cond_cent[L] for L in langs)]}")
        print(f"  mean cross-language RDM Spearman = {off.mean():+.3f}  (baseline 7-concept: "
              f"{'+0.363' if name=='LaBSE' else '+0.432'})")
        print(f"  SUBSTRATE facet-centroid degeneracy: mean pairwise cos among facets = {np.mean(deg):.3f} "
              f"(≈1 ⇒ facets near-degenerate, add noise not resolution)")


if __name__ == "__main__":
    main()
