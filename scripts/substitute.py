"""
Vocabulary substitution pipeline.

Reads corpus/passages.jsonl, applies a structural-role substitution dictionary
to each passage's text, and writes corpus/passages_substituted.jsonl.

Philosophy of the substitution scheme
-------------------------------------
The goal is to normalize *vocabulary* that signals which tradition a passage
comes from, while preserving the *structural role* each word plays in the
discourse. Words that play the same role across traditions get the same
placeholder, so the embedding sees the same token sequence for sentences
making the same structural claim in different vocabularies.

Categories (each role maps to a unique gibberish placeholder so the
embedding model has no prior semantic association with the placeholder
token — the relationship must be inferred purely from context):

  [qntrx]  — ULTIMATE: the fundamental reality each tradition posits as ground
              (God, Brahman, Tao, the One, Buddha-nature, Ein Sof,
               computational substrate, mathematical universe...)
  [vpbkz]  — SUBSTRATE: the layer beneath appearance
              (emptiness, the implicate order, the holographic principle,
               the quantum vacuum, integrated information, śūnyatā,
               dependent origination...)
  [mljfd]  — AWARENESS: consciousness / mind / knowing
              (consciousness, awareness, rigpa, chit, phi, nous,
               primordial awareness...)
  [hsdwq]  — WORLD: the apparent / phenomenal / manifest
              (samsara, simulation, creation, cosmos, the phenomenal,
               spacetime, the ten thousand things, appearances...)
  [trnbc]  — SELF: the apparent individual (tradition-specific names only;
              generic pronouns I/me/you are preserved)
              (atman, jiva, the ego, the agent, the apparent self,
               Markov blanket...)
  [fxgvp]  — RECOGNITION: liberation / enlightenment / awakening
              (moksha, nirvana, theosis, fana, gnosis, jnana, satori,
               liberation, salvation, beatific vision...)
  [wkqzr]  — NONSEP: explicit naming of the structural feature
              (nondual, advaita, wahdat al-wujud, unity of being)

Conservative principles:
  - We substitute only *distinctive* tradition-vocabulary. Generic English
    ("world", "mind", "reality", "thing") stays — substituting it would
    obliterate sentence structure without isolating the vocabulary effect.
  - Multi-word phrases are matched before single words (order matters).
  - Case-insensitive matching with word-boundary anchors; placeholder is
    inserted verbatim.
  - Possessives ("God's") and plurals where natural ("gods") are handled.

This is v0 of the substitution scheme. Refinements expected.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_IN = REPO_ROOT / "corpus" / "passages.jsonl"
DEFAULT_OUT = REPO_ROOT / "corpus" / "passages_substituted.jsonl"
DEFAULT_DIFF = REPO_ROOT / "corpus" / "substitution_log.txt"


# Patterns ordered: longer / more specific first, so they match before
# shorter patterns can intercept them. Each entry is (regex, placeholder).
# All matched case-insensitively. \b for word boundaries.

PATTERNS: list[tuple[str, str]] = [
    # ===== ULTIMATE — multi-word phrases first =====
    (r"\bthe holy one\b", "[qntrx]"),
    (r"\bcomputational substrate\b", "[qntrx]"),
    (r"\bmathematical structure\b", "[qntrx]"),
    (r"\bmathematical universe\b", "[qntrx]"),
    (r"\bthe one(?=\b)(?!\s+(who|that|which))", "[qntrx]"),  # Plotinus's "the One" but not "the one who..."
    (r"\bthe real\b", "[qntrx]"),
    (r"\bultimate reality\b", "[qntrx]"),
    (r"\bthe absolute\b", "[qntrx]"),
    (r"\bthe infinite\b", "[qntrx]"),
    (r"\bthe divine\b", "[qntrx]"),
    (r"\bdivine ground\b", "[qntrx]"),
    (r"\bdivine essence\b", "[qntrx]"),
    (r"\bground of being\b", "[qntrx]"),
    (r"\bbasic ground\b", "[qntrx]"),
    (r"\bgroundless ground\b", "[qntrx]"),
    (r"\bbuddha[-\s]?nature\b", "[qntrx]"),
    (r"\bdharma[-\s]?body\b", "[qntrx]"),
    (r"\bdharmakaya\b", "[qntrx]"),
    (r"\bein sof\b", "[qntrx]"),
    (r"\bha[-\s]?shem\b", "[qntrx]"),
    (r"\bthe creator\b", "[qntrx]"),
    # Single-word divine names
    (r"\bgod's\b", "[qntrx]'s"),
    (r"\bgods\b", "[qntrx]s"),
    (r"\bgod\b", "[qntrx]"),
    (r"\ballah\b", "[qntrx]"),
    (r"\bbrahman\b", "[qntrx]"),
    (r"\btao\b", "[qntrx]"),
    (r"\bdao\b", "[qntrx]"),
    (r"\bsuchness\b", "[qntrx]"),
    (r"\btathata\b", "[qntrx]"),
    (r"\bdivine\b", "[qntrx]"),
    (r"\blord\b", "[qntrx]"),
    # ===== SUBSTRATE — the layer beneath appearance =====
    (r"\bthe implicate order\b", "[vpbkz]"),
    (r"\bimplicate order\b", "[vpbkz]"),
    (r"\bthe holomovement\b", "[vpbkz]"),
    (r"\bholomovement\b", "[vpbkz]"),
    (r"\bthe quantum vacuum\b", "[vpbkz]"),
    (r"\bthe holographic principle\b", "[vpbkz]"),
    (r"\bholographic\b", "[vpbkz]"),
    (r"\bdependent origination\b", "[vpbkz]"),
    (r"\bdependently arisen\b", "[vpbkz] arisen"),
    (r"\bbasic space\b", "[vpbkz]"),
    (r"\bintegrated information\b", "[vpbkz]"),
    (r"\bemptiness\b", "[vpbkz]"),
    (r"\bshunyata\b", "[vpbkz]"),
    (r"\b(s|ś)ūnyatā\b", "[vpbkz]"),
    (r"\bsvabhava\b", "[vpbkz]"),  # actually means "self-nature" — the thing emptiness denies
    (r"\bnoumenon\b", "[vpbkz]"),
    (r"\bnoumena\b", "[vpbkz]"),
    (r"\bthing[-\s]?in[-\s]?itself\b", "[vpbkz]"),

    # ===== AWARENESS — consciousness / mind / knowing =====
    (r"\bprimordial awareness\b", "[mljfd]"),
    (r"\bpure consciousness\b", "[mljfd]"),
    (r"\bpure awareness\b", "[mljfd]"),
    (r"\bbare awareness\b", "[mljfd]"),
    (r"\bnaked awareness\b", "[mljfd]"),
    (r"\brigpa\b", "[mljfd]"),
    (r"\bsat[-\s]?cit[-\s]?ananda\b", "[mljfd]"),
    (r"\bchit\b", "[mljfd]"),
    (r"\bchitta\b", "[mljfd]"),
    (r"\bcitta\b", "[mljfd]"),
    (r"\bnous\b", "[mljfd]"),
    (r"\bphi\b", "[mljfd]"),  # IIT-specific
    (r"\bconsciousness\b", "[mljfd]"),
    (r"\bawareness\b", "[mljfd]"),
    (r"\bsentience\b", "[mljfd]"),

    # ===== WORLD — apparent / phenomenal / manifest =====
    (r"\bthe ten thousand things\b", "[hsdwq]"),
    (r"\bthe manifold of phenomena\b", "[hsdwq]"),
    (r"\bthe simulation\b", "[hsdwq]"),
    (r"\bancestor simulation\b", "[hsdwq]"),
    (r"\ba simulation\b", "a [hsdwq]"),
    (r"\bsimulations\b", "[hsdwq]s"),
    (r"\bsimulation\b", "[hsdwq]"),
    (r"\bsamsara\b", "[hsdwq]"),
    (r"\bphenomenal world\b", "[hsdwq]"),
    (r"\bphenomenal universe\b", "[hsdwq]"),
    (r"\bphenomenal\b", "[hsdwq]"),
    (r"\bcreation\b", "[hsdwq]"),
    (r"\bthe cosmos\b", "[hsdwq]"),
    (r"\bcosmos\b", "[hsdwq]"),
    (r"\bthe universe\b", "[hsdwq]"),
    (r"\bspacetime\b", "[hsdwq]"),
    (r"\bphysical universe\b", "[hsdwq]"),
    (r"\bphysical reality\b", "[hsdwq]"),
    (r"\bphysical objects?\b", "[hsdwq]"),
    (r"\bappearances\b", "[hsdwq]"),
    (r"\bappearance\b", "[hsdwq]"),
    (r"\bthe ten thousand\b", "[hsdwq]"),

    # ===== SELF — only tradition-specific names =====
    # We deliberately do NOT substitute "I/me/you/he/she" — those are generic pronouns
    (r"\batman\b", "[trnbc]"),
    (r"\bjiva\b", "[trnbc]"),
    (r"\bthe ego\b", "[trnbc]"),
    (r"\bthe empirical self\b", "[trnbc]"),
    (r"\bthe individual self\b", "[trnbc]"),
    (r"\bthe apparent self\b", "[trnbc]"),
    (r"\bthe agent\b", "[trnbc]"),
    (r"\bconscious agent\b", "[trnbc]"),
    (r"\bmarkov blanket\b", "[trnbc]"),  # FEP-specific name for the boundary

    # ===== RECOGNITION — liberation / awakening =====
    (r"\bmoksha\b", "[fxgvp]"),
    (r"\bmukti\b", "[fxgvp]"),
    (r"\bnirvana\b", "[fxgvp]"),
    (r"\bnibbana\b", "[fxgvp]"),
    (r"\benlightenment\b", "[fxgvp]"),
    (r"\bawakening\b", "[fxgvp]"),
    (r"\bsatori\b", "[fxgvp]"),
    (r"\bbodhi\b", "[fxgvp]"),
    (r"\btheosis\b", "[fxgvp]"),
    (r"\bdeification\b", "[fxgvp]"),
    (r"\bfana\b", "[fxgvp]"),
    (r"\bbaqa\b", "[fxgvp]"),
    (r"\bgnosis\b", "[fxgvp]"),
    (r"\bjnana\b", "[fxgvp]"),
    (r"\bself[-\s]realization\b", "[fxgvp]"),
    (r"\bliberation\b", "[fxgvp]"),
    (r"\bsalvation\b", "[fxgvp]"),
    (r"\bbeatific vision\b", "[fxgvp]"),
    # (removed: cascading union-with-X rules don't fire under single-pass substitution; the individual names handle it)

    # ===== NONSEP — the explicit naming of the structural feature =====
    (r"\bnon[-\s]?duality\b", "[wkqzr]"),
    (r"\bnon[-\s]?dual\b", "[wkqzr]"),
    (r"\badvaita\b", "[wkqzr]"),
    (r"\bwahdat al[-\s]?wujud\b", "[wkqzr]"),
    (r"\bunity of being\b", "[wkqzr]"),

    # ===== Tradition labels themselves — strip giveaways =====
    (r"\bvedanta\b", ""),
    (r"\bdzogchen\b", ""),
    (r"\bkabbalah\b", ""),
    (r"\bbuddhist\b", ""),
    (r"\bchristian\b", ""),
    (r"\bhindu\b", ""),
    (r"\bsufi\b", ""),
    (r"\bdaoist\b", ""),
    (r"\btaoist\b", ""),
    (r"\bislamic\b", ""),
    (r"\bjewish\b", ""),
    (r"\bzen\b", ""),
    (r"\bmahayana\b", ""),
    (r"\btheravada\b", ""),
    (r"\bmadhyamika\b", ""),
    (r"\bquantum\b", ""),
    (r"\bcomputational\b", ""),
    (r"\binformation[-\s]?theoretic\b", ""),
    (r"\bholy spirit\b", "[qntrx]"),
    (r"\bholy one\b", "[qntrx]"),
    (r"\bsefirot\b", ""),
    (r"\baggregates\b", ""),  # Theravada-specific term
    (r"\bfive aggregates\b", ""),
]


def compile_patterns() -> tuple[re.Pattern, dict[str, str]]:
    """
    Compile all patterns into a single alternation. Single-pass substitution
    avoids the cascade bug where one pattern's replacement (e.g. [mljfd])
    contains a word that a later pattern (\\bawareness\\b case-insensitive)
    would re-match.

    Pattern order in the alternation determines tie-breaking: in Python regex,
    the leftmost alternative wins. So longer/more-specific patterns should
    come first in the PATTERNS list — which they do.
    """
    parts = []
    repl_map: dict[str, str] = {}
    for i, (pat, repl) in enumerate(PATTERNS):
        name = f"g{i}"
        parts.append(f"(?P<{name}>{pat})")
        repl_map[name] = repl
    combined = re.compile("|".join(parts), flags=re.IGNORECASE)
    return combined, repl_map


def substitute(text: str, combined: re.Pattern, repl_map: dict[str, str]) -> tuple[str, list[tuple[str, str]]]:
    """Single-pass substitution. Return (new_text, list of (original, replacement) hits)."""
    hits: list[tuple[str, str]] = []

    def _cb(m: re.Match) -> str:
        for name, val in m.groupdict().items():
            if val is not None:
                repl = repl_map[name]
                hits.append((m.group(0), repl))
                return repl
        return m.group(0)

    out = combined.sub(_cb, text)
    # collapse double spaces from empty-string substitutions
    out = re.sub(r"\s{2,}", " ", out).strip()
    # tidy spacing around punctuation after empty substitutions
    out = re.sub(r"\s+([,.;:!?])", r"\1", out)
    return out, hits


def main() -> None:
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--in-path", type=Path, default=DEFAULT_IN)
    p.add_argument("--out-path", type=Path, default=DEFAULT_OUT)
    p.add_argument("--diff-path", type=Path, default=DEFAULT_DIFF)
    args = p.parse_args()

    IN_PATH = args.in_path
    OUT_PATH = args.out_path
    DIFF_PATH = args.diff_path

    combined, repl_map = compile_patterns()
    counts: Counter = Counter()
    log_lines: list[str] = []

    n = 0
    with IN_PATH.open("r", encoding="utf-8") as fin, OUT_PATH.open(
        "w", encoding="utf-8"
    ) as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            orig = rec["passage"]
            new, hits = substitute(orig, combined, repl_map)
            rec["passage"] = new
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
            for orig_term, _ in hits:
                counts[orig_term.lower()] += 1
            if hits:
                log_lines.append(
                    f"--- {rec['id']} ({rec['tradition']}/{rec['category']}) ---\n"
                    f"BEFORE: {orig}\n"
                    f"AFTER : {new}\n"
                    f"HITS  : {[h[0] for h in hits]}\n"
                )

    with DIFF_PATH.open("w", encoding="utf-8") as f:
        f.write(f"# Substitution log — {n} passages processed\n\n")
        f.write("## Substitution counts (lowercased)\n\n")
        for term, c in counts.most_common():
            f.write(f"  {term}: {c}\n")
        f.write("\n## Per-passage diffs\n\n")
        f.writelines(log_lines)

    print(f"wrote {OUT_PATH} ({n} passages)")
    print(f"wrote {DIFF_PATH} ({sum(counts.values())} total substitutions, {len(counts)} unique terms hit)")
    print("\nTop substitution hits:")
    for term, c in counts.most_common(20):
        print(f"  {c:>4}  {term}")


if __name__ == "__main__":
    main()
