"""
Clean raw downloaded book files into prose-only text.

  - Project Gutenberg: strip license header/footer, find the START/END markers,
    strip Roman-numeral chapter titles, normalize whitespace.
  - arxiv PDFs: extract text (pdftotext fallback to PyPDF2/pypdf).
  - HTML: extract text via html.parser.

Output: corpus/books/cleaned/<book_id>.txt + corpus/books/cleaned/<book_id>.meta.json
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "corpus" / "books" / "raw"
CLEAN_DIR = REPO_ROOT / "corpus" / "books" / "cleaned"

# Project Gutenberg standard markers
PG_START = re.compile(
    r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG EBOOK[^*]*\*\*\*",
    flags=re.IGNORECASE,
)
PG_END = re.compile(
    r"\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG EBOOK[^*]*\*\*\*",
    flags=re.IGNORECASE,
)


def clean_gutenberg(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace")

    # Strip header/footer using markers
    m = PG_START.search(text)
    if m:
        text = text[m.end() :]
    m = PG_END.search(text)
    if m:
        text = text[: m.start()]

    # PG transcribers often add an "End of the Project Gutenberg" or "PRODUCED BY"
    # signature outside markers; we already cut at markers so this is usually fine.

    # Strip Phase 1c segment markers added by the suttacentral_api fetcher
    # (e.g., '<!-- SEGMENT: dhp1-20 (URL: ...) -->' or
    # '<!-- SEGMENT FETCH FAILED: ... -->'). These are not source content.
    text = re.sub(r"<!--\s*SEGMENT[^>]*-->", "", text)

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Collapse 3+ blank lines into 2 (paragraph break)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def clean_pdf(raw_path: Path) -> str:
    """Extract text from a PDF. Prefer pdftotext (poppler); fall back to pypdf."""
    # Try pdftotext binary first
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(raw_path), "-"],
            capture_output=True,
            timeout=120,
            check=True,
        )
        return result.stdout.decode("utf-8", errors="replace")
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    # Fall back to pypdf if available
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(raw_path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages)
    except ImportError:
        pass

    raise RuntimeError(
        f"Cannot extract text from {raw_path}: install poppler (pdftotext) "
        "or 'pip install pypdf' in the venv."
    )


class _HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip = False

    def handle_starttag(self, tag: str, attrs):
        if tag in {"script", "style", "noscript"}:
            self.skip = True

    def handle_endtag(self, tag: str):
        if tag in {"script", "style", "noscript"}:
            self.skip = False
        elif tag in {"p", "br", "div", "h1", "h2", "h3", "h4", "li"}:
            self.parts.append("\n")

    def handle_data(self, data: str):
        if not self.skip:
            self.parts.append(data)


def clean_html(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace")
    parser = _HTMLTextExtractor()
    parser.feed(text)
    out = "".join(parser.parts)
    out = html.unescape(out)
    out = re.sub(r"[ \t]+", " ", out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()


def normalize_prose(text: str) -> str:
    """Generic post-clean: collapse excess whitespace, normalize quotes."""
    text = text.replace(" ", " ")  # non-breaking spaces
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" +\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Curly quotes / fancy dashes → ASCII equivalents
    text = (
        text.replace("‘", "'")
        .replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("—", "--")
        .replace("–", "-")
        .replace("…", "...")
    )
    return text.strip()


def clean_one(book_id: str) -> dict | None:
    meta_path = RAW_DIR / f"{book_id}.meta.json"
    if not meta_path.exists():
        print(f"[skip]      {book_id}  no meta — not fetched")
        return None

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    fmt = meta.get("_fetch", {}).get("format")
    raw_path = RAW_DIR / f"{book_id}.{fmt}"

    if not raw_path.exists():
        print(f"[skip]      {book_id}  raw file missing: {raw_path.name}")
        return None

    try:
        if fmt == "txt":
            text = clean_gutenberg(raw_path.read_bytes())
        elif fmt == "pdf":
            text = clean_pdf(raw_path)
        elif fmt == "html":
            text = clean_html(raw_path.read_bytes())
        else:
            print(f"[skip]      {book_id}  unknown format: {fmt}")
            return None

        text = normalize_prose(text)
    except Exception as e:
        print(f"[fail]      {book_id}  {type(e).__name__}: {e}")
        return None

    out_path = CLEAN_DIR / f"{book_id}.txt"
    out_meta = CLEAN_DIR / f"{book_id}.meta.json"
    out_path.write_text(text, encoding="utf-8")

    # token count estimate (rough: 1 token ≈ 0.75 words)
    word_count = len(text.split())
    token_est = int(word_count / 0.75)
    char_count = len(text)
    out_meta_data = {
        **meta,
        "_clean": {
            "word_count": word_count,
            "char_count": char_count,
            "token_estimate": token_est,
        },
    }
    out_meta.write_text(json.dumps(out_meta_data, indent=2), encoding="utf-8")
    print(
        f"[ok]        {book_id}  words={word_count:>7,}  ~tokens={token_est:>7,}"
    )
    return out_meta_data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", default=None, help="Comma-separated book IDs to clean")
    args = parser.parse_args()

    CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    if args.id:
        ids = [x.strip() for x in args.id.split(",")]
    else:
        ids = [p.name.removesuffix(".meta.json") for p in RAW_DIR.glob("*.meta.json")]

    total_tokens = 0
    n_ok = 0
    n_fail = 0
    for bid in ids:
        result = clean_one(bid)
        if result is not None:
            n_ok += 1
            total_tokens += result["_clean"]["token_estimate"]
        else:
            n_fail += 1

    print(
        f"\nDone. ok={n_ok}  fail/skip={n_fail}  estimated_total_tokens={total_tokens:,}"
    )


if __name__ == "__main__":
    main()
