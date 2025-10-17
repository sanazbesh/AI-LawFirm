# app2.py
import os
import json
import time
import math
import re
import tempfile
from collections import Counter
from pathlib import Path
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd


# LLM config
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")   # provider name
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")    # model id
LLM_API_KEY = os.getenv("LLM_API_KEY", "")           # api key

USE_EXTERNAL_LLM = bool(LLM_API_KEY)  # use summarize_text if no key

from summarizer2 import extract_text, summarize_text

# Quiet HF tokenizer warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Streamlit page setup
st.set_page_config(
    page_title="LegalDoc Pro - Document Management Dashboard",
    page_icon="⚖️",
    layout="wide",
)

try:
    from qa_llm import answer_from_context
    BACKEND_LABEL = "qa_llm adapter (LM Studio/Ollama/llama-cpp/Transformers)"
except Exception:
    # Fallback if adapter missing
    from summarizer2 import summarize_text as _fallback_summarize
    BACKEND_LABEL = "summarizer fallback — install LM Studio/Ollama/llama-cpp or transformers"
    def answer_from_context(question, contexts, max_tokens=220):
        prompt = (
            "Answer ONLY from context. If missing, reply exactly: Not specified.\n\n"
            + "\n\n---\n\n".join(contexts[:6])
            + f"\n\nQ: {question}\nA:"
        )
        return _fallback_summarize(prompt, max_len=max_tokens)

# Dev bypass login
BYPASS_LOGIN = True

# Firebase (optional; app works offline)
working_offline = False
auth = None
db = None

try:
    import pyrebase

    firebase_config = {
        "apiKey": "AIzaSyDt6y7YRFVF_zrMTYPn4z4ViHjLbmfMsLQ",
        "authDomain": "trend-summarizer-6f28e.firebaseapp.com",
        "projectId": "trend-summarizer-6f28e",
        "storageBucket": "trend-summarizer-6f28e.firebasestorage.app",
        "messagingSenderId": "655575726457",
        "databaseURL": "https://trend-summarizer-6f28e-default-rtdb.firebaseio.com",
        "appId": "1:655575726457:web:9ae1d0d363c804edc9d7a8",
        "measurementId": "G-HHY482GQKZ",
    }
    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()
    db = firebase.database()
except Exception:
    working_offline = True

# Session state
if "documents" not in st.session_state:
    st.session_state.documents = []
if "clients" not in st.session_state:
    st.session_state.clients = []
if "time_entries" not in st.session_state:
    st.session_state.time_entries = []
if "user" not in st.session_state:
    st.session_state.user = None

# QA engine state
if "qa_engine" not in st.session_state:
    st.session_state.qa_engine = None
if "qa_digest" not in st.session_state:
    st.session_state.qa_digest = None
if "qa_output" not in st.session_state:
    st.session_state.qa_output = None

# ============================================================
# Firebase / subscription helpers (works offline)
# ============================================================
def _user_key(email: str) -> str:
    return (email or "").replace(".", "_")

def _set_db(path_parts, value):
    """Write to Firebase if available; no-op offline."""
    global working_offline
    if working_offline or db is None:
        return
    try:
        ref = db
        for p in path_parts:
            ref = ref.child(p)
        ref.set(value)
    except Exception:
        # If write fails, switch offline
        working_offline = True

def _get_db(path_parts):
    """Read from Firebase if available; None offline/failure."""
    global working_offline
    if working_offline or db is None:
        return None
    try:
        ref = db
        for p in path_parts:
            ref = ref.child(p)
        return ref.get().val()
    except Exception:
        working_offline = True
        return None

def create_user_subscription(email, plan_type):
    user_key = _user_key(email)
    plans = {
        "trial": {
            "document_limit": 25,
            "client_limit": 10,
            "storage_limit_mb": 100,
            "has_advanced_reports": False,
            "has_time_tracking": True,
        },
        "basic": {
            "document_limit": 100,
            "client_limit": 50,
            "storage_limit_mb": 500,
            "has_advanced_reports": False,
            "has_time_tracking": True,
        },
        "premium": {
            "document_limit": "unlimited",
            "client_limit": "unlimited",
            "storage_limit_mb": "unlimited",
            "has_advanced_reports": True,
            "has_time_tracking": True,
        },
    }
    user_data = {
        "email": email,
        "subscription_type": plan_type,
        "subscription_status": "active" if plan_type != "trial" else "trial",
        "payment_date": datetime.now().isoformat(),
        "usage_limits": plans.get(plan_type, plans["trial"]),
        "current_usage": {
            "documents_count": 0,
            "clients_count": 0,
            "storage_used_mb": 0,
            "last_reset_date": datetime.now().replace(day=1).isoformat(),
        },
    }
    _set_db(["users", user_key], user_data)

def initialize_user_data(email):
    user_key = _user_key(email)
    data = _get_db(["users", user_key])
    if not data:
        create_user_subscription(email, "trial")

def get_user_info(email):
    return _get_db(["users", _user_key(email)]) or None

def check_usage_limits(email, action_type="document"):
    info = get_user_info(email) or {
        "subscription_type": "trial",
        "subscription_status": "trial",
        "usage_limits": {
            "document_limit": 25,
            "client_limit": 10,
        },
        "current_usage": {"documents_count": 0, "clients_count": 0},
    }
    status = info.get("subscription_status", "trial")
    if status not in ["active", "trial"]:
        return False, "Subscription expired. Please upgrade your plan."

    limits = info.get("usage_limits", {})
    current = info.get("current_usage", {})
    if action_type == "document":
        lim = limits.get("document_limit", 0)
        cur = current.get("documents_count", 0)
        if lim != "unlimited" and cur >= lim:
            plan = info.get("subscription_type", "trial")
            return False, f"Document limit of {lim} reached for {plan} plan. Please upgrade."
    elif action_type == "client":
        lim = limits.get("client_limit", 0)
        cur = current.get("clients_count", 0)
        if lim != "unlimited" and cur >= lim:
            plan = info.get("subscription_type", "trial")
            return False, f"Client limit of {lim} reached for {plan} plan. Please upgrade."
    return True, "ok"

def increment_usage(email, action_type="document"):
    info = get_user_info(email)
    if not info:
        return
    cur = info.get("current_usage", {})
    if action_type == "document":
        cur["documents_count"] = int(cur.get("documents_count", 0)) + 1
    elif action_type == "client":
        cur["clients_count"] = int(cur.get("clients_count", 0)) + 1
    info["current_usage"] = cur
    _set_db(["users", _user_key(email)], info)

def is_logged_in():
    return st.session_state.get("user") is not None

def show_usage_info():
    if not is_logged_in():
        return
    email = st.session_state["user"]["email"]
    info = get_user_info(email)
    if not info:
        return
    plan = info.get("subscription_type", "trial")
    status = info.get("subscription_status", "trial")
    limits = info.get("usage_limits", {})
    current = info.get("current_usage", {})

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Plan", plan.title())
    with c2:
        dl, dc = limits.get("document_limit", 0), current.get("documents_count", 0)
        st.metric("Documents", f"{dc}/∞" if dl == "unlimited" else f"{dc}/{dl}")
    with c3:
        cl, cc = limits.get("client_limit", 0), current.get("clients_count", 0)
        st.metric("Clients", f"{cc}/∞" if cl == "unlimited" else f"{cc}/{cl}")
    with c4:
        st.metric("Status", status.title())

    if working_offline:
        st.warning("Working offline (Firebase not reachable).", icon="⚠️")
    elif status == "trial":
        st.info("You're on a trial plan. Upgrade for more features.")

# Dev auto-login
if BYPASS_LOGIN and not is_logged_in():
    st.session_state["user"] = {"email": "dev@local"}
    try:
        initialize_user_data("dev@local")
    except Exception:
        pass  # offline is fine

# ============================================================
# Demo data (first run)
# ============================================================
if not st.session_state.documents:
    st.session_state.documents = [
        {
            "id": 1,
            "name": "Divorce_Settlement_Agreement_Smith.pdf",
            "client": "John Smith",
            "matter": "Divorce Proceedings",
            "type": "Settlement Agreement",
            "date_uploaded": "2024-01-15",
            "file_size": "2.1 MB",
            "status": "Final",
            "content": None,
            "summary": None,
        },
        {
            "id": 2,
            "name": "LLC_Formation_TechCorp.pdf",
            "client": "TechCorp LLC",
            "matter": "Business Formation",
            "type": "Articles of Incorporation",
            "date_uploaded": "2024-01-20",
            "file_size": "1.8 MB",
            "status": "Draft",
            "content": None,
            "summary": None,
        },
        {
            "id": 3,
            "name": "Child_Custody_Motion_Johnson.pdf",
            "client": "Mary Johnson",
            "matter": "Child Custody",
            "type": "Court Motion",
            "date_uploaded": "2024-01-25",
            "file_size": "3.2 MB",
            "status": "Filed",
            "content": None,
            "summary": None,
        },
        {
            "id": 4,
            "name": "Prenuptial_Agreement_Williams.pdf",
            "client": "Sarah Williams",
            "matter": "Prenuptial Agreement",
            "type": "Contract",
            "date_uploaded": "2024-01-30",
            "file_size": "1.5 MB",
            "status": "Under Review",
            "content": None,
            "summary": None,
        },
        {
            "id": 5,
            "name": "Business_Partnership_Agreement_ABC.pdf",
            "client": "ABC Partners",
            "matter": "Partnership Formation",
            "type": "Partnership Agreement",
            "date_uploaded": "2024-02-05",
            "file_size": "2.8 MB",
            "status": "Final",
            "content": None,
            "summary": None,
        },
    ]

if not st.session_state.clients:
    st.session_state.clients = [
        {"name": "John Smith", "type": "Individual", "active_matters": 1},
        {"name": "TechCorp LLC", "type": "Business", "active_matters": 2},
        {"name": "Mary Johnson", "type": "Individual", "active_matters": 1},
        {"name": "Sarah Williams", "type": "Individual", "active_matters": 1},
        {"name": "ABC Partners", "type": "Business", "active_matters": 1},
    ]

# ============================================================
# Sidebar
# ============================================================
def render_sidebar():
    st.sidebar.title("⚖️ LegalDoc Pro")
    st.sidebar.markdown("*Document Management for Small Law Firms*")

    if is_logged_in():
        user_email = st.session_state["user"]["email"]
        st.sidebar.markdown(f"Welcome, **{user_email}**!")
        info = get_user_info(user_email)
        if info:
            plan = info.get("subscription_type", "trial")
            st.sidebar.markdown(f"Plan: **{plan.title()}**")
            if plan == "trial":
                if st.sidebar.button("🚀 Upgrade Plan", key="btn_upgrade_plan"):
                    st.sidebar.markdown(
                        "[Upgrade Now](https://prolexisanalytics.com/pricing)"
                    )

    page = st.sidebar.radio(
        "Navigate",
        ["Dashboard", "Document Management", "Client Management", "Time Tracking", "Reports", "Questions"],
        key="nav_radio",
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("*LegalDoc Pro v1.0*")
    st.sidebar.markdown("*Simplifying legal document management*")
    st.sidebar.caption(f"Q&A backend: {BACKEND_LABEL}")
    return page

page = render_sidebar()

# ============================================================
# Utilities
# ============================================================
def _human_size_from_bytes(n_bytes: int) -> str:
    if not n_bytes:
        return "—"
    kb = n_bytes / 1024
    return f"{kb/1024:.1f} MB" if kb > 1024 else f"{kb:.1f} KB"

# ============================================================
# Tiny TF-IDF QA (pure Python) + Index helpers
# ============================================================
_WORD = re.compile(r"[A-Za-z0-9_']+")

def _tok(text: str):
    return _WORD.findall(text.lower())

class TinyTfidfQARetriever:
    """Lightweight TF-IDF retriever over chunks (no NumPy)."""
    def __init__(self, chunks):
        self.chunks = chunks  # list of dicts
        self.N = len(chunks)

        # Doc frequency
        df = Counter()
        docs_terms = []
        for c in chunks:
            terms = set(_tok(c["text"]))
            docs_terms.append(terms)
            for t in terms:
                df[t] += 1

        # IDF with smoothing
        self.idf = {t: math.log((self.N + 1) / (df_t + 1)) + 1.0 for t, df_t in df.items()}

        # L2-normalized vectors
        self.doc_vecs = []
        for c in chunks:
            tf = Counter(_tok(c["text"]))
            vec = {}
            for t, n in tf.items():
                if t in self.idf:
                    vec[t] = (1.0 + math.log(n)) * self.idf[t]
            norm = math.sqrt(sum(w * w for w in vec.values())) or 1.0
            for t in list(vec.keys()):
                vec[t] /= norm
            self.doc_vecs.append(vec)

    @staticmethod
    def _cosine(v1: dict, v2: dict) -> float:
        if len(v1) > len(v2):
            v1, v2 = v2, v1
        return sum(w * v2.get(t, 0.0) for t, w in v1.items())

    @staticmethod
    def _compose_prompt(question: str, contexts: list) -> str:
        header = (
            "You are a legal assistant. Answer ONLY using the provided context. "
            "No disclaimers. If the answer is not present, reply exactly: Not specified.\n\nContext:\n"
        )
        ctx = "\n\n---\n\n".join(contexts)
        return f"{header}{ctx}\n\nQuestion: {question}\nAnswer:"

    def ask(self, question: str, k: int = 3, max_new_tokens: int = 220):
        # Query vector
        q_tf = Counter(_tok(question))
        q_vec = {}
        for t, n in q_tf.items():
            if t in self.idf:
                q_vec[t] = (1.0 + math.log(n)) * self.idf[t]
        q_norm = math.sqrt(sum(w * w for w in q_vec.values())) or 1.0
        for t in list(q_vec.keys()):
            q_vec[t] /= q_norm

        # Rank
        scores = [(i, self._cosine(q_vec, self.doc_vecs[i])) for i in range(self.N)]
        scores.sort(key=lambda x: -x[1])
        k = max(1, min(k, self.N))
        top = scores[:k]

        # If comparing two docs, force one chunk per doc
        m = re.search(r'compare\s+(.+?)\s+and\s+(.+?)(\?|$)', question, flags=re.I)
        if m:
            want = {m.group(1).strip().strip('"\''), m.group(2).strip().strip('"\'')}
            forced = []
            seen_docs = set(c["doc_name"] for (i, _) in top for c in [self.chunks[i]])
            for name in list(want):
                if name not in seen_docs:
                    for idx, ch in enumerate(self.chunks):
                        if name.lower() in ch["doc_name"].lower():
                            forced.append((idx, 1.0))  # boost
                            seen_docs.add(name)
                            break
            if forced:
                merged = forced + top
                seen = set(); dedup = []
                for pair in merged:
                    if pair[0] in seen: 
                        continue
                    seen.add(pair[0]); dedup.append(pair)
                    if len(dedup) >= max(6, k): 
                        break
                top = dedup

        sources, contexts = [], []
        for rank, (i, s) in enumerate(top, start=1):
            c = self.chunks[i]
            sources.append(
                {
                    "rank": rank,
                    "doc_name": c["doc_name"],
                    "client": c["client"],
                    "chunk_id": c["chunk_id"],
                    "score": float(s),
                    "preview": c["preview"],
                }
            )
            contexts.append(c["text"])
        try:
            answer = answer_from_context(question, contexts, max_tokens=max_new_tokens)
        except Exception:
            # Last-resort fallback
            from summarizer2 import summarize_text
            prompt = self._compose_prompt(question, contexts)
            answer = summarize_text(prompt, max_len=max_new_tokens)

        return answer, sources

# Orchestration helpers
import difflib

def _norm(s: str) -> str:
    return re.sub(r"[\W_]+", " ", (s or "")).strip().lower()

def _fuzzy_pick(names_like, choices, topn=3, min_ratio=0.55):
    scores = []
    nl = _norm(names_like)
    for c in choices:
        cc = _norm(c)
        ratio = difflib.SequenceMatcher(None, nl, cc).ratio()
        if nl in cc or cc in nl:
            ratio = max(ratio, 0.99)
        scores.append((ratio, c))
    scores.sort(reverse=True)
    return [c for r, c in scores[:topn] if r >= min_ratio]

_DOC_FILE_RE = re.compile(r"\b([A-Za-z0-9_\- ]+\.(?:pdf|docx|txt|md))\b", re.I)

def _find_doc_mentions(question: str, all_doc_names: list[str]) -> list[str]:
    q = question.strip()
    mentioned = [m.group(1) for m in _DOC_FILE_RE.finditer(q)]
    # also catch 'in <name>' / 'between <A> and <B>'
    m_bw = re.search(r"between\s+(.+?)\s+and\s+(.+)", q, re.I)
    if m_bw:
        mentioned += [m_bw.group(1).strip(), m_bw.group(2).strip()]
    m_in = re.search(r"\bin\s+([A-Za-z0-9_\- ]+)", q, re.I)
    if m_in:
        mentioned.append(m_in.group(1).strip())
    # fuzzy-resolve to actual doc names
    resolved = []
    for cand in mentioned:
        picks = _fuzzy_pick(cand, all_doc_names, topn=1)
        if picks and picks[0] not in resolved:
            resolved.append(picks[0])
    return resolved

def _find_client_mentions(question: str, all_client_names: list[str]) -> list[str]:
    q = question.strip()

    # normalize possessives like "John's case" -> "John"
    def _clean(name: str) -> str:
        name = re.sub(r"'s\b", "", name)
        name = re.sub(r"\b(case|matter|file|documents?)\b", "", name, flags=re.I)
        return name.strip()

    # explicit “compare X and Y / with / vs”
    m = re.search(r"compare\s+(.+?)\s+(?:and|with|vs\.?|versus)\s+(.+?)(?:[?.!,]|$)", q, flags=re.I)
    cand = []
    if m:
        cand += [_clean(m.group(1)), _clean(m.group(2))]

    # fall back: grab any capitalized spans after “related to / for / of”
    for pat in [r"related to\s+(.+?)(?:[?.!,]|$)", r"\bfor\s+(.+?)(?:[?.!,]|$)", r"\bof\s+(.+?)(?:[?.!,]|$)"]:
        mm = re.findall(pat, q, flags=re.I)
        for g in mm:
            cand.append(_clean(g))

    # fuzzy resolve to known client names
    resolved = []
    for c in cand:
        picks = _fuzzy_pick(c, all_client_names, topn=1)
        if picks and picks[0] not in resolved:
            resolved.append(picks[0])

    # if still fewer than 2, try scanning all names and pick those mentioned
    if len(resolved) < 2:
        for name in all_client_names:
            if _norm(name) in _norm(q) and name not in resolved:
                resolved.append(name)

    return resolved[:2]
def _client_facts_text(client_name: str) -> str:
    """
    Deterministic per-client snapshot used as grounding for comparisons.
    Reads from st.session_state.documents and summarizes counts, types,
    statuses, date range, and doc names.
    """
    docs = [d for d in (st.session_state.get("documents", []) or [])
            if d.get("client") == client_name]
    if not docs:
        return f"FACTS for {client_name}: No documents found."

    by_type, by_status = {}, {}
    dates, names = [], []
    for d in docs:
        by_type[d.get("type", "Unknown")] = by_type.get(d.get("type", "Unknown"), 0) + 1
        by_status[d.get("status", "Unknown")] = by_status.get(d.get("status", "Unknown"), 0) + 1
        names.append(d.get("name", ""))
        try:
            dates.append(datetime.strptime(d.get("date_uploaded", "1970-01-01"), "%Y-%m-%d"))
        except Exception:
            pass

    lines = [f"FACTS for {client_name}",
             f"TOTAL_DOCS={len(docs)}"]
    if dates:
        lines.append(f"EARLIEST_DATE={min(dates).date().isoformat()}")
        lines.append(f"LATEST_DATE={max(dates).date().isoformat()}")
    lines.append("BY_TYPE: " + ", ".join(f"{k}={v}" for k, v in sorted(by_type.items())))
    lines.append("BY_STATUS: " + ", ".join(f"{k}={v}" for k, v in sorted(by_status.items())))
    lines.append("DOC_NAMES: " + ", ".join(names[:20]) + ("…" if len(names) > 20 else ""))
    return "\n".join(lines)

def _rank_masked(engine, question: str, mask_fn, topk: int = 4, include_internal: bool = False, min_score: float = 0.10):
    # Reuse engine TF-IDF
    q_tf = Counter(_tok(question))
    q_vec = {}
    for t, n in q_tf.items():
        if t in engine.idf:
            q_vec[t] = (1.0 + math.log(n)) * engine.idf[t]
    q_norm = math.sqrt(sum(w*w for w in q_vec.values())) or 1.0
    for t in list(q_vec.keys()):
        q_vec[t] /= q_norm

    scored = []
    for i in range(engine.N):
        ch = engine.chunks[i]
        if (not include_internal) and str(ch.get("doc_name","")).lstrip().startswith("("):
            continue  # drop internal “APP FACTS”, “client registry”, etc.
        if not mask_fn(ch):
            continue
        s = TinyTfidfQARetriever._cosine(q_vec, engine.doc_vecs[i])
        if s >= min_score:
            scored.append((s, i))

    scored.sort(key=lambda x: -x[0])
    return [(i, s) for s, i in scored[:max(1, topk)]]


def _sources_from_indices(engine, ranked):
    out, ctxs = [], []
    for rank, (i, s) in enumerate(ranked, start=1):
        ch = engine.chunks[i]
        out.append({
            "rank": rank,
            "doc_name": ch["doc_name"],
            "client": ch.get("client", "—"),
            "chunk_id": ch["chunk_id"],
            "score": float(s),
            "preview": ch["preview"],
        })
        ctxs.append(ch["text"])
    return out, ctxs

def qa_general_any(q: str, k: int, max_tokens: int):
    # Default: search everything
    return st.session_state.qa_engine.ask(q, k=k, max_new_tokens=max_tokens)

def qa_single_doc(q: str, doc_name: str, k: int, max_tokens: int):
    eng = st.session_state.qa_engine
    ranked = _rank_masked(eng, q, mask_fn=lambda ch: ch["doc_name"] == doc_name, topk=max(2, k))
    sources, ctxs = _sources_from_indices(eng, ranked)
    # Extractive-first prompt
    ans = answer_from_context(q, ctxs, max_tokens=max_tokens)
    return ans, sources

def qa_compare_docs(q: str, docs: list[str], k: int, max_tokens: int):
    eng = st.session_state.qa_engine
    # Take top chunks per doc so both sides show up
    per_doc = []
    for d in docs[:3]:  # up to 3 docs
        ranked = _rank_masked(eng, q, mask_fn=lambda ch, d=d: ch["doc_name"] == d, topk=max(2, k))
        per_doc.append((d, ranked))

    # Label contexts A1,A2 / B1,B2 ...
    label_map = {}
    ctxs = []
    sources = []
    labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for j, (d, ranked) in enumerate(per_doc):
        prefix = labels[j]
        for rnk, (i, s) in enumerate(ranked, start=1):
            ch = eng.chunks[i]
            lbl = f"[{prefix}{rnk}]"
            label_map[(d, rnk)] = lbl
            ctxs.append(f"{lbl} {d}\n{ch['text']}")
            sources.append({
                "rank": len(sources)+1,
                "doc_name": d,
                "client": ch.get("client", "—"),
                "chunk_id": ch["chunk_id"],
                "score": float(s),
                "preview": ch["preview"],
                "label": lbl,
            })

    instruct = (
        "Compare the specified documents using ONLY the context labels.\n"
        "Structure your answer as:\n"
        "- Per-document findings\n"
        "- Key similarities / differences\n"
        "Cite evidence with the labels you see (e.g., [A1], [B2]). If something is absent, say: Not specified."
    )
    ans = answer_from_context(f"{instruct}\n\n{q}", ctxs, max_tokens=max_tokens)
    return ans, sources


def _bytes_to_text_via_tmp(name: str, blob: bytes) -> str:
    suffix = Path(name).suffix or ".bin"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(blob)
        tmp_path = tmp.name
    try:
        return extract_text(tmp_path)
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass

def _chunk_text_words(text: str, chunk_words: int = 450, overlap: int = 60):
    """
    Section/sentence-aware chunker to reduce mid-sentence cuts.
    Keeps your existing signature so callers don't change.
    """
    import re

    def split_sections(t: str):
        # naive legal-ish headers (SECTION/ARTICLE/ALL-CAPS lines) as soft boundaries
        blocks = re.split(r'(?im)^\s*(?:section\s+\d+\s*[:.)-]?|article\s+\d+\s*[:.)-]?|[A-Z][A-Z0-9&() ,.\-]{6,})\s*$', t)
        out = [b.strip() for b in blocks if b and b.strip()]
        return out or [t]

    def split_sentences(t: str):
        # simple sentence split: end punctuation + space + capital/open paren
        sents = re.split(r'(?<=[.!?])\s+(?=[A-Z(])', t.strip())
        return [s.strip() for s in sents if s.strip()]

    # 1) break into sections, 2) pack sentences to target size with overlap
    words_target = max(50, chunk_words)
    words_overlap = max(0, min(overlap, words_target - 10))

    for sec in split_sections(text):
        sents = split_sentences(sec) or [sec]
        buf, count = [], 0
        for s in sents:
            w = s.split()
            if count + len(w) > words_target and buf:
                yield " ".join(buf)
                # build overlap from the tail
                tail = " ".join(buf)[-10000:].split()  # avoid huge join
                if words_overlap > 0:
                    buf = [" ".join(tail[-words_overlap:])]
                    count = len(buf[0].split())
                else:
                    buf, count = [], 0
            buf.append(s)
            count += len(w)
        if buf:
            yield " ".join(buf)


def _make_internal_facts_chunk():
    docs = st.session_state.get("documents", [])
    clients = st.session_state.get("clients", [])
    times = st.session_state.get("time_entries", [])

    lines = []
    lines.append("APP FACTS SNAPSHOT")
    lines.append(f"Total clients: {len(clients)}")
    if clients:
        lines.append("Client names: " + ", ".join(c.get("name", "") for c in clients))

    lines.append(f"Total documents: {len(docs)}")
    if docs:
        lines.append("Document names: " + ", ".join(d.get("name", "") for d in docs))

        # by client
        by_client = {}
        for d in docs:
            by_client[d.get("client","Unknown")] = by_client.get(d.get("client","Unknown"), 0) + 1
        lines.append("Documents per client:")
        for client, n in by_client.items():
            lines.append(f"- {client}: {n}")

        # by type
        by_type = {}
        for d in docs:
            by_type[d.get("type","Unknown")] = by_type.get(d.get("type","Unknown"), 0) + 1
        lines.append("Documents by type:")
        for t, n in by_type.items():
            lines.append(f"- {t}: {n}")

    if times:
        total_hours = sum(float(t.get("hours") or 0.0) for t in times)
        lines.append(f"Total time entries: {len(times)}")
        lines.append(f"Total recorded hours: {total_hours:.2f}")
        hours_by_client = {}
        for t in times:
            hours_by_client[t.get("client","Unknown")] = hours_by_client.get(t.get("client","Unknown"), 0.0) + float(t.get("hours") or 0.0)
        lines.append("Hours per client:")
        for client, h in hours_by_client.items():
            lines.append(f"- {client}: {h:.2f}")

    text = "\n".join(lines).strip()
    return {
        "text": text,
        "doc_name": "(internal) app facts",
        "client": "—",
        "chunk_id": 0,
        "preview": text[:350].replace("\n"," "),
    }

def _make_internal_facts_chunk():
    docs = st.session_state.get("documents", []) or []
    clients = st.session_state.get("clients", []) or []
    times = st.session_state.get("time_entries", []) or []

    # Per-client counts
    docs_per_client = {}
    for d in docs:
        c = (d.get("client") or "").strip() or "Unknown"
        docs_per_client[c] = docs_per_client.get(c, 0) + 1

    hours_per_client, revenue_per_client = {}, {}
    total_hours = total_revenue = 0.0
    for t in times:
        c = (t.get("client") or "").strip() or "Unknown"
        h = float(t.get("hours") or 0.0)
        r = float(t.get("amount") or ((t.get("rate") or 0.0) * h))
        hours_per_client[c] = hours_per_client.get(c, 0.0) + h
        revenue_per_client[c] = revenue_per_client.get(c, 0.0) + r
        total_hours += h
        total_revenue += r

    doc_lines = [
        " | ".join([
            f"name={d.get('name','')}",
            f"client={d.get('client','')}",
            f"type={d.get('type','')}",
            f"matter={d.get('matter','')}",
            f"status={d.get('status','')}",
            f"date={d.get('date_uploaded','')}",
        ]) for d in docs
    ]

    client_lines = [
        " | ".join([
            f"name={c.get('name','')}",
            f"type={c.get('type','')}",
            f"active_matters={c.get('active_matters',0)}",
            f"docs={docs_per_client.get(c.get('name',''), 0)}",
            f"hours={hours_per_client.get(c.get('name',''), 0.0):.2f}",
            f"revenue={revenue_per_client.get(c.get('name',''), 0.0):.2f}",
        ]) for c in clients
    ]

    # Include KEY=VALUE + natural lines for small models
    text = [
        "APP FACTS",
        "",
        f"DOCUMENTS_TOTAL={len(docs)}",
        f"CLIENTS_TOTAL={len(clients)}",
        f"TIME_ENTRIES_TOTAL={len(times)}",
        f"TIME_TOTAL_HOURS={total_hours:.2f}",
        f"TIME_TOTAL_REVENUE={total_revenue:.2f}",
        "",
        f"SENTENCE: There are {len(clients)} clients total.",
        f"SENTENCE: There are {len(docs)} documents total.",
        f"SENTENCE: There are {len(times)} time entries total.",
        "",
        "DOCS_PER_CLIENT:",
        *[f"- {k}: {v}" for k, v in sorted(docs_per_client.items())],
        "",
        "CLIENTS:",
        *client_lines,
        "",
        "DOCUMENTS:",
        *doc_lines,
    ]
    body = "\n".join(text).strip()
    return {
        "text": body,
        "doc_name": "(internal) app facts",
        "client": "—",
        "chunk_id": 0,  # set by caller
        "preview": body[:350].replace("\n", " "),
    }


def build_index_from_documents(documents: list) -> TinyTfidfQARetriever:
    chunks, cid = [], 0

    # Real document chunks
    for d in documents or []:
        name = d.get("name", "Untitled")
        client = d.get("client", "Unknown")

        # Prefer full text → summary → minimal metadata
        if isinstance(d.get("content"), (bytes, bytearray)) and d["content"]:
            raw = _bytes_to_text_via_tmp(name, d["content"])
        elif d.get("summary"):
            raw = d["summary"]
        else:
            raw = f"Document: {name}. Client: {client}. Matter: {d.get('matter')}. Type: {d.get('type')}."

        raw = (raw or "").strip()
        if not raw:
            continue

        for piece in _chunk_text_words(raw, 450, 60):
            cid += 1
            preview = piece[:350].replace("\n", " ") + ("..." if len(piece) > 350 else "")
            chunks.append({
                "text": piece,
                "doc_name": name,
                "client": client,
                "chunk_id": cid,
                "preview": preview,
            })

    # INTERNAL: Client Registry
    cl = st.session_state.get("clients", [])
    if cl:
        cid += 1
        lines = [
            f"- {c.get('name')} ({c.get('type')}); active_matters: {c.get('active_matters',0)}"
            for c in cl
        ]
        txt = "CLIENT REGISTRY\n" + "\n".join(lines)
        chunks.append({
            "text": txt,
            "doc_name": "(internal) client registry",
            "client": "—",
            "chunk_id": cid,
            "preview": txt[:350].replace("\n", " "),
        })

    # INTERNAL: Time Entries (recent tail)
    te = st.session_state.get("time_entries", [])
    if te:
        cid += 1
        lines = []
        for t in te[-200:]:
            lines.append(
                f"{t.get('date')} | {t.get('client')} | {t.get('hours')}h @ ${t.get('rate')}/hr — {t.get('description')}"
            )
        txt = "TIME ENTRIES LOG\n" + "\n".join(lines)
        chunks.append({
            "text": txt,
            "doc_name": "(internal) time entries",
            "client": "—",
            "chunk_id": cid,
            "preview": txt[:350].replace("\n", " "),
        })

    # INTERNAL: Machine-readable APP FACTS
    cid += 1
    facts = _make_internal_facts_chunk()
    facts["chunk_id"] = cid
    chunks.append(facts)

    # Always return at least the facts chunk
    return TinyTfidfQARetriever(chunks)



def _doc_digest(docs: list) -> str:
    parts = []
    for d in docs:
        nbytes = len(d.get("content") or b"") if isinstance(d.get("content"), (bytes, bytearray)) else 0
        summ_hash = (d.get("summary") or "")
        parts.append(f"{d.get('id')}|{d.get('name')}|{nbytes}|{summ_hash}")
    return "|".join(parts)

def _state_digest() -> str:
    base = _doc_digest(st.session_state.get("documents", []))
    c = len(st.session_state.get("clients", []))
    t = len(st.session_state.get("time_entries", []))
    return f"{base}|C{c}|T{t}"

def ensure_qa_index():
    digest = _state_digest()
    if st.session_state.qa_engine is None or st.session_state.qa_digest != digest:
        with st.spinner("Building knowledge index from your documents…"):
            engine = build_index_from_documents(st.session_state.documents)
            st.session_state.qa_engine = engine
            st.session_state.qa_digest = digest

def invalidate_qa_index():
    st.session_state.qa_engine = None
    st.session_state.qa_digest = None

# ============================================================
# Structured answers (no LLM)
# ============================================================
def _list_doc_names(docs, cap=12):
    names = [d.get("name", "Untitled") for d in docs]
    return ", ".join(names[:cap]) + ("…" if len(names) > cap else "")

def _infer_intent_with_llm(q: str) -> dict | None:
    """
    Use a tiny local LLM to normalize arbitrary wording into a JSON intent.
    Falls back gracefully if parsing fails.
    """
    from summarizer2 import summarize_text  # local CPU-friendly
    schema = """Parse the QUESTION into JSON ONLY with keys:
{
  "task": "COUNT|LIST|COMPARE|FILTERED_QA|GENERAL",
  "subject": "clients|documents|time_entries|other",
  "filters": {"client": string|null, "doc": string|null},
  "targets": [string, string]  // for COMPARE (client or doc names, as written)
}
Examples:
- "how many clients do i have?" -> {"task":"COUNT","subject":"clients","filters":{}}
- "name all our clients" -> {"task":"LIST","subject":"clients","filters":{}}
- "how many documents for Sarah?" -> {"task":"COUNT","subject":"documents","filters":{"client":"Sarah"}}
- "compare documents related to John's case with TechCorp case" -> {"task":"COMPARE","subject":"documents","targets":["John","TechCorp"]}
- "what is in the employment contract?" -> {"task":"FILTERED_QA","subject":"documents","filters":{}}
Return JSON only, no extra text."""
    prompt = f"{schema}\n\nQUESTION: {q}\nJSON:"
    raw = summarize_text(prompt, max_len=180).strip()
    # be forgiving about extra text
    import json, re
    m = re.search(r"\{.*\}", raw, flags=re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def try_structured_answer(q: str):
    """
    Robust deterministic answers (no generative LLM needed for the final value):
    - COUNT: clients / documents / time entries (any wording)
    - LIST: clients
    - COUNT documents for <client>
    Everything else -> let the router handle.
    """
    docs    = st.session_state.get("documents", []) or []
    clients = st.session_state.get("clients", []) or []
    times   = st.session_state.get("time_entries", []) or []

    # ---- 1) Try LLM intent parser (if summarizer2 is present) ----
    intent = None
    try:
        from summarizer2 import summarize_text
        schema = """Parse the QUESTION into JSON ONLY:
{"task":"COUNT|LIST|OTHER","subject":"clients|documents|time_entries|other","filters":{"client":string|null}}"""
        raw = summarize_text(f"{schema}\nQUESTION: {q}\nJSON:", max_len=160)
        import json, re
        m = re.search(r"\{.*\}", raw, flags=re.S)
        if m:
            intent = json.loads(m.group(0))
    except Exception:
        intent = None

    # ---- 2) Heuristic fallback (wording-agnostic) ----
    import re
    q_low = " " + re.sub(r"[^a-z0-9 ]+", " ", (q or "").lower()) + " "

    def _is_count():
        return any(k in q_low for k in (" how many ", " number of ", " count of ", " total ", " totals "))
    def _has_clients():   return " client " in q_low or " clients " in q_low
    def _has_docs():      return any(k in q_low for k in (" document ", " documents ", " file ", " files "))
    def _has_time():      return " time " in q_low and any(k in q_low for k in (" entry ", " entries ", " timesheet ", " timesheets "))

    # If LLM classified a simple COUNT/LIST, honor it; otherwise rely on heuristics.
    task    = (intent or {}).get("task", "").upper()
    subject = (intent or {}).get("subject", "").lower()
    filters = (intent or {}).get("filters", {}) or {}
    client_filter = (filters.get("client") or "").strip()

    # ---------- COUNT: Clients ----------
    if (task == "COUNT" and subject == "clients") or (_is_count() and _has_clients()):
        src = [{
            "rank": 1, "doc_name": "(internal) client registry",
            "client": "—", "chunk_id": 0, "score": 1.0,
            "preview": ", ".join(c.get("name","") for c in clients[:12])
        }]
        return True, str(len(clients)), src

    # ---------- COUNT: Documents (optionally for a client) ----------
    if (task == "COUNT" and subject == "documents") or (_is_count() and _has_docs()):
        # try to catch "for <client>" from raw question
        m = re.search(r"(?:for|from|by)\s+([A-Za-z][A-Za-z0-9 .'\-]+)$", q.strip(), flags=re.I)
        target = client_filter or (m.group(1).strip() if m else "")
        if target:
            # fuzzy-resolve to known client name
            picks = _fuzzy_pick(target, [c["name"] for c in clients], topn=1)
            resolved = picks[0] if picks else target
            subset = [d for d in docs if d.get("client","") == resolved]
            src = [{
                "rank": 1, "doc_name": f"(internal) documents for {resolved}",
                "client": resolved, "chunk_id": 0, "score": 1.0,
                "preview": ", ".join(d.get("name","") for d in subset[:12])
            }]
            return True, str(len(subset)), src
        src = [{
            "rank": 1, "doc_name": "(internal) document registry",
            "client": "—", "chunk_id": 0, "score": 1.0,
            "preview": ", ".join(d.get("name","") for d in docs[:12])
        }]
        return True, str(len(docs)), src

    # ---------- COUNT: Time entries ----------
    if (task == "COUNT" and subject == "time_entries") or (_is_count() and _has_time()):
        src = [{"rank": 1, "doc_name": "(internal) time entries", "client": "—",
                "chunk_id": 0, "score": 1.0, "preview": str(len(times))}]
        return True, str(len(times)), src

    # ---------- LIST clients ----------
    if (task == "LIST" and subject == "clients") or any(k in q_low for k in (" list clients", " show clients", " clients list ")):
        if not clients:
            return True, "No clients found.", []
        bullets = "\n".join(
            f"• {c.get('name')} — {c.get('type')}, matters: {c.get('active_matters',0)}"
            for c in clients
        )
        src = [{
            "rank": 1, "doc_name": "(internal) client registry",
            "client": "—", "chunk_id": 0, "score": 1.0,
            "preview": ", ".join(c.get("name","") for c in clients[:12])
        }]
        return True, f"Clients:\n{bullets}", src

    # Nothing deterministic → let the router do retrieval/LLM
    return False, "", []



def answer_question_hybrid(q: str, k: int, max_new_tokens: int):
    # 1) Try deterministic answers first (counts, lists, totals)
    handled, ans, srcs = try_structured_answer(q)
    if handled:
        return ans, srcs

    # 2) Resolve mentions
    doc_names = [d["name"] for d in st.session_state.get("documents", [])]
    client_names = [c["name"] for c in st.session_state.get("clients", [])]

    mentioned_docs = _find_doc_mentions(q, doc_names)
    mentioned_clients = _find_client_mentions(q, client_names)

    # 3) Route
    if len(mentioned_clients) >= 2 and re.search(r"\bcompare\b|\bvs\b|\bversus\b", q, flags=re.I):
        return qa_compare_clients(q, mentioned_clients[:2], k=max(2, k), max_tokens=max_new_tokens)

    if len(mentioned_docs) >= 2:
        return qa_compare_docs(q, mentioned_docs, k, max_new_tokens)
    elif len(mentioned_docs) == 1:
        return qa_single_doc(q, mentioned_docs[0], k, max_new_tokens)

    # If only one client mentioned, treat as a filtered query for that client's docs
    if len(mentioned_clients) == 1:
        eng = st.session_state.qa_engine
        ranked = _rank_masked(
            eng, q,
            mask_fn=lambda ch: str(ch.get("client","")) == mentioned_clients[0],
            topk=max(2, k),
            include_internal=False
        )
        sources, ctxs = _sources_from_indices(eng, ranked)
        if not sources:
            return "Not specified", []
        ans = answer_from_context(q, ctxs, max_tokens=max_new_tokens)
        return ans, sources

    # 4) General fallback: search everything but exclude internal chunks to cut noise
    eng = st.session_state.qa_engine
    ranked = _rank_masked(eng, q, mask_fn=lambda ch: True, topk=k, include_internal=False)
    sources, ctxs = _sources_from_indices(eng, ranked)
    if not sources:
        return "Not specified", []
    ans = answer_from_context(q, ctxs, max_tokens=max_new_tokens)
    return ans, sources

# ============================================================
# Routes
# ============================================================
if page == "Dashboard":
    st.title("📊 Dashboard Overview")
    show_usage_info()
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Documents", len(st.session_state.documents), "5 this week")
    with c2:
        st.metric("Active Clients", len(st.session_state.clients), "1 new")
    with c3:
        st.metric("Pending Reviews", 2, "-1")
    with c4:
        st.metric("Hours This Week", 42.5, "8.5")

    st.divider()
    a, b = st.columns(2)
    with a:
        st.subheader("📋 Recent Documents")
        recent = sorted(st.session_state.documents, key=lambda x: x["date_uploaded"], reverse=True)[:5]
        for doc in recent:
            st.markdown(f"**{doc['name']}**")
            st.caption(f"{doc['client']} • {doc['date_uploaded']}")
            if doc.get("summary"):
                st.caption(f"Summary: {doc['summary'][:150]}…")
            st.markdown("---")
    with b:
        st.subheader("⏰ Today's Schedule")
        st.markdown("**9:00 AM** - Client consultation (Smith)")
        st.markdown("**11:30 AM** - Document review (TechCorp)")
        st.markdown("**2:00 PM** - Court filing deadline")
        st.markdown("**4:00 PM** - Settlement negotiation call")

elif page == "Document Management":
    st.title("📁 Document Management")

    c1, c2, c3 = st.columns(3)
    with c1:
        search_term = st.text_input("🔍 Search documents", placeholder="Enter keywords…", key="doc_search")
    with c2:
        client_filter = st.selectbox(
            "Filter by Client", ["All"] + [c["name"] for c in st.session_state.clients], key="doc_client_filter"
        )
    with c3:
        doc_type_filter = st.selectbox(
            "Filter by Type",
            ["All", "Settlement Agreement", "Articles of Incorporation", "Court Motion",
             "Contract", "Partnership Agreement", "Lease Agreement", "Court Filing",
             "Employment Contract", "Court Complaint", "General Document"],
            key="doc_type_filter",
        )

    st.subheader("📤 Upload New Document")
    user_email = st.session_state["user"]["email"]
    can_upload, limit_message = check_usage_limits(user_email, "document")

    if not can_upload:
        st.error(limit_message)
        st.info("Please upgrade your plan to upload more documents.")
    else:
        u1, u2, u3 = st.columns(3)
        with u1:
            uploaded_file = st.file_uploader("Choose file", type=["pdf", "docx", "txt", "md"], key="uploader")
        with u2:
            upload_client = st.selectbox("Select Client", [c["name"] for c in st.session_state.clients], key="upload_client")
        with u3:
            upload_matter = st.text_input("Matter Description", key="upload_matter")

        if uploaded_file and upload_client and upload_matter:
            if st.button("Upload Document", key="btn_upload_doc"):
                # Read raw bytes
                file_bytes = uploaded_file.read()
                size_str = _human_size_from_bytes(len(file_bytes))

                # Extract text for summary
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
                    tmp.write(file_bytes)
                    tmp_path = tmp.name
                try:
                    with st.spinner("Extracting text…"):
                        text_content = extract_text(tmp_path)
                finally:
                    try:
                        os.unlink(tmp_path)
                    except Exception:
                        pass

                # Guess type from filename
                fn = uploaded_file.name.lower()
                doc_type = "General Document"
                if "contract" in fn or "agreement" in fn:
                    doc_type = "Contract"
                elif "motion" in fn or "complaint" in fn:
                    doc_type = "Court Motion"
                elif "llc" in fn or "incorporation" in fn:
                    doc_type = "Articles of Incorporation"
                elif "lease" in fn:
                    doc_type = "Lease Agreement"
                elif "employment" in fn:
                    doc_type = "Employment Contract"

                # Summarize if we got text
                if isinstance(text_content, str) and text_content.strip() and not text_content.startswith("Error:"):
                    with st.spinner("Summarizing…"):
                        summary = summarize_text(text_content, max_len=220)
                else:
                    summary = "No text extracted or extraction error."

                new_doc = {
                    "id": len(st.session_state.documents) + 1,
                    "name": uploaded_file.name,
                    "client": upload_client,
                    "matter": upload_matter,
                    "type": doc_type,
                    "date_uploaded": datetime.now().strftime("%Y-%m-%d"),
                    "file_size": size_str,
                    "status": "New",
                    "content": file_bytes,
                    "summary": summary,
                }
                st.session_state.documents.append(new_doc)
                increment_usage(user_email, "document")
                invalidate_qa_index()
                st.success(f"Document '{uploaded_file.name}' uploaded successfully!")
                st.rerun()

    st.divider()
    st.subheader("📋 Document Library")

    filtered = st.session_state.documents
    if search_term:
        q = search_term.lower()
        filtered = [d for d in filtered if q in d["name"].lower()
                    or q in d["client"].lower()
                    or q in (d.get("matter") or "").lower()]
    if client_filter != "All":
        filtered = [d for d in filtered if d["client"] == client_filter]
    if doc_type_filter != "All":
        filtered = [d for d in filtered if d["type"] == doc_type_filter]

    for doc in filtered:
        with st.expander(f"{doc['name']} — {doc['client']}"):
            a, b = st.columns(2)
            with a:
                st.markdown(f"**Client:** {doc['client']}")
                st.markdown(f"**Matter:** {doc['matter']}")
                st.markdown(f"**Type:** {doc['type']}")
            with b:
                st.markdown(f"**Date:** {doc['date_uploaded']}")
                st.markdown(f"**Size:** {doc['file_size']}")
                st.markdown(f"**Status:** {doc['status']}")

            if doc.get("summary"):
                st.markdown(f"**Summary:** {doc['summary']}")

            b1, b2, b3, b4 = st.columns(4)
            with b1:
                st.button("📖 View", key=f"view_{doc['id']}")
            with b2:
                st.button("📝 Edit", key=f"edit_{doc['id']}")
            with b3:
                if st.button("📥 Download", key=f"download_{doc['id']}"):
                    if doc.get("content"):
                        mime = "application/pdf" if doc["name"].lower().endswith(".pdf") else "application/octet-stream"
                        st.download_button(
                            "Click to Download",
                            data=doc["content"],
                            file_name=doc["name"],
                            mime=mime,
                            key=f"dl_{doc['id']}",
                        )
                    else:
                        st.info("Demo document - no file to download.")
            with b4:
                if st.button("🗑️ Delete", key=f"delete_{doc['id']}"):
                    st.session_state.documents = [d for d in st.session_state.documents if d["id"] != doc["id"]]
                    invalidate_qa_index()
                    st.success(f"Document '{doc['name']}' deleted!")
                    st.rerun()

elif page == "Client Management":
    st.title("👥 Client Management")

    user_email = st.session_state["user"]["email"]
    can_add_client, msg = check_usage_limits(user_email, "client")

    st.subheader("➕ Add New Client")
    if not can_add_client:
        st.error(msg)
        st.info("Please upgrade your plan to add more clients.")
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            new_client_name = st.text_input("Client Name", key="new_client_name")
        with c2:
            new_client_type = st.selectbox("Client Type", ["Individual", "Business"], key="new_client_type")
        with c3:
            st.write("")
            if st.button("Add Client", key="btn_add_client") and new_client_name:
                st.session_state.clients.append(
                    {"name": new_client_name, "type": new_client_type, "active_matters": 0}
                )
                increment_usage(user_email, "client")
                invalidate_qa_index()
                st.success(f"Client '{new_client_name}' added successfully!")
                st.rerun()

    st.divider()
    st.subheader("📋 Client List")
    st.dataframe(pd.DataFrame(st.session_state.clients), use_container_width=True)

    if st.session_state.clients:
        sel = st.selectbox("Select client for details", [c["name"] for c in st.session_state.clients], key="client_details_sel")
        if sel:
            client_docs = [d for d in st.session_state.documents if d["client"] == sel]
            st.subheader(f"Documents for {sel}")
            if client_docs:
                for d in client_docs:
                    st.markdown(f"• **{d['name']}** ({d['type']}) — {d['status']}")
            else:
                st.info("No documents found for this client.")

elif page == "Time Tracking":
    st.title("⏱️ Time Tracking")
    user_email = st.session_state["user"]["email"]
    info = get_user_info(user_email)
    if info and not info.get("usage_limits", {}).get("has_time_tracking", False):
        st.error("Time tracking is not available in your current plan.")
        st.info("Please upgrade to access time tracking features.")
        st.stop()

    st.subheader("🟢 Active Timer")
    c1, c2, c3 = st.columns(3)
    with c1:
        timer_client = st.selectbox("Client", [c["name"] for c in st.session_state.clients], key="timer_client")
    with c2:
        timer_matter = st.text_input("Matter/Task", key="timer_matter")
    with c3:
        timer_rate = st.number_input("Hourly Rate ($)", min_value=0.0, value=250.0, step=25.0, key="timer_rate")
    a1, a2 = st.columns(2)
    with a1:
        if st.button("▶️ Start Timer", key="btn_timer_start"):
            st.success("Timer started!")
    with a2:
        if st.button("⏹️ Stop Timer", key="btn_timer_stop"):
            st.info("Timer stopped. 1.5 hours recorded.")

    st.divider()
    st.subheader("📝 Manual Time Entry")
    m1, m2 = st.columns(2)
    with m1:
        entry_date = st.date_input("Date", key="tt_date")
        entry_client = st.selectbox("Client ", [c["name"] for c in st.session_state.clients], key="tt_client")
        entry_hours = st.number_input("Hours", min_value=0.0, max_value=24.0, value=1.0, step=0.25, key="tt_hours")
    with m2:
        entry_description = st.text_area("Description", key="tt_desc")
        entry_rate = st.number_input("Rate ($)", min_value=0.0, value=250.0, step=25.0, key="tt_rate")
    if st.button("Add Time Entry", key="btn_add_time"):
        if entry_client and entry_description:
            st.session_state.time_entries.append(
                {
                    "date": entry_date,
                    "client": entry_client,
                    "hours": entry_hours,
                    "description": entry_description,
                    "rate": entry_rate,
                    "amount": entry_hours * entry_rate,
                }
            )
            invalidate_qa_index()
            st.success("Time entry added successfully!")
            st.rerun()

    st.divider()
    st.subheader("📋 Recent Time Entries")
    if st.session_state.time_entries:
        st.dataframe(pd.DataFrame(st.session_state.time_entries), use_container_width=True)
    else:
        st.info("No time entries yet.")

elif page == "Reports":
    st.title("📊 Reports & Analytics")
    user_email = st.session_state["user"]["email"]
    info = get_user_info(user_email)
    has_adv = info and info.get("usage_limits", {}).get("has_advanced_reports", False)
    if not has_adv:
        st.warning("⚠️ Advanced reports are available in Pro plans only. Showing basic reports.")

    c1, c2 = st.columns(2)
    with c1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30), key="rep_start")
    with c2:
        end_date = st.date_input("End Date", value=datetime.now(), key="rep_end")

    st.divider()
    st.subheader("📁 Document Statistics")
    g1, g2 = st.columns(2)
    with g1:
        counts = {}
        for d in st.session_state.documents:
            counts[d["type"]] = counts.get(d["type"], 0) + 1
        st.bar_chart(counts)
    with g2:
        per_client = {}
        for d in st.session_state.documents:
            per_client[d["client"]] = per_client.get(d["client"], 0) + 1
        st.bar_chart(per_client)

    if has_adv:
        st.divider()
        st.subheader("📈 Advanced Analytics")
        st.info("Advanced analytics features would appear here for Pro users.")

    st.divider()
    st.subheader("⏱️ Time Tracking Summary")
    if st.session_state.time_entries:
        total_hours = sum(e["hours"] for e in st.session_state.time_entries)
        total_revenue = sum(e["amount"] for e in st.session_state.time_entries)
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Total Hours", f"{total_hours:.1f}")
        with m2:
            st.metric("Total Revenue", f"${total_revenue:,.2f}")
        with m3:
            st.metric("Average Rate", f"${(total_revenue/total_hours):.2f}/hr" if total_hours > 0 else "$0/hr")
    else:
        st.info("No time entries to analyze yet.")

elif page == "Questions":
    st.title("🧠 Ask Questions About Your Cases")

    # Build index if needed
    try:
        ensure_qa_index()
    except Exception as e:
        st.error(f"Could not build index from your current documents: {e}")
        st.info("Tip: Upload at least one document with extractable text or an existing summary.")
        st.stop()

    with st.expander("Index info", expanded=False):
        st.write(f"Chunks indexed: {len(st.session_state.qa_engine.chunks)}")

    # Single-render form (avoid duplicate runs)
    with st.form("qa_form"):
        q = st.text_area(
            "Your question",
            placeholder="e.g., How many documents do I have? Name them.",
            key="qa_question",
        )
        c1, c2 = st.columns(2)
        with c1:
            top_k = st.slider("Top sources (k)", 1, 6, 3, key="qa_top_k")
        with c2:
            max_tokens = st.slider("Max answer tokens", 120, 300, 220, key="qa_max_tokens")
        submitted = st.form_submit_button("🧾 Ask")

    # Rebuild button lives outside the form
    if st.button("🔄 Rebuild Index", key="btn_rebuild_index"):
        invalidate_qa_index()
        ensure_qa_index()
        st.success("Index rebuilt.")

    if submitted and q.strip():
        with st.spinner("Thinking…"):
            answer, sources = answer_question_hybrid(q.strip(), k=top_k, max_new_tokens=max_tokens)
        st.session_state.qa_output = {"answer": answer, "sources": sources}

    if st.session_state.qa_output:
        out = st.session_state.qa_output
        st.subheader("Answer")
        st.write(out["answer"])
        st.subheader("Sources")
        for i, src in enumerate(out["sources"], start=1):
            score = src.get("score", 1.0)
            cid = src.get("chunk_id", 0)
            with st.expander(f"[{i}] {src['doc_name']} (chunk {cid}) • score {score:.3f}"):
                st.write(src["preview"])
