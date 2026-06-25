import streamlit as st

st.set_page_config(page_title="SPIDER-AI | Home", layout="wide")

st.markdown("""
    <style>
    :root {
        --bg-color: #0b0e14;
        --accent-color: #00d4ff;
    }
    
    /* خلفية العنكبوت البرمجية */
    .stApp {
        background-color: var(--bg-color);
        background-image: 
            radial-gradient(circle at center, rgba(0, 212, 255, 0.05) 0%, transparent 70%),
            linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px),
            linear-gradient(0deg, rgba(255,255,255,0.03) 1px, transparent 1px);
        background-size: 50px 50px;
    }
    
    /* تصميم العنوان الرئيسي */
    .hero-title {
        text-align: center;
        font-family: 'Inter', sans-serif;
        color: white;
        margin-top: 100px;
        margin-bottom: 40px;
    }
    
    /* تصميم صندوق البرومبت */
    .input-container {
        max-width: 700px;
        margin: 0 auto;
        background: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .stTextInput > div > div > input {
        background: transparent !important;
        border: none !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='hero-title'>Start with one prompt. <br>You can change everything later.</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🌐 Web App", "📱 Mobile App"])

with tab1:
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    prompt = st.text_input("", placeholder="Describe your idea, we will bring it to life...", key="main_prompt")
    
    col_btn1, col_btn2 = st.columns([0.9, 0.1])
    with col_btn2:
        if st.button("🚀"):
            st.session_state.prompt = prompt
            st.success("جاري البدء...")
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    st.text_input("", placeholder="Describe your Mobile App idea...", key="mobile_prompt")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div style="position: fixed; bottom: 20px; right: 20px; color: #58a6ff; font-family: monospace;">
        SPIDER-AI // GENERATIVE ENGINE
    </div>
""", unsafe_allow_html=True)
