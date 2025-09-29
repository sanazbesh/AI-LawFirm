import streamlit as st
import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main {
        font-family: 'Inter', sans-serif;
        padding: 0 !important;
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 100% !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2E86AB 0%, #A23B72 100%);
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] .css-17eq0hr {
        color: white !important;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar buttons */
    [data-testid="stSidebar"] button {
        background: rgba(255,255,255,0.15) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        width: 100% !important;
        text-align: left !important;
        transition: all 0.3s ease !important;
        margin-bottom: 0.5rem !important;
    }
    /* Better sidebar styling */
    [data-testid="stSidebar"] .element-container {
        padding: 0.25rem 0 !important;
    }
    
    [data-testid="stSidebar"] p {
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        color: rgba(255,255,255,0.95) !important;
        padding: 0.75rem 1rem !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    
    [data-testid="stSidebar"] p:hover {
        background: rgba(255,255,255,0.15) !important;
        transform: translateX(5px) scale(1.05) !important;
        color: white !important;
    }
    [data-testid="stSidebar"] button:hover {
        background: rgba(255,255,255,0.25) !important;
        transform: translateX(5px);
    }
    
    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(46, 134, 171, 0.3);
        animation: slideDown 0.5s ease;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 18px;
        border-left: 5px solid #2E86AB;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    
    /* Streamlit metrics enhancement */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #2E86AB !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #666 !important;
    }
    
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        padding: 2rem;
        border-radius: 18px;
        box-shadow: 0 8px 25px rgba(46, 134, 171, 0.3);
    }
    
    [data-testid="metric-container"] > div {
        color: white !important;
    }
    
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: white !important;
    }
    
    /* Document card */
    .document-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        margin: 1.5rem 0;
        border-left: 5px solid #2E86AB;
        transition: all 0.3s ease;
    }
    
    .document-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .document-card h4 {
        color: #2E86AB;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    
    /* Matter card */
    .matter-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2.5rem;
        border-radius: 18px;
        border: 2px solid #e9ecef;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .matter-card:hover {
        border-color: #2E86AB;
        box-shadow: 0 12px 35px rgba(0,0,0,0.12);
    }
    
    /* Status badges */
    .status-badge {
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
    }
    
    .status-active { background-color: #28a745; color: white; }
    .status-pending { background-color: #ffc107; color: #212529; }
    .status-draft { background-color: #6c757d; color: white; }
    .status-review { background-color: #17a2b8; color: white; }
    .status-final { background-color: #28a745; color: white; }
    
    /* AI insight cards */
    .ai-insight {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196f3;
        border-radius: 18px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    
    .ai-insight:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(33, 150, 243, 0.3);
    }
    
    /* Client portal cards */
    .client-portal {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        border: 2px solid #9c27b0;
        border-radius: 18px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    
    .client-portal:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(156, 39, 176, 0.3);
    }
    
    /* Integration cards */
    .integration-card {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 18px;
        padding: 2rem;
        margin: 1.5rem 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .integration-card:hover {
        border-color: #2E86AB;
        box-shadow: 0 10px 30px rgba(46, 134, 171, 0.2);
        transform: translateY(-3px);
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #2E86AB, #A23B72) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(46, 134, 171, 0.3) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(46, 134, 171, 0.4) !important;
    }
    
    /* Input fields */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        border: 2px solid #e9ecef !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
        border-color: #2E86AB !important;
        box-shadow: 0 0 0 3px rgba(46, 134, 171, 0.1) !important;
    }
    
    /* Data tables */
    .dataframe {
        border: none !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #2E86AB, #A23B72) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 1rem !important;
    }
    
    .dataframe tbody tr:hover {
        background: #f8f9fa !important;
    }
    
    /* Mobile frame */
    .mobile-frame {
        width: 300px;
        height: 600px;
        background: #000;
        border-radius: 30px;
        padding: 20px;
        margin: 2rem auto;
        position: relative;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    }
    
    .mobile-screen {
        width: 100%;
        height: 100%;
        background: white;
        border-radius: 25px;
        overflow: hidden;
        position: relative;
    }
    
    /* Animations */
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(46, 134, 171, 0.1);
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #2E86AB;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2E86AB, #A23B72);
        color: white;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border-radius: 12px;
        font-weight: 600;
        color: #2E86AB;
    }
    
    /* Success/Error/Warning boxes */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        border-left: 5px solid !important;
    }
</style>
""", unsafe_allow_html=True)

# Import services with error handling
try:
    from services.subscription_manager import EnhancedAuthService as AuthService
except ImportError:
    st.error("Authentication service not found. Please check the services/auth.py file.")
    st.stop()

try:
    from session_manager import initialize_session_state, load_sample_data
except ImportError:
    st.error("Session manager not found. Please check the session_manager.py file.")
    st.stop()

# Import pages with fallbacks
def safe_import_page(page_name, module_path):
    """Safely import a page module with fallback"""
    try:
        module = __import__(module_path, fromlist=[page_name])
        return getattr(module, 'show', lambda: st.error(f"Page {page_name} show function not found"))
    except ImportError:
        return lambda: show_placeholder_page(page_name)
    except Exception as e:
        return lambda: st.error(f"Error loading {page_name}: {str(e)}")

def show_placeholder_page(page_name):
    """Show a placeholder page when the actual page is not available"""
    st.markdown(f"""
    <div class="main-header">
        <h1>{page_name}</h1>
        <p>This page is under development</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info(f"The {page_name} page is being developed. Please check back later.")
    
    if page_name == "Executive Dashboard":
        show_basic_dashboard()

def show_basic_dashboard():
    """Basic dashboard fallback"""
    st.subheader("📊 Basic Dashboard")
    
    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Matters", len(st.session_state.get('matters', [])))
    with col2:
        st.metric("Total Documents", len(st.session_state.get('documents', [])))
    with col3:
        st.metric("Active Clients", len(st.session_state.get('clients', [])))
    with col4:
        st.metric("Pending Tasks", len(st.session_state.get('tasks', [])))
    
    # Recent activity
    st.subheader("Recent Activity")
    recent_items = [
        "Document uploaded: Merger Agreement v2.1",
        "Matter created: Johnson Custody Case",
        "Invoice generated: INV-2024-001",
        "Client portal access granted",
        "Calendar event scheduled"
    ]
    
    for item in recent_items:
        st.write(f"• {item}")

# Try to import pages, with fallbacks
page_modules = {
    "Executive Dashboard": safe_import_page("dashboard", "pages.dashboard"),
    "Document Management": safe_import_page("documents", "pages.documents"), 
    "Matter Management": safe_import_page("matters", "pages.matters"),
    "Time & Billing": safe_import_page("billing", "pages.time_billing"),
    "AI Insights": safe_import_page("ai_insights", "pages.ai_insights"),
    "Calendar & Tasks": safe_import_page("calendar_tasks", "pages.calendar_tasks"),
    "Advanced Search": safe_import_page("advanced_search", "pages.advanced_search"),
    "Integrations": safe_import_page("integrations", "pages.integrations"),
    "Mobile App": safe_import_page("mobile_app", "pages.mobile_app"),
    "Business Intelligence": safe_import_page("business_intel", "pages.business_intelligence"),
    "Client Portal Management": safe_import_page("client_portal", "pages.client_portal"),
    "System Settings": safe_import_page("settings", "pages.system_settings"),
    "Client Dashboard": safe_import_page("client_dashboard", "pages.client_dashboard"),
    "My Documents": safe_import_page("my_documents", "pages.my_documents"),
    "Billing": safe_import_page("billing_view", "pages.billing_view"),
    "Messages": safe_import_page("messages", "pages.messages")
}

def main():
    """Main application function"""
    try:
        # Initialize session state and load data
        initialize_session_state()
        load_sample_data()
        
        # Initialize authentication service
        auth_service = AuthService()
        
        # Check authentication
        if not auth_service.is_logged_in():
            auth_service.show_login()
            return
        
        # Add styling for logged-in pages
        st.markdown("""
        <style>
        .stApp {
            background: #0f172a !important;
            min-height: 100vh;
        }
        .main .block-container {
            background: #1e293b !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
            border: 1px solid #334155 !important;
        }
        
        /* Make all text readable on dark background */
        .main .block-container * {
            color: #e2e8f0 !important;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #f1f5f9 !important;
        }
        
        /* Metric values and labels - high contrast */
        [data-testid="stMetricValue"] {
            color: #60a5fa !important;
        }
        
        [data-testid="stMetricLabel"] {
            color: #cbd5e1 !important;
        }
        
        /* Chart backgrounds - light for readability */
        .js-plotly-plot, .plotly {
            background: #ffffff !important;
        }
        
        .js-plotly-plot .plotly .main-svg {
            background: #ffffff !important;
        }
        
        /* Table styling */
        .dataframe {
            background: #1e293b !important;
            color: #e2e8f0 !important;
        }
        
        .dataframe th {
            background: #334155 !important;
            color: #f1f5f9 !important;
        }
        
        .dataframe td {
            background: #1e293b !important;
            color: #e2e8f0 !important;
            border-color: #334155 !important;
        }
        
        /* Input fields */
        .stTextInput input, .stSelectbox select, .stTextArea textarea {
            background: #334155 !important;
            color: #e2e8f0 !important;
            border-color: #475569 !important;
        }
        
        /* Top accent bar */
        .main .block-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3b82f6 0%, #06b6d4 100%);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Render sidebar
        auth_service.render_sidebar()
        
        # Get current page from session state
        current_page = st.session_state.get('current_page', 'Executive Dashboard')
        
        # Handle user settings modal
        if st.session_state.get('show_user_settings', False):
            auth_service.show_user_settings()
        
        # Route to appropriate page
        if current_page in page_modules:
            try:
                page_modules[current_page]()
            except Exception as e:
                st.error(f"Error loading {current_page}: {str(e)}")
                st.markdown("### Troubleshooting")
                st.write("This error occurred while loading the page. Common causes:")
                st.write("• Missing page module file")
                st.write("• Import error in page module")
                st.write("• Missing dependencies")
                
                if st.button("🏠 Return to Dashboard"):
                    st.session_state['current_page'] = 'Executive Dashboard'
                    st.rerun()
        else:
            st.error(f"Page '{current_page}' not found")
            available_pages = list(page_modules.keys())
            st.write("Available pages:", ", ".join(available_pages))
            
            if st.button("🏠 Go to Dashboard"):
                st.session_state['current_page'] = 'Executive Dashboard'
                st.rerun()
    
    except Exception as e:
        st.error("Application Error")
        st.write(f"An error occurred: {str(e)}")
        
        # Show debugging information
        with st.expander("🔧 Debug Information"):
            st.write("**Session State Keys:**")
            st.write(list(st.session_state.keys()))
            
            st.write("**Python Path:**")
            for path in sys.path:
                st.write(f"• {path}")
            
            st.write("**Current Directory:**")
            st.write(os.getcwd())
            
            st.write("**Available Files:**")
            try:
                files = os.listdir('.')
                for file in sorted(files):
                    st.write(f"• {file}")
            except:
                st.write("Could not list files")

def show_system_status():
    """Show system status in sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.markdown("**System Status**")
        st.success("🟢 All Systems Operational")
        st.write(f"**Last Updated:** {datetime.now().strftime('%H:%M:%S')}")
        
        # Show session stats if available
        try:
            stats = {
                'clients': len(st.session_state.get('clients', [])),
                'matters': len(st.session_state.get('matters', [])),
                'documents': len(st.session_state.get('documents', []))
            }
            
            st.markdown("**Quick Stats**")
            for key, value in stats.items():
                st.write(f"• {key.title()}: {value}")
        except:
            pass

def load_config():
    """Load configuration with fallback defaults"""
    return {
        'app_name': 'LegalDoc Pro',
        'version': '1.0.0',
        'debug': False,
        'theme': 'light'
    }

def handle_error(error, context="Application"):
    """Centralized error handling"""
    st.error(f"{context} Error: {str(error)}")
    
    with st.expander("Error Details"):
        st.code(str(error))
        
    if st.button("🔄 Reload Application"):
        st.rerun()

# Add system status to sidebar
if __name__ == "__main__":
    try:
        main()
        show_system_status()
    except Exception as e:
        handle_error(e, "Main Application")
        
        # Fallback - show basic interface
        st.markdown("""
        <div class="main-header">
            <h1>⚖️ LegalDoc Pro</h1>
            <p>Enterprise Legal Management Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.error("The application encountered an error during startup.")
        st.info("Please ensure all required files are present and properly configured.")
        
        if st.button("🔄 Try Again"):
            st.rerun()
        
        st.error("The application encountered an error during startup.")
        st.info("Please ensure all required files are present and properly configured.")
        
        if st.button("🔄 Try Again"):
            st.rerun()
