"""
Fetch a classical Arabic text from the OpenITI corpus (github.com/OpenITI), the
clean machine-readable Islamicate-texts collection (the Arabic analog of CBETA).
Strips OpenITI mARkdown markup -> plain Arabic + meta.json, mirroring the Chinese
CBETA pipeline. For Phase 2a: a SECOND non-Western ORIGINAL language to test
whether the WORLD-robust / AWARENESS-translation / SUBSTRATE-native pattern
generalizes beyond classical Chinese.

Usage:
  python scripts/fetch_openiti.py --century 0650AH --author 0638IbnCarabi \\
      --book 0638IbnCarabi.FususHikam --id fusus_arabic --tradition sufi --category nondual
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
UA = {"User-Agent": "CCB-Research/0.1 (https://github.com/davidredbird/concept-conditional-cross-tradition-binding)"}


def get(url: str) -> str:
    for a in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode("utf-8", errors="replace")
        except Exception:
            if a == 3:
                raise
            time.sleep(2)


def find_text_version(century: str, author: str, book: str) -> str:
    api = f"https://api.github.com/repos/OpenITI/{century}/contents/data/{author}/{book}"
    files = json.loads(get(api))
    cand = [(f["name"], f["size"]) for f in files if not f["name"].endswith(".yml")
            and not f["name"].endswith(".md")]
    if not cand:
        raise SystemExit(f"no text version found in {book}")
    return max(cand, key=lambda x: x[1])[0]


def clean_markdown(raw: str) -> str:
    # OpenITI mARkdown -> plain text
    lines = []
    for ln in raw.split("\n"):
        if ln.startswith("######OpenITI#") or ln.startswith("#META#") or ln.startswith("#NewRec"):
            continue
        ln = re.sub(r"^~~", "", ln)                 # line-continuation marker
        ln = re.sub(r"^###?\s*\|+\s*", "", ln)       # structural headers ### |
        ln = re.sub(r"^#\s*", "", ln)                # paragraph marker
        ln = re.sub(r"PageV\d+P\d+", "", ln)          # page markers
        ln = re.sub(r"ms\d+", "", ln)                 # manuscript markers
        ln = re.sub(r"@[A-Z]+@[^@]*@", "", ln)        # OpenITI tags
        ln = re.sub(r"\([٠-٩\d]+[أ-يA-Za-z]?\)", "", ln)  # footnote/edition refs (123) (2ب)
        ln = re.sub(r"[~|=]+", " ", ln)
        ln = ln.strip()
        if ln:
            lines.append(ln)
    text = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--century", required=True)
    ap.add_argument("--author", required=True)
    ap.add_argument("--book", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--tradition", required=True)
    ap.add_argument("--category", default="nondual")
    ap.add_argument("--title", default="")
    args = ap.parse_args()

    version = find_text_version(args.century, args.author, args.book)
    print(f"text version: {version}")
    raw = get(f"https://raw.githubusercontent.com/OpenITI/{args.century}/master/data/{args.author}/{args.book}/{version}")
    text = clean_markdown(raw)
    ar = sum(1 for c in text if "؀" <= c <= "ۿ")
    print(f"cleaned: {len(text)} chars, {len(text.split())} words, arabic-script {ar/max(len(text),1):.0%}")
    print("sample: " + text[:160].replace("\n", " / "))

    out = REPO_ROOT / "corpus" / "books" / "cleaned"
    (out / f"{args.id}.txt").write_text(text, encoding="utf-8")
    meta = {"id": args.id, "title": args.title or args.book, "tradition": args.tradition,
            "category": args.category, "language": "arabic", "source_id": args.book,
            "source": {"type": "openiti", "century": args.century, "author": args.author, "book": args.book, "version": version},
            "license": "pd", "notes": "Classical Arabic original (OpenITI). Phase 2a 2nd non-Western original-language anchor."}
    (out / f"{args.id}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {args.id}.txt + .meta.json")


if __name__ == "__main__":
    main()
