# services/auth.py - Multi-tenant subscription-based authentication
import streamlit as st
from datetime import datetime, timedelta
from enum import Enum
import uuid

class UserRole(Enum):
    SUBSCRIPTION_OWNER = "subscription_owner"    # Law firm owner who pays
    ATTORNEY = "attorney"                        # Law firm staff
    PARALEGAL = "paralegal"                      # Law firm staff  
    CLIENT = "client"                            # External clients

class PermissionLevel(Enum):
    # Subscription Owner - Full access
    OWNER_FULL = "owner_full"
    
    # Attorney permissions
    ATTORNEY_FULL = "attorney_full"              # Senior attorney
    ATTORNEY_LIMITED = "attorney_limited"        # Junior attorney
    
    # Staff permissions  
    PARALEGAL_STANDARD = "paralegal_standard"
    PARALEGAL_LIMITED = "paralegal_limited"
    
    # Client permissions
    CLIENT_FULL = "client_full"                  # Client admin
    CLIENT_LIMITED = "client_limited"            # Regular client user
    CLIENT_READONLY = "client_readonly"          # View-only access

class MultiTenantAuthService:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize multi-tenant session state"""
        if 'subscription_data' not in st.session_state:
            st.session_state.subscription_data = {}
        
        if 'organization_users' not in st.session_state:
            st.session_state.organization_users = {}
        
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        
        if 'user_data' not in st.session_state:
            st.session_state.user_data = {}
    
    def show_login(self):
        """Multi-tenant login interface"""
        st.markdown("""
        <div class="main-header">
            <h1>⚖️ LegalDoc Pro</h1>
            <p>Enterprise Legal Management Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Organization selection first
            st.subheader("Select Organization")
            org_code = st.text_input("Organization Code", 
                                    placeholder="Enter your firm's code (e.g., 'smithlaw')",
                                    help="Contact your administrator for your organization code")
            
            if org_code:
                # Validate organization exists
                if self.validate_organization(org_code):
                    st.success(f"✅ Organization: {self.get_organization_name(org_code)}")
                    
                    # Login form
                    with st.form("login_form"):
                        st.subheader("🔐 Login")
                        
                        username = st.text_input("Username")
                        password = st.text_input("Password", type="password")
                        
                        col_login1, col_login2 = st.columns(2)
                        
                        with col_login1:
                            login_button = st.form_submit_button("Login", type="primary")
                        
                        with col_login2:
                            demo_button = st.form_submit_button("Demo Login")
                        
                        if login_button or demo_button:
                            if self.authenticate_user(org_code, username, password, is_demo=demo_button):
                                st.rerun()
                            else:
                                st.error("Invalid credentials or insufficient permissions")
                
                else:
                    st.error("Organization not found. Please check your organization code.")
            
            # New subscription signup
            st.divider()
            if st.button("🚀 Start New Subscription"):
                self.show_subscription_signup()
    
    def validate_organization(self, org_code):
        """Check if organization exists and is active"""
        # Mock validation - in real app, check database
        valid_orgs = ["smithlaw", "techfirm", "legalcorp", "demo"]
        return org_code.lower() in valid_orgs
    
    def get_organization_name(self, org_code):
        """Get organization display name"""
        org_names = {
            "smithlaw": "Smith & Associates Law Firm",
            "techfirm": "TechFirm Legal Department", 
            "legalcorp": "LegalCorp International",
            "demo": "Demo Organization"
        }
        return org_names.get(org_code.lower(), "Unknown Organization")
    
    def authenticate_user(self, org_code, username, password, is_demo=False):
        """Authenticate user within their organization"""
        if is_demo:
            # Demo login - create sample user
            user_data = {
                'user_id': str(uuid.uuid4()),
                'username': 'demo_user',
                'organization_code': org_code,
                'organization_name': self.get_organization_name(org_code),
                'role': UserRole.SUBSCRIPTION_OWNER.value,
                'permission_level': PermissionLevel.OWNER_FULL.value,
                'name': 'Demo User',
                'email': f'demo@{org_code}.com',
                'is_subscription_owner': True,
                'login_time': datetime.now()
            }
        else:
            # Real authentication would check database
            user_data = self.get_user_from_db(org_code, username, password)
        
        if user_data:
            st.session_state.logged_in = True
            st.session_state.user_data = user_data
            self.load_organization_data(org_code)
            return True
        
        return False
    
    def get_user_from_db(self, org_code, username, password):
        """Mock user authentication - replace with real database query"""
        # Sample users for different organizations
        mock_users = {
            "smithlaw": {
                "owner": {
                    'user_id': str(uuid.uuid4()),
                    'username': 'owner',
                    'organization_code': 'smithlaw',
                    'organization_name': 'Smith & Associates Law Firm',
                    'role': UserRole.SUBSCRIPTION_OWNER.value,
                    'permission_level': PermissionLevel.OWNER_FULL.value,
                    'name': 'John Smith',
                    'email': 'john@smithlaw.com',
                    'is_subscription_owner': True
                },
                "attorney1": {
                    'user_id': str(uuid.uuid4()),
                    'username': 'attorney1',
                    'organization_code': 'smithlaw',
                    'organization_name': 'Smith & Associates Law Firm',
                    'role': UserRole.ATTORNEY.value,
                    'permission_level': PermissionLevel.ATTORNEY_FULL.value,
                    'name': 'Sarah Johnson',
                    'email': 'sarah@smithlaw.com',
                    'is_subscription_owner': False
                },
                "client1": {
                    'user_id': str(uuid.uuid4()),
                    'username': 'client1', 
                    'organization_code': 'smithlaw',
                    'organization_name': 'Smith & Associates Law Firm',
                    'role': UserRole.CLIENT.value,
                    'permission_level': PermissionLevel.CLIENT_FULL.value,
                    'name': 'TechCorp Admin',
                    'email': 'admin@techcorp.com',
                    'is_subscription_owner': False,
                    'client_company': 'TechCorp Inc'
                }
            }
        }
        
        org_users = mock_users.get(org_code.lower(), {})
        user = org_users.get(username.lower())
        
        if user and password:  # Mock password validation
            user['login_time'] = datetime.now()
            return user
        
        return None
    
    def load_organization_data(self, org_code):
        """Load organization-specific data and permissions"""
        # Load matters, documents, etc. filtered by organization
        if 'matters' not in st.session_state:
            st.session_state.matters = []
        
        # Filter data by organization
        user_role = st.session_state.user_data.get('role')
        user_id = st.session_state.user_data.get('user_id')
        
        # Apply role-based filtering
        if user_role == UserRole.CLIENT.value:
            # Clients only see their own matters
            client_company = st.session_state.user_data.get('client_company', '')
            st.session_state.accessible_matters = [
                m for m in st.session_state.matters 
                if getattr(m, 'client_name', '') == client_company
            ]
        else:
            # Law firm staff see all organization matters
            st.session_state.accessible_matters = st.session_state.matters
    
    def render_sidebar(self):
        """Role-based sidebar navigation"""
        user_data = st.session_state.get('user_data', {})
        user_role = user_data.get('role')
        organization_name = user_data.get('organization_name', 'Unknown')
        
        with st.sidebar:
            # Organization info
            st.markdown(f"**🏢 {organization_name}**")
            st.markdown(f"**👤 {user_data.get('name', 'User')}**")
            st.markdown(f"*{self.get_role_display_name(user_role)}*")
            
            st.divider()
            
            # Role-based navigation
            if user_role == UserRole.SUBSCRIPTION_OWNER.value:
                self.show_owner_navigation()
            elif user_role == UserRole.ATTORNEY.value:
                self.show_attorney_navigation()
            elif user_role == UserRole.PARALEGAL.value:
                self.show_staff_navigation()
            elif user_role == UserRole.CLIENT.value:
                self.show_client_navigation()
            
            st.divider()
            
            # User management (only for subscription owner)
            if user_role == UserRole.SUBSCRIPTION_OWNER.value:
                if st.button("👥 Manage Users"):
                    st.session_state['show_user_management'] = True
                    st.rerun()
            
            # Subscription info (only for owner)
            if user_data.get('is_subscription_owner', False):
                if st.button("💳 Subscription"):
                    st.session_state['show_subscription_management'] = True
                    st.rerun()
            
            # User settings
            if st.button("⚙️ Settings"):
                st.session_state['show_user_settings'] = True
                st.rerun()
            
            # Logout
            if st.button("🚪 Logout"):
                self.logout()
                st.rerun()
    
    def show_owner_navigation(self):
        """Navigation for subscription owners - full access"""
        st.markdown("### Full Platform Access")
        
        pages = [
            ("📊", "Executive Dashboard"),
            ("📁", "Document Management"), 
            ("⚖️", "Matter Management"),
            ("⏰", "Time & Billing"),
            ("🤖", "AI Insights"),
            ("📅", "Calendar & Tasks"),
            ("🔍", "Advanced Search"),
            ("🔗", "Integrations"),
            ("📱", "Mobile App"),
            ("📈", "Business Intelligence"),
            ("👥", "Client Portal Management"),
            ("⚙️", "System Settings")
        ]
        
        for icon, page_name in pages:
            if st.button(f"{icon} {page_name}", key=f"owner_nav_{page_name}"):
                st.session_state['current_page'] = page_name
                st.rerun()
    
    def show_attorney_navigation(self):
        """Navigation for attorneys - practice management access"""
        st.markdown("### Attorney Access")
        
        pages = [
            ("📊", "Executive Dashboard"),
            ("📁", "Document Management"),
            ("⚖️", "Matter Management"), 
            ("⏰", "Time & Billing"),
            ("🤖", "AI Insights"),
            ("📅", "Calendar & Tasks"),
            ("🔍", "Advanced Search"),
            ("👥", "Client Portal Management")
        ]
        
        for icon, page_name in pages:
            if st.button(f"{icon} {page_name}", key=f"attorney_nav_{page_name}"):
                st.session_state['current_page'] = page_name
                st.rerun()
    
    def show_staff_navigation(self):
        """Navigation for paralegals and staff - limited access"""
        st.markdown("### Staff Access")
        
        pages = [
            ("📁", "Document Management"),
            ("⚖️", "Matter Management"),
            ("📅", "Calendar & Tasks"),
            ("🔍", "Advanced Search")
        ]
        
        for icon, page_name in pages:
            if st.button(f"{icon} {page_name}", key=f"staff_nav_{page_name}"):
                st.session_state['current_page'] = page_name
                st.rerun()
    
    def show_client_navigation(self):
        """Navigation for clients - client portal only"""
        st.markdown("### Client Portal")
        
        client_company = st.session_state.user_data.get('client_company', '')
        if client_company:
            st.markdown(f"**Company:** {client_company}")
        
        pages = [
            ("🏠", "Client Dashboard"),
            ("📁", "My Documents"),
            ("💰", "Billing"), 
            ("📅", "Appointments"),
            ("💬", "Messages"),
            ("🤖", "Document Review")  # AI analysis for clients
        ]
        
        for icon, page_name in pages:
            if st.button(f"{icon} {page_name}", key=f"client_nav_{page_name}"):
                st.session_state['current_page'] = page_name
                st.rerun()
    
    def get_role_display_name(self, role):
        """Get user-friendly role names"""
        role_names = {
            UserRole.SUBSCRIPTION_OWNER.value: "Owner",
            UserRole.ATTORNEY.value: "Attorney",
            UserRole.PARALEGAL.value: "Paralegal", 
            UserRole.CLIENT.value: "Client"
        }
        return role_names.get(role, "User")
    
    def has_permission(self, permission):
        """Check if current user has specific permission"""
        user_data = st.session_state.get('user_data', {})
        role = user_data.get('role')
        permission_level = user_data.get('permission_level')
        
        # Define permission matrix
        permissions = {
            PermissionLevel.OWNER_FULL.value: ['all'],
            PermissionLevel.ATTORNEY_FULL.value: [
                'read_all_matters', 'write_all_matters', 'manage_clients', 
                'billing', 'time_tracking', 'ai_insights'
            ],
            PermissionLevel.ATTORNEY_LIMITED.value: [
                'read_assigned_matters', 'write_assigned_matters', 'time_tracking'
            ],
            PermissionLevel.PARALEGAL_STANDARD.value: [
                'read_assigned_matters', 'write_assigned_matters', 'document_management'
            ],
            PermissionLevel.CLIENT_FULL.value: [
                'read_own_matters', 'upload_documents', 'view_billing', 'ai_document_review'
            ],
            PermissionLevel.CLIENT_LIMITED.value: [
                'read_assigned_documents', 'view_own_billing'
            ],
            PermissionLevel.CLIENT_READONLY.value: [
                'read_assigned_documents'
            ]
        }
        
        user_permissions = permissions.get(permission_level, [])
        return 'all' in user_permissions or permission in user_permissions
    
    def show_user_management(self):
        """User management interface for subscription owners"""
        if not st.session_state.user_data.get('is_subscription_owner', False):
            st.error("Access denied. Only subscription owners can manage users.")
            return
        
        st.subheader("👥 User Management")
        
        tab1, tab2, tab3 = st.tabs(["Add User", "Manage Users", "Subscription"])
        
        with tab1:
            self.show_add_user_form()
        
        with tab2:
            self.show_user_list()
        
        with tab3:
            self.show_subscription_info()
    
    def show_add_user_form(self):
        """Form to add new users to the organization"""
        st.markdown("#### Add New User")
        
        with st.form("add_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name *")
                email = st.text_input("Email Address *")
                username = st.text_input("Username *")
            
            with col2:
                role = st.selectbox("Role *", [
                    "Attorney (Full Access)",
                    "Attorney (Limited)",
                    "Paralegal",
                    "Client (Full)",
                    "Client (Limited)",
                    "Client (Read-only)"
                ])
                
                if "Client" in role:
                    client_company = st.text_input("Client Company")
            
            if st.form_submit_button("Add User"):
                if name and email and username:
                    st.success(f"User {name} added successfully!")
                    st.info("Login credentials sent to user's email")
                else:
                    st.error("Please fill in all required fields")
    
    def show_user_list(self):
        """List all users in the organization"""
        st.markdown("#### Organization Users")
        
        # Mock user data
        users = [
            {"name": "John Smith", "role": "Owner", "email": "john@smithlaw.com", "last_login": "Today"},
            {"name": "Sarah Johnson", "role": "Attorney", "email": "sarah@smithlaw.com", "last_login": "Yesterday"},
            {"name": "TechCorp Admin", "role": "Client", "email": "admin@techcorp.com", "last_login": "2 days ago"}
        ]
        
        for user in users:
            with st.expander(f"{user['name']} ({user['role']})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Email:** {user['email']}")
                    st.write(f"**Last Login:** {user['last_login']}")
                
                with col2:
                    if st.button("Edit", key=f"edit_{user['name']}"):
                        st.info("User editing interface would appear here")
                
                with col3:
                    if user['role'] != 'Owner':  # Can't delete owner
                        if st.button("Remove", key=f"remove_{user['name']}"):
                            st.warning("Are you sure? This action cannot be undone.")
    
    def show_subscription_info(self):
        """Show subscription details and billing"""
        st.markdown("#### Subscription Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Plan", "Professional")
            st.metric("Users", "15 / 25")
            st.metric("Storage", "12.4 GB / 50 GB")
        
        with col2:
            st.metric("Monthly Cost", "$299")
            st.metric("Next Billing", "Nov 15, 2024")
            st.metric("Status", "Active")
        
        if st.button("💳 Manage Billing"):
            st.info("Billing management interface would open here")
    
    def show_subscription_signup(self):
        """New subscription signup process"""
        st.subheader("🚀 Start Your Legal Management Platform")
        
        with st.form("subscription_form"):
            st.markdown("#### Organization Information")
            col1, col2 = st.columns(2)
            
            with col1:
                firm_name = st.text_input("Law Firm/Company Name *")
                org_code = st.text_input("Choose Organization Code *", 
                                        placeholder="e.g., 'smithlaw' (used for login)")
            
            with col2:
                owner_name = st.text_input("Your Name *")
                owner_email = st.text_input("Your Email *")
            
            st.markdown("#### Subscription Plan")
            plan = st.selectbox("Choose Plan", [
                "Starter ($99/month) - 5 users, 10GB",
                "Professional ($299/month) - 25 users, 50GB", 
                "Enterprise ($599/month) - Unlimited users, 200GB"
            ])
            
            if st.form_submit_button("Create Subscription", type="primary"):
                if firm_name and org_code and owner_name and owner_email:
                    st.success("Subscription created! Check your email for login details.")
                else:
                    st.error("Please fill in all required fields")
    
    def logout(self):
        """Logout and clear session"""
        keys_to_clear = [
            'logged_in', 'user_data', 'current_page', 'subscription_data',
            'accessible_matters', 'show_user_management', 'show_subscription_management'
        ]
        
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return st.session_state.get('logged_in', False)

# Usage in main app
def get_auth_service():
    """Get the multi-tenant auth service instance"""
    return MultiTenantAuthService()
