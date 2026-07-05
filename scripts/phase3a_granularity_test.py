"""
Phase 3a — MODEL GRANULARITY / DISCRIMINATION test (firewall-safe; Phase 2c exploratory
data, NOT the sealed Plato/Aristotle gradient). Methods check, NOT a Phase 3a result.

Question (from the OpenAI-binds-everything finding): is the cross-lingual concept signal
DISCRIMINATING or does the model just align all topics? Tag the Phase 2c originals with
CONTROL concepts (governance, eating, drinking, warfare — should NOT structurally converge)
alongside SUBSTRATE/AWARENESS, and compare cross-language CCB on LaBSE vs OpenAI.

Control dicts cover en/gr/zh, and Phase 2c is non-English, so the clean control comparison
is Chinese↔Greek (classical Chinese Daoist/Chan + Confucian × Greek Neoplatonist/Christian —
Phase 2c mystical originals, e.g. Plotinus/TTC; NOT Plato/Aristotle). SUBSTRATE is included
only as a should-converge reference; its value here is NOT interpreted as a Phase 3a finding.

Prediction (granularity hypothesis): OpenAI binds governance ≈ the spiritual concepts (no
discrimination → over-aligned/coarse); LaBSE holds the controls lower than SUBSTRATE
(structural discrimination). Uses cached embeddings only.
Usage: python scripts/phase3a_granularity_test.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")
import control_concepts as cc  # noqa: E402

SLUG = "sentence_transformers__LaBSE"
ORIGINALS = ["chinese_taote_chinese", "chinese_zhuangzi_chinese", "chinese_platform_sutra_chinese",
             "chinese_analects_chinese", "arabic_fusus_arabic", "arabic_najat_arabic",
             "greek_plotinus_greek", "greek_clement_greek", "hindi_kabir_hindi",
             "hindi_tulsidas_hindi", "hindi_surdas_hindi", "spanish_molinos_spanish",
             "spanish_teresa_spanish", "hebrew_nachman_hebrew"]
OPENAI_CACHE = REPO / "results" / "phase3a" / "originals_openai_te3l.npy"
SPIRITUAL = ["SUBSTRATE", "AWARENESS"]
CONTROLS = ["GOVERNANCE", "EATING", "DRINKING", "WARFARE"]


def load():
    chunks, labse = [], []
    for stem in ORIGINALS:
        cf = REPO / "corpus" / f"chunks_{stem}.jsonl"
        nf = REPO / "results" / "phase2a" / f"{stem}_{SLUG}.npy"
        cs = [json.loads(l) for l in cf.read_text(encoding="utf-8").splitlines() if l.strip()]
        e = np.load(nf)
        assert e.shape[0] == len(cs), f"misalign {stem}"
        chunks += cs; labse.append(e)
    labse = np.vstack(labse)
    labse = labse / (np.linalg.norm(labse, axis=1, keepdims=True) + 1e-12)
    openai = np.load(OPENAI_CACHE)
    assert openai.shape[0] == len(chunks), f"openai cache misalign {openai.shape[0]} vs {len(chunks)}"
    return chunks, labse, openai


def ccb(sim, has, mask):
    both = has[:, None] & has[None, :] & mask
    one = (has[:, None] ^ has[None, :]) & mask
    nb, no = int(both.sum()), int(one.sum())
    if nb == 0 or no == 0:
        return float("nan"), nb
    return float((sim * both).sum() / nb - (sim * one).sum() / no), nb


def main():
    chunks, labse, openai = load()
    lang = np.array([c["language"] for c in chunks])
    # restrict to the control-dict-covered, 3a-relevant pair: classical_chinese ↔ greek
    keep = np.isin(lang, ["classical_chinese", "greek"])
    idx = np.where(keep)[0]
    chunks = [chunks[i] for i in idx]
    lang = lang[idx]
    labse = labse[idx]; openai = openai[idx]
    n = len(chunks)
    print(f"Chinese↔Greek subset of Phase 2c originals: {n} chunks "
          f"({int((lang=='classical_chinese').sum())} zh, {int((lang=='greek').sum())} gr)")

    # tags
    tags = {}
    for c in SPIRITUAL:
        tags[c] = np.array([c in (ch.get("option_a_concepts") or []) for ch in chunks])
    for c in CONTROLS:
        tags[c] = np.array([c in cc.tag(ch["language"], ch["text"]) for ch in chunks])
    print("tag counts (zh / gr):")
    for c in SPIRITUAL + CONTROLS:
        zc = int(tags[c][lang == "classical_chinese"].sum()); gc = int(tags[c][lang == "greek"].sum())
        print(f"  {c:11s} zh={zc:4d}  gr={gc:4d}")

    up = np.triu(np.ones((n, n), bool), 1)
    cross = (lang[:, None] != lang[None, :]) & up  # chinese × greek
    rng = np.random.default_rng(0)

    for name, emb in [("LaBSE", labse), ("OpenAI te3-large", openai)]:
        sim = emb @ emb.T
        print(f"\n=== {name}: Chinese↔Greek cross-language CCB ===")
        for c in SPIRITUAL + CONTROLS:
            has = tags[c]; nw = int(has.sum())
            obs, nb = ccb(sim, has, cross)
            if np.isnan(obs):
                print(f"  {c:11s} na (n_both=0)"); continue
            diffs = []
            for _ in range(500):
                m = np.zeros(n, bool); m[rng.permutation(n)[:nw]] = True
                d, _ = ccb(sim, m, cross)
                if not np.isnan(d):
                    diffs.append(d)
            p = float((np.array(diffs) >= obs).mean())
            tag = "  <- CONTROL" if c in CONTROLS else ""
            print(f"  {c:11s} CCB={obs:+.4f}  p={p:.4f}  n_both={nb}{tag}")
    print("\nGranularity read: if OpenAI binds GOVERNANCE/WARFARE ≈ SUBSTRATE it lacks "
          "discrimination (over-aligned); if LaBSE holds controls below SUBSTRATE it "
          "discriminates structurally. (SUBSTRATE value is a methods reference, not a 3a result.)")


if __name__ == "__main__":
    main()
