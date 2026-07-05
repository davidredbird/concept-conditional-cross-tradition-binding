"""
Phase 2d — embed + CCB the cached Bible × Quran corpus across all cached languages,
now SUBSTRATE-inclusive and HARMONIZED. This is the per-language reference BASELINE
other tests calibrate against (Δ_T = CCB_T − baseline).

Christian side : John (gospel) + Ecclesiastes (hevel/emptiness) + Genesis (tohu-
                 va-vohu / formless-void).
Islamic side   : Quran suras 50–114 (the contemplative/Meccan back-third — fanaʾ
                 'all perishes except His Face', al-ghayb, the Light material).
Tags           : harmonized_concepts.tag('english', ...) projected by (book, chunk
                 index) to every language. Includes SUBSTRATE (now testable).

Usage: python scripts/phase2b_bq_run_from_cache.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE = REPO_ROOT / "corpus" / "cache" / "bq"
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")
from harmonized_concepts import tag  # noqa: E402

GROUP = 8
CONCEPTS = ["SUBSTRATE", "AWARENESS", "ULTIMATE", "WORLD", "SELF", "RECOGNITION"]
BIBLE_BOOKS = ["john", "ecc", "gen"]


def vsort(d):
    return sorted(d.items(), key=lambda kv: [int(x) for x in re.findall(r"\d+", kv[0])])


def load(lang, name):
    p = CACHE / f"{lang}_{name}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def quran_meccan(lang):
    full = load(lang, "quran_full")
    return {k: v for k, v in full.items() if 50 <= int(k.split(".")[1]) <= 114}


def chunks(ordered):
    return [(i // GROUP, " ".join(t for _, t in ordered[i:i + GROUP])) for i in range(0, len(ordered), GROUP)]


def ccb(sim, has, mask):
    both = has[:, None] & has[None, :] & mask
    only = (has[:, None] ^ has[None, :]) & mask
    nb, no = int(both.sum()), int(only.sum())
    if nb == 0 or no == 0:
        return float("nan"), nb
    return float((sim * both).sum() / nb - (sim * only).sum() / no), nb


def en_tags():
    """English reference tags keyed by (side_book, chunk_idx)."""
    t = {}
    for bk in BIBLE_BOOKS:
        for i, txt in chunks(vsort(load("english", bk))):
            t[("c", bk, i)] = tag("english", txt)
    for i, txt in chunks(vsort(quran_meccan("english"))):
        t[("i", "quran", i)] = tag("english", txt)
    return t


def main():
    from multilingual_embedder import MultilingualEmbedder
    em = MultilingualEmbedder("sentence-transformers/LaBSE")
    REF = en_tags()
    langs = sorted({p.name[: -len("_john.json")] for p in CACHE.glob("*_john.json")
                    if (CACHE / (p.name[: -len("_john.json")] + "_quran_full.json")).exists()})
    print(f"{len(langs)} languages; SUBSTRATE-inclusive baseline\n")
    results = {}
    rng = np.random.default_rng(0)
    for lang in langs:
        recs = []
        for bk in BIBLE_BOOKS:
            for i, txt in chunks(vsort(load(lang, bk))):
                recs.append({"t": txt, "trad": "christian", "tags": REF.get(("c", bk, i), [])})
        for i, txt in chunks(vsort(quran_meccan(lang))):
            recs.append({"t": txt, "trad": "islamic", "tags": REF.get(("i", "quran", i), [])})
        if len(recs) < 60:
            print(f"  {lang:14s} skip (n={len(recs)})"); continue
        v = em.encode([r["t"] for r in recs], batch_size=64)
        v = v / (np.linalg.norm(v, axis=1, keepdims=True) + 1e-12)
        sim = v @ v.T
        trad = np.array([r["trad"] for r in recs]); n = len(recs)
        up = np.triu(np.ones((n, n), bool), 1); cross = (trad[:, None] != trad[None, :]) & up
        row = {}
        for c in CONCEPTS:
            has = np.array([c in r["tags"] for r in recs])
            obs, nb = ccb(sim, has, cross)
            if np.isnan(obs):
                row[c] = None; continue
            diffs = np.asarray([d for d in (ccb(sim, np.isin(np.arange(n), rng.permutation(n)[:int(has.sum())]), cross)[0] for _ in range(500)) if not np.isnan(d)])
            row[c] = [round(obs, 4), round(float((diffs >= obs).mean()), 4), int(nb)]
        results[lang] = row
        print(f"  {lang:13s} " + "  ".join(f"{c[:4]}={row[c][0] if row[c] else 'na'}" for c in CONCEPTS))
    (REPO_ROOT / "results" / "phase2b" / "bible_quran_baseline.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nwrote results/phase2b/bible_quran_baseline.json ({len(results)} languages)")


if __name__ == "__main__":
    main()
