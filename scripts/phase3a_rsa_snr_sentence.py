"""
Phase 3a — SENTENCE-LEVEL RSA SNR curve. Does sentence granularity (≈5-6× more units +
purer concept-units, the Phase 1 lesson) push per-concept n into the powerable range where
chunk-level capped out (n=65 → iso ~0.06; full-corpus chunks → ~0.4)? Firewall-safe (Phase
2c originals). LaBSE only (power trend; model-robustness already settled). Efficient: split
→ tag → embed ONLY tagged sentences.

Usage: python scripts/phase3a_rsa_snr_sentence.py
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
import importlib, harmonized_concepts as hc  # noqa: E402
importlib.reload(hc)

ORIGINALS = ["chinese_taote_chinese", "chinese_zhuangzi_chinese", "chinese_platform_sutra_chinese",
             "chinese_analects_chinese", "arabic_fusus_arabic", "arabic_najat_arabic",
             "greek_plotinus_greek", "greek_clement_greek", "hindi_kabir_hindi",
             "hindi_tulsidas_hindi", "hindi_surdas_hindi", "spanish_molinos_spanish",
             "spanish_teresa_spanish", "hebrew_nachman_hebrew"]
CONC = ["SUBSTRATE", "AWARENESS", "ULTIMATE", "WORLD", "SELF"]
LANGS = ["classical_chinese", "arabic", "greek", "hindi", "spanish"]
SENT = re.compile(r"[.!?。！？।॥؛؟·\n]+")
B = 100


def sentences(text):
    return [s.strip() for s in SENT.split(text) if len(s.strip()) >= 10]


def rank(v):
    o = v.argsort(); r = np.empty_like(o, float); r[o] = np.arange(len(v)); return r


def spearman(a, b):
    return float(np.corrcoef(rank(a), rank(b))[0, 1])


def main():
    # split all Phase 2c originals into sentences, tag, keep tagged
    sents, slang = [], []
    for stem in ORIGINALS:
        for l in (REPO / "corpus" / f"chunks_{stem}.jsonl").read_text(encoding="utf-8").splitlines():
            if not l.strip():
                continue
            ch = json.loads(l)
            for s in sentences(ch["text"]):
                sents.append((ch["language"], s))
    print(f"{len(sents)} sentences from Phase 2c originals; tagging…")
    tagged = []
    for L, s in sents:
        t = hc.tag(L, s)
        if any(c in t for c in CONC):
            tagged.append((L, s, set(t)))
    print(f"{len(tagged)} sentences tagged with ≥1 of {CONC}; embedding (LaBSE)…")

    from multilingual_embedder import MultilingualEmbedder
    emb = MultilingualEmbedder("sentence-transformers/LaBSE")
    V = emb.encode([s for _, s, _ in tagged], batch_size=64)
    V = V / (np.linalg.norm(V, axis=1, keepdims=True) + 1e-12)

    tl = np.array([t[0] for t in tagged])
    cell = {(L, c): [i for i in range(len(tagged)) if tl[i] == L and c in tagged[i][2]]
            for L in LANGS for c in CONC}
    counts = {k: len(v) for k, v in cell.items()}
    Nmax = min(counts.values())
    print(f"sentence cells: min={Nmax} at {min(counts, key=counts.get)} (chunk-level min was 65)")

    ns = sorted(set([n for n in [20, 50, 100, 200, 400, 700, 1200] if n <= Nmax] + [Nmax]))
    iu = np.triu_indices(len(CONC), 1)
    lp = np.triu_indices(len(LANGS), 1)
    rng = np.random.default_rng(0)
    print(f"\n{'n_sent/concept':>15}{'LaBSE iso':>11}")
    curve = []
    for n in ns:
        iso = []
        for _ in range(B):
            rd = {}
            for L in LANGS:
                cc = {}
                for c in CONC:
                    idx = rng.choice(cell[(L, c)], size=n, replace=False)
                    v = V[idx].mean(0); cc[c] = v / (np.linalg.norm(v) + 1e-12)
                rd[L] = np.array([[1 - float(cc[a] @ cc[b]) for b in CONC] for a in CONC])[iu]
            C = np.array([[spearman(rd[a], rd[b]) for b in LANGS] for a in LANGS])
            iso.append(C[lp].mean())
        curve.append(np.mean(iso))
        print(f"{n:>15}{np.mean(iso):>+11.3f}")
    print(f"\n  chunk-level reached only +0.06 at its max n=65; full-corpus chunks ~0.4.")
    print(f"  sentence-level reaches {curve[-1]:+.3f} at n={ns[-1]} sentences/concept.")
    print(f"  -> {'sentence-level RECOVERS the signal (purer units help)' if curve[-1] > 0.25 else 'sentence-level helps modestly; signal still needs large n'}")


if __name__ == "__main__":
    main()
