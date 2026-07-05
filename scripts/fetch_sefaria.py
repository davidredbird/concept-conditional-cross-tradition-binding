"""
Fetch Hebrew tradition text from Sefaria (sefaria.org API; clean digital Jewish
canon -- the Hebrew analog of CBETA/OpenITI). Phase 2a Hebrew pair:
Likutei Moharan (Rebbe Nachman, Hasidic mystical) × Guide for the Perplexed
(Maimonides, rationalist) -- a mystical×rationalist split paralleling Arabic
Sufi×Falsafa.

Iterates section refs "{prefix} {i}", pulls the Hebrew (he) segments, strips HTML.

Usage:
  python scripts/fetch_sefaria.py --prefix "Guide for the Perplexed, Part 1" --start 1 --count 76 \\
      --id maimonides_hebrew --tradition rationalist --category dualistic --title "Guide for the Perplexed"
  python scripts/fetch_sefaria.py --prefix "Likutei Moharan" --start 1 --count 80 \\
      --id nachman_hebrew --tradition hasidic --category nondual --title "Likutei Moharan"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
UA = {"User-Agent": "CCB-Research/0.1 (https://github.com/davidredbird/concept-conditional-cross-tradition-binding; research)"}


def get(url: str):
    wait = 4
    for attempt in range(5):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503):
                time.sleep(wait); wait = min(wait * 2, 40); continue
            return None
        except Exception:
            if attempt == 4:
                return None
            time.sleep(3)
    return None


def flatten(x) -> list[str]:
    out = []
    if isinstance(x, str):
        out.append(x)
    elif isinstance(x, list):
        for y in x:
            out += flatten(y)
    return out


def fetch_section(ref: str) -> str:
    r = get("https://www.sefaria.org/api/texts/" + urllib.parse.quote(ref) + "?context=0&commentary=0")
    if not r:
        return ""
    d = json.loads(r)
    segs = flatten(d.get("he", []))
    text = "\n".join(segs)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&[a-z]+;", " ", text)
    return text


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--count", type=int, default=76)
    ap.add_argument("--id", required=True)
    ap.add_argument("--tradition", required=True)
    ap.add_argument("--category", default="nondual")
    ap.add_argument("--title", default="")
    args = ap.parse_args()

    parts = []
    got = 0
    for i in range(args.start, args.start + args.count):
        t = fetch_section(f"{args.prefix} {i}")
        if t.strip():
            parts.append(t); got += 1
        time.sleep(0.3)
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(parts)).strip()
    heb = sum(1 for c in text if "֐" <= c <= "׿")
    print(f"{args.id}: {got} sections, {len(text)} chars, {len(text.split())} tokens, hebrew {heb/max(len(text),1):.0%}")

    out = REPO_ROOT / "corpus" / "books" / "cleaned"
    (out / f"{args.id}.txt").write_text(text, encoding="utf-8")
    meta = {"id": args.id, "title": args.title or args.prefix, "tradition": args.tradition,
            "category": args.category, "language": "hebrew", "source_id": args.id,
            "source": {"type": "sefaria", "prefix": args.prefix}, "license": "pd",
            "notes": "Phase 2a Hebrew (Sefaria). Mystical×rationalist pair."}
    (out / f"{args.id}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  wrote {args.id}.txt + .meta.json")


if __name__ == "__main__":
    main()
