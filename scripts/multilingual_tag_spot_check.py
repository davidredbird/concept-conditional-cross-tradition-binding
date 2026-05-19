"""
Option A spot-check on multilingual prototype concept tagging.

Per Phase 1c pre-registration §3.3, before Phase 1c.2 main analysis can be
reported confirmatorily, the Option B prototype tagger must be validated
against manual Sanskrit/Pali regex tagging on two specific concepts:
AWARENESS and RECOGNITION.

Procedure:
  1. Manually-constructed Sanskrit and Pali concept term lists from
     Monier-Williams Sanskrit-English Dictionary and Pali Text Society
     Pali-English Dictionary (committed below).
  2. Regex-tag Sanskrit and Pali chunks in the Phase 1c corpus using these
     manual dictionaries (Option A).
  3. Compare against Option B (prototype-embedding) tags from
     `multilingual_concept_tagger.py`.
  4. Compute Cohen's kappa and percent agreement per concept.

Decision rule (pre-registered):
  - If kappa < 0.5 OR percent agreement < 70% on AWARENESS or RECOGNITION,
    Option B is not validated and Phase 1c.2 is reported as exploratory.
  - If kappa >= 0.5 AND percent agreement >= 70% on both concepts, Option B
    is validated and Phase 1c.2 is reported as confirmatory.

Usage:
  python scripts/multilingual_tag_spot_check.py \\
    --tags corpus/chunks_with_multilingual_tags_intfloat__multilingual_e5_large.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


# Manual Sanskrit + Pali concept regex dictionaries. Each pattern is matched
# case-insensitively against the chunk text. Sanskrit Devanagari terms include
# the canonical Devanagari spelling; Pali terms include both diacritic-bearing
# Latin transliteration and a diacritic-stripped variant for robustness.
#
# AWARENESS (Sanskrit + Pali, hand-curated from scholarly glossaries):
MANUAL_AWARENESS: dict[str, list[str]] = {
    "sanskrit": [
        # Devanagari
        r"चित्",          # cit (consciousness)
        r"चैतन्य",         # caitanya
        r"चेतना",          # cetana
        r"विज्ञान",        # vijñāna
        r"ज्ञान",          # jñāna (also matches knowledge contexts)
        r"बोध",           # bodha
        r"प्रज्ञा",        # prajñā
        r"अनुभव",          # anubhava
        r"विमर्श",         # vimarśa
        # Common IAST transliterations (also present in some hybrid sources)
        r"\bcit\b",
        r"\bcaitanya\b",
        r"\bcetan[aā]\b",
        r"\bvij[ñn][aā]na\b",
        r"\bbodha\b",
        r"\bpraj[ñn][aā]\b",
        r"\banubhava\b",
        r"\bvimar[śs]a\b",
    ],
    "pali": [
        # Pali on SuttaCentral uses Latin transliteration with diacritics
        r"\bcitta\b",
        r"\bvi[ñn][ñn][aā][nṇ]a\b",   # viññāṇa
        r"\bpa[ñn][ñn][aā]\b",         # paññā
        r"\b[ñn][aā][nṇ]a\b",          # ñāṇa
        r"\bsati\b",
        r"\bsampaja[ñn][ñn]a\b",       # sampajañña
    ],
}

# RECOGNITION (liberation, awakening, realization terms):
MANUAL_RECOGNITION: dict[str, list[str]] = {
    "sanskrit": [
        r"मोक्ष",          # moksha
        r"मुक्ति",         # mukti
        r"कैवल्य",         # kaivalya
        r"निर्वाण",        # nirvāṇa
        r"जीवन्मुक्ति",     # jīvanmukti
        r"बोधि",           # bodhi
        r"समाधि",          # samādhi
        r"प्रत्यभिज्ञा",    # pratyabhijñā
        r"सिद्धि",         # siddhi
        # IAST equivalents
        r"\bmok[śs]a\b",
        r"\bmukti\b",
        r"\bkaivalya\b",
        r"\bnirv[āa][nṇ]a\b",
        r"\bj[īi]vanmukti\b",
        r"\bbodhi\b",
        r"\bsam[āa]dhi\b",
        r"\bpratyabhij[ñn][aā]\b",
        r"\bsiddhi\b",
    ],
    "pali": [
        r"\bnibb[āa]na\b",
        r"\bbodhi\b",
        r"\bnirodha\b",
        r"\bmokkha\b",
        r"\bcetovimutti\b",
        r"\bpa[ñn][ñn][aā]vimutti\b",
        r"\bsam[āa]dhi\b",
    ],
}


def regex_tag_any(text: str, patterns: list[str]) -> bool:
    for p in patterns:
        try:
            if re.search(p, text, re.IGNORECASE):
                return True
        except re.error:
            continue
    return False


def cohen_kappa(a: list[bool], b: list[bool]) -> float:
    """Compute Cohen's kappa for two boolean rater arrays of equal length."""
    n = len(a)
    if n == 0 or n != len(b):
        return float("nan")
    n_both_yes = sum(1 for i in range(n) if a[i] and b[i])
    n_both_no = sum(1 for i in range(n) if not a[i] and not b[i])
    p_o = (n_both_yes + n_both_no) / n
    p_a_yes = sum(a) / n
    p_b_yes = sum(b) / n
    p_e = p_a_yes * p_b_yes + (1 - p_a_yes) * (1 - p_b_yes)
    if p_e >= 1.0:
        return float("nan")
    return (p_o - p_e) / (1 - p_e)


def evaluate_concept(
    chunks: list[dict],
    concept: str,
    manual: dict[str, list[str]],
) -> dict:
    """Compare Option A (manual regex) vs Option B (prototype tag) for one concept
    on non-English chunks. Reports per-language and combined metrics.
    """
    results = {"concept": concept, "per_language": {}, "combined": None}
    combined_a, combined_b = [], []
    for lang in ("sanskrit", "pali"):
        if lang not in manual:
            continue
        patterns = manual[lang]
        idxs = [i for i, c in enumerate(chunks) if c.get("language") == lang]
        if not idxs:
            continue
        a_tags = []
        b_tags = []
        for i in idxs:
            text = chunks[i]["text"]
            a_tag = regex_tag_any(text, patterns)
            b_tag = concept in (chunks[i].get("multilingual_concepts") or [])
            a_tags.append(a_tag)
            b_tags.append(b_tag)
        a_count = sum(a_tags)
        b_count = sum(b_tags)
        agree = sum(1 for x, y in zip(a_tags, b_tags) if x == y)
        kappa = cohen_kappa(a_tags, b_tags)
        results["per_language"][lang] = {
            "n_chunks": len(idxs),
            "option_a_tagged": a_count,
            "option_b_tagged": b_count,
            "agree_count": agree,
            "percent_agreement": agree / max(len(idxs), 1) * 100,
            "kappa": kappa,
        }
        combined_a.extend(a_tags)
        combined_b.extend(b_tags)
    if combined_a:
        agree = sum(1 for x, y in zip(combined_a, combined_b) if x == y)
        results["combined"] = {
            "n_chunks": len(combined_a),
            "option_a_tagged": sum(combined_a),
            "option_b_tagged": sum(combined_b),
            "agree_count": agree,
            "percent_agreement": agree / max(len(combined_a), 1) * 100,
            "kappa": cohen_kappa(combined_a, combined_b),
        }
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tags", type=Path, required=True,
                        help="Path to chunks_with_multilingual_tags_*.jsonl")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    chunks = []
    with args.tags.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    print(f"Loaded {len(chunks):,} chunks from {args.tags}")

    n_san = sum(1 for c in chunks if c.get("language") == "sanskrit")
    n_pali = sum(1 for c in chunks if c.get("language") == "pali")
    print(f"  Sanskrit: {n_san}, Pali: {n_pali}")

    res_awareness = evaluate_concept(chunks, "AWARENESS", MANUAL_AWARENESS)
    res_recognition = evaluate_concept(chunks, "RECOGNITION", MANUAL_RECOGNITION)

    print()
    for r in (res_awareness, res_recognition):
        print(f"=== {r['concept']} ===")
        for lang, info in r["per_language"].items():
            print(f"  {lang:8s}  n={info['n_chunks']:>4}  "
                  f"A_tag={info['option_a_tagged']:>3}  B_tag={info['option_b_tagged']:>3}  "
                  f"agree={info['percent_agreement']:5.1f}%  kappa={info['kappa']:+.3f}")
        if r["combined"]:
            c = r["combined"]
            print(f"  combined n={c['n_chunks']:>4}  "
                  f"A_tag={c['option_a_tagged']:>3}  B_tag={c['option_b_tagged']:>3}  "
                  f"agree={c['percent_agreement']:5.1f}%  kappa={c['kappa']:+.3f}")
        print()

    # Decision
    print("=== DECISION (per Phase 1c prereg) ===")
    decisions = {}
    for r in (res_awareness, res_recognition):
        c = r["combined"]
        if c is None:
            verdict = "INCONCLUSIVE (no data)"
        elif c["kappa"] >= 0.5 and c["percent_agreement"] >= 70.0:
            verdict = "PASS (kappa >= 0.5 AND agreement >= 70%)"
        else:
            verdict = "FAIL (kappa < 0.5 OR agreement < 70%)"
        decisions[r["concept"]] = verdict
        print(f"  {r['concept']:14s} {verdict}")

    overall = "CONFIRMATORY" if all("PASS" in v for v in decisions.values()) else "EXPLORATORY"
    print()
    print(f"  Phase 1c.2 reporting mode: {overall}")

    out = {
        "input": str(args.tags),
        "AWARENESS": res_awareness,
        "RECOGNITION": res_recognition,
        "decisions": decisions,
        "phase1c2_reporting_mode": overall,
    }
    if args.out is None:
        slug = args.tags.stem.replace("chunks_with_multilingual_tags_", "")
        args.out = REPO_ROOT / "results" / "phase1c" / f"option_a_spot_check_{slug}.json"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
