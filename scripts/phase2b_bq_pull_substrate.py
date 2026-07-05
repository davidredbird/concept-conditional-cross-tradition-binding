"""
Phase 2b — extend the Bible×Quran cache with SUBSTRATE-bearing material so the
emptiness/non-being concept becomes testable in the reference grid:
  Bible side : Ecclesiastes (hevel/'vanity'-emptiness) + Genesis (tohu va-vohu,
               'formless and void') -> {lang}_ecc.json, {lang}_gen.json
  Quran side : the FULL Quran (so we can use 28:88 / 55 / 56 / 57 / 112 — the
               fanaʾ / 'all perishes except His Face' / al-ghayb material)
               -> {lang}_quran_full.json
(-NT-only Bible files have no OT, so Ecclesiastes/Genesis are skipped there.)
Network-only. Usage: python scripts/phase2b_bq_pull_substrate.py
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
sys.stdout.reconfigure(encoding="utf-8")
UA = {"User-Agent": "CCB-Research/0.1 (research)"}


def get(url):
    for a in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read().decode("utf-8", errors="replace")
        except Exception:
            if a == 3:
                return None
            time.sleep(2)


def norm(name):
    n = name.lower()
    for s in ("-nt", "-part", "-tok", " (simplified)", "(simplified)", "(traditional)"):
        n = n.replace(s, "")
    return n.strip()


def maps():
    r = get("https://api.github.com/repos/christos-c/bible-corpus/contents/bibles")
    bf = {}
    for x in json.loads(r):
        bf.setdefault(norm(x["name"].replace(".xml", "")), x["name"].replace(".xml", ""))
    eds = json.loads(get("https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions.json"))
    qe = {}
    for v in eds.values():
        if isinstance(v, dict) and v.get("language"):
            qe.setdefault(norm(v["language"]), v["name"])
    return bf, qe


def extract_book(xml, book):  # book e.g. 'ECC','GEN'
    out = {}
    for vid, txt in re.findall(rf'<seg id="(b\.{book}\.\d+\.\d+)"[^>]*>(.*?)</seg>', xml, re.DOTALL):
        t = " ".join(re.sub(r"<[^>]+>", " ", html.unescape(txt)).split())
        if t:
            out[vid] = t
    return out


def main():
    bf, qe = maps()
    langs = sorted(set(p.name.split("_")[0] for p in CACHE.glob("*_john.json")))
    print(f"{len(langs)} cached languages to extend")
    for lang in langs:
        # Quran full
        qf = CACHE / f"{lang}_quran_full.json"
        if not qf.exists() and lang in qe:
            r = get(f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{qe[lang]}.json")
            if r:
                try:
                    items = json.loads(r).get("quran", [])
                    full = {f"q.{int(i['chapter'])}.{int(i['verse'])}": i["text"] for i in items}
                    qf.write_text(json.dumps(full, ensure_ascii=False), encoding="utf-8")
                except Exception:
                    pass
        # Bible OT wisdom books
        ef = CACHE / f"{lang}_ecc.json"
        gf = CACHE / f"{lang}_gen.json"
        if (not ef.exists() or not gf.exists()) and lang in bf:
            xml = get(f"https://raw.githubusercontent.com/christos-c/bible-corpus/master/bibles/{bf[lang]}.xml")
            if xml:
                ecc = extract_book(xml, "ECC"); gen = extract_book(xml, "GEN")
                if ecc:
                    ef.write_text(json.dumps(ecc, ensure_ascii=False), encoding="utf-8")
                if gen:
                    gf.write_text(json.dumps(gen, ensure_ascii=False), encoding="utf-8")
        ec = len(json.loads(ef.read_text(encoding="utf-8"))) if ef.exists() else 0
        gc = len(json.loads(gf.read_text(encoding="utf-8"))) if gf.exists() else 0
        qc = len(json.loads(qf.read_text(encoding="utf-8"))) if qf.exists() else 0
        print(f"  {lang:14s} ecc={ec} gen={gc} quran_full={qc}")
        time.sleep(0.3)
    print("done extending cache")


if __name__ == "__main__":
    main()
