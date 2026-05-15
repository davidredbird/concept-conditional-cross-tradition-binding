"""
Phase 0 prototype: computational comparative mysticism.

Loads passages.jsonl, embeds them with one or more sentence-transformer
models (and optionally OpenAI), then asks the central question:

    Do nondual passages from unconnected traditions cluster together
    in embedding space more tightly than they cluster with dualistic
    passages from their own tradition?

Outputs:
    - results/<model_name>/summary.txt        statistical summary
    - results/<model_name>/umap.png           UMAP scatter, colored by category, shape by tradition
    - results/<model_name>/tsne.png           t-SNE alternative
    - results/<model_name>/similarity.npy     full pairwise similarity matrix
    - results/<model_name>/tradition_sim.csv  tradition-level similarity matrix

Usage:
    python prototype.py
    python prototype.py --model BAAI/bge-large-en-v1.5
    python prototype.py --models sentence-transformers/all-mpnet-base-v2,BAAI/bge-large-en-v1.5
"""

from __future__ import annotations

import argparse
import json
import os
import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np

# matplotlib is the only hard plotting dep; UMAP and sklearn are imported lazily
# inside the relevant functions so a partial install still gets you something.

REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS_PATH = REPO_ROOT / "corpus" / "passages.jsonl"
RESULTS_DIR = REPO_ROOT / "results"

DEFAULT_MODELS = [
    "sentence-transformers/all-mpnet-base-v2",
]


@dataclass
class Passage:
    id: str
    tradition: str
    category: str
    author: str
    source: str
    translator: str
    era: str
    source_status: str
    passage: str


def load_corpus(path: Path) -> list[Passage]:
    out: list[Passage] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            out.append(Passage(**rec))
    return out


def embed_sentence_transformers(model_name: str, texts: list[str]) -> np.ndarray:
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name)
    emb = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
    return np.asarray(emb)


def embed_openai(model_name: str, texts: list[str]) -> np.ndarray:
    from openai import OpenAI

    client = OpenAI()
    # batch in groups of 100 to be polite
    embs: list[list[float]] = []
    for i in range(0, len(texts), 100):
        chunk = texts[i : i + 100]
        resp = client.embeddings.create(model=model_name, input=chunk)
        embs.extend(d.embedding for d in resp.data)
    arr = np.asarray(embs)
    # normalize for cosine similarity
    arr = arr / np.linalg.norm(arr, axis=1, keepdims=True)
    return arr


def cosine_sim_matrix(emb: np.ndarray) -> np.ndarray:
    # already normalized
    return emb @ emb.T


def category_pair_stats(
    sim: np.ndarray, passages: list[Passage]
) -> dict[str, float]:
    """Core statistics for the central question."""
    n = len(passages)
    cats = [p.category for p in passages]
    trads = [p.tradition for p in passages]

    nondual_within_trad = []   # nondual, same tradition
    nondual_cross_trad = []    # nondual, different traditions
    nondual_to_dualistic = []  # nondual vs dualistic
    nondual_to_noncontemp = [] # nondual vs non-contemplative
    dualistic_to_dualistic = []
    dualistic_to_noncontemp = []

    for i in range(n):
        for j in range(i + 1, n):
            s = float(sim[i, j])
            ci, cj = cats[i], cats[j]
            ti, tj = trads[i], trads[j]
            if ci == "nondual" and cj == "nondual":
                if ti == tj:
                    nondual_within_trad.append(s)
                else:
                    nondual_cross_trad.append(s)
            elif {ci, cj} == {"nondual", "dualistic"}:
                nondual_to_dualistic.append(s)
            elif {ci, cj} == {"nondual", "non_contemplative"}:
                nondual_to_noncontemp.append(s)
            elif ci == "dualistic" and cj == "dualistic":
                dualistic_to_dualistic.append(s)
            elif {ci, cj} == {"dualistic", "non_contemplative"}:
                dualistic_to_noncontemp.append(s)

    def mean(lst): return float(np.mean(lst)) if lst else float("nan")

    return {
        "nondual_within_trad_mean": mean(nondual_within_trad),
        "nondual_within_trad_n": len(nondual_within_trad),
        "nondual_cross_trad_mean": mean(nondual_cross_trad),
        "nondual_cross_trad_n": len(nondual_cross_trad),
        "nondual_to_dualistic_mean": mean(nondual_to_dualistic),
        "nondual_to_dualistic_n": len(nondual_to_dualistic),
        "nondual_to_noncontemp_mean": mean(nondual_to_noncontemp),
        "nondual_to_noncontemp_n": len(nondual_to_noncontemp),
        "dualistic_to_dualistic_mean": mean(dualistic_to_dualistic),
        "dualistic_to_dualistic_n": len(dualistic_to_dualistic),
        "dualistic_to_noncontemp_mean": mean(dualistic_to_noncontemp),
        "dualistic_to_noncontemp_n": len(dualistic_to_noncontemp),
    }


def permutation_test_cross_vs_to_dualistic(
    sim: np.ndarray, passages: list[Passage], n_perm: int = 5000, seed: int = 0
) -> dict[str, float]:
    """
    Permutation test for the core hypothesis:
        H1: nondual_cross_trad_mean > nondual_to_dualistic_mean

    We permute category labels and recompute the difference. Two-sided p-value.
    """
    rng = random.Random(seed)
    cats = [p.category for p in passages]
    trads = [p.tradition for p in passages]
    n = len(passages)

    def diff(category_assignment):
        cross_sims = []
        to_dual_sims = []
        for i in range(n):
            for j in range(i + 1, n):
                ci, cj = category_assignment[i], category_assignment[j]
                ti, tj = trads[i], trads[j]
                s = float(sim[i, j])
                if ci == "nondual" and cj == "nondual" and ti != tj:
                    cross_sims.append(s)
                elif {ci, cj} == {"nondual", "dualistic"}:
                    to_dual_sims.append(s)
        if not cross_sims or not to_dual_sims:
            return float("nan")
        return float(np.mean(cross_sims) - np.mean(to_dual_sims))

    observed = diff(cats)
    perm_cats = list(cats)
    null_diffs = []
    for _ in range(n_perm):
        rng.shuffle(perm_cats)
        d = diff(perm_cats)
        if not np.isnan(d):
            null_diffs.append(d)

    null_arr = np.asarray(null_diffs)
    # one-sided: how many permutations meet or exceed the observed difference?
    p_one_sided = float((null_arr >= observed).mean())
    # two-sided
    p_two_sided = float((np.abs(null_arr) >= abs(observed)).mean())
    return {
        "observed_diff": observed,
        "null_mean": float(null_arr.mean()),
        "null_std": float(null_arr.std()),
        "p_one_sided": p_one_sided,
        "p_two_sided": p_two_sided,
        "n_perm": int(len(null_arr)),
    }


def cluster_and_score(emb: np.ndarray, passages: list[Passage]) -> dict[str, float]:
    """Run several clustering methods and score them against the category labels."""
    from sklearn.cluster import KMeans, AgglomerativeClustering
    from sklearn.metrics import (
        adjusted_rand_score,
        normalized_mutual_info_score,
        silhouette_score,
    )

    cats = [p.category for p in passages]
    cat_set = sorted(set(cats))
    cat_idx = {c: i for i, c in enumerate(cat_set)}
    cat_labels = np.asarray([cat_idx[c] for c in cats])
    k = len(cat_set)  # 3: nondual / dualistic / non_contemplative

    out: dict[str, float] = {"k": k}

    # k-means at the natural k
    km = KMeans(n_clusters=k, n_init=20, random_state=0).fit(emb)
    out["kmeans_ari"] = float(adjusted_rand_score(cat_labels, km.labels_))
    out["kmeans_nmi"] = float(normalized_mutual_info_score(cat_labels, km.labels_))

    # agglomerative
    ag = AgglomerativeClustering(n_clusters=k, linkage="average").fit(emb)
    out["agglo_ari"] = float(adjusted_rand_score(cat_labels, ag.labels_))
    out["agglo_nmi"] = float(normalized_mutual_info_score(cat_labels, ag.labels_))

    # silhouette under the *true* category labels (positive => categories
    # are well-separated in embedding space; negative => they overlap)
    try:
        out["silhouette_true_categories"] = float(
            silhouette_score(emb, cat_labels, metric="cosine")
        )
    except Exception:
        out["silhouette_true_categories"] = float("nan")

    return out


def plot_projection(
    emb: np.ndarray,
    passages: list[Passage],
    out_path: Path,
    method: str = "umap",
    title: str = "",
):
    import matplotlib.pyplot as plt

    if method == "umap":
        try:
            import umap

            reducer = umap.UMAP(
                n_neighbors=10, min_dist=0.15, metric="cosine", random_state=0
            )
            xy = reducer.fit_transform(emb)
        except ImportError:
            print("[warn] umap-learn not installed; falling back to t-SNE for UMAP plot")
            method = "tsne"

    if method == "tsne":
        from sklearn.manifold import TSNE

        xy = TSNE(
            n_components=2, perplexity=15, metric="cosine", init="pca", random_state=0
        ).fit_transform(emb)

    cats = [p.category for p in passages]
    trads = [p.tradition for p in passages]

    cat_to_color = {
        "nondual": "tab:blue",
        "dualistic": "tab:orange",
        "non_contemplative": "tab:gray",
    }
    trads_unique = sorted(set(trads))
    # use a marker per tradition (cycled if more traditions than markers)
    markers = ["o", "s", "^", "v", "D", "P", "X", "*", "<", ">", "h", "p"]
    trad_to_marker = {t: markers[i % len(markers)] for i, t in enumerate(trads_unique)}

    fig, ax = plt.subplots(figsize=(11, 9))
    for cat, color in cat_to_color.items():
        for trad in trads_unique:
            mask = np.asarray([(c == cat and t == trad) for c, t in zip(cats, trads)])
            if not mask.any():
                continue
            ax.scatter(
                xy[mask, 0],
                xy[mask, 1],
                c=color,
                marker=trad_to_marker[trad],
                s=70,
                edgecolors="black",
                linewidths=0.5,
                alpha=0.85,
                label=f"{cat} | {trad}",
            )
    ax.set_title(title or method.upper())
    ax.set_xlabel(f"{method.upper()}-1")
    ax.set_ylabel(f"{method.upper()}-2")
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=7)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def tradition_similarity_matrix(
    sim: np.ndarray, passages: list[Passage]
) -> tuple[list[str], np.ndarray]:
    trads = sorted({p.tradition for p in passages})
    idx_by_trad: dict[str, list[int]] = {t: [] for t in trads}
    for i, p in enumerate(passages):
        idx_by_trad[p.tradition].append(i)

    mat = np.zeros((len(trads), len(trads)))
    for i, ti in enumerate(trads):
        for j, tj in enumerate(trads):
            ii = idx_by_trad[ti]
            jj = idx_by_trad[tj]
            block = sim[np.ix_(ii, jj)]
            if ti == tj:
                # mean off-diagonal within tradition
                mask = ~np.eye(len(ii), dtype=bool)
                mat[i, j] = float(block[mask].mean()) if mask.any() else float("nan")
            else:
                mat[i, j] = float(block.mean())
    return trads, mat


def save_tradition_csv(
    trads: list[str], mat: np.ndarray, out_path: Path
) -> None:
    import csv

    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([""] + trads)
        for i, t in enumerate(trads):
            w.writerow([t] + [f"{v:.4f}" for v in mat[i]])


def summarize(
    stats: dict[str, float],
    perm: dict[str, float],
    cluster: dict[str, float],
    passages: list[Passage],
    model_name: str,
) -> str:
    lines = []
    lines.append(f"# Phase 0 prototype results")
    lines.append(f"model: {model_name}")
    lines.append(f"n_passages: {len(passages)}")
    n_by_cat: dict[str, int] = {}
    n_by_trad: dict[str, int] = {}
    for p in passages:
        n_by_cat[p.category] = n_by_cat.get(p.category, 0) + 1
        n_by_trad[p.tradition] = n_by_trad.get(p.tradition, 0) + 1
    lines.append(f"by category: {n_by_cat}")
    lines.append(f"by tradition: {n_by_trad}")
    lines.append("")
    lines.append("## Pairwise similarity means (cosine, normalized embeddings)")
    for k, v in stats.items():
        lines.append(f"  {k}: {v}")
    lines.append("")
    lines.append("## Core hypothesis test")
    lines.append("  H1: nondual_cross_trad_mean > nondual_to_dualistic_mean")
    diff = stats["nondual_cross_trad_mean"] - stats["nondual_to_dualistic_mean"]
    lines.append(f"  observed diff: {diff:+.4f}")
    lines.append(f"  permutation null mean: {perm['null_mean']:+.4f} (std {perm['null_std']:.4f})")
    lines.append(f"  one-sided p (cross > to-dualistic): {perm['p_one_sided']:.4f}")
    lines.append(f"  two-sided p:                         {perm['p_two_sided']:.4f}")
    lines.append(f"  n permutations: {perm['n_perm']}")
    lines.append("")
    lines.append("## Clustering recovery of the (nondual / dualistic / non_contemplative) labels")
    for k, v in cluster.items():
        lines.append(f"  {k}: {v}")
    lines.append("")
    lines.append("## Reading the result")
    lines.append("  - ARI/NMI near 1 means embeddings already separate the three categories.")
    lines.append("  - silhouette > 0 means categories are coherent clusters under cosine distance.")
    lines.append("  - The key number: nondual_cross_trad_mean > nondual_to_dualistic_mean,")
    lines.append("    significant under permutation, would be the Phase 0 positive signal.")
    lines.append("  - This is a rough cut. Do not over-interpret; design rigorous v1 next.")
    return "\n".join(lines)


def run_for_model(
    model_name: str,
    passages: list[Passage],
    backend: str,
    out_root: Path,
) -> None:
    safe_name = model_name.replace("/", "__").replace(":", "_")
    out_dir = out_root / safe_name
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== {model_name} ===")
    texts = [p.passage for p in passages]
    if backend == "openai":
        emb = embed_openai(model_name, texts)
    else:
        emb = embed_sentence_transformers(model_name, texts)

    np.save(out_dir / "embeddings.npy", emb)

    sim = cosine_sim_matrix(emb)
    np.save(out_dir / "similarity.npy", sim)

    stats = category_pair_stats(sim, passages)
    perm = permutation_test_cross_vs_to_dualistic(sim, passages)
    cluster = cluster_and_score(emb, passages)

    trads, trad_mat = tradition_similarity_matrix(sim, passages)
    save_tradition_csv(trads, trad_mat, out_dir / "tradition_sim.csv")

    summary = summarize(stats, perm, cluster, passages, model_name)
    (out_dir / "summary.txt").write_text(summary, encoding="utf-8")
    print(summary)

    plot_projection(emb, passages, out_dir / "umap.png", method="umap",
                    title=f"UMAP — {model_name}")
    plot_projection(emb, passages, out_dir / "tsne.png", method="tsne",
                    title=f"t-SNE — {model_name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corpus",
        type=Path,
        default=CORPUS_PATH,
        help="Path to passages.jsonl",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Single model name (sentence-transformers or OpenAI). If both --model and --models are given, --models wins.",
    )
    parser.add_argument(
        "--models",
        type=str,
        default=None,
        help="Comma-separated list of model names",
    )
    parser.add_argument(
        "--backend",
        type=str,
        choices=["sentence-transformers", "openai"],
        default="sentence-transformers",
        help="Embedding backend",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=RESULTS_DIR,
        help="Results directory",
    )
    args = parser.parse_args()

    if args.models:
        models = [m.strip() for m in args.models.split(",") if m.strip()]
    elif args.model:
        models = [args.model]
    else:
        models = DEFAULT_MODELS

    passages = load_corpus(args.corpus)
    print(f"Loaded {len(passages)} passages from {args.corpus}")

    args.out.mkdir(parents=True, exist_ok=True)
    for m in models:
        run_for_model(m, passages, args.backend, args.out)


if __name__ == "__main__":
    main()
