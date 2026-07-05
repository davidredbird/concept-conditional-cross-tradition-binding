"""
RSA vs CCB — head-to-head MODEL-ROBUSTNESS on the Phase 2c corpus (installment 1 of the
Phase 1+2 RSA-vs-CCB re-run, #72). Firewall-safe. Same corpus, same harmonized tags, both
LaBSE and OpenAI. The decisive question: which method gives MODEL-ROBUST conclusions?

- CCB per-concept (cross-language + within-language) on each model → cross-model agreement
  r(CCB_LaBSE, CCB_OpenAI) across the 7 concepts.
- RSA per-language-pair isomorphism on each model → cross-model agreement r(RSA_LaBSE, RSA_OpenAI).

If CCB cross-model r is low/negative while RSA's is high, CCB's per-concept conclusions are
model artifacts and RSA's holistic structure is the robust signal.

Usage: python scripts/phase3a_rsa_vs_ccb.py
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
MIN_N = 5


def load():
    chunks, labse = [], []
    for stem in ORIGINALS:
        cs = [json.loads(l) for l in (REPO / "corpus" / f"chunks_{stem}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        e = np.load(REPO / "results" / "phase2a" / f"{stem}_{SLUG}.npy")
        chunks += cs; labse.append(e)
    labse = np.vstack(labse); labse /= (np.linalg.norm(labse, axis=1, keepdims=True) + 1e-12)
    return chunks, labse, np.load(OPENAI_CACHE)


def ccb(sim, has, mask):
    both = has[:, None] & has[None, :] & mask
    one = (has[:, None] ^ has[None, :]) & mask
    nb, no = int(both.sum()), int(one.sum())
    return float((sim * both).sum() / nb - (sim * one).sum() / no) if nb and no else np.nan


def rank(v):
    o = v.argsort(); r = np.empty_like(o, float); r[o] = np.arange(len(v)); return r


def spearman(a, b):
    return float(np.corrcoef(rank(a), rank(b))[0, 1])


def main():
    chunks, labse, openai = load()
    n = len(chunks)
    lang = np.array([c["language"] for c in chunks])
    langs = sorted(set(lang))
    tags = [set(hc.tag(c["language"], c["text"])) for c in chunks]
    has = {c: np.array([c in t for t in tags]) for c in CONCEPTS}
    up = np.triu(np.ones((n, n), bool), 1)
    cross = (lang[:, None] != lang[None, :]) & up
    same = (lang[:, None] == lang[None, :]) & up

    ccb_x, ccb_w, rsa_off = {}, {}, {}
    for name, emb in [("LaBSE", labse), ("OpenAI", openai)]:
        sim = emb @ emb.T
        ccb_x[name] = np.array([ccb(sim, has[c], cross) for c in CONCEPTS])
        ccb_w[name] = np.array([ccb(sim, has[c], same) for c in CONCEPTS])
        # RSA isomorphism per language pair
        cents = {}
        for L in langs:
            cc = {}
            for c in CONCEPTS:
                idx = [i for i in range(n) if lang[i] == L and has[c][i]]
                if len(idx) >= MIN_N:
                    v = emb[idx].mean(0); cc[c] = v / (np.linalg.norm(v) + 1e-12)
            cents[L] = cc
        common = [c for c in CONCEPTS if all(c in cents[L] for L in langs)]
        iu = np.triu_indices(len(common), 1)
        rd = {L: np.array([[1 - float(cents[L][a] @ cents[L][b]) for b in common] for a in common])[iu] for L in langs}
        Cm = np.array([[spearman(rd[a], rd[b]) for b in langs] for a in langs])
        rsa_off[name] = Cm[np.triu_indices(len(langs), 1)]

    print("Per-concept CROSS-LANGUAGE CCB (the published dissociation lives here):")
    print(f"  {'concept':<12}{'LaBSE':>9}{'OpenAI':>9}")
    for i, c in enumerate(CONCEPTS):
        print(f"  {c:<12}{ccb_x['LaBSE'][i]:>+9.4f}{ccb_x['OpenAI'][i]:>+9.4f}")

    rxc = np.corrcoef(ccb_x["LaBSE"], ccb_x["OpenAI"])[0, 1]
    rwc = np.corrcoef(ccb_w["LaBSE"], ccb_w["OpenAI"])[0, 1]
    rsa_r = np.corrcoef(rsa_off["LaBSE"], rsa_off["OpenAI"])[0, 1]
    print("\n=== MODEL-ROBUSTNESS (LaBSE vs OpenAI agreement) ===")
    print(f"  CCB cross-language  per-concept r = {rxc:+.3f}   <- the published conclusions")
    print(f"  CCB within-language per-concept r = {rwc:+.3f}")
    print(f"  RSA per-language-pair isomorphism r = {rsa_r:+.3f}")
    print(f"\n  RSA isomorphism: LaBSE mean {rsa_off['LaBSE'].mean():+.3f} / OpenAI {rsa_off['OpenAI'].mean():+.3f}")
    print(f"  VERDICT: {'CCB cross-language conclusions are MODEL-FRAGILE' if rxc < 0.4 else 'CCB cross-language is model-robust'}; "
          f"{'RSA is MODEL-ROBUST' if rsa_r > 0.6 else 'RSA model-robustness weak'}.")


if __name__ == "__main__":
    main()
