"""
Validate the DRAFT control-concept dictionaries (control_concepts.py) on SCRIPTURE only
(Bible — firewall-safe; does NOT touch the sealed Plato…Zhuxi philosophical corpus).

Checks two things before these anchors are trusted for 3a:
  1. NATIVE prevalence — do the per-language dicts fire at comparable rates in en/grc/zh?
     (a coverage screen for the dictionaries themselves)
  2. WITHIN-BIBLE binding — do EATING/SLEEP/GOVERNANCE/WARFARE passages actually cluster
     (english-projected tags held identical across languages, so only embedding varies)?

Usage: python scripts/validate_control_concepts.py
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
import control_concepts as cc  # noqa: E402

GROUP = 8
BOOKS = ["john", "gen", "ecc"]
CONS = cc.CONCEPTS


def load(lang, b):
    p = CACHE / f"{lang}_{b}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def vkey(k):
    return [int(x) for x in re.findall(r"\d+", k)]


EN_BIBLE = {b: load("english", b) for b in BOOKS}
EN_TAGS = {}
for b in BOOKS:
    for vid, txt in EN_BIBLE[b].items():
        EN_TAGS[vid] = cc.tag("english", txt)


def chunk_proj(lang, b):
    d = load(lang, b)
    if not d:
        return []
    vids = [v for v in sorted(EN_BIBLE[b], key=vkey) if v in d]
    out = []
    for i in range(0, len(vids), GROUP):
        grp = vids[i:i + GROUP]
        cs = set()
        for v in grp:
            cs |= set(EN_TAGS.get(v, []))
        out.append((" ".join(d[v] for v in grp), cs))
    return out


def native_prev(lang, taglang):
    cnt = {c: 0 for c in CONS}
    tot = 0
    for b in BOOKS:
        for txt in load(lang, b).values():
            tot += 1
            for c in cc.tag(taglang, txt):
                cnt[c] += 1
    return {c: round(cnt[c] / tot, 3) for c in CONS}, tot


def binding(sim, has, mask):
    both = has[:, None] & has[None, :] & mask
    one = (has[:, None] ^ has[None, :]) & mask
    nb, no = int(both.sum()), int(one.sum())
    if nb == 0 or no == 0:
        return float("nan"), nb
    return float((sim * both).sum() / nb - (sim * one).sum() / no), nb


def main():
    from multilingual_embedder import MultilingualEmbedder
    em = MultilingualEmbedder("sentence-transformers/LaBSE")
    rng = np.random.default_rng(0)

    print("=== NATIVE prevalence (verses tagged / total) per language dict ===")
    for lang, tl in [("english", "english"), ("greekkoine", "greek"), ("chineseclassical", "chinese")]:
        pv, tot = native_prev(lang, tl)
        print(f"  {lang:17s} n={tot:4d}  " + "  ".join(f"{c[:4]}={pv[c]}" for c in CONS))

    print("\n=== WITHIN-BIBLE binding for control concepts (english-projected tags) ===")
    for lang in ["greekkoine", "chineseclassical", "english"]:
        ch = [c for b in BOOKS for c in chunk_proj(lang, b)]
        texts = [t for t, _ in ch]
        concs = [s for _, s in ch]
        if len(texts) < 30:
            print(f"  {lang}: skip")
            continue
        v = em.encode(texts, batch_size=64)
        v = v / (np.linalg.norm(v, axis=1, keepdims=True) + 1e-12)
        sim = v @ v.T
        n = len(texts)
        up = np.triu(np.ones((n, n), bool), 1)
        cells = []
        for c in CONS:
            has = np.array([c in s for s in concs])
            nw = int(has.sum())
            obs, nb = binding(sim, has, up)
            if np.isnan(obs):
                cells.append(f"{c[:4]}=na")
                continue
            diffs = []
            for _ in range(400):
                m = np.zeros(n, bool)
                m[rng.permutation(n)[:nw]] = True
                d, _ = binding(sim, m, up)
                if not np.isnan(d):
                    diffs.append(d)
            p = float((np.array(diffs) >= obs).mean())
            cells.append(f"{c[:4]}={obs:+.3f}(p{p:.2f},n{nw})")
        print(f"  {lang:17s} " + "  ".join(cells))
    print("\ndone")


if __name__ == "__main__":
    main()
