import streamlit as st
import re
from g4f.client import Client
import streamlit.components.v1 as components

# إعداد الصفحة لتكون بملء الشاشة
st.set_page_config(page_title="SPIDER-AI", layout="wide")

# تصميم بصري احترافي (السر في الـ CSS هنا)
st.markdown("""
    <style>
    /* تغيير الخطوط والخلفية */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono&display=swap');
    
    .stApp { background-color: #09090b; color: #f4f4f5; font-family: 'Inter', sans-serif; }
    
    /* جعل الـ Sidebar يبدو كجزء من IDE */
    [data-testid="stSidebar"] { background-color: #18181b; border-right: 1px solid #27272a; padding: 20px; }
    
    /* تصميم بطاقة المحادثة */
    .chat-bubble { background: #27272a; padding: 12px; border-radius: 8px; margin-bottom: 10px; font-size: 14px; border-left: 3px solid #2ea44f; }
    
    /* زر التوليد بتصميم عصري */
    div.stButton > button { background: #2ea44f; color: white; border: none; border-radius: 6px; padding: 10px 20px; width: 100%; font-weight: 600; }
    div.stButton > button:hover { background: #238636; }
    
    /* منطقة المعاينة */
    .preview-box { border: 1px solid #27272a; border-radius: 12px; overflow: hidden; background: white; }
    </style>
""", unsafe_allow_html=True)

# إدارة الحالة
if 'messages' not in st.session_state: st.session_state.messages = []
if 'generated_html' not in st.session_state: st.session_state.generated_html = ""

# الواجهة الجانبية (للدردشة)
with st.sidebar:
    st.markdown("### 🕸️ SPIDER-AI")
    st.caption("محرك التجسيد البرمجي")
    
    chat_box = st.container(height=400)
    for msg in st.session_state.messages:
        chat_box.markdown(f"<div class='chat-bubble'>{msg}</div>", unsafe_allow_html=True)
        
    user_input = st.text_area("وصف الفكرة:", height=100)
    if st.button("تجسيد المشروع"):
        st.session_state.messages.append(user_input)
        # هنا يتم استدعاء التوليد
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"Write a complete HTML/CSS/JS file for: {user_input}"}]
        )
        code = response.choices[0].message.content
        st.session_state.generated_html = re.sub(r'^```html\s*', '', code).replace('```', '')
        st.rerun()

# منطقة العرض الرئيسية (المعاينة)
st.markdown("### 🖥️ بيئة التجسيد الفوري")
if st.session_state.generated_html:
    with st.container():
        components.html(st.session_state.generated_html, height=650)
else:
    st.info("💡 انتظر التوجيهات... ابدأ بوصف فكرتك في القائمة الجانبية.")
