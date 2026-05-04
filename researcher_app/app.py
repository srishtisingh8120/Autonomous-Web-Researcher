import streamlit as st
import os
import json
from agent import ResearchAgent
from dotenv import load_dotenv
from tracing import tracer

load_dotenv()

# Page Config
st.set_page_config(page_title="AI Web Researcher", page_icon="🔍", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    .report-container {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #4b4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Autonomous Web Researcher")
st.markdown("Give me a topic, and I'll scour the web to write a detailed report for you.")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    model = st.selectbox("Select Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
    max_calls = st.slider("Max API Calls", 5, 20, 10)
    st.info("Built with Groq & DuckDuckGo")

# Main Input
query = st.text_input("What would you like to research?", placeholder="e.g. Latest breakthroughs in fusion energy")

if st.button("Start Research"):
    if not query:
        st.warning("Please enter a topic!")
    else:
        # We'll use a container to show progress
        status_container = st.status("Initializing Agent...", expanded=True)
        
        try:
            agent = ResearchAgent()
            agent.model = model
            agent.max_calls = max_calls
            
            # Since the agent prints to stdout, we can't easily capture it without redirecting
            # For now, let's just run it and show the final result.
            # In a more advanced version, we'd pass a callback to the agent.
            
            status_container.update(label="Searching and Scraping the Web...", state="running")
            
            report = agent.run(query)
            
            # Export trace after the agent span finishes to ensure the root is captured
            tracer.export_trace(output=report, query=query)
            
            status_container.update(label="Research Complete!", state="complete", expanded=False)
            
            st.markdown("### 📝 Research Report")
            st.markdown(f'<div class="report-container">{report}</div>', unsafe_allow_html=True)
            
            # Download Button
            st.download_button(
                label="Download Report as Markdown",
                data=report,
                file_name="research_report.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.divider()
st.caption("Powered by Sigmoid Agentic Framework")
