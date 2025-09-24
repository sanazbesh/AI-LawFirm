import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def show():
    st.markdown("""
    <div class="main-header">
        <h1>🏛️ Client Portal Management</h1>
        <p>Manage client access, permissions, and self-service capabilities</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Client Portal tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👥 Client Access", 
        "📄 Document Sharing", 
        "💬 Communications", 
        "🔧 Portal Settings", 
        "📊 Usage Analytics"
    ])
    
    with tab1:
        show_client_access()
    
    with tab2:
        show_document_sharing()
    
    with tab3:
        show_communications()
    
    with tab4:
        show_portal_settings()
    
    with tab5:
        show_usage_analytics()

def show_client_access():
    st.subheader("👥 Client Access Management")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Client access overview
        st.markdown("#### Active Client Portal Users")
        
        # Search and filter
        col_search1, col_search2, col_search3 = st.columns(3)
        with col_search1:
            client_search = st.text_input("Search Clients:", placeholder="Name, email, or company...")
        with col_search2:
            access_filter = st.selectbox("Access Level:", ["All", "Full Access", "Limited Access", "View Only", "Suspended"])
        with col_search3:
            status_filter = st.selectbox("Status:", ["All", "Active", "Inactive", "Pending Setup"])
        
        # Client access list
        client_users = [
            {
                "name": "John Smith",
                "company": "ABC Corporation",
                "email": "john.smith@abccorp.com",
                "access_level": "Full Access",
                "status": "Active",
                "last_login": "2024-09-23 09:30 AM",
                "documents_accessed": 23,
                "matters": ["Corporate Restructuring", "Contract Review"],
                "permissions": ["View Documents", "Download Files", "Submit Requests", "View Billing"]
            },
            {
                "name": "Sarah Johnson",
                "company": "Tech Solutions Inc",
                "email": "s.johnson@techsolutions.com",
                "access_level": "Full Access",
                "status": "Active",
                "last_login": "2024-09-22 04:15 PM",
                "documents_accessed": 18,
                "matters": ["IP Licensing", "Employment Agreement"],
                "permissions": ["View Documents", "Download Files", "Submit Requests", "View Billing", "Approve Invoices"]
            },
            {
                "name": "Mike Davis",
                "company": "Startup Innovations",
                "email": "mike@startup-innov.com",
                "access_level": "Limited Access",
                "status": "Active",
                "last_login": "2024-09-20 02:45 PM",
                "documents_accessed": 7,
                "matters": ["Incorporation Documents"],
                "permissions": ["View Documents", "Submit Requests"]
            },
            {
                "name": "Emily Chen",
                "company": "Global Manufacturing",
                "email": "emily.chen@globalmfg.com",
                "access_level": "View Only",
                "status": "Pending Setup",
                "last_login": "Never",
                "documents_accessed": 0,
                "matters": ["Compliance Review"],
                "permissions": ["View Documents"]
            }
        ]
        
        for client in client_users:
            access_color = {
                "Full Access": "🟢",
                "Limited Access": "🟡",
                "View Only": "🔵",
                "Suspended": "🔴"
            }
            
            status_color = {
                "Active": "✅",
                "Inactive": "⭕",
                "Pending Setup": "⏳"
            }
            
            with st.expander(f"{access_color[client['access_level']]} {client['name']} ({client['company']}) - {status_color[client['status']]} {client['status']}"):
                col_client1, col_client2, col_client3 = st.columns(3)
                
                with col_client1:
                    st.write(f"**Email:** {client['email']}")
                    st.write(f"**Access Level:** {client['access_level']}")
                    st.write(f"**Last Login:** {client['last_login']}")
                
                with col_client2:
                    st.write(f"**Documents Accessed:** {client['documents_accessed']}")
                    st.write("**Active Matters:**")
                    for matter in client['matters']:
                        st.write(f"• {matter}")
                
                with col_client3:
                    st.write("**Permissions:**")
                    for permission in client['permissions']:
                        st.write(f"✓ {permission}")
                
                # Client management actions
                col_action1, col_action2, col_action3, col_action4 = st.columns(4)
                with col_action1:
                    st.button("⚙️ Edit Access", key=f"edit_{client['email']}")
                with col_action2:
                    st.button("📧 Send Invite", key=f"invite_{client['email']}")
                with col_action3:
                    st.button("🔒 Reset Password", key=f"reset_{client['email']}")
                with col_action4:
                    if client['status'] == "Active":
                        st.button("⏸️ Suspend", key=f"suspend_{client['email']}")
                    else:
                        st.button("▶️ Activate", key=f"activate_{client['email']}")
        
        # Bulk operations
        st.markdown("#### Bulk Operations")
        
        col_bulk1, col_bulk2, col_bulk3, col_bulk4 = st.columns(4)
        with col_bulk1:
            if st.button("📧 Send Welcome Email"):
                st.info("Sending welcome emails to new users...")
        with col_bulk2:
            if st.button("🔄 Sync Permissions"):
                st.info("Synchronizing permissions across all users...")
        with col_bulk3:
            if st.button("📊 Export User List"):
                st.info("Exporting client user data...")
        with col_bulk4:
            if st.button("⚠️ Security Audit"):
                st.info("Running security audit on client accounts...")
    
    with col2:
        st.markdown("#### Access Statistics")
        
        access_stats = [
            ("Total Portal Users", "87"),
            ("Active This Month", "64"),
            ("Pending Setup", "8"),
            ("Login Success Rate", "98.2%")
        ]
        
        for label, value in access_stats:
            st.metric(label, value)
        
        st.markdown("#### Access Levels")
        
        access_breakdown = [
            ("Full Access", "45 users", "52%"),
            ("Limited Access", "28 users", "32%"),
            ("View Only", "12 users", "14%"),
            ("Suspended", "2 users", "2%")
        ]
        
        for level, count, percentage in access_breakdown:
            st.write(f"**{level}:** {count} ({percentage})")
        
        st.markdown("#### Recent Activity")
        
        recent_activity = [
            "John Smith logged in",
            "New user invitation sent",
            "Permission updated for Tech Solutions",
            "Password reset completed",
            "Document access granted"
        ]
        
        for activity in recent_activity:
            st.write(f"• {activity}")

def show_document_sharing():
    st.subheader("📄 Client Document Sharing")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Document sharing interface
        st.markdown("#### Share Documents with Clients")
        
        with st.form("share_document"):
            col_share1, col_share2 = st.columns(2)
            
            with col_share1:
                selected_client = st.selectbox("Select Client:", [
                    "ABC Corporation (John Smith)",
                    "Tech Solutions Inc (Sarah Johnson)",
                    "Startup Innovations (Mike Davis)",
                    "Global Manufacturing (Emily Chen)"
                ])
                
                document_type = st.selectbox("Document Type:", [
                    "Contract", "Legal Brief", "Court Filing", "Correspondence", 
                    "Invoice", "Report", "Other"
                ])
                
                sharing_method = st.selectbox("Sharing Method:", [
                    "Portal Access", "Secure Email", "Download Link", "View Only"
                ])
            
            with col_share2:
                access_level = st.selectbox("Access Level:", [
                    "View Only", "Download Allowed", "Comment Allowed", "Full Access"
                ])
                
                expiry_date = st.date_input("Access Expires:", value=datetime.now() + timedelta(days=30))
                
                notification = st.checkbox("Send notification to client", value=True)
            
            document_title = st.text_input("Document Title:", placeholder="Enter document title...")
            document_description = st.text_area("Description:", placeholder="Brief description of the document...")
            
            # File upload simulation
            uploaded_file = st.file_uploader("Upload Document:", type=['pdf', 'docx', 'txt'])
            
            if st.form_submit_button("📤 Share Document", type="primary"):
                st.success(f"Document shared successfully with {selected_client}!")
                if notification:
                    st.info("Notification email sent to client.")
        
        # Shared documents tracking
        st.markdown("#### Recently Shared Documents")
        
        shared_docs = [
            {
                "document": "Merger Agreement Final.pdf",
                "client": "ABC Corporation",
                "shared_date": "2024-09-23",
                "access_level": "Download Allowed",
                "status": "Viewed",
                "downloads": 2,
                "expires": "2024-10-23"
            },
            {
                "document": "Employment Contract.docx",
                "client": "Tech Solutions Inc",
                "shared_date": "2024-09-22",
                "access_level": "Full Access",
                "status": "Downloaded",
                "downloads": 1,
                "expires": "2024-11-22"
            },
            {
                "document": "Incorporation Documents.pdf",
                "client": "Startup Innovations",
                "shared_date": "2024-09-21",
                "access_level": "View Only",
                "status": "Not Viewed",
                "downloads": 0,
                "expires": "2024-10-21"
            },
            {
                "document": "Compliance Report.pdf",
                "client": "Global Manufacturing",
                "shared_date": "2024-09-20",
                "access_level": "Download Allowed",
                "status": "Viewed",
                "downloads": 3,
                "expires": "2024-10-20"
            }
        ]
        
        for doc in shared_docs:
            status_icons = {
                "Viewed": "👁️",
                "Downloaded": "📥",
                "Not Viewed": "⭕"
            }
            
            with st.expander(f"{status_icons[doc['status']]} {doc['document']} → {doc['client']}"):
                col_doc1, col_doc2, col_doc3 = st.columns(3)
                
                with col_doc1:
                    st.write(f"**Shared Date:** {doc['shared_date']}")
                    st.write(f"**Access Level:** {doc['access_level']}")
                    st.write(f"**Status:** {doc['status']}")
                
                with col_doc2:
                    st.write(f"**Downloads:** {doc['downloads']}")
                    st.write(f"**Expires:** {doc['expires']}")
                    
                    if doc['downloads'] > 0:
                        st.progress(min(doc['downloads'] / 5, 1.0))
                
                with col_doc3:
                    st.button("📊 View Analytics", key=f"analytics_{doc['document'][:10]}")
                    st.button("🔄 Reshare", key=f"reshare_{doc['document'][:10]}")
                    st.button("🗑️ Revoke Access", key=f"revoke_{doc['document'][:10]}")
    
    with col2:
        st.markdown("#### Sharing Statistics")
        
        sharing_stats = [
            ("Documents Shared", "247"),
            ("This Month", "34"),
            ("Total Downloads", "1,892"),
            ("Avg. View Time", "12.4 min")
        ]
        
        for label, value in sharing_stats:
            st.metric(label, value)
        
        st.markdown("#### Document Types")
        
        doc_types = [
            ("Contracts", "89 docs"),
            ("Correspondence", "67 docs"),
            ("Reports", "45 docs"),
            ("Invoices", "34 docs"),
            ("Other", "12 docs")
        ]
        
        for doc_type, count in doc_types:
            st.write(f"**{doc_type}:** {count}")
        
        st.markdown("#### Security Settings")
        
        security_settings = [
            ("Watermark Documents", "✅"),
            ("Track Downloads", "✅"),
            ("Expire Old Links", "✅"),
            ("Require Login", "✅"),
            ("IP Restrictions", "❌")
        ]
        
        for setting, status in security_settings:
            st.write(f"{setting}: {status}")

def show_communications():
    st.subheader("💬 Client Communications")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Communication center
        st.markdown("#### Client Communication Center")
        
        # Message composer
        with st.expander("✉️ Compose New Message"):
            col_msg1, col_msg2 = st.columns(2)
            
            with col_msg1:
                recipient = st.selectbox("To:", [
                    "ABC Corporation (John Smith)",
                    "Tech Solutions Inc (Sarah Johnson)",
                    "Startup Innovations (Mike Davis)",
                    "Global Manufacturing (Emily Chen)",
                    "All Clients"
                ])
                
                message_type = st.selectbox("Message Type:", [
                    "General Update", "Document Notification", "Billing Notice", 
                    "Appointment Reminder", "Status Update", "Urgent Notice"
                ])
            
            with col_msg2:
                priority = st.selectbox("Priority:", ["Normal", "High", "Low"])
                delivery_method = st.selectbox("Delivery:", ["Portal + Email", "Portal Only", "Email Only"])
            
            subject = st.text_input("Subject:", placeholder="Enter message subject...")
            message_body = st.text_area("Message:", placeholder="Type your message here...", height=150)
            
            col_compose1, col_compose2, col_compose3 = st.columns(3)
            with col_compose1:
                if st.button("📤 Send Message"):
                    st.success("Message sent successfully!")
            with col_compose2:
                if st.button("📝 Save Draft"):
                    st.info("Message saved as draft.")
            with col_compose3:
                if st.button("👁️ Preview"):
                    st.info("Opening message preview...")
        
        # Recent communications
        st.markdown("#### Recent Communications")
        
        communications = [
            {
                "type": "Message",
                "subject": "Document Review Complete",
                "client": "ABC Corporation",
                "date": "2024-09-23 10:30 AM",
                "status": "Read",
                "priority": "Normal",
                "method": "Portal + Email"
            },
            {
                "type": "Notification",
                "subject": "New Document Available",
                "client": "Tech Solutions Inc",
                "date": "2024-09-22 03:15 PM",
                "status": "Delivered",
                "priority": "Normal",
                "method": "Portal Only"
            },
            {
                "type": "Reminder",
                "subject": "Upcoming Court Date",
                "client": "Startup Innovations",
                "date": "2024-09-22 09:00 AM",
                "status": "Read",
                "priority": "High",
                "method": "Portal + Email"
            },
            {
                "type": "Invoice",
                "subject": "Monthly Invoice - September 2024",
                "client": "Global Manufacturing",
                "date": "2024-09-21 05:00 PM",
                "status": "Unread",
                "priority": "Normal",
                "method": "Email Only"
            }
        ]
        
        for comm in communications:
            type_icons = {
                "Message": "💬",
                "Notification": "🔔",
                "Reminder": "⏰",
                "Invoice": "💰"
            }
            
            status_colors = {
                "Read": "🟢",
                "Delivered": "🟡",
                "Unread": "🔴"
            }
            
            priority_icons = {
                "High": "🔴",
                "Normal": "🔵",
                "Low": "🟢"
            }
            
            with st.expander(f"{type_icons[comm['type']]} {comm['subject']} → {comm['client']} {status_colors[comm['status']]}"):
                col_comm1, col_comm2, col_comm3 = st.columns(3)
                
                with col_comm1:
                    st.write(f"**Type:** {comm['type']}")
                    st.write(f"**Date:** {comm['date']}")
                    st.write(f"**Status:** {comm['status']}")
                
                with col_comm2:
                    st.write(f"**Priority:** {priority_icons[comm['priority']]} {comm['priority']}")
                    st.write(f"**Method:** {comm['method']}")
                
                with col_comm3:
                    st.button("📖 View Full", key=f"view_{comm['subject'][:10]}")
                    st.button("↩️ Reply", key=f"reply_{comm['subject'][:10]}")
                    st.button("🔄 Resend", key=f"resend_{comm['subject'][:10]}")
        
        # Communication templates
        st.markdown("#### Message Templates")
        
        templates = [
            "📄 Document Ready for Review",
            "⏰ Appointment Confirmation",
            "💰 Invoice Payment Reminder",
            "📅 Status Update Request",
            "🎉 Matter Completion Notice"
        ]
        
        col_template1, col_template2 = st.columns(2)
        for i, template in enumerate(templates):
            col = col_template1 if i % 2 == 0 else col_template2
            with col:
                if st.button(template, key=f"template_{i}"):
                    st.info(f"Loading template: {template}")
    
    with col2:
        st.markdown("#### Communication Stats")
        
        comm_stats = [
            ("Messages Sent", "156"),
            ("This Month", "23"),
            ("Read Rate", "94.2%"),
            ("Avg Response Time", "4.2 hrs")
        ]
        
        for label, value in comm_stats:
            st.metric(label, value)
        
        st.markdown("#### Message Status")
        
        message_status = [
            ("✅ Read", "89%"),
            ("📤 Delivered", "8%"),
            ("❌ Unread", "3%")
        ]
        
        for status, percentage in message_status:
            st.write(f"{status}: {percentage}")
        
        st.markdown("#### Quick Actions")
        
        if st.button("📢 Send Announcement"):
            st.info("Opening announcement composer...")
        if st.button("📊 Communication Report"):
            st.info("Generating communication analytics...")
        if st.button("⚙️ Notification Settings"):
            st.info("Opening notification preferences...")

def show_portal_settings():
    st.subheader("🔧 Client Portal Configuration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Portal appearance settings
        st.markdown("#### Portal Appearance & Branding")
        
        with st.expander("🎨 Branding Settings"):
            col_brand1, col_brand2 = st.columns(2)
            
            with col_brand1:
                firm_name = st.text_input("Firm Name:", value="LegalDoc Pro")
                portal_title = st.text_input("Portal Title:", value="Client Portal")
                primary_color = st.color_picker("Primary Color:", value="#1f77b4")
                secondary_color = st.color_picker("Secondary Color:", value="#ff7f0e")
            
            with col_brand2:
                logo_upload = st.file_uploader("Upload Logo:", type=['png', 'jpg', 'svg'])
                favicon_upload = st.file_uploader("Upload Favicon:", type=['ico', 'png'])
                
                custom_css = st.text_area("Custom CSS:", placeholder="Enter custom CSS styles...")
            
            if st.button("💾 Save Branding"):
                st.success("Branding settings saved successfully!")
        
        # Access and security settings
        st.markdown("#### Access & Security Settings")
        
        with st.expander("🔒 Security Configuration"):
            col_security1, col_security2 = st.columns(2)
            
            with col_security1:
                two_factor_auth = st.checkbox("Require Two-Factor Authentication", value=True)
                session_timeout = st.selectbox("Session Timeout:", ["30 minutes", "1 hour", "2 hours", "4 hours", "8 hours"])
                password_policy = st.selectbox("Password Policy:", ["Standard", "Strong", "Very Strong"])
                ip_restrictions = st.checkbox("Enable IP Restrictions", value=False)
            
            with col_security2:
                document_watermarks = st.checkbox("Add Watermarks to Documents", value=True)
                download_tracking = st.checkbox("Track Document Downloads", value=True)
                audit_logging = st.checkbox("Enable Audit Logging", value=True)
                auto_logout = st.checkbox("Auto-logout Inactive Users", value=True)
            
            if st.button("🔒 Update Security Settings"):
                st.success("Security settings updated successfully!")
        
        # Feature settings
        st.markdown("#### Feature Configuration")
        
        with st.expander("⚙️ Portal Features"):
            col_features1, col_features2 = st.columns(2)
            
            with col_features1:
                document_sharing = st.checkbox("Document Sharing", value=True)
                messaging = st.checkbox("Client Messaging", value=True)
                billing_access = st.checkbox("Billing & Invoices", value=True)
                calendar_integration = st.checkbox("Calendar Integration", value=True)
            
            with col_features2:
                mobile_app = st.checkbox("Mobile App Access", value=True)
                notifications = st.checkbox("Email Notifications", value=True)
                file_uploads = st.checkbox("Client File Uploads", value=True)
                video_calls = st.checkbox("Video Conferencing", value=False)
            
            if st.button("🔧 Save Feature Settings"):
                st.success("Feature settings saved successfully!")
        
        # Notification settings
        st.markdown("#### Notification Configuration")
        
        with st.expander("📧 Email & Notification Settings"):
            col_notif1, col_notif2 = st.columns(2)
            
            with col_notif1:
                welcome_email = st.checkbox("Send Welcome Email", value=True)
                document_notifications = st.checkbox("Document Share Notifications", value=True)
                reminder_emails = st.checkbox("Appointment Reminders", value=True)
                invoice_notifications = st.checkbox("Invoice Notifications", value=True)
            
            with col_notif2:
                email_frequency = st.selectbox("Email Frequency:", ["Immediate", "Daily Digest", "Weekly Summary"])
                notification_hours = st.selectbox("Send Notifications:", ["Anytime", "Business Hours Only", "Custom Schedule"])
                
                if notification_hours == "Custom Schedule":
                    start_time = st.time_input("Start Time:")
                    end_time = st.time_input("End Time:")
            
            if st.button("📧 Save Notification Settings"):
                st.success("Notification settings saved successfully!")
    
    with col2:
        st.markdown("#### Portal Status")
        
        portal_status = [
            ("Portal Status", "🟢 Online"),
            ("Active Users", "64"),
            ("System Health", "98.5%"),
            ("Uptime", "99.9%")
        ]
        
        for label, value in portal_status:
            st.write(f"**{label}:** {value}")
        
        st.markdown("#### Configuration Backup")
        
        if st.button("💾 Backup Settings"):
            st.info("Creating configuration backup...")
        if st.button("📥 Restore Settings"):
            st.info("Opening restore interface...")
        if st.button("🔄 Reset to Default"):
            st.warning("This will reset all settings to default!")
        
        st.markdown("#### Support & Help")
        
        if st.button("📖 Portal Documentation"):
            st.info("Opening portal documentation...")
        if st.button("🎥 Video Tutorials"):
            st.info("Loading video tutorials...")
        if st.button("💬 Contact Support"):
            st.info("Opening support chat...")

def show_usage_analytics():
    st.subheader("📊 Portal Usage Analytics")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Usage metrics
        st.markdown("#### Portal Usage Overview")
        
        # Generate sample usage data
        dates = pd.date_range('2024-09-01', '2024-09-23', freq='D')
        usage_data = pd.DataFrame({
            'Date': dates,
            'Daily Logins': [45 + i*2 + (i%7)*10 for i in range(len(dates))],
            'Document Views': [120 + i*5 + (i%7)*20 for i in range(len(dates))],
            'Messages Sent': [25 + i*1 + (i%7)*5 for i in range(len(dates))]
        })
        
        fig = px.line(usage_data, x='Date', y=['Daily Logins', 'Document Views', 'Messages Sent'],
                     title='Portal Activity Trends')
        st.plotly_chart(fig, use_container_width=True)
        
        # Feature usage analytics
        st.markdown("#### Feature Usage Statistics")
        
        feature_usage = pd.DataFrame({
            'Feature': ['Document Viewing', 'Document Downloads', 'Messaging', 'Billing Access', 'File Uploads', 'Calendar'],
            'Usage Count': [1247, 892, 567, 445, 234, 123],
            'Unique Users': [87, 76, 45, 67, 23, 34],
            'Avg Session Time': [8.5, 3.2, 12.4, 6.7, 4.1, 2.8]
        })
        
        fig2 = px.bar(feature_usage, x='Feature', y='Usage Count',
                     color='Unique Users', color_continuous_scale='viridis',
                     title='Feature Usage by Count and Users')
        st.plotly_chart(fig2, use_container_width=True)
        
        # Client engagement analysis
        st.markdown("#### Client Engagement Analysis")
        
        engagement_data = pd.DataFrame({
            'Client': ['ABC Corporation', 'Tech Solutions Inc', 'Startup Innovations', 'Global Manufacturing', 'Continental Corp'],
            'Login Frequency': [23, 18, 12, 15, 8],
            'Documents Accessed': [45, 34, 12, 28, 16],
            'Messages Sent': [12, 8, 4, 9, 3],
            'Engagement Score': [85, 72, 45, 68, 38]
        })
        
        fig3 = px.scatter(engagement_data, x='Login Frequency', y='Documents Accessed',
                         size='Messages Sent', color='Engagement Score',
                         hover_name='Client', title='Client Engagement Matrix')
        st.plotly_chart(fig3, use_container_width=True)
        
        # Popular content
        st.markdown("#### Most Accessed Content")
        
        popular_content = [
            {"document": "Contract Templates", "views": 234, "downloads": 89},
            {"document": "Monthly Invoices", "views": 189, "downloads": 156},
            {"document": "Legal Updates", "views": 167, "downloads": 45},
            {"document": "Meeting Minutes", "views": 134, "downloads": 67},
            {"document": "Compliance Reports", "views": 98, "downloads": 34}
        ]
        
        for content in popular_content:
            col_content1, col_content2, col_content3 = st.columns([2, 1, 1])
            with col_content1:
                st.write(f"**{content['document']}**")
            with col_content2:
                st.write(f"{content['views']} views")
            with col_content3:
                st.write(f"{content['downloads']} downloads")
    
    with col2:
        st.markdown("#### Usage Summary")
        
        usage_summary = [
            ("Total Page Views", "12,847"),
            ("Unique Visitors", "87"),
            ("Avg Session Duration", "14.2 min"),
            ("Bounce Rate", "12.3%")
        ]
        
        for label, value in usage_summary:
            st.metric(label, value)
        
        st.markdown("#### Top Active Clients")
        
        top_clients = [
            ("ABC Corporation", "142 sessions"),
            ("Tech Solutions Inc", "89 sessions"),
            ("Global Manufacturing", "67 sessions"),
            ("Startup Innovations", "45 sessions"),
            ("Continental Corp", "23 sessions")
        ]
        
        for client, sessions in top_clients:
            st.write(f"**{client}:** {sessions}")
        
        st.markdown("#### Usage Reports")
        
        if st.button("📊 Daily Report"):
            st.info("Generating daily usage report...")
        if st.button("📈 Weekly Summary"):
            st.info("Creating weekly summary...")
        if st.button("📉 Monthly Analytics"):
            st.info("Compiling monthly analytics...")
        if st.button("📋 Export Data"):
            st.info("Preparing data export...")

# Main execution
if __name__ == "__main__":
    show()
