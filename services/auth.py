import streamlit as st
import time

class AuthService:
    def is_logged_in(self):
        return st.session_state.get('user') is not None
    
    def get_user_role(self):
        if not self.is_logged_in():
            return None
        return st.session_state.user.get('role', 'associate')
    
    def has_permission(self, permission: str) -> bool:
        role = self.get_user_role()
        if not role:
            return False
        
        role_permissions = {
            'partner': ['read', 'write', 'delete', 'admin', 'billing', 'manage_users', 'ai_insights', 'integrations'],
            'associate': ['read', 'write', 'time_tracking', 'ai_insights'],
            'paralegal': ['read', 'time_tracking'],
            'client': ['read', 'portal_access']
        }
        
        return permission in role_permissions.get(role, [])
    
    def show_login(self):
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
    
    def _show_client_login(self):
        with st.form("client_login"):
            client_email = st.text_input("Client Email", value="legal@acme.com")
            client_password = st.text_input("Password", type="password", value="demo123")
            
            if st.form_submit_button("Access Portal", use_container_width=True):
                st.session_state['user'] = {
                    'email': client_email,
                    'role': 'client',
                    'client_id': 'client_1',
                    'token': 'client_token'
                }
                st.success("Welcome to your client portal!")
                time.sleep(1)
                st.rerun()
    
    def render_sidebar(self):
        st.sidebar.markdown("""
        <div style="background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%); color: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <h3 style="margin: 0; text-align: center;">⚖️ LegalDoc Pro</h3>
            <p style="margin: 0.5rem 0 0 0; text-align: center;">Enterprise Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        user_role = self.get_user_role()
        user_email = st.session_state['user']['email']
        
        st.sidebar.markdown(f"**👤 Role:** {user_role.title()}")
        st.sidebar.markdown(f"**📧 User:** {user_email}")
        
        # Navigation
        if user_role == 'client':
            navigation_options = ["Client Dashboard", "My Documents", "Billing", "Messages"]
        else:
            navigation_options = ["Executive Dashboard", "Document Management", "Matter Management", "Calendar & Tasks"]
            
            if self.has_permission('time_tracking'):
                navigation_options.append("Time & Billing")
            if self.has_permission('ai_insights'):
                navigation_options.append("AI Insights")
            if self.has_permission('integrations'):
                navigation_options.append("Integrations")
            if self.has_permission('admin'):
                navigation_options.extend(["Business Intelligence", "System Settings"])
            
            navigation_options.extend(["Advanced Search", "Mobile App"])
        
        page = st.sidebar.selectbox("🧭 Navigate", navigation_options)
        st.session_state['current_page'] = page
        
        if st.sidebar.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
