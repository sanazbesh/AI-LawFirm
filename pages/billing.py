import streamlit as st
import uuid
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from services.auth import AuthService
from models.billing import TimeEntry, Invoice

def show():
    auth_service = AuthService()
    
    st.title("Time Tracking & Billing")
    
    if not auth_service.has_permission('time_tracking'):
        st.error("Access denied. Time tracking access required.")
        st.stop()
    
    # Billing metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Unbilled Hours", "45.5")
    
    with col2:
        st.metric("Unbilled Amount", "$11,375")
    
    with col3:
        st.metric("Outstanding Invoices", "3")
    
    with col4:
        st.metric("Collection Rate", "94.2%")
    
    st.divider()
    
    # Time entry tabs
    tab1, tab2, tab3 = st.tabs(["Time Entry", "Billing", "Reports"])
    
    with tab1:
        _show_time_entry_tab()
    
    with tab2:
        _show_billing_tab()
    
    with tab3:
        _show_reports_tab()

def _show_time_entry_tab():
    st.subheader("Time Entry")
    
    with st.form("time_entry"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            entry_matter = st.selectbox("Matter", [f"{m.name}" for m in st.session_state.matters])
            entry_hours = st.number_input("Hours", min_value=0.0, max_value=24.0, value=1.0, step=0.25)
        
        with col2:
            entry_date = st.date_input("Date", value=datetime.now().date())
            entry_rate = st.number_input("Rate ($)", min_value=0.0, value=250.0, step=25.0)
        
        with col3:
            entry_activity = st.selectbox("Activity", ["Legal Research", "Document Review", "Client Meeting", "Court Appearance"])
            billable = st.checkbox("Billable", value=True)
        
        entry_description = st.text_area("Description", placeholder="Describe work performed...")
        
        if st.form_submit_button("Add Time Entry"):
            if entry_matter and entry_description:
                new_entry = TimeEntry(
                    id=str(uuid.uuid4()),
                    user_id=st.session_state['user']['email'],
                    matter_id="demo_matter",
                    client_id="demo_client",
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
                st.success("Time entry added!")
                st.rerun()
    
    st.divider()
    
    # Recent entries
    st.subheader("Recent Time Entries")
    
    if st.session_state.time_entries:
        for entry in st.session_state.time_entries[-5:]:
            with st.container():
                st.write(f"**{entry.activity_type}** - {entry.hours} hours")
                st.write(f"Description: {entry.description[:80]}...")
                st.write(f"Status: {entry.status.upper()}")
                st.write("---")
    else:
        st.info("No time entries yet. Add your first time entry above.")

def _show_billing_tab():
    st.subheader("Invoice Generation")
    
    with st.form("generate_invoice"):
        col1, col2 = st.columns(2)
        
        with col1:
            invoice_client = st.selectbox("Client", [c.name for c in st.session_state.clients])
            billing_start = st.date_input("Period Start", value=datetime.now().replace(day=1).date())
        
        with col2:
            invoice_matter = st.selectbox("Matter", [m.name for m in st.session_state.matters])
            billing_end = st.date_input("Period End", value=datetime.now().date())
        
        if st.form_submit_button("Generate Invoice"):
            new_invoice = Invoice(
                id=str(uuid.uuid4()),
                client_id="client_1",
                matter_id="matter_1",
                invoice_number=f"INV-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.invoices) + 1:04d}",
                date_issued=datetime.now(),
                due_date=datetime.now() + timedelta(days=30),
                line_items=[{"description": "Legal services", "amount": 5000.0}],
                subtotal=5000.0,
                tax_rate=0.08,
                tax_amount=400.0,
                total_amount=5400.0,
                status="draft"
            )
            
            st.session_state.invoices.append(new_invoice)
            st.success(f"Invoice {new_invoice.invoice_number} generated!")
            st.rerun()
    
    st.divider()
    
    # Invoice list
    st.subheader("Recent Invoices")

    if st.session_state.invoices:
        for invoice in st.session_state.invoices:
            with st.container():
                st.write(f"**Invoice {invoice.invoice_number}**")
                st.write(f"Issued: {invoice.date_issued.strftime('%Y-%m-%d')} | Due: {invoice.due_date.strftime('%Y-%m-%d')}")
                st.write(f"Amount: ${invoice.total_amount:,.2f}")
                st.write(f"Status: {invoice.status.upper()}")
                st.write("---")
    else:
        st.info("No invoices generated yet.")

def _show_reports_tab():
    st.subheader("Billing Reports")
    
    # Monthly billing chart
    monthly_data = {
        'Jan': 15000, 'Feb': 18000, 'Mar': 22000, 'Apr': 19000,
        'May': 25000, 'Jun': 28000, 'Jul': 24000, 'Aug': 30000
    }
    
    fig = px.bar(x=list(monthly_data.keys()), y=list(monthly_data.values()),
                 title="Monthly Billing Revenue")
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance summary
    st.subheader("Billing Performance")
    
    performance_data = pd.DataFrame({
        'Metric': ['Total Billed', 'Total Collected', 'Collection Rate', 'Avg Days to Pay'],
        'This Quarter': ['$85,000', '$80,000', '94.1%', '28 days'],
        'Last Quarter': ['$78,000', '$72,000', '92.3%', '32 days'],
        'Change': ['+9.0%', '+11.1%', '+1.8pp', '-4 days']
    })
    
    st.dataframe(performance_data, hide_index=True)
