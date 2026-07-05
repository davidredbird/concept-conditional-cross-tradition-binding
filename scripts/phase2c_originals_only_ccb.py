"""
Phase 2c — ORIGINALS-ONLY convergence. Only texts in their original composition
language are allowed, so NO translation effect can appear in the results. Tests
cross-tradition concept convergence across languages (cross-language pairs) and is
designed to be re-run within-language too.

Excluded as translations: faju (Chinese Dharmapada, tr. from Indic), Maimonides
Guide (Hebrew = Ibn Tibbon tr. from Judeo-Arabic), all French/English/Japanese
corpora (translations/renderings of non-native traditions).

Included originals (LaBSE-gate-passing, composed in-language):
  ZH: Tao Te Ching (Daoist), Platform Sutra (Chan)
  AR: Fuṣūṣ al-Ḥikam (Sufi), al-Najāt (Falsafa)
  EL: Plotinus Enneads (Neoplatonism), Clement Stromateis (Christian)
  HI: Kabir (Sant), Tulsidas (Bhakti)
  ES: Molinos (Quietist), Teresa (Carmelite)
  HE: Likutei Moharan (Hasidic)

Caveats it does NOT remove: native shared-lineage vocabulary; the LaBSE
cross-lingual ALIGNMENT objective (for the cross-language pairs).

Usage:
  python scripts/phase2c_originals_only_ccb.py
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
ORIGINALS = [
    # Chinese originals — Daoist side BULKED with Zhuangzi (the small-TTC artifact fix);
    # Analects added as an original Confucian text.
    "chinese_taote_chinese", "chinese_zhuangzi_chinese", "chinese_platform_sutra_chinese",
    "chinese_analects_chinese",
    "arabic_fusus_arabic", "arabic_najat_arabic",
    "greek_plotinus_greek", "greek_clement_greek",
    "hindi_kabir_hindi", "hindi_tulsidas_hindi", "hindi_surdas_hindi",
    "spanish_molinos_spanish", "spanish_teresa_spanish",
    "hebrew_nachman_hebrew",
]
CAP = 300


def ccb(sim, has_c, mask):
    both = has_c[:, None] & has_c[None, :] & mask
    only = (has_c[:, None] ^ has_c[None, :]) & mask
    nb, no = int(both.sum()), int(only.sum())
    if nb == 0 or no == 0:
        return float("nan"), nb, no
    return float((sim * both).sum() / nb - (sim * only).sum() / no), nb, no


def run(mask_kind: str, chunks, emb, lang):
    n = len(chunks)
    up = np.triu(np.ones((n, n), dtype=bool), k=1)
    if mask_kind == "cross":
        mask = (lang[:, None] != lang[None, :]) & up
    else:  # within-language, cross-tradition
        trad = np.array([c["tradition"] for c in chunks])
        mask = (lang[:, None] == lang[None, :]) & (trad[:, None] != trad[None, :]) & up
    sim = emb @ emb.T
    rng = np.random.default_rng(0)
    print(f"\n=== {mask_kind}-language pairs (originals only): {int(mask.sum()):,} ===")
    print(f"{'concept':<14}{'n_with':>7}{'n_both':>9}{'CCB':>10}{'p':>8}")
    for concept in CONCEPT_PATTERNS:
        has_c = np.array([concept in (c.get("option_a_concepts") or []) for c in chunks])
        obs, nb, no = ccb(sim, has_c, mask)
        if np.isnan(obs):
            print(f"{concept:<14}{int(has_c.sum()):>7}{nb:>9}{'nan':>10}"); continue
        diffs = []
        for _ in range(800):
            m = np.zeros(n, dtype=bool); m[rng.permutation(n)[:int(has_c.sum())]] = True
            d, _, _ = ccb(sim, m, mask)
            if not np.isnan(d):
                diffs.append(d)
        p = float((np.asarray(diffs) >= obs).mean())
        print(f"{concept:<14}{int(has_c.sum()):>7}{nb:>9}{obs:>+10.4f}{p:>8.4f}")


def main() -> None:
    chunks, embs = [], []
    cap_rng = np.random.default_rng(0)
    present = {}
    for stem in ORIGINALS:
        cf = REPO_ROOT / "corpus" / f"chunks_{stem}.jsonl"
        nf = REPO_ROOT / "results" / "phase2a" / f"{stem}_{SLUG}.npy"
        if not (cf.exists() and nf.exists()):
            print(f"  skip {stem}"); continue
        cs = [json.loads(l) for l in cf.read_text(encoding="utf-8").splitlines() if l.strip()]
        e = np.load(nf)
        if len(cs) > CAP:
            idx = np.sort(cap_rng.permutation(len(cs))[:CAP]); cs = [cs[i] for i in idx]; e = e[idx]
        chunks += cs; embs.append(e)
        present[cs[0]["language"]] = present.get(cs[0]["language"], 0) + len(cs)
    emb = np.vstack(embs); emb = emb / (np.linalg.norm(emb, axis=1, keepdims=True) + 1e-12)
    lang = np.array([c["language"] for c in chunks])
    print(f"Pooled {len(chunks)} ORIGINAL-language chunks: {present}")
    run("cross", chunks, emb, lang)
    run("within", chunks, emb, lang)


if __name__ == "__main__":
    main()
