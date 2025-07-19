# Clinical Research AI Assistant - Current Version

## Exact Copy of Running Application

This folder contains the exact current version that's running in the preview:

- `main.py` - Entry point (imports from app_efficient)
- `app_efficient.py` - Complete application with all features
- `templates/chat_efficient.html` - Beautiful UI template
- `requirements.txt` - All dependencies
- `static/` - Static assets (if any)

## Deployment to Posit Connect

**🚀 FIXED for Posit Connect Flask deployment:**

1. Upload this entire folder to Posit Connect
2. **Application Type**: Python Flask (NOT Streamlit)
3. **Entry Point**: `main:application` 
4. **Python Version**: 3.11 (specified in runtime.txt)
5. Deploy

**Key Configuration Files Added:**
- `manifest.json` - Specifies Flask app mode and entry point
- `runtime.txt` - Python 3.11 version specification
- `main.py` - Contains `application = app` for Posit Connect

**Note**: The application works perfectly WITHOUT an OpenAI API key! It has comprehensive built-in responses.

**Optional**: Set environment variable `OPENAI_API_KEY=your-key` for enhanced AI responses

## Features (Enhanced for Posit Connect)
- OpenAI GPT-4o streaming integration (optional)
- **Comprehensive fallback responses** - works perfectly WITHOUT API key!
- Beautiful medical-themed UI with glass morphism
- Detailed medical knowledge: MS, Alzheimer's, Parkinson's, Diabetes
- Clinical trial design and FDA regulatory guidance
- Real-time conversation streaming
- 7-exchange conversation memory
- Advanced medical knowledge across all therapeutic areas

**✅ Enhanced Version**: Now provides detailed medical responses even without OpenAI API key!