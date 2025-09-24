# main.py
import streamlit as st
from datetime import datetime
import uuid

# Import all required modules
from services.auth import AuthService
from services.document_processor import DocumentProcessor
from services.ai_analysis import AIAnalysisSystem
from models.document import Document, DocumentStatus
from models.matter import Matter

# Initialize session state
def initialize_session_state():
    if 'documents' not in st.session_state:
        st.session_state.documents = []
    
    if 'matters' not in st.session_state:
        # Sample matters for demo
        st.session_state.matters = [
            Matter(
                id=str(uuid.uuid4()),
                name="Contract Negotiation",
                client_name="TechCorp Inc",
                description="Software licensing agreement",
                created_date=datetime.now()
            ),
            Matter(
                id=str(uuid.uuid4()),
                name="Employment Dispute",
                client_name="StartupXYZ",
                description="Wrongful termination case",
                created_date=datetime.now()
            ),
            Matter(
                id=str(uuid.uuid4()),
                name="Merger & Acquisition",
                client_name="GlobalCorp",
                description="Asset purchase agreement",
                created_date=datetime.now()
            )
        ]

# models/document.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional

class DocumentStatus(Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    FINAL = "final"
    ARCHIVED = "archived"

@dataclass
class Document:
    id: str
    name: str
    matter_id: str
    client_name: str
    document_type: str
    current_version: str
    status: str
    tags: List[str]
    extracted_text: str
    key_information: Dict[str, Any]
    created_date: datetime
    last_modified: datetime
    is_privileged: bool = False
    file_size: Optional[int] = None
    file_path: Optional[str] = None

# models/matter.py
@dataclass
class Matter:
    id: str
    name: str
    client_name: str
    description: str
    created_date: datetime
    status: str = "active"

# services/auth.py
class AuthService:
    def __init__(self):
        # Mock user with full permissions for demo
        self.current_user = {
            'id': '1',
            'username': 'demo_user',
            'role': 'admin',
            'permissions': ['read', 'write', 'delete', 'admin']
        }
    
    def has_permission(self, permission: str) -> bool:
        return permission in self.current_user.get('permissions', [])
    
    def get_current_user(self):
        return self.current_user
    
    def is_authenticated(self) -> bool:
        return True

# services/document_processor.py
import re
from typing import Dict, List, Any

class DocumentProcessor:
    def __init__(self):
        self.document_types = {
            'contract': ['agreement', 'contract', 'terms', 'conditions'],
            'legal_brief': ['brief', 'motion', 'pleading', 'filing'],
            'correspondence': ['letter', 'email', 'memo', 'correspondence'],
            'financial': ['invoice', 'receipt', 'statement', 'financial'],
            'regulatory': ['compliance', 'regulatory', 'filing', 'report']
        }
    
    def classify_document(self, filename: str, content: str) -> str:
        """Classify document based on filename and content"""
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        scores = {}
        for doc_type, keywords in self.document_types.items():
            score = 0
            for keyword in keywords:
                if keyword in filename_lower:
                    score += 3
                if keyword in content_lower:
                    score += content_lower.count(keyword)
            scores[doc_type] = score
        
        return max(scores, key=scores.get) if scores else 'general'
    
    def extract_key_information(self, content: str) -> Dict[str, Any]:
        """Extract key information from document content"""
        key_info = {}
        
        # Extract dates
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',
            r'\b\d{1,2}-\d{1,2}-\d{4}\b',
            r'\b\w+ \d{1,2}, \d{4}\b'
        ]
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, content))
        key_info['dates'] = list(set(dates))[:5]
        
        # Extract monetary amounts
        money_pattern = r'\$[\d,]+\.?\d*'
        amounts = re.findall(money_pattern, content)
        key_info['monetary_amounts'] = list(set(amounts))[:5]
        
        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, content)
        key_info['email_addresses'] = list(set(emails))[:5]
        
        # Extract phone numbers
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, content)
        key_info['phone_numbers'] = list(set(phones))[:5]
        
        # Extract company names (simple heuristic)
        company_pattern = r'\b[A-Z][a-zA-Z\s]+(Inc|LLC|Corp|Corporation|Company|Ltd|Limited)\b'
        companies = re.findall(company_pattern, content)
        key_info['companies'] = list(set(companies))[:5]
        
        return key_info
    
    def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
        """Extract text content from uploaded file"""
        if filename.endswith('.txt'):
            return file_content.decode('utf-8', errors='ignore')
        elif filename.endswith('.pdf'):
            # In a real implementation, you'd use PyPDF2 or similar
            return "Sample PDF content extracted for demo purposes"
        elif filename.endswith('.docx'):
            # In a real implementation, you'd use python-docx
            return "Sample DOCX content extracted for demo purposes"
        else:
            return "Unsupported file type"

# services/ai_analysis.py
import random
from typing import Dict, List, Any

class AIAnalysisSystem:
    def __init__(self):
        self.risk_levels = ['low', 'medium', 'high']
        self.clause_types = ['termination', 'payment', 'liability', 'confidentiality', 'intellectual_property']
    
    def analyze_contract(self, content: str) -> Dict[str, Any]:
        """Simulate AI contract analysis"""
        analysis = {
            'risk_level': random.choice(self.risk_levels),
            'complexity_score': random.uniform(20, 95),
            'key_clauses': self._extract_key_clauses(content),
            'recommendations': self._generate_recommendations(),
            'compliance_issues': self._check_compliance(),
            'summary': self._generate_summary(content)
        }
        return analysis
    
    def _extract_key_clauses(self, content: str) -> List[Dict[str, str]]:
        """Extract and classify key clauses"""
        clauses = []
        for i in range(random.randint(3, 7)):
            clause_type = random.choice(self.clause_types)
            clauses.append({
                'type': clause_type,
                'text': f"Sample {clause_type} clause extracted from document",
                'confidence': random.uniform(0.7, 0.95)
            })
        return clauses
    
    def _generate_recommendations(self) -> List[str]:
        """Generate AI recommendations"""
        recommendations = [
            "Consider adding force majeure clause",
            "Review payment terms for clarity",
            "Ensure compliance with local regulations",
            "Add dispute resolution mechanism",
            "Clarify intellectual property rights"
        ]
        return random.sample(recommendations, k=random.randint(2, 4))
    
    def _check_compliance(self) -> List[Dict[str, str]]:
        """Check compliance issues"""
        issues = [
            {"type": "GDPR", "status": "compliant", "notes": "Data processing clauses are adequate"},
            {"type": "CCPA", "status": "needs_review", "notes": "Consumer rights section requires update"},
            {"type": "SOX", "status": "compliant", "notes": "Financial reporting requirements met"}
        ]
        return random.sample(issues, k=random.randint(1, 3))
    
    def _generate_summary(self, content: str) -> str:
        """Generate document summary"""
        return f"This document contains approximately {len(content.split())} words and appears to be a legal document with standard commercial terms."

# Document Management UI (Enhanced)
import streamlit as st
import uuid
import time
from datetime import datetime

def show():
    # Initialize session state
    initialize_session_state()
    
    auth_service = AuthService()
    document_processor = DocumentProcessor()
    ai_system = AIAnalysisSystem()
    
    st.title("🏛️ Legal Document Management System")
    st.markdown("---")
    
    # Quick stats dashboard
    _show_dashboard_stats()
    
    st.divider()
    
    # Upload section
    if auth_service.has_permission('write'):
        _show_upload_section(document_processor, auth_service)
    else:
        st.warning("You don't have permission to upload documents.")
    
    st.divider()
    
    # Document library
    _show_document_library(ai_system, auth_service)

def _show_dashboard_stats():
    """Enhanced dashboard with more statistics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_docs = len(st.session_state.documents)
        st.metric("📄 Total Documents", total_docs, delta=None)
    
    with col2:
        draft_count = len([d for d in st.session_state.documents if (d.status if hasattr(d, 'status') else d.get('status', '')) == 'draft'])
        st.metric("✏️ Draft Documents", draft_count)
    
    with col3:
        review_count = len([d for d in st.session_state.documents if d.status == 'under_review'])
        st.metric("🔍 Under Review", review_count)
    
    with col4:
        final_count = len([d for d in st.session_state.documents if d.status == 'final'])
        st.metric("✅ Final Documents", final_count)
    
    # Additional stats row
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        privileged_count = len([d for d in st.session_state.documents if getattr(d, 'is_privileged', False)])
        st.metric("🔒 Privileged Docs", privileged_count)
    
    with col6:
        matters_count = len(st.session_state.matters)
        st.metric("📋 Active Matters", matters_count)
    
    with col7:
        contract_count = len([d for d in st.session_state.documents if d.document_type == 'contract'])
        st.metric("📝 Contracts", contract_count)
    
    with col8:
        # Calculate documents created this week (mock)
        this_week = len([d for d in st.session_state.documents if 
                        (datetime.now() - d.created_date).days <= 7])
        st.metric("📅 This Week", this_week)

def _show_upload_section(document_processor, auth_service):
    st.subheader("📤 Upload New Document")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose file", 
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, DOCX, TXT"
        )
    
    with col2:
        if st.session_state.matters:
            matter_options = [f"{m.name} - {m.client_name}" for m in st.session_state.matters]
            selected_matter = st.selectbox("Select Matter", matter_options)
            matter_id = st.session_state.matters[matter_options.index(selected_matter)].id
        else:
            st.error("No matters available. Please create a matter first.")
            matter_id = None
    
    # Additional metadata
    col3, col4 = st.columns(2)
    
    with col3:
        document_tags = st.text_input(
            "Tags (comma-separated)", 
            placeholder="contract, urgent, draft, confidential"
        )
        is_privileged = st.checkbox("🔒 Attorney-Client Privileged", value=False)
    
    with col4:
        document_status = st.selectbox(
            "Initial Status",
            [status.value.replace('_', ' ').title() for status in DocumentStatus],
            index=0
        )
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    
    if uploaded_file and matter_id:
        if st.button("🚀 Upload Document", type="primary"):
            with st.spinner("Processing document..."):
                # Read file content
                file_content = uploaded_file.read()
                extracted_text = document_processor.extract_text_from_file(file_content, uploaded_file.name)
                
                # Process document
                doc_type = document_processor.classify_document(uploaded_file.name, extracted_text)
                key_info = document_processor.extract_key_information(extracted_text)
                
                # Create new document
                new_doc = Document(
                    id=str(uuid.uuid4()),
                    name=uploaded_file.name,
                    matter_id=matter_id,
                    client_name=next(m.client_name for m in st.session_state.matters if m.id == matter_id),
                    document_type=doc_type,
                    current_version="v1.0",
                    status=document_status.lower().replace(' ', '_'),
                    tags=[tag.strip() for tag in document_tags.split(',') if tag.strip()] + [priority.lower()],
                    extracted_text=extracted_text,
                    key_information=key_info,
                    created_date=datetime.now(),
                    last_modified=datetime.now(),
                    is_privileged=is_privileged,
                    file_size=len(file_content)
                )
                
                st.session_state.documents.append(new_doc)
                st.success(f"✅ Document '{uploaded_file.name}' uploaded successfully!")
                
                # Show extracted information
                _show_extracted_info(doc_type, key_info)
                
                time.sleep(1)
                st.rerun()

def _show_extracted_info(doc_type, key_info):
    st.subheader("🔍 AI-Extracted Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**Document Type:** {doc_type.title()}")
        if key_info.get('dates'):
            with st.expander("📅 Important Dates"):
                for date in key_info['dates'][:5]:
                    st.write(f"• {date}")
    
    with col2:
        if key_info.get('monetary_amounts'):
            with st.expander("💰 Monetary Amounts"):
                for amount in key_info['monetary_amounts'][:5]:
                    st.write(f"• {amount}")
        
        if key_info.get('companies'):
            with st.expander("🏢 Companies"):
                for company in key_info['companies'][:3]:
                    st.write(f"• {company}")
    
    with col3:
        if key_info.get('email_addresses'):
            with st.expander("📧 Email Addresses"):
                for email in key_info['email_addresses'][:3]:
                    st.write(f"• {email}")
        
        if key_info.get('phone_numbers'):
            with st.expander("📞 Phone Numbers"):
                for phone in key_info['phone_numbers'][:3]:
                    st.write(f"• {phone}")

def _show_document_library(ai_system, auth_service):
    st.subheader("📚 Document Library")
    
    # Enhanced filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        matter_filter = st.selectbox("Filter by Matter", ["All"] + [m.name for m in st.session_state.matters])
    
    with col2:
        status_filter = st.selectbox("Filter by Status", 
                                   ["All"] + [status.value.replace('_', ' ').title() for status in DocumentStatus])
    
    with col3:
        type_filter = st.selectbox("Filter by Type", 
                                 ["All", "Contract", "Legal Brief", "Correspondence", "Financial", "Regulatory"])
    
    with col4:
        sort_by = st.selectbox("Sort by", ["Last Modified", "Created Date", "Name", "File Size"])
    
    # Search functionality
    search_term = st.text_input("🔍 Search documents", placeholder="Search by name, content, or tags...")
    
    # Apply filters
    filtered_docs = _apply_filters(st.session_state.documents, matter_filter, status_filter, 
                                 type_filter, search_term)
    
    # Sort documents
    filtered_docs = _sort_documents(filtered_docs, sort_by)
    
    if not filtered_docs:
        st.info("No documents found matching your filters.")
        return
    
    st.markdown(f"**Showing {len(filtered_docs)} documents**")
    
    # Display documents in a more organized way
    for i, doc in enumerate(filtered_docs):
        matter_name = next((m.name for m in st.session_state.matters if m.id == doc.matter_id), "Unknown Matter")
        
        with st.expander(f"{doc.name} - v{doc.current_version} ({'🔒 PRIVILEGED' if doc.is_privileged else ''})"):
            _show_document_details(doc, matter_name, ai_system, auth_service)

def _apply_filters(documents, matter_filter, status_filter, type_filter, search_term):
    """Apply various filters to the document list"""
    filtered = documents.copy()
    
    # Matter filter
    if matter_filter != "All":
        matter_id = next((m.id for m in st.session_state.matters if m.name == matter_filter), None)
        if matter_id:
            filtered = [d for d in filtered if d.matter_id == matter_id]
    
    # Status filter
    if status_filter != "All":
        status_value = status_filter.lower().replace(' ', '_')
        filtered = [d for d in filtered if d.status == status_value]
    
    # Type filter
    if type_filter != "All":
        type_value = type_filter.lower().replace(' ', '_')
        filtered = [d for d in filtered if d.document_type == type_value]
    
    # Search filter
    if search_term:
        search_lower = search_term.lower()
        filtered = [d for d in filtered if 
                   search_lower in d.name.lower() or
                   search_lower in d.extracted_text.lower() or
                   any(search_lower in tag.lower() for tag in d.tags)]
    
    return filtered

def _sort_documents(documents, sort_by):
    """Sort documents based on selected criteria"""
    if sort_by == "Last Modified":
        return sorted(documents, key=lambda x: x.last_modified, reverse=True)
    elif sort_by == "Created Date":
        return sorted(documents, key=lambda x: x.created_date, reverse=True)
    elif sort_by == "Name":
        return sorted(documents, key=lambda x: x.name.lower())
    elif sort_by == "File Size":
        return sorted(documents, key=lambda x: x.file_size or 0, reverse=True)
    else:
        return documents

def _show_document_details(doc, matter_name, ai_system, auth_service):
    # Document metadata
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**⚖️ Matter:** {matter_name}")
        st.markdown(f"**👤 Client:** {doc.client_name}")
        st.markdown(f"**📋 Type:** {doc.document_type.title()}")
        if doc.file_size:
            st.markdown(f"**📊 Size:** {doc.file_size:,} bytes")
    
    with col2:
        status_emoji = {"draft": "✏️", "under_review": "🔍", "final": "✅", "archived": "📦"}
        st.markdown(f"**Status:** {status_emoji.get(doc.status, '📄')} {doc.status.replace('_', ' ').title()}")
        st.markdown(f"**📅 Created:** {doc.created_date.strftime('%Y-%m-%d %H:%M')}")
        st.markdown(f"**📝 Modified:** {doc.last_modified.strftime('%Y-%m-%d %H:%M')}")
    
    with col3:
        if doc.tags:
            st.markdown(f"**🏷️ Tags:** {', '.join(doc.tags)}")
        if doc.is_privileged:
            st.markdown("**🔒 ATTORNEY-CLIENT PRIVILEGED**")
    
    # Key information in an organized layout
    if doc.key_information:
        st.markdown("**🤖 AI-Extracted Information:**")
        
        info_tabs = st.tabs(["📅 Dates", "💰 Financial", "👥 Contacts", "🏢 Entities"])
        
        with info_tabs[0]:
            if doc.key_information.get('dates'):
                for date in doc.key_information['dates'][:5]:
                    st.write(f"• {date}")
        
        with info_tabs[1]:
            if doc.key_information.get('monetary_amounts'):
                for amount in doc.key_information['monetary_amounts'][:5]:
                    st.write(f"• {amount}")
        
        with info_tabs[2]:
            if doc.key_information.get('email_addresses'):
                st.write("**Emails:**")
                for email in doc.key_information['email_addresses'][:3]:
                    st.write(f"• {email}")
            if doc.key_information.get('phone_numbers'):
                st.write("**Phones:**")
                for phone in doc.key_information['phone_numbers'][:3]:
                    st.write(f"• {phone}")
        
        with info_tabs[3]:
            if doc.key_information.get('companies'):
                for company in doc.key_information['companies'][:5]:
                    st.write(f"• {company}")
    
    # Action buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("👁️ View", key=f"view_{doc.id}", help="View document content"):
            _show_document_viewer(doc)
    
    with col2:
        if auth_service.has_permission('write'):
            if st.button("✏️ Edit", key=f"edit_{doc.id}", help="Edit document"):
                _show_document_editor(doc)
    
    with col3:
        if st.button("🤖 AI Analyze", key=f"analyze_{doc.id}", help="Run AI analysis"):
            _run_ai_analysis(doc, ai_system)
    
    with col4:
        if st.button("📊 Report", key=f"report_{doc.id}", help="Generate report"):
            _generate_document_report(doc)
    
    with col5:
        if auth_service.has_permission('delete'):
            if st.button("🗑️ Delete", key=f"delete_{doc.id}", type="secondary", help="Delete document"):
                _delete_document(doc.id)

def _show_document_viewer(doc):
    """Display document content in a viewer"""
    st.subheader(f"📄 Document Viewer: {doc.name}")
    
    # Show first 1000 characters of content
    content_preview = doc.extracted_text[:1000]
    if len(doc.extracted_text) > 1000:
        content_preview += "..."
    
    st.text_area("Document Content", content_preview, height=300, disabled=True)
    
    if len(doc.extracted_text) > 1000:
        st.info(f"Showing first 1000 characters of {len(doc.extracted_text)} total characters.")

def _show_document_editor(doc):
    """Simple document editor interface"""
    st.subheader(f"✏️ Edit Document: {doc.name}")
    st.info("Document editing interface would be implemented here with version control.")

def _run_ai_analysis(doc, ai_system):
    """Run and display AI analysis results"""
    with st.spinner("🤖 Running AI analysis..."):
        time.sleep(2)  # Simulate processing time
        analysis = ai_system.analyze_contract(doc.extracted_text)
        
        st.success("✅ AI Analysis Complete!")
        
        # Display analysis results in tabs
        analysis_tabs = st.tabs(["📊 Overview", "⚠️ Risk Analysis", "📋 Key Clauses", "💡 Recommendations"])
        
        with analysis_tabs[0]:
            col1, col2 = st.columns(2)
            with col1:
                risk_colors = {"low": "🟢", "medium": "🟡", "high": "🔴"}
                st.markdown(f"**Risk Level:** {risk_colors.get(analysis['risk_level'], '⚪')} {analysis['risk_level'].upper()}")
                st.markdown(f"**Complexity Score:** {analysis['complexity_score']:.1f}/100")
            
            with col2:
                st.markdown(f"**Summary:** {analysis['summary']}")
        
        with analysis_tabs[1]:
            for issue in analysis['compliance_issues']:
                status_emoji = {"compliant": "✅", "needs_review": "⚠️", "non_compliant": "❌"}
                st.markdown(f"{status_emoji.get(issue['status'], '❓')} **{issue['type']}**: {issue['notes']}")
        
        with analysis_tabs[2]:
            for clause in analysis['key_clauses'][:5]:
                with st.expander(f"{clause['type'].replace('_', ' ').title()} Clause"):
                    st.write(clause['text'])
                    st.write(f"Confidence: {clause['confidence']:.1%}")
        
        with analysis_tabs[3]:
            for rec in analysis['recommendations']:
                st.markdown(f"• {rec}")

def _generate_document_report(doc):
    """Generate a comprehensive document report"""
    st.subheader(f"📊 Document Report: {doc.name}")
    
    report_data = {
        "Document Name": doc.name,
        "Document Type": doc.document_type.title(),
        "Client": doc.client_name,
        "Status": doc.status.replace('_', ' ').title(),
        "Created": doc.created_date.strftime('%Y-%m-%d %H:%M'),
        "Last Modified": doc.last_modified.strftime('%Y-%m-%d %H:%M'),
        "Word Count": len(doc.extracted_text.split()) if doc.extracted_text else 0,
        "Character Count": len(doc.extracted_text) if doc.extracted_text else 0,
        "Is Privileged": "Yes" if doc.is_privileged else "No",
        "Tags": ", ".join(doc.tags) if doc.tags else "None"
    }
    
    for key, value in report_data.items():
        st.write(f"**{key}:** {value}")

def _delete_document(doc_id):
    """Delete a document with confirmation"""
    if st.button("⚠️ Confirm Delete", key=f"confirm_delete_{doc_id}", type="secondary"):
        st.session_state.documents = [d for d in st.session_state.documents if d.id != doc_id]
        st.success("🗑️ Document deleted successfully!")
        time.sleep(1)
        st.rerun()

# Additional utility functions for enhanced functionality

def export_documents_csv():
    """Export document metadata to CSV"""
    import pandas as pd
    import io
    
    if not st.session_state.documents:
        st.warning("No documents to export.")
        return
    
    # Prepare data for export
    export_data = []
    for doc in st.session_state.documents:
        matter_name = next((m.name for m in st.session_state.matters if m.id == doc.matter_id), "Unknown")
        export_data.append({
            'Document Name': doc.name,
            'Matter': matter_name,
            'Client': doc.client_name,
            'Type': doc.document_type,
            'Status': doc.status,
            'Version': doc.current_version,
            'Created Date': doc.created_date.strftime('%Y-%m-%d'),
            'Last Modified': doc.last_modified.strftime('%Y-%m-%d'),
            'Tags': ', '.join(doc.tags),
            'Is Privileged': 'Yes' if doc.is_privileged else 'No',
            'Word Count': len(doc.extracted_text.split()) if doc.extracted_text else 0
        })
    
    df = pd.DataFrame(export_data)
    
    # Convert to CSV
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    
    st.download_button(
        label="📥 Download Document Report (CSV)",
        data=buffer.getvalue(),
        file_name=f"document_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

def show_analytics_dashboard():
    """Show analytics dashboard with charts"""
    st.subheader("📈 Document Analytics")
    
    if not st.session_state.documents:
        st.info("No documents available for analytics.")
        return
    
    # Document type distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Document Types Distribution**")
        type_counts = {}
        for doc in st.session_state.documents:
            doc_type = doc.document_type.title()
            type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
        
        for doc_type, count in type_counts.items():
            st.write(f"• {doc_type}: {count}")
    
    with col2:
        st.markdown("**📈 Documents by Status**")
        status_counts = {}
        for doc in st.session_state.documents:
            status = doc.status.replace('_', ' ').title()
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in status_counts.items():
            st.write(f"• {status}: {count}")
    
    # Timeline analysis
    st.markdown("**📅 Document Creation Timeline (Last 30 Days)**")
    recent_docs = [d for d in st.session_state.documents 
                   if (datetime.now() - d.created_date).days <= 30]
    
    if recent_docs:
        st.write(f"Created {len(recent_docs)} documents in the last 30 days")
        
        # Group by date
        date_counts = {}
        for doc in recent_docs:
            date_str = doc.created_date.strftime('%Y-%m-%d')
            date_counts[date_str] = date_counts.get(date_str, 0) + 1
        
        sorted_dates = sorted(date_counts.items())
        for date, count in sorted_dates[-10:]:  # Show last 10 days with activity
            st.write(f"• {date}: {count} document(s)")
    else:
        st.write("No documents created in the last 30 days")

def show_bulk_operations():
    """Show bulk operations interface"""
    st.subheader("🔄 Bulk Operations")
    
    if not st.session_state.documents:
        st.info("No documents available for bulk operations.")
        return
    
    # Bulk status update
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📝 Bulk Status Update**")
        selected_docs = st.multiselect(
            "Select Documents",
            options=[(doc.id, doc.name) for doc in st.session_state.documents],
            format_func=lambda x: x[1]
        )
        
        if selected_docs:
            new_status = st.selectbox(
                "New Status",
                [status.value.replace('_', ' ').title() for status in DocumentStatus]
            )
            
            if st.button("🔄 Update Status", key="bulk_status"):
                status_value = new_status.lower().replace(' ', '_')
                updated_count = 0
                for doc in st.session_state.documents:
                    if any(doc.id == doc_id for doc_id, _ in selected_docs):
                        doc.status = status_value
                        doc.last_modified = datetime.now()
                        updated_count += 1
                
                st.success(f"Updated status for {updated_count} documents!")
                time.sleep(1)
                st.rerun()
    
    with col2:
        st.markdown("**🏷️ Bulk Tag Addition**")
        tag_selected_docs = st.multiselect(
            "Select Documents for Tagging",
            options=[(doc.id, doc.name) for doc in st.session_state.documents],
            format_func=lambda x: x[1],
            key="tag_multiselect"
        )
        
        if tag_selected_docs:
            new_tags = st.text_input(
                "Add Tags (comma-separated)",
                placeholder="urgent, reviewed, important"
            )
            
            if st.button("🏷️ Add Tags", key="bulk_tags") and new_tags:
                tags_to_add = [tag.strip() for tag in new_tags.split(',') if tag.strip()]
                updated_count = 0
                
                for doc in st.session_state.documents:
                    if any(doc.id == doc_id for doc_id, _ in tag_selected_docs):
                        # Add new tags without duplicates
                        existing_tags = set(doc.tags)
                        for tag in tags_to_add:
                            if tag not in existing_tags:
                                doc.tags.append(tag)
                        doc.last_modified = datetime.now()
                        updated_count += 1
                
                st.success(f"Added tags to {updated_count} documents!")
                time.sleep(1)
                st.rerun()

def show_document_comparison():
    """Show document comparison interface"""
    st.subheader("🔍 Document Comparison")
    
    if len(st.session_state.documents) < 2:
        st.info("Need at least 2 documents for comparison.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        doc1 = st.selectbox(
            "Select First Document",
            options=st.session_state.documents,
            format_func=lambda x: f"{x.name} ({x.document_type})",
            key="compare_doc1"
        )
    
    with col2:
        doc2 = st.selectbox(
            "Select Second Document",
            options=[d for d in st.session_state.documents if d.id != doc1.id],
            format_func=lambda x: f"{x.name} ({x.document_type})",
            key="compare_doc2"
        )
    
    if doc1 and doc2:
        if st.button("🔍 Compare Documents"):
            st.markdown("**📊 Comparison Results**")
            
            # Basic comparison
            comparison_data = [
                ["Document Name", doc1.name, doc2.name],
                ["Document Type", doc1.document_type, doc2.document_type],
                ["Client", doc1.client_name, doc2.client_name],
                ["Status", doc1.status, doc2.status],
                ["Word Count", len(doc1.extracted_text.split()), len(doc2.extracted_text.split())],
                ["Character Count", len(doc1.extracted_text), len(doc2.extracted_text)],
                ["Tags", ', '.join(doc1.tags), ', '.join(doc2.tags)],
                ["Created Date", doc1.created_date.strftime('%Y-%m-%d'), doc2.created_date.strftime('%Y-%m-%d')],
                ["Is Privileged", "Yes" if doc1.is_privileged else "No", "Yes" if doc2.is_privileged else "No"]
            ]
            
            # Display comparison table
            for row in comparison_data:
                col1, col2, col3 = st.columns([2, 3, 3])
                with col1:
                    st.write(f"**{row[0]}**")
                with col2:
                    st.write(row[1])
                with col3:
                    st.write(row[2])
            
            # Content similarity (basic)
            st.markdown("**📝 Content Analysis**")
            doc1_words = set(doc1.extracted_text.lower().split())
            doc2_words = set(doc2.extracted_text.lower().split())
            common_words = doc1_words.intersection(doc2_words)
            
            if doc1_words and doc2_words:
                similarity = len(common_words) / len(doc1_words.union(doc2_words)) * 100
                st.write(f"Content Similarity: {similarity:.1f}%")
                st.write(f"Common Words: {len(common_words)}")

# Enhanced main application with additional features
def show_enhanced():
    """Enhanced main application with additional features"""
    # Initialize session state
    initialize_session_state()
    
    auth_service = AuthService()
    document_processor = DocumentProcessor()
    ai_system = AIAnalysisSystem()
    
    # Sidebar for navigation
    with st.sidebar:
        st.title("🏛️ Legal DMS")
        
        page = st.radio(
            "Navigate to:",
            ["📄 Documents", "📈 Analytics", "🔄 Bulk Ops", "🔍 Compare", "⚙️ Settings"]
        )
        
        st.divider()
        
        # Quick actions
        st.markdown("**Quick Actions:**")
        export_documents_csv()
        
        st.divider()
        
        # User info
        user = auth_service.get_current_user()
        st.markdown(f"**User:** {user['username']}")
        st.markdown(f"**Role:** {user['role'].title()}")
    
    # Main content based on selected page
    if page == "📄 Documents":
        st.title("🏛️ Legal Document Management System")
        st.markdown("---")
        
        # Quick stats dashboard
        _show_dashboard_stats()
        st.divider()
        
        # Upload section
        if auth_service.has_permission('write'):
            _show_upload_section(document_processor, auth_service)
        else:
            st.warning("You don't have permission to upload documents.")
        
        st.divider()
        
        # Document library
        _show_document_library(ai_system, auth_service)
    
    elif page == "📈 Analytics":
        show_analytics_dashboard()
    
    elif page == "🔄 Bulk Ops":
        show_bulk_operations()
    
    elif page == "🔍 Compare":
        show_document_comparison()
    
    elif page == "⚙️ Settings":
        st.subheader("⚙️ System Settings")
        st.info("Settings interface would be implemented here.")
        
        # Sample settings
        st.checkbox("Enable automatic document classification", value=True)
        st.checkbox("Require approval for document deletion", value=True)
        st.selectbox("Default document status", ["Draft", "Under Review", "Final"])
        st.slider("AI analysis confidence threshold", 0.5, 1.0, 0.8)

# Main application entry point
if __name__ == "__main__":
    st.set_page_config(
        page_title="Legal Document Management",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Choose between basic and enhanced version
    enhanced_mode = st.query_params.get("enhanced", "false").lower() == "true"
    
    if enhanced_mode:
        show_enhanced()
    else:
        show()
