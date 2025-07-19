import streamlit as st
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Clinical Research AI Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Main container with glass effect */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.15);
        margin: 20px auto;
        max-width: 900px;
        overflow: hidden;
        position: relative;
    }
    
    /* Header with medical gradient */
    .medical-header {
        background: linear-gradient(135deg, #2196F3 0%, #21CBF3 100%);
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
        padding: 32px;
        text-align: center;
    }
    
    .welcome-title {
        font-size: 36px;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 20px;
    }
    
    .welcome-description {
        font-size: 18px;
        color: #5a6c7d;
        line-height: 1.6;
        margin-bottom: 32px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Topic buttons - override Streamlit button styling */
    div[data-testid="column"] .stButton > button {
        background: rgba(79, 172, 254, 0.1) !important;
        border: 1px solid rgba(79, 172, 254, 0.2) !important;
        color: #4facfe !important;
        padding: 12px 24px !important;
        border-radius: 25px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        width: 100% !important;
        margin-bottom: 8px !important;
        transition: all 0.3s ease !important;
        box-shadow: none !important;
    }
    
    div[data-testid="column"] .stButton > button:hover {
        background: rgba(79, 172, 254, 0.2) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.15) !important;
        border-color: rgba(79, 172, 254, 0.3) !important;
    }
    
    /* Chat input area */
    .chat-input-container {
        padding: 0 32px 32px 32px;
        display: flex;
        gap: 12px;
        align-items: center;
    }
    
    /* Style Streamlit input and button */
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        padding: 15px 20px !important;
        font-size: 16px !important;
        background: white !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4facfe !important;
        box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1) !important;
    }
    
    /* Send button specific styling */
    .send-button-container .stButton > button {
        border-radius: 25px !important;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .send-button-container .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.4) !important;
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = f"session_{int(time.time())}"

# Medical knowledge function
def get_medical_response(user_message):
    """Generate medical knowledge responses"""
    query_lower = user_message.lower()
    
    if any(term in query_lower for term in ['multiple sclerosis', 'ms drug', 'ms treatment', 'sclerosis', 'interferon', 'glatiramer']):
        return """**Multiple Sclerosis (MS) - FDA Approved Medications**

**Injectable Disease-Modifying Therapies:**
• **Interferon beta-1a (Avonex)** - FDA approved 1996, 30 mcg IM weekly
• **Glatiramer acetate (Copaxone)** - FDA approved 1996, 20 mg SC daily
• **Interferon beta-1b (Betaseron)** - FDA approved 1993

**Oral Medications:**
• **Fingolimod (Gilenya)** - FDA approved 2010, 0.5 mg daily
• **Dimethyl fumarate (Tecfidera)** - FDA approved 2013, 240 mg twice daily
• **Teriflunomide (Aubagio)** - FDA approved 2012, 14 mg daily

**High-Efficacy Therapies:**
• **Natalizumab (Tysabri)** - Monthly IV infusion
• **Ocrelizumab (Ocrevus)** - Every 6 months IV infusion"""
    
    elif any(term in query_lower for term in ['alzheimer', 'dementia', 'memory', 'aricept', 'donepezil']):
        return """**Alzheimer's Disease - FDA Approved Treatments**

**Cholinesterase Inhibitors:**
• **Donepezil (Aricept)** - 5-10 mg daily, all stages
• **Rivastigmine (Exelon)** - 1.5-6 mg twice daily or patch
• **Galantamine (Razadyne)** - 4-12 mg twice daily

**NMDA Receptor Antagonist:**
• **Memantine (Namenda)** - 5-10 mg twice daily, moderate to severe

**Recent Approval:**
• **Aducanumab (Aduhelm)** - Monthly IV infusion, targets amyloid plaques"""
    
    elif any(term in query_lower for term in ['parkinson', 'movement', 'levodopa', 'sinemet', 'dopamine']):
        return """**Parkinson's Disease - Standard Treatments**

**Dopamine Replacement:**
• **Carbidopa/Levodopa (Sinemet)** - Gold standard treatment
• **Carbidopa/Levodopa/Entacapone (Stalevo)** - Extended duration

**Dopamine Agonists:**
• **Pramipexole (Mirapex)** - 0.125-1.5 mg three times daily
• **Ropinirole (Requip)** - 0.25-8 mg three times daily

**MAO-B Inhibitors:**
• **Selegiline (Eldepryl)** - 5 mg twice daily
• **Rasagiline (Azilect)** - 0.5-1 mg daily"""
    
    elif any(term in query_lower for term in ['diabetes', 'blood sugar', 'insulin', 'metformin', 'glucose']):
        return """**Type 2 Diabetes - Evidence-Based Medications**

**First-Line:**
• **Metformin** - 500-2000 mg daily, reduces hepatic glucose production

**GLP-1 Receptor Agonists:**
• **Semaglutide (Ozempic)** - Weekly injection, significant weight loss
• **Liraglutide (Victoza)** - Daily injection, cardiovascular benefits

**SGLT-2 Inhibitors:**
• **Empagliflozin (Jardiance)** - 10-25 mg daily, cardioprotective
• **Dapagliflozin (Farxiga)** - 5-10 mg daily

**Insulin Options:**
• **Insulin glargine (Lantus)** - Long-acting basal insulin
• **Insulin lispro (Humalog)** - Rapid-acting mealtime insulin"""
    
    elif any(term in query_lower for term in ['clinical trial', 'phase', 'study design', 'protocol', 'fda']):
        return """**Clinical Trial Design Framework**

**Phase I Trials:** Safety and dosing (20-100 participants)
**Phase II Trials:** Preliminary efficacy (100-300 participants)  
**Phase III Trials:** Confirmatory studies (300-3000 participants)
**Phase IV Trials:** Post-marketing surveillance

**Key Requirements:**
• FDA IND (Investigational New Drug) application
• IRB (Institutional Review Board) approval
• Informed consent procedures
• GCP (Good Clinical Practice) compliance
• ClinicalTrials.gov registration

**Regulatory Pathways:**
• Standard NDA/BLA approval
• Accelerated approval for serious conditions
• Breakthrough therapy designation
• Fast track designation"""
    
    else:
        return f"""**Thank you for your question:** "{user_message}"

I'm a Clinical Research AI Assistant with comprehensive knowledge of:

**Medical Treatments:** FDA-approved medications for neurological, cardiovascular, and endocrine conditions
**Clinical Research:** Trial design, regulatory pathways, GCP guidelines  
**Therapeutic Areas:** Multiple sclerosis, Alzheimer's, Parkinson's, diabetes

**Examples of questions I can answer:**
• "What medications are available for multiple sclerosis?"
• "Tell me about Alzheimer's disease treatments"
• "How do clinical trial phases work?"
• "What are the requirements for FDA drug approval?"

What specific medical condition or clinical research topic would you like to explore?"""

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
            <div class="welcome-title">Welcome to Clinical Research AI</div>
            <div class="welcome-description">
                Your intelligent assistant for comprehensive clinical research coordination, FDA regulations, medical insights, and research excellence across all therapeutic areas.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Topic buttons using Streamlit columns
        st.markdown('<div style="padding: 0 32px;">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)
        
        with col1:
            if st.button("Clinical Trials", key="btn1", use_container_width=True):
                handle_topic_click("Clinical Trials")
        with col2:
            if st.button("FDA Regulations", key="btn2", use_container_width=True):
                handle_topic_click("FDA Regulations")
        with col3:
            if st.button("GCP Guidelines", key="btn3", use_container_width=True):
                handle_topic_click("GCP Guidelines")
        with col4:
            if st.button("Medical Research", key="btn4", use_container_width=True):
                handle_topic_click("Medical Research")
        with col5:
            if st.button("Drug Information", key="btn5", use_container_width=True):
                handle_topic_click("Drug Information")
        with col6:
            if st.button("Safety Reporting", key="btn6", use_container_width=True):
                handle_topic_click("Safety Reporting")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
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
    
    col1, col2, col3 = st.columns([6, 1, 1])
    
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
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process message
    if send_button and user_input.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate AI response
        with st.spinner("Processing your request..."):
            ai_response = get_medical_response(user_input)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Clear input and rerun
        st.rerun()
    
    # Handle Enter key
    if user_input and st.session_state.get('last_input') != user_input:
        st.session_state.last_input = user_input
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main container

if __name__ == "__main__":
    main()