"""
Phase 2b maximal-language expansion — Bible (Gospel of John, Christian) × Quran
(subset, Islamic) cross-tradition CCB across many languages, via verse-tag
projection. Both texts are verse-aligned across all their translations, so tag the
ENGLISH verses once and project by verse-chunk index to every language. No
per-language dictionary.

Sources (both raw/CDN, no rate-limited API):
  Bible: christos-c/bible-corpus (b.JOH.C.V).
  Quran: fawazahmed0/quran-api (CDN; 98 languages; sura:ayah aligned).

Concept caveat: both are Abrahamic scripture, so SUBSTRATE/NONSEP (emptiness/
non-duality) barely tag; this pair informs ULTIMATE / AWARENESS / WORLD across
many languages, not SUBSTRATE. EXPLORATORY data-gathering (expansion).

Usage: python scripts/phase2b_bible_quran_multiling.py
"""

from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")
from concept_analysis import CONCEPT_PATTERNS  # noqa: E402
from english_gate_prep import ENGLISH_OPTION_A  # noqa: E402

# display -> (bible-corpus file, quran-api language name)
LANGS = {
    "english": ("English", "English"), "french": ("French", "French"),
    "german": ("German", "German"), "spanish": ("Spanish", "Spanish"),
    "russian": ("Russian", "Russian"), "italian": ("Italian", "Italian"),
    "dutch": ("Dutch", "Dutch"), "turkish": ("Turkish", "Turkish"),
    "indonesian": ("Indonesian", "Indonesian"), "chinese": ("Chinese", "Chinese(simplified)"),
    "arabic": ("Arabic", "Arabic"), "portuguese": ("Portuguese-NT", "Portuguese"),
}
GROUP = 8
QURAN_VERSES = 880  # first N Quran verses (sura:ayah order) ~ matches John length
UA = {"User-Agent": "CCB-Research/0.1 (research)"}


def get(url):
    for a in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode("utf-8", errors="replace")
        except Exception:
            if a == 3:
                return None
            time.sleep(2)


def tag_en(text):
    return [c for c, pats in ENGLISH_OPTION_A.items() if any(re.search(p, text, re.IGNORECASE) for p in pats)]


def john(bible_file):
    r = get(f"https://raw.githubusercontent.com/christos-c/bible-corpus/master/bibles/{bible_file}.xml")
    if not r:
        return []
    out = {}
    for vid, txt in re.findall(r'<seg id="(b\.JOH\.\d+\.\d+)"[^>]*>(.*?)</seg>', r, re.DOTALL):
        t = " ".join(re.sub(r"<[^>]+>", " ", html.unescape(txt)).split())
        if t:
            out[vid] = t
    return sorted(out.items(), key=lambda kv: [int(x) for x in re.findall(r"\d+", kv[0])])


def quran(edition_name):
    r = get(f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{edition_name}.json")
    if not r:
        return []
    try:
        items = json.loads(r).get("quran", [])
    except Exception:
        return []
    rows = sorted(((int(it["chapter"]), int(it["verse"]), it["text"]) for it in items), key=lambda x: (x[0], x[1]))
    return [(f"q.{c}.{v}", t) for c, v, t in rows[:QURAN_VERSES]]


def chunk_aligned(ordered):
    return [(i // GROUP, " ".join(t for _, t in ordered[i:i + GROUP])) for i in range(0, len(ordered), GROUP)]


def ccb(sim, has_c, mask):
    both = has_c[:, None] & has_c[None, :] & mask
    only = (has_c[:, None] ^ has_c[None, :]) & mask
    nb, no = int(both.sum()), int(only.sum())
    if nb == 0 or no == 0:
        return float("nan"), nb
    return float((sim * both).sum() / nb - (sim * only).sum() / no), nb


def edition_map():
    eds = json.loads(get("https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions.json"))
    m = {}
    for v in eds.values():
        if isinstance(v, dict):
            m.setdefault(v.get("language"), v.get("name"))
    return m


def main():
    from multilingual_embedder import MultilingualEmbedder
    em = MultilingualEmbedder("sentence-transformers/LaBSE")
    edmap = edition_map()

    en_b = chunk_aligned(john("English")); en_q = chunk_aligned(quran(edmap["English"]))
    b_tags = {i: tag_en(t) for i, t in en_b}; q_tags = {i: tag_en(t) for i, t in en_q}
    print(f"reference: {len(en_b)} john chunks, {len(en_q)} quran chunks")

    results = {}
    for disp, (bfile, qlang) in LANGS.items():
        edition = edmap.get(qlang)
        if not edition:
            print(f"  {disp}: no quran edition for '{qlang}'"); continue
        b = chunk_aligned(john(bfile)); q = chunk_aligned(quran(edition))
        if not b or not q:
            print(f"  {disp}: missing (john={len(b)} quran={len(q)})"); continue
        recs = ([{"text": t, "trad": "christian", "tags": b_tags.get(i, [])} for i, t in b]
                + [{"text": t, "trad": "islamic", "tags": q_tags.get(i, [])} for i, t in q])
        v = em.encode([r["text"] for r in recs], batch_size=32)
        v = v / (np.linalg.norm(v, axis=1, keepdims=True) + 1e-12)
        sim = v @ v.T
        trad = np.array([r["trad"] for r in recs]); n = len(recs)
        up = np.triu(np.ones((n, n), bool), 1); cross = (trad[:, None] != trad[None, :]) & up
        rng = np.random.default_rng(0); row = {}
        for c in ["AWARENESS", "ULTIMATE", "WORLD", "SELF", "SUBSTRATE"]:
            has = np.array([c in r["tags"] for r in recs])
            obs, nb = ccb(sim, has, cross)
            if np.isnan(obs):
                row[c] = (None, None); continue
            diffs = np.asarray([d for d in (ccb(sim, np.isin(np.arange(n), rng.permutation(n)[:int(has.sum())]), cross)[0] for _ in range(600)) if not np.isnan(d)])
            row[c] = (round(obs, 4), round(float((diffs >= obs).mean()), 4))
        results[disp] = row
        print(f"  {disp}: " + "  ".join(f"{c}={row[c][0]}(p={row[c][1]})" for c in row))
    (REPO_ROOT / "results" / "phase2b" / "bible_quran_multiling.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nwrote results/phase2b/bible_quran_multiling.json ({len(results)} languages)")


if __name__ == "__main__":
    main()
