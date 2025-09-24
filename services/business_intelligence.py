import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import numpy as np

class BusinessIntelligence:
    def __init__(self):
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        
    def generate_executive_dashboard(self) -> Dict:
        """Generate key metrics for the executive dashboard."""
        # Get data from session state with fallbacks
        matters = getattr(st.session_state, 'matters', [])
        documents = getattr(st.session_state, 'documents', [])
        invoices = getattr(st.session_state, 'invoices', [])
        time_entries = getattr(st.session_state, 'time_entries', [])
        clients = getattr(st.session_state, 'clients', [])
        
        total_matters = len(matters)
        active_matters = len([m for m in matters if getattr(m, 'status', 'active') == 'active'])
        total_docs = len(documents)
        total_revenue = sum(getattr(inv, 'total_amount', 0) for inv in invoices if getattr(inv, 'status', '') == 'paid')
        
        # Calculate additional metrics
        total_billed = sum(getattr(inv, 'total_amount', 0) for inv in invoices)
        collection_rate = (total_revenue / total_billed * 100) if total_billed > 0 else 0
        
        # Calculate time-based metrics
        billable_hours = sum(getattr(entry, 'hours', 0) for entry in time_entries if getattr(entry, 'billable', False))
        total_hours = sum(getattr(entry, 'hours', 0) for entry in time_entries)
        utilization_rate = (billable_hours / total_hours * 100) if total_hours > 0 else 0
        
        return {
            'total_matters': total_matters,
            'active_matters': active_matters,
            'total_documents': total_docs,
            'total_revenue': total_revenue,
            'total_billed': total_billed,
            'revenue_growth': self._calculate_growth_rate('revenue'),
            'avg_matter_value': total_revenue / total_matters if total_matters > 0 else 0,
            'utilization_rate': utilization_rate,
            'collection_rate': collection_rate,
            'client_satisfaction': 4.2,  # Mock metric
            'active_clients': len([c for c in clients if getattr(c, 'status', 'active') == 'active']),
            'total_clients': len(clients),
            'billable_hours': billable_hours,
            'profit_margin': self._calculate_profit_margin()
        }
    
    def _calculate_growth_rate(self, metric_type: str) -> float:
        """Calculate growth rate for different metrics."""
        # Mock calculation - in real implementation would use historical data
        growth_rates = {
            'revenue': 8.5,
            'matters': 12.3,
            'clients': 6.7,
            'billable_hours': 4.2
        }
        return growth_rates.get(metric_type, 0.0)
    
    def _calculate_profit_margin(self) -> float:
        """Calculate profit margin."""
        # Mock calculation
        return 24.8
    
    def create_revenue_chart(self) -> go.Figure:
        """Create monthly revenue trend chart."""
        # Generate sample data for the past 12 months
        end_date = datetime.now().replace(day=1)
        start_date = end_date - timedelta(days=365)
        months = pd.date_range(start=start_date, end=end_date, freq='M')
        
        # Generate realistic revenue data with some variance
        base_revenue = 20000
        revenue_data = []
        for i, month in enumerate(months):
            # Add growth trend and seasonal variance
            growth_factor = 1 + (i * 0.02)  # 2% monthly growth
            seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * i / 12)  # Seasonal pattern
            variance = np.random.normal(0, 0.1)  # Random variance
            revenue = base_revenue * growth_factor * seasonal_factor * (1 + variance)
            revenue_data.append(max(revenue, 10000))  # Ensure minimum revenue
        
        fig = go.Figure()
        
        # Add revenue line
        fig.add_trace(go.Scatter(
            x=months,
            y=revenue_data,
            mode='lines+markers',
            name='Monthly Revenue',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=8)
        ))
        
        # Add trend line
        z = np.polyfit(range(len(revenue_data)), revenue_data, 1)
        trend_line = np.poly1d(z)(range(len(revenue_data)))
        
        fig.add_trace(go.Scatter(
            x=months,
            y=trend_line,
            mode='lines',
            name='Trend',
            line=dict(color='#FF6B6B', width=2, dash='dash'),
            opacity=0.7
        ))
        
        fig.update_layout(
            title='Monthly Revenue Trend (12 Months)',
            xaxis_title='Month',
            yaxis_title='Revenue ($)',
            template='plotly_white',
            height=400,
            showlegend=True,
            hovermode='x unified'
        )
        
        return fig
    
    def create_matter_type_distribution(self) -> go.Figure:
        """Create matter type distribution pie chart."""
        matters = getattr(st.session_state, 'matters', [])
        
        if matters:
            matter_types = {}
            for matter in matters:
                matter_type = getattr(matter, 'matter_type', 'other').replace('_', ' ').title()
                matter_types[matter_type] = matter_types.get(matter_type, 0) + 1
        else:
            # Sample data for demo
            matter_types = {
                'Corporate': 8,
                'Litigation': 6,
                'Family Law': 4,
                'Real Estate': 3,
                'Employment': 5,
                'Intellectual Property': 2
            }
        
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#24A148', '#8E44AD']
        
        fig = go.Figure(data=[go.Pie(
            labels=list(matter_types.keys()),
            values=list(matter_types.values()),
            hole=0.4,
            marker_colors=colors[:len(matter_types)],
            textinfo='label+percent',
            textposition='auto'
        )])
        
        fig.update_layout(
            title='Matter Distribution by Practice Area',
            height=400,
            showlegend=True
        )
        
        return fig
    
    def create_attorney_performance_chart(self) -> go.Figure:
        """Create attorney performance comparison chart."""
        # Sample attorney data
        attorneys = [
            {'name': 'John Partner', 'billable_hours': 180, 'revenue': 45000, 'matters': 8},
            {'name': 'Sarah Associate', 'billable_hours': 165, 'revenue': 33000, 'matters': 12},
            {'name': 'Mike Davis', 'billable_hours': 142, 'revenue': 28400, 'matters': 6},
            {'name': 'Emily Chen', 'billable_hours': 156, 'revenue': 31200, 'matters': 9},
            {'name': 'David Wilson', 'billable_hours': 138, 'revenue': 27600, 'matters': 7}
        ]
        
        names = [a['name'] for a in attorneys]
        hours = [a['billable_hours'] for a in attorneys]
        revenue = [a['revenue'] for a in attorneys]
        
        fig = go.Figure()
        
        # Add billable hours bars
        fig.add_trace(go.Bar(
            name='Billable Hours',
            x=names,
            y=hours,
            yaxis='y',
            marker_color='#2E86AB',
            text=hours,
            textposition='auto'
        ))
        
        # Add revenue line on secondary y-axis
        fig.add_trace(go.Scatter(
            name='Revenue ($)',
            x=names,
            y=revenue,
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='#A23B72', width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title='Attorney Performance - Billable Hours vs Revenue',
            xaxis=dict(title='Attorney'),
            yaxis=dict(title='Billable Hours', side='left'),
            yaxis2=dict(title='Revenue ($)', side='right', overlaying='y'),
            template='plotly_white',
            height=400,
            showlegend=True
        )
        
        return fig
    
    def create_collection_analysis_chart(self) -> go.Figure:
        """Create accounts receivable aging analysis."""
        # Sample aging data
        aging_buckets = ['Current', '1-30 Days', '31-60 Days', '61-90 Days', '90+ Days']
        amounts = [45000, 12000, 8000, 5000, 3000]
        colors = ['#24A148', '#F18F01', '#FF9800', '#FF5722', '#C73E1D']
        
        fig = go.Figure(data=[go.Bar(
            x=aging_buckets,
            y=amounts,
            marker_color=colors,
            text=[f'${amount:,.0f}' for amount in amounts],
            textposition='auto'
        )])
        
        fig.update_layout(
            title='Accounts Receivable Aging Analysis',
            xaxis_title='Age of Receivables',
            yaxis_title='Amount ($)',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def create_client_acquisition_chart(self) -> go.Figure:
        """Create client acquisition and retention chart."""
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        new_clients = [3, 5, 2, 4, 6, 3]
        lost_clients = [1, 0, 2, 1, 1, 0]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='New Clients',
            x=months,
            y=new_clients,
            marker_color='#24A148',
            text=new_clients,
            textposition='auto'
        ))
        
        fig.add_trace(go.Bar(
            name='Lost Clients',
            x=months,
            y=[-x for x in lost_clients],  # Negative values for visual distinction
            marker_color='#C73E1D',
            text=lost_clients,
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Client Acquisition vs Attrition (6 Months)',
            xaxis_title='Month',
            yaxis_title='Number of Clients',
            template='plotly_white',
            height=400,
            showlegend=True
        )
        
        return fig
    
    def create_profitability_analysis(self) -> go.Figure:
        """Create matter profitability analysis."""
        matters_data = [
            {'name': 'ABC Corp Merger', 'revenue': 85000, 'costs': 15000, 'hours': 340},
            {'name': 'Patent Defense', 'revenue': 45000, 'costs': 8000, 'hours': 180},
            {'name': 'Employment Dispute', 'revenue': 32000, 'costs': 5000, 'hours': 128},
            {'name': 'Real Estate Deal', 'revenue': 28000, 'costs': 4000, 'hours': 112},
            {'name': 'Contract Review', 'revenue': 15000, 'costs': 2000, 'hours': 60}
        ]
        
        names = [m['name'] for m in matters_data]
        profit = [m['revenue'] - m['costs'] for m in matters_data]
        profit_margin = [(m['revenue'] - m['costs']) / m['revenue'] * 100 for m in matters_data]
        
        fig = go.Figure()
        
        # Profit bars
        fig.add_trace(go.Bar(
            name='Profit ($)',
            x=names,
            y=profit,
            yaxis='y',
            marker_color='#2E86AB',
            text=[f'${p:,.0f}' for p in profit],
            textposition='auto'
        ))
        
        # Profit margin line
        fig.add_trace(go.Scatter(
            name='Profit Margin (%)',
            x=names,
            y=profit_margin,
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='#A23B72', width=3),
            marker=dict(size=10),
            text=[f'{pm:.1f}%' for pm in profit_margin],
            textposition='top center'
        ))
        
        fig.update_layout(
            title='Matter Profitability Analysis',
            xaxis=dict(title='Matter', tickangle=45),
            yaxis=dict(title='Profit ($)', side='left'),
            yaxis2=dict(title='Profit Margin (%)', side='right', overlaying='y'),
            template='plotly_white',
            height=400,
            showlegend=True
        )
        
        return fig
    
    def generate_kpi_summary(self) -> Dict[str, Any]:
        """Generate key performance indicators summary."""
        dashboard_data = self.generate_executive_dashboard()
        
        return {
            'financial_kpis': {
                'total_revenue': dashboard_data['total_revenue'],
                'revenue_growth': dashboard_data['revenue_growth'],
                'collection_rate': dashboard_data['collection_rate'],
                'profit_margin': dashboard_data['profit_margin'],
                'avg_matter_value': dashboard_data['avg_matter_value']
            },
            'operational_kpis': {
                'utilization_rate': dashboard_data['utilization_rate'],
                'billable_hours': dashboard_data['billable_hours'],
                'active_matters': dashboard_data['active_matters'],
                'total_matters': dashboard_data['total_matters'],
                'matter_completion_rate': 85.2  # Mock metric
            },
            'client_kpis': {
                'total_clients': dashboard_data['total_clients'],
                'active_clients': dashboard_data['active_clients'],
                'client_satisfaction': dashboard_data['client_satisfaction'],
                'client_retention_rate': 94.5,  # Mock metric
                'referral_rate': 23.8  # Mock metric
            }
        }
    
    def create_trend_analysis(self, metric: str, period: str = '12M') -> go.Figure:
        """Create trend analysis for specific metrics."""
        # Generate time series data based on period
        if period == '12M':
            periods = 12
            freq = 'M'
            title_period = '12 Months'
        elif period == '6M':
            periods = 6
            freq = 'M'
            title_period = '6 Months'
        else:  # 3M
            periods = 3
            freq = 'M'
            title_period = '3 Months'
        
        dates = pd.date_range(end=datetime.now(), periods=periods, freq=freq)
        
        # Generate sample data based on metric type
        base_values = {
            'revenue': 25000,
            'utilization': 75,
            'collection_rate': 92,
            'new_clients': 4
        }
        
        base_value = base_values.get(metric, 100)
        trend_data = []
        
        for i in range(periods):
            # Add trend and variance
            trend = base_value * (1 + i * 0.02)  # 2% growth
            variance = np.random.normal(0, base_value * 0.05)  # 5% variance
            trend_data.append(max(trend + variance, 0))
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=trend_data,
            mode='lines+markers',
            name=metric.replace('_', ' ').title(),
            line=dict(width=3),
            marker=dict(size=8)
        ))
        
        # Add trend line
        z = np.polyfit(range(len(trend_data)), trend_data, 1)
        trend_line = np.poly1d(z)(range(len(trend_data)))
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=trend_line,
            mode='lines',
            name='Trend',
            line=dict(dash='dash', width=2),
            opacity=0.7
        ))
        
        fig.update_layout(
            title=f'{metric.replace("_", " ").title()} Trend Analysis ({title_period})',
            xaxis_title='Period',
            yaxis_title=metric.replace('_', ' ').title(),
            template='plotly_white',
            height=400,
            showlegend=True
        )
        
        return fig
    
    def generate_comparative_analysis(self) -> Dict[str, Any]:
        """Generate comparative analysis against benchmarks."""
        current_metrics = self.generate_executive_dashboard()
        
        # Industry benchmarks (mock data)
        benchmarks = {
            'utilization_rate': 75.0,
            'collection_rate': 90.0,
            'profit_margin': 20.0,
            'client_satisfaction': 4.0,
            'revenue_per_attorney': 400000
        }
        
        comparisons = {}
        for metric, benchmark in benchmarks.items():
            current_value = current_metrics.get(metric, 0)
            variance = ((current_value - benchmark) / benchmark * 100) if benchmark > 0 else 0
            
            comparisons[metric] = {
                'current': current_value,
                'benchmark': benchmark,
                'variance_percent': variance,
                'performance': 'Above' if variance > 0 else 'Below' if variance < 0 else 'At',
                'status': 'good' if variance >= 0 else 'warning' if variance >= -10 else 'poor'
            }
        
        return comparisons
    
    def create_forecasting_chart(self, metric: str) -> go.Figure:
        """Create forecasting chart for business metrics."""
        # Historical data (12 months)
        historical_dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
        
        # Generate historical data
        base_value = {'revenue': 25000, 'matters': 15, 'clients': 45}.get(metric, 100)
        historical_data = []
        
        for i in range(12):
            trend = base_value * (1 + i * 0.015)  # 1.5% monthly growth
            variance = np.random.normal(0, base_value * 0.1)
            historical_data.append(max(trend + variance, base_value * 0.5))
        
        # Forecast data (6 months forward)
        forecast_dates = pd.date_range(start=datetime.now() + timedelta(days=30), periods=6, freq='M')
        
        # Simple linear forecast
        z = np.polyfit(range(len(historical_data)), historical_data, 1)
        forecast_trend = np.poly1d(z)
        forecast_data = [forecast_trend(12 + i) for i in range(6)]
        
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=historical_dates,
            y=historical_data,
            mode='lines+markers',
            name='Historical',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=8)
        ))
        
        # Forecast data
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_data,
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#FF6B6B', width=3, dash='dash'),
            marker=dict(size=8)
        ))
        
        # Confidence interval
        upper_bound = [f * 1.1 for f in forecast_data]
        lower_bound = [f * 0.9 for f in forecast_data]
        
        fig.add_trace(go.Scatter(
            x=list(forecast_dates) + list(forecast_dates)[::-1],
            y=upper_bound + lower_bound[::-1],
            fill='toself',
            fillcolor='rgba(255, 107, 107, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Confidence Interval',
            showlegend=True
        ))
        
        fig.update_layout(
            title=f'{metric.replace("_", " ").title()} Forecast (6 Months)',
            xaxis_title='Period',
            yaxis_title=metric.replace('_', ' ').title(),
            template='plotly_white',
            height=400,
            showlegend=True
        )
        
        return fig
    
    def export_analytics_report(self, format_type: str = 'summary') -> Dict[str, Any]:
        """Export comprehensive analytics report."""
        dashboard_data = self.generate_executive_dashboard()
        kpi_data = self.generate_kpi_summary()
        comparative_data = self.generate_comparative_analysis()
        
        report = {
            'report_date': datetime.now().isoformat(),
            'report_type': format_type,
            'executive_summary': dashboard_data,
            'key_performance_indicators': kpi_data,
            'benchmark_comparison': comparative_data,
            'recommendations': self._generate_recommendations(dashboard_data, comparative_data)
        }
        
        return report
    
    def _generate_recommendations(self, dashboard_data: Dict, comparative_data: Dict) -> List[Dict]:
        """Generate business recommendations based on analytics."""
        recommendations = []
        
        # Revenue recommendations
        if dashboard_data['revenue_growth'] < 10:
            recommendations.append({
                'category': 'Revenue',
                'priority': 'High',
                'recommendation': 'Consider implementing value-based billing or increasing hourly rates',
                'expected_impact': 'Potential 15-20% revenue increase'
            })
        
        # Utilization recommendations
        if dashboard_data['utilization_rate'] < 75:
            recommendations.append({
                'category': 'Operations',
                'priority': 'Medium',
                'recommendation': 'Focus on improving attorney utilization through better resource allocation',
                'expected_impact': 'Improved profitability and efficiency'
            })
        
        # Collection recommendations
        if dashboard_data['collection_rate'] < 90:
            recommendations.append({
                'category': 'Financial',
                'priority': 'High',
                'recommendation': 'Implement stricter collection procedures and consider offering payment plans',
                'expected_impact': 'Improved cash flow and reduced bad debt'
            })
        
        return recommendations
