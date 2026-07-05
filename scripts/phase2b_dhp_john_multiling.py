"""
Phase 2b scaling — Dhammapada × Gospel-of-John gradient across languages via
VERSE-TAG PROJECTION. Both texts are verse-aligned across languages, so we tag the
ENGLISH verses once (broad English dict) and project each tag to every language by
verse-group index — no per-language dictionary needed.

Sources (all raw, no rate-limited API):
  Dhammapada: SuttaCentral bilara-data (branch 'published'), 26 files/language.
  John: christos-c/bible-corpus (b.JOH.C.V segs).

Languages with a COMPLETE bilara Dhammapada + a bible-corpus Bible + LaBSE
resolution: en, de (German!), vi (Vietnamese). (et/ka also have the Dhammapada
but lower-resource; add later.)

Usage: python scripts/phase2b_dhp_john_multiling.py
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
from english_gate_prep import ENGLISH_OPTION_A  # broad dict  # noqa: E402

RANGES = json.loads((REPO_ROOT / "corpus" / "_dhp_ranges.json").read_text())
LANGS = {  # display: (bilara_lang, dhp_author, bible_corpus_file)
    "english": ("en", "sujato", "English"),
    "german": ("de", "sabbamitta", "German"),
    "vietnamese": ("vi", "phantuananh", "Vietnamese"),
    "estonian": ("et", "thitanana", "Estonian"),
    "georgian": ("ka", "luka", "Georgian"),
}
GROUP = 8  # verses per aligned chunk
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


def fetch_dhp(lang, author):
    """-> ordered list of (verse_id, text)."""
    verses = {}
    for rng in RANGES:
        u = f"https://raw.githubusercontent.com/suttacentral/bilara-data/published/translation/{lang}/{author}/sutta/kn/dhp/{rng}_translation-{lang}-{author}.json"
        r = get(u)
        if not r:
            continue
        for seg, txt in json.loads(r).items():
            if not txt.strip():
                continue
            vid = seg.rsplit(".", 1)[0]  # aggregate sub-segments to verse
            verses[vid] = verses.get(vid, "") + " " + txt.strip()
    ordered = sorted(verses.items(), key=lambda kv: [int(x) for x in re.findall(r"\d+", kv[0])])
    return ordered


def fetch_john(bible_file):
    r = get(f"https://raw.githubusercontent.com/christos-c/bible-corpus/master/bibles/{bible_file}.xml")
    if not r:
        return []
    out = {}
    for vid, txt in re.findall(r'<seg id="(b\.JOH\.\d+\.\d+)"[^>]*>(.*?)</seg>', r, re.DOTALL):
        t = " ".join(re.sub(r"<[^>]+>", " ", html.unescape(txt)).split())
        if t:
            out[vid] = t
    return sorted(out.items(), key=lambda kv: [int(x) for x in re.findall(r"\d+", kv[0])])


def chunk_aligned(ordered):
    """Group consecutive verses into GROUP-sized aligned chunks -> list of (idx, text)."""
    return [(i // GROUP, " ".join(t for _, t in ordered[i:i + GROUP])) for i in range(0, len(ordered), GROUP)]


def ccb(sim, has_c, mask):
    both = has_c[:, None] & has_c[None, :] & mask
    only = (has_c[:, None] ^ has_c[None, :]) & mask
    nb, no = int(both.sum()), int(only.sum())
    if nb == 0 or no == 0:
        return float("nan"), nb
    return float((sim * both).sum() / nb - (sim * only).sum() / no), nb


def main():
    from multilingual_embedder import MultilingualEmbedder
    emb_model = MultilingualEmbedder("sentence-transformers/LaBSE")

    # English reference tags by chunk index
    en_dhp = chunk_aligned(fetch_dhp("en", "sujato"))
    en_john = chunk_aligned(fetch_john("English"))
    dhp_tags = {idx: tag_en(t) for idx, t in en_dhp}
    john_tags = {idx: tag_en(t) for idx, t in en_john}
    print(f"English reference: {len(en_dhp)} dhp chunks, {len(en_john)} john chunks")

    results = {}
    for disp, (lang, author, bfile) in LANGS.items():
        dhp = chunk_aligned(fetch_dhp(lang, author))
        john = chunk_aligned(fetch_john(bfile))
        if not dhp or not john:
            print(f"  {disp}: missing source, skip"); continue
        recs = ([{"text": t, "trad": "buddhist", "tags": dhp_tags.get(i, [])} for i, t in dhp]
                + [{"text": t, "trad": "christian", "tags": john_tags.get(i, [])} for i, t in john])
        vecs = emb_model.encode([r["text"] for r in recs], batch_size=32)
        vecs = vecs / (np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-12)
        sim = vecs @ vecs.T
        trad = np.array([r["trad"] for r in recs]); n = len(recs)
        up = np.triu(np.ones((n, n), bool), 1); cross = (trad[:, None] != trad[None, :]) & up
        rng = np.random.default_rng(0); row = {}
        for concept in ["AWARENESS", "SUBSTRATE", "ULTIMATE", "WORLD", "RECOGNITION"]:
            has = np.array([concept in r["tags"] for r in recs])
            obs, nb = ccb(sim, has, cross)
            if np.isnan(obs):
                row[concept] = ("nan", 1.0); continue
            diffs = [ccb(sim, _m, cross)[0] for _m in
                     (np.isin(np.arange(n), rng.permutation(n)[:int(has.sum())]) for _ in range(800))]
            diffs = np.asarray([d for d in diffs if not np.isnan(d)])
            row[concept] = (round(obs, 4), round(float((diffs >= obs).mean()), 4))
        results[disp] = row
        print(f"  {disp} ({lang}): dhp {len(dhp)} + john {len(john)} chunks | " +
              " ".join(f"{c}={row[c][0]}(p={row[c][1]})" for c in row))
    (REPO_ROOT / "results" / "phase2b" / "dhp_john_multiling.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("\nwrote results/phase2b/dhp_john_multiling.json")


if __name__ == "__main__":
    main()
