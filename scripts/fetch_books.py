"""
Fetch books listed in corpus/books_manifest.json.

Supported source types:
  - gutenberg: simple HTTP GET of the .txt URL
  - arxiv: fetches the abstract page and follows to PDF (needs pdf extractor)
  - web: simple HTTP GET (HTML; needs HTML stripper). Used for GRETIL and ctext.org
        single-page sources.
  - archive_org: plaintext from Internet Archive item (uses {id}_djvu.txt by default,
                 or explicit `url` from manifest if provided)
  - sacred_texts: multi-chapter HTML book from sacred-texts.com. Fetches index.htm,
                  extracts chapter links by regex, fetches and concatenates all
                  chapter HTML files.
  - suttacentral_api: Pali / Sanskrit source text from SuttaCentral's JSON API.
                  Manifest specifies a list of segment ranges (e.g., dhp1-20,
                  dhp21-32, ...) and a URL template. Fetcher iterates segments,
                  extracts `root_text` values in `keys_order`, concatenates as
                  plain UTF-8 text.
  - manual: skipped — print a note that the user must fetch manually

Output:
  corpus/books/raw/<book_id>.{txt,html,pdf}   raw downloaded file
  corpus/books/raw/<book_id>.meta.json        copy of manifest entry + fetch info

Usage:
  python scripts/fetch_books.py                # fetch all books in manifest (default types)
  python scripts/fetch_books.py --id plotinus_enneads_mackenna,taote_legge
  python scripts/fetch_books.py --types gutenberg,arxiv,archive_org,sacred_texts
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "corpus" / "books_manifest.json"
RAW_DIR = REPO_ROOT / "corpus" / "books" / "raw"

USER_AGENT = "CCB-Research/0.1 (https://github.com/davidredbird/concept-conditional-cross-tradition-binding)"


def http_get(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def fetch_gutenberg(book: dict, out_path: Path) -> dict:
    url = book["source"]["url"]
    data = http_get(url)
    out_path.write_bytes(data)
    return {"fetched_url": url, "size_bytes": len(data), "format": "txt"}


def fetch_arxiv(book: dict, out_path: Path) -> dict:
    """Fetch the arxiv PDF. Note: text extraction happens in clean step."""
    abs_url = book["source"]["url"]
    # arxiv abs URL → pdf URL
    if "/abs/" in abs_url:
        pdf_url = abs_url.replace("/abs/", "/pdf/")
        if not pdf_url.endswith(".pdf"):
            pdf_url = pdf_url + ".pdf"
    else:
        pdf_url = abs_url
    data = http_get(pdf_url)
    out_path.write_bytes(data)
    return {"fetched_url": pdf_url, "size_bytes": len(data), "format": "pdf"}


def fetch_web(book: dict, out_path: Path) -> dict:
    url = book["source"]["url"]
    data = http_get(url)
    out_path.write_bytes(data)
    return {"fetched_url": url, "size_bytes": len(data), "format": "html"}


def fetch_archive_org(book: dict, out_path: Path) -> dict:
    """Fetch plaintext from an Internet Archive item.

    Manifest schema:
      "source": {
        "type": "archive_org",
        "id": "<archive-org-identifier>",
        "url": "<optional explicit text URL — overrides default _djvu.txt>"
      }

    If `url` is provided, fetch it directly. Otherwise construct the standard
    OCR plaintext URL: https://archive.org/download/{id}/{id}_djvu.txt
    """
    src = book["source"]
    identifier = src["id"]
    url = src.get("url") or f"https://archive.org/download/{identifier}/{identifier}_djvu.txt"
    data = http_get(url)
    out_path.write_bytes(data)
    return {"fetched_url": url, "size_bytes": len(data), "format": "txt"}


_CHAPTER_HREF_RE = re.compile(r'href=["\']([^"\'#?]+\.htm)["\']', re.IGNORECASE)


def fetch_sacred_texts(book: dict, out_path: Path) -> dict:
    """Fetch a multi-chapter book from sacred-texts.com.

    Manifest schema:
      "source": {
        "type": "sacred_texts",
        "id": "<section>/<book>",
        "url": "https://www.sacred-texts.com/<section>/<book>/index.htm"
      }

    Strategy: fetch the index page, regex out all .htm links in the same directory,
    fetch each, concatenate. Saved as a single HTML file with comment markers for
    chapter boundaries. clean_books.py handles HTML stripping downstream.
    """
    src = book["source"]
    index_url = src["url"]
    base = index_url.rsplit("/", 1)[0] + "/"

    index_html = http_get(index_url).decode("utf-8", errors="replace")

    seen = set()
    chapter_urls: list[str] = []
    for href in _CHAPTER_HREF_RE.findall(index_html):
        if href.startswith(("http://", "https://", "../", "/")):
            continue
        if href.lower() in ("index.htm", "errata.htm"):
            continue
        if href in seen:
            continue
        seen.add(href)
        chapter_urls.append(urljoin(base, href))

    parts: list[str] = [f"<!-- INDEX: {index_url} -->\n", index_html]
    n_ok = 0
    n_fail = 0
    for chapter_url in chapter_urls:
        try:
            chapter_data = http_get(chapter_url).decode("utf-8", errors="replace")
            parts.append(f"<!-- CHAPTER: {chapter_url} -->\n")
            parts.append(chapter_data)
            n_ok += 1
            time.sleep(0.5)
        except Exception as e:
            parts.append(f"<!-- CHAPTER FETCH FAILED: {chapter_url} - {type(e).__name__}: {e} -->\n")
            n_fail += 1

    combined = "\n\n".join(parts)
    out_path.write_text(combined, encoding="utf-8")
    return {
        "fetched_url": index_url,
        "size_bytes": len(combined.encode("utf-8")),
        "format": "html",
        "n_chapters_ok": n_ok,
        "n_chapters_failed": n_fail,
        "n_chapters_found": len(chapter_urls),
    }


def fetch_suttacentral_api(book: dict, out_path: Path) -> dict:
    """Fetch original-language text from SuttaCentral's JSON API.

    Manifest schema:
      "source": {
        "type": "suttacentral_api",
        "id": "<sutta_uid>",
        "url": "https://suttacentral.net/api/bilarasuttas/{segment}/pli",
        "segments": ["dhp1-20", "dhp21-32", ..., "dhp383-423"]
      }

    Strategy: for each segment, fetch the JSON, extract root_text values in
    keys_order, concatenate. The result is plain UTF-8 text with whitespace
    between segments (Pali source text for the configured language).
    """
    import json as _json
    src = book["source"]
    url_template = src["url"]
    segments = src["segments"]

    parts: list[str] = []
    n_segments_ok = 0
    n_segments_failed = 0
    n_text_chunks = 0

    for seg in segments:
        url = url_template.format(segment=seg)
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            obj = _json.loads(data.decode("utf-8"))
            keys_order = obj.get("keys_order", [])
            root_text = obj.get("root_text", {})

            parts.append(f"\n\n<!-- SEGMENT: {seg} (URL: {url}) -->\n")
            for k in keys_order:
                text = root_text.get(k, "")
                if text:
                    parts.append(text)
                    n_text_chunks += 1
            n_segments_ok += 1
            time.sleep(0.3)
        except Exception as e:
            parts.append(f"\n<!-- SEGMENT FETCH FAILED: {seg} ({url}) - {type(e).__name__}: {e} -->\n")
            n_segments_failed += 1

    combined = "".join(parts)
    out_path.write_text(combined, encoding="utf-8")
    return {
        "fetched_url": url_template,
        "size_bytes": len(combined.encode("utf-8")),
        "format": "txt",
        "n_segments_ok": n_segments_ok,
        "n_segments_failed": n_segments_failed,
        "n_text_chunks": n_text_chunks,
        "n_segments_requested": len(segments),
    }


FETCHERS = {
    "gutenberg": (fetch_gutenberg, "txt"),
    "arxiv": (fetch_arxiv, "pdf"),
    "web": (fetch_web, "html"),
    "archive_org": (fetch_archive_org, "txt"),
    "sacred_texts": (fetch_sacred_texts, "html"),
    "suttacentral_api": (fetch_suttacentral_api, "txt"),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", default=None, help="Comma-separated book IDs to fetch")
    parser.add_argument(
        "--types",
        default="gutenberg,arxiv,web,archive_org,sacred_texts,suttacentral_api",
        help="Comma-separated source types to fetch",
    )
    parser.add_argument("--force", action="store_true", help="Re-fetch even if cached")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds between requests")
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    books = manifest["books"]

    if args.id:
        ids = {x.strip() for x in args.id.split(",")}
        books = [b for b in books if b["id"] in ids]
    types_filter = {x.strip() for x in args.types.split(",")}

    n_fetched = 0
    n_skipped = 0
    n_failed = 0
    n_manual = 0

    for book in books:
        bid = book["id"]
        stype = book["source"]["type"]

        if stype == "manual":
            print(f"[manual]    {bid}  needs manual fetch -- skipping")
            n_manual += 1
            continue

        if stype not in types_filter:
            continue

        fetcher_info = FETCHERS.get(stype)
        if fetcher_info is None:
            print(f"[unknown]   {bid}  unknown source type: {stype}")
            n_failed += 1
            continue
        fetcher, ext = fetcher_info

        out_path = RAW_DIR / f"{bid}.{ext}"
        meta_path = RAW_DIR / f"{bid}.meta.json"

        if out_path.exists() and not args.force:
            print(f"[cached]    {bid}  {out_path.name} ({out_path.stat().st_size} bytes)")
            n_skipped += 1
            continue

        try:
            print(f"[fetching]  {bid}  <- {book['source']['url']}")
            fetch_info = fetcher(book, out_path)
            meta = {**book, "_fetch": fetch_info}
            meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
            print(f"[ok]        {bid}  {fetch_info['size_bytes']:>9} bytes")
            n_fetched += 1
            time.sleep(args.delay)
        except Exception as e:
            print(f"[fail]      {bid}  {type(e).__name__}: {e}")
            n_failed += 1

    print(f"\nDone. fetched={n_fetched}  cached={n_skipped}  manual={n_manual}  failed={n_failed}")


if __name__ == "__main__":
    main()
