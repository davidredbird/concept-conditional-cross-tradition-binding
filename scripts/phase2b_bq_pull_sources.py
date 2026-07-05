"""
Phase 2b — PULL & CACHE sources for the maximal Bible(John) × Quran multilingual
test. Network-only (no embedding), so it can run alongside other CPU jobs.

Matches the christos-c/bible-corpus languages against fawazahmed0/quran-api
languages, then caches per-language verse dicts to corpus/cache/bq/:
  {lang}_john.json   = {"b.JOH.C.V": text, ...}
  {lang}_quran.json  = {"q.S.A": text, ...}   (first QURAN_VERSES verses)
Verse IDs are stable across languages -> later embed step projects English tags.

Usage: python scripts/phase2b_bq_pull_sources.py
"""

from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE = REPO_ROOT / "corpus" / "cache" / "bq"
CACHE.mkdir(parents=True, exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8")
UA = {"User-Agent": "CCB-Research/0.1 (research)"}
QURAN_VERSES = 1200


def get(url):
    for a in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode("utf-8", errors="replace")
        except Exception:
            if a == 3:
                return None
            time.sleep(2)


def norm(name):  # normalize a language name for matching
    n = name.lower()
    for suf in ("-nt", "-part", "-tok", " (simplified)", "(simplified)", "(traditional)"):
        n = n.replace(suf, "")
    return n.strip()


def bible_files():
    r = get("https://api.github.com/repos/christos-c/bible-corpus/contents/bibles")
    if not r:
        return {}
    out = {}
    for x in json.loads(r):
        fn = x["name"].replace(".xml", "")
        out.setdefault(norm(fn), fn)  # keep first (prefer full Bible over -NT alphabetically? both fine for John)
    return out


def quran_editions():
    eds = json.loads(get("https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions.json"))
    out = {}
    for v in eds.values():
        if isinstance(v, dict) and v.get("language"):
            out.setdefault(norm(v["language"]), v["name"])
    return out


def fetch_john(bible_file):
    r = get(f"https://raw.githubusercontent.com/christos-c/bible-corpus/master/bibles/{bible_file}.xml")
    if not r:
        return {}
    out = {}
    for vid, txt in re.findall(r'<seg id="(b\.JOH\.\d+\.\d+)"[^>]*>(.*?)</seg>', r, re.DOTALL):
        t = " ".join(re.sub(r"<[^>]+>", " ", html.unescape(txt)).split())
        if t:
            out[vid] = t
    return out


def fetch_quran(edition):
    r = get(f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{edition}.json")
    if not r:
        return {}
    try:
        items = json.loads(r).get("quran", [])
    except Exception:
        return {}
    rows = sorted(((int(i["chapter"]), int(i["verse"]), i["text"]) for i in items), key=lambda x: (x[0], x[1]))
    return {f"q.{c}.{v}": t for c, v, t in rows[:QURAN_VERSES]}


def main():
    bf = bible_files()
    qe = quran_editions()
    common = sorted(set(bf) & set(qe))
    print(f"bible langs={len(bf)}, quran langs={len(qe)}, overlap={len(common)}")
    cached = 0
    for lang in common:
        jf = CACHE / f"{lang}_john.json"
        qf = CACHE / f"{lang}_quran.json"
        if jf.exists() and qf.exists():
            cached += 1
            continue
        john = fetch_john(bf[lang])
        quran = fetch_quran(qe[lang])
        if len(john) < 100 or len(quran) < 100:
            print(f"  {lang:18s} skip (john={len(john)} quran={len(quran)})")
            continue
        jf.write_text(json.dumps(john, ensure_ascii=False), encoding="utf-8")
        qf.write_text(json.dumps(quran, ensure_ascii=False), encoding="utf-8")
        cached += 1
        print(f"  {lang:18s} cached (john={len(john)} quran={len(quran)})")
        time.sleep(0.3)
    print(f"\nCached {cached} languages -> {CACHE}")


if __name__ == "__main__":
    main()
