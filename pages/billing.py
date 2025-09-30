import streamlit as st
import uuid
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Optional

# Mock data classes (since services and models aren't available)
@dataclass
class TimeEntry:
    id: str
    user_id: str
    matter_id: str
    client_id: str
    date: datetime
    hours: float
    description: str
    billing_rate: float
    billable: bool
    activity_type: str
    status: str
    created_date: datetime

@dataclass
class Invoice:
    id: str
    client_id: str
    matter_id: str
    invoice_number: str
    date_issued: datetime
    due_date: datetime
    line_items: List[dict]
    subtotal: float
    tax_rate: float
    tax_amount: float
    total_amount: float
    status: str

@dataclass
class Client:
    id: str
    name: str
    company: str
    email: str

@dataclass
class Matter:
    id: str
    name: str
    client_id: str
    description: str

# Mock auth service
class AuthService:
    def has_permission(self, permission: str) -> bool:
        return True  # Mock implementation

def initialize_session_state():
    """Initialize session state with mock data if not already present"""
    if 'time_entries' not in st.session_state:
        st.session_state.time_entries = []
    
    if 'invoices' not in st.session_state:
        st.session_state.invoices = []
    
    if 'clients' not in st.session_state:
        st.session_state.clients = [
            Client("1", "ABC Corporation", "ABC Corp", "contact@abc.com"),
            Client("2", "Tech Solutions Inc", "Tech Solutions", "info@techsolutions.com"),
            Client("3", "Global Manufacturing", "Global Mfg", "admin@globalmfg.com")
        ]
    
    if 'matters' not in st.session_state:
        st.session_state.matters = [
            Matter("1", "Corporate Restructuring", "1", "Major restructuring project"),
            Matter("2", "IP Licensing Agreement", "2", "Software licensing negotiations"),
            Matter("3", "Employment Contract Review", "3", "Executive employment contracts")
        ]
    
    if 'user' not in st.session_state:
        st.session_state.user = {'email': 'user@lawfirm.com', 'name': 'John Attorney'}

def show():
    initialize_session_state()
    auth_service = AuthService()
    # Professional header styling
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
    
    if not auth_service.has_permission('time_tracking'):
        st.error("Access denied. Time tracking access required.")
        st.stop()
    
    # Calculate real-time billing metrics
    total_unbilled_hours = sum(entry.hours for entry in st.session_state.time_entries if entry.status == "draft" and entry.billable)
    total_unbilled_amount = sum(entry.hours * entry.billing_rate for entry in st.session_state.time_entries if entry.status == "draft" and entry.billable)
    outstanding_invoices = len([inv for inv in st.session_state.invoices if inv.status in ["sent", "overdue"]])
    collection_rate = 94.2  # Mock value
    
    # Billing metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Unbilled Hours", f"{total_unbilled_hours:.1f}", delta="5.2")
    
    with col2:
        st.metric("Unbilled Amount", f"${total_unbilled_amount:,.0f}", delta="$2,840")
    
    with col3:
        st.metric("Outstanding Invoices", str(outstanding_invoices), delta="-1")
    
    with col4:
        st.metric("Collection Rate", f"{collection_rate}%", delta="2.1%")
    
    st.divider()
    
    # Time entry tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⏱️ Time Entry", 
        "📄 Billing & Invoices", 
        "📊 Reports & Analytics",
        "🎯 Time Management",
        "💰 Revenue Tracking"
    ])
    
    with tab1:
        _show_time_entry_tab()
    
    with tab2:
        _show_billing_tab()
    
    with tab3:
        _show_reports_tab()
    
    with tab4:
        _show_time_management_tab()
    
    with tab5:
        _show_revenue_tracking_tab()

def _show_time_entry_tab():
    st.subheader("Time Entry Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Quick time entry form
        st.markdown("#### Quick Time Entry")
        
        with st.form("time_entry"):
            col_form1, col_form2, col_form3 = st.columns(3)
            
            with col_form1:
                entry_matter = st.selectbox("Matter", [f"{m.name}" for m in st.session_state.matters])
                entry_hours = st.number_input("Hours", min_value=0.0, max_value=24.0, value=1.0, step=0.25)
            
            with col_form2:
                entry_date = st.date_input("Date", value=datetime.now().date())
                entry_rate = st.number_input("Rate ($)", min_value=0.0, value=250.0, step=25.0)
            
            with col_form3:
                entry_activity = st.selectbox("Activity", [
                    "Legal Research", "Document Review", "Client Meeting", 
                    "Court Appearance", "Drafting", "Phone Conference",
                    "Email Communication", "Case Preparation", "Administrative"
                ])
                billable = st.checkbox("Billable", value=True)
            
            entry_description = st.text_area("Description", placeholder="Describe work performed...", height=100)
            
            col_submit1, col_submit2 = st.columns(2)
            with col_submit1:
                if st.form_submit_button("Add Time Entry", type="primary"):
                    if entry_matter and entry_description:
                        selected_matter = next((m for m in st.session_state.matters if m.name == entry_matter), None)
                        
                        new_entry = TimeEntry(
                            id=str(uuid.uuid4()),
                            user_id=st.session_state['user']['email'],
                            matter_id=selected_matter.id if selected_matter else "1",
                            client_id=selected_matter.client_id if selected_matter else "1",
                            date=datetime.combine(entry_date, datetime.now().time()),
                            hours=entry_hours,
                            description=entry_description,
                            billing_rate=entry_rate,
                            billable=billable,
                            activity_type=entry_activity,
                            status="draft",
                            created_date=datetime.now()
                        )
                        
                        st.session_state.time_entries.append(new_entry)
                        st.success("Time entry added successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill in all required fields.")
            
            with col_submit2:
                if st.form_submit_button("Save as Template"):
                    st.info("Time entry template saved!")
        
        # Timer functionality
        st.markdown("#### Active Timer")
        
        col_timer1, col_timer2, col_timer3 = st.columns(3)
        
        with col_timer1:
            timer_matter = st.selectbox("Timer Matter:", [f"{m.name}" for m in st.session_state.matters], key="timer_matter")
            timer_activity = st.selectbox("Timer Activity:", [
                "Legal Research", "Document Review", "Client Meeting", "Court Appearance"
            ], key="timer_activity")
        
        with col_timer2:
            if 'timer_start' not in st.session_state:
                st.session_state.timer_start = None
            
            if st.session_state.timer_start:
                elapsed = datetime.now() - st.session_state.timer_start
                st.write(f"**Elapsed Time:** {str(elapsed).split('.')[0]}")
                
                if st.button("⏹️ Stop Timer", type="secondary"):
                    hours = elapsed.total_seconds() / 3600
                    st.session_state.timer_hours = round(hours, 2)
                    st.session_state.timer_start = None
                    st.success(f"Timer stopped. {st.session_state.timer_hours} hours recorded.")
                    st.rerun()
            else:
                if st.button("▶️ Start Timer", type="primary"):
                    st.session_state.timer_start = datetime.now()
                    st.rerun()
        
        with col_timer3:
            if 'timer_hours' in st.session_state and st.session_state.timer_hours:
                st.write(f"**Recorded Time:** {st.session_state.timer_hours} hours")
                if st.button("💾 Save Timer Entry"):
                    # Auto-fill form with timer data
                    st.info("Timer data ready to save. Fill in description and submit.")
        
        # Recent entries management
        st.markdown("#### Recent Time Entries")
        
        if st.session_state.time_entries:
            # Filter controls
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            with col_filter1:
                status_filter = st.selectbox("Filter by Status:", ["All", "draft", "billed", "approved"])
            with col_filter2:
                date_filter = st.date_input("From Date:", value=datetime.now().date() - timedelta(days=30))
            with col_filter3:
                billable_filter = st.selectbox("Billable:", ["All", "Yes", "No"])
            
            filtered_entries = st.session_state.time_entries
            if status_filter != "All":
                filtered_entries = [e for e in filtered_entries if e.status == status_filter]
            if billable_filter != "All":
                filtered_entries = [e for e in filtered_entries if e.billable == (billable_filter == "Yes")]
            
            for i, entry in enumerate(reversed(filtered_entries[-10:])):
                with st.expander(f"⏱️ {entry.activity_type} - {entry.hours}h - ${entry.hours * entry.billing_rate:.2f}"):
                    col_entry1, col_entry2, col_entry3 = st.columns(3)
                    
                    with col_entry1:
                        st.write(f"**Date:** {entry.date.strftime('%Y-%m-%d')}")
                        st.write(f"**Matter:** {next((m.name for m in st.session_state.matters if m.id == entry.matter_id), 'Unknown')}")
                        st.write(f"**Hours:** {entry.hours}")
                    
                    with col_entry2:
                        st.write(f"**Rate:** ${entry.billing_rate:.2f}/hr")
                        st.write(f"**Amount:** ${entry.hours * entry.billing_rate:.2f}")
                        st.write(f"**Billable:** {'Yes' if entry.billable else 'No'}")
                    
                    with col_entry3:
                        st.write(f"**Status:** {entry.status.upper()}")
                        st.write(f"**Description:** {entry.description[:50]}...")
                        
                        col_action1, col_action2 = st.columns(2)
                        with col_action1:
                            if st.button("✏️ Edit", key=f"edit_{i}"):
                                st.info("Edit functionality would open here")
                        with col_action2:
                            if st.button("🗑️ Delete", key=f"delete_{i}"):
                                st.session_state.time_entries.remove(entry)
                                st.success("Entry deleted")
                                st.rerun()
        else:
            st.info("No time entries yet. Add your first time entry above.")
    
    with col2:
        st.markdown("#### Today's Summary")
        
        today_entries = [e for e in st.session_state.time_entries 
                        if e.date.date() == datetime.now().date()]
        
        if today_entries:
            total_hours = sum(e.hours for e in today_entries)
            billable_hours = sum(e.hours for e in today_entries if e.billable)
            total_value = sum(e.hours * e.billing_rate for e in today_entries if e.billable)
            
            st.metric("Total Hours", f"{total_hours:.1f}")
            st.metric("Billable Hours", f"{billable_hours:.1f}")
            st.metric("Value Created", f"${total_value:.0f}")
        else:
            st.info("No entries for today")
        
        st.markdown("#### Quick Actions")
        
        if st.button("📋 Time Entry Templates"):
            st.info("Loading saved templates...")
        if st.button("📊 Weekly Summary"):
            st.info("Generating weekly report...")
        if st.button("⏰ Set Reminders"):
            st.info("Opening reminder settings...")
        if st.button("📤 Export Timesheet"):
            st.info("Preparing timesheet export...")

def _show_billing_tab():
    st.subheader("Invoice Generation & Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Invoice generation
        st.markdown("#### Generate New Invoice")
        
        with st.form("generate_invoice"):
            col_invoice1, col_invoice2 = st.columns(2)
            
            with col_invoice1:
                invoice_client = st.selectbox("Client", [c.name for c in st.session_state.clients])
                billing_start = st.date_input("Period Start", value=datetime.now().replace(day=1).date())
                
                # Show unbilled entries for selected client
                selected_client = next((c for c in st.session_state.clients if c.name == invoice_client), None)
                if selected_client:
                    unbilled_entries = [e for e in st.session_state.time_entries 
                                      if e.client_id == selected_client.id and e.status == "draft" and e.billable]
                    st.write(f"**Unbilled entries:** {len(unbilled_entries)} ({sum(e.hours for e in unbilled_entries):.1f} hours)")
            
            with col_invoice2:
                invoice_matter = st.selectbox("Matter", [m.name for m in st.session_state.matters])
                billing_end = st.date_input("Period End", value=datetime.now().date())
                
                payment_terms = st.selectbox("Payment Terms", ["Net 30", "Net 15", "Due on Receipt", "Net 60"])
                include_expenses = st.checkbox("Include Expenses", value=True)
            
            invoice_notes = st.text_area("Invoice Notes", placeholder="Additional notes for this invoice...")
            
            if st.form_submit_button("Generate Invoice", type="primary"):
                # Calculate invoice totals from unbilled entries
                if selected_client:
                    unbilled_entries = [e for e in st.session_state.time_entries 
                                      if e.client_id == selected_client.id and e.status == "draft" and e.billable]
                    
                    subtotal = sum(e.hours * e.billing_rate for e in unbilled_entries)
                    tax_rate = 0.08
                    tax_amount = subtotal * tax_rate
                    total_amount = subtotal + tax_amount
                    
                    # Create line items from time entries
                    line_items = []
                    for entry in unbilled_entries:
                        line_items.append({
                            "description": f"{entry.activity_type}: {entry.description[:50]}...",
                            "hours": entry.hours,
                            "rate": entry.billing_rate,
                            "amount": entry.hours * entry.billing_rate
                        })
                    
                    new_invoice = Invoice(
                        id=str(uuid.uuid4()),
                        client_id=selected_client.id,
                        matter_id="matter_1",
                        invoice_number=f"INV-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.invoices) + 1:04d}",
                        date_issued=datetime.now(),
                        due_date=datetime.now() + timedelta(days=30),
                        line_items=line_items,
                        subtotal=subtotal,
                        tax_rate=tax_rate,
                        tax_amount=tax_amount,
                        total_amount=total_amount,
                        status="draft"
                    )
                    
                    st.session_state.invoices.append(new_invoice)
                    
                    # Mark time entries as billed
                    for entry in unbilled_entries:
                        entry.status = "billed"
                    
                    st.success(f"Invoice {new_invoice.invoice_number} generated! Total: ${total_amount:.2f}")
                    st.rerun()
                else:
                    st.error("Please select a valid client.")
        
        # Invoice management
        st.markdown("#### Invoice Management")
        
        if st.session_state.invoices:
            # Invoice filters
            col_inv_filter1, col_inv_filter2 = st.columns(2)
            with col_inv_filter1:
                invoice_status_filter = st.selectbox("Filter by Status:", ["All", "draft", "sent", "paid", "overdue"])
            with col_inv_filter2:
                invoice_date_filter = st.date_input("From Date:", value=datetime.now().date() - timedelta(days=90))
            
            filtered_invoices = st.session_state.invoices
            if invoice_status_filter != "All":
                filtered_invoices = [inv for inv in filtered_invoices if inv.status == invoice_status_filter]
            
            for invoice in filtered_invoices:
                status_colors = {
                    "draft": "🟡",
                    "sent": "🔵", 
                    "paid": "🟢",
                    "overdue": "🔴"
                }
                
                with st.expander(f"{status_colors.get(invoice.status, '⚪')} Invoice {invoice.invoice_number} - ${invoice.total_amount:,.2f}"):
                    col_inv1, col_inv2, col_inv3 = st.columns(3)
                    
                    with col_inv1:
                        client = next((c for c in st.session_state.clients if c.id == invoice.client_id), None)
                        st.write(f"**Client:** {client.name if client else 'Unknown'}")
                        st.write(f"**Issued:** {invoice.date_issued.strftime('%Y-%m-%d')}")
                        st.write(f"**Due:** {invoice.due_date.strftime('%Y-%m-%d')}")
                    
                    with col_inv2:
                        st.write(f"**Subtotal:** ${invoice.subtotal:,.2f}")
                        st.write(f"**Tax ({invoice.tax_rate*100:.0f}%):** ${invoice.tax_amount:,.2f}")
                        st.write(f"**Total:** ${invoice.total_amount:,.2f}")
                    
                    with col_inv3:
                        st.write(f"**Status:** {invoice.status.upper()}")
                        
                        col_inv_action1, col_inv_action2 = st.columns(2)
                        with col_inv_action1:
                            if st.button("📄 View PDF", key=f"pdf_{invoice.id}"):
                                st.info("PDF generation would occur here")
                        with col_inv_action2:
                            if invoice.status == "draft" and st.button("📤 Send", key=f"send_{invoice.id}"):
                                invoice.status = "sent"
                                st.success("Invoice sent!")
                                st.rerun()
                    
                    # Show line items
                    if invoice.line_items:
                        st.write("**Line Items:**")
                        for item in invoice.line_items:
                            st.write(f"• {item['description']} - ${item['amount']:.2f}")
        else:
            st.info("No invoices generated yet.")
    
    with col2:
        st.markdown("#### Billing Summary")
        
        # Calculate billing metrics
        total_invoiced = sum(inv.total_amount for inv in st.session_state.invoices)
        paid_invoices = sum(inv.total_amount for inv in st.session_state.invoices if inv.status == "paid")
        outstanding = sum(inv.total_amount for inv in st.session_state.invoices if inv.status in ["sent", "overdue"])
        
        st.metric("Total Invoiced", f"${total_invoiced:,.0f}")
        st.metric("Paid", f"${paid_invoices:,.0f}")
        st.metric("Outstanding", f"${outstanding:,.0f}")
        
        # Collection rate calculation
        collection_rate = (paid_invoices / total_invoiced * 100) if total_invoiced > 0 else 0
        st.metric("Collection Rate", f"{collection_rate:.1f}%")
        
        st.markdown("#### Invoice Status Breakdown")
        
        status_counts = {}
        for invoice in st.session_state.invoices:
            status_counts[invoice.status] = status_counts.get(invoice.status, 0) + 1
        
        for status, count in status_counts.items():
            st.write(f"**{status.title()}:** {count}")
        
        st.markdown("#### Quick Actions")
        
        if st.button("📧 Send Reminders"):
            st.info("Sending payment reminders...")
        if st.button("📊 Aging Report"):
            st.info("Generating aging report...")
        if st.button("💳 Record Payment"):
            st.info("Opening payment recording...")
        if st.button("📋 Export Invoices"):
            st.info("Preparing invoice export...")

def _show_reports_tab():
    st.subheader("Billing Reports & Analytics")
    
    # Monthly billing trend
    st.markdown("#### Monthly Billing Revenue")
    
    # Generate sample monthly data
    months = pd.date_range('2024-01-01', '2024-09-01', freq='MS')
    monthly_data = pd.DataFrame({
        'Month': months,
        'Billed': [15000, 18000, 22000, 19000, 25000, 28000, 24000, 30000, 27000],
        'Collected': [14000, 17000, 20000, 18000, 23000, 26000, 22000, 28000, 25000]
    })
    
    fig = px.bar(monthly_data, x='Month', y=['Billed', 'Collected'],
                 title="Monthly Billing vs Collections", barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance metrics
    col_report1, col_report2 = st.columns(2)
    
    with col_report1:
        st.markdown("#### Billing Performance")
        
        performance_data = pd.DataFrame({
            'Metric': ['Total Billed', 'Total Collected', 'Collection Rate', 'Avg Days to Pay'],
            'This Quarter': ['$85,000', '$80,000', '94.1%', '28 days'],
            'Last Quarter': ['$78,000', '$72,000', '92.3%', '32 days'],
            'Change': ['+9.0%', '+11.1%', '+1.8pp', '-4 days']
        })
        
        st.dataframe(performance_data, hide_index=True)
    
    with col_report2:
        st.markdown("#### Top Billing Activities")
        
        activity_data = pd.DataFrame({
            'Activity': ['Document Review', 'Legal Research', 'Client Meetings', 'Court Appearances', 'Drafting'],
            'Hours': [245, 189, 156, 98, 134],
            'Revenue': [61250, 47250, 39000, 24500, 33500]
        })
        
        fig2 = px.pie(activity_data, values='Revenue', names='Activity',
                     title="Revenue by Activity Type")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Time utilization analysis
    st.markdown("#### Time Utilization Analysis")
    
    utilization_data = pd.DataFrame({
        'Attorney': ['John Smith', 'Sarah Johnson', 'Mike Davis', 'Emily Chen'],
        'Billable Hours': [180, 165, 142, 156],
        'Total Hours': [200, 185, 160, 175],
        'Utilization %': [90, 89, 89, 89],
        'Revenue': [45000, 41250, 35500, 39000]
    })
    
    fig3 = px.scatter(utilization_data, x='Billable Hours', y='Revenue',
                     size='Total Hours', color='Utilization %',
                     hover_name='Attorney',
                     title='Attorney Performance Matrix')
    st.plotly_chart(fig3, use_container_width=True)
    
    # Detailed reporting options
    st.markdown("#### Generate Reports")
    
    col_gen1, col_gen2, col_gen3 = st.columns(3)
    
    with col_gen1:
        report_type = st.selectbox("Report Type", [
            "Time Summary", "Revenue Analysis", "Client Billing", 
            "Matter Profitability", "Attorney Performance"
        ])
    
    with col_gen2:
        report_period = st.selectbox("Period", [
            "This Month", "Last Month", "This Quarter", 
            "Last Quarter", "Year to Date", "Custom"
        ])
    
    with col_gen3:
        report_format = st.selectbox("Format", ["PDF", "Excel", "CSV"])
    
    if st.button("🔄 Generate Report", type="primary"):
        st.success(f"Generating {report_type} report for {report_period} in {report_format} format...")

def _show_time_management_tab():
    st.subheader("Time Management & Productivity")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Weekly time tracking overview
        st.markdown("#### Weekly Time Overview")
        
        # Generate weekly data
        dates = pd.date_range('2024-09-17', '2024-09-23', freq='D')
        daily_hours = pd.DataFrame({
            'Date': dates,
            'Billable': [7.5, 8.0, 6.5, 9.0, 7.0, 4.0, 2.0],
            'Non-Billable': [1.5, 1.0, 2.0, 0.5, 2.0, 1.0, 0.5],
            'Target': [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0]
        })
        
        fig_weekly = px.bar(daily_hours, x='Date', y=['Billable', 'Non-Billable'],
                           title="Daily Hours Breakdown")
        fig_weekly.add_scatter(x=daily_hours['Date'], y=daily_hours['Target'], 
                              mode='lines', name='Target', line=dict(color='red', dash='dash'))
        st.plotly_chart(fig_weekly, use_container_width=True)
        
        # Time allocation by matter
        st.markdown("#### Time Allocation by Matter")
        
        matter_allocation = pd.DataFrame({
            'Matter': ['Corporate Restructuring', 'IP Licensing', 'Employment Contracts', 'Compliance Review'],
            'Hours This Week': [25.5, 18.0, 12.5, 8.0],
            'Budget Hours': [40.0, 30.0, 20.0, 15.0],
            'Percentage Complete': [64, 60, 63, 53]
        })
        
        for _, matter in matter_allocation.iterrows():
            col_matter1, col_matter2, col_matter3 = st.columns([2, 1, 1])
            
            with col_matter1:
                st.write(f"**{matter['Matter']}**")
                progress = matter['Hours This Week'] / matter['Budget Hours']
                st.progress(min(progress, 1.0))
                st.write(f"{matter['Hours This Week']:.1f}h / {matter['Budget Hours']:.1f}h budgeted")
            
            with col_matter2:
                st.metric("This Week", f"{matter['Hours This Week']}h")
            
            with col_matter3:
                st.metric("Complete", f"{matter['Percentage Complete']}%")
        
        # Productivity insights
        st.markdown("#### Productivity Insights")
        
        insights = [
            {"icon": "📈", "title": "Peak Performance", "description": "Your most productive hours are 9-11 AM with 2.3x efficiency"},
            {"icon": "⚡", "title": "Activity Focus", "description": "Document Review generates highest revenue per hour ($312/hr)"},
            {"icon": "🎯", "title": "Goal Progress", "description": "You're 12% ahead of monthly billing target"},
            {"icon": "⚠️", "title": "Attention Needed", "description": "3 matters are approaching deadline with unbilled hours"}
        ]
        
        for insight in insights:
            with st.container():
                col_insight1, col_insight2 = st.columns([1, 10])
                with col_insight1:
                    st.write(insight["icon"])
                with col_insight2:
                    st.write(f"**{insight['title']}:** {insight['description']}")
    
    with col2:
        st.markdown("#### Today's Goals")
        
        goals = [
            {"task": "Complete contract review", "progress": 75, "hours": "2.5h"},
            {"task": "Client presentation prep", "progress": 30, "hours": "1.5h"},
                            {"task": "Research case law", "progress": 50, "hours": "3.0h"},
            {"task": "Draft motion documents", "progress": 10, "hours": "2.0h"}
        ]
        
        for goal in goals:
            st.write(f"**{goal['task']}** ({goal['hours']})")
            st.progress(goal['progress'] / 100)
        
        st.markdown("#### Time Tracking Tips")
        
        tips = [
            "Use the timer for better accuracy",
            "Log time entries immediately",
            "Be specific in descriptions",
            "Track non-billable admin time",
            "Review weekly patterns"
        ]
        
        for tip in tips:
            st.write(f"• {tip}")
        
        st.markdown("#### Quick Stats")
        
        stats = [
            ("Week Target", "40h", "92%"),
            ("Billable Rate", "85%", "+3%"),
            ("Avg Entry", "1.8h", "Stable")
        ]
        
        for label, value, change in stats:
            st.metric(label, value, change)

def _show_revenue_tracking_tab():
    st.subheader("Revenue Tracking & Forecasting")
    
    # Revenue dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Revenue Trends")
        
        # Monthly revenue data
        revenue_months = pd.date_range('2024-01-01', '2024-09-01', freq='MS')
        revenue_data = pd.DataFrame({
            'Month': revenue_months,
            'Actual Revenue': [85000, 92000, 78000, 95000, 88000, 102000, 96000, 105000, 98000],
            'Projected Revenue': [80000, 85000, 85000, 90000, 90000, 95000, 95000, 100000, 100000],
            'Target Revenue': [90000, 90000, 90000, 90000, 90000, 90000, 90000, 90000, 90000]
        })
        
        fig_revenue = px.line(revenue_data, x='Month', 
                             y=['Actual Revenue', 'Projected Revenue', 'Target Revenue'],
                             title='Revenue Performance vs Targets')
        st.plotly_chart(fig_revenue, use_container_width=True)
        
        # Client revenue breakdown
        st.markdown("#### Revenue by Client")
        
        client_revenue = pd.DataFrame({
            'Client': ['ABC Corporation', 'Tech Solutions Inc', 'Global Manufacturing', 'Startup Innovations'],
            'YTD Revenue': [245000, 180000, 145000, 85000],
            'Q3 Revenue': [65000, 48000, 38000, 22000],
            'Growth': [12.5, -5.2, 8.9, 15.3]
        })
        
        for _, client in client_revenue.iterrows():
            col_client1, col_client2, col_client3, col_client4 = st.columns(4)
            
            with col_client1:
                st.write(f"**{client['Client']}**")
            with col_client2:
                st.metric("YTD", f"${client['YTD Revenue']:,}")
            with col_client3:
                st.metric("Q3", f"${client['Q3 Revenue']:,}")
            with col_client4:
                delta_color = "normal" if client['Growth'] >= 0 else "inverse"
                st.metric("Growth", f"{client['Growth']:+.1f}%", delta=f"{client['Growth']:+.1f}%")
    
    with col2:
        st.markdown("#### Revenue Forecasting")
        
        # Forecasting parameters
        with st.form("forecast_params"):
            forecast_period = st.selectbox("Forecast Period", ["Next Quarter", "Next 6 Months", "Next Year"])
            growth_assumption = st.slider("Growth Rate (%)", -10.0, 20.0, 5.0, 0.5)
            seasonal_factor = st.checkbox("Apply Seasonal Adjustments", value=True)
            
            if st.form_submit_button("Generate Forecast"):
                st.success(f"Forecast generated with {growth_assumption}% growth assumption")
        
        # Key revenue metrics
        st.markdown("#### Key Revenue Metrics")
        
        revenue_metrics = [
            ("Revenue Run Rate", "$1.2M", "+8.5%"),
            ("Avg Client Value", "$45K", "+12%"),
            ("Revenue per Hour", "$285", "+3.2%"),
            ("Collection Efficiency", "94.2%", "+1.8%")
        ]
        
        for metric, value, change in revenue_metrics:
            st.metric(metric, value, change)
        
        # Revenue opportunities
        st.markdown("#### Revenue Opportunities")
        
        opportunities = [
            {"type": "Rate Increase", "impact": "$25K", "confidence": "High"},
            {"type": "New Service Line", "impact": "$40K", "confidence": "Medium"},
            {"type": "Client Expansion", "impact": "$60K", "confidence": "High"},
            {"type": "Efficiency Gains", "impact": "$15K", "confidence": "Medium"}
        ]
        
        for opp in opportunities:
            confidence_colors = {"High": "🟢", "Medium": "🟡", "Low": "🔴"}
            st.write(f"{confidence_colors[opp['confidence']]} **{opp['type']}**: {opp['impact']} ({opp['confidence']} confidence)")
    
    # Detailed revenue analysis
    st.markdown("#### Detailed Revenue Analysis")
    
    col_analysis1, col_analysis2 = st.columns(2)
    
    with col_analysis1:
        st.markdown("#### Matter Profitability")
        
        matter_profit = pd.DataFrame({
            'Matter': ['Corporate Restructuring', 'IP Licensing Agreement', 'Employment Contract Review', 'Compliance Review'],
            'Revenue': [145000, 89000, 67000, 34000],
            'Costs': [25000, 15000, 12000, 8000],
            'Profit': [120000, 74000, 55000, 26000],
            'Margin': [82.8, 83.1, 82.1, 76.5]
        })
        
        fig_profit = px.bar(matter_profit, x='Matter', y='Profit',
                           color='Margin', color_continuous_scale='RdYlGn',
                           title='Matter Profitability Analysis')
        fig_profit.update_layout(xaxis=dict(tickangle=45))
        st.plotly_chart(fig_profit, use_container_width=True)
    
    with col_analysis2:
        st.markdown("#### Revenue Quality Score")
        
        quality_factors = pd.DataFrame({
            'Factor': ['Client Diversity', 'Payment Terms', 'Rate Stability', 'Recurring Revenue', 'Collection Rate'],
            'Score': [85, 78, 92, 65, 94],
            'Weight': [20, 15, 25, 15, 25]
        })
        
        # Calculate weighted score
        weighted_score = sum(quality_factors['Score'] * quality_factors['Weight']) / sum(quality_factors['Weight'])
        
        st.metric("Overall Revenue Quality", f"{weighted_score:.0f}/100")
        
        fig_quality = px.bar(quality_factors, x='Factor', y='Score',
                            title='Revenue Quality Factors')
        fig_quality.update_layout(xaxis=dict(tickangle=45))
        st.plotly_chart(fig_quality, use_container_width=True)
    
    # Revenue action items
    st.markdown("#### Revenue Action Items")
    
    action_items = [
        {"priority": "High", "action": "Follow up on overdue invoices totaling $45K", "due": "This Week"},
        {"priority": "Medium", "action": "Prepare rate increase proposal for Q4", "due": "Next Month"},
        {"priority": "High", "action": "Review and optimize billing processes", "due": "Next Week"},
        {"priority": "Low", "action": "Analyze client profitability for strategic planning", "due": "Next Quarter"}
    ]
    
    priority_colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
    
    for item in action_items:
        col_action1, col_action2, col_action3 = st.columns([1, 6, 2])
        
        with col_action1:
            st.write(priority_colors[item['priority']])
        with col_action2:
            st.write(item['action'])
        with col_action3:
            st.write(f"**{item['due']}**")

# Main execution
if __name__ == "__main__":
    show()
