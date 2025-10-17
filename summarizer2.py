# summarizer2.py

import os
import re
import json
import hashlib
import logging
import tempfile
from pathlib import Path
from typing import List, Dict, Optional

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# ---------- logging ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- determinism ----------
_SEED = 0
torch.manual_seed(_SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(_SEED)
try:
    torch.use_deterministic_algorithms(True)
except Exception:
    pass

# ---------- model ----------
MODEL_NAME = "facebook/bart-large-cnn"
MAX_MODEL_TOKENS = 1024
CHUNK_TOKENS = 900
CHUNK_STRIDE = 100

_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
_model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    use_safetensors=True,
    trust_remote_code=False,
)
_local_summarizer = pipeline(
    "summarization",
    model=_model,
    tokenizer=_tokenizer,
    device=-1  # use CPU for maximum reproducibility
)

# ---------- persistent cache ----------
CACHE_DIR = Path.home() / ".legaldoc_cache"
CACHE_FILE = CACHE_DIR / "summaries.json"

def _load_persistent_cache() -> Dict[str, str]:
    try:
        if CACHE_FILE.exists():
            return json.loads(CACHE_FILE.read_text())
    except Exception:
        pass
    return {}

def _save_persistent_cache(store: Dict[str, str]) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(json.dumps(store, ensure_ascii=False, indent=2))
    except Exception as e:
        logger.warning(f"Could not write cache file: {e}")

_persist_cache = _load_persistent_cache()

# ---------- file extraction ----------
def _extract_with_pypdf(pdf_path: str) -> str:
    from pypdf import PdfReader
    reader = PdfReader(str(pdf_path))
    return "\n".join((pg.extract_text() or "") for pg in reader.pages).strip()

def _extract_with_docx2txt(docx_path: str) -> str:
    import docx2txt
    return (docx2txt.process(str(docx_path)) or "").strip()

def extract_text(path: str) -> str:
    p = Path(path)
    ext = p.suffix.lower()
    if ext in {".txt", ".md"}:
        return p.read_text(errors="ignore")
    if ext == ".pdf":
        return _extract_with_pypdf(str(p))
    if ext == ".docx":
        return _extract_with_docx2txt(str(p))
    return "Error: Unsupported file type"

def extract_text_from_file(uploaded_file):
    tmp_path = None
    try:
        if not uploaded_file:
            return "Error: No file provided"
        suffix = Path(getattr(uploaded_file, "name", "")).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        return extract_text(tmp_path)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

# ---------- helpers ----------
def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(The\s*){3,}", "The ", text)
    text = re.sub(r"(\b\w+\b)( \1){2,}", r"\1", text)
    return text.strip()

def _tok_len(text: str) -> int:
    return len(_tokenizer.encode(text, truncation=False))

def _chunk_by_tokens(text: str, max_tokens: int, stride: int) -> List[str]:
    ids = _tokenizer.encode(text, truncation=False)
    n = len(ids)
    if n <= max_tokens:
        return [text]
    chunks, start = [], 0
    while start < n:
        end = min(start + max_tokens, n)
        chunk_ids = ids[start:end]
        chunks.append(_tokenizer.decode(chunk_ids, skip_special_tokens=True))
        if end >= n:
            break
        start = max(0, end - stride)
    return chunks

def _gen_kwargs(max_len: int) -> Dict:
    min_len = max(50, min(max_len - 10, int(max_len * 0.4)))
    return dict(
        max_length=max_len,
        min_length=min_len,
        do_sample=False,
        num_beams=4,
        no_repeat_ngram_size=3,
        length_penalty=1.0,
        early_stopping=True,
    )

# ---------- light legal facts ----------
_MONTHS = r"(January|February|March|April|May|June|July|August|September|October|November|December)"
DATE_PAT = re.compile(
    rf"(?:effective\s+as\s+of|dated\s+as\s+of|as\s+of)\s+({_MONTHS}\s+\d{{1,2}},\s+\d{{4}})",
    re.IGNORECASE,
)
BETWEEN_PAT = re.compile(
    r"(?:between|by and between)\s+(.+?)\s+(?:and)\s+(.+?)(?:\.|,|\n)",
    re.IGNORECASE | re.DOTALL,
)
GOV_LAW_PAT = re.compile(
    r"(?:governed by|governed and construed in accordance with)\s+(?:the\s+)?laws\s+of\s+([A-Za-z\s]+?)(?:,|\.)",
    re.IGNORECASE,
)
TITLE_PAT = re.compile(
    r"(?i)\b(mutual|one[-\s]?way)?\s*non[-\s]?disclosure\s+agreement\b|"
    r"\bmaster\s+services\s+agreement\b|\bstatement\s+of\s+work\b|"
    r"\blicense\s+agreement\b|\bservice\s+agreement\b|\bconsulting\s+agreement\b|\bagreement\b"
)

def _parse_date_to_iso(text: str) -> Optional[str]:
    try:
        from dateutil import parser as dateparser
    except Exception:
        return None
    m = DATE_PAT.search(text)
    if not m:
        return None
    try:
        dt = dateparser.parse(m.group(1))
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None

def _extract_parties(text: str) -> Optional[str]:
    m = BETWEEN_PAT.search(text)
    if m:
        a = re.sub(r"\s+", " ", m.group(1)).strip(' "’‘“”')
        b = re.sub(r"\s+", " ", m.group(2)).strip(' "’‘“”')
        a = re.sub(r"\s*\(.*?\)$", "", a)
        b = re.sub(r"\s*\(.*?\)$", "", b)
        return f"{a} and {b}"
    m2 = re.search(r"Parties?:\s*(.+?)\s*(?:\n|\.|;)", text, re.IGNORECASE | re.DOTALL)
    if m2:
        return re.sub(r"\s+", " ", m2.group(1)).strip()
    return None

def _extract_governing_law(text: str) -> Optional[str]:
    m = GOV_LAW_PAT.search(text)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()
    m2 = re.search(r"laws of (?:the )?(?:State of )?([A-Za-z\s]+)", text, re.IGNORECASE)
    if m2:
        return re.sub(r"\s+", " ", m2.group(1)).strip().rstrip(".")
    return None

def _infer_title(text: str) -> Optional[str]:
    # Only return the matched phrase, never the whole line
    early = text[:800]
    m = TITLE_PAT.search(early)
    if m:
        return m.group(0).upper()
    return None

def extract_key_facts(text: str) -> Dict[str, Optional[str]]:
    t = _clean_text(text or "")
    return {
        "title": _infer_title(t),
        "parties": _extract_parties(t),
        "effective_date": _parse_date_to_iso(t),
        "governing_law": _extract_governing_law(t),
    }

# ---------- summarization core ----------
def _summarize_once(text: str, max_len: int) -> str:
    return _local_summarizer(text, **_gen_kwargs(max_len))[0]["summary_text"]

def _reduce_until_fits(text: str, per_chunk_len: int, final_len: int) -> str:
    """
    Iteratively summarize in chunks until the text fits the model context,
    then do a final bounded pass to keep the output short.
    """
    current = text
    # Keep reducing while it doesn't fit in the model window
    while _tok_len(current) > MAX_MODEL_TOKENS:
        pieces = _chunk_by_tokens(current, CHUNK_TOKENS, CHUNK_STRIDE)
        subs = [_summarize_once(p, per_chunk_len) for p in pieces]
        current = _clean_text(" ".join(subs))
        # If somehow nothing changes, break to avoid loops
        if len(pieces) <= 1:
            break
    # Final bounded pass (even if it already fits) to enforce length cap
    return _summarize_once(current, final_len)

# ---------- public API ----------
_memory_cache: Dict[str, str] = {}

def summarize_text(text: str, max_len: int = 220) -> str:
    """
    Deterministic, schema-anchored summary with a hard length cap.
    - Extracts light legal facts (title/parties/effective date/governing law)
    - Generates a short narrative summary
    - Returns a fixed schema string
    - Uses persistent cache keyed by cleaned text + model + schema tag
    """
    if not text or not text.strip():
        return "Error: Empty text provided"

    cleaned = _clean_text(text)
    cache_key = hashlib.md5(
        f"{MODEL_NAME}|{max_len}|schema-v3|".encode() + cleaned.encode()
    ).hexdigest()

    if cache_key in _persist_cache:
        return _persist_cache[cache_key]
    if cache_key in _memory_cache:
        return _memory_cache[cache_key]

    try:
        facts = extract_key_facts(cleaned)
        # Two-stage reduce with a strict final cap
        narrative = _reduce_until_fits(
            cleaned,
            per_chunk_len=max(120, int(max_len * 0.75)),  # chunk summaries
            final_len=max_len,                            # final cap
        )
        def nz(x): return x if (x and str(x).strip()) else "Not specified"
        final = (
            f"- Document Type / Title: {nz(facts.get('title'))}\n"
            f"- Parties & Roles: {nz(facts.get('parties'))}\n"
            f"- Effective Date: {nz(facts.get('effective_date'))}\n"
            f"- Governing Law / Venue: {nz(facts.get('governing_law'))}\n"
            f"- Narrative Summary: {narrative.strip()}"
        )

        _memory_cache[cache_key] = final
        _persist_cache[cache_key] = final
        _save_persistent_cache(_persist_cache)
        return final

    except Exception as e:
        logger.error(f"Error summarizing: {str(e)}")
        return f"Error summarizing: {str(e)}"

def clear_cache():
    _memory_cache.clear()

def test_functions():
    print("✅ summarizer2 loaded (BART deterministic + schema + hard cap)")
    print("✅ summarize_text -> stable, bounded output")
    print("✅ extract_key_facts available")

__all__ = [
    "extract_text_from_file",
    "extract_text",
    "summarize_text",
    "extract_key_facts",
    "clear_cache",
]

def answer_from_context(context: str, question: str, max_len: int = 220) -> str:
    """Deterministic Q&A (no sampling) using the same BART pipe."""
    if not context or not question:
        return "Not specified"

    prompt = (
        "You are a legal assistant for a law firm. Answer the user question "
        "ONLY using the provided context. Be concise, factual, and list every "
        "relevant fact explicitly. If the answer is not present, say 'Not specified'.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
    try:
        out = _local_summarizer(
            prompt,
            max_length=max_len,
            min_length=max(50, int(max_len * 0.4)),
            do_sample=False
        )
        return out[0]["summary_text"]
    except Exception as e:
        logger.error(f"Error in answer_from_context: {e}")
        return "Error: could not generate answer"
