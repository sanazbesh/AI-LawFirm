# services/retriever_tf_idf.py
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import List, Dict, Iterable, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Optional, used by ask() for extractive answers
try:
    from services.qa_llm import answer_from_context_extractive
except Exception:
    def answer_from_context_extractive(context: str, q: str, max_len: int = 220) -> str:
        qn = q.lower()
        best = ""
        for para in re.split(r"\n{2,}", context):
            if any(tok in para.lower() for tok in qn.split()):
                best = para if len(para) > len(best) else best
        return best[:max_len] if best else ""

@dataclass
class Chunk:
    doc_name: str
    client: str
    chunk_id: int
    text: str
    preview: str
    meta: Dict

class TinyTfidfQARetriever:
    """Tiny TF-IDF retriever with graceful empty-index handling."""

    def __init__(self, chunks: List[Dict]):
        # Normalize to Chunk objects
        self.chunks: List[Chunk] = [
            Chunk(
                doc_name=c.get("doc_name") or c.get("name") or "Document",
                client=c.get("client") or "—",
                chunk_id=int(c.get("chunk_id", 0)),
                text=c.get("text", "") or "",
                preview=(c.get("preview") or (c.get("text", "")[:300])).strip(),
                meta={k: v for k, v in c.items()
                      if k not in {"doc_name", "name", "client", "chunk_id", "text", "preview"}}
            )
            for c in (chunks or [])
            if (c.get("text") or "").strip()
        ]

        # Empty index: keep things consistent and *do not* raise
        if not self.chunks:
            self._empty = True
            self.vectorizer = None
            self.matrix = None
            return

        self._empty = False
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            analyzer="word",
            ngram_range=(1, 2),
            max_df=0.95,
            min_df=1,
            stop_words="english",
        )
        texts = [c.text for c in self.chunks]
        self.matrix = self.vectorizer.fit_transform(texts)  # (N, vocab)

    # ---------- building ----------
    @staticmethod
    def _clean(s: str) -> str:
        return re.sub(r"\s+", " ", (s or "").strip())

    @staticmethod
    def build_chunks_from_documents(docs: Iterable[Dict], words: int = 350, overlap: int = 50) -> List[Dict]:
        """Split each document text into overlapping word chunks."""
        out: List[Dict] = []
        for d in docs or []:
            name = d.get("name") or d.get("doc_name") or "Document"
            client = d.get("client") or "—"
            raw = TinyTfidfQARetriever._clean(d.get("text") or d.get("content_text") or d.get("summary") or "")
            if not raw:
                continue
            tokens = raw.split()
            if not tokens:
                continue
            i = 0
            cid = 0
            while i < len(tokens):
                j = min(i + words, len(tokens))
                chunk_tokens = tokens[i:j]
                text = " ".join(chunk_tokens)
                out.append({
                    "doc_name": name,
                    "client": client,
                    "chunk_id": cid,
                    "text": text,
                    "preview": text[:300],
                })
                cid += 1
                if j == len(tokens):
                    break
                i = max(j - overlap, i + 1)
        return out

    # ---------- retrieval ----------
    def search(self, query: str, k: int = 3, filter_fn=None) -> List[Dict]:
        """Return up to k chunk dicts with score text similarity; supports optional metadata filter."""
        if self._empty:
            return []
        qv = self.vectorizer.transform([query or ""])
        sims = (self.matrix @ qv.T).toarray().ravel()  # cosine on L2-normed tfidf
        order = np.argsort(-sims)  # descending
        hits: List[Dict] = []
        for idx in order:
            if len(hits) >= max(1, k):
                break
            ch = self.chunks[idx]
            if filter_fn and not filter_fn(ch):
                continue
            hits.append({
                "doc_name": ch.doc_name,
                "client": ch.client,
                "chunk_id": ch.chunk_id,
                "text": ch.text,
                "preview": ch.preview,
                "score": float(sims[idx]),
                **(ch.meta or {}),
            })
        return hits

    # ---------- answer ----------
    def ask(self, question: str, k: int = 3, max_new_tokens: int = 220):
        """Retrieve, then extractive answer over the stitched context (no LLM generation)."""
        hits = self.search(question, k)
        if not hits:
            return "Not specified", []
        context = "\n\n".join(h["text"] for h in hits)
        answer = answer_from_context_extractive(context, question, max_len=max_new_tokens)
        sources = []
        for rank, h in enumerate(hits, start=1):
            sources.append({
                "rank": rank,
                "doc_name": h.get("doc_name", "Document"),
                "client": h.get("client", "—"),
                "chunk_id": h.get("chunk_id", 0),
                "score": float(h.get("score", 0.0)),
                "preview": h.get("preview", "")[:800],
            })
        return (answer or "Not specified"), sources
