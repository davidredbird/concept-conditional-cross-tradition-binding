"""
RSA vs CCB on PHASE 1 (English whole-book corpus) — installment 2 of #72. Does the
model-fragility of CCB / model-robustness of RSA replicate in the FOUNDATIONAL English
data? Same head-to-head as installment 1 (phase3a_rsa_vs_ccb.py), systems = the 11
English traditions, both models (OpenAI te3-large + LaBSE), harmonized English tags.

Uses the full 6009-chunk Phase 1 set (not the 920-passage subsample) for adequate
per-tradition centroid n. Embeddings cached. Firewall-safe (Phase 1 English).

Usage: python scripts/phase1_rsa_vs_ccb.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")
import importlib, harmonized_concepts as hc  # noqa: E402
importlib.reload(hc)

KEY = (REPO / ".openai_key").read_text(encoding="utf-8").strip()
OAI_MODEL = "text-embedding-3-large"
OAI_CACHE = REPO / "results" / "phase3a" / "phase1_openai.npy"
LAB_CACHE = REPO / "results" / "phase3a" / "phase1_labse.npy"
CONCEPTS = ["SUBSTRATE", "AWARENESS", "ULTIMATE", "WORLD", "SELF", "RECOGNITION", "NONSEP"]
MIN_N = 10


def load_chunks():
    return [json.loads(l) for l in (REPO / "corpus" / "chunks.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]


def embed_openai(texts):
    out = []
    for i in range(0, len(texts), 100):
        batch = [t if t.strip() else " " for t in texts[i:i + 100]]
        body = json.dumps({"model": OAI_MODEL, "input": batch}).encode("utf-8")
        req = urllib.request.Request("https://api.openai.com/v1/embeddings", data=body,
                                     headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
        for a in range(4):
            try:
                resp = json.loads(urllib.request.urlopen(req, timeout=120).read()); break
            except Exception:
                if a == 3: raise
                import time; time.sleep(3)
        out.extend(d["embedding"] for d in sorted(resp["data"], key=lambda x: x["index"]))
        if i % 1000 == 0: print(f"    openai {i+len(batch)}/{len(texts)}")
    a = np.asarray(out, dtype=np.float32); return a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-12)


def embed_labse(texts):
    from multilingual_embedder import MultilingualEmbedder
    v = MultilingualEmbedder("sentence-transformers/LaBSE").encode(texts, batch_size=64)
    return v / (np.linalg.norm(v, axis=1, keepdims=True) + 1e-12)


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
    chunks = load_chunks()
    texts = [c["text"] for c in chunks]
    trad = np.array([c["tradition"] for c in chunks])
    trads = sorted(set(trad))
    n = len(chunks)
    tags = [set(hc.tag("english", t)) for t in texts]
    has = {c: np.array([c in t for t in tags]) for c in CONCEPTS}
    print(f"{n} Phase 1 chunks, {len(trads)} traditions; tags via harmonized english")

    if OAI_CACHE.exists() and np.load(OAI_CACHE).shape[0] == n:
        oai = np.load(OAI_CACHE)
    else:
        OAI_CACHE.parent.mkdir(parents=True, exist_ok=True); oai = embed_openai(texts); np.save(OAI_CACHE, oai)
    if LAB_CACHE.exists() and np.load(LAB_CACHE).shape[0] == n:
        lab = np.load(LAB_CACHE)
    else:
        lab = embed_labse(texts); np.save(LAB_CACHE, lab)

    up = np.triu(np.ones((n, n), bool), 1)
    cross = (trad[:, None] != trad[None, :]) & up

    ccb_x, rsa_off = {}, {}
    for name, emb in [("LaBSE", lab), ("OpenAI", oai)]:
        sim = emb @ emb.T
        ccb_x[name] = np.array([ccb(sim, has[c], cross) for c in CONCEPTS])
        cents = {}
        for T in trads:
            cc = {}
            for c in CONCEPTS:
                idx = [i for i in range(n) if trad[i] == T and has[c][i]]
                if len(idx) >= MIN_N:
                    v = emb[idx].mean(0); cc[c] = v / (np.linalg.norm(v) + 1e-12)
            cents[T] = cc
        common = [c for c in CONCEPTS if sum(c in cents[T] for T in trads) >= len(trads) - 1]
        use_tr = [T for T in trads if all(c in cents[T] for c in common)]
        iu = np.triu_indices(len(common), 1)
        rd = {T: np.array([[1 - float(cents[T][a] @ cents[T][b]) for b in common] for a in common])[iu] for T in use_tr}
        Cm = np.array([[spearman(rd[a], rd[b]) for b in use_tr] for a in use_tr])
        rsa_off[name] = Cm[np.triu_indices(len(use_tr), 1)]
        if name == "LaBSE":
            print(f"RSA: {len(use_tr)} traditions, {len(common)} common concepts: {common}")

    print("\nPer-concept CROSS-TRADITION CCB (English):")
    print(f"  {'concept':<12}{'LaBSE':>9}{'OpenAI':>9}")
    for i, c in enumerate(CONCEPTS):
        print(f"  {c:<12}{ccb_x['LaBSE'][i]:>+9.4f}{ccb_x['OpenAI'][i]:>+9.4f}")
    rxc = np.corrcoef(ccb_x["LaBSE"], ccb_x["OpenAI"])[0, 1]
    rsa_r = np.corrcoef(rsa_off["LaBSE"], rsa_off["OpenAI"])[0, 1]
    print("\n=== MODEL-ROBUSTNESS (Phase 1 English; cf. Phase 2: CCB r=-0.43, RSA r=+0.78) ===")
    print(f"  CCB cross-tradition per-concept r(LaBSE,OpenAI) = {rxc:+.3f}")
    print(f"  RSA cross-tradition isomorphism r(LaBSE,OpenAI)  = {rsa_r:+.3f}")
    print(f"  RSA mean isomorphism: LaBSE {rsa_off['LaBSE'].mean():+.3f} / OpenAI {rsa_off['OpenAI'].mean():+.3f}")
    print(f"  VERDICT: CCB {'MODEL-FRAGILE' if rxc < 0.4 else 'robust'}; RSA {'MODEL-ROBUST' if rsa_r > 0.6 else 'weak'} "
          f"-> {'pattern REPLICATES in English' if rxc < 0.4 and rsa_r > 0.6 else 'pattern differs in English'}")


if __name__ == "__main__":
    main()
