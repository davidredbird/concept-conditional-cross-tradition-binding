"""
Fetch PD original-Castilian mystical texts from es.wikisource for Phase 2a.
Within-Christian Quietist×devotional pair:
  - Molinos, Guía Espiritual (Quietism: passive union / annihilation -> nondual)
  - Teresa de Ávila, Su Vida (Carmelite affective mysticism -> devotional)

(The cross-tradition contrast here is intra-Christian-school, not separate
lineages -- Spain's Muslim/Jewish traditions wrote in Arabic/Hebrew, so native
Castilian tradition text is overwhelmingly Christian.)

Usage:
  python scripts/fetch_spanish_texts.py
"""

from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
SITE = "es.wikisource.org"
UA = {"User-Agent": "CCB-Research/0.1 (https://github.com/davidredbird/concept-conditional-cross-tradition-binding; research)"}


def api(params: dict) -> dict:
    url = f"https://{SITE}/w/api.php?" + urllib.parse.urlencode(params)
    for a in range(5):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(8); continue
            raise
        except Exception:
            if a == 4:
                raise
            time.sleep(3)


def subpages(prefix: str) -> list[str]:
    d = api({"action": "query", "list": "allpages", "apprefix": prefix,
             "apnamespace": "0", "aplimit": "80", "format": "json"})
    return [p["title"] for p in d["query"]["allpages"]]


def fetch_page(page: str) -> str:
    d = api({"action": "parse", "page": page, "prop": "text", "format": "json", "disableeditsection": "1", "redirects": "1"})
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
        if ln and "mw-parser" not in ln and "parser-output" not in ln and len(re.findall(r"[a-záéíóúñ]", ln, re.I)) >= 8:
            lines.append(ln)
    return "\n".join(lines)


def save(bid, text, tradition, category, title):
    out = REPO_ROOT / "corpus" / "books" / "cleaned"
    (out / f"{bid}.txt").write_text(text, encoding="utf-8")
    meta = {"id": bid, "title": title, "tradition": tradition, "category": category,
            "language": "spanish", "source_id": bid, "source": {"type": "wikisource_es"},
            "license": "pd", "notes": "Phase 2a Spanish original (Castilian Christian mysticism)."}
    (out / f"{bid}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  wrote {bid}.txt ({len(text)} chars, {len(text.split())} tokens)")


def fetch_work(prefix, keep_re, bid, tradition, category, title):
    pages = [p for p in subpages(prefix) if re.search(keep_re, p)]
    print(f"{bid}: {len(pages)} pages")
    parts = []
    for p in pages:
        parts.append(fetch_page(p)); time.sleep(0.6)
    save(bid, re.sub(r"\n{3,}", "\n\n", "\n".join(parts)).strip(), tradition, category, title)


def main() -> None:
    fetch_work("Guía espiritual/", r"Libro|Introducción", "molinos_spanish",
               "quietist", "nondual", "Guía Espiritual (Molinos, Quietism)")
    fetch_work("Su vida (Santa Teresa de Jesús)/", r"Capítulo", "teresa_spanish",
               "carmelite", "dualistic", "Su Vida (Teresa de Ávila)")


if __name__ == "__main__":
    main()
