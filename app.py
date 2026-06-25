import streamlit as st

# إعداد الصفحة لتكون واسعة وتدعم التأثيرات البصرية
st.set_page_config(page_title="SPIDER-AI", layout="wide")

# محرك الستايلات المتطور (Glassmorphism + Scroll Animations)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
        font-family: 'Tajawal', sans-serif;
        color: white;
    }
    
    /* تصميم الـ Hero Section (المركز) */
    .hero {
        text-align: center;
        padding: 100px 20px;
        animation: fadeIn 1.5s ease-out;
    }
    
    /* تأثير الانبثاق عند التمرير */
    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 20px;
        margin: 20px 0;
        transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.6s;
    }
    
    .scroll-reveal {
        opacity: 1;
        transform: translateY(20px);
    }
    
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    
    .chat-box {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid #38bdf8;
        border-radius: 15px;
        padding: 20px;
        width: 80%;
        margin: 0 auto;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 1. قسم الواجهة الرئيسية (الهيرو)
st.markdown("""
    <div class="hero">
        <h1>SPIDER-AI</h1>
        <p style="font-size: 1.5rem; color: #94a3b8;">ابدأ ببرومبت واحد.. وغير كل شيء لاحقاً</p>
    </div>
""", unsafe_allow_html=True)

# 2. منطقة المحادثة (الأساس البرمجي)
st.markdown('<div class="chat-box">', unsafe_allow_html=True)
user_input = st.text_area("صف فكرتك وسنحولها لواقع..", height=150, label_visibility="collapsed")
if st.button("توليد التطبيق 🚀"):
    st.success("جاري بناء المحرك الخاص بك...")
st.markdown('</div>', unsafe_allow_html=True)

# 3. قسم الانبثاق (المعلومات والمميزات)
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("### 🕸️ اكتشف قدرات المنصة")

cols = st.columns(3)
with cols[0]:
    st.markdown('<div class="feature-card"><h3>محرك ذكي</h3><p>توليد كود لحظي</p></div>', unsafe_allow_html=True)
with cols[1]:
    st.markdown('<div class="feature-card"><h3>معاينة حية</h3><p>شاهد تطبيقك فوراً</p></div>', unsafe_allow_html=True)
with cols[2]:
    st.markdown('<div class="feature-card"><h3>تعديل مرن</h3><p>تحكم بكل بكسل</p></div>', unsafe_allow_html=True)

# تذييل الصفحة
st.markdown("<br><br><center>© 2026 SPIDER-AI Engine</center>", unsafe_allow_html=True)
