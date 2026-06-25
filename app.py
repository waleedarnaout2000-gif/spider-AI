import streamlit as st
import streamlit.components.v1 as components
import time

# إعدادات الصفحة
st.set_page_config(page_title="SPIDER-AI | محرك التطوير الذكي", layout="wide")

# CSS احترافي يدمج بين تصاميمك اليدوية وروح البرمجة الحديثة
st.markdown("""
    <style>
    :root { --bg: #0b0e14; --panel: #161b22; --accent: #00d4ff; }
    .main { background-color: var(--bg); }
    .stApp { background-color: var(--bg); }
    h1, h2, h3 { color: #ffffff; font-family: 'Segoe UI', sans-serif; }
    
    /* لوحة المحادثة */
    .chat-container { background: var(--panel); border-radius: 12px; padding: 20px; border: 1px solid #30363d; height: 400px; overflow-y: auto; }
    
    /* محاكي المتصفح (المعاينة) */
    .browser-frame { 
        background: #0d1117; border-radius: 12px; border: 2px solid #30363d; 
        box-shadow: 0 20px 40px rgba(0,0,0,0.5); overflow: hidden;
    }
    .browser-header { background: #21262d; padding: 10px; display: flex; gap: 8px; }
    .dot { width: 10px; height: 10px; border-radius: 50%; background: #ff5f56; }
    
    /* الأزرار */
    .stButton>button { border-radius: 8px; border: 1px solid var(--accent); background: transparent; color: var(--accent); width: 100%; }
    .stButton>button:hover { background: var(--accent); color: black; }
    </style>
""", unsafe_allow_html=True)

# إدارة الحالة (الأساس البرمجي)
if 'history' not in st.session_state: st.session_state.history = []
if 'chat_log' not in st.session_state: st.session_state.chat_log = []
if 'code' not in st.session_state: st.session_state.code = "<h1>SPIDER-AI</h1><p>ابدأ البرمجة الآن...</p>"

# الهيكل الجانبي (من واقع رسمك)
with st.sidebar:
    st.markdown("## 🕸️ SPIDER-AI")
    st.write("المنصة الذكية لبناء المواقع")
    st.divider()
    
    # تحكم في الإصدارات
    st.markdown("### ⏳ سجل الإصدارات")
    version = st.selectbox("اختر إصداراً للمعاينة:", [f"الإصدار {i+1}" for i in range(len(st.session_state.history))] or ["لا توجد إصدارات"])
    
    st.divider()
    st.markdown("### 📊 الأهداف المالية")
    subs = st.slider("عدد المشتركين:", 100, 100000, 5000)
    st.markdown(f"**الدخل المتوقع:** ${subs * 5:,}")
    
    st.divider()
    if st.button("تسجيل دخول"): st.write("جاري الانتقال...")
    if st.button("حساب جديد"): st.write("جاري الانتقال...")

# الواجهة الرئيسية
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### 💬 المحادثة البرمجية")
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.chat_log:
            st.write(f"**{msg['role']}:** {msg['text']}")
        
        prompt = st.text_input("اكتب فكرتك هنا...", key="user_prompt")
        if st.button("إرسال التوجيه"):
            st.session_state.chat_log.append({"role": "مستخدم", "text": prompt})
            # هنا يتم ربط منطق التوليد
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 🌐 المعاينة الحية")
    st.markdown('''
        <div class="browser-frame">
            <div class="browser-header"><div class="dot"></div><div class="dot" style="background:#ffbd2e;"></div><div class="dot" style="background:#27c93f;"></div></div>
    ''', unsafe_allow_html=True)
    components.html(st.session_state.code, height=500)
    st.markdown('</div>', unsafe_allow_html=True)
