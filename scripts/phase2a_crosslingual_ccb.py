"""
Cross-LINGUAL cross-tradition CCB. Pools every LaBSE-embedded Phase 2a corpus
into the one shared LaBSE space and tests whether concept-C passages converge
across LANGUAGE boundaries (not just tradition).

CCB(C) = mean_cos(both-tagged C, CROSS-LANGUAGE pairs)
       - mean_cos(one-tagged C, CROSS-LANGUAGE pairs)

Restricting to cross-language pairs cancels the language-clustering baseline
(same-language pairs are systematically more similar) in the both−one contrast.
Permutation null shuffles the concept tag across all pooled chunks.

MAJOR CAVEAT: each language was tagged by its OWN Option-A dictionary, so
"both tagged C" cross-language means two independently-built dictionaries fired.
Tag harmonization across languages is imperfect; results are EXPLORATORY.

Usage:
  python scripts/phase2a_crosslingual_ccb.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")
from concept_analysis import CONCEPT_PATTERNS  # noqa: E402

SLUG = "sentence_transformers__LaBSE"
# per-book corpora (chunk-file stem); npy derived as results/phase2a/{stem}_{SLUG}.npy
CORPORA = [
    # Chinese + Japanese + Hindi BULKED with the corpus-expansion texts
    "chinese_faju_jing_chinese", "chinese_platform_sutra_chinese", "chinese_taote_chinese",
    "chinese_zhuangzi_chinese", "chinese_analects_chinese",
    "french_taote_french", "french_gita_french", "french_jeandelacroix_french",
    "arabic_fusus_arabic", "arabic_najat_arabic",
    "hindi_kabir_hindi", "hindi_tulsidas_hindi", "hindi_surdas_hindi",
    "japanese_tannisho_japanese", "japanese_chuyo_japanese",
    "japanese_rennyo_japanese", "japanese_shoshinge_japanese",
    "japanese_daigaku_japanese", "japanese_rongo_japanese",
    "hebrew_nachman_hebrew", "hebrew_maimonides_hebrew",
    "spanish_molinos_spanish", "spanish_teresa_spanish",
    "greek_plotinus_greek", "greek_clement_greek",
    "english_dhammapada_radhakrishnan", "english_taote_legge",
]


def ccb(sim, has_c, mask):
    both = has_c[:, None] & has_c[None, :] & mask
    only = (has_c[:, None] ^ has_c[None, :]) & mask
    nb, no = int(both.sum()), int(only.sum())
    if nb == 0 or no == 0:
        return float("nan"), nb, no
    return float((sim * both).sum() / nb - (sim * only).sum() / no), nb, no


CAP = 300  # per-book cap so big corpora (Plotinus) don't dominate cross-language pairs


def main() -> None:
    chunks, embs = [], []
    langs_present = {}
    capper = np.random.default_rng(0)
    for stem in CORPORA:
        cf = REPO_ROOT / "corpus" / f"chunks_{stem}.jsonl"
        nf = REPO_ROOT / "results" / "phase2a" / f"{stem}_{SLUG}.npy"
        if not cf.exists() or not nf.exists():
            print(f"  skip {stem} (missing)")
            continue
        cs = [json.loads(l) for l in cf.read_text(encoding="utf-8").splitlines() if l.strip()]
        e = np.load(nf)
        if e.shape[0] != len(cs):
            print(f"  skip {stem} (misalign {len(cs)} vs {e.shape[0]})")
            continue
        if len(cs) > CAP:
            idx = np.sort(capper.permutation(len(cs))[:CAP])
            cs = [cs[i] for i in idx]; e = e[idx]
        chunks += cs
        embs.append(e)
        langs_present[cs[0]["language"]] = langs_present.get(cs[0]["language"], 0) + len(cs)
    emb = np.vstack(embs)
    emb = emb / (np.linalg.norm(emb, axis=1, keepdims=True) + 1e-12)
    n = len(chunks)
    print(f"\nPooled {n} chunks across {len(langs_present)} languages: {langs_present}")

    lang = np.array([c["language"] for c in chunks])
    up = np.triu(np.ones((n, n), dtype=bool), k=1)
    cross_lang = (lang[:, None] != lang[None, :]) & up
    print(f"Cross-language pairs: {int(cross_lang.sum()):,}")

    sim = emb @ emb.T
    rng = np.random.default_rng(0)
    n_perm = 1000
    print(f"\n{'concept':<14}{'n_with':>7}{'n_both':>10}{'CCB':>10}{'null_mn':>10}{'p':>8}")
    print("-" * 60)
    for concept in CONCEPT_PATTERNS:
        has_c = np.array([concept in (c.get("option_a_concepts") or []) for c in chunks])
        nw = int(has_c.sum())
        obs, nb, no = ccb(sim, has_c, cross_lang)
        if np.isnan(obs) or nb == 0 or no == 0:
            print(f"{concept:<14}{nw:>7}{nb:>10}{'nan':>10}")
            continue
        diffs = []
        for _ in range(n_perm):
            m = np.zeros(n, dtype=bool); m[rng.permutation(n)[:nw]] = True
            d, _, _ = ccb(sim, m, cross_lang)
            if not np.isnan(d):
                diffs.append(d)
        diffs = np.asarray(diffs)
        p = float((diffs >= obs).mean())
        print(f"{concept:<14}{nw:>7}{nb:>10}{obs:>+10.4f}{diffs.mean():>+10.4f}{p:>8.4f}")


if __name__ == "__main__":
    main()
