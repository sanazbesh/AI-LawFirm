import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict

class BusinessIntelligence:
    def __init__(self):
        pass
    
    def generate_executive_dashboard(self) -> Dict:
        total_matters = len(st.session_state.matters)
        active_matters = len([m for m in st.session_state.matters if m.status == 'active'])
        total_docs = len(st.session_state.documents)
        total_revenue = sum(inv.total_amount for inv in st.session_state.invoices if inv.status == 'paid')
        
        return {
            'total_matters': total_matters,
            'active_matters': active_matters,
            'total_documents': total_docs,
            'total_revenue': total_revenue,
            'revenue_growth': 8.5,
            'avg_matter_value': total_revenue / total_matters if total_matters > 0 else 0,
            'utilization_rate': 78.5,
            'client_satisfaction': 4.2
        }
    
    def create_revenue_chart(self) -> go.Figure:
        months = pd.date_range(start='2024-01-01', periods=12, freq='M')
        revenue_data = [15000, 18000, 22000, 19000, 25000, 28000, 24000, 30000, 27000, 32000, 29000, 35000]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=revenue_data,
            mode='lines+markers',
            name='Monthly Revenue',
            line=dict(color='#2E86AB', width=3)
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
            marker_colors=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
        )])
        
        fig.update_layout(title='Matter Distribution by Type', height=400)
        return fig
