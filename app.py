import streamlit as st
import re
import time
from g4f.client import Client
import streamlit.components.v1 as components

# --- إعدادات الصفحة والتصميم العام للمنصة ---
st.set_page_config(page_title="Emergent Engine", page_icon="🤖", layout="wide")

# تصميم واجهة مستخدم مظلمة واحترافية تحاكي البيئات البرمجية المتقدمة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Fira+Code:wght@400;500&display=swap');
    html, body, .main { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; background-color: #0d1117; color: #c9d1d9; }
    h1, h2, h3, p, label { color: #f0f6fc; text-align: right; }
    
    /* صناديق المحادثة السينمائية */
    .chat-card { padding: 15px; border-radius: 10px; margin-bottom: 15px; line-height: 1.6; }
    .user-msg { background-color: #21262d; border-right: 4px solid #58a6ff; }
    .agent-msg { background-color: #161b22; border-right: 4px solid #2ea44f; }
    
    /* مؤشرات تفكير الوكيل البرمجي */
    .thinking-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin: 10px 0; font-family: 'Fira Code', monospace; font-size: 13px; color: #8b949e; direction: ltr; text-align: left; }
    .step-done { color: #56d364; }
    .step-active { color: #58a6ff; font-weight: bold; animation: blink 1s infinite; }
    @keyframes blink { 50% { opacity: 0.5; } }
    
    /* أزرار مخصصة فخمة */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #238636, #2ea44f); color: white;
        border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; width: 100%; transition: 0.2s;
    }
    div.stButton > button:first-child:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(46, 164, 79, 0.3); }
    
    /* تصميم بطاقات الأخطاء الذكية */
    .error-card {
        background-color: #3b1212;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #f85149;
        color: #ff7b72;
        margin-bottom: 20px;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# --- إدارة وتخزين بيانات الجلسة (State Management) ---
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "agent", "content": "مرحباً بك! أنا مهندس البرمجيات الذكي الخاص بك. ضع هنا فكرتك البرمجية (موقع، تطبيق، لعبة 2D تفاعلية، أو لعبة 3D متطورة)، وسأقوم بمناقشتها معك وبنائها فوراً."}]
if 'generated_html' not in st.session_state:
    st.session_state.generated_html = ""
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = "discussion"
if 'code_blocks' not in st.session_state:
    st.session_state.code_blocks = {}
if 'error_occurred' not in st.session_state:
    st.session_state.error_occurred = False

client = Client()

# --- دالة الذكاء الاصطناعي ---
def ask_agent(prompt):
    system_prompt = """You are a senior full-stack developer. Output flawless single-file HTML/CSS/JS code. Return ONLY clean HTML code."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR_API_FAILED: {str(e)}"

# --- واجهة وتجربة المستخدم ---
if st.session_state.current_stage in ["discussion", "generating"]:
    st.markdown("## 🤖 المهندس البرمجي الذكي (الجيل القادم)")
    col_chat, col_steps = st.columns([1.2, 1])
    
    with col_chat:
        st.markdown("### 💬 سجل المحادثة الفعلية")
        for msg in st.session_state.messages:
            cls = "user-msg" if msg["role"] == "user" else "agent-msg"
            st.markdown(f"<div class='chat-card {cls}'>{msg['content']}</div>", unsafe_allow_html=True)
        
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("اكتب فكرتك البرمجية هنا:")
            submit_chat = st.form_submit_button("إرسال التوجيه")
            
        if submit_chat and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})
            if any(word in user_input for word in ["ابدا", "انشئ", "بناء", "ابدأ", "أنشئ"]):
                st.session_state.current_stage = "generating"
            else:
                agent_reply = ask_agent(f"User idea: {user_input}. Respond in Arabic.")
                st.session_state.messages.append({"role": "agent", "content": agent_reply})
            st.rerun()

    with col_steps:
        st.markdown("### 🛠️ خطوات العمل")
        if st.session_state.current_stage == "generating":
            st.markdown("<div class='thinking-box'><div class='step-active'>⏳ جاري التوليد...</div></div>", unsafe_allow_html=True)
            final_generated = ask_agent("Create a full project based on previous chat.")
            st.session_state.generated_html = final_generated
            st.session_state.current_stage = "finished"
            st.rerun()

elif st.session_state.current_stage == "finished":
    components.html(st.session_state.generated_html, height=750, scrolling=True)
    if st.button("🔄 العودة للمحادثة"):
        st.session_state.current_stage = "discussion"
        st.rerun()
