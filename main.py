import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Skopos Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        max-width: 80%;
    }
    
    .user-message {
        background-color: #007bff;
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .bot-message {
        background-color: #f8f9fa;
        color: #333;
        border: 1px solid #dee2e6;
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 0.5rem 1rem;
    }
    
    .stButton > button {
        border-radius: 25px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    
    .chat-container {
        height: 70vh;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        background-color: #fafafa;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq client
@st.cache_resource
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("Please set your GROQ_API_KEY in the .env file")
        st.stop()
    return Groq(api_key=api_key)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "model" not in st.session_state:
    st.session_state.model = "llama-3.3-70b-versatile"

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    # Model selection
    model_options = {
        "llama-3.3-70b-versatile": "Llama 3.3 70B Versatile",
        "llama-3.1-70b-versatile": "Llama 3.1 70B Versatile",
        "llama-3.1-8b-instant": "Llama 3.1 8B Instant",
        "mixtral-8x7b-32768": "Mixtral 8x7B",
        "gemma-7b-it": "Gemma 7B IT"
    }
    
    selected_model = st.selectbox(
        "Choose Model",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        index=list(model_options.keys()).index(st.session_state.model)
    )
    
    st.session_state.model = selected_model
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    # Bot info
    st.markdown("## 🤖 About Skopos Bot")
    st.markdown("""
    **Skopos Bot** is an AI-powered chatbot powered by Groq's lightning-fast inference.
    
    **Features:**
    - Multiple model options
    - Real-time responses
    - Chat history
    - Modern UI
    """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit & Groq")

# Main header
st.markdown("""
<div class="main-header">
    <h1>🤖 Skopos Bot</h1>
    <p>Your AI Assistant powered by Groq</p>
</div>
""", unsafe_allow_html=True)

# Chat interface
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "Ask me anything...",
        placeholder="Type your message here...",
        key="user_input"
    )

with col2:
    send_button = st.button("Send", use_container_width=True, type="primary")

# Chat container
chat_container = st.container()

# Handle user input
if send_button and user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get bot response
    try:
        with st.spinner("Skopos Bot is thinking..."):
            client = get_groq_client()
            response = client.chat.completions.create(
                messages=st.session_state.messages,
                model=st.session_state.model,
                temperature=0.7,
                max_tokens=1000
            )
            
            bot_response = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.session_state.messages.append({"role": "assistant", "content": "Sorry, I encountered an error. Please try again."})

# Display chat messages
with chat_container:
    if st.session_state.messages:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>🤖 Skopos Bot:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #666;">
            <h3>👋 Welcome to Skopos Bot!</h3>
            <p>Start a conversation by typing a message above.</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Powered by Groq • Built with Streamlit</div>",
    unsafe_allow_html=True
)
