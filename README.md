# AI-LawFirm

AI-LawFirm is an AI assistant for law firms. It helps lawyers quickly retrieve client context, past communication, and contract details without manually searching through emails and PDFs.

The system is built around a Retrieval-Augmented Generation (RAG) workflow:
1. Ingest internal documents (contracts, notes, client intake forms)
2. Create embeddings and index them in a vector store
3. Retrieve the most relevant context for a user question
4. Generate an answer using an LLM with that context attached

## Goal
Lawyers already have the answers; the problem is finding them. The goal of this project is to let them ask natural questions (e.g. “What did we agree about payment terms with Client A?”) and get an answer with supporting references from their own documents.

## Current work
- Document retrieval and embedding generation
- Context augmentation before LLM inference
- Evaluating / refining prompts to get more consistent answers on legal-style questions
- Building a lightweight knowledge base + search layer

## Tech stack
- Python
- sentence-transformers / Hugging Face
- Vector database (FAISS / similar)
- Prompt assembly for LLM responses
- Streamlit prototype UI

## Status
This is an active work-in-progress. Some parts are experimental and will change. All sample data in this repo is synthetic / redacted.

Next steps:
- Improve retrieval ranking for multi-client cases
- Add grounding / source citations in the final answer
- Tighten prompt structure for recurring legal queries
