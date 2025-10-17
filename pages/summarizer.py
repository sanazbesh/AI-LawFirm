# pages/41_Summarizer.py
import streamlit as st
from datetime import datetime

# Use your original module at project root
from summarizer2 import extract_text_from_file, summarize_text

st.set_page_config(page_title="Summarizer", page_icon="📝", layout="wide")
st.title("📝 Document Summarizer")

# Ensure session buckets exist (so the Questions page can see uploaded docs)
if "documents" not in st.session_state:
    st.session_state["documents"] = []
if "clients" not in st.session_state:
    st.session_state["clients"] = []

col1, col2, col3 = st.columns(3)
with col1:
    f = st.file_uploader("Upload PDF/DOCX/TXT", type=["pdf", "docx", "txt"])
with col2:
    client = st.selectbox("Client (optional)", ["(none)"] + [c.get("name","") for c in st.session_state["clients"]])
with col3:
    matter = st.text_input("Matter/Task (optional)", "")

if f and st.button("Extract & Summarize"):
    with st.spinner("Extracting text…"):
        raw = extract_text_from_file(f)

    with st.spinner("Summarizing…"):
        summary = summarize_text(raw, max_len=220)

    st.subheader("Summary")
    st.write(summary)

    # Save into session so your Questions page / retriever can use it
    st.session_state["documents"].append({
        "id": len(st.session_state["documents"]) + 1,
        "name": f.name,
        "client": (client if client != "(none)" else ""),
        "matter": matter,
        "type": "General Document",
        "date_uploaded": datetime.now().strftime("%Y-%m-%d"),
        "status": "New",
        "summary": summary,
        "content_text": raw if isinstance(raw, str) else "",
    })
    st.success(f"Added '{f.name}' to your document library. You can now query it on the Questions page.")
