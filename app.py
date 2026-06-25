import streamlit as st
from streamlit_option_menu import option_menu

# إعداد الصفحة لتكون واسعة (Wide Mode)
st.set_page_config(page_title="SPIDER-AI", layout="wide")

# تنسيق CSS مخصص ليشبه Tailwind (مظهر عصري)
st.markdown("""
    <style>
    .main {background-color: #f8fafc;}
    .stButton>button {width: 100%; border-radius: 10px; font-weight: bold;}
    .css-1r6slb0 {padding: 2rem;} /* تحسين التباعد للموبايل */
    </style>
""", unsafe_allow_html=True)

# 1. الـ Header (الشعار وأزرار التحكم)
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🕷️ SPIDER-AI")
    with col2:
        if st.button("⚙️ الإعدادات"):
            st.write("تم فتح الإعدادات")

# 2. نظام الصفحات (التبديل بين التسجيل والرئيسية)
selected = option_menu(
    menu_title=None,
    options=["تسجيل الدخول", "مولد الأفكار"],
    icons=["person-circle", "robot"],
    orientation="horizontal",
)

# 3. محتوى الصفحات
if selected == "تسجيل الدخول":
    st.header("مرحباً بك في SPIDER-AI")
    st.text_input("البريد الإلكتروني")
    st.text_input("كلمة المرور", type="password")
    st.button("دخول")
    st.info("ليس لديك حساب؟ سجل الآن")

elif selected == "مولد الأفكار":
    st.header("لوحة التحكم: مولد التطبيقات")
    
    # تقسيم الشاشة (يتجاوب تلقائياً مع الموبايل)
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        idea = st.text_area("اكتب فكرتك هنا...", height=150)
        if st.button("توليد التطبيق 🚀"):
            st.success("جاري التفكير في فكرتك...")
            
    with right_col:
        st.subheader("الأدوات المتاحة")
        st.write("✅ توليد أكواد")
        st.write("✅ تحسين التصميم")
