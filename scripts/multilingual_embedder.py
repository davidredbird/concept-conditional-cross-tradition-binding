"""
Multilingual embedding pipeline for Phase 1c (non-English source analysis).

Wraps multilingual transformer models with two backends, dispatching by model:

  - intfloat/multilingual-e5-large
      Backend: ONNX Runtime + tokenizers (pure ONNX path, no torch).
      Mean-pool + L2-normalize. Requires 'passage: ' (or 'query: ') prefix
      on inputs per the model card. Handles 100 languages including Sanskrit
      (Devanagari) and Pali. Uses ONNX external-data format.

  - sentence-transformers/LaBSE
      Backend: sentence-transformers (uses torch under the hood).
      Native LaBSE pipeline: CLS + tanh + dense projection + L2-normalize.
      Using sentence-transformers directly handles the dense projection
      correctly, which mean-pool on BERT output does not (mean-pool fallback
      gives 1/5 correct on validation vs 5/5 canonical).

The two backends produce comparable unit-normalized 768/1024-dim embeddings.
Cross-model replication on Phase 1c uses both: e5-large via ONNX, LaBSE via
sentence-transformers.

Usage:
    from multilingual_embedder import MultilingualEmbedder

    emb = MultilingualEmbedder('intfloat/multilingual-e5-large')
    vecs = emb.encode(texts)  # default prefix 'passage: ' applied automatically

    emb = MultilingualEmbedder('sentence-transformers/LaBSE')
    vecs = emb.encode(texts)  # canonical LaBSE pipeline
"""

from __future__ import annotations

import warnings
from typing import Iterable

import numpy as np
import onnxruntime as ort
from huggingface_hub import hf_hub_download
from tokenizers import Tokenizer


_KNOWN_MODELS: dict[str, dict] = {
    "intfloat/multilingual-e5-large": {
        "backend": "onnx",
        "onnx_files": ["onnx/model.onnx", "onnx/model.onnx_data"],
        "onnx_main": "onnx/model.onnx",
        "tokenizer_file": "onnx/tokenizer.json",
        "default_prefix": "passage: ",
        "dim": 1024,
        "notes": "Use 'query: ' prefix for queries, 'passage: ' for documents.",
    },
    "sentence-transformers/LaBSE": {
        "backend": "sentence_transformers",
        "default_prefix": "",
        "dim": 768,
        "notes": "Canonical LaBSE pipeline: CLS + tanh + dense + L2norm.",
    },
}


class MultilingualEmbedder:
    """Dispatcher for multilingual embedding models.

    Backends:
      - 'onnx': pure ONNX Runtime + tokenizers. Used for e5-large.
      - 'sentence_transformers': uses the sentence-transformers library
        (which uses torch). Used for LaBSE because its canonical pipeline
        includes a dense projection layer not present in the ONNX export.
    """

    def __init__(self, model_id: str) -> None:
        if model_id not in _KNOWN_MODELS:
            raise ValueError(
                f"Unknown model {model_id!r}; supported: {list(_KNOWN_MODELS)}"
            )
        self.model_id = model_id
        self.config = _KNOWN_MODELS[model_id]
        self.backend = self.config["backend"]
        self.default_prefix = self.config["default_prefix"]
        self.dim = self.config["dim"]
        # Backwards-compat attribute (used by validation script)
        self.pooling = self.backend

        if self.backend == "onnx":
            self._init_onnx()
        elif self.backend == "sentence_transformers":
            self._init_st()
        else:
            raise ValueError(f"Unknown backend {self.backend!r}")

    def _init_onnx(self) -> None:
        # External-data ONNX (e5-large) needs all referenced files cached locally
        for f in self.config["onnx_files"]:
            hf_hub_download(self.model_id, f)
        onnx_path = hf_hub_download(self.model_id, self.config["onnx_main"])
        tokenizer_path = hf_hub_download(self.model_id, self.config["tokenizer_file"])
        self.tokenizer = Tokenizer.from_file(tokenizer_path)
        self.tokenizer.enable_padding()
        self.tokenizer.enable_truncation(max_length=512)
        self.session = ort.InferenceSession(
            onnx_path, providers=["CPUExecutionProvider"]
        )
        self.input_names = {i.name for i in self.session.get_inputs()}

    def _init_st(self) -> None:
        from sentence_transformers import SentenceTransformer
        self.st_model = SentenceTransformer(self.model_id)

    def encode(
        self,
        texts: Iterable[str],
        batch_size: int = 16,
        prefix: str | None = None,
    ) -> np.ndarray:
        """Encode a list of texts. Applies model-specific prefix if not overridden."""
        texts_list = list(texts)
        eff_prefix = self.default_prefix if prefix is None else prefix
        if eff_prefix:
            texts_list = [eff_prefix + t for t in texts_list]
        if self.backend == "onnx":
            return self._encode_onnx(texts_list, batch_size)
        return self._encode_st(texts_list, batch_size)

    def _encode_onnx(self, texts: list[str], batch_size: int) -> np.ndarray:
        out: list[np.ndarray] = []
        for start in range(0, len(texts), batch_size):
            batch = texts[start : start + batch_size]
            encs = self.tokenizer.encode_batch(batch)
            max_len = max(len(e.ids) for e in encs)
            input_ids = np.zeros((len(encs), max_len), dtype=np.int64)
            attn = np.zeros((len(encs), max_len), dtype=np.int64)
            for i, e in enumerate(encs):
                input_ids[i, : len(e.ids)] = e.ids
                attn[i, : len(e.attention_mask)] = e.attention_mask
            inputs = {"input_ids": input_ids, "attention_mask": attn}
            if "token_type_ids" in self.input_names:
                inputs["token_type_ids"] = np.zeros_like(input_ids)
            outputs = self.session.run(None, inputs)
            token_emb = outputs[0]  # (B, L, H)
            # Mean-pool
            mask_f = attn[:, :, None].astype(np.float32)
            summed = (token_emb * mask_f).sum(axis=1)
            counts = np.maximum(mask_f.sum(axis=1), 1e-9)
            pooled = summed / counts
            pooled = pooled / np.maximum(
                np.linalg.norm(pooled, axis=1, keepdims=True), 1e-9
            )
            out.append(pooled.astype(np.float32))
        return np.concatenate(out, axis=0)

    def _encode_st(self, texts: list[str], batch_size: int) -> np.ndarray:
        vecs = self.st_model.encode(
            texts, batch_size=batch_size, normalize_embeddings=True,
            show_progress_bar=False,
        )
        return np.asarray(vecs, dtype=np.float32)


if __name__ == "__main__":
    # Quick sanity check (Sanskrit + English BG verse cross-lingual match)
    import json
    import sys
    from pathlib import Path

    REPO_ROOT = Path(__file__).resolve().parent.parent
    pairs_path = REPO_ROOT / "corpus" / "phase1c_validation_pairs.jsonl"
    pairs = [json.loads(line) for line in pairs_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    san = [p["sanskrit_devanagari"] for p in pairs]
    eng = [p["english"] for p in pairs]

    model_id = sys.argv[1] if len(sys.argv) > 1 else "intfloat/multilingual-e5-large"
    print(f"Loading {model_id} ...")
    emb = MultilingualEmbedder(model_id)
    san_v = emb.encode(san)
    eng_v = emb.encode(eng)
    sim = san_v @ eng_v.T
    diag = np.diag(sim)
    off = sim[~np.eye(len(san), dtype=bool)]
    correct = sum(1 for i in range(len(san)) if np.argmax(sim[i]) == i)
    print(
        f"Same-verse mean: {diag.mean():.4f}  Diff-verse mean: {off.mean():.4f}  "
        f"Separation: {diag.mean() - off.mean():+.4f}  Correct: {correct}/{len(san)}"
    )
