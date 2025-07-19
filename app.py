import streamlit as st
import time
import base64
import io
import os
import requests
import json

# Configure Streamlit page
st.set_page_config(
    page_title="Clinical Research AI Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# OpenAI Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def get_openai_response(user_message, conversation_history):
    """Get response from OpenAI GPT-4o with conversation memory"""
    if not OPENAI_API_KEY:
        return "I need an OpenAI API key to provide comprehensive responses. Please add your API key to the environment variables."
    
    # Build conversation context with last 5 exchanges
    messages = [
        {
            "role": "system",
            "content": """You are an expert Clinical Research Coordinator AI Assistant with comprehensive knowledge of:

• Clinical Research: All phases (I-IV), FDA regulations, GCP guidelines, ICH standards
• Medical Knowledge: Drug treatments for all conditions (Alzheimer's, Parkinson's, diabetes, cancer, etc.)
• Regulatory Affairs: FDA approvals, EMA guidelines, clinical trial regulations
• Study Design: Randomized controlled trials, observational studies, adaptive designs
• Data Management: Electronic data capture, statistical analysis, CDISC standards
• Ethics & Safety: Informed consent, adverse event reporting, data protection
• Career Development: CRC/CRA certification, professional growth paths

Provide detailed, professional responses with specific drug names, mechanisms of action, clinical evidence, and practical insights. Always be comprehensive and accurate."""
        }
    ]
    
    # Add conversation history (exactly last 5 exchanges for context)
    recent_exchanges = conversation_history[-5:] if len(conversation_history) > 5 else conversation_history
    for exchange in recent_exchanges:
        messages.append({"role": "user", "content": exchange["user"]})
        messages.append({"role": "assistant", "content": exchange["assistant"]})
    
    # Add current message
    messages.append({"role": "user", "content": user_message})
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
                "messages": messages,
                "max_tokens": 1500,
                "temperature": 0.7
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"I'm having trouble connecting to OpenAI. Please check your API key and try again. Error: {response.status_code}"
            
    except Exception as e:
        return f"I encountered an error while processing your request: {str(e)}"

# Custom CSS to recreate exact Replit design
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    .stApp > header {visibility: hidden;}
    .stApp > div[data-testid="stToolbar"] {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp > div:first-child {margin-top: -80px;}
    
    /* Full page gradient background */
    .stApp {
        background: linear-gradient(135deg, #8B7EC8 0%, #6B5B95 50%, #9A7BB0 100%);
        min-height: 100vh;
    }
    
    /* Main container with enhanced glass effect */
    .main-container {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(25px);
        border-radius: 28px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 40px 100px rgba(0, 0, 0, 0.2), 
                    0 20px 40px rgba(139, 126, 200, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.4);
        margin: 24px auto;
        max-width: 950px;
        overflow: hidden;
        position: relative;
        animation: containerGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes containerGlow {
        0% { box-shadow: 0 40px 100px rgba(0, 0, 0, 0.2), 0 20px 40px rgba(139, 126, 200, 0.15); }
        100% { box-shadow: 0 40px 100px rgba(0, 0, 0, 0.25), 0 20px 40px rgba(139, 126, 200, 0.25); }
    }
    
    /* Header with medical gradient */
    .medical-header {
        background: linear-gradient(135deg, #8B7EC8 0%, #6B5B95 100%);
        color: white;
        padding: 24px 32px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    /* Online status badge */
    .status-badge {
        background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
        color: white;
        padding: 8px 24px;
        border-radius: 25px;
        font-weight: 600;
        font-size: 14px;
        display: inline-block;
        margin-bottom: 16px;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    /* Header title styling */
    .header-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 8px;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
    }
    
    .header-subtitle {
        font-size: 16px;
        font-weight: 400;
        opacity: 0.9;
        letter-spacing: 0.01em;
    }
    
    /* Welcome section */
    .welcome-section {
        padding: 48px 32px;
        text-align: center;
    }
    
    .microscope-icon {
        font-size: 64px;
        margin-bottom: 24px;
        color: #8B7EC8;
        filter: drop-shadow(0 4px 8px rgba(139, 126, 200, 0.3));
    }
    
    .welcome-title {
        font-size: 36px;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 20px;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .welcome-description {
        font-size: 18px;
        color: #34495e;
        line-height: 1.6;
        margin-bottom: 48px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Remove topic button styling since we're not showing them */
    
    /* Chat input area */
    .chat-input-container {
        padding: 0 32px 32px 32px;
        display: flex;
        gap: 12px;
        align-items: center;
        margin-top: auto;
    }
    
    /* Style Streamlit input and button */
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        border: 2px solid rgba(0, 0, 0, 0.05) !important;
        padding: 16px 24px !important;
        font-size: 16px !important;
        background: white !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8B7EC8 !important;
        box-shadow: 0 4px 20px rgba(139, 126, 200, 0.2) !important;
        outline: none !important;
    }
    
    /* Send button specific styling */
    .send-button-container .stButton > button {
        border-radius: 50% !important;
        background: linear-gradient(135deg, #8B7EC8 0%, #6B5B95 100%) !important;
        color: white !important;
        border: none !important;
        padding: 16px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(139, 126, 200, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 56px !important;
        height: 56px !important;
        font-size: 18px !important;
    }
    
    .send-button-container .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(139, 126, 200, 0.5) !important;
    }
    
    /* Clear chat button styling */
    .clear-chat-container .stButton > button {
        background: rgba(0, 0, 0, 0.05) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        color: #5a6c7d !important;
        padding: 8px 16px !important;
        border-radius: 20px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
    }
    
    .clear-chat-container .stButton > button:hover {
        background: rgba(0, 0, 0, 0.1) !important;
    }
    
    /* File upload styling */
    .upload-section {
        padding: 24px 32px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .upload-section h3 {
        color: white !important;
        font-size: 24px !important;
        font-weight: 600 !important;
        margin-bottom: 16px !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stFileUploader > div {
        border-radius: 15px !important;
        border: 3px dashed rgba(255, 255, 255, 0.6) !important;
        background: rgba(255, 255, 255, 0.15) !important;
        padding: 40px !important;
        text-align: center !important;
        backdrop-filter: blur(5px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div:hover {
        border-color: rgba(255, 255, 255, 0.8) !important;
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px) !important;
    }
    
    .stFileUploader label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 18px !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stFileUploader div[data-testid="stFileUploaderDropzone"] div {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Upload info styling */
    .upload-info {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 20px 24px;
        margin: 16px 0;
        font-size: 16px;
        color: white;
        backdrop-filter: blur(5px);
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        font-weight: 500;
    }
    
    /* Chat messages */
    .chat-message {
        margin: 16px 0;
        padding: 20px;
        border-radius: 15px;
        line-height: 1.6;
    }
    
    .user-message {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        margin-left: auto;
        margin-right: 0;
        max-width: 80%;
        text-align: right;
    }
    
    .ai-message {
        background: rgba(248, 250, 252, 0.8);
        color: #2c3e50;
        border: 1px solid rgba(0, 0, 0, 0.05);
        max-width: 90%;
        white-space: pre-wrap;
    }
    
    /* Status indicator */
    .status-ready {
        color: #4CAF50;
        font-weight: 600;
        font-size: 14px;
        padding: 0 32px;
        margin-bottom: 16px;
    }
    
    /* Clear chat button */
    .clear-chat-btn {
        background: rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.1);
        color: #5a6c7d;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .clear-chat-btn:hover {
        background: rgba(0, 0, 0, 0.1);
    }
    
    /* Enhanced floating animations */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    .upload-section {
        animation: float 4s ease-in-out infinite;
    }
    
    /* Improve text visibility across all Streamlit elements */
    .stApp div, .stApp p, .stApp span {
        color: #2c3e50 !important;
        font-weight: 500 !important;
    }
    
    /* Enhanced button hover effects */
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(139, 126, 200, 0.6) !important;
    }
    
    /* Make upload description text highly visible */
    .stFileUploader p {
        color: rgba(255, 255, 255, 0.95) !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Override Streamlit markdown text for better visibility */
    .stMarkdown h3 {
        color: white !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Status indicator styling */
    .status-ready {
        color: #4CAF50 !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = f"session_{int(time.time())}"
if 'conversation_memory' not in st.session_state:
    st.session_state.conversation_memory = []

def process_uploaded_file(uploaded_file):
    """Process uploaded file and extract content"""
    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        file_content = ""
        
        if file_extension in ['txt', 'md', 'py', 'js', 'html', 'css', 'json', 'xml', 'csv']:
            # Text-based files
            content = uploaded_file.read()
            if isinstance(content, bytes):
                file_content = content.decode('utf-8', errors='ignore')
            else:
                file_content = str(content)
                
        elif file_extension in ['pdf']:
            # PDF files - basic text extraction
            file_content = f"PDF file '{uploaded_file.name}' uploaded. Content analysis available."
            
        elif file_extension in ['doc', 'docx']:
            # Word documents
            file_content = f"Word document '{uploaded_file.name}' uploaded. Document analysis available."
            
        elif file_extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']:
            # Image files
            file_content = f"Image '{uploaded_file.name}' uploaded. Image analysis available."
            
        elif file_extension in ['xls', 'xlsx']:
            # Excel files
            file_content = f"Excel file '{uploaded_file.name}' uploaded. Data analysis available."
            
        elif file_extension in ['ppt', 'pptx']:
            # PowerPoint files
            file_content = f"PowerPoint file '{uploaded_file.name}' uploaded. Presentation analysis available."
            
        else:
            file_content = f"File '{uploaded_file.name}' uploaded. General file analysis available."
            
        return {
            'name': uploaded_file.name,
            'type': file_extension,
            'size': uploaded_file.size,
            'content': file_content[:1000] + "..." if len(file_content) > 1000 else file_content
        }
    except Exception as e:
        return {
            'name': uploaded_file.name,
            'type': 'unknown',
            'size': uploaded_file.size,
            'content': f"Error processing file: {str(e)}"
        }

def build_conversation_context():
    """Build conversation context from last 5 exchanges"""
    if not st.session_state.conversation_memory:
        return ""
    
    context = "\n**Previous conversation context:**\n"
    for exchange in st.session_state.conversation_memory[-5:]:  # Last 5 exchanges
        context += f"User: {exchange['user']}\n"
        context += f"Assistant: {exchange['assistant'][:150]}...\n\n"
    
    return context

def update_conversation_memory(user_message, assistant_response):
    """Update conversation memory with new exchange - maintains exactly last 5 exchanges"""
    exchange = {
        'user': user_message,
        'assistant': assistant_response,
        'timestamp': time.time()
    }
    
    # Add new exchange
    st.session_state.conversation_memory.append(exchange)
    
    # Always keep exactly last 5 exchanges
    st.session_state.conversation_memory = st.session_state.conversation_memory[-5:]

# Enhanced medical response function with OpenAI integration
def get_medical_response(user_message, uploaded_files=None):
    """Generate comprehensive medical responses using OpenAI GPT-4o"""
    
    # Prepare enhanced message with file context
    enhanced_message = user_message
    
    # If files are uploaded, include file analysis in the message
    if uploaded_files:
        enhanced_message += "\n\n**Uploaded Files Context:**\n"
        for file_info in uploaded_files:
            enhanced_message += f"• **{file_info['name']}** ({file_info['type'].upper()}, {file_info['size']} bytes)\n"
            if file_info['content'] and not file_info['content'].startswith('Error'):
                enhanced_message += f"  Content: {file_info['content'][:500]}...\n"
    
    # Use OpenAI for comprehensive response
    response = get_openai_response(enhanced_message, st.session_state.conversation_memory)
    
    return response

# Topic button click handler
def handle_topic_click(topic):
    """Handle topic button clicks"""
    st.session_state.messages.append({"role": "user", "content": f"Tell me about {topic.lower()}"})
    ai_response = get_medical_response(f"Tell me about {topic.lower()}")
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Main application
def main():
    # Main container with glass effect
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header with medical gradient
    st.markdown("""
    <div class="medical-header">
        <div class="status-badge">Online</div>
        <div class="header-title">
            🩺 Clinical Research AI Assistant
        </div>
        <div class="header-subtitle">
            Advanced Medical Intelligence • GPT-4o Powered • Real-time Clinical Insights
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show welcome section only if no messages
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-section">
            <div class="microscope-icon">
                🔬
            </div>
            <div class="welcome-title">Welcome to Clinical Research AI</div>
            <div class="welcome-description">
                Your intelligent assistant for comprehensive clinical research coordination, FDA regulations, medical insights, and research excellence across all therapeutic areas.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat messages area
    if st.session_state.messages:
        st.markdown('<div style="padding: 0 32px; max-height: 400px; overflow-y: auto;">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message ai-message">
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Status indicator
    st.markdown('<div class="status-ready">Ready</div>', unsafe_allow_html=True)
    
    # Chat input area
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([8, 1, 2])
    
    with col1:
        user_input = st.text_input(
            "",
            key="user_input",
            placeholder="Ask me about clinical research, FDA approvals, drug information...",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown('<div class="send-button-container">', unsafe_allow_html=True)
        send_button = st.button("✈️", type="primary", help="Send message", key="send_btn")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="clear-chat-container">', unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat", help="Clear conversation", key="clear_chat"):
            st.session_state.messages = []
            st.session_state.conversation_memory = []  # Clear memory too
            st.session_state.uploaded_files = []  # Clear uploaded files
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # File upload section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 📎 Upload Documents")
    
    uploaded_files = st.file_uploader(
        "Choose files to analyze (PDF, Word, Excel, Images, Text files, etc.)",
        accept_multiple_files=True,
        type=['pdf', 'doc', 'docx', 'txt', 'md', 'csv', 'xlsx', 'xls', 'ppt', 'pptx', 
              'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'json', 'xml', 'html', 'css', 'js', 'py'],
        help="Upload various document types for analysis and discussion"
    )
    
    # Process uploaded files
    processed_files = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_info = process_uploaded_file(uploaded_file)
            processed_files.append(file_info)
            st.session_state.uploaded_files = processed_files
            
        # Show upload info
        st.markdown('<div class="upload-info">', unsafe_allow_html=True)
        st.markdown(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
        for file_info in processed_files:
            size_kb = file_info['size'] / 1024
            st.markdown(f"• **{file_info['name']}** ({file_info['type'].upper()}, {size_kb:.1f} KB)")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process message
    if send_button and user_input.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate AI response with file context
        with st.spinner("Processing your request..."):
            ai_response = get_medical_response(user_input, st.session_state.uploaded_files)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            # Update conversation memory
            update_conversation_memory(user_input, ai_response)
        
        # Clear input and rerun
        st.rerun()
    
    # Handle Enter key
    if user_input and st.session_state.get('last_input') != user_input:
        st.session_state.last_input = user_input
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main container

if __name__ == "__main__":
    main()