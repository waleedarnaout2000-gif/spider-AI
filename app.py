import streamlit as st
import re
import time
from g4f.client import Client
import streamlit.components.v1 as components

# إعدادات الصفحة والتصميم العام
st.set_page_config(page_title="Emergent Engine", page_icon="🤖", layout="wide")

# تصميم واجهة مستخدم مظلمة واحترافية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Fira+Code:wght@400;500&display=swap');
    html, body, .main { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; background-color: #0d1117; color: #c9d1d9; }
    h1, h2, h3, p, label { color: #f0f6fc; text-align: right; }

    .chat-card { padding: 15px; border-radius: 10px; margin-bottom: 15px; line-height: 1.6; }
    .user-msg { background-color: #21262d; border-right: 4px solid #58a6ff; }
    .agent-msg { background-color: #161b22; border-right: 4px solid #2ea44f; }

    .thinking-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin: 10px 0; font-family: 'Fira Code', monospace; font-size: 13px; color: #8b949e; direction: ltr; text-align: left; }
    .step-done { color: #56d364; }
    .step-active { color: #58a6ff; font-weight: bold; animation: blink 1s infinite; }
    @keyframes blink { 50% { opacity: 0.5; } }

    div.stButton > button:first-child {
        background: linear-gradient(135deg, #238636, #2ea44f); color: white;
        border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; width: 100%; transition: 0.2s;
    }
    div.stButton > button:first-child:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(46, 164, 79, 0.3); }

    .error-card {
        background-color: #3b1212; padding: 20px; border-radius: 10px; border: 1px solid #f85149;
        color: #ff7b72; margin-bottom: 20px; text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# إدارة بيانات الجلسة
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "agent", "content": "مرحباً! أنا مهندس البرمجيات الذكي. ضع هنا فكرتك البرمجية وسأقوم ببنائها فوراً."}]
if 'generated_html' not in st.session_state: st.session_state.generated_html = ""
if 'current_stage' not in st.session_state: st.session_state.current_stage = "discussion"
if 'code_blocks' not in st.session_state: st.session_state.code_blocks = {}
if 'error_occurred' not in st.session_state: st.session_state.error_occurred = False

client = Client()

def ask_agent(prompt):
    system_prompt = "You are an expert developer. Output full, self-contained HTML/CSS/JS code. No placeholders. Arabic interface."
    try:
        response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}])
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR_API_FAILED: {str(e)}"

# واجهة المستخدم
if st.session_state.current_stage in ["discussion", "generating"]:
    st.markdown("## 🤖 المهندس البرمجي الذكي")
    col_chat, col_steps = st.columns([1.2, 1])

    with col_chat:
        chat_placeholder = st.container(height=400)
        with chat_placeholder:
            for msg in st.session_state.messages:
                cls = "user-msg" if msg["role"] == "user" else "agent-msg"
                st.markdown(f"<div class='chat-card {cls}'>{msg['content']}</div>", unsafe_allow_html=True)

        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("اكتب فكرتك البرمجية هنا:")
            submit_chat = st.form_submit_button("إرسال")

        if submit_chat and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})
            if any(word in user_input for word in ["ابدا", "انشئ", "برمج", "بناء"]):
                st.session_state.current_stage = "generating"
                st.rerun()
            else:
                agent_reply = ask_agent(f"User: {user_input}. Ask 2 architectural questions.")
                st.session_state.messages.append({"role": "agent", "content": agent_reply})
                st.rerun()

    with col_steps:
        if st.session_state.current_stage == "generating":
            status_box = st.empty()
            status_box.markdown("<div class='thinking-box'><div class='step-active'>⏳ جاري التوليد...</div></div>", unsafe_allow_html=True)
            final_code = ask_agent("Generate full code for: " + str(st.session_state.messages))
            if "ERROR_API_FAILED" in final_code:
                st.session_state.error_occurred = True
                st.session_state.current_stage = "discussion"
            else:
                st.session_state.generated_html = final_code
                st.session_state.current_stage = "finished"
            st.rerun()

elif st.session_state.current_stage == "finished":
    components.html(st.session_state.generated_html, height=750, scrolling=True)
    if st.button("🔄 العودة للمحادثة"):
        st.session_state.current_stage = "discussion"
        st.rerun()
