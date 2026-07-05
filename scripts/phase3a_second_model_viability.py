"""
Phase 3a — SECOND-MODEL viability test (firewall-safe: Phase 2c originals only, NOT the
sealed China×Greece gradient). Does OpenAI text-embedding-3-large (a general contrastive
embedder — a DIFFERENT objective from LaBSE's bitext-alignment) (1) survive the anisotropy
screen that rejected multilingual-e5, and (2) reproduce the SUBSTRATE-binds / AWARENESS-flat
dissociation? If yes, it corroborates the dissociation against LaBSE's alignment-objective.

Screen verdicts vs precedent: LaBSE cross-tradition cosine ~0.45-0.65 (healthy);
e5 cone-collapsed non-English to ~0.84 mean, std ~0.02 (REJECTED).

Usage: python scripts/phase3a_second_model_viability.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")
key = (REPO / ".openai_key").read_text(encoding="utf-8").strip()
os.environ.setdefault("OPENAI_API_KEY", key)

MODEL = "text-embedding-3-large"
CACHE = REPO / "results" / "phase3a" / "originals_openai_te3l.npy"
META = REPO / "results" / "phase3a" / "originals_openai_meta.json"
ORIGINALS = ["chinese_taote_chinese", "chinese_zhuangzi_chinese", "chinese_platform_sutra_chinese",
             "chinese_analects_chinese", "arabic_fusus_arabic", "arabic_najat_arabic",
             "greek_plotinus_greek", "greek_clement_greek", "hindi_kabir_hindi",
             "hindi_tulsidas_hindi", "hindi_surdas_hindi", "spanish_molinos_spanish",
             "spanish_teresa_spanish", "hebrew_nachman_hebrew"]
CONCEPTS = ["SUBSTRATE", "AWARENESS", "ULTIMATE", "WORLD", "SELF", "NONSEP", "RECOGNITION"]


def load_chunks():
    chunks = []
    for stem in ORIGINALS:
        cf = REPO / "corpus" / f"chunks_{stem}.jsonl"
        if not cf.exists():
            print(f"  skip {stem} (missing)"); continue
        chunks += [json.loads(l) for l in cf.read_text(encoding="utf-8").splitlines() if l.strip()]
    return chunks


def embed_openai(texts):
    import urllib.request
    out = []
    for i in range(0, len(texts), 100):
        batch = [t if t.strip() else " " for t in texts[i:i + 100]]
        body = json.dumps({"model": MODEL, "input": batch}).encode("utf-8")
        req = urllib.request.Request(
            "https://api.openai.com/v1/embeddings", data=body,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        for attempt in range(4):
            try:
                resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
                break
            except Exception as e:
                if attempt == 3:
                    raise
                import time; time.sleep(3)
        out.extend(d["embedding"] for d in sorted(resp["data"], key=lambda x: x["index"]))
        if i % 1000 == 0:
            print(f"    embedded {i+len(batch)}/{len(texts)}")
    a = np.asarray(out, dtype=np.float32)
    return a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-12)


def ccb(sim, has, mask):
    both = has[:, None] & has[None, :] & mask
    one = (has[:, None] ^ has[None, :]) & mask
    nb, no = int(both.sum()), int(one.sum())
    if nb == 0 or no == 0:
        return float("nan"), nb
    return float((sim * both).sum() / nb - (sim * one).sum() / no), nb


def main():
    chunks = load_chunks()
    texts = [c["text"] for c in chunks]
    lang = np.array([c["language"] for c in chunks])
    n = len(texts)
    print(f"{n} Phase 2c originals chunks; embedding with {MODEL} (cache: {CACHE.name})")

    if CACHE.exists() and json.loads(META.read_text())["n"] == n:
        emb = np.load(CACHE)
        print("  loaded cached embeddings")
    else:
        emb = embed_openai(texts)
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        np.save(CACHE, emb)
        META.write_text(json.dumps({"n": n, "model": MODEL}), encoding="utf-8")
    sim = emb @ emb.T

    up = np.triu(np.ones((n, n), bool), 1)
    cross = (lang[:, None] != lang[None, :]) & up
    same = (lang[:, None] == lang[None, :]) & up

    print("\n=== ANISOTROPY SCREEN (cosine spread; e5 FAILED at ~0.84 mean/0.02 std) ===")
    cv = sim[cross]
    print(f"  cross-tradition/cross-language cosine: mean={cv.mean():.3f}  std={cv.std():.3f}")
    print("  per-language within-language cosine (the e5 non-English collapse check):")
    for L in sorted(set(lang)):
        m = (lang[:, None] == L) & (lang[None, :] == L) & up
        if m.sum() > 50:
            s = sim[m]
            print(f"    {L:18s} mean={s.mean():.3f}  std={s.std():.3f}")

    rng = np.random.default_rng(0)
    def run(mask, label):
        print(f"\n=== {label} CCB ===")
        for c in CONCEPTS:
            has = np.array([c in (ch.get("option_a_concepts") or []) for ch in chunks])
            obs, nb = ccb(sim, has, mask)
            if np.isnan(obs):
                print(f"  {c:11s} na"); continue
            nw = int(has.sum()); diffs = []
            for _ in range(500):
                mm = np.zeros(n, bool); mm[rng.permutation(n)[:nw]] = True
                d, _ = ccb(sim, mm, mask)
                if not np.isnan(d):
                    diffs.append(d)
            p = float((np.array(diffs) >= obs).mean())
            print(f"  {c:11s} CCB={obs:+.4f}  p={p:.4f}  n_both={nb}")

    run(cross, "CROSS-LANGUAGE (translation-free; the dissociation test)")
    run(same, "WITHIN-LANGUAGE")
    print("\nCompare to LaBSE Phase 2c: cross-language SUBSTRATE +0.0066 (binds), AWARENESS +0.0005 (flat).")


if __name__ == "__main__":
    main()
