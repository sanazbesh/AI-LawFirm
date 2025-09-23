import streamlit as st
from services.business_intelligence import BusinessIntelligence

def show():
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
    _show_recent_activity()

def _show_recent_activity():
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recent Document Activity")
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
        st.subheader("Upcoming Events")
        events = [
            "Board meeting - Jan 25, 2025",
            "Document review - Jan 30, 2025",
            "Closing preparation - Feb 5, 2025"
        ]
        
        for event in events:
            st.markdown(f"""
            <div class="client-portal">
                {event}
            </div>
            """, unsafe_allow_html=True)
