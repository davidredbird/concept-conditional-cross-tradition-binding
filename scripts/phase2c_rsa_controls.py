"""
Phase 2c -- RSA robustness CONTROLS: (A) split-half noise ceiling, (B) arbitrary-word-set
baseline. A peer review flagged that the headline cross-language RSA isomorphism (+0.392
LaBSE / +0.435 OpenAI, K=7 harmonized concepts -- see phase3a_rsa_recheck.py) has no
instrument ceiling and no null-geometry baseline. This script computes both.

FIREWALL: Phase 2c ORIGINALS ONLY -- the same 6-language, 14-book corpus used by
phase3a_rsa_prototype.py / _recheck.py / _snr.py (classical_chinese, arabic, greek, hindi,
spanish, hebrew). No China x Greece comparison, no Axial gradient corpus, no new embedding
computation -- only cached LaBSE (results/phase2a/*.npy) and cached OpenAI
(results/phase3a/originals_openai_te3l.npy) embeddings are read.

Control A (--control ceiling)
  Per language x model: split each concept's tagged chunks in half (100 resamples,
  seed=1908), build RDM_half1 / RDM_half2 (7x7 concept dissimilarity, upper triangle),
  Spearman-correlate the halves, average over resamples, Spearman-Brown correct (2r/(1+r))
  -> full-data within-language RDM reliability rel_L. Ceiling for a language pair (i,j) =
  sqrt(rel_i * rel_j); the ceiling for the overall isomorphism is the mean over the same 15
  language pairs used in the published number.

Control B (--control baseline)
  Per language: build 50 pseudo-concept-sets, each with 7 pseudo-concepts. A pseudo-concept
  is a set of tokens sampled from that language's OWN chunk text (whitespace tokens len>=3
  for languages with word boundaries; single/bigram Han characters for classical Chinese),
  greedily grown to match the tagged-chunk count of the CORRESPONDING real concept (same
  index, same language) within +/-20%, excluding any token overlapping the harmonized
  dictionaries. Pseudo-concepts are sampled INDEPENDENTLY per language -- no cross-language
  correspondence is constructed (that is the point of the control). Cross-language RDM
  isomorphism is computed for each of the 50 draws -> a null/baseline distribution; the real
  isomorphism (recomputed here as a sanity check) is located as a percentile of that
  distribution.

  Interpretive subtlety (see findings write-up for full discussion): the real concepts carry
  an INVESTIGATOR-MADE cross-language correspondence (the harmonized dictionary maps e.g.
  "AWARENESS" to a term list in every language); the pseudo-concepts deliberately do NOT.
  So Control B tests "correspondence + geometry" jointly against "no correspondence" -- a
  high percentile for the real value does not, by itself, prove the geometry-isomorphism
  part in isolation from the fact that the concepts were hand-matched across languages.

Usage:
  python scripts/phase2c_rsa_controls.py --control ceiling
  python scripts/phase2c_rsa_controls.py --control baseline
  python scripts/phase2c_rsa_controls.py --control all
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import re
import string
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")
import harmonized_concepts as hc  # noqa: E402

SLUG = "sentence_transformers__LaBSE"
ORIGINALS = ["chinese_taote_chinese", "chinese_zhuangzi_chinese", "chinese_platform_sutra_chinese",
             "chinese_analects_chinese", "arabic_fusus_arabic", "arabic_najat_arabic",
             "greek_plotinus_greek", "greek_clement_greek", "hindi_kabir_hindi",
             "hindi_tulsidas_hindi", "hindi_surdas_hindi", "spanish_molinos_spanish",
             "spanish_teresa_spanish", "hebrew_nachman_hebrew"]
OPENAI_CACHE = REPO / "results" / "phase3a" / "originals_openai_te3l.npy"
CONCEPTS = ["SUBSTRATE", "AWARENESS", "ULTIMATE", "WORLD", "SELF", "RECOGNITION", "NONSEP"]
MIN_N = 5
OUT_PATH = REPO / "results" / "robustness" / "rsa_controls.json"

PUBLISHED = {"LaBSE": 0.392, "OpenAI": 0.435}  # from phase3a_rsa_recheck.py (post-hyle-fix)

PUNCT = string.punctuation + "«»¡¿—–“”‘’·…、。，「」『』（）"
NORM_FNS = {
    "arabic": hc._norm_ar,
    "hebrew": hc._norm_he,
    "greek": hc._norm_gr,
    "hindi": lambda s: s,
    "spanish": lambda s: s.lower(),
}


# ----------------------------------------------------------------------------------
# shared loading / RDM machinery (mirrors phase3a_rsa_recheck.py exactly, so the
# "real" isomorphism recomputed here matches the published +0.392 / +0.435)
# ----------------------------------------------------------------------------------

def load():
    chunks, labse = [], []
    for stem in ORIGINALS:
        cs = [json.loads(l) for l in (REPO / "corpus" / f"chunks_{stem}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        e = np.load(REPO / "results" / "phase2a" / f"{stem}_{SLUG}.npy")
        chunks += cs
        labse.append(e)
    labse = np.vstack(labse)
    labse /= (np.linalg.norm(labse, axis=1, keepdims=True) + 1e-12)
    openai = np.load(OPENAI_CACHE)
    assert openai.shape[0] == len(chunks), f"openai rows {openai.shape[0]} != chunks {len(chunks)}"
    return chunks, labse, openai


def rank(v):
    o = v.argsort()
    r = np.empty_like(o, float)
    r[o] = np.arange(len(v))
    return r


def spearman(a, b):
    return float(np.corrcoef(rank(a), rank(b))[0, 1])


def cent(emb, idx):
    """Mean embedding over idx (array-like of global row indices), L2-normalized. None if empty."""
    idx = np.asarray(idx, dtype=int)
    if idx.size == 0:
        return None
    v = emb[idx].mean(0)
    n = np.linalg.norm(v)
    return v / (n + 1e-12) if n > 0 else v


def rdm_upper(cents, concepts):
    K = len(concepts)
    iu = np.triu_indices(K, 1)
    M = np.array([[1 - float(cents[a] @ cents[b]) for b in concepts] for a in concepts])
    return M[iu]


def real_iso(chunks, tags, langs, emb_dict):
    """Recompute the published holistic isomorphism (sanity check). Returns {model: (iso, common_concepts)}."""
    out = {}
    for name, emb in emb_dict.items():
        cents = {}
        for L in langs:
            cc = {}
            for c in CONCEPTS:
                idx = [i for i, ch in enumerate(chunks) if ch["language"] == L and c in tags[i]]
                if len(idx) >= MIN_N:
                    v = cent(emb, idx)
                    if v is not None:
                        cc[c] = v
            cents[L] = cc
        common = [c for c in CONCEPTS if all(c in cents[L] for L in langs)]
        rdms = {L: rdm_upper(cents[L], common) for L in langs}
        pairs = list(itertools.combinations(langs, 2))
        vals = [spearman(rdms[i], rdms[j]) for i, j in pairs]
        out[name] = (float(np.mean(vals)), common)
    return out


# ----------------------------------------------------------------------------------
# Control A: split-half noise ceiling
# ----------------------------------------------------------------------------------

def control_ceiling(chunks, tags, langs, emb_dict, resamples, seed):
    rng = np.random.default_rng(seed)
    per_lang_concept_idx = {
        L: {c: np.array([i for i, ch in enumerate(chunks) if ch["language"] == L and c in tags[i]])
            for c in CONCEPTS}
        for L in langs
    }
    reliab = {name: {} for name in emb_dict}
    for L in langs:
        concept_idx = per_lang_concept_idx[L]
        for name, emb in emb_dict.items():
            rs = []
            for _ in range(resamples):
                h1c, h2c = {}, {}
                ok = True
                for c in CONCEPTS:
                    idx = concept_idx[c].copy()
                    if idx.size < 2:
                        ok = False
                        break
                    rng.shuffle(idx)
                    n1 = len(idx) // 2
                    h1, h2 = idx[:n1], idx[n1:]
                    v1, v2 = cent(emb, h1), cent(emb, h2)
                    if v1 is None or v2 is None:
                        ok = False
                        break
                    h1c[c], h2c[c] = v1, v2
                if not ok:
                    continue
                M1 = rdm_upper(h1c, CONCEPTS)
                M2 = rdm_upper(h2c, CONCEPTS)
                rs.append(spearman(M1, M2))
            r_raw = float(np.mean(rs)) if rs else float("nan")
            r_sb = (2 * r_raw) / (1 + r_raw) if (r_raw == r_raw and (1 + r_raw) != 0) else float("nan")
            reliab[name][L] = {"raw_split_half_r": r_raw, "sb_corrected": r_sb,
                                "resamples_used": len(rs), "resamples_requested": resamples}

    pairs = list(itertools.combinations(langs, 2))
    ceiling = {}
    for name in emb_dict:
        vals = []
        pairwise = {}
        for i, j in pairs:
            ri = max(reliab[name][i]["sb_corrected"], 0.0)
            rj = max(reliab[name][j]["sb_corrected"], 0.0)
            c = math.sqrt(ri * rj)
            vals.append(c)
            pairwise[f"{i}|{j}"] = c
        mean_ceiling = float(np.mean(vals))
        published = PUBLISHED[name]
        ceiling[name] = {
            "mean_ceiling": mean_ceiling,
            "n_pairs": len(pairs),
            "pairwise_ceiling": pairwise,
            "published_iso": published,
            "iso_over_ceiling": published / mean_ceiling if mean_ceiling > 0 else float("nan"),
        }
    return {"reliability": reliab, "ceiling": ceiling, "seed": seed, "resamples": resamples}


# ----------------------------------------------------------------------------------
# Control B: arbitrary-word-set baseline
# ----------------------------------------------------------------------------------

def regex_core(pat):
    s = pat.replace(r"\b", "")
    s = re.sub(r"[()?|\[\]]", "", s)
    s = s.replace("\\-", "-")
    s = re.sub(r"\\", "", s)
    return s.lower().strip()


def banned_terms_for(lang):
    terms_dict = hc.TERMS.get(lang, {})
    flat = [t for lst in terms_dict.values() for t in lst]
    mode = hc._MATCH[lang]
    if mode == "regex":
        return [regex_core(p) for p in flat]
    if isinstance(mode, tuple):
        normfn = mode[1]
        return [normfn(t) for t in flat]
    return list(flat)


def is_banned(tok, banned):
    for b in banned:
        if not b:
            continue
        if tok == b or tok in b or b in tok:
            return True
    return False


HAN_RE = re.compile(r"[一-鿿]")


def build_language_vocab(chunks, lang):
    """token -> set of LOCAL chunk positions (0..len(idxL)-1) containing that token.
    idxL = global chunk indices for this language, in order."""
    idxL = [i for i, ch in enumerate(chunks) if ch["language"] == lang]
    texts = [chunks[i]["text"] for i in idxL]
    banned = banned_terms_for(lang)
    token_pos: dict[str, set[int]] = {}

    if lang == "classical_chinese":
        for p, t in enumerate(texts):
            toks = set()
            for k in range(len(t)):
                c1 = t[k]
                if HAN_RE.match(c1):
                    toks.add(c1)
                    if k + 1 < len(t) and HAN_RE.match(t[k + 1]):
                        toks.add(t[k:k + 2])
            toks = {tok for tok in toks if not is_banned(tok, banned)}
            for tok in toks:
                token_pos.setdefault(tok, set()).add(p)
    else:
        norm_fn = NORM_FNS.get(lang, lambda s: s.lower())
        for p, t in enumerate(texts):
            nt = norm_fn(t)
            toks = set()
            for rt in re.findall(r"\S+", nt):
                rt2 = rt.strip(PUNCT)
                if len(rt2) >= 3 and not is_banned(rt2, banned):
                    toks.add(rt2)
            for tok in toks:
                token_pos.setdefault(tok, set()).add(p)

    # drop hapax tokens (freq 1) -- pure efficiency/stability choice, documented in write-up
    token_pos = {tok: s for tok, s in token_pos.items() if len(s) >= 2}
    return idxL, token_pos


def sample_pseudo_concept(token_pos, target_n, rng, tol=0.2, max_tokens=60, max_scan=800):
    vocab = list(token_pos.keys())
    if not vocab or target_n <= 0:
        return set(), False
    order = rng.permutation(len(vocab))
    lo = max(1, math.ceil(target_n * (1 - tol)))
    hi = max(lo, math.floor(target_n * (1 + tol)))
    covered: set[int] = set()
    chosen = []
    scanned = 0
    hit = False
    for oi in order:
        tok = vocab[oi]
        scanned += 1
        cand = covered | token_pos[tok]
        if len(cand) <= hi:
            covered = cand
            chosen.append(tok)
            if len(covered) >= lo:
                hit = True
                break
        if scanned >= max_scan or len(chosen) >= max_tokens:
            break
    if not hit and len(covered) < lo:
        used = set(chosen)
        remaining = [vocab[oi] for oi in order if vocab[oi] not in used]
        for tok in remaining:
            if len(covered) >= lo:
                hit = True
                break
            covered = covered | token_pos[tok]
        hit = hit or (lo <= len(covered) <= hi)
    return covered, (lo <= len(covered) <= hi)


def control_baseline(chunks, tags, langs, emb_dict, draws, seed):
    rng = np.random.default_rng(seed)

    # real per-(language, concept) tagged-chunk count -- the prevalence target
    n_real = {L: {c: sum(1 for i, ch in enumerate(chunks) if ch["language"] == L and c in tags[i])
                  for c in CONCEPTS} for L in langs}

    vocabs = {L: build_language_vocab(chunks, L) for L in langs}  # {L: (idxL, token_pos)}

    pairs = list(itertools.combinations(langs, 2))
    draw_iso = {name: [] for name in emb_dict}
    qc_total, qc_within_tol = 0, 0
    qc_deviation = []

    for d in range(draws):
        # build this draw's pseudo-concepts per language (shared across models)
        masks = {}  # L -> {concept: global idx array}
        for L in langs:
            idxL, token_pos = vocabs[L]
            cc = {}
            for c in CONCEPTS:
                target = n_real[L][c]
                covered_local, within_tol = sample_pseudo_concept(token_pos, target, rng)
                qc_total += 1
                qc_within_tol += int(within_tol)
                achieved = len(covered_local)
                if target > 0:
                    qc_deviation.append(abs(achieved - target) / target)
                if covered_local:
                    cc[c] = np.array([idxL[p] for p in covered_local], dtype=int)
                else:
                    cc[c] = np.array(idxL, dtype=int)  # degenerate fallback: whole-language mean
            masks[L] = cc

        for name, emb in emb_dict.items():
            cents = {L: {c: cent(emb, masks[L][c]) for c in CONCEPTS} for L in langs}
            rdms = {L: rdm_upper(cents[L], CONCEPTS) for L in langs}
            vals = [spearman(rdms[i], rdms[j]) for i, j in pairs]
            draw_iso[name].append(float(np.mean(vals)))

    real = real_iso(chunks, tags, langs, emb_dict)

    out = {}
    for name in emb_dict:
        arr = np.array(draw_iso[name])
        r, _common = real[name]
        pct = 100.0 * (np.sum(arr < r) + 0.5 * np.sum(arr == r)) / len(arr)
        out[name] = {
            "draws": draws,
            "baseline_mean": float(arr.mean()),
            "baseline_sd": float(arr.std(ddof=1)),
            "baseline_min": float(arr.min()),
            "baseline_max": float(arr.max()),
            "real_iso_recomputed": r,
            "published_iso": PUBLISHED[name],
            "real_percentile_in_baseline": float(pct),
        }
    qc = {
        "pseudo_concepts_built": qc_total,
        "fraction_within_tol20": qc_within_tol / qc_total if qc_total else float("nan"),
        "mean_abs_relative_deviation": float(np.mean(qc_deviation)) if qc_deviation else float("nan"),
    }
    return {"models": out, "qc": qc, "seed": seed, "draws": draws,
            "raw_draw_values": {name: draw_iso[name] for name in emb_dict}}


# ----------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--control", choices=["ceiling", "baseline", "all"], default="all")
    ap.add_argument("--seed", type=int, default=1908)
    ap.add_argument("--resamples", type=int, default=100)
    ap.add_argument("--draws", type=int, default=50)
    args = ap.parse_args()

    chunks, labse, openai = load()
    langs = sorted(set(c["language"] for c in chunks))
    tags = [set(hc.tag(c["language"], c["text"])) for c in chunks]
    emb_dict = {"LaBSE": labse, "OpenAI": openai}

    print(f"{len(chunks)} chunks; languages ({len(langs)}): {langs}")
    real = real_iso(chunks, tags, langs, emb_dict)
    for name, (r, common) in real.items():
        print(f"  real isomorphism [{name}] recomputed = {r:+.3f}  (published {PUBLISHED[name]:+.3f}); common concepts K={len(common)}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    results = json.loads(OUT_PATH.read_text(encoding="utf-8")) if OUT_PATH.exists() else {}
    results["meta"] = {
        "n_chunks": len(chunks), "languages": langs, "concepts": CONCEPTS,
        "published_iso": PUBLISHED,
        "real_iso_recomputed": {name: r for name, (r, _c) in real.items()},
    }

    if args.control in ("ceiling", "all"):
        print(f"\n=== Control A: split-half noise ceiling (seed={args.seed}, resamples={args.resamples}) ===")
        ceil = control_ceiling(chunks, tags, langs, emb_dict, args.resamples, args.seed)
        results["ceiling"] = ceil
        for name in emb_dict:
            print(f"  [{name}] per-language SB-corrected reliability:")
            for L in langs:
                rr = ceil["reliability"][name][L]
                print(f"    {L:18s} raw={rr['raw_split_half_r']:+.3f}  SB={rr['sb_corrected']:+.3f}")
            c = ceil["ceiling"][name]
            print(f"    mean ceiling (over {c['n_pairs']} pairs) = {c['mean_ceiling']:.3f}")
            print(f"    published iso {c['published_iso']:+.3f}  ->  iso/ceiling = {c['iso_over_ceiling']:.3f}")

    if args.control in ("baseline", "all"):
        print(f"\n=== Control B: arbitrary-word-set baseline (seed={args.seed+1}, draws={args.draws}) ===")
        base = control_baseline(chunks, tags, langs, emb_dict, args.draws, args.seed + 1)
        results["baseline"] = base
        for name in emb_dict:
            b = base["models"][name]
            print(f"  [{name}] baseline mean={b['baseline_mean']:+.3f} sd={b['baseline_sd']:.3f} "
                  f"(range {b['baseline_min']:+.3f}..{b['baseline_max']:+.3f})")
            print(f"    real iso {b['real_iso_recomputed']:+.3f} (published {b['published_iso']:+.3f}) "
                  f"-> percentile {b['real_percentile_in_baseline']:.1f} in the null distribution")
        print(f"  QC: {base['qc']['pseudo_concepts_built']} pseudo-concepts built, "
              f"{base['qc']['fraction_within_tol20']:.1%} within +/-20% target, "
              f"mean |relative deviation| = {base['qc']['mean_abs_relative_deviation']:.3f}")

    OUT_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_PATH}")


if __name__ == "__main__":
    main()
