"""
Chunk cleaned books into ~500-token passages with metadata.

Output: corpus/chunks.jsonl  one record per chunk:
  {
    "id": "<book_id>::<chunk_index>",
    "book_id": "<book_id>",
    "tradition": "...",
    "category": "...",
    "author": "...",
    "translator": "...",
    "era": "...",
    "chunk_index": 0,
    "char_start": 0,
    "char_end": 1234,
    "token_estimate": 502,
    "text": "..."
  }

Chunking strategy:
  - Split on paragraph breaks (blank lines).
  - Pack paragraphs together until token budget is reached.
  - Soft target: 500 tokens, hard cap: 700 tokens.
  - If a single paragraph exceeds the cap, split it at sentence boundaries.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLEAN_DIR = REPO_ROOT / "corpus" / "books" / "cleaned"
OUT_PATH = REPO_ROOT / "corpus" / "chunks.jsonl"

TARGET_TOKENS = 500
HARD_CAP = 700

# Rough estimator: words / 0.75 ≈ tokens
def estimate_tokens(text: str) -> int:
    return int(len(text.split()) / 0.75)


SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'\[(])")


def split_paragraph_into_sentences(p: str) -> list[str]:
    return [s.strip() for s in SENT_SPLIT.split(p) if s.strip()]


def pack_paragraphs(paragraphs: list[str], target: int, hard_cap: int) -> list[str]:
    """
    Pack paragraphs into chunks, soft-targeting `target` tokens, never exceeding
    `hard_cap`. Oversized paragraphs are split at sentence boundaries.
    """
    chunks: list[str] = []
    current_parts: list[str] = []
    current_tokens = 0

    def flush():
        nonlocal current_parts, current_tokens
        if current_parts:
            chunks.append("\n\n".join(current_parts).strip())
            current_parts = []
            current_tokens = 0

    for para in paragraphs:
        ptok = estimate_tokens(para)

        if ptok > hard_cap:
            # Oversized paragraph: split into sentences, pack sentence-wise
            flush()
            sents = split_paragraph_into_sentences(para)
            sub_parts: list[str] = []
            sub_tokens = 0
            for s in sents:
                stok = estimate_tokens(s)
                if sub_tokens + stok > hard_cap and sub_parts:
                    chunks.append(" ".join(sub_parts).strip())
                    sub_parts = [s]
                    sub_tokens = stok
                else:
                    sub_parts.append(s)
                    sub_tokens += stok
            if sub_parts:
                chunks.append(" ".join(sub_parts).strip())
            continue

        if current_tokens + ptok > hard_cap and current_parts:
            flush()
            current_parts = [para]
            current_tokens = ptok
        elif current_tokens >= target and current_parts:
            flush()
            current_parts = [para]
            current_tokens = ptok
        else:
            current_parts.append(para)
            current_tokens += ptok

    flush()
    return [c for c in chunks if c]


def chunk_one_book(book_id: str) -> list[dict]:
    txt_path = CLEAN_DIR / f"{book_id}.txt"
    meta_path = CLEAN_DIR / f"{book_id}.meta.json"

    if not txt_path.exists() or not meta_path.exists():
        return []

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    text = txt_path.read_text(encoding="utf-8")

    # Paragraph split
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks_text = pack_paragraphs(paragraphs, TARGET_TOKENS, HARD_CAP)

    out: list[dict] = []
    char_cursor = 0
    for i, ctext in enumerate(chunks_text):
        # find approximate char range (best-effort)
        idx = text.find(ctext[:80], char_cursor)
        char_start = idx if idx >= 0 else char_cursor
        char_end = char_start + len(ctext)
        char_cursor = char_end

        out.append(
            {
                "id": f"{book_id}::{i:04d}",
                "book_id": book_id,
                "source_id": meta.get("source_id"),
                "tradition": meta["tradition"],
                "category": meta["category"],
                "author": meta["author"],
                "translator": meta.get("translator"),
                "era": meta.get("era"),
                "language": meta.get("language", "english"),
                "chunk_index": i,
                "char_start": char_start,
                "char_end": char_end,
                "token_estimate": estimate_tokens(ctext),
                "text": ctext,
            }
        )

    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--id", default=None, help="Comma-separated book IDs to chunk (default: all cleaned)"
    )
    parser.add_argument("--out", type=Path, default=OUT_PATH)
    args = parser.parse_args()

    if args.id:
        ids = [x.strip() for x in args.id.split(",")]
    else:
        ids = sorted(p.stem for p in CLEAN_DIR.glob("*.txt"))

    total_chunks = 0
    total_tokens = 0
    by_book: dict[str, int] = {}

    with args.out.open("w", encoding="utf-8") as f:
        for bid in ids:
            chunks = chunk_one_book(bid)
            for c in chunks:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
            by_book[bid] = len(chunks)
            total_chunks += len(chunks)
            total_tokens += sum(c["token_estimate"] for c in chunks)
            print(f"[chunked]   {bid}  {len(chunks):>4} chunks")

    print(
        f"\nWrote {total_chunks:,} chunks  (~{total_tokens:,} tokens)  to {args.out}"
    )
    print(f"\nPer-book chunk counts:")
    for bid in sorted(by_book):
        print(f"  {bid:<40} {by_book[bid]:>5}")


if __name__ == "__main__":
    main()
