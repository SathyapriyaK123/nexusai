import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def show_settings():
    st.title("⚙️ NexusAI Settings")
    st.caption("Configure your autonomous AI chief of staff")
    
    st.subheader("👤 Your Profile")
    
    domain = st.text_input(
        "Your Domain",
        value=st.session_state.get("domain", "AI Engineering and LLMs"),
        help="What field or industry are you in?"
    )
    
    goal = st.text_area(
        "Your Goal",
        value=st.session_state.get("goal", "I want to become an AI engineer and grow my LinkedIn presence"),
        help="What are you trying to achieve?",
        height=100
    )
    
    st.subheader("👥 Competitors / Key Players to Track")
    
    competitors_text = st.text_area(
        "Enter one name per line",
        value="\n".join(st.session_state.get("competitors", [
            "Andrej Karpathy",
            "Harrison Chase",
            "Swyx AI Engineer"
        ])),
        height=120
    )
    
    st.subheader("📱 Platforms")
    linkedin = st.checkbox("LinkedIn", value=True)
    twitter = st.checkbox("Twitter / X", value=True)
    
    st.divider()
    
    if st.button("💾 Save Settings", type="primary", use_container_width=True):
        st.session_state["domain"] = domain
        st.session_state["goal"] = goal
        st.session_state["competitors"] = [
            c.strip() for c in competitors_text.split("\n") if c.strip()
        ]
        platforms = []
        if linkedin:
            platforms.append("LinkedIn")
        if twitter:
            platforms.append("Twitter")
        st.session_state["platforms"] = platforms
        st.success("✅ Settings saved! Go to Home to run NexusAI.")