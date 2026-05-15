"""
Fetch books listed in corpus/books_manifest.json.

Supported source types:
  - gutenberg: simple HTTP GET of the .txt URL
  - arxiv: fetches the abstract page and follows to PDF (needs pdf extractor)
  - web: simple HTTP GET (HTML; needs HTML stripper)
  - manual: skipped — print a note that the user must fetch manually

Output:
  corpus/books/raw/<book_id>.{txt,html,pdf}   raw downloaded file
  corpus/books/raw/<book_id>.meta.json        copy of manifest entry + fetch info

Usage:
  python scripts/fetch_books.py                # fetch all gutenberg books in manifest
  python scripts/fetch_books.py --id plotinus_enneads_mackenna,taote_legge
  python scripts/fetch_books.py --types gutenberg,arxiv
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "corpus" / "books_manifest.json"
RAW_DIR = REPO_ROOT / "corpus" / "books" / "raw"

USER_AGENT = "ThinkOutsideTheBox-Research/0.1 (https://github.com/RedbirdSoftwareLLC/thinkoutsidethebox)"


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


FETCHERS = {
    "gutenberg": (fetch_gutenberg, "txt"),
    "arxiv": (fetch_arxiv, "pdf"),
    "web": (fetch_web, "html"),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", default=None, help="Comma-separated book IDs to fetch")
    parser.add_argument(
        "--types",
        default="gutenberg,arxiv,web",
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
