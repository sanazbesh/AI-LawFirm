# services/rag_router.py
import re
import streamlit as st
from typing import List, Dict
from services.retriever_tf_idf import TinyTfidfQARetriever
from services.retriever_hybrid import HybridRetriever, Chunk


try:
 
    from summarizer2 import extract_text as _extract_text_from_path  
except Exception:
    _extract_text_from_path = None


# ---------- tiny deterministic tools ( fast answers) ----------
def _src(label, preview):
    return [{"rank": 1, "doc_name": label, "client": "—", "chunk_id": 0, "score": 1.0, "preview": preview}]

def _norm(q: str) -> str:
    t = re.sub(r"[^a-z0-9 ]+", " ", (q or "").lower())
    t = " " + re.sub(r"\s+", " ", t) + " "
    # light synonym/alias normalization
    t = (t.replace(" customers ", " clients ")
           .replace(" docs ", " documents ")
           .replace(" files ", " documents ")
           .replace(" matters ", " matters "))
    return t

def _has_any(t: str, phrases) -> bool:
    return any(p in t for p in phrases)

def answer_via_tools(q: str):
    docs    = st.session_state.get("documents", []) or []
    clients = st.session_state.get("clients", []) or []
    times   = st.session_state.get("time_entries", []) or []

    def norm(s): return " " + re.sub(r"[^a-z0-9 ]+", " ", (s or "").lower()) + " "
    nl = norm(q).replace("customers", "clients").replace("docs", "documents")

    # count clients
    if any(k in nl for k in (" how many ", " number of ", " count ", " total ")) and " clients " in nl:
        return True, str(len(clients)), _src("(internal) client registry", ", ".join(c.get("name","") for c in clients[:12]))

    # list client names
    if any(k in nl for k in (" name the clients", " list clients", " show clients", " clients list ")):
        if not clients:
            return True, "Not specified", []
        names = ", ".join(c.get("name","") for c in clients if c.get("name"))
        return True, (names or "Not specified"), _src("(internal) client registry", names)

    # count documents
    if any(k in nl for k in (" how many ", " number of ", " count ", " total ")) and (" document " in nl or " documents " in nl):
        return True, str(len(docs)), _src("(internal) document registry", ", ".join(d.get("name","") for d in docs[:12]))

    # list doc names
    if any(k in nl for k in (" name the documents", " list documents", " show documents", " documents list ")):
        if not docs:
            return True, "Not specified", []
        names = ", ".join(d.get("name","") for d in docs if d.get("name"))
        return True, (names or "Not specified"), _src("(internal) document registry", names)

    return False, "", []




# ---------- build / cache retriever ----------
_RAW_TEXT_KEYS = ("content_text", "content", "text", "raw_text")

def _pick_raw_text(d: Dict) -> str:
    # 1) prefer any raw text fields on the doc dict
    for k in _RAW_TEXT_KEYS:
        v = (d.get(k) or "").strip()
        if v:
            return v
    # 2) optional fallback: if you store a file path, try to extract
    p = (d.get("path") or d.get("filepath") or "").strip()
    if p and _extract_text_from_path:
        try:
            t = _extract_text_from_path(p)
            if t and t.strip():
                return t.strip()
        except Exception:
            pass
    # 3) final fallback: nothing
    return ""

# --- build / cache retriever ---
def _extract_text_fields(d: dict) -> str:
    # prefer real body text; try multiple common keys
    for key in ("content_text", "content", "text", "body", "raw_text"):
        val = d.get(key)
        if isinstance(val, str) and val.strip():
            return val
    return ""

def _prep_documents_for_index():
    docs = st.session_state.get("documents", []) or []
    prepped = []
    for d in docs:
        text = (d.get("content_text") or d.get("content") or d.get("summary") or "").strip()
        if not text:
            continue  # skip unindexable docs
        prepped.append({
            "name": d.get("name", "Untitled"),
            "client": d.get("client", ""),
            "matter": d.get("matter", ""),
            "type": d.get("type", ""),
            "status": d.get("status", ""),
            "text": text,
            "summary": d.get("summary") or "",
        })
    return prepped

def _split_chunks(text: str, words: int = 320, overlap: int = 64):
    toks = re.findall(r"\S+", text)
    out, i, cid = [], 0, 0
    while i < len(toks):
        piece = " ".join(toks[i:i+words])
        if piece.strip():
            out.append((cid, piece))
            cid += 1
        i += max(1, words - overlap)
    return out


def _rebuild_index():
    prepped = _prep_documents_for_index()
    chunks  = TinyTfidfQARetriever.build_chunks_from_documents(prepped, words=350, overlap=50)
    # SAFE: even if chunks is empty, retriever won't raise
    st.session_state.qa_engine = TinyTfidfQARetriever(chunks)
    st.session_state.qa_digest = f"{len(prepped)}|{sum(len(p['text']) for p in prepped)}"

def ensure_qa_index():
    docs = st.session_state.get("documents", []) or []
    digest = f"{len(docs)}|{sum(len((d.get('content_text') or d.get('content') or d.get('summary') or '')) for d in docs)}"
    if st.session_state.get("qa_engine") is None or st.session_state.get("qa_digest") != digest:
        _rebuild_index()

# ---------- main entry ----------
def answer_question_hybrid(q: str, k: int = 3, max_new_tokens: int = 220):
    # A) tools (fast, deterministic)
    handled, ans, srcs = answer_via_tools(q)
    if handled:
        return ans, srcs

    # B) retrieval + LLM QA strictly from retrieved raw text chunks
    ensure_qa_index()

    # Narrow to a specific client/matter if the question names one
    name_like = re.findall(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*", q)
    if name_like:
        needles = {n.lower() for n in name_like}
        def _only_same_case(ch):
            hay = f"{ch.client} {ch.matter} {ch.doc_name}".lower()
            return any(n in hay for n in needles)
        # use the retriever's search with metadata filter
        hits = st.session_state.qa_engine.search(q, k=k, filter_fn=_only_same_case)
        if hits:
            from services.qa_llm import answer_from_context_extractive
            context = "\n\n".join(h["text"] for h in hits)
            ans = answer_from_context_extractive(context, q, max_len=max_new_tokens) or "Not specified"
            sources = [{
                "rank": h["rank"], "doc_name": h["doc_name"], "client": h["client"],
                "chunk_id": h["chunk_id"], "score": h["score"], "preview": h["preview"]
            } for h in hits]
            return ans, sources

    # Fallback: normal hybrid ask
    return st.session_state.qa_engine.ask(q, k=k, max_new_tokens=max_new_tokens)
