import streamlit as st

# إعداد الصفحة لتكون واسعة وتدعم التأثيرات البصرية
st.set_page_config(page_title="SPIDER-AI", layout="wide")

# محرك الستايلات المتطور (تنسيق مطابق للرسومات التخطيطية)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
        font-family: 'Tajawal', sans-serif;
        color: white;
    }
    
    /* تصميم الهيكل التخطيطي */
    .header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-box {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid #38bdf8;
        border-radius: 20px;
        padding: 40px;
        margin-top: 50px;
        text-align: center;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        margin-top: 40px;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.3s;
    }
    
    .feature-card:hover {
        transform: scale(1.02);
        border-color: #38bdf8;
    }
    </style>
""", unsafe_allow_html=True)

# 1. الشريط العلوي (مطابق للرسم التخطيطي)
st.markdown("""
    <div class="header-bar">
        <h1>SPIDER-AI</h1>
        <div>
            <button style="background:transparent; color:white; border:1px solid white; padding:5px 15px; border-radius:5px; margin-right:10px;">تسجيل دخول</button>
            <button style="background:#38bdf8; color:white; border:none; padding:5px 15px; border-radius:5px;">إنشاء حساب</button>
        </div>
    </div>
""", unsafe_allow_html=True)

# 2. منطقة الإدخال المركزية (مطابقة لصورة 45603)
st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.write("<h2>هنا يتم توليد التطبيق</h2>")
user_input = st.text_area("أدخل فكرتك هنا...", height=150, label_visibility="collapsed")
if st.button("توليد 🚀"):
    st.success("جاري البرمجة...")
st.markdown('</div>', unsafe_allow_html=True)

# 3. المربعات السفلية (مطابقة لصورة 45602)
st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
st.markdown('<div class="feature-card"><h3>صور عن الأداة</h3><p>شرح لكيفية عمل المنصة</p></div>', unsafe_allow_html=True)
st.markdown('<div class="feature-card"><h3>صور عن الأداة</h3><p>المزيد من التفاصيل والنتائج</p></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
