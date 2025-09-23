import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def show():
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
        
        fig = px.bar(doc_data, x='Document Type', y='Count', 
                    color='AI Confidence', color_continuous_scale='viridis',
                    title="Document Classification Results")
        st.plotly_chart(fig, use_container_width=True)
        
        # Sentiment analysis
        st.markdown("#### Document Sentiment Analysis")
        sentiment_data = pd.DataFrame({
            'Sentiment': ['Positive', 'Neutral', 'Negative'],
            'Count': [234, 312, 70],
            'Percentage': [38.0, 50.6, 11.4]
        })
        
        fig2 = px.pie(sentiment_data, values='Count', names='Sentiment',
                     color_discrete_sequence=['#2E8B57', '#FFD700', '#DC143C'],
                     title="Overall Document Sentiment Distribution")
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
        actions = [
            "✅ Classified 15 new contracts",
            "🔍 Extracted key terms from merger agreement",
            "⚠️ Flagged potential compliance issue",
            "📊 Updated risk assessment models",
            "🤖 Enhanced NLP algorithms"
        ]
        
        for action in actions:
            st.write(action)

def show_predictive_analytics():
    st.subheader("📈 Predictive Analytics Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Case Outcome Predictions")
        
        # Generate prediction data
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        predictions = pd.DataFrame({
            'Month': dates,
            'Win Probability': [random.uniform(0.6, 0.9) for _ in dates],
            'Settlement Probability': [random.uniform(0.3, 0.7) for _ in dates],
            'Cost Prediction': [random.uniform(50000, 200000) for _ in dates]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=predictions['Month'], y=predictions['Win Probability'],
                                mode='lines+markers', name='Win Probability',
                                line=dict(color='green', width=3)))
        fig.add_trace(go.Scatter(x=predictions['Month'], y=predictions['Settlement Probability'],
                                mode='lines+markers', name='Settlement Probability',
                                line=dict(color='orange', width=3)))
        
        fig.update_layout(title='Case Outcome Predictions Over Time',
                         xaxis_title='Month', yaxis_title='Probability')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Litigation Timeline Prediction")
        timeline_data = pd.DataFrame({
            'Phase': ['Discovery', 'Motions', 'Trial Prep', 'Trial', 'Appeal'],
            'Predicted Duration (Months)': [4.2, 2.1, 3.8, 1.2, 8.5],
            'Confidence': [89, 92, 87, 91, 76]
        })
        
        fig2 = px.bar(timeline_data, x='Phase', y='Predicted Duration (Months)',
                     color='Confidence', color_continuous_scale='RdYlGn',
                     title="Litigation Phase Duration Predictions")
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("#### Budget Forecasting")
        
        # Budget prediction
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        actual = [45000, 52000, 48000, 61000, 59000, 67000]
        predicted = [46000, 53000, 49000, 62000, 60000, 68000]
        
        budget_df = pd.DataFrame({
            'Month': months * 2,
            'Amount': actual + predicted,
            'Type': ['Actual'] * 6 + ['Predicted'] * 6
        })
        
        fig3 = px.line(budget_df, x='Month', y='Amount', color='Type',
                      title='Budget Forecast vs Actual')
        st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown("#### AI Recommendations")
        recommendations = [
            "🎯 Focus on settlement negotiations for Case #2024-107",
            "⏰ Expedite discovery phase for optimal timeline",
            "💰 Budget increase of 15% recommended for Q4",
            "📋 Additional resources needed for complex litigation",
            "🤝 Consider mediation for cost reduction"
        ]
        
        for rec in recommendations:
            st.info(rec)

def show_risk_assessment():
    st.subheader("🎯 AI-Powered Risk Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Overall Risk Score")
        
        # Risk gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = 73,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Risk Level"},
            delta = {'reference': 80},
            gauge = {'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps' : [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"}],
                    'threshold' : {'line': {'color': "red", 'width': 4},
                                  'thickness': 0.75, 'value': 90}}))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Risk Categories")
        
        risk_categories = pd.DataFrame({
            'Category': ['Compliance', 'Financial', 'Operational', 'Reputational', 'Strategic'],
            'Risk Score': [85, 67, 72, 43, 59],
            'Trend': ['↗️', '↘️', '→', '↘️', '↗️']
        })
        
        fig2 = px.bar(risk_categories, x='Category', y='Risk Score',
                     color='Risk Score', color_continuous_scale='Reds',
                     title='Risk by Category')
        st.plotly_chart(fig2, use_container_width=True)
    
    with col3:
        st.markdown("#### Risk Alerts")
        
        alerts = [
            ("🔴 High", "Regulatory compliance gap detected"),
            ("🟡 Medium", "Contract renewal deadline approaching"),
            ("🔴 High", "Litigation exposure increased"),
            ("🟡 Medium", "Staff capacity constraint"),
            ("🟢 Low", "Insurance coverage adequate")
        ]
        
        for severity, alert in alerts:
            if "High" in severity:
                st.error(f"{severity}: {alert}")
            elif "Medium" in severity:
                st.warning(f"{severity}: {alert}")
            else:
                st.success(f"{severity}: {alert}")

def show_contract_intelligence():
    st.subheader("📝 AI Contract Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Contract Analysis Results")
        
        # Contract metrics
        contract_metrics = pd.DataFrame({
            'Metric': ['Total Contracts', 'AI-Reviewed', 'Anomalies Detected', 'Key Terms Extracted'],
            'Count': [1247, 1180, 67, 5890],
            'Accuracy': [100, 94.6, 89.2, 97.1]
        })
        
        fig = px.bar(contract_metrics, x='Metric', y='Count',
                    color='Accuracy', color_continuous_scale='Blues',
                    title='Contract Processing Statistics')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Key Terms Analysis")
        
        terms_data = pd.DataFrame({
            'Term Type': ['Payment Terms', 'Termination Clauses', 'Liability Limits', 'Renewal Options', 'IP Rights'],
            'Frequency': [432, 387, 295, 234, 189],
            'Risk Level': ['Low', 'Medium', 'High', 'Medium', 'High']
        })
        
        color_map = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}
        fig2 = px.scatter(terms_data, x='Term Type', y='Frequency',
                         color='Risk Level', color_discrete_map=color_map,
                         size='Frequency', title='Contract Terms by Risk Level')
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("#### Contract Health Score")
        
        health_score = 87.3
        fig3 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = health_score,
            title = {'text': "Contract Portfolio Health"},
            gauge = {'axis': {'range': [None, 100]},
                    'bar': {'color': "green"},
                    'steps': [{'range': [0, 60], 'color': "lightgray"},
                             {'range': [60, 90], 'color': "gray"}],
                    'threshold': {'line': {'color': "red", 'width': 4},
                                'thickness': 0.75, 'value': 90}}))
        st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown("#### AI Insights")
        insights = [
            "📋 15 contracts require renewal within 90 days",
            "⚠️ 3 contracts have unusual termination clauses",
            "💰 Potential cost savings of $2.3M identified",
            "🔍 5 contracts missing standard IP protection",
            "📊 Average contract value increased 12% YoY"
        ]
        
        for insight in insights:
            st.info(insight)

def show_case_law_research():
    st.subheader("⚖️ AI Case Law Research Assistant")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### Research Query")
        
        # Search interface
        search_query = st.text_input("Enter your legal research query:", 
                                   placeholder="e.g., contract disputes intellectual property")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            jurisdiction = st.selectbox("Jurisdiction:", ["Federal", "State", "International"])
        with col_b:
            case_type = st.selectbox("Case Type:", ["All", "Civil", "Criminal", "Administrative"])
        with col_c:
            date_range = st.selectbox("Date Range:", ["Last 5 years", "Last 10 years", "All time"])
        
        if st.button("🔍 Search Case Law"):
            st.markdown("#### Search Results")
            
            # Mock search results
            results = [
                {
                    "case": "Smith v. ABC Corp",
                    "court": "9th Circuit Court of Appeals",
                    "year": "2023",
                    "relevance": "96%",
                    "summary": "Contract interpretation regarding intellectual property rights..."
                },
                {
                    "case": "Johnson Industries v. Tech Solutions",
                    "court": "Federal District Court",
                    "year": "2022",
                    "relevance": "94%",
                    "summary": "Licensing agreement dispute with similar fact pattern..."
                },
                {
                    "case": "Continental Corp v. Innovation LLC",
                    "court": "State Supreme Court",
                    "year": "2021",
                    "relevance": "89%",
                    "summary": "Trade secret misappropriation in technology sector..."
                }
            ]
            
            for i, result in enumerate(results, 1):
                with st.expander(f"{i}. {result['case']} ({result['relevance']} relevant)"):
                    st.write(f"**Court:** {result['court']}")
                    st.write(f"**Year:** {result['year']}")
                    st.write(f"**Summary:** {result['summary']}")
                    
                    col_x, col_y = st.columns(2)
                    with col_x:
                        st.button(f"📄 View Full Text", key=f"view_{i}")
                    with col_y:
                        st.button(f"📎 Add to Brief", key=f"add_{i}")
    
    with col2:
        st.markdown("#### Research Analytics")
        
        # Research metrics
        metrics = [
            ("Cases Analyzed", "147K"),
            ("Search Accuracy", "94.7%"),
            ("Avg. Research Time", "12 min"),
            ("Citations Generated", "2,347")
        ]
        
        for label, value in metrics:
            st.metric(label, value)
        
        st.markdown("#### Recent Searches")
        recent = [
            "Contract interpretation",
            "IP licensing disputes",
            "Employment law updates",
            "Corporate governance",
            "Tax regulation changes"
        ]
        
        for search in recent:
            st.write(f"• {search}")
        
        st.markdown("#### Quick Actions")
        if st.button("📚 Legal Research Library"):
            st.info("Opening research library...")
        if st.button("📊 Citation Analytics"):
            st.info("Loading citation analysis...")
        if st.button("🤖 AI Legal Assistant"):
            st.info("Activating AI assistant...")
