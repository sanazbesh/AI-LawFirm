# services/__init__.py  — side-effect-free re-exports

# RAG pieces (no summarizer in Q&A)
try:
    from .retriever_tf_idf import TinyTfidfQARetriever
except Exception:  # pragma: no cover
    TinyTfidfQARetriever = None  # type: ignore

from .rag_router import ensure_qa_index, answer_question_hybrid

# Auth service (real or stub)
try:
    from .auth import AuthService
except Exception:  # pragma: no cover
    class AuthService:
        def __init__(self, *_, **__): pass
        def is_logged_in(self): return True
        def show_login(self): pass
        def show_user_settings(self): pass
        def render_sidebar(self): pass

__all__ = [
    "TinyTfidfQARetriever",
    "ensure_qa_index",
    "answer_question_llm",
    "AuthService",
]
