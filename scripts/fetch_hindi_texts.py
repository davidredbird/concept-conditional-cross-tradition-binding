"""
Fetch PD original-Hindi tradition texts from hi.wikisource (born-digital
Devanagari, NOT OCR) for Phase 2a. Pair: Kabir Granthavali (Nirguṇa Sant,
nondual) × Tulsidas Ramcharitmanas Balkand (Saguṇa Vaishnava Bhakti,
devotional) -- both original Hindi/Awadhi (15-16c), a Nirguṇa×Saguṇa divide.

Uses a descriptive User-Agent + per-request pacing + 429-aware backoff
(Wikimedia rate-limits anonymous API bursts).

Usage:
  python scripts/fetch_hindi_texts.py
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
sys.stdout.reconfigure(encoding="utf-8")
SITE = "hi.wikisource.org"
UA = {"User-Agent": "CCB-Research/0.1 (https://github.com/davidredbird/concept-conditional-cross-tradition-binding; research)"}
DEVA = re.compile(r"[ऀ-ॿ]")


def api(params: dict) -> dict:
    import urllib.parse
    url = f"https://{SITE}/w/api.php?" + urllib.parse.urlencode(params)
    wait = 5
    for attempt in range(6):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                ra = int(e.headers.get("Retry-After", wait))
                print(f"    429; backing off {ra}s")
                time.sleep(min(ra, 60))
                wait = min(wait * 2, 60)
                continue
            raise
        except Exception:
            if attempt == 5:
                raise
            time.sleep(3)
    raise SystemExit("rate-limited")


def subpages(prefix: str) -> list[str]:
    d = api({"action": "query", "list": "allpages", "apprefix": prefix,
             "apnamespace": "0", "aplimit": "60", "format": "json"})
    return [p["title"] for p in d["query"]["allpages"]]


def fetch_page(page: str) -> str:
    d = api({"action": "parse", "page": page, "prop": "text", "format": "json", "redirects": "1"})
    if "error" in d:
        return ""
    h = d["parse"]["text"]["*"]
    h = re.sub(r"<style.*?</style>", "", h, flags=re.DOTALL)
    h = re.sub(r"<table.*?</table>", "", h, flags=re.DOTALL)
    h = re.sub(r"<sup\b.*?</sup>", "", h, flags=re.DOTALL)
    h = re.sub(r"<[^>]+>", "\n", h)
    t = html.unescape(h)
    lines = []
    for ln in t.split("\n"):
        ln = ln.strip()
        if ln and "mw-parser" not in ln and "parser-output" not in ln and len(DEVA.findall(ln)) >= 3:
            lines.append(ln)
    return "\n".join(lines)


def save(bid: str, text: str, tradition: str, category: str, title: str) -> None:
    out = REPO_ROOT / "corpus" / "books" / "cleaned"
    (out / f"{bid}.txt").write_text(text, encoding="utf-8")
    meta = {"id": bid, "title": title, "tradition": tradition, "category": category,
            "language": "hindi", "source_id": bid, "source": {"type": "wikisource_hi"},
            "license": "pd", "notes": "Phase 2a Hindi original (born-digital Devanagari)."}
    (out / f"{bid}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  wrote {bid}.txt ({len(text)} chars, {len(text.split())} tokens)")


def main() -> None:
    kabir_pages = [p for p in subpages("कबीर ग्रंथावली/") if "अंग" in p]
    print(f"Kabir: {len(kabir_pages)} sections")
    parts = []
    for i, p in enumerate(kabir_pages):
        parts.append(fetch_page(p))
        time.sleep(0.6)
    save("kabir_hindi", "\n".join(parts), "sant", "nondual", "कबीर ग्रंथावली (Kabir, Nirguna)")

    print("Tulsidas Balkand")
    save("tulsidas_hindi", fetch_page("रामचरितमानस/बालकाण्ड"), "bhakti", "dualistic",
         "रामचरितमानस बालकाण्ड (Tulsidas, Saguna)")


if __name__ == "__main__":
    main()
