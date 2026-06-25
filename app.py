import streamlit as st
import re
import time
from g4f.client import Client
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(page_title="SPIDER-AI Engine", page_icon="🕷️", layout="wide")

# CSS المحسن (Modern Tech Style)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono&display=swap');
    :root { --bg: #09090b; --sidebar: #18181b; --accent: #2ea44f; }
    [data-testid="stAppViewContainer"] { background-color: var(--bg); font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: var(--sidebar); border-left: 1px solid #27272a; padding: 20px; }
    .chat-msg { background: #27272a; padding: 12px; border-radius: 8px; margin-bottom: 10px; color: #e4e4e7; font-size: 14px; }
    h1, h2 { color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 6px; background: var(--accent); color: white; border: none; }
    </style>
""", unsafe_allow_html=True)

# إدارة الحالة
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "agent", "content": "أنا SPIDER-AI. صف لي مشروعك وسأقوم بتجسيده برمجياً."}]
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = "discussion"
if 'generated_html' not in st.session_state:
    st.session_state.generated_html = ""

client = Client()

def ask_agent(prompt):
    system_prompt = "You are a senior developer. Output ONLY valid, clean HTML/CSS/JS in a single file. No markdown blocks, no placeholders. Arabic text inside UI."
    try:
        response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}])
        return response.choices[0].message.content.strip()
    except: return "ERROR_API"

# --- الواجهة ---

with st.sidebar:
    st.title("🕷️ SPIDER-AI")
    st.write("---")
    chat_container = st.container(height=500)
    for msg in st.session_state.messages:
        chat_container.markdown(f"<div class='chat-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    
    user_input = st.text_input("أدخل فكرتك...")
    if st.button("توليد التجسيد"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.current_stage = "generating"
        st.rerun()

# منطقة المعاينة الرئيسية
if st.session_state.current_stage == "generating":
    with st.spinner("جاري بناء المحرك التفاعلي..."):
        full_prompt = f"Build this project: {user_input}. Ensure it is a complete single-file HTML/CSS/JS app."
        code = ask_agent(full_prompt)
        # تنظيف الكود
        code = re.sub(r'^```html\s*', '', code).replace('```', '')
        st.session_state.generated_html = code
        st.session_state.current_stage = "finished"
        st.rerun()

elif st.session_state.current_stage == "finished":
    st.markdown("### 🖥️ المعاينة الحية (Live View)")
    components.html(st.session_state.generated_html, height=700, scrolling=True)
    if st.button("إعادة المحادثة"):
        st.session_state.current_stage = "discussion"
        st.rerun()
else:
    st.markdown("## مرحباً بك في SPIDER-AI")
    st.info("اختر فكرتك من القائمة الجانبية لنبدأ عملية التجسيد البرمجي.")
