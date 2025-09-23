import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import time
import pyrebase
import uuid
import re
from typing import Dict, List, Optional, Tuple, Union
import difflib
from dataclasses import dataclass, asdict, field
from enum import Enum
import base64
import io
from PIL import Image
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import imaplib
import email
import calendar
from icalendar import Calendar, Event
import requests
from cryptography.fernet import Fernet
import qrcode
import stripe  # For payment processing
from twilio.rest import Client  # For SMS notifications
import openai  # For advanced AI features
from transformers import pipeline  # For local AI models
import spacy  # For advanced NLP
import networkx as nx  # For relationship mapping
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import docx
from docx2python import docx2python
import zipfile
import tempfile

# Configure page with enhanced settings
st.set_page_config(
    page_title="LegalDoc Pro - Complete Enterprise Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure page
st.set_page_config(
    page_title="LegalDoc Pro - Complete Enterprise Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

elif page == "Mobile App":
    st.title("📱 Mobile Application")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📱 Mobile Features")
        
        mobile_features = [
            ("📄 Document Viewer", "View and annotate documents on-the-go"),
            ("📸 Document Scanner", "Scan and upload documents using camera"),
            ("🎙️ Voice Notes", "Record voice memos for matters"),
            ("⏱️ Time Tracking", "Track billable hours with one tap"),
            ("📅 Calendar Sync", "View appointments and deadlines"),
            ("🔔 Push Notifications", "Get alerts for important events"),
            ("🔒 Biometric Security", "Fingerprint and Face ID protection"),
            ("☁️ Offline Sync", "Work offline, sync when connected")
        ]
        
        for feature, description in mobile_features:
            st.markdown(f"""
            <div style="margin: 1rem 0; padding: 1rem; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #2E86AB;">
                <strong>{feature}</strong><br>
                <small>{description}</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.subheader("📊 Mobile Analytics")
        st.metric("Daily Active Users", "156", "+12")
        st.metric("Documents Scanned", "2,341", "+89")
        st.metric("Voice Notes Created", "567", "+23")
    
    with col2:
        st.subheader("📱 Mobile App Preview")
        mobile_framework.render_mobile_interface()
        
        st.markdown("### 📲 Download Mobile App")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: #000; color: white; padding: 1rem; border-radius: 8px; text-align: center;">
                📱 iOS App Store<br>
                <small>Download for iPhone & iPad</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #34a853; color: white; padding: 1rem; border-radius: 8px; text-align: center;">
                🤖 Google Play Store<br>
                <small>Download for Android</small>
            </div>
            """, unsafe_allow_html=True)

elif page == "Business Intelligence":
    st.title("📊 Business Intelligence & Analytics")
    
    if not has_permission('admin'):
        st.error("🚫 Access denied. Business Intelligence requires admin privileges.")
        st.stop()
    
    # Generate comprehensive BI data
    exec_metrics = business_intelligence.generate_executive_dashboard()
    forecast_data = business_intelligence.generate_financial_forecast()
    productivity_data = business_intelligence.create_productivity_metrics()
    
    # Executive Summary
    st.subheader("📈 Executive Summary")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    metrics = [
        ("Revenue", f"${exec_metrics['total_revenue']:,.0f}", f"{exec_metrics['revenue_growth']:+.1f}%"),
        ("Matters", exec_metrics['active_matters'], "+2"),
        ("Utilization", f"{exec_metrics['utilization_rate']:.1f}%", "+3.2%"),
        ("Client Satisfaction", f"{exec_metrics['client_satisfaction']:.1f}/5", "+0.3"),
        ("Avg Matter Value", f"${exec_metrics['avg_matter_value']:,.0f}", "+12%"),
        ("Doc Growth", f"{exec_metrics['document_growth_rate']:.0f}%", "+5%")
    ]
    
    for col, (label, value, change) in zip([col1, col2, col3, col4, col5, col6], metrics):
        with col:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(label, value, change)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Comprehensive Analytics Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💰 Financial", "⏱️ Productivity", "👥 Client Analytics", "📊 Forecasting", "🎯 Performance"])
    
    with tab1:
        st.subheader("Financial Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(business_intelligence.create_revenue_chart(), use_container_width=True)
            
            # Revenue breakdown
            st.subheader("Revenue by Practice Area")
            practice_revenue = {
                'Corporate Law': 45000,
                'Litigation': 32000,
                'Family Law': 18000,
                'Real Estate': 15000,
                'Employment': 12000
            }
            
            fig = px.pie(values=list(practice_revenue.values()), 
                        names=list(practice_revenue.keys()),
                        title="Revenue Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Financial metrics table
            st.subheader("Financial KPIs")
            
            financial_data = pd.DataFrame({
                'Metric': ['Total Revenue', 'Total Expenses', 'Net Profit', 'Profit Margin', 'Revenue per Attorney', 'Collection Rate'],
                'Current Period': ['$125,000', '$85,000', '$40,000', '32%', '$25,000', '94%'],
                'Previous Period': ['$118,000', '$82,000', '$36,000', '30.5%', '$23,600', '91%'],
                'Change': ['+5.9%', '+3.7%', '+11.1%', '+1.5pp', '+5.9%', '+3pp']
            })
            
            st.dataframe(financial_data, hide_index=True)
            
            # Accounts receivable aging
            st.subheader("Accounts Receivable Aging")
            ar_data = pd.DataFrame({
                'Period': ['0-30 days', '31-60 days', '61-90 days', '90+ days'],
                'Amount': [25000, 8000, 3000, 1500],
                'Percentage': [67, 21, 8, 4]
            })
            
            fig = px.bar(ar_data, x='Period', y='Amount', title="Outstanding Invoices by Age")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Productivity & Efficiency Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Billable hours trend
            dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
            hours_data = np.random.normal(7.5, 1.5, 30)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=hours_data, mode='lines+markers', name='Daily Billable Hours'))
            fig.add_hline(y=7.5, line_dash="dash", annotation_text="Target: 7.5 hours")
            fig.update_layout(title="Daily Billable Hours Trend", height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Document processing metrics
            st.subheader("Document Processing Efficiency")
            proc_metrics = pd.DataFrame({
                'Document Type': ['Contracts', 'Court Filings', 'Correspondence', 'Research'],
                'Avg Processing Time (hours)': [3.2, 2.8, 0.5, 4.1],
                'Automation Potential': ['High', 'Medium', 'High', 'Low']
            })
            st.dataframe(proc_metrics, hide_index=True)
        
        with col2:
            st.plotly_chart(business_intelligence.create_workload_analysis(), use_container_width=True)
            
            # Efficiency improvements
            st.subheader("Efficiency Gains")
            efficiency_data = {
                'AI Document Review': '+35%',
                'Automated Time Tracking': '+22%',
                'Template Usage': '+18%',
                'Client Portal': '+15%'
            }
            
            for feature, improvement in efficiency_data.items():
                st.markdown(f"• **{feature}**: {improvement} time savings")
    
    with tab3:
        st.subheader("Client Analytics & Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Client satisfaction over time
            months = pd.date_range(start='2024-01-01', periods=12, freq='M')
            satisfaction_scores = [4.1, 4.0, 4.2, 4.3, 4.2, 4.4, 4.1, 4.3, 4.5, 4.2, 4.4, 4.2]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=months, y=satisfaction_scores, mode='lines+markers', name='Client Satisfaction'))
            fig.add_hline(y=4.0, line_dash="dash", annotation_text="Target: 4.0")
            fig.update_layout(title="Client Satisfaction Trend", yaxis=dict(range=[3.5, 5.0]), height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Client retention metrics
            st.subheader("Client Retention Metrics")
            retention_data = pd.DataFrame({
                'Metric': ['Client Retention Rate', 'New Client Acquisition', 'Client Lifetime Value', 'Referral Rate'],
                'Value': ['92%', '15 clients/month', '$85,000', '23%'],
                'Benchmark': ['85%', '12 clients/month', '$75,000', '20%']
            })
            st.dataframe(retention_data, hide_index=True)
        
        with col2:
            # Client segmentation
            client_segments = {
                'Enterprise': 25,
                'Mid-Market': 45,
                'Small Business': 35,
                'Individual': 60
            }
            
            fig = px.pie(values=list(client_segments.values()),
                        names=list(client_segments.keys()),
                        title="Client Segmentation")
            st.plotly_chart(fig, use_container_width=True)
            
            # Top clients by revenue
            st.subheader("Top Clients by Revenue")
            top_clients = pd.DataFrame({
                'Client': ['Acme Corporation', 'TechStart Inc', 'Global Enterprises', 'Local Business LLC', 'Individual Client A'],
                'Revenue YTD': [45000, 28000, 22000, 15000, 12000],
                'Matters': [8, 5, 6, 3, 4]
            })
            st.dataframe(top_clients, hide_index=True)
    
    with tab4:
        st.subheader("Financial Forecasting & Projections")
        
        # Revenue forecast
        forecast_months = [f['month'] for f in forecast_data['forecast']]
        forecast_values = [f['projected_revenue'] for f in forecast_data['forecast']]
        confidence_lower = [f['confidence_interval'][0] for f in forecast_data['forecast']]
        confidence_upper = [f['confidence_interval'][1] for f in forecast_data['forecast']]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=forecast_months, y=forecast_values, mode='lines+markers', name='Projected Revenue'))
        fig.add_trace(go.Scatter(x=forecast_months, y=confidence_upper, fill=None, mode='lines', line_color='rgba(0,0,0,0)', showlegend=False))
        fig.add_trace(go.Scatter(x=forecast_months, y=confidence_lower, fill='tonexty', mode='lines', line_color='rgba(0,0,0,0)', name='Confidence Interval'))
        fig.update_layout(title=f"6-Month Revenue Forecast (Growth Rate: {forecast_data['growth_rate']:.1%})", height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Forecast Assumptions")
            assumptions = [
                "8% monthly growth rate based on historical data",
                "Stable client retention at 92%",
                "New client acquisition of 15 clients/month",
                "Average matter value of $25,000",
                "Economic conditions remain stable"
            ]
            
            for assumption in assumptions:
                st.markdown(f"• {assumption}")
        
        with col2:
            st.subheader("Scenario Analysis")
            scenarios = pd.DataFrame({
                'Scenario': ['Optimistic', 'Base Case', 'Conservative'],
                '6-Month Revenue': ['$185,000', '$165,000', '$145,000'],
                'Growth Rate': ['12%', '8%', '4%'],
                'Probability': ['25%', '50%', '25%']
            })
            st.dataframe(scenarios, hide_index=True)
    
    with tab5:
        st.subheader("Performance Dashboard")
        
        # Key performance indicators
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### ⚖️ Legal Performance")
            legal_kpis = pd.DataFrame({
                'KPI': ['Case Win Rate', 'Avg Case Duration', 'Client Response Time', 'Document Turnaround'],
                'Current': ['78%', '145 days', '4.2 hours', '2.1 days'],
                'Target': ['80%', '120 days', '6 hours', '2 days'],
                'Status': ['🔴', '🔴', '🟢', '🔴']
            })
            st.dataframe(legal_kpis, hide_index=True)
        
        with col2:
            st.markdown("### 💼 Operational Performance")
            operational_kpis = pd.DataFrame({
                'KPI': ['Utilization Rate', 'Revenue per Hour', 'Collection Rate', 'Client Satisfaction'],
                'Current': ['78.5%', '$285', '94%', '4.2/5'],
                'Target': ['80%', '$300', '95%', '4.0/5'],
                'Status': ['🟡', '🔴', '🟡', '🟢']
            })
            st.dataframe(operational_kpis, hide_index=True)
        
        with col3:
            st.markdown("### 📊 Technology Performance")
            tech_kpis = pd.DataFrame({
                'KPI': ['System Uptime', 'Document Processing', 'AI Accuracy', 'Mobile Adoption'],
                'Current': ['99.8%', '94% automated', '91%', '67%'],
                'Target': ['99.9%', '95%', '90%', '70%'],
                'Status': ['🟡', '🟡', '🟢', '🟡']
            })
            st.dataframe(tech_kpis, hide_index=True)
        
        # Performance trends
        st.subheader("📈 Performance Trends")
        
        # Create performance trend chart
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        utilization = [75, 77, 74, 79, 76, 81, 78, 80, 79, 78, 82, 78.5]
        satisfaction = [4.0, 4.1, 3.9, 4.2, 4.0, 4.3, 4.1, 4.2, 4.4, 4.1, 4.3, 4.2]
        win_rate = [76, 78, 75, 80, 77, 82, 79, 81, 78, 76, 79, 78]
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=months, y=utilization, name="Utilization Rate (%)"), secondary_y=False)
        fig.add_trace(go.Scatter(x=months, y=win_rate, name="Win Rate (%)"), secondary_y=False)
        fig.add_trace(go.Scatter(x=months, y=[s*20 for s in satisfaction], name="Client Satisfaction (x20)"), secondary_y=True)
        
        fig.update_xaxes(title_text="Month")
        fig.update_yaxes(title_text="Percentage", secondary_y=False)
        fig.update_yaxes(title_text="Satisfaction Score (x20)", secondary_y=True)
        fig.update_layout(title="Key Performance Trends", height=400)
        
        st.plotly_chart(fig, use_container_width=True)

elif page == "Time & Billing":
    st.title("⏱️ Advanced Time Tracking & Billing")
    
    if not has_permission('time_tracking'):
        st.error("🚫 Access denied. Time tracking access required.")
        st.stop()
    
    # Billing overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_unbilled_hours = sum(entry.hours for entry in st.session_state.time_entries if entry.status in ['draft', 'submitted'])
    total_unbilled_amount = sum(entry.hours * entry.billing_rate for entry in st.session_state.time_entries if entry.status in ['draft', 'submitted'])
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Unbilled Hours", f"{total_unbilled_hours:.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Unbilled Amount", f"${total_unbilled_amount:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Outstanding Invoices", len([inv for inv in st.session_state.invoices if inv.status in ['sent', 'overdue']]))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Collection Rate", "94.2%", "+2.1%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Time tracking and billing tabs
    tab1, tab2, tab3, tab4 = st.tabs(["⏱️ Time Entry", "📊 Time Analysis", "💰 Billing", "📈 Reports"])
    
    with tab1:
        st.subheader("Time Entry Management")
        
        # Quick time entry form
        with st.form("quick_time_entry"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                entry_matter = st.selectbox("Matter", [f"{m.name} - {m.client_name}" for m in st.session_state.matters])
                entry_hours = st.number_input("Hours", min_value=0.0, max_value=24.0, value=1.0, step=0.25)
            
            with col2:
                entry_date = st.date_input("Date", value=datetime.now().date())
                entry_rate = st.number_input("Rate ($)", min_value=0.0, value=250.0, step=25.0)
            
            with col3:
                entry_activity = st.selectbox("Activity Type", ["Legal Research", "Document Review", "Client Meeting", "Court Appearance", "Administrative"])
                billable = st.checkbox("Billable", value=True)
            
            entry_description = st.text_area("Description", placeholder="Describe the work performed...")
            
            if st.form_submit_button("Add Time Entry"):
                if entry_matter and entry_description:
                    matter_id = st.session_state.matters[[f"{m.name} - {m.client_name}" for m in st.session_state.matters].index(entry_matter)].id
                    
                    new_entry = TimeEntry(
                        id=str(uuid.uuid4()),
                        user_id=st.session_state['user']['email'],
                        matter_id=matter_id,
                        client_id="demo_client",  # Simplified for demo
                        date=datetime.combine(entry_date, datetime.now().time()),
                        hours=entry_hours,
                        description=entry_description,
                        billing_rate=entry_rate,
                        billable=billable,
                        activity_type=entry_activity,
                        status=BillingStatus.DRAFT.value,
                        created_date=datetime.now()
                    )
                    
                    st.session_state.time_entries.append(new_entry)
                    st.success("Time entry added successfully!")
                    st.rerun()
        
        st.divider()
        
        # Recent time entries
        st.subheader("Recent Time Entries")
        
        recent_entries = sorted(st.session_state.time_entries, key=lambda x: x.created_date, reverse=True)[:10]
        
        for entry in recent_entries:
            matter_name = next((m.name for m in st.session_state.matters if m.id == entry.matter_id), "Unknown Matter")
            status_color = {"draft": "#6c757d", "submitted": "#ffc107", "approved": "#28a745", "billed": "#17a2b8"}
            
            st.markdown(f"""
            <div class="document-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{matter_name}</strong> - {entry.hours} hours<br>
                        <small>{entry.description[:100]}...</small><br>
                        <small>Rate: ${entry.billing_rate}/hr | Amount: ${entry.hours * entry.billing_rate:.2f}</small>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: {status_color.get(entry.status, '#6c757d')}; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">
                            {entry.status.upper()}
                        </span><br>
                        <small>{entry.date.strftime('%Y-%m-%d')}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Time Analysis & Utilization")
        
        # Time analysis charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Daily hours trend
            if st.session_state.time_entries:
                daily_hours = {}
                for entry in st.session_state.time_entries:
                    date_str = entry.date.strftime('%Y-%m-%d')
                    daily_hours[date_str] = daily_hours.get(date_str, 0) + entry.hours
                
                if daily_hours:
                    dates = list(daily_hours.keys())
                    hours = list(daily_hours.values())
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=dates, y=hours, mode='lines+markers', name='Daily Hours'))
                    fig.add_hline(y=7.5, line_dash="dash", annotation_text="Target: 7.5 hours")
                    fig.update_layout(title="Daily Hours Trend", height=400)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No time entries available for analysis")
        
        with col2:
            # Hours by activity type
            activity_hours = {}
            for entry in st.session_state.time_entries:
                activity_hours[entry.activity_type] = activity_hours.get(entry.activity_type, 0) + entry.hours
            
            if activity_hours:
                fig = px.pie(values=list(activity_hours.values()),
                           names=list(activity_hours.keys()),
                           title="Hours by Activity Type")
                st.plotly_chart(fig, use_container_width=True)
        
        # Utilization metrics
        st.subheader("Utilization Metrics")
        
        utilization_data = pd.DataFrame({
            'Attorney': ['John Partner', 'Jane Associate', 'Bob Paralegal'],
            'Billable Hours': [165, 158, 142],
            'Non-Billable Hours': [15, 22, 18],
            'Total Hours': [180, 180, 160],
            'Utilization Rate': ['91.7%', '87.8%', '88.8%']
        })
        
        st.dataframe(utilization_data, hide_index=True)
    
    with tab3:
        st.subheader("Billing Management")
        
        # Invoice generation
        st.markdown("### 📄 Generate New Invoice")
        
        with st.form("generate_invoice"):
            col1, col2 = st.columns(2)
            
            with col1:
                invoice_client = st.selectbox("Client", [f"{c.name}" for c in st.session_state.clients])
                billing_period_start = st.date_input("Billing Period Start", value=datetime.now().replace(day=1).date())
            
            with col2:
                invoice_matter = st.selectbox("Matter", [f"{m.name}" for m in st.session_state.matters])
                billing_period_end = st.date_input("Billing Period End", value=datetime.now().date())
            
            if st.form_submit_button("Generate Invoice"):
                client_id = next(c.id for c in st.session_state.clients if c.name == invoice_client)
                matter_id = next(m.id for m in st.session_state.matters if m.name == invoice_matter)
                
                new_invoice = billing_system.generate_invoice(
                    client_id, matter_id, 
                    datetime.combine(billing_period_start, datetime.min.time()),
                    datetime.combine(billing_period_end, datetime.max.time())
                )
                
                st.session_state.invoices.append(new_invoice)
                st.success(f"Invoice {new_invoice.invoice_number} generated successfully!")
                st.rerun()
        
        st.divider()
        
        # Invoice list
        st.subheader("📋 Invoice Management")
        
        for invoice in st.session_state.invoices:
            client_name = next((c.name for c in st.session_state.clients if c.id == invoice.client_id), "Unknown Client")
            matter_name = next((m.name for m in st.session_state.matters if m.id == invoice.matter_id), "Unknown Matter")
            
            status_colors = {
                'draft': '#6c757d',
                'sent': '#ffc107', 
                'paid': '#28a745',
                'overdue': '#dc3545'
            }
            
            st.markdown(f"""
            <div class="document-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>Invoice {invoice.invoice_number}</strong><br>
                        <small>Client: {client_name} | Matter: {matter_name}</small><br>
                        <small>Issued: {invoice.date_issued.strftime('%Y-%m-%d')} | Due: {invoice.due_date.strftime('%Y-%m-%d')}</small>
                    </div>
                    <div style="text-align: right;">
                        <strong>${invoice.total_amount:,.2f}</strong><br>
                        <span style="background: {status_colors.get(invoice.status, '#6c757d')}; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">
                            {invoice.status.upper()}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.subheader("Billing Reports & Analytics")
        
        # Billing summary charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly billing
            monthly_billing = {
                'Jan': 15000, 'Feb': 18000, 'Mar': 22000, 'Apr': 19000,
                'May': 25000, 'Jun': 28000, 'Jul': 24000, 'Aug': 30000,
                'Sep': 27000, 'Oct': 32000, 'Nov': 29000, 'Dec': 35000
            }
            
            fig = px.bar(x=list(monthly_billing.keys()), y=list(monthly_billing.values()),
                        title="Monthly Billing Revenue")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Collections analysis
            collections_data = {
                'Billed': 125000,
                'Collected': 118000,
                'Outstanding': 7000
            }

# Configure page with enhanced settings
st.set_page_config(
    page_title="LegalDoc Pro - Complete Enterprise Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for professional legal theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #2E86AB;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .alert-box {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid;
        backdrop-filter: blur(10px);
    }
    
    .alert-success {
        background: linear-gradient(135deg, #d1e7dd 0%, #badbcc 100%);
        border-color: #198754;
        color: #0a3622;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-color: #ffc107;
        color: #856404;
    }
    
    .alert-danger {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-color: #dc3545;
        color: #58151c;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #cff4fc 0%, #b6effb 100%);
        border-color: #0dcaf0;
        color: #055160;
    }
    
    .document-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border-left: 4px solid #2E86AB;
        transition: all 0.3s ease;
    }
    
    .document-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .matter-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #dee2e6;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .matter-card:hover {
        border-color: #2E86AB;
        transform: translateY(-2px);
    }
    
    .status-badge {
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-active { background-color: #28a745; color: white; }
    .status-pending { background-color: #ffc107; color: #212529; }
    .status-draft { background-color: #6c757d; color: white; }
    .status-review { background-color: #17a2b8; color: white; }
    .status-final { background-color: #28a745; color: white; }
    .status-archived { background-color: #6c757d; color: white; }
    
    .priority-high { color: #dc3545; font-weight: 600; }
    .priority-medium { color: #ffc107; font-weight: 600; }
    .priority-low { color: #28a745; font-weight: 600; }
    
    .ai-insight {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 1px solid #2196f3;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .client-portal {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        border: 1px solid #9c27b0;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .mobile-frame {
        width: 300px;
        height: 600px;
        background: #000;
        border-radius: 25px;
        padding: 20px;
        margin: 0 auto;
        position: relative;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .mobile-screen {
        width: 100%;
        height: 100%;
        background: white;
        border-radius: 20px;
        overflow: hidden;
        position: relative;
    }
    
    .integration-card {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .integration-card:hover {
        border-color: #2E86AB;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin: 1rem 0;
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    
    .stProgress .st-bo {
        background-color: #2E86AB;
    }
    
    .calendar-widget {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Data Classes
@dataclass
class User:
    id: str
    email: str
    role: str
    permissions: List[str]
    created_date: datetime
    last_login: datetime
    profile_settings: Dict
    notification_preferences: Dict
    billing_info: Dict

@dataclass
class Client:
    id: str
    name: str
    client_type: str  # 'individual', 'business', 'organization'
    contact_info: Dict
    billing_address: Dict
    primary_contact: str
    created_date: datetime
    status: str  # 'active', 'inactive', 'prospective'
    portal_access: bool
    portal_credentials: Dict
    billing_preferences: Dict
    communication_preferences: Dict

@dataclass
class Matter:
    id: str
    name: str
    client_id: str
    client_name: str
    matter_type: str
    status: str
    created_date: datetime
    assigned_attorneys: List[str]
    description: str
    budget: float
    estimated_hours: float
    actual_hours: float
    important_dates: Dict[str, datetime]
    billing_rate: float
    priority: str  # 'high', 'medium', 'low'
    court_info: Dict
    opposing_parties: List[Dict]
    statute_of_limitations: Optional[datetime]
    custom_fields: Dict

@dataclass
class EmailMessage:
    id: str
    subject: str
    sender: str
    recipients: List[str]
    body: str
    attachments: List[str]
    timestamp: datetime
    matter_id: Optional[str]
    client_id: Optional[str]
    message_type: str  # 'received', 'sent'
    priority: str
    is_privileged: bool

@dataclass
class CalendarEvent:
    id: str
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    event_type: str  # 'court_date', 'meeting', 'deadline', 'reminder'
    matter_id: Optional[str]
    client_id: Optional[str]
    location: str
    attendees: List[str]
    reminders: List[Dict]
    recurring: bool
    status: str

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
    status: str  # 'draft', 'submitted', 'approved', 'billed'
    created_date: datetime

@dataclass
class Invoice:
    id: str
    client_id: str
    matter_id: str
    invoice_number: str
    date_issued: datetime
    due_date: datetime
    line_items: List[Dict]
    subtotal: float
    tax_rate: float
    tax_amount: float
    total_amount: float
    status: str  # 'draft', 'sent', 'paid', 'overdue'
    payment_terms: str
    notes: str

@dataclass
class AIInsight:
    id: str
    document_id: str
    insight_type: str  # 'risk_analysis', 'clause_detection', 'deadline_extraction', 'similar_docs'
    content: Dict
    confidence_score: float
    created_date: datetime
    reviewed: bool
    action_required: bool

@dataclass
class Integration:
    id: str
    name: str
    type: str  # 'email', 'calendar', 'court_filing', 'esignature', 'accounting'
    status: str  # 'active', 'inactive', 'error'
    settings: Dict
    last_sync: datetime
    sync_frequency: str
    error_log: List[Dict]

# Enhanced Enums
class NotificationType(Enum):
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"
    PUSH = "push"

class DocumentRiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class BillingStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    BILLED = "billed"
    PAID = "paid"

# Initialize Enhanced Session State
def initialize_enhanced_session_state():
    """Initialize all session state variables for the enhanced system"""
    default_states = {
        'enhanced_documents': [],
        'matters': [],
        'clients': [],
        'users': [],
        'time_entries': [],
        'invoices': [],
        'email_messages': [],
        'calendar_events': [],
        'ai_insights': [],
        'integrations': [],
        'notifications': [],
        'user': None,
        'audit_log': [],
        'search_index': {},
        'dashboard_data': {},
        'mobile_session': {},
        'client_portal_sessions': {},
        'system_settings': {},
        'billing_summary': {},
        'analytics_cache': {}
    }
    
    for key, default_value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# Advanced Email Integration System
class EmailIntegration:
    def __init__(self, email_config: Dict):
        self.smtp_server = email_config.get('smtp_server')
        self.smtp_port = email_config.get('smtp_port', 587)
        self.imap_server = email_config.get('imap_server')
        self.imap_port = email_config.get('imap_port', 993)
        self.username = email_config.get('username')
        self.password = email_config.get('password')
    
    def connect_imap(self):
        """Connect to IMAP server for reading emails"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.username, self.password)
            return mail
        except Exception as e:
            st.error(f"Failed to connect to email server: {str(e)}")
            return None
    
    def fetch_emails(self, folder='INBOX', limit=50) -> List[EmailMessage]:
        """Fetch emails from specified folder"""
        mail = self.connect_imap()
        if not mail:
            return []
        
        try:
            mail.select(folder)
            _, message_ids = mail.search(None, 'ALL')
            
            emails = []
            for msg_id in message_ids[0].split()[-limit:]:  # Get latest emails
                _, msg_data = mail.fetch(msg_id, '(RFC822)')
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)
                
                # Extract email details
                email_obj = EmailMessage(
                    id=str(uuid.uuid4()),
                    subject=email_message.get('Subject', 'No Subject'),
                    sender=email_message.get('From', ''),
                    recipients=email_message.get('To', '').split(','),
                    body=self._extract_email_body(email_message),
                    attachments=self._extract_attachments(email_message),
                    timestamp=datetime.now(),
                    matter_id=None,
                    client_id=None,
                    message_type='received',
                    priority='normal',
                    is_privileged=False
                )
                emails.append(email_obj)
            
            mail.logout()
            return emails
            
        except Exception as e:
            st.error(f"Error fetching emails: {str(e)}")
            return []
    
    def send_email(self, to_addresses: List[str], subject: str, body: str, attachments: List = None):
        """Send email with optional attachments"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = ', '.join(to_addresses)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.username, to_addresses, text)
            server.quit()
            
            return True
            
        except Exception as e:
            st.error(f"Error sending email: {str(e)}")
            return False
    
    def _extract_email_body(self, email_message):
        """Extract plain text body from email"""
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()
        return body
    
    def _extract_attachments(self, email_message):
        """Extract attachment filenames from email"""
        attachments = []
        for part in email_message.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                if filename:
                    attachments.append(filename)
        return attachments
    
    def auto_assign_to_matter(self, email_obj: EmailMessage) -> Optional[str]:
        """Automatically assign email to matter based on content analysis"""
        # Simple keyword matching - can be enhanced with ML
        email_content = f"{email_obj.subject} {email_obj.body}".lower()
        
        for matter in st.session_state.matters:
            matter_keywords = [
                matter.name.lower(),
                matter.client_name.lower(),
                matter.matter_type.lower()
            ]
            
            if any(keyword in email_content for keyword in matter_keywords):
                return matter.id
        
        return None

# Advanced Calendar Integration
class CalendarIntegration:
    def __init__(self):
        self.events = []
    
    def create_event(self, title: str, description: str, start_time: datetime, 
                    end_time: datetime, event_type: str, matter_id: str = None) -> CalendarEvent:
        """Create a new calendar event"""
        event = CalendarEvent(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            event_type=event_type,
            matter_id=matter_id,
            client_id=None,
            location="",
            attendees=[],
            reminders=[],
            recurring=False,
            status="confirmed"
        )
        return event
    
    def get_upcoming_events(self, days_ahead: int = 30) -> List[CalendarEvent]:
        """Get upcoming events within specified days"""
        cutoff_date = datetime.now() + timedelta(days=days_ahead)
        upcoming = [event for event in st.session_state.calendar_events 
                   if event.start_time <= cutoff_date and event.start_time >= datetime.now()]
        return sorted(upcoming, key=lambda x: x.start_time)
    
    def get_court_dates(self) -> List[CalendarEvent]:
        """Get all court dates"""
        return [event for event in st.session_state.calendar_events 
                if event.event_type == 'court_date']
    
    def get_deadlines(self) -> List[CalendarEvent]:
        """Get all deadlines"""
        return [event for event in st.session_state.calendar_events 
                if event.event_type == 'deadline']
    
    def create_deadline_from_document(self, document, deadline_date: datetime):
        """Create deadline event from document analysis"""
        event = self.create_event(
            title=f"Deadline: {document.name}",
            description=f"Document deadline for {document.name}",
            start_time=deadline_date,
            end_time=deadline_date + timedelta(hours=1),
            event_type="deadline",
            matter_id=document.matter_id
        )
        st.session_state.calendar_events.append(event)
        return event

# Advanced Billing System
class BillingSystem:
    def __init__(self):
        self.default_rates = {
            'partner': 500.0,
            'senior_associate': 350.0,
            'associate': 250.0,
            'paralegal': 150.0
        }
    
    def create_time_entry(self, user_id: str, matter_id: str, hours: float, 
                         description: str, activity_type: str = "legal_work") -> TimeEntry:
        """Create a new time entry"""
        user_role = self._get_user_role(user_id)
        billing_rate = self.default_rates.get(user_role, 250.0)
        
        entry = TimeEntry(
            id=str(uuid.uuid4()),
            user_id=user_id,
            matter_id=matter_id,
            client_id=self._get_matter_client_id(matter_id),
            date=datetime.now(),
            hours=hours,
            description=description,
            billing_rate=billing_rate,
            billable=True,
            activity_type=activity_type,
            status=BillingStatus.DRAFT.value,
            created_date=datetime.now()
        )
        return entry
    
    def generate_invoice(self, client_id: str, matter_id: str, 
                        billing_period_start: datetime, billing_period_end: datetime) -> Invoice:
        """Generate invoice for specified period"""
        # Get time entries for the period
        time_entries = [
            entry for entry in st.session_state.time_entries
            if (entry.client_id == client_id and 
                entry.matter_id == matter_id and
                billing_period_start <= entry.date <= billing_period_end and
                entry.billable and entry.status == BillingStatus.APPROVED.value)
        ]
        
        # Calculate line items
        line_items = []
        subtotal = 0.0
        
        for entry in time_entries:
            line_item = {
                'date': entry.date,
                'description': entry.description,
                'hours': entry.hours,
                'rate': entry.billing_rate,
                'amount': entry.hours * entry.billing_rate,
                'attorney': entry.user_id
            }
            line_items.append(line_item)
            subtotal += line_item['amount']
        
        # Calculate tax
        tax_rate = 0.08  # 8% tax rate
        tax_amount = subtotal * tax_rate
        total_amount = subtotal + tax_amount
        
        invoice = Invoice(
            id=str(uuid.uuid4()),
            client_id=client_id,
            matter_id=matter_id,
            invoice_number=f"INV-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.invoices) + 1:04d}",
            date_issued=datetime.now(),
            due_date=datetime.now() + timedelta(days=30),
            line_items=line_items,
            subtotal=subtotal,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            total_amount=total_amount,
            status="draft",
            payment_terms="Net 30",
            notes=""
        )
        
        return invoice
    
    def _get_user_role(self, user_id: str) -> str:
        """Get user role for billing rate"""
        return "associate"  # Simplified for demo
    
    def _get_matter_client_id(self, matter_id: str) -> str:
        """Get client ID from matter ID"""
        matter = next((m for m in st.session_state.matters if m.id == matter_id), None)
        return matter.client_id if matter else ""

# Advanced AI Analysis System
class AIAnalysisSystem:
    def __init__(self):
        # Initialize AI models (in production, you'd load actual models)
        self.contract_analyzer = None
        self.risk_analyzer = None
        self.entity_extractor = None
    
    def analyze_contract(self, document_text: str) -> Dict:
        """Analyze contract for risks, clauses, and recommendations"""
        analysis = {
            'risk_level': self._assess_risk_level(document_text),
            'key_clauses': self._identify_key_clauses(document_text),
            'missing_clauses': self._identify_missing_clauses(document_text),
            'recommendations': self._generate_recommendations(document_text),
            'entities': self._extract_entities(document_text),
            'sentiment': self._analyze_sentiment(document_text),
            'complexity_score': self._calculate_complexity(document_text),
            'similar_documents': self._find_similar_documents(document_text)
        }
        return analysis
    
    def extract_deadlines(self, document_text: str) -> List[Dict]:
        """Extract potential deadlines from document text"""
        deadline_patterns = [
            r'(?:due|deadline|must be completed by|no later than)\s+(?:on\s+)?([A-Za-z]+ \d{1,2},? \d{4})',
            r'(?:within|in)\s+(\d+)\s+(days?|weeks?|months?)',
            r'(?:before|by)\s+([A-Za-z]+ \d{1,2},? \d{4})',
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
        ]
        
        deadlines = []
        for pattern in deadline_patterns:
            matches = re.findall(pattern, document_text, re.IGNORECASE)
            for match in matches:
                deadline = {
                    'text': match if isinstance(match, str) else ' '.join(match),
                    'confidence': 0.8,
                    'type': 'deadline',
                    'extracted_date': self._parse_date(match if isinstance(match, str) else match[0])
                }
                deadlines.append(deadline)
        
        return deadlines[:10]  # Return top 10 deadlines
    
    def analyze_document_relationships(self, documents: List) -> Dict:
        """Analyze relationships between documents"""
        relationships = {
            'document_clusters': self._cluster_documents(documents),
            'citation_network': self._build_citation_network(documents),
            'temporal_relationships': self._analyze_temporal_patterns(documents),
            'topic_evolution': self._track_topic_evolution(documents)
        }
        return relationships
    
    def predict_case_outcomes(self, matter_data: Dict) -> Dict:
        """Predict case outcomes based on historical data"""
        prediction = {
            'success_probability': 0.75,  # Placeholder
            'estimated_duration': 180,  # days
            'cost_estimate': 25000.0,
            'risk_factors': [
                'Complex contract terms',
                'Multiple parties involved',
                'Jurisdiction challenges'
            ],
            'recommendations': [
                'Consider early settlement',
                'Strengthen evidence gathering',
                'Engage subject matter expert'
            ]
        }
        return prediction
    
    def _assess_risk_level(self, text: str) -> str:
        """Assess risk level of document"""
        risk_keywords = {
            'high': ['penalty', 'termination', 'breach', 'litigation', 'damages'],
            'medium': ['condition', 'requirement', 'obligation', 'restriction'],
            'low': ['standard', 'routine', 'normal', 'typical']
        }
        
        text_lower = text.lower()
        high_count = sum(1 for word in risk_keywords['high'] if word in text_lower)
        medium_count = sum(1 for word in risk_keywords['medium'] if word in text_lower)
        
        if high_count >= 3:
            return DocumentRiskLevel.HIGH.value
        elif high_count >= 1 or medium_count >= 5:
            return DocumentRiskLevel.MEDIUM.value
        else:
            return DocumentRiskLevel.LOW.value
    
    def _identify_key_clauses(self, text: str) -> List[Dict]:
        """Identify important clauses in the document"""
        clause_patterns = {
            'termination': r'(?:termination|terminate|end|cancel)[^.]*\.',
            'payment': r'(?:payment|pay|fee|cost|price)[^.]*\.',
            'liability': r'(?:liability|liable|responsible)[^.]*\.',
            'confidentiality': r'(?:confidential|non-disclosure|proprietary)[^.]*\.',
            'intellectual_property': r'(?:intellectual property|copyright|trademark|patent)[^.]*\.'
        }
        
        clauses = []
        for clause_type, pattern in clause_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches[:3]:  # Limit to 3 per type
                clauses.append({
                    'type': clause_type,
                    'text': match.strip(),
                    'importance': 'high' if clause_type in ['termination', 'liability'] else 'medium'
                })
        
        return clauses
    
    def _identify_missing_clauses(self, text: str) -> List[str]:
        """Identify potentially missing important clauses"""
        standard_clauses = [
            'Force Majeure', 'Governing Law', 'Dispute Resolution',
            'Indemnification', 'Limitation of Liability', 'Confidentiality'
        ]
        
        text_lower = text.lower()
        missing = []
        
        for clause in standard_clauses:
            if clause.lower().replace(' ', '') not in text_lower.replace(' ', ''):
                missing.append(clause)
        
        return missing
    
    def _generate_recommendations(self, text: str) -> List[str]:
        """Generate recommendations based on document analysis"""
        recommendations = [
            "Consider adding explicit termination procedures",
            "Review payment terms for clarity",
            "Add force majeure clause for risk mitigation",
            "Include dispute resolution mechanism",
            "Strengthen intellectual property protections"
        ]
        return recommendations[:3]  # Return top 3
    
    def _extract_entities(self, text: str) -> Dict:
        """Extract named entities from text"""
        # Simplified entity extraction
        entities = {
            'organizations': re.findall(r'\b[A-Z][a-z]+ (?:Inc|LLC|Corp|Corporation|Company)\b', text),
            'people': re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text),
            'locations': re.findall(r'\b[A-Z][a-z]+(?:, [A-Z]{2})?\b', text),
            'dates': re.findall(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b', text)
        }
        return entities
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of document text"""
        # Simplified sentiment analysis
        positive_words = ['agree', 'benefit', 'advantage', 'positive', 'favorable']
        negative_words = ['dispute', 'breach', 'penalty', 'terminate', 'violation']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            sentiment = 'positive'
        elif neg_count > pos_count:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'confidence': 0.8,
            'positive_score': pos_count,
            'negative_score': neg_count
        }
    
    def _calculate_complexity(self, text: str) -> float:
        """Calculate document complexity score"""
        words = text.split()
        sentences = text.split('.')
        
        avg_words_per_sentence = len(words) / len(sentences) if sentences else 0
        long_words = sum(1 for word in words if len(word) > 6)
        complexity = (avg_words_per_sentence * 0.4) + (long_words / len(words) * 100 * 0.6)
        
        return min(complexity, 100.0)  # Cap at 100
    
    def _find_similar_documents(self, text: str) -> List[Dict]:
        """Find similar documents in the system"""
        similar = [
            {'name': 'Similar Contract A', 'similarity': 0.85, 'id': 'doc1'},
            {'name': 'Related Agreement B', 'similarity': 0.72, 'id': 'doc2'},
            {'name': 'Comparable Document C', 'similarity': 0.68, 'id': 'doc3'}
        ]
        return similar
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime object"""
        try:
            # Simple date parsing - enhance with more sophisticated parsing
            return datetime.strptime(date_str, '%B %d, %Y')
        except:
            return None
    
    def _cluster_documents(self, documents: List) -> List[Dict]:
        """Cluster documents by similarity"""
        clusters = [
            {'cluster_id': 1, 'documents': ['doc1', 'doc2'], 'theme': 'Employment Contracts'},
            {'cluster_id': 2, 'documents': ['doc3', 'doc4'], 'theme': 'Real Estate Agreements'}
        ]
        return clusters
    
    def _build_citation_network(self, documents: List) -> Dict:
        """Build citation network between documents"""
        network = {
            'nodes': [{'id': 'doc1', 'type': 'contract'}, {'id': 'doc2', 'type': 'amendment'}],
            'edges': [{'source': 'doc1', 'target': 'doc2', 'relationship': 'references'}]
        }
        return network
    
    def _analyze_temporal_patterns(self, documents: List) -> Dict:
        """Analyze temporal patterns in documents"""
        return {
            'creation_trends': {'monthly_growth': 0.15},
            'seasonal_patterns': {'peak_months': ['March', 'September']},
            'document_lifecycle': {'avg_duration': 45}
        }
    
    def _track_topic_evolution(self, documents: List) -> Dict:
        """Track how topics evolve over time"""
        return {
            'trending_topics': ['Remote Work', 'Data Privacy', 'AI Governance'],
            'declining_topics': ['Traditional Contracts', 'Paper Filing'],
            'emerging_topics': ['Blockchain Agreements', 'NFT Licensing']
        }

# Client Portal System
class ClientPortal:
    def __init__(self):
        self.active_sessions = {}
    
    def create_client_account(self, client_id: str, email: str, temp_password: str) -> Dict:
        """Create client portal account"""
        credentials = {
            'email': email,
            'password': hashlib.sha256(temp_password.encode()).hexdigest(),
            'temp_password': True,
            'last_login': None,
            'permissions': ['view_documents', 'view_billing', 'send_messages']
        }
        
        return credentials
    
    def authenticate_client(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate client for portal access"""
        # Simplified authentication
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        for client in st.session_state.clients:
            if (hasattr(client, 'portal_credentials') and 
                client.portal_credentials.get('email') == email and
                client.portal_credentials.get('password') == hashed_password):
                
                session_token = str(uuid.uuid4())
                self.active_sessions[session_token] = {
                    'client_id': client.id,
                    'email': email,
                    'login_time': datetime.now()
                }
                return {'token': session_token, 'client': client}
        
        return None
    
    def get_client_documents(self, client_id: str) -> List:
        """Get documents accessible to client"""
        client_docs = []
        for doc in st.session_state.enhanced_documents:
            if (hasattr(doc, 'client_id') and doc.client_id == client_id or
                hasattr(doc, 'client_name') and any(client.id == client_id and client.name == doc.client_name 
                                                   for client in st.session_state.clients)):
                # Only include non-privileged documents or those specifically shared
                if not getattr(doc, 'is_privileged', True) or getattr(doc, 'shared_with_client', False):
                    client_docs.append(doc)
        
        return client_docs
    
    def get_client_billing_summary(self, client_id: str) -> Dict:
        """Get billing summary for client"""
        client_invoices = [inv for inv in st.session_state.invoices if inv.client_id == client_id]
        
        total_billed = sum(inv.total_amount for inv in client_invoices)
        total_paid = sum(inv.total_amount for inv in client_invoices if inv.status == 'paid')
        outstanding = total_billed - total_paid
        
        return {
            'total_billed': total_billed,
            'total_paid': total_paid,
            'outstanding_balance': outstanding,
            'recent_invoices': sorted(client_invoices, key=lambda x: x.date_issued, reverse=True)[:5]
        }

# Third-Party Integration Manager
class IntegrationManager:
    def __init__(self):
        self.available_integrations = {
            'docusign': {'name': 'DocuSign', 'type': 'esignature', 'status': 'available'},
            'outlook': {'name': 'Microsoft Outlook', 'type': 'email', 'status': 'available'},
            'google_calendar': {'name': 'Google Calendar', 'type': 'calendar', 'status': 'available'},
            'quickbooks': {'name': 'QuickBooks', 'type': 'accounting', 'status': 'available'},
            'court_filing': {'name': 'Court E-Filing', 'type': 'court', 'status': 'available'},
            'lexisnexis': {'name': 'LexisNexis', 'type': 'research', 'status': 'available'},
            'zoom': {'name': 'Zoom', 'type': 'video_conference', 'status': 'available'},
            'slack': {'name': 'Slack', 'type': 'communication', 'status': 'available'}
        }
    
    def setup_integration(self, integration_id: str, config: Dict) -> bool:
        """Setup a third-party integration"""
        if integration_id not in self.available_integrations:
            return False
        
        integration = Integration(
            id=str(uuid.uuid4()),
            name=self.available_integrations[integration_id]['name'],
            type=self.available_integrations[integration_id]['type'],
            status='active',
            settings=config,
            last_sync=datetime.now(),
            sync_frequency='hourly',
            error_log=[]
        )
        
        st.session_state.integrations.append(integration)
        return True
    
    def sync_integration(self, integration_id: str) -> bool:
        """Sync data with third-party integration"""
        # Placeholder for actual sync logic
        integration = next((i for i in st.session_state.integrations if i.id == integration_id), None)
        if integration:
            integration.last_sync = datetime.now()
            return True
        return False
    
    def send_for_esignature(self, document_id: str, signers: List[Dict]) -> Dict:
        """Send document for electronic signature"""
        # Placeholder for DocuSign integration
        envelope_id = str(uuid.uuid4())
        
        return {
            'envelope_id': envelope_id,
            'status': 'sent',
            'signing_url': f"https://demo.docusign.net/signing/{envelope_id}",
            'expected_completion': datetime.now() + timedelta(days=7)
        }
    
    def file_court_document(self, document_id: str, court_info: Dict) -> Dict:
        """File document with court system"""
        # Placeholder for court e-filing integration
        filing_id = str(uuid.uuid4())
        
        return {
            'filing_id': filing_id,
            'status': 'submitted',
            'confirmation_number': f"CF-{datetime.now().strftime('%Y%m%d')}-{filing_id[:8]}",
            'filing_date': datetime.now()
        }

# Mobile App Framework
class MobileAppFramework:
    def __init__(self):
        self.mobile_features = {
            'document_viewer': True,
            'photo_scanner': True,
            'voice_notes': True,
            'offline_sync': True,
            'push_notifications': True,
            'biometric_auth': True
        }
    
    def render_mobile_interface(self):
        """Render mobile app simulation"""
        st.markdown("""
        <div class="mobile-frame">
            <div class="mobile-screen">
                <div style="background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%); color: white; padding: 1rem; text-align: center;">
                    <h3>📱 LegalDoc Mobile</h3>
                </div>
                <div style="padding: 1rem;">
                    <div style="margin: 0.5rem 0; padding: 0.8rem; background: #f8f9fa; border-radius: 8px;">
                        📄 Recent Documents (3)
                    </div>
                    <div style="margin: 0.5rem 0; padding: 0.8rem; background: #f8f9fa; border-radius: 8px;">
                        📅 Today's Schedule (2)
                    </div>
                    <div style="margin: 0.5rem 0; padding: 0.8rem; background: #f8f9fa; border-radius: 8px;">
                        📧 New Messages (5)
                    </div>
                    <div style="margin: 0.5rem 0; padding: 0.8rem; background: #f8f9fa; border-radius: 8px;">
                        ⏱️ Time Tracking
                    </div>
                    <div style="margin: 0.5rem 0; padding: 0.8rem; background: #f8f9fa; border-radius: 8px;">
                        📸 Scan Document
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def generate_mobile_qr_code(self) -> str:
        """Generate QR code for mobile app download"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data("https://legaldocpro.com/mobile-app")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        return img

# Business Intelligence & Analytics
class BusinessIntelligence:
    def __init__(self):
        self.metrics = {}
    
    def generate_executive_dashboard(self) -> Dict:
        """Generate executive dashboard metrics"""
        # Calculate key metrics
        total_matters = len(st.session_state.matters)
        active_matters = len([m for m in st.session_state.matters if m.status == 'active'])
        total_docs = len(st.session_state.enhanced_documents)
        total_revenue = sum(inv.total_amount for inv in st.session_state.invoices if inv.status == 'paid')
        
        # Time-based analytics
        current_month_revenue = sum(
            inv.total_amount for inv in st.session_state.invoices 
            if inv.date_issued.month == datetime.now().month and inv.status == 'paid'
        )
        
        last_month_revenue = sum(
            inv.total_amount for inv in st.session_state.invoices 
            if inv.date_issued.month == datetime.now().month - 1 and inv.status == 'paid'
        )
        
        revenue_growth = ((current_month_revenue - last_month_revenue) / last_month_revenue * 100) if last_month_revenue > 0 else 0
        
        return {
            'total_matters': total_matters,
            'active_matters': active_matters,
            'total_documents': total_docs,
            'total_revenue': total_revenue,
            'monthly_revenue': current_month_revenue,
            'revenue_growth': revenue_growth,
            'avg_matter_value': total_revenue / total_matters if total_matters > 0 else 0,
            'document_growth_rate': 15,  # Placeholder
            'client_satisfaction': 4.2,  # Placeholder
            'utilization_rate': 78.5  # Placeholder
        }
    
    def create_revenue_chart(self) -> go.Figure:
        """Create revenue trend chart"""
        # Generate sample data for demonstration
        months = pd.date_range(start='2024-01-01', periods=12, freq='M')
        revenue_data = [15000, 18000, 22000, 19000, 25000, 28000, 24000, 30000, 27000, 32000, 29000, 35000]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=revenue_data,
            mode='lines+markers',
            name='Monthly Revenue',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Monthly Revenue Trend',
            xaxis_title='Month',
            yaxis_title='Revenue ($)',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def create_matter_type_distribution(self) -> go.Figure:
        """Create matter type distribution chart"""
        matter_types = {}
        for matter in st.session_state.matters:
            matter_type = matter.matter_type.replace('_', ' ').title()
            matter_types[matter_type] = matter_types.get(matter_type, 0) + 1
        
        if not matter_types:
            matter_types = {'Corporate': 5, 'Litigation': 3, 'Family': 4, 'Real Estate': 2}
        
        fig = go.Figure(data=[go.Pie(
            labels=list(matter_types.keys()),
            values=list(matter_types.values()),
            hole=.3,
            marker_colors=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
        )])
        
        fig.update_layout(
            title='Matter Distribution by Type',
            height=400
        )
        
        return fig
    
    def create_productivity_metrics(self) -> Dict:
        """Create productivity metrics and charts"""
        # Sample productivity data
        productivity_data = {
            'billable_hours_trend': {
                'dates': pd.date_range(start='2024-01-01', periods=30, freq='D'),
                'hours': np.random.normal(7.5, 1.5, 30)
            },
            'document_processing_speed': {
                'avg_processing_time': 2.3,  # hours
                'documents_per_day': 12,
                'automation_savings': 45  # percentage
            },
            'client_response_time': {
                'avg_response_hours': 4.2,
                'target_response_hours': 6,
                'improvement_rate': 23  # percentage
            }
        }
        
        return productivity_data
    
    def generate_financial_forecast(self, months_ahead: int = 6) -> Dict:
        """Generate financial forecast"""
        # Simple linear regression for demonstration
        current_revenue = sum(inv.total_amount for inv in st.session_state.invoices if inv.status == 'paid')
        monthly_growth_rate = 0.08  # 8% monthly growth
        
        forecast = []
        base_revenue = current_revenue / 12  # Monthly average
        
        for month in range(1, months_ahead + 1):
            projected_revenue = base_revenue * (1 + monthly_growth_rate) ** month
            forecast.append({
                'month': (datetime.now() + timedelta(days=30*month)).strftime('%B %Y'),
                'projected_revenue': projected_revenue,
                'confidence_interval': (projected_revenue * 0.85, projected_revenue * 1.15)
            })
        
        return {
            'forecast': forecast,
            'growth_rate': monthly_growth_rate,
            'confidence': 0.75
        }
    
    def create_workload_analysis(self) -> go.Figure:
        """Create attorney workload analysis"""
        # Sample workload data
        attorneys = ['Partner A', 'Partner B', 'Associate C', 'Associate D', 'Paralegal E']
        current_hours = [42, 38, 35, 41, 28]
        capacity_hours = [45, 45, 40, 40, 35]
        
        fig = go.Figure(data=[
            go.Bar(name='Current Hours', x=attorneys, y=current_hours, marker_color='#2E86AB'),
            go.Bar(name='Capacity', x=attorneys, y=capacity_hours, marker_color='#E9ECEF', opacity=0.6)
        ])
        
        fig.update_layout(
            title='Attorney Workload Analysis',
            xaxis_title='Attorney',
            yaxis_title='Hours per Week',
            barmode='group',
            template='plotly_white',
            height=400
        )
        
        return fig

# Notification System
class NotificationSystem:
    def __init__(self):
        self.notification_queue = []
    
    def send_notification(self, user_id: str, title: str, message: str, 
                         notification_type: NotificationType, priority: str = 'normal'):
        """Send notification to user"""
        notification = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'title': title,
            'message': message,
            'type': notification_type.value,
            'priority': priority,
            'timestamp': datetime.now(),
            'read': False
        }
        
        self.notification_queue.append(notification)
        
        # In production, this would trigger actual notifications
        if notification_type == NotificationType.EMAIL:
            self._send_email_notification(notification)
        elif notification_type == NotificationType.SMS:
            self._send_sms_notification(notification)
    
    def _send_email_notification(self, notification: Dict):
        """Send email notification (placeholder)"""
        pass
    
    def _send_sms_notification(self, notification: Dict):
        """Send SMS notification (placeholder)"""
        pass
    
    def get_user_notifications(self, user_id: str, unread_only: bool = False) -> List[Dict]:
        """Get notifications for user"""
        user_notifications = [n for n in self.notification_queue if n['user_id'] == user_id]
        
        if unread_only:
            user_notifications = [n for n in user_notifications if not n['read']]
        
        return sorted(user_notifications, key=lambda x: x['timestamp'], reverse=True)

# Initialize all systems
initialize_enhanced_session_state()

# Load comprehensive sample data
def load_comprehensive_sample_data():
    """Load comprehensive sample data for demonstration"""
    
    # Sample clients
    if not st.session_state.clients:
        sample_clients = [
            Client(
                id="client_1",
                name="Acme Corporation",
                client_type="business",
                contact_info={"phone": "(555) 123-4567", "email": "legal@acme.com"},
                billing_address={"street": "123 Business St", "city": "New York", "state": "NY", "zip": "10001"},
                primary_contact="John Doe, General Counsel",
                created_date=datetime.now() - timedelta(days=365),
                status="active",
                portal_access=True,
                portal_credentials={"email": "legal@acme.com", "password": hashlib.sha256("demo123".encode()).hexdigest()},
                billing_preferences={"payment_terms": "Net 30", "preferred_format": "email"},
                communication_preferences={"email": True, "sms": False, "portal": True}
            ),
            Client(
                id="client_2",
                name="Sarah Johnson",
                client_type="individual",
                contact_info={"phone": "(555) 987-6543", "email": "sarah@email.com"},
                billing_address={"street": "456 Family Ave", "city": "Boston", "state": "MA", "zip": "02101"},
                primary_contact="Sarah Johnson",
                created_date=datetime.now() - timedelta(days=180),
                status="active",
                portal_access=True,
                portal_credentials={"email": "sarah@email.com", "password": hashlib.sha256("demo456".encode()).hexdigest()},
                billing_preferences={"payment_terms": "Net 15", "preferred_format": "mail"},
                communication_preferences={"email": True, "sms": True, "portal": True}
            )
        ]
        st.session_state.clients = sample_clients
    
    # Sample enhanced matters with more details
    if not st.session_state.matters:
        sample_matters = [
            Matter(
                id="matter_1",
                name="Acme Corp M&A Transaction",
                client_id="client_1",
                client_name="Acme Corporation",
                matter_type="corporate",
                status="active",
                created_date=datetime.now() - timedelta(days=45),
                assigned_attorneys=["partner@firm.com", "associate@firm.com"],
                description="Merger and acquisition transaction involving subsidiary purchase",
                budget=150000.0,
                estimated_hours=300,
                actual_hours=125.5,
                important_dates={
                    "Due Diligence Deadline": datetime.now() + timedelta(days=14),
                    "Closing Date": datetime.now() + timedelta(days=60),
                    "Board Approval": datetime.now() + timedelta(days=30)
                },
                billing_rate=450.0,
                priority="high",
                court_info={},
                opposing_parties=[],
                statute_of_limitations=None,
                custom_fields={"deal_value": "$5M", "target_company": "TechStart Inc"}
            ),
            Matter(
                id="matter_2",
                name="Johnson Custody Modification",
                client_id="client_2",
                client_name="Sarah Johnson",
                matter_type="family",
                status="active",
                created_date=datetime.now() - timedelta(days=30),
                assigned_attorneys=["family@firm.com"],
                description="Child custody modification due to relocation",
                budget=15000.0,
                estimated_hours=40,
                actual_hours=18.0,
                important_dates={
                    "Court Hearing": datetime.now() + timedelta(days=21),
                    "Mediation": datetime.now() + timedelta(days=7),
                    "Response Due": datetime.now() + timedelta(days=3)
                },
                billing_rate=350.0,
                priority="medium",
                court_info={
                    "court_name": "Superior Court of Massachusetts",
                    "case_number": "FC-2024-001234",
                    "judge": "Hon. Patricia Williams"
                },
                opposing_parties=[{"name": "Michael Johnson", "attorney": "Smith & Associates"}],
                statute_of_limitations=None,
                custom_fields={"children_ages": "8, 12", "current_custody": "joint"}
            )
        ]
        st.session_state.matters = sample_matters
    
    # Sample calendar events
    if not st.session_state.calendar_events:
        calendar_integration = CalendarIntegration()
        sample_events = [
            calendar_integration.create_event(
                "Court Hearing - Johnson",
                "Custody modification hearing",
                datetime.now() + timedelta(days=21, hours=9),
                datetime.now() + timedelta(days=21, hours=11),
                "court_date",
                "matter_2"
            ),
            calendar_integration.create_event(
                "Client Meeting - Acme Corp",
                "M&A due diligence review",
                datetime.now() + timedelta(days=2, hours=14),
                datetime.now() + timedelta(days=2, hours=16),
                "meeting",
                "matter_1"
            ),
            calendar_integration.create_event(
                "Document Filing Deadline",
                "Submit amended complaint",
                datetime.now() + timedelta(days=5, hours=17),
                datetime.now() + timedelta(days=5, hours=17, minutes=30),
                "deadline",
                "matter_2"
            )
        ]
        st.session_state.calendar_events = sample_events
    
    # Sample invoices
    if not st.session_state.invoices:
        billing_system = BillingSystem()
        sample_invoices = [
            Invoice(
                id="inv_1",
                client_id="client_1",
                matter_id="matter_1",
                invoice_number="INV-20241201-0001",
                date_issued=datetime.now() - timedelta(days=30),
                due_date=datetime.now(),
                line_items=[
                    {"date": datetime.now() - timedelta(days=35), "description": "Document review and analysis", "hours": 8.0, "rate": 450.0, "amount": 3600.0},
                    {"date": datetime.now() - timedelta(days=33), "description": "Client consultation", "hours": 2.5, "rate": 450.0, "amount": 1125.0}
                ],
                subtotal=4725.0,
                tax_rate=0.08,
                tax_amount=378.0,
                total_amount=5103.0,
                status="paid",
                payment_terms="Net 30",
                notes="Thank you for your business"
            )
        ]
        st.session_state.invoices = sample_invoices
    
    # Sample AI insights
    if not st.session_state.ai_insights:
        sample_insights = [
            AIInsight(
                id="ai_1",
                document_id="doc_1",
                insight_type="risk_analysis",
                content={
                    "risk_level": "medium",
                    "identified_risks": ["Undefined termination clause", "Ambiguous payment terms"],
                    "recommendations": ["Add specific termination procedures", "Clarify payment schedule"]
                },
                confidence_score=0.85,
                created_date=datetime.now() - timedelta(hours=2),
                reviewed=False,
                action_required=True
            ),
            AIInsight(
                id="ai_2",
                document_id="doc_2",
                insight_type="deadline_extraction",
                content={
                    "deadlines": [
                        {"text": "Response due within 30 days", "date": datetime.now() + timedelta(days=30)},
                        {"text": "Hearing scheduled for January 15", "date": datetime(2025, 1, 15)}
                    ]
                },
                confidence_score=0.92,
                created_date=datetime.now() - timedelta(hours=1),
                reviewed=False,
                action_required=True
            )
        ]
        st.session_state.ai_insights = sample_insights

# Load comprehensive sample data
load_comprehensive_sample_data()

# Initialize system components
email_integration = EmailIntegration({
    'smtp_server': 'smtp.gmail.com',
    'imap_server': 'imap.gmail.com',
    'username': 'demo@legaldocpro.com',
    'password': 'demo_password'
})

calendar_integration = CalendarIntegration()
billing_system = BillingSystem()
ai_system = AIAnalysisSystem()
client_portal = ClientPortal()
integration_manager = IntegrationManager()
mobile_framework = MobileAppFramework()
business_intelligence = BusinessIntelligence()
notification_system = NotificationSystem()

# Authentication Check
def is_logged_in():
    return st.session_state.get('user') is not None

def get_user_role():
    if not is_logged_in():
        return None
    return st.session_state.user.get('role', 'associate')

def has_permission(permission: str) -> bool:
    role = get_user_role()
    if not role:
        return False
    
    role_permissions = {
        'partner': ['read', 'write', 'delete', 'admin', 'billing', 'manage_users', 'ai_insights', 'integrations'],
        'associate': ['read', 'write', 'time_tracking', 'ai_insights'],
        'paralegal': ['read', 'time_tracking'],
        'client': ['read', 'portal_access']
    }
    
    return permission in role_permissions.get(role, [])

# Enhanced Login System
def show_comprehensive_login():
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ LegalDoc Pro Enterprise</h1>
        <p>Complete Legal Practice Management Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2, tab3 = st.tabs(["🔐 Login", "👥 Client Portal", "📱 Mobile Access"])
        
        with tab1:
            st.markdown("### Staff Login")
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
        
        with tab2:
            st.markdown("### Client Portal Access")
            with st.form("client_login"):
                client_email = st.text_input("Client Email", value="legal@acme.com")
                client_password = st.text_input("Password", type="password", value="demo123")
                
                if st.form_submit_button("Access Portal", use_container_width=True):
                    auth_result = client_portal.authenticate_client(client_email, client_password)
                    if auth_result:
                        st.session_state['user'] = {
                            'email': client_email,
                            'role': 'client',
                            'client_id': auth_result['client'].id,
                            'token': auth_result['token']
                        }
                        st.success("Welcome to your client portal!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        
        with tab3:
            st.markdown("### Mobile App Access")
            st.info("📱 Scan QR code to download mobile app")
            
            # Mobile app QR code (placeholder)
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <div style="width: 150px; height: 150px; background: #f0f0f0; margin: 0 auto; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                    📱 QR Code<br>Mobile App
                </div>
                <p style="margin-top: 1rem;">Available on iOS and Android</p>
            </div>
            """, unsafe_allow_html=True)

if not is_logged_in():
    show_comprehensive_login()
    st.stop()

# Enhanced Sidebar with Role-Based Navigation
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%); color: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
    <h3 style="margin: 0; text-align: center;">⚖️ LegalDoc Pro</h3>
    <p style="margin: 0.5rem 0 0 0; text-align: center; opacity: 0.9;">Enterprise Platform</p>
</div>
""", unsafe_allow_html=True)

user_role = get_user_role()
user_email = st.session_state['user']['email']

st.sidebar.markdown(f"**👤 Role:** {user_role.title()}")
st.sidebar.markdown(f"**📧 User:** {user_email}")

# Role-based navigation
if user_role == 'client':
    navigation_options = ["Client Dashboard", "My Documents", "Billing", "Messages", "Settings"]
else:
    navigation_options = ["Executive Dashboard", "Document Management", "Matter Management", "Calendar & Deadlines"]
    
    if has_permission('time_tracking'):
        navigation_options.append("Time & Billing")
    if has_permission('ai_insights'):
        navigation_options.append("AI Insights")
    if has_permission('integrations'):
        navigation_options.append("Integrations")
    if has_permission('admin'):
        navigation_options.extend(["Business Intelligence", "User Management", "System Settings"])
    
    navigation_options.extend(["Advanced Search", "Mobile App", "Audit Trail"])

page = st.sidebar.selectbox("🧭 Navigate", navigation_options)

# Notifications in sidebar
if user_role != 'client':
    unread_notifications = notification_system.get_user_notifications(user_email, unread_only=True)
    if unread_notifications:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🔔 Notifications")
        for notif in unread_notifications[:3]:  # Show top 3
            st.sidebar.markdown(f"• {notif['title']}")
        if len(unread_notifications) > 3:
            st.sidebar.markdown(f"... and {len(unread_notifications) - 3} more")

# System status in sidebar (for admins)
if has_permission('admin'):
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 System Status")
    st.sidebar.metric("Active Users", "24", "↑ 3")
    st.sidebar.metric("System Load", "68%", "↓ 5%")
    st.sidebar.metric("Storage Used", "2.1TB", "↑ 156GB")

if st.sidebar.button("🚪 Logout"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Main Content Area - Client Portal
if user_role == 'client' and page == "Client Dashboard":
    client_id = st.session_state['user']['client_id']
    client = next((c for c in st.session_state.clients if c.id == client_id), None)
    
    st.markdown(f"""
    <div class="main-header">
        <h1>👋 Welcome, {client.name if client else 'Client'}</h1>
        <p>Your Legal Matter Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Client metrics
    col1, col2, col3, col4 = st.columns(4)
    
    client_docs = client_portal.get_client_documents(client_id)
    client_billing = client_portal.get_client_billing_summary(client_id)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("My Documents", len(client_docs))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Outstanding Balance", f"${client_billing['outstanding_balance']:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Active Matters", len([m for m in st.session_state.matters if m.client_id == client_id and m.status == 'active']))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Paid", f"${client_billing['total_paid']:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Recent activity and updates
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Recent Documents")
        for doc in client_docs[-5:]:
            st.markdown(f"""
            <div class="client-portal">
                <strong>{doc.name}</strong><br>
                <small>Updated: {doc.last_modified.strftime('%Y-%m-%d')}</small><br>
                <small>Status: {doc.status.replace('_', ' ').title()}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📅 Upcoming Events")
        upcoming_events = [e for e in st.session_state.calendar_events 
                          if e.matter_id in [m.id for m in st.session_state.matters if m.client_id == client_id]]
        
        for event in upcoming_events[:5]:
            st.markdown(f"""
            <div class="client-portal">
                <strong>{event.title}</strong><br>
                <small>{event.start_time.strftime('%Y-%m-%d %H:%M')}</small><br>
                <small>Type: {event.event_type.replace('_', ' ').title()}</small>
            </div>
            """, unsafe_allow_html=True)

# Main Content Area - Staff Dashboards
elif page == "Executive Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Executive Dashboard</h1>
        <p>Strategic Overview & Key Performance Indicators</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate executive metrics
    exec_metrics = business_intelligence.generate_executive_dashboard()
    
    # Key Performance Indicators
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics_data = [
        ("Total Revenue", f"${exec_metrics['total_revenue']:,.0f}", f"{exec_metrics['revenue_growth']:+.1f}%"),
        ("Active Matters", exec_metrics['active_matters'], "+2"),
        ("Documents", exec_metrics['total_documents'], "+15"),
        ("Avg Matter Value", f"${exec_metrics['avg_matter_value']:,.0f}", "+12%"),
        ("Utilization", f"{exec_metrics['utilization_rate']:.1f}%", "+3.2%")
    ]
    
    for col, (label, value, change) in zip([col1, col2, col3, col4, col5], metrics_data):
        with col:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(label, value, change)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Charts and analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(business_intelligence.create_revenue_chart(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(business_intelligence.create_matter_type_distribution(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Workload Analysis
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(business_intelligence.create_workload_analysis(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Insights Summary
    if has_permission('ai_insights'):
        st.divider()
        st.subheader("🤖 AI Insights Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="ai-insight">
                <strong>📈 Performance Insights</strong><br>
                • Document processing speed up 23%<br>
                • Client response time improved by 18%<br>
                • Automated document classification: 94% accuracy
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="ai-insight">
                <strong>⚠️ Risk Alerts</strong><br>
                • 3 contracts require immediate attention<br>
                • 5 upcoming deadlines within 7 days<br>
                • 2 matters approaching budget limits
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="ai-insight">
                <strong>💡 Recommendations</strong><br>
                • Consider expanding paralegal team<br>
                • Automate routine document generation<br>
                • Implement client communication templates
            </div>
            """, unsafe_allow_html=True)

elif page == "Calendar & Deadlines":
    st.title("📅 Calendar & Deadline Management")
    
    # Calendar overview
    col1, col2, col3 = st.columns(3)
    
    upcoming_events = calendar_integration.get_upcoming_events()
    court_dates = calendar_integration.get_court_dates()
    deadlines = calendar_integration.get_deadlines()
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Upcoming Events", len(upcoming_events))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Court Dates", len(court_dates))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Deadlines", len(deadlines))
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Add new event
    if has_permission('write'):
        st.subheader("📅 Schedule New Event")
        
        with st.form("new_event"):
            col1, col2 = st.columns(2)
            
            with col1:
                event_title = st.text_input("Event Title")
                event_type = st.selectbox("Event Type", ["meeting", "court_date", "deadline", "reminder"])
                matter_selection = st.selectbox("Related Matter", [f"{m.name} - {m.client_name}" for m in st.session_state.matters])
            
            with col2:
                event_date = st.date_input("Date")
                event_time = st.time_input("Time")
                event_description = st.text_area("Description")
            
            if st.form_submit_button("Create Event"):
                if event_title and matter_selection:
                    matter_id = st.session_state.matters[[f"{m.name} - {m.client_name}" for m in st.session_state.matters].index(matter_selection)].id
                    
                    event_datetime = datetime.combine(event_date, event_time)
                    new_event = calendar_integration.create_event(
                        event_title, event_description, event_datetime,
                        event_datetime + timedelta(hours=1), event_type, matter_id
                    )
                    
                    st.session_state.calendar_events.append(new_event)
                    st.success(f"Event '{event_title}' created successfully!")
                    st.rerun()
        
        st.divider()
    
    # Upcoming events timeline
    st.subheader("📋 Upcoming Events")
    
    for event in upcoming_events[:10]:
        matter_name = next((m.name for m in st.session_state.matters if m.id == event.matter_id), "General")
        
        days_until = (event.start_time - datetime.now()).days
        urgency_class = "priority-high" if days_until <= 3 else ("priority-medium" if days_until <= 7 else "priority-low")
        
        st.markdown(f"""
        <div class="calendar-widget">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{event.title}</strong> <span class="status-badge status-{event.event_type.replace('_', '-')}">{event.event_type.replace('_', ' ').upper()}</span><br>
                    <small>Matter: {matter_name}</small><br>
                    <small>{event.start_time.strftime('%A, %B %d, %Y at %I:%M %p')}</small>
                </div>
                <div class="{urgency_class}">
                    <strong>{days_until} days</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif page == "AI Insights":
    st.title("🤖 AI-Powered Legal Intelligence")
    
    if not has_permission('ai_insights'):
        st.error("🚫 Access denied. AI Insights requires elevated permissions.")
        st.stop()
    
    # AI Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Documents Analyzed", "147", "+23")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Risk Alerts", "8", "+2")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Auto Classifications", "94%", "+3%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Time Saved", "127 hrs", "+18 hrs")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # AI Analysis Tools
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Document Analysis", "⚖️ Case Prediction", "🔍 Pattern Recognition", "📊 Insights Dashboard"])
    
    with tab1:
        st.subheader("AI Document Analysis")
        
        # Document selection for analysis
        if st.session_state.enhanced_documents:
            selected_doc_name = st.selectbox("Select Document to Analyze", 
                                           [d.name for d in st.session_state.enhanced_documents])
            selected_doc = next(d for d in st.session_state.enhanced_documents if d.name == selected_doc_name)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔍 Analyze Document", type="primary"):
                    with st.spinner("AI analyzing document..."):
                        time.sleep(2)  # Simulate processing
                        analysis = ai_system.analyze_contract(selected_doc.extracted_text)
                        
                        st.success("✅ Analysis Complete!")
                        
                        # Risk Assessment
                        st.markdown("### 📊 Risk Assessment")
                        risk_color = {"low": "🟢", "medium": "🟡", "high": "🔴", "critical": "⚫"}
                        st.markdown(f"{risk_color.get(analysis['risk_level'], '⚪')} **Risk Level: {analysis['risk_level'].upper()}**")
                        
                        # Key Clauses
                        st.markdown("### 📋 Key Clauses Identified")
                        for clause in analysis['key_clauses']:
                            importance_icon = "🔴" if clause['importance'] == 'high' else "🟡"
                            st.markdown(f"{importance_icon} **{clause['type'].replace('_', ' ').title()}:** {clause['text'][:100]}...")
                        
                        # Missing Clauses
                        if analysis['missing_clauses']:
                            st.markdown("### ⚠️ Potentially Missing Clauses")
                            for clause in analysis['missing_clauses']:
                                st.markdown(f"• {clause}")
            
            with col2:
                st.markdown("### 🎯 AI Recommendations")
                st.markdown("Based on document analysis:")
                
                recommendations = [
                    "Add explicit termination procedures to reduce ambiguity",
                    "Include force majeure clause for better risk protection",
                    "Clarify payment terms and penalties for late payment",
                    "Consider adding dispute resolution mechanism",
                    "Review limitation of liability clause"
                ]
                
                for rec in recommendations:
                    st.markdown(f"💡 {rec}")
                
                st.markdown("### 📈 Document Metrics")
                st.metric("Complexity Score", "67/100")
                st.metric("Completeness", "84%")
                st.metric("Risk Score", "Medium")
    
    with tab2:
        st.subheader("Case Outcome Prediction")
        
        # Matter selection for prediction
        if st.session_state.matters:
            selected_matter_name = st.selectbox("Select Matter for Analysis", 
                                              [f"{m.name} - {m.client_name}" for m in st.session_state.matters])
            selected_matter = st.session_state.matters[[f"{m.name} - {m.client_name}" for m in st.session_state.matters].index(selected_matter_name)]
            
            if st.button("🔮 Generate Prediction", type="primary"):
                with st.spinner("AI analyzing case factors..."):
                    time.sleep(2)
                    prediction = ai_system.predict_case_outcomes(selected_matter.__dict__)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 📊 Prediction Results")
                        st.metric("Success Probability", f"{prediction['success_probability']:.0%}")
                        st.metric("Estimated Duration", f"{prediction['estimated_duration']} days")
                        st.metric("Cost Estimate", f"${prediction['cost_estimate']:,.2f}")
                    
                    with col2:
                        st.markdown("### ⚠️ Risk Factors")
                        for risk in prediction['risk_factors']:
                            st.markdown(f"• {risk}")
                        
                        st.markdown("### 💡 Strategic Recommendations")
                        for rec in prediction['recommendations']:
                            st.markdown(f"• {rec}")
    
    with tab3:
        st.subheader("Pattern Recognition & Analytics")
        
        # Document relationship analysis
        if st.button("🔍 Analyze Document Patterns"):
            with st.spinner("Analyzing document relationships..."):
                time.sleep(2)
                relationships = ai_system.analyze_document_relationships(st.session_state.enhanced_documents)
                
                st.success("Pattern analysis complete!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📊 Document Clusters")
                    for cluster in relationships['document_clusters']:
                        st.markdown(f"**Cluster {cluster['cluster_id']}: {cluster['theme']}**")
                        st.markdown(f"Documents: {len(cluster['documents'])}")
                
                with col2:
                    st.markdown("### 📈 Topic Trends")
                    st.markdown("**Trending Topics:**")
                    for topic in relationships['topic_evolution']['trending_topics']:
                        st.markdown(f"🔥 {topic}")
                    
                    st.markdown("**Emerging Topics:**")
                    for topic in relationships['topic_evolution']['emerging_topics']:
                        st.markdown(f"🌟 {topic}")
    
    with tab4:
        st.subheader("AI Insights Dashboard")
        
        # Real-time AI insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Active Insights")
            for insight in st.session_state.ai_insights:
                action_icon = "🚨" if insight.action_required else "ℹ️"
                confidence_bar = "▓" * int(insight.confidence_score * 10) + "░" * (10 - int(insight.confidence_score * 10))
                
                st.markdown(f"""
                <div class="ai-insight">
                    {action_icon} <strong>{insight.insight_type.replace('_', ' ').title()}</strong><br>
                    Confidence: {confidence_bar} ({insight.confidence_score:.0%})<br>
                    <small>{insight.created_date.strftime('%Y-%m-%d %H:%M')}</small>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📈 AI Performance Metrics")
            
            # Create AI performance chart
            ai_metrics = pd.DataFrame({
                'Metric': ['Accuracy', 'Processing Speed', 'Risk Detection', 'Classification'],
                'Score': [94, 87, 91, 96]
            })
            
            fig = px.bar(ai_metrics, x='Metric', y='Score', 
                        title='AI Model Performance',
                        color='Score',
                        color_continuous_scale='viridis')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

elif page == "Integrations":
    st.title("🔗 Third-Party Integrations")
    
    if not has_permission('integrations'):
        st.error("🚫 Access denied. Integration management requires admin privileges.")
        st.stop()
    
    # Integration status overview
    col1, col2, col3, col4 = st.columns(4)
    
    active_integrations = len([i for i in st.session_state.integrations if i.status == 'active'])
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Active Integrations", active_integrations)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Available Integrations", len(integration_manager.available_integrations))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Last Sync", "2 mins ago")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Sync Success Rate", "98.5%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Available integrations
    st.subheader("🌐 Available Integrations")
    
    integration_categories = {
        'Email & Communication': ['outlook', 'gmail', 'slack'],
        'Document & Signature': ['docusign', 'adobe_sign', 'dropbox'],
        'Calendar & Scheduling': ['google_calendar', 'outlook_calendar', 'zoom'],
        'Accounting & Billing': ['quickbooks', 'xero', 'stripe'],
        'Legal Research': ['lexisnexis', 'westlaw', 'bloomberg_law'],
        'Court & Filing': ['court_filing', 'pacer', 'state_courts']
    }
    
    for category, integrations in integration_categories.items():
        st.markdown(f"### {category}")
        cols = st.columns(3)
        
        for i, integration_id in enumerate(integrations):
            with cols[i % 3]:
                if integration_id in integration_manager.available_integrations:
                    integration_info = integration_manager.available_integrations[integration_id]
                    is_active = any(integ.name == integration_info['name'] and integ.status == 'active' 
                                  for integ in st.session_state.integrations)
                    
                    status_color = "#28a745" if is_active else "#6c757d"
                    status_text = "CONNECTED" if is_active else "AVAILABLE"
                    
                    st.markdown(f"""
                    <div class="integration-card">
                        <h4>{integration_info['name']}</h4>
                        <p style="color: {status_color}
