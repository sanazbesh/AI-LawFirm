# pages/questions.py
import streamlit as st
from services.rag_router import ensure_qa_index, answer_question_hybrid

st.set_page_config(page_title="Questions", page_icon="🧠", layout="wide")
st.title("🧠 Ask Questions About Your Cases")

# build / rebuild index when needed
docs = st.session_state.get("documents", []) or []
if not any((d.get("content_text") or d.get("content") or d.get("summary") or "").strip() for d in docs):
    st.warning("No indexable document text was found. Upload documents or ensure content_text/content exists in st.session_state['documents'].")

import streamlit as st
from services.rag_router import ensure_qa_index, answer_question_hybrid

st.set_page_config(page_title="Questions", page_icon="🧠", layout="wide")
st.title("🧠 Ask Questions About Your Cases")

# --- Debug / Utilities -------------------------------------------------------
with st.expander("🔧 Debug / seed & index", expanded=False):
    c1, c2, c3 = st.columns(3)

    if c1.button("Seed demo doc"):
        st.session_state.setdefault("documents", [])
        st.session_state["documents"].append({
            "name": "Johnson Corporation – Complaint",
            "client": "Johnson Corporation",
            "matter": "Johnson v. Smith (2024)",
            "type": "complaint",
            "status": "active",
            "content_text": (
                "Johnson Corporation filed a complaint against Smith for breach of "
                "contract regarding the 2024 supply agreement. The complaint seeks "
                "damages and injunctive relief. Case caption: Johnson Corporation v. Smith."
            ),
        })
        # Force a clean rebuild on next run
        st.session_state.pop("qa_engine", None)
        st.session_state.pop("qa_digest", None)
        st.success("Seeded one document.")
        st.rerun()

    if c2.button("Force reindex"):
        st.session_state.pop("qa_engine", None)
        st.session_state.pop("qa_digest", None)
        st.success("Index will rebuild below.")

    if c3.button("Clear docs"):
        st.session_state["documents"] = []
        st.session_state.pop("qa_engine", None)
        st.session_state.pop("qa_digest", None)
        st.success("Cleared documents and index.")
        st.rerun()

docs = st.session_state.get("documents", [])
has_text = any((d.get("content_text") or d.get("content") or d.get("summary")) for d in docs)

if not has_text:
    st.warning("No indexable document text was found. Upload documents or ensure "
               "`content_text` / `content` exists in `st.session_state['documents']`.")
else:
    st.caption(f"📄 Docs: {len(docs)} | "
               f"Textful docs: {sum(1 for d in docs if d.get('content_text') or d.get('content') or d.get('summary'))}")

# Build (or rebuild) the retriever index *after* any seeding/clearing above
ensure_qa_index()

# Show index stats if present
engine = st.session_state.get("qa_engine")
if engine:
    try:
        st.caption(f"🗂️ Index chunks: {len(engine.chunks)}")
    except Exception:
        pass

# --- UI ----------------------------------------------------------------------
with st.form("qa_form"):
    user_q = st.text_area("Your question",
                          placeholder="e.g., Show the Johnson case, list documents for Johnson, count clients, etc.")
    c1, c2 = st.columns(2)
    with c1:
        k_top_k = st.slider("Top sources (k)", 1, 6, 3)
    with c2:
        max_tokens = st.slider("Max answer tokens", 120, 300, 220)
    submitted = st.form_submit_button("🧾 Ask")

if submitted and user_q.strip():
    with st.spinner("Thinking…"):
        answer, sources = answer_question_hybrid(user_q, k=k_top_k, max_new_tokens=max_tokens)

    st.subheader("Answer")
    st.write(answer or "Not specified")

    st.subheader("Sources")
    if sources:
        for i, src in enumerate(sources, start=1):
            with st.expander(f"[{i}] {src.get('doc_name','Document')} (chunk {src.get('chunk_id',0)}) • score {src.get('score',0.0):.3f}"):
                st.write(src.get("preview",""))
    else:
        st.caption("No sources (tool or empty result).")

try:
    ensure_qa_index()
except Exception as e:
    st.warning("No indexable document text was found. Upload documents or ensure "
               "`content_text` / `content` exists in st.session_state['documents'].")

with st.form("qa_form"):
    user_q = st.text_area(
        "Your question",
        placeholder="e.g., How many clients? Name the clients I have. Show documents about the Johnson matter.",
    )
    c1, c2 = st.columns(2)
    with c1:
        top_k = st.slider("Top sources (k)", 1, 6, 3)
    with c2:
        max_tokens = st.slider("Max answer tokens", 120, 300, 220)
    submitted = st.form_submit_button("🧾 Ask")

if submitted and user_q.strip():
    with st.spinner("Thinking…"):
        answer, sources = answer_question_hybrid(user_q, k=top_k, max_new_tokens=max_tokens)

    st.subheader("Answer")
    st.write(answer or "Not specified")

    st.subheader("Sources")
    if sources:
        for i, src in enumerate(sources, start=1):
            with st.expander(f"[{i}] {src['doc_name']} (chunk {src.get('chunk_id',0)}) • score {src.get('score',1.0):.3f}"):
                st.write(src.get("preview",""))
    else:
        st.caption("No sources (deterministic tool answer).")



