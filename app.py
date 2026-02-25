import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

st.set_page_config(
    page_title="NexusAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.title("🤖 NexusAI")
    st.caption("Autonomous AI Chief of Staff")
    st.divider()
    
    page = st.radio(
        "Navigate",
        ["🏠 Home", "🧠 Memory", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.caption("Built with LangGraph + Groq")

if page == "🏠 Home":
    from ui.home import show_home
    show_home()

elif page == "🧠 Memory":
    from ui.memory_view import show_memory
    show_memory()

elif page == "⚙️ Settings":
    from ui.settings import show_settings
    show_settings()