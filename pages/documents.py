import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid
import os
from services.subscription_manager import EnhancedAuthService
def show():
    # Professional header styling
    st.markdown("""
    <style>
    /* Match main app background */
    .stApp {
        background: linear-gradient(135deg, 
            #1a0b2e 0%,
            #2d1b4e 15%,
            #1e3a8a 35%,
            #0f172a 50%,
            #1e3a8a 65%,
            #16537e 85%,
            #0891b2 100%) !important;
        min-height: 100vh;
        position: relative;
    }
    
    /* Geometric overlay pattern */
    .stApp::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(168, 85, 247, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(14, 165, 233, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.05) 0%, transparent 50%);
        pointer-events: none;
    }
    /* Sidebar styling - must be in each page file */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 2rem 1rem !important;
    }
    
    [data-testid="stSidebar"] .css-17eq0hr {
        color: white !important;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] button {
        background: rgba(255,255,255,0.15) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        width: 100% !important;
    }
    
    [data-testid="stSidebar"] button:hover {
        background: rgba(255,255,255,0.25) !important;
    }
    .ai-header {
        background: rgba(30, 58, 138, 0.6);
        backdrop-filter: blur(10px);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    .ai-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    /* Default: Light text everywhere */
    * {
        color: #e2e8f0 !important;
    }
    
    /* Headers - light */
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }
    
    /* Dark text ONLY inside white expander boxes */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background: white !important;
    }
    
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] * {
        color: #1e293b !important;
    }
    
    /* Dark text in forms */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.95) !important;
    }
    
    [data-testid="stForm"] * {
        color: #1e293b !important;
    }
    
    /* Metrics - keep colored */
    [data-testid="stMetricValue"] {
        color: #60a5fa !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
    }
    
    /* Input fields */
    input, textarea, select {
        color: #1e293b !important;
        background: white !important;
    }
    
    /* Buttons */
    .stButton button * {
        color: white !important;
    }
    
    /* Info/warning/error boxes - keep light text */
    .stAlert, .stSuccess, .stWarning, .stError, .stInfo {
        color: #1e293b !important;
    }

    /* Dropdown menus - dark text */
    [data-baseweb="select"] [role="listbox"],
    [data-baseweb="select"] [role="option"],
    [data-baseweb="popover"] {
        background: white !important;
    }
    
    [data-baseweb="select"] [role="listbox"] *,
    [data-baseweb="select"] [role="option"] *,
    [data-baseweb="popover"] * {
        color: #1e293b !important;
    }
    
    /* Dropdown list items */
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] li *,
    div[role="listbox"] li,
    div[role="listbox"] li * {
        color: #1e293b !important;
        background: white !important;
    }
    
    /* Select/dropdown text */
    .stSelectbox [data-baseweb="select"] > div {
        color: #1e293b !important;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        border-left: 4px solid #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        background-color: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        font-weight: 600;
        color: #cbd5e1;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(59, 130, 246, 0.8);
        color: white;
    }
    

    </style>
    <div class="ai-header">
        <h1>📄 Document Management</h1>
        <p>Organize, store, and manage all your legal documents</p>
    </div>
    """, unsafe_allow_html=True)
    # OLD:
    auth_service = AuthService()

    # NEW:
    auth_service = EnhancedAuthService()
    
    
    # Initialize documents in session state if not exists
    if 'documents' not in st.session_state:
        st.session_state.documents = []
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Dashboard", 
        "📤 Upload", 
        "🔍 Search & Filter", 
        "📊 Analytics", 
        "⚙️ Settings"
    ])
    
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

def show_dashboard_stats(auth_service, org_code):
    """Show document management dashboard with subscription-aware stats"""
    
    # Get subscription info for display
    subscription = auth_service.subscription_manager.get_organization_subscription(org_code)
    limits = auth_service.subscription_manager.get_plan_limits(subscription["plan"])
    
    # Storage usage display
    storage_used = subscription.get("storage_used_gb", 0)
    max_storage = limits.get("storage_gb", 0)
    storage_percentage = (storage_used / max_storage * 100) if max_storage > 0 else 0
    
    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_docs = len(st.session_state.documents)
        st.metric("Total Documents", total_docs)
    
    with col2:
        draft_count = len([d for d in st.session_state.documents 
                          if getattr(d, 'status', d.get('status') if isinstance(d, dict) else None) == 'draft'])
        st.metric("Draft Documents", draft_count)
    
    with col3:
        st.metric("Storage Used", f"{storage_used:.1f}GB / {max_storage}GB")
        if storage_percentage > 90:
            st.error("Storage almost full!")
        elif storage_percentage > 75:
            st.warning("Storage getting full")
    
    with col4:
        privileged_count = len([d for d in st.session_state.documents 
                               if getattr(d, 'is_privileged', False)])
        st.metric("Privileged Documents", privileged_count)
    
    # Storage usage progress bar
    st.subheader("Storage Usage")
    progress_color = "red" if storage_percentage > 90 else "orange" if storage_percentage > 75 else "green"
    st.progress(min(storage_percentage / 100, 1.0), text=f"{storage_percentage:.1f}% of {max_storage}GB used")
    
    if storage_percentage > 80:
        st.warning("Consider upgrading your storage plan or removing old documents.")
        if st.button("Upgrade Storage Plan"):
            st.session_state['show_upgrade_modal'] = True
            st.rerun()
    
    # Recent documents
    st.subheader("Recent Documents")
    
    if st.session_state.documents:
        # Sort documents by date if available
        recent_docs = sorted(
            st.session_state.documents, 
            key=lambda x: getattr(x, 'upload_date', datetime.now()) if hasattr(x, 'upload_date') else datetime.now(),
            reverse=True
        )[:10]
        
        for doc in recent_docs:
            doc_name = getattr(doc, 'name', 'Unknown Document')
            doc_status = getattr(doc, 'status', 'unknown')
            doc_size = getattr(doc, 'size', 'Unknown size')
            
            with st.expander(f"📄 {doc_name}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Status:** {doc_status.title()}")
                
                with col2:
                    st.write(f"**Size:** {doc_size}")
                
                with col3:
                    if st.button("View", key=f"view_{doc_name}"):
                        st.info("Document viewer would open here")
    else:
        st.info("No documents uploaded yet. Use the Upload tab to add your first document.")

def show_upload_interface(auth_service, org_code):
    """Document upload interface with subscription-based storage limits"""
    
    st.subheader("📤 Upload Documents")
    
    # Get current subscription limits
    subscription = auth_service.subscription_manager.get_organization_subscription(org_code)
    limits = auth_service.subscription_manager.get_plan_limits(subscription["plan"])
    
    # Display storage info
    storage_used = subscription.get("storage_used_gb", 0)
    max_storage = limits.get("storage_gb", 0)
    available_storage = max_storage - storage_used
    
    st.info(f"Available storage: {available_storage:.1f}GB / {max_storage}GB")
    
    # File upload interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Single file upload
        st.markdown("#### Single File Upload")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg', 'xlsx', 'pptx'],
            help="Supported formats: PDF, Word, Text, Images, Excel, PowerPoint"
        )
        
        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            st.write(f"**File:** {uploaded_file.name}")
            st.write(f"**Size:** {file_size_mb:.1f} MB")
            st.write(f"**Type:** {uploaded_file.type}")
            
            # Check storage limits before upload
            if not auth_service.check_storage_before_upload(file_size_mb):
                st.error("❌ Storage limit exceeded! Cannot upload this file.")
                st.warning(f"File size: {file_size_mb:.1f}MB | Available space: {available_storage*1024:.1f}MB")
                
                col_error1, col_error2 = st.columns(2)
                with col_error1:
                    if st.button("🗑️ Delete Old Files"):
                        st.info("File management interface would open here")
                
                with col_error2:
                    if st.button("⬆️ Upgrade Storage"):
                        st.session_state['show_upgrade_modal'] = True
                        st.rerun()
            
            else:
                # File metadata form
                with st.form("file_upload_form"):
                    st.markdown("#### File Details")
                    
                    col_form1, col_form2 = st.columns(2)
                    
                    with col_form1:
                        document_title = st.text_input("Document Title", value=uploaded_file.name)
                        document_type = st.selectbox("Document Type", [
                            "Contract", "Legal Brief", "Correspondence", 
                            "Court Filing", "Research", "Template", 
                            "Invoice", "Other"
                        ])
                        matter_id = st.selectbox("Associated Matter", 
                                               options=["None"] + [f"Matter {i+1}" for i in range(5)])
                    
                    with col_form2:
                        tags = st.text_input("Tags (comma-separated)", placeholder="urgent, contract, client-a")
                        is_privileged = st.checkbox("Attorney-Client Privileged")
                        description = st.text_area("Description", height=100)
                    
                    # Upload button
                    if st.form_submit_button("📤 Upload Document", type="primary"):
                        # Process the upload
                        success = process_document_upload(
                            uploaded_file, document_title, document_type, 
                            matter_id, tags, is_privileged, description,
                            auth_service, org_code
                        )
                        
                        if success:
                            st.success(f"✅ Successfully uploaded: {document_title}")
                            st.info("Document has been processed and added to your document library.")
                            
                            # Update storage usage
                            auth_service.subscription_manager.update_storage_usage(org_code, file_size_mb, "add")
                            
                            # Refresh the page to show updated stats
                            st.rerun()
        
        # Batch upload (Professional+ only)
        st.divider()
        
        if auth_service.can_use_feature(org_code, "batch_processing"):
            st.markdown("#### Batch Upload")
            batch_files = st.file_uploader(
                "Upload multiple files",
                accept_multiple_files=True,
                type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'],
                help="Professional and Enterprise plans support batch upload"
            )
            
            if batch_files:
                total_size_mb = sum(file.size for file in batch_files) / (1024 * 1024)
                st.write(f"**Files selected:** {len(batch_files)}")
                st.write(f"**Total size:** {total_size_mb:.1f} MB")
                
                # Check if batch upload fits within storage limits
                if auth_service.check_storage_before_upload(total_size_mb):
                    if st.button("📤 Upload All Files", type="primary"):
                        process_batch_upload(batch_files, auth_service, org_code)
                else:
                    st.error(f"❌ Batch upload exceeds storage limit ({total_size_mb:.1f}MB)")
        else:
            st.info("🔒 Batch upload requires Professional plan or higher.")
            if st.button("Upgrade for Batch Upload"):
                st.session_state['show_upgrade_modal'] = True
                st.rerun()
    
    with col2:
        # Upload guidelines and limits
        st.markdown("#### Upload Guidelines")
        
        st.markdown(f"**Plan:** {subscription['plan'].title()}")
        st.markdown(f"**Max file size:** 100MB")
        st.markdown(f"**Storage limit:** {max_storage}GB")
        
        st.markdown("#### Supported Formats")
        formats = [
            "📄 PDF documents",
            "📝 Word documents", 
            "📊 Excel spreadsheets",
            "🖼️ Images (JPG, PNG)",
            "📑 Text files",
            "📋 PowerPoint presentations"
        ]
        
        for format_type in formats:
            st.write(format_type)
        
        # Quick actions
        st.markdown("#### Quick Actions")
        
        if st.button("📁 View All Documents"):
            st.session_state['current_page'] = 'Document Management'
            st.rerun()
        
        if st.button("🔍 Search Documents"):
            st.info("Search interface would open here")
        
        if st.button("📊 Storage Report"):
            show_storage_report(auth_service, org_code)

def process_document_upload(uploaded_file, title, doc_type, matter_id, tags, is_privileged, description, auth_service, org_code):
    """Process single document upload"""
    try:
        # Create document object
        new_document = {
            'id': str(uuid.uuid4()),
            'name': title,
            'original_filename': uploaded_file.name,
            'type': doc_type,
            'matter_id': matter_id if matter_id != "None" else None,
            'tags': [tag.strip() for tag in tags.split(',') if tag.strip()],
            'is_privileged': is_privileged,
            'description': description,
            'size': f"{uploaded_file.size / (1024 * 1024):.1f} MB",
            'upload_date': datetime.now(),
            'uploaded_by': st.session_state.user_data.get('name', 'Unknown'),
            'status': 'active',
            'organization_code': org_code
        }
        
        # Add to session state
        st.session_state.documents.append(new_document)
        
        # In a real app, you would save the file to storage here
        # For demo purposes, we just track the metadata
        
        return True
        
    except Exception as e:
        st.error(f"Upload failed: {str(e)}")
        return False

def process_batch_upload(batch_files, auth_service, org_code):
    """Process multiple file uploads"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    successful_uploads = 0
    total_files = len(batch_files)
    
    for i, file in enumerate(batch_files):
        status_text.text(f"Uploading {file.name}...")
        
        # Process each file
        success = process_document_upload(
            file, file.name, "Other", "None", "", False, "",
            auth_service, org_code
        )
        
        if success:
            successful_uploads += 1
            # Update storage for each file
            file_size_mb = file.size / (1024 * 1024)
            auth_service.subscription_manager.update_storage_usage(org_code, file_size_mb, "add")
        
        # Update progress
        progress_bar.progress((i + 1) / total_files)
    
    status_text.text(f"Batch upload complete: {successful_uploads}/{total_files} files uploaded successfully")
    
    if successful_uploads == total_files:
        st.success(f"✅ All {total_files} files uploaded successfully!")
    else:
        st.warning(f"⚠️ {successful_uploads}/{total_files} files uploaded. Some uploads failed.")

def show_search_and_filter():
    """Document search and filtering interface"""
    st.subheader("🔍 Search & Filter Documents")
    
    # Search interface
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search documents", placeholder="Enter keywords, tags, or document names...")
    
    with col2:
        doc_type_filter = st.selectbox("Document Type", 
                                     ["All Types"] + ["Contract", "Legal Brief", "Correspondence", 
                                                     "Court Filing", "Research", "Template", "Invoice", "Other"])
    
    with col3:
        date_filter = st.selectbox("Date Range", 
                                 ["All Time", "Last 7 days", "Last 30 days", "Last 90 days", "This Year"])
    
    # Advanced filters
    with st.expander("🔧 Advanced Filters"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            matter_filter = st.selectbox("Matter", ["All Matters"] + [f"Matter {i+1}" for i in range(5)])
            privileged_filter = st.selectbox("Privilege Status", ["All", "Privileged Only", "Non-Privileged Only"])
        
        with col2:
            size_filter = st.selectbox("File Size", ["All Sizes", "< 1MB", "1-10MB", "10-100MB", "> 100MB"])
            status_filter = st.selectbox("Status", ["All Status", "Active", "Draft", "Archived"])
        
        with col3:
            uploaded_by_filter = st.selectbox("Uploaded By", ["All Users", "Me", "Others"])
            tags_filter = st.text_input("Tags", placeholder="Enter tags to filter by")
    
    # Apply filters and show results
    filtered_documents = apply_document_filters(
        st.session_state.documents, search_query, doc_type_filter, 
        date_filter, matter_filter, privileged_filter
    )
    
    # Results
    st.markdown(f"### Search Results ({len(filtered_documents)} documents)")
    
    if filtered_documents:
        # Display options
        col1, col2 = st.columns([1, 1])
        
        with col1:
            view_mode = st.radio("View Mode", ["List", "Grid", "Table"], horizontal=True)
        
        with col2:
            sort_by = st.selectbox("Sort By", ["Upload Date", "Name", "Size", "Type", "Last Modified"])
        
        # Sort documents
        filtered_documents = sort_documents(filtered_documents, sort_by)
        
        # Display documents
        if view_mode == "List":
            show_document_list(filtered_documents)
        elif view_mode == "Grid":
            show_document_grid(filtered_documents)
        else:
            show_document_table(filtered_documents)
    
    else:
        st.info("No documents match your search criteria.")

def apply_document_filters(documents, search_query, doc_type, date_filter, matter_filter, privileged_filter):
    """Apply filters to document list"""
    filtered = documents.copy()
    
    # Search query filter
    if search_query:
        search_lower = search_query.lower()
        filtered = [doc for doc in filtered 
                   if search_lower in doc.get('name', '').lower() or 
                      search_lower in doc.get('description', '').lower() or
                      any(search_lower in tag.lower() for tag in doc.get('tags', []))]
    
    # Document type filter
    if doc_type != "All Types":
        filtered = [doc for doc in filtered if doc.get('type') == doc_type]
    
    # Date filter
    if date_filter != "All Time":
        cutoff_date = get_date_cutoff(date_filter)
        filtered = [doc for doc in filtered 
                   if doc.get('upload_date', datetime.now()) >= cutoff_date]
    
    return filtered

def get_date_cutoff(date_filter):
    """Get cutoff date based on filter selection"""
    now = datetime.now()
    
    if date_filter == "Last 7 days":
        return now - timedelta(days=7)
    elif date_filter == "Last 30 days":
        return now - timedelta(days=30)
    elif date_filter == "Last 90 days":
        return now - timedelta(days=90)
    elif date_filter == "This Year":
        return now.replace(month=1, day=1, hour=0, minute=0, second=0)
    
    return datetime.min

def sort_documents(documents, sort_by):
    """Sort documents based on criteria"""
    if sort_by == "Name":
        return sorted(documents, key=lambda x: x.get('name', '').lower())
    elif sort_by == "Upload Date":
        return sorted(documents, key=lambda x: x.get('upload_date', datetime.min), reverse=True)
    elif sort_by == "Size":
        return sorted(documents, key=lambda x: x.get('size', '0'), reverse=True)
    elif sort_by == "Type":
        return sorted(documents, key=lambda x: x.get('type', ''))
    
    return documents

def show_document_list(documents):
    """Show documents in list view"""
    for doc in documents:
        with st.expander(f"📄 {doc.get('name', 'Unknown')} - {doc.get('type', 'Unknown Type')}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Type:** {doc.get('type', 'Unknown')}")
                st.write(f"**Size:** {doc.get('size', 'Unknown')}")
                st.write(f"**Uploaded:** {doc.get('upload_date', 'Unknown').strftime('%Y-%m-%d') if isinstance(doc.get('upload_date'), datetime) else 'Unknown'}")
            
            with col2:
                st.write(f"**Status:** {doc.get('status', 'Unknown')}")
                st.write(f"**Privileged:** {'Yes' if doc.get('is_privileged') else 'No'}")
                st.write(f"**Uploaded by:** {doc.get('uploaded_by', 'Unknown')}")
            
            with col3:
                if doc.get('tags'):
                    st.write(f"**Tags:** {', '.join(doc['tags'])}")
                if doc.get('description'):
                    st.write(f"**Description:** {doc['description'][:100]}...")
            
            # Action buttons
            col_action1, col_action2, col_action3, col_action4 = st.columns(4)
            
            with col_action1:
                if st.button("👁️ View", key=f"view_{doc['id']}"):
                    st.info("Document viewer would open here")
            
            with col_action2:
                if st.button("📥 Download", key=f"download_{doc['id']}"):
                    st.info("Download would start here")
            
            with col_action3:
                if st.button("✏️ Edit", key=f"edit_{doc['id']}"):
                    st.info("Edit interface would open here")
            
            with col_action4:
                if st.button("🗑️ Delete", key=f"delete_{doc['id']}"):
                    delete_document(doc, st.session_state.user_data.get('organization_code'))

def show_document_grid(documents):
    """Show documents in grid view"""
    cols_per_row = 3
    for i in range(0, len(documents), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, doc in enumerate(documents[i:i+cols_per_row]):
            with cols[j]:
                with st.container():
                    st.markdown(f"**📄 {doc.get('name', 'Unknown')[:20]}...**")
                    st.write(f"Type: {doc.get('type', 'Unknown')}")
                    st.write(f"Size: {doc.get('size', 'Unknown')}")
                    
                    if st.button("View", key=f"grid_view_{doc['id']}"):
                        st.info("Document viewer would open here")

def show_document_table(documents):
    """Show documents in table view"""
    if documents:
        # Create DataFrame for table display
        table_data = []
        for doc in documents:
            table_data.append({
                "Name": doc.get('name', 'Unknown'),
                "Type": doc.get('type', 'Unknown'),
                "Size": doc.get('size', 'Unknown'),
                "Upload Date": doc.get('upload_date', datetime.now()).strftime('%Y-%m-%d') if isinstance(doc.get('upload_date'), datetime) else 'Unknown',
                "Status": doc.get('status', 'Unknown'),
                "Privileged": "Yes" if doc.get('is_privileged') else "No"
            })
        
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)

def delete_document(doc, org_code):
    """Delete a document and update storage usage"""
    try:
        # Remove from session state
        st.session_state.documents = [d for d in st.session_state.documents if d['id'] != doc['id']]
        
        # Update storage usage
        from services.subscription_manager import EnhancedAuthService
        auth_service = EnhancedAuthService()
        
        # Parse size string and update storage
        size_str = doc.get('size', '0 MB')
        size_mb = float(size_str.split()[0]) if 'MB' in size_str else 0
        auth_service.subscription_manager.update_storage_usage(org_code, size_mb, "remove")
        
        st.success(f"Document '{doc['name']}' deleted successfully!")
        st.rerun()
        
    except Exception as e:
        st.error(f"Error deleting document: {str(e)}")

def show_document_analytics(auth_service, org_code):
    """Show document analytics dashboard"""
    
    # Check if advanced analytics are available
    if not auth_service.can_use_feature(org_code, "advanced_analytics"):
        st.warning("📊 Advanced Document Analytics requires Professional plan or higher.")
        if st.button("Upgrade to Professional"):
            st.session_state['show_upgrade_modal'] = True
            st.rerun()
        
        # Show basic analytics only
        show_basic_document_analytics()
        return
    
    st.subheader("📊 Document Analytics")
    
    # Analytics dashboard
    if st.session_state.documents:
        # Document type distribution
        col1, col2 = st.columns(2)
        
        with col1:
            doc_types = {}
            for doc in st.session_state.documents:
                doc_type = doc.get('type', 'Unknown')
                doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
            
            if doc_types:
                fig1 = px.pie(values=list(doc_types.values()), names=list(doc_types.keys()),
                             title="Document Distribution by Type")
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Upload trends (mock data)
            dates = pd.date_range('2024-01-01', '2024-09-01', freq='M')
            upload_counts = [5, 8, 12, 15, 20, 18, 22, 25, 30]
            
            fig2 = px.line(x=dates, y=upload_counts, title="Document Upload Trends")
            fig2.update_layout(xaxis_title="Month", yaxis_title="Documents Uploaded")
            st.plotly_chart(fig2, use_container_width=True)
        
        # Storage analytics
        show_storage_analytics(auth_service, org_code)
    
    else:
        st.info("No documents available for analytics.")

def show_basic_document_analytics():
    """Show basic analytics for Starter plan users"""
    st.subheader("📊 Basic Document Analytics")
    
    if st.session_state.documents:
        # Basic stats
        total_docs = len(st.session_state.documents)
        doc_types = {}
        
        for doc in st.session_state.documents:
            doc_type = doc.get('type', 'Unknown')
            doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Documents", total_docs)
            st.metric("Document Types", len(doc_types))
        
        with col2:
            most_common_type = max(doc_types.items(), key=lambda x: x[1]) if doc_types else ("None", 0)
            st.metric("Most Common Type", most_common_type[0])
            st.metric("Count", most_common_type[1])
    
    else:
        st.info("No documents available for analytics.")

def show_storage_analytics(auth_service, org_code):
    """Show detailed storage analytics"""
    subscription = auth_service.subscription_manager.get_organization_subscription(org_code)
    limits = auth_service.subscription_manager.get_plan_limits(subscription["plan"])
    
    st.subheader("💾 Storage Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    storage_used = subscription.get("storage_used_gb", 0)
    max_storage = limits.get("storage_gb", 0)
    
    with col1:
        st.metric("Storage Used", f"{storage_used:.2f} GB")
    
    with col2:
        st.metric("Storage Limit", f"{max_storage} GB")
    
    with col3:
        remaining = max_storage - storage_used
        st.metric("Remaining", f"{remaining:.2f} GB")
    
    # Storage usage over time (mock data)
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    usage_data = [min(i * 0.1 + storage_used, max_storage) for i in range(30)]
    
    fig = px.line(x=dates, y=usage_data, title="Storage Usage Over Time")
    fig.update_layout(xaxis_title="Date", yaxis_title="Storage Used (GB)")
    st.plotly_chart(fig, use_container_width=True)

def show_storage_report(auth_service, org_code):
    """Show detailed storage report"""
    st.subheader("📊 Storage Usage Report")
    
    subscription = auth_service.subscription_manager.get_organization_subscription(org_code)
    limits = auth_service.subscription_manager.get_plan_limits(subscription["plan"])
    
    # Current usage
    storage_used = subscription.get("storage_used_gb", 0)
    max_storage = limits.get("storage_gb", 0)
    
    st.write(f"**Current Plan:** {subscription['plan'].title()}")
    st.write(f"**Storage Used:** {storage_used:.2f} GB / {max_storage} GB")
    st.write(f"**Usage Percentage:** {(storage_used/max_storage*100):.1f}%")
    
    # Recommendations
    if storage_used / max_storage > 0.9:
        st.error("⚠️ Storage is 90% full! Consider:")
        st.write("• Delete old or unnecessary documents")
        st.write("• Archive completed matters")
        st.write("• Upgrade to a higher storage plan")
    elif storage_used / max_storage > 0.75:
        st.warning("Storage is 75% full. Plan ahead for additional storage needs.")

def show_document_settings():
    """Document management settings and preferences"""
    st.subheader("⚙️ Document Settings")
    
    # Get current user and organization
    user_data = st.session_state.get('user_data', {})
    org_code = user_data.get('organization_code')
    
    from services.subscription_manager import EnhancedAuthService
    auth_service = EnhancedAuthService()
    subscription = auth_service.subscription_manager.get_organization_subscription(org_code)
    
    # Document preferences
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Default Settings")
        
        default_doc_type = st.selectbox(
            "Default Document Type",
            ["Contract", "Legal Brief", "Correspondence", "Court Filing", "Research", "Template", "Invoice", "Other"],
            index=0
        )
        
        auto_extract_text = st.checkbox("Auto-extract text from uploaded documents", value=True)
        auto_tag_documents = st.checkbox("Enable automatic document tagging", value=True)
        
        # Notification preferences
        st.markdown("#### Notifications")
        notify_upload = st.checkbox("Notify on document upload", value=True)
        notify_share = st.checkbox("Notify when documents are shared", value=True)
        notify_expire = st.checkbox("Notify before document expiration", value=False)
    
    with col2:
        st.markdown("#### Security Settings")
        
        require_approval = st.checkbox("Require approval for document sharing", value=False)
        watermark_documents = st.checkbox("Add watermark to downloaded documents", value=False)
        
        # Retention settings
        st.markdown("#### Document Retention")
        auto_archive_days = st.number_input("Auto-archive documents after (days)", min_value=0, value=365)
        auto_delete_days = st.number_input("Auto-delete archived documents after (days)", min_value=0, value=0)
        
        if auto_delete_days > 0:
            st.warning("Auto-deletion is permanent and cannot be undone!")
    
    # Advanced settings for higher tier plans
    if auth_service.can_use_feature(org_code, "white_label"):
        st.markdown("#### White Label Customization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            company_logo = st.file_uploader("Upload Company Logo", type=['png', 'jpg', 'jpeg'])
            company_name = st.text_input("Company Name", value=user_data.get('organization_name', ''))
        
        with col2:
            primary_color = st.color_picker("Primary Color", "#2E86AB")
            secondary_color = st.color_picker("Secondary Color", "#A23B72")
        
        if st.button("Apply Branding"):
            st.success("Branding settings saved!")
    else:
        st.info("🎨 White label customization available with Professional plan or higher.")
        if st.button("Upgrade for White Label"):
            st.session_state['show_upgrade_modal'] = True
            st.rerun()
    
    # Storage management
    st.markdown("#### Storage Management")
    
    storage_used = subscription.get("storage_used_gb", 0)
    limits = auth_service.subscription_manager.get_plan_limits(subscription["plan"])
    max_storage = limits.get("storage_gb", 0)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Usage", f"{storage_used:.1f}GB")
    
    with col2:
        st.metric("Plan Limit", f"{max_storage}GB")
    
    with col3:
        remaining = max_storage - storage_used
        st.metric("Available", f"{remaining:.1f}GB")
    
    # Storage cleanup tools
    st.markdown("#### Cleanup Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧹 Clean Duplicate Files"):
            st.info("Scanning for duplicate documents...")
            # Mock duplicate detection
            st.success("No duplicate files found!")
    
    with col2:
        if st.button("📦 Archive Old Documents"):
            old_docs_count = len([d for d in st.session_state.documents 
                                if (datetime.now() - d.get('upload_date', datetime.now())).days > 365])
            if old_docs_count > 0:
                st.info(f"Found {old_docs_count} documents older than 1 year")
                if st.button("Archive These Documents"):
                    st.success(f"Archived {old_docs_count} old documents!")
            else:
                st.success("No old documents to archive")
    
    with col3:
        if st.button("🗑️ Delete Unused Files"):
            st.warning("This will permanently delete unused documents!")
            if st.button("Confirm Delete", type="primary"):
                st.success("Cleanup completed!")
    
    # Backup and export
    st.markdown("#### Backup & Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export All Documents"):
            st.info("Preparing document export...")
            st.success("Export will be sent to your email when ready!")
    
    with col2:
        if st.button("☁️ Backup to Cloud"):
            if auth_service.can_use_feature(org_code, "custom_integrations"):
                st.success("Backup initiated to cloud storage!")
            else:
                st.error("Cloud backup requires Professional plan or higher")
    
    # Save settings
    if st.button("💾 Save All Settings", type="primary"):
        # In a real app, these settings would be saved to database
        st.success("All document settings saved successfully!")
        
        # Mock settings save
        settings = {
            'default_doc_type': default_doc_type,
            'auto_extract_text': auto_extract_text,
            'auto_tag_documents': auto_tag_documents,
            'notify_upload': notify_upload,
            'notify_share': notify_share,
            'notify_expire': notify_expire,
            'require_approval': require_approval,
            'watermark_documents': watermark_documents,
            'auto_archive_days': auto_archive_days,
            'auto_delete_days': auto_delete_days
        }
        
        # Store in session state for persistence during session
        st.session_state['document_settings'] = settings

# Helper functions for document management

def get_file_icon(file_type):
    """Get appropriate icon for file type"""
    icons = {
        'pdf': '📄',
        'docx': '📝', 
        'txt': '📑',
        'xlsx': '📊',
        'pptx': '📋',
        'jpg': '🖼️',
        'jpeg': '🖼️',
        'png': '🖼️',
        'contract': '📋',
        'legal brief': '⚖️',
        'correspondence': '💌',
        'court filing': '🏛️',
        'research': '🔍',
        'template': '📄',
        'invoice': '💰',
        'other': '📁'
    }
    
    return icons.get(file_type.lower(), '📄')

def validate_file_upload(uploaded_file, max_size_mb=100):
    """Validate uploaded file"""
    if not uploaded_file:
        return False, "No file selected"
    
    file_size_mb = uploaded_file.size / (1024 * 1024)
    
    if file_size_mb > max_size_mb:
        return False, f"File size ({file_size_mb:.1f}MB) exceeds limit ({max_size_mb}MB)"
    
    allowed_types = ['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg', 'xlsx', 'pptx']
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension not in allowed_types:
        return False, f"File type '{file_extension}' not supported"
    
    return True, "File validation passed"

def generate_document_summary():
    """Generate summary statistics for documents"""
    docs = st.session_state.documents
    
    if not docs:
        return {
            'total_documents': 0,
            'total_size_mb': 0,
            'document_types': {},
            'privileged_count': 0,
            'recent_uploads': 0
        }
    
    # Calculate statistics
    total_docs = len(docs)
    doc_types = {}
    privileged_count = 0
    recent_uploads = 0
    total_size_mb = 0
    
    week_ago = datetime.now() - timedelta(days=7)
    
    for doc in docs:
        # Document type distribution
        doc_type = doc.get('type', 'Unknown')
        doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
        
        # Privileged documents
        if doc.get('is_privileged', False):
            privileged_count += 1
        
        # Recent uploads
        upload_date = doc.get('upload_date')
        if upload_date and upload_date >= week_ago:
            recent_uploads += 1
        
        # Total size calculation
        size_str = doc.get('size', '0 MB')
        try:
            size_mb = float(size_str.split()[0])
            total_size_mb += size_mb
        except:
            pass
    
    return {
        'total_documents': total_docs,
        'total_size_mb': total_size_mb,
        'document_types': doc_types,
        'privileged_count': privileged_count,
        'recent_uploads': recent_uploads
    }

# Main execution
if __name__ == "__main__":
    show()
