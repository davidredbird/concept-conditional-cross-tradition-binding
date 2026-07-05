"""
Phase 3a POWER ANALYSIS (firewall-safe — pre-reg gating).

Question: at the realistic cross-language SUBSTRATE effect size (Phase 2c Δ≈0.006),
is the China×Greece cross-sphere test adequately powered — pooled and per era-cell?

Method:
  1. Calibrate the CCB sampling SE from the EXISTING Phase 2c LaBSE result: recompute
     the cross-language SUBSTRATE CCB + permutation null → (Δ_obs, σ_null, n_both0).
     The permutation null already captures pair-dependence, so σ_null is the right SE.
  2. Scale σ(n_both) = σ_null0 · sqrt(n_both0 / n_both)  (mean-of-pairs variance ∝ 1/n_both).
  3. Power(Δ, n_both) = Φ( Δ/σ(n_both) − z_0.05 ), one-sided.
  4. Project China×Greek n_both = (N_zh·p) · (N_gr·p) from gradient-corpus CHAR COUNTS
     (metadata only — never embeds/tags the sealed corpus) over a SUBSTRATE-prevalence
     range (measured on the safe Phase 2c originals as a proxy; sealed-corpus prevalence
     is confirmed post-pre-reg by the coverage screen).

Uses Phase 2c safe embeddings + gradient META char_counts only.
Usage: python scripts/phase3a_power_analysis.py
"""

from __future__ import annotations

import json
import math
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
NORM = {"john": 0.0}  # placeholder; not used


def load_originals():
    chunks, embs = [], []
    for stem in ORIGINALS:
        cf = REPO / "corpus" / f"chunks_{stem}.jsonl"
        nf = REPO / "results" / "phase2a" / f"{stem}_{SLUG}.npy"
        if not cf.exists() or not nf.exists():
            print(f"  skip {stem} (missing)"); continue
        cs = [json.loads(l) for l in cf.read_text(encoding="utf-8").splitlines() if l.strip()]
        e = np.load(nf)
        if e.shape[0] != len(cs):
            print(f"  skip {stem} (misalign)"); continue
        chunks += cs; embs.append(e)
    emb = np.vstack(embs)
    emb = emb / (np.linalg.norm(emb, axis=1, keepdims=True) + 1e-12)
    return chunks, emb


def ccb(sim, has, mask):
    both = has[:, None] & has[None, :] & mask
    one = (has[:, None] ^ has[None, :]) & mask
    nb, no = int(both.sum()), int(one.sum())
    if nb == 0 or no == 0:
        return float("nan"), nb, no
    return float((sim * both).sum() / nb - (sim * one).sum() / no), nb, no


def Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def main():
    chunks, emb = load_originals()
    n = len(chunks)
    lang = np.array([c["language"] for c in chunks])
    has = np.array(["SUBSTRATE" in (c.get("option_a_concepts") or []) for c in chunks])
    print(f"Phase 2c originals: {n} chunks; SUBSTRATE-tagged {int(has.sum())} ({has.mean():.3f})")

    # per-language SUBSTRATE prevalence (proxy for projection range)
    print("\nSUBSTRATE prevalence by language (proxy for sealed-corpus range):")
    for L in sorted(set(lang)):
        m = lang == L
        print(f"  {L:18s} n={int(m.sum()):4d}  prev={has[m].mean():.3f}")

    # calibrate σ_null on the cross-language SUBSTRATE CCB
    up = np.triu(np.ones((n, n), bool), 1)
    cross = (lang[:, None] != lang[None, :]) & up
    sim = emb @ emb.T
    obs, nb0, no0 = ccb(sim, has, cross)
    rng = np.random.default_rng(0)
    nw = int(has.sum())
    diffs = []
    for _ in range(1000):
        m = np.zeros(n, bool); m[rng.permutation(n)[:nw]] = True
        d, _, _ = ccb(sim, m, cross)
        if not np.isnan(d):
            diffs.append(d)
    diffs = np.array(diffs)
    sig0 = diffs.std()
    p = float((diffs >= obs).mean())
    z0 = obs / sig0
    print(f"\nCALIBRATION (Phase 2c cross-language SUBSTRATE):")
    print(f"  Δ_obs={obs:+.4f}  σ_null={sig0:.4f}  n_both0={nb0}  z={z0:.2f}  p={p:.4f}")

    Z05 = 1.645
    def power(delta, nb):
        sig = sig0 * math.sqrt(nb0 / max(nb, 1))
        return Phi(delta / sig - Z05)
    def needed_nb(delta, target=0.80):
        # solve Φ(δ/σ(nb) − z)=target → δ/σ = z + Φ^{-1}(target); Φ^{-1}(.8)=0.8416
        zt = Z05 + 0.8416
        sig_req = delta / zt
        return nb0 * (sig0 / sig_req) ** 2

    print(f"\nNeeded both-tagged-pair count n_both for 80% power (one-sided α=.05):")
    for d in (0.003, 0.006, 0.010):
        print(f"  Δ={d:.3f}:  n_both ≈ {needed_nb(d):,.0f}")

    # --- project China×Greek n_both from gradient META char_counts (metadata only) ---
    CHUNK_CHARS = {"greek": 600, "chinese": 250}  # gate-prep chunk targets
    cells = {}  # (sphere, era_bucket, category) -> total chars
    md = REPO / "corpus" / "books" / "cleaned"
    for mf in md.glob("*.meta.json"):
        m = json.loads(mf.read_text(encoding="utf-8"))
        sph = m.get("sphere")
        if sph not in ("greek", "chinese"):
            continue
        cc = (m.get("_clean") or {}).get("char_count", 0)
        key = (sph, m.get("contact_level", "?"), m.get("category", "?"))
        cells[key] = cells.get(key, 0) + cc

    def chunks_for(sphere, chars):
        return chars / CHUNK_CHARS[sphere]

    # total NONDUAL chunks per sphere (SUBSTRATE lives in nondual cells primarily)
    zh_nd = sum(chunks_for("chinese", c) for (s, _, cat), c in cells.items() if s == "chinese" and cat == "nondual")
    gr_nd = sum(chunks_for("greek", c) for (s, _, cat), c in cells.items() if s == "greek" and cat == "nondual")
    print(f"\nGradient corpus (META-derived chunk estimate, nondual cells):")
    print(f"  Chinese nondual ≈ {zh_nd:,.0f} chunks   Greek nondual ≈ {gr_nd:,.0f} chunks")

    print(f"\nPROJECTED China×Greek cross-sphere SUBSTRATE n_both and power(Δ=0.006):")
    print(f"  (pooled nondual; n_both = N_zh·p · N_gr·p)")
    print(f"  {'prevalence':>10}{'n_both':>10}{'power(.006)':>13}{'power(.003)':>13}")
    for pv in (0.02, 0.05, 0.10, 0.15):
        nb = (zh_nd * pv) * (gr_nd * pv)
        print(f"  {pv:>10.2f}{nb:>10,.0f}{power(0.006, nb):>13.2f}{power(0.003, nb):>13.2f}")

    # per-cell (single era × sphere) — the diff-in-diff unit; use the SMALLEST plausible era-cell
    print(f"\nPER-CELL caution (one era × sphere is much smaller than pooled):")
    for (s, era, cat), c in sorted(cells.items()):
        if cat == "nondual":
            print(f"  {s:8s} {era:14s} ≈ {chunks_for(s, c):6,.0f} chunks")
    print("\nInterpretation printed; see comments. Meta-analytic K-cell pooling improves the")
    print("intercept SE ~sqrt(K) but the heterogeneity (structural-vs-diffusion) test needs")
    print("adequate PER-CELL power first.")


if __name__ == "__main__":
    main()
