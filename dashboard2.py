import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import time
import uuid
import re
from typing import Dict, List, Optional, Tuple, Union
import difflib
from dataclasses import dataclass, asdict
from enum import Enum
import base64
import io
import numpy as np
import tempfile

# Configure Streamlit
st.set_page_config(
    page_title="LegalDoc Pro - Enterprise Legal Management",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #2E86AB;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .document-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border-left: 4px solid #2E86AB;
        transition: all 0.3s ease;
    }
    
    .document-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .matter-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #dee2e6;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .status-badge {
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-active { background-color: #28a745; color: white; }
    .status-pending { background-color: #ffc107; color: #212529; }
    .status-draft { background-color: #6c757d; color: white; }
    .status-review { background-color: #17a2b8; color: white; }
    .status-final { background-color: #28a745; color: white; }
    
    .ai-insight {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 1px solid #2196f3;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .client-portal {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        border: 1px solid #9c27b0;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .integration-card {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .integration-card:hover {
        border-color: #2E86AB;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .mobile-frame {
        width: 300px;
        height: 600px;
        background: #000;
        border-radius: 25px;
        padding: 20px;
        margin: 0 auto;
        position: relative;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .mobile-screen {
        width: 100%;
        height: 100%;
        background: white;
        border-radius: 20px;
        overflow: hidden;
        position: relative;
    }
</style>
""", unsafe_allow_html=True)

# Data Classes
@dataclass
class User:
    id: str
    email: str
    role: str
    created_date: datetime
    last_login: datetime

@dataclass
class Client:
    id: str
    name: str
    client_type: str
    contact_info: Dict
    created_date: datetime
    status: str
    portal_access: bool

@dataclass
class Matter:
    id: str
    name: str
    client_id: str
    client_name: str
    matter_type: str
    status: str
    created_date: datetime
    assigned_attorneys: List[str]
    description: str
    budget: float
    estimated_hours: float
    actual_hours: float

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
    key_information: Dict
    created_date: datetime
    last_modified: datetime
    is_privileged: bool

@dataclass
class TimeEntry:
    id: str
    user_id: str
    matter_id: str
    client_id: str
    date: datetime
    hours: float
    description: str
    billing_rate: float
    billable: bool
    activity_type: str
    status: str
    created_date: datetime

@dataclass
class Invoice:
    id: str
    client_id: str
    matter_id: str
    invoice_number: str
    date_issued: datetime
    due_date: datetime
    line_items: List[Dict]
    subtotal: float
    tax_rate: float
    tax_amount: float
    total_amount: float
    status: str

# Enums
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

# Initialize Session State
def initialize_session_state():
    defaults = {
        'documents': [],
        'matters': [],
        'clients': [],
        'time_entries': [],
        'invoices': [],
        'calendar_events': [],
        'ai_insights': [],
        'integrations': [],
        'user': None,
        'audit_log': [],
        'search_index': {},
        'mobile_session': {},
        'system_settings': {}
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# Document Processing Functions
class DocumentProcessor:
    @staticmethod
    def extract_key_information(text: str) -> Dict:
        key_info = {}
        
        # Extract dates
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
        dates = re.findall(date_pattern, text, re.IGNORECASE)
        key_info['dates'] = list(set(dates))[:10]
        
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
        
        return key_info
    
    @staticmethod
    def classify_document(filename: str, text: str) -> str:
        filename_lower = filename.lower()
        text_lower = text.lower()
        
        if any(word in filename_lower or word in text_lower[:1000] for word in 
               ['contract', 'agreement', 'terms', 'conditions']):
            return 'Contract/Agreement'
        elif any(word in filename_lower or word in text_lower[:1000] for word in 
                ['motion', 'complaint', 'petition', 'brief', 'order', 'judgment']):
            return 'Court Filing'
        elif any(word in filename_lower or word in text_lower[:1000] for word in 
                ['llc', 'corporation', 'incorporation', 'bylaws', 'board']):
            return 'Corporate Document'
        elif any(word in filename_lower or word in text_lower[:1000] for word in 
                ['lease', 'deed', 'mortgage', 'property', 'real estate']):
            return 'Real Estate'
        elif any(word in filename_lower or word in text_lower[:1000] for word in 
                ['divorce', 'custody', 'prenuptial', 'marriage', 'child support']):
            return 'Family Law'
        else:
            return 'General Document'

# AI Analysis System
class AIAnalysisSystem:
    def __init__(self):
        pass
    
    def analyze_contract(self, document_text: str) -> Dict:
        analysis = {
            'risk_level': self._assess_risk_level(document_text),
            'key_clauses': self._identify_key_clauses(document_text),
            'missing_clauses': self._identify_missing_clauses(document_text),
            'recommendations': self._generate_recommendations(),
            'complexity_score': self._calculate_complexity(document_text)
        }
        return analysis
    
    def _assess_risk_level(self, text: str) -> str:
        risk_keywords = ['penalty', 'termination', 'breach', 'litigation', 'damages']
        text_lower = text.lower()
        high_count = sum(1 for word in risk_keywords if word in text_lower)
        
        if high_count >= 3:
            return 'high'
        elif high_count >= 1:
            return 'medium'
        else:
            return 'low'
    
    def _identify_key_clauses(self, text: str) -> List[Dict]:
        clause_patterns = {
            'termination': r'(?:termination|terminate|end|cancel)[^.]*\.',
            'payment': r'(?:payment|pay|fee|cost|price)[^.]*\.',
            'liability': r'(?:liability|liable|responsible)[^.]*\.'
        }
        
        clauses = []
        for clause_type, pattern in clause_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches[:2]:
                clauses.append({
                    'type': clause_type,
                    'text': match.strip()[:100] + "...",
                    'importance': 'high' if clause_type in ['termination', 'liability'] else 'medium'
                })
        
        return clauses
    
    def _identify_missing_clauses(self, text: str) -> List[str]:
        standard_clauses = [
            'Force Majeure', 'Governing Law', 'Dispute Resolution',
            'Indemnification', 'Limitation of Liability', 'Confidentiality'
        ]
        
        text_lower = text.lower()
        missing = []
        
        for clause in standard_clauses:
            if clause.lower().replace(' ', '') not in text_lower.replace(' ', ''):
                missing.append(clause)
        
        return missing
    
    def _generate_recommendations(self) -> List[str]:
        return [
            "Consider adding explicit termination procedures",
            "Review payment terms for clarity",
            "Add force majeure clause for risk mitigation"
        ]
    
    def _calculate_complexity(self, text: str) -> float:
        words = text.split()
        sentences = text.split('.')
        
        avg_words_per_sentence = len(words) / len(sentences) if sentences else 0
        long_words = sum(1 for word in words if len(word) > 6)
        complexity = (avg_words_per_sentence * 0.4) + (long_words / len(words) * 100 * 0.6)
        
        return min(complexity, 100.0)

# Business Intelligence
class BusinessIntelligence:
    def __init__(self):
        pass
    
    def generate_executive_dashboard(self) -> Dict:
        total_matters = len(st.session_state.matters)
        active_matters = len([m for m in st.session_state.matters if m.status == 'active'])
        total_docs = len(st.session_state.documents)
        total_revenue = sum(inv.total_amount for inv in st.session_state.invoices if inv.status == 'paid')
        
        return {
            'total_matters': total_matters,
            'active_matters': active_matters,
            'total_documents': total_docs,
            'total_revenue': total_revenue,
            'revenue_growth': 8.5,
            'avg_matter_value': total_revenue / total_matters if total_matters > 0 else 0,
            'utilization_rate': 78.5,
            'client_satisfaction': 4.2
        }
    
    def create_revenue_chart(self) -> go.Figure:
        months = pd.date_range(start='2024-01-01', periods=12, freq='M')
        revenue_data = [15000, 18000, 22000, 19000, 25000, 28000, 24000, 30000, 27000, 32000, 29000, 35000]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=revenue_data,
            mode='lines+markers',
            name='Monthly Revenue',
            line=dict(color='#2E86AB', width=3)
        ))
        
        fig.update_layout(
            title='Monthly Revenue Trend',
            xaxis_title='Month',
            yaxis_title='Revenue ($)',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def create_matter_type_distribution(self) -> go.Figure:
        matter_types = {}
        for matter in st.session_state.matters:
            matter_type = matter.matter_type.replace('_', ' ').title()
            matter_types[matter_type] = matter_types.get(matter_type, 0) + 1
        
        if not matter_types:
            matter_types = {'Corporate': 5, 'Litigation': 3, 'Family': 4, 'Real Estate': 2}
        
        fig = go.Figure(data=[go.Pie(
            labels=list(matter_types.keys()),
            values=list(matter_types.values()),
            hole=.3,
            marker_colors=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
        )])
        
        fig.update_layout(title='Matter Distribution by Type', height=400)
        return fig

# Client Portal
class ClientPortal:
    def __init__(self):
        pass
    
    def authenticate_client(self, email: str, password: str) -> Optional[Dict]:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        for client in st.session_state.clients:
            if (hasattr(client, 'portal_credentials') and 
                client.portal_credentials.get('email') == email and
                client.portal_credentials.get('password') == hashed_password):
                return {'token': str(uuid.uuid4()), 'client': client}
        
        return None
    
    def get_client_documents(self, client_id: str) -> List:
        return [doc for doc in st.session_state.documents 
                if hasattr(doc, 'client_id') and doc.client_id == client_id]

# Mobile App Framework
class MobileAppFramework:
    def render_mobile_interface(self):
        st.markdown("""
        <div class="mobile-frame">
            <div class="mobile-screen">
                <div style="background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%); color: white; padding: 1rem; text-align: center;">
                    <h3>📱 LegalDoc Mobile</h3>
                </div>
                <div style="padding: 1rem;">
                    <div style="margin: 0.5rem 0; padding: 0.8rem; background: #f8f9fa; border-radius: 8px;">
                        📄 Recent Documents (3)
                    </div>
                    <div style="margin: 0.5rem 0; padding: 0.8rem; background: #f8f9fa; border-radius: 8px;">
                        📅 Today's Schedule (2)
                    </div>
                    <div style="margin: 0.5rem 0; padding: 0.8rem; background: #f8f9fa; border-radius: 8px;">
                        📧 New Messages (5)
                    </div>
                    <div style="margin: 0.5rem 0; padding: 0.8rem; background: #f8f9fa; border-radius: 8px;">
                        ⏱️ Time Tracking
                    </div>
                    <div style="margin: 0.5rem 0; padding: 0.8rem; background: #f8f9fa; border-radius: 8px;">
                        📸 Scan Document
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Integration Manager
class IntegrationManager:
    def __init__(self):
        self.available_integrations = {
            'docusign': {'name': 'DocuSign', 'type': 'esignature', 'status': 'available'},
            'outlook': {'name': 'Microsoft Outlook', 'type': 'email', 'status': 'available'},
            'google_calendar': {'name': 'Google Calendar', 'type': 'calendar', 'status': 'available'},
            'quickbooks': {'name': 'QuickBooks', 'type': 'accounting', 'status': 'available'},
            'zoom': {'name': 'Zoom', 'type': 'video_conference', 'status': 'available'},
            'slack': {'name': 'Slack', 'type': 'communication', 'status': 'available'}
        }
    
    def setup_integration(self, integration_id: str, config: Dict) -> bool:
        if integration_id in self.available_integrations:
            return True
        return False

# Initialize systems
initialize_session_state()
document_processor = DocumentProcessor()
ai_system = AIAnalysisSystem()
business_intelligence = BusinessIntelligence()
client_portal = ClientPortal()
mobile_framework = MobileAppFramework()
integration_manager = IntegrationManager()

# Load sample data
def load_sample_data():
    if not st.session_state.clients:
        sample_clients = [
            Client(
                id="client_1",
                name="Acme Corporation",
                client_type="business",
                contact_info={"phone": "(555) 123-4567", "email": "legal@acme.com"},
                created_date=datetime.now() - timedelta(days=365),
                status="active",
                portal_access=True
            ),
            Client(
                id="client_2",
                name="Sarah Johnson",
                client_type="individual",
                contact_info={"phone": "(555) 987-6543", "email": "sarah@email.com"},
                created_date=datetime.now() - timedelta(days=180),
                status="active",
                portal_access=True
            )
        ]
        st.session_state.clients = sample_clients
    
    if not st.session_state.matters:
        sample_matters = [
            Matter(
                id="matter_1",
                name="Acme Corp M&A Transaction",
                client_id="client_1",
                client_name="Acme Corporation",
                matter_type="corporate",
                status="active",
                created_date=datetime.now() - timedelta(days=45),
                assigned_attorneys=["partner@firm.com"],
                description="Merger and acquisition transaction",
                budget=150000.0,
                estimated_hours=300,
                actual_hours=125.5
            ),
            Matter(
                id="matter_2",
                name="Johnson Custody Modification",
                client_id="client_2",
                client_name="Sarah Johnson",
                matter_type="family",
                status="active",
                created_date=datetime.now() - timedelta(days=30),
                assigned_attorneys=["family@firm.com"],
                description="Child custody modification",
                budget=15000.0,
                estimated_hours=40,
                actual_hours=18.0
            )
        ]
        st.session_state.matters = sample_matters
    
    if not st.session_state.documents:
        sample_docs = []
        for i, matter in enumerate(st.session_state.matters):
            sample_text = f"This is a sample {matter.matter_type} document for {matter.client_name}. Important dates include January 15, 2024. Contact: john@example.com, (555) 123-4567. Amount: $50,000."
            
            doc = Document(
                id=str(uuid.uuid4()),
                name=f"{matter.name}_Document_{i+1}.pdf",
                matter_id=matter.id,
                client_name=matter.client_name,
                document_type=document_processor.classify_document(f"document_{i}", sample_text),
                current_version="v1.0",
                status=DocumentStatus.FINAL.value,
                tags=[matter.matter_type, "sample"],
                extracted_text=sample_text,
                key_information=document_processor.extract_key_information(sample_text),
                created_date=datetime.now() - timedelta(days=i),
                last_modified=datetime.now() - timedelta(days=i),
                is_privileged=False
            )
            sample_docs.append(doc)
        
        st.session_state.documents = sample_docs
    
    if not st.session_state.invoices:
        sample_invoices = [
            Invoice(
                id="inv_1",
                client_id="client_1",
                matter_id="matter_1",
                invoice_number="INV-20241201-0001",
                date_issued=datetime.now() - timedelta(days=30),
                due_date=datetime.now(),
                line_items=[
                    {"description": "Document review", "hours": 8.0, "rate": 450.0, "amount": 3600.0}
                ],
                subtotal=3600.0,
                tax_rate=0.08,
                tax_amount=288.0,
                total_amount=3888.0,
                status="paid"
            )
        ]
        st.session_state.invoices = sample_invoices

load_sample_data()

# Authentication functions
def is_logged_in():
    return st.session_state.get('user') is not None

def get_user_role():
    if not is_logged_in():
        return None
    return st.session_state.user.get('role', 'associate')

def has_permission(permission: str) -> bool:
    role = get_user_role()
    if not role:
        return False
    
    role_permissions = {
        'partner': ['read', 'write', 'delete', 'admin', 'billing', 'manage_users', 'ai_insights', 'integrations'],
        'associate': ['read', 'write', 'time_tracking', 'ai_insights'],
        'paralegal': ['read', 'time_tracking'],
        'client': ['read', 'portal_access']
    }
    
    return permission in role_permissions.get(role, [])

# Login system
def show_login():
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ LegalDoc Pro Enterprise</h1>
        <p>Complete Legal Practice Management Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Staff Login", "👥 Client Portal"])
        
        with tab1:
            st.markdown("### Staff Login")
            with st.form("staff_login"):
                role = st.selectbox("Role", ["partner", "associate", "paralegal", "admin"])
                email = st.text_input("Email", value=f"demo.{role}@legaldocpro.com")
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
        
        with tab2:
            st.markdown("### Client Portal Access")
            with st.form("client_login"):
                client_email = st.text_input("Client Email", value="legal@acme.com")
                client_password = st.text_input("Password", type="password", value="demo123")
                
                if st.form_submit_button("Access Portal", use_container_width=True):
                    # Simplified client auth
                    st.session_state['user'] = {
                        'email': client_email,
                        'role': 'client',
                        'client_id': 'client_1',
                        'token': 'client_token'
                    }
                    st.success("Welcome to your client portal!")
                    time.sleep(1)
                    st.rerun()

# Check authentication
if not is_logged_in():
    show_login()
    st.stop()

# Sidebar
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%); color: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
    <h3 style="margin: 0; text-align: center;">⚖️ LegalDoc Pro</h3>
    <p style="margin: 0.5rem 0 0 0; text-align: center;">Enterprise Platform</p>
</div>
""", unsafe_allow_html=True)

user_role = get_user_role()
user_email = st.session_state['user']['email']

st.sidebar.markdown(f"**👤 Role:** {user_role.title()}")
st.sidebar.markdown(f"**📧 User:** {user_email}")

# Navigation based on role
if user_role == 'client':
    navigation_options = ["Client Dashboard", "My Documents", "Billing", "Messages"]
else:
    navigation_options = ["Executive Dashboard", "Document Management", "Matter Management", "Calendar & Tasks"]
    
    if has_permission('time_tracking'):
        navigation_options.append("Time & Billing")
    if has_permission('ai_insights'):
        navigation_options.append("AI Insights")
    if has_permission('integrations'):
        navigation_options.append("Integrations")
    if has_permission('admin'):
        navigation_options.extend(["Business Intelligence", "System Settings"])
    
    navigation_options.extend(["Advanced Search", "Mobile App"])

page = st.sidebar.selectbox("🧭 Navigate", navigation_options)

if st.sidebar.button("🚪 Logout"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Main Content
if page == "Executive Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Executive Dashboard</h1>
        <p>Strategic Overview & Key Performance Indicators</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate metrics
    exec_metrics = business_intelligence.generate_executive_dashboard()
    
    # KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics_data = [
        ("Total Revenue", f"${exec_metrics['total_revenue']:,.0f}", f"{exec_metrics['revenue_growth']:+.1f}%"),
        ("Active Matters", exec_metrics['active_matters'], "+2"),
        ("Documents", exec_metrics['total_documents'], "+15"),
        ("Avg Matter Value", f"${exec_metrics['avg_matter_value']:,.0f}", "+12%"),
        ("Utilization", f"{exec_metrics['utilization_rate']:.1f}%", "+3.2%")
    ]
    
    for col, (label, value, change) in zip([col1, col2, col3, col4, col5], metrics_data):
        with col:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(label, value, change)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(business_intelligence.create_revenue_chart(), use_container_width=True)
    
    with col2:
        st.plotly_chart(business_intelligence.create_matter_type_distribution(), use_container_width=True)
    
    # Recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recent Document Activity")
        recent_docs = sorted(st.session_state.documents, key=lambda x: x.last_modified, reverse=True)[:5]
        
        for doc in recent_docs:
            st.markdown(f"""
            <div class="document-card">
            st.markdown(f"""
            <div class="client-portal">
                <strong>{doc.name}</strong><br>
                <small>Updated: {doc.last_modified.strftime('%Y-%m-%d')}</small><br>
                <small>Status: {doc.status.replace('_', ' ').title()}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Upcoming Events")
        events = [
            "Board meeting - Jan 25, 2025",
            "Document review - Jan 30, 2025",
            "Closing preparation - Feb 5, 2025"
        ]
        
        for event in events:
            st.markdown(f"""
            <div class="client-portal">
                {event}
            </div>
            """, unsafe_allow_html=True)

elif page == "Time & Billing":
    st.title("Time Tracking & Billing")
    
    if not has_permission('time_tracking'):
        st.error("Access denied. Time tracking access required.")
        st.stop()
    
    # Billing metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Unbilled Hours", "45.5")
    
    with col2:
        st.metric("Unbilled Amount", "$11,375")
    
    with col3:
        st.metric("Outstanding Invoices", "3")
    
    with col4:
        st.metric("Collection Rate", "94.2%")
    
    st.divider()
    
    # Time entry tabs
    tab1, tab2, tab3 = st.tabs(["Time Entry", "Billing", "Reports"])
    
    with tab1:
        st.subheader("Time Entry")
        
        with st.form("time_entry"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                entry_matter = st.selectbox("Matter", [f"{m.name}" for m in st.session_state.matters])
                entry_hours = st.number_input("Hours", min_value=0.0, max_value=24.0, value=1.0, step=0.25)
            
            with col2:
                entry_date = st.date_input("Date", value=datetime.now().date())
                entry_rate = st.number_input("Rate ($)", min_value=0.0, value=250.0, step=25.0)
            
            with col3:
                entry_activity = st.selectbox("Activity", ["Legal Research", "Document Review", "Client Meeting", "Court Appearance"])
                billable = st.checkbox("Billable", value=True)
            
            entry_description = st.text_area("Description", placeholder="Describe work performed...")
            
            if st.form_submit_button("Add Time Entry"):
                if entry_matter and entry_description:
                    new_entry = TimeEntry(
                        id=str(uuid.uuid4()),
                        user_id=st.session_state['user']['email'],
                        matter_id="demo_matter",
                        client_id="demo_client",
                        date=datetime.combine(entry_date, datetime.now().time()),
                        hours=entry_hours,
                        description=entry_description,
                        billing_rate=entry_rate,
                        billable=billable,
                        activity_type=entry_activity,
                        status="draft",
                        created_date=datetime.now()
                    )
                    
                    st.session_state.time_entries.append(new_entry)
                    st.success("Time entry added!")
                    st.rerun()
        
        st.divider()
        
        # Recent entries
        st.subheader("Recent Time Entries")
        
        for entry in st.session_state.time_entries[-5:]:
            amount = entry.hours * entry.billing_rate
            st.markdown(f"""
            <div class="document-card">
                <strong>{entry.activity_type}</strong> - {entry.hours} hours<br>
                <small>{entry.description[:80]}...</small><br>
                <small>Rate: ${entry.billing_rate}/hr | Amount: ${amount:.2f}</small>
                <span class="status-badge status-{entry.status}">{entry.status.upper()}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Invoice Generation")
        
        with st.form("generate_invoice"):
            col1, col2 = st.columns(2)
            
            with col1:
                invoice_client = st.selectbox("Client", [c.name for c in st.session_state.clients])
                billing_start = st.date_input("Period Start", value=datetime.now().replace(day=1).date())
            
            with col2:
                invoice_matter = st.selectbox("Matter", [m.name for m in st.session_state.matters])
                billing_end = st.date_input("Period End", value=datetime.now().date())
            
            if st.form_submit_button("Generate Invoice"):
                new_invoice = Invoice(
                    id=str(uuid.uuid4()),
                    client_id="client_1",
                    matter_id="matter_1",
                    invoice_number=f"INV-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.invoices) + 1:04d}",
                    date_issued=datetime.now(),
                    due_date=datetime.now() + timedelta(days=30),
                    line_items=[{"description": "Legal services", "amount": 5000.0}],
                    subtotal=5000.0,
                    tax_rate=0.08,
                    tax_amount=400.0,
                    total_amount=5400.0,
                    status="draft"
                )
                
                st.session_state.invoices.append(new_invoice)
                st.success(f"Invoice {new_invoice.invoice_number} generated!")
                st.rerun()
        
        st.divider()
        
        # Invoice list
        st.subheader("Recent Invoices")
        
        for invoice in st.session_state.invoices:
            status_colors = {'draft': '#6c757d', 'sent': '#ffc107', 'paid': '#28a745'}
            
            st.markdown(f"""
            <div class="document-card">
                <strong>Invoice {invoice.invoice_number}</strong><br>
                <small>Issued: {invoice.date_issued.strftime('%Y-%m-%d')} | Due: {invoice.due_date.strftime('%Y-%m-%d')}</small><br>
                <strong>${invoice.total_amount:,.2f}</strong>
                <span style="background: {status_colors.get(invoice.status, '#6c757d')}; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem; margin-left: 1rem;">
                    {invoice.status.upper()}
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Billing Reports")
        
        # Monthly billing chart
        monthly_data = {
            'Jan': 15000, 'Feb': 18000, 'Mar': 22000, 'Apr': 19000,
            'May': 25000, 'Jun': 28000, 'Jul': 24000, 'Aug': 30000
        }
        
        fig = px.bar(x=list(monthly_data.keys()), y=list(monthly_data.values()),
                     title="Monthly Billing Revenue")
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance summary
        st.subheader("Billing Performance")
        
        performance_data = pd.DataFrame({
            'Metric': ['Total Billed', 'Total Collected', 'Collection Rate', 'Avg Days to Pay'],
            'This Quarter': ['$85,000', '$80,000', '94.1%', '28 days'],
            'Last Quarter': ['$78,000', '$72,000', '92.3%', '32 days'],
            'Change': ['+9.0%', '+11.1%', '+1.8pp', '-4 days']
        })
        
        st.dataframe(performance_data, hide_index=True)

elif page == "System Settings":
    st.title("System Settings & Configuration")
    
    if not has_permission('admin'):
        st.error("Access denied. System administration required.")
        st.stop()
    
    tab1, tab2, tab3 = st.tabs(["Firm Settings", "User Management", "System Health"])
    
    with tab1:
        st.subheader("Firm Configuration")
        
        with st.form("firm_settings"):
            col1, col2 = st.columns(2)
            
            with col1:
                firm_name = st.text_input("Firm Name", value="LegalDoc Pro Demo Firm")
                firm_address = st.text_area("Address", value="123 Legal Street\nNew York, NY 10001")
                firm_phone = st.text_input("Phone", value="(555) 123-4567")
            
            with col2:
                firm_email = st.text_input("Email", value="info@legaldocpro.com")
                firm_website = st.text_input("Website", value="www.legaldocpro.com")
                default_rate = st.number_input("Default Billing Rate", value=250.0)
            
            if st.form_submit_button("Save Settings"):
                st.success("Firm settings saved successfully!")
    
    with tab2:
        st.subheader("User Management")
        
        # Add user form
        with st.form("add_user"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_email = st.text_input("Email")
                new_role = st.selectbox("Role", ["partner", "associate", "paralegal"])
            
            with col2:
                new_name = st.text_input("Full Name")
                new_rate = st.number_input("Billing Rate", value=250.0)
            
            if st.form_submit_button("Add User"):
                if new_email and new_name:
                    st.success(f"User {new_name} added successfully!")
        
        st.divider()
        
        # User list
        st.subheader("Current Users")
        
        users_data = pd.DataFrame({
            'Name': ['John Partner', 'Jane Associate', 'Bob Paralegal'],
            'Email': ['john@firm.com', 'jane@firm.com', 'bob@firm.com'],
            'Role': ['Partner', 'Associate', 'Paralegal'],
            'Status': ['Active', 'Active', 'Active'],
            'Last Login': ['2024-01-15', '2024-01-15', '2024-01-14']
        })
        
        st.dataframe(users_data, hide_index=True)
    
    with tab3:
        st.subheader("System Health")
        
        # System metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("System Uptime", "99.8%")
        
        with col2:
            st.metric("Active Users", "24")
        
        with col3:
            st.metric("Storage Used", "2.1TB")
        
        with col4:
            st.metric("Response Time", "0.24s")
        
        # System performance chart
        hours = list(range(24))
        cpu_usage = [45 + 20 * np.sin(h/24 * 2 * np.pi) + np.random.normal(0, 5) for h in hours]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hours, y=cpu_usage, mode='lines+markers', name='CPU Usage %'))
        fig.add_hline(y=80, line_dash="dash", annotation_text="Warning", line_color="orange")
        fig.update_layout(title="24-Hour CPU Usage", xaxis_title="Hour", yaxis_title="Usage %")
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem 0;">
    <strong>LegalDoc Pro Enterprise Platform</strong> | 
    Complete Legal Practice Management Solution<br>
    <small>AI Analysis • Advanced Analytics • Client Portal • Mobile Access • Integration Suite</small>
</div>
""", unsafe_allow_html=True)</strong><br>
                <small>Modified: {doc.last_modified.strftime('%Y-%m-%d')}</small>
                <span class="status-badge status-{doc.status.replace('_', '-')}">{doc.status.upper()}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Active Matters")
        for matter in st.session_state.matters[:5]:
            st.markdown(f"""
            <div class="matter-card">
                <strong>{matter.name}</strong><br>
                <small>Client: {matter.client_name}</small><br>
                <small>Type: {matter.matter_type.replace('_', ' ').title()}</small>
                <span class="status-badge status-{matter.status}">{matter.status.upper()}</span>
            </div>
            """, unsafe_allow_html=True)

elif page == "Document Management":
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
    if has_permission('write'):
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
                    
                    time.sleep(2)
                    st.rerun()
    
    st.divider()
    
    # Document library
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
                if has_permission('write') and st.button("Edit", key=f"edit_{doc.id}"):
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
                if has_permission('delete') and st.button("Delete", key=f"delete_{doc.id}"):
                    st.session_state.documents = [d for d in st.session_state.documents if d.id != doc.id]
                    st.success("Document deleted!")
                    st.rerun()

elif page == "Matter Management":
    st.title("Matter Management")
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_matters = len([m for m in st.session_state.matters if m.status == 'active'])
        st.metric("Active Matters", active_matters)
    
    with col2:
        total_docs = len(st.session_state.documents)
        st.metric("Total Documents", total_docs)
    
    with col3:
        st.metric("Total Revenue", "$125,000")
    
    with col4:
        st.metric("Avg. Matter Value", "$25,000")
    
    st.divider()
    
    # Create new matter
    if has_permission('write'):
        st.subheader("Create New Matter")
        
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
                    new_matter = Matter(
                        id=str(uuid.uuid4()),
                        name=matter_name,
                        client_id=str(uuid.uuid4()),
                        client_name=client_name,
                        matter_type=matter_type.lower().replace(' ', '_'),
                        status='active',
                        created_date=datetime.now(),
                        assigned_attorneys=[st.session_state['user']['email']],
                        description=description,
                        budget=estimated_budget,
                        estimated_hours=estimated_hours,
                        actual_hours=0.0
                    )
                    
                    st.session_state.matters.append(new_matter)
                    st.success(f"Matter '{matter_name}' created successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
        
        st.divider()
    
    # Matter list
    st.subheader("Active Matters")
    
    for matter in st.session_state.matters:
        matter_docs = [doc for doc in st.session_state.documents if doc.matter_id == matter.id]
        
        with st.expander(f"{matter.name} - {matter.client_name}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Client:** {matter.client_name}")
                st.markdown(f"**Type:** {matter.matter_type.replace('_', ' ').title()}")
                st.markdown(f"**Status:** {matter.status.title()}")
            
            with col2:
                st.markdown(f"**Documents:** {len(matter_docs)}")
                st.markdown(f"**Budget:** ${matter.budget:,.2f}")
                st.markdown(f"**Est. Hours:** {matter.estimated_hours}")
            
            with col3:
                st.markdown(f"**Actual Hours:** {matter.actual_hours}")
                st.markdown(f"**Created:** {matter.created_date.strftime('%Y-%m-%d')}")
            
            if matter.description:
                st.markdown(f"**Description:** {matter.description}")
            
            # Recent documents for this matter
            if matter_docs:
                st.markdown("**Recent Documents:**")
                for doc in matter_docs[-3:]:
                    st.markdown(f"• {doc.name} - {doc.document_type}")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Analytics", key=f"analytics_{matter.id}"):
                    st.info("Matter analytics would open here")
            
            with col2:
                if has_permission('write') and st.button("Edit", key=f"edit_matter_{matter.id}"):
                    st.info("Matter editor would open here")
            
            with col3:
                if st.button("Tasks", key=f"tasks_{matter.id}"):
                    st.info("Task management would open here")

elif page == "AI Insights":
    st.title("AI-Powered Legal Intelligence")
    
    if not has_permission('ai_insights'):
        st.error("Access denied. AI Insights requires elevated permissions.")
        st.stop()
    
    # AI metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Documents Analyzed", "147", "+23")
    
    with col2:
        st.metric("Risk Alerts", "8", "+2")
    
    with col3:
        st.metric("Auto Classifications", "94%", "+3%")
    
    with col4:
        st.metric("Time Saved", "127 hrs", "+18 hrs")
    
    st.divider()
    
    # AI analysis tools
    tab1, tab2, tab3 = st.tabs(["Document Analysis", "Risk Assessment", "Pattern Recognition"])
    
    with tab1:
        st.subheader("AI Document Analysis")
        
        if st.session_state.documents:
            selected_doc_name = st.selectbox("Select Document", [d.name for d in st.session_state.documents])
            selected_doc = next(d for d in st.session_state.documents if d.name == selected_doc_name)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Analyze Document", type="primary"):
                    with st.spinner("AI analyzing document..."):
                        time.sleep(2)
                        analysis = ai_system.analyze_contract(selected_doc.extracted_text)
                        
                        st.success("Analysis Complete!")
                        
                        # Risk assessment
                        risk_colors = {"low": "🟢", "medium": "🟡", "high": "🔴"}
                        st.markdown(f"**Risk Level:** {risk_colors.get(analysis['risk_level'], '⚪')} {analysis['risk_level'].upper()}")
                        
                        # Key clauses
                        st.markdown("**Key Clauses Identified:**")
                        for clause in analysis['key_clauses']:
                            st.markdown(f"• **{clause['type'].title()}:** {clause['text']}")
                        
                        # Missing clauses
                        if analysis['missing_clauses']:
                            st.markdown("**Potentially Missing Clauses:**")
                            for clause in analysis['missing_clauses']:
                                st.markdown(f"• {clause}")
            
            with col2:
                st.markdown("**AI Recommendations:**")
                recommendations = [
                    "Add explicit termination procedures",
                    "Include force majeure clause",
                    "Clarify payment terms",
                    "Add dispute resolution mechanism"
                ]
                
                for rec in recommendations:
                    st.markdown(f"💡 {rec}")
                
                st.markdown("**Document Metrics:**")
                st.metric("Complexity Score", "67/100")
                st.metric("Completeness", "84%")
    
    with tab2:
        st.subheader("Risk Assessment Dashboard")
        
        # Risk summary
        risk_summary = {
            'High Risk': 3,
            'Medium Risk': 8,
            'Low Risk': 25,
            'No Risk': 12
        }
        
        fig = px.pie(values=list(risk_summary.values()), names=list(risk_summary.keys()), 
                     title="Document Risk Distribution")
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk alerts
        st.markdown("**Recent Risk Alerts:**")
        alerts = [
            {"doc": "Contract_XYZ.pdf", "risk": "High", "issue": "Missing termination clause"},
            {"doc": "Agreement_ABC.pdf", "risk": "Medium", "issue": "Unclear payment terms"},
            {"doc": "License_DEF.pdf", "risk": "Medium", "issue": "No liability limitation"}
        ]
        
        for alert in alerts:
            risk_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            st.markdown(f"{risk_color[alert['risk']]} **{alert['doc']}** - {alert['issue']}")
    
    with tab3:
        st.subheader("Pattern Recognition")
        
        if st.button("Analyze Document Patterns"):
            with st.spinner("Analyzing patterns..."):
                time.sleep(2)
                st.success("Pattern analysis complete!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Document Clusters:**")
                    clusters = [
                        {"theme": "Employment Contracts", "count": 15},
                        {"theme": "Real Estate Agreements", "count": 8},
                        {"theme": "Corporate Documents", "count": 12}
                    ]
                    
                    for cluster in clusters:
                        st.markdown(f"• **{cluster['theme']}:** {cluster['count']} documents")
                
                with col2:
                    st.markdown("**Trending Topics:**")
                    topics = ["Remote Work Clauses", "Data Privacy Terms", "AI Governance"]
                    
                    for topic in topics:
                        st.markdown(f"🔥 {topic}")

elif page == "Integrations":
    st.title("Third-Party Integrations")
    
    if not has_permission('integrations'):
        st.error("Access denied. Integration management requires admin privileges.")
        st.stop()
    
    # Integration status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Integrations", "4")
    
    with col2:
        st.metric("Available", "12")
    
    with col3:
        st.metric("Last Sync", "2 mins ago")
    
    with col4:
        st.metric("Success Rate", "98.5%")
    
    st.divider()
    
    # Available integrations
    st.subheader("Available Integrations")
    
    integration_categories = {
        'Email & Communication': ['outlook', 'gmail', 'slack'],
        'Document & Signature': ['docusign', 'adobe_sign'],
        'Calendar & Scheduling': ['google_calendar', 'zoom'],
        'Accounting & Billing': ['quickbooks', 'xero']
    }
    
    for category, integrations in integration_categories.items():
        st.markdown(f"### {category}")
        cols = st.columns(3)
        
        for i, integration_id in enumerate(integrations):
            with cols[i % 3]:
                if integration_id in integration_manager.available_integrations:
                    integration_info = integration_manager.available_integrations[integration_id]
                    is_active = False  # Simplified for demo
                    
                    status_color = "#28a745" if is_active else "#6c757d"
                    status_text = "CONNECTED" if is_active else "AVAILABLE"
                    
                    st.markdown(f"""
                    <div class="integration-card">
                        <h4>{integration_info['name']}</h4>
                        <p style="color: {status_color}; font-weight: bold;">{status_text}</p>
                        <p>{integration_info['type'].replace('_', ' ').title()}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if not is_active:
                        if st.button(f"Connect {integration_info['name']}", key=f"connect_{integration_id}"):
                            config = {"api_key": "demo_key"}
                            if integration_manager.setup_integration(integration_id, config):
                                st.success(f"{integration_info['name']} connected!")
                                st.rerun()
                    else:
                        if st.button(f"Configure", key=f"config_{integration_id}"):
                            st.info(f"Configuration for {integration_info['name']}")

elif page == "Mobile App":
    st.title("Mobile Application")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Mobile Features")
        
        features = [
            ("Document Viewer", "View documents on mobile"),
            ("Document Scanner", "Scan with camera"),
            ("Voice Notes", "Record voice memos"),
            ("Time Tracking", "Track hours on-the-go"),
            ("Calendar Sync", "View appointments"),
            ("Push Notifications", "Important alerts"),
            ("Offline Sync", "Work without internet")
        ]
        
        for feature, desc in features:
            st.markdown(f"""
            <div style="margin: 1rem 0; padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                <strong>{feature}</strong><br>
                <small>{desc}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Mobile App Preview")
        mobile_framework.render_mobile_interface()
        
        st.markdown("### Download App")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: #000; color: white; padding: 1rem; border-radius: 8px; text-align: center;">
                iOS App Store<br>
                <small>iPhone & iPad</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #34a853; color: white; padding: 1rem; border-radius: 8px; text-align: center;">
                Google Play Store<br>
                <small>Android</small>
            </div>
            """, unsafe_allow_html=True)

elif page == "Business Intelligence":
    st.title("Business Intelligence & Analytics")
    
    if not has_permission('admin'):
        st.error("Access denied. Business Intelligence requires admin privileges.")
        st.stop()
    
    # Executive summary
    exec_metrics = business_intelligence.generate_executive_dashboard()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue", f"${exec_metrics['total_revenue']:,.0f}", "+8.5%")
    
    with col2:
        st.metric("Active Matters", exec_metrics['active_matters'], "+2")
    
    with col3:
        st.metric("Utilization Rate", f"{exec_metrics['utilization_rate']:.1f}%", "+3.2%")
    
    with col4:
        st.metric("Client Satisfaction", f"{exec_metrics['client_satisfaction']:.1f}/5", "+0.3")
    
    st.divider()
    
    # Analytics tabs
    tab1, tab2, tab3 = st.tabs(["Financial", "Productivity", "Client Analytics"])
    
    with tab1:
        st.subheader("Financial Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(business_intelligence.create_revenue_chart(), use_container_width=True)
        
        with col2:
            # Revenue by practice area
            practice_revenue = {
                'Corporate Law': 45000,
                'Litigation': 32000,
                'Family Law': 18000,
                'Real Estate': 15000
            }
            
            fig = px.pie(values=list(practice_revenue.values()), 
                        names=list(practice_revenue.keys()),
                        title="Revenue by Practice Area")
            st.plotly_chart(fig, use_container_width=True)
        
        # Financial KPIs
        st.subheader("Financial KPIs")
        
        kpi_data = pd.DataFrame({
            'Metric': ['Total Revenue', 'Total Expenses', 'Net Profit', 'Profit Margin'],
            'Current': ['$125,000', '$85,000', '$40,000', '32%'],
            'Previous': ['$118,000', '$82,000', '$36,000', '30.5%'],
            'Change': ['+5.9%', '+3.7%', '+11.1%', '+1.5pp']
        })
        
        st.dataframe(kpi_data, hide_index=True)
    
    with tab2:
        st.subheader("Productivity Analytics")
        
        # Sample productivity chart
        attorneys = ['Partner A', 'Associate B', 'Associate C', 'Paralegal D']
        hours = [42, 38, 35, 28]
        
        fig = px.bar(x=attorneys, y=hours, title="Weekly Hours by Team Member")
        st.plotly_chart(fig, use_container_width=True)
        
        # Efficiency metrics
        st.subheader("Efficiency Improvements")
        
        improvements = {
            'AI Document Review': '+35%',
            'Automated Billing': '+22%',
            'Template Usage': '+18%',
            'Client Portal': '+15%'
        }
        
        for feature, improvement in improvements.items():
            st.markdown(f"• **{feature}:** {improvement} time savings")
    
    with tab3:
        st.subheader("Client Analytics")
        
        # Client retention
        retention_data = pd.DataFrame({
            'Metric': ['Client Retention Rate', 'New Clients/Month', 'Avg Client Value', 'Referral Rate'],
            'Value': ['92%', '15', '$85,000', '23%'],
            'Benchmark': ['85%', '12', '$75,000', '20%']
        })
        
        st.dataframe(retention_data, hide_index=True)
        
        # Client segmentation
        segments = {'Enterprise': 25, 'Mid-Market': 45, 'Small Business': 35, 'Individual': 60}
        
        fig = px.pie(values=list(segments.values()), names=list(segments.keys()),
                     title="Client Segmentation")
        st.plotly_chart(fig, use_container_width=True)

elif page == "Client Dashboard" and user_role == 'client':
    client_id = st.session_state['user']['client_id']
    
    st.markdown("""
    <div class="main-header">
        <h1>Welcome to Your Legal Dashboard</h1>
        <p>Access your documents, billing, and case updates</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Client metrics
    col1, col2, col3, col4 = st.columns(4)
    
    client_docs = [doc for doc in st.session_state.documents if doc.client_name == "Acme Corporation"]
    
    with col1:
        st.metric("My Documents", len(client_docs))
    
    with col2:
        st.metric("Active Matters", 2)
    
    with col3:
        st.metric("Outstanding Balance", "$0.00")
    
    with col4:
        st.metric("Last Payment", "$3,888")
    
    st.divider()
    
    # Recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recent Documents")
        for doc in client_docs[-3:]:
            st.markdown(f"""
            <div class="client-portal">
                <strong>{doc.name}
