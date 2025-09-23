import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def show():
    st.markdown("""
    <div class="main-header">
        <h1>🔍 Advanced Search & Discovery</h1>
        <p>Comprehensive search across documents, matters, communications, and legal databases</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Universal Search", 
        "📄 Document Search", 
        "📊 Data Analytics", 
        "🤖 AI-Powered Search", 
        "📚 Legal Research"
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
                "relevance": 95
            },
            {
                "type": "Email",
                "title": "RE: Contract Review Feedback",
                "content": "Please review the attached contract amendments and provide feedback by EOD Friday...",
                "author": "John Smith",
                "date": "2024-09-22",
                "matter": "XYZ Services Agreement",
                "relevance": 88
            },
            {
                "type": "Matter",
                "title": "Continental Corp Defense - Patent Infringement",
                "content": "Defending against patent infringement claims related to software algorithms...",
                "author": "Mike Davis",
                "date": "2024-09-15",
                "matter": "Continental Corp Defense",
                "relevance": 82
            },
            {
                "type": "Document",
                "title": "Discovery Response Template.pdf",
                "content": "Standard template for responding to discovery requests in civil litigation matters...",
                "author": "Emily Chen",
                "date": "2024-09-18",
                "matter": "Johnson vs. Tech Solutions",
                "relevance": 76
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
        
        # Display results
        for i, result in enumerate(search_results, 1):
            type_icons = {"Document": "📄", "Email": "📧", "Matter": "⚖️", "Task": "✅", "Contact": "👤"}
            
            with st.expander(f"{type_icons.get(result['type'], '📄')} {result['title']} ({result['relevance']}% relevant)"):
                col_res1, col_res2 = st.columns([3, 1])
                
                with col_res1:
                    st.write(f"**Content Preview:** {result['content']}")
                    st.write(f"**Type:** {result['type']} | **Author:** {result['author']} | **Date:** {result['date']}")
                    st.write(f"**Related Matter:** {result['matter']}")
                
                with col_res2:
                    st.progress(result['relevance'] / 100)
                    st.write(f"Relevance: {result['relevance']}%")
                    
                    if st.button(f"📖 Open", key=f"open_{i}"):
                        st.info(f"Opening {result['title']}...")
                    if st.button(f"📎 Add to Collection", key=f"collect_{i}"):
                        st.success("Added to collection!")

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
            
            with col_adv2:
                metadata_search = st.checkbox("Include Metadata Search")
                version_control = st.checkbox("Search All Versions")
                annotations = st.checkbox("Include Annotations & Comments")
        
        if st.button("🔍 Search Documents", type="primary"):
            st.markdown("#### Document Search Results")
            
            # Mock document results
            document_results = [
                {
                    "filename": "ABC_Corp_Merger_Agreement_v3.2.pdf",
                    "size": "2.4 MB",
                    "pages": 47,
                    "last_modified": "2024-09-20",
                    "author": "Sarah Johnson",
                    "matter": "ABC Corp Acquisition",
                    "matches": 12,
                    "relevance": 94
                },
                {
                    "filename": "Patent_Defense_Strategy_Draft.docx",
                    "size": "856 KB",
                    "pages": 23,
                    "last_modified": "2024-09-19",
                    "author": "Mike Davis",
                    "matter": "Continental Corp Defense",
                    "matches": 8,
                    "relevance": 87
                },
                {
                    "filename": "Discovery_Response_Johnson_Case.pdf",
                    "size": "1.7 MB",
                    "pages": 15,
                    "last_modified": "2024-09-18",
                    "author": "Emily Chen",
                    "matter": "Johnson vs. Tech Solutions",
                    "matches": 6,
                    "relevance": 79
                }
            ]
            
            for doc in document_results:
                with st.expander(f"📄 {doc['filename']} ({doc['matches']} matches, {doc['relevance']}% relevant)"):
                    col_doc1, col_doc2, col_doc3 = st.columns(3)
                    
                    with col_doc1:
                        st.write(f"**Size:** {doc['size']}")
                        st.write(f"**Pages:** {doc['pages']}")
                        st.write(f"**Modified:** {doc['last_modified']}")
                    
                    with col_doc2:
                        st.write(f"**Author:** {doc['author']}")
                        st.write(f"**Matter:** {doc['matter']}")
                        st.write(f"**Matches:** {doc['matches']}")
                    
                    with col_doc3:
                        st.progress(doc['relevance'] / 100)
                        st.write(f"Relevance: {doc['relevance']}%")
                    
                    # Action buttons
                    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
                    with col_btn1:
                        st.button("👁️ Preview", key=f"preview_{doc['filename'][:10]}")
                    with col_btn2:
                        st.button("📥 Download", key=f"download_{doc['filename'][:10]}")
                    with col_btn3:
                        st.button("✏️ Annotate", key=f"annotate_{doc['filename'][:10]}")
                    with col_btn4:
                        st.button("📧 Share", key=f"share_{doc['filename'][:10]}")
    
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
            "✅ Final Versions"
        ]
        
        for filter_option in quick_filters:
            if st.button(filter_option, key=f"filter_{filter_option[:5]}"):
                st.info(f"Applied filter: {filter_option}")
        
        st.markdown("#### Saved Searches")
        saved_searches = [
            "Contract amendments 2024",
            "Patent litigation docs",
            "Client correspondence",
            "Discovery materials"
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
        
        st.line_chart(search_data.set_index('Date'))
        
        st.markdown("#### Most Searched Terms")
        
        search_terms = pd.DataFrame({
            'Term': ['contract', 'agreement', 'liability', 'intellectual property', 'termination', 'confidentiality'],
            'Frequency': [247, 198, 156, 134, 112, 98],
            'Trend': ['↗️', '↗️', '→', '↗️', '↘️', '→']
        })
        
        for _, row in search_terms.iterrows():
            col_term1, col_term2, col_term3 = st.columns([2, 1, 1])
            with col_term1:
                st.write(f"**{row['Term']}**")
            with col_term2:
                st.write(f"{row['Frequency']} searches")
            with col_term3:
                st.write(row['Trend'])
    
    with col2:
        st.markdown("#### Document Access Patterns")
        
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
            ("Standard_NDA_Template.docx", 87),
            ("Employment_Agreement_2024.pdf", 72),
            ("IP_License_Agreement.docx", 64),
            ("Merger_Checklist.xlsx", 58),
            ("Litigation_Timeline.pdf", 45)
        ]
        
        for doc, access_count in top_docs:
            col_acc1, col_acc2 = st.columns([3, 1])
            with col_acc1:
                st.write(f"📄 {doc}")
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
        
        if st.button("🤖 AI Search", type="primary"):
            st.markdown("#### AI Search Results & Analysis")
            
            # AI interpretation
            st.info("🤖 **AI Interpretation:** I understand you're looking for contract documents related to ABC Corp with upcoming expiration dates. Let me analyze the relevant documents and provide insights.")
            
            # AI-enhanced results
            ai_results = [
                {
                    "title": "ABC Corp Service Agreement",
                    "summary": "Multi-year service agreement covering IT support and maintenance. Key renewal clause on page 12.",
                    "entities": ["ABC Corp", "IT Services", "Renewal Clause", "John Smith"],
                    "sentiment": "Neutral",
                    "expiry_date": "2024-12-15",
                    "ai_insights": "Contract contains auto-renewal clause. Recommend review 90 days before expiry.",
                    "confidence": 94
                },
                {
                    "title": "ABC Corp NDA Extension",
                    "summary": "Non-disclosure agreement extension with specific IP protection clauses.",
                    "entities": ["ABC Corp", "NDA", "IP Protection", "Confidentiality"],
                    "sentiment": "Positive",
                    "expiry_date": "2025-01-30",
                    "ai_insights": "Strong IP protection. No immediate action required.",
                    "confidence": 87
                }
            ]
            
            for result in ai_results:
                with st.expander(f"🤖 {result['title']} (AI Confidence: {result['confidence']}%)"):
                    col_ai_res1, col_ai_res2 = st.columns(2)
                    
                    with col_ai_res1:
                        st.write(f"**AI Summary:** {result['summary']}")
                        st.write(f"**Key Entities:** {', '.join(result['entities'])}")
                        st.write(f"**Sentiment:** {result['sentiment']}")
                    
                    with col_ai_res2:
                        st.write(f"**Expiry Date:** {result['expiry_date']}")
                        st.write(f"**AI Insights:** {result['ai_insights']}")
                        st.progress(result['confidence'] / 100)
                    
                    # AI action buttons
                    col_ai_btn1, col_ai_btn2, col_ai_btn3 = st.columns(3)
                    with col_ai_btn1:
                        st.button("📝 Generate Summary", key=f"ai_summary_{result['title'][:10]}")
                    with col_ai_btn2:
                        st.button("🔍 Deep Analysis", key=f"ai_analysis_{result['title'][:10]}")
                    with col_ai_btn3:
                        st.button("⚡ Quick Actions", key=f"ai_actions_{result['title'][:10]}")
    
    with col2:
        st.markdown("#### AI Assistant")
        
        st.markdown("##### Query Suggestions")
        suggestions = [
            "Find overdue contracts",
            "Show high-risk documents",
            "Contracts expiring soon",
            "Documents needing review",
            "Recent amendments"
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
            "⚠️ Risk Identification"
        ]
        
        for capability in capabilities:
            st.write(capability)

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
        
        if st.button("📚 Search Legal Database", type="primary"):
            st.markdown("#### Legal Research Results")
            
            legal_results = [
                {
                    "title": "Smith v. Technology Corp (2023)",
                    "court": "9th Circuit Court of Appeals",
                    "date": "2023-08-15",
                    "citation": "987 F.3d 456 (9th Cir. 2023)",
                    "relevance": 96,
                    "summary": "Case addressing intellectual property rights in software development contracts...",
                    "key_holdings": ["IP ownership in work-for-hire", "Contract interpretation standards"]
                },
                {
                    "title": "Patent Protection Act § 201",
                    "source": "Federal Statute",
                    "date": "2022-12-01",
                    "citation": "35 U.S.C. § 201",
                    "relevance": 91,
                    "summary": "Federal statute governing patent ownership and licensing requirements...",
                    "key_provisions": ["Patent licensing", "Government rights", "Small business protections"]
                },
                {
                    "title": "Johnson Industries v. Innovation LLC (2022)",
                    "court": "Federal District Court",
                    "date": "2022-11-22",
                    "citation": "2022 U.S. Dist. LEXIS 45678",
                    "relevance": 88,
                    "summary": "District court decision on trade secret misappropriation claims...",
                    "key_holdings": ["Trade secret definition", "Reasonable measures requirement"]
                }
            ]
            
            for result in legal_results:
                with st.expander(f"⚖️ {result['title']} ({result['relevance']}% relevant)"):
                    col_legal_res1, col_legal_res2 = st.columns(2)
                    
                    with col_legal_res1:
                        st.write(f"**Court/Source:** {result.get('court', result.get('source', 'N/A'))}")
                        st.write(f"**Date:** {result['date']}")
                        st.write(f"**Citation:** {result['citation']}")
                        st.write(f"**Summary:** {result['summary']}")
                    
                    with col_legal_res2:
                        st.progress(result['relevance'] / 100)
                        st.write(f"Relevance: {result['relevance']}%")
                        
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
    
    with col2:
        st.markdown("#### Research Tools")
        
        research_tools = [
            "📚 Case Law Database",
            "📜 Statute Finder",
            "📋 Regulation Search",
            "📄 Legal Forms Library",
            "🔍 Citation Validator"
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
            "Corporate governance"
        ]
        
        for research in recent_research:
            st.write(f"• {research}")
        
        st.markdown("#### Citation Manager")
        if st.button("📚 Manage Citations"):
            st.info("Opening citation manager...")
        if st.button("📝 Generate Bibliography"):
            st.info("Generating bibliography...")
        if st.button("🔍 Check Citations"):
            st.info("Validating citations...")
