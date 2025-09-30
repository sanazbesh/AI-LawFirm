import streamlit as st
import pandas as pd
from datetime import datetime

def show():
    # Professional header styling
    st.markdown("""
    <style>
    /* Match main app background */
    .stApp {
        background: linear-gradient(135deg, 
            #1a0b2e 0%,
            #2d1b4e 15%,
            #1e3a8a 35%,
            #0f172a 50%,
            #1e3a8a 65%,
            #16537e 85%,
            #0891b2 100%) !important;
        min-height: 100vh;
        position: relative;
    }
    
    /* Geometric overlay pattern */
    .stApp::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(168, 85, 247, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(14, 165, 233, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.05) 0%, transparent 50%);
        pointer-events: none;
    }
    /* Sidebar styling - must be in each page file */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 2rem 1rem !important;
    }
    
    [data-testid="stSidebar"] .css-17eq0hr {
        color: white !important;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] button {
        background: rgba(255,255,255,0.15) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        width: 100% !important;
    }
    
    [data-testid="stSidebar"] button:hover {
        background: rgba(255,255,255,0.25) !important;
    }
    .ai-header {
        background: rgba(30, 58, 138, 0.6);
        backdrop-filter: blur(10px);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    .ai-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    /* Default: Light text everywhere */
    * {
        color: #e2e8f0 !important;
    }
    
    /* Headers - light */
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }
    
    /* Dark text ONLY inside white expander boxes */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background: white !important;
    }
    
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] * {
        color: #1e293b !important;
    }
    
    /* Dark text in forms */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.95) !important;
    }
    
    [data-testid="stForm"] * {
        color: #1e293b !important;
    }
    
    /* Metrics - keep colored */
    [data-testid="stMetricValue"] {
        color: #60a5fa !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
    }
    
    /* Input fields */
    input, textarea, select {
        color: #1e293b !important;
        background: white !important;
    }
    
    /* Buttons */
    .stButton button * {
        color: white !important;
    }
    
    /* Info/warning/error boxes - keep light text */
    .stAlert, .stSuccess, .stWarning, .stError, .stInfo {
        color: #1e293b !important;
    }

    /* Dropdown menus - dark text */
    [data-baseweb="select"] [role="listbox"],
    [data-baseweb="select"] [role="option"],
    [data-baseweb="popover"] {
        background: white !important;
    }
    
    [data-baseweb="select"] [role="listbox"] *,
    [data-baseweb="select"] [role="option"] *,
    [data-baseweb="popover"] * {
        color: #1e293b !important;
    }
    
    /* Dropdown list items */
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] li *,
    div[role="listbox"] li,
    div[role="listbox"] li * {
        color: #1e293b !important;
        background: white !important;
    }
    
    /* Select/dropdown text */
    .stSelectbox [data-baseweb="select"] > div {
        color: #1e293b !important;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        border-left: 4px solid #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        background-color: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        font-weight: 600;
        color: #cbd5e1;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(59, 130, 246, 0.8);
        color: white;
    }
    

    </style>
    <div class="ai-header">
        <h1>⚙️ System Settings</h1>
        <p>Configure platform preferences and user management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Settings tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏢 General Settings", 
        "🔒 Security & Access", 
        "📧 Email & Notifications", 
        "🔗 Integrations", 
        "🗄️ Data Management", 
        "🛡️ System Maintenance"
    ])
    
    with tab1:
        show_general_settings()
    
    with tab2:
        show_security_access()
    
    with tab3:
        show_email_notifications()
    
    with tab4:
        show_integrations_settings()
    
    with tab5:
        show_data_management()
    
    with tab6:
        show_system_maintenance()

def show_general_settings():
    st.subheader("🏢 General System Settings")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Firm information
        st.markdown("#### Firm Information")
        
        with st.form("firm_info"):
            col_firm1, col_firm2 = st.columns(2)
            
            with col_firm1:
                firm_name = st.text_input("Firm Name:", value="LegalDoc Pro Law Firm")
                firm_address = st.text_area("Address:", value="123 Legal Street\nSuite 500\nNew York, NY 10001")
                firm_phone = st.text_input("Phone:", value="+1 (555) 123-4567")
                firm_email = st.text_input("Email:", value="contact@legaldocpro.com")
            
            with col_firm2:
                firm_website = st.text_input("Website:", value="www.legaldocpro.com")
                practice_areas = st.text_area("Practice Areas:", value="Corporate Law\nLitigation\nIntellectual Property\nEmployment Law")
                time_zone = st.selectbox("Time Zone:", [
                    "Eastern Time (UTC-5)", "Central Time (UTC-6)", 
                    "Mountain Time (UTC-7)", "Pacific Time (UTC-8)"
                ])
                business_hours = st.text_input("Business Hours:", value="Monday-Friday, 9:00 AM - 6:00 PM")
            
            if st.form_submit_button("💾 Save Firm Information"):
                st.success("Firm information updated successfully!")
        
        # System preferences
        st.markdown("#### System Preferences")
        
        with st.form("system_prefs"):
            col_pref1, col_pref2 = st.columns(2)
            
            with col_pref1:
                default_language = st.selectbox("Default Language:", ["English", "Spanish", "French", "German"])
                date_format = st.selectbox("Date Format:", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
                currency = st.selectbox("Currency:", ["USD ($)", "EUR (€)", "GBP (£)", "CAD (C$)"])
                number_format = st.selectbox("Number Format:", ["1,234.56", "1.234,56", "1 234,56"])
            
            with col_pref2:
                fiscal_year_start = st.selectbox("Fiscal Year Start:", [
                    "January", "April", "July", "October"
                ])
                work_week = st.selectbox("Work Week:", ["Monday-Friday", "Sunday-Thursday", "Custom"])
                auto_save = st.checkbox("Enable Auto-save", value=True)
                dark_mode = st.checkbox("Enable Dark Mode", value=False)
            
            if st.form_submit_button("⚙️ Save System Preferences"):
                st.success("System preferences updated successfully!")
        
        # Document settings
        st.markdown("#### Document Settings")
        
        with st.form("document_settings"):
            col_doc1, col_doc2 = st.columns(2)
            
            with col_doc1:
                max_file_size = st.selectbox("Max File Size:", ["10 MB", "25 MB", "50 MB", "100 MB"])
                allowed_formats = st.multiselect("Allowed File Formats:", [
                    "PDF", "DOCX", "DOC", "TXT", "RTF", "XLS", "XLSX", "PPT", "PPTX"
                ], default=["PDF", "DOCX", "TXT"])
                version_control = st.checkbox("Enable Version Control", value=True)
                auto_backup = st.checkbox("Auto-backup Documents", value=True)
            
            with col_doc2:
                retention_period = st.selectbox("Document Retention:", [
                    "5 years", "7 years", "10 years", "Indefinite"
                ])
                watermark_documents = st.checkbox("Add Watermarks", value=True)
                ocr_processing = st.checkbox("Enable OCR Processing", value=True)
                digital_signatures = st.checkbox("Enable Digital Signatures", value=True)
            
            if st.form_submit_button("📄 Save Document Settings"):
                st.success("Document settings updated successfully!")
    
    with col2:
        st.markdown("#### System Status")
        
        system_status = [
            ("System Health", "🟢 Excellent"),
            ("Database", "🟢 Online"),
            ("Storage Usage", "65% (2.1TB)"),
            ("Active Users", "47"),
            ("System Uptime", "99.8%"),
            ("Last Backup", "2 hours ago")
        ]
        
        for label, value in system_status:
            st.write(f"**{label}:** {value}")
        
        st.markdown("#### Quick Actions")
        
        if st.button("🔄 Restart Services"):
            st.warning("Are you sure you want to restart system services?")
        if st.button("💾 Create Backup"):
            st.info("Initiating system backup...")
        if st.button("📊 System Report"):
            st.info("Generating system health report...")
        if st.button("🔧 Run Diagnostics"):
            st.info("Running system diagnostics...")
        
        st.markdown("#### Recent Changes")
        
        recent_changes = [
            "Updated firm address",
            "Changed time zone settings",
            "Modified document retention policy",
            "Enabled auto-backup",
            "Updated business hours"
        ]
        
        for change in recent_changes:
            st.write(f"• {change}")

def show_security_access():
    st.subheader("🔒 Security & Access Control")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Authentication settings
        st.markdown("#### Authentication Settings")
        
        with st.form("auth_settings"):
            col_auth1, col_auth2 = st.columns(2)
            
            with col_auth1:
                password_policy = st.selectbox("Password Policy:", [
                    "Standard (8 chars, mixed case)",
                    "Strong (12 chars, mixed case, numbers, symbols)",
                    "Very Strong (16 chars, complex requirements)"
                ])
                
                two_factor_auth = st.selectbox("Two-Factor Authentication:", [
                    "Optional", "Required for Admins", "Required for All Users"
                ])
                
                session_timeout = st.selectbox("Session Timeout:", [
                    "30 minutes", "1 hour", "2 hours", "4 hours", "8 hours"
                ])
                
                max_login_attempts = st.selectbox("Max Login Attempts:", ["3", "5", "10", "Unlimited"])
            
            with col_auth2:
                password_expiry = st.selectbox("Password Expiry:", [
                    "Never", "30 days", "60 days", "90 days", "180 days"
                ])
                
                sso_enabled = st.checkbox("Enable Single Sign-On (SSO)", value=False)
                
                if sso_enabled:
                    sso_provider = st.selectbox("SSO Provider:", [
                        "Azure Active Directory", "Google Workspace", "Okta", "SAML 2.0"
                    ])
                
                account_lockout = st.checkbox("Enable Account Lockout", value=True)
                audit_logging = st.checkbox("Enable Audit Logging", value=True)
            
            if st.form_submit_button("🔒 Save Authentication Settings"):
                st.success("Authentication settings updated successfully!")
        
        # User roles and permissions
        st.markdown("#### User Roles & Permissions")
        
        roles_data = [
            {
                "role": "System Administrator",
                "users": 2,
                "permissions": ["All System Access", "User Management", "Security Settings", "System Configuration"],
                "can_modify": True
            },
            {
                "role": "Partner",
                "users": 8,
                "permissions": ["Full Legal Access", "Client Management", "Financial Reports", "Matter Management"],
                "can_modify": True
            },
            {
                "role": "Senior Associate",
                "users": 12,
                "permissions": ["Legal Documents", "Client Access", "Time Entry", "Case Management"],
                "can_modify": True
            },
            {
                "role": "Associate",
                "users": 15,
                "permissions": ["Document Access", "Time Entry", "Basic Reports", "Client Communication"],
                "can_modify": True
            },
            {
                "role": "Paralegal",
                "users": 8,
                "permissions": ["Document Preparation", "Research Access", "Calendar Management", "Filing"],
                "can_modify": True
            },
            {
                "role": "Client",
                "users": 87,
                "permissions": ["Portal Access", "Document Viewing", "Message Attorney", "View Invoices"],
                "can_modify": False
            }
        ]
        
        for role_data in roles_data:
            with st.expander(f"👤 {role_data['role']} ({role_data['users']} users)"):
                col_role1, col_role2 = st.columns(2)
                
                with col_role1:
                    st.write("**Permissions:**")
                    for permission in role_data['permissions']:
                        st.write(f"✓ {permission}")
                
                with col_role2:
                    if role_data['can_modify']:
                        st.button("✏️ Edit Role", key=f"edit_{role_data['role']}")
                        st.button("👥 Manage Users", key=f"manage_{role_data['role']}")
                        st.button("📋 Permission Details", key=f"perms_{role_data['role']}")
                    else:
                        st.write("**Client Role**")
                        st.write("(Managed via Client Portal)")
        
        # Security monitoring
        st.markdown("#### Security Monitoring")
        
        security_events = [
            {
                "time": "2024-09-23 10:45 AM",
                "event": "Failed login attempt",
                "user": "unknown@suspicious.com",
                "ip": "192.168.1.100",
                "severity": "Medium"
            },
            {
                "time": "2024-09-23 09:30 AM",
                "event": "Password changed",
                "user": "john.smith@firm.com",
                "ip": "10.0.0.15",
                "severity": "Low"
            },
            {
                "time": "2024-09-23 08:15 AM",
                "event": "Admin login",
                "user": "admin@firm.com",
                "ip": "10.0.0.10",
                "severity": "Low"
            },
            {
                "time": "2024-09-22 11:20 PM",
                "event": "Multiple failed logins",
                "user": "sarah.johnson@firm.com",
                "ip": "172.16.0.25",
                "severity": "High"
            }
        ]
        
        for event in security_events:
            severity_colors = {
                "Low": "🟢",
                "Medium": "🟡",
                "High": "🔴"
            }
            
            with st.expander(f"{severity_colors[event['severity']]} {event['event']} - {event['time']}"):
                col_event1, col_event2 = st.columns(2)
                
                with col_event1:
                    st.write(f"**User:** {event['user']}")
                    st.write(f"**IP Address:** {event['ip']}")
                
                with col_event2:
                    st.write(f"**Severity:** {event['severity']}")
                    st.button("🔍 Investigate", key=f"investigate_{event['time']}")
    
    with col2:
        st.markdown("#### Security Status")
        
        security_metrics = [
            ("Security Score", "94/100"),
            ("Active Sessions", "47"),
            ("Failed Logins (24h)", "12"),
            ("Suspicious Activity", "2"),
            ("Last Security Scan", "6 hours ago")
        ]
        
        for label, value in security_metrics:
            st.metric(label, value)
        
        st.markdown("#### Security Alerts")
        
        alerts = [
            ("🔴 High", "Multiple failed logins detected"),
            ("🟡 Medium", "Unusual access pattern"),
            ("🟢 Low", "Password expiry reminder"),
            ("🟢 Info", "Security scan completed")
        ]
        
        for severity, alert in alerts:
            if "High" in severity:
                st.error(f"{severity}: {alert}")
            elif "Medium" in severity:
                st.warning(f"{severity}: {alert}")
            else:
                st.info(f"{severity}: {alert}")
        
        st.markdown("#### Quick Security Actions")
        
        if st.button("🔒 Force Password Reset"):
            st.warning("This will require all users to reset passwords")
        if st.button("🚫 Block Suspicious IPs"):
            st.info("Blocking flagged IP addresses...")
        if st.button("📊 Security Report"):
            st.info("Generating security analysis report...")

def show_email_notifications():
    st.subheader("📧 Email & Notification Settings")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Email server configuration
        st.markdown("#### Email Server Configuration")
        
        with st.form("email_config"):
            col_email1, col_email2 = st.columns(2)
            
            with col_email1:
                smtp_server = st.text_input("SMTP Server:", value="smtp.office365.com")
                smtp_port = st.selectbox("SMTP Port:", ["25", "587", "465", "993"])
                smtp_security = st.selectbox("Security:", ["STARTTLS", "SSL/TLS", "None"])
                smtp_username = st.text_input("Username:", value="noreply@legaldocpro.com")
            
            with col_email2:
                smtp_password = st.text_input("Password:", type="password")
                from_address = st.text_input("From Address:", value="noreply@legaldocpro.com")
                from_name = st.text_input("From Name:", value="LegalDoc Pro")
                reply_to = st.text_input("Reply-To:", value="support@legaldocpro.com")
            
            test_email = st.text_input("Test Email Address:")
            
            col_test1, col_test2 = st.columns(2)
            with col_test1:
                if st.form_submit_button("📧 Save Email Settings"):
                    st.success("Email settings saved successfully!")
            with col_test2:
                if st.form_submit_button("🧪 Send Test Email"):
                    if test_email:
                        st.info(f"Test email sent to {test_email}")
                    else:
                        st.error("Please enter a test email address")
        
        # Notification preferences
        st.markdown("#### Notification Preferences")
        
        with st.form("notification_prefs"):
            col_notif1, col_notif2 = st.columns(2)
            
            with col_notif1:
                st.write("**System Notifications:**")
                system_alerts = st.checkbox("System Alerts", value=True)
                security_notifications = st.checkbox("Security Notifications", value=True)
                backup_notifications = st.checkbox("Backup Notifications", value=True)
                maintenance_alerts = st.checkbox("Maintenance Alerts", value=True)
                
                st.write("**User Notifications:**")
                new_user_alerts = st.checkbox("New User Registration", value=True)
                login_alerts = st.checkbox("Login Notifications", value=False)
                password_reset = st.checkbox("Password Reset Requests", value=True)
            
            with col_notif2:
                st.write("**Business Notifications:**")
                new_matter_alerts = st.checkbox("New Matter Created", value=True)
                document_sharing = st.checkbox("Document Shared", value=True)
                deadline_reminders = st.checkbox("Deadline Reminders", value=True)
                invoice_notifications = st.checkbox("Invoice Generated", value=True)
                
                st.write("**Client Notifications:**")
                client_messages = st.checkbox("Client Messages", value=True)
                portal_activity = st.checkbox("Portal Activity", value=False)
                document_access = st.checkbox("Document Access", value=False)
            
            notification_frequency = st.selectbox("Notification Frequency:", [
                "Immediate", "Every 15 minutes", "Hourly", "Daily Digest"
            ])
            
            quiet_hours_enabled = st.checkbox("Enable Quiet Hours", value=True)
            if quiet_hours_enabled:
                col_quiet1, col_quiet2 = st.columns(2)
                with col_quiet1:
                    quiet_start = st.time_input("Quiet Hours Start:", value=pd.to_datetime("18:00").time())
                with col_quiet2:
                    quiet_end = st.time_input("Quiet Hours End:", value=pd.to_datetime("08:00").time())
            
            if st.form_submit_button("🔔 Save Notification Preferences"):
                st.success("Notification preferences updated successfully!")
        
        # Email templates
        st.markdown("#### Email Templates")
        
        templates = [
            {
                "name": "Welcome Email",
                "subject": "Welcome to LegalDoc Pro",
                "usage": "New user registration",
                "last_modified": "2024-09-20"
            },
            {
                "name": "Password Reset",
                "subject": "Password Reset Request",
                "usage": "Password reset requests",
                "last_modified": "2024-09-18"
            },
            {
                "name": "Document Notification",
                "subject": "New Document Available",
                "usage": "Document sharing alerts",
                "last_modified": "2024-09-22"
            },
            {
                "name": "Invoice Notification",
                "subject": "New Invoice Generated",
                "usage": "Billing notifications",
                "last_modified": "2024-09-19"
            }
        ]
        
        for template in templates:
            with st.expander(f"📧 {template['name']} - {template['subject']}"):
                col_template1, col_template2, col_template3 = st.columns(3)
                
                with col_template1:
                    st.write(f"**Usage:** {template['usage']}")
                    st.write(f"**Last Modified:** {template['last_modified']}")
                
                with col_template2:
                    st.button("✏️ Edit Template", key=f"edit_template_{template['name']}")
                    st.button("👁️ Preview", key=f"preview_template_{template['name']}")
                
                with col_template3:
                    st.button("🧪 Test Send", key=f"test_template_{template['name']}")
                    st.button("📋 Duplicate", key=f"duplicate_template_{template['name']}")
    
    with col2:
        st.markdown("#### Email Statistics")
        
        email_stats = [
            ("Emails Sent (Today)", "47"),
            ("Emails Sent (Month)", "1,247"),
            ("Delivery Rate", "98.7%"),
            ("Open Rate", "72.4%"),
            ("Bounce Rate", "1.3%")
        ]
        
        for label, value in email_stats:
            st.metric(label, value)
        
        st.markdown("#### Recent Email Activity")
        
        recent_emails = [
            "Welcome email sent to new user",
            "Invoice notification delivered",
            "Password reset email sent",
            "Document sharing alert sent",
            "System maintenance notice sent"
        ]
        
        for email in recent_emails:
            st.write(f"• {email}")
        
        st.markdown("#### Email Queue")
        
        queue_info = [
            ("Pending", "3 emails"),
            ("Processing", "1 email"),
            ("Failed", "0 emails"),
            ("Retry Queue", "2 emails")
        ]
        
        for status, count in queue_info:
            st.write(f"**{status}:** {count}")

def show_integrations_settings():
    st.subheader("🔗 Integration Settings")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # API configuration
        st.markdown("#### API Configuration")
        
        with st.form("api_config"):
            col_api1, col_api2 = st.columns(2)
            
            with col_api1:
                api_enabled = st.checkbox("Enable API Access", value=True)
                api_version = st.selectbox("API Version:", ["v1", "v2", "v3"])
                rate_limiting = st.checkbox("Enable Rate Limiting", value=True)
                
                if rate_limiting:
                    rate_limit = st.selectbox("Rate Limit:", [
                        "100 requests/hour", "500 requests/hour", 
                        "1000 requests/hour", "5000 requests/hour"
                    ])
            
            with col_api2:
                api_authentication = st.selectbox("Authentication:", [
                    "API Key", "OAuth 2.0", "JWT Tokens", "Basic Auth"
                ])
                
                cors_enabled = st.checkbox("Enable CORS", value=True)
                if cors_enabled:
                    cors_origins = st.text_area("Allowed Origins:", 
                        value="https://app.legaldocpro.com\nhttps://portal.legaldocpro.com")
                
                api_logging = st.checkbox("Enable API Logging", value=True)
            
            if st.form_submit_button("🔗 Save API Configuration"):
                st.success("API configuration updated successfully!")
        
        # Third-party integrations
        st.markdown("#### Third-Party Integrations")
        
        integrations = [
            {
                "name": "Microsoft Office 365",
                "type": "Productivity Suite",
                "status": "Connected",
                "config": {"tenant_id": "abc123", "client_id": "def456"},
                "last_sync": "2024-09-23 10:30 AM"
            },
            {
                "name": "QuickBooks Online",
                "type": "Accounting",
                "status": "Connected",
                "config": {"company_id": "789xyz", "sandbox": False},
                "last_sync": "2024-09-23 09:45 AM"
            },
            {
                "name": "DocuSign",
                "type": "E-Signature",
                "status": "Connected",
                "config": {"account_id": "456abc", "base_path": "https://demo.docusign.net"},
                "last_sync": "2024-09-23 08:15 AM"
            },
            {
                "name": "Salesforce",
                "type": "CRM",
                "status": "Disconnected",
                "config": {},
                "last_sync": "Never"
            }
        ]
        
        for integration in integrations:
            status_icon = "🟢" if integration["status"] == "Connected" else "🔴"
            
            with st.expander(f"{status_icon} {integration['name']} ({integration['type']})"):
                col_int1, col_int2, col_int3 = st.columns(3)
                
                with col_int1:
                    st.write(f"**Status:** {integration['status']}")
                    st.write(f"**Type:** {integration['type']}")
                    st.write(f"**Last Sync:** {integration['last_sync']}")
                
                with col_int2:
                    if integration['config']:
                        st.write("**Configuration:**")
                        for key, value in integration['config'].items():
                            st.write(f"• {key}: {value}")
                    else:
                        st.write("**Not Configured**")
                
                with col_int3:
                    if integration['status'] == "Connected":
                        st.button("⚙️ Configure", key=f"config_{integration['name']}")
                        st.button("🔄 Sync Now", key=f"sync_{integration['name']}")
                        st.button("🔌 Disconnect", key=f"disconnect_{integration['name']}")
                    else:
                        st.button("🔗 Connect", key=f"connect_{integration['name']}")
                        st.button("⚙️ Setup", key=f"setup_{integration['name']}")
        
        # Webhook configuration
        st.markdown("#### Webhook Configuration")
        
        with st.form("webhook_config"):
            webhook_enabled = st.checkbox("Enable Webhooks", value=True)
            
            if webhook_enabled:
                webhook_url = st.text_input("Webhook URL:", placeholder="https://your-app.com/webhooks")
                webhook_secret = st.text_input("Webhook Secret:", type="password")
                
                webhook_events = st.multiselect("Webhook Events:", [
                    "user.created", "user.updated", "document.created", "document.shared",
                    "matter.created", "matter.updated", "invoice.generated", "payment.received"
                ], default=["document.created", "matter.created"])
                
                retry_attempts = st.selectbox("Retry Attempts:", ["1", "3", "5", "10"])
                timeout_seconds = st.selectbox("Timeout (seconds):", ["10", "30", "60", "120"])
            
            if st.form_submit_button("🪝 Save Webhook Configuration"):
                st.success("Webhook configuration updated successfully!")
    
    with col2:
        st.markdown("#### Integration Status")
        
        integration_stats = [
            ("Active Integrations", "8"),
            ("API Calls (Today)", "1,247"),
            ("Success Rate", "99.2%"),
            ("Avg Response Time", "145ms")
        ]
        
        for label, value in integration_stats:
            st.metric(label, value)
        
        st.markdown("#### Recent API Activity")
        
        api_activity = [
            "Document created via API",
            "User authenticated",
            "Calendar sync completed",
            "Invoice data updated",
            "Contact information synced"
        ]
        
        for activity in api_activity:
            st.write(f"• {activity}")
        
        st.markdown("#### Integration Health")
        
        health_status = [
            ("Office 365", "🟢 Healthy"),
            ("QuickBooks", "🟢 Healthy"),
            ("DocuSign", "🟡 Warning"),
            ("API Gateway", "🟢 Healthy")
        ]
        
        for service, status in health_status:
            st.write(f"**{service}:** {status}")

def show_data_management():
    st.subheader("🗄️ Data Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Database management
        st.markdown("#### Database Management")
        
        with st.form("database_config"):
            col_db1, col_db2 = st.columns(2)
            
            with col_db1:
                backup_frequency = st.selectbox("Backup Frequency:", [
                    "Every 6 hours", "Daily", "Weekly", "Monthly"
                ])
                backup_retention = st.selectbox("Backup Retention:", [
                    "30 days", "90 days", "1 year", "2 years", "Indefinite"
                ])
                auto_backup = st.checkbox("Enable Auto-backup", value=True)
                compression = st.checkbox("Enable Backup Compression", value=True)
            
            with col_db2:
                encryption = st.checkbox("Encrypt Backups", value=True)
                if encryption:
                    encryption_method = st.selectbox("Encryption Method:", [
                        "AES-256", "AES-128", "3DES"
                    ])
                
                cloud_backup = st.checkbox("Cloud Backup", value=True)
                if cloud_backup:
                    cloud_provider = st.selectbox("Cloud Provider:", [
                        "AWS S3", "Azure Blob", "Google Cloud", "Dropbox Business"
                    ])
            
            if st.form_submit_button("💾 Save Database Settings"):
                st.success("Database settings updated successfully!")
        
        # Data retention policies
        st.markdown("#### Data Retention Policies")
        
        retention_policies = [
            {
                "data_type": "Client Documents",
                "retention_period": "7 years",
                "auto_delete": False,
                "archive_after": "2 years"
            },
            {
                "data_type": "Email Communications",
                "retention_period": "5 years",
                "auto_delete": True,
                "archive_after": "1 year"
            },
            {
                "data_type": "Audit Logs",
                "retention_period": "3 years",
                "auto_delete": True,
                "archive_after": "6 months"
            },
            {
                "data_type": "User Activity Logs",
                "retention_period": "1 year",
                "auto_delete": True,
                "archive_after": "3 months"
            },
            {
                "data_type": "Billing Records",
                "retention_period": "7 years",
                "auto_delete": False,
                "archive_after": "2 years"
            }
        ]
        
        for policy in retention_policies:
            with st.expander(f"📁 {policy['data_type']} - Retain for {policy['retention_period']}"):
                col_policy1, col_policy2, col_policy3 = st.columns(3)
                
                with col_policy1:
                    st.write(f"**Retention Period:** {policy['retention_period']}")
                    st.write(f"**Archive After:** {policy['archive_after']}")
                
                with col_policy2:
                    auto_delete_status = "✅ Enabled" if policy['auto_delete'] else "❌ Disabled"
                    st.write(f"**Auto-delete:** {auto_delete_status}")
                
                with col_policy3:
                    st.button("✏️ Edit Policy", key=f"edit_policy_{policy['data_type']}")
                    st.button("📊 View Data", key=f"view_data_{policy['data_type']}")
        
        # Data export and migration
        st.markdown("#### Data Export & Migration")
        
        with st.form("data_export"):
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                export_type = st.selectbox("Export Type:", [
                    "Full Database Export",
                    "Client Data Only",
                    "Documents Only",
                    "User Data Only",
                    "Configuration Only",
                    "Custom Selection"
                ])
                
                export_format = st.selectbox("Export Format:", [
                    "JSON", "CSV", "XML", "SQL Dump", "Excel"
                ])
                
                include_files = st.checkbox("Include File Attachments", value=True)
                compress_export = st.checkbox("Compress Export", value=True)
            
            with col_export2:
                date_range = st.selectbox("Date Range:", [
                    "All Time", "Last Year", "Last 6 Months", 
                    "Last 3 Months", "Custom Range"
                ])
                
                if date_range == "Custom Range":
                    start_date = st.date_input("Start Date:")
                    end_date = st.date_input("End Date:")
                
                exclude_sensitive = st.checkbox("Exclude Sensitive Data", value=True)
                anonymize_data = st.checkbox("Anonymize Personal Data", value=False)
            
            if st.form_submit_button("📤 Export Data"):
                st.success("Data export initiated. You will receive an email when ready.")
        
        # Storage analytics
        st.markdown("#### Storage Analytics")
        
        storage_data = [
            {"category": "Documents", "size_gb": 1250.5, "percentage": 62.8, "files": 12847},
            {"category": "Database", "size_gb": 456.2, "percentage": 22.9, "files": 1},
            {"category": "Email Archives", "size_gb": 189.7, "percentage": 9.5, "files": 8934},
            {"category": "System Logs", "size_gb": 67.3, "percentage": 3.4, "files": 2456},
            {"category": "Backups", "size_gb": 28.1, "percentage": 1.4, "files": 47}
        ]
        
        for storage in storage_data:
            with st.expander(f"💾 {storage['category']} - {storage['size_gb']:.1f} GB ({storage['percentage']:.1f}%)"):
                col_storage1, col_storage2, col_storage3 = st.columns(3)
                
                with col_storage1:
                    st.write(f"**Size:** {storage['size_gb']:.1f} GB")
                    st.progress(storage['percentage'] / 100)
                
                with col_storage2:
                    st.write(f"**Files:** {storage['files']:,}")
                    st.write(f"**Percentage:** {storage['percentage']:.1f}%")
                
                with col_storage3:
                    st.button("🧹 Cleanup", key=f"cleanup_{storage['category']}")
                    st.button("📊 Analyze", key=f"analyze_{storage['category']}")
    
    with col2:
        st.markdown("#### Storage Overview")
        
        storage_metrics = [
            ("Total Storage", "2.1 TB"),
            ("Available Space", "875 GB"),
            ("Usage Growth", "+12.3%"),
            ("Files Stored", "24,285")
        ]
        
        for label, value in storage_metrics:
            st.metric(label, value)
        
        st.markdown("#### Recent Backups")
        
        recent_backups = [
            ("Full Backup", "2024-09-23 02:00 AM", "✅"),
            ("Incremental", "2024-09-22 02:00 AM", "✅"),
            ("Incremental", "2024-09-21 02:00 AM", "✅"),
            ("Full Backup", "2024-09-20 02:00 AM", "✅"),
            ("Incremental", "2024-09-19 02:00 AM", "✅")
        ]
        
        for backup_type, date, status in recent_backups:
            st.write(f"{status} **{backup_type}** - {date}")
        
        st.markdown("#### Data Health")
        
        if st.button("🔍 Check Data Integrity"):
            st.info("Running data integrity check...")
        if st.button("🧹 Cleanup Orphaned Files"):
            st.info("Scanning for orphaned files...")
        if st.button("📊 Generate Storage Report"):
            st.info("Creating detailed storage report...")

def show_system_maintenance():
    st.subheader("🛡️ System Maintenance")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # System health monitoring
        st.markdown("#### System Health Monitoring")
        
        health_metrics = [
            {"component": "Web Server", "status": "Healthy", "uptime": "99.9%", "response_time": "45ms"},
            {"component": "Database", "status": "Healthy", "uptime": "99.8%", "response_time": "12ms"},
            {"component": "File Storage", "status": "Warning", "uptime": "98.5%", "response_time": "156ms"},
            {"component": "Email Service", "status": "Healthy", "uptime": "99.7%", "response_time": "89ms"},
            {"component": "API Gateway", "status": "Healthy", "uptime": "99.9%", "response_time": "34ms"},
            {"component": "Search Engine", "status": "Healthy", "uptime": "99.6%", "response_time": "78ms"}
        ]
        
        for metric in health_metrics:
            status_colors = {
                "Healthy": "🟢",
                "Warning": "🟡",
                "Critical": "🔴",
                "Offline": "⚫"
            }
            
            with st.expander(f"{status_colors[metric['status']]} {metric['component']} - {metric['status']}"):
                col_health1, col_health2, col_health3 = st.columns(3)
                
                with col_health1:
                    st.write(f"**Status:** {metric['status']}")
                    st.write(f"**Uptime:** {metric['uptime']}")
                
                with col_health2:
                    st.write(f"**Response Time:** {metric['response_time']}")
                    
                    uptime_value = float(metric['uptime'].replace('%', ''))
                    st.progress(uptime_value / 100)
                
                with col_health3:
                    st.button("🔍 Diagnose", key=f"diagnose_{metric['component']}")
                    st.button("🔄 Restart", key=f"restart_{metric['component']}")
        
        # Scheduled maintenance
        st.markdown("#### Scheduled Maintenance")
        
        with st.form("schedule_maintenance"):
            col_maint1, col_maint2 = st.columns(2)
            
            with col_maint1:
                maintenance_type = st.selectbox("Maintenance Type:", [
                    "System Update", "Database Optimization", "Security Patch",
                    "Performance Tuning", "Backup Verification", "Custom Task"
                ])
                
                maintenance_date = st.date_input("Scheduled Date:")
                maintenance_time = st.time_input("Scheduled Time:")
                
                estimated_duration = st.selectbox("Estimated Duration:", [
                    "15 minutes", "30 minutes", "1 hour", "2 hours", "4 hours"
                ])
            
            with col_maint2:
                notify_users = st.checkbox("Notify Users", value=True)
                
                if notify_users:
                    notification_advance = st.selectbox("Notify in Advance:", [
                        "1 hour", "4 hours", "1 day", "3 days", "1 week"
                    ])
                
                system_downtime = st.checkbox("Requires System Downtime", value=False)
                auto_execute = st.checkbox("Auto-execute", value=False)
            
            maintenance_description = st.text_area("Description:", 
                placeholder="Describe what will be done during maintenance...")
            
            if st.form_submit_button("📅 Schedule Maintenance"):
                st.success("Maintenance scheduled successfully!")
        
        # System logs
        st.markdown("#### System Logs")
        
        log_entries = [
            {
                "timestamp": "2024-09-23 10:45:23",
                "level": "INFO",
                "component": "Web Server",
                "message": "User authentication successful for user@firm.com"
            },
            {
                "timestamp": "2024-09-23 10:44:15",
                "level": "WARNING",
                "component": "File Storage",
                "message": "High disk usage detected on storage partition /data"
            },
            {
                "timestamp": "2024-09-23 10:42:08",
                "level": "INFO",
                "component": "Database",
                "message": "Automated backup completed successfully"
            },
            {
                "timestamp": "2024-09-23 10:40:33",
                "level": "ERROR",
                "component": "Email Service",
                "message": "Failed to deliver email to invalid@domain.com"
            },
            {
                "timestamp": "2024-09-23 10:38:17",
                "level": "INFO",
                "component": "API Gateway",
                "message": "Rate limit threshold reached for client API key"
            }
        ]
        
        log_filters = st.columns(4)
        with log_filters[0]:
            log_level = st.selectbox("Log Level:", ["All", "INFO", "WARNING", "ERROR", "CRITICAL"])
        with log_filters[1]:
            log_component = st.selectbox("Component:", ["All", "Web Server", "Database", "File Storage", "Email Service", "API Gateway"])
        with log_filters[2]:
            log_date = st.date_input("Date:", value=datetime.now().date())
        with log_filters[3]:
            if st.button("🔄 Refresh Logs"):
                st.info("Refreshing log entries...")
        
        for log in log_entries:
            level_colors = {
                "INFO": "🔵",
                "WARNING": "🟡",
                "ERROR": "🔴",
                "CRITICAL": "🟣"
            }
            
            with st.expander(f"{level_colors[log['level']]} {log['timestamp']} - {log['component']} ({log['level']})"):
                st.write(f"**Message:** {log['message']}")
                
                col_log1, col_log2, col_log3 = st.columns(3)
                with col_log1:
                    st.button("📋 Copy Message", key=f"copy_{log['timestamp']}")
                with col_log2:
                    st.button("🔍 View Details", key=f"details_{log['timestamp']}")
                with col_log3:
                    st.button("⚠️ Create Alert", key=f"alert_{log['timestamp']}")
        
        # Performance optimization
        st.markdown("#### Performance Optimization")
        
        optimization_tasks = [
            {"task": "Database Index Optimization", "status": "Completed", "last_run": "2024-09-22", "improvement": "+15%"},
            {"task": "Cache Cleanup", "status": "Scheduled", "last_run": "2024-09-21", "improvement": "+8%"},
            {"task": "Log File Rotation", "status": "Running", "last_run": "2024-09-23", "improvement": "N/A"},
            {"task": "Temporary File Cleanup", "status": "Pending", "last_run": "2024-09-20", "improvement": "+12%"},
            {"task": "Memory Optimization", "status": "Completed", "last_run": "2024-09-19", "improvement": "+23%"}
        ]
        
        for task in optimization_tasks:
            status_icons = {
                "Completed": "✅",
                "Running": "🔄",
                "Scheduled": "📅",
                "Pending": "⏳",
                "Failed": "❌"
            }
            
            with st.expander(f"{status_icons[task['status']]} {task['task']} - {task['status']}"):
                col_opt1, col_opt2, col_opt3 = st.columns(3)
                
                with col_opt1:
                    st.write(f"**Status:** {task['status']}")
                    st.write(f"**Last Run:** {task['last_run']}")
                
                with col_opt2:
                    st.write(f"**Performance Improvement:** {task['improvement']}")
                
                with col_opt3:
                    if task['status'] in ["Pending", "Failed"]:
                        st.button("▶️ Run Now", key=f"run_{task['task']}")
                    elif task['status'] == "Running":
                        st.button("⏹️ Stop", key=f"stop_{task['task']}")
                    else:
                        st.button("🔄 Run Again", key=f"rerun_{task['task']}")
    
    with col2:
        st.markdown("#### System Overview")
        
        system_overview = [
            ("System Uptime", "47 days"),
            ("Active Processes", "23"),
            ("Memory Usage", "68%"),
            ("CPU Usage", "34%"),
            ("Disk I/O", "Normal"),
            ("Network Traffic", "Low")
        ]
        
        for label, value in system_overview:
            st.metric(label, value)
        
        st.markdown("#### Maintenance History")
        
        maintenance_history = [
            ("Security Update", "2024-09-20", "✅"),
            ("Database Optimization", "2024-09-15", "✅"),
            ("System Backup", "2024-09-10", "✅"),
            ("Performance Tuning", "2024-09-05", "✅"),
            ("Log Cleanup", "2024-09-01", "✅")
        ]
        
        for task, date, status in maintenance_history:
            st.write(f"{status} **{task}** - {date}")
        
        st.markdown("#### Quick Actions")
        
        if st.button("🔄 Restart All Services"):
            st.warning("This will restart all system services!")
        if st.button("🧹 Run System Cleanup"):
            st.info("Initiating comprehensive system cleanup...")
        if st.button("📊 Generate System Report"):
            st.info("Creating detailed system report...")
        if st.button("⚡ Performance Analysis"):
            st.info("Starting performance analysis...")
        
        st.markdown("#### Emergency Actions")
        
        if st.button("🚨 Emergency Shutdown"):
            st.error("This will shut down the entire system!")
        if st.button("🔧 Safe Mode"):
            st.warning("This will restart system in safe mode!")
        if st.button("📞 Contact Support"):
            st.info("Opening support ticket...")

# Main execution
if __name__ == "__main__":
    show()
