import streamlit as st
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
import random

# Import models (assuming they exist in the models module)
try:
    from models.user import Client, User
    from models.matter import Matter
    from models.document import Document, DocumentStatus
    from models.billing import Invoice, TimeEntry
except ImportError:
    # Fallback dataclasses for demo purposes
    from dataclasses import dataclass
    from typing import List, Dict
    
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
    
    class DocumentStatus:
        DRAFT = "draft"
        UNDER_REVIEW = "under_review"
        APPROVED = "approved"
        FINAL = "final"
        ARCHIVED = "archived"

try:
    from services.document_processor import DocumentProcessor
except ImportError:
    # Fallback DocumentProcessor for demo
    class DocumentProcessor:
        @staticmethod
        def classify_document(filename: str, text: str) -> str:
            return "General Document"
        
        @staticmethod
        def extract_key_information(text: str) -> Dict:
            return {"dates": [], "monetary_amounts": [], "email_addresses": []}

def initialize_session_state():
    """Initialize all session state variables with default values."""
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
        'current_page': 'Executive Dashboard',
        'notifications': [],
        'user_sessions': {},
        'failed_attempts': {},
        'sync_history': [],
        'integration_configs': {},
        'webhooks': {},
        'demo_users': {},
        'tasks': [],
        'deadlines': [],
        'templates': [],
        'workflows': [],
        'reports': [],
        'analytics_cache': {},
        'email_queue': [],
        'document_versions': {},
        'access_logs': [],
        'backup_history': [],
        'performance_metrics': {}
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def load_sample_data():
    """Load comprehensive sample data for demonstration purposes."""
    document_processor = DocumentProcessor()
    
    # Load sample clients
    if not st.session_state.clients:
        st.session_state.clients = _create_sample_clients()
    
    # Load sample matters
    if not st.session_state.matters:
        st.session_state.matters = _create_sample_matters()
    
    # Load sample documents
    if not st.session_state.documents:
        st.session_state.documents = _create_sample_documents(document_processor)
    
    # Load sample invoices
    if not st.session_state.invoices:
        st.session_state.invoices = _create_sample_invoices()
    
    # Load sample time entries
    if not st.session_state.time_entries:
        st.session_state.time_entries = _create_sample_time_entries()
    
    # Load sample calendar events
    if not st.session_state.calendar_events:
        st.session_state.calendar_events = _create_sample_calendar_events()
    
    # Load sample tasks and deadlines
    if not st.session_state.tasks:
        st.session_state.tasks = _create_sample_tasks()
    
    if not st.session_state.deadlines:
        st.session_state.deadlines = _create_sample_deadlines()
    
    # Load sample templates
    if not st.session_state.templates:
        st.session_state.templates = _create_sample_templates()
    
    # Load sample notifications
    if not st.session_state.notifications:
        st.session_state.notifications = _create_sample_notifications()

def _create_sample_clients() -> List[Client]:
    """Create sample client data."""
    return [
        Client(
            id="client_1",
            name="Acme Corporation",
            client_type="corporation",
            contact_info={
                "phone": "(555) 123-4567", 
                "email": "legal@acme.com",
                "address": "123 Business Ave, Suite 100, New York, NY 10001",
                "website": "www.acmecorp.com"
            },
            created_date=datetime.now() - timedelta(days=365),
            status="active",
            portal_access=True
        ),
        Client(
            id="client_2",
            name="Sarah Johnson",
            client_type="individual",
            contact_info={
                "phone": "(555) 987-6543", 
                "email": "sarah.johnson@email.com",
                "address": "456 Residential Dr, Boston, MA 02101"
            },
            created_date=datetime.now() - timedelta(days=180),
            status="active",
            portal_access=True
        ),
        Client(
            id="client_3",
            name="Tech Solutions Inc",
            client_type="corporation",
            contact_info={
                "phone": "(555) 456-7890",
                "email": "contracts@techsolutions.com",
                "address": "789 Innovation Blvd, San Francisco, CA 94105",
                "website": "www.techsolutions.com"
            },
            created_date=datetime.now() - timedelta(days=90),
            status="active",
            portal_access=False
        ),
        Client(
            id="client_4",
            name="Global Manufacturing LLC",
            client_type="llc",
            contact_info={
                "phone": "(555) 321-0987",
                "email": "legal@globalmfg.com",
                "address": "321 Industrial Way, Chicago, IL 60601"
            },
            created_date=datetime.now() - timedelta(days=200),
            status="active",
            portal_access=True
        ),
        Client(
            id="client_5",
            name="Michael Davis",
            client_type="individual",
            contact_info={
                "phone": "(555) 654-3210",
                "email": "mdavis@personalmail.com",
                "address": "987 Suburb Lane, Austin, TX 78701"
            },
            created_date=datetime.now() - timedelta(days=60),
            status="prospective",
            portal_access=False
        )
    ]

def _create_sample_matters() -> List[Matter]:
    """Create sample matter data."""
    return [
        Matter(
            id="matter_1",
            name="Acme Corp M&A Transaction",
            client_id="client_1",
            client_name="Acme Corporation",
            matter_type="corporate",
            status="active",
            created_date=datetime.now() - timedelta(days=45),
            assigned_attorneys=["demo.partner@legaldocpro.com", "demo.associate@legaldocpro.com"],
            description="Acquisition of regional competitor including due diligence, contract negotiation, and regulatory approval",
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
            assigned_attorneys=["demo.associate@legaldocpro.com"],
            description="Modification of existing custody arrangement due to relocation",
            budget=15000.0,
            estimated_hours=40,
            actual_hours=18.0
        ),
        Matter(
            id="matter_3",
            name="Tech Solutions Employment Dispute",
            client_id="client_3",
            client_name="Tech Solutions Inc",
            matter_type="employment",
            status="active",
            created_date=datetime.now() - timedelta(days=20),
            assigned_attorneys=["demo.partner@legaldocpro.com"],
            description="Defense against wrongful termination claim",
            budget=75000.0,
            estimated_hours=150,
            actual_hours=45.0
        ),
        Matter(
            id="matter_4",
            name="Global Manufacturing IP Licensing",
            client_id="client_4",
            client_name="Global Manufacturing LLC",
            matter_type="intellectual_property",
            status="completed",
            created_date=datetime.now() - timedelta(days=120),
            assigned_attorneys=["demo.associate@legaldocpro.com"],
            description="Technology licensing agreement for manufacturing processes",
            budget=50000.0,
            estimated_hours=100,
            actual_hours=95.0
        ),
        Matter(
            id="matter_5",
            name="Davis Real Estate Transaction",
            client_id="client_5",
            client_name="Michael Davis",
            matter_type="real_estate",
            status="pending",
            created_date=datetime.now() - timedelta(days=10),
            assigned_attorneys=["demo.paralegal@legaldocpro.com"],
            description="Commercial property purchase and financing",
            budget=25000.0,
            estimated_hours=60,
            actual_hours=8.0
        )
    ]

def _create_sample_documents(document_processor: DocumentProcessor) -> List[Document]:
    """Create sample document data."""
    documents = []
    
    sample_documents_data = [
        {
            "name": "Merger_Agreement_Final_v2.1.pdf",
            "matter_id": "matter_1",
            "client_name": "Acme Corporation",
            "text": "This Merger Agreement is entered into between Acme Corporation and Target Company on January 15, 2024. The purchase price is $50,000,000. Contact: john.doe@acme.com, (555) 123-4567. Effective date: March 1, 2024.",
            "status": DocumentStatus.FINAL,
            "is_privileged": True,
            "tags": ["merger", "acquisition", "final"]
        },
        {
            "name": "Due_Diligence_Checklist.docx",
            "matter_id": "matter_1",
            "client_name": "Acme Corporation",
            "text": "Due diligence checklist for acquisition. Key dates: February 1, 2024 (financial review), February 15, 2024 (legal review). Budget allocation: $25,000 for external consultants.",
            "status": DocumentStatus.APPROVED,
            "is_privileged": False,
            "tags": ["due-diligence", "checklist"]
        },
        {
            "name": "Custody_Modification_Petition.pdf",
            "matter_id": "matter_2",
            "client_name": "Sarah Johnson",
            "text": "Petition for modification of child custody filed on behalf of Sarah Johnson. Hearing scheduled for April 10, 2024. Contact attorney: family@lawfirm.com.",
            "status": DocumentStatus.FINAL,
            "is_privileged": True,
            "tags": ["family-law", "custody", "petition"]
        },
        {
            "name": "Employment_Contract_Review.docx",
            "matter_id": "matter_3",
            "client_name": "Tech Solutions Inc",
            "text": "Review of employment contracts dated December 1, 2023. Severance provisions include 6 months salary. Contact HR: hr@techsolutions.com, (555) 456-7890.",
            "status": DocumentStatus.UNDER_REVIEW,
            "is_privileged": False,
            "tags": ["employment", "contracts", "review"]
        },
        {
            "name": "IP_License_Agreement_Draft.pdf",
            "matter_id": "matter_4",
            "client_name": "Global Manufacturing LLC",
            "text": "Intellectual Property License Agreement draft. Royalty rate: 3.5% of net sales. Term: 5 years with automatic renewal. Contact: licensing@globalmfg.com.",
            "status": DocumentStatus.ARCHIVED,
            "is_privileged": False,
            "tags": ["ip", "licensing", "completed"]
        },
        {
            "name": "Property_Purchase_Agreement.pdf",
            "matter_id": "matter_5",
            "client_name": "Michael Davis",
            "text": "Commercial property purchase agreement for 987 Business Plaza. Purchase price: $2,500,000. Closing date: May 15, 2024. Financing contingency expires April 1, 2024.",
            "status": DocumentStatus.DRAFT,
            "is_privileged": False,
            "tags": ["real-estate", "purchase", "commercial"]
        }
    ]
    
    for i, doc_data in enumerate(sample_documents_data):
        doc = Document(
            id=str(uuid.uuid4()),
            name=doc_data["name"],
            matter_id=doc_data["matter_id"],
            client_name=doc_data["client_name"],
            document_type=document_processor.classify_document(doc_data["name"], doc_data["text"]),
            current_version=f"v{random.randint(1,3)}.{random.randint(0,5)}",
            status=doc_data["status"],
            tags=doc_data["tags"],
            extracted_text=doc_data["text"],
            key_information=document_processor.extract_key_information(doc_data["text"]),
            created_date=datetime.now() - timedelta(days=random.randint(1, 60)),
            last_modified=datetime.now() - timedelta(days=random.randint(0, 30)),
            is_privileged=doc_data["is_privileged"]
        )
        documents.append(doc)
    
    return documents

def _create_sample_invoices() -> List[Invoice]:
    """Create sample invoice data."""
    return [
        Invoice(
            id="inv_1",
            client_id="client_1",
            matter_id="matter_1",
            invoice_number="INV-20241201-0001",
            date_issued=datetime.now() - timedelta(days=30),
            due_date=datetime.now(),
            line_items=[
                {"description": "Legal research and analysis", "hours": 8.0, "rate": 450.0, "amount": 3600.0},
                {"description": "Document review and drafting", "hours": 12.0, "rate": 450.0, "amount": 5400.0},
                {"description": "Client meetings and negotiations", "hours": 6.0, "rate": 450.0, "amount": 2700.0}
            ],
            subtotal=11700.0,
            tax_rate=0.08,
            tax_amount=936.0,
            total_amount=12636.0,
            status="paid"
        ),
        Invoice(
            id="inv_2",
            client_id="client_2",
            matter_id="matter_2",
            invoice_number="INV-20241215-0002",
            date_issued=datetime.now() - timedelta(days=15),
            due_date=datetime.now() + timedelta(days=15),
            line_items=[
                {"description": "Family law consultation", "hours": 3.0, "rate": 350.0, "amount": 1050.0},
                {"description": "Petition preparation", "hours": 5.0, "rate": 350.0, "amount": 1750.0}
            ],
            subtotal=2800.0,
            tax_rate=0.08,
            tax_amount=224.0,
            total_amount=3024.0,
            status="sent"
        ),
        Invoice(
            id="inv_3",
            client_id="client_3",
            matter_id="matter_3",
            invoice_number="INV-20241220-0003",
            date_issued=datetime.now() - timedelta(days=5),
            due_date=datetime.now() + timedelta(days=25),
            line_items=[
                {"description": "Employment law defense preparation", "hours": 15.0, "rate": 475.0, "amount": 7125.0},
                {"description": "Discovery response preparation", "hours": 8.0, "rate": 300.0, "amount": 2400.0}
            ],
            subtotal=9525.0,
            tax_rate=0.08,
            tax_amount=762.0,
            total_amount=10287.0,
            status="draft"
        )
    ]

def _create_sample_time_entries() -> List[TimeEntry]:
    """Create sample time entry data."""
    time_entries = []
    
    activities = [
        "Legal research", "Document review", "Client meeting", "Court appearance",
        "Drafting", "Phone conference", "Email communication", "Case preparation"
    ]
    
    users = ["demo.partner@legaldocpro.com", "demo.associate@legaldocpro.com", "demo.paralegal@legaldocpro.com"]
    matters = ["matter_1", "matter_2", "matter_3", "matter_4", "matter_5"]
    clients = ["client_1", "client_2", "client_3", "client_4", "client_5"]
    
    for i in range(50):  # Create 50 sample time entries
        entry = TimeEntry(
            id=str(uuid.uuid4()),
            user_id=random.choice(users),
            matter_id=random.choice(matters),
            client_id=random.choice(clients),
            date=datetime.now() - timedelta(days=random.randint(0, 90)),
            hours=round(random.uniform(0.25, 8.0), 2),
            description=f"{random.choice(activities)} for ongoing matter work",
            billing_rate=random.choice([250.0, 350.0, 450.0, 475.0]),
            billable=random.choice([True, True, True, False]),  # 75% billable
            activity_type=random.choice(activities),
            status=random.choice(["draft", "submitted", "approved", "billed"]),
            created_date=datetime.now() - timedelta(days=random.randint(0, 90))
        )
        time_entries.append(entry)
    
    return time_entries

def _create_sample_calendar_events() -> List[Dict[str, Any]]:
    """Create sample calendar events."""
    return [
        {
            "id": str(uuid.uuid4()),
            "title": "Client Meeting - Acme Corp M&A",
            "start": datetime.now() + timedelta(days=1, hours=10),
            "end": datetime.now() + timedelta(days=1, hours=11, minutes=30),
            "type": "meeting",
            "client_id": "client_1",
            "matter_id": "matter_1",
            "attendees": ["demo.partner@legaldocpro.com", "legal@acme.com"],
            "location": "Conference Room A",
            "description": "Quarterly review meeting for M&A transaction progress"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Court Hearing - Johnson Custody",
            "start": datetime.now() + timedelta(days=3, hours=9),
            "end": datetime.now() + timedelta(days=3, hours=10, minutes=30),
            "type": "court",
            "client_id": "client_2",
            "matter_id": "matter_2",
            "attendees": ["demo.associate@legaldocpro.com"],
            "location": "Family Court, Room 201",
            "description": "Custody modification hearing"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Deposition - Tech Solutions Case",
            "start": datetime.now() + timedelta(days=7, hours=14),
            "end": datetime.now() + timedelta(days=7, hours=17),
            "type": "deposition",
            "client_id": "client_3",
            "matter_id": "matter_3",
            "attendees": ["demo.partner@legaldocpro.com", "contracts@techsolutions.com"],
            "location": "Law Firm Conference Room",
            "description": "Employee deposition for wrongful termination case"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Document Review Session",
            "start": datetime.now() + timedelta(days=2, hours=13),
            "end": datetime.now() + timedelta(days=2, hours=16),
            "type": "work_session",
            "client_id": "client_1",
            "matter_id": "matter_1",
            "attendees": ["demo.associate@legaldocpro.com", "demo.paralegal@legaldocpro.com"],
            "location": "Library",
            "description": "Review due diligence documents"
        }
    ]

def _create_sample_tasks() -> List[Dict[str, Any]]:
    """Create sample tasks."""
    return [
        {
            "id": str(uuid.uuid4()),
            "title": "File motion for summary judgment",
            "description": "Prepare and file motion for summary judgment in Tech Solutions employment case",
            "assigned_to": "demo.partner@legaldocpro.com",
            "matter_id": "matter_3",
            "due_date": datetime.now() + timedelta(days=14),
            "priority": "high",
            "status": "in_progress",
            "created_date": datetime.now() - timedelta(days=3)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Review purchase agreement",
            "description": "Review and comment on commercial property purchase agreement",
            "assigned_to": "demo.associate@legaldocpro.com",
            "matter_id": "matter_5",
            "due_date": datetime.now() + timedelta(days=7),
            "priority": "medium",
            "status": "pending",
            "created_date": datetime.now() - timedelta(days=1)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Prepare custody modification documents",
            "description": "Draft supplemental documents for custody modification case",
            "assigned_to": "demo.paralegal@legaldocpro.com",
            "matter_id": "matter_2",
            "due_date": datetime.now() + timedelta(days=10),
            "priority": "medium",
            "status": "pending",
            "created_date": datetime.now() - timedelta(days=2)
        }
    ]

def _create_sample_deadlines() -> List[Dict[str, Any]]:
    """Create sample deadlines."""
    return [
        {
            "id": str(uuid.uuid4()),
            "description": "Discovery response deadline",
            "due_date": datetime.now() + timedelta(days=21),
            "matter_id": "matter_3",
            "priority": "critical",
            "assigned_to": "demo.partner@legaldocpro.com",
            "is_completed": False,
            "reminder_dates": [
                datetime.now() + timedelta(days=14),
                datetime.now() + timedelta(days=7),
                datetime.now() + timedelta(days=1)
            ]
        },
        {
            "id": str(uuid.uuid4()),
            "description": "Merger agreement execution deadline",
            "due_date": datetime.now() + timedelta(days=45),
            "matter_id": "matter_1",
            "priority": "high",
            "assigned_to": "demo.associate@legaldocpro.com",
            "is_completed": False,
            "reminder_dates": [
                datetime.now() + timedelta(days=30),
                datetime.now() + timedelta(days=15)
            ]
        },
        {
            "id": str(uuid.uuid4()),
            "description": "Property closing date",
            "due_date": datetime.now() + timedelta(days=60),
            "matter_id": "matter_5",
            "priority": "medium",
            "assigned_to": "demo.paralegal@legaldocpro.com",
            "is_completed": False,
            "reminder_dates": [
                datetime.now() + timedelta(days=45),
                datetime.now() + timedelta(days=30)
            ]
        }
    ]

def _create_sample_templates() -> List[Dict[str, Any]]:
    """Create sample document templates."""
    return [
        {
            "id": str(uuid.uuid4()),
            "name": "Standard NDA Template",
            "category": "Contracts",
            "description": "Non-disclosure agreement template for business transactions",
            "template_type": "legal_document",
            "created_by": "demo.partner@legaldocpro.com",
            "created_date": datetime.now() - timedelta(days=120),
            "usage_count": 45,
            "tags": ["nda", "confidentiality", "template"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Employment Agreement Template",
            "category": "Employment",
            "description": "Standard employment agreement template",
            "template_type": "legal_document",
            "created_by": "demo.associate@legaldocpro.com",
            "created_date": datetime.now() - timedelta(days=90),
            "usage_count": 23,
            "tags": ["employment", "agreement", "template"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Client Intake Form",
            "category": "Administration",
            "description": "Standard client intake and information gathering form",
            "template_type": "form",
            "created_by": "demo.paralegal@legaldocpro.com",
            "created_date": datetime.now() - timedelta(days=60),
            "usage_count": 67,
            "tags": ["intake", "client", "form"]
        }
    ]

def _create_sample_notifications() -> List[Dict[str, Any]]:
    """Create sample notifications."""
    return [
        {
            "id": str(uuid.uuid4()),
            "title": "Upcoming Court Hearing",
            "message": "Johnson custody modification hearing scheduled for tomorrow at 9:00 AM",
            "type": "deadline",
            "priority": "high",
            "created_date": datetime.now() - timedelta(hours=2),
            "is_read": False,
            "matter_id": "matter_2",
            "action_url": "/calendar"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "New Document Shared",
            "message": "Acme Corporation shared updated financial statements",
            "type": "document",
            "priority": "medium",
            "created_date": datetime.now() - timedelta(hours=6),
            "is_read": False,
            "matter_id": "matter_1",
            "action_url": "/documents"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Invoice Payment Received",
            "message": "Payment received for Invoice INV-20241201-0001 ($12,636.00)",
            "type": "billing",
            "priority": "low",
            "created_date": datetime.now() - timedelta(days=1),
            "is_read": True,
            "matter_id": "matter_1",
            "action_url": "/billing"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Task Assignment",
            "message": "You have been assigned to review purchase agreement for Davis matter",
            "type": "task",
            "priority": "medium",
            "created_date": datetime.now() - timedelta(hours=12),
            "is_read": False,
            "matter_id": "matter_5",
            "action_url": "/tasks"
        }
    ]

def clear_session_state():
    """Clear all session state data - useful for testing or reset functionality."""
    keys_to_clear = [
        'documents', 'matters', 'clients', 'time_entries', 'invoices',
        'calendar_events', 'ai_insights', 'integrations', 'audit_log',
        'search_index', 'mobile_session', 'tasks', 'deadlines',
        'templates', 'notifications', 'workflows', 'reports'
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
            st.session_state[key] = []

def get_session_stats() -> Dict[str, int]:
    """Get statistics about current session data."""
    return {
        'clients': len(st.session_state.get('clients', [])),
        'matters': len(st.session_state.get('matters', [])),
        'documents': len(st.session_state.get('documents', [])),
        'time_entries': len(st.session_state.get('time_entries', [])),
        'invoices': len(st.session_state.get('invoices', [])),
        'calendar_events': len(st.session_state.get('calendar_events', [])),
        'tasks': len(st.session_state.get('tasks', [])),
        'deadlines': len(st.session_state.get('deadlines', [])),
        'templates': len(st.session_state.get('templates', [])),
        'notifications': len(st.session_state.get('notifications', [])),
        'active_matters': len([m for m in st.session_state.get('matters', []) if getattr(m, 'status', '') == 'active']),
        'unread_notifications': len([n for n in st.session_state.get('notifications', []) if not n.get('is_read', True)])
    }

def backup_session_data() -> Dict[str, Any]:
    """Create a backup of current session data."""
    backup_data = {}
    
    backup_keys = [
        'clients', 'matters', 'documents', 'time_entries', 'invoices',
        'calendar_events', 'tasks', 'deadlines', 'templates'
    ]
    
    for key in backup_keys:
        if key in st.session_state:
            backup_data[key] = st.session_state[key]
    
    backup_data['backup_timestamp'] = datetime.now().isoformat()
    backup_data['backup_id'] = str(uuid.uuid4())
    
    # Store in session state backup history
    if 'backup_history' not in st.session_state:
        st.session_state.backup_history = []
    
    st.session_state.backup_history.append({
        'id': backup_data['backup_id'],
        'timestamp': backup_data['backup_timestamp'],
        'data_counts': get_session_stats()
    })
    
    # Keep only last 10 backups
    if len(st.session_state.backup_history) > 10:
        st.session_state.backup_history = st.session_state.backup_history[-10:]
    
    return backup_data

def restore_session_data(backup_data: Dict[str, Any]) -> bool:
    """Restore session data from backup."""
    try:
        restore_keys = [
            'clients', 'matters', 'documents', 'time_entries', 'invoices',
            'calendar_events', 'tasks', 'deadlines', 'templates'
        ]
        
        for key in restore_keys:
            if key in backup_data:
                st.session_state[key] = backup_data[key]
        
        return True
    except Exception as e:
        st.error(f"Failed to restore session data: {str(e)}")
        return False

def add_audit_log_entry(action: str, details: Dict[str, Any] = None, user_id: str = None):
    """Add an entry to the audit log."""
    if 'audit_log' not in st.session_state:
        st.session_state.audit_log = []
    
    log_entry = {
        'id': str(uuid.uuid4()),
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'user_id': user_id or st.session_state.get('user', {}).get('email', 'system'),
        'details': details or {},
        'ip_address': '127.0.0.1'  # Mock IP for demo
    }
    
    st.session_state.audit_log.append(log_entry)
    
    # Keep only last 1000 audit entries
    if len(st.session_state.audit_log) > 1000:
        st.session_state.audit_log = st.session_state.audit_log[-1000:]

def search_session_data(query: str, data_types: List[str] = None) -> Dict[str, List[Any]]:
    """Search across session data."""
    if not data_types:
        data_types = ['clients', 'matters', 'documents']
    
    results = {}
    query_lower = query.lower()
    
    for data_type in data_types:
        results[data_type] = []
        data_list = st.session_state.get(data_type, [])
        
        for item in data_list:
            # Search in various fields based on data type
            if data_type == 'clients':
                searchable_text = f"{getattr(item, 'name', '')} {getattr(item, 'client_type', '')} {getattr(item, 'contact_info', {}).get('email', '')}".lower()
            elif data_type == 'matters':
                searchable_text = f"{getattr(item, 'name', '')} {getattr(item, 'description', '')} {getattr(item, 'client_name', '')}".lower()
            elif data_type == 'documents':
                searchable_text = f"{getattr(item, 'name', '')} {getattr(item, 'extracted_text', '')} {' '.join(getattr(item, 'tags', []))}".lower()
            else:
                searchable_text = str(item).lower()
            
            if query_lower in searchable_text:
                results[data_type].append(item)
    
    return results

def get_recent_activity(limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent activity across the system."""
    activities = []
    
    # Recent documents
    recent_docs = sorted(st.session_state.get('documents', []), 
                        key=lambda x: getattr(x, 'last_modified', datetime.min), 
                        reverse=True)[:5]
    
    for doc in recent_docs:
        activities.append({
            'type': 'document',
            'action': 'modified',
            'item_name': getattr(doc, 'name', 'Unknown'),
            'timestamp': getattr(doc, 'last_modified', datetime.now()),
            'matter_name': next((m.name for m in st.session_state.get('matters', []) 
                               if m.id == getattr(doc, 'matter_id', '')), 'Unknown')
        })
    
    # Recent time entries
    recent_time = sorted(st.session_state.get('time_entries', []), 
                        key=lambda x: getattr(x, 'created_date', datetime.min), 
                        reverse=True)[:3]
    
    for entry in recent_time:
        activities.append({
            'type': 'time_entry',
            'action': 'created',
            'item_name': f"{getattr(entry, 'activity_type', 'Work')} - {getattr(entry, 'hours', 0)}h",
            'timestamp': getattr(entry, 'created_date', datetime.now()),
            'matter_name': next((m.name for m in st.session_state.get('matters', []) 
                               if m.id == getattr(entry, 'matter_id', '')), 'Unknown')
        })
    
    # Recent invoices
    recent_invoices = sorted(st.session_state.get('invoices', []), 
                            key=lambda x: getattr(x, 'date_issued', datetime.min), 
                            reverse=True)[:2]
    
    for invoice in recent_invoices:
        activities.append({
            'type': 'invoice',
            'action': 'issued',
            'item_name': getattr(invoice, 'invoice_number', 'Unknown'),
            'timestamp': getattr(invoice, 'date_issued', datetime.now()),
            'matter_name': next((m.name for m in st.session_state.get('matters', []) 
                               if m.id == getattr(invoice, 'matter_id', '')), 'Unknown')
        })
    
    # Sort all activities by timestamp and limit
    activities.sort(key=lambda x: x['timestamp'], reverse=True)
    return activities[:limit]

def validate_session_data() -> Dict[str, List[str]]:
    """Validate session data integrity and return any issues found."""
    issues = {
        'errors': [],
        'warnings': [],
        'info': []
    }
    
    # Validate client references in matters
    client_ids = [getattr(c, 'id', '') for c in st.session_state.get('clients', [])]
    for matter in st.session_state.get('matters', []):
        matter_client_id = getattr(matter, 'client_id', '')
        if matter_client_id and matter_client_id not in client_ids:
            issues['errors'].append(f"Matter '{getattr(matter, 'name', 'Unknown')}' references non-existent client ID: {matter_client_id}")
    
    # Validate matter references in documents
    matter_ids = [getattr(m, 'id', '') for m in st.session_state.get('matters', [])]
    for document in st.session_state.get('documents', []):
        doc_matter_id = getattr(document, 'matter_id', '')
        if doc_matter_id and doc_matter_id not in matter_ids:
            issues['warnings'].append(f"Document '{getattr(document, 'name', 'Unknown')}' references non-existent matter ID: {doc_matter_id}")
    
    # Check for duplicate IDs
    all_ids = []
    for data_type in ['clients', 'matters', 'documents', 'invoices']:
        for item in st.session_state.get(data_type, []):
            item_id = getattr(item, 'id', '')
            if item_id:
                if item_id in all_ids:
                    issues['errors'].append(f"Duplicate ID found: {item_id} in {data_type}")
                else:
                    all_ids.append(item_id)
    
    # Info messages
    stats = get_session_stats()
    issues['info'].append(f"Total items in session: {sum(stats.values())}")
    
    return issues

def export_session_data(format_type: str = 'json') -> str:
    """Export session data in specified format."""
    export_data = {}
    
    export_keys = [
        'clients', 'matters', 'documents', 'time_entries', 'invoices',
        'calendar_events', 'tasks', 'deadlines', 'templates'
    ]
    
    for key in export_keys:
        if key in st.session_state:
            # Convert objects to dictionaries for serialization
            items = st.session_state[key]
            if items and hasattr(items[0], '__dict__'):
                export_data[key] = [item.__dict__ if hasattr(item, '__dict__') else item for item in items]
            else:
                export_data[key] = items
    
    export_data['export_metadata'] = {
        'export_timestamp': datetime.now().isoformat(),
        'export_id': str(uuid.uuid4()),
        'format': format_type,
        'statistics': get_session_stats()
    }
    
    if format_type == 'json':
        import json
        return json.dumps(export_data, indent=2, default=str)
    else:
        return str(export_data)

def import_session_data(import_data: Dict[str, Any]) -> bool:
    """Import session data from external source."""
    try:
        import_keys = [
            'clients', 'matters', 'documents', 'time_entries', 'invoices',
            'calendar_events', 'tasks', 'deadlines', 'templates'
        ]
        
        for key in import_keys:
            if key in import_data:
                st.session_state[key] = import_data[key]
        
        add_audit_log_entry('data_import', {
            'imported_keys': list(import_data.keys()),
            'import_timestamp': datetime.now().isoformat()
        })
        
        return True
    except Exception as e:
        st.error(f"Failed to import session data: {str(e)}")
        return False

def update_performance_metrics():
    """Update performance metrics in session state."""
    if 'performance_metrics' not in st.session_state:
        st.session_state.performance_metrics = {}
    
    stats = get_session_stats()
    
    st.session_state.performance_metrics.update({
        'last_updated': datetime.now().isoformat(),
        'data_counts': stats,
        'memory_usage_estimate': sum(stats.values()) * 1024,  # Rough estimate in bytes
        'session_age': (datetime.now() - datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds(),
        'active_matters_ratio': stats.get('active_matters', 0) / max(stats.get('matters', 1), 1)
    })
