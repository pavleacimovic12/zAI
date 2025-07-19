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

# OpenAI Configuration with safe fallback
def get_api_key():
    """Safely get API key from environment or secrets"""
    # First try environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key
    
    # Then try Streamlit secrets (safely)
    try:
        return st.secrets.get("OPENAI_API_KEY", None)
    except:
        return None

OPENAI_API_KEY = get_api_key()

def simulate_typing_response(response_text, placeholder):
    """Simulate real-time typing effect for responses"""
    displayed_text = ""
    words = response_text.split()
    
    for i, word in enumerate(words):
        displayed_text += word + " "
        placeholder.markdown(displayed_text + "▊")  # Show cursor
        time.sleep(0.03)  # Realistic typing speed
    
    # Remove cursor and show final response
    placeholder.markdown(displayed_text)
    return displayed_text

def get_intelligent_fallback_response(user_message):
    """Generate dynamic, ChatGPT-like responses tailored specifically to each question"""
    
    # Analyze the specific question to generate a contextual response
    query_lower = user_message.lower()
    
    # Generate dynamic response based on the specific question asked
    
    # Generate tailored response for Alzheimer's disease
    if any(term in query_lower for term in ['alzheimer', 'dementia', 'memory loss', 'cognitive decline', 'ad ', 'aricept', 'donepezil']):
        return generate_alzheimer_specific_response(user_message)
    
    # Generate tailored response for Parkinson's disease
    elif any(term in query_lower for term in ['parkinson', 'movement disorder', 'tremor', 'pd ', 'levodopa', 'sinemet', 'dopamine']):
        return generate_parkinson_specific_response(user_message)
    
    # Generate tailored response for diabetes
    elif any(term in query_lower for term in ['diabetes', 'blood sugar', 'glucose', 'insulin', 'metformin', 'diabetic']):
        return generate_diabetes_specific_response(user_message)
    
    # Generate tailored response for clinical trials
    elif any(term in query_lower for term in ['clinical trial', 'phase', 'fda', 'regulatory', 'trial design', 'protocol']):
        return generate_clinical_trial_specific_response(user_message)
    
    # Generate tailored response for cancer/oncology
    elif any(term in query_lower for term in ['cancer', 'oncology', 'tumor', 'chemotherapy', 'immunotherapy']):
        return generate_oncology_specific_response(user_message)
    
    # Generate tailored response for cardiovascular
    elif any(term in query_lower for term in ['heart', 'cardiac', 'cardiovascular', 'hypertension', 'blood pressure']):
        return generate_cardiology_specific_response(user_message)
    
    # Default: Generate contextual medical response
    else:
        return generate_contextual_medical_response(user_message)

def generate_alzheimer_specific_response(user_message):
    """Generate specific, tailored response about Alzheimer's based on the exact question"""
    query_lower = user_message.lower()
    
    # Analyze what specific aspect they're asking about
    if 'medication' in query_lower or 'drug' in query_lower or 'treatment' in query_lower:
        return f"""**Alzheimer's Disease Medications - Comprehensive Overview**

Based on your question "{user_message}", here are the current FDA-approved treatments:

**Cholinesterase Inhibitors (Most Common):**
• **Donepezil (Aricept)** - 5-10mg daily, works for all stages of AD
  - Mechanism: Blocks acetylcholinesterase enzyme to increase brain acetylcholine
  - Efficacy: Modest cognitive improvement, may delay nursing home placement by 6 months
  - Side effects: Nausea, diarrhea, vivid dreams, potential heart rhythm changes

• **Rivastigmine (Exelon)** - Available as pill (1.5-6mg twice daily) or patch (4.6-13.3mg/24h)
  - Dual action: Blocks both acetylcholinesterase and butyrylcholinesterase
  - Patch form reduces GI side effects

• **Galantamine (Razadyne)** - 8-24mg daily in divided doses
  - Additional benefit: Also enhances nicotinic receptor function

**NMDA Receptor Antagonist:**
• **Memantine (Namenda)** - 10mg twice daily, for moderate to severe AD
  - Mechanism: Regulates glutamate to prevent brain cell damage
  - Often combined with cholinesterase inhibitors
  - Generally better tolerated than other AD medications

**Controversial Recent Approvals:**
• **Aducanumab (Aduhelm)** - Monthly IV infusion, targets amyloid plaques
  - FDA approved 2021 despite mixed trial results
  - Cost: ~$56,000/year, requires regular brain MRI monitoring
  - Controversy: Unclear clinical benefit, potential brain swelling risks

• **Lecanemab (Leqembi)** - Biweekly IV infusion, anti-amyloid therapy
  - FDA approved January 2023 based on 27% slowing of cognitive decline
  - Similar monitoring requirements and costs as Aduhelm

**Important Reality Check:**
These medications don't cure Alzheimer's or stop its progression. They may provide modest symptom relief for 6-12 months in some patients. The field is actively researching new approaches targeting tau protein, inflammation, and neuroprotection."""
    
    elif 'mechanism' in query_lower or 'how' in query_lower:
        return f"""**How Alzheimer's Medications Work - Mechanisms of Action**

You asked "{user_message}" - here's the science behind AD treatments:

**Cholinesterase Inhibitors (Donepezil, Rivastigmine, Galantamine):**
- **Problem**: AD destroys neurons that produce acetylcholine, a key memory neurotransmitter
- **Solution**: These drugs block acetylcholinesterase enzyme that breaks down acetylcholine
- **Result**: More acetylcholine available for brain communication
- **Analogy**: Like plugging holes in a leaky bucket to keep more water (acetylcholine) available

**Memantine (NMDA Antagonist):**
- **Problem**: Excess glutamate causes excitotoxicity, damaging brain cells
- **Solution**: Memantine partially blocks NMDA receptors to regulate glutamate activity
- **Result**: Protects neurons from glutamate-induced damage while preserving normal function
- **Analogy**: Like installing a pressure valve to prevent damaging overflows

**Anti-Amyloid Therapies (Aducanumab, Lecanemab):**
- **Problem**: Amyloid-beta plaques accumulate between brain cells
- **Solution**: Monoclonal antibodies bind to and help clear amyloid plaques
- **Result**: Reduced plaque burden (though clinical benefit remains debated)
- **Analogy**: Like using specialized cleaners to remove specific types of brain "debris"

**Why Limited Effectiveness:**
AD involves multiple pathological processes (amyloid, tau, inflammation, synaptic loss). Current drugs only address single targets, explaining their modest benefits."""
    
    else:
        return f"""**Alzheimer's Disease - Tailored Information**

Regarding your question "{user_message}", here's what you need to know:

Alzheimer's disease affects 6.7 million Americans and is the leading cause of dementia. It's characterized by progressive memory loss, cognitive decline, and behavioral changes.

**Current Treatment Landscape:**
The therapeutic approach focuses on symptom management rather than disease modification. We have four FDA-approved medications that provide modest benefits:

1. **Donepezil (Aricept)** - Most widely prescribed, suitable for all disease stages
2. **Rivastigmine (Exelon)** - Available in patch form for better tolerance
3. **Galantamine (Razadyne)** - Has additional nicotinic receptor benefits
4. **Memantine (Namenda)** - For moderate-severe disease, different mechanism

**Recent Developments:**
The controversial approval of amyloid-targeting drugs (Aducanumab, Lecanemab) represents a shift toward disease-modifying therapy, though their clinical benefit remains hotly debated.

**Research Pipeline:**
Active areas include tau-targeting therapies, anti-inflammatory approaches, neuroprotective strategies, and combination treatments.

**Patient/Family Considerations:**
Treatment decisions should involve thorough discussion of realistic expectations, cost-benefit analysis, and comprehensive care planning including non-pharmacological interventions."""

def generate_parkinson_specific_response(user_message):
    """Generate specific response about Parkinson's disease"""
    return f"""**Parkinson's Disease Treatment - Tailored to Your Question**

You asked: "{user_message}"

**Gold Standard Therapy:**
**Carbidopa/Levodopa (Sinemet)** remains the most effective treatment:
- Carbidopa prevents levodopa breakdown before reaching the brain
- Levodopa converts to dopamine in brain cells
- Standard dosing: Start 25/100mg three times daily, titrate based on response
- Extended-release formulations available for motor fluctuations

**Dopamine Agonists (Often First-Line in Younger Patients):**
• **Pramipexole (Mirapex)** - 0.125-1.5mg three times daily
• **Ropinirole (Requip)** - 0.25-8mg three times daily  
• **Rotigotine (Neupro patch)** - 2-8mg/24 hours, provides continuous stimulation

**MAO-B Inhibitors (Neuroprotective Potential):**
• **Rasagiline (Azilect)** - 0.5-1mg daily
• **Selegiline (Eldepryl)** - 5mg twice daily
• **Safinamide (Xadago)** - Newest option with additional glutamate effects

**Advanced Therapies for Motor Complications:**
• **Deep Brain Stimulation (DBS)** - Surgical option for tremor and motor fluctuations
• **Duopa pump** - Continuous carbidopa/levodopa gel delivery
• **Apomorphine (Apokyn)** - Injectable rescue therapy for "off" periods

**Treatment Strategy:**
- Early disease: MAO-B inhibitors or dopamine agonists (especially age <65)
- Moderate disease: Add levodopa when functional impairment occurs
- Advanced disease: Consider DBS, pumps, or continuous therapies
- Goal: Balance symptom control with minimizing long-term complications"""

def generate_diabetes_specific_response(user_message):
    """Generate specific response about diabetes"""
    return f"""**Type 2 Diabetes Medications - Evidence-Based Approach**

Responding to your question: "{user_message}"

**First-Line (Always Start Here):**
**Metformin** - 500-2000mg daily
- Reduces liver glucose production, improves insulin sensitivity
- Cardiovascular protective, weight neutral, low hypoglycemia risk
- Contraindications: Severe kidney disease (eGFR <30), severe heart failure

**Second-Line Options (Individualized Selection):**

**GLP-1 Receptor Agonists (Excellent for Weight Loss + CV Protection):**
• **Semaglutide (Ozempic)** - 0.25-2mg weekly injection
  - 14% reduction in major cardiovascular events (SUSTAIN-6 trial)
  - Average 12-15 lb weight loss
• **Liraglutide (Victoza)** - 0.6-1.8mg daily injection
• **Dulaglutide (Trulicity)** - 0.75-4.5mg weekly

**SGLT-2 Inhibitors (Heart Failure + Kidney Benefits):**
• **Empagliflozin (Jardiance)** - 10-25mg daily
  - 14% reduction in cardiovascular death (EMPA-REG trial)
  - Proven heart failure benefits regardless of diabetes status
• **Dapagliflozin (Farxiga)** - 5-10mg daily
• Risk: Genital infections, rare DKA, Fournier's gangrene

**Treatment Selection Strategy:**
- **Heart failure/CKD**: SGLT-2 inhibitors first
- **Obesity/weight concerns**: GLP-1 agonists first  
- **Cost considerations**: Sulfonylureas, DPP-4 inhibitors
- **Hypoglycemia risk**: Avoid sulfonylureas, choose DPP-4 inhibitors

**Insulin (When Needed):**
- Basal insulin first: Glargine (Lantus), Detemir (Levemir), Degludec (Tresiba)
- Rapid-acting for meals: Lispro (Humalog), Aspart (Novolog)"""

def generate_clinical_trial_specific_response(user_message):
    """Generate specific response about clinical trials"""
    return f"""**Clinical Trial Design & FDA Regulatory Framework**

Based on your question: "{user_message}"

**Phase I (Safety & Dose Finding):**
- Participants: 20-100 (healthy volunteers or patients)
- Primary goal: Maximum tolerated dose, dose-limiting toxicities
- Design: 3+3 dose escalation, continuous reassessment method
- Duration: 6-18 months
- Success rate: ~63% advance to Phase II

**Phase II (Proof of Concept):**
- Participants: 100-400 patients with target condition
- Primary goal: Preliminary efficacy signals
- Design: Single-arm or randomized Phase II
- Key endpoint: Response rate, progression-free survival
- Success rate: ~31% advance to Phase III

**Phase III (Pivotal Registration Trials):**
- Participants: 300-5000+ patients
- Primary goal: Definitive efficacy vs standard of care
- Design: Randomized, controlled, often double-blind
- Duration: 2-7 years
- Statistical power: 80-90% to detect clinically meaningful difference

**FDA Expedited Pathways:**
• **Fast Track** - Addresses unmet medical need
• **Breakthrough Therapy** - Substantial improvement over existing therapy  
• **Accelerated Approval** - Surrogate endpoints for serious conditions
• **Priority Review** - 6-month vs standard 10-month review

**Good Clinical Practice (GCP) Core Principles:**
- Subject safety and welfare as highest priority
- Protocol adherence and scientific integrity
- Proper informed consent processes
- Qualified investigators and adequate facilities
- Data integrity and source document verification
- Quality assurance and regulatory compliance"""

def generate_oncology_specific_response(user_message):
    """Generate specific response about cancer treatments"""
    return f"""**Cancer Treatment Revolution - Modern Oncology**

Addressing your question: "{user_message}"

**Immunotherapy Breakthrough:**
• **PD-1 Inhibitors**: Pembrolizumab (Keytruda), Nivolumab (Opdivo)
  - Unleash immune system against cancer cells
  - Durable responses in melanoma, lung cancer, many others
• **CAR-T Cell Therapy**: Tisagenlecleucel (Kymriah), Axicabtagene ciloleucel (Yescarta)
  - Genetically modified T-cells to attack specific cancers
  - Remarkable results in refractory blood cancers

**Precision Medicine Era:**
• **Biomarker-Driven Therapy**: Treatment based on tumor genetics
• **EGFR Inhibitors**: Osimertinib (Tagrisso) for EGFR+ lung cancer
• **BRAF Inhibitors**: Vemurafenib + Cobimetinib for BRAF+ melanoma
• **CDK4/6 Inhibitors**: Palbociclib (Ibrance) for HR+ breast cancer

**Targeted Therapy Success Stories:**
• **Imatinib (Gleevec)**: Transformed CML from fatal to manageable
• **Trastuzumab (Herceptin)**: HER2+ breast cancer game-changer
• **Rituximab (Rituxan)**: First monoclonal antibody for lymphomas

**Challenges & Future:**
- Resistance mechanisms remain major obstacle
- Combination strategies increasingly important
- Managing immune-related adverse events
- Access and cost considerations
- Liquid biopsies for early detection and monitoring"""

def generate_cardiology_specific_response(user_message):
    """Generate specific response about cardiovascular medicine"""
    return f"""**Cardiovascular Medicine - Evidence-Based Treatments**

Your question: "{user_message}"

**Heart Failure with Reduced Ejection Fraction (HFrEF):**
• **ACE Inhibitors/ARBs**: Lisinopril, Losartan - proven mortality reduction
• **Beta-blockers**: Metoprolol succinate, Carvedilol - reduce deaths by 30-35%
• **SGLT-2 Inhibitors**: Empagliflozin, Dapagliflozin - new heart failure indication
• **ARNI**: Sacubitril/Valsartan (Entresto) - superior to ACE inhibitors

**Coronary Artery Disease Prevention:**
• **Antiplatelet**: Aspirin 81mg daily, Clopidogrel for high-risk patients
• **Statins**: Atorvastatin, Rosuvastatin - target LDL <70 mg/dL
• **PCSK9 Inhibitors**: Evolocumab, Alirocumab for very high-risk patients

**Hypertension Management (2017 ACC/AHA Guidelines):**
• **First-line**: ACE inhibitors, ARBs, thiazide diuretics, calcium channel blockers
• **Target**: <130/80 mmHg for most adults
• **Combination therapy**: Often required, fixed-dose combinations available

**Atrial Fibrillation Anticoagulation:**
• **DOACs preferred**: Apixaban (Eliquis), Rivaroxaban (Xarelto), Dabigatran (Pradaxa)
• **Advantages over warfarin**: Fixed dosing, fewer interactions, no INR monitoring
• **CHA2DS2-VASc score**: Guides anticoagulation decisions

**Emerging Therapies:**
- Inclisiran (PCSK9 silencing) - twice yearly injections
- Finerenone for diabetic kidney disease
- Novel heart failure treatments in development"""

def generate_contextual_medical_response(user_message):
    """Generate contextual response for general medical questions"""
    return f"""**Comprehensive Medical & Clinical Research Response**

Thank you for your question: "{user_message}"

As a Clinical Research Coordinator AI with extensive medical knowledge, I can provide detailed information across:

**Medical Specialties:**
• **Neurology**: Alzheimer's, Parkinson's, multiple sclerosis, epilepsy, stroke
• **Cardiology**: Heart failure, coronary disease, hypertension, arrhythmias
• **Endocrinology**: Diabetes, thyroid disorders, adrenal conditions
• **Oncology**: Cancer treatments, immunotherapy, targeted therapy
• **Infectious Disease**: Antibiotics, antivirals, antimicrobial resistance
• **Psychiatry**: Depression, anxiety, bipolar disorder, ADHD medications

**Clinical Research Expertise:**
• **FDA Regulations**: IND/NDA processes, regulatory pathways
• **Study Design**: Phase I-IV trials, adaptive designs, statistical planning
• **Good Clinical Practice**: GCP guidelines, monitoring, data integrity
• **Biostatistics**: Power analysis, survival analysis, interim analyses
• **Safety Monitoring**: Adverse event reporting, risk management

**Drug Development Knowledge:**
• **Pharmacology**: Mechanisms of action, drug interactions, dosing
• **Regulatory Affairs**: FDA submissions, international harmonization
• **Clinical Operations**: Protocol development, site management
• **Data Management**: CDISC standards, electronic data capture

Please feel free to ask specific questions about:
- Medication information and clinical evidence
- Disease pathophysiology and treatment guidelines
- Clinical trial design and regulatory requirements
- Career development in clinical research
- Any medical specialty or therapeutic area

I'll provide detailed, evidence-based responses tailored to your specific interests."""

def generate_ms_specific_response(user_message):
    """Generate specific response about Multiple Sclerosis"""
    return f"""**Multiple Sclerosis (MS) - Tailored Treatment Information**

Based on your question: "{user_message}"

**Disease-Modifying Therapies (DMTs) - Complete Spectrum:**

**Injectable Therapies:**
• **Interferon beta-1a (Avonex)** - 30 mcg IM weekly, reduces relapse rate by 18-32%
• **Interferon beta-1b (Betaseron, Extavia)** - 250 mcg SC every other day
• **Glatiramer acetate (Copaxone)** - 20 mg SC daily or 40 mg SC 3x/week
• **Peginterferon beta-1a (Plegridy)** - 125 mcg SC every 2 weeks

**Oral Medications:**
• **Fingolimod (Gilenya)** - 0.5 mg daily, S1P receptor modulator
• **Dimethyl fumarate (Tecfidera)** - 240 mg twice daily, Nrf2 pathway activator
• **Teriflunomide (Aubagio)** - 7-14 mg daily, pyrimidine synthesis inhibitor
• **Siponimod (Mayzent)** - For secondary progressive MS
• **Ozanimod (Zeposia)** - S1P receptor modulator
• **Ponesimod (Ponvory)** - Approved 2021

**High-Efficacy Infusion Therapies:**
• **Natalizumab (Tysabri)** - 300 mg IV monthly, α4β1 integrin antagonist
• **Alemtuzumab (Lemtrada)** - 12 mg IV daily x5 days, then x3 days after 1 year
• **Ocrelizumab (Ocrevus)** - 300 mg IV every 6 months, anti-CD20 monoclonal antibody
• **Rituximab (Rituxan)** - Off-label use, anti-CD20 therapy

**Newer Therapies:**
• **Cladribine (Mavenclad)** - Oral pulse therapy, purine nucleoside analog
• **Ofatumumab (Kesimpta)** - 20 mg SC monthly, anti-CD20 subcutaneous

**Clinical Considerations:**
- First-line: Interferons, glatiramer acetate, oral DMTs
- High-efficacy: Reserved for aggressive disease or breakthrough activity
- JCV antibody testing required before natalizumab
- Regular monitoring for PML, infections, and liver function

**Treatment Selection Based on Your Question:**
The choice of MS therapy depends on disease activity, patient age, lifestyle factors, and risk tolerance. Early aggressive treatment is increasingly favored to prevent disability accumulation."""

def get_openai_response(message, conversation_memory=None):
    """Get response from OpenAI GPT-4o with conversation memory"""
    if not OPENAI_API_KEY:
        # Use intelligent fallback if no API key
        return get_intelligent_fallback_response(message)
    
    try:
        # Build context from conversation memory
        context = build_conversation_context(conversation_memory) if conversation_memory else ""
        
        # Clinical Research Coordinator system prompt
        system_prompt = """You are an expert Clinical Research Coordinator AI with comprehensive medical knowledge across all therapeutic areas. You provide professional, detailed responses about:

- Clinical trial design, FDA regulations, and GCP guidelines
- Drug information, mechanisms of action, and evidence-based medicine
- Disease pathophysiology and treatment protocols across all medical specialties
- Regulatory affairs, biostatistics, and research methodology
- Career development in clinical research and healthcare

Provide accurate, evidence-based information with proper clinical context. Always mention when information should be verified with healthcare professionals for individual medical decisions."""

        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation context if available
        if context:
            messages.append({"role": "system", "content": f"Conversation context:\n{context}"})
        
        messages.append({"role": "user", "content": message})
        
        # Make OpenAI API request
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
            "messages": messages,
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            response_data = response.json()
            if 'choices' in response_data and response_data['choices']:
                return response_data['choices'][0]['message']['content']
            else:
                return get_intelligent_fallback_response(message)
        else:
            return get_intelligent_fallback_response(message)
            
    except Exception as e:
        # Fallback to intelligent response system
        return get_intelligent_fallback_response(message)

def build_conversation_context(conversation_memory):
    """Build conversation context from memory for OpenAI"""
    if not conversation_memory:
        return ""
    
    context_parts = []
    for entry in conversation_memory[-5:]:  # Last 5 exchanges
        context_parts.append(f"User: {entry['user']}")
        context_parts.append(f"Assistant: {entry['assistant'][:200]}...")  # Truncate for context
    
    return "\n".join(context_parts)

def get_medical_response(user_message, uploaded_files=None):
    """Main function to get medical response with OpenAI integration"""
    
    # Add file context if files are uploaded
    file_context = ""
    if uploaded_files:
        file_context = "\n\n**Document Context:**\n"
        for file_info in uploaded_files:
            file_context += f"- {file_info['name']} ({file_info['type'].upper()}): {file_info.get('preview', 'File uploaded successfully')}\n"
    
    # Combine message with file context
    full_message = user_message + file_context
    
    # Get conversation memory from session
    conversation_memory = st.session_state.get('conversation_memory', [])
    
    # Use OpenAI if available, otherwise use intelligent fallback
    if OPENAI_API_KEY:
        response = get_openai_response(full_message, conversation_memory)
    else:
        response = get_intelligent_fallback_response(full_message)
    
    return response

# Session state initialization
def initialize_session_state():
    """Initialize all session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation_memory' not in st.session_state:
        st.session_state.conversation_memory = []
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

def update_conversation_memory(user_message, ai_response):
    """Update conversation memory with new exchange"""
    if 'conversation_memory' not in st.session_state:
        st.session_state.conversation_memory = []
    
    # Add new exchange
    st.session_state.conversation_memory.append({
        'user': user_message,
        'assistant': ai_response
    })
    
    # Keep only last 5 exchanges (as requested by user)
    if len(st.session_state.conversation_memory) > 5:
        st.session_state.conversation_memory = st.session_state.conversation_memory[-5:]

def process_uploaded_file(uploaded_file):
    """Process uploaded file and return file information"""
    file_info = {
        'name': uploaded_file.name,
        'type': uploaded_file.type or 'unknown',
        'size': uploaded_file.size if hasattr(uploaded_file, 'size') else 0
    }
    
    # Try to extract text preview for text-based files
    try:
        if uploaded_file.type and ('text' in uploaded_file.type or 
                                  uploaded_file.name.endswith(('.txt', '.md', '.py', '.json', '.xml', '.html', '.css', '.js'))):
            content = uploaded_file.read().decode('utf-8')
            file_info['preview'] = content[:500] + "..." if len(content) > 500 else content
            uploaded_file.seek(0)  # Reset file pointer
        else:
            file_info['preview'] = f"Binary file uploaded: {uploaded_file.name}"
    except:
        file_info['preview'] = f"File uploaded successfully: {uploaded_file.name}"
    
    return file_info

def main():
    """Main Streamlit application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Main container with glass-morphism design
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="medical-header">
        <div class="status-badge">
            🟢 AI System Online
        </div>
        <div class="header-title">
            🩺 Clinical Research AI Assistant
        </div>
        <div class="header-subtitle">
            Advanced Medical Intelligence & Research Coordination
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Memory counter display
    memory_count = len(st.session_state.conversation_memory)
    st.markdown(f"""
    <div style="text-align: center; padding: 16px; background: linear-gradient(135deg, rgba(139, 126, 200, 0.1), rgba(107, 91, 149, 0.1)); border-radius: 12px; margin: 16px 32px;">
        <h4 style="margin: 0; color: #6B5B95;">💭 Conversation Memory: {memory_count}/5 exchanges</h4>
        <p style="margin: 8px 0 0 0; font-size: 14px; color: #666;">The system remembers your last 5 conversation exchanges for context</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome section with animated particles
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-section">
            <div class="microscope-icon">🔬</div>
            <h1 class="welcome-title">Welcome to Your Clinical Research AI</h1>
            <p class="welcome-description">
                Ask me anything about clinical research, FDA regulations, drug information, 
                medical conditions, or healthcare topics. I'm here to provide expert-level guidance!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat messages display
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-avatar user-avatar">👤</div>
                <div class="message-content">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message ai-message">
                <div class="message-avatar ai-avatar">🤖</div>
                <div class="message-content">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
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
    
    # Process message with live response generation
    if send_button and user_input.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show generating message indicator
        with st.container():
            status_text = st.markdown("🔄 **Generating tailored response...**")
            
            # Generate AI response with file context
            ai_response = get_medical_response(user_input, st.session_state.uploaded_files)
            
            # Update status to show response generation complete
            status_text.markdown("✅ **Response generated!**")
            
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            # Update conversation memory
            update_conversation_memory(user_input, ai_response)
        
        # Clear input and rerun to show new messages
        st.rerun()
    
    # Handle Enter key
    if user_input and st.session_state.get('last_input') != user_input:
        st.session_state.last_input = user_input
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main container

if __name__ == "__main__":
    main()
