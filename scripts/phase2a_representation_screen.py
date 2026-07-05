"""
Phase 2a Stage-1 representation-quality screen.

Cheaply estimates how well the embedding model(s) represent each candidate
translation-target language, to decide eligibility for the westernization
triangulation BEFORE paying for a full within-language concept-binding gate on
each one. Uses the FLORES+ dev set (997 professionally-translated parallel
sentences per language) so semantic content is held constant across languages.

Two metrics, deliberately of different contamination profiles:

  (1) TOKENIZER FERTILITY  -- PRIMARY, contamination-immune.
      mean subword tokens per parallel sentence, per model tokenizer.
      Content is held constant (parallel sentences), so a language fragmented
      into more subword tokens has poorer vocabulary coverage = worse
      representation. Depends ONLY on the tokenizer's learned vocabulary, never
      on whether the model saw FLORES in pretraining -> immune to evaluation
      contamination. Reported as a ratio vs English (relative ranking only;
      cross-script absolute fertility is not directly comparable).

  (2) CROSS-LINGUAL RETRIEVAL ACCURACY  -- SECONDARY, contamination-susceptible.
      embed lang-X and English parallel sets; for each X sentence retrieve the
      nearest English sentence; P@1 and MRR of the correct translation.
      Directly measures cross-lingual semantic alignment, but if FLORES leaked
      into pretraining this is OPTIMISTIC. Used only to corroborate the
      fertility ranking, never as the sole eligibility signal.

CALIBRATION ANCHORS (we have independent within-language-gate ground truth):
  english/french/german  -> high-resource, expect top of ranking
  cmn_Hans (modern Chinese) -> Classical-Chinese 法句經 passed the gate 6/7
  san_Deva (Sanskrit)       -> gate FAILED 2/7  (known-bad anchor)
If the screen ranks these consistently with the gate, we trust it to rank the
untested candidates (hindi, japanese, korean, hebrew, arabic, persian, ...).

COMPLIANCE: reads FLORES+ text ONLY from the gitignored corpus/flores/ cache;
writes ONLY aggregate per-language scores to results/phase2a/. NEVER emits any
FLORES sentence text. Do not change this without re-reading the FLORES+ license.

Usage:
  python scripts/phase2a_representation_screen.py --metric fertility
  python scripts/phase2a_representation_screen.py --metric retrieval --model intfloat/multilingual-e5-large
  python scripts/phase2a_representation_screen.py --metric both
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

FLORES_CACHE = REPO_ROOT / "corpus" / "flores"
OUT_DIR = REPO_ROOT / "results" / "phase2a"

# candidate display name -> FLORES+ code present in the local cache
LANGS: dict[str, str] = {
    "english": "eng_Latn",
    "modern_chinese": "cmn_Hans",
    "hindi": "hin_Deva",
    "japanese": "jpn_Jpan",
    "french": "fra_Latn",
    "spanish": "spa_Latn",
    "german": "deu_Latn",
    "korean": "kor_Hang",
    "hebrew": "heb_Hebr",
    "arabic": "arb_Arab",
    "persian": "pes_Arab",
    "sanskrit": "san_Deva",  # known-FAIL gate anchor
}

# tokenizers for the two models used by the within-language gate
TOKENIZERS = {
    "e5-large": "intfloat/multilingual-e5-large",
    "LaBSE": "sentence-transformers/LaBSE",
}


def load_sentences(code: str) -> list[str]:
    """Read the cached FLORES+ dev file. Sentences stay local; never written out."""
    path = FLORES_CACHE / f"dev_{code}.jsonl"
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line)["text"])
    return out


def run_fertility() -> dict:
    from transformers import AutoTokenizer

    sents = {name: load_sentences(code) for name, code in LANGS.items()}
    sents = {k: v for k, v in sents.items() if v}

    result = {}
    for tname, tid in TOKENIZERS.items():
        print(f"\n=== tokenizer fertility: {tname} ({tid}) ===")
        tok = AutoTokenizer.from_pretrained(tid)
        per_lang = {}
        for name, texts in sents.items():
            enc = tok(texts, add_special_tokens=False)["input_ids"]
            n_tok = sum(len(x) for x in enc)
            n_char = sum(len(t) for t in texts)
            per_lang[name] = {
                "tokens_per_sentence": n_tok / len(texts),
                "chars_per_token": n_char / n_tok,
                "n_sentences": len(texts),
            }
        eng = per_lang["english"]["tokens_per_sentence"]
        for name, d in per_lang.items():
            d["fertility_ratio_vs_english"] = d["tokens_per_sentence"] / eng
        result[tname] = per_lang

        ordered = sorted(per_lang.items(), key=lambda kv: kv[1]["fertility_ratio_vs_english"])
        print(f"  {'language':18s} {'tok/sent':>9s} {'ratio/eng':>10s} {'chars/tok':>10s}")
        print("  " + "-" * 50)
        for name, d in ordered:
            mark = "  <- FAIL anchor" if name == "sanskrit" else ("  <- baseline" if name == "english" else "")
            print(f"  {name:18s} {d['tokens_per_sentence']:9.2f} {d['fertility_ratio_vs_english']:10.2f} {d['chars_per_token']:10.2f}{mark}")
    return result


def run_retrieval(model_id: str) -> dict:
    from multilingual_embedder import MultilingualEmbedder

    emb = MultilingualEmbedder(model_id)
    eng = load_sentences(LANGS["english"])
    eng_vec = emb.encode(eng, batch_size=16)
    eng_vec = eng_vec / (np.linalg.norm(eng_vec, axis=1, keepdims=True) + 1e-12)

    print(f"\n=== cross-lingual retrieval (X -> english): {model_id} ===")
    print("  (secondary metric; OPTIMISTIC if FLORES leaked into pretraining)")
    print(f"  {'language':18s} {'P@1':>7s} {'MRR':>7s} {'n':>6s}")
    print("  " + "-" * 42)
    per_lang = {}
    for name, code in LANGS.items():
        if name == "english":
            continue
        xs = load_sentences(code)
        if not xs:
            continue
        n = min(len(xs), len(eng))
        xv = emb.encode(xs[:n], batch_size=16)
        xv = xv / (np.linalg.norm(xv, axis=1, keepdims=True) + 1e-12)
        sim = xv @ eng_vec[:n].T              # (n_x, n_eng)
        ranks = (sim >= sim[np.arange(n), np.arange(n)][:, None]).sum(axis=1)  # rank of true match
        p_at_1 = float((ranks == 1).mean())
        mrr = float((1.0 / ranks).mean())
        per_lang[name] = {"p_at_1": p_at_1, "mrr": mrr, "n": n}
        print(f"  {name:18s} {p_at_1:7.3f} {mrr:7.3f} {n:6d}")
    return per_lang


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--metric", choices=["fertility", "retrieval", "both"], default="fertility")
    ap.add_argument("--model", default="intfloat/multilingual-e5-large",
                    help="embedder for the retrieval metric")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "representation_screen.json"
    blob = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
    blob.setdefault("_note", "Aggregate FLORES+ representation scores only. No FLORES text. "
                             "Fertility = contamination-immune primary; retrieval = caveated secondary.")

    if args.metric in ("fertility", "both"):
        blob["fertility"] = run_fertility()
    if args.metric in ("retrieval", "both"):
        blob.setdefault("retrieval", {})[args.model] = run_retrieval(args.model)

    out_path.write_text(json.dumps(blob, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
