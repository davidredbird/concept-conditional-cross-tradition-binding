"""
Phase 3a — EQUAL-N RSA: does the distinctive-concept (SUBSTRATE/RECOGNITION/NONSEP)
cross-language variability survive sample-size equalization, or is it small-n centroid
noise (those are the rarer concepts)? Firewall-safe (Phase 2c originals).

Method: subsample EVERY (concept × language) cell to a common floor F (= min cell count),
so all concept-centroids carry the SAME sampling noise. Bootstrap B times. If at equal-n the
backbone concepts (AWARENESS/ULTIMATE/WORLD/SELF) become as cross-language-variable as
SUBSTRATE/RECOGNITION/NONSEP, the original gap was sample size. If the gap persists, divergence
is real. Tags on-the-fly via harmonized_concepts (incl. the Greek SUBSTRATE ὕλη fix).

Compare to UNEQUAL-N (recheck): SUBSTRATE std 0.014 LaBSE / 0.035 OpenAI; backbone 0.005-0.008
/ 0.018-0.024; REC/NONSEP 0.016-0.017 / 0.043-0.051.

Usage: python scripts/phase3a_rsa_equalN.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")
import importlib, harmonized_concepts as hc  # noqa: E402
importlib.reload(hc)

SLUG = "sentence_transformers__LaBSE"
ORIGINALS = ["chinese_taote_chinese", "chinese_zhuangzi_chinese", "chinese_platform_sutra_chinese",
             "chinese_analects_chinese", "arabic_fusus_arabic", "arabic_najat_arabic",
             "greek_plotinus_greek", "greek_clement_greek", "hindi_kabir_hindi",
             "hindi_tulsidas_hindi", "hindi_surdas_hindi", "spanish_molinos_spanish",
             "spanish_teresa_spanish", "hebrew_nachman_hebrew"]
OPENAI_CACHE = REPO / "results" / "phase3a" / "originals_openai_te3l.npy"
CONCEPTS = ["SUBSTRATE", "AWARENESS", "ULTIMATE", "WORLD", "SELF", "RECOGNITION", "NONSEP"]
BACKBONE = {"AWARENESS", "ULTIMATE", "WORLD", "SELF"}
B = 200


def load():
    chunks, labse = [], []
    for stem in ORIGINALS:
        cs = [json.loads(l) for l in (REPO / "corpus" / f"chunks_{stem}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        e = np.load(REPO / "results" / "phase2a" / f"{stem}_{SLUG}.npy")
        chunks += cs; labse.append(e)
    labse = np.vstack(labse); labse /= (np.linalg.norm(labse, axis=1, keepdims=True) + 1e-12)
    return chunks, labse, np.load(OPENAI_CACHE)


def rank(v):
    o = v.argsort(); r = np.empty_like(o, float); r[o] = np.arange(len(v)); return r


def spearman(a, b):
    return float(np.corrcoef(rank(a), rank(b))[0, 1])


def main():
    chunks, labse, openai = load()
    langs = sorted(set(c["language"] for c in chunks))
    tags = [set(hc.tag(c["language"], c["text"])) for c in chunks]
    # cell index lists
    cell = {(L, c): [i for i, ch in enumerate(chunks) if ch["language"] == L and c in tags[i]]
            for L in langs for c in CONCEPTS}
    counts = {k: len(v) for k, v in cell.items()}
    F = min(counts.values())
    cmin = min(counts, key=counts.get)
    print(f"per-cell counts: min={F} at {cmin}; equalizing all {len(CONCEPTS)}×{len(langs)} cells to n={F}, B={B} bootstraps")

    rng = np.random.default_rng(0)
    iu = np.triu_indices(len(CONCEPTS), 1)
    lpairs = np.triu_indices(len(langs), 1)

    for name, emb in [("LaBSE", labse), ("OpenAI", openai)]:
        per_concept_std = {c: [] for c in CONCEPTS}
        isos = []
        for _ in range(B):
            cents = {}
            for L in langs:
                cc = {}
                for c in CONCEPTS:
                    idx = rng.choice(cell[(L, c)], size=F, replace=False)
                    v = emb[idx].mean(0); cc[c] = v / (np.linalg.norm(v) + 1e-12)
                cents[L] = cc
            # RDMs + isomorphism
            rd = {L: np.array([[1 - float(cents[L][a] @ cents[L][b]) for b in CONCEPTS] for a in CONCEPTS]) for L in langs}
            C = np.array([[spearman(rd[a][iu], rd[b][iu]) for b in langs] for a in langs])
            isos.append(C[lpairs].mean())
            # per-concept cross-language std of mean-dissim
            for ci, c in enumerate(CONCEPTS):
                md = [rd[L][ci][[j for j in range(len(CONCEPTS)) if j != ci]].mean() for L in langs]
                per_concept_std[c].append(np.std(md))
        print(f"\n=== {name}: equal-n (F={F}) RSA, {B} bootstraps ===")
        print(f"  mean isomorphism = {np.mean(isos):+.3f}")
        print(f"  per-concept cross-language std at EQUAL n (lower=more stable):")
        ordered = sorted(CONCEPTS, key=lambda c: np.mean(per_concept_std[c]))
        for c in ordered:
            grp = "backbone" if c in BACKBONE else "DISTINCTIVE"
            print(f"    {c:11s} std={np.mean(per_concept_std[c]):.3f}  [{grp}]")
        bb = np.mean([np.mean(per_concept_std[c]) for c in CONCEPTS if c in BACKBONE])
        ds = np.mean([np.mean(per_concept_std[c]) for c in ["SUBSTRATE", "RECOGNITION", "NONSEP"]])
        print(f"  backbone mean std={bb:.3f}  vs  distinctive(SUB/REC/NONSEP) mean std={ds:.3f}  "
              f"-> {'gap PERSISTS (real divergence)' if ds > bb*1.3 else 'gap CLOSED (was sample size)'}")


if __name__ == "__main__":
    main()
