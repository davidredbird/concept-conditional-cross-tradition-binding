"""
Phase 3a prep — REGISTER reliability + penalty for the languages 3a actually uses
(ancient Greek, classical Chinese), built on the new Greek/Chinese scripture cache.

Tags are projected from ENGLISH by VERSE ID (handles the LXX/Wenli versification
merges that would break chunk-index projection), so the concept assignment is held
IDENTICAL across registers and only the embedding varies.

Two deliverables:
  1. Within-Bible per-concept binding (the within-corpus gate metric) for each of
     {greekkoine, greekmodern, chineseclassical, chinese} on John+Gen+Ecc.
     -> ancient/classical vs modern REGISTER PENALTY per concept.
  2. Cross-tradition Bible×Quran profile (where a Quran exists: greekmodern, chinese)
     z-scored and correlated with the 40-language consensus profile
     -> modern-Greek reliability rank on the established profile-fit metric
        (chinese reproduces ~0.92 as a validation).

Scripture reference only (NOT the sealed China×Greece philosophical corpus).
Usage: python scripts/phase3a_register_reliability.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "corpus" / "cache" / "bq"
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")
from harmonized_concepts import tag  # noqa: E402

GROUP = 8
BOOKS = ["john", "gen", "ecc"]
CONCEPTS = ["SUBSTRATE", "AWARENESS", "ULTIMATE", "WORLD", "SELF"]


def load(lang, book):
    p = CACHE / f"{lang}_{book}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def vkey(k):
    return [int(x) for x in re.findall(r"\d+", k)]


# ---- English master verses + tags (the reference assignment, projected by verse id) ----
EN_BIBLE = {b: load("english", b) for b in BOOKS}
EN_QURAN = load("english", "quran_full")
EN_TAGS = {}
for b in BOOKS:
    for vid, txt in EN_BIBLE[b].items():
        EN_TAGS[vid] = tag("english", txt)
for vid, txt in EN_QURAN.items():
    EN_TAGS[vid] = tag("english", txt)
QVIDS = [k for k in sorted(EN_QURAN, key=vkey) if 50 <= int(k.split(".")[1]) <= 114]


def chunk_book(lang, book):
    """verse-id-aligned chunks for one Bible book; returns [(text, tagset)]."""
    d = load(lang, book)
    if not d:
        return []
    vids = [v for v in sorted(EN_BIBLE[book], key=vkey) if v in d]
    out = []
    for i in range(0, len(vids), GROUP):
        grp = vids[i:i + GROUP]
        cs = set()
        for v in grp:
            cs |= set(EN_TAGS.get(v, []))
        out.append((" ".join(d[v] for v in grp), cs))
    return out


def chunk_quran(lang):
    d = load(lang, "quran_full")
    if not d:
        return []
    vids = [v for v in QVIDS if v in d]
    out = []
    for i in range(0, len(vids), GROUP):
        grp = vids[i:i + GROUP]
        cs = set()
        for v in grp:
            cs |= set(EN_TAGS.get(v, []))
        out.append((" ".join(d[v] for v in grp), cs))
    return out


def binding(sim, has, mask):
    both = has[:, None] & has[None, :] & mask
    one = (has[:, None] ^ has[None, :]) & mask
    nb, no = int(both.sum()), int(one.sum())
    if nb == 0 or no == 0:
        return float("nan"), nb
    return float((sim * both).sum() / nb - (sim * one).sum() / no), nb


def ccb_profile(sim, concs, mask, n, rng, perm=500):
    row = {}
    for c in CONCEPTS:
        has = np.array([c in s for s in concs])
        obs, nb = binding(sim, has, mask)
        if np.isnan(obs):
            row[c] = None
            continue
        nw = int(has.sum())
        diffs = []
        for _ in range(perm):
            m = np.zeros(n, bool)
            m[rng.permutation(n)[:nw]] = True
            d, _ = binding(sim, m, mask)
            if not np.isnan(d):
                diffs.append(d)
        row[c] = [round(obs, 4), round(float((np.array(diffs) >= obs).mean()), 4), nb]
    return row


def consensus_profile():
    d = json.load(open(REPO / "results" / "phase2b" / "bible_quran_baseline.json", encoding="utf-8"))
    rows = []
    for L, r in d.items():
        if all(r.get(c) for c in CONCEPTS):
            rows.append([r[c][0] for c in CONCEPTS])
    M = np.array(rows)
    Z = (M - M.mean(1, keepdims=True)) / (M.std(1, keepdims=True) + 1e-9)
    return Z.mean(0)


def main():
    from multilingual_embedder import MultilingualEmbedder
    em = MultilingualEmbedder("sentence-transformers/LaBSE")
    rng = np.random.default_rng(0)

    print("=== (1) WITHIN-BIBLE per-concept binding (register reliability) ===")
    within = {}
    embcache = {}
    for lang in ["greekkoine", "greekmodern", "chineseclassical", "chinese"]:
        chunks = [c for b in BOOKS for c in chunk_book(lang, b)]
        if len(chunks) < 30:
            print(f"  {lang:17s} skip (n={len(chunks)})")
            continue
        texts = [t for t, _ in chunks]
        concs = [s for _, s in chunks]
        v = em.encode(texts, batch_size=64)
        v = v / (np.linalg.norm(v, axis=1, keepdims=True) + 1e-12)
        embcache[lang] = (v, concs)
        sim = v @ v.T
        n = len(texts)
        up = np.triu(np.ones((n, n), bool), 1)
        row = ccb_profile(sim, concs, up, n, rng)
        within[lang] = row
        print(f"  {lang:17s} n={n:4d}  " + "  ".join(f"{c[:4]}={row[c][0] if row[c] else 'na'}" for c in CONCEPTS))

    print("\n=== REGISTER PENALTY (ancient/classical − modern, within-Bible binding) ===")
    for anc, mod, label in [("greekkoine", "greekmodern", "Greek koine−modern"),
                            ("chineseclassical", "chinese", "Chinese classical−modern")]:
        if anc in within and mod in within:
            deltas = []
            for c in CONCEPTS:
                a, m = within[anc].get(c), within[mod].get(c)
                if a and m:
                    deltas.append(f"{c[:4]}={a[0] - m[0]:+.4f}")
            print(f"  {label:26s} " + "  ".join(deltas))

    print("\n=== (2) CROSS-TRADITION Bible×Quran profile-fit vs 40-lang consensus ===")
    cons = consensus_profile()
    print("  consensus order: " + " > ".join(np.array(CONCEPTS)[np.argsort(-cons)]))
    for lang in ["greekmodern", "chinese"]:
        qch = chunk_quran(lang)
        if not qch or lang not in embcache:
            print(f"  {lang}: no quran / no bible emb -> skip")
            continue
        bv, bconcs = embcache[lang]
        qtexts = [t for t, _ in qch]
        qconcs = [s for _, s in qch]
        qv = em.encode(qtexts, batch_size=64)
        qv = qv / (np.linalg.norm(qv, axis=1, keepdims=True) + 1e-12)
        v = np.vstack([bv, qv])
        concs = bconcs + qconcs
        trad = np.array(["c"] * len(bconcs) + ["i"] * len(qconcs))
        n = len(concs)
        sim = v @ v.T
        up = np.triu(np.ones((n, n), bool), 1)
        cross = (trad[:, None] != trad[None, :]) & up
        row = ccb_profile(sim, concs, cross, n, rng)
        prof = np.array([row[c][0] if row[c] else 0.0 for c in CONCEPTS])
        z = (prof - prof.mean()) / (prof.std() + 1e-9)
        r = float(np.corrcoef(z, cons)[0, 1])
        print(f"  {lang:13s} profile-fit r={r:+.2f}  | " +
              "  ".join(f"{c[:4]}={row[c][0] if row[c] else 'na'}" for c in CONCEPTS))

    (REPO / "results" / "phase2b" / "register_reliability.json").write_text(
        json.dumps({"within_bible": within}, indent=2), encoding="utf-8")
    print("\nwrote results/phase2b/register_reliability.json")


if __name__ == "__main__":
    main()
