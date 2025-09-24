import streamlit as st
from datetime import datetime, timedelta
import json
import os

def initialize_session_state():
    """Initialize session state variables with default values"""
    defaults = {
        'current_page': 'Executive Dashboard',
        'show_user_settings': False,
        'logged_in': False,
        'user_data': {},
        'clients': [],
        'matters': [],
        'documents': [],
        'tasks': [],
        'invoices': [],
        'time_entries': [],
        'calendar_events': [],
        'notifications': [],
        'data_loaded': False,
        'theme': 'light',
        'sidebar_expanded': True
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def load_sample_data():
    """Load sample data for demonstration purposes"""
    if st.session_state.get('data_loaded', False):
        return
    
    # Sample clients data
    st.session_state['clients'] = [
        {
            "id": 1, 
            "name": "Johnson Corporation", 
            "contact": "john.smith@johnsoncorp.com",
            "phone": "+1-555-0123",
            "address": "123 Business Ave, New York, NY 10001",
            "status": "Active",
            "created_date": datetime.now() - timedelta(days=90)
        },
        {
            "id": 2, 
            "name": "Smith & Associates LLC", 
            "contact": "info@smithlaw.com",
            "phone": "+1-555-0456",
            "address": "456 Law Street, Boston, MA 02101",
            "status": "Active",
            "created_date": datetime.now() - timedelta(days=120)
        },
        {
            "id": 3, 
            "name": "Tech Innovations Inc", 
            "contact": "legal@techinnovations.com",
            "phone": "+1-555-0789",
            "address": "789 Innovation Blvd, San Francisco, CA 94105",
            "status": "Pending",
            "created_date": datetime.now() - timedelta(days=30)
        },
        {
            "id": 4,
            "name": "Global Manufacturing Ltd",
            "contact": "contracts@globalmanuf.com",
            "phone": "+1-555-0321",
            "address": "321 Industrial Way, Detroit, MI 48201",
            "status": "Active",
            "created_date": datetime.now() - timedelta(days=200)
        }
    ]
    
    # Sample matters/cases data
    st.session_state['matters'] = [
        {
            "id": 1, 
            "title": "Johnson Corporation Merger", 
            "client_id": 1, 
            "status": "Active",
            "priority": "High",
            "assigned_attorney": "Sarah Williams",
            "created_date": datetime.now() - timedelta(days=45),
            "description": "Corporate merger and acquisition legal services"
        },
        {
            "id": 2, 
            "title": "Patent Filing - AI Technology", 
            "client_id": 3, 
            "status": "In Progress",
            "priority": "Medium",
            "assigned_attorney": "Michael Chen",
            "created_date": datetime.now() - timedelta(days=30),
            "description": "Patent application for innovative AI technology"
        },
        {
            "id": 3, 
            "title": "Contract Review - Service Agreement", 
            "client_id": 2, 
            "status": "Under Review",
            "priority": "Low",
            "assigned_attorney": "Jennifer Davis",
            "created_date": datetime.now() - timedelta(days=15),
            "description": "Review and negotiation of service agreements"
        },
        {
            "id": 4,
            "title": "Employment Law Consultation",
            "client_id": 4,
            "status": "Completed",
            "priority": "Medium",
            "assigned_attorney": "Robert Johnson",
            "created_date": datetime.now() - timedelta(days=60),
            "description": "Employment law compliance and policy review"
        }
    ]
    
    # Sample documents data
    st.session_state['documents'] = [
        {
            "id": 1, 
            "name": "Merger Agreement Draft v2.1.pdf", 
            "matter_id": 1, 
            "type": "Contract",
            "size": "2.4 MB",
            "uploaded_by": "Sarah Williams",
            "upload_date": datetime.now() - timedelta(days=5),
            "status": "Final",
            "version": "2.1"
        },
        {
            "id": 2, 
            "name": "Patent Application Form.docx", 
            "matter_id": 2, 
            "type": "Application",
            "size": "1.8 MB",
            "uploaded_by": "Michael Chen",
            "upload_date": datetime.now() - timedelta(days=10),
            "status": "Draft",
            "version": "1.0"
        },
        {
            "id": 3, 
            "name": "Service Agreement Template.pdf", 
            "matter_id": 3, 
            "type": "Template",
            "size": "945 KB",
            "uploaded_by": "Jennifer Davis",
            "upload_date": datetime.now() - timedelta(days=3),
            "status": "Review",
            "version": "3.2"
        },
        {
            "id": 4,
            "name": "Employment Policy Manual.docx",
            "matter_id": 4,
            "type": "Policy",
            "size": "3.1 MB",
            "uploaded_by": "Robert Johnson",
            "upload_date": datetime.now() - timedelta(days=20),
            "status": "Final",
            "version": "1.5"
        }
    ]
    
    # Sample tasks data
    st.session_state['tasks'] = [
        {
            "id": 1, 
            "title": "Review merger documentation", 
            "matter_id": 1,
            "assigned_to": "Sarah Williams",
            "due_date": datetime.now() + timedelta(days=3),
            "priority": "High",
            "status": "In Progress",
            "description": "Complete review of all merger documents and identify any issues"
        },
        {
            "id": 2, 
            "title": "File patent with USPTO", 
            "matter_id": 2,
            "assigned_to": "Michael Chen",
            "due_date": datetime.now() + timedelta(days=7),
            "priority": "Medium",
            "status": "Pending",
            "description": "Submit patent application to USPTO with all required documentation"
        },
        {
            "id": 3, 
            "title": "Schedule client meeting", 
            "matter_id": 3,
            "assigned_to": "Jennifer Davis",
            "due_date": datetime.now() + timedelta(days=1),
            "priority": "Low",
            "status": "To Do",
            "description": "Coordinate meeting with client to discuss contract terms"
        },
        {
            "id": 4,
            "title": "Prepare litigation strategy",
            "matter_id": 1,
            "assigned_to": "Sarah Williams",
            "due_date": datetime.now() + timedelta(days=14),
            "priority": "High",
            "status": "To Do",
            "description": "Develop comprehensive litigation strategy for potential disputes"
        }
    ]
    
    # Sample time entries for billing
    st.session_state['time_entries'] = [
        {
            "id": 1,
            "matter_id": 1,
            "attorney": "Sarah Williams",
            "date": datetime.now() - timedelta(days=1),
            "hours": 3.5,
            "rate": 450.00,
            "description": "Document review and analysis",
            "billable": True
        },
        {
            "id": 2,
            "matter_id": 2,
            "attorney": "Michael Chen",
            "date": datetime.now() - timedelta(days=2),
            "hours": 2.0,
            "rate": 400.00,
            "description": "Patent research and preparation",
            "billable": True
        },
        {
            "id": 3,
            "matter_id": 3,
            "attorney": "Jennifer Davis",
            "date": datetime.now() - timedelta(days=1),
            "hours": 1.5,
            "rate": 375.00,
            "description": "Client consultation",
            "billable": True
        }
    ]
    
    # Sample invoices
    st.session_state['invoices'] = [
        {
            "id": "INV-2024-001",
            "client_id": 1,
            "matter_id": 1,
            "amount": 15750.00,
            "status": "Paid",
            "issue_date": datetime.now() - timedelta(days=30),
            "due_date": datetime.now() - timedelta(days=0),
            "paid_date": datetime.now() - timedelta(days=5)
        },
        {
            "id": "INV-2024-002",
            "client_id": 2,
            "matter_id": 3,
            "amount": 8500.00,
            "status": "Outstanding",
            "issue_date": datetime.now() - timedelta(days=15),
            "due_date": datetime.now() + timedelta(days=15),
            "paid_date": None
        },
        {
            "id": "INV-2024-003",
            "client_id": 3,
            "matter_id": 2,
            "amount": 12000.00,
            "status": "Draft",
            "issue_date": datetime.now(),
            "due_date": datetime.now() + timedelta(days=30),
            "paid_date": None
        }
    ]
    
    # Sample calendar events
    st.session_state['calendar_events'] = [
        {
            "id": 1,
            "title": "Client Meeting - Johnson Corp",
            "date": datetime.now() + timedelta(days=2),
            "time": "10:00 AM",
            "duration": 60,
            "type": "Meeting",
            "matter_id": 1,
            "attendees": ["Sarah Williams", "John Smith"]
        },
        {
            "id": 2,
            "title": "Court Hearing - Patent Case",
            "date": datetime.now() + timedelta(days=7),
            "time": "2:00 PM",
            "duration": 120,
            "type": "Court",
            "matter_id": 2,
            "attendees": ["Michael Chen"]
        },
        {
            "id": 3,
            "title": "Document Review Session",
            "date": datetime.now() + timedelta(days=1),
            "time": "9:00 AM",
            "duration": 180,
            "type": "Work",
            "matter_id": 3,
            "attendees": ["Jennifer Davis", "Legal Assistant"]
        }
    ]
    
    # Sample notifications
    st.session_state['notifications'] = [
        {
            "id": 1,
            "title": "New Document Uploaded",
            "message": "Merger Agreement v2.1 has been uploaded to Johnson Corporation case",
            "type": "info",
            "timestamp": datetime.now() - timedelta(hours=2),
            "read": False
        },
        {
            "id": 2,
            "title": "Task Due Tomorrow",
            "message": "Client meeting scheduling task is due tomorrow",
            "type": "warning",
            "timestamp": datetime.now() - timedelta(hours=4),
            "read": False
        },
        {
            "id": 3,
            "title": "Invoice Payment Received",
            "message": "Payment received for INV-2024-001 from Johnson Corporation",
            "type": "success",
            "timestamp": datetime.now() - timedelta(days=1),
            "read": True
        }
    ]
    
    # Mark data as loaded
    st.session_state['data_loaded'] = True

def save_session_data():
    """Save session data to local storage (optional feature)"""
    try:
        data = {
            'clients': st.session_state.get('clients', []),
            'matters': st.session_state.get('matters', []),
            'documents': st.session_state.get('documents', []),
            'tasks': st.session_state.get('tasks', []),
            'time_entries': st.session_state.get('time_entries', []),
            'invoices': st.session_state.get('invoices', [])
        }
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        with open('data/session_data.json', 'w') as f:
            json.dump(data, f, default=str, indent=2)
            
        return True
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False

def load_session_data():
    """Load session data from local storage (optional feature)"""
    try:
        if os.path.exists('data/session_data.json'):
            with open('data/session_data.json', 'r') as f:
                data = json.load(f)
            
            for key, value in data.items():
                st.session_state[key] = value
            
            return True
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return False

def reset_session_data():
    """Reset all session data to defaults"""
    keys_to_reset = [
        'clients', 'matters', 'documents', 'tasks', 
        'time_entries', 'invoices', 'calendar_events', 
        'notifications', 'data_loaded'
    ]
    
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    
    # Reinitialize
    initialize_session_state()
    load_sample_data()

def get_client_by_id(client_id):
    """Get client data by ID"""
    clients = st.session_state.get('clients', [])
    return next((client for client in clients if client['id'] == client_id), None)

def get_matter_by_id(matter_id):
    """Get matter data by ID"""
    matters = st.session_state.get('matters', [])
    return next((matter for matter in matters if matter['id'] == matter_id), None)

def get_document_by_id(document_id):
    """Get document data by ID"""
    documents = st.session_state.get('documents', [])
    return next((doc for doc in documents if doc['id'] == document_id), None)

def add_notification(title, message, notification_type="info"):
    """Add a new notification to the session"""
    if 'notifications' not in st.session_state:
        st.session_state['notifications'] = []
    
    new_notification = {
        "id": len(st.session_state['notifications']) + 1,
        "title": title,
        "message": message,
        "type": notification_type,
        "timestamp": datetime.now(),
        "read": False
    }
    
    st.session_state['notifications'].insert(0, new_notification)

def get_unread_notifications_count():
    """Get count of unread notifications"""
    notifications = st.session_state.get('notifications', [])
    return len([n for n in notifications if not n.get('read', True)])

def mark_notification_read(notification_id):
    """Mark a notification as read"""
    notifications = st.session_state.get('notifications', [])
    for notification in notifications:
        if notification['id'] == notification_id:
            notification['read'] = True
            break
