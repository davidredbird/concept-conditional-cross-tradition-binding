"""
Fetch PD French tradition texts from fr.wikisource for Phase 2a (French = a
second high-resource language at the HIGH-westernization end of the axis: these
are 19th-century French translations of the Eastern texts + a French rendering
of a Spanish mystic).

Three traditions in one language:
  - daoism    : Tao Te King (Stanislas Julien, 1842)            -> Chapitre 01..81
  - vedanta   : La Bhagavad-Gita (Emile Burnouf, 1861)          -> Chapitre 1..18
  - christian : Oeuvres spirituelles de Jean de la Croix        -> core mystical works

Wikisource works are split into chapter subpages; we enumerate them via the
allpages API, fetch each via action=parse, strip HTML + the per-chapter
header/navigation furniture, and concatenate. Output mirrors the Chinese
pipeline: corpus/books/cleaned/<id>.txt + <id>.meta.json.

Usage:
  python scripts/fetch_french_texts.py
  python scripts/fetch_french_texts.py --only taote_french
"""

from __future__ import annotations

import argparse
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
SITE = "fr.wikisource.org"
UA = {"User-Agent": "CCB-Research/0.1 (https://github.com/davidredbird/concept-conditional-cross-tradition-binding)"}

WORKS = [
    {
        "id": "taote_french", "tradition": "daoism", "category": "nondual",
        "title": "Tao Te King (traduction Stanislas Julien)", "translator": "Stanislas Julien (1842)",
        "era": "6c BCE (tr. 1842)", "source_id": "tao_te_ching",
        "prefix": "Tao Te King (Stanislas Julien)/",
        "keep": re.compile(r"/Chapitre \d+$"), "drop": None,
        "cut": re.compile(r"^NOTES"),  # keep Laozi's verse, drop Julien's commentary
    },
    {
        "id": "gita_french", "tradition": "vedanta", "category": "nondual",
        "title": "La Bhagavad-Gita (traduction Emile Burnouf)", "translator": "Emile-Louis Burnouf (1861)",
        "era": "~2c BCE (tr. 1861)", "source_id": "bhagavad_gita",
        "prefix": "La Bhagavad-Gîtâ, ou le Chant du Bienheureux/",
        "keep": re.compile(r"/Chapitre \d+$"), "drop": None,
    },
    {
        "id": "jeandelacroix_french", "tradition": "christian", "category": "nondual",
        "title": "Oeuvres spirituelles de Jean de la Croix", "translator": "fr. tr. (PD ed.)",
        "era": "16c CE (tr. PD)", "source_id": "jean_de_la_croix",
        "prefix": "Les Œuvres spirituelles du Bienheureux Jean de la Croix/",
        "keep": re.compile(r"(Cantiques spirituels|Montée|Nuit obscure|Vive [Ff]lamme)"),
        "drop": re.compile(r"(Préface|Avertissement|Approbation|Table|Notes?|Lettre|Avis|Appendice|Introduction|Argument)"),
    },
]

# per-chapter Wikisource furniture to drop (headers, nav, provenance lines)
FURNITURE = re.compile(
    r"(Traduction par|Libr\.|Imprimerie|IMPRIM|p\.\s*\d+\s*-\s*\d+|^book$|^◄|►$|^\s*[IVXLC]+\.\s|^\s*$"
    r"|wikisource|Wikisource|^\d+\s*$|Chapitre précédent|Chapitre suivant"
    r"|\.djvu|^Livre\s+[IVXLC]+$|page\s*\d+|^collection$|Préface du traducteur"
    r"|CANTIQUES SPIRITUELS|JÉSUS-CHRIST SON ÉPOUX|^[IVXLC]+\.\s*p\.|Vers\.$)"
)
# repeated title/provenance lines that leak from the page header
EXACT_DROP = {
    "Lao Tseu", "Stanislas Julien", "Le Livre de la voie et de la vertu", "Paris",
    "La Bhagavad-Gîtâ, ou le Chant du Bienheureux", "Émile-Louis Burnouf", "Burnouf",
    "Saint Jean de la Croix", "Jean Maillard", "Les Œuvres spirituelles du Bienheureux Jean de la Croix",
    "Préface", "Préface,", "Cantique", "book",
}
CJK = re.compile(r"[　-鿿]")


def keep_line(ln: str) -> bool:
    if not ln or ln in EXACT_DROP:
        return False
    if FURNITURE.search(ln):
        return False
    if CJK.search(ln):                       # stray Chinese (Julien philology)
        return False
    if re.fullmatch(r"[\W\d_]+", ln):        # punctuation/digits-only (Cantique tables)
        return False
    if len(ln) <= 2:                         # lone letters / fragments
        return False
    return True


def api(params: dict) -> dict:
    url = f"https://{SITE}/w/api.php?" + urllib.parse.urlencode(params)
    for attempt in range(5):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8"))
        except Exception:
            if attempt == 4:
                raise
            time.sleep(2)


def list_subpages(prefix: str) -> list[str]:
    out, cont = [], None
    while True:
        p = {"action": "query", "list": "allpages", "apprefix": prefix,
             "apnamespace": "0", "aplimit": "500", "format": "json"}
        if cont:
            p["apcontinue"] = cont
        d = api(p)
        out += [x["title"] for x in d["query"]["allpages"]]
        cont = d.get("continue", {}).get("apcontinue")
        if not cont:
            return out


def fetch_text(page: str, cut: re.Pattern | None = None) -> str:
    d = api({"action": "parse", "page": page, "prop": "text", "format": "json",
             "disableeditsection": "1", "redirects": "1"})
    if "error" in d:
        return ""
    h = d["parse"]["text"]["*"]
    h = re.sub(r"<table.*?</table>", "", h, flags=re.DOTALL)
    h = re.sub(r"<style.*?</style>", "", h, flags=re.DOTALL)
    h = re.sub(r"<sup\b.*?</sup>", "", h, flags=re.DOTALL)
    h = re.sub(r"<[^>]+>", "\n", h)
    t = html.unescape(h)
    t = re.sub(r"\[\d+\]", "", t)
    lines = []
    for ln in t.split("\n"):
        ln = ln.strip()
        if cut and cut.match(ln):     # stop at the per-chapter commentary marker
            break
        if keep_line(ln):
            lines.append(ln)
    return "\n".join(lines)


def latin_ratio(s: str) -> float:
    letters = sum(1 for c in s if c.isalpha())
    latin = sum(1 for c in s if c.isalpha() and ord(c) < 0x250)
    return latin / max(letters, 1)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", default=None, help="fetch only this work id")
    args = ap.parse_args()
    out_dir = REPO_ROOT / "corpus" / "books" / "cleaned"

    for w in WORKS:
        if args.only and w["id"] != args.only:
            continue
        subs = list_subpages(w["prefix"])
        kept = [s for s in subs if w["keep"].search(s) and not (w["drop"] and w["drop"].search(s))]
        kept.sort()
        print(f"\n=== {w['id']} ({w['tradition']}) ===")
        print(f"  {len(subs)} subpages -> {len(kept)} kept")
        parts = []
        for i, page in enumerate(kept):
            txt = fetch_text(page, w.get("cut"))
            if txt:
                parts.append(txt)
            if (i + 1) % 20 == 0:
                print(f"    fetched {i+1}/{len(kept)}")
            time.sleep(0.25)
        text = "\n".join(parts)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        lr = latin_ratio(text)
        print(f"  cleaned: {len(text)} chars, {len(text.split())} words, latin-script {lr:.0%}")
        print("  sample: " + text[:200].replace("\n", " / "))
        (out_dir / f"{w['id']}.txt").write_text(text, encoding="utf-8")
        meta = {"id": w["id"], "title": w["title"], "translator": w["translator"],
                "tradition": w["tradition"], "category": w["category"], "era": w["era"],
                "language": "french", "source_id": w["source_id"],
                "source": {"type": "wikisource_fr", "prefix": w["prefix"], "n_subpages": len(kept)},
                "license": "pd", "notes": "Phase 2a French (high-westernization axis point). PD 19c fr. translation."}
        (out_dir / f"{w['id']}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  wrote {w['id']}.txt + .meta.json")


if __name__ == "__main__":
    main()
