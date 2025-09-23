import streamlit as st
import uuid
from datetime import datetime, timedelta
from models import Client, Matter, Document, Invoice, DocumentStatus
from services import DocumentProcessor

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
        'system_settings': {},
        'current_page': 'Executive Dashboard'
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def load_sample_data():
    document_processor = DocumentProcessor()
    
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
