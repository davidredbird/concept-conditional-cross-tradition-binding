"""
Phase 3a — RSA RE-CHECK after the Greek SUBSTRATE dict fix (dropped ὕλη=matter, added
κενό=void). Tags ON-THE-FLY via harmonized_concepts.tag() so the fix takes effect (the
chunks' baked-in option_a_concepts are stale for Greek SUBSTRATE). Firewall-safe (Phase 2c).

Question: does Greek SUBSTRATE fall into line (→ the outlier was the ὕλη artifact) or stay
idiosyncratic (→ Greek genuinely lacks the emptiness-SUBSTRATE concept, a real finding)?

Compares to BEFORE: 7-concept mean RDM-corr +0.363 LaBSE / +0.432 OpenAI; drop-SUBSTRATE
+0.460 / +0.541; SUBSTRATE std-across-langs 0.014 LaBSE / 0.035 OpenAI (most variable).

Usage: python scripts/phase3a_rsa_recheck.py
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
    openai = np.load(OPENAI_CACHE)
    return chunks, labse, openai


def rank(v):
    o = v.argsort(); r = np.empty_like(o, float); r[o] = np.arange(len(v)); return r


def spearman(a, b):
    return float(np.corrcoef(rank(a), rank(b))[0, 1])


def main():
    chunks, labse, openai = load()
    langs = sorted(set(c["language"] for c in chunks))
    # ON-THE-FLY tags (picks up the Greek SUBSTRATE fix)
    tagcache = [set(hc.tag(c["language"], c["text"])) for c in chunks]
    # Greek SUBSTRATE prevalence after the fix
    gi = [i for i, c in enumerate(chunks) if c["language"] == "greek"]
    gsub = sum("SUBSTRATE" in tagcache[i] for i in gi)
    print(f"Greek SUBSTRATE after fix: {gsub}/{len(gi)} chunks tagged ({gsub/len(gi):.3f})")

    for name, emb in [("LaBSE", labse), ("OpenAI", openai)]:
        def cent(L, c):
            idx = [i for i, ch in enumerate(chunks) if ch["language"] == L and c in tagcache[i]]
            if len(idx) < MIN_N:
                return None
            v = emb[idx].mean(0); return v / (np.linalg.norm(v) + 1e-12)
        cents = {L: {c: cent(L, c) for c in CONCEPTS if cent(L, c) is not None} for L in langs}

        def iso(concepts):
            common = [c for c in concepts if all(c in cents[L] for L in langs)]
            K = len(common); iu = np.triu_indices(K, 1)
            rd = {L: np.array([[1 - float(cents[L][a] @ cents[L][b]) for b in common] for a in common])[iu] for L in langs}
            C = np.array([[spearman(rd[a], rd[b]) for b in langs] for a in langs])
            return C[np.triu_indices(len(langs), 1)].mean(), common

        full, common = iso(CONCEPTS)
        nosub, _ = iso([c for c in CONCEPTS if c != "SUBSTRATE"])
        print(f"\n=== {name} (common={common}) ===")
        print(f"  7-concept mean RDM-corr = {full:+.3f}   (before fix: {'+0.363' if name=='LaBSE' else '+0.432'})")
        print(f"  drop-SUBSTRATE          = {nosub:+.3f}   (before fix: {'+0.460' if name=='LaBSE' else '+0.541'})")
        print(f"  -> SUBSTRATE {'still DRAGS (drop raises iso)' if nosub > full + 0.01 else 'now NEUTRAL/HELPS'}")
        # per-concept stability (std of mean-dissim across languages)
        K = len(common)
        rows = {c: [] for c in common}
        for L in langs:
            M = {a: {b: 1 - float(cents[L][a] @ cents[L][b]) for b in common} for a in common}
            for c in common:
                rows[c].append(sum(M[c][b] for b in common if b != c) / (K - 1))
        print("  per-concept stability (std across langs; lower=more stable):")
        for c in common:
            flag = "  <- SUBSTRATE" if c == "SUBSTRATE" else ""
            print(f"    {c:11s} std={np.std(rows[c]):.3f}{flag}")


if __name__ == "__main__":
    main()
