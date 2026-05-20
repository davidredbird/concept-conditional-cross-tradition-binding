"""
Option A multilingual concept tagger: manual Sanskrit/Pali regex dictionaries.

The Phase 1c first pass found that Option B (English-prototype embedding) tagging
fails to transfer across language boundaries (Cohen's kappa ~ 0 vs manual
dictionaries; see findings/phase1c-multilingual.md). This script implements the
Option A confirmatory tagger: hand-curated Sanskrit (Devanagari + IAST) and Pali
(Latin transliteration) term lists per concept, applied by regex.

Lexical sourcing and caveats:
  - Term-concept associations are drawn from standard scholarly references:
    Monier-Williams Sanskrit-English Dictionary, the Pali Text Society
    Pali-English Dictionary, and standard comparative-philosophy usage.
  - The investigator is not a Sanskrit/Pali philologist; these dictionaries are
    constructed from glossary-level associations, not expert annotation. This is
    a hidden-degree-of-freedom limitation analogous to the English regex tagging
    (paper §9 limitation 3), more acute for non-English. It should be reported
    as such, and ideally validated by held-out expert tagging in future work.
  - Theological asymmetries between Advaita (Sanskrit) and Theravada (Pali) are
    real and deliberately preserved rather than forced into false symmetry:
      * ULTIMATE: Advaita has Brahman / Ishvara / Paramatman; Theravada has no
        creator-deity or absolute substance. The closest Theravada terms are the
        "unconditioned" (asaṅkhata), "deathless" (amata), and nibbāna-as-
        unconditioned. This asymmetry mirrors the Phase 1a/§6.8 ULTIMATE
        coverage-asymmetry finding and is expected to limit cross-tradition
        ULTIMATE binding.
      * NONSEP (non-duality): advaita/advaya is a Hindu/Mahayana technical term;
        Theravada does not frame liberation as non-dual. Expected near-zero Pali
        coverage.
      * SELF: Advaita affirms atman; Theravada's central doctrine is anattā
        (non-self). Both reference the self-concept, but with opposite valence.

Devanagari terms are matched as plain substrings (Python re \\b is ASCII-word
oriented and unreliable at Devanagari boundaries). Latin/Pali terms use \\b and
tolerate diacritic variants via character classes.

Output: augmented chunks with an `option_a_concepts` field. English chunks are
left untagged by this script (Phase 1c.2 is Sanskrit-Pali only); their existing
regex tags are used for English analyses elsewhere.

Usage:
  python scripts/multilingual_option_a_tagger.py \\
    --chunks corpus/chunks_with_multilingual_tags_intfloat__multilingual_e5_large.jsonl \\
    --out corpus/chunks_with_option_a_tags.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


# Each concept maps language -> list of regex patterns.
# Devanagari (sanskrit): plain substring patterns (Devanagari word boundaries
#   are unreliable with ASCII-oriented \b; substrings catch inflected forms).
# Latin/Pali transliteration: leading \b only, NO trailing \b — Pali and
#   Sanskrit are heavily inflected (nibbāna -> nibbānaṁ, nibbāne, nibbānassa;
#   samādhi -> samādhiṁ). A trailing \b fails on the inflectional ending and
#   silently drops nearly all matches (the bug found in the first Option A run:
#   the Pali corpus has 30 "nibb" occurrences but \bnibbāna\b matched 0). Stem-
#   prefix matching catches inflected forms. Stems chosen are distinctive enough
#   that prefix over-matching is negligible for these religious-technical terms.
MANUAL_PATTERNS: dict[str, dict[str, list[str]]] = {
    "ULTIMATE": {
        "sanskrit": [
            r"ब्रह्मन्", r"ब्रह्म", r"परब्रह्म", r"परमात्मन्", r"परमात्मा",
            r"परमेश्वर", r"ईश्वर", r"भगवान्", r"भगवत्", r"पुरुषोत्तम",
            r"अक्षर",
            r"\bbrahma", r"\bparabrahma", r"\bparam[āa]tma", r"\b[īi][śs]vara",
            r"\bbhagav[āa]n", r"\bpuru[șs]ottama", r"\bak[șs]ara",
        ],
        "pali": [
            r"\bparamattha", r"\basa[ńn]khata", r"\bamata",
        ],
    },
    "SUBSTRATE": {
        "sanskrit": [
            r"माया", r"प्रकृति", r"मूलप्रकृति", r"अव्यक्त", r"शून्य",
            r"शून्यता", r"आधार",
            r"\bm[āa]y[āa]", r"\bprak[ŗr]ti", r"\bavyakta",
            r"\b[śs][ūu]nya",
        ],
        "pali": [
            r"\bsu[ńn][ńn]a", r"\bpa[țt]iccasamupp[āa]da", r"\banatt[āa]",
            r"\bsa[ńn]kh[āa]ra",
        ],
    },
    "AWARENESS": {
        "sanskrit": [
            r"चित्", r"चैतन्य", r"चेतना", r"विज्ञान", r"ज्ञान", r"बोध",
            r"प्रज्ञा", r"अनुभव", r"विमर्श", r"संवित्", r"चिति",
            r"\bcaitanya", r"\bcetan[aā]", r"\bvij[ñn][aā]na",
            r"\bbodha", r"\bpraj[ñn][aā]", r"\banubhava", r"\bvimar[śs]a",
        ],
        "pali": [
            r"\bcitta", r"\bvi[ńn][ńn][aā][nṇ]a", r"\bpa[ńn][ńn][aā]",
            r"\b[ńn][aā][nṇ]a", r"\bsati", r"\bsampaja[ńn][ńn]a",
        ],
    },
    "WORLD": {
        "sanskrit": [
            r"जगत्", r"जगति", r"लोक", r"संसार", r"प्रपञ्च", r"विश्व",
            r"भुवन", r"\bjagat", r"\bloka", r"\bsa[mṃ]s[āa]ra",
            r"\bprapa[ñn]ca", r"\bvi[śs]va",
        ],
        "pali": [
            r"\bloka", r"\bsa[mṃ]s[āa]ra", r"\bn[āa]mar[ūu]pa",
        ],
    },
    "SELF": {
        "sanskrit": [
            r"आत्मन्", r"आत्मा", r"जीव", r"जीवात्मन्", r"अहंकार", r"अहम्",
            r"\b[āa]tman", r"\bj[īi]va", r"\baha[mṃ]k[āa]ra",
        ],
        "pali": [
            r"\batt[āa]", r"\banatt[āa]", r"\baha[mṃ]k[āa]ra", r"\bsakk[āa]ya",
        ],
    },
    "RECOGNITION": {
        "sanskrit": [
            r"मोक्ष", r"मुक्ति", r"कैवल्य", r"निर्वाण", r"जीवन्मुक्ति",
            r"बोधि", r"समाधि", r"प्रत्यभिज्ञा", r"सिद्धि", r"मुमुक्षु",
            r"\bmok[șs]a", r"\bmukti", r"\bkaivalya", r"\bnirv[āa][nṇ]a",
            r"\bj[īi]vanmukti", r"\bbodhi", r"\bsam[āa]dhi",
            r"\bpratyabhij[ñn][āa]", r"\bsiddhi",
        ],
        "pali": [
            r"\bnibb[āa]na", r"\bbodhi", r"\bnirodha", r"\bmokkha",
            r"\bcetovimutti", r"\bpa[ńn][ńn][āa]vimutti", r"\bvimutti",
            r"\bsam[āa]dhi", r"\barahatta", r"\barahat",
        ],
    },
    "NONSEP": {
        "sanskrit": [
            r"अद्वैत", r"अद्वय", r"अभेद", r"एकत्व",
            r"\badvaita", r"\badvaya", r"\babheda", r"\bekatva",
        ],
        "pali": [
            r"\bekatta",
        ],
    },
}


def tag_chunk(text: str, lang: str) -> list[str]:
    """Return list of concepts whose patterns match in text for the given language."""
    tags = []
    for concept, by_lang in MANUAL_PATTERNS.items():
        patterns = by_lang.get(lang, [])
        for p in patterns:
            try:
                if re.search(p, text, re.IGNORECASE):
                    tags.append(concept)
                    break
            except re.error:
                continue
    return tags


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunks", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "corpus" / "chunks_with_option_a_tags.jsonl")
    parser.add_argument("--calibration-out", type=Path,
                        default=REPO_ROOT / "results" / "phase1c" / "option_a_tag_counts.json")
    args = parser.parse_args()

    chunks = []
    with args.chunks.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    print(f"Loaded {len(chunks):,} chunks")

    concepts = list(MANUAL_PATTERNS.keys())
    # Tag non-English chunks
    counts: dict[tuple[str, str], int] = {}
    lang_counts: dict[str, int] = {}
    for c in chunks:
        lang = c.get("language", "english")
        if lang in ("sanskrit", "pali"):
            tags = tag_chunk(c["text"], lang)
        else:
            tags = []  # Phase 1c.2 is Sanskrit-Pali only
        c["option_a_concepts"] = tags
        lang_counts[lang] = lang_counts.get(lang, 0) + 1
        for t in tags:
            counts[(lang, t)] = counts.get((lang, t), 0) + 1

    # Report
    print()
    print(f"{'language':<12} (n)    " + " ".join(f"{c:>11}" for c in concepts))
    print("-" * (20 + 12 * len(concepts)))
    for lang in ("sanskrit", "pali"):
        n = lang_counts.get(lang, 0)
        row = [f"{lang:<12} ({n:>3})"]
        for concept in concepts:
            ct = counts.get((lang, concept), 0)
            row.append(f"{ct:>4}/{n:<3} ".rjust(11))
        print(" ".join(row))

    # Save
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"\nWrote {args.out}")

    cal = {
        "concepts": concepts,
        "language_chunk_counts": lang_counts,
        "tag_counts_by_language_concept": {f"{l}|{c}": v for (l, c), v in counts.items()},
    }
    args.calibration_out.parent.mkdir(parents=True, exist_ok=True)
    args.calibration_out.write_text(json.dumps(cal, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {args.calibration_out}")


if __name__ == "__main__":
    main()
