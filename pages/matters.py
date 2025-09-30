# pages/matters.py - Enhanced Matter Management Interface
import streamlit as st
import uuid
import time
from datetime import datetime, timedelta
import pandas as pd
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum

class MatterType(Enum):
    LITIGATION = "litigation"
    CORPORATE = "corporate"
    REAL_ESTATE = "real_estate"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    EMPLOYMENT = "employment"
    TAX = "tax"
    FAMILY = "family"
    CRIMINAL = "criminal"
    IMMIGRATION = "immigration"
    BANKRUPTCY = "bankruptcy"
    CONTRACT = "contract"
    MERGERS_ACQUISITIONS = "mergers_acquisitions"

class MatterStatus(Enum):
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    CLOSED = "closed"
    ARCHIVED = "archived"
    CANCELLED = "cancelled"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Task:
    id: str = ""
    matter_id: str = ""
    title: str = ""
    description: str = ""
    assigned_to: str = ""
    due_date: datetime = field(default_factory=datetime.now)
    status: str = "pending"
    priority: str = "medium"
    created_date: datetime = field(default_factory=datetime.now)
    completed_date: Optional[datetime] = None
    estimated_hours: float = 0.0
    actual_hours: float = 0.0

@dataclass
class TimeEntry:
    id: str = ""
    matter_id: str = ""
    attorney_email: str = ""
    date: datetime = field(default_factory=datetime.now)
    hours: float = 0.0
    description: str = ""
    billable_rate: float = 250.0
    task_id: Optional[str] = None

@dataclass
class MatterExpense:
    id: str = ""
    matter_id: str = ""
    date: datetime = field(default_factory=datetime.now)
    amount: float = 0.0
    description: str = ""
    category: str = "general"
    is_billable: bool = True
    receipt_attached: bool = False

@dataclass
class Matter:
    id: str = ""
    name: str = ""
    client_id: str = ""
    client_name: str = ""
    matter_type: str = ""
    status: str = ""
    created_date: datetime = field(default_factory=datetime.now)
    assigned_attorneys: List[str] = field(default_factory=list)
    description: str = ""
    budget: float = 0.0
    estimated_hours: float = 0.0
    actual_hours: float = 0.0
    hourly_rate: float = 250.0
    priority: str = "medium"
    deadline: Optional[datetime] = None
    closed_date: Optional[datetime] = None
    billing_contact: str = ""
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)

# Import auth service
try:
    from services.auth import AuthService
except ImportError:
    class AuthService:
        def has_permission(self, perm):
            return True


def create_new_user():
    from services.subscription_manager import EnhancedAuthService
    auth_service = EnhancedAuthService()
    
    if not auth_service.check_user_limit_before_invite():
        st.error("User limit reached for your current plan.")
        current_plan = st.session_state.user_data.get('organization_code')
        subscription = auth_service.subscription_manager.get_organization_subscription(current_plan)
        limits = auth_service.subscription_manager.get_plan_limits(subscription['plan'])
        
        st.info(f"Your {subscription['plan'].title()} plan allows {limits['max_users']} users.")
        
        if st.button("Upgrade Plan"):
            st.session_state['show_upgrade_modal'] = True
            st.rerun()
        return


def initialize_matter_session_state():
    """Initialize matter-related session state"""
    if 'matters' not in st.session_state:
        st.session_state.matters = []
    
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
    
    if 'time_entries' not in st.session_state:
        st.session_state.time_entries = []
    
    if 'matter_expenses' not in st.session_state:
        st.session_state.matter_expenses = []
    
    # Sample data for demo
    if not st.session_state.matters:
        sample_matters = [
            Matter(
                id=str(uuid.uuid4()),
                name="Software License Agreement",
                client_id=str(uuid.uuid4()),
                client_name="TechCorp Inc",
                matter_type="contract",
                status="active",
                created_date=datetime.now() - timedelta(days=30),
                assigned_attorneys=["john.doe@lawfirm.com", "jane.smith@lawfirm.com"],
                description="Negotiation and drafting of enterprise software licensing agreement",
                budget=50000.0,
                estimated_hours=100.0,
                actual_hours=45.5,
                priority="high",
                deadline=datetime.now() + timedelta(days=15),
                billing_contact="finance@techcorp.com",
                tags=["contract", "technology", "urgent"]
            ),
            Matter(
                id=str(uuid.uuid4()),
                name="Employment Dispute Resolution",
                client_id=str(uuid.uuid4()),
                client_name="StartupXYZ",
                matter_type="employment",
                status="active",
                created_date=datetime.now() - timedelta(days=45),
                assigned_attorneys=["alice.johnson@lawfirm.com"],
                description="Wrongful termination claim defense",
                budget=30000.0,
                estimated_hours=80.0,
                actual_hours=32.0,
                priority="medium",
                billing_contact="hr@startupxyz.com",
                tags=["employment", "litigation"]
            ),
            Matter(
                id=str(uuid.uuid4()),
                name="Corporate Acquisition",
                client_id=str(uuid.uuid4()),
                client_name="GlobalCorp",
                matter_type="mergers_acquisitions",
                status="on_hold",
                created_date=datetime.now() - timedelta(days=60),
                assigned_attorneys=["partner@lawfirm.com", "senior@lawfirm.com"],
                description="Asset purchase agreement for subsidiary acquisition",
                budget=150000.0,
                estimated_hours=300.0,
                actual_hours=125.0,
                priority="critical",
                billing_contact="legal@globalcorp.com",
                tags=["M&A", "corporate", "high-value"]
            )
        ]
        st.session_state.matters.extend(sample_matters)

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
    """Main matter management interface"""
    initialize_matter_session_state()
    auth_service = AuthService()
    
    st.title("⚖️ Matter Management")
    st.markdown("---")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Matters", "📊 Analytics", "✅ Tasks", "⏰ Time Tracking", "💰 Expenses"])
    
    with tab1:
        _show_matter_dashboard(auth_service)
    
    with tab2:
        _show_matter_analytics()
    
    with tab3:
        _show_task_management(auth_service)
    
    with tab4:
        _show_time_tracking(auth_service)
    
    with tab5:
        _show_expense_tracking(auth_service)

def _show_matter_dashboard(auth_service):
    """Enhanced matter dashboard"""
    # Statistics
    _show_matter_statistics()
    
    st.divider()
    
    # Create new matter
    if auth_service.has_permission('write'):
        _show_create_matter_form(auth_service)
        st.divider()
    
    # Matter filters and search
    _show_matter_filters()
    
    # Matter list
    _show_matter_list(auth_service)

def _show_matter_statistics():
    """Display comprehensive matter statistics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_matters = len([m for m in st.session_state.matters if m.status == 'active'])
        st.metric("🟢 Active Matters", active_matters)
    
    with col2:
        total_budget = sum(m.budget for m in st.session_state.matters if m.status == 'active')
        st.metric("💰 Active Budget", f"${total_budget:,.0f}")
    
    with col3:
        total_hours = sum(m.actual_hours for m in st.session_state.matters if m.status == 'active')
        st.metric("⏰ Hours Logged", f"{total_hours:.1f}")
    
    with col4:
        avg_utilization = 0
        if st.session_state.matters:
            total_est = sum(m.estimated_hours for m in st.session_state.matters if m.estimated_hours > 0)
            total_actual = sum(m.actual_hours for m in st.session_state.matters if m.estimated_hours > 0)
            avg_utilization = (total_actual / total_est * 100) if total_est > 0 else 0
        st.metric("📈 Utilization", f"{avg_utilization:.1f}%")
    
    # Additional statistics row
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        overdue_matters = len([m for m in st.session_state.matters 
                             if m.deadline and m.deadline < datetime.now() and m.status == 'active'])
        st.metric("⚠️ Overdue", overdue_matters, delta=None, delta_color="inverse")
    
    with col6:
        high_priority = len([m for m in st.session_state.matters 
                           if m.priority in ['high', 'critical'] and m.status == 'active'])
        st.metric("🔴 High Priority", high_priority)
    
    with col7:
        on_hold = len([m for m in st.session_state.matters if m.status == 'on_hold'])
        st.metric("⏸️ On Hold", on_hold)
    
    with col8:
        closed_this_month = len([m for m in st.session_state.matters 
                               if m.closed_date and (datetime.now() - m.closed_date).days <= 30])
        st.metric("✅ Closed (30d)", closed_this_month)

def _show_create_matter_form(auth_service):
    """Enhanced matter creation form"""
    st.subheader("➕ Create New Matter")
    
    with st.form("new_matter_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            matter_name = st.text_input("Matter Name *", placeholder="e.g., Software License Agreement")
            client_name = st.text_input("Client Name *", placeholder="e.g., TechCorp Inc")
            matter_type = st.selectbox("Matter Type *", 
                                     [mt.value.replace('_', ' ').title() for mt in MatterType])
            priority = st.selectbox("Priority", [p.value.title() for p in Priority], index=1)
        
        with col2:
            description = st.text_area("Description", height=100)
            estimated_budget = st.number_input("Estimated Budget ($)", min_value=0.0, step=1000.0)
            estimated_hours = st.number_input("Estimated Hours", min_value=0.0, step=10.0, value=40.0)
            hourly_rate = st.number_input("Hourly Rate ($)", min_value=0.0, step=25.0, value=250.0)
        
        # Additional fields
        col3, col4 = st.columns(2)
        
        with col3:
            deadline = st.date_input("Deadline (optional)", value=None)
            billing_contact = st.text_input("Billing Contact Email", placeholder="billing@client.com")
        
        with col4:
            assigned_attorneys = st.text_input("Assigned Attorneys (comma-separated)", 
                                             placeholder="john@firm.com, jane@firm.com")
            tags = st.text_input("Tags (comma-separated)", placeholder="contract, urgent, technology")
        
        if st.form_submit_button("🚀 Create Matter", type="primary"):
            if matter_name and client_name:
                new_matter = Matter(
                    id=str(uuid.uuid4()),
                    name=matter_name,
                    client_id=str(uuid.uuid4()),
                    client_name=client_name,
                    matter_type=matter_type.lower().replace(' ', '_'),
                    status='active',
                    created_date=datetime.now(),
                    assigned_attorneys=[email.strip() for email in assigned_attorneys.split(',') if email.strip()],
                    description=description,
                    budget=estimated_budget,
                    estimated_hours=estimated_hours,
                    actual_hours=0.0,
                    hourly_rate=hourly_rate,
                    priority=priority.lower(),
                    deadline=datetime.combine(deadline, datetime.min.time()) if deadline else None,
                    billing_contact=billing_contact,
                    tags=[tag.strip() for tag in tags.split(',') if tag.strip()]
                )
                
                st.session_state.matters.append(new_matter)
                st.success(f"✅ Matter '{matter_name}' created successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields.")

def _show_matter_filters():
    """Matter filtering interface"""
    st.subheader("🔍 Filter & Search")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_filter = st.selectbox("Status", 
                                   ["All"] + [s.value.title() for s in MatterStatus])
    
    with col2:
        type_filter = st.selectbox("Type", 
                                 ["All"] + [mt.value.replace('_', ' ').title() for mt in MatterType])
    
    with col3:
        priority_filter = st.selectbox("Priority", 
                                     ["All"] + [p.value.title() for p in Priority])
    
    with col4:
        attorney_filter = st.selectbox("Assigned Attorney", 
                                     ["All"] + list(set([attorney for matter in st.session_state.matters 
                                                        for attorney in matter.assigned_attorneys])))
    
    # Search functionality
    search_term = st.text_input("🔍 Search matters", placeholder="Search by name, client, or description...")
    
    # Apply filters to session state for use in matter list
    st.session_state['matter_filters'] = {
        'status': status_filter,
        'type': type_filter,
        'priority': priority_filter,
        'attorney': attorney_filter,
        'search': search_term
    }

def _show_matter_list(auth_service):
    """Enhanced matter list with filtering"""
    st.subheader("📋 Matter List")
    
    # Apply filters
    filtered_matters = _apply_matter_filters(st.session_state.matters)
    
    if not filtered_matters:
        st.info("No matters found matching your filters.")
        return
    
    st.markdown(f"**Showing {len(filtered_matters)} matters**")
    
    # Sort options
    sort_by = st.selectbox("Sort by:", 
                          ["Created Date", "Deadline", "Priority", "Name", "Budget", "Hours"])
    
    filtered_matters = _sort_matters(filtered_matters, sort_by)
    
    # Display matters
    for matter in filtered_matters:
        _show_matter_card(matter, auth_service)

def _apply_matter_filters(matters):
    """Apply filters to matter list"""
    if 'matter_filters' not in st.session_state:
        return matters
    
    filters = st.session_state['matter_filters']
    filtered = matters.copy()
    
    # Status filter
    if filters['status'] != "All":
        status_value = filters['status'].lower()
        filtered = [m for m in filtered if m.status == status_value]
    
    # Type filter
    if filters['type'] != "All":
        type_value = filters['type'].lower().replace(' ', '_')
        filtered = [m for m in filtered if m.matter_type == type_value]
    
    # Priority filter
    if filters['priority'] != "All":
        priority_value = filters['priority'].lower()
        filtered = [m for m in filtered if m.priority == priority_value]
    
    # Attorney filter
    if filters['attorney'] != "All":
        filtered = [m for m in filtered if filters['attorney'] in m.assigned_attorneys]
    
    # Search filter
    if filters['search']:
        search_term = filters['search'].lower()
        filtered = [m for m in filtered if 
                   search_term in m.name.lower() or 
                   search_term in m.client_name.lower() or 
                   search_term in m.description.lower()]
    
    return filtered

def _sort_matters(matters, sort_by):
    """Sort matters based on selected criteria"""
    if sort_by == "Created Date":
        return sorted(matters, key=lambda x: x.created_date, reverse=True)
    elif sort_by == "Deadline":
        return sorted(matters, key=lambda x: x.deadline or datetime.max)
    elif sort_by == "Priority":
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        return sorted(matters, key=lambda x: priority_order.get(x.priority, 4))
    elif sort_by == "Name":
        return sorted(matters, key=lambda x: x.name.lower())
    elif sort_by == "Budget":
        return sorted(matters, key=lambda x: x.budget, reverse=True)
    elif sort_by == "Hours":
        return sorted(matters, key=lambda x: x.actual_hours, reverse=True)
    else:
        return matters

def _show_matter_card(matter, auth_service):
    """Enhanced matter card display"""
    # Priority and status indicators
    priority_colors = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}
    status_colors = {"active": "🟢", "on_hold": "🟡", "closed": "✅", "archived": "📦", "cancelled": "❌"}
    
    matter_docs = [doc for doc in st.session_state.get('documents', []) 
                   if hasattr(doc, 'matter_id') and doc.matter_id == matter.id]
    
    # Check if overdue
    is_overdue = matter.deadline and matter.deadline < datetime.now() and matter.status == 'active'
    overdue_indicator = "⚠️ OVERDUE" if is_overdue else ""
    
    with st.expander(f"{priority_colors.get(matter.priority, '⚪')} {matter.name} - {matter.client_name} {overdue_indicator}"):
        # Main information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**👤 Client:** {matter.client_name}")
            st.markdown(f"**📋 Type:** {matter.matter_type.replace('_', ' ').title()}")
            st.markdown(f"**🎯 Status:** {status_colors.get(matter.status, '❓')} {matter.status.title()}")
            st.markdown(f"**🔥 Priority:** {priority_colors.get(matter.priority, '⚪')} {matter.priority.title()}")
        
        with col2:
            st.markdown(f"**📄 Documents:** {len(matter_docs)}")
            st.markdown(f"**💰 Budget:** ${matter.budget:,.2f}")
            st.markdown(f"**⏰ Est. Hours:** {matter.estimated_hours}")
            st.markdown(f"**📊 Actual Hours:** {matter.actual_hours}")
        
        with col3:
            utilization = (matter.actual_hours / matter.estimated_hours * 100) if matter.estimated_hours > 0 else 0
            st.markdown(f"**📈 Utilization:** {utilization:.1f}%")
            st.markdown(f"**📅 Created:** {matter.created_date.strftime('%Y-%m-%d')}")
            if matter.deadline:
                deadline_str = matter.deadline.strftime('%Y-%m-%d')
                if is_overdue:
                    st.markdown(f"**⚠️ Deadline:** {deadline_str}")
                else:
                    st.markdown(f"**🎯 Deadline:** {deadline_str}")
            
            if matter.billing_contact:
                st.markdown(f"**💳 Billing:** {matter.billing_contact}")
        
        # Description and tags
        if matter.description:
            st.markdown(f"**📝 Description:** {matter.description}")
        
        if matter.tags:
            st.markdown(f"**🏷️ Tags:** {', '.join(matter.tags)}")
        
        if matter.assigned_attorneys:
            st.markdown(f"**👥 Attorneys:** {', '.join(matter.assigned_attorneys)}")
        
        # Recent documents
        if matter_docs:
            st.markdown("**📂 Recent Documents:**")
            for doc in matter_docs[-3:]:
                doc_name = getattr(doc, 'name', 'Unknown Document')
                doc_type = getattr(doc, 'document_type', getattr(doc, 'type', 'Unknown'))
                doc_status = getattr(doc, 'status', 'unknown')
                
                status_emoji = {"draft": "✏️", "under_review": "🔍", "final": "✅"}
                st.markdown(f"• {status_emoji.get(doc_status, '📄')} {doc_name} ({doc_type})")
        
        # Progress bar for budget utilization
        if matter.budget > 0:
            billed_amount = matter.actual_hours * matter.hourly_rate
            budget_utilization = min(billed_amount / matter.budget, 1.0)
            st.progress(budget_utilization, text=f"Budget Used: ${billed_amount:,.2f} / ${matter.budget:,.2f}")
        
        # Action buttons
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("📊 Analytics", key=f"analytics_{matter.id}"):
                _show_matter_analytics_modal(matter)
        
        with col2:
            if auth_service.has_permission('write'):
                if st.button("✏️ Edit", key=f"edit_matter_{matter.id}"):
                    _show_matter_editor(matter)
        
        with col3:
            if st.button("✅ Tasks", key=f"tasks_{matter.id}"):
                _show_matter_tasks(matter.id)
        
        with col4:
            if st.button("⏰ Time", key=f"time_{matter.id}"):
                _show_matter_time_entries(matter.id)
        
        with col5:
            if st.button("🔄 Update Status", key=f"status_{matter.id}"):
                _show_status_update_modal(matter)

def _show_matter_analytics():
    """Matter analytics dashboard"""
    st.subheader("📊 Matter Analytics")
    
    if not st.session_state.matters:
        st.info("No matters available for analytics.")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_matters = len(st.session_state.matters)
        st.metric("Total Matters", total_matters)
    
    with col2:
        total_revenue = sum(m.actual_hours * m.hourly_rate for m in st.session_state.matters)
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
    
    with col3:
        avg_matter_value = total_revenue / total_matters if total_matters > 0 else 0
        st.metric("Avg Matter Value", f"${avg_matter_value:,.0f}")
    
    with col4:
        total_hours = sum(m.actual_hours for m in st.session_state.matters)
        st.metric("Total Hours", f"{total_hours:.1f}")
    
    # Charts and analysis
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribution", "📈 Performance", "⏰ Time Analysis", "💰 Financial"])
    
    with tab1:
        _show_matter_distribution_charts()
    
    with tab2:
        _show_matter_performance_analysis()
    
    with tab3:
        _show_time_analysis()
    
    with tab4:
        _show_financial_analysis()

def _show_matter_distribution_charts():
    """Show matter distribution charts"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Matter Types Distribution**")
        type_counts = {}
        for matter in st.session_state.matters:
            matter_type = matter.matter_type.replace('_', ' ').title()
            type_counts[matter_type] = type_counts.get(matter_type, 0) + 1
        
        for matter_type, count in sorted(type_counts.items()):
            percentage = (count / len(st.session_state.matters)) * 100
            st.write(f"{matter_type}: {count} ({percentage:.1f}%)")
    
    with col2:
        st.markdown("**Status Distribution**")
        status_counts = {}
        for matter in st.session_state.matters:
            status = matter.status.title()
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in sorted(status_counts.items()):
            percentage = (count / len(st.session_state.matters)) * 100
            st.write(f"{status}: {count} ({percentage:.1f}%)")

def _show_matter_performance_analysis():
    """Show matter performance analysis"""
    st.markdown("**Top Performing Matters (by Revenue)**")
    
    # Calculate revenue for each matter
    matter_revenue = []
    for matter in st.session_state.matters:
        revenue = matter.actual_hours * matter.hourly_rate
        matter_revenue.append((matter, revenue))
    
    # Sort by revenue
    matter_revenue.sort(key=lambda x: x[1], reverse=True)
    
    # Display top 10
    for i, (matter, revenue) in enumerate(matter_revenue[:10], 1):
        utilization = (matter.actual_hours / matter.estimated_hours * 100) if matter.estimated_hours > 0 else 0
        st.write(f"{i}. **{matter.name}** - ${revenue:,.0f} ({utilization:.1f}% utilization)")

def _show_time_analysis():
    """Show time tracking analysis"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Hours by Matter Type**")
        type_hours = {}
        for matter in st.session_state.matters:
            matter_type = matter.matter_type.replace('_', ' ').title()
            type_hours[matter_type] = type_hours.get(matter_type, 0) + matter.actual_hours
        
        for matter_type, hours in sorted(type_hours.items(), key=lambda x: x[1], reverse=True):
            st.write(f"{matter_type}: {hours:.1f} hours")
    
    with col2:
        st.markdown("**Utilization Analysis**")
        over_budget = 0
        under_budget = 0
        on_target = 0
        
        for matter in st.session_state.matters:
            if matter.estimated_hours > 0:
                utilization = matter.actual_hours / matter.estimated_hours
                if utilization > 1.1:
                    over_budget += 1
                elif utilization < 0.9:
                    under_budget += 1
                else:
                    on_target += 1
        
        st.write(f"Over Budget (>110%): {over_budget}")
        st.write(f"On Target (90-110%): {on_target}")
        st.write(f"Under Budget (<90%): {under_budget}")

def _show_financial_analysis():
    """Show financial analysis"""
    st.markdown("**Financial Summary**")
    
    total_budget = sum(m.budget for m in st.session_state.matters)
    total_billed = sum(m.actual_hours * m.hourly_rate for m in st.session_state.matters)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Budgeted", f"${total_budget:,.0f}")
    
    with col2:
        st.metric("Total Billed", f"${total_billed:,.0f}")
    
    with col3:
        realization = (total_billed / total_budget * 100) if total_budget > 0 else 0
        st.metric("Realization Rate", f"{realization:.1f}%")

def _show_task_management(auth_service):
    """Task management interface"""
    st.subheader("✅ Task Management")
    
    # Create new task
    if auth_service.has_permission('write'):
        with st.form("new_task_form"):
            st.markdown("**➕ Create New Task**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                task_title = st.text_input("Task Title *")
                matter_options = [(m.id, f"{m.name} - {m.client_name}") for m in st.session_state.matters]
                if matter_options:
                    selected_matter = st.selectbox("Select Matter *", 
                                                 options=matter_options, 
                                                 format_func=lambda x: x[1])
                else:
                    st.warning("No matters available. Create a matter first.")
                    selected_matter = None
                task_priority = st.selectbox("Priority", [p.value.title() for p in Priority], index=1)
            
            with col2:
                task_description = st.text_area("Description")
                due_date = st.date_input("Due Date")
                assigned_to = st.text_input("Assigned To (email)", placeholder="attorney@firm.com")
                estimated_hours = st.number_input("Estimated Hours", min_value=0.0, step=0.5, value=1.0)
            
            if st.form_submit_button("Create Task"):
                if task_title and selected_matter and assigned_to:
                    new_task = Task(
                        id=str(uuid.uuid4()),
                        matter_id=selected_matter[0],
                        title=task_title,
                        description=task_description,
                        assigned_to=assigned_to,
                        due_date=datetime.combine(due_date, datetime.min.time()),
                        priority=task_priority.lower(),
                        estimated_hours=estimated_hours
                    )
                    
                    st.session_state.tasks.append(new_task)
                    st.success(f"Task '{task_title}' created successfully!")
                    time.sleep(1)
                    st.rerun()
    
    st.divider()
    
    # Task list
    _show_task_list(auth_service)

def _show_task_list(auth_service):
    """Display task list"""
    if not st.session_state.tasks:
        st.info("No tasks found. Create your first task above!")
        return
    
    # Task filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox("Filter by Status", 
                                   ["All", "Pending", "In Progress", "Completed", "Cancelled"])
    
    with col2:
        priority_filter = st.selectbox("Filter by Priority", 
                                     ["All"] + [p.value.title() for p in Priority])
    
    with col3:
        matter_filter = st.selectbox("Filter by Matter", 
                                   ["All"] + [m.name for m in st.session_state.matters])
    
    # Apply filters
    filtered_tasks = st.session_state.tasks.copy()
    
    if status_filter != "All":
        status_value = status_filter.lower().replace(' ', '_')
        filtered_tasks = [t for t in filtered_tasks if t.status == status_value]
    
    if priority_filter != "All":
        priority_value = priority_filter.lower()
        filtered_tasks = [t for t in filtered_tasks if t.priority == priority_value]
    
    if matter_filter != "All":
        matter_id = next((m.id for m in st.session_state.matters if m.name == matter_filter), None)
        if matter_id:
            filtered_tasks = [t for t in filtered_tasks if t.matter_id == matter_id]
    
    # Sort tasks by due date
    filtered_tasks.sort(key=lambda x: x.due_date)
    
    st.markdown(f"**Showing {len(filtered_tasks)} tasks**")
    
    # Display tasks
    for task in filtered_tasks:
        _show_task_card(task, auth_service)

def _show_task_card(task, auth_service):
    """Display individual task card"""
    # Get matter name
    matter = next((m for m in st.session_state.matters if m.id == task.matter_id), None)
    matter_name = matter.name if matter else "Unknown Matter"
    
    # Status and priority indicators
    status_colors = {"pending": "🟡", "in_progress": "🔵", "completed": "✅", "cancelled": "❌"}
    priority_colors = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}
    
    # Check if overdue
    is_overdue = task.due_date < datetime.now() and task.status not in ['completed', 'cancelled']
    overdue_indicator = "⚠️ OVERDUE" if is_overdue else ""
    
    with st.expander(f"{priority_colors.get(task.priority, '⚪')} {task.title} - {matter_name} {overdue_indicator}"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**📋 Matter:** {matter_name}")
            st.markdown(f"**👤 Assigned To:** {task.assigned_to}")
            st.markdown(f"**🎯 Status:** {status_colors.get(task.status, '❓')} {task.status.replace('_', ' ').title()}")
        
        with col2:
            st.markdown(f"**🔥 Priority:** {priority_colors.get(task.priority, '⚪')} {task.priority.title()}")
            st.markdown(f"**📅 Due Date:** {task.due_date.strftime('%Y-%m-%d')}")
            st.markdown(f"**⏰ Est. Hours:** {task.estimated_hours}")
        
        with col3:
            st.markdown(f"**📊 Actual Hours:** {task.actual_hours}")
            st.markdown(f"**📝 Created:** {task.created_date.strftime('%Y-%m-%d')}")
            if task.completed_date:
                st.markdown(f"**✅ Completed:** {task.completed_date.strftime('%Y-%m-%d')}")
        
        if task.description:
            st.markdown(f"**📝 Description:** {task.description}")
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if task.status != 'completed' and st.button("✅ Mark Complete", key=f"complete_task_{task.id}"):
                task.status = 'completed'
                task.completed_date = datetime.now()
                st.success("Task marked as completed!")
                st.rerun()
        
        with col2:
            if task.status == 'pending' and st.button("🔄 Start Task", key=f"start_task_{task.id}"):
                task.status = 'in_progress'
                st.success("Task started!")
                st.rerun()
        
        with col3:
            if st.button("⏰ Log Time", key=f"log_time_task_{task.id}"):
                _show_time_entry_modal(task)
        
        with col4:
            if auth_service.has_permission('write') and st.button("✏️ Edit", key=f"edit_task_{task.id}"):
                _show_task_editor(task)

def _show_time_tracking(auth_service):
    """Time tracking interface"""
    st.subheader("⏰ Time Tracking")
    
    # Log new time entry
    if auth_service.has_permission('write'):
        with st.form("new_time_entry_form"):
            st.markdown("**➕ Log Time Entry**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                matter_options = [(m.id, f"{m.name} - {m.client_name}") for m in st.session_state.matters]
                if matter_options:
                    selected_matter = st.selectbox("Select Matter *", 
                                                 options=matter_options, 
                                                 format_func=lambda x: x[1])
                else:
                    st.warning("No matters available. Create a matter first.")
                    selected_matter = None
                attorney_email = st.text_input("Attorney Email *", value="current@firm.com")
                date = st.date_input("Date", value=datetime.now().date())
            
            with col2:
                hours = st.number_input("Hours *", min_value=0.0, step=0.25, value=1.0)
                description = st.text_area("Description *", placeholder="Detail the work performed...")
                billable_rate = st.number_input("Billable Rate ($)", min_value=0.0, step=25.0, value=250.0)
            
            if st.form_submit_button("Log Time"):
                if selected_matter and attorney_email and hours > 0 and description:
                    new_entry = TimeEntry(
                        id=str(uuid.uuid4()),
                        matter_id=selected_matter[0],
                        attorney_email=attorney_email,
                        date=datetime.combine(date, datetime.now().time()),
                        hours=hours,
                        description=description,
                        billable_rate=billable_rate
                    )
                    
                    st.session_state.time_entries.append(new_entry)
                    
                    # Update matter's actual hours
                    matter = next((m for m in st.session_state.matters if m.id == selected_matter[0]), None)
                    if matter:
                        matter.actual_hours += hours
                    
                    st.success(f"Time entry logged: {hours} hours")
                    time.sleep(1)
                    st.rerun()
    
    st.divider()
    
    # Time entries list
    _show_time_entries_list()

def _show_time_entries_list():
    """Display time entries list"""
    if not st.session_state.time_entries:
        st.info("No time entries found. Log your first entry above!")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        matter_filter = st.selectbox("Filter by Matter", 
                                   ["All"] + [m.name for m in st.session_state.matters],
                                   key="time_matter_filter")
    
    with col2:
        attorney_filter = st.selectbox("Filter by Attorney", 
                                     ["All"] + list(set(e.attorney_email for e in st.session_state.time_entries)),
                                     key="time_attorney_filter")
    
    with col3:
        date_range = st.selectbox("Date Range", 
                                ["All", "Last 7 days", "Last 30 days", "This Month"])
    
    # Apply filters
    filtered_entries = st.session_state.time_entries.copy()
    
    if matter_filter != "All":
        matter_id = next((m.id for m in st.session_state.matters if m.name == matter_filter), None)
        if matter_id:
            filtered_entries = [e for e in filtered_entries if e.matter_id == matter_id]
    
    if attorney_filter != "All":
        filtered_entries = [e for e in filtered_entries if e.attorney_email == attorney_filter]
    
    if date_range != "All":
        now = datetime.now()
        if date_range == "Last 7 days":
            cutoff = now - timedelta(days=7)
        elif date_range == "Last 30 days":
            cutoff = now - timedelta(days=30)
        else:  # This Month
            cutoff = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        filtered_entries = [e for e in filtered_entries if e.date >= cutoff]
    
    # Sort by date (newest first)
    filtered_entries.sort(key=lambda x: x.date, reverse=True)
    
    # Summary
    total_hours = sum(e.hours for e in filtered_entries)
    total_value = sum(e.hours * e.billable_rate for e in filtered_entries)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Hours", f"{total_hours:.2f}")
    with col2:
        st.metric("Total Value", f"${total_value:,.2f}")
    
    st.markdown(f"**Showing {len(filtered_entries)} time entries**")
    
    # Display entries
    for entry in filtered_entries:
        _show_time_entry_card(entry)

def _show_time_entry_card(entry):
    """Display individual time entry card"""
    matter = next((m for m in st.session_state.matters if m.id == entry.matter_id), None)
    matter_name = matter.name if matter else "Unknown Matter"
    
    with st.expander(f"⏰ {entry.hours}h - {matter_name} - {entry.date.strftime('%Y-%m-%d')}"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**📋 Matter:** {matter_name}")
            st.markdown(f"**👤 Attorney:** {entry.attorney_email}")
        
        with col2:
            st.markdown(f"**📅 Date:** {entry.date.strftime('%Y-%m-%d %H:%M')}")
            st.markdown(f"**⏰ Hours:** {entry.hours}")
        
        with col3:
            st.markdown(f"**💰 Rate:** ${entry.billable_rate:.2f}/hr")
            st.markdown(f"**💵 Value:** ${entry.hours * entry.billable_rate:.2f}")
        
        st.markdown(f"**📝 Description:** {entry.description}")

def _show_expense_tracking(auth_service):
    """Expense tracking interface"""
    st.subheader("💰 Expense Tracking")
    
    # Log new expense
    if auth_service.has_permission('write'):
        with st.form("new_expense_form"):
            st.markdown("**➕ Log Expense**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                matter_options = [(m.id, f"{m.name} - {m.client_name}") for m in st.session_state.matters]
                if matter_options:
                    selected_matter = st.selectbox("Select Matter *", 
                                                 options=matter_options, 
                                                 format_func=lambda x: x[1])
                else:
                    st.warning("No matters available. Create a matter first.")
                    selected_matter = None
                amount = st.number_input("Amount ($) *", min_value=0.0, step=1.0)
                date = st.date_input("Date", value=datetime.now().date())
            
            with col2:
                category = st.selectbox("Category", 
                                      ["Travel", "Meals", "Supplies", "Filing Fees", 
                                       "Research", "Copying", "Other"])
                description = st.text_area("Description *", placeholder="Detail the expense...")
                is_billable = st.checkbox("Billable to Client", value=True)
            
            if st.form_submit_button("Log Expense"):
                if selected_matter and amount > 0 and description:
                    new_expense = MatterExpense(
                        id=str(uuid.uuid4()),
                        matter_id=selected_matter[0],
                        date=datetime.combine(date, datetime.now().time()),
                        amount=amount,
                        description=description,
                        category=category.lower(),
                        is_billable=is_billable
                    )
                    
                    st.session_state.matter_expenses.append(new_expense)
                    st.success(f"Expense logged: ${amount:.2f}")
                    time.sleep(1)
                    st.rerun()
    
    st.divider()
    
    # Expense list
    _show_expense_list()

def _show_expense_list():
    """Display expense list"""
    if not st.session_state.matter_expenses:
        st.info("No expenses found. Log your first expense above!")
        return
    
    # Summary metrics
    total_expenses = sum(e.amount for e in st.session_state.matter_expenses)
    billable_expenses = sum(e.amount for e in st.session_state.matter_expenses if e.is_billable)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Expenses", f"${total_expenses:.2f}")
    with col2:
        st.metric("Billable Expenses", f"${billable_expenses:.2f}")
    with col3:
        billable_pct = (billable_expenses / total_expenses * 100) if total_expenses > 0 else 0
        st.metric("Billable %", f"{billable_pct:.1f}%")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        matter_filter = st.selectbox("Filter by Matter", 
                                   ["All"] + [m.name for m in st.session_state.matters],
                                   key="expense_matter_filter")
    
    with col2:
        category_filter = st.selectbox("Filter by Category", 
                                     ["All", "Travel", "Meals", "Supplies", "Filing Fees", 
                                      "Research", "Copying", "Other"])
    
    with col3:
        billable_filter = st.selectbox("Billable Status", ["All", "Billable", "Non-Billable"])
    
    # Apply filters
    filtered_expenses = st.session_state.matter_expenses.copy()
    
    if matter_filter != "All":
        matter_id = next((m.id for m in st.session_state.matters if m.name == matter_filter), None)
        if matter_id:
            filtered_expenses = [e for e in filtered_expenses if e.matter_id == matter_id]
    
    if category_filter != "All":
        filtered_expenses = [e for e in filtered_expenses if e.category == category_filter.lower()]
    
    if billable_filter == "Billable":
        filtered_expenses = [e for e in filtered_expenses if e.is_billable]
    elif billable_filter == "Non-Billable":
        filtered_expenses = [e for e in filtered_expenses if not e.is_billable]
    
    # Sort by date (newest first)
    filtered_expenses.sort(key=lambda x: x.date, reverse=True)
    
    st.markdown(f"**Showing {len(filtered_expenses)} expenses**")
    
    # Display expenses
    for expense in filtered_expenses:
        _show_expense_card(expense)

def _show_expense_card(expense):
    """Display individual expense card"""
    matter = next((m for m in st.session_state.matters if m.id == expense.matter_id), None)
    matter_name = matter.name if matter else "Unknown Matter"
    
    billable_indicator = "💰" if expense.is_billable else "🚫"
    
    with st.expander(f"{billable_indicator} ${expense.amount:.2f} - {matter_name} - {expense.date.strftime('%Y-%m-%d')}"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**📋 Matter:** {matter_name}")
            st.markdown(f"**📂 Category:** {expense.category.title()}")
        
        with col2:
            st.markdown(f"**📅 Date:** {expense.date.strftime('%Y-%m-%d')}")
            st.markdown(f"**💰 Amount:** ${expense.amount:.2f}")
        
        with col3:
            st.markdown(f"**💳 Billable:** {'Yes' if expense.is_billable else 'No'}")
            st.markdown(f"**📎 Receipt:** {'Yes' if expense.receipt_attached else 'No'}")
        
        st.markdown(f"**📝 Description:** {expense.description}")

# Modal functions for enhanced interactions

def _show_matter_analytics_modal(matter):
    """Show detailed analytics for a specific matter"""
    st.subheader(f"📊 Analytics: {matter.name}")
    
    # Get related data
    matter_docs = [doc for doc in st.session_state.get('documents', []) 
                   if hasattr(doc, 'matter_id') and doc.matter_id == matter.id]
    matter_tasks = [task for task in st.session_state.tasks if task.matter_id == matter.id]
    matter_time = [entry for entry in st.session_state.time_entries if entry.matter_id == matter.id]
    matter_expenses = [exp for exp in st.session_state.matter_expenses if exp.matter_id == matter.id]
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Documents", len(matter_docs))
    
    with col2:
        st.metric("Tasks", len(matter_tasks))
        completed_tasks = len([t for t in matter_tasks if t.status == 'completed'])
        if matter_tasks:
            task_completion = completed_tasks / len(matter_tasks) * 100
            st.write(f"Completion: {task_completion:.1f}%")
    
    with col3:
        total_billed = matter.actual_hours * matter.hourly_rate
        st.metric("Billed Amount", f"${total_billed:,.2f}")
    
    with col4:
        total_expenses = sum(e.amount for e in matter_expenses)
        st.metric("Expenses", f"${total_expenses:.2f}")
    
    # Progress tracking
    if matter.budget > 0:
        budget_used = (total_billed / matter.budget) * 100
        st.progress(min(budget_used / 100, 1.0), text=f"Budget Utilization: {budget_used:.1f}%")
    
    if matter.estimated_hours > 0:
        hours_used = (matter.actual_hours / matter.estimated_hours) * 100
        st.progress(min(hours_used / 100, 1.0), text=f"Hours Utilization: {hours_used:.1f}%")

def _show_matter_editor(matter):
    """Show matter editing interface"""
    st.subheader(f"✏️ Edit Matter: {matter.name}")
    
    with st.form(f"edit_matter_{matter.id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Matter Name", value=matter.name)
            new_client = st.text_input("Client Name", value=matter.client_name)
            new_type = st.selectbox("Matter Type", 
                                  [mt.value.replace('_', ' ').title() for mt in MatterType],
                                  index=list(MatterType).index(MatterType(matter.matter_type)))
            new_priority = st.selectbox("Priority", 
                                      [p.value.title() for p in Priority],
                                      index=list(Priority).index(Priority(matter.priority)))
        
        with col2:
            new_description = st.text_area("Description", value=matter.description)
            new_budget = st.number_input("Budget", value=matter.budget, step=1000.0)
            new_estimated_hours = st.number_input("Estimated Hours", value=matter.estimated_hours, step=10.0)
            new_hourly_rate = st.number_input("Hourly Rate", value=matter.hourly_rate, step=25.0)
        
        if st.form_submit_button("💾 Save Changes"):
            matter.name = new_name
            matter.client_name = new_client
            matter.matter_type = new_type.lower().replace(' ', '_')
            matter.priority = new_priority.lower()
            matter.description = new_description
            matter.budget = new_budget
            matter.estimated_hours = new_estimated_hours
            matter.hourly_rate = new_hourly_rate
            
            st.success("Matter updated successfully!")
            time.sleep(1)
            st.rerun()

def _show_status_update_modal(matter):
    """Show status update interface"""
    st.subheader(f"🔄 Update Status: {matter.name}")
    
    new_status = st.selectbox("New Status", 
                            [s.value.title() for s in MatterStatus],
                            index=list(MatterStatus).index(MatterStatus(matter.status)))
    
    if st.button("Update Status"):
        matter.status = new_status.lower()
        if new_status.lower() == 'closed':
            matter.closed_date = datetime.now()
        
        st.success(f"Status updated to {new_status}")
        time.sleep(1)
        st.rerun()

def _show_matter_tasks(matter_id):
    """Show tasks for a specific matter"""
    matter = next((m for m in st.session_state.matters if m.id == matter_id), None)
    if not matter:
        return
    
    st.subheader(f"✅ Tasks: {matter.name}")
    
    matter_tasks = [task for task in st.session_state.tasks if task.matter_id == matter_id]
    
    if not matter_tasks:
        st.info("No tasks found for this matter.")
        return
    
    for task in matter_tasks:
        _show_task_card(task, AuthService())

def _show_matter_time_entries(matter_id):
    """Show time entries for a specific matter"""
    matter = next((m for m in st.session_state.matters if m.id == matter_id), None)
    if not matter:
        return
    
    st.subheader(f"⏰ Time Entries: {matter.name}")
    
    matter_time = [entry for entry in st.session_state.time_entries if entry.matter_id == matter_id]
    
    if not matter_time:
        st.info("No time entries found for this matter.")
        return
    
    total_hours = sum(e.hours for e in matter_time)
    total_value = sum(e.hours * e.billable_rate for e in matter_time)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Hours", f"{total_hours:.2f}")
    with col2:
        st.metric("Total Value", f"${total_value:,.2f}")
    
    for entry in matter_time:
        _show_time_entry_card(entry)

def _show_time_entry_modal(task):
    """Show time entry modal for a specific task"""
    st.subheader(f"⏰ Log Time: {task.title}")
    
    with st.form(f"time_entry_task_{task.id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            hours = st.number_input("Hours", min_value=0.0, step=0.25, value=1.0)
            rate = st.number_input("Rate ($)", min_value=0.0, step=25.0, value=250.0)
        
        with col2:
            date = st.date_input("Date", value=datetime.now().date())
            description = st.text_area("Work Description", placeholder="Describe work performed...")
        
        if st.form_submit_button("Log Time"):
            if hours > 0:
                new_entry = TimeEntry(
                    id=str(uuid.uuid4()),
                    matter_id=task.matter_id,
                    attorney_email="current@firm.com",
                    date=datetime.combine(date, datetime.now().time()),
                    hours=hours,
                    description=description,
                    billable_rate=rate,
                    task_id=task.id
                )
                
                st.session_state.time_entries.append(new_entry)
                task.actual_hours += hours
                
                # Update matter hours
                matter = next((m for m in st.session_state.matters if m.id == task.matter_id), None)
                if matter:
                    matter.actual_hours += hours
                
                st.success(f"Time logged: {hours} hours")
                time.sleep(1)
                st.rerun()

def _show_task_editor(task):
    """Show task editing interface"""
    st.subheader(f"✏️ Edit Task: {task.title}")
    
    with st.form(f"edit_task_{task.id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_title = st.text_input("Title", value=task.title)
            new_status = st.selectbox("Status", 
                                    ["Pending", "In Progress", "Completed", "Cancelled"],
                                    index=["pending", "in_progress", "completed", "cancelled"].index(task.status))
            new_priority = st.selectbox("Priority", 
                                      [p.value.title() for p in Priority],
                                      index=list(Priority).index(Priority(task.priority)))
        
        with col2:
            new_description = st.text_area("Description", value=task.description)
            new_due_date = st.date_input("Due Date", value=task.due_date.date())
            new_assigned_to = st.text_input("Assigned To", value=task.assigned_to)
        
        if st.form_submit_button("💾 Save Changes"):
            task.title = new_title
            task.status = new_status.lower().replace(' ', '_')
            task.priority = new_priority.lower()
            task.description = new_description
            task.due_date = datetime.combine(new_due_date, task.due_date.time())
            task.assigned_to = new_assigned_to
            
            st.success("Task updated successfully!")
            time.sleep(1)
            st.rerun()

# Main application integration
if __name__ == "__main__":
    st.set_page_config(
        page_title="Matter Management",
        page_icon="⚖️",
        layout="wide"
    )
    
    show()
