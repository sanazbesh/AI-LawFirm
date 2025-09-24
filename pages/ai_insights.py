import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="AI Legal Insights",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1f4e79, #2d5aa0);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.main-header h1 {
    margin: 0;
    font-size: 3rem;
    font-weight: bold;
}

.main-header p {
    margin: 0.5rem 0 0 0;
    font-size: 1.2rem;
    opacity: 0.9;
}

.metric-container {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #1f4e79;
    margin: 0.5rem 0;
}

.alert-high {
    background-color: #ffe6e6;
    border-left: 4px solid #dc3545;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 4px;
}

.alert-medium {
    background-color: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 4px;
}

.alert-low {
    background-color: #d4edda;
    border-left: 4px solid #28a745;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 4px;
}

.stTab > div > div > div > div {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

def show():
    """Main function to display the AI Insights dashboard"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Insights</h1>
        <p>Artificial Intelligence-Powered Legal Analytics & Predictions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Insights tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Document Analysis", 
        "📈 Predictive Analytics", 
        "🎯 Risk Assessment", 
        "📝 Contract Intelligence", 
        "⚖️ Case Law Research"
    ])
    
    with tab1:
        show_document_analysis()
    
    with tab2:
        show_predictive_analytics()
    
    with tab3:
        show_risk_assessment()
    
    with tab4:
        show_contract_intelligence()
    
    with tab5:
        show_case_law_research()

def show_document_analysis():
    """Display document analysis dashboard"""
    st.subheader("📊 AI Document Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Document Classification & Sentiment")
        
        # Document classification data
        doc_data = pd.DataFrame({
            'Document Type': ['Contracts', 'Briefs', 'Motions', 'Discovery', 'Correspondence'],
            'Count': [145, 89, 67, 112, 203],
            'AI Confidence': [94.2, 91.7, 88.9, 92.1, 87.4]
        })
        
        fig = px.bar(
            doc_data, 
            x='Document Type', 
            y='Count', 
            color='AI Confidence', 
            color_continuous_scale='viridis',
            title="Document Classification Results",
            text='Count'
        )
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Sentiment analysis
        st.markdown("#### Document Sentiment Analysis")
        sentiment_data = pd.DataFrame({
            'Sentiment': ['Positive', 'Neutral', 'Negative'],
            'Count': [234, 312, 70],
            'Percentage': [38.0, 50.6, 11.4]
        })
        
        fig2 = px.pie(
            sentiment_data, 
            values='Count', 
            names='Sentiment',
            color_discrete_sequence=['#2E8B57', '#FFD700', '#DC143C'],
            title="Overall Document Sentiment Distribution"
        )
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("#### AI Processing Status")
        
        # Processing metrics
        metrics = [
            ("Documents Processed", "2,847", "+12%"),
            ("AI Accuracy Rate", "94.2%", "+2.1%"),
            ("Processing Speed", "2.3s", "-0.4s"),
            ("Data Quality Score", "98.7%", "+1.2%")
        ]
        
        for label, value, change in metrics:
            st.metric(label, value, change)
        
        st.markdown("#### Recent AI Actions")
        st.markdown("---")
        
        actions = [
            ("✅", "Classified 15 new contracts", "2 min ago"),
            ("🔍", "Extracted key terms from merger agreement", "5 min ago"),
            ("⚠️", "Flagged potential compliance issue", "12 min ago"),
            ("📊", "Updated risk assessment models", "1 hour ago"),
            ("🤖", "Enhanced NLP algorithms", "2 hours ago")
        ]
        
        for icon, action, time in actions:
            st.markdown(f"{icon} {action}")
            st.caption(time)
            st.markdown("---")

def show_predictive_analytics():
    """Display predictive analytics dashboard"""
    st.subheader("📈 Predictive Analytics Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Case Outcome Predictions")
        
        # Generate prediction data with more realistic patterns
        np.random.seed(42)  # For reproducible results
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        win_prob_base = 0.75
        settlement_prob_base = 0.45
        
        predictions = pd.DataFrame({
            'Month': dates,
            'Win Probability': [max(0.3, min(0.95, win_prob_base + np.random.normal(0, 0.1))) for _ in dates],
            'Settlement Probability': [max(0.1, min(0.8, settlement_prob_base + np.random.normal(0, 0.1))) for _ in dates],
            'Cost Prediction': [np.random.uniform(50000, 200000) for _ in dates]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=predictions['Month'], 
            y=predictions['Win Probability'],
            mode='lines+markers', 
            name='Win Probability',
            line=dict(color='#2E8B57', width=3),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=predictions['Month'], 
            y=predictions['Settlement Probability'],
            mode='lines+markers', 
            name='Settlement Probability',
            line=dict(color='#FF8C00', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Case Outcome Predictions Over Time',
            xaxis_title='Month', 
            yaxis_title='Probability',
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Litigation Timeline Prediction")
        timeline_data = pd.DataFrame({
            'Phase': ['Discovery', 'Motions', 'Trial Prep', 'Trial', 'Appeal'],
            'Predicted Duration (Months)': [4.2, 2.1, 3.8, 1.2, 8.5],
            'Confidence': [89, 92, 87, 91, 76]
        })
        
        fig2 = px.bar(
            timeline_data, 
            x='Phase', 
            y='Predicted Duration (Months)',
            color='Confidence', 
            color_continuous_scale='RdYlGn',
            title="Litigation Phase Duration Predictions",
            text='Predicted Duration (Months)'
        )
        fig2.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("#### Budget Forecasting")
        
        # Budget prediction with trend
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        actual = [45000, 52000, 48000, 61000, 59000, 67000]
        predicted = [68000, 71000, 73000, 75000, 78000, 82000]
        
        budget_df = pd.DataFrame({
            'Month': months[:6] + months[6:],
            'Amount': actual + predicted,
            'Type': ['Actual'] * 6 + ['Predicted'] * 6
        })
        
        fig3 = px.line(
            budget_df, 
            x='Month', 
            y='Amount', 
            color='Type',
            title='Budget Forecast vs Actual',
            markers=True
        )
        fig3.update_layout(height=300)
        st.plotly_chart(fig3, use_container_width=True)
        
        # Cost breakdown
        st.markdown("#### Cost Breakdown Analysis")
        cost_breakdown = pd.DataFrame({
            'Category': ['Personnel', 'External Counsel', 'Technology', 'Travel', 'Other'],
            'Percentage': [45, 30, 15, 7, 3],
            'Amount': [270000, 180000, 90000, 42000, 18000]
        })
        
        fig4 = px.pie(
            cost_breakdown, 
            values='Percentage', 
            names='Category',
            title='Budget Allocation',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig4.update_layout(height=300)
        st.plotly_chart(fig4, use_container_width=True)
        
        st.markdown("#### AI Recommendations")
        recommendations = [
            ("🎯", "Focus on settlement negotiations for Case #2024-107", "High Priority"),
            ("⏰", "Expedite discovery phase for optimal timeline", "Medium Priority"),
            ("💰", "Budget increase of 15% recommended for Q4", "High Priority"),
            ("📋", "Additional resources needed for complex litigation", "Medium Priority"),
            ("🤝", "Consider mediation for cost reduction", "Low Priority")
        ]
        
        for icon, rec, priority in recommendations:
            if priority == "High Priority":
                st.error(f"{icon} {rec}")
            elif priority == "Medium Priority":
                st.warning(f"{icon} {rec}")
            else:
                st.info(f"{icon} {rec}")

def show_risk_assessment():
    """Display risk assessment dashboard"""
    st.subheader("🎯 AI-Powered Risk Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Overall Risk Score")
        
        # Risk gauge with improved styling
        risk_score = 73
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=risk_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk Level", 'font': {'size': 24}},
            delta={'reference': 80, 'position': "top"},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': 'lightgray'},
                    {'range': [50, 80], 'color': 'yellow'},
                    {'range': [80, 100], 'color': 'red'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk trend
        st.markdown("#### Risk Trend (30 Days)")
        trend_dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        risk_values = [risk_score + np.random.normal(0, 5) for _ in trend_dates]
        risk_values = [max(0, min(100, val)) for val in risk_values]  # Clamp between 0-100
        
        trend_df = pd.DataFrame({
            'Date': trend_dates,
            'Risk Score': risk_values
        })
        
        fig_trend = px.line(
            trend_df, 
            x='Date', 
            y='Risk Score',
            title='Risk Score Trend',
            line_shape='spline'
        )
        fig_trend.update_layout(height=250)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        st.markdown("#### Risk Categories")
        
        risk_categories = pd.DataFrame({
            'Category': ['Compliance', 'Financial', 'Operational', 'Reputational', 'Strategic'],
            'Risk Score': [85, 67, 72, 43, 59],
            'Trend': ['↗️', '↘️', '→', '↘️', '↗️'],
            'Impact': ['High', 'Medium', 'Medium', 'Low', 'Medium']
        })
        
        fig2 = px.bar(
            risk_categories, 
            x='Category', 
            y='Risk Score',
            color='Risk Score', 
            color_continuous_scale='Reds',
            title='Risk by Category',
            text='Risk Score'
        )
        fig2.update_traces(texttemplate='%{text}', textposition='outside')
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Risk matrix
        st.markdown("#### Risk Impact Matrix")
        risk_matrix_data = pd.DataFrame({
            'Probability': [0.8, 0.6, 0.7, 0.4, 0.5],
            'Impact': [0.9, 0.7, 0.6, 0.5, 0.6],
            'Category': ['Compliance', 'Financial', 'Operational', 'Reputational', 'Strategic'],
            'Size': [85, 67, 72, 43, 59]
        })
        
        fig3 = px.scatter(
            risk_matrix_data,
            x='Probability',
            y='Impact',
            size='Size',
            color='Category',
            title='Risk Probability vs Impact Matrix',
            hover_data=['Category']
        )
        fig3.update_layout(height=300)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col3:
        st.markdown("#### Risk Alerts")
        
        alerts = [
            ("🔴 Critical", "Regulatory compliance gap detected in contract #2024-089", "2 hours ago"),
            ("🟡 High", "Contract renewal deadline approaching in 15 days", "4 hours ago"),
            ("🔴 Critical", "Litigation exposure increased by 23%", "6 hours ago"),
            ("🟡 High", "Staff capacity constraint in IP department", "1 day ago"),
            ("🟢 Low", "Insurance coverage adequate for current exposure", "2 days ago")
        ]
        
        for severity, alert, time in alerts:
            if "Critical" in severity:
                st.error(f"**{severity}**")
                st.error(f"{alert}")
                st.caption(f"⏰ {time}")
            elif "High" in severity:
                st.warning(f"**{severity}**")
                st.warning(f"{alert}")
                st.caption(f"⏰ {time}")
            else:
                st.success(f"**{severity}**")
                st.success(f"{alert}")
                st.caption(f"⏰ {time}")
            st.markdown("---")
        
        # Risk mitigation actions
        st.markdown("#### Recommended Actions")
        actions = [
            "📋 Schedule compliance audit",
            "📞 Contact insurance broker",
            "👥 Hire additional IP counsel",
            "📊 Update risk assessment model",
            "🔍 Review high-risk contracts"
        ]
        
        for action in actions:
            if st.button(action, key=f"action_{action}"):
                st.success(f"Action initiated: {action}")

def show_contract_intelligence():
    """Display contract intelligence dashboard"""
    st.subheader("📝 AI Contract Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Contract Analysis Results")
        
        # Contract metrics with improved data
        contract_metrics = pd.DataFrame({
            'Metric': ['Total Contracts', 'AI-Reviewed', 'Anomalies Detected', 'Key Terms Extracted', 'Auto-Generated'],
            'Count': [1247, 1180, 67, 5890, 234],
            'Accuracy': [100, 94.6, 89.2, 97.1, 92.8]
        })
        
        fig = px.bar(
            contract_metrics, 
            x='Metric', 
            y='Count',
            color='Accuracy', 
            color_continuous_scale='Blues',
            title='Contract Processing Statistics',
            text='Count'
        )
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Key Terms Analysis")
        
        terms_data = pd.DataFrame({
            'Term Type': ['Payment Terms', 'Termination Clauses', 'Liability Limits', 'Renewal Options', 'IP Rights', 'Confidentiality'],
            'Frequency': [432, 387, 295, 234, 189, 156],
            'Risk Level': ['Low', 'Medium', 'High', 'Medium', 'High', 'Medium'],
            'Avg Value Impact': [50000, 75000, 200000, 45000, 150000, 25000]
        })
        
        color_map = {'Low': '#2E8B57', 'Medium': '#FF8C00', 'High': '#DC143C'}
        fig2 = px.scatter(
            terms_data, 
            x='Term Type', 
            y='Frequency',
            color='Risk Level', 
            color_discrete_map=color_map,
            size='Avg Value Impact',
            title='Contract Terms by Risk Level and Value Impact',
            hover_data=['Avg Value Impact']
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("#### Contract Health Score")
        
        health_score = 87.3
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health_score,
            title={'text': "Contract Portfolio Health", 'font': {'size': 20}},
            number={'font': {'size': 40}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': "#2E8B57"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 60], 'color': 'lightgray'},
                    {'range': [60, 90], 'color': 'lightgreen'},
                    {'range': [90, 100], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 95
                }
            }
        ))
        fig3.update_layout(height=300)
        st.plotly_chart(fig3, use_container_width=True)
        
        # Contract status distribution
        st.markdown("#### Contract Status Distribution")
        status_data = pd.DataFrame({
            'Status': ['Active', 'Pending Renewal', 'Under Review', 'Expired', 'Draft'],
            'Count': [856, 167, 98, 45, 81],
            'Percentage': [68.7, 13.4, 7.9, 3.6, 6.5]
        })
        
        fig4 = px.pie(
            status_data,
            values='Count',
            names='Status',
            title='Contract Status Overview',
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.4
        )
        fig4.update_layout(height=300)
        st.plotly_chart(fig4, use_container_width=True)
        
        st.markdown("#### AI Insights & Recommendations")
        insights = [
            ("📋", "15 contracts require renewal within 90 days", "Action Required"),
            ("⚠️", "3 contracts have unusual termination clauses", "Review Needed"),
            ("💰", "Potential cost savings of $2.3M identified", "Opportunity"),
            ("🔍", "5 contracts missing standard IP protection", "Risk Alert"),
            ("📊", "Average contract value increased 12% YoY", "Trend Analysis"),
            ("🤖", "AI suggests standardizing payment terms", "Optimization")
        ]
        
        for icon, insight, category in insights:
            if category == "Action Required":
                st.error(f"{icon} **{category}**: {insight}")
            elif category == "Review Needed" or category == "Risk Alert":
                st.warning(f"{icon} **{category}**: {insight}")
            elif category == "Opportunity":
                st.success(f"{icon} **{category}**: {insight}")
            else:
                st.info(f"{icon} **{category}**: {insight}")

def show_case_law_research():
    """Display case law research dashboard"""
    st.subheader("⚖️ AI Case Law Research Assistant")
    
    # Initialize session state for search results
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### Legal Research Query Interface")
        
        # Enhanced search interface
        search_query = st.text_input(
            "Enter your legal research query:", 
            placeholder="e.g., contract disputes intellectual property, employment law termination, patent infringement damages",
            help="Use specific legal terms and concepts for better results"
        )
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            jurisdiction = st.selectbox("Jurisdiction:", 
                                      ["Federal", "State", "International", "Supreme Court", "Circuit Courts"])
        with col_b:
            case_type = st.selectbox("Case Type:", 
                                   ["All", "Civil", "Criminal", "Administrative", "Constitutional", "Commercial"])
        with col_c:
            date_range = st.selectbox("Date Range:", 
                                    ["Last year", "Last 3 years", "Last 5 years", "Last 10 years", "All time"])
        
        # Advanced search options
        with st.expander("Advanced Search Options"):
            col_d, col_e = st.columns(2)
            with col_d:
                citation_required = st.checkbox("Must have citations")
                precedential_only = st.checkbox("Precedential cases only")
            with col_e:
                min_relevance = st.slider("Minimum relevance score:", 0, 100, 80)
                max_results = st.slider("Maximum results:", 1, 50, 10)
        
        if st.button("🔍 Search Case Law", type="primary"):
            with st.spinner("Searching legal databases..."):
                # Simulate search process
                progress_bar = st.progress(0)
                for i in range(100):
                    progress_bar.progress(i + 1)
                
                st.session_state.search_results = generate_mock_search_results(search_query, jurisdiction, case_type)
                st.success(f"Found {len(st.session_state.search_results)} relevant cases")
        
        # Display search results
        if st.session_state.search_results:
            st.markdown("#### Search Results")
            
            # Add sorting options
            col_sort1, col_sort2 = st.columns(2)
            with col_sort1:
                sort_by = st.selectbox("Sort by:", ["Relevance", "Date", "Citations", "Court Level"])
            with col_sort2:
                sort_order = st.selectbox("Order:", ["Descending", "Ascending"])
            
            for i, result in enumerate(st.session_state.search_results, 1):
                with st.expander(f"#{i} {result['case']} ({result['relevance']} relevant)", expanded=(i <= 3)):
                    col_info1, col_info2 = st.columns(2)
                    
                    with col_info1:
                        st.markdown(f"**Court:** {result['court']}")
                        st.markdown(f"**Date:** {result['date']}")
                        st.markdown(f"**Citations:** {result['citations']}")
                    
                    with col_info2:
                        st.markdown(f"**Judge:** {result['judge']}")
                        st.markdown(f"**Case Type:** {result['case_type']}")
                        st.markdown(f"**Precedential:** {'Yes' if result['precedential'] else 'No'}")
                    
                    st.markdown(f"**Summary:** {result['summary']}")
                    
                    if 'key_holdings' in result:
                        st.markdown("**Key Holdings:**")
                        for holding in result['key_holdings']:
                            st.markdown(f"• {holding}")
                    
                    # Action buttons
                    col_action1, col_action2, col_action3, col_action4 = st.columns(4)
                    with col_action1:
                        if st.button(f"📄 Full Text", key=f"view_{i}"):
                            st.info("Opening full case text...")
                    with col_action2:
                        if st.button(f"📎 Add to Brief", key=f"add_{i}"):
                            st.success("Added to research brief!")
                    with col_action3:
                        if st.button(f"📊 Citation Analysis", key=f"cite_{i}"):
                            st.info("Analyzing citation network...")
                    with col_action4:
                        if st.button(f"🔗 Similar Cases", key=f"similar_{i}"):
                            st.info("Finding similar cases...")
    
    with col2:
        st.markdown("#### Research Analytics")
        
        # Research metrics
        metrics = [
            ("Cases Indexed", "2.4M"),
            ("Search Accuracy", "96.3%"),
            ("Avg. Research Time", "8.5 min"),
            ("Citations Generated", "12,347"),
            ("Active Researchers", "1,247")
        ]
        
        for label, value in metrics:
            st.metric(label, value)
        
        st.markdown("---")
        
        st.markdown("#### Recent Research Activity")
        recent_searches = [
            ("Contract interpretation", "15 min ago"),
            ("IP licensing disputes", "32 min ago"),
            ("Employment law updates", "1 hour ago"),
            ("Corporate governance", "2 hours ago"),
            ("Tax regulation changes", "3 hours ago"),
            ("Securities fraud cases", "4 hours ago")
        ]
        
        for search, time in recent_searches:
            st.write(f"🔍 **{search}**")
            st.caption(time)
            st.markdown("---")
        
        st.markdown("#### Research Tools")
        
        tools = [
            ("📚 Legal Research Library", "Browse legal database"),
            ("📊 Citation Analytics", "Analyze case citations"),
            ("🤖 AI Legal Assistant", "Get AI-powered insights"),
            ("📋 Research Templates", "Use research templates"),
            ("💾 Save Research", "Save current session"),
            ("📤 Export Results", "Export to various formats")
        ]
        
        for tool_name, description in tools:
            if st.button(tool_name, key=f"tool_{tool_name}", help=description):
                st.success(f"Opening {tool_name}...")

def generate_mock_search_results(query, jurisdiction, case_type):
    """Generate realistic mock search results"""
    base_results = [
        {
            "case": "Smith v. ABC Corporation",
            "court": "9th Circuit Court of Appeals",
            "date": "2023-03-15",
            "judge": "Judge Johnson",
            "case_type": "Commercial",
            "relevance": "96%",
            "citations": 47,
            "precedential": True,
            "summary": "Landmark decision on contract interpretation regarding intellectual property licensing agreements. Court established new standard for determining implied terms in technology transfer agreements.",
            "key_holdings": [
                "Implied terms in IP licenses must be reasonably necessary for contract performance",
                "Industry custom can establish contractual obligations even without express terms",
                "Licensee's duty of good faith extends to protecting licensor's IP rights"
            ]
        },
        {
            "case": "Johnson Industries v. Tech Solutions LLC",
            "court": "Federal District Court, N.D. Cal",
            "date": "2022-11-08",
            "judge": "Judge Martinez",
            "case_type": "Commercial",
            "relevance": "94%",
            "citations": 23,
            "precedential": True,
            "summary": "Software licensing dispute involving breach of contract and trade secret misappropriation. Court addressed the intersection of contract law and intellectual property protection.",
            "key_holdings": [
                "Software escrow provisions are enforceable and essential for protecting both parties",
                "Trade secret protection continues even after contract termination",
                "Reasonable efforts to maintain secrecy must be documented and ongoing"
            ]
        },
        {
            "case": "Continental Corp v. Innovation Labs",
            "court": "Delaware Supreme Court",
            "date": "2021-07-22",
            "judge": "Chief Judge Roberts",
            "case_type": "Corporate",
            "relevance": "92%",
            "citations": 156,
            "precedential": True,
            "summary": "Corporate governance dispute involving fiduciary duties and business judgment rule. Significant precedent for director liability in technology acquisitions.",
            "key_holdings": [
                "Directors must exercise heightened scrutiny in related-party transactions",
                "Business judgment rule protection requires informed decision-making process",
                "Independent committee recommendations carry significant weight in court review"
            ]
        },
        {
            "case": "Metropolitan Insurance v. DataCorp",
            "court": "2nd Circuit Court of Appeals",
            "date": "2023-01-12",
            "judge": "Judge Thompson",
            "case_type": "Insurance",
            "relevance": "89%",
            "citations": 34,
            "precedential": True,
            "summary": "Coverage dispute for cyber liability insurance in data breach incident. Established important precedent for interpreting cyber insurance policy language.",
            "key_holdings": [
                "First-party coverage extends to business interruption from cyber incidents",
                "Notice requirements must be strictly complied with for coverage",
                "Policy exclusions are construed narrowly against the insurer"
            ]
        },
        {
            "case": "State v. Digital Dynamics",
            "court": "Texas Court of Appeals",
            "date": "2022-09-30",
            "judge": "Judge Williams",
            "case_type": "Regulatory",
            "relevance": "87%",
            "citations": 12,
            "precedential": False,
            "summary": "Regulatory enforcement action regarding data privacy compliance. Court addressed scope of state privacy law enforcement authority.",
            "key_holdings": [
                "State privacy laws can impose liability beyond federal requirements",
                "Corporate compliance programs receive deference in penalty calculations",
                "Voluntary disclosure of violations may reduce enforcement penalties"
            ]
        }
    ]
    
    # Filter and customize results based on search parameters
    filtered_results = []
    for result in base_results:
        if case_type != "All" and result["case_type"].lower() != case_type.lower():
            continue
        
        # Adjust relevance based on query content
        if query and any(term in result["summary"].lower() for term in query.lower().split()):
            result["relevance"] = f"{min(99, int(result['relevance'].rstrip('%')) + 2)}%"
        
        filtered_results.append(result)
    
    return filtered_results[:5]  # Return top 5 results

# Main execution
if __name__ == "__main__":
    show()
