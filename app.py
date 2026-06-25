import streamlit as st
import re
import time
from g4f.client import Client
import streamlit.components.v1 as components

# --- إعدادات الصفحة ---
st.set_page_config(page_title="SPIDER-AI | Next Gen", layout="wide", page_icon="🕷️")

# --- التصميم الاحترافي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root { --bg-dark: #09090b; --panel: #18181b; --accent: #2ea44f; --text: #f4f4f5; }
    
    .stApp { background-color: var(--bg-dark); color: var(--text); font-family: 'Inter', sans-serif; }
    
    /* الـ Sidebar الاحترافي */
    [data-testid="stSidebar"] { background-color: var(--panel); border-right: 1px solid #27272a; padding: 1rem; }
    
    /* بطاقات المحادثة الأنيقة */
    .chat-bubble { background: #27272a; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border-left: 4px solid var(--accent); font-size: 14px; }
    
    /* منطقة التفكير */
    .thinking-box { background: #000; border: 1px solid #333; padding: 1rem; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #a1a1aa; }
    
    /* الأزرار */
    div.stButton > button { background: var(--accent); color: white; border: none; border-radius: 6px; width: 100%; height: 45px; font-weight: 600; transition: 0.3s; }
    div.stButton > button:hover { opacity: 0.9; transform: translateY(-2px); box-shadow: 0 4px 15px rgba(46, 164, 79, 0.3); }
    
    /* تنظيف الواجهة */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- إدارة الجلسة ---
if 'messages' not in st.session_state: st.session_state.messages = []
if 'current_stage' not in st.session_state: st.session_state.current_stage = "discussion"
if 'generated_html' not in st.session_state: st.session_state.generated_html = ""

client = Client()

# --- دالة الذكاء الاصطناعي (كما هي، مع تحسين البرومبت) ---
def ask_agent(prompt):
    system_prompt = "You are a senior elite developer. Output ONLY clean, full HTML/CSS/JS in one file. No markdown, no placeholders. Arabic UI."
    try:
        response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}])
        return response.choices[0].message.content.strip()
    except: return "ERROR"

# --- الواجهة ---
with st.sidebar:
    st.markdown("## 🕷️ SPIDER-AI")
    st.markdown("---")
    chat_placeholder = st.container(height=450)
    for msg in st.session_state.messages:
        chat_placeholder.markdown(f"<div class='chat-bubble'>{msg['content']}</div>", unsafe_allow_html=True)

    with st.form("input_form", clear_on_submit=True):
        user_input = st.text_input("أدخل فكرتك:", placeholder="مثال: لعبة نيون أونلاين...")
        if st.form_submit_button("بدء التجسيد"):
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.current_stage = "generating"
            st.rerun()

# --- منطقة العرض الرئيسية ---
if st.session_state.current_stage == "generating":
    st.markdown("### 🛠️ المحرك البرمجي يعمل...")
    status = st.empty()
    status.markdown("<div class='thinking-box'>جاري تحليل البنية الأساسية...</div>", unsafe_allow_html=True)
    time.sleep(1)
    status.markdown("<div class='thinking-box'>توليد الواجهة التفاعلية...</div>", unsafe_allow_html=True)
    
    code = ask_agent(f"Generate full project for: {st.session_state.messages[-1]['content']}")
    st.session_state.generated_html = re.sub(r'^```html\s*', '', code).replace('```', '')
    st.session_state.current_stage = "finished"
    st.rerun()

elif st.session_state.current_stage == "finished":
    st.markdown("### 🖥️ النتيجة النهائية (Live Preview)")
    components.html(st.session_state.generated_html, height=700, scrolling=True)
    if st.button("تطوير فكرة جديدة"):
        st.session_state.current_stage = "discussion"
        st.rerun()

else:
    st.title("مرحباً بك في عالم التجسيد")
    st.write("استخدم القائمة الجانبية لبدء مشروعك القادم.")
