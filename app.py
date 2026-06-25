import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="SPIDER-AI", layout="wide")

# تصميم القائمة الجانبية (بناءً على دائرتك رقم 8)
with st.sidebar:
    st.title("🕷️ SPIDER-AI")
    st.markdown("---")
    st.button("🏠 الرئيسية")
    st.button("⚙️ الإعدادات")
    st.button("👤 البروفايل")
    st.markdown("---")
    st.subheader("أدوات التحكم")
    st.write("🔧 توليد تطبيقات")
    st.write("🎨 تصميم واجهات")

# الهيدر العلوي
st.header("لوحة التحكم - SPIDER-AI")

# منطقة العمل الرئيسية (كما في أسهمك)
# نستخدم أعمدة لتوزيع الصورة والبيانات والمدخلات
main_col, side_info_col = st.columns([3, 1])

with main_col:
    # منطقة كتابة الفكرة (الوسط)
    user_idea = st.text_area("اكتب فكرتك هنا لتوليد التطبيق أو اللعبة:", height=200, placeholder="مثال: أريد لعبة سباق سيارات بسيطة...")
    
    # زر التنفيذ
    if st.button("🚀 توليد المشروع الآن"):
        st.success("تم استلام الفكرة! جاري المعالجة...")
        # هنا سيظهر لاحقاً عرض النتائج/الصور

with side_info_col:
    # معلومات إضافية عن الموقع
    st.info("معلومات عن الموقع")
    st.write("هذا الموقع يساعدك في تحويل أفكارك إلى واقع برمجي بسرعة.")

# تذييل الصفحة
st.markdown("---")
st.caption("SPIDER-AI - جميع الحقوق محفوظة")
