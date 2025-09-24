import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

def show():
    st.markdown("""
    <div class="main-header">
        <h1>🔍 Advanced Search & Discovery</h1>
        <p>Comprehensive search across documents, matters, communications, and legal databases</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔍 Universal Search", 
        "📄 Document Search", 
        "📊 Data Analytics", 
        "🤖 AI-Powered Search", 
        "📚 Legal Research",
        "🗂️ Search Management"
    ])
    
    with tab1:
        show_universal_search()
    
    with tab2:
        show_document_search()
    
    with tab3:
        show_data_analytics()
    
    with tab4:
        show_ai_powered_search()
    
    with tab5:
        show_legal_research()
    
    with tab6:
        show_search_management()

def show_universal_search():
    st.subheader("🔍 Universal Search")
    
    # Search interface
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_query = st.text_input("", placeholder="Search across all documents, matters, communications, and data...", key="universal_search")
    with col2:
        search_button = st.button("🔍 Search", type="primary")
    
    # Search filters
    with st.expander("🔧 Advanced Filters"):
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            content_types = st.multiselect("Content Types:", 
                ["Documents", "Emails", "Matters", "Contacts", "Calendar Events", "Tasks"])
        with col_b:
            date_range = st.date_input("Date Range:", value=[datetime.now() - timedelta(days=365), datetime.now()])
        with col_c:
            authors = st.multiselect("Authors:", ["John Smith", "Sarah Johnson", "Mike Davis", "Emily Chen", "All Attorneys"])
        with col_d:
            matters = st.multiselect("Related Matters:", ["ABC Corp Acquisition", "Johnson vs. Tech Solutions", "Continental Corp Defense"])
    
    if search_query or search_button:
        st.markdown("#### Search Results")
        
        # Mock search results with different content types
        search_results = [
            {
                "type": "Document",
                "title": "Merger Agreement - ABC Corp Final Draft.docx",
                "content": "This merger agreement contains provisions for intellectual property transfer and employee retention...",
                "author": "Sarah Johnson",
                "date": "2024-09-20",
                "matter": "ABC Corp Acquisition",
                "relevance": 95,
                "tags": ["merger", "IP", "employment"]
            },
            {
                "type": "Email",
                "title": "RE: Contract Review Feedback",
                "content": "Please review the attached contract amendments and provide feedback by EOD Friday...",
                "author": "John Smith",
                "date": "2024-09-22",
                "matter": "XYZ Services Agreement",
                "relevance": 88,
                "tags": ["contract", "review", "amendment"]
            },
            {
                "type": "Matter",
                "title": "Continental Corp Defense - Patent Infringement",
                "content": "Defending against patent infringement claims related to software algorithms...",
                "author": "Mike Davis",
                "date": "2024-09-15",
                "matter": "Continental Corp Defense",
                "relevance": 82,
                "tags": ["patent", "infringement", "defense"]
            },
            {
                "type": "Document",
                "title": "Discovery Response Template.pdf",
                "content": "Standard template for responding to discovery requests in civil litigation matters...",
                "author": "Emily Chen",
                "date": "2024-09-18",
                "matter": "Johnson vs. Tech Solutions",
                "relevance": 76,
                "tags": ["discovery", "template", "litigation"]
            },
            {
                "type": "Task",
                "title": "File Motion for Summary Judgment",
                "content": "Prepare and file motion for summary judgment in the ABC Corp case by October 15th...",
                "author": "Sarah Johnson",
                "date": "2024-09-21",
                "matter": "ABC Corp Acquisition",
                "relevance": 73,
                "tags": ["motion", "summary judgment", "deadline"]
            }
        ]
        
        # Results summary
        col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
        with col_sum1:
            st.metric("Total Results", len(search_results))
        with col_sum2:
            st.metric("Documents", sum(1 for r in search_results if r["type"] == "Document"))
        with col_sum3:
            st.metric("Emails", sum(1 for r in search_results if r["type"] == "Email"))
        with col_sum4:
            st.metric("Avg Relevance", f"{sum(r['relevance'] for r in search_results) / len(search_results):.1f}%")
        
        # Sort and filter options
        col_sort1, col_sort2, col_sort3 = st.columns(3)
        with col_sort1:
            sort_by = st.selectbox("Sort By:", ["Relevance", "Date", "Author", "Matter"])
        with col_sort2:
            result_limit = st.selectbox("Show Results:", ["All", "Top 10", "Top 25", "Top 50"])
        with col_sort3:
            export_option = st.selectbox("Export:", ["None", "CSV", "PDF Report", "JSON"])
        
        # Display results
        for i, result in enumerate(search_results, 1):
            type_icons = {"Document": "📄", "Email": "📧", "Matter": "⚖️", "Task": "✅", "Contact": "👤"}
            
            with st.expander(f"{type_icons.get(result['type'], '📄')} {result['title']} ({result['relevance']}% relevant)"):
                col_res1, col_res2 = st.columns([3, 1])
                
                with col_res1:
                    st.write(f"**Content Preview:** {result['content']}")
                    st.write(f"**Type:** {result['type']} | **Author:** {result['author']} | **Date:** {result['date']}")
                    st.write(f"**Related Matter:** {result['matter']}")
                    
                    # Display tags
                    tag_display = " ".join([f"`{tag}`" for tag in result['tags']])
                    st.markdown(f"**Tags:** {tag_display}")
                
                with col_res2:
                    st.progress(result['relevance'] / 100)
                    st.write(f"Relevance: {result['relevance']}%")
                    
                    # Action buttons
                    if st.button(f"📖 Open", key=f"open_{i}"):
                        st.info(f"Opening {result['title']}...")
                    if st.button(f"📎 Add to Collection", key=f"collect_{i}"):
                        st.success("Added to collection!")
                    if st.button(f"🏷️ Add Tags", key=f"tag_{i}"):
                        st.info("Tag editor opened")

def show_document_search():
    st.subheader("📄 Advanced Document Search")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Document search interface
        st.markdown("#### Search Parameters")
        
        col_a, col_b = st.columns(2)
        with col_a:
            doc_search_query = st.text_input("Document Content Search:", placeholder="Enter keywords, phrases, or document content...")
        with col_b:
            doc_type = st.selectbox("Document Type:", ["All Types", "Contracts", "Briefs", "Motions", "Discovery", "Correspondence"])
        
        col_c, col_d, col_e = st.columns(3)
        with col_c:
            file_format = st.selectbox("File Format:", ["All Formats", "PDF", "DOCX", "TXT", "XLSX"])
        with col_d:
            size_range = st.selectbox("File Size:", ["Any Size", "< 1MB", "1-10MB", "10-50MB", "> 50MB"])
        with col_e:
            language = st.selectbox("Language:", ["All Languages", "English", "Spanish", "French"])
        
        # Advanced search options
        with st.expander("🔧 Advanced Search Options"):
            col_adv1, col_adv2 = st.columns(2)
            
            with col_adv1:
                exact_phrase = st.text_input("Exact Phrase:", placeholder="\"exact phrase in quotes\"")
                any_words = st.text_input("Any of These Words:", placeholder="word1 OR word2 OR word3")
                exclude_words = st.text_input("Exclude Words:", placeholder="NOT word1 NOT word2")
                
                # OCR and content analysis
                ocr_search = st.checkbox("Search OCR Text (Scanned Documents)")
                metadata_search = st.checkbox("Include Metadata Search")
            
            with col_adv2:
                version_control = st.checkbox("Search All Versions")
                annotations = st.checkbox("Include Annotations & Comments")
                
                # Date filters
                creation_date = st.date_input("Created After:", value=None)
                modified_date = st.date_input("Modified After:", value=None)
        
        if st.button("🔍 Search Documents", type="primary"):
            st.markdown("#### Document Search Results")
            
            # Mock document results with enhanced information
            document_results = [
                {
                    "filename": "ABC_Corp_Merger_Agreement_v3.2.pdf",
                    "path": "/matters/abc_corp/contracts/",
                    "size": "2.4 MB",
                    "pages": 47,
                    "last_modified": "2024-09-20",
                    "created": "2024-09-15",
                    "author": "Sarah Johnson",
                    "matter": "ABC Corp Acquisition",
                    "matches": 12,
                    "relevance": 94,
                    "version": "3.2",
                    "status": "Final",
                    "security": "Confidential"
                },
                {
                    "filename": "Patent_Defense_Strategy_Draft.docx",
                    "path": "/matters/continental/strategy/",
                    "size": "856 KB",
                    "pages": 23,
                    "last_modified": "2024-09-19",
                    "created": "2024-09-10",
                    "author": "Mike Davis",
                    "matter": "Continental Corp Defense",
                    "matches": 8,
                    "relevance": 87,
                    "version": "1.0",
                    "status": "Draft",
                    "security": "Attorney Work Product"
                },
                {
                    "filename": "Discovery_Response_Johnson_Case.pdf",
                    "path": "/matters/johnson_tech/discovery/",
                    "size": "1.7 MB",
                    "pages": 15,
                    "last_modified": "2024-09-18",
                    "created": "2024-09-16",
                    "author": "Emily Chen",
                    "matter": "Johnson vs. Tech Solutions",
                    "matches": 6,
                    "relevance": 79,
                    "version": "Final",
                    "status": "Filed",
                    "security": "Public"
                }
            ]
            
            # Enhanced results display
            for doc in document_results:
                with st.expander(f"📄 {doc['filename']} ({doc['matches']} matches, {doc['relevance']}% relevant)"):
                    col_doc1, col_doc2, col_doc3 = st.columns(3)
                    
                    with col_doc1:
                        st.write(f"**Size:** {doc['size']}")
                        st.write(f"**Pages:** {doc['pages']}")
                        st.write(f"**Version:** {doc['version']}")
                        st.write(f"**Status:** {doc['status']}")
                    
                    with col_doc2:
                        st.write(f"**Author:** {doc['author']}")
                        st.write(f"**Matter:** {doc['matter']}")
                        st.write(f"**Created:** {doc['created']}")
                        st.write(f"**Modified:** {doc['last_modified']}")
                    
                    with col_doc3:
                        st.progress(doc['relevance'] / 100)
                        st.write(f"Relevance: {doc['relevance']}%")
                        st.write(f"**Security:** {doc['security']}")
                        st.write(f"**Path:** {doc['path']}")
                    
                    # Enhanced action buttons
                    col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)
                    with col_btn1:
                        st.button("👁️ Preview", key=f"preview_{doc['filename'][:10]}")
                    with col_btn2:
                        st.button("📥 Download", key=f"download_{doc['filename'][:10]}")
                    with col_btn3:
                        st.button("✏️ Annotate", key=f"annotate_{doc['filename'][:10]}")
                    with col_btn4:
                        st.button("📧 Share", key=f"share_{doc['filename'][:10]}")
                    with col_btn5:
                        st.button("🔄 Versions", key=f"versions_{doc['filename'][:10]}")
    
    with col2:
        st.markdown("#### Search Statistics")
        
        stats = [
            ("Total Documents", "2,847"),
            ("Searchable Content", "99.2%"),
            ("Index Size", "14.7 GB"),
            ("Last Updated", "2 min ago")
        ]
        
        for label, value in stats:
            st.metric(label, value)
        
        st.markdown("#### Quick Filters")
        quick_filters = [
            "📄 Recent Documents",
            "⭐ Frequently Accessed", 
            "🔒 Confidential Only",
            "📝 Draft Documents",
            "✅ Final Versions",
            "📊 Excel Files",
            "📋 Templates"
        ]
        
        for filter_option in quick_filters:
            if st.button(filter_option, key=f"filter_{filter_option[:5]}"):
                st.info(f"Applied filter: {filter_option}")
        
        st.markdown("#### Saved Searches")
        saved_searches = [
            "Contract amendments 2024",
            "Patent litigation docs", 
            "Client correspondence",
            "Discovery materials",
            "Employment agreements"
        ]
        
        for search in saved_searches:
            col_search1, col_search2 = st.columns([3, 1])
            with col_search1:
                st.write(f"• {search}")
            with col_search2:
                st.button("🔍", key=f"saved_{search[:10]}")

def show_data_analytics():
    st.subheader("📊 Search & Data Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Search Pattern Analysis")
        
        # Search frequency chart
        search_data = pd.DataFrame({
            'Date': pd.date_range('2024-09-01', '2024-09-23', freq='D'),
            'Searches': [45, 52, 38, 67, 43, 59, 71, 48, 63, 56, 72, 41, 58, 69, 44, 61, 47, 55, 73, 49, 64, 57, 68]
        })
        
        fig_search = px.line(search_data, x='Date', y='Searches', title='Daily Search Volume')
        st.plotly_chart(fig_search, use_container_width=True)
        
        st.markdown("#### Most Searched Terms")
        
        search_terms = pd.DataFrame({
            'Term': ['contract', 'agreement', 'liability', 'intellectual property', 'termination', 'confidentiality'],
            'Frequency': [247, 198, 156, 134, 112, 98],
            'Trend': ['📈', '📈', '➡️', '📈', '📉', '➡️']
        })
        
        for _, row in search_terms.iterrows():
            col_term1, col_term2, col_term3 = st.columns([2, 1, 1])
            with col_term1:
                st.write(f"**{row['Term']}**")
            with col_term2:
                st.write(f"{row['Frequency']} searches")
            with col_term3:
                st.write(row['Trend'])
        
        # Search success rate
        st.markdown("#### Search Performance Metrics")
        
        performance_metrics = [
            ("Search Success Rate", "89.2%", "+2.1%"),
            ("Avg Results per Search", "24.7", "+3.2"),
            ("Zero Results Rate", "5.8%", "-1.4%"),
            ("User Satisfaction", "4.2/5", "+0.3")
        ]
        
        for metric, value, change in performance_metrics:
            st.metric(metric, value, change)
    
    with col2:
        st.markdown("#### Document Access Patterns")
        
        # Document type access pie chart
        doc_access_data = pd.DataFrame({
            'Document Type': ['Contracts', 'Correspondence', 'Briefs', 'Discovery', 'Other'],
            'Access Count': [342, 287, 198, 156, 89]
        })
        
        fig_pie = px.pie(doc_access_data, values='Access Count', names='Document Type', 
                        title='Document Access by Type')
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Document access metrics
        access_metrics = [
            ("Total Documents Accessed", "1,247", "+8.2%"),
            ("Unique Users", "23", "+2"),
            ("Avg. Session Duration", "12.4 min", "+1.3 min"),
            ("Mobile Access", "34%", "+5.2%")
        ]
        
        for label, value, change in access_metrics:
            st.metric(label, value, change)
        
        st.markdown("#### Top Accessed Documents")
        
        top_docs = [
            ("Standard_NDA_Template.docx", 87, "📄"),
            ("Employment_Agreement_2024.pdf", 72, "📄"),
            ("IP_License_Agreement.docx", 64, "📄"),
            ("Merger_Checklist.xlsx", 58, "📊"),
            ("Litigation_Timeline.pdf", 45, "📄")
        ]
        
        for doc, access_count, icon in top_docs:
            col_acc1, col_acc2 = st.columns([3, 1])
            with col_acc1:
                st.write(f"{icon} {doc}")
            with col_acc2:
                st.write(f"{access_count} views")

def show_ai_powered_search():
    st.subheader("🤖 AI-Powered Intelligent Search")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### Natural Language Query")
        
        # AI search interface
        ai_query = st.text_area("Ask a question in natural language:", 
                               placeholder="e.g., 'Show me all contracts with ABC Corp that expire in the next 6 months' or 'Find documents related to intellectual property disputes from last year'",
                               height=100)
        
        col_ai1, col_ai2 = st.columns(2)
        with col_ai1:
            search_scope = st.selectbox("Search Scope:", ["All Content", "Current Matter Only", "My Documents", "Recent Activity"])
        with col_ai2:
            ai_features = st.multiselect("AI Features:", ["Summarization", "Entity Extraction", "Sentiment Analysis", "Translation"])
        
        # AI search modes
        search_mode = st.radio("Search Mode:", ["Standard AI", "Deep Analysis", "Comparative Search", "Predictive Search"])
        
        if st.button("🤖 AI Search", type="primary"):
            st.markdown("#### AI Search Results & Analysis")
            
            # AI interpretation
            with st.container():
                st.info("🤖 **AI Interpretation:** I understand you're looking for contract documents related to ABC Corp with upcoming expiration dates. Let me analyze the relevant documents and provide insights.")
                
                # Query analysis
                st.markdown("**Query Analysis:**")
                col_query1, col_query2, col_query3 = st.columns(3)
                with col_query1:
                    st.write("**Entities Found:** ABC Corp, contracts, expiration")
                with col_query2:
                    st.write("**Intent:** Contract review, deadline tracking")
                with col_query3:
                    st.write("**Time Context:** Next 6 months")
            
            # AI-enhanced results
            ai_results = [
                {
                    "title": "ABC Corp Service Agreement",
                    "summary": "Multi-year service agreement covering IT support and maintenance. Key renewal clause on page 12.",
                    "entities": ["ABC Corp", "IT Services", "Renewal Clause", "John Smith"],
                    "sentiment": "Neutral",
                    "expiry_date": "2024-12-15",
                    "ai_insights": "Contract contains auto-renewal clause. Recommend review 90 days before expiry.",
                    "confidence": 94,
                    "risk_level": "Medium",
                    "action_required": "Review required"
                },
                {
                    "title": "ABC Corp NDA Extension",
                    "summary": "Non-disclosure agreement extension with specific IP protection clauses.",
                    "entities": ["ABC Corp", "NDA", "IP Protection", "Confidentiality"],
                    "sentiment": "Positive",
                    "expiry_date": "2025-01-30",
                    "ai_insights": "Strong IP protection. No immediate action required.",
                    "confidence": 87,
                    "risk_level": "Low",
                    "action_required": "Monitor"
                },
                {
                    "title": "ABC Corp Master Services Agreement",
                    "summary": "Comprehensive services agreement with multiple work orders and deliverables.",
                    "entities": ["ABC Corp", "MSA", "Work Orders", "Deliverables"],
                    "sentiment": "Neutral",
                    "expiry_date": "2024-11-30",
                    "ai_insights": "Complex agreement with multiple dependencies. Early renewal discussions recommended.",
                    "confidence": 91,
                    "risk_level": "High",
                    "action_required": "Immediate attention"
                }
            ]
            
            for result in ai_results:
                risk_colors = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
                
                with st.expander(f"🤖 {result['title']} (AI Confidence: {result['confidence']}%) {risk_colors[result['risk_level']]}"):
                    col_ai_res1, col_ai_res2 = st.columns(2)
                    
                    with col_ai_res1:
                        st.write(f"**AI Summary:** {result['summary']}")
                        st.write(f"**Key Entities:** {', '.join(result['entities'])}")
                        st.write(f"**Sentiment:** {result['sentiment']}")
                        st.write(f"**Risk Level:** {result['risk_level']}")
                    
                    with col_ai_res2:
                        st.write(f"**Expiry Date:** {result['expiry_date']}")
                        st.write(f"**AI Insights:** {result['ai_insights']}")
                        st.write(f"**Action Required:** {result['action_required']}")
                        st.progress(result['confidence'] / 100)
                    
                    # AI action buttons
                    col_ai_btn1, col_ai_btn2, col_ai_btn3, col_ai_btn4 = st.columns(4)
                    with col_ai_btn1:
                        st.button("📝 Generate Summary", key=f"ai_summary_{result['title'][:10]}")
                    with col_ai_btn2:
                        st.button("🔍 Deep Analysis", key=f"ai_analysis_{result['title'][:10]}")
                    with col_ai_btn3:
                        st.button("⚡ Quick Actions", key=f"ai_actions_{result['title'][:10]}")
                    with col_ai_btn4:
                        st.button("📅 Set Reminder", key=f"ai_reminder_{result['title'][:10]}")
    
    with col2:
        st.markdown("#### AI Assistant")
        
        st.markdown("##### Query Suggestions")
        suggestions = [
            "Find overdue contracts",
            "Show high-risk documents", 
            "Contracts expiring soon",
            "Documents needing review",
            "Recent amendments",
            "Similar agreements",
            "Compliance issues"
        ]
        
        for suggestion in suggestions:
            if st.button(f"💡 {suggestion}", key=f"suggest_{suggestion[:10]}"):
                st.info(f"Searching: {suggestion}")
        
        st.markdown("##### AI Capabilities")
        capabilities = [
            "🧠 Natural Language Understanding",
            "📊 Intelligent Summarization", 
            "🏷️ Automatic Entity Extraction",
            "💭 Sentiment Analysis",
            "🔗 Relationship Mapping",
            "⚠️ Risk Identification",
            "📈 Trend Analysis",
            "🎯 Predictive Insights"
        ]
        
        for capability in capabilities:
            st.write(capability)
        
        st.markdown("##### AI Search History")
        ai_history = [
            "Contract expiration analysis",
            "IP document classification", 
            "Risk assessment query",
            "Entity relationship mapping",
            "Compliance document search"
        ]
        
        for history in ai_history:
            if st.button(f"🔄 {history}", key=f"history_{history[:10]}"):
                st.info(f"Rerunning: {history}")

def show_legal_research():
    st.subheader("📚 Legal Research & Case Law Search")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### Legal Database Search")
        
        # Research query
        legal_query = st.text_input("Legal Research Query:", placeholder="Enter case law, statutes, regulations, or legal concepts...")
        
        col_legal1, col_legal2, col_legal3 = st.columns(3)
        with col_legal1:
            jurisdiction = st.selectbox("Jurisdiction:", ["All", "Federal", "State", "International"])
        with col_legal2:
            content_type = st.selectbox("Content Type:", ["All", "Case Law", "Statutes", "Regulations", "Legal Forms"])
        with col_legal3:
            date_filter = st.selectbox("Date Range:", ["All Time", "Last 5 Years", "Last 10 Years", "Since 2000"])
        
        # Advanced legal research options
        with st.expander("🔧 Advanced Legal Research"):
            col_adv_legal1, col_adv_legal2 = st.columns(2)
            
            with col_adv_legal1:
                court_level = st.multiselect("Court Level:", ["Supreme Court", "Circuit Courts", "District Courts", "State Supreme", "State Appellate"])
                practice_area = st.multiselect("Practice Area:", ["IP Law", "Contract Law", "Employment Law", "Corporate Law", "Litigation"])
            
            with col_adv_legal2:
                shepardize = st.checkbox("Shepardize Results", value=True)
                headnotes = st.checkbox("Include Headnotes", value=True)
                secondary_sources = st.checkbox("Include Secondary Sources")
        
        if st.button("📚 Search Legal Database", type="primary"):
            st.markdown("#### Legal Research Results")
            
            legal_results = [
                {
                    "title": "Smith v. Technology Corp (2023)",
                    "court": "9th Circuit Court of Appeals",
                    "date": "2023-08-15",
                    "citation": "987 F.3d 456 (9th Cir. 2023)",
                    "relevance": 96,
                    "summary": "Case addressing intellectual property rights in software development contracts and work-for-hire provisions...",
                    "key_holdings": ["IP ownership in work-for-hire", "Contract interpretation standards"],
                    "shepard_status": "Good Law",
                    "times_cited": 47,
                    "practice_areas": ["IP Law", "Contract Law"]
                },
                {
                    "title": "Patent Protection Act § 201",
                    "source": "Federal Statute",
                    "date": "2022-12-01",
                    "citation": "35 U.S.C. § 201",
                    "relevance": 91,
                    "summary": "Federal statute governing patent ownership and licensing requirements in government-funded research...",
                    "key_provisions": ["Patent licensing", "Government rights", "Small business protections"],
                    "amendments": "Last amended 2022",
                    "effective_date": "2023-01-01",
                    "practice_areas": ["IP Law", "Government Contracts"]
                },
                {
                    "title": "Johnson Industries v. Innovation LLC (2022)",
                    "court": "Federal District Court",
                    "date": "2022-11-22", 
                    "citation": "2022 U.S. Dist. LEXIS 45678",
                    "relevance": 88,
                    "summary": "District court decision on trade secret misappropriation claims and reasonable measures requirement...",
                    "key_holdings": ["Trade secret definition", "Reasonable measures requirement"],
                    "shepard_status": "Good Law",
                    "times_cited": 23,
                    "practice_areas": ["IP Law", "Trade Secrets"]
                }
            ]
            
            for result in legal_results:
                status_colors = {"Good Law": "🟢", "Questioned": "🟡", "Bad Law": "🔴"}
                shepard_status = result.get('shepard_status', 'Unknown')
                
                with st.expander(f"⚖️ {result['title']} ({result['relevance']}% relevant) {status_colors.get(shepard_status, '⚪')}"):
                    col_legal_res1, col_legal_res2 = st.columns(2)
                    
                    with col_legal_res1:
                        st.write(f"**Court/Source:** {result.get('court', result.get('source', 'N/A'))}")
                        st.write(f"**Date:** {result['date']}")
                        st.write(f"**Citation:** {result['citation']}")
                        st.write(f"**Summary:** {result['summary']}")
                        
                        if 'practice_areas' in result:
                            areas = ", ".join(result['practice_areas'])
                            st.write(f"**Practice Areas:** {areas}")
                    
                    with col_legal_res2:
                        st.progress(result['relevance'] / 100)
                        st.write(f"Relevance: {result['relevance']}%")
                        
                        if 'shepard_status' in result:
                            st.write(f"**Shepard's Status:** {result['shepard_status']}")
                        if 'times_cited' in result:
                            st.write(f"**Times Cited:** {result['times_cited']}")
                        
                        key_items = result.get('key_holdings', result.get('key_provisions', []))
                        if key_items:
                            st.write("**Key Points:**")
                            for point in key_items:
                                st.write(f"• {point}")
                    
                    # Legal research actions
                    col_legal_btn1, col_legal_btn2, col_legal_btn3, col_legal_btn4 = st.columns(4)
                    with col_legal_btn1:
                        st.button("📖 Full Text", key=f"legal_full_{result['title'][:10]}")
                    with col_legal_btn2:
                        st.button("📝 Cite", key=f"legal_cite_{result['title'][:10]}")
                    with col_legal_btn3:
                        st.button("🔗 Shepardize", key=f"legal_shep_{result['title'][:10]}")
                    with col_legal_btn4:
                        st.button("📎 Save", key=f"legal_save_{result['title'][:10]}")
        
        # Legal research workspace
        st.markdown("#### Research Workspace")
        
        with st.expander("📝 Research Notes & Citations"):
            col_workspace1, col_workspace2 = st.columns(2)
            
            with col_workspace1:
                research_notes = st.text_area("Research Notes:", height=150, 
                    placeholder="Take notes on your legal research...")
                
                citation_format = st.selectbox("Citation Format:", 
                    ["Bluebook", "ALWD", "APA", "MLA", "Chicago"])
            
            with col_workspace2:
                st.markdown("**Saved Citations:**")
                saved_citations = [
                    "Smith v. Technology Corp, 987 F.3d 456 (9th Cir. 2023)",
                    "35 U.S.C. § 201 (2022)",
                    "Johnson Industries v. Innovation LLC, 2022 U.S. Dist. LEXIS 45678"
                ]
                
                for citation in saved_citations:
                    col_cite1, col_cite2 = st.columns([4, 1])
                    with col_cite1:
                        st.write(f"• {citation}")
                    with col_cite2:
                        st.button("📋", key=f"copy_cite_{citation[:15]}")
            
            col_work_btn1, col_work_btn2, col_work_btn3 = st.columns(3)
            with col_work_btn1:
                st.button("💾 Save Research")
            with col_work_btn2:
                st.button("📄 Export Report")
            with col_work_btn3:
                st.button("📧 Share Research")
    
    with col2:
        st.markdown("#### Research Tools")
        
        research_tools = [
            "📚 Case Law Database",
            "📜 Statute Finder", 
            "📋 Regulation Search",
            "📄 Legal Forms Library",
            "🔍 Citation Validator",
            "📊 Court Analytics",
            "🏛️ Docket Search"
        ]
        
        for tool in research_tools:
            if st.button(tool, key=f"tool_{tool[:10]}"):
                st.info(f"Opening {tool}...")
        
        st.markdown("#### Recent Research")
        recent_research = [
            "Patent law updates 2024",
            "Contract interpretation",
            "Employment law changes", 
            "IP licensing agreements",
            "Corporate governance",
            "Trade secret protection"
        ]
        
        for research in recent_research:
            st.write(f"• {research}")
        
        st.markdown("#### Citation Manager")
        citation_stats = [
            ("Total Citations", "127"),
            ("This Month", "23"),
            ("Validated", "98.4%"),
            ("Recent Updates", "5")
        ]
        
        for stat, value in citation_stats:
            st.metric(stat, value)
        
        if st.button("📚 Manage Citations"):
            st.info("Opening citation manager...")
        if st.button("📝 Generate Bibliography"):
            st.info("Generating bibliography...")
        if st.button("🔍 Check Citations"):
            st.info("Validating citations...")

def show_search_management():
    st.subheader("🗂️ Search Management & Collections")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Search collections
        st.markdown("#### Search Collections")
        
        collections = [
            {
                "name": "ABC Corp Merger Documents", 
                "items": 47,
                "created": "2024-09-15",
                "shared": True,
                "tags": ["merger", "contracts", "due diligence"]
            },
            {
                "name": "Patent Defense Research",
                "items": 23, 
                "created": "2024-09-12",
                "shared": False,
                "tags": ["patent", "defense", "prior art"]
            },
            {
                "name": "Employment Law Updates",
                "items": 15,
                "created": "2024-09-10", 
                "shared": True,
                "tags": ["employment", "compliance", "updates"]
            }
        ]
        
        for collection in collections:
            with st.expander(f"📁 {collection['name']} ({collection['items']} items)"):
                col_coll1, col_coll2 = st.columns(2)
                
                with col_coll1:
                    st.write(f"**Items:** {collection['items']}")
                    st.write(f"**Created:** {collection['created']}")
                    st.write(f"**Shared:** {'Yes' if collection['shared'] else 'No'}")
                
                with col_coll2:
                    tag_display = " ".join([f"`{tag}`" for tag in collection['tags']])
                    st.markdown(f"**Tags:** {tag_display}")
                
                col_coll_btn1, col_coll_btn2, col_coll_btn3, col_coll_btn4 = st.columns(4)
                with col_coll_btn1:
                    st.button("👁️ View", key=f"view_coll_{collection['name'][:10]}")
                with col_coll_btn2:
                    st.button("✏️ Edit", key=f"edit_coll_{collection['name'][:10]}")
                with col_coll_btn3:
                    st.button("📤 Export", key=f"export_coll_{collection['name'][:10]}")
                with col_coll_btn4:
                    st.button("🗑️ Delete", key=f"delete_coll_{collection['name'][:10]}")
        
        # Saved searches
        st.markdown("#### Saved Search Queries")
        
        saved_queries = [
            {
                "name": "Expiring Contracts Q4 2024",
                "query": "contract expiration:2024-10-01 TO 2024-12-31",
                "results": 12,
                "last_run": "2024-09-20",
                "alert": True
            },
            {
                "name": "Patent Litigation Cases",
                "query": "patent AND (litigation OR infringement)",
                "results": 45,
                "last_run": "2024-09-18", 
                "alert": False
            },
            {
                "name": "Confidential ABC Corp Documents",
                "query": "client:'ABC Corp' AND security:confidential",
                "results": 78,
                "last_run": "2024-09-19",
                "alert": False
            }
        ]
        
        for query in saved_queries:
            alert_icon = "🔔" if query['alert'] else "🔕"
            
            with st.expander(f"🔍 {query['name']} ({query['results']} results) {alert_icon}"):
                col_query1, col_query2 = st.columns(2)
                
                with col_query1:
                    st.code(query['query'])
                    st.write(f"**Last Run:** {query['last_run']}")
                
                with col_query2:
                    st.write(f"**Results:** {query['results']}")
                    st.write(f"**Alert:** {'Enabled' if query['alert'] else 'Disabled'}")
                
                col_query_btn1, col_query_btn2, col_query_btn3, col_query_btn4 = st.columns(4)
                with col_query_btn1:
                    st.button("▶️ Run", key=f"run_query_{query['name'][:10]}")
                with col_query_btn2:
                    st.button("✏️ Edit", key=f"edit_query_{query['name'][:10]}")
                with col_query_btn3:
                    st.button(f"{'🔔' if not query['alert'] else '🔕'} Alert", key=f"alert_query_{query['name'][:10]}")
                with col_query_btn4:
                    st.button("🗑️ Delete", key=f"delete_query_{query['name'][:10]}")
        
        # Search alerts and notifications
        st.markdown("#### Search Alerts & Notifications")
        
        with st.form("create_alert"):
            alert_name = st.text_input("Alert Name:", placeholder="e.g., New ABC Corp Documents")
            alert_query = st.text_input("Search Query:", placeholder="Enter search terms or query...")
            
            col_alert1, col_alert2 = st.columns(2)
            with col_alert1:
                alert_frequency = st.selectbox("Check Frequency:", ["Real-time", "Hourly", "Daily", "Weekly"])
            with col_alert2:
                notification_method = st.multiselect("Notify Via:", ["Email", "In-App", "SMS", "Slack"])
            
            if st.form_submit_button("🔔 Create Alert"):
                st.success(f"Alert '{alert_name}' created successfully!")
    
    with col2:
        st.markdown("#### Search Statistics")
        
        search_stats = [
            ("Total Searches", "1,247"),
            ("Saved Collections", "12"),
            ("Active Alerts", "5"),
            ("Shared Searches", "8")
        ]
        
        for stat, value in search_stats:
            st.metric(stat, value)
        
        st.markdown("#### Quick Actions")
        
        quick_actions = [
            "📁 New Collection",
            "🔍 Save Current Search", 
            "🔔 Create Alert",
            "📤 Export All",
            "⚙️ Search Settings",
            "📊 Usage Analytics"
        ]
        
        for action in quick_actions:
            if st.button(action, key=f"quick_{action[:10]}"):
                st.info(f"Opening {action}...")
        
        st.markdown("#### Search Insights")
        
        insights = [
            {"icon": "📈", "text": "Search volume up 15% this month"},
            {"icon": "🎯", "text": "AI search accuracy: 94.2%"},
            {"icon": "⚡", "text": "Avg search time: 0.8 seconds"},
            {"icon": "📱", "text": "Mobile searches: 34%"}
        ]
        
        for insight in insights:
            col_insight1, col_insight2 = st.columns([1, 4])
            with col_insight1:
                st.write(insight["icon"])
            with col_insight2:
                st.write(insight["text"])

# Main execution
if __name__ == "__main__":
    show()
