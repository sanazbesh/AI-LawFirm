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
        
        # Handle both dict and Document object formats
        recent_docs = sorted(st.session_state.documents, 
                            key=lambda x: x.last_modified if hasattr(x, 'last_modified') else datetime.now(), 
                            reverse=True)[:5]
        
        for doc in recent_docs:
            # Handle both dict and Document object formats
            if hasattr(doc, 'name'):
                # Document object
                name = doc.name
                date = doc.last_modified.strftime('%Y-%m-%d')
                status = doc.status.replace('_', ' ').title()
            else:
                # Dictionary format
                name = doc.get('name', 'Unknown Document')
                date = datetime.now().strftime('%Y-%m-%d')
                status = doc.get('status', 'unknown').replace('_', ' ').title()
    
            st.markdown(f"""
            <div class="document-card">
                <strong>{name}</strong><br>
                <small>Updated: {date}</small><br>
                <small>Status: {status}</small>
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
