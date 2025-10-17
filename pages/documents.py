# pages/documents.py
import io
import os
import uuid
import tempfile
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

# Optional deps for text extraction
try:
    from pypdf import PdfReader          # pip install pypdf
except Exception:  # pragma: no cover
    PdfReader = None

try:
    import docx2txt                      # pip install docx2txt
except Exception:  # pragma: no cover
    docx2txt = None

# Your auth/subscription shim (we keep dev fallbacks so uploads always work)
from services.subscription_manager import EnhancedAuthService


# ---------- Text extraction helpers ----------
def _read_pdf_bytes(b: bytes) -> str:
    if not PdfReader:
        return ""
    try:
        reader = PdfReader(io.BytesIO(b))
        return "\n\n".join((p.extract_text() or "") for p in reader.pages).strip()
    except Exception:
        return ""

def _read_docx_bytes(b: bytes) -> str:
    if not docx2txt:
        return ""
    try:
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=True) as tmp:
            tmp.write(b)
            tmp.flush()
            return (docx2txt.process(tmp.name) or "").strip()
    except Exception:
        return ""

def _read_txt_bytes(b: bytes) -> str:
    try:
        return b.decode("utf-8", errors="ignore").strip()
    except Exception:
        return ""

def _extract_text_from_upload(uploaded_file) -> str:
    name = (uploaded_file.name or "").lower()
    data = uploaded_file.getvalue()
    if name.endswith(".pdf"):
        return _read_pdf_bytes(data)
    if name.endswith(".docx"):
        return _read_docx_bytes(data)
    if name.endswith(".txt"):
        return _read_txt_bytes(data)
    return ""


# ---------- Main page ----------
def show():
    # Styling/header
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg,
                #1a0b2e 0%, #2d1b4e 15%, #1e3a8a 35%,
                #0f172a 50%, #1e3a8a 65%, #16537e 85%, #0891b2 100%) !important;
            min-height: 100vh;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
        }
        .ai-header {
            background: rgba(30, 58, 138, 0.6);
            backdrop-filter: blur(10px);
            padding: 3rem 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            border: 1px solid rgba(59, 130, 246, 0.2);
            box-shadow: 0 4px 20px rgba(0,0,0,.3);
        }
        .ai-header h1 { color: #fff; font-size: 2.2rem; margin: 0; }
        </style>
        <div class="ai-header">
          <h1>📄 Document Management</h1>
          <p>Organize, store, and manage all your legal documents</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize state
    st.session_state.setdefault("documents", [])
    auth_service = EnhancedAuthService()
    user_data = st.session_state.get("user_data", {}) or {}
    org_code = user_data.get("organization_code")

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📋 Dashboard", "📤 Upload", "🔍 Search & Filter", "📊 Analytics", "⚙️ Settings"]
    )

    with tab1:
        show_dashboard_stats(auth_service, org_code)

    with tab2:
        show_upload_interface(auth_service, org_code)

    with tab3:
        show_search_and_filter()

    with tab4:
        show_document_analytics(auth_service, org_code)

    with tab5:
        show_document_settings()


# ---------- Sections ----------
def show_dashboard_stats(auth_service, org_code):
    # Dev-friendly: try subscription, fall back silently
    subscription = None
    try:
        subscription = auth_service.subscription_manager.get_organization_subscription(org_code)
    except Exception:
        pass

    limits = {"storage_gb": 1000}
    storage_used = 0.0
    if subscription:
        try:
            limits = auth_service.subscription_manager.get_plan_limits(subscription.get("plan", "trial"))
            storage_used = float(subscription.get("storage_used_gb", 0.0))
        except Exception:
            pass

    max_storage = float(limits.get("storage_gb", 0))
    storage_pct = (storage_used / max_storage * 100) if max_storage else 0.0

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Documents", len(st.session_state.documents))
    with col2:
        drafts = sum(1 for d in st.session_state.documents if (d.get("status") or "").lower() == "draft")
        st.metric("Draft Documents", drafts)
    with col3:
        label = "Storage Used" if subscription else "Storage Used • Dev (no subscription)"
        st.metric(label, f"{storage_used:.1f}GB / {max_storage:.0f}GB")
    with col4:
        privileged = sum(1 for d in st.session_state.documents if d.get("is_privileged"))
        st.metric("Privileged Documents", privileged)

    # Progress bar + caption (avoid Streamlit version differences)
    st.progress(min(storage_pct / 100.0, 1.0))
    st.caption(f"{storage_pct:.1f}% of {max_storage:.0f}GB used")

    # Recent docs
    st.subheader("Recent Documents")
    if not st.session_state.documents:
        st.info("No documents uploaded yet. Use the Upload tab to add your first document.")
        return

    recent_docs = sorted(
        st.session_state.documents,
        key=lambda d: d.get("upload_date") or datetime.min,
        reverse=True,
    )[:10]

    for doc in recent_docs:
        doc_name = doc.get("name", "Unknown Document")
        with st.expander(f"📄 {doc_name}"):  # no key (compat)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write(f"**Status:** {(doc.get('status') or 'unknown').title()}")
                st.write(f"**Privileged:** {'Yes' if doc.get('is_privileged') else 'No'}")
            with c2:
                st.write(f"**Type:** {doc.get('type','—')}")
                st.write(f"**Size:** {doc.get('size','—')}")
            with c3:
                up = doc.get("upload_date")
                up_str = up.strftime("%Y-%m-%d %H:%M") if isinstance(up, datetime) else "—"
                st.write(f"**Uploaded:** {up_str}")
                if st.button("View", key=f"recent_view_{doc.get('id')}"):
                    st.info("Document viewer would open here")


def show_upload_interface(auth_service, org_code):
    st.subheader("📤 Upload Documents")

    # Try subscription; if missing, allow dev uploading without checks
    subscription = None
    try:
        subscription = auth_service.subscription_manager.get_organization_subscription(org_code)
    except Exception:
        pass

    limits = {"storage_gb": 1000}
    storage_used = 0.0
    if subscription:
        try:
            limits = auth_service.subscription_manager.get_plan_limits(subscription.get("plan", "trial"))
            storage_used = float(subscription.get("storage_used_gb", 0.0))
        except Exception:
            pass

    max_storage = float(limits.get("storage_gb", 0))
    available_storage = max_storage - storage_used

    if subscription:
        st.info(f"Available storage: {available_storage:.1f}GB / {max_storage:.0f}GB")
    else:
        st.info("Dev upload mode: storage checks are disabled on this page.")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("#### Single File Upload")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "docx", "txt", "png", "jpg", "jpeg", "xlsx", "pptx"],
            help="Supported: PDF, Word, Text, Images, Excel, PowerPoint",
        )

        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            st.write(f"**File:** {uploaded_file.name}")
            st.write(f"**Size:** {file_size_mb:.1f} MB")
            st.write(f"**Type:** {uploaded_file.type}")

            # Storage enforcement only if subscription exists
            over_limit = subscription and (not auth_service.check_storage_before_upload(file_size_mb))
            if over_limit:
                st.error("❌ Storage limit exceeded! Cannot upload this file.")
                st.warning(f"File size: {file_size_mb:.1f}MB | Available: {available_storage*1024:.1f}MB")
            else:
                with st.form("file_upload_form"):
                    st.markdown("#### File Details")
                    c1, c2 = st.columns(2)
                    with c1:
                        document_title = st.text_input("Document Title", value=uploaded_file.name)
                        document_type = st.selectbox(
                            "Document Type",
                            [
                                "Contract", "Legal Brief", "Correspondence",
                                "Court Filing", "Research", "Template",
                                "Invoice", "Other",
                            ],
                        )
                        matter_id = st.selectbox(
                            "Associated Matter", options=["None"] + [f"Matter {i+1}" for i in range(5)]
                        )
                    with c2:
                        tags = st.text_input("Tags (comma-separated)", placeholder="urgent, contract, client-a")
                        is_privileged = st.checkbox("Attorney-Client Privileged")
                        description = st.text_area("Description", height=100)

                    if st.form_submit_button("📤 Upload Document", type="primary"):
                        ok = process_document_upload(
                            uploaded_file,
                            document_title,
                            document_type,
                            matter_id,
                            tags,
                            is_privileged,
                            description,
                            auth_service,
                            org_code,
                        )
                        if ok:
                            st.success(f"✅ Uploaded: {document_title}")
                            if subscription:
                                auth_service.subscription_manager.update_storage_usage(org_code, file_size_mb, "add")
                            st.rerun()

        st.divider()

        # Batch upload only if feature available
        can_batch = False
        try:
            can_batch = auth_service.subscription_manager.can_use_feature(org_code, "batch_processing")
        except Exception:
            can_batch = False

        if can_batch:
            st.markdown("#### Batch Upload")
            batch_files = st.file_uploader(
                "Upload multiple files",
                accept_multiple_files=True,
                type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
            )
            if batch_files and st.button("📤 Upload All Files", type="primary"):
                process_batch_upload(batch_files, auth_service, org_code)
        else:
            st.info("🔒 Batch upload requires Professional plan or higher.")

    with col2:
        st.markdown("#### Upload Guidelines")
        if subscription:
            plan = (subscription.get("plan") or "trial").title()
            st.markdown(f"**Plan:** {plan}")
            st.markdown("**Max file size:** 100MB")
            st.markdown(f"**Storage limit:** {max_storage:.0f}GB")
        else:
            st.markdown("**Mode:** Developer")
            st.markdown("**Max file size:** 100MB (soft)")

        st.markdown("#### Supported Formats")
        for t in ["📄 PDF", "📝 Word", "📑 Text", "🖼️ Images (JPG, PNG)", "📊 Excel", "📋 PowerPoint"]:
            st.write(t)

        st.markdown("#### Quick Actions")
        if st.button("📁 View All Documents"):
            st.toast("Scroll down to Search & Filter tab for listing.")

        if st.button("📊 Storage Report"):
            show_storage_report(auth_service, org_code)


def process_document_upload(
    uploaded_file,
    title,
    doc_type,
    matter_id,
    tags,
    is_privileged,
    description,
    auth_service,
    org_code,
):
    """Save metadata to session and extract text for RAG."""
    try:
        raw_text = _extract_text_from_upload(uploaded_file)
        if not raw_text:
            st.warning(
                f"Could not extract text from '{uploaded_file.name}'. "
                "It will be saved, but the Questions page won't use it."
            )

        new_doc = {
            "id": str(uuid.uuid4()),
            "name": title or uploaded_file.name,
            "original_filename": uploaded_file.name,
            "type": doc_type,
            "matter_id": matter_id if matter_id != "None" else None,
            "matter": matter_id if matter_id != "None" else "",
            "client": "",  # add later if you collect it
            "status": "active",
            "tags": [t.strip() for t in (tags or "").split(",") if t.strip()],
            "is_privileged": bool(is_privileged),
            "description": description or "",
            "size": f"{uploaded_file.size / (1024 * 1024):.1f} MB",
            "upload_date": datetime.now(),
            "uploaded_by": (st.session_state.get("user_data", {}) or {}).get("name", "Unknown"),
            "organization_code": org_code,
            # Fields the retriever expects:
            "content_text": raw_text,
            "summary": "",
        }

        st.session_state.setdefault("documents", [])
        st.session_state.documents.append(new_doc)

        # Invalidate QA index so Questions page rebuilds
        st.session_state.pop("qa_engine", None)
        st.session_state.pop("qa_digest", None)

        return True
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return False


def process_batch_upload(batch_files, auth_service, org_code):
    progress = st.progress(0.0)
    ok = 0
    for i, f in enumerate(batch_files):
        if process_document_upload(
            f, f.name, "Other", "None", "", False, "", auth_service, org_code
        ):
            ok += 1
        progress.progress((i + 1) / len(batch_files))
    st.success(f"Batch upload complete: {ok}/{len(batch_files)} files.")


def show_search_and_filter():
    st.subheader("🔍 Search & Filter Documents")

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        q = st.text_input("🔎 Search", placeholder="Enter keywords, tags, or document names…")
    with c2:
        doc_type = st.selectbox(
            "Document Type",
            ["All Types", "Contract", "Legal Brief", "Correspondence",
             "Court Filing", "Research", "Template", "Invoice", "Other"],
        )
    with c3:
        date_range = st.selectbox("Date Range", ["All Time", "Last 7 days", "Last 30 days", "Last 90 days", "This Year"])

    with st.expander("🔧 Advanced Filters"):
        c1, c2, c3 = st.columns(3)
        with c1:
            matter_filter = st.selectbox("Matter", ["All Matters"] + [f"Matter {i+1}" for i in range(5)])
            priv_filter = st.selectbox("Privilege Status", ["All", "Privileged Only", "Non-Privileged Only"])
        with c2:
            size_filter = st.selectbox("File Size", ["All Sizes", "< 1MB", "1-10MB", "10-100MB", "> 100MB"])
            status_filter = st.selectbox("Status", ["All Status", "Active", "Draft", "Archived"])
        with c3:
            uploaded_by = st.selectbox("Uploaded By", ["All Users", "Me", "Others"])
            tags_filter = st.text_input("Tags", placeholder="Enter tags to filter by")

    # Minimal filtering (extend as needed)
    docs = list(st.session_state.documents)
    if q:
        ql = q.lower()
        docs = [d for d in docs if ql in (d.get("name","").lower() + " " + d.get("description","").lower()) or any(ql in t.lower() for t in d.get("tags",[]))]
    if doc_type != "All Types":
        docs = [d for d in docs if d.get("type") == doc_type]
    if date_range != "All Time":
        cutoff = _date_cutoff(date_range)
        docs = [d for d in docs if (d.get("upload_date") or datetime.min) >= cutoff]

    st.markdown(f"### Search Results ({len(docs)} documents)")
    if not docs:
        st.info("No documents match your search criteria.")
        return

    # View options
    c1, c2 = st.columns(2)
    with c1:
        view_mode = st.radio("View Mode", ["List", "Grid", "Table"], horizontal=True)
    with c2:
        sort_by = st.selectbox("Sort By", ["Upload Date", "Name", "Size", "Type"])

    docs = _sort_documents(docs, sort_by)

    if view_mode == "List":
        _list_view(docs)
    elif view_mode == "Grid":
        _grid_view(docs)
    else:
        _table_view(docs)


def _date_cutoff(label: str) -> datetime:
    now = datetime.now()
    if label == "Last 7 days":
        return now - timedelta(days=7)
    if label == "Last 30 days":
        return now - timedelta(days=30)
    if label == "Last 90 days":
        return now - timedelta(days=90)
    if label == "This Year":
        return now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    return datetime.min


def _sort_documents(docs, by: str):
    if by == "Name":
        return sorted(docs, key=lambda d: (d.get("name") or "").lower())
    if by == "Upload Date":
        return sorted(docs, key=lambda d: d.get("upload_date") or datetime.min, reverse=True)
    if by == "Size":
        # naive lexical sort on "X.Y MB" works okay for demo
        return sorted(docs, key=lambda d: d.get("size","0"))
    if by == "Type":
        return sorted(docs, key=lambda d: d.get("type",""))
    return docs


def _list_view(docs):
    for d in docs:
        with st.expander(f"📄 {d.get('name','Unknown')} - {d.get('type','Unknown')}"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write(f"**Type:** {d.get('type','—')}")
                st.write(f"**Size:** {d.get('size','—')}")
                up = d.get("upload_date")
                st.write(f"**Uploaded:** {up.strftime('%Y-%m-%d') if isinstance(up, datetime) else '—'}")
            with c2:
                st.write(f"**Status:** {d.get('status','Unknown')}")
                st.write(f"**Privileged:** {'Yes' if d.get('is_privileged') else 'No'}")
                st.write(f"**Uploaded by:** {d.get('uploaded_by','Unknown')}")
            with c3:
                if d.get("tags"):
                    st.write(f"**Tags:** {', '.join(d['tags'])}")
                if d.get("description"):
                    st.write(f"**Description:** {d['description'][:100]}...")

            a1, a2, a3, a4 = st.columns(4)
            did = d.get("id")
            with a1:
                if st.button("👁️ View", key=f"list_view_{did}"):
                    st.info("Document viewer would open here")
            with a2:
                if st.button("📥 Download", key=f"list_download_{did}"):
                    st.info("Download would start here")
            with a3:
                if st.button("✏️ Edit", key=f"list_edit_{did}"):
                    st.info("Edit interface would open here")
            with a4:
                if st.button("🗑️ Delete", key=f"list_delete_{did}"):
                    delete_document(d, (st.session_state.get("user_data", {}) or {}).get("organization_code"))


def _grid_view(docs):
    cols_per_row = 3
    for i in range(0, len(docs), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, d in enumerate(docs[i : i + cols_per_row]):
            with cols[j]:
                st.markdown(f"**📄 {d.get('name','Unknown')[:22]}**")
                st.write(f"Type: {d.get('type','—')}")
                st.write(f"Size: {d.get('size','—')}")
                if st.button("View", key=f"grid_view_{d.get('id')}"):
                    st.info("Document viewer would open here")


def _table_view(docs):
    rows = []
    for d in docs:
        up = d.get("upload_date")
        rows.append(
            {
                "Name": d.get("name", "Unknown"),
                "Type": d.get("type", "Unknown"),
                "Size": d.get("size", "Unknown"),
                "Upload Date": up.strftime("%Y-%m-%d") if isinstance(up, datetime) else "—",
                "Status": d.get("status", "Unknown"),
                "Privileged": "Yes" if d.get("is_privileged") else "No",
            }
        )
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)


def delete_document(doc, org_code):
    try:
        st.session_state["documents"] = [d for d in st.session_state["documents"] if d.get("id") != doc.get("id")]
        # If you track storage, adjust here (guard for missing subscription manager in dev)
        try:
            auth_service = EnhancedAuthService()
            size_str = doc.get("size", "0 MB")
            size_mb = float(size_str.split()[0]) if "MB" in size_str else 0.0
            auth_service.subscription_manager.update_storage_usage(org_code, size_mb, "remove")
        except Exception:
            pass
        # Invalidate QA index after deletion too
        st.session_state.pop("qa_engine", None)
        st.session_state.pop("qa_digest", None)
        st.success(f"Deleted '{doc.get('name','Document')}'.")
        st.rerun()
    except Exception as e:
        st.error(f"Error deleting document: {e}")


def show_document_analytics(auth_service, org_code):
    st.subheader("📊 Document Analytics")
    if not st.session_state.documents:
        st.info("No documents available for analytics.")
        return

    c1, c2 = st.columns(2)
    with c1:
        counts = {}
        for d in st.session_state.documents:
            t = d.get("type", "Unknown")
            counts[t] = counts.get(t, 0) + 1
        if counts:
            fig = px.pie(values=list(counts.values()), names=list(counts.keys()), title="Document Types")
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        # simple mock trend
        dates = pd.date_range(datetime.now() - timedelta(days=240), periods=9, freq="M")
        uploads = [max(1, i) for i in range(1, 10)]
        fig2 = px.line(x=dates, y=uploads, title="Uploads Over Time")
        fig2.update_layout(xaxis_title="Month", yaxis_title="Documents")
        st.plotly_chart(fig2, use_container_width=True)

    show_storage_analytics(auth_service, org_code)


def show_storage_analytics(auth_service, org_code):
    # Try subscription, tolerate dev
    storage_used = 0.0
    max_storage = 1000.0
    try:
        subscription = auth_service.subscription_manager.get_organization_subscription(org_code)
        limits = auth_service.subscription_manager.get_plan_limits(subscription.get("plan", "trial"))
        storage_used = float(subscription.get("storage_used_gb", 0.0))
        max_storage = float(limits.get("storage_gb", 1000))
    except Exception:
        pass

    st.subheader("💾 Storage Analytics")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Storage Used", f"{storage_used:.2f} GB")
    with c2:
        st.metric("Storage Limit", f"{max_storage:.0f} GB")
    with c3:
        st.metric("Remaining", f"{max_storage - storage_used:.2f} GB")

    dates = pd.date_range(datetime.now() - timedelta(days=29), periods=30, freq="D")
    usage = [min(storage_used + i * 0.02, max_storage) for i in range(30)]
    fig = px.line(x=dates, y=usage, title="Storage Usage Over Time")
    fig.update_layout(xaxis_title="Date", yaxis_title="Storage Used (GB)")
    st.plotly_chart(fig, use_container_width=True)


def show_storage_report(auth_service, org_code):
    st.subheader("📊 Storage Usage Report")
    try:
        subscription = auth_service.subscription_manager.get_organization_subscription(org_code)
        limits = auth_service.subscription_manager.get_plan_limits(subscription.get("plan", "trial"))
        storage_used = float(subscription.get("storage_used_gb", 0.0))
        max_storage = float(limits.get("storage_gb", 0))
        st.write(f"**Current Plan:** {(subscription.get('plan') or 'trial').title()}")
        st.write(f"**Storage Used:** {storage_used:.2f} GB / {max_storage:.0f} GB")
        pct = (storage_used / max_storage * 100) if max_storage else 0.0
        st.write(f"**Usage Percentage:** {pct:.1f}%")
    except Exception:
        st.info("Dev report: subscription not available.")


def show_document_settings():
    st.subheader("⚙️ Document Settings")
    user_data = st.session_state.get("user_data", {}) or {}
    org_code = user_data.get("organization_code")

    auth_service = EnhancedAuthService()
    try:
        subscription = auth_service.subscription_manager.get_organization_subscription(org_code)
        limits = auth_service.subscription_manager.get_plan_limits(subscription.get("plan", "trial"))
    except Exception:
        subscription, limits = None, {"storage_gb": 1000}

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Default Settings")
        default_doc_type = st.selectbox(
            "Default Document Type",
            ["Contract", "Legal Brief", "Correspondence", "Court Filing", "Research", "Template", "Invoice", "Other"],
            index=0,
        )
        auto_extract_text = st.checkbox("Auto-extract text from uploaded documents", value=True)
        auto_tag_documents = st.checkbox("Enable automatic document tagging", value=True)

        st.markdown("#### Notifications")
        notify_upload = st.checkbox("Notify on document upload", value=True)
        notify_share = st.checkbox("Notify when documents are shared", value=True)
        notify_expire = st.checkbox("Notify before document expiration", value=False)

    with c2:
        st.markdown("#### Security Settings")
        require_approval = st.checkbox("Require approval for document sharing", value=False)
        watermark_documents = st.checkbox("Add watermark to downloaded documents", value=False)
        st.markdown("#### Document Retention")
        auto_archive_days = st.number_input("Auto-archive after (days)", min_value=0, value=365)
        auto_delete_days = st.number_input("Auto-delete archived after (days)", min_value=0, value=0)
        if auto_delete_days > 0:
            st.warning("Auto-deletion is permanent and cannot be undone!")

    # Storage overview
    st.markdown("#### Storage Management")
    storage_used = 0.0
    max_storage = float(limits.get("storage_gb", 1000))
    try:
        if subscription:
            storage_used = float(subscription.get("storage_used_gb", 0.0))
    except Exception:
        pass
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Current Usage", f"{storage_used:.1f}GB")
    with c2:
        st.metric("Plan Limit", f"{max_storage:.0f}GB")
    with c3:
        st.metric("Available", f"{max_storage - storage_used:.1f}GB")

    if st.button("💾 Save All Settings", type="primary"):
        st.session_state["document_settings"] = {
            "default_doc_type": default_doc_type,
            "auto_extract_text": auto_extract_text,
            "auto_tag_documents": auto_tag_documents,
            "notify_upload": notify_upload,
            "notify_share": notify_share,
            "notify_expire": notify_expire,
            "require_approval": require_approval,
            "watermark_documents": watermark_documents,
            "auto_archive_days": auto_archive_days,
            "auto_delete_days": auto_delete_days,
        }
        st.success("Settings saved.")


# Run standalone
if __name__ == "__main__":
    show()
