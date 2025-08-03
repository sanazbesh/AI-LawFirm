import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import time
import pyrebase

# Configure page
st.set_page_config(
    page_title="LegalDoc Pro - Document Management Dashboard",
    page_icon="⚖️",
    layout="wide"
)

# Firebase Configuration
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

# Initialize session state
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'clients' not in st.session_state:
    st.session_state.clients = []
if 'time_entries' not in st.session_state:
    st.session_state.time_entries = []
if 'user' not in st.session_state:
    st.session_state.user = None

# Firebase Authentication Functions
def initialize_user_data(email):
    """Initialize user data if it doesn't exist"""
    try:
        user_data = db.child("users").child(email.replace(".", "_")).get().val()
        if not user_data:
            create_user_subscription(email, "trial")
    except:
        create_user_subscription(email, "trial")

def create_user_subscription(email, plan_type):
    """Create user subscription data"""
    user_key = email.replace(".", "_")
    
    plans = {
        "trial": {
            "document_limit": 25,
            "client_limit": 10,
            "storage_limit_mb": 100,
            "has_advanced_reports": False,
            "has_time_tracking": True
        },
        "basic": {
            "document_limit": 100,
            "client_limit": 50,
            "storage_limit_mb": 500,
            "has_advanced_reports": False,
            "has_time_tracking": True
        },
        "premium": {
            "document_limit": "unlimited",
            "client_limit": "unlimited",
            "storage_limit_mb": "unlimited",
            "has_advanced_reports": True,
            "has_time_tracking": True
        }
    }
    
    user_data = {
        "email": email,
        "subscription_type": plan_type,
        "subscription_status": "active" if plan_type != "trial" else "trial",
        "payment_date": datetime.now().isoformat(),
        "usage_limits": plans.get(plan_type, plans["trial"]),
        "current_usage": {
            "documents_count": 0,
            "clients_count": 0,
            "storage_used_mb": 0,
            "last_reset_date": datetime.now().replace(day=1).isoformat()
        }
    }
    
    db.child("users").child(user_key).set(user_data)

def check_usage_limits(email, action_type="document"):
    """Check if user can perform action based on their plan"""
    user_key = email.replace(".", "_")
    
    try:
        user_data = db.child("users").child(user_key).get().val()
        
        if not user_data:
            return False, "No subscription found. Please contact support."
        
        if user_data.get('subscription_status') not in ['active', 'trial']:
            return False, "Subscription expired. Please upgrade your plan."
        
        usage_limits = user_data.get('usage_limits', {})
        current_usage = user_data.get('current_usage', {})
        
        if action_type == "document":
            limit = usage_limits.get('document_limit', 0)
            current = current_usage.get('documents_count', 0)
            
            if limit != "unlimited" and current >= limit:
                plan_type = user_data.get('subscription_type', 'trial')
                return False, f"Document limit of {limit} reached for {plan_type} plan. Please upgrade to continue."
        
        elif action_type == "client":
            limit = usage_limits.get('client_limit', 0)
            current = current_usage.get('clients_count', 0)
            
            if limit != "unlimited" and current >= limit:
                plan_type = user_data.get('subscription_type', 'trial')
                return False, f"Client limit of {limit} reached for {plan_type} plan. Please upgrade to continue."
        
        return True, "Access granted"
        
    except Exception as e:
        return False, f"Error checking limits: {str(e)}"

def increment_usage(email, action_type="document"):
    """Increment user's usage count"""
    user_key = email.replace(".", "_")
    
    try:
        if action_type == "document":
            current_count = db.child("users").child(user_key).child("current_usage").child("documents_count").get().val() or 0
            db.child("users").child(user_key).child("current_usage").child("documents_count").set(current_count + 1)
        elif action_type == "client":
            current_count = db.child("users").child(user_key).child("current_usage").child("clients_count").get().val() or 0
            db.child("users").child(user_key).child("current_usage").child("clients_count").set(current_count + 1)
    except Exception as e:
        st.error(f"Error updating usage: {str(e)}")

def get_user_info(email):
    """Get user subscription info"""
    user_key = email.replace(".", "_")
    
    try:
        user_data = db.child("users").child(user_key).get().val()
        return user_data
    except:
        return None

def show_usage_info():
    """Display user's current usage and limits"""
    if is_logged_in():
        email = st.session_state['user']['email']
        user_info = get_user_info(email)
        
        if user_info:
            plan = user_info.get('subscription_type', 'trial')
            status = user_info.get('subscription_status', 'trial')
            usage_limits = user_info.get('usage_limits', {})
            current_usage = user_info.get('current_usage', {})
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Plan", plan.title())
            
            with col2:
                doc_limit = usage_limits.get('document_limit', 0)
                doc_current = current_usage.get('documents_count', 0)
                if doc_limit == "unlimited":
                    st.metric("Documents", f"{doc_current}/∞")
                else:
                    st.metric("Documents", f"{doc_current}/{doc_limit}")
            
            with col3:
                client_limit = usage_limits.get('client_limit', 0)
                client_current = current_usage.get('clients_count', 0)
                if client_limit == "unlimited":
                    st.metric("Clients", f"{client_current}/∞")
                else:
                    st.metric("Clients", f"{client_current}/{client_limit}")
            
            with col4:
                st.metric("Status", status.title())
            
            if status == "trial":
                st.warning("⚠️ You're on a trial plan. Upgrade for more features!")

def is_logged_in():
    return st.session_state.get('user') is not None

def show_login():
    """Display login/signup interface"""
    st.markdown("""
    <div style="text-align: center; padding: 50px 0;">
        <h1>⚖️ LegalDoc Pro</h1>
        <h3>Document Management for Small Law Firms</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                login_button = st.form_submit_button("Login", use_container_width=True)
                
                if login_button and email and password:
                    try:
                        user = auth.sign_in_with_email_and_password(email, password)
                        st.session_state['user'] = user
                        initialize_user_data(email)
                        st.success("Logged in successfully!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error("Invalid email or password. Please try again.")
        
        with tab2:
            with st.form("signup_form"):
                new_email = st.text_input("Email", placeholder="Enter your email", key="signup_email")
                new_password = st.text_input("Password", type="password", placeholder="Create a password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                signup_button = st.form_submit_button("Create Account", use_container_width=True)
                
                if signup_button and new_email and new_password:
                    if new_password != confirm_password:
                        st.error("Passwords do not match!")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long!")
                    else:
                        try:
                            user = auth.create_user_with_email_and_password(new_email, new_password)
                            st.session_state['user'] = user
                            create_user_subscription(new_email, "trial")
                            st.success("Account created successfully! You're on a free trial.")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            if "EMAIL_EXISTS" in str(e):
                                st.error("An account with this email already exists. Please login instead.")
                            elif "WEAK_PASSWORD" in str(e):
                                st.error("Password is too weak. Please choose a stronger password.")
                            else:
                                st.error("Account creation failed. Please try again.")

def logout():
    """Logout function"""
    st.session_state.user = None
    st.session_state.documents = []
    st.session_state.clients = []
    st.session_state.time_entries = []
    st.rerun()

# Check if user is logged in
if not is_logged_in():
    show_login()
    st.stop()

# Load sample data for demo (in production, this would come from the database)
if not st.session_state.documents:
    st.session_state.documents = [
        {
            'id': 1,
            'name': 'Divorce_Settlement_Agreement_Smith.pdf',
            'client': 'John Smith',
            'matter': 'Divorce Proceedings',
            'type': 'Settlement Agreement',
            'date_uploaded': '2024-01-15',
            'file_size': '2.1 MB',
            'status': 'Final',
            'content': None
        },
        {
            'id': 2,
            'name': 'LLC_Formation_TechCorp.pdf',
            'client': 'TechCorp LLC',
            'matter': 'Business Formation',
            'type': 'Articles of Incorporation',
            'date_uploaded': '2024-01-20',
            'file_size': '1.8 MB',
            'status': 'Draft',
            'content': None
        },
        {
            'id': 3,
            'name': 'Child_Custody_Motion_Johnson.pdf',
            'client': 'Mary Johnson',
            'matter': 'Child Custody',
            'type': 'Court Motion',
            'date_uploaded': '2024-01-25',
            'file_size': '3.2 MB',
            'status': 'Filed',
            'content': None
        },
        {
            'id': 4,
            'name': 'Prenuptial_Agreement_Williams.pdf',
            'client': 'Sarah Williams',
            'matter': 'Prenuptial Agreement',
            'type': 'Contract',
            'date_uploaded': '2024-01-30',
            'file_size': '1.5 MB',
            'status': 'Under Review',
            'content': None
        },
        {
            'id': 5,
            'name': 'Business_Partnership_Agreement_ABC.pdf',
            'client': 'ABC Partners',
            'matter': 'Partnership Formation',
            'type': 'Partnership Agreement',
            'date_uploaded': '2024-02-05',
            'file_size': '2.8 MB',
            'status': 'Final',
            'content': None
        }
    ]

if not st.session_state.clients:
    st.session_state.clients = [
        {'name': 'John Smith', 'type': 'Individual', 'active_matters': 1},
        {'name': 'TechCorp LLC', 'type': 'Business', 'active_matters': 2},
        {'name': 'Mary Johnson', 'type': 'Individual', 'active_matters': 1},
        {'name': 'Sarah Williams', 'type': 'Individual', 'active_matters': 1},
        {'name': 'ABC Partners', 'type': 'Business', 'active_matters': 1}
    ]

# Sidebar
st.sidebar.title("⚖️ LegalDoc Pro")
st.sidebar.markdown("*Document Management for Small Law Firms*")

# User info
if is_logged_in():
    user_email = st.session_state['user']['email']
    st.sidebar.markdown(f"Welcome, **{user_email}**!")
    
    # Usage info in sidebar
    user_info = get_user_info(user_email)
    if user_info:
        plan = user_info.get('subscription_type', 'trial')
        st.sidebar.markdown(f"Plan: **{plan.title()}**")
        
        if plan == "trial":
            st.sidebar.warning("Trial Plan Active")
            if st.sidebar.button("🚀 Upgrade Plan"):
                st.sidebar.markdown('[Upgrade Now](https://prolexisanalytics.com/pricing)')

# Logout button
if st.sidebar.button("🚪 Logout"):
    logout()

# Navigation
page = st.sidebar.selectbox(
    "Navigate",
    ["Dashboard", "Document Management", "Client Management", "Time Tracking", "Reports"]
)

# Main content
if page == "Dashboard":
    st.title("📊 Dashboard Overview")
    
    # Show usage info
    show_usage_info()
    st.divider()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Documents", len(st.session_state.documents), "5 this week")
    
    with col2:
        st.metric("Active Clients", len(st.session_state.clients), "1 new")
    
    with col3:
        st.metric("Pending Reviews", 2, "-1")
    
    with col4:
        st.metric("Hours This Week", 42.5, "8.5")
    
    st.divider()
    
    # Recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Recent Documents")
        recent_docs = sorted(st.session_state.documents, key=lambda x: x['date_uploaded'], reverse=True)[:5]
        for doc in recent_docs:
            with st.container():
                st.markdown(f"**{doc['name']}**")
                st.markdown(f"Client: {doc['client']} | {doc['date_uploaded']}")
                st.markdown("---")
    
    with col2:
        st.subheader("⏰ Today's Schedule")
        st.markdown("**9:00 AM** - Client consultation (Smith)")
        st.markdown("**11:30 AM** - Document review (TechCorp)")
        st.markdown("**2:00 PM** - Court filing deadline")
        st.markdown("**4:00 PM** - Settlement negotiation call")

elif page == "Document Management":
    st.title("📁 Document Management")
    
    # Search and filter section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("🔍 Search documents", placeholder="Enter keywords...")
    
    with col2:
        client_filter = st.selectbox("Filter by Client", ["All"] + [client['name'] for client in st.session_state.clients])
    
    with col3:
        doc_type_filter = st.selectbox("Filter by Type", ["All", "Settlement Agreement", "Articles of Incorporation", "Court Motion", "Contract", "Partnership Agreement", "Lease Agreement", "Court Filing", "Employment Contract", "Court Complaint"])
    
    # Upload section
    st.subheader("📤 Upload New Document")
    
    # Check limits before allowing upload
    user_email = st.session_state['user']['email']
    can_upload, limit_message = check_usage_limits(user_email, "document")
    
    if not can_upload:
        st.error(limit_message)
        st.info("Please upgrade your plan to upload more documents.")
    else:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            uploaded_file = st.file_uploader("Choose file", type=['pdf', 'docx', 'txt'])
        
        with col2:
            upload_client = st.selectbox("Select Client", [client['name'] for client in st.session_state.clients])
        
        with col3:
            upload_matter = st.text_input("Matter Description")
        
        if uploaded_file and upload_client and upload_matter:
            if st.button("Upload Document"):
                file_content = uploaded_file.read()
                
                file_size_kb = len(file_content) / 1024
                if file_size_kb > 1024:
                    file_size_str = f"{file_size_kb / 1024:.1f} MB"
                else:
                    file_size_str = f"{file_size_kb:.1f} KB"
                
                doc_type = "General Document"
                filename_lower = uploaded_file.name.lower()
                if "contract" in filename_lower or "agreement" in filename_lower:
                    doc_type = "Contract"
                elif "motion" in filename_lower or "complaint" in filename_lower:
                    doc_type = "Court Motion"
                elif "llc" in filename_lower or "incorporation" in filename_lower:
                    doc_type = "Articles of Incorporation"
                elif "lease" in filename_lower:
                    doc_type = "Lease Agreement"
                elif "employment" in filename_lower:
                    doc_type = "Employment Contract"
                
                new_doc = {
                    'id': len(st.session_state.documents) + 1,
                    'name': uploaded_file.name,
                    'client': upload_client,
                    'matter': upload_matter,
                    'type': doc_type,
                    'date_uploaded': datetime.now().strftime('%Y-%m-%d'),
                    'file_size': file_size_str,
                    'status': 'New',
                    'content': file_content
                }
                st.session_state.documents.append(new_doc)
                increment_usage(user_email, "document")
                st.success(f"Document '{uploaded_file.name}' uploaded successfully!")
                st.rerun()
    
    st.divider()
    
    # Document list
    st.subheader("📋 Document Library")
    
    # Filter documents
    filtered_docs = st.session_state.documents
    
    if search_term:
        filtered_docs = [doc for doc in filtered_docs if search_term.lower() in doc['name'].lower() or search_term.lower() in doc['client'].lower()]
    
    if client_filter != "All":
        filtered_docs = [doc for doc in filtered_docs if doc['client'] == client_filter]
    
    if doc_type_filter != "All":
        filtered_docs = [doc for doc in filtered_docs if doc['type'] == doc_type_filter]
    
    # Display documents
    for doc in filtered_docs:
        with st.expander(f"{doc['name']} - {doc['client']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Client:** {doc['client']}")
                st.markdown(f"**Matter:** {doc['matter']}")
                st.markdown(f"**Type:** {doc['type']}")
            
            with col2:
                st.markdown(f"**Date:** {doc['date_uploaded']}")
                st.markdown(f"**Size:** {doc['file_size']}")
                st.markdown(f"**Status:** {doc['status']}")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("📖 View", key=f"view_{doc['id']}"):
                    if doc.get('content'):
                        st.info("Document content loaded successfully!")
                    else:
                        st.info("This is a demo document - no content to display.")
            with col2:
                if st.button("📝 Edit", key=f"edit_{doc['id']}"):
                    st.info("Edit functionality would open here.")
            with col3:
                if st.button("📥 Download", key=f"download_{doc['id']}"):
                    if doc.get('content'):
                        st.download_button(
                            label="Click to Download",
                            data=doc['content'],
                            file_name=doc['name'],
                            mime="application/pdf",
                            key=f"dl_{doc['id']}"
                        )
                    else:
                        st.info("Demo document - no file to download.")
            with col4:
                if st.button("🗑️ Delete", key=f"delete_{doc['id']}"):
                    st.session_state.documents = [d for d in st.session_state.documents if d['id'] != doc['id']]
                    st.success(f"Document '{doc['name']}' deleted!")
                    st.rerun()

elif page == "Client Management":
    st.title("👥 Client Management")
    
    # Check limits before allowing new client
    user_email = st.session_state['user']['email']
    can_add_client, limit_message = check_usage_limits(user_email, "client")
    
    # Add new client
    st.subheader("➕ Add New Client")
    
    if not can_add_client:
        st.error(limit_message)
        st.info("Please upgrade your plan to add more clients.")
    else:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            new_client_name = st.text_input("Client Name")
        
        with col2:
            new_client_type = st.selectbox("Client Type", ["Individual", "Business"])
        
        with col3:
            st.write("")  # Spacing
            if st.button("Add Client") and new_client_name:
                new_client = {
                    'name': new_client_name,
                    'type': new_client_type,
                    'active_matters': 0
                }
                st.session_state.clients.append(new_client)
                increment_usage(user_email, "client")
                st.success(f"Client '{new_client_name}' added successfully!")
                st.rerun()
    
    st.divider()
    
    # Client list
    st.subheader("📋 Client List")
    
    df = pd.DataFrame(st.session_state.clients)
    st.dataframe(df, use_container_width=True)
    
    # Client details
    if st.session_state.clients:
        selected_client = st.selectbox("Select client for details", [client['name'] for client in st.session_state.clients])
        
        if selected_client:
            client_docs = [doc for doc in st.session_state.documents if doc['client'] == selected_client]
            
            st.subheader(f"Documents for {selected_client}")
            
            if client_docs:
                for doc in client_docs:
                    st.markdown(f"• **{doc['name']}** ({doc['type']}) - {doc['status']}")
            else:
                st.info("No documents found for this client.")

elif page == "Time Tracking":
    st.title("⏱️ Time Tracking")
    
    # Check if time tracking is available
    user_email = st.session_state['user']['email']
    user_info = get_user_info(user_email)
    
    if user_info and not user_info.get('usage_limits', {}).get('has_time_tracking', False):
        st.error("Time tracking is not available in your current plan.")
        st.info("Please upgrade to access time tracking features.")
        st.stop()  # This stops Streamlit execution
    
    # Active timer
    st.subheader("🟢 Active Timer")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        timer_client = st.selectbox("Client", [client['name'] for client in st.session_state.clients])
    
    with col2:
        timer_matter = st.text_input("Matter/Task")
    
    with col3:
        timer_rate = st.number_input("Hourly Rate ($)", min_value=0.0, value=250.0, step=25.0)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("▶️ Start Timer"):
            st.success("Timer started!")
    
    with col2:
        if st.button("⏹️ Stop Timer"):
            st.info("Timer stopped. 1.5 hours recorded.")
    
    st.divider()
    
    # Manual time entry
    st.subheader("📝 Manual Time Entry")
    
    col1, col2 = st.columns(2)
    
    with col1:
        entry_date = st.date_input("Date")
        entry_client = st.selectbox("Client ", [client['name'] for client in st.session_state.clients])
        entry_hours = st.number_input("Hours", min_value=0.0, max_value=24.0, value=1.0, step=0.25)
    
    with col2:
        entry_description = st.text_area("Description")
        entry_rate = st.number_input("Rate ($)", min_value=0.0, value=250.0, step=25.0)
    
    if st.button("Add Time Entry"):
        if entry_client and entry_description:
            new_entry = {
                'date': entry_date,
                'client': entry_client,
                'hours': entry_hours,
                'description': entry_description,
                'rate': entry_rate,
                'amount': entry_hours * entry_rate
            }
            st.session_state.time_entries.append(new_entry)
            st.success("Time entry added successfully!")
            st.rerun()
    
    st.divider()
    
    # Recent time entries
    st.subheader("📋 Recent Time Entries")
    
    if st.session_state.time_entries:
        df = pd.DataFrame(st.session_state.time_entries)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No time entries yet.")

elif page == "Reports":
    st.title("📊 Reports & Analytics")
    
    # Check if advanced reports are available
    user_email = st.session_state['user']['email']
    user_info = get_user_info(user_email)
    has_advanced_reports = user_info and user_info.get('usage_limits', {}).get('has_advanced_reports', False)
    
    if not has_advanced_reports:
        st.warning("⚠️ Advanced reports are available in Pro plans only. Showing basic reports.")
    
    # Date range selector
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
    
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    st.divider()
    
    # Document statistics
    st.subheader("📁 Document Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        doc_types = {}
        for doc in st.session_state.documents:
            doc_types[doc['type']] = doc_types.get(doc['type'], 0) + 1
        
        st.bar_chart(doc_types)
    
    with col2:
        client_docs = {}
        for doc in st.session_state.documents:
            client_docs[doc['client']] = client_docs.get(doc['client'], 0) + 1
        
        st.bar_chart(client_docs)
    
    if has_advanced_reports:
        st.divider()
        st.subheader("📈 Advanced Analytics")
        st.info("Advanced analytics features would appear here for Pro users.")
    
    st.divider()
    
    # Time tracking summary
    st.subheader("⏱️ Time Tracking Summary")
    
    if st.session_state.time_entries:
        total_hours = sum(entry['hours'] for entry in st.session_state.time_entries)
        total_revenue = sum(entry['amount'] for entry in st.session_state.time_entries)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Hours", f"{total_hours:.1f}")
        
        with col2:
            st.metric("Total Revenue", f"${total_revenue:,.2f}")
        
        with col3:
            st.metric("Average Rate", f"${total_revenue/total_hours:.2f}/hr" if total_hours > 0 else "$0/hr")
    else:
        st.info("No time entries to analyze yet.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("*LegalDoc Pro v1.0*")
st.sidebar.markdown("*Simplifying legal document management*")
