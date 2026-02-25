import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def show_home():
    st.title("🏠 NexusAI Daily Briefing")
    
    # Load settings
    domain = st.session_state.get("domain", "AI Engineering and LLMs")
    goal = st.session_state.get("goal", "I want to become an AI engineer")
    competitors = st.session_state.get("competitors", ["Andrej Karpathy", "Harrison Chase"])
    
    # Show current settings
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📌 **Domain:** {domain}")
    with col2:
        st.info(f"🎯 **Goal:** {goal}")
    
    st.divider()
    
    # Run button
    if st.button("🚀 Run NexusAI Now", type="primary", use_container_width=True):
        
        with st.spinner("🤖 NexusAI is working autonomously..."):
            
            # Progress tracking
            progress = st.progress(0)
            status = st.empty()
            
            try:
                status.text("🧠 Retrieving past memories...")
                progress.progress(10)
                
                status.text("🔍 Searching web for trends...")
                progress.progress(25)
                
                status.text("💬 Analyzing community sentiment...")
                progress.progress(40)
                
                status.text("👥 Tracking competitors...")
                progress.progress(55)
                
                status.text("📋 Creating daily plan...")
                progress.progress(65)
                
                status.text("✍️ Writing content...")
                progress.progress(75)
                
                status.text("🔄 Running self-correction loop...")
                progress.progress(85)
                
                status.text("💾 Saving to memory...")
                progress.progress(95)
                
                # Run the actual pipeline
                from agents.orchestrator import run_nexusai
                result = run_nexusai(
                    domain=domain,
                    goal=goal,
                    competitors=competitors,
                    platforms=["LinkedIn", "Twitter"]
                )
                
                progress.progress(100)
                status.text("✅ Done!")
                
                # Store result in session
                st.session_state["last_result"] = result
                st.success("✅ NexusAI completed successfully!")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                return
    
    st.divider()
    
    # Show results if available
    if "last_result" in st.session_state:
        result = st.session_state["last_result"]
        content = result.get("final_content", {})
        plan = result.get("daily_plan", {})
        trends = result.get("trends", {}).get("trends", [])
        
        # Top trend
        if trends:
            st.subheader("🔥 Top Trend Today")
            st.warning(f"**{trends[0]['title']}** — {trends[0]['summary']}")
        
        # Daily plan
        st.subheader("📋 Your Plan")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Priority", "✅ Set")
            st.write(plan.get("top_priority", "N/A"))
        with col2:
            st.metric("Learn", "📚 Focus")
            st.write(plan.get("learning_focus", "N/A"))
        with col3:
            st.metric("Avoid", "🚫 Skip")
            st.write(plan.get("avoid_today", "N/A"))
        
        st.divider()
        
        # LinkedIn post
        st.subheader(f"📱 LinkedIn Post — Score: {content.get('linkedin_score', 'N/A')}/10")
        linkedin = content.get("linkedin_post", "Not generated")
        st.text_area("LinkedIn Post", linkedin, height=250, key="linkedin")
        if st.button("📋 Copy LinkedIn Post"):
            st.write("✅ Copied! (Select all text above and copy)")
        
        st.divider()
        
        # Twitter thread
        st.subheader("🐦 Twitter Thread")
        for i, tweet in enumerate(content.get("twitter_thread", []), 1):
            st.text_area(f"Tweet {i}", tweet, height=80, key=f"tweet_{i}")
        
        st.divider()
        
        # Networking message
        st.subheader("🤝 Networking Message")
        networking = content.get("networking_message", "Not generated")
        st.text_area("Networking Message", networking, height=120, key="networking")
        
        # Errors
        if result.get("errors"):
            with st.expander("⚠️ Errors encountered"):
                for e in result["errors"]:
                    st.error(e)