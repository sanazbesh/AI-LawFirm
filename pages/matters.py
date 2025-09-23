import streamlit as st
import uuid
from datetime import datetime
from services.auth import AuthService
from models.matter import Matter, MatterType

def show():
    auth_service = AuthService()
    
    st.title("Matter Management")
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_matters = len([m for m in st.session_state.matters if m.status == 'active'])
        st.metric("Active Matters", active_matters)
    
    with col2:
        total_docs = len(st.session_state.documents)
        st.metric("Total Documents", total_docs)
    
    with col3:
        st.metric("Total Revenue", "$125,000")
    
    with col4:
        st.metric("Avg. Matter Value", "$25,000")
    
    st.divider()
    
    # Create new matter
    if auth_service.has_permission('write'):
        _show_create_matter_form(auth_service)
        st.divider()
    
    # Matter list
    _show_matter_list(auth_service)

def _show_create_matter_form(auth_service):
    st.subheader("Create New Matter")
    
    with st.form("new_matter_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            matter_name = st.text_input("Matter Name *")
            client_name = st.text_input("Client Name *")
            matter_type = st.selectbox("Matter Type", [mt.value.replace('_', ' ').title() for mt in MatterType])
        
        with col2:
            description = st.text_area("Description")
            estimated_budget = st.number_input("Estimated Budget ($)", min_value=0.0, step=1000.0)
            estimated_hours = st.number_input("Estimated Hours", min_value=0.0, step=10.0)
        
        if st.form_submit_button("Create Matter"):
            if matter_name and client_name:
                new_matter = Matter(
                    id=str(uuid.uuid4()),
                    name=matter_name,
                    client_id=str(uuid.uuid4()),
                    client_name=client_name,
                    matter_type=matter_type.lower().replace(' ', '_'),
                    status='active',
                    created_date=datetime.now(),
                    assigned_attorneys=[st.session_state['user']['email']],
                    description=description,
                    budget=estimated_budget,
                    estimated_hours=estimated_hours,
                    actual_hours=0.0
                )
                
                st.session_state.matters.append(new_matter)
                st.success(f"Matter '{matter_name}' created successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields.")

def _show_matter_list(auth_service):
    st.subheader("Active Matters")
    
    for matter in st.session_state.matters:
        matter_docs = [doc for doc in st.session_state.documents if doc.matter_id == matter.id]
        
        with st.expander(f"{matter.name} - {matter.client_name}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Client:** {matter.client_name}")
                st.markdown(f"**Type:** {matter.matter_type.replace('_', ' ').title()}")
                st.markdown(f"**Status:** {matter.status.title()}")
            
            with col2:
                st.markdown(f"**Documents:** {len(matter_docs)}")
                st.markdown(f"**Budget:** ${matter.budget:,.2f}")
                st.markdown(f"**Est. Hours:** {matter.estimated_hours}")
            
            with col3:
                st.markdown(f"**Actual Hours:** {matter.actual_hours}")
                st.markdown(f"**Created:** {matter.created_date.strftime('%Y-%m-%d')}")
            
            if matter.description:
                st.markdown(f"**Description:** {matter.description}")
            
            # Recent documents for this matter
            if matter_docs:
                st.markdown("**Recent Documents:**")
                for doc in matter_docs[-3:]:
                    st.markdown(f"• {doc.name} - {doc.document_type}")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Analytics", key=f"analytics_{matter.id}"):
                    st.info("Matter analytics would open here")
            
            with col2:
                if auth_service.has_permission('write') and st.button("Edit", key=f"edit_matter_{matter.id}"):
                    st.info("Matter editor would open here")
            
            with col3:
                if st.button("Tasks", key=f"tasks_{matter.id}"):
                    st.info("Task management would open here")
