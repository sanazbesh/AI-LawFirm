import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

def show():
    st.markdown("""
    <div class="main-header">
        <h1>📅 Calendar & Task Management</h1>
        <p>Integrated scheduling, deadlines, and task tracking for legal professionals</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calendar tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📅 Calendar View", 
        "✅ Task Management", 
        "⚖️ Court Deadlines", 
        "📋 Matter Schedule"
    ])
    
    with tab1:
        show_calendar_view()
    
    with tab2:
        show_task_management()
    
    with tab3:
        show_court_deadlines()
    
    with tab4:
        show_matter_schedule()

def show_calendar_view():
    st.subheader("📅 Calendar Overview")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Calendar controls
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            view_type = st.selectbox("View:", ["Month", "Week", "Day", "Agenda"])
        with col_b:
            selected_date = st.date_input("Date:", datetime.now())
        with col_c:
            filter_type = st.selectbox("Filter:", ["All Events", "Meetings", "Deadlines", "Court Dates"])
        
        # Calendar display (simplified representation)
        st.markdown("#### Calendar Events")
        
        # Generate sample events
        events = [
            {
                "time": "09:00 AM",
                "title": "Client Meeting - ABC Corp",
                "type": "Meeting",
                "duration": "1 hour",
                "location": "Conference Room A",
                "attendees": "John Smith, Sarah Johnson"
            },
            {
                "time": "11:30 AM",
                "title": "Discovery Deadline - Case #2024-156",
                "type": "Deadline",
                "duration": "All day",
                "location": "N/A",
                "attendees": "Legal Team"
            },
            {
                "time": "02:00 PM",
                "title": "Court Hearing - Superior Court",
                "type": "Court Date",
                "duration": "2 hours",
                "location": "Courthouse Room 301",
                "attendees": "Attorney, Client"
            },
            {
                "time": "04:30 PM",
                "title": "Internal Review Meeting",
                "type": "Meeting",
                "duration": "45 minutes",
                "location": "Virtual",
                "attendees": "Partners, Associates"
            }
        ]
        
        for event in events:
            with st.expander(f"{event['time']} - {event['title']}"):
                col_x, col_y = st.columns(2)
                with col_x:
                    st.write(f"**Type:** {event['type']}")
                    st.write(f"**Duration:** {event['duration']}")
                with col_y:
                    st.write(f"**Location:** {event['location']}")
                    st.write(f"**Attendees:** {event['attendees']}")
                
                col_action1, col_action2, col_action3 = st.columns(3)
                with col_action1:
                    st.button("✏️ Edit", key=f"edit_{event['time']}")
                with col_action2:
                    st.button("📧 Notify", key=f"notify_{event['time']}")
                with col_action3:
                    st.button("❌ Cancel", key=f"cancel_{event['time']}")
    
    with col2:
        st.markdown("#### Quick Add Event")
        
        with st.form("add_event"):
            event_title = st.text_input("Event Title:")
            event_date = st.date_input("Date:")
            event_time = st.time_input("Time:")
            event_type = st.selectbox("Type:", ["Meeting", "Deadline", "Court Date", "Other"])
            event_duration = st.selectbox("Duration:", ["15 min", "30 min", "1 hour", "2 hours", "All day"])
            
            if st.form_submit_button("➕ Add Event"):
                st.success("Event added successfully!")
        
        st.markdown("#### Today's Summary")
        st.metric("Total Events", "4")
        st.metric("Meetings", "2")
        st.metric("Deadlines", "1")
        st.metric("Court Dates", "1")
        
        st.markdown("#### Upcoming Alerts")
        alerts = [
            "⏰ Meeting in 30 minutes",
            "📅 Deadline tomorrow",
            "⚖️ Court date next week",
            "📋 Review due Friday"
        ]
        
        for alert in alerts:
            st.info(alert)

def show_task_management():
    st.subheader("✅ Task Management Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Task filters
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            task_filter = st.selectbox("Filter by:", ["All Tasks", "My Tasks", "Overdue", "This Week"])
        with col_b:
            priority_filter = st.selectbox("Priority:", ["All", "High", "Medium", "Low"])
        with col_c:
            status_filter = st.selectbox("Status:", ["All", "Pending", "In Progress", "Completed"])
        
        # Task list
        st.markdown("#### Task List")
        
        tasks = [
            {
                "id": "T001",
                "title": "Review merger agreement draft",
                "assignee": "Sarah Johnson",
                "priority": "High",
                "status": "In Progress",
                "due_date": "2024-09-25",
                "matter": "ABC Corp Acquisition",
                "progress": 75
            },
            {
                "id": "T002",
                "title": "Prepare discovery responses",
                "assignee": "Mike Davis",
                "priority": "High",
                "status": "Pending",
                "due_date": "2024-09-24",
                "matter": "Johnson vs. Tech Solutions",
                "progress": 25
            },
            {
                "id": "T003",
                "title": "Client contract review",
                "assignee": "Emily Chen",
                "priority": "Medium",
                "status": "In Progress",
                "due_date": "2024-09-27",
                "matter": "XYZ Services Agreement",
                "progress": 50
            },
            {
                "id": "T004",
                "title": "File motion to dismiss",
                "assignee": "John Smith",
                "priority": "High",
                "status": "Completed",
                "due_date": "2024-09-20",
                "matter": "Continental Corp Defense",
                "progress": 100
            }
        ]
        
        for task in tasks:
            priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            status_color = {"Pending": "⭕", "In Progress": "🔄", "Completed": "✅"}
            
            with st.expander(f"{priority_color[task['priority']]} {task['title']} - Due: {task['due_date']}"):
                col_x, col_y = st.columns(2)
                with col_x:
                    st.write(f"**Assignee:** {task['assignee']}")
                    st.write(f"**Matter:** {task['matter']}")
                    st.write(f"**Status:** {status_color[task['status']]} {task['status']}")
                with col_y:
                    st.write(f"**Priority:** {task['priority']}")
                    st.write(f"**Task ID:** {task['id']}")
                    st.progress(task['progress'] / 100)
                
                # Task actions
                col_action1, col_action2, col_action3, col_action4 = st.columns(4)
                with col_action1:
                    st.button("✏️ Edit", key=f"edit_task_{task['id']}")
                with col_action2:
                    st.button("👥 Assign", key=f"assign_task_{task['id']}")
                with col_action3:
                    st.button("💬 Comment", key=f"comment_task_{task['id']}")
                with col_action4:
                    st.button("📎 Attach", key=f"attach_task_{task['id']}")
    
    with col2:
        st.markdown("#### Create New Task")
        
        with st.form("new_task"):
            task_title = st.text_input("Task Title:")
            task_assignee = st.selectbox("Assign to:", ["John Smith", "Sarah Johnson", "Mike Davis", "Emily Chen"])
            task_priority = st.selectbox("Priority:", ["High", "Medium", "Low"])
            task_due = st.date_input("Due Date:")
            task_matter = st.selectbox("Related Matter:", ["ABC Corp Acquisition", "Johnson vs. Tech Solutions", "XYZ Services Agreement"])
            task_description = st.text_area("Description:")
            
            if st.form_submit_button("➕ Create Task"):
                st.success("Task created successfully!")
        
        st.markdown("#### Task Statistics")
        st.metric("Total Tasks", "47")
        st.metric("Completed This Week", "12", "+3")
        st.metric("Overdue Tasks", "3", "-2")
        st.metric("High Priority", "8")

def show_court_deadlines():
    st.subheader("⚖️ Court Deadlines & Filing Management")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### Upcoming Court Deadlines")
        
        # Deadline filters
        col_a, col_b = st.columns(2)
        with col_a:
            deadline_filter = st.selectbox("Time Frame:", ["Next 30 Days", "Next 7 Days", "Overdue", "All"])
        with col_b:
            court_filter = st.selectbox("Court:", ["All Courts", "Federal Court", "State Court", "Superior Court"])
        
        # Deadlines list
        deadlines = [
            {
                "case": "Johnson vs. Tech Solutions Inc.",
                "deadline": "Motion to Dismiss",
                "due_date": "2024-09-24",
                "days_remaining": 1,
                "court": "Superior Court",
                "assigned": "John Smith",
                "status": "In Progress"
            },
            {
                "case": "ABC Corp Acquisition Review",
                "deadline": "Regulatory Filing",
                "due_date": "2024-09-26",
                "days_remaining": 3,
                "court": "Federal Court",
                "assigned": "Sarah Johnson",
                "status": "Pending Review"
            },
            {
                "case": "Continental Corp vs. Innovate LLC",
                "deadline": "Discovery Response",
                "due_date": "2024-09-30",
                "days_remaining": 7,
                "court": "State Court",
                "assigned": "Mike Davis",
                "status": "Draft Complete"
            },
            {
                "case": "XYZ Services Contract Dispute",
                "deadline": "Summary Judgment Brief",
                "due_date": "2024-10-05",
                "days_remaining": 12,
                "court": "Superior Court",
                "assigned": "Emily Chen",
                "status": "Research Phase"
            }
        ]
        
        for deadline in deadlines:
            # Color coding based on urgency
            if deadline["days_remaining"] <= 1:
                urgency_color = "🔴"
                border_color = "red"
            elif deadline["days_remaining"] <= 7:
                urgency_color = "🟡"
                border_color = "orange"
            else:
                urgency_color = "🟢"
                border_color = "green"
            
            st.markdown(f"""
            <div style="border-left: 4px solid {border_color}; padding-left: 10px; margin: 10px 0;">
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander(f"{urgency_color} {deadline['deadline']} - {deadline['case']} (Due: {deadline['due_date']})"):
                col_x, col_y = st.columns(2)
                with col_x:
                    st.write(f"**Court:** {deadline['court']}")
                    st.write(f"**Assigned:** {deadline['assigned']}")
                with col_y:
                    st.write(f"**Status:** {deadline['status']}")
                    st.write(f"**Days Remaining:** {deadline['days_remaining']}")
                
                # Action buttons
                col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
                with col_btn1:
                    st.button("📄 View Details", key=f"view_{deadline['case'][:10]}")
                with col_btn2:
                    st.button("📝 Update Status", key=f"status_{deadline['case'][:10]}")
                with col_btn3:
                    st.button("📧 Send Reminder", key=f"remind_{deadline['case'][:10]}")
                with col_btn4:
                    st.button("📎 Attach File", key=f"attach_{deadline['case'][:10]}")
    
    with col2:
        st.markdown("#### Deadline Alerts")
        
        alerts = [
            ("🔴 URGENT", "Motion due tomorrow"),
            ("🟡 SOON", "Filing due in 3 days"),
            ("🟢 SCHEDULED", "Brief due next week"),
            ("📅 REMINDER", "Court date in 2 weeks")
        ]
        
        for severity, alert in alerts:
            if "URGENT" in severity:
                st.error(f"{severity}: {alert}")
            elif "SOON" in severity:
                st.warning(f"{severity}: {alert}")
            else:
                st.info(f"{severity}: {alert}")
        
        st.markdown("#### Quick Actions")
        if st.button("📅 Add Court Date"):
            st.info("Opening court date form...")
        if st.button("⏰ Set Reminder"):
            st.info("Setting up reminder...")
        if st.button("📊 Deadline Report"):
            st.info("Generating deadline report...")

def show_matter_schedule():
    st.subheader("📋 Matter Schedule & Milestones")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Matter selection
        selected_matter = st.selectbox("Select Matter:", [
            "ABC Corp Acquisition",
            "Johnson vs. Tech Solutions",
            "Continental Corp Defense",
            "XYZ Services Agreement",
            "Innovation LLC Patent Dispute"
        ])
        
        st.markdown(f"#### Timeline for {selected_matter}")
        
        # Timeline visualization
        timeline_events = [
            {
                "date": "2024-09-15",
                "milestone": "Case Initiation",
                "status": "Completed",
                "description": "Initial client meeting and case assessment"
            },
            {
                "date": "2024-09-20",
                "milestone": "Discovery Request",
                "status": "Completed",
                "description": "Filed initial discovery requests"
            },
            {
                "date": "2024-09-25",
                "milestone": "Document Review",
                "status": "In Progress",
                "description": "Review client documents and evidence"
            },
            {
                "date": "2024-10-01",
                "milestone": "Expert Witness Selection",
                "status": "Pending",
                "description": "Identify and retain expert witnesses"
            },
            {
                "date": "2024-10-15",
                "milestone": "Motion Filing",
                "status": "Scheduled",
                "description": "File motion for summary judgment"
            },
            {
                "date": "2024-11-01",
                "milestone": "Settlement Conference",
                "status": "Scheduled",
                "description": "Court-ordered settlement conference"
            }
        ]
        
        for i, event in enumerate(timeline_events):
            status_icons = {
                "Completed": "✅",
                "In Progress": "🔄",
                "Pending": "⭕",
                "Scheduled": "📅"
            }
            
            status_colors = {
                "Completed": "green",
                "In Progress": "blue",
                "Pending": "orange",
                "Scheduled": "purple"
            }
            
            st.markdown(f"""
            <div style="border-left: 3px solid {status_colors[event['status']]}; padding-left: 15px; margin: 15px 0;">
                <h4>{status_icons[event['status']]} {event['milestone']}</h4>
                <p><strong>Date:</strong> {event['date']}</p>
                <p><strong>Status:</strong> {event['status']}</p>
                <p>{event['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("#### Matter Resources")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            if st.button("📁 View Documents"):
                st.info("Opening document library...")
        with col_res2:
            if st.button("👥 Team Members"):
                st.info("Showing team assignments...")
        with col_res3:
            if st.button("💰 Budget Tracking"):
                st.info("Opening budget dashboard...")
    
    with col2:
        st.markdown("#### Matter Progress")
        
        progress_metrics = [
            ("Overall Progress", 45, "%"),
            ("Discovery Complete", 75, "%"),
            ("Document Review", 60, "%"),
            ("Budget Utilized", 32, "%")
        ]
        
        for label, value, unit in progress_metrics:
            st.metric(label, f"{value}{unit}")
            st.progress(value / 100)
        
        st.markdown("#### Next Actions")
        next_actions = [
            "📋 Complete document review by Friday",
            "📞 Schedule expert witness interview",
            "📝 Draft motion for summary judgment",
            "📧 Send status update to client",
            "⏰ Prepare for settlement conference"
        ]
        
        for action in next_actions:
            st.write(action)
        
        st.markdown("#### Matter Team")
        team_members = [
            ("John Smith", "Lead Attorney"),
            ("Sarah Johnson", "Associate"),
            ("Mike Davis", "Paralegal"),
            ("Emily Chen", "Legal Assistant")
        ]
        
        for name, role in team_members:
            st.write(f"**{name}** - {role}")
        
        if st.button("➕ Add Team Member"):
            st.info("Opening team member form...")

# Main application entry point
if __name__ == "__main__":
    show()
