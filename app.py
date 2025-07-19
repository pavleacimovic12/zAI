import streamlit as st
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Clinical Research AI Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for medical theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #4facfe;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    .ai-message {
        background-color: #f5f5f5;
        border-left-color: #4caf50;
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
    }
    
    .stButton > button {
        border-radius: 25px;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
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

# Main application
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Clinical Research AI Assistant</h1>
        <p>Expert medical knowledge and clinical research guidance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message ai-message">
                <strong>AI Assistant:</strong><br>{message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask about medical treatments or clinical research...",
            key="user_input",
            placeholder="e.g., What medications are available for multiple sclerosis?"
        )
    
    with col2:
        send_button = st.button("Send", type="primary")
    
    # Process message
    if send_button and user_input.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate AI response
        with st.spinner("Processing your request..."):
            ai_response = get_medical_response(user_input)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Rerun to display new messages
        st.rerun()
    
    # Sidebar information
    with st.sidebar:
        st.markdown("### About")
        st.info("""
        This Clinical Research AI Assistant provides:
        
        • FDA-approved medications
        • Clinical trial information  
        • Regulatory guidance
        • Medical treatment options
        
        No external API keys required!
        """)
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()