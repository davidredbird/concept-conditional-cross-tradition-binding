"""
Convert a Markdown file to a styled PDF via Chrome headless.

Usage:
    python scripts/md_to_pdf.py paper/paper-draft.md paper/paper-draft.pdf
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown


CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


CSS = """
@page {
  size: Letter;
  margin: 0.85in 0.85in 0.95in 0.85in;
  @bottom-center {
    content: counter(page) " / " counter(pages);
    font-family: 'Source Sans Pro', 'Helvetica Neue', Arial, sans-serif;
    font-size: 9pt;
    color: #888;
  }
}

html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }

body {
  font-family: 'Source Serif Pro', 'Charter', 'Cambria', Georgia, 'Times New Roman', serif;
  font-size: 10.5pt;
  line-height: 1.45;
  color: #1a1a1a;
  max-width: 7in;
  margin: 0 auto;
  padding: 0;
}

h1, h2, h3, h4 {
  font-family: 'Source Sans Pro', 'Helvetica Neue', 'Segoe UI', Arial, sans-serif;
  color: #111;
  font-weight: 600;
  line-height: 1.25;
  page-break-after: avoid;
}

h1 {
  font-size: 18pt;
  margin: 0 0 0.4em 0;
  border-bottom: 2px solid #222;
  padding-bottom: 0.3em;
}
h2 {
  font-size: 13.5pt;
  margin: 1.6em 0 0.5em 0;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.15em;
}
h3 {
  font-size: 11.5pt;
  margin: 1.3em 0 0.35em 0;
}
h4 {
  font-size: 10.5pt;
  margin: 1.1em 0 0.3em 0;
}

p { margin: 0 0 0.6em 0; text-align: justify; hyphens: auto; }

ul, ol { margin: 0.2em 0 0.7em 0; padding-left: 1.4em; }
li { margin-bottom: 0.18em; }

strong { color: #000; }
em { color: #333; }

code {
  font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
  font-size: 9.2pt;
  background: #f3f3f3;
  padding: 0.05em 0.3em;
  border-radius: 2px;
}
pre {
  background: #f5f5f5;
  padding: 0.7em 0.9em;
  font-size: 9pt;
  border-left: 3px solid #999;
  overflow-x: auto;
  page-break-inside: avoid;
}

blockquote {
  border-left: 3px solid #bbb;
  margin: 0.7em 0;
  padding: 0.1em 0 0.1em 1em;
  color: #555;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 0.7em 0;
  font-size: 9.2pt;
  page-break-inside: avoid;
}
th, td {
  border: 1px solid #c4c4c4;
  padding: 0.32em 0.55em;
  text-align: left;
  vertical-align: top;
}
th {
  background: #ececec;
  font-family: 'Source Sans Pro', 'Helvetica Neue', Arial, sans-serif;
  font-weight: 600;
}
tr:nth-child(even) td { background: #fafafa; }

hr {
  border: none;
  border-top: 1px solid #ccc;
  margin: 1.5em 0;
}

/* Title-block first horizontal rule looks heavier */
body > hr:first-of-type { display: none; }

/* Make the lead "Preliminary preprint" block stand out */
body > p:first-of-type {
  font-size: 10pt;
  color: #555;
}
"""


def find_chrome() -> str:
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).is_file():
            return candidate
    raise RuntimeError("No Chrome or Edge installation found.")


def md_to_html(md_path: Path, css: str) -> str:
    text = md_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list", "footnotes"],
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{md_path.stem}</title>
<style>{css}</style>
</head>
<body>
{html_body}
</body>
</html>
"""


def html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    chrome = find_chrome()
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, timeout=180)


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python md_to_pdf.py <input.md> <output.pdf>", file=sys.stderr)
        sys.exit(2)
    md_path = Path(sys.argv[1]).resolve()
    pdf_path = Path(sys.argv[2]).resolve()
    if not md_path.is_file():
        print(f"Markdown file not found: {md_path}", file=sys.stderr)
        sys.exit(1)

    html = md_to_html(md_path, CSS)
    with tempfile.TemporaryDirectory() as td:
        html_path = Path(td) / (md_path.stem + ".html")
        html_path.write_text(html, encoding="utf-8")
        html_to_pdf(html_path, pdf_path)
    print(f"Wrote {pdf_path} ({pdf_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
