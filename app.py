import streamlit as st
import re
from g4f.client import Client
import streamlit.components.v1 as components

# إعدادات متقدمة
st.set_page_config(page_title="SPIDER-AI: Enterprise Edition", layout="wide")

# CSS العملاق للتصميم الاحترافي
st.markdown("""
    <style>
    .ide-container { background: #09090b; border: 1px solid #27272a; border-radius: 12px; padding: 20px; color: #e4e4e7; }
    .nav-tab { padding: 10px 20px; cursor: pointer; border-bottom: 2px solid transparent; }
    .nav-tab:hover { border-bottom: 2px solid #2ea44f; }
    .sidebar-content { font-family: 'JetBrains Mono'; font-size: 12px; }
    .code-block { background: #000; border: 1px solid #333; padding: 15px; border-radius: 8px; overflow-x: auto; }
    </style>
""", unsafe_allow_html=True)

# إدارة البيانات الكبيرة
if 'projects' not in st.session_state: st.session_state.projects = []
if 'active_tab' not in st.session_state: st.session_state.active_tab = "الدردشة"

# الـ Sidebar الاحترافي للمشاريع
with st.sidebar:
    st.markdown("### 🕸️ SPIDER-AI Core")
    st.write("---")
    if st.button("➕ مشروع جديد"):
        st.session_state.projects.append({"name": "مشروع تجسيد جديد", "code": ""})
    
    for i, proj in enumerate(st.session_state.projects):
        if st.button(f"📁 {proj['name']}"):
            st.session_state.active_project = i

# التبويبات الرئيسية (العمود الفقري للنظام)
tab1, tab2, tab3 = st.tabs(["💬 المحادثة الذكية", "💻 كود المصدري", "🚀 بيئة المعاينة"])

with tab1:
    st.markdown("### 🤖 وكيل البرمجيات المتخصص")
    user_prompt = st.text_area("صف المهمة البرمجية العملاقة:")
    if st.button("بدء التجسيد البرمجي"):
        client = Client()
        response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": user_prompt}])
        st.session_state.last_code = response.choices[0].message.content
        st.success("تم التجسيد بنجاح!")

with tab2:
    st.markdown("### 💻 كود المشروع المولد")
    if 'last_code' in st.session_state:
        st.code(st.session_state.last_code, language="html")

with tab3:
    st.markdown("### 🚀 معاينة حية (Live Engine)")
    if 'last_code' in st.session_state:
        clean_code = re.sub(r'```html\s*', '', st.session_state.last_code).replace('```', '')
        components.html(clean_code, height=600, scrolling=True)
    else:
        st.warning("لا يوجد كود للمعاينة حالياً.")

# تذييل احترافي
st.markdown("---")
st.caption("SPIDER-AI Engine v1.0.0 | نظام تجسيد تفاعلي")
