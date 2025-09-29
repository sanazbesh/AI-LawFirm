# services/subscription_manager.py - Complete subscription plan enforcement with account creation
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
                "trial_days": 7,  # Changed to 7 days
                "monthly_cost": 0
            }
        }
        return plan_limits.get(plan, {})
    
    def get_organization_subscription(self, org_code):
        """Get subscription details for organization"""
        return st.session_state.subscriptions.get(org_code, {})
    
    def create_trial_subscription(self, org_code, firm_name="", owner_name="", owner_email=""):
        """Create a trial subscription for new organization"""
        trial_subscription = {
            "organization_code": org_code,
            "organization_name": firm_name,
            "plan": SubscriptionPlan.TRIAL.value,
            "status": SubscriptionStatus.TRIAL.value,
            "created_date": datetime.now(),
            "trial_end_date": datetime.now() + timedelta(days=7),  # 7-day trial
            "current_users": 1,
            "storage_used_gb": 0.0,
            "monthly_cost": 0,
            "billing_email": owner_email,
            "owner_name": owner_name,
            "owner_email": owner_email,
            "payment_method": None,
            "next_billing_date": None
        }
        
        st.session_state.subscriptions[org_code] = trial_subscription
        return trial_subscription
    
    def check_user_limit(self, org_code):
        """Check if organization can add more users"""
        subscription = self.get_organization_subscription(org_code)
        limits = self.get_plan_limits(subscription.get("plan", "trial"))
        
        current_users = subscription.get("current_users", 0)
        max_users = limits.get("max_users", 0)
        
        return current_users < max_users
    
    def check_storage_limit(self, org_code, file_size_mb):
        """Check if organization can upload more files"""
        subscription = self.get_organization_subscription(org_code)
        limits = self.get_plan_limits(subscription.get("plan", "trial"))
        
        current_storage_gb = subscription.get("storage_used_gb", 0)
        max_storage_gb = limits.get("storage_gb", 0)
        
        new_total_gb = current_storage_gb + (file_size_mb / 1024)
        
        return new_total_gb <= max_storage_gb
    
    def has_ai_feature(self, org_code, feature_name):
        """Check if organization has access to specific AI feature"""
        subscription = self.get_organization_subscription(org_code)
        limits = self.get_plan_limits(subscription.get("plan", "trial"))
        
        allowed_features = limits.get("ai_features", [])
        
        # Enterprise gets all features
        if "all" in allowed_features:
            return True
        
        return feature_name in allowed_features
    
    def can_use_feature(self, org_code, feature_name):
        """Check if organization can use specific platform feature"""
        subscription = self.get_organization_subscription(org_code)
        limits = self.get_plan_limits(subscription.get("plan", "trial"))
        
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
        if not subscription:
            return False
            
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
        if not subscription:
            return "No subscription found"
            
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
        if not subscription:
            return
            
        limits = self.get_plan_limits(subscription.get("plan", "trial"))
        
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
            if subscription.get("plan") != SubscriptionPlan.ENTERPRISE.value:
                if st.button("Upgrade Plan"):
                    st.session_state['show_upgrade_modal'] = True
                    st.rerun()

# Enhanced auth service with subscription enforcement and account creation
class EnhancedAuthService:
    def __init__(self):
        self.subscription_manager = SubscriptionManager()
        self.initialize_session_state()
        initialize_demo_data()
    
    def initialize_session_state(self):
        """Initialize session state"""
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'user_data' not in st.session_state:
            st.session_state.user_data = {}
    
    def show_login(self):
        """Login interface with subscription validation and account creation"""
        # Add custom CSS for professional styling
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
            min-height: 100vh;
            overflow-y: auto;
        }
        .main-header {
            text-align: center;
            color: white;
            padding: 3rem 0 2rem 0;
            margin-bottom: 2rem;
        }
        .main-header h1 {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }
        .main-header p {
            font-size: 1.3rem;
            font-weight: 300;
            opacity: 0.95;
        }
        .login-box {
            background: white;
            padding: 3rem;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            margin: 0 auto 3rem auto;
            max-width: 900px;
        }
        .section-header {
            color: #1e3a8a;
            font-weight: 600;
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
        }
        .feature-card {
            background: #f8fafc;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #3b82f6;
            height: 100%;
        }
        .feature-card h4 {
            color: #1e3a8a;
            margin-bottom: 1rem;
            font-size: 1.2rem;
        }
        .stButton > button {
            font-weight: 600;
            border-radius: 8px;
            padding: 0.75rem 2rem;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        </style>
        <div class="main-header">
            <h1>LegalDoc Pro</h1>
            <p>Enterprise Legal Management Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show signup form if triggered
        if st.session_state.get('show_signup', False):
            self.show_subscription_signup()
            return
    
        if st.session_state.get('show_trial_signup', False):
            self.show_trial_signup()
            return
        
        # Don't create the login-box div yet - just show the org code input first
        
        # Existing customer login
        st.markdown('<h2 class="section-header">Sign In</h2>', unsafe_allow_html=True)
        org_code = st.text_input("Organization Code", 
                                placeholder="Enter your firm's code (e.g., 'smithlaw')",
                                label_visibility="visible")
        
        if org_code:
            # Check if organization exists
            if org_code.lower() in ['demo', 'smithlaw', 'testfirm']:
                # Mock validation for demo
                status_msg = self.subscription_manager.get_subscription_status_message(org_code)
                if self.subscription_manager.is_subscription_active(org_code):
                    st.success(f"Organization found: {status_msg}")
                else:
                    st.error("Subscription expired or inactive")
                    if st.button("Renew Subscription"):
                        st.session_state['show_upgrade_modal'] = True
                        st.rerun()
                    return
            elif org_code in st.session_state.subscriptions:
                # Check subscription status
                if self.subscription_manager.is_subscription_active(org_code):
                    status_msg = self.subscription_manager.get_subscription_status_message(org_code)
                    st.success(f"Organization found: {status_msg}")
                else:
                    st.error("Subscription expired or inactive. Please renew.")
                    if st.button("Renew Subscription"):
                        st.session_state['show_upgrade_modal'] = True
                        st.session_state['upgrade_org_code'] = org_code
                        st.rerun()
                    return
            else:
                st.error("Organization not found. Please check your code or create a new account.")
                return
                
            # Login form for existing organizations
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
            
        # Account creation section
        st.divider()
    
        st.markdown('<h2 class="section-header">New to LegalDoc Pro?</h2>', unsafe_allow_html=True)
    
        # Two-column layout for new customers
        col_trial, col_paid = st.columns(2, gap="large")
    
        with col_trial:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
                        padding: 2rem; border-radius: 12px; color: white; height: 320px;">
                <h3 style="margin-top: 0; font-size: 1.5rem; margin-bottom: 1rem;">Free Trial</h3>
                <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">Experience the full platform risk-free</p>
                <ul style="list-style: none; padding-left: 0; margin-bottom: 2rem;">
                    <li style="margin-bottom: 0.5rem;">✓ 7 days full access</li>
                    <li style="margin-bottom: 0.5rem;">✓ No credit card required</li>
                    <li style="margin-bottom: 0.5rem;">✓ Up to 3 users</li>
                    <li style="margin-bottom: 0.5rem;">✓ All core features</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Start Free Trial", type="primary", use_container_width=True, key="trial_btn"):
                st.session_state['show_trial_signup'] = True
                st.rerun()
    
        with col_paid:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); 
                        padding: 2rem; border-radius: 12px; color: white; height: 320px;
                        border: 2px solid #3b82f6;">
                <h3 style="margin-top: 0; font-size: 1.5rem; margin-bottom: 1rem;">Enterprise Account</h3>
                <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">Full-featured legal management solution</p>
                <ul style="list-style: none; padding-left: 0; margin-bottom: 2rem;">
                    <li style="margin-bottom: 0.5rem;">✓ Immediate activation</li>
                    <li style="margin-bottom: 0.5rem;">✓ Flexible plans</li>
                    <li style="margin-bottom: 0.5rem;">✓ Priority support</li>
                    <li style="margin-bottom: 0.5rem;">✓ Custom integrations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("View Plans & Pricing", use_container_width=True, key="paid_btn"):
                st.session_state['show_signup'] = True
                st.rerun()
    
        # Features preview
        st.markdown('<div style="max-width: 1200px; margin: 3rem auto; padding: 0 2rem;">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: white; margin-bottom: 3rem; font-size: 2.5rem;">Why Leading Law Firms Choose LegalDoc Pro</h2>', unsafe_allow_html=True)
    
        col_feat1, col_feat2, col_feat3 = st.columns(3, gap="large")
    
        with col_feat1:
            st.markdown("""
            <div class="feature-card" style="min-height: 400px>
                <h4>AI-Powered Intelligence</h4>
                <p style="color: #475569; line-height: 1.6;">
                Advanced document analysis and contract review powered by machine learning. 
                Automatically identify risks, obligations, and key terms in seconds.
                </p>
                <ul style="color: #64748b; margin-top: 1rem;">
                    <li>Smart document extraction</li>
                    <li>Risk scoring & assessment</li>
                    <li>Automated legal insights</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
        with col_feat2:
            st.markdown("""
            <div class="feature-card" style="min-height: 400px>
                <h4>Complete Practice Management</h4>
                <p style="color: #475569; line-height: 1.6;">
                Streamline your entire practice with integrated matter management, 
                time tracking, billing, and client communication tools.
                </p>
                <ul style="color: #64748b; margin-top: 1rem;">
                    <li>Matter & case tracking</li>
                    <li>Time & billing automation</li>
                    <li>Client portal access</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
        with col_feat3:
            st.markdown("""
            <div class="feature-card" style="min-height: 400px>
                <h4>Enterprise-Grade Security</h4>
                <p style="color: #475569; line-height: 1.6;">
                Bank-level encryption and security protocols. Fully compliant with 
                attorney-client privilege and international data protection standards.
                </p>
                <ul style="color: #64748b; margin-top: 1rem;">
                    <li>256-bit encryption</li>
                    <li>GDPR & SOC 2 compliant</li>
                    <li>Regular security audits</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
        st.markdown('</div>', unsafe_allow_html=True)
    
    def show_trial_signup(self):
        """7-day trial signup process"""
        st.subheader("Start Your 7-Day Free Trial")
        
        if st.button("← Back to Login"):
            st.session_state['show_trial_signup'] = False
            st.rerun()
        
        st.info("No credit card required. Get full access to all features for 7 days.")
        
        with st.form("trial_signup_form"):
            st.markdown("#### Organization Information")
            col1, col2 = st.columns(2)
            
            with col1:
                firm_name = st.text_input("Law Firm/Company Name *", placeholder="Smith & Associates Law Firm")
                owner_name = st.text_input("Your Full Name *", placeholder="John Smith")
                owner_email = st.text_input("Email Address *", placeholder="john@smithlaw.com")
            
            with col2:
                org_code = st.text_input("Choose Organization Code *", 
                                        placeholder="e.g., 'smithlaw'",
                                        help="This will be your unique login code")
                phone = st.text_input("Phone Number", placeholder="+1 (555) 123-4567")
                firm_size = st.selectbox("Firm Size", [
                    "Solo practice (1 attorney)",
                    "Small firm (2-10 attorneys)", 
                    "Medium firm (11-50 attorneys)",
                    "Large firm (51+ attorneys)",
                    "Corporate legal department",
                    "Other"
                ])
            
            st.markdown("#### Your Trial Includes")
            col_trial1, col_trial2 = st.columns(2)
            
            with col_trial1:
                st.markdown("""
                - Full platform access for 7 days
                - Up to 3 users
                - 1GB storage
                - AI document analysis
                - Email support
                """)
            
            with col_trial2:
                st.markdown("""
                - Matter management
                - Time tracking & billing
                - Document organization
                - Client portal access
                - No setup fees
                """)
            
            # Legal checkboxes
            marketing_consent = st.checkbox("I'd like to receive product updates and legal industry insights")
            terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
            
            # Submit button
            if st.form_submit_button("Start My Free Trial", type="primary"):
                if self.validate_trial_signup(firm_name, owner_name, owner_email, org_code, terms_accepted):
                    success = self.create_trial_account(org_code, firm_name, owner_name, owner_email)
                    if success:
                        st.success("Trial account created successfully!")
                        st.info("You can now login with your organization code and any username/password.")
                        
                        # Show login details
                        st.markdown("### Your Login Details")
                        st.code(f"""
Organization Code: {org_code}
Username: Any username
Password: Any password (or use Demo Login)
                        """)
                        
                        if st.button("Continue to Login"):
                            st.session_state['show_trial_signup'] = False
                            st.rerun()
                else:
                    st.error("Please correct the errors above")
    
    def show_subscription_signup(self):
        """Paid subscription signup process"""
        st.subheader("Create Your LegalDoc Pro Account")
        
        if st.button("← Back to Login"):
            st.session_state['show_signup'] = False
            st.rerun()
        
        # Plan selection
        st.markdown("#### Choose Your Plan")
        
        col1, col2, col3 = st.columns(3)
        
        plans = [
            {
                "name": "Starter",
                "price": "$99/month",
                "users": "5 users",
                "storage": "10GB storage",
                "features": ["Basic AI features", "Standard support", "Mobile app"],
                "plan_id": "starter"
            },
            {
                "name": "Professional", 
                "price": "$299/month",
                "users": "25 users",
                "storage": "50GB storage", 
                "features": ["Advanced AI analytics", "Priority support", "Custom integrations", "White-label options"],
                "plan_id": "professional",
                "popular": True
            },
            {
                "name": "Enterprise",
                "price": "$599/month", 
                "users": "Unlimited users",
                "storage": "200GB storage",
                "features": ["Full AI suite", "Dedicated account manager", "Custom development", "On-premises deployment"],
                "plan_id": "enterprise"
            }
        ]
        
        selected_plan = None
        
        for i, plan in enumerate(plans):
            with [col1, col2, col3][i]:
                # Plan card styling
                if plan.get("popular"):
                    st.success(f"**{plan['name']}** (Most Popular)")
                else:
                    st.info(f"**{plan['name']}**")
                
                st.write(f"**{plan['price']}**")
                st.write(f"• {plan['users']}")
                st.write(f"• {plan['storage']}")
                
                for feature in plan['features']:
                    st.write(f"• {feature}")
                
                if st.button(f"Select {plan['name']}", key=f"select_{plan['plan_id']}"):
                    selected_plan = plan['plan_id']
        
        # If plan selected, show signup form
        if selected_plan or st.session_state.get('selected_plan'):
            if selected_plan:
                st.session_state['selected_plan'] = selected_plan
            
            selected_plan_info = next(p for p in plans if p['plan_id'] == st.session_state['selected_plan'])
            
            st.success(f"Selected: {selected_plan_info['name']} Plan - {selected_plan_info['price']}")
            
            # Organization details form
            with st.form("paid_signup_form"):
                st.markdown("#### Organization Information")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    firm_name = st.text_input("Law Firm/Company Name *")
                    owner_name = st.text_input("Your Full Name *") 
                    owner_email = st.text_input("Email Address *")
                    phone = st.text_input("Phone Number *")
                
                with col2:
                    org_code = st.text_input("Choose Organization Code *", 
                                            placeholder="e.g., 'smithlaw'")
                    address = st.text_input("Business Address")
                    city_state = st.text_input("City, State")
                    zip_code = st.text_input("ZIP Code")
                
                st.markdown("#### Payment Information")
                st.info("This is a demo - no real payment will be processed")
                
                col_pay1, col_pay2 = st.columns(2)
                
                with col_pay1:
                    card_number = st.text_input("Card Number", placeholder="**** **** **** 1234")
                    cardholder_name = st.text_input("Cardholder Name")
                
                with col_pay2:
                    col_exp, col_cvv = st.columns(2)
                    with col_exp:
                        card_expiry = st.text_input("MM/YY", placeholder="12/25")
                    with col_cvv:
                        card_cvv = st.text_input("CVV", placeholder="123")
                    
                    billing_zip = st.text_input("Billing ZIP")
                
                # Agreement checkboxes
                terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
                
                # Create account button
                if st.form_submit_button("Create Account & Start Subscription", type="primary"):
                    if self.validate_paid_signup(firm_name, owner_name, owner_email, org_code, terms_accepted):
                        success = self.create_paid_account(
                            org_code, firm_name, owner_name, owner_email, 
                            st.session_state['selected_plan']
                        )
                        if success:
                            st.success("Account created successfully!")
                            st.info("You can now login with your organization code.")
                            
                            if st.button("Continue to Login"):
                                st.session_state['show_signup'] = False
                                if 'selected_plan' in st.session_state:
                                    del st.session_state['selected_plan']
                                st.rerun()
    
    def validate_trial_signup(self, firm_name, owner_name, owner_email, org_code, terms_accepted):
        """Validate trial signup form"""
        valid = True
        
        if not firm_name:
            st.error("Firm name is required")
            valid = False
        
        if not owner_name:
            st.error("Your name is required")
            valid = False
        
        if not owner_email or "@" not in owner_email:
            st.error("Valid email address is required")
            valid = False
        
        if not org_code or len(org_code) < 3:
            st.error("Organization code must be at least 3 characters")
            valid = False
        
        if org_code and org_code.lower() in st.session_state.subscriptions:
            st.error("Organization code already exists. Please choose a different one.")
            valid = False
        
        if not terms_accepted:
            st.error("You must accept the Terms of Service")
            valid = False
        
        return valid
    
    def validate_paid_signup(self, firm_name, owner_name, owner_email, org_code, terms_accepted):
        """Validate paid signup form"""
        return self.validate_trial_signup(firm_name, owner_name, owner_email, org_code, terms_accepted)
    
    def create_trial_account(self, org_code, firm_name, owner_name, owner_email):
        """Create a trial account"""
        try:
            self.subscription_manager.create_trial_subscription(
                org_code, firm_name, owner_name, owner_email
            )
            return True
        except Exception as e:
            st.error(f"Error creating trial account: {str(e)}")
            return False
    
    def create_paid_account(self, org_code, firm_name, owner_name, owner_email, plan):
        """Create a paid account"""
        try:
            # Create subscription with selected plan
            subscription = {
                "organization_code": org_code,
                "organization_name": firm_name,
                "plan": plan,
                "status": SubscriptionStatus.ACTIVE.value,
                "created_date": datetime.now(),
                "trial_end_date": None,
                "current_users": 1,
                "storage_used_gb": 0.0,
                "monthly_cost": self.subscription_manager.get_plan_limits(plan)["monthly_cost"],
                "billing_email": owner_email,
                "owner_name": owner_name,
                "owner_email": owner_email,
                "payment_method": "****1234",  # Mock payment method
                "next_billing_date": datetime.now() + timedelta(days=30)
            }
            
            st.session_state.subscriptions[org_code] = subscription
            return True
        except Exception as e:
            st.error(f"Error creating paid account: {str(e)}")
            return False
    
    def authenticate_user(self, org_code, username, password, is_demo=False):
        """Authenticate user with subscription validation"""
        # Mock authentication - in real app, check database
        if is_demo or (username and password) or org_code.lower() in ['demo', 'smithlaw', 'testfirm']:
            user_data = {
                'user_id': str(uuid.uuid4()),
                'username': username or 'demo',
                'organization_code': org_code,
                'name': f'User from {org_code}',
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
            st.markdown(f"**{user_data.get('name', 'User')}**")
            if org_code:
                st.markdown(f"**{org_code}**")
                
                # Show subscription widget
                self.subscription_manager.show_subscription_widget(org_code)
            
            st.divider()
            
            # Navigation with feature gating
            self.show_navigation(org_code)
            
            st.divider()
            
            # Management options for subscription owners
            if user_data.get('is_subscription_owner'):
                if st.button("Billing & Subscription"):
                    st.session_state['show_billing'] = True
                    st.rerun()
            
            if st.button("Logout"):
                self.logout()
                st.rerun()
    
    def show_navigation(self, org_code):
        """Show navigation with subscription-based restrictions"""
        if not org_code:
            return
            
        subscription = self.subscription_manager.get_organization_subscription(org_code)
        if not subscription:
            return
        
        # Basic pages (available to all plans)
        basic_pages = [
            ("Dashboard", "Executive Dashboard"),
            ("Documents", "Document Management"),
            ("Matters", "Matter Management"),
            ("Billing", "Time & Billing"),
            ("Calendar", "Calendar & Tasks")
        ]
        
        for icon_text, page_name in basic_pages:
            if st.button(f"{icon_text}", key=f"nav_{page_name}"):
                st.session_state['current_page'] = page_name
                st.rerun()
        
        # AI features (gated by subscription)
        if self.subscription_manager.has_ai_feature(org_code, "basic_analysis"):
            if st.button("AI Insights", key="nav_AI Insights"):
                st.session_state['current_page'] = "AI Insights"
                st.rerun()
        else:
            st.button("AI Insights (Upgrade Required)", disabled=True)
        
        # Advanced features (Professional/Enterprise only)
        if self.subscription_manager.can_use_feature(org_code, "advanced_analytics"):
            advanced_pages = [
                ("Advanced Search", "Advanced Search"),
                ("Business Intel", "Business Intelligence")
            ]
            
            for page_text, page_name in advanced_pages:
                if st.button(page_text, key=f"nav_{page_name}"):
                    st.session_state['current_page'] = page_name
                    st.rerun()
        
        # Enterprise-only features
        if subscription.get("plan") == "enterprise":
            enterprise_pages = [
                ("Integrations", "Integrations"),
                ("Mobile App", "Mobile App"),
                ("Settings", "System Settings")
            ]
            
            for page_text, page_name in enterprise_pages:
                if st.button(page_text, key=f"nav_{page_name}"):
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
    
    def show_upgrade_modal(self, org_code):
        """Show subscription upgrade interface"""
        st.subheader("Upgrade Your Subscription")
        
        if st.button("← Back"):
            st.session_state['show_upgrade_modal'] = False
            st.rerun()
        
        current_subscription = self.subscription_manager.get_organization_subscription(org_code)
        current_plan = current_subscription.get("plan", "trial")
        
        # Plan comparison
        col1, col2, col3 = st.columns(3)
        
        plans = [
            (SubscriptionPlan.STARTER.value, "Starter", "$99/month", "5 users, 10GB storage"),
            (SubscriptionPlan.PROFESSIONAL.value, "Professional", "$299/month", "25 users, 50GB storage"), 
            (SubscriptionPlan.ENTERPRISE.value, "Enterprise", "$599/month", "Unlimited users, 200GB storage")
        ]
        
        for i, (plan_id, plan_name, price, description) in enumerate(plans):
            with [col1, col2, col3][i]:
                limits = self.subscription_manager.get_plan_limits(plan_id)
                
                # Plan card
                if plan_id == current_plan:
                    st.success(f"**{plan_name}** (Current)")
                else:
                    st.info(f"**{plan_name}**")
                
                st.write(f"**{price}**")
                st.write(description)
                
                # Feature list
                if plan_id == SubscriptionPlan.STARTER.value:
                    features = ["Basic AI analysis", "Standard support", "Mobile access"]
                elif plan_id == SubscriptionPlan.PROFESSIONAL.value:
                    features = ["Advanced AI analytics", "Batch processing", "Priority support", "Custom integrations"]
                else:
                    features = ["Full AI suite", "Dedicated support", "White-label options", "On-premises deployment"]
                
                for feature in features:
                    st.write(f"• {feature}")
                
                if plan_id != current_plan:
                    if st.button(f"Upgrade to {plan_name}", key=f"upgrade_{plan_id}"):
                        self.upgrade_subscription(org_code, plan_id)
                        st.success(f"Successfully upgraded to {plan_name} plan!")
                        st.balloons()
                        st.rerun()
    
    def upgrade_subscription(self, org_code, new_plan):
        """Upgrade organization subscription"""
        subscription = self.subscription_manager.get_organization_subscription(org_code)
        
        subscription["plan"] = new_plan
        subscription["status"] = SubscriptionStatus.ACTIVE.value
        subscription["next_billing_date"] = datetime.now() + timedelta(days=30)
        
        new_limits = self.subscription_manager.get_plan_limits(new_plan)
        subscription["monthly_cost"] = new_limits["monthly_cost"]
        
        st.session_state.subscriptions[org_code] = subscription
    
    def show_billing_interface(self, org_code):
        """Show billing and payment interface"""
        subscription = self.subscription_manager.get_organization_subscription(org_code)
        
        st.subheader("Billing & Subscription Management")
        
        if st.button("← Back"):
            st.session_state['show_billing'] = False
            st.rerun()
        
        # Current plan info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current Plan", subscription.get("plan", "Unknown").title())
        with col2:
            st.metric("Monthly Cost", f"${subscription.get('monthly_cost', 0)}")
        with col3:
            next_billing = subscription.get("next_billing_date")
            if next_billing:
                st.metric("Next Billing", next_billing.strftime("%Y-%m-%d"))
            else:
                st.metric("Next Billing", "N/A")
        
        # Subscription status
        status = subscription.get("status")
        if status == SubscriptionStatus.TRIAL.value:
            trial_end = subscription.get("trial_end_date")
            if trial_end:
                days_left = (trial_end - datetime.now()).days
                if days_left > 0:
                    st.warning(f"Trial ends in {days_left} days")
                    if st.button("Upgrade Before Trial Ends", type="primary"):
                        st.session_state['show_upgrade_modal'] = True
                        st.rerun()
                else:
                    st.error("Trial has expired")
        
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
        
        # Usage summary
        st.markdown("#### Current Usage")
        
        limits = self.subscription_manager.get_plan_limits(subscription.get("plan", "trial"))
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_users = subscription.get("current_users", 0)
            max_users = limits.get("max_users", 0)
            
            if max_users == 999999:
                st.write(f"**Users:** {current_users} (Unlimited)")
            else:
                user_percent = (current_users / max_users * 100) if max_users > 0 else 0
                st.write(f"**Users:** {current_users}/{max_users} ({user_percent:.0f}%)")
                st.progress(min(user_percent / 100, 1.0))
        
        with col2:
            storage_used = subscription.get("storage_used_gb", 0)
            max_storage = limits.get("storage_gb", 0)
            
            storage_percent = (storage_used / max_storage * 100) if max_storage > 0 else 0
            st.write(f"**Storage:** {storage_used:.1f}GB/{max_storage}GB ({storage_percent:.0f}%)")
            st.progress(min(storage_percent / 100, 1.0))
        
        # Billing history
        st.markdown("#### Billing History")
        
        # Mock billing data
        billing_history = [
            {"date": "2024-10-01", "amount": f"${subscription.get('monthly_cost', 0)}", "status": "Paid", "invoice": "INV-001"},
            {"date": "2024-09-01", "amount": f"${subscription.get('monthly_cost', 0)}", "status": "Paid", "invoice": "INV-002"},
            {"date": "2024-08-01", "amount": f"${subscription.get('monthly_cost', 0)}", "status": "Paid", "invoice": "INV-003"}
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
    
    def logout(self):
        """Logout user"""
        keys_to_clear = [
            'logged_in', 'user_data', 'current_page', 'show_upgrade_modal',
            'show_billing', 'show_signup', 'show_trial_signup', 'selected_plan'
        ]
        
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return st.session_state.get('logged_in', False)

# Usage functions for easy integration
def get_auth_service():
    """Get the enhanced auth service instance"""
    return EnhancedAuthService()

# Demo data initialization for testing
def initialize_demo_data():
    """Initialize demo subscription data"""
    # Initialize subscriptions if not exists
    if 'subscriptions' not in st.session_state:
        st.session_state.subscriptions = {}
    
    if 'demo_initialized' not in st.session_state:
        demo_subscriptions = {
            'demo': {
                "organization_code": "demo",
                "organization_name": "Demo Law Firm",
                "plan": SubscriptionPlan.PROFESSIONAL.value,
                "status": SubscriptionStatus.ACTIVE.value,
                "created_date": datetime.now() - timedelta(days=30),
                "current_users": 8,
                "storage_used_gb": 12.5,
                "monthly_cost": 299,
                "billing_email": "demo@demolawfirm.com",
                "owner_name": "Demo Owner",
                "owner_email": "demo@demolawfirm.com",
                "payment_method": "1234",
                "next_billing_date": datetime.now() + timedelta(days=15)
            },
            'smithlaw': {
                "organization_code": "smithlaw", 
                "organization_name": "Smith & Associates",
                "plan": SubscriptionPlan.ENTERPRISE.value,
                "status": SubscriptionStatus.ACTIVE.value,
                "created_date": datetime.now() - timedelta(days=180),
                "current_users": 25,
                "storage_used_gb": 67.3,
                "monthly_cost": 599,
                "billing_email": "billing@smithlaw.com",
                "owner_name": "John Smith",
                "owner_email": "john@smithlaw.com",
                "payment_method": "5678",
                "next_billing_date": datetime.now() + timedelta(days=22)
            },
            'testfirm': {
                "organization_code": "testfirm",
                "organization_name": "Test Legal Firm",
                "plan": SubscriptionPlan.TRIAL.value,
                "status": SubscriptionStatus.TRIAL.value,
                "created_date": datetime.now() - timedelta(days=3),
                "trial_end_date": datetime.now() + timedelta(days=4),
                "current_users": 2,
                "storage_used_gb": 0.3,
                "monthly_cost": 0,
                "billing_email": "test@testfirm.com",
                "owner_name": "Test User",
                "owner_email": "test@testfirm.com"
            }
        }
        
        # Add demo data to session state
        for org_code, subscription in demo_subscriptions.items():
            st.session_state.subscriptions[org_code] = subscription
        
        st.session_state.demo_initialized = True


# Main execution for testing
if __name__ == "__main__":
    st.set_page_config(
        page_title="LegalDoc Pro - Subscription Demo",
        page_icon="⚖️",
        layout="wide"
    )
    
    auth_service = EnhancedAuthService()
    
    if not auth_service.is_logged_in():
        auth_service.show_login()
    else:
        # Handle modals
        user_data = st.session_state.get('user_data', {})
        org_code = user_data.get('organization_code')
        
        if st.session_state.get('show_upgrade_modal'):
            auth_service.show_upgrade_modal(org_code)
        elif st.session_state.get('show_billing'):
            auth_service.show_billing_interface(org_code)
        else:
            # Show main interface
            auth_service.render_sidebar()
            
            st.title("LegalDoc Pro Dashboard")
            st.write("Welcome to your legal management platform!")
            
            # Show subscription status
            subscription = auth_service.subscription_manager.get_organization_subscription(org_code)
            if subscription:
                status_msg = auth_service.subscription_manager.get_subscription_status_message(org_code)
                st.success(f"Subscription Status: {status_msg}")
                
                # Show usage
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Users: {subscription.get('current_users', 0)}")
                with col2:
                    st.write(f"Storage: {subscription.get('storage_used_gb', 0):.1f}GB")
