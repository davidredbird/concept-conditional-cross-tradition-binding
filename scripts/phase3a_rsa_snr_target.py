"""
Phase 3a — RSA SNR *target-n* curve. The basic SNR curve (phase3a_rsa_snr.py) capped at
n=65 because the rarest cell (spanish x SELF) bottlenecks a 5-language grid, so it never
reached the isomorphism plateau and could not yield a corpus-sizing target. This variant
DROPS the two smallest languages (spanish, hebrew) to raise the per-cell floor, extends the
n-sweep, and adds a PERMUTATION NULL at each n so we can read off the n at which the holistic
isomorphism reliably clears chance. That n / per-concept-prevalence = the chunks/concept/
tradition each Axial cell must supply -> the corpus-enlargement target.

Firewall-safe (Phase 2c originals only). Both models (LaBSE cache + OpenAI cache).

Usage: python scripts/phase3a_rsa_snr_target.py
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
             "hindi_tulsidas_hindi", "hindi_surdas_hindi"]  # spanish/hebrew dropped to raise floor
OPENAI_CACHE = REPO / "results" / "phase3a" / "originals_openai_te3l.npy"
CONC = ["SUBSTRATE", "AWARENESS", "ULTIMATE", "WORLD", "SELF"]
LANGS = ["classical_chinese", "arabic", "greek", "hindi"]
B = 120        # bootstrap subsamples per n
NPERM = 200    # permutation-null draws per n


def load():
    chunks, labse = [], []
    # OpenAI cache is aligned to the FULL originals order (incl. spanish/hebrew); rebuild the
    # same global index so we can slice OpenAI rows for the kept stems.
    full = ["chinese_taote_chinese", "chinese_zhuangzi_chinese", "chinese_platform_sutra_chinese",
            "chinese_analects_chinese", "arabic_fusus_arabic", "arabic_najat_arabic",
            "greek_plotinus_greek", "greek_clement_greek", "hindi_kabir_hindi",
            "hindi_tulsidas_hindi", "hindi_surdas_hindi", "spanish_molinos_spanish",
            "spanish_teresa_spanish", "hebrew_nachman_hebrew"]
    openai_full = np.load(OPENAI_CACHE)
    keep_oa, off = [], 0
    for stem in full:
        n = sum(1 for l in (REPO / "corpus" / f"chunks_{stem}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())
        if stem in ORIGINALS:
            keep_oa.append(openai_full[off:off + n])
        off += n
    openai = np.vstack(keep_oa)
    for stem in ORIGINALS:
        cs = [json.loads(l) for l in (REPO / "corpus" / f"chunks_{stem}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        e = np.load(REPO / "results" / "phase2a" / f"{stem}_{SLUG}.npy")
        chunks += cs; labse.append(e)
    labse = np.vstack(labse); labse /= (np.linalg.norm(labse, axis=1, keepdims=True) + 1e-12)
    assert len(chunks) == openai.shape[0] == labse.shape[0], (len(chunks), openai.shape, labse.shape)
    return chunks, labse, openai


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
    print(f"grid {len(CONC)} concepts x {len(LANGS)} langs (spanish/hebrew dropped)")
    print(f"min cell = {Nmax} at {min(counts, key=counts.get)}  (5-lang grid floor was 65)")
    for L in LANGS:
        print(f"  {L:>18}: " + " ".join(f"{c}={counts[(L,c)]}" for c in CONC))
    iu = np.triu_indices(len(CONC), 1)
    lp = np.triu_indices(len(LANGS), 1)
    rng = np.random.default_rng(0)
    ns = sorted(set([n for n in [20, 35, 60, 100, 150, 220, 320, 450] if n <= Nmax] + [Nmax]))

    print(f"\n{'n/concept':>10}{'LaBSE iso':>11}{'L p':>7}{'OpenAI iso':>12}{'OA p':>7}")
    for n in ns:
        out = {}
        for name, emb in [("LaBSE", labse), ("OpenAI", openai)]:
            obs, perm = [], []
            for _ in range(B):
                rd = {}
                for L in LANGS:
                    cc = {}
                    for c in CONC:
                        idx = rng.choice(cell[(L, c)], size=n, replace=False)
                        v = emb[idx].mean(0); cc[c] = v / (np.linalg.norm(v) + 1e-12)
                    M = np.array([[1 - float(cc[a] @ cc[b]) for b in CONC] for a in CONC])
                    rd[L] = M
                # observed: correlate RDM upper-triangles across languages
                tri = {L: rd[L][iu] for L in LANGS}
                C = np.array([[spearman(tri[a], tri[b]) for b in LANGS] for a in LANGS])
                obs.append(C[lp].mean())
            # permutation null: shuffle concept order of each language's RDM independently
            base = rd  # reuse last bootstrap's RDMs as a representative draw set is weak;
            # instead build the null from fresh subsamples to match obs variance:
            for _ in range(NPERM):
                rdp = {}
                for L in LANGS:
                    cc = {}
                    for c in CONC:
                        idx = rng.choice(cell[(L, c)], size=n, replace=False)
                        v = emb[idx].mean(0); cc[c] = v / (np.linalg.norm(v) + 1e-12)
                    M = np.array([[1 - float(cc[a] @ cc[b]) for b in CONC] for a in CONC])
                    p = rng.permutation(len(CONC))
                    rdp[L] = M[np.ix_(p, p)][iu]
                C = np.array([[spearman(rdp[a], rdp[b]) for b in LANGS] for a in LANGS])
                perm.append(C[lp].mean())
            obs_m = float(np.mean(obs)); perm = np.array(perm)
            pval = float((perm >= obs_m).mean())
            out[name] = (obs_m, pval)
        print(f"{n:>10}{out['LaBSE'][0]:>+11.3f}{out['LaBSE'][1]:>7.3f}"
              f"{out['OpenAI'][0]:>+12.3f}{out['OpenAI'][1]:>7.3f}")

    print("\nRead the target n as the smallest n where p<0.05 holds and iso stops climbing.")
    print("Corpus target: that n / per-concept prevalence = chunks/concept/tradition per cell.")


if __name__ == "__main__":
    main()
