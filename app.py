import streamlit as st
import re
import time
from g4f.client import Client
import streamlit.components.v1 as components

# --- إعدادات الصفحة ---
st.set_page_config(page_title="SPIDER-AI", page_icon="🕷️", layout="wide")

# --- التنسيق الاحترافي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, .main { font-family: 'Cairo', sans-serif; direction: rtl; background-color: #0d1117; color: #c9d1d9; }
    .chat-card { padding: 15px; border-radius: 10px; margin-bottom: 15px; }
    .user-msg { background-color: #21262d; border-right: 4px solid #58a6ff; }
    .agent-msg { background-color: #161b22; border-right: 4px solid #2ea44f; }
    .thinking-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin: 10px 0; font-size: 13px; color: #8b949e; }
    div.stButton > button { background: linear-gradient(135deg, #238636, #2ea44f); color: white; border: none; width: 100%; border-radius: 6px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- إدارة الحالة (Session State) ---
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "agent", "content": "مرحباً في SPIDER-AI! أنا مهندس البرمجيات الخاص بك. ما هي فكرتك اليوم؟"}]
if 'current_stage' not in st.session_state: st.session_state.current_stage = "discussion"
if 'generated_html' not in st.session_state: st.session_state.generated_html = ""
if 'error_occurred' not in st.session_state: st.session_state.error_occurred = False

client = Client()

def ask_agent(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are an expert coder. Output ONLY clean HTML/JS code."}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except: return "ERROR_API_FAILED"

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("## 🕷️ SPIDER-AI")
    st.write("---")
    if st.button("🏠 لوحة التحكم"): st.session_state.current_stage = "discussion"
    if st.button("⚙️ الإعدادات"): st.warning("قيد التطوير")
    st.write("---")
    st.metric(label="رصيد النقاط المتاح", value="10,000")
    st.info("النسخة: تجريبية (Beta)")

# --- الواجهة الرئيسية (Dashboard) ---
if st.session_state.current_stage == "finished":
    components.html(st.session_state.generated_html, height=750, scrolling=True)
    if st.button("⬅️ العودة للمحادثة"):
        st.session_state.current_stage = "discussion"
        st.rerun()
else:
    st.title("لوحة تحكم SPIDER-AI")
    col1, col2 = st.columns([0.7, 0.3])
    
    with col1:
        st.markdown("### 💬 سجل المحادثة")
        chat_container = st.container(height=400)
        with chat_container:
            for msg in st.session_state.messages:
                cls = "user-msg" if msg["role"] == "user" else "agent-msg"
                st.markdown(f"<div class='chat-card {cls}'>{msg['content']}</div>", unsafe_allow_html=True)
        
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("اكتب فكرتك هنا:")
            if st.form_submit_button("إرسال"):
                st.session_state.messages.append({"role": "user", "content": user_input})
                if any(word in user_input for word in ["ابدا", "انشئ", "برمج"]):
                    st.session_state.current_stage = "generating"
                else:
                    reply = ask_agent(user_input)
                    st.session_state.messages.append({"role": "agent", "content": reply})
                st.rerun()

    with col2:
        st.markdown("### 🛠️ حالة التوليد")
        if st.session_state.current_stage == "generating":
            st.info("⏳ جاري تحليل الفكرة وبناء الكود...")
            # هنا يمكنك إضافة منطق التوليد الفعلي
            full_code = ask_agent("Generate a full HTML file for: " + str(st.session_state.messages[-1]))
            st.session_state.generated_html = full_code
            st.session_state.current_stage = "finished"
            st.rerun()
        else:
            st.write("بانتظار تعليماتك للبدء في البرمجة.")
