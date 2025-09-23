import streamlit as st
from config import load_config
from services.auth import AuthService
from utils.helpers import initialize_session_state, load_sample_data
from pages import (
    dashboard, documents, matters, billing, ai_insights,
    calendar_tasks, advanced_search, integrations, mobile_app,
    business_intel, client_portal, settings
)

# Configure Streamlit
st.set_page_config(
    page_title="LegalDoc Pro - Enterprise Legal Management",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
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
</style>
""", unsafe_allow_html=True)

# Initialize
initialize_session_state()
load_sample_data()
auth_service = AuthService()

# Check authentication
if not auth_service.is_logged_in():
    auth_service.show_login()
    st.stop()

# Sidebar
auth_service.render_sidebar()

# Get navigation
page = st.session_state.get('current_page', 'Executive Dashboard')

# Route to pages
page_mapping = {
    "Executive Dashboard": dashboard.show,
    "Document Management": documents.show,
    "Matter Management": matters.show,
    "Time & Billing": billing.show,
    "AI Insights": ai_insights.show,
    "Calendar & Tasks": calendar_tasks.show,
    "Advanced Search": advanced_search.show,
    "Integrations": integrations.show,
    "Mobile App": mobile_app.show,
    "Business Intelligence": business_intel.show,
    "Client Dashboard": client_portal.show,
    "System Settings": settings.show
}

if page in page_mapping:
    page_mapping[page]()
else:
    st.error(f"Page '{page}' not found")
