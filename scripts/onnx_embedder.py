"""
Minimal BERT-class embedding pipeline using only ONNX Runtime + tokenizers.

Sidesteps the WDAC block on torch.dll: ONNX Runtime is Microsoft-signed.
Downloads ONNX model + tokenizer files from HuggingFace, runs inference
on CPU, mean-pools and L2-normalizes to produce sentence embeddings
comparable to sentence-transformers output.

Tested with:
  - sentence-transformers/all-MiniLM-L6-v2  (384-dim, fast)
  - BAAI/bge-small-en-v1.5  (384-dim, higher quality)
  - sentence-transformers/all-mpnet-base-v2  (768-dim, strongest small)
"""

from __future__ import annotations

import numpy as np
from huggingface_hub import hf_hub_download
from tokenizers import Tokenizer
import onnxruntime as ort


def _download_files(repo_id: str, onnx_subpath: str = "onnx/model.onnx") -> tuple[str, str]:
    onnx_path = hf_hub_download(repo_id, onnx_subpath)
    tokenizer_path = hf_hub_download(repo_id, "tokenizer.json")
    return onnx_path, tokenizer_path


class ONNXEmbedder:
    def __init__(self, repo_id: str, onnx_subpath: str = "onnx/model.onnx") -> None:
        self.repo_id = repo_id
        self.onnx_path, self.tokenizer_path = _download_files(repo_id, onnx_subpath)
        self.tokenizer = Tokenizer.from_file(self.tokenizer_path)
        self.tokenizer.enable_padding()
        self.tokenizer.enable_truncation(max_length=512)
        self.session = ort.InferenceSession(
            self.onnx_path, providers=["CPUExecutionProvider"]
        )
        self.input_names = {i.name for i in self.session.get_inputs()}

    def encode(self, texts: list[str], batch_size: int = 32) -> np.ndarray:
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
            token_embeddings = outputs[0]  # (B, L, H)
            mask_f = attn[:, :, None].astype(np.float32)
            summed = (token_embeddings * mask_f).sum(axis=1)
            counts = np.maximum(mask_f.sum(axis=1), 1e-9)
            pooled = summed / counts
            pooled = pooled / np.maximum(
                np.linalg.norm(pooled, axis=1, keepdims=True), 1e-9
            )
            out.append(pooled)
        return np.concatenate(out, axis=0)


def encode_with_model(repo_id: str, texts: list[str]) -> np.ndarray:
    """Convenience function for one-shot encoding."""
    return ONNXEmbedder(repo_id).encode(texts)


if __name__ == "__main__":
    # Quick test
    e = ONNXEmbedder("sentence-transformers/all-MiniLM-L6-v2")
    out = e.encode(["The cat sat on the mat.", "A feline rested on a rug.", "Quantum mechanics is hard."])
    print(out.shape)
    sim = out @ out.T
    print("similarity matrix:")
    print(sim)
