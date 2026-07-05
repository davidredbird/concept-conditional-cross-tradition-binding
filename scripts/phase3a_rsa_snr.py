"""
Phase 3a — RSA SNR CURVE: how does cross-language concept-geometry isomorphism rise with
n (passages per concept-centroid)? Sizes the corpus requirement for the RSA-based Phase 3a.
Firewall-safe (Phase 2c originals).

Fixed 5×5 grid (drop rarest concepts NONSEP/RECOGNITION + smallest language hebrew so cells
are large enough to subsample): concepts {SUBSTRATE,AWARENESS,ULTIMATE,WORLD,SELF} ×
languages {classical_chinese,arabic,greek,hindi,spanish}. Subsample every cell to n, build
RDMs, mean cross-language isomorphism; bootstrap; sweep n up to the grid's min cell count.

Usage: python scripts/phase3a_rsa_snr.py
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
CONC = ["SUBSTRATE", "AWARENESS", "ULTIMATE", "WORLD", "SELF"]
LANGS = ["classical_chinese", "arabic", "greek", "hindi", "spanish"]
B = 120


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
    tags = [set(hc.tag(c["language"], c["text"])) for c in chunks]
    cell = {(L, c): [i for i, ch in enumerate(chunks) if ch["language"] == L and c in tags[i]]
            for L in LANGS for c in CONC}
    counts = {k: len(v) for k, v in cell.items()}
    Nmax = min(counts.values())
    print(f"grid {len(CONC)} concepts × {len(LANGS)} langs; min cell = {Nmax} at {min(counts, key=counts.get)}")
    ns = [n for n in [8, 12, 20, 35, 60, 100, 150, 220] if n <= Nmax] + [Nmax]
    ns = sorted(set(ns))
    iu = np.triu_indices(len(CONC), 1)
    lp = np.triu_indices(len(LANGS), 1)
    rng = np.random.default_rng(0)

    print(f"\n{'n/concept':>10}{'LaBSE iso':>11}{'OpenAI iso':>12}")
    curves = {"LaBSE": [], "OpenAI": []}
    for n in ns:
        row = {}
        for name, emb in [("LaBSE", labse), ("OpenAI", openai)]:
            iso = []
            for _ in range(B):
                rd = {}
                for L in LANGS:
                    cc = {}
                    for c in CONC:
                        idx = rng.choice(cell[(L, c)], size=n, replace=False)
                        v = emb[idx].mean(0); cc[c] = v / (np.linalg.norm(v) + 1e-12)
                    M = np.array([[1 - float(cc[a] @ cc[b]) for b in CONC] for a in CONC])
                    rd[L] = M[iu]
                C = np.array([[spearman(rd[a], rd[b]) for b in LANGS] for a in LANGS])
                iso.append(C[lp].mean())
            row[name] = np.mean(iso); curves[name].append(np.mean(iso))
        print(f"{n:>10}{row['LaBSE']:>+11.3f}{row['OpenAI']:>+12.3f}")

    print("\nInterpretation:")
    for name in ["LaBSE", "OpenAI"]:
        asym = curves[name][-1]
        # n to reach 80% of asymptote
        n80 = next((ns[i] for i in range(len(ns)) if curves[name][i] >= 0.8 * asym), ns[-1])
        print(f"  {name}: asymptote≈{asym:+.3f} at n={ns[-1]}; reaches 80% (~{0.8*asym:+.3f}) by n≈{n80} passages/concept/tradition")
    # corpus translation: n passages/concept ÷ prevalence = total passages/tradition needed
    print("\nCorpus sizing: need ~n SUBSTRATE-passages per tradition; at SUBSTRATE prevalence p,")
    print("  that is ~n/p total passages/tradition (e.g. n=60, p=0.2 -> ~300; p=0.5 -> ~120).")


if __name__ == "__main__":
    main()
