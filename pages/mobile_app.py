import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

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
    .ai-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        margin: 0;
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
        <h1>AI Legal Insights</h1>
        <p>AI-powered document analysis, contract review, and legal intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mobile app tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 App Analytics", 
        "👥 User Management", 
        "🔧 Feature Control", 
        "📲 Push Notifications", 
        "🏪 App Store Management"
    ])
    
    with tab1:
        show_app_analytics()
    
    with tab2:
        show_user_management()
    
    with tab3:
        show_feature_control()
    
    with tab4:
        show_push_notifications()
    
    with tab5:
        show_app_store_management()

def show_app_analytics():
    st.subheader("📊 Mobile App Analytics Dashboard")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Key metrics
        col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
        
        with col_metric1:
            st.metric("Total Downloads", "12,847", "+847")
        with col_metric2:
            st.metric("Active Users", "8,234", "+234")
        with col_metric3:
            st.metric("Session Duration", "18.4 min", "+2.1 min")
        with col_metric4:
            st.metric("App Rating", "4.7/5", "+0.1")
        
        # Usage trends
        st.markdown("#### Usage Trends")
        
        # Generate sample data for charts
        dates = pd.date_range('2024-09-01', '2024-09-23', freq='D')
        usage_data = pd.DataFrame({
            'Date': dates,
            'Daily Active Users': [3400 + i*50 + (i%7)*200 for i in range(len(dates))],
            'Sessions': [8500 + i*120 + (i%7)*400 for i in range(len(dates))],
            'Screen Time (min)': [15.2 + (i%10)*0.8 for i in range(len(dates))]
        })
        
        fig = px.line(usage_data, x='Date', y=['Daily Active Users', 'Sessions'], 
                     title='User Engagement Over Time')
        st.plotly_chart(fig, use_container_width=True)
        
        # Feature usage analytics
        st.markdown("#### Feature Usage Analytics")
        
        feature_usage = pd.DataFrame({
            'Feature': ['Document Viewer', 'Calendar', 'Time Tracking', 'Search', 'Notifications', 'Chat', 'Tasks', 'Reports'],
            'Usage %': [89, 76, 68, 84, 95, 45, 72, 34],
            'User Rating': [4.6, 4.3, 4.1, 4.5, 4.8, 3.9, 4.2, 3.7]
        })
        
        fig2 = px.scatter(feature_usage, x='Usage %', y='User Rating', 
                         size='Usage %', color='User Rating',
                         hover_name='Feature', title='Feature Performance Matrix')
        st.plotly_chart(fig2, use_container_width=True)
        
        # Platform breakdown
        st.markdown("#### Platform Distribution")
        
        col_platform1, col_platform2 = st.columns(2)
        
        with col_platform1:
            platform_data = pd.DataFrame({
                'Platform': ['iOS', 'Android'],
                'Users': [4950, 3284],
                'Percentage': [60.1, 39.9]
            })
            
            fig3 = px.pie(platform_data, values='Users', names='Platform',
                         title='Users by Platform')
            st.plotly_chart(fig3, use_container_width=True)
        
        with col_platform2:
            version_data = pd.DataFrame({
                'Version': ['v2.1.3', 'v2.1.2', 'v2.1.1', 'v2.0.x', 'Older'],
                'Users': [5247, 2134, 892, 456, 105],
                'Percentage': [63.7, 25.9, 10.8, 5.5, 1.3]
            })
            
            fig4 = px.bar(version_data, x='Version', y='Users',
                         title='App Version Distribution')
            st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        st.markdown("#### Real-time Metrics")
        
        # Live metrics
        realtime_metrics = [
            ("Current Active Users", "1,247"),
            ("Sessions Today", "3,892"),
            ("App Opens (24h)", "12,450"),
            ("Crash Rate", "0.02%")
        ]
        
        for label, value in realtime_metrics:
            st.metric(label, value)
        
        st.markdown("#### Top Countries")
        
        countries = [
            ("🇺🇸 United States", "45.2%"),
            ("🇨🇦 Canada", "18.7%"),
            ("🇬🇧 United Kingdom", "12.4%"),
            ("🇦🇺 Australia", "8.9%"),
            ("🇩🇪 Germany", "6.1%"),
            ("🇫🇷 France", "4.8%"),
            ("🌍 Others", "3.9%")
        ]
        
        for country, percentage in countries:
            st.write(f"{country}: {percentage}")
        
        st.markdown("#### Performance Alerts")
        
        alerts = [
            ("🟢 Normal", "All systems operational"),
            ("🟡 Warning", "Increased crash rate on Android"),
            ("🟢 Normal", "Server response times good"),
            ("🟢 Normal", "Push notifications working")
        ]
        
        for severity, message in alerts:
            if "Warning" in severity:
                st.warning(f"{severity}: {message}")
            else:
                st.success(f"{severity}: {message}")

def show_user_management():
    st.subheader("👥 Mobile App User Management")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # User search and filters
        st.markdown("#### User Search & Management")
        
        col_search1, col_search2, col_search3 = st.columns(3)
        with col_search1:
            user_search = st.text_input("Search Users:", placeholder="Email, name, or ID...")
        with col_search2:
            user_filter = st.selectbox("Filter by:", ["All Users", "Active", "Inactive", "Premium", "Free Trial"])
        with col_search3:
            platform_filter = st.selectbox("Platform:", ["All", "iOS", "Android"])
        
        # User list
        users = [
            {
                "id": "U001",
                "name": "John Smith",
                "email": "john.smith@lawfirm.com",
                "platform": "iOS",
                "version": "v2.1.3",
                "last_active": "2024-09-23 10:30 AM",
                "subscription": "Premium",
                "sessions_today": 7,
                "total_sessions": 247
            },
            {
                "id": "U002",
                "name": "Sarah Johnson",
                "email": "s.johnson@legalcorp.com",
                "platform": "Android",
                "version": "v2.1.2",
                "last_active": "2024-09-23 09:45 AM",
                "subscription": "Premium",
                "sessions_today": 4,
                "total_sessions": 189
            },
            {
                "id": "U003",
                "name": "Mike Davis",
                "email": "mdavis@attorney.net",
                "platform": "iOS",
                "version": "v2.1.3",
                "last_active": "2024-09-22 06:20 PM",
                "subscription": "Free Trial",
                "sessions_today": 2,
                "total_sessions": 45
            },
            {
                "id": "U004",
                "name": "Emily Chen",
                "email": "emily.chen@lawpartners.com",
                "platform": "Android",
                "version": "v2.1.1",
                "last_active": "2024-09-23 08:15 AM",
                "subscription": "Premium",
                "sessions_today": 5,
                "total_sessions": 156
            }
        ]
        
        for user in users:
            platform_icon = "🍎" if user["platform"] == "iOS" else "🤖"
            subscription_icon = "⭐" if user["subscription"] == "Premium" else "🆓"
            
            with st.expander(f"{platform_icon} {subscription_icon} {user['name']} ({user['email']})"):
                col_user1, col_user2, col_user3 = st.columns(3)
                
                with col_user1:
                    st.write(f"**User ID:** {user['id']}")
                    st.write(f"**Platform:** {user['platform']}")
                    st.write(f"**App Version:** {user['version']}")
                
                with col_user2:
                    st.write(f"**Subscription:** {user['subscription']}")
                    st.write(f"**Last Active:** {user['last_active']}")
                    st.write(f"**Sessions Today:** {user['sessions_today']}")
                
                with col_user3:
                    st.write(f"**Total Sessions:** {user['total_sessions']}")
                    st.progress(min(user['sessions_today'] / 10, 1.0))
                    st.write("Activity Level")
                
                # User actions
                col_action1, col_action2, col_action3, col_action4 = st.columns(4)
                with col_action1:
                    st.button("👁️ View Profile", key=f"profile_{user['id']}")
                with col_action2:
                    st.button("📧 Send Message", key=f"message_{user['id']}")
                with col_action3:
                    st.button("🔒 Manage Access", key=f"access_{user['id']}")
                with col_action4:
                    st.button("📊 Usage Report", key=f"report_{user['id']}")
        
        # Bulk actions
        st.markdown("#### Bulk User Actions")
        
        col_bulk1, col_bulk2, col_bulk3, col_bulk4 = st.columns(4)
        with col_bulk1:
            if st.button("📧 Send Announcement"):
                st.info("Opening announcement composer...")
        with col_bulk2:
            if st.button("📊 Export User Data"):
                st.info("Preparing user data export...")
        with col_bulk3:
            if st.button("🔄 Force App Update"):
                st.info("Initiating app update notification...")
        with col_bulk4:
            if st.button("📈 Engagement Campaign"):
                st.info("Starting engagement campaign...")
    
    with col2:
        st.markdown("#### User Statistics")
        
        user_stats = [
            ("Total Registered", "12,847"),
            ("Active (30 days)", "8,234"),
            ("Premium Users", "3,456"),
            ("Free Trial Users", "1,892")
        ]
        
        for label, value in user_stats:
            st.metric(label, value)
        
        st.markdown("#### User Segmentation")
        
        segments = [
            ("Power Users (>50 sessions)", "15%"),
            ("Regular Users (10-50)", "45%"),
            ("Casual Users (1-10)", "30%"),
            ("Inactive Users", "10%")
        ]
        
        for segment, percentage in segments:
            st.write(f"**{segment}:** {percentage}")
        
        st.markdown("#### Recent Signups")
        
        recent_signups = [
            ("Today", 23),
            ("Yesterday", 31),
            ("This Week", 187),
            ("This Month", 723)
        ]
        
        for period, count in recent_signups:
            st.write(f"**{period}:** {count} users")

def show_feature_control():
    st.subheader("🔧 Feature Control & Configuration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Feature Toggle Management")
        
        # Feature toggles
        features = [
            {
                "name": "Document Scanner",
                "description": "AI-powered document scanning and OCR",
                "status": "Enabled",
                "rollout": "100%",
                "platform": "Both",
                "version": "v2.1.0+",
                "users_affected": 8234
            },
            {
                "name": "Voice Dictation",
                "description": "Voice-to-text for notes and documents",
                "status": "Beta",
                "rollout": "25%",
                "platform": "iOS",
                "version": "v2.1.3+",
                "users_affected": 1247
            },
            {
                "name": "Offline Mode",
                "description": "Access documents without internet",
                "status": "Enabled",
                "rollout": "100%",
                "platform": "Both",
                "version": "v2.0.0+",
                "users_affected": 8234
            },
            {
                "name": "Dark Mode",
                "description": "Dark theme for better readability",
                "status": "Enabled",
                "rollout": "100%",
                "platform": "Both",
                "version": "v1.9.0+",
                "users_affected": 8234
            },
            {
                "name": "Biometric Login",
                "description": "Fingerprint and face ID authentication",
                "status": "Pilot",
                "rollout": "10%",
                "platform": "Both",
                "version": "v2.1.2+",
                "users_affected": 823
            },
            {
                "name": "AI Legal Assistant",
                "description": "AI-powered legal research and Q&A",
                "status": "Development",
                "rollout": "0%",
                "platform": "Both",
                "version": "v2.2.0+",
                "users_affected": 0
            }
        ]
        
        for feature in features:
            status_colors = {
                "Enabled": "🟢",
                "Beta": "🟡",
                "Pilot": "🔵",
                "Development": "🟠",
                "Disabled": "🔴"
            }
            
            with st.expander(f"{status_colors[feature['status']]} {feature['name']} - {feature['status']}"):
                col_feat1, col_feat2 = st.columns(2)
                
                with col_feat1:
                    st.write(f"**Description:** {feature['description']}")
                    st.write(f"**Platform:** {feature['platform']}")
                    st.write(f"**Min Version:** {feature['version']}")
                
                with col_feat2:
                    st.write(f"**Rollout:** {feature['rollout']}")
                    st.write(f"**Users Affected:** {feature['users_affected']:,}")
                    
                    rollout_pct = int(feature['rollout'].replace('%', ''))
                    st.progress(rollout_pct / 100)
                
                # Feature controls
                col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns(4)
                with col_ctrl1:
                    if feature['status'] != "Development":
                        st.button("⚙️ Configure", key=f"config_{feature['name']}")
                    else:
                        st.button("🚀 Deploy", key=f"deploy_{feature['name']}")
                with col_ctrl2:
                    st.button("📊 Analytics", key=f"analytics_{feature['name']}")
                with col_ctrl3:
                    if feature['status'] == "Enabled":
                        st.button("⏸️ Disable", key=f"disable_{feature['name']}")
                    else:
                        st.button("▶️ Enable", key=f"enable_{feature['name']}")
                with col_ctrl4:
                    st.button("🧪 A/B Test", key=f"test_{feature['name']}")
        
        st.markdown("#### App Configuration")
        
        with st.expander("🎨 UI/UX Settings"):
            col_ui1, col_ui2 = st.columns(2)
            
            with col_ui1:
                default_theme = st.selectbox("Default Theme:", ["Light", "Dark", "Auto"])
                navigation_style = st.selectbox("Navigation:", ["Bottom Tabs", "Side Menu", "Hybrid"])
                font_size = st.selectbox("Default Font Size:", ["Small", "Medium", "Large"])
            
            with col_ui2:
                animation_level = st.selectbox("Animations:", ["None", "Reduced", "Standard", "Enhanced"])
                gesture_controls = st.checkbox("Enable Gesture Controls", value=True)
                haptic_feedback = st.checkbox("Haptic Feedback", value=True)
            
            if st.button("💾 Save UI Settings"):
                st.success("UI settings saved successfully!")
    
    with col2:
        st.markdown("#### Feature Analytics")
        
        feature_metrics = [
            ("Active Features", "8"),
            ("Beta Features", "2"),
            ("Development", "3"),
            ("User Adoption", "78%")
        ]
        
        for label, value in feature_metrics:
            st.metric(label, value)
        
        st.markdown("#### Rollout Schedule")
        
        upcoming_features = [
            ("AI Assistant", "Oct 15, 2024"),
            ("Advanced Search", "Nov 1, 2024"),
            ("Team Collaboration", "Nov 15, 2024"),
            ("Video Calls", "Dec 1, 2024")
        ]
        
        for feature, date in upcoming_features:
            st.write(f"**{feature}:** {date}")
        
        st.markdown("#### Quick Actions")
        
        if st.button("📱 Submit iOS Update"):
            st.info("Preparing iOS app submission...")
        if st.button("🤖 Submit Android Update"):
            st.info("Preparing Android app submission...")
        if st.button("📊 Download Reports"):
            st.info("Generating app store reports...")
        if st.button("🔔 Review Alerts"):
            st.info("Checking for new reviews and alerts...")
        if st.button("🚨 Emergency Disable"):
            st.warning("Emergency feature disable activated!")
        if st.button("📋 Feature Report"):
            st.info("Generating feature usage report...")
        if st.button("🔄 Sync Settings"):
            st.info("Syncing settings across platforms...")

def show_push_notifications():
    st.subheader("📲 Push Notification Management")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### Send Push Notification")
        
        with st.form("push_notification"):
            col_push1, col_push2 = st.columns(2)
            
            with col_push1:
                notification_title = st.text_input("Notification Title:", placeholder="Enter notification title...")
                notification_message = st.text_area("Message:", placeholder="Enter notification message...")
                notification_type = st.selectbox("Type:", ["General", "Feature Update", "Reminder", "Alert", "Promotion"])
            
            with col_push2:
                target_audience = st.selectbox("Target Audience:", ["All Users", "Premium Users", "Free Users", "Inactive Users", "Specific Segment"])
                platforms = st.multiselect("Platforms:", ["iOS", "Android"], default=["iOS", "Android"])
                send_time = st.selectbox("Send Time:", ["Send Now", "Schedule for Later"])
                
                if send_time == "Schedule for Later":
                    scheduled_date = st.date_input("Schedule Date:")
                    scheduled_time = st.time_input("Schedule Time:")
            
            # Advanced options
            with st.expander("🔧 Advanced Options"):
                col_adv1, col_adv2 = st.columns(2)
                
                with col_adv1:
                    priority = st.selectbox("Priority:", ["Normal", "High", "Low"])
                    badge_count = st.number_input("Badge Count:", min_value=0, max_value=99, value=1)
                    sound = st.selectbox("Sound:", ["Default", "Custom", "Silent"])
                
                with col_adv2:
                    deep_link = st.text_input("Deep Link:", placeholder="app://feature/page")
                    expiry_time = st.selectbox("Expiry:", ["24 hours", "7 days", "30 days", "Never"])
                    track_opens = st.checkbox("Track Opens", value=True)
            
            # Submit button
            if st.form_submit_button("📤 Send Notification", type="primary"):
                st.success("Push notification sent successfully!")
                st.info(f"Sent to approximately {8234 if target_audience == 'All Users' else 3456} users")
        
        st.markdown("#### Notification History")
        
        notification_history = [
            {
                "title": "New Feature: Voice Dictation",
                "message": "Try our new voice-to-text feature in the latest update!",
                "sent_date": "2024-09-23 09:00 AM",
                "recipients": 8234,
                "opened": 4521,
                "clicked": 1247,
                "type": "Feature Update"
            },
            {
                "title": "Reminder: Complete Your Profile",
                "message": "Complete your profile to get personalized recommendations.",
                "sent_date": "2024-09-22 02:00 PM",
                "recipients": 1892,
                "opened": 756,
                "clicked": 234,
                "type": "Reminder"
            },
            {
                "title": "System Maintenance Notice",
                "message": "Scheduled maintenance tonight from 11 PM to 1 AM EST.",
                "sent_date": "2024-09-21 06:00 PM",
                "recipients": 8234,
                "opened": 6789,
                "clicked": 123,
                "type": "Alert"
            }
        ]
        
        for notification in notification_history:
            open_rate = (notification['opened'] / notification['recipients']) * 100
            click_rate = (notification['clicked'] / notification['recipients']) * 100
            
            with st.expander(f"📧 {notification['title']} - {notification['sent_date']}"):
                col_hist1, col_hist2, col_hist3 = st.columns(3)
                
                with col_hist1:
                    st.write(f"**Message:** {notification['message']}")
                    st.write(f"**Type:** {notification['type']}")
                    st.write(f"**Recipients:** {notification['recipients']:,}")
                
                with col_hist2:
                    st.write(f"**Opened:** {notification['opened']:,} ({open_rate:.1f}%)")
                    st.write(f"**Clicked:** {notification['clicked']:,} ({click_rate:.1f}%)")
                    st.progress(open_rate / 100)
                
                with col_hist3:
                    st.button("📊 View Analytics", key=f"analytics_{notification['title'][:10]}")
                    st.button("🔄 Resend", key=f"resend_{notification['title'][:10]}")
                    st.button("📋 Duplicate", key=f"duplicate_{notification['title'][:10]}")
    
    with col2:
        st.markdown("#### Notification Stats")
        
        notification_stats = [
            ("Sent Today", "3"),
            ("Total This Month", "47"),
            ("Avg Open Rate", "67.2%"),
            ("Avg Click Rate", "18.4%")
        ]
        
        for label, value in notification_stats:
            st.metric(label, value)
        
        st.markdown("#### Notification Settings")
        
        notification_settings = [
            ("Enable Notifications", True),
            ("Rich Media Support", True),
            ("Location-Based", False),
            ("Time Zone Aware", True),
            ("A/B Testing", True)
        ]
        
        for setting, enabled in notification_settings:
            col_set1, col_set2 = st.columns([3, 1])
            with col_set1:
                st.write(setting)
            with col_set2:
                st.checkbox("", value=enabled, key=f"setting_{setting}")
        
        st.markdown("#### Templates")
        
        templates = [
            "🎉 Feature Announcement",
            "⏰ Reminder Notice",
            "🚨 System Alert",
            "📢 General Update",
            "🎯 Promotional"
        ]
        
        for template in templates:
            if st.button(template, key=f"template_{template[:5]}"):
                st.info(f"Loading template: {template}")

def show_app_store_management():
    st.subheader("🏪 App Store Management")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### App Store Performance")
        
        # App store metrics for both platforms
        store_metrics = {
            "iOS App Store": {
                "current_version": "v2.1.3",
                "rating": 4.7,
                "reviews": 1247,
                "downloads_week": 234,
                "ranking": "#12 in Legal",
                "approval_status": "Approved",
                "last_update": "2024-09-20"
            },
            "Google Play Store": {
                "current_version": "v2.1.2",
                "rating": 4.5,
                "reviews": 892,
                "downloads_week": 189,
                "ranking": "#18 in Business",
                "approval_status": "Approved",
                "last_update": "2024-09-18"
            }
        }
        
        for store, metrics in store_metrics.items():
            platform_icon = "🍎" if "iOS" in store else "🤖"
            
            with st.expander(f"{platform_icon} {store}"):
                col_store1, col_store2, col_store3 = st.columns(3)
                
                with col_store1:
                    st.write(f"**Current Version:** {metrics['current_version']}")
                    st.write(f"**Rating:** {metrics['rating']}/5.0")
                    st.write(f"**Total Reviews:** {metrics['reviews']:,}")
                
                with col_store2:
                    st.write(f"**Downloads (7 days):** {metrics['downloads_week']:,}")
                    st.write(f"**Category Ranking:** {metrics['ranking']}")
                    st.write(f"**Status:** {metrics['approval_status']}")
                
                with col_store3:
                    st.write(f"**Last Update:** {metrics['last_update']}")
                    
                    # Rating stars visualization
                    star_rating = "⭐" * int(metrics['rating']) + "☆" * (5 - int(metrics['rating']))
                    st.write(f"**Visual Rating:** {star_rating}")
                
                # Store actions
                col_action1, col_action2, col_action3, col_action4 = st.columns(4)
                with col_action1:
                    st.button("📤 Submit Update", key=f"update_{store}")
                with col_action2:
                    st.button("📊 Store Analytics", key=f"store_analytics_{store}")
                with col_action3:
                    st.button("💬 Manage Reviews", key=f"reviews_{store}")
                with col_action4:
                    st.button("🎯 ASO Tools", key=f"aso_{store}")
        
        st.markdown("#### App Store Optimization (ASO)")
        
        with st.expander("🎯 ASO Management"):
            col_aso1, col_aso2 = st.columns(2)
            
            with col_aso1:
                st.markdown("##### Keywords")
                current_keywords = st.text_area("Current Keywords:", 
                    value="legal document management, law firm software, legal calendar, attorney tools, case management")
                
                st.markdown("##### App Description")
                app_description = st.text_area("App Description:", 
                    value="Professional legal document management solution for law firms and legal professionals...")
            
            with col_aso2:
                st.markdown("##### Keyword Rankings")
                keyword_rankings = [
                    ("legal software", "#8"),
                    ("law firm app", "#15"),
                    ("document management", "#23"),
                    ("legal calendar", "#6"),
                    ("attorney tools", "#12")
                ]
                
                for keyword, rank in keyword_rankings:
                    col_kw1, col_kw2 = st.columns([3, 1])
                    with col_kw1:
                        st.write(f"**{keyword}**")
                    with col_kw2:
                        st.write(rank)
                
                st.markdown("##### Competitor Analysis")
                competitors = [
                    ("LegalZoom Mobile", "4.2★", "#5"),
                    ("Clio Mobile", "4.4★", "#9"),
                    ("MyCase", "4.1★", "#14")
                ]
                
                for comp, rating, rank in competitors:
                    st.write(f"**{comp}:** {rating} - {rank}")
        
        st.markdown("#### Review Management")
        
        recent_reviews = [
            {
                "platform": "iOS",
                "rating": 5,
                "title": "Excellent app for managing legal docs",
                "review": "This app has revolutionized how our firm handles documents. Great UI and features!",
                "author": "AttorneyJohn",
                "date": "2024-09-22",
                "responded": False
            },
            {
                "platform": "Android",
                "rating": 4,
                "title": "Good app, could use more features",
                "review": "Overall solid app, but would love to see voice dictation added soon.",
                "author": "LegalEagle23",
                "date": "2024-09-21",
                "responded": True
            },
            {
                "platform": "iOS",
                "rating": 2,
                "title": "App crashes frequently",
                "review": "The app keeps crashing when I try to open large PDF files. Please fix!",
                "author": "FrustratedUser",
                "date": "2024-09-20",
                "responded": False
            }
        ]
        
        for review in recent_reviews:
            platform_icon = "🍎" if review["platform"] == "iOS" else "🤖"
            star_display = "⭐" * review["rating"] + "☆" * (5 - review["rating"])
            response_status = "✅ Responded" if review["responded"] else "❌ Needs Response"
            
            with st.expander(f"{platform_icon} {star_display} {review['title']} - {response_status}"):
                st.write(f"**Author:** {review['author']} | **Date:** {review['date']}")
                st.write(f"**Review:** {review['review']}")
                
                if not review["responded"]:
                    response_text = st.text_area("Response:", key=f"response_{review['author']}")
                    if st.button("📤 Send Response", key=f"send_response_{review['author']}"):
                        st.success("Response sent successfully!")
                else:
                    st.info("Developer response already sent")
    
    with col2:
        st.markdown("#### Release Management")
        
        release_info = [
            ("Current Version", "v2.1.3"),
            ("Next Release", "v2.2.0"),
            ("Release Date", "Oct 15, 2024"),
            ("Beta Testers", "150")
        ]
        
        for label, value in release_info:
            st.metric(label, value)
        
        st.markdown("#### App Store Health")
        
        health_metrics = [
            ("iOS Health Score", "94%", "🟢"),
            ("Android Health Score", "91%", "🟢"),
            ("Crash Rate", "0.02%", "🟢"),
            ("Review Sentiment", "Positive", "🟢")
        ]
        
        for metric, value, status in health_metrics:
            col_health1, col_health2 = st.columns([3, 1])
            with col_health1:
                st.write(f"**{metric}:** {value}")
            with col_health2:
                st.write(status)
        
        st.markdown("#### Quick Actions")
        
        quick_actions = [
            ("📈 View Analytics", "View detailed app analytics"),
            ("🔄 Refresh Data", "Update all app store data"),
            ("📊 Export Report", "Download performance report"),
            ("⚠️ Check Issues", "Review any app store issues"),
            ("🎯 ASO Optimization", "Run ASO analysis"),
            ("📱 Version Compare", "Compare version performance")
        ]
        
        for action, description in quick_actions:
            if st.button(action, key=f"quick_{action[:5]}"):
                st.info(f"{description}")

# Additional utility functions for the mobile app dashboard
def get_app_health_score():
    """Calculate overall app health score based on various metrics"""
    crash_rate = 0.02
    rating = 4.6
    user_retention = 78.5
    
    # Simple health score calculation
    health_score = (100 - crash_rate) * 0.3 + (rating / 5 * 100) * 0.4 + user_retention * 0.3
    return round(health_score, 1)

def generate_user_engagement_data():
    """Generate sample user engagement data for charts"""
    dates = pd.date_range('2024-08-01', '2024-09-23', freq='D')
    
    engagement_data = pd.DataFrame({
        'Date': dates,
        'Daily Active Users': [3200 + i*30 + (i%7)*150 + (i%30)*10 for i in range(len(dates))],
        'Session Duration': [16.5 + (i%14)*0.5 - (i%7)*0.2 for i in range(len(dates))],
        'Screen Views': [45 + i*2 + (i%7)*8 for i in range(len(dates))],
        'Retention Rate': [82.5 + (i%21)*0.3 - (i%14)*0.1 for i in range(len(dates))]
    })
    
    return engagement_data

def calculate_feature_adoption_rate(feature_name, total_users=8234):
    """Calculate adoption rate for specific features"""
    adoption_rates = {
        'Document Scanner': 0.89,
        'Voice Dictation': 0.25,
        'Offline Mode': 1.0,
        'Dark Mode': 0.95,
        'Biometric Login': 0.45,
        'AI Legal Assistant': 0.0
    }
    
    rate = adoption_rates.get(feature_name, 0.5)
    return int(total_users * rate), f"{rate*100:.1f}%"

# Main execution
if __name__ == "__main__":
    show()
