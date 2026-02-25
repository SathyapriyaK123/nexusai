import streamlit as st
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def show_memory():
    st.title("🧠 NexusAI Memory")
    st.caption("Everything NexusAI has learned so far")
    
    try:
        from memory.long_term import LongTermMemory
        ltm = LongTermMemory()
        stats = ltm.memory_stats()
        
        # Memory stats
        st.subheader("📊 Memory Stats")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Daily Briefings", stats.get("daily_briefings", 0))
        col2.metric("Trends Learned", stats.get("trends_history", 0))
        col3.metric("Decisions Made", stats.get("decisions", 0))
        col4.metric("Knowledge Items", stats.get("domain_knowledge", 0))
        
        st.divider()
        
        # Search memory
        st.subheader("🔍 Search Memory")
        query = st.text_input("Search for anything NexusAI has learned...")
        collection = st.selectbox(
            "Search in:",
            ["trends_history", "decisions", "daily_briefings", "domain_knowledge"]
        )
        
        if query:
            results = ltm.search_memory(query, collection, n_results=5)
            if results:
                for r in results:
                    meta = r.get("metadata", {})
                    with st.expander(f"📄 {meta.get('title', meta.get('decision', 'Memory item'))} — {meta.get('date', 'N/A')}"):
                        st.json(meta)
            else:
                st.info("No memories found for that search.")
        
        st.divider()
        
        # Recent trends
        st.subheader("📈 Recent Trends Learned")
        domain = st.session_state.get("domain", "AI Engineering and LLMs")
        recent = ltm.get_recent_trends(domain, days=7)
        
        if recent:
            for t in recent:
                st.success(f"**{t.get('title', 'Trend')}** ({t.get('date', 'N/A')})")
                st.write(t.get('summary', ''))
        else:
            st.info("No recent trends in memory yet. Run NexusAI first!")
            
    except Exception as e:
        st.error(f"Memory error: {str(e)}")