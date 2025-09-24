import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import random
from dataclasses import dataclass
from typing import List

@dataclass
class Document:
    name: str
    last_modified: datetime
    status: str

class BusinessIntelligence:
    def __init__(self):
        self.setup_sample_data()
    
    def setup_sample_data(self):
        """Initialize sample data for the dashboard"""
        if 'documents' not in st.session_state:
            st.session_state.documents = self.generate_sample_documents()
    
    def generate_sample_documents(self) -> List[Document]:
        """Generate sample documents for demo purposes"""
        doc_names = [
            "Contract Amendment - ABC Corp",
            "Due Diligence Report - XYZ Merger",
            "Lease Agreement - Downtown Office",
            "Employment Agreement - Senior VP",
            "Patent Application - Tech Innovation",
            "Compliance Audit - Q4 2024",
            "Settlement Agreement - Litigation A",
            "Real Estate Purchase - Warehouse",
            "IP License Agreement - Software",
            "Corporate Bylaws Update"
        ]
        
        statuses = ["in_review", "approved", "pending", "draft", "executed"]
        documents = []
        
        for i, name in enumerate(doc_names):
            doc = Document(
                name=name,
                last_modified=datetime.now() - timedelta(days=random.randint(0, 30)),
                status=random.choice(statuses)
            )
            documents.append(doc)
        
        return documents
    
    def generate_executive_dashboard(self):
        """Generate executive dashboard metrics"""
        return {
            'total_revenue': 2850000,
            'revenue_growth': 8.3,
            'active_matters': 47,
            'total_documents': len(st.session_state.documents),
            'avg_matter_value': 125000,
            'utilization_rate': 87.5
        }
    
    def create_revenue_chart(self):
        """Create revenue trend chart"""
        months = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
        revenue = [180000, 195000, 210000, 225000, 240000, 260000, 285000]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=revenue,
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Monthly Revenue Trend',
            xaxis_title='Month',
            yaxis_title='Revenue ($)',
            yaxis=dict(tickformat='$,.0f'),  # FIXED: Moved tickformat into update_layout
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_matter_type_distribution(self):
        """Create matter type distribution chart"""
        matter_types = ['Corporate', 'Litigation', 'Real Estate', 'IP', 'Employment', 'Tax']
        values = [12, 8, 10, 7, 6, 4]
        colors = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
        
        fig = go.Figure(data=[go.Pie(
            labels=matter_types,
            values=values,
            hole=.3,
            marker_colors=colors
        )])
        
        fig.update_layout(
            title='Active Matters by Type',
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig

def show():
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .document-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 3px solid #28a745;
    }
    
    .client-portal {
        background: #e3f2fd;
        padding: 0.75rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
        border-left: 3px solid #2196f3;
    }
    
    .stMetric {
        background: transparent;
    }
    
    .stMetric > div {
        background: transparent;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-header">
        <h1>📊 Executive Dashboard</h1>
        <p>Strategic Overview & Key Performance Indicators</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate metrics
    bi = BusinessIntelligence()
    exec_metrics = bi.generate_executive_dashboard()
    
    # KPIs
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
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(bi.create_revenue_chart(), use_container_width=True)
    
    with col2:
        st.plotly_chart(bi.create_matter_type_distribution(), use_container_width=True)
    
    # Recent activity
    show_recent_activity()

def show_recent_activity():
    """Display recent activity section"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Recent Document Activity")
        
        # Ensure documents exist in session state
        if 'documents' not in st.session_state:
            bi = BusinessIntelligence()
            bi.setup_sample_data()
        
        recent_docs = sorted(st.session_state.documents, key=lambda x: x.last_modified, reverse=True)[:5]
        
        for doc in recent_docs:
            st.markdown(f"""
            <div class="document-card">
                <strong>{doc.name}</strong><br>
                <small>Updated: {doc.last_modified.strftime('%Y-%m-%d')}</small><br>
                <small>Status: {doc.status.replace('_', ' ').title()}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📅 Upcoming Events")
        events = [
            "📋 Board meeting - Jan 25, 2025",
            "📝 Document review - Jan 30, 2025", 
            "🏢 Closing preparation - Feb 5, 2025",
            "⚖️ Court hearing - Feb 8, 2025",
            "🤝 Client meeting - Feb 12, 2025"
        ]
        
        for event in events:
            st.markdown(f"""
            <div class="client-portal">
                {event}
            </div>
            """, unsafe_allow_html=True)

# Optional: Add a refresh button
if st.button("🔄 Refresh Dashboard"):
    st.rerun()

# Main execution
if __name__ == "__main__":
    show()
