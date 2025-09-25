# services/subscription_manager.py - Complete subscription plan enforcement
import streamlit as st
from datetime import datetime, timedelta
from enum import Enum
import uuid
import json

class SubscriptionPlan(Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    TRIAL = "trial"

class SubscriptionStatus(Enum):
    ACTIVE = "active"
    TRIAL = "trial"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"

class SubscriptionManager:
    def __init__(self):
        self.initialize_subscription_data()
    
    def initialize_subscription_data(self):
        """Initialize subscription data in session state"""
        if 'subscriptions' not in st.session_state:
            st.session_state.subscriptions = {}
        
        if 'usage_tracking' not in st.session_state:
            st.session_state.usage_tracking = {}
    
    def get_plan_limits(self, plan):
        """Get limits for each subscription plan"""
        plan_limits = {
            SubscriptionPlan.STARTER.value: {
                "max_users": 5,
                "storage_gb": 10,
                "ai_features": ["basic_analysis", "document_extraction", "simple_risk_scoring"],
                "support_level": "standard",
                "custom_integrations": False,
                "white_label": False,
                "batch_processing": False,
                "advanced_analytics": False,
                "predictive_insights": False,
                "monthly_cost": 99
            },
            SubscriptionPlan.PROFESSIONAL.value: {
                "max_users": 25,
                "storage_gb": 50,
                "ai_features": ["basic_analysis", "document_extraction", "advanced_contract_review", 
                              "batch_processing", "risk_scoring", "compliance_check"],
                "support_level": "priority",
                "custom_integrations": True,
                "white_label": True,
                "batch_processing": True,
                "advanced_analytics": True,
                "predictive_insights": False,
                "monthly_cost": 299
            },
            SubscriptionPlan.ENTERPRISE.value: {
                "max_users": 999999,  # Unlimited
                "storage_gb": 200,
                "ai_features": ["all"],  # All AI features
                "support_level": "dedicated",
                "custom_integrations": True,
                "white_label": True,
                "batch_processing": True,
                "advanced_analytics": True,
                "predictive_insights": True,
                "custom_development": True,
                "onpremises_deployment": True,
                "monthly_cost": 599
            },
            SubscriptionPlan.TRIAL.value: {
                "max_users": 3,
                "storage_gb": 1,
                "ai_features": ["basic_analysis"],
                "support_level": "standard",
                "custom_integrations": False,
                "white_label": False,
                "batch_processing": False,
                "advanced_analytics": False,
                "predictive_insights": False,
                "trial_days": 14,
                "monthly_cost": 0
            }
        }
        return plan_limits.get(plan, {})
    
    def get_organization_subscription(self, org_code):
        """Get subscription details for organization"""
        if org_code not in st.session_state.subscriptions:
            # Create trial subscription for new organizations
            self.create_trial_subscription(org_code)
        
        return st.session_state.subscriptions[org_code]
    
    def create_trial_subscription(self, org_code):
        """Create a trial subscription for new organization"""
        trial_subscription = {
            "organization_code": org_code,
            "plan": SubscriptionPlan.TRIAL.value,
            "status": SubscriptionStatus.TRIAL.value,
            "created_date": datetime.now(),
            "trial_end_date": datetime.now() + timedelta(days=14),
            "current_users": 1,
            "storage_used_gb": 0.0,
            "monthly_cost": 0,
            "billing_email": "",
            "payment_method": None,
            "next_billing_date": None
        }
        
        st.session_state.subscriptions[org_code] = trial_subscription
        return trial_subscription
    
    def check_user_limit(self, org_code):
        """Check if organization can add more users"""
        subscription = self.get_organization_subscription(org_code)
        limits = self.get_plan_limits(subscription["plan"])
        
        current_users = subscription.get("current_users", 0)
        max_users = limits.get("max_users", 0)
        
        return current_users < max_users
    
    def check_storage_limit(self, org_code, file_size_mb):
        """Check if organization can upload more files"""
        subscription = self.get_organization_subscription(org_code)
        limits = self.get_plan_limits(subscription["plan"])
        
        current_storage_gb = subscription.get("storage_used_gb", 0)
        max_storage_gb = limits.get("storage_gb", 0)
        
        new_total_gb = current_storage_gb + (file_size_mb / 1024)
        
        return new_total_gb <= max_storage_gb
    
    def has_ai_feature(self, org_code, feature_name):
        """Check if organization has access to specific AI feature"""
        subscription = self.get_organization_subscription(org_code)
        limits = self.get_plan_limits(subscription["plan"])
        
        allowed_features = limits.get("ai_features", [])
        
        # Enterprise gets all features
        if "all" in allowed_features:
            return True
        
        return feature_name in allowed_features
    
    def can_use_feature(self, org_code, feature_name):
        """Check if organization can use specific platform feature"""
        subscription = self.get_organization_subscription(org_code)
        limits = self.get_plan_limits(subscription["plan"])
        
        feature_map = {
            "batch_processing": limits.get("batch_processing", False),
            "advanced_analytics": limits.get("advanced_analytics", False),
            "predictive_insights": limits.get("predictive_insights", False),
            "custom_integrations": limits.get("custom_integrations", False),
            "white_label": limits.get("white_label", False)
        }
        
        return feature_map.get(feature_name, True)  # Default to True for basic features
    
    def update_storage_usage(self, org_code, file_size_mb, operation="add"):
        """Update storage usage for organization"""
        subscription = self.get_organization_subscription(org_code)
        
        current_storage = subscription.get("storage_used_gb", 0)
        change_gb = file_size_mb / 1024
        
        if operation == "add":
            new_storage = current_storage + change_gb
        elif operation == "remove":
            new_storage = max(0, current_storage - change_gb)
        
        subscription["storage_used_gb"] = round(new_storage, 3)
        st.session_state.subscriptions[org_code] = subscription
    
    def update_user_count(self, org_code, change):
        """Update user count for organization"""
        subscription = self.get_organization_subscription(org_code)
        current_users = subscription.get("current_users", 0)
        
        new_count = max(0, current_users + change)
        subscription["current_users"] = new_count
        st.session_state.subscriptions[org_code] = subscription
    
    def is_subscription_active(self, org_code):
        """Check if subscription is active"""
        subscription = self.get_organization_subscription(org_code)
        status = subscription.get("status")
        
        if status == SubscriptionStatus.TRIAL.value:
            trial_end = subscription.get("trial_end_date")
            if trial_end and datetime.now() > trial_end:
                # Trial expired
                subscription["status"] = SubscriptionStatus.EXPIRED.value
                return False
            return True
        
        return status == SubscriptionStatus.ACTIVE.value
    
    def get_subscription_status_message(self, org_code):
        """Get user-friendly subscription status message"""
        subscription = self.get_organization_subscription(org_code)
        status = subscription.get("status")
        plan = subscription.get("plan", "").title()
        
        if status == SubscriptionStatus.TRIAL.value:
            trial_end = subscription.get("trial_end_date")
            if trial_end:
                days_left = (trial_end - datetime.now()).days
                if days_left > 0:
                    return f"Trial - {days_left} days remaining"
                else:
                    return "Trial expired - Please upgrade"
        
        elif status == SubscriptionStatus.ACTIVE.value:
            return f"{plan} Plan - Active"
        
        elif status == SubscriptionStatus.EXPIRED.value:
            return "Subscription expired - Please renew"
        
        return "Subscription status unknown"
    
    def show_subscription_widget(self, org_code):
        """Show subscription status widget in sidebar"""
        subscription = self.get_organization_subscription(org_code)
        limits = self.get_plan_limits(subscription["plan"])
        
        with st.sidebar:
            st.markdown("### Subscription Status")
            
            # Plan and status
            status_message = self.get_subscription_status_message(org_code)
            if "expired" in status_message.lower() or "upgrade" in status_message.lower():
                st.error(status_message)
            elif "trial" in status_message.lower():
                st.warning(status_message)
            else:
                st.success(status_message)
            
            # Usage metrics
            st.markdown("#### Usage")
            
            # User count
            current_users = subscription.get("current_users", 0)
            max_users = limits.get("max_users", 0)
            if max_users == 999999:
                st.write(f"Users: {current_users} (Unlimited)")
            else:
                user_percentage = min(current_users / max_users, 1.0) if max_users > 0 else 0
                st.progress(user_percentage, text=f"Users: {current_users}/{max_users}")
            
            # Storage usage
            storage_used = subscription.get("storage_used_gb", 0)
            max_storage = limits.get("storage_gb", 0)
            storage_percentage = min(storage_used / max_storage, 1.0) if max_storage > 0 else 0
            st.progress(storage_percentage, text=f"Storage: {storage_used:.1f}GB/{max_storage}GB")
            
            # Upgrade button for non-enterprise plans
            if subscription["plan"] != SubscriptionPlan.ENTERPRISE.value:
                if st.button("⬆️ Upgrade Plan"):
                    st.session_state['show_upgrade_modal'] = True
                    st.rerun()
    
    def show_upgrade_modal(self, org_code):
        """Show subscription upgrade interface"""
        st.subheader("Upgrade Your Subscription")
        
        current_subscription = self.get_organization_subscription(org_code)
        current_plan = current_subscription["plan"]
        
        # Plan comparison
        col1, col2, col3 = st.columns(3)
        
        plans = [
            (SubscriptionPlan.STARTER.value, "Starter", "$99/month"),
            (SubscriptionPlan.PROFESSIONAL.value, "Professional", "$299/month"),
            (SubscriptionPlan.ENTERPRISE.value, "Enterprise", "$599/month")
        ]
        
        for i, (plan_id, plan_name, price) in enumerate(plans):
            with [col1, col2, col3][i]:
                limits = self.get_plan_limits(plan_id)
                
                # Plan card
                if plan_id == current_plan:
                    st.success(f"**{plan_name}** (Current)")
                else:
                    st.info(f"**{plan_name}**")
                
                st.write(f"**{price}**")
                st.write(f"• {limits['max_users']} users" if limits['max_users'] != 999999 else "• Unlimited users")
                st.write(f"• {limits['storage_gb']}GB storage")
                st.write(f"• {limits['support_level'].title()} support")
                
                if plan_id != current_plan:
                    if st.button(f"Select {plan_name}", key=f"select_{plan_id}"):
                        self.upgrade_subscription(org_code, plan_id)
                        st.success(f"Upgraded to {plan_name} plan!")
                        st.rerun()
        
        if st.button("Cancel"):
            st.session_state['show_upgrade_modal'] = False
            st.rerun()
    
    def upgrade_subscription(self, org_code, new_plan):
        """Upgrade organization subscription"""
        subscription = self.get_organization_subscription(org_code)
        
        subscription["plan"] = new_plan
        subscription["status"] = SubscriptionStatus.ACTIVE.value
        subscription["next_billing_date"] = datetime.now() + timedelta(days=30)
        
        new_limits = self.get_plan_limits(new_plan)
        subscription["monthly_cost"] = new_limits["monthly_cost"]
        
        st.session_state.subscriptions[org_code] = subscription
    
    def show_billing_interface(self, org_code):
        """Show billing and payment interface"""
        subscription = self.get_organization_subscription(org_code)
        
        st.subheader("Billing & Payment")
        
        # Current plan info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current Plan", subscription["plan"].title())
        with col2:
            st.metric("Monthly Cost", f"${subscription.get('monthly_cost', 0)}")
        with col3:
            next_billing = subscription.get("next_billing_date")
            if next_billing:
                st.metric("Next Billing", next_billing.strftime("%Y-%m-%d"))
        
        # Payment method
        st.markdown("#### Payment Method")
        payment_method = subscription.get("payment_method")
        
        if payment_method:
            st.success(f"Card ending in {payment_method}")
        else:
            st.warning("No payment method on file")
        
        # Mock payment form
        with st.form("payment_form"):
            st.markdown("#### Update Payment Method")
            
            card_number = st.text_input("Card Number", placeholder="**** **** **** 1234")
            
            col1, col2 = st.columns(2)
            with col1:
                expiry = st.text_input("Expiry", placeholder="MM/YY")
            with col2:
                cvv = st.text_input("CVV", placeholder="123")
            
            billing_email = st.text_input("Billing Email", 
                                        value=subscription.get("billing_email", ""))
            
            if st.form_submit_button("Update Payment Method"):
                # Mock payment processing
                subscription["payment_method"] = card_number[-4:] if card_number else None
                subscription["billing_email"] = billing_email
                st.session_state.subscriptions[org_code] = subscription
                st.success("Payment method updated successfully!")
        
        # Billing history
        st.markdown("#### Billing History")
        
        # Mock billing data
        billing_history = [
            {"date": "2024-10-01", "amount": "$299", "status": "Paid", "invoice": "INV-001"},
            {"date": "2024-09-01", "amount": "$299", "status": "Paid", "invoice": "INV-002"},
            {"date": "2024-08-01", "amount": "$99", "status": "Paid", "invoice": "INV-003"}
        ]
        
        for bill in billing_history:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(bill["date"])
            with col2:
                st.write(bill["amount"])
            with col3:
                if bill["status"] == "Paid":
                    st.success(bill["status"])
                else:
                    st.error(bill["status"])
            with col4:
                st.button(f"📄 {bill['invoice']}", key=f"invoice_{bill['invoice']}")

# Enhanced auth service with subscription enforcement
class EnhancedAuthService:
    def __init__(self):
        self.subscription_manager = SubscriptionManager()
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state"""
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'user_data' not in st.session_state:
            st.session_state.user_data = {}
    
    def show_login(self):
        """Login interface with subscription validation"""
        st.markdown("""
        <div class="main-header">
            <h1>⚖️ LegalDoc Pro</h1>
            <p>Enterprise Legal Management Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            org_code = st.text_input("Organization Code", 
                                    placeholder="Enter your firm's code")
            
            if org_code:
                # Check subscription status
                if self.subscription_manager.is_subscription_active(org_code):
                    status_msg = self.subscription_manager.get_subscription_status_message(org_code)
                    st.success(f"✅ {status_msg}")
                    
                    # Login form
                    with st.form("login_form"):
                        username = st.text_input("Username")
                        password = st.text_input("Password", type="password")
                        
                        col_login1, col_login2 = st.columns(2)
                        
                        with col_login1:
                            login_button = st.form_submit_button("Login", type="primary")
                        with col_login2:
                            demo_button = st.form_submit_button("Demo Login")
                        
                        if login_button or demo_button:
                            if self.authenticate_user(org_code, username, password, demo_button):
                                st.rerun()
                            else:
                                st.error("Invalid credentials")
                
                else:
                    st.error("Subscription expired or inactive. Please contact support.")
                    if st.button("Renew Subscription"):
                        st.session_state['show_upgrade_modal'] = True
                        st.session_state['upgrade_org_code'] = org_code
                        st.rerun()
    
    def authenticate_user(self, org_code, username, password, is_demo=False):
        """Authenticate user with subscription validation"""
        # Mock authentication
        if is_demo or (username and password):
            user_data = {
                'user_id': str(uuid.uuid4()),
                'username': username or 'demo',
                'organization_code': org_code,
                'name': 'Demo User',
                'email': f'{username or "demo"}@{org_code}.com',
                'role': 'subscription_owner',
                'is_subscription_owner': True,
                'login_time': datetime.now()
            }
            
            st.session_state.logged_in = True
            st.session_state.user_data = user_data
            return True
        
        return False
    
    def render_sidebar(self):
        """Render sidebar with subscription info"""
        user_data = st.session_state.get('user_data', {})
        org_code = user_data.get('organization_code')
        
        with st.sidebar:
            st.markdown(f"**👤 {user_data.get('name', 'User')}**")
            st.markdown(f"**🏢 {org_code}**")
            
            # Show subscription widget
            if org_code:
                self.subscription_manager.show_subscription_widget(org_code)
            
            st.divider()
            
            # Navigation with feature gating
            self.show_navigation(org_code)
            
            st.divider()
            
            # Management options for subscription owners
            if user_data.get('is_subscription_owner'):
                if st.button("💳 Billing & Subscription"):
                    st.session_state['show_billing'] = True
                    st.rerun()
            
            if st.button("🚪 Logout"):
                self.logout()
                st.rerun()
    
    def show_navigation(self, org_code):
        """Show navigation with subscription-based restrictions"""
        subscription = self.subscription_manager.get_organization_subscription(org_code)
        
        # Basic pages (available to all plans)
        basic_pages = [
            ("📊", "Executive Dashboard"),
            ("📁", "Document Management"),
            ("⚖️", "Matter Management"),
            ("⏰", "Time & Billing"),
            ("📅", "Calendar & Tasks")
        ]
        
        for icon, page_name in basic_pages:
            if st.button(f"{icon} {page_name}", key=f"nav_{page_name}"):
                st.session_state['current_page'] = page_name
                st.rerun()
        
        # AI features (gated by subscription)
        if self.subscription_manager.has_ai_feature(org_code, "basic_analysis"):
            if st.button("🤖 AI Insights", key="nav_AI Insights"):
                st.session_state['current_page'] = "AI Insights"
                st.rerun()
        else:
            st.button("🤖 AI Insights 🔒", disabled=True, 
                     help="Upgrade to access AI features")
        
        # Advanced features (Professional/Enterprise only)
        if self.subscription_manager.can_use_feature(org_code, "advanced_analytics"):
            advanced_pages = [
                ("🔍", "Advanced Search"),
                ("📈", "Business Intelligence")
            ]
            
            for icon, page_name in advanced_pages:
                if st.button(f"{icon} {page_name}", key=f"nav_{page_name}"):
                    st.session_state['current_page'] = page_name
                    st.rerun()
        
        # Enterprise-only features
        if subscription["plan"] == "enterprise":
            enterprise_pages = [
                ("🔗", "Integrations"),
                ("📱", "Mobile App"),
                ("⚙️", "System Settings")
            ]
            
            for icon, page_name in enterprise_pages:
                if st.button(f"{icon} {page_name}", key=f"nav_{page_name}"):
                    st.session_state['current_page'] = page_name
                    st.rerun()
    
    def has_permission(self, permission):
        """Check permissions with subscription validation"""
        user_data = st.session_state.get('user_data', {})
        org_code = user_data.get('organization_code')
        
        if not org_code:
            return False
        
        # Check subscription status first
        if not self.subscription_manager.is_subscription_active(org_code):
            return False
        
        # Check feature-specific permissions
        feature_permissions = {
            'ai_analysis': lambda: self.subscription_manager.has_ai_feature(org_code, 'basic_analysis'),
            'batch_processing': lambda: self.subscription_manager.can_use_feature(org_code, 'batch_processing'),
            'advanced_analytics': lambda: self.subscription_manager.can_use_feature(org_code, 'advanced_analytics'),
            'white_label': lambda: self.subscription_manager.can_use_feature(org_code, 'white_label')
        }
        
        if permission in feature_permissions:
            return feature_permissions[permission]()
        
        # Default permissions for basic features
        return True
    
    def check_storage_before_upload(self, file_size_mb):
        """Check storage limits before file upload"""
        user_data = st.session_state.get('user_data', {})
        org_code = user_data.get('organization_code')
        
        if org_code:
            return self.subscription_manager.check_storage_limit(org_code, file_size_mb)
        
        return False
    
    def check_user_limit_before_invite(self):
        """Check user limits before adding new users"""
        user_data = st.session_state.get('user_data', {})
        org_code = user_data.get('organization_code')
        
        if org_code:
            return self.subscription_manager.check_user_limit(org_code)
        
        return False
    
    def logout(self):
        """Logout user"""
        keys_to_clear = ['logged_in', 'user_data', 'current_page']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return st.session_state.get('logged_in', False)

# Usage functions
def show_subscription_enforcement_demo():
    """Demo of subscription enforcement in action"""
    auth_service = EnhancedAuthService()
    
    if not auth_service.is_logged_in():
        auth_service.show_login()
        return
    
    # Show upgrade modal if triggered
    if st.session_state.get('show_upgrade_modal'):
        org_code = st.session_state.get('upgrade_org_code') or st.session_state.user_data.get('organization_code')
        auth_service.subscription_manager.show_upgrade_modal(org_code)
        return
    
    # Show billing interface if triggered
    if st.session_state.get('show_billing'):
        org_code = st.session_state.user_data.get('organization_code')
        auth_service.subscription_manager.show_billing_interface(org_code)
        if st.button("← Back"):
            del st.session_state['show_billing']
            st.rerun()
        return
    
    # Render main interface with sidebar
    auth_service.render_sidebar()
    
    # Main content area with feature gating examples
    st.title("Subscription-Enforced Platform")
    
    org_code = st.session_state.user_data.get('organization_code')
    subscription = auth_service.subscription_manager.get_organization_subscription(org_code)
    
    st.write(f"Current Plan: **{subscription['plan'].title()}**")
    
    # Feature testing buttons
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("AI Features")
        if auth_service.has_permission('ai_analysis'):
            st.success("✅ Basic AI Analysis Available")
        else:
            st.error("❌ AI Analysis Requires Upgrade")
        
        if auth_service.has_permission('batch_processing'):
            st.success("✅ Batch Processing Available")
        else:
            st.error("❌ Batch Processing Requires Professional+")
    
    with col2:
        st.subheader("Storage & Users")
        
        # Test file upload limits
        uploaded_file = st.file_uploader("Test File Upload")
        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if auth_service.check_storage_before_upload(file_size_mb):
                st.success(f"✅ File can be uploaded ({file_size_mb:.1f}MB)")
            else:
                st.error("❌ Storage limit exceeded - upgrade needed")
        
        # Test user limits
        if auth_service.check_user_limit_before_invite():
            st.success("✅ Can add more users")
        else:
            st.error("❌ User limit reached - upgrade needed")
