import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة
st.set_page_config(page_title="SPIDER-AI Engine", layout="wide")

# محرك الستايلات (الأسود الملكي والأخضر المضيء)
st.markdown("""
    <style>
    :root { --royal-black: #050505; --neon-green: #00FF41; --panel-bg: #111111; }
    .stApp { background-color: var(--royal-black); color: #e2e8f0; }
    
    /* تصميم الأزرار والقوائم */
    .nav-btn { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid var(--neon-green); 
               background: transparent; color: var(--neon-green); border-radius: 5px; cursor: pointer; }
    .nav-btn:hover { background: var(--neon-green); color: black; }
    
    .panel { background: var(--panel-bg); padding: 20px; border-radius: 10px; border: 1px solid #333; }
    h1, h2 { color: var(--neon-green); }
    </style>
""", unsafe_allow_html=True)

# إدارة حالة التنقل
if 'page' not in st.session_state: st.session_state.page = 'landing'
if 'history' not in st.session_state: st.session_state.history = []

# القائمة الجانبية للتنقل
with st.sidebar:
    st.markdown("## 🕸️ SPIDER-AI")
    if st.button("الرئيسية", key="nav_landing"): st.session_state.page = 'landing'
    if st.button("لوحة التحكم", key="nav_dashboard"): st.session_state.page = 'dashboard'
    if st.button("معرض الأكواد", key="nav_editor"): st.session_state.page = 'editor'
    if st.button("المعاينة الحية", key="nav_preview"): st.session_state.page = 'preview'
    if st.button("الإعدادات", key="nav_settings"): st.session_state.page = 'settings'

# المنطق الأساسي للتنقل بين الصفحات
if st.session_state.page == 'landing':
    st.title("أهلاً بك في SPIDER-AI")
    st.write("حول فكرتك إلى واقع برمجيات احترافي.")

elif st.session_state.page == 'dashboard':
    st.title("لوحة التحكم")
    st.info("هنا ستظهر إحصائيات مشاريعك وحالة النظام.")

elif st.session_state.page == 'editor':
    st.title("معرض الأكواد")
    user_prompt = st.text_area("صف فكرتك هنا:")
    if st.button("توليد الكود"):
        st.session_state.history.append(user_prompt)
        st.success("تم التوليد بنجاح!")

elif st.session_state.page == 'preview':
    st.title("المعاينة الحية")
    if st.session_state.history:
        components.html(f"<html><body style='color:green;'>{st.session_state.history[-1]}</body></html>", height=400)
    else:
        st.warning("لا يوجد مشروع حالياً للمعاينة.")

elif st.session_state.page == 'settings':
    st.title("الإعدادات")
    st.selectbox("اللغة:", ["العربية", "English"])
