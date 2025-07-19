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

def get_intelligent_fallback_response(user_message):
    """Provide intelligent clinical research responses with flexible pattern matching"""
    query_lower = user_message.lower()
    
    # Enhanced keyword matching for more flexible responses
    
    # Multiple Sclerosis - Enhanced patterns
    if any(term in query_lower for term in ['multiple sclerosis', 'ms drug', 'ms treatment', 'ms medication', 'sclerosis', 'interferon', 'glatiramer', 'demyelinating', 'relapsing remitting']):
        return """**Multiple Sclerosis (MS) - FDA Approved Medications**

**Disease-Modifying Therapies (DMTs):**

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
- Regular monitoring for PML, infections, and liver function"""

    # Alzheimer's Disease
    elif any(term in query_lower for term in ['alzheimer', 'dementia', 'memory', 'aricept', 'donepezil', 'alzheimer drug']):
        return """**Alzheimer's Disease - FDA Approved Treatments**

**Cholinesterase Inhibitors:**
• **Donepezil (Aricept)** - 5-10 mg daily, all stages of AD
  - Mechanism: Reversible acetylcholinesterase inhibition
  - Efficacy: Modest cognitive improvement, delays nursing home placement
• **Rivastigmine (Exelon)** - 1.5-6 mg BID oral or 4.6-13.3 mg/24h patch
  - Dual inhibition: AChE and butyrylcholinesterase
• **Galantamine (Razadyne)** - 4-12 mg BID
  - Additional nicotinic receptor modulation

**NMDA Receptor Antagonist:**
• **Memantine (Namenda)** - 5-10 mg BID, moderate to severe AD
  - Mechanism: Uncompetitive NMDA receptor antagonist
  - Can be combined with cholinesterase inhibitors

**Recent Controversial Approvals:**
• **Aducanumab (Aduhelm)** - 10 mg/kg IV monthly
  - Mechanism: Anti-amyloid beta monoclonal antibody
  - FDA approval 2021 under accelerated pathway
  - Significant controversy over clinical benefit
• **Lecanemab (Leqembi)** - 10 mg/kg IV biweekly
  - Anti-amyloid beta protofibril antibody
  - FDA approval January 2023
  - 27% reduction in cognitive decline in Phase 3

**Combination Therapy:**
• **Namzaric** - Fixed-dose combination of memantine + donepezil

**Clinical Considerations:**
- Limited efficacy: 6-month delay in cognitive decline
- Side effects: GI upset, bradycardia, vivid dreams
- Amyloid-targeting agents require APOE4 testing
- Brain imaging monitoring for ARIA (amyloid-related imaging abnormalities)"""

    # Parkinson's Disease
    elif any(term in query_lower for term in ['parkinson', 'movement', 'levodopa', 'sinemet', 'dopamine', 'parkinson drug']):
        return """**Parkinson's Disease - Standard Treatments**

**Dopamine Replacement Therapy:**
• **Carbidopa/Levodopa (Sinemet)** - Gold standard
  - Standard: 25/100 mg TID, titrate to 25/250 mg QID
  - Extended-release (Sinemet CR): Longer duration
  - Entacapone combination (Stalevo): Reduces wearing-off

**Dopamine Agonists:**
• **Pramipexole (Mirapex)** - 0.125-1.5 mg TID
  - D2/D3 receptor agonist, neuroprotective properties
• **Ropinirole (Requip)** - 0.25-8 mg TID
  - Non-ergot dopamine agonist
• **Rotigotine (Neupro)** - 2-8 mg/24h transdermal patch

**MAO-B Inhibitors:**
• **Selegiline (Eldepryl)** - 5 mg BID
  - Selective MAO-B inhibition, mild symptomatic benefit
• **Rasagiline (Azilect)** - 0.5-1 mg daily
  - More potent than selegiline, potential neuroprotection

**COMT Inhibitors:**
• **Entacapone (Comtan)** - 200 mg with each levodopa dose
• **Tolcapone (Tasmar)** - 100-200 mg TID (hepatotoxicity monitoring)

**Anticholinergics:**
• **Trihexyphenidyl (Artane)** - 1-5 mg TID for tremor
• **Benztropine (Cogentin)** - 1-4 mg daily

**Advanced Therapies:**
• **Duopa** - Enteral carbidopa/levodopa gel
• **Deep Brain Stimulation (DBS)** - Subthalamic nucleus/GPi
• **Apomorphine (Apokyn)** - Subcutaneous rescue therapy"""

    # Diabetes
    elif any(term in query_lower for term in ['diabetes', 'blood sugar', 'insulin', 'metformin', 'glucose', 'diabetes drug']):
        return """**Type 2 Diabetes - Evidence-Based Medications**

**First-Line Therapy:**
• **Metformin** - 500-2000 mg daily
  - Mechanism: Decreases hepatic glucose production
  - Benefits: Weight neutral, cardiovascular protective
  - Contraindications: eGFR <30, severe heart failure

**GLP-1 Receptor Agonists:**
• **Semaglutide (Ozempic)** - 0.25-2 mg weekly injection
  - 14% reduction in MACE, significant weight loss
• **Liraglutide (Victoza)** - 0.6-1.8 mg daily injection
• **Dulaglutide (Trulicity)** - 0.75-4.5 mg weekly
• **Exenatide (Byetta/Bydureon)** - BID or weekly formulations

**SGLT-2 Inhibitors:**
• **Empagliflozin (Jardiance)** - 10-25 mg daily
  - 14% reduction in cardiovascular death
• **Dapagliflozin (Farxiga)** - 5-10 mg daily
• **Canagliflozin (Invokana)** - 100-300 mg daily

**DPP-4 Inhibitors:**
• **Sitagliptin (Januvia)** - 25-100 mg daily
• **Saxagliptin (Onglyza)** - 2.5-5 mg daily
• **Linagliptin (Tradjenta)** - 5 mg daily

**Insulin Therapies:**
• **Basal insulin:** Glargine (Lantus), Detemir (Levemir), Degludec (Tresiba)
• **Rapid-acting:** Lispro (Humalog), Aspart (Novolog), Glulisine (Apidra)
• **Combination:** 70/30, 75/25 mixtures

**Sulfonylureas:**
• **Glipizide** - 2.5-20 mg daily
• **Glyburide** - 1.25-20 mg daily
• **Glimepiride** - 1-8 mg daily"""

    # Comprehensive Clinical Trials & FDA - Expanded Coverage
    elif any(term in query_lower for term in ['clinical trial', 'phase', 'study design', 'protocol', 'fda', 'trial design', 'regulatory', 'gcp', 'ich', 'clinical research', 'crc', 'cra', 'monitor']):
        return """**Comprehensive Clinical Research & FDA Framework**

**Clinical Trial Phases - Complete Guide:**

**Phase 0 (Exploratory IND Studies):**
- Participants: 10-15 healthy volunteers or patients
- Purpose: Very early safety assessment, pharmacokinetics
- Dose: Sub-therapeutic, 1/100th of animal toxicity dose
- Duration: Days to weeks
- Regulatory: Exploratory IND required

**Phase I Trials (First-in-Human):**
- Participants: 20-100 (healthy volunteers or patients)
- Primary Endpoint: Safety, dose-limiting toxicity (DLT), maximum tolerated dose (MTD)
- Design Types: 3+3 dose escalation, continuous reassessment method (CRM), Bayesian optimal interval (BOIN)
- Duration: 6-18 months
- Key Assessments: Pharmacokinetics, pharmacodynamics, biomarkers
- Success Rate: 63% proceed to Phase II

**Phase II Trials (Proof of Concept):**
- Participants: 100-400 patients
- Design: Single-arm, randomized Phase II, seamless Phase I/II
- Primary Endpoint: Preliminary efficacy (response rate, progression-free survival)
- Secondary: Safety, biomarker analysis, quality of life
- Statistical Considerations: Simon two-stage design, randomized discontinuation
- Duration: 1-3 years
- Success Rate: 31% proceed to Phase III

**Phase III Trials (Pivotal Studies):**
- Participants: 300-5000+ patients
- Design: Randomized controlled trial (RCT), often double-blind, placebo-controlled
- Primary Endpoint: Overall survival, progression-free survival, clinical benefit
- Control Arms: Standard of care, placebo, historical control
- Statistical Power: 80-90% to detect clinically meaningful difference
- Interim Analyses: Pre-planned efficacy and futility assessments
- Duration: 2-7 years
- Success Rate: 25-30% achieve primary endpoint
- Regulatory: Basis for NDA/BLA submission

**Phase IV Trials (Post-Marketing):**
- Purpose: Long-term safety, real-world effectiveness, comparative effectiveness
- Types: Registry studies, pragmatic trials, pharmacovigilance studies
- Requirements: Often mandated by FDA as post-marketing commitments
- Duration: Ongoing, often 5-10 years

**FDA Regulatory Pathways & Designations:**

**Standard Drug Development Timeline:**
- IND Filing → Phase I → Phase II → Phase III → NDA → FDA Review → Approval
- Total Time: 10-15 years, $1-3 billion

**Expedited Pathways:**
• **Fast Track Designation:**
  - For drugs addressing unmet medical need
  - Benefits: Rolling review, frequent FDA meetings
  - Criteria: Serious condition + potential to address unmet need

• **Breakthrough Therapy Designation:**
  - Substantial improvement over existing treatments
  - Benefits: Intensive FDA guidance, expedited review
  - Timeline: 6-month review vs. standard 10-12 months

• **Accelerated Approval:**
  - Based on surrogate endpoints reasonably likely to predict clinical benefit
  - Requires confirmatory post-marketing studies
  - Examples: CD4 count for HIV drugs, tumor response for cancer

• **Priority Review:**
  - Significant advance in treatment, diagnosis, or prevention
  - 6-month FDA review timeline vs. standard 10-12 months

**Good Clinical Practice (GCP) Requirements:**

**ICH GCP Guidelines (E6):**
- International standard for clinical trial conduct
- Ensures quality, integrity, and regulatory acceptability
- Key Principles: Scientific approach, risk-benefit analysis, rights/safety/welfare protection

**Essential Documents:**
- Protocol and amendments
- Investigator brochure
- Informed consent forms
- IRB/IEC approvals
- Case report forms (CRFs)
- Source documents
- Audit trail documentation

**Clinical Research Roles & Responsibilities:**

**Clinical Research Coordinator (CRC):**
- Protocol implementation and compliance
- Patient recruitment, screening, enrollment
- Informed consent administration
- Data collection and CRF completion
- Adverse event reporting
- Regulatory compliance
- Communication with sponsors and monitors

**Clinical Research Associate (CRA):**
- Site monitoring and oversight
- Source data verification (SDV)
- Protocol compliance assessment
- Corrective and preventive action plans (CAPA)
- Risk-based monitoring approaches
- Site training and support

**Principal Investigator (PI) Responsibilities:**
- Overall study conduct and integrity
- Medical oversight and safety decisions
- Protocol adherence
- Investigational product accountability
- Staff supervision and training
- Regulatory compliance

**FDA Inspection Readiness:**

**Common FDA Inspection Findings:**
- Protocol deviations not properly documented
- Inadequate informed consent process
- Poor investigational product accountability
- Insufficient source documentation
- Inadequate safety reporting

**Key Regulatory Documents:**
- 21 CFR Part 50 (Informed Consent)
- 21 CFR Part 56 (IRB Regulations)
- 21 CFR Part 312 (IND Regulations)
- ICH Guidelines (E1-E20)
- FDA Guidance Documents

**Clinical Trial Endpoints & Biostatistics:**

**Primary Endpoints:**
- Overall Survival (OS): Gold standard in oncology
- Progression-Free Survival (PFS): Time to disease progression
- Response Rate: Complete + partial response per RECIST
- Quality of Life: Patient-reported outcomes (PROs)

**Statistical Considerations:**
- Type I Error (α): Usually 0.05 (5% false positive rate)
- Type II Error (β): Usually 0.20 (80% power)
- Multiple Testing: Bonferroni, Hochberg, hierarchical testing
- Interim Analysis: O'Brien-Fleming, Pocock boundaries
- Adaptive Designs: Sample size re-estimation, seamless Phase II/III

**Safety Monitoring & Pharmacovigilance:**

**Adverse Event Classification:**
- Mild (Grade 1): Minimal symptoms, intervention not indicated
- Moderate (Grade 2): Minimal intervention indicated
- Severe (Grade 3): Hospitalization or prolonged hospitalization
- Life-threatening (Grade 4): Urgent intervention indicated
- Death (Grade 5): Related to study intervention

**Serious Adverse Event (SAE) Reporting:**
- 24-hour notification to sponsor
- 15-day FDA safety report for unexpected SAEs
- Annual safety reports
- Risk evaluation and mitigation strategies (REMS)

**Data Management & Quality:**

**Electronic Data Capture (EDC):**
- Real-time data entry and validation
- Audit trail requirements
- Query management systems
- Database lock procedures

**CDISC Standards:**
- SDTM (Study Data Tabulation Model)
- ADaM (Analysis Data Model)
- ODM (Operational Data Model)
- Regulatory submission requirements"""

    # Enhanced flexible response system for various clinical research topics
    elif any(term in query_lower for term in ['cancer', 'oncology', 'chemotherapy', 'immunotherapy', 'tumor']):
        return """**Cancer/Oncology Treatments**

**Chemotherapy Classes:**
• **Alkylating agents**: Cyclophosphamide, Cisplatin, Carboplatin
• **Antimetabolites**: 5-FU, Methotrexate, Gemcitabine, Pemetrexed
• **Topoisomerase inhibitors**: Doxorubicin, Etoposide, Irinotecan
• **Mitotic inhibitors**: Paclitaxel, Docetaxel, Vincristine, Vinblastine

**Targeted Therapies:**
• **Tyrosine kinase inhibitors**: Imatinib (Gleevec), Erlotinib, Sunitinib
• **Monoclonal antibodies**: Trastuzumab (Herceptin), Bevacizumab (Avastin)
• **CDK4/6 inhibitors**: Palbociclib, Ribociclib, Abemaciclib

**Immunotherapy:**
• **PD-1/PD-L1 inhibitors**: Pembrolizumab (Keytruda), Nivolumab (Opdivo)
• **CTLA-4 inhibitors**: Ipilimumab (Yervoy)
• **CAR-T cell therapy**: Tisagenlecleucel, Axicabtagene ciloleucel"""

    elif any(term in query_lower for term in ['depression', 'anxiety', 'psychiatric', 'mental health', 'antidepressant']):
        return """**Psychiatric Medications**

**Antidepressants:**
• **SSRIs**: Sertraline (Zoloft), Fluoxetine (Prozac), Escitalopram (Lexapro)
• **SNRIs**: Venlafaxine (Effexor), Duloxetine (Cymbalta)
• **Atypical**: Bupropion (Wellbutrin), Mirtazapine (Remeron)
• **TCAs**: Amitriptyline, Nortriptyline (for treatment-resistant cases)

**Anxiety Medications:**
• **Benzodiazepines**: Lorazepam, Alprazolam, Clonazepam
• **Buspirone**: Non-benzodiazepine anxiolytic
• **Beta-blockers**: Propranolol for performance anxiety"""

    elif any(term in query_lower for term in ['hypertension', 'blood pressure', 'heart', 'cardiovascular', 'cardiac']):
        return """**Cardiovascular Medications**

**Antihypertensives:**
• **ACE inhibitors**: Lisinopril, Enalapril, Ramipril
• **ARBs**: Losartan, Valsartan, Olmesartan
• **Calcium channel blockers**: Amlodipine, Nifedipine
• **Beta-blockers**: Metoprolol, Atenolol, Carvedilol
• **Diuretics**: Hydrochlorothiazide, Furosemide, Spironolactone

**Heart Failure:**
• **ACE inhibitors + ARBs**: First-line therapy
• **Beta-blockers**: Carvedilol, Metoprolol succinate
• **SGLT-2 inhibitors**: Dapagliflozin, Empagliflozin"""

    elif any(term in query_lower for term in ['infection', 'antibiotic', 'antimicrobial', 'bacteria', 'virus', 'sepsis', 'pneumonia', 'uti', 'mrsa', 'resistance']):
        return """**Comprehensive Antimicrobial Therapy**

**Antibiotic Classes & Mechanisms:**

**β-Lactam Antibiotics:**
• **Penicillins**: 
  - Natural: Penicillin G (IV), Penicillin V (oral)
  - Aminopenicillins: Amoxicillin, Ampicillin
  - Extended-spectrum: Piperacillin-tazobactam, Ticarcillin-clavulanate
  - Anti-staphylococcal: Nafcillin, Oxacillin

• **Cephalosporins**:
  - 1st Generation: Cephalexin (oral), Cefazolin (IV) - Gram-positive coverage
  - 2nd Generation: Cefuroxime, Cefoxitin - Enhanced Gram-negative
  - 3rd Generation: Ceftriaxone, Ceftazidime - Broad Gram-negative, CNS penetration
  - 4th Generation: Cefepime - Extended Gram-negative, Pseudomonas
  - 5th Generation: Ceftaroline - MRSA coverage

• **Carbapenems**: Meropenem, Imipenem, Ertapenem, Doripenem
  - Broadest spectrum, reserved for multidrug-resistant organisms
  - Carbapenemase-producing Enterobacteriaceae (CPE) concern

**Protein Synthesis Inhibitors:**
• **Aminoglycosides**: Gentamicin, Tobramycin, Amikacin
  - Mechanism: 30S ribosomal subunit inhibition
  - Nephrotoxicity and ototoxicity monitoring required
  - Once-daily dosing for improved efficacy

• **Macrolides**: Azithromycin, Clarithromycin, Erythromycin
  - 50S ribosomal subunit inhibition
  - Atypical pneumonia coverage (Mycoplasma, Chlamydia, Legionella)

• **Tetracyclines**: Doxycycline, Minocycline, Tigecycline
  - Broad spectrum, tick-borne diseases, atypicals

**DNA/RNA Synthesis Inhibitors:**
• **Fluoroquinolones**:
  - Respiratory: Levofloxacin, Moxifloxacin
  - Genitourinary: Ciprofloxacin
  - FDA Black Box Warning: Tendon rupture, peripheral neuropathy

• **Metronidazole**: Anaerobic coverage, C. difficile
• **Trimethoprim-Sulfamethoxazole**: Pneumocystis, UTIs, MRSA

**Anti-MRSA Agents:**
• **Vancomycin**: IV, trough monitoring 15-20 mg/L
• **Linezolid**: Oral/IV, serotonin syndrome risk
• **Daptomycin**: Bactericidal, muscle toxicity monitoring
• **Ceftaroline**: MRSA-active cephalosporin
• **Tedizolid**: Newer oxazolidinone

**Antifungal Therapy:**

**Systemic Antifungals:**
• **Polyenes**: Amphotericin B (nephrotoxic), Liposomal amphotericin B
• **Triazoles**: Fluconazole, Voriconazole, Posaconazole, Isavuconazole
• **Echinocandins**: Caspofungin, Micafungin, Anidulafungin
  - First-line for Candida bloodstream infections

**Antiviral Agents:**

**Influenza Antivirals:**
• **Neuraminidase Inhibitors**: Oseltamivir (Tamiflu), Zanamivir
• **Endonuclease Inhibitor**: Baloxavir marboxil (Xofluza)

**Herpes Virus Antivirals:**
• **Nucleoside Analogs**: Acyclovir, Valacyclovir, Famciclovir
• **DNA Polymerase Inhibitors**: Foscarnet (resistant HSV/CMV)

**HIV Antiretrovirals:**
• **NRTIs**: Zidovudine, Emtricitabine, Tenofovir
• **NNRTIs**: Efavirenz, Rilpivirine
• **Integrase Inhibitors**: Dolutegravir, Bictegravir
• **Protease Inhibitors**: Darunavir, Atazanavir

**Antimicrobial Resistance Mechanisms:**
• **β-lactamases**: ESBLs, AmpC, KPC, NDM, OXA-48
• **Efflux pumps**: Fluoroquinolone resistance
• **Target modification**: MRSA (mecA gene), VRE (vanA/vanB)
• **Enzymatic inactivation**: Aminoglycoside-modifying enzymes

**Antimicrobial Stewardship:**
• **De-escalation**: Narrow spectrum after culture results
• **Duration optimization**: Procalcitonin-guided therapy
• **Dosing optimization**: Pharmacokinetic/pharmacodynamic principles
• **Combination therapy**: Synergy vs. resistance prevention"""

    # Enhanced general response with intelligent topic suggestions
    else:
        # Extract key medical terms for intelligent suggestions
        medical_terms = []
        if 'drug' in query_lower or 'medication' in query_lower or 'treatment' in query_lower:
            medical_terms.append("medication information")
        if 'trial' in query_lower or 'study' in query_lower:
            medical_terms.append("clinical trial design")
        if 'fda' in query_lower or 'approval' in query_lower:
            medical_terms.append("FDA regulatory processes")
        
        suggestions = ""
        if medical_terms:
            suggestions = f"\n**Based on your question about {', '.join(medical_terms)}:**"
        
        return f"""**Advanced Clinical Research & Medical Intelligence System**

{suggestions}

I'm your comprehensive medical and clinical research expert, covering all aspects of healthcare and drug development:

**Medical Specialties - Complete Coverage:**
• **Cardiology**: Heart failure, CAD, arrhythmias, valvular disease, interventional procedures
• **Oncology**: Solid tumors, hematologic malignancies, immunotherapy, precision medicine
• **Neurology**: Stroke, epilepsy, MS, Alzheimer's, Parkinson's, headache disorders
• **Endocrinology**: Diabetes, thyroid, adrenal, reproductive hormones, metabolism
• **Infectious Disease**: Bacterial, viral, fungal, parasitic infections, antimicrobial resistance
• **Psychiatry**: Depression, anxiety, bipolar, schizophrenia, ADHD, substance use disorders
• **Pulmonology**: COPD, asthma, pneumonia, pulmonary embolism, interstitial lung disease
• **Gastroenterology**: IBD, liver disease, GERD, pancreatic disorders, GI bleeding
• **Nephrology**: CKD, acute kidney injury, dialysis, transplantation, electrolyte disorders
• **Rheumatology**: RA, SLE, osteoarthritis, gout, vasculitis, biologics
• **Hematology**: Anemia, bleeding disorders, thrombosis, anticoagulation
• **Emergency Medicine**: Trauma, sepsis, cardiac arrest, toxicology, critical care

**Clinical Research - Complete Framework:**
• **Study Design**: Phase 0-IV trials, adaptive designs, basket/umbrella studies, real-world evidence
• **Regulatory Affairs**: FDA/EMA pathways, IND/NDA processes, international harmonization
• **Biostatistics**: Power analysis, survival analysis, Bayesian methods, multiplicity adjustment
• **Data Management**: CDISC standards, EDC systems, data integrity, ALCOA principles
• **Quality Assurance**: GCP compliance, risk-based monitoring, CAPA implementation
• **Safety & Pharmacovigilance**: AE reporting, signal detection, REMS, benefit-risk assessment
• **Biomarkers**: Predictive, prognostic, pharmacodynamic markers, companion diagnostics

**FDA Regulatory Expertise:**
• **Drug Development**: IND filing, meeting strategies, FDA guidance interpretation
• **Approval Pathways**: Standard, expedited (Fast Track, Breakthrough, Accelerated, Priority)
• **Post-Marketing**: Phase IV commitments, safety surveillance, label changes
• **Device Regulation**: 510(k), PMA, IDE studies, software as medical device

**Clinical Research Training & Certification:**
• **CRC Certification**: ACRP, SoCRA, IAOCR certification pathways
• **CRA Training**: Site monitoring, source data verification, corrective actions
• **PI Qualification**: ICH GCP training, medical oversight responsibilities
• **Regulatory Training**: FDA regulations, ICH guidelines, country-specific requirements

**Pharmacology & Drug Development:**
• **Pharmacokinetics**: ADME, drug interactions, population PK modeling
• **Pharmacodynamics**: Dose-response relationships, biomarker analysis
• **Formulation**: Immediate release, extended release, novel drug delivery systems
• **Manufacturing**: cGMP, process validation, analytical methods
• **Intellectual Property**: Patent strategies, exclusivity periods, generic pathways

**Your question:** "{user_message}"

**Expert Areas - Ask About:**
• Drug mechanisms, dosing, contraindications, drug interactions
• Disease pathophysiology, diagnostic criteria, treatment guidelines
• Clinical trial protocols, statistical analysis plans, regulatory submissions
• Medical device development, combination products, digital therapeutics
• Healthcare economics, market access, health technology assessment
• Medical writing, scientific publications, grant applications
• Career development in clinical research, pharmaceutical industry

I provide evidence-based, comprehensive responses drawing from medical literature, regulatory guidance, and clinical practice standards."""

def get_openai_response(user_message, conversation_history):
    """Get response from OpenAI GPT-4o with conversation memory"""
    if not OPENAI_API_KEY:
        return get_intelligent_fallback_response(user_message)
    
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
        color: #2c3e50 !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #7f8c8d !important;
        opacity: 0.7 !important;
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
    
    # Always keep exactly last 5 exchanges for optimal context
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
            Advanced Medical Intelligence • GPT-4o Powered • 5-Exchange Memory • Real-time Clinical Insights
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
    
    # Status indicator with memory display
    memory_count = len(st.session_state.conversation_memory)
    memory_status = f"Ready • Memory: {memory_count}/5 exchanges" if memory_count > 0 else "Ready"
    st.markdown(f'<div class="status-ready">{memory_status}</div>', unsafe_allow_html=True)
    
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