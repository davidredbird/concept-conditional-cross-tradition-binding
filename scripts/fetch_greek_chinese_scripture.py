"""
Source PARALLEL SCRIPTURE (Bible + Quran) in GREEK and CHINESE for the
comparative-NLP reference baseline. DATA COLLECTION ONLY (fetch / clean / write).

Outputs (register-explicit langkeys):
  greekkoine        -> ancient Greek Bible: John (Koine, original), Genesis+Ecclesiastes (LXX)
  greekmodern       -> modern Greek Bible (John/Gen/Ecc) + modern Greek Quran (quran_full)
  chineseclassical  -> classical Chinese Bible (Wenli Union 1919): John/Gen/Ecc

Per-verse JSON  -> corpus/cache/bq/{langkey}_{book}.json   (keys b.JOH.C.V / q.S.A; matches existing baseline)
Cleaned text    -> corpus/books/cleaned/{langkey}_{book}.txt + .meta.json

Network-only. No embedding / analysis / git.
Usage: python scripts/fetch_greek_chinese_scripture.py
"""

from __future__ import annotations

import html
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE = REPO_ROOT / "corpus" / "cache" / "bq"
CLEANED = REPO_ROOT / "corpus" / "books" / "cleaned"
CACHE.mkdir(parents=True, exist_ok=True)
CLEANED.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "CCB-Research/0.1 (research)"}


def get(url, tries=4, timeout=90):
    for a in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read().decode("utf-8", errors="replace")
        except Exception:
            if a == tries - 1:
                return None
            time.sleep(2)


# ---------- script-percentage (same definition the pipeline uses) ----------

def is_greek(c):
    o = ord(c)
    return (0x0370 <= o <= 0x03FF) or (0x1F00 <= o <= 0x1FFF)


def is_han(c):
    return 0x4E00 <= ord(c) <= 0x9FFF


def script_pct(t):
    nonws = [c for c in t if not c.isspace()]
    if not nonws:
        return 0.0
    g = sum(1 for c in nonws if is_greek(c))
    h = sum(1 for c in nonws if is_han(c))
    return max(g, h) / len(nonws)


# ---------- writers ----------

def write_cache(langkey, book, verses):
    """verses: dict {key: text}; key already in b.* / q.* form."""
    p = CACHE / f"{langkey}_{book}.json"
    p.write_text(json.dumps(verses, ensure_ascii=False), encoding="utf-8")
    return p


def write_cleaned(idd, verses, meta):
    """Running text = verses joined with newlines (clean, no refs)."""
    text = "\n".join(verses.values()).strip()
    (CLEANED / f"{idd}.txt").write_text(text + "\n", encoding="utf-8")
    meta = dict(meta)
    meta["_clean"] = {
        "char_count": len(text),
        "target_script_pct": round(script_pct(text), 3),
        "n_verses": len(verses),
    }
    (CLEANED / f"{idd}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(text), round(script_pct(text), 3), len(verses)


# =========================================================================
# PRIORITY 1a — Koine NT, Gospel of John (ORIGINAL). Nestle 1904 (PD).
# OSIS-ish XML: <milestone unit="verse" id="John.C.V"/> then <w>..</w> / <pc>..</pc>.
# =========================================================================

def fetch_koine_john():
    url = "https://raw.githubusercontent.com/biblicalhumanities/Nestle1904/master/xml/04-john.xml"
    raw = get(url)
    if not raw:
        return {}, url
    # Walk the XML in document order; accumulate <w>/<pc> text under the current verse milestone.
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        root = ET.fromstring(re.sub(r"<\?xml-model[^>]*\?>", "", raw))

    def local(tag):
        return tag.split("}", 1)[1] if (tag and "}" in tag) else (tag or "")

    verses = {}
    cur = None  # current canonical key e.g. b.JOH.1.1
    buf = []

    def flush():
        if cur and buf:
            # join words with spaces, then tidy spaces before punctuation
            t = " ".join(buf)
            t = re.sub(r"\s+([,.;··:!?])", r"\1", t)
            t = re.sub(r"\s+", " ", t).strip()
            if t:
                verses[cur] = verses.get(cur, "") + (" " if cur in verses else "") + t

    for el in root.iter():
        ln = local(el.tag)
        if ln == "milestone" and (el.get("unit") == "verse"):
            flush()
            buf = []
            vid = el.get("id") or el.get("osisID") or ""
            m = re.match(r"John\.(\d+)\.(\d+)", vid)
            cur = f"b.JOH.{m.group(1)}.{m.group(2)}" if m else None
        elif ln in ("w", "pc"):
            if el.text and el.text.strip():
                buf.append(el.text.strip())
    flush()
    return verses, url


# =========================================================================
# PRIORITY 1b — Septuagint (Swete LXX, 1909/1930) Genesis + Ecclesiastes (ancient Greek).
# eliranwong/LXX-Swete-1930: word-with-punctuation CSV + a versification CSV
# mapping (start_word_index -> "Gen.C:V"). A verse owns words [start, next_start).
# =========================================================================

LXX_BOOKMAP = {"gen": "Gen", "ecc": "Ecc"}


def _swete_data():
    words = get("https://raw.githubusercontent.com/eliranwong/LXX-Swete-1930/master/01-Swete_word_with_punctuations.csv")
    vers = get("https://raw.githubusercontent.com/eliranwong/LXX-Swete-1930/master/00-Swete_versification.csv")
    if not words or not vers:
        return None, None, None
    # word index -> token
    wmap = {}
    for ln in words.splitlines():
        if "\t" not in ln:
            continue
        idx, tok = ln.split("\t", 1)
        if idx.strip().isdigit():
            wmap[int(idx)] = tok.strip()
    # ordered (start_index, ref)
    rows = []
    for ln in vers.splitlines():
        if "\t" not in ln:
            continue
        idx, ref = ln.split("\t", 1)
        if idx.strip().isdigit():
            rows.append((int(idx), ref.strip()))
    rows.sort()
    return wmap, rows, max(wmap) if wmap else 0


def fetch_lxx_book(book):  # book in {'gen','ecc'}
    src = "https://raw.githubusercontent.com/eliranwong/LXX-Swete-1930"
    wmap, rows, maxidx = _swete_data()
    if not wmap:
        return {}, src
    label = LXX_BOOKMAP[book]
    osis = {"gen": "GEN", "ecc": "ECC"}[book]
    verses = {}
    for i, (start, ref) in enumerate(rows):
        end = rows[i + 1][0] if i + 1 < len(rows) else maxidx + 1
        m = re.match(rf"{label}\.(\d+):(\d+)$", ref)
        if not m:
            continue
        toks = [wmap[w] for w in range(start, end) if w in wmap]
        t = " ".join(toks)
        # strip apparatus: Göttingen/CATSS editorial sigla (U+2E00–2E7F) and
        # square brackets around uncertain letters (keep the bracketed letter).
        t = re.sub(r"[⸀-⹿]", "", t)
        t = t.replace("[", "").replace("]", "")
        t = re.sub(r"\s+([,.;··:!?])", r"\1", t)
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            verses[f"b.{osis}.{m.group(1)}.{m.group(2)}"] = t
    return verses, src


# =========================================================================
# PRIORITY 4 — Modern Greek Bible. christos-c/bible-corpus Greek.xml (TEI <seg>).
# Same extract_book pattern as the existing pipeline.
# =========================================================================

def fetch_modern_greek_bible():
    url = "https://raw.githubusercontent.com/christos-c/bible-corpus/master/bibles/Greek.xml"
    raw = get(url)
    out = {"john": {}, "gen": {}, "ecc": {}}
    if not raw:
        return out, url
    for book, osis in (("john", "JOH"), ("gen", "GEN"), ("ecc", "ECC")):
        for vid, txt in re.findall(rf'<seg id="(b\.{osis}\.\d+\.\d+)"[^>]*>(.*?)</seg>', raw, re.DOTALL):
            t = " ".join(re.sub(r"<[^>]+>", " ", html.unescape(txt)).split())
            if t:
                out[book][vid] = t
    return out, url


# =========================================================================
# PRIORITY 3 — Modern Greek QURAN (no ancient exists). quranenc.com greek_rwwad.
# Per-sura JSON: result[].{sura,aya,translation}. Register compromise -> flagged.
# =========================================================================

def fetch_greek_quran():
    base = "https://quranenc.com/api/v1/translation/sura/greek_rwwad/"
    verses = {}
    for s in range(1, 115):
        r = get(base + str(s), timeout=60)
        if not r:
            continue
        try:
            res = json.loads(r).get("result", [])
        except Exception:
            continue
        for item in res:
            try:
                c = int(item["sura"]); v = int(item["aya"]); t = (item.get("translation") or "").strip()
            except Exception:
                continue
            if t:
                verses[f"q.{c}.{v}"] = " ".join(t.split())
        time.sleep(0.15)
    return verses, "https://quranenc.com/api/v1/translation/sura/greek_rwwad/{1..114}"


# =========================================================================
# PRIORITY 2 — Classical Chinese Bible. zh.wikisource Wenli Union Version (文理和合, 1919).
# Subpages use {{verse|chapter=C|verse=V}} markers. Inline {{ul|X}}/{{du|X}} = proper names
# (unwrap to X); strip ○ paragraph marks and residual templates.
# =========================================================================

WENLI = {
    "john": "聖經 (文理和合)/約翰福音",
    "gen": "聖經 (文理和合)/創世記",
    "ecc": "聖經 (文理和合)/傳道書",
}
WENLI_OSIS = {"john": "JOH", "gen": "GEN", "ecc": "ECC"}


def _clean_zh_verse(t):
    # unwrap name templates: {{ul|約翰}} / {{du|猶太}} -> last pipe segment
    t = re.sub(r"\{\{(?:ul|du|le)\|([^{}]*?)\}\}", lambda m: m.group(1).split("|")[-1], t)
    # drop any remaining templates / wikilinks / html
    for _ in range(6):
        new = re.sub(r"\{\{[^{}]*\}\}", "", t)
        if new == t:
            break
        t = new
    t = re.sub(r"\[\[([^\[\]]*)\]\]", lambda m: m.group(1).split("|")[-1], t)
    t = re.sub(r"<[^>]+>", "", t)
    # editorial paragraph mark and stray markers
    t = t.replace("○", "").replace("　", "")
    t = t.strip().strip("'")
    return re.sub(r"\s+", "", t)  # classical Chinese: no internal spaces


def fetch_wenli_book(book):
    title = WENLI[book]
    url = "https://zh.wikisource.org/wiki/" + urllib.parse.quote(title) + "?action=raw"
    raw = get(url)
    verses = {}
    if not raw:
        return verses, url
    osis = WENLI_OSIS[book]
    # split on verse markers; capture chapter/verse then text up to next marker or heading
    pat = re.compile(r"\{\{verse\|chapter=(\d+)\|verse=(\d+)\}\}(.*?)(?=\{\{verse\||==|\{\{chapter|\Z)", re.DOTALL)
    for c, v, body in pat.findall(raw):
        t = _clean_zh_verse(body)
        if t:
            verses[f"b.{osis}.{c}.{v}"] = t
    return verses, "https://zh.wikisource.org/wiki/" + title


# =========================================================================

def main():
    rows = []  # (langkey, book, register, n, chars, pct, source)

    def record(langkey, book, register, verses, meta):
        if not verses:
            print(f"  !! {langkey}_{book}: NO VERSES (source failed)")
            rows.append((langkey, book, register, 0, 0, 0.0, meta["source"]["url"]))
            return
        write_cache(langkey, book, verses)
        idd = f"{langkey}_{book}"
        ch, pct, n = write_cleaned(idd, verses, meta)
        rows.append((langkey, book, register, n, ch, pct, meta["source"]["url"]))
        print(f"  ok {idd}: n={n} chars={ch} script_pct={pct}")

    # ---- P1a: Koine John (original) ----
    print("[P1a] Koine NT — John (Nestle 1904)")
    vj, ju = fetch_koine_john()
    record("greekkoine", "john", "ancient", vj, {
        "id": "greekkoine_john", "title": "ΚΑΤΑ ΙΩΑΝΝΗΝ (Gospel of John, Koine Greek — original)",
        "tradition": "christian", "category": "dualistic", "sphere": "greek",
        "language": "koine_greek", "register": "ancient",
        "source": {"type": "nestle1904_github", "url": ju},
        "license": "pd",
        "notes": "Original-language Koine NT (Nestle 1904, PD). Highest-value ancient Greek scripture in this set; verses reconstructed from <w>/<pc> tokens under verse milestones.",
    })

    # ---- P1b: LXX Genesis + Ecclesiastes (ancient) ----
    print("[P1b] Septuagint — Genesis + Ecclesiastes (Swete LXX 1909/1930)")
    for book, title in (("gen", "ΓΕΝΕΣΙΣ (Genesis, Septuagint/LXX — ancient Greek)"),
                        ("ecc", "ΕΚΚΛΗΣΙΑΣΤΗΣ (Ecclesiastes/Qoheleth, Septuagint/LXX — ancient Greek)")):
        v, su = fetch_lxx_book(book)
        record("greekkoine", book, "ancient", v, {
            "id": f"greekkoine_{book}", "title": title,
            "tradition": "jewish", "category": "dualistic", "sphere": "greek",
            "language": "ancient_greek_lxx", "register": "ancient",
            "source": {"type": "lxx_swete_1930_github", "url": su},
            "license": "gpl-3.0 (digitization); underlying Swete LXX 1909 text is public domain",
            "notes": "Septuagint (Swete edition). Ancient-Greek translation of a Hebrew original. Reconstructed from word + versification CSVs (eliranwong/LXX-Swete-1930).",
        })

    # ---- P4: Modern Greek Bible ----
    print("[P4] Modern Greek Bible (christos-c/bible-corpus Greek.xml)")
    mg, mu = fetch_modern_greek_bible()
    for book, title in (("john", "Κατά Ιωάννην (Gospel of John, modern Greek)"),
                        ("gen", "Γένεσις (Genesis, modern Greek)"),
                        ("ecc", "Εκκλησιαστής (Ecclesiastes, modern Greek)")):
        record("greekmodern", book, "modern", mg[book], {
            "id": f"greekmodern_{book}", "title": title,
            "tradition": "christian" if book == "john" else "jewish",
            "category": "dualistic", "sphere": "greek",
            "language": "modern_greek", "register": "modern",
            "source": {"type": "christos-c_bible-corpus", "url": mu},
            "license": "see christos-c/bible-corpus (modern translation; per-source terms)",
            "notes": "Modern Greek translation. Included for an ancient-vs-modern register comparison against greekkoine.",
        })

    # ---- P3: Modern Greek Quran (register compromise) ----
    print("[P3] Modern Greek Quran (quranenc greek_rwwad) — NO ancient version exists")
    vq, qu = fetch_greek_quran()
    record("greekmodern", "quran_full", "modern", vq, {
        "id": "greekmodern_quran_full", "title": "Το Κοράνιο (Quran, modern Greek translation — full)",
        "tradition": "islamic", "category": "dualistic", "sphere": "greek",
        "language": "modern_greek", "register": "modern",
        "source": {"type": "quranenc_greek_rwwad", "url": qu},
        "license": "QuranEnc.com (Rowad Translation Center); re-publishable with attribution",
        "notes": "REGISTER COMPROMISE: no ancient-Greek Quran exists; this is a MODERN Greek translation. Use only as a modern-register reference, not as an ancient-Greek anchor. Translation contains occasional inline parenthetical glosses (kept verbatim).",
    })

    # ---- P2: Classical Chinese Bible (Wenli Union 1919) ----
    print("[P2] Classical Chinese Bible — Wenli Union Version 1919 (文理和合)")
    for book, title in (("john", "聖經 (文理和合)/約翰福音 (Gospel of John, Literary/Wenli Chinese)"),
                        ("gen", "聖經 (文理和合)/創世記 (Genesis, Literary/Wenli Chinese)"),
                        ("ecc", "聖經 (文理和合)/傳道書 (Ecclesiastes, Literary/Wenli Chinese)")):
        v, su = fetch_wenli_book(book)
        record("chineseclassical", book, "classical", v, {
            "id": f"chineseclassical_{book}", "title": title,
            "tradition": "christian" if book == "john" else "jewish",
            "category": "dualistic", "sphere": "chinese",
            "language": "classical_chinese", "register": "classical",
            "source": {"type": "zh_wikisource_wenli_union_1919", "url": su},
            "license": "pd",
            "notes": "Wenli (Literary) Union Version, 1919 — classical-Chinese register. All three books from one edition. Proper-name templates {{ul}}/{{du}} unwrapped to plain text.",
        })

    # ---- report ----
    print("\n| langkey | book | register | n_verses | char_count | target_script_pct | source |")
    print("|---|---|---|---|---|---|---|")
    for lk, bk, reg, n, ch, pct, src in rows:
        print(f"| {lk} | {bk} | {reg} | {n} | {ch} | {pct} | {src} |")


if __name__ == "__main__":
    main()
