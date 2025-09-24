import streamlit as st
import time
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class UserSession:
    user_id: str
    email: str
    role: str
    permissions: List[str]
    login_time: datetime
    last_activity: datetime
    session_id: str
    ip_address: Optional[str] = None

class AuthService:
    def __init__(self):
        self.session_timeout = 3600  # 1 hour in seconds
        self.max_failed_attempts = 5
        self.lockout_duration = 1800  # 30 minutes in seconds
        
        # Initialize demo users if not in session state
        if 'demo_users' not in st.session_state:
            self._initialize_demo_users()
        
        # Initialize session tracking
        if 'user_sessions' not in st.session_state:
            st.session_state.user_sessions = {}
        
        # Initialize failed attempts tracking
        if 'failed_attempts' not in st.session_state:
            st.session_state.failed_attempts = {}
    
    def _initialize_demo_users(self):
        """Initialize demo users with different roles and permissions."""
        demo_users = {
            'demo.partner@legaldocpro.com': {
                'password': self._hash_password('demo123'),
                'role': 'partner',
                'name': 'John Partner',
                'permissions': ['read', 'write', 'delete', 'admin', 'billing', 'manage_users', 'ai_insights', 'integrations', 'system_settings'],
                'created_date': datetime.now(),
                'last_login': None,
                'is_active': True,
                'two_factor_enabled': False
            },
            'demo.associate@legaldocpro.com': {
                'password': self._hash_password('demo123'),
                'role': 'associate',
                'name': 'Sarah Associate',
                'permissions': ['read', 'write', 'time_tracking', 'ai_insights'],
                'created_date': datetime.now(),
                'last_login': None,
                'is_active': True,
                'two_factor_enabled': False
            },
            'demo.paralegal@legaldocpro.com': {
                'password': self._hash_password('demo123'),
                'role': 'paralegal',
                'name': 'Mike Paralegal',
                'permissions': ['read', 'time_tracking', 'document_management'],
                'created_date': datetime.now(),
                'last_login': None,
                'is_active': True,
                'two_factor_enabled': False
            },
            'demo.admin@legaldocpro.com': {
                'password': self._hash_password('demo123'),
                'role': 'admin',
                'name': 'Admin User',
                'permissions': ['read', 'write', 'delete', 'admin', 'billing', 'manage_users', 'ai_insights', 'integrations', 'system_settings', 'user_management'],
                'created_date': datetime.now(),
                'last_login': None,
                'is_active': True,
                'two_factor_enabled': False
            },
            'legal@acme.com': {
                'password': self._hash_password('demo123'),
                'role': 'client',
                'name': 'ACME Corporation',
                'client_id': 'client_1',
                'permissions': ['read', 'portal_access', 'document_view', 'billing_view'],
                'created_date': datetime.now(),
                'last_login': None,
                'is_active': True,
                'two_factor_enabled': False
            }
        }
        st.session_state.demo_users = demo_users
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return self._hash_password(password) == hashed_password
    
    def _is_account_locked(self, email: str) -> bool:
        """Check if an account is locked due to failed login attempts."""
        if email not in st.session_state.failed_attempts:
            return False
        
        attempts_data = st.session_state.failed_attempts[email]
        if attempts_data['count'] >= self.max_failed_attempts:
            time_since_last_attempt = (datetime.now() - attempts_data['last_attempt']).total_seconds()
            return time_since_last_attempt < self.lockout_duration
        
        return False
    
    def _record_failed_attempt(self, email: str):
        """Record a failed login attempt."""
        if email not in st.session_state.failed_attempts:
            st.session_state.failed_attempts[email] = {'count': 0, 'last_attempt': datetime.now()}
        
        st.session_state.failed_attempts[email]['count'] += 1
        st.session_state.failed_attempts[email]['last_attempt'] = datetime.now()
    
    def _reset_failed_attempts(self, email: str):
        """Reset failed attempts counter for an email."""
        if email in st.session_state.failed_attempts:
            del st.session_state.failed_attempts[email]
    
    def _create_session(self, user_data: Dict, email: str) -> UserSession:
        """Create a new user session."""
        session_id = str(uuid.uuid4())
        session = UserSession(
            user_id=email,
            email=email,
            role=user_data['role'],
            permissions=user_data['permissions'],
            login_time=datetime.now(),
            last_activity=datetime.now(),
            session_id=session_id,
            ip_address=self._get_client_ip()
        )
        
        st.session_state.user_sessions[session_id] = session
        return session
    
    def _get_client_ip(self) -> Optional[str]:
        """Get client IP address (mock implementation for demo)."""
        return "127.0.0.1"  # Mock IP for demo
    
    def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate a user with email and password."""
        # Check if account is locked
        if self._is_account_locked(email):
            return {
                'success': False,
                'message': 'Account is locked due to too many failed attempts. Try again later.',
                'locked': True
            }
        
        # Check if user exists
        if email not in st.session_state.demo_users:
            self._record_failed_attempt(email)
            return {
                'success': False,
                'message': 'Invalid email or password.',
                'user_exists': False
            }
        
        user_data = st.session_state.demo_users[email]
        
        # Check if account is active
        if not user_data.get('is_active', True):
            return {
                'success': False,
                'message': 'Account is deactivated. Contact administrator.',
                'account_inactive': True
            }
        
        # Verify password
        if not self._verify_password(password, user_data['password']):
            self._record_failed_attempt(email)
            return {
                'success': False,
                'message': 'Invalid email or password.',
                'password_incorrect': True
            }
        
        # Reset failed attempts on successful login
        self._reset_failed_attempts(email)
        
        # Update last login
        user_data['last_login'] = datetime.now()
        
        # Create session
        session = self._create_session(user_data, email)
        
        # Store user in session state
        st.session_state['user'] = {
            'email': email,
            'role': user_data['role'],
            'name': user_data['name'],
            'permissions': user_data['permissions'],
            'session_id': session.session_id,
            'client_id': user_data.get('client_id'),
            'login_time': session.login_time
        }
        
        return {
            'success': True,
            'message': f'Welcome back, {user_data["name"]}!',
            'user': st.session_state['user']
        }
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in and session is valid."""
        if 'user' not in st.session_state:
            return False
        
        user = st.session_state['user']
        session_id = user.get('session_id')
        
        if not session_id or session_id not in st.session_state.user_sessions:
            return False
        
        session = st.session_state.user_sessions[session_id]
        
        # Check session timeout
        time_since_activity = (datetime.now() - session.last_activity).total_seconds()
        if time_since_activity > self.session_timeout:
            self.logout()
            return False
        
        # Update last activity
        session.last_activity = datetime.now()
        
        return True
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current logged-in user data."""
        if not self.is_logged_in():
            return None
        return st.session_state['user']
    
    def get_user_role(self) -> Optional[str]:
        """Get the current user's role."""
        if not self.is_logged_in():
            return None
        return st.session_state.user.get('role')
    
    def get_user_permissions(self) -> List[str]:
        """Get the current user's permissions."""
        if not self.is_logged_in():
            return []
        return st.session_state.user.get('permissions', [])
    
    def has_permission(self, permission: str) -> bool:
        """Check if current user has a specific permission."""
        if not self.is_logged_in():
            return False
        
        user_permissions = self.get_user_permissions()
        return permission in user_permissions
    
    def has_any_permission(self, permissions: List[str]) -> bool:
        """Check if current user has any of the specified permissions."""
        user_permissions = self.get_user_permissions()
        return any(perm in user_permissions for perm in permissions)
    
    def has_all_permissions(self, permissions: List[str]) -> bool:
        """Check if current user has all of the specified permissions."""
        user_permissions = self.get_user_permissions()
        return all(perm in user_permissions for perm in permissions)
    
    def require_permission(self, permission: str) -> bool:
        """Require a specific permission or show access denied."""
        if not self.has_permission(permission):
            st.error(f"Access denied. Required permission: {permission}")
            return False
        return True
    
    def require_role(self, required_roles: List[str]) -> bool:
        """Require specific role(s) or show access denied."""
        user_role = self.get_user_role()
        if not user_role or user_role not in required_roles:
            st.error(f"Access denied. Required role: {', '.join(required_roles)}")
            return False
        return True
    
    def logout(self):
        """Log out the current user and clear session."""
        if 'user' in st.session_state:
            session_id = st.session_state['user'].get('session_id')
            if session_id and session_id in st.session_state.user_sessions:
                del st.session_state.user_sessions[session_id]
        
        # Clear all user-related session state
        keys_to_remove = ['user', 'current_page']
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
    
    def show_login(self):
        """Display the login interface."""
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
                self._show_staff_login()
            
            with tab2:
                self._show_client_login()
    
    def _show_staff_login(self):
        """Show staff login form."""
        st.markdown("#### Staff Authentication")
        
        with st.form("staff_login"):
            col_login1, col_login2 = st.columns(2)
            
            with col_login1:
                role = st.selectbox("Quick Select Role", ["", "partner", "associate", "paralegal", "admin"])
            
            with col_login2:
                if role:
                    default_email = f"demo.{role}@legaldocpro.com"
                else:
                    default_email = ""
            
            email = st.text_input("Email Address", value=default_email, placeholder="Enter your email address")
            password = st.text_input("Password", type="password", value="demo123" if role else "", placeholder="Enter your password")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                login_clicked = st.form_submit_button("🔐 Login", use_container_width=True, type="primary")
            
            with col_btn2:
                forgot_password = st.form_submit_button("🔑 Forgot Password?", use_container_width=True)
            
            if login_clicked:
                if not email or not password:
                    st.error("Please enter both email and password.")
                else:
                    with st.spinner("Authenticating..."):
                        result = self.authenticate_user(email, password)
                        
                        if result['success']:
                            st.success(result['message'])
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(result['message'])
                            
                            if result.get('locked'):
                                st.warning("Account locked for 30 minutes due to multiple failed attempts.")
            
            if forgot_password:
                st.info("Password reset functionality would be implemented here. For demo, use 'demo123'")
        
        # Demo credentials info
        with st.expander("🔧 Demo Credentials"):
            st.markdown("""
            **Available Demo Accounts:**
            - Partner: demo.partner@legaldocpro.com (Password: demo123)
            - Associate: demo.associate@legaldocpro.com (Password: demo123)  
            - Paralegal: demo.paralegal@legaldocpro.com (Password: demo123)
            - Admin: demo.admin@legaldocpro.com (Password: demo123)
            """)
    
    def _show_client_login(self):
        """Show client portal login form."""
        st.markdown("#### Client Portal Access")
        
        with st.form("client_login"):
            client_email = st.text_input("Client Email", 
                                       value="legal@acme.com", 
                                       placeholder="Enter your registered email")
            client_password = st.text_input("Password", 
                                          type="password", 
                                          value="demo123",
                                          placeholder="Enter your password")
            
            remember_me = st.checkbox("Remember me on this device")
            
            col_client_btn1, col_client_btn2 = st.columns(2)
            
            with col_client_btn1:
                client_login_clicked = st.form_submit_button("🚪 Access Portal", use_container_width=True, type="primary")
            
            with col_client_btn2:
                request_access = st.form_submit_button("📝 Request Access", use_container_width=True)
            
            if client_login_clicked:
                if not client_email or not client_password:
                    st.error("Please enter both email and password.")
                else:
                    with st.spinner("Verifying credentials..."):
                        result = self.authenticate_user(client_email, client_password)
                        
                        if result['success']:
                            st.success("Welcome to your client portal!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(result['message'])
            
            if request_access:
                st.info("Access request submitted. You will be contacted within 24 hours.")
        
        # Client demo info
        with st.expander("👥 Client Demo"):
            st.markdown("""
            **Demo Client Account:**
            - Email: legal@acme.com
            - Password: demo123
            - Company: ACME Corporation
            """)
    
    def render_sidebar(self):
        """Render the sidebar navigation."""
        st.sidebar.markdown("""
        <div style="background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%); color: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <h3 style="margin: 0; text-align: center;">⚖️ LegalDoc Pro</h3>
            <p style="margin: 0.5rem 0 0 0; text-align: center;">Enterprise Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        user = self.get_current_user()
        if not user:
            return
        
        user_role = user['role']
        user_email = user['email']
        user_name = user.get('name', user_email)
        
        # User info
        st.sidebar.markdown(f"**👤 {user_name}**")
        st.sidebar.markdown(f"**🎭 Role:** {user_role.title()}")
        st.sidebar.markdown(f"**📧 Email:** {user_email}")
        
        # Session info
        login_time = user.get('login_time')
        if login_time:
            session_duration = datetime.now() - login_time
            hours, remainder = divmod(int(session_duration.total_seconds()), 3600)
            minutes, _ = divmod(remainder, 60)
            st.sidebar.markdown(f"**⏱️ Session:** {hours}h {minutes}m")
        
        st.sidebar.divider()
        
        # Navigation based on role and permissions
        if user_role == 'client':
            navigation_options = self._get_client_navigation()
        else:
            navigation_options = self._get_staff_navigation()
        
        # Current page selection
        current_page = st.session_state.get('current_page', navigation_options[0])
        page = st.sidebar.selectbox("🧭 Navigate", 
                                   navigation_options,
                                   index=navigation_options.index(current_page) if current_page in navigation_options else 0)
        st.session_state['current_page'] = page
        
        st.sidebar.divider()
        
        # Quick actions
        if user_role != 'client':
            st.sidebar.markdown("**⚡ Quick Actions**")
            if st.sidebar.button("📄 New Document", use_container_width=True):
                st.session_state['quick_action'] = 'new_document'
            if st.sidebar.button("⏱️ Start Timer", use_container_width=True):
                st.session_state['quick_action'] = 'start_timer'
            if st.sidebar.button("📝 Add Note", use_container_width=True):
                st.session_state['quick_action'] = 'add_note'
            
            st.sidebar.divider()
        
        # User settings and logout
        col_settings, col_logout = st.sidebar.columns(2)
        
        with col_settings:
            if st.button("⚙️ Settings", use_container_width=True):
                st.session_state['show_user_settings'] = True
        
        with col_logout:
            if st.button("🚪 Logout", use_container_width=True):
                self.logout()
                st.rerun()
    
    def _get_staff_navigation(self) -> List[str]:
        """Get navigation options for staff users."""
        navigation = ["Executive Dashboard"]
        
        # Core features available to all staff
        navigation.extend([
            "Document Management",
            "Matter Management", 
            "Calendar & Tasks"
        ])
        
        # Permission-based features
        if self.has_permission('time_tracking'):
            navigation.append("Time & Billing")
        
        if self.has_permission('ai_insights'):
            navigation.append("AI Insights")
        
        if self.has_permission('integrations'):
            navigation.append("Integrations")
        
        if self.has_permission('admin'):
            navigation.append("Business Intelligence")
        
        if self.has_permission('system_settings'):
            navigation.append("System Settings")
        
        if self.has_permission('manage_users'):
            navigation.append("Client Portal Management")
        
        # Always available features
        navigation.extend([
            "Advanced Search",
            "Mobile App"
        ])
        
        return navigation
    
    def _get_client_navigation(self) -> List[str]:
        """Get navigation options for client users."""
        return [
            "Client Dashboard",
            "My Documents", 
            "Billing",
            "Messages",
            "Calendar",
            "Support"
        ]
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get statistics about current user sessions."""
        active_sessions = len([s for s in st.session_state.user_sessions.values() 
                              if (datetime.now() - s.last_activity).total_seconds() < self.session_timeout])
        
        total_users = len(st.session_state.demo_users)
        failed_attempts_count = sum(data['count'] for data in st.session_state.failed_attempts.values())
        
        return {
            'active_sessions': active_sessions,
            'total_users': total_users,
            'failed_attempts': failed_attempts_count,
            'session_timeout': self.session_timeout,
            'max_failed_attempts': self.max_failed_attempts
        }
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions."""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session in st.session_state.user_sessions.items():
            if (current_time - session.last_activity).total_seconds() > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del st.session_state.user_sessions[session_id]
    
    def show_user_settings(self):
        """Show user settings modal/form."""
        if st.session_state.get('show_user_settings', False):
            user = self.get_current_user()
            
            with st.form("user_settings"):
                st.markdown("#### User Settings")
                
                # User preferences
                theme = st.selectbox("Theme", ["Light", "Dark"], index=0)
                language = st.selectbox("Language", ["English", "Spanish", "French"], index=0)
                timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "CST"], index=0)
                
                # Notification preferences
                email_notifications = st.checkbox("Email Notifications", value=True)
                browser_notifications = st.checkbox("Browser Notifications", value=True)
                
                # Security settings
                if st.form_submit_button("💾 Save Settings"):
                    st.success("Settings saved successfully!")
                    st.session_state['show_user_settings'] = False
                    st.rerun()
                
                if st.form_submit_button("❌ Cancel"):
                    st.session_state['show_user_settings'] = False
                    st.rerun()
