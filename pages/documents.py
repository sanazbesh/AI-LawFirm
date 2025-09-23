import streamlit as st
import uuid
import time
from datetime import datetime
from services.auth import AuthService
from services.document_processor import DocumentProcessor
from services.ai_analysis import AIAnalysisSystem
from models.document import Document, DocumentStatus

def show():
    auth_service = AuthService()
    document_processor = DocumentProcessor()
    ai_system = AIAnalysisSystem()
    
    st.title("Document Management")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Documents", len(st.session_state.documents))
    with col2:
        draft_count = len([d for d in st.session_state.documents if d.status == 'draft'])
        st.metric("Draft Documents", draft_count)
    with col3:
        review_count = len([d for d in st.session_state.documents if d.status == 'under_review'])
        st.metric("Under Review", review_count)
    with col4:
        final_count = len([d for d in st.session_state.documents if d.status == 'final'])
        st.metric("Final Documents", final_count)
    
    st.divider()
    
    # Upload section
    if auth_service.has_permission('write'):
        _show_upload_section(document_processor, auth_service)
    
    st.divider()
    
    # Document library
    _show_document_library(ai_system, auth_service)

def _show_upload_section(document_processor, auth_service):
    st.subheader("Upload New Document")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        uploaded_file = st.file_uploader("Choose file", type=['pdf', 'docx', 'txt'])
    
    with col2:
        if st.session_state.matters:
            selected_matter = st.selectbox("Select Matter", 
                                         [f"{m.name} - {m.client_name}" for m in st.session_state.matters])
            matter_id = st.session_state.matters[
                [f"{m.name} - {m.client_name}" for m in st.session_state.matters].index(selected_matter)
            ].id
        else:
            st.error("No matters available. Please create a matter first.")
            matter_id = None
    
    with col3:
        document_tags = st.text_input("Tags (comma-separated)", placeholder="contract, urgent, draft")
        is_privileged = st.checkbox("Attorney-Client Privileged")
    
    if uploaded_file and matter_id:
        if st.button("Upload Document"):
            with st.spinner("Processing document..."):
                file_content = uploaded_file.read()
                extracted_text = file_content.decode('utf-8', errors='ignore') if uploaded_file.name.endswith('.txt') else "Sample extracted text for demo"
                
                doc_type = document_processor.classify_document(uploaded_file.name, extracted_text)
                key_info = document_processor.extract_key_information(extracted_text)
                
                new_doc = Document(
                    id=str(uuid.uuid4()),
                    name=uploaded_file.name,
                    matter_id=matter_id,
                    client_name=next(m.client_name for m in st.session_state.matters if m.id == matter_id),
                    document_type=doc_type,
                    current_version="v1.0",
                    status=DocumentStatus.DRAFT.value,
                    tags=document_tags.split(',') if document_tags else [],
                    extracted_text=extracted_text,
                    key_information=key_info,
                    created_date=datetime.now(),
                    last_modified=datetime.now(),
                    is_privileged=is_privileged
                )
                
                st.session_state.documents.append(new_doc)
                st.success(f"Document '{uploaded_file.name}' uploaded successfully!")
                
                # Show extracted information
                _show_extracted_info(doc_type, key_info)
                
                time.sleep(2)
                st.rerun()

def _show_extracted_info(doc_type, key_info):
    st.subheader("Extracted Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Classified as:** {doc_type}")
        if key_info.get('dates'):
            st.markdown(f"**Dates found:** {', '.join(key_info['dates'][:3])}")
    
    with col2:
        if key_info.get('monetary_amounts'):
            st.markdown(f"**Amounts:** {', '.join(key_info['monetary_amounts'][:3])}")
        if key_info.get('email_addresses'):
            st.markdown(f"**Emails:** {', '.join(key_info['email_addresses'][:2])}")

def _show_document_library(ai_system, auth_service):
    st.subheader("Document Library")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        matter_filter = st.selectbox("Filter by Matter", ["All"] + [m.name for m in st.session_state.matters])
    
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All"] + [status.value.replace('_', ' ').title() for status in DocumentStatus])
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Last Modified", "Created Date", "Name"])
    
    # Apply filters
    filtered_docs = st.session_state.documents
    
    if matter_filter != "All":
        matter_id = next((m.id for m in st.session_state.matters if m.name == matter_filter), None)
        if matter_id:
            filtered_docs = [d for d in filtered_docs if d.matter_id == matter_id]
    
    if status_filter != "All":
        status_value = status_filter.lower().replace(' ', '_')
        filtered_docs = [d for d in filtered_docs if d.status == status_value]
    
    # Display documents
    for doc in filtered_docs:
        matter_name = next((m.name for m in st.session_state.matters if m.id == doc.matter_id), "Unknown Matter")
        
        with st.expander(f"{doc.name} - v{doc.current_version}"):
            _show_document_details(doc, matter_name, ai_system, auth_service)

def _show_document_details(doc, matter_name, ai_system, auth_service):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**Matter:** {matter_name}")
        st.markdown(f"**Client:** {doc.client_name}")
        st.markdown(f"**Type:** {doc.document_type}")
    
    with col2:
        st.markdown(f"**Status:** {doc.status.replace('_', ' ').title()}")
        st.markdown(f"**Created:** {doc.created_date.strftime('%Y-%m-%d')}")
        st.markdown(f"**Modified:** {doc.last_modified.strftime('%Y-%m-%d')}")
    
    with col3:
        st.markdown(f"**Tags:** {', '.join(doc.tags) if doc.tags else 'None'}")
        if doc.is_privileged:
            st.markdown("**PRIVILEGED**")
    
    # Key information
    if doc.key_information:
        st.markdown("**AI-Extracted Information:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if doc.key_information.get('dates'):
                st.markdown(f"**Dates:** {', '.join(doc.key_information['dates'][:3])}")
        
        with col2:
            if doc.key_information.get('monetary_amounts'):
                st.markdown(f"**Amounts:** {', '.join(doc.key_information['monetary_amounts'][:3])}")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("View", key=f"view_{doc.id}"):
            st.info("Document viewer would open here")
    
    with col2:
        if auth_service.has_permission('write') and st.button("Edit", key=f"edit_{doc.id}"):
            st.info("Document editor would open here")
    
    with col3:
        if st.button("AI Analyze", key=f"analyze_{doc.id}"):
            with st.spinner("Analyzing with AI..."):
                time.sleep(1)
                analysis = ai_system.analyze_contract(doc.extracted_text)
                st.success("AI Analysis Complete!")
                
                st.markdown("**Risk Level:** " + analysis['risk_level'].upper())
                st.markdown("**Complexity Score:** " + f"{analysis['complexity_score']:.1f}/100")
                
                if analysis['key_clauses']:
                    st.markdown("**Key Clauses:**")
                    for clause in analysis['key_clauses'][:3]:
                        st.markdown(f"• {clause['type'].title()}: {clause['text']}")
    
    with col4:
        if auth_service.has_permission('delete') and st.button("Delete", key=f"delete_{doc.id}"):
            st.session_state.documents = [d for d in st.session_state.documents if d.id != doc.id]
            st.success("Document deleted!")
            st.rerun()
