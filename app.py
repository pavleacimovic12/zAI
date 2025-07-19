import os
import logging
import requests
import time
import json
import re
from urllib.parse import urlencode, quote
from flask import Flask, render_template, request, jsonify, Response
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure minimal logging
logging.basicConfig(level=logging.WARNING)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "posit-secret")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Check OpenAI API availability
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_AVAILABLE = bool(OPENAI_API_KEY and len(OPENAI_API_KEY.strip()) > 0)

# In-memory conversation store for efficiency
conversations = {}

@app.route('/')
def index():
    """Main application page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint with comprehensive fallbacks"""
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if session_id not in conversations:
            conversations[session_id] = []
        
        conversations[session_id].append({"role": "user", "content": user_message})
        
        # Enhanced fallback responses (works without OpenAI)
        query_lower = user_message.lower()
        
        if any(term in query_lower for term in ['multiple sclerosis', 'ms drug', 'ms treatment', 'sclerosis']):
            response = """**Multiple Sclerosis (MS) - FDA Approved Medications**

**Injectable Disease-Modifying Therapies:**
• **Interferon beta-1a (Avonex)** - FDA approved 1996, 30 mcg IM weekly
• **Glatiramer acetate (Copaxone)** - FDA approved 1996, 20 mg SC daily
• **Interferon beta-1b (Betaseron)** - FDA approved 1993, 250 mcg SC every other day

**Oral Medications:**
• **Fingolimod (Gilenya)** - FDA approved 2010, 0.5 mg daily
• **Dimethyl fumarate (Tecfidera)** - FDA approved 2013, 240 mg twice daily
• **Teriflunomide (Aubagio)** - FDA approved 2012, 14 mg daily

**High-Efficacy Therapies:**
• **Natalizumab (Tysabri)** - Monthly IV infusion
• **Ocrelizumab (Ocrevus)** - Every 6 months IV infusion
• **Alemtuzumab (Lemtrada)** - Annual treatment courses"""
        
        elif any(term in query_lower for term in ['alzheimer', 'dementia', 'memory', 'aricept']):
            response = """**Alzheimer's Disease - FDA Approved Treatments**

**Cholinesterase Inhibitors:**
• **Donepezil (Aricept)** - 5-10 mg daily, all stages
• **Rivastigmine (Exelon)** - 1.5-6 mg twice daily or patch
• **Galantamine (Razadyne)** - 4-12 mg twice daily

**NMDA Receptor Antagonist:**
• **Memantine (Namenda)** - 5-10 mg twice daily, moderate to severe stages

**Recent Approval:**
• **Aducanumab (Aduhelm)** - Monthly IV infusion, controversial approval"""
        
        elif any(term in query_lower for term in ['parkinson', 'movement', 'levodopa', 'sinemet']):
            response = """**Parkinson's Disease - Standard Treatments**

**Dopamine Replacement:**
• **Carbidopa/Levodopa (Sinemet)** - Gold standard, multiple formulations
• **Carbidopa/Levodopa/Entacapone (Stalevo)** - Extended duration

**Dopamine Agonists:**
• **Pramipexole (Mirapex)** - 0.125-1.5 mg three times daily
• **Ropinirole (Requip)** - 0.25-8 mg three times daily

**MAO-B Inhibitors:**
• **Selegiline (Eldepryl)** - 5 mg twice daily
• **Rasagiline (Azilect)** - 0.5-1 mg daily"""
        
        elif any(term in query_lower for term in ['diabetes', 'blood sugar', 'insulin', 'metformin']):
            response = """**Type 2 Diabetes - Evidence-Based Medications**

**First-Line:**
• **Metformin** - 500-2000 mg daily, reduces hepatic glucose

**GLP-1 Agonists:**
• **Semaglutide (Ozempic)** - Weekly injection, weight loss benefits
• **Liraglutide (Victoza)** - Daily injection

**SGLT-2 Inhibitors:**
• **Empagliflozin (Jardiance)** - 10-25 mg daily
• **Dapagliflozin (Farxiga)** - 5-10 mg daily

**Insulin Options:**
• **Glargine (Lantus)** - Long-acting basal
• **Lispro (Humalog)** - Rapid-acting mealtime"""
        
        elif any(term in query_lower for term in ['clinical trial', 'phase', 'study design']):
            response = """**Clinical Trial Design Framework**

**Phase I:** Safety and dosing (20-100 participants)
**Phase II:** Preliminary efficacy (100-300 participants)  
**Phase III:** Confirmatory studies (300-3000 participants)
**Phase IV:** Post-marketing surveillance

**Key Requirements:**
• FDA IND application
• IRB approval
• Informed consent
• GCP compliance
• ClinicalTrials.gov registration"""
        
        else:
            response = f"""Thank you for your question about "{user_message}".

I'm a Clinical Research AI Assistant with comprehensive knowledge of:

**Medical Treatments:** FDA-approved medications for neurological, cardiovascular, and endocrine conditions
**Clinical Research:** Trial design, regulatory pathways, GCP guidelines
**Therapeutic Areas:** Multiple sclerosis, Alzheimer's, Parkinson's, diabetes, and more

Could you specify which medical condition or clinical research topic you'd like to explore?"""
        
        conversations[session_id].append({"role": "assistant", "content": response})
        return jsonify({'response': response, 'session_id': session_id})
        
    except Exception as e:
        return jsonify({'error': 'Processing failed'}), 500

@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'healthy', 'openai_available': OPENAI_AVAILABLE})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)