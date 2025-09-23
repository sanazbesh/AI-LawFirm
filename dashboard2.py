import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import time
import pyrebase
import uuid
import re
from typing import Dict, List, Optional, Tuple
import difflib
from dataclasses import dataclass, asdict
from enum import Enum
import base64
import io
from PIL import Image
import pytesseract  # For OCR
import fitz  # PyMuPDF for PDF processing
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Configure page
st.set_page_config(
    page_title="LegalDoc Pro - Advanced Document Management",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 5px solid;
    }
    .alert-warning {
        background-color: #fff3cd;
        border-color: #ffc107;
        color: #856404;
    }
    .alert-success {
        background-color: #d1e7dd;
        border-color: #198754;
        color: #0a3622;
    }
    .alert-danger {
        background-color: #f8d7da;
        border-color: #dc3545;
        color: #58151c;
    }
    .document-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #2E86AB;
    }
    .matter-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.8rem;
        border: 2px solid #dee2e6;
        margin: 1rem 0;
    }
    .version-badge {
        background-color: #6c757d;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
    }
    .status-active {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
    }
    .status-pending {
        background-color: #ffc107;
        color: #212529;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
    }
    .status-draft {
        background-color: #6c757d;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# Data Classes for better structure
@dataclass
class User:
    email: str
    role: str  # 'partner', 'associate', 'paralegal', 'client'
    permissions: List[str]
    created_date: datetime
    last_login: datetime

@dataclass
class Matter:
    id: str
    name: str
    client_name: str
    matter_type: str  # 'litigation', 'corporate', 'family', 'real_estate', etc.
    status: str  # 'active', 'closed', 'on_hold'
    created_date: datetime
    assigned_attorneys: List[str]
    description: str
    budget: float
    estimated_hours: float
    actual_hours: float
    important_dates: Dict[str, datetime]

@dataclass
class DocumentVersion:
    version_number: str
    created_date: datetime
    created_by: str
    file_content: bytes
    changes_summary: str
    file_size: int

@dataclass
class Document:
    id: str
    name: str
    matter_id: str
    client_name: str
    document_type: str
    current_version: str
    versions: List[DocumentVersion]
    status: str
    tags: List[str]
    extracted_text: str
    key_information: Dict
    created_date: datetime
    last_modified: datetime
    access_permissions: Dict[str, List[str]]  # role -> permissions
    retention_date: Optional[datetime]
    is_privileged: bool
    digital_signatures: List[Dict]

@dataclass
class AuditEntry:
    id: str
    timestamp: datetime
    user_email: str
    action: str
    resource_type: str
    resource_id: str
    details: Dict
    ip_address: str

class DocumentStatus(Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    FINAL = "final"
    ARCHIVED = "archived"

class MatterType(Enum):
    LITIGATION = "litigation"
    CORPORATE = "corporate"
    FAMILY = "family"
    REAL_ESTATE = "real_estate"
    EMPLOYMENT = "employment"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    CRIMINAL = "criminal"
    IMMIGRATION = "immigration"

# Firebase Configuration (same as before)
firebase_config = {
    "apiKey": "AIzaSyDt6y7YRFVF_zrMTYPn4z4ViHjLbmfMsLQ",
    "authDomain": "trend-summarizer-6f28e.firebaseapp.com",
    "projectId": "trend-summarizer-6f28e",
    "storageBucket": "trend-summarizer-6f28e.firebasestorage.app",
    "messagingSenderId": "655575726457",
    "databaseURL": "https://trend-summarizer-6f28e-default-rtdb.firebaseio.com",
    "appId": "1:655575726457:web:9ae1d0d363c804edc9d7a8",
    "measurementId": "G-HHY482GQKZ"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

# Initialize session state with enhanced data structures
def initialize_session_state():
    if 'enhanced_documents' not in st.session_state:
        st.session_state.enhanced_documents = []
    if 'matters' not in st.session_state:
        st.session_state.matters = []
    if 'clients' not in st.session_state:
        st.session_state.clients = []
    if 'time_entries' not in st.session_state:
        st.session_state.time_entries = []
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'audit_log' not in st.session_state:
        st.session_state.audit_log = []
    if 'search_index' not in st.session_state:
        st.session_state.search_index = {}
    if 'ai_insights' not in st.session_state:
        st.session_state.ai_insights = {}

# Advanced Document Processing Functions
class DocumentProcessor:
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF using PyMuPDF"""
        try:
            pdf_document = fitz.open(stream=file_content, filetype="pdf")
            text = ""
            for page in pdf_document:
                text += page.get_text()
            pdf_document.close()
            return text
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    @staticmethod
    def perform_ocr(image_content: bytes) -> str:
        """Perform OCR on image content"""
        try:
            image = Image.open(io.BytesIO(image_content))
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            st.error(f"Error performing OCR: {str(e)}")
            return ""
    
    @staticmethod
    def extract_key_information(text: str) -> Dict:
        """Extract key information from document text using regex patterns"""
        key_info = {}
        
        # Extract dates
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
        dates = re.findall(date_pattern, text, re.IGNORECASE)
        key_info['dates'] = list(set(dates))[:10]  # Limit to 10 dates
        
        # Extract dollar amounts
        money_pattern = r'\$[\d,]+(?:\.\d{2})?'
        amounts = re.findall(money_pattern, text)
        key_info['monetary_amounts'] = list(set(amounts))[:10]
        
        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        key_info['email_addresses'] = list(set(emails))
        
        # Extract phone numbers
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        key_info['phone_numbers'] = list(set(phones))
        
        # Extract potential party names (capitalized words, could be improved with NER)
        name_pattern = r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'
        potential_names = re.findall(name_pattern, text)
        key_info['potential_names'] = list(set(potential_names))[:10]
        
        return key_info
    
    @staticmethod
    def classify_document(filename: str, text: str) -> str:
        """Classify document based on filename and content"""
        filename_lower = filename.lower()
        text_lower = text.lower()
        
        # Contract/Agreement detection
        if any(word in filename_lower or word in text_lower[:1000] for word in 
               ['contract', 'agreement', 'terms', 'conditions']):
            return 'Contract/Agreement'
        
        # Court documents
        elif any(word in filename_lower or word in text_lower[:1000] for word in 
                ['motion', 'complaint', 'petition', 'brief', 'order', 'judgment']):
            return 'Court Filing'
        
        # Corporate documents
        elif any(word in filename_lower or word in text_lower[:1000] for word in 
                ['llc', 'corporation', 'incorporation', 'bylaws', 'board']):
            return 'Corporate Document'
        
        # Real estate
        elif any(word in filename_lower or word in text_lower[:1000] for word in 
                ['lease', 'deed', 'mortgage', 'property', 'real estate']):
            return 'Real Estate'
        
        # Family law
        elif any(word in filename_lower or word in text_lower[:1000] for word in 
                ['divorce', 'custody', 'prenuptial', 'marriage', 'child support']):
            return 'Family Law'
        
        else:
            return 'General Document'
    
    @staticmethod
    def generate_document_summary(text: str, max_length: int = 200) -> str:
        """Generate a summary of the document"""
        if len(text) <= max_length:
            return text
        
        # Simple extractive summarization - take first few sentences
        sentences = sent_tokenize(text)
        summary = ""
        for sentence in sentences:
            if len(summary + sentence) <= max_length:
                summary += sentence + " "
            else:
                break
        
        return summary.strip() or text[:max_length] + "..."

# Advanced Search Engine
class DocumentSearchEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.document_vectors = None
        self.documents = []
    
    def index_documents(self, documents: List[Document]):
        """Index documents for search"""
        self.documents = documents
        if not documents:
            return
        
        # Combine text content for indexing
        texts = []
        for doc in documents:
            content = f"{doc.name} {doc.document_type} {doc.client_name} {doc.extracted_text}"
            texts.append(content)
        
        try:
            self.document_vectors = self.vectorizer.fit_transform(texts)
        except Exception as e:
            st.error(f"Error indexing documents: {str(e)}")
    
    def search(self, query: str, top_k: int = 10) -> List[Tuple[Document, float]]:
        """Search documents and return results with similarity scores"""
        if not self.document_vectors or not query.strip():
            return []
        
        try:
            query_vector = self.vectorizer.transform([query])
            similarities = cosine_similarity(query_vector, self.document_vectors)[0]
            
            # Get top-k results
            top_indices = np.argsort(similarities)[::-1][:top_k]
            results = []
            
            for idx in top_indices:
                if similarities[idx] > 0:  # Only return relevant results
                    results.append((self.documents[idx], similarities[idx]))
            
            return results
        except Exception as e:
            st.error(f"Error searching documents: {str(e)}")
            return []

# Matter Management Functions
class MatterManager:
    @staticmethod
    def create_matter(name: str, client_name: str, matter_type: str, description: str) -> Matter:
        """Create a new matter"""
        matter = Matter(
            id=str(uuid.uuid4()),
            name=name,
            client_name=client_name,
            matter_type=matter_type,
            status='active',
            created_date=datetime.now(),
            assigned_attorneys=[],
            description=description,
            budget=0.0,
            estimated_hours=0.0,
            actual_hours=0.0,
            important_dates={}
        )
        return matter
    
    @staticmethod
    def get_matter_documents(matter_id: str, documents: List[Document]) -> List[Document]:
        """Get all documents for a specific matter"""
        return [doc for doc in documents if doc.matter_id == matter_id]
    
    @staticmethod
    def get_matter_stats(matter_id: str, documents: List[Document], time_entries: List[Dict]) -> Dict:
        """Get statistics for a matter"""
        matter_docs = MatterManager.get_matter_documents(matter_id, documents)
        matter_time = [entry for entry in time_entries if entry.get('matter_id') == matter_id]
        
        total_hours = sum(entry.get('hours', 0) for entry in matter_time)
        total_revenue = sum(entry.get('amount', 0) for entry in matter_time)
        
        return {
            'document_count': len(matter_docs),
            'total_hours': total_hours,
            'total_revenue': total_revenue,
            'last_activity': max([doc.last_modified for doc in matter_docs], default=datetime.min)
        }

# Version Control System
class VersionControl:
    @staticmethod
    def create_version(document: Document, file_content: bytes, changes_summary: str, user_email: str) -> DocumentVersion:
        """Create a new version of a document"""
        version_number = f"v{len(document.versions) + 1}.0"
        
        version = DocumentVersion(
            version_number=version_number,
            created_date=datetime.now(),
            created_by=user_email,
            file_content=file_content,
            changes_summary=changes_summary,
            file_size=len(file_content)
        )
        
        return version
    
    @staticmethod
    def compare_versions(version1: DocumentVersion, version2: DocumentVersion) -> List[str]:
        """Compare two document versions and return differences"""
        try:
            # This is a simplified comparison - in production, you'd use more sophisticated diff tools
            text1 = version1.file_content.decode('utf-8', errors='ignore')
            text2 = version2.file_content.decode('utf-8', errors='ignore')
            
            diff = list(difflib.unified_diff(
                text1.splitlines(keepends=True),
                text2.splitlines(keepends=True),
                fromfile=f"Version {version1.version_number}",
                tofile=f"Version {version2.version_number}",
                lineterm=""
            ))
            
            return diff[:100]  # Limit to first 100 lines of diff
        except Exception as e:
            return [f"Error comparing versions: {str(e)}"]

# Audit System
class AuditLogger:
    @staticmethod
    def log_action(user_email: str, action: str, resource_type: str, resource_id: str, details: Dict):
        """Log user actions for audit trail"""
        audit_entry = AuditEntry(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            user_email=user_email,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address="127.0.0.1"  # In production, get real IP
        )
        
        if 'audit_log' not in st.session_state:
            st.session_state.audit_log = []
        
        st.session_state.audit_log.append(audit_entry)

# Initialize enhanced session state
initialize_session_state()

# Load sample enhanced data
def load_sample_data():
    if not st.session_state.matters:
        # Sample matters
        matters = [
            MatterManager.create_matter("Smith Divorce", "John Smith", "family", "Contested divorce proceedings"),
            MatterManager.create_matter("TechCorp Formation", "TechCorp LLC", "corporate", "LLC formation and corporate documents"),
            MatterManager.create_matter("Johnson Custody", "Mary Johnson", "family", "Child custody modification"),
            MatterManager.create_matter("Williams Prenup", "Sarah Williams", "family", "Prenuptial agreement drafting"),
            MatterManager.create_matter("ABC Partnership", "ABC Partners", "corporate", "Partnership agreement and formation")
        ]
        st.session_state.matters = matters
    
    if not st.session_state.enhanced_documents:
        # Sample enhanced documents
        sample_docs = []
        
        for i, matter in enumerate(st.session_state.matters):
            doc_id = str(uuid.uuid4())
            sample_text = f"This is a sample {matter.matter_type} document for {matter.client_name}. " \
                         f"Important dates include January 15, 2024, and March 30, 2024. " \
                         f"Contact information: john@example.com, (555) 123-4567. " \
                         f"Total amount: $50,000.00"
            
            # Create initial version
            initial_version = DocumentVersion(
                version_number="v1.0",
                created_date=datetime.now() - timedelta(days=i),
                created_by="system@legaldoc.com",
                file_content=sample_text.encode(),
                changes_summary="Initial document creation",
                file_size=len(sample_text.encode())
            )
            
            doc = Document(
                id=doc_id,
                name=f"{matter.name}_Document_{i+1}.pdf",
                matter_id=matter.id,
                client_name=matter.client_name,
                document_type=DocumentProcessor.classify_document(f"document_{i}", sample_text),
                current_version="v1.0",
                versions=[initial_version],
                status=DocumentStatus.FINAL.value,
                tags=[matter.matter_type, "sample"],
                extracted_text=sample_text,
                key_information=DocumentProcessor.extract_key_information(sample_text),
                created_date=datetime.now() - timedelta(days=i),
                last_modified=datetime.now() - timedelta(days=i),
                access_permissions={"partner": ["read", "write", "delete"], "associate": ["read", "write"], "paralegal": ["read"]},
                retention_date=None,
                is_privileged=False,
                digital_signatures=[]
            )
            
            sample_docs.append(doc)
        
        st.session_state.enhanced_documents = sample_docs
        
        # Index documents for search
        search_engine = DocumentSearchEngine()
        search_engine.index_documents(sample_docs)
        st.session_state.search_engine = search_engine

# User Authentication (simplified - same as before but with role management)
def is_logged_in():
    return st.session_state.get('user') is not None

def get_user_role():
    """Get current user's role"""
    if not is_logged_in():
        return None
    return st.session_state.user.get('role', 'associate')  # Default to associate

def has_permission(permission: str) -> bool:
    """Check if current user has a specific permission"""
    role = get_user_role()
    if not role:
        return False
    
    role_permissions = {
        'partner': ['read', 'write', 'delete', 'admin', 'billing', 'manage_users'],
        'associate': ['read', 'write', 'time_tracking'],
        'paralegal': ['read', 'time_tracking'],
        'client': ['read']
    }
    
    return permission in role_permissions.get(role, [])

# Simplified login for demo (in production, integrate with your auth system)
def show_enhanced_login():
    st.markdown('<div class="main-header">⚖️ LegalDoc Pro - Advanced Legal Document Management</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        
        with st.form("demo_login"):
            role = st.selectbox("Select Role (Demo)", ["partner", "associate", "paralegal", "client"])
            email = st.text_input("Email", value=f"demo.{role}@legaldoc.com")
            password = st.text_input("Password", type="password", value="demo123")
            
            if st.form_submit_button("Login", use_container_width=True):
                st.session_state['user'] = {
                    'email': email,
                    'role': role,
                    'idToken': 'demo_token'
                }
                st.success(f"Logged in as {role}!")
                time.sleep(1)
                st.rerun()

# Check authentication
if not is_logged_in():
    show_enhanced_login()
    st.stop()

# Load sample data
load_sample_data()

# Enhanced Sidebar
st.sidebar.title("⚖️ LegalDoc Pro Advanced")
st.sidebar.markdown("*Enterprise Legal Document Management*")

user_role = get_user_role()
st.sidebar.markdown(f"**Role:** {user_role.title()}")
st.sidebar.markdown(f"**User:** {st.session_state['user']['email']}")

# Navigation based on user role
navigation_options = ["Dashboard", "Document Management", "Matter Management"]

if has_permission('time_tracking'):
    navigation_options.append("Time Tracking")
if has_permission('billing'):
    navigation_options.append("Billing & Reports")
if has_permission('admin'):
    navigation_options.extend(["User Management", "System Settings"])

navigation_options.extend(["Advanced Search", "Audit Trail"])

page = st.sidebar.selectbox("Navigate", navigation_options)

# Logout
if st.sidebar.button("🚪 Logout"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Main Content Area
if page == "Dashboard":
    st.title("📊 Executive Dashboard")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Total Matters", len(st.session_state.matters), "2 active")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Total Documents", len(st.session_state.enhanced_documents), "15 this week")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        pending_docs = len([d for d in st.session_state.enhanced_documents if d.status == 'under_review'])
        st.metric("Pending Reviews", pending_docs, "-2")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("This Week's Revenue", "$12,450", "+$2,100")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Recent Activity and Matter Overview
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📋 Recent Document Activity")
        recent_docs = sorted(st.session_state.enhanced_documents, 
                           key=lambda x: x.last_modified, reverse=True)[:5]
        
        for doc in recent_docs:
            with st.container():
                st.markdown(f"""
                <div class="document-card">
                    <strong>{doc.name}</strong><br>
                    <small>Matter: {next((m.name for m in st.session_state.matters if m.id == doc.matter_id), 'Unknown')}</small><br>
                    <small>Modified: {doc.last_modified.strftime('%Y-%m-%d %H:%M')}</small>
                    <span class="version-badge">{doc.current_version}</span>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("⚖️ Active Matters")
        for matter in st.session_state.matters[:5]:
            stats = MatterManager.get_matter_stats(matter.id, st.session_state.enhanced_documents, [])
            
            status_class = "status-active" if matter.status == "active" else "status-pending"
            
            st.markdown(f"""
            <div class="matter-card">
                <strong>{matter.name}</strong> <span class="{status_class}">{matter.status.upper()}</span><br>
                <small>Client: {matter.client_name}</small><br>
                <small>Type: {matter.matter_type.replace('_', ' ').title()}</small><br>
                <small>Documents: {stats['document_count']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # AI Insights Section (placeholder for future ML features)
    if has_permission('admin'):
        st.divider()
        st.subheader("🤖 AI Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="alert-box alert-warning">
                <strong>⚠️ Upcoming Deadlines:</strong><br>
                • Smith Divorce: Response due in 3 days<br>
                • TechCorp Formation: Filing deadline in 1 week
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="alert-box alert-success">
                <strong>✅ Document Insights:</strong><br>
                • 3 contracts ready for review<br>
                • Average processing time: 2.3 days
            </div>
            """, unsafe_allow_html=True)

elif page == "Advanced Search":
    st.title("🔍 Advanced Document Search")
    
    # Search interface
    search_query = st.text_input("🔍 Search documents", 
                                placeholder="Enter keywords, client names, dates, or document content...")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        matter_filter = st.selectbox("Filter by Matter", 
                                   ["All Matters"] + [m.name for m in st.session_state.matters])
    
    with col2:
        doc_type_filter = st.selectbox("Filter by Type", 
                                     ["All Types"] + list(set(d.document_type for d in st.session_state.enhanced_documents)))
    
    with col3:
        status_filter = st.selectbox("Filter by Status", 
                                   ["All Statuses"] + [status.value for status in DocumentStatus])
    
    # Advanced search options
    with st.expander("🔧 Advanced Search Options"):
        col1, col2 = st.columns(2)
        
        with col1:
            date_from = st.date_input("From Date", value=datetime.now() - timedelta(days=365))
            search_content = st.checkbox("Search document content", value=True)
            
        with col2:
            date_to = st.date_input("To Date", value=datetime.now())
            include_archived = st.checkbox("Include archived documents")
    
    # Perform search
    if search_query or matter_filter != "All Matters" or doc_type_filter != "All Types":
        filtered_docs = st.session_state.enhanced_documents
        
        # Apply filters
        if matter_filter != "All Matters":
            matter_id = next((m.id for m in st.session_state.matters if m.name == matter_filter), None)
            if matter_id:
                filtered_docs = [d for d in filtered_docs if d.matter_id == matter_id]
        
        if doc_type_filter != "All Types":
            filtered_docs = [d for d in filtered_docs if d.document_type == doc_type_filter]
        
        if status_filter != "All Statuses":
            filtered_docs = [d for d in filtered_docs if d.status == status_filter]
        
        # Date range filter
        filtered_docs = [d for d in filtered_docs if date_from <= d.created_date.date() <= date_to]
        
        # Text search using search engine
        if search_query and hasattr(st.session_state, 'search_engine'):
            search_results = st.session_state.search_engine.search(search_query, top_k=50)
            search_doc_ids = [doc.id for doc, score in search_results]
            filtered_docs = [d for d in filtered_docs if d.id in search_doc_ids]
        
        # Display results
        st.divider()
        st.subheader(f"🔍 Search Results ({len(filtered_docs)} documents)")
        
        for doc in filtered_docs:
            matter_name = next((m.name for m in st.session_state.matters if m.id == doc.matter_id), "Unknown Matter")
            
            with st.expander(f"📄 {doc.name} - {doc.document_type}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Matter:** {matter_name}")
                    st.markdown(f"**Client:** {doc.client_name}")
                    st.markdown(f"**Type:** {doc.document_type}")
                
                with col2:
                    st.markdown(f"**Status:** {doc.status.replace('_', ' ').title()}")
                    st.markdown(f"**Version:** {doc.current_version}")
                    st.markdown(f"**Created:** {doc.created_date.strftime('%Y-%m-%d')}")
                
                with col3:
                    st.markdown(f"**Modified:** {doc.last_modified.strftime('%Y-%m-%d %H:%M')}")
                    st.markdown(f"**Size:** {len(doc.versions[-1].file_content) if doc.versions else 0} bytes")
                    st.markdown(f"**Tags:** {', '.join(doc.tags)}")
                
                # Show key information extracted
                if doc.key_information:
                    st.markdown("**📊 Key Information:**")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if doc.key_information.get('dates'):
                            st.markdown(f"**Dates:** {', '.join(doc.key_information['dates'][:3])}")
                        if doc.key_information.get('monetary_amounts'):
                            st.markdown(f"**Amounts:** {', '.join(doc.key_information['monetary_amounts'][:3])}")
                    
                    with col2:
                        if doc.key_information.get('email_addresses'):
                            st.markdown(f"**Emails:** {', '.join(doc.key_information['email_addresses'][:2])}")
                        if doc.key_information.get('phone_numbers'):
                            st.markdown(f"**Phones:** {', '.join(doc.key_information['phone_numbers'][:2])}")
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("📖 View", key=f"view_search_{doc.id}"):
                        st.info("Document viewer would open here")
                
                with col2:
                    if has_permission('write') and st.button("📝 Edit", key=f"edit_search_{doc.id}"):
                        st.info("Document editor would open here")
                
                with col3:
                    if st.button("📊 Analyze", key=f"analyze_search_{doc.id}"):
                        st.info("AI analysis would show here")
                
                with col4:
                    if has_permission('delete') and st.button("🗑️ Delete", key=f"delete_search_{doc.id}"):
                        st.error("Delete confirmation would appear here")

elif page == "Document Management":
    st.title("📁 Advanced Document Management")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Documents", len(st.session_state.enhanced_documents))
    with col2:
        draft_count = len([d for d in st.session_state.enhanced_documents if d.status == 'draft'])
        st.metric("Draft Documents", draft_count)
    with col3:
        review_count = len([d for d in st.session_state.enhanced_documents if d.status == 'under_review'])
        st.metric("Under Review", review_count)
    with col4:
        final_count = len([d for d in st.session_state.enhanced_documents if d.status == 'final'])
        st.metric("Final Documents", final_count)
    
    st.divider()
    
    # Document upload section
    if has_permission('write'):
        st.subheader("📤 Upload New Document")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            uploaded_file = st.file_uploader("Choose file", type=['pdf', 'docx', 'txt', 'png', 'jpg'])
        
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
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🚀 Upload & Process Document"):
                    with st.spinner("Processing document..."):
                        # Read file content
                        file_content = uploaded_file.read()
                        
                        # Extract text based on file type
                        if uploaded_file.name.lower().endswith('.pdf'):
                            extracted_text = DocumentProcessor.extract_text_from_pdf(file_content)
                        elif uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                            extracted_text = DocumentProcessor.perform_ocr(file_content)
                        else:
                            extracted_text = file_content.decode('utf-8', errors='ignore')
                        
                        # Process document
                        doc_type = DocumentProcessor.classify_document(uploaded_file.name, extracted_text)
                        key_info = DocumentProcessor.extract_key_information(extracted_text)
                        
                        # Create initial version
                        initial_version = DocumentVersion(
                            version_number="v1.0",
                            created_date=datetime.now(),
                            created_by=st.session_state['user']['email'],
                            file_content=file_content,
                            changes_summary="Initial document upload",
                            file_size=len(file_content)
                        )
                        
                        # Create document
                        new_doc = Document(
                            id=str(uuid.uuid4()),
                            name=uploaded_file.name,
                            matter_id=matter_id,
                            client_name=next(m.client_name for m in st.session_state.matters if m.id == matter_id),
                            document_type=doc_type,
                            current_version="v1.0",
                            versions=[initial_version],
                            status=DocumentStatus.DRAFT.value,
                            tags=document_tags.split(',') if document_tags else [],
                            extracted_text=extracted_text,
                            key_information=key_info,
                            created_date=datetime.now(),
                            last_modified=datetime.now(),
                            access_permissions={"partner": ["read", "write", "delete"], "associate": ["read", "write"]},
                            retention_date=None,
                            is_privileged=is_privileged,
                            digital_signatures=[]
                        )
                        
                        st.session_state.enhanced_documents.append(new_doc)
                        
                        # Log the action
                        AuditLogger.log_action(
                            st.session_state['user']['email'],
                            "document_upload",
                            "document",
                            new_doc.id,
                            {"filename": uploaded_file.name, "matter_id": matter_id}
                        )
                        
                        # Update search index
                        if hasattr(st.session_state, 'search_engine'):
                            st.session_state.search_engine.index_documents(st.session_state.enhanced_documents)
                        
                        st.success(f"✅ Document '{uploaded_file.name}' uploaded and processed successfully!")
                        
                        # Show extracted information
                        st.subheader("🔍 Extracted Information")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Classified as:** {doc_type}")
                            st.markdown(f"**Text length:** {len(extracted_text)} characters")
                            if key_info.get('dates'):
                                st.markdown(f"**Dates found:** {', '.join(key_info['dates'][:3])}")
                        
                        with col2:
                            if key_info.get('monetary_amounts'):
                                st.markdown(f"**Amounts:** {', '.join(key_info['monetary_amounts'][:3])}")
                            if key_info.get('email_addresses'):
                                st.markdown(f"**Email addresses:** {', '.join(key_info['email_addresses'][:2])}")
                        
                        time.sleep(2)
                        st.rerun()
            
            with col2:
                st.info("💡 **AI Processing includes:**\n- Text extraction (OCR for images)\n- Document classification\n- Key information extraction\n- Automatic tagging suggestions")
    
    st.divider()
    
    # Document library with enhanced features
    st.subheader("📚 Document Library")
    
    # Filters and sorting
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        matter_filter = st.selectbox("Filter by Matter", 
                                   ["All"] + [m.name for m in st.session_state.matters])
    
    with col2:
        status_filter = st.selectbox("Filter by Status", 
                                   ["All"] + [status.value.replace('_', ' ').title() for status in DocumentStatus])
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Last Modified", "Created Date", "Name", "File Size"])
    
    with col4:
        sort_order = st.selectbox("Order", ["Descending", "Ascending"])
    
    # Apply filters
    filtered_docs = st.session_state.enhanced_documents
    
    if matter_filter != "All":
        matter_id = next((m.id for m in st.session_state.matters if m.name == matter_filter), None)
        if matter_id:
            filtered_docs = [d for d in filtered_docs if d.matter_id == matter_id]
    
    if status_filter != "All":
        status_value = status_filter.lower().replace(' ', '_')
        filtered_docs = [d for d in filtered_docs if d.status == status_value]
    
    # Sort documents
    sort_key_map = {
        "Last Modified": lambda x: x.last_modified,
        "Created Date": lambda x: x.created_date,
        "Name": lambda x: x.name,
        "File Size": lambda x: len(x.versions[-1].file_content) if x.versions else 0
    }
    
    reverse = sort_order == "Descending"
    filtered_docs = sorted(filtered_docs, key=sort_key_map[sort_by], reverse=reverse)
    
    # Display documents
    for doc in filtered_docs:
        matter_name = next((m.name for m in st.session_state.matters if m.id == doc.matter_id), "Unknown Matter")
        
        with st.expander(f"📄 {doc.name} - v{doc.current_version}"):
            # Document metadata
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Matter:** {matter_name}")
                st.markdown(f"**Client:** {doc.client_name}")
                st.markdown(f"**Type:** {doc.document_type}")
                st.markdown(f"**Status:** {doc.status.replace('_', ' ').title()}")
            
            with col2:
                st.markdown(f"**Created:** {doc.created_date.strftime('%Y-%m-%d %H:%M')}")
                st.markdown(f"**Modified:** {doc.last_modified.strftime('%Y-%m-%d %H:%M')}")
                st.markdown(f"**Versions:** {len(doc.versions)}")
                if doc.is_privileged:
                    st.markdown("**🔒 PRIVILEGED**")
            
            with col3:
                st.markdown(f"**Size:** {len(doc.versions[-1].file_content) if doc.versions else 0} bytes")
                st.markdown(f"**Tags:** {', '.join(doc.tags) if doc.tags else 'None'}")
                if doc.retention_date:
                    st.markdown(f"**Retention:** {doc.retention_date.strftime('%Y-%m-%d')}")
            
            # Version history
            if len(doc.versions) > 1:
                st.markdown("**📚 Version History:**")
                for version in reversed(doc.versions[-3:]):  # Show last 3 versions
                    st.markdown(f"• {version.version_number} - {version.created_date.strftime('%Y-%m-%d')} by {version.created_by}")
            
            # Key information extracted by AI
            if doc.key_information:
                st.markdown("**🤖 AI-Extracted Information:**")
                col1, col2 = st.columns(2)
                
                with col1:
                    if doc.key_information.get('dates'):
                        st.markdown(f"**📅 Important Dates:** {', '.join(doc.key_information['dates'][:3])}")
                    if doc.key_information.get('monetary_amounts'):
                        st.markdown(f"**💰 Amounts:** {', '.join(doc.key_information['monetary_amounts'][:3])}")
                
                with col2:
                    if doc.key_information.get('email_addresses'):
                        st.markdown(f"**📧 Contacts:** {', '.join(doc.key_information['email_addresses'][:2])}")
                    if doc.key_information.get('potential_names'):
                        st.markdown(f"**👤 Names:** {', '.join(doc.key_information['potential_names'][:3])}")
            
            # Document preview
            if doc.extracted_text:
                with st.expander("👁️ Document Preview"):
                    preview_text = doc.extracted_text[:500] + "..." if len(doc.extracted_text) > 500 else doc.extracted_text
                    st.text(preview_text)
            
            # Action buttons
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                if st.button("📖 View Full", key=f"view_full_{doc.id}"):
                    st.info("Full document viewer would open here with annotations, comments, and collaborative features.")
            
            with col2:
                if has_permission('write') and st.button("📝 Edit", key=f"edit_{doc.id}"):
                    st.info("Document editor would open here with version control and collaborative editing.")
            
            with col3:
                if st.button("🔄 Versions", key=f"versions_{doc.id}"):
                    st.info("Version comparison and management would open here.")
            
            with col4:
                if st.button("🤖 AI Analyze", key=f"ai_analyze_{doc.id}"):
                    with st.spinner("Analyzing document with AI..."):
                        time.sleep(1)
                        st.success("✅ AI Analysis Complete!")
                        st.markdown("**📊 AI Insights:**")
                        st.markdown("• Document type: Contract with standard commercial terms")
                        st.markdown("• Risk level: Low")
                        st.markdown("• Suggested actions: Review section 4.2 for compliance")
                        st.markdown("• Similar documents: 3 found in system")
            
            with col5:
                if has_permission('delete') and st.button("🗑️ Delete", key=f"delete_{doc.id}"):
                    if st.button("⚠️ Confirm Delete", key=f"confirm_delete_{doc.id}"):
                        # Log the deletion
                        AuditLogger.log_action(
                            st.session_state['user']['email'],
                            "document_delete",
                            "document",
                            doc.id,
                            {"filename": doc.name}
                        )
                        
                        # Remove document
                        st.session_state.enhanced_documents = [d for d in st.session_state.enhanced_documents if d.id != doc.id]
                        st.success("Document deleted successfully!")
                        st.rerun()

elif page == "Matter Management":
    st.title("⚖️ Matter Management")
    
    # Matter statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_matters = len([m for m in st.session_state.matters if m.status == 'active'])
        st.metric("Active Matters", active_matters)
    
    with col2:
        total_docs = len(st.session_state.enhanced_documents)
        st.metric("Total Documents", total_docs)
    
    with col3:
        # Calculate total revenue (placeholder)
        st.metric("Total Revenue", "$125,000")
    
    with col4:
        # Calculate average matter value
        st.metric("Avg. Matter Value", "$25,000")
    
    st.divider()
    
    # Create new matter
    if has_permission('write'):
        st.subheader("➕ Create New Matter")
        
        with st.form("new_matter_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                matter_name = st.text_input("Matter Name *")
                client_name = st.text_input("Client Name *")
                matter_type = st.selectbox("Matter Type", [mt.value.replace('_', ' ').title() for mt in MatterType])
            
            with col2:
                description = st.text_area("Description")
                estimated_budget = st.number_input("Estimated Budget ($)", min_value=0.0, step=1000.0)
                estimated_hours = st.number_input("Estimated Hours", min_value=0.0, step=10.0)
            
            if st.form_submit_button("Create Matter"):
                if matter_name and client_name:
                    new_matter = MatterManager.create_matter(
                        matter_name, client_name, matter_type.lower().replace(' ', '_'), description
                    )
                    new_matter.budget = estimated_budget
                    new_matter.estimated_hours = estimated_hours
                    
                    st.session_state.matters.append(new_matter)
                    
                    # Log the action
                    AuditLogger.log_action(
                        st.session_state['user']['email'],
                        "matter_create",
                        "matter",
                        new_matter.id,
                        {"matter_name": matter_name, "client_name": client_name}
                    )
                    
                    st.success(f"Matter '{matter_name}' created successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
        
        st.divider()
    
    # Matter list with enhanced details
    st.subheader("📋 Active Matters")
    
    for matter in st.session_state.matters:
        stats = MatterManager.get_matter_stats(matter.id, st.session_state.enhanced_documents, [])
        
        with st.expander(f"⚖️ {matter.name} - {matter.client_name}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Client:** {matter.client_name}")
                st.markdown(f"**Type:** {matter.matter_type.replace('_', ' ').title()}")
                st.markdown(f"**Status:** {matter.status.title()}")
                st.markdown(f"**Created:** {matter.created_date.strftime('%Y-%m-%d')}")
            
            with col2:
                st.markdown(f"**Documents:** {stats['document_count']}")
                st.markdown(f"**Budget:** ${matter.budget:,.2f}")
                st.markdown(f"**Est. Hours:** {matter.estimated_hours}")
                st.markdown(f"**Actual Hours:** {stats['total_hours']}")
            
            with col3:
                st.markdown(f"**Revenue:** ${stats['total_revenue']:,.2f}")
                if stats['last_activity'] != datetime.min:
                    st.markdown(f"**Last Activity:** {stats['last_activity'].strftime('%Y-%m-%d')}")
                else:
                    st.markdown("**Last Activity:** No activity")
            
            if matter.description:
                st.markdown(f"**Description:** {matter.description}")
            
            # Matter documents
            matter_docs = MatterManager.get_matter_documents(matter.id, st.session_state.enhanced_documents)
            if matter_docs:
                st.markdown("**📄 Recent Documents:**")
                for doc in matter_docs[-3:]:  # Show last 3 documents
                    status_badge = f"<span class='status-{doc.status.replace('_', '-')}'>{doc.status.replace('_', ' ').title()}</span>"
                    st.markdown(f"• {doc.name} - {doc.document_type} {status_badge}", unsafe_allow_html=True)
            
            # Matter timeline (placeholder)
            st.markdown("**📅 Important Dates:**")
            if matter.important_dates:
                for event, date in matter.important_dates.items():
                    st.markdown(f"• {event}: {date.strftime('%Y-%m-%d')}")
            else:
                st.markdown("• No important dates set")
            
            # Action buttons
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("📊 Analytics", key=f"analytics_{matter.id}"):
                    st.info("Matter analytics dashboard would open here with financial reports, time tracking, and performance metrics.")
            
            with col2:
                if has_permission('write') and st.button("📝 Edit", key=f"edit_matter_{matter.id}"):
                    st.info("Matter editing interface would open here.")
            
            with col3:
                if st.button("📋 Tasks", key=f"tasks_{matter.id}"):
                    st.info("Task management for this matter would open here.")
            
            with col4:
                if st.button("👥 Team", key=f"team_{matter.id}"):
                    st.info("Team assignment and collaboration tools would open here.")

elif page == "Audit Trail":
    st.title("🔍 System Audit Trail")
    
    if not has_permission('admin'):
        st.error("🚫 Access denied. Admin privileges required.")
        st.stop()
    
    # Audit log filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        user_filter = st.selectbox("Filter by User", ["All Users"] + list(set([entry.user_email for entry in st.session_state.audit_log])))
    
    with col2:
        action_filter = st.selectbox("Filter by Action", ["All Actions"] + list(set([entry.action for entry in st.session_state.audit_log])))
    
    with col3:
        date_filter = st.date_input("From Date", value=datetime.now() - timedelta(days=30))
    
    # Filter audit log
    filtered_log = st.session_state.audit_log
    
    if user_filter != "All Users":
        filtered_log = [entry for entry in filtered_log if entry.user_email == user_filter]
    
    if action_filter != "All Actions":
        filtered_log = [entry for entry in filtered_log if entry.action == action_filter]
    
    filtered_log = [entry for entry in filtered_log if entry.timestamp.date() >= date_filter]
    
    # Sort by timestamp (newest first)
    filtered_log = sorted(filtered_log, key=lambda x: x.timestamp, reverse=True)
    
    st.divider()
    st.subheader(f"📋 Audit Entries ({len(filtered_log)} records)")
    
    # Display audit entries
    for entry in filtered_log[:50]:  # Show first 50 entries
        with st.expander(f"{entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {entry.action} by {entry.user_email}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**User:** {entry.user_email}")
                st.markdown(f"**Action:** {entry.action}")
                st.markdown(f"**Resource Type:** {entry.resource_type}")
                st.markdown(f"**Resource ID:** {entry.resource_id}")
            
            with col2:
                st.markdown(f"**Timestamp:** {entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                st.markdown(f"**IP Address:** {entry.ip_address}")
                if entry.details:
                    st.markdown("**Details:**")
                    st.json(entry.details)

# Add error handling and performance monitoring
try:
    # Performance metrics (placeholder)
    if has_permission('admin'):
        with st.sidebar:
            st.divider()
            st.markdown("### 📊 System Health")
            st.metric("Response Time", "0.24s", "-0.05s")
            st.metric("Active Sessions", "12", "+3")
            st.metric("Storage Used", "2.1GB", "+156MB")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    if has_permission('admin'):
        st.exception(e)
