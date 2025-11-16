
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Callable, Dict, Any, Optional
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

@dataclass
class Chunk:
    text: str
    doc_name: str
    client: str = ""
    matter: str = ""
    chunk_id: int = 0

class HybridRetriever:
    """
    Lightweight hybrid retriever:
      - TF-IDF (1–2 gram) sparse vectors
      - Cosine similarity search
      - Optional metadata filter (client/matter/name)
      - Extractive QA on top-k hits (no LLM generation)
    """
    def __init__(self, chunks: List[Chunk]):
        if not chunks:
            raise ValueError("No chunks provided")
        self.chunks: List[Chunk] = chunks

        corpus = [c.text for c in chunks]
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=50000,
            lowercase=True,
            token_pattern=r"(?u)\b\w+\b",
        )
        X = self.vectorizer.fit_transform(corpus)        # sparse CSR
        self.vecs = X.astype(np.float32)
        # row (chunk) L2 norms
        self.norms = np.sqrt(self.vecs.power(2).sum(axis=1)).A1
        self.norms[self.norms == 0] = 1.0  # safety

    # ---------- internals ----------
    def _qvec(self, query: str):
        v = self.vectorizer.transform([query]).astype(np.float32)
        n = float(np.sqrt(v.power(2).sum()).A1[0]) or 1.0
        return v, n

    def _cosine_scores(self, qv, qn) -> np.ndarray:
        # sims = (V * q) / (||V|| * ||q||)
        sims = (self.vecs @ qv.T).toarray().ravel()
        denom = self.norms * qn
        denom[denom == 0] = 1e-9
        return sims / denom

    # ---------- API ----------
    def search(
        self,
        query: str,
        k: int = 3,
        filter_fn: Optional[Callable[[Chunk], bool]] = None
    ) -> List[Dict[str, Any]]:
        qv, qn = self._qvec(query)
        sims = self._cosine_scores(qv, qn)

        # top-k indices
        k_eff = max(1, min(k, sims.size))
        idx = np.argpartition(-sims, kth=k_eff - 1)[:k_eff]
        idx = idx[np.argsort(-sims[idx])]

        hits: List[Dict[str, Any]] = []
        rank = 1
        for i in idx:
            ch = self.chunks[int(i)]
            if filter_fn and not filter_fn(ch):
                continue
            hits.append({
                "rank": rank,
                "doc_name": ch.doc_name,
                "client": ch.client,
                "matter": ch.matter,
                "chunk_id": ch.chunk_id,
                "score": float(sims[int(i)]),
                "text": ch.text,
                "preview": re.sub(r"\s+", " ", ch.text[:800]).strip(),
            })
            rank += 1
            if len(hits) >= k:
                break
        return hits

    def ask(self, question: str, k: int = 3, max_new_tokens: int = 220):
        # 1) retrieve
        hits = self.search(question, k=k)

        # 2) stitch retrieved text
        context = "\n\n".join(h["text"] for h in hits)

        # 3) extractive answer (no LLM generation)
        from services.qa_llm import answer_from_context_extractive
        answer = answer_from_context_extractive(context, question, max_len=max_new_tokens)

        # 4) compact sources for UI
        sources = [{
            "rank": h["rank"],
            "doc_name": h["doc_name"],
            "client": h["client"],
            "chunk_id": h["chunk_id"],
            "score": h["score"],
            "preview": h["preview"],
        } for h in hits]

        return (answer or "Not specified"), sources
