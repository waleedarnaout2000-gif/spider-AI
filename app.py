import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="SPIDER-AI | Next-Gen Engine", layout="wide")

# استخدام CSS متقدم لتنفيذ تصميم الـ Spider Web والـ Glassmorphism
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    :root {
        --bg-color: #05070a;
        --accent: #00d4ff;
        --glass: rgba(255, 255, 255, 0.03);
    }
    
    .stApp {
        background-color: var(--bg-color);
        background-image: 
            radial-gradient(circle at 50% 50%, #0c1524 0%, #05070a 100%);
        overflow: hidden;
    }
    
    /* تأثير الشبكة العنكبوتية المتقدم */
    .spider-web {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: radial-gradient(var(--accent) 0.5px, transparent 0.5px);
        background-size: 40px 40px;
        opacity: 0.15;
        pointer-events: none;
        z-index: 0;
    }

    .main-wrapper {
        position: relative;
        z-index: 1;
        max-width: 1200px;
        margin: auto;
        padding: 50px;
    }
    
    h1 {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        color: white;
        text-align: center;
        margin-bottom: 2rem !important;
    }
    
    .glass-box {
        background: var(--glass);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 40px;
        border-radius: 30px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    }
    
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        padding: 25px !important;
        font-size: 1.1rem !important;
    }
    
    .footer {
        text-align: center;
        color: #444;
        font-family: monospace;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []
if 'current_code' not in st.session_state: st.session_state.current_code = "<!-- Project Initialized -->"

st.markdown('<div class="spider-web"></div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)
    st.markdown("<h1>Start with one prompt.<br>You can change everything later.</h1>", unsafe_allow_html=True)
    
    # تبويبات العمل
    tab1, tab2 = st.tabs(["🌐 Web App Engine", "📱 Mobile App Engine"])
    
    with tab1:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        prompt = st.text_input("", placeholder="Describe your web idea...", key="main_prompt")
        
        if st.button("Generate Experience 🚀"):
            # محرك توليد الكود (الأساس)
            st.session_state.current_code = f"""
            <div style="background:black; color:white; padding:20px; font-family:monospace; border-radius:10px;">
                <h2>Project: {prompt}</h2>
                <p>Generating intelligent components...</p>
                <div style="width:100%; height:20px; background:grey;">
                    <div style="width:100%; height:100%; background:cyan;"></div>
                </div>
                <p>Engine initialized successfully.</p>
            </div>
            """
            st.success("Engine deployed.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab2:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.text_input("", placeholder="Describe your mobile idea...", key="mobile_prompt")
        st.markdown('</div>', unsafe_allow_html=True)

    # المعاينة (الأساس)
    st.markdown("### 🖥️ Live Preview", unsafe_allow_html=True)
    components.html(st.session_state.current_code, height=300)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">SPIDER-AI // GENERATIVE ENGINE // V.2.0</div>', unsafe_allow_html=True)
