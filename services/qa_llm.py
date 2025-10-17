# services/qa_llm.py
import re
from typing import List

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WS = re.compile(r"\s+")

def _norm(s: str) -> str:
    return _WS.sub(" ", s or "").strip()

def _keywords(q: str) -> List[str]:
    q = (q or "").lower()
    q = re.sub(r"[^a-z0-9\s]", " ", q)
    toks = [t for t in q.split() if len(t) > 2]
    # quick synonyms for common asks
    syn = {
        "customers": "clients",
        "docs": "documents",
        "files": "documents",
        "cases": "matters",
        "matter": "matters",
    }
    out = []
    for t in toks:
        out.append(syn.get(t, t))
    # de-dup preserving order
    seen = set(); kept=[]
    for t in out:
        if t not in seen:
            kept.append(t); seen.add(t)
    return kept

def _score_sentence(sent: str, kws: List[str]) -> int:
    s = " " + (sent or "").lower() + " "
    sc = 0
    for k in kws:
        if f" {k} " in s:
            sc += 2
        # crude plural/suffix match
        if f" {k}s " in s or f"{k}:" in s:
            sc += 1
    return sc

def answer_from_context_extractive(context: str, question: str, max_len: int = 220) -> str:
    """
    Deterministic, extractive QA:
    - split context into sentences
    - score by keyword overlap
    - return top sentences concatenated (bounded length)
    """
    if not context or not context.strip():
        return "Not specified"
    sents = _SENT_SPLIT.split(_norm(context))
    kws = _keywords(question)
    ranked = sorted(sents, key=lambda s: _score_sentence(s, kws), reverse=True)
    picked = []
    total = 0
    for s in ranked:
        if not s.strip():
            continue
        # require at least some overlap when we have keywords
        if kws and _score_sentence(s, kws) == 0:
            continue
        if total + len(s) > max_len:
            # try to trim last one
            remaining = max_len - total
            if remaining > 40:  # keep something meaningful
                s = s[:remaining].rstrip() + "…"
                picked.append(s)
                total = max_len
            break
        picked.append(s)
        total += len(s)
        if total >= max_len:
            break
    return " ".join(picked).strip() or "Not specified"
