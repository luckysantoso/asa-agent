import streamlit as st
import os
import subprocess
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Asa",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS - Keep the beautiful header design
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .status-box {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .status-ready {
        background: linear-gradient(135deg, #d1ecf1, #e8f8f0);
        color: #0c5460;
        border: 2px solid #bee5eb;
        box-shadow: 0 4px 15px rgba(192, 245, 236, 0.4);
    }
    .status-error {
        background: linear-gradient(135deg, #f8d7da, #ffe6e6);
        color: #721c24;
        border: 2px solid #f5c6cb;
        box-shadow: 0 4px 15px rgba(248, 215, 218, 0.4);
    }
    .status-running {
        background: linear-gradient(135deg, #d4edda, #e8f8e8);
        color: #155724;
        border: 2px solid #c3e6cb;
        box-shadow: 0 4px 15px rgba(212, 237, 218, 0.4);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 4px 15px rgba(212, 237, 218, 0.4); }
        50% { box-shadow: 0 6px 20px rgba(212, 237, 218, 0.7); }
        100% { box-shadow: 0 4px 15px rgba(212, 237, 218, 0.4); }
    }
    .control-section {
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #dee2e6;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .simple-info {
        background: linear-gradient(135deg, #e7f3ff, #f0f8ff);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent_running' not in st.session_state:
    st.session_state.agent_running = False
if 'process' not in st.session_state:
    st.session_state.process = None

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 Asa AI Agent (Beta)</h1>
    <p>Practice your interview with Asa</p>
</div>
""", unsafe_allow_html=True)

# Load configuration from .env
agent_id = os.getenv("AGENT_ID", "")
api_key = os.getenv("ELEVENLABS_API_KEY", "")
config_valid = bool(agent_id and api_key)


# Main controls - only show if config is valid
if config_valid:
    st.markdown("### Start Interview")
    
    # Current status
    if st.session_state.agent_running:
        st.markdown("""
        <div class="status-box status-running">
            🟢 Agent is Running - Speak Now!
        </div>
        """, unsafe_allow_html=True)
        
        # Check if process is still alive
        if st.session_state.process and st.session_state.process.poll() is not None:
            st.session_state.agent_running = False
            st.session_state.process = None
            st.warning("⚠️ Agent process ended unexpectedly")
            st.rerun()
            
    else:
        st.markdown("""
        <div class="status-box status-error">
            🔴 Agent is Not Running
        </div>
        """, unsafe_allow_html=True)
    
    # Control buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            "🚀 Start Agent", 
            use_container_width=True, 
            disabled=st.session_state.agent_running,
            type="primary"
        ):
            try:
                # Start the main.py process
                st.session_state.process = subprocess.Popen(
                    [sys.executable, "main.py"],
                    cwd=os.getcwd(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                st.session_state.agent_running = True
                st.success("✅ Agent started! Speak into your microphone.")
                time.sleep(1)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error starting agent: {str(e)}")
    
    with col2:
        if st.button(
            "⏹️ Stop Agent", 
            use_container_width=True, 
            disabled=not st.session_state.agent_running,
            type="secondary"
        ):
            if st.session_state.process:
                try:
                    st.session_state.process.terminate()
                    st.session_state.process = None
                    st.session_state.agent_running = False
                    st.success("✅ Agent stopped!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error stopping agent: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Simple instructions
    st.markdown("### 📋 How to Use")
    
    st.markdown("""
    **Simple Steps:**
    1. 🚀 **Click "Start Agent"** to begin
    2. 🎤 **Speak clearly** into your microphone
    3. 🤖 **Listen** as the AI responds
    4. ⏹️ **Click "Stop Agent"** when done
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Show setup instructions when config is missing
    st.markdown('<div class="control-section">', unsafe_allow_html=True)
    st.markdown("### 🔧 Setup Required")
    
    st.markdown("""
    Please create a `.env` file with your ElevenLabs credentials to get started.
    
    **Example .env file:**
    ```
    AGENT_ID="agent_xxxxxxxxxxxxxxxxx"
    ELEVENLABS_API_KEY="sk_xxxxxxxxxxxxxxxxx"
    ```
    """)
    
    if st.button("🔄 Reload Configuration", use_container_width=True):
        load_dotenv(override=True)
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh when agent is running for real-time status
if st.session_state.agent_running:
    time.sleep(0.5)
    st.rerun()

# Simple footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "🤖 Powered by Raih Asa"
    "</div>", 
    unsafe_allow_html=True
)
