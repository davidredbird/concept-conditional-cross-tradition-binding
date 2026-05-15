"""
Verify the books manifest by checking that PG IDs return books matching the
expected title/author.

For each Gutenberg entry, fetches the /ebooks/{id} metadata page, extracts the
title, and does fuzzy matching against the manifest entry's title/author.
Prints OK/MISMATCH/ERROR per entry and writes a verification report.

This catches the failure mode where we put a wrong PG ID in the manifest and
end up downloading something completely unrelated.

Usage:
  python scripts/verify_manifest.py
  python scripts/verify_manifest.py --fix-broken   # marks broken entries with _broken: true
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "corpus" / "books_manifest.json"
REPORT_PATH = REPO_ROOT / "corpus" / "manifest_verification.txt"

USER_AGENT = "ThinkOutsideTheBox-Research/0.1"


def fetch_pg_title(pg_id: str) -> str | None:
    url = f"https://www.gutenberg.org/ebooks/{pg_id}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"__ERROR__: {type(e).__name__}: {e}"
    m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if not m:
        return None
    title = m.group(1).strip()
    title = re.sub(r"\s*\|\s*Project Gutenberg\s*$", "", title)
    return title


def tokens(s: str) -> set[str]:
    """Lowercased alphanumeric tokens of length >= 3."""
    return {w for w in re.findall(r"[a-z]{3,}", s.lower())}


def title_matches(expected_title: str, expected_author: str, actual: str) -> tuple[bool, float]:
    """Loose match: fraction of expected-tokens present in actual."""
    exp_toks = tokens(expected_title) | tokens(expected_author)
    # Drop common skip-words
    exp_toks -= {"the", "and", "his", "her", "their", "from", "with", "translated", "translator",
                 "edition", "selections", "selected", "anonymous", "various"}
    if not exp_toks:
        return True, 1.0
    act_toks = tokens(actual)
    overlap = len(exp_toks & act_toks)
    score = overlap / max(len(exp_toks), 1)
    return score >= 0.4, score


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix-broken", action="store_true",
                        help="Mark broken PG entries with _broken: true in the manifest")
    parser.add_argument("--delay", type=float, default=0.7)
    args = parser.parse_args()

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    books = manifest["books"]

    results: list[dict] = []
    for b in books:
        src = b["source"]
        if src["type"] != "gutenberg":
            results.append({**b, "_verify": {"status": "skipped (non-gutenberg)"}})
            continue

        pg_id = src.get("id")
        if not pg_id:
            results.append({**b, "_verify": {"status": "skipped (no id)"}})
            continue

        actual_title = fetch_pg_title(pg_id)
        if actual_title is None:
            results.append({**b, "_verify": {"status": "error", "msg": "no title in page"}})
        elif actual_title.startswith("__ERROR__"):
            results.append({**b, "_verify": {"status": "error", "msg": actual_title}})
        else:
            ok, score = title_matches(b["title"], b["author"], actual_title)
            results.append({
                **b,
                "_verify": {
                    "status": "ok" if ok else "MISMATCH",
                    "score": round(score, 2),
                    "actual_title": actual_title,
                },
            })
        time.sleep(args.delay)

    # Print summary
    print(f"{'ID':<40} {'Status':<12} {'Score':<6} {'Actual title (truncated)'}")
    print("-" * 130)
    n_ok = n_mm = n_err = n_skip = 0
    lines = []
    for r in results:
        v = r["_verify"]
        st = v["status"]
        sc = v.get("score", "")
        at = v.get("actual_title", v.get("msg", ""))
        line = f"{r['id']:<40} {st:<12} {str(sc):<6} {at[:60]}"
        print(line)
        lines.append(line)
        if st == "ok":
            n_ok += 1
        elif st == "MISMATCH":
            n_mm += 1
        elif st == "error":
            n_err += 1
        else:
            n_skip += 1

    summary = f"\nSummary:  ok={n_ok}  mismatched={n_mm}  errors={n_err}  skipped={n_skip}  total={len(results)}"
    print(summary)
    REPORT_PATH.write_text("\n".join(lines) + summary, encoding="utf-8")
    print(f"\nReport: {REPORT_PATH}")

    if args.fix_broken:
        # Write a new manifest marking mismatched entries
        for b, r in zip(books, results):
            if r["_verify"]["status"] == "MISMATCH":
                b["_broken"] = True
                b["_broken_reason"] = f"actual PG title was: {r['_verify'].get('actual_title')}"
        MANIFEST_PATH.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"Manifest updated: broken entries marked")


if __name__ == "__main__":
    main()
